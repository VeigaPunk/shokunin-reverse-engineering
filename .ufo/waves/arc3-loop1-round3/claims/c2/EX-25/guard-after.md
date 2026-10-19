# EX-25 guard-after — write-guard scope, the clobber attempt `--paths X --out X`

Seat EX-25, chain c2, wave `arc3-loop1-round3`, 2026-10-19, repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Task: measure the **after-state**
of the VZ-4 A11 / D7 write-guard hole — the clobber attempt `--paths X --out X`
on scratch must be **refused** with the attacked file's **bytes intact**.

All scratch under `/var/tmp/ex25` (never `/tmp`). No git mutation. No custody path
written, renamed, or `utime`d: custody paths were opened for reading only (sha256 +
`lstat` capture), and every `--out` target in every case below lives under
`/var/tmp/ex25/probe` (for the canonical-set branch the probe uses a decoy-armed
copy of the tool whose `CUSTODY_PATHS` tuple points at `/var/tmp/ex25/probe/host/*`
— no real operator file is ever named as an output).

Artifacts: `guard-probe.py` (10-case harness), `probe-before.{txt,json}`,
`probe-after-candidate.{txt,json}`, `probe-rev-<sha>.{txt,json}` (per landed
revision), `raw-transcript.{sh,txt}` (shell-level record), `candidate-guard.diff`
+ `candidate-guard-extended.py`, `selftest-before.txt`,
`selftest-after-candidate.txt`, `custody-readonly-control.txt`,
`sha256-manifest-final.txt`, `/var/tmp/ex25/revision-probe-log.txt` (churn record).

## 1. What the hole is (code cite, before-state revision)

`custody-pair.py:564` at revision `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(round-2 v2 tool, still the base of every round-3 revision at probe time):

```python
        if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}:
            print("USAGE: refusing to write a receipt over a custody path: %s" % out, file=sys.stderr)
            return EXIT_USAGE
```

The guard's scope is the **canonical 5** only. Any `--paths` override escapes it:
the tool reads X, then writes the receipt *into* X. The declared round-3 fix is the
union guard `set(paths) ∪ CUSTODY_PATHS`.

## 2. Before-state (first-hand, revision `112d01dc…`, 13:07–13:09Z)

Raw transcript, seat-line case (`raw-transcript.txt`):

```
--- [before] tool sha256: 112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa
--- [before] X before: e1349782960b4f86436715dd750fdc2a6bc9aa9b08b55c51bab5df18e3f275fd  inode=11224639 mtime_ns=1792415330 ctime=1792415330 size=550
--- [before] $ python3 .../before/custody-pair.py capture --paths /var/tmp/ex25/raw/before/X --out /var/tmp/ex25/raw/before/X
RECEIPT: /var/tmp/ex25/raw/before/X  sha256=bfdef3fdbeef08a64f89a3c1f77934febcdc7f7e73c82ca2db2c3f4a88be49e4
SIDECAR: /var/tmp/ex25/raw/before/X.sha256
CUSTODY_PAIR_CAPTURE: OK paths=1/1 label=(none) exit=0
--- [before] exit=0
--- [before] X after : bfdef3fdbeef08a64f89a3c1f77934febcdc7f7e73c82ca2db2c3f4a88be49e4  inode=11224639 size=1295
```

exit **0**, "OK", and X is replaced by its own receipt (550 B → 1295 B; sha256,
size, mtime_ns, ctime_ns all moved) plus a stray `X.sha256` sidecar.

## 3. After-state, candidate pre-verification (`2ec0788f…`)

The declared fix applied to the scratch copy (`candidate-guard.diff`):

```diff
-        if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}:
-            print("USAGE: refusing to write a receipt over a custody path: %s" % out, file=sys.stderr)
+        guarded = {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}
+        guarded |= {p.resolve() for p in paths}
+        if out.resolve() in guarded:
+            print("USAGE: refusing to write a receipt over a path it measures"
+                  " or a custody path: %s" % out, file=sys.stderr)
             return EXIT_USAGE
