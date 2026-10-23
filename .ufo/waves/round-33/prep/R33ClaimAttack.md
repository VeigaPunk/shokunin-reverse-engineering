# R33ClaimAttack — structural CHPE depth claim

## Status, axes and evidence boundary

Read-only preparation against contract base `428315a8` (assignment-supplied pin; not independently resolved here). **No claim score, admission, integration or runtime invocation.** The control outcomes below are proposed discriminators, not executed results.

- **Depth (primary):** a source-backed, actionable table that distinguishes checked code-map structure and bounds. Counting fixtures or script existence alone does not measure this.
- **Coverage (must not widen):** retain the round-32 synthetic exported-leaf DLL envelope. No new published-hybrid, internal-function, EC-view or runtime holding follows.
- **Calibration (no-harm):** distinguish structural declarations from instruction/ABI authenticity and Windows validity; distinguish source facts from parser-profile policy.
- **Operability (no-harm):** bounded, reproducible byte reads and useful typed findings; a selftest is instrument evidence, not an independent domain result.
- **Freshness / adjacency (no-harm):** pin source versions; do not turn this reader-side instrument into a second PE-format or build-tool authority. Contested ownership remains integrator-owned.

These names follow the opened axis definitions [E9]:9–16. No numeric proxy changes or saturation claim are proposed. The existing finite depth proxy explicitly excludes semantic correctness and generality [E12]:23–31.

## 1. Strongest local counterexamples

### A. Coherent wrong tag survives structural checks

The retained probe [E2]:49–56 reports changing a `.hexpthk` range from tag 2 (AMD64/X64) to tag 1 (ARM64EC), without changing its contents. The old classifier and LLVM display both trust the new tag. This is attributed prior-run evidence, not a new run.

A concrete static counterpart on the independently captured k04 layout is:

- original ranges: ARM64 `[0x1000,0x1040)`, ARM64EC `[0x2000,0x205c)`, AMD64 `[0x3000,0x3010)` [E2]:20–35;
- change only the third encoded start from `0x3002` to `0x3001`;
- `.hexpthk` has RVA `0x3000`, virtual size `0x10`, raw size `512`, raw pointer `0x1600`, and `IMAGE_SCN_MEM_EXECUTE` [E11]:124–139;
- all three ranges remain disjoint, nonempty, aligned, wholly file-backed and within executable sections. The supported metadata version, pointer, count, and presence of both ARM64/ARM64EC tags are unchanged.

**[INFERENCE from those captured facts]** Every proposed structural guard can succeed while the tag-to-content attribution is wrong. This is a structural-positive / semantic-unknown control, not a negative the new parser must reject. Rejecting it merely by fixture identity would hide the boundary. Conversely, passing it must never be described as authenticated ISA/ABI content.

The retained pure-ARM64 forgery [E2]:58–72 is additional evidence that the old classifier trusts declarations. Its ranges overlap (`[0x1000,0x1020)` and `[0x1010,0x1020)`), so a new no-overlap profile may legitimately reject that particular specimen. That does **not** establish general forgery resistance. Neither specimen demonstrates end-to-end false acceptance by the frozen twelve-carrier REA predicate; the pure-ARM64 specimen is outside its hash roster and no REA run was reported for it.

**Smallest safe correction:** name success `structural_candidate` or “supported file-backed mixed-tag declarations,” not “valid hybrid” or “valid mixed-code instructions.” State which metadata fields/tables were checked; code-map checks do not validate every CHPE-referenced side table.

### B. A stricter local profile is not a source-defined PE validity test

The opened LLVM emitter explicitly comments that MS link.exe “generates empty code ranges in some cases” [E4]:611–616. Its length calculation is `last RVA + last size - start`, with no blanket length-modulo-four condition [E5]:948–955. LLVM's header defines a separate unsigned 32-bit `Length`, not instruction alignment [E3]:764–772.

Consequently, treating every zero-length range, every non-four-byte length (especially tag-2 AMD64), every count above an arbitrary cap, or every non-file-backed/executable range as **universally malformed CHPE** lacks the cited authority. Strict refusal can be a useful bounded-profile choice; claiming it proves universal invalidity is a different, unsupported claim. An emitted-empty-range comment is not proof of Windows acceptance either.

