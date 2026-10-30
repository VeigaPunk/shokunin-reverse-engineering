# c1-run.sh R52 port-fidelity checklist

Axes: port fidelity; provenance/guard integrity; independent-oracle integrity; truthful receipts. Static review only, not an admission or runtime pass.

All `H:N` citations mean `tools/round-50/c1-run.sh:N`; all `C:N` citations mean `plans/round-52-claims.md:N`, relative to the lane root. Source identity is captured in `inspection.json`. The requested comparison is baseline harness versus declared R52 contract, not a review of an unprovided R52 harness draft.

## MUST preserve

- [ ] **Pins:** `rea-agents@6.5.0`, unblob `26.6.4`, sasquatch `4.5.1`, unsquashfs `4.7.5` (H:83-86); binary path/hash/version capture H:239-249; oracle enforcement H:308-314; after-arm enforcement H:676-707. REA version probe and package-root discovery are not substitutes for the pinned extraction argv. Claims source/producer ground C:40-53 and independent reader C:94-97.
- [ ] **Child identity:** exact `FIXED_PATH` H:90-92; nonempty `C1_CHILD_PATH` override and boolean H:146-150; export before binary resolution; after receipt `child_path`/`child_path_override` H:839; oracle child path H:648. Preserve the same resolution policy in counter replay; merely retaining version strings does not ensure identical executable selection.
- [ ] **Arguments and inputs:** after/oracle mode vocabulary H:122-140; ID grammar, required readable regular carrier, optional lowercase SHA256 pin H:142-154,229-233; canonical paths H:154-163; unknown arguments reject. Preserve argv arrays rather than shell re-parsing.
- [ ] **Data-run guard:** `after` requires `--data-run` or `KAIDOKU_C1_DATA_RUN=1`; oracle requires it for evidence-root output H:125,165-173. Update the evidence segment before evaluating it. Scope matches post-freeze L1-only procedure C:154-161; `--data-run` is an operator assertion, not proof of a freeze.
- [ ] **Occupied-slot guard:** after.json/oracle.tsv blocks without explicit `--force`, H:196-199. Capture previous after digest H:709-710,850. Do not silently overwrite fresh evidence.
- [ ] **Scratch segment and canonical prefix:** normalized base, complete `/kaidoku-r52/` segment, after-arm canonical prefix refusal H:175-194; foreign-scratch waiver explicitly false provenance H:182-186. Actual receipt output path additionally checked for canonical prefix and `..` H:783-784. Claims provenance base C:163-166.
- [ ] **Scratch lifecycle:** private `c1-run.XXXXXX`, trap, writable cleanup, TMPDIR H:287-296; extractor root must not preexist H:712. Retry deletes only that extraction root H:735. Preserve explicit `--keep-scratch` H:291-294; never delete a caller's base.
- [ ] **provider_timeout retry:** at most `${C1_REA_ATTEMPTS:-3}` attempts; retry only parsed `.error.code == provider_timeout`; remove extraction tree before next attempt; record count and aggregate start/end/duration H:722-740,834. No broad retry-on-any-error substitution. **Do not conflate this harness behavior with the new counter projection ENOENT policy in C:105-114.**
- [ ] **Superblock precondition:** `hsqs`, offset zero, LE v4.0, xz compression ID 4, `mkfs_time == bytes_used`, and bytes_used no greater than carrier size H:252-286; NONAVM waiver recorded, not silently admitted. Oracle reader inspect must independently agree on LE/xz/marker H:363-368. Claims measured domain C:29,54-58.
- [ ] **Frozen extraction parameters:** npx pinned argv, JSON/full output, max depth 1 H:712-720; default 536870912 bytes/100000 files H:205-207; external timeout 900 seconds H:205,730; cwd private scratch, exported REA_UNBLOB_COMMAND H:690-697,730. Counter replays receipt parameters (H:714-716); preserve these unless the freeze expressly changes the contract.
- [ ] **After-envelope and publication gates:** require process exit zero, envelope `ok=true`, object `.data`; persist compact `.data` as after.json only then H:742-798. Raw envelope optional H:799. `receipt_written=false` exits 3 H:854-856; subject/carrier mismatch exits 3 H:864-866. Handler/failed-chunk observations are recorded negatives, not harness success criteria H:858-863; counter decides the claim.
- [ ] **Three-producer independent oracle:** frozen reader auto and le, byte-identical regular and nonregular TSVs H:300-306,316-362; unsquashfs 4.7.5 extraction plus `-lln` H:431-443; sasquatch `-le` cross-check H:445-455. Do not replace `le` with the reader's big-endian AVM layout. Claims explicitly retain independent oracle arms C:158-160 and census rederivation C:94-97.
- [ ] **Oracle grammar:** exact three tab fields H:378-388; nonempty regular table, nonempty nonabsolute path, lowercase 64-hex hash, decimal size, bytewise sorted unique paths H:391-405; closed dir/symlink/char-device/block-device/fifo/socket vocabulary; nonempty symlink target; device major:minor; empty dir/fifo/socket detail H:406-420; sorted unique nonregular paths and no regular/nonregular overlap H:421-424. Preserve actual checks, not an inaccurately stronger description (no `..` component rejection exists here).
- [ ] **Oracle comparison:** lstat/no link-following walk, byte hashing and sizes H:480-525; compare regular path union in both directions H:563-578; compare dir/symlink both trees H:580-590; compare special rows in both directions against numeric listing H:539-558,591-597; reject unexpected special tree entries and TSV-unsafe paths H:598-610. Preserve all_equal, mismatch count and first 20 examples.
- [ ] **Oracle completion:** write four TSVs and oracle-run.json H:615-667; require both extractor exits zero and all_equal true H:669-672. Do not treat table creation alone as successful oracle measurement.

