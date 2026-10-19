#!/usr/bin/env bash
# RV-9 re-verification (self-contained; run from anywhere).
# Audits the LIVE instrument against the frozen pre-edit artifact and re-runs the
# decisive fixtures. Evidence is written to /var/tmp/rv9-reverify/ (never /tmp).
set -u
R="$(cd "$(dirname "$0")" && pwd)"          # claims/c2/RV-9
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/var/tmp/rv9-reverify; mkdir -p "$W"
LIVE="$REPO/.ufo/gates/c1-census-v10.py"
PINNED=d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5
cd "$REPO" || exit 9

sha=$(sha256sum "$LIVE" | cut -d' ' -f1)
echo "live instrument: $sha  ($(wc -l < "$LIVE") lines, $(stat -c %y "$LIVE"))"
echo "pinned RV-9 post artifact: $(sha256sum "$R/c1-census-post.py" | cut -d' ' -f1)"
[ "$sha" = "$PINNED" ] && echo "IDENTITY: live == RV-9's verified revision" \
                       || echo "IDENTITY: live MOVED — re-audit required (expected below)"

python3 "$LIVE" > "$W/ordinary.out" 2>&1; rc=$?
echo "ordinary run: exit=$rc  sha=$(sha256sum "$W/ordinary.out" | cut -d' ' -f1)"
echo "expected at $PINNED: exit=0 sha=1db2ec31e8f8896031f1f80a2d90f7e2801af645c4f685d2c55100534d1b7cc0"
echo "--- byte-identity vs frozen pre-edit verdict ---"
python3 "$R/verdict-identity.py" "$R/pre-edit.out" "$W/ordinary.out"
echo "--- creep audit (round-1 scope-diff) ---"
python3 "$REPO/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py" "$R/c1-census-pre-edit.py" "$LIVE"
echo "--- decisive fixtures (live instrument, /var/tmp roots) ---"
python3 - "$LIVE" "$W" <<'PY'
import os, re, shutil, subprocess, sys
live, W = sys.argv[1], sys.argv[2]
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]
def fresh(n):
    d = os.path.join(W, n); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for f in FILES: shutil.copy(os.path.join(REPO, f), d)
    return d
def run(c, census, root):
    p = subprocess.run([sys.executable, census, "--root", root], capture_output=True, text=True)
    keys = [l for l in p.stdout.splitlines() if l.startswith(("UNREADABLE", "DECLARED", "VERDICT"))]
    print("[%s] exit=%d :: %s" % (c, p.returncode, " | ".join(keys)))
d = fresh("ctrl"); run("control", live, d)
d = fresh("h1"); os.remove(os.path.join(d, "SKILL.md")); run("absent-skill", live, d)
d = fresh("filler")
open(os.path.join(d, "SKILL.md"), "w").write("\n".join("plain filler %d" % i for i in range(1, 372)) + "\n")
run("per-file-collapse", live, d)
txt = open(live, encoding="utf-8").read()
for old, new in [('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
                  'PIN = re.compile(r"zzz@(\\d+\\.\\d+\\.\\d+)", re.I)'),
                 ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
                  'VER = re.compile(r"zzz6\\.\\d+\\.\\d+")'),
                 ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
                  'PTR = re.compile(r"zzzptr:(\\d+)")')]:
    assert old in txt, old[:50]; txt = txt.replace(old, new, 1)
blind = os.path.join(W, "blind.py"); open(blind, "w", encoding="utf-8").write(txt)
d = fresh("blind"); run("blind-all", blind, d)
PY
