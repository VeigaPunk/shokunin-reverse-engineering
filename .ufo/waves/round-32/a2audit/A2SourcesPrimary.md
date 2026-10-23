# Round 32 attempt-2 — A2SourcesPrimary source audit

**Axes:** R32-C1 coverage (ARM64X hybrid PE, Frontier → Core); R32-C2 calibration (Capabilities summary versus pinned non-author closure). This seat's assigned work was limited to source capture and proposed S098/S099 rows; it did not execute either counter or satisfy a gate. I read `claims.json` for C1 and `claims-v3.json` for C2. The C2 v3 file says it supersedes C2 only; C1 remains in `claims.json`. The assignment supplied freeze identifiers `9a73680a` and `f382e3b7` and base `283aad7f`; I did not independently inspect Git/JJ history.

## Findings

The Microsoft Learn page directly supports the hybrid interpretation, rather than an inference from `IMAGE_FILE_MACHINE_ARM64`/machine value alone: it describes Arm64X as one binary containing classic Arm64 and Arm64EC code, with architecture-dependent OS transformations. The pinned LLVM ARM64EC load-config fixture independently shows a load-config pointer to `__chpe_metadata`, which references `__hybrid_code_map`, x64 code-range-to-entry-point data, and ARM64X redirection metadata. Its paired ARM64 fixture is a distinct `.rdata` load-config input. The LLVM fixture is assembler test input, however: its map/range symbols are references, not definitions of map entries in these files. It does not, by itself, prove the linked PE has both ARM64 and ARM64EC ranges. These sources support the class rationale beyond a machine value, but do not establish the frozen oracle's per-carrier classification or REA behavior.

### Reopened source quotes

- S099 / Microsoft Learn, `Arm64X PE Files`, line 50: “Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together.” Source URL: <https://learn.microsoft.com/en-us/windows/arm/arm64x-pe>; page `ms.date` 2025-11-06, fetched 2026-10-23; response SHA-256 `a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66`.
- S099 / same source, line 56: “The built Arm64X binary has two sets of code, entry points, and other elements”. Same URL/date/hash.
- S098 / LLVM `loadconfig-arm64ec.s`, lines 20, 64, 66–67: “`.xword __chpe_metadata`”; “`.rva __hybrid_code_map`”; “`.rva __x64_code_ranges_to_entry_points`”; “`.rva __arm64x_redirection_metadata`”. URL: <https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s>; fetched 2026-10-23; SHA-256 `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4`.
- S098 / paired `loadconfig-arm64.s`, lines 1–5: “`.section .rdata,"dr"`” / “`.word 0x140`”. URL: <https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64.s>; fetched 2026-10-23; SHA-256 `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d`.

These are exact excerpts reopened from the saved response bytes; each quote is at most 25 contiguous source words. The two LLVM digests equal the corresponding `claims.json` frozen-input digests.

## Proposed source rows (draft only; no lane registry edit)

S098:

```text
| S098 | LLVM lld COFF ARM64 and ARM64EC load-config test inputs (llvmorg-23.1.3) — https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s; https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64.s | code | A | Paired upstream assembler inputs for ARM64EC CHPE load-config metadata and a plain ARM64 load-config comparison; not linked carrier bytes or Windows/REA behavior | LLVM llvmorg-23.1.3 raw files fetched 2026-10-23; SHA-256 `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4` and `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d`; ARM64EC lines 20, 59–67; ARM64 lines 1–15 | Pin the upstream test inputs used to construct the C1 carriers; the ARM64EC input's CHPE/hybrid-map references are structural evidence, not proof of populated map ranges or a successful carrier analysis. | mined | 2026-10-23 | on-release | corpus/evidence/round-32/c1/inputs/ |
```

S099:

```text
| S099 | Microsoft Learn, Arm64X PE Files — https://learn.microsoft.com/en-us/windows/arm/arm64x-pe | docs | A | Microsoft's definition and loading model for a PE that combines classic Arm64 and Arm64EC code; not a specific carrier's parsed layout or REA/Ghidra capability | Microsoft Learn response fetched 2026-10-23; page `ms.date` 2025-11-06, `git_commit_id` `ab16bb917a5a6310749000da77644e7c664759c1`; SHA-256 `a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66`; `Arm64X PE Files` lines 50–64 | Establish that ARM64X denotes hybrid Arm64/Arm64EC content and documented architecture-dependent views, not merely an ARM64 machine value; make no claim about the lane's reader or any tested carrier. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md |
```

## Gates and limits

The frozen C1 `doc_gates` text requires (1) `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` to cite S099 and (2) a `PROVINCE.md` row naming ARM64X and that entry under a nearest preceding `Core` heading, not Frontier/Adjacent/exclusion. These source findings and row drafts do not show that either gate is present or that C1's target passes. C1 predicate additionally requires an ARM64 machine value **and** a CHPE code map with at least one ARM64 and one ARM64EC range, plus its frozen live/committed-envelope conditions; the source inputs do not establish those per-carrier results. C2 v3's four capability statements, anchors, identity/description/evidence rules and target were read as frozen claim context only; no C2 counter or documentation gate was run here.

Out of scope/not performed: no lane source, docs, registry, index, or Git/JJ state edits; no carrier generation, binary execution, REA run, counter/predicate invocation, build, test, or gate evaluation; no held-item inspection/retry; no delegation; no tool installation. No sandbox clone or sandbox revision was used. The captured source snapshots and this report are the only artifacts from this seat. No claims are made about another seat's execution evidence.

## Commands and observed outcomes

`mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary && df -h /fast` printed:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  559G  245G  70% /fast
```

Exact bounded fetch commands (all returned HTTP 200):

```text
curl --fail --location --silent --show-error --max-time 60 --max-filesize 1048576 --header 'Accept: text/markdown' --output /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/arm64x-pe.md --write-out 'http_code=%{http_code} size_download=%{size_download}\n' 'https://learn.microsoft.com/en-us/windows/arm/arm64x-pe'
```

Output: `http_code=200 size_download=7386`

```text
curl --fail --location --silent --show-error --max-time 60 --max-filesize 1048576 --output /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/loadconfig-arm64ec.s --write-out 'http_code=%{http_code} size_download=%{size_download}\n' 'https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s'
```

Output: `http_code=200 size_download=2686`

```text
curl --fail --location --silent --show-error --max-time 60 --max-filesize 1048576 --output /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/loadconfig-arm64.s --write-out 'http_code=%{http_code} size_download=%{size_download}\n' 'https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64.s'
```

Output: `http_code=200 size_download=423`

Hash and size command:

```text
sha256sum /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/arm64x-pe.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/loadconfig-arm64ec.s /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/loadconfig-arm64.s && wc -c /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/arm64x-pe.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/loadconfig-arm64ec.s /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/loadconfig-arm64.s
```

Observed SHA-256 / byte counts:

```text
a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66  arm64x-pe.md                         7386
c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4  loadconfig-arm64ec.s                 2686
7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d  loadconfig-arm64.s                   423
```

**Artifacts:** source snapshots under `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourcesPrimary/`; this report at `.ufo/waves/round-32/a2audit/A2SourcesPrimary.md`. No packages/tools were installed or updated.
Report: `.ufo/waves/round-32/a2audit/A2SourcesPrimary.md`
