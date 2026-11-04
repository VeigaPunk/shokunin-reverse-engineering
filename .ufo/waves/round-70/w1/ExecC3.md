# Seat ExecC3 — R70-C3 carrier-evidence verification (round-70 w1, 2026-11-04)

Seat: independently verify R70-C3's carrier evidence from the host bytes. Full command log with
every observed value: `.ufo/waves/round-70/w1/ExecC3/verify.md` (raw REA JSONs preserved alongside
as `rea-orig.json` / `rea-packed.json`). Freeze `4737a542ae3b1b910d8fe43efbd572bc578b07c6`;
base `5cc845ca…`; HEAD `67217e09…`.

## What was re-derived (all from host bytes, no reliance on receipts for the measurement)

1. **Frozen state intact.** Freeze-blob `tools/round-70/packed-elf.py` sha256 `1601a5b8…` ==
   tree bytes == container `instruments` pin; claims.json blob `13e7afb5…` == tree; porcelain
   clean. The C3 instrument's frozen `CARRIERS` (4 rows incl. `dinit` kind `static-exe`, ceiling
   10, `min_orig_procedures` 1000) and `DECLARED_ORIG {jq:167, xxd:99, libz:184, dinit:1268}`
   match plan/A5 field-for-field. Base instrument at `5cc845ca…` hashes to its
   `loaded_by_counter` pin `4ac0d83b…` and carries 3 carriers with zero `static-exe` — the
   claim's before-world holds.
2. **dinit carrier.** `/usr/bin/docker-init` sha256 `0bd49c8d…` == pin; `file -L`: statically
   linked, stripped ELF64 x86-64 EXEC. UPX 5.2.0 (== A8 version pin; `/usr/bin/upx` bytes ==
   A8 sha pin `cf2f6e7c…`) `--best -q`: 851288 → 357784; `upx -d` → `cmp` byte-identical
   roundtrip; my packed copy sha256 `b67ce1bd…` **equals** the route's recorded `packed_sha256`
   (deterministic pack). `readelf -h`: orig 12 phdrs/28 shdrs, packed 6 phdrs/0 shdrs, both
   ELF64 LSB EXEC x86-64.
3. **REA counts** (pinned package, `package.json` == A8 pin `a5003023…`): original
   **1268/29/1111**, packed **3/3/5** — exactly the declared values, both `confidence: derived`.
   Ratio `round(10/1268,4) = 0.0079` ✓; all four class ceiling ratios ≤ 0.75.
4. **Other carriers.** jq `e81566…`, xxd `7b1e5d…`, libz `6c78c5…` host hashes == frozen table;
   route orig counts (167/30/190, 99/29/103, 184/29/199) bind to `DECLARED_ORIG` — 4/4 carriers
   pinned.
5. **Producer binding (supplementary, read-only).** Frozen checker over
   `.ufo/waves/round-69/l1/scores/c3-at-landing.json` at HEAD: exit 1, `met false`, `failing`
   names `instrument.sha256 4ac0d83b… != blob at 67217e09… (1601a5b8…)` and `target 3 != 4`.

## Boundaries
No tool installed (upx/node/file/readelf preinstalled; pacman untouched). Writes limited to
`w1/ExecC3/` + this file + scratch; scratch `/fast/scratch/hyaku/kaidoku-r70/ExecC3` removed;
`/tmp` unused; no mutating git/jj command (show/rev-parse/status only). Full-claim scoring
(`--check-receipt` at the measured revision, target 4 / carriers_matched 4 / control_ok) stays
with the L1's counting command at landing; this seat found nothing that would fail it.

VERDICT: met — R70-C3 carrier evidence independently re-derived from host bytes and matching the frozen declaration in every declared constant; no defect named.