**Smallest safe correction:** separate `malformed_checked_structure`, `outside_profile` / `unsupported`, `not_mixed`, `structural_candidate`, and `could_not_evaluate`. A resource cap or unsupported version is not a malformed-file observation. Do not force legitimate lookalikes to fail just to raise the negative tally.

## 2. Freeze the technical predicate, not a success vocabulary

Proposed bounded claim wording:

> Add one source-traceable CHPE code-map decision table and a bounded byte reader for the existing synthetic leaf-DLL envelope, distinguishing supported structural candidates, checked structural failures, and declared profile exclusions; no instruction, ABI, complete-PE or runtime validity claim.

The freeze should identify the exact table/rule addition and contain all of the following **before production observations**:

1. **Source contract:** immutable source commit, file hashes, line anchors, field widths/offset derivations, supported layout/version, and a row-by-row distinction between source fact and local policy. A source token somewhere in an entry is insufficient.
2. **Decision contract:** exact status and finding IDs, checked stage/span, required decoded facts, and deterministic precedence when several faults coexist. Prefer single-fault fixtures; do not let incidental first failures impersonate twelve distinct mechanisms.
3. **Instrument contract:** classifier, measurement driver, baseline adapter, dependencies, document check and generator pins. The original round-32 oracle and frozen predicates remain untouched. The driver must actually invoke the selected classifier, not calculate its answer from the expected column.
4. **Input/expectation contract:** independent, source-traceable expected records plus pinned bytes, identity and provenance. Known round-32 carriers/probes are disclosed re-observations, not newly unseen answers. Expectations must not be generated by importing or copying the classifier's decisions.
5. **Target contract:** every mandatory fixture exactly matches its independently expected status/finding and the frozen required decoded-fact projection; the substantive source-backed table is present and agrees with that contract. Print per-fixture mismatches and per-status/per-rule totals, not just “N handled.” Unexpected exceptions, missing reports, unreadable bytes and timeouts do not count as successful malformed-input classification.
6. **Control contract:** run the same measurement on every control below; retain exact input/implementation hashes, argv, UTC start/end, stdout/stderr, exit and per-case discrepancy. Commit receipts before any production data, regardless of whether data lives under `envelopes/`, JSON, TSV or another directory. `met_target=no` written by an author is not a scored receipt.

Source facts available from the opened material:

| Fact | Authority and limit |
|---|---|
| PE32+ load-config CHPE field is a 64-bit VA; required prefix through that field is derived as `0xc8 + 8 = 0xd0` | [E3]:676–714; LLVM uses the `offsetof + sizeof` condition and subtracts ImageBase [E6]:756–767. This is a field-availability threshold, not complete load-config validation. |
| Metadata starts with Version, CodeMap, CodeMapCount, each little-endian 32-bit | [E3]:734–759; the retained LLVM input supplies version word 2 [E10]:62–65. Header comments alone are not a complete version-acceptance specification. Freeze the chosen supported layout. |
| Each range record has two 32-bit words; type is `StartOffset & 3`, start is `StartOffset & ~3` | [E3]:762–773. Types 0/1/2 are named; value 3 has no enumerator. Do not confuse this with the separate StartRva/EndRva/EntryPoint structure. |
| Required table extent is count times the range-record width | [E5]:944–945; [E6]:771–778. Check the full referenced span and arithmetic, not merely its first RVA. Whole-file bounds alone are not section-span provenance. |
| `IMAGE_SCN_MEM_EXECUTE` is `0x20000000`; this lld release omits non-executable chunks from its code map | [E13]:335 and [E16]:475–486. This supports an **lld-emission-profile** check, not a universal Windows rule or proof of execution. Its tag-0 case is a default machine bucket, not an affirmative ARM64 instruction test. |
| This lld emitter page-rounds starts and derives lengths from the last chunk's end | [E5]:952–954. A 4KiB start requirement would describe this producer; the decoder's mask remains only two bits. It does not establish length alignment. |
| Nonoverlap, all-length alignment/nonzero, hard count/file caps, and strict no-zero-tail acceptance | Must be separately justified or explicitly labelled **profile policies**. No opened header establishes them as universal CHPE validity requirements; executable-only acceptance is producer-supported as above, still not universal validity. |

Do not call a checked prefix “all metadata validated.” LLVM also examines code-range-to-entry-point and redirection-table extents [E6]:781–798; a reader that checks only the code map must say so. Likewise, full-span single-section backing is a declared profile if cross-section mappings are not supported.

## 3. Cheapest controls and the measurements that discriminate them

