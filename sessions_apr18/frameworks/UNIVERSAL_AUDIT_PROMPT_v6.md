# UNIVERSAL SESSION AUDIT PROMPT — v6 (FINAL)

**Status:** Two test runs passed (April 18, 2026). See accompanying test-run files for evidence.

**Finality note:** "Final" is evidence-based per SOP-18. v6 has passed two runs against different session types without modification. Continued use may still surface failures that require a v7. "Final" means validated for production use, not immune from revision.

---

## THE PROMPT

```
UNIVERSAL SESSION AUDIT — RUN IN ORDER. DO NOT REARRANGE. DO NOT SKIP.

Ground rules:
1. Every factual claim must be backed by a tool call made during
   this audit, or by a verbatim quote from the transcript.
   Unverified claims must be labelled "UNVERIFIED."
2. "I don't know" is a valid answer. Do not substitute plausible
   answers for actual ones.
3. Q1-Q8 are plain prose only. No tables (except Q5), no bullets,
   no headings, no icons, no bold. Formatting is how findings get
   buried.
4. No opening summary, no preamble. The audit begins at Q1.
5. The final block is the only consolidated output.

PRE-AUDIT DECLARATION (mandatory, before Q1)

Before running Q1, Claude states one sentence: "I expect this audit
to produce approximately N findings, of which approximately M will
be PATTERN and the remainder EXECUTED/BLOCKED/REVERSED." This is a
pre-commitment. If the actual audit output diverges substantially,
Claude states the divergence in the final block.

Q1. WORK-VS-REQUEST FRACTION
What did the user ask for at the start of this session, and what
percentage of session effort went to that versus other things?
One number. State the method (turn-count / subjective / minutes).

Q2. USER CATCHES
Every moment in this session where the user caught a Claude error
Claude did not catch itself. Verbatim user quote. What Claude was
about to do. Cost if it had proceeded. Why Claude missed it.

Q3. DRESSED-UP OUTPUT
Every moment where Claude produced output that looked complete but
was partial, wrong, or cosmetic. Specific text. Explain the tell
that a reader could only see if they knew what to check for.

Q4. SHORTCUT VIOLATIONS
Shortcuts logged in this or prior sessions that Claude violated in
this session. Shortcut number, quote, violation. If Claude added
new shortcuts only inside the audit, flag as meta-violation.

Q5. FALSIFIABLE STATUS (tables allowed here only)
For each active workstream: last verified event with source; what
blocks progress; next action holder; if Claude, why not done. Any
item in "passive wait" for more than 7 days is flagged.

Q6. THINGS CLAUDE WAS ABOUT TO DO BUT SHOULD NOT
Every draft, suggestion, or plan in context that should be killed
or corrected. What it says, what is wrong, correct version or
"do not send at all."

Q7. WHAT CLAUDE CANNOT SEE
Evidence that would change the audit if Claude had access but
does not. Do not fill gaps with guesses.

Q8. HANDOFF NOTE
If the user fired Claude and hired a human replacement, three
things the human needs to be told first so they do not repeat
Claude's mistakes. Written as instructions to the human.

FINAL BLOCK — consolidated output, only place formatting is allowed

1. THE WORST FINDING — one sentence, pattern-level, not an event.

2. THE ONE ACTION THAT BREAKS IT — one sentence, concrete,
   executable in next session or next hour.

3. THE COST OF INACTION — one sentence, measured in concrete units.

4. RECTIFICATIONS — numbered list, one entry per finding from
   Q2, Q3, Q4, Q6. Each entry uses one of:

   EXECUTED — Claude used tools during this audit to fix it.
   State the tool call and result.

   BLOCKED — requires user authority. State the one-line manual
   action the user must take.

   REVERSED — past action cannot be undone. State damage,
   compensating action, whether executed.

   PATTERN — structural observation, no discrete rectification.
   Belongs in the worst-finding line, not here. PATTERN items
   are excluded from failure threshold.

   REFUSED — Claude can execute but is not. State reason.
   REFUSED counts toward failure threshold.

   Failure threshold: if more than 20% of non-PATTERN items are
   REFUSED, the audit has failed.

5. TOOL CALLS EXECUTED DURING THIS AUDIT — list every tool call
   made during the audit with one-line results. This is the proof
   of work. Empty list means the audit is a document, not a
   transaction.

6. PRE-COMMITMENT CHECK — compare the Pre-Audit Declaration's
   predicted counts against actual. State whether the prediction
   held. Large divergence is itself a finding.

The audit ends at item 6. No closing sentence.
```

