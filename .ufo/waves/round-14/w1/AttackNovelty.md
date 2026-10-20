# AttackNovelty — round 14, C1 novelty critique

Seat: `KaidokuR14.AttackNovelty` (critic, leaf, author side; this is not a non-author admission). Opened 2026-10-20.
Axes: coverage and calibration. Scope: report only. I made no corpus, registry, SKILL, LOG, or SCORECARD writes. I ran no REA, no Ghidra, and no target. I installed or upgraded no tools.

## Verdict

**C1 can count as novel only conditionally.** No existing `corpus/knowledge/` entry or README row contains the source-located Ghidra mechanism. That part of the ground is uncovered. However, the *observation*, the *version link*, the *log line*, and the *operator consequence* are already held by r4-10. The *diagnostic heuristic* is already stated in the S003 `teaches` cell. A near-identical entry was already drafted as fleet K1. An entry that restates any of these does not add coverage; it only adds a row (CE1). The claim's own wording, "version-gate", also names the wrong blocking mechanism (CE2). Fixes for both are given below.

## Bounded search performed

- `grep` `(?i)GoRttiMapper|GoApiSnapshot|unsupported.{0,20}version|go1\.2[0-9]|gover|Go version` over `corpus/knowledge` and `README.md`. Result: no `GoRttiMapper`/`GoApiSnapshot` hit in any knowledge entry. The Go hits are r4-10, `2026-10-16-l7-01-inspect-go-binary`, and `2026-10-19-arc3-r12-go-evidence-id-domain`. The l7-01 and arc3-r12 entries cover build-metadata extraction and Evidence-ID identity, not recovery loss. There was one unrelated firmware version-gate hit.
- `grep` `pclntab|moduledata|Go RTTI|bootstrap type|collapse|GoVer|gotypes|1\.26` over `corpus/`, `README.md`, and `SKILL.md`.
- Lane-wide `grep` (gitignore off) for `GoRttiMapper|GoApiSnapshot|GP-6528|bootstrap type info|go1\.26\.0\.json`. Hits were limited to `SCORECARD.md:2111` (plan lead), `corpus/SOURCES.md:9-10,33,50`, `corpus/lessons/round-13.md:30-31`, `r4-10:72`, and round-14 dispatch files.
- Fleet `grep` for the same pattern plus `bootstrap-gap`. This found the prior draft K1 at `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/kaidoku-art.md:200-215`.
- Not searched: other lanes' corpora beyond that fleet grep, git history, and LOG.md.

## Concrete overlap (what already exists)

