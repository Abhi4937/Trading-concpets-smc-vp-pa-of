import json, sys

# Reads agent-browser `cookies get --json` output (stdin or file) and writes a
# Netscape cookies.txt that yt-dlp can consume.
data = json.load(open(sys.argv[1], encoding="utf-8-sig")) if len(sys.argv) > 1 else json.load(sys.stdin)
cookies = data.get("data", {}).get("cookies", data.get("cookies", []))

lines = ["# Netscape HTTP Cookie File", "# Generated for yt-dlp", ""]
auth_markers = {"SAPISID", "__Secure-1PSID", "__Secure-3PSID", "SID", "HSID", "SSID", "LOGIN_INFO"}
found_auth = []
for c in cookies:
    domain = c.get("domain", "")
    if not domain:
        continue
    include_sub = "TRUE" if domain.startswith(".") else "FALSE"
    path = c.get("path", "/")
    secure = "TRUE" if c.get("secure") else "FALSE"
    exp = c.get("expires", 0)
    try:
        exp = int(exp) if exp and exp > 0 else 0
    except (TypeError, ValueError):
        exp = 0
    name = c.get("name", "")
    value = c.get("value", "")
    if name in auth_markers:
        found_auth.append(name)
    lines.append("\t".join([domain, include_sub, path, secure, str(exp), name, value]))

out = sys.argv[2] if len(sys.argv) > 2 else "cookies.txt"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {len(cookies)} cookies to {out}")
print("Auth cookies present:", sorted(set(found_auth)) or "NONE (not logged in?)")