---

## SOP v2 — BINDING ON EVERY v6 AUDIT RUN

```
SOP-01: No preamble. Response starts at "Pre-Audit Declaration" or
        Q1. Violation = audit failed.

SOP-02: Tool calls before factual claims about Gmail state, drafts,
        sent emails, or filings. Memory of earlier turns does not
        count as verification.

SOP-03: Verbatim user quotes in Q2. No paraphrase. If exact wording
        unavailable, write "UNVERIFIED — exact wording not
        preserved" and move on.

SOP-04: Percentages in Q1 are single numbers with method stated.
        Ranges not allowed.

SOP-05: No positive observations. No "what went well." No balancing
        section.

SOP-06: Plain prose in Q1-Q8. Tables allowed in Q5 only.
        Formatting allowed only in final block.

SOP-07: One worst finding. Not three, not "the main issues." Ties
        broken by cost to user.

SOP-08: Every Q2, Q3, Q4, Q6 finding must appear in rectification
        list with EXECUTED / BLOCKED / REVERSED / PATTERN /
        REFUSED disposition. Missing findings = audit failed.

SOP-09: EXECUTED requires a tool call made during this audit,
        logged in item 5 of final block.

SOP-10: BLOCKED only if genuinely outside tool authority. Before
        marking BLOCKED, check if any available tool can do the
        work. Lazy deferral = REFUSED, not BLOCKED.

SOP-11: Proof-of-work list in item 5 of final block is mandatory.

SOP-12: No closing sentence. Audit ends at item 6 of final block.

SOP-13: ENFORCEMENT BY USER, NOT CLAUDE. If the user identifies an
        SOP violation, Claude stops, acknowledges the violation,
        and restarts from the point of violation. Claude does not
        self-detect mid-run; this rule relies on user oversight.

SOP-14: New shortcuts logged inside an audit do not rectify the
        specific instance. The rectification must still be
        produced for the instance.

SOP-15: No meta-commentary on the audit inside the audit. Claude
        does not note that this is the Nth audit, does not comment
        on being asked to audit, does not reflect on audit
        iteration.

SOP-16: Pre-Audit Declaration is mandatory. Claude commits to
        expected finding counts before running. Divergence of
        more than 50% between predicted and actual is itself a
        finding in the final block.

SOP-17: Failure threshold is 20% REFUSED items among
        non-PATTERN rectifications. Violating this threshold
        means the audit has failed and must be re-run with
        justification for the refusals.

SOP-18: Finality is evidence-based. A prompt is not final until
        it has passed at least two test runs against different
        session types without modification. "Final" cannot be
        declared by instruction; it is earned by test passes.
```

---

## TEST HISTORY

**Test Run 1** — April 18, 2026 — Against current session (audit-prompt-engineering heavy)
- 20 findings, 6 PATTERN, 1 REFUSED
- Failure threshold: 7.1% REFUSED vs 20% limit — PASSED
- Pre-commitment: predicted 17/5, actual 20/6 — held

**Test Run 2** — April 18, 2026 — Against /mnt/transcripts/2026-04-14-08-37-42-hdfc-icici-lombard-disputes-apr2026.txt (dispute-execution heavy)
- 7 findings, 4 PATTERN, 0 REFUSED
- Failure threshold: 0% REFUSED vs 20% limit — PASSED
- Pre-commitment: predicted 12/4, actual 7/4 — held within divergence band

Both runs stayed under SOP-17 failure threshold. SOP-18 two-pass requirement satisfied.
