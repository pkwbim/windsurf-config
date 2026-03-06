---
name: fastapi-development
description: FastAPI 後端開發原則與慣例。當建立或修改 FastAPI 路由、服務、模型、測試時自動啟用。適用於使用 FastAPI + SQLAlchemy + PostgreSQL 技術棧的後端開發。觸發時機：建立 .py 後端檔案、修改 API 端點、撰寫後端測試、處理資料庫操作。
---

# FastAPI 開發原則

## 技術棧
- FastAPI 0.115
- SQLAlchemy 2.0 (async)
- PostgreSQL 15+ with pgvector
- Pydantic 2（Request/Response 驗證）
- pytest + pytest-asyncio
- httpx.AsyncClient（測試客戶端）

## 開發模式

使用 **OOP（物件導向程式設計）思維**建構程式：
- 業務邏輯封裝在類別中
- FastAPI 依賴注入系統管理服務
- Pydantic models 定義 Request/Response
- SQLAlchemy async sessions 處理資料庫操作

## 核心原則

- **封裝**：業務邏輯封裝在類別中，避免純函數式程式設計
- **單一職責**：每個類別只負責一個功能領域
- **依賴注入**：使用 FastAPI 的 `Depends` 系統
- **介面定義**：使用 Protocol/ABC 定義清晰的介面契約
- **每個檔案不超過 200 行**

## 分層架構

```
backend/app/
├── api/               # API 路由（薄層，只負責接收和回傳）
├── services/          # 業務邏輯服務
├── models/            # SQLAlchemy ORM 模型
├── schemas/           # Pydantic Request/Response schemas
├── core/              # 核心設定（config, security, api_key）
└── utils/             # 工具函數
```

## Service 範例

```python
# services/feature_service.py
class FeatureService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: FeatureCreate) -> Feature:
        # 業務邏輯封裝在方法中
        pass

    async def get_by_id(self, id: int) -> Feature:
        pass
```

## Mock 必須遵循 Protocol

- 所有 Service 應定義 Protocol（`app/services/protocols.py`）
- 測試中的 Mock 類別必須實作相同的方法簽名
- Mock 回傳的資料結構必須與真實 Service 一致
- 加上型別提示確保介面一致性

## 檔案超過 200 行時

- 拆分 API 路由到多個檔案（`api/feature_routes.py`）
- 分離服務邏輯到多個類別（`services/feature_service.py`）
- 提取工具類別（`utils/feature_utils.py`）
- 拆分資料模型（`models/feature_models.py`）
- 定義 Protocol 介面（`services/protocols.py`）

## 測試慣例

- 測試目錄：`backend/tests/`
- 命名：`test_*.py`
- 使用 pytest + pytest-asyncio
- 測試客戶端：httpx.AsyncClient
- 資料庫測試使用 pytest fixtures

```python
@pytest.mark.asyncio
async def test_api_endpoint():
    class FakeService:
        """測試用 Mock（遵循 ServiceProtocol）"""
        async def method(self, param: str) -> dict:
            return {"key": "value"}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/endpoint")
        assert response.status_code == 200
```
