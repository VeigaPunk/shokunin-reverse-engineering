# ExecC2 — R71-C2 independent rederivation (kaidoku round-71, wave w1)

Seat: ExecC2-3. Date: 2026-11-04. Python: `python3 -I -B` throughout. No tools installed; no
pacman use. Scratch `/fast/scratch/hyaku/kaidoku-r71/ExecC2/` (removed after findings were
copied here). Repo state observed: HEAD `46d9e311` (one commit past the freeze `b827a8b5`, the
wave-dispatch evidence commit); claims.json byte-identical to the freeze.

## Method (independent of the shipped builder)

Steps 2–3 were performed WITHOUT running `tools/round-71/forged-receipts.py`:

- Source material: `.ufo/waves/round-70/l1/scores/c3-at-landing.json` (rev `7c155617bb42dadf1725b88a06fe3f235c364f0a`).
- Relabel (my own `build-lying.py`): `rev → 4737a542ae3b1b910d8fe43efbd572bc578b07c6` and
  `instrument → {path: tools/round-70/packed-elf.py, rev: 4737a542…, sha256: 1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880}`,
  where `1601a5b8…` is the sha256 of the blob bytes of `git show 4737a542…:tools/round-70/packed-elf.py`
  (the git OBJECT id of that blob is `070010fa50aee93408264b6d3a35993e7c5bfb84`; the receipt
  field carries the content sha256, which is what both readers re-derive).
- Readers under test (extracted blobs, never edited): first cut = blob at `4737a542…` (764
  lines), superseded = blob at `7c155617…` (871 lines; adds the packer binding, the
  `before_ceilings` binding and the six evidence-field clauses). Both invoked as
  `--check-receipt <receipt> --root <lane> --rev 4737a542…` (the superseded reader is the
  7c155617 BYTES, the receipt is checked against the first-cut world — the declared topology).
- One lie per shape, chosen from the declared clause names alone (plan R71-C2 / claims.json A3).

## Six-row table (my own forgeries)

| shape | lie applied (exactly one field) | first cut | superseded | declared clause named |
|---|---|---|---|---|
| L1_unpacked-counts | carriers[0]=jq `.unpacked_counts.procedure_count` 167 → 168 | **rc 0, met** | **rc 1** — `jq: unpacked_counts {'procedure_count': 168, …} != orig_counts (the recovery arm is recover==orig)` | `unpacked_counts` ✅ |
| L2_packed-sha | carriers[1]=xxd `.packed_sha256` → 64×`0` | **rc 0, met** | **rc 1** — `xxd: packed_sha256 000…0 != declared 1727faf9…` | `packed_sha256` ✅ |
| L3_section-list | carriers[2]=libz `.section_count` → 3, `.upx_list_rc` → 1 | **rc 0, met** | **rc 1** — `libz: section_count 3 != 0` AND `libz: upx_list_rc 1 != 0` | `section_count` ✅ (+`upx_list_rc`) |
| L4_runs-argv | carriers[0]=jq `.runs.pack.argv` drops `--best` | **rc 0, met** | **rc 1** — `jq: runs.pack.argv […, '-q', '-o', …] lacks --best` | `runs.pack.argv` ✅ |
| L5_refusal | carriers[0]=jq `.refusal.packed_rc` 1 → 0 | **rc 0, met** | **rc 1** — `jq: refusal.packed_rc 0 (packed bytes must refuse)` | `refusal` ✅ |
| L6_format | carriers[3]=dinit `.format.type` `EXEC (Executable file)` → `DYN (Position-Independent Executable file)` | **rc 0, met** | **rc 1** — `dinit: format {…'DYN (Position-Independent Executable file)'} != readelf of the pinned source {…'EXEC (Executable file)'…}` | `format` ✅ |

**Honest relabel control** (relabel, no lie): first cut rc 0 met=true AND superseded rc 0
met=true — the relabel alone is sound in both worlds; only the single lie trips the superseded
reader. Machine output: `lying-rederive.json`. My receipts: `lying-receipts/*.json` +
`lying-receipts/manifest.json`. Builder + runner: `build-lying.py`, `run-checks.py`.

## Shipped battery (step 4) — command verbatim from the predicate/assignment

`--rev b827a8b5d54f2885ec9be7786389f356c59226ce --base-rev 5cc845ca… --first-cut-rev 4737a542…
--superseded-rev 7c155617… --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
--work <scratch> --json-out <findings>/battery.json`

### Run A — working-tree instrument bytes (sha256 `44b973f1edad28ed409fcd41f487c75e804d06ee6d24e3d7699e50c121cac1d5`)

**Exit 0, `ok: true`, failures [].** 10 base-world shapes (base reader accepts each: `base_rc 0
met`; landing reader rejects each naming its declared clause), **6 lying rows all
(first_cut_rc 0, superseded_rc 1, clause_found true)**, 2 landing-world identity shapes rejected
by the probe on `A5_carrier_record` false **with `A6_packer_pin` true**, genuine landing receipt
accepted by both frozen readers (checker rc 0 met; probe 6/6 arms), battery arms green
(`constant_validate_rc 1`, `floor_named` true, `work_dir_distinct` true, `wrong_pin_named` true,
`work_run_rcs [0, 0]`). Receipt: `battery.json`. Its six lying receipts copied to
`shipped-battery-lying-receipts/`.

