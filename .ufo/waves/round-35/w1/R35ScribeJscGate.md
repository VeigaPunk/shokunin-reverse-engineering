# R35ScribeJscGate — advisory source Gate quotes (draft, no writes)

Seat: UFO-FSD scribe. Item: "Draft advisory source Gate quotes; no writes."
Lane bounds honored: leaf member (no subagent dispatch); source trees read-only; no
product/corpus/counter/plan/claims/SCORECARD/LOG/report edits; no VCS/index/jj
mutation; no pacman installs; no `find`/`du` under `/fast/scratch`. Test write is
this report (`.ufo/waves/round-35/w1/`), per assignment. `considerthese/` does not
exist in this lane (verified: `ls -d considerthese` → absent) — one report line,
as required by the plan.

Read sources: `plans/round-35-claims.md` (base `aa04633a`), `.ufo/waves/round-35/claims-canonical.json`
(instrument_revision `d2729cba`; counters read the predicate from `claims-canonical.json`
at the freeze revision), `.ufo/waves/round-35/freeze-status.md`, control receipts
`.ufo/waves/round-35/controls/c1-do-nothing.json` + `c2-do-nothing.json`, prep captures
`.ufo/waves/round-35/prep/jsc-sources/` (`jsc2js-readme.md`, `releases-page1.json`,
`releases-page7.json`), `tools/round-35/c1-coverage-counter.py`, `corpus/SOURCES.md`,
`PROVINCE.md`, `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`.

## 1. Advisory Gate quotes (draft, for the two planned entries)

Frozen claims: C1 coverage assimilates `.jsc -> source mapping` via S125/S129; C2
calibration closes round-34 D1-D4. Do not alter predicates/scope. The quotes below are
verbatim from the prep captures (immutable prep artifacts, not downstream edits).

### S125 — jsc2js mapper contract (source: `prep/jsc-sources/jsc2js-readme.md`, the repo README)

Frontier anchor (`PROVINCE.md:147-148`):
> **`.jsc` → source mapping** — Ignition disassembly held; a View8/jsc2js-style
> bytecode-to-source mapper is the next frontier for typora's real app.

Source quotes (capture `jsc2js-readme.md`):
- Overview (lines 117-122, English): "`jsc2js` reverses **V8‑generated JSC bytecode**
  into readable (approximate) JavaScript. The repository contains two major parts:
  1. **Patched d8**: Multiple V8 versions (see Releases) with an added builtin helper
  `loadjsc()` that loads and prints `.jsc` bytecode. 2. **Integrated View8 tool
  (based on a customized fork of suleram/View8)**: Converts the textual bytecode dump
  emitted by d8 into an approximate JavaScript reconstruction."
- Pipeline (lines 128-157): "choose the V8 version that is **identical to** the one
  that produced your target `.jsc`"; `./d8 -e "loadjsc('path/to/xxx.jsc')" > xxx.txt`;
  then `python view8.py --disassembled ../xxx.txt ../xxx.js`; result "contains an
  approximate JavaScript reconstruction based on the bytecode analysis. (Identifiers /
  control flow may differ from the original source; this is a semantic approximation.)"
- Version/limitation notes (lines 172-208): patch set covers V8 5.1 and later; 5.1 is
  the compatibility lower bound (V8 ≤5.0 lacks `CodeSerializer::Deserialize`); "Always
  use a **matching** d8 build"; "Because there is no Node.js environment, the JSC
  compiled by Node.js may not be decompiled normally, while Electron works fine.";
  "JavaScript reconstruction cannot be 100% identical to the original: Variable /
  function names may be missing or replaced. Control flow may be structurally
  reorganized. Constant folding / runtime optimizations are not perfectly reversible."
- Anti-overclaim gate (line 90): "还原 JS 不能 100% 重建原始源码" (reconstruction cannot be
  100% faithful) — the entry must not claim exact source recovery.

### S129 — jsc2js release inventory (source: `prep/jsc-sources/releases-page{1,7}.json`, GitHub releases API)

Observed inventory facts (commands below):
- 177 releases across the two captured pages (page1: 100, page7: 77); zero drafts, zero
  prereleases; every release carries assets.
- Tag/name = the V8 version (e.g. `15.6.75.19`, `12.0.157`); assets per release are
  exactly two: `d8-<tag>-linux.tar.gz` and `d8-<tag>-windows.zip` (the README's
  `d8-linux`/`d8-windows.exe` are display names; actual asset filenames embed the tag).
- Published span 2025-08-24T03:19:17Z → 2026-10-21T08:33:45Z; tags observed span
  V8 12.0.157 → 15.6.75.19.
- Representative release body (`15.6.75.19`, published 2026-10-21T08:33:45Z):
  "Patched d8 for V8 15.6.75.19 (includes d8 + snapshot_blob.bin)." Assets:
  `d8-15.6.75.19-linux.tar.gz` (14,659,433 B) and `d8-15.6.75.19-windows.zip`
  (13,020,015 B), both from `https://github.com/xqy2006/jsc2js/releases/download/15.6.75.19/...`.

