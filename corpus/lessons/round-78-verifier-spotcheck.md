author: hyaku closure (non-author integrator, @m_zfl)
round: 78 — kaidoku
date: 2026-11-04
verdict: admitted — both declared claims verified, no axis harmed

# Round-78 non-author verification (hyaku closure)

The lane did not author this document. It records the closure checks run against the filed report
(`.ufo/reports/round-78/kaidoku.md`) and the lane tip `f9fb37e5592b82038bf418e3d8b4aacb9f9ecf95`.
No lane-authored file was edited; this is the only path the closure writes in the lane repo. The
spot-check axis table below and the MANIFEST `rounds[]` entry carry the same verdicts.

## 1. Conformance (step 1)

| check | command | observed |
|---|---|---|
| report attribution | `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H' -- .ufo/reports/round-78/kaidoku.md` | `kaidoku-shokunin <kaidoku@shokunin.local> c8dc329d19fb2792a82abdc09308447380d33695` — lane identity, one commit, path clean |
| report pushed | `git merge-base --is-ancestor c8dc329d origin/main` | true (`report-in-origin-main`) |
| report lands after lane tip | report commit date vs lane tip | report `c8dc329d` commit date `2026-11-04T09:42:52-03:00`; lane tip `f9fb37e5` `09:42:35-03:00`; report cites the tip at line 17 and in the Landed-changes table |
| `SHONEN` heading | `grep -nE '^## ' .ufo/reports/round-78/kaidoku.md` | `## SHONEN` at line 182 with 4 lines (one per `SHONEN.md` box, 4 `[~]` marks, each with a pointer); no `[x]` (correct: the author may not attest) |
| cited lane commits | per hash `git rev-parse --verify -q "$h^{commit}"` then `git merge-base --is-ancestor "$h" refs/heads/main` | the report's 21 unique hashes all resolve and are ancestors of `refs/heads/main`; the stated pre-round HEAD `749c5717` is an ancestor; the extra lane commits named in `claims.json`/`LOG.md` (`e134045e`, `c9d986eb`, `d2ab5f3e`) also resolve as ancestors |
| lane tree pushed and clean | `scripts/hyaku/jj-lane.sh state …/kaidoku-shokunin`; `git -C … status --porcelain` | `branch=main local=f9fb37e5 remote=f9fb37e5 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `status --porcelain` empty; `git ls-remote origin refs/heads/main` = `f9fb37e5592b82038bf418e3d8b4aacb9f9ecf95` |
| prompt contract | compare `.ufo/prompts/kaidoku-round-78.md` §§1–5 with `templates/round-prompt.md` | byte-identical modulo `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions; §6 carries the hyaku addendum. Round items (mission/axes, 1–3 claims, L2 floor of 8 batched, commit-then-push, push scope, L0) all present; child items (report path/filename, commit before report, `SHONEN` heading, commit-hash citation, lane write scope) present |
| report sections | `grep -nE '^## ' …/kaidoku.md` | Work performed (10), Landed changes (69), Before → after (94), Sources & frontier (129), Trend verdicts (148), `SHONEN` (182) — required order present |

Conformance defects, all status-neutral (named again as routed items in §6): the report's Work-performed
"Filing" bullet and the SCORECARD round-78 paragraph still name the superseded receipt revisions
(`bc73b27a`, `3bb87162`); the SCORECARD says the gate "changed twice" while four supersessions are
disclosed; `attack-gate.py:1-940` is a stale range (the file is 949 lines); the LOG round-78 block is
appended under the round-77 heading rather than its own heading. None of these changes the lane status
or the claim verdicts.

## 2. Per-claim re-check (step 2)

Both claims are capability acquisitions on lane-owned gates. Per PROTOCOL §Gate standard (Closure
consequence) I did not execute a sibling gate; I re-derived the counters from the committed receipts
and verified each receipt's instrument digest against the committed instrument bytes at the revision
the receipt names. C2's live values I also re-derived myself from the live objects.

### R78-C1 — calibration (attack-class refusal) — evidence-verified

Counting command (from `claims.json`):
`python3 -I -B tools/round-78/attack-gate.py --root . --rev <measured> --work <scratch> --battery --json-out <receipt>`

