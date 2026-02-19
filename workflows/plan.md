---
description: 將想法轉換為規格（包含澄清檢查）
---

## ⚠️ 重要：此工作流程僅撰寫規格。不要開始寫程式。

> **執行此 workflow 前，必須先載入 `plan` skill 的規範。**
> 參考 `.windsurf/skills/plan/SKILL.md` 取得 Use Case 格式、業務規則格式、DDD 分析方法。

## 📁 Story 目錄結構說明

每個 story 有獨立目錄，所有相關事務集中管理：

```
pm/planning/stories/
├── AGENTS.md                        # 所有 story 狀態總覽
└── STORY-{流水號}-{CamelCase描述}/   # 每個 story 的目錄
    ├── use-cases.md                  # Use Case 清單（先產生並確認）
    ├── business-rules.md             # 業務規則（確認 use-cases 後產生）
    ├── spec.md                       # 技術規格（確認 use-cases 後產生）
    ├── discussions/                  # 此 story 相關的討論問卷
    │   └── DISC-YYYYMMDDHHMM-{主題}.md
    └── decisions/                    # 此 story 相關的決策文件
        └── DEC-YYYYMMDDHHMM-{主題}.md
```

**⚠️ 重要：若在 story 執行期間使用 `/discussion`，問卷和決策文件應放在 story 目錄的 `discussions/` 和 `decisions/` 下，而非全域 `discussions/` 目錄。**

---

## 步驟 0：Git Branch Setup

// turbo
```bash
git branch --show-current
```
- 如果目前在 `main`：建立並切換到 `feat/<story-id>` 分支（例如 `feat/story-003`）
- 如果已在 feature 分支：沿用現有分支

---

## 步驟 1：讀取資料

// turbo
```bash
cat pm/planning/01_backlog.md
cat pm/planning/stories/AGENTS.md
cat docs/tech-stack.md
```

// turbo
```bash
cat pm/specs/README.md
cat pm/specs/glossary.md
```

**讀取 pm/specs/ 的目的：**
- 了解系統目前已有哪些 Bounded Context 和功能
- 確認新 Story 是否與既有 Context 有依賴關係（Shared Kernel、跨 BC 呼叫）
- 避免重複設計已存在的 Domain Model 或路由
- 若新 Story 屬於既有 Context，讀取對應的 `pm/specs/{context}/` 目錄下所有檔案

---

## 步驟 2：與使用者確認故事選擇

- 提問：「您想要規劃 Story-XXX，對嗎？」
- 等待使用者確認後再繼續。

---

## 步驟 3：澄清需求與規模評估

仔細審查使用者故事，依序判斷：

### 3a. 需求是否清楚？
- **問自己：**範圍是否 100% 清楚？Actor 是誰？主要操作是什麼？
- **如有任何疑問：**執行 `/discussion` workflow，**問卷放在全域 `discussions/questionnaires/` 下**（此時 story 目錄尚未建立），然後**停止**，等待使用者回覆後再繼續。
- **如果清楚：**繼續 3b。

### 3b. Story 規模是否合適？

**判斷標準（符合任一條即視為太大）：**
- 預估 Use Case 超過 6 個
- 涉及 3 個以上不同的 Bounded Context
- 預估開發時間超過 1 週

**如果 story 太大：**
1. 建議拆分方案，例如：
   ```
   原 Story：[原標題]
   建議拆分為：
   - 子 Story A：[標題] - [說明]
   - 子 Story B：[標題] - [說明]
   - 子 Story C：[標題] - [說明]（可選，加入 backlog）
   ```
2. 等待使用者確認拆分方案
3. 確認後：
   - 將子 Story 加入 `pm/planning/01_backlog.md`
   - 從 `pm/planning/01_backlog.md` 移除原 story（或標記為 `[已拆分]`）
   - Commit 並 merge 回 main（backlog 是共用資源，應在 main 上）：
     ```bash
     git add pm/planning/01_backlog.md
     git commit -m "plan: 拆分 [原 Story 標題] 為子 Story"
     git checkout main
     git merge [原 feature branch 名稱]
     git push origin main
     git branch -d [原 feature branch 名稱]
     ```
   - 告訴使用者：「原 Story 已拆分完畢，子 Story 已加入 backlog，並已 merge 回 main。請選擇要先規劃哪個子 Story，再重新執行 `/plan`（會從 main 建立新 branch）。」
   - **停止，不繼續建立目錄或規格。**

**如果規模合適：**繼續步驟 4。

---

## 步驟 4：初始化 Story 目錄

