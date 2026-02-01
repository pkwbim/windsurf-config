---
description: 初始化 Monorepo 專案（引導流程）
---

## 🎯 目的

這是 Monorepo 專案初始化的**入口 workflow**，引導你按正確順序執行各個初始化步驟。

## 📚 使用說明

詳細說明請參考：`.windsurf/docs/workflow-guide.md`

---

## 📋 初始化流程

### 完整流程（7 個階段）

| 順序 | Workflow | 用途 | 預估時間 |
|------|----------|------|----------|
| 1 | `/setup-project-info` | 建立非技術目錄 | 1 分鐘 |
| 2 | `/setup-techstack` | 設定技術棧（需回答問卷） | 3-5 分鐘 |
| 3 | `/setup-structure` | 建立 src/ 目錄結構 | 1 分鐘 |
| 4 | `/setup-logging` | 產生 logging 程式碼（可選） | 1 分鐘 |
| 5 | `/setup-agents` | 建立 AGENTS.md | 2 分鐘 |
| 6 | `/setup-makefile` | 建立 Makefile 和 .env | 1 分鐘 |
| 7 | `/setup-sample-project` | 建立 Hello World 範例 | 2 分鐘 |

---

## 🚀 快速開始

請告訴我你的情況：

### [A] 全新專案
從頭開始，執行完整流程 1-5

### [B] 已有目錄結構，只需設定技術棧
執行 2-4（跳過目錄建立）

### [C] 只更新 AGENTS.md
執行 4（技術棧已設定）

### [D] 只建立 Makefile
執行 5

### [E] 查看目前狀態
檢查哪些步驟已完成

---

## 📊 狀態檢查

執行以下指令檢查初始化狀態：

// turbo
```python
from pathlib import Path

checks = [
    ("1. 非技術目錄", ["pm/planning", "policies", "management"]),
    ("2. 技術棧設定", ["docs/tech-stack.md"]),
    ("3. src/ 結構", ["src/core", "src/contracts", "src/apps", "src/storage"]),
    ("4. Logging 程式碼", ["src/shared/logging"]),
    ("5. AGENTS.md", ["AGENTS.md", "src/AGENTS.md"]),
    ("6. Makefile", ["Makefile"]),
    ("7. Sample Project", ["src/apps/web/src/stores/apiStore.ts", "src/apps/backend/.env"]),
]

print("📊 專案初始化狀態\n")
for name, paths in checks:
    all_exist = all(Path(p).exists() for p in paths)
    status = "✅" if all_exist else "❌"
    print(f"{status} {name}")

print("\n提示：選擇上方選項 [A-E] 開始初始化")
```

---

## 📝 各階段說明

### 階段 1：`/setup-project-info`
建立非技術相關的目錄結構：
- `management/` - 私有經營層級
- `pm/` - 產品管理
- `policies/` - 公司規定
- `enterprise/` - 企業版
- 其他輔助目錄

### 階段 2：`/setup-techstack`
透過問卷設定技術棧：
- 選擇 Preset 或自訂
- 設定後端（Python/FastAPI 等）
- 設定前端（Vue/React/Astro 等）
- 結果寫入 `docs/tech-stack.md`

**⚠️ 此階段會停下來等你回答問卷**

### 階段 3：`/setup-structure`
根據技術棧建立 src/ 目錄：
- `src/contracts/` - 共享契約
- `src/core/` - DDD 三層架構
- `src/apps/` - 介面層（backend, web）
- `src/logs/` - Log 輸出目錄
- `src/shared/logging/` - Log 程式碼目錄

### 階段 4：`/setup-logging`（可選）
根據技術棧產生 logging 程式碼：
- Python: `loguru` + SQLite handler
- TypeScript: `winston` + SQLite transport
- Rust: `tracing` + SQLite layer

### 階段 5：`/setup-agents`
建立所有 AGENTS.md 規範檔案：
- 根目錄 AGENTS.md
- 各層級 AGENTS.md
- 內容根據技術棧動態調整

### 階段 6：`/setup-makefile`
建立 Makefile 和依賴檔案：
- Python 虛擬環境管理
- 前後端開發指令
- `make dev` 一鍵啟動
- `make dev-remote` 遠端開發指令
- `.env.example` 和 `.env` 檔案

### 階段 7：`/setup-sample-project`
建立完整的 Hello World 範例：
- Backend API（含 logging）
- Frontend 首頁（含 Zustand store）
- 前後端串接驗證
- `src/storage/` 目錄結構

---

## 🔧 故障排除

### 問題：不確定從哪裡開始
選擇 **[E] 查看目前狀態**，系統會告訴你哪些步驟已完成。

### 問題：技術棧設定錯誤
重新執行 `/setup-techstack`，然後執行 `/setup-agents` 更新 AGENTS.md。

### 問題：目錄結構不對
重新執行 `/setup-structure`，此 workflow 是冪等的。

---

## 📚 相關資源

- `.windsurf/docs/workflow-guide.md` - 完整使用指南
- `.windsurf/templates/` - 各種模板檔案
- `docs/tech-stack.md` - 技術棧設定（執行階段 2 後產生）
