---
description: 將想法轉換為規格（包含澄清檢查）
---

## ⚠️ 重要：此工作流程僅撰寫規格。不要開始寫程式。

## 🎯 DDD 規劃原則
本專案採用 Domain-Driven Design，規劃時需考慮：
- **領域實體 (Entity)**: 具有唯一識別的業務物件 → `backend/app/domain/entities/`
- **值物件 (Value Object)**: 無識別的不可變物件
- **用例 (Use Case)**: 應用層的業務操作 → `backend/app/domain/use_cases/`
- **服務介面 (Protocol)**: 定義契約 → `shared_contracts/interfaces/`
- **DTO**: 資料傳輸物件 → `shared_contracts/dto/`

0. Git Branch Setup
   // turbo
   ```bash
   git branch --show-current
   ```
   - 如果目前在 `main`：建立並切換到 `feat/<story-id>` 分支（例如 `feat/story-003`）
   - 如果已在 feature 分支：沿用現有分支
   - 目的：讓規格與後續實作都在同一個分支上

1. 讀取待辦清單、範本和技術堆疊
   // turbo
   ```bash
   cat _planning/01_backlog.md
   cat .windsurf/templates/story.md
   cat docs/TECH_STACK.md
   ```

2. 與使用者確認故事選擇
   - 提問：「您想要規劃 Story-XXX，對嗎？」
   - 等待使用者確認後再繼續。

3. 分析需求（強制澄清檢查）
   - 仔細審查使用者故事。
   - **問自己：**範圍是否 100% 清楚？我確切知道要建構什麼嗎？
   - **如有任何疑問：**在 `discussions/YYYYMMDD-StoryXXX-Clarification.md` 建立討論檔案並**停止**。
   - **如果清楚：**繼續下一步。

4. 初始化任務中
   // turbo
   ```bash
   # 將選擇的故事從 01_backlog.md 移至 02_active.md（使用者故事區段）
   # 套用 .windsurf/templates/story.md 結構
   ```

5. 在 `02_active.md` 撰寫技術規格（DDD 導向）
   用詳細規格填寫範本，並加入 DDD 分析：
   
   ### 5.1 領域分析（Domain Analysis）
   - **識別 Bounded Context**: 此功能屬於哪個領域邊界？
   - **識別 Aggregate Root**: 主要的聚合根是什麼？
   - **領域語言 (Ubiquitous Language)**: 定義此功能的核心術語
   
   ### 5.2 領域設計（Domain Design）
   - **新增/修改 Entity**: `backend/app/domain/entities/`
     - 實體名稱、屬性、業務方法
   - **新增/修改 Use Case**: `backend/app/domain/use_cases/`
     - 用例名稱、輸入輸出、業務規則
   - **新增/修改 Protocol**: `shared_contracts/interfaces/`
     - 服務介面定義
   - **新增/修改 DTO**: `shared_contracts/dto/`
     - 資料傳輸物件
   
   ### 5.3 基礎設施層（Infrastructure）
   - **Repository 實作**: `backend/app/domain/repositories/`
   - **資料庫 Model**: `backend/app/models/`
   - **API 端點**: `backend/app/api/`
   
   ### 5.4 其他規格
   - 1. 使用者故事（來源）
   - 2. 技術需求（UI、DB Migration）
   - 3. 測試準則（強制）
   - 4. 文件

6. **AI 自動檢查範圍完整性（含 DDD 檢查）**
   
   **檢查清單（AI 自己檢查並報告）：**
   
   **DDD 架構檢查：**
   - **領域邊界**：是否清楚定義 Bounded Context？
   - **Entity 設計**：業務邏輯是否封裝在 Entity 中？
   - **Use Case 識別**：是否列出所有應用層用例？
   - **Protocol 定義**：服務介面是否定義清楚？
   - **DTO 設計**：跨層資料傳輸是否使用 DTO？
   
   **功能完整性檢查：**
   - **CRUD 完整性**：檢查是否包含所有增刪改查操作
   - **頁面/元件**：檢查 UI 規劃是否完整
   - **資料庫設計**：檢查欄位、關聯、索引是否考慮完整
   - **API 端點**：檢查所有需要的 API 是否列出
   - **使用者流程**：檢查從進入到離開的完整流程
   - **邊界情況**：檢查錯誤處理、權限檢查
   - **Migration 需求**：判斷是否需要資料庫 Migration
   
   **AI 輸出檢查結果：**
   ```markdown
   ## 範圍檢查結果
   
   ### DDD 架構
   ✅ 領域邊界：[已定義 XXX Context]
   ✅ Entity 設計：[XXXEntity 包含業務邏輯]
   ⚠️ Use Case：[缺少 XXX 用例]
   ✅ Protocol：[已定義 XXXProtocol]
   ✅ DTO：[已設計 XXXCreate, XXXResponse]
   
   ### 功能完整性
   ✅ CRUD 完整性：[已包含 Create, Read, Update, Delete]
   ⚠️ 頁面/元件：[缺少 XXX 頁面]
   ✅ 資料庫設計：[已考慮所有欄位]
   ...
   
   ### 發現的潛在遺漏
   1. [遺漏項目 1] - 建議：[立即加入 / 加入 backlog]
   2. [遺漏項目 2] - 建議：[立即加入 / 加入 backlog]
   ```
   
   **詢問使用者：**
   「我檢查了規格，發現以上潛在遺漏。是否需要調整？」
   - 如需調整核心功能：更新 `02_active.md`
   - 如是非核心功能：記錄到 `01_backlog.md`
   - 不確定時：執行 `/scope` 協助判斷

7. **在此停止**
   - 告訴使用者：「規格已在 `02_active.md` 中準備就緒。當您想開始實作時，執行 `/build`。」
   - **不要撰寫任何程式碼。**

## 備註
- 必須使用 `.windsurf/templates/story.md` 作為結構
- 保持 `02_active.md` 乾淨，只有一個任務中
- 技術規格應足夠詳細以供實作
- **此工作流程在規格撰寫結束。實作是另一個工作流程（`/build`）。**

## 測試規劃最佳實踐

### ⚠️ Mock 陷阱警告
在規劃測試時，注意 **vi.mock() 會完全替換模組**，可能導致以下問題無法被測試捕捉：

1. **導入路徑錯誤**：當測試 mock 了某個模組，即使實際組件的導入路徑有誤，測試仍會通過
2. **測試環境 vs 開發環境差異**：Vitest 和 Vite dev server 的模組解析行為可能不同

### ✅ 建議的測試策略

#### 1. 導入驗證測試（必要）
每個新組件都應包含導入驗證測試，確保組件能正確載入：
```javascript
it('should validate Component imports work correctly', async () => {
  const Component = await import('@/path/to/Component.vue')
  expect(Component.default).toBeDefined()
})
```

#### 2. 測試分層
- **單元測試**：測試單一函數或組件邏輯（使用 mock）
- **導入驗證測試**：確保模組路徑正確（不使用 mock）
- **整合測試**：測試多個組件協作（部分 mock）

#### 3. 測試準則模板
在 `02_active.md` 的測試準則中，應包含：
```markdown
## 3. Testing Criteria (Mandatory)
- [ ] **Backend Unit Test:** [Service 層測試]
- [ ] **Backend Integration Test:** [API 端點測試]
- [ ] **Frontend Import Test:** [驗證組件導入正確]
- [ ] **Manual Testing:** [人工驗證項目]
```