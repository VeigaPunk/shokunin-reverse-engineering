source: S101 (LLVM llvmorg-23.1.3, commit 0d261d1ca552c95a8f007e061c787ac7132fbcbc; corpus/evidence/round-33/sources/), S102 (https://learn.microsoft.com/en-us/windows/win32/debug/pe-format; served Markdown corpus/evidence/round-33/sources/pe-format.md)
verified-at: 2026-10-23 — pinned source reading and separate isolated instrument selftests; no admissible production carrier study
recheck: .ufo/waves/round-33/source-pins.json and source-anchor-map.json; re-open S101 Object-COFF.h:734-773 and S102 PE Format, File Headers / Optional Header

# CHPE declared structure: source facts versus a local profile

## Observations from the sources

S101 defines each code-map range as two little-endian u32 words: StartOffset and Length. The low two bits encode a tag, with named values 0 ARM64, 1 ARM64EC, 2 AMD64; clearing those bits gives the RVA. The separate code-range-to-entrypoint record is not the same layout. LLVM lld page-rounds emitted starts, calculates Length independently, and omits chunks without the execute bit when assigning map types. Its tag-0 arm is a default bucket, not affirmative instruction attribution. LLVM's object reader checks full referenced table byte extents.

S102 locates the PE signature through the DOS field at 0x3c and requires optional-header size and directory count to bound data-directory probes. Its header/section documentation is the scope used here. This does not reverse S100's retained rejection as CHPE offset/tag authority: those definitions remain absent from that specification.

## Inference and explicit local policy

The captured 64-bit field layout yields CHPEMetadataPointer at 0xc8 and its required field prefix through 0xd0; the captured metadata words occupy 92 data bytes. These are layout derivations, not claims that the PE specification publishes those offsets. Version-2-only, count ≤ 1024, single-section file-backed spans, named tags only, nonzero lengths, tag-0/1 length alignment, executable-section membership and non-overlap are the new reader's conservative profile. LLVM's empty-range comment and cross-section test are reasons NOT to call such exclusions universal invalidity. No blanket AMD64 length-alignment rule or global range sorting rule is imposed.

The fixed SKILL section is the actionable decision table. The classifier returns the first finding in its published precedence and retains decoded facts; not_candidate, outside_profile, malformed checked structure and structural_candidate have different meanings. It checks selected load-config/metadata/code-map spans, not every CHPE side table.

## Limits

No new production carrier study was completed: the planned independent fixture item was stopped by a provider cyber-policy refusal, and its later auto-switched outputs and all derived controls are excluded. The original 32-row claim remains unprovable; the source-backed table and independent isolated instrument selftests are not substituted for it. No held-out generalization, published-hybrid coverage, EC-view recovery, internal-function analysis or runtime behavior is claimed. A coherent false tag can pass every structural guard. Candidate means supported declarations only, never authenticated instructions, ABI correctness, genuine hybrid identity or Windows loadability. The old round-32 oracle/envelopes stay unchanged. Public finite fixture agreement cannot rule out arbitrary exact-hash lookup programs.
