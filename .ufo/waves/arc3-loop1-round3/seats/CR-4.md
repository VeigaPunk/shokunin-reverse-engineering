# SEAT CR-4 — chain c2 — critic — write-guard attack (arc3-loop1-round3)

Task: attack the extended write-guard; hunt a new bypass (hardlink alias,
relative-path trickery, `--out` via symlink); scratch only.

Revisions named by sha256 of `custody-pair.py` content as tested. The C2 landing
was in mid-edit churn throughout this seat's run (observed sequence
`112d01dc… → 7b848eaf… → 68e30768… → 460a01f0… → b9bd55e9… → 9860149d… →
ec2b2d48… → 03bd6242… → 57dffff1… → dc841464… → 89bfebec…`); every verdict below
names the revision it was measured at. Final verdicts are at `dc841464…`
(selftest 21/21 CLEAN); `cmd_capture` was diff-verified byte-identical at the
later snapshot `89bfebec…`, so the verdicts hold for the current guard body.

## 1. Work performed (evidence pointers)

Artifacts, all under `.ufo/waves/arc3-loop1-round3/claims/c2/CR-4/`:

| file | what it is |
|---|---|
| `attack-battery.sh` | 19-case write-guard battery (`T0`…`T18`), every write under a fresh `/dev/shm` sandbox with a sandboxed `HOME`; real custody paths never opened for writing |
| `build-variants.py` | builds the three reference guard variants in scratch from a base revision (L1 literal `set(paths) ∪ CUSTODY_PATHS`; L2 half-fix trap; L3 resolve+samefile+sidecar fail-closed) |
| `toctou-race.sh` | symlink-swap race probe: an atomic swapper retargets `--out` between an unguarded file and the guarded `$HOME/.bashrc` while `capture` runs |
| `attack-failopen.sh` | blocked-side probe: scoped path inside a mode-000 dir + hardlink alias outside; tests the inode arm's `OSError` path |
| `run-current.out` | battery at `112d01dc…` (round-2 landed, canonical-only guard) |
| `run-L1.out`, `run-L2.out`, `run-L3.out` | battery at the three reference variants built on `112d01dc…` |
| `run-landed-ec2b2d48.out`, `run-landed-dc841464.out` | battery at the landed extensions |
| `race-old-revision.out`, `race-landed.out` | race probe, 300 attempts each, pre/post extension |
| `selftest-landed.out`, `selftest-landed-dc841464.out` | the landed revision's own selftest (15 CLEAN mid-landing; 21 CLEAN final) |
| `failopen-base.out`, `failopen-landed.out` | blocked-side probe at `112d01dc…` and at the landed revision |
| `proposed-write-guard.patch.md` | patch-text proposal: guard the sidecar path, mkdir inside the declared map, measured TOCTOU declaration, fail-open arm, non-atomic write ordering |
| `poll-landing.sh`, `poll-landing-v2.sh`, `/dev/shm/cr4-arc3-r3/poll*.log` | landing/churn log with revision hashes every 60 s |

Landed guard under attack (landed revision, `cmd_capture`):

```python
        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        if out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded):
            print("USAGE: refusing to write a receipt over a path it measures or a custody path"
                  " (path or inode): %s" % out, file=sys.stderr)
            return EXIT_USAGE
```

## 2. Proposed changes

`proposed-write-guard.patch.md` (this seat writes no tool code; EX-21 is the
designated implementer):

1. Extend the guard to the derived sidecar path `out.with_name(out.name + ".sha256")`
   — measured bypass T7/T18, still open at the landed revision.
2. Move `out.parent.mkdir(parents=True, exist_ok=True)` inside the `try:`, or map
   its `OSError` to USAGE — measured hole T16 (traceback, exit 1, declared-map
   violation).
3. Carry the measured TOCTOU rate in the scope statement (already declared out of
   scope by the landed docstring; numbers below), and optionally close the symlink
   vector with `O_NOFOLLOW`/fstat-recheck.
4. Add a selftest case for the sidecar spelling. The claim's 15 → ≥17 is met at
   the landed revision (21 CLEAN), but none of the 21 exercises the derived
   sidecar path — which is exactly why T7/T18 still pass.
5. State the inode arm's fail-open exception (blocked-side probe below) in the
   docstring's scope sentence, or make it fail closed when a scoped path is
   unstattable.

## 3. Before→after measurement (chain claim: write-guard extended to `set(paths) ∪ CUSTODY_PATHS`)

Command: `bash attack-battery.sh <revision> <label>` (19 cases, sandboxed HOME).

