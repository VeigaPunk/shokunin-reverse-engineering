# ConnCrossClaim — round 50 attempt 2, wave 3: C1×C3 cross-claim coupling

**Verdict: PASS with one blocking finding for the L1.** The attempt-2 claims doc says C1 and C3
"share no write surface except SCORECARD.md and LOG.md" — that is wrong, and the error is
load-bearing: the C3 claim's own instrument path lands inside the C1/C2-frozen `tools/round-50/`
family. Proved empirically in a scratch clone (lane untouched, read-only throughout): landing
`tools/round-50/sqfs-triage-v5.py` after the freeze trips C1 `frozen_drift` (exit 2,
`frozen_path_changed`) and C2 `freeze_check` (both its `touched` walk and its full-tree diff) at
any REV ≥ the C3 freeze commit; the walk covers the commit RANGE `435d41fd..REV`, so no later
repair un-trips it. Mitigation is free only before the C3 freeze: amend the C3 claim to
`tools/round-50c3/sqfs-triage-v5.py` (verified clean against both counters). With that one
change, a full simulated landing (instrument + registry row + block 22 + C1 docs) scores C2
all-11-atoms green, battery `failing []` (52 mutations), and all nine C1 documentation bindings
true.

Full matrix, per-file regions, drafting constraints, and the safe landing order:
`ConnCrossClaim/coupling.md`.

## Findings (ranked)

