#!/bin/sh
# Rebuild the 12 dev carriers used by R39C2AxisFit. Fresh tree, never K5/K6, never a held-out C2 carrier.
set -eu
S=${1:?scratch dir}
mkdir -p "$S"; cd "$S"; rm -rf treeA treeB; mkdir -p treeA/docs/deep/nested treeA/bin treeA/emptydir
printf 'hello dev\n' > treeA/hello.txt
printf '# dev readme\nsecond line\n' > treeA/docs/readme.md
python3 -c "open('treeA/docs/deep/nested/file.dat','wb').write(bytes((i*37+11)%256 for i in range(200))); open('treeA/bin/run','wb').write(b'#!/bin/sh\necho hi\n')"
: > treeA/empty
cp -a treeA treeB; ln -s hello.txt treeB/link-in; ln -s ../../../etc/passwd treeB/link-out
G=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-37/gen-squashfs.py
python3 "$G" treeA be-clean.sqsh --endian be --comp gzip
python3 "$G" treeA be-avm.sqsh --endian avm --comp gzip
python3 "$G" treeB be-sym.sqsh --endian be --comp gzip
python3 - <<'PY'
import struct
b=open('be-clean.sqsh','rb').read(); m=struct.unpack('>Q',b[40:48])[0]; it=struct.unpack('>Q',b[64:72])[0]
open('be-trunc.sqsh','wb').write(b[:len(b)-200])
d=bytearray(b); d[it+10]^=0xFF; open('be-bodyflip.sqsh','wb').write(bytes(d))
d=bytearray(b); d[3]=ord('x'); open('be-magic.sqsh','wb').write(bytes(d))
d=bytearray(b); [d.__setitem__(i,0) for i in range(96,200)]; open('be-zeroed.sqsh','wb').write(bytes(d))
d=bytearray(b); d[64:72]=struct.pack('>Q',0xFFFFFFFF); open('be-inodeptr.sqsh','wb').write(bytes(d))
d=bytearray(b); d[32:40]=struct.pack('>Q',0xDEADBEEF); open('be-rootino.sqsh','wb').write(bytes(d))
d=bytearray(b); d[40:48]=struct.pack('>Q',0x7FFFFFFF); open('be-bytesused.sqsh','wb').write(bytes(d))
PY
