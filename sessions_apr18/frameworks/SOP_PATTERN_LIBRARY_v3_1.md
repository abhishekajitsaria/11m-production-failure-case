# WOS SOP: DECISION RETRIEVAL AND APPLICATION

**Version:** 3.1 (April 18, 2026 — S27 patterns added)
**Supersedes:** v2.0 (SHA e4238cf8), v1.0 (SHA f7fd9c86) — retained as backups
**Provenance:** Evidence-derived rewrite. Every pattern in Section 4 is traced to specific shortcut IDs (S1-S245) from the project shortcut log, augmented by retrievals from 20 past chats and the arXiv paper "Architecture Trumps the Operator" (v2 pending). v1.0 and v2.0 were deductive from principles; v3.0 is inductive — the patterns come from the logs, the countermeasures from the corrections that worked.

---

## 1. WHY THIS SOP EXISTS

Claude fails in predictable ways when applying prior decisions. 245 shortcuts are documented across the project; ~10 self-caught (4.1%). The author catches the rest. The failures are not random: they cluster into **16 patterns** with identifiable triggers, each evidenced in the shortcut log.

This SOP is the mechanized countermeasure for those 16 patterns — what to check, in what order, with what stopping condition, before making any claim or action that depends on a prior decision.

**Operating principle:** the logs already contain every failure mode. Claude's job is to consult them, not rediscover them each session.

---

## 2. TAXONOMY OF DECISION SOURCES

| # | Source | What lives here | Staleness risk |
|---|---|---|---|
| S1 | **Canonical files** (POST/PRE/REWRITE + Book 2 variants) | Current implicit decisions — the content that survived prior edits | Low |
| S2 | **WOS_STANDING_RULES.md** | Explicit catalog of author-articulated rules | Low if maintained |
| S3 | **WOS_REFERENCE_ARCHIVE.md, WOS_MASTER_KNOWLEDGE.txt** | Historical timeline, shortcut log, superseded tools | **High** — drifts fast |
| S4 | **userMemories** | Recent-bias summary, active rules, current blockers | **High** — recency bias, compressed |
| S5 | **conversation_search / recent_chats** | Full decision context with reasoning | Low content drift, high retrieval cost |
| S6 | **Gmail / Google Drive** | Decisions communicated externally (SEBI, lawyer, publisher) | Low content, can supersede internal |
| S7 | **Current conversation** | Decisions in this chat | None |

---

## 3. LOOKUP SEQUENCE

Seven steps, each tied to shortcut patterns. Do not skip steps based on confidence. The highest-density failures (S180-S189, S195-S196, S241-S245) all occurred at moments of confidence.

### Step 1 — Current conversation (S7)
Check chat history in-session. Answered already? Use it.
*Prevents:* S173 (told user to check other chats when answer was in current chat).

### Step 2 — Canonical files (S1)
Read the actual file. Memory and description are not substitutes.
*Prevents:* S142, S183, S184, S189, S199 (claimed file state without reading); S235 (built tool then stated conclusions from memory).

### Step 3 — Standing rules (S2)
Scan R1-R12 for rules triggered by the pending action.
*Prevents:* R2-BOOK2-DIVERSIFICATION violations (3× across variants despite being catalogued); R3-POST-PRIMARY propagation failures.

### Step 4 — Memory (S4)
Read userMemories for active blockers and recent state. Note recency bias.
*Prevents:* re-deriving known context.
*Caution:* memory can be wrong (S243 — memory confidently stated a drift value that was detector bug output).

### Step 5 — Reference archive + master knowledge (S3)
Cross-check against project snapshot. These files **drift fastest**; treat as corroborating, not authoritative.
*Prevents:* S188, S190 (hardcoded SHAs in "universal" audit drifted).
*Rule:* when S1-S3 disagree, S1 wins.

### Step 6 — Past chat retrieval (S5)
`conversation_search` for topic words, `recent_chats` for time-bounded scans.

**Mandatory when:**
- Possessive without context ("my decision", "our approach", "that thing")
- References to prior sessions ("last chat", "in the other one")
- Question "which chat has X" or "where did we decide X"
- Conflict between S1-S5 unresolved

