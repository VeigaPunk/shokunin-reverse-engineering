# Round 96 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Round: kaidoku r96, attempt 1. Base `0ea695e826f2dca53dd55ac0bafead93de26b173`, lane HEAD
`26a7aa205f9e4a180ddbe2e8492789d61ab286de`, measured landing `f63ce41506a26d57275f1088235bcf672978a34b`.
Report: `.ufo/reports/round-96/kaidoku.md`. This file is written by the closure judge, not by the lane.

## 1. Step-1 conformance

- Report committed in the fleet repo by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-96/kaidoku.md` → `kaidoku-shokunin <kaidoku@shokunin.local> c5ebb7209f32a4442d7dbe1f494c1e7d0de5f217`; commit dated 2026-11-05 15:28:30 -0300, inside the watchdog window (launch `2026-11-05T14:14:06-03:00`, complete `2026-11-05T15:34:03-03:00`).
- `## SHONEN` heading present; four `- [~]` lines, one per SHONEN.md box; no `[x]`.
- Every cited lane commit exists and is an ancestor of `main` (`git merge-base --is-ancestor`): `e4d1f7de` (declaration), `3baac2ef4` (supersession), `f63ce4150` (landing), `26a7aa205` (bookkeeping). The routed sibling commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d` exists in `kake-shokunin` (it is kake-owned, not kaidoku's).
- Lane repo clean and pushed: `jj-lane.sh state` → `branch=main local=26a7aa205… remote=26a7aa205… ahead=0 behind=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/main` prints `26a7aa205f9e4a180ddbe2e8492789d61ab286de`.
- Prompt `.ufo/prompts/kaidoku-round-96.md` carries the full `templates/round-prompt.md` contract (sections 1–5 rendered verbatim) plus hyaku addendum §6; the axes line matches `shokunin.conf` line 45 (`coverage + depth + calibration (reverse engineering with REA)`).
- Timing note (status-neutral): the declaration commit `e4d1f7de` is author-dated 14:12:38 -0300, ~90 s before the watchdog launch line 14:14:06 -0300; the report and all later commits sit inside the window.
- No marker: the report names real committed work with evidence pointers throughout.

## 2. Per-claim re-check (re-measured over committed bytes by this judge)

### R96-C1 — calibration (measured; claims rest on lane-owned gates: evidence-verified per §Gate standard)

Gate-standard handling: the claim's counters (`tools/round-96/kill-rule-v2.py`, the v6 battery, `symlink-probe-v2.py`) are lane-owned gates; this judge verified their **committed evidence** — self-test tallies (wave seat `w1/ExecRepro.md`: v6 selftest 13/13, kill-rule selftest green), frozen-run verdicts (the `l1/scores/` receipts) and the revision each names — and re-measured the receipt fields themselves. No gate was re-executed.

- Pins: `sha256sum -c .ufo/waves/round-96/pins.sha256` → 60 entries, **0 mismatches** (run by this judge at closure).
- Before (base `0ea695e8`), `pre/c1-legacy-rule-at-base.json`: label `r95-rule mutants killed 5 of 10`; per-mutant rows `killed=true` only for M1/M5/M7/M8/M9 → survivors **M2/M3/M4/M6/M10**, exactly as reported.
- After, `l1/scores/c1-kill-rule-at-landing.json`: `counts` = `{mutants 10/10 killed, forgeries 10/10 refused, negctl 3/3 refused, probe 1/1 consistent, honest 1/1 accepted}`; `identity_not_killed true`; `world_revision f63ce415…`; label matches the report verbatim.
- Byte binding: `git show f63ce415:tools/round-96/stop-boundary-repair-battery-v6.py | sha256sum` → `7d7d559ac144eda6d163dd1d9ab26ed95ac089e18ccbb029bd91ae4277e46c06` = `honest-pos-at-landing.json` `counter_sha256`; its `revision` and `head` both equal `f63ce415…`. The receipt is bound to the exact committed counter bytes at the landing.
- Unbound fields: before `pre/c1-v5-admits-unbound-at-base.json` label `unbound accepted 5 of 6 (1 crash); nojson exit 0`, `nojson.receipt_written=false`, `unbound: 5`. After: the kill-rule receipt's `K-forgeries` rows refuse six fixtures with one typed reason each (`counter-pin-not-bound`, `head-not-bound`, `met-not-recomputed`, `repair-pin-not-bound`, `counts-missing-key:fresh_scored`, `verdict-pin-not-bound`).
- Probe write escape: before `pre/c1-probe-writer-unbound-at-base.json` `before.victim_intact=false`; after `l1/scores/c1-symlink-v6-at-landing.json` `verdict="hardened"`, `victim_intact=true`.
- Wave: `r96-w1-results.json` — 12 seats, 12 results, none dead; attack seats 6/12 = 50 %.
- **Verdict: improved** on the frozen predicate. The broader wording ("every unbound field is bound") is honestly not claimed; named limits 1–13 are disclosed in the lesson and routed to round 97.

### R96-C2 — depth (measured)

- Plain re-measure by this judge: `git show f63ce415:SKILL.md` split at `## Queue-drain craft `, counting `^- \*\*` rows → **35 blocks** (base `0ea695e8`: **34**); block 35 reads `- **35. A kill rule covers every gate its instrument asserts, and a green verdict exists only throug…`.
- Receipts at the landing: `c2-after-block35.json` exit 0 `ok`; junk control `c2-junk-at-landing.json` exit 1; `c2-depth-v2-at-landing.json` exit 0 `blocks 35 resolved 35`; `c2-depth-v3-at-landing.json` exit 0 `blocks 35, resolved 35, required-shaped 1/1`.
- Before side: `pre/c2-base-depth-v2.txt` `blocks 34 resolved 34 expect 35 … exit=1`; `pre/c2-base-block35-after-manifest.json` exit 1.
- `corpus/QUALITY.md` rows 193 and 194 present at the landing (Row 193 kill-rule gate coverage; Row 194 self-verification mandatory on every exit).
- **Verdict: improved** on the frozen predicate; the predicate is a vocabulary check (named limit 14), disclosed by the lane.

