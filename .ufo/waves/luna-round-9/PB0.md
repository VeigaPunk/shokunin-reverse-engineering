# PB0 — lane-B plan: verification brief on lane A's four item outputs

## CLAIM
Lane A's four round-9 item outputs verified at HEAD `a280e07`: item-1 pointer draft, item-2 instrument-limit note, item-3 `/tmp` audit + hygiene proposal, item-4 jq-shadow qualification draft. Invariants hold; integration requires the scoping conditions below.

## METHOD
Read the quartets A1–A4, B1–B4, C1–C4, D1–D4, plus E1/E2/H/R5/X4/Z1/Z4 and primary sources (r4-16, r12-01, r2-jq-shadow, `PROVINCE.md`, `SCORECARD.md`, round-4/5 reports), and lane-B peers landing during my run (CB4/CB6/CB7/HB2/VB4/TB1). Independently replayed Command A (`SCORECARD.md:93-123`, `REV=a280e07`) and git guards. Static only; no probes, network, or `/tmp` access; only this file written.

## FINDINGS
- **Invariants:** my Command A → `79/79`, `9/9`, `10.0/10.0`; `git diff --quiet HEAD --` exit 0; no tracked deletions; `PROVINCE.md` byte-identical (sha256 `fe7f3f61…`, blob `8a1cec88…`). T2 baselines re-derived (r4-16 `622e3661…`, jq entry `541f3499…`). No append has landed.
- **Item 1:** stale two-site text confirmed (`r4-16:751-752`); four-site correction and attribution confirmed (`r12-01:99-104,:115-118`). A2/Z1 draft pointer resolves. Conditions: pointer-only (CB4/H4 duplication risk), do not claim r12-01 supersedes r4-16 (A3/H), EOF `:925` open for append (Y3).
- **Item 2:** both limits independently sourced (`luna-round-4/kaidoku.md:43-46`; `luna-round-5/kaidoku.md:50-56,:63-67`; `SCORECARD.md:407-410,:458-460`); home → SCORECARD (X4). Conditions: B3 guard (`ADJUDICATED` not `PASS`, retest trigger) and a mechanics ruling on B2's mid-file "insertion" vs append (R5/CB4).
- **Item 3:** C1's scoped audit stands (C4/H/R5 concur). Caveats: retained historical `verify:` recipes consume `/tmp` artifacts (Q3 `r3-renderer-asar.md:11,19`; R5 `r14-01:11-17,45-48`) — outside C1's scope; L7-01 npm cache unverified. C2 hygiene is operator-owned; no deletions in any draft (CB6 sweep).
- **Item 4:** qualification draft (D2/Z4) verified; `PROVINCE.md:114-116` confirmed verbatim (HB2/mine). Open: D3 retraction-vs-qualification is a policy call; broaden loci to r2 `:12`/`:219` (D4/E1/R5/VB4); r3 bleed `:60,:136` is separate scope; stale `:107-109` citations at `SCORECARD.md:79` and `corpus/lessons/2026-10-15-round-1.md:149-153`.

## THREATS
Point-in-time snapshot (72 lane-A+lane-B `.md` files; CB4/CB6/CB7/HB2/VB4/TB1 landed 21:58–21:59). No post-landing append-only/byte-identity check exists yet. `G3.md:24`'s token-set SHA-256 is 63 hex chars (TB1) — unusable as a verbatim baseline. "7 values" not re-derived; `/tmp` state not inspected.

## VERDICT
FINDING: four item outputs verified at `a280e07` with invariants intact; integration requires item-1 pointer-only trim, item-2 guard/mechanics ruling, item-3 recipe-boundary wording, item-4 locus/policy adjudication.
