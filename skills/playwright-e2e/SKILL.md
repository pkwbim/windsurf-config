---
name: playwright-e2e
description: E2E 測試規範 skill，補充 webapp-testing skill 沒有的部分。定義測試目錄規範、DB 隔離策略、依 e2e-scenarios.md 撰寫測試的規範、測試資料建立方式。與 webapp-testing skill 互補使用。
---

# Playwright E2E 測試規範

> **與 `webapp-testing` skill 的分工：**
> - `webapp-testing`：Playwright 執行方式（server 啟動、DOM 偵測、截圖、`with_server.py`）
> - 本 skill（`playwright-e2e`）：E2E 測試規範（目錄、DB 隔離、劇本撰寫、測試資料）

---

## 1. 測試目錄規範

### 判斷流程
```
執行 /integration-e2e 時：
1. 讀取專案根目錄的 AGENTS.md
2. 尋找 E2E / Browser / 整合測試目錄的說明
3. 若找到 → 使用該目錄
4. 若找不到 → 詢問使用者，並建議以下慣例：
   - Laravel：src/app/tests/E2E/
   - FastAPI+Vue：tests/e2e/
5. 取得指示後，將目錄路徑加入 AGENTS.md
```

### 命名規範
```
tests/E2E/
├── {Feature}Test.py          # 對應 e2e-scenarios.md 的劇本群組
└── conftest.py               # 共用 fixture（登入、DB 設定）
```

範例：
```
tests/E2E/
├── ProfilesTest.py           # 對應 S-01 ~ S-07
├── AuthTest.py               # 對應登入/登出劇本
└── conftest.py
```

---

## 2. DB 隔離策略

### 原則
- **絕對不污染開發 DB**
- 使用獨立測試 DB，測試結束後 rollback 或清除

### Laravel 做法
啟動 server 時指定 `--env=testing`，使用 `.env.testing` 的 DB：

```bash
# 啟動測試用 server（使用測試 DB）
php artisan serve --port=8234 --env=testing

# 測試前 migrate + seed
php artisan migrate:fresh --seed --env=testing
```

在 `conftest.py` 中管理測試資料：
```python
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    subprocess.run(
        ["php", "artisan", "migrate:fresh", "--seed", "--env=testing"],
        cwd="src/app", check=True
    )
    yield
    # 測試結束後可選擇性清除
```

### FastAPI+Vue 做法
使用 `.env.test` 指向獨立測試 DB：
```bash
# 啟動測試用 server
APP_ENV=test uvicorn app.main:app --port=8000
```

---

## 3. 依 e2e-scenarios.md 撰寫測試

### 對應規則
每個 `S-XX` 劇本對應一個 test function：

```python
# e2e-scenarios.md 的 S-01 → test_s01_create_profile_solar
def test_s01_create_profile_solar(page):
    """S-01：成功建立命盤人物（陽曆）"""
    # 依劇本的「操作步驟」逐步實作
    # 依劇本的「預期結果」撰寫 assert
```

### 測試結構模板
```python
import pytest
from playwright.sync_api import Page, expect

class TestProfiles:
    """對應 e2e-scenarios.md 的 Profiles 劇本群組"""

    def test_s01_create_profile_solar(self, page: Page, logged_in_user):
        """S-01：成功建立命盤人物（陽曆）"""
        # 操作步驟
        page.goto("http://127.0.0.1:8234/profiles")
        page.click("text=新增人物")
        # ...
        # 預期結果
        expect(page).to_have_url("http://127.0.0.1:8234/profiles")
        expect(page.locator("text=王小明")).to_be_visible()

    def test_s02_create_profile_lunar(self, page: Page, logged_in_user):
        """S-02：成功建立命盤人物（農曆）"""
        pass
```

### 共用 fixture（conftest.py）
```python
import pytest
from playwright.sync_api import Page

@pytest.fixture
def logged_in_user(page: Page):
    """登入測試帳號"""
    page.goto("http://127.0.0.1:8234/login")
    page.fill('input[name="email"]', "test@example.com")
    page.fill('input[name="password"]', "password")
    page.click('button[type="submit"]')
    page.wait_for_url("**/dashboard")
    return page
```

---

## 4. 測試資料建立方式

### Laravel（Factory via Artisan）
```python
import subprocess

def create_test_user():
    """建立測試使用者"""
    subprocess.run([
        "php", "artisan", "tinker", "--execute",
        "User::factory()->create(['email' => 'test@example.com', 'password' => bcrypt('password')])"
    ], cwd="src/app", check=True)

def create_test_profile(user_id: int):
    """建立測試人物"""
    subprocess.run([
        "php", "artisan", "tinker", "--execute",
        f"Profile::factory()->create(['user_id' => {user_id}])"
    ], cwd="src/app", check=True)
```

### FastAPI（Fixture）
```python
@pytest.fixture
def test_user(db_session):
    user = User(email="test@example.com", hashed_password=hash_password("password"))
    db_session.add(user)
    db_session.commit()
    return user
```

---

## 5. 執行方式

參考 `webapp-testing` skill 的 `with_server.py` 啟動 server：

```bash
# Laravel（使用測試 DB）
python .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd src/app && php artisan serve --port=8234 --env=testing" \
  --port 8234 \
  -- pytest tests/E2E/ -v

# FastAPI+Vue
python .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd backend && APP_ENV=test uvicorn app.main:app --port=8000" --port 8000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- pytest tests/e2e/ -v
```

---

## 6. 注意事項

- **先讀 `e2e-scenarios.md`**：每個 test function 必須對應一個劇本
- **先讀 `webapp-testing` skill**：DOM 偵測、截圖、selector 選取方式參考該 skill
- **測試前確認 server 未運行**：避免 port 衝突（`with_server.py` 會自動管理）
- **Alpine.js 互動**：需要 `page.wait_for_load_state('networkidle')` 後再操作