- 決定 Story ID（查看 `pm/planning/stories/AGENTS.md` 取得下一個流水號）
- 目錄命名格式：`STORY-{流水號}-{CamelCase描述}`（例如 `STORY-001-UserLogin`）
- 建立以下結構：
  ```
  pm/planning/stories/STORY-{流水號}-{CamelCase描述}/
  ├── discussions/     ← 空目錄
  └── decisions/       ← 空目錄
  ```
- 更新 `pm/planning/02_active.md`：
  ```yaml
  ---
  active_story: STORY-{流水號}-{CamelCase描述}
  active_story_dir: pm/planning/stories/STORY-{流水號}-{CamelCase描述}/
  ---

  # 🚀 Active

  目前執行中：**STORY-{流水號}-{CamelCase描述}**
  規格文件：`pm/planning/stories/STORY-{流水號}-{CamelCase描述}/`
  ```
- 將故事從 `pm/planning/01_backlog.md` 移除

---

## 步驟 5：產生 use-cases.md（並等待確認）

依照 `plan` skill 的 Use Case 格式，在 story 目錄產生 `use-cases.md`：

**分析重點：**
- 識別所有 Actor（使用者角色）
- 列出每個 Actor 的主要目標 → 每個目標對應一個 Use Case
- 為每個 Use Case 寫出主要流程、替代流程、例外流程
- 參考 skill 的「Use Case 完整性檢查」自我檢查

**產生後：**
告訴使用者：
```
我已產生 Use Cases：`pm/planning/stories/STORY-XXX/use-cases.md`

請確認：
1. Actor 是否正確？
2. Use Case 是否完整？有沒有遺漏的操作？
3. 流程描述是否符合預期？

確認後請告訴我「Use Cases 確認」，我將繼續產生技術規格。
```

**完全停止，等待使用者確認。**

---

## 步驟 6：產生 business-rules.md、spec.md 和 checklist.md

使用者確認 Use Cases 後，**同時產生**以下三個文件：

### 6a. business-rules.md
依照 `plan` skill 的業務規則格式：
- 從 Use Case 的前置條件、例外流程中萃取業務規則
- 為每條規則標記分類（驗證/限制/計算/狀態）
- 每條規則標記對應的 Entity 或 Value Object
- 參考 skill 的「業務規則完整性檢查」自我檢查

### 6b. spec.md
依照 `.windsurf/templates/story-spec.md` 格式，進行 DDD 分析：

### 6c. checklist.md
依照 `.windsurf/templates/story-checklist.md` 格式，填入 Story ID 和標題。
此文件追蹤開發進度，在後續 `/build`、`/review`、`/merge` 過程中持續更新。

### 6d. e2e-scenarios.md
依照 `.windsurf/templates/story-e2e-scenarios.md` 格式和 `plan` skill 的 E2E 劇本規範：
- 從 `use-cases.md` 的主要流程 → 產生正向劇本（每個 UC 至少一個）
- 從 `use-cases.md` 的例外流程 + `business-rules.md` → 產生負向劇本
- 每個劇本的操作步驟要具體可執行，URL 來自 `spec.md` 路由表格
- 預期結果必須是可程式驗證的（URL、DOM 元素、文字內容）
- 參考 skill 的「E2E 劇本完整性檢查」自我檢查

### 6e. pages/（Page Spec 文件）

為此 Story 涉及的每個**新頁面**建立 page spec 文件：

**目錄位置（Story 執行期間）：**
```
pm/planning/stories/{story}/pages/page-{name}.md
```

**命名規則：** `page-{url-path-with-dashes}.md`
- `/profiles` → `page-profiles-index.md`
- `/profiles/create` → `page-profiles-create.md`
- `/profiles/{id}` → `page-profiles-show.md`

**Page Spec 格式：**
```markdown
# Page Spec: {url}

## 基本資訊
- **URL**: /path
- **Layout**: auth | guest
- **Blade**: `resources/views/{path}.blade.php`
- **對應 UC**: UC-XX

## Areas 內容

### Area: content
#### Block 1: {區塊名稱}
[說明或欄位表格]

#### Block 2: {區塊名稱}
| 欄位 | 資料來源 | 說明 |
|------|---------|------|

## 🧪 可測試性規範

> **⚠️ 此區塊為必填**，`build-laravel-ui` 實作時必須依此加上 `data-*` 屬性，`integration-e2e` 撰寫測試前必須讀此區塊確認 selector。

### 列表行定位
| 元素 | data-* 屬性 | 說明 |
|------|------------|------|
| 列表每行 | `:data-{entity}-name="{item.name}"` | Alpine.js 動態綁定，供 Playwright 定位特定行 |

### 操作按鈕/連結
| 元素 | 屬性 | 值 |
|------|------|-----|
| 編輯連結 | `title` | `"編輯"` |
| 刪除按鈕 | `title` | `"刪除"` |
| 其他操作 | `title` | `"操作名稱"` |

### 其他可測試元素
[列出此頁面特有的需要定位的元素，例如 modal、tab、狀態標籤等]
```

