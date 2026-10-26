# R36ExecHarnessRun — `tools/round-36/c1-run.sh` on K2, all three modes

Seat: leaf executor, R36 wave 1. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
lane HEAD at time of work `d2e46ef5` (2026-10-26). No lane file, frozen predicate, counter,
carrier or oracle was written or changed; the only write outside my scratch is this report.

## 0. Preconditions actually observed

| Fact | Evidence |
|---|---|
| I ran the **frozen** harness | `sha256sum tools/round-36/c1-run.sh` = `16907dca7fc7a104acb78d97694924a52e4a87f517348ce7a10eec1c270bf4d4`; identical blob at freeze `790561d4`, at C1-after `3310d8fa` and at `HEAD` (`git show <rev>:tools/round-36/c1-run.sh \| sha256sum`); absent at base `cab59f22` (empty `git show` = `e3b0c442…b855`, i.e. the harness landed with the freeze) |
| Working tree clean for the measured paths | `git status --porcelain tools/round-36 corpus/evidence/round-36 PROVINCE.md corpus/README.md` → empty |
| K2 fixture is the frozen carrier | `sha256sum corpus/evidence/round-36/c1/fixtures/k2-le-gzip.sqsh` = `ce5bf60e765e9942c1d317cfdd201b8b072b61e546e8dbdb6f87d6fe36a2084f` = `carriers.json` K2 `sha256` |
| Committed K2 receipts are the tip's receipts | blob sha of `K2/{before,after}.json`, `{before,after}-run.json`, `oracle.tsv` at `3310d8fa` equals the worktree file sha (e.g. `oracle.tsv` `302ffe9f…` both) |
| Tools present, none installed | `sasquatch` 4.5.1 `/home/vgpnk/.local/bin/sasquatch` sha `ad02d27a…c774754`; `unblob` sha `0ce7b624…a1d09`; `/usr/bin/unsquashfs` 4.7.5 (2026/03/01); `strace` 6.x; `jq`. No pacman/uv/npm install, no host service touched (`inotifywait` is **not** installed, so strace was used) |

