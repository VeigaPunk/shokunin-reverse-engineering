# R40-C2 table v2 — proposed action vocabulary, per-label action tokens, cause corrections

Seat R40C2ActionReview, round 40 wave 1 (pre-freeze). Scope: the draft labels in
`plans/round-40-claims.md` (R40-C2 class list) and the v1 table (`SKILL.md:333-343`), checked
against the lane's measured evidence. Every token below is grounded in a measured run cited in the
last column; `[INFERENCE]` marks the two places where no measured run backs the action half.

## 1. Closed vocabulary (11 tokens)

Tokens are atomic strings scored together with the label (`(label, action)` pair). One row = one
token; two rows may share a token only when the correct next step is observably identical.

| token | one-line meaning |
|---|---|
| `check-superblock` | verify magic / `s_major` / `bytes_used` on the carrier before any rerun; an empty envelope is not an empty filesystem |
| `install-dependency-rerun` | put the binary named by the gap's `dependencies` on the unblob child PATH and rerun into a fresh output directory; safe to leave installed |
| `wrapper-be-then-remove` | rerun through a **temporary** PATH wrapper named `sasquatch-v4be` that appends `-be`, fresh output directory, then remove the wrapper |
| `keep-evidence-quarantine` | keep the failing command + stderr from diagnostics, compare against a known-good carrier, never patch the envelope into a success; nothing was published to verify |
| `keep-evidence-match-published` | same evidence-keeping, and the published subset is real output: match it to the oracle by relative-path suffix + sha256 |
| `expect-absent` | the reported path is absent from the output; never materialise the link or match it against the regular-file oracle |
| `count-gaps` | expected, not a failure: one `unpublished-entry` gap per kept non-file entry; publish nothing for it |
| `expect-absent-and-count-gaps` | both of the above, because the image held both link kinds |
| `match-oracle` | nothing to fix: match every published regular file to the independent oracle by suffix + sha256 (for `clean-empty` the oracle expects zero regular files) |
| `not-comparable` | wrong verb or provider: this table does not apply to the envelope; do not relabel, rerun under `extract-firmware` if a squashfs reading is wanted |
| `none` | no row matched: the table cannot derive an action from these fields and says so instead of guessing |

## 2. Per-label proposal (rows in recommended first-match order)

Signature columns are the v1 interpreter features (`tools/round-39/sqfs-triage.py:341-421`):
H handlers, G gap kinds, D dependencies, BE (`-be` token in a recorded sasquatch command), SR
(MaliciousSymlinkRemoved present), P published files. The guard row precedes every signature row.

