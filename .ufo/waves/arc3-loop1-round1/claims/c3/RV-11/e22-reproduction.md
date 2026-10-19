# RV-11 — E22 census cross-check, independent reproduction (chain c3, reviewer)

Measured 2026-10-19 at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(work tree clean for all scoped files: `PROVINCE.md`/`SKILL.md`/`SCORECARD.md` and
`.ufo/gates/c1-census-v10.py` byte-identical to their HEAD blobs).

Instrument identity:
- HEAD instrument `.ufo/gates/c1-census-v10.py`: blob `1091d95`, 433 lines,
  sha256 `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`.
- v10 as created at `265e1aa`: blob `58f23bd`, sha256
  `fab61b07a561f66683178db961aca369668532dceef281c59aa5d37b9a5ba333`.
- v10 after the round-8 re-key (`6bc4c29`): blob `1091d95` = HEAD blob.
- v9 (the instrument that produced the E22 finding), recovered byte-exact from the
  fenced block `.ufo/waves/arc2-loop1-round2/E22.md:264-692`:
  429 lines, sha256 `213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c`
  — matches the digest its own report claims (`E22.md:698`).
  Recovery: `sed -n '264,692p' .ufo/waves/arc2-loop1-round2/E22.md > c1-census-v9-recovered.py`.

## 1. Commands and readings

Trees were exported read-only with `git show <rev>:<file>` into this seat's scratch
(`scratch/tree-<rev>/`); nothing in the repo was modified.

```
$ python3 scratch/c1-census-v9-recovered.py --root scratch/tree-b21c0da --quiet
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)            exit=0
$ python3 scratch/c1-census-v9-recovered.py --root scratch/tree-679af5d --quiet
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)            exit=1
  UNDECLARED: SCORECARD.md block 731-737 ; SCORECARD.md block 747-766
$ python3 scratch/c1-census-v9-recovered.py --root . --quiet        # HEAD tree
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)            exit=1
  SCOPE-ERRORS: ["SCORECARD.md:635 marker '2026-10-18' absent from ''"]

$ python3 scratch/c1-census-v10-at-265e1aa.py --root scratch/tree-265e1aa --quiet
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)            exit=0
$ python3 scratch/c1-census-v10-at-6bc4c29.py --root scratch/tree-6bc4c29 --quiet
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)            exit=0
$ python3 .ufo/gates/c1-census-v10.py --root . --quiet              # HEAD
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)            exit=0
```

Card sizes (`git show <rev>:SCORECARD.md | wc -l`): `b21c0da` 701, `679af5d` 766,
`fd30b9c` 766, `158a966` 854, `1692acb` 854, `265e1aa` 854, `6bc4c29` 1158,
HEAD 1336.

Full instrument x tree matrix (v9 / v10-at-HEAD-bounds):

| rev | card | v9 | v10 (HEAD bounds) |
|---|---|---|---|
| b21c0da | 701 | PASS 0/0/0/0 | FAIL 0/0/0/0 (3 scope errors: markers 636/704/769 off) |
| 679af5d | 766 | **FAIL undeclared=2** | FAIL 0/0/0/0 (same 3 scope errors) |
| fd30b9c | 766 | FAIL undeclared=2 | FAIL 0/0/0/0 |
| 158a966 | 854 | FAIL undeclared=2 | FAIL 0/0/0/0 |
| 1692acb | 854 | FAIL undeclared=2 | FAIL 0/0/0/0 |
| 265e1aa | 854 | FAIL undeclared=2 | FAIL 0/0/0/0 |
| HEAD | 1336 | FAIL undeclared=2 (+1 scope error) | **PASS 0/0/0/0** |

The v10-off-tree FAILs are the fixed-bound design working as documented: bounds are
calibrated to the tree the instrument ships with, and an off-calibration tree is
reported, never laundered. Matched pairs (instrument at rev x tree at rev) are all
PASS with exit 0.

## 2. Claim-by-claim cross-check against SCORECARD

| # | SCORECARD claim | Reading | Verdict |
|---|---|---|---|
| 1 | `:851` "FAIL undeclared=2 at 766-line HEAD" | v9@679af5d (766 lines) = FAIL undeclared=2, exit 1; UNDECLARED blocks 731-737, 747-766 | REPRODUCED |
| 2 | `:851` "PASS at 701-line `b21c0da`" | v9@b21c0da = PASS 0/0/0/0, exit 0 | REPRODUCED |
| 3 | `:908` "v10 PASS 0/0/0/0 at the work tree" | v10@265e1aa x tree-265e1aa = PASS, exit 0 | REPRODUCED |
| 4 | round-8 re-key (`6bc4c29`, "census SCOPE re-key") | `git show 6bc4c29 -- .ufo/gates/c1-census-v10.py` = exactly 3 DATED rows shifted +1 (635→636, 702→703, 768→769; ends 701→702, 767→768, 854→855); v10@6bc4c29 x tree-6bc4c29 = PASS, exit 0 | REPRODUCED |
| 5 | `:908` "(undeclared=2, **unreproducible at HEAD**)" | v9@HEAD = FAIL undeclared=2, exit 1 — the reading **is** mechanically reproducible at HEAD. What is not reproducible at HEAD is the 701-line PASS (v9@HEAD ≠ PASS). | DISCREPANCY (wording) |

