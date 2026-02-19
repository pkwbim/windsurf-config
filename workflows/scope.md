---
description: 判斷規格變動（遺漏、新需求、調整）的範圍與處理方式。 當使用者發現規格遺漏、想要修改現有功能、或新增需求時使用。 判斷應該：(1) 修改當前 Story 規格並更新程式，(2) 加入 Backlog，或 (3) 新建 Story。 觸發時機：使用者說「我想加入...」、「發現遺漏...」、「規格要改...」、「這個要不要做」、執行 /scope 指令。
---

> **執行此 workflow 前，必須先載入 `scope` skill 的規範。**
> 參考 `.windsurf/skills/scope/SKILL.md` 取得判斷標準、決策矩陣、規格調整順序。

---

## 步驟 1：讀取當前 Story 資訊

// turbo
```bash
cat pm/planning/02_active.md
```

取得：`active_story`（當前 Story ID）和 `active_story_dir`（Story 目錄路徑）

---

## 步驟 2：確認變動內容

若使用者已描述變動 → 直接進入步驟 3。

若使用者只說「我想加功能」等模糊描述 → 詢問：
- 「請描述你想加入或修改的內容？」
- 等待使用者回答後繼續。

---

## 步驟 3：判斷並輸出決策

依照 `scope` skill 的判斷框架，輸出：

```markdown
## 範圍判斷結果

**變動描述**：[使用者描述的變動]

**判斷**：
- 類型：核心功能 / 非核心功能 / 全新功能
- 影響：小（< 2h）/ 大（> 2h）
- 當前階段：規劃中 / UI 開發中 / Contract 開發中 / Backend 開發中 / 測試中
- 原因：[一句話說明判斷依據]

**決策**：修改當前 Story / 加入 Backlog / 新建 Story / 停止評估

**行動步驟**：
1. [具體步驟]
2. [具體步驟]
```

詢問使用者：「確認以上判斷嗎？」

---

## 步驟 4A：修改當前 Story（核心功能 + 影響小）

**⚠️ 必須先改規格，再改程式。**

依照 `scope` skill 的「規格調整順序」執行：

1. **更新規格文件**（依影響範圍選擇）：
   - Page spec：`pm/planning/stories/{story}/pages/page-{name}.md`
   - 技術規格：`pm/planning/stories/{story}/spec.md`
   - 業務規則：`pm/planning/stories/{story}/business-rules.md`
   - Use Cases：`pm/planning/stories/{story}/use-cases.md`

2. **更新 checklist.md**：在對應階段標記此變動

3. **更新程式碼**（規格確認後）：
   - Blade 模板 / FormRequest / Controller / Migration（依影響範圍）

4. **Commit**：
   ```bash
   git add -A && git commit -m "scope: [變動描述]"
   ```

---

## 步驟 4B：加入 Backlog（非核心功能）

// turbo
```bash
cat pm/planning/01_backlog.md
```

在 `pm/planning/01_backlog.md` 末尾加入：
```markdown
- [ ] [功能描述]（來自 STORY-XXX，[日期]）
```

Commit：
```bash
git add pm/planning/01_backlog.md && git commit -m "backlog: 新增 [功能描述]"
```

---

## 步驟 4C：停止評估（核心功能 + 影響大 + 開發中/測試中）

告知使用者：
```
⚠️ 此變動影響較大，建議停下來評估：

選項：
A. 繼續當前 Story，將此需求加入 Backlog，下個 Story 再處理
B. 停止當前 Story，重新規劃（執行 /plan）
C. 拆分：當前 Story 完成核心功能，新建 Story 處理此需求

請告訴我你的選擇。
```

等待使用者決定後執行對應行動。

---

## 步驟 4D：新建 Story（全新功能）

告知使用者：
```
此需求屬於全新功能，建議新建 Story。

我將：
1. 加入 pm/planning/01_backlog.md
2. 你可以在完成當前 Story 後執行 /plan 規劃新 Story
```

執行步驟 4B 加入 Backlog。
