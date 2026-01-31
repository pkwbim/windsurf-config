# fal.ai API 使用範例

## 基本設定

### JavaScript/TypeScript

```bash
npm install --save @fal-ai/client
```

```javascript
import { fal } from "@fal-ai/client";

// 設定 API Key
fal.config({
  credentials: "YOUR_FAL_KEY"
});

// 或使用環境變數
// export FAL_KEY="YOUR_API_KEY"
```

### Python

```bash
pip install fal-client
```

```python
import fal_client

# API Key 會自動從環境變數 FAL_KEY 讀取
# 或手動設定
fal_client.api_key = "YOUR_FAL_KEY"
```

## Z-Image Turbo 範例

### Text-to-Image (JavaScript)

```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/z-image/turbo", {
  input: {
    prompt: "A hyper-realistic portrait of a tribal elder",
    num_inference_steps: 4,  // 1-8 步
    num_images: 1,            // 最多 4 張
    image_size: "square_hd"   // 或 "landscape_4_3" 等
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  }
});

console.log(result.data.images[0].url);
```

### Image-to-Image (Python)

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/z-image/turbo/image-to-image",
    arguments={
        "prompt": "turn this into a watercolor painting",
        "image_url": "https://example.com/input.jpg",
        "strength": 0.8,  # 0.0-1.0，越高變化越大
        "num_inference_steps": 4
    }
)

print(result["images"][0]["url"])
```

### LoRA (JavaScript)

```javascript
const result = await fal.subscribe("fal-ai/z-image/turbo/lora", {
  input: {
    prompt: "a portrait in anime style",
    loras: [
      {
        path: "https://example.com/anime-style.safetensors",
        scale: 1.0
      },
      {
        path: "https://example.com/character.safetensors",
        scale: 0.8
      }
    ],
    num_images: 4  // 一次生成 4 張
  }
});
```

### ControlNet (Python)

```python
result = fal_client.subscribe(
    "fal-ai/z-image/turbo/controlnet",
    arguments={
        "prompt": "a beautiful landscape",
        "control_image_url": "https://example.com/edge-map.jpg",
        "controlnet_conditioning_scale": 0.8,
        "control_mode": "canny"  # 或 "depth", "pose" 等
    }
)
```

## FLUX 系列範例

### FLUX.1 [dev] (JavaScript)

```javascript
const result = await fal.subscribe("fal-ai/flux/dev", {
  input: {
    prompt: "a rhino in a suit sitting at a bar",
    image_size: "landscape_16_9",
    num_inference_steps: 28,
    guidance_scale: 3.5,
    num_images: 1
  }
});
```

### FLUX.1 [schnell] - 快速版本

```javascript
const result = await fal.subscribe("fal-ai/flux/schnell", {
  input: {
    prompt: "a cute puppy",
    num_inference_steps: 4,  // schnell 只需 1-4 步
    image_size: "square_hd"
  }
});
```

### FLUX1.1 [pro] Ultra - 最高品質

```javascript
const result = await fal.subscribe("fal-ai/flux-pro/v1.1-ultra", {
  input: {
    prompt: "ultra detailed portrait",
    image_size: "landscape_16_9",
    safety_tolerance: "2",  // 安全等級
    output_format: "jpeg"
  }
});
```

## 影片生成範例

### MiniMax Image-to-Video

```javascript
const result = await fal.subscribe("fal-ai/minimax-video/image-to-video", {
  input: {
    prompt: "A woman walks down a Tokyo street",
    image_url: "https://example.com/start-frame.jpg"
  }
});

