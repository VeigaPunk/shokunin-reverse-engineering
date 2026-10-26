# R36ExecIndependentC1 — independent C1 coverage checker

Seat: `R36ExecIndependentC1` (leaf, advisory). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Wave: round 36 / w1 (build drafts + first falsifiers). L1: `KaidokuR36`.

Verdict in one line: **an independently written checker that shares no code with
`tools/round-36/c1-counter.py` reproduces every per-carrier number in
`.ufo/waves/round-36/interim/c1-after-receipts-only.json` exactly (24/24 field comparisons, 0
disagreements), and independently re-derives all four frozen oracles from the raw carriers — both
oracle tables and the sasquatch-enabled receipts are faithful to real `unsquashfs` 4.7.5 output.**

## 0. What this seat measured, and what it deliberately did not

Measured revision `3310d8fa27bfaa95ad858c4aaad6f6377f853982` ("R36-C1 after receipts", parent
`6a870b9290e9566468d7d9e6d1b8308daf025b12`), freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`,
base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`. `git rev-parse HEAD` in the lane is
`d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`; the twelve measured artifacts (`after.json`, `before.json`, `oracle.tsv` for four carriers) are
byte-identical between the worktree and `3310d8f` (`git hash-object` vs `git rev-parse 3310d8f:<path>`, 12/12 SAME). Every
receipt I read came from `git show <rev>:<path>`; nothing was read from a mutable working file.

In scope (my assignment): oracle files; after files matching an oracle row by path suffix **and**
sha256; before files matching; sasquatch gaps before/after; count and identity of after files *not* in
the oracle; comparison against the counter's per-carrier numbers.

Out of scope by design, and not claimed here: the documentation bindings of P36-C1
(`PROVINCE.md` round-36 Core row, knowledge entry, `SOURCES.md` row, coverage-map row) — those are the
counter's `bindings` block and the `met_target` outcome at the landing revision. The interim receipt
is receipts-only and correctly reports `met_target: false` with
`province_core_row/entry_present/sourced/coverage_map_row = false` and `carriers_matched: 4`. Also out
of scope (owned by peer seats `R36ExecReproK1..K4`): re-running REA to compare envelopes.

## 1. The independent checker

Written from scratch at `$S/c1-indep.py` (`S=/fast/scratch/hyaku/kaidoku-r36/R36ExecIndependentC1`),
run as `python3 -I -B c1-indep.py > indep.json` (exit 0). It imports only the Python standard library,
does its own `git show` plumbing, its own TSV parser (rejecting any row without exactly three
tab-separated fields: 0 malformed rows in all four tables), its own envelope walker, and its own
matcher. Deliberate divergences from the counter's implementation, so agreement is meaningful:

| axis | counter (`c1-counter.py`) | this checker |
|---|---|---|
| path match | `fp == rel or fp.endswith('/' + rel)` | component-tuple suffix equality (`comps(fp)[-len(comps(rel)):] == comps(rel)`), i.e. no string-suffix aliasing across component boundaries |
| gap test | first `missing-extractor-dependency` gap containing `sasquatch` | full `extraction_gaps` enumeration + kind histogram + all sasquatch-carrying gaps with handler/dependencies, for both receipts |
| extras | not computed | every published file that satisfies no oracle row is classified (carved slice vs recursion vs other, by nearest `*_extract` ancestor), counted, and checked for sha collisions with oracle content |
| match multiplicity | implicit (one oracle row is "hit" if any file matches) | explicit: for every published file, how many oracle rows it can satisfy; for every oracle row, how many candidate files match |
| evidence id | `tools/round-27/xpin-attribute.mjs` (extracts the pin's `semanticProjection` source and hashes with the pin's digest) | the pin's own authenticated schema: `parseEvidence()` imported from `rea-agents@6.5.0` `dist/domain/evidence.js`, which recomputes `computeEvidenceId` internally and rejects a mismatch |
| oracle | taken as committed | re-derived from the raw carriers with `/usr/bin/unsquashfs` 4.7.5 (sections 5.2–5.3) |

Checker output kept as `indep.json` in scratch; every number below is a field of that file, and every
command that produced it is quoted with its exit code.

