# WOS STANDARD OPERATING PROCEDURES
## Built from 93 shortcuts. Every SOP exists because its absence caused a failure.

---

## THE MASTER EXECUTION LOOP — Governs ALL work

**This is how every task is executed. No exceptions.**

```
1. No premature termination, no judgements
2. Prepare inventory of ALL items
3. Prepare checklist of ALL items
4. Run/execute checklist till nothing to correct
5. Update everything
6. CROSS-SOP VERIFY: every update propagated to ALL files that reference it
7. Repeat 4, 5, and 6 till nothing to correct
8. Go back to 1 till nothing more to correct
```

**Step 1:** Do not stop because "it looks done." Stop because the loop returned zero.
**Steps 2-3:** Inventory comes FIRST — you cannot check what you haven't listed. Checklist comes from inventory, not from memory.
**Steps 4-5 (inner loop):** Run checklist → fix all failures → run checklist again → fix again → until 0 failures after the latest fix. This is Standing Order 2.
**Step 6 (cross-SOP):** After EVERY update, verify it propagated across ALL SOPs, ALL files, ALL memory entries. A change in one file (renaming a sheet, updating a count, fixing a status) must be reflected in EVERY file that references it. Grep every file for the old value. This step exists because: renaming v90R→v91 in the spreadsheet left 4 other files still saying v90R. Updating shortcuts from 56→59→60 left 5 files at 56. Fixing marketing files left the Pending Actions status at NOT STARTED. Every fix is a change. Every change must propagate. If it doesn't, the fix created a new inconsistency.
**Step 7:** The inner loop with cross-SOP. Fixes + propagation checks until stable.
**Step 8 (outer loop):** After inner loop stabilises, restart from Step 1. Fresh inventory — because updates may reveal items not in the original inventory. Only when the outer loop also returns zero does the process end.

**Every SOP below is executed WITHIN this loop.** The loop is not one of the SOPs — it is the framework that contains all of them.

---

## STANDING RULES (apply at all times, not just during the loop)

**Standing Order 1:** Update immediately, never defer. Every shortcut, learning, remedy, or correction gets incorporated in the SAME response where identified. If unsure, ask "Should I update now?" Deferred updates become forgotten updates.

**Standing Order 2:** Run-Fix-Rerun loop (the inner loop of the Master Execution Loop). Run checklist → fix → run again → fix → run again → until 0 failures after the latest fix. Never declare done after one pass.

---

## THE 26 STANDARD OPERATING PROCEDURES

## SOP 1: NEW SESSION STARTUP
1. Read ALL uploaded files before starting any work
2. Run `python3 WOS_MVG.py <production_file.docx>` — must exit 0
3. Paste WOS_NEW_CHAT_IMPORT.md detectors into system
4. Verify production file SHA matches memory
5. Check memory entries for conflicts or stale data
6. Only THEN begin work
*Born from: S1 (unread files), S9 (wrong base), D9 (unread files detector)*

## SOP 2: EDITING THE MANUSCRIPT (DOCX)
1. Copy file to working directory before editing
2. Use python-docx ONLY — NEVER raw XML, NEVER LibreOffice
3. Use `paragraph.style=` — NEVER `paragraph.text=` (destroys runs)
4. Test edit on ONE paragraph before batch
5. After edit: `grep -c "w:del\|w:ins" document.xml` — both must = 0
6. After edit: run WOS_MVG.py — must exit 0
7. After edit: verify word count, para count, table count match expectations
8. Name output file by what was done, not by claims
*Born from: P8 (LibreOffice corruption), P9 (paragraph.text= destruction), S11 (batch without sim), S16 (accept would corrupt), D6 (filename claims)*

## SOP 3: VERIFYING A DOCX FILE
1. XML layer: `unzip -p file.docx word/document.xml | grep -c "w:del"` — must = 0
2. XML layer: `grep -c "w:ins"` — must = 0
3. Run WOS_MVG.py — all 8 layers
4. Check styles: Normal ≤2, H1 = 26, H2 = 101, None = 0
5. Check content: 0.33% ≥17, 0.033% = 0, all definitions present
6. Check hard rules: Finology/Marcellus/Smallcase/Wisesheets/Arjun = 0
7. Check stutters: " the the ", "Bucket Bucket", "Relapse relapse" = 0
8. Check boundaries: operating system <250, architecture <120, documented <120
9. Run QC v2.0 (SOP 11) — all 22 checks must pass
10. Run Rajiv Ghost v6.0 (SOP 12) — all 6 passes, no gate failures
11. NEVER declare "clean" or "verified" until ALL steps pass
*Born from: P13 (v2.9 "CLEAN" with 538 TC), S15 (no TC check), S18 (hours without XML check), S35 (1 check declared as analysis)*

