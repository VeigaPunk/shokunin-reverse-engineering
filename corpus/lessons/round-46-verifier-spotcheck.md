author: hyaku closure (non-author integrator, @m_zfl)

# Round 46 — non-author verifier spot-check

Lane `kaidoku`, round 46. Lane tip before the round `5382acc85f9d8617fe242fc116819b8055dfc4c7`,
after `c0112995817b4d8caddd86705b08e89bdac99640`. Report `.ufo/reports/round-46/kaidoku.md`
(fleet repo commit `3184c5e9`, author date 14:03:24, committer date 14:12:20 -0300). I authored
nothing in this round: I re-measured committed bytes, re-opened the sources, and verified the
lane's committed gate evidence. **No lane gate was executed** (Gate standard, closure
consequence); every counter value below is either my own plain measurement over committed bytes
(`git show <rev>:<path>` piped to grep/awk/python3) or a value read from the committed receipt
named beside it.

## 1. Step-1 conformance

| item | result |
|---|---|
| report committed in the fleet repo by the lane identity | yes — `git log --format='%an <%ae> %H' -- .ufo/reports/round-46/kaidoku.md` → `kaidoku-shokunin <kaidoku@shokunin.local> 3184c5e9…` |
| `SHONEN` heading, one line per box | yes — four lines, all `[~]` (author assertions); no non-author `[x]` is written, promotion stays operator-owned |
| every cited lane commit exists and is an ancestor of the branch | yes — 22 hashes checked (`c0112995`, `332f4884`, `3182047`, `50862e4a`, `65678df0`, `04252247`, `227d6982`, `87578656`, `6e018068`, `7bf33e31`, `781e19ae`, `47b5e265`, `58eb04b6`, `1e32827b`, `49e6cac4`, `21b55a8f`, `c0ca5392`, `17a72375`, `eb8215ac`, `f762b727`, `f59565b7`, `deee6595`); each `git merge-base --is-ancestor <h> main` returned 0 |
| lane repo pushed | yes — `scripts/hyaku/jj-lane.sh state …/kaidoku-shokunin` → `branch=main local=c0112995 remote=c0112995 ahead=0 behind=0` |
| lane repo carries no uncommitted round work | **no** — `git -C kaidoku-shokunin status --porcelain` → 72 entries: 136 untracked files (`git ls-files --others --exclude-standard`) and 5 modified tracked (` M`) files, all under `.ufo/waves/` (130 untracked under `round-46`, 6 under `round-45`). Seats were still writing after the driver's `complete` line: the newest seat report `R46W1MutGate/report.md` landed 14:31:50, 17 minutes after it (defect V5) |
| dispatched prompt carries the template contract | yes — `.ufo/prompts/kaidoku-round-46.md` (committed 13:35:15): §1 mission/axes binding, §3 L2 floor ≥8 in one batched swarm with the role split matching `MISSION.md` §L2 concurrency, §5 commit-then-push, push scope, L0 side channel; report path, report-lands-last, `SHONEN` heading, commit-hash citation and write scope all present |
| marker vs report | real report — work performed, evidence pointers, changes tied to `LOG.md` and resolvable commits; **status `ok`**, defects below are status-neutral |

Defects named, not barring: uncommitted wave evidence; the report's own stale counts (V3–V6).

## 2. Claims — re-derived, not re-trusted

### R46-C1 / depth — `SKILL.md` craft rule block 23 and its discriminating counter

Commands run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (committed bytes only):

```sh
git show 50862e4a:SKILL.md | awk '/^## Queue-drain craft /{f=1;next} f&&/^## /{exit} f&&/^- \*\*/{c++} END{print c}'   # 22
git show c0112995:SKILL.md | awk '/^## Queue-drain craft /{f=1;next} f&&/^## /{exit} f&&/^- \*\*/{c++} END{print c}'   # 23
git show c0112995:SKILL.md | grep -o 'freeze-integrity-table v2' | wc -l                                              # 1
git show c0112995:SKILL.md | sed -n '/^- \*\*23\. /,/^## Config custody/p' | grep -cE '^\| R45-CL'                     # 13
git show c0112995:SKILL.md | sed -n '/^- \*\*23\. /,/^## Config custody/p' | grep -oE '(corpus|plans|tools)/[A-Za-z0-9._/-]+(:[0-9]+(-[0-9]+)?)?' | wc -l   # 9
git show c0112995:tools/round-46/attest.py | sha256sum                                                                # c405613170f0581661b9e2afb4bf278da8ac1f936eeb00eb4b456a9e70ad8e5c
```

