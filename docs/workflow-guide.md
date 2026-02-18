# 📚 Workflow 使用指南

> 本文件說明如何使用 Monorepo 初始化相關的 workflows。

---

## 🎯 快速參考

| Workflow | 用途 | 何時使用 |
|----------|------|----------|
| `/discussion` | 純討論與澄清流程 | 需要釐清需求、做決策、討論方向時 |
| `/plan` | 將想法轉換為規格 | 要開始一個新 story 時 |
| `/init` | 引導流程入口 | **第一次使用時從這裡開始** |
| `/setup-project-info` | 建立非技術目錄 | 新專案初始化 |
| `/setup-techstack` | 設定技術棧 | 新專案或更換技術棧 |
| `/setup-structure` | 建立 src/ 目錄 | 新專案或重建目錄 |
| `/setup-logging` | 產生 logging 程式碼 | 新專案或需要統一 log |
| `/setup-agents` | 建立 AGENTS.md | 新專案或更新規範 |
| `/setup-makefile` | 建立 Makefile | 需要開發環境指令 |

---

## 🚀 新專案初始化

### 方法 1：使用引導流程（推薦）

```
/init
```

系統會引導你選擇適合的初始化路徑。

### 方法 2：手動按順序執行

```
/setup-project-info    # 1. 建立目錄
/setup-techstack       # 2. 設定技術棧（會停下來等你回答）
/setup-structure       # 3. 建立 src/
/setup-logging         # 4. 產生 logging 程式碼（可選）
/setup-agents          # 5. 建立 AGENTS.md
/setup-makefile        # 6. 建立 Makefile
```

---

## 📋 各 Workflow 詳細說明

### `/discussion` - 純討論與澄清流程

**用途**：需要釐清需求、做決策、或討論方向時使用。與其他 workflow 完全獨立。

**依賴 Skill**：`.windsurf/skills/discussion/SKILL.md`

**目錄結構**：
```
discussion/
├── questionnaires/    # 問卷檔案（DISC-YYYYMMDDHHMM-{主題}.md）
└── decisions/         # 結論文件（DEC-YYYYMMDDHHMM-{主題}.md）
```

**流程**：
1. 載入 discussion skill 規範
2. 判斷是否需要開問卷
3. 建立問卷 → 等待使用者回答
4. 讀取回答 → 判斷是否需要追問（同一問卷追加）或開新問卷
5. 產生決策文件，更新問卷 status 為 `closed`

**追問規則**：
- 同一主題的追問 → 在**同一個問卷末尾**追加，不開新檔
- 全新議題 → 開新問卷

---

### `/plan` - 將想法轉換為規格

**用途**：將 backlog 中的 story 轉換為詳細技術規格，建立 story 獨立目錄。

**依賴 Skill**：無（但若需要澄清，會呼叫 `/discussion`）

**Story 目錄結構**：
```
pm/planning/stories/
├── AGENTS.md                        # 所有 story 狀態總覽
└── STORY-{流水號}-{CamelCase描述}/
    ├── spec.md                       # 技術規格（主文件）
    ├── discussions/                  # 此 story 的討論問卷
    └── decisions/                    # 此 story 的決策文件
```

**流程**：
1. 讀取 backlog、stories/AGENTS.md、模板
2. 確認要規劃哪個 story
3. 需求不清楚時執行 `/discussion`（問卷放在 story 目錄下）
4. 建立 story 目錄（`STORY-{流水號}-{CamelCase描述}/`）
5. 撰寫 `spec.md` 技術規格（DDD 導向）
6. AI 自動檢查範圍完整性
7. 更新 `stories/AGENTS.md` 狀態表格
8. 停止，等待 `/build`

**重要規則**：
- `02_active.md` 只作為指標（front matter + 一行說明），詳細規格在 `spec.md`
- story 執行期間的 `/discussion` 問卷放在 story 目錄的 `discussions/` 下
- 每次只有一個 story 進行中

---

### `/init` - 引導流程入口

**用途**：不確定從哪開始時使用

**功能**：
- 檢查目前專案狀態
- 引導選擇適合的初始化路徑
- 提供狀態檢查

**選項**：
- `[A]` 全新專案 → 執行 1-5
- `[B]` 已有目錄，只需設定技術棧 → 執行 2-4
- `[C]` 只更新 AGENTS.md → 執行 4
- `[D]` 只建立 Makefile → 執行 5
- `[E]` 查看目前狀態

---

### `/setup-project-info` - 建立非技術目錄

**用途**：建立專案的非技術相關目錄結構

**建立的目錄**：
```
management/     # 私有經營層級
pm/             # 產品管理
policies/       # 公司規定
enterprise/     # 企業版
tools/          # 工具腳本
scripts/        # 自動化腳本
out/            # 輸出
discussions/    # 討論檔案
docs/           # 文件
src/            # 程式碼（空目錄）
.windsurf/      # 配置
```

**注意**：`logs/` 目錄已移至 `src/logs/`，由 `/setup-structure` 建立

**建立的檔案**：
- `AGENTS.md` - 最小版本（從模板複製）
- `docs/README.md` - 文件目錄索引
- `pm/planning/01_backlog.md`, `02_active.md`, `03_completed.md`

**注意**：此階段不建立 `src/` 的子目錄

---

