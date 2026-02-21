---
description: 階段 1 - 純 UI 開發（Laravel + Blade + Tailwind CSS v4 + Alpine.js，使用假資料）
---

## 🎯 目的
開發 Blade 前端頁面，使用寫死的假資料，讓人類先確認 UI 設計和互動流程。
適用於 **Laravel 12 + Blade + Tailwind CSS v4 + Alpine.js** 技術棧（MPA，SEO 友善）。

## ⚠️ 重要原則
- **伺服器端渲染**：使用 Blade 模板，非 SPA，Google 可以抓到完整 HTML
- **新功能不接真實後端**：新開發的頁面使用假資料（寫死在 Blade 或 Controller），但**現有功能保持不變**
- **Alpine.js 處理局部互動**：表單驗證、loading 狀態、modal、toggle 等
- **人類確認後才進下一步**：完成後必須等待人類確認

---

## 🧠 相關 Skills

執行此 workflow 時，以下 skills 會自動或手動被觸發，請確保遵循其規範：

| Skill | 觸發時機 | 步驟 |
|-------|---------|------|
| `tailwindcss-development` | 加入 Tailwind CSS 樣式、響應式設計、dark mode | 步驟 4 |
| `frontend-design` | 設計頁面視覺風格、UI 元件美化 | 步驟 4 |
| `ui-ux-pro-max` | 產生設計系統（色彩、字型、風格）、UI/UX 設計指引 | 步驟 2.5 & 4 |
| `webapp-testing` | 使用 Playwright 驗證 UI 功能（可選） | 步驟 8 |

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
cat pm/planning/02_active.md
```
- 確認已在 feature 分支（非 `main`）
- 確認 `pm/planning/02_active.md` 有 `active_story`
- 確認此 Story 需要前端 UI（若純 Backend 功能，請改用 `/build-laravel`）

### 1. 讀取規格文件
// turbo
讀取 active story 目錄下的規格文件：
```bash
cat pm/planning/stories/{active_story}/spec.md
cat pm/planning/stories/{active_story}/use-cases.md
```

**必須理解以下內容後才能開始實作：**
- Frontend 章節中的頁面清單與 Blade 模板路徑
- 每個頁面對應的 UC（Use Case）
- 版型（Layout）需求

### 2. 分析 UI 需求（必須引用規格）

在開始實作前，明確列出：

```markdown
## 本次 UI 開發範圍（引用 spec.md）

### 頁面清單
| 頁面 | URL | Blade 模板路徑 | 對應 UC |
|------|-----|--------------|---------|
| [從 spec.md 複製] | ... | ... | ... |

### 版型（Layout）
- [從 spec.md 複製版型需求]
```

**若規格不清楚，觸發 `/discussion` workflow，不要自行假設。**

### 2.5. 產生設計系統（ui-ux-pro-max）

> 🧠 **此步驟使用 `ui-ux-pro-max` skill**，在寫任何 UI 之前先確立設計方向，確保所有頁面風格一致。

執行設計系統產生指令：
```bash
python3 .windsurf/skills/ui-ux-pro-max/scripts/search.py "<產品類型> <產業> <風格關鍵字>" --design-system --persist -p "<專案名稱>"
```

**範例（紫微斗數排盤）：**
```bash
python3 .windsurf/skills/ui-ux-pro-max/scripts/search.py "astrology chart fortune-telling traditional chinese" --design-system --persist -p "HeavenlyCode"
```

指令執行後會產生：
- `design-system/MASTER.md` — 全域設計系統（色彩、字型、風格、UX 規範）
- `design-system/pages/` — 各頁面 override 目錄（可選）

**後續步驟 4 實作 Blade 頁面時，必須先讀取 `design-system/MASTER.md`，依其規範套用色彩、字型、元件風格。**

> ⚠️ 若 `design-system/MASTER.md` 已存在（前次執行過），跳過此步驟，直接讀取現有設計系統。

### 3. 建立 Blade 版型（Layouts）

版型放在 `resources/views/layouts/` 目錄：

```
resources/views/
├── layouts/
│   ├── guest.blade.php    # 訪客版型（含導覽列：首頁、關於、登入、註冊）
│   └── auth.blade.php     # 會員版型（含導覽列：Dashboard、個人資料、登出）
```

**版型結構範例：**
```blade
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title') - 網站名稱</title>
    <meta name="description" content="@yield('description', '預設描述')">
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <nav>...</nav>
    <main>@yield('content')</main>
    <footer>...</footer>
</body>
</html>
```

### 4. 建立 Blade 頁面

> 🧠 **此步驟「必須」啟用以下 Skills（不可略過）**：
> - **`frontend-design`**：**必須先讀取此 skill，確定視覺風格方向再開始實作**。避免平常的 AI 審美、使用獨特字體、大膽配色、令人难忘的版面設計
> - `tailwindcss-development`：Tailwind CSS v4 樣式、響應式、dark mode
> - `ui-ux-pro-max`：色彩配置、字型搦配、UX 指引

**目錄結構：**
```
resources/views/
├── layouts/
│   ├── guest.blade.php
│   └── auth.blade.php
├── home.blade.php
├── about.blade.php
├── dashboard.blade.php
├── auth/
│   ├── login.blade.php
│   └── register.blade.php
└── profile/
    └── edit.blade.php
