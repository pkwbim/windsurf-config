---
name: plan
description: /plan workflow 的專業知識包。提供 Use Case 格式規範、業務規則格式規範、DDD 分析方法，以及 story 目錄下各文件的撰寫指引。支援 Web App 和 CLI/腳本兩種專案類型。當執行 /plan workflow 時必須參考此 skill。
---

# Plan Skill

此 skill 提供 `/plan` workflow 所需的所有格式規範與分析方法。

---

## 🔍 專案類型判斷

開始規劃前，先判斷 Story 屬於哪種專案類型，後續文件結構會依此調整：

| 類型 | 特徵 | spec.md 結構 | E2E 測試方式 |
|------|------|-------------|-------------|
| **Web App** | 有 API 端點、Frontend 頁面、DB Migration | DDD + API + Frontend | 瀏覽器 Playwright |
| **CLI / 腳本** | Makefile 指令、Shell/Python 腳本、SSH 遠端操作 | 架構總覽 + 指令介面 + 腳本結構 + 模板 | 終端機指令 + 驗證命令 |
| **混合型** | Web 介面呼叫後端腳本 | 兩者結合 | 瀏覽器 + 終端機 |

**判斷方式：**
1. 看 Story 的 Actor 是透過瀏覽器操作還是終端機操作
2. 看產出物是 API/頁面還是 Makefile 指令/腳本
3. 若不確定，詢問使用者

---

## � Story 目錄文件結構

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
記錄所有業務邏輯規則、驗證條件、業務限制。
- **Web App**：這些規則會在 Domain Layer 實作。
- **CLI / 腳本**：這些規則會在腳本的驗證與邏輯模組中實作。

### 文件結構
```markdown
# Business Rules：[Story 標題]

## BR-01：[規則名稱]

| 欄位 | 內容 |
|------|------|
| **分類** | 驗證規則 / 業務限制 / 計算規則 / 狀態規則 |
| **適用對象** | [Entity / Value Object / 輸入參數 / 腳本模組] |
| **規則描述** | [詳細說明] |
| **實作位置** | [Domain Entity / Value Object / Use Case / 腳本函式] |

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
- **驗證規則**：輸入資料的格式、長度、範圍（如密碼長度、domain 格式）
- **業務限制**：業務邏輯上的限制（如每人最多 3 個帳號、domain 不可重複）
- **計算規則**：金額計算、命名轉換規則（如 domain → site name）
- **狀態規則**：狀態機轉換條件、回滾規則、流程順序限制

---

## 🏗️ 技術規格文件規範（spec.md）

### 文件目的
記錄技術實作規格。**不包含** Use Case 和業務規則（已在獨立文件中）。

根據專案類型選擇對應的模板：

---

### 模板 A：Web App 型（有 API / Frontend / DB）

```markdown
# 技術規格：[Story 標題]

**Story ID**: STORY-{流水號}-{CamelCase描述}
**📊 開發狀態**: 🔵 規劃中
**專案類型**: Web App
**相關文件**：
- Use Cases：`use-cases.md`
- Business Rules：`business-rules.md`

---

## 1. Domain Design (DDD)

### Bounded Context
- **所屬領域**：[領域名稱]
- **Aggregate Root**：[聚合根]
- **領域語言**：[核心術語定義]

### Entities
| Entity | 屬性 | 業務方法 | 對應 BR |
|--------|------|----------|--------|
| [名稱] | [屬性列表] | [方法列表] | BR-01, BR-02 |

### Value Objects
| Value Object | 屬性 | 驗證規則 | 對應 BR |
|--------------|------|----------|--------|
| [名稱] | [屬性] | [規則] | BR-01 |

### Use Cases（Application Layer）
| Use Case | 輸入 | 輸出 | 對應 UC |
|----------|------|------|--------|
| [名稱] | [DTO] | [DTO] | UC-01 |

### Contracts (shared_contracts/)
- **Protocol**: `interfaces/[名稱]Protocol`
- **DTO**: `dto/[名稱]Create`, `[名稱]Response`, `[名稱]Update`

---

## 2. Backend（Infrastructure Layer）

### ⚠️ 命名一致性對照表（必填）

> 路由前綴、Controller 目錄、DB 表名稱必須使用**同一個英文單字**，避免日後混淆。

| 層次 | 命名 | 本 Story 實際值 |
|------|------|----------------|
| 路由前綴（URL） | 複數名詞 | `/[名稱複數]` |
| Controller 目錄 | 對應路由 | `[名稱複數]/` |
| Controller 類別 | 對應路由 + Controller | `[名稱複數]Controller` |
| DB 表名稱 | 對應路由 | `[名稱複數]` |
| Model 類別 | 單數 | `[名稱單數]` |

### Repository
- `[名稱]Repository` - [說明]

