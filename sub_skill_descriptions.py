#!/usr/bin/env python3
"""Per-sub-skill one-line descriptions for the USER-GUIDE.pdf sub-skill table.

Kept in this dependency-free module (no fpdf import) so tooling that only needs
the description data — notably validate_user_guide.py's Layer 0 column-fit check
— can import it without pulling in the PDF rendering stack. generate_user_guide.py
re-exports SUB_SKILL_DESCRIPTIONS for backwards compatibility.

These are editorial summaries, NOT extracted from frontmatter (which carries
routing-trigger language). Keep each entry within the column ceiling enforced by
validate_user_guide.py (SUB_SKILL_DESCRIPTION_CEILING).
"""

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
    "higgsfield-canvas":      "Node-based Canvas workspace + named patterns + Shared Canvas",
    "higgsfield-content-factory": "Campaign pipeline (research-plan-generate-publish-report) + cost report",
    "higgsfield-gpt-image-2": "GPT Image 2.0 director + static-ads + reference-sheet satellites",
    "higgsfield-marketing-studio": "Marketing Studio - 9 ad presets + 4-15s video + cross-surface",
    "higgsfield-recall":      "Pre-generation memory check",
    "higgsfield-vibe-motion": "Vibe Motion / motion graphics",
    "higgsfield-motion-design": "Animated-ad flow: brief -> storyboard -> Seedance video",
    "higgsfield-character-design": "Pre-production story bible: world, 9-Q character, visual DNA",
    "higgsfield-seedance":    "Seedance 2.0 + frame coords + spatial layout + named failure modes",
    "higgsfield-shotlist-director": "Brief -> connected Seedance shotlist HTML (prefix + @-glossary)",
    "higgsfield-facs":        "FACS Action Unit codes for precise facial expressions",
    "higgsfield-workspaces":  "Workspace-first decision layer",
}
