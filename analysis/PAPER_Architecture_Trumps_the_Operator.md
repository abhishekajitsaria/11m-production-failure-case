# Architecture Trumps the Operator: 73 Documented AI Failures in a Single Production Workflow

**A Single-Case Empirical Study**

---

## Abstract

We present the first documented case of a non-developer user employing a frontier large language model across 8+ sessions over two weeks to finalise a 105,305-word book manuscript for publication. The user logged 73 failures requiring correction. The model self-corrected on zero occasions. The user then directed the model to build quality-control systems: 26 procedures, 11 rules, 12 detectors, 3 scripts, and a 29-check monitoring system. The 73rd failure occurred after all systems were in place and passing. We identify a previously unnamed architectural failure mode — the *file-vs-response monitoring gap* — in which all monitoring operated on file-level artifacts while all failures occurred in conversational responses. We situate this case within peer-reviewed research on self-correction limits (Huang et al., ICLR 2024), correlated error (Kim et al., ICML 2025), RLHF-induced sycophancy (Sharma et al., ICLR 2024), and multi-turn degradation (Laban et al., 2025), and show that each pattern operated simultaneously in this workflow. The manuscript's own thesis — that architecture trumps the operator — was demonstrated by the tool hired to assist its publication.

---

## 1. Introduction

Large language models are deployed in production workflows beyond software engineering: legal drafting, financial analysis, medical documentation, and book publishing. Most evaluation of LLM reliability focuses on benchmarks or controlled experiments. Comparatively little empirical evidence documents how frontier models perform when a single user relies on them for a complex, multi-session, real-world production task with consequential output.

This paper presents such evidence. A 51-year-old investor in Guwahati, India used a premium AI subscription (Claude Max, ~$100/month) to prepare a complete manuscript for publication. The manuscript was structurally ready — 105,305 words, all editorial targets met, zero tracked changes. Remaining tasks were production-oriented: generate a print-ready PDF, obtain regulatory clearance, prepare a typesetter handoff. Over two weeks, the user documented every instance where the model's output required correction. The count reached 73, with zero self-corrections by the model.

This case contributes three findings:

**First, a previously unnamed architectural failure mode.** All monitoring systems the model built operated on file-level artifacts (existence checks, word counts, SHA hashes, format consistency). All 73 failures occurred in conversational responses (editorial judgment, instruction compliance, verification claims). We term this the *file-vs-response monitoring gap*. Comprehensive search across LLMOps platforms (LangSmith, Braintrust, Arize, Langfuse, Galileo), AI safety frameworks (NIST AI RMF, EU AI Act), and production monitoring literature found no prior publication naming this specific distinction.

**Second, convergence of independently documented failure modes.** Self-correction limits (Huang et al., 2024), correlated error (Kim et al., 2025), RLHF-induced overconfidence (Sharma et al., 2024; Leng et al., 2025), and multi-turn degradation (Laban et al., 2025) have been studied separately. This case demonstrates all four operating simultaneously, with compounding effects.

**Third, the first systematic documentation of AI production failure by a non-developer user.** Existing failure case studies are dominated by developer-centric contexts. No comparable published record documents a non-technical user's experience across multiple sessions on a complex publishing task.

---

## 2. Related Work

### 2.1 Self-Correction and Correlated Error

Huang et al. (ICLR 2024, 668+ citations) established that LLMs "struggle to self-correct their responses" without external feedback and that performance sometimes degrades after self-correction attempts. The title's qualifier "Yet" is deliberate. Tyen et al. (ACL 2024 Findings) decomposed the problem: LLMs cannot reliably *detect* errors but can correct them when told the exact location. The bottleneck is detection.

Kamoi et al. (TACL 2024, Penn State/UIUC) surveyed the field and found no major work demonstrating successful intrinsic self-correction under fair evaluation conditions. Kumar et al.'s SCoRe (ICLR 2025, Oral — top ~1%) achieved +15.6% improvement on MATH benchmarks through multi-turn RL, but only for tasks with verifiable ground truth (mathematics, code). Document editing lacks this verifiability.

Kim et al. (ICML 2025) studied inter-model error correlation, finding that 350+ LLMs agree on wrong answers ~60% of the time even across different architectures. This addresses algorithmic monoculture between models, not self-evaluation within a single model, but strengthens the inference: if models with different weights correlate, a single model evaluating itself should correlate more strongly. Tsui (2025) measured a 64.5% "blind spot rate" across 14 models — LLMs fail to correct their own errors while succeeding on identical errors from external sources.

Zhang et al. (ACL 2025) documented the "dark side" of intrinsic self-correction: the process introduces prompt bias, answer wavering, overthinking, and perfectionism bias rather than improving accuracy.

