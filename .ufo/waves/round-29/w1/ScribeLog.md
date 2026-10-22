# Round-29 wave-1 seat ScribeLog — LOG.md round-29 entry draft

Seat `KaidokuR29.ScribeLog`, 2026-10-22, 20:20Z–20:25Z. Leaf: no subagent, no REA, no network
lookup, no tool installed. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at
`18be864a528873b2b70d8c94e31f880290249e90` (working tree dirty throughout: see finding F5).

## Deliverable

- Draft: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/draft.md`,
  sha256 `21c2800a5b62b19b96d6837605926a89b8c2d2062ffe8383edfec11fe9072efd`, 6013 bytes.
- Content: one `## 2026-10-22 — round 29 …` entry in the shape of the round-28 entry
  (`LOG.md:2985-2995`): motivating evidence for both claims, freeze, measurement, re-verification,
  learned, round-28 routed defects, mistakes M29-1..3, wave status, evidence pointers.
- It supersedes the 12-line round-29 entry currently uncommitted in the working tree at
  `LOG.md:2997-3007` (observed by `git diff --stat -- LOG.md` → `LOG.md | 12 ++++++++++++`,
  exit 0, 20:22Z): same bullets, plus the re-verification block, the wave-status block and the
  evidence-pointer line.

## Behavior (what I ran, in order)

All commands ran in the lane, read-only. Counters and gates take `--rev`, so they read committed
bytes only; nothing was fetched and no lane file was written by me except this report.

| # | command | exact output excerpt | exit | UTC |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-29/c1-fresh-naming.py --root <LANE> --rev 18be864a…` | `primary rule openchain_sole_unfiltered_args_consistent: named 122, right 122, wrong 0, no_name 30` / `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` | 0 | 20:21:25Z, repeated 20:23:36Z |
| 2 | `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <LANE> --rev 18be864a…` | `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1` | 0 | 20:21:26Z, repeated 20:23:38Z |
| 3 | `python3 -I -B tools/round-29/c1-fresh-naming.py --selftest` | `selftest cases=22 failures=0` | 0 | 20:21:35Z |
| 4 | `python3 -I -B tools/round-29/c2-filtered-unseen.py --selftest` | `selftest cases=19 failures=0` | 0 | 20:21:35Z |
| 5 | `python3 -I -B tools/round-29/freeze-gate.py --root . --rev 18be864a… --disclosures corpus/claim-freezes-v2.tsv` | `"audited": 19, "clean": 2 … "disclosures": {"exact": 19, "mismatched": [], "missing": [], "of": 19 …}`; verdicts `FLAGGED 17, CLEAN 2` (round-24, round-28 `claims-c2`); round-29 `FLAGGED INSTRUMENT_UNPINNED tools/round-28/c1-heldout-naming.py` | 0 | 20:21:33Z, `--disclosures` re-run 20:23:36Z |
| 6 | `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root . --rev 18be864a… --disclosures corpus/claim-freezes.tsv` | `"audited": 16, "clean": 1 … "disclosures": {"exact": 16, "mismatched": [], "missing": [], "of": 16 …}` | 0 | 20:21:33Z |
| 7 | `sh /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | six `kaidoku W04 … duplicate url` lines (S033, S047, S054, S062, S069, S083) then `kaidoku ok /home/vgpnk/…/corpus/SOURCES.md` | 0 | 20:21:50Z, repeated 20:23:36Z |
| 8 | `sh tools/round-29/prefile-check.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | `prefile: NOT CLEAN (14 paths)` | 1 | 20:22:41Z |
| 9 | same, re-run | `prefile: NOT CLEAN (15 paths)` | 1 | 20:24:38Z |
| 10 | `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'` at `bacbe9cc` / `18be864a` | `112` / `114` | 0 | 20:22:37Z |
| 11 | `git cat-file blob <rev>:.ufo/waves/round-29/claims.json \| sha256sum` at `dbd87cfa` / `18be864a` | `76bc0d8f556019763157bbb74cd43b9983b9e7cf77ad9d92cae898365a60cf79` both times | 0 | 20:23Z |
| 12 | `git merge-base --is-ancestor dbd87cfa 4fcea978`; `git rev-list --count dbd87cfa..18be864a` | exit 0; `3` | 0 | 20:22:41Z |

