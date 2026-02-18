---
description: Laravel + TDD + Feature Test workflow for building features
auto_execution_mode: 1
---

## Context Files
- `pm/planning/02_active.md` - Current task specification
- `.windsurf/AGENTS.md` - Agent configuration

## Implementation Steps

### 0. Git Branch Setup
// turbo
```bash
git branch --show-current
```
- 如果目前仍在 `main`：停止並提醒先執行 `/plan` 以建立 `feat/<story-id>` 分支
- 如果已在 feature 分支：繼續後續實作

### 1. Read & Validate Spec
// turbo
```bash
cat pm/planning/02_active.md
```
- 確認需求清楚後再開始寫測試
- 檢查規格文件是否包含：
  - 使用者故事與驗收標準
  - 技術規格（Migration、API、UI）
  - 測試策略

### 2. Create Test Cases (TDD - Red)

#### 2.1 Unit Tests (PHPUnit)

**位置**: `tests/Unit/`

建立測試檔案：
- Model 測試: `tests/Unit/Models/{ModelName}Test.php`
- Service 測試: `tests/Unit/Services/{ServiceName}Test.php`
- 其他類別: `tests/Unit/{Namespace}/{ClassName}Test.php`

**測試內容**：
- 類別初始化與依賴注入
- 方法輸入輸出驗證
- 邊界條件處理
- Mock 外部依賴（DB、API、檔案系統）

#### 2.2 Feature Tests (PHPUnit + HTTP)

**位置**: `tests/Feature/`

建立測試檔案：
- API 測試: `tests/Feature/Api/{Resource}Test.php`
- 頁面測試: `tests/Feature/Web/{Page}Test.php`
- Controller 測試: `tests/Feature/Http/Controllers/{Controller}Test.php`

**頁面測試項目**：
1. **網址正確性**
   - 路由是否存在（HTTP 200）
   - 路由參數正確解析
   - 錯誤路由回傳 404

2. **內容正確性**
   - 頁面標題正確
   - 關鍵元素存在（按鈕、表單、列表）
   - 資料正確渲染（從 DB 讀取的內容）
   - Blade 變數正確傳遞

3. **互動測試**（如適用）
   - 表單提交後導向正確
   - 按鈕點擊後行為正確
   - AJAX 請求回應正確

#### 2.3 Database Testing

**使用**: `RefreshDatabase` trait

測試項目：
- Migration 正確執行
- Model Factory 正確產生資料
- 關聯關係正確運作
- 唯一約束正確觸發

### 3. Verify Test Failure (Red)
// turbo
```bash
php artisan test --filter={TestClassName}
# 或執行特定測試
php artisan test tests/Unit/{TestFile}.php
```
- 測試必須先失敗（Red），證明測試有檢查到東西
- 若測試直接通過，檢查測試邏輯是否正確

### 4. Implement Logic

#### 4.1 Database Layer

**Migration**:
- 使用 `php artisan make:migration` 建立，採用 Laravel 預設命名格式
- 必須包含 `up()` 和 `down()`
- 使用 `Schema::table()` 修改現有表，`Schema::create()` 新建表

**Model**:
- 定義 `$fillable` 或 `$guarded`
- 定義關聯方法（`hasMany()`, `belongsTo()` 等）
- 定義 Scope 方法（查詢重用）
- 使用 Accessor/Mutator 處理資料轉換

#### 4.2 Service Layer

**原則**:
- 商業邏輯封裝在 Service 類別
- 單一職責：每個 Service 只負責一個領域
- 依賴注入：透過建構子注入 Repository 或其他 Service
- 錯誤處理：使用 try-catch，記錄 Log，拋出有意義的例外

#### 4.3 Controller Layer

**原則**:
- 保持輕量：Controller 只負責接收請求、呼叫 Service、回傳回應
- 使用 FormRequest 驗證輸入
- 使用 Resource 轉換輸出（API）
- 錯誤處理：使用 try-catch，回傳適當的 HTTP 狀態碼

#### 4.4 View Layer

**原則**:
- 使用 Blade 元件（`components/`）重用 UI
- 使用 Layout（`layouts/app.blade.php`）統一頁面結構
- 表單使用 `@csrf` 和 `@method()`
- 使用 Laravel Pint 檢查程式碼風格

