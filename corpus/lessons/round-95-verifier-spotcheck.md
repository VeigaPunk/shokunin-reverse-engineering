author: hyaku closure (non-author integrator, @m_zfl)

# kaidoku round-95 — non-author verifier spot-check (closure, 2026-11-05)

Scope: closure verification of `.ufo/reports/round-95/kaidoku.md` (fleet repo) against lane tip
`51a90c757696e725be5e8a89a53f0991bf757583`, base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`,
declaration `4bda1d1dd3788973f10e61212b70df18b3b14ea0`. Every command below was run by the
verifier at closure time; receipts are read as committed bytes only. No sibling gate or
selftest was executed (PROTOCOL §Gate standard, Closure consequence): the round-95
instruments carry no registry row in SKILL.md, and the claims' frozen batteries are
evidence-verified through their committed receipts.

## 1. Conformance

- Report committed in the fleet repo by the lane identity:
  `git log --format='%an %ae %H' -- .ufo/reports/round-95/kaidoku.md` →
  `kaidoku-shokunin kaidoku@shokunin.local a1664f6c58a9efb533c74645076bdffc8b806113`. PASS.
- `## SHONEN` heading with one line per box: 4 boxes in `SHONEN.md`, 4 `[~]` lines in the
  report (`grep -cE '^- \['` = 4 / 4). PASS.
- Cited lane commits exist and are ancestors of the branch ref `main` (jj-colocated; ancestry
  tested against the ref, not `@{u}`):
  `git merge-base --is-ancestor 4bda1d1d… main` → OK;
  `git merge-base --is-ancestor 51a90c75… main` → OK;
  `git merge-base --is-ancestor b5331db1… main` → OK. PASS.
- No uncommitted round work; pushed:
  `scripts/hyaku/jj-lane.sh state <lane>` → `branch=main local=51a90c75… remote=51a90c75…
  ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` → empty. PASS.
- Dispatch digest (copied verbatim from `.ufo/watchdog.log`, lines 2877/2886):
  `2026-11-05T13:12:14-03:00 launch kaidoku round=95 pgid=2368305 driver=hyaku-inline attempt=1`
  `2026-11-05T14:04:34-03:00 complete kaidoku round=95; hyaku-inline attempt=1`. PASS.
