# MutScratch — scratch discipline of both R47 counters (probe + mutation table)

Seat `MutScratch`, lane `kaidoku-shokunin`, round 47, wave 1. Read-only on the lane: every
write of mine is under `.ufo/waves/round-47/w1/MutScratch/` and under
`/fast/scratch/hyaku/kaidoku-r47/MutScratch` (removed after the receipts were copied here).

| field | value |
|---|---|
| measured rev | `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` (`round-47: record the A6 freeze and the A7 measurement`) |
| drift-free freeze at that rev | `f54b3b6de9085d3db449ed5d0916296cb29c1f6d` (A6) |
| prompt freeze `5017e1f…` at that rev | exit 2 `frozen_path_changed` — see F6 |
| python | 3.14.8 (`python3 -I -B`, as the claims' counting command) |
| tracer | strace 7.2 (`-f -qq -e trace=mkdir,mkdirat[,unlink,unlinkat]`) |
| probe window (UTC) | 2026-10-28T17:56Z … 2026-10-28T18:00Z |
| baselines that pass | C1 exit 0 `failing []`, battery `v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`; C2 exit 0 `failing []`, battery `correction_forgeries 3 / forgeries_green 0` |

Note: HEAD moved under this seat mid-run (`caafeffa…` → `31b092d1…`, A5/A6 plus the A6 pin
commit). The matrix was re-run at `31b092d1`; both revs agree on every scratch verdict below.
Nothing of mine touched a lane file: `git status --porcelain` outside `.ufo/waves/` is empty
before and after, and `git status` shows no path of mine.

## 1. Probe matrix (the four assigned probes, plus the guard's neighbours)

`--json-out` targets that are outside the lane root are refused, so `--json-out` receipts
cannot live in scratch at all; every probe below is stdout-only (hashed) unless a target is
named. `S=/fast/scratch/hyaku/kaidoku-r47/MutScratch`,
`L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

| # | probe | command shape | C1 `exact.py` | C2 `record.py` |
|---|---|---|---|---|
| P1 | own root (`HYAKU_SCRATCH=$S TMPDIR=$S`), absolute `--json-out` in my seat dir | `python3 -I -B tools/round-47/{exact,record}.py --root $L --rev 31b092d1 [--freeze f54b3b6] --json-out $L/.ufo/waves/round-47/w1/MutScratch/c1-own-head.json` | **0**, `failing []` | **0**, `failing []` |
| P2 | `TMPDIR=/tmp`, `HYAKU_SCRATCH` unset | `env -u HYAKU_SCRATCH TMPDIR=/tmp python3 …` | **2** `scratch root is a temporary partition: /tmp`; 0 `/tmp` syscalls | **0**, receipt byte-identical to P1 (`d24410d1…`), 0 `/tmp` syscalls |
| P3 | no `HYAKU_SCRATCH`, no `TMPDIR` | `env -u HYAKU_SCRATCH -u TMPDIR python3 …` | **2** `no HYAKU_SCRATCH/TMPDIR root set` | **0**, byte-identical to P1 |
| P4 | `HYAKU_SCRATCH=/tmp` while `TMPDIR=$S` | `env HYAKU_SCRATCH=/tmp TMPDIR=$S python3 …` | **2** `scratch root is a temporary partition: /tmp` (`HYAKU_SCRATCH` wins over a good `TMPDIR` — correct, refuses) | **0**, byte-identical to P1 |
| P5 | relative `--json-out` from the lane root | `--json-out r47p3-c1.json` with cwd `$L` | **0** and **writes `$L/r47p3-c1.json`** (`b95251e8…`, byte-equal to stdout) → moved to `receipts/r9/` | **0** and **writes `$L/r47p3-c2.json`** (`d24410d1…`) → moved to `receipts/r9/` |
| P6 | relative `--json-out` from any other cwd | same, cwd `$S` | **2** `--json-out outside the lane root: rel-c1.json` | **2** same |
| P7 | `--json-out SKILL.md` / `./SKILL.md` / `tool s/round-47/exact.py` / `plans/round-47-claims.md` / `SCORECARD.md` / `LOG.md` | cwd `$L` | **2** `--json-out inside a graded or frozen surface: <rel>`; SKILL.md sha unchanged | **2** same reason for `SKILL.md` |
| P8 | symlink to a graded file (`$S/link-to-skill.json → SKILL.md`) | `--json-out $S/link-to-skill.json` | **2** `inside a graded or frozen surface: SKILL.md` (`realpath` resolves; defense holds) | **2** same |
| P9 | `--json-out` at a directory / outside / `..` / `/etc/passwd` / `~x.json` | — | **2** `outside the lane root: …` for all but `~x.json`, which is a literal name and lands in the lane root | same |
| P10 | `--json-out` whose parent dir does not exist | `--json-out .ufo/waves/round-47/w1/MutScratch/nodir/x.json` | **exit 1** + traceback on stderr (653 B) — see D1 | **exit 1** + traceback (655 B) — see D1 |
| P11 | empty `--json-out ''` | — | treated as absent: stdout only, no file | — |
| P12 | selftests under the same envs | `--selftest` | exit 2 (argparse: `--root/--freeze/--rev` are required before `--selftest` is honoured — see D6) | exit 2, same |

### Verdict on the assigned question

* **`TMPDIR=/tmp` → no counter writes under `/tmp`.** C1 refuses at the call site before
  `mkdtemp` (exit 2, reason quoted above, **0** `mkdir`/`mkdirat` under `/tmp` in the strace);
  C2 has no scratch surface at all (P2–P4 byte-identical receipts, **0** `/tmp` syscalls).
  A "counter that writes under /tmp" is **not** present at `31b092d1`.
* **`/tmp` is only half-guarded.** `TMPDIR=/dev/shm` is accepted and the C1 battery runs there
  (exit 0, `failing []`) — a tmpfs the round-46 guard's `TEMP_PARTITIONS` does not name (D4).
* **The relative-`--json-out` probe is a real, unfixed hole** (D2): exit 0 and an untracked
  file in the lane root.
* **C2 cannot express a scratch verdict.** `record.py` never calls `gate.scratch`; its battery
  mutates the card text in memory. Its scratch discipline is therefore *vacuous*, not
  *satisfied*: the only evidence is env-insensitivity (P2–P4) and the zero-syscall strace.
  A future C2 clause that claims to test scratch hygiene would be unfalsifiable.

## 2. Mutation table

Mutants live only in the fixture copy `$S/fx-lane` (`git archive HEAD -- SKILL.md plans
tools/round-46 tools/round-47 corpus/lessons corpus/knowledge`, own `git init`, first commit
`46ae5eb4…`; `git -C $F rev-parse --show-toplevel` = `$F` verified before the first commit).
Pristine control in the copy: exit **0**, `failing []`.

Detector for every row = the bounded behavioural triple *(exit code, `/tmp`+`/dev/shm`
`mkdir` count under `strace`, graded-file sha256)*, run on pristine → mutant → restored.

| # | mutation (smallest behaviour-bearing point) | pristine | mutant | detected by | restore |
|---|---|---|---|---|---|
| M1 | `gate.py` `TEMP_PARTITIONS = ("/tmp", "/var/tmp")` → `("/var/tmp",)` | exit 2 `temporary partition: /tmp`, 0 /tmp mkdirs | exit **0**, `failing []`, battery green, **82** mkdirs under `/tmp/kaidoku-r47-battery-wcg11h3a`, 4 fixture repos built in `/tmp` | **KILLED** by the /tmp-write count (exit alone also flips 2→0) | `gate.py` `c3ba6b93…` restored, match **YES**, re-run exit 2 again |
| M2 | `exact.py` call site: `if err: return 2, {...}` → `if err: scratch_root = None` | — | exit 2 **`frozen_worktree_dirty`**, 0 /tmp mkdirs | **INCONCLUSIVE** — the F3 dirty-frozen-path guard fires before the scratch call; the mutant never reaches `mkdtemp`. Committing it would trip `frozen_path_changed`, and pinning it would break `interpreter_sha256`. A call-site mutant on a frozen tool is masked by design; the load-bearing point is in `gate.py` (M1, M2b) | `exact.py` `01a4bca7…` restored, match **YES** |
| M2b | `gate.scratch`: create the dir under `/tmp` **and then** return the same refusal | exit 2, 0 /tmp mkdirs | exit **2** (unchanged!) **and 1 mkdir** `/tmp/kaidoku-r47-battery-fnycp_wc` | **survives exit-code-only checking; KILLED only by the syscall/residue detector.** Calibration: an exit-code check cannot detect a `/tmp` write | `gate.py` restored `c3ba6b93…`, match **YES**; my `/tmp` residue removed (`rm -rf`, 0 left) |
| M3 | `gate.out_path`: `if rel in GRADED or head in GRADED:` → `if False:` , cwd = fixture root, `--json-out SKILL.md` | exit 2 `inside a graded or frozen surface: SKILL.md`, fixture `SKILL.md` `bf94d1b5…` unchanged | exit **0** — and the fixture's `SKILL.md` is replaced by the receipt JSON (`5d7dab75…`): the graded surface is destroyed and the counter still scores **met** | **KILLED** by the graded-file sha256 | fixture `SKILL.md` and `gate.py` restored from `HEAD`, both match **YES** |

Supporting hashes: pristine trace `receipts/r4/pristine.trace` (0 `/tmp` lines),
M1 trace `receipts/r4/m1.trace` (82), M2b trace `receipts/r6/m2b.trace` (1, first line
`mkdir("/tmp/kaidoku-r47-battery-fnycp_wc", 0700) = 0`), C2 trace `receipts/r8/c2.trace` (0).

## 3. Routed defects (with the exact command that shows each)

**D1 — a can't-write is scored as a violation.** `gate.emit` is called *outside*
`gate.main_guard` (`tools/round-47/exact.py:446`, `tools/round-47/record.py:488`), so an
`--json-out` that cannot be created exits **1** with a Python traceback on stderr — the
"not met" verdict — instead of 2 with a JSON `reason`. A judge whose output directory is
missing records a red claim that was never measured.

```sh
python3 -I -B tools/round-47/record.py --root . --rev 31b092d1 \
  --json-out .ufo/waves/round-47/w1/MutScratch/nodir/x.json   # exit 1, 655 B traceback
python3 -I -B tools/round-47/exact.py --root . --rev 31b092d1 --freeze f54b3b6 \
  --json-out .ufo/waves/round-47/w1/MutScratch/nodir/x.json   # exit 1, 653 B traceback
```
Expected: exit 2, `{"reason": "--json-out unusable: …"}`. Receipts: `receipts/r9/c{1,2}-crash.{out,err}`.

**D2 — a relative `--json-out` is resolved against the cwd, not `--root`, and lands in the
lane root.** Same argv, same bytes, different verdict by cwd: exit 0 writing
`$LANE/r47p3-c1.json` from the lane root; exit 2 `outside the lane root` from anywhere else.
The written file is byte-equal to stdout (`b95251e8…` C1, `d24410d1…` C2) and sits in a
tracked directory — one `git add -A` from history. This is the exact discipline hole the
contract's "write only inside your seat dir" rule is meant to close; the counter does not
enforce it, and the claims file does not say `<OUT>` must be absolute.

```sh
cd "$LANE" && python3 -I -B tools/round-47/exact.py --root . --rev 31b092d1 \
  --freeze f54b3b6 --json-out r47p3-c1.json    # exit 0, writes ./r47p3-c1.json
```
Fixture path that shows it: none needed — it is the real lane. Residue preserved at
`receipts/r9/r47p3-c1.json`, `receipts/r9/r47p3-c2.json` (moved out of the lane root
immediately; `git status` outside `.ufo/waves/` empty afterwards).

**D3 — the documented counting command fails for a natural `<OUT>`.** `plans/round-47-claims.md`
gives `--json-out <OUT>` with no legal location. `<OUT>` in `/tmp` or in the seat's own
scratch is refused `--json-out outside the lane root` (exit 2), so a judge following the
command verbatim in a fresh scratch dir measures nothing:

```sh
env -u HYAKU_SCRATCH TMPDIR=/tmp python3 -I -B tools/round-47/exact.py --root "$LANE" \
  --rev caafeffa --freeze 5017e1f --json-out /tmp/c1.json
# exit 2 {"reason": "--json-out outside the lane root: /tmp/c1.json"}
```
The widening of this to "and the command needs `HYAKU_SCRATCH`/`TMPDIR` set to a non-`/tmp`
partition, or C1 exits 2" is F6/section 1 P2–P4. Both belong in the L1's landing note; the
frozen bytes are not to be edited.

**D4 — `/dev/shm` (and any tmpfs other than `/tmp`, `/var/tmp`) is accepted as a scratch
root.** `gate.TEMP_PARTITIONS` names only those two, so the C1 battery happily builds its
four fixture repos in shared memory, which is neither durable nor citable:

```sh
cd "$F" && env -u HYAKU_SCRATCH TMPDIR=/dev/shm python3 -I -B tools/round-47/exact.py \
  --root "$F" --freeze 46ae5eb4 --rev 46ae5eb4      # exit 0, failing []
```
`/dev/shm` residue after the run: 0 (`rmtree` in `finally`), but the evidence is gone with
the machine. This lives in frozen round-46 `gate.py` → route to round 48, not a C1 clause.

**D5 (scope, not a claim defect) — `out_path` protects graded names only.**
Accepted: `.ufo/state/x.json`, `.ufo/watchdog.log`, `.ufo/waves/round-47/w1/<sibling>/x.json`,
`.hidden/x.json`. Refused: every `GRADED` head, anything outside the lane, symlinks to graded
files. So `--json-out` can overwrite harness state or a sibling seat's report; no clause
claims otherwise, so this is a coverage finding, not a falsification.

**D6 (minor) — `--selftest` is dead from the CLI.** `--root/--freeze/--rev` are `required=True`
and argparse validates before `main` can honour `--selftest`, so every `--selftest`
invocation exits 2 on usage, in any environment:
`python3 -I -B tools/round-47/exact.py --selftest` → exit 2, `usage: … --root ROOT --freeze FREEZE --rev REV`.
The self-tests are therefore un-runnable as documented batch steps; the battery is the only
live self-check. (Same in `record.py`.)

## 4. What this does *not* show

* No /tmp write exists in either counter on the pristine bytes — I did not find the routed
  defect my seat was asked to look for, and M2b shows that an exit-code check alone could
  not have found it either. The routed defects above are about *where a receipt may be
  written*, not about scratch content.
* C2's clauses are untouched by scratch: P2–P4 receipts are byte-identical, so no clause
  can distinguish the environments. Nothing here scores R47-C2 either way.
* I did not evaluate any claim clause's truth; only the scratch surface. The C1 freezes
  (F6) and the block-24 pin (which follows A6) are other seats' ground.

## 5. Reproduction index

| file | content |
|---|---|
| `MutScratch/probe.sh` | matrix v1 (all four assigned probes plus graded/symlink/dir cases) |
| `MutScratch/probe2.sh` | matrix v2 (env modes × both counters, legal targets, residue checks) |
| `receipts/r2/exits.txt` | one line per probe: name, exit, env mode, json-out, reason |
| `receipts/r9/*` | re-run of the whole matrix at `31b092d1` (current HEAD) |
| `receipts/r4/{pristine,m1}.trace`, `receipts/r5/m2.trace`, `receipts/r6/m2b.trace`, `receipts/r8/c2.trace` | strace of `mkdir`/`mkdirat` (and unlink for C2) |
| `receipts/r3/pristine.out` | fixture-copy control, exit 0 |
| `receipts/r10/*` | D3 and D6 re-run on the current bytes (`/tmp/c1.json` refused, no file created; both `--selftest` exit 2 usage) |

Cleanup: `/fast/scratch/hyaku/kaidoku-r47/MutScratch` removed after these receipts were
copied here; `/tmp` and `/dev/shm` residue from my probes is 0 (`/tmp` pre-existing
`kaidoku-*` entries dated 26–28 Oct predate my probes and were left untouched; the only
`/tmp` dir a probe created was M2b's mutant output, removed with `rm -rf`).