### 5. Verify Test Success (TDD - Green)
// turbo
```bash
php artisan test
# 或執行特定測試
php artisan test --filter={TestClassName}
```
- 所有測試必須通過（Green）
- 若測試失敗，回到步驟 4 修正實作

### 6. Refactor & Clean

**檢查項目**:
- 程式碼重複：提取到 Service 或 Trait
- 命名清晰度：變數、方法、類別名稱是否表達意圖
- 效能優化：N+1 查詢、不必要的資料庫操作
- 錯誤處理：是否所有例外都有適當處理
- 程式碼風格：執行 `vendor/bin/pint` 檢查

**重構後驗證**:
// turbo
```bash
php artisan test
```
- 重構後所有測試仍必須通過

### 7. Update Task Status

完成單元測試後，更新 `pm/planning/02_active.md` 的狀態：

```markdown
# 🚀 Current Task: [Story Name] (Story-XXX)

**📊 開發狀態**: ✅ Build 完成 → 待整合測試

## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] 單元測試撰寫 (TDD Red)
- [x] 功能實作完成 (TDD Green)
- [x] 程式碼重構 (TDD Refactor)
- [ ] **整合測試通過** (`/integration`) ⬅️ 下一步
- [ ] 人工驗證通過
- [ ] 程式碼已提交 (`/commit`)
- [ ] 已合併到 main (`/merge`)

## 下一步行動
執行 `/integration` 進行整合測試
```

### 8. 🛑 人工驗證檢查點（MANDATORY）

**⚠️ 重要：此步驟不可跳過！**

完成整合測試後，**必須**停下來等待使用者進行人工驗證：

1. **提供驗證指南**：
   - 列出需要驗證的關鍵功能點
   - 提供具體的驗證步驟
   - 如有相關文件，提供連結

2. **明確告知使用者**：
   ```
   ⚠️ 請進行人工驗證
   
   已完成自動化測試，現在需要您進行人工驗證：
   
   📋 驗證項目：
   - [ ] [功能點 1]
   - [ ] [功能點 2]
   - [ ] [功能點 3]
   
   ✅ 驗證完成後，請回覆「驗證通過」或「好」以繼續下一步
   ❌ 如發現問題，請描述問題以便修正
   ```

3. **等待使用者回應**：
   - **不要自動執行 `/review`**
   - **不要假設驗證已通過**
   - 等待使用者明確回覆後才繼續

### 9. 提示下一步

告訴使用者：
- ✅ Build 階段完成
- 📝 已更新開發狀態
- 🔜 下一步：執行 `/integration` 進行整合測試
- ⚠️ 整合測試後需要人工驗證

## Notes

- 永遠遵循 TDD: Red → Green → Refactor
- 保持實作最小化且專注
- **文件更新在 `/review` 階段處理**

## Tech Stack Specifics

### Laravel + PHP

**測試工具**:
- PHPUnit: 單元和功能測試
- Laravel Test Helpers: `actingAs()`, `get()`, `post()` 等
- Database Testing: `RefreshDatabase`, `DatabaseMigrations` traits
- Mocking: Laravel Mockery, PHPUnit MockBuilder

**測試檔案位置**:
```
tests/
├── Feature/           # HTTP 功能測試、頁面測試
├── Unit/             # 單元測試（類別、方法）
└── CreatesApplication.php
```

**常用測試指令**:
```bash
php artisan test                    # 執行所有測試
php artisan test --filter={name}    # 執行特定測試
php artisan test --parallel         # 平行測試
vendor/bin/phpunit tests/Unit/       # 直接執行 PHPUnit
```

**頁面測試範例結構**:
```php
public function test_page_shows_correct_content()
{
    // Arrange
    $user = User::factory()->create();
    
    // Act
    $response = $this->actingAs($user)->get('/dashboard');
    
    // Assert
    $response->assertStatus(200);
    $response->assertSee('Dashboard');
    $response->assertViewHas('stats');
}
```

**程式碼風格**:
```bash
vendor/bin/pint                      # 檢查風格
vendor/bin/pint --fix                # 自動修復
```
