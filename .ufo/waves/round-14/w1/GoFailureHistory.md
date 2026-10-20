# Historical Go symbol-recovery collapse: `op` 2.34.1 → 2.40.0

**Access date:** 2026-10-20  
**Axes:** coverage (recover the historical pair and counts); calibration (separate the round-4 observed run from this round's source-only diagnosis).  
**Scope:** corpus/source inspection only. No REA diagnostics, target execution, builds, tests, linters, formatters, or smoke runs were performed; no tools were installed.

## Finding

The corpus records a **historical round-4 Ghidra 12.1.4 run** over two real cached `1password-cli` executables: `op` 2.34.1-1 / Go 1.25.7 and `op` 2.40.0-2 / Go 1.26.8. The report records 33,060 procedures on the older binary versus 11,595 on the newer one; the newer inventory contains 11,588 `FUN_*`/`thunk_FUN_*` auto-names and `entry` as its sole real name. It records `main.main` as searchable only on the older binary and the same ELF-entry role as `_rt0_amd64_linux` versus `entry`; an explicit function comparison reports `mismatched` identity. This is a pair-specific recorded observation, not a result produced or revalidated in round 14.

The **round-14 source-only diagnosis** is narrower than the old report's causal wording: the hash-pinned Ghidra 12.1.4 source declares Go 1.15–1.25 as its supported range. For an out-of-range Go version, `getGoBinary` emits an “Untested Go version” message, but that check itself does not return; it continues to API-snapshot lookup. `GoApiSnapshot.get` returns `EMPTY` if no matching snapshot file is found. These source paths make a version/bootstrap issue a plausible diagnosis to investigate, but they do not prove which path the old `op` analysis took, whether a Go 1.26 snapshot was present, or that this was the cause of the observed symbol loss.

## Evidence chain

1. **Pair identity and artifact pins — historical record.** The round-4 entry identifies cached pacman package members `usr/bin/op`, sizes 41,210,040 and 43,475,106 bytes, Go toolchains 1.25.7 and 1.26.8, and only abbreviated member SHA-256 values (`d24dc5d4…` and `8d029d2c…`). It says the members came from `tar -xOf <pkg> usr/bin/<name>` and that their hashes reproduce round 2's `op` values. This corpus entry does not preserve full digests.
   - **Present-day pin check:** the cached `1password-cli-2.40.0-2-x86_64.pkg.tar.zst` still exists. Hashing its `usr/bin/op` stream today yielded `8d029d2cd7112177132b1b20ef0b6012ba9a9dd9ef48d7f7660f2e8071d4f7b2`, matching the recorded prefix. This verifies the presently cached 2.40.0 member only; it is not the historical analysis output.
   - The 2.34.1 package is not present at `/var/cache/pacman/pkg/1password-cli-2.34.1-1-x86_64.pkg.tar.zst`. The round-4 scratch directory `/tmp/rea-r4` is also absent. A round-4 verifier later recorded that the 2.34.1 cache member had been evicted; the corpus entry remains the available historical account. The full 2.34.1 digest and binary cannot be rechecked here.

2. **Historical analysis counts and search results — recorded, not rerun.** The round-4 run log reports 33,060 procedures, 76,550 strings, and 18 segments for 2.34.1; for 2.40.0 it reports 11,595 procedures, 76,338 strings, and 16 segments. Its procedure search reports one `main.main` hit on the older binary and zero on the newer one. The entry's interpretation says about 32,933 old procedures carried namespaced Go names; on the new binary, 11,588 of 11,595 procedure names were `FUN_*`/`thunk_FUN_*` auto-names and `entry` was the sole real name. These figures are copied from the surviving round-4 report, not independently recomputed from its raw JSON.

3. **Function correspondence — recorded consequence.** The historical entry pairs the ELF-entry role at `0x485f40` (`_rt0_amd64_linux`) with the role at `0x491f20` (`entry`). It records `function_match.status=mismatched`, while the explicit dossier comparison still reports a behavioral diff across the functions. The entry recommends pairing by ELF role/address or explicit dossier IDs rather than recovered symbol names. This is evidence for a pairing hazard on this pair, not proof that those matching methods are universally sufficient.

4. **Current source-only version/bootstrap facts.** I hashed the installed Ghidra Base source archive at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`; SHA-256 is `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, matching the digest recorded for S003. In `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`, the `SUPPORTED_VERSIONS` constant is `GoVerRange.parse("1.15-1.25")` (line 79). In `getGoBinary`, an out-of-range `goVer` causes `Msg.error(..., "Untested Go version ...")`, after which control continues to `GoApiSnapshot.get(...)`; that condition is not itself a hard-return gate. In `GoApiSnapshot.java:get`, no available snapshot byte provider leads to `GoApiSnapshot.EMPTY`. This says what the pinned source does; I did not inventory installed snapshot files or exercise the analyzer.

5. **Historical log caveat.** The old report attributes the new-binary collapse to inability to parse Go 1.26 `moduledata`/`pclntab`, and says it saw `Missing Go bootstrap type info, unable to extract Go RTTI info` in `ghidra.log`. It explicitly marks that observation as transient and “observed-not-cited”; the session directory had been deleted. The same old entry names `s234-all.json` and `s240-all.json` under `/tmp/rea-r4`, which is now absent. Thus neither the raw inventories nor the log line are independently available in this inspection.

## Reconstructed contract, divergence, and confidence

- **Last-known-good (historical pair only):** the round-4 record says Ghidra 12.1.4 returned 33,060 procedures, including about 32,933 namespaced Go names, for `op` 2.34.1-1 / Go 1.25.7.
- **Divergence (historical pair only):** the same record says `op` 2.40.0-2 / Go 1.26.8 returned 11,595 procedures, of which 11,588 were auto-named, with `entry` its sole real name; `main.main` was absent. This is the last-known-good comparison available in the corpus, not a current host guarantee.
- **Source-level contract:** the pinned installed source marks 1.26 outside its 1.15–1.25 `SUPPORTED_VERSIONS`, logs “Untested Go version,” and proceeds to snapshot lookup. If no matching snapshot file is available, `GoApiSnapshot.get` returns `EMPTY`; `getSharedGoBinary` then initializes the mapper and catches/logs a `BootstrapInfoException`. This defines a plausible failure path, not proof that it explains the old result.
- **Confidence:** high that the corpus makes the stated historical claims and the checked source archive contains the described version/snapshot behavior; moderate that the old run happened exactly as transcribed because its raw JSON/logs and the 2.34.1 executable are no longer available here; low for any specific causal attribution among unsupported-version handling, snapshot/bootstrap availability, parser/layout incompatibility, or other version-pair differences.

## Causal boundary and unknown links

- **Observed in the historical record:** a paired product upgrade also changed Go toolchain versions, and the reported Ghidra name inventory shrank sharply on the newer member. The loss of names and the mismatched symbol identity are the direct reported observations.
- **Source-only in round 14:** Go 1.26 is outside the inspected Ghidra source's declared 1.15–1.25 supported range; the source logs that condition and continues, with snapshot/bootstrap behavior on the same path. This supports a version-compatibility diagnosis as a candidate, not a demonstrated root cause.
- **Not established:** that the unsupported-version diagnostic caused the collapse; that no Go 1.26 snapshot was installed; that a specific changed `moduledata`/`pclntab` layout was the failing parse; that the transient bootstrap message was captured exactly as transcribed; or that the Go compiler change alone caused the result. The product binaries also differ by package release and application contents. No controlled same-source Go 1.25/1.26 builds, retained raw analysis inventories, retained Ghidra log, or round-14 target run are available here to separate these links.
- **No uplift to held capability:** the round-13 non-author review explicitly limits the source-curation finding: “Source text establishes study provenance, not a held REA operation.” The current source read therefore does not upgrade the historical run to a round-14 held/reproduced operation.

## Sources opened (2026-10-20)

Quotes below are contiguous excerpts of no more than 25 whitespace-delimited words. Local corpus/report sources are historical records; their quoted text does not substitute for absent raw artifacts.

| Source and exact location | Quote | Limitation |
|---|---|---|
| `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:17-22` | “41,210,040 → 43,475,106 \| `d24dc5d4…` → `8d029d2c…`” | Historical report pins sizes and digest prefixes, not full hashes. |
| Same file `:24-43` | “33,060 procs / 76,550 strings / 18 segs” | Run-log transcription; raw evidence was held in `/tmp/rea-r4`, not available now. |
| Same file `:64-78` | “11,588 of them `FUN_*`/`thunk_FUN_*` auto-names” | Historical classification; no surviving inventory to recount. |
| Same file `:71-73` | “Missing Go bootstrap type info, unable to extract Go RTTI info” | Report says transient `ghidra.log` message, observed but not cited; session directory deleted. |
| Same file `:100-118` | “`s234-all.json` / `s240-all.json` inventories in `/tmp/rea-r4`” | Names the vanished raw inventories and the historical claim's source basis. |
| `.ufo/waves/arc3-loop1-round4/claims/c2/EX-15/adjudications.md:315-328` | “the 2.34.1 member has since been evicted by cache churn” | Later verifier corroboration of cache loss, not a retained artifact digest. |
| `corpus/SOURCES.md:9-12` and pinned local archive `Base-src.zip` (SHA-256 above), `GoRttiMapper.java:79` | “`SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`” | Source describes installed Ghidra code, not a run against either `op` target. `getGoBinary` and `GoApiSnapshot.get` were read directly from this pinned archive; their excerpts are described above. |
| `corpus/lessons/round-13-verifier-spotcheck.md:8-17` | “Source text establishes study provenance, not a held REA operation.” | Governing calibration boundary; not evidence for the historical binary result. |
| Binary member currently in `/var/cache/pacman/pkg/1password-cli-2.40.0-2-x86_64.pkg.tar.zst`, member `usr/bin/op` | *Binary artifact; quote not applicable.* SHA-256: `8d029d2cd7112177132b1b20ef0b6012ba9a9dd9ef48d7f7660f2e8071d4f7b2`. | Present-day read/hash only; confirms the current 2.40.0 member matches the recorded prefix, not the historical REA run. |

**LSP availability:** `xd://lsp` is not mounted in this session (`No such tool`). The source archive was read directly; literal searches were used only to locate corpus mentions, not as semantic proof. No Go definitions or call sites are claimed from grep output.