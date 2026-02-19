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
- 使用獨立測試 DB，每個 test class 開始前 `migrate:fresh`

### Laravel 做法
啟動 server 時指定 `--env=testing`，使用 `.env.testing` 的 DB：

```bash
# 啟動測試用 server（使用測試 DB）
php artisan serve --port=8234 --env=testing

# 測試前 migrate + seed（由 conftest.py 的 setup_db fixture 自動執行）
php artisan migrate:fresh --env=testing --force
php artisan db:seed --class=E2ETestSeeder --env=testing --force
```

### FastAPI+Vue 做法
使用 `.env.test` 指向獨立測試 DB：
```bash
# 啟動測試用 server
APP_ENV=test uvicorn app.main:app --port=8000
```

---

## 2a. .env.testing 必要設定（Laravel）

E2E 測試的 `.env.testing` **必須**包含以下設定，否則 session 或 CSRF 會失敗：

```ini
# Session 必須用 file，不能用 array（array 在真實瀏覽器請求間不持久）
SESSION_DRIVER=file

# APP_URL 必須與實際 server 一致（含 port），否則 CSRF token 驗證失敗
APP_URL=http://127.0.0.1:8234
```

**常見錯誤症狀：**
- `SESSION_DRIVER=array` → 登入後下一個請求就失去 session，表單送出後被 redirect 到 `/logout`
- `APP_URL` 不含 port → CSRF token 驗證失敗，POST 被 redirect 到 `/logout`

---

## 3. 測試架構：流程式測試（Positive）+ 獨立測試（Negative）

### 核心概念

**正向測試（Positive）→ 流程式**：整個 class 共用一個 `flow_page`，依序執行 UC，每步建立在前一步的結果上。
- S-01 建立資料 → S-02 繼續建立 → S-03 驗證列表 → S-06 編輯 → S-07 刪除
- 不依賴 Seeder 提供資料，測試本身就是資料的來源

**負向測試（Negative）→ 獨立**：每個測試用 `logged_in` fixture（function scope），互相隔離。

### 對應規則
每個 `S-XX` 劇本對應一個 test function，正向測試用 `flow_page`，負向測試用 `logged_in`：

```python
# 正向：S-01 → test_s01_create_xxx（用 flow_page）
def test_s01_create_xxx(self, flow_page: Page):
    """S-01：成功建立..."""

# 負向：S-E01 → test_se01_xxx（用 logged_in）
def test_se01_xxx(self, logged_in: Page):
    """S-E01：驗證失敗..."""
```

### 測試結構模板
```python
import pytest
from playwright.sync_api import Page, Browser, expect
from conftest import BASE_URL, TEST_EMAIL, TEST_PASSWORD


@pytest.fixture(scope="class")
def flow_page(browser: Browser, setup_db):
    """整個 positive class 共用一個 page，登入一次，依序執行所有 UC。"""
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="email"]', TEST_EMAIL)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    yield page
    context.close()


class TestFeaturePositive:
    """正向劇本：流程式，共用同一個已登入 page"""

    def test_s01_create(self, flow_page: Page):
        """S-01：建立資料"""
        page = flow_page
        # 操作...
        # 驗證...

    def test_s02_view(self, flow_page: Page):
        """S-02：查看（S-01 建立的資料）"""
        page = flow_page
        # 繼續操作...


class TestFeatureNegative:
    """負向劇本：每個測試獨立"""

    def test_se01_validation_error(self, logged_in: Page):
        """S-E01：驗證失敗"""
        page = logged_in
        # 操作...
```

### 共用 fixture（conftest.py）
```python
import os
import subprocess
import pytest
from playwright.sync_api import Page

BASE_URL = "http://127.0.0.1:8234"
TEST_EMAIL = "test_e2e@example.com"
TEST_PASSWORD = "password"

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))


def _fresh_db():
    """migrate:fresh + E2ETestSeeder"""
    subprocess.run(
        ["php", "artisan", "migrate:fresh", "--env=testing", "--force"],
        cwd=APP_DIR, check=True,
    )
    subprocess.run(
        ["php", "artisan", "db:seed", "--class=E2ETestSeeder", "--env=testing", "--force"],
        cwd=APP_DIR, check=True,
    )


@pytest.fixture(scope="class", autouse=True)
def setup_db():
    """每個 test class 開始前做 migrate:fresh，確保乾淨狀態"""
    _fresh_db()
    yield


@pytest.fixture
def logged_in(page: Page):
    """登入測試帳號，回傳已登入的 page（function scope，負向測試用）"""
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="email"]', TEST_EMAIL)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    return page
```

> **⚠️ 重要：`APP_DIR` 必須用絕對路徑**（`os.path.abspath`），避免 `with_server.py` 環境下相對路徑失效。

---

## 4. 測試資料建立方式

### 策略：流程式建立（推薦，取代 Seeder 策略）

**核心原則：正向測試自己建立資料，不依賴 Seeder。**

- S-01 建立人物 → S-02 再建立另一人物 → S-07 刪除 S-02 建立的人物
- 資料由測試流程本身產生，不需要額外的 Seeder
- `setup_db`（class scope）在每個 class 開始前 `migrate:fresh`，確保乾淨狀態

```python
# ✅ 正確：流程式，S-07 刪除 S-02 建立的資料
def test_s02_create(self, flow_page: Page):
    """S-02：建立陳小花"""
    # 建立資料...

def test_s07_delete(self, flow_page: Page):
    """S-07：刪除陳小花（S-02 建立的）"""
    chen_row = page.locator('[data-profile-name="陳小花"]').first
    chen_row.locator('button[title="刪除"]').click()
    # ...
```

