# Round 33 source/frontier ledger — WSourceLedger

## Finding

The admissible revision reviewed is `d7076120e4f00c6d18aa77b8764d14861e820eb2` (base `428315a8f5674b952def862910af6e07a6c2224b`). The lane's later `@` was `124e978e53b0347a4235506c022348cf3706e785`; commit comparisons and source-blob reads below explicitly name the pinned revision, not `@`.

S101 and S102 are source-backed **detail on the existing synthetic CHPE/ARM64X PE surface**, not a coverage or claim-target expansion. The new table distinguishes LLVM's declared code-map structure and reader/emitter choices from a local conservative profile, and uses Microsoft's PE document only for PE-header bounds. Neither establishes Windows-loader acceptance, instruction authenticity, ABI correctness, EC-view recovery, runtime behavior, published-hybrid coverage, or a new REA result. R33-C1 remains stopped **unprovable / honest stop**: its 32-row target and source/table checks have no admissible fixture manifest or after-measurement; source and isolated instrument evidence do not substitute for it. Numeric axis gain remains 0 (`.ufo/waves/round-33/claim-stop.json`).

## Source census and scope accounting

The pinned `source-pins.json` has **9** file entries, counted from the committed blob with `jq '.files|length'` (exit 0, stdout `9`). They comprise two source families:

- **S101 — LLVM `llvmorg-23.1.3`, commit `0d261d1ca552c95a8f007e061c787ac7132fbcbc`: 8 retained LLVM files** — `Object-COFF.h`, `BinaryFormat-COFF.h`, `Chunks.h`, `Chunks.cpp`, `COFFObjectFile.cpp`, `Writer.cpp`, `arm64ec-codemap.test`, and `COFFDumper.cpp`. The last is explicitly a supplementary generator citation, not a classifier dependency; the test is one capture, not another source family.
- **S102 — Microsoft PE Format served Markdown: 1 capture**, `pe-format.md`.

All nine blobs read from `d7076120e4f00c6d18aa77b8764d14861e820eb2` match their recorded SHA-256 values in `source-pins.json`; exact paths, hashes, byte counts, argv and per-command times are in `pinned-source-checks.json`. The source rows added are exactly two: S101 and S102.

S101's pinned `Object-COFF.h:734-773` defines little-endian 32-bit metadata fields and a `chpe_range_entry` with separate `StartOffset` and `Length`; `TypeMask = 3`, `getStart()` clears those bits, `getType()` reads them, and the enum names tags 0/1/2 as ARM64/ARM64EC/AMD64. The other retained LLVM anchors support the narrower reader/emitter statements: the object reader checks the referenced code-map table extent; lld excludes non-executable chunks from map assignment, uses ARM64 as its default machine bucket, page-rounds emitted starts, and computes length separately. These are LLVM implementation facts, not Windows or ISA truth.

S102's pinned capture states that the PE signature offset is at DOS location `0x3c` (line 133), that `SizeOfOptionalHeader` bounds directory probes and `NumberOfRvaAndSizes` bounds directory entries (lines 222-224), and that the Windows loader limits sections to 96 (line 141). These support header probing only; they do not supply CHPE offset/tag authority.

### S100 remains rejected

The pre-existing S100 row is still `rejected`. Its narrow rejected scope is the PE Format specification as authority for `CHPEMetadataPointer` offset and code-map tag semantics. The old flip still requires the searched Microsoft representations to document both the PE32+ offset `200/0xC8` and numeric tag meanings. S102 admits a different, header-bounds scope from a newly served Markdown capture; it does not satisfy that flip and does not reverse S100. S098/S099 retain their prior mined scopes. No source status, recheck, or `used-by` cell among the old rows changed in the base-to-pinned diff.

## Entry trio and Gate quotes

The three aligned R33 entry surfaces are `corpus/SOURCES.md` (new S101/S102 rows), `corpus/knowledge/2026-10-23-r33-chpe-structural-profile.md` (source facts versus local policy), and `SKILL.md` (`## CHPE structural profile — round 33`, the decision table). The knowledge entry correctly labels `0xc8/0xd0`, version-2-only, count cap, mapping/overlap/alignment/executable-section rules as derived or local profile constraints, not universal PE invalidity. The SKILL table preserves that distinction and says a structural candidate is not a genuine hybrid verdict. `corpus/lessons/round-33.md`'s Gate quotes match the pinned captures:

- S101, `Object-COFF.h:768`: “The two low bits of StartOffset contain a range type.” — 10 words.
- S102, `pe-format.md:133`: “At location 0x3c, the stub has the file offset to the PE signature.” — 13 words.

The quotes are contiguous and within the 25-word limit. **The committed `quote-manifest.json` counting command is not runnable as written:** its nested double quotes are stripped by the shell, and the recorded command exits 1 with Python `SyntaxError`. A corrected stdin-based count over the pinned manifest exits 0 and returns the 10/13 counts above. This is a command/receipt defect only; it does not falsify the quoted text. No quote-fidelity or document gate was run.

## Search-log correction (recommendation; no source-registry edit made)

The R33 Search log sentence in `corpus/SOURCES.md` has the right family and capture totals: **two families, nine pinned captures, two new rows, S100 unchanged**. Clarify what the count measures and give a runnable `jq` argv; the nine are files, not nine independent authorities or benchmarks. Suggested text:

