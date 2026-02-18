---
name: discussion
description: 討論與澄清流程的專業知識包。當使用 /discussion workflow 時必須參考此 skill。提供問卷格式規範、front matter 標準、決策文件格式、追問判斷邏輯，以及 discussion/questionnaires/ 和 discussion/decisions/ 目錄的管理規則。
---

# Discussion Skill

此 skill 提供 `/discussion` workflow 所需的所有規範與知識。

## 目錄結構

討論文件有兩種放置位置，依當前是否在執行 story 而定：

**在 story 執行期間**（`pm/planning/02_active.md` 的 `active_story` 不為 null）：
```
pm/planning/stories/{active_story}/
├── discussions/    # 此 story 的討論問卷
│   └── DISC-YYYYMMDDHHMM-{主題}.md
└── decisions/      # 此 story 的決策文件
    └── DEC-YYYYMMDDHHMM-{主題}.md
```

**非 story 執行期間**（全域討論）：
```
discussions/
├── questionnaires/    # 問卷檔案（含追問）
│   └── DISC-YYYYMMDDHHMM-{主題}.md
└── decisions/         # 結論文件
    └── DEC-YYYYMMDDHHMM-{主題}.md
```

## 問卷檔案規範

### 檔案命名
```
DISC-YYYYMMDDHHMM-{主題}.md
```
- 主題使用 PascalCase 英文，簡短描述（3-5 個字）
- 範例：`DISC-202502181106-WorkflowRedesign.md`

### Front Matter 格式
```yaml
---
id: DISC-YYYYMMDDHHMM-{主題}
title: 討論主題（中文簡述）
created_at: YYYY-MM-DD HH:MM
status: open | answered | closed
topic: 主題分類（如：架構設計、功能規劃、工具選擇）
related_decision: DEC-YYYYMMDDHHMM-{主題}  # 有結論後填入，否則留空
---
```

### 問卷內容結構
```markdown
---
[front matter]
---

# 討論主題：[簡短描述]

## 📋 背景說明
[說明當前情境與需求]

## ❓ 問題清單

### 問題 1：[問題標題]
[詳細描述]

**選項（如適用）：**
- A. [選項說明]
- B. [選項說明]

💡 AI 建議：[建議選項]，理由：[簡短說明]

答：

---

### 問題 2：[問題標題]
[詳細描述]

答：

---
```

## 追問規則（重要）

**同一問卷追加**（追問，非新議題）：
- 使用者回答後仍有疑問，且疑問與原主題直接相關
- 在同一個 `.md` 檔案末尾追加新的問題區塊
- 更新 front matter 的 `status` 為 `open`
- 追加格式：

```markdown
---

## 🔄 追問（Round 2）

### 追問 1：[問題標題]
[基於使用者回答的進一步問題]

答：

---
```

**開新問卷**（新議題）：
- 使用者提出的是全新、不相關的主題
- 建立新的 `DISC-YYYYMMDDHHMM-{新主題}.md`

## 決策文件規範

### 檔案命名
```
discussion/decisions/DEC-YYYYMMDDHHMM-{主題}.md
```

### Front Matter 格式
```yaml
---
id: DEC-YYYYMMDDHHMM-{主題}
title: 決策標題（中文）
created_at: YYYY-MM-DD HH:MM
source_questionnaire: DISC-YYYYMMDDHHMM-{主題}
status: decided
topic: 主題分類
---
```

### 決策文件內容結構
```markdown
---
[front matter]
---

# 決策：[標題]

## 📋 背景摘要
[簡述討論背景]

## ✅ 決策結論

### [決策項目 1]
**決定**：[具體決定]
**理由**：[使用者的理由或說明]

### [決策項目 2]
**決定**：[具體決定]
**理由**：[使用者的理由或說明]

## 📌 後續行動
- [ ] [需要執行的行動 1]
- [ ] [需要執行的行動 2]

## 🔗 參考
- 問卷來源：`discussion/questionnaires/DISC-YYYYMMDDHHMM-{主題}.md`
```

## 問題設計原則

- 問題數量不限，有需要釐清的就問
- 問題要具體，避免「你想要什麼？」這類籠統問題
- 有選項時提供 A/B/C 選項，降低使用者回答成本
- **有選項時必須給出 AI 建議**：在選項後加上「💡 AI 建議：[建議選項]，理由：[簡短說明]」
- 每個問題後立即放「答：」讓使用者就地回答

## Status 流轉

```
open → answered（使用者回答後）→ closed（產生決策文件後）
```
若有追問，status 從 `answered` 回到 `open`。
