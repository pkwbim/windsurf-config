---
description: 建立 Hello World 範例專案（前後端串接、Zustand、Logging）
---

# /setup-sample-project

建立完整的 Hello World 範例專案，讓 `make dev` 後可以看到前後端串接的完整範例。

## 📋 前置條件

- 已完成 `/setup-makefile`（Makefile 和依賴檔案已建立）
- 已安裝依賴（`make install`）

---

## 步驟 1：建立 src/storage 目錄結構

// turbo
```bash
python3 << 'EOF'
from pathlib import Path

storage_dirs = [
    "src/storage/database",
    "src/storage/logs",
    "src/storage/cache",
    "src/storage/uploads",
    "src/storage/temp",
]

for d in storage_dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
    gitkeep = Path(d) / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()
    print(f"✅ {d}")

print("\n📁 Storage 目錄結構建立完成")
EOF
```

---

## 步驟 2：建立 .env.example 和 .env

建立 `src/apps/backend/.env.example`：

```bash
# Database
DATABASE_URL=sqlite:///../../storage/database/app.db
LOG_DATABASE_URL=sqlite:///../../storage/database/log.db

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Environment
ENV=development
DEBUG=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=../../storage/logs/app.log
```

建立 `src/apps/web/.env.example`：

```bash
# API
VITE_API_URL=http://localhost:8000

# Environment
NODE_ENV=development
```

複製 `.env.example` 為 `.env`（兩個應用都要）。

---

## 步驟 3：建立 Backend Hello World API

更新 `src/apps/backend/main.py`：

```python
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# 載入環境變數
load_dotenv()

# 設定 logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "../../storage/logs/app.log")

# 確保 log 目錄存在
log_path = Path(__file__).parent / LOG_FILE
log_path.parent.mkdir(parents=True, exist_ok=True)

# 簡單的 logging 設定（使用 loguru）
from loguru import logger

logger.remove()  # 移除預設 handler
logger.add(sys.stderr, level=LOG_LEVEL)  # Console 輸出
logger.add(str(log_path), level=LOG_LEVEL, rotation="10 MB")  # 檔案輸出

app = FastAPI(
    title="Monorepo API",
    description="FastAPI Backend for Monorepo Project",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """記錄每個請求"""
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.get("/")
async def root():
    """根路徑"""
    logger.info("Root endpoint called")
    return {
        "message": "Welcome to Monorepo API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    """健康檢查 API"""
    logger.info("Health check called")
    return {
        "status": "healthy",
        "message": "Hello from FastAPI!",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENV", "development"),
    }


@app.get("/api/hello/{name}")
async def hello(name: str):
    """Hello API - 用於展示前後端串接"""
    logger.info(f"Hello endpoint called with name: {name}")
    return {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 步驟 4：更新 Backend requirements.txt

新增 loguru 依賴：

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pytest==7.4.3
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
loguru==0.7.2
```

---

## 步驟 5：建立 Frontend 首頁

### 5.1 建立 Zustand Store

建立 `src/apps/web/src/stores/apiStore.ts`：

```typescript
import { create } from 'zustand';

interface HealthStatus {
  status: string;
  message: string;
  timestamp: string;
  environment: string;
}

interface ApiStore {
  healthStatus: HealthStatus | null;
  greeting: string | null;
  isLoading: boolean;
  error: string | null;
  fetchHealth: () => Promise<void>;
  fetchGreeting: (name: string) => Promise<void>;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useApiStore = create<ApiStore>((set) => ({
  healthStatus: null,
  greeting: null,
  isLoading: false,
  error: null,

  fetchHealth: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_URL}/api/health`);
      const data = await response.json();
      set({ healthStatus: data, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch health status', isLoading: false });
    }
  },

  fetchGreeting: async (name: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_URL}/api/hello/${encodeURIComponent(name)}`);
      const data = await response.json();
      set({ greeting: data.message, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch greeting', isLoading: false });
    }
  },
}));
```

### 5.2 建立 React 元件

建立 `src/apps/web/src/components/HelloWorld.tsx`：

