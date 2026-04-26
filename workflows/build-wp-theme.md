---
description: WordPress 主題開發 workflow（PHP/CSS/JS + Docker 測試 + 部署到 WP-Web）
---

## 🎯 目的
開發和修改 WordPress 自訂主題（Quanhox 或其他主題），包含 Customizer 設定、CSS 樣式、JS 互動、模板檔案。
適用於所有 `src/themes/` 目錄下的主題開發工作。

## ⚠️ 重要原則
- **Docker 優先**：所有開發和測試在本地 Docker 環境完成，不直接在 production 操作
- **CSS Variables 驅動**：所有樣式透過 CSS Variables 控制，不硬編碼顏色/字體值
- **Customizer 相容**：所有設定必須可透過 WordPress Customizer UI 操作
- **WP-CLI 相容**：所有 setting key 必須可透過 `wp theme mod get/set` 操作
- **人類確認後才進下一步**
- **設計系統先行**：如有視覺設計需求，先用 `ui-ux-pro-max` + `frontend-design` skill 產生設計系統

---

## 工作流程步驟

### 0. 確認前置條件
// turbo
```bash
git branch --show-current
```
- 如果目前仍在 `main`：停止並提醒先執行 `/plan` 以建立 feature 分支
- 如果已在 feature 分支：繼續

// turbo
```bash
cat pm/planning/02_active.md
```
- 確認規格已在 `pm/planning/02_active.md`

**❗️ 重要：必須完整閱讀 Story 目錄下的規格文件，理解：**
- `use-cases.md`：Use Case 流程
- `business-rules.md`：業務規則（驗證、命名、預設值）
- `spec.md`：技術規格（setting keys、CSS Variables、檔案結構）
- `checklist.md`：開發進度追蹤
- `e2e-scenarios.md`：E2E 測試劇本

### 1. 閱讀規格並建立實作計畫

讀取所有規格文件：
// turbo
```bash
STORY_DIR=$(grep -oP 'stories/\S+' pm/planning/02_active.md | head -1)
ls pm/planning/$STORY_DIR/
```

// turbo
```bash
STORY_DIR=$(grep -oP 'stories/\S+' pm/planning/02_active.md | head -1)
cat pm/planning/$STORY_DIR/spec.md
```

**根據 `spec.md` 和 `checklist.md`，確認實作順序。**

典型的 WordPress 主題開發順序：
1. 設計系統產生（若有視覺設計需求）
2. Customizer 設定註冊（`inc/customizer.php`）
3. CSS Variables 輸出機制（`inc/helpers.php`）
4. Body class 輸出（`functions.php`）
5. 主樣式表（`assets/css/main.css`）
6. 即時預覽 JS（`assets/js/customizer.js`）
7. 模板檔案更新（`header.php`、`footer.php` 等）
8. `theme.json` 更新

### 2. 設計系統產生（若需要）

**觸發條件（符合任一即啟動）：**
- Story 涉及色盤、字體、排版、佈局等視覺設計
- 新增頁面模板或全新 UI 區塊
- Story 描述中有「風格」「樣式」「美觀」「排版」等關鍵字
- 不確定時：啟動（寧可多做設計思考，不要寫出 AI slop）

**不需要啟動：** 純 Customizer 欄位新增（無視覺變化）、bug 修正、邏輯修改

#### Step 2a：用 `ui-ux-pro-max` skill 產生設計系統

```bash
# 產生完整設計系統（色盤、字體、風格、效果）
python3 skills/ui-ux-pro-max/scripts/search.py "<產業關鍵字> <風格關鍵字>" --design-system -p "<主題名稱>"

# 保存設計系統供後續 session 使用（推薦）
python3 skills/ui-ux-pro-max/scripts/search.py "<產業關鍵字>" --design-system --persist -p "<主題名稱>"

# 補充搜尋（需要更多選項時）
python3 skills/ui-ux-pro-max/scripts/search.py "<關鍵字>" --domain style -n 5
python3 skills/ui-ux-pro-max/scripts/search.py "<關鍵字>" --domain typography -n 5
```

