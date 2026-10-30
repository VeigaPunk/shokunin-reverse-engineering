# Draft — SKILL.md rule block 27 (round 52, R52-C2)

Paste-ready text of the new numbered item for `## Queue-drain craft` in
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md`. It follows block 26
(`SKILL.md:548-584` as observed at the claims-draft base `ab0eafe`), keeps block 26's
numbering convention (`- **27. ...**`), its table style (the 13-column triage table,
one `<!-- sqfs-triage-table vN -->` marker, one `<!-- sqfs-triage-actions: ... -->`
comment) and its prose shape. Block 26 stays in the file as history.

The block text starts after the marker line `<<<BLOCK27>>>` and ends before
`<<<END BLOCK27>>>`.

---

<<<BLOCK27>>>

- **27. SquashFS `extract_firmware` outcome triage v6 — the failed-body executability rule (round 52).** Table v6 supersedes rule block 26 (table v5) for the routing of a FAILED body and for the action column of the row that routes it; block 26 stays as history, and from 2026-10-30 every decision this block makes, block 26 defers to it. One defect is repaired: **a prescribed action the corpus cannot execute is a depth defect** — the rule as written cannot be followed. Block 26's `legacy-body-failure` row keeps `squashfs_v3_ddwrt` in its `failing handler` comma-list (the reader-backed v1-v3 families), so the DD-WRT FAILED body `dmg_Z3_v3ddwrt_inode_table` (the round-42 dmg carve `Z3_v3ddwrt_inode_table.bin`; REA handler `squashfs_v3_ddwrt`; one `extractor-failure` gap; zero published files) is routed `legacy-body-failure` / `cross-read-legacy` — **a cross-read prescribed on a body whose readers refuse**: the DD-WRT family has no validated independent reader on any body the corpus hands to that handler (the census below). Measured at the claims-draft base `ab0eafe`, the frozen v5 instrument labels that envelope `legacy-body-failure` in both its table column and its independent evaluator column over the 126-envelope held-out corpus (receipt in the wave-1 draft `.ufo/waves/round-52/w1/ScribeBlock27/`). Table v6 therefore (i) removes `squashfs_v3_ddwrt` from the `legacy-body-failure` `failing handler` cell, which becomes `squashfs_v1,squashfs_v2,squashfs_v3`, and (ii) adds one row, `legacy-body-unreadable` (`failing handler` `squashfs_v3_ddwrt`, gap kinds `extractor-failure+`, published files `0`), whose action is `preserve-unresolved`: **no cross-read** — the failure is preserved unresolved, nothing is installed and nothing is changed, because reader absence forbids both the damaged-body verdict and the broken-extractor verdict. **Exactly one label changes** in the frozen 126-envelope corpus: `dmg_Z3_v3ddwrt_inode_table` moves from `legacy-body-failure`/`cross-read-legacy` to `legacy-body-unreadable`/`preserve-unresolved`. Every other envelope keeps its block-26 label and action, including the seven clean envelopes whose REA handler is `squashfs_v3_ddwrt` and, in particular, the two clean DD-WRT no-pad `_ddefault` envelopes this rule names. The action vocabulary is unchanged (the same 17 tokens as block 26); v6 adds one label and one row, and it adds no reader.

  **The reader census this rule depends on** (frozen; the partition is FAMILY-level, the measurement is FIXTURE-level; **no new reader is claimed validated** by this block, and a clean extraction is not independent-reader success):

  | family (REA handler) | no-reader | partial (7-Zip only) | readable by both | of | corpus bodies handled by that handler | census rows |
  | --- | --- | --- | --- | --- | --- | --- |
  | `squashfs_v3` | 0 | 0 | 8 | 8 | 1 (`squashfs_v3_le_ddefault`, 2 published files) | census `:13-20,:47` |
  | `squashfs_v3_broadcom` | 0 | 7 | 1 | 8 | 0 | census `:21-28,:48` |
  | `squashfs_v3_ddwrt` | 6 | 0 | 1 | 7 | 15 (7 `clean`, 6 `depth-limited`, 1 `dep-missing-le`, 1 FAILED) | census `:29-35,:49` |
  | `squashfs_v3_nonstandard` | 8 | 0 | 0 | 8 | 0 | census `:36-43,:50` |

  The census is the round-50 re-measurement of 2026-10-29 on the committed round-42 fixture bytes (`unsquashfs` 4.7.5 `-lls`, 7-Zip 26.04 `l -tSquashFS`; receipt `.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`, tracked in the lane tree); the family-level statement it grounds is the round-49 entry's `## What stays Frontier, and why` (`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:100-108`, whose ddwrt bullet at `:104` records that both readers refuse the DD-WRT no-pad fixture). The census file labels the DD-WRT family's one readable fixture (`squashfs_v3_le.bin`, sha256 prefix `0161351caec8`) as readable by both, but in the corpus those bytes are handled by REA as `squashfs_v3`, not as `squashfs_v3_ddwrt` (`squashfs_v3_le_ddefault`, 2 published files, `clean`); **no corpus body handled as `squashfs_v3_ddwrt` is readable by an independent reader**, which is the fact the new row rests on. Two limits are stated rather than hidden: (a) the census is fixture-level and the scored features expose no body-variant discriminator (block 26's disclosed limit, `tools/round-50-c3/sqfs-triage-v5.py:148-178`), so the new row is keyed on the handler family and errs toward preservation — a DD-WRT body that a reader could read would still be preserved unresolved, never given a damage verdict, and no cross-read is prescribed that the census cannot satisfy; (b) the FAILED body `Z3_v3ddwrt_inode_table.bin` (sha256 prefix `839c17a83b70`) is a dmg carve that the census never offered to a reader, so its unreadability is a family-level inference from the six DD-WRT fixtures the census measured, not a body-level measurement of those bytes; the audit's lookup key (family verdict plus this stated limit) is frozen with the instrument, not left to the reader of this block. "No-pad" above is descriptive prose for the body variant, not an upstream flag spelling: S251's writer option is `-nopad`, it identifies neither the producer of a shipped image nor a reader, and no routing decision here rests on it (`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:50-60`; S251 at `corpus/SOURCES.md:164`).

  **Scope correction to block 26's "`symlink` and `special` both count" phrasing (the device kinds).** Block 26's `mixed-symlinks` and `in-tree-symlink-metadata` rows count "one gap per kept link or special file" and "one gap per entry", carrying block 21's phrase "`symlink` and `special` both count" (`firmwareAnalysis.js:139`). Read that phrase with the extraction law's own scope, which block 26's round-51 correction (`SKILL.md:574-584`) already began: **a device-node kind carries no disposition at all.** Under the round-52 device-accounting law (R52-C1) the frozen rule admits **no** gap kind for a char-device, FIFO, socket or block-device oracle row — `allowed` for a device kind is the empty list and `required['char-device'] = false` — because the extraction producer materialises regular files and directories, re-creates symlinks, creates no device node and emits no gap record for one: a device row has no published path and no gap, and a gap that lands on a device row is a **violation** of the law (the rule fails closed), never a tolerated state. So "special" in the two rows above counts only the non-regular entries the extractor actually materialises inside the extraction tree; a device node is not one of them, and an absent char-device cannot be presumed to have an `unpublished-entry` gap. This is the law's scope and not a second convention: the device rows are enumerated from the committed round-50 non-regular tables (`tools/round-50/oracle/*.nonregular.tsv`), the law is stated in `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md:N-M PLACEHOLDER` (lands with the round-52 freeze), and its derivation and source ground are `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:14-29` and `:31-49` with S250 (`corpus/SOURCES.md:163`) and S251 (`:164`). The measured corpus exercises only char-device rows (one on each Cable-class carrier, thirteen on each FRITZ!Box-class carrier); the FIFO/socket/block extension rests on the source ground and no measured carrier exercises it. The correction changes no triage label: the triage table counts the gaps REA emitted, and no device row carries one.

  <!-- sqfs-triage-table v6 -->
  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be cross-read-legacy isolate-residue preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty record-unverified preserve-unresolved -->
  | label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | container-depth-limited | extract_firmware | unblob | none | * | depth-limited+ | * | * | * | * | raise-depth | no SquashFS handler was named and REA stopped at max_depth -> rerun with a higher max_depth or descend into the published container | SKILL.md table v4 row 1; S119 FirmwarePublication.js:23-29,:294-299 |
  | no-squashfs-chunk | extract_firmware | unblob | none | * | * | * | * | * | * | inspect-input | neither a chunk nor a gap names a SquashFS handler -> check the magic and superblock before rerunning | SKILL.md table v4 row 2; S112 :102,:159,:200,:245,:319,:364,:410,:463,:522 |
  | dep-missing-be | extract_firmware | unblob | squashfs_* | * | missing-extractor-dependency+ | sasquatch-v4be+ | * | * | * | install-extractor-be | the chunk resolved its extractor to sasquatch-v4be and that binary was not found -> install the sasquatch-v4be binary and rerun into a fresh output directory | SKILL.md table v4 row 3; S112 :40-41; S120 command.py:69-77 |
  | dep-missing-le | extract_firmware | unblob | squashfs_* | * | missing-extractor-dependency+ | sasquatch+ | * | * | * | install-extractor-le | the chunk resolved its extractor to plain sasquatch and that binary was not found -> install the little-endian sasquatch binary and rerun | SKILL.md table v4 row 4; S112 :37,:39-54; S120 report.py:118-122 |
  | partial-body-failure | extract_firmware | unblob | squashfs_* | * | extractor-failure+ | * | * | * | >0 | salvage-partial | the extractor failed after publishing at least one regular file -> keep the published files and the failing command, mark the run incomplete, never score the set as clean | SKILL.md table v4 row 5; S119 FirmwarePublication.js:288-293 |
  | avm-marker-be-dropped | extract_firmware | unblob | squashfs_* | squashfs_v4_be | extractor-failure+ | * | no | * | 0 | wrap-extractor-be | the failing chunk is the v4 BE one and unblob dropped -be -> rerun through a PATH executable named sasquatch-v4be that appends -be | SKILL.md table v4 row 6; S112 :44-50; S121 -DFIX_BE build |
  | legacy-body-failure | extract_firmware | unblob | squashfs_* | squashfs_v1,squashfs_v2,squashfs_v3 | extractor-failure+ | * | * | * | 0 | cross-read-legacy | the failing chunk is a reader-backed v1-v3 body that published zero files -> cross-read the same chunk with unsquashfs and 7-Zip, and only a reader that lists the tree while sasquatch failed shows a broken extractor build | SKILL.md table v4 row 7 narrowed by R50-C3: the v4 cell squashfs_v[123]* also matched squashfs_v2_nonstandard, squashfs_v3_broadcom and squashfs_v3_nonstandard, which have no independent reader (round-49 W2Skill.md F1); round-50 plans/round-50-attempt2-claims.md R50-C3; R52-C2 removes squashfs_v3_ddwrt from this cell (the ddwrt FAILED body has no validated independent reader) -> block 27 row legacy-body-unreadable |
  | legacy-body-unreadable | extract_firmware | unblob | squashfs_* | squashfs_v3_ddwrt | extractor-failure+ | * | * | * | 0 | preserve-unresolved | the failing chunk is a DD-WRT body whose family has no validated independent reader (census below: 6 of 7 DD-WRT fixtures NO-READER, and no corpus body handled as squashfs_v3_ddwrt is readable by a reader) and it published zero files -> keep the failure unresolved and prescribe no cross-read: install nothing, change nothing, and never read a reader refusal on this family as evidence of a damaged body | R52-C2; round-49 W2Skill.md F1; corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:100-108; reader census .ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt:29-35,:49; round-52 plans/round-52-claims.md R52-C2 |
  | no-reader-failure | extract_firmware | unblob | squashfs_* | squashfs_v2_nonstandard,squashfs_v3_broadcom,squashfs_v3_nonstandard | extractor-failure+ | * | * | * | 0 | preserve-unresolved | the failing chunk is a family with no independent second reader and published zero files -> keep the failure unresolved: reader absence forbids both the damaged-body verdict and the broken-extractor verdict, so install nothing and change nothing | R50-C3; round-49 W2Skill.md F1; round-50 plans/round-50-attempt2-claims.md R50-C3 |
  | body-extractor-failure | extract_firmware | unblob | squashfs_* | * | extractor-failure+ | * | * | * | 0 | preserve-failure | the extractor ran and published zero regular files on a body the rows above did not claim -> run the layout pre-check, keep the failing command, stdout and stderr | SKILL.md table v4 row 8; S120 report.py:91-98; S124 :35 |
  | unknown-residue | extract_firmware | unblob | squashfs_* | * | unknown-chunk-handler+ | * | * | * | * | isolate-residue | bytes beside the filesystem belong to no parser -> keep the residue out of the oracle and re-carve the SquashFS chunk to unblob chunk end | SKILL.md table v4 row 9; S119 FirmwarePublication.js:286; S118 :116-127 |
  | depth-limited | extract_firmware | unblob | squashfs_* | * | depth-limited+ | * | * | * | * | raise-depth | REA stopped at max_depth and recorded one depth-limited gap per path -> rerun with a higher max_depth into a fresh output directory | SKILL.md table v4 row 10; S119 FirmwarePublication.js:23-29,:294-299 |
  | mixed-symlinks | extract_firmware | unblob | squashfs_* | * | unpublished-entry+ | * | * | yes | * | audit-symlinks | both link kinds are present in one image -> expect the escaped paths absent and count one gap per kept link or special file (block 27 scopes "special" to the non-regular entries the extractor materialises in the tree: a device-node kind carries no disposition) | SKILL.md table v4 row 11; S118 :50-92; S122 |
  | escaping-symlink-removed | extract_firmware | unblob | squashfs_* | * | none | * | * | yes | * | expect-link-absent | a link escaped the extraction root or looped and unblob removed it with a MaliciousSymlinkRemoved report -> expect the path to be absent | SKILL.md table v4 row 12; S118 :42-47,:58-65,:79-87; S122 |
  | in-tree-symlink-metadata | extract_firmware | unblob | squashfs_* | * | unpublished-entry | * | * | * | * | count-gap | the gap set is exactly one kind and every non-file entry stayed inside the extraction root -> expected, not a sasquatch failure: count one gap per entry (block 27 scopes "special" to the non-regular entries the extractor materialises in the tree: a device-node kind carries no disposition) | SKILL.md table v4 row 13; S119 FirmwarePublication.js:301-307 |
  | clean-unverified | extract_firmware | unblob | squashfs_v2_nonstandard,squashfs_v3_broadcom,squashfs_v3_nonstandard | * | none | * | * | no | >0 | record-unverified | the run completed with no gap and published regular files, but the family has no independent second reader, so no oracle can corroborate the set -> record the envelope as unverified, never as clean | R50-C3; round-49 W2Skill.md F2 (the v4 clean row gave a no-reader run the oracle-backed action none); round-50 plans/round-50-attempt2-claims.md R50-C3 |
  | clean | extract_firmware | unblob | squashfs_* | * | none | * | * | no | >0 | none | every regular file was published and the gap set is empty on a reader-backed family -> nothing to install or fix; match files to the oracle by exact relative path and sha256 | SKILL.md table v4 row 14; S119 FirmwarePublication.js:301-307 |
  | clean-empty | extract_firmware | unblob | squashfs_* | * | none | * | * | no | 0 | confirm-empty | the extractor completed with no gap and published zero regular files -> confirm the independent oracle tree is empty before calling it clean | SKILL.md table v4 row 15; S119 FirmwarePublication.js:301-307 |

  **The executability audit (what this table is scored against).** A prescribed action the corpus cannot execute is a defect, so the v6 instrument checks, for every FAILED-body envelope of the frozen corpus, the action this table prescribes against the reader census above: a FAILED-body envelope whose prescribed action is a cross-read (`cross-read-legacy`) while its family's census records no independent reader is an **executability violation**, named with the envelope id and the action. The count must be `0`; the before-arm named by the claim is `1`, naming `dmg_Z3_v3ddwrt_inode_table`. `preserve-unresolved` is the compliant answer on such a body, never a damage verdict and never an installation. The audit is rule-scoped: it compares the table's action column with the census and never re-derives a label, and a table that routes the DD-WRT FAILED body to `cross-read-legacy` is red by this clause alone even if every label matched. The census clause is embedded in the instrument so the audit cannot lose it: the census rows above, the table rows above and the audit's lookup key are one frozen set, and a census table that no longer matches the committed receipt is a red, not a silently narrowed audit.

  **Status — draft, unscored (pre-freeze).** The before-arm was measured: the frozen v5 instrument (`tools/round-50-c3/sqfs-triage-v5.py`, sha256 `f29eb92073dfff0cae48658985a7df3a34b1558430183dacc9968c2dff71b16e`) run at the claims-draft base `ab0eafedc41402b43b41a4362084119578dfe7ce` over the frozen 126-envelope corpus (`.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`, the same held-out dir R50-C3 scored) exits **0** with `pair_mismatches 0`, `verdict met`, and labels `dmg_Z3_v3ddwrt_inode_table` `legacy-body-failure` in both the table column and the independent evaluator column (command, exit code, stdout sha256 and UTC time in the wave-1 draft's receipt). The after-arm is **not** claimed here: the v6 instrument does not exist at the time of this draft, so its selftest, its controls (do-nothing, junk table, audit-guard-deleted, swapped-new-row-action, census-guard-deleted), its freeze-drift gate and its executability count are the landing's to measure, and no receipt for them is asserted by this block. Pointers that depend on the landing are marked PLACEHOLDER and must be re-derived at the freeze revision: `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md:N-M PLACEHOLDER` (the device-accounting law entry), `tools/round-52/sqfs-triage-v6.py` (the v6 instrument), the SOURCES row for S252 (`corpus/SOURCES.md:N PLACEHOLDER`; the man7 `mknod(2)` CAP_MKNOD ground opened this round), and block 26's own line span (`SKILL.md:548-584` as observed at `ab0eafe`; the freeze inserts this block after block 26, so 548 is expected to hold — re-derive it).

<<<END BLOCK27>>>

---

## Draft notes (not part of the block text — for the L1)

### 1. What was measured here (honest capture)

| what | command | exit | stdout sha256 (first 16) | UTC |
| --- | --- | --- | --- | --- |
| v5 before-arm over the 126-envelope corpus | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev ab0eafedc41402b43b41a4362084119578dfe7ce --freeze c525de54a53eb3c4fee28ede2721da4527cf8ece --envelopes <LANE>/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out $S/v5-base.json` | 0 | `bca7e0baf0600a7e` | 2026-10-30T10:48:00Z |

Result: `n_envelopes 126`, `pair_mismatch_count 0`, `verdict met`, `instrument_sha256
f29eb92073dfff0cae48658985a7df3a34b1558430183dacc9968c2dff71b16e`,
`skill_source git:ab0eafe...:SKILL.md`, `freeze.ancestor true`,
`freeze.instrument_unchanged true`, `freeze.other_tools_round50_changed []`.
The JSON receipt is copied into this seat directory as `v5-base.json`
(sha256 `e14a2d1c3c908077655d1eb981a2033e2a55c01156be42a0e5380996c845a531`);
the stdout is `v5-base.stdout`.

This is the only execution behind the draft. **The v6 instrument does not exist at the
time of this draft, so the v6 audit's `executability_violations 0` after-arm is NOT
measured here** — the block says so in its Status paragraph rather than claiming it.
No REA run, no network fetch, no vendor bytes.

### 2. Label facts behind the draft (from the measured v5 receipt + the corpus)

- `dmg_Z3_v3ddwrt_inode_table` → label `legacy-body-failure` (table and evaluator),
  subject `Z3_v3ddwrt_inode_table.bin` sha256 prefix `839c17a83b70`, chunk handler
  `squashfs_v3_ddwrt`, gaps `['extractor-failure']`, 0 published files. → the one pair
  v6 moves.
- Envelopes whose REA handler is `squashfs_v3_ddwrt` (15 of 126): 7 `clean`,
  6 `depth-limited`, 1 `dep-missing-le`, 1 `legacy-body-failure`. The two clean DD-WRT
  no-pad `_ddefault` envelopes the claim names are
  `squashfs_v3_ddwrt_squashfs_v3.be.nopad_ddefault` (subject `squashfs_v3.be.nopad.bin`,
  sha256 prefix `daa8e72d355d`, 4 published files, no gaps) and
  `squashfs_v3_ddwrt_squashfs_v3.le.nopad_ddefault` (subject `squashfs_v3.le.nopad.bin`,
  sha256 prefix `e7482db480f9`, 4 published files, no gaps).
- The census's one readable-by-both DD-WRT fixture (`squashfs_v3_le.bin`,
  `0161351caec8`) is handled by REA as `squashfs_v3` in the corpus
  (`squashfs_v3_le_ddefault`, 2 published files) — so no corpus body handled as
  `squashfs_v3_ddwrt` has an independent reader. This is the fact the new row rests
  on, and it is stronger than the claim's phrasing (see §3).
- Census rows: `.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt` is
  **tracked** in the lane tree (`git ls-files` confirms), so the citation resolves at
  the landing. Family verdict lines are `:47-50`; the DD-WRT rows are `:29-35`.

### 3. Conflicts with the claims file (verbatim, for the amendment record)

1. `plans/round-52-claims.md` (R52-C2) says: *"The two clean ddwrt no-pad `_ddefault`
   envelopes keep `clean` (their readers succeeded; no route change)."* The census
   records the opposite for those two bodies: `reader-census.txt:31` and `:34` —
   `squashfs_v3.be.nopad.bin daa8e72d355d 1 2 NO-READER (both refuse)` and
   `squashfs_v3.le.nopad.bin e7482db480f9 1 2 NO-READER (both refuse)`. What succeeded
   is the **extraction** (sasquatch published 4 files, no gap), not a reader; the
   round-51 entry says it plainly: "A clean extraction is not independent-reader
   success" (`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:57-58`). The
   **route is unchanged either way** (label `clean`, action `none`), so the claim's
   decision stands and only its stated reason is wrong — the draft block states it
   correctly. Recommend the claims text be amended in the freeze's amendment record.
2. `plans/round-52-claims.md` (R52-C2) says: *"the ddwrt family has no validated second
   reader; 6/7 no-reader"*. Read literally this contradicts the same census row 35
   (`squashfs_v3_le.bin 0161351caec8 0 0 readable-by-both`). The defensible statement
   — the one the draft uses — is the stronger and exact one: **every corpus body that
   REA handles as `squashfs_v3_ddwrt` is over a census fixture with NO-READER**
   (6 of 6); the family's one readable fixture is handled by REA as `squashfs_v3`.
   Recommend the claims text be amended to that wording.
3. `plans/round-52-claims.md` (R52-C2) says the audit checks *"every FAILED-body
   envelope's prescribed action against the family's reader census"*. The census has
   **no row for the FAILED body's own bytes** (`Z3_v3ddwrt_inode_table.bin`,
   `839c17a83b70`) — it is a dmg carve, not a round-42 fixture. The audit's lookup is
   therefore a family-level inference with a stated body-variant limit, not a
   body-level measurement. The draft states that limit in the block; the L1 should
   freeze the lookup key (family verdict + disclosed limit) in the instrument so the
   audit cannot be widened or narrowed silently.
4. `plans/round-52-claims.md` (R52-C1) says block 27 "supersedes or scopes SKILL.md's
   *"`symlink` and `special` both count"* phrasing (rule block 26 rows)". The verbatim
   phrase "`symlink` and `special` both count" is in the **block 21 (table v4)** rows
   (`SKILL.md:540` the `mixed-symlinks` row and `SKILL.md:542` the
   `in-tree-symlink-metadata` row, both with `firmwareAnalysis.js:139`); block 26's
   rows (`SKILL.md:565` and `:567`) carry the terser "count one gap per kept link or
   special file" / "count one gap per entry". The draft scopes **both** rows of block 26 (the
   ones the claim names) and names block 21 as the carrier of the phrase, so the
   correction lands on the text the claim points at without contradicting it.
5. Not a conflict but a precision note: the claim calls the body "the ddwrt FAILED
   **no-pad** body". S251's upstream writer option is `-nopad` (not `-no-pad`), and it
   identifies neither the producer of a shipped image nor a reader
   (`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:50-60`). The draft keeps
   "no-pad" as descriptive prose and says so, so no routing rests on the spelling.

### 4. Open decisions the L1 owns (the draft does not pre-empt them)

- **Row placement / grammar.** The draft places `legacy-body-unreadable` immediately
  after `legacy-body-failure` (as its superseded sibling) and removes `squashfs_v3_ddwrt`
  from the legacy cell. The v6 evaluator must reproduce this precedence with the same
  first-match-wins order as the v5 precedence list (`tools/round-50-c3/sqfs-triage-v5.py:123-146`).
  Alternative the L1 may prefer: keep the legacy cell and put the new row **above** it.
  Both change exactly one label on this corpus; the mutation battery must decide.
- **Where the census lives for the audit.** The draft puts the census table **in the
  block** (marked by the `census rows` column) so the rule and the audit read one
  frozen set. The alternative is a frozen JSON beside the instrument. The draft chose
  the in-block table; the L1 may rewrite it, but then the block's census column and the
  instrument's lookup must still agree, and the census-guard-deleted mutant must go red.
- **The clean-body residue.** The v6 audit as scoped (FAILED bodies only) does **not**
  cover the seven clean `squashfs_v3_ddwrt` envelopes, whose `clean`/`none` action
  ("match files to the oracle") still prescribes an oracle match that the census says
  no reader can supply for those bodies — the same defect class v5's F2 fixed for the
  three wholly no-reader families. The claims freeze that residue out of v6. The draft
  block discloses it as an open underclaim (the clean ddwrt bodies keep `clean`; no
  reader is claimed for them) rather than leaving it silent; whether to widen the
  audit to clean bodies is the L1's call and would change more than one pair.
- **Placeholders to resolve at the freeze:** `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md:N-M`,
  `corpus/SOURCES.md:N` for S252, and the re-derivation of `SKILL.md:548-584` after
  block 27 is inserted.

### 5. Pointers used, and how they resolve

| pointer | resolves at the landing? |
| --- | --- |
| `SKILL.md:548-584` (block 26) | yes — observed at `ab0eafe`; `git diff ab0eafe..HEAD` shows SKILL.md unchanged since, and the freeze inserts block 27 **after** block 26 |
| `SKILL.md:574-584` (block 26's round-51 correction) | yes — same argument |
| `tools/round-50-c3/sqfs-triage-v5.py:123-146` (precedence), `:148-178` (reader boundary) | yes — committed file |
| `.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt:13-20,:21-28,:29-35,:36-43,:47-50` | yes — tracked in the lane tree |
| `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:100-108` (reader census entry; ddwrt bullet `:104`) | yes — committed |
| `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:14-29` (device kinds), `:31-49` (carriers), `:50-60` (padding) | yes — committed |
| `corpus/SOURCES.md:163` (S250), `:164` (S251) | yes — committed |
| `tools/round-50/oracle/*.nonregular.tsv` (device rows) | yes — committed |
| `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md:N-M PLACEHOLDER` | lands with the freeze |
| `tools/round-52/sqfs-triage-v6.py` | lands with the freeze |
| `corpus/SOURCES.md:N PLACEHOLDER` (S252) | lands with the freeze |

### 6. Table parity check (mechanical, against the committed v5 rows)

The draft's v6 table was diffed cell-by-cell against the committed block-26 table
(`SKILL.md:552-570`): **17 of 17 v5 rows are present, 18 rows in v6, and every row is
byte-identical to v5 except three intentional cells** —

- `legacy-body-failure` col 5 (`failing handler`): `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt`
  → `squashfs_v1,squashfs_v2,squashfs_v3`;
- `legacy-body-failure` col 13 (`source`): the v5 source cell plus the v6 supersession note;
- `mixed-symlinks` col 12 (`cause`) and `in-tree-symlink-metadata` col 12 (`cause`): the v5
  cause plus the in-block scope parenthetical.

All 13 columns of all 18 rows are present and every row has 13 cells; the action
vocabulary comment is byte-identical to block 26's (17 tokens, unchanged — the new row
reuses the existing `preserve-unresolved` token and adds only a label).

### 7. Boundary

No REA run, no network fetch, no vendor bytes, no lane-tree write outside this seat
directory, no git mutation. Read-only git only (`log`, `show`, `diff`, `ls-files`,
`merge-base --is-ancestor`). Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeBlock27`
holds `v5-base.json` and `v5-base.stdout`; both are copied into this seat directory
before the scratch is removed.
