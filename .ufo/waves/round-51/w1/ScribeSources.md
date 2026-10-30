# ScribeSources — round 51, wave 1: the two SOURCES rows (S250 device-node path, S251 padding option)

**Verdict: DONE — two rows drafted (S250, S251), every anchor located against today's fetched
bytes, the block validates clean on a scratch registry mirror (`sources-census.sh validate
--file <mirror>` exit 0, `E=0`, `W04=19` unchanged from the baseline), and the diff is 3 added
lines / 0 changed / 0 removed.** The draft is at `.ufo/waves/round-51/w1/ScribeSources/rows.md`;
it is **not** applied to the lane tree. No REA run, no data run, no `--data-run`, no vendor
firmware byte fetched, no git mutation, no tool installed.

**The one finding the L1 must not skip (F1):** the upstream option is spelled **`-nopad`** with
no hyphen — `grep -c -- 'no-pad'` is **0** in every upstream body opened today (tags `3.1`,
`4.4`, `4.5.1`, `4.6.1`, `4.7`, `4.7.4`, `4.7.5`, master, master-HEAD-pin, and the sasquatch
fork). The claims file's "`-no-pad` / padding source row" (`plans/round-51-claims.md:189`) and
`SKILL.md` block 26's "no-pad" are the **lane's own prose**, not an upstream option name. If the
C2 rule block cites "the `-no-pad` option" as upstream text, it cites a name that does not exist
upstream; the row's anchor quotes the real spelling and the real help line.

## Deliverable

