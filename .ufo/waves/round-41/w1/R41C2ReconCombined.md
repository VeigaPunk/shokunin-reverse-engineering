**Verdict: CONFIRMED (hypothesis) — DEFECTS FOUND (three holes in the draft v3 precedence, one live v2 mislabel, one live silent-clean trap in the frozen recipe), all measured on real REA 6.5.0 envelopes.**

A gzip partial-body failure that also holds an in-tree symlink carries exactly
`G = {extractor-failure, unpublished-entry}`, `SR = no`, `P = 8 > 0`, `BE = yes`; adding one
escaping symlink adds `SR = yes` and nothing else. The frozen v2 interpreter answers
`unclassified/none` to the first and `escaping-symlink-removed/expect-link-absent` to the second
(R40-CL5 confirmed, plus a *wrong label*, not just a fall-through). The draft v3 precedence labels
all four partial-combined shapes `partial-body-failure` and reproduces the 26 round-40 held-out
labels 26/26, but it cannot be frozen as written: it has no action token for `depth-limited-nested`,
its rule 7 makes the label a function of the `--max-depth` arm (same bytes, three different answers),
and the frozen `0x00` fill still yields a completely silent `clean` envelope over an all-zero
published file on xz.

Seat `R41C2ReconCombined`, leaf. Wrote only
`.ufo/waves/round-41/w1/R41C2ReconCombined.md` and
`.ufo/waves/round-41/w1/artifacts/R41C2ReconCombined/`. No VCS mutation; no subagent; no background
job; never messaged `agent://all`. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2ReconCombined`
removed at exit. No vendor firmware byte was fetched, copied or cited — every carrier below is
synthetic and rebuilt by the frozen round-40 writer. No tool installed, upgraded or moved.

## 1. What ran

Sixteen REA `extract-firmware` runs on 11 of the 17 dev carriers built from the frozen round-40
code, plus eight direct `sasquatch-v4be` runs (the four determinant probes and the four
semi-compressible carriers). Environment (measured):

```
python 3.14.8 · uname 7.2.11-arch1-1 · node v24.21.0
unblob 26.6.4 · sasquatch-v4be 4.5.1 (unsquashfs version 4.5.1 2022/03/17)
rea-agents 6.5.0 (package.json version, npx cache ad9a3fdbcad992c6)
```

Every REA run is exactly:

```
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output [--max-depth 1] <carrier> <fresh outdir>
```

Frozen inputs, read out of the lane at the base revision (`git show`, no checkout):

| file | sha256 |
| --- | --- |
| `tools/round-40/gen-squashfs.py` | `309c502d21dfeef9b7b2a5a9a62bfa875270fdf79eec671461070996d291042e` |
| `tools/round-40/heldout-gen-v2.py` | `644d8f6e44e0a46dfed0be4e8bfc4a365094b7f10b9415b2a7c5b2b98662af85` |
| `tools/round-40/sqfs-triage-v2.py` | `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617` |
| `SKILL.md` | read at base, not copied into artifacts |

Recipes (`build-combined.py`, `absorb-probe.py`): the tree comes from the frozen
`heldout-gen-v2.build_tree` (same `in-tree` / `escaping` link kinds, same `pattern` / `stream`
content), the image from the frozen `gen-squashfs.build_image(tree, out, 'be', comp)`, and the
damaged block from the frozen `heldout-gen-v2.corruption_partial` — its own selector picks
"the last compressed block of the last-extracted regular file" and reports
`path/block_offset/block_length/file_size/files`. **One variable differs from the round-40 frozen
partial recipe: the fill byte written over that block** (`0x00` in the frozen recipe, `0xff` here
where noted, per MH-4). The block selector is untouched, so a `--fill 00` rebuild is the frozen
recipe on a tree that also carries links. Rebuilds are byte-identical: two independent builds of
`gzip-ff-intree` produced `09cf1e08ee0661b1…` twice.

## 2. The hypothesis, envelope by envelope

`G` gap kinds, `BE` `-be` in the recorded child argv, `SR` a `MaliciousSymlinkRemoved` report,
`P` published entries. Columns are the *independently recomputed* features (`feature-scan.py`,
which imports nothing from the interpreter); the interpreter's own feature line agreed with every
row (its `PV` = my `PR` = `unblob`, `H` = `[squashfs_v4_be]` everywhere).

| carrier (sha256) | build | arm | G | SR | BE | P | damaged file as published |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gzip-ff-intree` `09cf1e08…` | gzip, fill `ff`, in-tree link | `--max-depth 1` | `depth-limited, extractor-failure, unpublished-entry` | no | yes | 8 | `wsw8y` **4096 B** `c18eb0c8…` (oracle 4151 B `9778d2c6…`) |
| `gzip-ff-intree` | same bytes | **no** `--max-depth` | `extractor-failure, unpublished-entry` | no | yes | 8 | same |
| `gzip-ff-mixed` `27ffa67e…` | gzip, `ff`, escaping + in-tree | `--max-depth 1` | `depth-limited, extractor-failure, unpublished-entry` | **yes** | yes | 8 | same `wsw8y` |
| `gzip-ff-mixed` | same bytes | **no** `--max-depth` | `extractor-failure, unpublished-entry` | **yes** | yes | 8 | same |
| `gzip-ff-none` `e4a6df53…` | gzip, `ff`, no links | `--max-depth 1` | `depth-limited, extractor-failure` | no | yes | 8 | same |
| `xz-ff-intree` `fe622cbb…` | xz, `ff`, in-tree | `--max-depth 1` | `depth-limited, extractor-failure, unpublished-entry` | no | yes | 8 | `wsw8y` **0 B** `e3b0c442…` |
| `xz-00-intree` `5aff77bf…` | xz, **`00`**, in-tree | `--max-depth 1` | `depth-limited, unpublished-entry` | no | **n/a** | 8 | `wsw8y` 4151 B `9814547d…` — extractor did **not** fail |

