---
description: 設定專案技術棧 - 詢問並更新所有 AGENTS.md 檔案中的技術棧資訊
---

## 🎯 目的
透過 `/discussion` 流程，收集專案的技術棧選擇，並記錄到 `docs/tech-stack.md`。

## ⚠️ 重要原則
- **使用 /discussion 流程**：透過單一討論檔案收集所有技術棧資訊
- **必須停下來等待**：產生討論檔案後，必須等待使用者回覆
- **只記錄到 docs/tech-stack.md**：不更新 AGENTS.md（由 `/setup-agents` 負責）

## 🔗 執行順序
此 workflow 是四階段初始化流程的第二階段：
1. `/setup-project-info` - 建立非技術目錄 ✅
2. `/setup-techstack` - 設定技術棧 ← 你在這裡
3. `/setup-structure` - 建立 src/ 目錄結構
4. `/setup-agents` - 建立 AGENTS.md

---

## 📋 執行步驟

### 1. 建立技術棧討論檔案

在 `discussions/` 資料夾建立討論檔案：

**檔案命名格式：**
```
discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md
```

**檔案內容：**
複製 `.windsurf/templates/discussion-techstack.md` 模板內容

### 2. 通知使用者並停止

告訴使用者：

```
我已建立技術棧討論檔案：`discussions/DISC-YYYYMMDD-HHMM-TechStackSetup.md`

請在檔案中回答問題：
1. 選擇 Preset 或自訂
2. 如果選 Preset，填入數字
3. 在表格中填入「您的選擇」欄位（只需填想修改的項目）

完成後，請告訴我「我已回答」。

⚠️ 在您回答之前，我不會執行任何動作。
```

**然後完全停止，不執行任何其他動作。**

### 3. 等待使用者回覆
- 使用者會說「我已回答」或類似的話
- **只有在使用者明確表示已回答後，才繼續下一步**

### 4. 讀取並處理結果

讀取討論檔案，根據使用者的選擇：

1. **判斷 Preset 或自訂**
2. **載入 Preset 預設值（如適用）**
3. **套用使用者的修改**
4. **顯示最終配置摘要，請使用者確認**

---

## 📦 Preset 預設值參考

參考 `.windsurf/templates/techstack-presets.yaml`

| # | Preset 名稱 | 後端 | 前端 |
|---|------------|------|------|
| 1 | fullstack-python-vue | Python + FastAPI | Vue 3 + Pinia |
| 2 | fullstack-python-react | Python + FastAPI | React 19 + Zustand |
| 3 | fullstack-python-astro | Python + FastAPI | Astro + React 19 |
| 4 | backend-only | Python + FastAPI | 無 |
| 5 | frontend-only | 無 | Vue 3 + Pinia |

---

## 📝 寫入 docs/tech-stack.md

確認後，根據 `.windsurf/templates/tech-stack.md` 模板格式，將技術棧資訊寫入 `docs/tech-stack.md`

---

## ✅ 完成訊息

```
✅ 技術棧設定完成！

已更新的檔案：
- docs/tech-stack.md

下一步：
- 執行 `/setup-structure` 建立 src/ 目錄結構
- 執行 `/setup-agents` 建立 AGENTS.md
```

## 📝 注意事項

1. 此 workflow 只更新 `docs/tech-stack.md`
2. 不會更新 AGENTS.md（由 `/setup-agents` 負責）
3. 只需一張問卷，一次完成所有設定
4. 可以重複執行此 workflow 來更新技術棧
5. Preset 詳細比較請參考 `docs/techstack-presets-comparison.md`
