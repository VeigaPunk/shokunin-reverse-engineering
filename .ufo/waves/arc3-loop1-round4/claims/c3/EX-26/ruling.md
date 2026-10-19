# (d) ruling — after-state verification (seat EX-26, chain c3, wave arc3-loop1-round4)

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`015e1bab914713568f339fd53999bc180459cc40` · gate pair measured read-only
(hash/stat only), 11:05-11:12Z, 2026-10-19.

**Verdict: the (d) ruling text is present in the README and the landed tool's
behavior matches it — verified first-hand on the landed bytes.** One named caveat:
the README was still churning when I closed (two revisions inside my window), so my
text-side digest binds the `125e7e02…` bytes I measured, and the parent must
re-derive at landing.

## Identities (read-only, rule #14)

| artifact | r3 revision (before) | landed revision (after) |
|---|---|---|
| `custody-pair.py` | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (54,279 B) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (65,902 B) |
| `README.md` | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` (9,603 B / 185 lines) | `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` (272 lines) — final bytes in my window; intermediates `a418675b…` (14,057 B) and `125e7e02…` (14,978 B / 267 lines) both carried the ruling section |

The README moved `a418675b…` → `125e7e02…` → `9d9400da…` while this seat was
measuring (all three carry the ruling section; the last adds the attribution
paragraph crediting this seat's authorship and EX-21's clause correction); the tool
was stable across my whole after-state window. **Re-verified on `9d9400da…`:**
`readme_ruling()` = 10 hits, probe `reported findings=0` / `clean findings=0`,
cleanly-absent fixture still `MATCH exit 0`.
Evidence: `evidence/evidence-4.txt` §1, `evidence/tool-landed-29bb45ae.py`
(byte-copy of the landed tool, digest in `evidence/sha256sums.txt`).

## 1. Text leg — the ruling is present

`## The both-absent `MATCH` (ruling, arc3-loop1-round4)` sits immediately before
`## Exit codes (declared)` and states the ruling in the form this seat proposed:

> …the adjudication is the declared design: **only error-carrying stanzas are
> `UNEVALUABLE`; a cleanly absent stanza on both sides is `MATCH`.**

The landed text also adds two clauses my proposal did not carry: a "closing this
with a flag was considered and rejected" sentence, and the claim that the coverage
gate is a distinct-path gate since round 4. **I verified that second claim
first-hand** — see §3 R-1.

EX-27's own (d) check (`readme_ruling()` in
`claims/c3/EX-27/harness/regress-r4.py`, run verbatim) reads **10 hits** on the
landed README (`evidence-4.txt` §8), up from **0** on the r3 bytes.

## 2. Behavior leg — the tool matches the ruling

All runs on scratch copies under `/var/tmp/ex26`; the real gate pair and the five
custody paths read-only throughout. Raw captures: `evidence/evidence-1.txt`,
`evidence-2.txt`, `evidence-4.txt`; harness `evidence/harness-behavior.sh`.

| # | fixture | observed on landed tool `29bb45ae…` | matches ruling |
|---|---|---|---|
| F1 | cleanly absent, receipt-vs-live | `MATCH` exit 0 | yes |
| F2 | control: path appears later | `ABSENT` exit 13 | yes (non-vacuity) |
| F3 | cleanly absent, receipt-vs-receipt | `MATCH` exit 0 | yes |
| F4 | `READ-ERROR` both sides vs live | `UNEVALUABLE` exit 14 | yes |
| F5 | `READ-ERROR` reference only | `UNEVALUABLE` exit 14 | yes |
| F6 | `READ-ERROR` candidate only | `UNEVALUABLE` exit 14 | yes |
| F7 | `READ-ERROR` candidate, receipt-vs-receipt | `UNEVALUABLE` exit 14 | yes |
| A1 | five distinct cleanly-absent paths, `--require-paths 5` | `MATCH 5/5` exit 0 | yes |
| A3 | one path repeated 5×, `--require-paths 5` | `USAGE` exit 2, `REFERENCE-COVERAGE: 1/5 … unaccounted: <5 paths>` | yes (see R-1) |
| A5 | readable + error-carrying mixed | `UNEVALUABLE` exit 14 | yes (worst class) |
| A6 | content-drift + cleanly-absent mixed | `CONTENT-DRIFT` exit 10 | yes (worst class) |
| B1 | **cleanly-absent ref vs `STAT-ERROR` candidate** | `UNEVALUABLE` exit 14, **not** `MATCH` | yes — the boundary |
| B2 | `STAT-ERROR` ref vs cleanly-absent live | `UNEVALUABLE` exit 14 | yes |
| B3 | `STAT-ERROR` both sides, receipt-vs-receipt | `UNEVALUABLE` exit 14 | yes |

