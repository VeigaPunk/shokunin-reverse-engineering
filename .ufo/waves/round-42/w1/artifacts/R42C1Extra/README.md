# R42C1Extra artifacts — round-42 `tools/round-42/c1-extra.py`

Seat: `R42C1Extra` (wave 1, pre-freeze). Owner installs `c1-extra.py` at
`tools/round-42/c1-extra.py`; everything else here is evidence, not lane content.

| file | what it is | sha256 |
|---|---|---|
| `c1-extra.py` | the port (stdlib only, Python 3.9+) | `63d7cf91ce749e12ee8ae38ed36cdbd274c092f4d215b3f8d24f77a672975158` |
| `dryrun.py` | reproducible end-to-end dry run on a sandbox clone of the lane | `b443b44d44af3d89715c7725ddbdb79a60c6500e01f089131e99a7f157e61ee7` |
| `selftest/selftest.txt` | `--selftest` transcript, 41 cases, 41 pass | — |
| `dryrun/` | 13 receipts + `dryrun-summary.json` from one dry run | — |
| `oracle-check/` | `--oracle-check` against the real `sqfs3-oracle.py` on five v3 fixtures | — |
| `fixtures/` | the five MIT unblob 26.6.4 v3 fixtures used (4 KiB each) + `fixtures.json` (URL, sha256) | — |
| `before-c4a38ea2….json`, `before-fdabdfa4….json` | the unmoved measurement at the base and at wave-1 HEAD (exit 2) | — |

## Rebuild

```sh
S=/fast/scratch/hyaku/kaidoku-r42/R42C1Extra; mkdir -p "$S"; cd "$S"
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42C1Extra
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin

# 1. offline selftest
python3 "$A/c1-extra.py" --selftest --work "$S"

# 2. the unmoved measurement (both exit 2: carriers.json and the oracle tool are absent)
python3 "$A/c1-extra.py" --root "$L" --rev c4a38ea2 --freeze c4a38ea2 \
        --base c4a38ea2 --json-out "$S/before.json"

# 3. dry run on real lane documents (clone only; five reds expected)
python3 "$A/dryrun.py" --lane "$L" --tool "$A/c1-extra.py" --scratch "$S" --out "$S/dry"

# 4. the real oracle once `tools/round-42/sqfs3-oracle.py` exists
python3 "$A/c1-extra.py" --oracle-check \
        --oracle /path/to/kaidoku-shokunin/tools/round-42/sqfs3-oracle.py \
        --dev-image "$A/fixtures/squashfs_v3_little_endian.bin" --work "$S"

# 5. the score itself, after the freeze
python3 "$A/c1-extra.py" --root "$L" --rev REV --freeze FREEZE \
        --base c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c \
        --carrier-cache DIR --json-out receipt.json
```

Fixture download (MIT, unblob 26.6.4 tree, small enough to keep):

```sh
curl -o squashfs_v3_le.bin \
  https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v3/little_endian/__input__/squashfs_v3_le.bin
```

No firmware image is copied here; the dry run uses 1.4 KiB of synthetic `SQF3`
bytes and a stand-in oracle, on purpose (see the report's Limits).