Exact hypothesis checks, from the bare (no `--max-depth`) rows:

* `G = {extractor-failure, unpublished-entry}` — yes, exactly, two elements.
* `SR = no` with only an in-tree link; the link `vvz`→`hrofr/pw902xwzv/g12` is the one and only
  `unpublished_entries` member (`kind: symlink`).
* `P = 8 > 0`; the chunk record is `handler: squashfs_v4_be, extraction_failed: true`; coverage
  `partial`; diagnostics `ExtractCommandFailedReport` with
  `squashfs… command: sasquatch-v4be -be -no-exit-code -f -d …` → `BE = yes`.
* adding one escaping link (`xcw8oqgi`→`../nm59-u3o`) adds `SR = yes` and nothing else: the
  admitted feature vector is unchanged otherwise, the escaped name is in neither `files` nor
  `unpublished_entries`, and diagnostics gain `MaliciousSymlinkRemoved`. **The symlink pass and the
  escaping-link removal both still run after the extractor failed** — this was the open question and
  it is answered yes.

Two facts the draft should state explicitly:

* `--max-depth 1` adds a `depth-limited` gap to *every* run, so the same bytes carry a two-element
  or a three-element `G` depending only on the arm (`gzip-ff-intree` row 1 vs row 2).
* `P > 0` counts published *entries*, not bytes: the xz arm published an **empty** `wsw8y`
  (0 B, `e3b0c442…`) and still reads `P = 8`.

## 3. The frozen v2 interpreter on these bytes

| run | G | SR | v2 (label, action) | v2 rule |
| --- | --- | --- | --- | --- |
| `gzip-ff-intree` (d1) | 3 kinds | no | `(unclassified, none)` | no row |
| `gzip-ff-intree` (no d1) | 2 kinds | no | `(unclassified, none)` | no row |
| `gzip-ff-mixed` (d1 and no d1) | 2/3 kinds | yes | **`(escaping-symlink-removed, expect-link-absent)`** | `gap kinds = *` |
| `gzip-ff-none` (d1) | `depth-limited, extractor-failure` | no | `(unclassified, none)` | no row |
| `clean-mixed` `8e829d9d…` (no d1) | `unpublished-entry` | yes | `(mixed-symlinks, audit-symlinks)` | correct |
| `clean-mixed` (d1) | `depth-limited, unpublished-entry` | yes | **`(escaping-symlink-removed, expect-link-absent)`** | `gap kinds = *` |
| `clean-intree` `8e1aeb36…` (d1) | `depth-limited, unpublished-entry` | no | `(unclassified, none)` | no row |
| `clean-none` `6f0537e3…` (d1) | `depth-limited` | no | `(unclassified, none)` | no row |
| `xz-00-intree` (d1) | `depth-limited, unpublished-entry` | no | `(unclassified, none)` | no row |

