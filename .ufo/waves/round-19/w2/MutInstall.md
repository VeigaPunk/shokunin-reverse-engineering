# MutInstall — INSTALL-RECORD checker mutation results

## Findings

### Medium — hash values are not bound to their version entries

**Observation.** In the private `/tmp/kr19-mutinstall-r5f8y8/repo` clone at observed `refs/heads/main` tip `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, I swapped the two full archive hashes on `corpus/lessons/round-19.md:69,72`, leaving the version labels, section and channel text intact. The mutation commit was `c700c200abadca36ae187d49b8797b4ff1ef8669`. `routed-r18.py --strict` returned **0**, with `R18-INSTALL-RECORD named=true, substance=true`, `open_count=0`.

**Inference from implementation.** `.ufo/waves/round-19/tools/routed-r18.py:293` checks only whether each expected version literal and each expected hash literal occurs somewhere in the captured body. It never checks that a hash belongs to its version's record. Thus the claimed install-record substance check accepts crossed version/hash associations.

### Medium — the reported channel field is not validated

**Observation.** In the same private clone at the same base, I changed `corpus/lessons/round-19.md:75` to say `Channel: Arch package repository (pacman), not an official Go release tarball`, while preserving the hashes and the unrelated `go.dev` source mentions at lines 68 and 71. The mutation commit was `ad552fd6d9afc96025a0b30dfe7152979a8901e7`. `routed-r18.py --strict` returned **0**, with `R18-INSTALL-RECORD named=true, substance=true`, `open_count=0`.

**Inference from implementation.** `.ufo/waves/round-19/tools/routed-r18.py:294-295` checks only whether the literal `go.dev` occurs anywhere in the captured section body; it does not parse or bind the `Channel:` field. The passed mutation is therefore a false green for the channel claim.

## Requested heading-scope mutation

**Observation.** In private-clone commit `d76a181d5afca2625bd410aaf91cc947fcf1bec3`, I put both full hashes into the prose `R18-INSTALL-RECORD` mention at `corpus/lessons/round-19.md:62` (outside the section), and removed both hashes from the actual `## Installs` section while leaving its version and `go.dev` text. The strict checker returned **1**: `R18-INSTALL-RECORD named=true, substance=false`, `open_count=1`, with both versions listed as missing in the substance reason. This satisfies the requested reopen condition.

**Inference from implementation.** `.ufo/waves/round-19/tools/routed-r18.py:289-292` anchors extraction to a line-start `## Installs` heading and stops at the next line-start `## ` heading, so matching prose outside the captured section does not count. The scope behavior is correct for this mutation.

## What binds

**Observed source:** `.ufo/waves/round-19/tools/routed-r18.py:285-296`.

**Inference from the predicate:** The section must exist; within its body, each configured version string and corresponding configured SHA-256 string must occur somewhere, and `go.dev` must occur somewhere. This binds section membership, not version-to-hash association or a channel field. The code does not require the `sha256` label to be attached to a value. The green swapped-hash and wrong-channel mutations confirm the first two gaps.

## Commands and verification

All mutations and commits were confined to the private clone; no production files were changed. The clean tip run and three focused strict runs were:

```text
python3 -I -B /tmp/kr19-mutinstall-r5f8y8/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-mutinstall-r5f8y8/repo --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
routed-r18 exit 0; open_count=0; R18-INSTALL-RECORD substance=true

python3 -I -B /tmp/kr19-mutinstall-r5f8y8/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-mutinstall-r5f8y8/repo --rev d76a181d5afca2625bd410aaf91cc947fcf1bec3 --strict
routed-r18 exit 1; open_count=1; R18-INSTALL-RECORD substance=false

python3 -I -B /tmp/kr19-mutinstall-r5f8y8/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-mutinstall-r5f8y8/repo --rev c700c200abadca36ae187d49b8797b4ff1ef8669 --strict
routed-r18 exit 0; open_count=0; R18-INSTALL-RECORD substance=true

python3 -I -B /tmp/kr19-mutinstall-r5f8y8/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-mutinstall-r5f8y8/repo --rev ad552fd6d9afc96025a0b30dfe7152979a8901e7 --strict
routed-r18 exit 0; open_count=0; R18-INSTALL-RECORD substance=true
```

The clone checkout command completed successfully (exit 0) at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main` observed that same tip before testing (exit 0). At supplied baseline B `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`, `git cat-file -e B:.ufo/waves/round-19/tools/routed-r18.py` reported the path absent (git exit 128; the wrapper assertion expecting exit 1 itself exited 1). Accordingly, tests exercised the tool at the observed current main tip, not at B.

**Verification gaps / residual risk.** No broad suite, tool selftest, build, formatter, install or external revalidation of the archive facts was run; only the focused strict command and these three targeted mutations were used. No tool was installed or updated.