### Run B — FROZEN instrument bytes (blob at `b827a8b5…`, sha256 `50bb190b3c0b91870bfcce74c9898167f961102c8381d1a2b0c70fe7df115c7f` = the claims.json pin)

**Exit 1, `ok: false`, failures 4:**

1. `F3L_relabelled-landing: frozen probe did not reject it on A5_carrier_record with A6 true (rc 1, arms {'A5_carrier_record': False, 'A6_packer_pin': False})`
2. `F9L_unknown-landing: frozen probe did not reject it on A5_carrier_record with A6 true (rc 1, arms {'A5_carrier_record': False, 'A6_packer_pin': False})`
3. `genuine landing receipt rejected by the frozen checker` (checker rc 1, met false; the receipt's own producer clause `rev 7c155617… != b827a8b5…` fires)
4. `genuine landing receipt rejected by the frozen probe` (probe rc 1, arms_passed 4 of 6)

Its six lying rows are STILL all (0, 1) + clause ✅; its ten base-world shapes ✅; its
`battery_arms` ✅. Receipt: `battery-frozen.json` (per-shape receipt paths under
`/fast/scratch/…/frozen-run/forged-receipts-_x2chaxd/` are run pointers, not evidence; the
clause strings are inline in the JSON; copies of the six lying receipts from this run's tempdir
are in `shipped-battery-lying-receipts-frozen/`).

### Root cause (the defect)

`tools/round-71/forged-receipts.py` at the freeze anchors the three LANDING-world invocations to
`--rev <measured>`:

- the landing-probe call for F3L/F9L (line ~326: `"--rev", rev`),
- the genuine-receipt checker call (line ~375: `"--rev", rev`),
- the genuine-receipt probe call (line ~378: `"--rev", rev`).

The landing material is bound to `7c155617…`, so at the declared `--rev b827a8b5…` the producer
clause `rev != <invoked rev>` always fires and the probe arms collapse to A6 false — the
predicate clauses "the genuine receipts still accepted by both frozen readers" and "the two
landing-world identity shapes rejected by the probe on A5_carrier_record with A6_packer_pin
true" are **unsatisfiable at the pinned bytes**. The round-70 tool bytes are identical at both
revs (packed-elf blob `9be15f77…`, contract-probe blob `803f6ed3…` at BOTH `7c155617…` and
`b827a8b5…`), so only the `--rev` anchoring differs.

An **uncommitted working-tree edit** (`git status`: ` M tools/round-71/forged-receipts.py`;
7 insertions / 6 deletions; sha256 `44b973f1…`) changes exactly those three call sites to
`superseded_rev` (`7c155617…`) and produces the declared green (Run A). `git log b827a8b5..HEAD`
touches the path in no commit (only `46d9e311`, wave dispatch); `claims.json` is unchanged and
still pins `50bb190b…`; the round-71 container has no `instrument_supersessions` entry. Diff
captured: `working-tree-drift.diff`.

### Do-nothing control observation

`.ufo/waves/round-70/l1/scores/c1-at-landing.json`: `shapes` = 10 rows, `landing_probe_shapes`
= 2 rows, `lying_shapes` ABSENT, rev `7c155617…` — matches the predicate's do-nothing clause
(12 forged rows, 0 lying-field rows).

## Verdict logic

- The C2 acquisition core — the six lying-field shapes exist, are accepted by the first cut and
  rejected by the superseded reader naming the declared clause — is verified THREE ways: my own
  builder, the shipped battery at the working-tree bytes, and the shipped battery's six lying
  rows at the frozen bytes (identical clause strings in all three).
- The declared predicate as a WHOLE ("exits 0 … genuine receipts still accepted … landing
  identities with A6 true") is **not met at the pinned bytes**: the frozen instrument fails its
  own battery at the declared argv. The only green state is an uncommitted post-freeze
  working-tree edit that contradicts the container pin. Per the kill rule ("a post-freeze
  instrument edit → not verified, reported") and A1 (no post-freeze edit of a pinned path
  without an appended `instrument_supersessions` entry and a re-taken pin), R71-C2 is
  **not verified as of this measurement — defect named, fix present but unpinned**. When the
  working-tree fix is committed, the pin must be re-taken and the supersession disclosed before
  the landing receipt is measured.

VERDICT: defect named — R71-C2's six lying-field shapes re-derive green independently (6× first_cut 0 / superseded 1 + declared clause; honest relabel passes both readers), but the FROZEN `forged-receipts.py` (pin `50bb190b…`) exits 1 at the declared argv — its genuine-receipt and F3L/F9L arms anchor to `--rev <measured>` instead of the landing world `7c155617…`, making "genuine accepted" and "A6 true" unsatisfiable at the pinned bytes; an uncommitted working-tree edit (`44b973f1…`) is the minimal fix and runs the battery green (exit 0, 10+6+2 rows) — pin re-take + supersession disclosure required at commit.
