# R39C2LabMixed — mixed in-tree + escaping symlinks on standard-BE SquashFS v4 (dev recon)

**VERDICT: CONFIRMED** — on every development standard-BE gzip carrier that holds exactly one in-tree
and one escaping symlink, the REA `extract-firmware` after-arm carries **exactly one
`unpublished-entry` gap and one `MaliciousSymlinkRemoved` diagnostic**, and the escaping link's path is
never published (absent from `files[]`, `unpublished_entries[]`, `extraction_gaps[]`, and the published
output tree). Two qualifiers matter for the frozen C2 grammar: the "exactly one" is **per link, not per
image** (2 in-tree links → 2 gaps; 2 escaping links → 2 diagnostics), and for **symlink→symlink chains**
`G` is **order-dependent** while `SR` is not. Item scope: 3 primary + 9 supplementary development BE
gzip carriers plus one non-container input, built and run entirely in scratch; **no K5/K6 carrier was run through REA and no held-out
carrier was built**.

Base `a2f64e1da78afcf8cc39287106604dbcc270844c`. Every number below comes from a full `{ok,data,meta}`
CLI envelope saved under `envelopes/` (26 envelopes, two identical repeats per carrier).

## 1. Hypothesis and method

Hypothesis tested: an image holding both one in-tree and one escaping symlink yields exactly one
`unpublished-entry` gap and one `MaliciousSymlinkRemoved` diagnostic, and the escaping link's path is
never published.

Toolchain (all as installed; **no package was installed, upgraded, moved or removed**):
`python3 3.14.8`, `unblob 26.6.4` (`~/.local/bin/unblob`), `rea-agents 6.5.0` via `npx -y`, `sasquatch-v4be`
(unsquashfs 4.5.1). Generator `tools/round-37/gen-squashfs.py` sha256
`1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5`; installed unblob
`squashfs.py` sha256 `2d7b901b…99287`, `extractor.py` sha256 `1bb49811…cd23a`.

Per carrier: tree authored by `make-dev-carriers.py` in scratch, image built with
`python3 tools/round-37/gen-squashfs.py TREE OUT --endian be --comp gzip`, then
`cd "$S" && TMPDIR="$S" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
extract-firmware --format json --full-output images/<C>.sqsh out-<C>-<a|b>/run > env-<C>-<a|b>.json`.
Every run exited 0 with `ok:true`; every envelope's `subject.digest.sha256` equals its carrier hash;
rebuilding all images reproduced the same sha256 (`sha256 -c` OK), and the a/b repeats are
feature-identical. Exact commands and versions: `commands.txt`.

## 2. Primary result (the hypothesis)

| carrier | image links (in-tree / escaping) | `G` = gap kinds | gap count | `unpublished_entries` | `MaliciousSymlinkRemoved` count | `P`=len(files) | `published_bytes` | escaping path published? |
|---|---|---|---|---|---|---|---|---|
| `D1-in-first` (441 B) | `a_in -> hello.txt` / `z_out -> ../outside-d1.txt` | `{unpublished-entry}` | 1 | `a_in` (`kind=symlink`, `link_target=hello.txt`) | 1 (`link=…/z_out`) | 2 | 29 | **no** |
| `D2-out-first` (441 B) | `z_in -> hello.txt` / `a_out -> ../outside-d2.txt` | `{unpublished-entry}` | 1 | `z_in` (`link_target=hello.txt`) | 1 (`link=…/a_out`) | 2 | 29 | **no** |
| `D3-nested-multi` (434 B) | `deep/up_in`, `deep/b_in2` → `../hello.txt` / `deep/out_up -> ../../outside-d3.txt` | `{unpublished-entry}` | **2** | `deep/b_in2`, `deep/up_in` | 1 (`link=…/deep/out_up`) | 1 | 11 | **no** |

Feature text for these three, read from the envelope exactly as the L1 contract prescribes:
`H=['squashfs_v4_be']`, `D=∅`, `BE=n/a`, `SR=yes`, `coverage=partial`.

