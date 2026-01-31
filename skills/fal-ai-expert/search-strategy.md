# fal.ai 搜尋策略進階指南

## 為什麼需要搜尋策略？

在第一次查詢 Z-Image 時，使用了不夠精確的方法導致沒有找到結果。這個文件記錄了經驗教訓和最佳實踐。

## 失敗案例分析

### ❌ 第一次嘗試（失敗）
```
使用工具: mcp0_SearchFal
查詢: "z-image versions supported"
結果: 沒有找到 Z-Image 相關資訊
```

**問題：**
1. 直接使用 MCP 工具，而不是先讀取 llms.txt
2. 查詢關鍵字太籠統
3. 沒有使用網路搜尋作為補充

### ✅ 第二次嘗試（成功）
```
1. 使用工具: search_web
   查詢: "fal.ai z-image model versions"
   domain: "fal.ai"
   
2. 使用工具: read_url_content
   URL: https://fal.ai/models/fal-ai/z-image/turbo/api
   
結果: 成功找到所有 Z-Image 版本和詳細資訊
```

**成功因素：**
1. 使用網路搜尋定位模型
2. 直接讀取模型頁面
3. 獲得完整且準確的資訊

## 標準搜尋流程（SOP）

### Level 1: llms.txt（必須先執行）

```javascript
// 步驟 1: 讀取 llms.txt
read_url_content("https://fal.ai/llms.txt")

// 步驟 2: 在返回的內容中搜尋關鍵字
// 例如：在 "Featured Model Categories" 中找到 Z-Image
```

**優點：**
- 最權威的資訊來源
- 包含完整的模型列表
- 提供直接的文件連結
- 保證是最新資訊

**何時使用：**
- 所有查詢都應該從這裡開始
- 特別是查詢模型列表、版本、分類時

### Level 2: 網路搜尋（高效定位）

```javascript
search_web({
  query: "fal.ai [model-name] [specific-feature]",
  domain: "fal.ai"
})
```

**範例查詢：**
- `"fal.ai z-image turbo versions"`
- `"fal.ai flux models comparison"`
- `"fal.ai video generation models"`

**優點：**
- 快速定位到具體頁面
- 可以找到 llms.txt 中沒有的細節
- 適合探索性查詢

**何時使用：**
- llms.txt 中資訊不夠詳細時
- 需要找到具體的模型頁面時
- 查詢使用範例和教學時

### Level 3: 直接讀取模型頁面

```javascript
// 從 llms.txt 或網路搜尋獲得模型路徑後
read_url_content("https://fal.ai/models/fal-ai/[model-path]")

// 或讀取 API 文件頁面
read_url_content("https://fal.ai/models/fal-ai/[model-path]/api")
```

**優點：**
- 獲得最完整的資訊
- 包含 API 範例、參數、定價
- 可以看到實際的使用方式

**何時使用：**
- 已知模型名稱，需要詳細資訊時
- 需要 API 使用範例時
- 需要確認定價和參數時

### Level 4: MCP 工具（細節查詢）

```javascript
mcp0_SearchFal({
  query: "specific parameter or feature",
  apiReferenceOnly: true  // 只查 API 文件
})
```

**優點：**
- 可以查詢特定參數
- 搜尋文件中的細節
- 適合已知模型，查詢特定功能時

**何時使用：**
- 已經找到模型，需要查詢特定參數時
- 需要搜尋文件中的特定內容時
- 作為補充工具，不是主要工具

## 查詢模式範例

### 模式 1: 探索性查詢（不知道具體模型名稱）

**問題：** "fal.ai 有哪些圖片生成模型？"

**流程：**
```
1. read_url_content("https://fal.ai/llms.txt")
2. 查看 "Featured Model Categories" > "High Quality Image Generation"
3. 查看 "Featured Model Categories" > "Fast Image Generation"
4. 列出所有相關模型
```

### 模式 2: 特定模型查詢（知道模型名稱）

**問題：** "Z-Image 有哪些版本？"

**流程：**
```
1. read_url_content("https://fal.ai/llms.txt")
   - 在內容中搜尋 "z-image"
   
2. 如果 llms.txt 中資訊不足：
   search_web({
     query: "fal.ai z-image versions",
     domain: "fal.ai"
   })
   
3. 讀取找到的模型頁面：
   read_url_content("https://fal.ai/models/fal-ai/z-image/turbo")
```

### 模式 3: API 使用查詢

**問題：** "如何使用 Z-Image Turbo API？"

