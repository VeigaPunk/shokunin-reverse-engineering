source: S090 (rea-agents 6.5.0 published tarball, `dist/rust/RustAuditableReader.js`, `dist/rust/RustBinaryImage.js`, `dist/go/GoElfImage.js`, `dist/go/GoBinaryContainer.js` and the CLI bundle; byte-identical to the installed copy); S089 (`.dep-v0` format); S091 (wheel digest of the base carrier)
verified-at: 2026-10-23, round 30 (R30-C2); 19 live `rea-agents@6.5.0` `inspect-rust-binary` calls 2026-10-23T03:00:36+00:00–2026-10-23T03:01:50+00:00 (`corpus/evidence/round-30/c2/runs.tsv`), after the freeze `4ee65c67` and the control receipts `f39f4530`; predictions frozen in `corpus/evidence/round-30/c2/predictions.tsv` at the instrument commit `0dbabf78`, before any REA run on any mutant
recheck: `python3 -I -B tools/round-30/c2-rust-refusals.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>` (rebuilds the 19 mutants deterministically from carrier `elf-x86_64-uvx`, checks each sha256 against the frozen column, re-runs REA live; target `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`, exit 0). Only one C2 run at a time: the counter rewrites the shared mutant files.

# `inspect-rust-binary` refusal signatures at REA 6.5.0: 19 of 19 code-read predictions hold live

## Claim

R30-C2 (depth): the REA 6.5.0 reader for cargo-auditable sections has a fixed order of gates, each with a literal message, and they can be predicted from the published code. 19 deterministic edits of one real carrier (uv 0.13.0 `uvx`, ELF x86_64, sha256 `2e9105ad…`) were frozen with a predicted outcome each (3 accept, 16 refuse with an exact message) before any REA run on them; all 19 hold live under predicate P2-match.

## Method

Mutants are built by `tools/round-30/c2-rust-refusals.py` (`build_mutants`): container edits patch the `.dep-v0` section header in place; content edits append a new payload at a 16-aligned end-of-file offset and point the header at it. The independent oracle (`tools/round-30/rust_dep_oracle.py`) reads the acceptances. Predicate P2 (verbatim from `.ufo/waves/round-30/claims.json`):

> A mutant matches when its live REA 6.5.0 inspect-rust-binary run agrees with its frozen prediction: for a predicted refusal, the envelope is not ok and the frozen message appears verbatim in the run's stdout or stderr; for a predicted acceptance, the run exits 0 with an ok inspect_rust_binary envelope whose subject sha256 is the mutant's sha256 and whose package multiset, file_offset and compressed_bytes equal the oracle's reading of the mutant; and its committed envelope, first added after the freeze commit, agrees with the live run on ok and evidence_id.

## Results

Observation (`corpus/evidence/round-30/c2/envelopes/<id>.json`, `runs.tsv`): `mutants=19 matches=19 target=19`.

| mutant | edit of `elf-x86_64-uvx` | predicted | observed REA error code | exit | evidence_id / match |
|---|---|---|---|---:|---|
| g-relocated | original section bytes moved to a 16-aligned offset at EOF (sh_offset/sh_size patched) | accept | ok | 0 | `ev_0b8cea2d06bf950e0c46966978abe9c4b6ce3ada468e58f4459107edbfd7128e` P2-match |
| g-recompressed | same JSON re-compressed with zlib level 9, at EOF | accept | ok | 0 | `ev_b805799ea2aa3c88979d86bbf750e315b740a6d6326e7e8cba33bcabb1448418` P2-match |
| g-no-root | `root` removed from every package, at EOF | accept | ok | 0 | `ev_7e0cbd0f191ead648bfabaa249a7113827c9dc4decd994d48474cebadc71b147` P2-match |
| r-empty | sh_size = 0 | refuse: Dependency section is not file-backed | invalid_request | 1 | P2-match |
| r-nobits | sh_type = SHT_NOBITS (8) | refuse: Dependency section is not file-backed | invalid_request | 1 | P2-match |
| r-compressed-flag | sh_flags OR SHF_COMPRESSED (0x800) | refuse: Compressed dependency sections are unsupported | unsupported_target | 1 | P2-match |
| r-two-sections | `.comment` header renamed to `.dep-v0` (two sections) | refuse: Image contains more than one dependency section | invalid_request | 1 | P2-match |
| r-not-zlib | section replaced by 9,870 patterned non-zlib bytes | refuse: Dependency section is not a complete zlib stream | invalid_request | 1 | P2-match |
| r-trailing-bytes | original stream + 4 trailing bytes | refuse: Dependency section is not a complete zlib stream | invalid_request | 1 | P2-match |
| r-over-1mib | 1,048,577-byte section | refuse: Dependency section exceeds the 1 MiB compressed limit | resource_constraint | 1 | P2-match |
| r-inflate-ratio | JSON padded with 3 MiB of spaces (14,009 compressed bytes, inflate bound 896,576) | refuse: Inflated dependency JSON exceeds the size limit | resource_constraint | 1 | P2-match |
| r-not-utf8 | zlib(`ff fe fd`) | refuse: Dependency JSON is not valid UTF-8 | invalid_request | 1 | P2-match |
| r-bad-json | zlib(`{"packages":[`) | refuse: Dependency section JSON is invalid | invalid_request | 1 | P2-match |
| r-nesting-33 | zlib(33 `[` + 33 `]`) | refuse: Dependency JSON nesting exceeds 32 levels | invalid_request | 1 | P2-match |
| r-format-negative | zlib(`{"format":-1,"packages":[]}`) | refuse: Dependency JSON does not match the format schema | invalid_request | 1 | P2-match |
| r-extra-field | package 0 gains `features: []` | refuse: Dependency package 0 does not match the package schema | invalid_request | 1 | P2-match |
| r-kind-dev | package 0 `kind` = `dev` | refuse: Dependency package 0 does not match the package schema | invalid_request | 1 | P2-match |
| r-two-roots | package 463 already root; package 0 also `root: true` | refuse: Dependency JSON declares more than one root package | invalid_request | 1 | P2-match |
| r-index-outside | package 0 gains dependency index 584 (= package count) | refuse: Dependency index 584 from package 0 is outside the package list | invalid_request | 1 | P2-match |

