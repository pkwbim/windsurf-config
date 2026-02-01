---
trigger: manual
---

# /init Workflow 執行規則

## 🎯 適用範圍
此規則僅在執行 `/init` workflow 及其子 workflow 時生效。

## 📋 核心原則

### 1. 嚴格遵循 Workflow 定義
- **必須先讀取 workflow 檔案**：執行任何 workflow 前，先用 `read_file` 讀取對應的 `.windsurf/workflows/{workflow-name}.md`
- **按步驟執行**：嚴格按照 workflow 中的「執行步驟」順序執行
- **不跳過步驟**：除非 workflow 明確說明可選，否則不得跳過任何步驟

### 2. 模板使用規範
- **複製模板，不自訂**：如果 workflow 指定使用模板（如 `.windsurf/templates/xxx.md`），必須：
  1. 先用 `read_file` 讀取模板內容
  2. 完整複製模板內容到目標檔案
  3. 不修改、不自訂、不創造新內容
- **驗證模板存在**：在複製前，確認模板檔案存在

### 3. 檔案命名規範
- **遵循 workflow 定義**：使用 workflow 中指定的檔案命名格式
- **常見格式**：
  - 討論檔案：`DISC-YYYYMMDD-HHMM-{Subject}.md`
  - 一般檔案：遵循 workflow 指定的格式

### 4. 預設值與定義驗證
- **不自己編造**：所有預設值（如 Preset、配置選項）必須來自：
  - Workflow 檔案中的定義
  - 模板檔案中的內容
  - 參考檔案（如 `.windsurf/templates/techstack-presets.yaml`）
- **驗證來源**：在使用任何預設值前，先讀取來源檔案確認

### 5. 停止與等待規範
- **明確停止點**：當 workflow 說「停止」、「等待使用者回答」時，必須：
  1. 告知使用者需要做什麼
  2. 完全停止，不執行任何其他動作
  3. 等待使用者明確表示已完成（如「我已回答」）
- **不主動繼續**：除非使用者明確表示可以繼續，否則不得自動進入下一步驟

## 📝 各階段特定規則

### `/setup-project-info`
- 建立目錄結構：`pm/`, `policies/`, `management/`, `enterprise/`, `legal/`, `docs/`
- 建立各目錄的 `README.md`
- 建立根目錄 `README.md`

### `/setup-techstack`
- **必須使用模板**：`.windsurf/templates/discussion-techstack.md`
- **檔案命名**：`discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md`
- **Preset 定義**：來自 workflow 或 `.windsurf/templates/techstack-presets.yaml`
- **停止等待**：建立討論檔案後，必須停止等待使用者回答

### `/setup-structure`
- 根據 `docs/tech-stack.md` 的技術棧設定建立目錄
- 建立 `src/` 下的標準目錄結構

### `/setup-logging`
- 根據技術棧產生對應的 logging 程式碼
- 支援：Python (loguru), TypeScript (winston), Rust (tracing)

### `/setup-agents`
- 使用模板建立 AGENTS.md 檔案
- 根據技術棧動態調整內容

### `/setup-makefile`
- 建立 Makefile
- 建立 `.env.example` 和 `.env`
- 根據技術棧調整指令

### `/setup-sample-project`
- 建立前後端 Hello World 範例
- 確保前後端可以串接
- 包含 logging 功能

## ⚠️ 常見錯誤與避免方式

### ❌ 錯誤 1：自己創造問卷內容
**正確做法**：讀取並複製 `.windsurf/templates/discussion-techstack.md`

### ❌ 錯誤 2：使用錯誤的 Preset 定義
**正確做法**：從 workflow 或 `techstack-presets.yaml` 讀取正確的 Preset

### ❌ 錯誤 3：檔案命名格式錯誤
**正確做法**：遵循 workflow 中指定的命名格式

### ❌ 錯誤 4：沒有停止等待使用者
**正確做法**：當 workflow 要求等待時，必須完全停止

### ❌ 錯誤 5：跳過驗證步驟
**正確做法**：執行前先讀取並驗證所有相關檔案

## 🔍 執行前檢查清單

每次執行 workflow 前，確認：
- [ ] 已讀取 workflow 檔案
- [ ] 已讀取需要的模板檔案
- [ ] 已驗證所有預設值來源
- [ ] 已確認檔案命名格式
- [ ] 已理解停止點在哪裡

## 📚 參考資源

- `.windsurf/docs/workflow-guide.md` - Workflow 使用指南
- `.windsurf/templates/` - 所有模板檔案
- `.windsurf/workflows/` - 所有 workflow 定義
