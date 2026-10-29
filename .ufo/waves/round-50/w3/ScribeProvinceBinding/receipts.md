# Receipts — ScribeProvinceBinding (kaidoku round 50, attempt 2, wave 3)

Every command is read-only (lane `git` reads, greps, sha256 sums, the seat's
own offline binding check). No REA, no network fetch, no write outside this
seat directory.

| # | receipt | command | exit | UTC start | UTC end | stdout sha256 | stdout bytes |
|---|---|---|---|---|---|---|---|
| 1 | head | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` | 0 | 2026-10-29T20:36:21Z | 2026-10-29T20:36:21Z | `863f27ba40a7d473fc171fd4351b3873da3990fc3bbcb99c278b574b624a7eab` | 41 |
| 2 | status | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` | 0 | 2026-10-29T20:36:21Z | 2026-10-29T20:36:22Z | `cf37fc079cbda0b60bbd58193a5d7d4953169d4d2370046e345b325fb15d608c` | 313 |
| 3 | frozen-counter-blob | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 435d41fd4ad9211d1579fc447936fb33d2b74467:tools/round-50/c1-counter.py` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` | 244493 |
| 4 | working-counter | `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `22be8fa4e9ce41af0d68707d5609aca3e4d666db409c766604f93559141d7a3f` | 142 |
| 5 | counter-constants | `grep -n -e ^ENTRY -e ^STEM -e ^CORE_HEADING -e ^FRONTIER_MARK -e ^HANDLER_RE -e ^AVM_MARKER_RE -e ^LE_AVM_RE /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `db45e7c3585d0016a1ecb4752311ac484db1a660b415088dc8177cc2149c7731` | 440 |
| 6 | attempt2-stem | `grep -n r50-le-avm-hsqs-core /home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-50-attempt2-claims.md` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `df657c23cf93e33e1bbd03782cf98579e1ddca7dc7616013afb86abf9072db91` | 117 |
| 7 | frozen-stem-sites | `grep -rn r50-avm-le-squashfs-core /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `90a432b90e0014a242ca066caa792c35313f6c96940e7a23ab8b7c3f7dc8d677` | 2829 |
| 8 | sources-s24-rows | `grep -n ^\| S24 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `b99c265ba4469b7ce4801b302cad85135a81010a841a626c3e4ccb9d8f6efeae` | 4239 |
| 9 | sources-row-count | `grep -c ^\| S /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `a6ade98870a92fc7e8bfd6eee3662e7823131fe83fdcdab6b73af38144accd49` | 4 |
| 10 | gap-rule | `cat /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/gap-rule.json` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef` | 633 |
| 11 | oracle-kind-counts | `bash -lc for f in /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/*.nonregular.tsv; do echo "--- $f"; awk -F'\t' '{c[$2]++} END{for(k in c) print k, c[k]}' "$f"; done` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `8f541002bd25e73e79c51a7d84309f19c3793182255b8921d4beb2bec59823a2` | 514 |
| 12 | oracle-file-counts | `bash -lc for f in /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/*.oracle.tsv; do echo -n "$f "; wc -l < "$f"; done` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `d68c9fa014f1fc66d043807d1a9551c059d29aae6b962fe1a36ddfe8d5474884` | 364 |
| 13 | frontier-le-avm-sites | `grep -n -o LE AVM members (`hsqs`) /home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `7a4e362dee8fbe04d15fa1f5632c4643d048c70d6e9bda438c2c046065d3ca38` | 140 |
| 14 | binding-check | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ScribeProvinceBinding/check-bindings.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ScribeProvinceBinding/province.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:36:22Z | `cf04dc93e4c7662e67b5250232046b745d750d895ba7c66fe2ebae26d28d5f16` | 828 |
| 15 | disk-guard | `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 | 2026-10-29T20:36:22Z | 2026-10-29T20:37:02Z | `576ff14bc967b14caf603caca90073bc61647d85c19ba87a1f3bf4618c53af93` | 1983 |

## stdout of each receipt

### 1. head (exit 0)
```
6f4aba635fc47b5823ed42afe9c8b5dc3e28127f

```

