# 開發階段檢查清單 Template

此 template 定義了標準的開發階段檢查清單，供各 workflow 引用。

---

## 使用方式

各 workflow 在「更新開發狀態」步驟中，應參考此 template 並標註：
1. 當前完成的階段打勾 `[x]` 並加上 `✅`
2. 下一步階段加上 `⬅️ 下一步`
3. 未完成的階段保持 `[ ]`

---

## 標準檢查清單

```markdown
## 開發階段檢查清單
- [ ] 需求規劃完成 (`/plan`)
- [ ] **階段 1: 純 UI 開發** (`/build-ui`)
- [ ] **階段 2: API Contract 設計** (`/build-contract`)
- [ ] **階段 3: Backend 實作** (`/build-backend`)
- [ ] **整合測試** (`/integration`)
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

---

## 各階段完成後的狀態

### `/build-ui` 完成後
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`) ✅
- [ ] **階段 2: API Contract 設計** (`/build-contract`) ⬅️ 下一步
- [ ] **階段 3: Backend 實作** (`/build-backend`)
- [ ] **整合測試** (`/integration`)
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

### `/build-contract` 完成後
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`) ✅
- [ ] **階段 3: Backend 實作** (`/build-backend`) ⬅️ 下一步
- [ ] **整合測試** (`/integration`)
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

### `/build-backend` 完成後
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`)
- [x] **階段 3: Backend 實作** (`/build-backend`) ✅
- [ ] **整合測試** (`/integration`) ⬅️ 下一步
- [ ] 文件更新 (`/review`)
- [ ] 已合併到 main (`/merge`)
```

### `/integration` 完成後
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`)
- [x] **階段 3: Backend 實作** (`/build-backend`)
- [x] **整合測試** (`/integration`) ✅
- [ ] 文件更新 (`/review`) ⬅️ 下一步
- [ ] 已合併到 main (`/merge`)
```

### `/review` 完成後
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`)
- [x] **階段 3: Backend 實作** (`/build-backend`)
- [x] **整合測試** (`/integration`)
- [x] 文件更新 (`/review`) ✅
- [ ] 已合併到 main (`/merge`) ⬅️ 下一步
```

### `/merge` 完成後
```markdown
## 開發階段檢查清單
- [x] 需求規劃完成 (`/plan`)
- [x] **階段 1: 純 UI 開發** (`/build-ui`)
- [x] **階段 2: API Contract 設計** (`/build-contract`)
- [x] **階段 3: Backend 實作** (`/build-backend`)
- [x] **整合測試** (`/integration`)
- [x] 文件更新 (`/review`)
- [x] 已合併到 main (`/merge`) ✅
```

---

## 下一步提示對照表

| 當前階段 | 下一步 | 提示訊息 |
|----------|--------|----------|
| `/build-ui` | `/build-contract` | 🔜 下一步：`/build-contract` - API Contract 設計 |
| `/build-contract` | `/build-backend` | 🔜 下一步：`/build-backend` - Backend 實作（TDD） |
| `/build-backend` | `/integration` | 🔜 下一步：`/integration` - 整合測試 |
| `/integration` | `/review` | 🔜 下一步：`/review` - 更新文件並歸檔 |
| `/review` | `/merge` | 🔜 下一步：`/merge` - 合併到 main |
| `/merge` | 完成 | ✅ Story 完成！ |
