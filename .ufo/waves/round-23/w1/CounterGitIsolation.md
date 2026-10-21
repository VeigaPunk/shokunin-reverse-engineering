# CounterGitIsolation — R22 Git isolation and helper trust

Seat: KaidokuR23.CounterGitIsolation (scout, read-only). No REA call, no target
execution, no device/network access, no Git writes, no sandbox clone, no
subagent. The only writes were temporary directories created by the R22 counter
itself (`tempfile.TemporaryDirectory` under the inherited `TMPDIR`) during
read-only measurement probes. Lane files were not modified.

Question answered: what exact environment-clearing and replacement-refs behavior
must an R23 wrapper preserve when it reuses R22 `measure()`/`bind_cli()`?

## Findings

### F1 — The scrub exists only in `main()`; `measure()` trusts the caller's environment

OBS — source: `.ufo/waves/round-22/tools/count-c1.py:190-193`

```python
for key in tuple(os.environ):
    if key.startswith("GIT_"):
        del os.environ[key]
os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
```

The same block is at `.ufo/waves/round-22/tools/count-c2.py:217-220` and
`.ufo/waves/round-22/verify.py:21-24`. It runs before `argparse` and therefore
only under CLI invocation. `measure()` (`count-c1.py:101-183`) contains no env
handling; every Git call it makes inherits `os.environ` through bare
`subprocess.run` (`count-c1.py:56,102,116`; R20 helper
`.ufo/waves/round-20/tools/verb-coverage.py:65-78,150-152`).

OBS — import does not scrub. Command (env: `GIT_DIR=/sentinel-git-dir`,
`GIT_CONFIG_COUNT=1`; all other `GIT_*` removed):

```text
/usr/bin/python3 -I -B -c '<importlib load of count-c1.py>'
{"module_name":"r22c1","after_import_GIT_DIR":"/sentinel-git-dir",
 "after_import_GIT_NO_REPLACE_OBJECTS":null,
 "after_import_GIT_CONFIG_COUNT":"1",
 "EVIDENCE_PREFIX":".ufo/waves/round-22/evidence/c1/","measure_doc":null}
exit 0
```

OBS — in-process `measure()` honors an inherited `GIT_DIR`:

```text
env GIT_DIR=/nonexistent-git-dir
  measure("<LANE>","aa1450b82f9ede35aada63efe8a34e01c6e02f72")
  -> {"result":"error","type":"ValueError","message":"invalid_revision"}   exit 0 (exception caught)
env clean (no GIT_*)
  same call
  -> {"result":"no_error","count":1,"rev":"aa1450b82f9ede35aada63efe8a34e01c6e02f72"}
```

OBS — CLI scrub works, including against a full hostile set:

```text
/usr/bin/python3 -I -B .ufo/waves/round-22/tools/count-c1.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev aa1450b82f9ede35aada63efe8a34e01c6e02f72
clean env      -> exit 1, finding c1_incomplete, t1_exercised_count 1,
                  t1_exercised ["identify-flutter-build"],
                  rev aa1450b82f9ede35aada63efe8a34e01c6e02f72, stderr ""
GIT_DIR=/nonexistent-git-dir GIT_WORK_TREE=/nonexistent-wt
GIT_INDEX_FILE=/nonexistent-index GIT_OBJECT_DIRECTORY=/nonexistent-obj
               -> identical exit 1, count 1, rev, exercised list, stderr ""
```

INFERENCE: a wrapper that imports `count-c1.py` and calls `measure()` MUST run
the same scrub in its own process before its first Git command and before
import. A wrapper that invokes the counter as a child process is protected by
the child's `main()`, but the wrapper's own commit resolution and `git show`
extraction of the counter are not protected.

### F2 — Order is load-bearing: purge `GIT_*` first, then set `GIT_NO_REPLACE_OBJECTS=1`

OBS — replay of the exact loop with the switch pre-set:

```text
before_has_no_replace "1"  -> after_loop_has_no_replace null, after_loop_GIT_DIR null
```

`GIT_NO_REPLACE_OBJECTS` itself starts with `GIT_`, so setting it before the
purge silently deletes the protection. The frozen order (`count-c1.py:190-193`)
is the only correct order for this implementation.

### F3 — Replacement refs: the env switch is the only mechanism; no Git argv flag

