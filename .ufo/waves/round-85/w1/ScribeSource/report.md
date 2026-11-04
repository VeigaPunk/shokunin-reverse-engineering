# ScribeSource — round 85 frontier: source row S304 + mutant-kill-binding knowledge entry

Lane `kaidoku-shokunin`, round 85. Draft only — no commits, no lane-tree writes outside this wave dir.

## Source facts

| fact | value |
|---|---|
| work | Papadakis, Kintis, Zhang, Jia, Le Traon, Harman, "Mutation Testing Advances: An Analysis and Survey" |
| venue | Advances in Computers vol. 112 (2019), pp. 275–378 (Elsevier), book chapter |
| DOI | 10.1016/bs.adcom.2018.03.015 |
| canonical URL | `https://doi.org/10.1016/bs.adcom.2018.03.015` → HTTP 200, resolves to `https://linkinghub.elsevier.com/retrieve/pii/S0065245818300305`; CrossRef confirms title/journal/publisher/year/DOI, **"No abstract available."** |
| publisher page | `https://www.sciencedirect.com/science/chapter/bookseries/pii/S0065245818300305` → **HTTP 403** (fetch failed) |
| ORBilu record | `https://orbilu.uni.lu/handle/10993/31612` → **TLS verify failed** ("unable to get local issuer certificate"), no content reached directly |
| full text read | `https://web.archive.org/web/20190429011957/http://orbilu.uni.lu/bitstream/10993/31612/1/survey.pdf` → **HTTP 200** (ORBilu author postprint, archived 2019-04-29) |
| access date | 2026-11-04 |
| PDF bytes / pages / sha256 | 1 129 278 B / 153 pages / `63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023` |
| snapshot | `source-snapshot.txt` (provenance header + verbatim `pdftotext -layout` text), sha256 `3452916192a447db89545cf9cdb4c0c7bfbd7f162b67482fb7582691e6bd7bee`, also in `source-snapshot.sha256` |

Full text **was** available (postprint), so the row was written; the abstract-only fallback was not used.

## Located quote

> "When a test distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant is 'killed' or 'detected'"

- Word count **24** (≤ 25 required).
- Location: Section 2 "Background", author postprint PDF **p. 6** (published as Advances in Computers 112 (2019), pp. 275–378); snapshot line 259.
- Same section, postprint PDF p. 7: "A mutant is strongly killed if the original program and the mutant exhibit some observable difference in their outputs." (19 words) — the observable-difference form of the same definition.
- **Gap stated**: the source defines the kill as an observed behavioural difference between the mutant's and the original's run, and says nothing about a test's *name*; the lane's declared-case-name binding is the lane's own tightening, not the source's wording. The row's `teaches` cell says exactly this.

## Registry row (candidate)

`candidate/corpus/SOURCES.md` = the lane file at `91eeb72f` + one row (diff is a single added line at line 220):

```
| S304 | Papadakis, Kintis, Zhang, Jia, Le Traon & Harman, "Mutation Testing Advances: An Analysis and Survey", Advances in Computers vol. 112 (2019), pp. 275-378 - https://doi.org/10.1016/bs.adcom.2018.03.015 (full text read from the ORBilu author postprint, archived 2019-04-29 at https://web.archive.org/web/20190429011957/http://orbilu.uni.lu/bitstream/10993/31612/1/survey.pdf) | docs | B | mutation-testing survey | Section 2 "Background", author postprint PDF p. 6: "When a test distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant is 'killed' or 'detected'" (24 words); publisher postprint fetched 2026-11-04 HTTP 200, PDF sha256 `63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023`, 153 pages, snapshot `.ufo/waves/round-85/w1/ScribeSource/source-snapshot.txt` | The survey defines a killed mutant by an observed difference in the test run: when a test distinguishes the mutant's behaviour from the original program's, the mutant is "killed" or "detected". It is silent on name-matching, so the lane's declared-case binding is the lane's own tightening of this definition, not the source's wording. | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md |
```

Schema: 11 cells, no `|` inside any cell, `kind=docs`, `tier=B`, `scope=mutation-testing survey`, `status=mined`, `opened=2026-11-04`, `recheck=180d`, `used-by=corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md`. `S304` did not exist before (`grep -c 'S304'` on the lane file = 0); the highest id was `S303`.

