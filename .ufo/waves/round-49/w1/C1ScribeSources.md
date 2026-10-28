# C1ScribeSources — round 49, wave 1 (pre-freeze): SOURCES registry draft for S138/S139, Gate rows, entry-draft check

Seat `C1ScribeSources` · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` · measured 2026-10-28T21:07–21:15Z · read-only on the lane (no registry write, no git mutation, no install).

## Verdict

1. **Registry edit (S138, S139 `used-by`): ready, but conditional.** Append `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` to the existing cell (old → new below). `opened` stays `2026-10-28` = counter `OPENED`. NF=13 on both rows and the scratch census is clean (no missing path) **only when the r49 entry exists**. Landed alone it prints two `missing:` lines. It must land in the same post-freeze commit as the entry.
2. **Gate rows for S138/S139: drafted** (`w1/C1ScribeSources/lesson-gate-rows-S138-S139.md`), from my own re-open and the two peer re-opens. Both peer reports (`C1S138Reopen.md`, `C1S139Reopen.md`) exist and agree with my fetches on every pin I checked.
3. **The R49 entry draft is not landable as written.** Blocking: its status header asserts a round-49 score that is a round-44 score (counter sha `9f2cc140…` is the round-44 counter; `c48f8a4` is the round-44 freeze; the receipt is `round-44/controls/pos`). Also a wrong manifest digest in its S138 source line (`4bc53dbb…`; file is `06a72dd5…`). Both are text defects, fixable in landing text (the entry is not frozen).
4. **Counter defect, corroborated by `C1S139Reopen` D1 and by my read of the code:** `oracle_tool_ok` returns True when the `oracle` block is absent (`c1-counter.py` lines 2222–2227). Fold before the freeze.

Top findings for L1:
- **F5 (blocking, entry):** the status header pre-states a result. The pinned counter sha is the round-44 counter's.
- **F4 (blocking, entry):** S138 manifest digest wrong in the entry's source line.
- **F8 (counter, fold pre-freeze):** `oracle_tool_ok` vacuous when the `oracle` key is removed.

## 1. Registry edit (draft, not applied)

Only column 11 (`used-by`) of rows S138 and S139 changes:

| row | old `used-by` | new `used-by` |
|---|---|---|
| S138 | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` |
| S139 | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` |

Separator `, ` matches existing multi-path cells (S001 and others). Cell-level diff: only cell 12 changed on lines 144 and 145 (`diff`-based check, below). `status` (`mined`), `opened` (`2026-10-28`), `recheck` (`180d` / `on-release`) unchanged.

Full files: `w1/C1ScribeSources/registry-S138-S139-landing.md`, `registry-rows-S138-S139.edited.md`, `registry-S138-S139.diff`.

## 2. Census and binding checks (scratch copy; census run from the lane root and from a scratch tree)

Command file: `w1/C1ScribeSources/census-run.txt` (sha256 `dc9683df3fd5036e3fe7996810fe6b4d160d15f6716b618aa6113abcca48a02c`, `census-run.sh` exit 0). Registry sha256s: base `68e6d028744096a4d9e5b2e777ad7ed3e1c56dcc83778f839cb775119627e712`; edited `40889cbf36b16d9dd7e1e55aaecdbe92e81a597bcb5af454ea4f78b9a98afe27`. Lane `corpus/SOURCES.md` **not** modified (still `68e6d028…`).

| variant | command (form) | result |
|---|---|---|
| V0 base registry, lane root | CORPUS.md SOURCES census awk, `[ -e "$p" ]` from lane root | `malformed 0`, no `missing:` line; rows 146; S138/S139 NF=13 |
| V1 edited registry, lane root, entry absent | same | `malformed 0`; **`missing: corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` ×2** (expected pre-landing) |
| V2 edited registry in scratch tree, entry present | same, cwd = scratch tree (corpus copy + entry draft) | `malformed 0`, no `missing:` line |
| counter-shaped binding (python replica of `c1-counter.py` lines 2172–2184; `len(cells)==11`, `c[8]==OPENED`, `ENTRY in c[10]`) | `python3 - edited.md` heredoc, exit 0 | S138 ✓ S139 ✓; `sourced True` |

Exit codes: census script 0; `diff` base/edited exit 1 (expected: differs); `grep -cE` rows 146.
Cell-level diff (awk, FNR-keyed): `CHANGED line 144 cell 12` and `CHANGED line 145 cell 12` only.

Landing constraint: registry edit and entry in the same commit. Notes: `used-by` appears to omit lessons that cite these rows (see F9).

## 3. Gate rows (drafted)

Full text: `w1/C1ScribeSources/lesson-gate-rows-S138-S139.md`. Summary:

| row | URL | accessed (UTC) | located quote |
|---|---|---|---|
| S138 | `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` (tag); `https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs/squashfs_v1/big_endian/__output__?ref=26.6.4` | 2026-10-28T21:09Z (listing, HTTP 200, 1241 B); tree page 21:11:03Z (`C1S138Reopen`) | listing `[0].name`: `"name": "squashfs_v1.0_be.bin_extract"`; tree `<title>`: "unblob/tests/integration/filesystem/squashfs at 26.6.4 · onekey-sec/unblob · GitHub" |
| S139 | `https://github.com/plougher/squashfs-tools/releases`; API `…/releases/tags/4.7.5`; `…/git/tags/1fdc2fe01d681438a04e2a137a9f51d829ba3358`; `/usr/bin/unsquashfs` | release API 21:08:58Z (HTTP 200, 5873 B); tag object 21:11:43Z; page 21:07:48Z (`C1S139Reopen`) | `$.name`: `"name": "Squashfs tools 4.7.5"`; `$.object.sha`: `"sha": "708c59ae80853b0845017c33b42e56061cc546cd"`; `unsquashfs -version` line 1: `unsquashfs version 4.7.5 (2026/03/01)` (exit 1) |

