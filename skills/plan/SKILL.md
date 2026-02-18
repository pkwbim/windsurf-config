---
name: plan
description: /plan workflow 的專業知識包。提供 Use Case 格式規範、業務規則格式規範、DDD 分析方法，以及 story 目錄下各文件的撰寫指引。當執行 /plan workflow 時必須參考此 skill。
---

# Plan Skill

此 skill 提供 `/plan` workflow 所需的所有格式規範與分析方法。

---

## 📁 Story 目錄文件結構

每個 story 目錄包含以下文件，依序產生：

```
STORY-001-CamelCaseDesc/
├── use-cases.md          # 1. Use Case 清單（先產生，確認後再繼續）
├── business-rules.md     # 2. 業務規則（確認後同時產生）
├── spec.md               # 3. 技術規格（確認後同時產生）
├── checklist.md          # 4. 開發進度追蹤（確認後同時產生）
├── e2e-scenarios.md      # 5. E2E 測試劇本（確認後同時產生）
├── discussions/          # 此 story 的討論問卷
└── decisions/            # 此 story 的決策文件
```

**執行順序：**
1. 產生 `use-cases.md` → 等待使用者確認
2. 確認後，同時產生 `business-rules.md`、`spec.md`、`checklist.md`、`e2e-scenarios.md`

---

## 📋 Use Case 文件規範（use-cases.md）

### 文件目的
定義系統的功能需求：誰（Actor）要做什麼（Use Case），以及流程和條件。

### 文件結構
```markdown
# Use Cases：[Story 標題]

## Actors（使用者角色）
- **[角色名稱]**：[角色說明]
- **[角色名稱]**：[角色說明]

---

## UC-01：[Use Case 名稱]

| 欄位 | 內容 |
|------|------|
| **Actor** | [主要使用者角色] |
| **觸發條件** | [什麼情況下觸發此 Use Case] |
| **前置條件** | [執行前必須滿足的條件] |
| **後置條件** | [成功執行後的系統狀態] |

### 主要流程
1. [步驟 1]
2. [步驟 2]
3. [步驟 3]

### 替代流程
- **[情況]**：[替代步驟]

### 例外流程
- **[錯誤情況]**：[系統如何處理]

---

## UC-02：[Use Case 名稱]
...
```

### Use Case 識別原則
- 每個 Use Case 對應一個**使用者目標**（不是系統動作）
- 命名格式：動詞 + 名詞（如「建立帳號」、「查詢訂單」）
- 一個 story 通常有 2-6 個 Use Case
- 複雜的 Use Case 可以有子 Use Case（`UC-01a`、`UC-01b`）

---

## 📏 業務規則文件規範（business-rules.md）

### 文件目的
記錄所有業務邏輯規則、驗證條件、業務限制。這些規則會在 Domain Layer 實作。

### 文件結構
```markdown
# Business Rules：[Story 標題]

## BR-01：[規則名稱]

| 欄位 | 內容 |
|------|------|
| **分類** | 驗證規則 / 業務限制 / 計算規則 / 狀態規則 |
| **適用對象** | [Entity 或 Value Object 名稱] |
| **規則描述** | [詳細說明] |
| **實作位置** | [Domain Entity / Value Object / Use Case] |

**規則細節：**
- [具體條件 1]
- [具體條件 2]

**錯誤訊息：** `[當規則違反時顯示的訊息]`

---

## BR-02：[規則名稱]
...

## 規則分類索引

| 規則 ID | 名稱 | 分類 | 適用對象 |
|---------|------|------|----------|
| BR-01 | [名稱] | [分類] | [對象] |
```

### 業務規則分類
- **驗證規則**：輸入資料的格式、長度、範圍（如密碼長度）
- **業務限制**：業務邏輯上的限制（如每人最多 3 個帳號）
- **計算規則**：金額計算、折扣計算等
- **狀態規則**：狀態機轉換條件（如訂單只能從「待付款」→「已付款」）

---

## 🏗️ 技術規格文件規範（spec.md）

