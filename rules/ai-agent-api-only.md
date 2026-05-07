# AI Agent 開發規則：僅透過 API 溝通

## 規則目的

確保 AI Coding Agent 在開發時，**永遠透過 HTTP API 端點呼叫後端，而非直接引用或呼叫內部 Service/Repository**。

這是為了維持架構邊界，確保：
1. **人類員工** 透過 Blade UI → 呼叫 API → 執行業務邏輯
2. **AI Agent** 直接透過 HTTP API → 執行業務邏輯
3. **兩者使用完全相同的 API 介面**

---

## 禁止行為 ❌

### 1. 禁止在 Controller 中直接呼叫 Repository
```php
// ❌ 錯誤：Controller 直接呼叫 Repository
class UserController extends Controller
{
    public function store(Request $request)
    {
        $user = User::create($request->all()); // 直接操作 Model/Repository
        return response()->json($user);
    }
}
```

### 2. 禁止在 API 測試中直接引用 Service 類別
```php
// ❌ 錯誤：測試直接引用內部 Service
$userService = app(UserService::class);
$result = $userService->create($data); // 直接呼叫 Service
```

### 3. 禁止在 Blade 頁面中直接操作資料庫
```php
// ❌ 錯誤：Blade 中使用 DB 查詢
@php
$users = DB::table('users')->get(); // 直接 SQL 查詢
@endphp
```

---

## 正確做法 ✅

### 1. Controller 只負責 HTTP 層，呼叫 Application Use Case
```php
// ✅ 正確：Controller 呼叫 Use Case
class UserController extends Controller
{
    public function __construct(
        private CreateUserUseCase $createUserUseCase
    ) {}

    public function store(CreateUserRequest $request): JsonResponse
    {
        $result = $this->createUserUseCase->execute($request->validated());
        return response()->json($result, 201);
    }
}
```

### 2. API 測試透過 HTTP Client 呼叫端點
```php
// ✅ 正確：測試使用 HTTP 請求
$response = $this->postJson('/api/v1/users', $data);
$response->assertStatus(201)
         ->assertJsonStructure(['id', 'name', 'account']);

// 驗證資料庫狀態（非直接操作）
$this->assertDatabaseHas('users', ['account' => 'testuser']);
```

### 3. Blade 頁面透過傳入的資料渲染
```php
// ✅ 正確：Controller 提供資料給 Blade
class UserController extends Controller
{
    public function index(): View
    {
        $users = $this->getUsersUseCase->execute();
        return view('users.index', compact('users'));
    }
}
```

---

## 架構邊界圖解

```
┌─────────────────────────────────────────────────────────┐
│  人類員工 (瀏覽器)                                        │
│  ┌──────────────┐                                       │
│  │ Blade UI     │                                       │
│  │ 表單、按鈕   │                                       │
│  └──────┬───────┘                                       │
└─────────┼───────────────────────────────────────────────┘
          │ HTTP Request
          ▼
┌─────────────────────────────────────────────────────────┐
│  Laravel Application                                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Routes (web.php / api.php)                      │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                     │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │  Controllers                                     │   │
│  │  - AuthController                                  │   │
│  │  - UserController                                  │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │ 呼叫 Use Case                        │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │  Application Layer (Use Cases)                   │   │
│  │  - LoginUseCase                                    │   │
│  │  - CreateUserUseCase                               │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                     │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │  Domain Layer (Entities, Value Objects)           │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                     │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │  Infrastructure (Repository)                     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
          ▲
          │ HTTP Request
┌─────────┼───────────────────────────────────────────────┐
│  AI Agent (外部程式)                                    │
│  ┌──────┴───────┐                                       │
│  │ HTTP Client  │  ← 直接呼叫 /api/v1/* 端點          │
│  │ (Bearer Token)│                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

**關鍵原則**：
- AI Agent **不進入** Laravel Application 內部
- AI Agent 與 Blade UI **共用相同的 API 端點**
- Controller 是**唯一**的邊界層

---

## 驗證方式

### 1. 程式碼審查檢查清單
- [ ] Controller 是否只依賴 Use Case 介面？
- [ ] 是否有任何檔案直接使用 `DB::` 或 Eloquent Model 靜態方法？
- [ ] 測試檔案是否使用 `postJson()` / `getJson()` 而非直接呼叫 Service？

### 2. 執行時驗證
```bash
# 檢查是否有直接 Model 操作
grep -r "User::create\|User::where" src/app/app/Http/Controllers --include="*.php"

# 應該回傳空結果（或只在 Use Case 中使用）
```

---

## 例外情況

以下情況允許直接存取：
1. **Seeders** - 資料填充時
2. **Artisan Commands** - 後台指令
3. **Queue Jobs** - 非同步任務
4. **Tests 的工廠模式** - 建立測試資料

---

## 違規處理

若發現 AI Agent 違反此規則：
1. 標記該程式碼為 `// FIXME: 違反 ai-agent-api-only 規則`
2. 重構為正確的 Use Case + Controller 架構
3. 更新相關測試為 HTTP 層測試
