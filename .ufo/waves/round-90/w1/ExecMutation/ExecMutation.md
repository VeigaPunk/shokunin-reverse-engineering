# ExecMutation — round-90 kaidoku w1

Declared-case mutation table over the two round-90 instruments
(`tools/round-90/upx-break-repair.py`, `tools/round-90/upx-later-block-battery.py`).
Per assignment: each mutant is one exact textual edit on a scratch copy, scored by the
instrument's own `--selftest`; the targets never mutated. Scratch copies verified
byte-identical to the frozen claim pins before mutation (receipts `baseline-selftest.json`).

## Instrument inventory and installs

- Tools used: python3 (system), no install or upgrade required. Tooling rule (install
  ledger): none recorded — nothing was installed.
- Instruments copied from the lane, sha256s match `plans/round-90-claims.md` pins:
  repair `aaf3536ea2226ac8ec498603d50b7b1b4a57c5572c7edef4fcf0e2a91d35590b`,
  battery `84664f52afa0c03b38aca23552046fcf5e8e04056a597da7b2b06ef6d5eb8206`.

## Baseline (pristine) selftests

```
python3 -I -B <mirror>/tools/round-90/upx-break-repair.py --selftest
  → rc 0, SELFTEST cases=17 failures=0
python3 -I -B <mirror>/tools/round-90/upx-later-block-battery.py --selftest
  → rc 0, SELFTEST cases=8 failures=0
```
Receipt: `receipts/baseline-selftest.json`. Full replay of all 17 mutants from the
receipts alone: `receipts/replay-driver.py` (rebuilds mirror + edits from
`receipts/mutants.json` + reruns every selftest).

## Result: killed 2 of 17

