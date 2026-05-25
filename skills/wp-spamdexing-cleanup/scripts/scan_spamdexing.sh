#!/bin/bash
# 偵測 WordPress SEO spamdexing（backlink spam）注入。
# 在目標 WP 主機本地執行（agent 透過 ssh 跑）。只讀，不改任何檔。
#
# 用法: scan_spamdexing.sh <docroot_root>
#   docroot_root: 站台根的上層，例如 cPanel 的 /home/<user>/public_html
#
# 輸出: 每個命中 spam 簽名的 footer/php 檔，含 sponsor-area 數、dofollow 數、行數。
# 注意: 不靠 mtime（攻擊者會偽造；spam 常存在數月）。改靠內容簽名。

set -u
ROOT="${1:?用法: scan_spamdexing.sh <docroot_root>，例如 /home/quanzar/public_html}"

# 排除備份/隔離區，避免誤報死碼
EXCLUDE='/backups/|/updraft/|/20251226-malware/|plugins-backup|themes-old|\.wp-backup'

echo "=== [1] 內容簽名掃描（sponsor-area + 賭場域名 + 通用 dofollow）==="
SIG='sponsor-area|harbicasino|paki99|onlinecasinoground|grandercasino|worldgamingcasino|rel=.?dofollow'
HITS=$(grep -rliE "$SIG" "$ROOT" --include='*.php' 2>/dev/null | grep -vE "$EXCLUDE")

if [ -z "$HITS" ]; then
  echo "（無命中——線上檔案層乾淨）"
else
  while IFS= read -r f; do
    sa=$(grep -c 'sponsor-area' "$f" 2>/dev/null)
    df=$(grep -c 'rel=.\?dofollow' "$f" 2>/dev/null)
    ln=$(wc -l < "$f" 2>/dev/null)
    echo "  HIT  $f  (sponsor-area=$sa dofollow=$df 行數=$ln)"
  done <<< "$HITS"
fi

echo ""
echo "=== [2] 異常大的前台 footer.php（>150 行；正常約 80-100）==="
echo "    註: inc/admin/settings/footer.php 是 woodmart 後台元件(378行)為正常，自動略過"
find "$ROOT" -name footer.php -path '*/themes/*' \
  ! -path '*/inc/admin/*' ! -path '*/updraft/*' ! -path '*/backups/*' \
  ! -path '*plugins-backup*' -exec wc -l {} + 2>/dev/null \
  | awk '$1>150 && $2!="total"{print "  BIG  "$2"  ("$1"行)"}'

echo ""
echo "=== 完成。對命中站務必再跑首頁雙 UA 驗證（見 verify_homepage.sh）==="