```

**Blade 頁面結構：**
```blade
@extends('layouts.guest')

@section('title', '頁面標題')
@section('description', 'SEO 描述')

@section('content')
    {{-- 頁面內容，使用 Tailwind CSS 樣式 --}}
    <div class="max-w-6xl mx-auto px-4 py-20">
        <h1 class="text-4xl font-bold">標題</h1>
    </div>
@endsection
```

**Alpine.js 局部互動範例（表單 loading 狀態）：**
```blade
<form method="POST" action="..." x-data="{ loading: false }" @submit="loading = true">
    @csrf
    <button type="submit" :disabled="loading" class="...">
        <span x-show="!loading">送出</span>
        <span x-show="loading">處理中...</span>
    </button>
</form>
```

> ⚠️ **Alpine.js x-show 表單規範：**
> 當用 `x-show` 切換多個表單區塊時（如陰曆切換），**不能在不同區塊重複相同的 `name` 欄位**。
> 應改用單一隱藏欄位配合 Alpine.js 綁定：
> ```blade
> {{-- ✅ 正確：單一隱藏欄位，由 Alpine.js 控制其值 --}}
> <input type="hidden" name="date_type" :value="dateType">
>
> {{-- ❌ 錯誤：兩個 x-show 區塊各有一個 name="date_type"，送出時會重複 --}}
> <div x-show="dateType === 'solar'">
>     <input type="hidden" name="date_type" value="solar">  {{-- 錯誤 --}}
> </div>
> <div x-show="dateType === 'lunar'">
>     <input type="hidden" name="date_type" value="lunar">  {{-- 錯誤 --}}
> </div>
> ```

> ⚠️ **表單必須顯示 `@error` 訊息：**
> 所有 Blade 表單欄位必須在驗證失敗時顯示錯誤訊息，並用 `old()` 保留已填入的內容：
> ```blade
> <input type="text" name="name" value="{{ old('name') }}"
>        class="... @error('name') border-red-500 @enderror">
> @error('name')
>     <p class="text-xs text-red-400">{{ $message }}</p>
> @enderror
> ```

**UI 開發階段假資料**：直接寫死在 Blade 模板中，或在 Controller 回傳假陣列：
```php
// routes/web.php - UI 開發階段
Route::get('/dashboard', function () {
    return view('dashboard');  // 假資料直接寫在 Blade 中
})->name('dashboard');
```

> ⚠️ **假資料標記規範（必遵）：**
> 所有寫死的假資料必須加上標記註解，方便 Backend 階段清查：
> ```blade
> {{-- TODO: 換成真實資料 --}}
> <p>王小明</p>
> ```
> ```php
> // TODO: 換成真實資料
> $profiles = [['name' => '王小明', 'gender' => 'male']];
> ```

> ⚠️ **可測試 UI 規範（必遵）：**
> 依照 `page-{name}.md` 的「🧪 可測試性規範」區塊，為互動元素加上 `data-*` 屬性：
> ```blade
> {{-- 列表每行：加上 data-* 供 Playwright 定位 --}}
> <div class="grid grid-cols-12 ..."
>      :data-profile-name="profile.name">
>
> {{-- 操作按鈕：加上 title 供 Playwright 定位 --}}
> <a :href="`/profiles/${profile.id}/edit`" title="編輯">...圖標...</a>
> <button @click="openDeleteModal(...)" title="刪除">...圖標...</button>
> ```

### 5. 設定 Laravel 路由

在 `routes/web.php` 新增對應路由：
```php
use Illuminate\Support\Facades\Route;

Route::get('/', fn() => view('home'))->name('home');
Route::get('/about', fn() => view('about'))->name('about');
Route::get('/login', fn() => view('auth.login'))->name('login');
Route::get('/register', fn() => view('auth.register'))->name('register');
Route::get('/dashboard', fn() => view('dashboard'))->name('dashboard');
Route::get('/profile', fn() => view('profile.edit'))->name('profile.edit');

// UI 假資料：POST 路由直接 redirect
Route::post('/login', fn() => redirect()->route('dashboard'));
Route::post('/register', fn() => redirect()->route('dashboard'));
Route::post('/logout', fn() => redirect()->route('login'))->name('logout');
Route::patch('/profile', fn() => back()->with('success', '資料已更新'))->name('profile.update');
Route::put('/profile/password', fn() => back()->with('success', '密碼已更新'))->name('profile.password');
```

### 6. 啟動開發伺服器
// turbo
```bash
make start
```
確認頁面可正常瀏覽，HTML 原始碼包含完整內容（非空 div）。

### 7. 更新 checklist.md
// turbo
更新 story 目錄下的 `checklist.md`，勾選已完成的 UI 項目：

```markdown
- [x] **階段 1: 純 UI 開發** (`/build-laravel-ui`) ✅
  - [x] layouts/guest.blade.php / layouts/auth.blade.php 版型
  - [x] [已完成的頁面列表]
  - [x] Alpine.js 規範檢查：x-show 切換區塊中沒有重複的 name 欄位
  - [x] 所有表單欄位已加入 @error 訊息顯示與 old() 保留
  - [x] 可測試 UI 檢查：依照 page spec 的 🧪 區塊加上 data-* 屬性
  - [x] 假資料標記：所有寫死假資料已加上 `{{-- TODO: 換成真實資料 --}}` 註解
  - [ ] 人工驗證 UI  ⬅️ 等待確認

