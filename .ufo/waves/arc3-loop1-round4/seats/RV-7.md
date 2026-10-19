# RV-7 — seat report (chain c3, reviewer)

Wave `arc3-loop1-round4` · seat RV-7 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · no git mutations · all fixtures
on scratch copies (`/dev/shm/rv7`), custody paths read-only (hash/stat/`verify` only).

Task: mutation tests — each of (a)(b)(c) reverted individually on copies → the
corresponding before-behavior returns (load-bearing).

**Verdict: PASS — the three fixes are load-bearing and mutually independent. The
mutation matrix is diagonal on the LANDED revision `29bb45ae…` (28 cases), and each
mutant is additionally caught by the landed selftest's own case. The two spelling
traps I found during rehearsal (leg A2, leg B2) are both closed in the landed bytes.**

## 1. Work performed (evidence pointers)

All artifacts under `.ufo/waves/arc3-loop1-round4/claims/c3/RV-7/`:

| artifact | role |
|---|---|
| `probe.py` | revision-agnostic residual probe: legs A (sidecar on measured file), A2 (sidecar-shaped neighbour spelling), B (mkdir under a non-directory), B2 (`--out ""`), C (coverage basis), legit-write control, selftest |
| `mutant-build-r4.py` | single-fix reverter for the landed revision (variant-tolerant; reports matched-pattern count, never silently) |
| `evidence/landed-r4-29bb45ae.py` | byte copy of the landed revision (`29bb45ae…`) as probed |
| `evidence/L-landed.json` | landed-revision probe (all legs) |
| `evidence/M-MUT-{A,B,C}-*.json` + `evidence/MUT-{A,B,C}-*.py` | the three mutants built from the landed bytes and their probes |
| `evidence/G-*.json`, `DRESS2-revision.py`, `MUT-{A,B,C}.py` | rehearsal round (before the target landed) |
| `evidence/I-EX23-VARIANT.json`, `J-DRESS3.json`, `J-MUT-A3.json` | peer-candidate and neighbour-arm controls |
| `mutate.py` | difflib-opcode hunk lister/reverter |

Commands:
```
python3 claims/c3/RV-7/probe.py <tool.py> /dev/shm/rv7/scratchM <LABEL>
python3 claims/c3/RV-7/mutant-build-r4.py .ufo/gates/custody-pair/custody-pair.py /dev/shm/rv7/mutants4
```

Identity re-derived at write time (rule #14):
- landed tool `.ufo/gates/custody-pair/custody-pair.py`
  `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`, 1343 lines,
  65902 B (mtime 2026-10-19 11:09:25 −03); README
  `125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186`, 267 lines.
- base (pre-r4) revision `7cd19c3c…`, 1155 lines.
- `evidence/landed-r4-29bb45ae.py` re-hashes to `29bb45ae…` (byte copy verified).

## 2. Proposed changes

**None by this seat** (reviewer; patch text only). Two requirements the landed
bytes already satisfy, recorded because a future revision could regress them
without any selftest firing:
1. the sidecar name must be derived inside a guarded region (`--out ''` / `--out .`
   → declared USAGE 2, not `ValueError`); the landed bytes do this at the
   `try: sidecar = out.with_name(...) except ValueError:` block;
2. the coverage line's count and its `unaccounted:` list must share one basis
   (`distinct_paths()`); a count/list basis mismatch prints a self-contradictory
   line — the exact symptom EX-24 found at `03bd6242…`.

## 3. Before → after measurement (the chain's claim)

### 3.1 The residual legs, before vs landed (first-hand)

| leg | command | before (`7cd19c3c…`) | landed (`29bb45ae…`) |
|---|---|---|---|
| (a) | `capture --out vic --paths vic.sha256` | exit **0**, measured file **overwritten** | exit **2**, USAGE, file intact |
| (a2) | `capture --out vic.sha256 --paths vic` (literal claim spelling) | exit 0, bystander neighbour overwritten | exit **2**, neighbour intact |
| (b) | `capture --out <regular-file>/sub/r.txt --paths meas.conf` | exit **1**, raw `NotADirectoryError` traceback | exit **2**, `USAGE: cannot create the receipt directory` |
| (b2) | `capture --out "" --paths meas.conf` | exit 2 declared (control, already correct) | exit 2, `USAGE: --out carries no usable name…` |
| (c) | 5× duplicate stanza of ONE path + `verify --live --require-paths 5` | exit **0**, `MATCH`, 0 coverage lines | exit **2**, `REFERENCE-COVERAGE: 1/5` (distinct basis) |
| (d) | both-sides-absent pair | `MATCH compared=0/11 exit 0`, unannotated | `MATCH exit 0` **with the ruling note** (`agreement on absence, not a verified presence`); error-carrying stanza still `UNEVALUABLE exit 14` |

### 3.2 The mutation matrix on the LANDED revision (the load-bearing result)

Each mutant reverts exactly one landed fix (pattern match `1/1`, `1/1`, `3/3`):

| variant | (a) exit / intact | (a2) exit / bystander | (b) exit / traceback | (b2) exit | (c) exit / distinct | legit write | selftest |
|---|---|---|---|---|---|---|---|
| base `7cd19c3c…` | 0 / **false** | 0 / **false** | 1 / **true** | 2 | 0 / none | ok | 22/22 CLEAN |
| **LANDED `29bb45ae…`** | 2 / true | 2 / true | 2 / false | 2 | 2 / **1** | ok | **28/28 CLEAN** |
| **MUT-A** guard → `out` only | **0 / false** | **0 / false** | 2 / false | 2 | 2 / 1 | ok | **DIRTY 26/28** |
| **MUT-B** mkdir outside the try | 2 / true | 2 / true | **1 / true** | 2 | 2 / 1 | ok | **DIRTY 27/28** |
| **MUT-C** coverage → stanza count | 2 / true | 2 / true | 2 / false | 2 | **0 / none** | ok | **DIRTY 27/28** |

Reading: each mutant restores **exactly** its own before-behavior and leaves the
other legs fixed — diagonal, so each fix is load-bearing and none is a
prerequisite of another. The landed selftest independently names the reverted
fix in every case:

```
MUT-A  FAIL refuses-sidecar-over-measured-file     (expected USAGE …, got 0)
       FAIL refuses-receipt-over-sidecar-neighbour (expected USAGE …, got 0)
MUT-B  FAIL out-parent-not-a-directory-usage-exit  (expected USAGE exit 2, got 1)
MUT-C  FAIL coverage-gate-rejects-duplicate-stanzas(expected USAGE exit 2 …, got 0)
```

### 3.3 Other claim legs measured first-hand

- **selftest**: 22/22 CLEAN (base) → **28/28 CLEAN** (landed) — the "22 → ≥24"
  leg is satisfied with 4 cases to spare, and all three residuals have their own
  cases (20-25).
- **live pair**: `verify live-pre.txt live-post.txt` → `MATCH 5/5 exit 0`, and
  `--require-paths 5` → `MATCH 5/5 exit 0`; re-run by this seat on EX-21's
  receipts (`claims/c3/EX-21/receipts/`), exit 0 both ways.
- **(d) ruling text**: landed in the README (`## The both-absent MATCH (ruling,
  arc3-loop1-round4)`) and in the tool's own row note; both reproduced.
- `command A` and the registry row are outside this seat's reach (other chains /
  parent integration).