## SOP 4: ANALYZING ALL FILES
1. Build COMPLETE file inventory: every upload, every ZIP contents, every working file
2. Include ALL file types: DOCX, PDF, MD, HTML, JSX, XLSX, CSV, images
3. Define parameter checklist BEFORE scanning
4. Run EVERY parameter on EVERY file — no sampling, no filtering
5. Compile comparative report with pass/fail matrix
6. Only declare analysis complete when files × parameters = total checks stated
*Born from: S35 (185×1 declared as 185×39), S36 (missed WhatsApp file), S38 (missed non-DOCX/PDF), S40 (filtered to DOCX only)*

## SOP 5: UPDATING FILES AFTER CHANGES
1. Make the change
2. Run the relevant checklist
3. If checklist fails → fix → run checklist again
4. Repeat until 0 failures AFTER the latest fix
5. Verify all counts are consistent across ALL files that reference them
6. Rebuild ZIP
7. Verify ZIP contents match source files
8. Present ZIP
*Born from: Standing Order 2 (Run-Fix-Rerun), multiple count mismatch incidents*

## SOP 6: LOGGING A SHORTCUT
1. Document WHAT happened
2. Document the LEARNING
3. Build the REMEDY in the same response
4. Update the shortcuts count in ALL files that reference it
5. Run checklist to verify no stale counts
6. Never log without remedy. Never defer the update.
*Born from: S30 (documented without remedy), S34 (writing ≠ implementing), Standing Order 1*

