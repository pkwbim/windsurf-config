---
description: 初始化專案根目錄（最小核心）
---

## 目的

初始化一個全新專案的根目錄，建立最基本的檔案結構。

## 重要原則

- **最小核心**：只建立最基本的檔案
- **空檔案優先**：README.md 和 AGENTS.md 建立為空檔案，內容用 `/discussion` 討論後填寫
- **模組化擴展**：需要其他目錄時，使用對應的 `init-*` workflow

---

## 工作流程步驟

### 1. 確認執行位置
// turbo
```bash
pwd
ls -la
```
- 確認目前在正確的專案目錄
- 檢查是否已有 `.git` 目錄或其他檔案

### 2. 初始化 Git
// turbo
```bash
git init
```

### 3. 建立 README.md
建立空的 README.md 檔案：
// turbo
```bash
touch README.md
```

### 4. 建立 AGENTS.md
建立空的 AGENTS.md 檔案：
// turbo
```bash
touch AGENTS.md
```

### 5. 建立 .gitignore
建立標準的 .gitignore 檔案，內容如下：

```
# Dependencies
node_modules/
.venv/
venv/
__pycache__/
*.pyc

# Build outputs
dist/
build/
out/
*.egg-info/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Logs
logs/
*.log
npm-debug.log*

# Test coverage
coverage/
.coverage
htmlcov/

# Temporary files
tmp/
temp/
*.tmp
```

### 6. 初始提交
// turbo
```bash
git add -A
git commit -m "chore: init project with README.md, AGENTS.md, .gitignore"
```

### 7. 提示下一步

告訴使用者：

專案初始化完成！

已建立：
- README.md（空檔案）
- AGENTS.md（空檔案）
- .gitignore（標準忽略清單）
- Git 倉庫已初始化

下一步建議：

1. **填寫專案說明**：執行 `/discussion` 討論 README.md 和 AGENTS.md 要寫什麼

2. **按需初始化其他目錄**：
   - `/init-discussions` - 建立 discussions/ 討論目錄
   - `/init-planning` - 建立 _planning/ 專案規劃目錄
   - `/init-docs` - 建立 docs/ 文件目錄
   - `/init-scripts` - 建立 scripts/ + Makefile
   - `/init-src` - 建立 src/ DDD 架構

**然後停止，等待使用者指示。**

---

## 建立的檔案清單

| 檔案 | 說明 |
|------|------|
| README.md | 空檔案，專案說明 |
| AGENTS.md | 空檔案，AI Agent 指引 |
| .gitignore | 標準忽略清單 |
| .git/ | Git 倉庫 |

## 成功標準

- Git 倉庫已初始化
- 三個檔案已建立
- 初始提交已完成
- 已提示可用的 init-* workflows

## 注意事項

- 此 workflow 假設在空目錄或新專案中執行
- 如果目錄已有檔案，請先確認是否要覆蓋
- README.md 和 AGENTS.md 的內容應透過 /discussion 討論後填寫
