# R40C2ReconEmpty — a clean SquashFS v4 image with ZERO regular files (P=0): REA outcome, v1 label, v2 expressibility

VERDICT: **CONFIRMED / DEFECTS FOUND** — a clean SquashFS v4 image whose tree holds no regular files
produces exactly the round-39 D2 vector (`H` non-empty, `G=∅`, `D=∅`, `BE=n/a`, `SR=no`, `P=0`) on
14 development runs (three directory-only trees × both endians × gzip/xz, plus a childless-root
control), REA records **no** extraction gap, no unpublished entry and no diagnostic, and the frozen v1
table labels it **`unclassified`**; two further measured zero-file shapes (in-tree-link-only and
escaping-link-only) are also `unclassified` because rows 6 and 7 carry `published files = >0`; a
candidate v2 table in the L1's grammar labels all 26 real envelopes correctly and keeps a non-`unblob`
/ non-`extract_firmware` envelope at `unclassified`; the truly childless root tree is a **carrier
hazard** (zero-length metadata block: `sqfs-list.py` exit 2 while REA and both sasquatch builds accept
it), and the current held-out generator cannot yet build a directory-only tree.

## 0. Scope and bounds

Seat `R40C2ReconEmpty`, round 40 wave 1 (pre-freeze). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `fa6a8a3f…`.

Question set: characterise a clean SquashFS v4 image with zero regular files (a tree of only
directories, or only symlinks) for BE and LE; does REA record a gap; does the v1 table label it
`unclassified` or wrongly; is the vector separable from `no-squashfs-chunk` and from `dep-missing`;
is the recipe stable on three trees and both endians; does the L1's v2 grammar express it.

Bounds honoured: all carriers are **fresh trees authored in scratch**, built only with
`tools/round-39/gen-squashfs.py` (LE/BE/AVM marker modes); no C1 carrier (V1/V2/L1/L2) and no C2
held-out carrier was built, opened or run through REA/unblob; REA ran only via its CLI; every write
is this report or `artifacts/R40C2ReconEmpty/`; no VCS mutation; no pacman; scratch removed at the end.

