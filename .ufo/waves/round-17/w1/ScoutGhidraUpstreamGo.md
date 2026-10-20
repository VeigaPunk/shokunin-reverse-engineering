# Scout — Ghidra upstream Go 1.26/1.27 declaration (SOURCES lead: "release notes after installed 12.1.4")

Access date **2026-10-20** (fetches ~10:32–10:39 -03). Read-only: releases feed, GitHub tree pages,
`raw.githubusercontent.com`, `git ls-remote`, and a blobless partial clone at `/tmp/ghidra-hist`
(18,825 master commits). No REA analyze/search/decompile, no Ghidra run, no carrier executed.
Observation = OBS, inference = [INFERENCE].

## Answer

**No release after 12.1.4 exists. Master declares Go 1.26 — not 1.27 — in the range, in the data dir,
and in an unreleased "Ghidra 12.2" ChangeHistory line. Nothing upstream declares Go 1.27.**

## 1. Releases after 12.1.4 — none (OBS)

- URL https://github.com/NationalSecurityAgency/ghidra/releases (feed alternate
  `releases.atom`), accessed 2026-10-20. Top item: `Ghidra 12.1.4`, `2026-09-21T17:38:59Z`,
  SHA-256 `ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db`.
  Quote (feed heading, under 25 words): `Ghidra 12.1.4` — from `## Ghidra 12.1.4 *2026-09-21T17:38:59Z*`.
- `git ls-remote --tags --refs` (59 tags): highest is `Ghidra_12.1.4_build` =
  `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc` (tag commit 2026-09-11 06:14:59 -0400,
  `GP-0: Adding ChangeHistory for 12.1.4`). No `12.2`/`13.x` tag.
- Upstream heads: `master` `b8e9917e4c01959fe97ba94954731ed8cf2d201c` (2026-10-20 08:14:31 -0400),
  `patch` `8b6bbb8…` (identical to the 12.1.4 tag commit), `stable` `e46d0866…`
  (`Merge tag 'Ghidra_12.1.4_build' into stable`, 2026-09-21 12:55:40 -0400).

## 2. Master range — `1.15-1.26` (OBS)

- URL https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java#L79
  (raw: `…/master/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`),
  anchor master HEAD `b8e9917e4c01959fe97ba94954731ed8cf2d201c`, accessed 2026-10-20.
- `GoRttiMapper.java:79` (one line, well under 25 words):
  `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");`
- Enforcement is warn-level, not a hard stop: `GoRttiMapper.java:170-171`
  `if (!SUPPORTED_VERSIONS.contains(goVer)) { Msg.error(…, "Untested Go version [%s]"…) }` —
  an out-of-range version still proceeds to `GoApiSnapshot.get` at `:173-176`.
