# ScribeLessonGate — receipts (round 50, attempt 2, wave 3)

Seat dir: `.ufo/waves/round-50/w3/ScribeLessonGate/`. Scratch: `/fast/scratch/hyaku/kaidoku-r50/w3-ScribeLessonGate` (removed after these receipts were copied). All commands run from the fleet root `/home/vgpnk/Projects/shokunin` or from the seat scratch; every fetch body is a public index/listing/text body — **no firmware image was downloaded by this seat**.

Lane tree writes: only this seat dir. The lane tree, the fleet repo, `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md` were **not** modified. No commit / push / stage / stash / mutating git or jj in the lane or the fleet repo. The only git write was inside a scratch `--shared` clone under the seat scratch (`git -C "$S/clone"`), whose toplevel was asserted before its first commit.

## R1 — source re-fetch (2026-10-29, UTC from the HTTP `date` header)

    S=/fast/scratch/hyaku/kaidoku-r50/w3-ScribeLessonGate; export TMPDIR="$S"
    curl -sS -D "$S/src/$name.hdr" -o "$S/src/$name.body" \
         -w '%{http_code} %{size_download} %{time_total}\n' --max-time 40 "$url"

| # | url | http | bytes | server date | body sha256 | exit |
|---|---|---|---|---|---|---|
| R1.1 | https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch | 200 | 1,153 | 2026-10-29T20:34:23Z | `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` | 0 |
| R1.2 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | 200 | 19,842 | 2026-10-29T20:34:23Z | `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` | 0 |
| R1.3 | https://download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/ | 200 | 574 | 2026-10-29T20:34:24Z | `c1dd76d62a6a2ac9964a9844be8d69c6dc902cb00ef16bcb04a2a39176248589` | 0 |
| R1.4 | https://download.avm.de/fritzbox/fritzbox-7582/other/fritz.os/ | 200 | 574 | 2026-10-29T20:34:25Z | `18ccf34526bb95f675679820e3ace0ddd9c56b6b5e6d76472c364d101453d70d` | 0 |
| R1.5 | https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/ | 200 | 604 | 2026-10-29T20:34:26Z | `4de2023728137eefc887853dded6b354e9c602929b35450576baa21533b2beb7` | 0 |
| R1.6 | https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/ | 200 | 604 | 2026-10-29T20:34:27Z | `ab4da28c400a7b8493e6bae56f68f1aa98fb104e64865336380e31aa7dfeaabf` | 0 |
| R1.7 | https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt | 200 | 67,591 | 2026-10-29T20:34:27Z | `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7` | 0 |
| R1.8 | https://download.avm.de/fritzbox/ (root index) | 200 | 8,990 | 2026-10-29T20:40:12Z | `75e886e28f104038649196da4f5509cab8536c5046479184c835e7f06fc40764` | 0 |

