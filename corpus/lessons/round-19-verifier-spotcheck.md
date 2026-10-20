author: hyaku closure (non-author integrator, @m_opus)

# kaidoku round 19 — non-author verifier spot-check

Closure date 2026-10-20. Lane B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`, verification source
S = `b26a6c42207a859e70bd892c7e89a5befedf379b`, retained verification E =
`2a6229f2fb415ba8efecbc2ae24e69ec89b64986`, tip A = `321da6300d5e3cefdb7bca4fa3114714ec166fd4`.
Report: fleet `.ufo/reports/round-19/kaidoku.md` (fleet commit `3a4d1aa`). Driver digest (copied
from mutable `.ufo/watchdog.log`):

```text
2026-10-20T15:28:58-03:00 launch kaidoku round=19 pgid=2705676 driver=hyaku-inline attempt=1
2026-10-20T17:13:18-03:00 complete kaidoku round=19; hyaku-inline attempt=1
```

Method: the closure ran plain measurements over committed bytes (`git show`/`ls-tree`/`grep`/`jq`/
`sha256sum`) plus five read-only reviewer seats (C1, C2, C3, wave accounting, no-harm/mcp.json). No
lane gate, counter or `measure.py` was executed by the closure; gate-backed numbers are
**evidence-verified** (committed stdout/exits re-read), all others **re-measured**.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-19/kaidoku.md` | `kaidoku-shokunin 3a4d1aa6489c…` | ok |
| SHONEN heading, one line per box | report `## SHONEN` vs `grep -c '^- \[' SHONEN.md` | 4 lines / 4 boxes, all `[~]` | ok |
| Cited commits exist and are ancestors of `refs/heads/main` | `git cat-file -e` + `git merge-base --is-ancestor <h> refs/heads/main` for B, 85589ac, a1140e7, 4f6c73f, 5e364bd, d0690fd, 279e8b1, b26a6c4, 2a6229f, 321da63 | all 10 `ok` | ok |
| Pushed | `jj-lane.sh state …` | `local=remote=321da630… ahead=0 behind=0 tracked=0 untracked=2` | ok |
| Leftovers | `git status --porcelain` | `?? .ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-fixture/`, `?? …/repo-sub-fixture/` | **defect (status-neutral)**, see D1 |
| Prompt carries template contract | `.ufo/prompts/kaidoku-round-19.md` headings | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN), §5 commit/push/L0, §6 hyaku addendum | ok |
| Not a marker | report cites 8 shipping commits, 769 changed paths B..A | real report | ok |

The two untracked paths are nested Git repositories (`repo-fixture/.git`, `repo-sub-fixture/.git`)
written by the custody-pair selftest at 16:46:23 -03 during verification; the other 85 files of that
scratch directory are committed at E. They are selftest residue, not uncommitted claim work.

## Per-claim re-check

### C1 calibration (owned) — improved

- Evidence-verified: `git show E:.ufo/waves/round-19/verify/routed-r18-baseline-strict.stdout` →
  `open_count 7, named_open 7, substance_open 7, rev 8a8da7e…`; `…-source-strict.stdout` → all seven
  `named:true, substance:true`, 0/0/0, rev `b26a6c4…`. `verification.json`: baseline exit 1, source exit 0.
- Re-measured per route at B vs S: MIDMAP-LISTSTEP (B `receipt-validate.py` list branch accepts pin
  checks on any step; S requires the `analyze` step); VALIDATOR-DIGEST (B format-only 64-hex; S
  recomputes `sha256(git show VALIDATOR_REV:receipt-validate.py)`; `git show 9011581d8452:… | sha256sum`
  → `618448829ba6…239126f`, 8 remapped copies 0 mismatches); STRICT-BASELINE (`9011581` exit 1 open 6,
  `454dee6` exit 0, round-19 tree absent at B); HEAD-ALIASES (B guards only literal `--rev HEAD`; S
  exit 2 for `@`, `HEAD~N`, `HEAD^{commit}`, reflog/pseudo-refs); DEADSEAT-RECORD
  (`evidence/r18-dead-seats.json` names 4 seats with causes; absent at B); REGISTRY-PINNED (SKILL
  542/545 rewritten with no-baseline statement and source path); INSTALL-RECORD (B round-18 lesson has
  0 `## Installs`; round-19 lesson records go1.24.6/go1.25.0 full SHA-256s, sizes, paths, channel).