- The same line at the installed-release tag, `Ghidra_12.1.4_build`, reads
  `GoVerRange.parse("1.15-1.25")` — `GoRttiMapper.java:79`, identical to the installed archive
  (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/…/Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79`).
  `patch` and `stable` tips also read `1.15-1.25` at line 79 (both files are 1,200 lines, matching the tag).
- Digest identity (OBS): installed zip member, `Ghidra_12.1.4_build` raw, `patch` tip and `stable` tip are
  **byte-identical**, SHA-256 `2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95`
  (41,672 B); master is `0712837a21754b42d3b2deb19ef5e37d829ea5ea87dd59a4232445f67d7c36cd` (41,895 B).
  So the installed source is not a stale local edit — it is exactly the released 12.1.4 file.
- **No 1.27**: `go1.27.0.json` is HTTP 404 on master (`go1.26.0.json` is 200); no `Go 1.27` mention in
  master `ChangeHistory.md` or `WhatsNew.md`; the range stops at 1.26.

## 3. golang data dir (snapshots) (OBS)

- Master tree `Ghidra/Features/Base/data/typeinfo/golang` (via `git ls-tree origin/master:…`):
  `go1.15.0.json … go1.26.0.json` (12 base JSONs), `golang_1.15…1.23_anybit_any.gdt` (9, no 1.24+ gdt),
  `patchverdiffs` 123 entries, max `go1.24.6.json.diff`.
- No `go1.25.*`, `go1.26.*`, or `go1.27.*` patchverdiffs anywhere on master. Master's 1.26 support is a
  **base snapshot only**. `go1.25.1.json.diff` → HTTP 404 (master).
- Installed 12.1.4 dir is the same shape minus 1.26: 11 JSONs to `go1.25.0.json`, gdt 1.15–1.23,
  123 patchverdiffs max `go1.24.6` (counted locally). `Ghidra_12.1.4_build` `go1.26.0.json` → HTTP 404.
- The JSON-vs-gdt switch is documented by GP-5470: installed `docs/ChangeHistory.md:585` and master
  `ChangeHistory.md:777` — `Added support for Golang 1.24 and 1.25.  Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files. (GP-5470)`
- Snapshot selection rule (OBS, `GoApiSnapshot.java`, byte-identical in the installed zip and master —
  534 lines, zero diff): `getApiSnapshotJsonFile`
  zeroes only the patch (`GoVer baseVer = goVer.withPatch(0)`, `:122`) and opens
  `typeinfo/golang/go<base>.json` (`:123`, `:170`); a miss returns `null`, and `get` returns
  `GoApiSnapshot.EMPTY` (`:115`). There is **no fallback to an earlier minor version**;
  `getPatchVerDiffFile` (`:148-153`) walks patch revs downward and is consulted only after a base exists.
  So on installed 12.1.4 a `go1.27.x` carrier gets `EMPTY`, not the `go1.25.0` base.

## 4. Release-note anchor — the actual lead (OBS)

- URL https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Configurations/Public_Release/src/global/docs/ChangeHistory.md,
  4,203 lines, accessed 2026-10-20.
- `ChangeHistory.md:1`: `# Ghidra 12.2 Change History (October 2026)` — an **unreleased** section
  (no `Ghidra_12.2_build` tag exists).
- `ChangeHistory.md:19` (one sentence, under 25 words): `* _Analysis_. Added support for Golang 1.26.0. (GP-6528, Issue #9013)`
- Installed 12.1.4 `docs/ChangeHistory.md` has **no** 1.26/1.27 line (regex `golang|Go 1.2[4-7]|GP-6528`
  over all 4,011 lines). Its own top section `# Ghidra 12.1.4 Change History (September 2026)`
  (lines 1–22) contains no Go entry; the newest Go support line anywhere in it is GP-5470 at line 585,
  inside `# Ghidra 12.0 Change History (December 2025)` (header at line 564), `### Improvements`.

## 5. Why 12.1.4 is 1.25 despite a March 2026 merge (OBS — calibration-relevant)

- GP-6528 commit `385e8cd923d09f10b1a7874108e71748875fa174`: author 2026-03-03 19:52:38 +0000,
  committer 2026-03-04 00:08:23 +0000, subject `GP-6528 add support for golang 1.26`.
- Merged to master at `f9bc56788cd4d762f4e72d3762b504a66bb8ffc8`, 2026-03-04 13:02:16 -0500:
  `Merge remote-tracking branch 'origin/GP-6528_dev747368_golang_1.26' (Closes #9013)`.
- Pickaxe over master: `-S"1.15-1.26"` → only `385e8cd`; `-S"1.15-1.25"` → `86a525a`
  (`GP-5470 Golang json snapshot data, go1.24, go1.25, swissmap, 2025-08-28`, introduction) then
  `385e8cd` (removal). **No revert** in master history.
- But the release line forked exactly at GP-6528's own parent:
  `git merge-base Ghidra_12.1.4_build 385e8cd^` = `c3fd55c9c8c482d1f67534fb86bf53ff905486f1`
  (2026-02-27 13:44:13 -0500). `Ghidra_12.1_build` has the same merge-base; `Ghidra_12.0.4_build`
  forks earlier, at `54c42f68…`. `Ghidra_12.1_build` is an ancestor of `Ghidra_12.1.4_build`.
- `git merge-base --is-ancestor 385e8cd <tag>` is **false** for 12.0.4, 12.1, 12.1.3 and 12.1.4;
  `git tag --contains 385e8cd` is empty. The tag lineage rejoins master only at
  `51915f3405c7d10aa4920842f4352d8bf80da922` (2026-09-11 06:35:51 -0400,
  `Merge remote-tracking branch 'origin/patch' into Ghidra_12.2`).
- Therefore installed 12.1.4 = 1.25 is **branch topology, not an install lag**: the 12.1 line was cut from
  GP-6528's parent and shipped without it (12.1 tag 2026-05-12; 12.1.4 released 2026-09-21).
  [INFERENCE] The first release that would carry 1.26 is 12.2 (ChangeHistory says October 2026); no such
  tag or release exists as of the access date.

## 6. Consequence for round-17 claims

- S004's mechanism is verified and sharpened: its date `2026-03-03` is the **author** date; the merge is
  2026-03-04 and `385e8cd` never reached any release tag. The row's guardrail ("not the installed 12.1.4
  release") is correct, and the reason is the fork at `c3fd55c`, which the row does not state.
- For `predict.py`'s basis: the installed host's only authoritative bound is `GoRttiMapper.java:79`
  = `1.15-1.25` (identical in installed zip, tag, `patch`, `stable`). A `go1.27.x` carrier is out of
  range → expected log `Untested Go version [go1.27…]` at `:170-171`; `GoApiSnapshot.get` then returns
  `EMPTY` (`GoApiSnapshot.java:115`), because the base file is derived exactly (`withPatch(0)` →
  `go1.27.0.json`, `:122-123`) with **no minor-version fallback**; the `patchverdiffs` walk (`:148-153`) is
  reached only after a base exists. Master's `1.26` is **not** a host capability.
- Lead "Ghidra release notes after installed 12.1.4" resolves to a bounded no-finding: there are no such
  release notes; the only newer statement is master's unreleased 12.2 line 19.

## Confidence

- No post-12.1.4 release, tag set, branch tips: **high** (two independent routes: releases feed + `ls-remote`).
- Range strings and line numbers: **high** (raw at master/tag/`patch`/`stable` + installed zip all agree on line 79).
- Fork point / ancestry / no-revert: **high** (full 18,825-commit blobless clone; pickaxe and `merge-base`).
- 12.2 shipping 1.26: **[INFERENCE]** from the unreleased ChangeHistory title and line; no tag exists.

## Remaining unknowns

- Whether a `Ghidra_12.2_build` tag/release appears in October 2026, and whether it adds 1.25/1.26 patchverdiffs.
- The project-side reason the 12.1 line forked at GP-6528's parent (not recorded in-repo).
- How far Go bootstrap proceeds after an `EMPTY` snapshot for 1.27 — selection is now observed
  (`GoApiSnapshot.java:115`), but downstream RTTI recovery is the S003 lane's question.
- Whether Go 1.27 is even released upstream — owned by the Go release-history lane.
- GitHub REST API (`api.github.com/repos/...`) returned HTTP 403 (unauthenticated block); every claim above
  was instead taken from the HTML tree pages, raw files, and git protocol, so no fact depends on the API.

## Tooling

No installs or upgrades (existing `git`, `curl`). Temporary evidence outside the lane:
`/tmp/ghidra-hist` (blobless partial clone), `/tmp/gr17-*.java|md|json`. Lane write: this report only.
