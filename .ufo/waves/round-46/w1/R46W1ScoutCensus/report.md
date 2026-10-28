# R46W1ScoutCensus — independent C2 census

Freeze `31820472784284727546808acc31b3ea1e73919b`. Claims read: `plans/round-41-claims.md` through `plans/round-46-claims.md` at that commit (`git show`). Census compared: `tools/round-46/census.json` at that same commit (`jq -r '.paths[]'`). `tools/round-46/census.py` was not executed.

Axes: coverage of named `tools/round-4[1-6]/**.{py,sh}` paths; independence from the counter; exact set-diff against `census.json`; existence via `git cat-file -e`.

## Counts

| set | count |
|---|---|
| Derived (brace-expanded names, then present at the freeze) | **42** |
| `census.json` `.paths` | **38** |
| Contiguous `grep -oE` only (no brace expansion) | **38**, identical to `.paths` |
| `.named_but_absent` | **0** |
| Derived named-but-absent | **0** |

Symmetric difference (LC_ALL=C `comm`, deciding run):

- derived minus JSON (4), all present at the freeze as blobs (`git cat-file -e` exit 0, `git cat-file -t` = `blob`):
  - `tools/round-42/c1-extra.py`
  - `tools/round-43/build-copies-r43.py`
  - `tools/round-43/c2-controls-r43.py`
  - `tools/round-43/receipt-wrap.py`
- JSON minus derived: empty

Every one of the 38 census paths is a tracked blob at the freeze: `census_n 38`, `census_fail 0`. A negative control `tools/round-46/does-not-exist.py` exits 128 (`fatal: path 'tools/round-46/does-not-exist.py' does not exist in '31820472784284727546808acc31b3ea1e73919b'`), so the probe is not vacuously zero.

## Where the four are named

The scope sentence (`plans/round-46-claims.md` lines 121-124) is: every path matching ``tools/round-4[1-6]/**.{py,sh}`` that is named in a `plans/round-4[1-6]-claims.md` at `--rev`, restricted to paths that exist there; named-but-absent paths go in `named_but_absent` and do not enter the scope.

These four are named only inside shell brace groups, not as a contiguous `tools/round-4N/file.py` token:

- `plans/round-42-claims.md:183` — ``tools/round-42/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-carrier.py,sqfs3-oracle.py,unblob-logtee.sh,prior-pins.json,rea-pkg.json}``. `prior-pins.json` and `rea-pkg.json` are not `.py`/`.sh` and were not taken. Line 209 names the bare basename ``c1-extra.py`` only; that basename was not promoted to a path.
- `plans/round-43-claims.md:263` — ``tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py,c2-score-r43.py,receipt-wrap.py,verify-copies-r43.py,build-copies-r43.py}``.

Other brace groups in rounds 41-43 expand to paths that also appear as contiguous tokens, so they are already in the JSON. The scope glob on `plans/round-46-claims.md:122` (``tools/round-4[1-6]/**.{py,sh}``) does not match the brace extractor: `[1-6]` is not a single round digit.

## Why the JSON is 38

Read, not run: `tools/round-46/census.py:27` is `TOOL = re.compile(r"tools/round-4[1-6]/[A-Za-z0-9._/-]+\.(?:py|sh)")`. `{` and `,` are outside that class, so a brace group is not a match and the inner basenames have no `tools/round-4N/` prefix. An independent `grep -oE` of that same class over the six frozen claim blobs, `sort -u`, is byte-identical to `jq -r '.paths[]' | LC_ALL=C sort` (sha256 `033e8c44db02525a29990244d87a73d4424a65117c1abb8074e1b2c550e9f85b`, `diff` exit 0). The JSON matches the regex. It does not match the claim sentence if a brace group names its members. Those four paths are in neither `.paths` nor `.named_but_absent`.

`tools/round-41/c1-extra.py` is in the JSON because it is also a contiguous path at `plans/round-41-claims.md:84`. `tools/round-42/c1-extra.py` is not.

## Not part of the difference

Tracked `*.py`/`*.sh` under `tools/round-4[1-6]/` at the freeze: 46. Four exist and are not named in the six claim files, so they are correctly outside both sets:

- `tools/round-44/c1-controls.py`
- `tools/round-44/c1-oracle.py`
- `tools/round-44/c1-run.py`
- `tools/round-44/c2-controls.py`

No boundary-truncated regex hit (character before and after every contiguous match was not in `[A-Za-z0-9._/-]`). Bare names that are not this glob: `tools/round-40/gen-squashfs.py`, `tools/round-39/gen-squashfs.py`, unblob `squashfs.py`, `.ufo/.../verify-copies.py`, `jj-lane.sh`. `nested.sh` was a prefix false friend of `nested.sha256` in a bare-name scan and is not a path.

## Receipts

Deciding run (supersedes an earlier `comm` that used locale sort and falsely listed `tools/round-42/sqfs3-oracle.py`; that path is in both sets). Command, exit, stdout sha256, UTC:

- UTC `2026-10-28T16:58:02Z`. Command: `LC_ALL=C sort -u` on the derived list and on `jq -r '.paths[]'`; `diff -u`; `comm -23` / `comm -13`; `git -C LANE cat-file -e REV:path` for all 38 census paths, the 4 difference paths, and the negative control. Wrapper exit **0**. `diff` exit **1** (sets differ; this is diff's exit, not a counter exit). `literal` vs JSON `diff` exit **0**. stdout sha256 `5ac58e077ec448c2b6bb8a4872e8d36c5d1ef1456405503217769c8ec8bb0494`. Copy: `receipt2.txt` (file sha256 `147b304eb103f480a41964186be5347c8641fce9ddb2e0f60e9ae2381d5868d3`).

- Extraction that built the lists, UTC `2026-10-28T16:57:45Z`, each exit 0: contiguous `grep -oE` stdout sha256 `d24ab2b14e07c817cc92bb78f02ede72c57c5c4a6703528e58e508486064ccde` (38 paths); brace-union `python3 -c` stdout sha256 `e6a160165c34de15523d2de955010c0bc75f928964ac9e42b626d0a680102f0e` (named 42, present 42, absent 0); `jq` stdout sha256 `06a332be67d166d8da109b744b85998e9c3c5527541fc6864ec7375e3a218537` (`json_paths 38`, `named_but_absent 0`). The `comm` inside that first receipt is not authoritative.

Lists: `derived.txt` (42, sha256 `f22bf386c4b8744907b319f704eaf05312bb6aff3bc85486305ee04f0d81dcd2`), `json-paths.txt` and `literal.txt` (identical, sha256 above).

No tool installed. Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1ScoutCensus` removed after these copies.
