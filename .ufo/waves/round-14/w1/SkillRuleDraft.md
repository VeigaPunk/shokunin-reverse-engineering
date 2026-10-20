# SkillRuleDraft — Go symbol-recovery source-diagnosis SKILL addendum (round 14, w1)

Seat: `KaidokuR14.SkillRuleDraft` (leaf executor, source-only; no subagent dispatch).
Worktree: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Baseline: `767adaf` (`git rev-parse --short HEAD`, 2026-10-20). At first check `git status --short` showed only untracked `.ufo/waves/round-14/`; at final check `corpus/QUALITY.md` showed `M` with 1 insertion (mtime 2026-10-20 02:23:33 -0300), a concurrent sibling write this seat did not make or edit.
Access date for every source below: 2026-10-20 (UTC).
Tooling: no package installed or upgraded; existing `unzip`, `sha256sum`, `nl`, `curl`, Python 3 used as-is.

## Axes and contribution

- **Coverage** — adds one actionable SKILL decision table for a symptom the current SKILL does not address: Go names collapsing to `FUN_*`/`thunk_FUN_*` while a sibling build keeps `namespace::pkg.name`. The SKILL was read first; it has no Go rule (§ `Decision table (this host, r3-verified)`, § `Error patterns`, § `Queue-drain craft`).
- **Calibration** — separates two conditions the registry's anchor text conflates: the declared-range check only logs and continues; the hard stop is a missing API snapshot plus a failing struct mapping. It also corrects the reading of S005's `1.20` layout list as a runtime ceiling: the same pinned README records Go 1.24 parsing support.

No axis score is claimed here; C1/C2 own the measured observables.

## Inputs inspected before drafting

- `SKILL.md` — `## Decision table (this host, r3-verified)`, `## Error patterns (typed refusals)`, `## Queue-drain craft (rounds 5-12, distilled in round 13)`, `## Known limits (r4)`, `## Local round-evidence gate registry`. No Go-version rule exists in the current SKILL.
- `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` — historical Go collapse, especially `:64-73` (collapse observation) and `:100-118` (pair-by-role candidate). Cited only for the pairing rule, not as proof of causation.
- `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md` — existing carrier observation of embedded build metadata, `:13`. Its own limitation line says metadata does not recover functions, source mappings, types, or decompilation.
- Parent steer (2026-10-20): S003 `GoRttiMapper` emits an unsupported-version message (`Msg.error`) and continues; a missing snapshot yields `EMPTY`; the rule must not blame the historical collapse or all REA Go operations; GoReSym's `Changes` explicitly claims Go 1.24 parsing while its layout list stops at 1.20. These points were re-verified against the pinned bytes below.
- `KaidokuR14.AttackNoHarm` message (2026-10-20): placement above `## Queue-drain craft` would shift the four `skill-rule14-*` line-pinned entries at `SKILL.md:246/248/252/254` and, at ≥23 inserted lines, push rule #13 at `SKILL.md:233` past `SHONEN.md:6`'s range. Verified directly against `.ufo/gates/citation-drift/pointer-table.json` and `SKILL.md`; its named report file was not present at read time. Placement changed to after `SKILL.md:318`.
- `corpus/lessons/round-13.md` and `corpus/lessons/round-13-verifier-spotcheck.md` — quote-splice and quote-location failure classes that govern how this report quotes.

## Sources opened this round (exact, contiguous, ≤25 words)

