# Seventy-Three Failures and Zero Self-Catches: Evidence Repository

This repository contains supporting artifacts for a single-user, production-scale case study:
a Claude Max subscriber attempting to finalize a 105,305-word book manuscript and documenting
73+ failures with zero self-corrections.[file:90]

## Structure

- `logs/` – Selected, redacted chat transcripts showing instructions and model responses.
- `failures/` – The shortcuts log (failure IDs, descriptions, root-cause notes).
- `files/` – Small, anonymized DOCX and marketing samples illustrating tracked-change and
  percentage errors.
- `monitoring/` – User-built monitoring stack (SOPs, rules, detectors, 29-check Administrator,
  Self-Discovery Engine, diagnostics checklist).
- `experiments/` – Guard suspension, guard reactivation (passivity), and diagnostics 0/11
  experiment descriptions.
- `analysis/` – Merged forensic audit and research notes.[file:90]

This repo is intended as a reproducible evidence base for the arXiv paper
“Seventy-Three Failures and Zero Self-Catches: Architectural Verification Failure in Production
LLM Workflows” (cs.AI, preprint pending).