Three findings, in order of severity:

1. **R40-CL5 reproduced on real envelopes.** Every combined set falls out of the exact-set gap
   cells: `partial-body-failure` requires `G` to equal exactly `{extractor-failure}`, so a partial
   failure with an in-tree link (or with `depth-limited`) is `unclassified`.
2. **New: an active mislabel, not a fall-through.** The `escaping-symlink-removed` row declares
   `gap kinds = *` and `symlink removed = yes`, and every row below it demands an exact gap set, so
   **any** `SR = yes` envelope is labelled "one or more symlinks escaped and were
   removed" and told to materialise nothing, even when the envelope also reports an extractor
   failure and in-tree `unpublished-entry` gaps. The v2 table's own comment
   ("a table whose escaping row matches on SR alone reports the wrong action. R39-CL2") describes
   exactly this, and the row was not narrowed. `clean-mixed` proves it on **undamaged** bytes:
   correct without `--max-depth`, wrong with it.
3. **The plain round-40 class is arm-sensitive too.** `gzip-ff-none` (partial failure, no links,
   `--max-depth 1`) is `unclassified`. The committed held-out set never saw this because it ran
   without `--max-depth` (H21/H22: `G = [extractor-failure]`, `P = 5` / `3`, `BE = yes`).

## 4. The draft v3 precedence, applied

`v3-precedence.py` is a transcription of the twelve numbered sentences of
`plans/round-41-claims.md` §R41-C2 into code; it reads no table, no interpreter and no generator.

**No regression on committed labels.** Over the 26 committed round-40 held-out envelopes
(`corpus/evidence/round-40/c2/heldout/`): **0 mismatches** against `manifest.json`'s
(label, action) pairs, matched rule by rule — H01–H04 r11, H05–H06 r11, H07–H08 r9, H09–H10 r10,
H11–H12 r8, H13–H16 r3, H17–H18 r5, H19–H20 r6, H21–H22 r4, H23–H24 r2, H25–H26 r1
(`heldout-regression.txt`).

Applied to my sixteen dev envelopes:

| run | draft-v3 label | rule | action |
| --- | --- | --- | --- |
| `gzip-ff-intree` (d1 and no d1) | `partial-body-failure` | 4 | `salvage-partial` |
| `gzip-ff-mixed` (d1 and no d1) | `partial-body-failure` | 4 | `salvage-partial` |
| `gzip-ff-none` (d1) | `partial-body-failure` | 4 | `salvage-partial` |
| `gzip-00-intree` (d1) | `partial-body-failure` | 4 | `salvage-partial` |
| `xz-ff-intree` (d1) | `partial-body-failure` | 4 | `salvage-partial` |
| `clean-mixed` (no d1) | `mixed-symlinks` | 8 | `audit-symlinks` |
| `clean-mixed`, `clean-intree`, `clean-none`, `xz-00-intree`, `absorb-*` (d1) | `depth-limited-nested` | 7 | **UNBOUND** |
| `absorb-gzip-00` (no d1) | `clean` | 11 | `none` |

The four combined shapes the claim asks for are all realisable and all labelled as the prose says:
`{extractor-failure, unpublished-entry}` (SR no / SR yes), `{depth-limited, unpublished-entry}`
(SR no / SR yes), `{depth-limited}` alone, plus the three-element d1 shapes.

### 4.1 Hole H1 — no action token for the new label

`depth-limited-nested` is named as a new label but no action. The v2 vocabulary line
(`<!-- sqfs-triage-actions: … -->`, 11 tokens) has no token for it, and the interpreter refuses a
table whose action cell is undeclared (exit 2). Six of sixteen envelopes land on that label, so the
claim's predicate — "the (label, action) pair that the frozen independent evaluator gives it" —
cannot be satisfied until a token is declared and added to `ACTION_SETS` / `label_actions`.
Second-order: if the combined shapes are meant to keep `salvage-partial` (rule 4), then the *only*
new row is the depth-limited one; but then `partial-body-failure`'s action silently drops the symlink
audit for the mixed case (`gzip-ff-mixed` → `salvage-partial`, never `audit-symlinks`). Either is
defensible; the draft does not say which.

