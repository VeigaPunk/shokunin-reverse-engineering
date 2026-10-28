# C1Census — round 48 frozen census findings

## Scope / provenance
Read the full frozen claims file before commands. Read-only analysis at declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` (HEAD confirmed equal). Existing lane modifications and untracked files were left untouched. Axes: census coverage, counter attack depth, exit evidence calibration. No packages installed.

## Fresh census derivation
Exact command:

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/census2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873
```

Exit 0. Output: `paths: 42`, `named_but_absent: []`; per-claims-file counts rounds 41–48: 12, 10, 9, 5, 6, 4, 4, 4. Stdout SHA-256 `af2ff1909f60efcfb8316c5bd69b19d68cce038d8c90c6ca3743ba6042eb1c1d`; UTC `2026-10-28T18:47:30.038829+00:00`. Committed census JSON SHA-256 `403b4c143b020f1a30905258543758b11992dbd2235358575fb09f63473d7b59`. Direct execution of committed `census_rederive()` confirms its entire derived census document equals committed `census2.json`.

Registry-path diff at freeze: 40 registry rows versus 42 census paths; missing `tools/round-48/meanings.py`, `tools/round-48/record2.py`; extra none; duplicates none. Thus frozen registry set does not meet clause 8.

## Counter run
Exact command:

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1Census python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C1Census/receipt.json
```

Exit 1; stdout empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). JSON receipt is `receipt.json`: missing craft marker, marker block count zero, battery skipped because structure fails first. This is expected pre-landing control, not evidence about a future landing.

## Counter defect and falsification
`meanings.py` lines 290–298: `census_rederive(files)` returns a dictionary (`census_text(read)`). Lines 429–444 compare `derived == doc["paths"]`, a dictionary with a list. Therefore the “fresh derivation equals committed census” predicate is false even when the frozen census is an exact fresh derivation (confirmed above). An otherwise structurally clean v3 artifact cannot pass that subclause without fixing the comparison. This defect also makes the synthetic attack tests red, but does not mask their specific failures:

* One-path drift fixture in memory: `wrong["paths"] = paths[:-1] + ["tools/round-48/not-real.py"]`. `score(..., profile="v3")` returned 1. Failures include missing fake path, extra original path, and the unconditional derived comparison.
* Duplicate row fixture in memory: `good_registry(paths + [paths[0]])`. Score returned 1; `registry_duplicates` reports `tools/round-41/c1-counter.py`; also reports unconditional derived comparison.

The attack driver imported only frozen counter bytes and used its in-module `good_block`, `good_registry`, `skill_text`, and `score` helpers, with census/registry fixtures in memory. No fixture files were created or lane bytes changed. These attacks establish drift/duplicate rejection but cannot establish counter green on a genuine structurally complete artifact because of the comparison defect. The counter's separate missing registry entries are independently established.

## Evidence
`receipt.json` is raw C1 freeze receipt. Census and attack receipts were captured in the command transcript; stdout/exit/time above retained. No fixture paths exist. Scratch `/fast/scratch/hyaku/kaidoku-r48/C1Census` was removed after report capture. No tests/build/lint run.
