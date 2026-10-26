# R39W2HeldReproD — run log (provenance attack on R39-C2 held-out H16–H20)

Scratch: `S=/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproD` (removed at exit; cited bytes copied here).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (`L`). Read-only git only. No VCS mutation.

## Environment (recorded, not asserted)

- `unblob 26.6.4` at `/home/vgpnk/.local/bin/unblob`; envelope engine
  `executable_sha256 = 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`
  (identical in committed and fresh envelopes and inside `run.json`).
- `sasquatch` and `sasquatch-v4be`: `unsquashfs version 4.5.1 (2022/03/17)`, both on `$HOME/.local/bin`.
- REA: `npx -y rea-agents@6.5.0`.
- `after` arm: shell `PATH` contains `/home/vgpnk/.local/bin` (position 4).

## Carrier custody

```
for h in H16 H17 H18 H19 H20; do cp $L/corpus/evidence/round-39/c2/heldout/$h/carrier.sqsh $S/hold/$h.sqsh; done
sha256sum $S/hold/*.sqsh
```

```
9a1ff456cfbd8707e8542ff28642438abc12d35a392e6f4fe91ef547e4ce17ac  H16.sqsh
ab8cca56c0d2e388799df32af3d44583f2b6a8da0c73449afd2f9a4b343edb58  H17.sqsh
9281fe20bfdbf30f3ce0c8ac93650799962fe3b0f347dc9ca66c91ec5c787edb  H18.sqsh
8cc715817f382e7ab6f8bb9b4e71f687e804d7674118c49d7414fc24855c2041  H19.sqsh
ed6a6964089670e90751532984816cb2ef89ecb1af10a2f941f264e423fe7a4d  H20.sqsh
```

All five equal the `sha256` fields in `heldout/manifest.json` (see `carrier-sha256.txt`).

## Fresh REA run (manifest arm = `after` for all five)

```
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  "$S/hold/$h.sqsh" "$S/repro/$h"
```

Exit code 0 for H16, H17, H18, H19, H20; `ok=true`; durations 2147/2122/2066/2191/2022 ms.
CLI stdout stored as `H16.json`…`H20.json`; the `data` object stored as `fresh-envelopes/H16.json`…`H20.json`.
Determinism re-run (H16, H19 into fresh outdirs) differs only in scratch paths + the producer's
monotonic `provider_id` counter (see `deepdiff.txt`).

## Labels

```
python3 -I -B $L/tools/round-39/sqfs-triage.py --skill $L/SKILL.md <envelope.json>
```

Output in `triage-labels.txt`; `--json` features/matched rows for the five fresh envelopes in
`triage-fresh.json`; all-20 committed-envelope run in `labels-all.json`.
Table at `SKILL.md:333-343`, marker line 333, 8 rules parsed, `--table-only` exit 0.

Table bytes at freeze vs worktree (rows after the marker, up to the first non-table line):

```
worktree block sha256 56bc6204ee597cb9d06978b024a290d71bb1dc982246650ce538523922fcef4f rows 10
freeze   block sha256 56bc6204ee597cb9d06978b024a290d71bb1dc982246650ce538523922fcef4f rows 10
IDENTICAL
```

`tools/round-39/sqfs-triage.py` sha256 `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2`
at freeze and in worktree. `tools/round-39/heldout-gen.py` sha256
`8b3eddf8225cfb1092726f2cabd78040f5ad765c5b4248c690a2d5bfad3cf5fc` at freeze and worktree =
`manifest.generator.sha256`; `tools/round-37/gen-squashfs.py` sha256
`1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5` = `manifest.generator.writer.sha256`.

## Envelope authenticity (evidence_id recomputation)

REA derives `evidence_id = "ev_" + sha256(canonical(semanticProjection(evidence)))`
(`rea-agents@6.5.0:dist/domain/evidence.js:156-182`, `dist/domain/canonicalDigest.js`). `eid.py`
reimplements that projection/digest; on all five committed envelopes the recomputation equals the
stored id (`MATCH`), so none of the five was edited after emission.

## s_minor differential control (scratch copies only)

Patch `s_minor` (bytes 30:32, BE) on copies of H19/H20 and re-run REA into fresh outdirs —
`s-minor-controls.txt`:

- H19 `s_minor=5` (as committed) → chunk `squashfs_v4_be`, `extraction_failed=true`, files 0,
  `FATAL ERROR: Block size too small.  File system is corrupt.`
- H19 `s_minor=1` (control) → same failure.
- H19 `s_minor=0` (control) → `extraction_failed=false`, 6 files, coverage `complete`, no gaps.
- H20 same three-way result.

unblob's v4-BE pattern pins only `s_major`:
`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py:523-529`
→ `73 71 73 68 [24] 00 04`, so `s_minor=5` still matches and the extractor runs.
