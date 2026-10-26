# R40C2ReconMixed -- exact commands

Scratch root (removed before yield): `/fast/scratch/hyaku/kaidoku-r40/R40C2ReconMixed`
(`TMPDIR` and `WORK` pointed there; `HYAKU_SCRATCH=/fast/scratch/hyaku`).
`A` = this artifacts directory, `S` = the scratch root, `L` = the lane root.

No tool was installed, upgraded or moved. `npx rea-agents@6.5.0` was served from the
existing npx cache; `unblob` 26.6.4, `sasquatch` and `sasquatch-v4be` 4.5.1 were used
as installed. No pacman transaction ran.

## carriers (development only, fresh trees authored by mkdev.py)

```
python3 -I -B "$A/mkdev.py" --root "$S/carriers"
# = per case: python3 -I -B tools/round-39/gen-squashfs.py TREE OUT --endian le|be|avm --comp gzip|xz
python3 -I -B "$L/tools/round-39/sqfs-list.py" "$S/carriers/$n/carrier.sqsh" \
  --files "$S/carriers/$n/files.tsv" --symlinks "$S/carriers/$n/symlinks.tsv" --inspect
```

`dironly` / `clean-empty` (not in mkdev.py; assembled trees):

```
mkdir -p "$S/trees/dironly/onlydir"
python3 -I -B "$L/tools/round-39/gen-squashfs.py" "$S/trees/dironly" \
  "$S/carriers/dironly/carrier.sqsh" --endian be --comp gzip
mkdir -p "$S/trees/empty"
python3 -I -B "$L/tools/round-39/gen-squashfs.py" "$S/trees/empty" \
  "$S/carriers/clean-empty/carrier.sqsh" --endian be --comp gzip   # sqfs-list exit 2
```

`dirlink` (symlink-to-directory probe):

```
mkdir -p "$S/trees/dirlink/d1"; printf 'alpha\n' > "$S/trees/dirlink/a.txt"
ln -s d1 "$S/trees/dirlink/inlink"
python3 -I -B "$L/tools/round-39/gen-squashfs.py" "$S/trees/dirlink" \
  "$S/carriers/dirlink/carrier.sqsh" --endian be --comp gzip
```

## damage copies (development only)

```
python3 -I -B "$A/corrupt.py" IN OUT zero-id-table|bad-minor|flip-data-tail|zero-first-data
head -c 9000  "$S/carriers/mx7/carrier.sqsh" > "$S/carriers/mx7-trunc/carrier.sqsh"
head -c 18400 "$S/carriers/mx7/carrier.sqsh" > "$S/carriers/mx7-trunc2/carrier.sqsh"
```

## REA runs (one per carrier/arm)

```
export TMPDIR="$S" WORK="$S/rea"
bash "$A/runrea.sh" NAME after|before ABSOLUTE_CARRIER
# expands to:
#   export REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob"
#   before: PATH = PATH minus "$HOME/.local/bin"
#   cd "$WORK/NAME-ARM" && npx -y rea-agents@6.5.0 extract-firmware \
#     --format json --full-output "$INPUT" "$WORK/NAME-ARM/out"
```

All 21 runs exited 0 and printed a parseable `{ok,data,meta}` envelope
(`envelopes/<run>/run.json: exit_code 0, parsed true`).

## feature reads and row-order checks

```
python3 -I -B "$A/feat.py" --json ENVELOPE...            # features + v2 extras
python3 -I -B "$L/tools/round-39/sqfs-triage.py" --skill "$L/SKILL.md" ENVELOPE...  # v1 label
python3 -I -B "$A/ordercheck.py" --table A|B|C ENVELOPE...
```

Round-39 envelopes read (read-only) for comparison:

```
$L/corpus/evidence/round-39/c1/K1..K6/after.json
$L/.ufo/waves/round-39/w1/artifacts/R39C2ReconCorrupt/envelopes/{ta-v5-corrupt-block-length,tc-v2-zero-first-data-block}.envelope.json
$L/.ufo/waves/round-39/w1/artifacts/R39C2ReconMarker/envelopes/rea-TA-be-xz.json
$L/.ufo/waves/round-39/w1/artifacts/R39C2ReconDep/envelopes/{full-be-dirempty-gzip,full-be1-xz,full-le1-xz}.json
$L/.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json   (not rerun)
```
