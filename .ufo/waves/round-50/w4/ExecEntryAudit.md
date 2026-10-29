# ExecEntryAudit — R50 attempt-2 wave-4 falsify: the landed C1 entry against the committed receipts

**Verdict: ATTACKED AND HELD — the landed entry's numbers reproduce; three wording overstatements were
found and are already corrected by the L1 in commits `b98fd2d0` / `1bff0613` / `4db20b0b` (landed during
this wave). One residual overstatement SURVIVES at the current tip and is reported below as F4.**

Seat: `ExecEntryAudit`. Axis: coverage / depth / calibration of the entry
`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`.
Target rev audited: `c67b741e8f6bd8d64adbdb15e059d47fde004c77` (the dispatched tip). Because the L1 landed
falsify corrections while this seat was running, the audit was re-run against the **then-current tip
`4db20b0b`** and re-confirmed once more at the **final tip `98cd8ce5`** (the state this report describes);
both states are reported. Read-only on the lane tree: no lane file other than this
report and `.ufo/waves/round-50/w4/ExecEntryAudit/` was written.

---

## 1. Findings table

| # | severity | claim under attack | verdict | evidence |
|---|---|---|---|---|
| F1 | STOP (at tip `c67b741e`) | entry:3 "every documentation binding true" and entry:82 "the counter at the landing reports every documentation binding true" | **REFUTED at tip `c67b741e`**; the cited receipt `c1-after-attempt2.json` carries `bindings_false: ["province_core_section","province_core_row"]`. **Already corrected** by `b98fd2d0` (entry:3 now names which bindings are true and which two are false). | `counter-receipt-extract.json`; `receipts.json` |
| F2 | STOP (at tip `c67b741e`) | entry:52 "(the counter's own REA rerun reproduced the projection on all four carriers)" | **REFUTED at tip `c67b741e`**: the receipt has `g7581:projection_ok = false` with `projection_error` = `execution_failure` / `ENOENT … readlink '…/usr/www.myfritz/avme/cgi-bin/luacgi'`; `failing` = `["g7581:gaps_ok","g7581:projection_ok","g7582:gaps_ok"]`. The rerun reproduced on **three** carriers. **Already corrected** by `b98fd2d0` (entry and `SCORECARD.md:3796` now say "three carriers … failed on `g7581`"). | `counter-receipt-extract.json` |
| F3 | MINOR (at tip `c67b741e`) | entry:52 "its 636 `unpublished-entry` gaps name no `dev/*` path" | **REFUTED literally**: 2 of the 636 gaps do name a `dev/*` path (`firmware.bin_extract/dev/kdsld_misc`, `firmware.bin_extract/dev/new_led`) — both are `symlink` oracle rows, so the *intended* claim (no `char-device` is disposed) held, but the wording as written was false. **Already corrected** by `b98fd2d0`. | `results-table-check.json`; `gap-rule-reapply.txt` |
| F4 | **MINOR — SURVIVES at tip `98cd8ce5`** | entry:82 "The binding question is now answered: the counter at the landing reports **every documentation binding true**" | **STILL FALSE at the final tip.** `grep -c "every documentation binding true"` on the entry = **1**, at line 82, re-confirmed at tips `4db20b0b` and `98cd8ce5`. The cited receipt still reports `bindings_false: ["province_core_section","province_core_row"]`. The status line (entry:3) was fixed in `b98fd2d0`; this second, identical claim at entry:82 was not. | `counter-receipt-extract.json`; `receipts.json` |
| F5 | MINOR | entry:82 "the big-endian **ARM** member of the cable images" | **UNSUPPORTED AS LABELLED.** The sibling's byte order and `sqsh` magic are backed (census `magic:"sqsh"`, `endian:"BE"`; `sbwalk` `structural_order: "BE"`, `mkfs_time == bytes_used == 5981012`), but **nothing in the lane names that member's CPU**: `carriers.json` says only "Puma x86 side" for the *x86* member, and the word "ARM" appears nowhere in `corpus/knowledge/*.md` for this carrier. The entry's own Limit 5 concedes "the SoC lines are not self-described by the images". Same word appears at entry:31. | `carriers.json` notes; `census-members.json`; `sbwalk-img_c6430.remote.fs.sqfs.json` |
| F6 | MINOR | entry:54 census "70 FRITZ!Box model directories are published under `https://download.avm.de/fritzbox/`" | **NUMBER NOT DERIVABLE FROM THE COMMITTED CENSUS.** The committed census metadata holds **69** distinct model keys (`census-members.json` and `census-images.json`); `census-run.log` prints `MODELS 70` because the tool counted a root-listing key set that includes a dir it then could not fetch. The live root listing does carry **70** `fritzbox-*` dirs (re-fetched, HTTP 200) — so the *published* claim is true, but the committed evidence underwrites 69, and the gap is 1 uncounted directory. Partially addressed in the working tree ("re-counts to 70 … 26 HTTP-416 rows and 4 no-image rows set aside"). | `census-members.json`, `census-images.json`, `census-run.log`, live listing capture |
| F7 | observation | entry:31 the BE sibling member sha256 / `bytes_used` for both cable carriers | **HELD.** `334e56df…` / 5 442 392 (6490) and `7d3677e6…` / 5 981 012 (6430) both reproduce from `census-members.json`; the 6430 sibling's own sha256 `7d3677e679ad…` is the `sbwalk` receipt's `sha256` field, and its `bytes_used` is 5 981 012 with `structural_order: BE`. | `census-members.json`; `sbwalk-img_c6430.remote.fs.sqfs.json` |

