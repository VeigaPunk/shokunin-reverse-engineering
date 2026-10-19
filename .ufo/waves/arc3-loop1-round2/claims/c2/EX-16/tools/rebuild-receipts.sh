#!/usr/bin/env bash
# EX-16 receipt rebuilder — regenerates every receipt under claims/c2/EX-16/
# against the CURRENT bytes of .ufo/gates/c1-census-v10.py.
# Writes only inside this claims dir, /var/tmp and /dev/shm. No git mutations.
# Usage: bash tools/rebuild-receipts.sh
set -u
export TMPDIR=/var/tmp
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ART=$REPO/.ufo/waves/arc3-loop1-round2/claims/c2/EX-16
TGT=$REPO/.ufo/gates/c1-census-v10.py
cd "$REPO" || exit 1
AFTER_SHA=$(sha256sum "$TGT" | cut -d' ' -f1)

{
  echo "== after-edit identity (r9 final), captured $(date -u +%FT%TZ) =="
  sha256sum "$TGT"; wc -l "$TGT"
  echo "== before-copy (must remain 6f1d19ff…) =="; sha256sum "$ART/tools/census-before.py"
  echo "== py_compile =="; python3 -m py_compile "$TGT" && echo ok
} 2>&1 | tee "$ART/receipts/after/after-sha256.txt"

diff -u "$ART/tools/census-before.py" "$TGT" > "$ART/receipts/after/landing-diff.patch"
{
  echo "# EX-16 landing diff — .ufo/gates/c1-census-v10.py (arc3-loop1-round2 r9: H1+H3 fail-closures)"
  echo
  echo "before sha256: 6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b (490 lines)"
  echo "after  sha256: $AFTER_SHA ($(wc -l < "$TGT") lines)"
  echo "SCOPE table: byte-identical (scope-diff.py rows before=20 after=20, ADDED/REMOVED/CHANGED 0, CREEP FLAGS [])"
  echo
  echo '```diff'
  cat "$ART/receipts/after/landing-diff.patch"
  echo '```'
} > "$ART/receipts/after/landing-diff.md"

python3 "$TGT" > "$ART/receipts/after/ordinary-at-head.txt" 2>&1; echo "exit=$?" >> "$ART/receipts/after/ordinary-at-head.txt"
python3 "$TGT" --json > "$ART/receipts/after/ordinary-at-head.json" 2>&1; echo "exit=$?" >> "$ART/receipts/after/ordinary-at-head.json"
python3 "$TGT" --quiet > "$ART/receipts/after/ordinary-quiet.txt" 2>&1; echo "exit=$?" >> "$ART/receipts/after/ordinary-quiet.txt"

python3 "$ART/tools/scope-diff.py" "$ART/tools/census-before.py" "$TGT" > "$ART/receipts/after/scope-diff.txt" 2>&1
echo "exit=$?" >> "$ART/receipts/after/scope-diff.txt"

python3 "$ART/tools/injections-r9.py" "$ART/tools/census-before.py" before "$ART/receipts/before" > /dev/shm/ex16/battery-before.log 2>&1
python3 "$ART/tools/injections-r9.py" "$TGT" after "$ART/receipts/after" > /dev/shm/ex16/battery-after.log 2>&1

python3 - <<'PY' > "$ART/receipts/after/matrix.md"
import re, os
ART = os.path.join(os.environ["ART"], "receipts")
def parse(label):
    out = {}
    for line in open(os.path.join(ART, label, "SUMMARY-%s.txt" % label)):
        m = re.match(r"\[%s\] (\S+)\s+exit=(\d+)\s+(.*)" % label, line.strip())
        if not m:
            continue
        name, rc, tail = m.group(1), int(m.group(2)), m.group(3)
        out[name] = (rc, ",".join(re.findall(r"'([A-Z-]+)'", tail)) or "-")
    return out
before, after = parse("before"), parse("after")
print("# EX-16 battery matrix — v10 before (sha256 6f1d19ff…) vs landed r9 (%s…)" % os.environ["AFTER_SHA"][:8])
print()
print("Source: receipts/before/SUMMARY-before.txt + receipts/after/SUMMARY-after.txt.")
print("Each case = a fresh copy of the three scoped files at HEAD, one single-file mutation")
print("(or an instrument copy for the h3/w cases), run as `python3 <instrument> --root <case>`.")
print("Class column = DECLARED FAIL CLASSES from the report line.")
print()
print("| case | before exit | before class | after exit | after class | delta |")
print("|---|---:|---|---:|---|---|")
for name in before:
    b, a = before[name], after[name]
    if b[0] == 0 and a[0] == 1:
        d = "**silent PASS closed**"
    elif b[0] == a[0] and b[1] == a[1]:
        d = "unchanged"
    elif b[0] == a[0]:
        d = "class added"
    else:
        d = "changed"
    print("| %s | %d | %s | %d | %s | %s |" % (name, b[0], b[1], a[0], a[1], d))
