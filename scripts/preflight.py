#!/usr/bin/env python3
"""
preflight.py
============
Free platform-constraint preflight for ANY Higgsfield model — video, image,
audio (and any future catalog section the CLI baseline grows). Nothing here
calls the platform: every verdict comes from committed files.

Two layers are checked for one request (model id + params + media roles):

  1. The model's enum / range surface from the generated specs
     (specs/model-specs.json, image-model-specs.json, audio-model-specs.json):
     option lists, numeric min/max, aspect ratios, accepted media roles, and
     the smart-duration sentinel (duration = -1 on models whose duration
     description says so — legal as the sentinel only, never as a length).
  2. The model's platform validation rules from specs/cli_baseline.json —
     the CEL strings the CLI returns in `higgsfield model get <id> --json`
     (e.g. `params.mode != "t2v" || size(params.image_references) == 0`).
     They are evaluated by the small parser below, which covers exactly the
     CEL subset the platform uses: literals (int, double, string, bool, null,
     list, map), `params.<field>`, `[]` indexing, `!` `-` `+` `-` `*` `/` `%`,
     `==` `!=` `<` `<=` `>` `>=` `in`, `&&` `||`, `?:`, `size()`, `has()`,
     `type()` with the CEL type names, `.matches()`, and the `.all()` /
     `.exists()` macros. It never calls eval().

FAIL CLOSED. A rule the evaluator cannot parse (an unsupported function, an
unknown identifier) or cannot evaluate (a type error) is reported UNCHECKED —
never a pass. `--strict` turns any UNCHECKED rule (and a model with no rule
set on record) into a non-zero exit. Rules are read dynamically from the
baseline; none are hard-coded here.

Evaluation is three-valued. The CLI (`complete` request) treats an omitted
param as the platform does — the spec default, else null — and an omitted
media role as absent. The Seedance linter calls in with `missing="unknown"`
instead: a prompt that never declares its media leaves those rules UNKNOWN
(reported as not evaluated), because the media may be attached in the UI.

Usage:
  python3 scripts/preflight.py --model seedance_2_5 --param mode=t2v \\
      --media start_image=1
  python3 scripts/preflight.py --model wan3_0 --param duration=-1
  python3 scripts/preflight.py --json '{"model": "seedance_2_5",
      "params": {"mode": "omni_reference"}, "media": {"image_references": 31}}'
  python3 scripts/preflight.py --input request.json [--strict] [--report-json]
  python3 scripts/preflight.py --check-rules [--strict]   # parse every rule

Exit codes: 0 = pass, 1 = any FAIL (or, with --strict, any UNCHECKED rule),
2 = usage error / unknown or ambiguous model.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

# The CLI's media-role params (start_image, image_references, mask, …): the
# same test the tripwire and the cross-check use.
from refresh_specs import is_media_role as is_cli_media_param

ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = ROOT / "specs"
BASELINE_DEFAULT = SPECS_DIR / "cli_baseline.json"
SPEC_FILES = {"video": "model-specs.json", "image": "image-model-specs.json",
              "audio": "audio-model-specs.json", "3d": "3d-model-specs.json"}
# models_explore (MCP) and the CLI name one media slot differently: the MCP
# role `image` is the CLI param `image_references` (specs/crosscheck_allowlist
# records it on image_auto, soul_cinematic, gpt_image_2 and the 3d image
# models). A request may use either spelling; checks and platform rules see
# the CLI name, because the rules are the CLI's.
MCP_TO_CLI_ROLE = {"image": "image_references"}


# ════════════════════════════════════════════════════════════════════════════
# CEL subset — tokenizer, parser, evaluator
# ════════════════════════════════════════════════════════════════════════════

class CelError(Exception):
    """Base class: anything that stops a rule from being checked."""


class CelParseError(CelError):
    """The rule uses syntax / a function outside the supported subset."""


class CelEvalError(CelError):
    """The rule parsed but could not be evaluated (type error, bad key)."""


class _Unknown:
    """Third truth value: the answer depends on an input nobody declared."""
    __slots__ = ()

    def __repr__(self):
        return "UNKNOWN"


UNKNOWN = _Unknown()


class CelType:
    """A CEL type value — what `type(x)` returns and `string`/`int` name."""
    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, CelType) and other.name == self.name

    def __hash__(self):
        return hash(("CelType", self.name))

    def __repr__(self):
        return self.name


TYPE_NAMES = {"int", "uint", "double", "bool", "string", "bytes", "list",
              "map", "null_type", "type"}
FUNCTIONS = {"size": 1, "has": 1, "type": 1}
METHODS = {"size": 0, "matches": 1}
MACROS = {"all", "exists"}  # x.all(v, pred) / x.exists(v, pred)

_TOKEN_RE = re.compile(r"""
    (?P<ws>\s+)
  | (?P<num>\d+\.\d+(?:[eE][+-]?\d+)?|\d+)
  | (?P<str>"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')
  | (?P<op>==|!=|<=|>=|&&|\|\||[<>!+\-*/%?:.,()\[\]{}])
  | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
""", re.X)
_ESCAPES = {"\\": "\\", '"': '"', "'": "'", "n": "\n", "t": "\t", "r": "\r"}


def _unescape(body: str) -> str:
    out, i = [], 0
    while i < len(body):
        ch = body[i]
        if ch == "\\":
            nxt = body[i + 1] if i + 1 < len(body) else ""
            if nxt not in _ESCAPES:
                raise CelParseError(f"unsupported string escape \\{nxt}")
            out.append(_ESCAPES[nxt])
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _tokenize(text: str) -> list[tuple[str, object]]:
    toks, pos = [], 0
    while pos < len(text):
        m = _TOKEN_RE.match(text, pos)
        if not m:
            raise CelParseError(f"unexpected character {text[pos]!r} at {pos}")
        pos = m.end()
        kind = m.lastgroup
        val = m.group(kind)
        if kind == "ws":
            continue
        if kind == "num":
            toks.append(("lit", float(val) if ("." in val or "e" in val.lower())
                         else int(val)))
        elif kind == "str":
            toks.append(("lit", _unescape(val[1:-1])))
        elif kind == "ident" and val in ("true", "false", "null"):
            toks.append(("lit", {"true": True, "false": False, "null": None}[val]))
        elif kind == "ident" and val == "in":
            toks.append(("op", "in"))
        else:
            toks.append((kind, val))
    return toks


class _Parser:
    """Recursive descent over the CEL precedence ladder:
    ?: < || < && < relations (== != < <= > >= in) < + - < * / % < unary < member."""

    def __init__(self, text: str):
        self.toks = _tokenize(text)
        self.i = 0

    def _peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def _accept(self, kind, val=None):
        k, v = self._peek()
        if k == kind and (val is None or v == val):
            self.i += 1
            return True
        return False

    def _expect(self, kind, val=None):
        if not self._accept(kind, val):
            got = self._peek()[1]
            raise CelParseError(f"expected {val or kind!r}, got {got!r}")

    def parse(self):
        if not self.toks:
            raise CelParseError("empty rule")
        node = self._expr()
        if self.i != len(self.toks):
            raise CelParseError(f"unexpected token {self._peek()[1]!r}")
        _validate(node, frozenset({"params"}))
        return node

    def _expr(self):
        cond = self._or()
        if self._accept("op", "?"):
            a = self._or()
            self._expect("op", ":")
            b = self._expr()
            return ("cond", cond, a, b)
        return cond

    def _or(self):
        node = self._and()
        while self._accept("op", "||"):
            node = ("or", node, self._and())
        return node

    def _and(self):
        node = self._rel()
        while self._accept("op", "&&"):
            node = ("and", node, self._rel())
        return node

    def _rel(self):
        node = self._add()
        while True:
            k, v = self._peek()
            if k == "op" and v in ("==", "!=", "<", "<=", ">", ">=", "in"):
                self.i += 1
                node = ("in", node, self._add()) if v == "in" else \
                    ("cmp", v, node, self._add())
            else:
                return node

    def _add(self):
        node = self._mul()
        while True:
            k, v = self._peek()
            if k == "op" and v in ("+", "-"):
                self.i += 1
                node = ("arith", v, node, self._mul())
            else:
                return node

    def _mul(self):
        node = self._unary()
        while True:
            k, v = self._peek()
            if k == "op" and v in ("*", "/", "%"):
                self.i += 1
                node = ("arith", v, node, self._unary())
            else:
                return node

    def _unary(self):
        if self._accept("op", "!"):
            return ("not", self._unary())
        if self._accept("op", "-"):
            return ("neg", self._unary())
        return self._member()

    def _args(self):
        args = []
        if self._accept("op", ")"):
            return args
        while True:
            args.append(self._expr())
            if self._accept("op", ")"):
                return args
            self._expect("op", ",")

    def _member(self):
        node = self._primary()
        while True:
            if self._accept("op", "."):
                k, name = self._peek()
                if k != "ident":
                    raise CelParseError(f"expected a field name after '.', got {name!r}")
                self.i += 1
                if self._accept("op", "("):
                    node = self._method(node, name, self._args())
                else:
                    node = ("select", node, name)
            elif self._accept("op", "["):
                idx = self._expr()
                self._expect("op", "]")
                node = ("index", node, idx)
            else:
                return node

    def _method(self, target, name, args):
        if name in MACROS:
            if len(args) != 2 or args[0][0] != "ident":
                raise CelParseError(f".{name}() takes (variable, predicate)")
            return ("macro", name, target, args[0][1], args[1])
        if name not in METHODS:
            raise CelParseError(f"unsupported method .{name}()")
        if len(args) != METHODS[name]:
            raise CelParseError(f".{name}() takes {METHODS[name]} argument(s)")
        if name == "size":
            return ("size", target)
        return ("matches", target, args[0])

    def _primary(self):
        k, v = self._peek()
        if k is None:
            raise CelParseError("unexpected end of rule")
        self.i += 1
        if k == "lit":
            return ("lit", v)
        if k == "ident":
            if self._accept("op", "("):
                args = self._args()
                if v not in FUNCTIONS:
                    raise CelParseError(f"unsupported function {v}()")
                if len(args) != FUNCTIONS[v]:
                    raise CelParseError(f"{v}() takes {FUNCTIONS[v]} argument")
                if v == "has":
                    if args[0][0] != "select":
                        raise CelParseError("has() needs a field selection")
                    return ("has", args[0][1], args[0][2])
                return (v, args[0])
            return ("ident", v)
        if (k, v) == ("op", "("):
            node = self._expr()
            self._expect("op", ")")
            return node
        if (k, v) == ("op", "["):
            items = []
            if not self._accept("op", "]"):
                while True:
                    items.append(self._expr())
                    if self._accept("op", "]"):
                        break
                    self._expect("op", ",")
            return ("list", items)
        if (k, v) == ("op", "{"):
            entries = []
            if not self._accept("op", "}"):
                while True:
                    key = self._expr()
                    self._expect("op", ":")
                    entries.append((key, self._expr()))
                    if self._accept("op", "}"):
                        break
                    self._expect("op", ",")
            return ("map", entries)
        raise CelParseError(f"unexpected token {v!r}")


def _validate(node, scope: frozenset):
    """Reject identifiers the evaluator cannot bind — at PARSE time, so the
    baseline coverage check (every rule parses) means every rule is
    evaluable, not merely tokenizable."""
    kind = node[0]
    if kind == "ident":
        if node[1] not in scope and node[1] not in TYPE_NAMES:
            raise CelParseError(f"unknown identifier {node[1]!r}")
        return
    if kind == "lit":
        return
    if kind == "macro":
        _validate(node[2], scope)
        _validate(node[4], scope | {node[3]})
        return
    if kind == "map":
        for k, v in node[1]:
            _validate(k, scope)
            _validate(v, scope)
        return
    if kind == "list":
        for item in node[1]:
            _validate(item, scope)
        return
    for child in node[1:]:
        if isinstance(child, tuple):
            _validate(child, scope)


def parse_rule(text: str):
    """Parse one CEL rule string into an AST, or raise CelParseError."""
    return _Parser(text).parse()


class Params:
    """The `params` object a rule sees. `missing` decides what an undeclared
    field is: "null" (a complete request — absent means absent) or
    "unknown" (a prompt that never said — the answer is not knowable)."""

    def __init__(self, values: dict, missing: str = "null"):
        if missing not in ("null", "unknown"):
            raise ValueError(f"missing must be 'null' or 'unknown', not {missing!r}")
        self.values = dict(values)
        self.missing = missing

    def get(self, name):
        if name in self.values:
            return self.values[name]
        return UNKNOWN if self.missing == "unknown" else None

    def has(self, name):
        if name in self.values:
            return self.values[name] is not None
        return UNKNOWN if self.missing == "unknown" else False


def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _cel_type(v) -> CelType:
    if v is None:
        return CelType("null_type")
    if isinstance(v, bool):
        return CelType("bool")
    if isinstance(v, int):
        return CelType("int")
    if isinstance(v, float):
        return CelType("double")
    if isinstance(v, str):
        return CelType("string")
    if isinstance(v, list):
        return CelType("list")
    if isinstance(v, dict):
        return CelType("map")
    if isinstance(v, CelType):
        return CelType("type")
    raise CelEvalError(f"value of unsupported type {type(v).__name__}")


def _cel_eq(a, b) -> bool:
    """CEL heterogeneous equality: numbers compare numerically, bools only
    with bools, mismatched types are simply unequal (never an error)."""
    if _is_num(a) and _is_num(b):
        return a == b
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_cel_eq(x, y) for x, y in zip(a, b))
    if type(a) is not type(b):
        return False
    return a == b


def _logic(op: str, left, right):
    """Kleene && / || with CEL error absorption: a decisive side (false for
    &&, true for ||) wins over an error or an unknown on the other side."""
    vals = []
    for side in (left, right):
        try:
            vals.append(side())
        except CelEvalError as e:
            vals.append(e)
    decisive = op == "or"
    if any(v is decisive for v in vals):
        return decisive
    for v in vals:
        if isinstance(v, CelEvalError):
            raise v
        if v is not UNKNOWN and not isinstance(v, bool):
            raise CelEvalError(f"'{'||' if op == 'or' else '&&'}' on non-bool {v!r}")
    if any(v is UNKNOWN for v in vals):
        return UNKNOWN
    return not decisive


_FLAG_GROUP_RE = re.compile(r"\(\?([a-zA-Z]*)(?:-([a-zA-Z]*))?([:)])")


def _re2_anchors(pat: str) -> str:
    """CEL `.matches()` is RE2: outside multi-line mode `$` matches only at
    the very end of the text. Python's `$` also matches before a trailing
    newline ("#A0B0C0\\n" would pass `^#[0-9A-F]{6}$`), so an unescaped `$`
    outside a character class becomes `\\Z` — but ONLY where multi-line mode
    is off: under `(?m)` (global) or inside a `(?m:…)` group both engines
    agree that `$` is end-of-line, and it is left alone."""
    out, i, in_class = [], 0, False
    multiline = [False]          # scope stack: one entry per open group
    while i < len(pat):
        ch = pat[i]
        if ch == "\\":
            out.append(pat[i:i + 2])
            i += 2
            continue
        if in_class:
            if ch == "]":
                in_class = False
            out.append(ch)
            i += 1
            continue
        if ch == "[":
            in_class = True
            j = i + 1 + (pat[i + 1:i + 2] == "^")
            if pat[j:j + 1] == "]":          # a literal ] first in the class
                j += 1
            out.append(pat[i:j])
            i = j
            continue
        if ch == "(":
            m = _FLAG_GROUP_RE.match(pat, i)
            state = multiline[-1]
            if m:
                on, off, end = m.group(1), m.group(2) or "", m.group(3)
                if "m" in on:
                    state = True
                if "m" in off:
                    state = False
                if end == ")":               # (?m) — sets the flag for the rest of the scope
                    multiline[-1] = state
                    out.append(m.group(0))
                    i = m.end()
                    continue
                multiline.append(state)      # (?m:…) — scoped
                out.append(m.group(0))
                i = m.end()
                continue
            multiline.append(state)
        elif ch == ")":
            if len(multiline) > 1:
                multiline.pop()
        elif ch == "$" and not multiline[-1]:
            out.append(r"\Z")
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _eval(node, env: dict):
    kind = node[0]
    if kind == "lit":
        return node[1]
    if kind == "ident":
        name = node[1]
        if name in env:
            return env[name]
        if name in TYPE_NAMES:
            return CelType(name)
        raise CelEvalError(f"unbound identifier {name!r}")
    if kind == "select":
        obj = _eval(node[1], env)
        if obj is UNKNOWN:
            return UNKNOWN
        if isinstance(obj, Params):
            return obj.get(node[2])
        if isinstance(obj, dict):
            if node[2] in obj:
                return obj[node[2]]
            raise CelEvalError(f"no such key {node[2]!r}")
        raise CelEvalError(f"cannot select .{node[2]} on {_cel_type(obj).name}")
    if kind == "has":
        obj = _eval(node[1], env)
        if obj is UNKNOWN:
            return UNKNOWN
        if isinstance(obj, Params):
            return obj.has(node[2])
        if isinstance(obj, dict):
            return node[2] in obj
        raise CelEvalError("has() needs a map or message")
    if kind == "size":
        v = _eval(node[1], env)
        if v is UNKNOWN:
            return UNKNOWN
        if v is None:
            # An absent repeated field (image_references not sent) is empty:
            # the platform's own t2v rule `size(...) == 0` depends on it.
            return 0
        if isinstance(v, (str, list, dict)):
            return len(v)
        raise CelEvalError(f"size() of {_cel_type(v).name}")
    if kind == "type":
        v = _eval(node[1], env)
        return UNKNOWN if v is UNKNOWN else _cel_type(v)
    if kind == "not":
        v = _eval(node[1], env)
        if v is UNKNOWN:
            return UNKNOWN
        if not isinstance(v, bool):
            raise CelEvalError(f"'!' on non-bool {v!r}")
        return not v
    if kind == "neg":
        v = _eval(node[1], env)
        if v is UNKNOWN:
            return UNKNOWN
        if not _is_num(v):
            raise CelEvalError(f"unary '-' on {_cel_type(v).name}")
        return -v
    if kind == "arith":
        op = node[1]
        a, b = _eval(node[2], env), _eval(node[3], env)
        if a is UNKNOWN or b is UNKNOWN:
            return UNKNOWN
        if _is_num(a) and _is_num(b):
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if b == 0:
                raise CelEvalError("division by zero")
            if isinstance(a, int) and isinstance(b, int):
                # CEL int `/` truncates toward zero and `%` keeps the sign of
                # the dividend (-7 / 2 == -3, -7 % 2 == -1); Python's // and %
                # floor instead (-4 and 1).
                q = abs(a) // abs(b)
                q = q if (a >= 0) == (b >= 0) else -q
                return q if op == "/" else a - b * q
            if op == "%":
                raise CelEvalError("'%' on double (CEL defines it for int / uint only)")
            return a / b
        if op == "+" and type(a) is type(b) and isinstance(a, (str, list)):
            return a + b
        raise CelEvalError(f"'{op}' on {_cel_type(a).name} and {_cel_type(b).name}")
    if kind == "cmp":
        op = node[1]
        a, b = _eval(node[2], env), _eval(node[3], env)
        if a is UNKNOWN or b is UNKNOWN:
            return UNKNOWN
        if op == "==":
            return _cel_eq(a, b)
        if op == "!=":
            return not _cel_eq(a, b)
        if not ((_is_num(a) and _is_num(b))
                or (isinstance(a, str) and isinstance(b, str))):
            raise CelEvalError(f"'{op}' on {_cel_type(a).name} and {_cel_type(b).name}")
        return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
    if kind == "in":
        a, coll = _eval(node[1], env), _eval(node[2], env)
        if a is UNKNOWN or coll is UNKNOWN:
            return UNKNOWN
        if isinstance(coll, list):
            if any(x is UNKNOWN for x in coll):
                return True if any(_cel_eq(a, x) for x in coll if x is not UNKNOWN) \
                    else UNKNOWN
            return any(_cel_eq(a, x) for x in coll)
        if isinstance(coll, dict):
            return any(_cel_eq(a, k) for k in coll)
        raise CelEvalError(f"'in' on {_cel_type(coll).name}")
    if kind == "index":
        coll, idx = _eval(node[1], env), _eval(node[2], env)
        if coll is UNKNOWN or idx is UNKNOWN:
            return UNKNOWN
        if isinstance(coll, dict):
            for k, v in coll.items():
                if _cel_eq(k, idx):
                    return v
            raise CelEvalError(f"no such key {idx!r}")
        if isinstance(coll, list) and isinstance(idx, int) and not isinstance(idx, bool):
            if 0 <= idx < len(coll):
                return coll[idx]
            raise CelEvalError(f"index {idx} out of range")
        raise CelEvalError(f"cannot index {_cel_type(coll).name}")
    if kind in ("and", "or"):
        return _logic(kind, lambda: _eval(node[1], env), lambda: _eval(node[2], env))
    if kind == "cond":
        c = _eval(node[1], env)
        if c is UNKNOWN:
            try:
                a, b = _eval(node[2], env), _eval(node[3], env)
            except CelEvalError:
                return UNKNOWN
            return a if (a is not UNKNOWN and b is not UNKNOWN and _cel_eq(a, b)) \
                else UNKNOWN
        if not isinstance(c, bool):
            raise CelEvalError(f"'?:' condition is {_cel_type(c).name}, not bool")
        return _eval(node[2] if c else node[3], env)
    if kind == "list":
        return [_eval(item, env) for item in node[1]]
    if kind == "map":
        out = {}
        for k, v in node[1]:
            key = _eval(k, env)
            if key is UNKNOWN or isinstance(key, (list, dict)):
                raise CelEvalError("unsupported map key")
            out[key] = _eval(v, env)
        return out
    if kind == "matches":
        s, pat = _eval(node[1], env), _eval(node[2], env)
        if s is UNKNOWN or pat is UNKNOWN:
            return UNKNOWN
        if not (isinstance(s, str) and isinstance(pat, str)):
            raise CelEvalError(".matches() needs strings")
        try:
            return re.search(_re2_anchors(pat), s) is not None
        except re.error as e:
            raise CelEvalError(f"bad regex {pat!r}: {e}") from e
    if kind == "macro":
        name, target, var, pred = node[1], node[2], node[3], node[4]
        coll = _eval(target, env)
        if coll is UNKNOWN:
            return UNKNOWN
        if coll is None:
            coll = []
        if isinstance(coll, dict):
            coll = list(coll)
        if not isinstance(coll, list):
            raise CelEvalError(f".{name}() on {_cel_type(coll).name}")
        result = name == "all"
        for elem in coll:
            inner = dict(env)
            inner[var] = elem
            op = "and" if name == "all" else "or"
            result = _logic(op, lambda r=result: r,
                            lambda e=inner: _eval(pred, e))
        return result
    raise CelEvalError(f"unhandled node {kind}")  # pragma: no cover


def referenced_params(node) -> set[str]:
    """Every `params.<field>` a rule reads (for 'depends on X' reporting)."""
    found: set[str] = set()

    def walk(n):
        if not isinstance(n, tuple):
            return
        if n[0] in ("select", "has") and n[1] == ("ident", "params"):
            found.add(n[2])
        for child in n[1:]:
            if isinstance(child, tuple):
                walk(child)
            elif isinstance(child, list):
                for c in child:
                    if isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], tuple):
                        walk(c[0])
                        walk(c[1])
                    else:
                        walk(c)
    walk(node)
    return found


# ════════════════════════════════════════════════════════════════════════════
# Rules from the CLI baseline
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class Rule:
    cel: str
    message: str = ""


@dataclass
class RuleResult:
    status: str          # PASS | FAIL | UNKNOWN | UNCHECKED
    rule: Rule
    detail: str = ""
    depends_on: list[str] = field(default_factory=list)


def _rule_from(raw) -> Rule | None:
    if isinstance(raw, str):
        return Rule(raw)
    if isinstance(raw, dict) and isinstance(raw.get("cel"), str):
        return Rule(raw["cel"], raw.get("message") or "")
    return None


def load_baseline(path: Path = BASELINE_DEFAULT) -> dict:
    """{"captured": date|None, "rules": {model_id: [Rule]}, "params":
    {model_id: {name: {...}}}, "sections": {model_id: section}}.

    Every top-level section that is a {model_id: entry} map is read — not a
    fixed video/image/audio list — so a regenerated baseline that grows a new
    catalog (3D) is covered without an edit here. Rule entries may be plain
    CEL strings (the refresh_specs.py shape) or {"cel", "message"} dicts (the
    raw `model get --json` shape).

    A model is "on record" only when its entry CARRIES a `rules` list — an
    empty list is a model the CLI gives no rules, a missing key is a channel
    nobody recorded (a renamed key once read as "0/0 rules parse", green).
    Entries without the key are listed under "no_rules"; a `rules` value that
    is not a list is malformed. `captured_by_type` (per-section capture
    dates, v3.37.0) is read when present; `captured` stays the summary."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    by_type = data.get("captured_by_type")
    out = {"captured": data.get("captured"),
           "captured_by_type": dict(by_type) if isinstance(by_type, dict) else {},
           "rules": {}, "params": {}, "sections": {}, "malformed": [],
           "no_rules": []}
    for section, models in data.items():
        if not isinstance(models, dict) or section == "captured_by_type":
            continue
        for mid, entry in models.items():
            if not isinstance(entry, dict):
                continue
            out["params"][mid] = entry.get("params") or {}
            out["sections"][mid] = section
            if "rules" not in entry:
                out["no_rules"].append(mid)
                continue
            raw_rules = entry["rules"]
            if not isinstance(raw_rules, list):
                out["malformed"].append((mid, raw_rules))
                continue
            rules = []
            for raw in raw_rules:
                rule = _rule_from(raw)
                if rule is None:
                    out["malformed"].append((mid, raw))
                else:
                    rules.append(rule)
            out["rules"][mid] = rules
    return out


def check_rule_coverage(baseline: dict) -> list[tuple[str, str, str]]:
    """Every rule in the baseline must parse, and every model entry must
    carry its rules channel. Returns [(model, cel, error)] for the ones that
    do not — the fail-closed coverage gate."""
    bad = [(mid, repr(raw), "malformed rule entry (neither a string nor "
            "{'cel': ...})") for mid, raw in baseline.get("malformed", [])]
    bad += [(mid, "<no `rules` key>", "the baseline entry records no rules "
             "channel — this model's platform rules are not on record")
            for mid in sorted(baseline.get("no_rules", []))]
    for mid, rules in sorted(baseline["rules"].items()):
        for rule in rules:
            try:
                parse_rule(rule.cel)
            except CelParseError as e:
                bad.append((mid, rule.cel, str(e)))
    return bad


def evaluate_rules(rules: list[Rule], params: dict, missing: str = "null") -> list[RuleResult]:
    """Evaluate each rule against `params` (a flat dict of param + media-role
    values). Never raises: parse/eval problems become UNCHECKED results."""
    results = []
    p = Params(params, missing=missing)
    for rule in rules:
        try:
            ast = parse_rule(rule.cel)
        except CelParseError as e:
            results.append(RuleResult("UNCHECKED", rule, f"unparseable: {e}"))
            continue
        try:
            value = _eval(ast, {"params": p})
        except CelEvalError as e:
            results.append(RuleResult("UNCHECKED", rule, f"unevaluable: {e}"))
            continue
        if value is True:
            results.append(RuleResult("PASS", rule))
        elif value is False:
            results.append(RuleResult("FAIL", rule))
        elif value is UNKNOWN:
            deps = sorted(n for n in referenced_params(ast) if n not in params)
            results.append(RuleResult("UNKNOWN", rule, "depends on undeclared "
                                      + ", ".join(deps), deps))
        else:
            results.append(RuleResult("UNCHECKED", rule,
                                      f"rule evaluated to non-bool {value!r}"))
    return results


# ════════════════════════════════════════════════════════════════════════════
# Specs surface (enums, ranges, media roles) + model resolution
# ════════════════════════════════════════════════════════════════════════════

class AmbiguousModelError(LookupError):
    """A display name that maps to more than one model id."""

    def __init__(self, arg: str, candidates: list[str]):
        self.arg = arg
        self.candidates = sorted(candidates)
        super().__init__(
            f"model {arg!r} is ambiguous — it is the display name of "
            f"{', '.join(self.candidates)}; pass the model id instead")


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def index_models(models: list[dict]) -> dict:
    """Index models by id, alias, and normalized display name. A display
    name shared by several ids is NOT indexed; it is recorded under
    "_ambiguous" so resolve_model() can refuse it with the candidate list
    (two catalog entries are both named "Cinema Studio Video" — silently
    picking one let a v1-illegal duration pass against v2's range)."""
    index: dict = {}
    by_name: dict[str, set[str]] = {}
    first: dict[str, dict] = {}
    for m in models:
        index[m["id"]] = m
        for alias in m.get("aliases", []):
            index[alias] = m
        key = norm_name(m.get("name", m["id"]))
        by_name.setdefault(key, set()).add(m["id"])
        first.setdefault(key, m)
    ambiguous = {}
    for key, ids in by_name.items():
        if len(ids) > 1:
            ambiguous[key] = sorted(ids)
        elif key not in index:
            index[key] = first[key]
    index["_ambiguous"] = ambiguous
    return index


def resolve_model(index: dict, arg: str) -> dict | None:
    """Exact id / alias first, then the normalized display name. Raises
    AmbiguousModelError when the name belongs to more than one model."""
    hit = index.get(arg)
    if isinstance(hit, dict) and "id" in hit:
        return hit
    key = norm_name(arg)
    if key in index.get("_ambiguous", {}):
        raise AmbiguousModelError(arg, index["_ambiguous"][key])
    hit = index.get(key)
    return hit if isinstance(hit, dict) and "id" in hit else None


def load_catalog(specs_dir: Path = SPECS_DIR) -> dict:
    """All generated spec files merged: {"models": [...], "snapshots":
    {type: date}}. Missing files are skipped (listed under "missing")."""
    models, snapshots, missing = [], {}, []
    for otype, name in SPEC_FILES.items():
        path = Path(specs_dir) / name
        try:
            spec = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            missing.append(name)
            continue
        snapshots[otype] = spec.get("snapshot_date")
        models.extend(spec.get("models", []))
    return {"models": models, "snapshots": snapshots, "missing": missing}


_RANGE_IN_DESC = re.compile(r"\(\s*(-?\d+)\s*[-–]\s*(-?\d+)\s*\)"
                            r"|between\s+(-?\d+)\s+and\s+(-?\d+)", re.I)


@dataclass
class DurationPolicy:
    values: list | None = None     # discrete legal lengths
    min: float | None = None       # legal length range (sentinel excluded)
    max: float | None = None
    sentinel: int | None = None    # smart duration: model picks the length
    floor_known: bool = True

    def describe(self) -> str:
        if self.values is not None:
            return "/".join(str(v) for v in self.values) + "s"
        rng = f"{self.min}–{self.max}s" if self.floor_known else f"up to {self.max}s"
        if self.sentinel is not None:
            return f"{rng}, or {self.sentinel} (smart duration — the model picks the length)"
        return rng

    def check(self, value) -> tuple[str, str]:
        """(status, note): status PASS | FAIL | UNCHECKED."""
        if not _is_num(value):
            return "FAIL", f"duration {value!r} is not a number"
        if self.sentinel is not None and value == self.sentinel:
            return "PASS", "smart-duration sentinel"
        if self.values is not None:
            return ("PASS", "") if value in self.values else ("FAIL", "")
        if self.max is not None and value > self.max:
            return "FAIL", ""
        if not self.floor_known:
            if value <= 0:
                return "FAIL", "a length must be positive"
            return "UNCHECKED", ("the minimum length could not be derived from "
                                 "the spec — verify live")
        if self.min is not None and value < self.min:
            return "FAIL", ""
        return "PASS", ""


def duration_policy(spec: dict) -> DurationPolicy | None:
    """The legal duration surface of one spec model.

    sync_specs normalizes wan3_0's `duration` to {min: -1, max: 30} — the -1
    is NOT a length but the smart-duration sentinel ("-1 to let the model
    choose … billed as 10 seconds"); the real length range (2–30) lives only
    in the parameter description. A negative min is therefore read as the
    sentinel and the true floor re-derived from the description; if it can't
    be, lengths are reported UNCHECKED rather than passed. A spec that carries
    an explicit {"smart": -1} key (the proposed sync_specs shape) is honored."""
    d = spec.get("duration")
    if not d:
        return None
    if "values" in d:
        return DurationPolicy(values=list(d["values"]))
    lo, hi = d.get("min"), d.get("max")
    if "smart" in d:
        return DurationPolicy(min=lo, max=hi, sentinel=d["smart"])
    if lo is not None and lo < 0:
        desc = next((p.get("description", "") for p in spec.get("params", [])
                     if p.get("name") == "duration"), "")
        for m in _RANGE_IN_DESC.finditer(desc or ""):
            a, b = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            a, b = int(a), int(b)
            if 0 < a <= b:
                return DurationPolicy(min=a, max=hi if hi is not None else b,
                                      sentinel=lo)
        return DurationPolicy(min=None, max=hi, sentinel=lo, floor_known=False)
    return DurationPolicy(min=lo, max=hi)


def media_roles(spec: dict) -> set[str]:
    return {r for roles in (spec.get("media_roles") or {}).values() for r in roles}


def cli_role(role: str) -> str:
    """The CLI name of a media role (MCP `image` → `image_references`)."""
    return MCP_TO_CLI_ROLE.get(role, role)


def normalize_media(media: dict) -> dict:
    """Media counts keyed by CLI role name; two spellings of one slot add up."""
    out: dict[str, int] = {}
    for role, count in (media or {}).items():
        key = cli_role(role)
        out[key] = out.get(key, 0) + int(count or 0)
    return out


def accepted_roles(spec: dict | None, cli_params: dict | None = None) -> set[str]:
    """CLI names of every media role the model takes: its specs roles (MCP
    names mapped) plus the CLI baseline's media-role params (gpt_image_2's
    inpaint `mask` exists only there)."""
    roles = {cli_role(r) for r in media_roles(spec or {})}
    roles |= {n for n in (cli_params or {}) if is_cli_media_param(n)}
    return roles


def _is_int(v) -> bool:
    return (isinstance(v, int) and not isinstance(v, bool)) or \
        (isinstance(v, float) and v.is_integer())


# JSON-schema type words the CLI's `model get` uses ("integer", "string|null").
_TYPE_OK = {
    "integer": _is_int,
    "number": lambda v: _is_num(v),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def type_matches(value, cli_type) -> bool | None:
    """True / False against the CLI's declared type; None when the type word
    is not one this check knows (never guessed into a pass or a fail)."""
    alts = [t.strip() for t in str(cli_type or "").split("|") if t.strip()]
    if not alts or any(t not in _TYPE_OK for t in alts):
        return None
    return any(_TYPE_OK[t](value) for t in alts)


def is_list_role(role: str) -> bool:
    """image_references / video_references / audio_references / urls are
    repeated; start_image / end_image are single objects."""
    return role.endswith("_references") or role.endswith("s")


@dataclass
class Check:
    status: str   # PASS | FAIL | WARN | UNCHECKED | INFO
    what: str
    detail: str = ""


def _option_match(value, options: list):
    """Case-insensitive option match; returns the canonical option or None."""
    for opt in options:
        if _cel_eq(value, opt) or str(value).lower() == str(opt).lower():
            return opt
    return None


def coerce_value(raw: str, spec_param: dict | None):
    """CLI `k=v` strings → typed values, driven by the spec's param type."""
    if raw.lower() in ("null", "none"):
        return None
    ptype = (spec_param or {}).get("type", "")
    if ptype in ("bool", "boolean"):
        if raw.lower() in ("true", "1", "yes"):
            return True
        if raw.lower() in ("false", "0", "no"):
            return False
        return raw
    if ptype in ("number", "integer", "int", "double", "float") or \
            (not ptype and re.fullmatch(r"-?\d+(\.\d+)?", raw)):
        try:
            num = float(raw)
        except ValueError:
            return raw
        # ponytail: models_explore types every numeric param "number", so an
        # integral input stays int (`params.duration == -1` and the enum
        # lists compare cleanly either way). A rule testing
        # `type(x) == double` on an integral input would read int — the only
        # such rules today are on 3D models the specs don't cover; switch to
        # CLI-schema typing (integer vs number) if one lands on a spec'd model.
        return int(num) if num.is_integer() else num
    if raw.lower() in ("true", "false") and not ptype:
        return raw.lower() == "true"
    return raw


def spec_surface_checks(spec: dict | None, params: dict, media: dict,
                        cli_params: dict | None = None) -> list[Check]:
    """Enum / range / type / role legality of one request.

    `spec` is the model's specs/ entry (None when it has none — the caller
    reports that surface UNCHECKED); `cli_params` is its CLI baseline param
    map, which adds the CLI's declared type per param (wan3_0 `duration` is
    an integer: 2.5 is illegal though it sits inside 2–30) and, without a
    spec entry, the CLI's enum lists. Every declared param yields a line."""
    checks: list[Check] = []
    spec = spec or {}
    cli_params = cli_params or {}
    mid = spec.get("id") or "this model"
    by_name = {p.get("name"): p for p in spec.get("params", [])}
    for name, value in params.items():
        if name == "prompt":
            continue
        what = f"{name}={value}"
        cp = cli_params.get(name) if isinstance(cli_params.get(name), dict) else None
        typed_ok = type_matches(value, cp.get("type")) if cp else None
        if typed_ok is False:
            checks.append(Check("FAIL", what, f"the CLI types {name} as {cp['type']}"))
            continue
        p = by_name.get(name)
        # Two sources, each consulted on its own: specs/ (models_explore) and
        # the CLI baseline. A spec entry no longer hides the CLI's param set
        # or enums (gpt_image_2 background=bogus passed; a misspelled
        # `resolutoin` on seedance_2_0 passed).
        spec_opts = spec.get("aspect_ratios") if name == "aspect_ratio" else (p or {}).get("options")
        known_spec = p is not None or (name == "aspect_ratio" and bool(spec.get("aspect_ratios")))
        spec_status, spec_detail = None, ""
        if name == "duration" and spec and duration_policy(spec) is not None:
            pol = duration_policy(spec)
            spec_status, note = pol.check(value)
            spec_detail = f"{mid} supports {pol.describe()}" + (f" — {note}" if note else "")
        elif spec_opts:
            ok = _option_match(value, spec_opts) is not None
            spec_status = "PASS" if ok else "FAIL"
            spec_detail = f"specs: {mid} supports {name}: " + ", ".join(map(str, spec_opts))
        elif p is not None and (p.get("min") is not None or p.get("max") is not None):
            ok = _is_num(value) and not (
                (p.get("min") is not None and value < p["min"]) or
                (p.get("max") is not None and value > p["max"]))
            spec_status = "PASS" if ok else "FAIL"
            spec_detail = (f"specs: {mid} range {p.get('min')}–{p.get('max')}" if _is_num(value)
                           else "not a number")
        cli_opts = (cp or {}).get("options") or (cp or {}).get("enum") or []
        cli_status, cli_detail = None, ""
        if cli_opts:
            cli_status = "PASS" if _option_match(value, cli_opts) is not None else "FAIL"
            cli_detail = f"CLI baseline enumerates {name}: " + ", ".join(map(str, cli_opts))

        if not known_spec and cp is None:
            if cli_params:
                checks.append(Check("FAIL", what, f"no '{name}' parameter in specs/ nor in "
                                    f"the CLI baseline — unknown to both sources"))
            else:
                checks.append(Check("WARN", what, f"no '{name}' parameter in specs/, and no "
                                    "CLI baseline entry to consult — the platform may "
                                    "reject or ignore it"))
            continue
        if spec_status and cli_status and spec_status != cli_status \
                and spec_status != "UNCHECKED":
            legal, illegal = ("specs/", "the CLI baseline") if spec_status == "PASS" \
                else ("the CLI baseline", "specs/")
            checks.append(Check("PASS", what, f"legal per {legal}, not per {illegal} — the "
                                f"sources disagree ({spec_detail}; {cli_detail})"))
            continue
        status = cli_status if spec_status in (None, "UNCHECKED") and cli_status \
            else spec_status
        detail = "; ".join(d for d in (spec_detail, cli_detail) if d)
        if spec and not known_spec and cp is not None:
            detail = (detail + "; " if detail else "") + "not in specs/ — known to the CLI baseline only"
        elif known_spec and cp is None and cli_params:
            detail = (detail + "; " if detail else "") + "not in the CLI baseline — known to specs/ only"
        if status:
            checks.append(Check(status, what, detail))
        else:
            checks.append(Check("PASS", what, f"type {cp['type']}"
                                + (f"; {detail}" if detail else "")) if typed_ok else
                          Check("INFO", what, detail or "no enum, range or type on record — "
                                "the value is not constrained here"))
    accepted = accepted_roles(spec, cli_params)
    for role, count in normalize_media(media).items():
        if not count:
            continue
        what = f"media {role}×{count}"
        if not accepted:
            checks.append(Check("FAIL", what, f"{mid} accepts no media — neither "
                                "specs/ nor the CLI baseline lists a media role for it"))
        elif role not in accepted:
            checks.append(Check("FAIL", what, f"{mid} accepts media roles: "
                                + ", ".join(sorted(accepted))))
        elif not is_list_role(role) and count > 1:
            checks.append(Check("FAIL", what, f"{role} is a single slot — at most 1"))
        else:
            checks.append(Check("PASS", what))
    return checks


def media_param_values(media: dict) -> dict:
    """Media counts → the values a rule sees (`size()` of a list, `== null`
    for a single slot)."""
    out = {}
    for role, count in media.items():
        if is_list_role(role):
            out[role] = [{"role": role, "n": i + 1} for i in range(int(count))]
        else:
            out[role] = {"role": role} if count else None
    return out


@dataclass
class PreflightReport:
    model: str
    checks: list[Check]
    rules: list[RuleResult]
    notes: list[str]
    rules_on_record: bool

    def verdict(self) -> str:
        if any(c.status == "FAIL" for c in self.checks) or \
                any(r.status == "FAIL" for r in self.rules):
            return "FAIL"
        unchecked = any(c.status == "UNCHECKED" for c in self.checks) or \
            any(r.status == "UNCHECKED" for r in self.rules) or \
            not self.rules_on_record
        if unchecked:
            return "UNCHECKED"
        return "PASS"

    def exit_code(self, strict: bool = False) -> int:
        v = self.verdict()
        if v == "FAIL":
            return 1
        if v == "UNCHECKED" and strict:
            return 1
        return 0


def run_preflight(model_arg: str, params: dict, media: dict, *,
                  specs_dir: Path = SPECS_DIR,
                  baseline_path: Path = BASELINE_DEFAULT,
                  catalog: dict | None = None,
                  baseline: dict | None = None,
                  fill_defaults: bool = True) -> PreflightReport:
    """Full preflight of one COMPLETE request (omitted = default / absent)."""
    catalog = catalog if catalog is not None else load_catalog(specs_dir)
    index = index_models(catalog["models"])
    spec = resolve_model(index, model_arg)  # may raise AmbiguousModelError
    notes: list[str] = []
    if baseline is None:
        try:
            baseline = load_baseline(baseline_path)
        except (OSError, json.JSONDecodeError) as e:
            baseline = {"captured": None, "rules": {}, "params": {}}
            notes.append(f"CLI baseline unreadable ({e}) — no platform rules checked")
    model_id = spec["id"] if spec else model_arg
    sections = baseline.get("sections", {})
    if spec is None and model_id not in sections and model_id not in baseline["rules"]:
        raise LookupError(f"unknown model {model_arg!r} — not in specs/ or the CLI baseline")
    cli_params = baseline.get("params", {}).get(model_id) or {}
    media = normalize_media(media)
    if catalog.get("missing"):
        notes.append("specs files missing or unreadable: "
                     + ", ".join(catalog["missing"]))

    # Canonicalize values against the spec options (case) before rules see them.
    typed = dict(params)
    checks = spec_surface_checks(spec, typed, media, cli_params)
    if spec is not None:
        by_name = {p.get("name"): p for p in spec.get("params", [])}
        for k, v in list(typed.items()):
            cp_k = cli_params.get(k) if isinstance(cli_params.get(k), dict) else {}
            opts = (by_name.get(k) or {}).get("options") or \
                (spec.get("aspect_ratios") if k == "aspect_ratio" else None) or \
                cp_k.get("options") or cp_k.get("enum")
            if opts:
                canon = _option_match(v, opts)
                if canon is not None:
                    typed[k] = canon
        if fill_defaults:
            for p in spec.get("params", []):
                if p.get("name") not in typed and "default" in p:
                    typed[p["name"]] = p["default"]
    else:
        # No specs entry: its enum / range / media surface is NOT checked
        # against specs/ — never a pass (a 3d model once passed
        # texture_quality=ultra because specs/ had no 3d file loaded).
        missing = catalog.get("missing") or []
        checks.insert(0, Check(
            "UNCHECKED", "spec surface",
            f"{model_id} has no entry in the specs catalog"
            + (f" (unreadable: {', '.join(missing)})" if missing else "")
            + " — its enum/range/duration/media surface was not checked against "
              "specs/; only the CLI baseline's enums and types were"))
    if fill_defaults:
        for name, meta in cli_params.items():
            if name not in typed and isinstance(meta, dict) and \
                    meta.get("default") is not None and name not in media:
                typed[name] = meta["default"]

    values = dict(typed)
    values.update(media_param_values(media))
    rules = baseline["rules"].get(model_id)
    rules_on_record = rules is not None
    section = sections.get(model_id)
    captured = (baseline.get("captured_by_type") or {}).get(section) \
        or baseline.get("captured")
    if rules is None:
        rules = []
        notes.append(f"no platform rules on record for {model_id} in the CLI "
                     f"baseline (captured {captured}) — its "
                     "cross-parameter rules are UNCHECKED")
    results = evaluate_rules(rules, values, missing="null")

    snaps = catalog.get("snapshots", {})
    otype = (spec or {}).get("output_type") or section
    snap = snaps.get(otype) if otype in snaps else \
        max((d for d in snaps.values() if d), default=None)
    if captured and snap and captured < snap:
        notes.append(f"CLI baseline rules captured {captured} predate the specs "
                     f"snapshot {snap} — rules may be stale; refresh with "
                     "scripts/refresh_specs.py --update-baseline")
    return PreflightReport(model_id, checks, results, notes, rules_on_record)


def render_report(rep: PreflightReport, strict: bool = False) -> str:
    tag = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠", "UNCHECKED": "?",
           "UNKNOWN": "·", "INFO": "·"}
    lines = [f"Platform preflight — {rep.model} — {rep.verdict()}", "=" * 44]
    lines.append("── SPEC SURFACE (specs/*.json)")
    if not rep.checks:
        # Every declared param and non-zero media role yields a line, so an
        # empty list really means nothing was declared.
        lines.append("  (no params or media declared)")
    for c in rep.checks:
        lines.append(f"  {tag[c.status]} [{c.status}] {c.what}"
                     + (f" — {c.detail}" if c.detail else ""))
    lines.append("── PLATFORM RULES (specs/cli_baseline.json)")
    if not rep.rules:
        lines.append("  (the CLI records no rules for this model)" if rep.rules_on_record
                     else "  (none on record)")
    for r in rep.rules:
        label = r.rule.message or r.rule.cel
        lines.append(f"  {tag[r.status]} [{r.status}] {label}")
        if r.rule.message:
            lines.append(f"      rule: {r.rule.cel}")
        if r.detail:
            lines.append(f"      {r.detail}")
    for n in rep.notes:
        lines.append(f"  note: {n}")
    if rep.verdict() == "UNCHECKED":
        lines.append("  Some constraints could not be verified"
                     + (" — --strict: failing." if strict else
                        " — verify live (`higgsfield model get <id> --json`)."))
    return "\n".join(lines)


def _parse_kv(items: list[str], what: str) -> list[tuple[str, str]]:
    out = []
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"--{what} expects key=value, got {item!r}")
        k, v = item.split("=", 1)
        out.append((k.strip(), v.strip()))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Free platform-constraint preflight for any Higgsfield model.")
    ap.add_argument("--model", help="model id (or unambiguous display name)")
    ap.add_argument("--param", action="append", default=[], metavar="K=V",
                    help="request parameter, e.g. mode=t2v (repeatable)")
    ap.add_argument("--media", action="append", default=[], metavar="ROLE=N",
                    help="media role count, e.g. image_references=3 (repeatable)")
    ap.add_argument("--json", dest="json_text",
                    help='request as JSON: {"model", "params", "media"}')
    ap.add_argument("--input", type=Path, help="request JSON file")
    ap.add_argument("--specs-dir", type=Path, default=SPECS_DIR)
    ap.add_argument("--baseline", type=Path, default=BASELINE_DEFAULT)
    ap.add_argument("--strict", action="store_true",
                    help="UNCHECKED rules / models without rules exit non-zero")
    ap.add_argument("--check-rules", action="store_true",
                    help="parse every baseline rule; report unparseable ones")
    ap.add_argument("--report-json", action="store_true",
                    help="machine-readable output")
    args = ap.parse_args(argv)

    if args.check_rules:
        try:
            baseline = load_baseline(args.baseline)
        except (OSError, json.JSONDecodeError) as e:
            print(f"ERROR: cannot read baseline {args.baseline}: {e}", file=sys.stderr)
            return 2
        bad = check_rule_coverage(baseline)
        total = sum(len(r) for r in baseline["rules"].values())
        n_models = len(baseline.get("sections", {}))
        # A coverage gate over nothing is not a pass: zero models or zero
        # rules parsed means the subject was never seen (a renamed `rules`
        # key once printed "0/0 baseline rules parse" and exited 0).
        vacuous = []
        if n_models == 0:
            vacuous.append("the baseline carries no models")
        elif total == 0:
            vacuous.append(f"zero rules on record across {n_models} model(s)")
        if args.report_json:
            print(json.dumps({"total": total, "models": n_models, "vacuous": vacuous,
                              "unchecked": [{"model": m, "rule": c, "error": e}
                                            for m, c, e in bad]}, indent=2))
        else:
            print(f"{total - len([b for b in bad if not b[1].startswith('<')])}/{total} "
                  f"baseline rules parse across {n_models} model(s) "
                  f"(baseline captured {baseline.get('captured')})")
            for mid, cel, err in bad:
                print(f"  ? UNCHECKED {mid}: {cel}\n      {err}")
            for v in vacuous:
                print(f"  ? UNCHECKED — nothing was checked: {v}")
        return 1 if ((bad or vacuous) and args.strict) else 0

    try:
        if args.json_text or args.input:
            req = json.loads(args.json_text if args.json_text
                             else args.input.read_text(encoding="utf-8"))
            if not isinstance(req, dict):
                raise ValueError(f"the request must be a JSON object "
                                 f'{{"model", "params", "media"}}, not {type(req).__name__}')
            model = req.get("model") or args.model
            if model is not None and not isinstance(model, str):
                raise ValueError(f'"model" must be a string, not {type(model).__name__}')
            params, media_raw = req.get("params") or {}, req.get("media") or {}
            for key, val in (("params", params), ("media", media_raw)):
                if not isinstance(val, dict):
                    raise ValueError(f'"{key}" must be a JSON object, not {type(val).__name__}')
            params = dict(params)
            media = {}
            for k, v in media_raw.items():
                if isinstance(v, list):
                    media[k] = len(v)
                elif v is None or (isinstance(v, int) and not isinstance(v, bool)):
                    media[k] = int(v or 0)
                else:
                    raise ValueError(f'media "{k}" must be a count or a list, not {v!r}')
        else:
            model = args.model
            params, media = {}, {}
            catalog = load_catalog(args.specs_dir)
            spec = None
            if model:
                try:
                    spec = resolve_model(index_models(catalog["models"]), model)
                except AmbiguousModelError:
                    spec = None
            by_name = {p.get("name"): p for p in (spec or {}).get("params", [])}
            for k, v in _parse_kv(args.param, "param"):
                params[k] = coerce_value(v, by_name.get(k))
            for k, v in _parse_kv(args.media, "media"):
                media[k] = int(v)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if not model:
        ap.print_help()
        return 2

    try:
        rep = run_preflight(model, params, media, specs_dir=args.specs_dir,
                            baseline_path=args.baseline)
    except AmbiguousModelError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except LookupError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if args.report_json:
        print(json.dumps({
            "model": rep.model, "verdict": rep.verdict(),
            "checks": [c.__dict__ for c in rep.checks],
            "rules": [{"status": r.status, "cel": r.rule.cel,
                       "message": r.rule.message, "detail": r.detail}
                      for r in rep.rules],
            "notes": rep.notes}, indent=2))
    else:
        print(render_report(rep, strict=args.strict))
    return rep.exit_code(strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
