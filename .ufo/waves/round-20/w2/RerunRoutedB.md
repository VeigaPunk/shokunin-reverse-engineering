HOLDS — attack: the C1 baseline claim that B has 11 open routed items (`.ufo/waves/round-20/claims.json:15-18`).

**Observation.** Ran:
```text
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/routed-r19.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 14f0260ad319ecc26994381b2415d5a999003375 --strict
```
Exit: **1**. The strict-mode exit matches the contract for open findings (`.ufo/waves/round-20/contract.md:28-32`). The invoked script's working-file blob and its Git object at measured source S are identical: `30a2b30c2ccee470756566d93ff19647052e11bb`; the S object was read with `git show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/tools/routed-r19.py`.

JSON summary from the run:
```json
{
  "items": [
    {
      "id": "D1",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; custody-pair selftest lacks the worktree-refusal or cleanup fixture; routed-r19.py absent at REV; routed-r19.py absent at REV"
    },
    {
      "id": "D2",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"
    },
    {
      "id": "D3",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"
    },
    {
      "id": "D4",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"
    },
    {
      "id": "D5",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; final-census.json absent or invalid at REV"
    },
    {
      "id": "D6a",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"
    },
    {
      "id": "D6b",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV for AST self-check"
    },
    {
      "id": "D6c",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"
    },
    {
      "id": "D6d",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; routed-r19.py absent at REV"
    },
    {
      "id": "D6e",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; wave-outcomes selftest lacks the seat_named_causes fixture"
    },
    {
      "id": "D6f",
      "named": false,
      "substance": false,
      "why": "SCORECARD.md name missing; round-20 lesson name missing; jj_ source case ids at REV=0 baseline=0; need at least two more"
    }
  ],
  "named_open": 11,
  "open_count": 11,
  "rev": "14f0260ad319ecc26994381b2415d5a999003375",
  "substance_open": 11
}
```

**Inference.** The B run confirms the stated 11-open baseline: all 11 items fail both named and substance checks. This is baseline-only evidence; it does not establish that the closures pass at S.