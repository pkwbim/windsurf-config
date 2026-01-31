---
description: Deploy Wang-Bot to staging environment (Vue 3 + FastAPI)
auto_execution_mode: 1
---

## Context Files
- `scripts/deploy-stage-v3.sh` - Main deployment script
- `backend/.env.example` - Backend environment template
- `frontend/.env.production` - Frontend production config

## Prerequisites
- SSH access to staging server: `ssh deployuser@localhost`
- Sudo access for Apache configuration (if needed)
- Git repository access

## Deployment Steps

### 1. Pre-deployment Checks
// turbo
```bash
# Check current branch and ensure clean working directory
git status
git branch --show-current

# Verify all tests pass locally
npm test -- --run
pytest
```
- **必須在 `main` 分支進行部署**
- **確保沒有未提交的變更**
- **所有測試必須通過**

### 2. SSH Connection Test
// turbo
```bash
# Test SSH connection to staging server
ssh deployuser@localhost "whoami && pwd"
```
- 確認能夠登入 staging 伺服器
- 驗證使用者權限正確

### 3. Update Staging Code
// turbo
```bash
# Update code on staging server
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && git fetch origin && git reset --hard origin/main"
```
- 拉取最新程式碼
- 重置到最新 main 分支

### 4. Backend Deployment
// turbo
```bash
# Rebuild Python virtual environment and install dependencies
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && rm -rf .venv-backend && python3 -m venv .venv-backend"

# Use explicit path for pip installation to avoid activation issues
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && .venv-backend/bin/pip install --upgrade pip && .venv-backend/bin/pip install -r backend/requirements.txt"

# Setup environment variables BEFORE running migrations
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/backend && cat > .env << 'EOF'
# 資料庫配置
DATABASE_URL=postgresql+asyncpg://wang_bot_user:wang_bot_password@127.0.0.1:5432/staging_wang_bot

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_CHAT_MODEL=gpt-oss-120b
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Azure Speech Service
AZURE_SPEECH_KEY=your_speech_key_here
AZURE_SPEECH_REGION=eastasia

# 應用程式配置
APP_NAME=Wang-Bot AI 品牌客服中台
APP_VERSION=2.0.0
DEBUG=False
CORS_ORIGINS=[\"*\"]

# JWT 配置
SECRET_KEY=your-secret-key-here-please-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Key 驗證（客戶端存取）
API_KEY=iMysKwDbuJZicvMhJ5hA_mWoquK9NLG9HK0OPBET1J8
EOF"

# Run database migrations with explicit path
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/backend && ../.venv-backend/bin/alembic upgrade head"

# Initialize database with explicit path and from correct directory
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/backend && ../.venv-backend/bin/python scripts/init_db.py"
```

### 5. Frontend Deployment
// turbo
```bash
# Install frontend dependencies
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/frontend && npm install"

# Create production environment config
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/frontend && cat > .env.production << 'EOF'
VITE_API_BASE_URL=https://wang-bot.staging.quanzar.com.tw/api
VITE_WS_BASE_URL=wss://wang-bot.staging.quanzar.com.tw/api
VITE_APP_NAME=Wang-Bot (Staging)
EOF"

# Build frontend application
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/frontend && npm run build"

# Copy built files to Apache directory
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && rm -rf public && cp -r frontend/dist public"

# Deploy SPA routing rules (.htaccess)
# NOTE: Without this, direct links like /chat/giguo will 404 on Apache.
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && test -f public/.htaccess || cp public/.htaccess public/.htaccess"
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && cp public/.htaccess public/.htaccess"
```

### 5.1. Fast Path: Run Stage Deploy Script (Recommended)
// turbo
```bash
# If you have access to run the deployment script on the staging server,
# this is faster and less error-prone than running each SSH command manually.
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && bash scripts/deploy-stage-v3.sh"
```

### 6. Service Management
// turbo
```bash
# Stop existing FastAPI service
ssh deployuser@localhost "pkill -f 'uvicorn app.main:app' || true"

# Start new FastAPI service
# Note: Using --workers 1 for WebSocket compatibility
# WebSocket requires single worker mode for proper session handling
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && source .venv-backend/bin/activate && cd backend && nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 > ../logs/fastapi.log 2>&1 &"

# Wait for service to start
sleep 3
```

### 7. Apache Configuration (if needed)
// turbo
```bash
# Check if Apache modules are enabled
ssh deployuser@localhost "sudo a2enmod proxy proxy_http proxy_wstunnel rewrite headers 2>/dev/null || echo 'Modules already enabled'"

# Check if site is enabled
ssh deployuser@localhost "sudo a2ensite wangbot-staging 2>/dev/null || echo 'Site already enabled'"

# Reload Apache configuration (may require sudo access)
ssh deployuser@localhost "sudo systemctl reload apache2 || echo 'Apache reload requires manual intervention'"
```

