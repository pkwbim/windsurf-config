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
| `ui-ux-pro-max` | 需要 UI/UX 設計指引、色彩配置、字型搭配 | 步驟 4 |
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

> 🧠 **此步驟啟用以下 Skills**：
> - `tailwindcss-development`：Tailwind CSS v4 樣式、響應式、dark mode
> - `frontend-design`：頁面視覺設計方向、UI 美化
> - `ui-ux-pro-max`：色彩配置、字型搭配、UX 指引

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

**UI 開發階段假資料**：直接寫死在 Blade 模板中，或在 Controller 回傳假陣列：
```php
// routes/web.php - UI 開發階段
Route::get('/dashboard', function () {
    return view('dashboard');  // 假資料直接寫在 Blade 中
})->name('dashboard');
```

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
  - [ ] 人工驗證 UI  ⬅️ 等待確認
```

### 8. 通知使用者驗證

> 🧠 **可選 Skill**：`webapp-testing`（Playwright）— 若需要自動截圖或驗證 UI 行為，可使用此 skill。

告訴使用者：

```
✅ UI 開發完成！

## 請驗證以下頁面

| 頁面 | URL | 驗證重點 |
|------|-----|---------|
| [頁面名稱] | [URL] | [需確認的 UI 細節] |

## 開發伺服器
執行 `make start` 後瀏覽上方 URL

## SEO 確認
在瀏覽器「檢視原始碼」，確認 HTML 包含完整文字內容（非空 div）

驗證完成後，請告訴我「UI 確認」或說明需要修改的地方。
```

**停止並等待使用者確認。**

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
