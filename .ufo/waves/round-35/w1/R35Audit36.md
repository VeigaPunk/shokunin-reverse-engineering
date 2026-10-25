# R35Audit36 — reviewer report (round 35 wave 1: build evidence / first falsifications)

Scope: froze claims C1 (coverage: `.jsc -> source mapping` via S125/S129) and C2
(calibration: closure of R34 D-1..D-4). Reviewed the actual landed diff (base
`aa04633a` → HEAD `3ecf4298`) and the frozen instruments/controls. Only read-only
verification was run; nothing mutated (no lane writes except this report).

## 1. Verified evidence (commands and observed output)

| # | check | command | result |
|---|---|---|---|
| E1 | do-nothing control C1 at base | `python3 -I -B tools/round-35/c1-coverage-counter.py --root <LANE> --rev aa04633a --freeze 2323d197` | exit 1; 8 named failures: entry_missing ×2, registry_row_missing:S125/S129, province_missing ×2, readme_missing ×2 |
| E2 | do-nothing control C2 at base | `python3 -I -B tools/round-35/c2-calibration-counter.py --root <LANE> --base aa04633a --rev aa04633a --freeze 2323d197` | exit 1; 8 failures incl. D1_census_start_missing, D2_lesson_missing, D3_* ×4, `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4`, `D4_section_missing:### Round-34 run-6 instrument registry` |
| E3 | selftests | `c1-coverage-counter.py --selftest` / `c2-calibration-counter.py --selftest` | both `ok` (green=0 red=1), exit 0 |
| E4 | counter pins at HEAD | `sha256sum tools/round-35/c1-coverage-counter.py c2-calibration-counter.py` | `e28792c7…` / `576c14dd…` = canonical `instruments` pins exactly |
| E5 | instrument bytes at `instrument_revision` d2729cba | `git show d2729cba:tools/round-35/… | sha256sum` | `cd4ab7e7…` / `39fe39c5…` — **do not match the pins** |
| E6 | instrument bytes at supersession commit a85ca674 | `git show a85ca674:…` | `018e96d0…` / `3a23f3eb…` — also not the pins (pins are the 2323d197/HEAD bytes) |
| E7 | first-add commits | `git log --diff-filter=A` | `claims.json` first added 131eacfa; `claims-frozen.json` first added 13d7a815, removed 50174048, re-added e4ca43dd; `claims-canonical.json` first added 2323d197 (same commit as last counter bytes) |
| E8 | freeze gate result | recorded in `.ufo/waves/round-35/freeze-status.md` | `freeze-integrity: FAIL pins=4 changed=2 freeze=13d7a815…`; exit 1; `INSTRUMENT_REVISED` debt documented |
| E9 | claim-freezes.tsv row | `git diff base HEAD -- corpus/claim-freezes.tsv` | round-35 row = `FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED` (counter/freeze first committed together, finalized later) |
| E10 | census receipt | read `.ufo/waves/round-35/assimilation/census-start.txt` | `rows=106`, `EXIT=0`, exactly 9 `W04` lines; sha256 `b6ce2b17…` = `frozen_inputs` pin; committed in d2729cba, before any SOURCES.md change post-base |
| E11 | plan pin | `sha256sum plans/round-35-claims.md` | `45b644a4…` = canonical pin |
| E12 | predicate byte-identity with plan | grep + normalization of `plans/round-35-claims.md` | neither P35-c1 nor P35-c2 sentence appears in the plan file (plan conveys content as After-state bullets) |
| E13 | jsc source captures | read prep/`jsc2js-readme.md`; JSON-parse `releases-page1.json`/`releases-page7.json` | valid; 100 + 77 GitHub releases for `xqy2006/jsc2js` (tags 15.6.75.19 / 12.9.202.26, d8 linux/windows assets) |
| E14 | pre-data state | SKILL.md, PROVINCE.md, corpus/README.md, SOURCES.md, lessons/round-35.md, knowledge entries | SKILL.md unchanged base→HEAD; PROVINCE/README/SOURCES untouched by round-35 commits (no S125/S129 yet); `lessons/round-35.md` absent; `w1-settle.json` exists (untracked, wave-1 artifact), `w2-settle.json` absent — data not yet landed |

## 2. Findings

### HIGH