> Opened two primary-source families and retained nine pinned capture files (eight LLVM files at `0d261d1c`, including the supplementary `COFFDumper.cpp` citation, plus one served Microsoft PE Format Markdown capture). `jq '.files|length' .ufo/waves/round-33/source-pins.json` over the committed pin manifest returned 9. Added mined rows S101 and S102 for distinct LLVM-structure and PE-header scopes; S100's CHPE-authority rejection and all prior status/recheck/used-by cells remain unchanged. No carrier-study result is admitted.

This is an accounting clarification, not a correction to the underlying counts. Do not describe the source captures as independent carrier cases or as a completed claim measurement.

## Immutable-cell check

Read-only `jj diff` from base to the pinned revision covered `corpus/SOURCES.md`, the knowledge entry, `SKILL.md`, and the R33 lesson. It shows the S101/S102 rows and R33 search-log line as additions; pre-existing S098/S099/S100 rows and their cells are unchanged. The previous SKILL section remains context and the R33 section is appended; the knowledge entry and R33 lesson are new files. A separate base-to-pinned diff of `corpus/lessons/round-32.md` is empty (exit 0), so the original S100 Gate rejection text is unchanged. This is the requested scoped immutability check, not a claim that every lane document was audited.

## Behavior, gates, and limits

- **Behavior:** no product behavior changed by this scribe seat; no product or registry file was written.
- **Gates:** no build, test, selftest, formatter, quote-fidelity gate, document-spec gate, REA/MCP call, or carrier execution was run. The work consists of source/document reads, pinned-blob SHA-256 checks, source/quote counts, and read-only revision diffs; none is an admission verdict.
- **Out of scope:** no held output or derivative was opened or used; no fixture construction, replacement benchmark, claim revival, scope widening, source edit, registry edit, or Git/JJ write occurred. No tool was installed or updated.
- **Known limits:** source citations establish LLVM and Microsoft documentation statements only. Counts cover pinned files and rows only; they do not count screened leads or fixture candidates. No non-author review or canonical judgment is claimed.

## Command/evidence record

Evidence-producing argv, UTC start/end, stderr, exit codes and outcomes are retained in the scratch receipts below. Full diff/count stdout is retained where material; `jj file show` receipts retain source-blob sizes and SHA-256 values plus the relevant excerpts/parsed manifest fields rather than duplicating whole blobs. The committed blobs remain available at the pinned revision.

| Check | UTC / exit | Outcome |
|---|---|---|
| `jj --repository <lane> diff --from 428315a8f5674b952def862910af6e07a6c2224b --to d7076120e4f00c6d18aa77b8764d14861e820eb2 -- corpus/SOURCES.md corpus/knowledge/2026-10-23-r33-chpe-structural-profile.md SKILL.md corpus/lessons/round-33.md` | 2026-10-23 09:31:19.558061–09:31:19.605823 UTC; 0 | Additions only on the changed source/entry surfaces; stdout in receipt. |
| `jj --repository <lane> diff --from 428315a8f5674b952def862910af6e07a6c2224b --to d7076120e4f00c6d18aa77b8764d14861e820eb2 -- corpus/lessons/round-32.md` | 2026-10-23 09:37:22.610979–09:37:22.649221 UTC; 0 | Empty stdout/stderr; old rejection lesson unchanged. |
| `jj file show --revision d707... .ufo/waves/round-33/source-pins.json` then `jq '.files|length'` on that blob | 2026-10-23 09:34:27 UTC; both 0 | `9`; all 9 `jj file show --revision d707... <pinned-source>` reads exited 0 and SHA-256 matched. Per-file exact timing is retained. |
| Pinned `jj file show` of `Object-COFF.h` and `pe-format.md` | 2026-10-23 09:35:15 UTC; both 0 | Excerpts at the cited lines; full-blob stdout digests match the source pins. |
| Exact `counting_command` from pinned `quote-manifest.json`, run through `/bin/sh -c` | 2026-10-23 09:36:51.047119–09:36:51.072515 UTC; 1 | Empty stdout; `SyntaxError` from lost nested quoting. |
| Corrected `python3 -c 'import json,sys; print([(q["path"],len(q["quote"].split())) for q in json.load(sys.stdin)["quotes"]])'` with the 590-byte pinned manifest on stdin | 2026-10-23 09:37:06.770450–09:37:06.781680 UTC; 0 | Exact output: `[('corpus/evidence/round-33/sources/Object-COFF.h', 10), ('corpus/evidence/round-33/sources/pe-format.md', 13)]`. |

## Artifact paths

- Lane report (only lane write): `.ufo/waves/round-33/w1/WSourceLedger.md`
- Scratch receipts: `/fast/scratch/hyaku/kaidoku-r33/w1/WSourceLedger/receipts/source-surface-diff.json`, `old-s100-lesson-diff.json`, `current-revision.json`, `pinned-source-checks.json`, `pinned-source-excerpts.json`, `pinned-quote-command.json`, and `pinned-quote-count-corrected.json`.

The temporary `jj cat --help` probe returned exit 2 (`jj` has no `cat` subcommand); subsequent committed-file reads used the supported `jj file show` command. No lane state was changed by these read-only probes.
