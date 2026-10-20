# PathSafety: read scope, untrusted JSON, and write scope (round 15, w1)

Seat: `KaidokuR15.PathSafety` (sentinel, leaf). Axes: depth, calibration.
Scope: the planned C1 inventory tool
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py`,
the measure script `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py`,
the C2 fixtures `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/`,
and the worktree write set.

What I did not do: I did not run any lane tool, gate, selftest, or measure script. I did not read any credential, auth, or `agent.db*` file, and I launched no Ghidra or omp process. I ran only read-only inventory probes: `find`, `stat`, `sha256sum`, `git status`/`diff`/`config --get-regexp`/`ls-tree`/`rev-parse`, and stdlib Python reads of installed bytes. Tool installs/updates: none.

The inventory script changed while I reviewed it (tags E9E8 → 9C2A → 0171 → 5DB6 → 500E). Every statement below about the script refers to snapshot **500E**, read at about 04:00 -03:00. L1 should re-check that tag before running it.

## Summary verdict

| # | Severity | Surface | Status at 500E |
|---|---|---|---|
| F1 | medium (fixed) | inventory: uncaught `ValueError`/`RecursionError` meant no JSON output and exit 1 | fixed after my message |
| F2 | low-medium (fixed) | inventory: NaN/Infinity copied into stdout made the output non-strict JSON | fixed |
| F3 | low (fixed) | inventory: hash and parse were two separate opens by name after a no-follow stat (time-of-check/time-of-use gap; digest might not match the parsed bytes) | fixed: one `O_NOFOLLOW` open, one read |
| F4 | medium, calibration (fixed) | inventory: glob fallback read non-Base modules, which Ghidra never loads for snapshots; the limit wording was imprecise | fallback removed; limit reworded |
| F5 | low, calibration (fixed in limits) | inventory: diff structure counts are not JsonPatch validity | named as a limit; `split("\n")` adopted |
| F6 | low (open) | inventory: no per-file byte cap; `bootstrap_types.entries` copied verbatim | open; bounded on this host |
| F7 | low (open) | inventory: directory-path components follow symlinks | open; labelled limit plus `resource_dir_realpath`; 0 symlinks on host |
| F8 | info (open) | inventory: for patch-0 selections, `exact_patch_diff_present` does not apply | open |
| F9 | low (open) | measure.py: no `--end-of-options`; strict UTF-8 decode is uncaught | open; option injection blocked in 4/4 probes |
| F10 | info (was high; adjudicated) | worktree: SHONEN.md box-1 rewrite and footer removal | attributed to L1, deliberate, no restore; see adjudication at the end |
| F11 | info | fixtures: path containment and digest | pass (static) |

## Loader contract the inventory has to mirror (S003 plus installed framework source)

- **Base selection and lookup.** `GoApiSnapshot.getApiSnapshotJsonFile` forces patch 0 for the base (`ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:122-126`). `getApiSnapshotFile` resolves `typeinfo/golang/<subdir>go<ver>.json<suffix>` through `Application.getModuleDataFile(...)`, and `IOException` becomes `null` (`:168-178`). That zip is S003, digest `f00d29c2…a8d804`, fresh `sha256sum` match.
- **Which module.** `Application.getModuleDataFile(String)` resolves only in the **calling class's own module** (Base). Source: `Ghidra/Framework/Generic/lib/Generic-src.zip` `ghidra/framework/Application.java:954-962` → `getDataFileInModule` `:354-367`.
- **Which roots.** `GModule.findModuleFile` takes the first `exists()` hit across `searchRootsByPriority`. Those roots are the module root, `<module>/build`, and shadow modules across app roots (`Ghidra/Framework/Utility/lib/Utility-src.zip` `ghidra/framework/GModule.java:62-69,147-155`). `File.exists()` follows symlinks.
- **Host observation.** `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/build` is absent. The install tree has 0 symlinks (`find -type l` printed nothing). `/opt/ghidra*` and `/usr/share/ghidra*` are absent.
- **Patch diffs.** The loader searches downward only while `patch > 0` and falls back with a warning (`GoApiSnapshot.java:148-166`). A patch-0 request never looks for a diff (`:128-131`).
- **Arch keys.** The loader keeps `[goOS-goArch, goOS, unix|"", goArch, all]` (`:108-109`). All other top-level keys are skipped without parsing (`:214-224`). For a duplicate top-level key, the last one wins (`arches.put`).
- **Diff format is not JSON.** It is jd native format. A first line that does not start with `@ ` throws (`JsonPatch.java:188-190`). Lines shorter than 3 characters are skipped (`:197-199`). The op is decided by the first character only, and `+` values are parsed as JSON (`:201-206`).

## Findings

### F1 — uncaught parse exceptions (medium; fixed at 500E)

- **Exploit path.** Point `--ghidra` at a root whose `go*.json` contains an integer longer than 4300 digits, or deeply nested arrays. Python 3.14.7 raised plain `ValueError` ("Exceeds the limit (4300 digits)") and `RecursionError` (probed in memory; neither is a `JSONDecodeError`). The earlier snapshot caught only `JSONDecodeError`, so it would crash with a traceback, exit 1, and emit no document. That breaks the declared "exit 2 + document with `errors`" contract.
- **Fix observed at 500E.** `except (ValueError, RecursionError)` on the base parse (`snapshot-inventory.py:145-148`) and on the diff header parse (`:246-250`).

### F2 — non-finite constants (low-medium; fixed)

- Python accepts `NaN` by default (probed), and `bootstrap_types.entries` copies values verbatim. A hostile file would therefore produce `NaN` in stdout, which is not strict JSON.
- **Fix observed.** `parse_constant=reject_constant` (`:96-97,145,246`) and `json.dump(..., allow_nan=False)` (`:484`).
- **Host:** 0 NaN/Infinity constants across all 11 installed base files.

### F3 — open/stat race and digest/parse split (low; fixed)

- **Before:** `scandir` checked no-follow, then `sha256_file(path)` and `open(path)` each opened by name again. A swapped-in symlink would be followed, and the digest could describe different bytes from the parsed document.
- **Now:** `read_regular` opens once with `O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_NONBLOCK`, `fstat` requires `S_ISREG`, and size, hash and parse all come from one buffer (`:100-117,137-145`). This mirrors the round-14 gate (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py:107-126`).
- **Host realism:** the directory and files are owned by `vgpnk`, modes 755/644, so tampering would need the same uid. Low.

