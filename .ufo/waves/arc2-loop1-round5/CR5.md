# CR5 — census completeness: R1–R4 claim-universe gaps

**Verdict: REFUTE treating census-v10 PASS as proof that the broader R1–R4 claim audit is complete.** This does not refute v10 on its narrower stale-statement purpose, nor prove the parent’s separate inventory is incomplete.

## Evidence and method

Archived the round-4 record tree at `0e8c96b48a8823e8c6964081cfc04e21f6adcf56` and compared v10’s literal `SCOPE` with the round headings there. Exact commands and observed output:

```sh
set -euo pipefail
scratch=/var/tmp/arc2-l5r5-CR5-audit
tree="$scratch/0e8c96b"
mkdir -p "$tree"
git archive 0e8c96b | tar -x -C "$tree"
printf 'archived %s into %s\n' "$(git rev-parse 0e8c96b)" "$tree"
```

```text
archived 0e8c96b48a8823e8c6964081cfc04e21f6adcf56 into /var/tmp/arc2-l5r5-CR5-audit/0e8c96b
```

```sh
python3 - <<'PY'
import ast, re
from pathlib import Path
root = Path('/var/tmp/arc2-l5r5-CR5-audit/0e8c96b')
probe = root / '.ufo/gates/c1-census-v10.py'
card = root / 'SCORECARD.md'
module = ast.parse(probe.read_text())
scope_node = next(n.value for n in module.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SCOPE' for t in n.targets))
scope = ast.literal_eval(scope_node)
ranges = [(a, b) for name, a, b, *_ in scope if name == 'SCORECARD.md']
lines = card.read_text().splitlines()
heads = [(i, line) for i, line in enumerate(lines, 1) if re.match(r'^## arc2-loop1-round[1-4] ', line)]
print('declared SCORECARD ranges=' + ','.join(f'{a}-{b}' for a,b in ranges))
for ix, (start, title) in enumerate(heads):
    limit = heads[ix+1][0]-1 if ix+1 < len(heads) else len(lines)
    while limit >= start and not lines[limit-1].strip():
        limit -= 1
    body = [n for n in range(start, limit+1) if lines[n-1].strip()]
    covered = sum(any(a <= n <= b for a,b in ranges) for n in body)
    print(f'{title.split("—")[0].strip()}: body={start}-{limit}; nonblank_declared={covered}/{len(body)}')
PY
```

```text
declared SCORECARD ranges=56-60,273-326,417-466,467-502,503-533,534-560,619-619,620-620,635-701,702-767,768-854
## arc2-loop1-round1: body=635-701; nonblank_declared=63/63
## arc2-loop1-round2: body=703-766; nonblank_declared=60/60
## arc2-loop1-round3: body=768-854; nonblank_declared=83/83
## arc2-loop1-round4: body=856-933; nonblank_declared=0/74
```

The v10 source describes its test as current-surface pin/version claims, declares its input ranges at `.ufo/gates/c1-census-v10.py:5-9,85-108`, and narrows matches to REA-related pin/version/cache/pointer assertions at `:110-121,270-287`. Its main file list is built only from those declared ranges (`:376-384`): it does not enumerate round reports, lessons, receipts, README claims, or probe artifacts. R4’s section begins at `SCORECARD.md:856` and runs to `:933`, beyond the last declared range (`:108`).

Receipt handling is also narrower than receipt verification: v10’s `RECEIPT` regex checks for receipt-like words in statement text (`.ufo/gates/c1-census-v10.py:116,358-366`); it does not open a receipt, compare its manifest/hash, or validate the claimed event. I did not rerun v10’s full live-anchor/cache check: the script reads client config paths and the user npx cache (`:74-83,124-134,218-234`). The scope comparison above is an archived-tree re-derivation, not a fresh v10 PASS/FAIL. SCORECARD’s recorded v10 result at `:880-883` remains a historical report claim here.

## Candidate omissions to test in the parent ledger

These are candidate claim classes outside v10’s detector, not proof that the parent’s separate claim ledger omitted them:

- **R1 — prose, adjudication, and receipts:** the safety-label and stale-pointer dispositions and rule #10 are stated as outcomes/prose changes (`SCORECARD.md:665-682`; `.ufo/reports/arc2-loop1-round1/kaidoku.md:19-45,113-128`). The three-config custody pair and live battery outcomes depend on receipts and command results (`SCORECARD.md:662-671`; report `:56-69,123-128`).
- **R2 — README, wire-log, custody/battery:** label and pointer repairs (`SCORECARD.md:742`), the 0/2195 Kimi tool-log finding (`:751-755`), and five-path custody plus 6.7.0 battery outcomes (`:721-737`; report `.ufo/reports/arc2-loop1-round2/kaidoku.md:32-50,65-92`) are not general REA-pin/version census rows. The report explicitly distinguishes configured from held and routes that finding as follow-up (`:47-50`).
- **R3 — exploratory and negative outcomes:** the outer-cap PE run is inconclusive and the citation-gate form is refuted, not verified (`SCORECARD.md:797-819`; report `.ufo/reports/arc2-loop1-round3/kaidoku.md:24-45,75-80`). The witnessed config mutate-and-revert and its voided bare zero-drift claim are receipt-backed outcomes (`SCORECARD.md:820-827`; report `:61-63,81-82`).
- **R4 — wholly outside v10’s SCORECARD scope:** rule #11, citation-drift probe, v10/lesson claims (`SCORECARD.md:867-885`); receipt-backed in-window custody drift (`:888-893`); and the contained PE OOM outcome (`:894-901`). The report distinguishes the probe from a gate and records OOM containment as exploratory evidence (`.ufo/reports/arc2-loop1-round4/kaidoku.md:16-44,58-65,79-81`).

## Conclusions

- **Observation:** In the archived round-4 tree, v10’s fixed SCORECARD ranges declare every nonblank R1–R3 section line and none of the 74 nonblank R4 lines. The detector is limited to selected files and assertion forms; receipt presence is textual, not content-verified.
- **Inference:** A v10 PASS cannot establish that every falsifiable before/after, exploratory outcome, prose change, or receipt-backed result in R1–R4 has a ledger row. If the parent’s candidate universe is generated from v10 alone, it can miss the classes above.
- **Unknown:** Whether the parent’s independent C1 inventory already includes these candidates; whether each receipt still validates at its cited historical revision; and whether each underlying domain claim is substantively correct. None is adjudicated by this scope audit.

## Suggested completeness rule (verbatim)

```text
For R1–R4, inventory each declared round claim and each falsifiable outcome or disposition in its round section and report, including exploratory runs, refutations, honest stops, no-change adjudications, prose/lesson edits, receipt-backed custody or battery events, and stated negative results. For every row, record the cited commit, source pointer, before→after or outcome class, exact command/output or verified receipt hash, and disposition (verified, refuted, inconclusive, not verified, adjudicated, or operator-owned). Receipt language alone is not verification: check the referenced manifest and bytes at the cited tree. Keep excluded candidates in a visible residual list with a reason; deduplicate without dropping original source pointers.
```
