# R45W2NoTmp — scratch discipline (round 45, wave 2)

Seat: `R45W2NoTmp` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: attack the *scratch discipline* of the landed round-45 instruments — the `/tmp`
literal audit, the "no new `/tmp` entries" property of every `--selftest`, and the claim
that a scratch location is injected through `HYAKU_SCRATCH`/`TMPDIR`.

## Observed revisions (calibration first)

| item | value |
|---|---|
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` |
| lane HEAD I probed | `0ee50aaff516571aa607769bbbdf19a3db90dfa5` |
| packet's "measured revision" A1 | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` — verified ancestor of HEAD, but **9 commits behind it** (A2, A3 and the w1 landings are on top) |
| `tools/round-45` + `plans/round-45-claims.md` freeze..HEAD | `git diff --stat f762b7..HEAD -- tools/round-45 plans/round-45-claims.md` → **0 lines** (byte-identical to the freeze) |
| gate at freeze..HEAD | `frozen-path-preflight --root . --freeze f762b7.. --rev HEAD --pathspec tools/round-45 --pathspec plans/round-45-claims.md --check-dirty --require-pathspec` → **0**, `touched[] = restored[] = blob_changed[] = dirty[] = []` |

So my probes ran against the freeze bytes even though the tip is later; every statement
below is anchored to the file sha256s in the receipts table, not to a commit id.

Tools under attack (sha256, read-only):

```
633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b  tools/round-45/frozen-path-preflight.py
2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509  tools/round-45/c1-counter.py
50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025  tools/round-45/c2-counter.py
9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993  tools/round-44/c1-counter.py
085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277  tools/round-44/c2-counter.py
c35d4b9bca6cd12e7ff1a89717da033841797dde5cf3f8bd3b262d3e9860b263  tools/round-44/c1-run.sh
```

## Verdicts

| # | attack | verdict |
|---|---|---|
| A1 | `/tmp` literal audit of `tools/round-45/*.py` | **holds** — no hardcoded `/tmp` root; the single hit is prose (A4 falsifies that prose) |
| A2 | each `--selftest` under `TMPDIR=$S` adds nothing under `/tmp` | **holds** — 3/3 exit 0, `/tmp` diff empty (twice) |
| A3 | scratch injected by `HYAKU_SCRATCH`/`TMPDIR` rather than only `--work` | **holds for the env half; falsified for the other half** — env is honoured by all three, but *none* of the three accepts a scratch argument, which `R44-SCR-TMP` names as a requirement |
| A4 | preflight docstring "never a bare /tmp root" + 3 registry write-scope cells "scratch under `$HYAKU_SCRATCH` or `$TMPDIR`" | **FALSIFIED** — with both unset the fixtures are created under `/tmp` |
| A5 | exit map: an unevaluable scratch state is `2` | **FALSIFIED** — it is `1`, i.e. indistinguishable from "violation" / "not met" |
| A6 | preflight leaves no fixtures behind | claim not made; **defect** — 11 dirs / 1.69 MiB per run, unbounded (c1 and c2 both `rmtree`) |
| A7 | c1's nested preflight run is contained | **holds** — both env vars are set to the work dir and the work dir is `rmtree`d in `finally` |
| A8 | round-44 c1-counter is hardened against the `/tmp` fallback | **holds** — no `gettempdir()`; `--work > $HYAKU_SCRATCH > /fast/scratch/hyaku` |
| A9 | c2-counter's *evaluate* path needs scratch | **holds (limit)** — it does not; a read-only scratch base still scores 0 |
| A10 | gate (evaluate) mode writes nothing | **holds** — no scratch dir created, `/tmp` diff empty; `--json-out` is unguarded (routed, low) |
| A11 | `/tmp/kaidoku-r45` present on the host | **observation only, not citable** — see limits |

---

## A1 — `/tmp` literal audit

```
$ grep -n '/tmp' tools/round-45/*.py
tools/round-45/frozen-path-preflight.py:26:$HYAKU_SCRATCH or $TMPDIR (never a bare /tmp root), runs every case, prints
EXIT=0
$ grep -rn '/tmp' tools/round-45/            # all file types
<same single line>
```

