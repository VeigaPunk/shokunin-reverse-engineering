#!/usr/bin/env bash
# Assimilation id-collision guard — round-50 wave-3 re-derivation (attempt 2)
# Exact guard as recorded by attempt-1: .ufo/waves/round-50/w1/AssimGuard.md
# checks 1a-1d, 2, 3. Source tree is READ-ONLY: nothing is written to the lane
# tree or to /home/vgpnk/Projects/shokuknow/merge/kaidoku/.
set -u
export TMPDIR=/fast/scratch/hyaku/kaidoku-r50/w3-ExecAssimGuard

LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
STAGED=/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md
REGISTER=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
OUT=/fast/scratch/hyaku/kaidoku-r50/w3-ExecAssimGuard/out
mkdir -p "$OUT"

stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha()   { sha256sum "$1" | cut -d' ' -f1; }

{
  echo "== guards run start: $(stamp)"
  echo "== lane tip: $(git -C "$LANE" rev-parse HEAD)"
} > "$OUT/run.log"

# ---- 1a: registry ids -------------------------------------------------------
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$LANE/corpus/SOURCES.md" \
  | grep -oE 'S[0-9]+' | sort > "$OUT/reg-ids"
rc1a=$?
# ---- 1b: staged ids ---------------------------------------------------------
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$STAGED" \
  | grep -oE 'S[0-9]+' | sort > "$OUT/staged-ids"
rc1b=$?
# ---- 1c: collisions ---------------------------------------------------------
comm -12 "$OUT/reg-ids" "$OUT/staged-ids" > "$OUT/collisions"
rc1c=$?

# ---- 3: quarantine slice ----------------------------------------------------
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  "$REGISTER" > "$OUT/quarantine-slice"
rc3=$?

# ---- 2: guard proof (indented row detection) --------------------------------
PROOF=$OUT/guard-proof
mkdir -p "$PROOF"
# registry with every col0..3 S### row removed, plus one indented fixture row
grep -vE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$LANE/corpus/SOURCES.md" > "$PROOF/SOURCES.indent.md"
printf '  | S106 | indented fixture row | docs | A |\n' >> "$PROOF/SOURCES.indent.md"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$PROOF/SOURCES.indent.md" \
  | grep -oE 'S[0-9]+' | sort > "$PROOF/reg-ids"
printf 'S106\n' > "$PROOF/staged-ids"
comm -12 "$PROOF/reg-ids" "$PROOF/staged-ids" > "$PROOF/collisions"
# column-zero-only pattern (the weaker form) on the same fixture
grep -oE '^\|[[:space:]]*S[0-9]{3,}' "$PROOF/SOURCES.indent.md" \
  | grep -oE 'S[0-9]+' | sort > "$PROOF/reg-ids-col0"
printf '' > "$PROOF/staged-ids-col0"
comm -12 "$PROOF/reg-ids-col0" "$PROOF/staged-ids-col0" > "$PROOF/collisions-col0"
rc2=$?

# ---- 1d: are the colliding ids the same source? -----------------------------
python3 - "$LANE/corpus/SOURCES.md" "$STAGED" "$OUT/reg-ids" "$OUT/collisions" \
  > "$OUT/samesource.txt" 2>&1 <<'PY'
import re, sys
reg_f, st_f, ids_f, col_f = sys.argv[1:5]
pat = re.compile(r'^\s{0,3}\|\s*(S\d{3,})\s*\|(.*)$')
def load(path):
    d = {}
    for line in open(path, encoding='utf-8', errors='replace'):
        m = pat.match(line)
        if m:
            cells = [c.strip() for c in m.group(2).split('|')]
            d[m.group(1)] = cells[0] if cells else ''
    return d
reg = load(reg_f); st = load(st_f)
ids = [l.strip() for l in open(ids_f) if l.strip()]
col = [l.strip() for l in open(col_f) if l.strip()]
same = 0
print("colliding_ids=%d" % len(col))
for i in col:
    r = reg.get(i, '<ABSENT-IN-REGISTRY>')
    s = st.get(i, '<ABSENT-IN-STAGED>')
    eq = (r == s)
    same += eq
    print("%s\teq=%s\treg=%s\tstaged=%s" % (i, "yes" if eq else "no", r[:120], s[:120]))
print("same_source_count=%d" % same)
# ids present in the registry but not in the staged file
extra = [i for i in ids if i not in st]
print("registry_ids_not_in_staged=%d" % len(extra))
if extra:
    print("  " + " ".join(extra))
PY
rc1d=$?

{
  echo
  echo "== rc: 1a=$rc1a 1b=$rc1b 1c=$rc1c 1d=$rc1d 2=$rc2 3=$rc3"
  echo "== counts"
  echo "reg-ids:        $(wc -l < "$OUT/reg-ids")  first=$(head -1 "$OUT/reg-ids") last=$(tail -1 "$OUT/reg-ids") uniq=$(sort -u "$OUT/reg-ids" | wc -l)"
  echo "staged-ids:     $(wc -l < "$OUT/staged-ids")  first=$(head -1 "$OUT/staged-ids") last=$(tail -1 "$OUT/staged-ids") uniq=$(sort -u "$OUT/staged-ids" | wc -l)"
  echo "collisions:     $(wc -l < "$OUT/collisions")  first=$(head -1 "$OUT/collisions") last=$(tail -1 "$OUT/collisions")"
  echo "quarantine:     $(wc -l < "$OUT/quarantine-slice")"
  echo "quarantine-no-Sid: $(grep -cvE 'S[0-9]+' "$OUT/quarantine-slice")"
  echo "guard-proof reg-ids: $(wc -l < "$PROOF/reg-ids") collisions: $(wc -l < "$PROOF/collisions") col0-ids: $(wc -l < "$PROOF/reg-ids-col0") col0-collisions: $(wc -l < "$PROOF/collisions-col0")"
  echo
  echo "== sha256"
  for f in reg-ids staged-ids collisions quarantine-slice samesource.txt \
           guard-proof/reg-ids guard-proof/collisions guard-proof/reg-ids-col0 \
           guard-proof/collisions-col0 guard-proof/SOURCES.indent.md; do
    printf '%s  %s\n' "$(sha "$OUT/$f")" "$f"
  done
  echo "== source file digests"
  for f in "$LANE/corpus/SOURCES.md" "$STAGED" "$REGISTER"; do
    printf '%s  %s\n' "$(sha "$f")" "$f"
  done
  echo "== guards run end: $(stamp)"
} >> "$OUT/run.log" 2>&1

cat "$OUT/run.log"