## 2. Required numbers, per carrier (independent)

| carrier | oracle rows | after published | **after matched** | before published | **before matched** | sasquatch gaps before / after | after gaps, all kinds | **after files not in oracle** |
|---|---|---|---|---|---|---|---|---|
| K1 | 3 | 3 | **3** | 0 | **0** | **1 / 0** | — | **0** |
| K2 | 4 | 4 | **4** | 0 | **0** | **1 / 0** | `unpublished-entry: 1` | **0** |
| K3 | 2130 | 2147 | **2130** | 2 | **0** | **1 / 0** | `unpublished-entry: 2` | **17** |
| K4 | 2130 | 2147 | **2130** | 2 | **0** | **1 / 0** | `unpublished-entry: 2` | **17** |

Matching rule: same sha256 **and** the oracle relative path is a component suffix of the published
`relative_path`. Every published path is prefixed by `firmware.bin_extract/`, so
`oracle_hits_strict_path_equal` is 0 for all four carriers by construction, and suffix matching is the
only matching in play.

Supporting measurements behind the table (all from `indep.json`):

- Shape of the oracle tables: 3/4/2130/2130 rows, unique relative paths 3/4/2130/2130, unique sha256
  3/4/2116/2116. K3/K4 have 14 content-duplicate rows in two groups (13 `ftplugin/*.lua` stubs sharing
  one digest, 3 `ftplugin/*.vim` stubs sharing another; 16 rows − 2 groups = 14). This does **not**
  weaken matching: no oracle relative path is a component suffix of another oracle relative path with
  the same digest (checked pairwise: 0 pairs), and **no published file satisfies more than one oracle
  row** (per-file oracle-row-satisfaction histogram: K1 `{1:3}`, K2 `{1:4}`, K3/K4 `{0:17, 1:2130}`).
  So `after_oracle_hits == 2130` counts 2130 distinct oracle rows, not 2130 coincidences.
- Per-oracle-row candidate counts: 1 candidate each, `oracle_rows_with_multiple_candidates = 0`;
  zero rows where the path matched but the digest differed; zero size conflicts (every matched
  candidate's `size` equals the oracle's size column, all 4267 rows across four carriers).
- Published relative paths are unique inside each after envelope (`dup_rels = 0`), as are the before
  envelopes.
- Both receipts carry `operation: extract_firmware`, `provider.id: unblob`, and
  `subject.digest.sha256` equal to the carrier digest from `carriers.json` — true for all eight
  envelopes (`subject_ok` 8/8).
- The before receipts each carry exactly one `missing-extractor-dependency` gap with
  `dependencies: ["sasquatch"]` and `handler: squashfs_v4_le`; the after receipts carry **zero**
  sasquatch gaps. The after residual gaps are `unpublished-entry` (K2 ×1, K3/K4 ×2) naming the symlink
  entries (K2 `var/notice-link`; K3/K4 `.DirIcon`, `nvim.png`) — and K1 has no gaps at all.
- Before receipts really publish none of the oracle content: `before_oracle_hits = 0` everywhere. But
  they are not empty: K3/K4 each publish **2** files — the ELF carve of the AppImage runtime
  (`firmware.bin_extract/0-944632.elf64_extract/carved.elf`, 944632 B; K4
  `0-936456…`, 936456 B) and the un-recursed squashfs blob
  (`…/944632-11454968.squashfs_v4_le`, 10510336 B; K4 `…/936456-11356680.squashfs_v4_le`, 10420224 B).
  That is the mechanical shape of the gap: the container is carved and published, the tree is not.
  In the after receipts the raw blob is gone and the tree is present (verified: no published path has
  basename `squashfs_v4_le` in any after envelope).

## 3. Comparison with the counter's per-carrier numbers

Source: `.ufo/waves/round-36/interim/c1-after-receipts-only.json` (fields under `carriers.<K>`).

