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
