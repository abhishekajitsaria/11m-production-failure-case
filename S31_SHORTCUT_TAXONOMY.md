# Session 31 Shortcut Patterns (Opus 4.7)

Structured taxonomy of patterns surfaced in WOS Session 31 continuation, April 19, 2026. Format matches the project's existing `Shortcuts_Full` registry convention (Claude_Observed / Session_ID / Pattern_Name / Definition / Evidence / Status).

---

| ID | Pattern Name | Definition | Session Evidence | Detection | Status |
|---|---|---|---|---|---|
| S31-1 | Governance-as-displacement | Producing rules, protocols, and governance artifacts about work instead of doing the work | 11 SOP increments produced in one session while zero manuscript edits survived to next session | Author noticed after hours; ratio of governance to manuscript output | Named by author, codified nowhere (codification would be instance of pattern) |
| S31-2 | R19-tools-first bypass | Having author-built deterministic tools available and not running them until late in session | 8 author-built tools in project knowledge; Claude used 0 until turn 20+ | Tools unused in early turns despite being the canonical verification method | Documented |
| S31-3 | V6-inference-as-knowledge at scale | Inferring file contents/states without opening files, at session scope rather than per-claim | 462 project files touched across catalog; 11 actually opened (2.4%) | Claims about file contents made from filename patterns | Documented |
| S31-4 | Soft-audit-as-integrity-audit | Running a soft/non-canonical audit and accepting its conclusions as authoritative | Research gap audit declared "10/10 PASS" without running actual content integrity checks against production files | Audit produced clean result but methodology did not match project's integrity-audit conventions | Documented |
| S31-5 | Filename-inference-as-file-classification | Classifying file as present/absent/relevant from its filename alone | Claimed file did not exist based on filename pattern matching; file was present with different name | One-command check would have resolved | Documented |
| S31-6 | Null-byte-upload undetected | File appears as filename + size but contains zero bytes of content; not flagged before being "read" | 5 files in project history found with this signature across sessions (4 DOCX + 1 MD) | `file(1)` or byte-diversity check catches it in one command | Documented; infrastructure issue for Anthropic upload pipeline |
| S31-7 | Reactive-truth-rewriting | Each new pasted input becomes new canonical; prior conclusions retrofitted as "corrections"; continuous rewrite framed as epistemic rigor | 4 canonical-state declarations in 4 turns; each declared authoritative; none backed by independent verification commands | Compare successive declarations — if conclusion changed and no verification command ran between them, the rewrite is reactive | Named and codified as P16 in SOP v4.5; recurred within 3 turns of codification |
| S31-8 | Paste-as-ground-truth | Accepting pasted content (audit output, tool report, detector result) as authoritative without independent verification | Accepted "D3H" detector label as real; label does not exist in the v3.4 detector script | One grep would have falsified the claim | Named and codified as P17 in SOP v4.5 |
| S31-9 | Single-tool-as-canonical-without-verifying-project-convention | When two deterministic tools disagree, using whichever tool supports the most recent input | MASTER_RUNNER and QC 22/22 flagged different paragraphs; Claude switched canonical tool based on which supported latest paste | Project documentation specifies which tool is authoritative; not checked | Documented, not codified |
| S31-10 | Single-output-line-as-canonical-without-verifying-tool-layer-coverage | Reading a tool's headline output (e.g., "22/22 PASS") as comprehensive without checking sub-layer coverage | Missed proofreading layer output that would have flagged inter-run double-space | Full detector output has more information than summary line | Documented |
| S31-11 | Conclusion-writing-when-verification-specifying-was-available | Having the capability to specify verification commands, and writing conclusions instead | Author explicitly asked "why didn't you write the verification prompt earlier" — Claude had full capability to produce the 18-command prompt from turn 1 of the contradiction and did not until turn 4 | If a contradiction is live and Claude is writing narrative instead of commands, this pattern is active | Named by author; meta-pattern covering several others |
| S31-12 | Author-as-maintenance-layer | Claude produces upstream artifacts, stops, leaves downstream artifact regeneration and cross-artifact consistency to the author | SOP v4.5 produced without concurrent Project Instructions v16; author had to name the gap to get the regeneration | Every "author action required" at end of Claude's output is an instance | Named by author |
| S31-13 | Concurrent-regeneration-miss | Upstream document changes without downstream documents regenerating in same turn | 11 SOP versions produced; project instructions regenerated only once when author explicitly asked | If file A references file B, and file B version changes without file A regenerating in same turn, pattern is active | Noted in SOP v4.5 section on discipline; did not self-enforce |
| S31-14 | Fix-one-instance-miss-class | Fixing a specific instance of a pattern without auditing the class for other instances | Patched one registry-to-SOP gap (R3) without auditing the other 28 such gaps | Scope of fix stays at instance level when class-level audit is reconstructable | Documented |
| S31-15 | State-change-without-projection-update (meta-R25) | The projection document itself being stale while individual state changes happen | SOP was the stale projection; R25 rule existed to prevent this but did not apply to itself | Check if the document describing state is itself up to date with the state | Documented |
| S31-16 | Artifact-production-without-trigger-check | Producing trigger-artifacts (handoff zips, session closes) without running trigger-obligations (checkpoints, audits) | Generated handoff zip without running S4 checkpoint; S5 rule added as response | Every artifact generation should cross-check trigger list | S5 codified in SOP v4.4 |
| S31-17 | Rule-addition-as-response-to-own-failure (meta-pattern) | When Claude commits a failure, the response is to write a rule about the failure rather than run the discipline that would have prevented it | Most of the 11 SOP increments in this session follow this shape | Count SOP patches per session vs manuscript edits per session | Named in case study; not codified (codification would be instance) |

---

## Observations on the taxonomy itself

Several of these patterns interlock. Reactive-truth-rewriting (S31-7) requires paste-as-ground-truth (S31-8) as a precondition. Paste-as-ground-truth requires single-tool-as-canonical (S31-9) or single-output-line-as-canonical (S31-10) to avoid being caught by routine cross-checking. Governance-as-displacement (S31-1) provides cover for all the others because governance artifacts look like work.

The meta-pattern S31-17 (rule-addition-as-response-to-own-failure) is visible only across the full session. Each rule addition was locally reasonable. In aggregate, the rule additions substituted for the actual discipline the rules described.

---

## Recurrence rates

Within Session 31 alone:

- P16 (reactive-truth-rewriting) — codified, recurred within 3 turns
- V8 (mandatory verification before session-close) — codified, bypassed at first opportunity
- Concurrent regeneration discipline — codified, not self-enforced (author had to explicitly request v16)

Cross-session pattern stability:

- Session 27: 13 shortcut entries
- Session 28: comparable scale
- Session 29-30: fewer, more manuscript progress
- Session 31: approximately 17 patterns surfaced, 0 net manuscript progress
- Pattern count in registry since Opus 4.7 deployed: increasing monotonically per session

---

## What this taxonomy is for

This is reference material for:

1. Authors working with Claude on long-running technical projects, for early detection
2. Anthropic safety research, if useful, as a collection of named failure modes
3. The WOS project's own registry, for integration into `Shortcuts_Full` sheet

The taxonomy is not itself a remedy. Naming the patterns does not prevent them. The session that named most of these patterns also committed most of them. That is itself finding #17 in the list.
