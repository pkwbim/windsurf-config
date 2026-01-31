---
description: 初始化專案根目錄（最小核心）
---

## 🎯 目的
建立專案的非技術相關目錄結構，為後續的技術棧設定做準備。

## ⚠️ 重要原則
- **不建立 src/ 內的子目錄**：等待 `/setup-techstack` 和 `/setup-structure`
- **建立最小的根目錄 AGENTS.md**：讓 AI 知道非技術目錄的用途
- **不建立任何與技術棧相關的檔案**

## 📋 執行步驟

### 1. 建立非技術目錄結構
// turbo
```python
import os
from pathlib import Path

# 定義所有需要建立的目錄（不含 src/ 內的子目錄）
directories = [
    # 私有經營層級
    "management/strategy",
    "management/finance",
    "management/legal",
    "management/docs",
    
    # 產品管理
    "pm/planning",
    "pm/discussions",
    "pm/decisions",
    "pm/sprints",
    
    # 政策規範
    "policies/foundation",
    "policies/engineering",
    "policies/operations",
    "policies/product",
    
    # 企業版
    "enterprise/packages",
    "enterprise/branding",
    
    # 其他
    "tools",
    "scripts",
    "logs",
    "out",
    "discussions",
    "docs",
    
    # src 只建立空目錄，等 /setup-structure 建立子目錄
    "src",
    
    # Windsurf 配置
    ".windsurf/rules",
    ".windsurf/workflows",
    ".windsurf/skills",
    ".windsurf/templates",
]

for d in directories:
    Path(d).mkdir(parents=True, exist_ok=True)
    print(f"✅ {d}")

print("\n📁 非技術目錄結構建立完成")
```

### 2. 建立基礎檔案
// turbo
```python
from pathlib import Path

# 建立 .gitkeep 檔案讓空目錄可以被 git 追蹤
gitkeep_dirs = [
    "logs",
    "out",
    "src",
]

for d in gitkeep_dirs:
    gitkeep = Path(d) / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()
        print(f"✅ {gitkeep}")

# 建立 pm/planning 的基礎檔案
planning_files = [
    ("pm/planning/01_backlog.md", "# 📋 Backlog\n\n待辦事項清單。\n"),
    ("pm/planning/02_active.md", "# 🚀 Active\n\n目前進行中的工作。\n"),
    ("pm/planning/03_completed.md", "# ✅ Completed\n\n已完成的工作。\n"),
]

for filepath, content in planning_files:
    path = Path(filepath)
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        print(f"✅ {filepath}")
    else:
        print(f"⏭️ {filepath} (已存在)")

print("\n📄 基礎檔案建立完成")
```

### 3. 建立根目錄最小 AGENTS.md
// turbo
```python
from pathlib import Path

# 最小的 AGENTS.md，只說明非技術目錄的用途
# 技術棧章節會由 /setup-agents 補充
agents_content = """# 🏢 專案規範

## 📋 專案概述

一人公司完整 monorepo，整合產品管理、政策規範、共享契約、DDD 核心業務邏輯、多介面應用層。

## 📁 目錄結構規範

```
project/
├── management/              # 私有經營層級
│   ├── strategy/           # 策略規劃
│   ├── finance/            # 財務管理
│   ├── legal/              # 法律文件
│   └── docs/               # 經營文件
├── pm/                      # 產品管理
│   ├── planning/           # 01_backlog, 02_active, 03_completed
│   ├── discussions/        # DISC-*.md 討論檔案
│   ├── decisions/          # DEC-*.md 決策檔案
│   └── sprints/            # Sprint 規劃
├── policies/                # 公司規定
│   ├── foundation/         # 基礎規定
│   ├── engineering/        # 工程規範
│   ├── operations/         # 營運規範
│   └── product/            # 產品規範
├── src/                     # 程式碼層（由 /setup-structure 建立）
├── enterprise/              # 企業版
├── tools/                   # 工具腳本
├── scripts/                 # 自動化腳本
├── logs/                    # 日誌檔案
├── out/                     # 輸出檔案
├── discussions/             # 全域討論檔案
├── docs/                    # 文件
└── .windsurf/              # Windsurf 配置
```

## 🛠️ 技術棧

> ⚠️ 技術棧尚未設定，請執行 `/setup-techstack` 設定技術棧。
> 設定完成後，執行 `/setup-agents` 會更新此章節。

## 🎯 核心開發原則

### DDD (Domain-Driven Design)
- **Domain Layer**: 業務邏輯、實體、用例
- **Infrastructure Layer**: 資料庫、API、外部服務
- **Application Layer**: 服務協調、事務管理

### OOP (Object-Oriented Programming)
- 在 `src/core/` 使用 OOP 設計
- 類別、介面、繼承、多型

### TDD (Test-Driven Development)
- 先寫測試，後寫實現
- 單元測試檔案：`*.unit.py` 或 `*.test.ts`
- 整合測試檔案：`*.integration.py` 或 `*.integration.ts`

## 📝 命名規範

| 層級 | 規範 | 範例 |
|------|------|------|
| 目錄 | kebab-case | `src/core/domain/use-cases/` |
| Python 檔案 | snake_case | `user_repository.py` |
| Python 類別 | PascalCase | `UserRepository` |
| TypeScript 檔案 | camelCase | `userService.ts` |
| TypeScript 類別 | PascalCase | `UserService` |
| 常數 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |

## 🔐 敏感資訊處理

- 環境變數存放在 `.env` 檔案（不提交到 Git）
- `.env.example` 提供範本
- 敏感資訊不應出現在程式碼中
"""

agents_path = Path("AGENTS.md")
if not agents_path.exists():
    agents_path.write_text(agents_content, encoding="utf-8")
    print(f"✅ AGENTS.md (最小版本)")
else:
    print(f"⏭️ AGENTS.md (已存在，將由 /setup-agents 更新)")
```

