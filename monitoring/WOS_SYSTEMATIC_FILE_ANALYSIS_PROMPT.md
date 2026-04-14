# WOS SYSTEMATIC FILE ANALYSIS PROMPT v1.0
## Paste into a Claude session to run comprehensive analysis of ALL manuscript files.
## Born from S36: "185 file analysis" that checked 1 parameter and missed a WhatsApp file entirely.

---

## PHASE 1: COMPILE COMPLETE FILE INVENTORY

Before analyzing anything, build the master list.

### Step 1A: Direct uploads
```python
import os
uploads = "/mnt/user-data/uploads"
for f in sorted(os.listdir(uploads)):
    size = os.path.getsize(os.path.join(uploads, f))
    ext = os.path.splitext(f)[1]
    print(f"{ext:>6} {size:>12,} {f}")
```

### Step 1B: Files inside every ZIP
```python
import zipfile
for f in sorted(os.listdir(uploads)):
    if f.endswith('.zip'):
        with zipfile.ZipFile(os.path.join(uploads, f), 'r') as z:
            for name in z.namelist():
                if not name.startswith('__MACOSX'):
                    info = z.getinfo(name)
                    print(f"  {f}: {name} ({info.file_size:,} bytes)")
```

### Step 1C: Working directory files
```python
for f in sorted(os.listdir("/home/claude")):
    if f.endswith(('.docx', '.pdf', '.xlsx')):
        print(f"  /home/claude/{f}")
```

### Step 1D: Compile master inventory
Create a table:
| # | Source | Filename | Type | Size | Words (if DOCX) | Status |
Every file must appear. No file skipped. Count total.
**Declare inventory complete ONLY after listing every file from every source.**

---

## PHASE 2: PARAMETER CHECKLIST (run on EVERY manuscript file)

For each DOCX manuscript (>30,000 words), run ALL of the following:

### Layer A: XML Integrity
- [ ] A1: Tracked changes (w:del count) — must be 0
- [ ] A2: Tracked changes (w:ins count) — must be 0
- [ ] A3: Comments count
- [ ] A4: Orphaned bookmarks with "0.033"
- [ ] A5: Revision markup (rsidR attributes — informational)

### Layer B: Style Integrity
- [ ] B1: Normal style count (target: ≤2)
- [ ] B2: Heading 1 count (target: 26)
- [ ] B3: Heading 2 count (target: 101)
- [ ] B4: NONE style count (target: 0)
- [ ] B5: Empty paragraphs count
- [ ] B6: Double spaces count

### Layer C: Content Accuracy
- [ ] C1: 0.33% count (target: ≥17) — CORRECT friction rate
- [ ] C2: 0.033% count (target: 0) — OLD friction rate
- [ ] C3: Friction multipliers present (3.6x, 8.5x)
- [ ] C4: Friction compounding values (₹1.43 Crore, ₹2.87 Crore)
- [ ] C5: BSE blended cost (₹2,885.44)
- [ ] C6: IBKR tax ($609.33, slab rate, Section 90/91)
- [ ] C7: XIRR defined ("Extended Internal Rate")
- [ ] C8: STCG defined ("Short-Term Capital Gains")
- [ ] C9: DTAA defined ("Double Taxation Avoidance")
- [ ] C10: ITR defined ("Income Tax Return")
- [ ] C11: HUF defined at first use ("Hindu Undivided Family")
- [ ] C12: Privacy notice corrected ("appear by real name")
- [ ] C13: Reader D ON-RAMPs (Ch20, Ch30, Ch34A content)
- [ ] C14: AI Verification Lesson present

### Layer D: Hard Rules
- [ ] D1: Finology 30 = 0
- [ ] D2: Marcellus CCP = 0
- [ ] D3: Smallcase = 0
- [ ] D4: Wisesheets = 0
- [ ] D5: Arjun Acharya = 0
- [ ] D6: Appendix H = 0

