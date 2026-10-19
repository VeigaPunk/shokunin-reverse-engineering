# scratchguard-after.md — EX-26, chain c2 (executor), D6 after-state

**Seat task.** after-state: `selftest --scratch <missing dir>` → declared USAGE class
(no traceback). This artifact is the measurement of that after-state against the
revision the wave actually landed, plus the adversarial sweep around it.

**Verdict (short).** Closed at the landed revision, measured first-hand:
`selftest --scratch <missing dir>` exits **2** with a `USAGE: scratch base is not a
directory: …` line on stderr and **no traceback**, in all 11 bad-input probes I
constructed; the four good-input probes stay `CLEAN 22/22` exit 0. The landed
revision additionally closes two sibling exit-1 paths (`mkdtemp` `OSError`, and the
`--scratch /tmp/…` bypass) that the round-2 patch texts left open. Two residuals on
the same axis remain and are named in §6, one of them with a **fenced-by-mutation
gap** in the tool's own new selftest case.

---

## 1. Revision identity (rule #14 — re-derived at write time)

| role | sha256 | size | lines | mtime (local, -03) | D6 probe |
|---|---|---|---|---|---|
| before (round-2 landed) | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` | 39157 | 889 | 2026-10-19 09:05:19 | **exit 1 + traceback** |
| mid-edit catch 1 — `a8f81dcf` | `a8f81dcf…` (12-char in `evidence/poll.log`) | 42331 | 943 | 10:09:16 | exit 1 + traceback |
| mid-edit catch 2 — `89bfebec` | `89bfebec…` | 51937 | — | 10:12:44 | exit 2 (selftest DIRTY 20/21) |
| **after (verified, stable ≥ 60 s at write time)** | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 54279 | 1155 | 2026-10-19 10:13:20 | **exit 2, no traceback** |

Byte-exact snapshots of the measured revisions are in
`evidence/real-03bd6242-custody-pair.py` and `evidence/real-7cd19c3c-custody-pair.py`
(re-derived: `sha256sum` of each equals the row above; see `sha256sums.txt`).

**Churn chain observed** (`evidence/poll.log`, 60 s cadence, UTC; plus 10 s watches):
`1287c9d6` (13:08:52Z) → `d9be407d` (13:09:52Z) → `a8f81dcf` (13:09:16Z) →
`a991f976` → `08fb6833` (13:10:06Z) → `ec2b2d48` → `f2412aaa` → `57dffff1` →
`03bd6242` (13:11:16Z, stable ≥ 3 min, fully swept) → `89bfebec` (13:12:44Z) →
`7cd19c3c` (13:13:20Z, stable through 13:13:52Z and at write time).

Two mid-edit states were caught in the act and are recorded as **the round's
caught churn** (round-2 D8 precedent), not as shipped defects:

- `a8f81dcf` (10:09:16): the module docstring's "ROUND-3 HARDENING … 6. SCRATCH
  GUARD (round-2 debt D6) … declared USAGE exit 2" was already present while
  `cmd_selftest` had **no** guard — the D6 probe still tracebacked at exit 1 and the
  selftest was still 15 cases. Documentation claiming an unlanded guard is the
  rule-#14 / claim-integrity surface the parent should keep in view.
- `89bfebec` (10:12:44): selftest `DIRTY cases=21 passed=20 failed=1 exit=3`,
  `case require-paths-blocks-partial-reference FAIL (TypeError: _run_verify() got an
  unexpected keyword argument 'require_paths')`. Same class as round-2's transient
  `KeyError: 'sha_agree'`. Not reproducible at `7cd19c3c`.

## 2. The after-state measurement

Commands (run from the repo root; the tool is read-only over custody paths):

```
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm/ex26/probe/missing-dir
exit=2
USAGE: scratch base is not a directory: /dev/shm/ex26/probe/missing-dir
```
(`evidence/d6-after-7cd19c3c.txt`; before-state, same command at `112d01dc`:
`evidence/d6-before-traceback.txt` — `FileNotFoundError` from
`tempfile.mkdtemp` at `custody-pair.py:630`, exit 1.)

```
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm/ex26/okdir
exit=0
CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0
```
(`evidence/selftest-real-7cd19c3c.out`; before-state at `112d01dc`:
`CLEAN cases=15 passed=15 failed=0 exit=0` — so the claim's "selftest 15 → ≥17" is
met with margin: **15 → 22**.)

Landed guard, source lines (`custody-pair.py:721-733`):

```
721  base = Path(args.scratch).expanduser() if args.scratch else default_scratch()
723  if base_s == "/tmp" or base_s.startswith("/tmp/"):      -> USAGE 2
726  if not base.is_dir():                                  -> USAGE 2
729  try: mkdtemp(...)  except OSError:                      -> USAGE 2
```

Note for the round record: `:723` is **unconditional** — the round-2 text
(`and not args.scratch`) refused the env-var route to `/tmp` while accepting an
explicit `--scratch /tmp/…`; that asymmetry is gone at this revision.

## 3. Boundary sweep — 15 probes, three revisions

Harness: `evidence/sweep.sh`, `evidence/sweep2.sh` (probe list baked in; each probe
records exit code, whether stderr carries `Traceback`, the first stderr line, and
the selftest summary line). Raw rows: `evidence/sweep-base.tsv`,
`evidence/sweep-fixA.tsv`, `evidence/sweep-fixAB.tsv`,
`evidence/sweep-real-03bd6242.tsv`, `evidence/sweep-real-7cd19c3c.tsv`.

| probe (input to `selftest --scratch`) | before `112d01dc` | landed `7cd19c3c` |
|---|---|---|
| `missing-dir` (absent) | exit 1, traceback | **exit 2, USAGE** |
| `nested/deeper/leaf` (absent parent) | exit 1, traceback | **exit 2, USAGE** |
| existing regular file | exit 1, traceback | **exit 2, USAGE** |
| dangling symlink | exit 1, traceback | **exit 2, USAGE** |
| dir mode 0500 (exists, unwritable) | exit 1, traceback | **exit 2, USAGE** ("cannot create a fixture root under …") |
| `/dev/null` | exit 1, traceback | **exit 2, USAGE** |
| `/proc/ex26-none` | exit 1, traceback | **exit 2, USAGE** |
| `/proc` (exists, unwritable) | exit 1, traceback | **exit 2, USAGE** |
| relative `does-not-exist-rel` | exit 1, traceback | **exit 2, USAGE** |
| `missing-dir/` (trailing slash) | exit 1, traceback | **exit 2, USAGE** |
| `../ex26-definitely-missing` | exit 1, traceback | **exit 2, USAGE** |
| existing dir | CLEAN 15/15 exit 0 | CLEAN 22/22 exit 0 |
| symlink → dir | CLEAN 15/15 exit 0 | CLEAN 22/22 exit 0 |
| `--scratch=` (empty ⇒ default) | CLEAN 15/15 exit 0 | CLEAN 22/22 exit 0 |
| no `--scratch` (default) | CLEAN 15/15 exit 0 | CLEAN 22/22 exit 0 |

Every one of the 11 bad inputs was an undeclared exit-1 traceback before and is a
declared `USAGE` exit 2 now; no good input was disturbed. (The `stderr1` column of
the good rows shows the selftest's *own* expected `USAGE: unparsable receipt …`
line from its junk-receipt case — not a probe failure.)

**Derived variants measured before the landed fix existed** (scratch only, the real
target was never written by this seat): `fixA` = the literal EX-34 `is_dir()` patch
(`evidence/…`; sha `c81ea9b8…`, 892 lines) closed 9 of 11 bad inputs but left
`readonly-dir` and `/proc` tracebacking at exit 1 — i.e. the round-2 patch text was
**incomplete on its own axis**. `fixAB` = `is_dir()` + `mkdtemp` `OSError` → USAGE
(sha `00e4694f…`, 928 lines) closed 11/11 and ran `CLEAN cases=17 passed=17`.
The landed revision matches `fixAB`'s shape (and goes further on `/tmp`).
Variant shas: `evidence/variants.sha256`; generator: `evidence/gen-variants.py`.

## 4. Fence integrity — is the tool's own new case load-bearing?

Mutation test (`evidence/mutate-fence.py`, output
`evidence/mutation-fence-7cd19c3c.out`), run on a scratch copy under the canonical
filename, guard block located **by content** (asserted, not by remembered line
numbers), two mutants:

| mutant | meaning | landed selftest |
|---|---|---|
| `mutA` — guard + `try/except` removed | pre-round-3 behaviour | `DIRTY cases=22 passed=21 failed=1 exit=3`, `selftest-missing-scratch-usage-exit FAIL (expected USAGE exit 2 for missing scratch, got 1)` |
| `mutAB` — `is_dir()` kept, `try/except` removed | the half fix | `CLEAN cases=22 passed=22 failed=0 exit=0` |

So the landed case **is** non-vacuous for the missing-dir regression, and it is
**blind to the `mkdtemp` `OSError` arm**: a regression that re-opened the
existing-but-unusable-dir class (mode-0500 dir, `/proc`) would ship with a green
selftest. That is a measured gap, not an opinion; §6 hands over a case body that is
proven in both directions on scratch: it FAILS without the `try/except`
(`fixAC`: `DIRTY cases=17 passed=16 failed=1`) and PASSES with it
(`fixAB`: `CLEAN 17/17`; transcripts `evidence/fence-fixAC.out`,
`evidence/fence-baseC.out` — the latter shows both new cases failing on the
unguarded base).

## 5. Read-only proof over the custody paths

No seat activity of mine wrote a custody path. The tool's own capture/verify pair
around all of my runs (pre at 10:08, post at 10:11, both captured by the *then*
landed tool), re-verified at write time:

```
CUSTODY_PAIR_CAPTURE: OK paths=5/5 label=EX-26 pre exit=0
CUSTODY_PAIR_CAPTURE: OK paths=5/5 label=EX-26 post exit=0
CUSTODY_PAIR_VERIFY: MATCH paths=5/5 drift=0 exit=0        (SHA256-CONTRACT: 5/5)
```
(`evidence/custody-pre.txt`, `custody-post.txt`, sidecars, `custody-verify.out`.)
All selftest fixtures lived under `/dev/shm/ex26/` or `/var/tmp`; **nothing was
written to `/tmp`**; no git mutation was issued (`git status` untouched by this seat);
the real target and README were never edited by this seat (all variants/mutants are
`/dev/shm` copies, named `custody-pair.py` **only** inside their own scratch dirs,
because the module's TZ case resolves a sibling of that name — a relocatability
detail worth knowing, and the reason `custody-pair-base.py` in a shared dir reports
`DIRTY 14/15`).

One residue of mine, disclosed rather than hidden: importing the real module for the
residual probe at 10:08 created
`.ufo/gates/custody-pair/__pycache__/custody-pair.cpython-314.pyc` (git-untracked).
It is outside this seat's write allowance, so I left it in place — exclude it from the
wave commit per the round-2 D9 rule.

## 6. Residuals on this axis (live at `7cd19c3c`), with patch text

Both are handed over as patch text in
`proposed-scratchguard-residuals.patch.md` (EX-21 owns the write):

- **R1 — `default_scratch()`'s failure arm exits 1, not 2.** `custody-pair.py:606-613`
  ends `raise SystemExit("USAGE: no writable scratch dir …")`; `SystemExit(<str>)`
  makes the interpreter exit **1** while printing a USAGE-looking line.
  Measured end to end as a *process* exit with `os.access` stubbed (the host has
  `/dev/shm` and `/var/tmp` writable, so the arm is otherwise unreachable here;
  declared synthetic): `exit=1 traceback=False` on both the real revision and my
  `fixAB` copy — `evidence/residual-probes-real-7cd19c3c.out`. This is the same
  defect *class* as D6 (an undeclared exit on a scratch-resolution failure) and the same
  one-line fix lands it in the declared map.
- **R2 — the `/tmp` exclusion is a string-prefix test.** `:723`
  (`base_s == "/tmp" or base_s.startswith("/tmp/")`) is not normalizing:
  predicate evaluated for `//tmp/x` → `guard_fires=False` though
  `os.path.realpath("//tmp/x") == "/tmp/x"`. Low severity (needs an explicit
  argument spelling the path that way); the end-to-end run was **not** executed
  because this host's standing rule forbids `/tmp` writes. `os.path.realpath(base)`
  would close it.
