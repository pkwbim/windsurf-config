---
name: scope
description: >
  判斷規格變動（遺漏、新需求、調整）的範圍與處理方式。
  當使用者發現規格遺漏、想要修改現有功能、或新增需求時使用。
  判斷應該：(1) 修改當前 Story 規格並更新程式，(2) 加入 Backlog，或 (3) 新建 Story。
  觸發時機：使用者說「我想加入...」、「發現遺漏...」、「規格要改...」、「這個要不要做」、執行 /scope 指令。
---

# Scope Skill

此 skill 提供 `/scope` workflow 所需的判斷標準、規格調整步驟、和文件更新順序。

---

## 判斷框架

### 第一步：核心 vs 非核心

**核心功能**（符合任一條件）：
- 沒有這個功能，Story 無法通過驗收
- 影響資料庫結構（表/欄位/關聯）
- 影響路由或 Controller 設計
- 使用者無法完成主要任務
- 影響其他 BC 的依賴（Shared Kernel）

**非核心功能**（符合任一條件）：
- 優化或增強現有功能（UI 美化、效能改善）
- 可獨立開發，不影響當前功能
- 便利功能（快捷鍵、排序選項）
- 處理極少發生的邊緣情況

### 第二步：影響大小（核心功能才需判斷）

**影響小（< 2h）**：
- 只改 Blade 模板或 CSS
- 只加欄位到現有表格（無關聯）
- 只加驗證規則到現有 FormRequest
- 只補 page spec 或 spec.md 說明

**影響大（> 2h）**：
- 需要新的 Migration 或修改現有 Migration
- 需要新的 Use Case 或 Domain Entity
- 需要新的路由或 Controller 方法
- 影響多個頁面或多個 BC

---

## 決策矩陣

| 類型 | 影響 | 階段 | 決策 |
|------|------|------|------|
| 核心 | 小 | 任何 | **修改當前 Story**（先改規格，再改程式） |
| 核心 | 大 | 規劃中 | **修改當前 Story**（更新 use-cases、spec） |
| 核心 | 大 | 開發中 | **停止評估**（可能需要重新規劃或拆分） |
| 核心 | 大 | 測試中 | **停止評估**（評估是否 rollback） |
| 非核心 | 任何 | 任何 | **加入 Backlog** |
| 全新功能 | 大 | 任何 | **新建 Story**（執行 /plan） |

---

## 規格調整順序（修改當前 Story 時）

**必須按此順序，先改規格再改程式：**

### 1. 判斷影響哪些規格文件

| 變動類型 | 需更新的文件 |
|---------|------------|
| 頁面欄位變動 | `pages/page-{name}.md` → `spec.md` Frontend 章節 |
| 業務規則變動 | `business-rules.md` → `spec.md` Domain 章節 |
| 資料庫欄位變動 | `spec.md` DB Model → `business-rules.md` |
| 路由變動 | `spec.md` 路由表 |
| Use Case 變動 | `use-cases.md` → `spec.md` Use Cases 章節 |

### 2. 規格更新步驟

```
1. 更新 page spec（若影響頁面顯示）
   → pm/planning/stories/{story}/pages/page-{name}.md

2. 更新 spec.md（Frontend 章節 / Domain 章節 / 路由表）

3. 更新 business-rules.md（若有業務規則變動）

4. 更新 use-cases.md（若有流程變動）

5. 更新 checklist.md（標記此變動）
```

### 3. 程式更新步驟（規格確認後）

```
1. 修改 Blade 模板（若影響 UI）
2. 修改 FormRequest（若影響驗證）
3. 修改 Controller（若影響邏輯）
4. 修改 Migration（若影響 DB，需重新執行）
5. Commit（附上規格變動說明）
```

---

## 輸出格式

每次執行 `/scope` 必須輸出：

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

---

## 特殊情況

### 規格遺漏 vs 新需求

- **規格遺漏**（原本應該有但沒寫）→ 直接補規格，不需要 `/discussion`
- **新需求**（原本沒想到的功能）→ 先用 `/discussion` 確認，再決定放哪裡

### Page Spec 遺漏

若發現某頁面沒有 page spec 但需要定義欄位：
- 建立 `pm/planning/stories/{story}/pages/page-{name}.md`
- 參考 `pm/specs/ui/layouts/` 確認 Layout 和 Areas
- 這屬於「規格遺漏」，影響小，直接補充

### 跨 Story 影響

若變動影響其他 Story（如修改 Shared Kernel）：
- 標記為「影響大」
- 在決策中說明對其他 Story 的影響
- 建議先完成當前 Story 再處理
