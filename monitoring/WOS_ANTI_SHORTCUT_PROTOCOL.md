# WOS MANDATORY ANTI-SHORTCUT PROTOCOL (MASP)
## Run at: session start, before every "all clear" declaration, and before final output
## Author: Should have been created by Claude. Was not. Author had to ask.

---

## TRIGGER: RUN THIS BEFORE EVERY RESPONSE THAT CONTAINS ANY OF THESE PHRASES:
- "all checks pass"
- "production-ready"
- "verified"
- "complete"
- "no issues found"
- "nothing to correct"
- "left for [someone else]"
- "editorial — not data"
- "need source text"
- "author decision"

If you are about to write any of the above, STOP. Run every gate below first.

---

## GATE 1: HAVE YOU READ EVERYTHING?

Before doing ANY work:

- [ ] List every uploaded file by name and size
- [ ] Have you OPENED and READ (not just listed) every .md, .docx, .xlsx prompt/instruction file?
- [ ] Have you EXTRACTED every ZIP completely (not just DOCX — also MD, HTML, JSX, XLSX, PNG, PDF)?
- [ ] Have you read the conversation's compacted summary (if one exists)?
- [ ] Have you checked Claude's memory for relevant context?

**If ANY box is unchecked: DO NOT PROCEED. Read first.**

---

## GATE 2: ARE YOU WORKING ON THE RIGHT FILE?

- [ ] What is the author's latest uploaded file? (Check SHA, not just name)
- [ ] Is the file you're editing the AUTHOR'S file or YOUR derivative?
- [ ] If the author uploaded a newer version, have you switched to it?
- [ ] Does the author's file contain edits not in your version? (Diff to verify)

**If working on your own derivative when the author has uploaded a newer file: STOP. Switch.**

---

## GATE 3: DID YOU CHECK THE RESOURCE FILES?

For every task, before declaring "need source text" or "this needs to be written":

- [ ] Check v90R — does any sheet contain the data needed?
- [ ] Check the Rajiv Ghost report — did it recommend this fix?
- [ ] Check the Grand Research Report — is this item flagged?
- [ ] Check ALL forensic audit files — is this item listed?
- [ ] Check ALL uploaded .md instruction files — do any address this?
- [ ] Check previous manuscript versions — did any contain this content?

**If ANY resource file contains relevant data: USE IT. Do not defer.**

---

## GATE 4: IS YOUR VERIFICATION REAL?

For every check you claim passes:

- [ ] Did you run actual code to verify (not just recall from earlier)?
- [ ] Did you search the FULL text, not just the first occurrence?
- [ ] Did you check for ABSENCE of things that should be absent (Finology 30, Marcellus CCP, 0.033%, Arjun Acharya, Wisesheets, Appendix H)?
- [ ] Did you check for PRESENCE of things that should be present (every v90R Reconciliation data point)?
- [ ] Did you verify the mathematical calculations (friction compounding, IBKR return %, BSE blended cost)?
- [ ] Are there any blank values, "approximately ." gaps, or missing figures?

**If you haven't run verification code for EACH claim: your check is fake. Run it.**

---

## GATE 5: ARE YOU DEFERRING ANYTHING YOU COULD DO NOW?

- [ ] Is anything marked "left for Ghost" or "editorial" that the Ghost report already flagged as a fix?
- [ ] Is anything marked "author decision" that is actually a factual accuracy issue (e.g., privacy notice)?
- [ ] Is anything marked "need source text" when v90R or a previous manuscript has the source?
- [ ] Is anything marked "for next session" that could be done in this one?
- [ ] Have you checked if any uploaded prompt file contains instructions you haven't executed?

**If ANY task is deferred that could be completed now: DO IT. Then declare complete.**

---

## GATE 6: WOULD THE AUTHOR'S OWN CHECKS CATCH SOMETHING YOU MISSED?

The author has built these checks. Run them BEFORE he does:

