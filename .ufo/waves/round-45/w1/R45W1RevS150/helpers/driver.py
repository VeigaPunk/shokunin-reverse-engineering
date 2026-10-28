#!/usr/bin/env python3
"""R45W1RevS150 receipt driver: run each check, capture stdout/exit/sha256/UTC.

Read-only on the lane tree. Writes only under $S (driver + helpers + out).
Helper python scripts are written from this file (no shell escaping), then run.
"""
import hashlib
import os
import subprocess
from datetime import datetime, timezone

S = os.environ["S"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R44 = LANE + "/.ufo/waves/round-44/w1/artifacts/R44Quarantine"
R39 = LANE + "/.ufo/waves/round-39/w2/artifacts/R39W2Quarantine"
REG = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
HOST = os.path.expanduser("~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md")
OUT = os.path.join(S, "out")
HELP = os.path.join(S, "helpers")
os.makedirs(OUT, exist_ok=True)
os.makedirs(HELP, exist_ok=True)
ENV = dict(os.environ, R44=R44, R39=R39)

HELPERS = {}

HELPERS["quote_s150.py"] = '''
import re, html, unicodedata, hashlib
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
u = html.unescape(t)
q = "\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8"
print("bytes", len(t.encode()), "sha256", hashlib.sha256(t.encode()).hexdigest())
for name, body in (("raw", t), ("html-unescaped", u), ("NFKC", unicodedata.normalize("NFKC", u))):
    print("%-15s quote=%d hint=%d shinboru_ga_nai=%d shinboru=%d"
          % (name, body.count(q), body.count("\\u30d2\\u30f3\\u30c8"),
             body.count("\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044"), body.count("\\u30b7\\u30f3\\u30dc\\u30eb")))
for v in ("\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u7121\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8",
          "\\u30b7\\u30f3\\u30dc\\u30eb\\u306e\\u306a\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8",
          "\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8", "\\u30b3\\u30c4"):
    print("variant", v, "->", u.count(v))
'''

HELPERS["heads_s150.py"] = '''
import re, html
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
def clean(x):
    return re.sub(r"<[^>]+>", "", html.unescape(x)).strip()
h2 = [clean(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.S)]
h3 = [clean(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", t, re.S)]
print("h2 count", len(h2))
for x in h2:
    print("H2:", x)
print("h3 count", len(h3))
for x in h3:
    print("H3:", x)
print("any heading contains hint-chars:", any("\\u30d2\\u30f3\\u30c8" in x for x in h2 + h3))
'''

HELPERS["escape_probe.py"] = '''
import re
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
q = "\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8"
low = "".join("\\\\u%04x" % ord(c) for c in q)
up = "".join("\\\\u%04X" % ord(c) for c in q)
print("lowercase-escape present:", low in t)
print("uppercase-escape present:", up in t)
print("escaped CJK sequences in page:", len(re.findall(r"\\\\u3[0-9a-fA-F]{3}", t)))
for k in ('"bodyMarkdown"', '"bodyHtml"', '"body_updated_at"', '"taggingsCount"', '"bodyLettersCount"'):
    print("field", k, "count", t.count(k))
'''

HELPERS["nonce_identity.py"] = '''
import re, hashlib, os
def masked(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    t = re.sub(r'nonce="[^"]*"', 'nonce="X"', t)
    return re.sub(r'data-n-css="[^"]*"', 'data-n-css="X"', t)
rows = [("r45-live", "s150-live.html"), ("r45-refetch1", "s150-refetch-1.html"),
        ("r45-refetch2", "s150-refetch-2.html"),
        ("r44-capture", os.environ["R44"] + "/s150-zenn.html"),
        ("r39-capture", os.environ["R39"] + "/zenn-s150.html")]
for name, p in rows:
    b = open(p, "rb").read()
    print("%-14s bytes=%7d nonces=%2d raw_sha=%s masked_sha=%s"
          % (name, len(b), len(re.findall(r'nonce="', b.decode("utf-8", "replace"))),
             hashlib.sha256(b).hexdigest()[:16], hashlib.sha256(masked(p).encode()).hexdigest()[:16]))
v45 = {hashlib.sha256(masked(p).encode()).hexdigest()
       for _, p in rows[:3]}
print("r45 same-day masked hashes identical:", len(v45) == 1)
pref = [hashlib.sha256(masked(p).encode()).hexdigest() for _, p in rows]
print("all five masked hashes identical:", len(set(pref)) == 1)
'''

HELPERS["r44_capture.py"] = '''
import html, hashlib, os
p = os.environ["R44"] + "/s150-zenn.html"
b = open(p, "rb").read()
t = b.decode("utf-8", "replace")
u = html.unescape(t)
q = "\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8"
print("bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())
print("quote raw", t.count(q), "unescaped", u.count(q),
      "hint", t.count("\\u30d2\\u30f3\\u30c8"))
'''

HELPERS["api_s150.py"] = '''
import json
a = json.load(open("zenn-api.json"))["article"]
bh = a["body_html"]
toc = [e.get("text", "") for e in a.get("toc", [])]
q = "\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8"
print("title", a["title"])
print("published_at", a["published_at"], "body_updated_at", a["body_updated_at"])
print("body_letters_count", a["body_letters_count"], "body_html_len", len(bh))
print("body_html quote", bh.count(q), "hint", bh.count("\\u30d2\\u30f3\\u30c8"),
      "shinboru_ga_nai", bh.count("\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044"))
print("toc entries", len(toc))
for x in toc:
    print("  TOC:", x)
print("toc contains quote:", any(q in x for x in toc),
      "toc contains hint:", any("\\u30d2\\u30f3\\u30c8" in x for x in toc))
'''

HELPERS["series_rows.py"] = '''
import re, html, json
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
u = html.unescape(t)
rows = re.findall(r"<tr[^>]*>\\s*<td>(\\u7b2c\\S+?)</td>\\s*<td><a href=\\"([^\\"]+)\\"[^>]*>([^<]*)</a>", u)
out = [{"part": p, "url": w, "title": ti} for p, w, ti in rows]
json.dump(out, open("series-rows.json", "w"), ensure_ascii=False, indent=1)
for r in out:
    print(r["part"], r["url"], r["title"])
print("rows", len(out))
for part in ("\\u7b2c6\\u56de", "\\u7b2c4\\u56de"):
    print(part, "count", u.count(part))
print("heading パターン認識のコツ count", u.count("\\u30d1\\u30bf\\u30fc\\u30f3\\u8a8d\\u8b58\\u306e\\u30b3\\u30c4"))
print("llvm-objdump lines", sum(1 for l in u.splitlines() if "llvm-objdump" in l), "occ", u.count("llvm-objdump"))
'''

HELPERS["series_sweep.py"] = '''
import json, subprocess, time
series = json.load(open("series-rows.json"))
q = "\\u30b7\\u30f3\\u30dc\\u30eb\\u304c\\u306a\\u3044\\u5834\\u5408\\u306e\\u30d2\\u30f3\\u30c8"
tot = 0
for r in series:
    aid = r["url"].rstrip("/").split("/")[-1]
    out = "api-" + aid + ".json"
    p = subprocess.run(["curl", "-sS", "--max-time", "45", "-o", out, "-w",
                        "%{http_code} %{size_download}",
                        "https://zenn.dev/api/articles/" + aid],
                       capture_output=True, text=True)
    a = json.load(open(out))["article"]
    bh = a["body_html"]
    print("%s %s http=%s quote=%d hint=%d title=%s"
          % (r["part"], aid, p.stdout.strip(), bh.count(q),
             bh.count("\\u30d2\\u30f3\\u30c8"), a["title"][:44]))
    tot += bh.count(q) + bh.count("\\u30d2\\u30f3\\u30c8")
    time.sleep(1)
print("SERIES TOTAL quote+hint =", tot)
'''

HELPERS["s113.py"] = '''
import re
t = open("s113-adb.html", encoding="utf-8", errors="replace").read()
h = re.findall(r'hreflang="([^"]*)"', t)
uniq = sorted(set(h))
narrow = sorted(set(re.findall(r'hreflang="([a-z-]*)"', t)))
print("hreflang occurrences", len(h), "unique", len(uniq))
print("unique:", uniq)
print("narrow-pattern unique", len(narrow))
print("locales excluding x-default", len([x for x in uniq if x != "x-default"]))
print("tools/adb?hl=ja occurrences", t.count("tools/adb?hl=ja"))
'''

HELPERS["s113_drift.py"] = '''
import re, sys
a = open(sys.argv[1], encoding="utf-8", errors="replace").read()
b = open("s113-adb.html", encoding="utf-8", errors="replace").read()
def mask(t):
    t = re.sub(r'nonce="[^"]*"', 'nonce="X"', t)
    return re.sub(r'data-n-css="[^"]*"', 'data-n-css="X"', t)
ma, mb = mask(a), mask(b)
print("r44 bytes", len(a), "r45 bytes", len(b), "delta", len(b) - len(a))
print("masked lens", len(ma), len(mb), "masked identical", ma == mb)
i = next((k for k in range(min(len(ma), len(mb))) if ma[k] != mb[k]), None)
if i is not None:
    print("first masked diff at", i)
    print("r44:", repr(ma[max(0, i - 100):i + 100]))
    print("r45:", repr(mb[max(0, i - 100):i + 100]))
'''

for name, body in HELPERS.items():
    with open(os.path.join(HELP, name), "w") as fh:
        fh.write(body.lstrip("\n"))

rows = []


def run(cid, desc, cmd, cwd=S, timeout=400):
    t0 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    p = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True,
                       timeout=timeout, env=ENV)
    t1 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(os.path.join(OUT, cid + ".txt"), "wb") as fh:
        fh.write(p.stdout)
    if p.stderr:
        with open(os.path.join(OUT, cid + ".stderr.txt"), "wb") as fh:
            fh.write(p.stderr)
    sha = hashlib.sha256(p.stdout).hexdigest()
    head = (p.stdout.decode("utf-8", "replace").strip().splitlines() or [""])[0][:140]
    rows.append((cid, str(p.returncode), sha, t0, t1, desc, head, cmd))
    print("%s\texit=%s\tsha=%s\t%s" % (cid, p.returncode, sha[:16], desc))
    if p.returncode not in (0, 1, 2):
        print("   stderr:", p.stderr.decode("utf-8", "replace")[:400])
    return p