### Advisory note for entry authoring (counter mechanics, from `c1-coverage-counter.py`)

- Provenance trio must open each entry: lines matching `^source\s*:`, `^verified-at\s*:`,
  `^recheck\s*:` (regex `(?m)`), and the `source:` line must contain the row id
  (S125 / S129), else `trio_missing_*` / `row_citation_missing` fail.
- SOURCES rows S125/S129 need exactly 11 cells with `status=mined`, `opened=2026-10-25…`,
  `used-by` containing the entry path.
- PROVINCE.md must contain the stems `2026-10-25-r35-jsc2js-mapper-contract` and
  `2026-10-25-r35-jsc2js-release-inventory`; `corpus/README.md` must contain both
  entry filenames.

## 2. Evidence, commands, output

- Lane tip: `git rev-parse HEAD` → `3ecf42981a0b63414de90ade643040d609dbb8a5`
  ("round-35: commit failing do-nothing controls before claim data (C1/C2 exit 1)").
- Do-nothing controls at base `aa04633a` (already committed as receipts; not rerun):
  - `controls/c1-do-nothing.json`: `pass:false`, 8 failing checks — `entry_missing` ×2
    (both planned entries), `registry_row_missing` S125/S129, `province_missing` ×2,
    `readme_missing` ×2. Exit 1 required and recorded.
  - `controls/c2-do-nothing.json`: `pass:false`, 7 failing checks —
    `D1_census_start_missing`, `D2_lesson_missing`, `D3_{source,verified_at,recheck}_missing`,
    `D3_source_not_s106`, `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4`,
    `D4_section_missing:### Round-34 run-6 instrument registry`.
- Instrument/input pins verified against `claims-canonical.json` (sha256 of worktree
  files):
  - `tools/round-35/c1-coverage-counter.py` `e28792c7…` ✓ (matches pin)
  - `tools/round-35/c2-calibration-counter.py` `576c14dd…` ✓ (matches pin)
  - `plans/round-35-claims.md` `45b644a4…` ✓ (matches pin)
  - `.ufo/waves/round-35/assimilation/census-start.txt` `b6ce2b17…` ✓ (matches `frozen_inputs`)
- Predicate/claims path: `git show 2323d197:.ufo/waves/round-35/claims-canonical.json`
  contains C1/C2; worktree file is byte-identical to commit `2323d197` (cmp). The c1
  counter reads `.ufo/waves/round-35/claims-canonical.json` at the freeze revision, and
  exit 2 if absent/unparseable/predicate-mismatched.
- Freeze order (from `git log`): `d2729cba` (prep: census-start receipt, captures,
  counters, plan) → … → `2323d197` (canonical claims) → `3ecf4298` (do-nothing control
  receipts). `corpus/SOURCES.md` last changed at `417a8211` (round-34) — no SOURCES
  change after base yet, so D-1's "commit before first SOURCES change" ordering is
  satisfied by the current history, and `census-start.txt` carries `rows=106`, `EXIT=0`,
  `9 W04 warnings` (verified in the receipt text).
- Freeze debt disclosure: `freeze-status.md` records the round-34 gate reject at
  `f1ea3a6d` (`INSTRUMENT_REVISED`, pins at `13d7a815` vs final counter bytes) and the
  canonical supersession; `claims-canonical-note.md` states counters' selftests passed
  green/red immediately before the candidate was written.

## 3. First falsifications (observed, not scored)

At current lane state (measured revision base `aa04633a`, control receipts committed at
`3ecf4298`), both claims fail as designed — do-nothing control must fail; nothing is yet
claim-eligible:
- C1: both knowledge entries absent; S125/S129 rows absent; PROVINCE lacks both new
  stems (only the Frontier bullet at `PROVINCE.md:147-148` exists); `corpus/README.md`
  coverage map lacks both filenames.
- C2: round-35 lesson (`corpus/lessons/round-35.md`) absent; the r34b knowledge entry's
  front-matter uses `sources:`/`revisions:` headers, not the appended provenance trio
  (`source:`/`verified-at:`/`recheck:` citing S106) — D-3 fails at base; SKILL.md
  round-32 instrument-registry rows have 4 cells (need 8) and the round-34 run-6
  instrument-registry section is absent — D-4 fails at base.
- No claim can be scored on anything authored after the freeze for its own data set;
  the measured revision must be a committed tree ref.

## 4. Limits

- Scribe role: advisory evidence only; no counter runs at the measured revision were
  performed (control receipts are the committed ground truth), no score computed, no
  verdict asserted on the eventual claim outcome.
- Captures are prep artifacts; the entry/row content they would feed is not written.
- The release pages are API captures as of prep (2026-10-25); later upstream release
  activity is not in scope.
- Checks above are advisory; the canonical judge is the frozen counter + kill rule.
