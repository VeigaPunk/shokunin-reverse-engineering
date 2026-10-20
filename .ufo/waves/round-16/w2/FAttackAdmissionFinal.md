# FAttackAdmissionFinal — wave 2 critic (depth, calibration)

Target: falsify "axis scores stay bounded, capability table unchanged, no scalar/SHONEN upgrade" against the **current worktree** (uncommitted round-16 edits over baseline `6235498b4112350eebce0812a74af1781fc0ee88`).
Method: `git show 6235498:<path>` vs worktree bytes, plus a static re-implementation in my own Python kernel of the citation-drift probe's `anchor`/`exact`/`extracted` checks (`.ufo/gates/citation-drift/citation-drift-probe.py:168-259`). I did **not** run the probe, selfcheck, selection, controls, measure or any other check. Every probe outcome below is `[INFERENCE]` from that static re-derivation. L1 must confirm it with the real strict probe.
Tool installs/updates: none.

## F1 — HIGH: new coverage-map row repeats round-12 Mistake #9 and kills 5 pinned citations

**Counterexample.** `corpus/README.md:36` adds a separate row: `| \`knowledge/2026-10-20-r16-go-selection-preview\` | … |`. It sits above `## Frontier`, so every README line from 36 down moves by +1 (190 → 191 lines). Five live pointer-table entries without a `stamp` read fixed README lines:

| entry (`pointer-table.json`) | cites | baseline line holds | worktree line holds |
|---|---|---|---|
| `sc69-readme-177` | `SCORECARD.md:69` → `corpus/README.md:180`, needs "held, not frontier" | Runtime-obs bullet ✓ | `- PE reserve: ARM64X…` ✗ |
| `sc72-readme-nitrow` | `SCORECARD.md:72` → `corpus/README.md:138`, needs "4 nits: 2 fixes…" | round-13-distillation row ✓ | r14-02 knowledge row ✗ |
| `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2` | `corpus/README.md:175` must carry `SCORECARD.md:N` / `r7-pe-wall.md:N-M` / `round8/E2.md:N-M` | >90MB PE bullet ✓ | `` - `.jsc` → source mapping `` (pattern absent) ✗ |

I re-derived all 21 entries that touch a round-16-changed file. All 21 resolve at baseline and 16 resolve in the worktree. Per `citation-drift-probe.py:77-93`, any non-`citation_historical_ok` finding under `--strict` gives FAILED, exit 1. r15's last clean strict run was `.ufo/waves/round-15/final-recheck.json`, `citation-final`, exit 0 at `ba3b219`. Between `ba3b219` and the baseline, the only change was the SCORECARD append, which does not affect lines 69 or 72.

