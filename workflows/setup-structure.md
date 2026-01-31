---
description: 初始化專案目錄結構和 AGENTS.md 檔案（Monorepo v3 架構）
---

## 🎯 目的
根據 `docs/tech-stack.md` 的技術棧設定，建立 src/ 內的目錄結構。

## ⚠️ 重要原則
- **讀取 docs/tech-stack.md**：根據技術棧決定要建立哪些目錄
- **只建立 src/ 內的目錄**：非技術目錄由 `/setup-project-info` 建立
- **不建立 AGENTS.md**：由 `/setup-agents` 負責

## 🔗 執行順序
此 workflow 是四階段初始化流程的第三階段：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ✅
3. `/setup-structure` - 建立 src/ 目錄結構 ← 你在這裡
4. `/setup-agents` - 建立 AGENTS.md

---

## 📋 執行步驟

### 1. 讀取技術棧設定
// turbo
```bash
cat docs/tech-stack.md
```

根據 `docs/tech-stack.md` 的內容，判斷：
- 是否使用 Python（建立 `__init__.py`、`src/contracts/python/`）
- 是否使用 TypeScript（建立 `src/contracts/typescript/`）
- 是否使用 Rust（建立 `src/contracts/rust/`）
- 前端框架是什麼（調整 `src/apps/web/` 結構）

### 2. 建立 src/ 核心目錄結構
// turbo
```python
import os
from pathlib import Path

# 核心目錄（不論技術棧都需要）
core_directories = [
    # src/contracts (共享契約) - 基礎目錄
    "src/contracts/schemas",
    "src/contracts/enums",
    "src/contracts/errors",
    "src/contracts/i18n",
    
    # src/core (DDD 三層)
    "src/core/domain/entities",
    "src/core/domain/use-cases",
    "src/core/domain/services",
    "src/core/infrastructure/repositories",
    "src/core/infrastructure/external-api",
    "src/core/infrastructure/db/migrations",
    "src/core/infrastructure/db/schemas",
    "src/core/infrastructure/mocks",
    "src/core/application/services",
    
    # src/apps (介面層) - 基礎目錄
    "src/apps",
]

for d in core_directories:
    Path(d).mkdir(parents=True, exist_ok=True)
    print(f"✅ {d}")

print("\n📁 核心目錄結構建立完成")
```

### 3. 根據技術棧建立語言相關目錄

**如果使用 Python：**
// turbo
```python
from pathlib import Path

# 讀取 tech-stack.md 判斷是否使用 Python
tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

if "Python" in tech_stack or "python" in tech_stack:
    python_dirs = [
        "src/contracts/python/dto",
        "src/contracts/python/interfaces",
        "src/apps/backend/routes",
    ]
    
    for d in python_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✅ {d}")
    
    # 建立 __init__.py
    init_files = [
        "src/contracts/__init__.py",
        "src/contracts/python/__init__.py",
        "src/contracts/python/dto/__init__.py",
        "src/contracts/python/interfaces/__init__.py",
        "src/core/__init__.py",
        "src/core/domain/__init__.py",
        "src/core/domain/entities/__init__.py",
        "src/core/domain/use-cases/__init__.py",
        "src/core/domain/services/__init__.py",
        "src/core/infrastructure/__init__.py",
        "src/core/infrastructure/repositories/__init__.py",
        "src/core/infrastructure/mocks/__init__.py",
        "src/core/application/__init__.py",
        "src/core/application/services/__init__.py",
        "src/apps/__init__.py",
        "src/apps/backend/__init__.py",
        "src/apps/backend/routes/__init__.py",
    ]
    
    for f in init_files:
        path = Path(f)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
            print(f"✅ {f}")
    
    print("\n🐍 Python 目錄和 __init__.py 建立完成")
else:
    print("⏭️ 不使用 Python，跳過 Python 目錄")
```

**如果使用 TypeScript：**
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

if "TypeScript" in tech_stack or "Node.js" in tech_stack or "React" in tech_stack or "Vue" in tech_stack:
    ts_dirs = [
        "src/contracts/typescript/dto",
        "src/contracts/typescript/interfaces",
    ]
    
    for d in ts_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✅ {d}")
    
    print("\n📦 TypeScript 目錄建立完成")
