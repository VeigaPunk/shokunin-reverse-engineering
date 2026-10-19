#!/bin/bash
# EX-21 before-probes: reproduce (a)(b)(c)(d) residuals at revision 7cd19c3c…
# Usage: bash before-probes.sh <tool.py> <outdir>
set -u
TOOL="$1"; OUT="$2"
mkdir -p "$OUT"
S=$(mktemp -d /var/tmp/ex21/probe-XXXXXX)
echo "tool=$TOOL sha=$(sha256sum "$TOOL" | cut -d' ' -f1)"
echo "scratch=$S"

echo "=== (a) sidecar path not scope-checked ==="
printf 'victim bytes\n' > "$S/vic.sha256"
before_a=$(sha256sum "$S/vic.sha256" | cut -d' ' -f1)
python3 "$TOOL" capture --out "$S/vic" --paths "$S/vic.sha256" --label probe-a > "$OUT/a.stdout" 2> "$OUT/a.stderr"
rc_a=$?
after_a=$(sha256sum "$S/vic.sha256" | cut -d' ' -f1)
echo "exit=$rc_a before=$before_a after=$after_a"
if [ "$before_a" != "$after_a" ]; then echo "A-VERDICT: SIDECAR-CLOBBERED (measured file destroyed, exit $rc_a)"; else echo "A-VERDICT: intact"; fi
echo "--- stdout"; cat "$OUT/a.stdout"; echo "--- stderr"; cat "$OUT/a.stderr"
{ echo "exit=$rc_a"; echo "before=$before_a"; echo "after=$after_a"; cat "$OUT/a.stdout"; echo "--stderr--"; cat "$OUT/a.stderr"; } > "$OUT/a.transcript"

echo
echo "=== (b) out.parent.mkdir outside the guarded try ==="
printf 'a regular file\n' > "$S/pfile.txt"
python3 "$TOOL" capture --out "$S/pfile.txt/sub/r.txt" --paths "$S/pfile.txt" --label probe-b > "$OUT/b.stdout" 2> "$OUT/b.stderr"
rc_b=$?
echo "exit=$rc_b"
echo "--- stderr"; cat "$OUT/b.stderr"
if grep -q Traceback "$OUT/b.stderr"; then echo "B-VERDICT: TRACEBACK (exit $rc_b, outside the declared map)"; else echo "B-VERDICT: no traceback"; fi
{ echo "exit=$rc_b"; echo "--stdout--"; cat "$OUT/b.stdout"; echo "--stderr--"; cat "$OUT/b.stderr"; } > "$OUT/b.transcript"

echo
echo "=== (b2) out parent that is a nonexistent dir chain under a file ==="
python3 "$TOOL" capture --out "$S/pfile.txt/deep/er/r.txt" --paths "$S/pfile.txt" > "$OUT/b2.stdout" 2> "$OUT/b2.stderr"
echo "exit=$?"; cat "$OUT/b2.stderr" | head -5

echo
echo "=== (c) coverage gate counts stanzas, not distinct paths ==="
# build a real v2 receipt over ONE path via the tool itself, then pad it 5x
printf 'cov fixture\n' > "$S/cov.conf"
python3 "$TOOL" capture --out "$S/cov-1.txt" --paths "$S/cov.conf" --label probe-c > "$OUT/c1.stdout" 2>&1
python3 - "$S" <<'PY'
import sys, re, pathlib
S = pathlib.Path(sys.argv[1])
src = (S / "cov-1.txt").read_text()
# split into header and one stanza
lines = src.splitlines(keepends=True)
# find first PATH: line
i = next(i for i, l in enumerate(lines) if l.startswith("PATH:"))
header = "".join(lines[:i])
stanza = "".join(lines[i:])
(S / "cov-5x.txt").write_text(header + stanza * 5)
PY
python3 "$TOOL" verify "$S/cov-5x.txt" --live --require-paths 5 > "$OUT/c5x.stdout" 2> "$OUT/c5x.stderr"
rc_c5=$?
echo "5x-duplicate --require-paths 5 exit=$rc_c5"
cat "$OUT/c5x.stdout"; echo "--- stderr"; cat "$OUT/c5x.stderr"
grep -c "REFERENCE-COVERAGE" "$OUT/c5x.stdout" "$OUT/c5x.stderr" | sed 's/^/coverage-line-count: /'
if [ "$rc_c5" = "0" ]; then echo "C-VERDICT: GATE-PASSED-ON-DUPLICATES (exit 0, 1 distinct path, 4 custody paths unexamined)"; else echo "C-VERDICT: exit $rc_c5"; fi
{ echo "exit=$rc_c5"; cat "$OUT/c5x.stdout"; echo "--stderr--"; cat "$OUT/c5x.stderr"; } > "$OUT/c5x.transcript"

echo
echo "=== (d) both-sides-absent MATCH semantics ==="
printf 'gone fixture\n' > "$S/gone.conf"
python3 "$TOOL" capture --out "$S/gone-a.txt" --paths "$S/gone.conf" --label probe-d-a > /dev/null 2>&1
rm -f "$S/gone.conf"
python3 "$TOOL" capture --out "$S/gone-b.txt" --paths "$S/gone.conf" --label probe-d-b > /dev/null 2>&1
python3 "$TOOL" verify "$S/gone-a.txt" "$S/gone-b.txt" > "$OUT/d.stdout" 2>&1
rc_d=$?
echo "both-absent receipt-vs-receipt exit=$rc_d"
cat "$OUT/d.stdout"
{ echo "exit=$rc_d"; cat "$OUT/d.stdout"; } > "$OUT/d.transcript"

echo
echo "=== (e) unsupported: does the guard see the sidecar's inode alias? ==="
printf 'alias fixture\n' > "$S/real.conf"
ln "$S/real.conf" "$S/alias.out"
python3 "$TOOL" capture --out "$S/alias.out" --paths "$S/real.conf" > "$OUT/e.stdout" 2> "$OUT/e.stderr"
echo "hardlink-alias exit=$? (expect 2 refused)"; cat "$OUT/e.stderr"

echo
echo "DONE scratch=$S"
