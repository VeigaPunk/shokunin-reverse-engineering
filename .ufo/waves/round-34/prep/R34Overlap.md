# R34Overlap — domain/axis fit for the proposed GNU ELF symbol-version requirements depth claim

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base: `ec3125ad3d130d92f888a4128dfaa2982f36fff7`. Reporting model: `opencode-go/beam-free` (no tool error visible). Held item `U064N008Hf47eb933` is not inspected, retried, or cited as findings.

## 1. Axes named

Owned axes (kaidoku): `coverage`, `depth`, `calibration` (all currently saturated at `10.0`, none retired). Fleet axes touched only as evidence: `freshness`, `operability`, `adjacency`. The proposed claim is a **depth** claim: a decision table with real thresholds, named error signatures, and cited sources. It must improve or leave unchanged every other axis. It is not a coverage claim: no new REA surface, no new host artifact class, and no PROVINCE Core row should be added merely because the table was measured.

Stagnation basis: all three owned proxies are tied at `10.0`, none retired, and the stagnation nudge is active. Under that nudge, a frontier/capability move is permitted, but a bounded depth table on already-owned ELF static metadata is still an admissible lowest-axis move because depth remains one of the tied lowest axes. No retired axis is revived.

## 2. Domain fit

Fits kaidoku's province: native ELF is an owned surface (`PROVINCE.md` Core: native ELF via Ghidra, host fallback readers including `readelf`, `objdump`, `llvm-readobj`), and the lane's stated discipline is evidence-first static analysis that keeps observation, inference, and unknown separate. The proposed work is static metadata interpretation only. It does not execute binaries, construct exploits, create synthetic carriers, or make safety/trust/license verdicts.

Stagnation basis (corrected): all three owned proxies are tied at `10.0`, none retired; depth is therefore a tied-lowest non-retired axis. The earlier wording in this report asserted that "the stagnation nudge is active"; that assertion is corrected here: Main does not rely on that waiver, and no no-new-capability-in-window measurement is established by this prep report. The lowest-axis basis is solely the tied owned scores, none retired. No retired axis is revived.

## 3. Recent rejection patterns this claim must avoid

- `R32-C2`: a lexical/semantic counter credited explicit denial and word bags (`4/4`). Any depth claim here must be structural and parser-derived, not prose agreement.
- `R33` metadata-only CHPE classification: structurally plausible forged tags were accepted as metadata. Structural plausibility is not loader authenticity.
- `R27` renamed-copy identity: filename/extension/path-sensitive shortcuts must be tested and must fail.
- `M33-4`: denial and word-bag controls must precede production data.
- `M33-5`: metadata alone cannot establish valid instructions, ABI semantics, loader acceptance, or authenticity.
- `M33-6`: safety-held builder outputs remain excluded; this claim must not reuse or reconstruct them.
- Held item `U064N008Hf47eb933` stays untouched.

## 4. Claim restated in bounded form

A depth claim only: a source-grounded decision table for GNU ELF symbol-version requirements (`.gnu.version_r` / `SHT_GNU_VERNEED`, with `DT_VERNEED` / `DT_VERNEEDNUM` and `.gnu.version` linkage context) plus an independent static reader, measured on 12 already-existing public host ELF binaries. It is **not** a claim that kaidoku gained a new REA operation, a new binary class, or runtime resolution behavior.

The 12 carriers are existing host binaries only. No critical-path binary fixture authoring, no synthetic ELF, no mutation of host binaries, and no execution.

## 5. Exact bounded predicate and control design

### Carrier set
- 12 public existing host ELF binaries, pinned before data by absolute path, size, SHA-256, ELF class, machine, and (if available) package identity.
- Prefer diversity of dependency/version profiles (e.g. `jq`, `readelf`, `ls`, `bash`, `python3`, `objdump`, `gcc`, `g++`, `ld`, `as`, `ar`, `nm` or an equivalent pinned set), but the set is fixed before measurement; no post-hoc substitution.
- All carriers must be read-only inputs. The predicate is over these 12 only.

