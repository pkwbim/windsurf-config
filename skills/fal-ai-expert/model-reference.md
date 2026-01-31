# fal.ai 模型快速參考

> 本文件整理自 https://fal.ai/llms.txt
> 最後更新：2026-01-30

## 主要模型分類

### 🎨 高品質圖片生成
- **FLUX1.1 [pro] Ultra** (`fal-ai/flux-pro/v1.1-ultra`)
  - 超高品質，支援 2K 解析度
  - 專業級圖片生成
  
- **Imagen4 Ultra** - Google 的高品質圖片生成
- **Recraft V3** (`fal-ai/recraft-v3`) - SOTA 圖片生成模型

### ⚡ 快速圖片生成
- **FLUX.1 [dev]** (`fal-ai/flux/dev`)
  - 12B 參數，高品質
  - 適合個人和商業用途
  
- **FLUX.1 [schnell]** (`fal-ai/flux/schnell`)
  - 1-4 步快速生成
  - 優化速度
  
- **Z-Image Turbo** (`fal-ai/z-image/turbo`)
  - 6B 參數，超快推理
  - $0.005/megapixel
  - 支援 1-8 步推理
  
- **Sana Sprint** - 快速生成模型

### 🖼️ 圖片編輯
- **FLUX.1 Kontext [max]** (`fal-ai/flux-pro/kontext/max`)
  - 高級圖片編輯
  - 增強的提示詞遵循
  
- **SeedEdit 3.0** - 圖片編輯工具
- **OmniGen v2** - 多功能圖片生成

- **Z-Image Turbo 變體**：
  - `fal-ai/z-image/turbo/image-to-image` - 圖片轉圖片
  - `fal-ai/z-image/turbo/lora` - 支援 LoRA 自訂風格
  - `fal-ai/z-image/turbo/controlnet` - ControlNet 精確控制

### 🎬 影片生成
- **Veo 3** (`fal-ai/veo3`)
  - Google 最先進的 AI 影片生成
  - 支援聲音
  
- **Kling 2.1 Master** - 高品質影片生成
- **MiniMax Hailuo-02 Pro** - 專業級影片生成
- **MiniMax Video Image-to-Video** (`fal-ai/minimax-video/image-to-video`)

### 🎙️ 音訊處理
- **MiniMax Voice Clone** (`fal-ai/minimax/voice-clone`)
  - 只需幾秒音訊樣本即可複製聲音
  
- **Speech-to-Speech** - 語音轉換
- **Audio Isolation** - 音訊分離

### 👤 虛擬人物
- **AI Avatar MultiTalk** (`fal-ai/ai-avatar`)
  - 創建會說話的虛擬人物
  - 自動唇形同步

### 🗣️ 文字轉語音
- **MiniMax Speech-02 HD** (`fal-ai/minimax/speech-02-hd`)
  - 多語言 TTS
  - 語音合成

### 🤖 大型語言模型
- **Any LLM** (`fal-ai/any-llm`)
  - 支援 Claude, GPT-4o, Gemini, Llama
  - 統一 API 介面

### 🎓 訓練與微調
- **FLUX LoRA Fast Training** (`fal-ai/flux-lora-fast-training`)
  - 快速自訂風格訓練
  - 個人化模型

### 🔍 圖片增強
- **Clarity Upscaler** (`fal-ai/clarity-upscaler`)
  - 高保真圖片放大
  - 細節增強

## Z-Image 系列完整列表

### 主要端點
1. **Text-to-Image** (`fal-ai/z-image/turbo`)
   - 文字生成圖片
   - 6B 參數
   - 1-8 步推理
   - 最高 4MP 解析度
   - $0.005/MP

2. **Image-to-Image** (`fal-ai/z-image/turbo/image-to-image`)
   - 圖片編輯
   - 文字 + 圖片輸入
   - $0.005/MP

3. **LoRA** (`fal-ai/z-image/turbo/lora`)
   - 支援最多 3 個 LoRA 適配器
   - 每次生成 4 張圖片
   - 品牌一致性
   - $0.0085/MP

4. **ControlNet** (`fal-ai/z-image/turbo/controlnet`)
   - 邊緣圖、深度圖、姿態引導
   - 精確控制
   - 專業級結果

## FLUX 系列完整列表

### 主要版本
1. **FLUX.1 [schnell]** (`fal-ai/flux/schnell`)
   - 最快版本
   - 1-4 步生成
   - 12B 參數

2. **FLUX.1 [dev]** (`fal-ai/flux/dev`)
   - 平衡版本
   - 高品質
   - 12B 參數

3. **FLUX1.1 [pro] Ultra** (`fal-ai/flux-pro/v1.1-ultra`)
   - 最高品質
   - 2K 解析度
   - 專業級

4. **FLUX.1 Kontext [max]** (`fal-ai/flux-pro/kontext/max`)
   - 圖片編輯專用
   - 增強提示詞理解

## 快速查詢表

| 需求 | 推薦模型 | 端點 |
|------|---------|------|
| 最快生成 | Z-Image Turbo | `fal-ai/z-image/turbo` |
| 最高品質 | FLUX1.1 Pro Ultra | `fal-ai/flux-pro/v1.1-ultra` |
| 平衡速度品質 | FLUX.1 [dev] | `fal-ai/flux/dev` |
| 圖片編輯 | Z-Image Image-to-Image | `fal-ai/z-image/turbo/image-to-image` |
| 自訂風格 | Z-Image LoRA | `fal-ai/z-image/turbo/lora` |
| 精確控制 | Z-Image ControlNet | `fal-ai/z-image/turbo/controlnet` |
| 影片生成 | Veo 3 | `fal-ai/veo3` |
| 聲音複製 | MiniMax Voice Clone | `fal-ai/minimax/voice-clone` |
| LLM | Any LLM | `fal-ai/any-llm` |

## 定價參考

### 圖片生成
- Z-Image Turbo: $0.005/MP (text-to-image, image-to-image)
- Z-Image LoRA: $0.0085/MP
- FLUX 系列: 約 $0.0025/次 (fast-sdxl)

### 其他
- 詳細定價請訪問：https://fal.ai/docs/pricing
- 或查看各模型頁面的定價資訊

## 更新此文件

定期執行以下步驟更新：
1. 訪問 https://fal.ai/llms.txt
2. 檢查新增的模型和分類
3. 更新本文件
4. 更新文件頂部的日期
