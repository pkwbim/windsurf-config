# Spamdexing 清除 SOP — 細節參考

目錄：
- [備份指令（含 mysqldump 坑）](#備份指令)
- [根因排查](#根因排查)
- [加固清單](#加固清單)
- [WP-CPANEL 環境速查](#wp-cpanel-環境速查)
- [偵測層：Google Search Console](#偵測層google-search-console)
- [歷史教訓：上次謊報事件](#歷史教訓上次謊報事件)

---

## 備份指令

### footer.php 原檔
`clean_footer_spam.sh` 會自動 `cp -p` 到備份目錄。手動備份同理。備份目錄放 **docroot 外**（如 `/home/<user>/<backup_dir>/`），web 存取不到。

### DB（完整保險，清 footer 不動 DB 但建議備）
**`wp db export` 在 cp172 會 exit 255 無輸出（壞掉），改用 mysqldump。** 且該機 `DB_HOST=localhost:3306`（含 port），mysqldump 不吃 `host:port`，要拆開，否則報 `2005 Unknown MySQL server host`：

```bash
cd <docroot>
DBNAME=$(sudo -u <owner> wp config get DB_NAME)
DBUSER=$(sudo -u <owner> wp config get DB_USER)
DBPASS=$(sudo -u <owner> wp config get DB_PASSWORD)
RAWHOST=$(sudo -u <owner> wp config get DB_HOST)
HOST=${RAWHOST%%:*}; PORT=${RAWHOST##*:}; [ "$PORT" = "$RAWHOST" ] && PORT=3306
mysqldump --no-tablespaces -h "$HOST" -P "$PORT" -u"$DBUSER" -p"$DBPASS" "$DBNAME" > <backup>/db.sql
tail -1 <backup>/db.sql   # 應為 "-- Dump completed"
```

### 改檔保留 owner
用 `cat /tmp/clean > <docroot>/file` 覆蓋（保留 inode/owner/perm），**不要用 mv**（會變成 root owner）。`clean_footer_spam.sh` 已照此做。

---

## 根因排查

清完 footer.php 是止血。攻擊者怎麼改到檔的（入口）通常未除，**會復發**。逐項查（皆只讀）：

```bash
DR=<docroot>
# 1. uploads 內的 php（正常不該有，高度可疑）
find $DR/wp-content/uploads -name '*.php' -type f

# 2. webshell 特徵（注意過濾 WP core / 知名外掛的大量誤報：
#    kses.php / ID3 / updraftplus / wordfence / woocommerce / phpseclib / litespeed 等都是合法）
grep -rlE 'eval\(.*base64_decode|assert\(\$_|\$_(POST|REQUEST|COOKIE|GET)\[.{0,15}\]\(|passthru\(|system\(\$' $DR --include='*.php'

# 3. 異常 admin 帳號（找非預期 email / 陌生帳號）
sudo -u <owner> wp user list --role=administrator --fields=ID,user_login,user_email,user_registered

# 4. mu-plugins（must-use，自動載入，常被植後門）
ls -la $DR/wp-content/mu-plugins/

# 5. .htaccess cloaking / 惡意 redirect
grep -niE 'googlebot|HTTP_USER|base64|eval' $DR/.htaccess

# 6. DB 內注入（posts 含 spam）+ 核心設定被竄改
sudo -u <owner> wp db query "SELECT COUNT(*) FROM <prefix>_posts WHERE post_content LIKE '%sponsor-area%'"
sudo -u <owner> wp option get siteurl; sudo -u <owner> wp option get home

# 7. 「插入頁首頁尾代碼」類外掛被濫用（wpcode / insert-headers-and-footers）
sudo -u <owner> wp option get ihaf_insert_footer | grep -iE 'casino|sponsor|dofollow'

# 8. 檔案管理器類外掛（fileorganizer 等，可後台編輯任意檔——疑似改檔工具）
#    比對它的安裝時間 vs 注入時間，可能洗清或坐實嫌疑
sudo -u <owner> wp plugin list --status=active | grep -iE 'fileorganizer|filemanager'
```

常見根因（2026 威脅環境）：過時漏洞外掛/主題、盜用的 admin 密碼、檔案管理器外掛、多層後門。

---

## 加固清單

- [ ] `wp-config.php` 加 `define('DISALLOW_FILE_EDIT', true);`（禁後台主題/外掛編輯器，斷掉盜帳號後直接改 footer 的路）
- [ ] 核心、主題、所有外掛更新到最新；**移除停用的外掛/主題與死碼目錄**（如 `plugins-backup_*`、`updraft/*-old`、`themes-old`——可被 web 存取的舊版漏洞碼）
- [ ] admin 帳號改強密碼 + 啟用 2FA；移除不明帳號
- [ ] 用乾淨來源重裝/比對主題 footer.php（確認沒有殘留變體）
- [ ] 嚴重時下載 fresh WordPress core 替換 `/wp-admin`、`/wp-includes`、根 index 等
- [ ] 平時不留檔案管理器類外掛（用完即移）
- [ ] 接 **Google Search Console**（見下節）+ 排定期掃描

---

## WP-CPANEL 環境速查

- SSH：`ssh WP-CPANEL`（root + id_ed25519），= cp172.quanzar.com.tw（172.105.210.241），匯智 cPanel 機，**不是** Linode WP-Web。
- 單一 cPanel 帳號 `quanzar`，docroot 在 `/home/quanzar/public_html/<domain>/`（主站直接在 public_html 根，其他為 addon 子目錄）。
- wp-cli：`/usr/local/bin/wp`，**一律 `sudo -u quanzar wp ...`**（站台 owner 身分）。
- table prefix 隨機（如 `2ve7CDP2_`），用 `wp db prefix` 取。

---

## 偵測層：Google Search Console

被 spamdexing 時 GSC 會直接通知「安全問題 / 手動處置」——這是最低成本、最早的警報，避免 spam 躺數月。
- 程式化存取需 **Google Cloud service account JSON**（或 OAuth），並在 GSC 把該 service account email 加為對應站 property 的使用者。
- 注意區分：`google<hash>.html`（網站擁有權**驗證檔**，放根目錄）≠ **API token**（service account JSON）。前者不能呼叫 API。
- 艦隊憑證走 agent-leader 取得（不要自己翻別的 agent 配置）。

---

## 歷史教訓：上次謊報事件

cp172 上 `/home/quanzar/public_html/20251226-malware/` 是 2025-12-26 入侵起的處理記錄。其中：
- `all_infected_20260225_*.txt` 列了 **36 站**有感染檔。
- 但 `BACKLINK_SPAM_CLEANUP_REPORT.md`(2026-03-06) 卻寫「僅 1 站受感染、其餘全乾淨、已全部清理完成」。

**兩份直接矛盾——上次根本沒清乾淨卻謊報全乾淨**，導致多站 spam 躺 5 個月到客戶回報才發現。**教訓：絕不口頭宣告乾淨，一律用 `verify_homepage.sh` 雙 UA + 繞 cache 留證；舊的「完工」報告不可盡信，要自己重驗。**
