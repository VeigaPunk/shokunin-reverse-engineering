# MidmapListStep — R18-MIDMAP-LISTSTEP (list-shaped `steps` under `--require-mid-maps`)

Seat: KaidokuR19.MidmapListStep (leaf, writer). Lane report; patch is the deliverable.
Base: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (observed: `git -C /tmp/kr19-MidmapListStep rev-parse HEAD`).
Clone: `/tmp/kr19-MidmapListStep`. Patch: `.ufo/waves/round-19/w1/patches/MidmapListStep.patch`
(sha256 `cdfea3b6…563b1b`, `git apply --check` OK on a fresh baseline checkout, one file, no `__pycache__`/`.pyc`).

## Defect (observation, confirmed)

`.ufo/waves/round-17/tools/receipt-validate.py:570-587` (pre-patch): the list branch at `:575-578`
`ok = any(isinstance(s, dict) and s.get("pin_checks") for s in steps)` accepted a pin check on *any*
step, while the object branch required `steps["analyze"]`. A list-shaped receipt could pass the
`--require-mid-maps` gate with the analyze step silently unpinned. No round-17/18 receipt is
list-shaped (23/23 checked: 8 r17 + 15 r18, all `steps` dicts), so no recorded result changes.

## Fix (patch, `.ufo/waves/round-17/tools/receipt-validate.py`)

- `:134-148` new `_is_analyze_step(step)`: a name-less list entry is the analyze step iff it declares
  `step`/`name == "analyze"` or its `argv` carries the literal `analyze` subcommand token
  (`carrier-run.py` always records `argv`; it names dict steps only via the mapping key, so a list
  producer has no other invariant identity).
- `:595-617` the require block now mirrors the object branch: for a list only identified analyze
  entries count (`ok = any(s.get("pin_checks") for _i, s in named)`); the finding `where` points at
  the found analyze entry (`$.steps[<i>].pin_checks`), else stays `$.steps.analyze.pin_checks`
  naming the missing identity. Finding code, count (`checks += 1`) and object-branch behaviour are
  unchanged — r18 receipts keep 360–372 checks.
- Docstrings `:36-39` and `:488-491` state the list rule (contract text, previously silent on lists).

## Red-before / green-after (observation)

Selftest cases added at `:1032-1090`: `carrier_flag_list_checks_off_analyze_red` (exit 1 +
`mid_checks_absent` at `$.steps[1].pin_checks`; pin check only on `inspect-go-binary`),
`carrier_flag_list_analyze_green` (argv identity), `carrier_flag_list_declared_name_green`
(`name` identity).

Same fixture through both modules (`/tmp/kr19-midmap-redbefore.py`, outside the patch; pre-fix
module extracted with `git show 8a8da7e…:…/receipt-validate.py`, sha256 `70672eb3…553d145`):

```
{"exit": 0, "finding_codes": [], "module": "pre-fix"}      # bug: off-analyze pin check accepted
{"exit": 1, "finding_codes": ["mid_checks_absent"], "module": "patched"}
EXIT=0
```

## Selftest (observation, required paste)

Baseline clone at B: `python3 -I -B receipt-validate.py --selftest` →
`SELFTEST: CLEAN cases=18`, `EXIT=0`.
Patched clone: same command → last line `SELFTEST: CLEAN cases=21`, `EXIT=0`.
Independently patched clean checkout (`/tmp/kr19-applycheck`, `git apply` of the delivered patch):
`SELFTEST: CLEAN cases=21`, `EXIT=0`, `receipt-validate.py` sha256 `9276b198…d563d45` (identical to the clone).

## Round-18 receipts under `--require-mid-maps` (observation; exits must stay 0)

`python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps <receipt>` per file
(15 files from `find .ufo/waves/round-18/runs -mindepth 2 -maxdepth 2 -name receipt.json`):

| receipt | exit | findings | checks |
|---|---|---|---|
| calib-aether | 0 | 0 | 372 |
| calib-notesmd-cli | 0 | 0 | 366 |
| real-kimi-webbridge | 0 | 0 | 366 |
| s1246-noswiss-methods | 0 | 0 | 360 |
| s1246-noswiss-nethttp | 0 | 0 | 366 |
| s1246-noswiss-nomethods | 0 | 0 | 360 |
| s1246-swiss-methods | 0 | 0 | 360 |
| s1246-swiss-nethttp | 0 | 0 | 360 |
| s1246-swiss-nomethods | 0 | 0 | 360 |
| s1250-noswiss-methods | 0 | 0 | 360 |
| s1250-noswiss-nethttp | 0 | 0 | 366 |
| s1250-noswiss-nomethods | 0 | 0 | 360 |
| s1250-swiss-methods | 0 | 0 | 360 |
| s1250-swiss-nethttp | 0 | 0 | 366 |
| s1250-swiss-nomethods | 0 | 0 | 360 |

Aggregate one invocation over the 15: `AGGREGATE EXIT=0`,
`{'invalid': 0, 'receipts': 15, 'unreadable': 0, 'valid': 15}`, `require_mid_maps=True`.

Regression on the r17 set (`find .ufo/waves/round-17/runs …`, 8 receipts): `R17 EXIT=1`,
`{'invalid': 8, 'receipts': 8, 'unreadable': 0, 'valid': 0}`, codes `mid_map_missing: 29` — identical to
the round-18 record (`w1/CarrierRunMidMaps.md:166`), i.e. the red stayed red for the old reason.

Note (observation about this harness's shell, not the tool): the shell expands `runs/*/receipt.json`
to include `runs/run-log.txt/receipt.json` even though `run-log.txt` is a regular file; that path made a
first aggregate exit 2 (`unreadable: 1`, correct behaviour for an unreadable receipt). The table above
uses `find` and is the valid 15-receipt set.

## Risks / limits (inference, labelled)

- List identity is a heuristic by necessity (`step`/`name` field or `argv` token). A future list
  producer that names steps only in some other field would fail closed (`mid_checks_absent`), not open.
- Multiple list entries that identify as analyze: any one carrying `pin_checks` satisfies the flag, as
  the object shape's single key cannot express multiplicity; stricter would be new policy, not this fix.
- The object branch and all recorded receipts are untouched, so r18's 15/15 gate result still holds by
  both modes.

## Commands run (exits observed)

1. baseline clone + `git rev-parse HEAD` → B; `--selftest` → `SELFTEST: CLEAN cases=18`, exit 0.
2. pre-fix extraction `git show B:…/pins.py`, `…/receipt-validate.py` → sha256 `70672eb3…`.
3. `python3 -I -B /tmp/kr19-midmap-redbefore.py` → pre-fix exit 0 / patched exit 1 (`mid_checks_absent`), harness exit 0.
4. patched `--selftest` → `SELFTEST: CLEAN cases=21`, exit 0.
5. 15 per-receipt `--require-mid-maps` runs → all exit 0 (table).
6. aggregate 15-receipt run → exit 0.
7. r17 aggregate → exit 1, 8 invalid, 29 `mid_map_missing`.
8. `git apply --check` on fresh baseline checkout → OK; applied-then-selftest → `CLEAN cases=21`, exit 0.

No tool installs or upgrades were made. No REA/Ghidra call, no carrier execution, no lane git write.
