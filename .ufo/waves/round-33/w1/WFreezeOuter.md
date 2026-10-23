# WFreezeOuter — round-33 freeze-integrity outer gate

Seat: `KaidokuR33.WFreezeOuter` (leaf). Lane: `kaidoku-shokunin`, read-only production.
Measured revision: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (`git rev-parse HEAD`, 2026-10-23T09:30Z).
Round-32 base: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.

**Scope of this report**: instrument and repair evidence only. Nothing here is an admission
benchmark, a carrier measurement, a 32-row result, or a revival of R33-C1. R33-C1 stays
stopped per `.ufo/waves/round-33/claim-stop.json` (freeze_status `NOT FROZEN`, verdict
`unprovable; honest stop`). The held R33FixtureBuilder and every derivative of it were not
opened, read or used; no `k01/k02/k08` derivative was inspected. The round-32 envelope files
(k01..k12) appear below **by path name only** from `git ls-tree` — their contents were not
opened.

## 1. Instrument under test

| item | value |
|---|---|
| path | `tools/round-33/freeze-integrity.py` |
| sha256 (worktree) | `a753b1d70ce8d7062fe9ffae8a31d90eb21fe26c30649d51bd95bd68ad656bb2` |
| sha256 of `HEAD:` blob | `a753b1d70ce8d7062fe9ffae8a31d90eb21fe26c30649d51bd95bd68ad656bb2` (identical → worktree == commit) |
| preserved r32 gate | `tools/round-32/freeze-integrity.py` sha256 `6b5aa1dfcaef04b8d6e58babebf826d677d6eeecc8b13906213dfd8f041804cd` |
| python / git | `3.14.8` / `2.56.0` |
| tool installs this run | none |

The round-33 file is the round-32 gate plus a `--selftest` harness. Audited by diff
(`logs/gate.diff`, sha256 `fb30eca4a81a2accbf45af4e842116e68ab18291f496a6615e4e2cf7643f5612`):
**223 added lines, 4 removed lines**, and the four removals are only the docstring line, the
usage line, and `--root`/`--round` losing `required=True` so `--selftest` can run without them.
The pin/history loop is unchanged. So the pin semantics asserted below are the same code the
round-32 freeze pinned.

## 2. Five-case outer selftest (one run, as assigned)

`argv: python3 -I -B <lane>/tools/round-33/freeze-integrity.py --selftest`
start `2026-10-23T09:30:44Z` → end `2026-10-23T09:30:44Z`, **exit 0**, stderr empty
(stdout sha256 `740d541e4bdc214de15f9c8791bd3415a97f24e70894e88a49d9652336398bf1`):

```
case clean: PASS freeze=2d1365bd0fca pins=2 exit=0
case tampered_pin: PASS exit=1 changed=1 sha=2412b990a7d3
case restored_after_change: PASS exit=1 digest_matches history_flagged commits_after_freeze=a5de85f,e52f529
case absent_claims: PASS exit=2 claims=.ufo/waves/round-99/claims.json absent
case missing_pinned_file: PASS exit=1 sha=absent changed=1
freeze-integrity-selftest: PASS cases=5 elapsed_s=0.24 base=/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest
```

The five outer exits are `0 / 1 / 1 / 2 / 1`. Each printed exit is bound to the real
subprocess status by an in-source assertion (`_check(rc == 0|1|2, ...)` after
`_run_gate` returns `proc.returncode`), so the PASS lines are exit-code assertions, not
narration. Case semantics: clean pinned tree → 0; committed tamper → 1; tamper-then-restore →
1 with the digest *matching* the pin (proves the history term, not just content); absent
claims → 2; a pin for a never-existing path → 1 with `sha=absent`.

Residue: the five `mkdtemp` fixtures are removed by `_drop`; the base dir now holds only the
pre-existing author files from 08:10:53Z–08:11:20Z (`freeze-integrity.py` copy,
`invocation-check.err/.log`, `selftest-run.log`, `selftest.diff`).

## 3. Lane variants at `d7076120` — historical 8 / 2 / 2

All three run `--root <lane> --round 32 --claims .ufo/waves/round-32/<v> --rev d7076120…`,
all start `2026-10-23T09:30:50Z`, end `2026-10-23T09:30:50Z`, **exit 0**, stderr empty.

`claims.json` (8 pins, freeze `9a73680af21b`, stdout sha256 `445ac4bc…`):