### 📝 假資料清單（Backend 階段必須逐一處理）
| 頁面 | Blade 模板路徑 | 假資料說明 |
|------|--------------|----------|
| [頁面名稱] | `resources/views/xxx.blade.php` | [哪些資料是假的] |
```

### 8. Playwright 自動截圖驗證 UI

> 🧠 **此步驟「必須」執行，不可略過**：使用 Playwright 自動截圖，確認 UI 正常再交件。

#### 8.1 執行方式（必須用 with_server.py，不可用獨立腳本）

參考 `/integration-e2e` workflow 的執行方式與 `src/tests/` 下的現有測試腳本：

```bash
# 讀取 APP_PORT
APP_PORT=$(grep '^APP_PORT=' src/app/.env.testing | cut -d'=' -f2)

# 用 with_server.py 啟動 testing server 並執行 pytest
python3 .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd src/app && php artisan serve --port=${APP_PORT} --env=testing" \
  --port ${APP_PORT} \
  -- .venv/bin/pytest scripts/temp/test_{story_id}_ui.py -v -s
```

> ⚠️ **不可直接 `python script.py` 執行**，必須透過 `with_server.py` 管理 server 生命週期。

#### 8.2 測試腳本結構（參考 `src/tests/AiChatTest.py`）

暫存腳本放在 `scripts/temp/test_{story_id}_ui.py`，結構如下：

```python
import pytest
from playwright.sync_api import Page, Browser, expect

APP_PORT = "8236"  # 從 .env.testing 讀取
BASE_URL = f"http://127.0.0.1:{APP_PORT}"
TEST_EMAIL = "test_e2e@example.com"
TEST_PASSWORD = "password"
GOTO_TIMEOUT = 30_000

@pytest.fixture(scope="module")
def ui_page(browser: Browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    # 登入
    page.goto(f"{BASE_URL}/login", timeout=GOTO_TIMEOUT)
    page.wait_for_load_state("networkidle")
    page.fill('input[name="email"]', TEST_EMAIL)
    page.fill('input[name="password"]', TEST_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    assert "/login" not in page.url
    yield page
    ctx.close()

class TestStoryUI:
    def test_01_page_loads(self, ui_page: Page):
        """頁面正常載入"""
        ui_page.goto(f"{BASE_URL}/your-url", timeout=GOTO_TIMEOUT)
        ui_page.wait_for_load_state("networkidle")
        ui_page.screenshot(path="/tmp/s{id}_01_page.png")
        # 驗證關鍵元素
        expect(ui_page.locator("[data-key-element]")).to_be_visible()
```

> ⚠️ **登入帳號**：`test_e2e@example.com` / `password`（來自 `src/tests/conftest.py`）  
> ⚠️ **取得 chart URL**：參考 `src/tests/AiChatTest.py` 的 `_get_chart_url()` 模式  
> ⚠️ **`scope="module"`**：UI 驗證腳本用 module scope，整個模組共用一個登入 session

#### 8.3 驗證重點

- 按鈕是否顯示在正確位置
- 樣式是否與頁面風格一致
- `data-*` 屬性是否存在（依 page spec 的 🧪 規範）
- 頁面是否正常載入（無 500 錯誤）
- Alpine.js 互動：`x-show` 切換、disabled 狀態等

#### 8.4 截圖確認

截圖存於 `/tmp/` 目錄，逐一檢查後告知使用者結果。**找到問題必須修正後再截圖確認，直到滿意才可進入下一步。**

**停止並等待使用者最終確認。**

### 9. 處理使用者回饋

**若需修改：**
1. 根據回饋修改 Blade 模板
2. 修改完成後 commit
3. 再次通知使用者驗證（重複步驟 8）

**若確認通過：**
1. 更新 `checklist.md`，勾選「人工驗證 UI」
2. Commit 所有變更：
```bash
git add resources/views/ resources/js/ routes/ && git commit -m "feat(ui): 完成 {story-id} UI 開發"
```
3. 告知使用者下一步

### 10. 提示下一步

```
✅ UI 階段完成！

下一步：執行 `/build-laravel`（後端 TDD 實作）
```

---

## 適用場景
- Laravel + Blade + Tailwind CSS v4 + Alpine.js 專案的前端 UI 開發
- 需要 SEO 友善的 MPA（多頁式）架構
- 需要先確認 UI 設計再實作 Backend

## 不適用場景
- 純 Backend/API 功能 → 請使用 `/build-laravel`
- SPA 架構（Inertia + Vue）→ 此專案不使用
- 只需修改現有 UI → 可直接修改，不需完整流程