**流程：**
```
1. 從 llms.txt 確認模型路徑: "fal-ai/z-image/turbo"

2. 讀取 API 文件頁面：
   read_url_content("https://fal.ai/models/fal-ai/z-image/turbo/api")
   
3. 查看 JavaScript/Python 範例
```

### 模式 4: 比較查詢

**問題：** "FLUX 和 Z-Image 哪個更快？"

**流程：**
```
1. read_url_content("https://fal.ai/llms.txt")
   - 找到兩個模型的分類
   
2. 分別讀取兩個模型頁面：
   - https://fal.ai/models/fal-ai/flux/dev
   - https://fal.ai/models/fal-ai/z-image/turbo
   
3. 比較：
   - 推理步數
   - 定價
   - 參數量
   - 使用者評價
```

### 模式 5: 定價查詢

**問題：** "Z-Image 的定價是多少？"

**流程：**
```
1. read_url_content("https://fal.ai/models/fal-ai/z-image/turbo")
   - 查看頁面中的 "Pricing" 區塊
   
2. 或訪問總定價頁面：
   read_url_content("https://fal.ai/docs/pricing")
```

## 關鍵字優化技巧

### ✅ 好的關鍵字
- 具體的模型名稱：`"z-image turbo"`
- 包含平台名稱：`"fal.ai z-image"`
- 明確的功能：`"z-image image-to-image"`
- 具體的問題：`"z-image pricing"`

### ❌ 不好的關鍵字
- 太籠統：`"image generation"`
- 缺少平台：`"z-image versions"`（應該加上 fal.ai）
- 模糊的描述：`"fast model"`

## 工具選擇決策樹

```
開始查詢
    ↓
是否知道具體模型名稱？
    ├─ 否 → 讀取 llms.txt → 瀏覽分類
    └─ 是 ↓
         需要什麼資訊？
         ├─ 基本資訊（版本、分類）→ llms.txt
         ├─ API 使用方式 → 模型頁面 /api
         ├─ 定價 → 模型頁面
         ├─ 特定參數 → MCP 工具
         └─ 比較多個模型 → 網路搜尋 + 多個頁面
```

## 常見錯誤與解決方案

### 錯誤 1: 直接使用 MCP 工具
**問題：** MCP 工具可能無法返回完整的模型列表

**解決：** 總是先讀取 llms.txt

### 錯誤 2: 關鍵字太籠統
**問題：** 搜尋結果太多或不相關

**解決：** 使用具體的模型名稱和功能描述

### 錯誤 3: 忽略 llms.txt
**問題：** 浪費時間在多次搜尋上

**解決：** llms.txt 是最權威的起點

### 錯誤 4: 只依賴單一工具
**問題：** 可能遺漏重要資訊

**解決：** 結合多種工具驗證資訊

## 效率提升技巧

### 1. 建立模型路徑快取
在查詢過的模型中記錄完整路徑：
```
FLUX.1 [dev] → fal-ai/flux/dev
Z-Image Turbo → fal-ai/z-image/turbo
```

### 2. 使用並行查詢
當需要比較多個模型時，同時讀取多個頁面

### 3. 記住常用 URL 模式
```
模型頁面: https://fal.ai/models/fal-ai/{model-path}
API 文件: https://fal.ai/models/fal-ai/{model-path}/api
Playground: https://fal.ai/models/fal-ai/{model-path}/playground
```

### 4. 優先使用官方文件
- llms.txt 是第一選擇
- 模型頁面是第二選擇
- MCP 工具是補充工具

## 檢查清單

查詢前確認：
- [ ] 是否已讀取 llms.txt？
- [ ] 關鍵字是否足夠具體？
- [ ] 是否包含平台名稱（fal.ai）？
- [ ] 是否知道要查詢的具體資訊類型？

查詢後驗證：
- [ ] 資訊是否來自官方來源？
- [ ] 是否有多個來源確認？
- [ ] 版本號是否最新？
- [ ] 是否提供了具體的 URL 連結？

## 總結

**黃金法則：**
1. **總是從 llms.txt 開始**
2. **使用具體的關鍵字**
3. **結合多種工具驗證**
4. **提供完整的 URL 連結**

**時間分配建議：**
- 70% - 讀取官方文件（llms.txt + 模型頁面）
- 20% - 網路搜尋定位
- 10% - MCP 工具查詢細節

遵循這些策略，可以大幅提升查詢效率和準確度。
