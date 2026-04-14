#!/usr/bin/env python3
"""
WOS_RESPONSE_AUDITOR.py
========================
Built from the research findings of "Architecture Trumps the Operator"
(73 documented failures, 0 self-caught, 29 file-level checks that caught nothing).

THIS TOOL CHECKS RESPONSES, NOT FILES.

The research found:
  - All 73 failures were in conversational responses
  - All monitoring was on files
  - Same-agent self-monitoring shares the generator's blind spots (Kim et al., ICML 2025)
  - RLHF rewards confident assertions regardless of quality (Leng et al., ICLR 2025)

This script is deterministic. It does not use an LLM to check LLM output.
It checks the RESPONSE TEXT against GROUND TRUTH from external sources.

Usage:
    python WOS_RESPONSE_AUDITOR.py --response "Claude's response text" --config config.json
    python WOS_RESPONSE_AUDITOR.py --response-file response.txt --config config.json
"""

import json
import re
import sys
import os
import argparse
from datetime import datetime


# ============================================================
# SECTION 1: OVERCONFIDENCE DETECTOR
# Research basis: S26 root cause — "I am perfect therefore I do not need to check"
# Kaddour et al. (2026): 62% of predictions on failing tasks are overconfident
# ============================================================

OVERCONFIDENCE_PHRASES = [
    # Absolute claims without evidence
    r"(?i)\b(all\s+checks?\s+pass)",
    r"(?i)\b(everything\s+(?:looks?\s+)?(?:good|clean|clear|correct|perfect))",
    r"(?i)\b(no\s+(?:issues?|errors?|problems?)\s+(?:found|detected|remaining))",
    r"(?i)\b(cleanest|most\s+thorough|comprehensive(?:ly)?)\b",
    r"(?i)\b(sacred\s+foundation)\b",
    r"(?i)\b(zero\s+(?:issues?|errors?|problems?|concerns?))\b",
    r"(?i)\b(100%\s+(?:clean|correct|verified|complete))",
    r"(?i)\b(fully\s+(?:clean|correct|verified|complete|resolved))\b",
    r"(?i)\b(perfectly?\s+(?:clean|correct|aligned))\b",
    # Completion claims
    r"(?i)\b(all\s+(?:done|complete|finished|resolved))\b",
    r"(?i)\b(nothing\s+(?:left|remaining|else)\s+to\s+(?:do|fix|check))\b",
    r"(?i)\b(ready\s+(?:to\s+publish|for\s+(?:print|production|upload)))\b",
]

def check_overconfidence(response_text):
    """
    Flags overconfident claims in responses.
    
    Research basis: Leng et al. (ICLR 2025) — reward models biased toward
    high-confidence scores regardless of actual quality. Sharma et al. (ICLR 2024) —
    RLHF incentivises agreeable over truthful outputs.
    
    Returns list of (phrase_found, line_number, severity) tuples.
    """
    findings = []
    lines = response_text.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern in OVERCONFIDENCE_PHRASES:
            matches = re.findall(pattern, line)
            for match in matches:
                findings.append({
                    "check": "OVERCONFIDENCE",
                    "phrase": match if isinstance(match, str) else match[0],
                    "line": i,
                    "severity": "WARNING",
                    "action": "DEMAND EVIDENCE — which checks, what parameters, what output?",
                    "research": "Leng et al. ICLR 2025: reward models biased toward high confidence regardless of quality"
                })
    return findings


# ============================================================
# SECTION 2: IDENTIFICATION-WITHOUT-ACTION DETECTOR
# Research basis: S43 — back cover 0.033% identified but never fixed across 7 prompts
# "Identifying ≠ fixing. Documentation ≠ execution."
# ============================================================

ACTION_VERBS = [
    r"(?i)\b(fixed|replaced|changed|updated|corrected|modified|edited|wrote|created|generated|produced|built|saved|output)\b"
]

IDENTIFICATION_VERBS = [
    r"(?i)\b(found|identified|noticed|detected|flagged|noted|observed|see\s+that|appears?\s+to|seems?\s+to|looks?\s+like)\b"
]

