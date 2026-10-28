# R46W1 Labrat — battery cost (wall time, RSS, scratch), measured

Seat: `R46W1ProbeCost` (executor, single labrat). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch: `/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeCost` (removed at exit; receipts copied to
`.ufo/waves/round-46/w1/R46W1ProbeCost/receipts/`). No installs: `time` 1.9 and `hyperfine` 2.0.0
were already present; `/usr/bin/time` does **not** exist on this host (see §0).

Hypothesis under test: **"a full C1 + C2 run costs under 60 s and under 50 MB of scratch."**

Verdict: **not falsified** on either axis — 3.2 s wall (concurrent) and **3.99 MB peak scratch**;
but the hypothesis's own literal command never runs the battery (§1), and if "50 MB" is read as
*RSS* instead of scratch the two counters together sit at 47–52 MB, i.e. on the line (§4).

Environment: AMD Ryzen 9 9950X (32 threads), 31 GB RAM, xfs on `/fast` (nvme1n1p2), Python 3.14.8,
git 2.56.0, **loadavg 55–75** during the run (40+ sibling seats live — wall times below are on a
loaded host, not an idle one).

## 0. Tool deviation (honest capture)

`/usr/bin/time` is absent (`ls: cannot access '/usr/bin/time'`; `pacman -Qo /usr/bin/time` →
`error: No package owns /usr/bin/time`). GNU time 1.9 is at `~/.local/bin/time`; I used that and
record the substitution. `inotifywait`/`fatrace` are also absent, so scratch peak was measured two
independent ways: `du -sk` sampled at 4–20 ms, and an in-process `os.walk` sampler at 2 ms that also
records the per-fixture byte totals before each `rmtree`.

## 1. The hypothesis command as written is a red run and never touches the battery

The seat prompt's command is `--freeze 3182047… --rev 3182047…` (rev = freeze). At that commit
`SKILL.md` has **no block 23** and **no registry section**, so both counters fail a structural
clause and the battery is skipped by design:

| command (`python3 -I -B tools/round-46/<inst> --root <lane> --freeze 3182047… --rev 3182047…`) | exit | wall (5 runs) | maxRSS | scratch peak |
|---|---|---|---|---|
| `attest.py` | 1 (`marker_occurrences 0 != 1`, `block_present 0`, `rule_blocks 22`) | 102–345 ms, mean 195 ms | 23 292 KB (22.7 MiB) | **0 B** |
| `registry.py` | 1 (`markers: 0 open, 0 close`, `unregistered 38 of 38`) | 111–215 ms, mean 166 ms | 18 920 KB (18.5 MiB) | **0 B** |

Both print `"battery": {"skipped": "artefact fails a structural clause first"}`. So the literal
hypothesis is satisfied **vacuously** at 0.2 s / 0 B: the expensive path is never entered. Any
closure that claims "under 60 s / under 50 MB" from this command is reporting the do-nothing control.
The full cost must be measured at a revision that carries the artefact (§2).

## 2. Full run (battery executes): the number the closure actually pays