OBS — no `--no-replace-objects` appears in `count-c1.py`, `count-c2.py`, or
`verify.py`; all Git calls inherit the environment. Control is exclusively
`GIT_NO_REPLACE_OBJECTS=1` set in-process.

OBS — retained R22 proof (`.ufo/waves/round-22/w2/C2Path.md:7-13`, data in
`w2/C2Path.json`): with `git replace c6beadb5... 3f668f6b...`, the same
`--root/--rev c6beadb5...` returned exit 0, `dispositions_complete`,
`accounted_count:14` while still reporting `rev:"c6beadb5..."`; the same command
with `GIT_NO_REPLACE_OBJECTS=1` returned exit 1, count 0. JSON run ids:
`replace_ref_original_revision` (exit 0, 14) and `replace_ref_disabled_control`
(exit 1, 0).

OBS — frozen final controls (`verify/final/controls-c1.json`, named
`controls-c1`, `source_rev: e9db7e2d5798ff3d5f1ba5ccd76bb86f2cc5c1bb`,
`script_sha256: c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`,
exit 0, pass true). Case rows embedded in its stdout:

| case | pass | exit | count | child env override |
|---|---|---|---|---|
| `git_dir_control` | true | 0 | 6 | `GIT_DIR=<fixture>/foreign/.git` |
| `replace_ref_control` | true | 0 | 6 | `GIT_NO_REPLACE_OBJECTS` removed (null) |

The replace control deliberately drops the switch from the child environment,
so the counter must set it itself. Both expected results are 6/6 exit 0.

INFERENCE: digest pins protect only helper/counter bytes (F6). Knowledge,
`corpus/SOURCES.md`, and evidence blobs are not digest-pinned, so a replace ref
or foreign `GIT_DIR` can change the measured content while the reported `rev`
stays truthful. Isolation is therefore part of the count's meaning, not helper
hygiene.

### F4 — `GIT_DIR` beats `-C <root>`; the scrub is the only defense

OBS — `measure` uses `git -C <root>` (`count-c1.py:56,102,116`) and R20 `git()`
uses `cwd=root` (`round-20/tools/verb-coverage.py:65-78`), never `--git-dir`.

OBS — retained R22 proof (`w2/C2Path.md:15-19`, `w2/C2Path.json` run ids
`foreign_revision_without_override` and `foreign_revision_with_GIT_DIR`): a
commit that exists only in a foreign repository, invoked with
`--root good --rev <foreign-commit>`, returns exit 2 `unevaluable`
`invalid_revision` without an override; with `GIT_DIR=<foreign>/.git` it returns
exit 0, `dispositions_complete`, 14/14 and reports the foreign revision.

OBS — my hostile CLI probe (F1) shows the scrub defeats this for the CLI path.

INFERENCE — the generic purge (`key.startswith("GIT_")`) removes every
repository/config/trace variable, including `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`,
`GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_CONFIG_COUNT/KEY_*/VALUE_*`,
`GIT_CEILING_DIRECTORIES`, `GIT_PREFIX`, and `GIT_TRACE*`. Consequence: an
env-injected Git config (for example `core.hooksPath` via `GIT_CONFIG_COUNT`,
used by the R22 MutateC1 harness) does not reach the counter's own Git
subprocesses; a wrapper must not rely on that channel.

### F5 — Resolve once and use the resolved SHA everywhere

OBS — `count-c1.py:101-107`:

```text
git -C root rev-parse --verify --end-of-options "<rev>^{commit}"
-> rev = resolved stdout
-> revision_helpers(root, rev)      # helper blobs read at resolved SHA
-> r21._measure(r20, root, rev)     # data read at the same SHA
-> read_blob(result["rev"] + ":" + path)
```

The raw `--rev` argument is not reused after resolution. This is the corrected
form: `w2/C1Source.json:29` (F6) and `w2/CriticCausal.md:173` recorded the
earlier double resolution of a symbolic revision and prescribed exactly this
fix. A wrapper must resolve one commit and pass that SHA to both `measure()`
calls (round-22 prefix and round-23 prefix); passing a symbolic ref twice allows
the two calls to read different commits if the ref moves.

OBS — stale line reference in the R22 record: `w2/CriticCausal.md:156` cites the
scrub at `count-c1.py:166-170`, but the frozen bytes (sha `c925918...`, equal to
`verify/final/summary.json` `counter_source_sha256`) have it at `190-193`. The
behavior is the same; anchor by file digest, not line number.

