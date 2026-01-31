---
description: 建立或更新 Makefile，包含虛擬環境管理
---

## 🎯 目的
自動生成完整的 Makefile，支援：
- Python 虛擬環境自動建立和啟用
- 前後端並行開發環境
- 依賴管理和安裝
- 清理和建置指令

## 📋 執行步驟

### 1. 檢查現有 Makefile
檢查專案根目錄是否已有 Makefile。
- 如果存在，詢問使用者是否要備份（建立 `Makefile.backup`）
- 如果不存在，直接建立新的

### 2. 建立完整的 Makefile
在專案根目錄建立 `Makefile`，包含以下功能：

#### 變數定義
```makefile
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
UVICORN = $(VENV_DIR)/bin/uvicorn
```

#### 核心指令
- `make help` - 顯示所有可用指令
- `make dev` - 啟動完整開發環境（前端 + 後端，自動建立 venv）
- `make install` - 安裝所有依賴（自動建立 venv）
- `make clean` - 清理所有建置產物和依賴

#### Frontend 指令
- `make frontend-install` - 安裝前端依賴
- `make frontend-dev` - 啟動前端開發伺服器
- `make frontend-build` - 建置前端生產版本

#### Backend 指令
- `make backend-venv` - 建立 Python 虛擬環境
- `make backend-install` - 安裝後端依賴（自動建立 venv）
- `make backend-dev` - 啟動後端開發伺服器（使用 venv）
- `make backend-clean` - 清理後端快取

#### 工具指令
- `make check-deps` - 檢查依賴是否已安裝
- `make venv-info` - 顯示虛擬環境資訊

### 3. 關鍵功能實作

#### 自動建立虛擬環境
```makefile
$(VENV_DIR):
	@echo "Creating Python virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"
```

#### Backend 安裝（依賴 venv）
```makefile
backend-install: $(VENV_DIR)
	@echo "Installing backend dependencies in virtual environment..."
	$(PIP) install --upgrade pip
	$(PIP) install -r backend/requirements.txt
	@echo "Backend dependencies installed!"
```

#### 開發環境（並行執行）
```makefile
dev: backend-install frontend-install
	@echo "Starting development environment..."
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@trap 'kill 0' EXIT; \
	(cd backend && ../$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000) & \
	(cd frontend && npm run dev)
```

#### 清理（包含 venv）
```makefile
clean: backend-clean
	@echo "Cleaning all build artifacts and dependencies..."
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf $(VENV_DIR)
	@echo "Clean complete!"
```

### 4. 建立 .gitignore 條目
確保 `.gitignore` 包含：
```
.venv/
src/apps/backend/__pycache__/
src/apps/backend/**/__pycache__/
src/apps/backend/**/*.pyc
```

### 5. 測試 Makefile
執行以下指令測試：
```bash
make help
make backend-venv
make venv-info
```

### 6. 顯示使用說明
```
✅ Makefile 已建立！

虛擬環境管理：
- 虛擬環境位置: .venv/
- 自動建立: 執行 make install 或 make backend-install 時自動建立
- 手動建立: make backend-venv

常用指令：
1. 首次安裝：
   make install

2. 啟動開發環境：
   make dev

3. 只啟動後端：
   make backend-dev

4. 清理重裝：
   make clean
   make install

5. 檢查虛擬環境：
   make venv-info

注意事項：
- 虛擬環境會自動建立在 .venv/
- 所有 Python 指令都會使用虛擬環境
- 不需要手動 activate venv
- 虛擬環境已加入 .gitignore
```

## 📝 Makefile 完整內容

建立包含以下內容的 Makefile：

