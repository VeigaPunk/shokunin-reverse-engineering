# R45W1PreflightArms — arm mutation test of the frozen freeze-integrity preflight

Seat `R45W1PreflightArms` (mutation-tester), kaidoku round 45 wave 1. Read-only on the lane
tree: this seat wrote only inside `.ufo/waves/round-45/w1/R45W1PreflightArms/`.

| item | value |
|---|---|
| target | `tools/round-45/frozen-path-preflight.py` |
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` |
| frozen bytes (freeze commit, `git show <freeze>:...`) | `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` |
| worktree bytes at start and at end of the seat | the same `633ebc05…523b` |
| detector (bounded behavioural) | the instrument's own `--selftest` |
| baseline on the **frozen file itself** | exit `0`, `PREFLIGHT_SELFTEST: cases=11 failures=0`, stdout sha256 `9f03df65…9ec06c`, 2026-10-28T15:47:31Z |
| baseline on a **copy** (before mutants, and again after) | exit `0`, `cases=11 failures=0`, stdout sha256 `9f03df65…9ec06c` — byte-identical to the frozen-file run, so the copy is behaviourally the frozen file |

**Verdict: 3 of the 4 assigned mutants are killed; `m2` survives.** Four further mutants
beyond the assigned arms (`x1`–`x4`) also survive, one of which is a false-clean in the
pristine instrument (`x2`) and one of which removes the only defence the round's own
two-path frozen set relies on (`x4`). Details and exact reproducers below.

Everything below is a finding. The instrument is frozen; this seat reports the differing
value and does not patch it.

---

## 1. Assigned arms — mutation table

Each mutant was applied to a private copy under
`/fast/scratch/hyaku/kaidoku-r45/R45W1PreflightArms/<mutant>/frozen-path-preflight.py`;
`--selftest` ran with `TMPDIR` and `HYAKU_SCRATCH` both pointed inside that scratch tree.

| # | arm | mutation (exact) | expected detector | mutated sha256 | exit | `cases=` / `failures=` | cases that flipped `expect→got` | verdict |
|---|---|---|---|---|---|---|---|---|
| m1 | dirty (`--check-dirty`) | the whole `if check_dirty:` block deleted; `dirty = []` retained so the receipt key survives | `red-dirty` (1→0) | `0861d831…28ee1d` | 1 | 11 / 1 | `red-dirty` 1→0 | **killed** |
| m2 | restored | the `elif any(t["path"] == path for t in touched): restored.append(path)` branch deleted | `red-restored` (1→0) | `a29d98c6…2b725b` | 0 | 11 / 0 | *none* | **SURVIVED — hole** |
| m3 | pathspec (`--require-pathspec`) | the arm returns `0` immediately without computing `missing` (before the log/blob/dirty arms) | `red-dirfreeze-no-pathspec` (2→0) | `e0211ea9…2012ee` | 1 | 11 / 5 | `red-touched` 1→0, `red-restored` 1→0, `red-dirty` 1→0, `red-dirfreeze-no-pathspec` 2→0, `red-bulk-sweep` 1→0 | **killed** |
| m4 | commit (`git log --name-status`) | the `git log` call and the `touched` parser deleted; `touched = []`; blob arm untouched | `red-restored` (1→0) | `e02af39e…38f7e6` | 1 | 11 / 1 | `red-restored` 1→0 | **killed** |

`m1` and `m4` stdout sha256 `cc07ca8a…ea33e`, `abfee0c5…f4da7` — different from baseline,
i.e. the detector actually saw them. `m2` stdout sha256 is `9f03df65…9ec06c` — **byte-identical
to the pristine run.** The detector did not see `m2` at all.

### 1.1 `m1` — killed, and properly paired

`red-dirty` is the only case that flips, and the selftest also carries its complement
`green-dirty-without-arm` (`check_dirty=False` on the same dirty worktree, expects 0). The
pair pins the arm's necessity in both directions: present-and-dirty → 1, absent-and-dirty → 0.
This is the design the other arms do not have.

### 1.2 `m3` — killed, but the kill is coarse

Five cases flip, only one of them meaningfully. The mutation is an early `return 0` inside
`evaluate`, so it bypasses the commit, blob and dirty arms as well: everything downstream of
`--require-pathspec` returns clean. `red-dirfreeze-no-pathspec` (2→0) is the only case that
attributes the flip to the pathspec arm. The other four are collateral, which means the
selftest would report a five-case failure for "the pathspec arm wrongly skipped everything"
and cannot distinguish it from "several arms broke at once". Not a hole (the mutant dies), a
calibration limit on the diagnosis.

### 1.3 `m4` — killed, but by exactly one case, and not the one you would expect

Dropping the commit arm leaves `touched == []`. `red-touched` stays **green** because the blob
arm catches the modified file at the tip; `red-bulk-sweep` stays **green** for the same
reason. Only `red-restored` (append-then-restore, tip blob equal to freeze) can fail when the
commit arm is gone. So the commit arm has exactly one unique detector, and that detector is
the case named for a different arm.

### 1.4 `m2` — SURVIVED: the `restored` list has no verdict authority

The mutant deletes the restore classifier and the selftest stays green (exit 0, 11 cases,
0 failures, byte-identical stdout). It is not an equivalent mutant — it is a **verdict-equivalent**
mutant whose observable change is receipt-only:

* fixture `repo kind = restored` (freeze → tamper `frozen/a.txt` → restore `alpha`);
* pristine `evaluate(d, f, r, ["frozen/"], ["frozen"], False, [], True)` → `code 1`,
  `verdict frozen_path_changed`, `restored ["frozen/a.txt"]`, `touched` 2 records;
* m2 → `code 1`, `verdict frozen_path_changed`, **`restored []`**, `touched` 2 records.

(receipt `receipts/m2b.json`, `receipts/reachability.json`)

**Why no case can ever catch it.** The append is guarded by

```python
elif any(t["path"] == path for t in touched):
    restored.append(path)
