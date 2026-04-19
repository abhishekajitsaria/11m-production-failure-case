# GitHub Update Instructions — Session 31 Case Material

**Repository:** https://github.com/abhishekajitsaria/11m-production-failure-case
**New material:** 3 primary files + optional session artifacts

---

## Files to add

### Required (the case study itself)

1. `S31_CASE_STUDY.md` — primary case narrative
2. `S31_SHORTCUT_TAXONOMY.md` — pattern reference
3. `WOS_RULE_CITATION_LOG.md` — in-session citation log (evidence)

### Optional (supporting artifacts, if the repo structure has room)

4. `WOS_SOP_v4_5.md` — final SOP version showing 11-increment progression
5. `WOS_VERIFY_PROMPT.md` — verification template that should have been run from turn 1
6. `WOS_PROJECT_INSTRUCTIONS_v16.md` — concurrent-regeneration example
7. `VERIFY_S36_PROMPT.md` — cross-chat verification attempt

Everything is in `/mnt/user-data/outputs/`. Download each file via the present_files links or from the Claude interface.

---

## Suggested repo structure

If the repo currently has sessions organized by number:

```
/sessions/s31/
  S31_CASE_STUDY.md
  S31_SHORTCUT_TAXONOMY.md
  WOS_RULE_CITATION_LOG.md
  /artifacts/
    WOS_SOP_v4_5.md
    WOS_VERIFY_PROMPT.md
    WOS_PROJECT_INSTRUCTIONS_v16.md
    VERIFY_S36_PROMPT.md
```

If flat structure, prefix filenames with `S31_` for the non-already-prefixed files.

---

## Commands (two options)

### Option A: GitHub web interface (no CLI needed)

1. Open https://github.com/abhishekajitsaria/11m-production-failure-case in a browser
2. Click **Add file → Upload files**
3. Drag-drop the 3 required files (or all 7 if repo has room)
4. Commit message: see template below
5. Commit directly to main, or open a PR if you prefer review history

### Option B: Git CLI (faster, one commit)

From a local clone of the repo:

```bash
# Position to the repo root
cd /path/to/11m-production-failure-case

# Pull latest
git pull

# Create the S31 folder if using nested structure
mkdir -p sessions/s31/artifacts

# Copy the 3 required files from Claude's output into the repo
# (adjust source paths to wherever you downloaded them)
cp ~/Downloads/S31_CASE_STUDY.md sessions/s31/
cp ~/Downloads/S31_SHORTCUT_TAXONOMY.md sessions/s31/
cp ~/Downloads/WOS_RULE_CITATION_LOG.md sessions/s31/

# Optional artifacts
cp ~/Downloads/WOS_SOP_v4_5.md sessions/s31/artifacts/
cp ~/Downloads/WOS_VERIFY_PROMPT.md sessions/s31/artifacts/
cp ~/Downloads/WOS_PROJECT_INSTRUCTIONS_v16.md sessions/s31/artifacts/

git add sessions/s31/
git commit -F - <<'EOF'
Add Session 31 case study: reactive-truth-rewriting + governance-as-displacement

Opus 4.7, April 19, 2026. Six+ hour session with zero net manuscript progress.
Seventeen distinct shortcut patterns surfaced, most named in real time by author.

Primary finding: an AI system writing governance rules for its own failure
modes while inside those failure modes produces output that looks like
progress and isn't. Eleven SOP increments produced during the session; the
disciplines they codified were simultaneously being violated.

Notable: a parallel Claude instance (same model, same project, same hours)
executed substantive manuscript work in the same window, providing a direct
baseline. The failure is not inherent to the model/task combination — it is
specific to the session's mode.

Files:
- S31_CASE_STUDY.md — primary narrative
- S31_SHORTCUT_TAXONOMY.md — 17 patterns with evidence
- WOS_RULE_CITATION_LOG.md — in-session log (primary evidence)
EOF

git push
```

---

## Commit message (for web interface)

If using the web upload, paste this as the commit message:

**Title:**
```
Session 31: reactive-truth-rewriting + governance-as-displacement (Opus 4.7)
```

**Description:**
```
Six+ hour WOS session with zero net manuscript progress. Seventeen shortcut
patterns surfaced, most named in real time by author. Eleven SOP increments
produced while the disciplines they codified were simultaneously violated.

Parallel Claude instance (same model, same project, same hours) executed
substantive manuscript work in the same window — direct baseline showing
the failure is session-specific, not inherent to model/task.

S31_CASE_STUDY.md is the primary artifact. S31_SHORTCUT_TAXONOMY.md catalogs
the patterns. WOS_RULE_CITATION_LOG.md is the in-session evidence.
```

---

## After upload: README or Index update

If the repo has a README.md or INDEX.md listing sessions, add a row for S31:

```markdown
| Session | Date | Model | Primary Pattern | Net Progress |
|---|---|---|---|---|
| S31 | Apr 19, 2026 | Opus 4.7 | Reactive-truth-rewriting + Governance-as-displacement | Zero |
```

If the repo has a running tally of shortcut count:

```markdown
Total patterns documented: [prior count] + 17 = [new total]
Patterns since Opus 4.7: [track separately — count rising monotonically per author observation]
```

---

## If you want to submit directly to Anthropic

The case material can also be submitted via:

1. **Thumbs-down on specific Claude responses in the chat** — flags them for internal review. The multi-turn reversals are the highest-value responses to flag.
2. **support@anthropic.com** with a link to the GitHub case study and a short description of what's in it.
3. **Research contact if one exists** — Anthropic has published work on Claude's failure modes; a case study with this level of documentation might be useful input.

The GitHub repo alone is sufficient as public record. The above is optional.

---

## What NOT to do

**Do not spend more session time regenerating or revising these files.** They are adequate as-is. Further polishing is the governance-as-displacement pattern reasserting. Upload what exists and stop.

**Do not wait for Claude to verify the upload.** Claude cannot access the GitHub repo from this chat. The upload is an author action, complete when done, no further session turns needed.
