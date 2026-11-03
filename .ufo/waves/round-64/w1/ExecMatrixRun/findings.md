# ExecMatrixRun — R64-C1 frozen matrix run (round 64, w1)

Claim: R64-C1 (depth, capability acquisition). Frozen instrument
`tools/round-64/jsc-route-matrix.py`, frozen predictions, 18 runs (2 artifacts × 3 d8 builds × 3 reps).

**Outcome: R64-C1 verified. exit=0, 18/18 runs match, 0 mismatches. One run only; no re-run performed.**

## Command (exactly as executed)

```
S=/fast/scratch/hyaku/kaidoku-r64/ExecMatrixRun          (TMPDIR="$S/tmp")
timeout 3600 python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-64/jsc-route-matrix.py \
  --probe /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-64/inputs/probe-electron.jsc \
  --typora /home/vgpnk/.local/share/kaidoku-jsc/inputs/atom.compiled.dist.jsc \
  --d8-match /home/vgpnk/.local/share/kaidoku-jsc/d8-14.8.178.14 \
  --d8-neighbour /home/vgpnk/.local/share/kaidoku-jsc/d8-14.8.178.1 \
  --d8-cross /home/vgpnk/.local/share/kaidoku-jsc/d8-14.7.173 \
  --view8-dir /home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src/View8 \
  --python /home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python --node node \
  --work "$S/matrix" \
  --out .../w1/ExecMatrixRun/matrix-run.json \
  > .../matrix-run.stdout 2> .../matrix-run.stderr
```

- shell exit: **0**
- matrix-run.stderr: **0 bytes**
- wall time of the whole shell job (pins + 18 runs): 383.54 s
- environment used by the run: node v24.21.0, python3 3.14.8, View8 venv `parse` 1.22.4

## Exit and counts (from matrix-run.json)

| field | value |
|---|---|
| exit | 0 |
| verified | true |
| runs_matching / runs_total | **18 / 18** |
| mismatches | **[] (none)** |
| receipts | 18 |
| skip_run | false |

## Instrument pin, before vs after

| when | sha256 |
|---|---|
| before run | `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` |
| after run | `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` |

Equal; the instrument was not modified. `pins-pre.txt` holds the independent pre-run `sha256sum` record;
`instrument-post.txt` holds the post-run one.

## Input and binary pins (pre-run `sha256sum`, all equal to PINS)

| item | sha256 |
|---|---|
| probe `probe-electron.jsc` | `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710` |
| typora `atom.compiled.dist.jsc` | `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9` |
| d8 D1 14.8.178.14 | `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` |
| d8 D2 14.8.178.1 | `4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8` |
| d8 D3 14.7.173 | `c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2` |
| D1 `snapshot_blob.bin` | `b5c418dc0c6006d8dc6f4ac9981182eecf783cd892ae4c4b4ba16977c17bf2bb` |
| D1 `icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` |
| View8 `view8.py` | `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c` |

`check_pins` passed (no refusal), so the run proceeded to the 18 cells.

## Per-run receipts (verbatim from matrix-run.json)

| artifact | build | rep | dump_rc | dump_bytes | view8_out_bytes | label |
|---|---|---|---|---|---|---|
| probe | D1 | 1 | 0 | 2882 | 213 | dump-ok\|view8-ok\|node-fail |
| probe | D1 | 2 | 0 | 2882 | 213 | dump-ok\|view8-ok\|node-fail |
| probe | D1 | 3 | 0 | 2882 | 213 | dump-ok\|view8-ok\|node-fail |
| probe | D2 | 1 | 0 | 2882 | 213 | dump-ok\|view8-ok\|node-fail |
| probe | D2 | 2 | 0 | 2882 | 213 | dump-ok\|view8-ok\|node-fail |
| probe | D2 | 3 | 0 | 2882 | 213 | dump-ok\|view8-ok\|node-fail |
| probe | D3 | 1 | 139 | 0 | null | dump-exit-139\|view8-skipped\|node-skipped |
| probe | D3 | 2 | 139 | 0 | null | dump-exit-139\|view8-skipped\|node-skipped |
| probe | D3 | 3 | 139 | 0 | null | dump-exit-139\|view8-skipped\|node-skipped |
| typora | D1 | 1 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D1 | 2 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D1 | 3 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D2 | 1 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D2 | 2 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D2 | 3 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D3 | 1 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D3 | 2 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |
| typora | D3 | 3 | 134 | 0 | null | dump-exit-134\|view8-skipped\|node-skipped |

## Predicted vs observed, per cell