Rationale for API quotes over page quotes: both rendered pages moved between fetches (S139 releases page: 398943 B in the row, 361752 B at 21:07:48Z; S138 tree page: 200946 B and 200958 B seconds apart, `C1S138Reopen` F1). The contents-API body hash also varies with request headers (`be3180fc…`, 11007 B here; `67a0fca8…`, 9960 B in `C1S138Reopen` F2). None of those is cited as identity.

## 4. Independent re-open receipts (this seat)

All run 2026-10-28, `curl -sS -L -m 60` with default headers unless noted. Receipt copies and `SHA256SUMS` (13 files; `sha256sum -c` exit 0): `w1/C1ScribeSources/receipts/`.

| # | command (abridged) | HTTP | bytes | sha256 | check |
|---|---|---|---|---|---|
| R1 | `curl … api.github.com/repos/plougher/squashfs-tools/releases/tags/4.7.5` | 200 | 5873 | `979b2d89a6d3cb4a395fb46381311a07b08315f267e18cc0dc6feb22cefa3591` | `"name": "Squashfs tools 4.7.5"` 1; `"tag_name": "4.7.5"` 1; `"published_at": "2026-03-01T23:05:47Z"` 1 (`grep -F -c`, exit 0 each) |
| R2 | `curl … git/refs/tags/4.7.5` | 200 | — | `d96fb53ce572aaaa9e32940c3b2f162ff84642f0ab58287645952cc266f4530d` | `"sha": "1fdc2fe01d681438a04e2a137a9f51d829ba3358"` 1, object type `tag` |
| R3 | `curl … git/tags/1fdc2fe01d681438a04e2a137a9f51d829ba3358` | 200 | — | `68b4ba6410859943a9e525c1eb1687521d81fa3ebfee650f38b282a3568b870a` | `tag 4.7.5`, object `708c59ae80853b0845017c33b42e56061cc546cd` type `commit` |
| R4 | `curl … api.github.com/repos/plougher/squashfs-tools/releases` | 200 | 54719 | `8d25bcd64ae87f596db10359f2cc892746db26fd96f65fbd3e9768d953b8c32f` | 9 releases, 9 distinct `tag_name` (row claim "9 distinct release tags" holds) |
| R5 | `curl … releases/tag/4.7.5` (rendered page) | 200 | 159465 | `ecb8bf473f259c82b50cbd6756a094af2eaa85ffe774c94df25fa5bc224024db` | not a pin; moved relative to the row and `C1S139Reopen` (159470 B tag page, 361752 B releases page) |
| R6 | `/usr/bin/unsquashfs -version` (stdout/stderr split) | **1** | stdout — | stdout `6154c39eee941fa66ea0ee7942802a2607d6ee2e749051c956569d7e9f6d333a`; stderr `e3b0c442…b855` (empty) | line 1 `unsquashfs version 4.7.5 (2026/03/01)`; exit 1 is the tool's convention |
| R7 | `sha256sum /usr/bin/unsquashfs` | 0 | 166976 (per reopen) | `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c` | equals the entry draft's and `carriers.json` pin (no install; host binary) |
| R8 | `curl … contents/…/squashfs?ref=26.6.4` (top) | 200 | 11007 | `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00` | 11 directory entries; `squashfs_v1` … `squashfs_v4_broadcom` |
| R9 | `curl … squashfs_v1/big_endian/__output__?ref=26.6.4` | 200 | 1241 | `8a59dc516ae92910c0a2c0a1a645590cfb82795567586839ea27a892022aad58` | `[0].name` `squashfs_v1.0_be.bin_extract` 1 |
| R10 | same, `squashfs_v1/little_endian` | 200 | 1256 | `f842973bc4db4f51e3ddaa4160dc63aeaadb0ea3bed7ce587d5be3d573af9716` | `squashfs_v1.0_le.bin_extract` |
| R11 | same, `squashfs_v2/big_endian` | 200 | 2479 | `580741c583d22b890a281d39e7a4286b4716250b161c2dd91a2db546cacf53d5` | `squashfs_v2.0_be.bin_extract`, `squashfs_v2.1_be.bin_extract` |
| R12 | same, `squashfs_v2/little_endian` | 200 | 2509 | `c1726865cd3e3050b98a6cde969e4cbebf09f07d04f731c36202f8aedd9980f0` | `squashfs_v2.0_le…`, `squashfs_v2.1_le…` |
| R13 | `curl … squashfs-tools/releases` rendered page (lineage) | 200 | 159465 | (as R5) | not used |