| file | what it is |
|---|---|
| `.ufo/waves/round-51/w1/ScribeSources/rows.md` | the two rows, the `## Gate` quote records, the `## Search log` entry, the landing constraints and the non-claims (sha256 `e194c31b29de709ffa4363bf4653f6017132ada8454f37ffd6cd00995966f6c1`) |
| `…/ScribeSources/rows_template.md` | the same file with the generated cells as `@@…@@` placeholders (the generator's input) |
| `…/ScribeSources/fetch-sources.sh`, `fetch-tags.sh` | the two fetch drivers (exact URL → UTC → HTTP status → bytes → sha256 → curl exit) |
| `…/ScribeSources/quote-check.py`, `quote-check.out.txt` | the anchor locator: `QUOTE_CHECK located=46 missing=0`, exit 0, with a negative control that must be absent |
| `…/ScribeSources/build-rows.py`, `build.log` | the row builder: 11-column/pipe/enum/length assertions, id-uniqueness check, the scratch mirror, the census proof (last line `BUILD OK`) |
| `…/ScribeSources/receipts/receipts.tsv` | the two **named** master-URL fetches |
| `…/ScribeSources/receipts/receipts-tags.tsv` | 20 tag-pinned / HEAD-pin / companion-file fetches |
| `…/ScribeSources/receipts/receipts-sasquatch.tsv` | 2 sasquatch-fork fetches (1 HTTP 200, 1 HTTP 404) |
| `…/ScribeSources/receipts/refetch.tsv` | 12 re-fetches of the bodies not copied on the first pass, to make every receipt row re-verifiable from the seat dir alone (all 12 digests equal the original receipt) |
| `…/ScribeSources/receipts/census-mirror.txt` | census output on the mirror and on the untouched lane registry |
| `…/ScribeSources/receipts/census-mined-variant.txt` | the `mined`-status variant, with and without the entry placeholder |
| `…/ScribeSources/mirror/corpus/SOURCES.md` | the whole patched registry (base + 2 rows + 1 search-log bullet) |
| `…/ScribeSources/body/` | the fetched source bodies, so every digest and every quote is re-checkable from the seat dir alone |

## The two rows

| id | kind | tier | scope | anchor (condensed) | used-by |
|---|---|---|---|---|---|
| S250 | code | A | the upstream extractor's char/block device-node creation path and its privilege refusal — the node is created only under `root_process`; an unprivileged run reports "not superuser" instead. **Not** REA's gap schema, **not** the sasquatch fork's tree, **not** any carrier's census | tag `4.7.5` = commit `708c59ae…`; sha256 `6222d940…9341` (116,844 B); `:1296` the `mknod`; `:1313`-`:1315` the refusal; `:1328`/`:1349` the fifo/socket `mknod`; `:4459` `root_process = geteuid() == 0;`; `unsquashfs_error.h:44`-`:50` the non-fatal `EXIT_UNSQUASH_STRICT` | `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` |
| S251 | code | A | the producer-side option that suppresses 4K padding, its upstream spelling and the padding logic it gates. **Not** any carrier's bytes, **not** a reader's behaviour, **not** REA's publication | tag `4.7.5`; `mksquashfs.c` sha256 `509241bb…7e2` `:7113` the parse, `:596`/`:7491`/`:8946` the padding writes, `:5964` the superblock offset; `mksquashfs_help.c` sha256 `9136f6e6…ac2` `:467` the help line; the v3-era producer at tag `3.1` carries the same name and help text | `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`, `SKILL.md` |

Both rows are `status queued`, `opened 2026-10-30`, `recheck on-release`. `S250`/`S251` are free
ids — the registry ends at **S249** with 156 rows; `S150`-`S242` stay skipped (earlier lessons
cite them as refused staged rows).

## Findings

| # | finding | evidence (command → exit; value) | action for the L1 |
|---|---|---|---|
| F1 | **The upstream option is `-nopad`, not `-no-pad`.** The claims file (`plans/round-51-claims.md:189`) and `SKILL.md` block 26 both write "`-no-pad`". No upstream body contains that string. | `grep -c -- 'no-pad'` over every fetched upstream body → **0** in all 9 upstream `mksquashfs.c` (tags `3.1`, `4.4`, `4.5.1`, `4.6.1`, `4.7`, `4.7.4`, `4.7.5`, master, master-HEAD-pin) and **0** in the sasquatch fork's `mksquashfs.c`; the same files hold 5–10 `nopad` hits each. The real help line is `mksquashfs_help.c:467` `"-nopad\t\t\tdo not pad filesystem to a multiple of 4K\n",`. | word the C2 block's citation with the upstream spelling (`-nopad`), or cite the lane's own "no-pad" as prose and say so. The row's scope cell already states the spelling explicitly. |
| F2 | **The device-node refusal is *silent by construction*, and the source says exactly why — but only for char/block devices.** `mknod` for a device runs only inside `if(root_process)`; the unprivileged branch calls `EXIT_UNSQUASH_STRICT("...not superuser!")` and `goto failed`, which **marks the inode created-but-missing** and returns FALSE. `EXIT_UNSQUASH_STRICT` degrades to a non-fatal `ERROR` unless `-strict-errors` is passed (`strict_errors = FALSE` by default), and `ERROR` prints without exiting while `BAD_ERROR` calls `exit(1)`. The exit code is `(failed == TRUE \|\| res == TRUE) && set_exit_code ? 2 : 0`, and the caller's argv passes `-no-exit-code` (S108), so `set_exit_code` is FALSE and the run exits 0. That is the whole mechanism of the round-51 law's "no disposition at all". | `unsquashfs-4.7.5.c:1287` `if(root_process) {`; `:1312`-`:1316`; `:1373`-`:1386` the `failed:` label; `:86` `int strict_errors = FALSE;`; `:92` `int set_exit_code = TRUE;`; `:3463` the exit-code return; `:3934`-`:3936` the `-no-exit-code` parse; `unsquashfs_error.h:44`-`:50` the `EXIT_UNSQUASH_STRICT` macro; `error.h:42`-`:45` (`ERROR`, no exit) and `:56`-`:61` (`BAD_ERROR` → `exit(1)`). | cite S250 for the mechanism, but keep the "no gap record" half attributed to the **round-50 receipts**, not to this row — the row is upstream extractor source, not REA's schema. |
| F3 | **The fifo and socket branches are NOT root-gated** — they attempt `mknod` unconditionally and only `ERROR` on failure. They are therefore a *different* mechanism from the device path, and the law must not fold them in. | `unsquashfs-4.7.5.c:1328` `res = mknod(pathname, S_IFIFO, 0);` and `:1349` `res = mknod(pathname, S_IFSOCK, 0);`, both outside any `root_process` test; the fork has the same at `:1288`/`:1306` | the v2 rule's `fifo`/`socket` allowances must not be justified by "an unprivileged extraction cannot `mknod`" — that claim is false for those two kinds. |
| F4 | **The carriers do not exercise the fifo/socket branches at all.** The four frozen oracle tables carry kinds `char-device`, `dir`, `symlink` only — **28** char-devices (1 + 1 + 13 + 13), **0** fifos, **0** sockets. | `cut -f2` over `tools/round-50/oracle/*.nonregular.tsv` → `char-device`/`dir`/`symlink`; `awk '$2=="char-device"' \| wc -l` → 28; `grep -cE "fifo\|socket"` matches only *symlink rows whose target* contains `mkfifo`/`wl_server_socket` (4 hits), never a `kind` cell. | the v2 rule's fifo/socket handling is unexercised by the four carriers — keep it, but the law must not claim four-carrier evidence for it. |
| F5 | **The round-50 receipts confirm the device rows carry no disposition** — and the round-50 rule's `247:0` singleton is *not* a property of the producer. All four `unpublished_entries` lists contain **only** `symlink` entries (636 / 636 / 567 / 612 for g7581 / g7582 / c6430 / c6490); there is **no** char-device entry anywhere, including `dev/led 247:0` on the Cable class. So `dev/led` is absent by the same producer mechanism as the other twelve — the singleton whitelist had no producer-side basis. | `python3` over `corpus/evidence/round-50/c1/<id>/after.json` → `normalized_result.unpublished_entries` kind counters: `{'symlink': 636}` / `{'symlink': 636}` / `{'symlink': 567}` / `{'symlink': 612}`; zero char-device entries; `tools/round-50/gap-rule.json` `removed.silent.char-device: ["247:0"]`. | this is the strongest available support for the law's shape: the absence is uniform across the two classes, which is what the per-carrier-class derivation should encode. It also means the round-50 rule's `247:0` allowance was a rule-side artefact, not a producer-side one — the L1 should say so explicitly in the freeze's amendment record. |
| F6 | **Master moved; the row pins the tag, not the moving branch.** `master` HEAD is `db038ef265ed00bb17aaf695a72f9b0c3489eb20` and the master bodies differ from tag `4.7.5` (2,172 changed lines in `unsquashfs.c`). The host oracle is `unsquashfs version 4.7.5 (2026/03/01)` at `/usr/bin/unsquashfs`, so the row pins **tag `4.7.5`** (peeled commit `708c59ae…`, per `git ls-remote --tags`). Master is recorded as a re-open with its own digest; the located line numbers in the master bodies are `:1373`/`:1390`/`:1405`/`:1426`/`:5381`. | `git ls-remote --tags` → `refs/tags/4.7.5` = `1fdc2fe0…`, peeled `708c59ae…`; `git ls-remote HEAD` → `db038ef2…`; `diff unsquashfs-4.7.5.c unsquashfs-master.c \| grep -c '^[<>]'` → 2172; `unsquashfs -version` → `4.7.5 (2026/03/01)`. Receipts for both refs (HTTP 200, 143,650 B / 116,844 B). | none — the pin is recorded in the anchor cell. |
| F7 | **The sasquatch fork the lane actually ran has the same structure**, so the upstream row is transferable — and the fork's copy is already committed in the lane. | lane copies `.ufo/waves/round-39/w2/artifacts/R39W2C2TableReview/unsquashfs.c` and `.ufo/waves/round-41/w2/artifacts/R41W2C1Docs/verification-copies/unsquashfs.c`, both sha256 `ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40` (the same digest S121 records), with `if(root_process)` at `:1247`, `mknod` at `:1256`, the refusal at `:1273`-`:1275`, fifo `:1288`, socket `:1306`, `root_process = geteuid() == 0;` at `:4460`. The installed `~/.local/bin/sasquatch` (sha256 `ad02d27a…`) carries the string `create_inode: could not create %s device %s, because you're not superuser!`. | the row's anchor cites the fork's line numbers so the L1 can cite the operative tree, not only upstream. |
| F8 | **The v3-era producer is the one that could have written the lane's ddwrt body.** The lane's `squashfs_v3.be.nopad.bin` fixture is 320 B and is a **v3** image; upstream `mksquashfs` at `4.7.5` writes v4.0 (`squashfs_fs.h:28`-`:29`), so the v3 producer is tag `3.1` (`squashfs_fs.h:27`-`:28`) — and it carries the same `-nopad` name and the same help text (`mksquashfs.c:1914`, `:1973`, `:2248`). | `squashfs_fs.h-4.7.5` `SQUASHFS_MAJOR 4` / `SQUASHFS_MINOR 0`; `squashfs_fs.h-3.1` `SQUASHFS_MAJOR 3`; `mksquashfs-3.1.c:1914` `} else if(strcmp(argv[i], "-nopad") == 0)` and `:1973` the help line; `tools/round-42/fixtures.json` `v3ddwrt-be` size 320. | the row is scoped to the option and its padding logic, **not** to the provenance of any body. If C2's rule needs "this body was made with `-nopad`", that is a separate, unproven claim — do not let the row carry it. |
| F9 | **Every anchor is mechanically located; the checker has a negative control.** | `python3 -I -B quote-check.py` → `QUOTE_CHECK located=46 missing=0`, exit 0 — 43 contiguous literal quotes at their exact lines plus 3 `composite` (C-string-literal) reconstructions; the control (a deliberately wrong `mknod` spelling at `unsquashfs-4.7.5.c:1296`) reports `CONTROL-OK`. | none — the checker ships with the receipts. |
| F10 | **The block is registry-clean and append-only.** | `sources-census.sh validate --file <mirror>` → **exit 0**, `E=0`, `W04=19` (identical to the baseline's 19); `sources-census.sh validate kaidoku-shokunin` on the untouched lane → **exit 0**, 19 findings, all `W04`; `diff` vs the base registry → **added=3 removed=0** (two rows + one search-log bullet; no existing row edited). `grep -c 'raw.githubusercontent.com/plougher' corpus/SOURCES.md` → 0, so neither new URL can raise a `W04` or an `E04`. | none. |
| F11 | **The `mined` flip is the E11 risk: the entry and the rows must land in one commit.** | On the mirror, the block with `status mined` and the entry present → **exit 0** (`receipts/census-mined-variant.txt`); with the entry removed → **exit 1** with exactly **two** `E11` lines, one per new row, both naming `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`. With `status queued` the block is already clean (exit 0) because the census's E11 rule only inspects `mined` rows (`sources-census.sh:559`). | land the entry file and both rows in the **same** commit, and flip both to `mined` in it. A rows-only landing makes the registry red. |
| F12 | **The counter v2's `sourced` binding needs the ENTRY's `source:` lines to name the row ids** — a registry row cannot fix this. | `tools/round-51/w1/ExecCounterV2/c1-counter.py:2469` — `if c[0] in src_ids and c[8] in OPENED_DATES and (ENTRY in used or STEM in used)`; `src_ids` comes from the entry's `source:` lines (`:2453`-`:2458`); `OPENED_DATES = ('2026-10-30',)` (`:393`); `ENTRY`/`STEM` = `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` / `2026-10-30-r51-avm-le-squashfs-core` (`:377`-`:378`). The entry draft's `source:` lines 9 and 10 are still `PLACEHOLDER`s naming no row id. | fill the entry's two `source:` placeholders with S250 and S251 (id, URL, access date, located quote, sha256 — all five are in `rows.md`), or the `sourced` binding stays red for a reason no registry row can fix. |
| F13 | **S251's `used-by` names both consumers, so the entry's placeholder can be filled either way.** | The entry draft's line 10 says the padding row is "included here only if the L1 lands it as a shared round-51 row whose `used-by` cell names this entry as well as R51-C2's rule block". S251's `used-by` is `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md, SKILL.md` — both names present; `SKILL.md` exists on disk today. | none — but if the L1 prefers a C2-only row, drop the entry from S251's `used-by` and remove the entry's line-10 placeholder. |
| F14 | **Two upstream paths 404'd** — the man pages are not at those paths. | `mksquashfs.1` and `unsquashfs.1` under `squashfs-tools/` at tag `4.7.5` → **HTTP 404**, 14 B, sha256 `d5558cd4…12ed` (the GitHub 404 body); recorded in `receipts/receipts-tags.tsv`. The option text is in `mksquashfs_help.c`, not a man page, so the row's anchor is unaffected. | none — recorded for honesty; no quote depends on a 404 body. |
| F15 | **No rejection row is warranted.** Both named URLs opened at HTTP 200 with located, contiguous quotes and a digest that survives a re-fetch at two refs. | `receipts/receipts.tsv`: the two named master URLs, HTTP 200, 143,650 B / 266,790 B, sha256 `bd2a6abd…b24f` / `205f58e6…2bc5c`, curl exit 0; the tag and HEAD-pin re-fetches are byte-identical to the master bodies at the same refs. | none — both rows are admitted; the search log records 2 identified / 2 screened / 2 included / 0 excluded. |

## Commands, exits and digests

| # | command | exit | result |
|---|---|---|---|
| R1 | `bash fetch-sources.sh` (the two named master URLs) | 0 | 2 fetches, HTTP 200, curl exit 0 each, 2026-10-30T04:57:51Z–04:57:52Z |
| R2 | `bash fetch-tags.sh` (tag `4.7.5`, master HEAD pin, companion files, older tags) + the companion-file and older-tag fetches | 0 | 20 fetches, HTTP 200 except two 404 man pages (F14), curl exit 0 each |
| R3 | `python3 -I -B quote-check.py` | 0 | `QUOTE_CHECK located=46 missing=0`; `CONTROL-OK` on the negative control |
| R4 | `python3 -I -B build-rows.py` | 0 | grammar assertions pass (11 cells, no `|`, enums, ids free); mirror written (sha256 `570a12dd…8cb`); census **exit 0**, `E=0`, `W04=19`; `diff` added=3 removed=0; `BUILD OK` |
| R5 | `sources-census.sh validate --file <mirror>` | 0 | 19 `W04` (the baseline's 19), final line `file ok <mirror>/corpus/SOURCES.md` |
| R6 | `sources-census.sh validate kaidoku-shokunin` (the untouched lane registry) | 0 | 19 findings, all `W04`; `kaidoku-shokunin ok …/corpus/SOURCES.md` |
| R7 | same census on the mirror with the entry placeholder removed, `status mined` | **1** | exactly 2 `E11` lines (S250, S251) naming the not-yet-landed entry; nothing else red (F11) |
| R8 | `grep -c -- 'no-pad'` over every fetched upstream body | 1 (no hits) | 0 in all 9 upstream `mksquashfs.c` and 0 in the sasquatch fork; `nopad` hits 5–10 each (F1) |
| R9 | `git ls-remote --tags / HEAD https://github.com/plougher/squashfs-tools` | 0 | `refs/tags/4.7.5` = `1fdc2fe0…` peeled `708c59ae…`; `HEAD` = `db038ef2…` (F6) |
| R10 | `sha256sum` of each copied body in the seat dir vs the receipt digests | 0 | all **36** receipt rows (24 original + 12 re-fetch) match their body's sha256 exactly — every receipt is re-verifiable from the seat dir alone |
| R12 | `python3 -I -B quote-check.py` and `python3 -I -B build-rows.py` re-run from the **seat dir** with the scratch removed | 0 / 0 | `QUOTE_CHECK located=46 missing=0` and `BUILD OK` (mirror sha256 `570a12dd…8cb`, census exit 0, `E=0`, `W04=19`, diff added=3 removed=0) — both scripts are self-locating and need no scratch |
| R11 | secret scan of the whole seat dir for `set-cookie` / `authorization` / `api_key` / `token=` | 1 (only prose) | the only hits are my own "no `Set-Cookie` was saved" sentence and the word "authorization" inside an existing SOURCES row the mirror carries; the fetch driver keeps only `content-type`/`content-length`/`last-modified`/`etag` and deletes the raw header file |