Exact JSON paths used (all three carriers): `normalized_result.chunks[0].handler == "squashfs_v4_be"`,
`…extraction_failed == false`; each gap at `normalized_result.extraction_gaps[i]` has
`kind=="unpublished-entry"`, `handler==null`, `provider_id==null`, `dependencies==[]`; each metadata row at
`normalized_result.unpublished_entries[i]` has `kind=="symlink"` and a relative `link_target`; each removal at
`normalized_result.diagnostics[j].report` has `__typename__=="MaliciousSymlinkRemoved"`, with **absolute
staging path** `link` and `target`. No `command` field exists on `MaliciousSymlinkRemoved`.

Publication check (`escape-check.txt`, machine-generated over the primary `-a` runs): every escaping
basename occurs only under `normalized_result.diagnostics[].report.link` and the corresponding
`raw_result.report[…].reports[…].link`; it never occurs in `files[].relative_path`,
`unpublished_entries[].relative_path` or `extraction_gaps[].relative_path`. The published output tree
(`out-<C>-a/run`) contains regular files and directories only — **zero symlinks** (REA's `SafeOutputTree`
publishes regular files only).

So the hypothesis's literal wording is confirmed; its "exactly one" is per link, not per image: a second
in-tree link adds a second gap (`D3`), a second escaping link adds a second diagnostic (`D6`).

Supplementary multiplicity carrier: `D6-two-escaping` (`in_link -> hello.txt`, `out_a`, `out_b` → outside)
→ `G={unpublished-entry}`, 1 gap (`in_link`), **2** `MaliciousSymlinkRemoved` diagnostics, `P=1`, `SR=yes`.
`D8-dir-links` (intended dir-symlink arm, see risk R2) behaved as escaping-only: `d_out -> ../outside-d8`
(dangling target) → `G=∅`, 1 diagnostic, `P=2`; a dangling escaping target is removed exactly like a
resolvable one.

## 3. Order dependence for the triage grammar (G, SR)

Two independent links are order-invariant: `D1` (in-tree name sorts before escaping) and `D2` (escaping
sorts first) give the **same** `(G, SR)` = (`{unpublished-entry}`, `yes`).

A **chain** — one link whose target is another symlink that escapes — is not. Mirrored carriers with the
same logical content but swapped names produce different `G`:

| carrier | link layout | `G` | `SR` | diagnostics | interpretation |
|---|---|---|---|---|---|
| `D4-chase-first` | `a_chase -> b_escape`, `b_escape -> ../outside` | **∅** | yes | 2 (`a_chase`, `b_escape`) | chase processed first → `resolve()` follows the escaping link → both removed |
| `D5-escape-first` | `a_escape -> ../outside`, `z_chase -> a_escape` | **`{unpublished-entry}`** | yes | 1 (`a_escape`) | escape removed first → chase now resolves inside → kept as metadata |
| `C1-target-first` | `a_target -> ../outside`, `z_link -> a_target` | `{unpublished-entry}` | yes | 1 | same as D5 with a distinct name pair |
| `C2-chase-first` | `a_chase -> z_target`, `z_target -> ../outside` | ∅ | yes | 2 | same as D4 with a distinct name pair |
| `C3-root-escape` | `a_target -> ../outside` (root), `deep/z_link -> ../a_target` (nested) | `{unpublished-entry}` | yes | 1 | root entry processed before nested |
| `C4-root-chase` | `a_chase -> deep/z_target` (root), `deep/z_target -> ../../outside` | ∅ | yes | 2 | root entry processed before nested |

