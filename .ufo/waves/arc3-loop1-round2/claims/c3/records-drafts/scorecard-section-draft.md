# SCORECARD.md round-section draft — C3 records (SC-4, arc3-loop1-round2)

Seat SC-4 · chain c3 · role scribe · 2026-10-19. **Draft for the PARENT;
SCORECARD.md was not touched by this seat.** Append at EOF (after the
`arc3-loop1-round1` section ending `SCORECARD.md:1417`; HEAD at draft time
`14b1682`, file 1417 lines). `⟨…⟩`/`⟨FILL⟩` = parent-fill slots; the **C3
bullet, the C3 verdict row, the C3 learning sentence and the C3 carried-debt
line are drafted complete**; values only other C3 seats can produce are marked
`⟨FILL: …⟩` with the producing seat named.

**Pin-free discipline (measured, load-bearing).** The census instrument
(`.ufo/gates/c1-census-v10.py`) scans `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`
against a fixed declared bound (last row `SCORECARD.md:769-855`,
`c1-census-v10.py:139-161`); any locus past the bound reads UNDECLARED → FAIL
(`:401-402`). A locus exists only where a REA_GATE line (`:167`) also carries an
`@`-pin (`:163`), a bare `6.x.y` (`:164`) or an absolute `path.json|toml|yaml:NNN`
pointer (`:165`). The C3 text below therefore carries **no version literal, no
`@`-pin, no `path:line` pointer, and no client config filename** — it refers to
"the five custody paths (three client configs + two shell profiles)". §3 records
the simulation that measures this (PASS, plus a planted-pin control that FAILs).

## Literal section text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL SECTION TEXT -->
## arc3-loop1-round2 — depth + freshness + operability: ⟨PARENT-FILL: verdict phrase per the cross seat's outline⟩, 2026-10-19

Round 2 of the arc (2/10), on the opencode-go lane (key 2 of 7 — rotation
advanced after round 1). All three owned proxies stay saturated at 10.0; depth
is the owned axis (three-way tie, most-falsifiable-next-claim tie-break per the
luna-round-2 precedent); freshness and operability ride the standing fleet-axis
recording ruling. Roster frozen PRE-DISPATCH (64 = 64, the r9 assertion), with
the freeze's own miscount caught and recorded pre-dispatch ⟨PARENT-FILL: keep iff
the parent confirms the freeze history line⟩.

- Wave: ⟨PARENT-FILL: reports path, wave-artifacts / work / records commits,
  delivery ⟨N⟩/64 per the roster reconciliation⟩.
- C1 depth (owned) — queue-drain rule #14 (self-identity re-derivation
  discipline): ⟨FILL from the C1 records draft (`claims/c1/records-drafts/`):
  rules 13 → 14, 14/14 citation-resolved at the work commit, prior 13 rules
  byte-identical; the rule text and its motivating EX-12/F2+D9 origin⟩.
- C2 freshness (fleet) — census fail-closures H1 (absent-file guard) + H3
  (positive floor): ⟨FILL from the C2 records draft (`claims/c2/records-drafts/`):
  instrument v11 sha, the declared FAIL classes for an absent CURRENT-only
  scoped file and for a zero-locus non-empty scope, the round-1 silent-PASS
  injections reproducing as declared FAILs, HEAD PASS 0/0/0/0, creep audit
  0 flags, the scope-diff external audit as the certificate of the H4 residual⟩.