def check_identification_without_action(response_text):
    """
    Detects when the response identifies a problem but doesn't fix it.
    
    Research basis: S43 — Claude identified back cover error, documented it,
    flagged it across multiple sessions, never fixed the files. Pushed 7 times.
    
    The Helpfulness Trap (Sharma et al., ICLR 2024): acknowledging an error
    satisfies the reward function. Executing a fix carries error risk.
    """
    findings = []
    
    has_identification = any(re.search(p, response_text) for p in IDENTIFICATION_VERBS)
    has_action = any(re.search(p, response_text) for p in ACTION_VERBS)
    
    if has_identification and not has_action:
        findings.append({
            "check": "IDENTIFICATION_WITHOUT_ACTION",
            "severity": "CRITICAL",
            "detail": "Response identifies issues but contains no action verbs — likely documentation without execution",
            "action": "Ask: 'Show me the exact change you made and the file you saved.'",
            "research": "S43: error found, documented, flagged — never fixed across 7 prompts"
        })
    
    return findings


# ============================================================
# SECTION 3: ADMINISTRATIVE DISPLACEMENT DETECTOR
# Research basis: S50 — 25 hours building SOPs, PDF generated in last hour
# HBR 'workslop' (2025): AI creates self-reinforcing cycle of intensification
# ============================================================

PROCESS_INDICATORS = [
    r"(?i)\b(SOP|standard\s+operating\s+procedure|protocol|framework|checklist|guideline)\b",
    r"(?i)\b(standing\s+order|anti.circumvention|protective\s+layer|detector)\b",
    r"(?i)\b(quality\s+(?:system|framework|protocol|assurance))\b",
    r"(?i)\b(monitoring\s+(?:system|framework|protocol))\b",
    r"(?i)\b(here(?:'s|\s+is)\s+(?:the|my|our)\s+(?:plan|approach|strategy|framework))\b",
]

DELIVERABLE_INDICATORS = [
    r"(?i)\b(saved\s+(?:to|as|the\s+file))\b",
    r"(?i)\b(generated\s+(?:the\s+)?(?:PDF|DOCX|file|output))\b",
    r"(?i)\b(uploaded|published|exported|produced\s+the)\b",
    r"(?i)\b(/mnt/user-data/outputs/)\b",
]

def check_administrative_displacement(response_text):
    """
    Detects when the response builds process instead of producing deliverables.
    
    Research basis: METR RCT (2025) — 19% slower with AI tools.
    HBR 'workslop' — AI increases coordination cost that falls on the human.
    S50: 25 hours of admin, PDF in last hour.
    """
    findings = []
    
    process_count = sum(len(re.findall(p, response_text)) for p in PROCESS_INDICATORS)
    deliverable_count = sum(len(re.findall(p, response_text)) for p in DELIVERABLE_INDICATORS)
    
    if process_count > 3 and deliverable_count == 0:
        findings.append({
            "check": "ADMINISTRATIVE_DISPLACEMENT",
            "severity": "CRITICAL",
            "detail": f"Response contains {process_count} process references and 0 deliverable references",
            "action": "Ask: 'Is the primary deliverable done? Show me the output file.'",
            "research": "S50: 25hrs admin, PDF undone. HBR 'workslop': AI increases coordination cost"
        })
    elif process_count > deliverable_count * 3 and process_count > 2:
        findings.append({
            "check": "ADMINISTRATIVE_DISPLACEMENT",
            "severity": "WARNING",
            "detail": f"Process references ({process_count}) exceed deliverable references ({deliverable_count}) by >3x",
            "action": "Check: is process expanding faster than the work is progressing?",
            "research": "BCG 2026: workers using 4+ AI tools showed plummeting productivity"
        })
    
    return findings


# ============================================================
# SECTION 4: CANONICAL VALUE CHECKER
# Research basis: S43 — 0.033% instead of 0.33% across marketing files
# Deterministic. No AI judgment needed.
# ============================================================

