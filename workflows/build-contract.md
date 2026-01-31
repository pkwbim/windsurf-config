---
description: 階段 2 - API Contract 設計（定義介面 + Mock API）
---

## 🎯 目的
定義前後端介面契約（Python Protocol），實作 Mock API，讓前端接上 Mock 進行驗證。

## ⚠️ 重要原則
- **介面先行**：先定義 Protocol，再實作 Mock
- **Mock 必須符合 Protocol**：確保 Mock 回傳格式與未來真實 API 一致
- **Mock 長期保留**：Mock 程式碼保留供測試使用，透過環境變數切換
- **前端建立 API 服務**：建立 API 服務模組（如 `surveyAPI.js`）
- **人類確認後才進下一步**

> **Mock API 策略**：詳見 `docs/mock-api-strategy.md`
> - Mock 主要用於介面契約驗證
> - 已有功能不需要額外建立 Mock
> - Mock 程式碼長期保留（單元測試需要）
> - 預設使用真實服務，透過環境變數切換 Mock

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
cat _planning/02_active.md
ls pm/{story-id}/
```
- 確認 UI 階段已完成（若有 UI）
- 確認規格中的 API 需求
- **讀取前一步驟（`/build-ui`）的查核單**（若有），了解 UI 需要的資料結構

**⚠️ 重要：必須完整閱讀 `02_active.md` 的規格內容，理解：**
- User Story 和驗收標準
- Domain Analysis 中的 Contracts（DTO 定義）
- Technical Requirements 中的 Backend API 需求
- Testing Criteria 中的測試項目

### 1. 定義 Python Protocol（介面）- 必須引用規格
**⚠️ 強制要求：在開始實作前，必須明確列出以下內容（引用 `02_active.md`）：**

```markdown
## 規格引用
### 來自 02_active.md 的 User Story
> [複製 User Story 內容]

### 來自 02_active.md 的 Contracts (DTO)
> [複製 Domain Analysis > Contracts 內容]

### 來自 02_active.md 的 Backend API 需求
> [複製 Technical Requirements > Backend 中的 API 端點需求]

### 來自前一步驟查核單的 UI 資料需求（若有）
> [複製 /build-ui 查核單中 UI 需要的資料結構]
```

**若規格不清楚，觸發 CLARIFICATION PROTOCOL，不要自行假設。**

**Protocol 定義：**
在 `shared-contracts/interfaces/` 目錄建立介面定義：

**目錄結構：**
```
shared-contracts/
└── interfaces/
    ├── __init__.py
    └── {feature}_protocol.py
```

**Protocol 範例：**
```python
# shared-contracts/interfaces/survey_protocol.py
from typing import Protocol, Optional
from uuid import UUID
from shared_contracts.dto.survey import (
    SurveySessionCreate,
    SurveySessionResponse,
    SurveyResponseInput,
    SurveyResponseOutput
)

class SurveyServiceProtocol(Protocol):
    """電訪服務介面"""
    
    async def create_session(
        self, 
        request: SurveySessionCreate
    ) -> SurveySessionResponse:
        """建立電訪 session"""
        ...
    
    async def process_response(
        self, 
        request: SurveyResponseInput
    ) -> SurveyResponseOutput:
        """處理使用者回應"""
        ...
```

**⚠️ Protocol 使用 DTO 類型的優點：**
- 型別明確，IDE 支援好
- 自動文件生成（FastAPI Swagger）
- 減少參數傳遞錯誤

### 2. 定義 Pydantic DTO (Data Transfer Objects)
在 `shared-contracts/dto/` 建立對應的 Request/Response DTOs：

**⚠️ 重要：DTO 放在 shared-contracts，不是 backend/app/schemas/**

```python
# shared-contracts/dto/survey.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime

# Request DTOs
class SurveySessionCreate(BaseModel):
    """建立 Survey Session 請求"""
    agent_id: UUID = Field(..., description="Agent UUID")
    customer_data: Dict[str, Any] = Field(..., description="客戶資料")

# Response DTOs
class SurveySessionResponse(BaseModel):
    """建立 Session 回應"""
    session_id: UUID
    status: str
    next_question: str
    progress: str
