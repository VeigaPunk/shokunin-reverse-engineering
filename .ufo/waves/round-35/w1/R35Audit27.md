# R35Audit27 — S113 locale-source reopen

## Scope and behavior
Read-only review of S113, identified by the round-35 quarantine verdict as the round-1 row for `https://developer.android.com/tools/adb?hl=en`. The verdict records a 2026-10-25 live fetch (HTTP 200, 368,063 bytes), an alternate-link `hreflang` matrix with 17 locales plus `x-default`, and exactly one `tools/adb?hl=ja` alternate link. It judges the previously unreachable row **verifiable-now**, not fabricated, while explicitly noting it is not adopted (no admitted entry cites it).

Independent repo inspection confirmed the quarantine entry and source URL. `corpus/SOURCES.md` currently has 208 lines and no S113 row; the only evident staging reference is round-34 r34b `assimilation/staged-ids`. This review did not locate S113's original full source-row text/teach quote or its capture, so the artifact-level observation in the quarantine verdict is not independently reproduced here. The locale matrix/link count supports a locale-alternate-link observation, but without the original `teaches`/`anchor` text this review cannot independently test the row's exact quote/anchor or assert broader ADB semantics. No adoption recommended from this evidence alone; frozen C1/C2 scope remains untouched.

## Commands and observed outputs
- Read `plans/round-35-claims.md` and `.ufo/waves/round-35/claims-canonical.json`: C1 is `.jsc -> source mapping` via S125/S129; C2 closes r34 D-1..D-4. Neither concerns S113.
- `grep` in lane for `S113`: located `.ufo/waves/round-34/r34b/assimilation/staged-ids` line 8 and `.ufo/waves/round-35/assimilation/quarantine-verdicts.md` line 18.
- Read quarantine verdicts: exact S113 verdict and HTTP/locale evidence as summarized above.
- `grep` lane `corpus/SOURCES.md` for `S113`: no matches.
- `grep` lane corpus for `adb|ADB|Android Debug Bridge`: found README coverage references to `2026-10-13-r4u-06-adb-surface`, including its stated device-free 2/24 verb scope; no S113 citation was found in the reported matches.
- `git log -S 'S113' --oneline --all`: showed only staging/quarantine-related history (round-34/35) plus unrelated matches; no original S113 source row surfaced. `git log -S 'developer.android.com/tools/adb' --oneline --all`: no output. `git log --oneline --all -- corpus/SOURCES.md`: inspected history listing; no source-row recovery performed.

## Gates, touched surfaces, and limits
- Gates: no counter, selftest, claim gate, or frozen predicate run or changed. C1/C2 remain strictly out of scope.
- Touched surface: this report only. Lane files, source trees, VCS/index/jj state, sibling/fleet repos, and `/home/vgpnk/Projects/shokuknow` were not written. No live fetch was performed in this audit; HTTP/HTML details above are sourced from the already-recorded quarantine verdict, not newly observed execution.
- Out of scope: adoption or editing of SOURCES/corpus, claims, counters, plans, scorecard/log, and any production changes.
- Limits: original S113 row text, exact quoted passage and retained capture were not recovered. The report therefore records a scoped corroboration lead, not independent validation of the precise source quotation.

Report: `.ufo/waves/round-35/w1/R35Audit27.md`