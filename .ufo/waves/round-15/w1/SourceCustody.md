# SourceCustody — kaidoku round 15, wave 1 (sentinel, report only)

Seat: `KaidokuR15.SourceCustody`. Axes: **depth** and **calibration**.
- **Harm** means any of: target or provider execution, a config or credential read, an install, a full upstream copy, or a provenance claim stronger than its bytes.
- **Writes:** this report only.
- **Not executed:** inventory, measure, gate, selftest, build, lint, or any Ghidra/REA process.
- **Not opened:** no credential, auth or client-config file. That includes `~/.omp/agent/agent.db*`, `.bashrc` and `.profile`.

Paths: `L` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `G` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`, `R15` = `L/.ufo/waves/round-15`.

## Reviewed byte snapshots (last check 2026-10-20T03:59 -03:00)

| File | sha256 | Status |
|---|---|---|
| `R15/snapshot-inventory.py` | `b72f045d3a1b17912c9c13949a82b5034c03e4331aff7812ae430b52fde44932` | Owner revised it twice during review: `33adf5b3…` then `3c15f4db…` then this one |
| `R15/measure.py` | `226e2f104fbc87139476238a8ab7d17b7749557aa3caaf7f171105d2d3900775` | Also revised during review (earlier `340f5b8f…`) |
| `R15/boundary-fixtures/raw-source.md` | `2e80083b7567beaf119463cee31eb617a02d3ab7887bce8441baf43150118270` | Equals both manifest pins (recomputed) |
| `R15/boundary-fixtures/raw-accepted.json` | `95c995035ebf539e4e3cce3410a8e52461f5f7c88d5b58563381f0cd19cd4537` | Matches `w1/BoundaryFixtures.md:21` |
| `R15/boundary-fixtures/rendered-rejected.json` | `bc97c4699bfcc06d5f6197d63592982f5a9ee245dd787c06ba6ca336746399e3` | — |

If any of these bytes change after this snapshot, the findings below apply to the bytes above, not to the later version.

## Findings (severity order)

### F1 — MEDIUM (calibration/custody): S003's pin does not cover the data files the inventory measures

**Evidence**
- The S003 registry row (`L/corpus/SOURCES.md:9`) pins only `Base-src.zip` (SHA-256 `f00d29c2…8d804`). I recomputed it and it matches. S007 (`c6b25301…65c4`) also matches.
- The C1 inventory reads `G/Ghidra/Features/Base/data/typeinfo/golang/*.json` and `patchverdiffs/*.json.diff`. These are separate installed files: 11 base JSON and 123 diffs by `ls`. No registered row covers them.
- The directory is `vgpnk:vgpnk 755` and was installed by hand under `~/.local/opt`, not by pacman. No package-manager integrity record exists.

**Exploit path / failure mode**
- An entry could write "S003 shows `go1.26.0.json` is absent" (or cite base digests to S003). That would launder an unpinned, user-mutable observation through a pinned row.
- Any agent acting under the RULES install directive could drop an upstream `go1.26.0.json` into this directory. That changes C1's observation while S003's digest still matches.

**Impact:** provenance overstatement in the C1 entry. Grounds shift silently if the data directory is mutated.

**Smallest remediation**
- For data-file facts (presence, sizes, digests, map keys), the entry cites the committed inventory output and its sha256.
- S003 is cited only for control flow.
- Alternatively, L1 opens a row for the installed data directory.

**Status:** sent to `KaidokuR15.SnapshotEntry` and `KaidokuR15.ReviewSources`. ReviewSources replied that it amended its D1 (`w1/ReviewSources.md` §3) to this custody limit and does not stretch S003's used-by.

### F2 — LOW (calibration): the digest was not bound to the parsed bytes — fixed

- **Evidence:** snapshot `33adf5b3…` hashed the file with `sha256_file()` and then reopened it for `json.loads` / `readlines`.
- **Failure mode:** the recorded digest and the parsed structure could describe different bytes if the file changed between the two reads.
- **Fix in `b72f045d…`:** each file is read once, then hashed and parsed from the same buffer:
  - base JSON at `snapshot-inventory.py:111-120`;
  - diffs at `:201-210`, which decode text from the same buffer.

### F3 — LOW (calibration): resolver scope — fallback glob removed; my own first claim corrected

- **Correction.** My first note to SnapshotCensus said `Application.getModuleDataFile` "may search other modules". The installed source shows that is wrong.
  - `G/Ghidra/Framework/Generic/lib/Generic-src.zip`, `ghidra/framework/Application.java:954-962` resolves through `getMyModuleRootDirectory()` into `getDataFileInModule` (`:354-366`).
  - That means one module: the caller's. The caller here is `GoApiSnapshot` in Base, and the lookup string is at `GoApiSnapshot.java:170-171`.
  - So `Features/Base/data/typeinfo/golang` is the resolver scope. I sent the correction.
- **Risk it exposed.** The earlier `fallback_glob` over `Ghidra/Features/*/data/typeinfo/golang` could have selected a directory the loader never reads.
- **Status in `b72f045d…`:**
  - the fallback is gone (no `glob` import; `resource_directory` is at `:356`);
  - `resource_dir_realpath` is reported (`:425-426`).
- **Residual [INFERENCE]:** a release layout has a single Base module root. Dev-tree multi-root module layouts were not examined.

### F4 — LOW (redistribution): bounded copy of upstream-derived bootstrap definitions

**Evidence**
- `bootstrap_types.entries` (`snapshot-inventory.py:184`) copies the full parsed `Types` entry for `runtime.moduledata` and `runtime.pcHeader`.
- Its siblings are `entry_keys` (`:177-180`) and `entry_sha256` (`:181-183`).
- I loaded `go1.25.0.json` once in Python to size this. It has 27 top-level keys. Both types appear only under `all`, with keys `Fields`/`Kind`/`Position`. Their compact `json.dumps` sizes are 2,218 B + 643 B = 2,861 B, including `$GOROOT/...` position strings.
- The rest of the roughly 10 MB file (`Funcs`/`Types` maps) is never emitted (`LIMITS`, `:72-84`).
- The installed `G/LICENSE` is Apache 2.0.
- [INFERENCE] The struct definitions derive from the Go toolchain source. This is not a licensing verdict (`L/PROVINCE.md:114-116`).

**Impact:** about 2.9 KB of structured third-party-derived data. The output will probably be committed to the public remote `VeigaPunk/shokunin-reverse-engineering` (`git remote -v`). This is bounded and far from a full copy.

**Smallest remediation (optional, L1 decision):** if committed output should carry no upstream content, drop `entries` and keep `field_counts`, `entry_keys` and `entry_sha256`. Otherwise keep it, and say in the entry that only these two named entries are reproduced.

### F5 — LOW (calibration): equal size is not equal content in patch diffs

- **Evidence (sha256 prefixes):**
  - `go1.21.12.json.diff` and `go1.21.13.json.diff` are identical (`d8dc5a728dd447be` for both).
  - Same-size pairs that differ: `go1.15.14`/`go1.15.15` (`f6a839e9…` / `d941cd17…`, both 110,373 B) and `go1.20.6`/`go1.20.7` (`8f3a9cb7…` / `5e109e91…`, both 138,685 B).
- **Why it matters:** `GoApiSnapshot.java:118-145` applies one diff onto the `x.y.0` base. Byte-identical diffs therefore make those patch levels indistinguishable to the snapshot.
- **Remediation:** the inventory already emits a per-diff sha256. L1 / the entry should group diffs by digest, never by size, and state the digest-equal groups as a discrimination limit.
- **Also observed (by `ls`, not the tool):** no `go1.25.*` diff and no `go1.26.0.json`. The final numbers belong to L1's inventory run.

### F6 — LOW (disclosure): `task-result.json` carries host privilege text

- **Evidence:**
  - `R15/task-result.json` contains "Passwordless" (`grep -l`).
  - The round-14 sentinel's F6 advised not committing the round-14 equivalent (`L/.ufo/waves/round-14/w1/CustodySafety.md:57-59`). It was committed anyway: `git grep` finds it at `HEAD:.ufo/waves/round-14/task-result.json`.
  - The round-14 closure saw ahead count 0 (`round-14-verifier-spotcheck.md:39`). [INFERENCE] The text is therefore already public, and the new disclosure from round 15 is roughly zero.
  - A token-shape scan of the round-15 `task-result.json`, `dispatch.json` and `spec.json` found 0 hits for `ghp_`, `gho_`, `github_pat_`, `sk-…`, `xai-…`, private-key headers, `auth.json`, `hosts.yml` and `.netrc`. The 2 `agent.db` hits are the contract's prohibition text. Only counts were printed.
- **Remediation:** commit `spec.json`/`dispatch.json`/`swarm-registry.json` as evidence. Leave `task-result.json` out unless the campaign requires it.

### F7 — INFO: synthetic boundary fixtures are custody-clean; manifests are unpinned

- **Content.** The source is 34 hand-authored bytes. Both manifests carry `origin: synthetic` and `upstream: false`. No upstream page was fetched, so there is no redistribution.
- **Provenance fields are self-asserted.** `parse_manifest` (`round-14/tools/quote-fidelity.py:173-209`) reads only `sources` and `quotes`, so the gate ignores the extra top-level `provenance` key.
- **Static expectation (not executed).** By `grade_quote` `:256-257`:
  - `raw-accepted` → exit 0, because `Use <em>raw</em> bytes.` occurs under `## Intro`;
  - `rendered-rejected` → exit 1 with `quote_not_contiguous@rendered-text`.