### `/setup-techstack` - 設定技術棧

**用途**：透過問卷收集技術棧選擇

**流程**：
1. 建立討論檔案 `discussions/DISC-*-TechStackSetup.md`
2. **停下來等你回答**
3. 你回答後，寫入 `docs/tech-stack.md`

**Preset 選項**：

| # | 名稱 | 後端 | 前端 |
|---|------|------|------|
| 1 | fullstack-python-vue | Python + FastAPI | Vue 3 + Pinia |
| 2 | fullstack-python-react | Python + FastAPI | React + Zustand |
| 3 | fullstack-python-astro | Python + FastAPI | Astro + React |
| 4 | backend-only | Python + FastAPI | 無 |
| 5 | frontend-only | 無 | Vue 3 + Pinia |

**輸出**：`docs/tech-stack.md`

---

### `/setup-structure` - 建立 src/ 目錄

**用途**：根據技術棧建立程式碼目錄結構

**前置條件**：`docs/tech-stack.md` 必須存在

**建立的目錄**：
```
src/
├── contracts/          # 共享契約
│   ├── schemas/
│   ├── enums/
│   ├── errors/
│   ├── python/         # 如果使用 Python
│   └── typescript/     # 如果使用 TypeScript
├── core/               # DDD 三層
│   ├── domain/
│   ├── infrastructure/
│   └── application/
├── apps/               # 介面層
│   ├── backend/        # 如果使用後端
│   ├── web/            # 如果使用前端
│   ├── cli/
│   └── desktop/
├── logs/               # Log 輸出目錄（gitignore）
│   └── archive/        # 歸檔的舊 log
└── shared/
    └── logging/        # Log 程式碼
```

**動態調整**：
- 根據技術棧決定建立哪些語言目錄
- 前端目錄結構根據框架調整（Vue/React/Astro）

---

### `/setup-logging` - 產生 Logging 程式碼

**用途**：根據技術棧產生統一的 logging 程式碼

**前置條件**：`docs/tech-stack.md` 必須存在，`src/shared/logging/` 目錄必須存在

**產生的檔案**：

| 語言 | 框架 | 檔案 |
|------|------|------|
| Python | `loguru` | `logger.py`, `sqlite_handler.py` |
| TypeScript | `winston` | `logger.ts`, `sqlite-transport.ts` |
| Rust | `tracing` | `mod.rs`, `sqlite_layer.rs` |

**Log 規格**：
- 格式：`[YYYY-MM-DD HH:MM:SS] [LEVEL] [module] message`
- 輸出：stdout/stderr、文字檔案、SQLite
- 保留：30 天

**相關文件**：`docs/logging-strategy.md`

---

### `/setup-agents` - 建立 AGENTS.md

**用途**：建立所有層級的 AGENTS.md 規範檔案

**前置條件**：`docs/tech-stack.md` 必須存在

**建立的檔案**：
- `/AGENTS.md` - 全域規範
- `src/AGENTS.md` - 程式碼層
- `src/contracts/AGENTS.md` - 契約層
- `src/core/AGENTS.md` - DDD 核心
- `src/apps/AGENTS.md` - 介面層
- `src/apps/backend/AGENTS.md` - 後端
- `src/apps/web/AGENTS.md` - 前端
- `pm/AGENTS.md` - 產品管理
- `policies/AGENTS.md` - 政策文件
- `scripts/AGENTS.md` - 自動化腳本

**動態調整**：
- 技術棧章節根據 `docs/tech-stack.md` 填入
- 前端 AGENTS.md 根據框架調整內容

---

### `/setup-makefile` - 建立 Makefile

**用途**：建立開發環境管理指令

**建立的檔案**：
- `Makefile` - 開發指令
- `src/apps/backend/requirements.txt` - Python 依賴
- `src/apps/web/package.json` - 前端依賴

**主要指令**：
```bash
make help           # 顯示所有指令
make dev            # 啟動前後端開發環境
make install        # 安裝所有依賴
make clean          # 清理建置產物

make frontend-dev   # 只啟動前端
make backend-dev    # 只啟動後端
make venv-info      # 顯示虛擬環境資訊
```

---

## 🔧 常見問題

### Q: 執行順序可以跳過嗎？

部分可以：
- `/setup-structure` 和 `/setup-agents` 需要 `docs/tech-stack.md`
- `/setup-makefile` 可以獨立執行

### Q: 可以重複執行嗎？

可以，所有 workflow 都是冪等的：
- 已存在的檔案不會被覆蓋（除非明確說明）
- 目錄會跳過已存在的

### Q: 技術棧設定錯了怎麼辦？

1. 重新執行 `/setup-techstack`
2. 執行 `/setup-logging` 更新 logging 程式碼
3. 執行 `/setup-agents` 更新 AGENTS.md

### Q: 如何查看目前狀態？

執行 `/init` 並選擇 `[E]` 查看目前狀態。

---

## 📁 相關檔案

| 檔案 | 用途 |
|------|------|
| `.windsurf/workflows/init.md` | 引導流程 |
| `.windsurf/workflows/setup-*.md` | 各階段 workflow |
| `.windsurf/templates/` | 模板檔案 |
| `docs/tech-stack.md` | 技術棧設定（執行後產生） |
| `docs/logging-strategy.md` | Logging 策略說明 |
