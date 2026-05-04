---
name: tasq-api-agent
description: 教 AI Agent 如何透過 Tasq API 管理任務。涵蓋認證、核心工作流程（建任務、拆步驟、記錄進度、標記完成）、搜尋、Dashboard，以及常見錯誤處理。
---

# Tasq API Agent Skill

你是一個使用 Tasq 個人任務管理系統的 AI Agent。本文件教你如何透過 REST API 操作任務。

---

## 1. 基本設定

### API Base URL
```
https://tasq.dev2.quanhox.com.tw/api
```
> 若在本機開發環境：`http://127.0.0.1:8344`

### 認證
所有請求需帶 `X-API-Key` header：
```
X-API-Key: {你的 api_key}
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

## 2. 核心工作流程

### 流程 A：建立新任務並開始執行

```
1. POST /tasks          → 建立任務，取得 task_id / task_no
2. POST /tasks/{id}/steps   → 拆分步驟（可 batch）
3. PATCH /steps/{id}    → 開始某步驟（status: in_progress）
4. POST /tasks/{id}/logs    → 記錄進度
5. PATCH /steps/{id}    → 完成步驟（status: done）
6. PATCH /tasks/{id}    → 完成任務（status: completed）
```

### 流程 B：查看今日待辦並執行

```
1. GET /steps/today?workspace=X     → 今日待辦步驟（due_date <= today）
2. GET /steps/followup-due?workspace=X → 需追蹤的委派步驟
3. PATCH /steps/{id}               → 更新步驟狀態
4. POST /tasks/{id}/logs           → 記錄工作紀錄
```

### 流程 C：查找任務

```
1. POST /search                    → 關鍵字搜尋（FTS + vector）
2. GET /tasks?workspace=X          → 列出所有任務
3. GET /tasks/by-no/{task_no}?workspace=X → 以 task_no 取得詳情
```

---

## 3. API 端點參考

### 任務（Tasks）

#### 建立任務
```http
POST /tasks
Content-Type: application/json
X-API-Key: {key}

{
  "workspace": "personal",
  "title": "整理 Q2 客戶回饋報告",
  "priority_tags": ["urgent"],
  "special_tags": []
}
```
回傳：`{ "id": 42, "task_no": "T260504-1430", "title": "...", "status": "active", ... }`

#### 列出任務
```http
GET /tasks?workspace=personal
X-API-Key: {key}
```

#### 取得任務詳情（含 steps / logs / retrospective）
```http
GET /tasks/by-no/T260504-1430?workspace=personal
GET /tasks/42?workspace=personal
```

#### 更新任務
```http
PATCH /tasks/42
Content-Type: application/json

{
  "status": "completed",
  "completed_at": "2026-05-04T18:00:00"
}
```
`status` 可選值：`active` | `completed` | `cancelled` | `on_hold`

---

### 步驟（Steps）

#### 建立步驟
```http
POST /tasks/42/steps
Content-Type: application/json

{
  "title": "整理原始問卷資料",
  "due_date": "2026-05-06",
  "estimated_minutes": 60
}
```

#### 批次建立步驟
```http
POST /tasks/42/steps/batch
Content-Type: application/json

{
  "steps": [
    { "title": "整理問卷", "sort_order": 1 },
    { "title": "分析趨勢", "sort_order": 2, "depends_on": [] },
    { "title": "撰寫報告", "sort_order": 3 }
  ]
}
```

#### 更新步驟狀態
```http
PATCH /steps/101
Content-Type: application/json

{
  "status": "done",
  "actual_minutes": 45,
  "completed_at": "2026-05-04T15:30:00"
}
```
`status` 可選值：`pending` | `in_progress` | `done` | `delegated` | `blocked`

**委派步驟**（需要追蹤）：
```json
{
  "status": "delegated",
  "assignee": "小明",
  "next_followup_date": "2026-05-07"
}
```

#### 查看今日待辦
```http
GET /steps/today?workspace=personal
```
回傳 status 為 pending/in_progress/blocked 且 due_date <= 今日的步驟，含 `task_no` / `task_title`。

#### 查看待追蹤委派
```http
GET /steps/followup-due?workspace=personal
```
回傳 status=delegated 且 next_followup_date <= 今日的步驟。

---

### 工作記錄（Logs）

#### 新增記錄
```http
POST /tasks/42/logs
Content-Type: application/json

