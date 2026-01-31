---
description: 設定專案技術棧 - 詢問並更新所有 AGENTS.md 檔案中的技術棧資訊
---

## 🎯 目的
透過 preset 或自訂流程，收集專案的技術棧選擇，並記錄到 `docs/tech-stack.md`。

## ⚠️ 重要原則
- **先問 preset 還是自訂**：讓使用者快速選擇
- **Preset 可微調**：選擇 preset 後可調整細節
- **只記錄到 docs/tech-stack.md**：不更新 AGENTS.md（由 `/setup-agents` 負責）

## 🔗 執行順序
此 workflow 是四階段初始化流程的第二階段：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ← 你在這裡
3. `/setup-structure` - 建立 src/ 目錄結構
4. `/setup-agents` - 建立 AGENTS.md

---

## 📋 執行步驟

### 1. 詢問使用 Preset 還是自訂

向使用者顯示以下選項：

```
🛠️ 技術棧設定

請選擇設定方式：

**[P] 使用 Preset（推薦）**
快速選擇預設組合，可微調細節

**[C] 自訂**
從頭填寫技術棧問卷

請輸入 P 或 C：
```

---

## 🅿️ Preset 流程

### P-1. 顯示 Preset 清單

如果使用者選擇 Preset，顯示以下清單：

```
📦 可用的 Preset

| # | Preset 名稱 | 後端 | 前端 |
|---|------------|------|------|
| 1 | fullstack-python-vue | Python + FastAPI | Vue 3 + Pinia + Vite |
| 2 | fullstack-python-react | Python + FastAPI | React + Zustand + Vite |
| 3 | fullstack-python-astro | Python + FastAPI | Astro + React + Zustand |
| 4 | backend-only | Python + FastAPI | 無 |
| 5 | frontend-only | 無 | Vue 3 + Pinia + Vite |

> 詳細比較請參考 `docs/techstack-presets-comparison.md`

請輸入數字 (1-5)：
```

### P-2. 載入 Preset 預設值

根據選擇載入對應的預設值：

**Preset 1: fullstack-python-vue**
```yaml
backend:
  python_version: "3.10"
  web_framework: "FastAPI"
  orm: "SQLAlchemy"
  database: "SQLite"
  test_framework: "pytest"
frontend:
  node_version: "22"
  package_manager: "npm"
  framework: "Vue 3"
  state_management: "Pinia"
  ui_framework: "shadcn-vue"
  build_tool: "Vite"
  test_framework: "Vitest"
  e2e_test: "Playwright"
tools:
  formatter_frontend: "Prettier"
  formatter_backend: "Ruff"
  linter_frontend: "ESLint"
  linter_backend: "Ruff"
  ci_cd: "GitHub Actions"
  container: "Docker"
```

**Preset 2: fullstack-python-react**
```yaml
backend:
  python_version: "3.10"
  web_framework: "FastAPI"
  orm: "SQLAlchemy"
  database: "SQLite"
  test_framework: "pytest"
frontend:
  node_version: "22"
  package_manager: "npm"
  framework: "React 19"
  state_management: "Zustand"
  ui_framework: "shadcn/ui"
  build_tool: "Vite"
  test_framework: "Vitest"
  e2e_test: "Playwright"
tools:
  formatter_frontend: "Prettier"
  formatter_backend: "Ruff"
  linter_frontend: "ESLint"
  linter_backend: "Ruff"
  ci_cd: "GitHub Actions"
  container: "Docker"
```

**Preset 3: fullstack-python-astro**
```yaml
backend:
  python_version: "3.10"
  web_framework: "FastAPI"
  orm: "SQLAlchemy"
  database: "SQLite"
  test_framework: "pytest"
frontend:
  node_version: "22"
  package_manager: "npm"
  framework: "Astro + React 19"
  state_management: "Zustand"
  ui_framework: "shadcn/ui"
  build_tool: "Astro"
  test_framework: "Vitest"
  e2e_test: "Playwright"
tools:
  formatter_frontend: "Prettier"
  formatter_backend: "Ruff"
  linter_frontend: "ESLint"
  linter_backend: "Ruff"
  ci_cd: "GitHub Actions"
  container: "Docker"
```

**Preset 4: backend-only**
```yaml
backend:
  python_version: "3.10"
  web_framework: "FastAPI"
  orm: "SQLAlchemy"
  database: "SQLite"
  test_framework: "pytest"
frontend: null
tools:
  formatter_backend: "Ruff"
  linter_backend: "Ruff"
  ci_cd: "GitHub Actions"
  container: "Docker"
```

**Preset 5: frontend-only**
```yaml
backend: null
frontend:
  node_version: "22"
  package_manager: "npm"
  framework: "Vue 3"
  state_management: "Pinia"
  ui_framework: "shadcn-vue"
  build_tool: "Vite"
  test_framework: "Vitest"
  e2e_test: "Playwright"
tools:
  formatter_frontend: "Prettier"
  linter_frontend: "ESLint"
  ci_cd: "GitHub Actions"
  container: "Docker"
```

### P-3. 顯示預設值並詢問是否微調

```
📦 已選擇 Preset: {preset_name}

預設配置：
┌─────────────────────────────────────┐
│ 後端 (Backend)                       │
├─────────────────────────────────────┤
│ Python: {python_version}             │
│ Web 框架: {web_framework}            │
│ ORM: {orm}                           │
│ 資料庫: {database}                   │
│ 測試: {test_framework}               │
├─────────────────────────────────────┤
│ 前端 (Frontend)                      │
├─────────────────────────────────────┤
│ Node.js: {node_version}              │
│ 框架: {framework}                    │
│ 狀態管理: {state_management}         │
│ UI: {ui_framework}                   │
│ 建置: {build_tool}                   │
│ 測試: {test_framework}               │
├─────────────────────────────────────┤
│ 工具                                 │
├─────────────────────────────────────┤
│ 格式化: {formatter}                  │
│ Linter: {linter}                     │
│ CI/CD: {ci_cd}                       │
│ 容器: {container}                    │
└─────────────────────────────────────┘

要微調任何項目嗎？
[Y] 是，我要調整一些項目
[N] 不用，直接使用這些設定

請輸入 Y 或 N：
```