### Parsed object (normalized table)
For each carrier, parse `SHT_GNU_VERNEED` according to the host `elf.h` structures (`Elf64_Verneed`, `Elf64_Vernaux`) and cross-check `DT_VERNEED`, `DT_VERNEEDNUM`, `.dynstr`, and section offsets. Normalize at least:
- dependency file name (`vn_file` resolved through `.dynstr`);
- `vn_version == VER_NEED_CURRENT`;
- `vn_cnt`;
- each aux entry: `vna_hash`, decoded `vna_flags` (`VER_FLG_BASE`, `VER_FLG_WEAK`, otherwise unknown bits), `vna_name` resolved through `.dynstr`, and `vna_other`;
- linked-list termination (`vn_next == 0`, `vna_next == 0`) and count consistency (`vn_cnt == number of aux entries`);
- section/file offsets and byte ranges used by the parser.

The independent reader must be a lane-owned minimal parser, not a wrapper around `readelf`. `readelf -V` (or `eu-readelf`) may be used only as an independent oracle after its output is frozen, and must not be the implementation under test.

### Success target
- `carriers == 12`, `matches == 12`, `target == 12`, with exact normalized-table equality between the two independent readers.
- `mismatches == 0`, `unparsed == 0`, `oracle_disagreements == 0`.
- Error/refusal cases for malformed inputs are counted separately and must match a frozen decision table.

### Controls that must fail before production data
1. **Do-nothing control**: parser returns an empty table for every carrier; must score `0/12` or otherwise fail the target.
2. **All-false control**: every normalized row/field is false; must score `0/12`.
3. **No-reader control**: output is produced without reading carrier bytes; must score `0/12`.
4. **Junk control**: corrupt or truncated ELF inputs must be refused with a named error signature; no partial table may be accepted.
5. **Filename/id-keyed shortcut control**: matching by path, file name, or evidence ID must score `0/12` or fail; the predicate must require byte-derived fields and offsets.
6. **Expected-copy forged-record control**: a copied expected JSON record without parser-derived byte offsets, hashes, and section ranges must be rejected. Expected values are not evidence unless regenerated by the parser from the pinned bytes.

### Additional structural controls
- A denial control (`"this dependency/version requirement does not exist"`) must score `0/12`.
- A word-bag control (correct vocabulary but wrong structure/offsets) must score `0/12`.
- Off-topic records must score `0/12`.
- Forged `vn_cnt`, forged `vna_next`, and stale-list controls must be detected by parser validation, not by string matching.

### Source boundary
- Source equality only: the table records what the static metadata says. It does not establish that the runtime loader accepts, resolves, or authenticates those versions.
- Any source quote must be opened and located before freeze. Candidate sources: host `elf.h` (structure definitions), GNU Binutils `readelf` source for `.gnu.version_r` interpretation, and the System V / gABI ELF specification. Microsoft PE/CHPE sources are out of scope and must not be reused for ELF claims.
- A source that does not define a field/tag must be rejected for that scope, with a flip condition, as in `S100`.

## 6. Observation, inference, and unknown

Observation:
- ELF header, section headers, dynamic tags, `.gnu.version_r` bytes, `.dynstr` bytes, and `readelf -V` output for the 12 pinned carriers.

Inference:
- That the parsed structures represent GNU symbol-version requirements and dependency/version metadata.
- That decoded flags correspond to `VER_FLG_BASE` / `VER_FLG_WEAK` or unknown bits.

Unknown:
- Whether the runtime loader will accept or resolve these versions.
- Whether the metadata is authentic, unmodified, or security-relevant.
- Whether the same structure appears in non-GNU, non-host, or non-ELF64 binaries.
- Whether version requirements are complete with respect to all runtime dependencies.

