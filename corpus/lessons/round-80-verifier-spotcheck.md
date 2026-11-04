# Round 80 — non-author verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: kaidoku round 80, lane tip `72f8c6e9ff2e2c740cee8ef96ffe4791c7d66366`, base
`16dfa009bf143080dfcdfc5f9ec34bd359536d90`. I did not author this round; I re-measured the claims over
committed bytes, verified the lane's committed gate evidence (I did not execute the lane's gates), and
spot-checked the round's gate decisions against the sources they cite. Lane state at closure:
`jj-lane.sh state` → `branch=main local=72f8c6e9 remote=72f8c6e9 ahead=0 behind=0 head=detached
tracked=0 untracked=0`; `git status --porcelain` empty.

## 1. Conformance (step 1)

| check | result | evidence |
|---|---|---|
| report committed in the fleet repo by the lane identity | pass | `.ufo/reports/round-80/kaidoku.md`, 254 lines, commit `5ac5b2b37ee85c030368c7d9154c0299b3309421`, author `kaidoku-shokunin <kaidoku@shokunin.local>`; on `origin/master` and `origin/main` (`git merge-base --is-ancestor 5ac5b2b3 origin/master` → true) |
| `SHONEN` heading, one line per box | pass | heading present with four `[~]` lines and a resolvable pointer each; no `[x]` (correct: no non-author attestation) |
| every cited lane commit exists and is an ancestor of the branch | pass | `84d68e90`, `253fc817`, `b8260107`, `b00419fb`, `6037f599`, `c935b543`, `a3e22df4` each resolve and `git merge-base --is-ancestor <h> main` → true (base `16dfa009` likewise) |
| lane repo clean and pushed, no uncommitted round work | pass | helper `state`: `ahead=0 behind=0 tracked=0 untracked=0`; `status --porcelain` empty |
| dispatched prompt carries the template contract | pass | `.ufo/prompts/kaidoku-round-80.md` bytes 1–8304 are byte-identical to the rendered `templates/round-prompt.md` (`LANE=kaidoku`, `ROUND=80`, `FLEET_ROOT=/home/vgpnk/Projects/shokunin`, `AXES=coverage + depth + calibration (reverse engineering with REA)`, `<kaidoku-repo>=kaidoku-shokunin`), followed by the hyaku addendum §6. The addendum file has since gained a later "routing restore" line; the prompt is a dispatch snapshot, so its absence is not a defect |
| report is real, not a marker | pass | work performed with per-item pointers, six landed commits each tied to the round's `LOG.md` entry, per-claim counting commands, `Sources & frontier`, `Trend verdicts`, `SHONEN`, a `## Gate` and `## Mistakes` in `corpus/lessons/round-80.md` |
| wave shape | pass | `r80-w1` spec: 15 seats (executor 4, scout 2, scribe 3, reviewer 2, critic 1, mutation-tester 1, sentinel 1, connector 1); `r80-w1-results.json`: 15 results, 0 dead, 0 empty, 0 seat notes; attack seats 4/15 = 26.7 %; policy band `waveMinLanes 8 … waveMaxLanes 16` |

Non-blocking timeline artefact: the report commit's *author* date (2026-11-04 11:01:02 -03:00) precedes
the lane tip it cites (11:01:59) while its *committer* date (11:02:21) follows it. The committed report
bytes cite `72f8c6e9`, so the report could not have preceded that commit; ordering holds on content and
committer time. Routed as D5.

## 2. Claim re-checks (commands run by me)

All three claims are capability acquisitions; each was re-derived over committed bytes. No lane gate was
executed; where a claim rests on the lane's own instrument, its committed receipts, pins and tallies are
the evidence, and the independent part below is my own measurement.

### R80-C1 — calibration: delimited-token rule + duplicate cells (re-measured)