## Census before → after (frozen commands)

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `kaidoku ok …/corpus/SOURCES.md`, **27 W04** (baseline).
- Same script on the candidate in a scratch clone (candidate `corpus/SOURCES.md` + candidate knowledge entry copied in, so `used-by` resolves) → exit 0, `file ok …`, **27 W04** — no new warning.
- Frozen manual census (CORPUS.md §Census) on the candidate: rows **208 → 209**; tier `A=190 B=10 C=8` → `A=190 B=11 C=8`; status `mined=186 rejected=22` → `mined=187 rejected=22`; malformed **0**; duplicate ids **0**; enum/tier-inflation violations **none**; missing `used-by` paths **none**.
- Fleet `shared` mode: the DOI appears in no other lane's registry (sibling `tameshi-shokunin` cites the DOI inside an anchor cell without a URL token, so no URL-keyed collision).

## Knowledge entry

`candidate/corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md` — provenance trio first (`source: S304 — …`, `verified-at: 2026-11-04 (round 85, lane commit to be filled at landing)`, `recheck: 180d`); body 35 lines (≤ 60). Sections: Claim · What the frozen counter measures (path `tools/round-84/mutation-closure.py`, declared case in the failing list + pristine green, counting command verbatim) · Limit (a kill binds a case *name*; semantic certification of each case's assertion is not claimed) · Falsification (one named refuting observation) · Receipts. Every number carries its command or receipt; no credential material.

## Measurements re-run here (frozen counters, as given) — BASE, not the round-85 result

At revision `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`, via `python3 -I -B tools/round-84/mutation-closure.py --root . --rev <rev> --mutants .ufo/waves/round-85/mutants.json --work <scratch> --json-out <receipt>` → 21 rows, **killed 3** (`sb-window-13th`, `sb-two-fields-first`, `cg-floor-le`), survivors 18, inconclusive 0, pristine_failed [], exit 1. Receipt `receipts/base-mutation-closure-at-declaration.json`; counts equal the committed BASE receipt `.ufo/waves/round-85/pre/c2/base-mutation-closure.json`. Same counter on the frozen r84 table `.ufo/waves/round-84/mutants.json` → 13 rows, **killed 13**, survivors 0, `ok true`, exit 0 (receipt `receipts/base-frozen13-regression-at-declaration.json`). Pristine green at that revision for all three targets: `conjunction-gate.py` 21 cases exit 0, `printed-command.py` 22 cases exit 0, `source-bind.py` exit 0.

## Gate block (hand to ScribeLesson)

```
URL         https://doi.org/10.1016/bs.adcom.2018.03.015 (HTTP 200; resolves to
            https://linkinghub.elsevier.com/retrieve/pii/S0065245818300305)
full text   https://web.archive.org/web/20190429011957/http://orbilu.uni.lu/bitstream/10993/31612/1/survey.pdf (HTTP 200)
access      2026-11-04
status      200 (DOI target) / 200 (archived postprint) / 403 (ScienceDirect chapter page) / TLS-verify failure (ORBilu handle)
quote       "When a test distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant is 'killed' or 'detected'"
location    Section 2 "Background", author postprint PDF p. 6 (Advances in Computers 112 (2019), pp. 275-378)
words       24
decision    ADMIT as tier B, scope `mutation-testing survey`, id S304, kind docs, status mined
            (cited by corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md)
gap         the source defines the kill behaviourally and is silent on name-matching; the declared-case
            binding is the lane's own tightening and must not be attributed to the source
```

## Installations

None — `pdftotext` (poppler) and `curl` were already present. No pacman transaction (pacman is PAUSED host-wide).

## Out of scope / note for the L1

No predicate, kill rule, target, `tools/round-84/` file, mutant table, or `.ufo/waves/round-85/pre/` fixture was changed; no lane-tree production bytes were written (both candidates live under `…/w1/ScribeSource/candidate/`); git writes happened only in a scratch clone. The S304 row's `used-by` points at `corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md` — row and entry must land together or the registry's `used-by` existence check flags E11.
