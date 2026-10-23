# CriticFreezeAfter — Post-Data Freeze Integrity and Pre-Data Control Ordering Audit (Round 30, Wave 2)

Seat: `KaidokuR30.CriticFreezeAfter` (`critic`)
Attack target:
1. Did any frozen round-30 instrument or input change after freeze commit `4ee65c6771058284aa947a266475839d196ed4d4` (`2026-10-23T02:35:13Z`) through the measured revision `92b1dd2ddc119fda89a611ba515bdf6cfe906f76` (`2026-10-23T03:07:42Z`) and `HEAD` (`3502b94c5b93d86c5d67866035fd150899456295`, `2026-10-23T03:11:31Z`)?
2. Did any REA claim data (`corpus/evidence/round-30/c1|c2/{envelopes,runs.tsv}`) precede the pre-data control receipts (`004053d6322e332d0b972a0c927292a9ca0956a1` at `02:59:08Z`; 4-column reformat `f39f4530cb2542df4ea95999625b31577cc09afa` at `02:59:22Z`)?
3. Do `tools/round-30/prefreeze-gate.py`, `tools/round-29/freeze-gate.py`, and `tools/round-30/axis-fit-gate.py` actually catch post-freeze mutations of pinned files or pre-control `runs.tsv` timestamps?

---

## Verdict

- **Round-30 empirical freeze & ordering integrity: HOLDS (`observation`).**
  - Zero tracked bytes in any frozen instrument (`tools/round-30/c1-rust-positive.py`, `tools/round-30/c2-rust-refusals.py`, `tools/round-30/rust_dep_oracle.py`), frozen input (`corpus/evidence/round-30/c1/carriers.tsv`, `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json`, `corpus/evidence/round-30/c2/predictions.tsv`), or `.ufo/waves/round-30/claims.json` changed between `4ee65c67` and `92b1dd2ddc119fda89a611ba515bdf6cfe906f76` (or `HEAD` `3502b94c`).
  - On disk, 4 shared carriers were transiently rewritten in place during wave 1 (`02:42:35Z` and `02:43:14Z`) by seat `RevOracleVsReadobj` running `llvm-objcopy --dump-section` without an output object (`M30-2`, disclosed in `corpus/lessons/round-30.md:45`). The C1 counter's SHA-256 pin check (`tools/round-30/c1-rust-positive.py:221`) caught the mismatch with exit `2` (`PIN carrier ... absent or altered`) before any REA invocation; the L1 restored all 4 carriers from verified wheel members and set `chattr +i` (`----i`) on all 16 carriers before the valid control reruns (`02:44:44Z–02:46:28Z`) and before data collection (`02:59:33Z`). All 16 carriers, 19 mutants, and `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` match their frozen SHA-256 digests (`observation`).
  - Zero committed REA claim runs preceded `f39f4530` (`2026-10-23T02:59:22Z`, `ct = 1792724362`): C1 `runs.tsv` `utc_start` values span `2026-10-23T02:59:33+00:00` to `2026-10-23T03:00:26+00:00` (`+11 s` to `+64 s` after `f39f4530`); C2 `runs.tsv` `utc_start` values span `2026-10-23T03:00:36+00:00` to `2026-10-23T03:01:47+00:00` (`+74 s` to `+145 s` after `f39f4530`); all 35 envelope `.json` mtimes on disk lie inside `[utc_start, utc_end + 2s]`; and all 35 envelopes + `runs.tsv` were first committed at `24da3459` (`2026-10-23T03:04:20Z`, `ct = 1792724660`, `+298 s` after `f39f4530`) (`observation`).
- **Automated gate coverage for post-freeze integrity: FIXABLE DEFECT (non-blocking for round-30 admission, since round-30 bytes are clean by direct `git diff` and `runs.tsv` inspection).**
  - As demonstrated by sandbox counterexample commit `c80152b8a6f4877ea7a8c6c909c29fa2110ca1fa`, `tools/round-30/prefreeze-gate.py` checks pin digests **only at the freeze commit** (`freeze`), not at `--rev` (`measured`), and `tools/round-29/freeze-gate.py` checks `INSTRUMENT_REVISED` in `freeze..measured` **only** for script paths matched by regex inside `claims[]` strings (`c1-rust-positive.py`, `c2-rust-refusals.py`), leaving `tools/round-30/rust_dep_oracle.py` and all `frozen_inputs` (`carriers.tsv`, `pypi-uv-0.13.0.json`, `predictions.tsv`) unguarded against post-freeze commits by both gates. In addition, no gate compares `runs.tsv` `utc_start` against the control-receipt commit timestamp, and `axis-fit-gate.py` checks `first_add` (`--diff-filter=A`, `004053d6`) rather than the last modifying commit (`f39f4530`) of `.ufo/waves/round-30/controls/receipts.tsv`.

