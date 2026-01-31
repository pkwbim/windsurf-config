---
description: Standard workflow for implementing features with TDD approach (Vue + FastAPI)
auto_execution_mode: 1
---

## Context Files
- `_planning/02_active.md` - Current task specification
- `.agents.md` - Agent configuration

## Implementation Steps

### 0. Git Branch Setup
// turbo
```bash
git branch --show-current
```
- 分支建立應在 `/plan` 階段完成
- 如果目前仍在 `main`：停止並提醒先執行 `/plan` 以建立 `feat/<story-id>` 分支
- 如果已在 feature 分支：繼續後續實作

### 1. Read & Validate Spec
// turbo
```bash
cat _planning/02_active.md
```
- Ensure requirements are clear before writing tests
- Verify spec follows the template structure:
  - 1. User Story
  - 2. Technical Requirements
  - 3. Testing Criteria

### 2. Create Test Case (TDD - Red)
Generate test file based on feature:

**Frontend (Vue):**
- Test directory: `frontend/tests/unit/` or `frontend/src/**/__tests__/`
- Naming convention: `*.spec.js` or ComponentName.spec.js
- Use Vitest with Vue Test Utils
- Example test structure:
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Component from '@/components/Component.vue'

describe('Component', () => {
  it('should render correctly', () => {
    const wrapper = mount(Component)
    expect(wrapper.exists()).toBe(true)
  })
})
```

**Backend (FastAPI):**
- Test directory: `backend/tests/`
- Naming convention: `test_*.py`
- Use pytest with async support
- **⚠️ Mock 必須遵循 Protocol**：
  - 所有 Service 都應定義 Protocol（`app/services/protocols.py`）
  - 測試中的 Mock 類別必須實作相同的方法簽名
  - Mock 回傳的資料結構必須與真實 Service 一致（特別是 dict/list 結構）
  - 加上型別提示確保介面一致性
- Example test structure:
```python
import pytest
from httpx import AsyncClient
from app.main import app
from app.services.protocols import ServiceProtocol  # 引入 Protocol

@pytest.mark.asyncio
async def test_api_endpoint():
    # Mock 類別遵循 Protocol
    class FakeService:
        """測試用 Mock（遵循 ServiceProtocol）"""
        async def method(self, param: str) -> dict:
            return {"key": "value"}  # 回傳真實結構
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/endpoint")
        assert response.status_code == 200
```

### 3. Verify Test Failure (Red)
// turbo
```bash
# Frontend (Vue)
npm test -- --run

# Backend (FastAPI)
pytest
```
- The test MUST fail first to prove it checks the right thing

### 4. Implement Logic
Write minimal code to make the test pass:

**⚠️ Code File Size Limit:**
- **每個程式檔案必須在 200 行內**
- 若超過 200 行，必須拆分為多個模組或類別
- 拆分原則：
  - 按功能職責拆分（Single Responsibility Principle）
  - 提取共用邏輯到獨立模組
  - 大型組件拆分為子組件
  - 服務層拆分為多個專門服務

**Frontend (Vue):**
- **使用 Composition API + Composables 模式（函數式組合）**
- Follow Vue 3 Composition API patterns
- Use `<script setup>` syntax for components
- Implement reactive data with `ref` and `reactive`
- Use Pinia for state management if needed

**Frontend 開發原則（Functional Composition）：**
- **組合優於繼承**：使用 composables 組合功能，而非類別繼承
- **關注點分離**：UI 組件 vs 業務邏輯 vs 狀態管理
- **可重用性**：提取共用邏輯到 composables
- **單一職責**：每個 composable 只負責一個功能領域
- **響應式設計**：善用 Vue 的響應式系統（ref, reactive, computed, watch）

**分層架構：**
```
frontend/src/
├── components/        # UI 組件（純展示邏輯）
├── composables/       # 可重用的組合式函數（業務邏輯）
├── services/          # API 呼叫和外部服務
├── stores/            # Pinia 狀態管理
└── views/             # 頁面組件（組合多個組件）
```

**範例結構：**
```javascript
// composables/useFeature.js
export function useFeature() {
  const data = ref([])
  const loading = ref(false)
  
  async function fetchData() {
    loading.value = true
    // 業務邏輯
    loading.value = false
  }
  
  return { data, loading, fetchData }
}

// Component.vue
<script setup>
import { useFeature } from '@/composables/useFeature'
const { data, loading, fetchData } = useFeature()
</script>
```

- **檔案超過 200 行時**：
  - 拆分為子組件（`components/Feature/SubComponent.vue`）
  - 提取 composables（`composables/useFeature.js`）
  - 分離業務邏輯到 services（`services/featureService.js`）
  - 拆分複雜狀態到 stores（`stores/featureStore.js`）

**Backend (FastAPI):**
- **必須使用 OOP（物件導向程式設計）思維建構程式**
- Follow FastAPI best practices with async/await
- Use Pydantic models for request/response validation
- Implement dependency injection for services
- Use SQLAlchemy async sessions for database operations

**OOP 開發原則：**
- **封裝（Encapsulation）**：將業務邏輯封裝在類別中，避免純函數式程式設計
- **單一職責（Single Responsibility）**：每個類別只負責一個功能領域
- **依賴注入（Dependency Injection）**：使用 FastAPI 的依賴注入系統
- **介面定義（Protocol/ABC）**：定義清晰的介面契約
- **繼承與多型（Inheritance & Polymorphism）**：適當使用繼承和多型特性

**範例結構：**
```python
# services/feature_service.py
class FeatureService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_feature(self, data: FeatureCreate) -> Feature:
        # 業務邏輯封裝在方法中
        pass
    
    async def get_feature(self, id: int) -> Feature:
        pass