Observation on the envelope shape, not predicted and not scored: 13 of the 16 refusals return error code `invalid_request` with the generic message "Analysis input is invalid. Check the arguments and try again." and the specific reader message only inside `error.details.issues`; the compressed-flag refusal returns `unsupported_target`; the 1 MiB and inflate-ratio refusals return `resource_constraint` with the reader message in `error.message` and `details.reported_limits.maximum_bytes` (1,048,576 and 896,576). A caller that reads only `error.message` sees the generic text for 13 of the 16 refusal mutants (10 distinct messages). In 15 of 16 refusals the reader message is prefixed `Selected artifact <path>: `; only the compressed-flag refusal's `error.details.reason` equals the bare message, so match by substring, not equality (`.ufo/waves/round-30/w2/ReviewC2Messages.md`).

Inference: the gate order read from the code is input cap (256 MiB) and container parse, then section count, compressed flag, file-backed, then size cap, inflate (with the ratio bound and Node's trailing-junk rejection), UTF-8, nesting depth, JSON parse, format schema, graph-expansion byte budget, package records, strict top-level schema, root count and index range, then the rustc-hash cap and the 8 MiB report check (wave 2 `ReviewEntryC2.md`; the mutants exercise the listed gates from section count to index range, not the outer ones). A zero-size `.dep-v0` is refused by the container layer as "not file-backed", so the reader's own "Dependency section is empty" message is unreachable through an ELF header edit; `file_backed` requires size > 0 on ELF, PE and Mach-O and `readDependency` is the reader's only caller, so the message cannot fire in 6.5.0 at all (inference from code, `ReviewEntryC2.md`).

## Limits

- One container (ELF x86_64), one pin, one host runtime (node v24.21.0). PE and Mach-O edits, the 256 MiB input cap and the 8 MiB report budget were not exercised.
- Several mutants share a message (r-empty/r-nobits; r-not-zlib/r-trailing-bytes; r-extra-field/r-kind-dev), so a match does not prove which branch fired for those pairs (`.ufo/waves/round-30/w1/RevSelftestLookalikes.md`).
- The committed-record clause for refusals compares only the `ok` flag: a fabricated refusal record passes it (control `no-reader`, 16 of 19, `.ufo/waves/round-30/w1/CtlC2Sequence.md`); the live re-run is the authority. The `code_pointer` column is a frozen annotation the counter does not read: most pointers are a few lines off the dist files, and the `r-two-roots`, `r-index-outside` and `g-no-root` pointers are about 150 lines off and land on other branches (`RevPredRefuseA.md`, `RevPredRefuseB.md`, `ReviewEntryC2.md`); the predicted messages were traced correct independently.
- Pre-data controls (`.ufo/waves/round-30/controls/receipts.tsv`): none met the target; trivial predictors (always refuse, one generic message, help-text messages, shuffled strings) are expected to match 0 to 2 of 19 (`CriticAxisFitC2.md`).
- Runtime dependence: the trailing-bytes prediction holds because node v24.21.0 supports `rejectGarbageAfterEnd`; on a Node without it the same mutant would get "Dependency section has bytes after the zlib stream" (`ReviewEntryC2.md`, node-only probe). Refusal envelopes carry no subject digest, so their errors are bound to the mutant bytes only through the frozen sha256 column and the path (`SentinelEvidence.md`).
- `dist/go/GoBinaryContainer.js:80` (the size > 0 rule) is cited from S090's tarball but the S090 row hashes only the CLI bundle that repeats it.

- Sibling overlap (cite, not absorb; wave 2 `ConnFleetOverlap2.md`): revenger-shokunin holds six committed REA 6.4.0 `inspect_pe_resources` error records (`corpus/live/runs/round-{31,35,36,51,52}/attempt-*.json` at its HEAD `876630db`) with the same `invalid_request` error shape (generic message, `details.issues[0]`). That is earlier independent evidence of the envelope shape at another pin and operation, not evidence for any of the 19 matches here; nothing is claimed for 6.7.0.

Correction (round 31): The code pointers for r-two-roots, r-index-outside, r-inflate-ratio and r-not-zlib in corpus/evidence/round-30/c2/predictions.tsv are RustAuditableReader.js:151-153 → RustAuditableReader.js:302, RustAuditableReader.js:154-157 → RustAuditableReader.js:306, RustAuditableReader.js:128-129 → RustAuditableReader.js:139, and RustAuditableReader.js:131-134 → RustAuditableReader.js:143, respectively. The 1 MiB compressed-size and 64x inflate-ratio limits were already recorded in corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10; the new R30-C2 content is the observed refusal messages and error codes. Corrections cite `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10` (routed defects 3 and 4 of `corpus/lessons/round-30-verifier-spotcheck.md:146-147`; evidence `.ufo/waves/round-31/w1/ScribeR30Corrections.md`).