---

## 1. Post-Freeze Instrument and Input Integrity (`4ee65c67..92b1dd2d` and `HEAD`)

### 1.1 Tracked Git objects (`observation`)

- **Command (2026-10-23T03:12:21Z, exit 0):**
  ```sh
  git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 4ee65c67 92b1dd2ddc119fda89a611ba515bdf6cfe906f76 -- tools/round-30/c1-rust-positive.py tools/round-30/c2-rust-refusals.py tools/round-30/rust_dep_oracle.py corpus/evidence/round-30/c1/carriers.tsv corpus/evidence/round-30/c2/predictions.tsv corpus/evidence/round-30/c1/pypi-uv-0.13.0.json .ufo/waves/round-30/claims.json
  ```
  **Exact output:** *(empty — 0 bytes, 0 files changed)*.

- **Per-commit SHA-256 verification across all round-30 commits and working tree (`python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticFreezeAfter/audit_freeze_after.py`, 2026-10-23T03:17:04Z, exit 0, `observation`):**

| Path | Pinned SHA-256 in `claims.json` | `0dbabf78` (instruments) | `4ee65c67` (freeze) | `92b1dd2d` (measured) | `3502b94c` (`HEAD` & worktree) | Unchanged post-freeze? |
|---|---|---|---|---|---|---|
| `tools/round-30/rust_dep_oracle.py` | `f0b144c6…4be9d81d` | `f0b144c6…4be9d81d` | `f0b144c6…4be9d81d` | `f0b144c6…4be9d81d` | `f0b144c6…4be9d81d` | Yes |
| `tools/round-30/c1-rust-positive.py` | `e07563d6…4c323ed2a` | `e07563d6…4c323ed2a` | `e07563d6…4c323ed2a` | `e07563d6…4c323ed2a` | `e07563d6…4c323ed2a` | Yes |
| `tools/round-30/c2-rust-refusals.py` | `1c357fca…78857a6b` | `1c357fca…78857a6b` | `1c357fca…78857a6b` | `1c357fca…78857a6b` | `1c357fca…78857a6b` | Yes |
| `corpus/evidence/round-30/c1/carriers.tsv` | `c968cd1e…369e4e4b` | `c968cd1e…369e4e4b` | `c968cd1e…369e4e4b` | `c968cd1e…369e4e4b` | `c968cd1e…369e4e4b` | Yes |
| `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json` | `2eaed6c8…e284b4c` | `2eaed6c8…e284b4c` | `2eaed6c8…e284b4c` | `2eaed6c8…e284b4c` | `2eaed6c8…e284b4c` | Yes |
| `corpus/evidence/round-30/c2/predictions.tsv` | `6852df3a…c6c87315` | `6852df3a…c6c87315` | `6852df3a…c6c87315` | `6852df3a…c6c87315` | `6852df3a…c6c87315` | Yes |
| `.ufo/waves/round-30/claims.json` | *(self)* | *(absent)* | `65d94d3f…db1e989a` | `65d94d3f…db1e989a` | `65d94d3f…db1e989a` | Yes |

### 1.2 External on-disk pinned inputs (`/fast/scratch/hyaku/kaidoku-r30/{carriers,mutants}`, `rea-agents` pin) (`observation`)

- **Command (2026-10-23T03:14:35Z, exit 0):** Python SHA-256/size verification against `carriers.tsv` (16 rows), `predictions.tsv` (19 rows), `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`, and `lsattr /fast/scratch/hyaku/kaidoku-r30/carriers`.
- **Exact output excerpt:**
  ```text
  carriers_checked=16 carrier_mismatches=0 immutable_i=16/16
  mutants_checked=19 mutant_mismatches=0
  pkg_json_sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c matches_pin=True
  ```
