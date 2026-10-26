# R41W2ReproV3 — run log (exact commands, versions, exit codes)

Seat `R41W2ReproV3`, round 41 wave 2. Scratch
`S=/fast/scratch/hyaku/kaidoku-r41/R41W2ReproV3` (removed at end; everything cited here is
copied into this directory). All runs `cd "$S"` with `TMPDIR="$S"`. Lane
`L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No VCS mutation, no write outside this
artifact directory and the seat report.

## Toolchain observed

| tool | version | path | sha256 |
|---|---|---|---|
| rea-agents | 6.5.0 (`package.json`) | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | n/a (npx cache) |
| unblob | 26.6.4 (`unblob --version`) | `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` | `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` |
| sasquatch-v4be | 4.5.1 (`-version` → `unsquashfs version 4.5.1 (2022/03/17)`) | `/home/vgpnk/.local/bin/sasquatch-v4be` | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` |
| node | v24.21.0 | PATH | — |

No tool was installed, upgraded or moved by this seat.

## 1. Rebuild the V3 carrier from the pinned chain (freeze)

```
python3 -I -B $L/tools/round-41/fetch-vendor.py --root $L \
  --rev d764389e9cbe61b9d1b07538ff3bff02d50bb34f --cache "$S/cache" \
  --json-out <artifacts>/fetch-chain.json
```
exit 0, 9.3 s (2 HTTP 200). V3: image sha256 `770efb4e…5ab7`, member
`./var/tmp/filesystem.image` 30236680 bytes sha256 `87cc5d6b…a0f8`, carrier slice
30233394 bytes sha256 `c4f74f54…f872a` == the pin. (V4 also rebuilt, not this seat's item.)

## 2. Independent REA run — NOT via c1-run.sh

```
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output --max-depth 1 \
  "$S/cache/c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a.bin" \
  "$S/rea-out-V3" > "$S/rea-V3.json" 2> "$S/rea-V3.err"
```
exit 0, 1.2 s (`meta.duration` 1215 ms), stderr empty. Envelope `ok=true`,
`evidence_id ev_09e2c40d012614ee79fb2b2a1640981baae9d8bb8efe044095b0f3bfa7d8cd82`.
`jq -c .data` → `<artifacts>/fresh-V3-after.json` (sha256 `6dcb3ce2…8b55`).

## 3. Carrier layout probe (independent of the counter)

```
python3 -I -B <artifacts>/layout-v3.py $S/cache/c4f74f54…f872a.bin c4f74f54…f872a
```
exit 0 → `<artifacts>/layout-v3.json`.

## 4. Oracle cross-producer (third extractor, no `-be`)

```
$HOME/.local/bin/sasquatch-v4be -f -no-exit-code -n -d "$S/sqcheck/root" <carrier>
```
exit 0 → 8 regular files; set-equal to `oracle.tsv` (rel, sha256, size), 0 mismatches.
Negative control, same bytes with `-be`:
```
$HOME/.local/bin/sasquatch-v4be -be -f -no-exit-code -n -d "$S/sqcheck/root-be" <carrier>
```
exit 1, stderr `Reading a different endian SQUASHFS filesystem … read_id_table: failed to
read id table block / FATAL ERROR: File system corruption detected`, 0 files produced.

## 5. Comparison of committed receipt vs fresh run vs oracle vs non-regular table

```
python3 -I -B <artifacts>/reproduce-v3.py \
  --committed $L/corpus/evidence/round-41/c1/V3/after.json \
  --fresh "$S/fresh-V3-after.json" \
  --oracle $L/corpus/evidence/round-41/c1/V3/oracle.tsv \
  --nonregular $L/corpus/evidence/round-41/c1/V3/nonregular.tsv \
  --pin c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a \
  --json-out <artifacts>/reproduce-v3.json
```
exit 0 → `projection_ok true`, both receipts: `oracle_hits 8/8`, `gaps_ok true`,
`nonregular_unpublished_ok true`, `structural_ok true`, gap kinds
`{depth-limited: 1, unpublished-entry: 85}` on 95 non-regular rows.

## 6. Evidence id recompute (frozen package rule, not retyped)

```
git -C $L show d764389e9cbe61b9d1b07538ff3bff02d50bb34f:tools/round-27/xpin-attribute.mjs > "$S/xpin-attribute.mjs"
node "$S/xpin-attribute.mjs" --pkg65 <rea-agents-6.5.0 root> --pkg67 <same> "$S/v3.wrapped.json"
```
(`v3.wrapped.json` = `{"data": <committed after.json>}`)
→ stored `ev_26a93366…ebc17` == recomputed `ev_26a93366…ebc17`
(`<artifacts>/xpin-v3.txt`). The xpin tool bytes are identical at the freeze and in the
tree (`8ea63837…f708`).

Extra probe (not a claim clause): re-hosting the fresh receipt's two `output_directory`
fields onto the committed path and re-minting yields `ev_a141eed2…` ≠ committed id
(`<artifacts>/xpin-v3-rehosted.txt`), because rea-agents 6.5.0's `semanticProjection`
(`dist/domain/evidence.js:156-182`) also hashes `parameters.path`, every
`normalized_result.files[].path`, `raw_result.execution.args[…]` and the report task paths.
A full field diff of committed vs fresh (`<artifacts>/receipt-diff.txt`, 27 differing
leaves) is exactly those absolute-path fields plus the provider blob counter
(`3104447:1` vs `4168704:1`); no content, gap, diagnostic, unpublished, engine or
parameter leaf differs.

## 7. Frozen-set checks (read-only git)

```
git -C $L diff --stat d764389e… e9a24d07… -- plans/round-41-claims.md tools/round-41/* \
  tools/round-40/gen-squashfs.py .ufo/waves/round-41/c1/* \
  corpus/evidence/round-41/c1/{V3,V4,L3,L4}/{oracle.tsv,nonregular.tsv} \
  corpus/evidence/round-41/c1/{L3,L4}/carrier.sqsh
```
empty. V3 `after.json` first added by `5ca6941b…` (only commit touching it), which
`merge-base --is-ancestor` places after the freeze and before the measured revision
`e9a24d07…`; `git rev-parse e9a24d07:…/V3/after.json` ==
`rev-parse 5ca6941b:…/V3/after.json` == working-tree blob `b22d4b91…`, and
`git diff --stat e9a24d07 -- <that path>` is empty (file sha256 `3097cc27…3f150`).

## 8. Side observation: what the run leaves in the user output tree

The fresh REA output tree (`$S/rea-out-V3/firmware.bin_extract`) holds 8 regular files and 5
directories — no symlinks, no `dev/led`, and 4 of the oracle's 9 directories absent. A direct
unblob run with REA's argv (`--process-num 1 --depth 1 --randomness-depth 0`, exit 0, 0.6 s)
leaves 10 dirs (9 + its own `_extract` root), 8 files and all 85 symlinks, and creates no
device (unprivileged). So the receipt's 95 non-regular rows are inventoried from unblob's
tree while only regular files are published into the user output directory; the missing
directories are the ones left with no files. [INFERENCE] on the mechanism; observed facts:
both the committed and the fresh receipt list the same 95 rows with the same dispositions.