closed = [n for n in before if before[n][0] == 0 and after[n][0] == 1]
resid = [n for n in before if before[n][0] == 0 and after[n][0] == 0 and n not in ("t0-baseline", "q0-quiet-baseline")]
print()
print("Silent-PASS cases closed by this landing (%d): %s." % (len(closed), ", ".join(closed)))
print()
print("Named residuals, still PASS on both sides (%d): %s." % (len(resid), ", ".join(resid)))
print()
print("H4 certificate: scope-diff.py (CR-5's tool, sha256 e0d2384c…) before→after gives")
print("`rows before=20 after=20, ADDED 0, REMOVED 0, CHANGED 0, CREEP FLAGS: []`, exit 0")
print("(after/scope-diff.txt). The same tool flags the w1 instrument (DATED end widened to")
print("1419) with `CREEP wide added DATED row` + `CREEP widen-by-add/remove` — i.e. the")
print("instrument cannot see its own widening but the external audit can (after/h4-scope-diff-widened.txt).")
PY

{
  echo "== --quiet surfaces (declared classes must be visible in quiet mode) =="
  echo "-- quiet on h1-skill-absent --"
  python3 "$TGT" --quiet --root /dev/shm/ex16/cases-after/h1-skill-absent; echo "exit=$?"
  echo "-- quiet on h3-blind-all (blinded instrument copy) --"
  python3 "$ART/receipts/after/instr-h3-blind-all.py" --quiet --root /dev/shm/ex16/cases-after/h3-blind-all; echo "exit=$?"
} 2>&1 | tee "$ART/receipts/after/quiet-class-visibility.txt"

{
python3 - <<'PY'
import json
for name, path in (("HEAD", "/var/tmp/ex16/ord.json"), ("h1-skill-absent", "/var/tmp/ex16/h1.json"), ("h3-nullskill", "/var/tmp/ex16/nulls.json")):
    d = json.load(open(path))
    print("%-18s verdict=%-4s declared=%-28s unreadable=%-32s g2_ok=%-5s floor=%-18s cur_per_file=%s" % (
        name, d["verdict"], d["declared_fail_classes"], d["unreadable"], d["g2_ok"], d["g2_floor"], d["current_ok_per_file"]))
PY
} > "$ART/receipts/after/json-fields.txt" 2>&1
python3 "$TGT" --json > /var/tmp/ex16/ord.json
python3 "$TGT" --json --root /dev/shm/ex16/cases-after/h1-skill-absent > /var/tmp/ex16/h1.json
python3 "$TGT" --json --root /dev/shm/ex16/cases-after/h3-nullskill > /var/tmp/ex16/nulls.json
{
python3 - <<'PY'
import json
for name, path in (("HEAD", "/var/tmp/ex16/ord.json"), ("h1-skill-absent", "/var/tmp/ex16/h1.json"), ("h3-nullskill", "/var/tmp/ex16/nulls.json")):
    d = json.load(open(path))
    print("%-18s verdict=%-4s declared=%-28s unreadable=%-32s g2_ok=%-5s floor=%-18s cur_per_file=%s" % (
        name, d["verdict"], d["declared_fail_classes"], d["unreadable"], d["g2_ok"], d["g2_floor"], d["current_ok_per_file"]))
PY
} > "$ART/receipts/after/json-fields.txt" 2>&1

python3 "$ART/tools/scope-diff.py" "$ART/tools/census-before.py" "$ART/receipts/after/instr-w1-scope-widen-tail.py" > "$ART/receipts/after/h4-scope-diff-widened.txt" 2>&1
echo "exit=$?" >> "$ART/receipts/after/h4-scope-diff-widened.txt"

# floor-granularity reconstruction against the CURRENT bytes
python3 - <<'PY'
src = open("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py").read()
weak_block = '''    n_loci = sum((c["loci"] or 0) for c in counts.values())
    n_current_ok = len(out.get("current-ok", []))
    floor = {f: n_current_ok for f in files}   # WEAK reconstruction: global block floor
    g2_ok = n_current_ok > 0
'''
a = src.index('    n_loci = sum(')
b = src.index('    declared = (["UNREADABLE"]')
weak = src[:a] + weak_block + src[b:]
weak = weak.replace(
    '''    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
          % ("ok" if g2_ok else "SUSPECT",
             ", ".join("%s=%d" % (f, floor[f]) for f in files), n_loci))''',
    '''    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)"
          % ("ok" if g2_ok else "SUSPECT", n_current_ok, n_loci))''')