### Models（DB）
| Model | DB 表名 |
|-------|---------|
| [名稱] | [表名] |

### API 端點
| Method | Path | Request | Response | 對應 UC |
|--------|------|---------|----------|--------|
| POST | `/api/...` | [DTO] | [DTO] | UC-01 |
| GET | `/api/...` | - | [DTO] | UC-02 |

### Database Migration
- [ ] 需要 Migration：是 / 否

---

## 3. Frontend

### 頁面與路由
| 頁面名稱 | URL | 元件路徑 | 對應 UC |
|----------|-----|----------|--------|
| [頁面] | `/path` | `views/[名稱].vue` | UC-01 |

### 元件
- [ ] `[元件名稱]` - [說明]

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

### 模板 B：CLI / 腳本型（Makefile + Shell/Python + SSH/API）

```markdown
# 技術規格：[Story 標題]

**Story ID**: STORY-{流水號}-{CamelCase描述}
**📊 開發狀態**: 🔵 規劃中
**專案類型**: CLI / 腳本
**相關文件**：
- Use Cases：`use-cases.md`
- Business Rules：`business-rules.md`

---

## 1. 架構總覽

[描述整體架構：入口（Makefile）→ 腳本 → 遠端操作（SSH/API）的關係]

### 設計原則
- **AI-friendly**：所有指令和輸出都要清楚、結構化，方便 AI Agent 解讀和操作
- **冪等性**：重複執行不會造成破壞
- **原子性**：失敗時完整回滾
- **可追溯**：完整 log 記錄

---

## 2. Makefile 指令介面

### 2.1 `make [指令名稱]`

[Makefile target 定義，含參數說明]

**參數說明（AI Agent 參考）：**

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| `param1` | ✅ | - | [說明] |
| `param2` | ❌ | `default` | [說明] |

**輸出格式（結構化，方便 AI 解讀）：**
```
[範例輸出]
```

---

## 3. 腳本檔案結構

```
src/scripts/
├── [主腳本].sh           # [說明]
├── [輔助腳本].sh         # [說明]
└── lib/
    ├── common.sh         # 共用函式
    ├── validation.sh     # 輸入驗證
    └── [模組].sh         # [說明]
```

---

## 4. 主腳本流程

[流程概要，對應 UC 步驟，含錯誤處理模式]

---

## 5. 遠端操作細節

### 5.x [目標主機/服務]（SSH / API）

| 步驟 | 指令/操作 | 對應 BR |
|------|-----------|--------|
| [步驟] | [具體指令] | BR-xx |

**回滾**：[回滾指令]

---

## 6. 設定檔模板

### 6.x [模板名稱]

位置：`src/templates/[檔名].tpl`
變數：`{{VAR1}}`、`{{VAR2}}`

---

## 7. 環境變數依賴（`.env`）

| 變數 | 用途 | 範例 |
|------|------|------|
| `VAR` | [用途] | `value` |

---

## 8. Testing Criteria

### 腳本單元測試
- [ ] [模組] - [測試案例]

### 整合測試（需遠端環境）
- [ ] [完整流程測試案例]

### 手動測試
- [ ] [手動驗證項目]

---

## 9. Implementation Notes

### 開發重點
- [重點]

### 技術挑戰
- [挑戰]

### 相依性
- [ ] [外部依賴：如已安裝的工具、SSH key、API Token]
- [ ] 依賴 Story：[Story ID]（若有）
```

---

## 🎯 DDD 分析方法（僅 Web App 型使用）

> **CLI / 腳本型不需要 DDD 分析**，直接在 spec.md 中描述架構和模組即可。

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

## 🔧 CLI / 腳本型分析方法

> **Web App 型不需要此分析**，使用上方 DDD 分析。

### 步驟 1：識別指令介面
- 問：「使用者（或 AI Agent）要執行什麼 make 指令？」
- 每個 UC 通常對應一個 `make` target
- 列出所有參數（必填/選填/預設值）

### 步驟 2：識別腳本模組
- 問：「主腳本可以拆成哪些獨立的函式/模組？」
- 原則：一個模組負責一件事（如 DNS 操作、DB 操作、回滾）
- 共用邏輯抽到 `lib/` 目錄

### 步驟 3：識別遠端操作
- 問：「需要 SSH 到哪些主機？需要呼叫哪些 API？」
- 每個遠端操作列出：目標、指令、回滾指令
- 設計錯誤傳播機制（SSH exit code → 回滾觸發）

### 步驟 4：識別設定檔模板
- 問：「哪些設定檔需要根據參數產生？」
- 模板使用 `{{VARIABLE}}` 佔位符
- 模板放在 `src/templates/`

