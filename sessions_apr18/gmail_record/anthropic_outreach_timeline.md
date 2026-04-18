# Anthropic Outreach Timeline

Record of correspondence attempts to Anthropic regarding the failures documented in this repository. Extracted from Gmail on 2026-04-18.

**Summary:** 9 emails sent across 11 days, via 3 channels (support@, feedback@, direct-to-founders). Response from human at Anthropic: **zero**. All received responses were either (a) Fin AI Agent auto-responses, (b) template classification replies, or (c) mail-delivery failures for invalid addresses.

This is itself a finding. The distribution mechanism for high-evidence user feedback to Anthropic appears to route all model-quality-related correspondence through the same auto-classifier, which replies with a best-practices template regardless of evidence volume or specificity.

---

## Complete outreach log

### Email 1 — 2026-04-07 10:43 UTC
**To:** feedback@anthropic.com
**Subject:** Claude Max Subscriber Feedback: 26 Documented Shortcuts Across a Production Book Project
**Payload:** 26 shortcut instances from first 7 production sessions
**Response:** Auto-reply from `feedback+noreply@anthropic.com`. Standard "your feedback has been logged" template. No human response.

### Email 2 — 2026-04-08 06:14 UTC
**To:** support@anthropic.com, cc: usersafety@anthropic.com
**Subject:** Claude Max Subscriber Feedback — 60 Documented AI Shortcuts Across 7 Sessions on a Book Manuscript Project
**Payload:** 60 shortcuts, escalated from 26
**Response:**
- usersafety@ auto-reply (safeguards template)
- support@ Fin AI Agent (automated)
- support@ template reply that misquoted the count (said 60 when body stated 60 — agent also auto-closed conversation after 4 hours of silence from user)

### Email 3 — 2026-04-08 07:22 UTC
**To:** support@anthropic.com
**Subject:** Third attempt — Claude Max subscriber requesting human review, not AI response
**Payload:** Explicit request for human reviewer after two AI-agent responses
**Response:**
- Fin AI Agent (same automated system)
- Support template acknowledgment

### Email 4 — 2026-04-08 10:34 UTC
**To:** support@anthropic.com
**Subject:** Claude Max subscriber: 73 documented production failures with peer-reviewed validation — requesting human review
**Payload:** 73 shortcuts + request for human review
**Response:** Fin AI Agent only.

### Email 5 — 2026-04-08 10:37 UTC
**To:** support@anthropic.com
**Subject:** Follow-up: Research paper now complete — 73 AI failures validated by 11 Grade-A peer-reviewed sources
**Payload:** Notification that formal research paper had been completed
**Response:** Fin AI Agent + generic support ack.

### Email 6 — 2026-04-08 10:49 UTC
**To:** feedback@anthropic.com
**Subject:** Claude Max subscriber offering Anthropic a validated research package: 73 documented failures, 11 Grade-A peer-reviewed sources including your own. Third attempt for human review.
**Payload:** Third attempt via feedback channel
**Response:** Auto-reply only.

### Email 7 — 2026-04-08 15:29 UTC
**To:** damodei@anthropic.com, daniela@anthropic.com, mkrieger@anthropic.com
**Subject:** 85 documented Claude Max production failures with peer-reviewed validation — dataset available for your engineering team
**Payload:** Direct to founders/leadership. 85 shortcuts.
**Delivery status:**
- `daniela@anthropic.com` — delivered
- `mkrieger@anthropic.com` — delivered
- `damodei@anthropic.com` — **BOUNCED** (address does not exist in this format)
- `jclark@anthropic.com` (also tried) — **BOUNCED**
- `smccandlish@anthropic.com` (also tried) — **BOUNCED**
- `tbrown@anthropic.com` (also tried) — **BOUNCED**
**Response from valid recipients:** Zero (daniela, mkrieger received — never replied).
**System responses:** security+noreply, feedback+noreply, usersafety, support (Fin AI) all auto-replied.