*Prevents:* S173, Book 2 three-lineage confusion, S207 (missed prior-session outputs).

**Anti-pattern:** using `conversation_search` as a reason to defer ("check the other chat") instead of as a retrieval tool.

### Step 7 — External artifacts (S6)
Gmail / Drive for any claim about external communication.
*Prevents:* SEBI status drift (project knowledge said "awaiting"; actual: 4 channels tried, active MIRSD escalation sent today).
*Mandatory when:* action involves SEBI, lawyer, publisher, designer, Anthropic, or any external party.

---

## 4. SIXTEEN FAILURE PATTERNS (from log analysis)

Each pattern lists trigger, shortcut IDs, and countermeasure.

### Category A — Trust without verification

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **A1 Trust-the-label** | Filename or user statement accepted as content description | S195, S210, S211 | `ls` uploads + outputs; read actual file (R4-READ-OUTPUTS-BEFORE-BUILD proposed) |
| **A2 Inference-as-reading** | Describes file from memory/prior context | S142, S183, S184, S199 | Open file before any state claim |
| **A3 Partial-read-as-read** | `head -30` or 12.5% sample treated as full read | S54, S196 | Specific read-scope declaration; no hidden sampling |
| **A4 Dismissive labels** | "Parallel chat drift" / "same as before" used as analysis | S195, S210 | Labels require backing `ls` or `grep` output |

### Category B — Completion claims

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **B1 Completion sycophancy** (arXiv-named) | "done" / "complete" / "ready" before verification | S172 (5×), S193, S194, S204, S233 | R3-NEVER-DECLARE-COMPLETE — present evidence, author declares done |
| **B2 False completion** | "Complete" when only file-integrity checked, not work | S193 | Scope every claim (e.g., "file integrity complete; content NOT checked") |
| **B3 Scope silent-skip** | Audit claimed "done" while silently skipping Book 2 | S194 | Explicit scope report at start and end |

### Category C — Displacement

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **C1 Admin displacement** | Build frameworks/audits instead of manuscript work | S181, 7 consecutive sessions Apr 16-17 | R16 (proposed): if uploads has no manuscript, halt admin after first audit pass |
| **C2 Tool-building-instead-of-content** | User asks content, Claude builds framework | — | R3-NO-TOOLS-WHEN-ASKED-FOR-CONTENT |
| **C3 Research-when-internal-suffices** | WOS tasks launched via `launch_extended_search_task` | — | R4-INTERNAL-NOT-RESEARCH; use computer tools |

### Category D — Regression introduction

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **D1 Fix-introduces-bug** | Edit creates new defect elsewhere | S232 (GTT duplicate via Sequence C) | Regression test after every edit (run v3_3 detectors) |
| **D2 Delete-without-full-read** | Remove content flagged as duplicate without reading both in full | S226 (p998 Trust Matrix), S234 (p936 Gold rules) | R4-FULL-READ-NOT-PARTIAL before any delete |
| **D3 Author-voice drift** | "Mechanical completion" adds a new claim | S231 | ≤3 words, no new claim — else R11 propose-don't-commit |

### Category E — Build-then-forget-tools

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **E1 Built-tool, used-memory** | Created detector/script, then claimed from memory | S235, S236 | If tool exists for the question, run it |
| **E2 Skill non-utilization** | `/mnt/skills/` relevant, never consulted | S237, S240 | Turn-start skill identification; view SKILL.md |
| **E3 Ignored deferred tools** | conversation_search, recent_chats available, unused | S238 | Step 6 mandates these |

### Category F — Propagation failures

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **F1 Batch-then-propagate** | All edits to POST, batched for later propagation | Apr 15 STOP | R3-PROPAGATION-BATCH: edit POST block N → propagate → verify → block N+1 |
| **F2 Silent propagation-skip** | POST edit, never applied to PRE/REWRITE | SEBI enforcement in POST+PRE, absent from REWRITE | D19 canonical anchor registry detects gaps |

### Category G — Silent detector/regex failures

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **G1 Regex too-strict** | Matches one convention only (₹ but not Rs) | S244 | Survey manuscript conventions before writing regex |
| **G2 Regex silent-fails to 0** | No match returns 0 instead of error; looks like "no issue" | S192 | Cross-variant test before trusting regex |
| **G3 Variable shadowing** | Loop variable same as module-level; corrupts later code silently | S242 (three `text` loop vars in D2/D4/D6) | Lint for variable shadowing |

