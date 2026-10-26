#!/usr/bin/env bash
# usage: carve.sh WORKDIR   (downloads V2 + D, verifies sha256, carves members). Honors TMPDIR via WORKDIR; never runs unblob/REA.
set -euo pipefail
W=${1:?workdir}; mkdir -p "$W"; cd "$W"
B=https://download.avm.de/fritzbox
# V2: FRITZ!Box 7430, FRITZ!OS 7.31 (MIPS wrapper family), AVM-BE member
curl -fsS -o v2.image $B/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image
EXP_V2_IMG=3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4; EXP_V2_MEM=b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c
echo "$EXP_V2_IMG  v2.image" | sha256sum -c -
tar -xOf v2.image ./var/tmp/filesystem.image > v2-member.sqfs
echo "$EXP_V2_MEM  v2-member.sqfs" | sha256sum -c -
# D: FRITZ!Box 6590 Cable, FRITZ!OS 7.57 image (same tar shape as V1); recon seats run REA on d.image itself
curl -fsS -o d.image $B/fritzbox-6590-cable/other/fritz.os/FRITZ.Box_6590_Cable-07.57.image
EXP_D_IMG=0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae; EXP_D_BE=65e85647f0199f9dcbb3f06674557bfda2fc9a4412378448b572478d2bff832a; EXP_D_LE=57552a6dd81b6a43032b761bfbd10090442dbbcce88609bdb731af1242932786
echo "$EXP_D_IMG  d.image" | sha256sum -c -
tar -xOf d.image ./var/remote/var/tmp/filesystem.image > d-be-member.sqfs
tar -xOf d.image ./var/remote/var/tmp/x86/filesystem.image > d-le-member.sqfs
echo "$EXP_D_BE  d-be-member.sqfs" | sha256sum -c -
echo "$EXP_D_LE  d-le-member.sqfs" | sha256sum -c -