```

Same command, same scratch shape:

```
--- [candidate] X before: 5c837cec076f2d34012559318f9230b5c323e6cd37345465baff8f27909713fe  inode=11224643 size=625
--- [candidate] $ python3 .../after/custody-pair.py capture --paths .../candidate/X --out .../candidate/X
USAGE: refusing to write a receipt over a path it measures or a custody path: /var/tmp/ex25/raw/candidate/X
--- [candidate] exit=2
--- [candidate] X after : 5c837cec076f2d34012559318f9230b5c323e6cd37345465baff8f27909713fe  inode=11224643 size=625
--- [candidate] sidecars: X
```

exit **2** (USAGE, the declared class), **every** identity field of X identical
before/after (sha256, size, inode, mtime_ns, ctime_ns), **no sidecar** written.

## 4. Full 10-case matrix (harness `guard-probe.py`, one run per tool variant)

`REFUSED` = exit 2 and no field of the attacked file moved. `CLOBBERED` = fields moved.

| case | aim | before `112d01dc…` | candidate `2ec0788f…` | landed `7b848eaf…` | landed `d164d49f…` |
|---|---|---|---|---|---|
| A `--paths X --out X` | absolute | **CLOBBERED** exit 0 | **REFUSED** exit 2 | **CLOBBERED** exit 0 | **CLOBBERED** exit 0 |
| A2 same, relative spellings | `X` / `./X` | **CLOBBERED** | **REFUSED** | **CLOBBERED** | **CLOBBERED** |
| B `--paths X Y --out Y` | out is 1 of N measured | **CLOBBERED** (Y) | **REFUSED** | **CLOBBERED** (Y) | **CLOBBERED** (Y) |
| C `--paths X --out R` (control) | distinct receipt target | INTACT (R written) | INTACT (R written) | INTACT | INTACT |
| D `--out` canonical-set path (decoy) | canonical branch | REFUSED exit 2 | REFUSED exit 2 | REFUSED | REFUSED |
| D2 `--paths X --out X.receipt` (prefix share) | over-refusal check | — | WRITTEN, X INTACT | — | — |
| E measured path absent, `--out` = it | create vs clobber | CREATED exit 13 | **REFUSED** exit 2 | CREATED exit 13 | CREATED exit 13 |
| F hardlink alias of X as `--out` | D7 class | **CLOBBERED** | **CLOBBERED** | **CLOBBERED** | **CLOBBERED** |
| G symlink alias of X as `--out` | resolve coverage | **CLOBBERED** | **REFUSED** | **CLOBBERED** | **CLOBBERED** |
| H `--paths R.sha256 --out R` | sidecar aliasing | **CLOBBERED** | **CLOBBERED** | **CLOBBERED** | **CLOBBERED** |
| I `--out` = symlink to canonical path (decoy) | indirect canonical aim | REFUSED | REFUSED | REFUSED | REFUSED |

Selftest at both `112d01dc…` and the candidate: **CLEAN 15/15, exit 0**
(`selftest-before.txt`, `selftest-after-candidate.txt`) — the guard change
regresses no existing case. Note the harness correction: a *renamed* copy of the
tool fails case 7 (`label-utc-render-tz-independent`), because
`custody-pair.py:733` resolves a sibling literally named `custody-pair.py`; both
selftests above were therefore run from directories where the copy keeps that
name. The initial failure was a harness artifact, not a tool defect.

## 5. Round-3 landed revisions — the after-state as it actually landed

Every revision seen was snapshotted, decoy-twinned and probed
(`/var/tmp/ex25/revision-probe-log.txt`, `probe-rev-<sha>.{txt,json}`);
the write-guard was landed mid-window by EX-21 while the wave ran:

| revision | seen (UTC) | write-guard code | case A measured |
|---|---|---|---|
| `112d01dc…` | round-2 landing | canonical-only (`:564`) | CLOBBERED exit 0 |
| `7b848eaf…` | 13:08:08Z | canonical-only (`:604`) | CLOBBERED exit 0 |
| `d164d49f…` | 13:08:57Z | canonical-only (`:604`) | CLOBBERED exit 0 |
| `460a01f0…` | 13:09:16Z | canonical-only | CLOBBERED exit 0 |
| `9860149d…` | 13:09:40Z | canonical-only (`:629`) | CLOBBERED (by code read; same state) |
| `d9be407d…` | 13:10:01Z | **union guard landed** | **REFUSED exit 2, X intact** (watcher) |
| `08fb6833…` | 13:10:40Z | union guard + inode arm (`guarded = CUSTODY + paths`, `_same_file`, `:648–652`) | **REFUSED exit 2, X intact** (full 10-case probe) |
| `57dffff1…` | 13:11:1xZ | union guard + inode arm | (superseded before probe; churn) |
| `03bd6242…` | 13:11:35Z | union guard + inode arm; selftest 21/21 | **REFUSED exit 2, X intact**; F REFUSED; C INTACT; H still CLOBBERED |

**Landed after-state, first-hand at `08fb6833c87d10a07e90ea84186993e95a6b81b853e9ae74045b2b3c2a3618e2`**
(raw shell, 13:10:40Z — same shape as the before-state transcript above):

```
X before: 71b706ac2eab2cb14506ec9a8d86ba5a0fc574e7c44c8d93156502a4a655eedd inode=11243047 size=600
USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode): /var/tmp/ex25/raw/08fb6833/X
exit=2
X after : 71b706ac2eab2cb14506ec9a8d86ba5a0fc574e7c44c8d93156502a4a655eedd inode=11243047 size=600
dir: X          # no X.sha256 sidecar
```

Case A verdict flips **CLOBBERED exit 0 → REFUSED exit 2 with every identity field
of X unchanged**, which is the seat claim's after-state. At the same revision the
full matrix reads REFUSED for A, A2, B, D, E, G, I **and F (the hardlink class,
now caught by the landed inode arm)**; control C still writes and leaves X intact;
only H (sidecar aliasing) still clobbers (§6). Selftest: 15/15 CLEAN at
`08fb6833…`; **21 cases / 21 passed / exit 0** at `03bd6242…`
(`selftest-landed-03bd6242-21cases.txt`) — the C2 claim's "15 → ≥17" growth is
visible in the landed tool by that revision.

**Hand-off revision `89bfebec…` (13:13:06Z): guard still holds, but the tool's own
selftest is DIRTY.** The seat-line attack remains REFUSED exit 2 with X bytes
intact (E and F also REFUSED, control C INTACT, H still CLOBBERED —
`probe-handoff-89bfebec.{txt,json}`), but the same revision's selftest reads
`CUSTODY_PAIR_SELFTEST: DIRTY cases=21 passed=20 failed=1 exit=3`
(`selftest-landed-89bfebec-DIRTY20of21.txt`): case
`require-paths-blocks-partial-reference` fails with
`TypeError: _run_verify() got an unexpected keyword argument 'require_paths'`
(the D3 case was added before the helper's signature in the same wave — mid-edit
state). Both write-guard cases introduced by the hardening,
`refuses-to-write-over-scoped-path` and `refuses-to-write-through-hardlink-alias`,
**PASS**. Flagged for the parent: C2's claim requires selftest at exit 0, and this
revision is not that state; the guard's after-state itself is unaffected.

**Later revision `7cd19c3c…` (13:13:4xZ): the DIRTY state resolved.** Selftest
`CLEAN cases=22 passed=22 failed=0 exit 0`
(`selftest-landed-7cd19c3c-CLEAN22.txt`) and the guard still holds — A, E, F
REFUSED exit 2 with bytes intact, control C INTACT, H still CLOBBERED
(`probe-handoff2-7cd19c3c.{txt,json}`). Revision churn was still in flight at
this writing (10+ distinct revisions between 13:08 and 13:14Z); the parent should
re-probe the commit-time revision with `guard-probe.py` and read the selftest
verdict at that same sha.

**Finding (claim/code divergence).** Revision `d164d49f…` **documents** the fix in
its own docstring — item 5, lines 50–57 at that sha: "`capture` refuses `--out`
when the output would resolve to — or share an inode with — any path being
captured OR any of the five custody paths. `--paths X --out X` no longer clobbers
the scoped file it measures…" — while `cmd_capture` at the same sha still carries
only the canonical check (line 604) and the file contains **no** inode-comparison
code (`grep` for `st_ino`/`samefile` hits only receipt fields and parse patterns;
`inode_guard_text_hits=3` in the watcher log at `460a01f0…` counts docstring/
comment text, not an arm). Rule #14 form: an artifact that claims its own
behavior must re-derive it — at `d164d49f…` the claim is **unbacked by the code**,
and the probe measures the old behavior exactly (exit 0, X destroyed, stray
sidecar). This is the mid-flight state EX-21 owns; it is reported here as a
before/after fact, not as a verdict on the chain's final landing.

**Status of the seat claim: RESOLVED at the probed landed revisions.** Before the
write-guard landed (revisions up to `9860149d…`, 13:07–13:09Z) the clobber is
reproduced exactly as the round-2 VZ-4 A11 finding describes; from `d9be407d…`
(13:10:01Z) the attempt is refused and the bytes are intact. The seat's own
candidate (`2ec0788f…`, a 5-line union guard, selftest-clean) predicted the
required after-state before the landed revision existed, so the measurement
corroborates rather than merely accompanies it. Residual: the wave's *commit-time*
revision must be re-probed at landing — `guard-probe.py` is committed here and
re-runs in ~0.5 s against any revision (snapshot first; the file is being edited
while the wave runs).

## 6. Residual holes outside the declared guard scope (named, not hidden)

- **F — hardlink alias of a measured path (round-2 D7). CLOSED at `08fb6833…`.**
  The landed guard adds an inode arm (`or any(_same_file(out, g) for g in guarded)`)
  and the probe measures REFUSED exit 2 for the `os.link` alias, X untouched.
  My pre-landing candidate used path resolution only and therefore still clobbered
  F — recorded as the difference between the candidate and the landed fix, and as
  evidence that the harness case is load-bearing: it distinguishes the two
  implementations.
- **H — sidecar aliasing (new; not in D1–D7).** `--paths R.sha256 --out R` writes
  the receipt to R and then writes the sidecar `R.sha256`, which is the measured
  path → measured file clobbered, exit 0, with a *receipt* as the damage. The
  declared union guard does not cover it (the sidecar name is derived from `out`,
  never compared to `paths`). Fix shape if wanted: guard
  `{out, out.with_name(out.name + ".sha256")}` against the union set. Named as
  round-4 candidate debt; outside this claim's declared scope.
- **E (boundary).** Under the candidate the missing-path create case is *also*
  refused (exit 2 instead of 13/CREATED). That is stricter than strictly needed —
  a file that does not exist cannot be "clobbered" — but it is what
  `set(paths) ∪ CUSTODY_PATHS` means, and it is fail-closed. Recorded as a
  behavior delta the parent should be aware of when reading the C2 claim.

## 7. Custody read-only control (the instrument stayed safe while probed)

`custody-readonly-control.txt`: with the candidate, a capture of the real 5 paths
exits 0 (5/5) and my own independent sha256+inode+ctime_ns capture around it reads
**moved=none** on all five paths.

Side finding worth the parent's attention: `~/.kimi-code/config.toml` is **not**
at its round-2 pin any more — round-2 recorded `8cbacd48…`, inode `34530637`;
now `bc66d543…`, inode `37793921`, ctime `2026-10-19T12:57:45Z` (09:57:45 local),
i.e. the operator rewrote it **between rounds** (before the round-3 pre-pair
`claims/c2/receipts/config-pre-pair-v2r3.txt`, 13:06:57Z, which already carries
the new bytes, and before EX-25's first write at 10:03 local, so not caused by
this seat). Consequence for C2's claim clause "the round's live pre/post pair
verifies MATCH 5/5": the pre-pair captures the post-drift bytes, so a MATCH is
still achievable — but a *second* operator write during the round would show up
as CONTENT-DRIFT on config.toml, which is an operator-path fact, not a tool
failure; the parent should read any such drift in that light.