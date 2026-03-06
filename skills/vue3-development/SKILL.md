---
name: vue3-development
description: Vue 3 前端開發原則與慣例。當建立或修改 Vue 3 組件、頁面、composables、services 時自動啟用。適用於使用 Vue 3 + Vite + TailwindCSS + DaisyUI 技術棧的前端開發。觸發時機：建立 .vue 檔案、修改前端組件、撰寫前端測試、處理前端路由。
---

# Vue 3 開發原則

## 技術棧
- Vue 3 + Vite
- TailwindCSS + DaisyUI
- Vitest + Vue Test Utils
- Vue Router
- Pinia（狀態管理）

## 開發模式

使用 **Composition API + Composables 模式（函數式組合）**：
- `<script setup>` 語法
- `ref` 和 `reactive` 管理響應式資料
- `computed` 和 `watch` 處理衍生資料

## 核心原則

- **組合優於繼承**：使用 composables 組合功能
- **關注點分離**：UI 組件 vs 業務邏輯 vs 狀態管理
- **可重用性**：共用邏輯提取到 composables
- **單一職責**：每個 composable 只負責一個功能領域
- **每個檔案不超過 200 行**

## 分層架構

```
frontend/src/
├── components/        # UI 組件（純展示邏輯）
├── composables/       # 可重用的組合式函數（業務邏輯）
├── services/          # API 呼叫和外部服務
├── stores/            # Pinia 狀態管理
└── views/             # 頁面組件（組合多個組件）
```

## Composable 範例

```javascript
// composables/useFeature.js
export function useFeature() {
  const data = ref([])
  const loading = ref(false)

  async function fetchData() {
    loading.value = true
    try {
      // 業務邏輯
    } finally {
      loading.value = false
    }
  }

  return { data, loading, fetchData }
}
```

## 檔案超過 200 行時

- 拆分為子組件（`components/Feature/SubComponent.vue`）
- 提取 composables（`composables/useFeature.js`）
- 分離業務邏輯到 services（`services/featureService.js`）
- 拆分複雜狀態到 stores（`stores/featureStore.js`）

## 測試慣例

- 測試目錄：`frontend/tests/unit/` 或 `frontend/src/**/__tests__/`
- 命名：`*.spec.js` 或 `ComponentName.spec.js`
- 使用 Vitest + Vue Test Utils
- Mock API 呼叫使用 `vi.mock`
- **API Contract testing**：`ApiContract.spec.js` 確保前後端資料格式一致
- **Router Config testing**：`RouterConfig.spec.js` 確保路由正確配置
- **Router Links testing**：`RouterLinks.spec.js` 確保 router-link 引用有效路由

## 路由測試

新增 URL 路徑時必須同時：
1. 在 `router/index.js` 新增路由配置
2. 在 `RouterConfig.spec.js` 新增對應測試
3. 驗證：路由存在、參數正確解析、路由名稱正確
