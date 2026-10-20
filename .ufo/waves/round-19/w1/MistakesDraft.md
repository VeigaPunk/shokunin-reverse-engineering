# MistakesDraft — round 19, wave 1 (read-only advisory seat)

Seat: `KaidokuR19.MistakesDraft`. Baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (claims.json `baseline`). Lane `refs/heads/main` observed at `85589ac` (contains baseline; `git merge-base --is-ancestor 8a8da7e… refs/heads/main` → 0). Lane writes: none. Git writes, `jj`, installs, tool upgrades: none. Scratch under `/tmp/kr19-MistakesDraft` was removed after use; the reproduction is in §Reproduction.

Observation vs inference: labelled inline. `fleet:` = `/home/vgpnk/Projects/shokunin/` root files.

## Findings

1. **Dead-seat count has three values in three records, and the SCORECARD's list is wrong in a second way.**
   - `SCORECARD.md:2462` (8a8da7e): "1 dead (GateSUMSRUNLOG …), 4 not returned at integration (GatePRODUCERREV, TruthREGISTRY, DecisionRuleApply, ShonenLines)".
   - Fleet report at filed commit `4338083`, `.ufo/reports/round-18/kaidoku.md:84`: dead = GateSUMSRUNLOG and GatePRODUCERREV (2); not returned = TruthREGISTRY, ShonenLines; "`DecisionRuleApply` … returned late and were integrated".
   - Erratum at `e9eec36`, `.ufo/reports/round-18/kaidoku.md:101`: "Dead seats in W2: 3 (GateSUMSRUNLOG, GatePRODUCERREV, TruthREGISTRY)".
   - Ledger, own command at 8a8da7e: `git show 8a8da7e:.ufo/waves/round-18/wave2-assignments.json` has 98 keys (`python3 … len(...)` → 98); `git ls-tree --name-only 8a8da7e -- .ufo/waves/round-18/w2/ | grep -c '\.md$'` → 94. The four assigned names without a `w2/<name>.md` are GatePRODUCERREV, GateSUMSRUNLOG, TruthREGISTRY, ShonenLines. `w2/DecisionRuleApply.md` exists (`git cat-file -e 8a8da7e:.ufo/waves/round-18/w2/DecisionRuleApply.md` → exit 0), contradicting SCORECARD:2462.
   - Retained failure text: `git grep -l 'zai/glm-5.3-flash' 8a8da7e -- .ufo/waves/round-18` → empty (exit 1). The 429 and usage-policy causes exist only in the fleet report and erratum prose. `wave2-result.txt` records spawn lines only (INFERENCE from its first lines; the closure seat reports the same).
2. **The strict baseline red state is real when run, and absent from the record.**
   - `SCORECARD.md:2451` (8a8da7e): "exit 1 at `9011581`" for `routed-defects.py --strict`.
   - `.ufo/waves/round-18/verification.json:387` label `routed-defects-baseline`: argv has `--rev 9011581…` and no `--strict`; stdout retained at `verify/routed-defects-baseline.stdout` (open 6, non-strict).
   - `verification.json:436` label `routed-defects-source-strict` runs at `db4bdb1…` (source), not at 9011581.
   - `git ls-tree -r --name-only 9011581 -- .ufo/waves/round-18 | grep -c routed-defects-baseline-strict` → 0.
   - Observed today in scratch (not retained): `--rev 9011581d84527ba34c675f9cf912e54d2e72d470 --strict` → exit 1, `open_count` 6; without `--strict` → exit 0.
3. **MIDMAP list branch is vacuous for analyze-step presence.** `git show 8a8da7e:.ufo/waves/round-17/tools/receipt-validate.py`: dict branch `:573-575` requires `steps["analyze"]` to carry `pin_checks`; list branch `:576-577` is `any(... s.get("pin_checks"))` over all steps; the finding `mid_checks_absent` is emitted at `:582`. Observed: calling `verify_mid_maps(..., require_mid_maps=True)` on the 8a8da7e module with a list-shaped receipt whose analyze step has no `pin_checks` and a sibling step does → codes `{mid_map_missing}`; the same content dict-shaped → `{mid_checks_absent, mid_map_missing}`. `mid_map_missing` comes from the probe's nonexistent map path and is not the subject.
4. **Validator digest check is format-only.** `git show 8a8da7e:.ufo/waves/round-18/tools/routed-defects.py:463-467`: `ok = isinstance(vs, str) and len(vs) == 64 and all(hex)`; the detail string says "format only; see limits". No comparison to a value. (Code reading, INFERENCE that a wrong 64-hex value passes; not run.) True value, observed today: `git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum` → `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`.
5. **PROVINCE pin drift is carried, and the gate that catches it is failing.**
   - `git show 8a8da7e:PROVINCE.md`: `:9`, `:16` (Devin `rea-agents@6.5.0`, `mcp_config.json:7`), `:17` (OMP `rea-agents@6.5.0`, `mcp.json:8`).
   - Live pin token, `grep -o` only (no file contents printed): `~/.config/devin/mcp_config.json` → `rea-agents@6.7.0`; `~/.omp/agent/mcp.json` → `rea-agents@6.7.0` (two occurrences). Kimi `~/.kimi-code/config.toml` → `rea-agents@6.7.0`, matching PROVINCE's Kimi line.
   - `.ufo/waves/round-19/evidence/c1-census-v10-before.txt:8,12,13,31,32` mark Devin/OMP `6.5.0 -> STALE`; `:112` `VERDICT: FAIL (stale=4 ambiguous=0 undeclared=2 unresolved=0)`, `:113` `exit=1`.
   - `corpus/lessons/round-18.md:89` records the 13:35:56 -03 config rewrite as outside the lane and "Freshness debt, not fixed this round". `SCORECARD.md:2455` says "not fixed".

