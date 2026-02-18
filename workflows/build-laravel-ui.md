---
description: 階段 1 - 純 UI 開發（Laravel + Inertia.js + Vue 3，使用假資料）
---

## 🎯 目的
開發 Vue 3 前端頁面與元件，使用寫死的假資料，讓人類先確認 UI 設計和互動流程。
適用於 **Laravel 12 + Inertia.js + Vue 3** 技術棧。

## ⚠️ 重要原則
- **新功能不接真實後端**：新開發的頁面使用假資料，但**現有功能保持不變**
- **專注 UI/UX**：確保介面設計和使用者體驗正確
- **人類確認後才進下一步**：完成後必須等待人類確認

---

## 🧠 相關 Skills

執行此 workflow 時，以下 skills 會自動或手動被觸發，請確保遵循其規範：

| Skill | 觸發時機 | 步驟 |
|-------|---------|------|
| `inertia-vue-development` | 建立 Vue 頁面元件、使用 `<Link>`、`useForm`、Inertia props | 步驟 4 |
| `tailwindcss-development` | 加入 Tailwind CSS 樣式、響應式設計、dark mode | 步驟 4 |
| `frontend-design` | 設計頁面視覺風格、UI 元件美化 | 步驟 4 |
| `ui-ux-pro-max` | 需要 UI/UX 設計指引、色彩配置、字型搭配 | 步驟 4 |
| `webapp-testing` | 使用 Playwright 驗證 UI 功能（可選） | 步驟 8 |

> **注意**：`fluxui-development` 是 Livewire 專用，不適用於 Inertia + Vue 3。

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
- Frontend 章節中的頁面清單與 Vue 元件路徑
- 每個頁面對應的 UC（Use Case）
- 版型（Layout）需求

### 2. 分析 UI 需求（必須引用規格）

在開始實作前，明確列出：

```markdown
## 本次 UI 開發範圍（引用 spec.md）

### 頁面清單
| 頁面 | URL | Vue 元件路徑 | 對應 UC |
|------|-----|-------------|---------|
| [從 spec.md 複製] | ... | ... | ... |

### 版型（Layout）
- [從 spec.md 複製版型需求]

### 元件清單
- [從 spec.md 複製元件清單]
```

**若規格不清楚，觸發 `/discussion` workflow，不要自行假設。**

### 3. 建立假資料檔案

假資料集中放在 `resources/js/mocks/{story-id}/` 目錄。

**目錄結構：**
```
resources/js/
├── mocks/
│   └── {story-id}/          # 例如：story-001a-user-auth/
│       ├── auth.mock.ts      # 登入/註冊相關假資料
│       └── profile.mock.ts   # 個人資料相關假資料
```

**假資料檔案格式：**
```typescript
// resources/js/mocks/story-001a-user-auth/auth.mock.ts

/** 已登入使用者資料 */
export interface AuthUser {
  /** 使用者 ID */
  id: number
  /** 顯示名稱 */
  name: string
  /** Email */
  email: string
}

/** 假資料 */
export const mockAuthUser: AuthUser = {
  id: 1,
  name: '測試用戶',
  email: 'test@example.com',
}

/**
 * UI 互動說明：
 * - 登入成功後顯示此使用者資料
 *
 * 預期 Inertia Props（供 /build-laravel-contract 參考）：
 * - auth.user: AuthUser | null
 */
```

### 4. 建立 Vue 元件與頁面

> 🧠 **此步驟啟用以下 Skills**：
> - `inertia-vue-development`：Vue 頁面結構、`<Link>`、`useForm`、Inertia props 寫法
> - `tailwindcss-development`：Tailwind CSS v4 樣式、響應式、dark mode
> - `frontend-design`：頁面視覺設計方向、UI 美化
> - `ui-ux-pro-max`：色彩配置、字型搭配、UX 指引

**目錄結構（標準 Laravel Breeze）：**
```
resources/js/
├── Layouts/
│   ├── GuestLayout.vue      # 訪客版型
│   └── AuthLayout.vue       # 會員版型
├── Pages/
│   ├── Home.vue
│   ├── About.vue
│   ├── Dashboard.vue
│   ├── Auth/
│   │   ├── Login.vue
│   │   └── Register.vue
│   └── Profile/
│       └── Edit.vue
└── Components/
    └── [共用元件]
```

**Vue 元件開發原則：**
- 使用 `<script setup lang="ts">` 語法
- 使用 `defineProps<{...}>()` 定義 props 型別
- 假資料從 `mocks/` import，不寫在元件內
- 使用 Inertia 的 `<Link>` 元件取代 `<a>` 標籤

**元件中使用假資料範例：**
```vue
<script setup lang="ts">
import { mockAuthUser } from '@/mocks/story-001a-user-auth/auth.mock'

// UI 開發階段使用假資料
const user = mockAuthUser
</script>
```

### 5. 設定 Laravel 路由（如需要）

若有新頁面，在 `routes/web.php` 新增對應路由：
```php
// UI 開發階段，Controller 直接回傳假資料
Route::get('/dashboard', function () {
    return Inertia::render('Dashboard', [
        'user' => [
            'id' => 1,
            'name' => '測試用戶',
            'email' => 'test@example.com',
        ],
    ]);
})->name('dashboard');
```

### 6. 啟動開發伺服器
// turbo
```bash
make start
```
確認前端頁面可正常瀏覽。

### 7. 更新 checklist.md
// turbo
更新 story 目錄下的 `checklist.md`，勾選已完成的 UI 項目：

```markdown
- [x] **階段 1: 純 UI 開發** (`/build-laravel-ui`) ✅
  - [x] GuestLayout / AuthLayout 版型
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

## 假資料位置
`resources/js/mocks/{story-id}/`（供後續 /build-laravel-contract 參考）

## 開發伺服器
執行 `make start` 後瀏覽上方 URL

驗證完成後，請告訴我「UI 確認」或說明需要修改的地方。
```

**停止並等待使用者確認。**

### 9. 處理使用者回饋

**若需修改：**
1. 根據回饋修改 Vue 元件
2. 修改完成後 commit
3. 再次通知使用者驗證（重複步驟 8）

**若確認通過：**
1. 更新 `checklist.md`，勾選「人工驗證 UI」
2. Commit 所有變更：
```bash
git add resources/js/ routes/ && git commit -m "feat(ui): 完成 {story-id} UI 開發"
```
3. 告知使用者下一步

### 10. 提示下一步

```
✅ UI 階段完成！

下一步：執行 `/build-laravel-contract` 定義 Inertia Props Contract
（此 workflow 尚未建立，完成後將引導你建立它）
```

---

## 適用場景
- Laravel + Inertia.js + Vue 3 專案的前端 UI 開發
- 需要先確認 UI 設計再實作 Backend

## 不適用場景
- 純 Backend/API 功能 → 請使用 `/build-laravel`
- React/TypeScript 專案 → 請使用 `/build-ui`
- 只需修改現有 UI → 可直接修改，不需完整流程