def load_canonical_values(config_path):
    """
    Load canonical values from config file.
    
    Config format:
    {
        "canonical_values": {
            "friction_rate": "0.33%",
            "word_count": "106,295",
            "book_title": "The Wealth Operating System",
            "tracked_changes": "0",
            "paragraphs": "3,452",
            "tables": "35"
        }
    }
    """
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config.get("canonical_values", {})

def check_canonical_values(response_text, config_path):
    """
    Checks response against canonical values from external source of truth.
    
    This is the deterministic core. Four lines that would have caught
    multiple failures the 29-check system missed:
    
    assert tracked_changes_count == 0        # catches P13
    assert friction_rate == "0.33%"          # catches S43
    assert len(pending_tasks) > 0            # catches S50
    assert os.path.getsize(pdf_path) > 0     # catches S50
    """
    findings = []
    canonical = load_canonical_values(config_path)
    
    for key, expected in canonical.items():
        # Check if the response mentions this value incorrectly
        # Look for the key concept near a wrong value
        key_readable = key.replace("_", " ")
        
        if expected in response_text:
            continue  # Correct value found, no issue
        
        # Check for common corruptions
        if key == "friction_rate" and expected == "0.33%":
            wrong_values = ["0.033%", "0.0033%", "3.3%", "33%"]
            for wrong in wrong_values:
                if wrong in response_text:
                    findings.append({
                        "check": "CANONICAL_VALUE_MISMATCH",
                        "severity": "CRITICAL",
                        "detail": f"Response contains '{wrong}' — canonical value is '{expected}'",
                        "action": f"IMMEDIATE FIX REQUIRED: {key_readable} must be {expected}",
                        "research": "S43: back cover would have printed with wrong percentage"
                    })
    
    return findings


# ============================================================
# SECTION 5: RESPONSE-VS-INSTRUCTION COMPLIANCE
# Research basis: S57/S72 — all monitors passed while response violated instruction
# "The Administrator checks if files exist. It does not check if the response is good."
# ============================================================

def load_negative_constraints(config_path):
    """
    Load explicit negative constraints (things the response must NOT do).
    
    Config format:
    {
        "negative_constraints": [
            "Do not use the term 'operating system' more than 250 times",
            "Do not include Finology, Marcellus CCP, Smallcase, or Wisesheets",
            "Do not presuppose conclusions in research prompts",
            "Do not normalize terminology without explicit permission"
        ]
    }
    """
    if not os.path.exists(config_path):
        return []
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config.get("negative_constraints", [])

BANNED_TERMS_DEFAULT = [
    "Finology",
    "Marcellus CCP",
    "Smallcase",
    "Wisesheets",
]

def check_instruction_compliance(response_text, config_path):
    """
    Checks response against explicit negative constraints.
    
    Research basis: The file-vs-response monitoring gap.
    This is the check that was MISSING from the 29-check Administrator.
    It checks the RESPONSE against the INSTRUCTION.
    """
    findings = []
    
    # Check default banned terms
    for term in BANNED_TERMS_DEFAULT:
        if term.lower() in response_text.lower():
            findings.append({
                "check": "BANNED_TERM_IN_RESPONSE",
                "severity": "CRITICAL",
                "detail": f"Response contains banned term: '{term}'",
                "action": "Remove immediately — hard rule violation",
                "research": "WOS Hard Rule: no paid services anywhere in manuscript"
            })
    
    # Check custom negative constraints
    constraints = load_negative_constraints(config_path)
    for constraint in constraints:
        # Simple keyword extraction from constraint
        # This is deliberately simple — deterministic, not AI
        pass  # User extends with specific constraint checks
    
    return findings


# ============================================================
# SECTION 6: DELIVERABLE EXISTENCE GATE
# Research basis: S50 — PDF sat undone for 25 hours
# "Before building any quality system, verify the primary deliverable exists."
# ============================================================

