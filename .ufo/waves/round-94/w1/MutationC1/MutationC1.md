# MutationC1 — round-94 instrument mutation probes (seat report)

Seat: MutationC1 (mutation-tester), lane kaidoku, round 94 w1. Godspeed axes named:
coverage (7 single-point mutants across both R94-C1 instruments), depth (writer-level
probes beyond the selftest for M1/M3, exit-propagation probe for M7), calibration
(pristine baselines run before every mutant verdict; baseline failure = inconclusive),
freshness (all bytes measured at the frozen declaration commit).
No clarifying questions, large parallel batches, no survivors kept.

## Setup (all work in scratch clone, lane untouched)

- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`
  `&& git -C "$S/clone" checkout -q dd4524916a0332bb65f83525532da1c1b8d709de`;
  `git rev-parse --show-toplevel` = `$S/clone` (asserted, OK); HEAD = dd4524916a03…9de.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r94/MutationC1`; `TMPDIR="$S/tmp"` on every run;
  deleted before yield. Seat dir holds this report + `receipts/`.
- Pristine instrument hashes at dd45249 (equal to the frozen pins in claims.json):
  v4 `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272`;
  agreement `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9`.
- Fixtures: L1 receipts copied from the lane working tree
  `.ufo/waves/round-94/l1/scores/` (c1-v4-{pos,F1,F2,F3}.{json,rc,stdout,stderr},
  c1-v4-agreement.json, c1-measured-revision.txt) to `$S/fixtures/pristine/`.
  Alteration is exactly one file per fixture, smallest behavior point:
  - `m4-rc`: `c1-v4-pos.rc` `0` → `1`.
  - `m5-label`: `c1-v4-pos.json` line 140 `"label": "repaired 12 of 12; …"` →
    `"TAMPERED-m5 receipt label no longer matches stdout"` (stdout untouched).
  - `m6-met`: `c1-v4-F1.json` line 132 `"met_target": false` → `true` (label/exit/rc/stdout untouched).
- Mutants: fresh copy per mutant inside the clone's `tools/round-94/`, one single-point
  edit each (file names `stop-boundary-repair-battery-v4-m{1,2,3,7}.py`,
  `c1-receipt-agreement-m{4,5,6}.py`). Public battery never run; selftests and fixture
  checks only, as tasked.

## Mutants (before-hash = pristine pin hash; after-hash)

| id | file | point mutated | after sha256 |
|----|------|---------------|--------------|
| M1 | stop-boundary-repair-battery-v4-m1.py | `_default`: bytes branch dropped (always `raise TypeError`) | `753c12bed4e9506d62c6ac9a3217e9be9ee589d34db605367b5d8135ddd44f4c` |
| M2 | …-v4-m2.py | `_default`: `return str(obj)` instead of raise | `95799c1e2d13fad596260f80043139bb49d7e52f33695d6e5aff946b29802a9d` |
| M3 | …-v4-m3.py | `write_receipt`: direct open(json-out), no `.tmp`, no `os.replace`, no cleanup | `a705da0c1827062437240dd2b1cdc06035270373cf0df3b35c62eeacb5adb068` |
| M4 | c1-receipt-agreement-m4.py | `.rc` file never read (gate `rc_text.isdigit()` and `int(rc_text)==s_exit` dropped) | `52f311eb005f7044eb6cbcda425e8d0618e40d8c2a0d889bbc4b8a8d53e5e059` |
| M5 | …-m5.py | agree: `rec.get("label")==s_label` term dropped | `dcabef6a81c54f270d45ecf96690b2147f5d7eb62217e9c209f4bc7add37590a` |
| M6 | …-m6.py | met_target ignored where the counter compares it: `met is s_met` dropped from agree AND `met is want_met` dropped from predicted | `877eaa60da1b7a0af1a46fbb0f5b319816131696590df17d55ca7b8019041ecc` |
| M7 | …-v4-m7.py | `main`: `return code` → `return 0` | `07c1a308d9381140db012f751f53ed9c238f731444091bee19c85bd3d7a03643` |

## Baselines (pristine; all green → no verdict below is inconclusive)

- `python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py --selftest --work $S/work/st-pristine`
  → rc=0, `SELFTEST cases=3 failures=0`.
