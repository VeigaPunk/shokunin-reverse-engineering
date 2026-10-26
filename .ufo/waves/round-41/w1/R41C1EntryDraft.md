**Verdict: DONE** — the four R41-C1 landing documents are drafted as text and every load-bearing token is
verified against the round-41 gate's own code (7/7 text bindings true, 8/8 checker cases green); every
number that only exists after the freeze runs is a `{FILL:…}` token listed in a fill ledger with its
source artifact; no lane file was written, no REA/unblob run was made, no reserved carrier was touched.

Seat `R41C1EntryDraft`, round 41 wave 1 (pre-freeze), lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `49096c7e6f226af0c750c4b003be58883cb6049f`.
Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1EntryDraft`, removed at the end; every cited file was
copied into the artifacts dir before removal. No VCS mutation, no subagent, no tool install.

---

## 1. What the claim needs, and which draft satisfies it

`plans/round-41-claims.md` R41-C1 requires four text surfaces (they are the `province_core_section`,
`province_core_row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row` bindings of
`tools/round-41/c1-counter.py` and the `frontier_content`/`sourced_new` bindings of
`tools/round-41/c1-extra.py`):

| surface | draft artifact | binding(s) it must satisfy |
|---|---|---|
| knowledge entry (14.7 KB) | `artifacts/R41C1EntryDraft/entry-corpus-knowledge-2026-10-26-r41-avm-be-squashfs-core.md` -> `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md` | `entry_present`, `sourced`, `sourced_new` |
| PROVINCE heading + row + frontier note | `…/province-round41-additions.md` | `province_core_section`, `province_core_row`, `frontier_note`, `frontier_content` |
| README coverage-map row (+ index row, + Frontier line) | `…/readme-r41-rows.md` | `coverage_map_row` |
| SOURCES row `S127` (the entry cites it) | `…/sources-r41-rows.md` | `sourced`, `sourced_new` (row absent at base, used-by naming the entry) |

The base has no round-41 text: `## Round-41 additions to Core` is absent, the entry does not exist, the
highest SOURCES id is `S126`, and `corpus/README.md` `## Frontier` ends at the round-40 `sasquatch-v4be`
line — so the counter at the base exits 1 (no receipts, no section) and the drafts are the delta.

## 2. The layout statement (entry §"The layout, from sources"), grounded this seat

Re-opened live 2026-10-26 with `curl` into scratch and hashed (no vendor bytes, public source text only):

```
$ curl -sS -o avmbe.txt   https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt
  -> 200, 1496 B, sha256 c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5
     lines 8-9  "the only data field stored in the little-endian format is the block length value at the beginning of each block"
     lines 13-14 super-block field 'mkfs_time' contains ... the same value as the super-block field 'bytes_used'
$ curl -sS -o sq.py      https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py
  -> 200, 19842 B, sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287
     lines 44-50  is_avm = header.bytes_used == header.mkfs_time ; if not is_avm: commands_args.append("-be")
$ curl -sS -o avm.patch  https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch
  -> 200, 2217 B, sha256 7f0a1b252d4bbde747efe98d1f97b52eab28d55ee957b7307d0344cbe1e220fc
     lines 7-9 new `swap_block_length`; lines 12-25 read_block swaps the 2-byte header only when set;
     lines 33-45 for TARGET_FORMAT == AVM_BE on a little-endian host swap_block_length = 0 while swap follows the magic
```

The handler hash `2d7b901b…` equals the hash the V3 seat recorded for the *installed* copy
(`.ufo/waves/round-41/w1/R41C1VendorV3.md` §2.3), so the source citation and the installed dependency are
the same bytes. The entry states the four-way separation the round-40 record already established —
marker = trigger, block-length byte order = format, `-be` = argv token, `squashfs-v4be` = binary — and it
does not re-derive round 40's evidence, it re-states it with the sources this seat re-read.

## 3. PROVINCE text (verbatim)

Append at the end of `PROVINCE.md`, after the round-40 `measured, not promoted` block and its note. The
round-40 block is NOT edited; it becomes dated history.

