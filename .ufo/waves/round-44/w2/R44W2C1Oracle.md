# R44W2C1Oracle — independent oracle re-derivation on the four frozen SquashFS v1/v2 carriers

Seat `R44W2C1Oracle`, round 44 wave 2 (falsification). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; freeze `c48f8a4b`; measured revision `55bcce69`;
lane tip at dispatch `c86ea508`; lane HEAD during this seat's work `8bb1090a`.

Scope: the oracle binding the R44-C1 score rests on — re-derive the member census, digests and
compression class of the four frozen carriers without using the lane's oracle generation tool
(`tools/round-44/c1-oracle.py`) and without trusting `carriers.json`, then compare to the frozen
`oracle` blocks, the committed `corpus/evidence/round-44/oracle/` trees and the four committed
`after.json` published sets. No claim, counter, rubric, frozen byte or production doc was modified;
this file and `artifacts/R44W2C1Oracle/` are the only lane writes.

## 1. Headline

| question | verdict | basis |
|---|---|---|
| Are the four frozen `oracle` blocks true on this host, byte for byte? | **CONFIRMED** — 13 independent checks × 4 carriers, all true | §3–§7 |
| Does any member digest differ between my extraction and the frozen/committed sets? | **NO** — zero differing digests | §3 |
| Is the oracle binding falsifiable (no free pass)? | **YES** — positive arm green, four attack arms each red on the expected clause; the *only* structural free-pass surface is the byte-order digest collapse, closed by `subject_pin_ok` | §7 |
| Is the recorded C1 verdict (`carriers_matched 4`, `met_target false`, exit 1 at `55bcce69`) reproducible? | **YES**, exit code and counters reproduce exactly — but **the stated reason does not**: no carrier/oracle clause fails, and at `4cc1ac11` the same counter exits **0** with `met_target true` | §8–§9 |
| Is "the stop is the only correct reading" supported? | **FALSIFIED** (F1–F3): the instrument's own Target was met at `4cc1ac11`; the stop rests on an un-instrumented, internally contradictory prose conjunct | §9, §11 |
| Is M44-2 honest and sufficient, and does the round-45 preflight really catch it? | **Honest as recorded** (both counters exit 2 at the tip; the round measures at `55bcce69` and says so). **Catches it only under the correct `--pathspec`** — a plausible invocation free-passes (F5), and the no-pathspec default is a guaranteed false red (F6) | §10 |
| C2 at the measured revision (secondary, other seats own the attacks) | **CONFIRMED once**: exit 0, `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []` | §8 table |

## 2. Tools, method, scratch

Tool identity (measured, matches the frozen `toolchain`):

- `/usr/bin/unsquashfs` sha256 `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c`;
  version line `unsquashfs version 4.7.5 (2026/03/01)`; `unsquashfs --version` and `-version`
  **both exit 1** (measured) — the claim's item-4 warning is correct, parse the text.
- `/usr/bin/7z` sha256 `f802383f13b8331aabaf779def00a356c8d2b8148255170b75b03028f4d23ad4`;
  `7-Zip 26.04 (x64)`.
- `tools/round-44/c1-counter.py` sha256 `9f2cc140…ffea993` at the freeze, at `55bcce69` and at
  HEAD `8bb1090a` — byte-identical (`git show <rev>:tools/round-44/c1-counter.py | sha256sum`).

Method (all under `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Oracle/`, no lane writes):
`unsquashfs -lls`, `unsquashfs -s`, `unsquashfs -d <scratch>/x/<id>/root`, `sha256sum` per regular
member, `7z l`/`7z x -tSquashFS`, an independent 32-byte superblock + metadata-header parser, and
`tools/round-44/c1-counter.py --dev-arm` for the attack arms. Captures are committed as artifacts
(`captures/`, `sevenzip/`), so every claim below is re-checkable without my scratch.

## 3. Per-carrier result — 13 checks, all true

`truth-table.json` is the machine output of `oracle-rederive.py`; this is the summary.