產出物：配色方案、字體配對、UI 風格推薦、需避免的反模式。

#### Step 2b：用 `frontend-design` skill 決定美學方向

在寫任何 CSS 之前，依 `frontend-design` skill 的 Design Thinking 流程思考：

1. **Purpose**：這個主題/排版解決什麼問題？誰在用？
2. **Tone**：選擇明確的美學方向（不可模糊）：
   - 例：editorial/magazine、luxury/refined、soft/pastel、brutalist/raw
3. **Differentiation**：什麼讓這個設計令人難忘？
4. **Anti-patterns**：絕不使用 Inter/Roboto/Arial、紫色漸層白背景、千篇一律的卡片圓角

**將設計決策記錄在 `spec.md` 或 `design-system/MASTER.md`，包含：**
- 選定的美學方向（一句話）
- 字體配對（Display + Body）
- 主色 / 強調色 / 背景色
- 間距與圓角策略
- 動效策略（hover、transition、scroll-triggered）

**設計系統確認後，更新 `spec.md` 的預設值。**

### 3. 啟動 Docker 測試環境

// turbo
```bash
make dev-up 2>&1 | tail -5
```

確認 WordPress 可訪問：
// turbo
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ || echo "Not running"
```

如果 Docker 環境尚未建立，參考 Story-008 的設定。

### 4. 實作 Customizer 設定（`inc/customizer.php`）

**這是核心檔案，定義所有 WordPress Customizer 面板設定。**

開發規範：
- 所有 setting key 以 `quanhox_` 前綴 + snake_case（如 `quanhox_primary_color`）
- 顏色設定使用 `WP_Customize_Color_Control` + `sanitize_hex_color`
- 選擇設定使用 `select` type + `sanitize_text_field`
- 數值設定使用 `number` type + 自訂 sanitize callback（含範圍限制）
- 所有設定 transport 為 `postMessage`（即時預覽）
- 設定按 section 分組：Colors、Typography、Styles、Layout

**語法檢查（每次修改後）：**
// turbo
```bash
php -l src/themes/quanhox/inc/customizer.php
```

### 5. 實作 CSS Variables 輸出（`inc/helpers.php`）

**負責將 `theme_mods` 轉換為 `:root { }` CSS Variables。**

開發規範：
- CSS Variable 前綴統一為 `--qh-`
- 繼承機制：`inherit` 值轉為 `var(--qh-text-font)` 等
- 空值使用預設值
- 透過 `wp_add_inline_style` 注入 `<head>`

**語法檢查：**
// turbo
```bash
php -l src/themes/quanhox/inc/helpers.php
```

### 6. 實作 Body Class 與 Meta Tags（`functions.php`、`header.php`）

- `functions.php`：`body_class` filter 新增佈局/樣式 class
- `header.php`：`<meta name="theme-color">` 輸出

**語法檢查：**
// turbo
```bash
php -l src/themes/quanhox/functions.php
php -l src/themes/quanhox/header.php
```

### 7. 實作主樣式表（`assets/css/main.css`）

**使用 CSS Variables 驅動所有樣式，不硬編碼值。**

開發規範：
- 所有顏色使用 `var(--qh-*)` 而非 hex 值
- 所有字體使用 `var(--qh-text-font)` 等而非直接寫字體名
- Body class 選擇器：`body.qh-layout-boxed`、`body.qh-btn-default-rounded` 等
- 響應式設計使用 media queries
- 重點優化文章閱讀體驗和 CTA 按鈕

**`frontend-design` 美學品質檢查（寫 CSS 時持續參考）：**
- **Typography**：字體是否有特色？Display + Body 配對是否和諧？
- **Color**：主色是否有存在感？強調色是否足夠醒目？避免平均分配色彩
- **Spatial**：間距是否有呼吸感？是否有非對稱或意外的佈局？
- **Motion**：hover 效果是否有驚喜？transition 是否流暢（200-300ms）？
- **Backgrounds**：是否避免了純白/純灰的平淡背景？有沒有紋理/漸層/陰影增加層次？
- **Anti-slop**：是否看起來像「AI 產生的」？如果是，重新設計

### 8. 實作即時預覽 JS（`assets/js/customizer.js`）

**讓 Customizer 修改即時反映在預覽區。**

```javascript
// 每個 setting 對應一個 postMessage handler
wp.customize( 'quanhox_primary_color', function( value ) {
    value.bind( function( newval ) {
        document.documentElement.style.setProperty( '--qh-primary-color', newval );
    });
});
```

**語法檢查：**
// turbo
```bash
node --check src/themes/quanhox/assets/js/customizer.js
```

### 9. 更新 theme.json

更新 color palette 和 typography 設定，與 Customizer 保持一致。

### 10. Docker 環境測試

**依照 `e2e-scenarios.md` 逐項測試：**

1. 瀏覽器開啟 `http://localhost:8080/wp-admin/`
2. 前往 Appearance > Customize
3. 測試每個設定項的操作和即時預覽
4. Publish 後確認前端 CSS Variables 正確
5. 確認 body class 正確
6. 確認 `<meta name="theme-color">` 正確

