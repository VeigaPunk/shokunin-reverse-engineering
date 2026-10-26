# R40C2HeldoutGen — held-out carrier generator v2 (round 40, wave 1, pre-freeze)

**DONE — `heldout-gen-v2.py` builds 13 classes × 2 deterministic replicates (26 carriers), assigns
each carrier its (label, action) pair from the class before any REA run, and its dev run reproduces
26/26 pairs under the working v2 interpreter while the frozen round-39 v1 table reproduces only
18/26; three incompatible action vocabularies need one L1 binding at the freeze (D1).**

Seat `R40C2HeldoutGen`, leaf. Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` (not touched; `git status`
shows only untracked `.ufo/waves/round-40/` and the draft `plans/round-40-claims.md`). Writes: this
report and `/.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/` only. No VCS mutation, no REA run on a
C1 carrier or on a C2 held-out carrier, no subagent, no background job left running, no tool installed
or upgraded (so no authorization entry). Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C2HeldoutGen`
removed at the end; everything cited is inside the artifacts dir.

---

## 1. What landed

| file (under `artifacts/R40C2HeldoutGen/`) | sha256 | what |
|---|---|---|
| `heldout-gen-v2.py` | `ffa6492e…e176a34` | the generator (1 command, 26 carriers, manifest, optional REA runs) |
| `audit-dev-run.py` | `f70f6ae5…b847a` | re-derives the feature table from the envelopes and fails on drift |
| `dev-run/` | 1.7 MB | the delivery: `manifest.json`, `features.json`, `feature-table.md`, and per carrier `carrier.sqsh`, `tree.json`, `envelope.json.gz`, `rea-full.json.gz`, `run.json` |
| `dev-run/manifest.json` | `62104b93…28846` | seed `sha256("dev40")`, 13 classes, 26 carriers, `label_actions`, `action_set`, `action_source`, per-carrier `label`/`action`/`sha256`/`damage` |
| `bound-table-v2-block.md` | `5122a03e…deda6c` | byte-copy of `R40C2Interp/v2-block.md` — the table the delivered `expected_action` tokens are bound to (provenance sidecar `.provenance.txt`) |
| `determinism.txt` | `0ffee808…45595c` | tool versions + the 6-check determinism transcript |
| `v1-table-on-v2-dev-set.txt` | `ae44dc4b…b9995d` | the frozen round-39 v1 table scored on the 26 dev envelopes |
| `interpreter-vs-generator.txt` | `2fa5150f…b0aa9` | the working v2 interpreter scored on the 26 dev envelopes |

## 2. The generator

```
python3 -I -B heldout-gen-v2.py --seed HEX --out DIR [--classes a,b,...] [--run] [--gzip]
                                [--ood-op NAME] [--actions-set NAME] [--actions-file PATH]
                                [--gen WRITER] [--scratch DIR]
python3 -I -B heldout-gen-v2.py --seed HEX --selftest
```

Every byte is a function of `--seed`: structure from `random.Random(int(seed[:16],16) ^ (class_index*1000+k))`,
file contents from a SHA-256 counter stream keyed by (seed, class, k, path). No clock, no `urandom`, no
directory order. Writer: `tools/round-39/gen-squashfs.py` (sha256 `f535e60e…41188`), loaded by path with
the round-39 block-encoder fix (gzip/zlib, xz container + comp id 4) — unchanged from round 39.

### Classes (13, 2 replicates each) and the pair each replicate must draw

| class | label | action (bound set `interp`) | endian | comp | tree / content | symlinks | damage | arm |
|---|---|---|---|---|---|---|---|---|
| clean-be | clean | none | be | k | random/stream | — | — | after |
| clean-le | clean | none | le | k | random/stream | — | — | after |
| clean-empty | clean-empty | confirm-empty | k | k | one empty dir | — | — | after |
| escaping-symlink-removed | escaping-symlink-removed | expect-link-absent | k | k | random/stream | 1 escaping | — | after |
| in-tree-symlink-metadata | in-tree-symlink-metadata | count-gap | k | k | random/stream | 1 in-tree | — | after |
| mixed-symlinks | mixed-symlinks | audit-symlinks | k | k | random/stream | 1 escaping + 1 in-tree | — | after |
| dep-missing-be | dep-missing-be | install-extractor-be | be | k | random/stream | — | — | before |
| dep-missing-le | dep-missing-le | install-extractor-le | le | k | random/stream | — | — | before |
| avm-marker-be-dropped | avm-marker-be-dropped | wrap-extractor-be | avm | k | random/stream | — | — | after |
| body-extractor-failure | body-extractor-failure | preserve-failure | be | k | random/pattern | — | zero-id-table (P=0) | after |
| partial-body-failure | partial-body-failure | salvage-partial | be | k | random/pattern | — | corrupt_partial (P>0) | after |
| no-squashfs-chunk | no-squashfs-chunk | inspect-input | k | k | random/stream | — | s_major 4→9 | after |
| out-of-domain | unclassified | none | k | k | random/stream | — | — | ood |

