---
description: 階段 4 - 建立所有 AGENTS.md 檔案（根據技術棧）
---

## 🎯 目的
根據 `docs/tech-stack.md` 的技術棧設定，建立所有層級的 AGENTS.md 規範檔案。

## 📚 參考資源
- **windsurf-config-manager skill**: 提供 AGENTS.md 的最佳實踐和規範
- 執行前建議參考該 skill 了解 AGENTS.md 的用途和結構

## ⚠️ 重要原則
- **讀取 docs/tech-stack.md**：根據技術棧調整 AGENTS.md 內容
- **不建立目錄**：目錄由 `/setup-project-info` 和 `/setup-structure` 建立
- **內容根據技術棧調整**：例如 web/AGENTS.md 會根據 Vue/React/Astro 調整
- **遵循 AGENTS.md 最佳實踐**：
  - 專注於目錄特定的規範
  - 使用清晰的格式（標題、列表、程式碼區塊）
  - 提供具體範例
  - 避免冗餘（會繼承父目錄的規範）

## 🔗 執行順序
此 workflow 是四階段初始化流程的第四階段：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ✅
3. `/setup-structure` - 建立 src/ 目錄結構 ✅
4. `/setup-agents` - 建立 AGENTS.md ← 你在這裡

---

## 📋 執行步驟

### 1. 讀取技術棧設定
// turbo
```bash
cat docs/tech-stack.md
```

根據 `docs/tech-stack.md` 的內容，判斷：
- 後端語言和框架（Python/FastAPI、Django 等）
- 前端框架（Vue、React、Astro 等）
- 使用的語言（Python、TypeScript、Rust）

### 2. 建立根目錄 AGENTS.md

建立 `/AGENTS.md`，內容包含：
- 專案概述（一人公司完整 monorepo）
- **技術棧章節**（從 docs/tech-stack.md 讀取）
- 目錄結構規範
- 核心開發原則（DDD、OOP、TDD）
- 命名規範
- 開發流程
- 敏感資訊處理

**技術棧章節範例：**
```markdown
## 🛠️ 技術棧

### 後端 (Backend)
- **Python**: {版本}
- **Web 框架**: {框架}
- **ORM**: {ORM}
- **資料庫**: {資料庫}
- **測試框架**: {測試框架}

### 前端 (Frontend)
- **Node.js**: {版本}
- **套件管理器**: {套件管理器}
- **框架**: {框架}
- **狀態管理**: {狀態管理}
- **UI 框架**: {UI框架}
- **前端測試**: {測試框架}
- **整合測試**: {整合測試}

### 開發工具
- **格式化**: {工具}
- **Linter**: {工具}
- **CI/CD**: {工具}
- **容器化**: {工具}

> 詳細說明請參考 `docs/tech-stack.md`
```

### 3. 建立 src/AGENTS.md

建立 `src/AGENTS.md`，內容包含：
- 程式碼層概述
- 目錄結構說明
- 依賴方向規則
- 多語言支援說明（根據技術棧）

### 4. 建立 src/contracts/AGENTS.md

建立 `src/contracts/AGENTS.md`，內容包含：
- 共享契約層職責
- JSON Schema 規範
- DTO 命名規範
- Protocol/Interface 定義規範
- **支援語言章節**（根據技術棧）

**支援語言章節範例：**
```markdown
## 🌐 支援語言

本專案 contracts 支援以下語言：
- **Python**: {版本}
- **TypeScript**: Node.js {版本}
```

### 5. 建立 src/core/AGENTS.md

建立 `src/core/AGENTS.md`，內容包含：
- DDD 三層架構說明
- 依賴方向
- 各層職責
- 測試規範
- **技術棧章節**（根據技術棧）

**技術棧章節範例：**
```markdown
## 🛠️ 技術棧

核心層使用：
- **主要語言**: Python {版本}
- **測試框架**: {測試框架}
```

### 6. 建立 src/apps/AGENTS.md

建立 `src/apps/AGENTS.md`，內容包含：
- 介面層職責
- 各 app 獨立依賴管理
- 路由規範
- 環境變數使用

### 7. 建立 src/apps/backend/AGENTS.md

建立 `src/apps/backend/AGENTS.md`，內容根據後端框架調整：

