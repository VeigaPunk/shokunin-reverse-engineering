# Kaidoku round-20 — Scout: inherited state (wave 1)

Clock at write: `2026-10-20T17:50:04-03:00` (`date -Iseconds`). Lane tip observed:
`refs/heads/main = d1d981d2cc041dda4656c5b01d2c8445d8d17124`; baseline B
`14f0260ad319ecc26994381b2415d5a999003375` present (`git cat-file -t` → `commit`).
Read-only sweep: no lane file modified or deleted; no tool installed. Every command
below is pasted with its exit code; OBS = observed from a command or file, INF = inference.

## Probes

P1 `git -C LANE status --porcelain --ignored` → **exit 0**, 15 lines (11 `??`, 4 `!!`):

```
?? .ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-fixture/
?? .ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-sub-fixture/
?? .ufo/waves/round-20/evidence/census-start/
?? .ufo/waves/round-20/w1/
?? .ufo/waves/round-20/wave1-assignments.json
?? .ufo/waves/round-20/wave1-dispatch-attempts.json
?? .ufo/waves/round-20/wave1-dispatch.json
?? .ufo/waves/round-20/wave1-registration.json
?? .ufo/waves/round-20/wave1-registry.json
?? .ufo/waves/round-20/wave1-result-attempt1.txt
?? .ufo/waves/round-20/wave1-result-attempt2.txt
!! .jj/
!! .ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/
!! .ufo/waves/arc3-loop1-round4/tools/
!! .ufo/waves/round-18/tools/__pycache__/
```

P2 `find LANE/.ufo -name .git -prune -print` → **exit 0**, exactly 2 paths (both under the
round-19 scratch dir). Cross-check without the `.ufo` restriction
(`find LANE \( -path LANE/.jj -o -path LANE/.git \) -prune -o -name .git -print`) → exit 0,
same 2 paths: **no other nested repo exists in the lane**.

P3 `grep -n "lane-dead-no-report kaidoku round=20" /home/vgpnk/Projects/shokunin/.ufo/watchdog.log`
→ **exit 1 (no match)**. The file exists: 36995 B, 513 lines, mtime `17:29:03.901266610`.
`grep -n kaidoku` → 16 lines (listed in §1). `pgrep -g 2303206 -a` → **exit 1** (no process).

## 1 Watchdog — no round-20 lane-dead line; lane is demonstrably live

OBS — the complete kaidoku history in the log (line: text):
`:351` launch r1, `:383` `lane-round-failed kaidoku round=1 :: marker/contentless report;
NOT advancing`, `:384` launch r1, `:431/:432` r14 launch/complete, `:447/:448` r15,
`:458/:463` r16, `:477/:483` r17, `:486/:496` r18, `:500/:511` r19,
`:512` `2026-10-20T17:25:07-03:00 launch kaidoku round=20 pgid=2303206 driver=hyaku-inline attempt=1`.
There is **no `lane-dead-no-report kaidoku …` line for any round**; the only kaidoku failure
record is the round-1 `lane-round-failed` at `:383`.

OBS — the log's last line is `17:29:03 complete tsukuroi round=18`; it has no entry after
17:29 even though lane wave-1 files were written 17:43:24-17:47:16 and a `.pyc` at 17:48:21
(§3/§4). Only one `watchdog tick` line exists in the whole file (`:1`, 2026-09-28), so the
log is event-driven and tick cadence is not established from it.

OBS — `pgrep -g 2303206` finds no process, yet files continue to appear in LANE during this
sweep (two `wave1-*.json` files at 17:47:16, a `.pyc` at 17:48:21).
INF — for `driver=hyaku-inline` the recorded pgid is a short-lived launcher, not the round
driver, so **`pgid` in the launch line is not a liveness oracle**; a "dead lane" verdict must
not be derived from it. The absence of a round=20 `lane-dead-no-report` line is consistent
with a live lane, and no round-20 death event is recorded as of this write.

## 2 Untracked nested `.git` residue — the round-19 D1 footprint (still present)