| id | source opened (absolute path or pinned URL) | location | exact contiguous quote | words |
|---|---|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` — SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (matches registry) | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | 7 |
| S003 | same archive/member | `GoRttiMapper.java:171` | `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));` | 5 |
| S003 | same archive, `.../rtti/GoApiSnapshot.java` | `:115` | `return GoApiSnapshot.EMPTY;` | 2 |
| S003 | same archive/member | `:242` | `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());` | 9 |
| S003 | same archive, `.../rtti/GoRttiMapper.java` | `:359` | `"Missing Go bootstrap type info, unable to extract Go RTTI info."` | 11 |
| S003 | same archive, `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` | `:135` | `Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");` | 9 |
| S004 | `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch` — fetched snapshot SHA-256 `f44945bc879d46f2e16624f7823246416d625229e57930db13a040862c170538` | patch line 4 | `Subject: [PATCH] GP-6528 add support for golang 1.26` | 8 |
| S004 | same fetched patch | patch line 151 | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");` | 7 |
| S004 | same fetched patch | patch line 18 | `create mode 100644 Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json` | 5 |
| S005 | `https://raw.githubusercontent.com/mandiant/GoReSym/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d/README.md` — fetched snapshot SHA-256 `d44dd94d5a74577fd86fdb70cb87a3f8a683aa6f2088bb30aba722e469bd6094` | `Version Support`, line 95 | ``This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.`` | 14 |
| S005 | same pinned README | `Changes`, line 118 | `Added parsing support for Go 1.24 binaries while retaining compatibility with older 1.2 layouts.` | 14 |
| S005 | same pinned README | `Usage`, line 79 | `Type parsing will fail if the version is not accurate.` | 10 |
| S006 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md` — SHA-256 `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`, 88 lines | line 19 | `Certain attributes, such as values of constants, names of registers, and data types, are intentionally not incorporated into the features.` | 20 |
| S006 | same file | line 21 | `BSim vectors are compared using *cosine similarity*.` | 7 |
| corpus | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` | line 70 | ``FUN_*`/`thunk_FUN_*` auto-names; the sole real name is `entry`.` | 8 |
| corpus | `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md` | line 13 | ``go1.26.5-X:nodwarf5`, module `github.com/docker/cli/cmd/docker`` | 3 |

Every S003 quote was extracted with Python `zipfile` from the hash-verified archive member and asserted as a substring of the cited line. S004/S005 line numbers are those of the fetched snapshots identified by the digests above; the commit/tag pins are the durable locator, not the download digest.

## Candidate and behavior

Candidate: `.ufo/waves/round-14/w1/SkillRuleDraft.candidate.md` (5,821 bytes / 45 lines after the placement-comment and calibration revisions; SHA-256 `24607b140cafdcda1a64001a98b4564c862ec573592b2b5ef42bc342795abc0d`; 9-row decision table plus anchors footer). Proposed placement is stated in its HTML comment: after the blank line at `SKILL.md:318`, immediately before `## Config custody for live-probe rounds (SOP)` at `:319` — not above the craft section.

The table's behavior:

1. Version from embedded metadata keys the diagnosis; the l7-01 carrier is scoped as one observation.
2. Declared range `1.15-1.25` is checked, but an outside version is **logged and processing continues** (`GoRttiMapper.java:170-172`); it is not a rejection.
3. Snapshot resolution is checked next: `GoApiSnapshot.get` returns `EMPTY` when no base JSON or patch diff resolves (`:102-115`); installed inventory is `go1.15.0.json` … `go1.25.0.json` (11 files), and `patchverdiffs/` ends at `go1.24.6.json.diff`.
4. `EMPTY` + a failing `registerStructures` takes the `BootstrapInfoException` path (`:351-361`); `getSharedGoBinary` catches it and returns null (`:114-125`); `GolangSymbolAnalyzer` returns false on the null mapper (`:133-137`). The table labels this a conditional, source-declared abort path — not a general Go rejection and not proof of a past collapse.
5. In-range + snapshot-present + still-absent is explicitly an unknown this table does not explain.
6. GP-6528 is more than a range bump: it also changes `GoPcHeader`, `GoModuledata`, `GoMapType`, and `GoTypeFlag`; installed 12.1.4 has none of it.
7. Cross-version pairing uses ELF role/address or explicit dossier ids (r4-10), not names.
8. BSim is name-free by design but similarity is not equivalence; no run claimed.
9. GoReSym's `Version Support` layout list is a layout-format list, not a runtime ceiling; the same README's `Changes` records Go 1.24 parsing, while Go 1.26 remains unstated.

## Findings and calibration notes