| value | reported | observed by me | match |
|---|---|---|---|
| rule blocks, pre-landing (`50862e4a`) | 22 ("at the freeze") | 22 | number yes, **label no** (V3) |
| rule blocks at tip | 23 | 23 | yes |
| block-23 marker occurrences | 1 | 1 | yes |
| block-23 table data rows | 13 | 13 (one header + separator + 13; every row 4 cells; exit cells `{0,1,2}`) | yes |
| refs | 9 | 9 tokens over 5 distinct paths | yes (but 8 carry a line selector, the 9th is the pin — V8) |
| citations resolve | `unresolved []` | all 9 present at `c0112995`; `round-45.md:142-176/90-101/197-217/212-231` (247 lines), `round-46.md:18-19/27-31` (102), `round-46-claims.md:37-166` (216), `r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` (79) — every range in bounds | yes |
| sha256 pin | matches bytes at rev | `c4056131…ad8e5c` == the pin in block 23, at `332f4884`, `58eb04b6` and `c0112995` | yes |

Gate evidence verified (not executed): `.ufo/waves/round-46/l1/scores/c1-at-A4.json` →
`freeze 332f4884…`, `rev 58eb04b6…`, `met_target true`, `failing []`, `rule_blocks 23`,
`rows 13`, `refs 9`, `frozen_path_changed []`, battery `forgeries_total 9 / v1_green 9 /
v2_green 0 / genuine_green 1`. Self-test tally from the committed banner
`.ufo/waves/round-46/w1/R46W1CritDenominator/selftest-attest-A4.txt` → `cases=18 failures=0`
(the code registers 18 `case(` invocations at `332f4884` and later). Freeze window
`332f4884..c0112995` over `tools/round-46 plans/round-46-claims.md` → **0 lines**, so the
frozen bytes were untouched through the measured revision and the tip.

**Verdict: `improved`.** The before state is genuine (block absent, 22 blocks at `50862e4a`)
and the depth proxy it moves is re-derivable (23 craft blocks, 23/23 with resolvable
citations, 138 knowledge files at both ends). The claim is met; the before-cell label is a
record defect (V3).

### R46-C2 / calibration — the marker-bound instrument registry over the 38-instrument census

```sh
git show c0112995:SKILL.md | sed -n '/<!-- instrument-registry v2 -->/,/<!-- \/instrument-registry -->/p' | grep -cE '^\| *`'   # 38
python3 -c "…registry parse…"   # 38 rows, every row 7 cells, every verdict cell has 0= 1= 2=, 0 empty cells
python3 -c "…census compare…"   # registry cell-0 set == tools/round-46/census.json paths (38, order-identical)
while read -r p; do git cat-file -e "58eb04b6:$p"; done      # 0 failures; same at c0112995
git ls-tree -r --name-only c0112995 corpus/knowledge | grep -c '\.md$'   # 138 (138 at 5382acc8 too)
```

| value | reported | observed by me | match |
|---|---|---|---|
| registry rows | 38 | 38 | yes |
| census scope | 38 | `len(census["paths"]) == 38`, `named_but_absent []` | yes |
| registered / unregistered | 38 of 38 / `[]` | set-equal with the census, 0 missing | yes |
| `thin []` | `[]` | 0 rows whose verdict cell lacks any of `0=`,`1=`,`2=`; 0 empty cells anywhere in the 38 rows | yes |
| `absent_at_rev []` | `[]` | all 38 exist at `58eb04b6` and at `c0112995` | yes |
| knowledge files (coverage no-harm) | 138, mapped 138 | 138 `.md` at `5382acc8` and at `c0112995` | yes |

Before: `.ufo/waves/round-46/controls/ctl-c2-1-v1-scope.json` → round-45 counter,
`scope_size 6`, `registry_rows 45`, `registered` 6. Gate evidence:
`.ufo/waves/round-46/l1/scores/c2-at-A4.json` → `freeze 332f4884`, `rev 58eb04b6`,
`met_target true`, `failing []`, `thin []`, `absent_at_rev []`, battery
`forgeries_total 7 / v1_green 7 / v2_green 0 / genuine_green 1`; registry self-test banner
`selftest-registry-F4.txt` → `cases=12 failures=0` (12 at every revision).

**Verdict: `improved`** for the measured move (6 → 38 registered, presence proven at the
revision). The limit the lane states is real and sharper than it says: the clause binds the
digits, not their meanings (R46-CL7, HIGH, open), and a false `purpose` cell passes (R46-CL5).

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | `unchanged` | 138 knowledge files at both ends; no coverage-map row changed; `corpus/README.md` and `PROVINCE.md` byte-unchanged (`git diff 5382acc8 c0112995 --stat` lists neither) |
| depth | `improved` | block 23: 13 routed rows, 8 line-selected citations + 1 sha256-pinned interpreter, all resolving; 23 craft blocks with 23/23 resolving citations |
| calibration | `improved` | registry 6 → 38 over the census with exact cell-0 equality, bound verdict maps and presence at the revision; 0 of 7 forgery classes accepted (committed receipt) — record defects V1/V2/V4 are routed, not absorbed |

No axis is harmed: the round's diff over the whole lane is `784 files changed, 75040
insertions(+)` and **zero deletions** (`git diff 5382acc8 c0112995 --numstat | awk '$2>0'`
prints nothing), so nothing pre-existing was weakened, and the `## Owned axes` table is
untouched.

