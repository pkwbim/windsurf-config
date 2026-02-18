---
description: 階段 2 - Laravel Form Contract 設計（定義 FormRequest + Controller 行為規格）
---

## 🎯 目的
在 UI 開發完成後，定義每個表單/功能的 **FormRequest 驗證規則**、**Controller 行為**、**Redirect 規則**，作為 Backend 實作（`/build-laravel`）的規格起點。

適用於 **Laravel 12 + Blade + Alpine.js（MPA）** 技術棧。

## ⚠️ 重要原則
- **規格先行**：先定義 FormRequest 骨架，再實作 Controller 邏輯
- **FormRequest 即規格**：FormRequest 的驗證規則就是可執行的介面契約
- **DDD 視複雜度決定**：
  - 簡單 CRUD → `Controller → FormRequest → Eloquent Model`（輕量版）
  - 複雜業務邏輯 → `Controller → FormRequest → Service/Action → Repository`（完整 DDD）
- **人類確認後才進下一步**

---

## 🧠 相關 Skills

| Skill | 觸發時機 | 步驟 |
|-------|---------|------|
| `laravel-ddd` | 功能複雜、需要 Service/Action/Repository 分層時 | 步驟 3 |
| `pest-testing` | 撰寫 FormRequest 測試、Feature Test 骨架 | 步驟 4 |

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
cat pm/planning/02_active.md
```
- 確認 UI 階段已完成（`/build-laravel-ui` checklist 已勾選）
- 確認已在 feature 分支（非 `main`）

### 1. 讀取規格文件
// turbo
```bash
cat pm/planning/stories/{active_story}/spec.md
cat pm/planning/stories/{active_story}/use-cases.md
```

**必須理解以下內容後才能開始：**
- 每個頁面的表單欄位與驗證需求
- 每個 UC 的成功/失敗流程
- Middleware 需求（`auth`、`guest`）

### 2. 分析 Contract 需求（必須引用規格）

在開始實作前，明確列出：

```markdown
## 本次 Contract 範圍（引用 spec.md）

### 表單清單
| 表單 | URL | Method | FormRequest 類別 | 成功 Redirect | 失敗行為 |
|------|-----|--------|-----------------|--------------|---------|
| 登入 | `/login` | POST | `LoginRequest` | `/dashboard` | back() with errors |
| 註冊 | `/register` | POST | `RegisterRequest` | `/dashboard` | back() with errors |
| 更新個人資料 | `/profile` | PATCH | `UpdateProfileRequest` | back() with success | back() with errors |
| 修改密碼 | `/profile/password` | PUT | `UpdatePasswordRequest` | back() with success | back() with errors |
| 登出 | `/logout` | POST | — | `/` | — |

### DDD 分層決定
| 功能 | 複雜度 | 採用架構 |
|------|--------|---------|
| 登入/登出 | 低 | 輕量版（Controller → Auth facade） |
| 註冊 | 低 | 輕量版（Controller → User::create） |
| 更新個人資料 | 低 | 輕量版（Controller → $user->update） |
| 修改密碼 | 低 | 輕量版（Controller → Hash::check + update） |
```

**若規格不清楚，觸發 `/discussion` workflow，不要自行假設。**

### 3. 建立 FormRequest 骨架

> 🧠 **若功能複雜，啟用 `laravel-ddd` skill** 決定是否需要 Service/Action 層。

**目錄結構：**
```
app/Http/Requests/
├── Auth/
│   ├── LoginRequest.php
│   └── RegisterRequest.php
└── Profile/
    ├── UpdateProfileRequest.php
    └── UpdatePasswordRequest.php
```

**FormRequest 骨架範例：**
```php
<?php

namespace App\Http\Requests\Auth;

use Illuminate\Foundation\Http\FormRequest;

class LoginRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'email'    => ['required', 'email'],
            'password' => ['required', 'string'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.required'    => '請輸入 Email',
            'email.email'       => 'Email 格式不正確',
            'password.required' => '請輸入密碼',
        ];
    }
}
```

**RegisterRequest 範例：**
```php
public function rules(): array
{
    return [
        'name'                  => ['required', 'string', 'max:255'],
        'email'                 => ['required', 'email', 'unique:users,email'],
        'password'              => ['required', 'string', 'min:8', 'confirmed'],
        'password_confirmation' => ['required'],
    ];
}
```

**UpdatePasswordRequest 範例：**
```php
public function rules(): array
{
    return [
        'current_password' => ['required', 'current_password'],
        'password'         => ['required', 'string', 'min:8', 'confirmed'],
    ];
}
```

### 4. 建立 Controller 骨架

> 🧠 **此步驟可啟用 `pest-testing` skill** 同步建立 Feature Test 骨架。

**目錄結構：**
```
app/Http/Controllers/
├── Auth/
│   ├── LoginController.php
│   ├── RegisterController.php
│   └── LogoutController.php
└── Profile/
    └── ProfileController.php
