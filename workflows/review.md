---
description: Extract learnings from discussions and archive to docs (post-build)
auto_execution_mode: 1
---

## Purpose
After completing a `/build`, run `/review` to preserve important technical decisions and learnings for future reference.

## Steps

### 1. Scan Knowledge Sources
// turbo
```bash
ls -la discussions/
cat _planning/03_completed.md
```
- Identify discussion files related to the completed Story
- Review recently completed items in `03_completed.md` for design decisions

### 2. Extract Key Learnings
**From `discussions/` files:**
- Read the Q&A content
- Identify **technical decisions** made
- Identify **problems solved** and their solutions

**From `03_completed.md` entries:**
- Extract **設計決策** from the 學習心得 section
- Identify **架構模式** that were established
- Note **介面定義** (interfaces, types) that should be documented

**General:**
- Identify **patterns** that should be reused

### 3. Update or Create Knowledge Doc
- Check if a relevant doc exists in `docs/`
- **IF EXISTS:** Append new learnings to the existing doc
- **IF NEW TOPIC:** Create a new doc in `docs/` with format:
  ```
  # [Topic Title]
  
  ## Context
  [When/why this knowledge is relevant]
  
  ## Key Decisions
  - [Decision 1]: [Rationale]
  - [Decision 2]: [Rationale]
  
  ## Common Issues & Solutions
  | Issue | Solution |
  |-------|----------|
  | [Problem] | [Fix] |
  
  ## References
  - Source: `discussions/[filename].md`
  - Related Story: Story-XXX
  ```

### 4. Update Project Documentation
// turbo
```bash
cat CHANGELOG.md
cat README.md
```
- **CHANGELOG.md**: Add entry for the completed Story/Version
  - Include new features, fixes, and changes
- **README.md**: Update if there are new CLI commands, setup steps, or features

### 5. Update docs/README.md Index
// turbo
```bash
cat docs/README.md
```
- Add new doc to the index if created

### 6. Complete & Archive Task
// turbo
```bash
cat .windsurf/templates/completed-task.md
```
- **INSERT** the filled template into `_planning/03_completed.md` under the `## 已完成項目` heading (top of the list)
- **DO NOT** overwrite the file. Keep all existing completed items.
- Update `_planning/03_completed.md` statistics if applicable

### 7. Archive Active Task
Archive the completed task spec for future reference:
// turbo
```bash
# Get Story ID from 02_active.md title
STORY_ID=$(grep -oP 'Story-\d+' _planning/02_active.md | head -1)
DATE=$(date +%Y%m%d)
# Archive with date and story ID
mkdir -p _planning/archived
cp _planning/02_active.md "_planning/archived/${DATE}-${STORY_ID}-active.md"
```
- Then reset `02_active.md` to template state:
// turbo
```bash
cp .windsurf/templates/story.md _planning/02_active.md
```

### 8. Archive Discussion (Optional)
- Ask user: "Move processed discussions to `discussions/archived/`?"
- If yes, move the files

## Example Output

After running `/review` on Story-001, you might create:
- `docs/monorepo-architecture.md` - Core logic sharing patterns
- `docs/esm-commonjs-compatibility.md` - Module format decisions

## Notes
- Run this after every `/build` completion
- Focus on **reusable knowledge**, not story-specific details
- Keep docs concise and actionable