| residue path (relative to LANE) | creator (traced) | mtime | content |
|---|---|---|---|
| `.ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-fixture/` | `.ufo/waves/round-19/verify.py:537-539` runs `.ufo/gates/custody-pair/custody-pair.py selftest --scratch <OUT>/scratch-custody` with `OUT` **inside the worktree**; the selftest calls `tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=base)` (`custody-pair.py:898`) | dir `16:46:23.167707608`, `.git` `16:46:23.181583535` | embedded repo; 2 **empty** commits `72fb50e c1`, `71695f3 c2` (`git -C repo-fixture ls-tree -r 71695f3` → no entries) |
| `…/custody-pair-selftest-k_zd4w5n/repo-sub-fixture/` | same call | dir `16:46:23.289768246`, `.git` `16:46:23.292367601` | embedded repo; 1 empty commit `72fb50e c1`; empty dirs `sub/`, `sub/deep/` |

OBS — timestamps/attribution corroborated by tracked receipts in the same dir: `repo-pre.txt:3`
`captured-utc: 2026-10-20T19:46:23Z` (= 16:46:23-03:00), `:10` `repo-root: …/repo-fixture`.
The whole subtree is 552K; 82 regular files sit at depth 1, and **85 files of this directory
are tracked and byte-clean at HEAD** (`git diff --stat HEAD -- <subtree>` empty; committed by
`2a6229f` @ `16:48:27`). **Only the two embedded repos are untracked residue.**

