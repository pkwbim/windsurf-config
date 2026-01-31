---
description: 階段 3 - Backend 實作（TDD 流程）
---

## 🎯 目的
依據 Protocol 介面，使用 TDD 方式實作真實 Backend 邏輯。

## ⚠️ 重要原則
- **TDD 流程**：Red → Green → Refactor
- **遵循 Protocol**：實作必須符合已定義的介面
- **OOP 設計**：使用物件導向方式封裝業務邏輯
- **檔案限制**：每個檔案不超過 200 行

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
cat pm/planning/02_active.md
```
- 確認已在 feature 分支
- 確認規格已在 `pm/planning/02_active.md`
- 若有前端，確認 Contract 階段已完成

**❗️ 重要：必須完整閱讀 `pm/planning/02_active.md` 的規格內容，理解：**
- User Story 和驗收標準
- Domain Analysis 中的 Entity、Use Case、Contracts
- Technical Requirements 中的 Backend 需求
- Testing Criteria 中的測試項目
- Database Migration 需求

### 1. 讀取 Protocol 介面並對照規格
// turbo
```bash
cat src/contracts/python/interfaces/{feature}_protocol.py
cat src/contracts/python/dto/{feature}.py
ls pm/{story-id}/
```
- 確認需要實作的方法簽名
- 確認輸入輸出格式
- **讀取前一步驟（`/build-contract`）的查核單**，了解已完成的 Contract 設計

**❗️ 強制要求：在開始實作前，必須明確列出以下內容（引用 `pm/planning/02_active.md`）：**

```markdown
## 規格引用
### 來自 pm/planning/02_active.md 的 User Story
> [複製 User Story 內容]

### 來自 pm/planning/02_active.md 的 Domain Entities
> [複製 Domain Analysis > Domain Entities 內容]

### 來自 pm/planning/02_active.md 的 Use Cases
> [複製 Domain Analysis > Use Cases 內容]

### 來自 pm/planning/02_active.md 的 Backend 需求
> [複製 Technical Requirements > Backend 內容]

### 來自 pm/planning/02_active.md 的測試標準
> [複製 Testing Criteria > Backend Unit Tests 內容]

### 來自前一步驟查核單的 Contract 設計
> [複製 /build-contract 查核單中的 Protocol 和 DTO 設計]
```

**若規格不清楚，觸發 CLARIFICATION PROTOCOL，不要自行假設。**

### 2. 建立單元測試（TDD - Red）
在 `src/core/` 對應目錄建立測試檔案（測試與原始碼同目錄）：

**測試檔案命名：** `{feature}_service.unit.py`（與原始碼同目錄）

**測試範例：**
```python
# src/core/application/services/survey_service.unit.py
import pytest
from uuid import uuid4
from src.core.application.services.survey_service import SurveyService

@pytest.mark.asyncio
async def test_create_session():
    """測試建立 session"""
    service = SurveyService()
    result = await service.create_session(
        agent_id=uuid4(),
        customer_data={"name": "測試"}
    )
    
    assert "session_id" in result
    assert result["status"] == "in_progress"

@pytest.mark.asyncio
async def test_process_response_correct_answer():
    """測試正確回答"""
    service = SurveyService()
    # ... 測試邏輯
```

**⚠️ Mock 必須遵循 Protocol：**
- 測試中的 Mock 類別必須實作相同的方法簽名
- Mock 回傳的資料結構必須與 Protocol 定義一致

### 3. 驗證測試失敗（Red）
// turbo
```bash
cd src/core && pytest application/services/{feature}_service.unit.py -v
```
- 測試必須先失敗，證明測試有效

### 4. 實作 DDD 三層架構（Green）
依據 DDD 架構，實作以下三層：

#### 4.1 Domain Layer（領域層）
**建立 Entity：**
```python
# src/core/domain/entities/survey_session_entity.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class SurveySessionEntity:
    """Survey Session 領域實體"""
    id: UUID
    agent_id: UUID
    customer_data: dict
    status: str
    created_at: datetime
    
    def is_completed(self) -> bool:
        """業務邏輯：判斷是否完成"""
        return self.status == "completed"
```

**建立 Use Case：**
```python
# src/core/domain/use-cases/create_survey_session.py
from src.core.domain.entities.survey_session_entity import SurveySessionEntity
from src.contracts.python.interfaces.survey_repository import ISurveyRepository

class CreateSurveySessionUseCase:
    """建立 Survey Session 用例"""
    
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository
    
    async def execute(self, agent_id: UUID, customer_data: dict) -> SurveySessionEntity:
        # 業務邏輯
        entity = SurveySessionEntity(
            id=uuid4(),
            agent_id=agent_id,
            customer_data=customer_data,
            status="in_progress",
            created_at=datetime.now()
        )
        return await self.repository.save(entity)
```

#### 4.2 Infrastructure Layer（基礎設施層）
**建立 Repository：**
```python
# src/core/infrastructure/repositories/survey_repository.py
from src.contracts.python.interfaces.survey_repository import ISurveyRepository
from src.core.domain.entities.survey_session_entity import SurveySessionEntity

