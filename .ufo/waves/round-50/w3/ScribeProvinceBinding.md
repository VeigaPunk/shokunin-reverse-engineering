# ScribeProvinceBinding — PROVINCE.md bindings for R50-C1 (kaidoku round 50, attempt 2, wave 3)

**Verdict: DRAFT COMPLETE — exit 0 (met).** Both requested bindings are drafted and machine-checked
offline against the **frozen counter's own** documentation-binding predicates: the `## Round-50
additions to Core` section (one table row: surface / ports-keys / probe / verified evidence) and the
`Round-50 frontier note` line. The seat's binding check exits 0 with all four documentation
bindings true (`province_core_section`, `province_core_row`, `frontier_note`, `coverage_map_row`).
Nothing was landed; the lane tree is byte-unchanged; no REA run (this wave forbids it).

Seat: `ScribeProvinceBinding` · 2026-10-29 · lane base given `f890bbead20ca2c549487167f56876ae47f1e1a4`
· lane HEAD observed at write time `6f4aba635fc47b5823ed42afe9c8b5dc3e28127f` (the L1's stem
correction, see F1) · C1 freeze `435d41fd4ad9211d1579fc447936fb33d2b74467`.

## Artifacts (all under my seat directory; receipts inside)

| path | sha256 | what |
|---|---|---|
| `.ufo/waves/round-50/w3/ScribeProvinceBinding/province.md` | `a98f4130b3a55fd22d69013b6c8cacafbdc716b634eb104b605f415b3de9d453` | the draft: paste-ready `## Round-50 additions to Core` block (table + one-line frontier note), the companion-binding table, the rejected variant and the scope limits |
| `.ufo/waves/round-50/w3/ScribeProvinceBinding/check-bindings.py` | `f5c50c161ad4056bf162ebbfb50da64dc51998125125297a81ea7cf91c113308` | offline checker: imports the byte-frozen counter for its constants/regexes/`section`/`cells` and applies the counter's own predicates to the draft text (no REA, no network, no lane write) |
| `.ufo/waves/round-50/w3/ScribeProvinceBinding/receipts.md` | `1f4a743a139516a3dade6f7b36f8ec5aab483a9a523b140eb20572d0cc495b10` | 15 receipts: exact argv, exit code, UTC start/end, stdout sha256, stdout |
| `.ufo/waves/round-50/w3/ScribeProvinceBinding/run-receipts.py` | `47722a833743953a06e5cc46d5c142cf8f700bd0b80536ec9182d98d3568f083` | the receipt runner (read-only commands only) |

The checker's own numbers (receipt 14, exit 0):
`draft_bindings = {province_core_section: true, province_core_row: true, frontier_note: true,
coverage_map_row: true}`, `note_is_one_line: true`, `draft_block_lines: 7`;
`variant_b_attempt2_stem_bindings = {province_core_section: true, province_core_row: false,
frontier_note: false, coverage_map_row: false}`.

## Findings

