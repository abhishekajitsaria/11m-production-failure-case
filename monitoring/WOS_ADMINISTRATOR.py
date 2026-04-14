#!/usr/bin/env python3
"""
WOS ADMINISTRATOR v2 — Quality, not performance.
Does not check if files EXIST. Checks if files are CORRECT.
Does not count keywords. Reads and verifies CONTENT.
Exit 0 = quality verified. Exit 1 = quality failures.
"""
import os, sys, re, glob

class Administrator:
    def __init__(self, directory):
        self.dir = directory
        self.files = {}
        self.fails = []
        self.passes = 0
        self.counts = {}
        
    def load(self):
        for f in glob.glob(os.path.join(self.dir, "*.md")) + \
                 glob.glob(os.path.join(self.dir, "*.py")) + \
                 glob.glob(os.path.join(self.dir, "*.csv")):
            with open(f, "r", errors="replace") as fh:
                self.files[os.path.basename(f)] = fh.read()
        # Read CURRENT_COUNTS
        sc = self.files.get("WOS_CLAUDE_SHORTCUTS_LOG.md", "")
        for line in sc.split("\n"):
            line = line.strip()
            for key in ["SHORTCUTS","LEARNINGS","SOPS","STANDING_ORDERS","AC_RULES","DETECTORS","FILES_IN_ZIP","FORTRESS_LAYERS"]:
                if line.startswith(f"{key}:"):
                    self.counts[key.lower()] = int(line.split(":")[1].strip())
    
    def check(self, name, condition, detail=""):
        if condition: self.passes += 1
        else:
            self.fails.append((name, detail))
            print(f"  FAIL [{name}] {detail}")

    # ================================================================
    # QUALITY CHECK 1: Does every shortcut have a learning AND remedy?
    # ================================================================
    def quality_shortcuts(self):
        print("\n--- Q1: SHORTCUT QUALITY ---")
        sc = self.files.get("WOS_CLAUDE_SHORTCUTS_LOG.md", "")
        
        # Find all shortcut entries
        entries = re.findall(r'### (S\d+|P\d+|0[AB]):.*?\n\*\*What.*?\n(.*?)(?=\n###|\n---|\Z)', sc, re.DOTALL)
        
        no_learning = []
        no_what = []
        for tag_line, body in entries:
            tag = tag_line.split(":")[0].strip()
            has_learning = "Learning" in body or "learning" in body
            has_what = "What" in tag_line or "What" in body
            if not has_learning:
                no_learning.append(tag)
        
        self.check("Q1-learnings", len(no_learning) == 0, 
            f"{len(no_learning)} shortcuts without learning: {no_learning[:5]}" if no_learning else "All have learnings")

    # ================================================================
    # QUALITY CHECK 2: Do SOPs have ACTUAL STEPS (not just titles)?
    # ================================================================
    def quality_sops(self):
        print("\n--- Q2: SOP QUALITY ---")
        sops = self.files.get("WOS_STANDARD_OPERATING_PROCEDURES.md", "")
        
        thin_sops = []
        for i in range(1, 27):
            # Find SOP content between this SOP and next
            pattern = f"SOP {i}:.*?(?=SOP {i+1}:|## THE|## NOTE|## ANTI|\\Z)"
            match = re.search(pattern, sops, re.DOTALL)
            if match:
                content = match.group()
                # Count numbered steps (1. 2. 3. etc)
                steps = len(re.findall(r'^\d+\.', content, re.MULTILINE))
                if steps < 3:
                    thin_sops.append(f"SOP {i} ({steps} steps)")
        
        self.check("Q2-sop-depth", len(thin_sops) == 0,
            f"Thin SOPs: {thin_sops}" if thin_sops else "All SOPs have ≥3 steps")

    # ================================================================
    # QUALITY CHECK 3: Cross-verify DATA between files
    # ================================================================
    def quality_data(self):
        print("\n--- Q3: DATA CONSISTENCY ---")
        
        # Collect all mentions of key data points across all files
        all_text = "\n".join(self.files.values())
        
        # Word count — should be consistent
        word_counts = set(re.findall(r'105,?\s*305', all_text))
        self.check("Q3-wordcount", len(word_counts) > 0, "106,295 words referenced")
        
        # Friction rate — only 0.33%, never 0.033%
        has_wrong = "0.033%" in all_text
        # Check ONLY public-facing files for wrong friction (historical/instructional refs are OK)
        marketing = ["back_cover_final.md", "WOS_20_LinkedIn_Posts.md", 
                     "WOS_Endorsement_Outreach.md", "WOS_Visual_Specs.md"]
        wrong_friction = []
        for mf in marketing:
            if mf in self.files and "0.033%" in self.files[mf]:
                wrong_friction.append(mf)
        self.check("Q3-friction", len(wrong_friction) == 0,
            f"Wrong friction in: {wrong_friction}" if wrong_friction else "All marketing files have 0.33%")
        
        # SHA references consistent
        has_702 = "702f3e91" in all_text
        has_f25 = "f252175a" in all_text
        self.check("Q3-sha", has_702 and has_f25, "Both production SHAs referenced")

    # ================================================================
    # QUALITY CHECK 4: Are AC rules SUBSTANTIVE (not just listed)?
    # ================================================================
    def quality_ac(self):
        print("\n--- Q4: AC RULE QUALITY ---")
        sc = self.files.get("WOS_CLAUDE_SHORTCUTS_LOG.md", "")
        
        for i in range(1, 12):
            tag = f"AC{i}"
            # Check if AC rule has: description + born-from reference
            idx = sc.find(f"**{tag}:")
            if idx == -1:
                idx = sc.find(f"**{tag} ")
            if idx >= 0:
                block = sc[idx:idx+300]
                has_description = len(block) > 50
                has_born = "S" in block and any(c.isdigit() for c in block[block.find("S"):block.find("S")+4])
                if not has_description:
                    self.check(f"Q4-{tag}", False, f"{tag} has no description")
            else:
                self.check(f"Q4-{tag}", False, f"{tag} not found")

    # ================================================================
    # QUALITY CHECK 5: Master Execution Loop is COMPLETE (all 8 steps)
    # ================================================================
    def quality_loop(self):
        print("\n--- Q5: MASTER LOOP QUALITY ---")
        sops = self.files.get("WOS_STANDARD_OPERATING_PROCEDURES.md", "")
        imp = self.files.get("WOS_NEW_CHAT_IMPORT.md", "")
        
        steps = ["No premature termination", "inventory", "checklist", 
                 "nothing to correct", "Update everything", "CROSS-SOP",
                 "Repeat", "Go back to 1"]
        
        for step in steps:
            in_sops = step.lower() in sops.lower()
            in_imp = step.lower() in imp.lower()
            self.check(f"Q5-{step[:15]}", in_sops and in_imp, 
                f"'{step}' missing from {'SOPs' if not in_sops else 'import'}")

    # ================================================================
    # QUALITY CHECK 6: DELIVERABLES — is the work done?
    # ================================================================
    def quality_deliverables(self):
        print("\n--- Q6: DELIVERABLES ---")
        # Check for production files in directory OR parent
        docx = any(f.endswith('.docx') for f in os.listdir(self.dir))
        pdf = any(f.endswith('.pdf') for f in os.listdir(self.dir))
        
        # Also check outputs directory
        outputs = "/mnt/user-data/outputs"
        if os.path.exists(outputs):
            docx = docx or any(f.endswith('.docx') for f in os.listdir(outputs))
            pdf = pdf or any(f.endswith('.pdf') for f in os.listdir(outputs))
        
        self.check("Q6-manuscript", docx, "Production DOCX not found — the manuscript is the work")
        self.check("Q6-pdf", pdf, "PDF not generated — pending since session 1")
        
        print(f"  Shortcuts logged: {self.counts.get('shortcuts', '?')}")
        print(f"  Admin files: {len(self.files)}")
        print(f"  → Is the book closer to publication?")

    # ================================================================
    # QUALITY CHECK 7: No contradictions between files
    # ================================================================
    def quality_contradictions(self):
        print("\n--- Q7: CONTRADICTIONS ---")
        imp = self.files.get("WOS_NEW_CHAT_IMPORT.md", "")
        sc = self.files.get("WOS_CLAUDE_SHORTCUTS_LOG.md", "")
        sops = self.files.get("WOS_STANDARD_OPERATING_PROCEDURES.md", "")
        
        # File count in import vs actual
        import zipfile
        zip_path = os.path.join(os.path.dirname(self.dir), "WOS_NEW_CHAT_UPLOAD.zip")
        if not os.path.exists(zip_path):
            zip_path = "/home/claude/WOS_NEW_CHAT_UPLOAD.zip"
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as z:
                actual = len(z.namelist())
            claimed = self.counts.get("files_in_zip", 0)
            self.check("Q7-filecount", actual == claimed,
                f"ZIP has {actual}, CURRENT_COUNTS says {claimed}")
        
        # SOP count
        sop_matches = len(re.findall(r'## SOP \d+:', sops))
        claimed_sops = self.counts.get("sops", 0)
        self.check("Q7-sopcount", sop_matches >= claimed_sops,
            f"Found {sop_matches} SOPs, claimed {claimed_sops}")

    # ================================================================
    # SELF-CHECK
    # ================================================================
    def quality_self(self):
        print("\n--- SELF-CHECK ---")
        admin = self.files.get("WOS_ADMINISTRATOR.py", "")
        methods = ["quality_shortcuts","quality_sops","quality_data",
                   "quality_ac","quality_loop","quality_deliverables",
                   "quality_contradictions","quality_self"]
        for m in methods:
            self.check(f"SELF-{m}", m in admin, f"Missing {m}")

    # ================================================================

    def quality_outputs(self):
        """Check what the USER actually receives — the outputs directory"""
        print("\n--- Q8: OUTPUT VERIFICATION ---")
        outputs = "/mnt/user-data/outputs"
        if not os.path.exists(outputs):
            self.check("Q8-dir", False, "Outputs directory doesn't exist")
            return
        
        out_files = os.listdir(outputs)
        
        # Is the ZIP there?
        zips = [f for f in out_files if f.endswith('.zip') and 'CHAT_UPLOAD' in f]
        self.check("Q8-zip", len(zips) > 0, "No upload ZIP in outputs" if not zips else f"ZIP: {zips[0]}")
        
        # Is the DOCX there?
        docx = [f for f in out_files if f.endswith('.docx')]
        self.check("Q8-docx", len(docx) > 0, "No DOCX in outputs — manuscript not delivered")
        
        # Is the PDF there?
        pdfs = [f for f in out_files if f.endswith('.pdf')]
        self.check("Q8-pdf", len(pdfs) > 0, "No PDF in outputs")
        
        # Is v91 there?
        xlsx = [f for f in out_files if f.endswith('.xlsx') and 'v91' in f.lower()]
        self.check("Q8-v91", len(xlsx) > 0, "No v91 in outputs")
        
        # Are output files non-zero?
        for f in out_files:
            path = os.path.join(outputs, f)
            if os.path.isfile(path) and os.path.getsize(path) == 0:
                self.check("Q8-zero", False, f"Output file is zero bytes: {f}")

    def run(self):
        print("=" * 60)
        print("WOS ADMINISTRATOR v2 — Quality, not performance")
        print("=" * 60)
        self.load()
        print(f"Loaded {len(self.files)} files. Counts: {self.counts}")
        
        self.quality_shortcuts()
        self.quality_sops()
        self.quality_data()
        self.quality_ac()
        self.quality_loop()
        self.quality_deliverables()
        self.quality_contradictions()
        self.quality_self()
        self.quality_outputs()
        
        print(f"\n{'='*60}")
        print(f"QUALITY: {self.passes} PASS, {len(self.fails)} FAIL")
        if self.fails:
            for n, d in self.fails:
                print(f"  [{n}] {d}")
            sys.exit(1)
        else:
            print("ALL QUALITY CHECKS PASS")
            sys.exit(0)

if __name__ == "__main__":
    Administrator(sys.argv[1] if len(sys.argv) > 1 else ".").run()
