# CB7 — PROVINCE-check 2: PROVINCE untouched by all drafts

## CLAIM
At snapshot HEAD `a280e07`, PROVINCE.md is byte-identical to its committed blob, and no round-9 draft present in the wave directory targets it for edit.

## METHOD
Read-only. Ran `git diff --quiet HEAD -- PROVINCE.md`; `git status --porcelain=v1 -- PROVINCE.md`; `git diff --cached --quiet -- PROVINCE.md`; `git hash-object PROVINCE.md` vs `git rev-parse HEAD:PROVINCE.md`; `sha256sum` of worktree vs `git show HEAD:PROVINCE.md`; `git diff HEAD --numstat -- PROVINCE.md`; `git diff --quiet HEAD --` (whole tracked tree). Scanned all 67 `.ufo/waves/luna-round-9/*.md` files (36 mention PROVINCE) for write/patch patterns (`> PROVINCE`, `sed -i`, patch headers, append/edit verbs) and classified every `PROVINCE.md` mention line-by-line. Read `PROVINCE.md:100-116`.

## FINDINGS
- Worktree = HEAD: blob `8a1cec88b50f0e9aa928b0c042354a017217ad47` from both `git hash-object` and `git rev-parse HEAD:PROVINCE.md`; sha256 `fe7f3f61c6be…3b37c1c` on both sides; size 18590 both; diff, numstat, status, and cached-diff all empty/exit 0; entire tracked tree `git diff --quiet HEAD --` exit 0.
- No draft names PROVINCE.md as a write target. Explicit guards: `P0.md:14`, `P1.md:13`, `D2.md:2`, `D4.md:8` ("Corpus and PROVINCE remain unchanged"), `R4.md:8` ("without changing PROVINCE.md"), `P2.md:14` ("Do not edit `PROVINCE.md`"), `E2.md:12`, `G4.md:8` ("keeps `PROVINCE.md` outside scope"), `R5.md:12`, `Z5.md:16`, `Y1.md:8`.
- All proposed append targets are corpus records: `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md` (A1/A2/P0), `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md` (D2/P2), `SCORECARD.md` measurement area (B2; `X4.md:2` selects SCORECARD).
- Refusal text confirmed at `PROVINCE.md:114-116` ("is it safe, trustworthy, or licensed for reuse"); `HB2.md:20` only widens the corpus append's citation anchor to `:102,:114-116` — not a PROVINCE edit.

## THREATS
Mid-wave snapshot: `HB2.md` appeared during this check, and later lane-B drafts are not covered; recheck the PROVINCE blob after integration. Only tracked state and this wave directory were scanned — drafts stored elsewhere are out of scope. PROVINCE.md mtime 2026-10-16 17:00:33 predates the wave (first file 21:44), corroborating no in-wave write. Verdict covers untouchability, not the truth of any draft's content.

## VERDICT
CLEAN — PROVINCE.md byte-identical to HEAD; no present round-9 draft edits it.