**No STOP finding survives at the final tip except F4**, which is a one-sentence wording fix that the L1
already made once (entry:3) and simply missed at entry:82. F5 and F6 are wording-bound, not numeric.

---

## 2. What reproduced exactly (the numbers the entry claims)

### 2.1 Results table vs `corpus/evidence/round-50/c1/<id>/after.json`

Every cell of the four-row results table was recomputed from the committed receipts — **all hold**:

| id | published regular files (entry) | = `len(files)` in after.json | oracle regular files (entry, frozen table) | = `wc -l` of `oracle.tsv` | = published | gaps (entry) | = gap kinds in after.json | `MaliciousSymlinkRemoved` (entry) | = diagnostics count | evidence id prefix |
|---|---|---|---|---|---|---|---|---|---|---|
| `g7581` | 4 556 | 4556 ✓ | 4 556 | 4556 ✓ | ✓ | 637 (1 `depth-limited`, 636 `unpublished-entry`) | 637 = {depth-limited:1, unpublished-entry:636} ✓ | 3 | 3 ✓ | `ev_f4251903a11bf283d…` ✓ |
| `g7582` | 4 564 | 4564 ✓ | 4 564 | 4564 ✓ | ✓ | 637 (1, 636) | {1, 636} ✓ | 3 | 3 ✓ | `ev_9f0bfadd046c21135…` ✓ |
| `c6490` | 4 709 | 4709 ✓ | 4 709 | 4709 ✓ | ✓ | 613 (1, 612) | {1, 612} ✓ | 1 | 1 ✓ | `ev_eb2df41db9fad594a…` ✓ |
| `c6430` | 3 955 | 3955 ✓ | 3 955 | 3955 ✓ | ✓ | 568 (1, 567) | {1, 567} ✓ | 1 | 1 ✓ | `ev_f7a3a30e098624ffc…` ✓ |

The "oracle non-regular entries" column (1 001 / 1 001 / 914 / 824) equals `wc -l` of the matching
`.nonregular.tsv` in all four cases, and the `sha256` of the frozen tables is unchanged
(`g7581.oracle.tsv` `03b24463…`, `g7581.nonregular.tsv` `e8706799…`).

**Published-set equality was re-derived, not assumed.** Comparing the `files[]` list of each
`after.json` (path, sha256, size) against the frozen oracle table row-by-row:

```
g7581  published=4556  oracle=4556  only_published=0  only_oracle=0  content_diff=0
g7582  published=4564  oracle=4564  only_published=0  only_oracle=0  content_diff=0
c6490  published=4709  oracle=4709  only_published=0  only_oracle=0  content_diff=0
c6430  published=3955  oracle=3955  only_published=0  only_oracle=0  content_diff=0
```

So "REA published every oracle regular file on all four carriers" is exactly true — no extra file, no
missing file, no content difference.

### 2.2 Oracle tables re-derived twice, independently

* **`unsquashfs` 4.7.5** (host binary `/usr/bin/unsquashfs`, `unsquashfs version 4.7.5 (2026/03/01)`)
  run over the cached carrier bytes: the per-kind counts equal the frozen tables' totals for every
  carrier — `g7581` regular 4556 / {dir 349, symlink 639, char-device 13} = 1001; `g7582` 4564 / same
  1001; `c6490` 4709 / {300, 613, 1} = 914; `c6430` 3955 / {255, 568, 1} = 824. Exit 0 on all four.