```
ok	corpus/evidence/round-32/c1/carriers.tsv	sha=8cf97b37f72b	commits_after_freeze=0
ok	corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s	sha=7c29f128a447	commits_after_freeze=0
ok	corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s	sha=c043b74850a4	commits_after_freeze=0
ok	corpus/evidence/round-32/c1/predictions.tsv	sha=fd8049498e51	commits_after_freeze=0
ok	tools/round-32/arm64x_oracle.py	sha=17eea1f9768e	commits_after_freeze=0
ok	tools/round-32/build-arm64x-carriers.sh	sha=7da284da5986	commits_after_freeze=0
ok	tools/round-32/c1-arm64x-positive.py	sha=7a534be655f9	commits_after_freeze=0
ok	tools/round-32/c2-capability-calibration.py	sha=c3412b04f5b6	commits_after_freeze=0
freeze-integrity: CLEAN pins=8 freeze=9a73680af21b rev=d7076120e4f00c6d18aa77b8764d14861e820eb2
```

`claims-v2.json` (2 pins, freeze `9d54070bebce`, stdout sha256 `9802e1c2…`):

```
ok	tools/round-32/c2-capability-calibration-v2.py	sha=82434cba039e	commits_after_freeze=0
ok	tools/round-32/freeze-integrity.py	sha=6b5aa1dfcaef	commits_after_freeze=0
freeze-integrity: CLEAN pins=2 freeze=9d54070bebce rev=d7076120e4f00c6d18aa77b8764d14861e820eb2
```

`claims-v3.json` (2 pins, freeze `f382e3b7978e`, stdout sha256 `7430fa99…`):

```
ok	tools/round-32/c2-capability-calibration-v3.py	sha=5955e8ace76d	commits_after_freeze=0
ok	tools/round-32/freeze-integrity.py	sha=6b5aa1dfcaef	commits_after_freeze=0
freeze-integrity: CLEAN pins=2 freeze=f382e3b7978e rev=d7076120e4f00c6d18aa77b8764d14861e820eb2
```

**Retained pin counts: 8 / 2 / 2, changed=0 everywhere.** The three freeze ids match the
project's own record exactly: `claims.json` supersedes block names `9a73680af21b`, v2 names
`9d54070bebce`, and v3 is the commit that added it (`f382e3b7`).

`--rev` defaulting was exercised too: `--round 32` with no `--rev` gives
`CLEAN pins=8 freeze=9a73680af21b rev=HEAD` (sha256 `3f226c5d…`), i.e. `HEAD == d7076120`.

## 4. Independent cross-checks (not produced by the instrument)

1. **Pin digests, three ways, 11/11.** For every distinct pinned path (union of the three
   claims files = 11 paths): `git show d7076120:<path>` sha256 == the pin digest **and** the
   worktree file sha256 == that blob. 0 mismatches. The gate reads the *rev blob*; the
   worktree comparison is a check the gate does not perform, and it agrees.
2. **Freeze-file self-coverage.** The gate reads each claims file *at its freeze commit*, so it
   never notices a later edit to the claims file itself. Checked separately: for all three,
   blob-at-freeze == blob-at-`d7076120` and **no commit touches the claims file after its own
   freeze** (`claims.json` none, `claims-v2.json` none, `claims-v3.json` none). The blind spot
   is real but currently unexercised.
3. **Rev sweep** on `claims.json` (`logs/revsweep.meta`):

   | rev | start→end UTC | exit | line |
   |---|---|---|---|
   | `283aad7f` (base) | 09:33:42Z→09:33:42Z | 2 | `ERROR no commit adds .ufo/waves/round-32/claims.json at 283aad7f` |
   | `428315a8` | 09:33:42Z→09:33:42Z | 0 | `CLEAN pins=8 freeze=9a73680af21b` |
   | `9a73680af21b` (freeze) | 09:33:42Z→09:33:43Z | 0 | `CLEAN pins=8 freeze=9a73680af21b` |
   | `d7076120` (HEAD) | 09:33:43Z→09:33:43Z | 0 | `CLEAN pins=8 freeze=9a73680af21b` |

   At the base the claims file does not exist → exit 2 (the exit-2 path is real lane data, not
   only a fixture). At the freeze commit the history term is vacuous (`freeze..rev` empty), so
   the `d7076120` result is the one that actually carries the 9 intervening commits.
4. **Round 33 has no freeze, by the gate's own rule**: `--round 33 --rev d7076120` exits 2 with
   `ERROR no commit adds .ufo/waves/round-33/claims.json` (sha256 `3f581f1b…`), and
   `git log --all -- '.ufo/waves/round-33/claims*'` is empty. This independently corroborates
   `claim-stop.json`'s `freeze_status: NOT FROZEN`.
