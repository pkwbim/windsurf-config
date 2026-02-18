---
description: 純討論與澄清流程 - 產生問卷並等待回覆，與其他 workflow 完全獨立
---

## ⚠️ 重要原則

> **執行此 workflow 前，必須先載入 `discussion` skill 的規範。**

- **不執行任何實作**：此 workflow 僅用於討論和澄清
- **必須停下來等待**：產生問卷後，必須等待使用者回覆
- **不猜測答案**：不確定就問清楚

---

## 步驟 1：載入 Discussion Skill

參考 `.windsurf/skills/discussions/SKILL.md` 取得：
- 問卷 front matter 格式
- 問卷內容結構
- 追問 vs 新問卷的判斷規則
- 決策文件格式

---

## 步驟 2：判斷是否需要開問卷

**自我檢查：**
- [ ] 需求範圍是否 100% 清楚？
- [ ] 是否有需要使用者決定的選項？
- [ ] 是否涉及重要決策？

**判斷結果：**
- **有任何疑問** → 繼續步驟 3
- **完全清楚** → 告知使用者「需求已清楚，無需討論。」然後**停止**

---

## 步驟 3：產生問卷檔案

在 `discussions/questionnaires/` 建立新檔案，依照 discussion skill 的規範：

**檔案路徑：**
```
discussions/questionnaires/DISC-YYYYMMDDHHMM-{主題}.md
```

**必須包含 front matter（參考 skill 規範）**，然後依格式撰寫問題（3-5 個）。

---

## 步驟 4：通知使用者並停止

告訴使用者：

```
我已建立問卷：`discussions/questionnaires/[檔案名稱]`

請在檔案中各問題的「答：」後填寫回答。完成後，請告訴我「我已回答」。

⚠️ 在您回答之前，我不會執行任何動作。
```

**完全停止，不執行任何其他動作。**

---

## 步驟 5：等待使用者回覆

- 等待使用者說「我已回答」或類似確認語
- **未收到確認前不繼續**

---

## 步驟 6：讀取問卷並判斷

// turbo
```bash
cat discussions/questionnaires/[檔案名稱]
```

讀取後判斷：

**A. 所有問題已清楚回答** → 繼續步驟 7

**B. 使用者的回答引發追問（同一主題）：**
- 在**同一個問卷檔案末尾**追加「🔄 追問（Round N）」區塊
- 更新 front matter `status: open`
- 通知使用者追問已加入，請繼續回答
- **停止等待**

**C. 使用者提出全新議題：**
- 建立新的問卷檔案 `DISC-YYYYMMDDHHMM-{新主題}.md`
- 通知使用者，**停止等待**

---

## 步驟 7：產生決策文件

在 `discussions/decisions/` 建立結論文件，依照 discussion skill 的規範：

**檔案路徑：**
```
discussions/decisions/DEC-YYYYMMDDHHMM-{主題}.md
```

**必須包含 front matter**，`source_questionnaire` 填入對應問卷 ID。

同時更新問卷的 front matter：
- `status: closed`
- `related_decision: DEC-YYYYMMDDHHMM-{主題}`

---

## 步驟 8：通知完成並停止

告訴使用者：

```
✅ 討論完成！

- 問卷：`discussions/questionnaires/[問卷檔名]`（status: closed）
- 決策：`discussions/decisions/[決策檔名]`

[簡述決策結論 2-3 行]

如需繼續其他工作，請告訴我。
```

**停止，等待使用者下一步指示。**

---

## ⚠️ 常見錯誤避免

- ❌ 不要猜測答案就繼續執行
- ❌ 不要在討論階段開始寫程式或修改檔案
- ❌ 不要問太籠統的問題（例如「你想要什麼？」）
- ❌ 不要一次問超過 5 個問題
- ❌ 追問時不要開新問卷（除非是全新議題）
- ❌ 不要把問卷存到 `discussions/`（舊路徑），要存到 `discussions/questionnaires/`