| Existing | Location | Content already held | Consequence for C1 |
|---|---|---|---|
| r4-10 entry | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:64-81, 100-118` | Measured collapse: 33,060 → 11,595 procedures, 11,588 `FUN_*`. go1.25.7 → go1.26.8 link. Log line “`Missing Go bootstrap type info, unable to extract Go RTTI info`” (:72), flagged “observed-not-cited” (:73). Pair-by-address rule. | Restating the collapse, the version link, or the pairing rule is duplicate. |
| r4-10 mechanism text | `:70-71` | Says Ghidra “cannot parse the Go 1.26 moduledata/pclntab layout”. This is uncited. | **The genuine gap**: an uncited and probably mis-attributed mechanism (CE5). |
| README coverage row | `corpus/README.md:35` | Says the “Go bump (1.25.7→1.26.8) collapses symbol recovery”. | Already mapped, so coverage needs a *distinct question* (CE8). |
| SOURCES S003 `teaches` | `corpus/SOURCES.md:9` | “Inspect the installed parser's declared Go range and missing-snapshot path before attributing recovery loss to a binary layout change.” | The heuristic itself is already registered. An entry that only restates it is padding. |
| SOURCES path | `corpus/SOURCES.md:33` | S003→S004→S005→S006 route; “These sources do not establish a Go 1.26 recovery run…” | The entry must respect this bound. |
| Fleet K1 draft | `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/kaidoku-art.md:200-215` | Same mechanism, same line numbers (`:79`, `:170-171`, `GoApiSnapshot.java:105-115,122-126`, `:351-360`, `:114-125`), same inference. | This is prior art. C1 is a *re-verification and admission* of K1, not a discovery. Provenance must say so. |
| SCORECARD plan | `SCORECARD.md:2174-2175` | “Round 14 may mine one source-backed knowledge entry only if the matching uncovered coverage-map question remains.” | This is the admission precondition. |

## Counterexamples (strongest first)

**CE1: row-count gaming through a self-defined observable.** `claims.json:8-10` measures a 0 → 1 count of a “source-backed Go recovery version-gate diagnostic entry”. Any new file satisfies that, including a paraphrase of `SOURCES.md:9` plus `r4-10:64-81`. Such an entry adds nothing the corpus does not already state. Axes: coverage (inflated) and calibration (overclaim).

**CE2: “version gate” names the wrong mechanism.** In installed `GoRttiMapper.java`, the declared range is advisory. The lookup that blocks recovery is the snapshot for the base minor version. Evidence (S003 `Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, re-hashed 2026-10-20):
- `GoRttiMapper.java:79`: `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`
- `:170-171`: `if (!SUPPORTED_VERSIONS.contains(goVer) ) {` then `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));`. There is no throw and no return, so execution continues to `GoApiSnapshot.get` at `:176`.
- `GoApiSnapshot.java:122-126`: `GoVer baseVer = goVer.withPatch(0);` … `if (jsonFile == null) {` `return null;`. Then `:115`: `return GoApiSnapshot.EMPTY;`.
- Installed `Ghidra/Features/Base/data/typeinfo/golang/` holds `go1.15.0.json` through `go1.25.0.json` (11 files). The `patchverdiffs/` entries matching `^go1\.2[56]\.` number 0.

An entry headlined “unsupported version ⇒ gate rejects” is falsified by `:170-172`. Name the claim as a missing-snapshot bootstrap failure; the range is only a log. Axis: calibration.

**CE3: the log line does not diagnose the version by itself.** `GoRttiMapper.java:356-359` throws “Missing Go bootstrap type info…” only when `registerStructures` throws *and* `apiSnapshot.isInvalid()`. `GoApiSnapshot.java:503-504` defines `isInvalid()` as `arches.isEmpty()`. `read()` (`:216-239`) keeps only the arch names in the search order. So a *present* snapshot that lacks the binary's GOOS/GOARCH entries also yields an invalid snapshot and the same message. The source comment at `:357` says so: “a normal'ish situation where we don't have type info for this arch/binary”. [INFERENCE from source; no such arch case was run.] The diagnostic must therefore pair the message with the binary's Go version and the absence of `go<maj>.<min>.0.json`.

**CE4: “EMPTY ⇒ analysis stops” is conditional and untraced.** The chain is: `EMPTY` → (`registerStructures` throws) → `BootstrapInfoException` → `getSharedGoBinary` returns null (`:114-117,125`) → `GolangSymbolAnalyzer.java:133-136` logs “Go symbol analyzer error: unable to get GoRttiMapper” and returns false. The `registerStructures` failure under `EMPTY` was not traced in this review. The only evidence that it happened for go1.26.8 is r4-10's garbage-collected (GC'd) log line. The entry must label the r4-10 link as INFERENCE, not as a reproduced cause.

**CE5: correcting r4-10 is the real value, but the correction must stay bounded.** The source chain fails at bootstrap, before any pclntab or moduledata parse. That undercuts r4-10:70-71's uncited layout attribution. It does **not** show that the Go 1.26 layout is unchanged. Whether GP-6528 also changed struct mappings is an S004 question owned by another seat. The correct wording is “not evidence of a layout change”, not “no layout change”. r4-10 must remain unedited, per the append-only rule. The new entry should cite r4-10:70-73 as the claim it supersedes in mechanism.