- **Wave-1 `M30-2` incident verification (`observation` + `inference`):**
  - During wave 1 (`02:42:35Z` and `02:43:14Z`), seat `RevOracleVsReadobj` ran `llvm-objcopy --dump-section` without an output object argument on `elf-x86_64-uvx`, `pe-x86_64-uvx`, `macho-x86_64-uvx`, and `elf-x86_64-uv` (`.ufo/waves/round-30/w1/RevOracleVsReadobj.md:9-16`).
  - The C1 counter's SHA-256 guard (`c1-rust-positive.py:221`) rejected the altered files with exit `2` before invoking REA (`CtlC1AllFalse` at `02:42:59Z`, `CtlC1DoNothing` at `02:43:03Z`, `CtlC1NoReader` at `02:43:31Z`, `CtlC1JunkRow` at `02:43:46Z`).
  - One seat (`CtlC1ShortcutIds`) ran its single standalone seed `npx -y rea-agents@6.5.0 inspect-rust-binary` call on the altered `elf-x86_64-uvx` at `02:42:42Z` (`sha256=9f41e2d4…`), caught the digest mismatch in its own assertion at `02:43:18Z`, and re-ran after carrier restoration at `02:46:06Z` (`sha256=2e9105ad…`, matching the frozen pin).
  - By `~02:44:44Z`, all 4 carriers were restored from the verified wheel members and all 16 carriers were set `chattr +i`. Neither the committed control results nor the `02:59:33Z` claim measurements used altered bytes (`inference` from matching SHA-256 pins in all runs).

---

## 2. Temporal Ordering: Commit Timeline vs. `runs.tsv` `utc_start` (`observation`)

### 2.1 Commit timeline (`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format='%H %ct %cI %at %aI %s' d210fb8f..HEAD`, 2026-10-23T03:14:08Z, exit 0)

| Commit | Role | Committer epoch (`%ct`) | Committer UTC (`%cI`) | Author epoch (`%at`) | Author UTC (`%aI`) |
|---|---|---:|---|---:|---|
| `d210fb8fa62d` | Round-30 base | `1792702309` | `2026-10-22T20:51:49Z` | `1792701685` | `2026-10-22T20:41:25Z` |
| `0dbabf78b6ab` | Instruments & frozen inputs (6 files) | `1792722864` | `2026-10-23T02:34:24Z` | `1792702309` | `2026-10-22T20:51:49Z` |
| `4ee65c677105` | Freeze (`.ufo/waves/round-30/claims.json`) | `1792722913` | `2026-10-23T02:35:13Z` | `1792722864` | `2026-10-23T02:34:24Z` |
| `a6e7d9cee57e` | `before/` receipts & `w1` dispatch | `1792723640` | `2026-10-23T02:47:20Z` | `1792722913` | `2026-10-23T02:35:13Z` |
| `004053d6322e` | Wave-1 reports, gates & `controls/receipts.tsv` (initial 6-col) | `1792724348` | `2026-10-23T02:59:08Z` | `1792723640` | `2026-10-23T02:47:20Z` |
| `f39f4530cb25` | `controls/receipts.tsv` (4-col `axis-fit-gate` shape) + `receipts-detail.tsv` | `1792724362` | `2026-10-23T02:59:22Z` | `1792724348` | `2026-10-23T02:59:08Z` |
| `24da3459a5b4` | Claim data (16 C1 + 19 C2 envelopes & `runs.tsv`), entries, PROVINCE, SKILL | `1792724660` | `2026-10-23T03:04:20Z` | `1792724362` | `2026-10-23T02:59:22Z` |
| `92b1dd2ddc11` | Measured rev (SKILL lead-line fix `M30-4`, lesson, QUALITY rows 48–49) | `1792724862` | `2026-10-23T03:07:42Z` | `1792724660` | `2026-10-23T03:04:20Z` |
| `3502b94c5b93` | SCORECARD, LOG, `after/` receipts at `92b1dd2d`, `w2` spec (`HEAD`) | `1792725091` | `2026-10-23T03:11:31Z` | `1792724862` | `2026-10-23T03:07:42Z` |

*(Note on `%at` vs `%ct`: in Jujutsu, each commit inherits its author timestamp `%at` from when the working-copy commit `@` was instantiated immediately upon finalizing the parent commit, whereas `%ct` records when the commit itself was finalized. Every commit's `%at` above equals its parent's `%ct`.)*

### 2.2 `runs.tsv` `utc_start` and `utc_end` vs. `f39f4530` (`2026-10-23T02:59:22Z`, `ct = 1792724362`) (`observation`)