5. **Cross-instrument agreement.** The *pinned* round-32 gate (`6b5aa1df…`) run on the same
   lane/rev produces **byte-identical stdout** to the round-33 gate for all three variants:
   `claims.json` `445ac4bc…`, `claims-v2.json` `9802e1c2…`, `claims-v3.json` `7430fa99…`.
   Given the diff above, this is agreement by shared code, not by independence of
   implementation — it rules out a round-33 editing accident, not a shared misconception.

## 6. Real-bytes replica negative control

Script (retained): `/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeOuter/build-replica-control.py`.
It materializes the **actual** round-32 claims bytes and the **actual** pinned payload
(84,635 bytes over 11 pinned paths + 3 claims files, hard-asserted < 1 MiB) into a tiny sandbox
repo under `/fast/scratch/hyaku/`, verifying each blob against its pin on the way in, then
walks four repository states. Run `2026-10-23T09:31:59Z`→`09:31:59Z`, exit 0, replica freeze
`21aa5b38121a`.

| state | claims.json (8) | claims-v2.json (2) | claims-v3.json (2) |
|---|---|---|---|
| s1 freeze | exit 0 `CLEAN pins=8` | exit 0 `CLEAN pins=2` | exit 0 `CLEAN pins=2` |
| s2 tamper `arm64x_oracle.py` | **exit 1** `FAIL pins=8 changed=1` | exit 0 `CLEAN pins=2` | exit 0 `CLEAN pins=2` |
| s3 restore pin bytes | **exit 1** `FAIL … sha=17eea1f9768e commits_after_freeze=eeec327,94e066b` | exit 0 `CLEAN` | exit 0 `CLEAN` |
| s4 claims.json edited after freeze | **exit 1** `FAIL pins=8 changed=1` | exit 0 `CLEAN` | exit 0 `CLEAN` |

What this buys: the same instrument that prints `CLEAN pins=8` on the lane prints `FAIL
pins=8 changed=1` when a *real* pinned file's bytes are altered, and still fails after the
bytes are restored (`sha=` equals the pin, `commits_after_freeze` non-empty) — so the CLEAN at
§3 is not vacuous. The v2/v3 columns staying clean under an `arm64x_oracle.py` tamper show the
per-file pin sets are disjoint where they should be. s4 shows the §4.2 blind spot in action:
with `claims.json` rewritten post-freeze to pin the oracle at `0`×64, the gate still reports
`pins=8` from the freeze-commit copy and never reads the edited file — the designed semantics,
and a limit worth knowing.

## 7. Boundaries and gaps found

- **Coverage of the freeze is 11 of 39 round-32 files at this rev.** 28 files are unpinned:
  24 envelope files (12 `k01..k12.json` + 12 `.stderr`), 3 source snapshots
  (`corpus/evidence/round-32/sources/{arm64x-pe.md,pe-format.html,pe-format.md}`) and
  `corpus/evidence/round-32/c1/runs.tsv`. `CLEAN pins=8/2/2` therefore does **not** mean "the
  round-32 evidence set is untampered"; evidence integrity is the C1 counter's job (committed
  envelope == live envelope), and that counter cannot run here (no REA, no carriers).
- **The gate never checks the claims file at `--rev`.** Only the freeze-commit copy is read
  (§4.2, §6 s4).
- **Default `--claims` is `claims.json`**, i.e. the *v1* pin set. A round-32 audit that omits
  `--claims` silently checks 8 pins and never touches the v2/v3 counters or the v2/v3 gate
  pin. All three variants must be invoked together, as done here.
- The gate verifies **history shape**, not semantics: a pin whose freeze commit already held
  the "wrong" bytes would pass, and the selftest's clean case is by construction.
- Selftest fixtures are staged under a hardcoded shared base
  (`/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest`), not under a per-seat directory; my run
  left no fixtures there, but two concurrent selftest runs share that parent.

## 8. Lane safety

- No lane Git/JJ writes. Only `git log/show/rev-parse/ls-tree/cat-file/count-objects` and the
  gate's own read-only calls; `GIT_OPTIONAL_LOCKS=0` and `--no-optional-locks` used for the
  status checks.
- Tracked worktree dirty set: empty before and after. No `.git/*.lock` at the end, no
  `__pycache__` created under `tools/round-33/`, pinned-file mtimes untouched
  (`arm64x_oracle.py` 05:59:44.148Z, `claims.json` 06:03:28.109Z, `freeze-integrity.py`
  08:12:29.304Z — all predate the first run at 09:30:44Z).
