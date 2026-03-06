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
Write minimal code to make the test pass.

**⚠️ 每個程式檔案必須在 200 行內**，超過則拆分。

**Frontend (Vue)**：遵循 `vue3-development` skill 的開發原則。

**Backend (FastAPI)**：遵循 `fastapi-development` skill 的開發原則。

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

## Skills 引用
- **Frontend**：`vue3-development` skill（Vue 3 開發原則、分層架構、測試慣例）
- **Backend**：`fastapi-development` skill（FastAPI 開發原則、OOP 架構、測試慣例）
- **UI 設計**：`frontend-design` skill + `ui-ux-pro-max` skill（當涉及 UI 開發時啟用）