### P-4. 微調流程（如果選 Y）

```
🔧 微調設定

請輸入要修改的項目（可多選，用逗號分隔）：

後端：
1. Python 版本 (目前: {python_version})
2. 資料庫 (目前: {database})

前端：
3. Node.js 版本 (目前: {node_version})
4. UI 框架 (目前: {ui_framework})

例如輸入「1,3」修改 Python 版本和 Node.js 版本
輸入「done」完成微調

請輸入：
```

對於每個選擇的項目，詢問新的值：
```
Python 版本 (目前: 3.10)
可選：3.10、3.11、3.12、3.13
請輸入新值：
```

### P-5. 確認最終配置

```
✅ 最終技術棧配置

{顯示最終配置表格}

確認以上配置？
[Y] 確認，寫入 docs/tech-stack.md
[N] 重新選擇

請輸入 Y 或 N：
```

---

## 🔧 自訂流程

### C-1. 建立技術棧討論檔案

如果使用者選擇自訂，使用 `/discussion` workflow 建立討論檔案：

**檔案命名格式：**
```
discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md
```

**檔案內容：**
```markdown
# 討論主題：專案技術棧設定

## 📋 背景說明
設定專案使用的技術棧，這些資訊將會記錄到 `docs/tech-stack.md`。

## ❓ 技術棧問卷

### 🐍 Python 相關

**問題 1：Python 版本**
例：3.10、3.11、3.12、3.13

答：

---

**問題 2：Web 框架**
例：FastAPI、Django、Flask、無

答：

---

**問題 3：ORM**
例：SQLAlchemy、Tortoise ORM、無

答：

---

**問題 4：資料庫**
例：PostgreSQL、MySQL、SQLite、MongoDB

答：

---

**問題 5：測試框架**
例：pytest、unittest

答：

---

### 📦 TypeScript/Node.js 相關

**問題 6：Node.js 版本**
例：20、22

答：

---

**問題 7：套件管理器**
例：npm、pnpm、yarn、bun

答：

---

### 🖥️ 前端框架（選一個主要框架）

**問題 8：前端框架**
例：Vue 3、React 19、Astro + React、無

答：

---

**問題 9：狀態管理**
例：Pinia (Vue)、Zustand (React)、無

答：

---

**問題 10：UI 框架**
例：shadcn/ui、shadcn-vue、Element Plus、Vuetify、無

答：

---

**問題 11：建置工具**
例：Vite、Astro、無

答：

---

**問題 12：前端測試框架**
例：Vitest、Jest、無

答：

---

**問題 13：E2E 測試**
例：Playwright、Cypress、無

答：

---

### 🛠️ 開發工具

**問題 14：程式碼格式化**
例：Prettier (前端)、Ruff (後端)

答：

---

**問題 15：Linter**
例：ESLint (前端)、Ruff (後端)

答：

---

**問題 16：CI/CD**
例：GitHub Actions、GitLab CI、無

答：

---

**問題 17：容器化**
例：Docker、無

答：

---

## ⏳ 狀態
- [ ] 等待回答
- [ ] 已回答，待處理
```

### C-2. 通知使用者並停止

```
我已建立技術棧討論檔案：`discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md`

請在檔案中回答所有問題。完成後，請告訴我「我已回答」。

⚠️ 在您回答之前，我不會執行任何動作。
```

**然後完全停止，等待使用者回覆。**

### C-3. 讀取並確認

使用者說「我已回答」後，讀取討論檔案並顯示摘要，請使用者確認。

---

## 📝 寫入 docs/tech-stack.md

確認後，將技術棧資訊寫入 `docs/tech-stack.md`：

```markdown
# 技術棧

> 建立日期：{日期}
> 來源：{preset 名稱 或 自訂}

## 後端 (Backend)

### Python
- **版本**: {版本}
- **Web 框架**: {框架}
- **ORM**: {ORM}
- **資料庫**: {資料庫}
- **測試框架**: {測試框架}

## 前端 (Frontend)

### Node.js
- **版本**: {版本}
- **套件管理器**: {套件管理器}

### {框架名稱}
- **版本**: {版本}
- **狀態管理**: {狀態管理}
- **UI 框架**: {UI框架}
- **建置工具**: {建置工具}
- **測試框架**: {測試框架}
- **E2E 測試**: {E2E}

## 開發工具

- **格式化 (前端)**: {工具}
- **格式化 (後端)**: {工具}
- **Linter (前端)**: {工具}
- **Linter (後端)**: {工具}
- **CI/CD**: {工具}
- **容器化**: {工具}
```

---

## ✅ 完成訊息

```
✅ 技術棧設定完成！

已更新的檔案：
- docs/tech-stack.md

下一步：
- 執行 `/setup-structure` 建立 src/ 目錄結構
- 執行 `/setup-agents` 建立 AGENTS.md
```

## 📝 注意事項

1. 此 workflow 只更新 `docs/tech-stack.md`
2. 不會更新 AGENTS.md（由 `/setup-agents` 負責）
3. 可以重複執行此 workflow 來更新技術棧
4. Preset 詳細比較請參考 `docs/techstack-presets-comparison.md`