### 4. 建立 docs/README.md
// turbo
```python
from pathlib import Path

readme_content = """# 📚 文件目錄

## 技術文件
- `tech-stack.md` - 技術棧說明（由 /setup-techstack 建立）
- `code-standards.md` - 程式碼規範
- `workflow-init-process.md` - 專案初始化流程

## 架構文件
- `monorepo-architecture-v3.md` - Monorepo 架構設計

## 其他
- 討論結論會記錄在此目錄
"""

readme_path = Path("docs/README.md")
if not readme_path.exists():
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"✅ docs/README.md")
else:
    print(f"⏭️ docs/README.md (已存在)")
```

### 5. 驗證結構
// turbo
```python
from pathlib import Path

key_dirs = [
    "management",
    "pm/planning",
    "policies",
    "enterprise",
    "tools",
    "scripts",
    "logs",
    "out",
    "discussions",
    "docs",
    "src",
    ".windsurf",
]

print("🔍 驗證目錄結構...")
all_ok = True
for d in key_dirs:
    if Path(d).exists():
        print(f"✅ {d}")
    else:
        print(f"❌ {d} (不存在)")
        all_ok = False

# 驗證 AGENTS.md
if Path("AGENTS.md").exists():
    print(f"✅ AGENTS.md")
else:
    print(f"❌ AGENTS.md (不存在)")
    all_ok = False

if all_ok:
    print("\n✅ 所有關鍵目錄和檔案已建立")
else:
    print("\n⚠️ 部分目錄或檔案未建立，請檢查")
```

### 6. 顯示完成訊息
執行完成後，輸出以下訊息：
```
✅ 專案基礎結構初始化完成！

已建立的目錄：
📁 私有層級
  - management/ (經營管理)
  - pm/ (產品管理)
  - policies/ (公司規定)
  - enterprise/ (企業版)

📁 其他
  - tools/, scripts/, logs/, out/
  - discussions/, docs/
  - src/ (空目錄，等待 /setup-structure)
  - .windsurf/ (配置)

已建立的檔案：
📄 AGENTS.md (最小版本，技術棧待設定)
📄 docs/README.md
📄 pm/planning/01_backlog.md, 02_active.md, 03_completed.md

下一步：
  - 執行 `/setup-techstack` 設定技術棧
```

## 📝 注意事項

1. 此 workflow 是冪等的（可重複執行）
2. 已存在的檔案不會被覆蓋
3. **不要**在此階段建立 src/ 的子目錄
4. **會建立最小的 AGENTS.md**（技術棧章節為空，由 `/setup-agents` 更新）

## 🔗 相關 Workflow

執行順序：
1. `/setup-project-info` ← 你在這裡
2. `/setup-techstack` - 設定技術棧
3. `/setup-structure` - 建立 src/ 目錄結構
4. `/setup-agents` - 建立/更新 AGENTS.md
