# SquashFS extract-firmware outcome triage — table v3 (round-41 wave-1 DRAFT, rule block 20)

Draft for `SKILL.md` → `## Queue-drain craft` rule block 20, to be integrated by the L1 in the
round-41 freeze. Nothing here is frozen: this file is the wave-1 artifact the freeze can take,
edit or reject.

What this file is, exactly:

* the block carries `<!-- sqfs-triage-table v3 -->`, the marker the round-41 v3 interpreter
  (`sqfs-triage-v3.py`, this artifacts directory) requires;
* the twelve columns are the v2 columns, unchanged and in the same order, so a v2 row can be
  read beside its v3 replacement column by column;
* the `gap kinds` column now uses the new CONTAINS form (`kind+`, `kind1,kind2+`) wherever the
  claim's precedence text says "∈ G" — that is what labels the combined outcomes
  (partial+in-tree, partial+mixed, depth-limited+in-tree, depth-limited+mixed, depth-limited
  alone, missing-dependency+other gaps);
* the new label `depth-limited-nested` and the new action `raise-depth` are declared here for
  the first time;
* the file repeats the `## Queue-drain craft` heading so the interpreter can read the block
  directly (`--skill sqfs-triage-v3-table.md --table-only`); the L1 pastes everything from the
  numbered item through the last table row into `SKILL.md`'s existing section and drops the
  heading.

## Queue-drain craft

20. **SquashFS `extract-firmware` outcome triage, table v3.** Read the REA envelope's own
    record — operation, provider, chunk handlers, `extraction_gaps[].kind`,
    `extraction_gaps[].dependencies`, the recorded sasquatch argv, `MaliciousSymlinkRemoved`
    and the published-file count — and take the FIRST row below whose every condition cell
    holds; no row is `unclassified`/`none`, which is a refusal to label, not a failure. Every
    row is scoped to `extract_firmware` from `unblob`, so a `inspect-firmware-regions` or
    `binwalk` envelope borrows no SquashFS label (R39-CL1). Order is the whole content of the
    table: rows are not sorted by severity but by the precedence the cause column states.
    `gap kinds` cells are either an EXACT set (`none`, `a`, `a+b`) or a CONTAINS set
    (`a+`, `a,b+` — these kinds and possibly others); use the exact form where the fact is
    exclusive (an in-tree-only gap set) and the contains form where the precedence text says
    "whatever other gaps accompany it". `published files` is `0`, `>0` or `*`. No table is
    embedded in the interpreter: the block below is the only machine surface (R40-CL5 M1).