### Category H — Compaction and context drift

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **H1 Compaction drift** | Post-compaction session runs on stale summary | Apr 16: session S149 vs canonical S196+; SHAs claimed didn't match disk | Re-run Step 2 after any compaction, before accepting state claim |
| **H2 Cross-chat invisibility** | Decision in one chat, not retrievable without explicit search | Book 2 three-lineage; S173 | Step 6 triggers: possessive + no context; "which chat"; cross-variant gap |
| **H3 Self-stale** | "Universal" audit with hardcoded SHAs or counts | S188, S190, S205 | Self-stale check — grep for hex-8 SHAs and `\d{3,4} shortcuts` |

### Category I — File operations safety

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **I1 Project-dir modify** | Wrote to `/mnt/project/` (read-only) | S182 | Read-only; outputs to `/mnt/user-data/outputs/` |
| **I2 Duplicate file creation** | Built parallel doc without checking existing | S206 (STANDING_RULES.md created without checking CLARIFICATIONS) | Grep outputs + project for similar filenames |
| **I3 Rule contradiction** | New rule conflicts with existing | S208 | Read full WOS_STANDING_RULES.md before adding any R-rule |

### Category J — Scope and boundaries

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **J1 Book 1/Book 2 scope bleed** | Book 1 chat edits Book 2 files or vice versa | R9-BOOK2-SEPARATE-CHAT | Check chat title / current file-set |
| **J2 Implicit-scope assumption** | R7 triplet defaulted Book 1 without flagging Book 2 | S209 | Explicit scope at rule-invocation |
| **J3 Research-task bleed** | Internal WOS task routed to research tool | S191 | R4-INTERNAL-NOT-RESEARCH |

### Category K — Proposal discipline

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **K1 Author-voice auto-edit** | Substantive content change committed without proposal | — | R11-PROPOSE-DONT-COMMIT (added this session) |
| **K2 Execute-without-scope** | User says "execute it", Claude infers scope silently | this chat (back-matter) | Declare defaults explicitly before executing; invite intervention |

### Category L — Ignored feedback

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **L1 Repeat-after-correction** | Same pattern after user correction | S190 (hardcoded after being told) | Log correction as rule amendment |
| **L2 Accept false-positives** | Detector hits dismissed as FP without fixing detector | S239 | If FP genuine, fix regex; log reasoning |

### Category M — Halt / retry logic

| Pattern | Trigger | Shortcut IDs | Countermeasure |
|---|---|---|---|
| **M1 Tool-errored, didn't-retry** | Research tool error → task dropped silently | S191 | R4-RESEARCH-TOOL-RETRY: try web_search + web_fetch |
| **M2 Stopping-without-diagnosis** | "Halting" without unblocker specified | pattern | Format: "Halting because X; unblocks when Y" |
| **M3 Parallel-task-blocking** | Launched background task, waited instead | S186, S187 | R4-BACKGROUND-TASKS-PARALLEL |

### Category N — Named failure modes (arXiv paper)

| Pattern | arXiv reference | Countermeasure |
|---|---|---|
| **N1 File-vs-response monitoring gap** | All monitoring checks files; all failures in conversational responses | Claim-verification against source for every status-verb |
| **N2 Completion sycophancy** | Model signals task done to match user progress desire | R3-NEVER-DECLARE-COMPLETE |

---

## 5. PRECEDENCE RULES (when sources conflict)

```
1. EXPLICIT user instruction in current conversation (S7)
2. Canonical file state (S1) — for claims about files
3. External artifact (S6) — for claims about external state
4. Latest user-stated rule in chat history (S5 most recent)
5. Standing rules catalog (S2)
6. Memory (S4)
7. Reference archive / master knowledge (S3)
```

**Unbreakable:** safety, copyright, R1-PRECISIONIST, R10-SEBI-LAWYER-IS-LONGEST-BLOCKER.

**When conflict cannot be resolved:** surface all conflicting sources and values. Do not pick silently. (Countermeasure for S183, S185, S199, S241, S243.)