```

**為什麼放在 shared-contracts？**
- DTO 是前後端共用的資料契約
- 前端可以參考 Python DTO 手動編寫 TypeScript 介面
- 符合 DDD 的 Shared Kernel 概念
- 已有功能（Brand, Agent）保持在 `backend/app/schemas/`（漸進式改進）

### 3. 實作 Mock API
在 `backend/app/mocks/` 目錄建立 Mock 實作：

**目錄結構：**
```
backend/app/
└── mocks/
    ├── __init__.py
    └── {feature}_mock.py
```

**Mock 範例：**
```python
# backend/app/mocks/survey_mock.py
from uuid import UUID, uuid4
from shared_contracts.dto.survey import (
    SurveySessionCreate,
    SurveySessionResponse,
    SurveyResponseInput,
    SurveyResponseOutput
)

class SurveyServiceMock:
    """電訪服務 Mock 實作"""
    
    async def create_session(
        self, 
        request: SurveySessionCreate
    ) -> SurveySessionResponse:
        session_id = uuid4()
        customer_name = request.customer_data.get("姓名", "未知")
        
        return SurveySessionResponse(
            session_id=session_id,
            status="in_progress",
            next_question=f"您好，請問是{customer_name}先生/小姐嗎？",
            progress="1/10"
        )
    
    async def process_response(
        self, 
        request: SurveyResponseInput
    ) -> SurveyResponseOutput:
        return SurveyResponseOutput(
            session_id=request.session_id,
            status="in_progress",
            reply="好的，謝謝您的確認。",
            next_question="感謝您的回答，下一題...",
            progress="2/10",
            judgment="correct"
        )
```

**⚠️ Mock 必須回傳 DTO 物件，不是 Dict！**

### 4. 建立 Mock API 端點
在 `backend/app/api/` 建立使用 Mock 的 API 端點：

```python
# backend/app/api/survey.py
from fastapi import APIRouter, HTTPException
from shared_contracts.dto.survey import (
    SurveySessionCreate,
    SurveySessionResponse,
    SurveyResponseInput,
    SurveyResponseOutput
)
from app.config import settings

router = APIRouter(prefix="/api/survey", tags=["survey"])

# 根據環境變數決定使用 Mock 或真實服務
if settings.use_mock_survey:
    from app.mocks.survey_mock import SurveyServiceMock
    survey_service = SurveyServiceMock()
else:
    # ⚠️ Contract 階段：真實服務尚未實作
    # 暫時 fallback 到 Mock，避免 import error
    from app.mocks.survey_mock import SurveyServiceMock
    survey_service = SurveyServiceMock()
    
    # 🎯 Backend 階段完成後，改為：
    # from app.services.survey_service import SurveyService
    # survey_service = SurveyService()

@router.post("/session", response_model=SurveySessionResponse)
async def create_session(request: SurveySessionCreate):
    """建立電訪 session"""
    try:
        # 直接傳遞 DTO 物件，不需要解包參數
        result = await survey_service.create_session(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**環境變數設定：**
```python
# backend/app/config.py
class Settings(BaseSettings):
    use_mock_survey: bool = False  # 預設使用真實服務
```

**⚠️ API 端點直接傳遞 DTO 物件，不要解包參數！**

### 5. 前端建立 API 服務
建立專用的 API 服務模組（不要在組件內直接寫假資料）：

```javascript
// frontend/src/services/surveyAPI.js
const API_BASE_URL = '/api'

export const surveyAPI = {
  createSession: (data) => {
    return fetch(`${API_BASE_URL}/survey/session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json())
  },
  
  getSessions: (params) => {
    const query = new URLSearchParams(params)
    return fetch(`${API_BASE_URL}/survey/sessions?${query}`)
      .then(res => res.json())
  }
}
```

**組件使用 API 服務：**
```javascript
// 組件內使用
import { surveyAPI } from '@/services/surveyAPI'