| # | label (unique) | guard / H | G | D | BE | SR | P | action token | evidence for the action | decidable from envelope fields alone? |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | out-of-domain → label `unclassified` | `operation != extract_firmware` OR `provider.id != "unblob"` | `*` | `*` | `*` | `*` | `*` | `not-comparable` | prose guard already in SKILL `SKILL.md:1270` ("the receipt is not comparable … do not relabel"); AxisFit C2 measured a ghidra `analyze_function` envelope labelled `no-squashfs-chunk` by v1; measured `provider.id` value is exactly `unblob` (H01) | yes — the guard reads only envelope fields |
| 1 | no-squashfs-chunk | H=∅ | ∅ | ∅ | `n/a` | no | 0 | `check-superblock` | knowledge entry :50-54; measured silent drop `TT-be-trunc` (`w1/R39C2ReconMarker.md` §5.1), `full-not-squashfs` (`w1/R39C2ReconDep.md` §2) | yes |
| 2 | dep-missing-be | `squashfs_v4_be` | {missing-extractor-dependency} | {sasquatch-v4be} | `n/a` | no | `*` | `install-dependency-rerun` | v1 row 2; D names the executable the chosen Command needed (S120 `command.py:101-102`); fresh-outdir is a schema requirement (S119 `firmwareAnalysis.js:20-24`); P=`*` required by measured AppImage K3 (P=2, round-36) | yes |
| 3 | dep-missing-le | `squashfs_v4_le` | {missing-extractor-dependency} | {sasquatch} | `n/a` | no | `*` | `install-dependency-rerun` | v1 row 3 + K3 AppImage receipt (published ELF prefix + opaque range beside the same gap) | yes |
| 4 | avm-marker-be-dropped | `squashfs_v4_be` | {extractor-failure} | ∅ | no | no | 0 | `wrapper-be-then-remove` | the `-be` fix is measured directly: `carrier-avm.sqsh` and `sqimg-avm-probe.bin` — sasquatch-v4be noflag exit 1 / `-be` exit 0 (R39AssimAvmCritic matrix); the **wrapper delivery through REA is untested** [INFERENCE] (`w1/R39C2TableDraft.md:144`, D5a); **remove-after is mandatory** (D5b: a persistent wrapper re-adds `-be` exactly when unblob omits it, S121:4389-4395, so every later genuine AVM-BE run fails and is mislabeled row 5) | **conditional — see §3.1** |
| 5 | body-extractor-failure | `squashfs_v4_be` | {extractor-failure} | ∅ | yes | no | 0 | `keep-evidence-quarantine` | v1 row 5 action (kept command/stderr verbatim in `ExtractCommandFailedReport`, S120 `report.py:91-98`); measured 6/6 `-be` failures with P=0 (marker recon §1-4, corrupt recon) | yes |
| 6 | partial-body-failure | `squashfs_v4_be` | {extractor-failure} | ∅ | `*` | no | >0 | `keep-evidence-match-published` | measured `full-be1-xz`: exactly one extractor-failure gap, BE=yes, **P=6** (`w1/R39C2ReconDep.md` §2, D1); the match-published half is [INFERENCE] — no measured partial run was oracle-compared | yes |
| 7 | escaping-symlink-removed | `squashfs_v4_*` | ∅ | ∅ | `n/a` | yes | `*` | `expect-absent` | v1 row 6; measured K1 after.json (1 removal, 0 gaps); loop images produce the same vector and the same action is correct for them (D3, S118:58-63); P widened to `*` — nothing else carries SR=yes, so `>0` buys no separation (D1/D2 lesson) | yes |
| 8 | mixed-symlinks | `squashfs_v4_*` | {unpublished-entry} | ∅ | `n/a` | yes | `*` | `expect-absent-and-count-gaps` | measured committed carriers K5 (`G=[unpublished-entry] SR=yes P=10`) and K6 (`… P=8`), re-read from `corpus/evidence/round-39/c1/K{5,6}/after.json` this seat; R39-CL2 | yes — the conjunction (SR=yes ∧ G={unpublished-entry}) is visible in fields; **the token must not collapse to either half**, that collapse is exactly the routed defect |
| 9 | in-tree-symlink-metadata | `squashfs_v4_*` | {unpublished-entry} | ∅ | `n/a` | no | `*` | `count-gaps` | v1 row 7; action survives the special-entry case (D4a: `kind` enum `["symlink","special"]`, S119 `firmwareAnalysis.js:137-141`) | yes |
| 10 | clean-be | `squashfs_v4_be` | ∅ | ∅ | `n/a` | no | >0 | `match-oracle` | v1 row 8 | yes |
| 11 | clean-le | `squashfs_v4_le` | ∅ | ∅ | `n/a` | no | >0 | `match-oracle` | v1 row 8 (LE half measured H03/H04) | yes |
| 12 | clean-empty | `squashfs_v4_*` | ∅ | ∅ | `n/a` | no | 0 | `match-oracle` (oracle expects zero regular files) | measured `full-be-dirempty-gzip`: clean extraction, coverage complete, P=0 (`w1/R39C2ReconDep.md` §5.4, D2) | yes |
| — | (no row matched) → label `unclassified` | — | — | — | — | — | — | `none` | the fallback must state non-decidability, not guess | no by construction — that is the point |

Notes on cells (each is a defect-class lesson from round 39, not style):

- Row 7 keeps `P=*`, row 6 keeps `P>0` and rows 10/12 split on P: the P cell is load-bearing **only**
  between partial-body-failure and the clean/body rows; everywhere else round 39 measured that a
  pinned P excludes real outcomes (D1, D2).
- Rows 7/8: the mixed row must also be **ordered ahead of** the escaping row (or the escaping row
  must pin `G=∅` as shown) — under a v1-style `G=*` escaping cell, row order alone decides K5/K6 and
  the mixed label never fires. Belt and suspenders: pin the cell AND order the row.
- Rows 2/3 keep `SR=no` pinned (v1); the compound "second chunk removes a link + squashfs dep-miss"
  shape then hides the dependency from the label. Unreachable in the claimed single-squashfs-carrier
  family; the block prose must say so (TableReview §6).
