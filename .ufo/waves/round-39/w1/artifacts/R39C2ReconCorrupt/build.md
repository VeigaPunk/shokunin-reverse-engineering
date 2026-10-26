# R39-C2 corruption recon — exact commands and carriers

Seat `R39C2ReconCorrupt`, wave `round-39 w1`, base `a2f64e1da78afcf8cc39287106604dbcc270844c`
(verified `git rev-parse HEAD`; only untracked `plans/round-39-claims.md` and `.ufo/waves/round-39/`
in the worktree). All work ran in scratch
`/fast/scratch/hyaku/kaidoku-r39/R39C2ReconCorrupt` (removed after the run) and every byte cited
here was copied into this directory.

## Environment

| tool | version | source |
|---|---|---|
| unblob | 26.6.4 | uv tool install, `/home/vgpnk/.local/bin/unblob` |
| rea-agents | 6.5.0 | `npx -y rea-agents@6.5.0` |
| sasquatch / sasquatch-v4be | 4.5.1 (`unsquashfs version 4.5.1`) | onekey-sec deb binaries in `~/.local/bin` |
| python3 | system | `-I -B` not required for these probes |

## Deterministic carriers (development only; never K5/K6, never held-out)

```sh
S=/fast/scratch/hyaku/kaidoku-r39/R39C2ReconCorrupt
mkdir -p "$S/trees" "$S/img" "$S/out"; export TMPDIR="$S"
python3 make-trees.py "$S/trees"          # ta tb tc td te tf, byte-deterministic
for t in ta tb tc td te tf; do
  python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-37/gen-squashfs.py \
      "$S/trees/$t" "$S/img/$t-be-gzip.sqsh" --endian be --comp gzip
done
for t in ta tb tc; do
  python3 .../gen-squashfs.py "$S/trees/$t" "$S/img/$t-be-xz.sqsh" --endian be --comp xz
done
```

Corrupted carriers: `python3 corrupt.py` (`corrupt(open(clean,'rb').read())`), or the five probe
variants in `probe-variants.py`. `run-matrix.json` records each carrier's sha256 and the offsets
`corrupt()` touched (`corruption_offsets`).

## REA runs (one fresh outdir each, no pre-existing dir)

```sh
cd "$S"
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
    --format json --full-output "$S/img/<carrier>.sqsh" "$S/rea/<run>"
```

Exit 0 for every run; envelopes are saved as `envelopes/<run>.envelope.json`, unmodified, with
`ok:true`, `data.evidence_id`, `data.normalized_result.*`, `data.raw_result.report`. The
`ta-clean-nodep` control ran the same command with `$HOME/.local/bin` removed from the child
`PATH`:

```sh
PATH="$CLEANPATH" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
    extract-firmware --format json --full-output "$S/img/ta-be-gzip.sqsh" "$S/rea/ta-clean-nodep"
```

## Direct sasquatch probes (before REA, to filter variants)

```sh
sasquatch-v4be -be -no-exit-code -f -d "$S/sq/<name>/out" "$S/img/<carrier>.sqsh"
echo $? > "$S/sq/<name>/exit"; # stderr copied to sasquatch-stderr/<name>.stderr.txt
```

`unblob-logs/ta-v1.unblob.log` is the unblob 26.6.4 debug log for the recommended corruption
(`Running extract command ... command='sasquatch-v4be -be -no-exit-code -f -d ...'`,
`Extract command failed ... exit_code=0x1`).

## Carrier hashes (sha256, full)

```
a4c5c05ef0008261116c0ba08cdc3675215caeba8888202830afe123d712e7c7  ta-be-gzip.sqsh
895b83d27b029945f1e8b94cd9b40bb88fda5e3d7892866fc1c9f690d1bd0d99  ta-be-gzip-v1.sqsh     (== ta-v1-zero-id-table.sqsh)
a8a5e2cd000c867c4a0b1157d572ce0f65de8a323fcf4054eea64ac82927daac  ta-be-xz-v1.sqsh
f5866951366128ca2cf6445e31027bd9c9b2cf21b9657151d3fb6f41393b3fda  tb-be-gzip.sqsh
6fb56e2dbf62021aa72dea5eb4edd947bd99aeaaac352eff84bfc985333d6a09  tb-be-gzip-v1.sqsh
4f0c6ddafb3051b9f9e156a3a25470594a6c98c2a06fc1553ec8b733d6464563  tc-be-gzip.sqsh
45f7ac03a219edd1ee0450933f81b2479633e006d61cbf971062abcebd59f0b0  tc-be-gzip-v1.sqsh
af2083e5229e24baa7fc9654afb1d791913d48aae9a3beda53b53ef1d066fe9c  td-be-gzip.sqsh
02f6155a45d7b5900657f8707cb7946c2adcc7eda96be8fa6eb3b490a9068d55  td-be-gzip-v1.sqsh
ae2df2044182fcd14df7fb3e8063ebc7bbd3a89dc85ee63c5ddccbc756d16e07  te-be-gzip.sqsh
8e37a8268f3464f1c909067d762328a772f6e391354ee00f34b1bfddc24c9682  tf-be-gzip.sqsh
```

Per-variant hashes: `sha256sum inputs/*.sqsh` (all 31 carriers are in `inputs/`).

## Files in this directory

| file | what |
|---|---|
| `corrupt.py` | **the deliverable**: `corrupt(image_bytes) -> bytes` (v1, zero the id table) + `describe()` + header guards |
| `probe-variants.py` | all five probed corruptions (v1-v5), offsets derived from superblock fields |
| `envelope_features.py` | computes H/G/D/BE/SR/P from an envelope (bare `data` or `{ok,data,meta}`) |
| `build-matrix.py` | regenerates `run-matrix.json` + `feature-table.md` from the saved envelopes only |
| `make-trees.py` | rebuilds trees ta/tb/tc/td/te/tf deterministically |
| `run-matrix.json` | 25 runs: features, carrier sha256, offsets, direct sasquatch exit/stderr |
| `feature-table.md` | the same matrix as a markdown table |
| `envelopes/` | 25 unmodified REA envelopes |
| `inputs/` | every clean and corrupted development carrier |
| `sasquatch-stderr/` | direct `sasquatch-v4be -be` exit codes and stderr per carrier |
| `unblob-logs/` | unblob debug log for the recommended corruption |