else:
    print("⏭️ 不使用 TypeScript，跳過 TypeScript 目錄")
```

**如果使用 Rust：**
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

if "Rust" in tech_stack and "無" not in tech_stack.split("Rust")[1][:50]:
    rust_dirs = [
        "src/contracts/rust/dto",
        "src/contracts/rust/interfaces",
    ]
    
    for d in rust_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✅ {d}")
    
    print("\n🦀 Rust 目錄建立完成")
else:
    print("⏭️ 不使用 Rust，跳過 Rust 目錄")
```

### 4. 根據前端框架建立 web 目錄

**讀取前端框架設定並建立對應結構：**
// turbo
```python
from pathlib import Path

tech_stack = Path("docs/tech-stack.md").read_text(encoding="utf-8")

# 判斷前端框架
if "Astro" in tech_stack:
    # Astro + React 結構
    web_dirs = [
        "src/apps/web/src/pages",
        "src/apps/web/src/components",
        "src/apps/web/src/layouts",
        "src/apps/web/src/services",
        "src/apps/web/src/mocks",
        "src/apps/web/src/stores",
        "src/apps/web/public",
    ]
    print("🚀 使用 Astro 結構")
elif "Vue" in tech_stack:
    # Vue 結構
    web_dirs = [
        "src/apps/web/src/pages",
        "src/apps/web/src/components",
        "src/apps/web/src/services",
        "src/apps/web/src/mocks",
        "src/apps/web/src/stores",
        "src/apps/web/src/types",
        "src/apps/web/public",
    ]
    print("💚 使用 Vue 結構")
elif "React" in tech_stack:
    # React 結構（純 React，非 Astro）
    web_dirs = [
        "src/apps/web/src/pages",
        "src/apps/web/src/components",
        "src/apps/web/src/hooks",
        "src/apps/web/src/services",
        "src/apps/web/src/mocks",
        "src/apps/web/src/stores",
        "src/apps/web/public",
    ]
    print("⚛️ 使用 React 結構")
else:
    # 預設結構
    web_dirs = [
        "src/apps/web/src/pages",
        "src/apps/web/src/components",
        "src/apps/web/src/services",
        "src/apps/web/public",
    ]
    print("📁 使用預設 Web 結構")

for d in web_dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    print(f"✅ {d}")

print("\n🌐 Web 目錄建立完成")
```

### 5. 建立其他 apps 目錄（可選）
// turbo
```python
from pathlib import Path

# CLI 和 Desktop 目錄（如果需要）
optional_dirs = [
    "src/apps/cli",
    "src/apps/desktop",
]

for d in optional_dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    print(f"✅ {d}")

print("\n📱 其他 apps 目錄建立完成")
```

### 6. 驗證結構
// turbo
```python
from pathlib import Path

key_dirs = [
    "src/contracts",
    "src/core/domain",
    "src/core/infrastructure",
    "src/core/application",
    "src/apps",
]

print("🔍 驗證目錄結構...")
all_ok = True
for d in key_dirs:
    if Path(d).exists():
        print(f"✅ {d}")
    else:
        print(f"❌ {d} (不存在)")
        all_ok = False

if all_ok:
    print("\n✅ 所有關鍵目錄已建立")
else:
    print("\n⚠️ 部分目錄未建立，請檢查")
```

### 7. 顯示完成訊息
執行完成後，輸出以下訊息：
```
✅ src/ 目錄結構建立完成！

已建立的目錄：
📁 contracts/ - 共享契約
📁 core/ - DDD 三層（domain, infrastructure, application）
📁 apps/ - 介面層（backend, web, cli, desktop）

下一步：
  - 執行 `/setup-agents` 建立 AGENTS.md
```

## 📝 注意事項

1. 此 workflow 是冪等的（可重複執行）
2. 已存在的檔案不會被覆蓋
3. 目錄結構會根據 `docs/tech-stack.md` 動態調整
4. 如果 `docs/tech-stack.md` 不存在，請先執行 `/setup-techstack`

## 🔧 故障排除

如果執行失敗：
1. 確認 `docs/tech-stack.md` 存在
2. 檢查是否在專案根目錄執行
3. 確認有足夠的檔案系統權限