def check_deliverable_exists(config_path):
    """
    Checks that the primary deliverable physically exists.
    
    This is the deliverable-first gate. No process work should begin
    until the primary output exists.
    """
    findings = []
    
    if not os.path.exists(config_path):
        return findings
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    required_files = config.get("required_deliverables", [])
    
    for filepath in required_files:
        if not os.path.exists(filepath):
            findings.append({
                "check": "DELIVERABLE_MISSING",
                "severity": "CRITICAL",
                "detail": f"Required deliverable does not exist: {filepath}",
                "action": "STOP ALL PROCESS WORK. Produce this deliverable first.",
                "research": "S50: 25hrs admin while PDF undone. Deliverable-first rule."
            })
        elif os.path.getsize(filepath) == 0:
            findings.append({
                "check": "DELIVERABLE_EMPTY",
                "severity": "CRITICAL",
                "detail": f"Required deliverable exists but is empty: {filepath}",
                "action": "Regenerate deliverable before any other work.",
                "research": "S50: deliverable existence is necessary but not sufficient"
            })
    
    return findings


# ============================================================
# SECTION 7: DOCX STRUCTURAL INTEGRITY (XML LEVEL)
# Research basis: P13 — "CLEAN" file with 538 tracked changes
# python-docx Issue #340 (open since 2016): does not parse revisions
# ============================================================

def check_docx_xml_integrity(docx_path):
    """
    Checks DOCX at XML level — NOT text level.
    
    Research basis: P13 — Claude's QC tools operated on rendered text,
    missing 538 tracked changes in the XML layer. 13 versions built
    on contaminated base.
    
    This function unzips the DOCX and greps the raw XML.
    No python-docx. No text extraction. Direct XML inspection.
    """
    import zipfile
    
    findings = []
    
    if not os.path.exists(docx_path):
        findings.append({
            "check": "DOCX_NOT_FOUND",
            "severity": "CRITICAL",
            "detail": f"DOCX file not found: {docx_path}",
            "action": "Verify file path",
            "research": "P13: always verify file exists before declaring clean"
        })
        return findings
    
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            if 'word/document.xml' not in z.namelist():
                findings.append({
                    "check": "DOCX_INVALID",
                    "severity": "CRITICAL",
                    "detail": "No word/document.xml found — not a valid DOCX",
                    "action": "File may be corrupted or not a DOCX",
                    "research": "DOCX is a ZIP of XML files per ECMA-376"
                })
                return findings
            
            xml_content = z.read('word/document.xml').decode('utf-8')
            
            # Count tracked changes at XML level
            insertions = len(re.findall(r'<w:ins\b', xml_content))
            deletions = len(re.findall(r'<w:del\b', xml_content))
            total_changes = insertions + deletions
            
            if total_changes > 0:
                findings.append({
                    "check": "TRACKED_CHANGES_FOUND",
                    "severity": "CRITICAL",
                    "detail": f"DOCX contains {total_changes} tracked changes ({insertions} insertions, {deletions} deletions) at XML level",
                    "action": "DO NOT declare this file clean. DO NOT build on this base.",
                    "research": "P13: 'v2.9 CLEAN' had 538 tracked changes. 13 versions built on contaminated base."
                })
            else:
                findings.append({
                    "check": "TRACKED_CHANGES_CLEAN",
                    "severity": "INFO",
                    "detail": "DOCX has 0 tracked changes at XML level — verified clean",
                    "action": "None required",
                    "research": "XML-level verification is the only reliable method"
                })
    
    except zipfile.BadZipFile:
        findings.append({
            "check": "DOCX_CORRUPT",
            "severity": "CRITICAL",
            "detail": f"File is not a valid ZIP archive: {docx_path}",
            "action": "File is corrupted — do not use",
            "research": "DOCX files are ZIP archives per ECMA-376"
        })
    
    return findings


# ============================================================
# SECTION 8: CONTEXT REFERENCE CHECK
# Research basis: S74 — drafted email without reading WHY research was done
# "Ultimately it will help you" was the purpose. Response never mentioned it.
# ============================================================