**CE6: the “Fallback Go Version” option is not a route-around.** `GoRttiMapper.java:154-158` uses `GoBuildInfo.fromFallbackInfo` only when `buildInfo == null || buildInfo.getGoVer().isInvalid()`. A go1.26.8 binary with valid build info cannot borrow the go1.25 snapshot through `GolangSymbolAnalyzer`'s `Fallback Go Version` option (`:129-131,1311-1345`). [Source reading only; not run.] The entry must not propose this option as a workaround.

**CE7: the source list is padded, and S007 is missing.** `claims.json:12-17` lists S003–S006.
- S006 (BSim) and S005 (GoReSym, whose README covers layouts “pre 1.2, 1.2, 1.16, 1.18, and 1.20”, per `round-13.md:32`) do not bear on *diagnosis*. They are route-around study leads.
- The installed release history *is* diagnostic. `docs/ChangeHistory.md` (SHA-256 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`), section `# Ghidra 12.0 Change History (December 2025)` › `### Improvements`, line 585: “Added support for Golang 1.24 and 1.25. Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.” `grep -c GP-6528` on the same file → 0.
- Fix: cite S003 (+S007) as diagnosis evidence and S004 as upstream state, and keep S005/S006 under a labeled route-around lead. Otherwise the four-source count overstates support.

**CE8: this may be depth relabeled as coverage.** The README coverage map (`:33,35`) marks cross-version diff and the Go collapse as held. No README row or Frontier bullet (`:170-181`) names an uncovered Go-mechanism question. The uncovered question currently exists only as r4-10's “observed-not-cited” (:73) and the fleet ART table row (`kaika-w1/kaidoku-art.md:49`). To satisfy `SCORECARD.md:2174-2175`, the entry must state the question explicitly and cite those two locations. One possible wording: *“Which installed-Ghidra code path suppresses Go symbol recovery for go1.26.x, and how is it distinguished from a layout change?”* L1 must add the matching coverage-map row only after the file exists (`README.md:9`).

**CE9: artifact identity (QUALITY #4) is reachable but not yet in the corpus.** r4-10 records only truncated hashes (`8d029d2c…`, `d24dc5d4…`). The lane has no full-hash match. I recomputed one without executing the target: `/var/cache/pacman/pkg/1password-cli-2.40.0-2-x86_64.pkg.tar.zst` (package SHA-256 `fb3e38a7d2eaa7444c2aa0ccd56ae45444c07728c623c984939faf92bcf8d850`) → `tar -xOf … usr/bin/op | sha256sum` = `8d029d2cd7112177132b1b20ef0b6012ba9a9dd9ef48d7f7660f2e8071d4f7b2`. This matches r4-10's prefix. `grep -aoE 'go1\.2[0-9]\.[0-9]+' | sort | uniq -c` gives `2 go1.26.8`. The 2.34.1 package is no longer cached (only 2.40.0 and 2.41.0 are present), so the go1.25.7 counterpart cannot be re-hashed. If the entry links to the carrier, it should use this full SHA and say the 2.34.1 side is r4-10-recorded only.

## Smallest safe correction: requirements for exactly one valid entry

1. **Headline the mechanism, not a version gate.** The declared range `1.15-1.25` is log-only (`:170-172`). Recovery depends on `go<maj>.<min>.0.json` existing (`GoApiSnapshot.java:122-126,115`). Both are labeled OBSERVATION (source text).
2. **State the new diagnostic test, which does not exist in the corpus.** Three conditions are needed together, and the bootstrap message alone is insufficient (CE3):
   - the binary's Go version (embedded string or `inspect_go_binary`);
   - presence of `typeinfo/golang/go<maj>.<min>.0.json`;
   - the bootstrap message.
3. **Label the r4-10 link as INFERENCE.** Cite `r4-10:70-73` as the uncited mechanism this supersedes. Do not edit r4-10. State UNKNOWN for whether the go1.26 layout changed (CE5) and for whether `registerStructures` fails under `EMPTY` (CE4).
4. **Credit prior art.** Cite `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/kaidoku-art.md:200-215` (K1) as the draft origin. C1's contribution is the round-14 re-verification plus the corrections in CE2, CE3, and CE6.
5. **Fix the sources.** S003 and S007 support the diagnosis, and S004 gives upstream state. S005/S006 go only under a labeled route-around lead, or are dropped from C1's evidence list (CE7).
6. **Satisfy QUALITY.**
   - #4: `Base-src.zip` path plus SHA, and the op 2.40.0 full SHA if the carrier is named.
   - #7: not examined: no Ghidra/REA rerun, `registerStructures` internals, the patch-diff branch, other arches, the master build.
   - #8: pin Ghidra 12.1.4 and the r4-10 `rea-agents@6.4.0` provider context.
   - #5: observation/inference/unknown labels on every conclusion.
7. **Make the coverage question explicit (CE8).** The entry names the uncovered question. L1 adds one README coverage row after the file exists, plus at most one Frontier pointer (“Go ≥1.26 recovery waits on a Ghidra release carrying GP-6528; operator-owned upgrade”). If L1 cannot name a question distinct from `README.md:35`, C1 is a depth claim and should be filed as depth, not coverage.
8. **Make no REA/target capability claim.** No “Ghidra cannot analyze Go 1.26 binaries” in general, and no “GoReSym/BSim recovers it”. That is consistent with `SOURCES.md:33` and the round goal.

## Not a defect (tradeoffs)

- A source-only entry that explains an earlier live observation is legitimate coverage *if* CE8 holds. Rejecting it because it adds no new run would make mechanism gaps unfillable without target execution, and the round forbids target execution.
- Restating the S003 `teaches` heuristic inside the entry is acceptable as context. It cannot be the claim.

## Sources opened (2026-10-20)

| Source | Location | Quote (≤25 words, contiguous) |
|---|---|---|
| S003 `Base-src.zip` (SHA-256 above) | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` |
| same | `GoRttiMapper.java:171` | `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));` |
| same | `GoRttiMapper.java:357` | `// a normal'ish situation where we don't have type info for this arch/binary` |
| same | `GoApiSnapshot.java:97-98` (javadoc) | “possibly an {@link #EMPTY} instance if no matching snapshot file is found” |
| same | `GoApiSnapshot.java:122` | `GoVer baseVer = goVer.withPatch(0);` |
| same | `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:135` | `Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");` |
| S007 `docs/ChangeHistory.md` (SHA-256 above) | `# Ghidra 12.0 Change History (December 2025)` › `### Improvements`, line 585 | “Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.” |
| lane corpus | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:70-71` | “Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout” |
| lane registry | `corpus/SOURCES.md:9` (`teaches`) | “Inspect the installed parser's declared Go range and missing-snapshot path before attributing recovery loss to a binary layout change.” |
| lane scorecard | `SCORECARD.md:2174-2175` | “Round 14 may mine one source-backed knowledge entry only if the matching uncovered coverage-map question remains.” |

Limitations:
- S004, S005, and S006 were not reopened. Other seats own them.
- `registerStructures` and the struct-mapped classes were not traced.
- Source text establishes declared and implemented code paths in the installed 12.1.4 archive. It does not establish held REA behavior or what happened in r4-10's session.
- Line numbers come from `unzip -p … | cat -n` on the pinned archive.

## Commands run (reads, hashes, and counts only)

- `sha256sum …/Base-src.zip` → `f00d29c2…a8d804`
- `unzip -l` and `unzip -p … | cat -n | sed -n` on the members above
- `ls …/typeinfo/golang/` → 11 `go1.*.0.json` files, `golang_1.15`–`1.23` `.gdt` files, and `patchverdiffs`
- `ls …/patchverdiffs | grep -cE '^go1\.2[56]\.'` → 0
- `grep -c GP-6528 …/ChangeHistory.md` → 0
- `sha256sum` on the cached 1password-cli package, plus `tar -xOf … usr/bin/op | sha256sum` and `grep -aoE … | sort | uniq -c` (stream only; nothing extracted to disk, target not executed)