- QUALITY: `git diff B A -- corpus/QUALITY.md` → one appended row `| 22 |`, 0 removed lines; rows 1–21
  byte-identical (21→22).
- Postfix mutants: `git show A:…/verify/postfix-mutations.stdout` → `"killed": 10`, `"survived": []`,
  scope "trusted lane code; mkdtemp clone is not an OS security sandbox".

### C2 freshness (fleet axis, no owned proxy) — improved

- Evidence-verified: `E:verify/province-pins-baseline-strict.stdout` → mismatch_count 2 (Devin and OMP
  stated 6.5.0 at PROVINCE 9/16/17/44 vs live 6.7.0), stated 9, unstated []; source-strict →
  mismatch 0, stated 9, unstated []; exits 1→0 in `verification.json`.
- Re-measured: `git show B:PROVINCE.md` states 6.5.0 for Devin/OMP; A states 6.7.0; live
  `~/.config/devin/mcp_config.json`, `~/.omp/agent/mcp.json`, `~/.kimi-code/config.toml` (read-only)
  all pin `rea-agents@6.7.0`, sha256/mtimes byte-match the digests recorded in the retained runs.
- Census: `git show E:…/evidence/c1-census-v10-before.txt | grep VERDICT` →
  `FAIL (stale=4 ambiguous=0 undeclared=2 unresolved=0)`; `git show A:…/verify/c1-census-v10.stdout`
  → `FAIL (stale=0 ambiguous=0 undeclared=2 unresolved=0)`.
- **Undeclared blocks ruling: pre-existing, not harm.** Both runs flag SCORECARD.md 2380-2382 and
  SKILL.md 511-519; `git log -L` at B attributes them to round-17 commits `8e7642c`, `d0ab299`,
  `da64646` (ancestors of B), and the flagged lines are byte-identical B→A. Round 19 neither added nor
  touched them; the census FAIL/1 is the carried state, honestly reported.
- Residual: the final census ran at E; A appends SCORECARD 2504-2567, which contains no `X.Y.Z` token
  (`grep` exit 1) — [INFERENCE] no new pin locus, but no post-A census run is committed.

### C3 depth (owned) — improved

- Evidence-verified: `verify/measure-baseline.stdout` `c3_bound_validated: 0`; `measure-source.stdout`
  `bound_validated: 8, run_tree: pass2, compare_jsons: 8, matched: 7`; 8/8
  `verify/receipt-validate-t1250-*.stdout` exit 0.
- Re-measured: `git ls-tree -r --name-only A -- .ufo/waves/round-19/runs/ | grep -c compare.json$` → 16
  (pass1 + pass2), `runs/pass2/` → 8; labels t1250-{go,gofmt,asm,cgo,compile,cover,preprofile,vet};
  `git grep -l 13902080 A -- '.ufo/waves/round-19/runs/*ghidra.log'` → only
  `runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log` and `runs/pass2/t1250-vet/logs/rea-ghidra-PEkTou/ghidra.log`;
  `Go analysis failure` present only in the vet logs, both passes; `jq .all_match` → 7 true / 1 false per
  pass; both `run-log.txt` end `aggregate exit=1`; round-19 tree has 0 entries at B.
- Freeze ordering: a1140e7 (15:57:44 -03) contains `predictions/` + `decision-rule.json`; first run
  start 15:57:51; `git diff a1140e7 A -- .ufo/waves/round-19/predictions` → empty; run outputs added only
  in 4f6c73f and b26a6c4, both descendants of a1140e7.
- Disclosures present in `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`: compile's deferred
  RTTI propagation NPE (`ghidra.log:347`, both passes), the unmasked variadic-bit emulator walk bug, and
  "never call this 8/8 exact prediction success". No overclaim found.

