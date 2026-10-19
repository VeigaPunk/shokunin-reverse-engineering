# Seat RV-3 — chain c2, role reviewer — arc3-loop1-round2

Mutation test of the H1 absent-file guard: on a `/var/tmp` copy of the landed v11,
revert ONLY the H1 guard → absent SKILL.md must return to silent PASS.

Instrument under test (READ-ONLY here): `.ufo/gates/c1-census-v10.py`,
sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(31,906 B, mtime 2026-10-19 09:19:52 −03, hash re-confirmed unchanged at 09:25 −03).
The instrument's `main()` block (§ the guard lives there) digests to
`2ae7ecd68a073987ed397e96137d0e7493fb1dbd74d48e2643696720d1ba2a61` and is
byte-identical across the last three landings. This seat wrote nothing to the real
target; scratch is under `/var/tmp/rv3-mutation`; custody paths untouched.

## 1. Work performed (evidence pointers)

- Read the frozen wave file, the round-1 H1/H3 patch texts, and the pre-landing v10
  instrument (`6f1d19ff…`, 23,939 B); before-state captured at 09:03 −03.
- Built a pre-landing projection (v10 + RV-11's H1 patch text) plus a scenario suite,
  then rebuilt the harness for the landed shape (`tools/mutate-h1.py` +
  `tools/run-suite.sh`; `tools/mutate-h1-v2.py` + `tools/landed-battery-v2.sh`).
- Four independent mutation cuts of the landed instrument, 11 fixtures, 66 runs —
  `receipts/landed-run/battery-matrix.txt`, `receipts/landed-run/rcpt/`.
- Round-1 origin reproduction on RV-11's `atk-missing` root —
  `receipts/landed-run/{m-full,landed}-r1-atkmissing.txt`.
- JSON-channel pair — `receipts/landed-run/{landed,m-full}-noskill.json`; ordinary
  HEAD run — `receipts/landed-run/landed-at-head.txt`.
- Primary artifact: `claims/c2/RV-3/mutation-h1.md`.

Landing churn (EX-16 editing through the window): v10 `6f1d19ff` → `1431620f` →
`2a89793a` → `65442158` → `9373964c` → `a455391e` → `82fb807e` → `df9ffdf9` →
`a4c16763` → `d0772ce8` (pinned; 31,906 B). The last two landings changed header
stanza text only — the `main()` block digest (`2ae7ecd6…`) is identical across
`df9ffdf9`, `a4c16763` and `d0772ce8`. The battery was run against all four of those
landings; every H1-relevant row is identical.

## 2. Proposed changes

None. This seat is a reviewer; no real-target write, no patch text needed. The landed
H1 already covers the subclass this seat would have proposed hardening for (0-byte /
rows-past-declared-EOF truncation), so no follow-up patch is warranted.

## 3. Before → after (chain c2 claim, H1 leg)

Fixture: SKILL.md absent, PROVINCE.md + SCORECARD.md present (round-1 origin shape).

```
before (v10, sha 6f1d19ff):  exit 0  VERDICT: PASS   SKILL.md lines=0 loci=0     # silent PASS
after  (v11, sha d0772ce8):  exit 1  VERDICT: FAIL   UNREADABLE ['SKILL.md: FileNotFoundError']
                                     --json: declared_fail_classes=['UNREADABLE'], SKILL {lines: null, loci: null}
mutation (H1 reverted):      exit 0  VERDICT: PASS   SKILL.md lines=0 loci=0     # silent PASS returns
                                     --json: classes [], SKILL {lines: 0, loci: 0}
control (H3 reverted only):  exit 1  VERDICT: FAIL   UNREADABLE ['SKILL.md: FileNotFoundError']
ordinary run at HEAD:        exit 0  VERDICT: PASS (0/0/0/0)  UNREADABLE []  DECLARED FAIL CLASSES []
```

Mutant footprints vs the landing: whole-H1 revert 24 changed lines (H1 lines only),
verdict-term-only 4, rows-beyond-EOF-only 9, H3-only 4
(`receipts/landed-run/diff-landed-vs-*.diff`).

Verdict: **the guard is load-bearing** — reverting only H1 restores the round-1 silent
PASS (exit 0, text and JSON). On RV-11's own round-1 fixture the mutant's report is
identical to the round-1 receipt apart from the two lines H3 added. The load-bearing
link is the verdict term at `c1-census-v10.py:569`; the H3-only control still FAILs,
so H1 — not H3 — carries absence.

## 4. Attacks / refutations attempted (with verdicts)

- A1 whole-H1 revert → silent PASS — **CONFIRMED** (exit 0, `lines=0 loci=0`, no
  UNREADABLE line; JSON also PASS with classes `[]`).
- A2 verdict-term-only revert → guard collects and reports but does not fail —
  **CONFIRMED**: PASS exit 0 while `UNREADABLE ['SKILL.md: FileNotFoundError']` is
  still printed. A report-only variant of this guard would be inert; the term at
  `:569` is the guard.
- A3 H3-only revert with H1 intact → still FAIL — **CONFIRMED** (isolation).
- A4 mutant is vacuous / a blanket PASS — **REFUTED**: `m-full` still FAILs exit 1 on
  `atk-undecl`, absent PROVINCE.md, absent SCORECARD.md, all-absent.
- A5 absence is doubly covered, hiding a broken H1 — **REFUTED**: for a missing file
  the H3 per-file floor is exempt (`filelines[f] is None`), so absence rests on H1
  alone (proved by A1).
- A6 truncation subclass (beyond the strict claim wording): 0-byte and 10-line
  SKILL.md read PASS under v10, FAIL under the landing (`0 lines < declared max 20`)
  — **CONFIRMED closed on two independent paths**: H1's G19 site and H3's per-file
  floor (removing the G19 site alone leaves those fixtures FAILing as
  `BLIND-INSTRUMENT`, `UNREADABLE []`), so that cut is redundant, not load-bearing.
- A7 directory-as-file / mode-000 file — **CONFIRMED covered**
  (`IsADirectoryError` / `PermissionError`, both declared UNREADABLE, both reverted
  to PASS by the same mutation).
- A8 churn invalidates the pin — **REFUTED by digest**: `main()` byte-identical
  across the last three landings, battery re-run green on the newest; a moved anchor
  makes the harness abort rather than mutate the wrong code.

## 5. Blockers

- Hash churn: the instrument changed nine times in the window; measurements are
  pinned to `d0772ce8` (block digest `2ae7ecd6…`). If EX-16 edits again,
  `mutate-h1-v2.py` aborts on a moved anchor, so this test must be re-run (≈3 s)
  rather than re-cited — no silent reuse.
- The census has no `--selftest`; the mutation evidence is behavioural (exit codes,
  verdict lines, JSON payloads), not an in-file assertion.