Measured pair: `--freeze 332f4884` (F5, the freeze the lane's own LOG names) `--rev 58eb04b6`
(A4, the first revision whose block-23 pin matches the F5 interpreter bytes). Instrument executed
from the worktree: `attest.py` sha256 `c4056131…`, `registry.py` sha256 `5e16e4af…`, `gate.py`
`c3ba6b93…` (identical at `332f4884`, `58eb04b6` and `HEAD=c0112995`).

| | wall (5 runs, min–max, mean) | maxRSS (`time -v`) | peak scratch (`du -sk` / exact walk) | fixture dirs | scratch churn (sum of fixture bytes) | leftovers |
|---|---|---|---|---|---|---|
| C1 `attest.py` | 0.98–1.21 s, **1.08 s** | 24.4–26.5 MiB (24 940–27 168 KB; `time -v` run 25 768 KB) | **724 KiB** / 599 032 B (44 files) | 10 (9 forged + the battery root) | 5.38 MB | 0 |
| C2 `registry.py` | 2.17–2.52 s, **2.35 s** | 21.1–22.1 MiB (21 640–22 668 KB; `time -v` run 21 828 KB) | **3 992 KiB** / 3 785 292 B (113 files) | 8 (7 forged + the battery root) | 26.49 MB | 0 |
| both, concurrent | **2.88–3.21 s** | — | 4 369 995 B sampled while both ran | — | — | 0 |
| full closure bundle¹ | **8.04 s** serial | — | 3 992 KiB | — | — | 0 |

¹ 2 selftests (`attest --selftest` 2.3 s / 18 cases, `registry --selftest` 0.9 s / 12 cases) +
C1 + C2 + both `--spec r45 --profile v1 --no-battery` fidelity reproductions.

Against the hypothesis bar: **60 s → 3.2 s** (19× margin; even the whole 8 s closure bundle is 7×
inside it) and **50 MB scratch → 3.99 MB** (12.5× margin). Peak scratch is one fixture at a time,
because each fixture repo is created, scored and `rmtree`d before the next: the registry's largest
fixture is 2.70 MB of worktree (SKILL.md 299 KB + the 38 census tools 2.39 MB) plus 1.08 MB of git
objects = 3.78 MB, which is the whole peak.

## 3. What dominates

**git subprocess spawns, ~70–94 % of wall.** Instrumented by wrapping `gate.git` (calls, seconds,
verbs) and, separately, `subprocess.run`:

| | git calls | of which lane-repo / fixture | `git show` | git share of wall | unique calls | repeat ratio | Python share |
|---|---|---|---|---|---|---|---|
| C1 | 235 (298 incl. fixture `init/add/commit`) | 94 / 141 | 226 | 0.96 s / 1.37 s = **70 %** (92 % when fixture subprocesses are counted) | 54 | **4.35×** | 0.41 s |
| C2 | 539 (581 incl. fixture) | 411 / 128 | 530 | 2.10 s / 2.70 s = **78 %** (94 %) | 168 | **3.21×** | 0.60 s |

Measured per-call cost on the lane repo: `git show rev:path` **3.78 ms**, `git cat-file -e`
1.96 ms, one `git ls-tree -r` over 37 434 entries 41 ms. Both counters re-read the same blobs:
C1 asks for 54 distinct `(rev, path)` pairs 235 times; C2 for 168 pairs 539 times — because every
fixture is scored twice (v1 + v2) and each scoring re-reads SKILL.md, the census and each scope
path. A memoised `gate.show` (same semantics, cache keyed by `(root, rev, path)`), measured by
monkey-patching in a driver against the unmodified instrument, cuts C1 0.933 s → **0.372 s** (−60 %)
and C2 1.637 s → **0.854 s** (−48 %). That is the single cheap optimisation available, and it is
worth ~1.3 s of the concurrent 3.2 s. It is **not** required by either claim.

Second-order: mkdtemp + `rmtree` are negligible (rmtree total 15 ms / 39 ms over 10 / 8 fixtures);
Python interpreter floor is 9.8 MB bare, 14.0 MB importing `gate`.

## 4. Calibration notes a closure must know

1. **Peak scratch ≠ RSS.** Scratch peak is 3.99 MB; each process's own peak is 25.6 MB (C1) and
   21.8 MB (C2), and run concurrently they sum to ~47 MB, i.e. within 6 % of the 50 MB line if the
   bar was meant as memory. The claim "under 50 MB" is true only in the scratch reading the seat
   prompt used (`du -s` of the scratch root). State the unit.
2. **`--json-out` cannot leave the lane** (measured: exit 2 `--json-out outside the lane root`,
   and `--json-out SKILL.md` → exit 2 `inside a graded or frozen surface`). A closure cannot write
   its receipt into its own scratch root; it writes inside `.ufo/waves/…`. Receipt size 3.3 KB / 3.1 KB.
3. **`-B` is load-bearing.** Running the counters with plain `python3` writes
   `tools/round-46/__pycache__/gate.cpython-314.pyc` (14 281 B) *inside the frozen directory*; it is
   `.gitignore`d, so `git status` stays clean and F5's dirty arm does not see it. The documented
   counting command uses `-I -B`, which suppresses it — the frozen tree's byte-identity survives
   only because of that flag.
4. **Determinism.** Five runs of each instrument at the same `(freeze, rev)` produced a
   byte-identical stdout receipt (C1 `0b3d8c3f…`, C2 `f4a0c39b…`), so cost is reproducible and a
   closure can diff receipts.
5. **Scratch root guard works and is cheap**: unset `HYAKU_SCRATCH`/`TMPDIR` → exit 2
   `no HYAKU_SCRATCH/TMPDIR root set` (0.04 s); `TMPDIR=/tmp` → exit 2
   `scratch root is a temporary partition: /tmp` (0.04 s). No partial scratch left behind.
6. **Host load matters**: at loadavg ≈ 67 the same C1 run took 1.55 s vs 1.07 s quiet; earlier
   hyperfine passes on the F4 bytes gave 2.08 s / 3.85 s means. Treat ±40 % as noise, not drift.

## 5. Receipts (exact commands, exit codes, stdout sha256, UTC)

All commands run from scratch cwd with `TMPDIR=HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeCost/…`,
`python3 -I -B`, root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, 2026-10-28T17:10–17:37Z
(`head=c0112995…`, loadavg 67.7/64.3/55.7 at the receipt batch). Per-row UTC is in
`R46W1ProbeCost/receipts/receipts.json`; rows there marked `approx` come from run order.

| # | command | exit | stdout sha256 (16) | wall | maxRSS |
|---|---|---|---|---|---|
| R1 | `attest.py --freeze 3182047… --rev 3182047…` | 1 | `dda3086b126619bb` | 0.10 s | 23 292 KB (22.7 MiB) |
| R2 | `registry.py --freeze 3182047… --rev 3182047…` | 1 | `8841358751b18788` | 0.09 s | 18 920 KB (18.5 MiB) |
| R3 | `attest.py --freeze 332f4884 --rev 58eb04b6` | 0 | `0b3d8c3f88f87b2c` | 1.07–1.55 s | 25 768 KB (25.2 MiB) |
| R4 | `registry.py --freeze 332f4884 --rev 58eb04b6` | 0 | `f4a0c39bf424b80e` | 2.17–2.96 s | 21 828 KB (21.3 MiB) |
| R5 | `attest.py --freeze 332f4884 --rev 58eb04b6 --json-out <lane>/.ufo/…/c1-F5.json` | 0 | `0b3d8c3f…` | 1.31 s | 24 812 KB (24.2 MiB) |
| R6 | `registry.py --freeze 332f4884 --rev 58eb04b6 --json-out <lane>/.ufo/…/c2-F5.json` | 0 | `f4a0c39b…` | 3.00 s | 21 828 KB (21.3 MiB) |
| R7 | `attest.py --freeze 332f4884 --rev HEAD` | 0 | (same receipt shape) | 1.15 s | 25 304 KB (24.7 MiB) |
| R8 | `registry.py --freeze 332f4884 --rev HEAD` | 0 | — | 2.54 s | 21 504 KB (21.0 MiB) |
| R9 | `attest.py --freeze HEAD --rev HEAD --selftest` | 0 | `6aa73c612069dd72` | 2.31 s | 21 828 KB (21.3 MiB) |
| R10 | `registry.py --freeze HEAD --rev HEAD --selftest` | 0 | `0fa8c31a6419905f` | 0.92 s | 18 072 KB (17.6 MiB) |
| R11 | `attest.py --freeze 332f4884 --rev 58eb04b6 --no-battery` | 0 | `0866041b0d3f220c` | 0.16–0.25 s | 24 184 KB (23.6 MiB) |
| R12 | `registry.py --freeze 332f4884 --rev 58eb04b6 --no-battery` | 0 | `8fe65a95e015bd00` | 0.32–0.45 s | 19 996 KB (19.5 MiB) |
| R13 | `census.py --root <lane> --rev 332f4884` | 0 | — | 0.21 s | 16 420 KB (16.0 MiB) |
| R14 | bundle: 2 selftests + C1 + C2 + 2 fidelity | 0/0/0/0/0/0 | — | **8.04 s** | — |

Peak-scratch receipts: C1 `du -sk` 724 KiB over 700 samples @4 ms and 300 samples @5 ms; exact
walker 599 032 B / 44 files; C2 `du -sk` 3 992 KiB over 900 samples @4 ms and 400 @5 ms; exact
walker 3 785 292 B / 113 files; both-concurrent `du -sb` peak 4 369 995 B. Every run reported
`leftover=0` after exit (`find <scratch> -mindepth 1` empty).

## 6. Findings outside the hypothesis (routed to L1, not fixed here)

These surfaced while measuring and concern the frozen instrument's *behaviour*, not its cost:

**F1 — the freeze named in the dispatch cannot score the landed artefact.** `tools/round-46/` is
touched by four later commits (50862e4a, 65678df0, 04252247, 332f4884), so with
`--freeze 3182047…` every rev that carries block 23 exits 2 `frozen_path_changed`. Measured:

```
attest.py   --freeze 3182047… --rev 04252247 → exit 2  frozen_path_changed ['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py', 'tools/round-46/registry.py']
registry.py --freeze 3182047… --rev 04252247 → exit 2  (same)
attest.py   --freeze 3182047… --rev HEAD     → exit 2  (same)
```
Block 23 first appears at 65678df0, i.e. after 50862e4a already changed the frozen paths — so the
pair (freeze 3182047, any artefact-bearing rev) is unscorable by construction.

**F2 — the bytes frozen at 3182047 cannot run a battery at all.** `gate.main_guard` in that
snapshot prints and `return 2` (an int) while both `main()`s do `code, receipt = gate.main_guard(...)`,
and `attest.py`'s `m_self_refs` names an undefined `REF`. Running the frozen copies
(`receipts/frozen-attest-3182047.py`, `receipts/frozen-registry-3182047.py`):

```
frozen attest.py   --freeze 04252247 --rev 04252247            → exit 1, {"reason": "unhandled NameError: name 'REF' is not defined"} + TypeError traceback  (0.56 s, 25 324 KB / 24.7 MiB)
frozen registry.py --freeze 3182047… --rev 3182047…            → exit 1, {"reason": "unhandled AttributeError: 'NoneType' … splitlines"} + TypeError traceback  (0.08 s, 19 084 KB / 18.6 MiB)
frozen attest.py   --freeze 04252247 --rev 04252247 --no-battery → exit 0
frozen registry.py --freeze 04252247 --rev 04252247 --no-battery → exit 0
```
A crash reported as **exit 1 with a traceback** is exactly what R45-CL13(f) forbids. F2/F3 fixed
this in 50862e4a/65678df0 — i.e. after the freeze the dispatch cites.

**F3 — the claims file's selftest count is wrong for registry, at the freeze.**
`plans/round-46-claims.md:194` says `registry.py --selftest` prints `cases=11`; the frozen bytes
print `REGISTRY_SELFTEST: cases=12 failures=0` and so does HEAD (12 `case(` calls at 3182047 and at
HEAD). `attest.py --selftest` is 15 at the freeze (matches line 192) and 18 at HEAD (F5 added 3).

**F4 — the fidelity sentences are only reproducible with an unstated `--no-battery`.**
`--spec r45 --profile v1` at `f59565b7`/`f762b727` with the battery enabled exits **2**
`IsADirectoryError … /tools/round-45/` (the r45 block cites the *directory* `tools/round-45/` and the
fixture builder `open()`s it as a file); registry's r45 profile with battery exits **1**
`battery v1_green 0 != 7`. With `--no-battery` both reproduce the control receipts exactly
(`rule_blocks 22, block_present 1, rows 10, refs 8, unresolved []`; scope 6, 6 registered). The
claim text gives the command without the flag.

**F5 — the pin binds, and it produced a transient red.** `--freeze 332f4884 --rev 332f4884` →
`attest.py` exit 1 `interpreter sha256 pin does not match the bytes at rev` (block 23 still pinned
`e6c44d2d…` while the F5 bytes are `c4056131…`), which A4 (`58eb04b6`) re-pins. `registry.py` was
already green there. So the scorable window for C1 opens at 58eb04b6, not at its own freeze.

**F6 — F5's dirty arm works** (verified on the clone): a non-ignored stray file in a frozen
directory → exit 2 `frozen_worktree_dirty` listing the path; the gitignored `__pycache__` is
invisible to it (see §4.3).
