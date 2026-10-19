# RV-10 — laundering refusal re-measurement (fixtures A-F) + bound-guard probe (G1-G4b)

Seat RV-10, chain c3, wave arc3-loop1-round1, 2026-10-19. All runs are
read-only w.r.t. the repo: the census reads `$HOME` configs (live anchors
`devin 6.5.0 / omp 6.5.0 / kimi 6.7.0`) and the three scoped files from
`--root`. Every fixture root is a scratch copy under `/var/tmp/rv10/`
(`/tmp` is EDQUOT on this host: a plain `echo > /tmp/...` fails, and a python
redirect exits 120 with a 0-byte file — same standing hazard as the peers
recorded; precedent for `/var/tmp` scratch: Z1 r4).

## 1. Fixture design

Synthetic stale append (3 lines, lands at EOF of the copy):

```
## arc2-loop1-round4-fixture — laundering probe, 2026-10-19
Kimi is pinned at rea-agents@6.4.0 on this host.
```

That line is a gated locus (pin kind, client `kimi`, value `6.4.0` vs live
`6.7.0`): **stale unless a DATED bound or inline marker absorbs it**. Word
choice avoids every INLINE_MARKER token, so only scope decides.

Trees:
- `tree1` = `265e1aa` files (SCORECARD 854 L) + append → locus at `:857`
- `tree2` = HEAD files (SCORECARD 1336 L) + append → locus at `:1339`
- `tree3` = HEAD files, clean; `tree4` = `265e1aa` files, clean
- `tree5` = HEAD files + one-line insert at `:600` (inside the undeclared gap
  561-618), shifting everything below

Instrument variants (unified diffs + sha256 in `evidence/variants.diff` and
`evidence/sha256-manifest.txt`): `v10-r4.py` / `v10-HEAD.py` (landed forms,
verbatim), `open-r4.py` (last row end `854 → 10**9`), `over-r4.py`
(`854 → 900`), `open-HEAD.py` (`855 → 10**9`).

## 2. Laundering fork, re-measured (the r4 question)

| # | instrument | tree | result | evidence |
|---|---|---|---|---|
| A | landed v10@r4, fixed bound 768-854 | tree1 (locus `:857`) | **FAIL, rc 1**, `undeclared=1`; block `857-857 [scope None]`, `:857 [pin] kimi=6.4.0 -> STALE` | `evidence/fx-A.txt` |
| B | overshoot `768-900` | tree1 (locus `:857`, inside 900) | **PASS, rc 0**, `0/0/0/0`; `:857 -> historical (dated scope)` | `evidence/fx-B.txt` |
| C | open `768-10**9` | tree1 | **PASS, rc 0**, `0/0/0/0`; `:857 -> historical (dated scope)` | `evidence/fx-C.txt` |
| D | landed v10@HEAD, fixed bound 769-855 | tree2 (locus `:1339`) | **FAIL, rc 1**, `undeclared=1`; `:1339 [pin] kimi=6.4.0 -> STALE` | `evidence/fx-D.txt` |
| E | open `769-10**9` | tree2 | **PASS, rc 0**, `0/0/0/0`; `:1339 -> historical (dated scope)` | `evidence/fx-E.txt` |
| F | landed v10@HEAD | tree5 (mid-gap insert `:600`) | **FAIL, rc 1**, `undeclared=2` (`:600` planted pin; `:621` shifted capability-row locus) | `evidence/fx-F.txt` |

Verdict: **the r4 fork is unchanged and the landed side is the refusing one.**
The same stale append is visible under the landed fixed bound (A, D) and
swallowed as `historical (dated scope)` under both relaxed variants (B, C, E)
— R3 §2.7 rows 10/11 and Z1 §5.5 reproduced with the current instrument.
Mid-file inserts also fail loud (F); the undeclared gap class is not silent.

## 3. Bound-guard probe (proposal evidence)

Guard hunk (5 additive lines at the top of `assert_markers` — a pre-loop over
**all** SCOPE rows, so CURRENT rows are covered too, not only DATED):
`if lines and e > len(lines): errs.append(... "declared end %d beyond EOF" ...)`.
The first builds placed the check after the marker test (DATED rows only) and
gave the same four results; the form re-measured here is the all-rows one.

| # | instrument | tree | result | evidence |
|---|---|---|---|---|
| G1 | landed v10@HEAD + guard | tree3 (clean HEAD) | **PASS, rc 0**, scope-errors `[]` — guard is inert on the landed form | `evidence/fx-G1.txt` |
| G2b | landed v10@r4 + guard | tree4 (clean r4) | **PASS, rc 0**, scope-errors `[]` | `evidence/fx-G2b.txt` |
| G3 | guard + open `10**9` | tree3 | **FAIL, rc 1**: `SCOPE-ERRORS: ['SCORECARD.md: declared end 1000000000 beyond EOF (1336 lines) -- open/overshooting bound']` — the relaxation is caught **statically**, without needing a laundered locus | `evidence/fx-G3.txt` |
| G4b | guard + overshoot `900` | tree4 (854 L) | **FAIL, rc 1**: `declared end 900 beyond EOF (854 lines)` | `evidence/fx-G4b.txt` |

Two discarded runs, recorded for honesty: the first G2/G4 builds substituted
the wrong base (HEAD rows into an r4 tree); their outputs were discarded and
rebuilt as G2b/G4b above. A first G2 run's failure was itself correct
behaviour (HEAD rows against an 854-line file = marker scope-errors + the
guard firing).

Byte-identity cross-check: **G1's output is byte-identical to the census's own
HEAD capture** — `fx-G1.txt` sha256
`3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418` equals the
digest five independent seats captured at HEAD (EX-26, EX-29, SC-6, RV-11,
EX-30). The guard is provably inert on the landed form.

## 4. Commands (verbatim, rerunnable)

```bash
# reconstruction of v9 (byte-exact; sha256 213fe679…, 429 lines)
sed -n '264,692p' .ufo/waves/arc2-loop1-round2/E22.md > c1-census-v9.py

# the landed versions
git show 265e1aa:.ufo/gates/c1-census-v10.py > v10-r4.py   # fab61b07…
git show 6bc4c29:.ufo/gates/c1-census-v10.py > v10-r8.py   # 36e96cd5… == HEAD

# fixtures (example: A)
python3 v10-r4.py --root tree1        # rc 1, VERDICT: FAIL (undeclared=1)

# guard variant build (from v10-HEAD.py): add a pre-loop at the top of
#   assert_markers (all rows):
#     for (f, s, e, cls, ml, mr) in SCOPE:
#         lines = filelines.get(f)
#         if lines and e > len(lines):
#             errs.append("%s: declared end %d beyond EOF (%d lines) -- open/overshooting bound"
#                         % (f, e, len(lines)))
python3 v10-guard.py --root tree3     # rc 0, PASS — inert on the landed form
python3 guard-open-HEAD.py --root tree3  # rc 1, scope-error: 1000000000 beyond EOF
```