`k = 1` ⇒ gzip, `k = 2` ⇒ xz; `endian = k` ⇒ `k=1` big-endian, `k=2` little-endian. So the two
replicates of every class differ in compression **and** tree shape, plus endianness for the six classes
whose row is `squashfs_v4_*`/handler-agnostic. Classes whose row pins one endianness (clean-be/clean-le,
dep-missing-be/le) or the AVM marker keep it in both replicates. `manifest.replicate_variation` records
the axes.

The avm class is the round-39 recipe (`gen-squashfs.py --endian avm`: BE magic with
`mkfs_time := bytes_used`, a marker-only **standard-BE** body). Genuine AVM layout is R40-C1's ground and
is not generated here.

### Expected pair assigned before any run, and the action binding

`manifest.json` is written by `build_set()` **before** the `--run` loop; the pair comes from the class
alone. The label is fixed per class. The action token is not paraphrased from prose: the generator
carries all three wave-1 candidate vocabularies verbatim in `ACTION_SETS`
(`tabledraft`, `interp`, `actionreview`) and the freeze selects one:

```
--actions-set interp --actions-file <SKILL.md-or-block>
```

`--actions-file` reads the `<!-- sqfs-triage-actions: ... -->` line and **refuses** (exit 1, exact
missing/extra token lists) when the selected set is not that line's vocabulary; `none` is treated as the
implicit no-match default, not a row token. Carriers never depend on tokens: the same seed under all
three sets yields an identical carrier-sha256 list (measured, §4). The delivered dev-run is bound to
`interp` (`action_set: interp`, `action_source.sha256 = 5122a03e…`); a bare run defaults to
`tabledraft` — see D2.

### Out-of-domain binding

`out_of_domain_run(entry, scratch, keep_extraction, gz, operation=DEFAULT_OOD_OP)` is the placeholder the
task asked for: the operation is the CLI `--ood-op`, is echoed into `manifest.out_of_domain.operation`,
and takes no output dir. Default `inspect-firmware-regions` (REA 6.5.0, provider **binwalk** 3.1.0 at
`/usr/bin/binwalk` sha256 `5fc19aac…0a40d6`). Measured on a clean BE carrier: exit 0, `ok:true`, full
Evidence envelope, `operation = "inspect_firmware_regions"`, `provider.id = "binwalk"`, no chunks, no
files. `inspect-artifact` / `extract-artifact` / `analyze` / `inspect` are **unusable** for this class:
they exit 1 with `{"ok":false,"error":{"code":"target_unavailable", ... "unsupported binary format"}}`
and emit no Evidence envelope. See §6 for the guard limitation this leaves.

### Hooks `corrupt_partial` and `empty_tree`

Both are named functions in the generator and self-contained on purpose: the frozen carrier set must not
depend on a wave artifact whose bytes may move. The algorithm is the one the sibling seats specified —
`corrupt_partial` zeroes the **last compressed, non-sparse data block of the last regular file in
directory-scan order** (the extractor writes every earlier file, then fails), and `empty_tree` builds a
valid image whose only content is one empty directory.

* `corrupt_partial` parses the image with an embedded pure-stdlib SquashFS 4.0 reader (superblock →
  inode table metadata → per-inode block list), so it works for both endiannesses and both compressors
  and never uses a fixed offset. Preconditions fail loudly: ≥2 regular files, a compressed block exists,
  the damaged file must not be the first in scan order.
* Cross-checked against the sibling's independent implementation
  (`R40C2ReconPartial/sqfs-corrupt.py`): on the delivered H21 it lists the same last file
  (`pxb_cv71/q9kr7/wjwxki-xh`, 4 compressed blocks) my manifest records as damaged at offset 1469/len 34;
  on H22 the same (`z95-1xy`, 3 blocks, offset 1012/len 84). On H01 (stream content) it marks every
  block **R**aw — which is exactly why the partial class uses compressible content: a raw block cannot be
  damaged into a decompression failure.