| # | Finding | Evidence (exact commands, exit codes, sha256s) |
|---|---|---|
| F1 BLOCKING | C3 instrument path `tools/round-50/sqfs-triage-v5.py` (claim text, predicate, counting command, registry bullet) collides with C1 `FROZEN_PREFIXES=('tools/round-50/',)` (`c1-counter.py:413,1661-1703`) and C2 `FROZEN=('tools/round-50','plans/round-50-claims.md')` (`c2-record.py:124,1090-1109`). C1 selftest pins the semantics: "a new file under tools/round-50 after the freeze" → exit 2 (`c1-counter.py:4252-4254`). The C1 counter raises `FrozenPathChanged` → `{"reason":"frozen_path_changed","exit_code":2}`; `met_target` never computed. C2's attempt-2 step-4 gate ("C2 consistency at the final REV exits 0") fails the same way. | `python3 -I -B $S/demo_coupling.py` in `$S/clone` (clone of the lane at `6f4aba63`): branch `c3-in-frozen` tip `94749500…` → `c1 frozen_drift -> ["tools/round-50/sqfs-triage-v5.py"]`, `c2 freeze_check -> {"code":"frozen_path_changed"}`; branch `c3-outside` tip `509a3d54…` (`tools/round-50c3/…`) → both walks `[]`/null; branch `c3-docs` tip `d1c4dc05…` (SKILL row + block 22 only) → clean. Receipt `ConnCrossClaim/receipts/counter-walks.txt`, stdout sha256 `ccb4b707a6917f45cb213822635c3dec4a0a2a5dc866f61a1d1ea4fd2c5d7a1e`, driver exit 0, 2026-10-29T20:46:38Z. Lane-side confirmation: `git log -m --diff-merges=first-parent --name-status 435d41fd..6f4aba63 -- tools/round-50` → empty (no drift at tip); `git diff --stat 435d41fd 6f4aba63` over all frozen paths → 0 lines. |
| F2 HIGH (measured, self-caught) | C1's README coverage-map row must be a table line INSIDE `## Coverage map` — `section()` stops at the next `## ` heading. My first draft appended it at end-of-file → C2 B1 red: `knowledge files not mapped in README Coverage map: ['corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md']`. | `python3 -I -B $S/validate_landing.py` run 1 (tip `0a1e3fb8…`), in-session stdout captured 2026-10-29T20:52:50Z, recorded sha256 `02cefa8a41b7c12ecc88016d253f3ab8926e989b290a574629d2c3b13b7c5855`, driver exit 1 (file later re-tee'd by run 3; quoted output above is verbatim). Fixed and green in run 3 (`receipts/landing-validation.txt`). |
| F3 HIGH (measured, self-caught) | SCORECARD tail order is load-bearing: the C2 battery's five `duplicate line` mutations (B3/B4/B5/B10/B11) append `- B<n>` lines at end-of-file; they only flip their atoms if the file tail is still inside `## Record corrections — round 50` (currently the last heading, line 3790). Appending any `## ` section after it → `failing=["B3 duplicate line -> red [] noop []", "B4 duplicate line -> red [] noop []", "B5 duplicate line -> red [] noop []", "B10 duplicate line -> red [] noop []", "B11 duplicate line -> red [] noop []"]` and C2's kill rule trips. | Same driver run 2 (tip `da472fa0…`): score green but battery failing as quoted; in-session stdout captured 2026-10-29T20:55:23Z, recorded sha256 `ed1ec1e7a83fb0242cf2066d21120415bb309f6e41617689878e78373783b202`, driver exit 1. Fixed by inserting new sections before the corrections heading; battery `failing []` in run 3. |
| F4 MEDIUM | SCORECARD bullet hygiene: `_line_of` (battery mutation source) scans the whole file for `^ {0,3}- (B\d+)` and takes the first hit; `corr()` requires exactly one corrections section and one line per atom. Drafting rule: new sections use `- **C3:**`-style bullets, never `- B3 …`; never add a second corrections heading; never touch `## Round 48`/`## Round 49`. | Code walk `c2-record.py:423-493,1076-1088` + battery runs above (green at run 3 with compliant text). |
| F5 MEDIUM | B9 registry-row shape for the moved instrument (row optional for B9 — `tools/round-50c3` is outside `census_paths`' prefixes — but the C3 claim wants it): exactly 7 cells inside the `<!-- instrument-registry v2 -->` markers, visible (not fenced/commented — `vis` strips both), kind cell opens `gate|probe`, verdict map parses as exactly `0=;1=;2=` with three DISTINCT meaning classes (success / not-met / could-not-evaluate; placeholder text is caught by `BANANA`), selftest cell `<interp> <path> … --selftest` or `none — <reason>`, pinned cell a path or `none — <reason>`. My drafted template row passes all five checks. | `validate_landing.py` step 5 (registry_region + meaning_classes + regexes from `c2-record.py:806-851,852-889`): `{"cells==7": true, "kind gate|probe": true, "verdict map": true, "selftest cell": true, "pinned cell": true}`; run-3 receipt below. |
| F6 INFO | Stem correction: the seat prompt and the claims first draft name `corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md`; the FROZEN counter pins `2026-10-28-r50-avm-le-squashfs-core` (`c1-counter.py` `ENTRY`/`STEM`), corrected in-lane by `6f4aba63`. Any draft using the 2026-10-29 name fails `entry_present`. C1 needs NO SKILL.md edit (the C1 counter reads no SKILL.md — confirmed). LOG.md is read by nothing — one or two entries are both safe. | `grep ENTRY/STEM c1-counter.py:364-370`; `git show 6f4aba63 --stat`; run-3 binding check `entry_present: true`. |
| F7 INFO | Safe landing order validated end-to-end: C3 freeze (amended path + instrument + registry row + C3 section BEFORE the corrections heading) → C3 after-run (block 22) → C1 single commit (receipts + entry + PROVINCE/README/SOURCES/SCORECARD-140) → C2 consistency at tip. Simulated as one commit at tip `da472fa0…` (plus the F2/F3 fixes): `freeze_check null; score mismatches {}; battery mutation_count=52 failing=[]; c1 bindings all true` (province_core_section/row, frontier_note, entry_present, sourced S243-S245+S249, coverage_map_row); drafted registry row passes all five B9 shape checks. | `python3 -I -B $S/validate_landing.py` run 3, receipt `ConnCrossClaim/receipts/landing-validation.txt`, stdout sha256 `01c28a30f350cfa399ea3d9e278ddff8eccdae06af913e877de929967ce4aafd`, driver exit 0, 2026-10-29T20:58:06Z. |

## Riskiest coupling + mitigation (one line)

F1 — the v5 instrument path: both frozen counters walk `435d41fd..REV` and treat ANY post-freeze
add under `tools/round-50/` as drift (a later restore does not un-block), so C1 could never exit
0 once C3 freezes at the claim's literal path; mitigation: amend the C3 claim pre-freeze to
`tools/round-50-c3/sqfs-triage-v5.py` and keep the registry row inside the markers (measured
clean on all three fixture branches).

## Integration status (measured during this seat's run)

The L1 landed the F1 mitigation mid-wave: `03f852b9` moved the C3 instrument path out of the
frozen walk (commit message cites the seat-measured `frozen_drift`), `d71829bf` added the C3
pre-freeze amendments; both commits touch only `plans/round-50-attempt2-claims.md`. Re-verified
at tip `d71829bf`: the frozen walk `435d41fd..d71829bf` over every C1 frozen path and the C2
`FROZEN` pathspecs is EMPTY; the pending uncommitted `SKILL.md` registry row for
`tools/round-50-c3/sqfs-triage-v5.py` matches the F5 shape (gate kind; `0=met / 1=not met /
2=could-not-evaluate`; entry command names the path; selftest and pinned cells present).
Remaining hazards for the landing drafts: F2 (README row inside `## Coverage map`), F3 (new
SCORECARD sections BEFORE `## Record corrections — round 50`), F4 (no `- B<n>` bullets).

## Artifacts

- `ConnCrossClaim/coupling.md` — full matrix, regions, constraints, landing order.
- `ConnCrossClaim/receipts/counter-walks.txt` — F1 demonstration (3 branches × 2 counters).
- `ConnCrossClaim/receipts/landing-validation*.txt` — F2/F3/F5/F7 (runs 1-3).
- `ConnCrossClaim/receipts/branch-d-build.txt`, `frozen-bytes.txt` — fixture landing diff; frozen counter sha256s (c1 `9820811b…`, c2 `4749bcd8…`, carriers `0d7a6336…`, gap-rule `43f7c8d7…`, plan `a6559ed2…`).
- No tools installed; no REA runs; lane read-only (all git writes in `$S/clone`, identity set in the clone only, toplevel asserted); scratch `$S` removed after copying receipts.

## Not run (out of scope / forbidden this wave)

- C1 counting command / C3 counting command (REA runs — L1 only, after the wave).
- `c1-counter.py --selftest` (not named by this seat's task; the walks above use the counters' own functions).
- B6/B7/B8 deep-review of the new SOURCES rows' quote anchors (C1 seats own the row text; B6-B8 guard only the S246-S248 correction rows, measured untouched).