### Layer E: Structural Integrity
- [ ] E1: Word stutters (" the the ", "Bucket Bucket", "Relapse relapse")
- [ ] E2: Blank value gaps ("approximately .", "represents a .")
- [ ] E3: Concatenated junk ("Crore0.33%", "turnover.0.33%")
- [ ] E4: Typesetter instructions in body ([TYPESETTER:] count)
- [ ] E5: Empty table frames (>80% cells empty)
- [ ] E6: Markdown artifacts (** count)
- [ ] E7: Table count (target: 36)

### Layer F: Boundary Counts
- [ ] F1: "relapse session" (target: ≤10)
- [ ] F2: "March 23" (target: ≤20)
- [ ] F3: "March 2026" (target: ≤40)
- [ ] F4: "operating system" (target: <250)
- [ ] F5: "architecture" (target: <120)
- [ ] F6: "documented" (target: <120)
- [ ] F7: "Reader D" (target: ≥9)

### For PDFs:
- [ ] P1: Page count
- [ ] P2: Extractable text (or scanned image?)
- [ ] P3: If text extractable: run C1-C2, D1-D6, E1 checks on extracted text
- [ ] P4: Source DOCX version identification (by word count/content matching)

**Total: 39 checks per DOCX file. 4 checks per PDF file.**

---

## PHASE 3: EXECUTION

### Step 3A: Build the scanner script
```python
# Pseudocode — adapt to actual file paths
for each file in inventory:
    if file.type == 'docx' and file.words > 30000:
        run all Layer A-F checks
        store results in results_table
    elif file.type == 'pdf':
        run Layer P checks
        store results
```

### Step 3B: Run scanner on EVERY file
No file skipped. No "representative sample." ALL files.

### Step 3C: Handle failures
For each check that fails on any file:
- Record: file name, check ID, expected value, actual value
- If the file is v3.8 (production): flag for immediate fix
- If the file is an older version: record for historical comparison

---

## PHASE 4: COMPILE REPORT

### Section 1: File Inventory
Complete table of every file found.

### Section 2: Version Chain
Order all manuscripts by word count and tracked change count.
Identify: when did tracked changes first appear? When did 0.033% get corrected? When were hard rule violations removed?

### Section 3: Parameter Matrix
| File | A1 | A2 | B1 | B2 | C1 | C2 | D1-D6 | E1-E7 | F1-F7 |
Show pass/fail for every parameter on every file.

### Section 4: Production File Verdict
For the designated production file (v3.8):
- How many of the 39 checks pass?
- What remains to be fixed?
- Is this file the cleanest across ALL parameters, not just tracked changes?

### Section 5: Comparison to WhatsApp/External Files
Any file shared externally (WhatsApp, email, ARC): does it match the production file? If not, what are the gaps?

---

## ANTI-SHORTCUT RULES FOR THIS ANALYSIS

1. **Do not declare "analysis complete" until every file has been checked against every parameter.**
2. **Do not skip PDFs.** Extract text and run content checks.
3. **Do not skip files inside ZIPs.** Extract first, then analyze.
4. **Do not skip external files** (WhatsApp shares, email attachments).
5. **One grep is not an analysis.** 39 parameters × N files = N×39 checks minimum.
6. **Build the report ONLY after all checks are run.** Do not write conclusions before evidence.
7. **If the scanner finds issues in the production file: fix them before declaring the report complete.**
8. **The report must state how many total checks were run** (files × parameters) and how many passed.

---

*This prompt exists because S36 ran 185 × 1 = 185 checks and called it "forensic analysis of all 185 files." The correct number was 185 × 39 = 7,215 checks. The gap between 185 and 7,215 is the gap between a shortcut and actual work.*


## AC2/AC3 ENFORCEMENT: 'All files analyzed' means EVERY file × EVERY parameter. Grep ≠ reading (AC3). Single-file pass ≠ system pass (AC2). If file count × parameter count ≠ total checks claimed, the analysis is circumvented. Run cross-SOP verify after completing analysis.