| id | finding | evidence (command · exit · sha256 / observed) | confidence |
|---|---|---|---|
| F1 | **Entry-stem drift, already corrected by the L1.** At the base I was given, the frozen counter and the attempt-2 declaration named different entries: the counter pins `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, the declaration's first draft named `corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md`. The counter reads that path in four documentation bindings plus the SOURCES `used-by` check, so the attempt-2 stem would have failed four bindings and made C1 exit 1 on naming alone. The L1 committed `6f4aba63` ("attempt-2 claims corrected — entry stem pinned to the frozen counter constants") while this seat worked; **my draft follows the frozen stem**, and the rejected variant is kept in the draft as the measured consequence. | `grep -n -e ^ENTRY -e ^STEM … tools/round-50/c1-counter.py` · exit 0 · stdout `db45e7c3585d0016a1ecb4752311ac484db1a660b415088dc8177cc2149c7731` (`:377 ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'`, `:378 STEM = '2026-10-28-r50-avm-le-squashfs-core'`); `grep -n r50-le-avm-hsqs-core plans/round-50-attempt2-claims.md` · exit 0 · `df657c23cf93e33e1bbd03782cf98579e1ddca7dc7616013afb86abf9072db91` (now the correction sentence); `git -C LANE show 435d41fd:tools/round-50/c1-counter.py` · exit 0 · `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` (identical to the working copy, receipt 3/4) | observed |
| F2 | **The frontier note must be one physical line.** The counter searches `prov_text.splitlines()` for a single line carrying `Round-50 frontier note`, the entry stem and an `LE AVM`/`AVM LE` token; a note wrapped over two lines fails the binding. The round-49 note above is one line for the same reason; my draft keeps that shape (`note_is_one_line: true`). | `grep -n -e ^FRONTIER_MARK -e ^LE_AVM_RE …` (receipt 5) · exit 0 · `db45e7c3585d0016a1ecb4752311ac484db1a660b415088dc8177cc2149c7731` (`:380 FRONTIER_MARK = 'Round-50 frontier note'`, `:428 LE_AVM_RE = re.compile(r'\bLE[ _-]AVM\b\|\bAVM[ _-]LE\b', re.IGNORECASE)`); binding check receipt 14 · exit 0 | observed |
| F3 | **Row shape constraints** (counter `c1-counter.py:2444-2449`): the row's **first cell** must name `squashfs_v4_le` (word-boundary regex), the row text **outside the entry path** must spell the AVM marker (`AVM[ _-]marker`), and the frozen entry path must appear **verbatim** in the row. My row satisfies all three; the checker's `province_core_row: true` is the proof. | receipt 14 · exit 0 · stdout `cf04dc93e4c7662e67b5250232046b745d750d895ba7c66fe2ebae26d28d5f16` | observed |
| F4 | **The supersede list must name six PROVINCE locations, not five.** The literal clause `LE AVM members (`hsqs`)` stands at `PROVINCE.md:394` (round-40 note), `:405` (round-41 supersede body), `:408` (round-41 note), `:430` (round-44 note), `:438` (round-49 note); the round-42 note at `:416` carries the same clause without the `hsqs` token. My note enumerates all six (round-40 note, round-41 supersede body, round-41 note, round-42 note, round-44 note, round-49 note) and says "and nothing else", matching the round-49 note's precedent. My seat prompt named only the round-40/41/42/44/49 notes. | `grep -n -o "LE AVM members (\`hsqs\`)" PROVINCE.md` · exit 0 · stdout `7a4e362dee8fbe04d15fa1f5632c4643d048c70d6e9bda438c2c046065d3ca38` (5 hits at 394/405/408/430/438); `PROVINCE.md:416` read raw (round-42 clause "LE AVM members" without `hsqs`); corroborated by `.ufo/waves/round-50/w1/C1LandingMap.md` finding (six locations, four README bullets) | observed |
| F5 | **The `sourced` binding cannot hold yet: SOURCES rows S243/S244/S245/S249 do not exist.** `corpus/SOURCES.md` has 152 rows and the only `S24x` rows are S246/S247/S248 (landed by C2). The entry's `source:` lines must cite rows that exist, are **opened 2026-10-28 or 2026-10-29**, and carry the entry path/stem in `used-by`; the counter's window is the tuple `('2026-10-28','2026-10-29')`, so a 2026-10-29-opened row is accepted even though the attempt-2 declaration's prose mentions only 2026-10-28. One integration owner is required (C2's correction rows share the file). | `grep -n "^| S24" corpus/SOURCES.md` · exit 0 · `b99c265ba4469b7ce4801b302cad85135a81010a841a626c3e4ccb9d8f6efeae`; `grep -c "^| S" corpus/SOURCES.md` · exit 0 · `a6ade98870a92fc7e8bfd6eee3662e7823131fe83fdcdab6b73af38144accd49` (152) | observed |
| F6 | **`coverage_map_row` needs a `corpus/README.md` `## Coverage map` row carrying the frozen stem** (counter `c1-counter.py:2479-2482`; the binding reads only `\|`-lines inside that section). The draft proposes the exact row text (README is not append-only; the map row is inserted inside the section). | `PROVINCE.md`/`corpus/README.md` reads; binding check (README row fed to the counter's own `section`/`cells`) receipt 14 · exit 0 | observed |
| F7 | **The Probe cell must not claim `extraction_gaps == []`** (the round-49 row's wording). The frozen gap rule allows `unpublished-entry` for symlink/char-device/fifo/socket, permits a `MaliciousSymlinkRemoved` removal at an exact path for escaping symlinks, allows `dev/led` (`247:0`) to carry no record, and allows at most one `depth-limited` gap with zero `unknown-chunk-handler`. The four frozen oracles hold 639/639/613/568 symlinks and 13/13/1/1 char devices, so gaps are expected on a healthy run. My Probe cell states the gap rule instead of an empty-gap claim. | `cat tools/round-50/gap-rule.json` · exit 0 · `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef`; oracle kind counts · exit 0 · `8f541002bd25e73e79c51a7d84309f19c3793182255b8921d4beb2bec59823a2`; oracle file counts · exit 0 · `d68c9fa014f1fc66d043807d1a9551c059d29aae6b962fe1a36ddfe8d5474884` (4556/4564/4709/3955 regular files) | observed |
| F8 | **Two claims the row must not make.** (a) The AVM marker proves nothing about origin: unblob 26.6.4's LE branch never reads `mkfs_time == bytes_used` (the counter's docstring says so: "The marker is invisible to unblob … the claim is 'REA publishes every oracle file of the pinned LE AVM members'"), so the Ports/keys cell says the marker is a constant of the pinned bytes, not a routing input. (b) The ~13k-file LE AVM rootfs members (FRITZ!Box 7530/7590 08.25) stay Frontier — REA's fixed 120 s `provider_timeout` fired on them at host load 42–54 — so the Surface cell excludes them and the frontier note lists them as still Frontier. | `tools/round-50/c1-counter.py` docstring lines 53-63 (read); `plans/round-50-claims.md` "Carrier swap, before the freeze" paragraph (read); `tools/round-50/carriers.json` `rea_parameters` (`max_depth 1`, `max_output_bytes 536870912`, `max_output_files 100000`) | observed (prose read) |
| F9 | **Two REA command shapes exist and the row names both.** The data harness runs `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 --max-output-bytes 536870912 --max-output-files 100000 <carrier> <extract>`; the counter's own rerun uses **node on the package at `--pkg65`** (no `npx`, no ambient PATH). My Probe cell states both so the L1's data arm and the counter's rerun are the same measurement. | `tools/round-50/c1-run.sh` header and `after` arm (read); `tools/round-50/c1-counter.py:288-298` (read) | observed |
| F10 | **PROVINCE.md is append-only**: the block must be appended at EOF after the round-49 note (the round-49 POS builder enforces prefix byte-preservation); `corpus/README.md` is **not** append-only — the map row goes inside `## Coverage map`. | `.ufo/waves/round-50/w1/C1LandingMap.md` items 1-2 and 8 (read); `PROVINCE.md` ends at line 438 (read) | observed |

## Conflicts (verbatim, for the canonical Rust judge)

1. Frozen instrument vs attempt-2 declaration (first draft), attempt-2 claims `f890bbea:106`:
   `3. C1: controls-attempt2 receipts, data run, entry `corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md``
   vs frozen counter `tools/round-50/c1-counter.py:377-378`:
   `ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'` /
   `STEM = '2026-10-28-r50-avm-le-squashfs-core'`
   — **resolved by the L1** in `6f4aba63`, which states: `this file's first draft wrongly named a
   `2026-10-29-r50-le-avm-hsqs-core` stem and is corrected by this commit before any data — the
   counter, not this file, is the rule`. My draft follows the counter.
2. The attempt-2 declaration's corrected prose names the counter's constants as `entry`/`stem`,
   `core_heading`, `frontier_mark`, `opened` `2026-10-28`, `prov_base`
   `/fast/scratch/hyaku/kaidoku-r50`; the frozen counter's actual names are the module constants
   `ENTRY`, `STEM`, `CORE_HEADING`, `FRONTIER_MARK`, `OPENED_DATES = ('2026-10-28','2026-10-29')`,
   `PROV_BASE = '/fast/scratch/hyaku/kaidoku-r50/'`. The prose is a pointer, not a rename, so the
   counter is the rule — but note that the counter's opened window **includes 2026-10-29**, which
   the prose's single day does not express.

## Out of scope / not run (stated, not implied)

- **No REA run.** Forbidden this wave; the L1 alone runs the controls and the C1 data run in a
  quiet window. Nothing in the draft asserts an extraction, a handler name from a receipt, or a
  4/4 score — those are `<REV>` / counts marked **FILLED-AT-LANDING**.
- **The counter's own `--selftest` was not run** (my task did not name it; it is the L1's gate).
  I used a separate offline checker that reuses the counter's constants and predicates only.
