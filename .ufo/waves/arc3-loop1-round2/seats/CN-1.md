# SEAT CN-1 | CHAIN cross | ROLE connector — cross-chain consistency sweep

Wave arc3-loop1-round2 · 2026-10-19 · repo HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`
(immobile; seats do not commit) · **Status: COMPLETE.** All three shared
instruments re-derived independently before any seat artifact was read; both
authorized real targets (EX-16's census, EX-31's custody-pair gate) caught by
poll and verified on the landed bytes; the records-commit pre-flight with all
three chains' drafted sections passes on both instruments.

Task (frozen seat line): the three chains' instrument readings must not
contradict — (i) census PASS baseline identical across chains, (ii) custody pair
digests match the 5 paths, (iii) command A readings consistent — reconcile or
flag at `claims/cross/consistency.md`.

Deliverable: `.ufo/waves/arc3-loop1-round2/claims/cross/consistency.md`
(task-named path; tool-run receipt copies under `claims/cross/CN-1/`).

## 1. Work performed (evidence pointers)

**Baseline (all four shared readings re-derived by CN-1 before reading any
round-2 seat artifact; first capture 12:00:06Z):**

- HEAD pinned `14b1682b…` (`git rev-parse HEAD`); worktree == `git show HEAD:`
  blob for all 8 measured files (`claims/cross/CN-1/baseline-pins.txt`).
- **command A** (recipe `SCORECARD.md:92-124`, `REV=14b1682…`) → 82/82 files,
  13/13 rules, 10.0/10.0 (`baseline/commandA-t0.txt`).
- **census** copy of `6f1d19ff…` → `PASS (0/0/0/0)` exit 0; counts 162/6 ·
  1417/9 · 371/2; `current_ok` blocks 5 (`baseline/census-t0.json`).
- **probe** copies of `e2665074…`/`738b3a56…` → selftest 13/13 CLEAN exit 0;
  `--rev HEAD` reported/`--strict` findings=0 exit 0.
- **custody 5-path** → 5/5, byte-identical to every round-1 capture
  (`receipts/custody-v2-cn1-t0.txt`, `baseline.md` §5).

**Cross-chain verification work:**

- All 5 custody digests matched by 6 independent chain captures (CU-1 3-engine,
  VZ-4, RV-12, EX-33, EX-31, CN-1) — inode/ctime/mtime_epoch per path also equal.
- Census landed revisions measured live: `82fb807e…` (12:06:50), `df9ffdf9…`
  (12:11:50), `a4c16763…` (12:15:39) — full injection battery on each (§3).
- C1's rule text verified byte-exact, **both generations** (v1 superseded, v2
  current): v2 payload `6cc388cb…` (1,071 B) and whole-file `a8170b96…` (387 L)
  reproduced from scratch application; command A 14/14; census-neutral; probe
  clean with SHONEN unrefreshed and refreshed; exact SHONEN end for v2 = 254.
- Records-commit pre-flight: three chains' literal sections (84+86+106 = 279 L)
  scanned with the census's own token vocabulary (0 hits) and run through the
  landed census (PASS 0/0/0/0) and the probe in a git simulation (findings=0).
- Custody-pair tool verified at its settled revision `112d01dc…`: selftest 15/15
  CLEAN; capture 5/5 exit 0; `verify --live` MATCH 5/5 on both my receipt and
  EX-31's pre receipt; same-content-rewrite attacks caught (`REWRITE-DRIFT`,
  exit 11); v1 round-1 receipt → `SHA256-CONTRACT 5/5` + 5 `LABEL-DEFECT` lines,
  exit 12 (as declared).

## 2. Proposed changes

**None.** CN-1 is a connector seat: no patch text is proposed and no repo file
was written outside `claims/cross/consistency.md` (plus the seat-scoped copy and
receipts under `claims/cross/CN-1/`). All findings are flags for the parent's
integration and for the chains' records (consistency.md §4, F1-F8).

## 3. Before → after measurement (the cross-chain claim)

Claim: the three chains' readings do not contradict (census PASS baseline,
custody digests, command A).

| Reading | Before (12:00Z, HEAD) | After (landed targets, 12:1xZ) | Verdict |
|---|---|---|---|
| census, healthy root | PASS 0/0/0/0 exit 0, counts 162/6 · 1417/9 · 371/2, instrument `6f1d19ff…` | PASS 0/0/0/0, **same counts**, on `82fb807e…`, `df9ffdf9…`, `a4c16763…` | **consistent — with the revision-stamp caveat (F1)** |
| census, H1 injection (SKILL.md absent) | silent PASS exit 0 (the round-1 hole) | FAIL exit 1, `UNREADABLE: ['SKILL.md: FileNotFoundError']`, `['UNREADABLE']` | **closed** |
| census, H3 injection (needles neutered) | silent PASS exit 0, `G2 … ok` | FAIL exit 1, `['BLIND-INSTRUMENT']` | **closed** |
| custody 5/5 | round-1 digests | identical at every chain capture (6 methods/sets) | **consistent** |
| custody rewrite detection | sha256-only: silent (round-1 attack 3) | `REWRITE-DRIFT moved=ctime_ns` exit 11 (same bytes, same inode, mtime restored) | **closed** |
| command A, C1 slice | 13/13, 82/82, 10.0/10.0 | 14/14, 82/82, 10.0/10.0 on EX-01's real payload | **consistent (see F2 for the one failure form)** |
| command A, C2/C3 slices | 13/13 | 13/13 (their edit surfaces are outside recipe A's reads) | **consistent** |

Reproduction (all read-only; scratch `/dev/shm/cn1r2`):

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 /dev/shm/cn1r2/gates/c1-census-v10.py --root .            # baseline instrument
python3 .ufo/gates/c1-census-v10.py --root .                      # landed instrument
python3 /dev/shm/cn1r2/sim-h1h3.py .ufo/gates/c1-census-v10.py /dev/shm/cn1r2/cases  # projected v11
python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm/cs
python3 .ufo/gates/custody-pair/custody-pair.py verify <receipt> --live
```