```makefile
# 變數定義
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
UVICORN = $(VENV_DIR)/bin/uvicorn

.PHONY: help dev install clean check-deps venv-info
.PHONY: frontend-dev frontend-install frontend-build
.PHONY: backend-venv backend-dev backend-install backend-clean

help:
	@echo "Available commands:"
	@echo "  make dev              - Start development environment (frontend + backend)"
	@echo "  make install          - Install all dependencies (auto-creates venv)"
	@echo "  make clean            - Clean all build artifacts and dependencies"
	@echo ""
	@echo "Frontend commands:"
	@echo "  make frontend-dev     - Start frontend development server"
	@echo "  make frontend-install - Install frontend dependencies"
	@echo "  make frontend-build   - Build frontend for production"
	@echo ""
	@echo "Backend commands:"
	@echo "  make backend-venv     - Create Python virtual environment"
	@echo "  make backend-dev      - Start backend development server"
	@echo "  make backend-install  - Install backend dependencies (auto-creates venv)"
	@echo "  make backend-clean    - Clean backend cache and artifacts"
	@echo ""
	@echo "Utility commands:"
	@echo "  make check-deps       - Check if all dependencies are installed"
	@echo "  make venv-info        - Show virtual environment information"

# 建立虛擬環境
$(VENV_DIR):
	@echo "Creating Python virtual environment at $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	@echo "✓ Virtual environment created!"

# 開發環境 - 同時啟動前後端
dev: backend-install frontend-install
	@echo "Starting development environment (frontend + backend)..."
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@trap 'kill 0' EXIT; \
	(cd src/apps/backend && $(UVICORN) main:app --reload --host 0.0.0.0 --port 8000) & \
	(cd src/apps/web && npm run dev)

# 安裝所有依賴
install: frontend-install backend-install

# 檢查依賴
check-deps:
	@echo "Checking dependencies..."
	@command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is not installed"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "Error: node is not installed"; exit 1; }
	@command -v npm >/dev/null 2>&1 || { echo "Error: npm is not installed"; exit 1; }
	@test -d frontend/node_modules || echo "Warning: Frontend dependencies not installed"
	@test -d $(VENV_DIR) || echo "Warning: Python virtual environment not created"
	@test -d $(VENV_DIR) && $(PYTHON) -c "import fastapi" 2>/dev/null || echo "Warning: Backend dependencies not installed"
	@echo "✓ Dependencies check complete!"

# 顯示虛擬環境資訊
venv-info:
	@echo "Virtual Environment Information:"
	@echo "  Location: $(VENV_DIR)"
	@test -d $(VENV_DIR) && echo "  Status: ✓ Created" || echo "  Status: ✗ Not created"
	@test -d $(VENV_DIR) && echo "  Python: $$($(PYTHON) --version)" || true
	@test -d $(VENV_DIR) && echo "  Pip: $$($(PIP) --version)" || true

# Frontend 指令
frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✓ Frontend dependencies installed!"

frontend-dev:
	@echo "Starting frontend development server..."
	cd frontend && npm run dev

frontend-build:
	@echo "Building frontend..."
	cd frontend && npm run build

# Backend 指令
backend-venv: $(VENV_DIR)

backend-install: $(VENV_DIR)
	@echo "Installing backend dependencies in virtual environment..."
	$(PIP) install --upgrade pip
	$(PIP) install -r src/apps/backend/requirements.txt
	@echo "✓ Backend dependencies installed!"

backend-dev: $(VENV_DIR)
	@echo "Starting backend development server..."
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@test -f src/apps/backend/main.py || { echo "Error: src/apps/backend/main.py not found"; exit 1; }
	cd src/apps/backend && $(UVICORN) main:app --reload --host 0.0.0.0 --port 8000

backend-clean:
	@echo "Cleaning backend cache and artifacts..."
	find src/apps/backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find src/apps/backend -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Backend clean complete!"

# 清理所有
clean: backend-clean
	@echo "Cleaning all build artifacts and dependencies..."
	rm -rf src/apps/web/node_modules
	rm -rf src/apps/web/dist
	rm -rf $(VENV_DIR)
	@echo "✓ Clean complete!"
```

## 🔧 故障排除

### 問題：虛擬環境建立失敗
解決方案：
```bash
# 確認 python3-venv 已安裝
sudo apt-get install python3-venv  # Ubuntu/Debian
# 或
brew install python3  # macOS
```

### 問題：權限錯誤
解決方案：
```bash
# 確保有寫入權限
chmod +x backend/venv/bin/*
```

### 問題：找不到 uvicorn
解決方案：
```bash
# 重新安裝 backend 依賴
make clean
make backend-install
```

## 📚 參考資料

- Python venv 文件: https://docs.python.org/3/library/venv.html
- Make 文件: https://www.gnu.org/software/make/manual/
- 專案架構: 參考根目錄 AGENTS.md
