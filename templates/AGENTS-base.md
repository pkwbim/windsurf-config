# 🏢 專案規範

## 📋 專案概述

一人公司完整 monorepo，整合產品管理、政策規範、共享契約、DDD 核心業務邏輯、多介面應用層。

## 📁 目錄結構規範

```
project/
├── management/              # 私有經營層級
│   ├── strategy/           # 策略規劃
│   ├── finance/            # 財務管理
│   ├── legal/              # 法律文件
│   └── docs/               # 經營文件
├── pm/                      # 產品管理
│   ├── planning/           # 01_backlog, 02_active, 03_completed
│   ├── discussions/        # DISC-*.md 討論檔案
│   ├── decisions/          # DEC-*.md 決策檔案
│   └── sprints/            # Sprint 規劃
├── policies/                # 公司規定
│   ├── foundation/         # 基礎規定
│   ├── engineering/        # 工程規範
│   ├── operations/         # 營運規範
│   └── product/            # 產品規範
├── src/                     # 程式碼層（由 /setup-structure 建立）
├── enterprise/              # 企業版
├── tools/                   # 工具腳本
├── scripts/                 # 自動化腳本
├── out/                     # 輸出檔案
├── discussions/             # 全域討論檔案
├── docs/                    # 文件
└── .windsurf/              # Windsurf 配置
```

## 🛠️ 技術棧

> ⚠️ 技術棧尚未設定，請執行 `/setup-techstack` 設定技術棧。
> 設定完成後，執行 `/setup-agents` 會更新此章節。

## 🎯 核心開發原則

### DDD (Domain-Driven Design)
- **Domain Layer**: 業務邏輯、實體、用例
- **Infrastructure Layer**: 資料庫、API、外部服務
- **Application Layer**: 服務協調、事務管理

### OOP (Object-Oriented Programming)
- 在 `src/core/` 使用 OOP 設計
- 類別、介面、繼承、多型

### TDD (Test-Driven Development)
- 先寫測試，後寫實現
- 單元測試檔案：`*.unit.py` 或 `*.test.ts`
- 整合測試檔案：`*.integration.py` 或 `*.integration.ts`

## 📝 命名規範

| 層級 | 規範 | 範例 |
|------|------|------|
| 目錄 | kebab-case | `src/core/domain/use-cases/` |
| Python 檔案 | snake_case | `user_repository.py` |
| Python 類別 | PascalCase | `UserRepository` |
| TypeScript 檔案 | camelCase | `userService.ts` |
| TypeScript 類別 | PascalCase | `UserService` |
| 常數 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |

## 🔐 敏感資訊處理

- 環境變數存放在 `.env` 檔案（不提交到 Git）
- `.env.example` 提供範本
- 敏感資訊不應出現在程式碼中