- **Gap.** No frozen file pins the two manifests. L1 should record their sha256 in the verification record. BoundaryFixtures deliberately did not extend the round-14 `--frozen` inventory (`w1/BoundaryFixtures.md:105-107`), which is correct.

### F8 — INFO: tool design host-safety (static, `b72f045d…` / `226e2f10…`)

**`snapshot-inventory.py`**
- **Stdlib only, no execution or network.** Imports at `:54-60` are argparse, functools, hashlib, json, os, re and sys. There is no subprocess, network or write.
- **Read scope.** Reads are bounded to the fixed `RESOURCE_REL` (`:63`) plus `patchverdiffs/`. There is no recursive walk, so a mistyped `--ghidra` cannot crawl `~`.
- **Symlink handling.**
  - Leaf entries are `lstat`ed (`follow_symlinks=False`) and non-regular entries are skipped.
  - A residual time-of-check/time-of-use gap remains: `open()` by name after the `lstat`. It is LOW in a user-owned directory.
  - Directory components are not symlink-checked; this is disclosed in its LIMITS and offset by `resource_dir_realpath`.
- **Untrusted keys** are emitted through `json.dump` with the default `ensure_ascii`. Control characters and escape sequences become `\uXXXX`, which is terminal-safe.
- **Memory.** Each base JSON (4.27–10.08 MB; about 84 MB across 11 files) is fully parsed one at a time. [INFERENCE] Peak memory is a few hundred MB, which is acceptable.

