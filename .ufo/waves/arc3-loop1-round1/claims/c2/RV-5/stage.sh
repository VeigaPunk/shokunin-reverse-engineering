#!/usr/bin/env bash
# RV-5: stage gate dirs in scratch. Never writes into the repo.
#   stage.sh proto   -> copy EX-21's prototype (draft, NOT the landed artifact)
#   stage.sh post    -> copy EX-16's landed gate dir (fails if not landed)
#   stage.sh postfix -> build derived post fixtures (identical copy, stale pin)
set -u
REPO=${REPO:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
S=$(cd "$(dirname "$0")" && pwd)
SCRATCH=${SCRATCH:-/home/vgpnk/.cache/kaidoku-rv5-arc3r1}
case "${1:-}" in
pre)
  # pre-guard state: the three files as committed at HEAD, reconstructed from
  # git objects (the worktree now carries EX-16's landed guard)
  D=$SCRATCH/pre-gate; mkdir -p "$D"
  for f in citation-drift-probe.py expected.json pointer-table.json; do
    git -C "$REPO" show "HEAD:.ufo/gates/citation-drift/$f" > "$D/$f" || exit 1
  done
  cp -a "$D/citation-drift-probe.py" "$D/probe.py"
  sha256sum "$D"/* | tee "$SCRATCH/pre-gate.sha256"
  ;;
proto)
  # EX-21's draft prototype (their scratch dir; NOT the landed artifact)
  D=$SCRATCH/proto-gate; mkdir -p "$D"
  cp -a "$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-21/tmp/proto/probe.py" "$D/probe.py"
  cp -a "$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-21/tmp/proto/expected.json" "$D/expected.json"
  cp -a "$REPO/.ufo/gates/citation-drift/pointer-table.json" "$D/pointer-table.json"
  sha256sum "$D"/* | tee "$SCRATCH/proto-gate.sha256"
  ;;
post)
  D=$SCRATCH/post-gate; mkdir -p "$D"
  cp -a "$REPO/.ufo/gates/citation-drift/citation-drift-probe.py" "$D/probe.py" || exit 1
  cp -a "$REPO/.ufo/gates/citation-drift/expected.json" "$D/expected.json" || exit 1
  cp -a "$REPO/.ufo/gates/citation-drift/pointer-table.json" "$D/pointer-table.json" || exit 1
  sha256sum "$D"/* | tee "$SCRATCH/post-gate.sha256"
  ;;
postfix)
  # derived fixtures, computed from the landed expected.json (design-agnostic:
  # any string equal to the table's digest is treated as the pin)
  D=$SCRATCH/post-gate
  python3 - "$D" "$S/fixtures" <<'PY'
import hashlib, json, os, shutil, sys
D, F = sys.argv[1], sys.argv[2]
raw = open(os.path.join(D, "pointer-table.json"), "rb").read()
dig = hashlib.sha256(raw).hexdigest()
shutil.copyfile(os.path.join(D, "pointer-table.json"), os.path.join(F, "table-identical-copy.json"))
exp = json.load(open(os.path.join(D, "expected.json")))
def scrub(o):
    if isinstance(o, dict):
        return {k: ("0" * 64 if v == dig else scrub(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub(v) for v in o]
    return o
stale = scrub(exp)
assert json.dumps(stale) != json.dumps(exp), "no pin equal to the table digest found"
json.dump(stale, open(os.path.join(F, "expected-stale-pin.json"), "w"))
print("pin found; stale-pin fixture written; table digest", dig)
PY
  ;;
*) echo "usage: stage.sh proto|post|postfix" >&2; exit 2;;
esac
