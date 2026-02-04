# CometAPI Usage Guide

## Authentication

CometAPI uses API keys for authentication. Include your API key in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

## API Base URL

Primary endpoint: Refer to https://apidoc.cometapi.com/ for the current base URL.

## Common Use Cases

### 1. Text Generation (LLM)
Call language models like GPT-4, Claude, Llama, etc.

### 2. Image Generation
Models for text-to-image generation (DALL-E, Stable Diffusion, Midjourney, etc.)

### 3. Audio Processing
- Speech-to-text (Whisper, etc.)
- Text-to-speech

### 4. Code Generation
Specialized coding models

### 5. Embeddings
Vector embeddings for semantic search

## Finding the Right Model

1. Visit https://cometapi.com/models/
2. Filter by:
   - **Provider**: OpenAI, Anthropic, Google, Meta, etc.
   - **Capability**: text, image, audio, code
   - **Pricing tier**: Check per-model costs

3. Get model details at: `https://cometapi.com/en/models/{provider}/{model-id}/`

## Example: Python Integration

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "https://api.cometapi.com/v1"  # Check docs for current URL

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Example: Chat completion
response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers=headers,
    json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)

print(response.json())
```

## Rate Limits

Check https://apidoc.cometapi.com/ for:
- Requests per minute
- Tokens per minute
- Concurrent request limits

## Error Handling

Common error codes:
- `401`: Invalid API key
- `429`: Rate limit exceeded
- `500`: Server error

## Getting Help

- **API Docs**: https://apidoc.cometapi.com/
- **Email**: support@cometapi.com
- **Discord**: https://discord.com/invite/HMpuV6FCrG