* `empty_tree` uses one empty directory (the round-39 measured `full-be-dirempty-gzip` vector). The
  sibling recon's root-only variant T4 produces the same v2 feature vector (handler present, `G=∅`,
  `SR=no`, `P=0`; `R40C2ReconEmpty/features.tsv` T4-be/le-gzip), so the class is not sensitive to which
  empty shape is used; the generator pins one and records it (`tree: "empty"`).

## 3. Dev run — seed `sha256("dev40")` = `96832afb…341715`

26 REA runs, all exit 0, every envelope's subject digest equals its carrier (`digest-ok`). Measured
feature vectors (`dev-run/feature-table.md`, machine form `features.json`):

| carrier | class | end/com | H | G | D | -be | SR | P | operation/provider |
|---|---|---|---|---|---|---|---|---|---|
| H01/H02 | clean-be | be/gz, be/xz | squashfs_v4_be | none | none | n/a | no | 8 / 6 | extract_firmware/unblob |
| H03/H04 | clean-le | le/gz, le/xz | squashfs_v4_le | none | none | n/a | no | 3 / 3 | extract_firmware/unblob |
| H05/H06 | clean-empty | be/gz, le/xz | squashfs_v4_be/le | none | none | n/a | no | 0 / 0 | extract_firmware/unblob |
| H07/H08 | escaping-symlink-removed | be/gz, le/xz | squashfs_v4_be/le | none | none | n/a | **yes** | 5 / 7 | extract_firmware/unblob |
| H09/H10 | in-tree-symlink-metadata | be/gz, le/xz | squashfs_v4_be/le | unpublished-entry | none | n/a | no | 7 / 6 | extract_firmware/unblob |
| H11/H12 | mixed-symlinks | be/gz, le/xz | squashfs_v4_be/le | unpublished-entry | none | n/a | **yes** | 8 / 6 | extract_firmware/unblob |
| H13/H14 | dep-missing-be | be/gz, be/xz | squashfs_v4_be | missing-extractor-dependency | **sasquatch-v4be** | n/a | no | 0 | extract_firmware/unblob |
| H15/H16 | dep-missing-le | le/gz, le/xz | squashfs_v4_le | missing-extractor-dependency | **sasquatch** | n/a | no | 0 | extract_firmware/unblob |
| H17/H18 | avm-marker-be-dropped | avm/gz, avm/xz | squashfs_v4_be | extractor-failure | none | **no** | no | 0 | extract_firmware/unblob |
| H19/H20 | body-extractor-failure | be/gz, be/xz | squashfs_v4_be | extractor-failure | none | **yes** | no | 0 | extract_firmware/unblob |
| H21/H22 | partial-body-failure | be/gz, be/xz | squashfs_v4_be | extractor-failure | none | **yes** | no | **8 / 4** | extract_firmware/unblob |
| H23/H24 | no-squashfs-chunk | be/gz, le/xz | **none** | none | none | n/a | no | 0 | extract_firmware/unblob |
| H25/H26 | out-of-domain | be/gz, le/xz | none | none | none | n/a | no | 0 | **inspect_firmware_regions/binwalk** |

`audit-dev-run.py` re-derives all of it from the envelopes and re-checks the oracle: **375 checks, 0
failed** (manifest label/action per class, action ∈ declared vocabulary, domain operation/provider,
handler class, gap-kind set, gap-dependency set, `-be` token, MalformedSymlink report, P class, every
oracle regular file published under a suffix-equal path with an equal sha256, no escaping-symlink path
published, and one unpublished-entry gap per in-tree link). Counts: **26 carriers, 12 labels, 12 distinct
(label, action) decisions** — the two replicate envelopes of a class are *not* counted as a second
decision, so "20 means 20 decisions" (R39-CL3) becomes "26 envelopes ↔ 12 decisions" with the 12
decisions each measured twice on non-decision variation.

### The three discriminating pairs this set measures

* **clean-empty vs clean vs no-chunk**: all three are `G=∅, SR=no`; `P` separates empty (0) from clean
  (>0), and the handler separates both from no-chunk. H05/H06 are also the only P=0 carriers that still
  carry a `squashfs_v4_*` handler with no gap.
* **mixed vs escaping vs in-tree**: `SR` alone cannot separate mixed from escaping (both `yes`); `G`
  alone cannot separate mixed from in-tree (both `{unpublished-entry}`); only the conjunction does, and
  only if the mixed row precedes the escaping row or the escaping row pins `G=∅`.