def hp(name):
    return "python3 " + HELP + "/" + name


# --- register / slice -------------------------------------------------------
run("C01", "sha256 of the staged register (identity)", "sha256sum '%s'" % REG)
run("C02", "stat of the staged register (size + mtime)", "stat -c '%%s bytes mtime=%%y' '%s'" % REG)
run("C03", "re-derive the kaidoku quarantine slice and hash it",
    "awk -F'|' -v l='kaidoku' '$2 ~ l && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' '%s' > quarantine-slice && sha256sum quarantine-slice && cat quarantine-slice" % REG)
run("C04", "slice byte-identical to the round-43 artifact",
    "diff quarantine-slice %s/.ufo/waves/round-43/w1/artifacts/R43Quarantine/quarantine-slice && echo IDENTICAL" % LANE)
run("C05", "slice byte-identical to the round-44 artifact",
    "diff quarantine-slice %s/quarantine-slice && echo IDENTICAL" % R44)

# --- S150 ------------------------------------------------------------------
run("C06", "live fetch of the staged S150 URL (status, bytes, url, sha256)",
    "curl -sSL --max-time 60 -o s150-live.html -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\\n' https://zenn.dev/yasu01/articles/7370bd5d414ec4 && sha256sum s150-live.html")
run("C07", "two independent refetches (byte-size stability vs body-sha instability)",
    "for i in 1 2; do curl -sSL --max-time 60 -o s150-refetch-$i.html -w \"refetch$i http=%{http_code} bytes=%{size_download} \" https://zenn.dev/yasu01/articles/7370bd5d414ec4; sha256sum s150-refetch-$i.html | cut -d' ' -f1; done")