| check | v1le | v1be | v2le | v2be |
|---|---|---|---|---|
| image sha256 + size == frozen `sha256`/`size` | ✓ | ✓ | ✓ | ✓ |
| `unsquashfs -lls` stdout sha256 == frozen `oracle.listing.stdout_sha256` | ✓ | ✓ | ✓ | ✓ |
| `unsquashfs -s` stdout sha256 == frozen `superblock_info.stdout_sha256` | ✓ | ✓ | ✓ | ✓ |
| `unsquashfs` extraction stdout sha256 == frozen `extraction.stdout_sha256` | ✓ | ✓ | ✓ | ✓ |
| extracted regular members (path,sha256,size) == frozen `oracle.members` | ✓ | ✓ | ✓ | ✓ |
| `7z x` members == frozen `oracle.members` | ✓ | ✓ | ✓ | ✓ |
| committed `corpus/evidence/round-44/c1/<id>/firmware.bin_extract` == frozen members | ✓ | ✓ | ✓ | ✓ |
| committed `corpus/evidence/round-44/oracle/…__output__/*_extract` == frozen members | ✓ | ✓ | ✓ | ✓ |
| recomputed `output_tree_digest` == frozen digest | ✓ | ✓ | ✓ | ✓ |
| `after.json` `normalized_result.files` (segment-bounded) == frozen members | ✓ | ✓ | ✓ | ✓ |
| `after.json` `raw_result.report` Stat/Hash pairs == frozen members | ✓ | ✓ | ✓ | ✓ |
| `after.json` normalized published set == raw report file set | ✓ | ✓ | ✓ | ✓ |
| `-lls` census (path,mode,owner,mtime,size,type) == frozen `oracle.census` | ✓ | ✓ | ✓ | ✓ |

Frozen `output_tree_digest` values, reproduced exactly:
`v1le = v1be = 8faae7739b14315c10683db41d63b92f511ec8e73ec94e6cc74bc414894f2a48`;
`v2le = v2be = 4178bb8379de3e5573eb448010d1c309fcda4dcb6bb4fd16ab11b4ab0535f947`.

## 4. Member digests (the attack surface) — no file differs

| carrier | member | size | sha256 |
|---|---|---|---|
| v1le, v1be | `apple.txt` | 6 | `303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0` |
| v1le, v1be | `banana.txt` | 7 | `5a81483d96b0bc15ad19af7f5a662e14b275729fbc05579b18513e7f550016b1` |
| v1le, v1be | `cherry.txt` | 7 | `86baf3529da550a44b0681ffa031b6b676e620e9e06dc5ac1119d0cd21cbcf55` |
| v2le, v2be | `apple1.txt` | 7 | `6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30` |
| v2le, v2be | `apple2.txt` | 7 | `919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff` |
| v2le, v2be | `apple3.txt` | 7 | `2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6` |
| v2le, v2be | `apple4.txt` | 7 | `08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d` |

Census rows (mode/owner/mtime) also match the frozen `census` arrays exactly — including the
`drwxrwxrwx` v1 root vs `drwxrwxr-x` v2 root and the 2024-08-05 / 2022-04-06 mtimes. Non-regular
members: **0 on all four** (`find … ! -type f ! -type d | wc -l` = 0), matching frozen
`oracle.nonregular: []` and the claim's zero-gap rule.
`after.json` `extraction_gaps` / `unpublished_entries` / `diagnostics` are absent-or-empty on all
four, and the only chunk is `squashfs_v1`/`squashfs_v2` with `extraction_failed: false`,
`encrypted: false` — exact strings, no prefix match.

One checked non-defect: `v2le/unblob.log` contains `File format is invalid handler=lzma` probe lines
at `real_offset=0xc`/`0x18` before the squashfs chunk is found. These are handler probes, not
chunks: `normalized_result.diagnostics` is `[]` on all four receipts and the single chunk succeeds.

## 5. Compression tokens — `unsquashfs -s` vs `file(1)`

`file(1)` here is `file` 5.48 (per `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:102`);
captures of every command are in `captures/<id>/`.

