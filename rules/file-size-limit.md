---
trigger: glob
glob: "src/**/*.{py,ts,tsx,js,jsx,vue,rs}"
---

# 📏 檔案大小限制

## 規範
- 每個程式檔案**不超過 200 行**
- 接近 200 行時，主動提醒重構

## 超過時的處理策略

### Python
- 拆分為多個模組
- 提取共用邏輯到 `utils/` 或 `helpers/`
- 使用 Mixin 或組合模式

### TypeScript / JavaScript / React
- 拆分為多個元件
- 提取 hooks 到獨立檔案
- 提取工具函式到 `utils/`

### Vue
- 拆分為多個子元件
- 提取 composables
- 提取工具函式

### Rust
- 拆分為多個模組
- 使用 `mod.rs` 組織

## 例外情況
- 自動生成的檔案（如 migrations）
- 測試檔案（可放寬至 300 行）
- 設定檔案

## 檢查時機
- 建立新檔案時
- 修改現有檔案時
- Code Review 時
