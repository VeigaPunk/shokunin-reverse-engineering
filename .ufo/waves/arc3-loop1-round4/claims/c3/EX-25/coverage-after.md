# EX-25 — coverage-after: the duplicate-stanza 5-path reference (chain c3, wave arc3-loop1-round4)

Seat EX-25 · chain c3 · role executor · 2026-10-19.
Task: **after-state** — a duplicate-stanza 5-path reference is caught by
**distinct-path counting**, and the single-stanza 5-path control still passes.

Artifact status: **AFTER MEASURED** — EX-21 landed the revised tool at
2026-10-19T14:09:25Z (`.ufo/gates/custody-pair/custody-pair.py` sha256
`7cd19c3c…` → `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`,
65,902 B, 1343 lines). Every column below is measured; the real custody target
was **read-only for this seat** (sha256/stat only) and is copied to
`tools/tool-after-29bb45ae.py` for re-verification.

## 0. Instruments, revisions, method

| item | value |
|---|---|
| BEFORE revision (frozen baseline) | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (54,279 B, 1155 lines, mtime 2026-10-19 10:13:20 -03) — the r3 landed tool |
| **AFTER revision (the landing)** | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (65,902 B, 1343 lines, mtime 2026-10-19 11:09:25 -03 = 14:09:25Z); re-hashed unchanged at 14:09:52Z and at the end of the matrix (`logs/`), i.e. stable across the whole measurement window |
| tool copies under test | `tools/tool-baseline-7cd19c3c.py`, `tools/tool-after-29bb45ae.py` (both byte-identical to their sources) |
| PREDICTION revision | `63e67631f6dd5be2730823040181c409011f93347a9fc3047a16a9706df581bb` — the frozen baseline with EX-24's r3 patch text (`arc3-loop1-round3/claims/c2/EX-24/proposed-coverage-count.patch.md`) applied to a **scratch copy**. Retained because the landed fix agrees with it on every leg. |
| harness | `harness/run-matrix.py` (17 legs), `harness/attacks.py` (12 attacks), `harness/build-fixtures.py` + `build-fixtures2.py` (fixture builders) |
| scratch | `/var/tmp/ex25-r4/` only; custody paths read-only (capture = sha256+stat) |
| determinism | `attacks.py` re-run byte-identical in both the before and after phases; `run-matrix.py after` re-run identical |

The landed fix introduces a named helper and states the basis in the tool's own
contract header: `distinct_paths()` returns
`{Path(s["path"]).expanduser().resolve() for s in sections}`, and
`reference_coverage()` plus the USAGE line both use it
(`custody-pair.py:637-651`, `:750-756`). That is the same basis as the
prediction — so the prediction column doubles as an independent reproduction of
the landed behaviour by different bytes.

Fixture provenance: every stanza is produced by the **tool's own renderer**
(`build-fixtures.py` imports the baseline copy and calls `capture_path` /
`render_receipt`); only the *padding* is synthetic (repeating a stanza the tool
itself emitted). The hardlink and spelling-alias vectors are built by
`build-fixtures2.py` and consumed read-only so their bytes are identical in
every phase.

## 1. The seat's claim — BEFORE → PREDICTION → AFTER

The claim's two halves, one leg each:

| leg | vector | BEFORE `7cd19c3c` | PREDICTION `63e67631` | **AFTER `29bb45ae` (landed)** |
|---|---|---|---|---|
| **V1** | `verify dupe5-one-path-pre.txt --live --require-paths 5` — **5 duplicate stanzas for ONE path** (header keeps the honest `# paths: 5 present: 5`) | **exit 0**, `VERDICT: MATCH paths=1`, four custody paths unexamined, **0 `REFERENCE-COVERAGE` lines** (padding defeats the gate) | **exit 2**, `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile`; stderr `USAGE: reference covers 1 of the required 5 paths` | **exit 2** — identical line; stderr reads `USAGE: reference covers 1 of the required 5 distinct paths` (the landing names the unit in the USAGE text too) |
| **V2** | `verify custody5-distinct-pre.txt --live --require-paths 5` — **single stanza per path, the 5 real custody paths** | **exit 0**, `MATCH paths=5/5`, `SHA256-CONTRACT: 5/5` | unchanged **exit 0**, `MATCH paths=5/5` (no false positive) | **exit 0**, `VERDICT: MATCH paths=5 MATCH=5 exit=0`, `SHA256-CONTRACT: 5/5` — the control still passes |

