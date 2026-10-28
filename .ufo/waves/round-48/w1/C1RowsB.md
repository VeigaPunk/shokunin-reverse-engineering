# C1RowsB — scoped findings

## Scope and execution record

- Frozen claims read in full before other commands: `plans/round-48-claims.md`, freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`.
- Axes: coverage, depth, calibration. Direct contribution is depth, attacking the C1 registry-meaning clause.
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` completed successfully (exit 0); `/tmp` 19%, `/var/tmp` 38%, `/fast/scratch/hyaku` 32%.
- Read-only source inspected: `tools/round-48/meanings.py` lines 57–62, 154–247, 303–463, 533–552; `SKILL.md` registry area.

## Attack: verdict maps use lexical classifications

`meaning_classes()` (`meanings.py:227-247`) searches each digit segment with broad regexes. Success accepts `met|clean|ok|green|pass|passed|verified|succeeded|wrote`; not-met accepts `not met|violation|red|fail|failed|no verdict|refusal|refused|unresolved`; unevaluable accepts `could-not-evaluate|unevaluable|could not evaluate|usage|error|absent|unreadable|refus`. Placeholder exclusion only targets `banana|nope|whatever`. Distinctness compares the lowercased segment strings, not their interpreted meanings.

This creates a semantic weakness: e.g. a success segment containing the negative phrase `not met` also satisfies the success regex because `met` is matched without negation handling. Similarly, each segment may contain irrelevant class tokens and pass its one required regex. This is a source-level review finding, **not** an observed counter result: no `meanings.py --rev ...` command or fixture was run. Exact forged registry fixture and execution evidence remain unavailable.

## Gates and status

- R48-C1 structural checks and battery: **not run**.
- R48-C2 and five-forgery battery: **not run**.
- No counter/mutation command was executed. No fixture was created, and no forgery result is claimed.
- No tools installed; no lane product or frozen file changed. Only this report was written.

## Artifacts and limits

- Report: `.ufo/waves/round-48/w1/C1RowsB.md`
- Receipts: none; no exact command/stdout hash/UTC receipt exists for counter checks because none were executed.
- Scratch fixture cleanup was not applicable.