- **F1 (high, corrects the registry shorthand).** `SUPPORTED_VERSIONS` at `:79` is consulted at `:170`; the miss branch at `:171` is `Msg.error` and does not throw. The code proceeds to `GoApiSnapshot.get` at `:176`. A rule that says the version gate rejects 1.26 contradicts the source.
- **F2 (high).** The hard path is data-dependent: no `go1.26.0.json` in the installed `data/typeinfo/golang/` tree; `GoApiSnapshot.get` returns `EMPTY` (`:115`, `EMPTY` = `GoVer.INVALID` at `:242`); only when `registerStructures` throws does `initStructMappings` convert that to `BootstrapInfoException` (`:351-361`). The analyzer's null check then returns false (`GolangSymbolAnalyzer.java:133-137`). This is a source-declared path, not a measured run.
- **F3 (high).** S005 is internally broader than its layout list: `Version Support` lists layouts through 1.20, while `Changes` says "Added parsing support for Go 1.24 binaries." The candidate cites both and states that the layout list is not a runtime ceiling. It does not claim Go 1.26 support.
- **F4 (medium).** GP-6528 is not reducible to `SUPPORTED_VERSIONS` + `go1.26.0.json`; the fetched patch also edits `GoPcHeader.java` (`textStart` → `presentWhen = "1.18-1.25"`), `GoModuledata.java` (`go.module` lookup), `GoMapType.java` (`presentWhen = "1.26-"`), and `GoTypeFlag.java`. The installed release has none of these changes.
- **F5 (medium, scope).** The candidate does not blame the r4-10 collapse. It cites that entry only for its measured pairing result; the original entry itself says the Ghidra log directory was deleted, so its log line is observed-not-cited. The addendum's "Do not" line explicitly forbids blaming a named historical collapse without its own evidence.
- **F6 (low, citation hygiene).** `GoApiSnapshot.java:115` is the `return GoApiSnapshot.EMPTY;` line by direct `nl` read; `.ufo/waves/round-14/w1/InstalledGoGate.md` cites 116. The candidate and this report use 115. No shared file was corrected.
- **F7 (low).** The registry row's anchor `GoApiSnapshot.java:get` is a method name, not a line. The candidate cites concrete lines (`102-115`, `118-146`, `168-178`, `242`) and does not edit the row (Rule 2).
- **F8 (high, harm-free placement).** `KaidokuR14.AttackNoHarm`'s 2026-10-20 message reported that inserting the section above `## Queue-drain craft` would shift the four `skill-rule14-*` extracted entries at `SKILL.md:246/248/252/254` and, at ≥23 inserted lines, push rule #13 at `SKILL.md:233` past `SHONEN.md:6`'s `SKILL.md:81-255` range. Direct check: `pointer-table.json` places every `SKILL.md` line pin at 246, 248, 252, or 254 (plus anchor-kind rows with no line); `SKILL.md:314` ends the craft section and `:319` is `## Config custody`; no `SKILL.md` line pin lies after 318. The candidate's placement comment was moved to after `:318` / before `:319`. The peer's named report file `.ufo/waves/round-14/w1/AttackNoHarm.md` was not readable when checked (path not found), so only its message and the directly read pointer table were used.

## What this draft does not claim

- No Go target was analyzed, no REA session was opened, no provider was run, and no Go 1.26 recovery was attempted.
- No claim that the installed parser rejects all Go 1.26 operations, or that the range log alone explains any symbol-loss observation.
- No claim that GoReSym supports or rejects Go 1.26; only that its pinned README does not state it.
- No claim that GP-6528 is present in any released Ghidra other than as an upstream commit; it is not in installed 12.1.4.
- No registry, SKILL, SCORECARD, LOG, corpus, MANIFEST, or sibling-file edit.

## Checks not run (limits)

- No build, lint, test, formatter, smoke run, gate, or `--selftest` was executed. The C2 quote gate was neither run nor used as a manifest; that is L1's post-integration step.
- No REA diagnostics (`rea doctor`, `binary_session`) and no target execution; not needed for source-only work.
- S004/S005 are network fetches pinned by commit/tag; the downloaded bytes were hashed but not GPG-verified. A future fetch of the same commit may differ in transport encoding, though the quoted lines are commit-pinned.
- S003 line numbers bind to archive SHA-256 `f00d29c2…`; a Ghidra upgrade invalidates them. The candidate states this recheck rule.
- The candidate is author-side material. It is not non-author admission of C1, C2, or any capability.

## Files changed

- `.ufo/waves/round-14/w1/SkillRuleDraft.candidate.md` (new)
- `.ufo/waves/round-14/w1/SkillRuleDraft.md` (new, this report)

No other writes by this seat. `corpus/QUALITY.md` gained one insertion from another seat during this run (seen as ` M`, 1 insertion at 02:23:33 -0300); it was not read as authority and was not modified here. No installs to record.

## Handoff to L1

1. If C1's entry `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` lands, consider adding a one-line pointer in the addendum's anchors footer; the candidate deliberately cites only stable source/corpus anchors because that file did not exist when this draft was written.
2. Recheck the S003 lines against archive SHA-256 `f00d29c2…` after integration; do not carry line numbers across a Ghidra upgrade.
3. Insert only after the blank line at `SKILL.md:318`, before `## Config custody` at `:319`; do not place it above the craft section. Keep the logged-message vs missing-snapshot distinction; collapsing it back to a version-gate rejection would reverse the calibration this seat verified.
