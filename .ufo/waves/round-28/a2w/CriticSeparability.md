# CriticSeparability: causal separability of R28-C1 and R28-C2 (round 28, attempt 2)

Seat: KaidokuR28a2.CriticSeparability (critic, leaf). Lane tip read: 9db24c9e10287d44d9f780d782ab608f3c84ff5a.
Attacked: the independence of the two frozen counters, `tools/round-28/c1-heldout-naming.py` and `tools/round-28/c2-filtered-flag.py`, together with their data, entries, SOURCES rows and the round-28 lesson Gate.
Installs: none. Network: none. REA: none. Lane: read only. All mutation was done in the sandbox clone `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticSeparability/clone` and in throwaway clones at `.../CriticSeparability/p`.

## Verdict: separable, with one entanglement in the entry gate (fixable, not exploited at the tip)

Each counter's verdict survives deleting the other claim's data, knowledge entry and SOURCES rows (observation, E1 to E7 below). The one entanglement: C1's `entry_ok` accepts any cited S### row that is new, mined, opened 2026-10-22 and in the Gate. The C1 entry's `source:` line cites C2's rows S084 and S085 as well as S086. So C2's rows alone can set C1's `entry_ok` to 1 (E1). At the tip, S086 carries it by itself (E2), and C1 fails anyway on `runs_ok` 60/61. Neither claim's success is manufactured by the other's artifacts at 9db24c9e (observation).

## Dependency list (observation unless labelled)

