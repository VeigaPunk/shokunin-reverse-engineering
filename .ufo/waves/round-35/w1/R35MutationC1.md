# R35MutationC1 — C1 mutation probe (round 35, wave one)

Seat: R35MutationC1 (UFO-FSD mutation tester). One plausible defect against the frozen C1
counter, built and run entirely in /tmp fixtures. Lane untouched except this report file.

## Probe setup

- Instrument: `tools/round-35/c1-coverage-counter.py`, sha256
  `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220` — matches the frozen
  instrument pin in `.ufo/waves/round-35/claims-canonical.json`.
- Freeze rev: `2323d197` (first commit adding `claims-canonical.json`; full
  `2323d197456f1328459d9420aff025cffbcb3e27`). `git diff --stat 2323d197 HEAD --
  .ufo/waves/round-35/claims-canonical.json` → empty: canonical file unchanged since freeze.
  History order verified: counters finalized at `a85ca674` before canonical claims at
  `2323d197`; do-nothing controls committed at `3ecf4298` before any data.
- Fixture: `git clone --no-local --no-hardlinks` of the lane → `/tmp/r35c1-mutation/lane-fixture`
  at tip `3ecf4298`. Green data commit `63147fbbf343bbce231386bf15d41f28a923b670` on top
  (simulated future measured revision, since C1 data has not landed at any revision):
  - `corpus/SOURCES.md`: S125/S129 rows appended after S106 (11-column registry format,
    status `mined`, opened `2026-10-25`, used-by naming the respective entry; anchor cells
    cite the prep captures with their sha256 prefixes);
  - `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md` and
    `corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md` created, each opening with
    the provenance trio (`source:`/`verified-at:`/`recheck:`) and citing its row;
  - `PROVINCE.md`: "Round-35 additions to Core" section appended (Round-32 table format,
    both entry paths named);
  - `corpus/README.md`: one coverage-map row appended naming both `.md` filenames.

## Detector baseline (pristine)

- Command: `python3 -I -B tools/round-35/c1-coverage-counter.py --root
  /tmp/r35c1-mutation/lane-fixture --rev HEAD --freeze 2323d197456f1328459d9420aff025cffbcb3e27
  --json-out /tmp/r35c1-mutation/receipt-pristine.json`
- Output: `C1_CLEAN revision=HEAD`, exit 0; receipt `pass:true`, `failing:[]`.
- Green baseline passes → the verdict below is conclusive, not inconclusive.

## Mutant (one plausible defect, smallest behavior-bearing point)

- Invariant challenged: predicate clause "…and PROVINCE.md and the README coverage map hold
  both entry filenames."
- Mutant commit `ee0d146fa3d641113c49a894ad86188311329c9e` (fixture): the round-35
  coverage-map row in `corpus/README.md` is deleted and replaced by a prose line that still
  contains both `.md` filenames (one-row diff, `a55f152c..df2ecd08`):

  ```
-| `.jsc` → source mapping (round 35) | `2026-10-25-r35-jsc2js-mapper-contract.md`, `2026-10-25-r35-jsc2js-release-inventory.md` | held — mapper contract + release inventory enter the `.jsc` → source mapping frontier |
+See-also (round 35): the jsc2js mapper contract is `2026-10-25-r35-jsc2js-mapper-contract.md` and the release inventory is `2026-10-25-r35-jsc2js-release-inventory.md`.
  ```

- Plausibility: a map row dropped during a README reflow while the filenames survive in a
  see-also note — the coverage map no longer "holds" the filenames, so the frozen predicate
  clause is violated.

## Expected vs actual

- Expected (from the frozen counter source): the README check is
  `if p.rsplit("/", 1)[1] not in readme` — a basename substring test over the whole README —
  so the mutant should pass (survive).
- Actual: `C1_CLEAN revision=HEAD`, exit 0; `receipt-mutant.json` `pass:true`, `failing:[]` —
  byte-identical receipt to the pristine run.

## Verdict: SURVIVED (coverage finding)

The frozen C1 counter cannot distinguish "the README coverage map holds both entry
filenames" from "the filenames appear anywhere in README prose": a mutant that violates the
predicate's coverage-map clause scores green. Per the probe charter this is a coverage
finding about the frozen instrument's fidelity to the predicate, not permission to change
the contract. Advisory for the score seat: a green C1 score attests README mention, not
coverage-map membership.

## Restoration evidence

- `git reset --hard 63147fbb…` in the fixture; mutant commit `ee0d146f…` left dangling
  (fixture is disposable /tmp scratch; the lane was never touched).
- `corpus/README.md` sha256 before mutation = after restore =
  `ce8a28f6866e8c7c36f244e8333ec0a206d0f09afd1ecb5f14ab99b0b4a59e1b`; git blob
  `a55f152cfd030fb0b85abe0947477fea1a8065c7` before = after; HEAD == green `63147fbb…`;
  `git status --porcelain` clean.
- Restored run: `C1_CLEAN revision=HEAD`, exit 0 (`receipt-restored.json`).

## Controls run (advisory context)

- Instrument selftest: `python3 -I -B tools/round-35/c1-coverage-counter.py --selftest` →
  `C1_SELFTEST: ok green=0 red=1`, exit 0.
- Lane-tip do-nothing (read-only, `--root <lane> --rev HEAD --freeze 2323d197456f…`) →
  exit 1: `C1_FAIL: entry_missing:…mapper-contract.md; entry_missing:…release-inventory.md;
  registry_row_missing:S125; registry_row_missing:S129; province_missing:…mapper-contract;
  province_missing:…release-inventory; readme_missing:…mapper-contract.md;
  readme_missing:…release-inventory.md` — matches the committed do-nothing control at
  `3ecf4298`.

## Additional observations (not mutations; advisory)

- The counter's README check requires the `.md`-suffixed basename, while the coverage map's
  existing convention lists entry stems without `.md` (e.g. the round-33 row
  `2026-10-23-r33-chpe-structural-profile`; existing `.md` strings in map rows appear only
  inside citation paths in state cells). The future data commit must include the `.md` form
  in the map row, or `readme_missing` fires at the measured revision.
- The receipt's `checks` map (`c1_0..c1_5`) is degenerate, observed on both a passing run
  (pristine/mutant/restored) and a failing run (lane tip): all six entries are `true` even
  while `pass:false` with 8 `failing` strings — the map never reflects failures; only
  `failing`/`pass` are meaningful in a receipt.

## Limits

- One mutation probe (charter: stop after the assigned probe). The fixture green state is
  seat-authored because C1 data has not landed anywhere yet; entry bodies are minimal
  fixture text, not the planned entries. Counter runs are read-only (`git show`/`ls-tree`);
  no lane file, ref, index or worktree state was modified (lane HEAD `3ecf4298` unchanged,
  tracked tree clean). Scratch: `/tmp/r35c1-mutation/` (clone, `probe.py`, four receipts,
  `probe-log.json`).
