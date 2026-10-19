# EX-06 probe interplay — citation-drift probe vs the rule-#14 scratch tree

Seat EX-06 | chain c1 | role executor | wave arc3-loop1-round2 | 2026-10-19

Task: run the citation-drift probe (copy under `/var/tmp`) against the same
scratch tree the c1 rule-#14 work uses — `findings=0` expected because the new
rule's citations resolve.

## 1. Setup and provenance (all read-only over the repo)

- **Probe copy**: `/var/tmp/arc3-l1r2-EX-06/gate/` is a byte-identical copy of
  `.ufo/gates/citation-drift/` — probe `e2665074…`, pointer table `738b3a56…`
  (unchanged; not widened), expected `ff47bfd6…`. Selftest on the copy:
  `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`.
- **The chain's scratch tree**: `/dev/shm/vz1r2/tree` (VZ-1's committed copy of
  HEAD `14b1682b`, single snapshot commit `ed405a3`, worktree == HEAD blobs).
  My projections are copies of that same tree under `/var/tmp/arc3-l1r2-EX-06/`
  (`proj*`). Scratch-tree commits happen only inside those `/var/tmp` copies;
  the lane repo was never written or git-mutated (read-only `git show`/`sha256sum`).
- **Baselines** (frozen table, both modes): repo at HEAD `14b1682b` →
  `reported findings=0 exit=0`; the clean tree at `ed405a3` → same.
- Probe grading reads **Git objects at `--rev`**, never the moving worktree — an
  uncommitted treatment is invisible to it (by design; the landing flow commits).
- Cross-seat inputs, pinned at use (sha256): EX-01 `rule14.patch.md`
  `885fa537…`; EX-05 `fallback-rule14-candidate.txt` `debe4d4e…`;
  EX-05 `insert-rule.py` `c064bef4…`; EX-02 `commandA-scratch.py` `37bffa27…`;
  RV-2 `rule-citation-audit.py` `8c25b9ec…`; EX-04 `craft-pointer-truth.py`
  `1df6f510…`.

## 2. Before → after: the probe on the treated tree (the measurement asked for)

| # | Tree / rev | Probe (frozen table) | command A | Notes |
|---|---|---|---|---|
| B0 | repo HEAD `14b1682b` | 0 / exit 0, both modes | 13/13, 82/82 | baseline (re-measure of round-1 state) |
| B1 | clean tree `ed405a3` | 0 / exit 0 | — | the chain's scratch tree pre-treatment |
| S0 | stand-in block (dry-run harness validation) `2488036` | 0 both modes | 14/14 | superseded; kept as harness proof + controls |
| T1a | EX-01 **v1** payload (896 B `a47dc38d…` → SKILL 385 L `19057c13…`) `00b672e3` | 0 both modes | 14/14 | v1 identities independently **reproduced and MATCHed** |
| T1b | v1 + SHONEN refresh (81-252) `aea0a18c` | 0 (strict) | 14/14 | |
| T2a | EX-01 **v2** payload (1,071 B `6cc388cb…` → SKILL 387 L `a8170b96…`) `b35ac223` | 0 both modes | 14/14 | v2 = final text (mid-wave revision, fresh identities in `identity-final.txt`) |
| T2b | v2 + SHONEN refresh (81-254) `89b8957d` | 0 (strict) | 14/14 | the integrator's same-commit shape (EX-01 §4.3) |
| T3 | EX-05 fallback text `debe4d4e…` via EX-05 harness `1dac4c64` | 0 (strict) | 14/14 | the "frozen wording verbatim" alternative |

**Custom scratch tables** (the sanctioned custom-table recipe — committed table
NOT widened; each scratch table pinned in its own scratch `expected.json`, per
the round-1 C2 ruling): the rule's own citations were extracted **out of the
treated SKILL.md** and verified against their named targets —
v1 table (`a17e09a2…`) vs v1 tree: 0; v2 table (`21d421ec…`) vs v2 tree: 0.
v2 entries and what each verified: headline `SKILL.md:240` exact; `CR-2.md:86-89`
holds the F2 fix; `verdict.md:149-153` holds "Three different applied identities";
`evm-real-solc.md:7` holds the recheck line (the counted corpus/knowledge
citation); `SCORECARD.md:1366-1368` and `LOG.md:1411-1412` hold the fresh
10,225 B / `dd986f56…` landing record.