Frozen fixtures: `.ufo/waves/round-80/l1/fixtures/strictness.json` — red `rb01`/`rb02` (bind), `rb03`/`rb04`
(record), green `gr01`/`gr02`. I re-implemented both match rules from the fixture bytes (no import of the
lane's modules):

```sh
# for each red/green fixture: naive substring rule vs delimited rule (TOKEN_CHARS = [A-Za-z0-9._-])
```

Observed: `rb01 old_binds True new_binds False`; `rb02 True / False`; greens `gr01`, `gr02` bind under
both rules. Record arm: my own regex over `PROVINCE.md@72f8c6e9` counts `Devin 1, OMP 1, Kimi 1` client
cells; appending each record fixture's `append_cell` yields `OMP 2` / `Devin 2`, i.e. a duplicate the
round-79 last-wins parse collapses. **Old binder false greens 4, new binder 0, green refusals 0** —
matching the claim's `4 → 0`.

Committed receipts: `c1-at-base.json` `candidate_false_greens 4`, `control_false_greens 4`, greens 0,
`validate.defects []`; `c1-at-landing.json` candidate 0, control 4, greens 0, `validate.defects []`.
Live arm: I extracted the five `PROVINCE.md` pointer cells at `72f8c6e9` and read the five live objects
they name (`~/.config/devin/mcp_config.json:7`, `~/.omp/agent/mcp.json:12`, `~/.kimi-code/config.toml:4722`,
`…/Ghidra/application.properties:17`, `.bashrc:28-29` with `GHIDRA_INSTALL_DIR=` and `JAVA_HOME=`):
**5 checks, 0 mismatches** (`w1/ExecBinder/live-16dfa009.json`: `checks_total 5, matched 5, mismatches 0,
unparsed 0, duplicates []`). No regression of the five cells.

### R80-C2 — freshness: receipt provenance (re-measured)

Population and rule reproduced independently: `git ls-tree -r --name-only <rev>` for
`.ufo/waves/round-{60..79}/l1/scores/*.json`, `/attacks/` excluded, keeping JSON objects with
`instrument.path` and a 64-hex `instrument.sha256`; each digest compared to `sha256` of the blob at the
tip, at the receipt's 40-hex declared rev, and at every `git rev-list --all -- <path>` revision.

```text
rev 16dfa009 → receipts 34, flagged 2, expected_control_flags 1, unexpected 1
             = [".ufo/waves/round-79/l1/scores/c2-at-landing.json"]
rev 72f8c6e9 → receipts 34, flagged 1, expected_control_flags 1, unexpected 0
revs b00419fb / 6037f599 / c935b543 → receipts 34, flagged 1, unexpected 0 (same flag set)
```

The single remaining flag is `.ufo/waves/round-69/l1/scores/prov-forged-instrument.json`, the declared
negative control. Committed receipts agree (`c2-at-base.json` flagged 2 / unexpected 1;
`c2-at-landing.json` flagged 1 / unexpected 0; `validate.defects []` on both). **1 → 0 unexpected**
across the same 34 receipts.

### R80-C3 — depth: clause-to-case binding with isolation proof (evidence-verified + counted)

```sh
git show b8260107:tools/round-78/attack-gate.py | grep -c 'defects.append'   # 9 inside validate_receipt (lines 782-807)
git show b8260107:tools/round-78/attack-gate.py | grep -cE '^[[:space:]]+case\("'   # 37 (16dfa009: 29)
git show 16dfa009:SKILL.md | grep -c 'Round-80 receipt-guard table'        # 0 → base rows 0
git show b8260107:tools/round-78/attack-gate.py | sha256sum
#   df6fb85670549ff1a03f925a3bed456cc3b64a311ae8681754c8efcc567149d6
```

Each of the nine declared case names appears exactly once in the gate source; the SKILL block at
`b8260107` has nine clause rows (`G01`…`G09`) with one declared case each. The receipt's
`target_pin.actual == expected == df6fb856…` is the `sha256` of the committed gate blob at `b8260107` —
re-derived above. `w1/ExecGate/mutants.json`: nine mutants, `isolating true` on all nine,
`own_case_failed true` on all nine, `other_cases_failed []` on all nine, `SELFTEST cases=37 failures=1`.
Base arm `rows 0 / bound 0 / survivors 9 / pristine 29/0`; landing arm `rows 9 / bound 9 /
survivors_count 0 / pristine 37/0` (`c3-at-base.json`, `c3-at-landing.json`, both `validate.defects []`).
**9 → 0 unpinned clauses**, one-to-one in the landed set.

Verbatim receipts `verbatim-{C1,C2,C3}.json` record the three printed commands with `exit 0` and
counters `candidate_false_greens 0`, `unexpected 0`, `survivors_count 0`; `plan-command-{C1,C2,C3}.json`
record the `tools/round-76/plan-command.py` prefix refusal, as the report discloses.

## 3. Per-axis verdicts

| axis | verdict | reason (evidence) |
|---|---|---|
| calibration | **improved** | C1 verified: 4 → 0 false greens on a frozen fixture set, with the do-nothing control still at 4 and both green controls bound; live arm 5/5, no regression |
| freshness | **improved** | C2 verified: 34-receipt population, unexpected 1 → 0, control still flagged, digests compared against committed blobs only |
| depth | **improved** | C3 verified: nine refusal clauses each bound to one SKILL row and one isolating case; survivors 9 → 0; pristine 29 → 37; pin re-derived from the committed blob |
| coverage | unchanged | no new surface class; the round's work is the lane's own instrument layer |
| operability | unchanged | instruments run and their printed commands were executed verbatim; no new operator-facing runbook |
| adjacency | unchanged | no cross-domain evidence claimed; `PROVINCE.md` untouched and its pointer cells re-read 5/5 |

No axis harmed: `git diff 16dfa009 72f8c6e9 -- SCORECARD.md` is additive only (81 insertions, 0
deletions), and `SKILL.md` changes are the two corrected registry tallies, four new registry rows and the
new decision table — no removed rows or lowered scores.

## 4. Discernment spot-check (LEARNING.md, checked from outside)

Sources re-opened both live and in the committed snapshots; quotes located by line.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S298 Python 3 `re` §`\b` | admit (new row, tier A, `mined`) | https://docs.python.org/3/library/re.html (live HTTP 200, 257 722 B) and `.ufo/waves/round-80/l1/sources/re.html:747` (sha256 `24ef5ff0…`) | **agree** | line 747 reads "Matches the empty string, but only at the beginning or end of a word." in both the live page and the snapshot; 14 words ≤ 25; it grounds the delimited-token rule exactly as `teaches` states. Snapshot sha matches the row |
| Wikipedia `JSON` | reject (no row; reason + flip recorded) | https://en.wikipedia.org/wiki/JSON (live HTTP 200, 478 308 B) and `w1/ScribeSources/wiki-json.html` (478 308 B) | **agree** | tertiary; the page does carry the ECMA-404 quotation "does not require that name strings be unique", so the stated reason (it would sit against the rule it illustrates) is true, and the flip is stated |
| S049 RFC 8259 §4 | re-open, no new row; `used-by` extended | `.ufo/waves/round-80/l1/sources/rfc8259.txt:322` (sha256 `61a5378f…`) | **agree** | line 322 reads "The names within an object SHOULD be unique."; the new knowledge entry cites S049 and the extended `used-by` names that entry — the old→new change is logged in `round-80.md` M80-6 |
| registry census | — | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | **exit 0** | 203 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 203), `malformed=0`, status histogram `mined=184 rejected=19`, 24 `W04` (23 pre-existing + S298) |