<!-- sqfs-triage-table v3 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty raise-depth -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | no chunk in the envelope carries a squashfs handler at all, so neither sasquatch flavour ran and there is no extractor argv to read: unblob's finder dropped a truncated image, a bytes_used past the end or a non-4 s_major without a report -> check the magic, s_major and bytes_used before rerunning, because an empty envelope is not an empty filesystem -> inspect-input | S112 finder v4 patterns; S120 report.py :91-98; R39-CL3 |
| dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_*` | `missing-extractor-dependency+` | `sasquatch-v4be` | `*` | `*` | `*` | `install-extractor-be` | the gap set contains missing-extractor-dependency and its dependency names sasquatch-v4be, which was absent from the unblob child PATH, so no command ran and no argv exists; further gaps may accompany it and none of them changes the install -> install the onekey-sec sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh output directory, the image is unmeasured and not unreadable -> install-extractor-be | S112 :68-69; S120 command.py :69-77,101-102; round-36 K3/before.json |
| dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_*` | `missing-extractor-dependency+` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | the gap set contains missing-extractor-dependency and its dependency names plain sasquatch, which was absent from the unblob child PATH, so no command ran; sasquatch-v4be alone does not satisfy this gap and other accompanying gaps do not change that -> install the little-endian sasquatch 4.5.1 binary on that PATH and rerun into a fresh output directory -> install-extractor-le | S112 :25,37,68-69; S120 command.py :101-102; round-36 K3/before.json |
| partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | the gap set contains extractor-failure and at least one regular file was published, so the envelope is a partial read; whatever else the set holds (unpublished-entry for kept links, depth-limited for a stopped descent, a removed escaping link) the body was only partly walked and a zero-file failure row would hide it -> keep the published files and the failing command, match files to the frozen oracle by exact relative path and sha256, and mark the run incomplete rather than clean -> salvage-partial | R39-CL3 D1 (full-be1-xz P>0); S119 firmwareAnalysis.js :137-141; round-40 c2 H21,H22 |
| avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | the gap set contains extractor-failure, nothing was published, the recorded sasquatch-v4be argv carries no standalone -be token and the handler is squashfs_v4_be: mkfs_time equals bytes_used, so unblob read the AVM marker and deliberately omitted -be and the extractor read a standard-BE body in the wrong byte order; an accompanying gap does not change the cause -> rerun through a PATH wrapper named sasquatch-v4be that appends -be (REA has no flag passthrough) and remove the wrapper afterwards -> wrap-extractor-be | S112 :44-50; S121 -DFIX_BE build; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40 |
| body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | the gap set contains extractor-failure and nothing was published, with no marker-stripped BE story beside it: the handler is not squashfs_v4_be, or the argv does carry -be, or no sasquatch argv was recorded at all, so the fault is in the image body or the extractor build rather than the endianness handshake -> keep the failing command and stderr from diagnostics, diff the carrier against a known-good arm, and never patch the envelope into a success -> preserve-failure | S120 report.py :91-98; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40; R39-CL3 D1 |
| depth-limited-nested | `extract_firmware` | `unblob` | `squashfs_v4_*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | the gap set contains depth-limited: REA recorded a path whose descent stopped at max_depth and emitted the depth-limited kind with its own continuation, with or without unpublished-entry symlink gaps beside it, so the published tree is shallow rather than wrong and no extractor failed -> rerun with a larger max_depth (REA caps it at 10) or, at the ceiling, restart the budget from one eligible published child, always into a fresh output directory; score the deeper tree and never report the shallow one as clean -> raise-depth | REA 6.5.0 cli.js :14069 (continuation text), :14073 (MAX_EXTRACTION_DEPTH = 10), :14271-14276 (kind mint); S120 report.py :91-98; round-40 c1/V1 after.json (depth-limited beside unpublished-entry); round-41 claims R41-C2 precedence 7 |
| mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | the gap set contains unpublished-entry and at least one symlink was removed with a MaliciousSymlinkRemoved report, so both link kinds live in one image: the escaped links are gone and the in-tree ones are unpublished metadata -> expect the escaped paths absent, count exactly one gap per kept in-tree link or special file, never materialise a removed link, and never read this as permission to ignore the in-tree gaps -> audit-symlinks | S118 extractor.py :50-92; S119 firmwareAnalysis.js :137-141, FirmwarePublication.js :68-75; R39-CL2; round-40 c2 H11,H12 |
| escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | no gap was recorded and at least one symlink was removed, so every removal was an escaping or looping link and the removal itself is the only record: unblob keeps a link only while it resolves inside the extraction root -> expect those paths absent, never materialise the link, and never match a symlink against the regular-file oracle, because the file count is unaffected (R40-CL5 L6: the silent removal is the point) -> expect-link-absent | S118 extractor.py :50-92 (loop branch :58-65); round-40 c2 H07,H08 |
| in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | the whole gap-kind set is exactly one unpublished-entry kind and no link was removed: every non-file entry resolved inside the extraction root, so it is kept as metadata and recorded as one unpublished-entry gap per entry while only regular files are published -> expected outcome, not a sasquatch failure: count one gap per in-tree link or special file and install nothing; an extra gap kind beside it is a different row, not this one -> count-gap | S119 firmwareAnalysis.js :137-141, FirmwarePublication.js :68-75,301-308; round-40 c2 H09,H10 |
| clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `>0` | `none` | every regular file was published, no gap kind was recorded and no symlink was removed -> nothing to install or fix; match files to the frozen oracle by exact relative path and sha256 (no suffix matching, R40-CL1) and ignore nested carves -> none | round-40 c2 H01..H04; S114 AVM layout |
| clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `0` | `confirm-empty` | the extractor completed with no gap kind and published zero regular files because the image tree holds no regular file, which is a fact about this image and not a silent failure -> confirm the frozen independent oracle tree is empty before calling it clean, and never confuse it with the no-chunk row -> confirm-empty | R39-CL3 D2 (full-be-dirempty-gzip clean P=0); round-40 c2 H05,H06 |

### Label precedence realized by row order

The draft claims state the precedence as a numbered list over operation `OP`, provider `PR`,
handler set `H`, gap-kind set `G`, dependency set `D`, `-be` in a recorded child argv `BE`,
symlink removed `SR` and published regular files `P`. This table is a first-match reading of that
list, and the mapping is one-to-one:

| precedence step (claims text) | row that realizes it | why the row is the step |
| --- | --- | --- |
| 1. `OP ≠ extract_firmware` or `PR ≠ unblob` → unclassified | none (every row is domain-scoped) | no row can match, so the default `unclassified`/`none` is the step |
| 2. no `squashfs_v4_*` handler in `H` → no-squashfs-chunk | 1 | handler cell `none`; the row is first and domain-scoped |
| 3. `missing-extractor-dependency` ∈ `G` → dep-missing-be / dep-missing-le | 2, 3 | contains form on `G`, exact dependency name decides which |
| 4. `extractor-failure` ∈ `G` and `P > 0` → partial-body-failure | 4 | contains form on `G`, `published files` `>0`, `symlink removed *` (removed links may accompany it) |
| 5. `extractor-failure` ∈ `G`, `P = 0`, `BE = no`, handler `squashfs_v4_be` → avm-marker-be-dropped | 5 | contains form plus the three narrowing cells; sits above row 6 |
| 6. `extractor-failure` ∈ `G`, `P = 0` → body-extractor-failure | 6 | the same contains form without row 5's narrowing |
| 7. `depth-limited` ∈ `G` → depth-limited-nested | 7 | contains form, `symlink removed *` (symlink gaps may accompany it), above rows 8-12 |
| 8. `SR = yes` and `unpublished-entry` ∈ `G` → mixed-symlinks | 8 | contains form plus `symlink removed yes` |
| 9. `SR = yes` and `G = ∅` → escaping-symlink-removed | 9 | exact `none` |
| 10. `G = {unpublished-entry}` → in-tree-symlink-metadata | 10 | exact singleton, `symlink removed no` |
| 11. `G = ∅`, `P > 0` → clean | 11 | exact `none`, `>0` |
| 12. anything else → unclassified, none | none | no row matches; the default pair is the step |

Two feature tuples are NOT expressible by this grammar and are recorded rather than papered
over. Both are outside the held-out envelope domain (the generator never emits a non-v4
squashfs handler and never puts two dependency names on one gap), and both are measured in
`precedence-check.tsv`:

1. `H` holds a squashfs handler that is not `squashfs_v4_*` (e.g. `squashfs_v3`). Precedence
   step 2 labels it `no-squashfs-chunk`; row 1's handler cell `none` means "no squashfs handler
   at all", and no cell can say "no handler matching a pattern", so the table returns
   `unclassified`. A second row carrying the same label is refused (duplicate labels are exit
   2), so one row per label is the binding constraint here.
2. The missing-extractor-dependency gap names BOTH `sasquatch` and `sasquatch-v4be`. Precedence
   step 3 checks `sasquatch-v4be` first, so it labels `dep-missing-be`; the `dependencies` cell
   keeps the v2 exact-set form (the round-41 seat brief extends CONTAINS to `gap kinds` only),
   so no row matches and the table returns `unclassified`. If the freeze wants agreement on
   this tuple, the cheapest repair is to extend the CONTAINS form to `dependencies` as well
   (`sasquatch+`), not to widen a row to `*`.

### Prose repairs riding this block (unscored, reviewed)

* R40-CL5 M1 — **done**: no table copy lives in the interpreter any more. The v2
  `TABLE_BLOCK` and `--print-table` are deleted; the selftest builds its tables inline and the
  only table surface is a document read through `--skill`. A selftest case greps this module's
  own source for the header row and for `TABLE_BLOCK` so the copy cannot come back.
* R40-CL5 M2 — body failure vs marker-stripped AVM: rows 5 and 6 are split by the three
  narrowing cells (`BE`, `handler`, `P`), and row 6's cause names all three escapes (other
  handler, `-be` present, no sasquatch argv recorded) so a marker-stripped AVM can never be
  reported as a body failure without one of them being false.
* R40-CL5 M3 — avm row damage branch: row 5 says an accompanying gap does not change the
  cause, and row 4 catches the case where the failure did publish files, so damage that only
  partly read the body leaves the avm row.
* R40-CL5 L3 — REA mints the dependency gap kind: rows 2 and 3 are the only rows that read
  `dependencies`, and both state that no argv exists for that gap.
* R40-CL5 L6 — an empty-target symlink removal is silent: row 9 says the removal itself is the
  only record and the file count is unaffected.
* R40-CL4 — the partial recipe stays pinned by the zeroed block's compressed length
  (round-40 c2 H21,H22), cited in row 4's source.
* New in v3: `depth-limited` is its own row and its own action (`raise-depth`) instead of
  falling into `unclassified`; the row states that the shallow tree must never be scored as
  clean, which is the same trap row 4 closes for partial bodies.