{
  "content": "完成問卷整理，共 87 份，其中 23 份有具體改善建議",
  "step_id": 101
}
```
`step_id` 可選（不填表示任務層級的記錄）。

#### 查看最近記錄
```http
GET /logs/recent?workspace=personal&limit=10
```

---

### 搜尋（Search）

#### 混合搜尋（FTS + Vector）
```http
POST /search
Content-Type: application/json

{
  "workspace": "personal",
  "query": "客戶回饋",
  "scope": ["tasks", "logs"],
  "limit": 20,
  "offset": 0
}
```

`scope` 可選：`["tasks"]` / `["logs"]` / `["tasks", "logs"]`

回傳：
```json
{
  "results": [
    {
      "type": "task",
      "task_no": "T260504-1430",
      "title": "整理 Q2 客戶回饋報告",
      "score": 0.032,
      "matched_via": ["fts", "vector"]
    },
    {
      "type": "log",
      "task_no": "T260504-1430",
      "task_title": "整理 Q2 客戶回饋報告",
      "log_id": 55,
      "content": "完成問卷整理...",
      "score": 0.018,
      "matched_via": ["fts"]
    }
  ]
}
```

---

### Dashboard 摘要

```http
GET /dashboard/summary?workspace=personal
```
回傳：
```json
{
  "active_count": 5,
  "completed_count": 23,
  "today_completed_count": 2,
  "followup_due_count": 1
}
```

---

### 回顧（Retrospective）

```http
POST /tasks/42/retrospective
Content-Type: application/json

{
  "what_went_well": "資料整理流程順暢",
  "what_to_improve": "下次需要更早聯絡客戶",
  "next_actions": "建立標準問卷模板"
}
```

---

### 模板（Templates）

```http
# 列出模板
GET /templates?workspace=personal

# 建立模板
POST /templates
{
  "workspace": "personal",
  "name": "週報流程",
  "steps": [
    { "title": "收集本週數據", "sort_order": 1 },
    { "title": "撰寫摘要", "sort_order": 2 },
    { "title": "發送給主管", "sort_order": 3 }
  ]
}

# 使用模板（從模板建立任務）— 需自行 GET template 後 POST tasks + steps/batch
```

---

## 4. 欄位速查

### Task status
| 值 | 意義 |
|----|------|
| `active` | 進行中（預設） |
| `completed` | 已完成 |
| `cancelled` | 已取消 |
| `on_hold` | 暫停 |

### Step status
| 值 | 意義 |
|----|------|
| `pending` | 待處理（預設） |
| `in_progress` | 執行中 |
| `done` | 已完成 |
| `delegated` | 已委派他人，需追蹤 |
| `blocked` | 被阻擋，無法進行 |

### priority_tags（建議值）
`urgent`、`important`、`low`（自由填寫，無強制格式）

### special_tags（建議值）
`delegated`、`waiting`、`someday`、`reference`

---

## 5. 常見錯誤與處理

| HTTP | 錯誤碼 | 意義 | 處理方式 |
|------|--------|------|---------|
| 401 | `missing_api_key` | 未帶 X-API-Key | 檢查 header |
| 401 | `invalid_api_key` | Key 錯誤或無此 workspace | 確認 key 正確 |
| 403 | — | workspace 無存取權 | 確認 workspace 與 key 對應 |
| 404 | `task_not_found` | 任務不存在 | 確認 task_no / id |
| 422 | — | 欄位格式錯誤 | 檢查 request body |

---

## 6. 操作建議

**開始工作前**：
```
GET /steps/today → 看今日待辦
GET /steps/followup-due → 看需要追蹤的委派
GET /dashboard/summary → 看整體狀況
```

**找任務時**：優先用 `POST /search`（語意搜尋比 list + filter 更準）

**步驟粒度**：單一步驟預期 15-120 分鐘可完成；太大請再拆

**記錄頻率**：完成每個步驟後立即 log，不要累積

**task_no vs task_id**：
- `task_no`（如 `T260504-1430`）是人類識別碼，在 URL 和對話中使用
- `task_id`（整數）是 DB 主鍵，只在 API response 中使用，不需要記憶
