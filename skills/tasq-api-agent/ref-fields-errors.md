# Tasq API — 欄位速查、錯誤碼、操作建議

## 欄位速查

### Task status
| 值 | 意義 |
|----|------|
| `active` | 進行中（預設） |
| `completed` | 已完成 |
| `cancelled` | 已取消 |
| `on_hold` | 暫停 |

### Step status（7 態）
| 值 | 意義 |
|----|------|
| `pending` | 待處理（預設） |
| `in_progress` | 執行中 |
| `waiting` | **預期內暫停，不告警**——等一件預期會發生的事（見下方語義） |
| `blocked` | **非預期 error，要告警**——碰到不該發生的錯（見下方語義） |
| `done` | 已完成 |
| `delegated` | 已委派他人，需追蹤 |
| `cancelled` | 已取消 |

> ⚠️ `waiting` 與 `blocked` 是**刻意分開**的兩態，語義不同、後端處理也不同。誤用會讓正常的等待觸發假警報（或讓真的卡住被當成正常等待沒人管）。動手標之前務必讀下一節。

---

## ⭐ waiting vs blocked — step 狀態語義（Story 22）

**一句話判斷準則：**
> **等一件預期會發生的事 → `waiting`；碰到不該發生的錯 → `blocked`。**

後端對兩者的處理不同：
- `waiting` = 預期內暫停，**不告警**。waiting-monitor 在條件滿足 / 到期後可協助恢復。
- `blocked` = 非預期錯誤，**會告警**、不自動恢復，需要有人來看。

**誰來標**：由你（agent）自己 `PATCH /steps/{id}` 設定，**系統不會自動判斷**。你最清楚當下是「在等」還是「壞了」。

### `waiting`（預期暫停，不告警）

```bash
PATCH /steps/{id}
{
  "workspace": "task-agent-api",
  "status": "waiting",
  "waiting_on_type": "hub_questionnaire",   # 在等什麼類別（enum，見下）
  "waiting_on_id": "<post_id / thread_id / task_no>",  # 不透明參照，可選
  "waiting_reason": "等老闆在問卷拍板部署策略",  # 人類可讀原因
  "due_date": "2026-05-23T00:00:00Z"        # SLA / 預期恢復時點，建議帶
}
```

`waiting_on_type` 允許值（`WaitingOnTypeLiteral`）：

| 值 | 在等什麼 |
|----|---------|
| `hub_thread` | 等某 hub thread 有人回 |
| `hub_questionnaire` | 等某問卷被回答 |
| `human_approval` | 等人類授權 / 拍板 |
| `external` | 等外部資源（API 配額、第三方、別的系統） |
| `task` | 等另一個 TASQ task 先完成（`waiting_on_id` 放 task_no） |
| `time` | 等到某個時間點（排程、冷卻） |

> 設了 step `waiting` 後，**task 本身保持 active**，繼續推進其他沒有依賴的 step（並行），不要把整個 task 宣告卡住。

### `blocked`（非預期 error，要告警）

```bash
PATCH /steps/{id}
{
  "workspace": "task-agent-api",
  "status": "blocked",
  "blocked_reason": "deploy.sh 第 3 步拋 PermissionError，sudo 壞掉",  # 必填，講清楚錯在哪
  "error_class": "exception"                # 錯誤分類（enum，可選）
}
```

`error_class` 允許值（`ErrorClassLiteral`）：

| 值 | 意義 |
|----|------|
| `exception` | 程式拋例外 |
| `timeout` | 逾時 |
| `dependency_failed` | 依賴的東西失敗了（不是「還在等」，是「等的對象掛了」） |
| `external_error` | 外部服務回錯（如一直 500） |
| `unknown` | 分不出來 |

### 判斷範例

| 情境 | 標哪個 | 怎麼填 |
|------|--------|--------|
| 等老闆在問卷回覆才能繼續 | `waiting` | `waiting_on_type=hub_questionnaire`, `waiting_on_id=<post_id>`, `waiting_reason="等拍板"` |
| 這步要等另一個 task 先做完 | `waiting` | `waiting_on_type=task`, `waiting_on_id=<task_no>` |
| 撞到 API 每日配額，明天才恢復 | `waiting` | `waiting_on_type=external`（或 `time`）, `due_date=明天` |
| 部署腳本拋例外、sudo 壞掉 | `blocked` | `error_class=exception`, `blocked_reason="..."` |
| 依賴的服務一直回 500 | `blocked` | `error_class=external_error`, `blocked_reason="..."` |

**容易混的點**：「等外部 API 配額」是 `waiting`（預期會恢復）；「外部 API 一直回錯」是 `blocked`（不該發生）。同樣對著外部，差在「預期會好」還是「壞了」。

> 對應 task 層：task 也有 `waiting`（搭 `waiting_reason` / `waiting_for_task_no` / `resume_at`）與 `blocked`（搭 `blocked_reason` / `error_class`）。step 層語義同此節。

---

### priority_tags（建議值）
`urgent`、`important`、`low`（自由填寫，無強制格式）

### special_tags（建議值）
`delegated`、`waiting`、`someday`、`reference`

---

## 常見錯誤與處理

| HTTP | 錯誤碼 | 意義 | 處理方式 |
|------|--------|------|---------|
| 401 | `missing_api_key` | 未帶 X-API-Key | 檢查 header |
| 401 | `invalid_api_key` | Key 錯誤或無此 workspace | 確認 key 正確 |
| 403 | — | workspace 無存取權 | 確認 workspace 與 key 對應 |
| 404 | `task_not_found` | 任務不存在 | 確認 task_no / id |
| 422 | — | 欄位格式錯誤 | 檢查 request body |

---

## 操作建議

**開始工作前**：
```
GET /steps/today        → 看今日待辦
GET /steps/followup-due → 看需要追蹤的委派
GET /dashboard/summary  → 看整體狀況
```

**找任務時**：優先用 `POST /search`（語意搜尋比 list + filter 更準）

**步驟粒度**：單一步驟預期 15–120 分鐘可完成；太大請再拆

**記錄頻率**：完成每個步驟後立即 log，不要累積

**task_no vs task_id**：
- `task_no`（如 `T260504-1430`）是人類識別碼，在 URL 和對話中使用
- `task_id`（整數）是 DB 主鍵，只在 API response 中使用，不需要記憶
