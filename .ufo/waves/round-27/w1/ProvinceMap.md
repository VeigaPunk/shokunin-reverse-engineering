# ProvinceMap — round-27 coverage-map and frontier drafts

Seat: `KaidokuR27.ProvinceMap` (leaf, wave 1, round 27 attempt 1).
Scope: drafts only. No lane file was edited, no REA call was made, no commit was made.

## Behavior delivered

Six drafted lines, each with its exact insertion point at lane HEAD `a4f674b343d8564e21f7eb8984630a95089c82d6`
(the round-27 freeze commit). Full text with fill instructions is in the artifact below.

| # | File | Heading | Insertion point | Action |
|---|---|---|---|---|
| A | `corpus/README.md` | `## Coverage map` (line 11) | after line 75 (round-26 map row); new row becomes line 76 | one coverage-map row, `<V1>` `<V2>` placeholders |
| B | `corpus/README.md` | `## Knowledge` (line 77) | after line 166 (round-26 entry row); new row becomes line 167 | one Knowledge index line |
| C | `corpus/README.md` | `## Known gaps` (line 201), evidence-id bullet opened at line 205 | after line 206 (the round-26 sub-bullet); new sub-bullet becomes line 207 | two indented sub-bullets: round-27 renamed-copy/second-carrier update, and the cross-pin attribution limit |
| D | `PROVINCE.md` | end of file (after line 303) | append one `## ` dated section | two Core-grade lines; no Core table row added, no Frontier bullet retired |
| E | `SCORECARD.md` | `## Capabilities` (line 615), table body | after line 622 (last capability row); new row becomes line 623 | one capability row naming `tools/round-27/xpin-attribute.mjs` (required by the frozen R27-C2 statement) |

No line is drafted for `corpus/README.md` `## Frontier` (heading line 189, bullets 190-199):
none of those ten open-surface items is about evidence-id identity and round 27 closes
none of them. No `PROVINCE.md` Frontier bullet moves to Core — the five bullets at
`PROVINCE.md:82-93` (PE subtypes, recorded crashes above 32 MiB, alternate providers,
macOS-only surfaces, EVM bytecode extended) are untouched by this round, so the drafted
PROVINCE change is a dated section in the form the file already uses for rounds 20, 22, 23
and 24, leaving the Core table above unrewritten.

Round-26 precedent read and matched: `git show ebe2cb4a -- corpus/README.md PROVINCE.md`
(round 26 touched `corpus/README.md` only, three insertions: one map row, one Knowledge
line, one Known-gaps sub-bullet) and `git show 08c7a729 -- PROVINCE.md` (round 25 changed
one Frontier bullet in place).

## Gates on landing

- `corpus/README.md` states "A row is written when its file exists, never before". Drafts
  A, B, C and D all cite the round-27 knowledge entry, so none lands before
  `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` exists in the tree.
- Drafts A, B, C and D carry `<V1>` (verdict tally over the 16 committed rows) and `<V2>`
  (what the rename changed against the round-26 table), so they land with the committed
  table `corpus/evidence/round-27/c1/table.tsv` and the counter's pass (16 of 16 rows, exit 0).
- Draft E lands with the C2 checker's pass (24 of 24 round-26 envelopes, 3 of 3 red
  envelopes, exit 0) and the tool's own run receipts; the Capabilities table's own footer
  rule is that a row is entered only for a round that demonstrated the capability running.