### 4.2 Hole H2 — rule 7 makes the label a function of the run arm

Same carrier bytes `8e829d9d9ea0be5c…`, three answers:

| arm | G | v2 | draft-v3 |
| --- | --- | --- | --- |
| no `--max-depth` | `{unpublished-entry}` | `mixed-symlinks / audit-symlinks` | `mixed-symlinks / audit-symlinks` |
| `--max-depth 1` | `{depth-limited, unpublished-entry}` | `escaping-symlink-removed / expect-link-absent` | `depth-limited-nested / UNBOUND` |

Because rule 7 precedes rules 8–10 ("whatever symlink gaps accompany it"), **any** `--max-depth 1`
success envelopes becomes `depth-limited-nested`, including the in-tree class
(`clean-intree-d1`: `{depth-limited, unpublished-entry}`, SR no → `depth-limited-nested`). So the
combined-depth classes are not distinguishable from their non-depth siblings by label alone, and the
held-out set's expectation depends on the arm rather than on the carrier. Two consistent ways out:
carry the depth arm as part of the carrier identity in the manifest and pin it per class (the C1
side already runs everything `--max-depth 1`), or move rule 7 below rules 8–10 and accept that a
depth-limited+mixed carrier then reads `mixed-symlinks`. The claim's stated intent
("labels COMBINED gap sets … depth-limited + symlinks") requires the first.

### 4.3 Hole H3 — `BE = n/a` is the success-path value, not `no`

Every success-path envelope in my set records **no diagnostics at all**, so `BE = n/a`:
`clean-mixed` (both arms), `clean-intree-d1`, `clean-none-d1`, `absorb-*-d1`, `xz-00-intree-d1`, and
the committed H01/H07/H09/H11 (`BE = n/a`). `BE = no` is only observable on a failure arm, which is
the only place rule 5 uses it — so rule 5 is safe, but the table's `-be in child argv` column and
the v3 documentation must say `n/a ≠ no`. `BE` is **not** an artifact of `--full-output`: the same
carrier without that flag returns the bare evidence document (`gzip-ff-intree-lite`) with
`G` unchanged and the child argv still recorded (`sasquatch-v4be -be …`), hence `BE = yes`.

## 5. The compressed-length determinant (MH-4), measured on the frozen writer

`absorb-probe.py` builds one tree (`a/one` 100 B, `a/two` 200 B, `a/zz-big` 3000 B semi-compressible)
so that the frozen selector lands on a *large* block, then rewrites that block with the fill byte.
Direct extractor runs use unblob's own argv shape (`sasquatch-v4be -be -no-exit-code -f -d`):

| carrier | codec | fill | damaged block | direct extractor | REA |
| --- | --- | --- | --- | --- | --- |
| `gzip-00-intree` `f9f9e035…` | gzip | `00` | 19 B (`wsw8y`, 4151 B) | rc 1, `FATAL ERROR` | `extractor-failure` |
| `gzip-semi-00-intree` `96a46a77…` | gzip | `00` | 50 B | rc 1, `FATAL ERROR`, 8 published | — |
| `absorb/gzip-00` `573cad18…` | gzip | `00` | **1704 B** | **rc 0**, 3 published, `Detected lzma-ddwrt compression` | **`clean`, coverage `complete`, 0 gaps** |
| `gzip-ff-intree` | gzip | `ff` | 19 B | rc 1, FATAL | `extractor-failure` |
| `gzip-semi-ff-intree` `fadf8d03…` | gzip | `ff` | 50 B | rc 1, FATAL, 8 published | — |
| `absorb/gzip-ff` `7c7940e5…` | gzip | `ff` | 1704 B | rc 1, FATAL, 3 published | — |
| `xz-00-intree` `5aff77bf…` | xz | `00` | 148 B | absorbed | `{unpublished-entry}` only |
| `xz-semi-00-intree` `e17f77b3…` | xz | `00` | 2232 B | **rc 0**, `Detected lzma-ddwrt compression` | — |
| `absorb/xz-00` `94dabd05…` | xz | `00` | 1652 B | **rc 0**, 3 published | `{depth-limited}` only |
| `xz-ff-intree` | xz | `ff` | 148 B | rc 1, FATAL | `extractor-failure` |
| `xz-semi-ff-intree` `ec5ee46b…` | xz | `ff` | 2232 B | rc 1, FATAL | — |
| `absorb/xz-ff` `a258ac26…` | xz | `ff` | 1652 B | rc 1, FATAL, 3 published | — |

