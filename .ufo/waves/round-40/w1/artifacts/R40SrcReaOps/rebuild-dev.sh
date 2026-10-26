#!/usr/bin/env bash
# Rebuilds the development SquashFS (sha256 7494b3d7634e76868a6c8bf3b5609cd9f3bb6c60e08a4b305ad66eed01f951b3) and re-runs the probes.
# Usage: TMPDIR=<scratch> bash rebuild-dev.sh   (honours TMPDIR; never touches /tmp)
set -euo pipefail
S=${TMPDIR:?set TMPDIR}; cd "$S"; export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
mkdir -p tree/a; echo hello > tree/a/x.txt; echo world > tree/y.txt; ln -s y.txt tree/lnk
python3 $L/tools/round-39/gen-squashfs.py tree dev.sqfs --endian le --comp gzip; sha256sum dev.sqfs
P=$L/.ufo/waves/round-40/w1/artifacts/R40SrcReaOps/probe.py
python3 $P inspect-firmware-regions dev.sqfs; python3 $P execute-rizin-command dev.sqfs i
python3 $P inspect-with-objdump dev.sqfs file_headers; python3 $P inspect-evm-interface dev.sqfs raw
python3 $P inspect-artifact dev.sqfs; python3 $P analyze dev.sqfs; python3 $P inspect-binary-layout dev.sqfs
