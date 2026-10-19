#!/usr/bin/env bash
# EX-25 (c2, executor): post-implementation replay driver for the citation-drift
# frozen-run guard (EX-16's claim). Read-only over the repo: every capture is
# written under this seat's claims dir. Scratch fixtures (tampered/absent table)
# are copies under ./scratch, never the real gate files.
#
# usage: replay-driver.sh <label>     label = before | after
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
LABEL="${1:?label required}"
W=.ufo/waves/arc3-loop1-round1/claims/c2/EX-25
P=.ufo/gates/citation-drift/citation-drift-probe.py
T=.ufo/gates/citation-drift/pointer-table.json
E=.ufo/gates/citation-drift/expected.json
D=$W/logs; mkdir -p "$D"

run() { # run <name> <cmd...>
  local name="$1"; shift
  { echo "\$ $*"; "$@"; echo "exit=$?"; } > "$D/$LABEL-$name.txt" 2>&1
}

echo "== $LABEL: provenance ==" | tee "$D/$LABEL-provenance.txt"
{ echo "date: $(date -Is)"
  echo "git HEAD: $(git rev-parse HEAD)"
  echo "git status (gate dir): $(git status --porcelain .ufo/gates/citation-drift/ | tr '\n' ';')"
  echo "--- sha256 of gate files ---"
  sha256sum "$P" "$T" "$E"
  echo "--- expected.json table digest field (if any) ---"
  python3 - "$E" <<'PY'
import json,sys
e=json.load(open(sys.argv[1]))
print("top-level keys:", list(e.keys()))
print("frozen_run:", json.dumps(e.get("frozen_run"))[:300])
print("snapshots:", json.dumps(e.get("snapshots")))
print("pointer_table digest field:", json.dumps({k:v for k,v in e.items() if "table" in k.lower()}))
print("selftest cases:", [c["case"] for c in e.get("selftest",[])])
PY
} | tee -a "$D/$LABEL-provenance.txt"

echo "== $LABEL: probe at HEAD (probe semantics) =="
run probe-head python3 "$P" --root . --rev HEAD --table "$T" --expected "$E"
echo "== $LABEL: probe --rev deadbeef =="
run probe-rev-deadbeef python3 "$P" --root . --rev deadbeef --table "$T" --expected "$E"
echo "== $LABEL: probe --strict at HEAD (gate map) =="
run probe-strict python3 "$P" --root . --rev HEAD --table "$T" --expected "$E" --strict
echo "== $LABEL: selftest =="
run selftest python3 "$P" --selftest --expected "$E"
echo "== $LABEL: independent tampered-table injection (scratch copy) =="
python3 - "$T" "$W/scratch/table-tampered.json" <<'PY'
import json,sys
t=json.load(open(sys.argv[1]))
# tamper: one entry's must_match can never match, leaving the table otherwise intact
for e in t.get("entries",[]):
    if e.get("id")=="sc59-stanza-key-anchor":
        e["must_match"]="NEVER_MATCHES_THIS_STRING_ZZZ"
        break
json.dump(t,open(sys.argv[2],"w"),indent=2)
print("tampered table written:", sys.argv[2])
PY
run tampered-table python3 "$P" --root . --rev HEAD --table "$W/scratch/table-tampered.json" --expected "$E"
run tampered-table-strict python3 "$P" --root . --rev HEAD --table "$W/scratch/table-tampered.json" --expected "$E" --strict
echo "== $LABEL: independent absent-table injection =="
run absent-table python3 "$P" --root . --rev HEAD --table "$W/scratch/no-such-table.json" --expected "$E"
echo "== $LABEL: digest cross-check (expected.json vs on-disk table) =="
python3 - "$T" "$E" <<'PY' | tee "$D/$LABEL-digest-check.txt"
import hashlib,json,sys
disk=hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()
e=json.load(open(sys.argv[2]))
pinned=None
for k,v in e.items():
    if isinstance(v,dict):
        for kk,vv in v.items():
            if isinstance(vv,str) and len(vv)==64 and "pointer-table" in str(kk).lower():
                pinned=vv
    if isinstance(v,dict) and "pointer-table.json" in json.dumps(v):
        pass
print("on-disk pointer-table.json sha256:", disk)
print("pinned digest found:", pinned)
print("MATCH" if pinned==disk else ("NO-PIN" if pinned is None else "MISMATCH"))
PY
echo "== $LABEL complete =="
