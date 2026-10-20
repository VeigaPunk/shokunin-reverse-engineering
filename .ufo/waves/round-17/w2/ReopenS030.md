# ReopenS030 — S030 (GoReSym v3.3 release note), wave-2 falsification

Seat: `KaidokuR17.ReopenS030` (leaf; read-only attack of wave-1/L1 artifacts)
Date: 2026-10-20. Lane revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`.
Targets: `corpus/SOURCES.md:36` (row S030), `corpus/lessons/round-17.md:53` (Gate, "Opened sources and located quotes").
Verdict: **bounded no-finding**. All five checked row fields and the located quote reproduce at the access date; no correction is needed.

## What I opened, verbatim

`read https://github.com/mandiant/GoReSym/releases/tag/v3.3` (rendered; access 2026-10-20) returned, among the page chrome:

```
# v3.3
...
stevemk14ebr released this 06 Mar 20:19
...
[Commit] `78c02cc`
...
- Add 1.26 support
- Add 1.25 support
- Enhance CI thanks @kami922
```

`read https://github.com/mandiant/GoReSym/releases/tag/v3.3:raw`, then `grep -n "Add 1.26" artifact://16136`:

```
625:<li>Add 1.26 support</li>
```

`read https://github.com/mandiant/GoReSym/releases.atom` (the `/releases/latest` and `/releases?page=2` fetches redirected to this feed):

```
## v3.4.1
*2026-09-14T17:09:16Z*

Improve handling of 1.20+ layouts when version info cannot be recovered by trying runtime versions 1.20 - 1.26 which all share the same layout  version but have fields shifted in 1.26+ #102 @mlhaigh

...
## v3.3
*2026-03-06T20:20:36Z*

Add 1.26 support
Add 1.25 support
Enhance CI thanks @kami922
```

Feed is newest-first; `v3.4.1` is the top entry and `read https://github.com/mandiant/GoReSym/releases/latest` resolved to `https://github.com/mandiant/GoReSym/releases/tag/v3.4.1` with the `Latest` label.

`git ls-remote https://github.com/mandiant/GoReSym 'refs/tags/v3.3*' 'refs/tags/v3.4*'` (run 2026-10-20):

```
78c02cc73064da84dd528220a234e9bd9f133d81	refs/tags/v3.3
157cabbafb9c1f9ecbe548b702c8f0e8a66148a2	refs/tags/v3.4
722897e0a80da0a06c00c5e40591a253a551f04e	refs/tags/v3.4.1
```

`git ls-remote --tags https://github.com/mandiant/GoReSym` ends at `722897e0a80da0a06c00c5e40591a253a551f04e refs/tags/v3.4.1`; no tag newer than v3.4.1 exists (38 tags total, v1 through v3.4.1).

`read https://github.com/mandiant/GoReSym/commit/78c02cc73064da84dd528220a234e9bd9f133d81.patch` header:

```
From 78c02cc73064da84dd528220a234e9bd9f133d81 ...
Date: Thu, 5 Mar 2026 21:29:56 +0000
Subject: [PATCH] add support for Go runtime v1.26 (#85)
```

`read https://raw.githubusercontent.com/mandiant/GoReSym/{v3.3,v3.4.1,master}/README.md` — all three agree on the two relevant statements:

```
This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.
...
*   Added parsing support for Go 1.24 binaries while retaining compatibility with older 1.2 layouts.
```

`read https://github.com/mandiant/GoReSym/commit/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d.patch` header: `Date: Tue, 17 Feb 2026 20:14:48 +0500` (= 2026-02-17T15:14:48Z); `refs/tags/v3.2` is the same commit, and the v3.2 release is `2026-02-17T15:21:31Z`. So "after the S005 README commit" holds for v3.3.

Both target files are clean at the lane revision — `git status --porcelain corpus/` printed nothing, and `git diff --stat da64646adcb19c1ede7537b799b8c7d283fe43da -- corpus/SOURCES.md corpus/lessons/round-17.md` printed nothing. `git show da64646...:corpus/SOURCES.md | sed -n '36p'` and `git show da64646...:corpus/lessons/round-17.md | sed -n '53p'` reproduce the working-tree rows quoted below.

## Row S030 field-by-field