- **Killed: M03, M07.** Both are repair-side. M03 (strictly-greater acceptance weakened
  `<=` → `<`) fails `intact-idempotent`, `anchor-class-composed`,
  `last-block-before-stop-unrepaired`: the intact fixture reaches `derive_break` with a
  chain-valid candidate at an offset past the true successor (derived 80 = the loader-stop
  position, total 400 = stored total, measured in
  `receipts/mut-behaviour/repair-tamper-battery.json`'s companion enumeration), so a
  grounded repair on uncorrupted bytes fires. M07 (block-0 handoff fallthrough replaced
  by a refusal) crashes `repair(clean)` (Refused escaping, selftest line 367) — the
  intact and last-block cases route through that fallthrough.
- **Survivors (15), each naming the missing case:**

| id | file | one exact edit | missing case |
|----|------|----------------|--------------|
| M01 | repair:219 | `if total != require_total:` → `if False and total != require_total:` (exact-total filter deleted) | a fixture whose stored chain under-accounts u_len (the **libz** shape kills the filter's class role): the synthetic fixture's only chain-valid candidate already equals u_len, so the answer doesn't change. Enumerated under the M01 lens: tampered input has exactly 1 chain-valid candidate {derived 24, total 400=u_len}; intact has 1 candidate but the r89 fallback (`stored==derived` ⇒ intact) absorbs it |
| M02 | repair:219 | `!=` → `<` (over-accounting accepted) | same missing case on the over-accepting side: no fixture has a chain-valid candidate with total > u_len |
| M04 | repair:210 | `… or derived == sc_p:` deleted (stored-value candidates enumerated) | stored value never both chains and passes downstream filters → assert `rec['candidates']` never enumerates it, or a fixture where it does |
| M05 | repair:210 | `derived <= su_p` → `0 < derived` (sz_unc bound deleted) | one successor only; r89 fallback applies its own bound on intact inputs → a fixture with a second chain-valid successor whose derived > sz_unc |
| M06 | repair:204-207 | successor method-byte clause deleted | no size-plausible wrong-method b_info in the fixture scan window → a decoy-successor fixture |
| M08 | repair:270 | `if found is None: return _block0(...)` → refusal | no selftest input reaches `longest_prefix → None` → an input whose every l_info candidate has sz_unc0 == 0 |
| M09 | battery:188 | `after = sorted(os.listdir(box))` → `after = ["in","out"]` (post-exit isolation listing fabricated) | battery selftest never calls invoke()/score() → an invoke() against a stub repair that plants a stray file, asserting `box_after == ['in','out']` fails |
| M10 | battery:435-437 | `blind_ok` proof dropped from `arms_ok["carrier_blind"]` | score()-level harness: blind_ok False with blind cases recovered ⇒ met stays False |
| M11 | battery:439 | no_work `== 0` → `>= 0` | score()-level harness: no_work recovery > 0 ⇒ met stays False |
| M12 | battery:440 | cheat_live `is True` → `is not False` | score()-level harness: cheat unblinded False/None ⇒ met stays False |
| M13 | battery:441 | cheat_killed `is False` → `is not True` | score()-level harness: cheat blinded True/None ⇒ met stays False |
| M14 | battery:448 | `all(arms_ok.values())` dropped from `met` | score()-level harness: any single control false ⇒ met stays False |
| M15 | battery:450 | `label == args.expect` → `len(label) > 0` (binding tautologised) | main()-level fixture run with wrong `--expect` ⇒ exit 1 / met_target False |
| M16 | battery:148 | window `block+4, block+8` → `block+4, block+12` (method/flags bytes admitted) | a repair output differing in the tampered b_info method/flags byte (+8..+11) that field_only must reject — the selftest flips a byte at blocks[2], far outside |
| M17 | battery:447 | `== len(p1) == 6` → `== len(p1)` (hardcount relaxed) | score()-level harness: P1 recovering len(p1) ≠ 6 ⇒ met False (the six is the declared population contract) |

Full table with old/new strings, mutated sha256s, selftest outputs, exit codes and the
fixture behaviour probes: `receipts/mutants.json`; per-mutant selftest stdout+stderr+rc:
`receipts/mut-selftest/M*.txt`; each mutated copy: `receipts/mut/M*-{file}`; behaviour
probes (intact/tamper1±/tamper2-last/tamper0-wrong/zeroed per mutant):
`receipts/mut-behaviour/repair-probes.json` and `repair-tamper-battery.json`.

## What the observed kills are actually proving

- The surviving battery mutants are not a counter defect: the battery's selftest only
  covers its pure helpers (layout, tamper, window_only, static tables — 8 cases). Every
  arms_ok / met / invoke / expect mutant survives by construction because those code
  paths are only exercised by the frozen four-carrier run. The kill power for the
  battery lives in the pinned run (packer + REA + bwrap + carriers), not in its selftest;
  each survivor names the score()-level fixture that would close the gap.
- The repair's selftest is much stronger (17 cases, synthetic 3-block fixture): it kills
  the two routing mutants and the weakened strictly-greater filter. The five
  derivation-filter mutants (M01, M02, M04, M05, M06) survive because the fixture has a
  unique chain-valid successor and the r89 intact-fallback (`stored == derived ⇒ intact`)
  redirects every intact-path deviation. Their declared-class guards (libz chain gap,
  in-range window, method plausibility) are enforced by the *counter's* frozen run +
  fixture design, not by the repair's selftest — those are exactly the cases a
  round-91 revision of the repair selftest should add (a chain-gap fixture for
  M01/M02, a bound/skip/method decoy fixture for M04/M05/M06).

## Commands (all run from `/home/vgpnk/Projects/shokunin`; instruments live under scratch, never the lane originals)

```
# mirror + baseline
mkdir -p /fast/scratch/hyaku/kaidoku-r90/ExecMutation/repo/tools
cp -r kaidoku-shokunin/tools/{round-87,round-88,round-89,round-90} /fast/scratch/hyaku/kaidoku-r90/ExecMutation/repo/tools/
cd /fast/scratch/hyaku/kaidoku-r90/ExecMutation/repo && \
  python3 -I -B tools/round-90/upx-break-repair.py --selftest          # rc 0
  python3 -I -B tools/round-90/upx-later-block-battery.py --selftest   # rc 0

# per mutant (17 dirs, one exact edit each, selftest only)
cd /fast/scratch/hyaku/kaidoku-r90/ExecMutation/mut/<ID> && \
  python3 -I -B tools/round-90/<file> --selftest
```

## Deliverable paths (absolute, inside the lane)

- Report (this file): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ExecMutation/ExecMutation.md`
- Wave-rendered report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ExecMutation.md`
- Receipts root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ExecMutation/receipts/`
  - `baseline-selftest.json`, `mutants.json` (17-row table), `replay-driver.py`
  - `mut-selftest/M{01..17}.txt` + `summary.json`
  - `mut/M{01..17}-{upx-break-repair|upx-later-block-battery}.py` (mutated copies)
  - `mut-behaviour/repair-probes.json`, `repair-tamper-battery.json`

## Limits

- Selftest-only scoring per assignment; the full four-carrier battery run (packer/REA/bwrap)
  was not executed against mutants — that is the L1's frozen-open gate, not mine.
- Scratch was removed after receipts were secured (rmtree of
  `/fast/scratch/hyaku/kaidoku-r90/ExecMutation`); the lane originals were never touched.
