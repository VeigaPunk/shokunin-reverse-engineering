# Round 48 frozen-instrument preflight — ExecGateRun

## Commands and receipts

Scratch used: `/fast/scratch/hyaku/kaidoku-r48/ExecGateRun`; disk guard status was checked before the counter passes. No tools installed. All commands were read-only; stdout below captured directly from frozen counters. UTC receipts record command, exit, stdout SHA-256 and capture time.

### C2

Command:
```sh
python tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873
```
Exit: **1**. UTC: `2026-10-28T18:51:02.567837+00:00`. SHA-256 of captured stdout: `4551553020459bbe56e3a6b2d91d6dc419757dd4005bd01d5ffa44ac569d69ca`.

Red lines (`failing`):
- `round-47: no seat atom and no re-derived seats correction`
- `no \`## Record corrections — round 48\` line re-derived`
- `quoted numbers with no backing receipt: 1`

Other material: oracle `mismatches []`, `met_target true`; `floor` has round-47 path 4, rev 13, window 1, claims R47-C1/R47-C2, but no seats; round-46 is similarly complete for seats/path/rev. `axis_score_bad []`, two axes atoms; coverage fraction `[138,138]`, score `[9.72,10.0]`; depth `[24,24]`, score `[10.0,10.0]`. Battery skipped because structural clauses failed. Frozen paths derived exactly (`tools/round-48/`, claims file), `frozen_path_changed []`, touched 0.

### C1

Command:
```sh
python tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873
```
Exit: **1**. Exact captured output:
```json
{
 "battery": {"skipped": "artefact fails a structural clause first"},
 "block_present": 0,
 "counter": "round-48-c1",
 "failing": ["marker_occurrences 0 != 1", "marker_block_count 0 != 1"],
 "freeze": "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873",
 "frozen_derived": ["tools/round-48/", "plans/round-48-claims.md"],
 "frozen_path_changed": [],
 "marker_occurrences": 0,
 "met_target": false,
 "profile": "v3",
 "restored": [],
 "rev": "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873",
 "rule_blocks": 24,
 "touched": 0
}
```
Battery skipped; no claim about forged/genuine battery outcome. Output SHA/time metadata not successfully recorded for this command; do not treat it as a complete receipt.

## Exact L1 landing-revision commands

Run both with `<LANDING_REV>` replaced by the actual landing revision; freeze remains the claim freeze:
```sh
python tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev <LANDING_REV>
python tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev <LANDING_REV>
```

## Scope and blockers

This run measured the C2LandingGate preflight on the exact frozen revision. Neither counter passed at freeze; neither battery ran. No clause-vacuity or successful-forgery finding was established. Freeze derivation in both receipts reports the declared hash and no frozen-path changes. Report contains only this seat's findings; frozen files and all lane implementation files were not edited. Main/L1 must run the exact commands above at the integrated landing revision and capture full receipts; these freeze-time red results are preflight, not landing verification.