| carrier | field | independent | counter | agree |
|---|---|---|---|---|
| K1 | `oracle_files` / `after_oracle_hits` / `before_oracle_hits` | 3 / 3 / 0 | 3 / 3 / 0 | yes |
| K1 | `before_sasquatch_gap` / `after_sasquatch_gap` | true / false | true / false | yes |
| K1 | `oracle_frozen` / `matched` (matched derived) | true / true | true / true | yes |
| K2 | oracle / after / before hits | 4 / 4 / 0 | 4 / 4 / 0 | yes |
| K2 | sasquatch before / after | true / false | true / false | yes |
| K3 | oracle / after / before hits | 2130 / 2130 / 0 | 2130 / 2130 / 0 | yes |
| K3 | sasquatch before / after | true / false | true / false | yes |
| K4 | oracle / after / before hits | 2130 / 2130 / 0 | 2130 / 2130 / 0 | yes |
| K4 | sasquatch before / after | true / false | true / false | yes |

`counter_disagreements` is the empty list for all four carriers (24 field comparisons — six fields
per carrier, two of them the boolean gap flags). `matched` is not recomputed here; the independent
column in the table derives from my own fields satisfying every counter conjunct (`oracle_files > 0`,
both receipts present, subject digest = carrier sha, `extract_firmware`/`unblob`, ids authenticated,
before gap present with 0 hits, after gap absent with hits == oracle files). The counter's derived flags that I did not recompute but
did corroborate by a different route: `after_evidence_id_ok` / `before_evidence_id_ok` = true for all
eight envelopes; my independent authentication (§5.4) accepts all eight under the package's own rule.
`carriers_unchanged` = true (carriers.json blob identical at `790561d` and `3310d8f`).

## 4. The after files that are not in the oracle

K1 and K2: none. After-file set equals the oracle set exactly (3 and 4 files).

K3 and K4: **17 each**, all inside the recursion subtree (the squashfs tree itself lives under
`firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/`; K4 `936456-11356680.…`). Full K3 list:

```
firmware.bin_extract/0-944632.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/bin/nvim_extract/0-11170568.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/bin/nvim_extract/11170568-11170569.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/c.so_extract/0-633232.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/c.so_extract/633232-633233.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/lua.so_extract/0-81104.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/lua.so_extract/81104-81105.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/markdown.so_extract/0-376352.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/markdown.so_extract/376352-376353.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/markdown_inline.so_extract/0-363768.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/markdown_inline.so_extract/363768-363769.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/query.so_extract/0-31120.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/query.so_extract/31120-31121.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/vim.so_extract/0-1088936.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/vim.so_extract/1088936-1088937.padding
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/vimdoc.so_extract/0-186768.elf64_extract/carved.elf
firmware.bin_extract/944632-11454968.squashfs_v4_le_extract/usr/lib/nvim/parser/vimdoc.so_extract/186768-186769.padding
```

Classification (same 17-shape for K4, only the offsets/sizes differ):

- **9 × `carved.elf`** — `elf64` slices carved by unblob recursion: the AppImage runtime itself
  (top level, 944632 B) plus the ELF payloads of `usr/bin/nvim` and the seven
  `usr/lib/nvim/parser/*.so` shims (`c`, `lua`, `markdown`, `markdown_inline`, `query`, `vim`,
  `vimdoc`). 8 of the 9 are *additional* output of recursion into oracle files; the top-level one is
  the runtime carve.
- **8 × `*.padding`** — 1-byte `padding` handler chunks trailing each of the 9 carved payloads
  (one per carve, except the top-level runtime carve). Mechanical recursion residue, zero content.
- **0 × re-published oracle content**: no extra shares a sha256 with any oracle row
  (`after_extra_dupe_sha_count = 0` for all carriers).
- Depth accounting for K3 (K4 identical): `after_depth_hist` = `{"1": 2131, "2": 8, "None": 8}` over
  2147 files — 2130 oracle files plus the top-level runtime carve at depth 1, the 8 nested `carved.elf`
  at depth 2, and the 8 one-byte padding chunks with `analysis_depth: null`. So the 17 extras split
  1 (depth 1) + 8 (depth 2) + 8 (null). None of them is a member of the frozen tree, so none affects
  `after_oracle_hits`.
