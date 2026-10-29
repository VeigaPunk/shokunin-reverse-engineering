# C1OracleBuild — round 50 wave 1 (pre-freeze) — independent oracle for the four LE AVM carriers

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Seat dir: `.ufo/waves/round-50/w1/C1OracleBuild/`. Run 2026-10-28 (UTC 23:32–23:37). Scratch `/fast/scratch/hyaku/kaidoku-r50/C1OracleBuild` (removed after copying receipts). No `--data-run`, no lane write outside the seat dir, no vendor bytes copied.

## Verdict

**Oracle built; all four carriers are genuine LE AVM `hsqs` v4.0 xz, `mkfs_time == bytes_used`. The four primary readers agree exactly (0 disagreements on 35,388 regular files in total: path, size, sha256; every non-regular entry).** Residue is (a) the unprivileged device-node failure of `unsquashfs` on the two cables (1 `char-device dev/led 247:0`), and (b) `7z x` extract artefacts (advisory reader, not scored).

**One plan defect (must be fixed before the freeze): the cable carriers' member is NOT `./var/tmp/filesystem.image`.** `FRITZ.Box_6490_Cable-07.57.image` and `FRITZ.Box_6430_Cable-07.30.image` have no such member. They carry two rootfs members each: `./var/remote/var/tmp/x86/filesystem.image` = LE `hsqs` (the 28 MB / 23.9 MB the plan's table names) and `./var/remote/var/tmp/filesystem.image` = BE `sqsh` v4.0 xz (5.4 MB / 6.0 MB, also `mkfs_time == bytes_used`, i.e. an AVM-BE member in the same tar). `carriers.json` must pin `member` = the `x86` path, and the C1 counter's chunk/carrier mapping must not be fooled by the second (BE) member of the same image (round-41 `fetch-vendor.py` selects by literal `member`, so the pin handles it; an REA run on the whole `.image` tar would see both).

## Carrier chain (pin material; `chain.json`)

| id | image url (download.avm.de/fritzbox/…) | image size | image sha256 | tar member | member size | member sha256 |
|---|---|---|---|---|---|---|
| a7530 | fritzbox-7530/deutschland/fritz.os/FRITZ.Box_7530-08.25.image | 41,850,880 | `b17fe5cd0bd3faa713dd92513cb3a65c23e61f5f23366c343b78674955d35e9c` (= plan) | `./var/tmp/filesystem.image` | 34,005,000 | `df6c22ddd009870404375aff606853c9d5171580437b6aae193114d2040c6e56` |
| a7590 | fritzbox-7590/…/FRITZ.Box_7590-08.25.image | 42,393,600 | `267ef427337d2141736ad6ed5d9389722a6a1234dd590bb7d4ebf11a00616c0d` | `./var/tmp/filesystem.image` | 35,835,912 | `05ba6ac992f77076cd72d97ed98ab7612f3cc6969f6bbf736515537a9373c3dc` |
| c6490 | fritzbox-6490-cable/…/FRITZ.Box_6490_Cable-07.57.image | 39,741,440 | `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d` | `./var/remote/var/tmp/x86/filesystem.image` | 28,200,968 | `7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419` |
| c6430 | fritzbox-6430-cable/…/FRITZ.Box_6430_Cable-07.30.image | 35,911,680 | `52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815` | `./var/remote/var/tmp/x86/filesystem.image` | 23,863,304 | `25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c` |

Fetch: `curl -sS -f -L -o <id>.image <url>` (headers discarded, no cookies), all exit 0, 14–31 s wall in parallel. Member extraction: `tar -xOf <id>.image <member> > fs.image`. The BE sibling member of c6490 (`./var/remote/var/tmp/filesystem.image`) has sha256 `334e56df…f3d4` (full: `334e56dfba6a785590bb5cdbd78fcb5be183b9af160b51fc8935a3015ad3f3d4`); the c6430 BE sibling hash was not taken.

Superblock (python `struct`, member bytes): all four `hsqs`, v4.0, comp 4 (xz), block size 65536, `mkfs_time == bytes_used` (34003969 / 35834769 / 28200029 / 23861507); inodes 15150 / 15151 / 5624 / 4780. `7z l -slt` additionally shows `Created = 1970-11-23 …` (mkfs_time read as a date — the marker is visible there too) and `Tail Size = 8` on c6490.

## Census per carrier (`<id>/oracle-summary.json`)

