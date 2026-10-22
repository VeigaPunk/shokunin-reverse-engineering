# Round-29 freeze-gate mutation probe

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/freeze-gate.py`, tested in the isolated clone `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutFreezeGateV2/clone` at `18be864a528873b2b70d8c94e31f880290249e90`.

## Detector and baseline

The bounded detector was the same gate invocation for every row:

```sh
python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutFreezeGateV2/clone/tools/round-29/freeze-gate.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutFreezeGateV2/clone --rev 18be864a528873b2b70d8c94e31f880290249e90 --disclosures corpus/claim-freezes-v2.tsv
```

[Observation] Pristine run, 2026-10-22T20:21:15Z, exit 0:
`{"audited": 19, "claim": "R29-freeze-gate", "clean": 2, "disclosures": {"exact": 19, "mismatched": [], "missing": [], "of": 19, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}`

## Mutants

| Mutant (single behavior point) | Gate source SHA-256 while mutated | UTC run | Exit | Exact output excerpt and observed effect | Verdict |
|---|---|---|---:|---|---|
| `CLAIMS`: restrict regex to `claims.json` only | `a10a222af15f7827acac50fb21cd920e083069c1efd95a97833ea72371ab3ef4` | 2026-10-22T20:21:46Z | 1 | `{"audited": 16, "claim": "R29-freeze-gate", "clean": 1, "disclosures": {"exact": 16, "mismatched": [], "missing": [], "of": 16, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": ["round-14/claims-review.json", "round-15/claims-review.json", "round-28/claims-c2.json"]}`. Three variant claims are skipped; the ledger's corresponding rows become stray. | **Killed** by the disclosure check. |
| `PIN_KEYS`: omit `producers_not_counters` | `c8edc349100613c391121d76e990f93ecbeab54218e1837280e451d1a49acabd` | 2026-10-22T20:22:03Z | 1 | `{"audited": 19, "claim": "R29-freeze-gate", "clean": 1, "disclosures": {"exact": 17, "mismatched": ["round-28", "round-28/claims-c2.json"], "missing": [], "of": 19, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}`. `INSTRUMENT_UNPINNED` rises from 6 to 11; new findings are `tools/round-28/collect-c1.py`, `tools/round-28/collect-c2.py`, `tools/round-29/collect-c1.py`, `tools/round-29/collect-c2.py`, and `tools/round-29/make-carriers.py`. | **Killed** by changed findings disagreeing with the disclosure ledger. |
| `freeze_key`: always return `round-N` | `45f1c40763ad24087f90978119ac8057f29e47e8663e21379061920e201456ea` | 2026-10-22T20:22:17Z | 1 | `{"audited": 19, "claim": "R29-freeze-gate", "clean": 2, "disclosures": {"exact": 15, "mismatched": ["round-28"], "missing": [], "of": 16, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": ["round-14/claims-review.json", "round-15/claims-review.json", "round-28/claims-c2.json"]}`. Variant and canonical keys collide; the disclosure comparison loses distinct keys and reports a mismatch. | **Killed** by the disclosure check. |
| Sort key: use the round label string instead of `int(round-N)`; retain the remaining tie-breakers | `00234c753486f33f831dfba3bd02e1c498935aeee65b28c0ca60a01df2e15fdc` | 2026-10-22T20:22:36Z | 0 | Output was byte-identical to pristine: `{"audited": 19, "claim": "R29-freeze-gate", "clean": 2, "disclosures": {"exact": 19, "mismatched": [], "missing": [], "of": 19, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}`. stdout SHA-256 equals pristine. | **Survived**: numeric and lexical round order coincide for the observed round-14–29 set, so this invocation produces no observable change. |

[Observation] All four mutant stderr files were empty. The pristine and mutant outputs are actual gate JSON captured from the invocation above; each output file's SHA-256 is listed below.

## Selftest and overall verdict

[Observation] `freeze-gate.py` has no `selftest` or `--selftest` match. Its `main()` defines only `--root`, `--rev`, `--require-clean`, and `--disclosures` (lines 200–204).

[Inference] Regression detection is partial: this run killed the three mutations that altered audited coverage, pins/findings, or freeze keys, because the gate compared its results against `corpus/claim-freezes-v2.tsv`. It did not catch the sort-key regression, whose output remained identical for this dataset. There is no dedicated gate selftest to detect that unexercised sorting difference.

## Restoration and hashes

[Observation] Before mutation, the gate source SHA-256 was `25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2`. After each mutant, the scratch clone's gate file was restored with checkout from its target commit and had that same SHA-256. The final restored detector ran at 2026-10-22T20:23:14Z with exit 0; its stdout SHA-256 exactly matched pristine (`217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c`), and stderr matched the empty pristine stderr.

Raw output artifacts (all under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutFreezeGateV2/`):

| Artifact | SHA-256 |
|---|---|
| `pristine.stdout` | `217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c` |
| `claims-regex.stdout` | `3f9f15631d747cf92ccd9cc0eae3447965ec0d98eef95cf81465937d2d2ebcc1` |
| `pin-keys.stdout` | `d328103865736616974d1cd04703579fe908bb4afd9eb97950d84b43c71ec903` |
| `freeze-key.stdout` | `0262fd2d158431f12f4b70b301a318091549933d43fe312b101a2e37937792bd` |
| `sort-key.stdout` | `217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c` |
| `restored.stdout` | `217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c` |
| `pristine.stderr`, `claims-regex.stderr`, `pin-keys.stderr`, `freeze-key.stderr`, `sort-key.stderr`, `restored.stderr` | each empty; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Restored `clone/tools/round-29/freeze-gate.py` | `25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2` |

No tools were installed or updated.