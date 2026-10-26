#!/bin/sh
# R39C2ReconClean — development carriers for R39-C2 recon (never held-out, never K5/K6).
# Two fresh trees per class; trees authored here, images built with the frozen round-37 writer.
# Usage: sh build-dev-carriers.sh <SCRATCH>
set -eu
S=${1:?scratch dir}
GEN=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-37/gen-squashfs.py
T=$S/trees
O=$S/carriers
rm -rf "$T" "$O"; mkdir -p "$T" "$O"

mkbase() { mkdir -p "$@"; }

# ---------- tree A1: clean BE, no symlinks ----------
A1=$T/a1
mkbase "$A1/etc" "$A1/usr/share/app" "$A1/var/lib"
printf 'welcome to node a1\n' > "$A1/etc/motd.txt"
printf 'name=a1\nmode=dev\n' > "$A1/usr/share/app/main.cfg"
python3 - "$A1/var/lib/counter.db" <<'PY'
import sys
open(sys.argv[1],'wb').write(bytes((i*7+3) & 0xFF for i in range(200)))
PY
printf 'tree a1\n' > "$A1/README"

# ---------- tree A2: clean BE, no symlinks ----------
A2=$T/a2
mkbase "$A2/boot" "$A2/opt/app" "$A2/data"
printf 'kernel=/boot/vmlinuz\n' > "$A2/boot/loader.cfg"
printf '#!/bin/sh\necho a2\n' > "$A2/opt/app/run.sh"
python3 - "$A2/data/blob.bin" <<'PY'
import sys
open(sys.argv[1],'wb').write(bytes((i*37+11) & 0xFF for i in range(6000)))
PY

# ---------- tree B1: clean LE, no symlinks ----------
B1=$T/b1
mkbase "$B1/srv/http" "$B1/srv/data"
printf '<html><body>b1</body></html>\n' > "$B1/srv/http/index.html"
printf 'body{margin:0}\n' > "$B1/srv/http/style.css"
printf 'id,name\n1,b1\n' > "$B1/srv/data/table.csv"

# ---------- tree B2: clean LE, no symlinks ----------
B2=$T/b2
mkbase "$B2/lib/firmware" "$B2/etc" "$B2/usr/bin"
python3 - "$B2/lib/firmware/fw.bin" <<'PY'
import sys
open(sys.argv[1],'wb').write(bytes((i*13+5) & 0xFF for i in range(3000)))
PY
printf 'root:x:0:0\n' > "$B2/etc/passwd.sample"
printf '#!/bin/sh\necho tool\n' > "$B2/usr/bin/tool"

# ---------- tree C1: BE, exactly one escaping relative symlink ----------
C1=$T/c1
mkbase "$C1/etc" "$C1/usr/bin"
printf 'c1 marker\n' > "$C1/etc/marker.txt"
printf '#!/bin/sh\necho c1\n' > "$C1/usr/bin/c1"
ln -s ../outside.txt "$C1/up.txt"

# ---------- tree C2: BE, exactly one escaping relative symlink (deeper) ----------
C2=$T/c2
mkbase "$C2/deep/inner" "$C2/etc"
printf 'c2 marker\n' > "$C2/etc/marker.txt"
printf 'payload c2\n' > "$C2/deep/inner/payload.dat"
ln -s ../../../outside/x.txt "$C2/deep/inner/link-out"

# ---------- tree D1: BE, exactly one in-tree relative symlink ----------
D1=$T/d1
mkbase "$D1/etc"
printf 'hello d1\n' > "$D1/hello.txt"
printf 'd1 config\n' > "$D1/etc/app.cfg"
ln -s hello.txt "$D1/alias.txt"

# ---------- tree D2: BE, exactly one in-tree relative symlink (parent-relative) ----------
D2=$T/d2
mkbase "$D2/etc" "$D2/cfg"
printf 'd2 config\n' > "$D2/etc/app.cfg"
printf 'd2 notes\n' > "$D2/cfg/notes.txt"
ln -s ../etc/app.cfg "$D2/cfg/current"

# ---------- tree E1: BE, one in-tree AND one escaping relative symlink (mixed probe) ----------
E1=$T/e1
mkbase "$E1/etc"
printf 'e1 marker\n' > "$E1/etc/marker.txt"
printf 'e1 data\n' > "$E1/plain.txt"
ln -s plain.txt "$E1/alias.txt"
ln -s ../../outside/x.txt "$E1/esc.txt"

# ---------- tree F1: BE, absolute symlink targets (rule probe, not a class) ----------
F1=$T/f1
mkbase "$F1/etc"
printf 'f1 marker\n' > "$F1/etc/marker.txt"
printf 'f1 plain\n' > "$F1/plain.txt"
ln -s /etc/passwd "$F1/abs-out"
ln -s /plain.txt "$F1/abs-in"

# ---------- tree F2: BE, absolute target that strips to an escaping relative one ----------
F2=$T/f2
mkbase "$F2/etc"
printf 'f2 marker\n' > "$F2/etc/marker.txt"
ln -s /../../outside.txt "$F2/abs-dotdot"

# ---------- tree C2X: the superseded two-level target probe (resolves INSIDE the root) ----------
# `deep/inner/../../outside/x.txt` is root-relative, not escaping: kept as metadata, exactly like
# K2's `var/lib/run-link -> ../../a/run.sh`. Evidence for the resolution-based symlink rule.
C2X=$T/c2-twolevel
cp -r "$C2" "$C2X"
rm "$C2X/deep/inner/link-out"
ln -s ../../outside/x.txt "$C2X/deep/inner/link-out"

build() { # name tree endian comp
  python3 "$GEN" "$2" "$O/$1.sqsh" --endian "$3" --comp "$4"
}
build a1 "$A1" be gzip
build a2 "$A2" be gzip
build b1 "$B1" le gzip
build b2 "$B2" le gzip
build c1 "$C1" be gzip
build c2 "$C2" be gzip
build d1 "$D1" be gzip
build d2 "$D2" be gzip
build e1 "$E1" be gzip
build f1 "$F1" be gzip
build f2 "$F2" be gzip
build c2-twolevel "$C2X" be gzip

cd "$O" && sha256sum ./*.sqsh