### 3.4 Rehearsal round (before the target landed) — kept as the false-positive control

Before `29bb45ae` existed I built a reference revision from the r3 patch shapes
(`DRESS2`, `6e920b22…`) and its three single-fix mutants; the matrix was diagonal
there too, and the independent partial-fix controls behaved as declared:

| control | sha | result of my legs |
|---|---|---|
| EX-24 `after2` (mkdir fix only) | `ac2cd74e…` | B fixed; **A and C still at before-behavior**; selftest 24/24 |
| EX-23 guarded variant (sidecar spelling A only) | `b61cee68…` | A fixed; **A2 still exit 0 with the neighbour clobbered**; B and C at before-behavior |

Both readings match those revisions' actual diffs — the legs do not
false-positive on a partially-fixed tool.

## 4. Attacks / refutations attempted

| # | attack | verdict |
|---|---|---|
| 1 | "the sidecar fix is free" | **CONFIRMED as a real trap, then closed**: the naive eager-sidecar shape turns `--out ""` from declared USAGE 2 into a `ValueError` traceback (my `DRESS` vs `DRESS2`). The landed bytes guard the derivation (`USAGE: --out carries no usable name…`) — my leg B2 reads exit 2, no traceback |
| 2 | "the claim's literal spelling `--out X.sha256 --paths X` is covered by the same fix" | **REFUTED for the naive fix, CONFIRMED closed in the landed bytes**: EX-23's candidate (`b61cee68…`) leaves it at exit 0 with the neighbour clobbered (RV-8 independently confirms); the landed revision refuses it (exit 2, neighbour intact) via the `neighbours` set. My `DRESS3`/`MUT-A3` pair isolates that extra arm |
| 3 | "the mutants only fail because they crash" | **REFUTED** — MUT-A exits 0 with a clean `CUSTODY_PAIR_CAPTURE: OK`; MUT-C exits 0 with a full `VERDICT: MATCH`; only MUT-B crashes, and that *is* (b)'s before-class |
| 4 | "the probe's legs are entangled" | **REFUTED** — the diagonal in §3.2 on the landed bytes |
| 5 | "the probe false-positives on any revision" | **REFUTED** — two independent partial-fix controls (§3.4) read exactly the fixes their diffs contain |
| 6 | "a fixture accidentally touches a custody path" | **REFUTED** — every fixture is created inside the scratch box; no leg writes a custody path; all runs under `/dev/shm` |
| 7 | "the coverage fix could leave count and `unaccounted:` on different bases" | **CONFIRMED as a coupling**: the landed fix routes both through `distinct_paths()`; MUT-C reverts all three call sites together and reproduces the silent-pass |
| 8 | "`--out ''` regression is pre-existing" | **REFUTED** — exit 2 on base, exit 1 on the naive fix, exit 2 on the landed bytes |
| 9 | "(d) was silently re-labelled to avoid work" | **REFUTED** — the landed bytes keep `MATCH` for cleanly-absent stanzas, add the explanatory row note, and keep the error-carrying form `UNEVALUABLE` (14); measured both |

## 5. Blockers

**None remaining for this seat's task.** The target landed at 14:09:25Z while I
was mid-poll; everything above is measured against the landed bytes
`29bb45ae…`. Two scope notes for the parent:

1. The mutants are built by textual pattern from the landed revision
   (`mutant-build-r4.py` reports `matched=N/N` and would report `PARTIAL` on a
   future revision whose fix shape changed) — re-run that script after any
   further tool revision, before trusting the matrix.
2. `command A` / registry-row / pointer-table coupling were not measurable from
   this seat (c1/c2 surfaces); this report claims nothing about them.