**WP-CLI 測試（在 Docker 容器內）：**
```bash
docker compose exec wordpress wp theme mod list --allow-root
docker compose exec wordpress wp theme mod set quanhox_primary_color '#ff0000' --allow-root
```

### 11. 更新 checklist.md

更新 story 目錄下的 `checklist.md`，勾選已完成的項目。

### 12. 更新開發狀態

更新 `pm/planning/02_active.md`：
```markdown
**📊 開發狀態**: ✅ Build 完成 → 待人工驗證
```

### 13. 🛑 人工驗證檢查點（MANDATORY）
**⚠️ 重要：此步驟不可跳過！**

完成實作後，**必須**停下來等待使用者進行人工驗證：

1. **提供驗證指南**：
   - Docker 環境訪問方式（`http://localhost:8080`）
   - 需要驗證的 Customizer 設定清單
   - 前端需要檢查的 CSS Variables 和 body class
   - WP-CLI 測試指令

2. **明確告知使用者**：
   ```
   ⚠️ 請進行人工驗證
   
   已完成主題開發，Docker 環境已啟動：
   - 🌐 前端：http://localhost:8080
   - 🔧 後台：http://localhost:8080/wp-admin/
   
   📋 驗證項目：
   - [ ] Customizer 面板設定項正確顯示
   - [ ] 即時預覽正常運作
   - [ ] Publish 後前端樣式正確
   - [ ] CSS Variables 輸出正確
   - [ ] Body class 輸出正確
   
   ✅ 驗證完成後，請回覆「驗證通過」以繼續下一步
   ❌ 如發現問題，請描述問題以便修正
   ```

3. **等待使用者回應**：
   - **不要自動執行 `/commit`**
   - **不要假設驗證已通過**

### 14. 提示下一步

告訴使用者：
- ✅ WordPress 主題開發完成
- 📝 已更新開發狀態和 checklist
- 🔜 下一步：執行 `/commit` 提交程式碼
- 🚀 部署到 production：`make install-theme domain=xxx` 或 `make update-theme domain=xxx`

---

## 適用場景
- WordPress 自訂主題開發（Quanhox 或其他主題）
- Customizer 設定面板修改
- 主題 CSS/JS 樣式修改
- 模板檔案（header/footer/page）修改
- theme.json 設定更新

## 不適用場景
- CLI 腳本開發 → 使用 `/build-cli`
- Laravel 介面開發 → 使用 `/build-laravel`
- 純遠端操作（Nginx、MariaDB） → 使用 `/build-cli`

---

## Tech Stack
- **語言**: PHP 8.x、CSS3、JavaScript (ES6+)
- **框架**: WordPress 6.x Customizer API
- **樣式**: CSS Custom Properties (Variables)
- **測試環境**: Docker Compose（WordPress + MariaDB）
- **部署**: rsync over SSH → WP-Web VPS
- **設計工具**: `ui-ux-pro-max` + `frontend-design` skill
- **驗證**: 手動 + WP-CLI + e2e-scenarios.md
