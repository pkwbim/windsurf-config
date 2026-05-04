# Tasq API — 欄位速查、錯誤碼、操作建議

## 欄位速查

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