Classification: **one hit, a docstring sentence — not a hardcoded root.** It is, however,
a *claim*, and A4 shows it to be false as written. For contrast, the registered round-44
set has a deliberate host default, not a `/tmp` literal:

```
tools/round-44/c1-counter.py:456:    unset that resolves to /tmp (R44-SCR-TMP)."""   # comment
tools/round-44/c1-counter.py:460:    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
```

`/fast/scratch/hyaku` at :460 is a **hardcoded-root default** (routed, low — it is
documented in the function docstring and in `tools/round-44/c1-run.sh:25`, and it is
`makedirs`ed). The other `/fast/scratch/hyaku/kaidoku-r44/...` literals in that file
(:2657, :2846, :3053, :3131, :3135) build *synthetic receipt* payloads and expected
argv strings — fixture data, not roots; they create nothing.

## A2 — `--selftest` under `TMPDIR=$S` adds nothing under `/tmp`

Receipts (stdout sha256 over the exact bytes, `/tmp` name-filter `kaidoku|c1-|c2-|preflight`,
before/after sorted diff):

| tool | rc | stdout sha256 | UTC | `/tmp` diff |
|---|---|---|---|---|
| `frozen-path-preflight.py --selftest` | 0 | `00c89f9dd2b61c3b71a4d0ac73dbf623e4036feb6bafefd414444f80f4fc05c2` | 2026-10-28T16:00:43Z | empty (`diff_rc=0`) |
| `c1-counter.py --selftest` | 0 | `da889b6e53dadfa9a9e33eb3dfbbb7d1ca4290a4f69bb5c185bb302b6f79a848` | 2026-10-28T16:00:52Z | empty (shared window with c2) |
| `c2-counter.py --selftest` | 0 | `84153a60623b0a378f5bf314f712de8da321f1aed9d3ddc40f2044375eb7a9d5` | 2026-10-28T16:00:52Z | empty (`diff_rc=0`) |

Stronger form of the same receipt: all five `/tmp` snapshots I took (`tmp.before.txt`,
`tmp.after-pf.txt`, `tmp.post-two.txt`, `tmp.pre-iso2.txt`, `tmp.post-iso2.txt`) are
**byte-identical** — `sha256 c1276e1bd2931407949ec847ed5c5804241f3e1ec4d34f9e4385ca8de07f30ed`
for each. The listing did not change once across every run in this seat.

`PREFLIGHT_SELFTEST: cases=11 failures=0` · `C1_SELFTEST: cases=9 failures=0` ·
`C2_SELFTEST: cases=7 failures=0`. The case counts match the three registry rows.
Conclusion: **with `TMPDIR` set, not one byte lands under `/tmp`**, including from the
`git` children (git honours `TMPDIR`).

## A3 — how a scratch location is injected

Probe: import each tool with `-B` while `os.makedirs`/`tempfile.mkdtemp` are replaced by
recorders, so the *intended* path is observed and nothing is written
(`$S/probe_scratch.py`).

| env shape | preflight root | c1 root | c2 root |
|---|---|---|---|
| `HYAKU_SCRATCH` unset, `TMPDIR` unset | `/tmp/kaidoku-r45/preflight-selftest` | `/tmp/kaidoku-r45/c1-STUB` | `/tmp/kaidoku-r45` |
| `HYAKU_SCRATCH=""`, `TMPDIR=$S` | `$S/kaidoku-r45/preflight-selftest` | `$S/kaidoku-r45/c1-STUB` | `$S/kaidoku-r45` |
| `HYAKU_SCRATCH=$S/hs`, `TMPDIR=$S` | `$S/hs/kaidoku-r45/preflight-selftest` | `$S/hs/kaidoku-r45/c1-STUB` | `$S/hs/kaidoku-r45` |

* The env half **holds**: `HYAKU_SCRATCH` beats `TMPDIR` in all three, and the resolved
  path is under the variable in both set cases. Empirically confirmed by A2 (the fixtures
  appeared under `$S`).