* **the lane's own second reader** `tools/round-41/sqfs-list.py --layout auto` over the same bytes:
  **0 diff lines** against both frozen tables for all four carriers (`diff <(sort new) <(sort frozen)`),
  i.e. the re-derivation is byte-identical to the committed oracle tables.

Artifact: `unsquashfs-rederive.txt`, `sqfs-list-rederive.txt`.

### 2.3 The frozen gap rule re-applied by hand

`tools/round-50/gap-rule.json` was re-implemented against each committed `after.json` + frozen
non-regular table (`gap-rule-reapply.py`, output `gap-rule-reapply.txt`):

```
g7581: nonregular=1001 gapped=636 removed=3 silent=1 MISSING=12
   dev/pts/0..7 (char-device 136:0..136:7), dev/tiatm (230:0), dev/ttyp0..2 (3:0..3:2)
g7582: same shape, MISSING=12
c6490: nonregular=914  gapped=612 removed=1 silent=1 MISSING=0
c6430: nonregular=824  gapped=567 removed=1 silent=1 MISSING=0
```

**The "12 vs 13" census in the task brief resolves as: 13 char-device rows exist per FRITZ!Box carrier,
of which `247:0` (`dev/led`) is the *one* the rule silently admits, leaving exactly 12 undisposed.**
The entry's census sentence ("13 `char-device` entries each … the frozen rule … silently admits only
`247:0` … no gap and no removal for the other twelve") is **correct** and the counter's own
`gaps_note` ("required entry with no disposition … on ['dev/pts/0' … 'dev/pts/7']", truncated at 8) is
the receipt's own wording.

### 2.4 Run facts vs `run.json`

| id | `duration_ms` | entry claim | `rea_attempts` | `output_directory_prefix_ok` | `run_provenance_segment_ok` | tool pins |
|---|---|---|---|---|---|---|
| `g7581` | 12 687 (**12.7 s ✓**) | 12.7 s ✓ | 1 ✓ | true ✓ | true ✓ | rea-agents 6.5.0 / unblob 26.6.4 / sasquatch 4.5.1 ✓ |
| `g7582` | 21 874 | (not claimed) | 1 ✓ | true ✓ | true ✓ | ✓ |
| `c6490` | 20 282 | (not claimed) | 1 ✓ | true ✓ | true ✓ | ✓ |
| `c6430` | 8 266 | (not claimed) | 1 ✓ | true ✓ | true ✓ | ✓ |

The entry's "12.7 s" is a single-carrier datum and is exact for `g7581`; it does not claim the other
three durations. The tool pins in every `run.json` match the entry's recheck text.

### 2.5 The POS statement vs `.ufo/waves/round-50/controls-attempt2.json`

The entry says: *"The positive control CTL-C1-POS was already red on the frozen POS fixtures before the
data run (`.ufo/waves/round-50/controls-attempt2/`), which is the same defect measured pre-data; the kill
rule did not fire (no counterfactual went green)."*

Committed controls summary (`controls-attempt2.json`, sha256 `bca20d5e…`):

* `CTL-C1-POS`: `exit_code 1`, `carriers_matched 2`, `verdict "misbehaved"`, `why "expected exit 0, got 1"` → **red pre-data ✓**
* `kill_rule_fires: false`, `kill_rule_detail: []` → **kill rule silent ✓**
* `failures: ["CTL-C1-POS"]`, `unevaluated: []`, `utc 2026-10-29T20:43:19Z`
* the POS receipt's own `per_carrier_failing` = `{g7581: ["gaps_ok"], g7582: ["gaps_ok"]}` → **"the same defect measured pre-data" ✓**

**HELD.** The POS statement reproduces exactly.

### 2.6 Counter receipt vs entry (and the F1/F2 refutations)