Both halves of the seat's claim hold on the landed bytes: the padded reference
is caught, the single-stanza control is untouched. The count and the
`unaccounted:` list share one basis (`distinct_paths()`), which is exactly the
r3 residual R2 (`arc3-loop1-round3/claims/c2/EX-24/coverage-after.md` §3).

### Padding variants (the same root cause, four shapes)

| leg | vector | BEFORE | PREDICTION | **AFTER** |
|---|---|---|---|---|
| V3 | `dupe4plus1-pre.txt` — 4 distinct custody stanzas + 1 duplicate, `--require-paths 5` | exit 0 (4-of-5 masked by the padding) | **exit 2**, `REFERENCE-COVERAGE: 4/5 … unaccounted: ~/.profile` | **exit 2**, same line |
| V4 | `symlink-alias-5stanzas-pre.txt` — 5 stanzas, two symlink aliases resolving to one file (4 distinct) | exit 0 | **exit 2**, `4/5 … unaccounted: <all five canonical>` | **exit 2**, same line |
| V5 | `v1-dupe5-one-path-pre.txt` — v1 **sums** shape, 5 rows / 1 path | exit 0 | **exit 2**, `1/5 …` | **exit 2**, same line |
| V11 | `custody5-distinct-pre.txt --require-paths 6` — threshold above the reference | exit 2, `5/6 …` (identical) | exit 2, `5/6 …` | exit 2, `5/6 …` (unchanged) |

### Controls held on both revisions (no collateral change)

| leg | vector | BEFORE | PREDICTION | **AFTER** |
|---|---|---|---|---|
| V6 | 1-of-5 reference, `--require-paths 5` (the r3 D3 leg) | exit 2, `REFERENCE-COVERAGE: 1/5 …` | identical | identical |
| V7 | 1-of-5 reference, `--require-paths 1` | exit 0 | identical | identical |
| V8 | padded reference, `--require-paths 1` | exit 0 | identical | identical |
| V10 | v1 **sums**, 5 distinct paths, `--require-paths 5` | exit 0 | identical | identical |
| V12/V13 | padded / canonical reference **without** the flag (declared opt-in) | exit 0 | identical | identical |
| V14 | the r3 **real** receipt pair `verify pre post --require-paths 5` | exit 0, `MATCH 5/5` | identical | **exit 0, `MATCH 5/5`** — the real artifacts are unaffected |
| V16 | `selftest` | `CLEAN cases=22 passed=22 failed=0` | `CLEAN cases=22` | **`CLEAN cases=28 passed=28 failed=0 exit=0`** — the landing added 6 cases, two of them the coverage pair below |
| V17 | `paths` | the 5 canonical paths | identical | identical |

Adjudicator `harness/run-matrix.py` (13 checks): **BEFORE 9 pass / 4 fail**
(C1, C3, C4, C5 — exactly the four padding vectors); **PREDICTION 13 pass / 0
fail**; **AFTER 13 pass / 0 fail**.

### Sabotage arm on the landed revision (is the new selftest case load-bearing?)

| arm | change | selftest |
|---|---|---|
| landed bytes | — | `CLEAN cases=28 passed=28 failed=0` |
| `tools/sabotage-cov.py` | `reference_coverage()` back to the stanza basis (`have = [s for s in ref_sections]`) | **`DIRTY 27/28 failed=1`** — `coverage-gate-rejects-duplicate-stanzas` **FAIL** ("expected USAGE exit 2 on 5 duplicate stanzas, got 0"), while `coverage-gate-passes-distinct-five` still PASS |
| `tools/sabotage-cov2.py` | `distinct_paths()` returns a **list** (stanza multiplicity leaks back through `len()`) | same single failure |

So the new case fails exactly when the fix is reverted, and the paired control
does not fail with it — the case is load-bearing and not over-broad.

## 2. Attacks attempted, with verdicts

Run by `harness/attacks.py`; verbatim output in `out/<phase>/attacks.out`.