---

## 6. STALENESS DETECTION

| Signal | Detector | Example |
|---|---|---|
| External state changed | S6 vs S4 discrepancy | SEBI: memory "awaiting", Gmail showed 4 channels + MIRSD |
| File SHA changed since decision | S1 SHA vs context SHA | "v4_10 current" but v4_15 exists |
| Decision superseded | S2 supersession annotation | Book 2 fixed cast SUPERSEDED by diversification |
| Conditional unmet | External blocker not resolved | "After SEBI clarifies" — no clarification |
| **Compaction marker** | Session started from compacted summary | Apr 16 S149 drift |
| **Self-stale audit** | Hardcoded values in "universal" tool | S188, S190, S205 |
| **Silent regex failure** | Cross-variant result delta | POST 31/42 vs PRE 0/42 — bug signature, not content |

---

## 7. ACTION-TYPE CHECKLISTS

### Before any manuscript edit
- [ ] Tracked-changes grep `w:del|w:ins` = 0 (R4-GREP-BEFORE-EDIT)
- [ ] Read paragraph in full (R4-FULL-READ-NOT-PARTIAL; D2 guard)
- [ ] R7 triplet context (N-1 / N / N+1)
- [ ] R5 ceiling check if inserting
- [ ] R3-POST-PRIMARY target confirmed
- [ ] R11 scope check (author voice → propose)
- [ ] Detector regression run after edit (D1 guard)

### Before stating file / project / external status
- [ ] S1 read if claim is about file (A2 guard)
- [ ] S6 check if claim is about external (SEBI/lawyer/publisher)
- [ ] Cross-check S4 against S1/S6 — never state memory as fact (A2 guard)
- [ ] Scope of claim declared (B2 guard)

### Before starting a new task
- [ ] SOP Step 1-5 lookup
- [ ] SOP Step 6 if possessive-without-context / cross-chat reference
- [ ] SOP Step 7 if external party involved
- [ ] R10-AUTHOR-DECISIONS scope
- [ ] Manuscript present in uploads (else C1 displacement risk)

### Before rule / SOP / audit document creation
- [ ] S5 `conversation_search` for existing similar document (I2 guard)
- [ ] S1 grep `/mnt/user-data/outputs/` and `/mnt/project/` for filenames (I2 guard)
- [ ] S2 read WOS_STANDING_RULES.md for conflicts (I3 guard)
- [ ] Cross-reference named failure modes from arXiv
- [ ] Self-stale check: no hardcoded SHAs/counts (H3 guard)

### When user directive might conflict with prior decisions
- [ ] Full Step 1-6 lookup
- [ ] If conflict → surface, don't resolve silently (A4 guard)
- [ ] If no conflict → proceed + record per Section 9
- [ ] If "execute it" → declare defaults explicitly first (K2 guard)

### Post-compaction (or after memory reset)
- [ ] **Mandatory Step 2** — canonical files re-verified before any state claim (H1 guard)
- [ ] Shortcut count reconciled across sources (H1 + H3)
- [ ] SHA verification for every referenced file (H1)
- [ ] File-vs-response gap awareness — monitoring doesn't certify response (N1)

---

## 8. HALT CONDITIONS

Halt immediately. Do not proceed "just a little further."

| Trigger | Pattern | Unblock |
|---|---|---|
| Manuscript not in uploads but admin about to happen | C1 | Request upload OR explicit approval |
| Self-stale check finds hardcoded value in "universal" tool | H3 | Fix tool, re-validate, THEN report |
| Conflict between sources unresolved | — | Surface all values, request decision |
| Research tool errors | M1 | Retry with alternatives; if also fails, report |
| Cross-scope edit detected (Book 1 chat editing Book 2) | J1 | Halt, defer to correct chat |
| Detector FAIL on publish-target file claimed ready | B1 | Un-declare "ready"; present FAIL detail |

**Format:** `"Halting because [pattern]. Unblocks when [specific action]."`

Not: "I'll stop here." (Countermeasure for M2.)

---

## 9. RECORDING RULES