All entries are **design-time counterexamples; none executed by this seat**. A target miss is needed for each impostor as a whole, not necessarily a failure on every individual fixture.

| Control | Cheapest attempted improvement | Frozen discriminator / smallest correction |
|---|---|---|
| **Do nothing** | Keep the base table and old tag-only oracle; merely wrap its output or replay the twelve known positive results. A weaker variant adds the new heading only. | Run the unchanged base behavior through a frozen, non-repairing adapter on the **same** cases as the new classifier. Include a source/profile-labelled full-span or range-containment failure the old oracle calls mixed: old `classify` never examines range lengths or range destinations [E1]:79–109. Require the substantive new table and exact independent findings, not a baseline miss caused solely by an absent new script/manifest. A base-pin failure or exit 2 is not evidence of improved discrimination. |
| **All false** | Return `candidate=false` / the same refusal for every input, counting all rejected junk as progress. | Freeze mandatory structural-positive lookalikes as well as negatives, with nonzero positive support in the target. Require exact failure identity for negatives, not merely any refusal. Include a valid boundary counterpart for each restrictive guard where possible. The coherent retag control in §1A must not be mis-scored as a semantic negative. Report true-candidate misses separately; negative-heavy accuracy cannot hide them. |
| **Junk / lexical bag** | Add rows containing CHPE, ARM64EC, `0xc8`, all finding names and a resolving source path, but no operative condition-to-result relationship; emit null, prose, empty objects, or success-shaped records. | Require the frozen structured result and byte-derived facts; missing/wrong types, unexpected findings or absent stage/span facts cannot be coerced into a match. Independently compare each table's actual condition, threshold, action and limitation to its exact source/policy row. File existence, keyword co-occurrence or shared-word counts do not establish depth. R32 denial/word bags already show that failure mode [E8]:71–76. |
| **No reader** | Driver hashes the DLL, then copies expected findings/reports into “observations” without invoking a structural reader; or invokes a stub returning canned reports. | The driver passes bytes/path, not expected finding or descriptive fixture ID, to the classifier and retains its actual output/status. Equality is to an independent expectation, not a driver-constructed report. Additionally score an explicit canned-output/no-read classifier on different byte layouts/facts: it must miss. An invocation receipt or successful SHA read alone does **not** show structural parsing; the unseen-byte and fact-sensitive controls below close that cheap gap. No REA call is required merely to prove this provider-free depth claim. |
| **Fixture-ID / label shortcut** | Map `bad_count`, `good`, numbered case IDs, path order, or a manifest's expected column directly to answers. | Give the classifier only opaque randomized filenames; independently permute runner IDs/order and keep expectations associated by an out-of-band runner key. Same bytes under changed names/IDs must retain the same structural projection; different bytes under the same nominal role must change the appropriate decoded facts/finding. No filename/ID branch is part of the byte predicate. Keep expected labels inaccessible through the normal classifier interface. A retained manifest remains auditable evidence, not an input authority for the classifier. |
| **Hash shortcut** | Compute SHA-256 and return the frozen expected record from a hash table; never interpret CHPE. This survives renaming, ID rotation and ordinary per-run pin checks. | Pin the implementation **before** independent unseen-byte representatives are selected; use a prospectively frozen source-backed transformation grammar, then freeze exact resulting bytes/hashes/expectations before scoring. Change irrelevant bytes (e.g. unused COFF timestamp) to alter the hash while preserving the structural projection; also vary meaningful valid RVAs/counts and one-fault boundaries so a constant fallback fails. Score the explicit old-hash lookup on those representatives. A hash miss is not malformed metadata. Do not conflate subject digest verification with structural evidence. |

**Hash-control impossibility boundary:** on a completely public finite byte set, an exact `sha256 → full expected report` table is observationally indistinguishable from a parser under output equality alone. More fields, repeated runs, shuffled labels and another SHA check cannot fix that. The ordering/independent unseen-byte construction above discriminates the specified cheap frozen lookup; it is not a proof that no possible finite shortcut exists. If no independent unseen-byte arm is available, disclose “finite fixture agreement,” not “hash shortcuts ruled out” or general parser competence. Freeze implementation/selection ordering explicitly; do not invent fresh controls or change targets after a miss.

Two cheap equivalence relations must therefore remain distinct:

- **Identity invariance:** identical bytes, different opaque names/IDs/order → same structural result (allow only predeclared path/provenance fields to differ).
- **Byte dependence:** changed hash with structure preserved → same structural projection; a meaningful span/tag/count change → the independently predicted facts/finding. Subject digest and unrelated metadata are outside the invariance projection, but must be checked independently.

## 4. Axis misfit, false provenance and source-free counting

1. **“12 malformed + 4 positive” is not sixteen units of depth.** Each counted mechanism needs the byte delta, independently derived expected result, exact source rule or explicit policy, and legitimate counterpart. Twelve mutations of one guard are repeated instrument checks, not twelve new domain facts. A selftest generated from the parser's own decision code is not an independent oracle [E7]:38.
2. **New thresholds must not be manufactured from the fixtures.** A hard cap chosen to fit them, assumptions that all sections start at the twelve carriers' fixed RVAs, or blanket alignment learned only from these leaves are profile choices. Labelling them sourced “malformed metadata” and then scoring self-authored examples is circular. The empty-range emitter comment is a concrete local counterexample to one such universal.
3. **Source authority is scoped.** S098 supplies assembler inputs, not complete format invariants or linked-range authenticity; S099 supplies the hybrid/default-view distinction; S100 was rejected for missing CHPE offset/tag authority [E14]:104–106. New LLVM structure/emitter bytes must be cited for the details they actually define, not silently attributed to the old Microsoft page. Builder, LLVM reader and source emitter share a toolchain family; agreement is not independent runtime evidence.
4. **Base discrimination matters.** The old classifier currently ignores metadata Version, every range length, range containment/overlap and instruction bytes [E1]:79–109. The new table must say what additional decision it enables. Repeating the twelve already-known successes or increasing the number of author-built cases is not itself the proposed depth move. The prior lane already records a rejection where the trivial baseline met a completeness-only target [E15]:9–11,44.
5. **No duplicate authority or identity cutover.** Keep the frozen R32 oracle/predicate intact and clearly name the new profile; do not silently replace what old `arm64x:true` meant. New fixture hashes and structural findings are not new REA Evidence IDs, demonstrated native-view capability, Windows-loader evidence, or expanded Core coverage.
6. **No lexical gate laundering.** QUALITY 48 requires controls; QUALITY 50 explicitly says the axis-fit gate's field/order checks do not prove they were actually scored [E7]:58–60. Retain the real counter receipts, not a table of author-filled outcomes. Do not reuse C2v3.

## 5. Fixable defects versus non-offsettable scope tradeoffs

**Fixable before freeze:** vague “valid” wording; missing full-span checks; conflating absent/unsupported/policy-limited with malformed; no positive lookalikes; first-failure ambiguity; a label/manifest-driven driver; unpinned source/expectations; baseline measured only by missing files. Correct the table/profile, frozen output contract and controls without touching the R32 freeze.

**Not repaired by a higher fixture count:** claiming semantic/runtime validation from metadata; labelling a source-unsupported restriction universally malformed; claiming all hash shortcuts excluded on a public finite set; relabelling synthetic re-observation as coverage. These would trade depth/calibration/coverage honesty for an attractive tally. More successful fixtures cannot offset that harm. The canonical Rust judge, not this critic, owns the axis and round outcome.

**Smallest safe overall correction:** freeze one narrow, source-traceable code-map profile; retain semantic-unknown structural positives; separate policy exclusions; measure exact independent facts/findings against an honest base; score all six cheap controls plus independent byte/name variants before data. Do not promise authenticity or generality that the profile cannot observe.

## Evidence locators and pins

All opened 2026-10-23; local source bodies were read using specialized tools. Pin values below are from the named freeze or source-seat receipt, **not newly recomputed by this review**.