**Precedent.** This is the identical five-finding class (`sc69`, `readme175`×3 plus one SHONEN entry) recorded in `corpus/lessons/round-12.md:20` (Mistake #9). `SCORECARD.md:2071-2077` states the rule: "the index cannot grow above `## Frontier` while `SCORECARD.md:69` pins `corpus/README.md:180`". Rounds 14 and 15 obeyed it by appending their tokens to existing row 35 (`corpus/README.md:35`). `controls.py` cannot see this harm because it checks no pointer-table entries and no README line stability. Its byte, prefix and craft fields can therefore look clean while the strict citation gate fails.

**Axes.** Calibration is harmed: a recorded lesson recurs while the round claims improved provenance discipline. Depth: no proxy change. The round-16 LOG bullet "New map row … retain those limits" describes the harmful insert as neutral.

**Smallest safe correction (in-place, net 0 lines):**
1. Delete README line 36.
2. Append `` , `2026-10-20-r16-go-selection-preview` `` to row 35's entry cell.
3. Add one short r16 clause to row 35's state cell, and the exact exercised selection argv to its evidence cell.

This keeps command A at 94/94 (worktree token set: 94 knowledge stems, 94 mapped, missing `[]`). Do **not** copy r12's "remove the row" fix: r12 removed a lessons-index row, but this row is a counted knowledge token. Removing it without relocating drops coverage to 93/94 (9.89), which is a scalar regression. Then reword the LOG bullet to "map token appended to the existing Go row". L1 runs the strict probe once at the integration commit.

## F2 — MEDIUM: registered fixture recheck does not exercise the negative fixtures it names (QUALITY #18 self-violation)

In the `SKILL.md` go-selection-preview row (`SKILL.md:~505`), the fixture-check command is bare `python3 -I …/selfcheck.py`. `selfcheck.py:81,379-380` defaults to `selection-fixtures.json` **only**. The same row's pinned-values cell names both `selection-fixtures.json` and `negative-fixtures.json`. Running the registered command never loads the negative cases.

This conflicts with the round's own new `corpus/QUALITY.md:29` (#18), which requires future recheck guidance to match "the exercised isolation flags and paths or explicitly name an unexercised variant".

README row 36's recheck (`python3 -I .ufo/waves/round-16/selection.py --root <installed-golang-dir> …`) also uses a relative path plus a placeholder, while the knowledge entry and SKILL row use the absolute exercised form. That is the same class as r15 route 1, introduced in the round that claims to discharge it.

**Correction:**
- Make the SKILL fixture cell the exact argv L1 retains, e.g. `… selfcheck.py --fixtures <abs>/selection-fixtures.json --fixtures <abs>/negative-fixtures.json`. Use absolute paths: `--fixtures` resolves against the cwd.
- In the relocated README evidence cell, either use the absolute argv or write "placeholder form; exercised argv in verification.json".

## F3 — MEDIUM (conditional): `verification.json` is cited as retained but does not exist yet

`.ufo/waves/round-16/verification.json` is absent from the directory listing, yet three places describe results as already retained there:

- `corpus/README.md:36`: "retained argv/results in `.ufo/waves/round-16/verification.json`"
- the SKILL go-selection-preview row: "execution results retained in `verification.json`"
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:3`: "compare the retained per-file identities … in `.ufo/waves/round-16/verification.json`"

Line 2 of the same entry defers to an unnamed "execution addendum". The C2 "after" state ("all four resolved with reproducible command evidence", `claims.json:14`) likewise depends on outputs not yet retained: the documentation-red rerun and the `controls.py` output for route 3.

This is fine only if L1 writes exactly that path, with those argvs, before the records commit. Otherwise it is false provenance under #18.

**Correction:** L1 writes `verification.json` at that exact path and includes the selection, selfcheck (both fixture files), controls, measure, documentation-red-after and strict citation-drift argv/exit/stdout. If not, change "retained" to "to be retained" in all three places. No checks are claimed passed by this report.

## F4 — LOW: depth claim cannot move the depth scalar; keep the SCORECARD row at delta 0

`claims.json:5` declares C1 on depth. Command A's depth proxy reads only the `## Queue-drain craft` section (`SCORECARD.md:103-117`). That section is byte-identical to baseline, with 17 rule blocks. The SKILL edits are an in-place row change at line 449 and an append from line 489, both outside the section that ends at line 318.

Any depth figure other than 10.0 → 10.0 (delta 0) would be invented. `corpus/lessons/round-16.md:10` says "calibration works that tied-lowest axis" but does not name C1's depth slot. Make the SCORECARD row mirror the r15 form (`SCORECARD.md:2247`): proxy delta 0, with any "improved" verdict labelled author-side and qualitative.

## Bounded no-findings (checked, not executed)

- **Capability table unchanged:** `git diff --quiet 6235498 -- SCORECARD.md PROVINCE.md .ufo/gates` returns 0. `SCORECARD.md:615-624` is untouched. The LOG says "no capability table row".
- **SHONEN:** all four marks are `[~]` and there is no `[x]`. The only edit is the in-place line 10 wording. The `shonen-skill-range`, `shonen-province-range` and `sc-arc3r2-cites-shonen` pointers still resolve (re-derived).
- **SOURCES:** 23 → 23 rows, no IDs added or removed. Only cell 11 (used-by) changed, and only for S003 and S023, as prefix-preserving appends.
- **QUALITY #18:** inserted at line 29. No pinned `QUALITY.md:` citation at ≥29 exists in the live surfaces, and the `arc3r1`/`r7wall` QUALITY pointers resolve.
- **Knowledge appends:** the r14 final-sweep and r15 inventory edits are pure tail appends. The r15 correction's argv exactly matches `.ufo/waves/round-15/verification.json` `commands[2..3]`, revision `7ad23fe`. The r14 correction's cited lines 146-150 hold the quoted overclaim.
- **Fixtures:** no hand-written sha256 or size expectations, and no "pass" asserted in docs. `selfcheck.py:4-5` disclaims gate and score status.
