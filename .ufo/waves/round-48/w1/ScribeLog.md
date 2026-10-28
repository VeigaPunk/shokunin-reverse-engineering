# ScribeLog — round 48, w1: the LOG.md entry draft, plus one measured C2 kill-rule finding

## Behavior

Drafted the round-48 `LOG.md` entry in the rounds-46/47 house format (`### Round 48 — …`,
bold-labelled bullets, `### Round 48 claim ledger` 7-column table) at
`.ufo/waves/round-48/w1/ScribeLog/log-entry.md`. Everything receipt-backed is filled;
only post-landing numbers remain `[fill: …]`. One falsification pass was executed in
process against the frozen `record2.py` (my own measurement, receipt below).

## Gates run (this seat)

| check | exact command | exit | evidence |
|---|---|---:|---|
| C2 clause-5 blind spot | `python3 -I -B -` importing `record2`+`gate`; `files=gate.show(root,0f06251b)`; `mut=_m_axes_cell_off(card)`; `score(mut,files,root,rev,'v3')` vs `score(card,…)` | 0 | `.ufo/waves/round-48/w1/ScribeLog/c2-axes-blindspot.json`, wrapper `c2-axes-blindspot.receipt.json` (UTC 2026-10-28T18:55:16Z, stdout sha256 `451e9731…d8`) |
| Counter bytes pinned | `sha256sum tools/round-48/record2.py` vs `git show 0f06251b:tools/round-48/record2.py \| sha256sum` — identical `eb7dc887…8581` | 0 | above |
| Freeze re-derivation | `git log --format='%H %ci %s' -- plans/round-48-claims.md` → `663f30ee`-era tip list; `--diff-filter=A -- tools/round-48/`; `merge-base --is-ancestor dc73587a HEAD` | 0 | transcript; freeze series `7fe11332 → dc73587a(A1) → ac02a79f(A2) → f3a7afc4(A3) → 0f06251b(A4)`; declared freeze = A4, the commit carrying the A4 paragraph |
| Landing state | `git grep verdict-meaning-table HEAD -- SKILL.md` (empty); `git grep '## Round 48\|Record corrections — round 48' HEAD -- SCORECARD.md` (empty) | 1 (no match) | landing not yet present at HEAD `663f30ee` |
| Frozen worktree check | `git status --porcelain tools/round-48/ plans/round-48-claims.md`; `git diff tools/round-48/` | clean | the `M` flag seen earlier was racy-stat; `git diff` empty — no content change |

## Findings (scoped, ranked)

1. **[HIGH, measured] C2 `axes-score-cell-off` is invisible to clause 5.** `score()` parses
   the mutated `card` for sections/oracle/corrections/quotes, but `axis_scores(files)`
   re-fetches `files("SCORECARD.md")` — committed bytes — so the forgery's decremented score
   cell never enters `axis_score_cells`: receipt shows forged row `9.72 → 9.0` vs `138/138`
   (wants `10.0`), `axis_score_bad []`, failing list identical to the genuine card. On a
   green landing card this forgery scores `v3_green 1`, tripping the kill rule and blocking
   any green claim until a further amendment (one-line: `axis_scores` on the artifact text).
   Same defect class as A3 — a clause that cannot be measured correctly.
2. **[HIGH, verified in git] Declared-freeze staleness.** The wave tasking pins
   `dc73587a` (A1); the claims file's own rule (`git log -1`) yields `0f06251b` (A4).
   ExecMeasure receipts: stale `--freeze dc73587a --rev <tip>` exits 2
   `frozen_path_changed`. All wave receipts used `freeze=rev=<stale A1>` — consistent but
   pre-amendment; the counted command must carry the A4 hash.
3. **[MED] Meaning classifier residual.** Post-A4 the classes are still closed-token
   regexes: `MutC1Rows`' `0=met; actual exit 0 means the command failed` survives (probe
   exit 0); `LabC1Meaning` measured 16/40 registry rows failing on honest vocabulary and
   four tools whose real exits overload a digit or leave the 0/1/2 map entirely
   (`unblob-logtee` exit 7). The grammar cannot be satisfied honestly on those rows —
   needs an L1 policy call (mixed-class cell or dominant class + disclosure).
4. **[MED] C2 laxities** (`RevC1`, `MutC2Corr`): malformed lines under the corrections
   heading are silently ignored; one quote correction excuses all same-key wrong quotes in
   its round; `section_bodies` takes the last two `## Round N` headings without
   distinctness checks; claim-id regex `R\d\d-C\d` unbound to the round's own claims; a
   no-op mutation counts as `v2_green` while never scoring v3; `gate` imports from the
   worktree (`C2OracleLimit`, R47-CL1 class).
5. **[LOW] Racy `frozen_worktree_dirty`.** `gate.dirty()` (porcelain status) fired exit 2
   on `tools/round-48/meanings.py` twice (`w1/C1Meaning/receipt.json`) while bytes were
   identical — a stat race, not a tamper; recheck on next counter run.
6. **[LOW] Census name-map drift** (`ExecCensus`): committed `census2.json` equals its own
   rule at A2, but worktree derivation names 5 paths from the round-48 claims file vs 4 —
   path set unchanged; informational only (the clause binds `paths`).

## What the log draft asserts (per claims file + receipts)

- Before-state: C1 exit 1 (`marker_occurrences 0`, `rule_blocks 24`); C2 exit 1 (oracle
  green 44 atoms, floor red on round-47 seats, `corrections 0`, `exempted 2` unbacked);
  C2 `--profile v2` exit 0 — the hole. Both batteries legitimately unexercised pre-landing.
- Landing requirements on record: block 25 (draft `l1/block25.md`, sim green at A3),
  registry rows for `meanings.py`/`record2.py` + meaning repairs (~16 rows, 4 needing a
  policy call), `## Round 48`, `## Record corrections — round 48` with a re-derived
  `seats` correction (`1 wave, 75 seats total` — w1-dispatch `counts.spawn 75`, no w2 file)
  and a `quote` correction (`exempted 1` per `c2-at-A7.json` vs quoted `2`), Owned-axes head.
- Wave: 75 registered seats (manifest), role mix in the draft; no tools installed.

## Touched surfaces

Written only: `.ufo/waves/round-48/w1/ScribeLog.md`,
`.ufo/waves/round-48/w1/ScribeLog/log-entry.md`,
`.ufo/waves/round-48/w1/ScribeLog/c2-axes-blindspot.json`,
`.ufo/waves/round-48/w1/ScribeLog/c2-axes-blindspot.receipt.json`.
Scratch `/fast/scratch/hyaku/kaidoku-r48/ScribeLog` removed after receipts copied. No lane,
frozen, fleet, or sibling files modified; no git mutation; no installs.

## Out of scope / not run

Both counters' live `--rev` runs at A4 (ExecMeasure already covers `ac02a79f`; the
post-landing measurement is the L1's). No fixture repo needed: `record2.score` accepts text
in memory, so the blind spot needed no fabricated card. Wave-2 verification, ledger
verdicts and routed-CL numbering are the L1's.