- Also not in the oracle and correctly excluded from the file list: the 2 symlinks per AppImage
  (`.DirIcon`, `nvim.png`) appear as `unpublished_entries` with `kind: symlink`, matching exactly the
  symlink count I observed with `unsquashfs` (K3/K4: 2; K2: 1; K1: 0). 115 directory entries per AppImage (including the extraction root)
  are likewise not in the file list. `coverage` is `partial` for K2/K3/K4 after (consistent with those
  `unpublished-entry` gaps) and `complete` for K1.

## 5. Independent evidence beyond the counter's own checks

These are the falsifiers I can run that the counter cannot, and they all pass.

### 5.1 Carrier digests (fetched, not trusted)
`curl -sSL --max-time 180 -o <name> <url>` for both neovim v0.12.6 AppImages → exit 0, then
`sha256sum`:
`b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` (x86-64, 11454968 B) and
`8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2` (arm64, 11356680 B). Both equal
`carriers.json`. The two synthetic fixtures were extracted from the freeze blob
(`git show 790561d:corpus/evidence/round-36/c1/fixtures/*.sqsh`) and hash to
`93802938…a589` / `ce5bf60e…084f`, equal to `carriers.json`.

### 5.2 Squashfs offsets, re-derived
Scan for the `hsqs` magic myself: K1 0 (single hit), K2 0 (single hit), K3 hits at 194183 and 944632
(the first is a false positive inside the ELF runtime; the real payload starts at 944632, matching
`K3/oracle-run.json`), K4 936456 (single hit, matching `oracle-run.json`).

### 5.3 Oracle tables re-derived with `unsquashfs` 4.7.5
`unsquashfs -o <off> -d ux-k<N> -no-progress <carrier>` → exit 0 four times; then a fresh walk
computing sha256 and size for every entry with `os.path.isfile()` true and `os.path.islink()` false:

| carrier | oracle rows | my regular files | missing in mine | extra in mine | sha mismatch | size mismatch |
|---|---|---|---|---|---|---|
| K1 | 3 | 3 | 0 | 0 | 0 | 0 |
| K2 | 4 | 4 | 0 | 0 | 0 | 0 |
| K3 | 2130 | 2130 | 0 | 0 | 0 | 0 |
| K4 | 2130 | 2130 | 0 | 0 | 0 | 0 |

The oracle tables are therefore exact — same set, same digests, same sizes — and, transitively, so are
the 2130 published after-digests per AppImage (after ↔ oracle matched on sha256, oracle ↔ real image
matched on sha256). This is the check that closes the "could the after envelope be fabricated?"
question for these receipts: fabricated hashes would have to equal real `unsquashfs` output.

### 5.4 Evidence ids authenticated by the rule owner
`node evauth.mjs` imports `parseEvidence` from `rea-agents@6.5.0`
`dist/domain/evidence.js` (the schema that recomputes `computeEvidenceId` and rejects a mismatch) and
runs it on all eight committed envelopes: **8/8 `accept`**, e.g. K3 before `ev_91e4ab30b6a5edf4a…`,
K3 after `ev_b83bd3056f103a72e…`, K4 after `ev_ff0fdb798eea077df…` — each equal to the stored
`evidence_id`. Sensitivity control: a copy of K1 after with one published sha256 rewritten to
`0…0` → `REJECT` with `path: ["evidence_id"], message: "Evidence semantic identifier does not match
its record"`. So the acceptance is not vacuous.

### 5.5 Run metadata vs the host
`after-run.json` records sasquatch `/home/vgpnk/.local/bin/sasquatch`, sha256
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, version string
`unsquashfs version 4.5.1 (2022/03/17)`. On the host: same path, `sha256sum` =
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (382824 B, mtime 01:22),
`sasquatch -version` → `unsquashfs version 4.5.1 (2022/03/17)`. `unblob` resolves to
`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` = the after envelope's
`normalized_result.engine.executable_sha256`, `--version` → `26.6.4` = `engine.version`. The before
envelopes record no sasquatch path (`before-run.json` `sasquatch: ""`).

### 5.6 Receipt immutability
`before.json` blob ids at `790561d` and `3310d8f` are identical for all four carriers
(frozen with the claim); `oracle.tsv` likewise (`oracle_frozen = true` per carrier).

## 6. Observations and residual risk (advisory — nothing repaired)

