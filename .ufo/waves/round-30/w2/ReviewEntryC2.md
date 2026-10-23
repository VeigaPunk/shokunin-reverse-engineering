# R30-C2 entry review — ReviewEntryC2 (wave 2, falsify)

Seat: `KaidokuR30.ReviewEntryC2`. Access date 2026-10-23. Work window 2026-10-23T03:11Z–03:17Z.
Attacked: `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` (sha256 `b7020ea1abc9b574fe1fd9af89bae3dc79a72790d6d7e517c1af7af42811e013`, lane HEAD `3502b94c`, unchanged since `24da3459`). The attack covered its numbers, error codes, the gate-order inference, the inference that the "empty" message is unreachable, and its limits. Evidence came from `corpus/evidence/round-30/c2/` and from REA 6.5.0 `dist/rust`, `dist/go` and `dist/cli-runtime/cli.js` under `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`.

**Verdict: the table holds.** All 19 rows agree with the predictions, the envelopes, `runs.tsv` and a rebuild of the mutants from scratch bytes. The messages, codes, exits, evidence_ids and every quoted number reproduce. **The prose has 5 low-severity defects and 2 informational notes** (listed below). The most important defect is that the gate-order inference leaves out a reachable gate. None of the defects changes the P2 score.

## Claim-by-claim table