* **partial vs body vs avm-marker**: all `G={extractor-failure}`, all BE handlers. `P` separates partial
  (>0) from body (0); the `-be` token separates body (`yes`) from avm-marker (`no`). Measured on both
  compressors for each.

### Scored against the two interpreters (read-only)

| interpreter / table | result |
|---|---|
| `tools/round-39/sqfs-triage.py` with base `SKILL.md` (v1 block 18) | **18/26** labels agree; **9** distinct v1 rows over 26 envelopes |
| `R40C2Interp/sqfs-triage-v2.py` with its own block (copy `bound-table-v2-block.md`) | **26/26** (label, action) pairs agree |

v1's eight mismatches are exactly the four routed defects, two envelopes each:
`clean-empty → unclassified` (R39-CL3 D2), `mixed-symlinks → escaping-symlink-removed` (R39-CL2),
`partial-body-failure → unclassified` (R39-CL3 D1), `out-of-domain → no-squashfs-chunk` (R39-CL1 —
v1 has no domain guard, and its no-chunk row matches a binwalk envelope). Full transcripts:
`v1-table-on-v2-dev-set.txt`, `interpreter-vs-generator.txt`.

## 4. Determinism

`--selftest` builds all 13 classes three times (twice with the seed, once with it reversed) and compares
manifest bytes and every carrier sha256:

```
PASS  same seed: manifest bytes identical  62104b933d9ca90f vs 62104b933d9ca90f
PASS  same seed: every carrier sha256 identical  26 carriers
PASS  same seed: carrier ids identical  H01..H26
PASS  different seed: manifest differs  62104b933d9ca90f vs 743bdbda9d7cd552
PASS  different seed: every carrier differs  26/26 differ
PASS  replicate variation: no class has two identical carriers  26 distinct of 26
all 6 selftest checks passed
```

The manifest sha256 the selftest reproduces (`62104b93…28846`) is the delivered `dev-run/manifest.json`
sha256, so the delivery is reproducible from the seed. Action tokens do not reach carrier bytes:
`--actions-set tabledraft | interp | actionreview` produce an identical carrier-sha256 list (checked;
carriers were also unchanged across the earlier manifest-schema changes).

## 5. Commands (exact, for the freeze)

```sh
S=/fast/scratch/hyaku/kaidoku-r40/<seat>; mkdir -p "$S"; export TMPDIR="$S"
G=<lane>/.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/heldout-gen-v2.py
SEED=$(git -C <lane> rev-parse FREEZE)

# 1. regenerate carriers + manifest from the freeze hash and bind the frozen table's tokens
python3 -I -B "$G" --seed "$SEED" --out <fresh> --actions-set <tabledraft|interp|actionreview> \
        --actions-file <lane>/SKILL.md --ood-op <frozen op>

# 2. evidence run (26 REA extract-firmware / 1 out-of-domain op per carrier)
python3 -I -B "$G" --seed "$SEED" --out <fresh> --run --gzip \
        --actions-set <set> --actions-file <lane>/SKILL.md

# 3. re-derive the feature table and fail on drift
python3 -I -B audit-dev-run.py <fresh> --json <fresh>/features.json --md <fresh>/feature-table.md
```

`--run` uses `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` (absolute) and `npx -y rea-agents@6.5.0
extract-firmware --format json --full-output <carrier> <fresh-outdir>` from `$TMPDIR`, never an existing
outdir. The `before` arm removes `$HOME/.local/bin` from the child PATH only (so both sasquatch binaries
are unresolvable while REA still runs). The out-of-domain arm runs the `--ood-op` verb with no outdir.

## 6. Limits and inferences

* **Out-of-domain exercises both guard columns together, not separately.** REA 6.5.0 has no operation
  that (a) produces an Evidence envelope on a SquashFS carrier and (b) keeps provider `unblob` while
  changing the verb; `inspect-firmware-regions` changes operation *and* provider (binwalk). A
  provider-only variant would need a synthetic envelope. The measured pair still proves the guard is
  load-bearing: H23/H24 (no-chunk) and H25/H26 (out-of-domain) are indistinguishable on every v1 feature
  (`H=∅, G=∅, P=0, coverage complete`), so only `operation`/`provider` separates them.
