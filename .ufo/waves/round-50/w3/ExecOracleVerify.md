# ExecOracleVerify — R50-C1 frozen-oracle spot-check (c6430)

**VERDICT: PASS — no STOP-THE-CLAIM finding. The c6430 carrier, the carve, and both frozen
oracle tables agree in every dimension I could measure without a REA run.**

Seat: `ExecOracleVerify` (wave 3, build wave). Claim: **R50-C1** (resumed; predicate frozen at
`435d41fd4ad9211d1579fc447936fb33d2b74467`). Carrier spot-checked: **`c6430`** (the smallest of
the four frozen carriers). No REA invocation, no `npx rea-agents`, no `--data-run`, no write into
the lane tree outside this report and `.ufo/waves/round-50/w3/ExecOracleVerify/`.

Scope of the check (as assigned): fetch the c6430 image, take the pinned LE tar member, carve it
to `bytes_used`, and compare **two independent readers** (`/usr/bin/unsquashfs -lls` and the lane's
`tools/round-41/sqfs-list.py --layout auto`) against the frozen
`tools/round-50/oracle/c6430.oracle.tsv` + `c6430.nonregular.tsv` — row counts equal, sha256 equal
for a deterministic 25-row sample (first 10 / last 10 / 5 hash-random) **plus all non-regular
rows**.

I measured the required sample and then the **complete tables** (3 955 regular rows, 824
non-regular rows), so the sha256 comparison here is a superset of the assignment.

---

## 1. Findings table

