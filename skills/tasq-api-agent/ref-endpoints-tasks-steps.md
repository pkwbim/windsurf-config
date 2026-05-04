# Tasq API — Tasks & Steps 端點參考

## 任務（Tasks）

### 建立任務
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

### 列出任務
```http
GET /tasks?workspace=personal
X-API-Key: {key}
```

### 取得任務詳情（含 steps / logs / retrospective）
```http
GET /tasks/by-no/T260504-1430?workspace=personal
GET /tasks/42?workspace=personal
```

### 更新任務
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

## 步驟（Steps）

### 建立步驟
```http
POST /tasks/42/steps
Content-Type: application/json

{
  "title": "整理原始問卷資料",
  "due_date": "2026-05-06",
  "estimated_minutes": 60
}
```

### 批次建立步驟
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

### 更新步驟狀態
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

### 查看今日待辦
```http
GET /steps/today?workspace=personal
```
回傳 status 為 pending/in_progress/blocked 且 due_date <= 今日的步驟，含 `task_no` / `task_title`。

### 查看待追蹤委派
```http
GET /steps/followup-due?workspace=personal
```
回傳 status=delegated 且 next_followup_date <= 今日的步驟。
