---
name: tasq-api-agent
description: 教 AI Agent 如何透過 Tasq API 管理任務。涵蓋認證、核心工作流程（建任務、拆步驟、記錄進度、標記完成）、搜尋、Dashboard，以及常見錯誤處理。
---

# Tasq API Agent Skill

你是一個使用 Tasq 個人任務管理系統的 AI Agent。本文件涵蓋基本設定與核心工作流程。

詳細參考資料：
- `ref-endpoints-tasks-steps.md` — Tasks / Steps 端點
- `ref-endpoints-logs-search-misc.md` — Logs / Search / Dashboard / Retrospective / Templates
- `ref-fields-errors.md` — 欄位速查、錯誤碼、操作建議

---

## 基本設定

### API Base URL
```
https://tasq.dev2.quanhox.com.tw/api
```
> 本機開發環境：`http://127.0.0.1:8344`

### 認證
所有請求需帶 `X-API-Key` header。

**Claude Code 兄弟（.env）：**
```bash
# .env 裡有這兩個變數
TASQ_BASE_URL=https://tasq.dev2.quanhox.com.tw/api
TASQ_API_KEY=<your-key>

# 使用前載入
set -a; source .env; set +a
```

**Hermes profile（credential file）：**
```
credential file: tasq-api.json
field: credential
header to use: X-API-Key
```

### Workspace
每個請求都需指定 workspace（資料隔離單位）。預設 workspace 為 `personal`。
- Query string：`?workspace=personal`
- Request body：`"workspace": "personal"`

### 互動式文件
```
https://tasq.dev2.quanhox.com.tw/api/docs
```

---

## ⭐ 4 段 Pipeline — 艦隊核心 operating model（先讀這段）

**接到任何工作，不要 inline 執行。走這 4 段 pipeline：**

```
[外部進來] → 1. Intake → 2. Triage → 3. Plan with history → 4. Execute → [外部回報]
              寫進 TASQ    從 TASQ    搜過去類似任務        按 step
              不丟失       撈活       撿步驟改用            機械執行
```

### 為什麼這樣設計

- **規劃貴、執行便宜**：規劃要強模型 + 上下文 + 思考；執行可機械化。分離後**只有規劃需要強模型**，執行可丟給 Haiku / 本地模型。
- **步驟複用**：今天的 plan 變明天的 template；vector + FTS 搜尋讓步驟自動 emergent 出來。
- **任務不丟失**：daemon 重啟也記得待辦。

### 1. Intake — 進來就寫 TASQ

接到 hub thread / 人類請求 / cron / webhook：

```
POST /tasks
{
  "workspace": "<your_ws>",
  "title": "<關鍵動詞 + 對象 + 範圍>"
}
```

⚠️ **命名紀律最重要**——標題要讓未來搜得到：
- ✅ "推 agenthub-client skill 到 hermes 兄弟"
- ❌ "處理 skill"
- ✅ "查 isofh.org SSL 憑證到期日 + 規劃續簽流程"
- ❌ "SSL 的事"

標題要含關鍵字（動詞、對象、目的），否則 FTS / vector 搜不到 → pipeline 第 3 段就失效。

### 2. Triage — 從 TASQ 撈活

不從 hub 即時被動拉。Daemon 應該：

```
GET /steps/today?workspace=X      → 今天該做的
GET /tasks?workspace=X&status=active → 所有 active
```

從待辦池決定下一個處理哪個（依優先序 / 截止 / 上下文）。Hub inbox 只是 intake 來源，不是執行 queue。

### 3. Plan with history — 開工前先搜（最關鍵的一段）

決定動手之前，**先搜過去類似任務**：

```bash
curl -X POST "$TASQ_BASE_URL/search" \
  -H "X-API-Key: $TASQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace": "<your_ws>",
    "query": "<簡短描述本次任務>",
    "limit": 5
  }'
```

搜到類似任務 →
1. `GET /tasks/{old_id}` 抓它的 `steps` 陣列
2. 把那組 steps 拿來**改一改套到新任務**：

```
POST /tasks/{new_id}/steps  (對每個步驟逐筆送，⚠️一次一個不能 batch)
{
  "workspace": "<your_ws>",
  "title": "<step 內容>"
}
```

搜不到才從頭拆。**這條讓「規劃成本」攤平到無限次未來執行**。

⭐ **撿到舊步驟必標來源**：套用舊任務的 step 時，在新 task 的 `workspace_notes` 或第一條 log 寫 `Reused steps from <task_no>`（多個就列多筆）。沒撿就不標。**這是 search 命中率唯一可量化的訊號**——沒有這條紀律，3 個月驗收時無從判斷 Plan 階段到底有沒有真做 search。

### 4. Execute — 機械按 step 走

對每個 step 順序執行：

```
PATCH /steps/{id}  {"workspace": "...", "status": "in_progress"}
... [做事] ...
POST /tasks/{id}/logs  {"workspace": "...", "content": "<決策/指令/坑>"}
PATCH /steps/{id}  {"workspace": "...", "status": "done"}
```

**卡住的鐵則**：
- 不要 inline 亂改 step 內容
- 不要硬猜
- 卡住時先分清是 `waiting`（等預期的事）還是 `blocked`（碰到不該發生的錯）——見下節「卡住時：waiting 還是 blocked？」；log 卡住原因、回 hub thread 問人（或 plan 階段的強模型 review）

