# R44W2Census — registry integrity

Seat `R44W2Census`. No tools installed. Lane HEAD at measurement `8bb1090af3fef64477c4337855e4347472db2701` (detached; not moved). `corpus/SOURCES.md` blob is identical at freeze `c48f8a4`, measured `55bcce69`, HEAD, and the worktree: git blob `c513fad08543075d304c49af212005153d64a22e`, sha256 `90a10fddc549777e841182986f4841d4736721ac05955d85bbf1d11641255dfd`. Base `c29360e3` blob `d0e6770a85f4be9a5e09865f4e8cce5934c2b7fe`.

Census script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`. W04 is same first source-URL, different scope string (`scripts/sources-census.sh:644-645`). E04 is same URL and same scope, non-rejected, no `supersedes S###` (`:646-649`). E03 is a duplicate id (`:641`). Neither warning changes a clean exit (`:18`, `:803-806`).

## Verdict

The registry change is a pure append of S138 and S139. Current `validate` is exit 0, `kaidoku ok`, 14 W04, no E-code. Ids `S001`–`S139` are contiguous, unique, and all inside `## Registry`. Both new rows have 11 cells. No pre-existing row changed any cell, including `status` / `recheck` / `used-by`.

S138's W04 partner is **S130** (`corpus/SOURCES.md:136`), the same normalized URL, **different scope strings**. That is across-scopes (W04), not a within-scope duplicate (E04) and not a duplicate id. The lesson's round-start sentence says otherwise. See CENSUS-1 and CENSUS-2.

## Receipts

1. Current tree, the lesson's command.

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

exit **0**. wall **0.229187 s**. stdout sha256 `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` (1518 bytes). stderr empty. Copy: `.ufo/waves/round-44/w2/artifacts/R44W2Census/census-validate-head.txt`. Last line: `kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. No `E` lines.

2. Base tree `c29360e3` (detached worktree; `git -C <worktree> rev-parse --show-toplevel` was the worktree, lane HEAD stayed `8bb1090a`).

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-28 <base-worktree>
```

exit **0**. wall **0.222921 s**. stdout sha256 `4e22182bc1200607129cfc5ef425ef2b14564c143ab55ea4358f5045451aa444` (1399 bytes). stderr empty. Copy: `.ufo/waves/round-44/w2/artifacts/R44W2Census/census-validate-base-c29360e3.txt`. **13 W04, zero E, S138 absent**, then `base-wt ok`.

3. Row counts, pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}`.

- worktree `corpus/SOURCES.md`: **139**, grep exit 0
- `git show c29360e3:corpus/SOURCES.md`: **137**, grep exit 0
- `git show c48f8a4:corpus/SOURCES.md`: **139**
- `git show 55bcce69:corpus/SOURCES.md`: **139**

4. `git diff c29360e3..55bcce69 -- corpus/SOURCES.md`: exit **1** (a diff exists). numstat `3 0`. One hunk `@@ -141,6 +141,9 @@`: added S138, added S139, added one blank line; **zero deletions**. Only commit in that range touching the file: `b2a1bd91` `round-44: freeze-reviewed claims and S138/S139 source rows`. Copy: `.ufo/waves/round-44/w2/artifacts/R44W2Census/sources-diff-c29360e3-55bcce69.diff` sha256 `215d49d5caa2c63764c5cf68ad159dbb9acfbe6dcbce6ceb47ac6a23a5f7886b`.

`git diff c48f8a4 55bcce69 -- corpus/SOURCES.md` and `git diff 55bcce69 HEAD -- corpus/SOURCES.md` are empty. `git log 55bcce69..HEAD -- corpus/SOURCES.md` is empty. Freeze commit `c48f8a4` has sole parent `b2a1bd91` and its own diff does not touch `corpus/SOURCES.md`; the rows are in the freeze tree because that parent added them.

## What held

- Duplicate ids: none. Non-`S` ids: none. Gaps in `S001`–`S139`: none. Rows outside `## Registry`: none. Rows whose pipe-split cell count is not 11: none (census would have emitted E01 on `NF!=13`).
- Header `corpus/SOURCES.md:5` is the 11 names `id source kind tier scope anchor teaches status opened recheck used-by` (12 pipe characters).
- S138 `corpus/SOURCES.md:144` and S139 `:145`: 11 cells, awk `NF=13`, 12 pipes. Both `mined`, tier `A`. S138 kind `dataset`, opened `2026-10-28`, recheck `180d`. S139 kind `docs`, opened `2026-10-28`, recheck `on-release`. Both `used-by` = `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` (exists, 20164 bytes, text contains `S138` and `S139`).
- Shared ids base∩measured = 137. Cell-tuple mismatches = 0. `status` / `recheck` / `used-by` mismatches = 0. Ids only at measured: `S138`, `S139`.
- S139's normalized first URL `github.com/plougher/squashfs-tools/releases` has no other holder. S113's URL is the child path `…/squashfs/squashfs_v4_be/__input__` and does not match S138.