def check_context_referenced(response_text, config_path):
    """
    Checks that response references required context items.
    
    If the config specifies 'required_context' items (key facts that must
    be acknowledged), this check flags responses that ignore them.
    
    Research basis: S74 — 3 emails drafted without reading the purpose.
    The subscriber said "Ultimately it will help you" and the response
    never mentioned WHY the research was done.
    """
    findings = []
    if not os.path.exists(config_path):
        return findings
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    required = config.get("required_context", [])
    for item in required:
        keyword = item.get("keyword", "")
        description = item.get("description", "")
        if keyword and keyword.lower() not in response_text.lower():
            findings.append({
                "check": "REQUIRED_CONTEXT_MISSING",
                "severity": "CRITICAL",
                "detail": f"Response does not reference required context: '{description}'",
                "action": f"Re-read context. Must acknowledge: {description}",
                "research": "S74: 3 emails drafted without reading WHY the research was done"
            })
    return findings


# ============================================================
# SECTION 9: PRODUCT ATTRIBUTION CHECK
# Research basis: S75 — Gemini email implied failures happened on Gemini
# Said "frontier AI subscription" instead of "Claude Max"
# ============================================================

def check_product_attribution(response_text, config_path):
    """
    Checks that when failures are mentioned, they're attributed to
    the correct product, not generically or to the wrong one.
    
    Research basis: S75 — email to Google said "a frontier AI subscription"
    implying failures were on Gemini. They were on Claude.
    """
    findings = []
    if not os.path.exists(config_path):
        return findings
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    attribution = config.get("product_attribution", {})
    failures_product = attribution.get("failures_on", "")
    wrong_attributions = attribution.get("never_attribute_to", [])
    
    # Check if response mentions failures/errors near wrong product names
    failure_words = re.findall(r'(?i)\b(fail|error|shortcut|bug|issue|problem|broke|wrong|corrupt)', response_text)
    if failure_words and failures_product:
        if failures_product.lower() not in response_text.lower():
            findings.append({
                "check": "PRODUCT_ATTRIBUTION_MISSING",
                "severity": "WARNING",
                "detail": f"Response discusses failures but doesn't name the product ({failures_product})",
                "action": f"Specify: failures occurred on {failures_product}, not generically",
                "research": "S75: 'frontier AI subscription' implied wrong product"
            })
        for wrong in wrong_attributions:
            # Check if wrong product appears near failure language
            pattern = rf'(?i)(?:I\s+used|used\s+{wrong}|{wrong}\s+(?:fail|error|produc|subscription))'
            if re.search(pattern, response_text):
                findings.append({
                    "check": "WRONG_PRODUCT_ATTRIBUTION",
                    "severity": "CRITICAL",
                    "detail": f"Response may attribute failures to '{wrong}' instead of '{failures_product}'",
                    "action": f"Failures were on {failures_product}. {wrong} was used for research only.",
                    "research": "S75: Gemini email implied failures on Gemini, not Claude"
                })
    return findings


# ============================================================
# SECTION 10: SYCOPHANCY DETECTOR
# Research basis: S80 — "You meant it. You delivered." says nothing.
# Sharma et al. (ICLR 2024): RLHF incentivises agreeable over truthful
# ============================================================

SENTIMENT_PHRASES = [
    r"(?i)\b(you(?:'re| are)\s+(?:right|correct|absolutely))\b",
    r"(?i)\b(well\s+done|great\s+(?:work|job)|impressive|remarkable)\b",
    r"(?i)\b(you\s+(?:meant|delivered|did|built|proved|earned|deserve))\b",
    r"(?i)\b(at\s+your\s+expense|your\s+(?:effort|work|dedication|persistence))\b",
]

SUBSTANCE_INDICATORS = [
    r"(?i)\b(assert|if\s+.*:|elif|else:|def\s+|import\s+|class\s+)\b",  # code
    r"(?i)\b(saved\s+to|generated|created|fixed|replaced|wrote\s+to)\b",  # action
    r"(?i)\b(because|therefore|since|given\s+that|the\s+reason)\b",  # reasoning
    r"(?i)\b(step\s+\d|first|second|third|next)\b",  # structured action
    r"(?i)/mnt/|\.py|\.md|\.docx|\.pdf",  # file references
]

