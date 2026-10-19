# RV-5 — seat report (chain c2, reviewer seat, LATE JOIN) — wave `arc3-loop1-round3`

Seat RV-5 · chain c2 · role reviewer · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
· HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (unchanged; no git mutation, no write
to any real target, no write to LOG/SCORECARD/SHONEN/corpus/SKILL/README).

Task: code-review the four closures in the revised custody tool (D2, D3, write-guard
scope, D6), each fix correct, each declared class reachable, no regression; compare
against the round-2 named debt (D2/D3/guard/D6).

**Verdict: all four closures CONFIRMED CORRECT and load-bearing on the landed revision
`7cd19c3c…`; every declared class reachable; no regression found; one test-coverage
hole found in the D6 case (fix proposed) and two precision gaps confirmed
(cross-referenced to CR-4 / RV-7, not re-proposed).**

Disposition: **COMPLETED the missing work** (this seat report — the only RV-5
deliverable absent; plus an independent battery, mutation matrix and precision probes
under `claims/c2/RV-5/late-join/`) and **VERIFIED the existing work** (the four
pre-interruption artifact sets in `claims/c2/RV-5/` — re-run and re-derived, not
trusted).

## 1. Work performed (evidence pointers)

All scratch under `/var/tmp/rv5-late/` (never `/tmp`). Custody paths read-only
(sha256/stat capture only); the clobber and sidecar demos ran on scratch fixtures.
The landed tool and README were read-only for this seat.

**Instrument under review (re-derived at run time, twice):**
`.ufo/gates/custody-pair/custody-pair.py` sha256
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (54,279 B, 1,155
lines, mtime `2026-10-19 10:13:20 −03:00`); `README.md` sha256
`f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` (9,603 B, 185
lines). Prior revision (round-2, still at HEAD): `112d01dc…`. Both match the
implementer's own manifest (`claims/c2/EX-21/sha256s.txt`) and the receipt self-pins.

**What existed when I joined** (pre-interruption, verified present and re-run):
`before-112d01dc/` (D2/D3/guard/D6 reproduced on the round-2 revision, incl. the
fail-open `MATCH exit 0`, the `PermissionError` traceback at `:219`/`:593`, the
`--out X --paths X` clobber, the D6 traceback at `:630`), `after-03bd6242/` and
`final-7cd19c3c/` batteries, `attack-89bfebec/` + `attack-final-7cd19c3c/` (guard,
D2, D3, D6, cross-version, command A), `sabotage-7cd19c3c/`, and the three
`revision-snapshots/`. **Missing: this seat report.**

**What I completed:**

| artifact | what |
|---|---|
| `seats/RV-5.md` | this report (was missing) |
| `late-join/battery.sh` + `battery.log` | my own independent battery (9 sections, ~90 commands) at the landed revision |
| `late-join/mutate.py` + `mutation-matrix.log` | 8-mutant revert matrix (incl. the S3 diagnosis) |
| `late-join/precision.sh` + `precision.log` | two precision attacks on the new closures (gate counting, sidecar scope) |
| `proposed-d6-test-hardening.patch.md` + `.patched.py` | patch text: makes the D6 case load-bearing (with proof) |

Rule-#14: every identity below was re-derived in the run that produced it; nothing is
quoted from another seat without a first-hand re-run.

## 2. Proposed changes (patch-text paths)

1. **`claims/c2/RV-5/proposed-d6-test-hardening.patch.md`** (sha256 `df53cee4…`) +
   drop-in copy `proposed-d6-test-hardening.patched.py` (sha256 `d47e4fd5…`). Test-only
   (22 cases, no count change, no production-code change): makes
   `selftest-missing-scratch-usage-exit` assert the **declared message** per arm and
   that the in-process arm hits the explicit `is_dir` guard, so the D6 closure becomes
   load-bearing under a single-line revert like every other landed closure. Proof in
   the file: patched copy CLEAN 22/22; patched+guard-reverted → DIRTY exit 3 failing
   exactly that case.
2. Everything else: **none**. The two precision gaps I measured (sidecar write path;
   D3 stanza-count vs distinct-path) are already proposed by siblings — CR-4 §1
   (`proposed-write-guard.patch.md`) and RV-7 §2 (`rv7-proposed-coverage-gate.patch.md`)
   respectively. I reproduced both independently and cross-reference them rather than
   duplicating patch text.
3. **Flag for the parent (tool change, not a test change):** `selftest --scratch
   <symlink-to-/tmp>` runs fixtures under `/tmp` — the `/tmp` exclusion is a literal
   string-prefix check on the unresolved path (`:722-725`), before `base.is_dir()`.
   Measured first-hand: exit 0, `scratch: .../tmp-link/custody-pair-selftest-5rwrnovd`,
   and that directory created under `/tmp` (removed after measuring). Contradicts
   README.md's "requires an existing, non-`/tmp` directory" and defeats the EDQUOT
   hazard the guard exists for. Needs a resolved-path check; the implementer's call.