| cell | predicted (frozen) | observed (all 3 reps) | match |
|---|---|---|---|
| probe\|D1 | dump-ok\|view8-ok\|node-fail | dump-ok\|view8-ok\|node-fail | yes |
| probe\|D2 | dump-ok\|view8-ok\|node-fail | dump-ok\|view8-ok\|node-fail | yes |
| probe\|D3 | dump-exit-139\|view8-skipped\|node-skipped | dump-exit-139\|view8-skipped\|node-skipped | yes |
| typora\|D1 | dump-exit-134\|view8-skipped\|node-skipped | dump-exit-134\|view8-skipped\|node-skipped | yes |
| typora\|D2 | dump-exit-134\|view8-skipped\|node-skipped | dump-exit-134\|view8-skipped\|node-skipped | yes |
| typora\|D3 | dump-exit-134\|view8-skipped\|node-skipped | dump-exit-134\|view8-skipped\|node-skipped | yes |

The two cells that were unobserved before the freeze both matched: `probe|D2` (dump-ok / View8 / node-fail,
2882 B / 213 B) and `typora|D2` (134).

## Observations (context for the label result, not a re-prediction)

1. **Probe dumps are equal-length but not byte-identical across reps.** All six `probe-D1/D2-*` dumps are
   2882 B; their sha256 differ because heap addresses (the pointer-cage base) differ per process. The diff
   between reps is confined to address literals (`0x17d00101e221` vs `0x20000101e221` vs `0x1ca30101e221`,
   plus the maps/ConstPool/BytecodeArray addresses). The instruction stream, opcodes and byte offsets are
   identical. The same holds against the pre-freeze receipt `l1/prefreeze-probe/dump-probe.txt`
   (2882 B, sha256 `cd06b72a6ca75121cf3ccd938e6935f1203af51cd40a6793b7aa27207be89307`): same structure, different
   addresses. The frozen predicate counts labels, not dump bytes, so this does not affect the verdict; it
   does mean the per-cell `dump.txt`/`reconstruction.js` copies are not byte-stable receipts.
2. **View8 reconstructions** are 213 B in all six dump-ok cells, differing only in the same embedded
   addresses (`function func_sfi_<addr>()` and `ConstPool[0:0x… <FixedArray[4]>]`). Content class:
   `function func_sfi_<addr>()` + `ACCU = DeclareGlobals(...)`, `ACCU = ConstPool[1:"add"](1, 2)`,
   `r0 = ConstPool[2:"mul"](3, 4)`, `return ConstPool[2:"mul"](3, 4)`. `node --check` fails (label
   `node-fail`), consistent with the plan's "pseudo-Ignition text, not parseable JavaScript".
3. **probe×D3 crash class:** `dump.err` begins `Received signal 11 SEGV_ACCERR 32fdfff6fffc`, 646 B, 0 stdout
   bytes; identical label in all 3 reps.
4. **typora crash class on all three builds:** `dump.err` line 1 is
   `gen/third_party/libc++/src/include/__vector/vector.h:416: libc++ Hardening assertion __n < size() failed: vector[] index out of bounds`,
   then `Received signal 6` → 134. The assertion text is identical on D1, D2 and D3 (stderr sizes 4819 /
   4766 / 4660 bytes; stack traces differ by build). The crash is build-independent across the three named
   builds, including the cross-minor one.
5. No `--skip-run` control was re-run (already committed at `l1/c1-before-donothing.json`, 0/18, exit 1) and
   no selftest was re-run; this seat's task was the single matrix run.

## Retained artifacts (this directory)

| file | size | sha256 |
|---|---|---|
| `matrix-run.json` | 3970 | `c65f81b52f78d2cf9c8938b173aaf4316d1993ed4f34f8d8ba2213b264015f8d` |
| `matrix-run.stdout` | 3970 | `c65f81b52f78d2cf9c8938b173aaf4316d1993ed4f34f8d8ba2213b264015f8d` (identical to the JSON) |
| `matrix-run.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `pins-pre.txt` | — | `383f29dd88a035902280a8c829fe9250660a12a680b31b5df6f367da0a176f45` |
| `instrument-post.txt` | — | `d0a5819bb454bca3595f62784690e6b81becdf8d712a60182f99b3b97763de60` |

`cells/<artifact>-<build>-r<rep>/` holds `dump.txt` and `reconstruction.js` copies where each file is
under 2 MB: 6 × `dump.txt` (2882 B) and 6 × `reconstruction.js` (213 B) for the probe D1/D2 cells, and
12 × empty `dump.txt` (0 B) for the crashing cells. No file exceeded the 2 MB cap, so nothing was skipped
for size. Empty dumps are retained as proof of 0-byte stdout.

## Scope and hygiene

- Instrument and `claims/round-64-claims.md` untouched (hashes above; no edits made).
- No second matrix run; diagnosis needs none, since no mismatch occurred.
- No tool installed or upgraded by this seat (node, python3, `parse`, d8 builds and View8 were already the
  frozen toolchain).
- Scratch `/fast/scratch/hyaku/kaidoku-r64/ExecMatrixRun` deleted after copying the cell artifacts.