### 8. Deployment Verification
// turbo
```bash
# Test FastAPI service health
ssh deployuser@localhost "curl -s http://127.0.0.1:8000/health"

# Test API endpoint through Apache proxy
curl -s https://wang-bot.staging.quanzar.com.tw/api/brands | head -3

# Test frontend
curl -s https://wang-bot.staging.quanzar.com.tw/ | grep -o '<title>[^<]*'

# Check service status
ssh deployuser@localhost "ps aux | grep uvicorn | grep -v grep"
```

### 9. Post-deployment Tasks
- **手動檢查環境變數**：確認 `backend/.env` 中的敏感資訊已正確設定
- **測試關鍵功能**：
  - 品牌列表載入
  - 聊天功能
  - 管理面板
- **檢查日誌**：`ssh deployuser@localhost "tail -f /var/www/staging/wang-bot.staging.quanzar.com.tw/logs/fastapi.log"`

## Troubleshooting

### Common Issues

**資料庫權限問題**：
```bash
# 檢查資料庫權限
sudo -u postgres psql -d staging_wang_bot -c "\l"

# 設定正確權限 (以 postgres 超級使用者身份執行)
sudo -u postgres psql -d staging_wang_bot << 'EOF'
-- 1. 確保使用者存在
CREATE USER wang_bot_user WITH PASSWORD 'wang_bot_password';

-- 2. 給予資料庫連線權限
GRANT CONNECT ON DATABASE staging_wang_bot TO wang_bot_user;

-- 3. Schema 權限
GRANT USAGE ON SCHEMA public TO wang_bot_user;

-- 4. 表格和序列權限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO wang_bot_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO wang_bot_user;

-- 5. 預設權限（未來新增的表格）
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO wang_bot_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO wang_bot_user;
EOF

# 重新執行遷移
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw/backend && ../.venv-backend/bin/alembic upgrade head"
```

**虛擬環境路徑問題**：
```bash
# 如果遇到虛擬環境啟動問題，使用絕對路徑
# 不要使用 source activate，直接使用完整路徑
/var/www/staging/wang-bot.staging.quanzar.com.tw/.venv-backend/bin/pip install -r requirements.txt
/var/www/staging/wang-bot.staging.quanzar.com.tw/.venv-backend/bin/alembic upgrade head
/var/www/staging/wang-bot.staging.quanzar.com.tw/.venv-backend/bin/python scripts/init_db.py
```

**權限問題**：
```bash
# Fix virtual environment permissions
sudo chown -R deployuser:deployuser /var/www/staging/wang-bot.staging.quanzar.com.tw/.venv-backend

# Fix public directory permissions  
sudo chown -R www-data:www-data /var/www/staging/wang-bot.staging.quanzar.com.tw/public
```

**API 404 錯誤**：
```bash
# Check Apache proxy configuration
sudo cat /etc/apache2/sites-enabled/wangbot-staging.conf

# Restart Apache
sudo systemctl restart apache2
```

**FastAPI 服務無法啟動**：
```bash
# Check logs
ssh deployuser@localhost "tail -20 /var/www/staging/wang-bot.staging.quanzar.com.tw/logs/fastapi.log"

# Manual start for debugging
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && source .venv-backend/bin/activate && cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
```

### Rollback Procedure
如果部署失敗需要回滾：
```bash
# 回滾到上一個版本
ssh deployuser@localhost "cd /var/www/staging/wang-bot.staging.quanzar.com.tw && git log --oneline -5 && git reset --hard HEAD~1"

# 重啟服務
ssh deployuser@localhost "pkill -f 'uvicorn app.main:app' && cd /var/www/staging/wang-bot.staging.quanzar.com.tw && source .venv-backend/bin/activate && cd backend && nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 > ../logs/fastapi.log 2>&1 &"
```

## Deployment URLs
- **Frontend**: https://wang-bot.staging.quanzar.com.tw
- **Backend API**: https://wang-bot.staging.quanzar.com.tw/api/health
- **API Documentation**: https://wang-bot.staging.quanzar.com.tw/api/docs (if enabled)

## Notes
- 部署前務必確認本地測試通過
- 部署過程中會短暫中斷服務
- 環境變數中的敏感資訊需要手動設定
- 建議在非尖峰時段進行部署
- 部署完成後務必進行完整功能測試
