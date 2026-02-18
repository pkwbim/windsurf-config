---
description: 階段 3 - Backend TDD 實作（Laravel Controller 邏輯 + Feature Test）
---

## 🎯 目的
依據 Form Contract 階段產出的 FormRequest + Controller 骨架，使用 TDD 方式實作真實 Backend 邏輯。

適用於 **Laravel 12 + Blade + Alpine.js（MPA）** 技術棧。

## ⚠️ 重要原則
- **TDD 流程**：Red（先寫測試）→ Green（實作邏輯）→ Refactor
- **測試類型視複雜度決定**：
  - 簡單 CRUD → 只寫 Feature Test（測試 HTTP 層行為）
  - 複雜業務邏輯（如計算邏輯）→ Feature Test + Unit Test
- **測試 DB**：使用專用 PostgreSQL 測試資料庫 + `RefreshDatabase` trait
- **Migration 時機**：測試 DB 由 `RefreshDatabase` 自動管理；正式 DB 在驗收通過後才 migrate
- **人類確認後才進下一步**

---

## 🧠 相關 Skills

| Skill | 觸發時機 | 步驟 |
|-------|---------|------|
| `pest-testing` | 撰寫 Feature Test、Unit Test | 步驟 3、4 |
| `laravel-ddd` | 功能複雜、需要 Service/Action/Repository 分層時 | 步驟 4 |

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
cat pm/planning/02_active.md
```
- 確認 Form Contract 階段已完成（checklist 已勾選）
- 確認已在 feature 分支（非 `main`）
- 確認 `.env.testing` 已設定（若無，先執行步驟 0.1）

### 0.1 設定測試環境（首次執行時）

若 `.env.testing` 不存在，建立並設定：

```bash
cp src/app/.env.testing.example src/app/.env.testing
```

然後填入測試 DB 連線資訊（`DB_DATABASE`、`DB_USERNAME`、`DB_PASSWORD`）。

**確認測試環境可連線：**
// turbo
```bash
cd src/app && php artisan migrate --env=testing
```

### 1. 讀取規格與 Contract 骨架
// turbo
```bash
cat pm/planning/stories/{active_story}/spec.md
ls src/app/app/Http/Requests/
ls src/app/app/Http/Controllers/
```

**必須理解以下內容後才能開始：**
- 每個 Controller method 的 TODO 行為規格
- 對應的 FormRequest 驗證規則
- 成功/失敗的 Redirect 行為
- 需要的 Middleware（`auth`、`guest`）

### 2. 分析實作範圍（必須引用規格）

在開始實作前，明確列出：

```markdown
## 本次 Backend 實作範圍

### Controller 實作清單
| Controller@method | 行為 | 測試類型 |
|-------------------|------|---------|
| LoginController@store | Auth::attempt → redirect/back | Feature Test |
| RegisterController@store | User::create → Auth::login → redirect | Feature Test |
| LogoutController@destroy | Auth::logout → session invalidate → redirect | Feature Test |
| ProfileController@update | $user->update → back()->with('success') | Feature Test |
| ProfileController@updatePassword | Hash::check + update → back()->with('success') | Feature Test |

### 複雜邏輯（需要 Unit Test）
| 類別 | 邏輯 | 測試類型 |
|------|------|---------|
| （無，UserAuth 全部是簡單 CRUD） | — | — |
```

### 3. 建立 Feature Test（TDD - Red）

> 🧠 **啟用 `pest-testing` skill** 撰寫測試。

**目錄結構：**
```
tests/Feature/
├── Auth/
│   ├── LoginTest.php
│   ├── RegisterTest.php
│   └── LogoutTest.php
└── Profile/
    └── ProfileTest.php
```

**Feature Test 範例（LoginTest）：**
```php
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

it('can view login page as guest', function () {
    $this->get('/login')->assertSuccessful();
});

it('redirects authenticated user away from login page', function () {
    $user = User::factory()->create();
    $this->actingAs($user)->get('/login')->assertRedirect('/dashboard');
});

it('validates login form - empty fields', function () {
    $this->post('/login', [])->assertSessionHasErrors(['email', 'password']);
});

it('validates login form - invalid email format', function () {
    $this->post('/login', ['email' => 'not-an-email', 'password' => 'password'])
        ->assertSessionHasErrors(['email']);
});

it('fails login with wrong password', function () {
    $user = User::factory()->create();
    $this->post('/login', ['email' => $user->email, 'password' => 'wrong-password'])
        ->assertSessionHasErrors(['email']);
});

it('can login with valid credentials', function () {
    $user = User::factory()->create();
    $this->post('/login', ['email' => $user->email, 'password' => 'password'])
        ->assertRedirect('/dashboard');
    $this->assertAuthenticated();
});
```

**RegisterTest 範例：**
```php
uses(RefreshDatabase::class);

it('can view register page as guest', function () {
    $this->get('/register')->assertSuccessful();
});

it('validates register form - email already taken', function () {
    $user = User::factory()->create();
    $this->post('/register', [
        'name'                  => '新用戶',
        'email'                 => $user->email,
        'password'              => 'password123',
        'password_confirmation' => 'password123',
    ])->assertSessionHasErrors(['email']);
});

