---
description: CLI/腳本開發 workflow（Makefile + Python + SSH 遠端操作）
---

## 🎯 目的
開發 CLI 工具和自動化腳本，包含 Makefile 指令、Python 腳本、SSH 遠端操作、設定檔模板。
適用於無 Web UI、無 API 端點、無 DB Migration 的純命令列功能。

## ⚠️ 重要原則
- **Python 為主**：所有邏輯用 Python 實作，Makefile 僅作為入口
- **模組化**：每個 Python 模組負責一件事，放在 `src/scripts/` 的子 package 目錄
- **可回滾**：每個遠端操作都有對應的回滾方法
- **可追溯**：使用 Python `logging` 模組，不記錄明文密碼
- **AI-friendly**：輸出結構化資訊（JSON），方便 AI Agent 解讀
- **檔案限制**：每個 Python 檔案不超過 200 行，超過則拆分模組
- **型別提示**：所有函式加上 type hints
- **人類確認後才進下一步**

---

## 虛擬環境管理
- 本專案使用 `.venv/` 作為 Python 虛擬環境
- 如果 `.venv/` 不存在，先建立：
  // turbo
  ```bash
  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
  ```
- Makefile targets 需透過 `.venv/bin/python` 呼叫腳本

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

典型的 Python CLI 開發順序：
1. Python package 結構與 `__init__.py`
2. 共用模組（`utils/logger.py`、`utils/ssh.py`、`utils/env.py`）
3. 設定檔模板（`src/templates/*.tpl`）
4. 各功能模組（依 spec.md 的腳本結構）
5. 主程式入口（`main.py` 或 `cli.py`）
6. Makefile targets
7. 測試（pytest）

### 2. 建立 Python Package 結構

**先建立目錄和 package 結構：**

```
src/scripts/
├── __init__.py
├── create_site.py           # 主程式：建站（UC-01）
├── show_credentials.py      # 查詢憑證（UC-02）
├── list_sites.py            # 列出站點（UC-03）
├── utils/
│   ├── __init__.py
│   ├── logger.py            # logging 設定
│   ├── ssh.py               # SSH 執行封裝
│   ├── env.py               # 環境變數載入
│   └── password.py          # 密碼產生
├── validators/
│   ├── __init__.py
│   └── domain.py            # domain 格式驗證（BR-01）
├── naming/
│   ├── __init__.py
│   └── convention.py        # 命名規則（BR-03, BR-04）
├── operations/
│   ├── __init__.py
│   ├── dns.py               # DNS 預檢與設定（BR-05, BR-06）
│   ├── database.py          # DB VPS 操作
│   ├── webserver.py         # Web VPS 操作
│   ├── frontend.py          # Front VPS 操作
│   └── security.py          # 安全強化（BR-07）
├── rollback/
│   ├── __init__.py
│   └── manager.py           # 回滾邏輯（BR-08）
└── credentials/
    ├── __init__.py
    └── store.py             # 憑證管理（BR-09）
```

**驗證 package 結構：**
// turbo
```bash
python3 -c "import src.scripts" && echo "Package OK" || echo "Package Error"
```

### 3. 建立共用工具模組

**先建立基礎設施：**

- `utils/logger.py`：Python logging 設定（console + file handler）
- `utils/ssh.py`：SSH 執行封裝（使用 `subprocess.run`）
- `utils/env.py`：環境變數載入（使用 `python-dotenv`）
- `utils/password.py`：密碼產生（使用 `secrets` 模組）

**logging 規範：**
```python
import logging

def setup_logger(name: str, log_file: str = "logs/wp-manager.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Console handler（帶顏色）
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(ColorFormatter())
    logger.addHandler(console)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    ))
    logger.addHandler(file_handler)
    
    return logger
```

**SSH 封裝規範：**
```python
import subprocess

def ssh_exec(host: str, command: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """執行 SSH 指令，統一參數和錯誤處理"""
    return subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no",
         "-o", "ConnectTimeout=10",
         "-o", "BatchMode=yes",
         host, command],
        capture_output=True, text=True, timeout=timeout
    )
```

**驗證模組語法：**
// turbo
```bash
.venv/bin/python -m py_compile src/scripts/utils/logger.py && echo "OK" || echo "Error"
.venv/bin/python -m py_compile src/scripts/utils/ssh.py && echo "OK" || echo "Error"
```