## Not run / limits

- **No REA run, no counter run, no data run, no `--data-run`.** This wave is build-only; the L1
  runs the REA-dependent controls and the C1 data run in its own quiet window.
- **No vendor firmware byte was fetched.** Only upstream source files went over the network, into
  the seat scratch and then the seat dir. The AVM carrier images were never touched.
- **`S250` is upstream squashfs-tools source, not the operative extractor.** The operative binary
  is the sasquatch fork; the row's anchor cites the fork's line numbers too (F7), but the row's
  *source* cell is the upstream URL, and the row does not claim to be the fork's own tree (S121's
  scope). The L1 should decide whether the entry cites this row for the mechanism or also names
  S121 for the fork.
- **The row does not establish that REA emits no gap record.** That is REA's envelope schema
  (S119) plus the round-50 receipts (F5). This row establishes the producer-side mechanism only.
- **No claim about fifos or sockets being omitted** (F3, F4), and no claim about the ddwrt body's
  provenance (F8).
- **Not claimed:** that the upstream option is named `-no-pad` (F1); that the four carriers
  exercise the fifo/socket branches (F4); that the ddwrt body was produced with `-nopad` (F8).
- The `## Gate` rows and the `## Search log` bullet are **drafts for the L1 to integrate** into
  `corpus/lessons/round-51.md` and `corpus/SOURCES.md`; they are not applied here.