- Row 4/5: `BE` is the only separator between them (`SKILL.md:326` prose: "only the recorded `-be`
  token separates them"); both rows pin P=0, row 6 carries P>0.

## 3. Labels whose correct action is NOT decidable from envelope fields alone

### 3.1 `avm-marker-be-dropped` — decidable only under a stated domain assumption

Envelope fields (H=`squashfs_v4_be`, G={extractor-failure}, D=∅, BE=no, P=0) mean exactly
"the marker held, so unblob omitted `-be`, and sasquatch-v4be then died". Two carrier bodies
produce that vector with **different correct actions**:

1. marker-only **standard-BE** body (the v2 draft class; `--endian avm` writer output): `-be` fixes
   it — measured (critic's sasquatch matrix, exit 1 → exit 0).
2. a **genuine AVM-layout** body that fails for an unrelated reason (e.g. damaged block): `-be` does
   not fix it (it forces the wrong reading per S121:4389-4395); the right action is damage triage.

The fields cannot separate 1 from 2. R40-C2's own "Not claimed" list excludes genuine AVM-layout
outcomes, so **within the claim** the action is decidable — but the table must carry that
assumption in the row or its prose ("assumes a standard-BE body; genuine AVM-layout outcomes are
out of scope"), not guess. The AVM critic's proposed carrier-byte disambiguator (2-byte metadata
block-length endianness at `inode_table_start`: exact on ≤4096-B fixtures, plausibility-only when
the inode table spans multiple blocks) is reachable via `subject.local_path` without REA — but a
table that reads carrier bytes is no longer envelope-fields-only, and the v2 interpreter spec would
have to say so explicitly. Either choice is fine; silence is not. Additionally (critic feed-forward):
never key the row or its cause on the stderr sentence "suggests a SquashFS image of a different
endianess" — it is printed by runs that succeed and runs that fail alike.

### 3.2 The `unclassified` fallback — action `none`, stated as undecidable

Any envelope matching no row (timeout corner: `ExtractorTimedOut` records `cmd` not `command`, so BE
reads `n/a`, S120 `report.py:125-131`; broadcom dep-miss; unknown gap kinds) must emit
`(unclassified, none)`. The v1 interpreter already labels these `unclassified`; v2 must give the
pair a `none` action rather than borrowing a look-alike row's action.

### 3.3 `partial-body-failure` in multi-chunk envelopes — the `-be` hint is lost (out of claimed family)

A marker-only BE chunk inside a container that also publishes files (AppImage before-arm shape)
would carry P>0 and land on row 6, whose token says nothing about `-be`. Single-squashfs carriers
(the claimed family) cannot produce this; the block prose must state the masking rather than let
row 6's cause imply it was considered.

## 4. Cause-cell corrections v2 must carry (each measured in round 39)

| row | required cause change | evidence |
|---|---|---|
| escaping-symlink-removed | add the symlink-loop branch: `MaliciousSymlinkRemoved` is also emitted for recursive links, which never resolve at all (action unaffected) | S118 `extractor.py:58-63` vs cited 79-91 (D3); demonstrated loop vector → rule 6 |
| in-tree-symlink-metadata | say "non-file entry (symlink or special)", not symlink-only; and absolute targets are kept by lstrip+re-root, not because they resolve inside | S119 `firmwareAnalysis.js:137-141` (D4a); S118:74-75 + `file_utils.py:34-39` (D4b) |
| avm-marker-be-dropped | keep "unblob omitted `-be` because `bytes_used == mkfs_time`"; add the standard-BE-body assumption (§3.1); no stderr-text keying; add the stale-wrapper warning (a leftover wrapper from a previous fix lands genuine AVM-BE here) | S112:48-50; D5b; critic feed-forward 2-3 |
| body-extractor-failure | restore the dev table's "or the extractor build" alternative (unsupported compressor fails under `-be` too); add the stale-wrapper false-positive note | `tools/round-39/sqfs-triage.py:130` TABLE_BLOCK (D6); D5b |
| partial-body-failure | new cause: the chunk failed after other output was published (measured `full-be1-xz`, P=6) | D1, ReconDep §2/§5.3 |
| clean-empty | new cause: the tree yields no regular file (measured: single empty directory, coverage complete) | D2, ReconDep §5.4 |
| mixed-symlinks | new cause: ≥1 link removed+reported AND ≥1 non-file entry kept; row order must not decide it silently | K5/K6 vectors (re-verified this seat); R39-CL2 |
| dep-missing-be/le | source cell must cite REA as the minter of the `missing-extractor-dependency` string (S112/S120 do not contain it) | D7, S119 `FirmwarePublication.js:165-205`, `FirmwareReports.js:333-334` |
| out-of-domain | cause = wrong verb or provider; cite the prose guard the executable table restores | `SKILL.md:1270`; AxisFit C2; R39-CL1 |

## 5. Scoring consequences (depth accounting, for the counter)

- v1 labels are not unique per decision: the round-39 manifest maps `clean-be` and `clean-le` both
  to `clean`, and `version-minor-mismatch` to `body-extractor-failure` (verified in
  `corpus/evidence/round-39/c2/heldout/manifest.json`), so 20 envelopes carried 9 distinct
  decisions (AxisFit §3b). The v2 draft's 13 unique labels + the two `unclassified` variants give
  **14 distinct row decisions** if replicates are also split on a non-decision feature per class.
- v1 scored the action column 0% (nonsense-cause mutant 20/20, AxisFit §3c; the counter compares
  `label == expected_label` only, `tools/round-39/c2-counter.py:389-390`). The v2 counter must
  compare the `(label, action)` pair, or the vocabulary above is decorative again.
- Kill-control interaction: a trailing `*` default row is inert on the claimed set (every class row
  fires first) and only observable through out-of-set probes — the "best table + `*` default row"
  control must therefore be scored with at least one out-of-set envelope, or it cannot fail.
- `not-comparable` vs `none` under the same `unclassified` label is what makes the domain guard
  observable in the scored pair; collapsing both to a bare label would re-open R39-CL1's silent
  mislabeling path at action level.

## 6. Tooling record

Nothing installed, upgraded, moved or removed. No pacman transaction. No REA or unblob run; no
carrier built or run (frozen-carrier discipline). All reads were committed lane bytes plus the
round-39 wave reports. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C2ActionReview` removed.
