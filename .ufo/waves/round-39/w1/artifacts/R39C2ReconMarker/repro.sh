#!/bin/sh
# R39C2ReconMarker — reproduce every development carrier and REA after-arm of the
# AVM-marker recon (round 39 wave 1, pre-freeze). Scratch only; writes nothing in the lane.
#
#   S=/fast/scratch/hyaku/kaidoku-r39/R39C2ReconMarker sh repro.sh
#
# Requires: python3, unblob 26.6.4 + sasquatch-v4be 4.5.1 in ~/.local/bin,
#           rea-agents 6.5.0 via npx. Never run on K5/K6 or held-out carriers.
set -u
S=${S:-/fast/scratch/hyaku/kaidoku-r39/R39C2ReconMarker}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
GEN="$LANE/tools/round-37/gen-squashfs.py"
mkdir -p "$S"; cd "$S" || exit 1
export PATH="$HOME/.local/bin:$PATH"
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku

# ---- trees -----------------------------------------------------------------
# TA: regular files incl. one 9000-byte multi-block file, nested dirs, in-tree link,
#     in-tree dir link, absolute non-escaping link (/etc/passwd -> rewritten into root)
rm -rf treeA; mkdir -p treeA/docs/deep/nested treeA/bin
printf 'hello from tree A\n' > treeA/hello.txt
printf '# readme\n\nmarker recon tree A\n' > treeA/docs/readme.md
python3 -c "open('treeA/docs/deep/nested/file.dat','wb').write(bytes(range(256))*35+bytes(40))"
printf '#!/bin/sh\necho run\n' > treeA/bin/run
: > treeA/empty
ln -s hello.txt treeA/link-in
ln -s docs treeA/dir-in
ln -s /etc/passwd treeA/link-out

# TB: regular files only, one 5000-byte multi-block file, no symlinks
rm -rf treeB; mkdir -p treeB/a treeB/b/deep/x/y
printf 'A\n' > treeB/a.txt
printf 'C\n' > treeB/b/c.txt
python3 -c "open('treeB/b/deep/x/y/z.bin','wb').write(bytes((i*7)%251 for i in range(5000)))"
: > treeB/empty2
printf 'notes\n' > treeB/notes.md

# TC: every file single-block (< 4096) + the three TC symlinks (xz path is clean here)
rm -rf treeC; mkdir -p treeC/docs treeC/bin
printf 'hello from tree C\n' > treeC/hello.txt
printf '# readme C\n' > treeC/docs/readme.md
printf '#!/bin/sh\necho c\n' > treeC/bin/run
: > treeC/empty
ln -s hello.txt treeC/link-in
ln -s docs treeC/dir-in
ln -s /etc/passwd treeC/link-out

# TT: single-block, no symlinks
rm -rf treeT; mkdir -p treeT
printf 'tiny\n' > treeT/a.txt; printf 'tiny2\n' > treeT/b.txt

# TE: in-tree link + RELATIVE escaping link + symlink loop
rm -rf treeE; mkdir -p treeE/docs
printf 'hello E\n' > treeE/hello.txt
printf 'readme E\n' > treeE/docs/readme.md
ln -s hello.txt treeE/link-in
ln -s ../outside.txt treeE/link-esc
ln -s loop treeE/loop

# ---- carriers --------------------------------------------------------------
for t in A B C T E; do
  for e in be avm; do for c in gzip xz; do
    [ "$t" = E ] && [ "$e$c" != "begzip" ] && continue   # E is the escape probe only
    python3 "$GEN" "tree$t" "carrier-T$t-$e-$c.bin" --endian "$e" --comp "$c"
  done; done
done
for c in gzip xz; do
  python3 "$GEN" treeA "carrier-TA-le-$c.bin" --endian le --comp "$c"
  python3 "$GEN" treeT "carrier-TT-le-$c.bin" --endian le --comp "$c"
done