| # | attack | BEFORE | PREDICTION | **AFTER** | verdict |
|---|---|---|---|---|---|
| A1/A2 | **hardlink**: 5 names, **one inode** — a `--paths`-scoped receipt built by the tool itself | exit 0 (no coverage line) | **exit 0** (no coverage line) | **exit 0** (no coverage line) | **CONFIRMED residual of the fix** — the fix counts distinct *resolved path names*, not distinct *files*; 5 hardlink names still satisfy `--require-paths 5`. The fix is not worse than the baseline here (both pass) and it is not in the r3 patch text's letter (which says "distinct resolved paths"); filed as a named residual (§3 R4). |
| A3 | **spelling aliases**: 5 lexical spellings of one path (`~/.bashrc`, `/home/vgpnk/.bashrc`, `/home/vgpnk/./.bashrc`, `/home/vgpnk/../vgpnk/.bashrc`, `/home/vgpnk//.bashrc`) | exit 13 (`ABSENT=3 MATCH=2` — raw-string keying in `verify_sets`) | **exit 2**, `1/5 …` | **exit 2**, `1/5 …` | **fix improves it** — the gate now catches the padding. Note the exit-13 shape is a *separate* raw-string-vs-resolved keying in `verify_sets` (pre-existing, unchanged by the fix). |
| A4 | **duplicate with an unevaluable copy**: 5 stanzas of one path, the 2nd carrying `READ-ERROR` | exit 0 (`MATCH`) | **exit 2**, `1/5 …` | **exit 2**, `1/5 …` | **fix improves it.** Pre-existing last-wins masking in `verify_sets` (`ref_by = {s["path"]: s …}`, duplicate keys collapse) is unchanged: with the bad stanza **last** the tool reads exit 14, with it **second** exit 0 — identical on all three revisions (`dupe5-bad-last`/`dupe5-bad-second`). Named residual R5. |
| A5 | **4 canonical + 1 extra path** (5 distinct) | exit 0 | exit 0 | exit 0 | **CONFIRMED residual (r3 R3, declared)** — the gate is a *count*, not a canonical-set identity check; a fifth unrelated path satisfies it. The patch text's optional identity gate would close it; not in the frozen claim's letter. |
| A6 | **padded receipt whose one path drifted** (sha256 zeroed) under the gate | exit 10 (`CONTENT-DRIFT`) | **exit 2** (coverage refusal) | **exit 2** | **fail-closed order confirmed** — the coverage refusal pre-empts the drift report; the drift is still reported when the flag is absent (A7 exit 10 on all revisions). Benign: the refusal is the fail-closed direction. |
| A8/A9 | `--require-paths 0` / `-1` | exit 0 (falsy = no gate) | exit 0 (unchanged) | exit 0 (unchanged) | **no change** — the truthiness guard is untouched. |
| A10/A11 | `dupe4plus1` at `--require-paths 4` / `5` | exit 0 / **exit 0 (the hole)** | exit 0 / **exit 2** | exit 0 / **exit 2** | **the fix's exact boundary**: 4 distinct satisfies 4, and no longer satisfies 5. |
| A12 | symlink-alias pair | exit 0 | exit 2 | exit 2 | see V4. |
| — | **SC-3's independent harness** (`arc3-loop1-round4/claims/c3/SC-3/harness/injections.sh`) run by this seat on all three revisions | c3 rc=0, c5 (v1 sums) rc=0, c7 (distinct-5 control) rc=0 | c3 rc=2, c5 rc=2, c7 rc=0 | c3 rc=2, c5 rc=2, c7 rc=0; a1 0→**2**, b1 **1**→**2** | **cross-confirmed** by a harness written independently of mine (`out/sc3-<phase>/`, full `.rc` table in §4). SC-3's a1/b1 legs move too because the same landing carries the sidecar-scope and mkdir-guard fixes (EX-23's / EX-24's targets) — not this seat's claim, recorded for the parent. |

## 3. Residuals (measured)

- **R1 — the gate is opt-in** (r3 R1, unchanged). Flag-absent 1-of-5 or padded
  reference reads `MATCH exit=0`; declared in the README. The landing does not
  change this and does not claim to (V12/V13, A7: identical on all revisions).
- **R2 — the count/stanza unit** — this seat's target. **CLOSED on the landed
  revision**: BEFORE 4/4 padding vectors pass the gate → AFTER 4/4 caught
  (V1, V3, V4, V5), controls held (V2, V6-V10, V12-V14). The landing names the
  basis in the tool contract header, the README, and the USAGE text.
- **R3 — count, not canonical-set identity** (r3 R3, unchanged). 5 unrelated
  paths still satisfy `--require-paths 5` (A5, all three revisions). Declared;
  the r3 patch text offers an optional `--require-custody-set` identity gate.
- **R4 — distinct *names*, not distinct *files*** (new, this seat; **still
  open on the landed revision**). 5 hardlink names for one inode pass
  `--require-paths 5` (A1/A2: exit 0 on all three revisions). The landed basis
  is `Path(...).resolve()`, which collapses spelling and symlinks but **not
  hardlinks**; `distinct_paths()` is explicitly documented as "distinct RESOLVED
  paths", so the code matches its declared unit — the *unit* is the weak point.
  Filed as a patch-text addendum (`proposed-hardlink-inode-key.patch.md`), not
  claimed as part of the frozen claim.