const sessions = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const result = await surveyAPI.getSessions()
    sessions.value = result.sessions
  } catch (error) {
    console.error('Failed to load sessions:', error)
  } finally {
    loading.value = false
  }
})
```

**⚠️ 注意：**
- ✅ 前端組件不需要判斷 Mock/真實 API（Backend 統一處理）
- ✅ 已有功能（如 Brand、Agent）不需要額外建立 Mock
- ✅ 只有新功能在 `/build-contract` 階段需要 Mock

### 6. API Contract 測試
建立前端 API Contract 測試：

```javascript
// frontend/tests/unit/ApiContract.spec.js
describe('Survey API Contract', () => {
  it('should return expected response format', async () => {
    const response = await surveyAPI.createSession({...})
    expect(response).toHaveProperty('session_id')
    expect(response).toHaveProperty('status')
  })
})
```

### 7. 更新開發狀態
更新 `_planning/02_active.md`，參考 `.windsurf/templates/dev-status-checklist.md`：
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`) ✅
- [ ] **階段 3: Backend 實作** (`/build-backend`) ⬅️ 下一步
- [ ] **整合測試** (`/integration`)
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

告訴使用者：
- ✅ API Contract 設計完成
- 🔜 下一步：`/build-backend` - Backend 實作（TDD）

### 8. 🛑 產生查核單並等待人工驗證（MANDATORY）
**⚠️ 重要：此步驟不可跳過！**

**產生查核單檔案**：在 `pm/{story-id}/` 目錄建立查核單：

檔名格式：`CHLT-{YYYYMMDD}-{HHMM}-{StoryId}-build-contract.md`

```markdown
---
story_id: {Story-ID}
phase: build-contract
status: pending
created_at: {ISO timestamp}
---

# API Contract 查核單

## 📋 基本資訊
- **Story**: {Story ID} {Story 標題}
- **階段**: 階段 2 - API Contract 設計
- **API 文件**: http://localhost:8000/docs

## ✅ 查核項目

### Protocol 介面定義
- [ ] O / [ ] X - Protocol 檔案已建立（`shared_contracts/interfaces/`）
- [ ] O / [ ] X - 方法簽名與 DTO 類型正確
- [ ] O / [ ] X - 文件註解完整

### Pydantic DTO
- [ ] O / [ ] X - Request/Response DTO 已定義（`shared_contracts/dto/`）
- [ ] O / [ ] X - 欄位類型與驗證規則正確
- [ ] O / [ ] X - 範例資料合理

### Mock API
- [ ] O / [ ] X - Mock 服務已實作（`backend/app/mocks/`）
- [ ] O / [ ] X - Mock 回傳格式符合 DTO
- [ ] O / [ ] X - API 端點可正常呼叫

### 前端整合
- [ ] O / [ ] X - 前端 API 服務已建立（`frontend/src/services/`）
- [ ] O / [ ] X - 前端可正確呼叫 Mock API
- [ ] O / [ ] X - 資料流程符合預期

## 📁 相關檔案
- Protocol: `{protocol_file_path}`
- DTO: `{dto_file_path}`
- Mock: `{mock_file_path}`
- API: `{api_file_path}`

## 📝 補充說明
（請在此填寫任何問題、建議或補充說明）

答：


## 🎯 驗證結果
- [ ] ✅ 全部通過，可進入下一階段
- [ ] ❌ 需要修改

---
**填寫完成後，請回覆「已填寫查核單」**
```

**告訴使用者**：
```
⚠️ 請進行 API Contract 人工驗證

已產生查核單：`pm/{story-id}/CHLT-{timestamp}-build-contract.md`

請填寫查核單後回覆「已填寫查核單」
```

**然後停止，等待使用者回應。**

### 9. 提示下一步
收到確認後，告訴使用者：
- ✅ Contract 階段完成
- 🔜 下一步：執行 `/build-backend` 實作真實 Backend（TDD）

---

## 適用場景
- UI 階段完成後，需要定義 API 介面
- 需要前後端分離開發
- 需要明確的介面契約

## 不適用場景
- 純 Backend 功能（無前端）→ 可跳過此步驟，直接 `/build-backend`
- 簡單的 API 修改 → 可直接修改，不需完整流程
