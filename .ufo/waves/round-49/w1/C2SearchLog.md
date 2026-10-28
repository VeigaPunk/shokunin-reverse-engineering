# C2SearchLog — round 49 wave 1 (pre-freeze): A8 search-log review

Seat: C2SearchLog (leaf, read-only on the lane). Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Date 2026-10-28 UTC.

## Verdict

**A8 is arithmetically sound on its literal predicate but does not enforce the search-log contract, and the drafted entries are not contract-complete.** The counter derives the round-48 numbers correctly (rows 144 → 146, included 1, excluded 1) and the round-49 numbers correctly (rows 146 → 148, included 2, excluded 0), and it reproduces green on the dev-after fixture (exit 0). It is not a contract check: `identified` is unbounded, exclusions can be satisfied by a padded row, the battery exercises A8 by one marker mutation only, and the contract elements below are not in the counter at all. **Four decisions are needed before the freeze** (F3–F6, section 4). Nothing was edited in the lane.

## 1. Re-derived numbers (round 48, as asked)

| revision | `grep -cE` registry rows (exit 0) | notes |
|---|---|---|
| `61b87d74` (round-48 base) | 144 | S143, S144 last |
| `8847042a` (round-48 tip) | 146 | S145 `mined`, S146 `rejected` added |
| `e4f2cfa5` (round-49 base) | 146 | identical blob to 8847042a (sha256 68e6d028…) |
| dev-after `77580bf4` | 148 | S147 `mined`, S148 `mined` added |

Round 48: 144 → 146, new rows S145 (mined) + S146 (rejected) → included 1, excluded 1. The draft entry says `identified 2, screened 2, included 1, excluded 1; rows 144 → 146` — **matches**. Round 49: 146 → 148, new rows S147 + S148, both non-rejected → included 2, excluded 0 — the draft says `identified 2, screened 2, included 2, excluded 0; rows 146 → 148` — **matches**. Numbers are correct; the text around them is not (section 3).

## 2. Findings table

Receipts: `w1/C2SearchLog/receipts/RECEIPTS.md` (R1–R12, with sha256 and exit codes).