| shared item | read by C1 counter | read by C2 counter | coupling |
|---|---|---|---|
| `corpus/SOURCES.md` | yes, any cited new mined row (`check_entry`) | yes, same rule | C1 entry cites S084, S085 (C2's rows) and S086; C2 entry cites S084, S085, S078, S076 |
| `corpus/lessons/round-28.md` `## Gate` | yes | yes | one Gate table lists S084, S085, S086 for both claims |
| `tools/round-25/a2/resolve-selectors.py` | yes, loaded and pinned (sha `4be91566...`) | no | the C2 producer `tools/round-28/collect-c2.py` calls the resolver's `_get`. Editing the resolver for C2 would make C1 exit 2 (producer-level coupling only) |
| `corpus/evidence/round-28/c1/heldout.tsv` and `c2/selectors.tsv` | heldout.tsv (pinned) | selectors.tsv (pinned) | all 187 C1 selectors are the 187 `r28-heldout` rows of C2's 230; the files are separate and separately pinned |
| openchain responses `c1/db/openchain-*.json` and `c2/db/openchain-*.json` | c1/db only | c2/db only | 187 of 187 shared names are byte-identical; separate files and manifests |
| knowledge entries | `2026-10-22-r28-evm-heldout-selector-naming.md` | `2026-10-22-r28-openchain-filtered-flag.md` | neither counter reads the other's entry. The C1 entry's lines 49-50 explain the "inert filter step" with C2's rule. Both entries cite the round-25 entry, which neither counter reads |
| constants BASE 935c3660, OPENED 2026-10-22, `check_entry`, `gate_ids`, `sources_rows` | duplicated code | duplicated code | same any-row gate logic in both counters |

## Experiments (sandbox clones of 9db24c9e; each step commits one change and then runs both counters)

Command: `bash /fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticSeparability/probe.sh`. Exit 0. Ran 2026-10-22T18:25:04Z to 18:25:56Z. Output excerpts (from probe.out):

- E0, the tip as committed: C1 `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1 (exit 1)`; C2 `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1 (exit 0)`.
- E1, S086 row and Gate row removed: C1 `entry_ok=1 (exit 1)`; C2 `entry_ok=1 (exit 0)`. **C2's rows alone satisfy C1's entry gate.**
- E2, S084 and S085 rows and Gate rows removed: C1 `entry_ok=1 (exit 1)`; C2 `entry_ok=0 (exit 1)`. S086 carries C1 by itself; C2 needs its own rows.
- E3, S084, S085 and S086 all removed: C1 `entry_ok=0`; C2 `entry_ok=0`.
- E4, C1 data removed (runs.tsv, envelopes/, db/, tally.json): C1 `runs_ok=0/61 ... (exit 1)`; C2 unchanged `(exit 0)`.
- E5, C2 db/ removed: C1 unchanged `runs_ok=60/61 ... entry_ok=1 (exit 1)`; C2 `responses_complete=0/230 (exit 1)`.
- E6, C2 entry removed: C1 unchanged `entry_ok=1`; C2 `entry_ok=0 (exit 1)`.
- E7, C1 entry removed: C1 `entry_ok=0`; C2 unchanged `(exit 0)`.
- E8, C2's 187 held-out responses replaced by C1's bytes plus C1's manifest rows: C2 `responses_complete=105/230 entries=142 ... entry_ok=0 (exit 1)`. The 82 copies whose C1 timestamp is before the C2 freeze (17:21:55Z) are refused. The 62 copies timestamped after it are accepted.

Fetch independence check (inline python over both committed manifests, exit 0, 18:26:19Z): `shared 187 same utc string 0`, `C2 earlier than C1 for 0 selectors; later for 187`, `C2 manifest utc monotone: True`, `C1 openchain utc after C2 freeze 17:21:55Z: 62`. Inference: C2 made a second, sequential fetch, not a copy of C1's files. This rests on self-reported manifest timestamps. The bytes cannot show it, because the 187 bodies are identical.

## Findings

1. **Any-row entry gate (impacted axis: coverage, R28-C1 provenance).** Fixable defect; both counters are frozen. E1 shows that C1's `entry_ok` would read 1 on C2's rows alone. At the tip this is not exploited, because E2 shows S086 suffices. Counterexample: a future tip where S086 is reverted or left out of the Gate still reports C1 `entry_ok=1`.
2. **Used-by gap (impacted axis: provenance).** Fixable defect. The C1 entry's `source:` line cites S084 and S085, yet both rows' used-by cells name only `corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`. S086's used-by cell names only the C1 entry. Command: inline python over the clone's `corpus/SOURCES.md`, 18:26:19Z, excerpt `S084 ... used-by: corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`.
3. **The C1 data do not need C2's claim (holds).** The C1 entry explains the inert filter step through C2's rule (S084, S085). But the C1 data show it directly: `C1 openchain entries with filtered != false: 0`. The C1 tally gives `openchain_sole_unfiltered` named 143 and the primary rule named 137, from flags as observed. C1's numbers would not change if C2's rule were false (observation from the counter code, `rule_outputs` reads only observed flags).
4. **C2's discriminating branch rests only on the round-25 subset (tradeoff, not entanglement).** 0 of the 187 held-out selectors are canonical keys, and 10 of the 43 round-25 selectors are. So all 59 `predicted_true` entries come from round-25 selectors. The 187 shared selectors exercise only the predicted-false branch, and their bytes duplicate C1's lookups. Any claim that the rule was tested on 230 selectors should say the filtered=true branch was exercised by 10 selectors (59 entries), all from round 25.

## Smallest safe correction (for the L1; the counters stay frozen)

- Add `corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md` to the used-by cells of S084 and S085. Alternatively, move S084 and S085 out of the C1 `source:` line into the entry body.
- In the round report, state that C1's `entry_ok` is carried by S086 alone (E2), and quote E1 as the known weakness of the any-row gate. Route this to the next round's counters: require the claim-specific row named in claims.json, not any new row.
- In C2's limits, state finding 4.

## Artifacts (sha256)

- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticSeparability/probe.sh` `16cf5494f5063d7b4c4e7496e918663a91c2c38bc01c9af5395c6c9b64a50f6a`
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticSeparability/probe.out` `cf928d1eb5d0c7a60b9ed92ccec3e4dd8044c2d81912c7d3074c6b9859544108`
- Sandbox clone `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticSeparability/clone` at HEAD 9db24c9e10287d44d9f780d782ab608f3c84ff5a (unmodified). At 18:24:23Z both counters ran there with exit 1 for C1 and exit 0 for C2, the same numbers as E0.
