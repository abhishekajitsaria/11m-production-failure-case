# WOS Universal Session Audit — v3.4

**Supersedes:** v3.3
**Date:** 2026-04-18
**Origin:** S27 audit of POST v4_23 / PRE v4_13 / REWRITE v4_18 surfaced four detector gaps, patched in this version.
**Governance status:** Active. Supersedes v3.3 for all sessions opened after v3.4 is uploaded to `/mnt/project/`.

---

## Purpose

Session audit spec defining the gates, detectors, and verification protocols that govern every Claude session operating on WOS manuscript files. Paired with `WOS_PROMPTS_v3_4_TEST.py` (SHA `64de642b`) which implements the detectors.

---

## What changed from v3.3

Four detector patches, each grounded in specific false-positive or false-negative instances surfaced during S27:

### D1 — Mid-word truncations

**Problem in v3.3:** Regex matched only 1-3 char lowercase tails (`r' ([a-z]{1,3})$'`). Missed truncations where the dangling fragment is a complete-but-orphaned article or preposition:
- POST p928 ends `...Rule MV-R2 a` — `'a'` is a legitimate 1-char match but was filtered by `COMPLETE_SHORT` as a valid article
- POST p1186 ends `...terminal value from a` — same pattern

**Patch:** Added a secondary pattern that matches paragraphs ending on a lowercase article or preposition (a/an/the/to/from/of/with/for/by/on/in/at/as/is/and/or/but/into/onto/upon/than/that/this/these/those). These cannot legitimately end a declarative sentence, so their appearance at paragraph end with no terminal punctuation indicates truncation.

**Case-sensitivity:** Kept case-sensitive intentionally to avoid flagging title-case headers like "Who This Book Is For" — `"For"` in a header is legitimate; `"for"` mid-sentence at paragraph end is not.

**Result on POST v4_23:** v3.3 caught 0. v3.4 catches 7 — the 2 known-remaining from S25 Part 5A (p928, p1186) plus 5 previously unidentified (p321, p921, p1090, p2705, p3427). All 7 verified as genuine truncations via context inspection.

### D7 — Mid-list truncations

**Problem in v3.3:** Flagged enumerated lists that ended without terminal punctuation, even when the list was complete. MASTER Screener ten-criteria list (POST p530, PRE p559) triggered a false positive because `"...10. P/FCF: ≤20"` has no period after the final item.

**Patch:** Added list-completeness check. If a paragraph declares an item count ("ALL TEN CRITERIA", "five themes", "Three Rules") and the enumerated items reach that declared count with the final item containing substantive content, the list is considered complete and no flag fires.

**Implementation:** New `declared_count()` function parses the paragraph for count-declarations in the pattern `\b(?:ALL\s+)?(\w+)\s+(?:CRITERIA|RULES|ITEMS|STEPS|POINTS|THEMES|QUESTIONS|PRINCIPLES|CONDITIONS|FACTORS|CHECKS|TESTS|GATES|PHASES|PARTS|SIGNALS)\b`. Number-words `one` through `twelve` are mapped to integers.

**Result on POST v4_23:** v3.3 flagged 1 (false positive). v3.4 flags 0.

### D10 — Rule coverage

**Problem in v3.3:** Formal-definition detection required paragraph-head patterns (`R10:`, `RULE R10`, `R10 —`). Missed REWRITE R10 which is defined in body text as `(R10 — War Dip Protocol)` at p1726 and `The R10 War Dip Protocol operationalises this pattern` at p1730. v3.3 census reported REWRITE missing R10 formal def; manual post-check found it present.

**Patch:** Added two new formal-definition formats:
- **Format D:** parenthetical `(R10 — Protocol Name)` or `(R10: Protocol Name)`
- **Format E:** body-text `The R10 <Protocol Name>` where the rule number is immediately followed by a title-cased name + one of the protocol-type suffix words (Protocol, Rule, Gate, Ceiling, Filter, Cap, Cooling, Block, Limit)

**Result on POST v4_23:** v3.3 found 18 defined / 22 used / 4 gaps. v3.4 finds 19 defined / 22 used / 3 gaps — one previously-missed definition now correctly classified.

### D11 — Numerical consistency

**Problem in v3.3:** The portfolio-total detector flagged any `₹X.Y Crore` appearance where X.Y differs from 7.8 and the paragraph context contains "portfolio/family/total/author". False positive on POST p1204 which contains `"₹12,000 SIP ... compounding at 12% CAGR over 20 years grows to approximately ₹1.8 Crore"` — ₹1.8 Cr is a calculation outcome, not a portfolio-total variant.

**Patch:** Added calculation-context guard. Before flagging a ₹ amount as a portfolio-total variant, check a 300-char window around it for calculation markers (`CAGR`, `compounding at`, `grows to`, `accumulates`, `produces approximately`, `\d+ years`, `SIP`, `step-up`). If any marker appears, the amount is a calculation outcome and is skipped.

**Result on POST v4_23:** v3.3 flagged portfolio variants `[1.0, 1.8, 7.8]` (1 inconsistency). v3.4 flags 0 inconsistencies — the 1.8 and 1.0 mentions are both calculation outcomes.

---

## Unchanged from v3.3

All other detectors (D2/D3/D4/D5/D6/D8/D9/D12/D13/D14/D15/D16/D17/D18) unchanged.

All gates (G1-G10) unchanged.

All hard rules (R1-R22 in manuscript space + R23/R24 in governance space) unchanged.

