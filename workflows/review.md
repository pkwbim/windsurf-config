---
description: Extract learnings from discussions and archive to docs (post-build)
---

## 🎯 目的
每次 Story 完成後，執行 `/review` 以：
1. 整理技術決策和學習心得 → `pm/docs/`
2. **更新系統規格** → `pm/specs/`（永遠保持最新狀態）
3. 更新 checklist 並 commit

---

## 工作流程步驟

### 1. 確認前置條件
// turbo
```bash
git branch --show-current
cat pm/planning/02_active.md
```
- 確認 Backend 階段已完成（checklist 全部勾選）
- 取得 active_story ID

### 2. 掃描知識來源
// turbo
```bash
ls pm/planning/stories/{active_story}/discussions/
ls pm/planning/stories/{active_story}/decisions/
cat pm/planning/stories/{active_story}/checklist.md
```
- 讀取所有 decisions/ 文件，提取技術決策
- 讀取 checklist 確認完成項目

### 3. 更新技術知識文件（pm/docs/）
- 檢查 `pm/docs/` 是否有相關主題的文件
- **若已存在**：append 新的學習心得
- **若是新主題**：建立新文件

文件格式：
```markdown
# [主題標題]

## Context
[何時/為何此知識相關]

## Key Decisions
- [決策 1]：[理由]

## Common Issues & Solutions
| 問題 | 解法 |
|------|------|

## References
- Related Story: STORY-XXX
```

### 4. 更新系統規格（pm/specs/）⭐ 重要

> 此步驟確保 `pm/specs/` 永遠反映系統最新狀態。

// turbo
```bash
cat pm/planning/stories/{active_story}/spec.md
ls pm/specs/
```

**判斷此 Story 影響哪個 Bounded Context：**

| Story 類型 | 對應 Context 目錄 |
|-----------|-----------------|
| UserAuth | `pm/specs/user-auth/` |
| ProfileManagement | `pm/specs/profile-management/` |
| AstrologyChart | `pm/specs/astrology-chart/` |
| 新 Context | 建立新目錄 |

**每個 Context 的目錄結構：**
```
pm/specs/{context}/
├── spec.md          # 入口：功能摘要 + 連結
├── use-cases.md     # Use Cases 詳細描述
├── domain-model.md  # Entity、Value Object
└── routes.md        # 路由對照表（含 FormRequest、Middleware）
```

**更新規則：**
- `spec.md`：更新功能摘要、狀態、最後更新日期
- `use-cases.md`：新增或修改 Use Case 描述
- `domain-model.md`：新增或修改 Entity、Value Object（只記錄 DDD 概念層：Entity 名稱、業務方法、對應 BR）
- `routes.md`：新增或修改路由、FormRequest、Middleware

> **DB 欄位細節不在 `domain-model.md` 維護**，直接查 Migration 檔或執行 `php artisan db:show --json`。

> ⚠️ **specs 必須自給自足（Self-Contained）**：
> - 合併到 `pm/specs/` 的內容必須直接包含所有知識，**不得以 `pm/planning/stories/...` 路徑回參 story 文件**
> - 技術決策、計算公式、業務規則等，直接寫入 `pm/specs/` 對應檔案
> - `pm/specs/` 是系統的唯一真相來源（Single Source of Truth），讀者不需要再去翻 story 目錄

**若是全新 Context：**
- 建立目錄和 4 個檔案
- 更新 `pm/specs/README.md` 索引表

**更新 `pm/specs/glossary.md`：**
- 若此 Story 引入新的領域術語，加入術語表

**檢查 `pm/specs/AGENTS.md`：**
- 讀取現有內容，確認格式規範和更新規則是否仍然正確
- 若有新的 Context 類型或格式變更，更新對應說明

### 4b. 合併 Page Spec 到 pm/specs/ui/（若有新頁面）

// turbo
```bash
ls pm/planning/stories/{active_story}/pages/ 2>/dev/null || echo "無 page spec"
```

若 story 目錄下有 `pages/` 目錄：
- 將所有 `page-{name}.md` 複製到 `pm/specs/ui/pages/`
- 若 `pm/specs/ui/pages/` 不存在，先建立目錄
- 若同名檔案已存在，以 story 版本覆蓋（story 版本是最新的）

```bash
mkdir -p pm/specs/ui/pages
cp pm/planning/stories/{active_story}/pages/*.md pm/specs/ui/pages/
```

**Layout Spec 不需要複製**（`pm/specs/ui/layouts/` 是全域共用，只建立一次）

### 4c. 更新 pm/specs/AGENTS.md 與 README.md

// turbo
```bash
cat pm/specs/README.md
cat pm/specs/AGENTS.md
```

**若此 Story 建立了全新 Bounded Context：**

1. 更新 `pm/specs/README.md`：
   - 將對應 Context 的狀態從 `⬜ 待規劃` 改為 `✅ 完成`
   - 確認目錄路徑正確

2. 更新 `pm/specs/AGENTS.md` 的目錄結構圖：
   - 在 `{context}/` 區塊加入新建立的 context 目錄名稱

**若此 Story 引入新的資料查找路徑（如新的 ui/ 子目錄、新的規格類型）：**

3. 更新 `pm/specs/AGENTS.md` 的「AI 查找資料導引」表格：
   - 加入新的查找路徑說明，讓未來的 AI 知道去哪裡找資料

**目的：** 隨著 specs 愈來愈大，AGENTS.md 是 AI 的導覽地圖，必須保持最新。

### 5. 更新 checklist.md
勾選「文件更新完成」：
```markdown
- [x] 文件更新完成 (`/review`) ✅
```

### 6. Commit 所有變更
```bash
git add pm/ && git commit -m "docs(review): {story-id} review 完成

- 更新 pm/docs/（技術知識文件）
- 更新 pm/specs/{context}/（系統規格）"
```

### 7. 提示下一步
告知使用者：
```
✅ /review 完成！

## 更新內容
- pm/docs/：[更新了哪些文件]
- pm/specs/{context}/：[更新了哪些規格]

## 下一步
- 執行 `/merge` 合併到 main
```

---

## pm/specs/ 目錄說明

```
pm/specs/
├── README.md          # 索引：所有 Context 清單
├── glossary.md        # DDD 術語表（通用 + 本專案）
├── user-auth/         # Identity Bounded Context
│   ├── spec.md
│   ├── use-cases.md
│   ├── domain-model.md
│   └── routes.md
└── {future-context}/
    └── ...
```

## Notes
- 每次 `/build` 完成後執行
- `pm/specs/` 是系統的「活文件」，永遠反映最新實作狀態
- 技術決策放 `pm/docs/`，系統規格放 `pm/specs/`