- **R5 — duplicate-stanza last-wins masking in `verify_sets`** (new, this seat;
  pre-existing, NOT introduced by the fix; **still open on the landed
  revision**). The reference is keyed by raw path string; with duplicates, the
  **last** stanza wins. Measured: 5 copies of one path with the bad copy last →
  `UNEVALUABLE exit 14`; with it second → `MATCH exit 0` (all three revisions).
  The gate now catches the *count*, so a padded reference is refused before
  comparison when the flag is passed; the masking itself remains for flag-absent
  runs. Filed as a patch-text addendum (`proposed-verify-key-resolved.patch.md`).
- **Observation (not this seat's claim).** The same landing also carries the
  sidecar-scope and mkdir-guard fixes (EX-23's / EX-24's targets): SC-3's a1 leg
  moves 0 → 2 and its b1 leg moves 1 (traceback) → 2 (USAGE). Verified by this
  seat only as a by-product of running SC-3's harness; not measured further here.
- **Observation — README churn during the window.** `README.md` sha256 moved
  `f30df42e…` (r3) → `125e7e0225…` at the landing (14:09Z) → `9d9400dab7…`
  (15,293 B) at 14:11:35Z — a second write by another seat (the (d) ruling text
  EX-26 carries). The tool itself did **not** move: it is still
  `29bb45ae…`/65,902 B at 14:12Z, and both headline legs re-run against the
  current target read V1 exit 2 / V2 exit 0, i.e. unchanged. The r3 note about
  the D3 wording ("fewer than N stanzas") is superseded: the landed README says
  "fewer than N **distinct resolved paths**". Neither README revision is this
  seat's write path; recorded for the parent's census.

## 4. Evidence index

- `out/before/`, `out/after/` — `matrix.out` (17 legs, verbatim), `checks.json` (13 criteria), `attacks.out` (12 attacks)
- `out/candidate/` — the same for the PREDICTION revision
- `out/sabotage/` — the two sabotage-arm selftest transcripts (`sabotage-cov`, `sabotage-cov2`)
- `out/sc3-before/`, `out/sc3-candidate/`, `out/sc3-after/` — SC-3's independent harness, run by this seat (full logs + `.rc` per leg). The exit-code table across all 16 legs:

| leg | before `7cd19c3c` | candidate `63e67631` | after `29bb45ae` |
|---|---|---|---|
| a1 sidecar-scope | 0 | 0 | **2** (the landing's sidecar fix) |
| b1 mkdir traceback | 1 | 1 | **2** (the landing's mkdir fix) |
| b2 empty --out | 2 | 2 | 2 |
| c0 1-path capture | 0 | 0 | 0 |
| c1 1-of-5 gated | 2 | 2 | 2 |
| c2 dupe5 capture | 0 | 0 | 0 |
| **c3 dupe5 gated** | **0** | **2** | **2** |
| c4 padded, no flag | 0 | 0 | 0 |
| **c5 v1-sums dupe** | **0** | **2** | **2** |
| c6 distinct-5 capture | 0 | 0 | 0 |
| c7 distinct-5 control | 0 | 0 | 0 |
| d1/d2/d3 both-absent | 13/0/0 | 13/0/0 | 13/0/0 |
| k1 selftest | 0 | 0 | 0 |
| k2 paths | 0 | 0 | 0 |

  On the coverage legs only c3 and c5 move; every other leg is unchanged except
  a1/b1, which move because the same landing carries the other two chains' fixes.
- `tools/` — `tool-baseline-7cd19c3c.py`, `tool-candidate-predicted-63e67631.py`, `tool-after-29bb45ae.py`, `sabotage-cov.py`, `sabotage-cov2.py`
- `fixtures/` — the 15 vectors + `fixtures/scratch/` payloads (incl. the hardlink set)
- `harness/` — `build-fixtures.py`, `build-fixtures2.py`, `run-matrix.py`, `attacks.py`
- `logs/` — `attacks-{before,candidate,after}.log`, `attacks-before-rerun.log`, `matrix-after-rerun.log` (determinism), `poll-landing.log` (the landing timeline), `identity-*.txt`
- `proposed-hardlink-inode-key.patch.md`, `proposed-verify-key-resolved.patch.md` — R4/R5 patch texts (patch text only; the target is EX-21's write path)
- `IDENTITY-after.txt` — re-derived sha256 of every evidence file (rule #14)

Identity (rule #14): re-derived after the last revision of this artifact — see
`IDENTITY-after.txt`. The real target was read-only throughout: its sha256 is
recorded at every phase boundary in `logs/poll-landing.log`.
