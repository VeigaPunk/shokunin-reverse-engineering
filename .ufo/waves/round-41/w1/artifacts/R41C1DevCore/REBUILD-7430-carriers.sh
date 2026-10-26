#!/bin/sh
# Rebuild the two R41C1DevCore development carriers from the public AVM image.
# No vendor bytes are stored in the lane: this script re-derives them, and every
# step is digest-checked.  Development input only (the image is one of the two
# AVM builds the operator released for RE training in round 40).
#
#   sh REBUILD-7430-carriers.sh [SCRATCH_DIR]
#
# Requires: curl, unblob 26.6.4 (REA_UNBLOB_COMMAND target), python3.
# Outputs in SCRATCH_DIR: 7430-wrapper.sqsh, 7430-core.sqsh
set -eu
S=${1:-$PWD}
mkdir -p "$S"
cd "$S"

IMG=FRITZ.Box_7430-07.31.image
[ -f "$IMG" ] || curl -sSL -o "$IMG" \
  https://download.avm.de/fritzbox/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image
echo "3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4  $IMG" | sha256sum -c -

# One unblob run at its default depth extracts the AVM wrapper and the nested
# rootfs under it (a plain `unblob -e OUTDIR IMG`, never `-be`).
if [ ! -d "${IMG}_extract" ]; then
  PATH="$HOME/.local/bin:$PATH" unblob -e . "$IMG" || true   # exit 2 on warnings
fi

W="${IMG}_extract/var/tmp/filesystem.image"
echo "b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c  $W" | sha256sum -c -
# AVM wrapper: bytes_used = 25824314 (mkfs_time == bytes_used)
head -c 25824314 "$W" > 7430-wrapper.sqsh
echo "c88ba9faa038e73ed1a3ca264be9b1da89aae51cf800a9b7605bd865c06c9c5a  7430-wrapper.sqsh" | sha256sum -c -

CORE=$(ls "${W}_extract"/*.squashfs_v4_be_extract/filesystem_core.squashfs)
# nested rootfs as stored in the wrapper: 25198592 bytes
echo "14dc8e550482c7608943fb1adad8960a989d3da16e7444e1fdf9a0652fb08329  $CORE" | sha256sum -c -
# rootfs: bytes_used = 25194540 (mkfs_time == bytes_used)
head -c 25194540 "$CORE" > 7430-core.sqsh
echo "1588129540dfdcce09cb8304f724a66fd50aa1eb0bc6481cc6a2246670aa628f  7430-core.sqsh" | sha256sum -c -

# Superblock check (big-endian `sqsh`, marker, xz):
python3 - "$PWD/7430-core.sqsh" <<'PY'
import struct, sys
b = open(sys.argv[1], 'rb').read(96)
f = struct.unpack('>IIIIIHHHHHHQQQQQQQQ', b)
print('magic %08x inodes %d mkfs_time %d bytes_used %d marker %s comp %d'
      % (f[0], f[1], f[2], f[12], f[2] == f[12], f[5]))
PY
