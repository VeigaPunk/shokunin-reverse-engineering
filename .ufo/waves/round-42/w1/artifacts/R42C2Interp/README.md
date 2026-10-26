# R42C2Interp artifacts — SquashFS triage interpreter v4 (13-column grammar, A1)

Seat `R42C2Interp`, kaidoku-shokunin round 42 wave 1. Base
`c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`. Grammar per the L1's decision: 13 columns
with `failing handler` after `handler`; `handler` globs over F, `failing handler` globs
over HF, `dependencies` speaks the contains form.

| file | what it is |
|---|---|
| `sqfs-triage-v4.py` | the R42-C2 interpreter: reads only a SKILL-shaped document's `<!-- sqfs-triage-table v4 -->` block and REA envelopes, prints `(label, action)`. `--selftest` = 123 isolated cases. Source of record for `tools/round-42/sqfs-triage-v4.py` (the L1 moves it). |
| `probe-table-v4.md` | **test input, not block 21.** The draft precedence including A1, one row per clause, 13 columns, so the interpreter can be exercised while `SKILL.md` still carries only v3. Placeholder `cause`/`source` prose. |
| `measure.sh` | reproduction driver: selftest, probe-table parse, 12 real-envelope labels (v3 vs v4), 52 round-41 held-out envelopes, 4 round-41 C1 receipts, base-SKILL refusal. |
| `mutants.py` | 20 single-point mutants of the interpreter; a mutant survives only if its `--selftest` still exits 0. |
| `envelopes/` | 12 real REA 6.5.0 `extract-firmware` envelopes produced this seat from unblob 26.6.4 test fixtures (MIT). |
| `fixtures/` | the fixture bytes those envelopes came from (MIT; ≤ 4 KiB each) plus damaged/cut derivatives. |

## Fixtures: provenance and rebuild