| # | Finding | Evidence | Status |
|---|---|---|---|
| F1 | The whole c6430 chain reproduces from the vendor URL: **image sha256**, **tar member sha256** and **carve sha256** are byte-identical to the three frozen pins in `tools/round-50/carriers.json`. | `receipts.json` → `pins` (all three `*_match: true`); observed image `52e3687d…11f5d815`, member `25194a87…dcdd4934c`, carve `da1c8049…898b46f` | **met** |
| F2 | The superblock reads exactly the frozen note string: `hsqs` (LE) v4.0, compression id 4 (xz), block_size 65536, `mkfs_time == bytes_used == 23861507` (AVM marker true). The **frozen counter's own** `layout_probe` returns `ok=true, marker=true, compression_xz=true, version_v4=true, le_magic=true, tables_sane=true`. | `counter_clauses.json` → `layout_probe`; `compare_c6430.py` (superblock decode) | **met** |
| F3 | **Row counts equal on both readers and both tables.** `unsquashfs -lls`: 4 779 entries = 3 955 regular + 255 dir + 568 symlink + 1 char-device. `sqfs-list.py --layout auto`: 3 955 files + 824 non-regular. Frozen: `c6430.oracle.tsv` = 3 955 rows, `c6430.nonregular.tsv` = 824 rows (255 dir / 568 symlink / 1 char-device). | `compare.json` → `checks.C1..C4` (`equal: true` ×4) | **met** |
| F4 | **Path sets are identical in both directions** (not just equal counts): reader-minus-frozen = 0 and frozen-minus-reader = 0 for the regular set *and* the non-regular set, for both readers. | `compare.json` → `checks.C5_paths_*` (4 checks, all `equal: true`) | **met** |
| F5 | **sha256 equality on ALL 3 955 regular rows** (the assignment asked for 25): frozen oracle ↔ `sqfs-list.py --layout auto` derivation → 0 mismatches; frozen oracle ↔ the frozen counter's own `rederive_oracle` (unsquashfs extraction + sha256 walk) → 0 mismatches, 0 frozen-only, 0 derived-only. `unsquashfs -lls` carries no hash, so on that side **all 3 955 sizes** were compared → 0 mismatches. | `compare.json` → `checks.C7_sqfsls_full_sha256`, `checks.C8_lls_full_size`; `rederive.json` (`equal: true`, 3955/3955); `counter_clauses.json` → `oracle_rederived_ok.ok` | **met** |
| F6 | The **required deterministic 25-row sample** (first 10 + last 10 + 5 hash-random by `sha256(path)`) is equal on every row, in all three columns (frozen sha256, `sqfs-list.py` sha256, `unsquashfs -lls` size). Sample rows are listed verbatim in §3. | `compare.json` → `checks.C9_sample25` (`n: 25`, `all_equal: true`) | **met** |
| F7 | **ALL 824 non-regular rows** agree on path **and** kind with the frozen table (0 kind mismatches). The kind vocabulary matches the frozen table's exactly (`char-device`, `dir`, `symlink`). | `compare.json` → `checks.C6_nonregular_kinds`, `checks.C10_all_nonregular` | **met** |
| F8 | Stronger than required: the **detail column also agrees byte-for-byte** — all 568 symlink targets as `unsquashfs -lls` prints them (`name -> target`) match the frozen table's third column, and the single char-device row's detail is `247:0` in all three views (frozen table, `sqfs-list.py`, `unsquashfs -lls` `247, 0` → major/minor). 0 differences on all 824 rows. | `compare.json` → `checks.C10_all_nonregular.rows` (detail columns compared) | **met** |
| F9 | **Inode arithmetic closes**: superblock `inodes = 4780`; the two readers together account for 4 779 entries = 3 955 + 568 + 255 + 1, i.e. every inode except the image root. No entry is hidden from either reader and no reader invents one. | `compare.json` → `lls.kinds` + superblock `inodes` (4780) | **met** |
| F10 | The **frozen counter's own frozen code** accepts these bytes and tables: `parse_oracle` → 3 955 rows, error `None` (`oracle_ok`); `parse_nonregular` → 824 rows, error `None` (`nonregular_ok`); `layout_probe.ok` (`layout_ok`); `bytes_used == ext.length == carve size == 23861507` (`carve_ok`); `rederive_oracle` set-equal (`oracle_rederived_ok`). All five C1 clauses that do not need a REA receipt are green for c6430 **using the shipped instrument, not a re-implementation**. | `counter_clauses.json` (`verdict: PASS`) | **met** |
| F11 | The frozen `gap-rule.json`'s `removed.silent` entry for `char-device` is exactly `["247:0"]`, and c6430's only char-device row carries exactly that detail — so the device node is dispositioned by the frozen *removed-silently* rule, not left as a residual gap for `gaps_ok`. | `tools/round-50/gap-rule.json` + `c6430.nonregular.tsv:63` (`dev/led  char-device  247:0`) | **met** |
| F12 | The **trailing-byte structure** is confirmed: member 23 863 304 B = squashfs 23 861 507 B + 1 789 zero bytes of 4 096-padding + the 8-byte AVM trailer `23de53c4fdf3423a`. The carve to `bytes_used` removes both, exactly as the claim text states. | superblock/trailer decode in this seat (section 3 note) | **met** |
| F13 | The carve is **safe**: reading the *uncarved* member with `sqfs-list.py --layout auto` yields tables byte-identical to the carved ones (`diff` empty, both exit 0) — both readers stop at `bytes_used`, so no trailing-byte hazard. | `sqfs.files.tsv` vs `uncarved.files.tsv`, `sqfs.nonreg.tsv` vs `uncarved.nonreg.tsv` (diff exit 0) | **met** |
| F14 | **Provenance of the tables I compared against**: every frozen input I used is byte-identical at the freeze commit `435d41fd…` and in the working tree — `carriers.json` `0d7a6336…`, `c6430.oracle.tsv` `f657ef51…`, `c6430.nonregular.tsv` `cb691b44…`, `gap-rule.json` `43f7c8d7…`, `c1-counter.py` `9820811b…`, `sqfs-list.py` `a8e633f5…`. My check therefore ran against the frozen bytes, not a mutated tree. | `git -C <lane> show 435d41fd…:<path> | sha256sum` vs `sha256sum <path>` (all `SAME`) | **met** |
| F15 | The four frozen oracle tables are **distinct per carrier** (different sha256 each); c6430 shares 2 202 path names with c6490 and 2 116 with g7581, but only 1 208 of its (path, sha256) pairs are shared with g7581 — the c6430 table is carrier-specific, not a copy of another model's table. | `sha256sum tools/round-50/oracle/*.tsv`; `comm -12` over path and (path,sha) sets | **met** |