## Draft

## Mistakes

| # | class | evidence | captured-by | fix (red-before named) |
|---|---|---|---|---|
| 1 | number-drift | R18-DEADSEAT-RECORD. `SCORECARD.md:2462` at 8a8da7e says "1 dead (GateSUMSRUNLOG …), 4 not returned at integration (GatePRODUCERREV, TruthREGISTRY, DecisionRuleApply, ShonenLines)". Fleet report `.ufo/reports/round-18/kaidoku.md:84` at `4338083` names 2 dead; the erratum at `e9eec36` line 101 names 3 dead. `wave2-assignments.json` has 98 keys; `w2/*.md` has 94; `w2/DecisionRuleApply.md` exists. No retained failure text for any dead seat. | `CORPUS.md` "A count carries its command" (`CORPUS.md:34-38`), prose only; no gate. The SCORECARD count carries no command. | Append a dated correction entry to `SCORECARD.md` (no edit at `:2462`) stating assigned 98 / reports 94 / dead 3 / not returned 1 (ShonenLines), with seat names and report paths; retain the failure causes as an evidence file. Red-before at 8a8da7e: `git show 8a8da7e:.ufo/waves/round-18/wave2-assignments.json \| python3 -c 'import json,sys;print(len(json.load(sys.stdin)))'` → 98, and `git ls-tree --name-only 8a8da7e -- .ufo/waves/round-18/w2/ \| grep -c '\.md$'` → 94. The SCORECARD's stated non-report total 1+4=5 ≠ 98−94=4, so the count check exits non-clean. |
| 2 | landing (INFERENCE) | R18-STRICT-BASELINE. `SCORECARD.md:2451` claims "exit 1 at `9011581`" for `routed-defects.py --strict`. `verification.json:387` retains only the non-strict baseline run (`verify/routed-defects-baseline.stdout`); the strict run at `:436` is at `db4bdb1`. `git ls-tree -r --name-only 9011581 -- .ufo/waves/round-18 \| grep -c routed-defects-baseline-strict` → 0. Reproduced today in scratch: `--rev 9011581 --strict` → exit 1, open 6; plain → exit 0. Routed at `corpus/lessons/round-18-verifier-spotcheck.md:195`. | `corpus/QUALITY.md:28` (#18: execution evidence retains argv, measured revision, stdout/stderr and exit). The red state was asserted in prose and not retained. | Retain `routed-defects-baseline-strict.{stdout,stderr,receipt.json}` at 9011581 with the exact argv. Red-before: `git ls-tree -r --name-only 8a8da7e -- .ufo/waves/round-18 \| grep -c routed-defects-baseline-strict` → 0 (exit 1, non-clean); after the fix it lists the three files. |
| 3 | vacuous | R18-MIDMAP-LISTSTEP. `.ufo/waves/round-17/tools/receipt-validate.py` at 8a8da7e: dict branch `:573-575` requires `analyze.pin_checks`; list branch `:576-577` accepts any step with `pin_checks`; `mid_checks_absent` at `:582`. Red-before observed by calling `verify_mid_maps(..., require_mid_maps=True)` on the 8a8da7e module: list-shaped receipt with analyze lacking `pin_checks` yields no `mid_checks_absent`; dict-shaped yields it. Routed at `round-18-verifier-spotcheck.md:193`. | `corpus/QUALITY.md:29` (#19 names the mid-map requirement). The flag that implements it carries the loophole, and no list-shaped red fixture is retained. | Require the step named `analyze` in the list branch and add a list-shaped red fixture. Red-before: `verify_mid_maps` on the list-shaped receipt at 8a8da7e yields no `mid_checks_absent` (observed); the CLI `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps <list-shaped-fixture>` is expected to exit 0 at 8a8da7e (NOT run by this seat; pin wiring unverified) and non-zero after the fix. |
| 4 | vacuous | R18-VALIDATOR-DIGEST. `.ufo/waves/round-18/tools/routed-defects.py:463-467` at 8a8da7e checks only that `validator_sha256` is 64 hex characters ("format only; see limits"); the value is never compared. True digest of `.ufo/waves/round-17/tools/receipt-validate.py` at 9011581 is `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f` (observed). Routed at `round-18-verifier-spotcheck.md:194`. | none. No QUALITY row requires a value-bound check. The fix-able-to-fail rule (`CORPUS.md` "A fix is shown able to fail") was not applied to this check. | Compare `validator_sha256` with `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py \| sha256sum`, and hash-bind each remapped copy in `validate16/summary.json`. Red-before: a fixture root whose `validate16/summary.json` carries `validator_sha256` = 64 zeros passes the check at 8a8da7e (INFERENCE from `:463-467`; the fixture is not run by this seat). The fix must report it failed. |
| 5 | reference-drift (cause: provider config rewrite outside the lane, INFERENCE) | R18 PROVINCE pin drift, carried. `PROVINCE.md:9,16,17` at 8a8da7e state Devin and OMP `rea-agents@6.5.0`. Live token (`grep -o`): Devin `~/.config/devin/mcp_config.json` and OMP `~/.omp/agent/mcp.json` both `rea-agents@6.7.0`. `.ufo/waves/round-19/evidence/c1-census-v10-before.txt:112-113` `VERDICT: FAIL … undeclared=2`, exit 1. `corpus/lessons/round-18.md:89`: "Freshness debt, not fixed this round". | `.ufo/gates/c1-census-v10.py` (ran and FAILed, `c1-census-v10-before.txt:112-113`), but the round disposed the result as carried rather than as a blocking red. | Rewrite PROVINCE's pin lines to live identities and add a pin-drift probe comparing PROVINCE's stated client pins to the live config files. Red-before: `.ufo/gates/c1-census-v10.py --root <LANE>` at 8a8da7e → VERDICT FAIL, exit 1 (`c1-census-v10-before.txt:112-113`); the fix must return exit 0 without widening any DATED range. |

Rows are unique incidents, one primary class each. Numbering is local to this draft; the L1 renumbers on integration.

## Reproduction

Harness for row 3, run from `/tmp` (module exported with `git show 8a8da7e:.ufo/waves/round-17/tools/receipt-validate.py > rv-8a8.py`; no lane write):

```python
import importlib.util, sys, json
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("rv818", "rv-8a8.py")
rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
pins = {"entries": {}, "taken_at_utc": "2026-10-20T00:00:00Z"}
def receipt(steps):
    return {"label": "probe", "carrier": {}, "steps": steps,
            "pins_pre": {"entries": {}, "taken_at_utc": "2026-10-20T00:00:00Z"},
            "retained_logs": []}
chk = {"entries": 0, "map_path": "/nonexistent/map.json", "map_sha256": "0" * 64}
list_shape = [{"name": "analyze", "argv": ["npx", "analyze"]},
              {"name": "inspect-go-binary", "pin_checks": [chk]}]
dict_shape = {"analyze": {"argv": ["npx", "analyze"]},
              "inspect-go-binary": {"pin_checks": [chk]}}
for name, steps in (("list", list_shape), ("dict", dict_shape)):
    f = []
    rv.verify_mid_maps(receipt(steps), pins, f, require_mid_maps=True)
    print(name, sorted({x["code"] for x in f}))
```

Observed output: `list ['mid_map_missing']` and `dict ['mid_checks_absent', 'mid_map_missing']`.

Row 1 red-before, observed: `98` and `94`, then the SCORECARD's stated total is `5`.

Row 2 and row 4 commands are listed in the table; row 2's `git ls-tree` gives 0 matches.

Routed-defects at 8a8da7e, run from `/tmp` against the lane root:
- `python3 -I -B routed-defects.py --root <LANE> --rev 9011581d84527ba34c675f9cf912e54d2e72d470` → exit 0.
- same with `--strict` → exit 1, `open_count` 6 (all six R17 defects open).

## Limits

- No CLI-level red run of `receipt-validate.py` (row 3) or `routed-defects.py` on a fixture (row 4): those need fixtures this seat may not write in the lane. Both are named as commands, not as observations.
- Row 5's live pins were read by `grep -o` of the pin token only; the census evidence is the 15:32 pre-round file, not a re-run.
- Installs/upgrades: none. Git writes: none. Lane files: unchanged.
