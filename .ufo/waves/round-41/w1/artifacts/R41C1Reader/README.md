# R41C1Reader artifacts

Derived metadata only: paths, sha256 digests, sizes, superblock fields. No vendor firmware
bytes and no extracted vendor file contents are stored here (AVM licence); every claim is
reproducible from the commands in `../R41C1Reader.md` §Reproduction.

| file | what |
|---|---|
| `timings.txt` | wall time / peak RSS / exit code per run |
| `7430-core-oracle.tsv` | `sqfs-list.py --layout avm --files` output for the 7430 nested core (6485 rows: relpath, sha256, size) |
| `7430-core-nonregular.tsv` | `--nonregular` output (409 dirs, 628 symlinks with targets, 1 char device `dev/led 247:0`) |
| `7430-core-inspect.json` | `--inspect` superblock/layout/decode-path summary for the core |
| `7430-core-lls-head.txt` | first 20 lines of the `sasquatch-v4be -lls` listing (format evidence) |
| `compare.json` | reader vs `sasquatch-v4be` tree + `-lls` on the core: every diff class (all empty) |
| `wrapper-compare.json` | same for the outer `./var/tmp/filesystem.image` wrapper |
| `auto-inspect.json` | core read with `--layout auto` (resolved `avm`, signal `plausibility`) |
| `census.json` | core coverage census (fragments, multi-block, empty, charset, depth, sizes) |
| `suffix-census.json` | k-component suffix collision pairs on the core (k=1..4) |
| `suffix-all.json` | the same census over the 7430 core+wrapper and the four round-40 dev carriers |
| `fetch-vendor.json` | V1/V2 dev carrier rebuild record (image/member/carrier sha256) |
| `compare.py`, `census.py`, `suffix-census.py`, `suffix-all.py`, `run_timed.py` | the comparison tools used (stdlib only; `run_timed.py` reports `resource.getrusage(RUSAGE_CHILDREN)` because `/usr/bin/time` is absent on this host) |

Reproduce (scratch, absolute lane path):

```
S=/fast/scratch/hyaku/kaidoku-r41/R41C1Reader; mkdir -p "$S"; cd "$S"
curl -fsSL -o 7430.image https://download.avm.de/fritzbox/fritzbox-7430/other/fritz.os/FRITZ.Box_7430-07.31.image
sha256sum 7430.image   # 3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4
tar -xf 7430.image ./var/tmp/filesystem.image
~/.local/bin/sasquatch-v4be -d fs-extract -no-progress var/tmp/filesystem.image
head -c 25194540 fs-extract/filesystem_core.squashfs > core.squashfs
~/.local/bin/sasquatch-v4be -d core-sasq -no-progress core.squashfs
~/.local/bin/sasquatch-v4be -lls -no-progress core.squashfs > core-lls.txt
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40/sqfs-list.py \
  --layout avm --files core-reader-files.tsv --nonregular core-reader-nonreg.tsv core.squashfs
python3 -I -B compare.py core-sasq core-lls.txt core-reader-files.tsv core-reader-nonreg.tsv
```