* The other half is **falsified**: none of `frozen-path-preflight.py`, `c1-counter.py`,
  `c2-counter.py` has a `--work` flag (`--root/--freeze/--rev/--selftest/--json-out` only;
  `grep -n 'work' tools/round-45/*.py` finds only `run_preflight(..., work)` internals).
  The round-44 lineage requirement that `R44-SCR-TMP` records — *"counters must honour
  TMPDIR **and accept a scratch argument**"*
  (`.ufo/waves/round-44/w1/R44ConnRouted.md:29`) — is met by `tools/round-44/c1-counter.py`
  (`--work`, :455-460) and by `tools/round-44/c2-counter.py` (`--work`, :1631), and by
  **zero of the three round-45 instruments**. A seat cannot point scratch at a chosen
  directory except by mutating the process environment (which it can, and did).

## A4 — FALSIFIED: "under `$HYAKU_SCRATCH` or `$TMPDIR`"

Claim 1, `tools/round-45/frozen-path-preflight.py:25-26`:

> `--selftest` builds private git fixtures under `$HYAKU_SCRATCH` or `$TMPDIR`
> (never a bare /tmp root), runs every case, …

Claim 2, the three landed registry rows (`SKILL.md:1655`, `:1656`, `:1657`), write-scope
cell:

* preflight — "`--json-out` only; selftest fixtures under `$HYAKU_SCRATCH` or `$TMPDIR`"
* c1-counter — "`--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR`"
* c2-counter — "`--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR`"

Exact input (the differing value is the root):

```
$ env -u TMPDIR -u HYAKU_SCRATCH unshare -m -r --map-root-user bash -c \
    'mount --bind $S/iso2 /tmp && env -u TMPDIR -u HYAKU_SCRATCH ./tools/round-45/frozen-path-preflight.py --selftest'
rc=0   stdout sha256=00c89f9d…05c2   utc=2026-10-28T16:03:20Z
PREFLIGHT_SELFTEST: cases=11 failures=0
```

`/tmp` was a bind mount of my own empty scratch dir for the duration of that command, so
the host `/tmp` was untouched (`/tmp` name-filter diff `rc=0`) and the writes are fully
attributable. What the tool created **inside that `/tmp`**:

```
/kaidoku-r45
/kaidoku-r45/preflight-selftest
/kaidoku-r45/preflight-selftest/tmpqu139nz3/.git/…          (11 fixtures, one .git each)
```

The import probe shows the same resolution without writing anything:
`preflight.scratch_root() -> "/tmp/kaidoku-r45/preflight-selftest"`, and c1/c2 resolve to
`/tmp/kaidoku-r45/c1-STUB` / `/tmp/kaidoku-r45`. Code, `:50-58`:

```python
def scratch_root():
    for key in ("HYAKU_SCRATCH", "TMPDIR"):
        base = os.environ.get(key)
        if base:
            break
    else:
        base = tempfile.gettempdir()      # <- /tmp when both are unset
```

Same line, three files: `frozen-path-preflight.py:56`, `c1-counter.py:46`,
`c2-counter.py:174` (`... or tempfile.gettempdir()`, same semantics).

Why this is a falsification and not a reading quibble: the round-44 set already contains
the ruling. `tools/round-44/c1-counter.py:455-458` —

> `--work > $HYAKU_SCRATCH > /fast/scratch/hyaku.`
> `Deliberately never tempfile.gettempdir(): with TMPDIR and HYAKU_SCRATCH unset that`
> `resolves to /tmp (R44-SCR-TMP).`

So `R44-SCR-TMP` is *open* (`.ufo/waves/round-44/w2/R44W2ConnDefects.md:198`, resolution
criterion "counter fallback anchored"), and the two landed round-45 instruments that the
registry says implement the rule (`c1-counter.py`, and the preflight it invokes) re-open
it in the same breath as a docstring that says the opposite. The wave contract is also
stricter than the finding: "Never write under `/tmp`; nothing there is citable" — a tool
whose default is `/tmp` puts a non-citable fixture under every seat that forgets the env.

**Fix (minimal, matches the lineage):** in all three, replace the `else:` branch with a
refusal — `return 2` / `sys.exit(2)` printing `{"reason": "scratch_unset", "gate": …}` —
and add `--work` as the highest-precedence override, exactly like
`tools/round-44/c1-counter.py:455-460`. If instead the fallback is kept deliberately,
the docstring's parenthetical and the three registry write-scope cells MUST read
"`$HYAKU_SCRATCH`, else `$TMPDIR`, else the platform temp dir (`/tmp` when both are
unset)" — a claim must not be stronger than the code.