```

so `restored ≠ [] ⟹ touched ≠ []`, and the verdict is

```python
ok = not touched and not blob_changed and not restored and not dirty
```

`not touched` is already `False`, so `ok` is `False` regardless of `restored`. In **every**
reachable state the `restored` list cannot change the exit code: a restored path is always
already a violation through `touched`. `restored` is a receipt classifier, not an arm.

**Root cause of invisibility.** `selftest()`'s `case()` compares only `code == expect`:

```python
ok = code == expect
cases.append({"case": name, "expect": expect, "got": code, "ok": ok, "receipt": receipt})
```

The receipt is captured into the case record and then never asserted and never printed. No
case in the selftest asserts any receipt field. Every receipt-only regression — `restored`
membership, `touched` records, `blob_changed` membership, the `dirty` entry strings, the
`pathspec` echo — is structurally outside the detector's reach. `m2` is the proof, and `x4`
is the same hole on a load-bearing arm.

---

## 2. Arm coverage matrix (what the 11 cases actually pin)

| arm | case that can only it fail | complementary green case | note |
|---|---|---|---|
| commit | `red-restored` | — | shared responsibility: `red-touched` and `red-bulk-sweep` stay green without this arm |
| restored | **none** | **none** | verdict-equivalent to `touched`; only the receipt field distinguishes it |
| blob (`blob_changed`) | **none** | **none** | every red fixture that changes a blob also has a non-empty `touched`, so the commit arm absorbs the kill (see `x4`) |
| dirty | `red-dirty` | `green-dirty-without-arm` | sound pair |
| pathspec | `red-dirfreeze-no-pathspec` | `green-dirfreeze-pathspec` | sound pair |
| revision guard | `red-unknown-freeze`, `red-nonancestor` | `green-empty-range`, `green-clean` | sound |

Two of the five documented arms — `restored` and `blob` — have **zero unique detection**.
That is the concrete content of "a surviving mutant is a hole".

---

## 3. Exploratory mutants (not assigned; reported because they are holes)

| # | mutation | mutated sha256 | exit | failures | flips | verdict |
|---|---|---|---|---|---|---|
| x1 | `covers()` inverted: accept an **ancestor** pathspec (`fp.startswith(p + "/")`) | `91af24c9…00ec05` | 0 | 0 | none | **survived** |
| x2 | `scope_paths = pathspecs` — `--dirty-pathspec` ignored | `93c1b891…f684af` | 0 | 0 | none | **survived** |
| x3 | dirty arm filters out `??` (untracked) entries | `748f524e…b218af` | 0 | 0 | none | **survived** |
| x4 | blob arm records nothing (`blob_changed` stays `[]`) | `498d7905…479373` | 0 | 0 | none | **survived** |

All four are behaviourally reachable — pristine vs mutant on the same read-only fixture
(`receipts/x1b| x2b| x3b| x4b.json`), so none is an equivalent mutant:

| probe | fixture | pristine | mutant | delta |
|---|---|---|---|---|
| x1b | nested frozen dir, `--pathspec frozen --freeze-path frozen/inner --require-pathspec` | exit **2**, `reason pathspec_required` | exit **0**, `verdict clean` | covers() direction is unpinned |
| x2b | `frozen/b.txt` dirty, `--pathspec frozen/ --freeze-path frozen --check-dirty --dirty-pathspec other.txt` | exit **0**, `dirty []`, `verdict clean` | exit **1**, `dirty [" M frozen/b.txt"]` | **pristine false-clean** (see F3) |
| x3b | `frozen/stray.txt` created, never `git add` | exit **1**, `dirty ["?? frozen/stray.txt"]` | exit **0**, `dirty []`, `clean` | untracked shape unsupported by any case |
| x4b | commit changes `frozen/a.txt`, `--pathspec other.txt --freeze-path frozen` (log scope excludes the change) | exit **1**, `blob_changed ["frozen"]`, `touched []` | exit **0**, `blob_changed []`, `verdict clean` | **blob arm is the only defence here; untested** |

---

## 4. Findings for the L1 (severity-ordered; each with the exact reproducer)

**F1 — `x4`/blob: the round's own two-path frozen set is defended by an arm with no red case.**
The claims file freezes two things, `plans/round-45-claims.md` and the **directory**
`tools/round-45/`, and `plans/round-45-claims.md:135-136` tells the caller to pass
`--pathspec tools/round-45/ --freeze-path tools/round-45`. A caller who passes both
`--freeze-path` values but only one `--pathspec` gets a log that is scoped away from the
other frozen path; the **blob** arm is then the only detector, and the selftest has no
fixture in that shape (every case's pathspec covers its freeze-path). Removing the blob
arm entirely leaves all 11 cases green.

```
python3 -I -B tools/round-45/frozen-path-preflight.py --root <d> --freeze <F> --rev <R> \
  --pathspec other.txt --freeze-path frozen