it('can register with valid data', function () {
    $this->post('/register', [
        'name'                  => '新用戶',
        'email'                 => 'new@example.com',
        'password'              => 'password123',
        'password_confirmation' => 'password123',
    ])->assertRedirect('/dashboard');
    $this->assertAuthenticated();
    $this->assertDatabaseHas('users', ['email' => 'new@example.com']);
});
```

**驗證測試失敗（Red）：**
// turbo
```bash
cd src/app && php artisan test tests/Feature/Auth/ --env=testing
```
測試必須先失敗（因為 Controller 還是空的 TODO）。

### 4. 實作 Controller 邏輯（TDD - Green）

> 🧠 **若功能複雜，啟用 `laravel-ddd` skill** 決定是否需要 Service/Action 層。

將 Controller 骨架中的 TODO 替換為真實邏輯：

**LoginController@store 實作：**
```php
public function store(LoginRequest $request): RedirectResponse
{
    if (!Auth::attempt($request->only('email', 'password'), $request->boolean('remember'))) {
        return back()
            ->withErrors(['email' => '帳號或密碼錯誤'])
            ->withInput($request->only('email', 'remember'));
    }

    $request->session()->regenerate();

    return redirect()->intended(route('dashboard'));
}
```

**RegisterController@store 實作：**
```php
public function store(RegisterRequest $request): RedirectResponse
{
    $user = User::create([
        'name'     => $request->name,
        'email'    => $request->email,
        'password' => Hash::make($request->password),
    ]);

    Auth::login($user);

    return redirect()->route('dashboard');
}
```

**LogoutController@destroy 實作：**
```php
public function destroy(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();
    $request->session()->regenerateToken();

    return redirect()->route('home');
}
```

**ProfileController@update 實作：**
```php
public function update(UpdateProfileRequest $request): RedirectResponse
{
    $request->user()->update([
        'name'  => $request->name,
        'email' => $request->email,
    ]);

    return back()->with('success', '個人資料已更新');
}
```

**ProfileController@updatePassword 實作：**
```php
public function updatePassword(UpdatePasswordRequest $request): RedirectResponse
{
    $request->user()->update([
        'password' => Hash::make($request->password),
    ]);

    return back()->with('success', '密碼已更新');
}
```

**驗證測試通過（Green）：**
// turbo
```bash
cd src/app && php artisan test tests/Feature/ --env=testing
```
所有測試必須通過。

### 5. 重構（Refactor）

- 確認 Controller 沒有業務邏輯（只有協調）
- 若有重複程式碼，提取到 private method 或 Service
- 確認測試仍然通過

### 6. 確認 Blade 模板顯示錯誤訊息

確認 Blade 模板正確顯示 FormRequest 驗證錯誤和 session 訊息：

**錯誤訊息顯示（在 Blade 中）：**
```blade
@if ($errors->any())
    <div class="...">
        @foreach ($errors->all() as $error)
            <p>{{ $error }}</p>
        @endforeach
    </div>
@endif
```

**成功訊息顯示：**
```blade
@if (session('success'))
    <div class="...">{{ session('success') }}</div>
@endif
```

### 7. 執行完整測試套件
// turbo
```bash
cd src/app && php artisan test --env=testing
```
確認所有測試通過，無任何失敗。

### 8. 更新 checklist.md
// turbo
更新 story 目錄下的 `checklist.md`：

```markdown
- [x] **階段 3: Backend TDD 實作** (`/build-laravel`)
  - [x] Feature 測試（所有路由）
  - [x] 功能實作完成（Controller 邏輯）
  - [ ] **資料庫 Migration**（正式 DB）⬅️ 驗收後執行
  - [ ] 人工驗證通過
```

### 9. 通知使用者驗證

告訴使用者：

```
✅ Backend TDD 實作完成！

## 測試結果
所有 Feature Test 通過：
- Auth/LoginTest：X 個測試通過
- Auth/RegisterTest：X 個測試通過
- Auth/LogoutTest：X 個測試通過
- Profile/ProfileTest：X 個測試通過

## 請驗證
執行 `make start` 後，測試以下完整流程：
- [ ] 訪客首頁 → 點「登入」→ 輸入帳密 → 進入 Dashboard
- [ ] 訪客首頁 → 點「註冊」→ 填表 → 進入 Dashboard
- [ ] Dashboard → 點「登出」→ 回到首頁
- [ ] Profile 頁 → 更新姓名/Email → 看到成功訊息
- [ ] Profile 頁 → 修改密碼 → 看到成功訊息
- [ ] 未登入直接訪問 /dashboard → 導向 /login

驗證完成後，請告訴我「Backend 確認」。
```

**停止並等待使用者確認。**

### 10. 執行正式 DB Migration（驗收通過後）

收到確認後：

```bash
cd src/app && php artisan migrate
```

更新 checklist：
```markdown
- [x] **資料庫 Migration**（正式 DB）✅
- [x] 人工驗證通過 ✅
```

### 11. Commit 並提示下一步

```bash
git add src/app/app/Http/Controllers/ src/app/tests/ && git commit -m "feat: 完成 {story-id} Backend TDD 實作"
```

告知使用者：
```
✅ Backend 階段完成！

下一步：執行 `/merge` 合併到 main，或 `/review` 更新文件。
```

---

## 適用場景
- Laravel + Blade + Alpine.js 專案，Form Contract 完成後
- 需要 TDD 確保 Controller 邏輯正確
- 需要 Feature Test 覆蓋所有路由行為

## 不適用場景
- 純 API 專案（FastAPI/Node.js）→ 請使用 `/build-backend`
- 尚未完成 Form Contract → 先執行 `/build-laravel-contract`