### F4 — inventory scope must equal the loader's scope (medium calibration; fixed)

- The earlier glob fallback `Ghidra/Features/*/data/typeinfo/golang` would have inventoried a non-Base module directory that `getModuleDataFile` never reads (Application.java:954-962). The output would then have been false "installed snapshot" evidence.
- The earlier limit, "may search other module data directories", was also wrong.
- **At 500E:** canonical Base path only (`:378-387`). The limit now reads "Base module search may also consult build/shadow roots" (`:83`), which matches GModule.java:62-69.
- **Remaining residual:** the script does not itself report whether `<Base>/build/data/typeinfo/golang` exists. I observed it absent on this host; L1 can record that as one `stat`.

### F5 — diff counts are not loader validity (low calibration; limit stated)

- The script counts `"+ "`/`"- "` with a space and never parses `+` values. Ghidra keys on the first character and parses every `+` value.
- **Host census (my stdlib probe, all 123 diffs, read-only):**
  - every first line begins with `@ `
  - 0 op lines without a following space
  - 0 `+` values that fail to parse
  - 1665 lines shorter than 3 characters, which the loader skips
  - 0 `splitlines` hazard characters (U+2028/2029, `\x0b`, `\x0c`, `\x1c`–`\x1e`, `\x85`, `\r`)
- So the gap does not bite on these bytes. The limit at `:85` and the switch to `split("\n")` (`:234`) are correct.

### F6 — unbounded input size (low; open)

- `read_regular` has no byte cap. The largest installed base is 10,081,618 B, and all 11 bases total 84,442,754 B (`du -cb`). With an arbitrary `--ghidra` there is no upper bound on memory.
- `bootstrap_types.entries` copies whole entries. On host, go1.25.0 `all` has `runtime.moduledata` at 2218 B and `runtime.pcHeader` at 643 B serialized. Both appear only under `all`; the go1.25.0 document has 27 top-level keys.
- **Smallest remediation:** a per-file cap of 64 MiB, with an explicit `oversize` error before reading. Alternatively, emit `canonical_digest` plus field names instead of whole entries for non-default roots. `canonical_digest` already exists at `:120-123`.

### F7 — directory components are followed (low; open, labelled)

