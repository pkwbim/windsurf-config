# .windsurf 目錄規範

此目錄包含 Windsurf/Cascade AI 的配置檔案。

## 📁 目錄結構

| 目錄 | 用途 | 命名規範 |
|------|------|----------|
| `workflows/` | 可重複執行的流程 | `kebab-case.md` |
| `templates/` | 模板檔案 | `kebab-case.md` |
| `docs/` | 使用說明文件 | `kebab-case.md` |
| `skills/` | 複雜任務的技能包 | `skill-name/SKILL.md` |
| `rules/` | 行為規則 | `kebab-case.md` |

## 📝 維護規範

### 新增/修改 Workflow 時
1. 在 `workflows/` 建立或修改 `.md` 檔案
2. **必須**在 `docs/workflow-guide.md` 更新說明

### 需要模板時
- 模板檔案放在 `templates/` 目錄
- 命名格式：`{用途}-{類型}.md`（如 `AGENTS-base.md`）

### 新增 Skill 時
- 在 `skills/{skill-name}/` 建立目錄
- 必須包含 `SKILL.md`
- 可選：`scripts/`, `references/`, `assets/`

## 🔗 重要檔案

- `docs/workflow-guide.md` - Workflow 使用指南
- `templates/AGENTS-base.md` - 根目錄 AGENTS.md 模板
- `templates/docs-README.md` - docs/README.md 模板