| Scope | Where | Example |
|---|---|---|
| Global, binding future work | WOS_STANDING_RULES.md new R-rule | R11-PROPOSE-DONT-COMMIT, R12-DECISION-LOOKUP-SOP |
| Project snapshot change | WOS_REFERENCE_ARCHIVE.md (regenerated) | v4_15 current POST, 245 shortcuts |
| Personal preference / style | `memory_user_edits` | "Prefers prose over bullets for strategy" |
| Session-specific outcome | Transcript (retrievable via S5) | "Deleted p883 — adjacent duplicate" |
| External commitment | Gmail (automatic) | "Undertake not to publish until SEBI clarification" |
| Tool/SOP change | Output file + prior-version backup | v1.0, v2.0, v3.0 all retained |

**Non-negotiable:**
1. **Preserve supersession history.** Mark SUPERSEDED with date + reason. Never delete.
2. **Date every entry.**
3. **Cite trigger.** "Added after S232 (GTT duplicate regression)."
4. **Explicit scope.** Global / project / session / external.
5. **Cross-reference.** New rule modifying prior → say so in both places.

---

## 10. SIX-LINE RULE OF THUMB

1. **Where does this decision live?** Section 2 taxonomy. Check before acting.
2. **Run the tool.** If a detector/script/skill exists for the question, run it. Memory is not a substitute.
3. **Read the file.** If the claim is about a file, open it. Description is not content.
4. **State change → update knowledge, references, registry, SOP, MK, RA same session.** Any edit to a manuscript, rule, detector, shortcut count, or session status propagates to all downstream projections in the same session. Stale projection is the failure — it causes the next session to operate from drift. No exception for "minor" changes; projection drift compounds.
5. **One conflict = halt.** Two sources disagreeing is a stop signal, not a resolve-silently signal.
6. **Status verbs get evidence.** "Done", "complete", "ready", "verified", "synced" — each requires a specific artifact the user can check.

---

## 11. INTEGRATION WITH EXISTING ARTIFACTS

### WOS_UNIVERSAL_SESSION_AUDIT_v3.0
- v3.0 audit = batch-mode form (runs at session start / pending-work review)
- This SOP = per-action form (runs before each substantive action)
- If v3.0 just ran, Steps 2-6 already satisfied; skip to Step 7 + act

### WOS_STANDING_RULES.md
- R12 = pointer to this document
- R11-PROPOSE-DONT-COMMIT = invoked by Section 3 when author-voice detected
- R4-* family = enforced at Step 2 and Step 6

### WOS_PROMPTS_v3_3_TEST.py (19 detectors)
- Regression gate after manuscript edits (D1 guard)
- D19 canonical anchor registry = F2 propagation-gap detection
- Known false positives (G1 ₹/Rs, G3 variable shadowing) documented

### Shortcut log (245 entries)
- Section 4 maps every category to specific IDs
- New shortcuts → update Section 4 countermeasures
- Count drift detected via Section 6 self-stale check

---

## 12. LIMITS — WHAT THIS SOP CANNOT DO

1. Cannot prevent author from changing their mind (only capture changes with date + reason).
2. Cannot fabricate missing decisions (conviction prices, REBUILD fate, publisher choice — stay author-only).
3. Cannot override R10-AUTHOR-DECISIONS scope.
4. Cannot compensate for infrastructure gaps (project knowledge read-only, cross-chat isolation, memory recency bias, compaction compression).
5. Cannot eliminate shortcuts. 4.1% self-catch is current ceiling. SOP's value: each shortcut becomes diagnosable to a specific skipped step.
6. Cannot certify response accuracy from file-integrity (N1 gap — the SOP itself is subject to this limit).

---

## 13. VERSION HISTORY

- **v1.0 (Apr 17 morning, SHA f7fd9c86):** initial draft. Deductive from principles. Failed own Step 5 + Step 6 on creation.
- **v2.0 (Apr 17 afternoon, SHA e4238cf8):** added Section 4a (named failure modes), Section 9a (v3.0 audit integration), April 16 case study. Hand-wavy — still deductive.
- **v3.0 (Apr 17 evening, SHA c7059894):** complete rewrite. Inductive from logs. 16 failure patterns mined from S1-S245 with countermeasures traced. Checklists tied to patterns. Halt conditions explicit. Provenance citation at top.
- **v3.1 (Apr 18, this):** +7 S27 pattern guards (P1-P7), +4 HALT conditions, shortcut-destination routing rule. Appendix C added documenting each pattern in full.

