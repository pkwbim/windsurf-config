---
description: CLI/腳本開發 workflow（Makefile + Shell/Python + SSH 遠端操作）
---

## 🎯 目的
開發 CLI 工具和自動化腳本，包含 Makefile 指令、Shell/Python 腳本、SSH 遠端操作、設定檔模板。
適用於無 Web UI、無 API 端點、無 DB Migration 的純命令列功能。

## ⚠️ 重要原則
- **模組化**：每個腳本函式/模組負責一件事，放在 `lib/` 目錄
- **可回滾**：每個遠端操作都有對應的回滾指令
- **可追溯**：完整 log 記錄（時間戳 + level），不記錄明文密碼
- **AI-friendly**：輸出結構化資訊，方便 AI Agent 解讀
- **檔案限制**：每個腳本檔案不超過 200 行，超過則拆分為 `lib/` 模組
- **人類確認後才進下一步**

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
```
- 如果目前仍在 `main`：停止並提醒先執行 `/plan` 以建立 `feat/<story-id>` 分支
- 如果已在 feature 分支：繼續後續實作

// turbo
```bash
cat pm/planning/02_active.md
```
- 確認規格已在 `pm/planning/02_active.md`

**❗️ 重要：必須完整閱讀 Story 目錄下的規格文件，理解：**
- `use-cases.md`：Use Case 流程（主要流程、替代流程、例外流程）
- `business-rules.md`：業務規則（驗證、命名、安全、回滾）
- `spec.md`：技術規格（架構、指令介面、腳本結構、遠端操作、模板）
- `checklist.md`：開發進度追蹤
- `e2e-scenarios.md`：E2E 測試劇本

### 1. 閱讀規格並建立實作計畫

讀取所有規格文件：
// turbo
```bash
STORY_DIR=$(grep -oP 'stories/\S+' pm/planning/02_active.md | head -1)
ls pm/planning/$STORY_DIR/
```

// turbo
```bash
STORY_DIR=$(grep -oP 'stories/\S+' pm/planning/02_active.md | head -1)
cat pm/planning/$STORY_DIR/spec.md
```

**根據 `spec.md` 和 `checklist.md`，確認實作順序：**

典型的 CLI 開發順序：
1. 共用函式庫（`lib/common.sh`、`lib/validation.sh`）
2. 設定檔模板（`src/templates/*.tpl`）
3. 各模組（依 spec.md 的腳本結構）
4. 主腳本（組合各模組）
5. Makefile targets
6. 測試

### 2. 建立共用函式庫

**先建立基礎設施：**

- `lib/common.sh`：log 函式、顏色輸出、錯誤處理框架、環境變數載入
- `lib/validation.sh`：輸入參數驗證（對應 BR 的驗證規則）

**log 函式規範：**
```bash
log() {
    local level="$1" module="$2" message="$3"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] [$module] $message"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] [$module] $message" >> "$LOG_FILE"
}
```

**驗證後立即測試：**
// turbo
```bash
bash -n src/scripts/lib/common.sh && echo "Syntax OK" || echo "Syntax Error"
bash -n src/scripts/lib/validation.sh && echo "Syntax OK" || echo "Syntax Error"
```

### 3. 建立設定檔模板

根據 `spec.md` 的「設定檔模板」章節，建立所有模板檔案：

- 模板放在 `src/templates/` 目錄
- 使用 `{{VARIABLE}}` 佔位符
- 每個模板對應 spec.md 中的一個模板定義

### 4. 實作各功能模組

**依照 `spec.md` 的「腳本檔案結構」逐一實作 `lib/` 下的模組。**

每個模組實作時：
1. 閱讀對應的 BR 和 UC 步驟
2. 實作函式
3. 包含回滾函式（若涉及遠端操作）
4. 語法檢查

**語法檢查（每個模組完成後）：**
// turbo
```bash
bash -n src/scripts/lib/{module}.sh && echo "Syntax OK" || echo "Syntax Error"
```

**⚠️ SSH 指令規範：**
- 統一使用 `ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10`
- 每個 SSH 指令的 exit code 都要捕獲
- 失敗時觸發回滾邏輯

### 5. 實作主腳本

組合 `lib/` 模組，實作主腳本（對應 UC-01 主流程）：

- 載入環境變數和函式庫
- 解析參數
- 依序呼叫各模組
- 錯誤處理 + trap 回滾
- 結構化輸出結果

**語法檢查：**
// turbo
```bash
bash -n src/scripts/{main_script}.sh && echo "Syntax OK" || echo "Syntax Error"
```

### 6. 實作輔助腳本

根據 spec.md，實作其他 UC 對應的腳本（如查詢、列表等）。

### 7. 更新 Makefile

在 `Makefile` 新增對應的 targets：

```makefile
# 每個 target 對應 spec.md 的 Makefile 指令介面
target-name:
	@bash src/scripts/{script}.sh $(param1) $(param2)
```

**驗證 Makefile 語法：**
// turbo
```bash
make -n {target-name} 2>&1 | head -5
```

### 8. 功能驗證測試

**依照 `e2e-scenarios.md` 的正向劇本進行測試：**

1. 先測試驗證規則（負向劇本 S-E01, S-E02...）
2. 再測試主流程（正向劇本 S-01）
3. 最後測試替代流程（S-03, S-04...）

**驗證規則測試（不需要遠端環境）：**
```bash
# 測試非法輸入被拒絕
make {target} param=invalid_value
echo "Exit code: $?"
```

**主流程測試（需要遠端環境，謹慎操作）：**
```bash
# 使用測試用參數
make {target} param=test-value
```

**⚠️ 重要：**
- 涉及遠端操作的測試需要使用者確認後才執行
- 測試用的參數加上 `test-` 前綴，方便事後清理
- 每次測試前確認環境狀態

### 9. 更新 checklist.md

更新 story 目錄下的 `checklist.md`，勾選已完成的項目。

### 10. 更新開發狀態

更新 `pm/planning/02_active.md`：
```markdown
**📊 開發狀態**: ✅ Build 完成 → 待人工驗證
```

### 11. 🛑 人工驗證檢查點（MANDATORY）
**⚠️ 重要：此步驟不可跳過！**

完成實作後，**必須**停下來等待使用者進行人工驗證：

1. **提供驗證指南**：
   - 列出需要驗證的 make 指令和參數
   - 列出需要 SSH 檢查的遠端狀態
   - 提供具體的驗證步驟

2. **明確告知使用者**：
   ```
   ⚠️ 請進行人工驗證
   
   已完成 CLI 腳本實作，現在需要您進行人工驗證：
   
   📋 驗證項目：
   - [ ] `make {target} param=test-value` 執行成功
   - [ ] 遠端資源已正確建立（SSH 檢查）
   - [ ] 憑證已正確儲存
   - [ ] Log 記錄完整
   
   ✅ 驗證完成後，請回覆「驗證通過」以繼續下一步
   ❌ 如發現問題，請描述問題以便修正
   ```

3. **等待使用者回應**：
   - **不要自動執行 `/commit`**
   - **不要假設驗證已通過**
   - 等待使用者明確回覆後才繼續

### 12. 提示下一步

告訴使用者：
- ✅ CLI 腳本實作完成
- 📝 已更新開發狀態和 checklist
- 🔜 下一步：執行 `/commit` 提交程式碼
- ⚠️ 如需整合測試，可執行 `/integration-e2e`

---

## 適用場景
- Makefile + Shell/Python 腳本開發
- SSH 遠端操作自動化
- 系統管理工具（如 WordPress 建站、伺服器管理）
- 無 Web UI、無 API 端點、無 DB Migration 的功能

## 不適用場景
- Web App 開發 → 使用 `/build-laravel` 或 `/build`
- 有前端 UI → 使用 `/build-laravel-ui` 或 `/build-ui`
- 有 API 端點 → 使用 `/build-backend` 或 `/build-laravel-backend`

---

## Tech Stack
- **入口**: Makefile
- **腳本**: Bash (Shell Script) / Python
- **遠端操作**: SSH (key-based auth)
- **外部 API**: curl + JSON 解析 (jq)
- **模板引擎**: sed / envsubst
- **測試**: bash -n (語法) + 手動驗證 + e2e-scenarios.md