**`measure.py`**
- Uses only `git rev-parse`, `ls-tree` and `show`, with argv lists (no shell). The revision arg is suffixed `^{commit}` and verified.
- Reads no worktree files.
- `corpus/lessons/round-14.md` exists at baseline `9719dd2` (`git ls-tree`), so the before-measure does not hard-fail on that path.

**Environment cross-check:** the process env `GHIDRA_INSTALL_DIR` equals the default root (`printenv`; no shell file read).

**Installed data integrity at review time:** 0 symlinks/special files in the golang tree, and 0 files newer than 2026-09-22.

## Constraints for L1 (from prior files, not new policy)

- **No full captures.** Commit no installed snapshot JSON/diff or extracted `Base-src.zip` source. Record path, size and sha256 only. Basis: `round-14/w1/CustodySafety.md` F2; `SKILL.md:358-359`, quoted: "Hashing stores digests only, never contents".
- **No installs or "fixes".** Do not install, upgrade or patch Ghidra, and do not add upstream `go1.26.0.json` to "repair" support. This is operator-owned under `PROVINCE.md:108-113`, and it would invalidate C1's observation as well as S003 (prior F4).
- **No target or provider execution.** C1 is a filename/byte inventory and source reading; no Go binary or Ghidra analysis is run.

## Proposed L1 checks (not run here; no pass claimed)

1. **Pin before running.** Run `sha256sum` on `R15/snapshot-inventory.py R15/measure.py R15/boundary-fixtures/*`, then record the values in the round-15 verification/pins file.
2. **Inventory determinism and scope.** Run `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py` twice and `cmp` the two outputs. Then check:
   - exit 0 and `errors == []`;
   - `resource_discovery == "canonical"`;
   - `resource_dir_realpath == G/Ghidra/Features/Base/data/typeinfo/golang`;
   - `skipped_non_regular == []`;
   - the output's sha256 is recorded and cited by the entry (F1).
3. **No-dump bound.** Confirm the output contains no `Funcs` map body: no `"Params"` key outside `bootstrap_types`. Decide on F4.
4. **Digest groups.** From the inventory output, group `patch_diffs.files` by `sha256` and report every group with more than one member (F5).
5. **Limitation controls.** Run `python3 -I L/.ufo/waves/round-14/tools/quote-fidelity.py --manifest R15/boundary-fixtures/raw-accepted.json`, expecting exit 0. Run it on `rendered-rejected.json`, expecting exit 1 with `quote_not_contiguous@rendered-text`. Record both manifest digests (F7).
6. **No host mutation.** After the runs, `find G/Ghidra/Features/Base/data/typeinfo/golang -newermt '2026-10-20 03:54'` should print nothing.
7. **Pre-commit.** Run the token-shape scan or `gitleaks dir` over `R15/`. Exclude `task-result.json` unless required (F6).

## Limits

- **Static review of moving files.** The scripts were edited during review. I do not attest behaviour of later bytes.
- **Non-verdict inspection I did run.** All of it was read-only:
  - `ls`, `find`, `stat`, `sha256sum` and `unzip -p` on Ghidra install and source files;
  - a 300-byte `head` of one diff and one base JSON;
  - one Python `json.loads` of `go1.25.0.json` to size F4;
  - `git` read commands.
- **Not done:**
  - no `gh` or network calls, and no client config, credential or shell rc file opened;
  - GitHub repo visibility was not re-queried. "Public" rests on round-14 `CustodySafety.md:19`;
  - the Ghidra release zip's own digest is unavailable, so the installed data files' upstream provenance is UNKNOWN beyond install mtime (2026-09-21).

## Tool installs

None.