Scratch: `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecHarnessRun` with `TMPDIR=$S`,
`HYAKU_SCRATCH=$S`; all OUTDIRs at `$S/out-*` (siblings of the harness's own scratch, not inside it).
`S` removed at the end — verified absent (`test -e "$S"` → absent).

## 1. The three modes, exit codes, receipts

```
cd <lane>; HYAKU_SCRATCH=$S TMPDIR=$S bash tools/round-36/c1-run.sh <mode> \
  corpus/evidence/round-36/c1/fixtures/k2-le-gzip.sqsh $S/out-<mode>
```

| mode | exit | stated by run json | content produced |
|---|---|---|---|
| `oracle` | 0 | `squashfs_offset: 0`, `unsquashfs version 4.7.5 (2026/03/01)`, `regular_files: 4` | `oracle.tsv` (4 rows) |
| `before` | 0 | `exit: 0`, `sasquatch: ""`, `sasquatch_sha256: ""`, `stderr_head: ""` | envelope, **0** published files, one `missing-extractor-dependency` gap `dependencies:["sasquatch"]` |
| `after`  | 0 | `exit: 0`, `sasquatch: /home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256: ad02d27a…c774754`, `sasquatch_version: unsquashfs version 4.5.1 (2022/03/17)` | envelope, **4** published files, no sasquatch gap |

Published after-mode files (relative path / sha256 / size), order as published:

```
firmware.bin_extract/usr/lib/kaidoku/blocks.bin     76eaa72beec080e682b667795701938dbaeb4ee32777114f9471c502b9a72e87  200000
firmware.bin_extract/usr/lib/kaidoku/text.txt       2defc0b25de7e2c560c87ca2461b0e317dd5b889150323b2e718ba8c1c1ebb94   73890
firmware.bin_extract/usr/share/doc/NOTICE           70488b47ee9c7ab20d96e35558afd583adc3b5a3fd68574d83ed145e50342cc9      75
firmware.bin_extract/var/small.dat                  87d3d14a123c5a64139b050fe9c33188e1f484d6367d71a30c12fa21fdc9001f       6
```

The gap is unblob's own, not REA's assumption (before envelope):

```
normalized_result.extraction_gaps[0] = {"kind":"missing-extractor-dependency","handler":"squashfs_v4_le",
  "dependencies":["sasquatch"],"continuation_id":"4ca863d0…97a07a"}
normalized_result.diagnostics[0]     = {"stage":"squashfs_v4_le","missing_dependencies":["sasquatch"],
  "report":{"severity":"ERROR","__typename__":"ExtractorDependencyNotFoundReport"}}
raw_result.execution.stdout          contains "Severity.ERROR │ ExtractorDependencyNotFoundReport"
```

After mode: `coverage:"partial"`, chunk `extraction_failed:false`, single gap `unpublished-entry`
`firmware.bin_extract/var/notice-link` (`continuation_id 602c674b…f08cfca`) — the fixture's symlink.
`raw_result.execution.stdout` headline: `Extracted files: 5 / directories: 7 / links: 1`.

## 2. Receipts vs the committed K2 ones (paths/shas)

Byte-identity is impossible by construction, because the envelope embeds absolute paths; the
content is identical. Verified:

- `oracle.tsv`: `cmp` against committed → **identical**, both `302ffe9fe43b82839abbf1977541cd59330c8451d02983d17ddd568f53194926`.
- `{oracle,before,after}-run.json`: `diff <(jq -S 'del(.carrier,.utc)')` → **no differences**; only the carrier path (my fixture vs L1's scratch copy) and the `utc` stamp differ. After-mode `sasquatch_sha256`/`sasquatch_version` therefore reproduce the committed values exactly.
- `before.json` / `after.json`, full envelope with `del(.evidence_id)`, absolute-path fields
  (`.subject.local_path`, `.parameters.path`, `.parameters.output_directory`,
  `.normalized_result.output_directory`, `files[].path`), REA temp-tree paths and every
  `provider_id`/`provider_blob_id`/`blob_id` stripped: **no remaining difference**. Every
  leftover diff line was one of those run-specific fields (before: `244895:1` vs `580141:1` +
  `rea-firmware-QX9wti` vs `rea-firmware-upMlx2`; after: `348734:1` vs `647169:1` + temp paths).
- Predicate-relevant projections are equal: `files[]` (relative_path, sha256, size) identical
  **in order** for both modes (unsorted `diff` empty); before = 0 rows both, after = 4 rows both;
  `extraction_gaps` identical modulo `provider_id`; `chunks[].range/handler/extraction_failed`
  identical; `coverage` `partial`/`partial`; `subject.digest.sha256` equal; `provider` equal
  (`unblob` 26.6.4); `locations`/`evidence_links` counts equal (1/0).

Recomputing the C1 counter's own projection functions on **my** receipts (functions copied
verbatim from `tools/round-36/c1-counter.py:119-138`, applied to my files, not to git):

```
oracle rows: 4
before: files=0 oracle_hits=0 sasquatch_gap=True  subject_sha_ok=True op=extract_firmware/unblob
after : files=4 oracle_hits=4 sasquatch_gap=False subject_sha_ok=True op=extract_firmware/unblob
```

i.e. the harness output satisfies P36-C1's K2 branch (`before_sasquatch_gap is True`,
`before_oracle_hits == 0`, `after_sasquatch_gap is False`, `after_oracle_hits == oracle_files`,
subject/operation checks true).

Evidence ids recompute (`node tools/round-27/xpin-attribute.mjs --pkg65 …/ad9a3fdbcad992c6/node_modules/rea-agents --pkg67 <same> wrapped.json`):

```
my before.json : stored ev_14242ad722a971cbbeff51ece46ebedf974eea30676358ac1c671d714bcc678d = recomputed (6.5.0 and 6.7.0)  verdict both
my after.json  : stored ev_ea10c650844790412bd0bab1bb68432cc5461132d394149095593b11afe93f1d = recomputed (6.5.0 and 6.7.0)  verdict both
committed K2   : ev_7506d2a8…5767b3c (before), ev_c939cd88…b0c88f (after) — both also stored==recomputed
```

