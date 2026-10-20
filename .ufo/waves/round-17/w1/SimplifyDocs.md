# Simplify — r17 Go entry: redundancy map and minimal cross-reference set

Seat: KaidokuR17.SimplifyDocs-3 (author-side advisory, leaf). Read-only: only this
report was written. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier
execution; `inspect-go-binary` and `--help` only. Tree is baseline `b563c799` except
untracked `.ufo/waves/round-17/` (`git status --porcelain`; `git diff --stat b563c799
-- SKILL.md corpus/knowledge corpus/lessons` empty), so every anchor below is
baseline text. The ticket's `SKILL.md:455-507` is off by one: the Go surface starts
at the heading `SKILL.md:454` and ends at `:507`.

## What I searched

- `SKILL.md:454-507`: three Go sections (r14, r15, r16) plus three registry rows.
- `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (129 lines),
  `-r15-go-snapshot-inventory.md` (94), `-r16-go-selection-preview.md` (97).
- The live r17 draft `.ufo/waves/round-17/w1/draft-knowledge-r17.md` (143 lines)
  and its report `DraftKnowledgeEntry.md`.
- Supporting: `corpus/lessons/round-16.md`, `round-16-verifier-spotcheck.md`,
  `corpus/SOURCES.md` S003/S023, `.ufo/waves/round-17/contract.md`, pilot logs.
- Bounded negative: `PROVINCE.md` and `README.md` contain no Go law to deduplicate
  (`grep -n 'Go RTTI|Go snapshot|Go bootstrap|Go API snapshot' PROVINCE.md README.md`
  → none). Duplication is confined to SKILL + knowledge + the r17 draft.

Anchor shorthand below: `r14` = `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`,
`r15` = `...-r15-go-snapshot-inventory.md`, `r16` = `...-r16-go-selection-preview.md`,
`draft` = `.ufo/waves/round-17/w1/draft-knowledge-r17.md`, `SKILL` = `SKILL.md`,
`contract` = `.ufo/waves/round-17/contract.md`.

## Direct answer

1. The r17 entry needs **no** restatement of the r14-r16 law. Seven anchors (below)
   cover every inherited predicate; the entry's own payload is the two carriers,
   three observed log facts and the prediction/observation comparison.
2. The current draft repeats inherited law in 4 of its 8 sections
   (`draft-knowledge-r17.md:25-45`, the predicted column at `:82-100` duplicating
   `:42-45`, `:122-126`, and 5 of 14 bullets at `:128-143`). Roughly 45-50 of 143
   lines carry no new observation; the same claim set fits in ~55-60 lines.
3. SKILL has grown one Go section per round and now states the same caveats up to
   11 times (table below). r17 must not add a fourth section-shaped law block; one
   short section + one registry row is the ceiling.

## Redundancy map (occurrence counts are textual sites, not weights)

| # | Predicate already held | Sites (path:line) | Owner r17 must cite |
|---|---|---|---|
| P1 | Base is requested at patch 0; missing base → `EMPTY`; no earlier-minor fallback | r14`:35-38`, r14`:76`; r15`:17`, r15`:29`; r16`:19`; SKILL`:483` (6) | r14`:35-38` |
| P2 | One downward patch-diff search within the same minor | r14`:38`; r15`:19`, `:30-31`; r16`:21-23`; SKILL`:481`, `:494-495`, `:499` (7) | r16`:21-23` |
| P3 | Requested-version label ≠ selected data bytes | r15`:5`, `:21`, `:31-32`; r16`:24`, `:40`; SKILL`:477`, `:481`, `:494-495`, `:500` (9) | r15`:21` |
| P4 | Generic `all` bucket survives; platform-key absence is not an empty snapshot | r14`:51-54`, `:121-127`; r15`:15`, `:23`, `:33`, `:46`; r16`:25`, `:28`; SKILL`:464`, `:482`, `:502` (11) | r14`:121-127` |
| P5 | Selected diff/base is hashed, not parsed or applied | r14`:126`; r15`:19`, `:30`, `:74`; r16`:21`, `:23`, `:38`, `:40`, `:49`; SKILL`:499`, `:501` (11) | r16`:38-40` |
| P6 | S003/S023 share an installation origin; archive not authenticated against loaded classes | r14`:96-97`; r15`:13`; r16`:44-45` (3) | r16`:44-45` |
| P7 | Historical `op` cause UNKNOWN; r4-10 supersession stands | r14`:83-90`; r15`:9`; r16`:11`; SKILL`:468-470` (4) | r14`:83-90` |
| P8 | No target execution, no new Go capability | r14`:88`; r15`:43`; r16`:52`; SKILL`:469-470` (4) | r14`:88` |
| P9 | Probe/selfcheck is not a conformance gate | r15`:44`; r16`:34`; SKILL`:487`, `:506` (4) | r16`:34` |

Two further duplications matter because they **caused** routed defects:

- **Command retyping.** The r15 inventory argv exists in two spellings: the drifted
  relative `recheck:` at `r15:3` and the corrected absolute block at `r15:83`,
  requiring the whole `Round-16 correction` section `r15:76-94`; the corrected
  spelling is again in SKILL`:487`. r16 got this right: argv once at `r16:3`, then
  referenced at `r16:78-79` ("differs from `recheck:` only by `--request 1.24.5`").
  Rule for r17: define each argv once (registry row or `recheck:`), reference by
  name everywhere else.
- **Preamble scope drift.** `SKILL.md:440-443` says the rows below register four
  named tools, but the registry now has seven rows: the four at `:447-450` plus
  `go-snapshot-inventory` at `:487`, `go-selection-preview` and
  `round16-structural-controls` at `:506-507`. The three Go rows are outside the
  preamble's stated enumeration. Adding r17 rows as a fourth table compounds it.

## Minimal cross-reference set (use these seven; write nothing else about the class)

| Anchor | Covers | Permitted r17 use |
|---|---|---|
| X1 `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:31-50` (+ table `:73-79`) | range advisory, bootstrap-conditional, `EMPTY` branch | one sentence: "branch law per r14:31-50" |
| X2 `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:61-74` | installed bases/diffs and per-request results | cite for "no base above 1.25"; do not re-list `go1.15.0…go1.25.0` |
| X3 `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:17-26` (+ tool contract `:34-40`) | request-bounded selection, `patch_applied:false`, label law application | cite for the selector semantics; r17 prints only its two computed results |
| X4 `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:42-52` | shared limits (same origin, unauthenticated archive, source model ≠ Java) | one limits bullet: "shared limits: r16:42-52" |
| X5 `SKILL.md:485-487` and `SKILL.md:504-507` | command definitions | registry row defines argv once; the entry's `recheck:` names the row |
| X6 `corpus/SOURCES.md:9` (S003), `:29` (S023) | paths, digests, `used-by` | header cites `S003`/`S023` tokens + member names only |
| X7 `.ufo/waves/round-17/pilot/README.txt` + `SHA256SUMS` | pilot facts and capture limit | one header sentence "PILOT, not measured" + cite |

`recheck:` should be **one** command, not the draft's four (`draft:3`): the
receipt-validating argv (`receipt-validate.py` over `W/runs/*/receipt.json`)
recomputes every recorded sha256, so the separate `sha256sum`,
`inspect-go-binary` and `selection.py` re-runs are already covered by the retained
receipts (contract `carrier-run.py` step 2 and `receipt-validate.py`).

## r17-unique content — state each exactly once

- **Version-normalization precondition (new).** `GoBuildInfo.java:488-490` strips
  the leading `go`; `GoVer.java:65` then cuts at the first non-`[.0-9]` character.
  `GoVer.parse` alone maps `go1.27.0-X:nodwarf5` to `INVALID` (`GoVer.java:67-68`);
  the draft already proves this by re-evaluating the regex (`draft:29-31`). Keep;
  it is the one genuinely new source fact.
- **Computed selections (new).** 1.27.0 → `missing_base`; 1.23.12 →
  `exact_diff`, base `go1.23.0.json`, patch 12 (`w1/selection-1.27.0.json`,
  `selection-1.23.12.json`). Two rows, not a re-derivation.
- **Observed log facts (new).** Untested `[1.27.0]` then bootstrap WARN then
  `unable to get GoRttiMapper` (`pilot/shfmt-log/ghidra.log:83-85`), repeated for
  the string analyzer (`:86-89`); snapshot labels at
  `pilot/esbuild-0.25.12-log/ghidra.log:63-64` and `Go version` at `:67`.
- **Failure-tail ordering (new).** `GolangSymbolAnalyzer.java:139` follows the
  `:133-136` early return, so a failed carrier logs no `Go version` line; cite the
  string analyzer separately at `GolangStringAnalyzer.java:103-105` (the draft's
  `:88` attributes both messages to the symbol analyzer's `133-137`).
- **Unpredicted lines (new, bounded).** three `GoTypeManager` subtype WARNs
  (`:68-70`), `Missing Go type names: 19` (`:85`). One bullet each, UNKNOWN cause.
- **Capture limits (new).** polling copy can miss post-poll lines; REA deletes its
  runtime root (contract `carrier-run.py`, `log_capture_limit` field). One bullet.
- **Pilot boundary (new).** pilot logs carry no pre/post pins
  (`pilot/README.txt:6`), so they are ineligible for the C2 count.

## Concrete cuts to `draft-knowledge-r17.md`

| Lines | Issue | Action |
|---|---|---|
| `3` | four `recheck:` commands | one receipt-validating command |
| `25-39` | re-derives r14/r15/r16 law (P1-P5, P7) | keep item 1; compress 2/3/5 to one sentence each; replace item 4's law with the two selection rows |
| `42-45` | predicted values duplicate the `predicted` column at `:84-100` | delete one of the two |
| `58-60`, `71-72` | two `script.log` REA-bridge lines and four `binary_overview` counts, which the draft itself calls non-Go evidence | keep at most one script.log line; delete the counts (already in retained JSON) |
| `87`, `98`, `113-120` | per-row classification labels plus a section repeating the same labels | one label-convention sentence; keep the three UNKNOWN bullets and the unpredicted-WARN row |
| `122-126` | "Corrections" contains no correction; `:125` is self-contradictory — "Not previously stated: the r14 rule that … yields EMPTY", which r14`:35-38` already states | delete the section; the normalization precondition is new content, already in item 1 |
| `128-143` | 14 bullets; 5 restate r14/r16 limits (P6-P8), not new | keep 5 new limits + one cross-ref to X4 |

Resulting entry ≈ 55-60 lines with every new observation retained; the current
143-line draft would make r17 the longest Go entry while adding the least new law.

## Calibration findings

**F1 (calibration, high) — a temporal-stability claim escapes the C1(a) sweep.**
`contract.md:91-93` defines sweep sites as LOG.md, SCORECARD.md,
`corpus/lessons/round-16.md`, SKILL.md and `round-16/verification.json`. It omits
`corpus/knowledge/`, yet `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95-96`
reads "Producer and fixture pins were unchanged during the run." (the same class of
statement as `corpus/lessons/round-16.md:154`, which *is* caught). The sweep can
report `unqualified: 0` while this site remains uncorrected. Fix: add
`corpus/knowledge/*.md` to the site definition or pass that file via `--extra`
(contract already supports `--extra`). The r17 entry must not contain the phrase
at all; the honest wording is the contract's own: "same bytes at two instants", never
"unchanged throughout" (`contract.md:20`).

**F2 (calibration, medium) — false-novelty phrasing.** `draft:125` labels a
restatement of r14`:35-38` as "Not previously stated". Delete, per the cuts table.

**F3 (calibration, medium) — pilot artifacts do not bind the version.**
`pilot/shfmt.json` and `pilot/esb.json` are `operation: binary_overview`
(`normalized_result` = document/segments/counts); the go versions live only in
`pilot/README.txt:7-8` and the drafts. The draft's shfmt evidence id
`ev_f8ef12a805…` is reproducible — my own allowed `inspect-go-binary /usr/bin/shfmt`
returned the same id and `go1.27.0-X:nodwarf5` — but no pilot file is the
inspect-go artifact. FINAL runs must retain `DIR/inspect-go.json`
(contract `carrier-run.py` step 2); the entry must not call the pilot's README a
receipt.

**F4 (calibration, medium) — the contract's predictor instruction is incomplete.**
`contract.md:62-66` says to normalize "exactly as Ghidra's `GoVer.parse` would" and
points at `GoVer.java`. `GoVer.parse("go1.27.0-X:nodwarf5")` returns `INVALID`; the
`go` strip is at `GoBuildInfo.java:488-490`. An executor implementing the contract
literally exits 2 on both carriers. The draft caught this (`draft:29-31`); the
contract text should cite `GoBuildInfo.java:488-490` first. Flagged for L1, not
edited (read-only seat).

**F5 (depth, medium) — `snapshot_label` is a requested-version echo, not a
selection test.** The esbuild pilot log prints only the requested label
(`esbuild…log:63-64`), and the shfmt log prints none; no line names the selected base or diff. Since Java passes
the original `GoVer` to `read` (`r15:21`), an observed `1.23.12` would appear even
if a fallback diff had been used. The comparison therefore confirms label
propagation and the missing-base branch, not that the selector chose
`go1.23.12.json.diff`. No fallback-diff carrier exists among the host binaries I
sampled: `/usr/bin/{op,shfmt,docker,containerd,dockerd,gh,yay,lazygit,gitleaks,runc,fzf}`
are 1.26.x/1.27.x (out of range, missing base), and the esbuild builds are
0.25.12 = 1.23.12 and 0.21.5 = 1.20.12, both `exact_diff` per
`w1/selection-*.json`; 0.27.7 has `build_info: null`. The entry should say this in
one limit line and avoid claiming the run validates the selector.

**F6 (depth, low) — the third C2 carrier is cheap and relevant.**
`/usr/bin/op` is 1password-cli 2.41.0-1, `go1.26.8`, evidence
`ev_4279a4264ab81b1511b5ce263eeed288474fddf180f019008ca1ece2a23f69f4`. It gives
the third receipt and ties to r14's held `op` task, but its prediction is the same
`missing_base` branch as shfmt; the entry must not present it as the historical
`op` pair's cause. (Alternative: esbuild 0.21.5, `go1.20.12`, evidence
`ev_5c06eceff96ee9f44596daacb182839e8ab629d1b1b8926f187cfafaddae43f7`.)

## SKILL delta (recommended ceiling for the r17 section)

- One section, ≤3 table rows, each a *new* discriminator: (a) version
  normalization precondition, (b) failure tail (`unable to get GoRttiMapper`, no
  `Go version` line), (c) capture limit. No row restating range/bootstrap/`all`/
  label law.
- One registry row for the carrier pipeline entrypoint; group `pins`/`retain`/
  `log-extract`/`predict`/`compare` under it by receipt field, rather than five
  near-identical rows each repeating absolute paths.
- Do not add to the three existing `all` caveats (`SKILL:464`, `:482`, `:502`) or
  the three label-law restatements (`SKILL:477`, `:481`, `:494-495`). Either the
  r17 section applies them in its table or it does not mention them.
- Optionally fix the registry preamble (`SKILL:440-443`) to say "the rows below and
  the per-round Go rows" so the table split stops being a documentation defect.

## Bounded no-findings

- No Go law in `PROVINCE.md` or `README.md` to deduplicate.
- `corpus/SOURCES.md` holds paths/digests only (`S003` line 9, `S023` line 29); it
  does not restate the selector law, so no cross-entry collision there.
- SKILL's Go decision tables are projections, not copies, of the knowledge tables
  (3/7, 4/8, 4/5 rows); the duplication is in the caveat columns, not the rows.

## Evidence and commands (observed)

- Reads: SKILL.md 454-507; r14/r15/r16 entries; `draft-knowledge-r17.md` +
  `DraftKnowledgeEntry.md`; `round-16.md`; SOURCES S003/S023; contract; pilot logs.
- `sha256sum -c pilot/SHA256SUMS` → OK for all six files.
- `npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json` →
  `go1.27.0-X:nodwarf5`, `ev_f8ef12a805…` (matches the draft). Same verb on
  `/usr/bin/op`, `/usr/bin/docker`, `/usr/bin/containerd`, `/usr/bin/dockerd`,
  `/usr/bin/gh`, `/usr/bin/yay`, `/usr/bin/lazygit`, `/usr/bin/gitleaks`,
  `/usr/bin/runc`, `/usr/bin/fzf`, and esbuild 0.21.5 / 0.27.7 (versions above).
- Read-only `zipfile` reads of S003 members: `GoVer.java` 46-81, `GoBuildInfo.java`
  226-246/470-494, `GolangSymbolAnalyzer.java` 128-142,
  `GolangStringAnalyzer.java` 103-105/120-150, `GoRttiMapper.java` 76-82/110-128/
  166-184/348-368.
- `pacman -Qo /usr/bin/op /usr/bin/shfmt` → 1password-cli 2.41.0-1,
  shfmt 3.14.1-1 (read-only).
- Tool installs: none. `npx` may have populated its cache on first fetch.

## Limits of this report

- Occurrence counts are textual; two anchors can encode one predicate in different
  words, and the count is not a semantic weight.
- I did not run `analyze`, so all observed log lines are the pilot copies; the
  final runs may differ.
- The suggested ~55-60-line target is an estimate from section sizes, not a
  measured rendering.
- Nothing here judges r17's admission or promotion; it is a redundancy and
  calibration input to L1.