### Harm check

`git diff 0ea695e8 26a7aa20 -- SCORECARD.md`: coverage, depth, calibration, freshness numeric proxies all unchanged at 10.0; the round appends its section and one capability row, retires nothing. **No axis harmed.**

## 3. Discernment spot-check (LEARNING.md — sampled from `corpus/lessons/round-96.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S321 `/usr/bin/printf` (new row) | admit | `sha256sum /usr/bin/printf` → `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`, `stat -c %s` → 76088 B — both match the row, the lesson and the knowledge entry; receipt `pre/s321-fresh-source2-at-base.json` `exit 0`, `met_target true`, label byte-matches the quoted text | **agree** | the row's `teaches` is the measured property (source diversity of the held-out arm), pinned by digest, recheck re-runnable; the knowledge entry's provenance trio (`source:`/`verified-at:`/`recheck:`) cites it |
| `/usr/bin/head` | reject (no row) | `sha256sum /usr/bin/head` → `313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1` matches the lesson; `w1/fs2-head-repro.json` exit 0 `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1` — head performs identically | **agree** | head adds no property S321 lacks; the stated flip condition (a cited claim needing a third distinct source) is the right bar |

The ≤25-word quote grounding S321's `teaches` is verified: its label portion byte-matches the committed receipt's `label`, and the trailing `met True exit 0` matches the receipt's `met_target`/`exit` fields.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → **exit 0, `ok`**; W04 duplicate-URL warnings 32 (unchanged from before the round). `corpus/SOURCES.md` 225 → 226 rows, one tier-A row (S321), no existing row edited.

## 4. Trend verdicts (this judge's grades, evidence per above)

- **expansion: unchanged** — `git diff 0ea695e8 26a7aa20 -- corpus/README.md` is empty (coverage map not extended); S321 is a second source for ground the map already holds (kill-rule / stop-boundary families); the knowledge entry lands on held ground.
- **quality: improved** — five round-95 survivors now killed (5/10 → 10/10 under the frozen rule); six unbound forgeries refused with typed reasons; the no-`--json-out` green exit removed (`receipt_written=false` → mandatory receipt); the probe's own write escape closed on its public leg (`victim_intact false` → `true`); the M96-a attribution defect named and corrected by re-measurement at the landing.
- **discernment: improved** — the lane reported `unchanged` at filing time (no non-author check existed then; correct). This closure spot-check now supplies it and agrees with the gate on the sampled admit (S321) and reject (`/usr/bin/head`) — LEARNING.md's improved condition. The wave's attack seats (ReviewerInstruments H-1, CriticC1/C2, MutationC1 N1–N10, SentinelWrite) found real limits the gate disclosed as named limits rather than hiding; that disclosure is itself calibration-positive.

## 5. Axis verdicts

| axis | verdict |
|---|---|
| calibration | improved |
| depth | improved |
| coverage | unchanged |
| freshness | unchanged |
| adjacency | unchanged (sibling writer defect routed to kake, not absorbed; `PROVINCE.md` untouched this round) |

## 6. Routed defects and carried items (the lane acts next round; status-neutral)

1. Concur with the lane's round-97 routes: byte binding through `git cat-file blob` (named limit 2 / M96-a), `met_target` typed (limit 3 / M96-f), the M11 `--rev ≠ HEAD` frozen scenario (limit 4 / M96-e), remaining unbound fields and the COUNT_KEYS allow-list (limit 5), `--json-out` required on `kill-rule-v2.py` with a re-read of its own receipt (limit 7), bool and extra-key fixtures (limit 6), the planted-link K-probe leg on the v6 writer (limits 8/16 / M96-h), crash-vs-false kill semantics (limit 17 / N9), the cwd-dependent `--honest-dir` (limit 18 / M96-j), and C2's vocabulary-successor predicate (limit 14).
2. kake-shokunin owns `scripts/instrument_receipts.py:643-646` (commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d`, plain `open` on `destination + ".tmp"`): routed to kake; kaidoku correctly did not edit it.
3. For the operator (promotion is operator-owned): every SHONEN box now carries non-author-checkable evidence — SKILL.md craft blocks incl. block 35 (checked 34→35 by this judge), `LOG.md` round-96 entry with the end-to-end public battery run (`## Measured` receipts re-verified here), counting commands executable from the committed text (re-run as the plain re-measures above), and `PROVINCE.md` untouched with no sibling overlap (`w1/ConnectorOverlap.md`).

## 7. Closure

Both claims verify on their frozen predicates; no axis is harmed; the report is conformant; the round is **admitted**. Conformance defects: none beyond the status-neutral timing note in §1.