## MUST preserve receipt contracts

- [ ] **After run.json, H:803-852:** schema/mode/claim/id; carrier path/hash/size/superblock/waiver; outdir; exact argv + display argv_shell; cwd/extraction_root; segment/prefix flags; UTC timestamps/duration/attempt count/exit; REA pin/version/package root; unblob original env/resolved command/hash/version; sasquatch path/hash/version/version_line/precondition waiver; child PATH/override; envelope parseable/ok/hash/bytes/error; data_extracted/receipt_written; receipt and envelope summary; subject/prefix/LE-handler/no-failed-chunk observations; previous receipt digest; stderr head.
- [ ] **After data summary, H:756-781,793-797:** receipt SHA/bytes and evidence_id/operation/provider/engine identity; coverage; handler list; chunks and extraction_failed; regular count/published bytes; gap count and first-20 details; unpublished counts/kinds/head; extraction parameters; selection and subject hashes; output directories. This bounded summary is not the full gap census; after.json retains the full data object.
- [ ] **Successful oracle-run.json, H:621-667:** identity/carrier+superblock waiver/outdir/layout/offset; scratch and child path; reader path/hash/auto+le argv/equality/timing/exit/stderr; both extractors' paths/hashes/version/argv/timing/exit/log heads; table counts/kind census; four output filenames/digests/byte counts; crosscheck and reader inspect.
- [ ] **Reader-auto failure receipt, H:333-350:** schema/mode/claim/id/carrier/outdir/provenance, reader identity+argv, UTC/duration/exit/stderr/error. Preserve the separate failure construction; global replacement must cover it too. Other early failures do not all emit this receipt.

## MUST change for the R52 port