# pristine : exit 1  {"blob_changed": ["frozen"], "touched": [], "verdict": "frozen_path_changed"}
# with x4  : exit 0  {"blob_changed": [], "verdict": "clean"}
```
Highest severity: it is an arm the frozen round must rely on, and the selftest cannot see its
loss. A killing case is cheap and needs no new surface: the existing `touched` fixture with
`pathspecs=["other.txt"]` and `require_pathspec=False` expects 1.

**F2 — `m2`/restored: the named red case `red-restored` tests nothing about `restored`.**
`SKILL.md:555` promises "one red case per arm (11 cases at the round-45 freeze)" and
block 22's row 2 names `restored` as an arm with its own exit and receipt. Under the block's
own reading rule — "the first row whose trigger holds decides" (`SKILL.md:556-557`) — row 2
is unreachable as a decision, because row 1 (any commit touching a frozen path) already holds
for every restored path; the code agrees (`restored ⊆ touched`, §1.4). So the sentence is true
about the *outcome* (a restored touch yields 1) and false about the *arm* (the list can be
deleted with the selftest still green). Killing case: assert the receipt, e.g. `red-restored`
also requires `receipt["restored"] == ["frozen/a.txt"]` — the only thing in the selftest that
could ever distinguish the classifier from its absence.

**F3 — `x2`: `--dirty-pathspec` *replaces* the frozen scope, and the pristine gate returns a
false clean.** `SKILL.md:582` and the docstring both say the dirty arm means "the worktree
must be clean **under the frozen pathspec**". With `--dirty-pathspec` supplied,
`scope_paths = dirty_pathspecs or pathspecs` drops the frozen pathspec entirely, so a dirty
file under the frozen directory is reported clean by the instrument that exists to catch it.
Reproducer (exit and value observed today, not reconstructed):

```
python3 -I -B tools/round-45/frozen-path-preflight.py --root <d> --freeze <F> --rev <F> \
  --pathspec frozen/ --freeze-path frozen --check-dirty --dirty-pathspec other.txt
