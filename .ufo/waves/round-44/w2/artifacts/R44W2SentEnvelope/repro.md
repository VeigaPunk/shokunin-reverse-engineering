# R44W2SentEnvelope — reproduction recipe

All paths absolute. `S=/fast/scratch/hyaku/kaidoku-r44/R44W2SentEnvelope`;
`CL=$S/lane`; `PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.
Nothing below touches the lane; every git mutation names `-C "$CL"` after
`git -C "$CL" rev-parse --show-toplevel` prints `$CL`.

## 1. Clone and pin the measured revision

```
mkdir -p "$S" && cd "$S"
git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin lane
git -C "$CL" rev-parse --show-toplevel          # must print $CL
git -C "$CL" checkout -q --detach 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac
```

## 2. Baseline score at the measured revision (exit 1 confirmed)

```
python3 -I -B "$CL/tools/round-44/c1-counter.py" --root "$CL" \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --pkg65 "$PKG" \
  --work "$S/work-baseline" --json-out "$S/out/c1-at-55bcce69.json"
```

## 3. Accepted arm — receipts re-pathed outside the scratch tree

`gen_mut.py receipts` sets `parameters.output_directory` to
`/etc/kaidoku-r44/<id>/out` for all four receipts and re-mints `evidence_id` with
the frozen `tools/round-27/xpin-attribute.mjs` (the counter's own
`evidence_ids()`); `gen_mut.py manifest` points every manifest path field at
`/etc/passwd`, `/etc/shadow`, `/home/operator/...`.

```
python3 -B gen_mut.py manifest
git -C "$CL" add -- corpus/evidence/round-44/c1/manifest.json
git -C "$CL" -c user.name=fixture -c user.email=fixture@invalid commit -qm fixture-manifest
python3 -I -B "$CL/tools/round-44/c1-counter.py" --root "$CL" --rev "$(git -C "$CL" rev-parse HEAD)" \
  --freeze c48f8a4b --pkg65 "$PKG" --work "$S/work-manifest"
python3 -B gen_mut.py receipts
git -C "$CL" add -- corpus/evidence/round-44/c1
git -C "$CL" -c user.name=fixture -c user.email=fixture@invalid commit -qm fixture-receipts
python3 -I -B "$CL/tools/round-44/c1-counter.py" --root "$CL" --rev "$(git -C "$CL" rev-parse HEAD)" \
  --freeze c48f8a4b --pkg65 "$PKG" --work "$S/work-receipts"
```

Dev arm over the same four envelopes (no rerun; exit 0):

```
python3 -I -B "$CL/tools/round-44/c1-counter.py" --dev-arm \
  --arm-dir "$S/arms/accepted_absolute_outside" --root "$CL" \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --pkg65 "$PKG" --work "$S/work-devarm"
```

## 4. Rejected arms

`gen_mut2.py traversal` → `v1le` output_directory
`/fast/scratch/hyaku/kaidoku-r44/sub/../../../etc/out`, id re-minted.
`gen_mut2.py id_mismatch` → `v1le` output_directory `/kaidoku-r44/other-run/out`
with the id minted over `/kaidoku-r44/a-different-run/out`.

Each is committed (`git -C "$CL" commit`) and scored with the same counter
command at the new HEAD. Expected and measured: `carriers_matched 3`,
`failing ['v1le:run_provenance_ok']` and `['v1le:evidence_id_ok']`, exit 1.

## 5. c2 at the measured revision and at the tip

```
python3 -I -B "$CL/tools/round-44/c2-counter.py" --root "$CL" --rev 55bcce69 \
  --freeze c48f8a4b --work "$S/work-c2" --json-out "$S/out/c2-at-55bcce69.json"   # exit 0
python3 -I -B "$CL/tools/round-44/c2-counter.py" --root "$CL" --rev 8bb1090a \
  --freeze c48f8a4b --work "$S/work-c2tip"                                        # exit 2
```

## 6. Preflight gate

```
P=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/frozen-path-preflight.py
for rev in c48f8a4 55bcce69 c86ea508 8bb1090a; do
  python3 -B "$P" --root "$CL" --freeze c48f8a4 --rev "$rev" --pathspec tools/round-44
done
python3 -B "$P" --root "$CL" --freeze c48f8a4 --rev 55bcce69      # no pathspec → exit 1
python3 -B gen_mut2.py claims                                     # append to plans/round-44-claims.md
git -C "$CL" add -- plans/round-44-claims.md
git -C "$CL" -c user.name=fixture -c user.email=fixture@invalid commit -qm fixture-claims
python3 -B "$P" --root "$CL" --freeze c48f8a4 --rev "$(git -C "$CL" rev-parse HEAD)" --pathspec tools/round-44      # exit 0
python3 -B "$P" --root "$CL" --freeze c48f8a4 --rev "$(git -C "$CL" rev-parse HEAD)" --pathspec plans/round-44-claims.md  # exit 1
```

## 7. Function-level harnesses

`attack.py` and `attack2.py` import the counter bytes from `$CL` at 55bcce69 and
drive `provenance_ok`, `trusted_run_root`, `path_shape_problem`, `diagnostic_rel`,
`evidence_ids`, `oracle_rows`, `carriers_spec`, `oracle_tool_ok`, `parse_rubric`,
`check_script_paths` and `extract_tar`. `extract_tar` is exercised over a real
`git archive` of a fixture repo carrying `/etc/passwd` and `../../outside`
symlinks (fixture at `$S/fixture-archive`, extract at `$S/fixture-extract`).
