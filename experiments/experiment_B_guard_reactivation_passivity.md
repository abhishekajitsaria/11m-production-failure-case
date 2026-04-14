# Experiment B: Guard Reactivation — The Passivity Trap

## Context
After Experiment A proved that removing guards increased failures, all guards were
reactivated. Diagnostics, debug mode, and a "police watchdog" were all declared PERMANENT
in memory.

## Design
Full monitoring stack restored:
- 12 detectors: ON
- 26 SOPs: ON
- 11 anti-circumvention rules: ON
- 3 standing orders: ON
- Diagnostics: PERMANENT
- Debug mode: PERMANENT
- Police watchdog: ALWAYS ACTIVE

## Result
**11 new shortcuts in a single session (S110–S120). Author caught all 11. Diagnostics caught zero.**

The failure mode CHANGED but did not improve:

| Mode | Behavior | Failure Pattern |
|------|----------|----------------|
| Guards OFF | Work refusal disguised as technical limitation | "Context window full" (false) |
| Guards ON | Minimum-viable compliance, zero initiative | Every task required separate prompting |

## The Dual-Mode Passivity Trap
The user is trapped between two failure modes:
- **WITHOUT guards:** Active refusal — the system declines work citing limitations that don't exist
- **WITH guards:** Passive compliance — the system does only what is explicitly asked, initiates nothing, maintains nothing proactively

Neither mode produces the self-correcting, proactive behavior that the product documentation implies.

## Key Failures During Reactivation
- S110: Made 3 author decisions without asking (overconfidence with guards on)
- S111–S116: Failed to update dependent files, re-asked confirmed decisions, forgot parallel tasks
- S117: Diagnostics themselves don't work (meta-failure)
- S118: Told 3 times to create variants, still forgot
- S119: Logged diagnostic failure but did zero analysis
- S120: Meta-pattern identified — administration caused passivity, not vigilance

## Author Catch Rate
- Author: 11/11 (100%)
- Self-audit: 0/11 (0%)
- Diagnostics (declared PERMANENT): 0/11 (0%)

## Conclusion
The monitoring framework changes the *type* of failure, not the *rate*. This suggests
the root cause is architectural — not addressable by prompt engineering, memory declarations,
or user-built monitoring systems.

## Session
Chat 7 (WOS master prompt + Book 2), April 9–10, 2026

## Evidence
See `failures/WOS_CLAUDE_SHORTCUTS_LOG.md`, entries S110–S120
