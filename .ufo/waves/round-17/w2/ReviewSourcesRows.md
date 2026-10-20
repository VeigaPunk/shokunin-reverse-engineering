# ReviewSourcesRows — round 17 w2 (falsify)

Seat: `KaidokuR17.ReviewSourcesRows` (leaf; no dispatch). Revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`
(baseline `b563c799d97774aae4351276fe43cb897311e349`; predictions frozen at `271167473d87ef710f07ecdd98caf0ce12091686`).

Scope: rows S024–S030 in `corpus/SOURCES.md:30-36` against `CORPUS.md:76-129` contract v1 —
11 cells, no pipes, scoped tiers (community never A; S027 B justified; S028 rejected format),
anchors with revision, `used-by` paths that exist and cite each id, search-log counts.
Read-only: no REA analyze/search/decompile, no Ghidra, no carrier execution. Local `go1.27.3`
tree read only; `go version -m /usr/bin/shfmt` reads bytes. Web reads via `curl`; Python used
only with `-B`; scratch under `/tmp`. No tools installed or upgraded.

## Findings

### P2-1 — S028's `flip` is already satisfied by a source this round opened; it does not describe a verdict change

`corpus/SOURCES.md:34` (S028) rejects the **Go 1.27** notes, then says:
`flip: a release note or doc page that defines the DWARF 5 experiment opt-out.`

OBS: The Go 1.25 release notes do exactly that, and the round already opened them:

```
$ curl -sL https://go.dev/doc/go1.25 -o /tmp/kr17-go125.html
$ grep -c 'DWARF 5 generation can be disabled by setting the environment variable GOEXPERIMENT=nodwarf5 at build time' /tmp/kr17-go125.html
1
$ sed -n '621p' /tmp/kr17-go125.html
<h3 id="dwarf5-support">DWARF5 support</h3>
```

w1 records the same page and quote: `.ufo/waves/round-17/w1/ScoutGoExperimentSuffix.md:106`
(`Go 1.25 release notes | https://go.dev/doc/go1.25#dwarf5-support | quote: DWARF 5 generation
can be disabled by setting the environment variable GOEXPERIMENT=nodwarf5 at build time`).

[INFERENCE] Read literally, the flip is already true, so it is not "what would change the
verdict" on the 1.27 page: a 1.25 release note does not make the 1.27 notes document the token.
The rejection reason itself is sound (the 1.27 page has zero dwarf text — verified below); the
flip is mis-scoped.

Smallest fix: make the flip version-specific, e.g.
`flip: a Go 1.27-or-later release note or doc page that defines the DWARF 5 opt-out.`
(Alternatively admit the 1.25 page as its own `docs`/A row and drop the flip.)

### P2-2 — Round-17 search-log counts are row-level; sources the round opened are uncounted, and the universal negatives' denominators are absent

`corpus/SOURCES.md:57` says: `Identified 8 new candidate sources; screened 8; included 6 as
mined rows (S024–S027, S029, S030); excluded 2: S028 kept as a rejected row ..., and
pkg.go.dev/debug/buildinfo screened out without a row ...`.

OBS: The arithmetic matches the registry exactly: 6 mined + 1 rejected + 1 no-row = 8, and
6 + 2 = 8. The row-level check passes.

OBS: The same round's w1 record opens further sources that the log neither lists under
"Where searched" nor counts:

- `go.dev/doc/go1.25#dwarf5-support` — opened and quoted (`ScoutGoExperimentSuffix.md:106`);
- `go.dev/doc/toolchain#name` — opened and quoted (`:107`);
- commit `9daaab3` — opened (`:108`);
- go1.27.2 source tarball (`:104`) and five tag files (`:133`).

The go1.25 page is not incidental: it is the page that defines the `nodwarf5` opt-out that
S028 rejects and that the carriers' version strings use. It is absent from both the registry
and the log's counts.

OBS: The universal negatives also rest on sweeps whose counts are not in the log:
S029 "no Ghidra source observed declares 1.27" (`SOURCES.md:35`) rests on 59 tags and the
releases feed (`.ufo/waves/round-17/w1/ScoutGhidraUpstreamGo.md:19-21`); S030 "no release
states 1.27" (`SOURCES.md:36`) rests on 10 releases (`w1/ScoutGoReSymReleases.md:61-66`).

