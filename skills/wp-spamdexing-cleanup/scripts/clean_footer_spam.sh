#!/bin/bash
# 安全清除單一 footer.php 內的 sponsor-area spam 區塊。
# 在目標 WP 主機本地執行（agent 透過 ssh 跑）。內建備份 + 驗證 gate：
# 只有清除版驗證乾淨才覆蓋，否則原檔不動並報錯。
#
# 用法: clean_footer_spam.sh <footer.php路徑> <備份目錄>
#
# 手法: 刪除 "sponsor-area" 起始行 到 "</body>" 前一行（動態定位，不寫死行號——
#       各站被注入後行數不同，如 471/480）。用 cat > 覆蓋以保留 inode/owner/perm。

set -u
FP="${1:?用法: clean_footer_spam.sh <footer.php路徑> <備份目錄>}"
BK="${2:?需指定備份目錄}"

[ -f "$FP" ] || { echo "ERROR: 檔案不存在: $FP"; exit 1; }
mkdir -p "$BK"

TAG=$(echo "$FP" | sed 's#/wp-content/.*##; s#.*/##')   # 取站台目錄名當標籤
ORIG="$BK/${TAG}_footer.php.orig"

SA=$(grep -c 'sponsor-area' "$FP")
[ "$SA" -eq 0 ] && { echo "SKIP: $FP 無 sponsor-area，可能已清或非此注入"; exit 0; }

S=$(grep -n 'sponsor-area' "$FP" | head -1 | cut -d: -f1)
B=$(grep -n '</body>' "$FP" | head -1 | cut -d: -f1)
if [ -z "$S" ] || [ -z "$B" ] || [ "$S" -ge "$B" ]; then
  echo "ERROR: 定位失敗 (S=$S B=$B)，不自動清除，請人工檢視 $FP"; exit 1
fi

cp -p "$FP" "$ORIG" || { echo "ERROR: 備份失敗"; exit 1; }
TMP=$(mktemp)
sed "${S},$((B-1))d" "$FP" > "$TMP"

# 驗證 gate：清除版必須 spam 歸零且結尾正常
nsa=$(grep -c 'sponsor-area' "$TMP")
ndf=$(grep -c 'rel=.\?dofollow' "$TMP")
tail1=$(tail -1 "$TMP" | tr -d ' \r')
if [ "$nsa" -ne 0 ] || [ "$ndf" -ne 0 ] || [ "$tail1" != "</html>" ]; then
  echo "ABORT: 清除版驗證未過 (sponsor-area=$nsa dofollow=$ndf tail=$tail1)，原檔未動。備份在 $ORIG"
  rm -f "$TMP"; exit 1
fi

cat "$TMP" > "$FP"      # 保留 inode/owner/perm
rm -f "$TMP"
echo "OK: $TAG 已清 ($(wc -l <"$ORIG")行→$(wc -l <"$FP")行, sponsor-area→0)。備份: $ORIG"
echo "    下一步: purge cache + 雙 UA 驗證首頁（見 verify_homepage.sh / SKILL.md cache 章節）"
