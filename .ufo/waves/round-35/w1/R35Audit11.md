# R35Audit11 — C1 used-by mutation evidence (wave 1)

Seat: R35Audit11 (executor; item: "Mutate C1 used-by in /tmp"). Lane root:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. All mutation work ran in private
`/tmp/r35-audit11/`; no lane writes except this report, no VCS mutation, no
subagent/background work.

## Method

- Built a synthetic green repo in `/tmp/r35-audit11/green` mirroring the frozen counter's
  own selftest fixture (same SOURCES.md S125/S129 rows, same entries, PROVINCE.md,
  corpus/README.md, `.ufo/waves/round-35/claims-canonical.json` carrying the frozen
  predicate P35-c1). `git init` + one green commit.
- Freeze rev = green HEAD `8fd94993e69bfef183b44b1559bb9987138844f3`.
- For each mutant: copied green repo, edited **only** the used-by cell (cell 10) of
  SOURCES.md rows S125/S129 (verified: every mutant commit touches only
  `corpus/SOURCES.md`), committed, ran the frozen counter
  `tools/round-35/c1-coverage-counter.py --root <mutant> --rev HEAD --freeze 8fd9499… --json-out <receipt>`.
- Controls: green reproduction (expect 0); read-only re-run at lane base
  `aa04633a…` with freeze `2323d197…` (expect 1, matching committed c1-do-nothing.json);
  instrument selftest.

## Evidence

| Mutant | head (abbrev) | exit | counter outcome (failing check) |
|---|---|---|---|
| green control | 8fd94993 | 0 | `C1_CLEAN` |
| M1 S125 used-by empty | 07846e30 | 1 | `registry_usedby_missing:S125:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md` |
| M2 S129 used-by wrong entry | 152605a4 | 1 | `registry_usedby_missing:S129:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md` |
| M3 S125 used-by partial (no prefix/.md) | 0c04daf7 | 1 | `registry_usedby_missing:S125:…mapper-contract.md` |
| M4 both used-by cross-swapped | 63748065 | 1 | `registry_usedby_missing:S125:…` and `registry_usedby_missing:S129:…` |
| M5 S125 used-by typo (trailing `x`) | bd2a478c | 1 | `registry_usedby_missing:S125:…mapper-contract.md` |
| M6 S125 used-by + noise suffix (` (see notes)`) | c55c7b6d | 0 | `C1_CLEAN` (survives) |

Receipts (JSON) for every run: `/tmp/r35-audit11/receipt-*.json`; run logs
`/tmp/r35-audit11/run-*.txt`.

## Findings

1. The frozen used-by check is alive and kills 5/6 mutations: deleting the used-by value
   (M1), pointing at the wrong entry (M2), partial filename (M3), cross-swapping both rows
   (M4), and a single-char typo (M5) all flip the counter to exit 1 with a named
   `registry_usedby_missing:<row>:<entry>` failure. Nothing else in the synthetic tree was
   touched, so the failure is attributable to the used-by mutation alone.
2. Check granularity is **substring containment**: the counter tests
   `entry not in cells[9]` (source line 130). M6 appends text after the exact entry name
   and still passes (exit 0). A writer who names the entry somewhere in the used-by cell —
   e.g. with trailing annotations — satisfies C1. This is a survivable-mutation limit to
   note for scoring; it does not weaken the kill rule (empty/wrong/partial names still fail).
3. Controls re-verified: green reproduction exit 0; lane-base do-nothing re-run exits 1
   with the identical 8 failing names as the committed `.ufo/waves/round-35/controls/c1-do-nothing.json`
   (entry_missing ×2, registry_row_missing ×2, province_missing ×2, readme_missing ×2);
   `--selftest` reports `ok (green=0 red=1)`.

## Commands

```
python3 -I -B tools/round-35/c1-coverage-counter.py --root /tmp/r35-audit11/green --rev 8fd94993e69bfef183b44b1559bb9987138844f3 --freeze 8fd94993e69bfef183b44b1559bb9987138844f3 --json-out /tmp/r35-audit11/receipt-green.json
python3 -I -B tools/round-35/c1-coverage-counter.py --root <mutant repo> --rev <head> --freeze 8fd94993e69bfef183b44b1559bb9987138844f3 --json-out /tmp/r35-audit11/receipt-<mutant>.json
python3 -I -B tools/round-35/c1-coverage-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev aa04633a686d49756763b1feed4be6830d5bb479 --freeze 2323d197456f1328459d9420aff025cffbcb3e27 --json-out /tmp/r35-audit11/receipt-lane-base-c1.json
python3 -I -B tools/round-35/c1-coverage-counter.py --selftest --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
```

## Limits

- Tree shape: synthetic green fixture mirrors the counter's selftest (round-shaped, minimal)
  rather than a copy of the lane corpus; conclusion is about counter sensitivity, not about
  any future data commit (none exists for this round yet).
- Lane accessed read-only via `git show`,ls-tree,rev-parse` only; no source-tree writes.
- Mutations scoped to the used-by cell per the item; other C1 invariants (trio, citation,
  province, readme) deliberately untouched.
