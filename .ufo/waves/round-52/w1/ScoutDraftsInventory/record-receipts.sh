#!/usr/bin/env bash
# ScoutDraftsInventory — receipt recorder for the round-52 draft inventory.
# Every row: label<TAB>command<TAB>exit<TAB>stdout_sha256<TAB>stdout_bytes<TAB>utc
# Read-only on the lane tree: this script only READS lane/r51 files and WRITES
# into this seat directory (and $S scratch).
set -u
S=/fast/scratch/hyaku/kaidoku-r52/w1-ScoutDraftsInventory
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScoutDraftsInventory
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R51=$L/.ufo/waves/round-51
OUT=$SEAT/receipts/receipts.tsv
export TMPDIR=$S
mkdir -p "$S" "$SEAT/receipts"

printf 'label\tcommand\texit\tstdout_sha256\tstdout_bytes\tutc\n' > "$OUT"

rec() { # rec LABEL CMD...
  local label=$1; shift
  local out rc sha bytes utc
  out=$("$@" 2>&1); rc=$?
  printf '%s' "$out" > "$SEAT/receipts/$label.out"
  sha=$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)
  bytes=$(printf '%s' "$out" | wc -c)
  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$label" "$*" "$rc" "$sha" "$bytes" "$utc" >> "$OUT"
}

# ---- A. syntax validity of the r51 drafts under assessment -------------------
for f in w1/ExecCounterV2/c1-counter.py l1/drafts/c1-counter.py w1/ExecTriV6/sqfs-triage-v6.py \
         w1/ExecControls/c1-controls.py w1/ExecFetchSelftest/fetch-vendor.py \
         w1/ExecCensusDrift/census3.py w1/ExecOfflineGrammar/disposition-dryrun.py \
         w1/MutGapRule/amended-law-battery.py w1/MutGapRule/gap-rule-mutation-battery.py \
         w1/MutGapRule/law-enforcement-probe.py w1/CritTriV6/v5-source-snapshot.py; do
  lbl=$(printf 'py_compile_%s' "$f" | tr '/' '_')
  rec "$lbl" python3 -m py_compile "$R51/$f"
done
for f in l1/drafts/c1-run.sh w1/ExecMisrootSweep/misroot-sweep.sh w1/CritTriV6/capture.sh; do
  lbl=$(printf 'bash_n_%s' "$f" | tr '/' '_')
  rec "$lbl" bash -n "$R51/$f"
done
rec json_load_gap-rule-v2 python3 -c "import json,sys;json.load(open(sys.argv[1]))" "$R51/w1/ExecRuleDerive/gap-rule-v2.json"

# ---- B. the counter draft's --controls mode, CTL-OLD and CTL-NEW -------------
REV=$(git -C "$S/clone" rev-parse HEAD)
rec ctl_old_r50_rule python3 -I -B "$S/clone/tools/round-51/c1-counter.py" --root "$S/clone" --rev "$REV" \
    --controls --gap-rule tools/round-50/gap-rule.json --receipts corpus/evidence/round-50/c1 --json-out "$SEAT/receipts/ctl-old.json"
rec ctl_new_law_rule python3 -I -B "$S/clone/tools/round-51/c1-counter.py" --root "$S/clone" --rev "$REV" \
    --controls --gap-rule tools/round-51/gap-rule.json --receipts corpus/evidence/round-50/c1 --json-out "$SEAT/receipts/ctl-new.json"

# ---- C. the r51 ExecControls driver against the r51 counter draft ------------
rm -rf "$S/ctl-out"; mkdir -p "$S/ctl-out"
rec r51_controls_driver python3 -I -B "$R51/w1/ExecControls/c1-controls.py" --root "$S/clone" \
    --counter "$S/clone/tools/round-51/c1-counter.py" --old-gap-rule "$S/clone/tools/round-50/gap-rule.json" \
    --receipts "$S/clone/corpus/evidence/round-50/c1" --out "$S/ctl-out"

# ---- D. the r51 fetch-vendor draft selftest, in its intended tools/ location --
cp "$R51/w1/ExecFetchSelftest/fetch-vendor.py" "$S/clone/tools/round-51/fetch-vendor.py"
rec r51_fetch_vendor_selftest python3 -I -B "$S/clone/tools/round-51/fetch-vendor.py" --selftest
rec r50_fetch_vendor_selftest python3 -I -B "$L/tools/round-50/fetch-vendor.py" --selftest

# ---- E. corrected redirect-guard probe (the way the draft should call it) ----
rec redirect_guard_corrected python3 -c "
import importlib.util,urllib.request,urllib.error
spec=importlib.util.spec_from_file_location('fv','$L/tools/round-50/fetch-vendor.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
req=urllib.request.Request('https://download.avm.de/x')
try:
    m._AvmOnlyRedirect().redirect_request(req,None,302,'Found',{'Location':'http://example.invalid/redirect'},'http://example.invalid/redirect')
    print('REDIRECT-GUARD: NOT REFUSED')
except urllib.error.HTTPError as e:
    print('REDIRECT-GUARD refused ok:', 'redirect off' in str(e.reason), '|', e.reason)
"

# ---- F. the r51 triage v6 draft's syntax error, verbatim ---------------------
rec v6_draft_py_compile python3 -m py_compile "$R51/w1/ExecTriV6/sqfs-triage-v6.py"
rec v6_draft_cut_marker grep -n 'CUT 1033' "$R51/w1/ExecTriV6/sqfs-triage-v6.py"

echo "receipts written: $OUT"