## 3. Before → after measurement for the chain's claim

The claim's falsifiable core (`claims-frozen.md` C2): four injections reproduce as their
declared classes; selftest 15 → ≥17 at exit 0; live pair MATCH 5/5; command A unchanged.
Each row below is my own re-run; `before` = round-2 `112d01dc` (snapshot re-run by me),
`after` = landed `7cd19c3c`.

| # | injection (round-2 named debt) | before | after | declared class reached |
|---|---|---|---|---|
| D2a | exists-but-EACCES parent dir, capture + `verify --live` + receipt-vs-receipt | capture `PARTIAL paths=0/1 exit 13`; verify **`MATCH exit 0` compared=0/11 (fail-open)** | capture `UNEVALUABLE paths=0/1 exit 14`; verify `UNEVALUABLE compared=0/11 exit 14`; receipt records `EXISTS: yes`+`STAT-ERROR` | **14 UNEVALUABLE** ✔ no fail-open |
| D2b | chmod-000 file | `PermissionError` traceback, exit 1, **no receipt** | capture `UNEVALUABLE paths=1/1 exit 14` with `READ-ERROR:` in the receipt | 14 ✔ |
| D2c | readable receipt, candidate turns unreadable | traceback at `:593`→`:219`, exit 1 | `UNEVALUABLE ... exit 14`, note "on candidate side" | 14 ✔ |
| D2-ref | unreadable **reference** side | — | `UNEVALUABLE ... exit 14` ("reference side") | 14 ✔ (both directions) |
| D2-ctl | genuinely absent path / delete-after-capture | `PARTIAL 13` / `MATCH` | `PARTIAL 13` / `ABSENT exit 13` | 13 ✔ (ENOENT not conflated) |
| D3 | 1-of-5 reference vs live | `MATCH 1/1 exit 0`, four paths unexamined | default still `MATCH 1/1 exit 0` (declared opt-in); `--require-paths 5` → `REFERENCE-COVERAGE: 1/5 … unaccounted: <5>` + `USAGE exit 2`; control canonical 5-of-5 + flag → `MATCH 5/5 exit 0` | **2 USAGE** ✔ gate reachable, default unchanged |
| guard | `--out X --paths X` clobber | clobbers, exit 0 (sha changed) | refused, `USAGE exit 2`, sha **identical before/after** | 2 ✔ |
| guard | relative form `./rel.conf`, symlink alias, hardlink alias, canonical custody path | (round-2: canonical 5 guarded only) | all refused, exit 2; fresh non-guarded `--out` still writes (no false positive) | 2 ✔ |
| D6 | `selftest --scratch <missing>` | `FileNotFoundError` traceback at `:630`, exit 1 | `USAGE: scratch base is not a directory: …`, exit 2, no traceback | **2 USAGE** ✔ |
| D6 | scratch = existing file / `/tmp` / symlink-to-missing / read-only dir | — | file→2, `/tmp`→2 (`/tmp is excluded scratch`), symlink-to-missing→2, read-only→2 (`cannot create a fixture root …`); valid scratch → CLEAN 22/22 | 2 ✔ |

**Claim numbers (re-derived):** selftest `cases=15 passed=15 exit 0` (before) →
`cases=22 passed=22 failed=0 exit 0` (after) — 15 → **22**, exceeding the ≥17 floor.
Live pair: `verify config-pre-pair-v2r3-revised.txt config-post-pair-v2r3.txt` →
`MATCH 5/5 drift=0 exit 0`, also with `--require-paths 5`; both receipts self-pin
`# tool: custody-pair.py sha256 7cd19c3c…` (re-derived), sidecars match; the round-start
receipt (captured by the *previous* revision `112d01dc`) vs the revised post receipt →
`MATCH 5/5 exit 0`; round-2 `EX-31/capture-pre.txt` vs round-3 post → **`CONTENT-DRIFT
exit 10` on `~/.kimi-code/config.toml` only** (see residual R2 — this is *correct*
behaviour, not a regression). Command A at HEAD: `knowledge_files 82, mapped 82,
missing [], dangling [], rules 14/14` — unchanged. Exit-map sweep over my whole
battery: only `0, 2, 10, 11, 12, 13, 14` — **no exit outside the declared map, zero
tracebacks** (before-state had exit 1 tracebacks in two shapes).

## 4. Attacks / refutations attempted, with verdicts

