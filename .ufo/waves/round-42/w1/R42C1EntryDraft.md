**Verdict: DONE** — the four R42-C1 landing documents (knowledge entry, PROVINCE row + frontier note,
README coverage-map row + Frontier line, LOG entry skeleton) plus the SOURCES rows and the supersession
statement are drafted as text, every measured number is an explicit fill token in a 111-row fill
ledger, and the drafts are green on **two** independent gates: the round-41 gate's own matchers with the
round-42 constants patched (7/7, exit 0) and a checker with a 14-case selftest (8/8, exit 0). No lane
file was written, no carrier was fetched or run, no VCS mutation, no tool install.

Seat `R42C1EntryDraft`, round 42 wave 1 (pre-freeze). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`.
Scratch `S=/fast/scratch/hyaku/kaidoku-r42/R42C1EntryDraft`, removed at the end; everything cited was
copied into the artifacts dir first.

---

## 1. The drafts and the bindings each one satisfies

| target path in the lane | draft artifact | bindings it must satisfy |
|---|---|---|
| `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md` | `artifacts/R42C1EntryDraft/entry-corpus-knowledge-2026-10-26-r42-squashfs-v3-core.md` (16 148 B) | `entry_present`, `sourced`, `sourced_new` |
| `PROVINCE.md` `## Round-42 additions to Core` + `Round-42 frontier note` | `…/province-round42-additions.md` | `province_core_section`, `province_core_row`, `frontier_note`, and the round-41 `c1-extra` `frontier_content` shape |
| `corpus/README.md` coverage-map row, index row, `## Frontier` line | `…/readme-r42-rows.md` | `coverage_map_row` (scored), index row (practice) |
| `corpus/SOURCES.md` rows `S130`–`S134` | `…/sources-r42-rows.md` | `sourced`, `sourced_new` |
| `LOG.md` round-42 entry | `…/log-r42-entry.md` | none (record) |
| supersession statement | `…/supersession.md` | none (record; the claim requires the statement) |
| counter-port consequences | `…/port-delta.md` | none (input for the L1's port) |
| fill ledger | `…/fill-ledger.tsv` | 115 rows, one per concrete token |

Insertion points verified against the base blob, not the working tree: `PROVINCE.md` is 408 lines and
the round-41 frontier note is line 408 (the round-41 section starts at :396); `corpus/README.md`'s last
coverage-map row is line 99, its last `## Knowledge` row is line 214, and the round-41
`sasquatch-v4be` Frontier bullet is line 258.

## 2. What this seat measured (development inputs only)

All runs are on unblob 26.6.4's own SquashFS test fixtures — MIT, explicitly development inputs, never a
C1 carrier — in `$S`; text and digests copied to `dev-evidence/dev-input-evidence.txt` (67 lines,
sha256 `5cb5f9b9b480fa966874430569ea04bbdd4cda18136de07817fb72f11d77935d`).

**2.1 The extractor argv for v3, per endianness** — `unblob -d 1 <fixture> -e <out>`, exit 0, argv read
from `unblob.log`'s `Running extract command` line:

```
squashfs_v3_le.bin         exit=0  2 files  sasquatch -le -no-exit-code -f -d <out> <in>
squashfs_v3_be.bin         exit=0  2 files  sasquatch -be -no-exit-code -f -d <out> <in>
squashfs_v3_le.lzma.bin    exit=0  2 files  sasquatch -le -no-exit-code -f -d <out> <in>
squashfs_v3.le.nopad.bin   exit=0  4 files  sasquatch -le …
squashfs_v3.le.1kpad.bin   exit=0  4 files  sasquatch -le …
squashfs_v3.le.4kpad.bin   exit=0  4 files  sasquatch -le …
```

The binary is always plain `sasquatch`; `sasquatch-v4be` never appears. That matches the installed source
(S112 :25-26, :39-54, :68-69) and is the entry's headline.

**2.2 The oracle pair on v3, and its measured hole** — `unsquashfs` 4.7.5 (2026/03/01) and 7-Zip 26.04:

| fixture | `unsquashfs -s` | `unsquashfs` extract | `7z l`/`x` | digests agree |
|---|---|---|---|---|
| `squashfs_v3_le.bin` (sha256 `0161351c…`) | "Found a valid little endian SQUASHFS 3:0 superblock" | exit 0, 2 files | exit 0, 2 files | yes, both files (`apple.txt` `303980bc…`, `cherry.txt` `86baf352…`) |
| `squashfs_v3_be.bin` (`4e9493d9…`) | "Reading a different endian … valid big endian SQUASHFS 3:0 superblock" | exit 0, 2 files | exit 0, 2 files, `Big-endian = +` | yes, identical |
| `squashfs_v3_le.lzma.bin` (`2ac15e5c…`) | valid 3:0 | **exit 1**, no files: `gzip uncompress failed with error code -3` → `FATAL ERROR: read_inode` | exit 0, 2 files | **no — one reader refuses** |

So the claim's oracle premise ("both read v3") holds for gzip v3 bodies in both endiannesses and fails on
an LZMA-block v3 body; the entry states the hole and the carrier rule inherits it (Finding F3).

**2.3 v3 declares no compression** — `squashfs3_super_block` in S112 :284-315 has no compression member
(v4's struct declares `uint16 compression` at :476), and `unsquashfs -s` prints no algorithm line for a v3
image. This is the source ground for Finding F1.

**2.4 The fixture URL shape** — the media host 404s a bare tag path and serves `refs/tags/<tag>`:

```
404  …/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/…/squashfs_v3_le.bin
200  4096 B  …/media/onekey-sec/unblob/refs/tags/26.6.4/tests/…/squashfs_v3_le.bin
200  4096 B  …/media/onekey-sec/unblob/main/tests/…/squashfs_v3_le.bin
```

The claims file's fixture URL template carries the bare `26.6.4` form; C2's fixture pins (and any
rebuild command) must use `refs/tags/26.6.4`. Recorded as Finding F6.

## 3. PROVINCE text

`artifacts/R42C1EntryDraft/province-round42-additions.md` carries the verbatim block to append after base
line 408, plus the constants table it was written against. Two properties are load-bearing:

- the new row's **first cell** names the bare token `squashfs_v3` and carries five spellings of the
  format token (`little-endian SquashFS v3`, `SquashFS v3`, `v3 family`, `SquashFS version 3`,
  `squashfs_v3 family`), because the round-41 port gated the row on one case-insensitive layout regex and
  the round-42 spelling is not yet fixed;
- the **frontier note is one physical line** and names the heading `## Round-42 additions to Core`, the
  entry stem, two supersede verbs, the old phrase `coverage claim only`, and the same five format
  spellings. The heading reference is not decoration: the round-41 gate's `note_verdict` tests
  `HEADING in line`, and my first draft note — which superseded the format-matrix status in prose but did
  not quote the heading — failed exactly there (`gate-crosscheck.json` run 1, `names_heading false`).

The fallback paragraph is part of the draft: if the counter does not reach 4/4, the section must land as
a `measured, not promoted` record instead, never as a Core row.

## 4. README text

`…/readme-r42-rows.md`: three insertions, each fenced and anchored to a base line (EDIT 1 after :99,
EDIT 2 after :214, EDIT 3 after :258). EDIT 1 is the scored one; the counter's `section()` stops at the
next `## `, so a row in `## Knowledge` cannot satisfy `coverage_map_row` (round-41 F4, still true). EDIT 3
is keyed on `sasquatch` rather than `sasquatch-v4be` because the round-42 surface is the plain binary's
`-le`/`-be` leg, and it must not re-supersede the v4 chain at :254-258.

## 5. SOURCES rows

`…/sources-r42-rows.md`: base has `S001`–`S129` (`grep -c '^| S' corpus/SOURCES.md` = 129), so `S130` is
the next free id. Four publisher rows (`S130`–`S133`, one per carrier, placeholders for the publisher
document) plus `S134`, a fully specified own-work row for the v3 oracle premise with the fixture sha256s
and the dev-evidence digest — the row that makes `sourced_new` true regardless of how the publisher rows
are finally worded. Invariant stated for any renumbering: 11 cells, `opened` = `2026-10-26`, `used-by`
containing the entry path, `status` = `mined`.

## 6. Supersession

`…/supersession.md`, with base line numbers and verbatim quotes. Three dispositions, none of which edits
old text:

1. **Superseded as a status:** `corpus/README.md:92`'s "coverage claim only, never an extraction outcome"
   and the same document's caveat at `2026-10-26-unblob-format-matrix.md:38` — for the v3 handlers
   measured, by dated pointer in the PROVINCE note and the README Frontier line. The matrix row's own
   producer-coverage scope stands.
2. **Partially superseded:** `corpus/README.md:254`'s "vendor-mangled images" — only for the v3 magics a
   frozen carrier actually carries; the entry's handler matrix is a source reading, not a per-variant
   measurement.
3. **Named, deliberately not superseded:** the triage v3 table's legacy-chunk cause
   (`2026-10-26-r41-sqfs-triage-v3.md:22-24`, restated at :108-110). C1 labels no envelope, so it cannot
   supersede a label-precedence cell; that replacement belongs to R42-C2's block 21 and
   `2026-10-26-r42-sqfs-triage-v4`. The PROVINCE note says so explicitly, so the v3 coverage row cannot
   be misread as a relabelling.

Also recorded there: `plans/round-42-claims.md`'s "no REA run on a v3 chunk is in the corpus" is a
pre-round description of `corpus/evidence/`, not corpus text, and needs no corpus edit.

## 7. LOG entry

`…/log-r42-entry.md`: the round-41 bullet shape (claims / motivating evidence / controls before data /
data / scores / re-verification / wave 2 / frontier step / tool installs), every number a token, plus four
writing rules (a score bullet names counter + revision + exit code + artifact; "killed" only when the row
shows a sub-target score; commits recorded by hash and content; the installs bullet is mandatory even
when empty).

## 8. Gates run

| command | exit | result |
|---|---|---|
| `python3 -I -B check-draft.py --selftest` | 0 | `selftest_ok true`, 14 cases: baseline green + 13 single-clause mutants each dying on its intended binding (miscased heading → `province_core_section`; handler token renamed in the first cell → `province_core_row`; format tokens stripped → `province_core_row`; entry path missing → `province_core_row`; note reflowed → `frontier_note`; supersede verb dropped → `frontier_note`; old phrase dropped → `frontier_note`; coverage stem removed → `coverage_map_row`; used-by rewritten → `sourced_new`; row cell lost → `sources_rows_valid`; wrong `opened` → `sources_rows_valid`; empty token → `fill_tokens_closed`; token absent from the ledger → `fill_tokens_closed`) |
| `python3 -I -B check-draft.py --dir . --json-out check-real.json` | 0 | `met true`; all 8 bindings true; 111 fill tokens, 0 missing, 0 orphan |
| `python3 -I -B gate-crosscheck.py --selftest` | 0 | round-41 constants restored find nothing in round-42 text (2/2) |
| `python3 -I -B gate-crosscheck.py --dir . --json-out gate-crosscheck.json` | 0 | `met true`; `province_section`, `province_row`, `counter_frontier`, `extra_frontier`, `sourced_new`, `sources_row`, `coverage_row` — all computed by `git show base:tools/round-41/c1-{counter,extra}.py` **verbatim**, with only `ENTRY`/`STEM`/`CORE_HEADING`/`FRONTIER_MARK`/`HANDLER`/`HANDLER_RE`/`AVM_LAYOUT_RE`/`OPENED` and the extra's `HEADING`/`STEM`/`R40_RECORD` reassigned |

Both checkers are stdlib-only, honour `TMPDIR`/`--work`, and never write in the lane. Their green means
the documents will not fail on their tokens under a port that keeps the round-41 *shape*; it does not mean
the claim meets its target — no carrier has been fetched, receipted or scored.

## 9. Findings

**F1 (blocking for the counter port): `compression_coverage` cannot be true on a v3 carrier set.** The
round-41 clause demands one gzip-id carrier and one xz-id carrier, reading a v4 superblock field that the
v3 superblock does not have (S112 :284-315 vs :476). Kept as-is, a real 4/4 would score as a stop;
dropped silently, the round loses its decompressor binding. Recommended replacement and evidence in
`port-delta.md` D1.

**F2 (blocking if copied): `layout_ok` is the AVM check.** A port that keeps it fails every v3 carrier.
Recommended v3 structural clause in `port-delta.md` D2, with the walk sub-test marked `[INFERENCE]` and a
fallback so the L1 need not freeze an unmeasured walk. Seat `R42C1Sentinel` measured the second half of
this: the round-41 reader `tools/round-41/sqfs-list.py` exits 2 on any v3 image ("unsupported SquashFS
version 3.0, need 4.0", its line 243), and `c1-extra.py`'s `READER` is that same tool, so
`oracle_rederived` is unreachable for a v3 carrier until a v3-capable reader is frozen with the claim
(`.ufo/waves/round-42/w1/R42C1Sentinel.md` §3 B1/B2, probe-log P3). The frozen list must name that
reader — a new file, since the claim freezes the reader — and that same reader is what an
`oracle_agreement` clause needs. One more trap from the producer source, recorded in `port-delta.md` D2:
`calculate_chunk` truncates `start_offset + bytes_used` to 32 bits (S112 :82) before the padding probe,
and a tight carrier's chunk ends at `bytes_used` while a padded one ends at the 4 KiB boundary, so
`carve_ok` must allow both. Measured offsets for that reader (mine, from the fixture bytes): `s_major`
u16 at 0x1c and `s_minor` u16 at 0x1e — `b[28:30] = 03 00` on the LE fixture, `b[30:32] = 01 00` on the
1kpad fixture, which is **version 3.1**, so the frozen "major/minor" cell needs an explicit minor policy;
the v4 `compression` field at 0x14 has no v3 counterpart, and the legacy 32-bit `bytes_used_2` at 0x08 is
0 on all three fixtures. Separately, Sentinel measured the padded envelope: the 3.1 1 KiB fixture
(`bytes_used` 320) through REA `--max-depth 1` gives `chunks[0].range = 0-1024`, so the round-41
`carve_ok` (`length == bytes_used == size`) rejects a correct padded carrier — the clause needs
`bytes_used <= size <= round_up(bytes_used, 4096)` with a zero tail. Sentinel also ran the frozen
`layout_probe` itself on all four v3 fixtures: it fails *before* the magic/version tests, on the v4 read
`raw[64:72]` (`inode_table_start 72057594037928190 outside the file`), and reports `major: 768` (= 0x0300
from an unconditional big-endian read of 0x1c), `bytes_used` 1.38e19, `compression` 0 on a little-endian
v3 carrier. A `major == 3` check built on that output rejects every LE v3 carrier, and the reason text
looks like carrier corruption — it must be attributed to the tool, not the image
(`.ufo/waves/round-42/w1/R42C1Sentinel.md` §10 A8).

**F3 (oracle hole, measured): an LZMA-block v3 body defeats `unsquashfs` 4.7.5.** §2.2. Consequence for
the claim: the oracle "must agree file-for-file" is a per-carrier measurement, and a carrier whose blocks
are not gzip cannot satisfy it; the entry's Limits say so and the recommended counter clause
(`oracle_agreement`, `port-delta.md` D5) refuses it.

**F3b (correction folded in after Sentinel's final report §B3): the pairwise agreement must be scoped to
regular files.** 7-Zip's `-slt` output carries a mode but never a link target, `7z x` rewrites an absolute
link and writes an escaping relative link as a zero-byte file, and `unsquashfs` cannot read an LZMA v3 body
— so "the pair agrees file-for-file, symlinks included" is unsatisfiable on any carrier that has links.
`port-delta.md` D5 and the entry's oracle paragraph now read: two readers on the regular files, one reader
(`unsquashfs -lls`) on the non-regular table, and the gap rule accounts for the links. Their H1 (an
`unsquashfs` shim yields an identical projection), H2 (the carrier URL is never exercised at score time),
H3 (`PRIOR_CARRIERS` not frozen), H4 (`XPIN` and the npm package not frozen) and H5 (round-41 C1 receipts
read by C2, frozen by neither) are counter-provenance defects outside this seat's documents; the drafts
claim none of them.

**F4 (receipt reading): a `dependencies` cell can name `squashfs-v4be` on a pure-v3 chunk.** Every
SquashFS handler declares both binaries (S112 :68-69). The argv claim rests on source plus the unblob
logs, never on the receipt.

**F5 (freeze-integrity gap in the claim as drafted): "no extractor touched before the freeze" has no
committed evidence.** `carrier_fresh_ok` binds pins, not processes (round-41 critic's finding, still
unrepaired in the round-42 predicate). The freeze should commit the reservation record — which
`R42C1Img*` seat named which candidate URL, at what time, and the assertion that no extractor ran on it
or on anything carved from it — or the clause reads as fresh because no one wrote down the run.

**F6 (provenance defect for C2's pins): the media URL needs `refs/tags/26.6.4`.** §2.4. The claims file's
template path 404s.

**F7 (frontier-note shape): the note must quote the round-42 heading.** Measured failure of my own first
draft against the round-41 `note_verdict`; the corrected note names `## Round-42 additions to Core`, the
stem, two supersede verbs and the old phrase on one line.

**F8 (supersession boundary): the v3 table's cause cell is named, not superseded.** §6.3; the reason is in
Separability, not in politeness.

**F9 (lineage for a later v1/v2 claim): `squashfs_v1` and `squashfs_v2` inherit `SquashFSExtractor(3, …)`.**
They override only `NAME` and `PATTERNS` (S112 :101-157, :158-197); `version` is read only in the
`BIG, 4` branch, so the inherited `3` changes nothing for them, while `squashfs_v2_nonstandard` overrides
it to `2` (:204). A v1/v2 port must not read the inherited number as a version claim.

**F10 (conflict, reported verbatim for the judge): `s_major` is at 28, not 0x1e.** `R42C1Sentinel` states
that "`s_major=3` sits at 0x1e, not at 28; `layout_probe`'s `raw[28:30]` read returns 3 for these fixtures
only by coincidence of neighbouring zeros". My byte read of the same three fixtures contradicts the offset
claim: `squashfs_v3_le.bin` bytes 24..36 are `00 00 00 00 03 00 00 00 00 00 10 00`, so `b[28:30] = 03 00`
(u16 3) and `b[30:32] = 00 00`; `squashfs_v3.le.1kpad.bin` gives `b[28:30] = 03 00`, `b[30:32] = 01 00`
(3.1). Their conclusion — do not reuse v4 offsets, do not reuse `layout_probe`'s field reads — stands and is
what `port-delta.md` D2 adopts; the specific "major at 30" claim is refuted by the bytes, and a port written
to it would read `s_minor` as the major. Recorded in `port-delta.md` D9. Sentinel withdrew the offset
claim and attributed it to reading decimal 28 as the hex digits `0x1e` (§10 A4); the bytes stand as
above. Also note what their re-measurement withdrew: an earlier statement of theirs that `sasquatch`
"never tries lzma-adaptive / rc 141" was a SIGPIPE artifact of a `| head` pipe — unpiped, `sasquatch -le`
exits 0 and REA extracts the LZMA v3 fixture (handler `squashfs_v3`, 2 files). **This report never relied
on that claim**: the LZMA constraint recorded here binds the *oracle* (`unsquashfs` exit 1) only, and
`sasquatch`'s success on that fixture is consistent with the entry's extractor paragraph.

## 10. Touched surfaces

| surface | change |
|---|---|
| `.ufo/waves/round-42/w1/artifacts/R42C1EntryDraft/` | created: 7 markdown drafts, `fill-ledger.tsv`, 2 checker scripts, 4 result JSONs, `dev-evidence/dev-input-evidence.txt` |
| `.ufo/waves/round-42/w1/R42C1EntryDraft.md` | this report |
| everything else in the lane | read only (`git show` at `c4a38ea2`; plain reads of `tools/round-41/*.py`, `corpus/SOURCES.md`, and peer artifacts). No `corpus/`, `tools/`, `plans/`, `PROVINCE.md`, `README.md`, `SKILL.md`, `LOG.md` write; no VCS mutation; nothing written to `~/.local/bin` or any PATH directory |
| `/fast/scratch/hyaku/kaidoku-r42/R42C1EntryDraft` | created and removed (six fixtures, extract dirs, `unblob.log`s, 7z/unsquashfs output) |
| tools | **none installed or updated** (channel order not needed: `unsquashfs` 4.7.5, 7-Zip 26.04, unblob 26.6.4, sasquatch 4.5.1 were already on the host and were only read/run) |

Artifact digests:

```
f6b95031dc5a543a82a045dbd2f90a9b9fb9222fc327dfefa167466573fa9c4f  entry-corpus-knowledge-2026-10-26-r42-squashfs-v3-core.md
2c636aaa2223d5b4a44889a236f8be5c5a3ca5bc5c4d18def55b7c66e4e03fa1  province-round42-additions.md
a40b457f41adc363012fd6cf4dda65f0823457375fc77905e6931d79c215c422  readme-r42-rows.md
78e6acbed5dcd182cc217e3ed128ac76a7a86fa3be1a40cc0bdeaf9f4264e3ce  sources-r42-rows.md
9f9a840c8dd8755af1efe0ab5e87bb5f59e74023cac071dc9dad0a712f1f01cf  log-r42-entry.md
422f9a8b5ac90e19bafce6f9f21c9f22418a925de1d242132a66a8d0c03c94a2  supersession.md
abcfb890567da926142564e39e95ae8b67bfcc9a3a9e3a104f990f0e7aa5be43  port-delta.md
806f869102120b5ca66ba78e133a84058b9d02b81477faef09aef4fc96055a67  fill-ledger.tsv
898cfc06ea7d707c0e0f9f482ce3011db9f7f4dedcdb88979bb5d7cc520b4466  check-draft.py
41f66f0e4433c8e8d477b8f0d26ccf3ce7bf7a568a2d9533c7433c0b7856cf93  gate-crosscheck.py
a97f4162f83e1e4b18acdb81a82942a88601ad4757f0a32df67ac04a3f20481a  check-real.json
51358d39aa999b9d4c7910ac1d1b69871b3e86de1683036c506f6240e96beb70  check-selftest.json
f7752b1f77cd3c54cb28604b6fbe582dda0936baf21bcc7298f140f38d55034f  gate-crosscheck.json
579fce1ae7667e2ba34827c89959c5f8669ae087cacdfa7bce4bf5c3daecd739  gate-selftest.json
5cb5f9b9b480fa966874430569ea04bbdd4cda18136de07817fb72f11d77935d  dev-evidence/dev-input-evidence.txt
```

## 11. Out of scope for this seat

- Carrier selection, fetch, oracle construction, `carriers.json`/`gap-rule.json`, receipts, the counter
  port and its freeze, `c1-run.sh`: the `R42C1Img*` and counter seats own them; this seat only wrote the
  document slots they fill.
- R42-C2 entirely (table v4, interpreter, evaluator, generator, controls). The drafts name C2's documents
  only where a supersession boundary or a separability argument requires it.
- Whether R42-C1 lands as `met` or as an honest stop: that is the counter's verdict at the measured
  revision. The drafts carry both branches.
- Any claim about the *contents* of the published rootfs files.

## 12. Limits of this report

- Every per-carrier number in the entry is a token; nothing in the drafts asserts an extraction outcome. The
  carrier table's structure (product, member/carve, pin, handler, magic, version, oracle counts, gap rows,
  staged entries) is the fill contract, not a measurement.
- The two gates exercise *text* matchers on synthesized PROVINCE/README text built from the base blobs.
  A green here means the documents will not fail on their tokens under a port of the round-41 shape; the
  port's actual regexes are unknown, which is why both the row and the note carry five format spellings.
- The dev-input evidence comes from fixtures, not carriers: it establishes the extractor argv and the
  oracle pair's behaviour, not that any published v3 image extracts.
- `[INFERENCE]` marks: the v1/v2 inherited-extractor point (F9), the v3 metadata walk (D2 sub-test 3), and
  the 32-bit truncation's effect on a >4 GiB chunk (stated in the entry's Limits as a source observation
  with its consequence inferred).
- No tool was installed; no pacman transaction was attempted; no VCS state changed.
- **Concurrent lane movement, not mine:** the lane advanced to `fdabdfa4` ("round-42: draft claims (not frozen),
  start census, wave-1 spec/generator/dispatch") during this seat, and `plans/round-42-claims.md` now carries an
  uncommitted working-tree edit by another agent (amendment A1 to the R42-C2 precedence, generator classes, target
  bindings and controls). Every hunk of that diff is at old line ≥66, i.e. inside `## R42-C2`; `## R42-C1` runs
  lines 23-57 and is untouched, so the predicate text this seat drafted against is unchanged. `PROVINCE.md`,
  `corpus/README.md` and `corpus/SOURCES.md` are byte-identical between the spec base `c4a38ea2` and `HEAD`
  (`git diff --quiet … -- PROVINCE.md corpus/README.md corpus/SOURCES.md` → identical), so the insertion anchors
  (408 / 99, 214, 258 / 129 rows) still hold. This seat wrote none of those files.