```

- **檔案超過 200 行時**：
  - 拆分 API 路由到多個檔案（`api/feature_routes.py`）
  - 分離服務邏輯到多個類別（`services/feature_service.py`）
  - 提取工具類別（`utils/feature_utils.py`）
  - 拆分資料模型（`models/feature_models.py`）
  - 定義 Protocol 介面（`services/protocols.py`）

### 5. Verify Test Success (TDD - Green)
// turbo
```bash
# Frontend (Vue)
npm test -- --run

# Backend (FastAPI)
pytest
```
- If tests fail, loop back to step 4
- Continue until all tests pass

### 6. Refactor & Clean
- Improve code quality while maintaining functionality
- Ensure all tests still pass after refactoring

**Frontend:**
- Extract reusable composables
- Optimize component re-renders
- Clean up imports and unused code

**Backend:**
- Extract service layers and repositories
- Optimize database queries
- Add proper error handling and logging

### 7. Update Task Status
完成單元測試後，更新 `_planning/02_active.md` 的狀態：

```markdown
# 🚀 Current Task: [Story Name] (Story-XXX)

**📊 開發狀態**: ✅ Build 完成 → 待整合測試

## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] 單元測試撰寫 (TDD Red)
- [x] 功能實作完成 (TDD Green)
- [x] 程式碼重構 (TDD Refactor)
- [ ] **整合測試通過** (`/integration`) ⬅️ 下一步
- [ ] 人工驗證通過
- [ ] 程式碼已提交 (`/commit`)
- [ ] 已合併到 main (`/merge`)

## 下一步行動
執行 `/integration` 進行整合測試
```

### 8. 🛑 人工驗證檢查點（MANDATORY）
**⚠️ 重要：此步驟不可跳過！**

完成整合測試後，**必須**停下來等待使用者進行人工驗證：

1. **提供驗證指南**：
   - 如果有相關的人工驗證文件（如 `docs/docker-manual-verification.md`），提供連結
   - 列出需要驗證的關鍵功能點
   - 提供具體的驗證指令或步驟

2. **明確告知使用者**：
   ```
   ⚠️ 請進行人工驗證
   
   已完成自動化測試，現在需要您進行人工驗證：
   
   📋 驗證項目：
   - [ ] [功能點 1]
   - [ ] [功能點 2]
   - [ ] [功能點 3]
   
   📖 驗證指南：[連結到相關文件]
   
   ✅ 驗證完成後，請回覆「驗證通過」或「好」以繼續下一步
   ❌ 如發現問題，請描述問題以便修正
   ```

3. **等待使用者回應**：
   - **不要自動執行 `/review`**
   - **不要假設驗證已通過**
   - 等待使用者明確回覆後才繼續

4. **收到確認後**：
   - 更新 `_planning/02_active.md` 標記「人工驗證通過」
   - 提示使用者執行 `/review` 或 `/commit`

### 9. 提示下一步
告訴使用者：
- ✅ Build 階段完成
- 📝 已更新開發狀態
- 🔜 下一步：執行 `/integration` 進行整合測試
- ⚠️ 整合測試後需要人工驗證
 
## Notes
- Always follow TDD: Red → Green → Refactor
- Keep implementation minimal and focused
- **文件更新在 `/review` 階段處理**
 
## Tech Stack Specifics
 
### Frontend (Vue 3 + Vite)
- Test runner: Vitest
- Test utilities: Vue Test Utils
- Test environment: happy-dom
- Component testing: Use mount from Vue Test Utils
- API testing: Mock API calls with vi.mock
- **API Contract testing: `ApiContract.spec.js` 確保前後端資料格式一致**
- **Router Config testing: `RouterConfig.spec.js` 確保所有路由都正確配置，避免 404**
- **Router Links testing: `RouterLinks.spec.js` 確保組件內的 router-link 引用有效路由**

### 路由測試注意事項
當功能涉及新的 URL 路徑時，**必須**同時：
1. 在 `router/index.js` 新增路由配置
2. 在 `RouterConfig.spec.js` 新增對應測試
3. 測試應驗證：
   - 路由是否存在（不會 404）
   - 路由參數是否正確解析
   - 路由名稱是否正確

```javascript
// 路由配置測試範例
it('should have route for /admin/brands/:slug/:tab', async () => {
  const resolved = router.resolve('/admin/brands/wangsteak/tone')
  expect(resolved.matched.length).toBeGreaterThan(0)
  expect(resolved.name).toBe('admin-brand-panel-tab')
  expect(resolved.params.slug).toBe('wangsteak')
  expect(resolved.params.tab).toBe('tone')
})
```

### Backend (FastAPI + Python)
- Test runner: pytest
- Async testing: pytest-asyncio (configured)
- Test client: httpx.AsyncClient
- Database testing: Use pytest fixtures for test DB
- Coverage: pytest-cov (configured)