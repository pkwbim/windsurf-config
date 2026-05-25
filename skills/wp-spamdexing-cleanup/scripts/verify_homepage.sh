#!/bin/bash
# 雙 UA + 繞 cache 驗證站台首頁是否還有 spam。從可連外的機器執行（如 agent 本地）。
# 這是「留證」工具——清除後務必跑，杜絕「以為清完=乾淨」的謊報。
#
# 用法: verify_homepage.sh <domain> [domain2 ...]
#
# 對每站抓三種：一般 UA、Googlebot UA、帶 unique query 繞 cache。
# 全 0 才算真乾淨。若一般/Googlebot 有命中但繞 cache=0 → 是 cache 殘留，去 purge（見 SKILL.md）。

set -u
[ $# -ge 1 ] || { echo "用法: verify_homepage.sh <domain> [domain2 ...]"; exit 1; }

UA_NORMAL='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
UA_BOT='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
PAT='rel="dofollow"|casino|paki99|sponsor-area'

for d in "$@"; do
  ts=$(date +%s)
  n=$(curl -sL --max-time 25 -A "$UA_NORMAL" "https://$d/"        2>/dev/null | grep -ciE "$PAT")
  g=$(curl -sL --max-time 25 -A "$UA_BOT"    "https://$d/"        2>/dev/null | grep -ciE "$PAT")
  c=$(curl -sL --max-time 25                 "https://$d/?nc=$ts" 2>/dev/null | grep -ciE "$PAT")
  code=$(curl -sL -o /dev/null -w '%{http_code}' --max-time 20 "https://$d/" 2>/dev/null)
  if [ "$n" -eq 0 ] && [ "$g" -eq 0 ] && [ "$c" -eq 0 ]; then
    verdict="✅ 乾淨"
  elif [ "$c" -eq 0 ]; then
    verdict="⚠️ 檔案乾淨但有 CACHE 殘留→需 purge"
  else
    verdict="❌ 仍有 spam"
  fi
  echo "$d → HTTP $code | 一般UA=$n Googlebot=$g 繞cache=$c  $verdict"
done