console.log(result.data.video.url);
```

### Veo 3 - 文字生成影片

```python
result = fal_client.subscribe(
    "fal-ai/veo3",
    arguments={
        "prompt": "A cat playing piano in a jazz club",
        "duration": 5,  # 秒數
        "aspect_ratio": "16:9"
    }
)
```

## 音訊處理範例

### Voice Clone

```javascript
const result = await fal.subscribe("fal-ai/minimax/voice-clone", {
  input: {
    audio_url: "https://example.com/voice-sample.mp3",  // 參考音訊
    text: "Hello, this is a cloned voice speaking."
  }
});
```

### Text-to-Speech

```python
result = fal_client.subscribe(
    "fal-ai/minimax/speech-02-hd",
    arguments={
        "text": "你好，這是語音合成測試",
        "voice_id": "female_calm",
        "language": "zh"
    }
)
```

## 進階功能

### 即時串流 (WebSocket)

```javascript
import { fal } from "@fal-ai/client";

const connection = fal.realtime.connect("fal-ai/flux/schnell", {
  onResult: (result) => {
    console.log("Received:", result);
    // 即時顯示生成的圖片
  },
  onError: (error) => {
    console.error("Error:", error);
  }
});

// 發送請求
connection.send({
  prompt: "a beautiful sunset",
  sync_mode: true
});

// 關閉連接
connection.close();
```

### 批次處理

```python
import fal_client

prompts = [
    "a cat",
    "a dog", 
    "a bird"
]

handlers = []
for prompt in prompts:
    handler = fal_client.submit(
        "fal-ai/z-image/turbo",
        arguments={"prompt": prompt}
    )
    handlers.append(handler)

# 等待所有結果
results = [handler.get() for handler in handlers]
```

### 檔案上傳

```javascript
import { fal } from "@fal-ai/client";

// 上傳本地檔案
const file = await fal.storage.upload(fileBlob);
console.log(file.url);  // 使用這個 URL 作為 image_url

// 使用上傳的檔案
const result = await fal.subscribe("fal-ai/z-image/turbo/image-to-image", {
  input: {
    prompt: "make it artistic",
    image_url: file.url
  }
});
```

### 錯誤處理

```javascript
try {
  const result = await fal.subscribe("fal-ai/z-image/turbo", {
    input: { prompt: "test" }
  });
  console.log(result.data);
} catch (error) {
  if (error.status === 429) {
    console.error("Rate limit exceeded");
  } else if (error.status === 400) {
    console.error("Invalid input:", error.message);
  } else {
    console.error("Error:", error);
  }
}
```

## 常用參數說明

### 圖片尺寸 (image_size)
- `square` - 1024x1024
- `square_hd` - 1536x1536
- `portrait_4_3` - 768x1024
- `portrait_16_9` - 576x1024
- `landscape_4_3` - 1024x768
- `landscape_16_9` - 1024x576

### 推理步數 (num_inference_steps)
- Z-Image Turbo: 1-8 步（推薦 4 步）
- FLUX schnell: 1-4 步
- FLUX dev: 20-50 步（推薦 28 步）

### 引導強度 (guidance_scale)
- 範圍: 1.0-20.0
- 較低值: 更有創意，較不遵循提示詞
- 較高值: 更嚴格遵循提示詞
- 推薦: 3.5-7.5

## 最佳實踐

### 1. 使用環境變數管理 API Key
```bash
# .env
FAL_KEY=your_api_key_here
```

### 2. 處理長時間運行的請求
```javascript
const result = await fal.subscribe("fal-ai/model", {
  input: { /* ... */ },
  pollInterval: 5000,  // 每 5 秒檢查一次狀態
  logs: true,
  onQueueUpdate: (update) => {
    console.log("Status:", update.status);
  }
});
```

### 3. 使用 Webhook（適合伺服器端）
```python
result = fal_client.submit(
    "fal-ai/z-image/turbo",
    arguments={"prompt": "test"},
    webhook_url="https://your-server.com/webhook"
)
# 結果會 POST 到你的 webhook URL
```

### 4. 成本優化
- 使用較小的圖片尺寸
- 減少推理步數（在品質可接受範圍內）
- 批次處理多個請求
- 使用快速模型（如 Z-Image Turbo）

## 參考連結

- API 文件: https://fal.ai/docs
- JavaScript SDK: https://github.com/fal-ai/fal-js
- Python SDK: https://github.com/fal-ai/fal-python
- 範例程式碼: https://github.com/fal-ai/examples