Mechanism: unblob's sanitiser walks the extraction tree with `directory.iterdir()` (unsorted) and judges
each link with `path.resolve()` + `is_safe_path` (installed `unblob/extractor.py:50-92 (removal branch 81-89; walker 95-115)`,
`file_utils.py:34-39`); `Path.resolve()` follows intermediate symlinks, so whether the chase link resolves
inside or outside depends on whether its escaping target was already unlinked. `C1/C2` isolate naming as
the cause (same semantics, names permuted), `C3/C4` isolate directory traversal (root before children).
The features are deterministic per image (a/b repeats identical) but not a function of the link
semantics; they are a function of extraction order (name order within a directory, directory order above
it) — which the C2 held-out generator cannot promise to preserve across filesystems. **`SR` was `yes` in
all six chain runs**; only `G` (and the diagnostic count) flipped.

Grammatical consequence: a row that selects escaping-link removal by `gap kinds` alone is wrong — the
same chain image can be `G=∅` or `G={unpublished-entry}`. The escaping class must be selected by
`symlink removed = yes` (with `gap kinds = *`, or two rows, see §4); `SR` is the stable discriminator.
Conversely, `G={unpublished-entry}` with `SR=no` is stable (K2-style pure in-tree image).

## 4. What this fixes for the L1's triage table (tested, not proposed blindly)

Advisory reference interpreter `sqfs-triage.py` implements the L1 grammar verbatim (marker →
first table inside `## Queue-drain craft`; exact header; first-match-wins; exact-set cells; malformed cell
→ exit 2) and was run on 33 envelopes: my 26 dev envelopes plus four round-38 after receipts, two
round-38 AVM-probe envelopes, and round-36 `K1/before.json` (`labels-all.json`). Labels obtained:

- 24 × `escaping-symlink-removed`, 2 × `body-extractor-failure`, 2 × `no-squashfs-chunk`,
  2 × `clean`, 1 × `in-tree-symlink-metadata`, 1 × `avm-marker-be-dropped`, 1 × `dep-missing-le`;
  0 × `unclassified`.
- Unevaluable paths verified: bad `-be` cell → exit 2; wrong header → exit 2; missing marker → exit 2
  (also exit 2 on the real lane `SKILL.md`, which has no table yet).

Findings that constrain the frozen table/interpreter (each observed, not inferred unless marked):

1. **`-be` needs a basename prefix rule.** The recorded `ExtractCommandFailedReport.command` is
   `sasquatch-v4be -be -no-exit-code -f -d …` for a body failure (`D7-corrupt-body`: inode table zeroed;
   chunk `extraction_failed=true`, `G={extractor-failure}`, `P=0`, `BE=yes`) and
   `sasquatch-v4be -no-exit-code -f -d …` for the AVM-marker drop (`rea-k1-avm.json`; `BE=no`). If "names
   sasquatch" requires the token to be exactly `sasquatch`, `BE` is always `n/a` and the AVM row can never
   match. Accept a token whose basename is `sasquatch` or starts with `sasquatch-`, and test `-be` as a
   standalone token (never a substring: `-no-exit-code` must not count).
2. **`BE=n/a` on clean/in-tree/escaping runs.** No diagnostic carries a `command` on those paths, so a row
   for them must use `*` for `-be`, or explicitly `n/a`. `D7` shows `-be` is observable only when the
   extractor failed, which is exactly where the AVM/body split needs it.
3. **Exact-set cells cannot express a disjunction.** Escaping-only images give `G=∅`; mixed images and
   order-kept chains give `G={unpublished-entry}`. One cell cannot mean "either", so the escaping class
   needs **two rows** with `symlink removed = yes` (`gap kinds = none` and `gap kinds = unpublished-entry`)
   — or one row with `*`, which then also swallows `extractor-failure` images that happen to carry a
   removal. The two-row form is the safe one; both were exercised (`D4/C2/C4` and `D1/D2/D3/D6`).
4. **Row order is load-bearing.** Any `clean` row with `gap kinds = none` must require
   `symlink removed = no`; otherwise it shadows every escaping-only image (`G=∅`, `SR=yes`). The
   `in-tree-symlink-metadata` row must require `SR = no`. The `SR=yes` rows must precede the `SR=no` rows.
   The advisory fixture puts failure rows (`dep-missing-*`, `avm-marker`, `body-extractor-failure`) first,
   then escaping ×2, then in-tree, clean, and the `handler = none` catch-all last.