> **規範說明：**
> - `data-*` 屬性不影響視覺呈現，是 HTML 標準屬性
> - Alpine.js 動態綁定用 `:data-xxx="value"`，Playwright 在 `networkidle` 後可正確讀取
> - 操作按鈕用 `title` 屬性，Playwright 用 `locator('button[title="刪除"]')` 定位

**Layout 參考：**
- `pm/specs/ui/layouts/layout-auth.md`（已登入頁面）
- `pm/specs/ui/layouts/layout-guest.md`（訪客頁面）

**只需為「有業務判斷的頁面」建立 page spec：**
- ✅ 列表頁（欄位選擇有業務意義）
- ✅ 詳情頁（顯示哪些資訊有業務意義）
- ✅ 首頁/行銷頁（文案和區塊結構）
- ⬜ 表單頁（欄位直接對應 FormRequest，不需重複定義）

**Domain Design（參考 plan skill 的 DDD 分析方法）：**
- 識別 Bounded Context 和 Aggregate Root
- 設計 Entities（對應 BR 規則）
- 設計 Value Objects（封裝驗證規則）
- 列出 Application Use Cases（對應 use-cases.md 的 UC）
- 定義 Protocols 和 DTOs

**Backend：**
- Repository 介面
- DB Model 和欄位設計
- API 端點表格（含對應 UC）

**Frontend：**
- 頁面與路由表格（含 URL 和對應 UC）
- 元件清單

**Testing Criteria：**
- Backend Unit / Integration Tests
- Frontend Tests
- Manual Testing

---

## 步驟 7：AI 自動檢查範圍完整性

產生文件後，AI 自動執行以下檢查並輸出結果：

```markdown
## 範圍檢查結果

### Use Case 完整性
✅/⚠️ Actor 識別：[說明]
✅/⚠️ CRUD 完整性：[說明]
✅/⚠️ 例外流程：[說明]

### 業務規則完整性
✅/⚠️ 輸入驗證：[說明]
✅/⚠️ 狀態規則：[說明]
✅/⚠️ 業務限制：[說明]

### DDD 架構
✅/⚠️ Bounded Context：[說明]
✅/⚠️ Entity 設計：[說明]
✅/⚠️ Value Object：[說明]
✅/⚠️ Protocol/DTO：[說明]

### 功能完整性
✅/⚠️ API 端點：[說明]
✅/⚠️ 頁面/路由：[說明]
✅/⚠️ DB 設計：[說明]

### E2E 劇本
✅/⚠️ 正向劇本：[說明]
✅/⚠️ 負向劇本：[說明]
✅/⚠️ 預期結果可驗證：[說明]

### 發現的潛在遺漏
1. [遺漏項目] - 建議：[立即加入 / 加入 backlog]
```

詢問使用者：「我檢查了規格，發現以上潛在遺漏。是否需要調整？」
- 如需調整核心功能：更新對應文件
- 如是非核心功能：記錄到 `pm/planning/01_backlog.md`
- 不確定時：執行 `/scope` 協助判斷

---

## 步驟 8：更新 stories/AGENTS.md

在狀態總覽表格新增此 story 的一列：
```
| STORY-{流水號}-{CamelCase描述} | [標題] | [簡短描述] | `planning` | YYYY-MM-DD | - |
```

---

## 步驟 9：在此停止

告訴使用者：
```
規格已準備就緒：
- Use Cases：`pm/planning/stories/STORY-XXX/use-cases.md`
- 業務規則：`pm/planning/stories/STORY-XXX/business-rules.md`
- 技術規格：`pm/planning/stories/STORY-XXX/spec.md`
- 開發進度：`pm/planning/stories/STORY-XXX/checklist.md`
- E2E 劇本：`pm/planning/stories/STORY-XXX/e2e-scenarios.md`

當您想開始實作時，執行 `/build` 系列，如 `/build-ui`, `/build-contract`, `/build-backend`, `/build-laravel-ui`, `/build-laravel-contract`, `/build-laravel-backend`。
```

**不要撰寫任何程式碼。**

---

## 備註
- 必須載入 `plan` skill（`.windsurf/skills/plan/SKILL.md`）
- `02_active.md` 只作為指標，詳細規格在 story 目錄下
- 每個 story 同時只有一個進行中
- `use-cases.md` 確認後才能產生 `business-rules.md` 和 `spec.md`
- **此工作流程在規格撰寫結束。實作是另一個工作流程（`/build`）。**