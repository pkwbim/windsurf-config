# 🚀 Current Task: [Story 標題]

**📊 開發狀態**: 🔵 規劃中

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

---

## 1. User Story (Source)
> [在此填寫使用者故事]

### 需求背景
- [背景說明]

### 驗收標準
- [ ] [標準 1]
- [ ] [標準 2]

---

## 2. Domain Analysis (DDD)

### Bounded Context
- **所屬領域**: [例如：Survey, Chat, Brand 等]
- **領域語言**: [定義此功能的核心術語]

### Domain Entities
- [ ] **新增 Entity**: `backend/app/domain/entities/`
  - [實體名稱] - [屬性與業務方法]
- [ ] **修改 Entity**: 
  - [實體名稱] - [修改內容]

### Use Cases
- [ ] **新增 Use Case**: `backend/app/domain/use_cases/`
  - [用例名稱] - [輸入/輸出/業務規則]

### Contracts (shared_contracts/)
- [ ] **Protocol**: `interfaces/`
  - [介面名稱] - [方法定義]
- [ ] **DTO**: `dto/`
  - [名稱]Create, [名稱]Response, [名稱]Update

---

## 3. Technical Requirements

### Backend (Infrastructure Layer)
- **Repository**: `backend/app/domain/repositories/`
  - [ ] [名稱]Repository - [說明]
- **新增/修改 Models**: `backend/app/models/`
  - [ ] [Model 名稱] - [說明]
- **API 端點**: `backend/app/api/`
  - [ ] `GET /api/...` - [說明]
  - [ ] `POST /api/...` - [說明]
- **Services**: `backend/app/services/`
  - [ ] [Service 名稱] - 實作 Protocol 介面

### Frontend
- **新增頁面**: `frontend/src/views/`
  - [ ] [頁面路徑] - [說明]
- **修改頁面**:
  - [ ] [頁面路徑] - [修改內容]
- **新增元件**: `frontend/src/components/`
  - [ ] [元件名稱]
- **路由變更**: `frontend/src/router/`
  - [ ] [路由說明]

### Database Migration
- [ ] 需要 Migration: 是 / 否
- [ ] Migration 說明: [新增表/修改欄位等]

---

## 4. Testing Criteria

### Backend Unit Tests
- [ ] [Service 名稱] 單元測試
  - [ ] [測試案例 1]
  - [ ] [測試案例 2]

### Backend Integration Tests
- [ ] API 端點整合測試
  - [ ] [測試案例 1]
  - [ ] [測試案例 2]

### Frontend Tests (Optional)
- [ ] [元件名稱] 測試
  - [ ] [測試案例 1]

### Manual Testing
- [ ] [手動測試項目 1]
- [ ] [手動測試項目 2]

---

## 5. Implementation Notes

### 開發重點
- [重點 1]
- [重點 2]

### 技術挑戰
- [挑戰 1]
- [挑戰 2]

### 相依性
- [ ] 依賴 Story: [Story ID]
- [ ] 依賴功能: [功能說明]

---

## 6. Migration 執行步驟

**⚠️ 重要：整合測試通過後，執行 Migration 前才能進行人工驗證**

```bash
# 1. 檢查目前版本
cd backend
source ../.venv-backend/bin/activate
alembic current

# 2. 創建 Migration（若需要）
alembic revision --autogenerate -m "描述"

# 3. 檢查 Migration 檔案
# 查看 backend/alembic/versions/ 中的新檔案

# 4. 執行 Migration
alembic upgrade head

# 5. 驗證
alembic current
```

---

## 7. Commit Messages

### 範例
```
feat: 實作 [功能名稱]
test: 新增 [測試名稱]
docs: 更新 [文件名稱]
chore: 執行資料庫 migration
```