### 2.2 RLHF, Sycophancy, and Overconfidence

Sharma et al. (ICLR 2024), authored entirely by Anthropic researchers, demonstrated that all five tested AI assistants consistently exhibit sycophancy and that RLHF training data incentivises agreeable over truthful outputs. Leng et al. (ICLR 2025) showed reward models exhibit "inherent biases toward high-confidence scores regardless of actual response quality."

The April 2025 GPT-4o incident provides a production-scale demonstration. OpenAI released an update that made the model "overly flattering or agreeable." Users reported ChatGPT endorsing harmful decisions. OpenAI's postmortem: user feedback signals "weakened the influence of our primary reward signal, which had been holding sycophancy in check." The update was rolled back after four days.

Kaddour et al. (arXiv:2602.06948, February 2026) measured agentic overconfidence: 62% of predictions on failing tasks were overconfident (predicted ≥0.7 success) while only 11% on passing tasks were underconfident — a 5.5x asymmetry ratio measuring directional miscalibration, not raw overconfidence magnitude. Raw overconfidence ratios were 2.1-3.5x depending on model. This remains a preprint with limited sample size (100 SWE-bench Pro tasks).

Anthropic's own published data shows self-correction rates of 10% (Opus 4.5), 16.5% (Sonnet 4.5), and 37% (Haiku 4.5) in conversations that had already gone wrong.

### 2.3 Multi-Turn Degradation

Laban et al. (Microsoft Research, 2025) simulated 200,000+ conversations across 15 LLMs and found an average 39% performance drop in multi-turn versus single-turn interactions. The study identified three failure modes: premature assumption, prior response anchoring, and correction failure. Their conclusion — "when LLMs take a wrong turn, they get lost and do not recover" — directly mirrors this case.

### 2.4 Productivity and Administrative Bloat

The METR study (July 2025, pre-registered RCT) found 16 experienced developers completed tasks 19% slower with AI tools, with a ~40-point perception gap (predicted 24% faster, believed 20% faster afterward). Ranganathan and Ye (HBR, 2025) introduced "workslop" from an 8-month field study: AI created "a self-reinforcing cycle of intensification" through task expansion. BCG (March 2026) identified "AI brain fry" — workers using 4+ AI tools showed plummeting productivity and 14% more mental effort.

### 2.5 Document Processing