Before — `112d01dc…`: **10 of 19 cases ALLOWED a clobber** of a file the run
measures: T0 scoped-as-out, T1 hardlink alias of a scoped file, T2 symlink alias,
T3 relative-vs-absolute spellings, T5 `/proc/self/root` alias, T7 sidecar path,
T8 symlink alias, T9 canonical-`.bashrc` hardlink (D7 re-confirmed), T11
symlinked parent dir, T12 `~` spelling. Plus T4 (`/proc/self/fd/N`): receipt
bytes landed through the alias while the sidecar write failed — exit 2 *after* a
destructive write.

After — landed revision `dc841464…` (guard = resolve-set ∪ `_same_file` over
canonical ∪ scoped; `cmd_capture` diff-identical at `89bfebec…`): T0, T1, T2,
T3, T4, T5, T6, T8, T9, T10, T11, T12, T17 all exit 2 REFUSED with victims
byte-identical; T13/T14/T15 (must-allow: fresh `--out`, missing scoped path,
plain path) still exit 0/13 with the receipt written — the inode arm does not
regress ordinary captures (`_same_file` returns False on `OSError`).

Still open at the landed revision (measured, not inferred):

- **T7 sidecar path** — `capture --out scope/vic --paths scope/vic.sha256` → exit 0,
  `scope/vic.sha256` CLOBBERED by the receipt sidecar. The guard covers `--out`,
  not the derived sidecar write (`sidecar = out.with_name(...)` inside the try;
  the landed guard never inspects it). Reference variants: ALLOWED on the base and
  L1, REFUSED only on the fail-closed variant that guards `(out, sidecar)`.
- **T18 sidecar hardlink alias** — no name coincidence needed: `--out mk18` where
  `mk18.sha256` is a hardlink of the scoped file → exit 0, scoped file CLOBBERED.
- **T16** — `--out <regular file>/sub/r.txt` → `NotADirectoryError` from the
  `mkdir` outside the `try` → raw traceback, exit 1, outside the declared map
  (reproduced on the base revision and all three reference variants; the landed
  revision still has `mkdir` outside the `try`).
- **Blocked-side fail-open (inode arm)** — `attack-failopen.sh`: scoped path in a
  mode-000 dir (`EACCES`), hardlink alias outside it, `--out` = alias. Landed
  revision: `exit=14` (UNEVALUABLE, D2 closed) **and the receipt written over the
  alias — victim CLOBBERED**. `_same_file` catches `OSError` and returns False, so
  a scoped path the tool itself records as unevaluable is not protected against
  its own alias, contradicting the docstring's "refuses … a path it measures"
  without exception. Base revision clobbers too (exit 13, the D2 fail-open read).
  Severity: low under the declared threat model (an actor able to create the
  alias can already write the file), but the exception belongs in the scope
  sentence, or the arm should fail closed for unstattable scoped paths.
- **Half-fix trap pinned (L2)** — resolving `out` but not the scope side leaves
  `--out ./x --paths x` (relative spellings) clobbering; the landed revision
  resolves both sides, so it is safe on this axis.
- **TOCTOU (declared out of scope)** — race probe, 300 attempts each:
  pre-extension `68e30768…`: 76/300 and 60/300 clobbers of the guarded file
  (20–25%); landed extension `ec2b2d48…`: 12/300 (4%), refusals rose 141–174 →
  272/300 because the added `stat` calls widen the check window. The landed
  docstring declares TOCTOU inherent and out of scope — the honest declaration
  now has a measured cost.
- **Self-refutation of my own L3 reference**: `--out ''` dies at exit 1 in L3
  (`with_name` on an empty name → `ValueError` outside the try) while the base
  revision answers exit 2 USAGE. If EX-21 guards the sidecar, compute its name
  inside the guarded region or catch `ValueError` too — a hardening that makes
  the declared map worse than the base is a regression.

Selftest at the landed revision: `CUSTODY_PAIR_SELFTEST: CLEAN cases=21 passed=21
failed=0 exit=0` (`selftest-landed-dc841464.out`) — claim target 15 → ≥17 met,
with `refuses-to-write-over-scoped-path`, `refuses-to-write-through-hardlink-alias`,
`unreadable-file-is-unevaluable`, `stat-blocked-path-is-unevaluable`,
`require-paths-blocks-partial-reference`, `selftest-unusable-scratch-usage-exit`
among the new cases. D6 closed: `selftest --scratch <missing>` → `USAGE: scratch
base is not a directory: …`, exit 2.