### 文件目的
記錄技術實作規格：Domain 設計、API 端點、Frontend 頁面與路由、DB Migration。
**不包含** Use Case 和業務規則（已在獨立文件中）。

### 文件結構
```markdown
# 技術規格：[Story 標題]

**Story ID**: STORY-{流水號}-{CamelCase描述}
**📊 開發狀態**: 🔵 規劃中
**相關文件**：
- Use Cases：`use-cases.md`
- Business Rules：`business-rules.md`

## 開發階段檢查清單
[checklist]

---

## 1. Domain Design (DDD)

### Bounded Context
- **所屬領域**：[領域名稱]
- **Aggregate Root**：[聚合根]
- **領域語言**：[核心術語定義]

### Entities
| Entity | 屬性 | 業務方法 | 對應 BR |
|--------|------|----------|---------|
| [名稱] | [屬性列表] | [方法列表] | BR-01, BR-02 |

### Value Objects
| Value Object | 屬性 | 驗證規則 | 對應 BR |
|--------------|------|----------|---------|
| [名稱] | [屬性] | [規則] | BR-01 |

### Use Cases（Application Layer）
| Use Case | 輸入 | 輸出 | 對應 UC |
|----------|------|------|---------|
| [名稱] | [DTO] | [DTO] | UC-01 |

### Contracts (shared_contracts/)
- **Protocol**: `interfaces/[名稱]Protocol`
- **DTO**: `dto/[名稱]Create`, `[名稱]Response`, `[名稱]Update`

---

## 2. Backend（Infrastructure Layer）

### Repository
- `[名稱]Repository` - [說明]

### Models（DB）
| Model | 欄位 | 索引 |
|-------|------|------|
| [名稱] | [欄位列表] | [索引] |

### API 端點
| Method | Path | Request | Response | 對應 UC |
|--------|------|---------|----------|---------|
| POST | `/api/...` | [DTO] | [DTO] | UC-01 |
| GET | `/api/...` | - | [DTO] | UC-02 |

### Database Migration
- [ ] 需要 Migration：是 / 否
- [ ] Migration 說明：[新增表/修改欄位等]

---

## 3. Frontend

### 頁面與路由
| 頁面名稱 | URL | 元件路徑 | 對應 UC |
|----------|-----|----------|---------|
| [頁面] | `/path` | `views/[名稱].vue` | UC-01 |

### 元件
- [ ] `[元件名稱]` - [說明]

### 路由設定（`frontend/src/router/`）
```javascript
{ path: '/path', component: () => import('@/views/[名稱].vue') }
```

---

## 4. Testing Criteria

### Backend Unit Tests
- [ ] [Service 名稱] - [測試案例]

### Backend Integration Tests
- [ ] `[Method] /api/...` - [測試案例]

### Frontend Tests
- [ ] [元件名稱] - [測試案例]

### Manual Testing
- [ ] [手動測試項目]

---

## 5. Implementation Notes

### 開發重點
- [重點]

### 技術挑戰
- [挑戰]

### 相依性
- [ ] 依賴 Story：[Story ID]
```

---

## 🎯 DDD 分析方法

### 步驟 1：識別 Bounded Context
- 問：「這個功能屬於哪個業務領域？」
- 常見領域：Identity（身份認證）、Order（訂單）、Product（產品）、Payment（付款）
- 一個 story 通常只涉及 1-2 個 Bounded Context
- **跨 BC 依賴分析**：
  - 問：「這個 BC 需要從其他 BC 取得資料嗎？」→ 依賴關係
  - 問：「這個 BC 的事件會影響其他 BC 嗎？」→ 被依賴關係
  - 溝通方式選擇：
    - **Domain Event**：非同步通知（如 `UserRegistered`、`OrderPlaced`）
    - **ACL（Anti-Corruption Layer）**：轉換外部 BC 的模型，避免污染本 BC
    - **Shared Kernel**：兩個 BC 共用少量模型（謹慎使用）
  - 若無跨 BC 依賴：明確記錄「無」，避免未來誤解