- `c1-receipt-agreement.py --dir $S/fixtures/pristine --prefix c1-v4` → rc=0,
  counts_of_4 {valid 4, agree 4, predicted 4}, met True (matches L1's receipt).
- Pristine counter on altered fixtures (the "original exits 1" side of each kill):
  m4-rc → rc=1 (agree 3); m5-label → rc=1 (agree 3); m6-met → rc=1 (agree 3, predicted 3).
- Writer probes (in-process `write_receipt` into `$S/work/probes`):
  bytes payload → complete JSON, no `.tmp` left; `object()` payload → `TypeError`,
  no target, no `.tmp` left.
- Exit-propagation probe: `v3.score` patched to return `(1, receipt)`;
  pristine `main([--root clone --work W --expect x --json-out out])` → returns 1,
  receipt `exit` 1.

## Kill matrix (killed = mutant exits 0 where pristine exits 1 on the altered
fixture, or a mutant-only behavioral difference is observed by the probe)

| mutant | check | observed output | verdict |
|--------|-------|-----------------|---------|
| M1 | `--selftest` | rc=1; uncaught `TypeError: Cannot serialize object of <class 'bytes'>` at `_selftest` line 83 (`enc = _default(blob)`); no SELFTEST line printed | **KILLED** |
| M1 | write_receipt probe | bytes payload raises `TypeError`; no truncated file left (`.tmp` cleanup intact) — M93-e crash reproduced at writer level, but the atomic wrapper still prevents the truncated artifact | observed |
| M2 | `--selftest` | rc=1; `selftest unknown-type-raises: FAIL`, `SELFTEST cases=3 failures=1` | **KILLED** |
| M3 | `--selftest` | rc=1; `selftest unknown-type-raises: FAIL`, `SELFTEST cases=3 failures=1` (truncated `receipt-unknown.json` exists → case fails) | **KILLED** |
| M3 | write_receipt probe | `object()` payload → `TypeError` but truncated target left behind: 8 bytes, head `{\n "x": `, not valid JSON ("complete JSON or absent" violated) | observed |
| M4 | counter on pristine fixture | rc=0, 4/4/4 (mutant still passes clean data) | — |
| M4 | counter on m4-rc fixture | rc=0, counts 4/4/4 while pristine on same fixture rc=1 (agree 3) → tampered rc not caught | **KILLED** |
| M5 | counter on pristine fixture | rc=0, 4/4/4 | — |
| M5 | counter on m5-label fixture | rc=0, counts 4/4/4 while pristine rc=1 (agree 3) → tampered label not caught | **KILLED** |
| M6 | counter on pristine fixture | rc=0, 4/4/4 | — |
| M6 | counter on m6-met fixture | rc=0, counts 4/4/4 while pristine rc=1 (agree 3, predicted 3) → tampered met_target not caught | **KILLED** |
| M7 | `--selftest` | rc=0, `SELFTEST cases=3 failures=0` — selftest is blind to `main`'s return | survived this check |
| M7 | exit-propagation probe (patched v3.score → code 1) | pristine `main` returns 1 (receipt exit 1); M7 `main` returns 0 while its receipt records `exit` 1 → stdout/exit contract broken | **KILLED** |

**Survivors: none.** 7/7 mutants killed. Every verdict has a green pristine baseline;
no baseline failed, so no verdict is inconclusive.

Notes for the L1:
- M6 implementation choice: met_target is compared in two places (agree, predicted).
  Dropping only the agree term is NOT distinguishable by the met-changed fixture
  (predicted still rejects → mutant exits 1); the killable form ignores the field
  wherever the counter compares it, which is what was mutated and killed.
- M7's selftest blindness is itself a small finding: `--selftest` exercises writer
  helpers only (the claim already names this limit: "A helper-only green is not
  counted"). The public-CLI agreement check does bound M7 indirectly — a v4 that
  returns 0 with receipt `exit` 1 would leave `rc`=0 ≠ receipt `exit`, which the
  frozen agreement counter's `int(rc_text)==s_exit` term rejects (reasoned from the
  counter source, not run as a public battery run).
- M1 reproduces the round-93 M93-e crash mode on the v4 writer but confirms the v4
  atomic wrapper's cleanup: no truncated file is left even when serialization raises.

## Restoration evidence

The two pristine instruments in the clone were never edited (mutants are separate
copies); re-hashed after all runs:
- `tools/round-94/stop-boundary-repair-battery-v4.py` =
  `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272` (pin match)
- `tools/round-94/c1-receipt-agreement.py` =
  `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9` (pin match)

## Files written

- This report: `.ufo/waves/round-94/w1/MutationC1/MutationC1.md` (absolute:
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/MutationC1/MutationC1.md)
- `receipts/`: 10 agreement-counter outputs + stderr
  (`agr-{pristine,M4,M5,M6}-{pristine,m4rc,m5label,m6met}.out/.err`) and `probes/`
  (writer-probe artifacts: pristine-bytes.json, m3-unknown truncated file, M7 main
  receipts, etc.).
- Scratch `$S` (clone with mutant copies, fixtures, work dirs) deleted before yield.
- No tools installed or upgraded (none needed); no host changes; no lane file touched.
