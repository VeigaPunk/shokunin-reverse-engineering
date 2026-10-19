# SEAT PL-3 — chain c3, role planner — arc3-loop1-round3

Seat line: plan C3 (probe-table arc3 coverage extension): enumerate every in-repo
citation introduced by arc3 rounds 1-2; classify pinnable-under-rule-11 vs
adjudicated NO-ENTRY with cause; design conforming entries in the existing schema.
Artifact: `claims/c3/PL-3/plan.md`.

Repo HEAD throughout `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (read-only `git rev-parse`;
no git mutation by this seat). Scratch `/var/tmp/pl3` (`/tmp` never used). Real target
(`.ufo/gates/citation-drift/pointer-table.json` + `expected.json`) NOT written by this seat —
C3's implementer EX-41 owns it; this seat's output is a tested **delta fragment** for it (or the
parent) to splice.

## 1. Work performed (evidence pointers)

- Read: freeze (`claims-frozen.md:64-81`), the pointer table + expected (r2 landing), the probe
  script (499 lines), the r1 EVM entry, SCORECARD's arc3 sections (`:1338-1496`), SKILL.md rule #14
  (`:240-255`) + registry rows (`:379-390`), custody README, QUALITY.md, the r1/r2 non-wave diffs,
  the r10 13→31 extension precedent (`dbae324`), and the landed round-3 peers (EX-44 baseline, EX-46
  `pin-check.py`, CN-2 `pin-free-check.py`, VZ-4 c3 harness, CU-1, records drafts).
- **Census (mechanical, this seat's instrument):** `claims/c3/PL-3/census-v2.json` +
  `census-table.out` — 356 backticked tokens from 11 sources (the four declared families + the two
  census-instrument surfaces), resolution ladder exact→relative→suffix→`../`→absent; **128 path-ish
  tokens, every in-repo target present at HEAD, 0 absent path tokens**.
- **Delta fragment (tested):** `claims/c3/PL-3/entries-arc3.json` — 51 entries + 11 exempt rows
  re-based on EX-41's landed cut; builder `build_entries.py` (re-runnable against any later base);
  `validation.out`.
- **Falsification suite:** `bite.py` + `bite-suite.out` — per-entry mutation testing through the
  probe's own `check_entry` with an in-memory tree (no writes, no real-file mutation).
- **Patch text:** `proposed-readme-path-forms.patch.md` (README path-form defects, measured).

Artifacts (identities re-derived after the last edit, 2026-10-19T13:2xZ):

| artifact | bytes | sha256 |
|---|---|---|
| `claims/c3/PL-3/plan.md` (213 lines) | 17,371 | `6d49ebb3f7937d59afeb8a8f8c88240f9157f39d9a8bf5c90e08de92a15e8d31` |
| `claims/c3/PL-3/entries-arc3.json` | 19,601 | `3c38ad182e4b9bd805b68034d1618cd7976b9f4c450aaab37f57065fe0a566e5` |
| `claims/c3/PL-3/build_entries.py` | 24,019 | `4103656e38980c2e76c05a07b0d4de2d390c9a8bb6dddb9ea3e4cc69660a20ab` |
| `claims/c3/PL-3/bite.py` | 4,931 | `00933dd5774748483722ac7ce53ff433ebd936d8bdd7fac8f199ea750fb8f609` |
| `claims/c3/PL-3/validation.out` | 1,279 | `2348414676f8732e023030d042566fdba398d358f286b420bf4ee00bb031806f` |
| `claims/c3/PL-3/bite-suite.out` | 4,197 | `93069f4b023c27f5d2c9e8b0234405c9dc39f28013f2ef8134b29e4275364db9` |
| `claims/c3/PL-3/census-v2.json` | 65,874 | `9d291125684c5f913eb3f0d5f1bb8bea5a3cf35d94d962f700689d90a2b88154` |
| `claims/c3/PL-3/census-table.out` | 18,430 | `f276265e26ce0aab977c9f117b5248358305019000d368533d154f4b17b2d756` |
| `claims/c3/PL-3/proposed-readme-path-forms.patch.md` | 2,381 | `5b00c8b95c7b3fb4d156e02689ec18bd922d574721b5fd2fe581870dbfd8b659` |

Mid-seat event: EX-41 landed its first-cut extension (table 31→57 entries, exempt 3→8, sha
`bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7`, expected pin `d97dd60a…`).
This seat validated that cut read-only (probe findings=0 both modes at HEAD; EX-46 pin-check MATCH)
and **re-based its fragment as a delta over it**; 17 of the originally designed 68 entries were
dropped as functional duplicates of EX-41's (mapping in plan §4).

## 2. Proposed changes

- `claims/c3/PL-3/entries-arc3.json` — splice into `.ufo/gates/citation-drift/pointer-table.json`
  (51 entries, 11 exempt rows, `_doc` addendum; N 57 → 108) + re-pin the digest in
  `expected.json` **in the same commit** (procedure: plan §6; byte-format facts from EX-41's
  round-trip builder and the no-trailing-newline expected.json).
- `claims/c3/PL-3/proposed-readme-path-forms.patch.md` — custody README `:129` (`../waves/` →
  `../../waves/`) and `:103-105` (receipt examples need the `.ufo/waves/` base). C2's file: patch
  text only; both defects measured, not inferred.
- Two optional table-internal note edits (plan §6.4): refresh `shonen-skill-range`'s stale 13/13
  note; widen EX-41's operator-paths exempt row to name the `a3r2-cp-path-*` proxy anchors.
- No other repo file is proposed for change; no LOG/SCORECARD/SHONEN/corpus/SKILL/README edit lands
  from this seat.

## 3. Before → after measurement (chain claim: entries 31 → N; findings 0; selftest 13/13)

```
$ python3 /var/tmp/pl3/build_entries.py         # fragment spliced on the live worktree base
BASE table sha256=bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7
BASE entries=57 quoted=4 exempt=8
NEW entries=51 new_exempt=11 new_table_sha256=c895a671827f5712e7a1559169aae5b5a46b796ea7472530976d8a3ebc0e9ad3 N=108
probe default : CITATION_DRIFT_VERDICT: reported findings=0 exit=0
probe --strict: CITATION_DRIFT_VERDICT: clean findings=0 exit=0
stale-pin demo (scratch table + base expected): could-not-evaluate findings=1 exit=2 (pointer_table_tampered)
selftest (scratch expected): CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
real artifacts unchanged: table bfc42f1b == bfc42f1b; expected d97dd60a == d97dd60a
$ python3 /var/tmp/pl3/bite.py
BITE_SUITE: entries=51 control_silent=51 both_mutations_bite=51 failed=0
```

Landed-cut control at this seat's close: probe at HEAD findings=0 both modes; 57-entry cut stable
(`bfc42f1b` re-hashed). Counted mechanically: **entries 57 → 108**; claim-relevant before→after for
the chain is the census (every pinnable arc3 citation covered or adjudicated), not the count.

## 4. Attacks / refutations attempted, with verdicts

1. **Vacuous needles.** Mutation suite: wrong-stated-number on every extracted entry, all-occurrence
   needle removal elsewhere, isolation (only the mutated entry may report). First run caught **13
   non-biting entries** (12 multi-site needles; 1 too-mild in-range number mutation) → suite
   semantics corrected; final **68/68 bites on the original design, 51/51 on the delta**, all silent
   on real content.
2. **Two wrong needles of my own design.** The probe scratch run caught `8,316 B / `f95c5a05``
   (ellipsis before the closing backtick) and a guessed map-row needle (true H1: `# 07 — EVM
   interface inspection (round 3)`); both fixed, re-verified.
3. **Table lands without the digest re-pin.** Stale-pin demo → exit 2 `pointer_table_tampered`,
   no silent findings (frozen-run guard holds).
4. **C2's same-commit revision breaks needles.** Grepped every delta needle that touches
   `.ufo/gates/custody-pair/**` against C2's in-progress worktree revision (README `fa484d57…` →
   `f30df42e…`, tool `112d01dc…` → `7cd19c3c…`): all survive (`CUSTODY_PATHS` 7 lines; each path
   string 2 lines). **Verdict: delta safe; one landed needle stays at risk** — EX-41's
   `skill-registry-custody-pair-row` needle is the precedence sentence C2's claim revises (H2, plan
   §6.1, mitigation named).
5. **Relative-path citation conforms (README `../waves/`).** Refuted by measurement: `.ufo/gates/waves`
   absent, `git show HEAD:../waves/…` exit 128 → NO-ENTRY as written + patch text.
6. **Operator-path citation might be pinnable.** Refuted: rule #11 by construction; converted to the
   in-repo `CUSTODY_PATHS` proxy coverage (an upgrade over EX-41's blanket exemption).
7. **Census under-scoping.** S7 diff scan + instrument scans (S8-S11) found exactly one surface the
   four families did not name — the census instrument's own SCORECARD citations; EX-41 had already
   covered all three (ratified). No other uncensused source in the r1/r2 commits.

## 5. Blockers

None blocking. Carried hazards (named, with procedure): **H1** base table moved mid-seat — all
numbers re-based on `bfc42f1b`, builder re-runnable; **H2** re-verify the landed custody-row
needle after C2's landing revision (plan §6.1); **H3** README path-form patch needs a human decision
(C2's file, same-commit ordering); **H4** if EX-41 revises the table again, re-run the builder and
use the fresh `c895a671…`-derived digest, never a carried-over one.