| | a7530 | a7590 | c6490 | c6430 |
|---|---|---|---|---|
| regular files | 13,366 | 13,358 | 4,709 | 3,955 |
| regular bytes | 172,089,096 | 189,853,641 | 93,857,626 | 77,587,772 |
| zero-size regular | 66 | 67 | 8 | 13 |
| unique sha256 | 4,473 | 4,517 | 3,234 | 2,498 |
| dirs (root excluded) | 926 | 932 | 300 | 255 |
| symlinks | 857 | 860 | 613 | 568 |
| absolute-target symlinks | 238 | 239 | 54 | 58 |
| …whose target is absent in-image (lexical) | 65 | 65 | 22 | 22 |
| relative symlinks escaping the root (lexical `..`) | 0 | 0 | 0 | 0 |
| empty-target symlinks | 0 | 0 | 0 | 0 |
| char/block devices | 0 | 0 | 1 (`dev/led` 247:0) | 1 (`dev/led` 247:0) |
| fifo/socket, setuid/setgid | 0 | 0 | 0 | 0 |
| case-colliding path pairs | 1 (`etc/init.d/e40-dsl` vs `E40-dsl`) | 1 | 0 | 1 |
| odd names | 1 with a space (`etc/internal_memory_default_de/Videos/FRITZ! Clips.html`), no tab/newline/CR/backslash/leading-dash/non-UTF-8 | same | same | same |

Inode check: files+dirs+symlinks(+devices)+root = superblock inode count for every carrier (15150 = 13366+926+857+1 for a7530). Counts are identical between `unsquashfs -lls`, the extract tree, `sqfs-list.py` and `7z l`.

No symlink escapes the root *relatively*. 238/239/54/58 symlinks carry **absolute** targets (`/var/…`, `/usr/…`, `/dev/null`, …) — "escaping" for any extractor that follows links against the host; 65/65/22/22 of them have no in-image target (runtime paths such as `/var/tmp/providers`). Write-side safety is the extractor's business (see unblob below).

## Reader comparison (exact commands: `<id>/times.json` carries argv, exit, stdout sha256, UTC, wall; driver `tools/round-50/oracle-build.py`)

| reader | command (member = `fs.image`) | exit a7530/a7590/c6490/c6430 | wall s (4 carriers run in parallel on 32 threads) |
|---|---|---|---|
| unsquashfs extract | `unsquashfs -d <ex> -f fs.image` | 0/0/**2**/**2** | 0.18–0.38 |
| unsquashfs list | `unsquashfs -lls fs.image` | 0/0/0/0 | 0.02–0.07 |
| lane pure-Python | `python3 -I tools/round-41/sqfs-list.py --layout auto --files F --nonregular N fs.image` | 0/0/0/0 | 2.1–5.8 |
| lane pure-Python | same with `--layout le` | 0/0/0/0 | 2.1–5.6 |
| 7z list | `7z l -slt fs.image` | 0/0/0/0 | 0.01–0.04 |
| 7z extract | `7z x -snl -y -o<ex> fs.image` | **2**×4 | 0.9–2.1 |
| unblob | `unblob -d 1 -e <out> -f fs.image` | 0×4 | 1–2 |

Cable `unsquashfs` exit 2: `create_inode: could not create character device …/dev/led, because you're not superuser!` — the one device; every other entry (4709 files, 613 symlinks) extracted, tree complete (counts above). `7z x` exit 2: `ERROR: Dangerous link path was ignored` (3 listed in stderr tail; 96/96/93/94 links demoted to 0-byte regular files, and on the cables `dev/led` extracted as a 0-byte regular file).

**Cross-reader results** (`<id>/disagreements.json`, `<id>/disagreement-totals.json`):
- Regular files: `unsquashfs` extract-tree vs `-lls` vs `sqfs-list auto` vs `sqfs-list le` vs `7z l`: **identical path set and size on all four**; sha256 identical between the extract tree and both `sqfs-list` layouts (`auto` and `le` TSVs byte-identical for a7530). No only-in-one, no size, no sha mismatch.
- Non-regular (kind + symlink target + device major:minor): `-lls` vs extract-tree vs `sqfs-list auto`/`le` vs `7z l` (kind only): identical except cables' extract-tree lacking `dev/led` (unprivileged; `-lls` and `sqfs-list` both say `char-device 247:0`).
- `7z x` residue (advisory, 18/18/10/14 diffs after demotion bookkeeping): 7z collapses `/./x` and `//x` in absolute link targets and rewrites absolute targets under its output dir. Not scored.
- Primary disagreement totals: a7530 0, a7590 0, c6490 1 (device), c6430 1 (device). a7530/a7590 `disagreements.json` are byte-identical (same 7z residue samples) — expected, same tree shape.

## unblob 26.6.4 cross-check (beyond the brief; `unblob-receipts/`, `<id>/unblob-vs-oracle.json`)