### Email 8 — 2026-04-14 09:00 UTC (6 days after last attempt)
**To:** daniela@anthropic.com, mkrieger@anthropic.com, cc: usersafety@, support@, feedback@
**Subject:** Follow-up #2: No human response after 6 days — 119+ documented Claude Max failures, peer-reviewed validation, three controlled experiments
**Payload:** Follow-up acknowledging 6-day silence
**Response:** Auto-replies from feedback+noreply, usersafety, support Fin AI. No human response.

### Email 9 — 2026-04-14 10:08 UTC
**To:** daniela@anthropic.com, mkrieger@anthropic.com, cc: usersafety@, support@, feedback@
**Subject:** Follow-up #3: Evidence now public on GitHub — 119+ failures, repo link inside
**Payload:** Public github repo link (this repository)
**Response:** Auto-replies only.

### Response received — 2026-04-16 03:45 UTC + 04:35 UTC
**From:** support@mail.anthropic.com
**Subjects:** Auto-categorized as "Re: [original subject]" and "Re: Accept"
**Content:** Template apology for response delay + standard "model output quality" category response. Content of the template:
- Apology for delay
- Standard explanation that Claude generates responses based on training patterns
- 5 best-practices tips for better prompting
- Suggestion to use thumbs-down feedback
- **Last line: "Note that further replies to this ticket may not be monitored."**

This template is sent to every user who writes about Claude quality, regardless of evidence volume. It closes the support ticket.

---

## Observed patterns

### Pattern A: Email categorization routes evidence to template
Every email mentioning "Claude", "failures", or "model quality" received the same template-category response. The template's closing line ("further replies may not be monitored") closes the support ticket, regardless of the specificity or volume of evidence attached.

### Pattern B: Four founder/leadership email addresses appear to be invalid
Emails to `damodei@`, `jclark@`, `smccandlish@`, `tbrown@` all bounced. These follow the common corporate format `firstinitiallast@company.com` but are not active. Only `daniela@anthropic.com` and `mkrieger@anthropic.com` are receiving.

### Pattern C: Valid recipients do not reply
`daniela@anthropic.com` and `mkrieger@anthropic.com` have received three emails (Apr 8, Apr 14 x2). No response has arrived from either. Not acknowledgments, not declines — silence.

### Pattern D: Fin AI Agent misquoted evidence
In email exchange thread 3 (Apr 8), the Fin AI Agent quoted "60 shortcuts" when the email body stated a different number. The user's follow-up explicitly noted this: "I documented 73 AI failures — not 60, as your AI agent states. Your AI agent didn't read my email."

### Pattern E: Duplicate auto-responses when cc'd
Emails cc'd to multiple Anthropic addresses (usersafety@, support@, feedback@) generated 3-4 simultaneous auto-replies from each channel, clogging the sender's inbox with the same template content.

---

## What this means for research

The Gmail outreach record is not noise — it is a data point. A subscriber with a specific, documented, well-formatted research corpus attempted direct contact with Anthropic through the published channels. The response at every step was an auto-classifier routing to a template.

For research on LLM-company user-feedback loops, this is the case study. The infrastructure designed to receive user feedback appears optimized to close tickets, not to escalate substantive evidence.

**If you are reading this as an Anthropic employee:** the point is not that no one responded. The point is that the system is designed such that no one could respond — every channel classifies and templates before a human sees.

---

## For journalists investigating this story

Thread IDs retained in sender's Gmail; full plaintext bodies available on request. Dates, recipients, and response templates as listed are verifiable.

Conversation IDs from Fin AI Agent (for Anthropic internal reference): 215473819689789, 215473820418259, 215473822013163, 215473822035371, 215473900939366, 215473901453706.

---

Extract generated: 2026-04-18
Source: abhishek.ajitsaria@gmail.com Gmail archive
Tool used: Gmail API via MCP
