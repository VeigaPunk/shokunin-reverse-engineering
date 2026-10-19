# Lesson — arc3-loop1-round12 (steered round 12): mistakes mined while finishing a frozen round

author: kaidoku-shokunin (L1), 2026-10-19, kaika W2a integration session
scope: only mistakes this round shows, first-hand; earlier rounds' classes are in the
kaika W1 STATE dossier (`/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/kaidoku-state.md` §4).
`R12` = `.ufo/waves/arc3-loop1-round12`.

## Mistakes

| # | class | evidence pointer | captured-by criterion | fix |
|---|---|---|---|---|
| 1 | Seeded measurement overstated a gate: three single-fault seeds "proved" substring needles that let 7/24 breaking mutants through (suffix renames of a pinned prefix, unpinned round/claims tokens, r11's bare `TMPDIR` token next to a sentence that names `/tmp`) | `R12/claims/c3/PL-4.md:71-98` (3/3 seeds caught); `R12/integration/mutation/table1-rerun.md` (PL-4 column: 17/24 killed) | `none` — `corpus/QUALITY.md:11-25` grades entries, not instrument needles | Before landing a needle, run a mutation matrix with breaking **and** harmless mutants; report kill rate and false-alarm rate, not seed count |
| 2 | Over-correction: full-line pins killed every breaking mutant but rejected harmless rewording (`expect`→`yield`; `; then run`→`; and then run`) | `R12/integration/mutation/table1-rerun.md` (`ec3ae3aa` column, 1/9 false alarm); R12Reviewer finding (C3 major, tightened rows brittle) | `none` | Pin delimited tokens as order-free lookaheads `^recheck: (?=.*tok1)(?=.*tok2)…`; landed table sha256 `7994eec7…` |
| 3 | Custody SOP skipped on live CLI legs: r11's and r12's live `rea.mjs` calls ran with no same-round pre-pair (0 receipt files under `arc3-loop1-round11/` and the r12 seat tree), and this integration's live recheck also ran before any pre-pair | `SKILL.md` §Config custody ("no probe runs on an unpaired round"); `find .ufo/waves/arc3-loop1-round11 -ipath '*receipt*'` → 0; `R12/receipts/config-post-only.txt` (post-only, labeled unpaired) and `R12/receipts/config-post-only-2.txt` | SOP text only (`SKILL.md` §Config custody); no gate enforces it | No zero-drift claim is made for r12. The first post-only receipt (21:38:54Z) records all five custody paths with ctime before the integration leg (latest ctime 19:09:51Z; first live envelope 21:33:02Z) — a no-rewrite bound for that leg, not a pair. `~/.bashrc` then changed content at 21:46:35Z, after the last live leg (`CONTENT-DRIFT paths=4/5 drift=1`; the second receipt brackets it); `[INFERENCE]` an operator/orchestrator edit (the fleet-wide `cd` alias repair notice arrived in that window) — operator-owned, never touched by the lane. Next live round freezes the pre-pair before dispatching any probing L2 |
| 4 | A verdict seat's computed result cited with no retained script (VZ-1's 27/27 ID reconciliation) | `R12/claims/verdicts/VZ-1.md:26-30`; R12Reviewer finding (C1 major, unreproducible claim) | QUALITY #6 (a REA claim cites its Evidence ID or exact reproducing call) — partially | Retained `R12/integration/c1/reconcile-all-go-ids.mjs`; output `records=27 matched=27`, exit 0 |
| 5 | Stale status clause inside a cited range: r11 entry line 23 still says Command A 90/90 "remains pending" after it landed | `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:23`; R12Critic attack 2 | `none` | Rule #17 cites `:19` (behavior) instead of `:19-23`; the stale clause stays as written (append-only) and is carried debt with the D7 draft headers |
| 6 | Dispatch counting: one frozen seat (`CN-1`) never reported | `R12/claims-frozen.md:65-70`; `ls R12/claims/*/*.md \| wc -l` → 47 | lesson `corpus/lessons/2026-10-18-wave-dispatch-counting.md`; no QUALITY row | Recorded as a named non-completion, never as an inferred shortfall |
| 7 | Digest pinned without naming the serializer (VZ-1's first PL-4 hash used `ensure_ascii=False` → wrong `ec7636…`) | `R12/claims/verdicts/VZ-1.md:58` | `none` | Every table re-pin this round was computed as `json.dumps(t, indent=2) + "\n"` with a round-trip byte-equality check before writing `expected.json` |
| 8 | Frozen claim set ignored an active stagnation nudge (all owned proxies 10.0, no capability since arc2-r8, window past 10/10) | `R12/claims-frozen.md:11-16`; `/home/vgpnk/Projects/shokunin/AXES.md:66-73` ("should", not MUST) | `none` | Round 13 is planned as a capability/frontier move (`SCORECARD.md` round-12 `Planned:` line) |
| 9 | Line-shifting insert into a pinned file: the work commit `4072ebb` added a lessons-index row inside `corpus/README.md` (above `## Frontier`) and an inline correction line in `SHONEN.md`; the strict citation-drift probe at `4072ebb` then reported 5 `citation_dead` (`sc69-readme-177`, `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2`, `shonen-province-range`) — the live `SCORECARD.md:69` cites `corpus/README.md:180` and cannot be rewritten (append-only). The scout's simulation covered SKILL/SCORECARD/LOG growth but not these two files | `R12/integration/probe-at-4072ebb.txt`; fix commit (this lesson's commit) | `none` — census does not scope README/SHONEN; only the probe saw it | Removed the README row (the index cannot grow above `## Frontier` while `SCORECARD.md:69` pins `:180`); moved the SHONEN correction to EOF. Run the strict probe at the work commit before writing records; a simulation must include every file the commit touches |

Criteria added to `corpus/QUALITY.md` this round: **none**. The round's three claim slots are
held by the frozen claims; the instrument-side lessons (#1, #2, #7) are for the gate registry,
and the entry-side lessons (#3, #5) are queued as round-13 QUALITY rows.

## Gate

Each row is checkable from the repo:

- #1, #2: `R12/integration/mutation/table1-rerun.md` carries the per-mutant matrix for every
  needle version; `python3 R12/integration/c3/seeded-measurement.py` reruns the seeds on the
  landed table (`R12/integration/c3/seeded-run-lookahead.txt`).
- #3: `python3 .ufo/gates/custody-pair/custody-pair.py verify R12/receipts/config-post-only.txt R12/receipts/config-post-only-2.txt`
  → `CONTENT-DRIFT paths=4/5 drift=1` (`.bashrc` only): the two post-only captures bracket the operator-side edit; neither is a pre-pair.
- #4: `node R12/integration/c1/reconcile-all-go-ids.mjs` exits 0 with `matched=27`.
- #5: `grep -c 'remains pending' corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md` → 1 (the debt is still open).
- #6: `ls R12/claims/verdicts/*.md | wc -l` → 11.
- #9: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <commit> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict`
  → `failed findings=5` at `4072ebb`, `clean findings=0` at the fix commit.