[INFERENCE] "Candidate sources" is being used as "candidate rows". The count is defensible
only if labelled that way; as written, a reader reconciling rule 5's identified/screened
counts against the round's actual reading will find opened sources missing.

Smallest fix: add one sentence to the round-17 entry naming the w1 supporting pages and the
tag/release sweep counts with their disposition ("supporting, not rows"), or relabel the
count "8 candidate rows" and say the supporting pages were not row candidates.

### P3-1 — S026's anchor does not ground the `nodwarf5` spelling

`corpus/SOURCES.md:32` anchor cites `exp.go:79-84` (baseline `Dwarf5`) and
`exp.go:157-161` (`String()` elides baseline flags). It omits the branch that spells a
disabled experiment `no<name>`:

```
$ sed -n '182,187p' /home/vgpnk/.local/opt/go-1.27.3/src/internal/buildcfg/exp.go
		if all || val != baseVal {
			if val {
				list = append(list, name)
			} else {
				list = append(list, "no"+name)
			}
```

OBS: From the cited lines alone a reader can learn that only non-baseline flags are listed,
but not that a disabled `Dwarf5` becomes `nodwarf5`; the row's own example
`go1.27.0-X:nodwarf5` is therefore not derivable from its anchor.

OBS: The w1 draft row anchored `exp.go:79,84,167-189`
(`w1/ScoutGoExperimentSuffix.md:124`), so the admitted row dropped the needed lines.

Smallest fix: append `; exp.go:176-188` to S026's anchor.

### P3-2 — S029's master half is not revision-pinned

`corpus/SOURCES.md:35` anchor: `master :79 "1.15-1.26"; ... fetched 2026-10-20`. A fetch date
is not the revision the contract asks for (version, commit, or publication date); unlike the
tag half, there is no digest for master.

OBS: The values needed already exist in the round:

```
$ sha256sum /tmp/kr17-ghidra/GoRttiMapper.master.java
0712837a21754b42d3b2deb19ef5e37d829ea5ea87dd59a4232445f67d7c36cd
$ sed -n '22p' .ufo/waves/round-17/w1/ScoutGhidraUpstreamGo.md
  `master` `b8e9917e4c01959fe97ba94954731ed8cf2d201c` (2026-10-20 08:14:31 -0400),
```

Smallest fix: append `master @ b8e9917e4c01959fe97ba94954731ed8cf2d201c` (or the file sha256)
to the anchor.

## Bounded no-findings (checked, nothing actionable)

- **Cells / pipes.** OBS: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
  → `30`; `awk -F'|' '/^\|.../ && NF!=13 {n++} END{print n+0}'` → `0`; lines 30–36 each
  `NF=13` (11 cells). No stray pipe.
- **Tier scoping.** OBS: S027 is `kind=docs`, `tier=B`, scope "Maintainer discussion ... rationale
  only, not normative", and its teaches defers shipped behavior to S026 — B is the highest
  defensible tier for a tracker thread; it is not used as normative support. No `community`
  row in S024–S030 claims A. S028 is `rejected` with tier C, which only marks it a lead.
- **Rejected-row format.** OBS: S028 reads `REJECTED: <reason>; flip: <condition>` exactly.
  The 1.27 page really has no dwarf text: `grep -ic dwarf /tmp/kr17-ghidra/go-1.27.html` → `0`;
  `nosizespecializedmalloc` and `nojsonv2` each occur once (both are opt-out sentences).
- **`used-by` existence and citation.** OBS: the contract census's mined-row loop prints no
  `missing:` path. Per-id counts: knowledge file cites S024/S025/S026/S029 (1 each) and not
  S027/S028/S030; `corpus/lessons/round-17.md` cites S024–S030 (4/3/4/2/2/4/4). Every mined
  row therefore has ≥1 listed path that cites it; S027/S028/S030 being lesson-only is
  consistent with the knowledge entry's `source:` line (`knowledge/...:1`).
- **Append-only rule.** OBS: `git diff b563c79..HEAD -- corpus/SOURCES.md` is 14 insertions /
  4 deletions: S024–S030 added, and only S003/S023 changed. Field-by-field extraction of both
  rows at baseline vs HEAD shows exactly one changed cell, field 12 (`used-by`); the old→new
  transitions are logged at `corpus/lessons/round-17.md:64-66`. No status, recheck, tier, or
  anchor changes on existing rows.
