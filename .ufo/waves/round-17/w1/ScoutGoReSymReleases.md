# ScoutGoReSymReleases — releases after README commit d7f23b7

- Seat: `KaidokuR17.ScoutGoReSymReleases-3` (scout; leaf; no dispatch).
- Question: is there a GoReSym release after README commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` that states Go 1.26/1.27 support?
- Access date for every source: **2026-10-20**.
- Method: read-only web reads of the releases page/feed, tag READMEs, tag trees, and tag diffs; no REA analyze/search/decompile, no Ghidra, no carrier execution, no installs. Scratch extraction under `/tmp` was removed; this report is the only lane write.

## Verdict

**Go 1.26: yes.** Release `v3.3` (2026-03-06) states `Add 1.26 support`. **Go 1.27: no.** No release, tag, README, or master-tree string states 1.27 support; `v3.4.1` (2026-09-14) is the latest release and only reaches `1.26`.

Primary located quote (3 words, release body verbatim):

> "Add 1.26 support"

- URL: https://github.com/mandiant/GoReSym/releases/tag/v3.3
- Tag: `v3.3`; tag commit `78c02cc73064da84dd528220a234e9bd9f133d81`
- Release date: 2026-03-06T20:20:36Z (releases feed); the HTML page renders `06 Mar 20:19`, same event.
- Full body: `Add 1.26 support` / `Add 1.25 support` / `Enhance CI thanks @kami922`.
- Caveat (observation): the body does not contain the token `Go`. Reading `1.26` as Go 1.26 is [INFERENCE], corroborated below by the tag's code and test-version list.

Second release, 1.26 handling without the word "support" (13 words):

> "trying runtime versions 1.20 - 1.26 which all share the same layout version"

- URL: https://github.com/mandiant/GoReSym/releases/tag/v3.4.1
- Tag: `v3.4.1`; tag commit `722897e0a80da0a06c00c5e40591a253a551f04e`; `Latest`.
- Release date: 2026-09-14T17:09:16Z.
- Full body adds: `but have fields shifted in 1.26+ #102 @mlhaigh`.

Chronology check (observation): pinned commit `d7f23b7` is dated **2026-02-17T15:14:48Z** (commit page `meta-og:updated_time` epoch 1771341288; matches `.ufo/waves/round-14/w1/ReviewRegistry.md:37`). Releases after it: `v3.2` 2026-02-17T15:21:31Z (under seven minutes later; only the `-strings` flag, no version claim), `v3.3`, `v3.4` 2026-07-01T20:30:38Z (field tags/string VA; no version claim), `v3.4.1`.

## Calibration: the README itself was never updated

Observed: the README at `v3.3`, at `v3.4.1`, and on `master` (all fetched 2026-10-20) is unchanged on the two relevant sections:

- `README.md:95` (v3.4.1 tag): "This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20."
- `README.md:118` (v3.4.1 tag): "Added parsing support for Go 1.24 binaries while retaining compatibility with older 1.2 layouts."
- The `# Version Support` block (README lines 85–95) diffs clean between `v3.3` and `v3.4.1`.

Consequence: a citation of GoReSym's README cannot establish Go 1.26 support; only the `v3.3` **release note** (plus tag code) does. Conversely, `corpus/SOURCES.md:11`'s statement that S005 "does not establish Go 1.26 support" stays true **for the pinned commit** and must not be silently rewritten to say the README claims 1.26.

## Depth corroboration in the tag trees (observed)

`v3.3` tree (sha256 not taken; downloaded tag tarball, removed):

- `objfile/layouts.go:187` — "Go stopped bumping the pclntab magic byte after 1.20, so 1.20-1.26 all share the same layoutVersion ("1.20")."
- `objfile/layouts.go:195` — `case "1.26":`; `:234` — `case "1.26", "1.25", ... "1.21":`; `:780` — `case "1.20" ... "1.26":`.
- `objfile/layouts_test.go:19` — `{"1.26", "1.22"}, // 1.26 uses 1.22 layout`.
- `build_test_files.sh:4` — fixture versions start `("1.26" "1.25" ...)`.
- `debug/gosym/pclntab.go:267` — `if strings.Contains(versionOverride, "1.26") ||`.
- `objfile/objfile.go:295,531,997,1168` — `1.26` cases.

`v3.4.1` tree:

- `objfile/objfile.go:271–283` — `runtimeVersions` retry list; `:275` — "Go 1.26 introduced epclntab, shifting textsectmap and subsequent fields."; `:278` — `runtimeVersions = []string{"1.20", "1.26"}`.
- `objfile/objfile.go:303,551,1171,1342` — `1.26` cases.

Interpretation [INFERENCE]: `v3.3`'s "Add 1.26 support" is a real code-path addition, not a marketing-only note; `v3.4.1` is a later fix for Go 1.26 moduledata parsing when version recovery fails. Neither release promises symbol/type recovery equivalence to an in-support Go compiler.

## Go 1.27 — bounded no-finding

Searched, all on 2026-10-20:

1. Releases page and full `releases.atom` body text (10 releases, v3.0 → v3.4.1): zero occurrences of `1.27`.
2. Tags listing `https://github.com/mandiant/GoReSym/tags`: newest tag is `v3.4.1`; no later tag exists.
3. `master` tree (tarball of `refs/heads/master`, grep `*.go,*.sh,*.md` for `1.27`): no Go-version hit; the only `127` matches are unrelated numeric constants (`buildid/rewrite.go:41`, `debug/dwarf/attr_string.go:118,244`, `debug/elf/elf.go` relocation numbers).

So the release-note answer for 1.27 is **no statement of support**, not "support absent from the code" — master was only string-grepped, and no execution or analysis was performed.

## SOURCES lead disposition (draft for L1; I did not edit SOURCES)

`corpus/SOURCES.md:53` currently reads that no GoReSym release source "was opened to check for later Go-version coverage." This is now resolved and that lead can be closed. Minimal replacement (one line):

> - GoReSym releases after README commit `d7f23b7…` — **closed 2026-10-20**: `v3.3` release notes state "Add 1.26 support" (tag `v3.3`, 2026-03-06, `https://github.com/mandiant/GoReSym/releases/tag/v3.3`); `v3.4.1` (2026-09-14) adds 1.26 moduledata handling; no release states Go 1.27 support.

Suggested adjacent note on `corpus/SOURCES.md:11` (S005 row), keeping its existing scope: the pinned README still says layouts through 1.20 and Changes through Go 1.24; the 1.26 claim is a **later release note**, not the pinned README. A new SOURCES row for the `v3.3` release note (kind `docs`/`code`, recheck `on-release`) would let knowledge entries cite the release directly without overloading S005.

## Remaining unknowns

- Whether `v3.3`'s 1.26 path fully covers type parsing: `v3.4.1`'s retry fix implies gaps existed; not tested (no execution permitted in this lane).
- Any pre-release/CI-only 1.27 work upstream: not visible in releases, tags, or literal `1.27` strings on master.
- Release-note "1.26" is not prefixed with "Go"; the Go meaning is inferred from repository context and `build_test_files.sh:4`, not stated in the note.

## Confidence

High that `v3.3` states 1.26 support, that no release states 1.27 support, and that `v3.4.1` is latest; medium-high for the master-tree 1.27 bound (literal grep only); high for the README-unchanged observation (tag/master fetches + clean block diff).

No tools installed or upgraded; no pacman operations. Footprint: this report only.