| # | Entry claim | Check (command / source) | Result | Verdict |
|---|---|---|---|---|
| 1 | Base carrier is uv 0.13.0 `uvx`, ELF x86_64, sha256 `2e9105ad…` | `sha256sum base.bin` (scratch copy) | `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d`, 332008 bytes; equals the `carriers.tsv` row `elf-x86_64-uvx` | holds (observation) |
| 2 | 19 mutants: 3 predicted accept, 16 predicted refuse | `predictions.tsv` | 3 `ok` + 16 `refuse` | holds (observation) |
| 3 | Mutants are deterministic and frozen before data | `check.py` imports the lane `build_mutants` in memory and compares with `predictions.tsv` | all 19 `rebuilt==frozen:True` (sha256, size, kind and message); the shared mutant files are also equal to frozen (`live_file==frozen:True`, read only); `predictions.tsv` was added once at `0dbabf78` (2026-10-22T23:34:24-03:00 = 02:34:24Z) and never modified | holds (observation); "before any REA run on any mutant" was not independently checkable (unknown) |
| 4 | 19 live calls 03:00:36–03:01:50 UTC, after freeze `4ee65c67` and receipts `f39f4530` | `runs.tsv`; `git show -s --format=%cI` | first start `2026-10-23T03:00:36+00:00`, last end `03:01:50+00:00`; freeze 02:35:13Z; `f39f4530` 02:59:22Z; data commit `24da3459` 03:04:20Z; envelopes first added at `24da3459` | holds (observation) |
| 5 | Table column `exit`: 0 for the 3 accepts, 1 for the 16 refusals | `runs.tsv` col 4 | g-* 0, r-* 1 | holds |
| 6 | Table column "observed REA error code" (13 `invalid_request`, 1 `unsupported_target`, 2 `resource_constraint`) | `cat envelopes/r-*.json` | identical per row (for example `r-compressed-flag` `"code":"unsupported_target"`; `r-over-1mib` and `r-inflate-ratio` `"code":"resource_constraint"`) | holds |
| 7 | Predicted messages appear in the envelopes | same | each `r-*` envelope carries its frozen message verbatim (in `details.issues[0].message` or `error.message`) | holds |
| 8 | Three accept evidence_ids | `check.out` | `ev_0b8cea2d…7128e`, `ev_b805799e…48418`, `ev_7e0cbd0f…1b147` equal the envelopes; subject sha256 equals frozen; `file_offset` 332016 and `compressed_bytes` 9870/9797/9786 equal the patched header; `g-no-root` `root_package_index None` | holds |
| 9 | r-not-zlib "9,870 patterned bytes" | `check.out` | original `.dep-v0` at 319695, size 9870; mutant section size 9870 | holds |
| 10 | r-over-1mib "1,048,577-byte section" | `check.out` | `sec_size=1048577` | holds |
| 11 | r-inflate-ratio "14,009 compressed bytes, inflate bound 896,576" | `check.out` | `padded len 3201452 compressed 14009 bound min(8MiB,64x) 896576`; envelope `reported_limits.maximum_bytes: 896576` | holds |
| 12 | r-two-roots "package 463 already root; package 0 also root" | `check.out` | `packages 584 roots [463]`; the builder sets `other=0` | holds |
| 13 | r-index-outside "584 (= package count)" | `check.out` | `packages 584`; envelope message "Dependency index 584 from package 0 …" | holds |
| 14 | r-trailing-bytes "original stream + 4 trailing bytes" | `check.out` | `sec_size=9874` (9870 + 4) | holds |
| 15 | g-recompressed "same JSON re-compressed with zlib level 9" | `check.out` | `compact re-serialization == original inflated bytes: True 55724` | holds (the bytes are identical, not only the document) |
| 16 | Method: "container edits patch the `.dep-v0` section header in place" | `c2-rust-refusals.py:140-143` | `r-two-sections` patches the **`.comment`** header's `sh_name` | holds except one row (D-info-1) |
| 17 | P2 quoted verbatim from `claims.json` | Python string equality | `P2 verbatim: True` | holds |
| 18 | `mutants=19 matches=19 target=19` | `.ufo/waves/round-30/after/c2-rust-refusals-at-92b1dd2d.txt:21` | `mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)` (the receipt was not rerun by this seat; only ReRunC2 may run it) | holds (recorded receipt) |
| 19 | Envelope shape: "13 of the 16 refusals return `invalid_request` + generic message, reader text only in `details.issues`" | envelopes | 13 mutant envelopes have `"message":"Analysis input is invalid. Check the arguments and try again."` | holds |
| 20 | "1 MiB and inflate-ratio refusals return `resource_constraint` with reader message in `error.message` and `maximum_bytes` 1,048,576 / 896,576" | envelopes | exact | holds |
| 21 | "A caller that reads only `error.message` sees the generic text for **13 of 16 refusal kinds**" | envelopes plus a count of distinct messages | 13 of 16 refusal **mutants**; there are only 13 distinct refusal **kinds** (messages), and 10 of those are generic-only | **fails as worded** (D2) |
| 22 | Inference: gate order "container first (section count, compressed flag, file-backed), then size cap, inflate (…), UTF-8, nesting depth, JSON parse, format schema, package records, root count and index range" | `RustAuditableReader.js:50-61,146-171,299-308`; `RustBinaryImage.js:10-11,42-56`; bundle `cli.js:5214,5244,5307-5308,5453-5460` | The listed relative order is correct. It **omits reachable gates**: `admitGraphExpansion` (between format schema and package records, `:165`, message "Dependency graph exceeds the complete report byte budget before expansion", resource `transport`); the strict top-level `documentSchema` (between package records and root count, `:168-170`, "Dependency JSON does not match the package schema"); and the gates that come before the section-count check (the 256 MiB `readStableArtifact` cap and ELF/PE/Mach-O parse refusals in `readGoBinaryContainer`). After the index range come the rustc-hash cap (`RustBinaryImage.js:94-98`) and the 8 MiB report check (`RustBinaryProvider.js`) | **partially fails** (D1) |
| 23 | Inference: "the reader's own 'Dependency section is empty' message is unreachable through an ELF header edit" | `GoBinaryContainer.js:69-81`, `GoElfImage.js:184-186`, `RustBinaryImage.js:52-56`; `rg` call sites | `file_backed` is only true when `size > 0n` and the span is in-bounds; NOBITS forces false; `readDependency` is the only caller of `readAuditableSection` (dist and the single `readAuditableSection(` occurrence at bundle `cli.js:5460`), so `bytes.length == size > 0` | **holds**. It is also true in a stronger form: no input reaches the message on any container. PE (`GoPeImage.js:117`) and Mach-O (`GoMachoImage.js:145-148`) use the same `declaredFileRange`, and Mach-O applies a stricter AND. This is an inference from code; PE and Mach-O were not run (D-info-2) |
| 24 | Inference: inflate step "with the ratio bound and Node's trailing-junk rejection" | `node junk.mjs` (v24.21.0, no REA) | with `rejectGarbageAfterEnd`: `threw code ERR_TRAILING_JUNK_AFTER_STREAM_END`; without it: `raw+00010203 without option inflated 55724`; patterned junk: `Z_DATA_ERROR incorrect header check` | holds on v24.21.0. On a Node that lacks the option, the code path `:85-87` emits a **different** message, "Dependency section has bytes after the zlib stream", which the entry does not name (D4) |
| 25 | Limits: "one container, one pin, one host runtime; PE and Mach-O edits, the 256 MiB input cap and the 8 MiB report budget were not exercised" | code read | true. The list also leaves unexercised: the 8 MiB absolute inflate cap (only the 64× ratio governed), the strict top-level schema gate, the rustc-hash cap and the container-parse refusals | holds but incomplete (part of D1) |
| 26 | Limits: shared-message pairs do not prove which branch fired | code read | each pair throws from one site (`RustBinaryImage.js:53`; `RustAuditableReader.js:143`; `:236`) | holds |
| 27 | Limits: committed-record clause for refusals checks only `ok`; control `no-reader` 16 of 19 | `controls/receipts-detail.tsv:10`; `w1/CtlC2Sequence.md:26` | `no-reader … predictions copied as observations … matches=16` | holds |
| 28 | Limits: "`code_pointer` column cites line numbers **a few lines off**; branches are correct" | `sed -n '151,159p;301,308p' RustAuditableReader.js` | `r-two-roots` cites 151-153, which lands on the UTF-8 catch/throw (the real throw is at 301-302). `r-index-outside` cites 154-157, which lands on `assertDepth`/`JSON.parse` (real 303-306). `g-no-root` cites 159, the JSON.parse catch (real 308). These are about 150 lines off and point at other branches; only the symbol text (`rootIndex`, `roots[0] ?? null`) is right | **fails as worded** (D3) |
| 29 | Limits: no pre-data control met the target; trivial predictors match 0–2 of 19 | `controls/receipts.tsv`; `w1/CriticAxisFitC2.md:21-26` | 10 rows `met_target=no`; named predictors give 0/19, 0/19 (2/19 best single signature), 0/19, ≈0.72/19 expected | holds |
| 30 | Source line: S090 covers `RustAuditableReader.js`, `RustBinaryImage.js`, `GoElfImage.js`, `GoBinaryContainer.js` and the CLI bundle | `sed -n 96p corpus/SOURCES.md`; `sha256sum` of installed files | S090 records sha256 for `RustAuditableReader.js` `1f3748c9…`, `RustBinaryImage.js` `08adaa59…`, `GoElfImage.js` `ee88b9cd…` and `cli.js` `168cd322…`, all equal to the installed files. **`GoBinaryContainer.js` (installed `2db56f92…`) has no hash or line range in S090** | **partially fails** (D5) |
| 31 | Claim sentence: "a fixed order of gates, each with a literal message" | `RustAuditableReader.js:236,306` | two of the 13 refusal messages are template strings (`Dependency package ${index} …`, `Dependency index ${outside} from package ${index} …`) | wording nit (folded into D-info-1) |