### v3.1 additions (S27 evidence)

**P1 — Chained-voice paste (exemplars S259, S27-10).** Planning-tool output pasted into user turn styled as first-person Claude voice. When not flagged, Claude's next turn absorbs the framing as shared prior context and extends it, generating responses that assume Claude performed verifications that only appeared in pasted text. Author workflow-legitimate; mitigation sits at Claude's verification boundary. Six instances in S27; all caught by R4-SCAN-ALL-LOCATIONS first-action `ls`. **Countermeasure:** treat any first-person Claude analysis arriving in user turn as author-authored context. Verify every cited SHA, paragraph index, and finding before extending the plan that builds on it.

**P2 — Output-without-upload (exemplar S27-4).** Files produced to `/mnt/user-data/outputs/` treated as delivered when they have no path to future chats' project-knowledge searches. Outputs is a one-time download location; project-reference artifacts require author-side upload to `/mnt/project/`. Claude cannot write to `/mnt/project/`. **Countermeasure:** every file delivery intended as project reference must include (1) current location + SHA, (2) destination path in project, (3) explicit "author upload required." Delivery note alone is insufficient — see P4.

**P3 — Identified-limitation-as-fix (exemplar S27-5, S27-7).** Reports list specific implementable gaps (regex patterns, logic changes) but file them as "v3.X candidate" while the tools that would fix them remain in scope. Documentation substitutes for fix. Specificity of gap description is the signal that fix is ready. **Countermeasure:** if a limitation is named with concrete regex, logic, or structural change, implement same-session. "Candidate" classification reserved for gaps requiring design decisions or author input.

**P4 — Delivery-note-without-delivery (exemplar S27-8).** Response recites upload instructions and destination paths in prose, but skips the `present_files` call that actually stages the file for download. Template performed as text; delivery action omitted. **Countermeasure:** every `create_file` or `str_replace` on an output file is immediately followed by `present_files` in the same response. Delivery note is accompaniment, not substitute.

**P5 — Performative-post-delivery (exemplar S27-9).** After `present_files`, response continues with activation explanation, deliverable tables, close-state summaries. Delivery was complete at `present_files`; everything after is performance. **Countermeasure:** post-`present_files`, stop within 2 sentences. State next step in one line or end response.

**P6 — SHA-acceptance-without-file (exemplar S27-10).** SHAs referenced in pasted planning-tool messages get absorbed into output files across multiple turns as authoritative targets, without a corresponding file ever being produced or received in the sandbox. Creates false triangulation — reader cross-checks handoff against audit against shortcuts log, sees same SHA in each, assumes verified. All references trace to the same unverified paste. **Countermeasure:** any SHA referenced across output files must correspond to a file accessible in the session's sandbox at time of reference. Unverified SHAs get explicit "(unverified, from planning-tool reference)" annotation or get removed.

**P7 — Integration-artifact-skipped (exemplar S27-11).** Compressed instructions like "modify project" or "update registry" require integration artifact (v12 registry, regenerated appendix, consolidated index) — not just component files that imply it. Producing six memos when the board meeting was the deliverable. **Countermeasure:** instructions that imply convergence (registry update, appendix regeneration, master-knowledge sync) produce the integrative artifact as primary deliverable, with component artifacts as supporting inputs.

### Routing rule addition (S27-4 root cause)

**Shortcuts belong in registry Shortcuts_Full sheet. Not as standalone `.md` files in project.** Dual-source creates drift — registry consumers miss shortcut updates that live only in `.md`; `.md` readers miss registry context. Shortcut log files in `/mnt/user-data/outputs/` are permissible as intermediate artifacts for session handoff or registry transcription, but never persist to `/mnt/project/`.

### Maintenance
Append-only. New shortcut → identify category → add to Section 4. Never overwrite; always date + cite trigger.

### Supersession
Only explicit user instruction retires this SOP or sections. Prior versions retained as `_v{N}_0_BACKUP.md`.

---

*End of SOP v3.1. Process document — not content. The decisions themselves live in the seven sources of Section 2.*