My ids differ from the committed ones because the 6.5.0 semantic projection hashes run-specific
absolute scratch paths and pid-derived blob ids. That is expected of the rule, is not a harness
defect, and the counter's predicate only requires stored==recomputed per envelope.

## 3. "Never writes under /tmp"

Method: `strace -f -qq -s 4096 -e trace=openat,mkdir,mkdirat,creat,rename,renameat,renameat2,link,linkat,symlink,symlinkat -e status=successful -o <log> bash tools/round-36/c1-run.sh …`
(the before/after runs add `execve,execveat,openat2,mknodat`), plus a `/tmp` listing count.

| traced run | trace lines | `/tmp` `O_CREAT`/`mkdir`/`rename` dest | `/tmp` entries before → after |
|---|---|---|---|
| oracle | 207 | none (0 lines containing `/tmp`) | 28 → 28 |
| before | 29 888 | none | 28 → 28 |
| after | 30 344 | none | 28 → 28 |
| before + execve/openat2/mknodat | not counted (superset of the before syscall set) | none | 28 → 28 |
| forced REA failure (exit 3) | 3 202 | none | 28 → 28 |

The only `/tmp` **strings** in any trace are `…/node_modules/npm/node_modules/cacache/lib/util/tmp.js`,
`…/tuf-js/dist/utils/tmpfile.js`, `…/solc/node_modules/tmp/package.json` etc. (module paths) and
`/home/vgpnk/.npm/_cacache/tmp/<uuid>` (npm cache staging, absolute, not `/tmp`).

All successful creates land in exactly two roots: my scratch (541-549 `O_CREAT` per run, incl.
`<scratch>/node-compile-cache/`, `<scratch>/rea-firmware-*/`, `<scratch>/root/…`, `<scratch>/out/`)
and OUTDIR (`before.json`, `before-run.json`, `oracle.tsv`, `oracle-run.json`), plus `/dev/null`.
REA's own staging honoured the exported `TMPDIR` (`rea-firmware-*` inside the harness scratch),
and the oracle's `unsquashfs` root is `<scratch>/root`.

