---
name: curl-cheatsheet
description: 'Use when the user needs curl commands: HTTP methods, headers, authentication, posting JSON and form data, file downloads and uploads, following redirects, cookies, retries, and debugging APIs with verbose output from the terminal.'
---

# curl Cheatsheet — Commands That Actually Work

One page. 29 commands. Each entry tells you **what it does**, gives you **a command you can copy-paste**, and tags the scenario. No made-up flags — every command verified against real curl.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Docs: https://curl.se/docs/

---

## 🌐 Basic requests

### Simple GET
The default: fetch a URL and print the response body to stdout.
```bash
curl https://api.example.com/users
```
🏷️ `#get` `#basics`

### POST JSON
`-X` sets the method, `-H` sets headers, `-d` sends the body (`-d` implies POST).
```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"ezra","role":"engineer"}'
```
🏷️ `#post` `#json` `#api`

### PUT (replace a resource)
Full replacement of the resource at the given URL.
```bash
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"ezra","role":"senior engineer"}'
```
🏷️ `#put` `#api`

### DELETE a resource
```bash
curl -X DELETE https://api.example.com/users/1
```
🏷️ `#delete` `#api`

### PATCH (partial update)
Only the fields you send get updated.
```bash
curl -X PATCH https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com"}'
```
🏷️ `#patch` `#api`

### HEAD request (headers only)
Check a URL exists / read headers without downloading the body.
```bash
curl -I https://example.com
```
🏷️ `#head` `#inspect`

---

## 🔑 Headers & auth

### Custom headers
Send any header with `-H`; repeat it for multiple headers.
```bash
curl -H "X-API-Key: abc123" -H "Accept: application/json" \
  https://api.example.com/data
```
🏷️ `#headers` `#api-key`

### Bearer token auth
The standard way to call APIs protected by OAuth2 / JWT.
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..." \
  https://api.example.com/me
```
🏷️ `#auth` `#bearer` `#jwt`

### Basic auth
`-u user:password` builds the `Authorization: Basic ...` header for you.
```bash
curl -u admin:s3cret https://api.example.com/secure
# equivalent: -H "Authorization: Basic YWRtaW46czNjcmV0"
```
🏷️ `#auth` `#basic`

### Custom User-Agent
Some servers / WAFs behave differently depending on the client string.
```bash
curl -A "MyApp/1.0 (contact: me@example.com)" https://example.com
```
🏷️ `#headers` `#user-agent`

---

## 📤 Sending data

### POST form data (URL-encoded)
Classic HTML-form style body; `-d` already implies `-X POST`.
```bash
curl -d "name=ezra&plan=pro" https://example.com/signup
```
🏷️ `#post` `#form`

### URL-encode the data for you
`--data-urlencode` encodes special characters (spaces, `&`, `=`) safely.
```bash
curl --data-urlencode "q=hello world & more" https://example.com/search
```
🏷️ `#post` `#encoding`

### Upload a file (multipart)
`-F` builds a `multipart/form-data` request; `@` reads the file from disk.
```bash
curl -F "avatar=@me.png" -F "bio=hello world" https://example.com/upload
# add ;type=image/png after the filename to set the MIME type explicitly
```
🏷️ `#upload` `#multipart` `#file`

---

## 📥 Response handling

### Show response headers too
`-i` includes the HTTP response headers above the body.
```bash
curl -i https://example.com
```
🏷️ `#headers` `#inspect`

### Save body to a file
Lowercase `-o` saves to the filename you choose.
```bash
curl -o page.html https://example.com
```
🏷️ `#download` `#save`

### Save using the remote filename
Uppercase `-O` uses the last part of the URL as the local filename.
```bash
curl -O https://example.com/files/report.pdf   # saves as report.pdf
```
🏷️ `#download` `#save`

### Silent mode, but still show errors
`-s` hides the progress bar; `-S` makes sure real errors still print.
```bash
curl -sS https://api.example.com/data
```
🏷️ `#quiet` `#scripting`

### Measure timing and status code
`-w` prints a custom format after the transfer; `-o /dev/null` discards the body.
```bash
curl -s -o /dev/null -w "code=%{http_code} time=%{time_total}s size=%{size_download}\n" \
  https://example.com
# more variables: %{time_connect} %{speed_download} %{url_effective}
```
🏷️ `#timing` `#metrics` `#debug`

---

## 🐞 Debugging

### Verbose: see the whole conversation
`-v` shows request headers, response headers, and the TLS handshake.
```bash
curl -v https://example.com
```
🏷️ `#debug` `#verbose`

### Full trace (ASCII)
`--trace-ascii` dumps everything including connection internals; `-` means stdout.
```bash
curl --trace-ascii - https://example.com 2>&1 | head -40
```
🏷️ `#debug` `#trace`

### Which HTTP version was negotiated?
`-w %{http_version}` tells you if you got HTTP/1.1, HTTP/2, or HTTP/3.
```bash
curl -s -o /dev/null -w "HTTP version: %{http_version}\n" https://example.com
# force one: curl --http2 https://example.com
```
🏷️ `#debug` `#http2`

### Skip TLS certificate verification (debug only)
Useful against self-signed dev servers. ⚠️ Never in production — it disables MITM protection.
```bash
curl -k https://self-signed.example.com   # ⚠️ debug only, never in scripts that matter
```
🏷️ `#tls` ⚠️ `#debug-only`

---

## ⬇️ Downloads & rate limiting

### Resume an interrupted download
`-C -` auto-detects how much you already have and continues from there.
```bash
curl -C - -O https://example.com/big.iso
```
🏷️ `#download` `#resume`

### Limit download speed
`--limit-rate` accepts K/M/G suffixes — be nice to shared servers.
```bash
curl --limit-rate 500K -O https://example.com/big.iso
```
🏷️ `#download` `#throttle`

### Retry on failure
`--retry` retries transient failures; `--retry-delay` waits between attempts.
```bash
curl --retry 5 --retry-delay 3 -O https://example.com/file.zip
```
🏷️ `#download` `#retry` `#robust`

---

## 🍪 Cookies & sessions

### Save cookies from a login
`-c` writes a cookie jar file after the request (e.g. after logging in).
```bash
curl -c cookies.txt -d "user=ezra&pass=s3cret" https://example.com/login
```
🏷️ `#cookies` `#session` `#login`

### Send saved cookies
`-b` reads the cookie jar and sends it with the request.
```bash
curl -b cookies.txt https://example.com/dashboard
# -b "name=value" also works for a one-off cookie without a file
```
🏷️ `#cookies` `#session`

---

## 🔀 Proxy

### Route through an HTTP proxy
```bash
curl -x http://proxy.example.com:8080 https://example.com
# with auth: -x http://user:pass@proxy.example.com:8080
```
🏷️ `#proxy` `#http`

### Route through a SOCKS5 proxy
Common for SSH tunnels (`ssh -D 1080 host`) and local proxies.
```bash
curl -x socks5://127.0.0.1:1080 https://example.com
```
🏷️ `#proxy` `#socks5`

---

## Reference

Official documentation: https://curl.se/docs/

## Contributing

Found a wrong command, an outdated flag, or a bad translation? Pull requests are welcome — keep entries to the format above (heading / one line / code block / tags) and verify every command with a real curl before submitting.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