- **Fence gap (from §4, not a behavior defect):** add a case for the
  `mkdtemp` `OSError` arm; the case body is proven in both directions on scratch.

Documentation: at `7cd19c3c` the README (re-derived `f30df42e…`, 10:15:12, snapshot
`evidence/README-at-writetime.md`; it had also moved `752032cf…` 10:14:47 and
`039993ed…` 10:13:35) carries
the 14-row, the extended USAGE causes, `UNEVALUABLE` in the precedence line, and the
22-case list including `selftest-missing-scratch-usage-exit` — **consistent** with the
tool. Earlier mid-edit states were not: README `68458081…` (10:12) still pinned
`cases=15` while the tool ran 21, and the 10:13 README had no `14 UNEVALUABLE` row.
Recorded as transient churn (caught, timestamped, gone), not as landed debt.

## 7. Identity re-derivation (rule #14)

Every sha256 quoted here was re-derived after the last revision of the file it
describes. The evidence inventory's digests live in the sibling `sha256sums.txt`,
re-derived at the end of this seat's work; this file's own digest cannot appear in
that inventory's own line sense, so it is recorded in the seat report
(`.ufo/waves/arc3-loop1-round3/seats/EX-26.md`). No artifact of mine claims its own
byte-identity without that re-derivation.

## 8. Honest limits

- The landed after-state is measured on this host with the real tool; the R1 arm is
  a declared synthetic stub measurement, and R2 is a predicate evaluation, not a run.
- Boundary probes were executed against byte-exact snapshot copies (canonical
  filename) plus direct runs of the live path for the D6 case at each revision.
- The revision could move again after write time; `evidence/poll.log` and the
  snapshot files pin what was measured, and a re-check of `sha256sum` against the
  §1 table is the re-derivation the parent should run at landing.