| ID | sev | finding | evidence (command → exit, sha256) |
|---|---|---|---|
| F1 | high | Draft entries omit four contract elements: **where searched**, **exclusion reasons** (round 48 has the reason only in row S146), **stop rationale**, and the round-49 **answer** to its question. | `c2-after.py` entries read via `git show 77580bf4:corpus/SOURCES.md \| awk` (exit 0); draft entries in `search-log-draft.md` |
| F2 | high | **"A count carries its command"** (CORPUS.md, rule under "Rules added from the round-1/2 corpus audits"): every number in a corpus entry is `<number> — <command> <date>`. Draft "rows 144 → 146" and "rows 146 → 148" carry no command. Counter does not check. | `grep -n 'A count carries its command' /home/vgpnk/Projects/shokunin/CORPUS.md` (exit 0) |
| F3 | high | **`identified` is unbounded above.** Only `identified ≥ screened` is checked; `identified 999, screened 2, included 2, excluded 0; rows 146 → 148` is green. | `a8_probe.py` case T1 → A8 `[]`; R6, `a8_probe.out` sha256 21dd8b08… (exit 0) |
| F4 | high (forgery) | **Padded exclusion passes.** Excluded = count of new *rejected registry rows*. Adding a rejected row S149 that was never screened and changing the entry to `identified 3, screened 3, included 2, excluded 1; rows 146 → 149` leaves A8 green, all atoms green. Counter never checks that an excluded item was a candidate of any search. | `a8_probe.py` case T4 → A8 `[]`, `other_red []` (R6); `dup_probe.py` confirms all atoms green on an overlay (R7) |
| F5 | medium | **Supersession convention is undecided.** The round-49 entry's "included 2" counts S147 (supersedes S145) and S148 (supersedes S146) as new included families. Precedent split: round-23 W2 correction — "the two added rows are corrections, not discovery" (identified5/included4 unchanged); round-25 residual — "included 6 families as rows S064–S071 (three of them supersessions)". Draft text states "identified 2, both already-known: 0 new families; included 2, both supersessions" — counter stays green either way. Choosing the other convention would change the counter, which is a pre-freeze change only. | `SOURCES.md` search log entries 2026-10-22 round 25 and 2026-10-21 round23 W2 (read-only, `git show e4f2cfa5`) |
| F6 | medium | **Battery covers A8 by one marker mutation only.** `m.mutations(...)` at the dev-after REV lists exactly one A8 entry, `A8 round-48 entry loses its late marker`. No mutation exercises the numeric clauses (rows, included/excluded). Numeric breakage is red in memory (T2 `included/excluded 1/1`, T3 `rows 144 -> 145`, T6 date, T7 `identified 1 < screened 2`, T8 semicolon form, T9 entry moved to Leads — all red, `other_red []`), but the plan's "eleven single-mutation overlays, one per defect class" evidence does not show A8's numeric branch can fail. | `a8_probe.py` `battery_mutation_labels` (R6); the `--battery` run exit 0 (R4) |
| F7 | low | **Duplicate row id passes A8.** `registry_rows` keys by id, so `rows` counts unique ids. Adding a duplicate S148 line leaves A8 green while `grep -cE` gives 149 and the lane census's `uniq -d` would print S148. | `dup_probe.py` → A8 `[]`, all atoms green, census lines 149 (R7, exit 0) |
| F8 | low | **Format brittleness is a hand-write constraint.** The counter needs the exact tokens `identified N, screened N, included N, excluded N` (commas), `rows N → M` or `->`, the header `- 2026-10-28 round 48` containing `late entry`, and `- 2026-10-28 round 49`. T8 (semicolons) → red. A header written `2026-10-28 UTC` → red. | `a8_probe.py` T8 (R6) |
| F9 | medium | **Round-49 lesson draft has no `## Gate`** (CORPUS.md: each `lessons/round-<N>.md` carries `## Gate`; SOURCES rule 1: per new row the URL, access date and ≤25-word quote with location). S147/S148 Gate content is absent from the draft. Routed defect 4 (round-48 closure) also asks for a census before→after line in the landed lesson; the draft has none, and A8 does not check it. | `c2-after.py` writes `corpus/lessons/round-49.md` with `## Corrections` only (`git show 77580bf4:corpus/lessons/round-49.md`) |
| F10 | low | **Negative claim has no sweep.** Round-48 entry answers "does sysexits ground exit 2?" with "no" and no sweep (CORPUS: "A negative claim carries its sweep"). The sweep is the two fetches in R11 (404 at `sysexits.h.3`; 200 with `EX_USAGE 64` at `sysexits.h.3head`). | RECEIPTS R11, R12 |
| F11 | info | **Date is consistent.** Round 48 ran 2026-10-28 (closure: watchdog `launch … round=48` 2026-10-28T15:25:47-03:00; S145/S146 accessed 2026-10-28). Header `2026-10-28` is correct for both entries. | round-48 closure `corpus/lessons/round-48-verifier-spotcheck.md` (read-only) |

## 3. Re-opened sources (2026-10-28 21:11Z, live)

- `plato.stanford.edu/entries/popper/`: HTTP 200, 118,135 B, sha256 `2c2d48c6…207` = S145/S147 pin = draft snapshot. The S147 quote (both the 21-word and the 22-word wording) is present in normalised text. The quote sits after the heading "Backdrop to Popper’s Thought" (offset 8875) and before the heading "The Problem of Demarcation" (offset 12989). **S147's locator is correct; S145's locator (§2 "The Problem of Demarcation") is wrong,** as the closure said. R11, R12.
- `man7.org/.../sysexits.h.3head.html`: HTTP 200, 12,725 B, sha256 `d9db4b96…340` = S148 pin = draft snapshot; contains `EX_USAGE 64` (raw markup `EX_USAGE        64   </b>`; normalised text matches) and the S148 quote. R11, R12.
- `man7.org/.../sysexits.h.3.html`: HTTP 404, 196 B, sha256 `80c3fe2a…880` = S146 pin. Still unreachable. R11.

