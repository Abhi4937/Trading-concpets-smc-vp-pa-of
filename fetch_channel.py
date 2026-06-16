import os, re, json, glob, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# config JSON: {"out": "<abs folder>", "skip_regex": "...optional...",
#               "playlists": [["01_Folder","Label","PLAYLIST_ID"], ...]}
CFG = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = CFG["out"]
TMP = os.path.join(OUT, "_vtt")
os.makedirs(TMP, exist_ok=True)
SKIP_RE = re.compile(CFG["skip_regex"], re.I) if CFG.get("skip_regex") else None

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

def safe(name):
    name = re.sub(r"[^\w\s\-\.&+()]", "", name).strip()
    return re.sub(r"\s+", " ", name)[:90]

def clean_vtt(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out, last = [], None
    for ln in lines:
        s = ln.strip()
        if not s or s == "WEBVTT" or s.startswith("Kind:") or s.startswith("Language:"):
            continue
        if "-->" in s or re.match(r"^\d+$", s):
            continue
        s = re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip()
        if not s or s == last:
            continue
        out.append(s); last = s
    return re.sub(r"\s+", " ", " ".join(out)).strip()

def enumerate_playlist(pid):
    url = f"https://www.youtube.com/playlist?list={pid}"
    r = run(["python", "-m", "yt_dlp", "--flat-playlist", "-J", "--no-warnings", url])
    if r.returncode != 0:
        print("  ENUM FAIL:", r.stderr[-300:]); return []
    data = json.loads(r.stdout)
    return [(e.get("id"), e.get("title") or "") for e in data.get("entries", []) if e.get("id")]

def fetch_subs(vid):
    for f in glob.glob(os.path.join(TMP, "*")):
        try: os.remove(f)
        except OSError: pass
    url = f"https://www.youtube.com/watch?v={vid}"
    cmd = ["python", "-m", "yt_dlp", "--skip-download", "--ignore-no-formats-error",
           "--write-subs", "--write-auto-subs", "--sub-langs", "en.*,en-orig",
           "--sub-format", "vtt", "--no-warnings", "--sleep-requests", "1",
           "-o", os.path.join(TMP, "%(id)s.%(ext)s")]
    ck = CFG.get("cookies")
    if ck:
        cmd += ["--cookies", ck]
    cmd.append(url)
    run(cmd)
    vtts = glob.glob(os.path.join(TMP, "*.vtt"))
    if not vtts:
        return None
    vtts.sort(key=lambda p: os.path.getsize(p), reverse=True)
    return clean_vtt(vtts[0])

def main():
    index = [f"# {os.path.basename(OUT)} — Transcripts\n"]
    seen, stats = set(), {}
    for folder, label, pid in CFG["playlists"]:
        outdir = os.path.join(OUT, folder)
        os.makedirs(outdir, exist_ok=True)
        vids = enumerate_playlist(pid)
        print(f"\n=== {label}: {len(vids)} videos ===")
        index.append(f"\n## {label}\n")
        kept = skipped = nosub = n = 0
        for vid, title in vids:
            if SKIP_RE and SKIP_RE.search(title):
                skipped += 1; continue
            n += 1; tag = f"{n:03d}"
            if vid in seen:
                index.append(f"- {title}  _(dup)_"); kept += 1; continue
            seen.add(vid)
            if glob.glob(os.path.join(outdir, f"*[[]{vid}[]].txt")):
                kept += 1; index.append(f"- {title}  (saved)")
                print(f"  [{tag}] skip (exists)  {title[:55]}"); continue
            txt = fetch_subs(vid)
            if not txt:
                nosub += 1; index.append(f"- (no captions) {title}")
                print(f"  [{tag}] NO SUBS: {title[:55]}"); continue
            with open(os.path.join(outdir, f"{tag} - {safe(title)} [{vid}].txt"), "w", encoding="utf-8") as f:
                f.write(f"{title}\nhttps://www.youtube.com/watch?v={vid}\n\n{txt}\n")
            kept += 1; index.append(f"- {title}  ({len(txt.split())} words)")
            print(f"  [{tag}] {len(txt.split()):5d}w  {title[:55]}")
        stats[label] = dict(total=len(vids), kept=kept, skipped=skipped, nosub=nosub)
    open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(index))
    print("\n=== SUMMARY ===")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
