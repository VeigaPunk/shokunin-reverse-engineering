# ScribeShonen — round 48: SHONEN section draft + stale-cell audit

Seat: `ScribeShonen` (leaf; no subagents). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch `/fast/scratch/hyaku/kaidoku-r48/ScribeShonen` (removed at exit). Anchor: the round's
declared freeze re-derived in-session as **A4 `0f06251bf6a3a6964c715f67243d4df12e854258`**
(`git log -1 --format=%H -- plans/round-48-claims.md` at 2026-10-28T18:53Z; lane tip at write
time `663f30ee751694fb0970e7de68fe88356e680822`, inherited-evidence commits), base
`61b87d742032e65fca9c38267d7d6ed7e555edad`. All work read-only on the lane; no counter
modified, no frozen byte touched, no VCS mutation anywhere.

Deliverable: `.ufo/waves/round-48/w1/ScribeShonen/shonen.md` — four lines, one per box, each
`[~]` with a pointer re-derived or verified by this seat at A4/tip, the `[x]` verifier status,
six stale cells (S1–S6) and four round-48 observations (O1–O4). **No `[x]` is awarded and none
is justified**: no named non-author verifier exists for any box as a whole (see §2).

## 1. SHONEN lines (summary of the draft)

| box | `[~]` pointer that survives a repo check at A4 | `[x]` verifier |
|---|---|---|
| SKILL.md real tables, cited sources | craft `SKILL.md:81-642`, **24** blocks, command A verbatim → `citation_resolved_rules 24` / `rule_blocks 24` / `mapped 138` (receipt `receipts/commandA-at-A4.json`); block 24's knowledge cite landed at `04469ee8` (the round-47 23/24 gap is closed); pending at landing: block 25 `<!-- verdict-meaning-table v1 -->` (0 occurrences at A4) and the registry section `:1705-1750` re-bound to `census2.json` (40 rows = 42-path census minus exactly the two round-48 tools, diff re-derived) | none; nearest non-author artefacts: `w1/C1Gold.md`, `w1/CritAxis.md` attacks on the same surface, round-46/47 spot-checks on earlier blocks |
| end-to-end task logged | `LOG.md:3174-3183` (round 42, 4 carriers, `corpus/evidence/round-42/c1/*`), `:3184-3197` (round 43, 78/78), `:3164-3173`, `:3153-3163`, `:3137-3152`; round 48 adds none by design (`plans/round-48-claims.md:16-17`) | none outside the lane; wave-2 reproductions exist only for rounds 39/40/41 |
| executable without oral context | committed-blob selftests re-run at `663f30ee`: r39 triage 35/35, r39 c2 27/27, r40 v2 45/45, **r48 `meanings.py` `"failures":0`**, **r48 `record2.py` `corr_parse true`** — all exit 0 (`receipts/*selftest*.txt`); held-out 20/20 and 26/26 stand; recipes = command A + B only | none outside the lane; `R39W2TriageMutants`, `R39W2C2Mutants`, `R40W2C2IndepEval` |
| no cross-domain bleed | `PROVINCE.md:97-125` sha256 `f1a5cfc6…78b4` identical at `52b0eb29` and `663f30ee`; appended sections `:378-384`, `:386-394`, `:396`, `:410`, `:424`; file unmodified since round 44 (`55bcce69`); rounds 45-48 add no PROVINCE line (instrument rounds) | none; `R39W2C1AxisFit` D2 (repaired) the only named non-author PROVINCE audit |

## 2. Findings

### O1 (MEDIUM, process) — the seat prompt's named freeze is three amendments dead

