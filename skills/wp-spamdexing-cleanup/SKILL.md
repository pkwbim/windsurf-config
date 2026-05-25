---
name: wp-spamdexing-cleanup
description: 偵測與清除 WordPress 站台群的 SEO spamdexing（backlink spam）注入——典型是主題 footer.php 被植入 sponsor-area（display:none）隱藏容器，內含數百條 dofollow 賭場/spam 連結（harbicasino、paki99、casino.id 等）。觸發時機：(1) 收到站台 spam 檢舉或 Google Search Console 安全問題通知、(2) 懷疑某站首頁被注入隱藏外連、(3) 一站中招後要巡檢同主機/同 cPanel 其他站、(4) 定期 spam 巡檢。涵蓋偵測、定位、備份、清除、cache purge、雙 UA 驗證留證、根因與加固。主要在 WP-CPANEL（cp172 匯智 cPanel）上操作，但流程通用於任何 WordPress 主機。
---

# WordPress SEO Spamdexing 偵測與清除

## 攻擊特徵

- 注入點通常是**主題 footer.php**（每頁都載入），位置在 `<?php wp_footer(); ?>` 之後、`</body>` 之前。
- 一個 `<div class="sponsor-area" style="display:none">` 容器內塞 300-400 條 `<a rel="dofollow">` 賭場/spam 外連。
- 靠 **CSS `display:none` 隱藏**（不是 User-Agent cloaking）——人眼看不到，Googlebot 照吃。一般 UA 與 Googlebot UA 抓到的內容相同。
- 純靜態硬編碼，通常無 base64/eval 等動態執行碼（後門另尋，見加固）。

## 鐵則（血淚教訓，先讀）

1. **不要只靠 mtime 篩近期異動檔。** spam 常已存在數月才被發現；攻擊者也會偽造 mtime（實例見過顯示 2023 年的）。改靠**內容簽名**定位（grep `sponsor-area` / 賭場域名 / 大量 dofollow）。
2. **一站中招 → 巡檢同主機全部站，且不限主題。** 同一波攻擊會打多站；不同主題（woodmart、dizzcox…）的 footer.php 都可能中。
3. **清完一定雙 UA + 繞 cache 複驗並留證，絕不口頭宣告「清乾淨」。** 曾有前次處理謊報「全部乾淨」實際大量漏網躺 5 個月。用 `verify_homepage.sh`。
4. **有 litespeed-cache 外掛的站，清完檔案首頁仍會吐舊 spam**——見下方 cache 章節，務必用對 purge 方式。
5. **動正式站前先備份、確認可回滾**；危險刪除走 `clean_footer_spam.sh` 的驗證 gate，不要手動 sed 寫死行號。

## 五階段流程

### 1. 偵測（只讀）
在目標 WP 主機本地跑掃描（agent 透過 ssh 餵入）：
```bash
ssh <host> "bash -s <docroot_root>" < scripts/scan_spamdexing.sh
# 例: ssh WP-CPANEL "bash -s /home/quanzar/public_html" < scripts/scan_spamdexing.sh
```
列出所有命中簽名的 footer/php 檔 + 異常大的前台 footer.php。

### 2. 確認對外影響（只讀）
從可連外機器對命中站跑雙 UA 驗證：
```bash
bash scripts/verify_homepage.sh <domain> [domain2 ...]
```
站台常 301 → www，腳本已用 `-L` 跟隨。首頁實際吐 spam 才是活躍中招；footer.php 有 spam 但主題未啟用 = 休眠（仍應清）。

### 3. 備份（可回滾）
至少備份 footer.php 原檔（`clean_footer_spam.sh` 會自動做）。完整保險另備 DB——**`wp db export` 在 cp172 會 exit 255，改用 mysqldump，且注意 DB_HOST 含 port 的坑**，細節見 [references/cleanup-sop.md](references/cleanup-sop.md)。

### 4. 清除（危險，有 gate）
逐檔在目標主機跑：
```bash
ssh <host> "bash -s '<footer.php路徑>' '<備份目錄>'" < scripts/clean_footer_spam.sh
```
動態定位 `sponsor-area`→`</body>`，刪除區塊，`cat >` 覆蓋保留 owner。清除版未通過驗證（spam 歸零 + 結尾 `</html>`）則原檔不動並報錯。

### 5. Purge cache + 驗證留證
purge（見下節）後再跑一次 `verify_homepage.sh`，三項（一般 UA / Googlebot / 繞 cache）全 0 才算完工。

## Cache purge —— 兩種情況（最易錯）

清完檔案但首頁仍吐 spam = cache 殘留。看 `curl -sI` 的 `x-litespeed-cache` header 判斷：

- **站台沒裝 litespeed-cache 外掛**：server 內發 PURGE 即可
  ```bash
  curl -s -X PURGE "http://127.0.0.1/" -H "Host: <domain>"      # 含 www 版各發一次
  ```
- **站台有裝 litespeed-cache 外掛**（header 顯示 `x-litespeed-cache: hit`）：**上面的 PURGE 和 `wp cache flush` 都無效**，必須用外掛命令：
  ```bash
  cd <docroot> && sudo -u <owner> wp litespeed-purge all
  ```

判斷 cache vs 檔案問題：`verify_homepage.sh` 的「繞 cache」欄＝0 但一般/Googlebot 有命中 → 純 cache 殘留，去 purge；繞 cache 仍有命中 → 檔案還沒清乾淨或有第二注入點。

## 根因與加固

清除只是止血。footer.php 被改代表有入口（漏洞外掛 / 盜用密碼 / 過時主題外掛 / 檔案管理器外掛）。清完務必追根因 + 加固，否則會復發。完整清單（全站後門掃描、admin 帳號、死碼目錄、DISALLOW_FILE_EDIT、GSC 偵測層、fresh core 替換）見 [references/cleanup-sop.md](references/cleanup-sop.md)。

## 紀錄紀律

每次中招事件在 TASQ 開 task，log 記注入點/時間/範圍，retrospective 記教訓。完工回報要附**雙 UA 驗證數據**（清除前→後對照），不只說「清好了」。