**如果使用 FastAPI：**
- FastAPI 路由結構
- 依賴注入
- Mock 切換機制
- TDD 流程

**技術棧章節：**
```markdown
## 🛠️ 技術棧

- **Python**: {版本}
- **Web 框架**: FastAPI
- **ORM**: {ORM}
- **資料庫**: {資料庫}
- **測試框架**: {測試框架}
- **格式化**: {格式化工具}
- **Linter**: {Linter}
```

### 8. 建立 src/apps/web/AGENTS.md

建立 `src/apps/web/AGENTS.md`，內容根據前端框架調整：

**如果使用 Astro + React：**
- Astro 頁面結構
- React 元件規範
- Zustand 狀態管理
- API 服務呼叫

**如果使用 Vue：**
- Vue 3 組件結構
- Pinia 狀態管理
- API 服務呼叫

**技術棧章節：**
```markdown
## 🛠️ 技術棧

- **Node.js**: {版本}
- **套件管理器**: {套件管理器}
- **框架**: {框架}
- **狀態管理**: {狀態管理}
- **UI 框架**: {UI框架}
- **前端測試**: {測試框架}
- **整合測試**: {整合測試}
- **格式化**: Prettier
- **Linter**: ESLint
```

### 9. 建立 pm/AGENTS.md

建立 `pm/AGENTS.md`，內容包含：
- 產品管理規範
- planning/ 目錄用途
- discussions/ 命名規範
- decisions/ 命名規範

### 10. 建立 policies/AGENTS.md

建立 `policies/AGENTS.md`，內容包含：
- 政策文件規範
- 版本資訊要求
- 修訂歷史格式

### 11. 建立 scripts/AGENTS.md

建立 `scripts/AGENTS.md`，內容包含：
- 自動化腳本規範
- 腳本命名規範
- 環境變數使用

### 12. 驗證 AGENTS.md 檔案
// turbo
```python
from pathlib import Path

agents_files = [
    "AGENTS.md",
    "src/AGENTS.md",
    "src/contracts/AGENTS.md",
    "src/core/AGENTS.md",
    "src/apps/AGENTS.md",
    "src/apps/backend/AGENTS.md",
    "src/apps/web/AGENTS.md",
    "pm/AGENTS.md",
    "policies/AGENTS.md",
    "scripts/AGENTS.md",
]

print("🔍 驗證 AGENTS.md 檔案...")
all_ok = True
for f in agents_files:
    if Path(f).exists():
        print(f"✅ {f}")
    else:
        print(f"❌ {f} (不存在)")
        all_ok = False

if all_ok:
    print("\n✅ 所有 AGENTS.md 已建立")
else:
    print("\n⚠️ 部分 AGENTS.md 未建立，請檢查")
```

### 13. 顯示完成訊息
執行完成後，輸出以下訊息：
```
✅ 所有 AGENTS.md 建立完成！

已建立的 AGENTS.md：
  - /AGENTS.md (全域規範)
  - src/AGENTS.md (程式碼層)
  - src/contracts/AGENTS.md (契約層)
  - src/core/AGENTS.md (DDD 核心)
  - src/apps/AGENTS.md (介面層)
  - src/apps/backend/AGENTS.md (Backend)
  - src/apps/web/AGENTS.md (Frontend)
  - pm/AGENTS.md (產品管理)
  - policies/AGENTS.md (政策文件)
  - scripts/AGENTS.md (自動化腳本)

🎉 專案初始化完成！

下一步：
  - 執行 `/setup-makefile` 建立 Makefile 和虛擬環境管理
  - 建立完成後即可使用 `make install` 安裝依賴
  - 使用 `/build-ui` 開始 UI 開發
  - 使用 `/build-backend` 開始後端開發
```

## 📝 注意事項

1. 此 workflow 會建立多個 AGENTS.md 檔案
2. 已存在的 AGENTS.md 會被更新（技術棧章節）
3. 內容會根據 `docs/tech-stack.md` 動態調整
4. 如果 `docs/tech-stack.md` 不存在，請先執行 `/setup-techstack`

## 🔧 故障排除

如果執行失敗：
1. 確認 `docs/tech-stack.md` 存在
2. 確認目錄結構已建立（執行 `/setup-structure`）
3. 檢查是否在專案根目錄執行