Not re-run by this seat: the 22-member digest and the 10-listing set (run by `C1S138Reopen` F0/F5: `mismatch 0` of 22, manifest sha256 `06a72dd5…`). The S139 page digest in the row (`d08749f4…`, 398943 B) is a round-44 fetch and was not reproduced today.

Identity confirmations (match row / entry draft): tag `4.7.5` → `1fdc2fe…` → `708c59ae…` (R2–R3); 9 releases (R4); `unsquashfs -version` text and exit (R6); binary sha `461e1fd9…` (R7); `published_at` (R1).

## 5. Entry draft: defects touching S138/S139 and pre-filled results

Draft file: `w1/artifacts/R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`. Lines are the draft's own.

| ID | severity | line(s) | finding | evidence (command → exit → value) | fold |
|---|---|---|---|---|---|
| F4 | **blocking** (wrong source digest) | 12 (S138 source) | cites manifest sha256 `4bc53dbba8beee0fbf912771efc0a55fd47a197cca1f56d2aaed790f817c1a13`. The file is `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`. | `sha256sum corpus/evidence/round-44/oracle/manifest.json` → 0 → `06a72dd5…f5fe`; `grep -c 4bc53dbb` on the committed manifest = 0; on the draft = 1. Already flagged by `round-44-verifier-spotcheck.md` (S138 row) and by `C1S138Reopen` F8. | replace the digest in the landing text. The counter does not read it (`sourced` binds only id, `opened`, `used-by`), so this is a disclosed gap, not a counter catch. |
| F5 | **blocking** (pre-filled result; reference drift = M49-1 class) | 3–7 (status) | states round-49 scoring: "counter sha256 `9f2cc140…` … against the round-49 freeze `c48f8a4…`: `carriers_matched 4/4`, `met_target true`, exit 0 … Scored-run receipt `.ufo/waves/round-44/controls/pos/counter.json`". (a) `9f2cc140…` = sha256 of `tools/round-44/c1-counter.py` at `c48f8a4` (`git show c48f8a4…:tools/round-44/c1-counter.py \| sha256sum`). The draft round-49 counter is `d6d70cb7…` (`sha256sum .ufo/waves/round-49/draft/tools/round-49/c1-counter.py`). (b) `c48f8a4` = `round-44: freeze C1/C2 claims, carriers, counters, and controls` (`git show -s`, ancestor of HEAD `e4f2cfa5…`), not a round-49 freeze. (c) the receipt is round-44's. | — | strip the header to "pending data run". The landing text may cite only the post-freeze counter's own receipt and sha256. This is the "copy last round's run" shortcut in prose. |
| F7 | defect (provenance) | 12–13 | S138/S139 lines cite round-44 fetch times (`2026-10-28T11:10:29Z–11:12:37Z`; S139 `2026-10-28 (HTTP 200)`) while the Frontier step says the sources were re-opened this round. | round-49 re-open receipts now exist (21:07:48Z–21:11:43Z; this seat R1–R9; `C1S138Reopen`, `C1S139Reopen`). | cite the round-49 re-opens and the Gate rows in §3. |
| F6 | minor (copy) | 21 | "Round 44 adds the `## Round-49 additions to Core` row" inside a round-49 entry. | `grep -n "Round 44 adds"` line 21 | fix the wording. |