## 4. Discernment spot-check (`corpus/lessons/round-46.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S142 `git-log` documentation | admit (`docs`, tier A, `mined`, used-by `corpus/lessons/round-46.md`) | `https://git-scm.com/docs/git-log` fetched 2026-10-28, HTTP 200, 375,834 bytes, sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a` — **identical to the recorded digest**; the sentence sits inside the `--diff-merges=<format>` definition list under the `first-parent` value | **agree** | the quote is verbatim and 19 words: "Show full diff with respect to first parent. This is the same format as --patch produces for non-merge commits."; the row's `teaches` matches what the page says; tier A is right for upstream docs of the flag the arm uses |
| S105 System V ABI draft | reject (standing registry reject; this round's Gate records **no reject**) | `https://www.sco.com/developers/gabi/latest/contents.html` fetched 2026-10-28, 2,717 bytes, sha256 `860a69166779d1c2264867df76c750e21af9f9f185fd451659be64e794da18b0` — identical to the recorded anchor — and the page is the Object Files index with no `verneed`/`vernaux`/`gnu.version_r` token | **agree** | the recorded reason ("four opened files lack GNU version-needs definitions") holds for the anchored file; the flip condition (a chapter that defines Verneed/Vernaux) is correctly stated and has not been met |
| S142 row shape | new row this round | same page as above | **agree** | ≤25-word quote (19), located anchor, `opened 2026-10-28`, `recheck on-release`, `used-by` path exists; the only census warning is `W04 duplicate url` against S074's git-log URL — a different scope, legitimate, though the report's claim that "the Gate explains" it is not true: the lesson's Gate does not mention it (defect, minor) |

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ `kaidoku ok`, exit 0, 15 `W04` warnings (14 inherited + S142), matching the report.

The round has no reject decision of its own, so the reject arm of this check was exercised on
the registry's standing reject. That gap is routed (V9).

## 5. Trend verdicts

- **expansion — `unchanged`.** `corpus/knowledge/*.md` 138 → 138 (`git ls-tree -r --name-only
  <rev> corpus/knowledge | grep -c '\.md$'`); no knowledge entry added, no coverage-map row
  changed, `corpus/README.md` `## Frontier` byte-unchanged; SOURCES 141 → 142 is instrument
  documentation (S142), not domain ground.
- **quality — `improved`.** The measure now rejects its own mutated copies: 9 C1 and 7 C2
  forgery classes scored red by v2 and green by the ported v1 clause set, genuine artefact
  green (committed receipts `c1-at-A4.json`, `c2-at-A4.json`); block 22's false R45-CL19 exit
  cell corrected at `58eb04b6`; two HIGH instrument bypasses closed at `332f4884` with one
  self-test case each; `corpus/QUALITY.md` row 77 added from M46-4. Bound, as the lane states:
  this is instrument quality, not new reverse-engineering ground. It does not extend to the
  round's own record, which carries the falsified claims V1/V2.
- **discernment — `improved`.** The outside check agrees on the admit and on the standing
  reject above; the round found four of its own defects before the operator (M46-1 a control
  naming a measurement that cannot exist at the freeze, M46-2 an unpinned denominator, M46-3
  the freeze series, M46-4 the depth-proxy recurrence) and grounded two `QUALITY.md` rows from
  them. Caveats recorded: the Gate carried no reject, and the round did not catch its own
  2× seat overstatement (V1) — both routed.

## 6. Routed defects (lane must fix in round 47)

- **R46-V1 (HIGH, record).** `LOG.md` round-46 entry states "wave 1 = 40 seats … wave 2 = 40
  seats … Round total 80, inside the 64–128 band; per-seat output in
  `.ufo/waves/round-46/{w1,w2}-results.json`", and `SCORECARD.md` repeats "Waves: 40 + 40 = 80
  seats." Observed: one dispatched wave of 40 (`w1-dispatch.json` `counts.spawn 40`), no `w2/`
  tree beyond `w2/swarm-registry.json`, no `*.ready` for wave 2, **zero** `*-results.json`
  (`git ls-tree -r --name-only c0112995 .ufo/waves/round-46 | grep -c results.json` → 0). The
  report is the honest record (40 seats, below the band). Append a LOG correction naming the
  superseded text and amend the SCORECARD claim, append-only.
- **R46-V2 (HIGH, record).** `SCORECARD.md` says "`git log --name-status 0425224..<tip> --
  tools/round-46 plans/round-46-claims.md` is empty at every measurement above". It is not:
  `332f4884` modifies `tools/round-46/attest.py` and `tools/round-46/gate.py`. The empty window
  is `332f4884..58eb04b6` (0 lines), which is the one the claims rest on. State that window.
- **R46-V3 (MEDIUM, evidence).** The report's before cell ("at the freeze: exit 1,
  `marker_occurrences 0`, `block_present 0`, `rule_blocks 22`") is true of `50862e4a` — the
  receipt's own `freeze`/`rev` — not of the declared freeze `332f4884`, where block 23 already
  exists (`rule_blocks 23`, marker 1). `c1-at-F4.json` at `0425224` also reads `rule_blocks 23`.
  Name the revision the before numbers were measured at.
- **R46-V4 (MEDIUM, record).** The report's wave settlement ("32 of 40 produced a report"; the
  eight named as producing nothing; "8 of 32 (25 %) attack seats") is false at its own cited
  `c0112995`: 33 top-level seat reports (34 counting nested), and
  `R46W1CritBattery.md` was added **in** `c0112995`, while `CritBattery/report.md` (355 lines)
  and `MutC1Checks/report.md` (423 lines) exist at the parent `22fd0d6b` too, so those two
  "produced nothing" under no reading. The report's figures reproduce `22fd0d6b` by top-level
  counting only. At the cited tip the dead set is 7 top-level (CritC1, CritDenominator,
  MutC1Checks, MutGate, SentTools, SimplInstruments, ProbeCost), 34 of 40 seats have a report
  somewhere, and settled attack seats are 10 of 34 (5 reviewer, 2 critic, 2 mutation-tester,
  1 revenger). At closure the worktree has moved further: 39 of 40 seats have a report
  (`R46W1ProbeCost` is the only one with none) and all 13 attack seats are settled. Re-derive
  and append the correction.
- **R46-V5 (MEDIUM, hygiene).** The lane repo is dirty at closure and still growing: 136
  untracked files (130 under `round-46`, 6 under `round-45`) and 5 modified tracked files,
  all under `.ufo/waves/`. The wave kept writing after the driver's `complete kaidoku round=46`
  line (14:15:00): `R46W1MutGate/report.md` landed 14:31:50. The report's "Eight untracked
  files remain" cannot be reconciled with any count I can take. Land the evidence deliberately
  under a named commit or remove it; never sweep-commit.
- **R46-V6 (LOW, freshness).** Stale self-test counts: `SHONEN` box 3 and the `SKILL.md`
  instrument-registry row for `tools/round-46/attest.py` say `cases=16`; the code and the
  committed A4 banner say `cases=18` (registry 12). The claims file's 15/11 is frozen and
  already routed as R46-CL8; sweep the other two mentions.
- **R46-V7 (LOW, evidence).** Four receipt paths cited in the round's record do not exist at
  the tip: `controls/ctl-c1-1-v1-profile.json` (claims, lesson M46-1 — allows the claim but is
  absent), `controls/ctl-c2-1-v1-profile.json`, `controls/ctl-c2-2-ghost-tool.json` (claims),
  `l1/scores/c1-v1-gap.json` (lesson M46-1's own fix column). The nearest real evidence is the
  battery block inside `c1-at-F4.json` / `c2-at-F4.json`. Name the real receipt or land the
  file; `controls/ctl-c2-0-do-nothing.json` exists and is cited by nothing.
- **R46-V8 (LOW, wording).** "9 line-selected citations": 8 carry a line selector, the 9th is
  the sha256-pinned interpreter (the claims' own clause 5 exempts it). Say "8 line-selected +
  1 pinned interpreter" wherever the number is described in prose.
- **R46-V9 (LOW, discernment coverage).** The round's `## Gate` records no rejected candidate,
  so the non-author check could only test the reject arm on a standing registry row. Record at
  least one rejected candidate with its reason and flip, or state that there was none and why.
- **R46-V10 (LOW, evidence label).** "Eight untracked files remain under `.ufo/waves/
  round-46/w1/`" — no committed artefact can attest an untracked set, and the tree now holds
  130 untracked files under `round-46` alone. State the set by count and name at the cited tip,
  or drop the figure.

Also noted, not routed as work: the report's author date (14:03:24) precedes the lane tip it
cites (`c0112995`, committed 14:11:20); the report's committer date (14:12:20) is after it, so
"lands last" holds but the label "lane tip at filing" is imprecise.