Observation: every re-run reproduced the L1's after receipts
(`.ufo/waves/round-29/after/c1-at-18be864a.txt`, `c2-at-18be864a.txt`) line for line; the after
receipts record the same numbers at 20:16:35Z and 20:16:37Z.

## Gates

- C1 and C2 counters: both target-met, exit 0, at the measured tip (rows 1–2). Selftests green
  with all 22 and 19 cases (rows 3–4).
- Freeze gates: both exit 0 with `--disclosures`; both ledgers `exact` (16/16 and 19/19), no
  `mismatched`, `missing` or `stray` entries (rows 5–6).
- Census: exit 0, no new warning (row 7).
- Pre-file gate: **red, by design, while the wave runs** (rows 8–9); it is a filing-time gate, and
  the LOG entry must not claim it passed. See F5.

## Touched surfaces

- Written by me: this report only, at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/w1/ScribeLog.md`.
- Scratch: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/` (`draft.md`, `out/`, `tmp/`).
- Lane files read: `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-29.md`, `corpus/lessons/round-28-verifier-spotcheck.md`, both round-29
  knowledge entries, `.ufo/waves/round-29/{claims.json,w1*,before/,after/}`,
  `corpus/evidence/round-29/c1/{runs.tsv,tally.json,db/manifest.json}`,
  `corpus/evidence/round-29/c2/db/manifest.json`, `tools/round-29/*`.
- No git or jj write anywhere; no REA; no 4byte.directory or openchain request.

## Findings

**F1 — both counters reproduce at the measured tip.** Observation. Commands 1–2 at
`18be864a…`, exit 0 at 20:21:25Z and 20:21:26Z; exact lines quoted above. The draft may state
these as measured, not merely copied from the L1's receipts.

**F2 — freeze precedes data and the claims file did not move.** Observation. `claims.json` blob
sha256 `76bc0d8f…` at `dbd87cfa` and at `18be864a` (command 11); `git merge-base --is-ancestor
dbd87cfa 4fcea978` exit 0; commit times `dbd87cfa` 20:03:06Z, `4fcea978` 20:09:09Z, `18be864a`
20:16:21Z; first C1 run `n01 2026-10-22T20:03:21Z` (`corpus/evidence/round-29/c1/runs.tsv`).

**F3 — census is clean over the tip SOURCES.md, which carries both new rows.** Observation.
Command 7, exit 0; `corpus/SOURCES.md` is 177 lines with `S087` at `:93` and `S088` at `:94`;
`git diff --stat -- corpus/SOURCES.md` empty. The six W04 duplicate-URL warnings are on
pre-existing rows and are unchanged by this round. The L1's own `before/census.txt` (20:07:16Z)
ran before those rows were written and says `SOURCES.md unchanged since base`; my run is the
first census over the filed table.

**F4 — the round-29 freeze is FLAGGED by both gates, and that is already disclosed.** Observation.
Command 5 and 6: round-29 verdict `FLAGGED` with `INSTRUMENT_UNPINNED` on
`tools/round-28/c1-heldout-naming.py`; M29-3 in `corpus/lessons/round-29.md` and the round-29 row
of `corpus/claim-freezes-v2.tsv`. The gates exit 0 because no `--require-clean` is passed; a
future run with `--require-clean round-29` would exit 1. Inference: the LOG entry should say the
flag exists rather than imply a clean audit.