`unblob -d 1` on each member, host `sasquatch` 4.5.1: handler **`squashfs_v4_le`** found for chunk `0x0–0x206e000` (34,004,992 B; the squashfs rounded up to 1 KiB), command `sasquatch -le -no-exit-code -f -d …`, exit 0 on all four. Each member also yields one **`.unknown` chunk of exactly 8 bytes** (`34004992-34005000.unknown`, `35835904-35835912`, `28200960-28200968`, `23863296-23863304`; the c6490 log lost its debug records — only the summary table survived: SQUASHFS_V4_LE 100% + UNKNOWN 8 B — so the handler/command lines are read from the other three logs) — a chunk that is "unknown" is not a failed chunk; the plan's "no failed chunk" clause must not count it. The 8-byte tail equals `member_size − chunk_end`.
- Files: unblob tree vs oracle: **0 missing, 0 extra, 0 differing (path/size/sha256)** on all four. Dirs: all present.
- Symlinks: unblob **removed** 5/5/1/1 symlinks (`MaliciousSymlinkRemoved` WARNING in the log): a7530/a7590 `lib/libbroadbandcfg.so`, `lib/libbroadbandcfg.so.1` (link-to-link chain), `usr/www/{1und1,avm,avme}/cgi-bin/system_status` → `/usr/www/cgi-bin/system_status`; cables `usr/www/avm/cgi-bin/system_status`. Every removed link's own target is itself a symlink (chain). unblob also **rewrites targets**: 281/282/93/91 surviving symlinks have a target different from the stored one (≈ 235/…/53 are absolute→relative rewrites like `/usr/share/zoneinfo/…` → `../../usr/share/zoneinfo/…`; the rest are `./x`→`x` and link-to-link collapse, e.g. `libncurses.so`→`libncurses.so.6` became `libncurses.so.6.1`). So a counter cannot demand symlink-target equality against the raw oracle; it needs the round-41 three-family disposition (device gap / removal / rewrite) with the removed set above as the expected-removal evidence, or a path-only symlink presence rule plus the removal list.
- Devices: unblob creates none (`dev/led` absent from the cables' tree) — a "gap" family entry.
- unblob prints a logging `PermissionError` on `unblob.log` in its cwd under its sandbox (exit still 0): noise, not a failure.

## Files

`<id>/oracle.tsv` (relpath TAB sha256 TAB size, bytewise-sorted, verified `sorted`; all ≤ 1.6 MB so not gzip'd), `<id>/nonregular.tsv` (relpath TAB kind TAB detail; from `-lls`, raw stored targets, devices `major:minor`), `<id>/oracle-summary.json`, `<id>/disagreements.json`, `<id>/times.json`, `<id>/unblob-vs-oracle.json`, `chain.json`, `unblob-receipts/*`, `tools/round-50/oracle-build.py` (draft driver: `oracle-build.py ID MEMBER WORK OUTDIR`; exit 0 agree / 1 disagree / 2 cannot evaluate), `tools/round-50/ub-compare.py` (unblob tree vs oracle). Receipt sha256 (oracle.tsv / nonregular.tsv): in `chain.json` per carrier (a7530 `20c62eaa…`/`fd3fb9ad…`, a7590 `dde2dd3f…`/`154d6c09…`, c6490 `d4f660aa…`/`74f17174…`, c6430 `f657ef51…`/`cb691b44…`).

## Findings table

| # | finding | evidence | action for L1 |
|---|---|---|---|
| F1 | Cable carriers' member path wrong in plan (`./var/tmp/…` absent); two rootfs members per cable image (LE x86 + BE) | tar listing / `chain.json` | pin `./var/remote/var/tmp/x86/filesystem.image`; decide if the BE sibling is out of scope (a second BE AVM member in the same image) |
| F2 | 4 readers agree exactly on all regular files and non-regular entries | `disagreements.json` primary = 0/0/1/1 (device only) | oracle is stable; use `oracle.tsv`/`nonregular.tsv` |
| F3 | unprivileged `unsquashfs` exit 2 on cables because of `dev/led` (247:0); tree otherwise complete | `times.json` | the counter's oracle must come from `-lls`/`sqfs-list`, not exit codes of the extract |
| F4 | unblob rewrites/removes symlinks (5/5/1/1 removed, ~90–280 retargeted) and creates no device | `unblob-vs-oracle.json` | symlink clause = disposition rule, never raw-target equality |
| F5 | unblob emits an 8-byte `.unknown` tail chunk beside each valid chunk | `unblob-receipts/*.log` | "no failed chunk" must ignore unknown tail chunks (check REA's chunk statuses) |
| F6 | 66/67/8/13 zero-size regular files; sha `e3b0c442…` is the most frequent after the 170× duplicate | oracle.tsv | none; hash dedup by REA may collapse duplicates — compare per path |
| F7 | case-colliding pairs (`e40-dsl`/`E40-dsl`) on a7530/a7590/c6430; a space in one name | summary | fine on Linux; reject case-folding comparisons |
| F8 | 65/65/22/22 absolute symlinks have no in-image target; 0 relative escapes; 0 empty targets | summary | none |

Not run: REA `extract-firmware` (other seats); the BE sibling members were not census'd; hard links not separately enumerated (unsquashfs reports `created 0 hardlinks` for a7530; not captured for others); wall times are from a parallel run (contended), not isolated.