## 4. Decisions for L1 before the freeze

1. **D1 — supersession convention (F5).** Either keep the counter and state in the text that the two round-49 included rows are supersessions with 0 new families (draft does this), or change the counter before freeze so supersession rows are not `included`. Do not do the second after freeze.
2. **D2 — `identified` (F3).** Disclose it as self-reported in the entry text, or add a bound the counter can check. No bound is derivable from the registry; disclosure is the honest option.
3. **D3 — battery (F6).** Either swap one of the eleven mutations to a numeric A8 mutation (rows 144 → 145, or included/excluded swap), or keep the marker mutation and state that the numeric clauses are not battery-exercised. The current battery says "one per defect class", which A8 does not meet.
4. **D4 — padded exclusion and duplicate ids (F4, F7).** Add to A8: each new row id must be named in its entry (closes the lazy padding case, not a determined forger), and row lines must equal unique ids (closes F7). Both are small; both alter the plan's A8 sentence, so decide before freeze.

## 5. Contract elements the counter does not check (L1 writes by hand)

Full table with draft text: `w1/C2SearchLog/search-log-draft.md`. In short: question answer; where searched (URLs, HTTP status, bytes, sha256, access date, "no query" if none); exclusion reasons per excluded item; stop rationale; command beside every count (CORPUS); negative-claim sweep for "sysexits does not ground exit 2"; `## Gate` in `corpus/lessons/round-49.md` with URL, access date and ≤25-word quote for S147 and S148; the census before→after line from routed defect 4; the supersession convention; and the lesson file must exist before any row with `used-by` naming it is landed (census rule).

## 6. Scope limits and not-run

- No new candidate search was run (not in A8's scope; the round-49 entry is a re-open). `identified` and `screened` therefore cannot be checked against any search log beyond the lesson's Gate for round 48.
- Round 48's Gate lists exactly two candidates; I could not verify that no other candidate was screened and dropped before the Gate (the lesson does not say). L1 confirms (bracketed in the draft).
- A6/A7 mechanics (snapshot pins, teaches cell) were checked only where they bear on the entries (R11, R12); the atom verdicts belong to the other C2 seat.
- Not run: `c1-run.sh` (forbidden), any data run, any lane write, any git mutation in the lane or fleet repo.
- Tools: none installed or upgraded. Used `git` (read), `python3` (stdlib), `curl`, `sha256sum`, `awk`/`grep` in scratch.
- Scratch `/fast/scratch/hyaku/kaidoku-r49/C2SearchLog` removed after receipts were copied to `w1/C2SearchLog/receipts/`.

## 7. Artifacts

- `w1/C2SearchLog/search-log-draft.md` — draft landing entries for round 48 (late) and round 49, with commands beside counts, and the contract checklist.
- `w1/C2SearchLog/receipts/RECEIPTS.md` — command, exit code, sha256 index (R1–R12).
- `w1/C2SearchLog/receipts/` — counter JSON (`af.json`, `afb.json`, `fz.json`), stdout copies, `a8_probe.py`/`a8_probe.out`, `dup_probe.py`/`dup_probe.out`, dev-fixture outputs (`mk.out`, `after.out`), three live fetches.

Key sha256s: `c2-mismatch.py` 90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f (draft = clone copy); dev freeze `541044b6…d3d3`; dev after `77580bf4…4fb`; `--rev` after stdout 64805124…fc8 (exit 0); `--rev` freeze stdout 8b469c5b…17d6 (exit 1); battery stdout 33d895c2…b915 (exit 0).
