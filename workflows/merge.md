---
description: Merge feature branch back to main after build completion
auto_execution_mode: 1
---

## Purpose
After completing `/review`, run `/merge` to safely merge the feature branch back to `main`.

## Pre-requisites
確認已完成 `/review`：
- Story 已歸檔到 `_planning/03_completed.md`
- `_planning/02_active.md` 已清空
- 所有文件已更新

## Commit Check（重要）
在執行 merge 前，請先確認 working tree 乾淨：
- 若還有未提交的變更（staged/unstaged），**先執行 `/commit`** 產生並提交本次變更
- 確認 `git status` 顯示乾淨後，再繼續執行 `/merge`

## Usage
```bash
./scripts/merge.sh
```

## What it does
1. Verify on feature branch (abort if on `main`)
2. Run Frontend tests (abort if fail)
3. Run Backend tests (abort if fail)
4. Rebase from `origin/main`
5. Switch to `main` and pull
6. Merge with `--no-ff`
7. Push to remote
8. Delete local feature branch

## Notes
- Script will abort on any failure
- Resolve rebase conflicts manually if needed, then re-run
- **Story 歸檔由 `/review` 負責，不是 `/merge`**
- `/merge` 只負責 Git 分支合併操作