| Change | Baseline locations | Required R52 value / claims anchor |
|---|---|---|
| Header identity | H:2 | R52-C1 / round 52; preserve genuine round-41/49 provenance references |
| Scratch segment | H:59-65,87,104-105,175 | `kaidoku-r52`; C:156,166 |
| Canonical scratch prefix | H:62,88 | `/fast/scratch/hyaku/kaidoku-r52/`; C:156,166 |
| Evidence guard and default | H:68,89,102,162 | `/corpus/evidence/round-52/`, default `<lane>/corpus/evidence/round-52/c1/ID`; C:90,159-160 |
| Schema, all receipt constructors | H:334,622,804 | `kaidoku-r52-c1-run-v1` (seat's port contract; claims do not spell this schema) |
| Claim, all receipt constructors | H:334,622,804 | `R52-C1`; C:27,71-75; rule grammar C:151-153 applies to counter/rule rather than independently specifying harness schema |
| Diagnostics | H:184,186 | R52-C1 provenance warning/refusal, not R50-C1 |

Keep shared reader `tools/round-41/sqfs-list.py` H:201-203 unless deliberately re-frozen: `round-41` is not a stale round-50 evidence constant. Likewise keep version numbers, inherited source/probe comments and named historical controls unless an amendment changes them.

## Harness behavior not explicitly specified in R52-C1 prose

The R52-C1 section names a port (C:71-75) and data procedure (C:154-161), but does **not** enumerate most harness invariants above. The seat contract makes them explicit preservation obligations. These additional knobs deserve explicit freeze/receipt policy, not accidental disappearance:

| Knob / behavior | Evidence | Consequence to retain or explicitly disposition |
|---|---|---|
| `C1_KEEP_ENVELOPE=1` | H:28,113,799 | Keeps raw envelope as after.envelope.json; optional, not evidence admission by itself |
| `C1_ALLOW_NONAVM=1` | H:56-57,274-282,366 | Waives superblock and inspect-domain check, recorded in successful receipts; control-only prose |
| `C1_REA_ATTEMPTS` | H:733-734 | Overrides default 3 provider-timeout attempts; absent from usage env list H:111-116 and R52 claim text; do not describe harness as unconditionally capped at 3 |
| `C1_ALLOW_FOREIGN_SCRATCH=1` | H:182-193 | Allows foreign segment/prefix, records negative segment; never makes canonical provenance true |
| `C1_ALLOW_PIN_DRIFT=1` | H:237,311-314,685-707 | Permits mismatched tool versions; actual identity recorded but no dedicated pin-drift waiver field |
| `C1_ALLOW_NO_SASQUATCH=1` | H:115-116,677-688,837-838 | After-only missing-binary control waiver; does not waive oracle dependency |
| `C1_READER`, `C1_UNSQUASHFS` | H:201-204,300-314 | Alternate executable/source locations, actual paths/hashes recorded |
| `C1_MAX_OUTPUT_BYTES`, `C1_MAX_OUTPUT_FILES` | H:206-207,717-718 | Defaults maxima; empty variable omits its flag and restores REA default rather than frozen maximum |
| `REA_UNBLOB_COMMAND` | H:690-697 | Executable override; resolves and pins concrete command before export |
| `HYAKU_SCRATCH` / `--scratch` | H:175-194 | Noncanonical base can pass segment but after prefix still refuses without explicit waiver |
| `KAIDOKU_C1_DATA_RUN` | H:125,168-173 | Environment substitute for flag; not freeze verification |
| `--force`, `--keep-scratch`, `--dry-run`, `--pin` | H:129-137,196-225,229-233,291-295 | Force replacement / scratch retention / early no-write plan / optional asserted hash |
| `npm_config_cache` | H:701-705 | Alters searched package-root discovery path, not REA pin |
| Exit convention | H:75-77,94-95,854-868 | Harness uses 3 for tool/disagreement, unlike claim scorer's 1 not-met and 2 unavailable; do not silently recode on port |

## Findings, residual risks and verification gaps

1. **Medium — declaration does not explicitly freeze harness preservation details.** C:71-75 names c1-run.sh, C:154-161 names its invocation; neither enumerates the pins, PATH/waiver behavior, guards, oracle grammar or receipt schema. Integrate this checklist or equivalent review into the freeze; an unreviewed mechanical port could weaken provenance while still matching the prose.
2. **Medium — retry claims must distinguish harness from counter.** C:105-114 promises counter projection retry on provider_timeout and extraction-tree ENOENT. H:733-737 retries only provider_timeout; H:733 allows arbitrary C1_REA_ATTEMPTS and H:834 records only aggregate count, not earlier failing diagnostics. This is not proof the new counter is defective: it is a concrete boundary to preserve and audit, not a request to broaden harness retries implicitly.
3. **Low — F8 visibility is counter-specific, absent from harness summary.** C:59-62,97-98 requires input_path and continuation_id for depth-limited gaps in the v2 counter receipt. H:772's bounded gap summary does not include either. Full after.json remains available (H:755,791); do not use the summary alone to satisfy depth_gap_recorded. An explicit harness summary enhancement would need review rather than being described as already present.

No R52 harness draft was assigned or executed; no assertion about its correctness is made. No REA, downloads, controls, oracle binaries or data-run executed. Runtime fidelity, post-freeze freshness, projection retry semantics and counter binding checks remain for the integration owner. No canonical-runtime/rerouting/resume implementation is changed or evaluated by this static port checklist.

LSP unavailable: `read xd://lsp` returned `No such tool`; no status/references/definition/diagnostics device exists in this environment. Citations are literal source inspection, not semantic-reference proof.
