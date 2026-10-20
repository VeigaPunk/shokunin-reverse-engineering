# MeasureR20

## Result

**Observation.** Added `.ufo/waves/round-20/measure.py`. It resolves REV and `--freeze`, reads tracked paths and blob identities from Git, runs `routed-r19.py --strict` and `verb-coverage.py` from REV-extracted source, and retains each JSON summary (`measure.py:2-11,60-118,132-231`).

**Observation.** C3 emits `first_failure_bound` and label IDs only where the prediction blob is identical at REV and freeze, the REV `receipt-validate.py --require-mid-maps` result is valid, and a parseable `runs/<label>/compare.json` is present. `matched`/IDs count matching bound labels; raw file and result counts are included (`measure.py:234-436`). Freeze resolution, JSON output, and the required `--freeze` argument are in `measure.py:439-471,646-671`.

**Observation.** The selftest uses only `tempfile.mkdtemp()` fixture repositories, covers freeze-equal/changed predictions, valid/invalid receipts, compare requirements, working-tree exclusion, absent tools, and invalid revisions (`measure.py:534-643`).

## Retained evidence and commands

- Clone base observed as `14f0260ad319ecc26994381b2415d5a999003375` (contract baseline; also returned by both clone setup and explicit `rev-parse`; contract `contract.md:8-14`).
- Required selftest: `SELFTEST: CLEAN cases=25`; exit **0**. The selftest invocation and stable cases are at `measure.py:558-643`; interface is specified at `contract.md:28-32`.
- Patch: `.ufo/waves/round-20/w1/patches/MeasureR20.patch`; cached diff stat: `1 file changed, 671 insertions(+)`.

Commands run and exits:

1. `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-MeasureR20 && git -C /tmp/kr20-MeasureR20 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-MeasureR20 rev-parse HEAD` — exit **0**; printed `14f0260ad319ecc26994381b2415d5a999003375`.
2. `git -C /tmp/kr20-MeasureR20 rev-parse HEAD` — exit **0**; printed `14f0260ad319ecc26994381b2415d5a999003375`.
3. `python3 -I -B .ufo/waves/round-20/measure.py --selftest` (cwd `/tmp/kr20-MeasureR20`) — exit **0**; exact last line: `SELFTEST: CLEAN cases=25`.
4. `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-MeasureR20 add -A && git -C /tmp/kr20-MeasureR20 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/MeasureR20.patch && git -C /tmp/kr20-MeasureR20 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit **0**; printed `1 file changed, 671 insertions(+)`.

No tools were installed or updated.

## Risks and blockers

**Observation.** `receipt-validate.py` is run from REV with the REV `pins.py` sibling; that validator rechecks file paths recorded in receipts, so referenced external bytes are live and can vary independently of the committed receipt (`measure.py:39-51`; shared interface `contract.md:76-81`).

**Inference.** The comparison record path `runs/<label>/compare.json` and optional `compare.exit` follow the prior runner's output convention (`round-19/run-carriers.sh:346-347`); round-20's shared interface names the compare tool and exit contract but does not specify the output filename (`round-20/contract.md:79-81`). No blocker identified.
