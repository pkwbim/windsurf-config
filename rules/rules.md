---
trigger: always_on
---

做任何事情前，但看看 windsurf 的 skills 裡有無可以用的 skill，如果有就用。

如果這件事值得做成 skill 再執行效果更好的話，就
1. 去網路上查 windsurf 的 skills 是什麼，先去了解。
2. 使用 [skill-creator](../skills/skill-creator) 來創建新的 skill，再執行。


## 禁止在 chat 直接問需求問題

**任何需要使用者決策或澄清的問題，禁止直接在 chat 中詢問。**
必須執行 `/discussion` workflow，建立 `DISC-*.md` 問卷檔案後，再告知使用者「請查看問卷檔案並填寫回答」。

這條規則的目的：
- 確保所有決策有檔案記錄可追溯
- 避免重要決策只存在於 chat 歷史中
- 符合 workflow 規範（`/plan`、`/discussion` 等都要求寫問卷檔案）