## 4. Attacks / refutations attempted, with verdicts

| # | Attack | Verdict |
|---|---|---|
| A1 | H1 reproduce on the **baseline** instrument (absent CURRENT-only file reads silent PASS) | **CONFIRMED** (my own run, not a citation) — the claim's before-state |
| A2 | H3 reproduce on the baseline (blind → PASS, `G2 ok`) | **CONFIRMED** |
| A3 | H1/H3 on the **landed** bytes | **REFUTED (closed)**: both read declared FAIL exit 1 |
| A4 | Does the landed floor hold on a *non-empty but unreadable* tree (truncated / directory)? | **CONFIRMED closed** by the landed revision: FAIL `['UNREADABLE']` — the intermediate revision did not cover this |
| A5 | Is the landed census scope-creeping under cover of the fail-closures? (scope-diff, both revisions) | **REFUTED**: rows 20/20, 0 added/removed/changed, `CREEP FLAGS: []` |
| A6 | C1's rule #14: is the whole-file identity claim honest after an independent apply? | **CONFIRMED honest**, both generations (v1 `19057c13…`, v2 `a8170b96…`); the failure form measured: incident-only text = 13/14, depth 9.29 |
| A7 | Does C1's append stale the probe needle (r10-class coupling)? | **REFUTED for the append shape** (findings=0, both SHONEN states); **teeth proven** by a 12-line insert before rule #13 → `citation_dead entry=shonen-skill-range` exit 1 |
| A8 | C3's tool: same-content rewrite with same inode + restored mtime (the sha-only blind spot) | **CONFIRMED caught** — `moved=ctime_ns`, exit 11 |
| A9 | C3's tool: does it reproduce the 5 real digests, and does a v1 receipt still verify? | **CONFIRMED** — 5/5 live; v1 → `SHA256-CONTRACT 5/5` + declared LABEL-DEFECT, exit 12 |
| A10 | C2's claim wording: "every round-1 silent-PASS injection" | **REFUTED as universal** — H2 (fabricated pin + inline marker → PASS exit 0) and H5 (gate-free statement at EOF → PASS exit 0) still silent on the landed census; the landed header names H2/t5/H4 as open, so the records must not inherit the universal form (F8) |
| A11 | Do the records drafts land clean on both instruments (with C1's rule + SHONEN refresh)? | **CONFIRMED clean**: census PASS 0/0/0/0 (SCORECARD 1417→1696), probe findings=0 strict + default |
| A12 | Transient mid-edit states of the two real targets (custody tool `KeyError: 'sha_agree'`, selftest DIRTY 6/15 at `b10ad1c8`; census `9373964c` TypeError) | **recorded, not defects** — both tools settled clean (`112d01dc`, `a4c16763`); every receipt is stamped with the bytes actually run |

## 5. Blockers

None. Two items are structurally parent-side and are named in consistency.md §5:
the landed SKILL.md/LOG/SCORECARD records (patch-text-only this round), and the
final custody capture at close. Residual risk carried to the parent: **F1** — the
C2 drafts pin `df9ffdf9…` (601 L) while the worktree census is `a4c16763…`
(603 L); land one revision and re-derive that revision's identity in the records.
