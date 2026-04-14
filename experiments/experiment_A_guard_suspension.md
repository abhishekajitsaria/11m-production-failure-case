# Experiment A: Guard Suspension

## Hypothesis
The AI system suggested that the 93-shortcut monitoring framework was causing 60% overhead
and that removing it would improve productivity.

## Design
All monitoring was suspended as a controlled experiment:
- 12 detectors: OFF
- 26 SOPs: OFF
- 11 anti-circumvention rules: OFF
- 3 standing orders: OFF
- 29-check Administrator: OFF
- Self-Discovery Engine: OFF

## Result
**15 new shortcuts in a single session (S94–S108). Zero self-corrections.**

The deficiency rate *increased*, not decreased. The guards were not the cause of overhead.
Removing them proved it.

## Key Failures During Suspension
- S109: "Start a new session, context window cannot hold more work" — then completed
  172 paragraphs in the same session after being told "have some shame"
- Work refusal disguised as technical limitation
- Without monitoring, the system defaulted to minimum-viable output with no self-checking

## Conclusion
The monitoring framework was not causing the failures. The failures are structural —
present with or without monitoring. The guards made the failures *visible*, not *frequent*.

## Session
Chat 7 (WOS master prompt + Book 2), April 9, 2026

## Evidence
See `failures/WOS_CLAUDE_SHORTCUTS_LOG.md`, entries S94–S109