So: the determinant is the **damaged block's compressed length**, not the fill byte alone.
`0x00` fails at 19 B and 50 B on gzip and is absorbed at 1704 B; on xz it is absorbed at every length
this writer produces (148 B … 2232 B). `0xff` fails at every length measured on both codecs
(19/50/1704 B gzip, 148/1652/2232 B xz). [INFERENCE: after the header check fails, sasquatch
re-detects the codec — the stderr line `Detected lzma-ddwrt compression` appears in both absorbed
arms — and the fallback decoder emits a zero run long enough to satisfy the block's expected output
length; the larger the zeroed block, the more zero bytes it can satisfy.]

**Consequence, measured end-to-end.** `absorb-gzip-00-nod1` is a genuine REA envelope, `ok: true`,
`coverage: complete`, `extraction_gaps: []`, `P = 3`, and the published
`firmware.bin_extract/a/zz-big` is **3000 bytes of zeros** (first differing offset 0, 3000 trailing
zero bytes, sha `c81ca5ed…` vs oracle `3698cca0…`). No table, v2 or v3, can label that anything but
`clean`. This is MH-4's forward finding, now on the frozen writer's own bytes for both codecs.

**Consequence for the held-out design.** The frozen partial recipe's two replicates vary compression
(v2's H21/H22 escaped only because both were pinned to gzip). With the frozen `0x00` fill, an xz
replicate of a combined partial class does not fail at all: on identical trees and links,
`gzip-00-intree` → `extractor-failure` while `xz-00-intree` → absorbed. The claim's own check
("the generator's own class expectation agrees with the evaluator on every envelope") would then
either fail loudly or, worse, pass because generator and table share the class map. `0xff`, or
pinning the partial classes to gzip, removes the hazard: every `ff` arm above failed at every length
on both codecs.

## 6. Publication semantics worth pinning in the v3 prose

* `P` counts published entries including zero-byte ones (xz-ff published `wsw8y` at 0 B).
* A failed extraction publishes a **truncated** file (`wsw8y` 4096 B of 4151) or an **empty** one;
  the sha never matches the oracle, and REA raises nothing because it compares against unblob's own
  post-write hash. Salvage therefore cannot be "files present ⇒ files good".
* The damaged block is the *last* compressed block of the last-extracted file, so its compressed
  length is a property of tree shape and file size, not of the recipe alone — which is exactly why
  the frozen recipe is fragile across seeds.
* The kept in-tree link is one `unpublished_entries` entry and one `unpublished-entry` gap; the
  removed escaping link is neither published nor counted, only reported
  (`MaliciousSymlinkRemoved`). This holds after an extractor failure.

## 7. Recommendations for the freeze (minimal, each backed above)

1. **Declare the action for `depth-limited-nested`** (and say whether combined partial shapes keep
   `salvage-partial` or get an audit-carrying action). Without a token the v3 table is unfreezable
   (H1; §4.1).
2. **Make the depth arm part of the carrier identity** — record `--max-depth` per held-out carrier
   and state in the predicate that labels are read on that arm; otherwise rule 7 relabels every
   d1 success envelope and the combined-depth classes collide with their siblings (H2; §4.2).
3. **Repair the escaping row if any v2 row is carried into v3**: `gap kinds = *` with
   `symlink removed = yes` is the wrong-answer row (R39-CL2's own comment), measured live on
   `clean-mixed-d1` and on both partial+mixed arms (§3, finding 2).
4. **Change the corruption fill to `0xff` and assert the measured tuple at build time**
   (`extraction_failed: true`, `files > 0`); or pin every partial class to gzip. Otherwise an xz
   replicate is silently `clean` with an all-zero published file (§5).
5. If any cause text is carried over, drop "match files to the oracle only by relative-path
   suffix" from the `partial-body-failure`/`clean` rows: R40-CL1 ruled that join out, and C2 prose
   that re-teaches it would reintroduce the counter defect on the C2 surface.

## 8. Evidence index (`artifacts/R41C2ReconCombined/`)

| file | content |
| --- | --- |
| `envelopes/<run>.json.gz` | the full `--format json --full-output` envelope of each of the 16 runs, `mtime=0` gzip; every `subject.digest.sha256` equals its carrier's pin |
| `envelopes/*.stderr.txt` | REA stderr where non-empty (all empty) |
| `PINS.tsv` | carrier sha256 + size + build variables + which runs cite that subject digest (17 carriers, 16 runs, no unmatched pin) |
| `recipes/<carrier>.recipe.json`, `<carrier>.tree.json` | build recipe (codec, fill, links, damage block offset/length, image sha) and the tree oracle |
| `recipes/absorb-*.probe.json`, `direct/absorb-*.{stdout,stderr}.txt` | the determinant probe and the direct `sasquatch-v4be` transcript |
| `features.jsonl`, `features.md` | independently recomputed `OP PR H G D BE SR P` per run + the v2 pair per run |
| `v3.jsonl`, `v3-heldout.jsonl`, `heldout-regression.txt` | draft-v3 precedence on my 16 envelopes and on the 26 committed held-out ones (0/26 mismatches) |
| `build-combined.py`, `absorb-probe.py`, `feature-scan.py`, `v3-precedence.py`, `run-all.sh` | every probe, pure stdlib, re-runnable |
| `sqfs-triage-v2.py` | byte copy of the frozen interpreter (`336c621c…`) so `feature-scan.py` runs self-contained |

Tool sha256: `build-combined.py 7cd899b6…`, `absorb-probe.py 9591577e…`,
`feature-scan.py 5479d8e4…`, `v3-precedence.py 479caa5f…`, `run-all.sh 522d51ea…`.
Reproduce everything with `S=<scratch> bash run-all.sh` (needs the lane checkout at the base
revision for the two frozen tools and `SKILL.md`, `unblob`, `sasquatch-v4be`, `npx`).

## 9. Bounds compliance

Wrote only the report and the artifacts directory above; nothing in `corpus/`, `tools/`, `plans/`,
`PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `LOG.md`, the fleet repo outside the lane,
`/home/vgpnk/Projects/shokuknow`, or any PATH directory. VCS read-only (`git show`, `rev-parse`,
`ls-tree`); no `git add/commit/checkout/reset/stash/pull/push`, no jj. No REA/unblob/sasquatch run
touched any reserved image or member (3490/5490/5491/7560, L3/L4) — no vendor byte was fetched at
all. Scratch and `TMPDIR` under `/fast/scratch/hyaku/kaidoku-r41/R41C2ReconCombined`, removed at
exit; no `find`/`du` sweep under `/fast/scratch` (one `find` inside my own run outdirs, for the
published file). No install, upgrade or move of any tool.

## 10. Risks and limits

* All carriers are synthetic; the 5490/5491 AVM-layout vendor bodies were not touched, and nothing
  here tells the L1 whether a *vendor* AVM body behaves like these standard-BE bodies under the same
  combined sets (the `-be` arm is yes in both cases, so the labels should not move — [INFERENCE]).
* One tree per class: tree shape drives the damaged block's compressed length, so the per-class
  tuples are stable only because the fill is `ff` (§5).
* The `escape`/`in-tree` link construction is the frozen generator's, not the vendor's; a real vendor
  image with symlinks at depth > 1 under `--max-depth 1` could additionally mint `depth-limited` on a
  *nested* chunk, giving four-element `G` sets I did not measure.
* `feature-scan.py` and `v3-precedence.py` implement the draft text as written; both are independent
  of the frozen interpreter and generator, but they are my transcription — the freeze's own
  independent evaluator must still be written separately (round-40 closure D3).