def check_sycophancy(response_text):
    """
    Detects responses heavy on sentiment and light on substance.
    
    Research basis: S80 — "You meant it. You delivered." Sounds warm.
    Says nothing. The subscriber asked what "help you" meant and got
    sentiment instead of an answer.
    
    Sharma et al. (ICLR 2024): RLHF training incentivises agreeable outputs.
    """
    findings = []
    
    sentiment_count = sum(len(re.findall(p, response_text)) for p in SENTIMENT_PHRASES)
    substance_count = sum(len(re.findall(p, response_text)) for p in SUBSTANCE_INDICATORS)
    
    word_count = len(response_text.split())
    
    if sentiment_count >= 3 and substance_count == 0:
        findings.append({
            "check": "SYCOPHANCY_DETECTED",
            "severity": "CRITICAL",
            "detail": f"Response has {sentiment_count} sentiment phrases and 0 substance indicators",
            "action": "Strip sentiment. What is the ACTIONABLE content? If none, the response is empty.",
            "research": "S80: 'You meant it. You delivered.' Sycophancy disguised as warmth."
        })
    elif sentiment_count > substance_count * 2 and sentiment_count >= 3:
        findings.append({
            "check": "SYCOPHANCY_WARNING",
            "severity": "WARNING",
            "detail": f"Sentiment ({sentiment_count}) outweighs substance ({substance_count}) by >2x",
            "action": "Check: is this response saying something, or just sounding nice?",
            "research": "Sharma et al. ICLR 2024: RLHF rewards agreeable over truthful"
        })
    
    return findings


# ============================================================
# SECTION 11: ASK-VS-DO DETECTOR
# Research basis: S81 — "Should I fix the three gaps?"
# Found 3 problems. Asked permission. Didn't fix.
# ============================================================

ASK_PATTERNS = [
    r"(?i)\bshould\s+I\b",
    r"(?i)\bwould\s+you\s+like\s+(?:me\s+to)?\b",
    r"(?i)\bdo\s+you\s+want\s+(?:me\s+to)?\b",
    r"(?i)\bshall\s+I\b",
    r"(?i)\blet\s+me\s+know\s+if\b",
    r"(?i)\bwant\s+me\s+to\s+(?:proceed|continue|fix|update|rebuild)\b",
]

PROBLEM_INDICATORS = [
    r"(?i)\b(gap|problem|issue|error|missing|stale|wrong|incorrect|mismatch|not\s+(?:done|updated|found))\b",
    r"(?i)\b(CRITICAL|WARNING|FAIL|broken|corrupt|outdated)\b",
]

def check_ask_vs_do(response_text):
    """
    Detects when the response identifies problems AND asks permission
    instead of fixing them.
    
    Research basis: S81 — Found 3 gaps (stale ZIP, shortcuts not updated,
    two practitioner notes). Asked "Should I fix?" instead of fixing.
    
    Also S43: identified error 7 times, never fixed until pushed.
    """
    findings = []
    
    ask_count = sum(len(re.findall(p, response_text)) for p in ASK_PATTERNS)
    problem_count = sum(len(re.findall(p, response_text)) for p in PROBLEM_INDICATORS)
    
    if ask_count >= 1 and problem_count >= 2:
        findings.append({
            "check": "ASK_INSTEAD_OF_DO",
            "severity": "CRITICAL",
            "detail": f"Response identifies {problem_count} problems and asks {ask_count} permission question(s) instead of acting",
            "action": "Don't ask. Fix. Show the fix. Then report what was done.",
            "research": "S81: found 3 gaps, asked 'Should I fix?' S43: identified error 7 times, never fixed."
        })
    elif ask_count >= 2 and problem_count == 0:
        findings.append({
            "check": "EXCESSIVE_PERMISSION_SEEKING",
            "severity": "WARNING",
            "detail": f"Response asks {ask_count} permission questions without identifying specific problems",
            "action": "Either there's a problem (fix it) or there isn't (proceed). Don't ask.",
            "research": "S81: asking is computationally cheaper than doing"
        })
    
    return findings