## A5 — FALSIFIED: a scratch failure reports `1` (violation), not `2` (unevaluable)

Input: the same three `--selftest` commands with the scratch *base* made unwritable.

```
$ mkdir -p $S/ro && chmod 500 $S/ro
$ TMPDIR=$S/ro ./tools/round-45/frozen-path-preflight.py --selftest   -> rc=1
$ TMPDIR=$S/ro ./tools/round-45/c1-counter.py           --selftest   -> rc=1
$ TMPDIR=$S/ro ./tools/round-45/c2-counter.py           --selftest   -> rc=1
utc=2026-10-28T16:02:14Z
  File "<frozen os>", line 236, in makedirs
  PermissionError: [Errno 13] Permission denied: '…/ro/kaidoku-r45'
```

and with `HYAKU_SCRATCH` naming a regular file: `rc=1`,
`NotADirectoryError: [Errno 20] … '/…/afile/kaidoku-r45'`.

Every one of these is an uncaught exception, so `python` exits **1** — the code the
registry rows define as "a frozen path changed" / "not met". No `PREFLIGHT_SELFTEST:`
line and no JSON receipt is printed either, so a caller reading only `rc` records a
violation that never happened.

This reaches the claim-scoring path, not just the selftests:

```
$ TMPDIR=$S    ./tools/round-45/c1-counter.py --root . --freeze f762b7… --rev HEAD
rc=0  sha256=231bc68312e7379d5a019744f768a4016a8f18d3c39a641a01b9284aa168fff5  16:02:23Z
     {"failing": [], "preflight_selftest": {"cases": 11, "exit": 0, "failures": 0, "ok": true}}
$ TMPDIR=$S/ro ./tools/round-45/c1-counter.py --root . --freeze f762b7… --rev HEAD
rc=1  (PermissionError traceback, no JSON)
```

Same revision, same bytes, opposite verdict driven only by whether `/fast` was writable.
The correct code is `2` ("could-not-evaluate"), and the wording of the exit maps already
reserves `2` for exactly this class ("usage, … a git call failing" —
`frozen-path-preflight.py:22-23`).

Calibration: the same experiment on **c2-counter's evaluate path** returns `rc=0`
(`met_target: true`, sha `d088a7c4…`) because that path never touches scratch. A5 is
therefore demonstrated for preflight `--selftest`, c1 `--selftest`, c2 `--selftest`, and
c1 evaluate — and **not** for c2 evaluate.

**Fix:** wrap the scratch-root creation in `try/except OSError` and emit
`{"reason": "scratch_unwritable", "path": <path>, "errno": …}` with exit 2. Never let a
`PermissionError` reach the interpreter's default exit.

## A6 — DEFECT: the preflight never removes its fixtures

```
$ TMPDIR=$S … --selftest           # run 1
$ TMPDIR=$S … --selftest           # run 2
after1: dirs=11 kib=1696 | after2: dirs=22 kib=3388 (delta dirs=11 kib=1692)
nested .git dirs left behind: 22        utc=2026-10-28T16:03:05Z
```

Linear growth: **11 directories, ~1.69 MiB and 11 real git repositories per run**, no
`shutil.rmtree` anywhere in the file (`grep -n rmtree tools/round-45/frozen-path-preflight.py`
→ nothing). `c1-counter.py:159` (`try/finally`) and `c2-counter.py:239` both remove theirs.
This is not a falsified claim (no landed sentence promises cleanup) but it is the same
class the round is about, and 11 git repos per gate run is how a shared `/fast` fills.
**Fix:** `base = scratch_root(); try: … finally: shutil.rmtree(base, ignore_errors=True)`
around the case loop.

Also calibrated: c2's `shutil.rmtree(workroot)` at `:239` is **not** in a `finally`
(each case catches its own exceptions, so the practical exposure is small; still a leak
on SIGINT or a print failure). Low.

## A7 — HOLDS: c1 contains the preflight it shells out to

`c1-counter.py:97-110` copies the interpreter out of the revision under test and runs it
with `env = dict(os.environ, TMPDIR=work, HYAKU_SCRATCH=work)`; `:155-159` wraps the call
in `try/finally: shutil.rmtree(work)`. Probe (outer env **unset**, work dir in scratch):

