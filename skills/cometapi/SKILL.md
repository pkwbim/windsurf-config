---
name: cometapi
description: |
  Expert knowledge for using CometAPI - a unified API providing access to 500+ AI models from multiple providers.
  Use this skill when:
  - User wants to call AI models via CometAPI
  - User asks about available models on CometAPI
  - User needs help with CometAPI authentication, endpoints, or pricing
  - User mentions "CometAPI", "comet api", or wants to use a unified AI API
  - User wants to compare or select models from multiple providers
---

# CometAPI Skill

CometAPI is a unified API that provides access to **500+ AI models** from multiple providers through a single interface.

## Quick Reference

| Resource | URL |
|----------|-----|
| Homepage | https://www.cometapi.com/ |
| Model Catalog | https://www.cometapi.com/models/ |
| API Documentation | https://apidoc.cometapi.com/ |
| Changelog | https://www.cometapi.com/changelog/ |

## How to Search for Models

1. **Browse all models**: Visit https://cometapi.com/models/
2. **View model details**: Use pattern `https://cometapi.com/en/models/{provider}/{model-id}/`
3. **Filter by capability**: Text-to-image, audio-to-text, code generation, etc.

## API Usage

### Base URL
Refer to https://apidoc.cometapi.com/ for:
- Authentication (API key setup)
- Base URLs and endpoints
- Request/response schemas
- Rate limits
- SDK examples

### Common Workflow

1. Get API key from CometAPI dashboard
2. Set `Authorization: Bearer <API_KEY>` header
3. Call the appropriate endpoint based on model type
4. Handle response according to model's output format

## Support Resources

| Channel | Contact |
|---------|---------|
| Email | support@cometapi.com |
| Discord | https://discord.com/invite/HMpuV6FCrG |
| GitHub | https://github.com/CometAPI-dev |
| Twitter/X | https://x.com/cometapi2025 |

## When to Use This Skill

- **Model discovery**: Finding the right model for a task
- **API integration**: Setting up CometAPI in a project
- **Pricing lookup**: Checking model costs
- **Troubleshooting**: Debugging API calls or authentication issues

## References

See `references/llms.txt` for the complete CometAPI LLM instructions document.