Header secret scan: `grep -il 'set-cookie\|authorization' *.hdr` matched only `freetz101.hdr` and `unblob-squashfs.hdr` (GitHub's anonymous `_gh_sess`/`_octo` cookies). **No header was copied into the seat dir**; only the status/date/length/etag lines were read. The licence body was kept in scratch; only its located line 850 was copied.

## R2 — located-quote verification (offline, seat tool)

    python3 -I -B tools/quote-check.py --body <body> --label <row> --expect <line>:<substring> ...

| # | row | body | expectations | result | exit |
|---|---|---|---|---|---|
| R2.1 | S243 | freetz101 body | `:7` `+#define AVM_LE 2`; `:8` `+#define AVM_BE 3`; `:17` the byte-order condition; `:18` `#define TARGET_FORMAT_BYTE_ORDER __LITTLE_ENDIAN` | `located=4 missing=0 sha256=e28b3341…4c707` | 0 |
| R2.2 | S245 | unblob body | `:40` `case Endian.BIG, 4:`; `:48` `is_avm = header.bytes_used == header.mkfs_time`; `:53` `case Endian.LITTLE, _:`; `:54` `commands_args.append("-le")`; `:455` `NAME = "squashfs_v4_le"`; `:463` `68 73 71 73 [24] 04 00` | `located=6 missing=0 sha256=2d7b901b…599287` | 0 |
| R2.3 | S249 | licence body | `:850` "The licensee may create only one copy of the software, which may be used exclusively for backup use." (18 words) | `located=1 missing=0 sha256=6c601b34…070a7` | 0 |
| R2.4 | S244 | 7581 index body | `:5` `FRITZ.Box_7581-07.18.image</a>  19-Aug-2024 12:33  32010240` | `located=1 missing=0 sha256=c1dd76d6…6248589` | 0 |

## R3 — census (lane's own script; read-only)

    bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku

| # | what | exit | result |
|---|---|---|---|
| R3.1 | re-run at the attempt-2 base | 0 | 19 lines, 18 `W04`, final `kaidoku ok …/corpus/SOURCES.md`; `diff` against `.ufo/waves/round-50/l1/sources-census-start-attempt2.txt` → exit 0 (byte-identical) |
| R3.2 | `census` mode at the base | 0 | rows 152, tier.A 139, tier.B 8, tier.C 5, status.mined 143, status.rejected 9 |
| R3.3 | after-state simulation (scratch tree: the four L1-drafted rows + the entry, symlinked corpus) | 0 | rows 156, tier.A 142, tier.B 9, tier.C 5, status.mined 147, status.rejected 9; 19 `W04` (the new one is S245's URL across scopes); no `E`-code |
| R3.4 | mutant: the four rows' `used-by` names a path that does not exist | 1 | `E11` ×4 (S243, S244, S245, S249) |
| R3.5 | mutant: S245's `scope` cell replaced by S112's scope cell (byte-copy) | 1 | `E04 S245 duplicate url … within scope …` — the S245 scope must differ from S108's and S112's |

## R4 — frozen bytes and the counter

    git diff --stat 435d41fd4ad9211d1579fc447936fb33d2b74467 f890bbead20ca2c549487167f56876ae47f1e1a4 \
        -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs

| # | what | exit | result |
|---|---|---|---|
| R4.1 | frozen C1 paths, freeze → attempt-2 base | 0 | empty diff — the frozen bytes are unchanged |
| R4.2 | `git show 435d41fd:tools/round-50/c1-counter.py \| grep -nE '^ENTRY\|^STEM'` | 0 | `377:ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'` / `378:STEM = '2026-10-28-r50-avm-le-squashfs-core'` |
| R4.3 | `python3 -I -B tools/round-50/c1-counter.py --root . --selftest` (in the scratch clone at the base) | 0 | `{"selftest": "c1-counter", "cases": 169, "green_ok": 17, "red_ok": 152, "path_probes": 6, "path_probes_discriminating": 3, "root_probes": 8, "spec_probes": 43}` |

## R5 — the landing-defect measurement (scratch clone, read-only in the lane)

Fixture: `git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"` then `git -C "$S/clone" checkout -q --detach f890bbead20ca2c549487167f56876ae47f1e1a4`; `git -C "$S/clone" rev-parse --show-toplevel` printed the scratch clone path before the first commit (asserted); `user.name`/`user.email` set **in that clone only**.

The frozen counter's own binding code was executed against the scratch clone's committed tree (imported as a module, `show()` bound to `git show`), so the binding result is the counter's logic, not a paraphrase.

| # | what | exit | result |
|---|---|---|---|
| R5.1 | the L1's `land_c1.py` + `land_sources.py` landing text applied verbatim (entry at the L1 stem `2026-10-28-r50-le-avm-members-core`) | 0 | `entry_present` false, `province_core_row` false, `frontier_note` false, `coverage_map_row` false, `sourced` false; only `province_core_section` true |
| R5.2 | the same tree with the stem rewritten to the counter's pin `2026-10-28-r50-avm-le-squashfs-core` | 0 | all six bindings true; `opened_source_rows = [S243, S244, S245, S249]`; `sourced` true |
| R5.3 | `python3 -I -B tools/sourced-check.py --registry … --entry …` (seat replica of the frozen `sourced` predicate) with the counter's constants | 1 | `entry_source_ids=S243,S244,S245,S249`, `opened_source_rows=` (empty), `NEAR-MISS` on all four rows, `sourced=False` |
| R5.4 | the same, with the L1's stem as the constant | 0 | `opened_source_rows=S243,S244,S245,S249`, `sourced=True` |

## R6 — id availability and collision (read-only)

| # | what | exit | result |
|---|---|---|---|
| R6.1 | ids at the attempt-2 base (`grep -cE '^ {0,3}\|\|?\s*S[0-9]{3,}'`-equivalent parse of `corpus/SOURCES.md`) | 0 | 152 rows, no duplicate ids, max id S248; S243/S244/S245/S249 **free**, S246/S247/S248 present |
| R6.2 | staged ids in the merge package ≥ S240 (`grep -rhoE '\bS[0-9]{3}\b' /home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/*.md \| sort -u \| awk -F'S' '$2>=240'`) | 0 | empty — no staged id collides with S243/S244/S245/S249 |
| R6.3 | staged-vs-registry overlap re-measured at the attempt-2 base | 0 | 44 ids (S106-S149), 0 of 44 naming the same source (attempt-1 receipt `assimilation/collisions`, re-derived) |
| R6.4 | `find /home/vgpnk/Projects/shokunin/kaidoku-shokunin -maxdepth 4 -name 'considerthese*'` | 0 | empty — the directory does not exist in this lane |

## R7 — the L1's landing scripts (read-only reads of the lane tree)

| # | what | exit | result |
|---|---|---|---|
| R7.1 | `grep -nE '^STEM\|^ENTRY' .ufo/waves/round-50/l1/land_c1.py .ufo/waves/round-50/l1/land_sources.py` | 0 | both use `STEM = '2026-10-28-r50-le-avm-members-core'` — **not** the counter's pin (R4.2) |
| R7.2 | `os.path.isdir('/fast/scratch/hyaku/kaidoku-r50/l1/srcs/')` and the five file names `land_sources.py` copies | 0 | the directory does **not** exist; all five files absent → `shutil.copy` raises `FileNotFoundError` before the registry is written |
| R7.3 | `land_sources.py:130` | 0 | `S = {k: S[k] for k in ('S246', 'S247', 'S248')}` — attempt 1's honest-stop filter still drops S243/S244/S245/S249 |

## R8 — the attempt-1 lesson's own receipt pointers (read-only)

| # | what | exit | result |
|---|---|---|---|
| R8.1 | `git ls-tree -r --name-only HEAD -- corpus/evidence/round-50/c1 .ufo/waves/round-50/l1/srcs` | 0 | empty — neither path exists at the attempt-2 base |
| R8.2 | `git log --all --oneline --diff-filter=A -- 'corpus/evidence/round-50/c1/**' '.ufo/waves/round-50/l1/srcs/**'` | 0 | empty — neither path was ever committed in any branch of the lane repo |
| R8.3 | `ls corpus/evidence/round-50/` | 0 | only `c2/`; the `c1/` tree the attempt-1 lesson names does not exist on disk either |
| R8.4 | `ls -d /fast/scratch/hyaku/kaidoku-r50/l1/srcs/` | 2 | absent — the L1's attempt-1 scratch was removed, so `land_sources.py`'s `shutil.copy(SRC + …)` raises `FileNotFoundError` |
| R8.5 | attempt-2 start receipt vs. attempt-1 start receipt | 0 | the attempt-2 receipt has **18** `W04` lines and **no** trailing `exit 0` line; the attempt-1 receipt had **15** `W04` lines **and** an `exit 0` line. The three extra `W04` lines are S246, S247, S248, landed in attempt 1. `diff` of the two `W04` sets: `15a16,18` (three added) |
| R8.6 | `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | rows **152** at the attempt-2 base — matches the prompt's "152 rows"; the prompt's "15 W04" describes attempt 1's receipt, not attempt 2's |

## R9 — the attempt-2 controls (the L1's own receipts, read-only)

Read from `.ufo/waves/round-50/controls-attempt2/` (the L1's seat C1ControlsBuild wrote them; this seat did not run REA and did not modify them).

| # | what | exit | result |
|---|---|---|---|
| R9.1 | `controls-attempt2/summary.json` — the scored controls | 1 (the driver returns 1 when a control misbehaved) | CTL-C1-0/1/2/4 `as_expected`; **CTL-C1-POS `misbehaved`, "expected exit 0, got 1", exit 1, `carriers_matched 2`; `kill_rule_fires: false`, `kill_rule_detail: []`; `unevaluated: []`; `failures: ["CTL-C1-POS"]`; `fixtures_verified_against_freeze: 21`** |
| R9.2 | `controls-attempt2/pos/counter.json` — the POS counter output | — | `carriers_matched 2`, `target 4`, `met_target false`, `exit_code 1`, `frozen_path_changed []`, `failing: ["g7581:gaps_ok", "g7582:gaps_ok"]`; all six documentation bindings **true** (`entry_present`, `province_core_row`, `frontier_note`, `coverage_map_row`, `sourced`, `province_core_section`); `gaps_note` for both g7581 and g7582: "required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0' … 'dev/pts/7']"; `nonregular_kinds: [char-device, dir, symlink]`, `nonregular_entries 1001`, `nonregular_published []` |
| R9.3 | the frozen `tools/round-50/gap-rule.json` at the freeze | 0 | `required: {symlink: true, char-device: true, …}`, `removed.silent: {char-device: ["247:0"]}`, `removed.kinds: [symlink]`, `removed.diagnostic: MaliciousSymlinkRemoved` |
| R9.4 | the frozen oracle tables at the freeze (`git show 435d41fd:tools/round-50/oracle/<id>.nonregular.tsv`) | 0 | char-device rows: c6430 **1** (`247:0`), c6490 **1** (`247:0`), g7581 **13** (`136:0…136:7`, `230:0`, `247:0`, `3:0…3:2`), g7582 **13** (same) — unchanged at the tip (`git diff --stat 435d41fd HEAD -- tools/round-50/oracle/` empty) |
| R9.5 | **reproduction with the frozen counter's own code**: `disposition_check(gaps, diags, nonreg, model, 'firmware.bin_extract', output_directory)` over the frozen POS fixtures and the frozen rule | — | g7581 `False` (12 undisposed char-devices: `dev/pts/0…7` at `136:N`, `dev/tiatm` `230:0`, `dev/ttyp0…2` `3:N`; `dev/led` `247:0` is the one the rule silently admits), g7582 the same, c6490 `True` ("613 gaps (1 structural), 1 removals, 1 silent, on 913 non-regular entries"), c6430 `True` ("568 gaps (1 structural), 1 removals, 1 silent, on 823 non-regular entries") |
| R9.6 | the POS fixture envelopes' own content | — | g7581: 637 `extraction_gaps` (636 `unpublished-entry` + 1 `depth-limited`), 3 diagnostics; `grep 'dev/pts'` over the whole envelope → **no match**; `grep '136:0'` → no match. The twelve char-devices carry no disposition in the receipt, which is why the frozen rule fails them |
| R9.7 | the POS fixtures' carrier pins vs `tools/round-50/carriers.json` | 0 | all four pins equal the frozen carrier table's (`968d997d…` g7581, `a119b644…` g7582, `880370e7…` c6490, `da1c8049…` c6430) |

**Reading.** The POS red is a frozen-instrument inconsistency, not a load problem and not a counter bug: the frozen gap rule requires every char-device to carry a disposition and silently admits exactly one detail (`247:0`), while the two FRITZ!Box 7581/7582 members carry thirteen char-devices each and the REA receipt dispositions none of the other twelve. The two Cable carriers carry one char-device (`dev/led`, `247:0`) and pass. Because the gap rule and the oracle tables are both frozen paths (`tools/round-50/**` is a frozen prefix), the C1 claim cannot be made to pass on the frozen bytes for those two carriers without an unfreeze — which the attempt-2 claims forbid ("no new C1 freeze, no amendment"). **This seat did not run REA and did not modify any control receipt.**