Claim 5 detail: the frozen claims' own "before" framing (`FAIL undeclared=2 … →
PASS 0/0/0/0`) also reads as if HEAD starts red; measured HEAD reality with the
shipped instrument is PASS 0/0/0/0 (before) — so the claim's before→after is
PASS→PASS, and the discriminating content is the disposition record, not a verdict
flip. (EX-26 §3 flags the same framing; this seat's independent matrix confirms it.)

## 3. Attacks / refutations attempted (this seat)

| # | attack | result |
|---|---|---|
| A1 | gate-free version append beyond the declared bound (`"The build shipped 6.7.0 last week."` at SCORECARD EOF, scratch copy) | PASS, exit 0 — **silent skip confirmed**: a version statement carrying no `REA_GATE` token is invisible to the census. Consistent with the docstring's definition of "locus", but stronger than the prose "file growth can never silently shrink the census". Latent at HEAD (tail 856-1336 holds 0 tokens of any kind — verified independently by raw grep for `6.x.y`, `rea-agents@`, and path:line pointers). |
| A2 | gated version append beyond the declared bound (`"kimi pins 6.7.0 here."`) | FAIL undeclared=1, exit 1 — growth detection works when a gate token is present. |
| A3 | anchor failure (`HOME=/nonexistent-rv11`) | `ANCHOR-FAIL: {'devin': None, 'omp': None, 'kimi': None}`, **exit 2** — the declared could-not-evaluate class fires. |
| A4 | simulated live anchors (`HOME=<scratch>/fakehome`, all three configs pinning `rea-agents@6.4.0`) | re-anchors to `{'devin':'6.4.0','omp':'6.4.0','kimi':'6.4.0'}`, FAIL stale=5 — G5 (live anchors re-derived, nothing baked in) demonstrated; no custody path was read or written for content. |
| A5 | **absent scoped file** (`SKILL.md` removed from a scratch tree) | **PASS, exit 0** — silent shrink: `SKILL.md lines=0 loci=0`, no scope error, because both SKILL.md rows are CURRENT (`ml=None`) so `assert_markers` has nothing to check. SCORECARD.md absent → FAIL (exit 1) and PROVINCE.md absent → FAIL (exit 1), since their rows are DATED and the marker assertion fires. The hole is specific to files whose declared rows are all CURRENT. Proposed fix: `proposed-missing-file-guard.patch.md`. |
| A6 | 5-way capture agreement (my run vs EX-26, EX-29, SC-6, EX-30) | all byte-identical: sha256 `3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418` |
| A7 | determinism | my run repeated byte-identical (rerun via `--quiet` and `--json` paths too, same verdict) |

## 4. Scope-coverage sweep (independent of the instrument)

Raw scan of every line of the three scoped files for `(?<![\d.])6\.\d+\.\d+`,
`rea-agents@\d+\.\d+\.\d+`, and `((~|/)[\w./+-]+\.(json|toml|ya?ml)):\d+`, flagged
against the declared SCOPE ranges **without** the REA_GATE filter (i.e. stricter
than the instrument): zero hits outside declared ranges. Undeclared extents at HEAD:
PROVINCE 31 lines (132-162), SKILL 351 lines (21-371), SCORECARD 481 lines
(856-1336) — none carries a token of the three classes.

## 5. Artifact index (this seat dir)

- `census-head.out` — before-state, full output, exit 0 (`3b677b8e…`)
- `scratch/c1-census-v9-recovered.py` — recovered v9 (`213fe679…`)
- `scratch/v9-at-b21c0da.txt`, `scratch/v9-at-679af5d.txt`, `scratch/v9-at-HEAD-full.txt`
- `scratch/matched-*.out` — matched-pair runs (265e1aa, 6bc4c29, HEAD)
- `scratch/atk-*.out` — attack outputs A1-A5
- `scratch/tree-*/` — read-only `git show` exports used as `--root`
- `poll-log.txt` — EX-28 watch (census sha256 every 60 s)