```markdown
## Round-41 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`) | no new REA key — unblob 26.6.4 appends `-be` to `sasquatch-v4be` only when the AVM marker `mkfs_time == bytes_used` is false (S112 lines 44-50), so a genuine AVM body runs `sasquatch-v4be` WITHOUT `-be` (S121 lines 664-669, 4389-4400); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch-v4be` 4.5.1; `extract-firmware --max-depth 1` (a vendor member exceeds the 10 000-entry staging budget at the default depth) | `extract-firmware` (rea-agents 6.5.0) on four frozen carriers no extractor touched before the freeze — V3 FRITZ!Box 5490 FRITZ!OS 07.31 member `./var/tmp/filesystem.image`, V4 FRITZ!Box 5491 FRITZ!OS 07.31 {FILL:V4 carrier = the nested filesystem_core.squashfs carved to its own bytes_used, or the wrapper member if the nested image does not fit the staging budget}, L3 lane-built AVM layout xz and L4 lane-built AVM layout gzip (both carrying in-tree and absolute symlinks and both-direction path collisions) — against the frozen reader oracle; vendor bytes fetched by `tools/round-41/fetch-vendor.py` (url -> image sha256 -> member sha256 -> carve -> pin), never committed | entry `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`; every oracle regular file published at its exact path relative to the chunk extract root with the same sha256 {FILL:V3 8/8, V4 6349/6349, L3 13/13, L4 14/14}, no regular file at a non-regular entry's exact path, gaps one `unpublished-entry` per retained symlink plus one `depth-limited`, no failed chunk, `plus-extractor` projection reproduced by the counter's own rerun; counter `tools/round-41/c1-counter.py` `carriers_matched {FILL:carriers_matched 4}` exit {FILL:exit code 0} at `{FILL:measured revision}`; receipts `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json` |

The row above supersedes the status of the block below for the genuine AVM layout only: the layout was
correctly measured in round 40, and the block's own status line was a counter false negative. A standard
big-endian body whose AVM marker was stripped stays governed by `## Round-39 additions to Core`, and
LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1 and other vendor-mangled
images stay Frontier.

Round-41 frontier note, 2026-10-26: for the genuine AVM layout the block `## Round-40 measured, not promoted (R40-C1 honest stop)` above is superseded by `## Round-41 additions to Core` (`2026-10-26-r41-avm-be-squashfs-core`); its `measured, not promoted` status came from a counter suffix false negative (R40-CL1), not from the images, and this note also supersedes the AVM sentence of the round-39 note. Still Frontier: LE AVM members (`hsqs`), AVM kernel images, nested `filesystem_core` images below depth 1, other vendor-mangled images.
```

The frontier-note line is ONE physical line on purpose: `c1-extra.py` reads a line that *starts* with
`Round-41 frontier note` and requires four clauses in it (heading string, entry stem, a supersede verb,
the phrase `measured, not promoted`). It also names the round-40 record so that a reader cannot take the
round-41 note as a silent replacement of an honest stop.

## 4. README text (verbatim)

Three edits; edit 1 is the scored one, and it must land inside the `## Coverage map` table (the counter's
`section()` stops at the next `## `, so the `## Knowledge` index row does NOT satisfy it).

```markdown
# EDIT 1 — last row of `## Coverage map`
| Genuine AVM-layout big-endian SquashFS v4 through REA (round 41) | `2026-10-26-r41-avm-be-squashfs-core` | **Core** — `extract-firmware --max-depth 1` publishes every oracle regular file at its exact path relative to the chunk extract root (no suffix matching) on four frozen carriers (V3 FRITZ!Box 5490 07.31, V4 FRITZ!Box 5491 07.31, L3/L4 lane-built with both-direction path collisions); gaps one `unpublished-entry` per retained symlink plus one `depth-limited`; repairs round-40's suffix false negative (R40-CL1) and binds `member_sha256` in the vendor fetch chain (R40-CL6) {FILL:counter `carriers_matched 4/4`, exit 0}; LE AVM members and AVM kernels stay Frontier |

# EDIT 2 — last row of `## Knowledge` (practice, not scored)
| `2026-10-26-r41-avm-be-squashfs-core` | genuine AVM-layout BE SquashFS v4 via REA, Core: big-endian fields, little-endian metadata block lengths, no `-be`; exact extract-root path matching and the `member_sha256` fetch chain | S112, S114, S124, S121, S125, S127; receipts `corpus/evidence/round-41/c1/`; counter `tools/round-41/c1-counter.py` | 2026-10-26 |