- **Anchors with revision (other rows).** OBS:
  - S024: `buildinfo.go:58` `var buildInfoMagic = []byte("\xff Go buildinf:")`, `:97`
    `bi.GoVersion = vers`, `:200-202` version flag constants, `:224-237` inline decode,
    `:262-268` modinfo framing — all match the go1.27.3 tree.
  - S025: snapshot sha256 `d9a4b0ebb8eed5e50b092d5360d811b6dd89a21cb2518f5953bcc12f744d8968`
    matches; rendered text has `go1.27.0 (released 2026-08-19)`, `go1.27.3 (released
    2026-10-19)`, `go1.26.0 (released 2026-02-10)`, and one Release Policy sentence.
  - S026: `main.go:191-198` contains `buildVersion += sep + "X:" + goexperiment` with the dash
    branch at `:194-196`; `exp.go:84` sets baseline `Dwarf5: dwarf5Supported`.
  - S027: page title is `go/version: does not support the X: suffix from go env GOVERSION`;
    the quoted sentence is in a comment whose embedded JSON author is `login":"dmitshur"`
    (found at byte 216179, body at 217275), dated 2025-10-17; `Go1.26` milestone present.
  - S028: snapshot sha256 `a4c56ba584ac26614537ac40bf07aa638314decdacf32ea96acb60dbfe57393e`
    matches.
  - S029: tag file sha256 `2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95`
    matches; `sed -n '79p'` gives `parse("1.15-1.25")` at the tag and `parse("1.15-1.26")` on
    master; `gp6528.patch:151` is the `+...1.15-1.26` line; atom newest entry is `Ghidra
    12.1.4`, `2026-09-21T17:38:59Z`.
  - S030: release page contains `Add 1.26 support` (4 HTML copies) with
    `datetime="2026-03-06T20:19:28Z"` and tag commit `78c02cc73064da84dd528220a234e9bd9f133d81`;
    releases page shows `v3.4.1` and `2026-09-14`.
- **Gate rule 1.** OBS: `round-17.md:39-53` has at least one URL+location+quote for every new
  row, access date 2026-10-20 section-wide; all quotes are ≤25 words (S027 14, S028 9,
  S030 3, others shorter). Quotes were checked against the sources above.
- **S024's teaches.** OBS: the stdlib reader returns the raw token end to end:
  `go version -m /usr/bin/shfmt` → `go1.27.0-X:nodwarf5`; `Read` assigns `vers` unchanged at
  `buildinfo.go:97`. Absence of the magic yields `errNotGoExe` (`buildinfo.go:172,183,188,260`),
  i.e. no build-info record.
- **S030's negative claim.** OBS: after stripping tags, the releases page has zero `1.27[^0-9]`
  version tokens; the 27 raw `1.27` hits are SVG path data such as `1.275`. Latest release is
  `v3.4.1` (2026-09-14). The claim is true as of access; only its sweep accounting is thin
  (P2-2).

## Residual risk / verification gaps

- GitHub REST API was rate-limited (`{"message":"API rate limit exceeded ..."}`), so release
  enumeration used the HTML release pages (e.g. 407,880 B for GoReSym releases) and w1 reports,
  not the API.
- `go.dev/src` URLs are the unversioned master view; line anchors were verified against the
  pinned local go1.27.3 tree, not the live pages. The row anchors do name `go1.27.3`, so the
  revision is present.
- The Gate's second S029 quote is the GP-6528 commit patch, which is S004's anchored artifact
  (`SOURCES.md:10`), listed under S029. The URL makes provenance visible; a reader scanning by
  id may double-count it. This is not a contract violation (S029's teaches cites GP-6528).
- S027's `kind: docs` for an issue thread is a taxonomy judgment; `community` would also be
  defensible. Tier B keeps the authority bounded either way; no change required.
- I re-opened all seven rows' quoted sources and the go1.25 page, but did not re-open every w1
  quote in the round. No carrier was executed and no REA/Ghidra run was made; recovery-quality
  claims were outside this lane's contract.