- `.git/` directory mtime is volatile during the window (observed `09:32:38Z`, then
  `09:34:25Z`) while every *entry* inside it predates my runs (`.git/index` 09:29:57Z,
  `logs/HEAD` 09:27:49Z). `[INFERENCE]` other live seats issue git commands in this lane and
  create/remove a transient `.git/index.lock`; no objects were added (`count-objects`: 4
  packs, `garbage 0`), no ref moved (`HEAD` still `d7076120`). Reported rather than repaired.
- Post-run re-hash (after every run, at 09:35Z) of all 11 pinned worktree files still equals
  their pin digests exactly — e.g. `arm64x_oracle.py` `17eea1f9768e…`, `carriers.tsv`
  `8cf97b37f72b…`, `freeze-integrity.py` (r32) `6b5aa1dfcaef…`; `HEAD` still `d7076120…`;
  tracked tree clean.
- Only lane write: this report. All fixtures/logs/receipts are under
  `/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeOuter/` (484 KB, of which 400 KB is the replica).
- No subagents, no background jobs, no builds/tests/linters, no network, no REA/MCP, no
  credentials read. Every subprocess ran under `timeout`; nothing was left running.

## 9. Risks

1. The strongest result here (`CLEAN 8/2/2` at `d7076120`) says the instruments and frozen
   inputs are unmodified since their freezes. It says nothing about the 28 unpinned evidence
   files, and it cannot substitute for the C1 counter that would compare envelopes to runs.
2. Cross-instrument agreement is agreement of one code path with itself across two revisions;
   a shared misreading of "commit touches path" would not be caught by §4.5. The §6 control
   bounds that: commit-touch and content failure were separately observed on real bytes.
3. The five selftest cases all use round 99 fixtures; none exercises a multi-claims round, so
   the 8/2/2 selection behaviour is evidenced only by the lane runs and the §6 matrix.
4. The `.git/` mtime bump (§8) is unexplained by my commands and is left as a stated
   observation.

## 10. Blockers

None for this item. The assigned work is complete: selftest once, three `--round 32 --claims`
variants at the pinned revision, exact five-case exits, exact 8/2/2 pin counts, all retained.

## Evidence index (`/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeOuter/`)

| file | sha256 |
|---|---|
| `logs/selftest.out` | `740d541e4bdc214de15f9c8791bd3415a97f24e70894e88a49d9652336398bf1` |
| `logs/claims-json.out` | `445ac4bcb509b77e3141b5504c0afd7745161cf007f1065d1e6f6a6f5e262559` |
| `logs/claims-v2-json.out` | `9802e1c2f8b0f4922cacb46ade8d84b612cd75bd60f07bbdb9f8694673be895a` |
| `logs/claims-v3-json.out` | `7430fa990960e126e45c4b1b12228d358c18c0695bd6590f607add5bd3c8f679` |
| `logs/gate-defaultrev.out` | `3f226c5d6474c4cfac7be7fc43648893ab5b895401a6863a3985e5f131ac480e` |
| `logs/gate-round33.out` | `3f581f1ba58743aaefd52627f0301dd8c5028b0c12cbeacd4acfa9f0b834544b` |
| `logs/r32gate-claims.out` | `445ac4bc…` (identical to `claims-json.out`) |
| `logs/r32gate-claims-v2.json.out` | `9802e1c2…` (identical to `claims-v2-json.out`) |
| `logs/r32gate-claims-v3.json.out` | `7430fa99…` (identical to `claims-v3-json.out`) |
| `logs/replica-control.json` | `728333f5df6f6a15ada43691ac025ca30a5bad7b5a69975cb185ae77e017e362` |
| `logs/gate.diff` | `fb30eca4a81a2accbf45af4e842116e68ab18291f496a6615e4e2cf7643f5612` |
| `logs/unpinned-round32.txt` | `81c31b26c20ff97404e63771c8a0f2efcdfce67f65970367ad9eaf5f6fcc3647` |
| `logs/revsweep.meta` + `logs/revsweep-<rev>.out` | see §4.3 |
| `receipts/freeze-outer-receipt.json` | structured argv/start/end/exit/pin table |
| `build-replica-control.py` | replica control script (real bytes, sandbox only) |

All stderr files are empty (`e3b0c442…`, the sha256 of zero bytes) except where quoted.
