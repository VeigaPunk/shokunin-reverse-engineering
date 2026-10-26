# REBUILD — R42C2Gen (`heldout-gen-v4.py`, amendment A1)

Everything below was run in round-42 wave 1. Toolchain measured, not assumed:

| tool | version / identity |
| --- | --- |
| rea-agents | 6.5.0 via `npx -y` |
| unblob | 26.6.4, commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` |
| sasquatch / sasquatch-v4be | 4.5.1 |
| python3 | 3.13 (the interpreter that ran every command here) |

`S` = a scratch directory (the generator never writes outside `--out`, `--scratch`
and the fixture cache). Always `cd "$S"` first: unblob and REA write `unblob.log`
into their cwd.

## 1. Fixtures

`fixtures.json` pins 14 distinct v1–v3 images (MIT, unblob 26.6.4 integration
fixtures) by URL + sha256. Two further fixture paths are byte-identical to one of
those 14 and are recorded under `duplicate_bytes` instead of being pinned twice
(`squashfs_v3_broadcom/big_endian/__input__/squashfs_v3_be.bin` == `v3-be`,
`squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` == `v3-le`).

Resolution order for each fixture: `--fixtures-dir/<id>--<file>`, then
`--fixtures-dir/<file>`, then the cache under `--scratch/fixtures-cache`, then the
pinned URL **only with `--fetch`**. Every candidate is sha256-checked.

The copies this report used are in `fixtures/` beside this file, already named
`<id>--<file>`. To commit them (L1 action, outside this seat's bounds):

```sh
mkdir -p corpus/evidence/round-42/c2/fixtures
cp .ufo/waves/round-42/w1/artifacts/R42C2Gen/fixtures/* \
   corpus/evidence/round-42/c2/fixtures/
```

## 2. Determinism selftest (no REA, ~1.5 s)

```sh
S=/fast/scratch/hyaku/kaidoku-r42/R42C2Gen; mkdir -p "$S"; cd "$S"
export TMPDIR="$S"
SEED=$(printf dev42 | sha256sum | cut -c1-40)      # e48947bb2a1542206bc6a324257b3500231946e3
python3 -I -B .ufo/waves/round-42/w1/artifacts/R42C2Gen/heldout-gen-v4.py \
  --seed "$SEED" --selftest \
  --gen tools/round-39/gen-squashfs.py \
  --scratch "$S" --fixture-pins .ufo/waves/round-42/w1/artifacts/R42C2Gen/fixtures.json \
  --fixtures-dir .ufo/waves/round-42/w1/artifacts/R42C2Gen/fixtures
# 17/17 checks pass, exit 0
```

## 3. Dev arm, end to end (78 REA runs, ~2.7 min)

```sh
S=/fast/scratch/hyaku/kaidoku-r42/R42C2Gen; mkdir -p "$S"; cd "$S"
export TMPDIR="$S"
SEED=$(printf dev42 | sha256sum | cut -c1-40)
python3 -I -B .ufo/waves/round-42/w1/artifacts/R42C2Gen/heldout-gen-v4.py \
  --seed "$SEED" --out "$S/dev42" --run --verify --gzip \
  --gen tools/round-39/gen-squashfs.py \
  --scratch "$S" \
  --fixtures-dir .ufo/waves/round-42/w1/artifacts/R42C2Gen/fixtures \
  --fixture-pins .ufo/waves/round-42/w1/artifacts/R42C2Gen/fixtures.json
```

`--verify` does three things and returns 1 if any of them fails:

1. every envelope's observed six-field tuple equals `carriers[].declared_features`
   (plus the two `declared_extras` facts);
2. `combo_unseen_majority` — at least half of the combos have an OBSERVED tuple
   outside the union of the named classes' declared tuples;
3. regeneration — the whole set is rebuilt from the seed into a fresh directory and
   `manifest.json`, every `carrier.sqsh` and every `tree.json` are compared byte for
   byte.

`build_set` itself refuses to emit a manifest whose declared combos miss the
unseen-majority binding (`--allow-unseen-minority` downgrades that to a warning and
exists only for inspection).

## 4. Individual probes behind the declared rules

`wave1-measurements.tsv` is the consolidated feature table of the 60 ad-hoc REA
probes (columns: input, depth, H, G, D, BE, SR, P). Command shape for one probe:

```sh
cd "$S"
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output --max-depth 3 <input> <fresh-outdir> > envelope.json
```

Dependency arm — strip `$HOME/.local/bin` from the child PATH, keep
`REA_UNBLOB_COMMAND` absolute:

```sh
PATH=$(python3 -c "import os;hb=os.path.realpath(os.path.expanduser('~/.local/bin'));print(os.pathsep.join(p for p in os.environ['PATH'].split(os.pathsep) if p and os.path.realpath(p)!=hb))") \
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output --max-depth 3 <input> <fresh-outdir>
```
