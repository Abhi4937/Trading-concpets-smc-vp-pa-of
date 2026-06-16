import json, urllib.request, sys

PORT = sys.argv[1] if len(sys.argv) > 1 else "9333"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"C:\dev\trading_concepts\cookies.txt"

# get the browser-level websocket debugger url
ver = json.load(urllib.request.urlopen(f"http://localhost:{PORT}/json/version", timeout=5))
ws_url = ver["webSocketDebuggerUrl"]

try:
    from websocket import create_connection  # websocket-client
except ImportError:
    print("NEED websocket-client"); sys.exit(2)

ws = create_connection(ws_url, max_size=None)
ws.send(json.dumps({"id": 1, "method": "Storage.getCookies"}))
while True:
    msg = json.loads(ws.recv())
    if msg.get("id") == 1:
        break
ws.close()

cookies = msg.get("result", {}).get("cookies", [])
lines = ["# Netscape HTTP Cookie File", "# yt-dlp", ""]
auth = {"SAPISID", "__Secure-1PSID", "__Secure-3PSID", "SID", "HSID", "SSID", "LOGIN_INFO", "__Secure-1PAPISID"}
found = []
for c in cookies:
    dom = c.get("domain", "")
    if not dom:
        continue
    inc = "TRUE" if dom.startswith(".") else "FALSE"
    path = c.get("path", "/")
    sec = "TRUE" if c.get("secure") else "FALSE"
    try:
        exp = int(c.get("expires", 0)) if c.get("expires", 0) and c["expires"] > 0 else 0
    except (TypeError, ValueError):
        exp = 0
    name, val = c.get("name", ""), c.get("value", "")
    if name in auth:
        found.append(name)
    lines.append("\t".join([dom, inc, path, sec, str(exp), name, val]))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print(f"Total cookies: {len(cookies)} -> {OUT}")
yt = [c for c in cookies if "youtube" in c.get("domain", "") or "google" in c.get("domain", "")]
print(f"google/youtube cookies: {len(yt)}")
print("Auth markers present:", sorted(set(found)) or "NONE")