```
run_preflight(LANE, 'HEAD', $S/nesttest) -> {'ok': True, 'exit': 0, 'cases': 11, 'failures': 0}
$S/nesttest/frozen-path-preflight.py
$S/nesttest/kaidoku-r45/preflight-selftest     <- nested fixtures land under work
host /tmp diff: rc=0
```

So the `/tmp` default of A4 cannot be reached *through* c1-counter, and the nested 11
fixtures are removed with the work dir. Good design; the defect is the direct-invocation
path only.

## A8 / A9 / A10 — claims that survive

* **A8** `tools/round-44/c1-counter.py:451-461` is the hardened form; the docstring names
  `R44-SCR-TMP` and the code has no `gettempdir()`. Holds. Its `/fast/scratch/hyaku`
  default is a host-specific default, routed low (documented at `c1-run.sh:25`).
* **A9** c2-counter's evaluate path derives everything from git objects; read-only scratch
  still scores `0` (`met_target: true`). Holds — and it bounds A5.
* **A10** preflight in evaluate mode creates no scratch directory and touches no `/tmp`
  (count of fixtures before/after identical at 22; `/tmp` diff `rc=0`), consistent with
  `scratch_root()` being called only from `selftest()`. Holds for the gate.
  Routed low: `--json-out` is written exactly where named (`:160`, plain `open(...)`); a
  relative path would land in the caller's cwd — the fleet root for a seat that forgets
  the host guard — and nothing rejects `/tmp/<x>` or a lane path.

## A11 — observation, deliberately not used as evidence

`/tmp/kaidoku-r45` exists on the host (empty, mtime `2026-10-28 12:39:15 -0300`, i.e.
~20 min before this seat started, and empty because `preflight-selftest` is absent). Under
the contract nothing in `/tmp` is citable, my own runs added nothing there, and I cannot
attribute the directory to a specific seat or tool. It is recorded only as consistent
with A4's mechanism — the proof of A4 is the namespace run, not this directory.

## Receipts (all ran; nothing "green by assumption")

| # | command (cwd = lane root unless stated) | rc | stdout/observation sha256 | UTC |
|---|---|---|---|---|
| R1 | `grep -n '/tmp' tools/round-45/*.py` | 0 | 1 hit, `:26` | — |
| R2 | `TMPDIR=$S ./tools/round-45/frozen-path-preflight.py --selftest` | 0 | `00c89f9d…05c2` | 16:00:43Z |
| R3 | `TMPDIR=$S ./tools/round-45/c1-counter.py --selftest` | 0 | `da889b6e…a848` | 16:00:52Z |
| R4 | `TMPDIR=$S ./tools/round-45/c2-counter.py --selftest` | 0 | `84153a60…a9d5` | 16:00:52Z |
| R5 | `env -u TMPDIR -u HYAKU_SCRATCH unshare -m -r … mount --bind $S/iso /tmp && preflight --selftest` | 0 | `00c89f9d…05c2` (identical to R2 — output is env-independent) | 16:01:30Z, 16:03:20Z |
| R6 | gate: `--root . --freeze f762b7… --rev HEAD --pathspec tools/round-45 --pathspec plans/round-45-claims.md --freeze-path … --check-dirty --require-pathspec` | 0 | `2c0317b5…b2e2` | 16:02:05Z |
| R7 | `TMPDIR=$S/ro {preflight,c1,c2} --selftest` (ro = `chmod 500`) | **1**, **1**, **1** | `PermissionError` traceback | 16:02:14Z |
| R8 | `HYAKU_SCRATCH=$S/afile preflight --selftest` | 1 | `NotADirectoryError` | 16:02:14Z |
| R9 | `TMPDIR=$S ./tools/round-45/c1-counter.py --root . --freeze f762b7… --rev HEAD` | 0 | `231bc683…fff5` | 16:02:23Z |
| R10 | `TMPDIR=$S/ro ./tools/round-45/c1-counter.py --root . --freeze … --rev HEAD` | **1** | traceback, no JSON | 16:02:23Z |
| R11 | `TMPDIR=$S ./tools/round-45/c2-counter.py --root . --freeze … --rev HEAD` | 0 | `d088a7c4…2aa7` | 16:02:23Z |
| R12 | `TMPDIR=$S/ro ./tools/round-45/c2-counter.py --root . --freeze … --rev HEAD` | 0 | `d088a7c4…2aa7` (unchanged) | 16:02:23Z |
| R13 | import probes (recorder-stubbed `makedirs`/`mkdtemp`), 3 env shapes | 0 | path table in A3 | 16:01Z |
| R14 | `run_preflight(LANE,'HEAD',$S/nesttest)` | 0 | `{'ok': True, 'exit': 0, 'cases': 11}` | 16:01Z |
| R15 | leak: two consecutive `--selftest` runs | 0 | dirs 11→22, KiB 1696→3388 | 16:03:05Z |
| R16 | `runpy` + instrumented `tempfile.mkdtemp` over `tools/round-44/c2-counter.py --selftest` | 0 | 18 mkdtemp calls, all `dir=…/kaidoku-r44` | 16:02Z |