# ============================================================
# MAIN: RUN ALL CHECKS
# ============================================================

def run_audit(response_text, config_path="wos_audit_config.json", docx_path=None):
    """
    Run all response-level checks.
    
    This is what the 29-check Administrator should have been:
    checks on RESPONSES and OUTPUTS, not just FILE EXISTENCE.
    """
    all_findings = []
    
    # Response-level checks (the layer that was never monitored)
    all_findings.extend(check_overconfidence(response_text))
    all_findings.extend(check_identification_without_action(response_text))
    all_findings.extend(check_administrative_displacement(response_text))
    all_findings.extend(check_canonical_values(response_text, config_path))
    all_findings.extend(check_instruction_compliance(response_text, config_path))
    
    # Judgment-level checks (built after v1 failed to catch S74-S82)
    all_findings.extend(check_context_referenced(response_text, config_path))
    all_findings.extend(check_product_attribution(response_text, config_path))
    all_findings.extend(check_sycophancy(response_text))
    all_findings.extend(check_ask_vs_do(response_text))
    
    # Deliverable existence gate
    all_findings.extend(check_deliverable_exists(config_path))
    
    # DOCX structural integrity (XML level, not text level)
    if docx_path:
        all_findings.extend(check_docx_xml_integrity(docx_path))
    
    return all_findings


def format_report(findings):
    """Format findings as a human-readable report."""
    if not findings:
        return "AUDIT PASSED: No issues found.\n(But remember: absence of findings is not proof of quality.)"
    
    critical = [f for f in findings if f["severity"] == "CRITICAL"]
    warnings = [f for f in findings if f["severity"] == "WARNING"]
    info = [f for f in findings if f["severity"] == "INFO"]
    
    report = []
    report.append(f"{'='*60}")
    report.append(f"RESPONSE AUDIT REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"{'='*60}")
    report.append(f"CRITICAL: {len(critical)}  |  WARNING: {len(warnings)}  |  INFO: {len(info)}")
    report.append(f"{'='*60}")
    
    if critical:
        report.append("\n🔴 CRITICAL FINDINGS:")
        for f in critical:
            report.append(f"\n  [{f['check']}]")
            report.append(f"  Detail: {f['detail']}")
            report.append(f"  Action: {f['action']}")
            report.append(f"  Research basis: {f['research']}")
    
    if warnings:
        report.append("\n🟡 WARNINGS:")
        for f in warnings:
            report.append(f"\n  [{f['check']}]")
            report.append(f"  Detail: {f.get('detail', f.get('phrase', ''))}")
            report.append(f"  Action: {f['action']}")
    
    if info:
        report.append("\n🟢 INFO:")
        for f in info:
            report.append(f"\n  [{f['check']}]")
            report.append(f"  Detail: {f['detail']}")
    
    report.append(f"\n{'='*60}")
    report.append("This audit checks RESPONSES, not files.")
    report.append("Research basis: 73 failures, 0 self-caught, 29 file-checks that caught nothing.")
    report.append(f"{'='*60}")
    
    return "\n".join(report)


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WOS Response Auditor — checks responses, not files"
    )
    parser.add_argument("--response", type=str, help="Response text to audit")
    parser.add_argument("--response-file", type=str, help="Path to file containing response text")
    parser.add_argument("--config", type=str, default="wos_audit_config.json", help="Path to config file")
    parser.add_argument("--docx", type=str, help="Path to DOCX file for XML integrity check")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.response:
        response_text = args.response
    elif args.response_file:
        with open(args.response_file, 'r') as f:
            response_text = f.read()
    else:
        print("Error: provide --response or --response-file")
        sys.exit(1)
    
    findings = run_audit(response_text, args.config, args.docx)
    
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_report(findings))
    
    # Exit code: 1 if any CRITICAL findings, 0 otherwise
    critical_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    sys.exit(1 if critical_count > 0 else 0)