```

**Controller 骨架範例（行為規格）：**
```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Http\Requests\Auth\LoginRequest;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    public function create()
    {
        return view('auth.login');
    }

    public function store(LoginRequest $request)
    {
        // TODO: 實作登入邏輯
        // 1. Auth::attempt($request->only('email', 'password'), $request->boolean('remember'))
        // 2. 成功 → redirect()->intended('/dashboard')
        // 3. 失敗 → back()->withErrors(['email' => '帳號或密碼錯誤'])->withInput()
    }
}
```

**Controller 行為規格表：**

| Controller | Method | 行為 | 成功結果 | 失敗結果 |
|-----------|--------|------|---------|---------|
| `LoginController@create` | GET | 顯示登入頁 | `view('auth.login')` | — |
| `LoginController@store` | POST | 驗證 + 登入 | `redirect('/dashboard')` | `back()->withErrors()` |
| `RegisterController@create` | GET | 顯示註冊頁 | `view('auth.register')` | — |
| `RegisterController@store` | POST | 驗證 + 建立帳號 | `redirect('/dashboard')` | `back()->withErrors()` |
| `LogoutController@destroy` | POST | 登出 | `redirect('/')` | — |
| `ProfileController@edit` | GET | 顯示個人資料頁 | `view('profile.edit')` | — |
| `ProfileController@update` | PATCH | 更新個人資料 | `back()->with('success', ...)` | `back()->withErrors()` |
| `ProfileController@updatePassword` | PUT | 修改密碼 | `back()->with('success', ...)` | `back()->withErrors()` |

### 5. 更新路由（加入 Controller）

將 UI 階段的 closure 路由改為指向 Controller：

```php
use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\RegisterController;
use App\Http\Controllers\Auth\LogoutController;
use App\Http\Controllers\Profile\ProfileController;

// 訪客路由（已登入者不可存取）
Route::middleware('guest')->group(function () {
    Route::get('/login', [LoginController::class, 'create'])->name('login');
    Route::post('/login', [LoginController::class, 'store']);
    Route::get('/register', [RegisterController::class, 'create'])->name('register');
    Route::post('/register', [RegisterController::class, 'store']);
});

// 會員路由（未登入者不可存取）
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', fn() => view('dashboard'))->name('dashboard');
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::put('/profile/password', [ProfileController::class, 'updatePassword'])->name('profile.password');
});

Route::post('/logout', [LogoutController::class, 'destroy'])->name('logout')->middleware('auth');
```

### 6. 建立 Feature Test 骨架（可選）

> 🧠 **啟用 `pest-testing` skill** 撰寫測試。

```php
// tests/Feature/Auth/LoginTest.php
it('can view login page', function () {
    $this->get('/login')->assertSuccessful();
});

it('redirects authenticated user from login page', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->get('/login')->assertRedirect('/dashboard');
});

it('validates login form', function () {
    $this->post('/login', [])->assertSessionHasErrors(['email', 'password']);
});

it('can login with valid credentials', function () {
    $user = User::factory()->create();
    $this->post('/login', [
        'email'    => $user->email,
        'password' => 'password',
    ])->assertRedirect('/dashboard');
    $this->assertAuthenticated();
});
```

### 7. 更新 checklist.md
// turbo
更新 story 目錄下的 `checklist.md`：

```markdown
- [x] **階段 2: Form Contract 設計** (`/build-laravel-contract`) ✅
  - [x] FormRequest 骨架（驗證規則）
  - [x] Controller 骨架（行為規格）
  - [x] 路由更新（指向 Controller）
  - [ ] 人工驗證  ⬅️ 等待確認
```

### 8. 通知使用者驗證

告訴使用者：

```
✅ Form Contract 設計完成！

## 已建立的 FormRequest
| 類別 | 路徑 | 驗證規則數 |
|------|------|----------|
| LoginRequest | app/Http/Requests/Auth/ | 2 個欄位 |
| RegisterRequest | app/Http/Requests/Auth/ | 4 個欄位 |
| UpdateProfileRequest | app/Http/Requests/Profile/ | 2 個欄位 |
| UpdatePasswordRequest | app/Http/Requests/Profile/ | 3 個欄位 |

## 已建立的 Controller 骨架
- LoginController（create + store）
- RegisterController（create + store）
- LogoutController（destroy）
- ProfileController（edit + update + updatePassword）

## 請確認
- [ ] FormRequest 驗證規則是否符合需求？
- [ ] Controller 行為規格是否正確？
- [ ] 路由 Middleware 設定是否正確？

確認後，請告訴我「Contract 確認」。
```

**停止並等待使用者確認。**

### 9. 處理使用者回饋

**若需修改：**
1. 根據回饋修改 FormRequest 或 Controller 骨架
2. 修改完成後 commit
3. 再次通知使用者驗證

**若確認通過：**
1. 更新 `checklist.md`，勾選「人工驗證」
2. Commit 所有變更：
```bash
git add app/Http/Requests/ app/Http/Controllers/ routes/ && git commit -m "feat(contract): 完成 {story-id} Form Contract 設計"
```

### 10. 提示下一步

```
✅ Form Contract 階段完成！

下一步：執行 `/build-laravel`（後端 TDD 實作）
在 FormRequest 骨架基礎上，實作 Controller 邏輯和業務邏輯。
```

---

## 適用場景
- Laravel + Blade + Alpine.js 專案，UI 開發完成後
- 需要規格先行，定義驗證規則和 Controller 行為
- 需要為 Backend 實作建立清晰的起點

## 不適用場景
- 純 API 專案（FastAPI/Node.js）→ 請使用 `/build-contract`
- 沒有表單的純展示頁面 → 可直接進入 `/build-laravel`
- 已有完整 Controller 實作 → 不需要此步驟
