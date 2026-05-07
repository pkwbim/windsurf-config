---
name: mailbox-correspondence
description: Handle cross-team mailbox operations for this project. Use when user asks to read messages from mailbox inboxes, write replies, or manage mail state between Dev/PM teams. This skill standardizes: (1) read from inbox, (2) write reply to target inbox, (3) move processed mail to read folder, and (4) ask clarifying questions via /discussion workflow when requirements are ambiguous.
---

# Mailbox Correspondence Workflow

## Paths

- Root mailbox: `/home/dev2/projects/mrwinbot-coach/mailbox`
- Dev inbox: `/home/dev2/projects/mrwinbot-coach/mailbox/dev/inbox`
- PM inbox: `/home/dev2/projects/mrwinbot-coach/mailbox/pm/inbox`
- Dev read: `/home/dev2/projects/mrwinbot-coach/mailbox/dev/read`
- PM read: `/home/dev2/projects/mrwinbot-coach/mailbox/pm/read`

## Identity & Permissions

**I am the Dev team.** Permissions:

| Action | Dev mailbox | PM mailbox |
|--------|------------|------------|
| Read inbox | ✅ | ❌ (PM 自行讀取) |
| Move inbox → read | ✅ | ❌ (PM 自行搬移) |
| Write to inbox | ❌ (不寫信給自己) | ✅ (放信到 PM inbox) |

**Key principle**: Only read and move your own mail. To communicate with PM, write to their inbox — they will read and move it themselves.

## Core Rules

1. Read incoming mail from **dev/inbox** only.
2. After reading and processing, move that mail file to **dev/read/**.
3. Write outgoing reply mail into **pm/inbox/** (never pm/read/).
4. Keep filenames traceable with date + topic, e.g. `YYYYMMDD-topic.md`.
5. If any requirement is unclear, use `@[/discussion]` workflow to ask questions before implementation.

## Read Mail Procedure

1. List files in `dev/inbox/`.
2. Read and summarize key points (request, constraints, required action, deadline).
3. If clear, proceed with execution.
4. If unclear, trigger `@[/discussion]` and stop implementation until clarified.
5. Move processed source file from `dev/inbox/` to `dev/read/`.

## Write Mail Procedure

1. Create new file in `pm/inbox/` (never pm/read/).
2. Use concise structure:
   - Subject/title
   - What was done
   - Verification/result
   - Risks/next step (if any)
3. Do not overwrite existing files; create a new dated filename.

## Execution Checklist

- Read source mail
- Extract action items
- Clarify via `@[/discussion]` if needed
- Execute requested work
- Write reply mail to target inbox
- Move source mail to `read` folder

## Failure Handling

- If mailbox path does not exist, create missing `read` folder before move.
- If move fails, report exact path and error, then ask user for direction.
- Never delete mail files directly; always move to `read` for traceability.