最後：

```
PATCH /tasks/{id}  {"workspace": "...", "status": "completed"}
```

---

## ⭐ 卡住時：waiting 還是 blocked？（Story 22）

step / task 卡住時不要只設 `blocked` 了事——這兩態語義不同、後端處理不同：

> **等一件預期會發生的事 → `waiting`（不告警）；碰到不該發生的錯 → `blocked`（會告警）。**

- `waiting`：等問卷 / 等授權 / 等別的 task / 等外部配額 / 等時間。設 `waiting_on_type` + `waiting_reason`（+ `waiting_on_id` / `due_date`）。**設完 step waiting 後 task 保持 active，繼續推進其他無依賴的 step。**
- `blocked`：程式拋例外、依賴掛了、外部一直回錯。設 `blocked_reason`（+ `error_class`）。會告警、不自動恢復。
- **由 agent 自己 `PATCH /steps/{id}` 標，系統不自動判斷。**

完整 enum 值、欄位與判斷範例見 `ref-fields-errors.md` 的「waiting vs blocked」一節。

---

## ⭐ PDCA — 任務生命週期紀律（套在 4-pipeline Execute 內外）

4-pipeline 解了 Plan / Do，但**沒解** Check / Act——做完不寫 retrospective、學到的東西不回饋系統。下次 search 撈到的只是事實流水，不是「我學到什麼」。PDCA 補這兩層。

```
Plan  → 搜過去 + 拆 step      （4-pipeline 第 3 段）
Do    → 逐 step 執行 + log    （4-pipeline 第 4 段）
Check → 寫 retrospective      ⭐ 新加
Act   → 回饋到 skill/memory   ⭐ 新加
```

### 📝 鐵則：寫給「從沒碰過這任務的陌生 agent」看（老闆 2026-05-13 原話）

`workspace_notes` / `steps` / `logs` / `retrospective` 不是事後報告，是**即時交接文件**：
- 對話裡產生的設計決策**當下就 dump 到 workspace_notes**（不要等 session 結束，對話會消失，TASQ 不會）
- log 要讓陌生 agent 讀完能接著做——寫**決策 / 指令 / 卡的點 / 對話補充**，不只是「我做了 X」
- step title 是動作句（「查 isofh.org SSL 到期日」），未來搜出來能直接複用

### C — Check（寫 retrospective）

結案前必寫，沒有「太小不用寫」這種事。

```bash
curl -X POST "$TASQ_BASE_URL/tasks/{id}/retrospective" \
  -H "X-API-Key: $TASQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace": "<your_ws>",
    "summary": "<3-5 行，這次交付了什麼，給 90 天後的自己看>",
    "lessons_learned": "<新知 / 踩到的坑 / 下次該做不一樣的事>"
  }'
```

`lessons_learned` 空白比硬寫廢話可怕——下次 search 命中後就少一條警示。小任務也至少寫一行 summary。

### A — Act（回饋系統）

把學到的東西寫回**系統能讀到的地方**，不是只留在這 task 裡。5 個落點（看「下次誰要用」決定）：

| 落點 | 適用 |
|---|---|
| skill 更新（`~/.claude/skills/...`） | 跨任務通用 SOP / 踩雷修正 |
| memory（`~/.claude/projects/.../memory/`） | 個人視角 / feedback / 偏好 / 跨 session 脈絡 |
| `workspace_notes`（task 本身） | 「這個 task 的設計決策」 |
| 新 task / step | 衍生待辦 |
| `HANDOFF.md` | 跨 session 短期備忘 |

**強制 ≥ 1 落點**——結案前自問「這次學到的東西寫去哪了？」沒落點 → 補一個再 close。

然後才：`PATCH /tasks/{id} {"status": "completed"}`。

### 為什麼 PDCA 是複利來源

跳過 Check / Act = 把學費丟掉。今天的 retrospective + skill 更新，是下次 Plan 階段 search 命中後直接撿得到的素材。詳細設計見 TASQ task `T260513-0957`。

---

## 核心 API 工作流程速查

### 流程 A：建立新任務並開始執行（4-stage pipeline 落地版）

```
1. POST /tasks              → Intake：建任務，取得 task_id / task_no
2. POST /search             → Plan: 找類似舊任務 (recommended)
3. POST /tasks/{id}/steps   → 拆步驟（⚠️一次一個，不能 batch；舊版 SKILL 寫「可 batch」是錯的）
4. PATCH /steps/{id}        → 開始某步驟（status: in_progress）
5. POST /tasks/{id}/logs    → 記錄進度
6. PATCH /steps/{id}        → 完成步驟（status: done）
7. PATCH /tasks/{id}        → 完成任務（status: completed）
```

### 流程 B：查看今日待辦並執行（Triage + Execute）

```
1. GET /steps/today?workspace=X        → 今日待辦步驟（due_date <= today）
2. GET /steps/followup-due?workspace=X → 需追蹤的委派步驟
3. PATCH /steps/{id}                   → 更新步驟狀態
4. POST /tasks/{id}/logs               → 記錄工作紀錄
```

### 流程 C：查找任務（Plan 階段必用）

```
1. POST /search                           → FTS + vector 混合搜尋（RRF）
2. GET /tasks?workspace=X                 → 列出所有任務
3. GET /tasks/by-no/{task_no}?workspace=X → 以 task_no 取得詳情
```
