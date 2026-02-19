---
description: Playwright E2E 整合測試（通用，支援 Laravel + FastAPI+Vue）
---

## 🎯 目的
在 `/build-laravel-backend` 或 `/build-backend` 完成後，使用 **Playwright（Python）** 執行 E2E 整合測試，依 `e2e-scenarios.md` 劇本驗證完整使用者操作流程。

> **Skill 分工：**
> - `playwright-e2e` skill：E2E 測試規範（目錄、DB 隔離、劇本撰寫、測試資料）
> - `webapp-testing` skill：Playwright 執行方式（server 啟動、DOM 偵測、截圖）

---

## 執行步驟

### 1. 載入規範並確認前置條件
// turbo
```bash
cat pm/planning/02_active.md
```

確認：
- Backend 階段已完成（Feature Test 全部通過）
- `e2e-scenarios.md` 存在且有劇本

載入兩個 skill：
- `playwright-e2e` skill（E2E 規範）
- `webapp-testing` skill（Playwright 執行方式）

### 2. 確認測試目錄

讀取專案根目錄 `AGENTS.md`，尋找 E2E 測試目錄說明：

```bash
cat AGENTS.md
```

- **找到** → 使用該目錄
- **找不到** → 詢問使用者，建議慣例（Laravel: `src/app/tests/E2E/`；FastAPI+Vue: `tests/e2e/`），取得指示後加入 `AGENTS.md`

### 3. 確認 Playwright 已安裝
// turbo
```bash
python -m playwright --version 2>/dev/null && echo "已安裝" || echo "未安裝"
```

若未安裝：
```bash
pip install playwright pytest-playwright
python -m playwright install chromium
```

### 4. 讀取 e2e-scenarios.md

```bash
cat pm/planning/stories/{active_story}/e2e-scenarios.md
```

逐一列出所有劇本（S-01、S-02...），確認哪些需要自動化。

### 5. 確認 DB 隔離設定

依 `playwright-e2e` skill 的 DB 隔離策略：

**Laravel：**
```bash
# 確認 .env.testing 存在
cat src/app/.env.testing | grep DB_DATABASE
```

**FastAPI+Vue：**
```bash
cat backend/.env.test | grep DATABASE_URL
```

### 6. 建立 conftest.py（若不存在）

依 `playwright-e2e` skill 的模板，在測試目錄建立 `conftest.py`：
- `logged_in_user` fixture（登入共用邏輯）
- `setup_db` fixture（測試前 migrate + seed）

### 7. 依劇本撰寫測試

每個 `S-XX` 劇本對應一個 test function，依 `playwright-e2e` skill 的模板撰寫：

```python
def test_s01_{scenario_name}(self, page: Page, logged_in_user):
    """S-01：{劇本標題}"""
    # 操作步驟 → 程式碼
    # 預期結果 → assert / expect
```

### 8. 執行測試

依 `webapp-testing` skill 的 `with_server.py` 啟動 server 並執行：

**Laravel：**
```bash
python .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd src/app && php artisan serve --port=8234 --env=testing" \
  --port 8234 \
  -- pytest {測試目錄}/ -v
```

**FastAPI+Vue：**
```bash
python .windsurf/skills/webapp-testing/scripts/with_server.py \
  --server "cd backend && APP_ENV=test uvicorn app.main:app --port=8000" --port 8000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- pytest tests/e2e/ -v
```

### 9. 處理失敗的測試

若測試失敗：
1. 截圖確認頁面狀態（`playwright-e2e` + `webapp-testing` skill）
2. 確認 selector 是否正確（DOM 偵測）
3. 確認 Alpine.js 互動是否需要等待 `networkidle`
4. 修正測試程式或回報 Bug

### 10. 完成

告知使用者：
- ✅ E2E 測試完成，N 個劇本通過
- 🔜 下一步：`/review` - 更新文件並歸檔

---

## 與其他 Workflow 的關係
- `/build-laravel-backend` / `/build-backend` → Backend 實作完成後執行本 workflow
- `/integration` → 保留給 FastAPI+Vue 的舊版整合測試 workflow
- `/review` → E2E 測試完成後執行