5. **`P` must be `len(normalized_result.files)`.** `normalized_result.derivations[]` also lists
   unpublished symlinks as `child_path` (`D1` `derivations[3].child_path = $output/firmware.bin_extract/a_in`),
   so counting derivations over-counts published files.
6. **Mixed images are labelled `escaping-symlink-removed`** under the SR-priority ordering — correct for a
   removal class, but it means the **`in-tree-symlink-metadata` class in `heldout-gen.py` must contain only
   in-tree links** (no escaping link, no chain), or the classifier will (correctly, by its own grammar)
   return the escaping label for an in-tree-class carrier. Likewise `clean` carriers must have no symlink
   at all.
7. `handler = none` is real: a 920-byte plain file yields `H=∅`, `G=∅`, `P=0`, `coverage=complete`
   (`env-plain.json`), so `no-squashfs-chunk` is distinguishable from a failed squashfs extraction
   (`D7`: `H={squashfs_v4_be}`, `P=0`).

The fixture (`SKILL-fixture.md`, ADVISORY — not the lane SKILL.md) is the exercised table. Its
`dep-missing-be` row is `[INFERENCE]` in this seat (unblob `get_dependencies()` returns both `sasquatch`
and `sasquatch-v4be`; no BE dependency envelope exists in my runs — the in-wave draft
`R39C2ReconDep.md` measured `D={sasquatch-v4be}` on stripped-PATH BE carriers, which corroborates it);
the `dep-missing-le` row is evidenced by the round-36 before-arm (`D={sasquatch}`, `H={squashfs_v4_le}`,
`P=0`).

### Cross-check against the two in-wave drafts (read-only, not authoritative)

- `R39C2TableDraft.md` flags one open ordering decision: "if one image holds both an escaping and an
  in-tree symlink … matches row 5 and never row 6". My `D1`/`D2`/`D3`/`D6` settle it: such images exist
  and are `G={unpublished-entry}`, `SR=yes`. With that draft's row 5 (`symlink removed = no`) and row 6
  (`gap kinds = none`), the mixed envelope is **`unclassified`**. The fix is the two-row escaping pair in
  point 3 above (or one `gap kinds = *` escaping row above the in-tree row).
- `R39C2ReconDep.md` measured the two `published files` traps this seat did not: an xz body failure can
  publish files beside the failed chunk (`P>0`), and a clean image whose tree is one empty directory is
  `P=0`. My fixture therefore uses `*` for those two cells and still labels 33/33 envelopes, 0
  `unclassified`; a `0`-only body cell or a `>0`-only clean cell is wrong.
- `R39C2ReconDep.md` also argues "names sasquatch" must be substring semantics; my interpreter's
  basename rule (`sasquatch` or `sasquatch-*`) is the same decision and reproduces `-be yes`
  (`D7`, `sasquatch-v4be -be -no-exit-code …`) / `-be no` (`rea-k1-avm.json`,
  `sasquatch-v4be -no-exit-code …`).

## 5. Risks for the freeze (C1 carriers, C2 held-out set)

- **R1 — symlink chains break the C1 predicate as drafted.** The R39-C1 oracle resolves a symlink
  "POSIX-style against the link's own directory inside the image root" (lexical), so a chase link
  (`z_link -> a_escape`) counts as *in-tree* and the predicate expects an `unpublished-entry` gap for it.
  `C2-chase-first`/`C4-root-chase` show unblob removes that link when it is processed before its escaping
  target (2 diagnostics, 0 gaps) — the receipt would then fail C1 on a well-formed carrier. K5/K6 must
  contain **no symlink whose target is another symlink**, or the oracle rule must follow the second hop and
  the predicate must tolerate the order-dependent gap. Full evidence: §3 table.