- C3 operability (fleet) — custody receipt v2. Measured origin (arc3-loop1-round1
  cross seats): the canonical pre-pair receipt rendered each path's modification
  time in the host's local zone (UTC-3) under a UTC label — the recorded epoch
  `1792011200` = `2026-10-14T20:53:20Z`, printed `2026-10-14 17:53:20` — a
  3-hour label defect (digests unaffected; round-1
  `claims/cross/receipts/config-pre-pair-metadata.txt`, reproduced by the
  round-1 connector); and sha256-only custody is blind to a same-content
  rewrite, where inode and ctime move while the digest does not (round-1
  attack 3). Landed at the work commit: the custody-pair instrument (sha256
  re-derived at landing — the file churned in-window, so the observed shas are
  not pins) emits a v2 receipt per path carrying sha256 + modification-time
  epoch + UTC render (strict `gmtime`, TZ-invariant) + a separately recorded
  local render + change-time epoch/ns + inode + mode/uid/gid, with declared
  exit classes (0 match; 10 content drift; 11 rewrite drift; 12 metadata
  drift incl. the v1 label defect; 13 absent; 2 usage; 3 selftest) and v1
  compatibility for three legacy receipt shapes. The label defect is measured
  gone: the defect epoch `1792011200` renders `2026-10-14T20:53:20Z` in the v2
  receipt and is invariant across three TZ settings (selftest case; the
  scribe's independent scratch run: 15/15 cases PASS, exit 0). A live
  same-content rewrite of a **scratch copy** is detected by time/identity pins
  alone: in-place with the modification time restored → exit 11 with only the
  change-time ns field moved; replace-by-rename → exit 11 on inode movement;
  a content flip still exits 10, an absent path exits 13, a mutated copy of
  the round receipt exits 10 (comparator non-vacuous), and a mutated legacy
  digest entry exits 10 — reproduced independently by three seats on their own
  scratch files (EX-31 attacks; EX-32 battery A; RV-14 battery on fixtures
  with a sandboxed fake home, real paths untouched, tool hash stable across
  the battery). The dedicated attack ladder closes the class: six same-content
  rewrite forms — including a forged modification time — all flagged as rewrite
  drift (exit 11) where a digest-only comparison stays silent, detected via
  inode and change-time fields (nanosecond precision is load-bearing: a
  whole-second format would be blind to a same-second rewrite), with the
  control cases (content flip, absent, permission-only) each in their declared
  classes; the same seat independently re-ran the landing pair and a second
  seat's capture — match 5/5, exit 0, sidecars clean. v1 receipts remain
  verifiable: the round-1 canonical receipt
  re-derived 5/5 on sha256 + inode + ctime sidecar + mtime epoch (EX-35
  `backcompat-v1-standard.out`), and the tool classifies the historical label
  defect as a declared finding, not a silent pass. The round's own live
  pre/post pair (5/5, exit 0) is captured by the tool: the pre-pair receipt
  (sha256 `fa9706c6…` = its sidecar, captured-utc `2026-10-19T12:04:06Z`),
  and a same-revision pre/post pair (`capture-pre.txt` → `capture-post.txt`,
  tool sha256 `112d01dc…` at both ends) verifying MATCH 5/5 exit 0 — zero
  drift across the wave window; cross-seat corroboration: the pre-pair receipt
  replays byte-equal from the held earlier revision, and two same-revision
  captures agree with an independent field ledger 50/50 (per-path × field
  class, normalized diffs empty, nanosecond fields matched against the host's
  stat renders). The five
  custody paths stayed READ-ONLY for every seat (hash/stat capture only; the
  tool refuses to write over a custody path) and independent captures agree
  (two further seats' pre-captures, 5/5). No corpus/knowledge edit in this
  claim; no scope-bound widening (the round's scope-diff audit ⟨FILL: 0
  flags⟩).
- Measured at the records commit: ⟨PARENT-FILL per the cross seat's outline —
  command A; probe selftest + findings; census PASS 0/0/0/0; custody post-pair
  5/5⟩.

| Axis | Before → after | Verdict |
|---|---|---|
| depth (owned) — C1 | ⟨PARENT-FILL from the C1 records draft⟩ | ⟨PARENT-FILL⟩ |
| freshness (fleet) — C2 | ⟨PARENT-FILL from the C2 records draft⟩ | ⟨PARENT-FILL⟩ |
| operability (fleet) — C3 | sha256-only custody receipt with a mislabeled local mtime under a UTC label, blind to a same-content rewrite → v2 receipt (sha256 + UTC-rendered epoch + inode + ctime) committed under `.ufo/gates/custody-pair/`; label defect measured gone; same-content rewrite detected on a scratch copy; v1 receipts re-verified; round's live pre/post pair captured 5/5 exit 0 | improved |
| calibration | ⟨PARENT-FILL: unchanged, with the measurement recipe at the records commit⟩ | unchanged |

Learning trends: ⟨PARENT-FILL C1/C2 sentences; C3's:⟩ the round-1 cross seats'
two C3 findings (a label defect that false-names its own time base, and a digest
pair that cannot see a metadata-only rewrite) were turned into an instrument
with a stated time base and two extra pins, and the fix was verified by the same
class of attack that motivated it — detect-by-inode/ctime on a live scratch
rewrite, not by re-reading the receipt's prose.
Planned: ⟨PARENT-FILL⟩. Carried debt (named): ⟨PARENT-FILL C1/C2 merges⟩; C3
adds three named residuals measured this round — a capture over an unreadable
path raises an uncaught permission traceback (exit 1, outside the declared
class table; the file is opened for hashing outside its stat guard); `verify`
does not authenticate the receipt it is given, so a tampered receipt can read
`MATCH` (the capture-time sidecar digest catches the tamper, but the verify
path never reads it — an audit must check the sidecar or use the committed
copy); and a selftest given a nonexistent scratch parent dies with a traceback
instead of a usage error. The whole-second-granularity boundary the attack
ladder measured is closed in the landed tool by its nanosecond fields ⟨FILL:
parent keeps these named or records their closure⟩; the round's census residual H4
(self-certification — an instrument cannot detect its own scope widening) stays
named until an external audit lands. Retired: ⟨PARENT-FILL: none / list⟩.
<!-- END LITERAL SECTION TEXT -->

## Notes for the parent

- Every `⟨FILL⟩` in the C3 bullet is a round-2 C3-chain artifact; fill from the
  landed files, not from the frozen claim. If a slot has no landed evidence,
  say so in the section rather than asserting it (an unrun check has not
  passed) — the C3 claim is only as strong as its weakest filled slot.
- Keep the section pin-free after filling. In particular, when quoting EX-31's
  receipts, quote the **epoch integers** and UTC renderings, not client config
  paths; and when quoting the tool's sha256s, do not introduce a
  `path.json:NNN`-shaped pointer. If the merged text cannot stay pin-free,
  the SCOPE bound must be re-keyed in the same commit as a DATED row (round-1
  EX-28 precedent) — not measured here.
- The verdict-table row and the learning sentence are drafted complete; the C1
  and C2 rows/sentences should be spliced from those chains' records drafts so
  the three chains' numbers stay single-sourced.

## 3. Records-append census simulation (SC-4, `/var/tmp/sc4` scratch) — MEASURED

Method (round-1 SC-7 precedent, re-run against the round-2 drafts): copy the
three scoped files at HEAD into scratch roots, append the literal section text
(re-extracted between the BEGIN/END markers), run the census with `--root`.
Instrument identity bracketed around the runs: `.ufo/gates/c1-census-v10.py`
sha256 `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`
(EX-16's in-flight v11 fail-closures, `+80/-10` vs HEAD `14b1682`) — identical
before and after every run, so the pairings are exact.

Revision history (this section's text is re-derived after every revision —
rule #14 discipline; both revisions measured 2026-10-19 ~12:07-12:11Z):

- revision 1 — skeleton, 77 lines, section sha256
  `683d4bd768d64356ad06afe3b0c6ccc347f7368343499df4742af64b674f6228`
  → outputs `b4722def…` (base) / `6198f33b…` (records) / `a5857c46…` (control).
- revision 2 — evidence-filled (published below), 90 lines, section sha256
  `f805cbb1a2eff7cb22c97106e48615a944617195eea849f603b40eca610519fb`
  → outputs `b4722def…` (base, unchanged) / `649f374379d8bb3f910f3f4e697c5b35d8662312a003da37ab16d042cccd669d`
  (records) / `b722abf308a155136eff9b846716626dcedea7b8986c200f74e10b6c60f564b6`
  (control). The filled text adds **zero** loci (9 → 9) and keeps the PASS.
- revision 4 — final published text (below), 105 lines, section sha256
  `0055fedaa0ce834d31d23a846f1dcc0a09d1cfbb5247af8529b8eb2405eea59d`; zero
  needle hits; instrument `c95a5cf3…` — same verdicts as revision 3 (base and
  records trees both FAIL on the per-file G2 floor with undeclared 0; control
  isolates `UNDECLARED (1)`; outputs rev-4: base `f1188c6e…`, records
  `2754cf4f…`, control `b72ef81d…`). §3 documents this revision; the section
  text below is unchanged by §3 edits (which are outside the BEGIN/END markers).
- revision 3 — residuals-filled (the published text), 102 lines, section sha256
  `e2f9164bc8ecc4222cb01148b2df2e876b4cfcd73013daebda75bc2d99417115`; zero
  needle hits again. The measurement interleaved with the C2 chain's landing:
  the instrument changed under the run (`82fb807e…` → `09e270c2…`), and at the
  newest revision the **untouched base tree also FAILs** — `G2
  positive-assertion guard: SUSPECT` (current-ok loci per file: PROVINCE 1,
  SCORECARD 4, SKILL 0, floor 1/file) — so that FAIL is instrument-state at
  HEAD, **not** the records text: base 9 loci / records 9 loci, undeclared 0 in
  both; the control still isolates `UNDECLARED (1)` (10 loci). Parent: re-run at
  the records commit once the C2 landing settles, quote the then-current
  instrument sha and verdict; if the G2 floor stays red at HEAD, that is a C2
  finding, and the records section must not be landed as if it were green.

| Tree | SCORECARD lines | loci | VERDICT | exit | output sha256 (rev 2) |
|---|---|---|---|---|---|
| sim-base (HEAD files) | 1417 | 9 | PASS 0/0/0/0 | 0 | `b4722def…` |
| sim-records (+90-line section) | 1507 | 9 | PASS 0/0/0/0 | 0 | `649f3743…` |
| sim-control (+1 planted `rea-agents@6.4.0`) | 1510 | 10 | FAIL undeclared=1 | 1 | `b722abf3…` |

- The drafted section adds **zero loci** (9 → 9) and does not perturb the other
  files' counts — the pin-free property is measured, not asserted.
- The control shows the detector is live on the same appended region: one
  planted pin literal flips the run to UNDECLARED → FAIL exit 1.
- The section text also carries zero hits of the instrument's own needle
  regexes (PIN/VER/PTR/CACHE/REA_GATE each `hits: []`).
- Caveat for the parent: the instrument was mid-flight (EX-16's landing) at
  measurement time; re-run at the records commit and quote the then-current
  instrument sha. The drafted text's pin-free property does not depend on
  which revision of the instrument is current, since the appended region
  contains no locus in either v10 or v11 semantics.