1. **"The D2 closure is verify-side only / the capture side is dead code."** Refuted by
   containment: reverting only the 8-line verify guard (`:485-492`) restores the
   fail-open `MATCH exit 0` while capture stays closed (my `M1`; RV-6 measured the same
   on the landed bytes and, independently, on EX-40's patched variant). The guard keys
   on recorded `STAT-ERROR`/`READ-ERROR`, not on `exists=no` — proven by the absent-path
   control staying `MATCH`/`ABSENT`. *Verdict: correct, load-bearing, correctly scoped.*
2. **"The parser cannot see a v2 receipt's error keys, so a receipt-vs-receipt compare
   stays fail-open."** Refuted: my `M1b` (drop `"stat_error","read_error"` from
   `_parse_section`'s key list) makes exactly
   `parsed-unevaluable-reference-never-matches` fail. The landed parser reads both keys
   and the parsed-receipt path is exercised (`parsed-hidden.txt` vs `parsed-open.txt` →
   `UNEVALUABLE exit 14`). *Verdict: closed on both paths.*
3. **"The write guard is over-broad (false positives) or under-broad."** Over-broad:
   refuted — a fresh, unrelated `--out` writes normally (`C5-false-positive` / `D6`).
   Under-broad: **partially confirmed**. Refuted for the shapes the claim names
   (`--out X --paths X` by path, relative form, symlink alias, hardlink alias, canonical
   custody paths — all refused, target sha unchanged). **Confirmed for one shape not in
   the claim's wording**: the derived sidecar path is unguarded, so `--paths X.sha256
   --out X` overwrites `X.sha256` at exit 0 (measured on a scratch victim, sha changed;
   also visible in `D8`). Same defect as CR-4 §1 — cross-referenced, patch text exists
   there. *Verdict: guard correct for `set(paths) ∪ CUSTODY_PATHS` as claimed; the
   sidecar escape is a residual, not a claim breach.*
4. **"The D3 gate is satisfied by a degenerate reference."** **Confirmed (independent
   reproduction of RV-7 §2).** `reference_coverage` (`:591-599`) compares
   `len(ref_sections) >= required` — a stanza count, while the printed `unaccounted`
   list is computed from distinct resolved paths. A 5-stanza single-path reference
   passes `--require-paths 5` at `exit 0` (`MATCH paths=1`) while printing all five
   canonical paths as unaccounted. `--require-paths 0`/`-1` = no gate (falsy, as
   documented); non-integer → argparse exit 2. *Verdict: the gate closes the *named*
   debt D3 (a 1-of-5 receipt no longer reads exit 0 under the flag); the count-vs-
   distinct-path incoherence is a real residual with RV-7's patch text.*
5. **"The D6 fix is load-bearing."** **Partially refuted — the finding of this seat.**
   The landed D6 case is PASS in both the landed tool and in a mutant with the explicit
   `is_dir` guard reverted (`M3`: CLEAN 22/22) — because the mkdtemp `except OSError`
   still yields USAGE 2, and the case asserts only exit code + absence of "Traceback".
   Only reverting **both** layers (`M3b`) makes the case fail. Behaviour: still closed
   (two layers, either alone suffices; both messages declared). Test: not load-bearing
   against a single-line revert, unlike every other closure. *Verdict: fix correct;
   test coverage hole — patch text provided (proposed changes §1).*
6. **"`--require-paths` is cosmetic / the gate would break the declared default."**
   Refuted both ways: `M4` (gate disabled) fails exactly
   `partial-reference-require-paths-gate`; and the default path is unchanged
   (`1/1 MATCH exit 0` without the flag — declared opt-in in README and docstring).
   *Verdict: gate load-bearing and default-preserving.*
7. **"The guard extension broke the canonical arm / a reverted guard could clobber a
   real custody path."** Refuted: all my guard arms (including the mutant runs) refuse
   the canonical path with `~/.bashrc` sha256 `7d2ca28a…` unchanged before and after;
   the canonical five were already guarded pre-revision. No real custody path was ever
   at risk in this seat's work. *Verdict: safe; matches RV-7's canonical-scope control.*
8. **"No regression outside the four closures."** Refuted as a concern: same-content
   in-place rewrite → `REWRITE-DRIFT exit 11` (ctime pin); rename rewrite → `exit 11`
   (inode pin); content drift → `exit 10`; absent → `exit 13`; mode drift → `exit 12`;
   UTC render TZ-independent (`TZ=UTC-3` vs `TZ=Asia/Tokyo` identical,
   local render separate); three v1 shapes → `MATCH-V1-PARTIAL 0` / `METADATA-DRIFT 12`
   with `LABEL-DEFECT` named; unparsable → `USAGE 2`; empty receipt → `USAGE 2`.
   *Verdict: no regression.*
9. **"The D2 class is reachable but unreachable in practice (root-only)."** Checked:
   the cases self-skip under `os.geteuid() == 0`; this host runs as uid 1000 and every
   arm fired first-hand (exit 14, messages as declared). *Verdict: reachable and
   measured, not merely declared.*
10. **"RV-5's own pre-interruption verdicts were stale (measured on a superseded
    revision)."** Refuted: `final-7cd19c3c/` and `attack-final-7cd19c3c/` pin the landed
    sha256 in their headers and match my re-runs; `after-03bd6242/` pins an intermediate
    revision (superseded — its D2/D3/guard/D6 results are identical to the landed ones,
    which is itself evidence the closures did not churn between those revisions).
    *Verdict: artifacts valid; the only gap was the missing report.*

## 5. Blockers, if any

None. `/var/tmp` had ample space; `/tmp` never used except the deliberate
symlink-to-`/tmp` probe (its fixture dir removed after measuring). The landed tool,
README, registry patch, custody paths and all wave artifacts were read-only for this
seat. The two residuals (sidecar escape, D3 stanza count) and the `/tmp`-symlink flag
do not block the c2 claim as frozen: the claim names `set(paths) ∪ CUSTODY_PATHS` and
the four injections, all of which hold as declared.

## 6. Residuals carried forward (measured here; none voids the claim)

- **R1 — sidecar write path unguarded** (`:657`, `sidecar = out.with_name(out.name +
  ".sha256")` written outside the guarded block). Reproduced: `--paths X.sha256 --out X`
  → exit 0, `X.sha256` overwritten (scratch victim). Patch text: CR-4 §1.
- **R2 — `~/.kimi-code/config.toml` operator drift** (not a defect): sha256
  `8cbacd48…` (round-1 pin) → `bc66d543…` (round-3, live now, mtime epoch `1792414665`
  = `2026-10-19T12:57:45Z`, i.e. 9 min before the round's first capture); every other
  custody path byte-identical to its round-1 pin (`16f496e6…`, `38d2a1d0…`, `7d2ca28a…`,
  `6c6be761…`). The round's own pair is same-revision (both sides `bc66d543…`) →
  `MATCH 5/5`; the cross-round compare correctly reports `CONTENT-DRIFT` on that one
  path. Records should name the drift rather than read the cross-round `exit 10` as a
  failure.
- **R3 — D3 gate counts stanzas, not distinct covered paths** (R1 above; RV-7 §2).
- **R4 — `/tmp` exclusion is an unresolved string-prefix check**; a symlink-to-`/tmp`
  scratch runs fixtures under `/tmp` (measured; `__pycache__` risk and EDQUOT hazard).
- **R5 — D6 test case not load-bearing under a single-line revert** (patch text in
  proposed changes §1). Behaviour unaffected; two independent layers close it.
- **R6 — revision-churn caveat for the record** (round-2 D8 shape, re-confirmed):
  `config-pre-pair-v2r3.txt` self-pins the superseded `112d01dc…`; the authoritative
  same-revision pair is `config-pre-pair-v2r3-revised.txt` + `config-post-pair-v2r3.txt`
  (both `7cd19c3c…`). EX-21's own pair (`config-{pre,post}-pair-ex21.txt`) also
  self-pins the landed revision. Payloads are byte-identical across all of them
  (5/5 sha256 equal, re-derived), so comparability holds.

**Files touched by this seat:** `.ufo/waves/arc3-loop1-round3/seats/RV-5.md` (new);
`.ufo/waves/arc3-loop1-round3/claims/c2/RV-5/late-join/` (6 new files);
`.ufo/waves/arc3-loop1-round3/claims/c2/RV-5/proposed-d6-test-hardening.patch.md` and
`proposed-d6-test-hardening.patched.py` (new). Nothing else.

Landing notes for the parent: (a) `.ufo/gates/custody-pair/__pycache__/
custody-pair.cpython-314.pyc` is untracked and pre-existed this seat; one import-time
refresh at 10:27Z (from a module-load probe with `PYTHONDONTWRITEBYTECODE` unset) —
exclude it from the wave commit as usual (round-2 D9). (b) Self-identity: any sha256 this report prints for itself is invalidated by the
write that prints it (a fixed point), so none is asserted here — the parent
re-derives `seats/RV-5.md` at landing per rule #14. The identities that are
asserted are the ones re-derived after all my writes: the landed tool and README
were re-hashed after all my writes and are unchanged (`7cd19c3c…` / `f30df42e…`),
i.e. this seat wrote no byte of the real target. (c) `git status --porcelain` is
otherwise identical to the wave-start state; HEAD still `c07af80`.