### 步驟 5：設計輸出格式
- 問：「使用者或 AI Agent 如何知道操作成功/失敗？」
- 成功：結構化摘要（key-value 格式，方便 AI 解讀）
- 失敗：明確的錯誤訊息 + exit code 非 0
- Log：每步驟記錄，含時間戳和 level

---

## ✅ spec.md 完整性檢查

### Web App 型檢查

產生 `spec.md` 後，AI 應自動檢查：

- [ ] 路由前綴、Controller 目錄、DB 表名稱是否使用同一個英文單字（複數）？
- [ ] Controller 類別名稱是否為「路由單字複數 + Controller」？
- [ ] Model 類別名稱是否為路由單字的單數形？
- [ ] 若有不一致，必須在規劃階段就修正，不可留到開發階段才發現

### CLI / 腳本型檢查

產生 `spec.md` 後，AI 應自動檢查：

- [ ] 每個 Makefile target 都有完整的參數說明（必填/選填/預設值/範例）？
- [ ] 輸出格式是否結構化、方便 AI Agent 解讀？
- [ ] 腳本模組分工是否清晰（一個模組一件事）？
- [ ] 每個遠端操作都有對應的回滾指令？
- [ ] 所有環境變數依賴都已列出？
- [ ] 設定檔模板的變數是否都有說明？

---

## 🔍 需求不清楚時的處理原則

規劃過程中遇到需求不明確、需要使用者決策的情況，**必須執行 `/discussion` workflow**，不可自行假設或猜測答案。

觸發時機：
- Actor 或操作範圍不確定
- 有多個設計方案需要使用者選擇
- 業務規則有歧義
- backlog 的「待補充資訊」尚未確認

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
描述端對端測試流程。根據專案類型不同：
- **Web App**：描述瀏覽器操作流程，供 Playwright 測試使用
- **CLI / 腳本**：描述終端機指令執行與驗證流程

### 劇本來源對應

| 劇本類型 | 來源 | 說明 |
|----------|------|------|
| 正向劇本 | `use-cases.md` 主要流程 | 每個 UC 至少一個 happy path |
| 替代劇本 | `use-cases.md` 替代流程 | 有替代流程時產生 |
| 負向劇本 | `use-cases.md` 例外流程 + `business-rules.md` | 錯誤輸入、業務規則違反 |

### 劇本格式（Web App 型）
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

### 劇本格式（CLI / 腳本型）
```markdown
### S-{序號}：[劇本標題]

| 欄位 | 內容 |
|------|------|
| **對應 UC / BR** | UC-01 / BR-01 |
| **Actor** | [角色] |
| **前置條件** | [測試開始前的系統/環境狀態] |

**操作步驟：**
1. 執行 `make [指令] param1=value1`
2. 等待執行完成

**預期結果：**
- 終端輸出包含 `[預期文字]`
- exit code 為 `[0 或非 0]`
- [檔案/遠端狀態驗證，如：SSH 指令確認資源已建立]
- [JSON 檔案內容驗證]
```

### 劇本命名規則
- 正向劇本：`S-01`、`S-02`...
- 負向劇本：`S-E01`、`S-E02`...
- 安全性劇本：`S-SEC01`、`S-SEC02`...（CLI 型可選）
- 清理劇本：`S-CLEANUP`（CLI 型建議加入）

### 操作步驟撰寫原則

**Web App 型：**
- 每個步驟要具體、可執行（「點擊 id=submit 的按鈕」優於「點擊送出」）
- 輸入值要明確（「輸入 `test@example.com`」優於「輸入 email」）
- URL 使用 `spec.md` 路由表格中的實際路徑

**CLI / 腳本型：**
- 指令要完整可複製執行（含所有參數）
- 驗證步驟要包含具體的 SSH 指令或 API 呼叫
- 測試用的 domain/參數加上 `test-e2e-` 前綴，方便事後清理

### 預期結果撰寫原則
- 必須是可程式驗證的
- **Web App**：URL、DOM 元素、文字內容
- **CLI**：終端輸出文字、exit code、檔案存在與內容、遠端狀態（SSH 指令回傳值）
- 避免主觀描述（「看起來正確」→ 改為具體的驗證條件）

## ✅ E2E 劇本完整性檢查

產生 `e2e-scenarios.md` 後，AI 應自動檢查：

- [ ] 每個 UC 都有至少一個正向劇本？
- [ ] 每個例外流程都有對應的負向劇本？
- [ ] 每條業務規則（BR）都有對應的邊界值劇本？
- [ ] 每個劇本的預期結果都是可程式驗證的？
- [ ] **Web App**：所有 URL 都來自 `spec.md` 的路由表格？
- [ ] **CLI**：所有指令都來自 `spec.md` 的 Makefile 指令介面？
- [ ] **CLI**：是否有清理劇本（清除測試資源）？
