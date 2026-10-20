# RegistryDeltaDraft — reopened S003/S004 and bounded C1 registry delta (round 14, wave 1)

Seat: `KaidokuR14.RegistryDeltaDraft` (executor). Access date for every reopened item below: **2026-10-20**.
Scope: source re-open plus a proposed `used-by` delta; `corpus/SOURCES.md` was read and **not modified**.

## Result

Produced `.ufo/waves/round-14/w1/RegistryDeltaDraft.candidate.md`: four `used-by` cell appends
(**S001, S003, S004, S007**, the final C1 candidate's actual citation set), each appending
`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` after the existing `corpus/lessons/round-13.md`;
no status or recheck change; a separately guarded, non-frozen optional round-14-lesson append.
**S005 and S006 receive no append**: the final entry cites neither (correction F5). Application is
conditional on the C1 entry existing at the claims-bound path and citing each id (census check E11), and
the `claims.json` source list (`S003`–`S006`) does not match the final entry's (`S001`/`S003`/`S004`/`S007`)
— L1 must reconcile that, not this seat (F6).

## Sources reopened

### S003 — installed Ghidra 12.1.4 Base source archive

Path: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
SHA-256 recomputed: `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (matches the registry).
Members extracted read-only to `/tmp/r14reg`; original archive untouched.

| location | contiguous quote (≤25 words) | limitation |
|---|---|---|
| `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | Declared range only; not a runtime result. |
| `…/GoRttiMapper.java:171` | `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));` | Error log, not a throw/return; see finding F2. |
| `…/GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` | Missing-snapshot path, distinct from the version check. |

### S004 — GP-6528 upstream commit

URL: `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174`
Reopened through the GitHub REST commit endpoint (JSON metadata + `application/vnd.github.diff`).
Resolved SHA: `385e8cd923d09f10b1a7874108e71748875fa174`; author date `2026-03-03T19:52:38Z`.

| location | contiguous quote (≤25 words) | limitation |
|---|---|---|
| commit message (whole message) | `GP-6528 add support for golang 1.26` | Title only; no release claim. |
| `GoRttiMapper.java` hunk `@@ -76,7 +76,7 @@` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");` | Added side of the diff. |
| `certification.manifest` hunk `@@ -102,6 +102,7 @@` | `data/typeinfo/golang/go1.26.0.json||GHIDRA||||END|` | Manifest registration of the new snapshot. |

Changed-file list confirms a new `Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json` and a one-line
change in `GoRttiMapper.java`. The commit precedes installed 12.1.4; no attribution to the installed
release is made.

### S001 — installed REA skill (cited by the final entry)

Path: `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md`
SHA-256 recomputed: `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0`.

| location | contiguous quote (≤25 words) | limitation |
|---|---|---|
| lines 168–169, bullet `Embedded Go compiler, module or build-setting metadata: inspect_go_binary` | `This built-in target-free inspection requires no Go installation or disassembler.` | Documents the target-free metadata route only; not proof the verb is available on this host. |

### S007 — installed Ghidra 12.1.4 Change History (cited by the final entry)

Path: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md`
SHA-256 recomputed: `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`.

| location | contiguous quote (≤25 words) | limitation |
|---|---|---|
| line 585, under `# Ghidra 12.0 Change History (December 2025)` (line 564) and `### Improvements` (line 582) | `Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.` | Records the 12.0 change (GP-5470), not Go 1.26 support in 12.1.4. |

### S005 — GoReSym pinned README (opened to validate the row before a used-by append)

URL: `https://raw.githubusercontent.com/mandiant/GoReSym/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d/README.md`
Bytes fetched this round, SHA-256 `d44dd94d5a74577fd86fdb70cb87a3f8a683aa6f2088bb30aba722e469bd6094`
(local copy `/tmp/gore_s005_readme.md`, not added to the repository).

| location | contiguous quote (≤25 words) | limitation |
|---|---|---|
| `README.md:95`, `Version Support` | ``This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.`` | Layout coverage, not Go 1.26 support; "current" is the README's own word. |
| `README.md:79`, `-v` entry | `Type parsing will fail if the version is not accurate.` | Self-stated override caveat, not observed behavior. |

### S006 — installed BSim tutorial

Path: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md`
SHA-256 recomputed: `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`.

| location | contiguous quote (≤25 words) | limitation |
|---|---|---|
| line 19, under heading `# How Does BSim Work?` (line 13) | `Certain attributes, such as values of constants, names of registers, and data types, are intentionally not incorporated into the features.` | Documentation of feature construction; not a semantic-equivalence result. |

## Findings

- **F1 — anchors intact.** S003's digest and `GoRttiMapper.java:79` line match the registry exactly;
  `GoApiSnapshot.get` is present at line 102 of member `GoApiSnapshot.java`. S004 resolves to the stated
  commit with the stated title and a `1.15-1.25` → `1.15-1.26` range change in the same file. S005's
  support clause and S006's line 19 still exist as recorded.
- **F2 — calibration flag for C1, not a registry edit.** In the installed 12.1.4 archive, an out-of-range
  Go version does **not** stop the mapper at the inspected call site: `GoRttiMapper.java:170-171` logs
  `Msg.error(…)` inside `if (!SUPPORTED_VERSIONS.contains(goVer))` and control continues to
  `GoApiSnapshot.get(...)` at line 176. A "versions outside 1.15–1.25 stop analysis" statement would not be
  supported by this source; "declared supported range, with an untested-version error logged" is.
  Separately, `GoApiSnapshot.get` returns `GoApiSnapshot.EMPTY` when no matching snapshot file is found
  (`GoApiSnapshot.java:115`), so missing-snapshot and out-of-range are distinct conditions in the source.
  The existing S003 `scope` ("version gate and snapshot bootstrap behavior") remains accurate; only a
  stronger stop-behavior claim would be wrong. This is reported for the entry author/L1, not proposed as a
  row edit (my permitted columns are `used-by`, `recheck`, `status`).
- **F3 — measured no-change for status/recheck.** All six inspected rows (S001, S003, S004, S005, S006,
  S007) stay `mined` / `on-release`; only the four cited rows get a `used-by` append. The new artifact is an
  additional citation, not an admission or rejection event; `opened` also stays `2026-10-19` because it is
  outside my permitted columns and the prior open is genuine.
- **F4 — ordering constraint.** The C1 entry did not exist on disk when this draft was written
  (`corpus/knowledge/` had no `2026-10-20-*` file), so the used-by append cannot be applied yet.
  `sources-census.sh` E11 validates each comma-separated `used-by` path, so applying the path before the
  entry lands would fail validation.

- **F5 — final citation set (supersedes the earlier draft read).** The 02:22 draft of
  `.ufo/waves/round-14/w1/GoEntryDraft.candidate.md` cited `S003`–`S006` once each; peer correction and
  direct re-read of the final 02:23 file (19,539 bytes) show a different set. `grep -o` counts on the final
  file: `S001`=1, `S002`=0, `S003`=1, `S004`=1, `S005`=0, `S006`=0, `S007`=1. Its "Sources reopened for this
  entry" table lists S001 (SKILL `:168-169`), S003, S004, and S007 (`ChangeHistory.md:564,582,585`).
  The frozen delta was corrected to that set; **S005/S006 are not appended** because a used-by that the
  artifact does not cite would be a false registry claim.
- **F6 — claims/entry source mismatch, for L1.** `claims.json` C1 lists `S003`, `S004`, `S005`, `S006`;
  the final entry cites `S001`, `S003`, `S004`, `S007`. This seat does not edit `claims.json` or the entry.
  L1 must either amend the claim's `sources` or restore the dropped citations and remove the added ones;
  the registry should follow the integrated artifact. Until reconciled, neither list can be cited as
  authoritative for the other.
- **F7 — earlier F5 record retained in this trail.** The pre-correction sentence said the draft "names
  S003, S004, S005, and S006 once each". That was true of the 02:22 draft and false of the 02:23 final;
  F5 above is the controlling statement. No registry cell of the earlier shape should be applied.

## Exact retained evidence

- Archive digest: `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`.
- `GoRttiMapper.java`: 1200 lines; version check at 170–171; snapshot call at 176.
- `GoApiSnapshot.java`: `get` at 102; `getApiSnapshotJsonFile` at 118; `EMPTY` return at 115.
- S004 commit: SHA `385e8cd923d09f10b1a7874108e71748875fa174`, `2026-03-03T19:52:38Z`, 10 changed files,
  `GoRttiMapper.java` +1/−1, `go1.26.0.json` added.
- S001 `SKILL.md` digest: `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0`; quote at `:168-169`.
- S007 `ChangeHistory.md` digest: `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`; quote at `:585`.
- S005 README digest: `d44dd94d5a74577fd86fdb70cb87a3f8a683aa6f2088bb30aba722e469bd6094`.
- S006 file digest: `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`.
- Registry rows: S001 line 7, S003 line 9, S004 line 10, S005 line 11, S006 line 12, S007 line 13; the
  four appended rows' final cells are ` corpus/lessons/round-13.md ` before the delta. S005/S006 stay
  untouched.

## Checks run, and not run

Run: digest recomputation (`sha256sum`), archive member listing/extraction, line greps, GitHub commit
metadata and diff fetch, `used-by` cell extraction from the registry, final-entry citation counts
(`S001`=1, `S002`=0, `S003`=1, `S004`=1, `S005`=0, `S006`=0, `S007`=1), quote word counts
(7/5/2/6/7/1/10/17/14/10/20, all ≤25).

Not run: no census validation after a delta (nothing was applied; the C1 entry is absent), no build, lint,
test, formatter, or smoke run; no REA call, provider probe, Ghidra analysis, or target execution. No
checked claim above depends on those unrun checks.

## Risks and blockers

- **R1 (highest)** `claims.json` C1 sources (`S003`–`S006`) and the final entry's citations
  (`S001`/`S003`/`S004`/`S007`) disagree. Apply the delta only after L1 reconciles them; a registry append
  that follows the stale claim would cite an artifact for rows it no longer uses, and omitting S001/S007
  would under-record actual use.
- **R2** If the integrated C1 entry cites a subset of the four, append only for the cited rows (P2).
- **R3** If L1 renames the entry, the literal new cells are wrong; P3 requires substitution, not application.
- **R4** `corpus/SOURCES.md` can shift lines during integration; the candidate says to anchor on `| S00N |`,
  not on the recorded line numbers.
- **Blocker:** none for this seat's work. The delta is intentionally not applied because the cited entry is
  an L1/sibling artifact and is not yet on disk.

## Files written

- `.ufo/waves/round-14/w1/RegistryDeltaDraft.candidate.md` (candidate delta; not applied)
- `.ufo/waves/round-14/w1/RegistryDeltaDraft.md` (this report)

Tool installs/updates: **none** — no new tool was needed for source reading.
