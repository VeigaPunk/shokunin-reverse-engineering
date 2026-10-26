#!/usr/bin/env bash
set -uo pipefail
S=/fast/scratch/hyaku/kaidoku-r38/R38W2SymlinkUnblob
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
export REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob"
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GEN=$L/tools/round-37/gen-squashfs.py
mkdir -p "$S/direct" "$S/rea" "$S/trees"

# ---- A. direct unblob on the two frozen carriers: what survives sanitisation on disk
for K in K1 K2; do
  C="$L/corpus/evidence/round-37/c1/$K/carrier.sqsh"
  rm -rf "$S/direct/$K"
  ~/.local/bin/unblob -e "$S/direct/$K" -f "$C" > "$S/direct/$K.stdout.json" 2> "$S/direct/$K.stderr.txt"
  echo "A $K unblob_exit=$?"
  echo "A $K links_on_disk:"
  find "$S/direct/$K" -type l -printf '   %p -> %l\n' | sed "s|$S/direct/$K|OUT|"
  echo "A $K link_entries_in_stdout_json=$(grep -c '"link_target"' "$S/direct/$K.stdout.json")"
  grep -o 'MaliciousSymlinkRemoved[^}]*}' "$S/direct/$K.stdout.json" | head -2 | sed 's/^/   diag: /'
done

# ---- B. probes: boundary cases of fix_symlink, each a BE-v4 gzip carrier
mk() { rm -rf "$S/trees/$1"; mkdir -p "$S/trees/$1"; }
# P1 in-tree relative (K2 shape)
mk P1; mkdir -p "$S/trees/P1/a" "$S/trees/P1/var/lib"
printf '#!/bin/sh\necho hi\n' > "$S/trees/P1/a/run.sh"
ln -s ../../a/run.sh "$S/trees/P1/var/lib/run-link"
# P2 escaping relative (K1 shape) + a plain file
mk P2; printf 'hello world\n' > "$S/trees/P2/hello.txt"
ln -s ../hello.txt "$S/trees/P2/link-to-hello"
# P3 symlink loop, both targets in-tree paths
mk P3; printf 'x\n' > "$S/trees/P3/keep.txt"
ln -s b "$S/trees/P3/a"; ln -s a "$S/trees/P3/b"
# P4 absolute targets: one in-image path, one outside the real root
mk P4; printf 'hello world\n' > "$S/trees/P4/hello.txt"
ln -s /hello.txt "$S/trees/P4/abs-in"; ln -s /etc/passwd "$S/trees/P4/abs-out"
# P5 dangling relative target that stays inside the tree
mk P5; mkdir -p "$S/trees/P5/docs"; printf 'y\n' > "$S/trees/P5/docs/real.txt"
ln -s docs/nothere "$S/trees/P5/dangling"

for P in P1 P2 P3 P4 P5; do
  python3 "$GEN" "$S/trees/$P" "$S/$P.sqsh" --endian be --comp gzip
  echo "B $P built rc=$? size=$(stat -c%s "$S/$P.sqsh" 2>/dev/null)"
done

# ---- C. REA extract-firmware on K1, K2 and every probe
run() { # name carrier
  local n="$1" c="$2"
  rm -rf "$S/rea/$n"
  npx -y rea-agents@6.5.0 extract-firmware --format json "$c" "$S/rea/$n" > "$S/rea/$n.json" 2> "$S/rea/$n.err"
  echo "C $n rea_exit=$?"
  python3 - "$S/rea/$n.json" "$n" <<'PY'
import json,sys
p,n=sys.argv[1],sys.argv[2]
try: d=json.load(open(p))
except Exception as e:
    print(f"   {n}: unparsable {e}"); raise SystemExit
d=d.get('data',d)
nr=d.get('normalized_result') or {}
print(f"   {n}: coverage={nr.get('coverage')} files={len(nr.get('files') or [])} "
      f"unpublished={json.dumps(nr.get('unpublished_entries'))}")
print(f"   {n}: gaps={json.dumps([g.get('kind')+':'+str(g.get('relative_path')) for g in (nr.get('extraction_gaps') or [])])}")
for dg in (nr.get('diagnostics') or []):
    r=dg.get('report') or {}
    print(f"   {n}: diag={r.get('__typename__')} link={str(r.get('link')).split('/extracted/')[-1]} target={str(r.get('target')).split('/extracted/')[-1]}")
PY
  # on-disk lstat of the published root and of the sanitised staging tree if kept
  find "$S/rea/$n" -maxdepth 6 \( -type l -o -type f \) -printf "   %n ondisk %y %P -> %l\n" 2>/dev/null | sed 's/ -> $//'
}

run K1 "$L/corpus/evidence/round-37/c1/K1/carrier.sqsh"
run K2 "$L/corpus/evidence/round-37/c1/K2/carrier.sqsh"
for P in P1 P2 P3 P4 P5; do run "$P" "$S/$P.sqsh"; done

# ---- D. direct unblob on probes: what fix_symlink did, with unblob's own log
for P in P1 P2 P3 P4 P5; do
  rm -rf "$S/direct/$P"
  ~/.local/bin/unblob -e "$S/direct/$P" -f "$S/$P.sqsh" > "$S/direct/$P.stdout.json" 2> "$S/direct/$P.stderr.txt"
  echo "D $P unblob_exit=$? links_after_sanitisation:"
  find "$S/direct/$P" -type l -printf '   %P -> %l\n' | sort
  grep -o 'MaliciousSymlinkRemoved[^}]*}' "$S/direct/$P.stdout.json" | sed 's/^/   diag: /'
  grep -i "symlink" "$S/direct/$P.stderr.txt" | head -4 | sed 's/^/   log: /'
done
echo "DONE"