- **The lane's `plans/round-51-claims.md` was already modified by another seat** when I started
  (`git status` shows ` M plans/round-51-claims.md`, mtime 02:18, before my seat's first write).
  I did not touch it. The fleet root has two untracked `count-c*.cover` files (mtime 02:27, also
  not mine). Neither is mine; I wrote only under my seat dir and my scratch.

## Tool installs / updates

**None.** No pacman transaction, no `uv tool`/`npx`/release-binary install, no PATH change, no host
service touched, no `~/.local/bin` write. Used only `curl`, `sha256sum`, `git ls-remote`,
`python3` (standard library), `diff`, `grep`, `awk`, `cut`, `stat` — all already present. (Channel
per `/home/vgpnk/.omp/agent/RULES.md`; the pacman guard was respected: nothing was installed at
all.)

## Scratch

`/fast/scratch/hyaku/kaidoku-r51/w1-ScribeSources` — **removed after** the receipts, the fetched
bodies, the mirror and the scripts were copied into
`.ufo/waves/round-51/w1/ScribeSources/`. `scripts/hyaku/disk-guard.sh status` was run before the
pass (exit 0). Nothing was written under `/tmp`.

## Self-assessment

Accuracy 4/5: every anchor is located in the served bytes and every claim about the source is
backed by a line I read; the residual risk is the upstream-vs-fork attribution the L1 must
settle. Completeness 4/5: both named URLs opened, both anchors located, the block validated, the
Gate and search-log drafts supplied, and the landing constraints measured — but the *row-vs-claim*
wording of the C2 block and the entry's `source:` placeholders are the L1's to write, not mine.
Clarity 4/5: the findings table separates what the source establishes from what the receipts
establish and from what is unproven. Actionability 5/5: each finding names the L1's action.
Conciseness 4/5: the detailed evidence sits in `rows.md` and the receipts, not in this report.
Overall 4.2/5. Highest-impact improvement: F1 — the `-no-pad` spelling — because a rule block
that cites a non-existent upstream option name is exactly the kind of overclaim this lane's
source gate exists to catch. User-alignment check: the two rows, the `## Gate` records, the
search-log entry, the receipts with UTC/status/bytes/sha256, and the ref pin are all delivered;
the lane tree is untouched.