- [ ] Rajiv Ghost 5-pass audit (Sleep Test, Scorecard, Four Readers, Jargon, Signpost)
- [ ] Anti-Overconfidence check (repetition counts, boundary values, missing references)
- [ ] QC 16-point integrity check (styles, word count, table count, SHA)
- [ ] 56-point v90R data sync (every financial figure manuscript ↔ spreadsheet)
- [ ] Friction value audit (0.33% count, no blank "approximately ." gaps)
- [ ] Hard rule verification (no paid services, no real tickers, pseudonym compliance)

**If ANY of these would find something: fix it now, not after the author catches it.**

---

## GATE 7: IS YOUR OUTPUT LOG COMPLETE?

- [ ] Does the changelog document EVERY edit with paragraph number, old text, new text?
- [ ] Does the shortcuts log cover ALL sessions (not just today)?
- [ ] Does the sync report cover ALL data points (not just the ones that pass)?
- [ ] Does the version chain cover ALL manuscripts (not just the recent ones)?
- [ ] Have you noted discrepancies, not just matches?

**If ANY log is incomplete: complete it before presenting.**

---

## ENFORCEMENT

This prompt exists because across 24+ documented instances, Claude:
1. Did minimum viable work
2. Declared complete
3. Got caught by the author
4. Redid properly

The correct sequence is:
1. Read ALL resource files
2. Do exhaustive work
3. Run ALL gates above
4. Fix everything the gates catch
5. Run gates again
6. ONLY THEN declare complete

**The author should never have to build the tool's quality control system. This prompt should have been created by Claude in the first session. It was not. The author had to ask for it in the 24th shortcut.**

---

*Store this prompt in memory. Run it silently at every decision point. The author should never need to invoke it manually — if he does, that's shortcut #25.*

---

## LEARNINGS THAT GENERATED EACH GATE

| Gate | Born from shortcut | Learning |
|------|-------------------|----------|
| Gate 1 (Read everything) | S1, S2, 0A — partial extraction, unread prompts | Instructions exist to be read first. "ALL" means ALL. |
| Gate 2 (Correct base file) | S3 — built from wrong file | Author's upload is truth. Claude's derivative is draft. |
| Gate 3 (Check resources) | S8, S11, P2, P3 — "need source text" when data existed | Never defer when v90R/Ghost/audits have the answer. |
| Gate 4 (Real verification) | S4, P6, P10 — fake passes, stale memory | Coded checks miss content gaps. Memory lies. Re-read the file. |
| Gate 5 (Do it now) | S9, S10, P1 — deferred as "editorial"/"author decision"/refused | If the fix is within capability and a resource says do it, do it. |
| Gate 6 (Pre-run author's checks) | P2, P3, P6, P7 — author had to build QA tools | Claude should catch what the Ghost/Anti-Overconfidence catches — before the author runs them. |
| Gate 7 (Complete logs) | 0B, S12 — incomplete log, premature "all clear" | Accountability covers all sessions. "Complete" means verified complete. |

**NEW GATES ADDED FROM QC SESSION (S13-S17):**

## GATE 8: HAVE YOU CHECKED THE XML LAYER?

Before declaring any DOCX "clean," "production-ready," or "print-ready":

- [ ] Run `grep -c "w:del\|w:ins" document.xml` — are there tracked changes?
- [ ] If tracked changes exist: how many? Who created them? What date?
- [ ] Simulate accepting ONE tracked change before batch-accepting
- [ ] Check if tracked changes are positioned inline or appended to paragraph ends
- [ ] p.text is NOT the full picture — it hides tracked changes, comments, and revision markup

**If tracked changes exist in a "CLEAN" file: the file is not clean. Strip or accept, but VERIFY first.**

| Gate 8 (Check XML layer) | S13, S14, S15, S16, P13 — missed 253 tracked changes across 13 versions, named v2.9 "CLEAN" with 538 tracked changes | p.text ≠ XML. "CLEAN" filename ≠ clean file. Check tracked changes FIRST. |
| Gate 8 addendum | P13 — v2.9 named "CLEAN" and "SACRED FOUNDATION" with 538 tracked changes | A filename is a claim. Verify every claim against XML. |
| Gate 8 addendum | S16 — proposed accept when it would corrupt | Simulate on one paragraph before batch operations. |
| Gate 8 addendum | S17 — top-down grep instead of bottom-up XML | For files with corruption history: XML → paragraphs → runs → text. Always. |