### Disclosed process items — judged

- **Carrier-version execution breach** (lesson Mistakes row 5; `w1/InstallRecordDraft.md:26`): a real
  violation of the wave's no-carrier-execution contract. `grep -rn 'go version go1'` over `runs/`,
  `evidence/receipt-validation`, `verification.json` → 0 matches; the output feeds only the install
  record. Ruling: disclosed, **does not taint C3**; status-neutral process defect (D3).
- **Timestamp correction**: `claims.json:36` amendment dated 16:20:00-03 shipped in 4f6c73f committed
  16:09:17; withdrawn at `claims.json:45`. Future-dated evidence is a §Evidence-standard conformance
  defect (D2), but `git diff a1140e7 A -- predictions/decision-rule.json` is empty and the amendment
  restates the frozen rule, so the operative C3 rule did not change after outcomes. Status-neutral.

### Verification claim tallies (evidence-verified)

`git show A:.ufo/waves/round-19/verification.json | jq` → 62 commands, 0 with exit ≠ expected_exit,
`unexpected_exits []`, 26 checks all `true`, `failed_checks []`, `tool_integrity_mismatches []`,
`source_revision b26a6c4…`. Matches the report (62/62, 26/26).

### Wave seats — no claim rests on a missing seat

Re-counted from committed `evidence/wave-outcomes/w1-terminal.json`, `wave1-outcomes.json`,
registrations and `ls-tree w1/ w2/`: W1 90 seats, 48 reports (28 stop + 17 aborted + 3 error), 42
reportless (33 aborted + 9 error), raw terminal 50/12/28, 20 report-present non-clean; W2 72/72/72 stop;
role tables match; no duplicate names, W1∩W2 = 0, job-cap refusals spawned none (attempt 3 spawned 72).
Of 39 cited seats, three cited only by the lesson are reportless (CitationDriftAliases,
HeadRevLintNested, ValidatorDigestGuard) — each explicitly disclosed as a dead seat whose substance
rests on committed `w1/inherited/*.patch` plus L1 verification; FallbackReaders (aborted, report present,
cited for C2) is corroborated by `evidence/doctor/` and clean seats LiveConfigPins/GhidraJdkRecheck;
MidmapListStep (aborted) and R12Disclosure (error) rest on committed patches. SCORECARD 2473-2567 and
LOG 2219-2287 cite no seat names. Ruling: **true** — no claim rests on a missing seat.

### mcp.json writer — no evidence of lane write

`stat ~/.omp/agent/mcp.json` → mtime/birth 2026-10-20 13:35:56.12 -03, ~1h53m before the 15:28:58
dispatch, sha256 `266078529e…` byte-identical to the w1 `LiveConfigPins` record. `git diff --name-only
B A` (769 paths) contains no client-config path; `git log -p B..A` and `git grep` over
`.ufo/waves/round-19` and `.ufo/gates` show only reads (grep/sha256/stat/doctor); province-pins writes
only temp-dir selftest fixtures via env overrides. B's `corpus/lessons/round-18.md:89` already recorded
the rewrite as outside the lane. Ruling: no evidence of a round-19 lane write. The writer remains
unidentified and operator-owned.

## No-harm and per-axis verdicts

`git diff B A -- SCORECARD.md` is append-only (B is a byte prefix of A for SCORECARD 174530→182993
bytes and LOG 146631→151282); r12/r18 knowledge entries prefix-preserving; `git diff --stat B A --
corpus/lessons/` adds only `round-19.md`; r17/r18 `runs`/`predictions` unchanged; SOURCES edits are
used-by-cell appends on six rows plus S037-S039; SKILL/PROVINCE deletions reappear updated;
`verify/controls-r19.stdout` → map 96/96→97/97, missing/dangling [], depth 17→17, scores 10.0, 13 checks
true. Four r17/r18 tool files changed in place (receipt-validate.py, jj-red-before.py, revpin.py,
routed-defects.py) — these are the routed R18 fixes; history keeps old bytes; not harm.

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | re-measured per route + evidence-verified strict counter 7/7/7→0/0/0, exit 1→0 |
| freshness | improved | evidence-verified pins 2→0 + re-read PROVINCE/live configs; census stale 4→0, undeclared 2 pre-existing |
| depth | improved | re-measured 0→8 bound labels, H1-only 13902080 both passes, 7/8 compare, freeze intact |

