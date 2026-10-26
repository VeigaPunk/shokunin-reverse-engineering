# R38ConnSiblingOverlap — sibling-lane overlap scan for round-38 surfaces

Seat: R38ConnSiblingOverlap (connector, leaf; read-only). Date: 2026-10-26.
Wave: round 38, wave 1. Integration owner: L1 KaidokuR38.
Report path (lane-relative): `.ufo/waves/round-38/w1/R38ConnSiblingOverlap.md`

Scope: scan the 16 named sibling lanes under `/home/vgpnk/Projects/shokunin`
(kake, chousa, mado, tsukuroi, kumitate, kengaku, tabi, souji, kama, mori,
kotoba, kotodama, revenger, tameshi, kasegi, kagi) for ground overlapping this
round's scored surfaces — R38-C1 (standard big-endian SquashFS v4 through
sasquatch / unblob 26.6.4 `squashfs_v4_be` / REA `extract-firmware`,
Frontier → Core) and R38-C2 (self-assessment pointer calibration across
SCORECARD/SHONEN/PROVINCE) — plus the SOURCES-registry surface the routed
defects touch (R37-CL2). Cite, never absorb; flag duplicable ground.

## Axes (named)

The round's judged axes per the assignment: **coverage** (R38-C1) and
**calibration** (R38-C2). The proposed move below is scored against these two
only; depth/operability/freshness/adjacency are untouched by any finding here.

## Method

- Read-only grep sweeps (the `grep` tool, case-insensitive) over each sibling
  lane root for `squashfs`, `sasquatch`, `unblob`, `extract-firmware`,
  `squashfs_v4|v4be|big.?endian`, `pointer counter|pointers resolve|
  self-assessment|unresolved pointer|backticked`, `self-assessment|self
  assessment` (scoped to sibling SKILL.md/LOG.md/corpus), and `SOURCES.md`
  (same scope). Sibling `corpus/SOURCES.md` files grepped directly for
  `unblob|squashfs|sasquatch|freetz|avm`.
- Direct verification reads of every load-bearing citation (paths below).
- No installs, no network fetches, no writes into any sibling, no git/jj
  mutation anywhere. Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ConnSiblingOverlap`
  created and removed; nothing cited lives only in scratch.
- Limits: the fleet-wide sweeps paginate (e.g. "files 1-20 of 209+"). Later
  pages were pattern-deduplicated, not read file-by-file; every distinct match
  class is represented in the pages shown. Hit counts below are therefore a
  lower bound per class, and each class is classified by content, not count.

## Surface inventory (this round, from plans/round-38-claims.md)

- C1 carriers/oracle: `corpus/evidence/round-37/c1/K{1..4}` + `carriers.json`;
  claim receipts land at `corpus/evidence/round-38/c1/K*/after.json`; counter
  `tools/round-38/c1-counter.py`; harness `tools/round-38/c1-run.sh`.
- C1 knowledge/registry targets: `corpus/knowledge/2026-10-26-r38-sasquatch-be-
  squashfs-recursion.md`, PROVINCE round-38 Core row + frontier-note
  supersession of `PROVINCE.md:156-157` (sasquatch bullet; verified live:
  bullet reads "big-endian/AVM stays here"), and the `sasquatch-v4be` aside at
  `PROVINCE.md:372` (round-36 Core row; verified live).
- C2 counter: `tools/round-38/c2-counter.py` — frozen predicate: every
  backticked lane-repo pointer in SCORECARD `## Owned axes` + `## Capabilities`
  rows, SHONEN boxes, PROVINCE `## Core`/`## Frontier` rows resolves (path
  exists, line range inside file); four stated counts equal command A/B counts;
  three section ranges equal heading-to-last-non-blank ranges; no unit removed;
  no fewer pointers than base; base mismatches repaired to the same document.
  Base state: 1 mismatch (`evidence/doctor/` in the PROVINCE Core `REA MCP
  server` row).
- SOURCES gate: C1 entry must cite a `corpus/SOURCES.md` row opened 2026-10-26;
  R37-CL2 routes `avm.txt` / `be-squashfs_v4{,.nopad}.bin` provenance through
  that gate.

## Findings — C1 extraction surfaces (coverage axis)

**Verdict: no sibling lane holds or is building any part of this ground.**
No sibling claims sasquatch, sasquatch-v4be, big-endian SquashFS v4, the
`squashfs_v4_be` handler, or REA `extract-firmware` results. Every hit in the
sweeps is one of six non-ground classes:

1. **Read-only captures of kaidoku's own bytes.** The densest hits are
   `tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kaidoku/
   {8451e4710954,d1d981d2cc04}/PROVINCE.md` — snapshots of this lane's
   province at two commits, including the sasquatch frontier bullet
   (`:147`), the `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4) firmware
   row (`:123`), and the AppImage unblob/squashfs carve row (`:131`).
   These are kaidoku ground observed from tsukuroi, not tsukuroi ground.
   Live tsukuroi files carry **zero** sasquatch/unblob/squashfs matches
   (scoped grep over tsukuroi PROVINCE/SKILL/LOG/SCORECARD/corpus: no hits).
2. **Fixture copies of a frontier-queue line.** `souji-shokunin/census/
   round-26/waves/assimilation/validate/tests/vault/fixture-src-*/
   atlas-dir-*/Frontier-Queue.md:7` (13+ copies shown, pattern repeats):
   "sasquatch build (AUR) → unblob squashfs recursion (7z fallback works
   today)" — souji assimilation *test fixtures* snapshotting a queue file;
   not souji-held ground.
3. **Prior connector scan.** `kengaku-shokunin/.ufo/waves/round-26/build/
   ConnRosterScan.md:16,39` (duplicated in two round-28 scratch exports):
   kengaku already scanned sibling PROVINCE files, found kaidoku's sasquatch
   line, and ruled "unrelated filesystem/archive extractor… VERDICT: No
   competing lane ownership appears in the scanned PROVINCE files; the sole
   cross-lane hit is Kaidoku's unrelated squashfs extractor." Prior art for
   this seat's verdict, from the response-extraction side.
4. **Fleet-root debris analyses.** `kake-shokunin/.ufo/waves/round-50/w1/
   SentinelWriteScope.md:122`, `round-51/w1/ScoutMisroot.md:39`;
   `mado-shokunin/.ufo/waves/round-32/w1/reports/SentinelScope.md:39`,
   `round-34/w1/reports/SentinelScope.md:38-39`; `chousa-shokunin/.ufo/waves/
   round-44/seat-logs/W2ConnSibling.log:4107` — seats cataloguing a stray
   `unblob.log` (`file=/tmp/test-fw.bin`) dropped at the fleet root by an
   unrelated tooling run. Hygiene records, not extraction ground.
5. **Host-tooling plane.** tsukuroi `.ufo/waves/round-24/w1/ExecMirrorTimestamps/
   *-pkglist.txt` (`squashfs-tools 4.7.5-1`), `round-38/w1/C2ExecLogOracle/
   log-order.json:2327` and `round-39/frozen/txcapture/pacman.log:3192`
   (pacman installing squashfs-tools); `mado-shokunin/.ufo/waves/round-19/w2/
   reports/AtkInstallsRecord.md:42` (unblob 26.6.4 in a `uv tool list`
   install-inventory record); tsukuroi round-29/36 `NEWS-v262*` systemd
   mentions. Package health/inventory only. Note: unblob 26.6.4 and
   squashfs-tools 4.7.5 are shared host tools whose versions kaidoku's own
   rows pin; sibling inventories do not assert any extraction result.
6. **The revenger fence (the one live adjacency).** `revenger-shokunin` has
   run three rounds of overlap arbitration against this lane's firmware
   surface, all "reported, not absorbed":
   - `.ufo/waves/round-63/build/R63ConnectorOverlap.md:36,42` — names
     kaidoku PROVINCE.md:76-79 (firmware pruned into Core) and `:125`
     (`inspect-firmware-regions` / `extract-firmware` rows; binwalk 3.1.0 /
     unblob 26.6.4) and instructs revenger's C2 to neither restate kaidoku's
     GSP counts/evidence ids nor run `extract-firmware`.
   - `.ufo/waves/round-64/R64ConnectorOverlap.md:14-16,45` — ADJ-06 remains
     open; the proposed entry's Q10 sentence must name kaidoku's rows "not
     absorbed", and revenger's README frontier note naming the same two verbs
     and the same pins must not be promoted into an admitted entry
     ("second-order, same verb and same pin").
   - `.ufo/waves/round-65/R65ConnectorOverlap.md:16` + `corpus/knowledge/
     round-64-firmware-region-byte-evidence.md:203` — the landed fence
     sentence, naming `kaidoku-shokunin/PROVINCE.md:50,76-79,125` and the
     pin registry `:64-71` as not absorbed, ADJ-06 unresolved.
   - `corpus/SOURCES.md:101` — revenger's only registry touch: "REA firmware
     guide (docs/firmware-analysis.md, Binwalk 3.1.x / Unblob 26.6.x
     requirement) — read by the scout, not yet a row; open it when the
     firmware family is claimed."
   ADJ-06 status verified live: `tsukuroi-shokunin/PROVINCE.md:51` (ADJ-06
   row, recipient "protocol integrator — kaidoku/revenger ownership
   unresolved… Request an ownership ruling before any RE work") and
   `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:42` region (tsukuroi
   round-1 question asking to arbitrate the kaidoku/revenger shipped-artifact
   overlap before an ADJ-06 analysis is routed). `mori-shokunin/PROVINCE.md:
   12-14` refuses driver/firmware outright (→ tsukuroi). The l0 question and
   the tsukuroi/mori fences mean the ownership question around the firmware
   *verb family* is contested fleet ground; the specific BE-SquashFS-v4
   ground underneath C1 is not claimed by anyone but this lane.

**Cross-registry SOURCES check (R37-CL2 surface).** All 17 lanes
(16 siblings + kaidoku) hold a `corpus/SOURCES.md` (sibling sizes: kake 275,
chousa 322, mado 480, tsukuroi 320, kumitate 285, kengaku 163, tabi 178,
souji 252, kama 491, mori 328, kotoba 380, kotodama 936, revenger 102,
tameshi 486, kasegi 105, kagi 192 lines; kaidoku 213). Grep of all sibling
registries for `unblob|squashfs|sasquatch|freetz|avm`: the only hits are
revenger:101 above and kotodama's cryptozoology rows (S353–S355, the
Sasquatch of cryptid fame — homonym, irrelevant). **No sibling has opened or
registered any source C1's assimilation step is about to open** (unblob
squashfs handler source, unblob test-fixture provenance, Freetz AVM-BE note).
No registry id-collision risk for the rows R38-C1 adds; kake's QUALITY.md:1115
rule ("another lane's or a staged package's identically numbered row is not a
substitute") is the standing fleet caution for the assimilation id-check.

## Findings — C2 self-assessment pointer calibration (calibration axis)

**Verdict: the method class is convergent at two siblings, but every counted
byte is lane-local; there is no ground this lane would duplicate.** The
self-assessment surfaces each counter reads are that lane's own
SCORECARD/SHONEN/PROVINCE; no sibling bytes appear in kaidoku's C2 inputs or
vice versa. Two siblings run recognizably the same discipline:

1. **chousa-shokunin — closest predicate, and it predates this round.**
   - `corpus/evidence/round51/c3-count.py:1-22` (frozen counter, docstring):
     "every repo-path pointer a self-assessment names resolves at the tip",
     where self-assessment = evidence-pointer cell of every SCORECARD
     `## Capabilities` row + every indented SHONEN.md evidence line; target
     `DANGLING=0`, with the same no-fewer-than-base guard shape as kaidoku's
     C2 ("neither the capability-row count nor the pointer count is below its
     value at BASE_REV"). Named limit also matches in spirit: "existence, not
     truth".
   - `corpus/QUALITY.md:880-883` — standing criterion 83: "A self-assessment
     pointer resolves, or carries a `correction:` line naming a non-empty
     target", check `c3-count.py` printing `CAP_ROWS/POINTERS/
     RESOLVED_BY_CORRECTION/DANGLING`, `C3=PASS` exit 0.
   - `corpus/evidence/round34/self-audit.py:2-5` and
     `corpus/evidence/round34/claims-a2.md:23,120-124` — round 34 ran the
     same claim ("C3 — calibration: self-assessment text vs observed repo
     state, counted").
   - `corpus/lessons/round-51.md:17-18` — routed defects 4 and 5 for that
     round: (4) "five self-assessment evidence pointers dangle at the base,
     and no criterion 1–80 requires a pointer to resolve" — the same
     before-shape kaidoku's C2 carries (`evidence/doctor/` dangling at base,
     repaired by a pointer to the same document); (5) a counter defect class
     worth porting: the c3 extractor stripped a leading dot, so three
     existing `.ufo/...` paths read as dangling (false positives), and its
     controls were derived from the counter's own `DANGLING` output, so no
     control ever seeded the dot class — a vacuous-control pair.
     `claims-erratum.md:12-19` records the extraction correction
     (`tok.strip(",;:()").rstrip(".")`, never a leading dot) with the
     predicate unchanged.
2. **kake-shokunin — report-seat calibration, no frozen counter.**
   - `.ufo/waves/round-29/w2/CalibrationScorecard.md:1-3` — "self-assessment
     versus repo state": 6 mismatches found, several of the exact C2 classes
     (e.g. item 2: `QUALITY.md:337` cites `PROTOCOL.md:398-402`, which does
     not resolve from the lane and whose line range points at the wrong
     section; item 4: PROVINCE prose contradicting same-file state).
   - `.ufo/waves/round-33/w2/ReviewHistoricalMarkings.md:9` and
     `round-34/w2/ReviewQualityCriteria34.md:9-10,24-25,47,62` — recurring
     "pointers resolve at the pinned rev / pointers resolve against committed
     bytes" review discipline.
   - `corpus/knowledge/claim-count-derivation.md:2-3` (round 43) — count
     calibration: "re-derive any count filed in a report or SCORECARD row…
     before filing" — the same lane-scoped command-A/B count discipline C2
     freezes; kake's later rounds file census counts (135→136→142→145 rows)
     with committed census receipts.

The other 14 lanes: the scoped sweeps (`self-assessment|self assessment` over
sibling SKILL.md/LOG.md/corpus; `pointer counter|pointers resolve|unresolved
pointer|backticked` over the lane roots) produced no calibration-counter
ground outside chousa and kake. Incidental "pointer" hits elsewhere are RE
domain prose (revenger) or dispatch text.

**Carryover falsifier patterns (reported, not executed — wave/L1 material).**
Chousa's round-51 erratum hands this wave two cheap mutation classes for
kaidoku's `c2-counter.py` selftest, both within the frozen counter's own
reading rules: (a) dot-lead stripping — a pointer to an existing `.ufo/...`
path must not read as unresolved (kaidoku's `PTR` regex strips only a
trailing `:N-M`; a mutant that also strips leading dots would false-dangle,
exactly chousa's defect); (b) controls derived from the counter's own
mismatch output never seed the dot class (vacuous selftest). Kaidoku's
selftest already includes "new unresolved pointer" and "deleted pointer"
cases; a dot-leading existing path is the unseeded class chousa hit. This is
a falsifier *idea* for the wave's mutation seats; it changes no frozen
artifact.

## Findings — ground this lane would be duplicating

- **C1: none.** Sole-holder ground; every sibling hit classified above is a
  capture, fixture copy, debris record, host-inventory line, or an explicit
  fence that names this lane's rows as not-absorbed. The revenger fence is a
  live adjacency: revenger's C07 (`frontier → held`) names the firmware
  family while ADJ-06 is unresolved, and revenger's own reports warn that a
  coverage-map row is "what a later handoff will quote".
- **C2: none at the byte level.** Method convergence with chousa (frozen
  pointer counter, R34+R51, guard shape shared) and kake (report-seat
  calibration + count re-derivation) is real but lane-scoped by construction.
  Kaidoku's C2 is not the fleet's first pointer counter; it is the most
  surface-inclusive one (adds Owned axes rows, PROVINCE Core/Frontier rows,
  count and section-range calibration).
- **SOURCES: none.** No sibling registry holds any row for the sources C1's
  assimilation is about to open.

## Proposed move (one, bounded)

**Carry a "Cross-lane scope note" in the C1 knowledge entry
(`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`) that
names the revenger fence and the open ADJ-06, in revenger's own round-64
Q10 sentence format.** Suggested shape (for the L1/entry author; this seat
writes no corpus file):

> Reported, not absorbed: this entry covers only the four frozen standard
> big-endian SquashFS v4 carriers and their committed oracles; it does not
> settle ADJ-06 (fleet `.ufo/l0-questions.md:42` open; `tsukuroi-shokunin/
> PROVINCE.md:51` still names the recipient "protocol integrator —
> kaidoku/revenger ownership unresolved"), does not absorb revenger's C07
> firmware-family ground (`revenger-shokunin/.ufo/waves/round-64/
> R64ConnectorOverlap.md`), and does not move the AVM-BE / vendor-mangled
> frontier.

- **Affected axis:** calibration (cross-lane consistency of what the new Core
  row asserts) — and only calibration. Coverage is unchanged: the move adds
  prose to the entry; the C1 predicate's counting conditions (Core row naming
  `squashfs_v4_be` citing the entry; entry citing a 2026-10-26 SOURCES row;
  frontier-note supersession; README coverage row) are untouched.
- **Why it is the move:** revenger's round-64 report establishes both that
  coverage-map/Core rows are "what a later handoff will quote" and that a
  `held`/`Core` token on the contested firmware verb family can be misread as
  an ownership ruling. Kaidoku's round-38 Core row moves exactly that verb
  family (REA `extract-firmware`) one step deeper into Core. Without the
  sentence, a fleet integrator sampling the entry (the R37-CL3 lesson-gate
  pattern) can route a "kaidoku settled ADJ-06" finding; with it, the entry
  is aligned with the fence revenger already landed, at zero cost to C1's
  target. This is symmetric: revenger names kaidoku's rows as not-absorbed;
  kaidoku names revenger's fence as not-a-ruling.
- **Risks:** none to frozen artifacts (prose-only, outside every counted
  condition); the only cost is one sentence in an entry the round already
  must write. If the L1 judges the sentence out of the entry's scope, the
  fallback is the same sentence in the SCORECARD round-38 record notes, where
  prose is free.
- **Verification after landing:** re-open the entry and confirm the sentence
  names (i) ADJ-06 open at l0-questions.md:42, (ii) tsukuroi PROVINCE.md:51
  recipient text, (iii) revenger's C07 fence path; then confirm
  `c1-counter.py --selftest` still passes 15/15 unchanged and the frozen
  counting command at the measured revision still reports the same verdict.

## Tools / installs

None installed, none upgraded. Sweeps used the harness `grep`/`read` tools and
one `bash` existence/size loop. No pacman, no uv, no npx (REA not invoked —
this seat ran no extraction). No network.

## Evidence appendix — commands exercised

1. `grep -i 'squashfs'` / `'sasquatch'` / `'unblob'` / `'extract-firmware'`
   over the 16 sibling roots — classes (1)–(6) above; all hit paths listed
   with line numbers in the findings.
2. `grep -i 'squashfs_v4|v4be|big.?endian'` over the 16 sibling roots — only
   kake XML/UTF-16 material and tsukuroi host-inventory lines (chaff).
3. `grep -i 'pointer counter|pointers resolve|self-assessment|unresolved
   pointer|backticked'` over the 16 sibling roots — chousa and kake classes
   only, plus RE-domain "pointer" prose.
4. `grep -i 'self-assessment|self assessment'` over sibling
   SKILL.md/LOG.md/corpus — chousa only.
5. `grep -i 'SOURCES\.md'` over sibling SKILL.md/LOG.md/corpus, and
   `grep -i 'unblob|squashfs|sasquatch|freetz|avm'` over the 16 sibling
   `corpus/SOURCES.md` — revenger:101 and the kotodama homonym only.
6. `test -f`/`wc` loop over all 17 lanes' `corpus/SOURCES.md` — sizes table
   above.
7. Direct reads: kaidoku `plans/round-38-claims.md`;
   `corpus/lessons/round-37-verifier-spotcheck.md`; `tools/round-38/
   c2-counter.py:1-55`; `PROVINCE.md:44-80,150-160,366-374`; chousa
   `corpus/evidence/round51/c3-count.py:1-63`, `corpus/QUALITY.md:879-883`,
   `corpus/lessons/round-51.md:16-19`, `corpus/evidence/round51/
   claims-erratum.md:12-19`, `corpus/evidence/round34/claims-a2.md:22-26,
   119-124`, `corpus/evidence/round34/self-audit.py:1-6`; kake `.ufo/waves/
   round-29/w2/CalibrationScorecard.md`, `corpus/knowledge/
   claim-count-derivation.md:1-36`; revenger `.ufo/waves/round-63/build/
   R63ConnectorOverlap.md:35-45`, `.ufo/waves/round-64/R64ConnectorOverlap.
   md:1-53`, `corpus/knowledge/round-64-firmware-region-byte-evidence.md:
   202-205`, `corpus/SOURCES.md:100-102`; tsukuroi `PROVINCE.md:44-58,
   159-183`; mori `PROVINCE.md:1-73`; fleet `.ufo/l0-questions.md:38-49`;
   kengaku `.ufo/waves/round-26/build/ConnRosterScan.md:14-20,38-40`.

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ConnSiblingOverlap` removed at
close; every citation above is to committed or live lane/sibling/fleet paths.
