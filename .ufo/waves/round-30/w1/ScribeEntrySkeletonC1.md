# R30-C1 knowledge-entry skeleton — scoped findings

## Result and artifact

**Observation:** Drafted the requested no-results skeleton in the assigned scratch directory; the lane's knowledge entry itself was not written. It has the requested `source: S089 S091` and C1 recheck header, Claim, 16-row Carriers table, Method with frozen P1 verbatim, pending Results table, frozen Limits, and the two earlier-entry pointers.

- Scratch draft: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC1/2026-10-23-r30-rust-auditable-positive.md`
- SHA-256: `8d7081cb0835ea4c33d11b131e32c8f55fef59369d62643d51936c3711de3f2a`
- Hash command: `timeout 30 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC1/2026-10-23-r30-rust-auditable-positive.md`
- Exact output: `8d7081cb0835ea4c33d11b131e32c8f55fef59369d62643d51936c3711de3f2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeEntrySkeletonC1/2026-10-23-r30-rust-auditable-positive.md`
- UTC sample: `2026-10-23T02:45:30Z`, from `timeout 30 date -u +%Y-%m-%dT%H:%M:%SZ`, run in the same final capture batch. The shell tool returned the digest and timestamp but did not surface numeric exit statuses.

The first edit attempt against the external scratch path was rejected with `File not found`; it made no change. The file was then written with `functions.write` (successful response: `Successfully wrote 6735 bytes ...`) and the final scratch version was written again to make referenced filesystem paths absolute (successful response: `Successfully wrote 6735 bytes ...`). The final digest above is for that latter version.

## Evidence and findings

1. **Observation — frozen claim and method inputs.** Producer: `functions.read` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json` (successful content response; read tool has no process exit code). The output excerpt was `"predicate_label": "P1-pass"`, `"target": "carriers=16 pass=16 target=16 entry_ok=1 province_ok=1, exit 0"`, and `"limits": "uv and uvx of one wheel carry the same dependency document; the 16 carriers hold 5 distinct package lists (573-596 packages). The oracle shares the format spec (S089) with REA, not code. One REA pin (6.5.0), one host (Linux)."` The full P1 sentence in the draft was copied from claim R30-C1. **UTC:** read batch completed by the following observed clock sample, `2026-10-23T02:43:43Z` (`timeout 30 date -u +%Y-%m-%dT%H:%M:%SZ`). Individual read timestamps and process exit codes are not exposed by the read tool.

2. **Observation — frozen carrier inputs.** Producer: `functions.read` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv` (successful response; no process exit code exposed). The output contains header `id format arch wheel wheel_sha256 member sha256 size path` and 16 member rows. Excerpt: `elf-x86_64-uv ... 3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0 39714040`; the last row is `macho-arm64-uvx ... 360f023f4f5354b35e5240d081b7c40fc6b489692e7b178cad697380d753223b 334512`. The draft table uses their first 12 digest characters and exact sizes. **UTC:** same read batch, captured by `2026-10-23T02:43:43Z`; individual call time/status not exposed.

3. **Observation — shape and prior-entry pointers.** Producers: `functions.read` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md`, and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md` (all returned file contents; no process exit code exposed). Excerpts include R29 lines `source: S088 ...`, `verified-at: ...`, `recheck: ...`; the 2026-10-16 entry says `auditable_metadata null`; the 2026-10-19 entry describes the separate 6.7.0 Evidence-ID study and also records null `auditable_metadata` for its measured Rust input. The draft explicitly calls this positive-class entry complementary, not a replacement. **UTC:** same read batch, captured by `2026-10-23T02:43:43Z`; individual call time/status not exposed.

4. **Observation — path resolution and source-ID limit.** The draft's local path pointers to the C1 claim, counter, oracle, manifest, `PROVINCE.md`, and the two previous knowledge entries resolve in the lane snapshot: the claim, counter, manifest and prior entries were read; the oracle path appears in the successful lane search result; `PROVINCE.md` appears in the lane-root directory listing. The draft uses absolute paths for these. However, `functions.grep` with pattern `S089|S091` against `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` returned exactly `No matches found` (the read/search tool does not expose a process exit code). Thus **the requested source identifiers S089 and S091 are not resolvable as registry rows in the current lane snapshot**; the draft retains the requested header, but those source rows need to be present when L1 integrates it. An earlier search at the incorrect root path `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SOURCES.md` returned `Path not found`; the correct index is `corpus/SOURCES.md`. **UTC:** searches were in the read batch captured by `2026-10-23T02:43:43Z`.

5. **Observation — source package pointer.** `functions.read` on `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/pypi-uv-0.13.0.json?q=.info.version` returned exactly `"0.13.0"`; the file pointer resolves. No external source was opened.

## Gates and limits

- **Observation:** No REA call, C1 counter run, build, test, or source-registry update was performed. The counter command appears only as the recheck instruction; its target string above is frozen contract data, not an observed run result. No carrier or mutant was executed.
- **Inference:** The draft is ready for L1 to populate once the post-freeze C1 run records and source rows are integrated; this artifact establishes no P1 pass and no measured C1 result.
- **Unknown / pending:** Source registry rows S089 and S091 are absent in the checked lane snapshot, as noted above. No result values or evidence IDs exist in this draft.
- **Installations:** None.
- **Touched surfaces:** One scratch draft listed above and this scoped report. No lane product files, evidence, source index, Git/JJ state, or shared inputs were modified.
- **Out of scope:** data collection, P1 judgment, results population, PROVINCE changes, C2, and integration/commit.

Report: .ufo/waves/round-30/w1/ScribeEntrySkeletonC1.md
