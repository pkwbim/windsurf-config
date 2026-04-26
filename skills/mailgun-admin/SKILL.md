---
name: mailgun-admin
description: 透過 Mailgun API 管理 WP-Web 上各 WordPress 站台的 Mailgun 發信網域。觸發時機：(1) 使用者收到大量來自站上聯絡表單的 spam 信、(2) 需要清空 Mailgun 隊列中的殘留信件、(3) 需要查 Mailgun 發信狀態 / events / logs、(4) 需要將某 email 加入 / 移除 bounces / complaints / unsubscribes 抑制清單、(5) 需要查找某 WP 站台的 Mailgun API key、(6) 任何提到 "Mailgun"、"清隊列"、"sending queue"、"清 spam 殘留"、"post-smtp" 的請求。
---

# Mailgun Admin

管理本專案各 WordPress 站台所使用的 Mailgun 發信網域（每個站通常有自己的 `mg.<site>.tw` 子網域）。

## 憑證

- **Master Account API Key**：`credentials/mailgun-master-api.key`（單行字串，無 prefix）。可管理所有網域、清隊列、操作 bounces。
- **網域發信 key**（domain sending key）：存在各 WP 站的 `postman_options` option 內，base64 編碼。**權限不足以管理隊列或 suppression list**，只能發信、查 events。除非要 debug 站台本身的發信，否則一律用 master key。

取得 master key：
```bash
MG_KEY=$(cat credentials/mailgun-master-api.key | tr -d ' \n\r')
```

從 WP 站取得網域 key（如有需要 debug）：
```bash
ssh WP-WEB "wp option get postman_options --path=/var/www/<site>/public --allow-root --format=json" \
  | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['mailgun_api_key']).decode())"
```

## 重要：API host 規則

Mailgun 的 API 分兩種 host，**用錯會 404 / 405**：

| 操作類型 | Host | 範例 |
|---------|------|------|
| 一般帳號 / 網域 / suppression / events | `api.mailgun.net` | `https://api.mailgun.net/v3/<domain>/bounces` |
| **隊列管理（清隊列）** | `storage-<region>.api.mailgun.net` | `https://storage-us-east4.api.mailgun.net/v3/<domain>/envelopes` |

Storage region 從 events response 的 `storage.region` 欄位取得，常見值：
- `us-east4` → `storage-us-east4.api.mailgun.net`
- `us-west1` → `storage-us-west1.api.mailgun.net`
- `europe-west1` → `storage-europe-west1.api.mailgun.net`

查 region：
```bash
curl -sS -G --user "api:$MG_KEY" "https://api.mailgun.net/v3/<domain>/events" \
  --data-urlencode 'limit=1' | python3 -c "import sys,json; print(json.load(sys.stdin)['items'][0]['storage']['region'])"
```

## 常見任務 SOP

### 1. 清空殘留隊列（緊急止血 spam）

當站上 CF7 / 表單被機器人狂送 spam，已關掉表單但 Mailgun 還在補送殘留隊列：

```bash
MG_KEY=$(cat credentials/mailgun-master-api.key | tr -d ' \n\r')
DOMAIN=mg.ai-summoner.tw
REGION=us-east4   # 從 events 查到
curl -sS -X DELETE --user "api:$MG_KEY" \
  "https://storage-${REGION}.api.mailgun.net/v3/${DOMAIN}/envelopes"
# 預期回應: {"message":"done"}
```

### 2. 查發信記錄 / events

```bash
curl -sS -G --user "api:$MG_KEY" \
  "https://api.mailgun.net/v3/${DOMAIN}/events" \
  --data-urlencode 'event=accepted OR delivered OR failed' \
  --data-urlencode 'limit=20' | python3 -m json.tool
```

可用 `event` 參數：`accepted`、`delivered`、`failed`、`rejected`、`stored`、`opened`、`clicked`。  
篩選失敗類型：`severity=temporary` 或 `severity=permanent`。

### 3. Suppression list 操作（bounces / complaints / unsubscribes）

緊急情境：把目標收件人加進 bounces，可讓 Mailgun **立即跳過所有送給該地址的隊列訊息**（比清隊列更精準，不影響其他人）。但記得事後移除，否則正常通知信也收不到。

```bash
# 加入 bounce（暫時封鎖）
curl -sS -X POST --user "api:$MG_KEY" \
  "https://api.mailgun.net/v3/${DOMAIN}/bounces" \
  --data-urlencode "address=user@example.com" \
  --data-urlencode "code=550" \
  --data-urlencode "error=temp mitigation"

# 查 bounce
curl -sS --user "api:$MG_KEY" \
  "https://api.mailgun.net/v3/${DOMAIN}/bounces/user@example.com"

# 移除 bounce
curl -sS -X DELETE --user "api:$MG_KEY" \
  "https://api.mailgun.net/v3/${DOMAIN}/bounces/user@example.com"
```

對 `complaints` 和 `unsubscribes` 路徑同模式（替換 endpoint 名稱）。

### 4. 列出帳號下所有網域

```bash
curl -sS --user "api:$MG_KEY" "https://api.mailgun.net/v3/domains" | python3 -m json.tool
```

### 5. 查 WP 端 SMTP 發信記錄（post-smtp）

每個 WP 站若安裝 post-smtp plugin，本地 DB 有完整 log（含失敗原因）：

```bash
ssh WP-WEB "wp db query 'SELECT id, FROM_UNIXTIME(time) AS t, LEFT(success,80) AS status, LEFT(original_subject,40) AS subj, LEFT(original_to,40) AS recipient FROM <prefix>_post_smtp_logs ORDER BY id DESC LIMIT 20' --path=/var/www/<site>/public --allow-root"
```

`<prefix>` 從 `wp db prefix` 取得（不是固定 `wp_`）。

## 已知陷阱

- **`DELETE /v3/<domain>/envelopes` 在 `api.mailgun.net` 會回 405**：必須打 storage host。文件雖寫 `DELETE /v3/{domain_name}/envelopes`，但實際 host 必須是該網域所在的 storage region。
- **網域發信 key 操作 `bounces` / `domain disable` 會 401**：權限不足，必須改用 master key。
- **Mailgun 新帳號處於 probation 時 100 封/小時**：spam 攻擊很容易把全天額度燒光，並讓正常通知信全部 403。修完 spam 漏洞後可能還要等 probation 解除。
- **`is_disabled` 欄位透過 PUT `/domains/<name>` 設定會被靜默忽略**：API 回 200 但實際 `is_disabled` 仍為 false。要停用網域只能透過 web UI 或刪除網域。

## 參考

官方文件：https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun.md  
（這個 markdown 版本適合餵給 LLM。網頁版常被 CDN 擋。）