OBS — already routed: `corpus/lessons/round-19-verifier-spotcheck.md:29` (Leftovers row,
"defect (status-neutral), see D1"), `:33-35` ("nested Git repositories … written by the
custody-pair selftest at 16:46:23 -03 during verification; the other 85 files … are committed
at E"), `:180` (D1 bullet). `d1-residue-before.txt:1-4` (tracked at `d1d981d`) is the L1's own
17:42:59 byte-snapshot of the same two paths.

OBS — the guard D1 requires is **absent at baseline**: `custody-pair.py` contains no
`scratch_inside_worktree` string; `cmd_selftest` only rejects `/tmp*` and a non-directory base
(`:891-898`). `git diff --stat 14f0260 -- .ufo/gates/custody-pair/custody-pair.py` → empty.
INF — re-running round-19 `verify.py` in the lane today reproduces the residue (new random
suffix); only the fixed gate can refuse it, and the present two dirs are not removed by the fix.

## 3 Round-20 untracked artifacts — live wave-1 working set, not stale residue

All created after the declaration commit `d1d981d` (committer `2026-10-20T17:43:06-03:00`,
`kaidoku-shokunin`; `git show -s`), which tracked only the 6 declaration files.

| path | mtime | size | content (OBS) |
|---|---|---|---|
| `evidence/census-start/` (5 files) | `17:44:13.555064155` … `17:44:31.979119833` | 16K | `meta.txt`: rev `d1d981d…`, `sources-census exit=0`, `c1-census exit=1`; `sources-census.stdout` ends `kaidoku ok …/corpus/SOURCES.md`; both `.stderr` are 0 B |
| `w1/swarm-registry.json` | `17:43:24.838579473` | 20927 | swarm registry, schema `ufo-swarm-registry-v1` (per `wave1-dispatch.json`) |
| `wave1-dispatch.json` | `17:43:24.840116033` | 181849 | schema `ufo-swarm-wave-dispatch-v1`, `wave: kaidoku-r20-w1`, `counts: spawn 100` |
| `wave1-result-attempt1.txt` | `17:44:04.336602732` | 11339 | `Failed to start background task jobs: … Background job limit reached (100)…` |
| `wave1-dispatch-attempts.json` | `17:46:42.174978984` | 169 | attempt1 `refused:100 chars:11339`; attempt2 `refused:0 chars:7555` |
| `wave1-result-attempt2.txt` | `17:46:42.175110724` | 7555 | `Spawned 100 background agents using executor, scout, reviewer, …` |
| `wave1-assignments.json` | `17:47:02.868927443` | 5408 | seat/assignment set (created during this sweep) |
| `wave1-registry.json` | `17:47:16.386819374` | — | registry mirror (created during this sweep) |
| `wave1-registration.json` | `17:47:16.391587612` | 23671 | registration record (created during this sweep) |

OBS — the last three appeared **after** this sweep started (first status did not list them),
which independently confirms a live writer. INF — creator is the L1's wave-1 dispatch path
(`gen-wave1.py` is tracked at `d1d981d`; `wave1-result-attempt2.txt` names 100 spawned seats);
whether these files are committed is the L1's integration decision, not seat residue.

## 4 Ignored entries — classified, none is round-20 residue

- `.jj/` — jj store, self-ignored by `.jj/.gitignore:1:/*` (`git check-ignore -v .jj` → that
  file). OBS: written `17:43:06.727`-`17:43:08.716`; the op-store records (`.jj/repo/op_store/operations/`)
  contain `jj … file track --include-ignored … claims.json contract.md gen-wave1.py wave1-spec.json
  manual-arm.json d1-residue-before.txt`, `jj … diff --summary`, `jj … metaedit --update-author`,
  and `jj … commit -m 'round-20: declare claims C1 calibration, C2 coverage, C3 depth; …'`.
  These are the L1's declaration-commit operations and match `d1d981d`'s committer instant; no
  seat-side jj write is evidenced here.
- `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/` — ignored by
  `.ufo/waves/arc3-loop1-round1/.gitignore:1`; old arc3 wave, unrelated to rounds 19/20.
- `.ufo/waves/arc3-loop1-round4/tools/` — 0 tracked files; every child is ignored by
  `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/.gitignore` (content `*`), so git collapses the
  directory as ignored. Old arc3 wave, unrelated.
- `.ufo/waves/round-18/tools/__pycache__/jj-red-before.cpython-314.pyc` — 66933 B, mtime
  `17:48:21.672620771` (**created during this sweep**), ignored by root `.gitignore:1`
  (`__pycache__/`). OBS: host `python3 -V` = `3.14.8`; a `.pyc` is written only for an *imported*
  module (not `__main__`), so some process imported `jj-red-before` from the LANE copy.
  INF: actor not recoverable from the filesystem (candidate: a wave-1 seat verifying D6f, or
  L1 tooling); this is a tool run against LANE without `-B`, contrary to the convention
  `python3 -I -B` (`contract.md:32`) and — for a read-only seat — to "write only your report"
  (`contract.md:21-22`). It is the only residue created during round 20 outside `round-20/`.

## 5 Interface conflict the D1 fix must resolve (code-level, not opinion)

OBS — `default_scratch()` (`custody-pair.py:752-759`) searches `$CUSTODY_PAIR_SCRATCH`,
`/dev/shm`, `/var/tmp`; `/tmp*` is refused with `USAGE: /tmp is excluded scratch (EDQUOT hazard)`
(`:891-893`). `TMPDIR` is unset on this host, so `tempfile.mkdtemp()` defaults under `/tmp`.
INF — contract `contract.md:23-24` ("every selftest, fixture repo and scratch dir lives under
`tempfile.mkdtemp()` in the system temp dir") and this tool's `/tmp` refusal are mutually
exclusive unless the fixed selftest ignores `--scratch` for its own fixture root or treats
`/dev/shm`/`/var/tmp` as the permitted system-temp base. Also `custody-pair.py` has no
`shutil.rmtree` of the fixture root, so "leaves no `custody-pair-selftest-*` dir under DIR on
exit" (`contract.md:38-40`) is not merely unguarded — it is unimplemented at baseline.

## 6 Gaps

- mtime is not authorship: for untracked/ignored paths no LANE-side pid→path audit exists.
- Watchdog tick cadence is unestablished (one tick line in 513); "no round-20 lane-dead line"
  is a true absence, not proof the watchdog is watching.
- The two fixture commits are empty trees; there is no file content to mine from them.
- The `c1-census exit=1` in `census-start/meta.txt` is the pre-fix baseline at `d1d981d`
  (D4/CensusRekey scope), observed, not re-judged here.

Report: .ufo/waves/round-20/w1/ScoutInheritedState.md
