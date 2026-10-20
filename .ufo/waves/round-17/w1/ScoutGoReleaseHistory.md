# ScoutGoReleaseHistory — round 17 w1 (calibration + depth)

Read-only scout. Question: record go1.27 and 1.26 release dates/minor revisions as stated on
<https://go.dev/doc/devel/release>, bound whether go1.27.0–go1.27.2 carriers are plausible on
2026-10-20, and draft a contract-v1 SOURCES row. Related claim: `.ufo/waves/round-17/claims.json:18`
(C2 out-of-range go1.27.x carrier).

## Method (all observed)

- Fetched the page 2026-10-20T13:32:17Z (HTTP `Date` header), 149,359 bytes, SHA-256
  `d9a4b0ebb8eed5e50b092d5360d811b6dd89a21cb2518f5953bcc12f744d8968`. HTML line anchors below are
  positions **in that fetched representation**, not a stable page version.
- Cross-check: official machine list <https://go.dev/dl/?mode=json&include=all>, SHA-256
  `6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950`. It contains every
  1.26.0–1.26.10 and 1.27.0–1.27.3 object with `stable: true` and 45 files each; it carries no dates,
  so it corroborates existence/ordering only.
- Carrier cross-check (allowed verb): `npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt`
  -> evidence `ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`,
  `go_version: go1.27.0-X:nodwarf5`, `vcs.time 2026-09-06T14:51:11Z`, `GOEXPERIMENT=nodwarf5`.
  Carrier SHA-256 `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459` matches the
  pilot pin at `.ufo/waves/round-17/pilot/README.txt:7`.

## Observed release table (page text, dates only)

| train | release | stated date | anchor (fetched HTML line) | days before 2026-10-20 |
|---|---|---|---|---|
| 1.27 | go1.27.0 | 2026-08-19 | `#go1.27.0` (:474) | 62 |
| 1.27 | go1.27.1 | 2026-09-01 | `#go1.27.1` (:484) | 49 |
| 1.27 | go1.27.2 | 2026-10-08 | `#go1.27.2` (:503) | 12 |
| 1.27 | go1.27.3 | 2026-10-19 | `#go1.27.3` (:525) | 1 |
| 1.26 | go1.26.0 | 2026-02-10 | `#go1.26.0` (:547) | 252 |
| 1.26 | go1.26.1 | 2026-03-05 | `#go1.26.1` (:557) | 229 |
| 1.26 | go1.26.2 | 2026-04-07 | `#go1.26.2` (:579) | 196 |
| 1.26 | go1.26.3 | 2026-05-07 | `#go1.26.3` (:601) | 166 |
| 1.26 | go1.26.4 | 2026-06-02 | `#go1.26.4` (:623) | 140 |
| 1.26 | go1.26.5 | 2026-07-07 | `#go1.26.5` (:645) | 105 |
| 1.26 | go1.26.6 | 2026-08-13 | `#go1.26.6` (:667) | 68 |
| 1.26 | go1.26.7 | 2026-08-19 | `#go1.26.7` (:689) | 62 |
| 1.26 | go1.26.8 | 2026-09-01 | `#go1.26.8` (:708) | 49 |
| 1.26 | go1.26.9 | 2026-10-08 | `#go1.26.9` (:727) | 12 |
| 1.26 | go1.26.10 | 2026-10-19 | `#go1.26.10` (:749) | 1 |

The page has no separate "go1.27" or "go1.26" heading: the major-release entry is the `.0`, with minors
nested under `#go1.27.minor` (:481) and `#go1.26.minor` (:554). Minor headings are `<p id="go1.27.N">`,
not `<h4>`, so `#go1.27.N` is the usable fragment.

## Located quotes (each <=25 words, verbatim rendered text)

- `#go1.27.0` — "go1.27.0 (released 2026-08-19)" (3 words)
- `#go1.27.2` — "go1.27.2 (released 2026-10-08)" (3 words)
- `#go1.27.3` — "go1.27.3 (released 2026-10-19)" (3 words)
- `#go1.26.0` — "go1.26.0 (released 2026-02-10)" (3 words)
- `#go1.26.10` — "go1.26.10 (released 2026-10-19)" (3 words)
- `#policy` (:464) — "Each major Go release is supported until there are two newer major releases." (13 words)

Quote text is identical in the HTML source, e.g. `:474` is
`<h2 id="go1.27.0">go1.27.0 (released 2026-08-19)</h2>` and `:484-486` holds `go1.27.1` /
`(released 2026-09-01)`.

## Bound on go1.27.0–go1.27.2 carriers at 2026-10-20