## 1. Method (exact commands; all REA runs exit 0, `ok:true`)

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40C2ReconEmpty`, `TMPDIR=$S`, `HYAKU_SCRATCH=/fast/scratch/hyaku`.

Trees (`trees.json`): `T1` = one empty directory; `T2` = nested empty directories `a/b`, `c`;
`T5` = 7 directories incl. UTF-8 names `ümlaut/`, `ümlaut/empty/`, `日本語/`, chain `a/b/c/d`;
`T3` = 2 directories + 2 in-tree symlinks, zero regular files; `T6` = 1 directory + 2 escaping
symlinks, zero regular files; `T4` = **no entries at all** (childless root, degenerate control).
No tree contains a regular file.

Carrier build (`23` carriers, 146–511 B, digests in `carriers.sha256`):

```
python3 /…/kaidoku-shokunin/tools/round-39/gen-squashfs.py TREE OUT --endian le|be|avm --comp gzip|xz
```

For every (tree ∈ {T1,T2,T3,T5}) × (endian ∈ {le,be}) × (comp ∈ {gzip,xz}); T4 le/be gzip;
T6 le/be gzip; `T1 --endian avm --comp gzip`, `T2 --endian avm --comp xz`; `NOTSQFS-gzip.bin` =
21 bytes of ASCII. Determinism check: a second build of `T1-be-gzip` is byte-identical
`65886123f5e2e223b8013d4dbe2edbc4557b42f8c538803f2145d124202abfb7`.

REA (26 runs, each in its own fresh cwd and fresh output directory):

```
cd "$S/runs/<id>" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <abs carrier> <fresh outdir>
```

`after` arm = PATH unchanged; `before` arm (`*-dep` runs) = `$HOME/.local/bin` stripped from the
child PATH with the unblob command kept absolute. Versions: REA 6.5.0, unblob 26.6.4 (engine
`executable_sha256 = 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`),
sasquatch / sasquatch-v4be 4.5.1. Durations 2.1–5.6 s per run.

Independent reads: `python3 -I -B tools/round-39/sqfs-list.py IMAGE --files F --symlinks S --inspect`
(`oracle/`), and direct `sasquatch` (LE) / `sasquatch-v4be -be` (BE) reads (`logs/direct-reads.txt`).
v1 labelling: `python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json ENV`
(`v1-labels.tsv`).

## 2. Measured feature table (26 REA runs; features extracted with the v1 grammar plus the v2 fields)

`H` = squashfs* chunk handlers, `G` = gap-kind set, `D` = union of gap dependencies, `BE` = `-be` in a
recorded sasquatch argv, `SR` = `MaliciousSymlinkRemoved` seen, `P` = `len(normalized_result.files)`.

| run | H | G | D | BE | SR | P | chunk failed | unpublished | diagnostics | v1 label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NOTSQFS-gzip | ∅ | ∅ | ∅ | n/a | no | 0 | ∅ | ∅ | ∅ | no-squashfs-chunk |
| T1-avm-gzip | squashfs_v4_be | extractor-failure | ∅ | no | no | 0 | squashfs_v4_be:true | ∅ | ExtractCommandFailedReport(cmd) | avm-marker-be-dropped |
| T1-be-gzip | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T1-be-gzip-dep | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | squashfs_v4_be:true | ∅ | ExtractorDependencyNotFoundReport | dep-missing-be |
| T1-be-xz | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T1-le-gzip | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T1-le-gzip-dep | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0 | squashfs_v4_le:true | ∅ | ExtractorDependencyNotFoundReport | dep-missing-le |
| T1-le-xz | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T2-avm-xz | squashfs_v4_be | extractor-failure | ∅ | no | no | 0 | squashfs_v4_be:true | ∅ | ExtractCommandFailedReport(cmd) | avm-marker-be-dropped |
| T2-be-gzip | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T2-be-xz | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T2-be-xz-dep | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0 | squashfs_v4_be:true | ∅ | ExtractorDependencyNotFoundReport | dep-missing-be |
| T2-le-gzip | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T2-le-xz | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T3-be-gzip | squashfs_v4_be | unpublished-entry | ∅ | n/a | no | 0 | squashfs_v4_be:false | symlink,symlink | ∅ | unclassified |
| T3-be-xz | squashfs_v4_be | unpublished-entry | ∅ | n/a | no | 0 | squashfs_v4_be:false | symlink,symlink | ∅ | unclassified |
| T3-le-gzip | squashfs_v4_le | unpublished-entry | ∅ | n/a | no | 0 | squashfs_v4_le:false | symlink,symlink | ∅ | unclassified |
| T3-le-xz | squashfs_v4_le | unpublished-entry | ∅ | n/a | no | 0 | squashfs_v4_le:false | symlink,symlink | ∅ | unclassified |
| T4-be-gzip | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T4-le-gzip | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T5-be-gzip | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T5-be-xz | squashfs_v4_be | ∅ | ∅ | n/a | no | 0 | squashfs_v4_be:false | ∅ | ∅ | unclassified |
| T5-le-gzip | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T5-le-xz | squashfs_v4_le | ∅ | ∅ | n/a | no | 0 | squashfs_v4_le:false | ∅ | ∅ | unclassified |
| T6-be-gzip | squashfs_v4_be | ∅ | ∅ | n/a | yes | 0 | squashfs_v4_be:false | ∅ | MaliciousSymlinkRemoved,MaliciousSymlinkRemoved | unclassified |
| T6-le-gzip | squashfs_v4_le | ∅ | ∅ | n/a | yes | 0 | squashfs_v4_le:false | ∅ | MaliciousSymlinkRemoved,MaliciousSymlinkRemoved | unclassified |

Full per-run detail (chunks, gaps, derivations, published bytes, output directory): `features.json`;
TSV: `features.tsv`; raw envelopes: `envelopes/*.full.json`; run records (exit code, argv, arm,
duration): `envelopes/*.run.json`.

## 3. Findings

**F1 — REA records no gap, no unpublished entry, no diagnostic for a clean P=0 image.** For all 12
directory-only runs and the 2 childless-root controls (14 clean runs) the envelope carries:
`chunks = [{handler: squashfs_v4_be|le, extraction_failed: false, encrypted: false}]`,
`extraction_gaps = []`, `unpublished_entries = []`, `diagnostics = []`, `files = []`,
`coverage = "complete"`, `published_bytes = 0`, `depth_limited_paths = []`,
`extraction_continuations = []`. The output directory is left empty (REA publishes only regular
files; `ls` of `runs/T1-be-gzip/out` is empty). So `P=0` with `H` non-empty and `G=∅` is the honest
"extracted cleanly, nothing to publish" signal.

**F2 — the tree's structure is still visible in `derivations`.** The same clean run records
`derivations = [{$output/firmware.bin_extract/onlydir, handler:null}, {$output/firmware.bin_extract,
handler:squashfs_v4_be}]` — directory nodes appear as `handler:null` derivations (T2: 4; T5: 8;
T4 childless: 0). The v2 feature set does not expose `derivations`, so the label cannot distinguish
"empty tree with directories" from "childless root"; the counter can still use it as an optional
oracle aid (see F8).

**F3 — v1 labels the clean P=0 image `unclassified` (D2 confirmed on fresh carriers).** All 12
directory-only runs (T1/T2/T5 × le/be × gzip/xz) get `label=unclassified, rule=none` from
`tools/round-39/sqfs-triage.py` reading the frozen SKILL.md table. This reproduces
`w2/R39W2C2TableReview.md` D2 (`SKILL.md:343` `published files = >0`) on development inputs the
review did not have.

**F4 — NEW: row 7 (`in-tree-symlink-metadata`, `SKILL.md:342`) also excludes a measured P=0 shape.**
A tree of two directories plus two in-tree symlinks and no regular files yields
`G={unpublished-entry}`, `unpublished_entries = [{kind:symlink, link_target:../ghost,
relative_path:firmware.bin_extract/linkdir/rel}, …]`, `D=∅`, `SR=no`, `P=0` and is `unclassified`
under the frozen `>0` cell. The row's cause and action ("count one gap per in-tree link and publish
nothing for it") are exactly right at P=0, so the cell buys no separation and loses a real outcome —
the same defect class as D2.

**F5 — NEW: row 6 (`escaping-symlink-removed`, `SKILL.md:341`) also excludes a measured P=0 shape.**
A tree of one directory plus two escaping symlinks and no regular files yields `G=∅`, `D=∅`,
`SR=yes` (two `MaliciousSymlinkRemoved` reports), `P=0` and is `unclassified` under the frozen `>0`
cell. The action ("expect the path to be absent; never materialise the link") survives P=0 unchanged.

**F6 — the clean-empty vector is separable from both neighbours.**
`no-squashfs-chunk`: `H=∅` (measured `NOTSQFS-gzip`: `H=[], G=[], P=0`, `coverage=complete`) versus
`H=[squashfs_v4_be|le]` — the v1 row 1 is keyed on `handler none`, so no overlap.
`dep-missing`: `G={missing-extractor-dependency}`, `D={sasquatch-v4be}` or `{sasquatch}`, and
`diagnostics=[ExtractorDependencyNotFoundReport]` versus `G=∅, D=∅, diagnostics=[]` — disjoint on
both set columns. The AVM marker and dependency rows still match at P=0 (`T1-avm-gzip` → row 4,
`T1-be-gzip-dep`/`T1-le-gzip-dep`/`T2-be-xz-dep` → rows 2/3/2), so shrinking to zero files does not
disturb the neighbouring decisions.

**F7 — the recipe is stable.** Three different directory-only trees (one empty dir; nested dirs; 7
dirs with UTF-8 names and depth 4) × both endians × gzip/xz produce the *identical* vector apart from
the endian-specific handler, which the `squashfs_v4_*` pattern covers: 12/12 clean-empty runs are
indistinguishable to the table. Independent readers agree the images are well-formed:
`sqfs-list.py` → `regular_files 0`, `warnings []`, exit 0; `sasquatch` (LE) and `sasquatch-v4be -be`
(BE) → exit 0 with exactly the authored directory count (T1 2, T2 4, T5 8 including the extraction
root) and 0 files. T6/BE additionally shows `links=2` in the direct read. No writer extension was
needed: the round-39 `gen-squashfs.py` writes empty directories correctly as long as the tree has at
least one entry (see F8 for the one shape it cannot write).

**F8 — HAZARD: a truly childless root tree yields a zero-length metadata block.** T4 (no entries at
all, 146 B) is accepted by REA (clean, `P=0`, `derivations=[]`), by `sasquatch` (LE) and by
`sasquatch-v4be -be` (BE) — but the independent reader refuses it:
`sqfs-list: zero-length metadata block at 130`, exit 2 (both endians, `oracle/T4-*.err`). Cause:
`gen-squashfs.py`'s `MetaWriter.settle()` (`tools/round-39/gen-squashfs.py:61-64`) appends a block for
an empty buffer when the table has no appends, and only the childless root produces an empty directory
table. Therefore the clean-empty recipe **must contain at least one directory** (which the current
generator's tree builder already guarantees, see §6) and must never be the bare empty tree; if it
ever is, `sqfs-list.py`-based oracles and any image-reading gate will fail on it while REA calls it
clean.

**F9 — writer limitation found while building T3 (not used as evidence):** `os.walk` lists a symlink
whose target is a directory in `dnames` and never walks it, so `build_image` silently drops it
(`T3` first build: `inodes 3`, no symlink inodes; `sqfs-list` reported `symlinks 0`). Symlinks must
target non-directories (files or dangling paths) to be written. The held-out generator always links
to an existing regular file, so this is dormant there; record it for any hand-authored tree.

**F10 — REA's process exit code is not a discriminator:** all 26 runs exit 0 with `ok:true`,
including the dependency miss, the AVM marker drop, the body failure and the no-chunk input. Any
counter must read envelope features, never the CLI exit code (consistent with R39-CL6).

## 4. The L1's v2 grammar — verified, with the zero-file vectors as the test load

The probe `probe-v2-rows.py` implements the draft contract as written (marker inside
`## Queue-drain craft`, exact 12-column header, first full match, `unclassified/none` on no match,
unique labels → exit 2, closed action vocabulary → exit 2, malformed cell → exit 2). It reads nothing
but the table and the envelope, accepts a bare `data` object or a full `{ok,data,meta}` envelope
(both verified), and is a **recon probe, not the frozen interpreter**.

4.1 **Provider field: `data.provider.id`.** Measured on every envelope:
`data.provider = {id:"unblob", name:"Unblob", version:"26.6.4"}`. The draft's "or the provider name
field REA really emits — verify" resolves to `id`; if an interpreter used `name`, every cell would
need `Unblob`. A synthetic envelope with `provider.name` changed but `id` kept is still `clean-empty`
(`fixtures/synthetic/T1-le-gzip-PV-name-only.json`), so the guard is on `id` as intended.

4.2 **Operation value is `extract_firmware`** (underscore), not the CLI spelling `extract-firmware`.

4.3 **Candidate table result (`probe-v2-labels.tsv`):** 30 envelopes, 10 rules, 9-token vocabulary.
26 real envelopes: 14 `clean-empty` (T1/T2/T5 + T4), 4 `in-tree-symlink-metadata` (T3), 2
`escaping-symlink-removed` (T6), 3 `dep-missing-*`, 2 `avm-marker-be-dropped`, 1
`no-squashfs-chunk` — every one equal to the outcome the run measured. 4 synthetic envelopes (`fixtures/synthetic/`):
`operation=analyze` → (`unclassified`,`none`); `provider.id=binwalk` → (`unclassified`,`none`);
`operation=decompile` on the in-tree carrier (`fixtures/synthetic/T3-le-gzip-OP-decompile.json`) → (`unclassified`,`none`); provider-`name`-only change →
`clean-empty`.

4.4 **Error paths exercised** (`fixtures/`): duplicate label → exit 2
(`probe: duplicate label 'clean'`); `published files = many` → exit 2; action
`accept-everything` outside the vocabulary → exit 2. No silent non-match.

4.5 **Domain-guard kill control works:** the same candidate table with both domain columns set to `*`
(`fixtures/nodomain.md`) labels the synthetic `analyze` envelope `clean-empty`, i.e. exactly the
R39-CL1 defect; with the guard it is `unclassified`. This is a cheap pre-freeze control the freeze can
carry.

4.6 **Two grammar points to pin in the contract (ambiguities, not defects):**
(a) "the actions line … directly above the table" — with the marker line between them it is unclear
whether the comment must precede the marker or the header; the probe accepts either. Recommend:
pin it immediately above the marker, so the marker directly precedes the header.
(b) `handler` semantics must be "`none` = no squashfs handler; otherwise fnmatch applied to *any*
handler", exactly like v1 (`rule_matches`, `tools/round-39/sqfs-triage.py:453-457`). A `*` handler
cell is a legal fnmatch that matches any non-empty `H` and must **not** match an empty `H` (fnmatch
over an empty list), which is what keeps row 1 (`no-squashfs-chunk`) reachable. The probe implements
this; the contract text should say it.

## 5. Recommended v2 rows (exact 12-column cells; paste-ready)

Order: `… mixed-symlinks`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `clean-empty`,
`clean`. The two symlink rows move from `>0` to `*` (F4/F5); `clean-empty` is a new row before
`clean` (F3); the mixed row is the claim's R39-CL2 row. Actions are proposals from one closed
vocabulary; the L1 owns the token names.

```
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `yes` | `*` | `count-gap-and-absence` | both kinds in one image: an escaping link removed with a report and in-tree links recorded as one gap each | S118 79-91; S119 68-75 |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `yes` | `*` | `expect-link-absent` | a symlink target resolved outside the extraction root and was removed with a report, no gap | S118 extractor.py:79-91 |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `no` | `*` | `count-gap` | a non-file entry stayed inside the root; one unpublished-entry gap each, nothing published | S119 FirmwarePublication.js:68-75,301-308 |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `0` | `accept-empty` | the filesystem is readable and holds no regular files; chunk extracted, no gap: verify the derivation/directory list, do not read zero published files as a missing chunk or a dependency miss | recon R40C2ReconEmpty (14 runs) |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | `accept-oracle` | every regular file was published, no gap recorded and no symlink removed | S119; knowledge entry :11-19 |
```

Why a distinct `clean-empty` row rather than one `clean` row with `*`: the claim names `clean-empty`
as a class and (R39-CL3) wants the counter to report distinct row decisions; at P=0 the `clean`
action ("match files to an oracle by suffix + sha256") is vacuous, while `accept-empty` names the
right check (directories/derivations, and the fact that zero published files is expected). If the L1
prefers the minimal table, `clean` with `published files = *` also scores `clean-empty` correctly, but
then `clean-empty` is a non-decision replicate and must not be counted as a distinct decision. The two
orders are behaviourally identical only because `0` and `>0` are disjoint; if `clean` keeps `*`, the
`clean-empty` row must come first or it can never fire.

## 6. Freeze implications for the `clean-empty` held-out class

- **`tools/round-39/heldout-gen.py` cannot build it today.** `build_tree` (`:271-311`) always writes
  3–8 regular files (`:293`); a `clean-empty` recipe needs a tree flag such as `files=0` while keeping
  the existing `depth = rng.randint(1, 3)` directory chain (≥1 directory — which also avoids the F8
  childless-root hazard). `tree_oracle` already handles `files: []`.
- **Writer version.** The generator loads `tools/round-37/gen-squashfs.py` (`WRITER_LOGICAL` `:121`,
  `load_writer` `:150`) and only replaces the block encoder. The round-37 writer writes the
  dir-entry `name_size` as `len(name) - 1` characters (`tools/round-37/gen-squashfs.py:147`); the
  round-39 copy fixed it to UTF-8 bytes (`tools/round-39/gen-squashfs.py:159`) and is byte-identical
  for ASCII trees. Either keep the clean-empty tree names ASCII (the generator's `token()` alphabet
  is ASCII, so this is live today) or switch the generator to the round-39 writer before adding
  non-ASCII names. My T5 shows UTF-8 directory names are fine with the round-39 writer
  (`sqfs-list` and both sasquatch builds read them; feature vector unchanged).
- **Replicate design.** The 12 directory-only runs show endian and compression are non-decision
  features; make the two `clean-empty` replicates differ in both (e.g. one BE/xz, one LE/gzip) so the
  class demonstrates the row is endian-agnostic rather than duplicating one decision.

## 7. Residual risks and limits

- **Silent loss inside a clean-empty label.** An empty-target symlink is removed by unblob with no
  `MaliciousSymlinkRemoved` and no gap (`S118 extractor.py:68-71`, cited in the round-39 row-6
  caveat), so an image whose only entry is such a link would label `clean-empty` while a path is
  absent. [INFERENCE] from the cited source: I did not build that carrier (`os.symlink('')` is not
  permitted on Linux). The `accept-empty` action's derivation/directory check is the containment.
- **`unpublished-entry` for non-symlink entries.** A device node/FIFO (`kind: "special"`) produces the
  same `G={unpublished-entry}` and would take the in-tree row under a symlink-only cause (R39 D4a);
  the writer cannot emit special nodes, so it is unmeasured here.
- **The v2 feature set cannot see `derivations`.** T4 (childless, `derivations=[]`) and T1
  (`derivations=2`) share a vector. If the counter needs to reject T4-shaped carriers, it must read
  `derivations` (or the image); the table alone cannot.
- **P is `len(normalized_result.files)` and counts regular files only** (verified: directories and
  symlinks are absent from it, present in `derivations`/`unpublished_entries`). If REA ever changes
  that, every `published files` cell changes meaning.
- **AVM interplay is unchanged by zero files** (row 4 still matches at P=0), but a *genuine* AVM-layout
  carrier was out of scope (C1's ground); nothing here says a genuine AVM body with no files behaves
  like the marker-only body.
- **Direct-read asymmetry observed:** on a standard-BE body, `sasquatch-v4be` *without* `-be` fails
  (`different endianess … read_id_table: failed … FATAL`, exit 1), while with `-be` it extracts 0
  files (exit 0) — `logs/be-without-flag.txt`. This is the mechanism row 4 describes; it also means
  the clean-empty BE carriers depend on unblob supplying `-be`, which it does for a non-marker body.

## 8. Tooling and bounds record

No tool installed, upgraded, moved or removed (RULES.md read; nothing needed; pacman untouched).
REA invoked only as `npx -y rea-agents@6.5.0 extract-firmware`; `unblob`/`sasquatch*` unchanged.
No VCS mutation (no git/jj writes); lane files read only. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C2ReconEmpty` removed after copying the cited bytes into the
artifacts directory; one narrow `find` listing ran under the scratch tree early on (my own scratch,
not a `/fast/scratch` sweep) — subsequent listings used `ls`/Python.

## 9. Artifacts

`.ufo/waves/round-40/w1/artifacts/R40C2ReconEmpty/` (876 KB): `README.md` index, `build.sh`
(reproduces everything, `usage: ./build.sh WORKDIR`), `trees.json`, `carriers/` + `carriers.sha256`
(23), `envelopes/` (26 full + 26 run records + `runs.json`), `features.json`/`features.tsv`,
`v1-labels.tsv`, `probe-v2-labels.tsv`, `candidate-triage-v2.md`, `probe-v2-rows.py`, `fixtures/`
(4 malformed/control tables + 4 synthetic domain-guard envelopes), `oracle/` (per-carrier `sqfs-list` output, incl. the T4 exit-2 error),
`logs/sqfs-list.txt`, `logs/direct-reads.txt`, `logs/be-without-flag.txt`.