Selftest on the landed tool: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28
failed=0 exit=0` (22 → 28; the new cases include
`both-sides-absent-is-agreement-match`, `coverage-gate-rejects-duplicate-stanzas`,
`coverage-gate-passes-distinct-five`).

The landed tool also adds a per-row note on the both-absent row, which is stronger
than the README text alone:

```
PATH /var/tmp/ex26/behavior/fx/live/gone.txt: MATCH  compared=0/11
    note: both sides record the path absent — the MATCH is an agreement on absence,
    not a verified presence (declared ruling: only error-carrying stanzas are UNEVALUABLE)
```

## 3. Attacks/refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | both-absent `MATCH` is fail-open (hides an appearing path) | **REFUTED** — F2 reads `ABSENT 13` |
| A2 | the `MATCH` is vacuous | **CONFIRMED as a bounded property** — `compared=0/11` by design; now stated in both the README ruling and the per-row note; unreachable when either side errors (B1) |
| A3 | cleanly-absent ref swallows a candidate-side error | **REFUTED** — B1 reads `UNEVALUABLE 14` |
| A4 | absent-`MATCH` outranks real drift | **REFUTED** — A5/A6 worst-class precedence holds |
| A5 | the ruling text would break the citation-drift gate | **REFUTED** — probe reads `reported findings=0 exit=0` and `clean findings=0 exit=0` on the landed repo, and its selftest is 13/13 |
| A6 | the four `custody-readme-*` anchors are decorative | **REFUTED** (measured on the r3 bytes, scratch clone) — each anchor reddens its own entry when neutered; restore returns clean |
| A7 | my R-1 residual (dup stanzas satisfy the coverage gate) still holds | **REFUTED by the landed tool** — A3 now exits 2 with `REFERENCE-COVERAGE: 1/5`; the landed README's distinct-path claim is true |
| A8 | the landed README's ruling is my block verbatim | **REFUTED** — the landed text is an edited version (my stanza-gate sentence replaced by the flag-rejection sentence and the distinct-path clause). Reported as an edit, not a defect; the operative content is intact |
| A9 | the landed tool silently regressed a class while adding the distinct-path gate | **REFUTED** — all 14 fixtures reproduce their r3 classes except A3, which closed as declared |

## 4. Residuals named (not absorbed)

- **R-1 (closed).** The r3 coverage gate counted stanzas; one path repeated N times
  satisfied `--require-paths N`. The landed tool counts distinct paths and exits 2
  (A3, measured). My original R-1 is closed by the landed revision.
- **R-2 (text churn).** The README moved `a418675b…` → `125e7e02…` inside my
  measurement window. Both carry the ruling section; my text-side findings bind
  `125e7e02…`. The parent must re-derive the README digest at landing (rule #14).
- **R-3 (stanza-shape caveat).** "Cleanly absent" is "no sha256 and no error key"; a
  hand-written stanza recording `EXISTS: no` *and* a bogus `SHA256` would take the
  content path, not the both-absent branch. No in-tree producer emits that shape.
- **R-4 (my proposal superseded).** `proposed-readme-ruling.patch.md` was written
  against `f30df42e…` and is **superseded** by the landed text. Do not apply it. It
  is retained as the provenance of the ruling wording, not as a pending change.

## 5. Provenance

No seat report was treated as evidence. Every number above is a command result or
digest measured by this seat against the named bytes. This seat wrote no real
target: the gate pair, the custody paths, LOG.md, SCORECARD.md, corpus/, SKILL.md,
PROVINCE.md and every README were read-only (hash/stat/read only); all mutation ran
on scratch copies under `/var/tmp/ex26` (`/tmp` never used); no git mutation in the
real repo (the scratch clone's commits are local to `/var/tmp/ex26/clone`).