Entry text not defective for my rows: the S139 source line's binary sha `461e1fd9…`, version line, `squashfs-tools 4.7.5-1` (`C1S139Reopen` pacman receipts), and `HTTP 200, tag present` all match this seat's R6–R7 and the peer's receipts.

## 6. Counter defect, corroborated (outside my seat's files; reported because it is pre-freeze)

**F8 — `oracle_tool_ok` is vacuous when the `oracle` key is missing.** `.ufo/waves/round-49/draft/tools/round-49/c1-counter.py` lines 2222–2227:

```python
def oracle_tool_ok(spec):
    """(ok, detail) for the frozen oracle identity against the live binary."""
    doc = spec.get('oracle') if isinstance(spec, dict) else None
    if not isinstance(doc, dict):
        return True, {'reason': 'no oracle block frozen (advisory)'}
```

Plan wording (`plans/round-49-claims.md`): the frozen oracle "resolves and … its sha256/version match" — not advisory. `C1S139Reopen` D1 ran the draft import on six specs (stdout sha `6c7c0905…`, exit 0): `{}` → True; `{"oracle": None}` → True; `{"oracle": {}}` → False; wrong sha and wrong version → False. A spec with the block removed therefore passes this binding without resolving `/usr/bin/unsquashfs`. I read the code lines; I did not run the import. Fold: an absent oracle block should be false in the frozen spec, since `carriers.json` already carries the block.

## 7. Registry convention (decision for L1, not applied)

- `used-by` is defined as "knowledge entries **or lessons** citing the row" (`CORPUS.md` SOURCES field list).
- Lessons citing S138/S139 but not listed in their `used-by`: `corpus/lessons/round-44.md` (Gate row S138 and S139), `corpus/lessons/round-44-verifier-spotcheck.md`, `corpus/lessons/round-45.md` (S138 correction). `S001`-style rows list lessons, so the omission is inconsistent with the rest of the registry.
- The counter only requires the knowledge entry, so this does not block the freeze. Options: (a) append only the entry (what I drafted, per instruction); (b) also append the lesson paths (requires them to exist at the landing commit, and the round-49 lesson will exist then). Choosing (b) would need the same-commit rule to cover the lesson. L1's call.

## 8. Mutable pages (for the Gate reader)

