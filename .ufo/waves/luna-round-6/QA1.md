## CLAIM

Evidence-discipline audit of a deterministic 8-report sample of the 52 lane-A seat reports: every claim pointer-backed, lapses listed.

## METHOD

Read-only. Lane-A set = 52 reports written 18:16:42–18:29:27 (later files EX7/XA/BB1/SB2/CC1/PB0 excluded as lane-B-wave writes, mtime ≥18:53; XA's "53 top-level reports" at 18:58 corroborates the 52+EX7 count). Sampled positions 1, 8, 15, 22, 29, 36, 43, 50 of the sorted 52: CA1, CA8, EX4, PR1, RE2, RV5, SC4, SH1. For each claim: resolved path:line and receipt pointers, re-ran cited read-only commands (`sha256sum`, CA8's `sed|sha256sum` pipeline, `git status --short -uall`, `git ls-files`, `file`), compared claims against receipts, file mtimes, and cited SHONEN/PROTOCOL/SCORECARD text. No probes, no MCP, no config edits.

## FINDINGS

- CA1 — **LAPSE**: "Glob … showed RV6 and RV8 but no RV1–RV5/RV7" and "repository exposes only RV6/RV8 reports" do not reproduce: `RV5.md` exists, mtime 18:18:54, 51s before CA1.md (18:19:45); no snapshot anchor given. Its other pointers (RV6/RV8/CA8/leg-1 ranges) resolve.
- CA8 — clean: PS4:8-11 and leg-1:3-11 say what is claimed; cited recompute pipeline returns `3eb8e06c…`; untracked/ls-files claims reproduce; "only leg-1 receipt" was true at 18:17:54 (leg-2 lands 18:19:00).
- EX4 — minor: pointers resolve (libsignal corpus :9 digest; leg-4.md 43 lines with `ev_0618e7…`, 24,944,200 B; luna-round-2/A6.md:8 = 207). "round-6 absent at dispatch" is unpointed testimony (corroborated by RV6/RV8).
- PR1 — clean: SC2/PS4/EX1/RV6/SHONEN:5-12/leg-1:3-11 all resolve; TBDs stated honestly.
- RE2 — minor: presence-check output quoted, exact `test -f` command not shown; result consistent with receipt mtimes.
- RV5 — clean: `sha256sum receipts/leg-1.md` = `24bfd90f…` reproduced; MANIFEST.txt matches; L1 digest recompute verified.
- SC4 — clean, live-verified: index.db exists, 16,384 B, same SQLite signature and sha256 `3701a7e3…`.
- SH1 — minor: SHONEN:9-10, lesson :87-109, PROTOCOL:63-68/434-435 resolve and match; `../PROTOCOL.md` base ambiguous (resolves only from repo root).

Substantive lapse 1/8 (CA1); minor pointer-hygiene 3/8 (EX4, RE2, SH1); clean 4/8.

## THREATS

Repo is a later snapshot; several cited absences were true at their write times (mtimes bear this out) yet unreproducible now. I verified pointer resolution and cited-command reproduction, not full probe re-execution.

## VERDICT

FINDING: 1/8 sampled lane-A reports contains a claim falsified by repo state; 3/8 have minor pointer gaps; 4/8 clean.
