---
description: Interview user to generate structured backlog items
---

## Purpose
透過問卷式訪談，引導用戶描述需求，AI 產生結構化的 User Story，確認後加入 `_planning/01_backlog.md`。

## Steps

1. Read `docs/MISSION.md` and `docs/PRODUCT_VISION.md` for context
2. Create a discussion file in `discussions/` with the interview questions:

### 訪談問題模板

```markdown
# Backlog 訪談

## 1. 使用情境
你想解決什麼問題？在什麼情況下會用到這個功能？

**答：**

## 2. 目標用戶
這是給誰用的？（桌機用戶 / 手機用戶 / 兩者）

**答：**

## 3. 期望結果
完成後，你希望看到什麼？有什麼具體的輸出或行為？

**答：**

## 4. 優先級
這個功能有多急？（高 / 中 / 低）

**答：**

## 5. 補充說明（選填）
有沒有其他細節、限制、或參考？

**答：**
```

3. Wait for user to answer, then read the discussion file
4. Generate User Story in this format:
   ```
   - [ ] **Story-XXX ([Category]):** 身為 [角色]，我想要 [功能]，以便於 [價值]。
   ```
5. Show the generated story to user for confirmation
6. After user confirms, append to `_planning/01_backlog.md` under "## 待辦事項"

## Notes
- Category examples: Desktop, Mobile, Sync, Memory, Privacy, Plugin
- Story ID should be sequential (check existing stories first)
- Always link back to MISSION/VISION core values when explaining the story
