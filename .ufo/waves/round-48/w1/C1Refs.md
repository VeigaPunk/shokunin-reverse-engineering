# C1Refs — Round 48 citation clause

## Scope and evidence

Read the frozen claim file in full before investigating. Frozen revision: `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`.

Required citation set for a landing block: at least five resolving, line-selected, distinct paths in the allowed roots; must include `corpus/lessons/round-47.md:<valid range>` and at least one `corpus/knowledge/<entry>.md:<valid range>`. The entry should directly support a craft decision; the existing relevant precedent is `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` (QUALITY 77(a) precedent is noted by round-47 lesson lines 22-23). Additional citations should substantiate the two routed defects and counter semantics, e.g. `corpus/lessons/round-47.md:24-44`, `:103-120`, `plans/round-48-claims.md:41-76`, and `tools/round-48/meanings.py:<actual line range>`; use exact in-range selectors. This gives five distinct paths, includes both mandatory classes, and anchors expected arms by routed id.

`SKILL.md` currently has 24 craft blocks and no verdict-meaning marker (observed via read). Ran the required command at `--rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` with `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1Refs`; exit 1, stdout reports `marker_occurrences 0 != 1`, `marker_block_count 0 != 1`, battery skipped because structure fails. Receipt was written to `.ufo/waves/round-48/w1/C1Refs/receipt.json` after creating report directory.

The runner did not accept an out-of-lane `--json-out /dev/null`; it returned exit 2 with `--json-out outside the lane root: /dev/null`. This is path policy, not evidence about citation selector validation. No crafted forged-block fixture was run; exact out-of-range-selector result therefore remains unmeasured.

## Receipt metadata

Required counter invocation:
`HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1Refs python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C1Refs/receipt.json`
Exit 1. UTC time: not captured. stdout SHA-256: not captured. (The JSON receipt records counter fields but not the exact stdout envelope.)

First attempted invocation failed before producing a receipt because the report directory did not exist; it was then created and the required run above succeeded in producing the receipt.

## Files changed

Only this report and its receipt under the assigned wave report directory. No frozen source files were changed. No installs.