The gate decisions agree with the outside check on the round's one admit and its one reject, and the
round additionally refused a duplicate URL (RFC 8259 §4) before it landed (M80-6) — an admit-side
refusal, not a silent append.

## 5. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | **unchanged** | SOURCES 202 → 203 rows: one new row (S298, tier A) and one re-opened row (S049 `used-by`); no frontier → core move, and the new knowledge entry is on the instrument layer the coverage map already records as held (`corpus/README.md` row "Instrument and record layer, round 80"); no new source kind beyond `docs`/`spec` |
| quality | **improved** | two real defects in the lane's evidence apparatus found and fixed with receipts: the round-79 landing receipt now names a committed instrument blob (my sweep: unexpected 1 → 0 over 34 receipts) and the binder no longer gives a false unbound reason to a duplicate cell (my fixture re-derivation: 4 → 0); the gate gained eight isolating cases (29 → 37, survivors 9 → 0); pre-existing registry tallies corrected 26 → 37 and 19 → 21. D2 (three tallies made stale by the in-round repairs) is routed, not hidden |
| discernment | **improved** | the outside seats' findings are answered (C1 conjunction, symbolic-rev class, C3 printed command, binder `base_id`), a source was refused after opening, and my own spot-check agrees on both the admit and the reject |

## 6. Routed defects the lane must fix next round

1. **D1 — `corpus/SOURCES.md:324` search log contradicts the landed registry.** The round-80 note says
   "two included (S297/S298)" and ends "Rows 202 -> 204", but S297 was withdrawn before landing (M80-6)
   and the census reads 203 rows with one new row. The append-only log needs a new correction note naming
   the superseded text (never an in-place rewrite).
2. **D2 — three new registry tallies are stale after the in-round repairs.** `SKILL.md` rows say
   `--selftest` "33 cases" (pointer-bind), "8 cases" (strictness-battery), "14 cases"
   (receipt-provenance) and "19 cases" (guard-battery); the committed instruments at `c935b543`/tip
   register 34, 9, 16 and 19 `case("` calls respectively (33/8/14 at `b8260107`, so the repairs added
   1/1/2). The repair disclosure already says the battery reached "9 cases"; the rows were not swept.
3. **D3 — report count error.** The report says "the three claim rows and the four capability rows";
   `git diff 16dfa009 72f8c6e9 -- SCORECARD.md` adds three capability rows (plus four registry rows). A
   filed report takes an appended erratum naming the superseded text.
4. **D4 — report pointer overreach.** "All receipts are in `.ufo/waves/round-80/l1/scores/`" is false for
   the live arm, whose receipts are under `.ufo/waves/round-80/w1/` (`ExecBinder/live-16dfa009.json`,
   `CriticClaims/c1-live-head.json`). Same erratum as D3.
5. **D5 — report commit author-date precedes the lane tip it cites** (`5ac5b2b3` author 11:01:02 vs
   `72f8c6e9` 11:01:59; committer 11:02:21). Ordering holds on content and committer time; the lane
   should let the fleet helper stamp author = committer so the timeline reads straight.
6. **D6 — SCORECARD `freshness` row cites `--rev b00419fb` while its receipt records `6037f599`.** Both
   revisions re-derive `receipts 34 / flagged 1 / unexpected 0` (my sweep), so the score stands; align
   the citation next round.
7. **D7 — confirmed lane debt kept on the queue:** `w1/ExecProv/selftest.txt` is stale (19 cases /
   3 failures at 10:46:24 vs the 10:46:52 instrument's 0 failures); nothing in the landed tree depends on
   it, and the lane already routed it.

SHONEN: four boxes, all `[~]`, each with a resolvable pointer. Boxes 1–4 look checkable by a non-author
from committed artifacts (decision table + registry rows; three end-to-end counter runs; printed
commands executed verbatim; `PROVINCE.md` untouched and its cells re-bound), but promotion remains
operator-owned and is not claimed here.