No owned axis harmed.

## Discernment spot-check (lesson round-19 `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| SOURCES S037 (rea-agents 6.7.0 registry identity) | admit (mined) | `curl https://registry.npmjs.org/rea-agents/6.7.0 \| jq .dist.integrity`; packument `.time["6.7.0"]` | agree | integrity `sha512-yhIx2ioJ…OhFw==` and time `2026-10-18T08:12:05.640Z` match the lesson quotes exactly; `dist-tags.latest` 6.7.0 |
| SOURCES S038 (go1.25.0 linux-amd64 archive) | admit (mined) | `curl 'https://go.dev/dl/?mode=json&include=all' \| jq` go1.25.0 entry | agree | sha256 `2852af0c…b613`, size 59659213, filename match the row and quotes |
| SOURCES S039 (r12 Evidence-ID experiment) | admit (mined) | `git show 8a8da7e:.ufo/waves/arc3-loop1-round12/integration/c1/reconcile-all-go-ids.txt` line 28 | agree | line 28 reads `records=27 matched=27 bundles=CR-1,CR-4,EX-2,EX-4,EX-5,EX-6,EX-8`, as quoted |
| rea-agents 6.6.0 as a source | reject (no row) | `curl -o /dev/null -w %{http_code} https://registry.npmjs.org/rea-agents/6.6.0`; packument `.versions` | agree | HTTP 404; packument has no 6.6.0 |
| "c1-census PASS" as first declared | reject as declared | `git log -L 2380,2382:SCORECARD.md B`, `-L 511,519:SKILL.md B`; census VERDICT lines | agree | the two undeclared blocks are round-17 text outside the gate's scope table; final census is still FAIL/1 |

Newly written SOURCES row re-opened: S037/S038/S039 quotes are each a single contiguous token
(≤25 words) and match the live/committed source byte-for-byte.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ `kaidoku W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes`,
`kaidoku ok …/corpus/SOURCES.md`, exit 0 (the W04 is the pre-existing S032/S033 supersession warning).

## Trend verdicts

- **expansion: unchanged** — one knowledge entry on held Go ground; no new domain surface or capability
  (`controls-r19.stdout` capability/saturation unchanged).
- **quality: improved** — stale client-pin statements corrected against re-read live configs; r12/r18
  corrections are prefix-preserving addenda; C3 limits (7/8, NPE, walk bug) retained without overclaim.
- **discernment: improved** — all five sampled admit/reject decisions agree on outside re-opening; the
  outside-routed R18 dead-seat defect became grounded QUALITY #22 with red/green records.

## Routed defects (lane fixes next round)

- D1: untracked nested-repo selftest residue `.ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/{repo-fixture,repo-sub-fixture}/`
  left in the working tree; selftests must write nested repos outside the lane tree or clean them up.
- D2: future-dated evidence timestamp (`claims.json:36`, 16:20 in a 16:09:17 commit) — withdrawn, but
  timestamps must be at or before their shipping commit.
- D3: carrier execution by InstallRecordDraft despite the prohibition; there is still no enforcement
  that prevents or detects carrier execution.
- D4: census FAIL/1 on the two pre-existing round-17 undeclared blocks (SCORECARD 2380-2382, SKILL
  511-519) needs the scope re-key the lane itself identified.
- D5: no census run covers A's post-E SCORECARD append; run the final census at the delivered tip.
- D6: the report's open residuals (nested compare-only lint, trusted-revision import trust, citation
  slug escape, argv decoy token, wave-outcomes `causes` key collision, jj selftest gaps) stay open.

SHONEN: all four boxes remain `[~]`; none is yet fully checkable by a non-author without an outside
execution of the written instructions and a full-province review. Promotion stays operator-owned.