From `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (sha256 `e1e0ac17…`):

| receipt field | value | entry claim at tip `c67b741e` | verdict |
|---|---|---|---|
| `carriers_matched` / `target` | 2 / 4 | "2 of 4" | ✓ |
| `exit_code` | 1 | "exit 1" | ✓ |
| `frozen_path_changed` | `[]` | "`frozen_path_changed []`" | ✓ |
| `failing` | `["g7581:gaps_ok","g7581:projection_ok","g7582:gaps_ok"]` | entry cited only the two `gaps_ok` items | **F2** |
| `bindings_false` | `["province_core_section","province_core_row"]` | "every documentation binding true" | **F1** |
| `projection_ok` per carrier | g7581 **false**, g7582/c6490/c6430 true | "reproduced the projection on all four carriers" | **F2** |
| `gaps_ok` per carrier | g7581 false, g7582 false, c6490 true, c6430 true | "`gaps_ok` false on `g7581` and `g7582`" | ✓ |

The `province_core_*` bindings are false because the landing deliberately put the row under
`## Round-50 measured, not promoted (R50-C1 honest stop)` — the counter's `CORE_HEADING` is
`## Round-50 additions to Core` (`tools/round-50/c1-counter.py:379`) — so the section and the Core-row
bindings cannot be true for a not-promoted landing. The binding is *structural*, not a defect in the
landing; the defect was only the entry's wording that all bindings were true.

### 2.7 Carrier table vs `tools/round-50/carriers.json`

All 7 populated cells of all 4 carrier rows (image URL, image sha256, tar member, member sha256,
member B, carrier B, carrier sha256) were compared cell-by-cell against `carriers.json`: **all match
(28/28 cells)**. The `member B` values (28 368 904 / 28 610 568 / 28 200 968 / 23 863 304) and the
`carrier B` values (28 368 210 / 28 607 082 / 28 200 029 / 23 861 507) reproduce. The BE sibling values
(F7) reproduce.

### 2.8 Census rows vs the committed census metadata

`census-members.json` re-counted: **28** `hsqs` v4.0 xz rows, **28/28 with `marker: true`** (0 without),
across **16 models**; **23** rows at `./var/tmp/filesystem.image` in **13** models and **5** rows at
`./var/remote/var/tmp/x86/filesystem.image` in **3** models (`fritzbox-6430-cable`, `fritzbox-6490-cable`,
`fritzbox-6590-cable`). All four carriers are among the 28 (`c6490` appears twice — the entry's carrier
uses the `deutschland` URL, which is the one pinned in `carriers.json`).

"20 census rows had zero-length headers" → **20** rows with `member_size == 0` ✓.
"4 `sqsh` rows reported version 0.0" → **4** ✓ (the 20 zero-length rows carry magic `2e2f7661`, i.e.
the tar path bytes, not a squashfs magic — consistent with a zero-length member).
"none of the 28 lacks the marker (0 of 28 rows)" ✓.

### 2.9 SOURCES rows S243 / S244 / S245 / S249 re-opened

* **S243** (Freetz patch 101) re-fetched live: sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`, 1 153 B — **equals the row** ✓. Cited lines verified: `:7` is `+#define AVM_LE 2` ✓; `:17-18` are the byte-order condition naming `AVM_LE` ✓.
* **S245** (unblob `squashfs.py` @ 26.6.4) — the installed copy at `/home/vgpnk/.local/share/uv/tools/unblob/.../squashfs.py` hashes to `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, 19 842 B — **equals the row and the entry's claim that it is byte-identical to the installed copy** ✓. Cited lines verified in the installed file: `:40` `case Endian.BIG, 4:`, `:48` the sole `is_avm` test (`header.bytes_used == header.mkfs_time`), `:53-54` `case Endian.LITTLE, _:` → `commands_args.append("-le")`, `:455` `NAME = "squashfs_v4_le"`, `:463` the LE pattern `68 73 71 73 [24] 04 00` ✓. The entry's inference — "every little-endian image takes `sasquatch -le -no-exit-code -f -d …`, marker or not" — is **confirmed by the source**: the `is_avm` test sits inside the `Endian.BIG, 4:` branch and the LE branch appends `-le` unconditionally.
* **S249** (licence `info_en.txt`) re-fetched live: sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7`, 67 591 B — **equals the row** ✓. Line 850 holds the quoted 18-word sentence ✓ (the committed `licence-6490-info_en-line850.txt` receipt is 224 B and matches the live line exactly).
* **S244** — the four `fritz.os/` listings re-fetched live: the row's size/date facts reproduce exactly (19-Aug-2024 32 010 240 B; 19-Aug-2024 32 256 000 B; 04-Sep-2023 39 741 440 B; 05-Sep-2023 35 911 680 B), and the re-fetched listing bodies are committed under `.ufo/waves/round-50/w3/ScribeLessonGate/receipts/sources/` (21 tracked files there) ✓.
* Registry: **152 → 156** rows (`git show 0f0eee3b^:corpus/SOURCES.md | grep -c "^| S[0-9]"` = 152; tip = 156) ✓; the four new rows are S243/S244/S245/S249 and all four name the entry in `used-by` ✓.

