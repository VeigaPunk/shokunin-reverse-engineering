# ReviewRoutedDefects — coverage of the five routed defects

Seat KaidokuR27.ReviewRoutedDefects (reviewer), 2026-10-22. Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin, read only.
Target: corpus/lessons/round-26-verifier-spotcheck.md `## Routed defects` (:195) against freeze a4f674b3 and wave-1 items in .ufo/waves/round-27/w1-spec.json.
Method: read-only git and file reads, plus re-running the two committed counter selftests (`--selftest`, writes only under /fast/scratch). No REA run, no installs, no external source opened.

## Defect 1 — 6.7.0 installed code has no SOURCES row — addressed; landing pending

- Freeze: claims.json R27-C2 statement requires "SOURCES has a row new since the base, opened 2026-10-22, status mined, naming the installed 6.7.0 package root a1722018f28f9df2". The checker enforces it: tools/round-27/c2-xpin-check.py:55 `PKG67_MARK = "a1722018f28f9df2"`, `source_row` at :204, counted in the exit rule at :275. Red fixtures reject a base-era row, a row outside `## Gate`, and status `candidate` (c2-selftest.txt rows-fixture lines; re-run PASS 15:01:33Z, exit 0).
- Wave 1: SrcS081 drafts exactly that row (code, tier A, mined, tarball URL + installed root, family decision vs S037); BuildXpinTool must exercise the 6.7.0 package's own code.
- Missing: seats cannot edit corpus/, so SOURCES.md is untouched in wave 1. Smallest missing step: the L1 lands SrcS081's S081 row and Gate lines; the checker's source_row then reaches 1.

## Defect 2 — instrument committed with red fixtures before the data — addressed

- `git show --stat a4f674b3` (exit 0, 14:56:16Z): exactly 7 files — claims.json, both counters, both red selftests, both before receipts. Committer 2026-10-22T11:51:23-03:00 (14:51:23Z), message "round-27: freeze claims; commit both counters, red selftests and before receipts before any data".
- `git show a4f674b3:<counter> | sha256sum` equals the worktree bytes and the claims.json `instruments` pins (e0a079…, d8de66…; exit 0).
- The refusal is coded, not promised: c1-rename-identity.py:206 takes the counter's first commit time; :244-246 refuses `utc_start` before it; :256-258 refuses an envelope first committed before it. Obs: before receipt c1-at-cd32264f.txt shows 0/16, entry_ok 0, exit 1 at the base.
- Wave 1: CriticFreeze re-verifies the freeze and drafts the claim-freezes.tsv line; LessonMistake and QualityRow convert it into a lesson row and QUALITY criteria; MutC1Time attacks the time gates.
- Smallest missing step: CriticFreeze's re-run of both before commands plus the verdict line landing.

## Defect 3 — do not reuse the old C1 counter or K6 without new gates — C1 half addressed; one forgery class partly open

Checked the new counter's gates against MutC1Forgery's four forgeries (all line numbers c1-rename-identity.py):

| forgery | round-27 outcome | killing gates |
|---|---|---|
| M1 copy envelope is base, table coherent | refused | :258-260 sha equals runs.tsv; :294 own path must appear in bytes; :296 other path must not. A resynced coherent copy still dies at :294/:296 (inference from code; adjacent red cases swap-renamed-with-base, run-path, other-path-in-envelope all PASS) |
| M2 one run reused | refused | :249-250 every envelope sha256 globally distinct (`sha_count != 1`); red case reuse-one-run resyncs and still fails |
| M3 analyze/inspect swapped | refused | :271-272 `meta.command` must equal the verb (ids and table cells would also mismatch); red case swap-verbs resyncs, fails on meta.command |
| M4 pre-freeze probe as a row | partly open, see below | :244-246 and :256-258 only if the reused bytes or run were committed/labelled before the counter |