* **`partial-body-failure` P>0 is measured, and its mechanism is [INFERENCE].** Four carriers measured
  (H21 P=8, H22 P=4, plus a lab carrier P=3 and round-39's `full-be1-xz` P=6). The inference is that
  sasquatch extracts in directory-entry order, so damaging the last file guarantees the earlier ones are
  written. The generator enforces the structural preconditions (≥2 files, damaged file not first in scan
  order, compressed block) and fails the build rather than emit a class instance that cannot be partial —
  but the P>0 outcome itself is still a measured, not a proven, property of sasquatch 4.5.1.
* **`clean-empty` tree shape.** One empty directory; the sibling recon's root-only T4 gives the same v2
  feature vector. A tree with only symlinks (their T3/T6) is **not** clean-empty — that is the escaping /
  in-tree ground, so it is not part of this class.
* **Envelope portability.** Envelopes record absolute paths (`subject.local_path`, published file paths,
  `evidence_id` inputs) from the generating host's scratch; `TMPDIR` was
  `/fast/scratch/hyaku/kaidoku-r40/R40C2HeldoutGen`, now removed. The scoring surfaces are the feature
  fields and the subject digest (equals the carrier sha256 in every `run.json`), not those paths.
* **No AVM-layout carriers here.** The `avm` class is the marker-only standard-BE recipe; genuine
  AVM-layout big-endian images and vendor members are R40-C1's evidence and were not built or run.
* **Carriers are included in `dev-run/`** (1.15 MB of the 1.7 MB) so every digest in the manifest is
  checkable without regenerating; drop them if the L1 prefers the round-39 lean layout.
* `--classes` accepts any subset; a class listed twice in `--classes` is collapsed to one.

## 7. Routed defects (freeze blockers for the L1, not for this seat)

* **D1 — three incompatible action vocabularies for the same 11 labels.** `R40C2TableDraft/block.md:30`
  (10 tokens, `clean → accept`), `R40C2Interp/v2-block.md:2` (11 tokens, `clean → none`,
  `clean-empty → confirm-empty`), `R40C2ActionReview/actions.md` §1 (11 tokens incl. `not-comparable`
  for the guard row, `clean → match-oracle`). The manifest can only carry one. The generator refuses to
  emit tokens the bound line does not declare, so a wrong binding fails at generation, not at scoring.
  **The freeze must freeze one line and regenerate the manifest with `--actions-file SKILL.md`.**
* **D2 — default drift.** `DEFAULT_ACTION_SET` is `tabledraft` (the table owner's line) while the
  delivered dev-run is bound to `interp` (`action_set: interp`, `action_source` sha256 `5122a03e…`); a
  bare regeneration would therefore mismatch the Interp table. Pass `--actions-set`/`--actions-file`
  explicitly, or change the two constants before freezing.
* **D3 — TableDraft's vocabulary line omits `none`.** Its table's no-match answer is `none` (their own
  `block.md` note), which is the interpreter's default rather than a row token. The generator treats
  `none` as implicit and does not require it on the line; a counter that requires the emitted action to
  appear on the line verbatim would reject the guard/no-match answer. L1 should state which reading
  holds.
* **D4 — `clean` is one label for two classes.** clean-be and clean-le therefore share a (label, action)
  pair, which is why the set reports **12** distinct decisions over 26 envelopes rather than 13. If the
  frozen table splits `clean-be`/`clean-le` into two labels (the ActionReview proposal does), the
  generator's label for those two classes must be rebound — it is one line in `RECIPES`.
* **D5 — the no-chunk / out-of-domain feature vectors are identical.** Any future table revision that
  drops the `operation`/`provider` guard silently relabels every out-of-domain envelope as
  `no-squashfs-chunk`; H25/H26 are the regression pair.

## 8. Evidence index

| evidence | where |
|---|---|
| feature table (26 rows, 12 columns) | `dev-run/feature-table.md`, `dev-run/features.json` |
| per-carrier run record (arm, argv, exit code, digest match, shape) | `dev-run/H*/run.json` |
| carrier digests, dparams, damage offsets | `dev-run/manifest.json` (`carriers[]`, `damage`) |
| oracle trees | `dev-run/H*/tree.json` |
| determinism transcript + tool versions | `determinism.txt` |
| v1 table vs this set | `v1-table-on-v2-dev-set.txt` |
| v2 interpreter vs this set | `interpreter-vs-generator.txt` |
| bound table bytes + provenance | `bound-table-v2-block.md`, `bound-table-v2-block.provenance.txt` |
