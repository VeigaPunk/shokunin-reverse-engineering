author: hyaku closure (non-author integrator, @m_zfl)
round: 79 — kaidoku
date: 2026-11-04
verdict: admitted — both declared claims verified, no axis harmed

# Round-79 non-author verification (hyaku closure)

The lane did not author this document. It records the closure checks run against the filed report
(`.ufo/reports/round-79/kaidoku.md`, fleet commit `58088c38`) and the lane tip
`369fa6e7fe1af5c65f1014da2ef509e379ea9a10`. No lane-authored file was edited; this is the only path
the closure writes in the lane repo. The per-axis table in §3 and the MANIFEST `rounds[]` entry carry
the same verdicts.

## 1. Conformance (step 1)

| check | command | observed |
|---|---|---|
| report attribution | `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H' -- .ufo/reports/round-79/kaidoku.md` | `kaidoku-shokunin <kaidoku@shokunin.local> 58088c387a00e67fb441d6211e90ef6345c3625e` — lane identity, one commit, path clean in `git status --porcelain` |
| report lands after the lane work | `git log --format='%h A=%ad C=%cd'` on the report commit and the lane tip | report `58088c38` committer date `2026-11-04T10:23:02-03:00`; lane tip `369fa6e7` committer date `2026-11-04T10:22:03-03:00`; the report cites the tip at its header and in `Landed changes` (a jj describe keeps the earlier author date `10:18:10`, which is why the committer date is the one read) |
| report pushed | `git merge-base --is-ancestor 58088c38 HEAD` (fleet) | true |
| `SHONEN` heading | `grep -nE '^## ' .ufo/reports/round-79/kaidoku.md` | `## SHONEN` at line 156 with exactly 4 box lines, all `[~]` with a resolvable pointer; no `[x]` (correct: the author may not attest) |
| report sections in order | same grep | Work performed (9), Landed changes (57), Before → after measurements (76), Sources & frontier (105), Trend verdicts (127), `SHONEN` (156) — all required sections present in contract order |
| cited lane commits | per hash `git -C …/kaidoku-shokunin rev-parse --verify "<h>^{commit}"` then `git merge-base --is-ancestor <h> refs/heads/main` | 11 hashes resolve and are ancestors of `refs/heads/main`: base `29d2ca30`, `a1f9b81c`, `ed68cd0a`, `e0c19339`, `da8e5d5e`, `868710d6`, `1caf23ed`, `4e23255a`, `eb301514`, `dd10ffd3`, `954ed89c`, `369fa6e7` (the branch ref was used, never `@{u}`: HEAD is detached under jj) |
| lane tree pushed and clean | `scripts/hyaku/jj-lane.sh state …/kaidoku-shokunin`; `git -C …/kaidoku-shokunin status --porcelain` | `branch=main local=369fa6e7 remote=369fa6e7 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `status --porcelain` empty; `git ls-remote origin refs/heads/main` = `369fa6e7…` |
| prompt contract | `diff` of `templates/round-prompt.md` (substituted) against `.ufo/prompts/kaidoku-round-79.md` §§1–5; heading scan | 704 lines; §§1–5 byte-identical modulo `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}`; §6 hyaku addendum (run-15 + amendments), §7 scratch discipline. Round items present: mission/axes binding (line 3–8), 1–3 causally-separable claims on distinct axes with the lowest-axis rule (9–41), frontier step (42–79), L2 floor of ≥8 in one batched call (80–98), commit-then-push ordering and push scope (131–137), L0 side channel (138–140). Child items present: report path/filename (101), commit-before-report and hash citation (511 and the SHONEN pre-commit check at 518), `SHONEN` heading requirement (118), lane write scope (556–570) |
| axes string | prompt line 6 vs `shokunin.conf:45` | both `coverage + depth + calibration (reverse engineering with REA)` — no drift |
| dispatch digest (copied; the log is mutable) | `.ufo/watchdog.log` | `2026-11-04T09:54:27-03:00 launch kaidoku round=79 pgid=1289363 driver=hyaku-inline attempt=1`; `2026-11-04T10:23:45-03:00 complete kaidoku round=79; hyaku-inline attempt=1` |
| fleet worktree leftovers | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | 16 entries, none round-79 lane-authored (`.scratch/*`, `.ufo/l0-questions.md`, `scripts/hyaku/*`, `.ufo/reports/round-82/{kama,tameshi}.md`, `.ufo/reports/round-87/mori.md`, `after`) |

The report is a real report, not a marker: it names committed work, cites resolvable commits and
carries the required sections.

## 2. Per-claim re-check (step 2)

Both claims are capability acquisitions on lane-owned gates. Per PROTOCOL §Gate standard (Closure
consequence) I did not execute either gate; I verified each committed receipt, its instrument digest
against the committed instrument bytes at the revision it names, and re-derived the counter's
before→after with plain reads of the committed and live bytes.

### R79-C1 — calibration (selftest mutation battery) — evidence-verified + plain re-measure

Counting command (from `claims.json`):
`python3 -I -B tools/round-79/gate-mutation.py --root . --rev <measured> --work <scratch> --battery --json-out <receipt>`

- **Mutant population, re-measured:** `tools/round-79/gate-mutation.py:60-130` defines 8 mutants
  (`m01-auth-dead` … `m08-validate-no-refusal-guard`); `SOLE_REQUIRED` (line 45) names `m03`, `m05`,
  `m08`. The instrument digest recorded in both receipts is `ff74d63713524f37636257c53ccbe64a64e475b6e9cab7fd7ebcf26d85b3ed02`
  = `git show 868710d6|HEAD:tools/round-79/gate-mutation.py | sha256sum` — both arms were taken with
  the final bytes.
- **Before (base `29d2ca30`),** `l1/scores/c1-at-base-final.json`: exit 1, `mutants_total 8`,
  `killed 5`, **`survivors 3`** = `survivor_ids [m03-near-miss-re-dead, m05-atom-absent-bound,
  m08-validate-no-refusal-guard]` = `sole_missing`, `declared_case_hits 5`. `target_pin.actual`
  `961d5a23c1d38116f5b992434fa2295b5a90643b4a52233e205837ac73bf48c0` =
  `git show 29d2ca30:tools/round-78/attack-gate.py | sha256sum`; expected (and `matched false`) the
  landing digest — the base arm differs as designed. Pristine selftest `26 cases, 0 failures`.
- **After (record `ed68cd0a`),** `l1/scores/c1-at-landing.json`: exit 0, `mutants_total 8`,
  `killed 8`, **`survivors 0`**, `survivor_ids []`, `declared_case_hits 8`, `sole_missing []`,
  each of `m03`/`m05`/`m08` `sole_detector true` and `killed_by_declared true`; `target_pin.matched
  true` with `actual` = `4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf` =
  `git show ed68cd0a:tools/round-78/attack-gate.py | sha256sum` = the HEAD worktree digest;
  `target.bytes 46214` matches. Pristine selftest `29 cases, 0 failures`.
- **Selftest tallies, re-measured by static count of the `case()` calls plus the committed receipts:**
  `tools/round-78/attack-gate.py` selftest `case()` calls 26 at `29d2ca30` and 29 at `ed68cd0a`
  (re-derived from the blobs, not from the report); `pre/selftest-gate.txt` ends
  `SELFTEST cases=29 failures=0` (committed at the declaration, `a1f9b81c`); the final
  `gate-mutation.py` has 14 selftest cases and `pre/selftest-c1.json` ends
  `SELFTEST cases=14 failures=0`.
- **Control, verified from the receipt:** `l1/scores/c1-empty-set-final.json` — `control empty-set`,
  `mutants_total 0`, `ok false` (a declared population floor, not a pass).
- **Verdict: improved.** The base state is a genuine do-nothing arm (3 survivors, target pin missed);
  the after state kills all eight with their declared cases and makes the three named mutants sole
  detectors.

### R79-C2 — freshness (line-bound pointer binding) — re-measured live + evidence-verified

Counting command (from `claims.json`):
`python3 -I -B tools/round-79/pointer-bind.py --root . --rev <measured> --json-out <receipt>`

- **Before (record at `29d2ca30`), re-measured myself from the committed `PROVINCE.md` and the live
  files:** the record's pointers are OMP `:8` and Kimi `:4126`.
  `sed -n '8p' /home/vgpnk/.omp/agent/mcp.json` → `"type": "stdio",` (not the pin);
  `sed -n '4126p' /home/vgpnk/.kimi-code/config.toml` → `max_output_size = 128000` (not the pin);
  `sed -n '7p' /home/vgpnk/.config/devin/mcp_config.json` → `"rea-agents@6.7.0",` (pin holds);
  Ghidra `application.properties:17` → `application.version=12.1.4` (holds); `.bashrc:28-29` →
  both exports (holds). That is 3 matched / 2 mismatched —
  `l1/scores/c2-at-base-final.json` reports exactly `checks_total 5, matched 3, mismatches 2,
  unparsed 0`, naming `omp-pin` and `kimi-pin`.
- **After (record `ed68cd0a`), re-measured myself:** the record's pointers are OMP `:12` and Kimi
  `:4722`; `sed -n '12p' /home/vgpnk/.omp/agent/mcp.json` → `"rea-agents@6.7.0",` and
  `sed -n '4722p' /home/vgpnk/.kimi-code/config.toml` → `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`
  (the file is 4746 lines). All five pointers name the declared live object at the line they name —
  5 matched / 0 mismatched, matching `l1/scores/c2-at-landing.json` (`checks_total 5, matched 5,
  mismatches 0, unparsed 0`).
- **Control, verified from the receipt:** `l1/scores/c2-path-only-final.json` — `control path-only`,
  `mismatches 0` on the stale base record but `ok false` and `would_pass true`: the rule that cannot
  fail, recorded as such and never a pass.
- **`--validate` evidence:** the landing validate line `{"checks": 5, "defects": [], "matched": 5}`
  is committed at `.ufo/waves/round-79/w1/CriticClaims/validate-combined-c2.txt` (and the C1
  `{"defects": [], "mutants": 8, "survivors": 0}` at `w1/ReviewerC1/validate-log.txt:5`).
- **Defect found by this check (routed, §6.1):** `c2-at-landing.json` records instrument
  `a0044c4c5006ac0f7e7fe57513c28bc9f98002aaab188575b87b0377466f9811`, which matches **no** committed
  blob of `tools/round-79/pointer-bind.py`: the committed revisions are
  `91d23dade98d831f…` (declaration `a1f9b81c` and freeze `ed68cd0a`) and
  `40905d396245313b…` (`868710d6` … tip, and the current worktree). The before arm and the path-only
  control *were* re-taken with the final bytes; the after arm was not. The report's "with the final
  instrument bytes" is therefore inaccurate for that one receipt. The claim's truth survives: the
  final rule's extra conjuncts (declared live object plus scored conjuncts) are satisfied by the same
  bytes I read myself, and the counter's before→after direction is independently reproduced above.
- **Verdict: improved.** Two real drifts in the record are corrected with a dated receipt and the
  value set re-derives 5/5 against the live objects.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | R79-C1 verified: survivors 3 → 0, `declared_case_hits 5 → 8`, target pin missed → matched, pristine 26 → 29 cases, mutant set 8; capability row `selftest mutation battery` entered; SCORECARD claim verdict `improved` |
| freshness | improved | R79-C2 verified: mismatches 2 → 0, 5/5 bound at `:12`/`:4722` (live reads above), path-only control recorded as unable to fail; capability row entered (worded as a revision of the round-78 pointer rule) |
| coverage | unchanged | coverage-map row 120 added for a ground already marked "held … not a new carrier class"; stem recipe maps 162/162 (`coverage-selfcheck-at-record.json`, `mismatches 0`), the same 10.0 as the round-76 re-derivation; no score moved |
| depth | unchanged | the two SKILL rows are registry/exit-contract rows; no decision-table or craft block was added or deepened this round |

No axis harmed: `git -C …/kaidoku-shokunin diff 29d2ca30 369fa6e7 -- SCORECARD.md` removes only the
superseded coverage-row wording (157/157 → 162/162, same 9.72 → 10.0 pair) and adds the capability
rows and the round-79 section — no score line decreased.

## 4. Discernment spot-check (LEARNING.md — non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S295 POSIX.1-2024 `grep` (2026-11-04) | admit (mined, tier A) | committed snapshot `.ufo/waves/round-79/l1/sources/grep-posix.html` (21 316 B, sha256 `9473205c…`) line 97; live `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html` re-fetched (HTTP 200, 21 316 B) | agree | the quote "Precede each output line by its relative line number in the file, each file starting at line 1." is present verbatim at the named line, 18 words; the `-n` numbering rule does ground the binder's 1-based per-file line rule |
| S296 cargo-mutants book, Welcome (2026-11-04) | admit (mined, tier B) | committed snapshot `.ufo/waves/round-79/w1/ScribeSources/cargo-mutants.html` (22 602 B, sha256 `d056b2b3…`) lines 184-186; live `https://mutants.rs/` re-fetched (HTTP 200, 22 602 B) | agree on the admit; disagree on the word count | the quote "quality by finding places where bugs can be inserted without causing any tests to fail" is contiguous and exact (15 words by `len(quote.split())`), so the ≤25-word bar holds — but the row, the lesson and the LOG record "17 words"; the tier-B scoping (a tool's book, not the technique's specification) is right |
| reject sample | none exists in this round | `corpus/lessons/round-79.md` `## Gate`: "no source was refused this round (the duplicate check ran before the append)"; the newest rejected row is S294 (round 78) | n/a — reject side unexercised | a round that admits two sources and refuses none gives the outside check nothing to test on the reject side; recorded as routed (§6.5), never as `harmed` |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0,
202 rows, the same 23 W04 duplicate-URL warnings (none on S295/S296). Rows before → after 200 → 202
(`git show 29d2ca30:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → 200;
`grep -cE … corpus/SOURCES.md` → 202); tiers A:1, B:1; no existing row's `status`/`recheck`/`used-by`
changed (`git diff 29d2ca30 369fa6e7 -- corpus/SOURCES.md` is two added lines). Both snapshots are
byte-identical to the independent source-seat fetches (same sha256s under `w1/ScribeSources/`).

## 5. Trend verdicts

- **expansion: unchanged.** Two rows enter and one knowledge entry lands
  (`corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md`), but on the lane's own
  instrument/record layer, which the coverage map marks "held …, not a new carrier class"; no
  frontier → core move, no new source kind. The lane claims the same and it reproduces (knowledge
  files 162, stem map 162/162).
- **quality: improved.** Two real record drifts are corrected with a dated receipt (`:8 → :12`,
  `:4126 → :4722`), the gate's selftest gains three behavioural cases (26 → 29, machine receipt
  `pre/selftest-gate.txt`), and five wave-forced instrument repairs are disclosed with unchanged
  predicates, counters and kill rules. The knowledge entry's two quotes re-open exactly; no admitted
  entry was found false. The defects this check found (after-arm instrument digest, registry tally)
  are routed, not failures of an admitted entry.
- **discernment: improved.** The outside spot-check agrees with the gate on both admits. The reject
  side had no sample this round (routed). The wave's disagreements did become grounded criteria:
  QUALITY rows 138–140 cite the round-79 lesson (M79-2/3/4) and the instruments, and the three
  findings that could not be adopted in-round (source-text vs behaviour cases, receipt authenticity,
  `freshness` as a fleet axis) are named as routed rather than scored green.

## 6. Routed defects the lane must fix next round

1. **C2 after-arm receipt names an unrecoverable instrument revision.** `c2-at-landing.json` carries
   instrument `a0044c4c…`, which is no committed blob (committed: `91d23dad…` at `a1f9b81c`/
   `ed68cd0a`, `40905d39…` from `868710d6` to the tip). The before arm and the path-only control
   carry the final `40905d39…`. Fix: re-take the landing receipt with the committed instrument and
   commit it (or disclose the intermediate revision in `instrument_supersessions`); until then the
   filing sentence "with the final instrument bytes" is wrong for that receipt.
2. **Registry row tally and entry command.** `SKILL.md:1914` says `pointer-bind.py --selftest` has
   19 cases; the final instrument has 21 (`pre/selftest-c2.json` ends `cases=21`, and 21 `case()`
   calls in the committed file). The two round-79 rows also omit the entry (counting) command that
   older rows carry in that column. Fix: restate the tally and add the entry command in the next
   round's registry update.
3. **S296 word count.** The SOURCES row, `corpus/lessons/round-79.md` and `LOG.md` say "17 words";
   the quote is 15. Fix: an appended correction naming both values (append-only; never rewrite).
4. **R79-C2 is declared on `freshness`, which is not one of the lane's owned axes** (coverage, depth,
   calibration per `SCORECARD.md` and `shokunin.conf:45`), and no axis-addition claim or owned-axis
   row landed. The wave's critic flagged it (Q5) and the lane recorded but did not adopt it. Fix:
   either add `freshness` to the owned axes with its evidence row, or re-label the claim on the
   owning axis next round.
5. **No rejection decision in the round's `## Gate`.** The outside discernment check had no reject to
   sample. Fix: record at least one considered-but-rejected candidate with its reason and flip
   condition (a rejection is evidence of taste), so the next spot-check covers both halves.
6. **Capability naming.** The `## Capabilities` table row is `line-bound pointer rule` while the
   report and the SCORECARD prose call it `line-bound pointer binding`. Fix: reconcile the name in
   the next record (the capability table is the registry of record).

## 7. Limits of this check

- I did not execute either lane gate (Gate standard: the integrator verifies committed evidence, not
  a sibling's gate). C1's counters are re-derived from the committed receipts and bound by the
  instrument and target digests above; C2's values were re-derived by plain reads of the live files.
- The live values were read at closure time (2026-11-04T13:31Z); a later host edit invalidates the
  receipt, not this check.
- `.ufo/watchdog.log` is mutable; the dispatch/completion digest in §1 is the pointer of record.
- SHONEN boxes 1–4 look checkable by a non-author from the committed pointers (instruments, LOG
  entry, plan, PROVINCE receipt); promotion remains operator-owned.