unblob 26.6.4 (commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`), LFS media path
`https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/`:

| local file | upstream path | bytes | sha256 |
|---|---|---|---|
| `fixtures/v3-le-nopad.bin` | `squashfs_v3/little_endian/__input__/squashfs_v3.le.nopad.bin` | 320 | `314d4bbe07b83f491e9987d7db39d8560945b2ae273ed23ead7e9d92250deb3c` |
| `fixtures/squashfs_v3_be-squashfs_v3.bin` | `squashfs_v3/big_endian/__input__/squashfs_v3_be.bin` | 4096 | `4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c` |
| `fixtures/ddwrt-le-nopad.bin` | `squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3.le.nopad.bin` | 320 | `e7482db480f923189d649d6452d5c9c2cab267570dd88110dde2dfa1bdfa3b42` |
| `fixtures/v4-le-nopad.bin` | `squashfs_v4_le/__input__/squashfs_v4.nopad.bin` | 308 | `c72ddaa56a78b3d901a037acb47eb9be4b6f5303654cf3e7d5cfed1321fbd874` |
| `fixtures/v4-be-1kpad.bin` | `squashfs_v4_be/__input__/squashfs_v4.1kpad.bin` | 1024 | `d0bd6f90610d139aafe2f33f7002e742700d15c423f7b34c7292a220641cfa42` |

Fixture trap measured this seat: `squashfs_v3/little_endian/__input__/squashfs_v3_le.bin`
and `squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` are **byte-identical**
(both 4096 B, sha256 `0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7`),
so the file name in the ddwrt directory does not select the ddwrt handler; only the
`*.le.nopad.bin` there (magic `68737174`) reads `squashfs_v3_ddwrt`.

Derivatives (rebuild; no firmware bytes involved):

```bash
# fixtures/trunc-300.bin, trunc-180.bin  (superblock cut away -> unblob finds no chunk)
python3 -c "d=open('v3-le-nopad.bin','rb').read();open('trunc-300.bin','wb').write(d[:300])"
# fixtures/ff-200.bin, ff-120.bin        (tail overwritten -> extractor-failure, 0 files)
python3 -c "d=open('v3-le-nopad.bin','rb').read(200);open('ff-200.bin','wb').write(d+b'\xff'*120)"
# the container envelope: a tar holding one squashfs image (shape only; tar mtimes differ)
mkdir -p wrap && cp v3-le-nopad.bin wrap/firmware.bin && tar cf container.tar -C wrap firmware.bin
# the residue envelope: a squashfs image followed by 128 random bytes
python3 -c "d=open('v4-le-nopad.bin','rb').read();open('residue.bin','wb').write(d+open('rnd.bin','rb').read())"
```

## Envelopes: how they were made

Every envelope is a real `rea-agents@6.5.0` run, not synthetic. `cd` into scratch first
(unblob writes `unblob.log` into its cwd) and give REA a fresh output directory:

```bash
cd "$WORK"
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output --max-depth 1 <fixture> <fresh-outdir>
```

For the three dependency envelopes the child PATH deliberately lacked `$HOME/.local/bin`
(so `sasquatch` is unreachable) with `REA_UNBLOB_COMMAND` still absolute:

```bash
PATH=/usr/bin:/bin:$(dirname "$(command -v npx)") \
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output <fixture> <fresh-outdir>
```

| envelope | source | observed features | v3 pair | v4 pair |
|---|---|---|---|---|
| `rea-v3-le-nopad.json` | v3 LE nopad | H=`squashfs_v3`, G=`depth-limited`, P=4, BE=`n/a` | `unclassified` / `none` | `depth-limited` / `raise-depth` |
| `rea-squashfs_v3_be-squashfs_v3.json` | v3 BE | H=`squashfs_v3`, G=`depth-limited`, P=2 | `unclassified` / `none` | `depth-limited` / `raise-depth` |
| `rea-ddwrt-le-nopad.json` | v3 DD-WRT LE nopad | H=`squashfs_v3_ddwrt`, G=`depth-limited`, P=4 | `unclassified` / `none` | `depth-limited` / `raise-depth` |
| `rea-ff-200.json` | v3 LE nopad, tail `0xff` from 200 | H=`squashfs_v3`, G=`extractor-failure` (gap handler `squashfs_v3`), P=0, BE=`no` (argv `sasquatch -le -no-exit-code -f -d …`) | `unclassified` / `none` | `legacy-body-failure` / `cross-read-legacy` |
| `rea-ff-120.json` | same, from 120 | as above | `unclassified` / `none` | `legacy-body-failure` / `cross-read-legacy` |
| `rea-trunc-300.json` | v3 LE nopad cut to 300 B | no chunk, no gap, P=0 | `no-squashfs-chunk` / `inspect-input` | `no-squashfs-chunk` / `inspect-input` |
| `rea-trunc-180.json` | cut to 180 B | no chunk, no gap, P=0 | `no-squashfs-chunk` / `inspect-input` | `no-squashfs-chunk` / `inspect-input` |
| `rea-nodep-v3-le-nopad.json` | v3 LE nopad, no sasquatch on PATH | H=`squashfs_v3`, G=`missing-extractor-dependency`, D=`[sasquatch]` | `unclassified` / `none` | `dep-missing-le` / `install-extractor-le` |
| `rea-nodep-v4-le-nopad.json` | v4 LE nopad, no sasquatch on PATH | H=`squashfs_v4_le`, D=`[sasquatch]` | `dep-missing-le` / `install-extractor-le` | `dep-missing-le` / `install-extractor-le` |
| `rea-nodep-v4-be.json` | v4 BE 1kpad, no sasquatch on PATH | H=`squashfs_v4_be`, D=`[sasquatch-v4be]` | `dep-missing-be` / `install-extractor-be` | `dep-missing-be` / `install-extractor-be` |
| `rea-container.json` | `container.tar` at `--max-depth 1` | H=`[tar]` (F=∅), G=`depth-limited`, P=1 | `no-squashfs-chunk` / `inspect-input` | `container-depth-limited` / `raise-depth` |
| `rea-residue.json` | v4 LE nopad + 128 random bytes | H=`[null, squashfs_v4_le]`, G=`unknown-chunk-handler`, P=5 incl. `308-436.unknown` | `unclassified` / `none` | `unknown-residue` / `isolate-residue` |

## Results recorded this wave

| check | command | result |
|---|---|---|
| selftest | `python3 -I -B sqfs-triage-v4.py --selftest` | `SELFTEST cases=123 pass=123 fail=0`, exit 0 |
| probe table | `… --skill probe-table-v4.md --table-only` | 15 rules, 14 action tokens, exit 0 |
| base SKILL refused | `… --skill $LANE/SKILL.md --table-only` | exit 2, names the refused v3 marker |
| real envelopes | `measure.sh` §3 | 12 labels; the v3 table differs on 8 |
| round-41 held-out | `measure.sh` §4 | `compared=52 identical=52` |
| round-41 C1 receipts | `measure.sh` §5 | 4/4 identical (`depth-limited` / `raise-depth`) |
| mutants | `python3 -I -B mutants.py --work "$TMPDIR"` | `MUTANTS total=20 killed=20 survived=0` |
| CTL-C2-0b | `… --skill controls-ctl-c2-0b.md <12 envelopes>` | 7 `unclassified`, 3 `no-squashfs-chunk`, 2 correct — do-nothing |

## Rerun

```bash
WORK=/fast/scratch/hyaku/kaidoku-r42/R42C2Interp/measure ./measure.sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r42/R42C2Interp python3 -I -B mutants.py --work "$TMPDIR"
```

Both honour `$TMPDIR`/`$WORK`; neither writes outside them. `measure.sh` reads the v3
control interpreter from the base commit (`git show c4a38ea:tools/round-41/sqfs-triage-v3.py`,
sha256 `6ad2b4e1638a2b5f883d7bed14f8863ad5396dbc1af64b7cd521720ea42b6aa4`), never from a
working tree that the L1 may be editing.