run("C08", "S150 quote counters: raw / html-unescaped / NFKC / kana variants", hp("quote_s150.py"))
run("C09", "S150 real heading outline (h2 + h3) and heading-set membership", hp("heads_s150.py"))
run("C10", "escaped-unicode and JSON-embedded forms of the quote", hp("escape_probe.py"))
run("C11", "nonce-masked page identity across five captures (r39, r44, r45 x3)", hp("nonce_identity.py"))
run("C12", "round-44 archived capture: independent quote counts", hp("r44_capture.py"))
run("C13", "authoritative Zenn API: body_html + Zenn-authored TOC quote counters",
    "curl -sS --max-time 45 -o zenn-api.json -w 'http=%{http_code} bytes=%{size_download}\\n' https://zenn.dev/api/articles/7370bd5d414ec4 && " + hp("api_s150.py"))
run("C14", "series position: the cited article is which installment; durable counters", hp("series_rows.py"))
run("C15", "series sweep: quote + hint across all six series articles (API bodies)", hp("series_sweep.py"), timeout=420)

# --- S113 / S117 / S136 / S147 --------------------------------------------
run("C16", "S113 adb page: fetch + hreflang census (the '17 locales' claim)",
    "curl -sSL --max-time 60 -o s113-adb.html -w 'http=%{http_code} bytes=%{size_download}\\n' https://developer.android.com/tools/adb && " + hp("s113.py"))
run("C17", "S113 drift vs the round-44 capture (is the delta content?)",
    hp("s113_drift.py") + " " + R44 + "/s113-adb.html")
run("C18", "S117 DOI resolver chain (status + Location)",
    "curl -sSI --max-time 45 https://doi.org/10.1109/SP46214.2022.9833799 -o doi-head.txt -w 'http=%{http_code}\\n' ; grep -i '^location' doi-head.txt")
run("C19", "S117 publisher body (status + bytes + sha)",
    "curl -sSL --max-time 60 -o s117-ieee.html -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\\n' https://doi.org/10.1109/SP46214.2022.9833799 && sha256sum s117-ieee.html")
