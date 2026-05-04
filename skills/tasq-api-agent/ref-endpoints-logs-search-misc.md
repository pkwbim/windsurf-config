# Tasq API — Logs / Search / Dashboard / Retrospective / Templates 端點參考

## 工作記錄（Logs）

### 新增記錄
```http
POST /tasks/42/logs
Content-Type: application/json

{
  "content": "完成問卷整理，共 87 份，其中 23 份有具體改善建議",
  "step_id": 101
}
```
`step_id` 可選（不填表示任務層級的記錄）。

### 查看最近記錄
```http
GET /logs/recent?workspace=personal&limit=10
```

---

## 搜尋（Search）

### 混合搜尋（FTS + Vector）
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

## Dashboard 摘要

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

## 回顧（Retrospective）

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

## 模板（Templates）

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

# 使用模板（從模板建立任務）— GET template 後 POST tasks + steps/batch
```