### 2. status (exit 0)
```
?? .ufo/waves/round-50/controls-attempt2/
?? .ufo/waves/round-50/gen-w3.py
?? .ufo/waves/round-50/l1/sources-census-start-attempt2.txt
?? .ufo/waves/round-50/w3-dispatch.json
?? .ufo/waves/round-50/w3-spec.json
?? .ufo/waves/round-50/w3.ready
?? .ufo/waves/round-50/w3.ready.dispatched
?? .ufo/waves/round-50/w3/

```

### 3. frozen-counter-blob (exit 0)
```
#!/usr/bin/env python3
"""R50-C1 counter (coverage: genuine AVM-marker little-endian SquashFS v4 -> Core).

Port of `tools/round-41/c1-counter.py` (the R41-C1 counter, genuine AVM-layout
BIG-endian vendor carriers) to the little-endian layout, with the non-v1/v2-specific
round-49 hardening carried over (see PORT-DELTA.md for every delta). The claims
text is `plans/round-50-claims.md` R50-C1; the predicate is embedded here clause
by clause:

  At the measured revision REV, for each frozen carrier, the committed round-50
  REA 6.5.0 `extract-firmware --max-depth 1` after-receipt (unblob 26.6.4,
  sasquatch 4.5.1 on the child PATH, no `-be` binary needed), first added in a
  commit that descends from the freeze, names the `squashfs_v4_le` handler for
  the carrier's chunk with no failed chunk, publishes every regular file of the
  frozen independent oracle (unsquashfs 4.7.5 listing + per-file sha256; the
  lane's pure-Python `tools/round-41/sqfs-list.py` `auto` layout is the second
  reader that equals it) at its exact path relative to the chunk extract root
  (equality after mapping into the root, never a suffix) with the same sha256
  and size, and no extra regular file; accounts for every non-regular oracle
  entry by the frozen gap/removal rule (round-41 `gaps_ok` three-family
  disposition); has a subject digest equal to the carrier pin and recomputes
  its evidence id; the carrier bytes hash to the frozen pin and their superblock
  reads the frozen layout -- little-endian `hsqs`, v4.0, compression id 4,
  `mkfs_time == bytes_used` (the AVM marker); **and** a counter-time REA rerun
  of the same bytes (scratch output directory, carriers fetched through the
  pinned chain or the `--carrier-cache`; executed by node on the REA package at
  `--pkg65`, never through `npx`; repeated, up to 3 attempts, only when REA reports
  its own `provider_timeout`) has the same semantic projection as the
  committed receipt; **and** a scoring-time `unsquashfs` 4.7.5 re-derivation of
  the carrier bytes yields exactly the frozen oracle table (both directions);
  **and** the receipt's `parameters.output_directory` starts
  with `/fast/scratch/hyaku/kaidoku-r50/` (prefix test, no `..`); documentation
  bindings: `PROVINCE.md` holds a `## Round-50 additions to Core` section whose
  row names `squashfs_v4_le` with the AVM marker and cites the entry path; one
  line carries `Round-50 frontier note`, the entry stem and an LE-AVM token; the
  entry exists at REV and its `source:` lines cite SOURCES rows opened
  2026-10-28..2026-10-29 that list the entry in `used-by`; `corpus/README.md`
  `## Coverage map` maps the entry stem; no frozen C1 path changed after the
  freeze.

Target: carriers_matched == 4 (g7581, g7582, c6490, c6430), every binding true,
`frozen_path_changed []`, exit 0.