**Observed:** 1.27.0, 1.27.1 and 1.27.2 are each stated as released 62, 49 and 12 days before the
access date. **Conclusion (inference from those dates):** all three are time-plausible toolchain
versions for a carrier observed on 2026-10-20 — yes.

Boundary details that matter for the C2 claim:

1. The time-plausible 1.27 set is **.0–.3, not .0–.2**: go1.27.3 was released 2026-10-19, one day
   before access, so it may also appear (newest distro rebuilds are unlikely but not impossible).
2. Per-version **lower bound** on build time: the stated release date. A carrier reporting
   `go1.27.2` cannot have been built before 2026-10-08; `go1.27.0` before 2026-08-19; `go1.27.3`
   before 2026-10-19. Date granularity only — the page states no time of day.
3. **No upper bound follows.** A binary built on 2026-10-20 with a pinned older toolchain still
   reports the old patch. Observed example: `/usr/bin/shfmt` package Build Date 2026-09-07 05:40:01
   -03 (`pacman -Qi shfmt`), six days *after* go1.27.1 (2026-09-01), yet its buildinfo reports
   go1.27.0. So the release list bounds toolchain availability from below, never the carrier's build
   date from above.
4. The only timestamp inside the carrier's buildinfo is `vcs.time` (main-module commit), also a lower
   bound: derived lower bound = max(toolchain release, `vcs.time`). For shfmt,
   max(2026-08-19, 2026-09-06T14:51:11Z) = 2026-09-06, consistent with the 2026-09-07 package build.
5. **Bounded absence (observed at fetch):** the page contains no `go1.27.4` and no `go1.26.11`
   (grep count 0). A carrier claiming those versions is not time-plausible as of 2026-10-20, absent
   a page update after this fetch.
6. Support status (from `#policy`): with 1.27 out, 1.25 is no longer supported and 1.26 remains
   supported. This affects "uses a supported toolchain", not plausibility; the in-range esbuild
   carrier `go1.23.12` (`.ufo/waves/round-17/pilot/README.txt:8`) is a valid but unsupported toolchain.

**Cross-train pattern (observed dates; inference):** after 1.27.0 the two trains ship in lockstep —
1.26.7/1.27.0 (08-19), 1.26.8/1.27.1 (09-01), 1.26.9/1.27.2 (10-08), 1.26.10/1.27.3 (10-19). So a
future patch pair can be expected to share one date; this predicts availability windows but does not
change the current bound.

## SOURCES row draft (contract v1, 11 columns; `corpus/SOURCES.md:5`)

Proposed id `S024` (first free at `corpus/SOURCES.md:29` ends S023; renumber if
`.ufo/waves/round-17/w1/draft-sources-rows.md` assigns otherwise — that aggregate is
ScoutRegistryRows/L1-owned).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S024 | Go Release History — https://go.dev/doc/devel/release | docs | A | Official Go project release-date list for stable Go 1.26 and 1.27 majors/minors, not carrier build dates | Fetched 2026-10-20T13:32:17Z, 149359 B, SHA-256 `d9a4b0ebb8eed5e50b092d5360d811b6dd89a21cb2518f5953bcc12f744d8968`; `#go1.27.0` (:474), `#go1.27.minor` (:481), `#go1.26.0` (:547), `#go1.26.minor` (:554); quote "go1.27.2 (released 2026-10-08)" | A stated release date is a lower bound for when a toolchain version could appear and never dates a carrier's build; patch trains 1.26/1.27 shipped in lockstep after 1.27.0. | mined | 2026-10-20 | on-release | `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (planned, `.ufo/waves/round-17/contract.md:117`), `corpus/lessons/round-17.md` — L1 to finalize |

## Remaining unknowns / limits

- Living page: the SHA-256 pins only the fetched representation; dates could be edited or reordered.
  Recheck is `on-release` by design. A later fetch could also change the `.3`/`.4` boundary.
- No time-of-day is published; the bound is day-granular.
- The `dl` JSON cross-check proves listed release objects and linux/amd64 artifacts exist, not their
  dates and not archive signatures (tarballs were not downloaded or verified).
- The release page says nothing about Ghidra's `1.15–1.25` Go gate (S003); 1.27 remains out of range
  for that parser regardless of release date.
- No go1.27.3 carrier is present in this lane's pilot evidence; only go1.27.0 (`shfmt`) was observed.

## Tooling

No installs or upgrades. Commands used: `curl` read-only fetches, `npx -y rea-agents@6.5.0
inspect-go-binary` (allowed verb), `pacman -Qi/-Qo` read-only queries, `sha256sum`, `stat`.
