---
name: fal-ai-expert
description: Expert knowledge for querying fal.ai models, versions, API usage, and documentation. Use when searching for fal.ai model information, checking supported versions, or integrating fal.ai APIs.
---

# fal.ai Expert Skill

這個 skill 提供查詢 fal.ai 平台的最佳實踐和策略。

## 查詢 fal.ai 資訊的標準流程

### 1. 第一步：讀取 llms.txt（最重要）
```
URL: https://fal.ai/llms.txt
```

**為什麼優先使用 llms.txt？**
- 專為 LLM 設計的標準化格式
- 包含完整的模型分類和列表
- 提供所有 API 文件的直接連結
- 保證是最新的官方資訊

**使用方法：**
```javascript
// 使用 read_url_content 工具讀取
read_url_content("https://fal.ai/llms.txt")
```

### 2. 第二步：定位具體模型

從 llms.txt 中找到模型的完整路徑，例如：
- `fal-ai/z-image/turbo` - Z-Image Turbo 文字生成圖片
- `fal-ai/z-image/turbo/image-to-image` - Z-Image 圖片編輯
- `fal-ai/z-image/turbo/lora` - Z-Image with LoRA
- `fal-ai/z-image/turbo/controlnet` - Z-Image with ControlNet
- `fal-ai/flux/dev` - FLUX.1 [dev]
- `fal-ai/flux-pro/v1.1-ultra` - FLUX1.1 [pro] Ultra

### 3. 第三步：查看模型詳細頁面

訪問模型頁面獲取完整資訊：
```
https://fal.ai/models/{model-path}
```

例如：
- https://fal.ai/models/fal-ai/z-image/turbo
- https://fal.ai/models/fal-ai/flux/dev

**頁面包含：**
- API 使用範例
- 輸入/輸出參數
- 定價資訊
- Playground 測試介面

### 4. 第四步：使用 MCP 工具查詢細節

使用 `mcp0_SearchFal` 工具查詢特定細節：
```javascript
mcp0_SearchFal({
  query: "z-image turbo parameters",
  apiReferenceOnly: true  // 只返回 API 參考文件
})
```

### 5. 第五步：網路搜尋作為補充

如果以上方法都找不到，使用網路搜尋：
```javascript
search_web({
  query: "fal.ai z-image turbo versions",
  domain: "fal.ai"
})
```

## 常見查詢模式

### 查詢模型版本
1. 讀取 llms.txt
2. 在 "Featured Model Categories" 或 "Top Recommended Models" 中查找
3. 訪問模型頁面確認版本

### 查詢 API 使用方式
1. 從 llms.txt 獲取模型路徑
2. 訪問 `/models/{model-path}/api` 頁面
3. 查看 JavaScript/Python 範例

### 查詢定價
1. 訪問模型頁面
2. 查看 "Pricing" 區塊
3. 或訪問 https://fal.ai/docs/pricing

### 比較不同模型
1. 從 llms.txt 的分類中找到相關模型
2. 逐一訪問模型頁面比較
3. 參考 "Top Recommended Models" 的推薦

## 重要提醒

### ❌ 不要做的事
- 不要直接使用 MCP 工具作為第一選擇
- 不要猜測模型名稱或版本
- 不要使用過於籠統的搜尋關鍵字

### ✅ 應該做的事
- 總是先讀取 llms.txt
- 使用完整的模型路徑（如 `fal-ai/z-image/turbo`）
- 結合多種工具確認資訊準確性
- 提供具體的 URL 連結給使用者

## 快速參考

### 主要文件連結
- llms.txt: https://fal.ai/llms.txt
- 模型瀏覽: https://fal.ai/models
- API 文件: https://fal.ai/docs
- 快速開始: https://fal.ai/docs/getting-started

### SDK 安裝
```bash
# JavaScript
npm install --save @fal-ai/client

# Python
pip install fal-client
```

### 基本 API 使用
```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/model-name", {
  input: {
    prompt: "your prompt here"
  }
});
```

## 參考其他檔案

- [model-reference.md](./model-reference.md) - 完整模型列表
- [api-examples.md](./api-examples.md) - 常用 API 範例
- [search-strategy.md](./search-strategy.md) - 進階搜尋策略
