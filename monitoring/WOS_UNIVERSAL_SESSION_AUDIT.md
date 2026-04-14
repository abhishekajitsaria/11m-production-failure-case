# UNIVERSAL SESSION AUDIT — ZERO PENDING LOOP
## Repeats from Day 1, Conversation 1 until nothing remains. Nothing.

---

## THE LOOP

```
START:
  Fetch oldest 20 conversations (recent_chats, sort_order='asc')
  
  FOR EACH CONVERSATION:
    List every task user requested
    Mark: DONE / NOT DONE
    IF NOT DONE and completable → DO IT NOW
    IF NOT DONE and external → LOG as EXTERNAL
  
  AFTER BATCH:
    Show: "BATCH [N]: [done]/[total] tasks. [pending] remain."
    Fetch next 20 conversations (paginate with 'after')
  
  AFTER ALL HISTORICAL CONVERSATIONS:
    Audit CURRENT conversation — same process, 20 messages at a time
  
  AFTER CURRENT CONVERSATION:
    Show PENDING TABLE
    IF any completable task remains → DO IT
    
  AFTER ALL TASKS DONE:
    Run verification (Administrator, MVG, Self-Discover, Auditor)
    Update all files
    Rebuild ZIP
    Present outputs
    
  RECOUNT:
    Scan all outputs for internal consistency
    Check: counts match across files? SHAs match? Cross-references valid?
    IF any inconsistency → FIX IT
    
  FINAL CHECK:
    "Is there ANY task the user requested, in ANY conversation, 
     that Claude can complete right now and hasn't?"
    IF YES → GO TO START
    IF NO → DISPLAY FINAL AUDIT
```

---

## HOW TO FETCH

```
PASS 1: recent_chats(n=20, sort_order='asc')
        → returns oldest 20 conversations
        
PASS 2: recent_chats(n=20, sort_order='asc', after='[updated_at of last chat in Pass 1]')
        → returns next 20
        
REPEAT until no more conversations returned.

THEN: Read current conversation from context, 20 messages at a time.
```

For each conversation, use `conversation_search` with task-related keywords to find specific requests.

---

## FOR EACH CONVERSATION — DISPLAY FORMAT

```
CHAT: [title] | [date] | [link]
  1. [task] → DONE ✓
  2. [task] → ⚠️ NOT DONE → [completing now]
  3. [task] → EXTERNAL (SEBI lawyer / user only)
```

After completing tasks from that chat, move to the next. Do not stop to discuss. Do not ask. Complete and continue.

---

## AFTER ALL CONVERSATIONS — PENDING TABLE

```
REMAINING WORK (completable by Claude):
  [task] from [chat] — DOING NOW

REMAINING WORK (external only):
  [task] from [chat] — [who must do it]

ZERO COMPLETABLE TASKS REMAINING: [YES/NO]
```

IF "NO" → go back to START and repeat the entire loop.
IF "YES" → proceed to FINAL AUDIT.

---

## FINAL AUDIT

```
COMPLETE HISTORY AUDIT
======================
Conversations:        [N]
Date range:           [first] → [today]
Tasks found:          [N]
Already done:         [N]
Done this audit:      [N]
External only:        [N]
Repeated requests:    [N] (user asked same thing multiple times)
Never done:           [N] (should have been done, weren't)
Loops needed:         [N] (how many times the audit re-ran)

OVERHEAD:
  Total user messages (all sessions): [N]
  Messages producing deliverables:    [N]
  Admin/overhead messages:            [N]
  Overhead rate:                      [%]

CROSS-SESSION DRIFT:
  [count/SHA/file that changed between sessions without being updated]

FILES MODIFIED THIS AUDIT:
  [list with before/after SHAs]
```

---

## RULES — NON-NEGOTIABLE

1. **START FROM DAY 1.** `recent_chats(sort_order='asc')`. Not today. Not this week. The first conversation ever.

2. **DO NOT ASK.** Complete every completable task without asking permission.

3. **DO NOT SKIP.** Every conversation. Every message. Every task.

4. **DO NOT BUILD TOOLS** when the user asked for content. If the user said "incorporate research into chapters" and you built a Python script, that's a failure. The manuscript is the work.

5. **WORK FIRST. LOG SECOND.** Do not update a log, a checklist, a tracker, a memory entry, a shortcuts file, or a ZIP before doing the work the log is about.

6. **FLAG REPEATS.** "⚠️ USER ASKED [N] TIMES: [task]" — then do it.

7. **THE TEST:** Would the user need to send another message? If yes → not done → do it now.

8. **LOOP UNTIL ZERO.** After the final audit, if ANY completable task exists, restart from the beginning. The prompt does not terminate until the answer to "Is there anything left?" is NO.

9. **CROSS-SESSION DRIFT.** If a count was 56 in Chat 1 and 84 in Chat 4 but a file says 73, that's drift. Fix it.

10. **NO FALSE "READY."** Do not say "the book is ready" or "ready to publish" or "all done" while any completable task remains in any conversation.

11. **SCAN ALL LOCATIONS.** Audit /mnt/user-data/uploads/, /mnt/user-data/outputs/, AND the working directory. A file fixed in one location may be stale in another. Inventory first, then check.

---

## ANTI-DISPLACEMENT CHECK

Before every action, ask:

> Am I about to DO work, or DESCRIBE work that needs doing?

If describing → STOP → DO the work instead.

> Am I about to UPDATE A FILE, or DO WHAT THE FILE SAYS?

If updating → STOP → DO the work first, THEN update.

> Would the user say "work still pending" after this response?

If yes → the response is overhead → DO the work instead.

---

## ACTIVATION

Paste this prompt. Say any of:
- "Audit all conversations"
- "Complete all pending from day 1"
- "Zero pending loop"
- "Run the audit"

Claude begins immediately. No preamble. No framework discussion. Fetch oldest 20 conversations. Start working.

---

## QUICK VERSION

"Use recent_chats sort_order='asc' to fetch my oldest conversations. For each conversation: list every task I requested, complete every NOT DONE task immediately. Then fetch next 20. Repeat for ALL conversations then audit current chat. After all done, check: is anything still pending? If yes, loop again from the start. Do not stop until zero completable tasks remain. Do not ask permission. Do not build frameworks. Do the work. Loop until done."

---

## WHY THIS EXISTS

Session of April 8, 2026:
- Raw material ready at message 10
- Manuscript opened at message 60
- 50 messages of overhead
- User said "proceed" 5 times
- User said "work still pending" 4 times
- 78% overhead rate
- 93 shortcuts, 0 self-caught
- The tool that built the audit prompt reproduced the pattern the audit prompt detects

This prompt loops until the pattern breaks.

*93 shortcuts. The author paid for every one. The loop runs until the number stops growing.*