# EDIT 3 — `## Frontier`, append after the round-40 `sasquatch-v4be` line, keeping the older lines as dated history
- sasquatch-v4be — 2026-10-26 round 41: the genuine AVM layout is **Core** (`2026-10-26-r41-avm-be-squashfs-core`), superseding the round-40 `measured, not promoted` line above; that stop was a counter suffix false negative (R40-CL1), not an image property. Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.
```

## 5. SOURCES `S127` (verbatim, 11 cells)

The base's highest id is `S126`; the entry cites `S127`, so the row must land in the same freeze. The
numbers are the round-41 source seat's measured served bytes
(`artifacts/R41SrcAvm/avm-http-probe.tsv`, fetched 2026-10-26T20:23Z; cross-checked against
`artifacts/R41C1VendorV3/fetch-5490.json`). If that seat lands different text, keep only the two
invariants: `opened` = `2026-10-26`, `used-by` naming the entry.

```markdown
| S127 | AVM FRITZ!Box 5490 and 5491 FRITZ!OS 07.31 firmware download directories — https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/; https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/ (files `info_en.txt`, `info_de.txt`, `FRITZ.Box_5490-07.31.image`, `FRITZ.Box_5491-07.31.image`) | dataset | A | The vendor's own published identity for the V3 and V4 carrier images: product, FRITZ!OS version, release date, advertised file sizes, ETags and the licence notice; not the SquashFS layout of any member, not licence permission to redistribute or reverse engineer, not other models or FRITZ!OS versions | opened 2026-10-26T20:23Z: both `fritz.os/` listings HTTP 200, 574 B, sha256 `88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4` (5490) and `badbb744ff9d916fb52b4e89d6bd613009fc1b5891f115fa93b74c73583af6f7` (5491); `info_en.txt` 50 653 B sha256 `e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18` (5490) and 53 166 B sha256 `ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4` (5491), both carrying `Product:` at line 8, `Version: FRITZ!OS 7.31` at line 10 and `Release date: 09/04/2023` at line 14; image HEAD 200 with Content-Length 33 269 760 and ETag `64f592ae-1fba800` (5490), 36 392 960 and ETag `64f5a91e-22b5000` (5491); licence text at lines 665-670 (5490) and 688-693 (5491) restricts redistribution and reverse engineering | Bind the V3 and V4 carrier images to a vendor-published product and version before any layout claim, and read the licence sentence before publishing anything beyond derived metadata | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md |
```

No own-work row is drafted for the fresh carriers: their provenance is the frozen
`.ufo/waves/round-41/c1/carriers.json` plus `corpus/evidence/round-41/c1/`, and a source row exists for
opened external sources, not for a pin file.

## 6. The entry draft

Path: `artifacts/R41C1EntryDraft/entry-corpus-knowledge-2026-10-26-r41-avm-be-squashfs-core.md`
(14.7 KB, sha256 `68e20bf013aeafd68f4c79a1e67807584a0c967bdb2409c6bb85dab0e84e43fa`). It mirrors the
round-40 entry's shape (title line, `source:` lines, `verified-at`, `recheck`, then evidence sections,
then limits) with these sections:

| section | carries | grounded in |
|---|---|---|
| title + `status:` + 7 `source:` lines + `verified-at` + `recheck:` | the Core claim, `{FILL:R41-C1 verdict}` | sources re-read this seat (§2); S125/S126/S127 for carrier identity |
| The layout, from sources | the four-way separation (marker / byte order / `-be` / binary), S112 :44-50, S114 :8-9, :13-14, S124 :7-9, :12-25, :33-45, S121 :664-669, :4389-4400 | live source reads (§2) |
| The test the lane uses | LE vs BE metadata-header walk; the exact single-block identity; V3 `30231260 + 2 + 724 == 30231986`; all-BE reader exit 2; V1 dev-carrier reader output | `R41C1VendorV3/{inode-chain-walk.txt,layout-be.log}`, `R41C1Fetch/reader-real-vendor.txt` |
| The exact-path rule (R40-CL1) | the suffix rule, the L2 false positive, `extract_rel` semantics (`$input` -> `firmware.bin_extract`, nested `<p>_extract/` kept, ambiguity fails closed), prototype diff + 75-case selftest + 4/4 re-score | `.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/*` |
| Measured: four frozen carriers | per-carrier table (oracle counts measured, published/gaps as `{FILL}`), counter command, `plus-extractor` rerun, gzip+xz coverage | peer artifacts named per cell (§7) |
| Fetch chain (R40-CL6) | `member_sha256` mandatory link, red path on real bytes, V1 digests | `R41C1Fetch/vendor-chain-evidence.txt` |
| What round 40 measured and why it stopped | 3/4 at `42c10a58`, L2 clause, the honest-stop record | round-40 receipt + lesson |
| Why `--max-depth 1` | staging budget; V3 103 entries; V4 `{FILL}` (7 367 by the oracle's count = 73.7 %) | `R41C1VendorV3.md` §4, V4 oracle counts |
| Lineage | S126 image, no exit code, reproduced on vendor bytes | `R41C1VendorV3/crosscheck.txt` |
| Correction to the round-40 record | the layout was right, the status was a false negative; round-39 AVM sentence superseded for the genuine layout only | round-40 entry + PROVINCE |
| Limits | two vendor models, one FRITZ!OS generation, nested core not opened, LE `hsqs` and kernels uncovered, no argv on success, licence | sources + round-40 limits |

Carrier facts the table states as measured (oracle side only; each is a plain read of a wave-1 peer
artifact, not a run by this seat):

| carrier | counts used in the draft | peer artifact |
|---|---|---|
| V3 | 8 regular / 95 non-regular (9 dirs, 85 symlinks, 1 char device), 104 inodes, xz, carve 30 233 394, image `770efb4e…`, member `87cc5d6b…`, carve `c4f74f54…`, 0 both-direction collisions | `R41C1VendorV3/{carriers-fragment.json,collision-census.txt,oracle.tsv,nonregular.tsv}` |
| V4 | 6 349 regular / 1 017 non-regular (401 dirs, 615 symlinks, 1 char device), 7 367 inodes, xz, carrier 32 720 860 B = `bytes_used`, carrier sha256 `ce27ebca…` | `R41C1VendorV4/{carriers-V4.json,chain-walk.json,oracle.tsv,nonregular.tsv}` |
| L3 | 13 regular / 23 non-regular (20 dirs, 3 symlinks), 37 inodes, xz, 187 892 B, sha256 `04cfb4cd…`, collisions `usr/bin/busy` vs `bin/busy` and `usr/sbin/tool` vs `sbin/tool` | `R41C1LCarriers/{carriers.json,L3/*}` |
| L4 | 14 regular / 20 non-regular (17 dirs, 3 symlinks), 35 inodes, gzip, 169 545 B, sha256 `4c0e5459…` | `R41C1LCarriers/{carriers.json,L4/*}` |

The L1 must re-derive these from the frozen `oracle.tsv`/`nonregular.tsv` (they become lane files at the
freeze) rather than trust a peer artifact that a running seat may still rewrite; the counts are stable
enough to draft around but are not evidence of an extraction.

## 7. Fill ledger

`artifacts/R41C1EntryDraft/fill-ledger.tsv` — 19 unique tokens, 21 occurrences (2 tokens appear twice,
in the entry and in the PROVINCE row), one row per token with where it appears, what fills it and who
owns it. Summary:

| token | filled by |
|---|---|
| `R41-C1 verdict`, `measured revision`, `score artifact`, `counter result…`, `carriers_matched 4`, `exit code 0`, `counter carriers_matched 4/4, exit 0` | the counter run at the measured revision (JSON + exit code) |
| `V3/V4/L3/L4 published … and gaps …`, `V3/V4/L3/L4 chunk …`, `V3 8/8, V4 6349/6349, L3 13/13, L4 14/14` | the four `after.json` receipts |
| `V4 carrier = …`, `V4 staged entries` | the V4 carrier decision + its `run.json` (see finding F1) |
| `both vendor chains still resolve to their pins at the reading` | the recheck run, not the freeze |

## 8. Gates run by this seat

| command | result |
|---|---|
| `python3 -I -B gate-crosscheck.py --dir . --ports ..` | exit 0, `met: true`; 7/7 bindings true using the GATE's own helpers: `province_section` (`counter.section` on `CORE_HEADING`), `province_row` (`HANDLER_RE` on the first cell + `AVM_LAYOUT_RE` + `ENTRY`), `counter_frontier` (`FRONTIER_MARK` + `STEM` + `AVM_LAYOUT_RE`), `extra_frontier` (`extra.note_verdict` four clauses), `entry_sids` (`counter.sid_tokens`), `sources_row` (11 cells, `opened == 2026-10-26`, entry in used-by), `coverage_row` (`counter.section` on a synthesized `## Coverage map`). Port files read: `c1-counter.py` sha256 `cd454c4a…`, `c1-extra.py` sha256 `531724e1…` (in-wave versions; a later edit changes the hash, not the constants verified here) |
| `python3 -I -B check-draft.py --dir . --base-sources <base SOURCES>` | exit 0, 10/10 checks true, 21 fill tokens all closed and all listed, `S127` the only new id, 11 cells |
| `python3 -I -B check-draft.py --selftest` | exit 0, 8/8 cases: baseline green + 7 single-clause mutants each killed on its intended check (miscased heading -> `province_section`; handler token renamed in the row's first cell -> `province_row`; round-40 heading reference and phrase both removed -> `frontier_note`; heading-only removal -> `frontier_note`; used-by rewritten -> `sourced_new`; coverage row stem removed -> `coverage_row`; emptied fill -> `fill_tokens`) |

Path check at report time: `tools/round-41/` already holds `c1-extra.py`, `c1-run.sh`, `fetch-vendor.py`,
`mk-l-carriers.py`, `sqfs-list.py` (placed by the L1); `tools/round-41/c1-counter.py`,
`.ufo/waves/round-41/c1/{carriers.json,gap-rule.json}` and `corpus/evidence/round-41/c1/` do not exist yet,
which is the pre-freeze state the entry's `recheck` and counter paragraphs assume.

Not run by this seat, by rule: the counter (`tools/round-41/c1-counter.py` needs a freeze, four receipts
and a rerun on the reserved carriers), `c1-extra.py` end-to-end (needs the frozen `carriers.json`),
REA/unblob on any carrier, and any carrier build.

## 9. Findings

**F1 (blocking before the freeze): V4's carrier is still a choice, and it is a budget question.** The
wave-1 V4 artifact pins a self-contained 32 720 860-byte image (`bytes_used == size`, 7 367 inodes, 6 349
regular + 1 017 non-regular entries), while the claims' V4 line allows the 5491 wrapper member as a
fallback and says the nested image must fit REA's entry budget. 7 367 staged entries is 73.7 % of the
10 000-entry budget at depth 1 — under it, but with little margin, and no REA run may confirm it before
the freeze (reserved carriers). All three drafts therefore carry the choice as a `{FILL:V4 carrier…}`
token instead of asserting one. The freeze must pin exactly one, and `carriers.json`, the entry table, the
PROVINCE row and the README row must agree on it.

**F2: `names_r40_record` is satisfied by naming the round-40 heading, not only by stating the phrase.**
`c1-extra.py` tests `measured[,\s-]+not[,\s-]+promoted` against the note line, and the round-40 heading
`## Round-40 measured, not promoted (R40-C1 honest stop)` contains it. A copy-edit that cites the heading
and drops the sentence still passes (measured: my own mutant survived until both forms were removed). The
drafted note carries both forms, so it survives either edit, and the "supersedes" verb is stated twice
("is superseded by", "also supersedes") because one occurrence is easy to reflow away.

**F3: the `sourced`/`sourced_new` used-by test is a substring test.** A used-by cell holding the entry
stem with trailing characters passes; a cell holding only a prefix of the stem fails. Practical
consequence: `S127`'s used-by must contain the literal stem or path (it does), and a later rename of the
entry breaks the binding silently as a substring mismatch, not as a missing row.

**F4: `coverage_map_row` is scoped to the `## Coverage map` section.** The counter's `section()` ends at
the next `## `, so a row added to the `## Knowledge` index would not satisfy it; the coverage-map row is
mandatory and the index row is practice only. Both are drafted, in that order.

**F5: `province_core_row` reads the FIRST cell for the handler token.** A row that names
`squashfs_v4_be` only in a later cell fails; the drafted row puts it in the first cell inside parentheses
and repeats the AVM-layout token and the entry path in the row's own line.

**F6: the round-40 stop is documented as a test defect, not an image defect.** The entry keeps exactly
one sentence of causal claim (the L2 suffix false positive, cited to
`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`) and the prototype's own numbers (75 cases, 7 green /
68 red; 4/4 re-scored; suffix mutant dies on 3 cases), so a reader cannot mistake the repair for a
re-reading of the images.

**F7: reserved-carrier discipline held.** This seat ran no extractor on V3/V4/L3/L4 or on any AVM image,
and fetched no firmware bytes. The only network reads were three public source files (§2) and one
`git show` of the base SOURCES; the carrier numbers in the drafts are peer artifacts, each cited.

## 10. Touched surfaces

| surface | change |
|---|---|
| `.ufo/waves/round-41/w1/artifacts/R41C1EntryDraft/` | created: 7 text artifacts + 3 JSON results (below) |
| `.ufo/waves/round-41/w1/R41C1EntryDraft.md` | this report |
| everything else in the lane | read only (`git show` at `49096c7e`; plain line reads and `python3` JSON reads of wave-1 peer artifacts). No `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `README.md`, `SKILL.md`, `LOG.md` write; no VCS mutation; no PATH or `~/.local/bin` write |
| `/fast/scratch/hyaku/kaidoku-r41/R41C1EntryDraft` | created and removed (base SOURCES dump, curl outputs, selftest dirs) |

Artifacts (sha256):

```
68e20bf013aeafd68f4c79a1e67807584a0c967bdb2409c6bb85dab0e84e43fa  entry-corpus-knowledge-2026-10-26-r41-avm-be-squashfs-core.md
b31e5a8f6e26d83a335165f8dd890fe46098d980939bf471b8d1d1f13f587515  province-round41-additions.md
23d981549e2c6f11ec5ea1d76115bc5aff0f9cf2d21c22b9468c118765b97e1a  readme-r41-rows.md
b442d4e0e988ad7256f5ce433e340721ed5749ed061bc9af8b25aa2a8abe67fd  sources-r41-rows.md
f203ec2c5e7274dd1be8a2ac581b6ce029134baabd033209f1652cc6fd6755fc  fill-ledger.tsv
c89653d6f6f2897acbbecdc19ca6958f3dcb3d5c859285412523e79f2405885f  check-draft.py
48b8bf786877d4f503cfde6244e640e6f6d10a4b329583dd31a4ee6ba312c2c6  gate-crosscheck.py
ee5ebfdebaa04aab5bd55c2888679fee1092e34b3547a8dc1d577c25bcf1452f  check-real.json
1789b5e06a8bd343e4cf14e4337b2817ad97561199b338f17c475936d34c5ca3  check-selftest.json
b53e4eeb75b30dae6068aca8da7bae1e143613679edc4a12d5772db842e07d4d  gate-crosscheck.json
```

## 11. Out of scope for this seat

- R41-C2 (table v3 text, precedence labels, held-out scoring) — separate seat and separate files.
- Carrier construction, oracles, receipts, `carriers.json`/`gap-rule.json`, the counter port and its
  freeze, `c1-run.sh` execution, and the final `S127` wording (the source seat owns the row; this seat
  drafted it to keep the `sourced` binding testable).
- Any decision on whether R41-C1 lands as `met` or as an honest stop: that is the counter's verdict at
  the measured revision. If it stops, the PROVINCE section must NOT be added; the fallback text is named
  in `province-round41-additions.md`.

## 12. Limits of this report

- Every carrier number in §6 was read from a wave-1 peer artifact whose seat may still be running; none
  is an extraction outcome and none is mine. The drafts mark exactly those that need a run as `{FILL}`.
- The gate cross-check (§8) exercises the ports' text matchers on draft text, not the counters' git and
  receipt logic; a green here means the documents will not fail on their tokens, not that the claim meets
  its target.
- No REA receipt, no rerun, no score exists for the four carriers at this point, and by the reserved
  rule none can exist before the freeze.