run("C20", "S117 Crossref identity (title / container / issued)",
    "curl -sS --max-time 45 -o s117-crossref.json -w 'http=%{http_code} bytes=%{size_download}\\n' https://api.crossref.org/works/10.1109/SP46214.2022.9833799 && python3 -c \"import json;d=json.load(open('s117-crossref.json'))['message'];print(d['title'],'|',d['container-title'],'|',d['issued'],'|',d['DOI'])\"")
run("C21", "S136 lane locator: size, sha256, line 8, quote count",
    "cd %s && wc -c corpus/knowledge/2026-10-13-r4u-06-adb-surface.md && sha256sum corpus/knowledge/2026-10-13-r4u-06-adb-surface.md && sed -n '8p' corpus/knowledge/2026-10-13-r4u-06-adb-surface.md && grep -c '2 of 24 verbs are' corpus/knowledge/2026-10-13-r4u-06-adb-surface.md" % LANE)
run("C22", "S147 host locator: size, sha256, line 41, headings, '207 tools' count",
    "H='%s'; wc -c \"$H\" && sha256sum \"$H\" && sed -n '41p' \"$H\" && grep -n '^## ' \"$H\" && grep -c '207 tools' \"$H\"" % HOST)
run("C23", "S147 caveat test: PROVINCE client pins vs the round-carrier pin",
    "cd %s && sed -n '9p;12p' PROVINCE.md | cut -c1-330 && echo '--- carrier pin in a tool ---' && grep -n 'rea-agents@6.5.0' tools/round-28/c1-heldout-naming.py | head -1" % LANE)

# --- assimilation line ----------------------------------------------------
run("C24", "staged subjects present in corpus/knowledge/ (adoption audit)",
    "cd %s && grep -rlE '7370bd5d414ec4|9833799|developer\\.android\\.com/tools/adb|207 tools|hreflang' corpus/knowledge/ ; echo grep_exit=$?" % LANE)
run("C25", "corpus commits since the round-44 close + working-tree status",
    "cd %s && echo commits=$(git log --oneline c29360e3ba5381a5ab69e372d0d9577970f85018..HEAD -- corpus/ PROVINCE.md | wc -l) && git status --porcelain -- corpus/ PROVINCE.md | head -5 && echo status_ok" % LANE)
run("C26", "frozen paths touched in FREEZE..HEAD (directory-freeze audit)",
    "cd %s && git log --name-status --format='%%h %%s' f762b7273e3f6ca3c710bb37d5de92a4a4417aec..HEAD -- plans/round-45-claims.md tools/round-45/ ; echo lines=$(git log --format='%%h' f762b7273e3f6ca3c710bb37d5de92a4a4417aec..HEAD -- plans/round-45-claims.md tools/round-45/ | wc -l)" % LANE)
run("C27", "frozen round-45 instruments do not read the staged register (separability)",
    "cd %s && grep -rn 'S150\\|quarantine\\|absent-defect\\|shokuknow' tools/round-45/ ; echo grep_exit=$?" % LANE)
run("C28", "lane registry row count, max id, and whether a lane S150 row exists",
    "cd %s && echo rows=$(grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md) && echo max=$(grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -V | tail -1) && echo s150_hits=$(grep -c 'S150' corpus/SOURCES.md)" % LANE)
run("C29", "round-44 gate line citations resolve (r44:18,63,88 / spotcheck:89,166)",
    "cd %s && for spec in corpus/lessons/round-44.md:18 corpus/lessons/round-44.md:63 corpus/lessons/round-44.md:88 corpus/lessons/round-44-verifier-spotcheck.md:89 corpus/lessons/round-44-verifier-spotcheck.md:166; do f=${spec%%:*}; n=${spec##*:}; printf '%%s -> ' \"$spec\"; sed -n \"${n}p\" \"$f\" | cut -c1-110; done" % LANE)
run("C30", "round-44 verdict artifact re-read (the 5-row table re-verified here)",
    "cut -c1-150 %s/quarantine-verdicts.tsv" % R44)

with open(os.path.join(OUT, "receipts.tsv"), "w") as fh:
    fh.write("id\texit\tstdout_sha256\tutc_start\tutc_end\tdescription\tfirst_line\tcommand\n")
    for cid, rc, sha, t0, t1, desc, head, cmd in rows:
        fh.write("\t".join([cid, rc, sha, t0, t1, desc,
                            head.replace("\t", " "),
                            cmd.replace("\n", "\\n").replace("\t", " ")]) + "\n")
print("\nreceipts:", len(rows), "->", os.path.join(OUT, "receipts.tsv"))