1. **The after envelope carries no in-receipt sasquatch attribution.** `json.dumps(after.json)`
   contains the string `sasquatch` **0 times** for all four carriers; the successful chunk is recorded
   as `handler: squashfs_v4_le` with `extraction_failed: false`, and unblob's per-task report entries
   are Stat/Magic/Hash only. Attribution rests on (a) the committed `after-run.json`
   (path/sha256/version), (b) the paired no-sasquatch receipt which *does* name sasquatch as a missing
   dependency, and (c) the two running on the same unblob build. `after-run.json` is **not** covered by
   the evidence id, so the "run with sasquatch on PATH" half of the predicate is author-asserted
   metadata; §5.5 corroborates the binary identity, §5.3 corroborates the output. Consistent with the
   frozen predicate as written — flagged so the calibration reading does not overstate what the
   receipt alone proves.
2. **Evidence ids are not reproducible across runs.** `semanticProjection` includes
   `normalized_result` and `raw_result`, and both embed absolute scratch paths: K1 after has
   `normalized_result.output_directory = /fast/scratch/hyaku/kaidoku-r36/c1-run.dcmJTg/out`, and
   `raw_result.report[0].task.path` is
   `/fast/scratch/hyaku/kaidoku-r36/c1-run.dcmJTg/rea-firmware-ris5IG/extracted/firmware.bin_extract/README.txt`
   (K3 after's raw paths use `c1-run.7PV16k/rea-firmware-2j28Os/…`). Re-running with
   identical output would yield a different `ev_…`. This does not break the predicate (each receipt
   recomputes to *its* stored id — §5.4), but it means "recompute to the stored id" can only ever be a
   property of the committed bytes, never a cross-run equality. This is presumably why the peer
   reproduction seats diff with the outdir scrubbed.
3. **`coverage: partial` on K2/K3/K4 after** is caused solely by the symlink `unpublished-entry` gaps
   (1, 2, 2). The predicate bars only `missing-extractor-dependency` gaps naming sasquatch, so it is
   satisfied; recorded so a reader does not read `partial` as a silent miss.
4. **Counter's suffix matcher has a latent precondition that is absent here.** If an oracle ever held
   two rows where one relative path is a component suffix of the other *and* they share a digest, one
   published file could satisfy two rows and `after_oracle_hits` would overcount. I checked both
   preconditions on all four tables: 0 such pairs, and per-file satisfaction multiplicity is 1
   everywhere. No defect at this revision; noted for future freezes.
5. **Fidelity nuance in the symlink metadata.** For K3/K4 the envelope's `.DirIcon` `link_target` is
   `usr/share/icons/hicolor/128x128/apps/nvim.png`, whereas the raw squashfs link is `nvim.png`
   (`nvim.png` itself points at the icon). [INFERENCE] unblob reports the resolved target for the
   indirect link. Cosmetic; does not touch the regular-file predicate.
6. **K1's after envelope is `coverage: complete` with 3/3 files and no gaps**, so the synthetic
   minimal case exercises only the happy path; K2 is the one that exercises regular-files-only
   accounting (one symlink, `usr/lib/kaidoku/*` nested dirs).

## 7. Commands run (exact, with exit codes)

```
S=/fast/scratch/hyaku/kaidoku-r36/R36ExecIndependentC1; mkdir -p "$S"; export TMPDIR="$S"
curl -sSL --max-time 180 -o nvim-linux-x86_64.appimage <release url>     # exit 0, 11454968 B
curl -sSL --max-time 180 -o nvim-linux-arm64.appimage   <release url>     # exit 0, 11356680 B
sha256sum *.appimage                                                      # both == carriers.json
git -C LANE show 790561d:corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh   > "$S/k1-le-xz.sqsh"
git -C LANE show 790561d:corpus/evidence/round-36/c1/fixtures/k2-le-gzip.sqsh > "$S/k2-le-gzip.sqsh"
sha256sum k1-le-xz.sqsh k2-le-gzip.sqsh                                   # both == carriers.json
python3 -  # hsqs scan -> offsets 0, 0, 944632, 936456                    # exit 0
unsquashfs -o 0      -d ux-k1 -no-progress k1-le-xz.sqsh                  # exit 0
unsquashfs -o 0      -d ux-k2 -no-progress k2-le-gzip.sqsh                # exit 0
unsquashfs -o 944632 -d ux-k3 -no-progress nvim-linux-x86_64.appimage     # exit 0
unsquashfs -o 936456 -d ux-k4 -no-progress nvim-linux-arm64.appimage      # exit 0
python3 -  # oracle re-derivation walk; 0 missing / 0 extra / 0 sha / 0 size diffs on 3,4,2130,2130
python3 -I -B c1-indep.py > indep.json                                    # exit 0
node evauth.mjs before-K{1..4}.json after-K{1..4}.json tamper-K1.json      # exit 0; 8 accept, 1 REJECT
sha256sum ~/.local/bin/sasquatch; readlink -f ~/.local/bin/unblob; sha256sum <resolved>  # == run metadata
for k in K1..K4: git rev-parse 790561d:<…>/before.json vs 3310d8f:<…>/before.json         # 4/4 identical
for k,f in 12 files: git hash-object <worktree> vs git rev-parse 3310d8f:<path>          # 12/12 SAME
```

Tooling: **nothing installed, nothing upgraded** (so the 2026-10-19 authorization was not exercised).
Used: system `git`, `python3` 3.14 stdlib, `node`, `/usr/bin/unsquashfs` 4.7.5, `curl`, the
already-installed `rea-agents@6.5.0` package at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (imported read-only), and the
host's existing `~/.local/bin/sasquatch` (hashing only — I never executed it and never ran REA).
No `npx`, no VCS mutation (only `show`/`hash-object`/`rev-parse`/`cat-file`-class reads), no writes
outside this report.

## 8. Risks / blockers

- No blocker. The per-carrier half of P36-C1 is corroborated at `3310d8f` by a checker that shares no
  code with the counter, and by an oracle re-derived from the carriers themselves.
- Open decision for the L1, not for me: whether "the receipt run with sasquatch on PATH" should be
  evidenced by something inside the evidence-id envelope (observation 1). Changing that would be a
  predicate/counter change and is out of bounds for this seat; as frozen, the claim is met on the
  receipt side.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ExecIndependentC1` (carriers, extractions,
  `c1-indep.py`, `indep.json`, `evauth.mjs`, envelope copies) is removed before this seat ends; the
  numbers, enumerations and commands above are the retained evidence.

## 9. Appendix — checker output excerpt (retained because scratch is deleted)

Fields of `indep.json` after removing the long sample lists; values are verbatim.

```json
{
 "carriers_unchanged": true,
 "counter_carriers_matched": 4,
 "counter_met_target": false,
 "freeze": "790561d4e3aca732a434081aa9573ec2fa5fd7d0",
 "per_carrier": {
  "K1": {
   "after_continuations": 0,
   "after_coverage": "complete",
   "after_depth_hist": {
    "1": 3
   },
   "after_dup_rels": 0,
   "after_extra_dupe_sha_count": 0,
   "after_extras": 0,
   "after_files": 3,
   "after_gap_kinds": {},
   "after_gaps_total": 0,
   "after_max_depth": 1,
   "after_oracle_hits": 3,
   "after_oracle_hits_strict_path_equal": 0,
   "after_oracle_rows_with_multiple_candidates": 0,
   "after_present": true,
   "after_sasquatch_gaps": 0,
   "after_size_or_sha_conflicts": 0,
   "after_unpublished_entries": 0,
   "before_dup_rels": 0,
   "before_files": 0,
   "before_gap_kinds": {
    "missing-extractor-dependency": 1
   },
   "before_gaps_total": 1,
   "before_oracle_hits": 0,
   "before_present": true,
   "before_sasquatch_gaps": 1,
   "before_size_or_sha_conflicts": 0,
   "counter_disagreements": [],
   "oracle_bad_rows": 0,
   "oracle_frozen_at_rev": true,
   "oracle_rows": 3,
   "oracle_unique_rels": 3,
   "oracle_unique_shas": 3
  },
  "K2": {
   "after_continuations": 1,
   "after_coverage": "partial",
   "after_depth_hist": {
    "1": 4
   },
   "after_dup_rels": 0,
   "after_extra_dupe_sha_count": 0,
   "after_extras": 0,
   "after_files": 4,
   "after_gap_kinds": {
    "unpublished-entry": 1
   },
   "after_gaps_total": 1,
   "after_max_depth": 1,
   "after_oracle_hits": 4,
   "after_oracle_hits_strict_path_equal": 0,
   "after_oracle_rows_with_multiple_candidates": 0,
   "after_present": true,
   "after_sasquatch_gaps": 0,
   "after_size_or_sha_conflicts": 0,
   "after_unpublished_entries": 1,
   "before_dup_rels": 0,
   "before_files": 0,
   "before_gap_kinds": {
    "missing-extractor-dependency": 1
   },
   "before_gaps_total": 1,
   "before_oracle_hits": 0,
   "before_present": true,
   "before_sasquatch_gaps": 1,
   "before_size_or_sha_conflicts": 0,
   "counter_disagreements": [],
   "oracle_bad_rows": 0,
   "oracle_frozen_at_rev": true,
   "oracle_rows": 4,
   "oracle_unique_rels": 4,
   "oracle_unique_shas": 4
  },
  "K3": {
   "after_continuations": 1,
   "after_coverage": "partial",
   "after_depth_hist": {
    "1": 2131,
    "2": 8,
    "None": 8
   },
   "after_dup_rels": 0,
   "after_extra_dupe_sha_count": 0,
   "after_extras": 17,
   "after_files": 2147,
   "after_gap_kinds": {
    "unpublished-entry": 2
   },
   "after_gaps_total": 2,
   "after_max_depth": 2,
   "after_oracle_hits": 2130,
   "after_oracle_hits_strict_path_equal": 0,
   "after_oracle_rows_with_multiple_candidates": 0,
   "after_present": true,
   "after_sasquatch_gaps": 0,
   "after_size_or_sha_conflicts": 0,
   "after_unpublished_entries": 2,
   "before_dup_rels": 0,
   "before_files": 2,
   "before_gap_kinds": {
    "missing-extractor-dependency": 1
   },
   "before_gaps_total": 1,
   "before_oracle_hits": 0,
   "before_present": true,
   "before_sasquatch_gaps": 1,
   "before_size_or_sha_conflicts": 0,
   "counter_disagreements": [],
   "oracle_bad_rows": 0,
   "oracle_frozen_at_rev": true,
   "oracle_rows": 2130,
   "oracle_unique_rels": 2130,
   "oracle_unique_shas": 2116
  },
  "K4": {
   "after_continuations": 1,
   "after_coverage": "partial",
   "after_depth_hist": {
    "1": 2131,
    "2": 8,
    "None": 8
   },
   "after_dup_rels": 0,
   "after_extra_dupe_sha_count": 0,
   "after_extras": 17,
   "after_files": 2147,
   "after_gap_kinds": {
    "unpublished-entry": 2
   },
   "after_gaps_total": 2,
   "after_max_depth": 2,
   "after_oracle_hits": 2130,
   "after_oracle_hits_strict_path_equal": 0,
   "after_oracle_rows_with_multiple_candidates": 0,
   "after_present": true,
   "after_sasquatch_gaps": 0,
   "after_size_or_sha_conflicts": 0,
   "after_unpublished_entries": 2,
   "before_dup_rels": 0,
   "before_files": 2,
   "before_gap_kinds": {
    "missing-extractor-dependency": 1
   },
   "before_gaps_total": 1,
   "before_oracle_hits": 0,
   "before_present": true,
   "before_sasquatch_gaps": 1,
   "before_size_or_sha_conflicts": 0,
   "counter_disagreements": [],
   "oracle_bad_rows": 0,
   "oracle_frozen_at_rev": true,
   "oracle_rows": 2130,
   "oracle_unique_rels": 2130,
   "oracle_unique_shas": 2116
  }
 },
 "revision": "3310d8fa27bfaa95ad858c4aaad6f6377f853982"
}
```

Report: `.ufo/waves/round-36/w1/R36ExecIndependentC1.md`