Out-of-scope writes, all from `npx` (npm itself, not the harness's code path), none under `/tmp`:
`~/.npm/_logs/<utc>-debug-0.log`, `~/.npm/_cacache/tmp/<uuid>` → `rename` into
`~/.npm/_cacache/index-v5/dd/d3/959…`, and `mkdir ~/.npm/_npx/ad9a3fdbcad992c6/concurrency.lock`.

## 4. The before-mode PATH filter really hides sasquatch

Filter as written (`c1-run.sh:71`):

```
path=$(python3 -I -c 'import os,sys; print(":".join(d for d in sys.argv[1].split(":") if d and not os.access(os.path.join(d,"sasquatch"), os.X_OK)))' "$PATH")
```

Unit tests of that exact program text:

| input PATH | output | verdict |
|---|---|---|
| `/a:/home/vgpnk/.local/bin:/b` (only `.local/bin` has +x sasquatch) | `/a:/b` | drops the holder |
| `/usr/bin:<T1>:/usr/local/bin:<T2>` (two holders) | `/usr/bin:/usr/local/bin` | drops **all** holders |
| `/usr/bin:<T3>` (`sasquatch` present but not executable) | `/usr/bin:<T3>` | keeps (matches `os.access(X_OK)`) |
| `::/usr/bin::` | `/usr/bin` | empty components dropped |
| `/usr/bin:.` | `/usr/bin:.` | relative component kept |

Real PATH: the one and only directory holding an executable `sasquatch` is
`/home/vgpnk/.local/bin`; the filter drops it and the filtered PATH resolves
`sasquatch` → **NOT-FOUND**. Independent confirmation from the run itself:

- `execve` trace of the before run enumerates every binary started by the harness and its
  children — `bash, realpath, mkdir, mktemp, python3, date, cut, sha256sum, timeout, npx, node,
  rea, unblob(×2), ps(×4), ldconfig(×4), prlimit(×2), sed, grep, rm, jq` — **no sasquatch exec**.
  The string `sasquatch` appears only inside the filter's own `python3 -I -c` argv and inside the
  final `jq` receipt-building argv (`"--arg","sq",""`).
- `before-run.json` records `sasquatch:""`, `sasquatch_sha256:""`, `sasquatch_version:""` and
  `exit:0`.
- unblob itself reported the dependency missing (§1), which is the behavioural proof the extractor
  was not reachable at run time.
- The post-filter guard (`c1-run.sh:72`, `command -v sasquatch` → `exit 2`) would have aborted the
  run had anything survived; it did not fire. Guard semantics checked directly:
  `PATH=/home/vgpnk/.local/bin:/usr/bin command -v sasquatch` → 0/`/home/vgpnk/.local/bin/sasquatch`.

## 5. Scratch removal on exit, incl. forced failures

`trap 'rm -rf -- "$scratch"' EXIT` (`c1-run.sh:26`); `scratch=${4:-$(mktemp -d "$root/c1-run.XXXXXX")}`.

| case | command shape | exit | per-run scratch left | OUTDIR |
|---|---|---|---|---|
| oracle success | `oracle K2 $S/out-oracle` | 0 | none | ts v+run json |
| before success | `before K2 $S/out-before` | 0 | none | envelope+run json |
| after success | `after K2 $S/out-after` | 0 | none | envelope+run json |
| F1 nonexistent carrier | `before $S/nope.sqsh …` | 2 (`usage: …`) | none — scratch never created | not created |
| F1b bad mode token | `bogus K2 …` | 2 | none | not created |
| F2 corrupt carrier with `hsqs` magic | `oracle $S/corrupt.sqsh …` | 3 (`FATAL ERROR: Can't find a valid SQUASHFS superblock`) | none | created, empty |
| F2b plain text carrier | `oracle $S/plain.bin …` | **1** (`unsupported carrier header`) | none | none |
| F3 after mode with sasquatch off PATH | `PATH=/usr/local/bin:/usr/bin … after K2 …` | 2 (`sasquatch not on PATH`) | none | created, empty |
| F4 REA capability failure | `REA_UNBLOB_COMMAND=file://$S/does-not-exist before K2 …` | 3 (`re-run of `rc!=0`` path) | none | `before.json` (502-byte `capability_unavailable` object) + `before-run.json` (`exit:1`) |
| F5 explicit SCRATCH arg | `oracle K2 $S/out-f5 $S/decoy` | 0 | the caller-supplied `decoy/` **is** deleted on exit | receipts written |
| F6 OUTDIR nested in explicit SCRATCH | `oracle K2 $S2/out $S2` | 0 | `$S2` deleted → **receipts gone, exit 0** | destroyed |

After every case, `ls -d $S/kaidoku-r36/c1-run.*` → none.

## 6. Defects and risks (reported, not repaired)

**D-1 (low, real) — silent receipt loss when OUTDIR ⊆ SCRATCH.** `mkdir -p "$outdir"` (`:21`)
happens before the trap is armed against that subtree; `rm -rf "$scratch"` (`:26`) then removes the
receipts while the run exits **0**. Evidence: F6 above — `exit=0`, `$S2` absent, `$S2/out/oracle.tsv`
gone. Any caller that reads the header ("Writes only under OUTDIR and a private scratch dir") and
puts OUTDIR under the same `$HYAKU_SCRATCH/kaidoku-r36` subtree as the mktemp scratch can lose
results silently. Suggested guard: refuse when `realpath(outdir)` is inside `realpath(scratch)`.

**D-2 (low) — exit-code contract mismatch.** Header documents `2 usage/environment error`,
`3 tool failure`. `oracle` on a file whose first four bytes are not `hsqs` and not ELF exits **1**:
`off=$(python3 -I - …)` (`:31-44`) fails with `unsupported carrier header` and `set -e` propagates
python's status 1, so the explicit `exit 3` at `:46` is never reached. Evidence: F2b, `exit=1`.

**D-3 (nit) — residual empty parent.** Only the per-run `c1-run.XXXXXX` is removed; `mkdir -p "$root"`
(`:23`) leaves `$HYAKU_SCRATCH/kaidoku-r36/` behind empty after every run (`ls -A` → 0 entries,
`drwxr-xr-x 2`).

**R-1 (risk) — the 4th argument is `rm -rf`'d unconditionally.** Passing an existing, populated
directory as SCRATCH destroys it (F5). Documented as "private scratch dir" but not enforced (no
ownership/emptiness/mktemp-shape check).

**R-2 (risk) — before mode hides the whole directory, not just sasquatch.** The filter removes the
entire `PATH` component that holds an executable `sasquatch`, so every sibling tool in
`/home/vgpnk/.local/bin` disappears for the REA child (`unblob` → NOT-FOUND, `jq` → falls back to
`/usr/bin/jq`). The run survives only because `REA_UNBLOB_COMMAND` defaults to the **absolute**
`$HOME/.local/bin/unblob` (envelope `normalized_result.engine.executable_path` =
`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha `0ce7b624…`, version 26.6.4). On a host
where unblob is reachable only by name, before mode would end in `capability_unavailable` (REA exit
1 → harness 3) instead of a missing-sasquatch gap — a different, louder failure, not a silent one.

**R-3 (risk, pin fidelity) — the pin is a literal string.** `rea:"rea-agents@6.5.0"` in
`*-run.json` is echoed by `:85`, not probed; both my and the committed envelopes carry
`environment: null`, so no receipt field states which package ran. The host holds two npx cache
roots — `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` = **6.5.0** and
`/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents` = 6.4.0. The executed binary in the
`execve` trace was `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea`, i.e. the 6.5.0
root, so the pin held for these runs. Suggest recording the resolved `.bin/rea` realpath + its
`package.json` version in `<mode>-run.json` so the pin is provable from the receipt alone.

Non-defects I first suspected, then cleared:
- A **relative** `mkdir("out-before", 0777)` appears in the trace although the argument is absolute.
  `execve("/usr/bin/mkdir", ["mkdir","-p","/fast/scratch/…/out-before2"])` shows the harness passes
  the absolute path; the relative syscall comes from coreutils/gnulib `mkdir -p` traversal.
  [INFERENCE] on the gnulib mechanism; the argv and the successful result are observed.
- `Available PATH` executed binaries `/usr/bin/ps` ×4 and `/sbin/ldconfig` ×4 come from unblob's
  dependency probing, not from the harness.

## 7. Limits of this seat's evidence

- K2 only (the assignment's carrier); K1/K3/K4, the AppImage offset computation and `/tmp` on other
  mounts/namespaces are untested here.
- `/tmp` freedom is established for these runs via `strace` on the process tree, not via a
  filesystem quota or namespace isolation; a child that wrote through an already-open fd it never
  opened itself would be invisible (no such fd exists in the traces).
- npx resolved from the local cache (`~/.npm/_npx/ad9a3fdbcad992c6`, ~2 s per run); I did not verify
  any registry tarball, only that the executed package root is the 6.5.0 one.
- `sasquatch` 4.5.1 is the L1-installed official deb binary (`ad02d27a…`), as in the committed
  after receipt; I neither reinstalled nor removed it.
- No VCS mutation: only `git show/log/rev-parse/status/cat-file`-class reads. No file written
  outside `$S` and this report; lane scratch (`/fast/scratch/hyaku/kaidoku-r36/R36ExecHarnessRun`)
  removed before finishing.

## 8. Verdict

All three modes run clean on K2 (exit 0), their receipts reproduce the committed K2 receipts in
every content-bearing field (files/shas/sizes/order, gaps, chunks, coverage, provider, oracle
`oracle.tsv` byte-identical), the before-mode filter demonstrably hides sasquatch (unit tests,
filtered-PATH resolution, `execve` trace, and unblob's own `ExtractorDependencyNotFoundReport`),
nothing is ever written under `/tmp` (four straced runs incl. a failure, `/tmp` entry count flat at
28), and the scratch is removed on success and on all six forced-failure shapes. Six findings are
advisory only (§6); none of them touches a frozen predicate, counter, carrier or oracle.
