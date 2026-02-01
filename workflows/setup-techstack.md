---
description: 設定專案技術棧 - 詢問並更新所有 AGENTS.md 檔案中的技術棧資訊
---

## 🎯 目的
透過 `/discussion` 流程，收集專案的技術棧選擇，並記錄到 `docs/tech-stack.md`。

## ⚠️ 重要原則
- **使用 /discussion 流程**：透過單一討論檔案收集所有技術棧資訊
- **必須停下來等待**：產生討論檔案後，必須等待使用者回覆
- **只記錄到 docs/tech-stack.md**：不更新 AGENTS.md（由 `/setup-agents` 負責）

## 🔗 執行順序
此 workflow 是四階段初始化流程的第二階段：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ← 你在這裡
3. `/setup-structure` - 建立 src/ 目錄結構
4. `/setup-agents` - 建立 AGENTS.md

---

## 📋 執行步驟

### 1. 建立技術棧討論檔案

在 `discussions/` 資料夾建立討論檔案：

**檔案命名格式：**
```
discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md
```

**檔案內容：**
```markdown
# 討論主題：專案技術棧設定

## 📋 背景說明
設定專案使用的技術棧，這些資訊將會記錄到 `docs/tech-stack.md`。

---

## ❓ 問題 1：選擇設定方式

**[P] 使用 Preset（推薦）**
快速選擇預設組合，可在下方微調

**[C] 自訂**
跳過 Preset，直接填寫下方所有問題

答：

---

## ❓ 問題 2：選擇 Preset（如果問題 1 選 P）

| # | Preset 名稱 | 後端 | 前端 | 建議使用情境 |
|---|------------|------|------|------------|
| 1 | fullstack-python-vue | Python + FastAPI | Vue 3 + Pinia + Vite | 漸進式框架，適合中小型 SPA、管理後台、內部工具 |
| 2 | fullstack-python-react | Python + FastAPI | React + Zustand + Vite | 生態系最大，適合需要豐富第三方套件的專案 |
| 3 | fullstack-python-astro | Python + FastAPI | Astro + React + Zustand | 內容導向網站、部落格、文件站、SEO 優先專案 |
| 4 | backend-only | Python + FastAPI | 無 | 純 API 服務、微服務、CLI 工具 |
| 5 | frontend-only | 無 | Vue 3 + Pinia + Vite | 純靜態網站、使用外部 API 的前端專案 |

> 詳細比較請參考 `docs/techstack-presets-comparison.md`

答：（請輸入數字 1-5，如果問題 1 選 C 請填「跳過」）

---

## 📝 技術棧詳細設定

> **如果選了 Preset：** 以下已填入預設值，只需修改想調整的項目
> **如果選自訂：** 請填寫所有項目

### 🐍 後端 (Backend)

| 項目 | 預設值 (Preset 1) | 您的選擇 |
|------|------------------|----------|
| Python 版本 | 3.10 | |
| Web 框架 | FastAPI | |
| ORM | SQLAlchemy | |
| 資料庫 | SQLite | |
| 測試框架 | pytest | |

> 如果不使用後端，請填「無」

### 🖥️ 前端 (Frontend)

| 項目 | 預設值 (Preset 1) | 您的選擇 |
|------|------------------|----------|
| Node.js 版本 | 22 | |
| 套件管理器 | npm | |
| 框架 | Vue 3 | |
| 狀態管理 | Pinia | |
| UI 框架 | shadcn-vue | |
| 建置工具 | Vite | |
| 測試框架 | Vitest | |
| E2E 測試 | Playwright | |

> 如果不使用前端，請填「無」

### 🛠️ 開發工具

| 項目 | 預設值 | 您的選擇 |
|------|--------|----------|
| 格式化 (前端) | Prettier | |
| 格式化 (後端) | Ruff | |
| Linter (前端) | ESLint | |
| Linter (後端) | Ruff | |
| CI/CD | GitHub Actions | |
| 容器化 | Docker | |

### 📝 Logging

| 項目 | 預設值 | 您的選擇 |
|------|--------|----------|
| Python Log 框架 | loguru | |
| TypeScript Log 框架 | winston | |
| Rust Log 框架 | tracing | |

> Preset 預設使用上述框架，如需變更請填寫「您的選擇」欄位

---

## ⏳ 狀態
- [ ] 等待回答
- [ ] 已回答，待處理
```

### 2. 通知使用者並停止

告訴使用者：

```
我已建立技術棧討論檔案：`discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md`

請在檔案中回答問題：
1. 選擇 Preset 或自訂
2. 如果選 Preset，填入數字
3. 在表格中填入「您的選擇」欄位（只需填想修改的項目）

完成後，請告訴我「我已回答」。

⚠️ 在您回答之前，我不會執行任何動作。
```

**然後完全停止，不執行任何其他動作。**

### 3. 等待使用者回覆
- 使用者會說「我已回答」或類似的話
- **只有在使用者明確表示已回答後，才繼續下一步**

### 4. 讀取並處理結果

讀取討論檔案，根據使用者的選擇：

1. **判斷 Preset 或自訂**
2. **載入 Preset 預設值（如適用）**
3. **套用使用者的修改**
4. **顯示最終配置摘要，請使用者確認**

---

## 📦 Preset 預設值參考

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
logging:
  python: "loguru"
  typescript: "winston"
  rust: "tracing"
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
logging:
  python: "loguru"
  typescript: "winston"
  rust: "tracing"
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
logging:
  python: "loguru"
  typescript: "winston"
  rust: "tracing"
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
logging:
  python: "loguru"
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
logging:
  typescript: "winston"
```

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

## Logging

- **Python**: {框架}
- **TypeScript**: {框架}
- **Rust**: {框架}
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
3. 只需一張問卷，一次完成所有設定
4. 可以重複執行此 workflow 來更新技術棧
5. Preset 詳細比較請參考 `docs/techstack-presets-comparison.md`
