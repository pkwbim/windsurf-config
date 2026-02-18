# 開發進度：[Story 標題]

**Story ID**: STORY-{流水號}-{CamelCase描述}
**📊 開發狀態**: 🔵 規劃中
**📁 Story 目錄**: `pm/planning/stories/STORY-{流水號}-{CamelCase描述}/`

## 開發階段檢查清單 (UI-First 流程)
- [ ] 需求規劃完成 (`/plan`)
- [ ] **階段 1: 純 UI 開發** (`/build-ui`) - 若無 UI 可跳過
  - [ ] UI 元件開發（使用寫死假資料）
  - [ ] 路由設定
  - [ ] 人工驗證 UI
- [ ] **階段 2: API Contract 設計** (`/build-contract`)
  - [ ] Protocol 介面定義 (`shared-contracts/interfaces/`)
  - [ ] Pydantic Schemas (`backend/app/schemas/`)
  - [ ] Mock API 實作 (`backend/app/mocks/`)
  - [ ] 前端接上 Mock API
  - [ ] 人工驗證 Contract
- [ ] **階段 3: Backend TDD 實作** (`/build-backend`)
  - [ ] 單元測試撰寫 (TDD Red)
  - [ ] 功能實作完成 (TDD Green)
  - [ ] 程式碼重構 (TDD Refactor)
  - [ ] 整合測試通過 (`/integration`)
  - [ ] **資料庫 Migration** (若有新增/修改 Model)
  - [ ] 人工驗證通過
- [ ] 文件更新完成 (`/review`)
- [ ] Story 已歸檔 (`/review`)
- [ ] 已合併到 main (`/merge`)