- **Fixture population, re-measured:** `ls -d .ufo/waves/round-78/attacks/*/` → 10 directories
  (`a1-forged-receipt` … `b4-stale-gate-rev`), 4–6 files each; the `ATTACKS` table in
  `tools/round-78/attack-gate.py:68-93` names 10 classes with 10 distinct rules.
- **Before:** `git cat-file -e 6205ec8c:tools/round-78/attack-gate.py` → absent at base. In
  `pre/c1-at-base.json` (rev `3e6b1efc`) all ten `fixtures[].base.accepted` are `true`
  (`base_accepted 10`), the do-nothing control `pre/controls/c1-base-only.json` reports `refused 0`
  of 10, `all-refuse` reports `genuine.mismatch_count 1`, `no-fixtures` `base_accepted 0` — the
  reported values reproduce.
- **After (record `93753d88`):** re-counted from `l1/scores/c1-at-record.json` — `fixtures_total 10`,
  `refused 10` (every `refused: true`), `base_accepted 10`, `distinct_rules 10`, each fixture's
  `rule` equal to its declared id, `genuine.mismatch_count 0`, `genuine.defects []`,
  `genuine.record {in_scope_cells 4, groups 4, bound_clauses 12}`, `validate {defects [], fixtures 10}`.
- **After (tip `51c08cda`):** `l1/scores/c1-at-tip.json` reproduces the same counters and adds
  `genuine.population_floor {cells 4, clauses 8, met true}`; the three controls re-scored at the
  tip keep `base-only refused 0`, `all-refuse genuine 1`, `no-fixtures base_accepted 0`.
- **Digest bind:** `git show 93753d88:tools/round-78/attack-gate.py | sha256sum` =
  `a86f6d4d94987ac07a2c68ef18168ea23dc577cfb078dba90485a577cbda7d43` = the record receipt's
  `instrument.sha256`; at `51c08cda` = `961d5a23c1d38116f5b992434fa2295b5a90643b4a52233e205837ac73bf48c0`
  = the tip receipt's; at the declaration = `780089e3…` = the `claims.json` pin. The gate's three
  post-freeze revisions and the fourth wave revision are disclosed in `instrument_supersessions`
  (4 entries).
- **Self-test:** `pre/selftest-c1.json` exit 0 at rev `3e6b1efc`, 21 cases / 0 failures
  (stdout ends `SELFTEST cases=21 failures=0`) — the freeze-era tally. The final instrument's 26-case
  tally is stated in `w1/MutGate.md` ("selftest: exit 0, 26 cases, 0 failures") and the SKILL row,
  not in a machine receipt at the final revision — routed (R4).
- **Verdict: improved** (capability acquisition verified; the counter's before state is absent and
  the frozen instruments accept all ten fixtures, the after state refuses all ten and keeps the
  genuine record clean).

### R78-C2 — freshness (surface recheck) — evidence-verified + live values re-derived

Counting command (from `claims.json`):
`python3 -I -B tools/round-78/surface-recheck.py --battery --root . --rev <measured> --json-out <receipt>`

- **Before:** `pre/c2-at-base.json` (rev `3e6b1efc`, instrument sha `e7ea1717…`) exit 1,
  `checks_total 8`, `matched 6`, `mismatches 2`, `unparsed 0` — `jdk-version` record `21.0.12.1`
  vs live `21.0.13`; `omp-rea-disable` record `false` vs live `true`. The record text at the
  declaration is byte-identical to base: `git diff 6205ec8c 3e6b1efc -- PROVINCE.md` → 0 lines.
- **After (record `93753d88` and tip `51c08cda`):** both receipts exit 0 with `checks_total 8`,
  `matched 8`, `mismatches 0`, `unparsed 0`, `validate {defects [], checks 8}`, `checked_at`
  `09:15:23` / `09:41:21 -03:00`; instrument sha `e7ea1717…` matches `git show
  <rev>:tools/round-78/surface-recheck.py | sha256sum` at both revs and the declaration pin.
