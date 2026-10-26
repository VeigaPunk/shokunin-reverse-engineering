#!/bin/sh
# build-fixture.sh -- build the dev fixture repo the control suite is exercised on.
#
# Not evidence of the claim: it is a *shape* fixture. The carriers are the retained
# round-11 genuine AVM-layout body (read-only copy from shokuknow) plus zero padding to
# make four distinct pins, and the receipts are synthesized, because this wave may not
# run REA on an AVM-layout body. It exists so `run-controls.sh` can be executed today and
# every clause/output path of every control is exercised before the freeze.
#
#   ./build-fixture.sh <dir> <genuine-avm-body> <reader-with-avm-mode> <gen-squashfs.py> \
#                      <round-39-receipts-dir>
set -eu
F=$1; GENUINE=$2; READER=$3; WRITER=$4; R39=$5
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
rm -rf "$F"; mkdir -p "$F"
cd "$F"
git init -q .
git -C "$F" rev-parse --show-toplevel
mkdir -p plans .ufo/waves/round-40/c1 tools/round-40 tools/round-39 \
         corpus/knowledge corpus/evidence/round-40/c1 corpus/evidence/round-39/c1
printf '# claims (DRAFT dev fixture)\n' > plans/round-40-claims.md
printf '# PROVINCE dev fixture\n\nFrontier: AVM-BE bodies and vendor-mangled images stay Frontier.\n' > PROVINCE.md
printf '# README dev fixture\n' > corpus/README.md
cat > corpus/SOURCES.md <<'EOF'
| S1 | dev round-38 row | docs | A | a | b | c | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r39-other.md |
| S112 | unblob SquashFS handler at tag 26.6.4 | code | A | a | b | c | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r39-other.md |
| S122 | unblob path-containment helper at tag 26.6.4 | code | A | a | b | c | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r39-other.md |
EOF
git add -A
git -c user.name=fx -c user.email=fx@fx commit -q -m base
echo "BASE=$(git rev-parse HEAD)"

cp "$READER" tools/round-40/sqfs-list.py
cp "$WRITER" tools/round-39/gen-squashfs.py
for k in K1 K2 K3 K4; do
    [ -d "$R39/$k" ] && cp -a "$R39/$k" corpus/evidence/round-39/c1/
done
python3 -I -B - "$GENUINE" <<'PY'
import hashlib, json, os, subprocess, sys
genuine = open(sys.argv[1], 'rb').read()
pads = {'V1': b'', 'V2': b'\0' * 4, 'L1': b'\0' * 8, 'L2': b'\0' * 12}
cs = []
for cid, pad in pads.items():
    d = 'corpus/evidence/round-40/c1/' + cid
    os.makedirs(d, exist_ok=True)
    body = genuine + pad
    with open(d + '/carrier.sqsh', 'wb') as f:
        f.write(body)
    r = subprocess.run([sys.executable, '-I', '-B', 'tools/round-40/sqfs-list.py',
                        '--avm', d + '/carrier.sqsh', '--files', d + '/oracle.tsv',
                        '--symlinks', d + '/symlinks.tsv'], capture_output=True)
    assert r.returncode == 0, r.stderr
    o = open(d + '/oracle.tsv', 'rb').read()
    s = open(d + '/symlinks.tsv', 'rb').read()
    cs.append({'id': cid, 'kind': 'dev fixture carrier', 'path': d + '/carrier.sqsh',
               'sha256': hashlib.sha256(body).hexdigest(), 'size_bytes': len(body),
               'oracle': d + '/oracle.tsv',
               'oracle_sha256': hashlib.sha256(o).hexdigest(),
               'oracle_files': sum(1 for l in o.splitlines() if l.strip()),
               'symlinks': d + '/symlinks.tsv',
               'symlinks_sha256': hashlib.sha256(s).hexdigest(),
               'receipt': d + '/after.json', 'extract_root': 'carrier.sqsh_extract'})
json.dump({'claim': 'R40-C1', 'GENUINE_AVM': os.path.abspath(sys.argv[1]),
           'carriers': cs}, open('.ufo/waves/round-40/c1/carriers.json', 'w'),
          indent=1, sort_keys=True)
json.dump({'controls': 'dev fixture'},
          open('.ufo/waves/round-40/c1/controls.json', 'w'))
PY
git add -A
git -c user.name=fx -c user.email=fx@fx commit -q -m freeze
echo "FREEZE=$(git rev-parse HEAD)"

python3 -I -B "$here/ctl-lib.py" --control CTL-C1-2 --root "$F" \
    --spec .ufo/waves/round-40/c1/carriers.json >/dev/null
printf '# AVM layout knowledge entry\n\nGenuine AVM-layout big-endian SquashFS v4 extracts (dev fixture).\n' \
    > corpus/knowledge/2026-10-26-r40-avm-be-squashfs-v4-core.md
cat > PROVINCE.md <<'EOF'
# PROVINCE dev fixture

Frontier: AVM-BE bodies and vendor-mangled images stay Frontier.

## Round-40 additions to Core

| Surface | Ports | Probe | Evidence |
|---|---|---|---|
| AVM-layout BE v4 | none | extract-firmware | `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-v4-core.md` |

Round-40 frontier note, 2026-10-26: the AVM part is superseded by Round-40 additions to Core (`2026-10-26-r40-avm-be-squashfs-v4-core`).
EOF
printf '# README dev fixture\n\n2026-10-26-r40-avm-be-squashfs-v4-core\n' > corpus/README.md
cat >> corpus/SOURCES.md <<'EOF'
| S240 | dev round-40 row | docs | A | a | b | c | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r40-avm-be-squashfs-v4-core.md |
EOF
git add -A
git -c user.name=fx -c user.email=fx@fx commit -q -m tip
echo "TIP=$(git rev-parse HEAD)"
