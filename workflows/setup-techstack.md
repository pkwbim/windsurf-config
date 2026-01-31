---
description: 設定專案技術棧 - 詢問並更新所有 AGENTS.md 檔案中的技術棧資訊
---

## 🎯 目的
透過 `/discussion` 流程，收集專案的技術棧選擇，並記錄到 `docs/tech-stack.md`。

## ⚠️ 重要原則
- **使用 /discussion 流程**：透過討論檔案收集技術棧資訊
- **必須停下來等待**：產生討論檔案後，必須等待使用者回覆
- **只記錄到 docs/tech-stack.md**：不更新 AGENTS.md（由 `/setup-agents` 負責）

## 🔗 執行順序
此 workflow 是四階段初始化流程的第二階段：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ← 你在這裡
3. `/setup-structure` - 建立 src/ 目錄結構
4. `/setup-agents` - 建立 AGENTS.md

---

## 📋 執行步驟

### 1. 建立技術棧討論檔案

在 `discussions/` 資料夾建立討論檔案：

**檔案命名格式：**
```
discussions/DISC-YYYYMMDDHHMM-TechStackSetup.md
```

**檔案內容：**
```markdown
# 討論主題：專案技術棧設定

## 📋 背景說明
設定專案使用的技術棧，這些資訊將會更新到所有相關的 AGENTS.md 檔案中。

## ❓ 技術棧問卷

### 🐍 Python 相關

**問題 1：Python 版本**
例：3.11、3.12、3.13

答：

---

**問題 2：Web 框架**
例：FastAPI、Django、Flask、無

答：

---

**問題 3：ORM**
例：SQLAlchemy、Tortoise ORM、無

答：

---

**問題 4：資料庫**
例：PostgreSQL、MySQL、SQLite、MongoDB

答：

---

**問題 5：測試框架**
例：pytest、unittest

答：

---

### 🦀 Rust 相關（如不使用請填「無」）

**問題 6：Rust 版本**
例：1.75、stable、無

答：

---

**問題 7：Rust 用途**
例：核心運算、CLI 工具、WebAssembly、無

答：

---

**問題 8：主要 crates**
例：tokio、serde、axum、無

答：

---

### 📦 TypeScript/Node.js 相關

**問題 9：Node.js 版本**
例：20、22

答：

---

**問題 10：套件管理器**
例：npm、pnpm、yarn、bun

答：

---

### 💚 Vue 相關（如不使用請填「無」）

**問題 11：Vue 版本**
例：Vue 3、無

答：

---

**問題 12：Vue 狀態管理**
例：Pinia、Vuex、無

答：

---

**問題 13：Vue UI 框架**
例：Vuetify、Element Plus、PrimeVue、Nuxt UI、無

答：

---

**問題 14：Vue 建置工具**
例：Vite、Nuxt、無

答：

---

### ⚛️ React 相關（如不使用請填「無」）

**問題 15：React 版本**
例：React 18、React 19、無

答：

---

**問題 16：React 狀態管理**
例：Zustand、Redux、Jotai、無

答：

---

**問題 17：React UI 框架**
例：shadcn/ui、MUI、Ant Design、無

答：

---

**問題 18：React 建置工具**
例：Vite、Next.js、無

答：

---

### 🛠️ 開發工具

**問題 19：程式碼格式化**
例：Prettier、Black、Ruff

答：

---

**問題 20：Linter**
例：ESLint、Ruff、Clippy

答：

---

**問題 21：CI/CD**
例：GitHub Actions、GitLab CI、無

答：

---

**問題 22：容器化**
例：Docker、無

答：

---
```

### 2. 通知使用者並停止

告訴使用者：

```
我已建立技術棧討論檔案：`discussions/DISC-YYYYMMDDHHMM-TechStackSetup.md`

請在檔案中回答所有問題。完成後，請告訴我「我已回答」，我會繼續處理。

⚠️ 在您回答之前，我不會執行任何動作。
```

**然後完全停止，不執行任何其他動作。**

### 3. 等待使用者回覆
- 使用者會說「我已回答」或類似的話
- **只有在使用者明確表示已回答後，才繼續下一步**

### 4. 讀取並確認技術棧

讀取討論檔案，整理成摘要：

```
📦 技術棧摘要

後端 (Backend):
- Python: {版本} + {框架} + {ORM} + {資料庫}
- Rust: {版本} + {用途}
- 測試: {測試框架}

前端 (Frontend):
- Node.js: {版本} ({套件管理器})
- Vue: {版本} + {狀態管理} + {UI框架}
- React: {版本} + {狀態管理} + {UI框架}

工具:
- 格式化: {工具}
- Linter: {工具}
- CI/CD: {工具}

確認以上資訊正確嗎？(Y/N)
```

**等待使用者確認後，才繼續下一步。**

### 5. 建立/更新 docs/tech-stack.md

確認後，將技術棧資訊寫入 `docs/tech-stack.md`：

```markdown
# 技術棧

> 建立日期：{日期}
> 討論檔案：`discussions/DISC-YYYYMMDDHHMM-TechStackSetup.md`

## 後端 (Backend)

### Python
- **版本**: {版本}
- **Web 框架**: {框架}
- **ORM**: {ORM}
- **資料庫**: {資料庫}
- **測試框架**: {測試框架}

### Rust（如有使用）
- **版本**: {版本}
- **用途**: {用途}
- **主要 crates**: {crates}

## 前端 (Frontend)

### Node.js
- **版本**: {版本}
- **套件管理器**: {套件管理器}

### Vue（如有使用）
- **版本**: {版本}
- **狀態管理**: {狀態管理}
- **UI 框架**: {UI框架}
- **建置工具**: {建置工具}

### React（如有使用）
- **版本**: {版本}
- **狀態管理**: {狀態管理}
- **UI 框架**: {UI框架}
- **建置工具**: {建置工具}

## 開發工具

- **格式化**: {工具}
- **Linter**: {工具}
- **CI/CD**: {工具}
- **容器化**: {工具}
```

**注意：不要在此階段更新 AGENTS.md，由 `/setup-agents` 負責。**

### 6. 建立/更新依賴檔案（可選）

根據技術棧選擇，可以建立以下檔案（或留給 `/setup-structure`）：

- `src/apps/backend/requirements.txt` - Python 依賴
- `src/apps/web/package.json` - Node.js 依賴
- `src/contracts/rust/Cargo.toml` - Rust 依賴（如果使用）

### 7. 顯示完成訊息

```
✅ 技術棧設定完成！

已更新的檔案：
- docs/tech-stack.md

下一步：
- 執行 `/setup-structure` 建立 src/ 目錄結構
- 執行 `/setup-agents` 建立 AGENTS.md
```

## 📝 注意事項

1. 此 workflow 只更新 `docs/tech-stack.md`
2. 不會更新 AGENTS.md（由 `/setup-agents` 負責）
3. 如果某些技術不使用，可以回答「無」或「不使用」
4. 可以重複執行此 workflow 來更新技術棧