## SOP 7: CROSS-SESSION HANDOFF
1. Compile all output files into a single ZIP
2. Include CORRECTED versions of any files that were fixed (don't just flag — include the fix)
3. Note which production file SHA is current
4. Note any files that exist in LATER sessions but not this one
5. Update memory entries
6. Remove duplicate/conflicting memory entries
7. Verify memory matches ZIP matches import prompt
8. The import prompt in the ZIP is the authority — not any version displayed in chat
9. `unzip -t` the ZIP after building — verify no corruption
10. Verify file count in import prompt matches actual ZIP contents
11. Verify each listed file exists and is non-zero
12. Read key files from ZIP programmatically to verify content is current
*Born from: S43 (identified but never fixed marketing files), memory duplicate discovery, SHA conflict*

## SOP 8: CHECKING MARKETING/PUBLIC-FACING FILES
1. Extract from ALL source ZIPs
2. Check for: 0.033% (wrong friction), paid service names, old version references, old word counts
3. Fix ALL issues found
4. Include CORRECTED versions in the handoff ZIP
5. Check TYPESETTER handoff packages — do they contain the CURRENT manuscript?
6. If typesetter package has old manuscript → flag as 🔴 CRITICAL, do NOT send
*Born from: S40 (back cover with wrong friction), S44 (typesetter handoff with wrong manuscript)*

## SOP 9: MEMORY MANAGEMENT
1. After any significant work: update relevant memory entries
2. Check for duplicate entries across sessions
3. Check for conflicting data (different SHAs, different counts)
4. Keep the MORE CURRENT version when duplicates conflict
5. Verify memory matches the files in the ZIP
*Born from: Memory duplicate discovery (entries 2-12 vs 13-23)*

## SOP 10: MAKING CLAIMS
1. "Clean" requires: 0 tracked changes verified at XML level
2. "Analyzed" requires: every file × every parameter checked
3. "Complete" requires: all gates pass, all files updated, all counts consistent
4. "Production-ready" requires: MVG exit 0 + opened in Word + all marketing files corrected
5. If you cannot prove the claim with code output, do not make the claim
*Born from: P13 (CLEAN with 538 TC), S35 (cleanest after 1 check), S39 (evidence at 3.6%), S42 (MISSING without reading)*

---

## SOP 11: QUALITY CONTROL (QC v2.0 — 22 checks)
Run WOS_MANDATORY_QC_PROMPT_v2.md (merged into SOP 11) AFTER any manuscript edit, BEFORE declaring production-ready.
1. Checks 1-16: text layer (word count, styles, hard rules, content markers, stutters)
2. Checks 17-22: XML layer (w:del, w:ins, blank values, concatenated junk, orphaned bookmarks, comments)
3. ALL 22 checks must PASS
4. A file passing 1-16 but failing 17-22 is clean text in a corrupt container
5. Run AFTER MVG.py (MVG is the gate; QC is the detailed audit)
6. Quick check: `unzip -p file.docx word/document.xml | grep -c "w:del "` — must return 0
*Born from: S19 (QC had 16 checks, all text-layer, none caught 538 tracked changes). Checks 17-22 added because v2.9 "CLEAN" passed checks 1-16 perfectly.*

## SOP 12: RAJIV GHOST DEVELOPMENTAL EDIT (Ghost v6.0 — 6 passes)
Run WOS_RAJIV_GHOST_v6_PROMPT.md (merged into SOP 12) AFTER QC passes, BEFORE finalising for typesetter.
1. Pass 1: Sleep Test (pages 1-30) — drowsiness score, GATE if >6
2. Pass 2: 5-Point Scorecard — jargon, repetition, engagement, clarity, credibility + word frequency counts
3. Pass 3: Four Readers — A (₹10L first SIP), B (₹5-50L), C (₹50L-5Cr), D (₹5Cr+)
4. Pass 4: Jargon Audit — every term defined at first use, GATE if any used 5× before definition
5. Pass 5: Signpost Check — WHY THIS MATTERS hook, ON-RAMP box, ONE DECISION closing per chapter
6. Pass 6: Structural Hygiene — XML TC=0, blank gaps, junk patterns, privacy vs names, hard rules, boundary counts
7. ANY Gate Failure = max score 7.0/10
8. Run HERE first (trial), fix issues, re-run until passes, THEN optionally run on external tool for independent validation
*Born from: P6 (Ghost scored 9.7/10 on file with 538 TC — Pass 6 didn't exist), S20 (5 passes all blind to XML), S31 (recommended ChatGPT without running Ghost here first).*

## SOP 20: NON-DOCX FILE SCANNING
Different file types require different read methods:
1. MD/HTML/JSX/TXT: `open(path, 'r', encoding='utf-8', errors='replace')` → scan as text
2. XLSX: `openpyxl.load_workbook(path, data_only=True)` → iterate worksheets → join cell values as text → scan
3. PDF: `pdftotext path -` via subprocess → scan extracted text
4. CSV: `open()` as text or `csv.reader()` → scan
5. Images (PNG/JPG/SVG): cannot scan for text content — log as "image, not scanned"
6. For ALL scannable types: check for 0.033%, hard rule terms, paid service names, old version refs
7. Do NOT skip file types. "All files" means MD+HTML+JSX+XLSX+PDF+CSV, not just DOCX.
*Born from: S38/S40 (filtered to DOCX/PDF only, missed back_cover_final.md with wrong friction).*

## SOP 21: DEEP CHECKLIST CREATION & EXECUTION
When building an audit checklist:
1. INVENTORY: list every file in every location (uploads, ZIPs, outputs, working dir, memory)
2. CATEGORIZE: group checks by type (counts, cross-refs, content, integrity, memory, author decisions)
3. WRITE CHECKS: each check has ID, description, method (grep/read/code/tool), expected value
4. EXECUTE: run every check, record pass/fail/warning with detail
5. FIX: fix all failures
6. RE-RUN: run checklist again (fixes may introduce new issues)
7. REPEAT: until 0 failures after latest fix (Standing Order 2)
8. THINK HARDER: after stability, ask "what am I forgetting?" — check categories not in the checklist
*Born from: 7 audit runs in this session. Runs 1-2 caught surface issues. Run 3 found memory conflicts. Run 5 found handoff gap. Run 7 found unfixed marketing files.*

## SOP 22: MANUSCRIPT PARAGRAPH INSERTION (python-docx)
When inserting new content into the manuscript:
1. Find target paragraph by index: `doc.paragraphs[target_idx]`
2. Deepcopy the target element: `new_para = deepcopy(target_para._element)`
3. Clear existing runs from copy: remove all `w:r` children
4. Create new run: `etree.SubElement(new_para, qn('w:r'))`
5. Copy run properties from target's first run (preserves font/size)
6. Add text element with `xml:space='preserve'`
7. Insert after target: `target_para._element.addnext(new_para)`
8. VERIFY: read the paragraph back, confirm text is present
9. Run MVG.py after insertion
*Born from: AI Verification Lesson + Ch14 parallel insertion in this session.*

## SOP 23: MASP 8-GATE CHECK
Run before ANY "all clear" / "complete" / "verified" / "production-ready" claim:
1. GATE 1: Read EVERY uploaded file? (not just listed — actually opened and read)
2. GATE 2: Working on author's LATEST file, not a derivative?
3. GATE 3: Checked v90R/v91/Ghost/audits BEFORE saying "need source text"?
4. GATE 4: Ran ACTUAL CODE for every verification claim? (no ✅ without code output)
5. GATE 5: Completed all deferrable tasks? (nothing pushed to "next session")
6. GATE 6: Pre-ran author's checks (Ghost/QC/MVG)?
7. GATE 7: Logs complete across ALL sessions?
8. GATE 8: XML check — `grep -c "w:del|w:ins" document.xml` = 0?
If ANY gate fails: fix FIRST, then re-check. Do not declare with failed gates.
*Born from: S23 (MASP built without Gate 8), 93 shortcuts total.*

## SOP 24: DATA DISCREPANCY INVESTIGATION
When manuscript, Master Plan, and memory show different numbers:
1. List ALL sources for the data point (manuscript paragraph, v91 sheet, memory entry)
2. Identify the PRIMARY source (annual report, ICICI statement, BSE filing, order book)
3. Check which file was updated most recently
4. If primary source available: use it, update all others
5. If primary source unavailable: flag as DISCREPANCY in all files, mark for author verification
6. NEVER silently pick one number — document the conflict explicitly
*Born from: Private Treasury ₹1.70Cr (v91) vs ₹3.50-3.79Cr (manuscript). Net Worth ₹6.35Cr vs ₹7.8Cr.*

## SOP 25: ZIP PACKAGING & VERIFICATION
When building a handoff ZIP:
1. Copy ALL final files to a staging directory (new_chat_package)
2. `zip -r output.zip .` from the staging directory
3. `unzip -t output.zip` — verify no corruption
4. Verify file count matches import prompt
5. Verify EACH file listed in import prompt exists in ZIP
6. Verify file sizes in ZIP match staging directory (no stale copies)
7. Open ZIP programmatically: read key files, verify content (counts, references)
8. Present via present_files tool
*Born from: Multiple ZIP rebuilds where stale copies persisted.*

## SOP 26: ENDORSEMENT & MARKETING CONTENT REVIEW
When reviewing marketing files for hard rule violations:
1. Check for paid service names (Finology, Marcellus, Smallcase, Wisesheets)
2. DISTINGUISH: mentioning a company AS an outreach target for endorsement ≠ recommending their product to readers
3. Endorsement emails TO Finology founders → OK in marketing file, NOT OK in manuscript
4. Recommending Finology 30 subscription → NOT OK anywhere
5. When in doubt: flag for author decision with the specific context
*Born from: WOS_Endorsement_Outreach.md mentions Finology and Marcellus as endorsement targets.*

---

## SOP 13: VERSION CHAIN RECONSTRUCTION & CONTAMINATION TRACING
When working with multiple manuscript versions:
1. Extract ALL DOCX from ALL ZIPs + standalone uploads
2. For each: SHA, word count, para count, table count, tracked changes count
3. Sort by word count to establish chronological order
4. Identify contamination inflection points (where TC first appears, where it jumps)
5. Build version chain table: version → words → TC → status
6. Identify which versions are truly clean (TC=0) vs falsely labeled clean
7. Trace content markers across versions (when did each feature appear/disappear)
*Born from: v2.9 "CLEAN" discovery. Contamination appeared v7_Master_Final (24 TC), peaked v12.2 (575 TC), carried through v3.7.*

## SOP 14: EDITORIAL FREQUENCY REDUCTION
When word frequency targets are set (e.g., "operating system" <250):
1. Count current frequency: `full.lower().count("operating system")`
2. Calculate how many to replace: current - target + buffer
3. Identify safe replacements (e.g., "the operating system" → "the system")
4. SKIP: headings, titles, definitions, first-use contexts
5. Test on ONE paragraph first
6. Apply batch via run.text replacement (within existing runs, not paragraph.text=)
7. Verify: recount, confirm under target
8. Run MVG.py after to verify nothing broke
*Born from: Session 2 editorial pass — 50× opsys, 40× arch, 35× documented. Each tested on one before batch.*

## SOP 15: CROSS-SESSION MANAGEMENT
When working across multiple Claude sessions:
1. Differential export: list all files in current session, compare against prior session's inventory, export everything NOT in prior
2. Count synchronization: after adding shortcuts/learnings, update count in EVERY file that references it, then verify with grep
3. Memory deduplication: view memory, identify entries from different sessions, keep MORE CURRENT version, remove duplicates
4. SHA tracking: note which SHA is from which session, flag conflicts in import prompt
5. Import prompt must reference ALL known production file SHAs
*Born from: Memory duplicates (entries 2-12 vs 13-23), count mismatches (56 vs 60), SHA conflict (702f3e91 vs f252175a).*

## SOP 16: CONVERSATION FORENSIC AUDIT
When auditing a conversation for shortcuts:
1. Read FULL transcript — every line, not grep samples (S41/S54: read 4%, declared complete)
2. Extract every human message chronologically
3. For each exchange: what was asked, what was done, what was missed
4. Register every shortcut with: number, what happened, who caught it, learning
5. Cross-reference against existing shortcuts log — are there duplicates or gaps?
6. Count total shortcuts: must match across log, audit, memory, import prompt
*Born from: S41 (4% transcript reading), S54 (same pattern repeated).*

## SOP 17: TOOL BUILDING FROM FAILURE PATTERNS
When a shortcut reveals a gap in existing tools:
1. Identify WHICH tool should have caught it (MVG, QC, Ghost, MASP, Engine)
2. Add a check/layer/pass to that tool specifically for this failure mode
3. Test the updated tool on a file KNOWN to have the issue (must FAIL)
4. Test on a file KNOWN to be clean (must PASS)
5. Document the remedy in the shortcuts log WITH the shortcut, not after
*Born from: S30 (documented without remedy), Layer 8 (added to MVG after S35), Pass 6 (added to Ghost after P6).*

## SOP 18: MASTER PLAN MAINTENANCE
When updating the Master Plan spreadsheet:
1. Version Log: add new entries, mark old as SUPERSEDED with reason
2. Pending Actions: update stale references, add new tasks, mark completed
3. Reconciliation: verify data matches current manuscript version
4. Mistakes Register: add any new failures (including AI tool failures)
5. Net Worth Tracker: verify SUM formulas, check for empty columns
6. Insurance: verify policy status, dispute updates
7. Session Start: update to reference current production file
8. Save as new version number (v90R → v91 → v92)
*Born from: v91 creation — 6 sheets updated, stale v3.0 references found, AI audit entries added.*

## SOP 19: TRACKED CHANGES STRIPPING
When a DOCX has tracked changes that must be removed:
1. NEVER use "Accept All" in Word — may concatenate junk (S16)
2. Use lxml XML parser: parse document.xml, find all w:del elements, remove them
3. Find all w:ins elements, unwrap them (keep content, remove w:ins wrapper)
4. Check for orphaned runs after stripping
5. Check for blank value gaps created by deletion
6. Verify: `grep -c "w:del" document.xml` = 0, `grep -c "w:ins"` = 0
7. Run MVG.py on stripped file
8. Compare word count before/after — should change minimally
*Born from: v3.7→v3.8 stripping (253 del, 269 ins, 11 orphan runs). Regex failed — lxml required.*

---

*26 SOPs. 3 Standing Orders (including the Master Execution Loop). 93 shortcuts created them. Every procedure exists because its absence caused a documented failure.*

---

## ANTI-CIRCUMVENTION ENFORCEMENT — Applies to EVERY SOP above

After executing ANY SOP, run this 11-point check before declaring done:

| # | Check | If violated |
|---|-------|-------------|
| AC1 | Did I fix a value? → grep ALL files for old value | Fix without propagate = new inconsistency |
| AC2 | Does checklist cover cross-file consistency? | Single-file pass ≠ system pass |
| AC3 | Did I read full content or just grep? | Grep ≠ reading |
| AC4 | Did I verify at ALL layers (text + XML + structural)? | One layer ≠ verification |
| AC5 | Did I build a tool? → test on fail + pass cases | Untested tool = untested claim |
| AC6 | Did I write a learning? → did next response change? | Writing ≠ implementing |
| AC7 | Did inner loop pass? → restart outer loop | Inner stable ≠ system stable |
| AC8 | Did I identify a problem? → is the FIX in this response? | Identifying ≠ fixing |
| AC9 | Did I make a claim? → is code output proof present? | Claim without proof = S26 |
| AC10 | Did I use a remembered value? → verify against file | Memory ≠ truth |
| AC11 | Did I add a framework? → is it at the top, governing? | Appendix ≠ architecture |

**If ANY AC check fails: fix FIRST, then re-run SO3 from Step 4.**

---
## NOTE: ELIMINATED FILES — Content merged here
- WOS_MANDATORY_QC_PROMPT_v2.md (merged into SOP 11) → SOP 11 (QC v2.0)
- WOS_RAJIV_GHOST_v6_PROMPT.md (merged into SOP 12) → SOP 12 (Ghost v6.0)  
- WOS_ANTI_SHORTCUT_PROTOCOL.md → SOP 23 (MASP)
- WOS_SESSION_REPORT.md → superseded by Forensic Audit
- WOS_HANDOFF_TO_NEXT_SESSION.md → superseded by Import Prompt + Forensic Audit
