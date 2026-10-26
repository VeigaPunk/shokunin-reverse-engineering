# R41C1Revenger — how a REA receipt path is formed, and the exact rule an exact-path matcher must use

**Verdict: DONE — the mapping is not a string suffix.** A published receipt path is
`<depth-0 extract dir>/<relative path inside the extracting tool's output>`, where the
depth-0 extract dir is *always* `firmware.bin_extract` (`selected.bin_extract` under
`--offset/--length`), and every deeper chunk extraction inserts its own
`<start>-<end>.<handler>_extract` directory **inside** the parent root. Because of that,
`rel = path.split('_extract/', 1)[1]` is correct only in the single-whole-file-chunk case.
It is falsified by live receipts on two shapes that the round-41 carriers can legitimately
have (a carve at a nonzero offset, and a second chunk root) — measured below, 0/5 oracle
matches while the derivation-rooted rule scores 5/5. Round-40's `rel_suffix`
(`tools/round-40/c1-counter.py:746-762`) fails the same way, and `same_rel`
(`c1-counter.py:606-607`) still reproduces R40-CL1 on a fresh carrier even after the path
is mapped exactly.

---

## 1. The rule (normative)

For one carrier, let `R` be that carrier's receipt `normalized_result`.

1. **Strip an optional `$output/` prefix, once.** The receipt mixes two namespaces:
   `files[].relative_path`, `unpublished_entries[].relative_path` and gap
   `relative_path` are **bare** (`firmware.bin_extract/...`), while gap `input_path`,
   `derivations[].parent_path/child_path` and `depth_limited_paths[]` are **`$output/`-prefixed**
   (`$output/firmware.bin_extract/...`). Cause: `inventoryFirmwareOutput` emits
   `relative(root, path)` (`rea-agents/dist/firmware/FirmwareFiles.js:177`) and publication
   copies it verbatim (`FirmwarePublication.js:88`), whereas every report-derived path goes
   through `firmwareLogicalPath` (`FirmwareFiles.js:191-200`), which returns `$input` /
   `$output/<rel>`.
2. **Derive the chunk extract root from the receipt, never from text.** The roots are the
   `derivations[]` edges whose `handler` starts with `squashfs_v4`; the child path is the
   extract directory of that chunk (`FirmwareReports.js:341-357`, produced from unblob's
   `subtasks` at `unblob/processing.py:683-688`). For a chunk extracted from the selected
   input the root is the depth-0 directory `firmware.bin_extract`; for a chunk carved out of
   a parent it is `<parent root>/<start>-<end>.<handler.NAME>_extract`.
3. **Map with whole-segment prefix equality.**
   `rel(P) = '' if P == CR else P[len(CR)+1:] if P.startswith(CR + '/') else NOT_IN_NAMESPACE`.
   An entry outside `CR` belongs to another namespace (another chunk root, a carve artifact
   of the parent, a deeper root) and **must not** be compared against this oracle and must
   not be reported as "published outside the oracle".
4. **Key the comparison by `(root, rel)`.** Two roots can carry the same `rel` with different
   bytes (measured: `sbin/tool` 5000 vs 3000 bytes in one receipt). Flattening roots into one
   `rel → row` dict silently loses one of them.
5. **Compare regular files by `rel ==` + `sha256` + `size`; compare non-regular entries from
   `unpublished_entries` only** (`files` never holds links: `FirmwareFiles.js:166-172`,
   `FirmwarePublication.js:88`). Compare the link *path* only — never the target (see §2.2.4).
6. **Never use a receipt's absolute `path`, nor a diagnostic's `link`/`target`.** Those point
   into REA's private runtime root (`PrivateRuntimeRoot`, `FirmwareProvider.js:151`), which is
   removed when the run finishes; only `relative_path` survives.