# exit 0  {"dirty": [], "verdict": "clean"}
git -C <d> status --porcelain     # " M frozen/b.txt"
```
`--dirty-pathspec` is not in the arm documentation at all (the docstring documents
`--check-dirty` only) while argparse accepts it, so the option's contract is unstated and its
composition with `--pathspec` is additive-looking but subtractive in effect. Blast radius for
scoring is nil — `tools/round-45/c1-counter.py:106` (`run_preflight`) runs the interpreter with `--selftest`
only (`run_preflight(root, rev, work)`), so no counter passes `--dirty-pathspec` — but any
human or L1 invocation that adds it silently loses the arm that block 22 calls "the arm that
matters most" (`SKILL.md:591`).

**F4 — `x3`: the M44-2 precursor shape (a writer's uncommitted stray file) is supported but
untested.** Pristine catches `?? frozen/stray.txt` (exit 1); filtering untracked entries keeps
all 11 cases green. The only dirty fixture writes to a **tracked** file (`M`), so the
`??` path — the literal state M44-2 describes before the sweep commits anything — has no
case. Killing case: drop an untracked file into the frozen dir in a `dirty` variant.

**F5 — `x1`: `covers()` direction is unpinned, and pristine is over-strict.** An ancestor
pathspec that does cover the frozen directory (`--pathspec frozen` for
`--freeze-path frozen/inner`) yields exit 2 `pathspec_required` — a could-not-evaluate for a
caller whose pathspec does include the frozen path. Whether that is intended (the docstring's
"equals or lies under" says yes; git's pathspec semantics say no) is the L1's call, but no case
pins either reading: inverting the predicate keeps the selftest green. Low severity — the
documented invocation passes the exact directory (`--pathspec tools/round-45/`,
`--freeze-path tools/round-45`, equal → covered).

**F6 — general: the detector asserts exit codes only.** See §1.4. `cases=11 failures=0` is a
statement about exit codes in eleven fixtures, not about trailing receipt fidelity. Since the
receipt is the adjudicable artefact (the claims' `--json-out` and block 22's `receipt` column),
that gap is the one to name in the lesson rather than the individual survivors.

---

## 5. Calibration — what this does and does not touch

*Anchor note.* `SKILL.md` was being landed by the L1 while this seat read it (its line count
grew by 9 between two reads). Every `SKILL.md:<n>` below is the line observed at
`sha256 e08ee7d03b8f66772a9b72f991446228d2d1445174967d49a49afd4dbcfed66d` (1654 lines,
2026-10-28T15:49Z); the quoted text, not the number, is the citation.

* R45-C1 clause 6 (`--selftest` exit 0, `cases >= 11`, `failures == 0`) is **unaffected**:
  the frozen file runs `cases=11 failures=0` exit 0 today (§baseline), from the freeze commit's
  bytes.
* No clause of R45-C1 or R45-C2 is failed or passed differently by anything here; the graded
  counters never call the preflight's arms. This seat's findings are about the *truth of the
  depth narrative* (`SKILL.md:555` "one red case per arm") and about the gate a human runs
  at commit time.
* The registry row `SKILL.md:1648` stays accurate as an enumeration of receipt fields
  (`arms commit, restored, blob, dirty, pathspec`) and of exits; "`1` a frozen path changed, a
  restored touch, or a dirty worktree" is outcome-true. It does not claim per-arm selftest
  coverage, so it needs no correction — block 22's "one red case per arm" does.
* Not tested here (outside this seat's assignment, so "not run"): `c1-counter.py`,
  `c2-counter.py`, block 22's table/citation clauses, `registry-scope.json`. The `--selftest`
  was not run under a hostile environment (no `GIT_DIR`, no bare `/tmp`); it was run with
  `TMPDIR`/`HYAKU_SCRATCH` pinned to scratch and `-I -B`.

---

## 6. Honest limits of this seat

* The detector is the instrument's own selftest. A mutant that survives is a hole **in that
  detector**, not proof that the arm is worthless — `m2`'s classifier is real and does change
  the receipt.
* One fixture per case, no fuzzing, no path names with spaces/tabs/unicode, no `-z`-hostile
  paths, no rename or typechange fixtures (the `R`/`T`/`C` status letters in the commit parser
  are exercised by no case at all — visible in §2 as part of the commit arm's single-detector
  situation).
* `x4`'s scoped-out configuration is a caller configuration I constructed, not one the round's
  counter or block 22 prescribes verbatim; it is the shape the two-frozen-path set *invites*,
  and it is exactly the state where the blob arm is the only detector.

---

## 7. Restoration and cleanliness evidence

| check | command | result |
|---|---|---|
| frozen bytes = freeze commit | `git -C <lane> show f762b72…:tools/round-45/frozen-path-preflight.py \| sha256sum` | `633ebc05…523b` |
| worktree bytes before the seat | `sha256sum tools/round-45/frozen-path-preflight.py` | `633ebc05…523b` |
| worktree bytes after every run | same, `mutation-matrix.json:instrument_sha256_after_all_runs` | `633ebc05…523b`, `instrument_untouched true` |
| lane write-check | `git status --porcelain -- plans/ tools/ \| wc -l` | `0` |
| scratch removed | `rm -rf /fast/scratch/hyaku/kaidoku-r45/R45W1PreflightArms; ls -d …` | `No such file or directory` |
| no `/tmp` writes | every run carried `TMPDIR` **and** `HYAKU_SCRATCH` inside that scratch tree (`-I -B`); the `/tmp/kaidoku*` entries on this host predate this seat's first run (15:39Z vs 15:46Z) and were not written by it | — |
| frozen originals never mutated | the four mutants were written only to scratch copies, each deleted after its run; the restored-bytes control re-ran the pristine copy (bytes identical, stdout hash identical) | see `receipts/baseline-2-restored.json` |
| git mutations | none — read-only `log`/`show`/`status`; fixtures were `git -C "$D"` repos under scratch, each `rev-parse --show-toplevel` asserted equal to `$D` | — |

No installs, no upgrades: nothing was needed (Python 3.14.8, git; no network).
`$S` was removed after the receipts were copied into `receipts/`.

---

## 8. Receipts (all under `receipts/`, sha256 of each file)

| file | sha256 | what it carries |
|---|---|---|
| `canonical-frozen-file.json` | `138bd6b3…1d00c` | the frozen file's own `--selftest`: command, exit 0, `cases=11 failures=0`, stdout sha256 `9f03df65…9ec06c`, 15:47:31Z |
| `baseline-1.json` | `bdd4b687…4119d` | pristine copy baseline (command, exit, stdout sha256, UTC, per-case JSON) |
| `baseline-2-restored.json` | `3c51fd74…a26a86` | restored-bytes control: bytes + stdout bit-identical to baseline-1 |
| `m1.json` | `eace637c…a0797` | mutant m1: command, mutated sha256, exit 1, flips |
| `m2.json` | `31d78b5f…705845` | mutant m2: exit 0, zero flips, stdout byte-identical to baseline |
| `m3.json` | `a36bff1e…c1ea17` | mutant m3: exit 1, five flips |
| `m4.json` | `ba31ef26…b54a6` | mutant m4: exit 1, `red-restored` only |
| `x1.json` … `x4.json` | `01144d99…`, `ec6c2862…`, `9651af12…`, `9ed04d3a…` | the four exploratory mutants (exit 0, zero flips each) |
| `m2b.json`, `x1b.json`, `x2b.json`, `x3b.json`, `x4b.json` | `c1607a1c…`, `97c953e8…`, `73375dbe…`, `d0da307e…`, `a1c90659…` | reachability: pristine vs mutant on the same read-only fixture, both receipts |
| `mutation-matrix.json` | `dcf0a4db…5d8d` | the whole matrix, verdicts, restored-bytes control, `instrument_untouched` |
| `reachability.json` | `9c0eb1ef…e319c3` | all five probes in one file |

Harness (reproducible; reads the frozen file, writes only scratch):
`run_mutants.py` `dc323ec2…67c7d2`, `probe_receipt.py` `c9fdc0b8…fa3024`.

Reproduce:

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-45/w1/R45W1PreflightArms
python3 -B run_mutants.py    # baseline → m1..m4, x1..x4 → restored-bytes control
python3 -B probe_receipt.py  # pristine-vs-mutant receipts on shared fixtures
```

---

## 9. One-line answer to the assignment

`m1` killed by `red-dirty`; `m3` killed by `red-dirfreeze-no-pathspec` (plus four collateral
reds); `m4` killed by `red-restored` alone; **`m2` survives — the `restored` list cannot
change the verdict, so no exit-code case can ever detect its loss, and the selftest asserts no
receipt field.** The same blind spot hides the blob arm (`x4`, severity-high because the
round's own frozen set depends on it), plus the untested `--dirty-pathspec` composition
(`x2`, a pristine false-clean), untracked worktree entries (`x3`) and the `covers()`
direction (`x1`).