- **No downloads, no carrier fetch, no vendor bytes** anywhere: the draft cites hashes, listings
  and the chain pin only (`tools/round-50/carriers.json`), so nothing AVM-licensed entered the
  lane tree.
- **No lane write outside my seat directory**: `PROVINCE.md`, `corpus/`, `SKILL.md`, `plans/`,
  `tools/` are untouched (`git status --porcelain` shows only untracked `.ufo/waves/round-50/…`
  paths, receipt 2 · exit 0 · `cf37fc079cbda0b60bbd58193a5d7d4953169d4d2370046e345b325fb15d608c`).
  The PROVINCE row, the frontier note, the README map row, the SOURCES rows and the knowledge
  entry are the L1's to land.
- **Not measured:** `entry_present` and `sourced` (they need the entry file and the SOURCES rows
  at a landing revision); the `coverage_map_row` check was run against the *proposed* README row,
  not a landed one.
- **Tooling:** nothing installed or upgraded (stdlib `python3` only); `pacman` untouched, as the
  host-wide pacman guard requires.

## Bounds honored

Read-only on the lane tree; the only writes are this seat's directory
`.ufo/waves/round-50/w3/ScribeProvinceBinding/` and this report file. No commit, push, stage,
stash or mutating git/jj command; only `rev-parse`, `status --porcelain` and
`show <blob>` were used. No `--data-run`, no `corpus/evidence/` write, no `.ufo/state/`, no
`agent://all`, no sibling lane touched. Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ScribeProvinceBinding`
(`TMPDIR` set to it) was removed after the receipts were copied here; the disk guard was read
before the pass (receipt 15 · exit 0 · `576ff14bc967b14caf603caca90073bc61647d85c19ba87a1f3bf4618c53af93`).