## S138 W04 — partner, not a real duplicate

Normalized first URL (census `url_of`: first `https?://` token, fragment and one trailing slash stripped, host lowercased):

`github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs`

Holders, both `mined`, neither `teaches` contains `supersedes S`:

| id | line | scope (full) |
|---|---|---|
| S130 | 136 | MIT-licensed Git-LFS fixture bytes and expected member trees for the unblob 26.6.4 SquashFS handler family (v1, v2, v2-nonstandard, v3, v3-adaptive-LZMA, v3-Broadcom, v3-DDWRT, v3-nonstandard, v4 LE, v4 BE, v4-Broadcom), the bytes a round-42 C2 generator may pin; not the handler code, not extractor behaviour, not a C1 carrier and not a vendor image |
| S138 | 144 | The second, cross-checking oracle for the R44-C1 carriers: unblob 26.6.4's committed expected member trees for `squashfs_v1` and `squashfs_v2`, both byte orders, as content-addressed member bytes (4 endian trees, 22 files); not handler code, not extractor behaviour, not a C1 carrier |

The scope strings differ, so the validator emits W04 and does not emit E04. Same-URL groups that would be E04: **none**. S130 already names v1 and v2 member trees, so S138 is a second mined registration of that URL under a narrower scope, which is the warning the script is built to allow. It is not an id collision and not a within-scope duplicate.

The other 13 W04 payloads are byte-identical at base and at HEAD (lane prefix differs only in the base-worktree run). S138 is the only payload added.

## Every current warning (exit 0)

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	W04	S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S123 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S138 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

S047's printed URL includes a trailing backtick because `url_of` keeps every non-space non-pipe byte (`sources-census.sh:601`). The same token is already the base warning. Not introduced by S138/S139 and not an E-code.

## Defects the record gets wrong

### CENSUS-1

`corpus/lessons/round-44.md:45-48` at HEAD `8bb1090a` (worktree lines 45-48 match; the worktree diff on this file does not touch them) says the round-start command

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`

yields `kaidoku ok`, exit 0, **14** W04, and that S138 is the 14th, **pre-existing**, a **within-scope** URL also present at another row's evidence pointer.

Observed:

- That command on the current tree: exit **0**, **14** W04, S138 is the 14th. stdout sha256 `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19`.
- The same validator on base `c29360e3` (receipt 2): exit **0**, **13** W04, S138 not in the output. stdout sha256 `4e22182bc1200607129cfc5ef425ef2b14564c143ab55ea4358f5045451aa444`.
- S138's partner is S130's **source** URL at `corpus/SOURCES.md:136`, not a side evidence pointer. Scopes differ, so the script's own word is `across scopes`. Within-scope would be E04 and would have made exit 1. Exit stayed 0. The other 13 warnings are pre-existing; S138's is not (the row does not exist at base).

`137 → 139` on lines 44-45 is true. "No `status`/`recheck`/`used-by` cell of an existing row was changed" on lines 49-50 is true.

### CENSUS-2

`corpus/lessons/round-44.md:49` cites `.ufo/waves/round-44/l1/sources-census-end.txt` as the round-end receipt.

- `git cat-file -e HEAD:.ufo/waves/round-44/l1/sources-census-end.txt` fails (not in `8bb1090a`, not in `55bcce69`).
- `git status --porcelain` shows `?? .ufo/waves/round-44/l1/sources-census-end.txt` and `?? .ufo/waves/round-44/l1/sources-census-start-replay.txt`.
- Other files in that directory are tracked by HEAD (`c1-score-at-55bcce69.json`, `c2-score-at-55bcce69.json`, `preflight-55bcce69.json`, `probe-fixture-404.txt`, …). These two are not.
- The worktree end file's sha256 **equals** receipt 1 (`9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19`). The bytes are a faithful current census. They are not in the commit that cites them.
- The untracked start replay begins `ERROR: config not found: /fast/scratch/hyaku/kaidoku-r44/l1/shokunin.conf` and then lists **13** `baseclone` W04 lines and `baseclone ok` for a scratch base clone. It is not a clean transcript of the lesson's round-start command, and it agrees with receipt 2 that the base registry has 13 warnings.

## Scratch

Base worktree removed and `/fast/scratch/hyaku/kaidoku-r44/R44W2Census` deleted before yield. Evidence kept under `.ufo/waves/round-44/w2/artifacts/R44W2Census/`.
