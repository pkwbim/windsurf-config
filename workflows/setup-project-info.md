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
若 `AGENTS.md` 不存在，從模板複製：
// turbo
```bash
if [ ! -f AGENTS.md ]; then
    cp .windsurf/templates/AGENTS-base.md AGENTS.md
    echo "✅ AGENTS.md (從模板建立)"
else
    echo "⏭️ AGENTS.md (已存在，將由 /setup-agents 更新)"
fi
```

### 4. 建立 docs/README.md
若 `docs/README.md` 不存在，從模板複製：
// turbo
```bash
if [ ! -f docs/README.md ]; then
    cp .windsurf/templates/docs-README.md docs/README.md
    echo "✅ docs/README.md (從模板建立)"
else
    echo "⏭️ docs/README.md (已存在)"
fi
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
  - tools/, scripts/, out/
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
