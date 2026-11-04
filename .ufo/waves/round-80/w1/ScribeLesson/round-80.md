# Round 80 — exact pointer tokens, receipts bound to committed instruments, and a row per refusal clause

Base: `16dfa009bf143080dfcdfc5f9ec34bd359536d90`.
Declaration: `84d68e90f8a1ea3a3a7f94a208695c21023c0472` — the last commit touching
`plans/round-80-claims.md` (`git log -1 --format=%H -- plans/round-80-claims.md`), which freezes the
three predicates, kill rules and controls and the strictness fixture set
(`.ufo/waves/round-80/l1/fixtures/strictness.json`, 2 802 B, sha256 `40f99456…`).
Axes: **calibration** (R80-C1 — the record's pointer cells bind as delimited tokens and a duplicate
cell is a defect), **freshness** (R80-C2 — every landing-class receipt's instrument digest names a
committed blob; the first measured move after the round-79 gate entered `freshness` as an owned
axis) and **depth** (R80-C3 — the nine `validate_receipt` clauses become a decision table with one
isolating case each).

The numbers below are labelled by their source: committed receipts the claim freezes, and this
lesson's own re-derivations under `.ufo/waves/round-80/w1/ScribeLesson/grounding/`. All four
round-80 instruments were on disk by the end of this seat's draft — `receipt-provenance.py`
(sha256 `b59068d6…`), `guard-battery.py` (`b9b3b10c…`), `strictness-battery.py` (`2b26d75a…`) and
`pointer-bind.py` (`2e4a7852…`) — and each was run; every executed value below is pinned to the
digest of the bytes that produced it. After arms are measured at
`b00419fb8c3d083761034605fec2eed1897f60ad` (the L1's landing tip at this seat's final read; HEAD
moved three times during the seat, every movement a landing of this round's own work).

## Mistakes

| class | evidence (path:line@blob) | captured-by | fix, shown able to fail |
|---|---|---|---|
| **unrecoverable-provenance — a landing receipt names an instrument revision that no committed blob carries.** | `.ufo/waves/round-79/l1/scores/c2-at-landing.json:90` declares `instrument.sha256 a0044c4c…` for `tools/round-79/pointer-bind.py`; the only committed blobs of that path are `91d23dad…` (freeze) and `40905d39…` (supersession onward). Neither matches. | Nothing until R80-C2. The round-79 non-author spot-check found it by reading (`corpus/lessons/round-79-verifier-spotcheck.md:161`), not by an instrument, so the class was a one-off repair. | `tools/round-80/receipt-provenance.py --from-round 60 --to-round 79` compares each receipt's digest against committed blobs of the path it names. Shown able to fail: at base it exits 1 with `receipts 34`, `flagged 2`, `expected_control_flags 1`, `unexpected 1`, naming the forged control and `c2-at-landing.json` (`grounding/c2-base-run.json`). Re-run at the declaration (`84d68e90`) it still exits 1; after the L1's landing (`b00419fb`) it exits 0 with `flagged 1`, `expected_control_flags 1`, `unexpected 0` and a defect-free `--validate` (`grounding/c2-after-run.json`). |
| **silent-information-loss — a record that declares the same client cell twice keeps the last cell, and nothing counts the duplicate.** | `tools/round-79/pointer-bind.py:163@40905d39…`: `pins = {name: (pin, pointer) for name, pin, pointer in RE_PIN.findall(text)}`; the same line is `:127` at blob `91d23dad…`. The probe is `w1/ReviewerC2.md:122` (F2). | Round-79 ReviewerC2 F2 — one end-to-end fixture, one instance. `checks_total` counts unique ids, so a duplicate cannot appear in any counter. | Fixtures `rb03`/`rb04` append a duplicate `OMP`/`Devin` cell and require every declared cell counted plus the id in `duplicates`. Shown able to fail: the control arm returns `checks_total 5` with the unchanged id list and no duplicate channel, and a stale-first plus green-second record drops the stale cell and binds (`grounding/c1-base-arm.txt`). Executed on the landed bytes: the candidate scores `cases 4`, `green_cases 2`, `candidate_false_greens 0`, `control_false_greens 4`, both green refusals 0, exit 0, `--validate` defect-free (`grounding/c1-candidate.json`); the control-as-candidate arm reports `candidate_false_greens 4` naming `rb01`–`rb04` and exits 1 (`grounding/c1-control-as-candidate.json`). |
| **exercised-but-unpinned — one selftest case asserts a validate defect, but no table row declares it, and the other eight clauses are deletable with every case green.** | `tools/round-78/attack-gate.py:921@4e4baf00…` is the only selftest case calling `validate_receipt`; the nine `defects.append` clauses sit at `:782 :785 :790 :792 :794 :797 :801 :804 :807`. | The deletion test. The same class was proved for the round-79 instruments by `w1/MutInstruments/receipt.json:70` — `gm-f`, `gm-g`, `gm-h` survive deletion with every case green. | `tools/round-80/guard-battery.py` binds each clause to exactly one SKILL row and one declared case, then deletes the clause from a copy. Shown able to fail: at base it exits 1 with `guards 9`, `rows 0`, `bound 0`, `survivors 9`, pristine `cases 29 failures 0`, `target_pin.matched false` (`grounding/c3-base-run.json`); my own deletion arm removes clause 5 and gets `failures=1`, removes any of the other eight and gets `failures=0` (`grounding/c3-clause-deletion.txt`). The survivor reason is "no declared case bound", not "no case exists". After the landing (`b00419fb`) it exits 0 with `rows 9`, `bound 9`, `survivors 0`, `pristine 37/0`; `target_pin.matched` is true only when `--expect-sha256 df6fb856…` is passed, which the prose predicate (`plans/round-80-claims.md`) omits and the machine `claims.json:34,37` carries (report F1). |
| **reference-drift — a prose `path:line` without the blob digest, in a wave whose own rule is that lines move.** | `w1/ReviewerC2.md:130` cites `token in line` at `:106` — true at blob `91d23dad…`; at blob `40905d39…` line 106 is `def git_show(...)` and the rule is `:142`. | Nothing until the pointer rule is applied to prose: R79-C2's class (a pointer compared by path and never by line) one layer up, in the lesson that records it. | Every lesson row names `path:line@<blob-sha256-16>`; the criterion re-prints the line from the named blob. Shown able to fail: `:106` resolves to the token test at `91d23dad…` and to `def git_show` at `40905d39…`, so a digest-less `:106` names two different lines (`grounding/m4-line-drift.txt`). |

### Capture commands

Each mechanism is a criterion the lane can run, not a sentiment.

1. **M1 provenance.**
   `python3 -I -B tools/round-80/receipt-provenance.py --root . --rev 16dfa009bf143080dfcdfc5f9ec34bd359536d90 --from-round 60 --to-round 79 --json-out <receipt>`
   → base `exit 1`, `receipts 34`, `flagged 2`, `expected_control_flags 1`, `unexpected 1`; after the
   L1 replaces the round-79 receipt, `exit 0`, `flagged 1`, `unexpected 0`, `--validate` defect-free.
2. **M2 exact token + duplicate.**
   `python3 -I -B tools/round-80/strictness-battery.py --root . --impl tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json --json-out <receipt>`
   → `cases 4`, `green_cases 2`, `candidate_false_greens 0`, `control_false_greens 4`,
   `candidate_green_refusals 0`, `control_green_refusals 0`.
3. **M3 unpinned clause.**
   `python3 -I -B tools/round-80/guard-battery.py --root . --rev <measured> --expect-sha256 <gate digest at that rev> --json-out <receipt>`
   → `guards 9`, `rows 9`, `bound 9`, `survivors 0`, `pristine.cases 37`, `pristine.failures 0`,
   `target_pin.matched true`; at base `rows 0`, `bound 0`, `survivors 9`. The flag is required for the
   pin conjunct: the machine record (`.ufo/waves/round-80/claims.json:34,37`, sha256 `0f33ea87…`)
   carries it; the prose predicate (`plans/round-80-claims.md`) does not, and without it the
   instrument records `expected ""` and `matched false`, which `--validate` does not flag.
4. **M4 prose pointer.** `git show <rev>:<path>`, then `sed -n '<line>p'`; the printed text must equal
   the row's quoted text and the row must carry the blob digest it was read at.

## Gate

Rows opened 2026-11-04 and landed in `corpus/SOURCES.md` as `S297`/`S298` by the L1 (the sources
seat drafted the reverse order and withheld the RFC row as a reuse; the registry file is the record).
Both quotes and digests were re-verified here against the snapshots the registry cites. The Q&A row
is the sources seat's recorded rejection; the UAX #29 row is this scribe's own screen (opened because
a word-boundary claim invites the Unicode report as authority) and is not a registry row.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S298, Python `re` documentation, `\b` assertion — **admit** (docs, tier A) | https://docs.python.org/3/library/re.html#re-syntax-special-word-boundary | 2026-11-04 (HTTP 200, 257 722 B, sha256 `24ef5ff0…`, snapshot `.ufo/waves/round-80/l1/sources/re.html`) | "Matches the empty string, but only at the beginning or end of a word." (14 words; snapshot line 747) | Grounds the vocabulary of a delimited match — a zero-width assertion at a word edge — not the alphabet. The binder's class adds `.` and `-` to `\w`, so the row grounds "delimited on both sides" while the exact class stays a declared lane choice; the same split S295's `-n` row made for line numbers. |
| S297, RFC 8259 §4 Objects, duplicate names — **admit** (spec, tier A) | https://www.rfc-editor.org/rfc/rfc8259.txt | 2026-11-04 (HTTP 200, 28 360 B, sha256 `61a5378f…`; byte-identical to S289's snapshot) | "The names within an object SHOULD be unique." (8 words; `grep -n` line 322 of `.ufo/waves/round-80/l1/sources/rfc8259.txt`) | The sentence is a SHOULD plus an interoperability warning: receivers of a non-unique object behave unpredictably. It grounds why the lane refuses instead of picking a winner; the stricter "duplicate is a defect" rule is the lane's policy, not the RFC's requirement (`rb03`/`rb04` score the refusal). |
| Stack Overflow Q&A 21 802 701, duplicate JSON keys — **reject** (sources seat) | https://stackoverflow.com/questions/21832701 | 2026-11-04 (rendered page HTTP 403, 5 753 B interstitial; content opened through the Stack Exchange API 2.3, HTTP 200, `so-api.json` 1 387 B and `so-answers.json` 21 102 B) | "Yes but is not recommended." (5 words; `so-answers.json` `items[0].body`, score-226 answer) | Rejected: its normative sentence is the RFC's, reproduced by quotation, and its own contribution is vote-ordered interpretation that drifts without notice; grounding a refusal rule there puts a mutable page where a primary text is required. **Flip:** if a claim becomes "implementers report last-wins in practice", it is a community tier-B row pinned by the answer's `last_edit_date` and the API snapshot digest. |
| Unicode UAX #29, Word Boundaries — **reject** (this scribe's own screen) | https://www.unicode.org/reports/tr29/ | 2026-11-04 (HTTP 200, 141 203 B, sha256 `60fb49ee…`, snapshot `w1/ScribeLesson/sources/uax29-tr29.html`) | "An implementation shall choose either UAX29-C2-1 or UAX29-C2-2 to determine whether an offset within a sequence of characters is a word boundary." (22 words; snapshot line 447) | Rejected: it defines boundaries over Unicode Character Database properties and requires a declared profile; the binder uses a fixed ASCII class over decoded text (`errors="replace"`), so citing it would claim a conformance the instrument neither implements nor tests. **Flip:** adopt UAX29-C2-1 (or declare a profile) and add a non-ASCII boundary case to the strictness fixtures. |

## Sources

The round's opening list as the lane records it, and the snapshots this round moved. Values are read
from the committed files at draft time; `…` abbreviates a digest whose full form is in the receipt.

| item | as the lane records it | bytes / sha256 |
|---|---|---|
| `corpus/SOURCES.md` | at final read 204 rows (`S297` RFC 8259, `S298` `re` appended by the L1 in the working tree, uncommitted); 202 rows committed at `b00419fb` | 232 495 B / `3b7f44f6…` committed → 235 406 B / `b4d67a32…` at read |
| round-80 census start | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, 202 rows, 23 W04 duplicate-URL warnings, none new (`.ufo/waves/round-80/l1/census-start.txt`) | 2 372 B, sha256 `a5818e9a…` |
| declaration | `plans/round-80-claims.md` freezes the three predicates, kill rules and controls | 12 617 B, sha256 `d50c5a95…` |
| frozen fixtures | `.ufo/waves/round-80/l1/fixtures/strictness.json` — 4 red, 2 green, record template | 2 802 B, sha256 `40f99456…` |
| S298 snapshot | `.ufo/waves/round-80/l1/sources/re.html` | 257 722 B, sha256 `24ef5ff0…` |
| S297 snapshot (same bytes as S289's) | `.ufo/waves/round-80/l1/sources/rfc8259.txt` | 28 360 B, sha256 `61a5378f…` |
| rejected Q&A | `so-answers.json`, `so-api.json`, `so-dupkeys.html` under `w1/ScribeSources/` | 21 102 / 1 387 / 5 753 B; sha256 `e086dc8b…` / `79f61b33…` / `d6404958…` |
| this seat's independent opens (not appended, no SOURCES row) | `man7-grep.html`, `toml-v1.0.0.html`, `uax29-tr29.html` under `w1/ScribeLesson/sources/` | 43 199 / 44 035 / 141 203 B; sha256 `d6f07a7f…` / `728a5c13…` / `60fb49ee…` |

## Limits of this draft

- **C1's base shape is an argument, not a checkout.** The frozen base arm is the same battery with
  `--impl tools/round-79/pointer-bind.py`; it was executed that way (`candidate_false_greens 4`,
  exit 1) rather than from a `16dfa009` checkout. The battery scores the record from the worktree,
  and `PROVINCE.md` is unchanged between base and declaration, so the live arm's `checks_total 5`,
  `matched 5`, `mismatches 0`, `unparsed 0`, `duplicates []` is the same reading at both revisions.
- **C2 and C3 after arms are measured, with one caveat.** At `b00419fb` C2 exits 0 (`flagged 1`,
  `unexpected 0`) and C3 exits 0 (`rows 9`, `bound 9`, `survivors 0`, `pristine 37/0`). C3's
  `target_pin.matched` is false unless `--expect-sha256` is supplied; the frozen printed command does
  not supply it, so that one conjunct of the predicate is not reachable as printed (report F1).
- The registry append (`S297`, `S298`) is in the working tree at this read, not committed; the
  post-append census and any correction to the sources seat's id order are the L1's landing steps.
  The Q&A rejection and this seat's UAX #29 screen add no registry row.
