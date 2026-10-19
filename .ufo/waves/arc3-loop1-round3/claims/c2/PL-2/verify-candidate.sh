#!/usr/bin/env bash
# PL-2 (arc3-loop1-round3, chain c2) — custody-pair hardening injection matrix.
# Re-runnable evidence: runs the four named injections + the selftest + the live
# pair against whatever tool revision it is given, and prints a plain transcript.
# It writes nothing under the custody paths (read-only capture) and nothing
# under /tmp (standing EDQUOT rule).
#
#   usage: verify-candidate.sh <custody-pair.py> <outdir>
set -u
TOOL=${1:?usage: verify-candidate.sh <tool.py> <outdir>}
OUT=${2:?usage: verify-candidate.sh <tool.py> <outdir>}
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
FX=$(mktemp -d /var/tmp/pl2-matrix-XXXXXX)
mkdir -p "$OUT"
cd "$FX"

echo "### tool: $TOOL"
echo "### sha256=$(sha256sum "$TOOL" | cut -d' ' -f1)"
echo "### scratch: $FX   utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo
echo "### L0 selftest (scratch base exists)"
mkdir -p "$FX/self"
python3 "$TOOL" selftest --scratch "$FX/self" >l0.out 2>&1; echo "exit=$?"; tail -1 l0.out

echo
echo "### L1 D6 — selftest --scratch <missing dir> (declared class: USAGE 2)"
python3 "$TOOL" selftest --scratch "$FX/nope" >l1.out 2>l1.err; echo "exit=$?"
echo "stderr: $(head -1 l1.err)"
echo "traceback_lines=$(grep -c Traceback l1.err || true)"

echo
echo "### L2 D2a — blocked parent dir (declared class: UNEVALUABLE 14, never MATCH)"
mkdir -p blocked_dir; printf 'inner\n' > blocked_dir/inner.txt; chmod 000 blocked_dir
python3 "$TOOL" capture --out blocked-pre.txt --paths blocked_dir/inner.txt >l2a.out 2>&1; echo "capture exit=$?"
grep -E "EXISTS|STAT-ERROR" blocked-pre.txt
python3 "$TOOL" verify blocked-pre.txt --live >l2b.out 2>&1; echo "verify exit=$?"
grep -E "VERDICT|CUSTODY_PAIR_VERIFY" l2b.out
chmod 755 blocked_dir

echo
echo "### L3 D2b — chmod-000 regular file (declared class: UNEVALUABLE 14, receipt written)"
printf 'victim\n' > victim.txt; chmod 000 victim.txt
python3 "$TOOL" capture --out victim-hidden.txt --paths victim.txt >l3.out 2>l3.err; echo "capture exit=$?"
if [ -f victim-hidden.txt ]; then grep -E "EXISTS|READ-ERROR" victim-hidden.txt; else echo "no receipt written; stderr tail: $(tail -1 l3.err)"; fi
chmod 644 victim.txt
python3 "$TOOL" capture --out victim-open.txt --paths victim.txt >/dev/null 2>&1; echo "control capture exit=$?"

echo
echo "### L4 D2-parsed — reference RECEIPT carries the unreadable stanza (parser arm)"
grep -v "^SHA256:" victim-open.txt > ref-hidden.txt
printf 'READ-ERROR: [Errno 13] Permission denied: victim.txt\n' >> ref-hidden.txt
python3 "$TOOL" verify ref-hidden.txt victim-open.txt >l4.out 2>&1; echo "exit=$?"
grep -E "VERDICT|CUSTODY_PAIR_VERIFY" l4.out

echo
echo "### L5 D3 — 1-of-5 canonical receipt: plain (declared default) and --require-paths 5 (gate)"
python3 - <<'PY'
src="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt"
text=open(src).read(); head=text.split("\nPATH: ",1)[0]; parts=text.split("\nPATH: ")[1:]
assert len(parts)==5, "expected 5 stanzas"
open("one-of-five.txt","w").write(head+"\nPATH: "+parts[0]+"\n")
PY
python3 "$TOOL" verify one-of-five.txt --live >l5a.out 2>&1; echo "plain exit=$?"; tail -1 l5a.out
python3 "$TOOL" verify one-of-five.txt --live --require-paths 5 >l5b.out 2>&1; echo "gated exit=$?"
grep -E "REFERENCE-COVERAGE|USAGE" l5b.out | head -2

echo
echo "### L6 write guard — scoped clobber and hardlink alias (declared class: USAGE 2, bytes unchanged)"
printf 'scoped fixture bytes\n' > scoped.conf
s0=$(sha256sum scoped.conf | cut -d' ' -f1)
python3 "$TOOL" capture --out scoped.conf --paths scoped.conf >l6a.out 2>&1; echo "scoped exit=$?"; head -1 l6a.out
s1=$(sha256sum scoped.conf | cut -d' ' -f1); echo "scoped unchanged=$([ "$s0" = "$s1" ] && echo YES || echo NO)"
printf 'hardlink fixture\n' > hl-a.conf; ln hl-a.conf hl-b.txt
h0=$(sha256sum hl-a.conf | cut -d' ' -f1)
python3 "$TOOL" capture --out hl-b.txt --paths hl-a.conf >l6b.out 2>&1; echo "hardlink exit=$?"; head -1 l6b.out
h1=$(sha256sum hl-a.conf | cut -d' ' -f1); echo "hardlink target unchanged=$([ "$h0" = "$h1" ] && echo YES || echo NO)"

echo
echo "### L7 live pair over the 5 custody paths (read-only) + coverage gate"
python3 "$TOOL" capture --out "$OUT/live-pre.txt" --label pl2-live-pre >l7a.out 2>&1; echo "pre exit=$?"; grep CUSTODY_PAIR_CAPTURE l7a.out
python3 "$TOOL" capture --out "$OUT/live-post.txt" --label pl2-live-post >l7b.out 2>&1; echo "post exit=$?"; grep CUSTODY_PAIR_CAPTURE l7b.out
python3 "$TOOL" verify "$OUT/live-pre.txt" "$OUT/live-post.txt" >l7c.out 2>&1; echo "pair exit=$?"; tail -1 l7c.out
python3 "$TOOL" verify "$OUT/live-pre.txt" "$OUT/live-post.txt" --require-paths 5 >l7d.out 2>&1; echo "pair+gate exit=$?"; tail -1 l7d.out
grep -m1 "# tool:" "$OUT/live-pre.txt"

echo
echo "### L8 v1 controls (EX-35 fixtures) — sha256 contract preserved"
for f in "$REPO"/.ufo/waves/arc3-loop1-round2/claims/c3/EX-35/fixtures/*.txt; do
  n=$(basename "$f")
  python3 "$TOOL" verify "$f" --live >"l8-$n.out" 2>&1; rc=$?
  echo "$n exit=$rc :: $(grep -E 'CUSTODY_PAIR_VERIFY|USAGE:' "l8-$n.out" | head -1 | cut -c1-88)"
done

echo
echo "### L9 custody digests after the whole matrix (round-1 pins: 16f496e6.., 38d2a1d0.., 8cbacd48.., 7d2ca28a.., 6c6be761..; path 3 carries the recorded operator drift)"
sha256sum ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile | sed 's|/home/vgpnk|~|'