### 4. 建立設定檔模板

根據 `spec.md` 的「設定檔模板」章節，建立所有模板檔案：

- 模板放在 `src/templates/` 目錄
- 使用 Python `string.Template`（`$VARIABLE`）或 Jinja2（`{{ variable }}`）
- 每個模板對應 spec.md 中的一個模板定義

### 5. 實作各功能模組

**依照 `spec.md` 的「腳本檔案結構」逐一實作 `operations/` 下的模組。**

每個模組實作時：
1. 閱讀對應的 BR 和 UC 步驟
2. 實作 class 或函式（加 type hints）
3. 包含回滾方法（若涉及遠端操作）
4. 語法檢查

**語法檢查（每個模組完成後）：**
// turbo
```bash
.venv/bin/python -m py_compile src/scripts/operations/{module}.py && echo "OK" || echo "Error"
```

**⚠️ SSH 指令規範：**
- 統一使用 `utils/ssh.py` 的 `ssh_exec()` 函式
- 每個 SSH 呼叫的 returncode 都要檢查
- 失敗時呼叫 `rollback.manager` 的回滾方法

### 6. 實作主程式入口

組合各模組，實作主程式（對應 UC-01 主流程）：

- 使用 `argparse` 解析參數
- 依序呼叫各 operations 模組
- try/except 錯誤處理 + 回滾
- 結構化輸出結果（JSON）

**語法檢查：**
// turbo
```bash
.venv/bin/python -m py_compile src/scripts/create_site.py && echo "OK" || echo "Error"
```

### 7. 實作輔助程式

根據 spec.md，實作其他 UC 對應的程式（如查詢、列表等）。

### 8. 更新 Makefile

在 `Makefile` 新增對應的 targets：

```makefile
PYTHON = .venv/bin/python

# 每個 target 對應 spec.md 的 Makefile 指令介面
create-site:
	@$(PYTHON) src/scripts/create_site.py --domain=$(domain) --dns=$(dns) --www=$(www)

show-credentials:
	@$(PYTHON) src/scripts/show_credentials.py --domain=$(domain)

list-sites:
	@$(PYTHON) src/scripts/list_sites.py
```

**驗證 Makefile 語法：**
// turbo
```bash
make -n {target-name} 2>&1 | head -5
```

### 9. 功能驗證測試

**依照 `e2e-scenarios.md` 的正向劇本進行測試：**

1. 先測試驗證規則（負向劇本 S-E01, S-E02...）
2. 再測試主流程（正向劇本 S-01）
3. 最後測試替代流程（S-03, S-04...）

**驗證規則測試（不需要遠端環境）：**
```bash
# 測試非法輸入被拒絕
make create-site domain=invalid..domain
echo "Exit code: $?"
```

**主流程測試（需要遠端環境，謹慎操作）：**
```bash
# 使用測試用參數
make create-site domain=test-example.com dns=external
```

**⚠️ 重要：**
- 涉及遠端操作的測試需要使用者確認後才執行
- 測試用的參數加上 `test-` 前綴，方便事後清理
- 每次測試前確認環境狀態

### 10. 更新 checklist.md

更新 story 目錄下的 `checklist.md`，勾選已完成的項目。

### 11. 更新開發狀態

更新 `pm/planning/02_active.md`：
```markdown
**📊 開發狀態**: ✅ Build 完成 → 待人工驗證
```

### 12. 🛑 人工驗證檢查點（MANDATORY）
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
   - [ ] `make create-site domain=test-example.com dns=external` 執行成功
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

### 13. 提示下一步

告訴使用者：
- ✅ CLI 腳本實作完成
- 📝 已更新開發狀態和 checklist
- 🔜 下一步：執行 `/commit` 提交程式碼
- ⚠️ 如需整合測試，可執行 `/integration-e2e`

---

## 適用場景
- Makefile + Python 腳本開發
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
- **語言**: Python 3.10+
- **虛擬環境**: `.venv/`（venv）
- **遠端操作**: `subprocess` + SSH (key-based auth)
- **外部 API**: `requests` / `httpx`
- **模板引擎**: `string.Template` 或 Jinja2
- **設定管理**: `python-dotenv`
- **測試**: pytest + 手動驗證 + e2e-scenarios.md
- **型別檢查**: type hints（可選 mypy）