- `os.path.isdir`/`os.scandir` follow symlinks in `--ghidra` and in every component down to `golang/patchverdiffs`. The script reports `resource_dir_realpath` (`:447`) and states the limit (`:82`).
- **Read scope stays bounded anyway.** Only names matching `^go\d+\.\d+\.\d+\.json(\.diff)?$` are opened (`:67-68,291`). A symlinked directory pointing at, say, a credential directory would leak only the **names** listed in `unrecognized_files`, never their contents. Filenames are capped at 255 bytes on Linux, so `int(\d+)` cannot reach the 4300-digit limit.
- **Remediation, if wanted:** fail with an error when `realpath(resource_dir) != resource_dir`, or when it is not under `realpath(--ghidra)`.

### F8 — patch-0 field semantics (info; open)

- For `--select 1.26.0` the script reports `exact_patch_diff_filename: go1.26.0.json.diff`. The loader never consults a patch-0 diff (`GoApiSnapshot.java:128-131,153`). For patch > 0, `exact_patch_diff_present: false` does not mean "no diff used", because the loader falls back downward (`:151-156`).
- **Smallest fix:** add `"patch_diff_lookup_applies": patch > 0`. Otherwise L1's entry must state this.
- **Host:** go1.26.0.json is absent; go1.25.0.json is present; there are no `go1.25.*` diffs (highest is go1.24.6).

### F9 — measure.py argv/git hygiene (low; open)

- **Command construction.** The code is `git -C ROOT rev-parse --verify "<argv1>^{commit}"` (`measure.py:46-48`), and later calls use only the resolved 40-hex revision. My probes against git 2.55.0 in the lane repo returned exit 128 "Needed a single revision" for all four option-shaped inputs: `--since=yesterday`, `--prefix=x`, `--output=/dev/null`, `--short=7`. `HEAD` resolved to `9719dd23…`.
  - So argument injection into `show`/`ls-tree` was not reachable in those 4 probes. That is not an exhaustive proof.
  - `--end-of-options` works on this git (exit 0 with `HEAD^{commit}`), so the smallest hardening is `rev-parse --verify --end-of-options`.
- **Decoding.** `get()` decodes strict UTF-8 (`:31-34`). A non-UTF-8 blob raises `UnicodeDecodeError`, which is not caught (`:55` catches only `CalledProcessError`/`OSError`), so the script exits 1 instead of the documented 2.
- **Path quoting.** `ls-tree` lacks `-z`. HEAD today has 0 quoted paths out of 14,956 (compared against the `-z` count). Latent only.
- **Execution surface.** There is no `.gitattributes`, and local config has no fsmonitor/pager/textconv/hooksPath keys. The global `filter.lfs.*` settings exist, but no attribute maps them, and `show`/`ls-tree`/`rev-parse` run no hooks. [INFERENCE: `git show <rev>:<path>` does not apply smudge/textconv without explicit flags; not tested.]

### F10 — out-of-seat worktree writes (HIGH for write scope; attribution unknown)

`git status` at 2026-10-20T04:01:24-03:00 shows these modified tracked files:

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SHONEN.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md`

There is also a new `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-15.md`. Totals: 5 files, +43/−6. The first three corpus edits share an mtime of 03:55:10.002–.003. The contract says no seat writes corpus/SHONEN, and L1 integrates.

- **Corpus edits look in-scope for L1 integration.**
  - QUALITY #17 is an append.
  - The r14 entry and the round-14 lesson receive appended, named `Round-15 …` corrections.
  - SOURCES gains S023. Its pinned SHA-256 `54d10162…16252` matches a fresh `sha256sum` of go1.25.0.json.
- **SHONEN.md is different.** Its diff rewrites box-1 text in place and **deletes** the EOF paragraph "Correction to box 1, 2026-10-19 (arc3-loop1-round12; appended at EOF so the pinned box lines keep their numbers; box-1 text above kept)…". It also renames the H1.
  - This is outside C1/C2.
  - It breaks that paragraph's stated append-only and pinned-line discipline.
  - No round-15 seat is assigned SHONEN.
- **Remediation:** L1 confirms who authored the SHONEN diff. If it is not deliberate L1 work with a recorded rationale, restore the deleted correction paragraph and leave box text unchanged. I made no edit.

### F11 — fixtures read and write scope (info; pass, static)

- `raw-accepted.json` and `rendered-rejected.json` reference the relative `raw-source.md`. The gate's `resolve_relative` rejects absolute paths and realpath escapes from the manifest directory (`quote-fidelity.py:152-164`), and `read_regular` requires a regular file (`:107-126`).
- `find` shows three regular files and no symlinks. A fresh `sha256sum` of `raw-source.md` is `2e80083b…118270`, equal to both pins. Bytes (`od -c`): `## Intro\n\nUse <em>raw</em> bytes.\n` (34 B).
- Provenance is marked `origin: synthetic`, `upstream: false`.
- Gate `--manifest` mode prints only. Selftest writes only under `TemporaryDirectory(dir=SELFTEST_ROOT)`, which defaults to `/var/tmp`, overridable via `QUOTE_FIDELITY_SELFTEST_DIR` (`:57-58,566`ff). L1 must not point that variable at the repo.