- M4 residual (inference from code + greps, exit 1 = absent): the L1 pre-freeze probe envelope (claims.json `pre_freeze_probe`, sha256 93660137…, id ev_8af5c38f…) is not committed; its first commit would be post-counter, so :256-258 cannot fire. Those bytes are a genuine ok envelope (command function, carrier tinyxxd, recomputing id, base path present), so a coherent runs.tsv/table around them passes every gate. `grep -c claims tools/round-27/c1-rename-identity.py` = 0 — the counter never reads claims.json, although claims.json is the one committed byte that names the probe's sha256 and id and could deny it.
- K6 half: calibration is not claimed (claims.json `not_claimed`), so K6 is not reused — the non-reuse requirement holds vacuously this round. The new C2 row gates are pointer-content-style and stricter than K6: `## Capabilities` membership, `## Gate` listing, status mined, new-since-base, each with a red fixture (c2-selftest rows-fixture PASS).
- Selftest evidence: committed c1-selftest.txt 22 cases 0 failures; re-run 15:01:27Z, exit 0. Wave 1 adds MutC1Forgery/MutC1Entry/MutC1Verdict/MutC1Time and ReviewC1Counter against the same gates.
- Smallest missing step: two constants and one comparison in the C1 counter refusing the probe envelope sha256 93660137… and id ev_8af5c38f… (or commit the probe envelope pre-freeze so :256-258 bites). The freeze cannot change; this is a next-round or disclosed-residual item.

## Defect 4 — record the resolved package version per call — addressed

- claims.json R27-C1 `invocation`: after each call the seat records pkg_version and pkg_json_sha256 from the installed package.json, frozen 6.5.0 / a5003023…. The runs.tsv header carries both columns (counter :74-77) and the counter refuses any other value per run (:247-249, message "not the frozen 6.5.0"). Red cases package-version and package-json-sha PASS in the receipt and in my re-run.
- Live check: sha256sum of /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json = a5003023… (exit 0, 14:56:16Z) — the frozen constant matches the installed bytes today.
- Wave 1: all eight Run* seats record both columns after every call; ReviewC2Checker re-hashes the frozen package files.
- Residual (inference): the columns are seat-recorded, not envelope-carried; a seat that ran a different pin and lied is caught only where the id recompute distinguishes pins (round-26 closure measured 3 of 24 envelopes where the two rules coincide). The defect asked for per-call recording and that is delivered; no smaller in-lane step exists without changing REA's envelope format.

## Defect 5 — 11 stale SCORECARD statements — addressed in draft; landing pending (unclaimed by design)

- claims.json `not_claimed` keeps hygiene outside the claims.
- Wave 1: HygieneA (items 1-6) and HygieneB (items 7-11) draft append-only corrections with re-run commands; ReviewHygieneTargets independently re-derives all 11 first as the L1's reference.
- Smallest missing step: the L1 lands the drafted bullets; SCORECARD.md is untouched by seats.

## Commands run (all exit 0 unless noted; UTC 2026-10-22)

- 14:56:16Z `git log -1 --format='%H %cI %s' a4f674b3…` → freeze commit, 11:51:23-03:00; `git show --stat a4f674b3…` → 7 files; sha256sum of both counters + 6.5.0 package.json → all three equal the frozen pins.
- 14:56Z `git show a4f674b3:tools/round-27/{c1-rename-identity.py,c2-xpin-check.py} | sha256sum` → equal to pins.
- 14:58Z greps: gate lines 206/244-260/271/294-297 in c1; PKG67_MARK/source_row/capability_row in c2; "Routed defects" at lesson :195. `grep -c claims` on c1 = 0; probe sha/id absent (exit 1, expected absence).
- 15:01:27-33Z `python3 -I -B tools/round-27/c1-rename-identity.py --selftest` → cases=22 failures=0, exit 0; `…/c2-xpin-check.py --selftest` → cases=6 failures=0, exit 0.

## Residual risk and verification gaps

1. M4-shape probe reuse as detailed in defect 3 — the only round-26 forgery class not fully closed; harm is provenance (a row claims.json forbids), not a false verdict.
2. Gate :256-258 (envelope committed before the counter) has no red fixture: no selftest case commits an envelope early; the green build commits the counter (11:00Z) before data (12:00Z). One red case would close it. Also the gate is strict `<`, so a same-commit envelope would pass — unreachable post-freeze, but wave-1 MutC1Forgery's list already includes that mutant.
3. No committed-bytes counter can expose a wholly fabricated but coherent envelope set; the gates force identity, distinctness, command, path, package and times to cohere, which is the reachable maximum. MutC1Time's inherent-limit item says this plainly.
4. I ran no counter against real round-27 data (none exists yet); counter behavior evidence is the committed receipts, my re-runs, and code reading. ReviewC1Counter is the wave-1 seat that re-checks clause by clause.

Artifacts: this report (lane path above, per assignment) and a copy at /fast/scratch/hyaku/kaidoku-r27/seats/ReviewRoutedDefects/report.md (sha256 listed in the seat report). Tools installed or updated: none.