- Prompt fidelity: `.ufo/prompts/kaidoku-round-95.md` is the `templates/round-prompt.md`
  rendering (sections 1–5 byte-match modulo placeholders) plus the declared hyaku addendum §6;
  the five child-lane items (report path/filename §4, commit-before-report ordering §5,
  `SHONEN` heading §4, commit-hash citation rule §4, write scope §5) and the round-level
  items (mission/axes binding §1, L2 floor ≥8 §3, commit-then-push §5, push scope §5, L0
  side channel §5) are present. The quoted L2 map ("at least 8 L2 subagents in ONE batched
  AgentSwarm call") matches `MISSION.md` §L2 concurrency ("at least 8 L2 subagents per
  round"). PASS.
- Report is a real report, not a marker: work performed, landed changes tied to LOG entries
  and commits, before→after measurements, Sources & frontier, trend verdicts, SHONEN. Status
  `ok`.

## 2. Per-claim re-check

### R95-C1 — calibration (evidence-verified; committed receipts re-read)

Before (base `b5331db1`, committed `pre/` receipts):

- `jq -c '{met, counts_of_4}' .ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json` →
  `{"met":true,"counts_of_4":{"agree":4,"predicted":4,"valid":4}}` — the pinned round-94
  counter admits all 4 forgeries, as reported.
- `jq -c '{victim_intact, verdict}' .ufo/waves/round-95/pre/c1-symlink-v4-at-base.json` →
  `{"victim_intact":false,"verdict":"followed-symlink"}` — the v4 writer follows the planted
  `<json-out>.tmp` symlink, as reported.

After (`4bda1d1d`, committed `l1/scores/` receipts):

- `jq -c '{expect_ok, before, forgeries, honest}' l1/scores/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`
  → `expect_ok:true`; `before {admits:true, met:true, exit:0}`; all four forgeries
  `refused:true, exit:1`, each with exactly its intended reason (pos→`label-not-frozen`,
  F1→`label-not-recomputed`, F2→`revision-not-bound`, F3→`pins-not-bound`); honest leg
  `exit:0, met:true, valid:true`.
- Fixture spot-check: `jq -r '.revision' forgery/forge-F2.json` → `8a40ceb65` (9 chars, the
  M94-f shape). Forgery rc pins: `forge-F1.rc=forge-F2.rc=forge-F3.rc=1`, `forge-pos.rc=0`
  (the old counter accepts pos — the before-arm behaviour).
- `jq -c '{met_target, revision, exit, expect}' l1/scores/honest-pos.json` →
  `met_target:true, revision:"4bda1d1dd3788973f10e61212b70df18b3b14ea0", exit:0, expect:"repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2"`;
  counts `repaired 12, wrong 0, unsafe 0, intact 6, far_refused 12, fresh_roundtrip 2` match
  the frozen label; `honest-pos.rc` = 0.
- `jq -c '{verdict, victim_intact, receipt_valid, tmp_is_symlink, writer_rc}' l1/scores/c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`
  → `hardened, victim_intact:true, receipt_valid:true, tmp_is_symlink:true, writer_rc:1`
  (planted link left in place; v5 writer refused it).
- Pin integrity (my own measurement): `sha256sum -c .ufo/waves/round-95/pins.sha256` → 28/28
  OK, 0 mismatches — the pinned counter bytes are unchanged between declaration and landing.

Verdict: **improved** (verified on the committed receipts; the frozen predicate's before and
after both reproduce from committed bytes).

### R95-C2 — depth (evidence-verified; committed receipts + committed bytes)

Before (base): `pre/c2-base-block34-stdout.txt` → `failing exit 1 / block 34 missing (craft
has 33 blocks)`; `pre/c2-base-depth-v2.txt` → `blocks 33 resolved 33 expect 34 … exit=1`;
`pre/c2-base-depth-v3.txt` → `blocks 33 … required-shaped 0/0 … exit=1`. As reported.

After:

- `jq -c '{tool, revision, manifest_block, exit, atoms}' l1/scores/c2-after-block34-worktree.json`
  → `exit:0`, `manifest_block:34`, `atoms {block_present,marker,shape} all true`, four rows
  cite QUALITY 191/192 with `missing_keywords:[]`.
- Junk control: `l1/scores/c2-junk-worktree.json` → `exit:1`, `failing` rows cite the three
  missing keyword sets (`str() fallback`, `complete JSON or absent`, `helper-only selftest`)
  — not a rubber stamp.
- My own committed-bytes check (independent of the worktree measurement):
  `git show 51a90c75…:SKILL.md | grep -c 'receipt-world-binding v1'` → 1; block 34 with its
  four table rows is in the landing commit; `corpus/QUALITY.md` rows 191 and 192 are at the
  landing (`git show 51a90c75…:corpus/QUALITY.md`, lines 327–329).

Deviation noted (status-neutral): the declared frozen commands name `--rev <landing>`; the
after-side receipts record `revision:"worktree"` (measured at the landing worktree because
the craft block is landed after the freeze). The report discloses this. The landed commit's
bytes carry the block, so the worktree measurement is anchored; the residual gap is that no
receipt re-runs the counter at the landing hash. Routed below as R95-VD-1.

Verdict: **improved** (evidence-verified).

### No axis harmed

`git diff b5331db1… 51a90c75… -- SCORECARD.md` → only the round-95 section, one capability
row (`world-bound receipt battery with a symlink-safe writer`, first working round 95), and
the planned/limits text. No score row changed; all four owned axes (coverage, depth,
calibration, freshness) remain 10.0 on their finite proxies. No axis harmed.

## 3. Discernment spot-check (LEARNING.md; outside non-author)

Sample from `corpus/lessons/round-95.md` `## Gate`: the one admit (S320) and the explicit
non-admission from the same page (the `O_PATH` interaction and the other `O_NOFOLLOW`
occurrences). Re-opened source: the committed fetch evidence
`.ufo/waves/round-95/l1/scores/s320-open2-fetch{1,2}.html` (byte-identical re-fetches; also
matches the live page contract via the entry's `recheck` command shape).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S320 admit (`open(2)` `O_NOFOLLOW` trailing-component rule) | admit | `s320-open2-fetch1.html` + `s320-open2-fetch2.html`, `wc -c` 76506 each, `sha256sum` both `d665489c…9491c789` (= `claims.json`), `diff -q` identical | **agree** | The located quote reproduces exactly after tag-stripping and whitespace normalisation (`grep -o 'If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP'`); quote is 20 words ≤ 25, located to the `O_NOFOLLOW` entry, page footer "Linux man-pages 6.19"; tier A docs scope is honest; used-by resolves (`corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`, craft block 34). |
| `O_PATH` interaction (not admitted from the same page) | reject | same fetch; tag-stripped contexts: "flag bits other than O_CLOEXEC, O_DIRECTORY, and O_NOFOLLOW are ignored"; "If path is a symbolic link and the O_NOFOLLOW flag is also specified, then the call returns a file descriptor referring to the symlink itself"; ELOOP: "O_NOFOLLOW but not O_PATH" | **agree** | The `O_PATH` sentences state a different rule (descriptor-to-the-link behaviour, flags-ignored carve-out) than the row's teaches; excluding it from S320's scope is correct curation. |
| Gate prose count "the page states the flag five times" | (observation) | tag-stripped page: `grep -o 'O_NOFOLLOW' | wc -l` → **6** | minor disagreement | The prose count is off by one (six occurrences in the tag-stripped page: flag list, description, O_PATH carve-out, O_PATH symlink note, ELOOP entry, versions list) and carries no counting command. Does not affect the row, its scope, or the admit. Routed below as R95-VD-2. |

SOURCES.md re-open: S320 is the only new row (base 224 → landing 225 by
`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` →
224 / 225); no in-place row edits (`git diff` on the file shows exactly one added line).
Census re-run by the verifier:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ exit 0, `ok`, 32 W04 duplicate-URL warnings — identical to the committed
`census-after.txt` and `census-before.txt` (W04 32 → 32 as reported).

Knowledge entry provenance trio: `source:` cites S320 with URL and anchor; `verified-at:`
2026-11-05, commit `4bda1d1d…`; `recheck:` names the curl+hash re-verification command. PASS
(CORPUS.md additional rules).

## 4. Trend verdicts (closure)

- **expansion: unchanged.** `corpus/README.md` is untouched between base and landing
  (`git diff --stat <base> <landing> -- corpus/README.md` → empty): the one new knowledge
  entry lands on the receipt/battery family already held in Core; no new coverage-map
  ground. One capability row enters the repertoire table (repertoire grows, map does not).
  Matches the lane's verdict.
- **quality: improved.** The three round-94 routed defects (M94-e, M94-f, SentinelWrite F1)
  each have a measured fix on committed receipts; the two code fixes are shown able to fail
  (`m95a-intact-denominator-red-green.txt` RED exit 1 → GREEN exit 0;
  `m95b-selftest-idempotence-red-green.txt` RED run 2 exit 1 → GREEN exit 0); craft block 34
  and QUALITY 191–192 state the class; named limits recorded rather than hidden. No admitted
  entry failed a re-check. Matches the lane's verdict.
- **discernment: improved.** The lane itself recorded `unchanged` because no outside
  spot-check existed at its write time. This verifier's outside spot-check now agrees with
  the gate on the admit (S320) **and** the reject (the `O_PATH` interaction non-admission),
  which is LEARNING.md's `improved` condition for discernment. Evidence: section 3 above.

## 5. Routed defects for round 96 (status-neutral; the lane owns these)

- **R95-VD-1 (measurement-revision gap).** C2's after-side receipts were measured
  `--worktree`, not at the landing hash as the declaration's frozen commands state. The
  landed bytes carry the block (verified), but no receipt names the landing commit. Next
  round: when a fix lands after the freeze, land the fix and then re-run the counters once
  at the landing hash (one receipt naming the landing revision), or declare the landing
  receipt in the freeze itself.
- **R95-VD-2 (count without command).** `corpus/lessons/round-95.md` `## Gate` prose says
  "the page states the flag five times"; the tag-stripped page has six `O_NOFOLLOW`
  occurrences and no counting command is given. Next round: a numeric claim carries its
  command (CORPUS.md round-1/2 rule); a one-line correction entry in the next lesson is
  sufficient (append-only).
- **R95-VD-3 (registry debt, standing).** The round-95 instruments
  (`tools/round-95/c1-forgery-refusal.py`, `stop-boundary-repair-battery-v5.py`,
  `c1-agreement-v2.py`, `symlink-probe.py`) carry selftests and verdict-shaped outputs but
  no registry rows at the lane's registry home (SKILL.md), unlike their round-89/91/93
  predecessors. Next round: add the four rows (name, kind, entry, verdict map, selftest,
  pinned values, write scope, owner).

## 6. Notes for the operator

- All four SHONEN boxes are asserted `[~]` by the lane with resolvable pointers; on this
  verifier's read every box looks checkable by a non-author (box 1: decision tables/error
  patterns/checklists with cited sources throughout SKILL.md; box 2: LOG round-95 end-to-end
  frozen-battery run; box 3: counting commands and selftests re-runnable from the report;
  box 4: ConnectorOverlap scan + PROVINCE.md untouched). Promotion is operator-owned; no
  `[x]` was written by this verifier.
- Conformance defects: none that bar admission. The two status-neutral defects above
  (R95-VD-1, R95-VD-2) are recorded for routing.
