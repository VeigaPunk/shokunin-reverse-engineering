<!--
Proposed SKILL placement: after the blank line at SKILL.md:318, immediately
before "## Config custody for live-probe rounds (SOP)" (line 319). This is
outside the craft split: it keeps every craft rule block, the SHONEN.md:6
range (SKILL.md:81-255 per that line; craft ends at :314), and the four
line-pinned citation-drift entries (SKILL.md:246, :248, :252, :254) on their
current lines. Draft only — L1 owns integration. Source-diagnosis rules; no
capability claim. Anchors are pinned to Ghidra 12.1.4 installed bytes / exact
commits. Line numbers are release-bound; the archive SHA-256 + member + line
is the stable citation.
-->

## Go symbol-recovery source diagnosis (installed 12.1.4)

Use when a Go image recovers only `FUN_*`/`thunk_FUN_*` names (often just
`entry`) while a sibling build recovers `namespace::pkg.name`. The rows are
separate conditions, not a chain: an out-of-range version is logged and
processing continues; the hard stop needs an unavailable snapshot and a failing
struct mapping. Nothing here proves the cause of a past collapse or applies to
Go operations that never build the RTTI mapper.

| # | Ask | Installed-source anchor (Base-src.zip SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`) | Reading |
|---|---|---|---|
| 1 | What Go version does the target declare? | Embedded build metadata. Existing carrier observation: `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:13` reports `go1.26.5-X:nodwarf5` for one linux/amd64 carrier. | The version string keys rows 2–3; it does not decide the outcome alone. That probe is one carrier; metadata never proves name recovery. |
| 2 | Is the version inside the declared range? | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` declares `GoVerRange.parse("1.15-1.25")`; `:170-172` emits `Msg.error(... "Untested Go version [%s]")` when outside. | A 1.26.x target misses the range, but the source logs and continues to snapshot lookup; a range miss alone is not a rejection. |
| 3 | Is a bootstrap snapshot shipped for it? | `GoApiSnapshot.java:102-115` returns `GoApiSnapshot.EMPTY` when no base JSON or patch diff resolves; resolution is `:118-146` and `:168-178` (`typeinfo/golang/go%s.json`); `EMPTY` carries `GoVer.INVALID` (`:242`). | Installed inventory: `go1.15.0.json` … `go1.25.0.json` (11 files); `patchverdiffs/` stops at `go1.24.6.json.diff`. On this inventory a 1.26 target resolves to `EMPTY` (source-derived, not run). |
| 4 | What does `EMPTY` cause? | `GoRttiMapper.java:351-361`: if struct registration fails while `apiSnapshot.isInvalid()`, the source throws `BootstrapInfoException` with `"Missing Go bootstrap type info, unable to extract Go RTTI info."`; `:114-125` catches that and returns null; `GolangSymbolAnalyzer.java:133-137` returns false when the mapper is null. | Source-declared abort path for the Go symbol analyzer, conditional on the failing mapping. It is not a general Go rejection and says nothing about a past collapse. |
| 5 | Range and snapshot both pass, names still absent? | Rows 2–4 pass. | This table does not explain it; record an unknown. Do not generalize the range log to all Go operations. |
| 6 | Is the upstream fix just a range bump + JSON? | S004 GP-6528 (`385e8cd923d09f10b1a7874108e71748875fa174`) also changes `GoPcHeader.java` (`textStart` becomes `presentWhen = "1.18-1.25"`), `GoModuledata.java` (finds `go.module` before the symbol), `GoMapType.java` (`presentWhen = "1.26-"`), and `GoTypeFlag.java`. | The upstream diff indicates 1.26 crosses pclntab, moduledata, and type-field boundaries too. Installed 12.1.4 has none of the commit: GP-6528 is release-boundary/roadmap evidence, never a held parser. |
| 7 | Names recovered on both sides, but cross-version pairing fails? | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:100-118`: zero shared names across go1.25.7→go1.26.8; the same ELF entry compares `mismatched`. | Pair by ELF role/address or explicit dossier ids, never by name; re-run the explicit pair before calling a diff real. |
| 8 | Need name-free matching? | S006 `docs/GhidraClass/BSim/BSimTutorial_Intro.md:15-22`: features omit constant values, register names, and data types; vectors compare by cosine similarity. | A study route whose output is close-but-not-identical by design; similarity is not equivalence proof, and no BSim run is claimed. |
| 9 | Cross-check with another parser? | S005 pinned README `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`: `Version Support` lists pclntab layout formats pre 1.2, 1.2, 1.16, 1.18, and 1.20; `Changes` adds parsing support for Go 1.24 binaries; `-v` requires an accurate version or type parsing fails. | Layout-format max is not a runtime ceiling: the same README records Go 1.24 parsing. Go 1.26 remains unstated, so neither support nor a 1.20 ceiling follows. |

**Do not:** edit the installed release or its environment to widen the declared
range (operator-owned install decision); read `FUN_*` names as proof the target
was stripped; blame a named historical collapse on this path without its own
evidence; or cite S004/S005 as this host's Go 1.26 capability. **Recheck:**
archive SHA-256 plus member/line; line numbers are 12.1.4-only.

**Anchors.** S003 — `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`,
SHA-256 `f00d29c2…`; members `ghidra/app/util/bin/format/golang/rtti/{GoRttiMapper,GoApiSnapshot}.java`
and `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java`.
S004 — Ghidra commit `385e8cd923d09f10b1a7874108e71748875fa174` (GP-6528), patch diff.
S005 — Mandiant GoReSym README at commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`, `Version Support` / `Changes` / `Usage`.
S006 — `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md:15-22`.