The audit loop order remains: STEP 0 → G1 → STEP 1 → G2 → STEPS 2-3c → STEP 4 → STEPS 5-6 → G3 → G10 → G9 → G4 → STEP 7 → STEP 8 → 8a → G5-G8 → STEP 9.

---

## Regression test — v3.4 vs v3.3 on S27 canonical files

| File | Detector | v3.3 | v3.4 | Delta |
|---|---|---|---|---|
| POST v4_23 | D1 | 0 FAIL | 7 FAIL | +7 (all genuine) |
| POST v4_23 | D7 | 1 FAIL (false pos) | 0 PASS | corrected |
| POST v4_23 | D10 | 4 gaps | 3 gaps | −1 (one def recovered) |
| POST v4_23 | D11 | 1 FAIL (false pos) | 0 PASS | corrected |
| PRE v4_13 | D1 | 0 FAIL | 1 FAIL | +1 (to verify) |
| PRE v4_13 | D7 | 1 FAIL (false pos) | 0 PASS | corrected |
| PRE v4_13 | D10 | 3 gaps | 2 gaps | −1 |
| PRE v4_13 | D11 | 0 PASS | 0 PASS | unchanged |
| REWRITE v4_18 | D1 | 0 FAIL | 3 FAIL | +3 (to verify) |
| REWRITE v4_18 | D7 | 0 PASS | 0 PASS | unchanged |
| REWRITE v4_18 | D10 | 6 gaps | 5 gaps | −1 (R10 parenthetical recovered) |
| REWRITE v4_18 | D11 | 2 FAIL | 1 FAIL | −1 (portfolio false pos removed; 1,011/1,113 still flagged correctly) |

Net effect: 11 new real truncations surfaced, 3 false positives eliminated, 3 parenthetical definitions correctly classified.

---

## R23 + R24 hard rules (unchanged from v3.3, restated for completeness)

**R23-REGISTRY-FIRST:** Before replying to any state claim, pending-work recommendation, or classification of a manuscript issue, consult the relevant registry sheets (Sessions_Detail, Pending_Work, Shortcuts_Full, All_Files_Inventory, Data_Gaps, Audit_V41_Issues, Forensic_Events, Ghost_Audit). Registry is authority. Disk state is secondary. Memory is last. If the registry contradicts a forwarded claim or prior analysis, the registry wins.

**R24-VERIFY-BEFORE-EXECUTE:** Before executing any action (create file, create draft, send email, edit registry, modify document), verify action-state preconditions using the same authority hierarchy as R23: action-relevant live state (Gmail drafts/sent, outputs/, registry sheets) → tool-accessible secondary state → memory (last resort). If verification shows action redundant, conflicting, or operating on stale target, HALT and surface. R24 is symmetric to R23: R23 governs reply-side verification, R24 governs action-side verification.

---

## Gate priority (unchanged from v3.3)

Order: G1 → G2 → G3 → **G10** → G9 → G4 → G5 → G6 → G7 → G8.

G10 moves ahead of G9 because pre-execution verification might HALT *before* registry consistency matters for the action at hand. If G10 HALTs on a duplicate-action check, G9's registry-check on an unrelated file doesn't need to run yet.

---

## What v3.4 cannot do

All v3.3 limits preserved, plus:

- D1 still cannot catch truncations where the dangling word is a complete uncommon word (e.g., paragraph ending `...the conglomerate`). If `"conglomerate"` is a noun that could start a following clause, detection requires semantic parsing, which is out of scope.
- D7's list-completeness check only works when the paragraph declares a count. Lists that rely on implicit completeness ("a, b, and c" without declaring "three X") cannot be verified.
- D10's parenthetical matcher requires a dash (`—` / `–` / `-`) or colon separator between rule number and name. Other formulations still slip through.
- D11's calculation-context guard uses fixed markers. New calculation idioms (e.g., "yields", "returns", "becomes") not in the marker set will still trigger false positives until the list is extended.

All v3.4 detectors remain heuristic. They surface candidates; author judgment classifies.

---

## Upgrade path from v3.3 to v3.4

1. Upload `WOS_PROMPTS_v3_4_TEST.py` (SHA `64de642b`) to `/mnt/project/`
2. Upload `WOS_UNIVERSAL_SESSION_AUDIT_v3_4.md` (this file) to `/mnt/project/`
3. Archive v3.3 script if desired; retain for diff/regression purposes
4. Future sessions opening against `project_knowledge_search` will find v3.4 as the canonical audit spec

Author action required. Claude cannot write to `/mnt/project/`.

---

## Version history

- v1.0 — First zero-pending loop
- v2.0-v2.2 — Structured but hardcoded flaws
- v3.0 — Added chat iteration, rule extraction, drift detection
- v3.1 — Added 6 immunity-breaking gates (G1-G6)
- v3.2 — Widened to shortcut integrity + subject-areas + registry consistency (G7-G9)
- v3.3 — Added G10 pre-execution verification; R24-VERIFY-BEFORE-EXECUTE as symmetric partner to R23
- **v3.4 (this) — Patched D1/D7/D10/D11 detector gaps surfaced in S27 audit. No new gates, no new rules — implementation refinement only.**

---

*v3.1 made the audit refuse to run without action. v3.2 made the audit check the state it wasn't checking. v3.3 made actions verify the state they're about to modify. v3.4 sharpened the detectors to catch what v3.3 was missing and stop flagging what it shouldn't.*