**F5 — the lane working tree is dirty mid-wave, and one dirty path is a committed measured
artifact.** Observation. Command 9, `prefile: NOT CLEAN (15 paths)`, exit 1, 20:24:38Z. Fourteen of
the paths are the round's own in-flight material (`M LOG.md`, `M SCORECARD.md`,
`M tools/round-29/prefile-check.sh` and the eleven untracked `after/` and
`w1*`/`w1/` paths). The fifteenth is
`M corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md` — a committed lane file at
`18be864a` — modified at 2026-10-22 17:23:56 -03:00 (20:23:56Z) by two lines
(`git diff -- corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`): the `string` →
`bytes` bullet now reads `castVoteWithReason`, `setBaseURI`, and `propose`, whose `string[]` is
also inferred as `bytes[]`; seat `ExecArgsBreakdown`. At 20:22:41Z the same command printed 14
paths and this file was not among them, so the edit landed during this seat's run. The counters
read committed bytes (`--rev`), so the measured numbers are unaffected; the file must be committed
or dropped before filing (QUALITY row 47 / M29-1).

**F6 — `tools/round-29/prefile-check.sh` is itself dirty.** Observation. Working-tree diff against
`18be864a` is 3 insertions/2 deletions, all inside the comment and the status call:
`out=$(GIT_OPTIONAL_LOCKS=0 git -C "$1" status --porcelain)`. Its v2 red-then-green receipt is
`.ufo/waves/round-29/after/prefile-check-red-r28-v2.txt` (20:21:57Z). Until that commit lands, the
gate a report cites is not the gate in the tree at `18be864a`.

**F7 — the wave is live.** Observation. `w1/swarm-registry.json` createdAt
`2026-10-22T20:20:04.631Z`, 44 members (executor 15, reviewer 10, critic 7, mutation-tester 5,
scout 3, scribe 3, connector 1); `w1-dispatch.json` `{"spawn": 44, "resume": 0, "total": 44}`. The
draft says results are pending; the L1 has to replace that line with the real outcome before the
entry is landed.

## Out of scope

- No claim re-measurement beyond the offline counters; no new REA run, no new lookup, no new fetch.
- No judge of the claims: verdicts belong to the canonical Rust judge; this report states counters,
  gates and their limits only.
- The claim text's `pre_freeze_probe: none` is the frozen file's own statement (observation of the
  record); I did not and cannot verify absence of pre-freeze requests independently.
- No edit to `LOG.md` itself (lane read-only); the draft stays in scratch for the L1 to land.

## Artifacts (all sha256)

| path | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/draft.md` | `21c2800a5b62b19b96d6837605926a89b8c2d2062ffe8383edfec11fe9072efd` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/out/c1-count.txt` | `a847042f88334dfa54b6673a3a056dbef4ac01562de31235ebd1bd8a21adf762` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/out/c2-count.txt` | `6008aaede9917ec62c61255ad9e2cfcae7f52f48807619244f44a0fb5f9b41da` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/out/census.txt` | `b426b2556badd31945877202cc012401067ac2abf81e690e4447d10fcefbd757` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/out/gate-v1.txt` | `ad456b88913a2311b759bc0ef61bc1cea7a297b66caddc59370a87507d2675d7` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/out/gate-v2.txt` | `678e9d55e26e7d6c10afcc2eda1a3a6d966bb0c46b75a83be54199513f88f739` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/out/prefile-now.txt` | `221a992863d6b683a7e1908386ec3d6e8afd46c47ef8a634fa2ec491d36f56a3` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/tmp/c1-selftest.txt` | `db513ee5f8e16016a8b6e4b82d67a436a4bf51a6a89667348f30e6ae19929dfe` |
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeLog/tmp/c2-selftest.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |

Known limit of the artifacts: `out/gate-v1.txt` and `out/gate-v2.txt` hold the gate JSON with the
`freezes` array removed by `python3 -c` (pipelines, `PIPESTATUS` printed literally in a temporary
shell), so the exit codes in those files are the shell's, not the gate's; the gate exits are taken
from the direct runs at 20:21:33Z (both 0). `out/prefile-now.txt` is the 20:24:38Z run.