class SurveyRepository(ISurveyRepository):
    """Survey Repository 實作"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def save(self, entity: SurveySessionEntity) -> SurveySessionEntity:
        # ORM 操作
        pass
```

#### 4.3 Application Layer（應用層）
**建立 Service：**
```python
# src/core/application/services/survey_service.py
from src.contracts.python.dto.survey import SurveySessionCreate, SurveySessionResponse
from src.core.domain.use_cases.create_survey_session import CreateSurveySessionUseCase
from src.core.infrastructure.repositories.survey_repository import SurveyRepository

class SurveyService:
    """Survey 應用服務 - 編排 Use Case"""
    
    def __init__(self, db: AsyncSession):
        self.repository = SurveyRepository(db)
        self.create_use_case = CreateSurveySessionUseCase(self.repository)
    
    async def create_session(self, dto: SurveySessionCreate) -> SurveySessionResponse:
        # 1. 調用 Use Case
        entity = await self.create_use_case.execute(
            agent_id=dto.agent_id,
            customer_data=dto.customer_data
        )
        # 2. Entity -> DTO
        return SurveySessionResponse.from_entity(entity)
```

**⚠️ DDD 架構原則：**
- **Domain Layer**：純業務邏輯，無 I/O 操作
- **Infrastructure Layer**：資料存取、外部服務
- **Application Layer**：編排 Use Case，DTO 轉換

**檔案超過 200 行時：**
- 拆分為多個 Use Case 類別
- 拆分為多個 Entity 類別
- 提取工具函數到 `utils/`

### 5. 驗證測試通過（Green）
// turbo
```bash
cd src/core && pytest application/services/{feature}_service.unit.py -v
```
- 所有測試必須通過
- 若失敗，回到步驟 4 修正

### 6. 重構（Refactor）
- 改善程式碼品質
- 確保測試仍然通過
- 移除重複程式碼

### 7. 建立 API 端點
在 `src/apps/backend/routes/` 建立或更新 API 路由：

```python
# src/apps/backend/routes/survey.py
from fastapi import APIRouter, Depends
from src.core.application.services.survey_service import SurveyService

router = APIRouter(prefix="/survey", tags=["survey"])

@router.post("/session")
async def create_session(
    request: SurveySessionCreate,
    service: SurveyService = Depends(get_survey_service)
):
    return await service.create_session(
        agent_id=request.agent_id,
        customer_data=request.customer_data
    )
```

### 8. 切換到真實服務（Backend）
在 Backend 中移除 Mock Service 的切換邏輯，直接使用真實服務：

```python
# src/apps/backend/dependencies.py
# 移除 Mock 切換邏輯，直接使用真實服務
from src.core.application.services.survey_service import SurveyService

def get_survey_service(db: AsyncSession = Depends(get_db)):
    return SurveyService(db)
```

**注意：這是 Backend 的設定，不涉及前端程式碼。**

### 9. 建立 Backend 驗證查核單
在 `pm/{story}/` 目錄下建立查核單檔案：

**檔案命名格式：**
```
pm/{story}/CHLT-YYYYMMDDHHMM-{Story}-backend-verification.md
```

**查核單內容結構：**

查核單應包含以下章節：
- 環境設定檢查
- 資料庫檢查  
- API 端點測試（包含測試指令和預期結果）
- DDD 架構驗證
- 錯誤處理測試

**⚠️ 注意：此查核單不包含整合測試項目，因為下一步驟就是整合測試。**

**查核單範例：** 參考 `pm/story-0017/CHLT-202601121756-Story0017-backend-verification.md`

### 10. 自動化測試（依據查核單）
根據查核單內容，撰寫自動化測試：

在 `src/apps/backend/` 建立整合測試檔案：

**測試檔案命名：** `{feature}_api.integration.py`

**測試範例：**
```python
# src/apps/backend/routes/survey_api.integration.py
import pytest
from httpx import AsyncClient
from src.apps.backend.main import app

@pytest.mark.asyncio
async def test_create_endpoint():
    """測試建立端點"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/{endpoint}",
            json={"field": "value"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
```

執行測試並自動更新查核單：
// turbo
```bash
cd src/apps/backend && pytest routes/{feature}_api.integration.py -v
```

**測試通過後，自動在查核單中打勾。**

### 11. 更新開發狀態並提示下一步
更新 `pm/planning/02_active.md`，參考 `.windsurf/templates/dev-status-checklist.md`：
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`)
- [x] **階段 3: Backend 實作** (`/build-backend`) ✅
- [ ] **整合測試** (`/integration`) ⬅️ 下一步
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

告訴使用者：
- ✅ Backend 實作完成，所有自動化測試通過
- 🔜 下一步：`/integration` - 整合測試

---

## 適用場景
- 有 Protocol 介面定義的 Backend 實作
- 純 Backend/API 功能（無前端 UI）
- 需要 TDD 流程的功能開發

## 純 Backend 功能流程
若功能沒有前端 UI（如 Story-0017 Survey Agent）：
1. 跳過 `/build-ui`
2. 可選擇性執行 `/build-contract`（定義 Protocol）
3. 執行 `/build-backend`（TDD 實作）

---

## Tech Stack
- **Framework**: FastAPI 0.115
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL 15+ with pgvector
- **Testing**: pytest + pytest-asyncio
- **Validation**: Pydantic 2