# payload damage on standard BE bodies (chunk still detected / chunk lost)
python3 - <<'EOF'
b=bytearray(open('carrier-TT-be-gzip.bin','rb').read()); open('carrier-TT-be-trunc.bin','wb').write(bytes(b[:-40]))
b=bytearray(open('carrier-TT-be-gzip.bin','rb').read())
for i in range(259, 279): b[i] ^= 0xA5                     # inode-table metadata header
open('carrier-TT-be-inodecorrupt.bin','wb').write(bytes(b))
b=bytearray(open('carrier-TA-be-gzip.bin','rb').read())
for i in range(200, 260): b[i] ^= 0xFF                     # data area
open('carrier-TA-be-midcorrupt.bin','wb').write(bytes(b))
# AVM marker planted on a LE image: mkfs_time := bytes_used (marker code path is BE-only)
import struct
b=bytearray(open('carrier-TT-le-gzip.bin','rb').read())
bu=struct.unpack('<4sIIIIHHHHHHQQQQQQQQ', bytes(b[:96]))[12]
b[8:12]=struct.pack('<I', bu); open('carrier-TT-le-avmmark.bin','wb').write(bytes(b))
EOF

# ---- REA after-arm ---------------------------------------------------------
run() {  # run NAME CARRIER [PATH]
  name=$1; img=$2; p=${3:-$PATH}
  rm -rf "rea/$name"
  PATH="$p" npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
    "$img" "rea/$name" > "rea-$name.json" 2> "rea-$name.err"
  echo "$name rc=$? bytes=$(stat -c%s rea-$name.json)"
}
mkdir -p rea
for n in TC-avm-gzip TC-be-gzip TC-avm-xz TC-be-xz \
         TT-avm-gzip TT-be-gzip TT-avm-xz TT-be-xz \
         TA-avm-gzip TA-be-gzip TA-avm-xz TA-be-xz \
         E-be-gzip TT-le-gzip TA-le-xz TT-le-avmmark \
         TT-be-trunc TA-be-midcorrupt TT-be-inodecorrupt; do
  run "$n" "carrier-$n.bin"
done
STRIP=$(printf '%s' "$PATH" | tr ':' '\n' | grep -v "^$HOME/.local/bin$" | paste -sd:)
run TC-be-nosasq carrier-TC-be-gzip.bin "$STRIP"
run TT-le-nosasq carrier-TT-le-gzip.bin "$STRIP"

# ---- features (P39-C2 grammar) --------------------------------------------
python3 features.py rea-*.json > feat-all.json

# ---- unblob ground truth (child argv, verbose log) ------------------------
for c in TC-avm-gzip TC-avm-xz TC-be-gzip; do
  rm -rf "ub-$c"; unblob -v -e "ub-$c" "carrier-$c.bin" > "ub-$c.log" 2>&1
  grep -oE "command='[^']*'" "ub-$c.log" | head -2
done

# ---- direct sasquatch matrix (isolated session: a failing run can kill the group)
python3 - <<'EOF'
import subprocess, glob, os, shutil, json
S=os.getcwd(); exe=os.path.expanduser('~/.local/bin/sasquatch-v4be'); rows=[]
for f in sorted(glob.glob('carrier-*.bin')):
    for mode in ('noflag','beflag'):
        out=f'sq/{f}-{mode}'; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
        p=subprocess.run([exe]+(['-be'] if mode=='beflag' else [])+['-no-exit-code','-f','-d',out,os.path.join(S,f)],
                         capture_output=True, start_new_session=True, cwd=S)
        n=sum(len(fs) for _,_,fs in os.walk(out))-2
        rows.append(dict(carrier=f, mode=mode, rc=p.returncode, files=n,
                         stderr_head=(p.stderr.decode('utf-8','replace').strip().splitlines() or [''])[0]))
json.dump(rows, open('sasquatch-matrix.json','w'), indent=1)
for r in rows: print(r['carrier'], r['mode'], 'rc=', r['rc'], 'files=', r['files'])
EOF
