# R29 w1 — ReviewLedger: both freeze ledgers at 18be864

Seat: KaidokuR29.ReviewLedger. Date: 2026-10-22. Lane base bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47, measured tip 18be864a528873b2b70d8c94e31f880290249e90.

## Method

Sandbox clone (bounds-compliant; no git/jj write in the lane or fleet repo):
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin <scratch>/clone` then `git -C clone checkout -q 18be864a528873b2b70d8c94e31f880290249e90` → HEAD verified `18be864a528873b2b70d8c94e31f880290249e90`. All commands below ran in the clone with the three `GIT_*` vars unset.

Gates run (both with `--disclosures`, per assignment):

1. `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <clone> --rev 18be864a... --require-clean round-24 --disclosures corpus/claim-freezes.tsv` → **exit 0**, 2026-10-22T20:24:31Z (start and end). JSON: `audited=16 clean=1 required_failed=[]`, `disclosures exact=16 of=16 mismatched=[] missing=[] stray=[]` (sha256 of output f651b24a...).
2. `python3 -I -B tools/round-29/freeze-gate.py --root <clone> --rev 18be864a... --disclosures corpus/claim-freezes-v2.tsv` → **exit 0**, 2026-10-22T20:24:31Z. JSON: `audited=19 clean=2`, `disclosures exact=19 of=19 mismatched=[] missing=[] stray=[]` (sha256 217131d5...).

Gate identities confirmed at the rev (observation): round-24 gate sha256 `8a71fe84...`, `CLAIMS = ... round-[0-9]+)/claims\.json$` (claims.json only) and `pins = frozen.get('instruments')` only; round-29 gate sha256 `25b54339...`, `claims[A-Za-z0-9_.-]*\.json` and `PIN_KEYS = ('instruments','loaded_by_counter','producers_not_counters')`. This matches every ledger row's "this gate reads only the instruments key" / "reads producers_not_counters as pins" phrasing.

Changed-row set confirmed (observation): `git diff bacbe9cc..18be864 -- corpus/claim-freezes.tsv` = rows round-26, round-27, round-28 rewritten + round-29 added (7 lines, 4+3-); rounds 14–25 byte-unchanged. v2 ledger added whole at 18be864 (20 lines); its v2-only keys vs v1 are exactly the three non-`claims.json` rows.

No tools installed (nothing needed; python3/git preexisting). No LSP server was available/used in this environment; all checks are git-object and CLI evidence, and no claim below rests on symbol-level code analysis.

## Per-row verdicts (verdict/findings vs gate; pointer prose vs repository)

Gate output quoted from the two saved JSONs (per-freeze findings, freeze commit, revised-commit lists).

| ledger row | gate (both gates agree unless noted) | prose checks vs repository | verdict |
|---|---|---|---|
| v1 `round-26` | FLAGGED `INSTRUMENT_ABSENT,INSTRUMENT_REVISED` (matches row codes); freeze c27f445e; c1-id-identity.py ABSENT + REVISED at bd0c84bc; c2-calibration.py ABSENT + REVISED at 81f63f36, `disclosed: 0` | "C1 at bd0c84bc after the C1 data at ebe2cb4a" — `git merge-base --is-ancestor ebe2cb4a bd0c84bc` = ancestor ✓; `claims.json freeze_kind` at the rev says "definitions-first ... INSTRUMENT_ABSENT by design and is disclosed as such" ✓; receipt `.ufo/waves/round-29/after/ledger-before-fix.txt` present at rev and shows the pre-fix gate: `mismatched: ["round-26","round-28"], missing: ["round-29"], exit=1` (matches M29-2 story) ✓; `corpus/lessons/round-29.md` M29-2 matches ✓ | **holds** |
| v1 `round-27` | FLAGGED `INSTRUMENT_ABSENT,INSTRUMENT_REVISED,INSTRUMENT_UNPINNED` (matches); UNPINNED recompute-ids.py; xpin-attribute.mjs ABSENT + REVISED at 97358f75; c2-xpin-check.py NOT flagged (superseded) | recompute-ids.py sha256 identical at r27 base cd32264f and 97358f75 = `89afa3756a9b...fd60208b` ("byte-identical 89afa375") ✓; receipt `recompute-pin.txt` present ✓; c2-xpin-check.py pin at freeze a4f674b3 = `d8de667ff82a...209bd3` and blob at 18be864 = `1c8259a8fe4f...36783` = `sha256_after` in `.ufo/waves/round-27/claims.json` `instrument_supersessions` (commit 7431096b, selftest-only reason) ✓; diff at 7431096b is one hunk `@@ -298,29 +298,39 @@` starting at `def selftest():` (selftest 298–347, next def 348) = selftest-only ✓; receipts `r27-c2-xpin-selftest-unpatched.txt` / `...-patched.txt` present ✓; CriticFreeze.md present ✓; 7431096b is ancestor of 18be864 ✓ | **holds** |
| v1 `round-28` | FLAGGED `INSTRUMENT_UNPINNED,INSTRUMENT_UNRESOLVED` (matches; codes sorted, base row had them unsorted — the row's own "codes re-sorted in round 29 (M29-2)" note ✓); UNRESOLVED select-heldout.py (bare); UNPINNED tools/round-28/collect-c1.py | freezes 87d3dfb6 (claims.json) / 86fa8526 (claims-c2.json) = gate ✓; data commits ca4069a4, cb8d495e verified descendants of freeze 87d3dfb6 (`git merge-base --is-ancestor`) ✓, a2673116 descendant of 86fa8526 ✓; `.ufo/waves/round-28/a2w/ExecFreezeGate.md` present ✓ | **holds** |
| v1 `round-29` (new) | FLAGGED `INSTRUMENT_UNPINNED`, exactly 4: make-carriers.py, collect-c1.py, collect-c2.py, c1-heldout-naming.py — matches the row's list and its "this gate reads only the instruments key" explanation | freeze dbd87cfa = gate ✓; data 4fcea978 descendant of dbd87cfa ✓; receipt `freeze-gates-at-dbd87cfa.txt` present ✓ (its v2-gate run flags round-29 INSTRUMENT_UNPINNED; receipt v1 run at dbd87cfa flags the same set); M29-3 in `corpus/lessons/round-29.md` matches ✓ | **holds** |
| v2 `round-26`, v2 `round-27` | same findings as v1 rows | rows carry the same pointer text as v1 (diff-verified); same repository facts | **holds** |
| v2 `round-28` | FLAGGED `INSTRUMENT_UNRESOLVED` only (producers_not_counters now read as pins → collect-c1.py pinned) — exactly what the row's "except that ..." sentence predicts | ✓ | **holds** |
| v2 `round-28/claims-c2.json` (v2-only) | CLEAN | `claims-c2.json` at 86fa8526 pins `instruments={tools/round-28/c2-filtered-flag.py}`; collect-c2.py under `producers_not_counters` (v2 gate reads it) ✓; gate CLEAN = present, pinned, unchanged since ✓; prose honestly scopes CLEAN away from M28-4 ✓; ExecFreezeGate.md receipt present ✓ | **holds** |
| v2 `round-29` | FLAGGED `INSTRUMENT_UNPINNED`, exactly 1: c1-heldout-naming.py — matches "only tools/round-28/c1-heldout-naming.py stays unpinned" | ✓ | **holds** |
| v2 `round-14/claims-review.json` (v2-only) | FLAGGED `INSTRUMENT_NONE` (matches codes) | codes match gate and the claims-review file truly names no script; but the pointer cites `.ufo/waves/round-29/after/freeze-gates-v2.txt`, which is **absent from the tree at 18be864** | **holds on verdict; pointer defect F-1** |
| v2 `round-15/claims-review.json` (v2-only) | FLAGGED `INSTRUMENT_NONE` (matches codes) | same dangling pointer | **holds on verdict; pointer defect F-1** |

## Findings by severity

**F-1 (minor, prose-vs-repository): both v2-only rows cite a receipt that does not exist in the repository at the measured revision.** Rows `round-14/claims-review.json` and `round-15/claims-review.json` in `corpus/claim-freezes-v2.tsv` (committed at 18be864) end with "first audited in round 29 (.ufo/waves/round-29/after/freeze-gates-v2.txt)".
Evidence (2026-10-22T20:29:31Z): `git ls-tree --name-only 18be864a... -- .ufo/waves/round-29/after/` → only `freeze-gates-at-dbd87cfa.txt`, `ledger-before-fix.txt`, `prefile-check-red-r28.txt`, `r27-c2-xpin-selftest-patched.txt` (rc=0); `git log --all --format=%H -- .ufo/waves/round-29/after/freeze-gates-v2.txt | wc -l` → `0` (never committed on any ref); lane worktree `git status --porcelain` → `?? .ufo/waves/round-29/after/freeze-gates-v2.txt` (untracked). Mitigation (observation): the untracked file's content is the genuine receipt of exactly the two assigned gate runs at 18be864 — same commands, `exit=0` both, summaries identical to my independent reruns (v1: NONE 3 / UNRESOLVED 9 / ABSENT 12 / UNPINNED 10 / REVISED 15 / PIN_MISMATCH 0) — so the prose is truthful but not repository-backed at the rev; the gate's own Limits disclaim pointer completeness ("the ledger is author-written and checked for agreement, not for completeness of its prose pointer"). Two committed rows point at bytes that live only in a dirty worktree — the same filing-while-tree-is-dirty class as M29-1. Fix: commit the receipt (it is the gate run the ledger discloses with).
Sub-observation (cosmetic): inside that receipt the round-24 gate is invoked without `--require-clean round-24` (the frozen R24-C2 counting command includes it). Exit is unaffected here (round-24 is CLEAN, `required_failed=[]` in my run with the flag), but the receipt is not byte-for-byte the frozen counting command.

No other defect found in the assigned scope. Both ledgers disclose **exactly** (v1 16/16, v2 19/19, no mismatch/missing/stray), and every checked prose assertion in the seven assigned rows reproduced from Git objects.

## Residual risk and verification gaps

- The 13 unchanged rows (round-14…round-25) were not re-verified line-by-line — `--disclosures` checks verdict+code-set agreement only, never pointer prose; out of assigned scope.
- Commit timestamps and authorship unauthenticated (both gates' stated limit); "first data commit" ordering for round-28 rests on ancestry, which I did check, plus ledger prose.
- The untracked receipt could change before it is committed; I hashed the bytes I read (`5363eb34...`). Whether it lands in a later commit is unknown from this seat.
- round-27 row's "the round-27 C2 measurement is not re-scored" is a scope statement, not falsifiable from the ledger; the supersession reason repeats it (inference: consistent, unverified deeper).
- Historical claims inside rows about earlier rounds' seat outputs (e.g., "freeze-gate.py at 9db24c9e (seat ExecFreezeGate) flags ...") are corroborated by present receipts, not re-derived from that seat's session.

## Artifacts (scratch, /fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewLedger/)

- `clone/` — sandbox clone checked out at 18be864a528873b2b70d8c94e31f880290249e90
- `gate-v1.out.json` — round-24 gate output, sha256 `f651b24a9a981c8e53cc444db99a47da8be51246644dac0802aaf94497330855`
- `gate-v2.out.json` — round-29 gate output, sha256 `217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c`
- `v1-ledger.diff` — base..tip diff of corpus/claim-freezes.tsv, sha256 `67fb2fcc0d49ae9829fa80914b3cacf77e3d108f1fe8bc39996554ae04f3349f`
- `tmp/` — empty scratch dir

Installs: none.

Report: .ufo/waves/round-29/w1/ReviewLedger.md
