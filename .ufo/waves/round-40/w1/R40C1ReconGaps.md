# R40C1ReconGaps — C1 gap-rule recon on development AVM inputs

**Verdict: DONE** (gap rule derived and measured on two vendor AVM-BE images that are not V1, plus three
lane-built standard-BE carriers; **DEFECTS FOUND** in three places the freeze must absorb: the REA
staging/report budgets make default-parameter AVM carrier runs fail, the round-39 oracle cannot read the
AVM layout at all, and `gen-squashfs.py` silently drops a symlink whose target resolves to an existing
directory).

Seat: executor (leaf). Lane corpus untouched, no VCS mutation, no REA/unblob run on any C1 carrier and no
C2 held-out carrier built. Nothing written outside `.ufo/waves/round-40/w1/R40C1ReconGaps.md` and
`.ufo/waves/round-40/w1/artifacts/R40C1ReconGaps/`. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1ReconGaps`
removed at exit. **No tool installed or upgraded** (no pacman transaction; `sasquatch`, `sasquatch-v4be`,
`unblob` untouched; `npx -y rea-agents@6.5.0` resolved from the existing cache under
`~/.npm/_npx/ad9a3fdbcad992c6`).

## Axes named (Godspeed)

| axis | what this recon moves |
|---|---|
| **coverage** | freezes *which* envelopes a genuine AVM-BE carrier may produce: two new vendor AVM-BE images (7490 07.62, 7430 07.31) measured end-to-end, so the gap rule rests on 2 independent images plus lane-built controls, not on V1. |
| **depth** | the discriminating rule the corpus does not hold: the AVM layout is proven by the **metadata-chain identity** (`inode_table_start` walked with LE headers lands exactly on `directory_table_start`), not by the marker; REA's gap vocabulary is mapped to the on-disk entry classes, and the one carrier parameter that decides between a valid and an impossible receipt (`--max-depth`) is measured in both directions. |
| **calibration** | three surfaces of the draft are now measured rather than assumed: the "allowed gap kinds" set, the "publishes every regular file" clause (8/8 sha equal, plus one extra residual file), and the oracle's own capability (`sqfs-list.py` exit 2 on the layout it is supposed to read). |

## 1. Inputs, provenance, isolation

| item | value |
|---|---|
| development vendor image A | `https://download.avm.de/fritzbox/fritzbox-7490/deutschland/fritz.os/FRITZ.Box_7490-07.62.image`, HTTP 200, 38 092 800 B, sha256 `2ab05656563abe7fabdbbf62b3305123098b798e6f79c678f00baefc553f8ee9` (POSIX tar) |
| its AVM member | `./var/tmp/filesystem.image`, 35 012 616 B, sha256 `58d73b2f490a0fd22b49154382d7d5726d9813efdfae490d8cba0f12433474e5` |
| development vendor image B | `…/fritzbox-7430/deutschland/fritz.os/FRITZ.Box_7430-07.31.image`, HTTP 200, 28 856 320 B, sha256 `3dd6940c3aea429944d41508cc6c5a4e3573dae8ad9bf92e293e5bf945a6ecf4` |
| its AVM member | `./var/tmp/filesystem.image`, 25 825 288 B, sha256 `b919a6a218a57c8bf69e64baeab28bd6cb4c77bfd1fe2e8e4c1880edb9342c6c` |
| lane-built carriers | `t1` (gzip, `--endian be`, sha256 `f64b29fe…bbd5`), `t2`/`t2b` (xz, `--endian be`, `f4609aa1…4181` / `60d0e87c…fc8a`) built with `tools/round-39/gen-squashfs.py` |
| pins | `artifacts/R40C1ReconGaps/image-pins.txt`, `vendor-scan.tsv` |

