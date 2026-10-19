# EX-44 — after-state artifact (C3 freshness, arc3-loop1-round3)

Seat: EX-44, chain c3, role executor (after-state). Task: after EX-41's landing,
independently run the citation-drift probe in both modes (findings = 0) and
record the entry-count delta. All evidence in this directory; scratch under
`/var/tmp/arc3r3-EX-44` (never `/tmp`).

## Revision measured (rule #14)

- HEAD: `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (unchanged all round).
- Probe: `.ufo/gates/citation-drift/citation-drift-probe.py`, sha256
  `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`
  (byte-identical before/after; not revised).
- Final landed pair: `pointer-table.json` sha256
  `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7`
  (30,348 B); `expected.json` sha256
  `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2`
  (2,154 B). Measured 2026-10-19T13:15:00Z.
- Mid-flight revision caught: pass 1 (13:12:54Z) graded expected.json sha
  `179db3c74882624573ef3017b66440716821d5309485a4f54f55a12c1301e2b2`
  (pin already `bfc42f1b…`, MATCH); EX-41's final expected.json rewrite landed
  35 s later. Pass 1 output kept at `after-proof.pass1.txt`; pass 2 re-ran the
  full battery on the final revision (`after-proof.txt`). Both passes: probe
  clean in both modes; table bytes identical across the two passes
  (`landed-identity.txt`).

## Before → after measurement

| quantity | before (13:06:47Z) | after (13:15:00Z) |
|---|---|---|
| table entries | 31 | **57 (+26)** |
| quoted | 4 | 4 (unchanged) |
| exempt | 3 | 8 (+5) |
| table sha256 | `738b3a56…` | `bfc42f1b…` |
| expected.json sha256 | `ff47bfd6…` | `d97dd60a…` |
| expected pin == table | MATCH | MATCH (re-derived) |
| probe default mode | reported findings=0 exit 0 | reported findings=0 exit 0 |
| probe strict mode | clean findings=0 exit 0 | clean findings=0 exit 0 |
| selftest | 13/13 exit 0 | 13/13 exit 0 |

Commands: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .`
and `… --root . --strict` (TMPDIR=/var/tmp/arc3r3-EX-44/tmp); before evidence
`before-probe.txt`/`before-selftest.txt`, after evidence `after-proof.txt`.
Pin re-derivation cross-checked with EX-46's `pin-check.py` (their tool sha256
`1c8067e6…`): `PIN_CHECK: VERDICT MATCH` (in `census-and-pin.txt`).

Delta composition: 26 new entries; removed entries/quoted: none; the retained
31 entries show **zero field drift** (kind/file/line/pattern/target/groups/
must_match/window/pin_line/stamp/rev compared, none changed — `after-proof.txt`
§RETAINED-entry). Every new entry's citing file and target resolves as a Git
object at HEAD (list in `after-proof.txt` §target resolution). `expected.json`
vs HEAD differs only in `pointer_table.sha256`: `frozen_run`, `snapshots`,
`selftest` byte-identical (`diff` of `git show HEAD:…expected.json` vs landed).

## Attacks / refutations (all run; verdicts)

1. **Frozen-run guard live** — one-byte-appended table copy vs the real pin:
   `pointer_table_tampered … d9d81e9c… != pinned bfc42f1b…`, exit 2.
   VERDICT: guard live on the landed pair.
2. **Non-vacuity of "clean"** — dead rev `deadbeef…`: exit 2
   `revision_unresolvable`. VERDICT: the clean verdict is rev-sensitive, not
   a short-circuit.
3. **New entries are graded, not skipped** — scratch table (custom pinned
   expected, the r1 custom-table recipe) with 3 new entries'
   `must_match` neutered: probe emits exactly 3 `citation_dead` rows naming
   `arc3r1-entry-r3-offsets`, `arc3r1-entry-r3-stub-mutability`,
   `arc3r1-entry-quality-ids` (`neuter-proof.txt`). VERDICT: live grading
   proven on the landing itself.
4. **Silent weakening of retained needles** — retained-31 field-drift scan:
   none. VERDICT: extension is additive; `entries`/`quoted`/`exempt` prefixes
   preserved (independently corroborated by EX-41's
   `claims/c3/EX-41/05-identity-and-diff.txt` §additive proof).
5. **Census-vs-landing cross-check** (`semantic-map.txt`,
   `census-and-pin.txt`) — EX-43's census ran 17 entry candidates + 1 quoted
   candidate + 5 NO-ENTRY adjudications. By id, 3/18 landed verbatim; by
   (file,line) semantics, **16/17 entry candidates are landed** (13 under
   renamed ids); 10 net-new entries go beyond the census ids (3
   `census-cites-*`, 2 `sc-arc3*` section keys, 4 `custody-readme-*`, and
   `skill-rule14-log-fresh-identity`, which grades the census's quoted
   candidate LOG.md:1411-1412 at SKILL.md:254). One candidate has no
   (file,line) landing: `custody-receipt-v2-tool-self-pin`
   (`.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/capture-pre.txt`) — a
   wave-internal receipt, covered by class per EX-41 dispositions row 28
   (`.ufo/waves/arc3-loop1-round3/claims/c3/EX-41/03-census-dispositions.md`,
   exempt row B "wave-internal citations"). VERDICT: recorded as the one
   residual observation for the chain verdict seat; not ruled a defect here.
6. **Measured-stale round record (spot check of a disposition claim)** —
   `SKILL.md:371` at HEAD holds `## Refuses`; the citation-drift registry row
   moved to `:389`; the round-1 report's `SKILL.md:371` token is stale by
   design (append-only round record, NO-ENTRY). Independently reproduced via
   `git show HEAD:SKILL.md | sed -n '371p'`/`'389p'`. VERDICT: matches EX-41
   dispositions row 5.

## Blockers

None. Standing caveat: all identities above are re-derived at write time and
cover the revision named; any later revision of the pair by EX-41 invalidates
them and they must be re-derived (rule #14).