## Defects (all low; none changes the P2 count)

- **D1 — the gate-order inference is incomplete (low-medium).** Entry line 46 lists the order without two reachable reader gates. The first is `admitGraphExpansion` (`RustAuditableReader.js:165`, resource_constraint/`transport`, "Dependency graph exceeds the complete report byte budget before expansion"). It runs after the format schema and **before** the package-record check, so an array of about 105k `{}` packages refuses on budget, not with "package 0 does not match". The second is the strict top-level `documentSchema` (`:168-170`, "Dependency JSON does not match the package schema", no index), which runs between package records and root count. The phrase "container first (section count, …)" also skips the container-parse refusals and the 256 MiB input cap, which come before the section count. The gates after the index range (rustc-hash cap, 8 MiB complete report) are missing too. Fix: name these gates, or say "among the gates exercised here". Inference from code; not run.
- **D2 — "13 of 16 refusal kinds" mixes units.** It should read 13 of 16 refusal mutants, which is 10 of the 13 distinct refusal messages (the r-empty/r-nobits, r-not-zlib/r-trailing-bytes and r-extra-field/r-kind-dev pairs share messages). Observation from the envelopes.
- **D3 — "a few lines off" understates the code_pointer drift.** Three pointers are about 150 lines off and land on other branches (claim 28). The cited `RevPredRefuseB.md:153-155` itself lists 151-153 vs 302, 154-157 vs 306 and 159 vs 308. Fix: say "most are 2–10 lines off; three rootIndex pointers cite the wrong region (~150 lines)".
- **D4 — the runtime-dependent alternate message is not named.** The r-trailing-bytes prediction depends on `rejectsTrailingJunk()` being true. Where it is false, REA 6.5.0 emits "Dependency section has bytes after the zlib stream" (`:85-87`). The Limits section says only "one host runtime (node v24.21.0)". Observed on v24.21.0 by `node junk.mjs`; the other runtimes are inference.
- **D5 — the S090 provenance has a gap for `GoBinaryContainer.js`.** The entry's source line names it, and both the r-empty prediction and the "empty unreachable" inference rest on its line 80 (`file_backed: size > 0n`), but the S090 row records no sha256 or line range for it (installed sha256 `2db56f9285c349dff9c9ac807a2e2bd1ddc468acd18f17f2e22456b3e52788b2`). The bundle repeats the line (`cli.js:4006`), and `cli.js` is hashed in S090, so the inference is still sourced. Only the per-file citation is missing.
- **D-info-1 (informational).** The Method sentence says container edits patch the `.dep-v0` header, but r-two-sections patches `.comment`'s `sh_name`. The Claim says "each with a literal message", but two messages are templates.
- **D-info-2 (informational).** The "empty unreachable" inference is scoped to "an ELF header edit" and says the container layer refuses. The stronger statement also holds: the message is dead for every input of `inspect-rust-binary` 6.5.0 on ELF, PE and Mach-O. The throw itself is in `RustBinaryImage.dependencySection`, which uses the container's `file_backed` verdict.

