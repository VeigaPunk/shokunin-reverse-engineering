# R46W1ProbeTmp — probe seat, round 46 wave 1

Lane: `kaidoku-shokunin`. Seat: `R46W1ProbeTmp` (leaf; no subagent dispatch available to this seat, so the
single labrat task in the seat spec was executed in-seat and its report is at
`.ufo/waves/round-46/w1/R46W1LabratTmp/report.md`).

**Hypothesis under test:** *the round-46 battery writes nothing outside the scratch root it is given.*

**Verdict: NOT falsified** — for the canonical counting invocation (`python3 -I -B …`), the attest battery and
the registry battery each write **only** under `$HYAKU_SCRATCH`; every traced creation is removed at exit; and
both counters refuse to run at all when the scratch root is absent or is `/tmp`/`/var/tmp`. Two scoped
exceptions exist and are reported below as findings, not as leaks of the battery: the explicit `--json-out`
channel (one file, by request, confined to the lane and outside graded/frozen surfaces), and CPython bytecode
caching when the interpreter is invoked **without** `-B` (F4).

## 0. Inputs and identity

| item | value |
|---|---|
| freeze named by the wave prompt | `31820472784284727546808acc31b3ea1e73919b` |
| freeze the claims file derives (`git log --format=%H -1 -- plans/round-46-claims.md`) | same: `31820472784284727546808acc31b3ea1e73919b` |
| measured revision used for runs | `49e6cac4f6604986b1a7e9cfcbd9d46704dff390` (HEAD) |
| scoring freeze used for runs | `0425224756791b414454df28a9abf93dcdf154ce` (the F4 freeze the L1's own receipts use) |
| python / git / strace | 3.14.8 / 2.56.0 / 7.2 |

The two freezes differ because `tools/round-46/` was modified **after** the commit the claims file names as the
freeze. That is finding **F1**; it is why the runs below use `--freeze 04252247 --rev 49e6cac4` (the only pair that
is both clean and green) and why the prompt's freeze is additionally exercised as a red control (r7).

## 1. Method

1. Baseline snapshot of the shared temporary partitions, exactly as specified and additionally as a name/mtime set:
   `find /tmp /var/tmp -maxdepth 2 -newermt '-5 minutes'` plus `os.walk` over `/tmp`, `/var/tmp` at depth ≤ 2.
2. `trap`-equivalent: scratch root `S=/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeTmp`, `HYAKU_SCRATCH=S`, `TMPDIR=S`.
3. Three assigned runs (`--selftest`, `--no-battery`, full battery) plus the registry battery, all under
   `strace -f -y` with every write-capable file syscall (`open/openat/creat/mkdir/unlink/rename/link/symlink/
   chmod/utimensat/truncate/write/pwrite64/…`).
4. Every traced path resolved with its real base: `AT_FDCWD<…>` decoration, the syscall's dirfd decoration
   (`3</dir>, "name"` for `unlinkat`/`renameat`/…), else the pid's last known cwd. Unresolved events were required
   to be zero, and they are zero in both traces.
5. Post-run snapshot; name-set diff against the baseline; scratch census; per-path existence test for every path
   the traces showed being created under `S`.
6. Negative controls: scratch root `/tmp`, no scratch root, `--json-out` outside the lane / into graded or frozen
   surfaces / through symlinks; and an injected mid-battery exception to exercise the cleanup `finally`.

## 2. Receipts (exact commands, exit codes, stdout sha256, UTC)

All commands run with `cwd=/home/vgpnk/Projects/shokunin`, `PY=/usr/bin/python3`, `ATT=<lane>/tools/round-46/attest.py`,
`REG=<lane>/tools/round-46/registry.py`, `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`--freeze 0425224756791b414454df28a9abf93dcdf154ce --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390`
unless stated. Full commands, environments and stdout/stderr bodies: `evidence/receipts.json` + `evidence/*.stdout`.

| # | run | exit | expect | UTС start–end | stdout sha256 (16) |
|---|---|---|---|---|---|
| r1 | `attest.py --root … --selftest` (literal claim text) | **2** | 0 | 17:04:07–17:04:07 | `e3b0c44298fc1c14` (empty) |
| r1b | same + `--freeze REV --rev REV` | 0 | 0 | 17:04:07–17:04:18 | `0bf8f4c6ae0e46a0` |
| r2 | `… --no-battery` | 0 | 0 | 17:04:18–17:04:18 | `8c55d92fc9cd0a40` |
| r3 | full battery | 0 | 0 | 17:04:18–17:04:25 | `4fca83c63d4b3ca6` |
| r4 | full, `HYAKU_SCRATCH=/tmp/r46probe-tmp` | 2 | 2 | 17:04:44 | `6431210817a725f1` |
| r5 | full, `HYAKU_SCRATCH`+`TMPDIR` unset | 2 | 2 | 17:04:44 | `ef924935c3857505` |
| r6 | full, `--json-out /tmp/r46probe-out.json` | 2 | 2 | 17:04:44 | `07629685231d5877` |
| r7 | full, `--freeze 3182047… --rev 49e6cac4` | **2** | 2 | 17:04:44 | `5b72067d19c30ce9` |
| r8 | full, `--json-out <seat>/c1-r8-receipt.json` | 0 | 0 | 17:04:44–17:04:46 | `4fca83c63d4b3ca6` |
| r9 | full battery **under comprehensive write trace** | 0 | 0 | 17:04:52–17:04:58 | `4fca83c63d4b3ca6` |
| r10 | `registry.py` full battery | 0 | 0 | 17:06:46–17:06:49 | `67b4dac13f00b0a7` |
| r11 | `registry.py --root … --selftest` (literal claim text) | **2** | 0 | 17:06:49 | `e3b0c44298fc1c14` (empty) |
| r11b | same + `--freeze REV --rev REV` | 0 | 0 | 17:06:49–17:06:50 | `0fa8c31a6419905f` |
| r12 | `registry.py` full **under comprehensive write trace** | 0 | 0 | 17:06:57–17:07:14 | `67b4dac13f00b0a7` |
| r14 | copy of `attest.py` patched to raise inside `run_battery` | 2 | 2 | 17:08:14 | `9f29a940444bc522` |
| r15 | `--json-out SKILL.md` | 2 | 2 | 17:08:22 | `5f8ad68395deded0` |
| r16 | `--json-out tools/round-46/leak.json` | 2 | 2 | 17:08:22 | `6ce1d5f7b2f24e86` |
| r17 | `--json-out <seat>/evil-link.json` → `/tmp/r46probe-evil.json` | 2 | 2 | 17:08:22 | `7e00cf18b0897cb4` |
| r18 | `--json-out <seat>/skill-link.json` → `SKILL.md` | 2 | 2 | 17:08:22 | `39cc50e92fb5c1e2` |

Instrument answers in those runs (all green, matching the frozen predicates):

- r3/r9: `forgeries_total 9, v1_green 9, v2_green 0, genuine_green 1, v2_crash 0`, `met_target true`,
  `failing []`, `rule_blocks 23`, `rows 13`, `refs 9`, `frozen_path_changed []`, pin == expected
  (`e6c44d2d…532346`).
- r10/r12: `scope_size 38`, `registered` 38, `unregistered []`, `thin []`, `absent_at_rev []`,
  `forgeries_total 7, v1_green 7, v2_green 0, genuine_green 1`, `met_target true`.

## 3. Write-scope result (the hypothesis)

| trace | write-class syscalls | resolved inside `S` | `/dev/null` | outside `S` | unresolved |
|---|---|---|---|---|---|
| r9 attest battery | 2523 | 2208 | 314 | **1** (the requested `--json-out` file) | 0 |
| r12 registry battery | 4633 | 4041 | 592 | **0** | 0 |

- Zero `.pyc` write opens in either trace (`-B` honoured).
- Zero writes inside the lane repository, its `.git`, `/tmp`, `/var/tmp`, `$HOME`, or any other path.
  The counters do *read* the lane (`git -C <lane> show`, `rev-parse`, `log`); all of those events are read-only.
- `/dev/null` (`O_RDWR`, 314/592 events) is a device node: no persistent bytes; excluded from "writes" but counted
  so the exclusion is auditable.

**Scratch census and removal:** the attest trace shows 641 distinct paths created under `S`
(`kaidoku-r46-battery-bc0epoq3/` and its nine `fx-*/` one-commit fixture repos). After exit, **0 of them exist**;
the only traced path still present is `S` itself, which this seat created before the run. The registry trace
is the same: 631 distinct paths under `S`, **0 still existing**, no `kaidoku-r46-battery-*` root on disk
(`evidence/r12-census.json`). After every run: `[n for n in os.listdir(S) if n.startswith("kaidoku-r46-battery")] == []`.
The injected mid-battery exception (r14) exits 2 with
`{"reason": "unhandled RuntimeError: injected mid-battery failure"}` and also leaves no scratch directory, so the
`finally: shutil.rmtree(scratch_root)` path is exercised, not merely inspected.

**Negative controls behave as the claims say:** `/tmp` scratch → exit 2
`scratch root is a temporary partition: /tmp/r46probe-tmp`; no scratch root → exit 2 `no HYAKU_SCRATCH/TMPDIR root
set`; neither created anything. `--json-out` refusals (r6, r15–r18) returned exit 2 and created nothing —
including through a symlink into `/tmp` and a symlink to `SKILL.md` (`realpath` is taken before the containment
test).

**Leftover paths with mtime: none.** No file created by any of these runs survives.

## 4. The prescribed snapshot method is not diagnostic under concurrency (calibration)

`find /tmp /var/tmp -maxdepth 2 -newermt '-5 minutes'` returned **235 entries before any run started** (sibling
seats' files). Across the run window the name set gained 253 and lost 172 entries; of the 255 window-new entries,
**none** matches the instrument's patterns (`kaidoku-r46-battery-*`, `kaidoku-r46-selftest-*`, `fx-*`, `self-*`)
and every one belongs to another lane/seat: `tameshi-r14-evidence-disposition-selftest.*` (45),
`tameshi-r17-registry-check-selftest.*` (~150), `tameshi-r4-2-regression.*` (2), plus `ed.*.out/err`, `rc.strace`,
`census-r55-rev01.txt`, `claude-tool-count-*`, `scribe-block-extract2.md`. A post-hoc `find … -name
'kaidoku-r46-battery-*'` over `/tmp /var/tmp` is empty. Conclusion: the before/after mtime diff can only *suggest*
leakage here; attribution needs the syscall trace (or a private mount namespace). Recorded so the next seat does
not read a sibling's `/tmp` file as this battery's leak.

## 5. Findings for the L1 (reported, not fixed)

### F1 — the freeze the claims file derives is not the freeze the instruments were scored at (blocking for a literal reading)

- `git log --format=%H -1 -- plans/round-46-claims.md` → `31820472…` (what the claims file itself says the freeze is).
- `git log --oneline --name-status 31820472..HEAD -- tools/round-46/ plans/round-46-claims.md` shows **three**
  later commits touching the frozen directory: `50862e4a` (attest/gate/registry), `65678df0` (attest),
  `04252247` (registry). Their messages declare `50862e4a`/`04252247` "the authoritative freeze"; that
  declaration lives only in commit messages, not in the claims file, and the claims file says
  *"Nothing in this file or in `tools/round-46/` changes after the freeze: a change makes both counters exit 2
  frozen_path_changed."*
- Consequence, measured: `attest.py --freeze 31820472… --rev 49e6cac4` → **exit 2**, receipt
  `blob_changed: ["tools/round-46/"], frozen_path_changed: ["tools/round-46/"]` (r7, sha `5b72067d19c30ce9`).
  So the wave prompt's freeze cannot score at any rev that carries the landed block 23.
- Byte-level drift: `sha256(tools/round-46/attest.py)` = `dd1e7df1…` at `3182047`, `eba59958…` at `50862e4a`,
  `e6c44d2d…532346` at `65678df0` and `04252247` and on disk. Block 23's pin is the **last** value, so the pin
  pins bytes that did not exist at the named freeze.
- Probe-visible symptom of the same drift: the claims file's preflight says `attest.py --selftest` prints
  `cases=15 failures=0` and `registry.py --selftest` prints `cases=11 failures=0`; the bytes on disk print
  **`cases=16`** and **`cases=12`** (r1b/r11b).
- Needed decision (L1's, not mine): re-derive the freeze by a new claims commit that lands after the last tool
  edit, or amend the claims file's freeze definition to "the last commit touching `tools/round-46/`", and re-pin.
  Until then a diligence reviewer can reproduce "exit 2" from the wave prompt's freeze with one command.

### F2 — the documented selftest invocations exit 2 (both instruments)

`attest.py --root <lane> --selftest` and `registry.py --root <lane> --selftest` exit **2** with empty stdout and
`error: the following arguments are required: --freeze, --rev` (r1, r11). `--selftest` is handled after parsing,
and `argparse` marks `--freeze`/`--rev` required unconditionally. The documented preflight therefore does not run
as written; with two throwaway revisions added (`--freeze REV --rev REV`) both run and pass (r1b: 16/0, r11b: 12/0).
Cheap fix if the L1 wants it: `required=False` for those two, or document the full invocation in the claims file.

### F3 — block 23's `R45-CL15 | dirty` row names an arm no code path executes (non-discriminating row in the landed artefact)

- `SKILL.md:622` (block 23) asserts
  `| R45-CL15 … | dirty: the dirty scope is the union of the pathspecs, and each arm has a red case that names it | 1 |`.
- `grep -rn '\bdirty(' tools/` → **no caller**; the only occurrence is `gate.py:132 def dirty(...)`. Both counters
  call only `gate.freeze_state` (`attest.py:442`, `registry.py:390`), which computes the history arm and the blob
  arm; it never consults `gate.dirty`.
- The attest selftest's 16 cases contain **no** dirty-scope case (names: green, no-marker, two-markers,
  marker-not-last, title-unnumbered, header-inexact, rows-thin, exit-cell, routed-id-missing, arm-vocabulary,
  ref-no-selector, ref-outside-allowlist, pin-mismatch, malformed-heading, frozen-touched, green-with-battery).
- The C1 predicate (clause 4) only requires the arm cell to belong to the vocabulary, so the counter scores this
  row green while the arm it advertises cannot fail anything. That is the round-45 defect class
  ("a row that cannot discriminate") surviving inside the round-46 measure. A clause that would catch it:
  each vocabulary token used by a row must be reachable from a computed value and from a named red selftest case.

### F4 — the bytecode cache is a write outside the scratch root whenever `-B` is dropped, and it lands inside the frozen directory

- Demo on a **copy** of the tools (`S/pycopy`, lane untouched): `python3 -I <copy>/attest.py … --no-battery`
  exits 0 and creates `<copy>/__pycache__/gate.cpython-314.pyc` (r13).
- The lane already carries this: `tools/round-46/__pycache__/{gate,attest,registry}.cpython-314.pyc` with mtimes
  **13:53:37 / 13:54:50 / 14:00:26** — i.e. written by earlier seats' imports, `git check-ignore`d
  (`.gitignore:1 __pycache__/`), invisible to `git status`, to the history arm and to the blob arm.
- Therefore `-B` in the counting command is load-bearing for the write-scope claim, and the sha256 pin covers only
  `attest.py` source bytes, not the cache. Nothing in the predicate fails if a seat runs without `-B`; each such
  run leaves a new file in the frozen directory. (My runs used `-B`; the trace shows zero `.pyc` writes and I did
  not modify or remove the pre-existing caches.)

### F5 — `--json-out` relative paths resolve against the process cwd, not `--root` (minor, no leak)

`gate.out_path` calls `os.path.realpath(path)` before comparing with `realpath(root)`. With cwd outside the lane,
`--json-out SKILL.md` is refused as "outside the lane root" rather than "inside a graded surface"; with cwd inside
the lane it is refused for the graded reason. Both exits are 2 and nothing is written (r15/r16), but the message
depends on invocation directory. Absolute paths and symlinks are handled correctly (r17/r18).

## 6. Read-only attestation of this seat

- `git -C <lane> status --porcelain -- tools plans SKILL.md corpus LOG.md SCORECARD.md` → **empty**
  (`evidence/frozen-surfaces.json`).
- Frozen surfaces on disk equal their bytes at `HEAD` (sha256 equality for `attest.py`, `gate.py`, `registry.py`,
  `census.py`, `census.json`, `plans/round-46-claims.md`); mtimes all predate this seat's first run
  (13:44–14:00 local vs 14:04 first run).
- Writes made by this seat: only under `.ufo/waves/round-46/w1/R46W1ProbeTmp/` (this report + `evidence/`), the
  flat `.md` report, the named labrat report, and `$HYAKU_SCRATCH` (removed at exit). The one `--json-out` write
  (r8/r9) is inside this seat's directory, as `gate.out_path` requires.
- No commits, stages, checkouts or other mutating git calls. No package installs were needed.

## 7. Evidence index (`evidence/`, sha256 of the large items)

| file | content |
|---|---|
| `receipts.json` `b16b65c259f98c23…` | every run: exact argv, cwd, env, exit, UTC window, stdout/stderr sha256, output file |
| `r9-full-writeset.trace.gz` `293e17c86add0a4e…` | attest battery, all write-capable syscalls, `-f -y` (15 168 lines) |
| `r12-registry-writeset.trace.gz` `50c0ce8c58371751…` | registry battery, same trace set (31 946 lines) |
| `write-attribution.json` `f582f2f0c2f23404…` | per-trace counts: inside/outside/`/dev/null`/unresolved |
| `tmp-var-tmp-diff.json` `6d9ee35f7de98401…` | baseline and post name/mtime sets for `/tmp`, `/var/tmp` |
| `frozen-surfaces.json` `2958213c5f86fbdb…` | frozen file sha256 + mtimes + restricted `git status` |
| `*.stdout`, `*.stderr` | verbatim output of every run in the table |
| `../c1-r8-receipt.json`, `../c1-r9-receipt.json` | receipts written by the instrument through `--json-out` |

Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeTmp` was removed after these files were copied here; no path
under `/tmp` was created or is cited.