Equivalently: *the oracle is frozen relative to the same root the extraction tool wrote into
(sasquatch's `-d` output directory), and the receipt path is that root's name in front of the
oracle's relative path — one segment for a whole-file chunk, more for carved/nested chunks.*

---

## 2. Contract reconstruction (evidence chain)

### 2.1 REA 6.5.0 (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist`)

* `firmware/FirmwareFiles.js:37` — the input is copied to `<private root>/firmware.bin`
  (mode 0400). With a range, `FirmwareFiles.js:82-85` slices it to `<private root>/selected.bin`.
  **The user's file name never reaches unblob.** Measured: input `F1.sqsh` →
  `firmware.bin_extract`; same bytes with `--offset 0 --length 2417` → `selected.bin_extract`.
* `firmware/FirmwareProvider.js:151-159` — the private runtime root is created and `cwd` is set to it; `:226` `outputRoot =
  <private root>/extracted`; `:227-241` the unblob argv is
  `--process-num 1 --depth <max_depth> --randomness-depth 0 --report <report> --log <log>
  --extract-dir <outputRoot> <absolute input path>`.
  The input is an **absolute path outside** the extract directory.
* `firmware/FirmwareFiles.js:122-180` — `inventoryFirmwareOutput` walks the output with
  `lstat`/`opendir` (no symlink following) and records
  `relativePath: relative(root, path).split(sep).join("/")`, `kind ∈ file|symlink|special`,
  `linkTarget` via `readlink`.
* `firmware/FirmwarePublication.js:66-96` — every staged `file` is re-hashed and published as
  `{relative_path: entry.relativePath, path: join(tree.outputRoot, entry.relativePath), sha256,
  size, reported_sha256, mime_type, analysis_depth}`; non-files become
  `unpublished_entries` (`relative_path, kind, link_target`). Nothing is renamed.
* `firmware/FirmwareReports.js:145,225-230,341-357` — report task paths → `$output/<rel>`;
  `depth >= maxDepth` → `depth_limited_paths`; derivation edges carry `child_path` (the
  extract dir), `handler`, `parent_file_range`.
* `firmware/FirmwarePublication.js:294-306` — gap rows: `depth-limited` with
  `relative_path: null` and `input_path` = the extract dir; `unpublished-entry` with
  `relative_path` = the entry's staged relative path (bare form).

### 2.2 unblob 26.6.4 (`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob`)

1. **Root directory name** — `processing.py:116-129`:
   `_get_output_path` maps a path inside the extract root to its relative form and any other
   path to `Path(path.name)`; `get_extract_dir_for(path)` appends `extract_suffix` to the
   **file name**. Suffixes default to `_extract` for both extract and carve
   (`cli.py:345-356`, `processing.py:104-105`). Root task: `processing.py:144`.
   ⇒ depth 0 root = `<extract-dir>/<input basename>_extract` = `firmware.bin_extract`.
2. **Whole-file chunk ⇒ no carve, no prefix** — `processing.py:561-573`:
   `is_whole_file_chunk = len(outer_chunks) + len(unknown_chunks) == 1`; then the chunk is
   extracted straight into `get_extract_dir_for(task.path)` with
   `remove_extracted_input=False`. This is the round-40 V1/V2/L1/L2 shape and the F1 shape.
3. **Several chunks / a chunk at a nonzero offset ⇒ carve directory == the same directory**
   — `processing.py:581-612`: `carve_dir = get_carve_dir_for(task.path)` (identical name to
   the extract dir), carved name `f"{chunk.start_offset}-{chunk.end_offset}.{handler.NAME}"`
   (`extractor.py:131`; unknown/padding chunks use `.unknown`/`.padding`, `extractor.py:123`),
   extraction into `get_extract_dir_for(carved_path)` = `<carve dir>/<start>-<end>.<handler>_extract`.
   The carved input is unlinked after a successful extraction (`processing.py:662-666`) but an
   **unknown/padding carve stays published** as a regular file (measured: `0-4096.padding`).
4. **Links are rewritten or removed, and that is silent for the unsafe cases**
   — `extractor.py:50-113` (`fix_extracted_directory` → `fix_symlink`):
   loop → removed (`:58-65`); **empty target → removed with no report** (`:68-71`);
   absolute target → leading `/` stripped (`:73-75`); outside the extraction dir →
   `MaliciousSymlinkRemoved` report + unlink (`:79-87`); otherwise rewritten to a relative
   target computed from the extraction dir (`:89-91`).
   ⇒ `unpublished_entries[].link_target` is **not** the stored SquashFS target for absolute
   links, and a removed link appears in *neither* list, only in `diagnostics`.
5. **Normalisation.** Entry names are written through `FileSystem` (`file_utils.py:500-514`);
   a name that would escape is redirected into a lost+found path
   (`file_utils.py:434-450`, `make_lost_and_found_path` at `:416-421`, `.`→`dot`,
   `..`→`dot-dot`). Directory paths are `.resolve()`d (`processing.py:116-123`), entries are
   not. Consequently the published relative paths contain no `.`/`..`/`//`/trailing-slash
   segments in the normal case (Node `relative()` of real dirents), directory names are
   preserved verbatim (measured: `lib/firmware_extract/marker.bin` survived as-is), and no
   image-internal symlink re-roots a path, because inventory never follows links.

### 2.3 Measured shapes (all six receipts in `artifacts/R41C1Revenger/receipts/`)

| fixture | input | chunk root as the receipt states it | published regular / non-regular |
|---|---|---|---|
| F1 | 1 whole-file AVM-BE squashfs | `$output/firmware.bin_extract` | 5 / 4 |
| F1range | same bytes via `--offset 0 --length 2417` | `$output/selected.bin_extract` | 5 / 4 |
| F2 | 4096 B zeros + that squashfs | `$output/firmware.bin_extract/4096-6513.squashfs_v4_be_extract` | 6 / 4 (incl. `…/0-4096.padding`) |
| F3 | outer squashfs containing F1 as `nested/inner.squashfs`, `--max-depth 2` | `$output/firmware.bin_extract/nested/inner.squashfs_extract` **and** `$output/firmware.bin_extract` | 7 / 4 |
| F4 | escaping + absolute + in-tree links | `$output/firmware.bin_extract` | 2 / 2 |
| F6 | two concatenated squashfs chunks | `$output/firmware.bin_extract/0-2417.squashfs_v4_be_extract`, `$output/firmware.bin_extract/2417-3029.squashfs_v4_be_extract` | 7 / 6 |

Every run: `exit=0`, `depth-limited` present at the reached depth (the *extract dir*, never a
file), `unpublished-entry` per surviving link.

---

## 3. Counterexamples to `rel = path.split('_extract/', 1)[1]`

All measured; the runnable comparison is `artifacts/R41C1Revenger/rel-exact-rule.py` and its
captured output `demo-output.txt`.

**C1 — carve at a nonzero offset (F2).** Receipt: `firmware.bin_extract/4096-6513.squashfs_v4_be_extract/etc/a.txt`.
`split('_extract/',1)[1]` → `4096-6513.squashfs_v4_be_extract/etc/a.txt`.
Result: **0/5** oracle regular files matched; the same receipt under the rooted rule: **5/5**.
Round-40's `rel_suffix` (drop the first `*_extract` segment) is identical here: 0/5.
Beware the second-order effect: `firmware.bin_extract/0-4096.padding` is published and, under
`split`, appears as an oracle "extra" (`0-4096.padding`).

**C2 — nested chunk root (F3, `--max-depth 2`).** `firmware.bin_extract/nested/inner.squashfs_extract/etc/a.txt`
→ `split` and `rel_suffix` both yield `nested/inner.squashfs_extract/etc/a.txt`: 0/5, while the
rooted rule scores 5/5 against the inner oracle and 2/2 against the outer one. The prefix is as
deep as the path to the nested image, so no fixed segment count can be assumed.

**C3 — two sibling chunk roots (F6).** `split` returns
`0-2417.squashfs_v4_be_extract/etc/a.txt` and `2417-3029.squashfs_v4_be_extract/etc/f.txt`:
0/5 for the first image's oracle. This also shows why the matcher must key on `(root, rel)`:
rooted-at-both-roots with a flattened dict collapses `sbin/tool` (5000 B vs 3000 B) into one
row — the one collision that survives exact name comparison.

**C4 — a directory whose own name ends in `_extract`.** `firmware.bin_extract/lib/firmware_extract/marker.bin`:
first-occurrence split is accidentally right (`lib/firmware_extract/marker.bin`), but any
greedy variant is wrong — `rsplit('_extract/',1)[1]` → `marker.bin`, and a
`.*_extract/(.*)` regex → `marker.bin`. A suffix-based matcher (`same_rel`) is immune to this
one but pays for it in C6.

**C5 — range mode.** With `--offset/--length` the root is `selected.bin_extract`, not
`firmware.bin_extract`, and never the caller's file stem (`F1.sqsh_extract` does not exist).
A matcher that hardcodes the root or reconstructs it from the input name is wrong on the first
range run; take the root from `derivations` (or from `parameters.range` presence) instead.

**C6 — `same_rel` still reproduces R40-CL1.** Even with the root mapped exactly, the round-40
suffix test admits a false positive in *every* fixture: regular `usr/bin/busy` is claimed at
the non-regular oracle path `bin/busy` (`same_rel`, `c1-counter.py:606-607` → `endswith('/bin/busy')`).
The exact rule reports `exact-name hits: []` on all six receipts. Exactness must be `==`,
applied to both directions (`files` vs oracle regular, `unpublished_entries` vs oracle
non-regular; and "no non-regular path appears in `files`").

**C7 — traversal-redirected names.** A name that would escape the extraction dir is published
at a lost+found path (`file_utils.py:434-450`), so the receipt rel and the oracle rel differ by
more than a prefix. No matcher can repair that; the correct behaviour is "not published at the
oracle path" plus the gap row. It also means "publishes no non-regular entry at its exact
path" must be evaluated on paths only.

**Also falsified by C1/C2: "the first `_extract` segment is the chunk root".** In F6 the first
`_extract` segment is `firmware.bin_extract` (the *carve* directory) while the chunk root is
`firmware.bin_extract/0-2417.squashfs_v4_be_extract`. In unblob the carve and extract
directories share the same name (`processing.py:125-129`), which is exactly why this
confusion is easy to make.

---

## 4. What the round-41 counter should encode

```python
def strip_output(p):                     # step 1: one optional prefix
    while isinstance(p, str) and p.startswith('$output/'):
        p = p[len('$output/'):]
    return p

def chunk_roots(nr):                     # step 2: from the receipt, not the text
    return sorted({strip_output(d['child_path']) for d in nr['derivations']
                   if (d.get('handler') or '').startswith('squashfs_v4')},
                  key=lambda r: (-len(r), r))

def oracle_rel(path, root):              # step 3: whole-segment prefix
    p = strip_output(path)
    if p == root: return ''
    if p and p.startswith(root + '/'): return p[len(root) + 1:]
    return None                          # another namespace: exclude, not "extra"
```

Bindings worth freezing next to it (each is a one-line assertion on the receipt, and each
would have caught a round-40-style masking):

* `len(chunk_roots(nr)) >= 1` and the intended root is *in* that set (record the intended root
  in `carriers.json`, e.g. `oracle_root: "firmware.bin_extract"`);
* `chunks` contains exactly one `handler == "squashfs_v4_be"` with `extraction_failed == false`
  and `range.offset == 0` when the carrier is carved to `bytes_used` (V3-style);
* every `files[]` entry maps into a root (no `None` buckets) — otherwise the run has carve
  artifacts and the oracle root was chosen wrongly;
* `set(rel(f) for f in files) ∩ set(oracle non-regular rel) == ∅` **by equality**, and the
  same for `unpublished_entries` vs oracle regular rel;
* `depth_limited_paths == ['$output/' + root]` at `max_depth 1` (a successful whole-file run
  still carries one depth-limited gap at the root: measured on all four round-40 receipts and
  on F1/F2/F4) — so the frozen gap rule must allow exactly that row.

---

## 5. Attacks on the draft (R41-C1 wording, carriers)

1. **"exact path relative to the chunk's extract root" is under-specified for the counter.**
   The claim does not say how the counter learns the root. If it is learned by text
   (`_extract` segment) the four carriers pass by luck in the whole-file case and the predicate
   silently becomes suffix-like again on any carrier with a leading offset. Freeze the root
   per carrier in `carriers.json` *and* assert it equals the receipt's derivation root.
2. **Carve the carriers to `bytes_used`, starting at offset 0.** V3/V4 as drafted ("carved to
   `bytes_used`") give the whole-file shape (root `firmware.bin_extract`), identical to
   round-40's V1/V2, so the round-40 receipts stay usable as development evidence and the
   round-41 predicate is comparable. If a carrier keeps any leading byte, the root becomes
   `firmware.bin_extract/<start>-<end>.squashfs_v4_be_extract` and the "exact path" statement
   must name *that* root.
3. **V4's two readings must be resolved now.** "The nested `filesystem_core.squashfs` of
   FRITZ.Box_5491, if it is AVM-BE and fits REA's entry budget at depth 1" — at `max_depth 1`
   on the wrapper image, `filesystem_core.squashfs` is *carved and published as a member file*
   (as in round-40 V2: `firmware.bin_extract/filesystem_core.squashfs`, sha256 in the receipt),
   never extracted; its contents are not in the receipt at all. To score the *contents* the
   carrier must be that member carved out (then root = `firmware.bin_extract` again). The two
   readings have different oracles and different roots; the freeze must pick one, and the
   fallback ("the 5491 wrapper member") is the *other* reading.
4. **The budgets that decide V4 are tighter than the draft implies.** `max_output_files`
   defaults to 10,000 and is capped at 100,000, and it counts **every dirent — directories and
   links included** (`domain/firmware/firmwareAnalysis.js:46-52`; `FirmwareFiles.js:151,161-168`
   increments per name and throws `Staging entry budget exceeded`). `max_output_bytes` defaults
   to 256 MiB (cap 512 MiB), the input cap is 128 MiB, and each run has a **120 s** deadline
   (`firmware/FirmwareRelease.js:27-33`). A full FRITZ rootfs (thousands of files + dirs +
   links) can exceed 10,000; the counter must surface that as an inventory error, not as a
   negative, and the V4 decision has to be made by counting the oracle's rels + directories +
   links.
5. **Non-regular comparison must ignore `link_target`** (or normalise it the way unblob does:
   absolute target `/X` becomes `relpath(root/X, dir(link))`, `extractor.py:73-91`). Round-40's
   nonregular TSVs hold paths and kinds only — keep it that way; a target-comparing oracle will
   disagree with every absolute link (measured: oracle `bin/busy -> /usr/bin/busy`, receipt
   `bin/busy -> ../usr/bin/busy`).
6. **V3/V4 oracle provenance.** The round-40 oracle shape is "sasquatch output dir enumerated
   independently"; the rule above is exactly "receipt root + '/' + that enumeration", so no
   oracle rewrite is needed — only the per-carrier root binding and the `==` comparison.
7. **L3/L4 (lane-built, both-direction collisions).** The owned collision class (regular file
   whose path ends with a symlink's path, and the reverse) is already exercised by F1
   (`usr/bin/busy` regular vs `bin/busy` link; `bin_busy_abs_placeholder` link vs any `*busy`
   regular). It is caught only by equality — `same_rel` calls it a match (C6). Add to the
   counter's selftest: one fixture *per* direction, exact verdict `published`, suffix verdict
   `mismatch`.

---

## 6. Evidence — commands, exit codes, artifacts

Scratch root (removed before yield): `/fast/scratch/hyaku/kaidoku-r41/R41C1Revenger`,
`TMPDIR` set there; every REA run `cd`'d there first (unblob writes `unblob.log` into cwd).

Fixtures (lane-built, no vendor bytes; rebuilt by `artifacts/R41C1Revenger/build-fixtures.sh`):

```
python3 -I -B <lane>/tools/round-40/gen-squashfs.py fx/t1 fx/F1.sqsh --endian avm-genuine --comp xz   # exit 0
sha256 F1.sqsh e274b9067e2ff036b02981787e59658863355ab58c1ccb74979a1f77ce9dc6bc  (2417 B)
F2.bin  926548bd5d1daa995cb4f5cb98581c4f6d9475d4bf8f7b5c8b6349b5a5f2c725  (6513 B, 4096 B zeros + F1)
F3.sqsh fcab77b7e462f9f7dbb130cfdc335c7eb4ba64920b7f15618f453f258bed8f2c  (1185 B, contains F1)
F4.sqsh 94b7b0d4f9647067d9f48165c38ba008ee7a38ab7e466b944aa2f4b7c2eaa827  (612 B)
F6.bin  df0b8571b71cb0c478641a90cecbafd2cd9fe7d320fdd967a5e978543cc7fcf4  (3029 B, F1||F4)
```

Runs (`cd "$S"`, all `exit=0`; receipts kept in `artifacts/R41C1Revenger/receipts/`):

```
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
    --format json --full-output --max-depth 1 F1.sqsh            run-F1        # exit 0
... --max-depth 1 --offset 0 --length 2417 F1.sqsh               run-F1range   # exit 0
... --max-depth 1 F2.bin                                         run-F2        # exit 0
... --max-depth 2 F3.sqsh                                        run-F3        # exit 0
... --max-depth 1 F4.sqsh                                        run-F4        # exit 0
... --max-depth 1 F6.bin                                         run-F6        # exit 0
```

Matcher comparison (`artifacts/R41C1Revenger/demo-output.txt`, exit 0 on every invocation):

| receipt | oracle root | exact | split | round-40 `rel_suffix` |
|---|---|---|---|---|
| F1 | `firmware.bin_extract` | 5/5 | 5/5 | 5/5 |
| F1range | `selected.bin_extract` | 5/5 | 5/5 | 5/5 |
| F2 | `…/4096-6513.squashfs_v4_be_extract` | **5/5** | **0/5** | **0/5** |
| F3 (inner) | `…/nested/inner.squashfs_extract` | **5/5** | **0/5** | **0/5** |
| F3 (outer) | `firmware.bin_extract` | 2/2 | 2/2 | 2/2 |
| F6 (root A) | `…/0-2417.squashfs_v4_be_extract` | **5/5** | **0/5** | **0/5** |

`same_rel` false positive on every receipt: oracle non-regular `bin/busy` claimed by the
published regular `usr/bin/busy`; exact rule: no hit.

Artifacts (all under `.ufo/waves/round-41/w1/artifacts/R41C1Revenger/`):
`rel-exact-rule.py` (matcher + comparison, 3 matchers × 3 directions),
`build-fixtures.sh`, `fixtures/{F1.sqsh,F2.bin,F3.sqsh,F4.sqsh,F6.bin}`,
`receipts/{F1,F1range,F2,F3,F4,F6}.out.json` (full REA CLI JSON, `--full-output`),
`oracle-t1.tsv`, `oracle-t3outer.tsv`, `rea-summary.tsv`, `demo-output.txt`, `manifest.sha256`.

---

## 7. Confidence and limits

* **High confidence** (source + live measurement, two independent shapes): root naming,
  carve naming, sibling placement of nested roots, `$output/` prefix split, whole-file-chunk
  behaviour, padding/unknown carve artifacts staying published, absolute-link rewriting,
  escaping-link removal, `selected.bin_extract`.
* **Medium confidence** [INFERENCE]: that *every* round-41 carrier will take the whole-file
  shape. It follows from "carved to `bytes_used`, offset 0" plus `is_whole_file_chunk`
  (`processing.py:561`), but it was not run on V3/V4/L3/L4 (reserved; no REA/unblob touched
  them, and none of the reserved images was opened).
* **Not measured**: device/fifo entries (`special`) — `gen-squashfs.py` emits no device nodes
  (`tools/round-40/gen-squashfs.py` header "Todos ... no device nodes"). Source reading says
  they are staged via `mknod`/`mkfifo` (`file_utils.py:546-557`) and would appear as
  `kind: "special"` in `unpublished_entries` with host-privilege dependent success
  (`has_root_permissions`, `file_utils.py:491`) — treat `special` as non-regular and
  environment-sensitive [INFERENCE].
* **Not measured**: `make_lost_and_found_path` redirects — impossible to emit through the
  round-40 writer (names are fixed by `os.walk`); read from source only.
* Unblob's own `--carve-suffix`/`--extract-suffix` overrides are not reachable through REA
  (REA passes neither), so the suffix is always `_extract`.

## 8. Hygiene / tooling

No installs, no upgrades, no `~/.local/bin` writes, no VCS mutation, no writes outside this
report and this artifacts directory, no REA/unblob run on any reserved image or member (only
lane-built fixtures under my own scratch). Tools used read-only: REA 6.5.0 from the pinned npx
cache (via `npx`, offline), unblob 26.6.4 at `~/.local/share/uv/tools/unblob`, sasquatch 4.5.1
(reached only through REA/unblob). Scratch removed after the artifacts were copied out.