- The knowledge entry, the SOURCES rows (`S081`, `S082` — the L1 assigns which is the
  second carrier's provenance and which is the 6.7.0 package root) and
  `corpus/lessons/round-27.md` `## Gate` are other seats' work.

## Findings

1. Observation (2026-10-22T14:57Z, `sha256sum`): the two renamed copies are byte-identical
   to their carriers — `jq-r27-renamed.dat` and `/usr/bin/jq` both
   `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`;
   `tinyxxd-r27-renamed.dat` and `/usr/bin/tinyxxd` both
   `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`. The renamed files
   are mode `r-xr-xr-x`; not modified by me.
2. Observation (read-only, wave-1 sibling reports, not committed, not verified by me):
   `.ufo/waves/round-27/w1/RunTxA.md` reports `analyze` and `inspect` on `/usr/bin/tinyxxd`
   as rename-sensitive, with the single differing hashed leaf at
   `.data.normalized_result.document` (`target-7b1e5d0c970a.bin` against
   `target-7b1e5d0c970a.dat`), that is, the file extension reaches the hashed projection;
   `.ufo/waves/round-27/w1/RunJqB.md` reports `decompile` and `xrefs` on `/usr/bin/jq` as
   content-keyed across the rename. If the committed table confirms this, the round-27
   result is that the round-26 "seven content-keyed verbs" are content-keyed only while the
   extension is unchanged. The drafted `<V2>` placeholder carries that wording; the L1
   fills it from the table, not from these reports.
3. Observation: the round-26 map row at `corpus/README.md:75` keeps the clause "different
   file names not tested". Append-only forbids editing it, so that clause stays true of
   round 26 and is stale as a current statement; the new row and the Known-gaps sub-bullet
   carry the round-27 answer. A rewrite of line 75 is a lane decision, not mine.
4. Inference: because the renamed copy moves directory, file name and extension together,
   a rename-sensitive verdict cannot attribute the change to the name rather than to the
   extension or the directory. jq's directory-only control is the round-26 table; tinyxxd
   has none; neither carrier has a name-only or extension-only control. Recorded as a limit
   in every drafted line rather than as a claim.
5. The round-26 planned move at `SCORECARD.md:3081` ("a renamed-copy and second-carrier
   extension of the identity table (does a different file name or extension change the
   seven content-keyed ids; one non-jq ELF)") is what R27-C1 measures. The line that
   discharges it belongs to the L1's round-27 SCORECARD section, which I did not draft.
6. There is no capability row for R27-C1: the C1 counter is a checker over committed
   envelopes, not a capability runnable on new material, and round 26 added no capability
   row either.

## Touched surfaces

- Read: `corpus/README.md`, `PROVINCE.md`, `SCORECARD.md` (headings and line numbers),
  `corpus/SOURCES.md` (last id `S080`), `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`,
  `tools/round-27/c1-rename-identity.py` (frozen `table.tsv` header),
  `.ufo/waves/round-27/claims.json`, wave-1 sibling reports `RunTxA.md` and `RunJqB.md`.
- Read-only git: `git show ebe2cb4a`, `git show 08c7a729`, `git log`, `git rev-parse`,
  `git status` (read-only; no write, no `jj`).
- Wrote: this report only, at `.ufo/waves/round-27/w1/ProvinceMap.md`.
- Not written: no lane file, no corpus file, no tools file, no SCORECARD/PROVINCE edit.

## Out of scope (not done by me, by contract)

- No calibration claim: the 11 stale SCORECARD statements disclosed at `SCORECARD.md:3075`
  are the L1's hygiene item (frozen `not_claimed` list in `claims.json`).
- No REA call, so no verdict of my own; no claim about other pins, MCP sessions, parameter
  values, error envelopes or other verbs.
- The knowledge entry body, the SOURCES rows, the round-27 lesson `## Gate` and the
  round-27 SCORECARD section are other owners' work.

## Artifacts

- `/fast/scratch/hyaku/kaidoku-r27/seats/ProvinceMap/draft.md` —
  sha256 `ab4d92c63653e7f48b8dde9cfe77957eafd487109c3af2e154f6c584813eab3a`, 201 lines,
  written 2026-10-22T14:58Z. Holds the six drafted lines verbatim, the placeholder legend
  (`<V1>`, `<V2>`, `<R1>`), the fill commands, the landing gates and the wave-1 material
  that may fill the placeholders.

## Tooling

No install, no upgrade, no `pacman` transaction, no `uv`/`npx`/`cargo` install was needed or
run by this seat. No new tool was introduced.