No execution, loader invocation, or authenticity verdict is permitted.

## 7. Risks

- Low carrier diversity: many host binaries depend on the same glibc versions, so the table may test parser fidelity more than version diversity. This is acceptable only if the claim is framed as parser/metadata fidelity, not coverage.
- 64-bit-only scope: no claim about 32-bit ELF, other architectures, or non-GNU toolchains.
- Source drift: host binutils/glibc versions change; the frozen source and carrier hashes must be rechecked before any admission.
- Expected-output circularity: mitigated only if byte offsets/hashes are required and expected-copy controls fail.
- Overreach risk: must not imply runtime loader acceptance or security properties.

## 8. Verification plan (bounded, no production scoring now)

Before any production run:
1. Freeze carrier manifest with hashes.
2. Freeze source quotes and locations.
3. Freeze controls and expected failure signatures.
4. Run selftests for parser, freeze integrity, and timestamp discipline.
5. Cap all probes with `timeout`, memory limits, and process caps; kill process trees afterward.
6. Do not run the production reader or REA until the frozen predicate is settled.

After data (separate round):
- Run the independent parser and oracle on the 12 carriers.
- Run all controls and record `0/12` or named refusal signatures.
- Record before/after counts, immutable revisions, and streams.

## 9. Recommendation

The claim fits kaidoku's domain and the depth axis if it remains a bounded static-metadata table on existing host binaries. It must not be presented as new coverage, runtime loader behavior, or authenticity. Proceed only after the frozen predicate, controls, and source boundaries above are settled; do not run the production reader or REA in this prep step. The held item remains untouched.

Report trailer: `.ufo/waves/round-34/prep/R34Overlap.md` (relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`).

## 10. Addendum — randomized `.dynstr` schedule and no-reader shortcuts

The strengthened second schedule changes only the linked `.dynstr` bytes by a secret same-length printable-ASCII permutation while deliberately leaving `vna_hash` unchanged, then transforms and sorts expected names accordingly. This is a useful control: it defeats a reader that merely recognizes an original carrier, looks up a precomputed expected record by path/id/hash, or copies expected names without parsing the transformed bytes.

Answer to the reopened question: **no conceptual no-reader shortcut should meet the target under the two-schedule opaque-path design**, because the second schedule's expected names are not knowable without reading and parsing the transformed string table. A constant, hardcoded, filename-keyed, id-keyed, size-keyed, or hash-keyed output can pass only the original schedule; it must fail the randomized schedule unless it actually parses the permuted bytes.

Residual conceptual shortcuts and required controls:

1. **External-tool shortcut**: a reader could shell out to `readelf`/`llvm-readobj` on the opaque path. That is not a no-reader shortcut; it is an indirect reader. If the claim requires a lane-owned minimal parser, the reader must be a single process with no subprocess/network and its imports/argv must be audited.
2. **Leaked-expected shortcut**: if expected JSON or translations are visible before scoring, a no-reader can hardcode them. Keep expected records and translations uncommitted/unpublished until after scoring; the final report may summarize counts and hashes, not full expected tables, before admission.
3. **Hash-only shortcut**: because `vna_hash` is deliberately unchanged, a reader could output names keyed by `vna_hash`. It still fails the randomized schedule because expected names are transformed while hashes are not; equality requires the transformed names.
4. **Offset-ignoring shortcut**: a reader could output transformed-looking names from bytes but omit byte ranges. The predicate must require parser-derived offsets and section ranges in every matched record; otherwise a no-reader with a guessed table could pass.
5. **State-carrying shortcut**: separate invocations and opaque paths prevent state reuse, but the control should also verify no sidecar files or environment-derived state are read.

Therefore the randomized schedule is sufficient only when combined with opaque paths, secret expected outputs until scoring, byte-derived offsets in the normalized record, and an explicit no-subprocess reader. It does not convert static metadata equality into runtime loader authenticity.