- **H1 — Setup order violates the plan's own freeze discipline.** The plan requires
  instruments (counters + selftests + red fixtures) committed *before* `claims.json`
  and a single first-add freeze commit. Observed: earliest claims object (`claims.json`,
  131eacfa) predates the final counter bytes; the canonical claims file
  (`claims-canonical.json`) was first added in the **same commit** as the last counter
  mutation (2323d197); the red do-nothing receipts were committed *after* the canonical
  freeze (3ecf4298). E7/E8/E9. The lane discloses this in freeze-status.md, the
  `instrument_supersessions` array, and the claim-freezes.tsv row — good honesty, and
  the canonical snapshot is self-consistent (freeze=2323d197 ⇔ pins ⇔ HEAD bytes,
  E4/E1/E2), but the round carries `INSTRUMENT_ABSENT,INSTRUMENT_REVISED` baggage of
  the exact class that stopped earlier rounds. Expect verifier scrutiny; a stop is
  plausible unless the supersession precedent (r24 CLEAN) is accepted.

### MEDIUM

- **M1 — Two competing claims files remain in the tree with different pins.**
  `claims-frozen.json` (first added 13d7a815) pins `a4be290a…`/`f36fad30…`;
  `claims-canonical.json` pins `e28792c7…`/`576c14dd…` (E4). The round-34 freeze gate
  discovers by first-add and therefore rejects (E8). A scorer reading the wrong file
  fails pin verification; the stale file should be removed or pointed to before scoring.
- **M2 — `instrument_revision` metadata is stale.** Canonical JSON says revision
  `d2729cba`, but the pinned bytes are the 2323d197/HEAD bytes (E5/E6); the supersession
  entry cites a85ca674, whose bytes also differ from the pins. The final re-pin (2323d197)
  is undocumented in the supersession list.
- **M3 — D-4 check is stricter than its wording and currently un-passable as coded.**
  `c2-calibration-counter.py` counts cells on **every** `|`-line between the section
  heading and the next `##`/`###`, including headers, separators, and unrelated tables.
  Inside the Round-32 section sits the 4-cell “Residual witness registry” table, which is
  why the base control reports `line1081:cells=4` (E2). Closing D-4 therefore forces
  rewriting/moving historical records, and the check breaks after the first bad row
  (subsequent defects masked).
- **M4 — Predicate matching is a loose substring, and the plan is not consulted.**
  Counters accept any claims object whose JSON dump *contains* the `PREDICATE` constant;
  byte-identity with the plan (E12) and with the claims file is not enforced. Receipts
  embed the counter constant, not the claims-file sentence.

### LOW

- **L1 — Counters do not self-pin.** Receipts carry no counter hash, no first-add
  freeze verification, and no check that `--freeze` is the canonical freeze commit;
  enforcement depends entirely on the (currently failing) gate.
- **L2 — D-1 vacuous case fails.** If measured revision has no post-base SOURCES.md
  change, `D1_no_sources_change_after_base` is reported; harmless for the real score
  (C1 guarantees S125/S129 rows land), but semantically a no-op closure is rejected.
- **L3 — D-1 uses the *latest* census-touching commit time.** A later repair to the
  census file after the first SOURCES change would invert the ordering and falsely fail.
- **L4 — D-2 settle arithmetic tolerates extra keys but adds zero for missing ints**
  (double-fault path already covered by the specific failure).

## 3. Positive observations

- Frozen counters are real, runnable, and match their pins at HEAD; selftests green/red
  behave (E3/E4).
- Controls at base fail exactly as declared (exit 1, named failures) — the do-nothing
  control is a genuine red fixture (E1/E2).
- Census receipt satisfies D-1 content (106 rows, exit 0, 9×W04) and is committed in prep
  before any data (E10).
- Kill rules are present in the canonical claims; no score has been produced on post-freeze
  data (no data landed: E14); no frozen predicate/scope was altered (E12 finds drift in
  *location*, not in content).
- jsc captures are real, dated, and source-plausible (E13).

## 4. Residual risk / verification gaps

- Freeze gate failure not re-executed (documented in freeze-status.md; read-only record).
- Live re-fetch of S125/S129 URLs not performed; captures are the evidence.
- Score-time D-1 ordering and D-2 totals cannot be exercised until data lands (w1/w2
  settle receipts, round-35 lesson).

## 5. Advisory bottom line

The claim machinery is internally coherent at freeze `2323d197` and controls behave, but
the round's freeze setup deviates from its own plan letter (H1, M1/M2) and D-4 as coded
cannot close without restructuring unrelated historical tables (M3). Treat the round as
setup-flagged; the honest supersession disclosure is the mitigation.
