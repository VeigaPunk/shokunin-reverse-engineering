# C1 R18-INSTALL-RECORD review

Axes: calibration (counter soundness), freshness (revision/blob binding), depth (mutation sensitivity).

## Finding — P2: `s_install` can false-close an incomplete or misbound record

**Observation.** The routed requirement is to record Go 1.24.6/1.25.0 tool, version, channel, SHA and reason (`corpus/lessons/round-18-verifier-spotcheck.md:199`); the scorecard correction additionally claims date (`SCORECARD.md:2489`). The immutable-main implementation hard-codes two expected hashes (`.ufo/waves/round-19/tools/routed-r18.py:36-37`), extracts the `## Installs` section, then only checks that each version token and its expected hash occur *somewhere* in that section and that `go.dev` occurs somewhere (`:265-276`). It does not require a reason/date/channel field or bind a particular hash to its version. The checker’s green selftest fixture is similarly weak: it starts with `## Installs`, both version strings and `go.dev`, appends both hashes, then expects the install check to pass (`:341-366`).

I independently read the committed main record: it currently has both version/hash pairs, sizes, install paths/times, a reason and an official-release-tarball channel (`corpus/lessons/round-19.md:64-76`); the named corrections are present in both that lesson (`:62`) and `SCORECARD.md:2489`. The go1.25.0 digest also matches the S038 quote (`corpus/lessons/round-19.md:42-43`). Thus **the committed main record itself is not a false close**, and the baseline’s open result is not a false open. However, two isolated mutations in separate scratch clones, each checked out at observed main `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, demonstrate false-close capability:

- At mutant `b3d5179d5c1318ac3df742e1988fcde34f6addb7`, I removed the record’s `- Reason:` line only. The detector still reported `R18-INSTALL-RECORD` `named=true`, `substance=true`, `open_count=0`, strict exit 0. Only `corpus/lessons/round-19.md` changed in that clone.
- At mutant `e06ca5b53f0a23432c577f6f85fd4c4b70429039`, I swapped the two version/hash associations while retaining both versions and both expected hash strings. The detector again reported `named=true`, `substance=true`, `open_count=0`, strict exit 0. Only `corpus/lessons/round-19.md` changed in that clone.

The first mutant violates an explicit routed field; the second is a checksum-to-version misbinding. The `go.dev` substring check also cannot establish the claimed channel field: a wrong channel label would pass if `go.dev` remains elsewhere in the section [INFERENCE from `:269-275`]. These are detector false closes, not evidence that the unmutated main record is wrong.

## Counter runs (tool bytes loaded from immutable main blob)

```sh
set -o pipefail
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show d0690fd44f46d8a7fe9da5f01c6be723d12abd41:.ufo/waves/round-19/tools/routed-r18.py | python3 -I -B - --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# COMMAND_EXIT=1; open_count=7, named_open=7, substance_open=7; INSTALL-RECORD: named=false, substance=false, "round-19 lesson absent"
```

```sh
set -o pipefail
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show d0690fd44f46d8a7fe9da5f01c6be723d12abd41:.ufo/waves/round-19/tools/routed-r18.py | python3 -I -B - --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
# COMMAND_EXIT=0; open_count=0, named_open=0, substance_open=0; INSTALL-RECORD: named=true, substance=true
```

The counter’s `Git.show` reads `git show REV:path` (`routed-r18.py:53-59`); the invocation above supplied the tool itself from the main commit blob, not the mutable working copy. Direct baseline checks were consistent: `git cat-file -e B:corpus/lessons/round-19.md` exited 128 (absent), and `git grep -n -- '- R18-INSTALL-RECORD:' B -- SCORECARD.md corpus/lessons/round-19.md` exited 1; the same `git grep` at main exited 0 with entries in both files.

The two mutant detector commands were the same immutable-main-blob pipeline, with `--root` set respectively to `/tmp/kr19-w2-SubstanceINSTALLRECORD.BeGv1Q/lane --rev b3d5179d5c1318ac3df742e1988fcde34f6addb7` and `/tmp/kr19-w2-SubstanceINSTALLRECORD-hash.cxi4Qv/lane --rev e06ca5b53f0a23432c577f6f85fd4c4b70429039`, both with `--strict`; both returned `COMMAND_EXIT=0` and `open_count=0`. Both scratch clones were created and detached at the observed main tip before mutation. No production files were edited; only this report is written in the lane.

## Residual risk and verification gaps

- The detector checks text presence, not whether an archive was actually installed or whether its bytes match the stated digest. It does not recompute an archive digest from a retained artifact. S038 is scoped to the go1.25.0 archive (`corpus/SOURCES.md:44`); I found no corresponding retained Go 1.24.6 archive source in the cited round-19 source rows, so the Go1.24.6 digest remains a recorded assertion here, not independently established archive provenance.
- `refs/heads/main` was observed at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. The lane working copy’s `routed-r18.py` and `round-19.md` did not hash to those main blobs and showed additional uncommitted differences; runs and mutation probes therefore intentionally use immutable main bytes/revisions. This result does not certify the later mutable working copy.
- `xd://lsp` was unavailable (`No such tool`), so LSP status/references/definition/diagnostics could not be obtained. Literal searches were only used to locate occurrences, not as semantic proof. No builds, broad suite, formatter, installs or updates were run.