### ⚠️ 驗證「已刪除」的正確做法

刪除後不要用 `not_to_be_visible()`（strict mode 下多個匹配會報錯），改用：

```python
# ✅ 正確：確認 data-* 行數為 0
expect(page.locator('[data-profile-name="陳小花"]')).to_have_count(0)

# ✅ 或：確認成功訊息 + 目標人物仍存在
expect(page.locator("text=人物已成功刪除")).to_be_visible()
expect(page.get_by_role("link", name="王大明").first).to_be_visible()

# ❌ 錯誤：strict mode 下若有多個同名元素會 AssertionError
expect(page.get_by_role("link", name="陳小花")).not_to_be_visible()
```

### E2ETestSeeder 的職責

`E2ETestSeeder` 只負責建立**測試帳號**（user），不建立業務資料：

```php
// E2ETestSeeder.php
User::create([
    'name'     => 'E2E Test User',
    'email'    => 'test_e2e@example.com',
    'password' => Hash::make('password'),
]);
```

業務資料（如 Profile）由測試流程的 `flow_page` 測試步驟自己建立。

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
# Laravel（從 .env.testing 讀取 APP_PORT，不寫死 port）
APP_PORT=$(grep '^APP_PORT=' src/app/.env.testing | cut -d'=' -f2)
python3 .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd src/app && php artisan serve --port=${APP_PORT} --env=testing" \
  --port ${APP_PORT} \
  -- .venv/bin/pytest src/tests/ -v

# FastAPI+Vue
python3 .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd backend && APP_ENV=test uvicorn app.main:app --port=8000" --port 8000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- pytest tests/e2e/ -v
```

---

## 5.5 撰寫測試前：UI 可測性檢查（必做）

> **目的：** 確認 Blade 實作有照 `page-{name}.md` 的「🧪 可測試性規範」加上 `data-*` 屬性。這同時也是 UI 程式碼級的可測性檢查。

```bash
# 1. 讀取此頁面的 page spec（了解應有哪些 data-* 屬性）
cat pm/planning/stories/{active_story}/pages/page-{name}.md

# 2. 讀取對應的 Blade 模板（確認實作有照規格）
cat src/app/resources/views/{path}.blade.php
```

**檢查項目：**
- [ ] `page-{name}.md` 的 🧪 區塊列出的所有 `data-*` 屬性，在 Blade 中都有對應實作
- [ ] 操作按鈕/連結有 `title` 屬性（如 `title="編輯"`、`title="刪除"`）
- [ ] 若有不一致，**先修正 Blade**，再撰寫測試

---

## 6. Playwright Selector 規範（Laravel + Alpine.js）

### 按鈕點擊
```python
# ✅ 正確：用 role + name，避免匹配到多個 button[type="submit"]
page.get_by_role("button", name="儲存人物").click()
page.get_by_role("button", name="刪除").click()

# ❌ 錯誤：可能匹配到多個元素
page.click('button[type="submit"]')
```

### 等待與 URL 驗證
```python
# ✅ 正確：navigation event 可能已過，用 expect 更穩定
from playwright.sync_api import expect
expect(page).to_have_url(f"{BASE_URL}/profiles")

# ❌ 錯誤：navigation event 已過時會 timeout
page.wait_for_url(f"{BASE_URL}/profiles")
```

### type="date" input（Alpine.js 環境）
```python
# ✅ 正確：用 evaluate 設定值並觸發 input/change event，確保 Alpine.js 感知
page.evaluate("""
    const el = document.querySelector('input[name="birth_date_solar"]');
    el.value = '1990-05-15';
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
""")

# ❌ 錯誤：page.fill 對 type="date" 不可靠，Alpine.js 可能感知不到
page.fill('input[name="birth_date_solar"]', '1990-05-15')
```

### Alpine.js x-show 切換後的操作
```python
# 切換到農曆模式後，等待 networkidle 確保 Alpine.js 完成渲染
page.click('label[for="lunar"]')  # 或對應的切換按鈕
page.wait_for_load_state("networkidle")
# 然後再操作農曆欄位
page.select_option('select[name="birth_lunar_year"]', "1985")
```

### Alpine.js 動態 `:data-*` 屬性的定位
```python
# Blade 模板中的寫法：:data-profile-name="profile.name"
# Playwright 在 networkidle 後可正確讀取（Alpine.js 已初始化）
page.wait_for_load_state("networkidle")

# 用 data-* 屬性定位列表特定行
row = page.locator('[data-profile-name="王小明"]').first
row.locator('a[title="編輯"]').click()

# 用 title 屬性定位操作按鈕
row.locator('button[title="刪除"]').click()

# 若同一實體有多筆（如同名人物），用 .first 取第一筆
row = page.locator('[data-profile-name="王小明"]').first
```

---

## 7. 注意事項

- **先讀 `e2e-scenarios.md`**：每個 test function 必須對應一個劇本
- **先讀 `webapp-testing` skill**：DOM 偵測、截圖、selector 選取方式參考該 skill
- **測試前確認 server 未運行**：避免 port 衝突（`with_server.py` 會自動管理）
- **Alpine.js 互動**：需要 `page.wait_for_load_state('networkidle')` 後再操作
- **`.env.testing` 必須正確設定**：`SESSION_DRIVER=file`、`APP_URL` 含 port（見 2a 節）
- **資料用 Seeder 建立，不用 tinker**：tinker 的 `bcrypt()` 與 `Hash::make()` 行為不同，且欄位容易猜錯
