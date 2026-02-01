---
trigger: glob
glob: "AGENTS.md|.windsurf/workflows/**|.windsurf/rules/**|.windsurf/skills/**"
---

# Windsurf 配置研究與修改規範

## 🎯 適用範圍

此規則適用於以下檔案的修改和建立：
- `AGENTS.md` - 所有目錄層級
- `.windsurf/workflows/*.md` - Workflow 定義
- `.windsurf/rules/*.md` - Rule 定義
- `.windsurf/skills/**` - Skill 定義和資源

## 📚 修改前的研究流程

在修改或建立 Windsurf 配置檔案前，**必須先進行網路研究**：

### 1. 搜尋官方文件和最佳實踐
使用 `search_web` 工具搜尋：
- Windsurf 官方文件
- Cascade AI 配置指南
- 相關的 GitHub 專案範例
- 社群討論和最佳實踐

**搜尋關鍵字範例：**
- `Windsurf workflow`
- `Windsurf rules`
- `Windsurf skills`
- `Windsurf AGENTS.md`

### 2. 查閱相關資源
- 查看 `.windsurf/docs/` 中的文件
- 參考 `.windsurf/templates/` 中的模板
- 檢查現有的類似檔案作為參考

### 3. 理解核心概念
在開始修改前，確保理解：
- **Workflow**: 可重複執行的步驟序列，用 `/slash-command` 觸發
- **Rule**: 行為規範和偏好設定，支援多種觸發模式
- **Skill**: 複雜任務的完整套件，包含資源和文件
- **AGENTS.md**: 目錄特定的指南，自動根據位置應用

## 📋 修改檢查清單

修改前檢查：
- [ ] 已搜尋相關的官方文件和最佳實踐
- [ ] 已理解該配置類型的用途和結構
- [ ] 已檢查現有類似檔案的寫法
- [ ] 已確認 YAML frontmatter 格式正確
- [ ] 已驗證檔案位置和命名規範

## 🔍 常見配置類型的研究重點

### Workflow 修改
研究重點：
- 步驟序列的邏輯順序
- `// turbo` 註解的使用（標記可自動執行的步驟）
- 前置條件和依賴關係
- 錯誤處理和驗證步驟

### Rule 修改
研究重點：
- 觸發模式選擇（always_on, manual, model_decision, glob）
- Glob 模式的正確語法
- 規則的清晰性和可操作性
- 避免過於通用的規則

### Skill 建立
研究重點：
- 目錄結構（SKILL.md, scripts/, references/, assets/）
- YAML frontmatter 的必要欄位
- 資源檔案的組織方式
- 何時應該建立 Skill vs Workflow vs Rule

### AGENTS.md 編寫
研究重點：
- 目錄特定的指南內容
- 繼承和作用域規則
- 清晰的格式和具體範例
- 避免與父目錄重複

## 🌐 推薦的研究資源

### 官方資源
- Windsurf 官方文件
- Cascade AI 配置指南
- GitHub 上的 windsurf-config 範例

### 社群資源
- GitHub Discussions
- Stack Overflow (windsurf tag)
- 相關的開源專案配置

### 本地資源
- `.windsurf/docs/workflow-guide.md`
- `.windsurf/templates/` 中的模板
- 現有的 AGENTS.md 檔案

## ✅ 修改完成後

修改完成後的驗證：
1. 檢查 YAML frontmatter 語法
2. 驗證檔案位置和命名
3. 測試配置的實際效果
4. 如果是 .windsurf 下的檔案，執行 `/commit-windsurf` 提交

## 📝 範例工作流程

```
1. 識別需要修改的檔案
   ↓
2. 使用 search_web 搜尋相關最佳實踐
   ↓
3. 查閱本地的相似檔案和模板
   ↓
4. 理解該配置類型的結構和用途
   ↓
5. 執行修改或建立
   ↓
6. 驗證語法和功能
   ↓
7. 如需要，提交變更
```

## 🚫 常見錯誤

避免以下錯誤：
- ❌ 未經研究直接修改
- ❌ 複製不適合的模板
- ❌ 忽視 YAML frontmatter 的必要欄位
- ❌ 建立過於通用的 Rule
- ❌ 在 Workflow 中混淆步驟順序
- ❌ 忘記驗證 Glob 模式語法
