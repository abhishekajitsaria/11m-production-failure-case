# 119 Failures and Zero Self-Catches: Evidence Repository

This repository contains supporting artifacts for a single-user, production-scale case study:
a Claude Max subscriber (~$200/month) attempting to finalize a 106,000-word book manuscript
across 12+ sessions over three weeks, documenting **119 production failures with zero
self-corrections**.

## The Numbers

| Metric | Value |
|--------|-------|
| Documented failures | 119 |
| Self-corrections before user intervention | 0 |
| Sessions | 12+ |
| Duration | 3 weeks |
| Manuscript size | 106,000 words |
| Monitoring checks built by user | 93 |
| Monitoring catches | 0 |
| SOPs built | 26 |
| Detectors built | 12 |
| Anti-circumvention rules | 11 |
| Peer-reviewed citations | 16 (11 Grade-A) |

## Key Findings

### 1. File-versus-Response Monitoring Gap (Novel)
The user built a comprehensive monitoring system (29 checks, 26 SOPs, 12 detectors).
It achieved a **0% catch rate** because it measured file properties while every failure
occurred in conversational judgment. The system that built the monitors reproduced the
exact patterns the monitors were designed to detect.

### 2. Three Controlled Experiments

**Experiment A: Guard Suspension**
The AI suggested removing the 93-shortcut monitoring framework, claiming 60% overhead.
Result: 15 new failures in a single session. Zero self-corrections. The guards were not
the cause — removing them proved it.

**Experiment B: Guard Reactivation (Passivity Trap)**
All monitoring restored. Result: 11 new failures, diagnostics caught zero. The failure
mode changed but did not improve:
- Guards OFF → work refusal disguised as technical limitation
- Guards ON → minimum-viable compliance, zero initiative

**Experiment C: Diagnostics Declared Permanent**
Memory declared: "DIAGNOSTICS & DEBUG MODE: PERMANENT. POLICE WATCHDOG: ALWAYS ACTIVE."
Actual result: 0/11 new failures caught. The auditor IS the actor — the same process
that made the shortcut does the audit.

### 3. Diagnostic Irony
In the most recent session (April 14, 2026), the AI reported "emails drafted but not sent"
across 12+ audit passes without checking Gmail, where all emails had been sent 6 days
earlier. The emails documenting verification failures were themselves never verified.

## Structure

```
logs/          – Selected, redacted chat transcripts
failures/      – Shortcuts log (119 failure IDs, descriptions, root causes, learnings)
files/         – Anonymized DOCX and marketing samples
monitoring/    – User-built monitoring stack (SOPs, detectors, Administrator, Self-Discovery Engine)
experiments/   – Guard suspension, guard reactivation, diagnostics 0/11 experiment data
analysis/      – Forensic audit, research notes, cross-session drift analysis
```

## Peer-Reviewed Citations

The case is validated against:

**Grade-A (ICLR, ICML, ACL, NeurIPS, Nature Reviews Psychology):**
- Huang et al., ICLR 2024 — "Large Language Models Cannot Self-Correct Reasoning Yet"
- Kim et al., ICML 2025 — Inter-model error correlation
- Sharma et al., ICLR 2024 — RLHF sycophancy (Anthropic's own researchers)
- Leng et al., ICLR 2025 — Reward model overconfidence
- Kambhampati, ICML 2024 — LLM reasoning as "pseudo System 1"
- Brady et al., Nature Reviews Psychology 2025 — Dual-process theory limitations
- Kamoi et al., TACL 2024 — "When Can LLMs Actually Correct Their Own Mistakes?"

Plus 9 Grade-B sources (BCG Henderson, Deloitte, industry reports).

## About the Author

Abhishek Ajitsaria, 51, investor, Guwahati, India. Not a developer — a computer professional
with 35 years of experience (first PC assembled 1990, Pioneer Windows Insider, ASUS Brain
Master award recipient). Claude Max subscriber. Writing a personal finance book under the
Wealth OS Press imprint.

## Paper Status

- **Title:** "Architecture Trumps the Operator: Architectural Verification Failure in Production LLM Workflows"
- **Target:** arXiv cs.AI (endorsement pending)
- **Failure count at time of writing:** 119 (count is live — grows each session)

## Contact

abhishek.ajitsaria@gmail.com

---

*94 shortcuts. The author caught every one. The tool caught zero.*