## Untrusted-content handling (applies to all outputs)

- **What echoes resource content into stdout:** top-level keys, container field names, `unrecognized_files` names, error `detail` strings, and the two copied bootstrap entries.
- `json.dump` keeps the default `ensure_ascii=True`, so control and non-ASCII characters are escaped, with no raw terminal bytes. Even so, L1 and the entry author must treat every name and value as target data, not instructions.
- **Duplicate keys** stay unreported by the script (limit `:79`). My host census with `object_pairs_hook` found **0 duplicate keys at any depth** in all 11 base files. L1 can cite that as a separately measured observation if re-run.
- **BOM:** Python `json.loads(bytes)` accepts a UTF-8 BOM (probed). [INFERENCE: the Java `InputStreamReader` path does not strip it.] The host has 0 files with a BOM.

## Exact write scope (expected)

- `snapshot-inventory.py` and `measure.py` write **stdout only**: no `open(..., "w")`, and `os.open` uses `O_RDONLY` only (`:100-105`).
- Any persisted output comes from L1's shell redirection. Name it explicitly, for example `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.json`, and record its sha256.
- This seat wrote only `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/PathSafety.md`.

## Proposed L1 checks (not executed by me)

1. Confirm tag 500E or later is the final inventory script, then run `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.json`. Expect exit 0, `errors == []`, `skipped_non_regular == []`, and `resource_dir == resource_dir_realpath`. Use `-I` so `PYTHON*` environment variables and the user site directory are ignored, as the gate's own `observe()` does.
2. Cross-check against independent observations: `base_json.count == 11` and `patch_diffs.count == 123`. The selection should show go1.25.0 present with sha256 `54d10162…16252`, go1.26.0 absent, and no 1.25 diffs.
3. Run `stat` on `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/build` (expected absent) and `find /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC -type l` (expected empty). Record both in the entry, since loader-root equivalence depends on them.
4. Run `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py <before-rev>` and again with `<after-rev>`, passing 40-hex revisions. Optionally apply the `--end-of-options` hardening first.
5. Attribute or revert the SHONEN.md diff (F10) before any commit.
6. Before running the C2 controls, verify that the two fixture pins still match `raw-source.md`. Keep `QUOTE_FIDELITY_SELFTEST_DIR` unset.

## Limits

- All script observations are static readings of a file that was still being edited.
- The probes covered Python 3.14.7 and git 2.55.0 behaviour on crafted in-memory inputs and option-shaped argv. That is not an exhaustive fuzz.
- Gson behaviour on duplicate inner map keys, and on BOMs, is [INFERENCE] from library defaults; I did not open Gson source.
- No historical target, provider, or loader run is implied.

## Adjudication of F10 (appended 2026-10-20, after L1 reply)

Author: L1 (`KaidokuR15`), by peer message to this seat. Stated reason: the canonical protocol requires the directory-name title `kaidoku-shokunin` and exactly one evidence line per box, with no footer. The 17/17 footer qualification was moved into the box-1 evidence line instead of being appended. This is a regeneration of SHONEN under that protocol, not an edit to the append-only LOG or corpus.

Checked statically (no restore, no edit to SHONEN):
- Box marks are identical before and after: `HEAD:SHONEN.md` and the worktree both read `[~] [~] [~] [~]`, and 0 diff lines touch a box mark. No promotion.
- The moved substance is present. The new box-1 line cites `SKILL.md:81-314`, 17/17 craft citation blocks at `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`, and `SCORECARD.md` command A.
- The change is recorded in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md:1868-1870` (worktree, uncommitted). It states the title and one-line-per-box restoration, the footer move, and all four boxes remaining author-only `[~]`.

Result: F10 is downgraded to info. The deletion is attributed and in scope for L1 integration. My earlier "breaks append-only discipline" reading assumed SHONEN followed the same append-only rule as LOG and corpus; under the protocol L1 cites, it does not. The one remaining limit: I did not open the canonical protocol text myself, so the claim that it requires no footer is L1's statement, not something I verified.