### F6 — Helper trust: digest-pinned extraction from the measured commit, refused before import

OBS — `.ufo/waves/round-22/frozen/helper-hashes.json`
(sha256 `2f83156bd5f769e55eea6b4946496763df8b8cdd14809e93ce4242c4d047c23f`):

```text
revision: 7787fea4d6fd718726de92ed20759d11ce7b8b48
R20 .ufo/waves/round-20/tools/verb-coverage.py
    cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f
R21 .ufo/waves/round-21/tools/verb-coverage.py
    615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b
scope: "Only these reviewed helper bytes may execute in R22-C1 measurement;
        modified measured-revision helpers are refused before import."
```

OBS — enforcement in `.ufo/waves/round-22/tools/count-c1.py`:
`HELPER_SHA256` at `:36-39`; `revision_helpers` at `:50-66` does
`git -C root show "<resolved-sha>:<rel>"` into a
`tempfile.TemporaryDirectory(prefix="kaidoku-r22-helpers-")`; `show` failure
raises `helper_revision_unreadable: <rel>` (`:59`), digest mismatch raises
`helper_source_untrusted: <rel>` (`:61`) before any write/import (`:62-64`);
R21 is imported from that temp directory (`:65`) and R20 is loaded from it via
`r21.legacy_helpers(directory)` (`:66`). No helper code is read from the
worktree.

OBS — pins hold at both relevant commits (`git show <rev>:<path> | sha256sum`):

```text
aa1450b8 (round-23 baseline)
  R20 cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f
  R21 615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b
e9db7e2d (R22 final source_rev)
  R20 cfbf1880... (same)   R21 61536938... (same)
```

OBS — final controls at `source_rev e9db7e2d...`, script sha `c925918...`,
exit 0: `helper_drift` pass (exit 0, count 6) and `committed_helper_change`
pass (exit 2, count null). The first mutates only the worktree helper, which is
never loaded; the second commits an altered helper at the measured revision and
is refused as unevaluable before import.

OBS — the selftest manifest chain is separate:
`SELFTEST_MANIFEST_SHA256 = 1abdd9df...` (`count-c1.py:40`) pins
`frozen/expected-v2.json`, whose `inputs` pin `counter-fixtures.py`, both
helpers, and `round-20/verify/round20/verb-coverage.json` — it does not pin
`count-c1.py` itself. R22's `verify/final/summary.json` separately records
`counter_source_sha256[".ufo/waves/round-22/tools/count-c1.py"] =
c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`, which equals
the worktree file at HEAD `a3c92eb6bc70984e90ae5b895412de978840b2c5` and the
committed blob at `e9db7e2d...` (verified with `git show | sha256sum`). The
last commit touching the file is `e9db7e2d5798ff3d5f1ba5ccd76bb86f2cc5c1bb`
("round-22: freeze reviewed CLI boundaries and complete wave evidence").

INFERENCE (directly directed by the BuildCounter task text): the R23 wrapper
must load `count-c1.py` from one Git-resolved commit, verify sha256
`c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` before
import, and never import the mutable worktree copy. That keeps the same trust
shape as `revision_helpers`.

### F7 — Reuse knobs and semantics a wrapper must preserve when calling `measure()` twice

OBS — `EVIDENCE_PREFIX` is a module global (`count-c1.py:33`) read inside
`measure()` at `:109-110` and `:154`. `measure()` rebuilds
`r20.EVIDENCE_PREFIX` and `r20.CITED` on every call, so assigning
`module.EVIDENCE_PREFIX` before each invocation is sufficient to switch
`.ufo/waves/round-22/evidence/c1/` → `.ufo/waves/round-23/evidence/c1/`.
Nothing else about the binding policy should be reimplemented.

OBS — exit contract (`count-c1.py:228-233`): `0` iff
`t1_exercised_count == t1_total`; `1` otherwise; `ValueError`, `OSError`,
`UnicodeError`, `RecursionError` → `{"finding":"unevaluable","error":...}` and
exit `2`. The BuildCounter task restates this for R23.