| Field | Committed text | What I observed (2026-10-20) | Verdict |
|---|---|---|---|
| id/source | `S030` / `Mandiant GoReSym release v3.3 — https://github.com/mandiant/GoReSym/releases/tag/v3.3` | Page exists at that URL; title `Release v3.3 · mandiant/GoReSym` | match |
| kind/tier | `docs` / `A` | Primary maintainer release note on the project's own GitHub release page; same convention as S012/S025/S029 (primary docs = A) | match |
| scope | `GoReSym's own release-note statement of Go version support after the S005 README commit` | v3.3 release published 2026-03-06; S005 README commit d7f23b7a authored 2026-02-17T15:14:48Z; README unchanged through v3.4.1/master | match |
| anchor | `Tag v3.3 (commit 78c02cc73064da84dd528220a234e9bd9f133d81), 2026-03-06, release body; latest release v3.4.1 2026-09-14; accessed 2026-10-20` | Tag ref resolves exactly to `78c02cc...`; release feed timestamp `2026-03-06T20:20:36Z`; top/latest release `v3.4.1` at `2026-09-14T17:09:16Z`; access date is today | match |
| teaches | `The maintainer's release note states 1.26 support while the README stays at older layouts, so version support must be read from release notes; no release states 1.27.` | v3.3 body says `Add 1.26 support`; README at v3.3/v3.4.1/master still lists pclntab layouts through 1.20 and Changes through Go 1.24; the ten releases exposed by the feed (v3.0–v3.4.1) contain no `1.27`; no tag newer than v3.4.1 | match |
| status/opened/recheck | `mined` / `2026-10-20` / `on-release` | Opened and quoted this round; cited by the lesson at lines 53 and 67; a release-notes source changes on release, so `on-release` is the right cadence | match |
| used-by | `corpus/lessons/round-17.md` | The lesson cites S030 at line 53 (quote) and line 67 (lead resolved); the knowledge entry's source line (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1`) lists S003/S023/S024/S025/S026/S029, not S030, consistent with the row's single used-by path | match |

## Located quote

Committed row (`corpus/lessons/round-17.md:53`):

```
| S030 | https://github.com/mandiant/GoReSym/releases/tag/v3.3, release body | Add 1.26 support |
```

- Exact text: `Add 1.26 support` is a contiguous substring of the release body (`<li>Add 1.26 support</li>`, raw-HTML line 625) and of the feed's v3.3 body. No punctuation, ellipsis, or case change.
- Length: 3 words (limit 25).
- Location: "release body" is correct; the phrase is in the release description, not the title (`v3.3`), tag, or compare text.
- The neighbouring bullets are `Add 1.25 support` and `Enhance CI thanks @kami922`; the quoted phrase is the first bullet, unmodified.

## Precision observations (not findings; no correction proposed)

1. **Release date vs commit date.** The row's `2026-03-06` is the release publication date (`2026-03-06T20:20:36Z` in the feed; `06 Mar 20:19` rendered on the tag page). The tag commit `78c02cc` was authored `Thu, 5 Mar 2026 21:29:56 +0000`. This is not a mismatch — the row cites the *release body*, and the release page dates the release — but the row does not spell the distinction out. Optional clarity only: `Tag v3.3 (commit 78c02cc...; release published 2026-03-06)`.
2. **The release body does not contain the token `Go`.** `Add 1.26 support` is unqualified in the body; reading `1.26` as Go 1.26 comes from repository context and is corroborated by the v3.3 commit subject `add support for Go runtime v1.26 (#85)` and the tag code (w1 `ScoutGoReSymReleases.md` records the `case "1.26"` paths). The row's scope already frames the source as "Go version support", so the registry statement is not overreaching; this is a caveat the w1 report carries and the SOURCES row compresses.
3. **"No release states 1.27" is bounded but safe.** The feed exposes the 10 most recent releases (v3.0 → v3.4.1), not all 38 tags; older tags may or may not have release objects. Any release old enough to be absent from the feed predates Go 1.27.0 (2026-08-19, S025), and v3.4.1 — the only release published after that date — does not state 1.27. So the negative holds in the only window where a 1.27 statement could exist. The row does not state this bound; no correction needed.

## Bounded no-finding

I checked: tag-to-commit identity for v3.3 (`git ls-remote`), the release publication timestamp and body (feed + tag page + raw HTML), the latest-release identity and timestamp (`/releases/latest` redirect + feed top), the complete tag list (no tag after v3.4.1), the README text at v3.3/v3.4.1/master ("layouts through 1.20", "Go 1.24" changes), the S005 commit date (patch header), the committed rows at `da64646` (`git show`/`git diff`), and the lesson's citation paths. I found no inaccurate field, no non-contiguous or over-25-word quote, and no wrong quote location.

Confidence: high for the row and quote; high for the "no release states 1.27" result within the stated bound (the feed/tag evidence is complete for releases published after Go 1.27.0).

Tool installs/updates: none. No REA analyze/search/decompile, no Ghidra, no carrier execution. `api.github.com` returned HTTP 403 to the read tool, so the HTML page, atom feed and `git ls-remote` were used instead; that is a host/tooling limitation, not a lane defect.