```tsx
import React, { useEffect, useState } from 'react';
import { useApiStore } from '../stores/apiStore';

export const HelloWorld: React.FC = () => {
  const { healthStatus, greeting, isLoading, error, fetchHealth, fetchGreeting } = useApiStore();
  const [name, setName] = useState('');

  useEffect(() => {
    fetchHealth();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      fetchGreeting(name.trim());
    }
  };

  return (
    <div className="hello-world">
      <h1>🚀 Welcome to Monorepo</h1>
      
      <section className="status-section">
        <h2>Backend Status</h2>
        {isLoading && <p>Loading...</p>}
        {error && <p className="error">{error}</p>}
        {healthStatus && (
          <div className="status-card">
            <p><strong>Status:</strong> {healthStatus.status}</p>
            <p><strong>Message:</strong> {healthStatus.message}</p>
            <p><strong>Environment:</strong> {healthStatus.environment}</p>
            <p><strong>Timestamp:</strong> {healthStatus.timestamp}</p>
          </div>
        )}
      </section>

      <section className="greeting-section">
        <h2>Say Hello</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
          />
          <button type="submit" disabled={isLoading}>
            Say Hello
          </button>
        </form>
        {greeting && <p className="greeting">{greeting}</p>}
      </section>

      <section className="next-steps">
        <h2>📋 Next Steps</h2>
        <ul>
          <li>Check API docs at <a href="http://localhost:8000/docs" target="_blank">/docs</a></li>
          <li>Add your first feature with <code>/build</code> workflow</li>
          <li>Create user stories with <code>/idea</code> workflow</li>
        </ul>
      </section>

      <style>{`
        .hello-world {
          max-width: 800px;
          margin: 0 auto;
          padding: 2rem;
          font-family: system-ui, -apple-system, sans-serif;
        }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 2rem; }
        .status-card {
          background: #f5f5f5;
          padding: 1rem;
          border-radius: 8px;
          margin-top: 1rem;
        }
        .greeting-section form {
          display: flex;
          gap: 0.5rem;
          margin-top: 1rem;
        }
        input {
          padding: 0.5rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          flex: 1;
        }
        button {
          padding: 0.5rem 1rem;
          background: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        button:disabled { opacity: 0.5; }
        .greeting {
          font-size: 1.5rem;
          color: #0070f3;
          margin-top: 1rem;
        }
        .error { color: red; }
        .next-steps ul {
          line-height: 2;
        }
        code {
          background: #f0f0f0;
          padding: 0.2rem 0.4rem;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};
```

### 5.3 更新首頁

更新 `src/apps/web/src/pages/index.astro`：

```astro
---
import { HelloWorld } from '../components/HelloWorld';
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Monorepo - Hello World</title>
  </head>
  <body>
    <HelloWorld client:load />
  </body>
</html>
```

---

## 步驟 6：更新 Makefile 加入 dev-remote

在 Makefile 中加入 `dev-remote` 指令：

```makefile
# Remote development - for Windsurf/SSH access
dev-remote: backend-install frontend-install
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║      Starting Remote Development Environment               ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🌐 Services are listening on 0.0.0.0 (all interfaces)"
	@echo "🎨 Frontend: http://<your-host-ip>:4321"
	@echo "🐍 Backend:  http://<your-host-ip>:8000"
	@echo "📚 API Docs: http://<your-host-ip>:8000/docs"
	@echo ""
	@echo "Press Ctrl+C to stop both servers"
	@echo ""
	@trap 'kill 0' EXIT; \
	(cd src/apps/backend && $(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000) & \
	(cd src/apps/web && npm run dev -- --host 0.0.0.0)
```

---

## 步驟 7：驗證

// turbo
```bash
# 檢查檔案是否都建立
python3 << 'EOF'
from pathlib import Path

files_to_check = [
    "src/storage/database/.gitkeep",
    "src/storage/logs/.gitkeep",
    "src/apps/backend/.env",
    "src/apps/backend/main.py",
    "src/apps/web/.env",
    "src/apps/web/src/stores/apiStore.ts",
    "src/apps/web/src/components/HelloWorld.tsx",
    "src/apps/web/src/pages/index.astro",
]

print("🔍 驗證檔案...")
all_ok = True
for f in files_to_check:
    if Path(f).exists():
        print(f"✅ {f}")
    else:
        print(f"❌ {f}")
        all_ok = False

if all_ok:
    print("\n✅ 所有檔案已建立")
else:
    print("\n⚠️ 部分檔案未建立")
EOF
```

---

## 步驟 8：完成訊息

顯示以下訊息：

```
╔════════════════════════════════════════════════════════════╗
║         🎉 Sample Project Setup Complete!                  ║
╚════════════════════════════════════════════════════════════╝

✅ Storage 目錄結構已建立
✅ 環境變數檔案已建立
✅ Backend Hello World API 已建立
✅ Frontend 首頁已建立（含 Zustand store）
✅ Logging 已設定

🚀 Quick Start:

  # 本地開發
  make dev

  # 遠端開發（Windsurf/SSH）
  make dev-remote

📍 URLs:
  - Frontend: http://localhost:4321
  - Backend:  http://localhost:8000
  - API Docs: http://localhost:8000/docs

📋 Next Steps:
  - /idea     - 新增 User Story 到 backlog
  - /plan     - 將需求轉換為規格
  - /build    - 開始實作開發
```
