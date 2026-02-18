# 🚀 技術規格：[Story 標題]

**Story ID**: STORY-{流水號}-{CamelCase描述}
**📊 開發狀態**: 🔵 規劃中
**📁 Story 目錄**: `pm/planning/stories/STORY-{流水號}-{CamelCase描述}/`

**相關文件**：
- Use Cases：`use-cases.md`
- 業務規則：`business-rules.md`
- 開發進度：`checklist.md`

---

## 1. Domain Design (DDD)

### Bounded Context
- **所屬領域**: [例如：Identity, Order, Product 等]
- **Aggregate Root**: [聚合根名稱]
- **領域語言**: [定義此功能的核心術語]

### Entities

| Entity | 屬性 | 業務方法 | 對應 BR |
|--------|------|----------|---------|
| [名稱] | [屬性列表] | [方法列表] | BR-01 |

### Value Objects

| Value Object | 屬性 | 驗證規則 | 對應 BR |
|--------------|------|----------|---------|
| [名稱] | [屬性] | [規則] | BR-02 |

### Use Cases（Application Layer）

| Use Case 類別 | 輸入 DTO | 輸出 DTO | 對應 UC |
|---------------|----------|----------|---------|
| [名稱]UseCase | [名稱]CreateDTO | [名稱]ResponseDTO | UC-01 |

### Contracts (shared_contracts/)
- **Protocol**: `interfaces/[名稱]RepositoryProtocol`
- **DTO**: `dto/[名稱]Create`, `[名稱]Response`, `[名稱]Update`

---

## 2. Backend（Infrastructure Layer）

### Repository
- `[名稱]Repository` - 實作 `[名稱]RepositoryProtocol`

### Models（DB）

| Model | 欄位 | 索引 |
|-------|------|------|
| [名稱] | id, [欄位列表], created_at, updated_at | [索引欄位] |

### API 端點

| Method | Path | Request Body | Response | 對應 UC |
|--------|------|-------------|----------|---------|
| POST | `/api/[resource]` | [名稱]CreateDTO | [名稱]ResponseDTO | UC-01 |
| GET | `/api/[resource]/{id}` | - | [名稱]ResponseDTO | UC-02 |
| PUT | `/api/[resource]/{id}` | [名稱]UpdateDTO | [名稱]ResponseDTO | UC-03 |
| DELETE | `/api/[resource]/{id}` | - | - | UC-04 |

### Database Migration
- [ ] 需要 Migration: 是 / 否
- [ ] Migration 說明: [新增表/修改欄位等]

---

## 3. Frontend

### 頁面與路由

| 頁面名稱 | URL | 元件路徑 | 對應 UC |
|----------|-----|----------|---------|
| [頁面名稱] | `/path` | `views/[名稱].vue` | UC-01 |

### 元件
- [ ] `[元件名稱]` - [說明]

### 路由設定（`frontend/src/router/`）
```javascript
{ path: '/path', component: () => import('@/views/[名稱].vue') }
```

---

## 4. Testing Criteria

### Backend Unit Tests
- [ ] [UseCase 名稱] 單元測試
  - [ ] [測試案例 1]
  - [ ] [測試案例 2]

### Backend Integration Tests
- [ ] API 端點整合測試
  - [ ] `POST /api/[resource]` - [測試案例]
  - [ ] `GET /api/[resource]/{id}` - [測試案例]

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