## Residual risk and verification gaps

- The live data tests only a few precedences: the zero-size refusal comes before the empty check (r-empty), the size cap before inflate (r-over-1mib: patterned bytes also have an invalid zlib header), UTF-8 before JSON parse (r-not-utf8), nesting before the format schema (r-nesting-33: an array also fails `z.object`), and package records before the strict schema (r-extra-field and r-kind-dev). The other adjacent orderings (count/compressed/file-backed, inflate/UTF-8, parse/format, format/package, package/root, root/index) come from reading the code; no mutant violates two of them (inference).
- This seat ran no REA, so it did not re-observe the live run; it relies on the committed envelopes and the `after/` receipt. Live agreement belongs to ReRunC2.
- PE and Mach-O `file_backed` paths were read in `dist/go`, not in the bundle (inference).
- Whether an REA run on any mutant happened before the `0dbabf78` freeze could not be checked (unknown).

## Commands (all exit 0, run from scratch, lane read-only)

| UTC | Command | Key output |
|---|---|---|
| 03:12:09Z | `date; date -u` | host TZ -03; envelope mtimes 00:00–00:01 local equal 03:00–03:01Z |
| 03:14:47Z | `timeout 300 python3 -I -B check.py` | see claims 1, 3, 8–15 |
| 03:14:52Z | `timeout 120 node junk.mjs 319695 9870` | `node v24.21.0`; `ERR_TRAILING_JUNK_AFTER_STREAM_END`; `without option inflated 55724`; `Z_DATA_ERROR incorrect header check` |
| ~03:15Z | `rg` / `sed` over `dist/rust`, `dist/go`, `dist/cli-runtime/cli.js` | `readAuditableSection(` occurs once in `cli.js` (line 5460, `readDependency`); `file_backed: size > 0n` at `cli.js:4006` |
| ~03:16Z | `sha256sum` of dist files vs `SOURCES.md:96` | 4 of 4 recorded hashes equal; `GoBinaryContainer.js` absent from the row |
| ~03:16Z | `git show -s`, `git log --diff-filter=A` (read-only) | commit times as in claim 4 |

## Sources (local reads, access date 2026-10-23)

| Source | sha256 | Located quote (line) |
|---|---|---|
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js | `1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505` | L165-167: `admitGraphExpansion(value); // One malformed package must fail before Zod retains an issue for every field. rejectMalformedPackages(value);` |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustBinaryImage.js | `08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681` | L52-53: `if (!section.file_backed) throw new RustAuditableFormatFailure("malformed", "Dependency section is not file-backed");` |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/go/GoBinaryContainer.js | `2db56f9285c349dff9c9ac807a2e2bd1ddc468acd18f17f2e22456b3e52788b2` | L80: `file_backed: size > 0n,` |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/go/GoElfImage.js | `ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204` | L186: `const range = type === SHT_NOBITS ? { ...declared, file_backed: false } : declared;` |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js | `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204` | L5214: `if (bytes.length === 0) throw new RustAuditableFormatFailure("malformed", "Dependency section is empty");` |

## Scratch artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewEntryC2/`)

| File | sha256 |
|---|---|
| check.py | `8ae72cd091f24e64dee0c93f5ecb2b61170d292d3b03c8c67ee20d037c4fbdd2` |
| check.out | `4d119ea4fbe625f7fdbe99d745ae4d7279229d8a6a6b98a63022a8df07dc33d9` |
| junk.mjs | `a52e8a16201f05570ec3360535d1d4d1d9ae17b290f7150fabd83d454d7dd207` |
| junk.out | `6c8e5d27c4a6ea298ccaef0e279f85d947cb085e2449f2b36d2b3db16937e76b` |
| base.bin (copy of carrier `elf-x86_64-uvx`) | `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d` |

Tool installs or updates: none. No REA run, no C2 counter run, no write to carriers or the mutant directory, no git or jj writes, no agents spawned, no process left running.