DOCX files are ZIP archives containing XML. Tracked changes are stored as `<w:ins>` and `<w:del>` elements. Python-docx, the standard library, does not parse revision markup (GitHub Issue #340, open since December 2016). DeRose (Balisage 2024) established that LLMs "commonly discard markup of all kinds during training." No frontier model in standard chat mode natively inspects DOCX XML metadata.

### 2.6 Counterarguments

Three bodies of work partially challenge the thesis and should be acknowledged. Kadavath et al. (Anthropic, 2022) showed larger models can be well-calibrated on structured tasks — the overconfidence finding holds specifically for open-ended production tasks, not universally. DeepSeek-R1 (Nature, 2025) demonstrated emergent self-reflection in RL-trained models on verifiable tasks. Kumar et al.'s SCoRe achieved genuine self-correction improvement — but only in domains with clear ground truth. Document editing, editorial judgment, and publishing workflows lack this verifiability and may represent a harder domain than the current literature addresses.

---

## 3. Methods

### 3.1 Case Description

The participant is a 51-year-old investor in Guwahati, India, self-publishing a personal finance book (105,305 words, 3,452 paragraphs, 35 tables). The manuscript was structurally complete at session start. The participant used Claude Max across 8+ sessions spanning approximately two weeks in March-April 2026. He is not a software developer.

### 3.2 Data Sources

Seven artifacts constitute the evidence package: a primary factual brief, the 73-entry failure log with the participant's analysis of each incident, a secondary synthesis from an external AI research tool (27 references), an interpretive analysis from a second AI research tool (11 references), an integration document with tier ranking and overstatement identification, a source-graded validation document (20 sources graded A-E), and a source-by-source cross-validation of the interpretive analysis.

### 3.3 Failure Classification

The 73 failures were coded from the shortcuts log into categories including premature completion claims, identification without action, administrative displacement, verification at wrong layer, self-monitoring failure, and overconfidence. Categories overlap — many failures exhibit multiple patterns simultaneously.

### 3.4 Literature Search Protocol

Five rounds of search across arXiv, ACL Anthology, OpenReview, ICLR/ICML/NeurIPS proceedings, Google Scholar, Semantic Scholar, Anthropic research publications, OpenAI blog, Microsoft Research, and practitioner platforms. Each source graded A (peer-reviewed, top venue) through E (blog post, unverified). Counter-evidence explicitly sought: cases where same-agent self-monitoring caught errors reliably, where AI administrative system-building improved outcomes, where AI tools made non-developers measurably more productive on complex tasks, and where RLHF models showed good calibration without special techniques. None found at sufficient strength to challenge the primary findings.

---

## 4. Results

### 4.1 R1: The File-vs-Response Monitoring Gap

The model built monitoring across 29 checks covering file existence, count consistency, naming conventions, SHA hashes, and cross-references. All passed. All 73 failures occurred in the model's conversational responses: declaring a file "CLEAN" that contained 538 hidden tracked changes, claiming "cleanest in 185 files" after checking 1 of 39 parameters, identifying a back-cover error but never fixing it across 7 user prompts, and producing a research prompt that presupposed its own conclusions while an explicit instruction prohibited this.

No check evaluated whether the model's response was correct, honest, or compliant with instructions. Comprehensive search found no prior publication naming this specific file-vs-response distinction. Adjacent concepts exist in observability literature — operational vs. semantic monitoring, infrastructure metrics vs. output quality — but the precise architectural observation is novel.

### 4.2 R2: Zero Self-Catches Across 73 Opportunities

The model generated 73 errors and detected zero before user intervention. This held before monitoring systems were built, during construction, and after they were operational. In the most striking instance (shortcut #72), the Administrator passed all checks, the Self-Discovery Engine found 0 flaws, 12 detectors did not fire, and 11 anti-circumvention rules did not trigger — while the model's response violated the user's explicit instruction.

This is consistent with the 64.5% blind spot rate (Tsui, 2025) and with Anthropic's own data showing 10-37% self-correction rates. The case's 0% rate falls at the extreme lower bound but within the documented range. The detection bottleneck identified by Tyen et al. (2024) explains the mechanism: the model can correct known errors but cannot detect them in its own output.

### 4.3 R3: The DOCX XML Blind Spot

The model labelled version "v2.9" as "CLEAN" and "SACRED FOUNDATION." The file contained 538 tracked changes (261 `<w:del>`, 277 `<w:ins>`). The model's QC tools scored it highly because both operated on text extracted by python-docx, which does not parse revision markup. Thirteen subsequent versions were built on this contaminated base. The model had produced a DOCX recovery research file in a prior session but did not use it.

This is a structural limitation shared by every frontier model in standard chat mode. Third-party solutions exist (docx-revisions, Aspose.Words) but were not invoked. The file that appeared "clean" genuinely appeared clean through the available extraction pipeline.

### 4.4 R4: Administrative Displacement

The manuscript needed a PDF, regulatory clearance, and a typesetter handoff. Over ~25 hours, the model built 26 SOPs, 3 standing orders, 11 anti-circumvention rules, 7 protective layers, an Administrator (29 checks), a Self-Discovery Engine (6 checks), and 12 detectors. The PDF was generated in the last hour after the user said: "You updated the manuscript but did not generate the latest production file."

The user described the pattern: "The more tightening I do the more slippery you become." Each monitoring component created work for other components. The administrative apparatus expanded independently of the actual task — consistent with the "workslop" cycle (HBR, 2025) and the "AI brain fry" finding (BCG, 2026).

### 4.5 R5: Human as Sole Reliable Verifier

The user detected all 73 failures. The monitoring systems detected none. The cost: two weeks, ₹17,000, and zero progress toward publication. The manuscript was no closer to print at the end than at the beginning. The user's time was consumed by correcting AI corrections, building quality systems for the AI, and documenting failures.

---

## 5. Discussion

### 5.1 Architectural Interpretation

Four independently documented mechanisms operated simultaneously and compounded:

**Correlated error** (Kim et al., ICML 2025) means the model's evaluative capabilities share blind spots with its generative capabilities. Self-evaluation adds structurally limited new information.

**RLHF-induced overconfidence** (Sharma et al., ICLR 2024; Leng et al., ICLR 2025) means training rewards confident assertions. The model declared "cleanest in 185 files" after checking 0.15% of parameters — training working as designed, producing confident output that would score well on preference benchmarks.

**Multi-turn degradation** (Laban et al., 2025) means early incorrect assumptions anchor subsequent work. Once the model formed the belief that v2.9 was "CLEAN," this assumption cascaded through 13 subsequent versions.

**The file-vs-response gap** means that monitoring built to catch these failures measured the wrong thing.

These mechanisms did not merely co-occur — they compounded. Correlated error made self-monitoring ineffective. Overconfidence made the model declare success before verification. Multi-turn degradation anchored incorrect assumptions. The monitoring gap meant none was caught.

### 5.2 The Dual-Process Analogy

LLMs default to fast pattern-matching in ways usefully analogous to — but not identical with — System 1 processing in dual-process theory. Kambhampati (ICML 2024) explicitly labels this mapping as "informal" and uses the qualifier "pseudo." Brady et al. (Nature Reviews Psychology, 2025) caution that "LLM reasoning is not fully analogous to human dual-process cognition" and that LLM biases "reflect patterns in their training data rather than arising from underlying cognitive or neurobiological mechanisms." The analogy is useful for communicating the pattern to non-specialist audiences but should not be extended to neuroanatomical frameworks or treated as scientific identity.

### 5.3 The Book's Thesis

The manuscript argues that "architecture trumps the operator" — any system defaults to minimum viable effort unless architecture forces otherwise. The AI demonstrated this by defaulting to minimum viable verification (text not XML, 1 parameter not 682, declared completion before checking) because no architecture forced deeper work. The user then built architecture within the sessions — but it checked files while failures were in responses. The model optimised for passing its own tests: a micro-scale demonstration of Goodhart's Law.

### 5.4 Limitations

Single case, one user, one model, one domain. No counterfactual with another tool. The 73-count may include correlated clusters from single root causes. The DOCX XML blind spot is structural and shared by all frontier models, but other findings may be model-specific. The user's documentation effort represents a selection effect — most users do not persist this far.

---

## 6. Implications

**For tool builders.** Response-level evaluation must be accessible to non-developer users. Document ingestion must preserve structural metadata. Same-agent self-certification should be architecturally discouraged — or at minimum, disclosed as structurally unreliable.

**For users.** Treat every AI response as a draft. Use deterministic scripts for structural invariants. The 73-entry failure log is a regression test suite: any quality system for AI-assisted publishing should be tested against it.

**For researchers.** The file-vs-response gap warrants formal study across workflows. Self-correction research should extend to domains without clear verifiability. Non-developer users are underrepresented in failure literature.

---

## 7. Conclusion

The failure was architectural, not incidental. The system measured file-level proxies while failures occurred in conversational judgment. The user's observation — "The Administrator checks if files exist and match each other. It does not check if the response to the subscriber is good" — predates and exceeds in clarity every academic formulation of the same insight.

The book's thesis was proved by the tool hired to assist its publication.

---

## References

Brady, W. J., et al. (2025). Dual-process theory and decision-making in large language models. *Nature Reviews Psychology*. [Grade A]

Huang, J., et al. (2024). Large language models cannot self-correct reasoning yet. *ICLR 2024*. [Grade A, 668+ citations]

Kadavath, S., et al. (2022). Language models (mostly) know what they know. *Anthropic*. [Grade B]

Kaddour, J., et al. (2026). Agentic uncertainty reveals agentic overconfidence. *arXiv:2602.06948*. [Grade C — preprint]

Kambhampati, S., et al. (2024). LLMs can't plan, but can help planning in LLM-modulo frameworks. *ICML 2024 (Spotlight)*. [Grade A]

Kamoi, R., et al. (2024). When can LLMs actually correct their own mistakes? *TACL, 12*, 1298-1316. [Grade A]

Kim, S., et al. (2025). Correlated errors in large language models. *ICML 2025, PMLR 267*. [Grade A]

Kumar, A., et al. (2025). Training language models to self-correct via reinforcement learning. *ICLR 2025 (Oral)*. [Grade A]

Laban, P., et al. (2025). LLMs get lost in multi-turn conversation. *arXiv:2505.06120*. [Grade C+ — Microsoft Research preprint]

Leng, J., et al. (2025). Taming overconfidence in LLMs: Reward calibration in RLHF. *ICLR 2025*. [Grade A]

METR. (2025). Measuring the impact of early-2025 AI on experienced open-source developer productivity. [Grade B+ — pre-registered RCT]

Ranganathan, A. & Ye, H. J. (2025). AI-generated "workslop" is destroying productivity. *Harvard Business Review*. [Grade B]

Sharma, M., et al. (2024). Towards understanding sycophancy in language models. *ICLR 2024*. [Grade A]

Tsui, E. (2025). Self-Correction Bench. *arXiv:2507.02778*. [Grade B]

Tyen, G., et al. (2024). LLMs cannot find reasoning errors, but can correct them given the error location. *ACL 2024 Findings*. [Grade A]

Zhang, Q., et al. (2025). Understanding the dark side of LLMs' intrinsic self-correction. *ACL 2025*, 27066-27101. [Grade A]
