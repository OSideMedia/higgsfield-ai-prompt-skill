#!/usr/bin/env python3
"""Generate USER-GUIDE.pdf for Higgsfield AI Prompt Skill.

Version metadata is read from the root SKILL.md frontmatter at build time.
Sub-skill list at Section 24 is discovered by filesystem walk of skills/.
Per-sub-skill description text remains hardcoded in SUB_SKILL_DESCRIPTIONS
below to preserve the PDF's editorial voice (entries refreshed at v3.7.12
to add higgsfield-stack and update higgsfield-soul + higgsfield-seedance).

Exit codes (v3.7.16+):
  0 = success
  1 = unknown / uncaught error (catch-all)
  2 = frontmatter parse error (root SKILL.md)
  3 = sub-skill dict-parity mismatch (SUB_SKILL_DESCRIPTIONS vs filesystem)
  4 = font registration error (missing or malformed TTF)
  5 = rendering error (e.g., FPDFUnicodeEncodingException)
  6 = output write error (disk full, permission denied, path missing)

Exit code 1 is the unenumerated catch-all for failures not anticipated by
codes 2-6. If you see exit 1, the failure surfaced from a path the matrix
didn't enumerate -- file an issue with the stderr message.
"""

import re
from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from fpdf.errors import FPDFException


REPO_ROOT = Path(__file__).resolve().parent
ROOT_SKILL_PATH = REPO_ROOT / "SKILL.md"
SKILLS_DIR = REPO_ROOT / "skills"
FONT_DIR = REPO_ROOT / "assets" / "fonts"


# -- Exit-code matrix (v3.7.16+) --------------------------------------------
EXIT_OK = 0
EXIT_UNKNOWN = 1
EXIT_FRONTMATTER = 2
EXIT_DICT_PARITY = 3
EXIT_FONT = 4
EXIT_RENDER = 5
EXIT_OUTPUT = 6


# -- Named exception classes (v3.7.16+) -------------------------------------
class BuildError(RuntimeError):
    """Base class for build_pdf failures."""


class FrontmatterError(BuildError):
    """Root SKILL.md frontmatter missing or malformed."""


class DictParityError(BuildError):
    """SUB_SKILL_DESCRIPTIONS dict out of sync with skills/ filesystem walk."""


class FontError(BuildError):
    """Font file missing, malformed, or fpdf2 add_font failed."""


class RenderError(BuildError):
    """fpdf2 rendering exception (e.g., FPDFUnicodeEncodingException)."""


class OutputWriteError(BuildError):
    """pdf.output() write failed (disk full, permission, missing path)."""


def read_root_metadata():
    """Parse root SKILL.md frontmatter for version, updated, author."""
    text = ROOT_SKILL_PATH.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        raise FrontmatterError(f"No YAML frontmatter found in {ROOT_SKILL_PATH}")
    fm = m.group(1)

    def field(name, default=None):
        # Match "name: value" at any indent depth, capture value through end-of-line.
        match = re.search(rf"^\s*{re.escape(name)}:\s*(.+?)\s*$", fm, re.MULTILINE)
        if not match:
            if default is None:
                raise FrontmatterError(f"Field '{name}' not found in root SKILL.md frontmatter")
            return default
        return match.group(1).strip()

    return {
        "version": field("version"),
        "updated": field("updated"),
        "author": field("author", "O-Side Media"),
    }


def discover_sub_skills():
    """Filesystem walk of skills/*/SKILL.md. Returns ordered list of sub-skill names.

    Excludes shared/ (utility directory, no SKILL.md). Order is deterministic
    (alphabetical by directory name). Per-sub-skill descriptions are looked up
    in SUB_SKILL_DESCRIPTIONS below, NOT extracted from frontmatter (which
    carries routing-trigger language, not editorial summaries).
    """
    out = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        if d.name == "shared":
            continue
        if not (d / "SKILL.md").exists():
            continue
        out.append(d.name)
    return out


SUB_SKILL_DESCRIPTIONS = {
    "higgsfield-prompt":      "MCSLA formula + Seedance 2.0 best practices",
    "higgsfield-image-shots": "Cinematic image prompting",
    "higgsfield-models":      "Model selection guide + CS 3.0 comparison",
    "higgsfield-camera":      "Camera controls + One-Move Rule + Smart Mode + @Video reference",
    "higgsfield-motion":      "Motion presets + intent-first choreography",
    "higgsfield-style":       "Visual styles + One Style Anchor Rule",
    "higgsfield-soul":        "Soul ID + Character Anchor Block + Two-Tool Refinement Pipeline",
    "higgsfield-stack":       "CLI / MCP / bundled-skills coexistence + two-step preflight",
    "higgsfield-audio":       "Audio prompting + CS 3.0 native audio (SCELA)",
    "higgsfield-apps":        "One-click Apps guide (80+)",
    "higgsfield-recipes":     "Genre templates",
    "higgsfield-troubleshoot":"Fix generations + CS 3.0 diagnostic tree",
    "higgsfield-assist":      "Platform copilot + credit optimization",
    "higgsfield-mixed-media": "Artistic preset overlays",
    "higgsfield-moodboard":   "Moodboard + style consistency",
    "higgsfield-pipeline":    "Multi-step production pipeline",
    "higgsfield-cinema":      "Cinema Studio 2.5 + 3.0 + 3.5 (Soul Cast, Image Mode, Cinematic models)",
    "higgsfield-gpt-image-2": "GPT Image 2.0 prompt director + static-ads workflow satellite",
    "higgsfield-marketing-studio": "Marketing Studio - 9 ad presets + 4-15s video + cross-surface",
    "higgsfield-recall":      "Pre-generation memory check",
    "higgsfield-vibe-motion": "Vibe Motion / motion graphics",
    "higgsfield-seedance":    "Seedance 2.0 + frame coords + spatial layout + named failure modes",
    "higgsfield-workspaces":  "Workspace-first decision layer",
}


class UserGuidePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        # Register DejaVu Sans Condensed under the family alias "Body" + DejaVu
        # Sans Mono under the alias "Mono" so set_font(...) calls below pick up
        # the bundled Unicode fonts. Bundled in assets/fonts/ — see
        # assets/fonts/README.md for rationale.
        try:
            self.add_font("Body", "",  str(FONT_DIR / "DejaVuSansCondensed.ttf"))
            self.add_font("Body", "B", str(FONT_DIR / "DejaVuSansCondensed-Bold.ttf"))
            self.add_font("Body", "I", str(FONT_DIR / "DejaVuSansCondensed-Oblique.ttf"))
            self.add_font("Mono", "", str(FONT_DIR / "DejaVuSansMono.ttf"))
        except Exception as e:
            raise FontError(f"Font registration failed: {e}") from e

    def header(self):
        if self.page_no() > 1:
            self.set_font("Body", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f"Higgsfield AI Prompt Skill - User Guide v{META['version']}", align="L")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Body", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Body", "B", 16)
        self.set_text_color(30, 30, 30)
        self.ln(4)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(70, 130, 180)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def subsection_title(self, title):
        self.set_font("Body", "B", 13)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Body", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text, align="L")
        self.ln(2)

    def bold_text(self, text):
        self.set_font("Body", "B", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text, align="L")
        self.ln(1)

    def bullet(self, text):
        self.set_font("Body", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(8, 5.5, "-")
        self.multi_cell(0, 5.5, text, align="L")
        self.ln(1)

    def code_block(self, text):
        self.set_font("Mono", "", 9)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(50, 50, 50)
        self.ln(1)
        lines = text.split("\n")
        for line in lines:
            self.cell(0, 5, "  " + line, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(3)

    def callout(self, text):
        self.set_fill_color(240, 248, 255)
        self.set_draw_color(70, 130, 180)
        x = self.get_x()
        y = self.get_y()
        self.set_font("Body", "I", 10)
        self.set_text_color(50, 80, 120)
        self.set_line_width(0.3)
        # Draw left border
        self.line(x, y, x, y + 12)
        self.set_x(x + 5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 5, 5.5, text, fill=True, align="L")
        self.ln(3)

    def table_row(self, cols, widths, bold=False, fill=False):
        self.set_font("Body", "B" if bold else "", 9)
        self.set_text_color(40, 40, 40)
        if fill:
            self.set_fill_color(235, 240, 250)
        h = 5.5
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.cell(w, h, col, border=1, fill=fill)
        self.ln(h)

    def new_tag(self):
        self.set_font("Body", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(70, 130, 180)
        self.cell(18, 5, " NEW ", fill=True)
        self.set_text_color(40, 40, 40)
        self.set_font("Body", "", 10)

    def v3_tag(self):
        self.set_font("Body", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(46, 139, 87)
        self.cell(22, 5, " v3.0 ", fill=True)
        self.set_text_color(40, 40, 40)
        self.set_font("Body", "", 10)


# Read version/date/author from root SKILL.md frontmatter (single source of truth).
META = read_root_metadata()


def build_pdf(dry_run: bool = False):
    try:
        pdf = UserGuidePDF()
        pdf.alias_nb_pages()
        # Pin creation date to the metadata 'updated' field for reproducible builds.
        # Without this, FPDF2 embeds current time in /CreationDate, breaking
        # byte-for-byte reproducibility across runs.
        pdf.set_creation_date(datetime.fromisoformat(META["updated"]))

        # --- COVER PAGE ---
        pdf.add_page()
        pdf.ln(50)
        pdf.set_font("Body", "B", 32)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 15, "Higgsfield AI", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 15, "Prompt Skill", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Body", "", 18)
        pdf.set_text_color(80, 80, 80)
        pdf.ln(5)
        pdf.cell(0, 10, "User Guide", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        pdf.set_font("Body", "", 12)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 7,
            "A plain-English guide for getting the most out of this skill.\n"
            "No coding knowledge required.\n\n"
            "Teaches Claude how to write professional-quality prompts for\n"
            "Higgsfield AI -- the cinematic video and image generation platform.",
            align="C")
        pdf.ln(15)
        pdf.set_font("Body", "I", 11)
        pdf.cell(0, 8, f"v{META['version']} | {META['updated']} | Built by {META['author']}", align="C")

        # --- TABLE OF CONTENTS ---
        pdf.add_page()
        pdf.section_title("Table of Contents")
        toc = [
            "1. What Is This?",
            "2. What Can It Do?",
            "3. How to Install",
            "4. Running the Prompt -- CLI / MCP / Bundled Skills / Paste  NEW",
            "5. Quick Start -- Your First Prompt",
            "6. The MCSLA Formula",
            "7. Choosing a Model",
            "8. Generation Types",
            "9. What 'Production Quality' Costs -- Iteration Anchors  NEW",
            "10. Cinema Studio 2.5",
            "11. Cinema Studio 3.0 (Business/Team Plan)",
            "12. Prompting Best Practices (Seedance 2.0)",
            "13. Soul ID -- Character Consistency",
            "14. Character Sheet Creation",
            "15. Identity vs. Motion Separation",
            "16. Genre Recipes",
            "17. Genre Templates",
            "18. Cinematic Image Prompts",
            "19. Negative Constraints Reference",
            "20. Troubleshooting",
            "21. Top Tips",
            "22. Memory System (Advanced)",
            "23. Cinema Studio Advanced Features",
            "24. Repository Contents",
            "25. FAQ",
        ]
        for item in toc:
            if "NEW" in item:
                pdf.set_font("Body", "", 11)
                pdf.cell(150, 7, item.replace("  NEW", ""))
                pdf.new_tag()
                pdf.ln(7)
            else:
                pdf.set_font("Body", "", 11)
                pdf.set_text_color(40, 40, 40)
                pdf.cell(0, 7, item, new_x="LMARGIN", new_y="NEXT")

        # --- 1. WHAT IS THIS? ---
        pdf.add_page()
        pdf.section_title("1. What Is This?")
        pdf.body_text(
            "This is a Claude skill -- a set of instructions that teaches Claude (Anthropic's AI) how to "
            "write professional-quality prompts for Higgsfield AI, a cinematic video and image generation platform.\n\n"
            "Instead of learning Higgsfield's dozens of models, camera controls, motion presets, and "
            "prompt tricks yourself, you just tell Claude what you want in normal language and it "
            "writes an optimized, ready-to-paste prompt for you.")
        pdf.callout("Think of it as hiring a cinematographer who knows every Higgsfield feature by heart.")

        # --- 2. WHAT CAN IT DO? ---
        pdf.section_title("2. What Can It Do?")
        capabilities = [
            "Write production-ready prompts for any Higgsfield video or image model",
            "Recommend the best model for your specific shot",
            "Guide you through Cinema Studio 2.5's professional multi-shot workflow",
            "Guide you through Cinema Studio 3.0's Smart mode, native audio, and @ references (Business/Team plan)",
            "Apply Seedance 2.0 prompting best practices: Intent over Precision, Genre Router, I2V Gate, Anti-Slop check",
            "Use 3D Mode (Gaussian Splatting) to explore scenes from new angles",
            "Generate batch variations with Grid Generation (2x2 and 4x4)",
            "Help you maintain character consistency with Soul ID and Character Sheets",
            "Apply named camera controls and motion presets",
            "Troubleshoot failed or poor-quality generations with a diagnostic tree",
            "Optimize your credit usage",
            "Build multi-shot sequences with per-character emotions",
            "Use Frame Extraction Loop for iterative creative workflows",
            "Insert objects and people not in your original start frame",
            "Automatically prevent common AI artifacts using shared negative constraints",
            "Separate identity from motion to prevent character drift during camera moves",
            "Match your request to genre templates with Cinema Studio 3.0 genre mappings and prompt length targets",
            "Describe audio as a first-class element with SCELA integration (BGM, SFX, dialogue)",
        ]
        for cap in capabilities:
            pdf.bullet(cap)

        # --- 3. HOW TO INSTALL ---
        pdf.add_page()
        pdf.section_title("3. How to Install")
        pdf.subsection_title("Option A -- Claude Cowork (Desktop App)")
        pdf.body_text("Drop the entire repo folder into your Cowork workspace. The skill loads automatically.")
        pdf.subsection_title("Option B -- Claude Code (Terminal)")
        pdf.code_block("git clone https://github.com/OSideMedia/higgsfield-ai-prompt-skill\ncp -r higgsfield-ai-prompt-skill ~/.claude/skills/higgsfield")
        pdf.subsection_title("Option C -- Claude.ai (Web / Projects)")
        pdf.bullet("Create a new Project in Claude.ai")
        pdf.bullet("Upload the main SKILL.md file as your project instruction base")
        pdf.bullet("Upload individual sub-skill files from the skills/ directory as project documents")

        pdf.ln(3)
        pdf.body_text(
            "Once the skill is installed, you'll need to know where to run the prompts it produces. "
            "See Section 4 for the four execution paths.")

        # --- 4. RUNNING THE PROMPT --- NEW SECTION (v3.7.12) ---
        pdf.add_page()
        pdf.section_title("4. Running the Prompt -- CLI / MCP / Bundled Skills / Paste")
        pdf.new_tag()
        pdf.ln(5)
        pdf.body_text(
            "This skill writes prompts. Higgsfield runs them. The two halves are separate by "
            "design -- Claude does prompt construction and production discipline; Higgsfield "
            "handles auth, file upload, job submission, and result delivery. Once Claude has "
            "produced a prompt for you, you have four ways to actually run it.")

        pdf.subsection_title("The four execution surfaces")

        pdf.bold_text("Higgsfield CLI (terminal-native)")
        pdf.body_text(
            "Command-line tool for terminal-native agents -- Claude Code, Codex, Cursor. "
            "Authenticate with `higgsfield auth login` (device flow). If you're working in Claude "
            "Code or Codex, prefer the CLI over the MCP -- it uses long-lived API tokens rather "
            "than the MCP's interactive OAuth, which holds up better in headless and scripted "
            "contexts. Install via Homebrew (`brew install higgsfield-ai/tap/higgsfield`) or the "
            "install script at the `higgsfield-ai/cli` GitHub repo.")

        pdf.bold_text("Higgsfield MCP custom connector")
        pdf.body_text(
            "MCP connector for claude.ai web and the Claude desktop app. Separate product from "
            "the CLI. Connector URL: `https://mcp.higgsfield.ai/mcp`. Install via claude.ai "
            "Settings -> Connectors -> Add custom connector. Single OAuth sign-in, no token "
            "management. Best fit for conversational generation inside the Claude desktop app "
            "or claude.ai web.")

        pdf.bold_text("Higgsfield bundled skills")
        pdf.body_text(
            "Markdown skill bundle for agents that consume Cowork-style skills. Three skills: "
            "`higgsfield-generate`, `higgsfield-soul`, `higgsfield-product-photoshoot`. Install "
            "via `npx skills add higgsfield-ai/skills`. Invoke with `/higgsfield:generate`. All "
            "three drive the CLI under the hood, so they inherit the CLI's auth model and "
            "behavior.")

        pdf.bold_text("Paste into higgsfield.ai (no install required)")
        pdf.body_text(
            "The always-works fallback. Copy the prompt Claude produced, paste into "
            "higgsfield.ai, and generate. No CLI, no MCP, no skill package -- works on any plan, "
            "any device. Slower for iteration than the other three, but the path with zero "
            "install overhead.")

        pdf.callout(
            "All four surfaces share one credit pool and one job queue. Queue priority is your "
            "plan tier (Plus / Ultra / Business / Team), NOT the choice of surface. Pick the "
            "surface that matches your environment, not the queue you imagine.")

        pdf.subsection_title("Pre-Flight: check cost before you generate")
        pdf.body_text(
            "Preflight is two steps -- verify the model's parameter schema first, then estimate "
            "the cost. Why it matters: production-grade work runs at roughly 1% image and 1.5% "
            "video acceptance (see Section 9), so iteration burn is real and preflight catches "
            "the easy mistakes (wrong aspect-ratio value, invalid model param) before credit "
            "burn.")

        pdf.body_text(
            "Claude knows enough about Higgsfield to sound right without actually being right. "
            "Verification surfaces are sitting right there -- the CLI's `model get` command, the "
            "MCP's `models_explore` tool -- and they're cheap. Use them before the cost call, "
            "not after a failed submission.")

        w_pf = [25, 75, 70]
        pdf.table_row(["Step", "MCP", "CLI"], w_pf, bold=True, fill=True)
        pdf.table_row(
            ["1. Schema verify",
             'models_explore(action="get", model_id="<model>")',
             "higgsfield model get <model>"],
            w_pf)
        pdf.table_row(
            ["2. Cost estimate",
             "generate_image / generate_video with get_cost: true",
             "higgsfield generate cost <model> [--param value]..."],
            w_pf)
        pdf.ln(3)

        pdf.body_text(
            "The MCP response to `get_cost: true` includes an `adjustments` block listing any "
            "optional parameters the server defaulted on your behalf (e.g. `mode=std`, "
            "`sound=on`). Surface those alongside the credit number when you preflight -- "
            "they're part of the preflight contract.")

        pdf.callout(
            "Marketing Studio models don't support `get_cost` cost preflight. For those, check "
            "your `balance` before and after the run instead.")

        # --- 5. QUICK START ---
        pdf.section_title("5. Quick Start -- Your First Prompt")
        pdf.body_text("Just tell Claude what you want. Be as casual or specific as you like.")
        pdf.bold_text("Casual request:")
        pdf.code_block('"Write me a Higgsfield prompt for a woman walking through a foggy forest at dawn"')
        pdf.body_text("Claude will respond with a complete, ready-to-paste prompt including the model recommendation, camera movement, style, and all the details.")
        pdf.bold_text("More specific request:")
        pdf.code_block('"I need a Kling 3.0 prompt for a close-up dialogue scene between two characters\nin a coffee shop. Warm lighting, shallow depth of field, handheld camera."')

        # --- 6. MCSLA FORMULA ---
        pdf.add_page()
        pdf.section_title("6. The MCSLA Formula")
        pdf.body_text("Every prompt is built on five layers -- the cinematographer's checklist:")
        w = [15, 25, 130]
        pdf.table_row(["Letter", "Layer", "Example"], w, bold=True, fill=True)
        pdf.table_row(["M", "Model", "Kling 3.0"], w)
        pdf.table_row(["C", "Camera", "FPV Drone weaving through the alley"], w)
        pdf.table_row(["S", "Subject", "A woman in a tactical jacket"], w)
        pdf.table_row(["L", "Look", "Cinematic, cold blue shadows, 16:9"], w)
        pdf.table_row(["A", "Action", "She sprints, slides under a gate"], w)
        pdf.ln(3)
        pdf.callout("You don't need to specify all five layers every time. Claude fills in sensible defaults for anything you leave out.")

        # --- 7. CHOOSING A MODEL ---
        pdf.section_title("7. Choosing a Model")
        pdf.subsection_title("Video Models")
        w = [85, 85]
        pdf.table_row(["What you're making", "Best model"], w, bold=True, fill=True)
        rows = [
            ("Character-driven drama, dialogue", "Kling 3.0"),
            ("Epic scale, big environments", "Sora 2"),
            ("Lip-sync, multilingual dialogue", "Seedance 1.5 Pro"),
            ("Complex choreography, reference-based", "Seedance 2.0"),
            ("Long takes, camera control", "Kling Motion Control"),
            ("Motion transfer from reference video", "Kling 3.0 Motion Control"),
            ("60fps, first+last frame, reference images", "Wan 2.7"),
            ("Budget Veo 3.1 quality at volume", "Veo 3.1 Lite"),
            ("Quick iteration, drafts", "Kling 2.5 Turbo"),
            ("Nature, documentary", "Veo 3 / Veo 3.1"),
            ("Dance, fluid body motion", "Minimax Hailuo 02"),
            ("Cinema Studio 3.0 workflow", "Business/Team plan"),
        ]
        for r in rows:
            pdf.table_row(list(r), w)

        pdf.ln(3)
        pdf.subsection_title("Image Models")
        pdf.table_row(["What you're making", "Best model"], w, bold=True, fill=True)
        irows = [
            ("Portraits, fashion", "Soul 2.0"),
            ("Maximum photorealism", "Nano Banana Pro"),
            ("Fast pro-quality + text", "Nano Banana 2"),
            ("Text/logo rendering", "GPT Image 1.5"),
            ("Reference editing", "Seedream 4.5"),
            ("Cinematic keyframes for I2V", "Soul Cinema Preview"),
        ]
        for r in irows:
            pdf.table_row(list(r), w)

        # --- 8. GENERATION TYPES ---
        pdf.add_page()
        pdf.section_title("8. Generation Types")
        pdf.subsection_title("Text-to-Video (T2V)")
        pdf.body_text("Describe the scene from scratch. No input image needed. Best for establishing shots, environments, abstract concepts.")
        pdf.subsection_title("Image-to-Video (I2V)")
        pdf.body_text("Upload a still image and describe what should move or change. Best for character consistency, product shots, bringing storyboards to life.")
        pdf.callout("Key rule for I2V: Do NOT re-describe what's already in the image. Only describe what should change or animate. (See I2V Gate rule in Section 12.)")

        # --- 9. WHAT 'PRODUCTION QUALITY' COSTS --- NEW SECTION (v3.7.12) ---
        pdf.add_page()
        pdf.section_title("9. What 'Production Quality' Costs -- Iteration Anchors")
        pdf.new_tag()
        pdf.ln(5)
        pdf.body_text(
            "Production-grade AI cinema runs on iteration. This section gives one production team's "
            "actual numbers -- credits spent, generations rejected, dollars deployed -- as planning "
            "anchors for your own work. Most public framing of AI-cinema cost either understates "
            "iteration burn (highlight reels only) or overstates it (worst-case anchoring without "
            "context); the numbers below are the source-of-truth alternative for budget planning. "
            "Source: Higgsfield's 'Road to Cannes' three-episode documentary on the Hell Grind "
            "90-minute Cannes feature.")

        pdf.subsection_title("The headline numbers")
        pdf.bullet("108,859 generations across 14 days")
        pdf.bullet("9,540,047 credits consumed (against a 10M-credit budget set on Day 1)")
        pdf.bullet("~$400,000 generation cost; ~$500,000 total project cost (generation + 15-person team + audio + post)")
        pdf.bullet("Traditional-VFX-equivalent estimate for the same scope: ~$50M -- placing the AI production at roughly 1% of traditional baseline")
        pdf.bullet("15-person team -- fourteen directors/DPs/editors plus one supervising lead")

        pdf.subsection_title("Acceptance-rate anchors (quadruple-confirmed)")
        pdf.body_text(
            "Across the production, the image acceptance rate sits at roughly 1.0% and the video "
            "acceptance rate at roughly 1.5%. Four independently-sourced data points across the "
            "three-episode documentary confirm this range:")
        w_ar = [60, 65, 45]
        pdf.table_row(["Source", "Sample", "Rate"], w_ar, bold=True, fill=True)
        pdf.table_row(["Ep. 1 funnel (prior project)", "107 images used / 10,710 generated", "1.00% image"], w_ar)
        pdf.table_row(["Ep. 1 funnel (prior project)", "253 videos used / 16,181 generated", "1.56% video"], w_ar)
        pdf.table_row(["Ep. 2 audience anchor", "'1 in 64 video, 1 in 100 image'", "~1.5% / ~1.0%"], w_ar)
        pdf.table_row(["Day-4 session actuals", "800 generated / 8 made final", "1.0% (image-dominant)"], w_ar)
        pdf.table_row(["Full project (Ep. 3 wrap)", "108,859 generations / 90 min finished", "comparable funnel"], w_ar)
        pdf.ln(3)
        pdf.callout(
            "Treat 1.0% image and 1.5% video as the conservative planning anchor for "
            "production-grade AI-cinema work. Budget for the iteration burn -- it IS the work, "
            "not the failure.")

        pdf.subsection_title("Per-character iteration anchor")
        pdf.body_text(
            "Single-character anchor work absorbs disproportionate iteration cost up front, because "
            "the character is then reused across every subsequent shot -- investment compounds "
            "forward. For Hell Grind's lead character ('Jack'):")
        pdf.bullet("~600 generations on Higgsfield Soul Cinema (initial pose / costume / expression variations)")
        pdf.bullet("~200 generations on GPT Image 2 (refinement editing of selected anchors)")
        pdf.bullet("~800 total iterations to lock the character anchor sheet BEFORE any narrative shot generation began")
        pdf.ln(2)
        pdf.body_text(
            "Plan character-anchor budgets accordingly. A character appearing in tens of shots can "
            "justify the front-loaded ~800-iteration investment; a character appearing in one or two "
            "shots cannot.")

        pdf.subsection_title("Per-shot iteration anchor")
        pdf.body_text(
            "Single-shot iteration cost varies widely with shot complexity, scene physics, and how "
            "clean the reference assets are. One worked example from the production:")
        pdf.bullet("Prompt 21C, a 10-second establishing shot -- 72 generations before the shot was accepted as final.")
        pdf.ln(2)
        pdf.body_text(
            "Conceptually-simple shots (this one was a single pan plus push-in) can be the most "
            "iteration-heavy in practice. Budget for the surprise. Use 72-generations-per-10-seconds "
            "as an upper-bound planning point for a single iteration-heavy establishing shot, not "
            "as a per-shot average.")

        pdf.subsection_title("Iteration-budget projection")
        pdf.body_text(
            "Worked example for sizing a credit budget against a shot: a single Kling 3.0 8s "
            "generation at 16:9 std mode costs 16 credits. The 1.5% video-acceptance anchor implies "
            "roughly 67 attempts on average to land one keeper. At 16 credits per attempt, that's "
            "about 1,000 credits per finished shot. Multiply by shot count for multi-shot sequences.")
        pdf.body_text(
            "The discipline isn't to surface the multiplied number every time -- it's to read "
            "single-shot cost in the context of iteration cost, not as an absolute. Preflight a shot "
            "by its credit-per-keeper, not by its credit-per-attempt.")

        pdf.subsection_title("AI vs. traditional cost anchors")
        pdf.body_text(
            "Three Hollywood validators in the documentary anchor the AI-vs-traditional cost "
            "comparison for Hell Grind-equivalent scope:")
        w_val = [38, 55, 55, 22]
        pdf.table_row(["Validator", "Credentials", "Anchor", "Source"], w_val, bold=True, fill=True)
        pdf.table_row(["Chuck Russell", "Director (The Mask, Scorpion King)", "~$5M, 25-min live-action equiv", "Ep. 1"], w_val)
        pdf.table_row(["Patrick Kalin", "Emmy VFX (Avatar, Dune)", "~$15-20M, 25-min VFX-heavy equiv", "Ep. 2"], w_val)
        pdf.table_row(["Jamafe", "Concept artist (Mandalorian, Avengers)", "Qualitative -- 'watching a movie'", "Ep. 3"], w_val)
        pdf.ln(3)
        pdf.body_text(
            "Russell and Kalin bracket the traditional-equivalent cost at $5-20M for a 25-min "
            "equivalent, scaling to roughly $50M for the 90-min scope at the VFX-heavy end. The "
            "Higgsfield team's actual ~$500K total cost sits at roughly 1% of the $50M traditional "
            "baseline. The bracket matters more than any single number -- the 1% AI-vs-traditional "
            "ratio is an order-of-magnitude framing, not a precision claim.")

        pdf.subsection_title("Falsifiable success criteria")
        pdf.body_text(
            "The production was held to a five-criterion success rubric stated up front, before any "
            "generation began. Either the finished feature hits the criteria and the AI-cinema "
            "thesis is proved, or it misses and the result is a catalog of remaining gaps:")
        pdf.bullet("Viewer stops perceiving AI generation across the full runtime -- the production reads as cinema, not as 'AI work'")
        pdf.bullet("Narrative coherence -- structured opening, middle, resolution; setups have payoffs")
        pdf.bullet("Characters register as inhabited people -- not as model-produced figures with the characteristic AI tells")
        pdf.bullet("Intended emotional beats produce the intended audience response")
        pdf.bullet("Audience experiences unanticipated emotional impact -- the scenes that surprise beyond the script")
        pdf.ln(2)
        pdf.body_text(
            "When framing your own AI-cinema work, write down the success criteria first. Then ship "
            "and check them. The binary structure (proved / gaps cataloged) prevents the failure "
            "mode of post-hoc rationalization -- claiming success regardless of outcome because no "
            "specific test was committed to up front.")

        pdf.callout(
            "Plan iteration budget against these anchors, not against highlight reels. Iteration "
            "burn is the work, not the failure -- preflight your shots by credit-per-keeper, not "
            "by credit-per-attempt.")

        # --- 10. CINEMA STUDIO 2.5 ---
        pdf.section_title("10. Cinema Studio 2.5")
        pdf.body_text(
            "Cinema Studio is Higgsfield's professional filmmaking environment. It gives you control over "
            "optical physics, multi-shot sequences, character elements, Soul Cast AI actors, and built-in color grading.")
        pdf.subsection_title("The 10-step workflow:")
        w3 = [15, 40, 115]
        pdf.table_row(["Step", "What you do", "Details"], w3, bold=True, fill=True)
        steps = [
            ("1", "Script", "Write your scene description / shot list"),
            ("2", "Soul Cast", "Generate AI actors from parameters (no photos needed)"),
            ("3", "Reference", "Upload character photo or use Soul Cast actor as Reference Anchor"),
            ("4", "Elements", "Define @Characters, @Locations, @Props"),
            ("5", "Optical Stack", "Choose camera body + lens + focal length + aperture"),
            ("6", "Hero Frame", "Generate a key image to lock the visual tone"),
            ("7", "Color Grade", "Apply color grading to keyframes before video generation"),
            ("8", "Camera Config", "Set Director Panel movement + Speed Ramp + Duration"),
            ("9", "Shot Mode", "Single Shot, Multi-Shot Auto, or Multi-Shot Manual"),
            ("10", "Generate", "Run generation and export"),
        ]
        for s in steps:
            pdf.table_row(list(s), w3)
        pdf.ln(3)
        pdf.body_text(
            "Director Panel: 18 camera movements -- Static, Handheld, Zoom Out/In, Camera Follows, Pan Left/Right, "
            "Tilt Up/Down, Orbit Around, Dolly In/Out, Jib Up/Down, Drone Shot, Dolly Left/Right, 360 Roll, Auto.\n\n"
            "Speed Ramp: Linear, Slow Mo, Speed Up, Impact, Auto, Custom (with editable curve).\n\n"
            "Shot structure: Up to 6 scenes, 12s total max, per-scene config.")

        # --- 11. CINEMA STUDIO 3.0 ---
        pdf.add_page()
        pdf.section_title("11. Cinema Studio 3.0 (Business/Team Plan)")
        pdf.v3_tag()
        pdf.ln(5)
        pdf.callout("Cinema Studio 3.0 is available exclusively on Business and Team plans. Free and individual plan users should use Cinema Studio 2.5, which remains fully supported.")
        pdf.body_text(
            "Cinema Studio 3.0 is a separate generation engine from 2.5. Switch between them using "
            "the version selector in the upper-right corner of the Cinema Studio UI. Both versions coexist -- "
            "Cinema Studio 2.5 is NOT deprecated.")

        pdf.subsection_title("Resolution Comparison Table")
        w2 = [55, 55, 60]
        pdf.table_row(["Feature", "Cinema Studio 2.5", "CS 3.0 (Biz/Team)"], w2, bold=True, fill=True)
        pdf.table_row(["Video Resolution", "Up to 1080p", "Up to 720p (may increase)"], w2)
        pdf.table_row(["Image Resolution", "Up to 4K", "Up to 2K"], w2)
        pdf.table_row(["Max Duration", "12s", "15s"], w2)
        pdf.table_row(["Aspect Ratios", "6 options", "7 (+ 21:9 ultrawide)"], w2)
        pdf.table_row(["Audio", "On/Off", "On/Off (native stereo)"], w2)
        pdf.table_row(["Shot Control", "Manual multi-shot", "Smart + Custom"], w2)
        pdf.table_row(["Generation Cost", "Varies", "48 credits"], w2)
        pdf.ln(3)
        pdf.callout("Resolution limits for Cinema Studio 3.0 are subject to change. If you need higher resolution now, use Cinema Studio 2.5.")

        pdf.subsection_title("Key Differences in 3.0")
        pdf.bullet("Native dual-channel stereo audio -- generated simultaneously with video, not post-processed")
        pdf.bullet("Smart shot control -- model auto-plans camera based on genre and scene description")
        pdf.bullet("21:9 ultrawide aspect ratio (not available in 2.5)")
        pdf.bullet("Up to 15s video duration (vs 2.5's 12s)")
        pdf.bullet("7 genres: General, Action, Horror, Comedy, Noir, Drama, Epic")
        pdf.bullet("7 Speed Ramp presets: Auto, Slow-mo, Ramp Up, Flash In, Flash Out, Bullet Time, Hero Moment")
        pdf.bullet("No optical physics engine, color grading suite, 3D Mode, or Grid Generation (use 2.5 for these)")

        pdf.subsection_title("@ Reference Input Limits")
        w4 = [35, 45, 45, 45]
        pdf.table_row(["Type", "Max Count", "Formats", "Limit"], w4, bold=True, fill=True)
        pdf.table_row(["Images", "9", "jpeg/png/webp/bmp", "--"], w4)
        pdf.table_row(["Video clips", "3", "mp4/mov", "Combined <=15s"], w4)
        pdf.table_row(["Audio clips", "3", "mp3/wav", "Combined <=15s"], w4)
        pdf.table_row(["Total files", "<=12", "", ""], w4)

        pdf.ln(3)
        pdf.subsection_title("When to Use 3.0 vs 2.5")
        w5 = [85, 85]
        pdf.table_row(["Need", "Recommendation"], w5, bold=True, fill=True)
        pdf.table_row(["Highest resolution (1080p/4K)", "Cinema Studio 2.5"], w5)
        pdf.table_row(["Longer duration (up to 15s)", "Cinema Studio 3.0"], w5)
        pdf.table_row(["Native audio with video", "Cinema Studio 3.0"], w5)
        pdf.table_row(["Optical physics / color grading", "Cinema Studio 2.5"], w5)
        pdf.table_row(["3D Mode / Grid Generation", "Cinema Studio 2.5"], w5)
        pdf.table_row(["Ultrawide 21:9", "Cinema Studio 3.0"], w5)
        pdf.table_row(["Smart auto-camera", "Cinema Studio 3.0"], w5)
        pdf.table_row(["Free/Individual plan", "Cinema Studio 2.5"], w5)

        pdf.ln(5)
        pdf.subsection_title("Cinema Studio 3.5 -- Briefly")
        pdf.body_text(
            "Cinema Studio 3.5 sits alongside 2.5 and 3.0 in the model selector -- all three coexist, "
            "version is user-selected, no auto-routing. 3.5 collapses creative control into a three-pill "
            "main UI (Genre / Style / Camera), each defaulting to Auto with manual override. "
            "Camera Settings restores optical physics via a four-axis panel (Camera Body / Lens / "
            "Focal Length / Aperture, with 75mm added). Style Settings exposes three preset axes "
            "(Color Palette / Lighting / Camera Moveset Style) plus a free-form Manual Style mode. "
            "Image mode adds a Cinematic models picker with four options: Soul Cinema (default), "
            "Cinematic Characters, Cinematic Locations, and Cinematic Cameras (the latter surfaces "
            "the 2.5 optical vocabulary)."
        )
        pdf.callout(
            "For full Cinema Studio 3.5 documentation -- three-pill UI, Style Settings, Camera Settings, "
            "Manual Style mode, Image Mode, four Cinematic models picker, Physics Rendering Decision Matrix -- "
            "see the higgsfield-cinema sub-skill."
        )

        # --- 12. PROMPTING BEST PRACTICES ---
        pdf.add_page()
        pdf.section_title("12. Prompting Best Practices (Seedance 2.0)")
        pdf.v3_tag()
        pdf.ln(5)
        pdf.body_text(
            "These best practices apply to Cinema Studio 3.0's generation engine and complement "
            "the MCSLA formula. They are not a replacement -- use MCSLA as the primary framework, "
            "then apply these refinements.")

        pdf.subsection_title("Intent over Precision")
        pdf.body_text(
            "Tell the model WHAT you want and HOW it should FEEL, not every micro-detail. "
            "Short prompts (30-100 words) consistently outperform long ones. The model is an AI director "
            "you collaborate with, not a render engine you command.")

        pdf.subsection_title("Genre Router -- Prompt Length Targets")
        w6 = [50, 35, 85]
        pdf.table_row(["Genre", "Lead With", "Target Length"], w6, bold=True, fill=True)
        pdf.table_row(["Product/E-commerce", "Subject", "30-50 words"], w6)
        pdf.table_row(["Lifestyle/Social", "Action", "40-60 words"], w6)
        pdf.table_row(["Drama/Narrative", "Scene", "60-100 words"], w6)
        pdf.table_row(["Music Video", "Style", "50-80 words"], w6)
        pdf.table_row(["Landscape/Travel", "Scene", "30-60 words"], w6)
        pdf.table_row(["Commercial/Brand", "Style", "40-70 words"], w6)
        pdf.table_row(["Anime/Artistic", "Style", "50-90 words"], w6)

        pdf.ln(3)
        pdf.subsection_title("I2V Gate Rule")
        pdf.body_text(
            "When using image references (@Image), describe ONLY motion and camera movement. "
            "NEVER re-describe what's already visible in the image. The model can see the image -- "
            "re-describing creates conflict and degrades output.")

        pdf.subsection_title("Anti-Slop Vocabulary")
        pdf.body_text("Kill these words -- they add zero information and waste tokens:")
        w7 = [55, 115]
        pdf.table_row(["Kill", "Replace With"], w7, bold=True, fill=True)
        pdf.table_row(["beautiful/stunning", "(delete -- describe specific visual)"], w7)
        pdf.table_row(["epic", "large-scale, sweeping, towering"], w7)
        pdf.table_row(["amazing", "(delete -- show, don't tell)"], w7)
        pdf.table_row(["dynamic", "fast-tracking, whip-pan, handheld"], w7)
        pdf.table_row(["cinematic camera movement", "slow dolly push / crane up / tracking"], w7)

        pdf.ln(3)
        pdf.subsection_title("The One-Move Rule")
        pdf.body_text(
            "For any single shot, specify only ONE primary camera move. Do NOT stack multiple moves "
            "(e.g., dolly push + pan left + tilt up). This is the #1 cause of jitter, unwanted rotation, "
            "and failed generations.")

        pdf.subsection_title("Physics Language")
        pdf.body_text(
            "Use concrete physics consequences instead of mood words. "
            "Not 'powerful punch' but 'fist connects, sweat flies off in slow motion, opponent's head snaps back.' "
            "Not 'dramatic entrance' but 'door slams open, dust erupts from the frame, light floods the dark room.'")

        pdf.subsection_title("Audio as First-Class Element (SCELA)")
        pdf.body_text(
            "Describe audio separately in prompts. BGM, ambient SFX, and dialogue are parallel tracks "
            "via dual-channel stereo generation. Specific foley descriptions directly influence output: "
            "'the scratch of frosted glass, rustling plush fabric, gentle tapping on acrylic.'")

        pdf.subsection_title("No Negative Prompts")
        pdf.body_text(
            "Cinema Studio 3.0 does not support negative prompt syntax. Use positive constraints: "
            "'locked-off static camera' instead of 'no shaky camera.' "
            "'sharp focus throughout' instead of 'no blur.'")

        pdf.subsection_title("Aspect Ratio Is an Enum (Anamorphic is NOT Output Ratio)")
        pdf.body_text(
            "Output aspect ratio is a hard, enumerated platform spec -- Kling 3.0 emits 16:9, 9:16, "
            "or 1:1 and nothing else. 'Anamorphic' is a cinematography register (anamorphic lens "
            "flares, letterboxed composition, >2:1 framing aesthetic) that the model can render "
            "WITHIN any output ratio. Writing '16:9 anamorphic' as a single phrase in the prompt "
            "body is incoherent -- pick one. Output ratio belongs in the header (and must be one of "
            "the enum values for the chosen model -- check `higgsfield model get <model>` or the "
            "MCP `models_explore` equivalent before assuming). Anamorphic style cues belong in the "
            "Look line, as a style request, not as an output dimension.")
        w_ar2 = [55, 75, 40]
        pdf.table_row(["Concern", "Where it belongs", "Bound by"], w_ar2, bold=True, fill=True)
        pdf.table_row(
            ["Output ratio (16:9 / 9:16 / 1:1)",
             "Header (e.g. 'Aspect ratio: 16:9')",
             "Per-model enum"],
            w_ar2)
        pdf.table_row(
            ["Anamorphic / 2.35:1 / Scope",
             "Look line, as style ('anamorphic-style flares')",
             "Stylistic"],
            w_ar2)

        pdf.subsection_title("Frame Coordinate System (Seedance)")
        pdf.body_text(
            "Frame Coordinate System locks where subjects, props, and compositional elements sit "
            "inside the frame. Two notations, paired:")
        pdf.bullet("Qualitative anchors -- 'left third', 'center', 'right third'; 'upper third', 'lower third'; 'foreground', 'midground', 'background'")
        pdf.bullet("Percentage notation -- x-position 0% (left edge) to 100% (right edge); y-position 0% (top) to 100% (bottom); frame occupancy as a % of frame area")
        pdf.body_text(
            "Ship both notations in the same prompt, not as alternatives. The qualitative term "
            "gives the model the film-language hook; the percentage gives it the precision target. "
            "Example:")
        pdf.code_block(
            "Character A stands in the right third, x-position 70%, y-position 50%,\n"
            "frame occupancy 25%. Character B stands in the left third,\n"
            "x-position 25%, y-position 55%, frame occupancy 22%.")
        pdf.body_text(
            "Frame coordinates are a strong compositional anchor, NOT a geometric guarantee. The "
            "model treats them as directorial intent -- the same way a DP reads 'right third' on a "
            "storyboard -- not as pixel-exact targets. When a coordinate drifts in the output, "
            "tighten the qualitative anchor or add a contact-point clause ('feet on the marked "
            "floor mark') rather than re-specifying the percentage harder.")

        pdf.subsection_title("Spatial Layout Block (multi-character)")
        pdf.body_text(
            "A Spatial Layout Block is a named structural unit inside a Seedance prompt that "
            "consolidates the spatial-vocabulary fields into a single block the model can read as "
            "one coherent spatial brief. Scattered spatial directives force the model to reassemble "
            "scene geometry from fragments -- and it often picks the wrong reassembly.")
        pdf.body_text("A complete Spatial Layout Block names, per subject in frame:")
        pdf.bullet("Identity -- which character/prop/element this is (matches a Reference Role handle when references are present)")
        pdf.bullet("Screen position -- qualitative anchor + percentage notation paired per the Frame Coordinate System above")
        pdf.bullet("Depth layer -- foreground / midground / background")
        pdf.bullet("Frame occupancy -- % of frame area the subject fills")
        pdf.bullet("Body orientation -- direction the subject faces (toward camera, away, profile-left, three-quarter)")
        pdf.bullet("Contact points -- what physical surface or object the subject is grounded against")
        pdf.body_text(
            "Use a block when: more than one subject is in frame, a specific compositional intent "
            "needs to read across multiple shots, or the shot is in a failure-mode-prone category "
            "(door-entry, hallway-direction, around-furniture). Single-subject shots with a clear "
            "position don't need the full block -- a single qualitative-plus-percentage anchor "
            "inside the description suffices.")

        # --- 13. SOUL ID ---
        pdf.add_page()
        pdf.section_title("13. Soul ID -- Character Consistency")
        pdf.body_text(
            "Soul ID keeps a character looking the same across multiple generations. Upload a clear "
            "reference photo, create a Soul ID, and every future prompt can reference that same character.")
        pdf.subsection_title("Best Practices for the Reference Photo:")
        pdf.bullet("Front-facing or 3/4 angle -- full face visible")
        pdf.bullet("Even lighting -- no harsh shadows")
        pdf.bullet("Neutral expression (slight smile is fine)")
        pdf.bullet("Clear image -- no blur, no obstruction")
        pdf.bullet("Solo subject -- no other people")

        pdf.subsection_title("Cinema Studio 3.0 Character Consistency")
        pdf.v3_tag()
        pdf.ln(3)
        pdf.bullet("Use 2-3 clear, well-lit reference shots (frontal, 3/4-angle, side profile)")
        pdf.bullet("Outfit descriptions must be specific -- materials, colors, distinctive details")
        pdf.bullet("In I2V workflows: describe what the character DOES, not what they LOOK LIKE")
        pdf.bullet("If features drift: use character sheet directly as @Image1 for tighter anchoring")
        pdf.bullet("Multi-character scenes: reference each character separately with distinct @Image tags")

        # --- 14. CHARACTER SHEET ---
        pdf.section_title("14. Character Sheet Creation")
        pdf.body_text(
            "A character sheet is a multi-angle reference image showing the same character from several "
            "viewpoints -- front, 3/4, side profile, and back. It gives Soul ID far more geometry data "
            "than a single photo.")
        pdf.bullet("Generate your character using your preferred model")
        pdf.bullet("Use Grid Generation (2x2 or 4x4) to produce multiple variations")
        pdf.bullet("Use 3D Mode to orbit and capture front, side, and 3/4 angles")
        pdf.bullet("Arrange the best angles into a single composite reference image")
        pdf.bullet("Upload as your Soul ID reference")

        pdf.subsection_title("Character Anchor Block (per-shot, 10 attributes)")
        pdf.body_text(
            "Character Sheet Creation above is build-time -- the multi-angle identity reference "
            "that goes into Soul ID. The Character Anchor Block is shot-time -- the per-shot "
            "prompt structure that locks how that character appears IN a specific shot. The two "
            "work together: the sheet defines the identity, the block places that identity inside "
            "the frame for each shot.")
        pdf.body_text("A complete anchor block names, per character in frame, ten attributes:")
        pdf.bullet("Identity -- which character (matches a Soul ID handle when references are present)")
        pdf.bullet("Screen position -- qualitative anchor + percentage notation paired (see Section 12 Frame Coordinate System)")
        pdf.bullet("Depth layer -- foreground / midground / background")
        pdf.bullet("Frame occupancy -- % of frame area the character fills")
        pdf.bullet("Body orientation -- direction the character faces (toward camera, away, profile-left, three-quarter)")
        pdf.bullet("Pose -- current physical configuration (standing, seated, leaning, mid-stride)")
        pdf.bullet("Gaze direction -- where the character is looking, named by frame-position or by another subject ('looking at Character B')")
        pdf.bullet("Contact points -- what physical surface or object the character is grounded against")
        pdf.bullet("State lock -- current emotional or physical state (calm, exhausted, injured, soaked, in motion)")
        pdf.bullet("Facial expression -- specific emotional register (composed, fearful, smiling small, gritted teeth)")
        pdf.body_text(
            "The block sits before the Dynamic Description in a Seedance prompt and feeds a "
            "Spatial Layout Block (Section 12) when multiple characters share frame.")

        pdf.subsection_title("Two-Tool Refinement -- Soul Cinema + GPT Image 2")
        pdf.body_text(
            "For high-investment characters -- leads who carry many shots in a project -- initial "
            "generation in Soul Cinema plus refinement editing in GPT Image 2 produces stronger "
            "anchor sheets than either tool alone. Soul Cinema is Higgsfield's first-pass image "
            "surface (batches well against the character description); GPT Image 2 is OpenAI's "
            "edit surface that preserves existing image details -- particularly facial geometry -- "
            "when modifying outfits, accessories, lighting, or background elements.")
        pdf.body_text(
            "When to reach for both tools: the character will appear in tens of shots and is worth "
            "front-loading iteration cost into. The 90-minute Cannes feature's lead character "
            "absorbed ~600 Soul Cinema generations plus ~200 GPT Image 2 generations before any "
            "narrative shot generation began (see Section 9 for the full per-character iteration "
            "anchor). When to stick with one tool: characters appearing in only a handful of shots "
            "don't justify the two-tool overhead -- a single Soul Cinema pass suffices.")
        pdf.bullet("Multi-Form State Tracking -- when a character changes state across the project (wounds, costume changes, transformations), generate a separate anchor sheet per state. Full discipline in the higgsfield-soul sub-skill.")

        # --- 15. IDENTITY VS MOTION ---
        pdf.add_page()
        pdf.section_title("15. Identity vs. Motion Separation")
        pdf.body_text(
            "When Soul ID or character consistency is involved, every prompt must be split into two "
            "clearly labeled blocks:")
        pdf.bold_text("Identity Block -- Static visual descriptors ONLY")
        pdf.bullet("Face features, skin tone, body type, distinguishing marks")
        pdf.bullet("Clothing, accessories, color palette")
        pdf.bullet("NO motion, NO camera, NO temporal language")
        pdf.ln(2)
        pdf.bold_text("Motion Block -- Temporal and camera ONLY")
        pdf.bullet("Camera movement, action choreography, speed")
        pdf.bullet("Environmental motion, atmospheric changes")
        pdf.bullet("NO character appearance repetition")
        pdf.ln(3)
        pdf.bold_text("Example (Good -- separated):")
        pdf.code_block(
            "Identity Block:\n"
            "The Soul ID character -- sharp cheekbones, auburn hair shoulder-length,\n"
            "wearing a blue trench coat with silver buttons, lean athletic build.\n\n"
            "Motion Block:\n"
            "She runs through a rain-soaked alley, coat flapping behind her.\n"
            "Camera: Action Run -- low behind, matching pace.\n"
            "Neon reflections streak across wet concrete.\n"
            "Style: Cinematic, cold blue shadows, warm neon accents. 16:9.")

        # --- 16. GENRE RECIPES ---
        pdf.section_title("16. Genre Recipes")
        w8 = [55, 115]
        pdf.table_row(["Genre", "Story Pattern"], w8, bold=True, fill=True)
        pdf.table_row(["Action / Chase", "Establish -> Pursuit -> Obstacle -> Climax"], w8)
        pdf.table_row(["Emotional Drama", "Context -> Tension -> Breaking Point -> Resolution"], w8)
        pdf.table_row(["Horror", "Calm -> Unease -> Build -> Scare"], w8)
        pdf.table_row(["Product Ad", "Hero Shot -> Feature Detail -> Lifestyle -> CTA"], w8)
        pdf.table_row(["Sci-Fi", "World -> Discovery -> Conflict -> Revelation"], w8)
        pdf.table_row(["Romance", "Meeting -> Tension -> Connection Moment"], w8)
        pdf.table_row(["Documentary", "Environment -> Subject in Context -> Observational"], w8)
        pdf.table_row(["Dance / Music", "Establish Space -> Performance Builds -> Beat Sync"], w8)
        pdf.table_row(["Transformation", "Before State -> Trigger -> Transform -> After State"], w8)

        # --- 17. GENRE TEMPLATES ---
        pdf.add_page()
        pdf.section_title("17. Genre Templates")
        pdf.body_text("10 deeply annotated prompt templates in the templates/ folder. Each includes: "
            "when to use, recommended model, full example prompt, line-by-line annotation, "
            "negative constraints, common mistakes, variations, Identity/Motion blocks, "
            "and Cinema Studio 3.0 genre mappings with prompt length targets.")
        w9 = [10, 60, 50, 50]
        pdf.table_row(["#", "Template", "CS 3.0 Genre", "Prompt Length"], w9, bold=True, fill=True)
        tmpl = [
            ("01", "Cinematic Action Chase", "Action", "60-100 words"),
            ("02", "Product / UGC Showcase", "General", "30-50 words"),
            ("03", "Horror / Atmospheric Dread", "Horror", "60-100 words"),
            ("04", "Fashion / Editorial", "Drama/General", "40-60 words"),
            ("05", "Sci-Fi / VFX Spectacle", "Epic/Action", "50-90 words"),
            ("06", "Portrait / Character Intro", "Drama", "60-100 words"),
            ("07", "Landscape / Establishing", "Epic/General", "30-60 words"),
            ("08", "Comedy / Social Media", "Comedy", "40-60 words"),
            ("09", "Romantic / Intimate", "Drama", "60-100 words"),
            ("10", "Dance / Music Performance", "Action/Drama", "50-80 words"),
        ]
        for t in tmpl:
            pdf.table_row(list(t), w9)

        pdf.ln(3)
        pdf.subsection_title("Technique templates (Seedance multi-character coordination)")
        pdf.body_text(
            "When the request is technique-shaped rather than genre-shaped, four templates in "
            "`templates/seedance/` provide the structural scaffolding. Use these alongside (not "
            "instead of) the genre templates above.")
        w_tech = [70, 100]
        pdf.table_row(["Template", "What it is"], w_tech, bold=True, fill=True)
        pdf.table_row(["top-down-map.md", "Claude meta-prompt template for top-down spatial map pre-visualization"], w_tech)
        pdf.table_row(["multi-character-anchor.md", "Paste-ready Seedance multi-character anchor block template"], w_tech)
        pdf.table_row(["single-character-position.md", "Single-character shot with position + pose + contact-point locks"], w_tech)
        pdf.table_row(["worked-example-two-character.md", "End-to-end fill of the multi-character anchor (Roco + Lulu neo-noir alley)"], w_tech)

        pdf.ln(3)
        pdf.subsection_title("Text-overlay templates")
        pdf.body_text(
            "Paste-ready prompts for on-screen text rendering, in `templates/text-overlays/`.")
        w_text = [55, 115]
        pdf.table_row(["Type", "When to use"], w_text, bold=True, fill=True)
        pdf.table_row(["slogan.md", "Display text + entrance animation (brand callout, opening title)"], w_text)
        pdf.table_row(["subtitle.md", "Dialogue-synchronized subtitles"], w_text)
        pdf.table_row(["speech-bubble.md", "Character-attributed in-frame dialogue"], w_text)

        # --- 18. CINEMATIC IMAGE PROMPTS ---
        pdf.ln(5)
        pdf.section_title("18. Cinematic Image Prompts")
        pdf.body_text("The skill includes a complete cinematic shot reference for still images -- "
            "10 distance/size shots, 10 camera angles, and 17 camera movement keywords.")
        pdf.bold_text("Image Prompt Formula:")
        pdf.code_block("[Shot size] + [Angle] + [Movement keyword] of [character].\n[Pose]. [Environment]. [Lighting]. [Style].")

        # --- 19. NEGATIVE CONSTRAINTS ---
        pdf.add_page()
        pdf.section_title("19. Negative Constraints Reference")
        pdf.body_text("A shared constraints file consolidates all known AI generation artifacts "
            "and the prompt phrasing to prevent them.")
        w10 = [45, 70, 55]
        pdf.table_row(["Category", "Covers", "Check when"], w10, bold=True, fill=True)
        pdf.table_row(["Body / Motion", "Floating limbs, jittery motion", "Action prompts"], w10)
        pdf.table_row(["Face / Identity", "Face morphing, identity drift", "Character prompts"], w10)
        pdf.table_row(["Texture / Lighting", "Flickering, style ignored", "Style-heavy prompts"], w10)
        pdf.table_row(["Temporal", "Static I2V, camera fails, lip-sync", "Multi-shot, I2V"], w10)
        pdf.table_row(["Content Filter", "Blocked content, brands, persons", "Horror, branded"], w10)
        pdf.table_row(["Cinema Studio", "512 char limit, @ Element bugs", "CS 2.5 prompts"], w10)
        pdf.table_row(["CS 3.0 Notes", "No negative prompts -- positive only", "CS 3.0 prompts"], w10)
        pdf.ln(3)
        pdf.callout("Cinema Studio 3.0 does not support negative prompt syntax. All constraints must be phrased as positive statements. The shared constraints file includes a positive alternatives table.")

        # --- 20. TROUBLESHOOTING ---
        pdf.section_title("20. Troubleshooting")
        w11 = [55, 115]
        pdf.table_row(["Problem", "Quick Fix"], w11, bold=True, fill=True)
        pdf.table_row(["Character face keeps changing", "Soul ID + character sheet + Identity/Motion separation"], w11)
        pdf.table_row(["Video is static / not animating", "Describe ONLY what changes (I2V Gate rule)"], w11)
        pdf.table_row(["Camera movement ignored", "Use exact preset name (e.g. 'Dolly In')"], w11)
        pdf.table_row(["Style not applying", "Put style at end; use One Style Anchor Rule"], w11)
        pdf.table_row(["Generation filtered", "Check memory DB for known workarounds"], w11)
        pdf.table_row(["Too many actions", "Split into separate shots (One Action Per Shot)"], w11)
        pdf.table_row(["Identity drift during moves", "Separate Identity Block from Motion Block"], w11)

        pdf.ln(3)
        pdf.subsection_title("Cinema Studio 3.0 Diagnostic Tree")
        pdf.v3_tag()
        pdf.ln(3)
        w12 = [50, 50, 70]
        pdf.table_row(["Symptom", "Likely Cause", "Fix"], w12, bold=True, fill=True)
        pdf.table_row(["Blurry/jittery/morphing", "Overspecification", "Cut to 30-100 words, use @ref"], w12)
        pdf.table_row(["Camera chaotic", "Multiple moves", "ONE move per shot (One-Move Rule)"], w12)
        pdf.table_row(["Character mismatch", "Re-describing character", "Delete appearance, keep action"], w12)
        pdf.table_row(["Action stiff", "No physics language", "Add adverbs + consequences"], w12)
        pdf.table_row(["Just not right", "Ambiguous prompt", "Run Anti-Slop Check"], w12)
        pdf.table_row(["Audio mismatch", "Conflicting audio desc", "Timestamp anchor, remove SFX"], w12)

        pdf.ln(3)
        pdf.subsection_title("Seedance Failure Modes -- Named Catalog")
        pdf.body_text(
            "When a Seedance generation lands in a recognizable failure pattern, the named catalog "
            "in `skills/higgsfield-seedance/FAILURE-MODES.md` is faster than guessing. Eight named "
            "modes, each with a symptom, a mechanism, a prompt-side counter, and a worked example.")
        w_fm = [55, 60, 55]
        pdf.table_row(["Failure mode", "What you see", "Counter"], w_fm, bold=True, fill=True)
        pdf.table_row(
            ["FPS drift / dupe frames",
             "Choppy playback, duplicate frames",
             "State frame rate in body: '24 fps, no frame repeated'"],
            w_fm)
        pdf.table_row(
            ["Frame-level review mandatory",
             "Clip fine at speed; one bad frame in scrub",
             "Scrub frame-by-frame before approving any take"],
            w_fm)
        pdf.table_row(
            ["Failed-generation salvage",
             "Take rejected; instinct: discard",
             "Mark and bank the 1-3 usable seconds first"],
            w_fm)
        pdf.table_row(
            ["NSFW false-positive",
             "Clean prompt rejected by NSFW classifier",
             "Rephrase body-anatomy + sensual-register tokens"],
            w_fm)
        pdf.table_row(
            ["Keyframe forces invention",
             "Required element placed wrong (not in source frame)",
             "State the absence explicitly in prompt"],
            w_fm)
        pdf.table_row(
            ["Physics-state-anchor",
             "Adjacent object moves with target",
             "Name the invariant: 'X stays attached'"],
            w_fm)
        pdf.table_row(
            ["Multi-motion overload",
             "Stacked moves render as instability",
             "ONE dominant motion per shot; split compounds"],
            w_fm)
        pdf.table_row(
            ["Spatial-awareness failure",
             "Door-entry / hallway-direction shots fail",
             "Lock geometry with Spatial Layout Block (Section 12) first"],
            w_fm)
        pdf.ln(3)
        pdf.callout(
            "All eight failure modes include worked before/after examples in the sub-skill file -- "
            "consult that for the deep dive, this catalog for fast pattern-matching.")

        # --- 21. TOP TIPS ---
        pdf.add_page()
        pdf.section_title("21. Top Tips")
        tips = [
            "Be specific. Name camera presets, describe VFX concretely. 'Dolly In' beats 'the camera moves forward.'",
            "One action per shot. AI renders clean physics for one action. Chain multiple shots for complex sequences.",
            "Subject first, style last. Subject -> Action -> Camera -> Style is the most reliable prompt order.",
            "Keep it under 200 words. Focused prompts outperform exhaustive ones. For Cinema Studio 3.0: 30-100 words is the sweet spot.",
            "Cinema Studio 2.5: 512 character limit. @ Element chips consume ~80-100 hidden characters each.",
            "Use the Hero Frame method. Generate the perfect still image first, then animate it.",
            "Slow motion trick. If fast action keeps breaking, generate in Slow Mo and speed up in post.",
            "Don't say 'cinematic masterpiece.' Replace with actual visual details (One Style Anchor Rule).",
            "12-second cap. Multi-Shot Manual sequences max 12 seconds total across all scenes.",
            "Separate identity from motion. Keep face descriptors and camera/action in separate blocks.",
            "Check templates first. Before writing from scratch, see if a genre template matches your request.",
            "One-Move Rule. Specify only ONE primary camera move per shot to avoid jitter.",
            "Intent over Precision. Describe what you want and how it should feel, not every micro-detail.",
            "Audio is first-class. Describe BGM, SFX, and dialogue separately for Cinema Studio 3.0.",
            "Use @Video for complex motion. Camera transfer and choreography cloning via video reference is the most reliable method.",
        ]
        for i, tip in enumerate(tips, 1):
            pdf.bold_text(f"{i}.")
            pdf.body_text(tip)

        # --- 22. MEMORY SYSTEM ---
        pdf.section_title("22. Memory System (Advanced)")
        pdf.body_text(
            "The skill includes a memory system that stores what works and what doesn't. Content "
            "filter workarounds and quality failure fixes are stored in JSON databases and consulted "
            "automatically before generation.")
        pdf.callout("You don't need to manage this yourself -- Claude checks the memory automatically when the recall skill is loaded.")

        # --- 23. CINEMA STUDIO ADVANCED ---
        pdf.add_page()
        pdf.section_title("23. Cinema Studio Advanced Features")

        features = [
            ("Soul Cast -- AI Actor Generation (2.5 + 3.0)",
             "Generate AI actors from 8 parameter categories (Genre, Budget, Era, Archetype, Identity, "
             "Physical Appearance, Details, Outfit). In Cinema Studio 3.0 (Business/Team): General (2K) / Character (4K) / Location (4K) modes, 0.125 credits per image."),
            ("Built-in Color Grading (2.5 only)",
             "Color temperature, contrast, saturation, sharpness, film grain, exposure, bloom -- "
             "applied to keyframes before video generation. Not available in Cinema Studio 3.0."),
            ("3D Mode -- Gaussian Splatting (2.5 only)",
             "Generate an image, then enter 3D Mode to build a 3D version. Orbit the virtual camera "
             "to explore from any angle. Not available in Cinema Studio 3.0."),
            ("Grid Generation -- Batch Variations (2.5 only)",
             "Generate 2x2 (4 variations) or 4x4 (16 variations) from a single prompt. Not available in Cinema Studio 3.0."),
            ("Resolution Settings (2.5)",
             "Explicit resolution control: 1K (fast drafts), 2K (default), 4K (final delivery). "
             "Cinema Studio 3.0: up to 720p video, up to 2K image."),
            ("Frame Extraction Loop (2.5)",
             "Build an image -> Animate -> Extract a frame -> Feed it back -> Repeat."),
            ("Object and Person Insertion (2.5)",
             "Insert characters or objects not in your original start frame."),
            ("Smart Shot Control (3.0 only)",
             "Model auto-plans camera language based on genre and scene description. Trust it for "
             "genre-appropriate camera work. Override by switching to Custom multi-shot."),
            ("Native Audio-Video Joint Generation (3.0 only)",
             "Audio generated simultaneously with video via unified multimodal architecture. "
             "Dual-channel stereo. Sound design prompts directly influence both audio AND visual generation."),
        ]
        for title, desc in features:
            pdf.bold_text(title)
            pdf.body_text(desc)

        # --- 24. REPOSITORY CONTENTS ---
        pdf.add_page()
        pdf.section_title("24. Repository Contents")
        pdf.subsection_title("Root Files")
        w13 = [60, 110]
        pdf.table_row(["File", "What it is"], w13, bold=True, fill=True)
        root_files = [
            ("SKILL.md", "Main dispatcher -- routes requests to the right sub-skill"),
            ("README.md", "Installation and usage guide"),
            ("CHANGELOG.md", "Version history"),
            ("docs/user-guide/USER-GUIDE.pdf", "This document"),
            ("DISCIPLINE.md", "Cross-cutting discipline patterns (workflow / output / architectural)"),
            ("model-guide.md", "Model comparison tables + decision flowchart"),
            ("image-models.md", "Image model reference + pricing tiers"),
            ("vocab.md", "Full platform vocabulary reference"),
            ("prompt-examples.md", "High-quality example prompts"),
            ("photodump-presets.md", "29 Photodump style presets"),
            ("production-benchmarks.md", "Iteration anchors + Hollywood-validator cost comparisons"),
        ]
        for f in root_files:
            pdf.table_row(list(f), w13)

        pdf.ln(3)
        discovered = set(discover_sub_skills())
        declared = set(SUB_SKILL_DESCRIPTIONS.keys())
        if discovered != declared:
            added = discovered - declared
            removed = declared - discovered
            raise DictParityError(
                f"Sub-skill list out of sync between filesystem and SUB_SKILL_DESCRIPTIONS.\n"
                f"  In filesystem but undeclared: {sorted(added)}\n"
                f"  Declared but missing from filesystem: {sorted(removed)}\n"
                f"Update SUB_SKILL_DESCRIPTIONS at top of generate_user_guide.py."
            )

        pdf.subsection_title(f"Sub-Skills ({len(SUB_SKILL_DESCRIPTIONS)} total)")
        w14 = [55, 115]
        pdf.table_row(["Sub-Skill", "What it covers"], w14, bold=True, fill=True)
        for name, desc in SUB_SKILL_DESCRIPTIONS.items():
            pdf.table_row([name, desc], w14)

        # --- 25. FAQ ---
        pdf.add_page()
        pdf.section_title("25. FAQ")
        faqs = [
            ("Do I need a Higgsfield account?",
             "Yes -- this skill writes prompts for you, but you paste and run them on higgsfield.ai."),
            ("Do I need the Higgsfield CLI installed?",
             "No -- the skill works regardless of execution surface. The CLI is one of four ways to "
             "run the prompts Claude writes for you. Most casual users paste directly into "
             "higgsfield.ai. Heavy users on Claude Code or Codex benefit from the CLI's long-lived "
             "API tokens (better in headless and scripted contexts than the MCP's interactive OAuth). "
             "See Section 4 for the full picture."),
            ("Which Claude plan do I need?",
             "Any plan works -- Free, Pro, or Team. The skill loads as project instructions."),
            ("Do I need a Business/Team plan for Cinema Studio 3.0?",
             "Yes -- Cinema Studio 3.0 is exclusive to Business and Team plans on Higgsfield. Cinema Studio 2.5 is available on all plans."),
            ("Can I use this with other AI video tools?",
             "The prompts are optimized for Higgsfield specifically. General prompt techniques (MCSLA, shot framing) transfer to other tools."),
            ("How do I get updates?",
             f"The skill is versioned (currently v{META['version']}). Check the repository for updates."),
            ("Can I contribute?",
             "Yes! Fork the repo, add your improvements, and submit a pull request."),
            ("What changed since v3.0.0?",
             "Thirty platform releases shipped between v3.0.0 (April 2026) and this guide (v3.7.16). "
             "Major themes by era: install-path simplification, Seedance 2.0 prompt modes, Kling 3.0 Motion "
             "Control, and Cinema Studio 3.5 with Image Mode + Physics Rendering Decision Matrix "
             "(v3.3.0 through v3.6.x); a v3.7.0 metadata refactor making version and sub-skill discovery "
             "automatic; a v3.7.4 - v3.7.7 audit-corpus mega-release sequence that added production-"
             "benchmarks (Hell Grind Cannes-feature iteration anchors), Seedance Frame Coordinate System "
             "+ Spatial Layout Block + FAILURE-MODES catalog, and Soul Character Anchor Block + Two-Tool "
             "Refinement Pipeline; a v3.7.8 - v3.7.11 stack-integration arc that added the higgsfield-"
             "stack sub-skill (CLI / MCP / bundled-skills coexistence), two-step preflight discipline "
             "(schema verify before cost estimate), aspect-ratio-as-enum vs. anamorphic-as-style-register "
             "separation, and the dispatcher pre-delivery checklist; a v3.7.12 USER-GUIDE refresh closing "
             "the deferred PDF modernization arc; and a v3.7.13 - v3.7.16 cross-surface mega-arc that "
             "added the higgsfield-marketing-studio sub-skill (9 ad-video presets + ms_image cross-surface), "
             "USER-GUIDE rendering pipeline hardening (DejaVu Sans Condensed + Mono fonts, --dry-run smoke "
             "gate with exit-code matrix, validate.py subprocess integration), the cinematic-motion-language "
             "5-pillar translation to vocab.md (Camera Contract / Motion Physics Anchor / Lens Behavior "
             "Sequence / Spatial Zoning / Negative space expansion), and the higgsfield-gpt-image-2 sub-skill "
             "(Format A/B/C prompt taxonomy + static-ads ad-recreation satellite + DTC Ads cross-surface "
             "expansion). See CHANGELOG.md for full per-release detail."),
        ]
        for q, a in faqs:
            pdf.bold_text(f"Q: {q}")
            pdf.body_text(f"A: {a}")
            pdf.ln(1)

        # --- FOOTER ---
        pdf.ln(10)
        pdf.set_font("Body", "I", 11)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"Built by {META['author']} | v{META['version']} | {META['updated']} | Platform: higgsfield.ai", align="C")
    except FPDFException as e:
        raise RenderError(f"PDF rendering failed: {e}") from e

    if dry_run:
        print(f"DRY-RUN: pipeline OK ({pdf.page_no()} pages). Output NOT written.")
        return
    try:
        pdf.output("docs/user-guide/USER-GUIDE.pdf")
    except Exception as e:
        raise OutputWriteError(f"PDF write failed: {e}") from e
    print(f"Generated docs/user-guide/USER-GUIDE.pdf ({pdf.page_no()} pages)")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Regenerate USER-GUIDE.pdf.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Run dict-parity check + full build_pdf() rendering pipeline in-memory "
            "without writing the output file. Exit codes: 0 OK, 1 unknown, 2 "
            "frontmatter, 3 dict-parity, 4 font, 5 render, 6 output."
        ),
    )
    args = parser.parse_args()

    try:
        build_pdf(dry_run=args.dry_run)
        sys.exit(EXIT_OK)
    except FrontmatterError as e:
        print(f"FRONTMATTER ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_FRONTMATTER)
    except DictParityError as e:
        print(f"DICT-PARITY ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_DICT_PARITY)
    except FontError as e:
        print(f"FONT ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_FONT)
    except OutputWriteError as e:
        print(f"OUTPUT-WRITE ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_OUTPUT)
    except RenderError as e:
        print(f"RENDER ERROR: {e}", file=sys.stderr)
        sys.exit(EXIT_RENDER)
    except Exception as e:
        print(f"UNKNOWN ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(EXIT_UNKNOWN)