- **Command (2026-10-23T03:14:08Z, exit 0):** `python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticFreezeAfter/audit_freeze_after.py`
- **Exact output excerpt:**
  ```text
  4ee65c67 (freeze)           ct = 1792722913 (2026-10-23T02:35:13+00:00)
  004053d6 (w1 controls add)  ct = 1792724348 (2026-10-23T02:59:08+00:00)
  f39f4530 (controls 4-col)   ct = 1792724362 (2026-10-23T02:59:22+00:00)
  24da3459 (data commit)      ct = 1792724660 (2026-10-23T03:04:20+00:00)

  C1 (corpus/evidence/round-30/c1/runs.tsv): 16 rows
    earliest utc_start: elf-x86_64-uv @ 2026-10-23T02:59:33+00:00 (1792724373), delta vs f39f4530 = +11s, delta vs 004053d6 = +25s, delta vs 4ee65c67 = +1460s
    latest   utc_start: macho-arm64-uvx @ 2026-10-23T03:00:26+00:00 (1792724426), delta vs f39f4530 = +64s
    latest   utc_end  : macho-arm64-uvx @ 2026-10-23T03:00:31+00:00 (1792724431), delta vs 24da3459 = -229s
    rows with utc_start <= f39f4530 ct: []
    monotonically ordered start<=end<=next_start: True

  C2 (corpus/evidence/round-30/c2/runs.tsv): 19 rows
    earliest utc_start: g-relocated @ 2026-10-23T03:00:36+00:00 (1792724436), delta vs f39f4530 = +74s, delta vs 004053d6 = +88s, delta vs 4ee65c67 = +1523s
    latest   utc_start: r-index-outside @ 2026-10-23T03:01:47+00:00 (1792724507), delta vs f39f4530 = +145s
    latest   utc_end  : r-index-outside @ 2026-10-23T03:01:50+00:00 (1792724510), delta vs 24da3459 = -150s
    rows with utc_start <= f39f4530 ct: []
    monotonically ordered start<=end<=next_start: True
  ```
- **On-disk envelope mtime consistency (2026-10-23T03:16:13Z, exit 0, `observation`):**
  ```text
  === C1 runs.tsv mtime=2026-10-23T03:00:31.385509+00:00 ===
    envelope mtimes within [utc_start, utc_end+2s]: 16/16
  === C2 runs.tsv mtime=2026-10-23T03:01:50.675896+00:00 ===
    envelope mtimes within [utc_start, utc_end+2s]: 19/19
  ```
- **Note on wave-1 control-seat REA runs (`observation`):**
  During wave 1 (`02:44:19Z–02:47:13Z`, after the freeze `4ee65c67` at `02:35:13Z` and before `004053d6`/`f39f4530` at `02:59:08Z`/`02:59:22Z`), the six control seats (`CtlC1DoNothing`, `CtlC1JunkRow`, `CtlC1AllFalse`, `CtlC1NoReader`, `CtlC1ShortcutIds`, `CtlC2Sequence`) invoked the frozen C1 and C2 counters in measure mode (without `--write-evidence`) inside their scratch clones; because the counters always execute REA live before checking the committed-envelope clause, REA ran on the carriers and mutants during wave 1 to score the controls. None of those wave-1 runs wrote to `corpus/evidence/round-30/`; the committed claim envelopes and `runs.tsv` were freshly generated by `--write-evidence` runs at `02:59:33Z–03:01:50Z` after `f39f4530`, as confirmed by the 35 file mtimes above (`observation`).

---

## 3. Gate Runs and Counterexample Attack on Gate Blind Spots

### 3.1 `prefreeze-gate.py` on the lane (`observation`)

- **Command (2026-10-23T03:12:21Z, exit 0):**
  ```sh
  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/prefreeze-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 30
  ```
- **Exact stdout (exit 0):**
  ```text
  prefreeze round=round-30 freeze=4ee65c6771058284aa947a266475839d196ed4d4 rev=3502b94c5b93d86c5d67866035fd150899456295 claims=.ufo/waves/round-30/claims.json
  pins=6 present=6 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
  verdict=CLEAN
  ```
  *(With `--rev 92b1dd2ddc119fda89a611ba515bdf6cfe906f76`, stdout is identical except `rev=92b1dd2ddc119fda89a611ba515bdf6cfe906f76`, exit 0.)*

### 3.2 Counterexample (`c80152b8a6f4877ea7a8c6c909c29fa2110ca1fa`): post-freeze pin edits and pre-freeze `runs.tsv` timestamps evade all three gates (`observation`)

To test whether the automated gates actually enforce post-freeze pin immutability and `runs.tsv` timestamp ordering, we cloned the lane into `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticFreezeAfter/clone-ce` at `92b1dd2ddc119fda89a611ba515bdf6cfe906f76` and created sandbox commit `c80152b8a6f4877ea7a8c6c909c29fa2110ca1fa` (2026-10-23T03:16:13Z) making four simultaneous violations without any `instrument_supersessions` entry:
1. Appended `# post-freeze tampering test` to `tools/round-30/rust_dep_oracle.py` (pinned under `instruments`).
2. Appended `# post-freeze tampering test` to `corpus/evidence/round-30/c1/carriers.tsv` (pinned under `frozen_inputs`).
3. Appended `# post-freeze tampering test` to `corpus/evidence/round-30/c2/predictions.tsv` (pinned under `frozen_inputs`).
4. Rewrote every `utc_start` / `utc_end` in `corpus/evidence/round-30/c1/runs.tsv` and `c2/runs.tsv` from `02:59–03:01Z` to `2026-10-23T02:30:xx+00:00` (5 minutes **before** the freeze `4ee65c67` and 29 minutes **before** `f39f4530`).