What the layout test is NOT (round-50 delta, deliberate): there is no big-endian
field and no little-endian-block-length special case. In the big-endian AVM layout
the metadata block headers were little-endian inside a big-endian superblock, so
the marker `mkfs_time == bytes_used` alone could not tell a genuine AVM image from
a standard BE image with a normalised timestamp and the block-length endianness was
the format test. A little-endian image has ONE byte order: `hsqs` fixes the whole
file, so the superblock reads the marker directly and the only extra tests are
sanity ones (v4.0, compression id 4, table starts inside `bytes_used`).
The marker is invisible to unblob (`SquashFSExtractor` runs `sasquatch -le` for every
little-endian image and only branches on `mkfs_time == bytes_used` for BIG-endian
v4): the claim is "REA publishes every oracle file of the pinned LE AVM members",
not "REA recognises AVM". The marker is a CONSTANT OF THE PINNED BYTES: once
`carrier_pin_ok` holds the bytes are fixed and the marker adds no evidence beyond
it; the counter does NOT claim that `layout_ok` separates genuine AVM images from
re-stamped ones (anyone can write `mkfs_time = bytes
```

### 4. working-counter (exit 0)
```
9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py

```

### 5. counter-constants (exit 0)
```
377:ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
378:STEM = '2026-10-28-r50-avm-le-squashfs-core'
379:CORE_HEADING = '## Round-50 additions to Core'
380:FRONTIER_MARK = 'Round-50 frontier note'
426:HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
427:AVM_MARKER_RE = re.compile(r'AVM[ _-]marker', re.IGNORECASE)
428:LE_AVM_RE = re.compile(r'\bLE[ _-]AVM\b|\bAVM[ _-]LE\b', re.IGNORECASE)

```

### 6. attempt2-stem (exit 0)
```
110:   first draft wrongly named a `2026-10-29-r50-le-avm-hsqs-core` stem and is corrected by this commit before any

```

### 7. frozen-stem-sites (exit 0)
```
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py:377:ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py:378:STEM = '2026-10-28-r50-avm-le-squashfs-core'
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-controls.py:245:    entry = k.get('ENTRY') or 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/pos/manifest.json:3:  "entry": "# CONTROL FIXTURE entry for 2026-10-28-r50-avm-le-squashfs-core (CTL-C1-POS plant, not the landing)\n\nstatus: control fixture\n\nsource: S990 \u2014 https://example.invalid/ctl-c1-pos \u2014 as read 2026-10-28\nverified-at: 2026-10-28\n",
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/pos/manifest.json:4:  "province_core": "## Round-50 additions to Core\n\n| Surface | Ports / keys | Probe | Verified evidence |\n|---|---|---|---|\n| genuine AVM-marker little-endian SquashFS v4 (`squashfs_v4_le`, `hsqs`, v4.0, xz, `mkfs_time == bytes_used`) | no new REA key; unblob 26.6.4 with `sasquatch` 4.5.1 on the child PATH, no `-be` binary; `extract-firmware --max-depth 1` with the staging budgets raised | CONTROL-FIXTURE TEXT (CTL-C1-POS), not the landing: AVM marker, AVM layout, entry `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` | `extract-firmware` on four frozen carriers |\n",
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/pos/manifest.json:5:  "province_frontier": "Round-50 frontier note, 2026-10-28 (CONTROL FIXTURE): genuine AVM-marker little-endian members (LE AVM, LE-AVM, AVM-LE, `hsqs`) moved Frontier -> Core with `2026-10-28-r50-avm-le-squashfs-core`. Still Frontier: AVM kernel images.\n",
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/pos/manifest.json:6:  "readme_row": "| Genuine AVM marker little-endian SquashFS v4 through REA (CONTROL FIXTURE) | `2026-10-28-r50-avm-le-squashfs-core` | **Core** (CTL-C1-POS plant; not the landing) |",
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/pos/manifest.json:7:  "sources_row": "| S990 | CONTROL FIXTURE source row \u2014 https://example.invalid/ctl-c1-pos | docs | A | plant for CTL-C1-POS only | none | nothing; a fixture row so the `sourced` binding can be true | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md |"
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/GEN-INDEX.json:7:  "entry": "corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md",
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/control-fixtures/GEN-INDEX.json:14:  "stem": "2026-10-28-r50-avm-le-squashfs-core",

--- stderr ---
grep: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/__pycache__/c1-counter.cpython-314.pyc: binary file matches

```

### 8. sources-s24-rows (exit 0)
```
156:| S246 | Stanford Encyclopedia of Philosophy, Karl Popper — https://plato.stanford.edu/entries/popper/ | docs | B | Popper falsifiability criterion | `2. Backdrop to Popper’s Thought`: "falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific" (21 words); SEP `substantive revision Fri Jul 31, 2026`; re-opened 2026-10-28 HTTP 200, 118,135 bytes, sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`, snapshot `corpus/evidence/round-49/c2/popper.html` | supersedes S147 — tier B (was tier A): CORPUS.md tier text defines B as "strong secondary (expert write-up with reproducible detail, survey, textbook)" and A as "primary or authoritative"; this entry is a named-author survey with a bibliography, so the learner cites Popper's own works for the criterion's wording; the round-49 closure `corpus/lessons/round-49-verifier-spotcheck.md` disagreed with tier A | mined | 2026-10-28 | 365d | corpus/lessons/round-50.md, corpus/lessons/round-49.md |
157:| S247 | sysexits(3) FreeBSD manual, correction of S149 — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | docs | C | The stated reason and locator of S149 only: what the FreeBSD sysexits(3) page says about the EX_USAGE gloss and where the interface first appeared | `ERRORS`: "EX_USAGE (64) The command was used incorrectly" (7 words), under `ERRORS` and not under `DESCRIPTION`; `HISTORY`: "The sysexits file first appeared in 4BSD." (7 words); re-opened 2026-10-28 HTTP 200, 59,251 bytes, byte-identical to the committed snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html`, sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` | supersedes S149 — REJECTED: S149's reason was wrong and inverted provenance: FreeBSD is the origin of sysexits (its `HISTORY` dates the file to 4BSD) and man7 is the Linux rendering, so this page is not a "second mirror" of S148; it stays rejected because S148's header already gives 64 the meaning "command line usage error" and this page adds no claim a registry row makes; flip: a claim whose verdict rests on the prose gloss beyond S148's header comment, or on the 4BSD origin, which would admit this page with locator `ERRORS` or `HISTORY` | rejected | 2026-10-28 | on-request | corpus/lessons/round-50.md |
158:| S248 | unblob 26.6.4 SquashFS `__output__` expected trees, member listings — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (contents API `https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs/<tree>/__output__?ref=26.6.4`; commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`) | dataset | A | unblob 26.6.4 upstream expected member listings, census only | committed listing snapshots (v1 3 files each, v2.0 and v2.1 4 files each per endian = 22 file entries in 4 endian trees); located names, each a `name` field of its listing: "cherry.txt" (1 words) in `corpus/evidence/round-50/c2/unblob-listings/squashfs_v1_big_endian__squashfs_v1.0_be.bin_extract.json` sha256 `588573625c5185bd94f3c53bc9f4f92925f6e0592c26435f5bc168f37c171fda`; "cherry.txt" (1 words) in `corpus/evidence/round-50/c2/unblob-listings/squashfs_v1_little_endian__squashfs_v1.0_le.bin_extract.json` sha256 `b858d860a2598a980931ef5cb86e3df106b94fd97ec3f6ff2aa3f06fdb620ad6`; "apple4.txt" (1 words) in `corpus/evidence/round-50/c2/unblob-listings/squashfs_v2_big_endian__squashfs_v2.0_be.bin_extract.json` sha256 `74807ec11dea00f18a8b8251574cce0e474384bf22c447f102962154fe09dadd`; "apple4.txt" (1 words) in `corpus/evidence/round-50/c2/unblob-listings/squashfs_v2_little_endian__squashfs_v2.0_le.bin_extract.json` sha256 `ab0918849c105b5a684efdf5518bad95b4be101496a5a7f004e744ddc33fdbcd` | supersedes S138 — the census of 22 member files (v1 3 each; v2.0 and v2.1 4 each per endian) rests on these fetched member listings, not on the directory name S138 quoted; grounds the member censu
```

### 9. sources-row-count (exit 0)
```
152

```

### 10. gap-rule (exit 0)
```
{
 "claim": "R50-C1",
 "allowed": {
  "symlink": [
   "unpublished-entry"
  ],
  "char-device": [
   "unpublished-entry"
  ],
  "block-device": [],
  "fifo": [
   "unpublished-entry"
  ],
  "socket": [
   "unpublished-entry"
  ],
  "dir": []
 },
 "required": {
  "symlink": true,
  "char-device": true,
  "block-device": false,
  "fifo": false,
  "socket": false,
  "dir": false
 },
 "removed": {
  "diagnostic": "MaliciousSymlinkRemoved",
  "kinds": [
   "symlink"
  ],
  "disposition": "exclusive",
  "silent": {
   "char-device": [
    "247:0"
   ]
  }
 },
 "structural": {
  "depth-limited": 1,
  "unknown-chunk-handler": 0
 }
}

```

### 11. oracle-kind-counts (exit 0)
```
--- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/c6430.nonregular.tsv
dir 255
symlink 568
char-device 1
--- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/c6490.nonregular.tsv
dir 300
symlink 613
char-device 1
--- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/g7581.nonregular.tsv
dir 349
symlink 639
char-device 13
--- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/g7582.nonregular.tsv
dir 349
symlink 639
char-device 13

```

### 12. oracle-file-counts (exit 0)
```
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/c6430.oracle.tsv 3955
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/c6490.oracle.tsv 4709
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/g7581.oracle.tsv 4556
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/oracle/g7582.oracle.tsv 4564

```

### 13. frontier-le-avm-sites (exit 0)
```
394:LE AVM members (`hsqs`)
405:LE AVM members (`hsqs`)
408:LE AVM members (`hsqs`)
430:LE AVM members (`hsqs`)
438:LE AVM members (`hsqs`)

```

### 14. binding-check (exit 0)
```
{
 "counter_entry_constant": "corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md",
 "counter_path": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py",
 "counter_sha256": "9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813",
 "counter_stem_constant": "2026-10-28-r50-avm-le-squashfs-core",
 "draft_bindings": {
  "coverage_map_row": true,
  "frontier_note": true,
  "province_core_row": true,
  "province_core_section": true
 },
 "draft_block_lines": 7,
 "draft_sha256": "a98f4130b3a55fd22d69013b6c8cacafbdc716b634eb104b605f415b3de9d453",
 "note_is_one_line": true,
 "variant_b_attempt2_stem_bindings": {
  "coverage_map_row": false,
  "frontier_note": false,
  "province_core_row": false,
  "province_core_section": true
 },
 "variant_b_note_is_one_line": true,
 "verdict": "ok"
}

```

### 15. disk-guard (exit 0)
```
root                             use%     free
/tmp                              23%    99.2G
/var/tmp                          41%   535.3G
/fast/scratch/hyaku               39%   490.0G

top consumers /tmp
     25.4G idle=1688  /tmp/verif-kasegi-r42
      3.8G idle=1436  /tmp/r43-work.MZlnvf
    697.0M idle=1479  /tmp/kaidoku-before
    666.6M idle=1604  /tmp/r50tip
    666.3M idle=1612  /tmp/r50clone
    665.5M idle=1612  /tmp/r50base
    420.3M idle=2942  /tmp/k57
    410.7M idle=2942  /tmp/k57b
    408.6M idle=3825  /tmp/node-compile-cache
    399.8M idle=1479  /tmp/afterchk
    390.7M idle=1479  /tmp/frz
    390.6M idle=1479  /tmp/basefull
    380.6M idle=1226  /tmp/tameshi-registry-check-nisa2gpx
    367.3M idle=4773  /tmp/.mount_KimiCogEAx7f
    367.3M idle=9468  /tmp/.mount_KimiColz3RmH

top consumers /var/tmp
    201.8M idle=4529  /var/tmp/souji-r21-replay-eq45dano
     12.4M   idle=0  /var/tmp/OptixCache_vgpnk
     11.6M idle=4530  /var/tmp/r15-census-config.3tk6qehq
     10.9M idle=1130  /var/tmp/r15-census-config.zpym7cf5
     10.3M idle=4520  /var/tmp/r15-census-config.psjsbayp
      9.8M idle=1131  /var/tmp/r15-census-config.8wrllrw0
      9.8M idle=4532  /var/tmp/r15-census-config.xec8q0wl
      7.1M idle=4529  /var/tmp/r17-census-hygiene._ke3xywa
      3.4M idle=1277  /var/tmp/souji-r18-FixtureR18Bounded.rfi_p7vx
      3.4M idle=1277  /var/tmp/souji-r18-FixtureR18Bounded.pcv_xoq1
      3.4M   idle=7  /var/tmp/souji-r18-FixtureR18Bounded.p9hrbg7v
      3.4M   idle=7  /var/tmp/souji-r18-FixtureR18Bounded.npumj1z_
      2.1M idle=3389  /var/tmp/souji-census-selftest.XXl2r7
      1.6M idle=1968  /var/tmp/souji-census-selftest.uFAiOl
      1.1M idle=4529  /var/tmp/souji-r18-FixtureR18Bounded.6bewdtxp

top consumers /fast/scratch/hyaku
      4.1G   idle=0  /fast/scratch/hyaku/kaidoku-r50
      1.9G   idle=8  /fast/scratch/hyaku/souji-r42
     31.9M   idle=8  /fast/scratch/hyaku/kasegi-r46
      2.8M   idle=0  /fast/scratch/hyaku/tabi-r43

```