- **Live re-derivation by the closure (plain reads, today):** `java -version` →
  `openjdk version "21.0.13"`; Ghidra `application.version=12.1.4`; OMP
  `disabledServers: ["rea"]` and `rea` args `rea-agents@6.7.0`; Devin `rea` args `rea-agents@6.7.0`;
  Kimi `rea-agents@6.7.0` (line 4722). `PROVINCE.md` lines 18–20 and 27 carry the corrected values
  and the 2026-11-04 recheck pointer.
- **Control:** `pre/c1`'s counterpart `pre/controls/c2-token-grep.json` (rev `6205ec8c`) matches 6 of
  8, mismatches 2; at the tip it matches 7 of 8 (mismatch 1, the `omp-rea-disable` claim a token grep
  cannot see); selftest case `red-token-grep-accepts` passes in `pre/selftest-c2.json` (12 cases,
  0 failures, rev `3e6b1efc`).
- **Pointer gap found by the closure (routed, R3):** the record's OMP pointer
  `~/.omp/agent/mcp.json:8` now points at `"type": "stdio"` (the pin is line 12) and its Kimi pointer
  `~/.kimi-code/config.toml:4126` now points at `max_output_size = 128000` (the pin is line 4722).
  The values are correct, but `surface-recheck.py:201-208` compares `pointer.split(":")[0]` — the file
  only — so a stale line suffix passes.
- **Verdict: improved** (the two real drifts are corrected with a dated receipt and the value set
  re-derives 8/8 against the live objects; the line-pointers are a remaining gap, not a regression).

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | R78-C1 verified (10/10 declared-rule refusals, 10/10 base acceptances, genuine record clean, instrument digests bound); capability row `attack-class refusal` entered; SCORECARD claim verdict `improved` |
| freshness | improved | R78-C2 verified (6/8 → 8/8; the two live drifts corrected with the 2026-11-04 pointer; digests bound); capability row `surface recheck` entered |
| coverage | unchanged | no coverage-map ground moved: the new row 119 says "held …, not a new carrier class"; no frontier → core move; SOURCES 197 → 200 rows is registry work, not admitted knowledge on uncovered ground |
| depth | unchanged | no depth claim; the two SKILL rows are registry/exit-contract rows, not a new decision-table block |
| operability | unchanged | the two gates are runnable and registered, but the round scores that work as the calibration/freshness capabilities, not as an operability axis move |
| adjacency | unchanged | the wave's `ConnectorSibling` cross-check was used in-round; nothing from a sibling lane was absorbed |

No axis harmed: `git -C … diff 749c5717 f9fb37e5 -- SCORECARD.md | grep '^-' | grep -v '^---'` → no
lines (the round only adds capability rows and its round section; no score or evidence was removed).

## 4. Discernment spot-check (LEARNING.md — non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S292 `stdtypes` (Python docs, 2026-11-04) | admit (mined, tier A) | committed snapshot `.ufo/waves/round-78/l1/sources/stdtypes.html` lines 440–441 (814 496 B, sha256 `16f072e1…`); live `https://docs.python.org/3/library/stdtypes.html` re-fetched | agree | the quote "In addition, Booleans are a subtype of integers" is present (line 440→441) and still served live; 8 words; it grounds the bool-excluded integer guard the knowledge entry cites. Minor: the anchor says line 441 while the sentence starts on 440 |
| S293 `tomllib` (Python docs, 2026-11-04) | admit (mined, tier A) | `tomllib.html` lines 221–223 (34 923 B, sha256 `d98e62f7…`); live URL re-fetched | agree | both sentences of the quote are present ("…parsing TOML 1.1.0 … does not support writing TOML"), 17 words; it grounds parsing the Kimi TOML instead of grepping it |
| S294 GnuPG handbook (2026-11-04) | reject (tier C) | `gnupg-manual.html` line 1017 (113 892 B, sha256 `6d8e63bd…`); live URL re-fetched | agree | the quote is exact (11 words); the reject reason — a signature authenticates a key holder, not a receipt's fields, and the lane has no signer/key — is sound and the flip condition is stated |
| refused reuse `re.html` / `hashlib.html` | not a row | `corpus/SOURCES.md` lines 149 (S143) and 180 (S263) | agree | both URLs are already held; a duplicate URL would be a registry defect (the round's own M78-1 shows the census only warns W04) |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0,
200 rows, the 23 W04 duplicate-URL warnings (none on S292–S294); `grep -cE '^\|…S[0-9]{3,}…\|'
corpus/SOURCES.md` → 200. Spot-check agrees with every gate decision; no disagreement is left
unlearned.

## 5. Trend verdicts

- **expansion: unchanged.** Three rows enter (S292/S293 mined, S294 rejected; 197 → 200 rows, census
  exit 0 both ends) but both knowledge entries sit on the lane's own record layer, which the
  coverage map (row 119) marks "held …, not a new carrier class"; no new source kind, no frontier →
  core move, no new carrier. Correctly not claimed as expansion.
- **quality: improved.** Two real record drifts found at the base text and corrected with a dated
  receipt (`jdk-version` 21.0.12.1 → 21.0.13; `omp-rea-disable` false → `disabledServers: ["rea"]`);
  the round's own gate was run on the genuine record and its three self-found defects (plus the wave's
  fourth revision) are disclosed; QUALITY rows 136–137 add the two criteria with the lesson pointers.