Prompt and `w1-spec.json` declare `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` (the A1 commit,
"after disclosed amendment A1"). The frozen file's own rule re-derives the freeze as the newest
claims-file commit: **A4 `0f06251b`** at write time (A1 axis-score cell → A2 success-token
claims-file commit: **A4 `0f06251b`** at write time (A1 axis-score cell → A2 success-token
guard → A3 census object-vs-list → A4 negated-meaning + indented row). During this seat's run
`git rev-parse HEAD` moved `ac02a79 → f3a7afc4 → 663f30ee` and `git log -1 --format=%H --
plans/round-48-claims.md` moved `ac02a79 → 0f06251b` (the f3a7afc4 window is inferable —
A3 also touched the claims file). Sibling reports
anchored at A1 (`w1/C1Gold.md`, `w1/C1Meaning/receipt.json` `--freeze dc73587…`) scored a dead
freeze; their receipts stay meaningful only as clause-level evidence. Four amendments before
any verdict is the round-47 F2 pattern recurring — disclosed each time, but the claims file
says "Nothing in this file or in `tools/round-48/` changes after the freeze" and the file
changed three times after `7fe11332`.

### O2 (MEDIUM, frozen instrument) — the committed selftest crashed at the A3 bytes; A4 repaired it

```sh
git show f3a7afc4:tools/round-48/meanings.py > scratch/round-48/meanings.py   # + round-46/gate.py
python3 -I -B scratch/round-48/meanings.py --selftest
# → AttributeError: 'list' object has no attribute 'get'  (score(): derived.get("paths"))
#   rc=1 — receipt `receipts/meanings-selftest-A3-committed.txt`, sha256 74c2aa39…
```

A3 fixed the *counter's* object-vs-list comparison but the selftest's `census_text` fixture
still returned a bare list, so the committed A3 instrument could not pass its own selftest —
an un-runnable selftest inside a frozen path for ~2 min between amendments. A4's worktree diff
(seen dirty at 18:51Z, committed `0f06251b`) makes the fixture return `{'paths': …}`, adds the
`NEGATED` polarity guard and `ROW_START`, and appends `red-opposite-polarity` /
`red-hidden-row` cases. At `0f06251b` bytes: `--selftest` rc=0, `"failures": 0`
(`receipts/meanings-selftest-HEAD.txt`). Implication for the claim instrument: the counter's
selftest is not itself a scored clause — a claim instrument shipped frozen with a crashing
selftest and nothing scored it. Whether that gap should be a clause is the judge's call.

### O3 (LOW) — a frozen path was dirty mid-wave; any run then exits 2 for a non-claim reason

`git status --porcelain` at 18:51Z: ` M tools/round-48/meanings.py` (A4 being prepared);
`w1/C1Meaning/receipt.json` captures the consequence: rc=2 `frozen_worktree_dirty`,
`dirty: ["tools/round-48/meanings.py"]`. Clean at write time
(`receipts/frozen-path-status.txt`). Receipt captured, not a claim defect.

### O4 (evidence) — both counters reproduce their control semantics at the declared freeze

`--freeze 0f06251b --rev HEAD` (in-lane receipts `receipts/c1-at-A4.json`, `c2-at-A4.json`,
stdout logs alongside):

- **C1** rc=1: `block_present 0`, `marker_occurrences 0`, `rule_blocks 24`,
  `frozen_path_changed []`, `touched 0`, battery skipped — the ctl-c1-0 do-nothing shape.
- **C2** rc=1: `failing` = round-47 seat atom missing + no re-derived `## Record corrections —
  round 48` line + 1 unbacked quoted number (`exempted 2` vs the two `c{1,2}-at-A7.json`
  receipts the section cites); `oracle.met_target true` (`atoms 44`, `mismatches []`),
  `axis_score_bad []` (the A1 fix scored `coverage 138/138→10.0`, `depth 24/24→10.0`),
  battery skipped — the ctl-c2-0 shape. Both are pre-landing reds, i.e. the instruments are
  live, not vacuous.

### S-cells (stale stated cells, audited at A4/tip)

S1 box-1 line ranges are round-41 values (`81-449`, 20 blocks); S2 "no promotion verifier"
superseded in detail by two outside spot-checks; S3 wave-2 reproduction only for rounds
39/40/41; S4 box-4 append list stops at `:394` while `:396`, `:410`, `:424` exist; S5 SHONEN
unchanged since `8de80f1d` (round 43 — five rounds of asserted drift at landing); S6 R46-V6's
`cases=16` cell still resolves against no revision (`git log -S` → 0).

## 3. Checks run (exact command, exit code, stdout sha256, UTC)

| # | command (lane root unless noted) | rc | receipt / stdout sha256 | UTC |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-48/meanings.py --root <lane> --freeze 0f06251b… --rev HEAD --json-out .ufo/waves/round-48/w1/ScribeShonen/receipts/c1-at-A4.json` | 1 | `9d956494…` (stdout log); JSON `7bdf3376…` | 18:54:27Z |
| 2 | same shape, `tools/round-48/record2.py` → `receipts/c2-at-A4.json` | 1 | `682fffd6…` (stdout log); JSON `263d46ba…` | 18:54:27Z |
| 3 | command A verbatim (`SCORECARD.md:86-143`) at `0f06251b` | 0 | `4cf13474…` → `{"rule_blocks":24,"citation_resolved_rules":24,"mapped":138,"dangling":[],"missing":[]}` | 18:53:53Z |
| 4 | committed-blob `meanings.py --selftest` at `f3a7afc4` (scratch copy + `round-46/gate.py`) | 1 | `74c2aa39…` (AttributeError) | 18:51:50Z |
| 5 | committed-blob `meanings.py --selftest` at `663f30ee` | 0 | `ae7c2506…` (`"failures": 0`) | ~18:52Z |
| 6 | committed-blob `record2.py --selftest` at `663f30ee` | 0 | `7a4edb7f…` (`corr_parse true`) | ~18:52Z |
| 7 | committed-blob r39 `sqfs-triage.py --selftest` | 0 | `6120f4ea…` (`cases=35 pass=35`) | ~18:53Z |
| 8 | committed-blob r39 `c2-counter.py --selftest` | 0 | `01419147…` (`{"cases":27,"pass":27}`) | ~18:53Z |
| 9 | committed-blob r40 `sqfs-triage-v2.py --selftest` | 0 | `67fa774b…` (`cases=45 pass=45`) | ~18:53Z |
| 10 | `git show 663f30ee:PROVINCE.md \| sed -n '97,125p' \| sha256sum` vs same at `52b0eb29` | 0 | `f1a5cfc6…78b4` both | ~18:51Z |
| 11 | registry-vs-census2 set diff (python3, `git show` blobs) | 0 | stdout only: `rows 40 census 42; in census not registered: ['tools/round-48/meanings.py','tools/round-48/record2.py']; registered not in census: []` | ~18:52Z |
| 12 | `git status --porcelain` over frozen paths (three samples) | 0 | `f76075ea…` (dirty-window capture) | 18:51-18:55Z |
| 13 | `git log -1 --format=%H -- plans/round-48-claims.md` and `git rev-parse HEAD` (repeated) | 0 | claims-file newest commit `ac02a79 → 0f06251b` (observed); tip `ac02a79 → f3a7afc4 → 663f30ee` | 18:46-18:55Z |
| 14 | `bash scripts/hyaku/disk-guard.sh status` | 0 | `/fast/scratch/hyaku 33%` | 18:50:25Z |

Verified-not-executed (read in place): `.ufo/waves/round-48/controls/*` inventory (7 files,
incl. `ctl-c1-a3-simulation.json`), `w1/C1Gold.md`, `w1/C1Meaning/receipt.json`,
`w1/MutC1Rows/probe.json`, `corpus/lessons/round-47-verifier-spotcheck.md` §Spot-check,
`SCORECARD.md:86-143`, `LOG.md:3137-3434`, `PROVINCE.md:378-438`, SHONEN history
(`8de80f1d` last change, `git log -S 'cases=16'` → 0).

## 4. Not run / out of scope

- No SHONEN.md, SKILL.md, SCORECARD.md, LOG.md, PROVINCE.md, plans/, tools/, corpus/ edit; no
  commit/stage/stash/checkout or any VCS mutation; no counter "repair" — the A3→A4 fixes were
  observed, not authored, by this seat.
- No forgery construction against the counters (other seats own the battery attacks); no
  fixture repo created.
- The two counters were run as black boxes once each at the declared freeze; exit 2 paths
  (`--json-out` outside lane root, `frozen_worktree_dirty`) observed and reported, never
  counted as pass.
- Installs: **none** (no `uv`, `npx`, pacman, or `~/.local/bin` write); pacman is paused
  host-wide per the contract.

## 5. Touched surfaces

Written, all inside the seat dir: `.ufo/waves/round-48/w1/ScribeShonen.md`,
`.ufo/waves/round-48/w1/ScribeShonen/shonen.md`,
`.ufo/waves/round-48/w1/ScribeShonen/receipts/` (`c1-at-A4.json`, `c2-at-A4.json`,
`c1-at-A4.stdout`, `c2-at-A4.stdout`, `commandA-at-A4.json`, `frozen-path-status.txt`,
`meanings-selftest-A3-committed.txt`, `meanings-selftest-HEAD.txt`,
`record2-selftest-HEAD.txt`, `selftest-{sqfs-triage-r39,c2-counter-r39,sqfs-triage-v2-r40}.txt`).
Scratch `/fast/scratch/hyaku/kaidoku-r48/ScribeShonen` removed before yield. Nothing else in
the lane or the fleet repo was written.

**Report: `.ufo/waves/round-48/w1/ScribeShonen.md`**