## 4. Attacks/refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| 1 | `--paths X --out X` (VZ-4 baseline) | REFUTED at landed revision (exit 2); was a clobber at `112d01dc…` |
| 2 | hardlink alias of a scoped file (custom `--paths`) | REFUTED at landed (inode arm catches) |
| 3 | hardlink alias of canonical `.bashrc` (D7) | REFUTED at landed; still open on the literal L1 extension (ALLOWED/CLOBBERED) — the inode arm is what closes it, not the scope extension |
| 4 | symlink alias / dangling-symlink alias | REFUTED at landed (`resolve()`); also REFUTED by L1 |
| 5 | relative-vs-absolute spellings | REFUTED at landed; ALLOWED on the L2 half-fix — the exact implementation trap named in the proposal |
| 6 | `/proc/self/fd/N` alias | REFUTED at landed; at `112d01dc…` it wrote the receipt through the alias and then failed the sidecar (exit 2 after a destructive write) |
| 7 | `/proc/self/root` alias | REFUTED at landed |
| 8 | symlinked parent directory | REFUTED at landed |
| 9 | `~` spelling | REFUTED at landed |
| 10 | symlink loop as `--out` | REFUTED (declared USAGE via the write-failure catch, no traceback) |
| 11 | **derived sidecar path** (`--paths vic.sha256 --out vic`) | **CONFIRMED OPEN** at landed: exit 0, scoped file clobbered |
| 12 | **sidecar hardlink alias** | **CONFIRMED OPEN** at landed: exit 0, scoped file clobbered |
| 13 | **`--out` whose parent is a regular file** (mkdir outside try) | **CONFIRMED OPEN** at landed: traceback exit 1 |
| 14 | **blocked-side alias** (scoped path unstattable) | **CONFIRMED OPEN** at landed: exit 14 UNEVALUABLE + receipt written over the alias; `_same_file` fail-open on `OSError` |
| 15 | empty `--out` | REFUTED at landed (exit 2) |
| 16 | fresh `--out`, missing scoped path, plain path (must-allow regressions) | hold at landed (no `samefile` crash) |
| 17 | symlink-swap TOCTOU race | CONFIRMED (12/300 at landed) — declared out of scope; quantified |
| 18 | inode identity across a *replace* (same inode reused) | not attempted in this seat — EX-33's case J / round-2 D4 territory (receipt-store trust domain), unchanged by this round's guard |

## 5. Blockers

- Revision churn (round-2 D8, recurring): the tool changed ≥11 times during this
  seat's run (`112d01dc…` → `89bfebec…`); measurements are pinned to snapshots and
  named by sha256. Final verdicts are at `dc841464…` with the guard body
  diff-verified identical at the later snapshot `89bfebec…`; if EX-21 changes the
  guard body again, the battery is re-runnable as
  `bash attack-battery.sh <tool> <label>`.
- Selftest growth landed after this seat's first measurement pass (15 → 21
  CLEAN); the battery verdicts were re-derived at the grown revision
  (`run-landed-dc841464.out`), so nothing here rests on the earlier 15-case run.
- `.ufo/gates/custody-pair/__pycache__/` exists again (untracked, first seen
  ~10:05Z; round-2 D9 recurrence — not created by this seat, which ran the tool
  as a script with `PYTHONDONTWRITEBYTECODE=1`). Exclude it from the wave-artifacts
  commit; the parent should note it as D9 at landing.

## 6. Identity re-derivation (rule #14)

`identity-rederivation.out` (written 10:14:04 — after the last revision of every
artifact it hashes; the seat report itself is not self-hashed and claims no
self-identity):

```
2026-10-19T10:14:04-03:00
tool under test at verdict time: 7cd19c3c…  (sha256, .ufo/gates/custody-pair/custody-pair.py)
tested snapshot:                 dc841464…  (sha256)
cmd_capture dc841464 vs now: identical = True
_same_file identical = True;  CUSTODY_PATHS identical = True;  EXIT_* identical = True
```

The revision changed three more times after the verdict runs
(`dc841464… → 89bfebec… → 7cd19c3c…`), but the diff is confined to selftest
cases and `_run_verify`; every guard-relevant block is byte-identical. Re-measured
rather than inferred: the full 19-case battery was re-run against `7cd19c3c…`
(`run-landed-7cd19c3c.out`) and **all 19 verdicts are identical** to the
`dc841464…` run — the still-open clobbers are exactly T7 (sidecar path) and T18
(sidecar hardlink alias), the traceback is exactly T16. Artifact hashes (sha256)
are in `identity-rederivation.out`; the real custody paths were touched read-only
(hash capture) — their digests are recorded there as the seat's protocol check.