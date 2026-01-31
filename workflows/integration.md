---
description: 整合測試流程 - 建置並執行 Frontend + Backend 整合測試
---

## 🎯 目的
在 `/build-backend` 完成後，建立整合測試查核單並執行自動化整合測試，驗證 Frontend + Backend 的協作流程。

## ⚠️ 重要原則
- **先建立查核單**：在 `pm/{story}/` 目錄下建立整合測試查核單
- **自動化優先**：能自動化的測試項目必須自動化
- **人工測試補充**：只有無法自動化的項目才進行人工測試
- **使用 `make test`**：所有測試都要能透過 `make test` 執行

---

## 執行步驟

### 1. 讀取測試場景
// turbo
```bash
cat _planning/02_active.md
```
查找測試場景和驗收條件。

### 2. 讀取 Backend 驗證查核單
// turbo
```bash
find pm/ -name "CHLT-*-backend-verification.md" -type f | head -1 | xargs cat
```
了解 Backend 階段已經測試過哪些項目，避免重複測試。

### 3. 確認前置條件
- `/build-ui` 階段已完成（若有前端）
- `/build-contract` 階段已完成（若有 API）
- `/build-backend` 階段已完成，單元測試通過
- Backend 驗證查核單已完成

---

## 建立整合測試查核單

### 4. 建立查核單檔案
在 `pm/{story}/` 目錄下建立查核單：

**檔案命名格式：**
```
pm/{story}/CHLT-YYYYMMDDHHMM-{Story}-integration.md
```

**使用 Template：**
```bash
cp .windsurf/templates/checklist-integration.md pm/{story}/CHLT-YYYYMMDDHHMM-{Story}-integration.md
```

**查核單內容結構：**

查核單應包含以下章節：
- 測試環境確認
- Frontend 整合測試項目（自動化）
- Backend 整合測試項目（自動化）
- Frontend + Backend 協作測試（自動化）
- 無法自動化的人工測試項目（若有）

**⚠️ 注意：**
- 每個測試項目都要標註是「自動化」還是「人工」
- 避免重複測試 Backend 已驗證的項目
- 專注在「整合」層面的測試

---

## 撰寫自動化測試

### 5. 撰寫 Frontend 整合測試

**⚠️ 重要：Frontend 整合測試建議在 Backend 測試中一起完成**

由於 Frontend 需要呼叫真實 Backend API，但我們希望使用測試資料庫（SQLite in-memory），最佳做法是在 **Backend 整合測試**中一起測試 Frontend 的流程。

#### 方式 A：在 Backend 測試中測試完整流程（推薦）✅

測試目錄：`backend/tests/integration/`
命名規範：`test_{feature}_integration.py`

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_complete_user_flow(async_client):
    """測試完整的使用者流程（包含 Frontend 會做的操作）"""
    # 這裡的 async_client 會使用測試資料庫（SQLite in-memory）
    
    # 1. 建立資源（模擬 Frontend POST 請求）
    response = await async_client.post("/api/resources", json={
        "name": "Test Resource"
    })
    assert response.status_code == 201
    resource = response.json()
    assert resource["id"] is not None
    
    # 2. 取得資源列表（模擬 Frontend GET 請求）
    response = await async_client.get("/api/resources")
    assert response.status_code == 200
    resources = response.json()
    assert len(resources) > 0
    assert resources[0]["name"] == "Test Resource"
    
    # 3. 更新資源（模擬 Frontend PUT 請求）
    response = await async_client.put(f"/api/resources/{resource['id']}", json={
        "name": "Updated Resource"
    })
    assert response.status_code == 200
    
    # 4. 驗證更新成功
    response = await async_client.get(f"/api/resources/{resource['id']}")
    assert response.status_code == 200
    updated_resource = response.json()
    assert updated_resource["name"] == "Updated Resource"
```

**優點：**
- ✅ 使用測試資料庫（SQLite in-memory）
- ✅ 不會污染開發資料庫
- ✅ 測試完整的 API 流程
- ✅ 速度快，可重複執行

#### 方式 B：Frontend 單獨測試（僅測試 UI 邏輯）

測試目錄：`frontend/tests/integration/`
命名規範：`{Feature}Integration.spec.js`

```javascript
import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import ComponentA from '@/views/ComponentA.vue'
import { someAPI } from '@/services/api'

// Mock API，專注測試 Frontend 邏輯
vi.mock('@/services/api', () => ({
  someAPI: {
    getAll: vi.fn(),
    create: vi.fn()
  }
}))

describe('Frontend Integration Tests - UI Logic', () => {
  it('should display resources from API', async () => {
    // Mock API 回應
    someAPI.getAll.mockResolvedValue([
      { id: 1, name: 'Resource 1' },
      { id: 2, name: 'Resource 2' }
    ])
    
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', component: ComponentA }]
    })
    
    router.push('/')
    await router.isReady()
    
    const wrapper = mount(ComponentA, {
      global: { plugins: [router] }
    })
    await flushPromises()
    
    // 驗證 UI 正確顯示
    expect(wrapper.text()).toContain('Resource 1')
    expect(wrapper.text()).toContain('Resource 2')
  })
})
```

**⚠️ 注意：此方式使用 Mock，不會測試真實 Backend**

### 6. 路由配置測試（必須）

**整合測試無法發現路由配置問題！** 當功能涉及新 URL 時，必須在 `RouterConfig.spec.js` 新增測試：

```javascript
// frontend/tests/unit/RouterConfig.spec.js
it('should have route for /admin/brands/:slug/:tab', async () => {
  const resolved = router.resolve('/admin/brands/wangsteak/tone')
  expect(resolved.matched.length).toBeGreaterThan(0)
  expect(resolved.params.tab).toBe('tone')
})
```

---

## 執行測試

### 7. 執行全部測試
// turbo
```bash
make test
```

這會執行：
- Backend 單元測試 + 整合測試
- Frontend 單元測試 + 整合測試

### 8. 更新查核單結果
根據測試結果，更新查核單：
- ✅ 測試通過的項目打勾
- ❌ 測試失敗的項目標註原因
- 記錄測試輸出摘要

---

## 人工測試（若有需要）

### 9. 執行人工測試
若查核單中有無法自動化的項目：

1. 啟動開發環境
   ```bash
   make dev
   ```

2. 根據查核單進行人工測試

3. 在查核單中記錄人工測試結果

**常見無法自動化的項目：**
- 視覺樣式驗證
- 複雜的使用者互動流程
- 第三方服務整合（LINE、Azure 等）

---

## 完成

### 10. 更新開發狀態並提示下一步
更新 `_planning/02_active.md`，參考 `.windsurf/templates/dev-status-checklist.md`：
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`)
- [x] **階段 3: Backend 實作** (`/build-backend`)
- [x] **整合測試** (`/integration`) ✅
- [ ] 文件更新 (`/review`) ⬅️ 下一步
- [ ] 已合併到 main (`/merge`)
```

告訴使用者：
- ✅ 整合測試完成，查核單已更新
- 🔜 下一步：`/review` - 更新文件並歸檔

---

## 與其他 Workflow 的關係
- `/plan` → 定義測試場景和驗收條件
- `/build-ui` → 純 UI 開發
- `/build-contract` → API Contract 設計
- `/build-backend` → Backend 實作（TDD）
- `/integration` → 整合測試（本 workflow）⬅️
- `/review` → 文件更新並歸檔
- `/merge` → 所有測試通過後才合併