### 2.10 Frozen instrument integrity

`tools/round-50/c1-counter.py` sha256 `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`
is **identical** at the freeze `435d41fd`, at the tip, and in the receipt's `counter_frozen_sha256` /
`counter_sha256` ✓. Its **offline** `--selftest` (no REA) on a scratch clone at `c67b741e`:
**exit 0, 169 cases, 17 `green_ok`, 152 `red_ok`** (artifact `counter-selftest.out`, sha256 `fd43ee62…`).

---

## 3. What I could not verify

* **No REA run.** The C1 counter's full predicate command was not re-run (the L1 owns it), so
  `g7581`'s rerun remains unverified — the committed receipt says the fresh rerun *failed* there, and
  nothing in the lane re-ran it since. The entry now discloses this (F2 corrected).
* **`g7581`'s rerun failure is unexplained.** The `ENOENT … readlink '…/usr/www.myfritz/avme/cgi-bin/luacgi'`
  is an extractor-tree race in the *rerun* tree, not a receipt-side fact; the committed receipt's own
  `files[]` list **does** contain `firmware.bin_extract/usr/www/cgi-bin/luacgi` with the oracle-matching
  sha256 `49e3ece0…`. I could not determine whether the failure is host-load, a unblob race, or a real
  body difference, because reproducing it needs a REA run. **Left as an open question for the L1.**
* **ARM (F5)** — the BE sibling's CPU is not named anywhere in the lane; the claim cannot be checked,
  only bounded.
* The census's 70th model directory (F6) is not identified by name in the committed metadata.

---

## 4. Notes for the L1

1. **F4 is the only actionable item left.** entry:82 still says "every documentation binding true"
   (`grep -c` = 1, at line 82, re-confirmed at tip `98cd8ce5`) while the cited receipt says
   `bindings_false: ["province_core_section","province_core_row"]`. entry:3 was already fixed to name
   the true/false split in `b98fd2d0`; entry:82 carries the identical sentence and was missed.
   One-clause fix, same wording as the status line.
2. **F5** — drop or bound the word "ARM" at entry:31 and entry:82 ("the big-endian ARM member of the
   cable images"). The bytes support `sqsh`/BE/`bytes_used`; the CPU is not in evidence, and the
   entry's own Limit 5 already concedes the images do not name their SoC.
3. **F6** — the "70 model directories" figure is true of the live listing but the committed census
   metadata underwrites 69; the working-tree wording ("re-counts to 70 … 26 HTTP-416 rows and 4
   no-image rows set aside") is the better form and should be carried into the commit.
4. **Everything else held.** The results table, the carrier table, the run facts, the POS statement,
   the 13-vs-1 char-device census, the gap-rule re-application, both oracle re-derivations, the SOURCES
   rows and the registry counts all reproduce exactly against the committed receipts.

---

## 5. Reproduction

Artifacts in `.ufo/waves/round-50/w4/ExecEntryAudit/`:

| file | what it holds |
|---|---|
| `receipts.json` | every command run by this seat: exact argv, exit code, stdout sha256, UTC |
| `results-table-check.json` | per-carrier published/gap/removal/evidence extraction from the committed `after.json` |
| `counter-receipt-extract.json` | the counter receipt's bindings, failing list, per-carrier `projection_ok` / `gaps_ok` / `gaps_note`, and `g7581`'s `projection_error` |
| `oracle-wc-l.txt` | `wc -l` of the eight frozen oracle tables |
| `unsquashfs-rederive.txt` | independent oracle re-derivation (unsquashfs 4.7.5) per carrier |
| `sqfs-list-rederive.txt` | second-reader re-derivation + `diff` line counts vs the frozen tables |
| `gap-rule-reapply.py` / `gap-rule-reapply.txt` | the frozen gap rule re-applied by hand per carrier |
| `controls-attempt2-summary.json` | the POS control verdict + kill-rule state as committed |
| `counter-selftest.out` | the frozen counter's offline selftest output (169 cases, exit 0) |

Scratch `S=/fast/scratch/hyaku/kaidoku-r50/w4-ExecEntryAudit` held the carrier-cache reads, the
`git clone --shared` lane copy and the two reader outputs; it is removed on yield. No lane file was
modified; no commit, push, stage or stash was run. No tool was installed or upgraded (none needed).

**Exit codes.** All commands in `receipts.json` exited 0 — this is a *verdict* report, not a gate: the
findings are semantic mismatches between the entry text and the receipts, not command failures.