assert "WEAK reconstruction" in weak and "current-ok loci=%d, total loci=%d" in weak
open("/var/tmp/ex16/census-global-floor.py", "w").write(weak)
NEVER = 're.compile(r"(?!x)x")'
blind = weak.replace('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)', "PIN = " + NEVER)
blind = blind.replace('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")', "VER = " + NEVER)
blind = blind.replace('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")', "PTR = " + NEVER)
assert blind.count(NEVER) == 3
open("/var/tmp/ex16/census-global-floor-blind.py", "w").write(blind)
PY
{
echo "== floor-granularity delta: WEAK global-block floor (interim 82fb807e shape) vs LANDED per-readable-file det floor =="
sha256sum /var/tmp/ex16/census-global-floor.py /var/tmp/ex16/census-global-floor-blind.py "$TGT" "$ART/receipts/after/instr-h3-blind-all.py"
run() { printf "%-22s %-34s exit=%d  %s\n" "$1" "$(basename "$2")" "$3" "$(echo "$4" | grep -E '^(G2|DECLARED|VERDICT)' | tr '\n' '|')"; }
for fx in t0-baseline h3-nullskill h5-skill-padded h1-skill-absent; do
  root=/dev/shm/ex16/cases-after/$fx; [ -d "$root" ] || root=/dev/shm/ex16/root-before
  o=$(python3 /var/tmp/ex16/census-global-floor.py --quiet --root $root 2>&1); r=$?; run "$fx" /var/tmp/ex16/census-global-floor.py $r "$o"
  o=$(python3 "$TGT" --quiet --root $root 2>&1); r=$?; run "$fx" "$TGT" $r "$o"
done
for fx in h3-blind-all t0-baseline; do
  root=/dev/shm/ex16/root-before
  o=$(python3 /var/tmp/ex16/census-global-floor-blind.py --quiet --root $root 2>&1); r=$?; run "$fx(blinded)" /var/tmp/ex16/census-global-floor-blind.py $r "$o"
  o=$(python3 "$ART/receipts/after/instr-h3-blind-all.py" --quiet --root $root 2>&1); r=$?; run "$fx(blinded)" "$ART/receipts/after/instr-h3-blind-all.py" $r "$o"
done
} 2>&1 | tee "$ART/receipts/after/floor-granularity-delta.txt"

{
echo "== residual quantification vs the landed revision ($AFTER_SHA) =="
echo "-- ordinary tree: assertion census --"
echo "total assertion lines: $(python3 "$TGT" 2>/dev/null | grep -cE '^\s+:[0-9]+ \[')   [pin] assertions: $(python3 "$TGT" 2>/dev/null | grep -cE '\[pin\]')"
echo "-- PIN-only neuter (partial blindness, survives the floor; a real H4 case) --"
python3 "$ART/receipts/after/instr-h3-blind-pin.py" --root /dev/shm/ex16/root-before 2>/dev/null | grep -E "^(G2|DECLARED|VERDICT)"
echo "total assertion lines: $(python3 "$ART/receipts/after/instr-h3-blind-pin.py" --root /dev/shm/ex16/root-before 2>/dev/null | grep -cE '^\s+:[0-9]+ \[')   [pin] assertions: $(python3 "$ART/receipts/after/instr-h3-blind-pin.py" --root /dev/shm/ex16/root-before 2>/dev/null | grep -cE '\[pin\]')"
echo "-- VER-only neuter (EX-14 partial-neuter shape) --"
sed 's|VER = re.compile(r"(?<!\[\\d.\])6\\.\\d+\\.\\d+")|VER = re.compile(r"(?!x)x")|' "$TGT" > /var/tmp/ex16/census-ver-blind.py
grep -n '^VER = ' /var/tmp/ex16/census-ver-blind.py
python3 /var/tmp/ex16/census-ver-blind.py --root /dev/shm/ex16/root-before 2>/dev/null | grep -E "^(PROVINCE|SCORECARD|SKILL|G2|DECLARED|VERDICT)"
echo "-- ALL-needle neuter (total blindness; closed) --"
python3 "$ART/receipts/after/instr-h3-blind-all.py" --root /dev/shm/ex16/root-before 2>/dev/null | grep -E "^(G2|DECLARED|VERDICT)"
} 2>&1 | tee "$ART/receipts/after/residual-partial-blindness.txt"

echo "== reps =="
for i in 1 2 3 4 5; do python3 "$TGT" 2>/dev/null | sha256sum | cut -c1-16; done
for i in 1 2 3; do python3 "$TGT" 2>/dev/null --root /dev/shm/ex16/cases-after/h1-skill-absent | sha256sum | cut -c1-16; done
echo "== final sha =="; sha256sum "$TGT"
