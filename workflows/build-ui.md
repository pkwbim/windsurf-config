---
description: 階段 1 - 純 UI 開發（不接 API，使用假資料）
---

## 🎯 目的
開發前端 UI 組件，使用寫死的假資料，讓人類先確認 UI 設計和互動流程。

## ⚠️ 重要原則
- **新功能不接 API**：新開發的功能使用寫死的假資料，但**現有功能保持不變**
- **專注 UI/UX**：確保介面設計和使用者體驗正確
- **人類確認後才進下一步**：完成後必須等待人類確認

> **注意**：「不接 API」僅針對本次新開發的 UI 組件。現有已完成的頁面和功能不需要修改，保持原有的 API 連接。

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
cat _planning/02_active.md
```
- 確認已在 feature 分支
- 確認規格已在 `02_active.md`
- 確認此 Story 需要前端 UI（若純 Backend 功能，請改用 `/build-backend`）

**⚠️ 重要：必須完整閱讀 `02_active.md` 的規格內容，理解：**
- User Story 和驗收標準
- Domain Analysis 中的 Entity 和 Use Case
- Technical Requirements 中的 Frontend 需求
- Testing Criteria 中的測試項目

### 1. 分析 UI 需求（必須引用規格）
**⚠️ 強制要求：在開始實作前，必須明確列出以下內容（引用 `02_active.md`）：**

```markdown
## 規格引用
### 來自 02_active.md 的 User Story
> [複製 User Story 內容]

### 來自 02_active.md 的 Frontend 需求
> [複製 Technical Requirements > Frontend 內容]

### 來自 02_active.md 的驗收標準（UI 相關）
> [複製相關驗收標準]
```

從規格中提取：
- 需要哪些頁面/組件
- UI 互動流程
- 需要顯示的資料結構

**若規格不清楚，觸發 CLARIFICATION PROTOCOL，不要自行假設。**

### 2. 建立組件與假資料
**Vue 3 組件開發原則：**
- 使用 `<script setup>` 語法
- 使用 Composition API
- 假資料直接寫在組件內或 composable 中

**假資料範例：**
```javascript
// 在組件內直接定義假資料
const mockData = ref([
  { id: 1, name: '測試項目 1', status: 'active' },
  { id: 2, name: '測試項目 2', status: 'pending' },
])
```

**檔案結構：**
```
frontend/src/
├── views/           # 頁面組件
├── components/      # UI 組件
└── composables/     # 可重用邏輯（含假資料）
```

### 3. 設定路由（如需要）
若有新頁面，更新 `frontend/src/router/index.js`

### 4. 組件測試（可選）
```bash
cd frontend && npm test -- --run
```
- 測試組件是否正確渲染
- 測試基本互動行為

### 5. 啟動開發伺服器
```bash
cd frontend && npm run dev
```

### 6. 更新開發狀態
更新 `_planning/02_active.md`，參考 `.windsurf/templates/dev-status-checklist.md`：
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`) ✅
- [ ] **階段 2: API Contract 設計** (`/build-contract`) ⬅️ 下一步
- [ ] **階段 3: Backend 實作** (`/build-backend`)
- [ ] **整合測試** (`/integration`)
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

告訴使用者：
- ✅ UI 開發完成
- 🔜 下一步：`/build-contract` - API Contract 設計

### 7. 產生查核單（Checklist）
**⚠️ 重要：此步驟不可跳過！**

**查核單命名規則：**
- 位置：`pm/{story-id}/`
- 檔名：`CHLT-{年月日時分}-{Story編號}-{階段}.md`
- 範例：`pm/story-0017/CHLT-202601120430-Story0017-build-ui.md`

**查核單內容結構：**
```markdown
---
story_id: Story-0017
phase: build-ui
status: pending
created_at: 2026-01-12T04:30:00Z
---

# UI 開發查核單

## 📋 基本資訊
- **Story**: Story-0017 電訪機器人
- **階段**: 階段 1 - 純 UI 開發
- **開發伺服器**: http://localhost:5173

## ✅ 查核項目

### 已完成的頁面/組件
- [ ] O / [ ] X - {頁面/組件名稱}
  - 路徑：{URL 路徑}
  - 說明：{簡短說明}

### UI/UX 驗證
- [ ] O / [ ] X - UI 設計是否符合預期
- [ ] O / [ ] X - 互動流程是否正確
- [ ] O / [ ] X - 假資料顯示是否合理
- [ ] O / [ ] X - 響應式設計是否正常

## 📝 補充說明
（請在此填寫任何問題、建議或補充說明）

答：


## 🎯 驗證結果
- [ ] ✅ 全部通過，可進入下一階段
- [ ] ❌ 需要修改

---
**填寫完成後，請回覆「已填寫查核單」**
```

**產生查核單後：**
1. 建立 `pm/{story-id}/` 目錄（如不存在）
2. 產生查核單檔案
3. 告訴使用者查核單位置
4. **停止並等待使用者填寫**

### 8. 處理查核單回覆
使用者回覆「已填寫查核單」後：
1. 讀取查核單內容
2. 檢查驗證結果
3. **若需修改**：
   - 根據補充說明進行調整
   - 修改完成後 commit
   - **產生新版本查核單**（版本號 +1）
   - 在新查核單中標記「已修正」的項目
   - 告訴使用者新查核單位置並等待再次驗證
4. **若全部通過**：
   - 更新查核單狀態為 `status: completed`
   - 更新 `02_active.md` 並提示下一步

**⚠️ 重要規則：每次修改後都必須產生新版本查核單！**
- 第一次：`CHLT-{時間}-Story{編號}-build-ui.md`
- 修改後：`CHLT-{時間}-Story{編號}-build-ui-v2.md`
- 再修改：`CHLT-{時間}-Story{編號}-build-ui-v3.md`
- 依此類推...

### 9. 提示下一步
收到確認後，告訴使用者：
- ✅ UI 階段完成
- 🔜 下一步：執行 `/build-contract` 定義介面與 Mock API

---

## 適用場景
- 有前端 UI 的功能開發
- 需要先確認 UI 設計再實作 Backend

## 不適用場景
- 純 Backend/API 功能 → 請使用 `/build-backend`
- 只需修改現有 UI → 可直接修改，不需完整流程
