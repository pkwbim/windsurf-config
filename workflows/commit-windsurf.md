---
description: 提交 .windsurf submodule 變更並更新主專案引用
---

## 🎯 目的
將 `.windsurf/` 子專案的變更提交到 GitHub，並同步更新主專案的 submodule 引用。

## 📋 執行步驟

### 1. 檢查 .windsurf 子專案狀態
// turbo
```bash
cd .windsurf && git status
```

如果沒有變更，會顯示 "nothing to commit"，可以跳過後續步驟。

### 2. 查看變更內容
// turbo
```bash
cd .windsurf && git diff --stat
```

### 3. 暫存所有變更
// turbo
```bash
cd .windsurf && git add -A && git status
```

### 4. 提交變更

請根據變更內容，使用以下格式提交：

```bash
cd .windsurf && git commit -m "<type>: <description>

<詳細說明（可選）>"
```

**Commit 類型：**
- `feat`: 新功能（新增 workflow、skill、rule）
- `fix`: 修復問題
- `docs`: 文件更新
- `refactor`: 重構（不影響功能）
- `chore`: 雜項（更新依賴等）

**範例：**
```bash
cd .windsurf && git commit -m "feat: 新增 /commit-windsurf workflow

- 自動提交 .windsurf submodule
- 同步更新主專案引用"
```

### 5. 推送到 GitHub
```bash
cd .windsurf && git push origin main
```

### 6. 更新主專案的 submodule 引用
// turbo
```bash
git status .windsurf
```

如果顯示 `.windsurf (new commits)`，需要更新引用：

```bash
git add .windsurf && git commit -m "chore: update .windsurf submodule"
```

### 7. 推送主專案（可選）

如果需要同步推送主專案：
```bash
git push origin main
```

### 8. 驗證完成
// turbo
```bash
echo "=== .windsurf submodule ===" && cd .windsurf && git log -1 --oneline && echo "" && echo "=== 主專案 ===" && cd .. && git status .windsurf
```

## ✅ 完成訊息

```
✅ .windsurf submodule 已提交並推送！

已完成：
1. .windsurf/ 變更已提交到 GitHub
2. 主專案 submodule 引用已更新

下次其他人 clone 專案時，會拿到最新的 .windsurf/ 配置。
```

## 📝 注意事項

1. 此 workflow 需要有 GitHub 推送權限
2. 如果有衝突，需要先解決衝突再提交
3. 建議在提交前先檢查變更內容
