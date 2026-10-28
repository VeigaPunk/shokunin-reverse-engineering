# C1Gold — R48-C1 gold-artefact attack

## Axis
Depth: attack the frozen verdict-meaning and registry binding counter. Coverage and calibration are not assessed here.

## Result

The required gold-artefact score was **not run**. At frozen revision `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`, C1 reports 24 rule blocks, no marker (`marker_occurrences: 0`), and exits 1 on the missing marker. The mutation battery is skipped. This baseline result cannot establish whether a valid gold artefact passes; no gold-green or gold-red claim is made.

## Concrete counterexample

The semantic classifier is a regex-substring heuristic, not an exact binding: `meaning_classes()` at frozen `tools/round-48/meanings.py:227-247` accepts any distinct segment texts that contain one matching token for each digit's class. In particular, the verdict map:

`0=not met; 1=violation; 2=usage`

is accepted as `{0: success, 1: not-met, 2: unevaluable}`. `not met` matches `SUCCESS` via `\bmet\b`; `violation` matches `NOTMET`; `usage` matches `UNEVAL`; all three segment texts differ and contain no banned placeholder. Yet exit 0's stated outcome is explicitly not-met, the opposite of success. This is a direct semantic false-positive candidate for every registry row using that map. It doesn't depend on odd negation or incidental appended text.

The actual test was not executed against a valid registry fixture, so this is a source-grounded counterexample to the classifier's accepted language, not a reported counter exit code. The cheapest safe correction is exact structured meaning tokens or an explicit allowlist of whole segment values, rather than substring regexes; add the opposite-polarity map above to the mutation battery.

## Evidence

- Claims read in full: `plans/round-48-claims.md`.
- Frozen source evidence: `tools/round-48/meanings.py:57-62` (regex vocabularies), `:227-247` (classification), `:418-453` (registry score), `:491-528` (battery).
- Counter command (exact): `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C1Gold/receipt.json`
- Exit code: 1. Receipt reports `marker_occurrences 0 != 1`, `marker_block_count 0 != 1`; battery skipped (`artefact fails a structural clause first`).
- Stdout SHA-256: `95c01672c03b53ae18ce0f010af2b472b14d271d74a5bd0a84bd1fde4f2007fc` (canonical sorted/indented JSON receipt). UTC: `2026-10-28T18:47:34.606461+00:00`.
- Exact command saved as `counter-command.txt`; receipt saved as `receipt.json` here. No fixture repo was created, no files under frozen paths modified, and no tool installed.
- Disk-guard status was run before the counter; `/fast/scratch/hyaku` at 32% use.

## Completion caveat

The assignment explicitly requires constructing the minimal full valid artifact in a scratch copy, scoring it, and providing the fixture path. That step remains uncompleted. This report is a partial static attack only and must not be interpreted as the required measured gold-artefact result. No checks other than disk status and the frozen baseline counter were run.