OBS — the reused `measure()` hard-codes the R22 source gate at
`count-c1.py:129`: `int(S###) >= 51`, tier A/B, `status == mined`,
`date == 2026-10-21`, with used-by parsed from `cells[11]` (`:130,:141`). This
is necessary but not sufficient for R23: BuildCounter requires any newly
counted witness to come from a round-23 entry citing a mined A/B `S058+` row
opened `2026-10-21` with exact used-by. The wrapper must add that S058+ gate for
new witnesses; editing the R22 file is forbidden by the task.

OBS — measured-commit prerequisite for R23: at HEAD `a3c92eb`,
`.ufo/waves/round-23/claims.json` is tracked, but the directory is mostly
uncommitted — `git status --porcelain -- .ufo/waves/round-23` observed 17
untracked entries (`evidence/`, `tools/`, `w1/`, `wave1-*.json`,
`gen-wave1.py`, and others; the set is live because peer seats are writing). At
the R23 baseline `aa1450b8...` `claims.json` is absent (`git cat-file -e`
fails; `git show ... | sha256sum` produced the empty-input digest). `measure()`
reads only the resolved Git commit, so new knowledge/evidence must be committed
at the measured revision or the wrapper will keep reporting the historical 1/6.

### Host state observed (2026-10-21)

```text
git version 2.56.0
/usr/bin/python3 3.14.8
git for-each-ref refs/replace | wc -l -> 0
env GIT_* -> GIT_EDITOR=true, GIT_PAGER=cat, GIT_TERMINAL_PROMPT=0
```

No repository-selecting `GIT_*` and no replace refs exist on this host now, so
the hazard is latent, not active. The frozen controls and the C2Path probes show
what happens when it is active.

## Unknowns / not tested

- No replace ref or foreign repository was created by this seat (read-only; Git
  writes are restricted to private clones under the lane contract). F3/F4 rest
  on retained R22 probes, not a fresh reproduction.
- Behavior of env-based Git config injection into `measure()` is inferred from
  the generic `GIT_*` purge; I did not run it.
- The R23 wrapper (`round-23/tools/count-c1.py`) does not exist yet, so no
  wrapper code was inspected; F7 is a contract for its author, not a review of
  it.
- I did not inspect `git config` sources (`~/.gitconfig`, system config) for
  `core.useReplaceRefs` or `url.*.insteadOf`; the R22 mechanism controls only
  env and replace refs, not every Git configuration path.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CounterGitIsolation.md`
  — sole output. Its whole-file sha256 is reported in the final hand-off
  message: embedding the digest in this file would change it. Every other path
  in this report is pre-existing read-only source or retained R22 evidence.

Reference digests used above:
`claims.json` `249811d9d103960811025d5305422e97271877bec1f470c1601cadc1f40d1906`;
`w2/C2Path.md` `321542f1f279220469adb53ff856d5e9a3c6f30c652f8a85c6f826065cd8377b`;
`w2/C1Revision.md` `cbbb8d3be0b9537b418332520094f344d041c31de21acc8e18015dec3d318a82`.

## Installs

None. No pacman, uv, npx, npm, or cargo transaction; no global or config change.
`npx rea-agents@6.5.0` was not invoked because this seat's question is entirely
in source and retained Git objects.

## Open risks

1. **Scrub gap at import.** A wrapper that imports `count-c1.py` and calls
   `measure()` without executing the F1 scrub is reroutable by `GIT_DIR` and
   replace refs; only `main()` scrubs.
2. **Switch ordering.** Setting `GIT_NO_REPLACE_OBJECTS=1` before the `GIT_*`
   purge deletes the switch; the purge must run first.
3. **Two-commit hazard.** Passing a symbolic `--rev` to two `measure()` calls
   can pair data from different commits; resolve once and pass the SHA.
4. **Source gate mismatch.** Reusing the R22 `>=51` gate as the only source gate
   can admit a new witness from an older row or miss an `S058+` row whose date
   differs; BuildCounter's S058+/2026-10-21 gate must be added by the wrapper.
5. **Uncommitted R23 inputs.** `measure()` reads Git blobs only; untracked R23
   knowledge/evidence at the measured revision yields the historical 1/6. This
   is an L1 integration prerequisite, not a counter defect.
6. **Line-number drift.** R22 reports cite `count-c1.py:166-170` for the scrub;
   frozen bytes put it at `190-193`. Anchor on sha `c925918...`, not lines.
7. **Unpinned measured data.** Helper/counter pins do not authenticate
   knowledge, SOURCES, or evidence blobs; with isolation lost, counts can be
   steered without breaking the pins.
