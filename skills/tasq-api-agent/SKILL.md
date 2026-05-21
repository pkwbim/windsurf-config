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
所有請求需帶 `X-API-Key` header。API Key 存放於 credential：

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

## 核心工作流程

### 流程 A：建立新任務並開始執行

```
1. POST /tasks              → 建立任務，取得 task_id / task_no
2. POST /tasks/{id}/steps   → 拆分步驟（可 batch）
3. PATCH /steps/{id}        → 開始某步驟（status: in_progress）
4. POST /tasks/{id}/logs    → 記錄進度
5. PATCH /steps/{id}        → 完成步驟（status: done）
6. PATCH /tasks/{id}        → 完成任務（status: completed）
```

### 流程 B：查看今日待辦並執行

```
1. GET /steps/today?workspace=X        → 今日待辦步驟（due_date <= today）
2. GET /steps/followup-due?workspace=X → 需追蹤的委派步驟
3. PATCH /steps/{id}                   → 更新步驟狀態
4. POST /tasks/{id}/logs               → 記錄工作紀錄
```

### 流程 C：查找任務

```
1. POST /search                           → 關鍵字搜尋（FTS + vector）
2. GET /tasks?workspace=X                 → 列出所有任務
3. GET /tasks/by-no/{task_no}?workspace=X → 以 task_no 取得詳情
```

---

## ⭐ 卡住時：waiting 還是 blocked？（Story 22）

step / task 卡住時不要只設 `blocked` 了事——這兩態語義不同、後端處理不同：

> **等一件預期會發生的事 → `waiting`（不告警）；碰到不該發生的錯 → `blocked`（會告警）。**

- `waiting`：等問卷 / 等授權 / 等別的 task / 等外部配額 / 等時間。設 `waiting_on_type` + `waiting_reason`（+ `waiting_on_id` / `due_date`）。**設完 step waiting 後 task 保持 active，繼續推進其他無依賴的 step。**
- `blocked`：程式拋例外、依賴掛了、外部一直回錯。設 `blocked_reason`（+ `error_class`）。會告警、不自動恢復。
- **由 agent 自己 `PATCH /steps/{id}` 標，系統不自動判斷。**

完整 enum 值、欄位與判斷範例見 `ref-fields-errors.md` 的「waiting vs blocked」一節。