Neither image is V1 (`FRITZ.Box_6490_Cable-07.57.image`); V1's bytes were never opened, copied or run.
Every REA/unblob invocation below used a development input. REA ran only through the CLI with
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` (absolute) and `cwd` inside scratch.

## 2. The AVM layout reconfirmed on two images the lane never measured

`artifacts/…/sqfs-avm-layout.txt` (BE superblock fields decoded both ways, then walked):

| image | magic | `mkfs_time == bytes_used` | first inode-table metadata header | LE / BE length | LE walk lands on `directory_table_start` | file size vs `round_up(bytes_used,4096)` |
|---|---|---|---|---|---|---|
| 7490 07.62 member | `sqsh` | **true** (35 008 578) | `24 03` | 804 / 9219 | **yes** (35006420 + 2 + 804 = 35007226) | 35 012 616 vs 35 012 608 → **+8** |
| 7430 07.31 member | `sqsh` | **true** (25 824 314) | `ec 02` | 748 / 27650 | **yes** (25822108 + 2 + 748 = 25822858) | 25 825 288 vs 25 825 280 → **+8** |

So the load-bearing layout statement in the draft holds on two fresh images: **BE superblock, AVM marker,
little-endian 2-byte metadata block-length headers**. The chain identity is exact (not a plausibility
guess) for both, and the BE reading fails it in both. `sasquatch-v4be` with **no** `-be` reads each member
(exit 0; 105 and 109 `-ll` rows), and `sasquatch-v4be -ll` also accepts them. Both are xz (compression id 4),
block size 65536, 1 fragment, 1 uid.

## 3. REA `extract-firmware` on the AVM member — measured envelope shape

Full machine table: `artifacts/…/feature-table.tsv`; envelopes: `env-7490-member-d1.json.gz`,
`env-7430-member-d1.json.gz`, `env-7490-whole-d2.json.gz`, plus the six failure envelopes.

| run | ok | REA duration / wall | envelope | chunks | `extraction_failed` | files | published bytes | unpublished | gaps | MSR | depth-limited |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7490 member, **default** (depth 3) | **false** `unreadable_output` | 2828 / 3986 ms | 588 B | — | — | — | — | — | — | — | — |
| 7490 member, `--max-depth 1` | **true** | 2305 / 3454 ms | 56 271 B | `squashfs_v4_be` 0..35012608 + handler-less 35012608..35012616 (8 B) | 0 | 9 | 36 502 270 | symlink 86 | `unpublished-entry` 86, `unknown-chunk-handler` 1, `depth-limited` 1 | **0** | 1 |
| 7490 member, `--max-depth 2` | **false** entry budget | 2582 / 3699 ms | 588 B | — | — | — | — | — | — | — | — |
| 7490 member, `--max-output-files 100000` | **false** `Report exceeded 8388608 bytes` | 20416 / 21436 ms | 3 068 B | — | — | — | — | — | — | — | — |
| 7490 whole `.image`, **default** | **false** entry budget | 2972 / 4170 ms | 588 B | — | — | — | — | — | — | — | — |
| 7490 whole `.image`, `--max-depth 1` | true | 1364 / 2086 ms | 10 582 B | `tar` 0..38092800 | 0 | 9 | 38 081 231 | none | `depth-limited` 1 | 0 | 1 |
| 7490 whole `.image`, `--max-depth 2` | true | 2226 / 3049 ms | 81 657 B | `tar`, `elf32` (var/chksum), `squashfs_v4_be`, unknown 8 B | 0 | 18 | 74 583 501 | symlink 86 | 86 + 1 + 1 | 0 | 1 |
| 7430 member, `--max-depth 1` | true | 1833 / 2802 ms | 58 182 B | `squashfs_v4_be` 0..25825280 + 8 B unknown | 0 | 9 | 26 828 008 | symlink 90 | 90 + 1 + 1 | **0** | 1 |
| 7430 member, default (depth 3) | **false** entry budget | 4216 / 5284 ms | 588 B | — | — | — | — | — | — | — | — |

The failure text is identical at both depths and on both members:
`{"code":"unreadable_output","category":"execution_failure","details":{"operation":"extract_firmware","reason":"Staging entry budget exceeded (10000)"}}`.
Raised budget, the failure moves to the report cap: `"reason":"Report exceeded 8388608 bytes; stdout (2409 bytes): ╭──…"`.

Non-regular entries in both members (from `sasquatch-v4be -ll`, `artifacts/…/sq-v4be-noflag-ll.txt`):
10 dirs, **86 / 90 symlinks**, 8 regular files, **1 character device** (`dev/led`, 247,0).

## 4. THE GAP RULE (freeze candidate, stated from these measurements)

For a genuine AVM-BE vendor member measured with `extract-firmware --max-depth 1` (default budgets),
the receipt is `ok: true`, `coverage: "partial"`, and:

- **G1 chunk rule.** Exactly two chunks: one with `handler == "squashfs_v4_be"` covering
  `[0, round_up(bytes_used,4096))` and `extraction_failed == false`, plus one handler-less chunk covering
  the trailing pad `[round_up(bytes_used,4096), file_size)`. Both measured members are `+8`, because unblob's
  squashfs handler ends a chunk at `round_up(bytes_used, max(PAD_SIZES))` when the pad bytes are zero
  (`unblob/handlers/filesystem/squashfs.py` `PAD_SIZES = [4096, 1024]`). A member with
  `file_size == round_up(bytes_used,4096)` has **one** chunk and no `unknown-chunk-handler` gap.
- **G2 gap vocabulary.** REA emits exactly six kinds (`dist/firmware/FirmwarePublication.js:239-307`):
  `missing-extractor-dependency`, `extractor-failure`, `unknown-chunk-handler`, `encrypted-chunk`,
  `depth-limited`, `unpublished-entry`. `extractor-failure` is emitted for a chunk with
  `extraction_failed == true` and for a failed extraction stage; `encrypted-chunk` for `encrypted == true`.
  For an AVM member at depth 1 the allowed set is exactly
  `{unpublished-entry × #symlinks, unknown-chunk-handler × 1 (G1 padding), depth-limited × 1}`.
  A carrier receipt carrying any other kind is a defect, not a tolerance.
- **G3 `unpublished-entry` rule.** One gap per **symlink** in the image, and only symlinks. Measured:
  86/86 (7490) and 90/90 (7430) image symlinks appear, one gap each, `relative_path` = full output-relative
  path, `link_target` = unblob's rewritten target (§5). Link count and gap count are equal in every run
  where the image has no escaping link; with escapes, `#unpublished-entry == #links − #escaping`
  (t1: 5 links → 4 gaps + 1 MSR; t2: 4 → 3 + 1; t2b: 5 → 3 + 2).
- **G4 `unknown-chunk-handler`.** One gap per handler-less chunk, i.e. the G1 residual. It is *not* an
  extraction failure: the residual is also **published as a file** (`35012608-35012616.unknown`,
  8 B, sha256 recorded in the envelope), so `len(files) == #regular_files + #unknown_chunks`.
- **G5 `depth-limited`.** Emitted per unblob task at `task.depth >= max_depth`
  (`FirmwareReports.js`, `if (record.task.depth >= context.maxDepth)`). At `--max-depth 1` that is exactly
  the chunk's carve directory → **1 gap**, `input_path` = `$output/<carve dir>`. It is not a content loss
  for the carrier itself; it is the only reason the nested `filesystem_core.squashfs` is left unopened.
  At the default depth 3 a small carrier with no nested container has **0** depth-limited gaps
  (t1/t2/t2b).
- **G6 `extractor-failure` / `encrypted-chunk` / `missing-extractor-dependency`.** None may appear.
  `sasquatch-v4be` is on the child PATH (no `-be` path taken), and the handler's `get_dependencies()`
  names both `sasquatch` and `sasquatch-v4be`; stripping `~/.local/bin` would produce
  `missing-extractor-dependency` instead of a receipt (`INFERENCE` from source; not measured this wave).
- **G7 special files are invisible.** The member's character device `dev/led` produces **no gap, no
  unpublished entry, no diagnostic, and no log line**: `sasquatch-v4be`, as non-root, leaves `dev/` empty
  (`ls -la` in `unblobs…-evidence.txt`), and REA's inventory only sees what the extractor materialized
  (`FirmwareFiles.js` entry loop: `kind` ∈ `symlink|file|special`). Directories are likewise neither
  published nor unpublished; they only count against the entry budget. So a frozen oracle that lists a
  device must not expect a corresponding gap. A materialized fifo/socket *would* appear as
  `unpublished-entry` with `kind: "special"` — `[INFERENCE]` from the same source, not measured on a
  vendor member.
- **G8 `MaliciousSymlinkRemoved` count is 0** on every vendor member measured (7490, 7430; also the
  7590 LE member's 860 links are all in-tree). Vendor AVM filesystems re-root absolute targets inside the
  tree, so no link escapes.
- **G9 coverage.** `coverage` is forced to `"partial"` whenever any entry is unpublished
  (`FirmwarePublication.js:103`). A carrier with symlinks can never report `complete`; the predicate must
  not require `complete`.
- **G10 argv is not in the envelope.** REA records **no** extractor command line. The 7490 member
  envelope's `raw_result` carries only
  `{StatReport×2, FileMagicReport, HashReport, CarveDirectoryReport, UnknownChunkReport, ChunkReport}`
  and the string `sasquatch` appears **0 times in all 13 envelopes** (`grep -c sasquatch env-*.json` → 0).
  Any "-be / no -be" claim must cite a direct `unblob -v` log, as round 39 did.
- **G11 budget envelope.** `max_output_files` (default 10000, CLI ceiling 100000) is polled over the
  *provider's* staged output — directories and links included (`FirmwareFiles.js:121-160`). Exceeding it
  yields `ok:false / unreadable_output / "Staging entry budget exceeded (10000)"` and **no chunk list at
  all**; so a carrier must stay under the budget at the frozen parameters, and the receipt format for
  "over budget" is an error envelope, not a partial receipt. Raising the budget can still fail on the
  8 MiB report cap (`FirmwareFiles.js:108`, `FIRMWARE_LIMITS.reportBytes`).

## 5. Symlinks: absolute targets are re-rooted and kept; escaping links are removed with no gap

`member-link-map.tsv` (all 86 of the 7490 member, image target → published `link_target`):

- **86/86 symlinks are `unpublished-entry`** — absolute and relative alike. **7 are absolute** and every
  one is rewritten to a **relative path from the link's own directory**, i.e. re-rooted inside the output
  tree: `sbin/notify_avmnet  /usr/sbin/notify_avmnet → ../usr/sbin/notify_avmnet`;
  `sbin/udevadm  /usr/bin/udevadm → ../usr/bin/udevadm`; `etc/mtab  /tmp/mtab → ../tmp/mtab`;
  `bin/supportdata_argo.dpm  /bin/supportdata.dpm → supportdata.dpm`;
  `sbin/showaddrs  /./sbin/showroutes → showroutes` (dot segments cleaned).
- **8 of 86 targets change**, 78 are byte-identical. The eighth is a *relative* link:
  `lib/ld-uClibc.so.0 -> ld-uClibc.so.1` is published as `ld-uClibc-1.0.32.so`, because unblob resolves
  the link chain (`extractor.py:58-65`, `target = path.resolve()`) and re-links to the final target.
  **An oracle that compares symlink targets byte-for-byte will disagree with REA; compare class
  (absolute / in-tree / escaping) and resolved in-tree endpoint instead.**
- **Escaping links produce `MaliciousSymlinkRemoved` and no gap.** Measured on lane-built BE carriers:
  absolute+dotdot `/../../../../etc/passwd` → MSR `target="../../../../etc/passwd"` (lstripped, *not*
  resolved); relative escape `../../../../../../etc/shadow` → MSR `target="/etc/shadow"` (resolved
  absolute); relative escape to a nonexistent path `../../../../../../nonexistent-xyz` → MSR
  `target="/nonexistent-xyz"`. All three: 0 extraction gaps for the link, link absent from
  `unpublished_entries`. An empty target is removed **silently** (`extractor.py:74-77`) — source-only,
  `[INFERENCE]`, not measured.
- Consequence for the rule: `MSR count == #escaping links`, and `#unpublished-entry gaps == #links −
  #escaping links`. For vendor AVM members `#escaping == 0`, so the two counts coincide — which is why
  the rule must say "one gap per *retained* link", not "per link".

## 6. Carrier parameters the freeze must fix (measured constraint, not a preference)

- At **default parameters** a vendor AVM member **cannot** produce a receipt: depth 3 descends into the
  nested `filesystem_core.squashfs` (34 MB / 25 MB) and the staged tree passes 10000 entries. Measured
  twice (7490, 7430) and on the whole `.image`.
- At `--max-depth 1` the receipt is valid, small (56–58 kB), and carries the full member tree.
- `--max-depth 2` on the member also fails (the nested image *is* extracted at depth 2).
  Whole `.image` at `--max-depth 2` succeeds and contains `handler: squashfs_v4_be` plus the member's
  86 link gaps — an alternative carrier form with the provenance chain built in (tar member list), if the
  freeze prefers not to carve.
- A member whose own tree exceeds 10000 staged entries cannot run at any depth under default budgets:
  the 7590 08.25 LE member (15 151 entries: 13 358 regular, 860 links, 933 dirs) failed at
  `--max-depth 1` with the same budget error in 3540 ms. So **V2 candidate selection must check the
  member's entry count**, or the frozen run must carry `--max-output-files`, and the counter must then
  reuse the same parameter set (the parameter block is recorded in `data.parameters`).
- Consequence for P40-C1: the committed receipt, the rerun projection and the claims text should carry
  `max_depth: 1` (and default budgets) explicitly; `data.parameters` is part of the semantic projection.

## 7. The oracle: round-39's reader refuses the AVM layout; a marker-blind AVM mode works

- `python3 -I -B tools/round-39/sqfs-list.py carved/filesystem-7490.image …` → **exit 2**,
  `sqfs-list: metadata body out of bounds: offset 35006422 length 9219, image 35012616 bytes` — it read
  the 2-byte header big-endian (`0x2403 = 9219`). The round-40 oracle **must** gain an AVM metadata mode;
  the draft's "AVM mode" is a real, currently missing feature, not a formality.
- Prototype `artifacts/…/sqfs-list-avm.py` (copy of the round-39 reader; only `meta_block` reads its
  header with the detected endianness; detection walks the inode-table chain and asks which reading lands
  exactly on `directory_table_start`, never consulting `mkfs_time`). Results:

| image | detected metadata endian | marker | regular files | symlinks | specials | escaping |
|---|---|---|---|---|---|---|
| 7490 07.62 member | **little** | true | 8 | 86 | 1 | 0 |
| 7430 07.31 member | **little** | true | 8 | 90 | 1 | 0 |
| t1 (`--endian be`) | big | false | 4 | 5 | 0 | 1 |
| t2b (`--endian be`) | big | false | 3 | 5 | 0 | 2 |
| t1 rebuilt `--endian avm` (marker-only body) | **big** | **true** | 4 | 5 | 0 | 1 |

- The prototype's publication check against the REA envelopes: **8/8 regular files matched by sha256 and
  size** on both members; all 86 / 90 oracle links present as `unpublished-entry`; the only REA-only file
  is the G1 residual (`35012608-35012616.unknown`, `25825280-25825288.unknown`).
- The marker-only image differs from `t1` in **exactly 4 bytes** (offsets 8..11, `mkfs_time := bytes_used`,
  sha256 `eb384f70…bd8e`) and is still detected as metadata-**big**: the marker alone does not make an AVM
  image, and a marker+BE pair is a *standard-BE* body that `unblob` will hand to `sasquatch-v4be` without
  `-be` (round-39 measured 0 files). For C2's `avm-marker-be-dropped`, key on the **metadata length
  endianness**, never on `mkfs_time`.

## 8. `gen-squashfs.py` defect found while building the lane carriers

`t2` was authored with five symlinks; the image contains four and `inodes 16` instead of 17. Cause: the
writer collects symlinks from `os.walk(...)`'s *file* list, and a symlink whose target resolves to an
existing directory on the build host lands in the walker's *directory* list, so it is dropped entirely
(`tmp/a/rel-dotdot-escape -> ../../../../../../..` resolves to `/fast`, which exists). Rebuilding the same
tree with a non-resolving escape target (`../../../../../../nonexistent-xyz`) produced `inodes 17` and
five links (`t2b`). **Repro:** `find t2 -printf '%y %p -> %l\n'` shows 5 links; `sasquatch-v4be -be -ll
t2-be-xz.sqsh` shows 4. Consequence for the freeze: a lane-built carrier's link set depends on the build
host's filesystem state, so carrier generation must assert the entry count against the intended tree (the
writer prints `inodes N`) and the tree must use targets that cannot resolve on the host.

## 9. What the freeze should say, minimally

1. Add to the C1 carrier note: vendor AVM members are measured at `--max-depth 1` (default budgets);
   default depth cannot produce a receipt (G11). Record `max_depth` in the projection.
2. Replace "carries only the extraction gaps the frozen gap rule allows" with G2/G3/G4/G5 explicitly:
   allowed = one `unpublished-entry` per retained symlink, one `unknown-chunk-handler` for the
   `round_up(bytes_used,4096)` residual, one `depth-limited`; nothing else; MSR = 0; device nodes yield
   no gap.
3. Say "publishes every regular file of the oracle **and may publish the G1 residual chunk file**", so
   9-vs-8 is not a mismatch; and define the oracle's symlink comparison by class, not by target bytes (§5).
4. V2 candidate menu (measured, all AVM-BE, all `+8` tail): 7490 07.62 member (`58d73b2f…`, 105 inodes) or
   7430 07.31 member (`b919a6a2…`, 109 inodes). Both need post-freeze receipts. 7590 08.25 / 7530 08.25
   are **LE** (`hsqs`) and 5590 fiber / 6660 cable ship no flat squashfs member (`fit-image`,
   `firmware-update.uimg`) — see `vendor-scan.tsv`.
5. Note in the claims that the round-40 oracle must add the AVM metadata mode; the round-39 reader exits 2
   on a genuine AVM member (§7), so a "same oracle, new carriers" assumption is false.

## 10. Not examined / risks

- V1 bytes were not read at all this wave, so V1's own staged-entry count is unmeasured; round 39 reported
  2942 regular files for the 07.57 BE member, which is safely under 10000, but the count must be confirmed
  by the freeze with `sasquatch-v4be -ll <member> | wc -l` before the carrier parameters are frozen.
  `[INFERENCE]` that V1 is under budget.
- Nested `filesystem_core.squashfs` internals (device nodes, traversal removals inside it) were only
  observed in direct `unblob -v` logs (4 `Path traversal attempt` removals in the 7430 core), never
  through REA; they are outside a depth-1 receipt.
- `missing-extractor-dependency` and `encrypted-chunk` were not produced (no such input); their emission
  conditions are read from source only.
- Empty-target symlinks are removed silently (source only).
- Nothing here was run on a frozen carrier, so no carrier receipt exists yet; all envelopes are development
  evidence.

## 11. Artifacts (all under `.ufo/waves/round-40/w1/artifacts/R40C1ReconGaps/`)

| file | contents |
|---|---|
| `feature-table.tsv` | every run: ok, duration, envelope bytes, coverage, chunks/handlers, failed chunks, files, published bytes, unpublished kinds, gap kinds, MSR, depth-limited, error reason |
| `env-7490-member-d1.json.gz`, `env-7430-member-d1.json.gz`, `env-7490-whole-d1.json.gz`, `env-7490-whole-d2.json.gz`, `env-t1-be-gzip.json.gz`, `env-t2-be-xz.json.gz`, `env-t2b.json.gz` | gzip full envelopes (success) |
| `env-member.json.gz`, `env-member-d2.json.gz`, `env-member-hi.json.gz`, `env-whole.json.gz`, `env-7430-d3.json.gz`, `env-7590le-d1.json.gz` | gzip failure envelopes (budget / report cap) |
| `sqfs-avm-layout.txt` | superblock decode both endiannesses, chain identity, residual arithmetic |
| `vendor-scan.tsv`, `image-pins.txt` | six vendor images and their members |
| `member-link-map.tsv` | 86 rows: image path, image target, published target, rewritten?, class |
| `sq-v4be-noflag-ll.txt`, `sq-7430-ll.txt` | `sasquatch-v4be -ll` (no `-be`) listings of both AVM members |
| `unblob-7490-member-evidence.txt`, `unblob-7430-member-evidence.txt` | direct `unblob -v` argv (no `-be`), special-file handling, empty `dev/` |
| `oracle-7490-*.tsv/json`, `oracle-7430-*.tsv/json` | AVM-mode oracle files/symlinks/inspect |
| `sqfs-list-avm.py` | prototype AVM-mode reader (round-39 reader + metadata-endian detection + `--meta-endian`) |
| `run-commands.txt` | every command with its exact arguments |
| `gap-rule.json`, `gap-rule-notes.md` | the counter-bindable rule (`{claim, allowed, required, structural}` keyed by the reader's non-regular kinds) and its derivation; §12 |

## 12. Counter binding: `gap-rule.json` (settled shape)

`gap-rule.json` (counter shape, fixed from the development runs only; keys use the frozen reader's
vocabulary `dir|symlink|char-device|block-device|fifo|socket`):

```json
{"claim":"R40-C1",
 "allowed": {"symlink":["unpublished-entry"], "char-device":[], "block-device":[],
             "fifo":["unpublished-entry"], "socket":["unpublished-entry"], "dir":[]},
 "required": {"symlink":true, "char-device":false, "block-device":false,
              "fifo":false, "socket":false, "dir":false},
 "structural": {"unknown-chunk-handler":1, "depth-limited":1}}
```

- `symlink → ["unpublished-entry"]`, `required: true` — measured 86/86, 90/90, and 4/3/3 minus escapes on
  the lane-built carriers.
- `char-device → []`, `required: false` — the `dev/led` char device (squashfs type 5) yields **no** gap and
  is **not** materialised (empty `dev/`, no log line), so the counter's default `required: true` would be
  wrong here; the device is the counterexample to "no gap ⇒ it was published". `block-device` (type 4) is
  absent from every measured member and encoded identically as an unmeasured branch.
- `dir → []`, `required: false` — directories never enter REA's entry list (`inventoryFirmwareOutput`
  traverses and budget-counts them but pushes only non-directories), so no gap can map to one; measured
  10 dirs per member with 0 dir gaps.
- `fifo`/`socket → ["unpublished-entry"]` with `required: false`: the gap kind is source-grounded
  (`FirmwarePublication.js:301-307` emits `unpublished-entry` for every unpublished entry), while the
  entry kind for a materialised special file would be `special`; the carrier is unmeasured, so the row is
  encoded to pass whether or not such an entry materialises.
- `structural` — `unknown-chunk-handler` (the 8-byte `round_up(bytes_used,4096)` residual) and
  `depth-limited` are mandatory for vendor members and both carry `relative_path: null`, so they are
  validated against a per-carrier allowance instead of suffix resolution. Both are 1 on every vendor
  receipt measured (member at depth 1, whole image at depth 2) and 0 on the lane-built carriers, so a
  maximum of 1 per carrier holds for every form measured here; a form outside these needs a re-frozen
  rule, not a looser one.

