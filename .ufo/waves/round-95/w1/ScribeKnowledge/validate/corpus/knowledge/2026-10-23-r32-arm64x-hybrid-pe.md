source: S099 (Microsoft Learn, Arm64X PE Files, https://learn.microsoft.com/en-us/windows/arm/arm64x-pe, lines 50–64 of retained source); S098 (LLVM llvmorg-23.1.3 load-config assembler inputs); original REA envelopes and producing argv/package identities in corpus/evidence/round-32/c1/runs.tsv
verified-at: 2026-10-23, round 32, attempt 2; original producer ran after pre-data control receipts landed at 33393e594f1e278777fa49020b42c66ac4fa352e
recheck: `env GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC JAVA_HOME=/usr/lib/jvm/java-21-openjdk python3 -I -B tools/round-32/c1-arm64x-positive.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>`; target `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0. Write mode exits 3 and is never a claim receipt.

# ARM64X hybrid PE: bounded native-view import and overview

## Surface and result

R32-C1 is coverage of a previously reserved PE edge class, not a new REA verb: at base `283aad7f`, PROVINCE.md names ARM64X only in Frontier. The widened historical sweep (`.ufo/waves/round-32/a2audit/A2NoveltyFull.md`) found earlier ARM64X-targeted linker exploration, including a non-genuine hybrid, but no recorded REA run on an observed hybrid file. This entry does not claim the lane never named ARM64X or never tried its linker.

Observation: REA 6.5.0 `inspect --format json --full-output` produced twelve successful `binary_overview` envelopes on the frozen, author-built DLLs. Their compared format, architecture, document, image base, ordered segment fields, segment count and procedure count match the frozen oracle/predictions in the producer run. That write-mode comparison omits the committed-record clause; only the later measure-mode receipt is a claim measurement. The retained full envelopes, not these summary counts alone, support the recheck.

| id | subject sha256 | native/EC exports | optimization | observed segments | observed procedures | evidence_id |
|---|---|---|---|---|---|---|
| k01 | 2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989 | 1/1 | -O1 | 8 | 1 | `ev_d7fe3164aef68b83604ff240aaa7cea64ce097fbe0780dbe9b1f88d8431a1bdf` |
| k02 | a16ba36205f584b0a1589895ed31feffcc36eda692b81e675cdfeadb819519d4 | 2/2 | -O2 | 8 | 2 | `ev_032c2af47055785b6668265ce05feaf6fc9a28f211fef43a8489eb303c0d6699` |
| k03 | 0291e17bd517802b44984fb8e8fcc2cec0266b02ded1cb81bccea040a737b73d | 3/3 | -O0 | 8 | 3 | `ev_7d983639597236a8c25133a01fe6364a7ef12ab08fadde7663b7ec76dd50a183` |
| k04 | 3c783318ea3aea29033460edb17b4cade7b0eca675e0d5410d278672d2bfb386 | 4/1 | -O1 | 8 | 4 | `ev_0a5879b6962d52807bf842ab2fc5a2c5b801c425a76c1996c478dec5cf31b57a` |
| k05 | cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf | 1/4 | -O1 | 8 | 1 | `ev_fec48cb3a4bee51c883fb18ae569f6ceffc0e7f3251c048af095ee479f23bee5` |
| k06 | 6c45a3ce1c3e9b91719a3ded213d995c35947af221145b14c06f0ca838247b3c | 5/5 | -O0 | 8 | 5 | `ev_2b7fb69a2e46eb319841d9783d7e00dbe6b65c9a9ea58bb8a70b3dca687c9a34` |
| k07 | 84a78b7894fa11f876734d2bd926d8e3e73f08be3f2a6f93b35925e3605afb6f | 6/2 | -O2 | 8 | 6 | `ev_d2cc4361b7c8c897dad143d207d019ab2fed8875acabeb25633b85ca94cd9570` |
| k08 | b158eaf7c7417400202f06acc0867013185260efdf296a6dbbe622e873e3215c | 2/6 | -O2 | 8 | 2 | `ev_8642af3e9c8bc5aa55e7764fd5a7972d4a37adc340ed55c17f4fbbf6edfbe61e` |
| k09 | cf0148615fce4399e067715eb48554f63c4a30cf04a40c75776d58b1a2b82a87 | 7/3 | -O1 | 8 | 7 | `ev_3cd5776b21c117cdd9b9b0298d20edae5c02b9933f2b1fdde93de266f0ae98dc` |
| k10 | a48499d2df92de871fd3e7c7d8cba63bbfbc019fd84ee312bdbdada632c766c7 | 3/7 | -O0 | 8 | 3 | `ev_63b7f3d4aecbd0e560c0d809ea83f4261900855ff7c5598a92dcc3204e99eebf` |
| k11 | b5e2af7f2b96fd66f87ed0be99e576fa94b7f843d088bdb05e212ac67592d181 | 8/8 | -O2 | 8 | 8 | `ev_85d09ca4512cdea17c18dbb20935d1c627cfd189809e04e448cab07ee8a715af` |
| k12 | 8c852d075fab64aca5c165ff3b907507d62d409972bbfddb72543ef3efea04fa | 1/2 | -O1 | 8 | 1 | `ev_9a2cd4a45022eecf01ce6d46ff8fbcbbec1c64fa0c6c4151b45009cafd3338a1` |

These twelve rows are enumerated by `corpus/evidence/round-32/c1/carriers.tsv`; the table is regenerated from each corresponding `envelopes/<id>.json` subject and normalized_result. Producing calls and UTC start/end are retained in `runs.tsv`; compiler reproduction and an LLVM dual-view witness are in `.ufo/waves/round-32/a2audit/A2BuildRecheck.md`.

## Interpretation and decision table

| Observation / condition | Action / limit |
|---|---|
| On-disk COFF machine is 0xAA64 | Do not infer a plain ARM64 file or a hybrid from that value alone. Require CHPE metadata and the code-map range evidence. LLVM displays these linked bytes as ARM64X, while the raw machine bytes remain 0xAA64. |
| Frozen oracle finds at least one ARM64 and one ARM64EC code-map range | Treat this as a structural classification for these bytes, not proof of Windows loader validity or execution. The independent build witness also exposes an x64 thunk range. |
| REA reports architecture arm64 and procedure_count equal to native exports | This is the native view. It does not recover the EC view: k05 has one native export and four EC exports but REA reports one procedure. Seven roster rows have unequal native/EC counts; the frozen motivation's six is an erratum, not a changed predicate. |
| Need dual-view decompilation, internal-function recovery or runtime behavior | Remains Frontier. This overview experiment does not establish any of those capabilities. |
| Provider not configured under an Eval subprocess | Retain the failure; pass the existing GHIDRA_INSTALL_DIR and JAVA_HOME explicitly after diagnosing their absence. Provider failure is not evidence that a forgery-control's committed-record check ran. |

S099 directly states that Arm64X combines classic Arm64 and Arm64EC code and defaults to an Arm64 appearance. S098 supplies upstream assembler inputs, not linked carrier bytes or REA behavior. The separate Microsoft PE Format source is rejected for the specific CHPE offset/tag claim (S100): its machine-type table cannot support that detail.

## Reproduction and boundaries

1. Use `bash tools/round-32/build-arm64x-carriers.sh <LANE> <NEW-OUTPUT>` with LLVM 23.1.3. The independently repeated build matches all twelve frozen SHA-256 values; do not overwrite the immutable originals.
2. Keep the pinned DLLs at the paths in carriers.tsv. Never execute them; this work reads their bytes through the configured Ghidra provider.
3. Run the recheck at a committed revision containing the entry, Core row and envelopes. It re-hashes carriers and compares the whole committed envelope with a live run except `meta`; entry evidence IDs must agree. The record check establishes association, not cryptographic authenticity.
4. Audit `claims.json` with `tools/round-32/freeze-integrity.py --round 32 --claims .ufo/waves/round-32/claims.json`; source and model prose are not substitutes for the frozen predicate.

Limits: twelve synthetic, exported-leaf DLLs, one LLVM release, one host and REA pin, configured Ghidra 12.1.4 provider. No published third-party ARM64X binary, target execution, EC decompilation, internal/call-reached function count, or section with VirtualSize greater than SizeOfRawData is tested. The procedure-count rule is local to this leaf-export class; the segment-length max rule is not separated from raw size by these inputs. The LLVM witness is independent of the lane oracle and REA, not of the builder's toolchain release. PE-format maintenance belongs outside this lane's reader-coverage claim.
