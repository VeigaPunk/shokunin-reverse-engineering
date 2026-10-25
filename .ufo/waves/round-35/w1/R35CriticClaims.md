# R35CriticClaims — UFO-FSD critic report (wave 1)

Seat: `R35CriticClaims`. Assignment: **falsify claim separability and control reachability** for frozen claims C1/C2 (round 35, wave 1). Review only — no edits, no lane mutations, no scoring.

Method: read-only inspection of plan/claims/counters/controls at `aa04633a`…HEAD (`3ecf4298`); all instrument runs executed in `mktemp -d` sandbox repos; lane untouched. Counter selftests pass (C1 green=0 red=1; C2 green=0 red=1).

---

## F1 — SEVERABILITY: C2 D-1 has a hidden prerequisite on C1 (cross-claim coupling)

- `c2-calibration-counter.py` D-1: if no commit in `base..rev` touches `corpus/SOURCES.md`, it appends `D1_no_sources_change_after_base` and fails the claim (lines 71-77).
- In this round, **only C1's data landing edits `corpus/SOURCES.md`** (rows S125/S129). No other round-35 work touches it (verified: `git diff --stat aa04633a..HEAD` — no SOURCES change; plan §C1 is the only SOURCES writer).
- Consequence: C2 cannot close D-1 unless C1 lands. C2's score is hostage to C1's execution — the two claims are not separable, and C2's "do-nothing cannot reach it" sizing fails (a C2-perfect state with C1 stalled still fails D-1).
- Proof (sandbox): all four defects green (census committed before a SOURCES change, lesson totals == settle receipts, r34b trio present, both registry sections exactly 8 cells) but **no post-base SOURCES change**:

```
$ python3 -I -B tools/round-35/c2-calibration-counter.py --root $D --base $BASE --rev HEAD --freeze $BASE
C2_FAIL: D1_no_sources_change_after_base
exit=1
```

- Impacted axes: calibration (C2) primarily; claim-independence claim (plan §"fresh-start", "do-nothing control cannot reach it") invalid for C2.

## F2 — CONTROL REACHABILITY: D-1 content check is substring-only; frozen-input pin never enforced

- D-1 content check (lines 68-69) accepts any census containing substrings `rows=106`, `EXIT=0`, `W04`. It does not parse the row count, the warning count (`9 W04` is never verified), or the receipt's authenticity.
- `frozen_inputs` pins census-start.txt to sha256 `b6ce2b17…` (claims-canonical.json), but **the counter never reads or validates that pin** — an amended or fabricated census with the substrings passes.
- Proof (sandbox): census content = `rows=106 EXIT=0 W04` (no 106 rows, no 9 warnings, no real census) after a normal post-base SOURCES change:

```
$ python3 -I -B tools/round-35/c2-calibration-counter.py --root $D --base $BASE --rev HEAD --freeze $BASE
C2_CLEAN revision=HEAD
exit=0
```

- The documented junk controls cover only D-2 (lesson numbers) and D-4 (cell count); **no junk control exists for D-1 or D-3**. D-3's checks are also substring-only: `^source\s*:.*S106` matches `source: S1060`; `AAdjacencyCite`/`31/32` (D-2) are presence-only substrings, so a lesson stating the correction was *not* applied still passes those two sub-checks.
- Impacted axes: calibration (C2) control reachability; frozen-input integrity claim.

## F3 — CONTROL REACHABILITY: D-4 cannot be closed without rewriting archived historical records

- The counter matches section headers by exact equality (`l.rstrip() == sec`). Actual SKILL.md at base/HEAD:
  - line 1209: `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)` → **not an exact match** → `D4_section_missing` even though the section exists;
  - round-32 section spans two tables: residual-witness rows (lines 1081-1084, 4 cells) and the main registry (lines 1090-1092, 7 cells) → each fails `D4_not_eight_cells`.
- Closing D-4 therefore requires (a) deleting the historical qualifier from the round-34 header and (b) re-piping archived tables to exactly 8 cells, including a 4-column "Residual witness registry" whose columns predate this format. This is a historiographic rewrite driven by raw `|`-count (`l.count("|") - 1`), not closure of any record defect; it can selectively fabricate column semantics for archived rows.
- Impacted axis: calibration (C2) — D-4 as designed scores formatting, not defect closure; the only reachable "closure" is a cosmetic rewrite of the historical record.

## F4 — Timing robustness: D-1 ordering compares committer timestamps, not commit order

- `parse_iso(commit_time(census)) > parse_iso(first_change_time(SOURCES))` uses `%cI` wall clock. This repo already commits multiple objects within the same second (e.g. `16:05:46` for `d2729cba` and three siblings). Equal-second commits make `ct == fc` → check passes even when the census topologically follows the first SOURCES change; clock skew can invert the verdict the other way.

## Minor (non-blocking)

- C1 `province_missing` is a plain substring search for the entry stem anywhere in PROVINCE.md; the plan's "Round-35 Core-addition table row" is not enforced (a prose mention or TODO line would pass).
- C1 row-citation `^source\s*:.*S125` also matches `source: S1250` (no word boundary); C1's red selftest only exercises missing trio, not wrong-row citation.
- C1/C2 `--freeze` predicate check is a substring-of-`json.dumps` match; acceptable but weak.

---

## Smallest safe corrections (advisory)

1. **D-1 bifurcation**: when no post-base SOURCES change exists, score D-1 as *unevaluable* (exit 2) or neutral-pass — never a failure — and declare C2 independent of C1 in the predicate text. Alternatively, make the check read the `frozen_inputs` sha256 from the claims file at freeze and byte-verify the census, parse `rows=`/`EXIT=`/warning count properly, and compare commit order topologically (`git rev-list --ancestry-path`) instead of `%cI` timestamps.
2. **D-3**: require the appended trio to be a separately appended block (position after the existing header), match `S106` at a word boundary, and add a red fixture for wrong-row citation (the plan's junk controls should include D-1/D-3 red cases).
3. **D-4**: anchor sections by stable heading *prefix* (accept the round-34 qualifier suffix) and count true cells (handle escaped/inner pipes), or explicitly scope the check to the registered instrument-registry table with declared column semantics so archived tables are not rewritten to satisfy raw `|`-count.
4. **C1**: bind the PROVINCE check to a table row (e.g. require the stem in a `|`-delimited row) and use word-boundary row IDs both in SOURCES used-by and entry citations.

Limits: static/worktree-free review; sandbox proofs used the frozen instruments verbatim; no lane writes; no delegation; pacman paused; no `find`/`du` under `/fast/scratch`.