- **discernment: improved.** The outside spot-check agrees 3/3 with the gate (two admits, one
  reject); the wave's independent seats re-derived the counters and found real gaps (`receipt_auth`
  mode, plural near-miss stems, population floor); the two mutation survivors (`m03`, `m08`) and
  `SentinelScope`'s unverified escape claim are recorded as routed items, not passes. The pointer-line
  gap above is routed here, not adopted.

## 6. Routed defects the lane must fix next round

1. **Stale filing-receipt revisions in prose (report + SCORECARD).** The report's Work-performed
   "Filing" bullet says the prefile gate passed at `bc73b27a` (`prefile-at-filing.json`) and
   `3bb87162` (`gate-at-tip.json`); the committed receipts now both carry `rev e2846648` because
   `f9fb37e5` re-took them (the tip-only diff is exactly those two files). The report's opening
   paragraph and Landed-changes row correctly give `e2846648`, so the filed report is internally
   inconsistent. Fix: append a correction naming the current receipts (report is filed once; never
   rewrite it) and correct the SCORECARD pointer in the next round's record.
2. **SCORECARD supersession count.** Line 6041 says "The gate changed twice after the freeze; both
   commits (`59a92fbd`, `01768ac5`)", but `claims.json` discloses four supersessions (also
   `1a99064b`, `e134045e`) and the same SCORECARD section's wave paragraph names the other two. Fix:
   restate the count/list in the next round's record.
3. **Stale line pointers + path-only pointer rule.** `PROVINCE.md`'s OMP pointer `:8` and Kimi
   pointer `:4126` no longer point at the pin lines (12 and 4722 today); `surface-recheck.py`
   compares only `pointer.split(":")[0]`. Fix: correct the two pointers and add a line-pointer arm
   (or drop line suffixes from the record) with a red selftest case, so a moved line is a mismatch.
4. **Final-instrument self-test receipt.** The machine tally is `pre/selftest-c1.json` at the
   21-case freeze instrument; the final instrument's 26-case tally lives only in `w1/MutGate.md`
   and the SKILL row. Fix: commit a `--selftest` receipt at the final instrument revision (and
   reference it from the registry row) next round.
5. **Stale line range.** The report cites `tools/round-78/attack-gate.py:1-940`; the file is 949
   lines at the tip. Fix: correct the range in the next round's record.
6. **LOG structure.** The round-78 block is appended as bullet items under the round-77 heading
   (no `## 2026-11-04 — round 78 …` heading), though the report calls it the round-78 entry. Fix:
   open the next entry with its own heading; do not rewrite the filed bytes.

## 7. Limits of this check

- I did not execute either lane gate (Gate standard: the integrator verifies committed evidence, not
  a sibling's gate). C1's counters are re-derived from the committed receipts and bound by the
  instrument digests above.
- The live surface values were re-derived at closure time (2026-11-04T12:51Z); the receipts' own
  `checked_at` is the lane's measurement time, and a later host change would invalidate the receipt,
  not this spot-check.
- The `prefile` and freeze-gate receipts are the lane's evidence; I verified their revision, exit and
  verdict fields and the 53-row ledger count (`grep -c '^round-' corpus/claim-freezes-v2.tsv` → 53),
  not the gates' internal logic.