S139 releases page: 398943 B / `d08749f4…` (row, round-44 fetch); 361752 B / `f60447fa…` (`C1S139Reopen`, 21:07:48Z). Tag page: 159465 B / `ecb8bf47…` (R5, 21:08Z); 159470 B / `75e940e4…` (`C1S139Reopen`). S138 tree page: 200946 B / `d37b6c45…` and 200958 B / `d85bed79…` (`C1S138Reopen` F1). The rows' own rationale says page digests are fetch records, not pins. The Gate follows that.

## 9. Peer report status (read at 21:13–21:14Z)

- `w1/C1S138Reopen.md`: verdict "re-opened, pins hold"; manifest `06a72dd5…` confirmed; 22 members mismatch 0; entry digest `4bc53dbb…` flagged; top page does not ground `teaches`. Agrees with my findings F4 and §3.
- `w1/C1S139Reopen.md`: verdict "re-open holds"; release identity, tag, `unsquashfs` pin, page-digest movement; D1 (`oracle_tool_ok`) — §6. Agrees with my R1–R7.
- The seat directories `C1S138Reopen/` and `C1S139Reopen/` carry their own receipts; I did not re-read them beyond their `.md` reports and the cited rows.

## 10. Commands, exit codes, and what was not run

| step | command (abridged) | exit |
|---|---|---|
| row extraction | `awk -F'|' '/^\| *S13[89] *\|/ …' corpus/SOURCES.md` | 0 |
| scratch copy | `cp corpus/SOURCES.md …/SOURCES.base.md` (registry read only) | 0 |
| scratch edit | `_edit` on the scratch copy only (lines 144–145) | — |
| verify edit | `diff SOURCES.base.md SOURCES.edit.md` | 1 (expected: differs) |
| cell diff | awk FNR-keyed compare | 0 |
| census | `census-run.sh` (V0/V1/V2 + opened column) | 0 |
| counter binding replica | python3 heredoc | 0 |
| re-open | curl ×13 (R1–R13) | 0 each |
| checks | `grep -F -c`, `sha256sum`, `git show -s`, `git show … \| sha256sum`, `git ls-tree`, `git merge-base --is-ancestor`, `git branch --contains`, `git status --porcelain` (read-only) | 0 (`git merge-base --is-ancestor` = 0, ancestor) |

Installs: none. Host `curl`, `python3`, `awk`, `git` (read-only) were used.

Not run: `c1-run.sh` (any mode); `c1-counter.py` full score; `c2-mismatch.py`; any registry write; any lane file write; the 22-member re-digest (`C1S138Reopen` did it); the peer's `oracle_tool_ok` import (cited, not repeated).

Scratch `/fast/scratch/hyaku/kaidoku-r49/C1ScribeSources` removed after the receipts were copied (see §11).

## 11. Artifacts (all under `w1/C1ScribeSources/`)

- `lesson-gate-rows-S138-S139.md` — Gate rows (draft, not landed)
- `registry-S138-S139-landing.md` — old → new `used-by` and the same-commit constraint
- `registry-rows-S138-S139.edited.md` (sha256 `1b5eac5d…fbf4`) and `registry-S138-S139.diff` (sha256 `082a457c…ccdc`)
- `census-run.txt` (sha256 `dc9683df…a02c`)
- `receipts/` (13 files + `SHA256SUMS`; `sha256sum -c` exit 0)
- `SHA256SUMS-artifacts.txt`; `census-run.sh` (the V0/V1/V2 script; its scratch paths were removed after the run); `counter-binding-replica.py` + `.out` (sha256 `5e5d804c…81ec`; the python replica of `c1-counter.py` lines 2172–2184, exit 0)

## 12. Fold-in list for L1 (pre-freeze)

1. Fix F8 in the counter before the freeze (absent `oracle` block → False). Frozen-file edit now, not after.
2. Strip the round-44 pre-fill in the entry status (F5); the landing text cites only the post-freeze receipt.
3. Replace the S138 manifest digest in the entry (F4): `4bc53dbb…` → `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`.
4. Land the registry edit (§1) in the same commit as the entry.
5. Adopt the Gate rows (§3); cite the round-49 re-opens, not the round-44 times (F7).
6. Decide the `used-by` lesson-citer convention (§7).
7. Fix the "Round 44 adds" wording (F6).
