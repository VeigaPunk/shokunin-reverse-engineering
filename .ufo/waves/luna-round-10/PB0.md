## CLAIM
Independent closeout verification: re-audit lane-A sample, complete the raced D-chain, assess SHONEN + final-report assembly at live HEAD.

## METHOD
Read lane-A wave (P0, D1–D6, A4, N3, S5, K1), `SHONEN.md`, nine reports' §SHONEN; `git show/diff` on records commits `a9580eb` r2, `0772d54` r3, `cfc84c2` r4, `6e2ee8f` r7 and HEAD `c343939`; python enum scan of fleet `MANIFEST.json`; replayed command A (`SCORECARD.md:86-123`) at `c343939`/`40162fc` (offline, git objects only); siblings read-only. No probes; only this note written.

## FINDINGS
- MANIFEST: the six enum-led prose rows are exact (`MANIFEST.json:2791,2805,2819,2846,2847,2860`), but the roster totals 10 non-exact values on 9 rows, adding `improved (audit queued in round 2)` (`:1509`) and three `verified (…)` (`:1522,1535,1548`) — non-enum; fleet scan: 12 exact `improved`.
- Rewrites confirmed by numstat: r2 `a9580eb` 60+/8− (calibration row reworded), r3 55+/7− (depth row + quoted block), r4 `cfc84c2` 46+/1− (`:157`→`:160`, `SCORECARD.md:68-72`), r7 32+/1− (coverage row 72/72→78/78 at `3395b6d`). LOG.md additive in all four; HEAD `c343939` +16/+12, 0 deletions.
- Round 6 = 127 distinct seats (`reports/luna-round-6/kaidoku.md:47-52`; `BC6.md:13-25`); five short-count rounds in-report: r2 58+6 backfill, r4 58/64 second, r5 58/64 third, r6 53/64 fourth, r7 59+5.
- Command A replay: both revisions give `mapped 79/79, rules 9/9, coverage 10.0, depth 10.0, missing/dangling []`.
- SHONEN 4×`[~]` in all nine reports (r1/r2 list four; r3–r9 “`[~]` ×4 unchanged”); `SHONEN.md` names no verifier. Assembly pending: `.ufo/reports/luna-round-10/kaidoku.md` absent; fleet round-10 has 8 lanes, no kaidoku; SB5's draft supersedes S5's on two points.
- D-chain: D4 raced D1–D3, D6 raced D4. Union D1–D5 leaves five named items open — R1 R4 no-peeking + S2 pointer-style (`r1:66-69`), R2 G9 E-draft dates (`r2:63-65`), R3 misnamed report + C4 unpersisted command (`r3:64-67`); only B2's L7 hash closed (D5; my sha256 prefix `dc740c46…` matches).
- K1 read-only verified: Tameshi `verification-patterns-fleet.md:35` keeps `f(content,path,params)` as INFERENCE with U4 open; tsukuroi `PROVINCE.md:42,70-71` leaves ADJ-06 unresolved. Kaidoku counter-record: `SCORECARD.md:347-357`; `corpus/QUALITY.md:24-25` (#15 supersedes #14).

## THREATS
Command A is index arithmetic, not semantic truth. Sample, not census; the wave was live (75 files; new lane-B seats arriving). Prompt pins `6e83a20` but HEAD is `c343939` (additive) — the final report must pin the live revision. D1's “corrected to :71” conflicts with the diff (`:157`→`:160`); per-item pointers need re-check at integration.

## VERDICT
FINDING: lane-A findings confirmed with two corrections (MANIFEST 10 non-exact values/9 rows, not 6; D-chain omission list of five items); rewrites r2/r3/r4/r7 verified; SHONEN 4×`[~]` holds; final report assembly pending at live HEAD `c343939`.