- **R2 — the round-37 generator cannot encode a symlink to a directory.** `os.walk` puts a dir symlink in
  `dirnames`; `build_image` records only `fnames` links, so the entry is silently dropped (D8 tree has
  `d_in -> docs`, the image has 5 inodes and `sasquatch-v4be -be -ls` lists no `d_in`). Any K5/K6 or
  held-out tree that authors a dir symlink will produce an `oracle.tsv`/`symlinks.tsv` row with no image
  entry. Keep every symlink pointing at a regular file or a nonexistent path.
- **R3 — "never published" ≠ "never mentioned".** The escaping link's path occurs in
  `diagnostics[].report.link` (absolute staging path) — and for chain images its **basename** also occurs
  as the `link_target` of a retained in-tree link (`D5`, `C1`, `C3`). A C1 counter must test
  `files`/`unpublished_entries`/`extraction_gaps`/output tree only; `D5`'s `unpublished_entries[0].link_target`
  is `a_escape`, an escaping link's name in metadata of a kept link.
- **R4 — the AVM detection is a header equality.** unblob omits `-be` iff `bytes_used == mkfs_time`
  (`squashfs.py:48-50`), so an AVM-marker image is byte-identical in body behaviour to a standard BE one
  under `-be` (probe matrix: `-be` exit 0, no flag exit 1). Held-out `avm-marker-be-dropped` carriers must
  be produced by that single patch (`mkfs_time := truncate(bytes_used)`); patching anything else makes the
  class a body failure.

## 6. Evidence inventory (all under `.ufo/waves/round-39/w1/artifacts/R39C2LabMixed/`)

| path | content |
|---|---|
| `envelopes/env-*.json` (26) | full REA CLI envelopes `{ok,data,meta}`, 2 repeats per carrier, `--full-output`; 5–14 KB each, no gzip needed |
| `carriers/*.sqsh` (12) + `plain-input.bin` | the exact dev images and the non-container input (327–441 B), `carriers.sha256` |
| `features.tsv` | one row per run: carrier sha256, `evidence_id`, `H/G/D/BE/SR/P`, gap/unpublished counts, diagnostics, label |
| `labels-all.json` | interpreter output for 33 envelopes (26 dev + K1–K4 afters + 2 AVM probe + round-36 K1 before) |
| `escape-check.txt` | machine check that escaping names occur only in diagnostic `report.link` / raw reports, never in published paths; output trees hold no symlink |
| `commands.txt` | exact commands, versions, checksums of generator/unblob/REA inputs |
| `make-dev-carriers.py` | deterministic tree authoring + `gen-squashfs.py` invocation |
| `sqfs-triage.py` | ADVISORY grammar interpreter (12 KB, implements §4 contract; not the frozen tool) |
| `SKILL-fixture.md` | ADVISORY craft-section table exercised by the interpreter |
| `collect.py` | copies envelopes/carriers and renders `features.tsv` from scratch |

## 7. Limits and inference

- The three primary carriers are synthetic (441/434 B) gzip trees built by the round-37 generator; no
  vendor image, xz body, AVM body, K5/K6 or held-out carrier was touched. `[INFERENCE]` the same
  sanitiser path applies to xz and to multi-chunk images (same `fix_extracted_directory` call site).
- Only file symlinks and dangling escaping targets were exercised as links. Directory symlinks are
  **unexercised** because the generator cannot emit them (R2); a resolvable escaping dir link is
  `[INFERENCE]` removed like a file link.
- Extraction order is a filesystem property (`iterdir`); this seat measured one XFS scratch volume. The
  order-invariance claim is only for **independent** links; for chains the finding is that the vector is
  order-determined, not which order a future volume will choose.
- `BE=yes` evidence comes from a deliberately corrupted inode table (`D7`), a dev carrier only; it is not a
  claim about real mangled vendor images.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39C2LabMixed` was removed after the bundle was copied; nothing
  outside the artifacts dir and the report was written. Two pre-TMPDIR REA staging dirs may remain under
  `/tmp/rea-firmware-*` from the first run (they were not deleted: sibling seats run REA concurrently and
  the names are not attributable). No VCS command was run; no external state changed.
