---
description: Auto-analyze changes and commit with AI-generated message
auto_execution_mode: 1
---

## Purpose
Automatically analyze staged/unstaged changes since last commit, generate a meaningful commit message, and commit.

## Steps

// turbo
1. Run `./scripts/commit-summary.sh` to get a concise summary of changes (saves LLM tokens)
2. Analyze the summary and generate a commit message following conventional commits format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks
   - `style:` for formatting changes
3. Stage all changes with `git add -A`
4. Execute `git commit -m "<message>"`

## Commit Message Format
```
<type>(<scope>): <subject>

<body>
```

## Notes
- Will analyze diff against HEAD (last commit)
- Commits all changes (staged + unstaged)
- Does not require manual confirmation of the commit message
