#!/usr/bin/env bash
# receipt-run.sh -- re-runs the R50-C1 layout recon probes and records exit code and
# stdout sha256 per probe. Vendor bytes stay in SCRATCH (never copied to the lane).
# Usage: receipt-run.sh SCRATCH SEAT_DIR   (SCRATCH holds img/ and ctl/ from the recon)
set -u
SCRATCH="$1"; SEAT="$2"
T="$SEAT/tools/round-50"; R="$SEAT/receipts"; mkdir -p "$R"
REA_SQFS_LIST=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/sqfs-list.py
LOG="$R/receipts.tsv"; : > "$LOG"
run() { # id, outname, command...
  local id="$1" out="$2"; shift 2
  local start; start=$(date -u +%FT%TZ)
  "$@" > "$R/$out" 2> "$R/$out.stderr"; local rc=$?
  local sha; sha=$(sha256sum "$R/$out" | cut -d' ' -f1)
  printf '%s\t%s\t%s\trc=%s\tstdout_sha256=%s\tstdout=%s\tcmd=%s\n' "$id" "$start" "" "$rc" "$sha" "$out" "$*" >> "$LOG"
}
cd "$SCRATCH" || exit 2
for f in img/a7530.fs.sqfs img/c6430.x86.fs.sqfs img/c6430.remote.fs.sqfs ctl/ctl-xz-b64k-noxattr-t0.sqfs ctl/ctl-xz-b64k-noxattr-forged.sqfs ctl/ctl-xz-b64k-default-t.sqfs ctl/stock-le-xz.sqfs ctl/stock-le-gzip.sqfs; do
  n=$(echo "$f" | tr '/' '_')
  run "sbwalk:$n" "sbwalk-$n.json" python3 "$T/sbwalk.py" "$f"
  run "census:$n" "census-$n.json" python3 "$T/inodecensus.py" "$f"
done
run "footer:carriers" "footer-carriers.txt" python3 "$T/footer-probe.py" img/a7530.fs.sqfs img/c6430.x86.fs.sqfs img/c6430.remote.fs.sqfs ctl/ctl-xz-b64k-noxattr-t0.sqfs ctl/ctl-xz-b64k-noxattr-forged.sqfs
run "sqfs-list:le:a7530" "sqlist-le-a7530.inspect.txt" python3 "$REA_SQFS_LIST" --layout le --files "$R/a7530.le.files.tsv" --nonregular "$R/a7530.le.nonreg.tsv" --inspect img/a7530.fs.sqfs
run "sqfs-list:auto:a7530" "sqlist-auto-a7530.inspect.txt" python3 "$REA_SQFS_LIST" --layout auto --files "$R/a7530.auto.files.tsv" --nonregular "$R/a7530.auto.nonreg.tsv" --inspect img/a7530.fs.sqfs
run "sqfs-list:avm:a7530(expect-refusal)" "sqlist-avm-a7530.txt" python3 "$REA_SQFS_LIST" --layout avm --files "$R/a7530.avm.files.tsv" img/a7530.fs.sqfs
run "sqfs-list:le:c6430x86" "sqlist-le-c6430x86.txt" python3 "$REA_SQFS_LIST" --layout le --files "$R/c6430x86.le.files.tsv" --nonregular "$R/c6430x86.le.nonreg.tsv" img/c6430.x86.fs.sqfs
run "unsquashfs:-s:a7530" "unsq-s-a7530.txt" unsquashfs -s img/a7530.fs.sqfs
run "unsquashfs:-l:a7530" "unsq-l-a7530.txt" unsquashfs -l img/a7530.fs.sqfs
run "unsquashfs:-s:stock-ctl" "unsq-s-ctl-t0.txt" unsquashfs -s ctl/ctl-xz-b64k-noxattr-t0.sqfs
rm -rf "$SCRATCH/x/unsq-a7530" "$SCRATCH/x/sasq-le-a7530" "$SCRATCH/x/sasq-c6430x86-nx"; mkdir -p "$SCRATCH/x"
run "unsquashfs:-x:a7530" "unsq-x-a7530.txt" unsquashfs -no-progress -d "$SCRATCH/x/unsq-a7530" img/a7530.fs.sqfs
run "sasquatch:-le:-no-exit-code:a7530" "sasq-le-a7530.txt" sasquatch -le -no-exit-code -f -d "$SCRATCH/x/sasq-le-a7530" img/a7530.fs.sqfs
run "sasquatch:no-exit-code:c6430x86" "sasq-nx-c6430x86.txt" sasquatch -no-exit-code -f -d "$SCRATCH/x/sasq-c6430x86-nx" img/c6430.x86.fs.sqfs
run "tree:unsq-a7530-vs-le-oracle" "tree-unsq-a7530.json" python3 "$T/tree-compare.py" "$SCRATCH/x/unsq-a7530" "$R/a7530.le.files.tsv"
run "tree:sasq-le-a7530-vs-le-oracle" "tree-sasq-a7530.json" python3 "$T/tree-compare.py" "$SCRATCH/x/sasq-le-a7530" "$R/a7530.le.files.tsv"
run "tree:sasq-c6430x86-vs-le-oracle" "tree-sasq-c6430x86.json" python3 "$T/tree-compare.py" "$SCRATCH/x/sasq-c6430x86-nx" "$R/c6430x86.le.files.tsv"
echo "receipts written to $LOG"