Running all three gates against `--rev c80152b8a6f4877ea7a8c6c909c29fa2110ca1fa` (2026-10-23T03:16:13Z, `gate-blindspot-counterexample.json`):
- `prefreeze-gate.py --root clone-ce --round 30 --rev c80152b8…` → `pins=6 present=6 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0` / `verdict=CLEAN` (**exit 0**).
- `tools/round-29/freeze-gate.py --root clone-ce --rev c80152b8…` → round-30 entry has `"findings": []`, `"instruments": ["tools/round-30/c1-rust-positive.py", "tools/round-30/c2-rust-refusals.py"]`, `"verdict": "CLEAN"` (**exit 0**).
- `axis-fit-gate.py --root clone-ce --round 30 --rev c80152b8…` → `"findings": []`, `"verdict": "PASS"` (**exit 0**).

**Why all three gates missed the counterexample (`observation`):**
1. `tools/round-30/prefreeze-gate.py:191-203` checks `blob_sha256(root, freeze, path)` only at `freeze`, never at `measured` (`--rev`).
2. `tools/round-29/freeze-gate.py:116-136` checks `git rev-list --reverse freeze..measured -- path` (`INSTRUMENT_REVISED`) only for script paths matched by `SCRIPT` regex inside `claims[]` strings (`c1-rust-positive.py`, `c2-rust-refusals.py`), ignoring `tools/round-30/rust_dep_oracle.py` (which is in top-level `instruments`/`loaded_by_counter`, not in `claims[]` strings) and all `frozen_inputs` (`carriers.tsv`, `pypi-uv-0.13.0.json`, `predictions.tsv`).
3. Neither `prefreeze-gate.py`, `axis-fit-gate.py`, nor the counters parse `runs.tsv` `utc_start`. Moreover, `axis-fit-gate.py:92-99` uses `first_add` (`--diff-filter=A`, returning `004053d6` at `1792724348`) rather than the last commit touching `controls/receipts.tsv` (`f39f4530` at `1792724362`); in round 30 both commits precede `runs.tsv` (`1792724373`) and `24da3459` (`1792724660`), so round-30's ordering holds, but a post-data edit to `receipts.tsv` would not be flagged by `axis-fit-gate.py`.

---

## Impacted Axes and Smallest Safe Correction

- **Impacted axes:**
  - Round-30 `coverage` (R30-C1) and `depth` (R30-C2) claim admissibility: **unharmed (HOLDS)** — direct Git object diffs, SHA-256 checks, and `runs.tsv` timestamp comparisons confirm no post-freeze instrument/input change at measurement time and no pre-control claim data.
  - Governance / verifier gate completeness (`tools/round-30/prefreeze-gate.py`, `tools/round-30/axis-fit-gate.py`): **fixable tool blind spots**.
- **Smallest safe correction (for a future gate revision; do not edit frozen round-30 counters):**
  1. In `tools/round-30/prefreeze-gate.py`, for every `path` in `pins`, also check `blob_sha256(root, measured, path) != at_freeze` (unless `path` is in `superseded`) and emit `PIN_REVISED`.
  2. In `tools/round-30/axis-fit-gate.py`, compare both `first_add` and `last_touch` (`git log -1 --format='%H %ct' rev -- .ufo/waves/round-<N>/controls/receipts.tsv`) against `first_envelope_add` and against the minimum `utc_start` parsed from `corpus/evidence/round-<N>/*/runs.tsv`.

---

## Tooling and Retained Scratch Artifacts

- **Tooling installs/updates:** None performed.
- **Scratch artifacts under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticFreezeAfter/` (`sha256sum`, 2026-10-23T03:17:04Z, exit 0):**
  - `296f55b831b685791341f5cbfbe336555bef4804f53897257249cfcd35315810`  `audit_freeze_after.py`
  - `8b561beb442addec85230fd217a912a25bf368deabd5bf9512c58013a911cef6`  `audit_freeze_after.json`
  - `32726fddeaf27129f91626b61cd7adf9a6552855f7956d7f1273db1b8dc506a9`  `gate-blindspot-counterexample.json`
  *(Temporary sandbox clone `clone-ce/` was deleted upon script completion; no background processes remain.)*

Report: .ufo/waves/round-30/w2/CriticFreezeAfter.md