**Cross-instruments on the treated tree** (v2): RV-2's audit — `dead=0`,
`resolved=59`; form_flags = 2, both the **same class**: rule #12's pre-existing
`SCORECARD.md:544-545` at HEAD and rule #14's `SCORECARD.md:1366-1368`
(bare-line-into-in-place-target per its heuristic; rule #12's flag exists at
HEAD untouched — RV-2 owns adjudication). EX-04's pointer-truth: v2 tree FAILs
`A2-end` (243<254) + `A3-count` (13/13 vs 14) — **probe-clean ≠ pointer-truth**;
with the SHONEN refresh (`81-254`, `14/14`) all four assertions PASS. So the
probe's needle stays green while SHONEN is stale, exactly the blind spot EX-04
exists to cover; the same-commit refresh closes it.

Verdict: **the new rule's citations resolve; the treated tree grades
`findings=0` under the frozen table in both modes, and every generation/placement
tested (v1, v2, fallback text; EX-01 recipe and EX-05 harness) holds.**

## 3. Attacks / refutations attempted (each with a run, not an assertion)

| Attack | Run | Verdict |
|---|---|---|
| "0 findings is vacuous — the frozen table cannot see the new rule" | design read: the table's only SKILL.md entry is an `anchor`; it does not grade rule #14's own citations | **CONFIRMED blind spot** (by design, table not widened per r4 precedent); covered by the custom pinned tables + RV-2 + EX-04 |
| Wrong citation numbers must redden the custom table (stand-in form) | stand-in tree `proj-ctl` `ff9f7ff0`, `CR-2.md:202→:203`, `entry:1-33→:4-6` → 2× `citation_dead`, exit 1 | PASS (bites) |
| Wrong citation numbers must redden the custom table (v1-real) | `proj2-ctl` `a676ca64`, entry:7->:8 and SCORECARD:1366-1368->:1360-1362 -> 2x `citation_dead`, exit 1 | PASS (bites) |
| Wrong v2 numbers (`entry:7→:8`, `SCORECARD:1366-1368→1360-1362`) | `proj3-ctl` `f1117eb8` → 2× `citation_dead`, exit 1 | PASS (bites) |
| A broken SHONEN rule-range must redden the frozen table | `proj-neg` `d38870c5` (stand-in) and `proj2-neg` `02c75cb8` (v1-real), each cutting range end below rule #13's line → `citation_dead shonen-skill-range`, exit 1 | PASS (bites) |
| Mid-wave payload revision (v1→v2) could carry stale identities | extracted and hashed both payload generations; applied both; SKILL sizes/hashes match EX-01's claims exactly (896 B `a47dc38d…`/385 L `19057c13…`; 1,071 B `6cc388cb…`/387 L `a8170b96…`) | REFUTED (fresh identities are current; v1 kept as labeled history) |
| Placement dependence (EX-05's before-heading harness vs EX-01's after-rule-13 recipe) | both placements built and probed (T3 / T1a-T2a) | REFUTED (both clean; blank-line layout differs, verdicts don't) |
| Uncommitted treatment | probe grades `--rev` objects only; worktree edits invisible | CONFIRMED (operational note: re-run at the work commit, not the worktree) |
| Probe internals broken in the copy | selftest 13/13 CLEAN | REFUTED |

## 4. Gaps / named residuals

- The **final landing text/placement** (EX-01 v2 vs fallback vs scoped) was not
  frozen at my close; all three circulated forms were measured clean. If the
  parent lands a different text, my harness (`apply-ex01-rule14-v2.py` +
  `insert-rule.ex05.py` + table generator in the log) re-runs in minutes.
- The RV-2 form flag on `SCORECARD.md:1366-1368` is real per its heuristic but
  matches pre-existing rule #12; **RV-2's to adjudicate**, not mine.
- `SHONEN.md:6` must be refreshed in the same commit (EX-04 A2/A3 fail otherwise,
  measured) — the probe alone will not catch that omission (measured).
- The committed pointer table / expected must stay byte-stable at the records
  commit (`738b3a56…` / `ff47bfd6…`); any C2-side change is EX-16's guard to
  keep honest — re-check at landing belongs to the cross seats.

Evidence: `/var/tmp/arc3-l1r2-EX-06/logs/interplay-log.txt` (89 lines, all runs
above verbatim) + copies under `evidence/` with `manifest.sha256.txt`.