### Disagreements found: **0**

Neither reader disagreed with the frozen tables on any row, count, path, kind, detail, size or
hash. No STOP-THE-CLAIM condition is triggered for c6430.

---

## 2. Exact commands and exit codes (all receipts carry stdout sha256 + UTC start/end)

Scratch `S=/fast/scratch/hyaku/kaidoku-r50/w3-ExecOracleVerify` (removed after the receipts were
copied here). `TMPDIR` was set to `$S` for the whole seat. Machine-readable receipts:
`.ufo/waves/round-50/w3/ExecOracleVerify/receipts.json`.

| # | Command | Exit | stdout sha256 (16) | UTC |
|---|---|---|---|---|
| 0 | `curl -sS -L --fail --max-time 300 -D headers.txt -o FRITZ.Box_6430_Cable-07.30.image "https://download.avm.de/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image"` | 0 | (image bytes) | 2026-10-29T20:34:05Z → 20:34:10Z |
| 1 | `sha256sum …/FRITZ.Box_6430_Cable-07.30.image` | 0 | `bd95f57b9af18d0c` | 20:36:10Z |
| 2 | `tar -xf …image -C …/x ./var/remote/var/tmp/x86/filesystem.image` | 0 | `e3b0c44298fc1c14` | 20:36:11Z |
| 3 | `sha256sum …/x/var/remote/var/tmp/x86/filesystem.image` | 0 | `3d893e2674183971` | 20:36:11Z |
| 4 | `head -c 23861507 …/filesystem.image > carrier.bin` (carve to `bytes_used`) | 0 | — | 20:34Z |
| 5 | `sha256sum …/carrier.bin` | 0 | `403802408305ae9f` | 20:36:11Z |
| 6 | `/usr/bin/unsquashfs -lls …/carrier.bin` | 0 | `9393f40afba610aa` | 20:36:11Z |
| 7 | `python3 -I -B tools/round-41/sqfs-list.py --layout auto --files sqfs.files.tsv --nonregular sqfs.nonreg.tsv …/carrier.bin` | 0 | `e3b0c44298fc1c14` | 20:36:11Z → 20:36:14Z |
| 8 | `python3 -I -B compare_c6430.py` (both readers vs both frozen tables) | 0 | `118128234cf8b8e6` | 20:36:14Z |
| 9 | `python3 -I -B rederive_c6430.py` (unsquashfs extraction re-derivation vs frozen oracle) | 0 | `0a161459d19927ed` | 20:36:15Z |
| 10 | `python3 -I -B counter_clauses.py` (frozen counter's own parsers / `layout_probe` / `rederive_oracle`) | 0 | `de832c3c527a3a14` | 20:36:16Z |

`unsquashfs -version` → `unsquashfs version 4.7.5 (2026/03/01)` (the version the counter pins,
`UNSQUASHFS_VERSION = '4.7.5'`).

HTTP response headers of the fetch (no `Set-Cookie` present; nothing to redact —
`artifacts/headers.txt`): `HTTP/2 200`, `content-length: 35911680`,
`last-modified: Tue, 05 Sep 2023 09:10:35 GMT`, `etag: "64f6f08b-223f800"` — the `last-modified`
and `etag` match the frozen `carriers.json` notes for c6430 exactly.

Hash pins (frozen `carriers.json` → observed):

| item | frozen | observed | match |
|---|---|---|---|
| image sha256 | `52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815` | same | ✅ |
| member sha256 | `25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c` | same | ✅ |
| carve sha256 | `da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f` | same | ✅ |

---

## 3. The required 25-row deterministic sample (all equal)

`first 10` = first 10 sorted oracle paths; `last 10` = last 10 sorted oracle paths;
`hash-random 5` = 5 rows of the middle, ordered by `sha256(path)` (deterministic, no RNG).

| path | frozen sha256 (16) | size | sqfs-list sha256 (16) | -lls size | equal |
|---|---|---|---|---|---|
| bin/aicmd | `31140cdbc69a813c` | 13592 | `31140cdbc69a813c` | 13592 | ✅ |
| bin/allcfgconv | `addd49c725875292` | 9640 | `addd49c725875292` | 9640 | ✅ |
| bin/ar7cfgchanged | `650dfbe2a5a53994` | 42 | `650dfbe2a5a53994` | 42 | ✅ |
| bin/ar7cfgctl | `c0fa3850dfa5d571` | 9416 | `c0fa3850dfa5d571` | 9416 | ✅ |
| bin/ar7cfgget | `023b8e8e773893e7` | 5288 | `023b8e8e773893e7` | 5288 | ✅ |
| bin/armconsole | `bea16edd0e7742d3` | 43 | `bea16edd0e7742d3` | 43 | ✅ |
| bin/aurachanged | `fda83a791404b2c4` | 344 | `fda83a791404b2c4` | 344 | ✅ |
| bin/auracntl | `8e8dcee913078690` | 13448 | `8e8dcee913078690` | 13448 | ✅ |
| bin/aurad | `053fa34eecf35773` | 33980 | `053fa34eecf35773` | 33980 | ✅ |
| bin/avmike | `068dd7f26b7304e9` | 208524 | `068dd7f26b7304e9` | 208524 | ✅ |
| etc/default.0255/fx_moh.default | `7cd22b0e908b4307` | 32768 | `7cd22b0e908b4307` | 32768 | ✅ |
| usr/www.myfritz/avm/resources/icons/ic_phoneInCradle_gray.svg | `cfb27f6e8f7a5512` | 1779 | `cfb27f6e8f7a5512` | 1779 | ✅ |
| usr/www/avm/css/rd/icons/ic_star_yellow.gif | `4783b8b9db26f29c` | 988 | `4783b8b9db26f29c` | 988 | ✅ |
| usr/www/avm/fon_devices/fax_overview.lua | `d19c7fcb0b198d33` | 2704 | `d19c7fcb0b198d33` | 2704 | ✅ |
| usr/www/avm/tools/import_assi_result.html | `6cc09c0b37a371ec` | 529 | `6cc09c0b37a371ec` | 529 | ✅ |
| usr/www/avm/wlan/wps_test.js | `f7c61f08fc09b815` | 3235 | `f7c61f08fc09b815` | 3235 | ✅ |
| usr/www/avm/wlan/wps_test.lua | `429501b86b604e60` | 1534 | `429501b86b604e60` | 1534 | ✅ |
| usr/www/cgi-bin/captive_pic | `b8db3cd08f23e4f1` | 9340 | `b8db3cd08f23e4f1` | 9340 | ✅ |
| usr/www/cgi-bin/capture_notimeout | `eb7a859ada6126c2` | 22064 | `eb7a859ada6126c2` | 22064 | ✅ |
| usr/www/cgi-bin/firmwarecfg | `2aecd950f28c2b98` | 58636 | `2aecd950f28c2b98` | 58636 | ✅ |
| usr/www/cgi-bin/luacgi | `01df452139dc3b8a` | 50348 | `01df452139dc3b8a` | 50348 | ✅ |
| usr/www/cgi-bin/nasupload_notimeout | `ea7a7d3a70f2a076` | 17524 | `ea7a7d3a70f2a076` | 17524 | ✅ |
| usr/www/cgi-bin/rpcstreamcap_notimeout | `6a9a9e461fa576f6` | 13636 | `6a9a9e461fa576f6` | 13636 | ✅ |
| usr/www/cgi-bin/tr064cgi | `8dd624547855fed0` | 13428 | `8dd624547855fed0` | 13428 | ✅ |
| var.tar | `7434aaef7f7d49bf` | 30720 | `7434aaef7f7d49bf` | 30720 | ✅ |

Full 3 955-row and full 824-row comparisons: `artifacts/compare.json`
(`checks.C7_sqfsls_full_sha256`, `checks.C8_lls_full_size`, `checks.C10_all_nonregular`).

Trailing-byte note (F12): member 23 863 304 B = 23 861 507 B squashfs + 1 789 zero bytes (4 096
alignment) + 8-byte trailer `23 de 53 c4 fd f3 42 3a`.

---

## 4. Risks, limits and what this seat did **not** measure

1. **One carrier of four.** Only `c6430` was checked (as assigned). `c6490`, `g7581`, `g7582`
   remain unverified by this seat; their frozen tables were only shown to be *distinct* (F15), not
   re-derived.
2. **No REA run, by contract.** Every clause that depends on a REA receipt stays unmeasured by
   this seat: `handler_ok`, `chunks_ok`, `projection_ok`, `evidence_id_ok`, `oracle_hits_ok`,
   `gaps_ok`, `nonregular_unpublished_ok`, `path_shape_ok`, `receipt_fresh`,
   `run_provenance_ok`, `parameters_ok`, `subject_pin_ok`, `operation_ok`. This seat measured only
   the carrier/layout/oracle side (`carrier_present`, `carrier_pin_ok`, `layout_ok`, `carve_ok`,
   `oracle_ok`, `oracle_rederived_ok`, `nonregular_ok`) — all seven green for c6430.
3. **`unsquashfs -lls` carries no hash.** On that reader I compared path, kind and **size** for all
   3 955 rows (0 mismatches); sha256 equality comes from `sqfs-list.py --layout auto` and from the
   unsquashfs extraction walk — two independent sha256 sources, both equal to the frozen table.
4. **Symlink targets agree here**, but the claim already discloses that the *set* of
   `MaliciousSymlinkRemoved` links depends on readdir order; my check does not re-open that limit
   (it is a `gaps_ok`/REA-side property, not an oracle-table property).
5. **Vendor bytes never entered the lane tree.** The image, the member, the carve and the
   extracted tree stayed in `$S` and `$S` was removed after the receipts and the listings were
   copied into `.ufo/waves/round-50/w3/ExecOracleVerify/`. Only hashes, listings, receipts and my
   own check drivers are in the lane tree.
6. **Host load** was 66–76 during the seat (shared fleet host). These checks are host-load
   independent (no REA, no timeout surface); they do not qualify the L1's quiet-window choice for
   the REA-dependent controls and the C1 data run.
7. **Working tree vs base revision.** The lane `HEAD` moved to `6f4aba635fc47b5823ed42afe9c8b5dc3e28127f`
   during the wave (the assignment named base `f890bbea…`). This does not affect the verdict: the
   six frozen inputs I used are byte-identical at the freeze commit `435d41fd…` and in the working
   tree (F14). I made no git mutation anywhere.

---

## 5. Artifacts (`.ufo/waves/round-50/w3/ExecOracleVerify/`)

| file | what it is |
|---|---|
| `receipts.json` | every command: exit code, stdout sha256, stdout/stderr byte counts, UTC start/end, duration; plus the three pin comparisons |
| `compare.json` | the full check result: counts, path-set diffs (both directions), the full 3 955-row sha256/size comparison, the 25-row sample, all 824 non-regular rows with kind+detail |
| `rederive.json` | unsquashfs-extraction re-derivation vs the frozen oracle (3 955/3 955, 0 diffs both directions) |
| `counter_clauses.json` | the **frozen counter's own** `parse_oracle` / `parse_nonregular` / `layout_probe` / `rederive_oracle` results on these bytes and tables |
| `lls.txt` | `unsquashfs -lls` listing of the carve (4 780 lines) — a listing, no vendor bytes |
| `sqfs.files.tsv`, `sqfs.nonreg.tsv` | `sqfs-list.py --layout auto` tables of the carve (independent re-derivation of the frozen tables) |
| `headers.txt` | the fetch's HTTP response headers (no cookies) |
| `compare_c6430.py`, `rederive_c6430.py`, `counter_clauses.py`, `make_receipts.py` | this seat's check drivers (drafts; the L1 may reuse or rewrite them) |

Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ExecOracleVerify` was removed after the copy.
No tooling was installed or upgraded by this seat (pre-existing: `/usr/bin/unsquashfs` 4.7.5,
Python 3.14.8, curl 8.23.0, GNU tar) — recorded per `/home/vgpnk/.omp/agent/RULES.md`.
