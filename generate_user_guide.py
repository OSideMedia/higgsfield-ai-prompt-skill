#!/usr/bin/env python3
"""Generate USER-GUIDE.pdf for Higgsfield AI Prompt Skill v3.0.0"""

from fpdf import FPDF


class UserGuidePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, "Higgsfield AI Prompt Skill - User Guide v3.0.0", align="L")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 30, 30)
        self.ln(4)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(70, 130, 180)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(50, 50, 50)
        self.ln(2)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bold_text(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(8, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 9)
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
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(50, 80, 120)
        self.set_line_width(0.3)
        # Draw left border
        self.line(x, y, x, y + 12)
        self.set_x(x + 5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 5, 5.5, text, fill=True)
        self.ln(3)

    def table_row(self, cols, widths, bold=False, fill=False):
        self.set_font("Helvetica", "B" if bold else "", 9)
        self.set_text_color(40, 40, 40)
        if fill:
            self.set_fill_color(235, 240, 250)
        h = 6
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.cell(w, h, col, border=1, fill=fill)
        self.ln(h)

    def new_tag(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(70, 130, 180)
        self.cell(18, 5, " NEW ", fill=True)
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 10)

    def v3_tag(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(46, 139, 87)
        self.cell(22, 5, " v3.0 ", fill=True)
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 10)


def build_pdf():
    pdf = UserGuidePDF()
    pdf.alias_nb_pages()

    # --- COVER PAGE ---
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 15, "Higgsfield AI", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, "Prompt Skill", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(80, 80, 80)
    pdf.ln(5)
    pdf.cell(0, 10, "User Guide", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 7,
        "A plain-English guide for getting the most out of this skill.\n"
        "No coding knowledge required.\n\n"
        "Teaches Claude how to write professional-quality prompts for\n"
        "Higgsfield AI -- the cinematic video and image generation platform.",
        align="C")
    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, "v3.0.0 | April 2026 | Built by O-Side Media", align="C")

    # --- TABLE OF CONTENTS ---
    pdf.add_page()
    pdf.section_title("Table of Contents")
    toc = [
        "1. What Is This?",
        "2. What Can It Do?",
        "3. How to Install",
        "4. Quick Start -- Your First Prompt",
        "5. The MCSLA Formula",
        "6. Choosing a Model",
        "7. Generation Types",
        "8. Cinema Studio 2.5",
        "9. Cinema Studio 3.0 (Business/Team Plan)  NEW",
        "10. Prompting Best Practices (Seedance 2.0)  NEW",
        "11. Soul ID -- Character Consistency",
        "12. Character Sheet Creation",
        "13. Identity vs. Motion Separation",
        "14. Genre Recipes",
        "15. Genre Templates",
        "16. Cinematic Image Prompts",
        "17. Negative Constraints Reference",
        "18. Troubleshooting",
        "19. Top Tips",
        "20. Memory System (Advanced)",
        "21. Cinema Studio Advanced Features",
        "22. Repository Contents",
        "23. FAQ",
    ]
    for item in toc:
        if "NEW" in item:
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(150, 7, item.replace("  NEW", ""))
            pdf.v3_tag()
            pdf.ln(7)
        else:
            pdf.set_font("Helvetica", "", 11)
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

    # --- 4. QUICK START ---
    pdf.section_title("4. Quick Start -- Your First Prompt")
    pdf.body_text("Just tell Claude what you want. Be as casual or specific as you like.")
    pdf.bold_text("Casual request:")
    pdf.code_block('"Write me a Higgsfield prompt for a woman walking through a foggy forest at dawn"')
    pdf.body_text("Claude will respond with a complete, ready-to-paste prompt including the model recommendation, camera movement, style, and all the details.")
    pdf.bold_text("More specific request:")
    pdf.code_block('"I need a Kling 3.0 prompt for a close-up dialogue scene between two characters\nin a coffee shop. Warm lighting, shallow depth of field, handheld camera."')

    # --- 5. MCSLA FORMULA ---
    pdf.add_page()
    pdf.section_title("5. The MCSLA Formula")
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

    # --- 6. CHOOSING A MODEL ---
    pdf.section_title("6. Choosing a Model")
    pdf.subsection_title("Video Models")
    w = [85, 85]
    pdf.table_row(["What you're making", "Best model"], w, bold=True, fill=True)
    rows = [
        ("Character-driven drama, dialogue", "Kling 3.0"),
        ("Epic scale, big environments", "Sora 2"),
        ("Lip-sync, multilingual dialogue", "Seedance 1.5 Pro"),
        ("Complex choreography, reference-based", "Seedance 2.0"),
        ("Long takes, camera control", "Kling Motion Control"),
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

    # --- 7. GENERATION TYPES ---
    pdf.add_page()
    pdf.section_title("7. Generation Types")
    pdf.subsection_title("Text-to-Video (T2V)")
    pdf.body_text("Describe the scene from scratch. No input image needed. Best for establishing shots, environments, abstract concepts.")
    pdf.subsection_title("Image-to-Video (I2V)")
    pdf.body_text("Upload a still image and describe what should move or change. Best for character consistency, product shots, bringing storyboards to life.")
    pdf.callout("Key rule for I2V: Do NOT re-describe what's already in the image. Only describe what should change or animate. (See I2V Gate rule in Section 10.)")

    # --- 8. CINEMA STUDIO 2.5 ---
    pdf.section_title("8. Cinema Studio 2.5")
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

    # --- 9. CINEMA STUDIO 3.0 --- NEW SECTION
    pdf.add_page()
    pdf.section_title("9. Cinema Studio 3.0 (Business/Team Plan)")
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

    # --- 10. PROMPTING BEST PRACTICES --- NEW SECTION
    pdf.add_page()
    pdf.section_title("10. Prompting Best Practices (Seedance 2.0)")
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

    # --- 11. SOUL ID ---
    pdf.add_page()
    pdf.section_title("11. Soul ID -- Character Consistency")
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

    # --- 12. CHARACTER SHEET ---
    pdf.section_title("12. Character Sheet Creation")
    pdf.body_text(
        "A character sheet is a multi-angle reference image showing the same character from several "
        "viewpoints -- front, 3/4, side profile, and back. It gives Soul ID far more geometry data "
        "than a single photo.")
    pdf.bullet("Generate your character using your preferred model")
    pdf.bullet("Use Grid Generation (2x2 or 4x4) to produce multiple variations")
    pdf.bullet("Use 3D Mode to orbit and capture front, side, and 3/4 angles")
    pdf.bullet("Arrange the best angles into a single composite reference image")
    pdf.bullet("Upload as your Soul ID reference")

    # --- 13. IDENTITY VS MOTION ---
    pdf.add_page()
    pdf.section_title("13. Identity vs. Motion Separation")
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

    # --- 14. GENRE RECIPES ---
    pdf.section_title("14. Genre Recipes")
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

    # --- 15. GENRE TEMPLATES ---
    pdf.add_page()
    pdf.section_title("15. Genre Templates")
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

    # --- 16. CINEMATIC IMAGE PROMPTS ---
    pdf.ln(5)
    pdf.section_title("16. Cinematic Image Prompts")
    pdf.body_text("The skill includes a complete cinematic shot reference for still images -- "
        "10 distance/size shots, 10 camera angles, and 17 camera movement keywords.")
    pdf.bold_text("Image Prompt Formula:")
    pdf.code_block("[Shot size] + [Angle] + [Movement keyword] of [character].\n[Pose]. [Environment]. [Lighting]. [Style].")

    # --- 17. NEGATIVE CONSTRAINTS ---
    pdf.add_page()
    pdf.section_title("17. Negative Constraints Reference")
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

    # --- 18. TROUBLESHOOTING ---
    pdf.section_title("18. Troubleshooting")
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

    # --- 19. TOP TIPS ---
    pdf.add_page()
    pdf.section_title("19. Top Tips")
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

    # --- 20. MEMORY SYSTEM ---
    pdf.section_title("20. Memory System (Advanced)")
    pdf.body_text(
        "The skill includes a memory system that stores what works and what doesn't. Content "
        "filter workarounds and quality failure fixes are stored in JSON databases and consulted "
        "automatically before generation.")
    pdf.callout("You don't need to manage this yourself -- Claude checks the memory automatically when the recall skill is loaded.")

    # --- 21. CINEMA STUDIO ADVANCED ---
    pdf.add_page()
    pdf.section_title("21. Cinema Studio Advanced Features")

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

    # --- 22. REPOSITORY CONTENTS ---
    pdf.add_page()
    pdf.section_title("22. Repository Contents")
    pdf.subsection_title("Root Files")
    w13 = [60, 110]
    pdf.table_row(["File", "What it is"], w13, bold=True, fill=True)
    root_files = [
        ("SKILL.md", "Model selection guide (routes model questions)"),
        ("README.md", "Installation and usage guide"),
        ("CHANGELOG.md", "Version history"),
        ("USER-GUIDE.pdf", "This document"),
        ("model-guide.md", "Model comparison tables + decision flowchart"),
        ("image-models.md", "Image model reference + pricing tiers"),
        ("vocab.md", "Full platform vocabulary reference"),
        ("prompt-examples.md", "High-quality example prompts"),
    ]
    for f in root_files:
        pdf.table_row(list(f), w13)

    pdf.ln(3)
    pdf.subsection_title("Sub-Skills (18 total)")
    w14 = [55, 115]
    pdf.table_row(["Sub-Skill", "What it covers"], w14, bold=True, fill=True)
    skills = [
        ("higgsfield-prompt", "MCSLA formula + Seedance 2.0 best practices"),
        ("higgsfield-image-shots", "Cinematic image prompting"),
        ("higgsfield-models", "Model selection guide + CS 3.0 comparison"),
        ("higgsfield-camera", "Camera controls + One-Move Rule + Smart Mode"),
        ("higgsfield-motion", "Motion presets + intent-first choreography"),
        ("higgsfield-style", "Visual styles + One Style Anchor Rule"),
        ("higgsfield-soul", "Soul ID + Soul Cast 3.0 character consistency"),
        ("higgsfield-audio", "Audio prompting + CS 3.0 native audio (SCELA)"),
        ("higgsfield-apps", "One-click Apps guide (80+)"),
        ("higgsfield-recipes", "Genre templates"),
        ("higgsfield-troubleshoot", "Fix generations + CS 3.0 diagnostic tree"),
        ("higgsfield-assist", "Platform copilot + credit optimization"),
        ("higgsfield-mixed-media", "Artistic preset overlays"),
        ("higgsfield-moodboard", "Moodboard + style consistency"),
        ("higgsfield-pipeline", "Multi-step production pipeline"),
        ("higgsfield-cinema", "Cinema Studio 2.5 + 3.0 (Business/Team)"),
        ("higgsfield-recall", "Pre-generation memory check"),
        ("higgsfield-vibe-motion", "Vibe Motion / motion graphics"),
    ]
    for s in skills:
        pdf.table_row(list(s), w14)

    # --- 23. FAQ ---
    pdf.add_page()
    pdf.section_title("23. FAQ")
    faqs = [
        ("Do I need a Higgsfield account?",
         "Yes -- this skill writes prompts for you, but you paste and run them on higgsfield.ai."),
        ("Which Claude plan do I need?",
         "Any plan works -- Free, Pro, or Team. The skill loads as project instructions."),
        ("Do I need a Business/Team plan for Cinema Studio 3.0?",
         "Yes -- Cinema Studio 3.0 is exclusive to Business and Team plans on Higgsfield. Cinema Studio 2.5 is available on all plans."),
        ("Can I use this with other AI video tools?",
         "The prompts are optimized for Higgsfield specifically. General prompt techniques (MCSLA, shot framing) transfer to other tools."),
        ("How do I get updates?",
         "The skill is versioned (currently v3.0.0). Check the repository for updates."),
        ("Can I contribute?",
         "Yes! Fork the repo, add your improvements, and submit a pull request."),
        ("What changed in v3.0.0?",
         "Three major additions: (1) Cinema Studio 3.0 documentation (Business/Team plan) with full specs, @ reference patterns, "
         "and native audio; (2) Seedance 2.0 prompting best practices integrated into MCSLA -- Intent over Precision, "
         "Genre Router, I2V Gate, Anti-Slop, Physics Language, One-Move Rule, SCELA audio; (3) All 10 genre templates "
         "updated with Cinema Studio 3.0 genre mappings and prompt length targets. All Cinema Studio 2.5 content preserved."),
    ]
    for q, a in faqs:
        pdf.bold_text(f"Q: {q}")
        pdf.body_text(f"A: {a}")
        pdf.ln(1)

    # --- FOOTER ---
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Built by O-Side Media | v3.0.0 | April 2026 | Platform: higgsfield.ai", align="C")

    pdf.output("USER-GUIDE.pdf")
    print(f"Generated USER-GUIDE.pdf ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build_pdf()