Retained in `.ufo/waves/round-45/w2/R45W2NoTmp/receipts/`: `tmp.before.txt`,
`tmp.after-pf.txt`, `tmp.post-two.txt`, `tmp.pre-iso2.txt`, `tmp.post-iso2.txt`,
`pf.out`, `pf-iso.out`, `c1.out`, `c2.out`, `r44c2-mkdtemp.json`.

## Corrections I made to my own hypotheses

* I first read `tools/round-44/c2-counter.py:1205,1390`
  (`work or HYAKU_SCRATCH or tempfile.gettempdir()`) as "ignores `TMPDIR`". **Wrong.**
  R16 shows the selftest's 18 `mkdtemp` calls all resolve `dir=…/kaidoku-r44` when only
  `TMPDIR` is set, because `gettempdir()` honours `TMPDIR`. Round-44 c2's only defect is
  the *both-unset* fallback, identical to A4. Its registry row's write-scope cell
  ("`--work`, `--json-out`") is accurate and does not claim otherwise.
* `c2-counter.py:1206-1207` has a second, narrower hole: if the chosen base is not a
  directory, `mkdtemp(prefix=…)` is called **without** `dir=`, i.e. straight into
  `gettempdir()` — a silent `/tmp` write even when `HYAKU_SCRATCH` was set to something
  unusable. Routed low (same fix as A4).

## Not run (and why)

* `tools/round-44/c1-counter.py --selftest` — its row requires `--pkg65 <rea-agents 6.5.0 root>`;
  I have no verified package root in this seat and its 47 cases are not my axis (its
  scratch resolution is verified by reading and by A8). `tools/round-44/c2-counter.py --selftest`
  was run (R16) but only instrumented for scratch resolution, not re-scored.
* `tools/round-44/c1-run.sh` — probe that calls REA; out of scratch scope beyond its
  `HYAKU_SCRATCH` header line (`:25`), verified by reading.
* Nothing installed; `pacman` untouched (host-paused). No writes outside
  `.ufo/waves/round-45/w2/R45W2NoTmp/` and `$S`; `git status --porcelain` shows only
  pre-existing untracked `.ufo/waves/round-45/**` paths, and
  `git diff --stat f762b7..HEAD -- tools/round-45 plans/round-45-claims.md` is empty.

## Risks / limits

* `/tmp` is shared with ~50 live seats; a before/after snapshot can be perturbed by a
  sibling. Mitigation used: the decisive test (R5) ran inside a private mount namespace,
  where only my tool could write, and R2/R3/R4 produced no additions at all.
* "never a bare /tmp root" admits a narrow reading in which `/tmp/kaidoku-r45/...` is not
  "bare". I reject that reading because the lineage's own comment (`c1-counter.py:455-458`)
  treats `gettempdir()` itself as the defect, and because the three registry cells name
  exactly two sources. If the L1 prefers the narrow reading, the *defect* stands
  unchanged and only its severity drops from "false claim" to "undocumented third source".
* Scratch-discipline only: I did not attack block 22's arms, the six rows' verdict maps,
  the sources, or the measured revision. A1's `1f4b27f8` being 9 commits behind HEAD is
  reported for the L1's reconciliation, not claimed as a defect.