### 步驟 2：識別 Aggregate Root
- 問：「這個功能的核心業務物件是什麼？」
- Aggregate Root 是有唯一 ID 的 Entity，負責維護業務不變量
- 範例：`User`、`Order`、`Product`

### 步驟 3：識別 Entity vs Value Object
- **Entity**：有唯一 ID，生命週期內狀態可變（如 `User`、`Order`）
- **Value Object**：無 ID，不可變，用值來比較（如 `Email`、`Password`、`Money`）
- 業務規則通常封裝在 Value Object 的建構子中

### 步驟 4：識別 Use Case（Application Layer）
- 每個 UC 對應一個 Application Use Case 類別
- 命名：`[動詞][名詞]UseCase`（如 `CreateUserUseCase`）
- 輸入：Command DTO，輸出：Response DTO

### 步驟 5：定義 Protocol（Interface）
- 定義 Repository 介面：`[名稱]RepositoryProtocol`
- 定義 Service 介面：`[名稱]ServiceProtocol`
- 放在 `shared_contracts/interfaces/`

---

## ✅ Use Case 完整性檢查

產生 `use-cases.md` 後，AI 應自動檢查：

- [ ] 每個 Actor 的主要目標都有對應的 Use Case？
- [ ] CRUD 操作是否完整（Create/Read/Update/Delete）？
- [ ] 是否有遺漏的錯誤流程（如輸入錯誤、權限不足）？
- [ ] Use Case 之間是否有依賴關係需要說明？

## ✅ 業務規則完整性檢查

產生 `business-rules.md` 後，AI 應自動檢查：

- [ ] 所有輸入欄位都有對應的驗證規則？
- [ ] 狀態轉換是否有完整的規則定義？
- [ ] 業務限制（如數量上限）是否都已列出？
- [ ] 每條規則都有明確的錯誤訊息？

---

## 🎭 E2E 測試劇本規範（e2e-scenarios.md）

### 文件目的
描述使用者在瀏覽器上的操作流程，供 Playwright 測試程式開發使用。
每個劇本對應一個 `test()` 區塊。

### 劇本來源對應

| 劇本類型 | 來源 | 說明 |
|----------|------|------|
| 正向劇本 | `use-cases.md` 主要流程 | 每個 UC 至少一個 happy path |
| 替代劇本 | `use-cases.md` 替代流程 | 有替代流程時產生 |
| 負向劇本 | `use-cases.md` 例外流程 + `business-rules.md` | 錯誤輸入、業務規則違反 |

### 劇本格式
```markdown
### S-{序號}：[劇本標題]

| 欄位 | 內容 |
|------|------|
| **對應 UC / BR** | UC-01 / BR-01 |
| **Actor** | [角色] |
| **前置條件** | [測試開始前的系統狀態] |

**操作步驟：**
1. 前往 `[URL]`
2. [操作描述]
3. [操作描述]

**預期結果：**
- [可驗證的結果，如：URL 變為 `/dashboard`]
- [可驗證的結果，如：頁面出現文字「歡迎」]
```

### 劇本命名規則
- 正向劇本：`S-01`、`S-02`...
- 負向劇本：`S-E01`、`S-E02`...

### 操作步驟撰寫原則
- 每個步驟要具體、可執行（「點擊 id=submit 的按鈕」優於「點擊送出」）
- 輸入值要明確（「輸入 `test@example.com`」優於「輸入 email」）
- URL 使用 `spec.md` 路由表格中的實際路徑

### 預期結果撰寫原則
- 必須是可程式驗證的（URL、DOM 元素、文字內容）
- 避免主觀描述（「頁面看起來正確」→ 改為「頁面標題為 XXX」）

## ✅ E2E 劇本完整性檢查

產生 `e2e-scenarios.md` 後，AI 應自動檢查：

- [ ] 每個 UC 都有至少一個正向劇本？
- [ ] 每個例外流程都有對應的負向劇本？
- [ ] 每條業務規則（BR）都有對應的邊界值劇本？
- [ ] 每個劇本的預期結果都是可程式驗證的？
- [ ] 所有 URL 都來自 `spec.md` 的路由表格？