| carrier | endian | `unsquashfs -s` token | `file -b` token | block size `unsquashfs` vs `file` | `flags`@36 | inode-table meta header | body |
|---|---|---|---|---|---|---|---|
| v1le | le | Inodes compressed, Data compressed | `compressed` | 32768 vs **-32768** | `0x00` | `3700` (len 55, compressed) | `78da` |
| v1be | be | Inodes compressed, Data compressed | **`uncompressed`** ← wrong | 32768 vs **-32768** | `0x00` | `0038` (len 56, compressed) | `78da` |
| v2le | le | Inodes/Data/**Fragments** compressed | `compressed` | 65536 vs 65536 | `0x40` | `2e00` (len 46) | `78da` |
| v2be | be | Inodes/Data/**Fragments** compressed | **`uncompressed`** ← wrong | 65536 vs 65536 | `0x40` | `0030` (len 48) | `78da` |

- The v1/v2 superblock is 32 bytes and has no compression field; my independent parse confirms
  `bytes_used u32@8, s_major u16@28, s_minor u16@30`, magic `hsqs` (le) / `sqsh` (be), and the
  packed v1/v2 tail at 32: `block_size_1 u16@32`, `block_log u16@34`, `flags u8@36`,
  `no_uids@37`, `no_guids@38`. All values equal the frozen `probe_v1v2`/knowledge-entry table.
- `flags`@36 is `0x00` (v1) and `0x40` (v2); the NOD bit (`0x08`) is clear on all four, and the
  inode-table metadata header's high bit is clear on all four with a zlib body, so
  `compression: zlib(gzip)` is **observed from the bytes**, exactly as frozen.
- The `file` token flips with byte order alone: the two byte orders carry identical `flags` and
  identical member bytes, and `file`'s verdict differs — so the word is a `file` decode artifact,
  not an image property. This reproduces lesson R44-CL5 and `.ufo/waves/round-44/w1/R44C1FixtureAudit.md` N1.
- The scored path never binds `file`: `tools/round-44/c1-counter.py` contains no `/usr/bin/file`
  call; the only caller is the oracle **generator** `tools/round-44/c1-oracle.py:717`, which stores
  it as `superblock_info.file_verdict` with an explicit "do not bind" note. Counter-time
  `bindings.compression_detail` = `["gzip","gzip","gzip","gzip"]` and `oracle_tool_ok` re-hashes
  `unsquashfs` only.

## 6. Third reader: 7-Zip

`7z l -tSquashFS` exits 0 on all four and reports `File System = SquashFS 1.0/2.0`,
`Method = ZLIB`, `Big-endian = -/+/+`, `Cluster Size = 32768/32768/65536/65536` — matching
`carriers.json.oracle.sevenzip.header` field for field. `7z x` extracts the same member set with
the same digests (§3 row 6). `7z` is corroboration, not the independent oracle.

## 7. Attack arms — the binding is falsifiable and was falsified

`--dev-arm --arm-dir <scratch arm> --root <lane> --rev 4cc1ac11` (lane tree, scratch envelopes; the
mode never writes `corpus/evidence/round-44/c1`). Artifacts: `arms/arm{0..5}.json`.

| arm | mutation | exit | `dev_matched` | failing clauses | hits |
|---|---|---|---|---|---|
| arm0 | none (the four real receipts) | **0** | 4 | `[]` | 3/3, 3/3, 4/4, 4/4 |
| arm2 | v1le `apple.txt` sha256 → `0…0` | **1** | 3 | `v1le:oracle_hits_ok`, `v1le:evidence_id_ok` | v1le 2/3 |
| arm3 | v2le extra published file `extra.txt` | **1** | 3 | `v2le:oracle_hits_ok`, `v2le:evidence_id_ok` | v2le 4/4 but published set 5 |
| arm4 | v1be `apple.txt` → `sub/apple.txt` | **1** | 3 | `v1be:oracle_hits_ok`, `v1be:evidence_id_ok` | v1be 2/3 |
| arm5 | v1le ↔ v1be receipts swapped | **1** | 2 | `v1be:subject_pin_ok`, `v1le:subject_pin_ok` | 3/3, 3/3 |

So: a single wrong digest, one extra file, a nested wrong path and a byte-order swap each red, and
the unmutated set is green. No free pass in the oracle binding on this evidence.

**The latent collapse (F7).** `output_tree_digest` is *identical between byte orders*
(`8faae773…` for the v1 pair, `4178bb83…` for the v2 pair) because the member sets are identical.
The oracle binding therefore cannot distinguish `v1le` from `v1be`; byte-order discrimination rests
entirely on `subject_pin_ok` (the image sha256). arm5 shows that binding does its job today — the
swap reds only on `subject_pin_ok` — but a future claim that treats `output_tree_digest` as carrier
identity, or drops the subject binding, would free-pass a byte-order mislabel.

## 8. What the oracle did *not* fail on — and what the 55bcce69 red actually is

My re-runs (exact commands and receipts in `receipts.json`, JSONs in `counters/`):

| rev | command | exit | wall | `carriers_matched` | `met_target` | `failing` | `bindings_false` | `frozen_path_changed` |
|---|---|---|---|---|---|---|---|---|
| `4cc1ac11` | `c1-counter.py --rev 4cc1ac11 …` | **0** | 7.156 s | 4 | **true** | `[]` | `[]` | `[]` |
| `55bcce69` | `c1-counter.py --rev 55bcce69 …` | **1** | 7.062 s | 4 | false | **`[]`** | `province_core_section`, `province_core_row`, `frontier_note` | `[]` |
| `c86ea508` | `c1-counter.py --rev c86ea508 …` | **2** | 0.071 s | — | — | — | — | 8 paths (see §10) |
| `55bcce69` | `c2-counter.py --rev 55bcce69 …` | **0** | 4.388 s | — | true | — | — | `[]`; `entries_evaluated 80`, `mismatches []` |

At **both** `4cc1ac11` and `55bcce69` every carrier is green on `oracle_ok` (hits == files),
`tree_ok`, `projection_ok` (`projection_diff []`), `run_provenance_ok`, `subject_pin_ok`,
`evidence_id_ok`, `gaps_ok`, `nonregular_unpublished_ok`; `failing` is `[]` at `55bcce69`. The red at
`55bcce69` is produced by **the commit's own doc rollback**, not by any receipt field:

- `4cc1ac11` PROVINCE.md has `## Round-44 additions to Core` (line 424), a Core row naming both
  handlers, and a frontier note containing the entry stem → all three doc bindings true.
- `55bcce69` renamed that heading to `## Round-44 measured, not promoted (R44-C1 honest stop)`
  (PROVINCE.md:424), so `province_core_section` and `province_core_row` are false; and the rewritten
  frontier note (PROVINCE.md:430) **no longer contains the entry stem** `2026-10-28-r44-squashfs-v1v2-core`
  (0 occurrences of the stem in PROVINCE.md at `55bcce69`), so `frontier_note` is false.

The committed `counter-at-4cc1.json` says the same thing I measured: exit 0, `carriers_matched 4`,
`met_target true`, `bindings_false []`, `failing []`. The claim's own Target line is
`carriers_matched == 4, every binding true, frozen_path_changed [], met_target true, exit 0`
(`plans/round-44-claims.md:157-158`) — **satisfied at `4cc1ac11`**.

## 9. The stop: what the frozen text actually says

Two frozen sentences in the same file disagree, and only one of them is instrumented:

- `plans/round-44-claims.md:137-139` (Predicate P44-C1): "*the receipt's `parameters.output_directory`
  names this round's `/kaidoku-r44/` scratch segment and the evidence id is minted over that
  provenance; the runner binds the scratch-produced tree to the verbatim committed copy under
  `corpus/evidence/round-44/c1/`*" — **satisfied by all four receipts**
  (`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out`).
- `plans/round-44-claims.md:34-35` (wave-1 amendment, item 3): "*the receipt's
  `parameters.output_directory` must name a `corpus/evidence/round-44/c1/` path and the evidence id
  must be minted over that path*" — **unsatisfiable together with the predicate** when "a
  `corpus/evidence/round-44/c1/` path" means the committed path, and the data procedure
  (`plans/round-44-claims.md:161-164`) mandates `--rea-outdir-mode scratch`.

The counter implements the predicate and nothing else: `PROV_SEGMENT = '/kaidoku-r44/'`
(`tools/round-44/c1-counter.py:258`), `provenance_ok()` at 1176-1182 checks only absolute,
segment-containing, `..`-free (`d['run_provenance_ok']` at :1966), and the only
`corpus/evidence/round-44/c1` constant is `AFTERDIR` (:246), used solely as the default receipt
path (:2070, :2856). No scored clause reads item 3. Hence:

- the 55bcce69 red is **not** a provenance red — `run_provenance_ok` is true for all four;
- the met receipt at `4cc1ac11` stands as an admissible score under the claim's own
  freeze-integrity rule (`FREEZE` ancestor, `frozen_path_changed []`);
- the round's operative sentences describe the stop the other way round (F1, F2).

Defensible reading: because the frozen claim is internally contradictory, a conservative lane may
refuse to promote ("cannot satisfy the whole claim as written"). Not defensible: calling that the
*only* correct reading, or describing the counter as having rejected the landing on provenance, or
saying the score "does not satisfy the frozen predicate". The honest formulation is: *the predicate
and the instrument were met at `4cc1ac11`; the claim's amendment item 3 is unsatisfiable; the round
chose not to promote and rolled the Core docs back, which is what makes its counter red at
`55bcce69`.*

## 10. M44-2 and the round-45 preflight (secondary; the gate seat owns the audit)

As recorded, the freeze defect is honest: both counters exit **2** with the same 8
`tools/round-44/control-fixtures/**` paths at `c86ea508` (my C1 run reproduces it; C2's committed
receipt lists the identical 8), and the round measures at `55bcce69`, where both are clean
(`frozen_path_changed []`). Measuring at an ancestor whose frozen blobs are intact is what the rule
permits; the tip is disclosed as inadmissible, not silently scored.

`tools/round-45/frozen-path-preflight.py` behaviour I measured at `--freeze c48f8a4b --rev c86ea508`:

| invocation | exit | verdict | observed |
|---|---|---|---|
| `--pathspec tools/round-44/` | **1** | `frozen_path_changed` | the same 8 paths, status `M`, `blob_changed` also 8 |
| `--pathspec plans/round-44-claims.md` | **0** | `clean` | `touched []` — **the violation is present and the gate says clean** |
| no `--pathspec` | **1** | `frozen_path_changed` | 542 touched paths: 423 under `.ufo/`, 107 under `corpus/`, 8 under `tools/`, plus `PROVINCE.md`, `SCORECARD.md` — none of which this claim freezes |

At `55bcce69` with `tools/round-44/`, `plans/round-44-claims.md` and the fixtures directory it exits
0 clean, so it is not a blanket red. So: **it really catches c86ea508 — when handed the frozen
directory pathspec.** It cannot derive that pathspec from the claim's `## Frozen paths` prose, so a
plausible operator invocation (the claims file) returns clean on the exact defect (F5), and the
declared default is a guaranteed false red (F6). It also takes a resolved `--rev`, so it can only
gate an existing commit object (candidate-before-push or a post-commit gate), not the commit being
created — [INFERENCE] from the argument contract.

## 11. Findings for L1 (each with path:line, command, exit code, observed value)

**F1 — record misattributes the stop to the predicate (medium).**
`PROVINCE.md:428` at `55bcce69`: "*the claim required the committed evidence path, while the counter
accepts only the `/kaidoku-r44/` scratch provenance. The score therefore does not satisfy the frozen
predicate*".
Command `python3 -I -B tools/round-44/c1-counter.py --root <lane> --rev 55bcce69… --freeze c48f8a4b…
--pkg65 <rea-agents> --work <scratch> --json-out <scratch>` → **exit 1**, and every carrier shows
`run_provenance_ok: true`. The predicate (`plans/round-44-claims.md:137-139`) requires precisely the
scratch segment the receipts carry; the `corpus/evidence/round-44/c1/` demand is amendment item 3
(`plans/round-44-claims.md:34-35`). Also, the claim required **both**, not only the committed path.
Fix: say "the wave-1 amendment's committed-path conjunct is unsatisfiable with the scratch predicate"
— not "the counter accepts only …" and not "does not satisfy the frozen predicate".

**F2 — the 55bcce69 exit 1 is a doc-rollback red, and the met receipt is not reconciled (high).**
`bindings_false = ["province_core_section","province_core_row","frontier_note"]`, `failing = []`
(measured twice, and identical to `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`). PROVINCE.md at
`55bcce69` has no `## Round-44 additions to Core` heading and **zero** occurrences of the entry stem
(`git -C <lane> show 55bcce69:PROVINCE.md | grep -c 2026-10-28-r44-squashfs-v1v2-core` → `0`), while
at `4cc1ac11` both exist (heading line 424, stem present). `corpus/evidence/round-44/c1/counter-at-4cc1.json`
records exit 0 / `met_target true` / `bindings_false []`. The lesson
(`corpus/lessons/round-44.md:63-68`) does not disclose this; only
`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:224` does. Fix: the lesson must state the
4cc1 met receipt and that the 55bcce69 red is the rollback itself (three doc bindings), so a reader
cannot conclude the instrument rejected the evidence.

**F3 — the rolled-back PROVINCE frontier note lost the entry stem (medium).**
`PROVINCE.md:430` at `55bcce69` cites neither the stem nor the entry; the round's own predicate
requires a frontier note carrying the stem (`tools/round-44/c1-counter.py:2161` binds
`FRONTIER_MARK in l and STEM in l`). So the honest-stop landing is itself a doc-binding failure,
independent of the provenance question. Fix: re-add the stem to that note (append only) or record
that the binding is knowingly false for the stop revision.

**F4 — `counter_sha256_at_freeze` is required by the claim and absent from every C1 receipt (medium).**
`plans/round-44-claims.md:85-87`: "*Every score receipt records the scorer's exit code,
`counter_sha256` … and `counter_sha256_at_freeze` (round-41 closure D4)*". `counter-at-4cc1.json`,
`.ufo/waves/round-44/l1/c1-score-4cc1.json` and `c1-score-at-55bcce69.json` carry `counter_sha256`
`9f2cc140…` and **no** `counter_sha256_at_freeze` key; `grep -n counter_sha256
tools/round-44/c1-counter.py` shows only the former. The C2 receipts do carry it
(`c2-score-at-55bcce69.json`), so the field is a lane convention C1 skipped. (Value today would be
identical — the counter blob is unchanged freeze→rev — so this is a record gap, not a score gap.)

**F5 — the round-45 preflight free-passes under a plausible pathspec (medium).**
Commands and exits in §10: `--pathspec plans/round-44-claims.md --rev c86ea508` → **exit 0, verdict
`clean`, `touched []`**, on the very revision that adds/modifies 8 files under the frozen
`tools/round-44/` directory. The gate has no binding to the claim's frozen-path list and no
requirement that the pathspec set be complete. Fix: take the claim file and derive its `## Frozen
paths` entries (or fail closed when no pathspec is given), and record the pathspec set in the
receipt so a passing receipt proves coverage.

**F6 — the preflight's no-pathspec default is a guaranteed false red (low).**
`tools/round-45/frozen-path-preflight.py:30` advertises "*Default: none (tree backstop only)*", but
:47 passes no `--` filter and :63 collects every changed path, so :79 reds on any non-empty range.
Measured: exit 1, 542 touched paths (423 `.ufo/`, 107 `corpus/`, 8 `tools/`, `PROVINCE.md`,
`SCORECARD.md`) — including paths no R44 claim freezes, e.g. `SCORECARD.md` which
`plans/round-44-claims.md:316-322` explicitly does **not** freeze. Fix: skip the walk when no
pathspec is given (tree backstop only), or correct the help text.

**F7 — `output_tree_digest` is not a carrier identity (low, latent free pass).**
Frozen digests collide across byte orders (`8faae773…` v1le=v1be, `4178bb83…` v2le=v2be); the arm5
swap reds only via `subject_pin_ok`. Fix: never cite `output_tree_digest` as a per-carrier pin; if a
future claim drops the subject binding, add the image sha256 into the digest definition.

**F8 — the scored path never re-runs the oracle (low, disclosed class D-09/D-13).**
`oracle_hits_ok` compares against frozen `carriers.json` rows plus the committed `__output__` tree
(`tree_check`, `tools/round-44/c1-counter.py:2254`); `oracle_tool_ok` only re-hashes
`/usr/bin/unsquashfs` and its version line. My re-derivation (§3–§7) is what makes the frozen rows
trustworthy on this host today; the score itself does not. Fix: keep an oracle re-derivation seat in
every round that promotes on a frozen census, or add a counter-time `unsquashfs -lls` re-read
bounded to the carrier set.

## 12. Confirmations (what I could not break)

- All four frozen `oracle` blocks, both `-lls`/`-s`/extraction stdout sha256s, the census rows, the
  member digests, the two `output_tree_digest` values, the committed extract and oracle trees, and
  the `after.json` published sets (both `normalized_result.files` and the paired
  `raw_result.report` Stat/Hash rows): **all equal**. Zero differing digests.
- Zero non-regular members; `gaps`/`unpublished_entries`/`diagnostics` empty; handler strings exact
  (`squashfs_v1`, `squashfs_v1`, `squashfs_v2`, `squashfs_v2` — no prefix match); single chunk per
  carrier, not encrypted, not failed.
- `subject_sha256` == frozen pin on all four; `evidence_id_ok` flips under any published-set
  mutation (arms 2–4), so the evidence id binds the published bytes.
- The counter binary is byte-identical at freeze, `55bcce69` and HEAD; `compression_detail` is
  `["gzip","gzip","gzip","gzip"]` from the metadata block, and `file` text is never bound.
- C2 at `55bcce69`: exit 0, 80/80, no mismatches, no frozen-path drift (one run; the C2 attack
  seats own vacuity/note-vs-value).

## 13. Residual limits of this seat

- The four carriers are 4 KiB images with 3–4 members of 6–7 bytes; a green oracle says nothing
  about multi-block members, fragments across blocks, symlinks, devices or subdirectories (D-07,
  D-08). `unsquashfs` and `sasquatch` (unblob's extractor) share squashfs-tools lineage; `7z` is a
  third implementation but still one family (D-09). `output_tree_digest` collapses byte order (F7).
- I adjudicated the *oracle* surface. The frozen-claim satisfiability adjudication belongs to the
  Satisfiability seat, the receipt-content audit to the ReceiptAudit seat, the gate audit to the
  Preflight seat; F1–F3 are oracle-adjacent record statements and F5–F6 overlap that seat — they are
  reported because they were measured here, not to pre-empt it.
- [INFERENCE] where marked: the preflight cannot run against an uncreated commit, and the
  admissibility of a mid-round revision is read from the claim's freeze-integrity wording.

## 14. Scratch discipline and artifacts

All scratch lived in `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Oracle/` (one live extraction per
carrier, one `--work` dir per counter family, `TMPDIR` never used, nothing under `/tmp` cited) and
was deleted at the end of the seat (`rm -rf`; the tree is gone, verified). No git/jj mutation ran
anywhere; no fixture repo was created; no lane file outside
`.ufo/waves/round-44/w2/R44W2C1Oracle.md` and `.ufo/waves/round-44/w2/artifacts/R44W2C1Oracle/` was
written (`git -C <lane> status` shows only sibling seats' own paths and pre-existing L1 edits).
No tool was installed or upgraded; nothing needed it.

Artifacts (`artifacts/R44W2C1Oracle/`, 45 files plus `MANIFEST.sha256`, verified clean with `sha256sum -c`):
`receipts.json` (every command with cwd, exit code, stdout/stderr sha256, wall time),
`truth-table.json`, `census-check.json`, `oracle-rederive.py`, `counters/c1-at-4cc1ac11.json`,
`counters/c1-at-55bcce69.json`, `counters/c1-at-c86ea508.json`,
`counters/c2-at-55bcce69-headline.json`, `preflight/pf-dir-c86ea508.json`,
`preflight/pf-claims-only-c86ea508.json`, `preflight/pf-no-pathspec-c86ea508-summary.json`,
`preflight/pf-55bcce69-3pathspecs.json`, `arms/arm{0,2,3,4,5}.json`,
`captures/<id>/{lls.out,lls.err,s.out,s.err,extract.out,extract.err}`, `sevenzip/<id>-list.txt`.