- **E0** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/prep-contract.txt`: mandatory containment, base, no-score and held-item boundaries; read first.
- **E1** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/arm64x_oracle.py`:36–109. Frozen at `9a73680af21b002e3b99956c89234b2bbde2a71b`; recorded SHA-256 `17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686` in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json`:42.
- **E2** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2CHPEBits.md`:14–18,20–35,49–72. Retained attributed forgery SHA-256 `1542e5102fbb42e7c951d3e1ee27373824c3fd8e80ee6adf2174dac24efbc7f9`; fixture itself was not opened or run here.
- **E3** [LLVM Object/COFF.h at commit 0d261d1ca552c95a8f007e061c787ac7132fbcbc](https://github.com/llvm/llvm-project/blob/0d261d1ca552c95a8f007e061c787ac7132fbcbc/llvm/include/llvm/Object/COFF.h#L676-L773), opened source-seat copy `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/Object-COFF.h`. Source seat reports SHA-256 `214d3f4a186be95dee7df0d19edaf04408b45f9d243152e2a4c2fb2f762f2320`. Its opened tag receipt `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/tag-object-llvmorg-23.1.3.json` maps annotated tag `856f0005e57023e63664c560a829c620360ea1f1` to that commit. No signature verification was executed here.
- **E4** [LLVM lld/COFF/Writer.cpp at the same commit](https://github.com/llvm/llvm-project/blob/0d261d1ca552c95a8f007e061c787ac7132fbcbc/lld/COFF/Writer.cpp#L592-L631), opened `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/Writer.cpp`:592–631. The emitter's comment is evidence of its stated producer boundary, not a Windows-loader test.
- **E5** [LLVM lld/COFF/Chunks.cpp at the same commit](https://github.com/llvm/llvm-project/blob/0d261d1ca552c95a8f007e061c787ac7132fbcbc/lld/COFF/Chunks.cpp#L944-L955), opened `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/Chunks.cpp`:944–955.
- **E6** [LLVM lib/Object/COFFObjectFile.cpp at the same commit](https://github.com/llvm/llvm-project/blob/0d261d1ca552c95a8f007e061c787ac7132fbcbc/llvm/lib/Object/COFFObjectFile.cpp#L738-L798), opened `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/COFFObjectFile.cpp`:738–798. These are implementation checks, not a complete PE specification.
- **E7** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md`:38,48–68 (independence, pre-data instruments, known answers, source binding, controls and disclosure limits).
- **E8** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md`:71–76,111–117 (lexical false acceptance and routed limits).
- **E9** `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md`:9–16,25–38, read for axis definitions, not as an alternate task assignment.
- **E10** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s`:59–94. Frozen SHA-256 `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4` in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json`:50.
- **E11** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/independent-pe/readobj-k04.txt`:106–155. A retained reader capture, not direct carrier bytes or a fresh readobj invocation; its displayed machine label is not the raw COFF machine.
- **E12** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md`:19–31,3278–3298.
- **E13** [LLVM BinaryFormat/COFF.h at the same source commit](https://github.com/llvm/llvm-project/blob/0d261d1ca552c95a8f007e061c787ac7132fbcbc/llvm/include/llvm/BinaryFormat/COFF.h#L335), opened `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/BinaryFormat-COFF.h`:303–337; source-seat reported SHA-256 `a44641df4bf2ecf96bbfa86b5145c3679b043a579a5df6afba1ac2852b593339`.
- **E14** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`:104–106.
- **E15** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-30.md`:9–11,44.
- **E16** [LLVM lld/COFF/Chunks.h at the same source commit](https://github.com/llvm/llvm-project/blob/0d261d1ca552c95a8f007e061c787ac7132fbcbc/lld/COFF/Chunks.h#L475-L486), opened `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/Chunks.h`:475–486; machine aliases opened in `/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/Config.h`:39–42. Membership is an emitter decision, not instruction validation.

## Execution, limitations and containment

Actual UTC review date: **2026-10-23**. No code/command execution interval is claimed: **argv, process stdout/stderr and exit are not applicable; no process was launched**. Tool activity used `read`, `grep`, `glob`, short peer coordination, and this assigned report write. A read-only clock sample returned `/proc/driver/rtc` date `2026-10-23`, time `08:13:15`; contemporaneous opened source HTTP metadata recorded `Fri, 23 Oct 2026 08:10:10 GMT` (`/fast/scratch/hyaku/kaidoku-r33/R33SourceChpe/coff-object.headers`:13). The RTC's timezone was not independently configured/verified, so no fabricated precise UTC execution timestamp is asserted.

No builds, tests, selftests, parser/counter runs, carrier execution, REA, Git/JJ command, package transaction, network fetch by this seat, new runtime, production code/doc/source change, or hold-item inspection/retry. No tools installed/updated. No scratch outputs, background jobs, services or process trees were created. No verification scores or shortcut-kill receipts exist from this review. Only the assigned report was written; source/pin equality, new-parser behavior and the proposed discriminators remain unexercised here.

Trailer: `.ufo/waves/round-33/prep/R33ClaimAttack.md`
