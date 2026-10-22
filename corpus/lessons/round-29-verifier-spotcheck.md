# kaidoku round 29: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Session `HyakuCloseKaidoku29`, 2026-10-22, about 20:43Z to 20:52Z. Range `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47..33570c3ab8e4c9748fa48ae4609113c561e20e05`. Report `.ufo/reports/round-29/kaidoku.md` (fleet `f9560fa5f8b6e49531d689f7aab5e32ea47dce2c`). Four read-only seats were dispatched by this session: `ReMeasureC1`, `ReMeasureC2` (reviewers), `CriticAxisFit` (critic; it replaces the lane's dead seat of that name), `GateEvidence` (reviewer). None executed a lane gate or counter. Everything else below was run by this session. Tool use: pycryptodome 4.1.0 in an ephemeral `uv run --with` environment (uv 0.13.0), for an independent keccak check. Nothing was installed system-wide.

Driver digest (copied from `.ufo/watchdog.log:756,758`):

```
2026-10-22T16:46:20-03:00 launch kaidoku round=29 pgid=619856 driver=hyaku-inline attempt=1
2026-10-22T17:43:19-03:00 complete kaidoku round=29; hyaku-inline attempt=1
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane | `git log --format='%an %H' -- .ufo/reports/round-29/kaidoku.md` (fleet) | `kaidoku-shokunin f9560fa5f8b6e49531d689f7aab5e32ea47dce2c` (17:42:59-03) | pass |
| SHONEN heading, one line per box | read of the report `## SHONEN` | 4 lines, all `[~]`, each with a pointer | pass |
| cited commits on the branch | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> main` for `bacbe9cc dbd87cfa 7431096b 4fcea978 18be864a 2f18996d 33570c3a` | all 7 ok. `git log bacbe9cc..33570c3a`: 6 commits, all `kaidoku-shokunin` | pass |
| pushed | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=main local=33570c3a… remote=33570c3a… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| leftovers | `GIT_OPTIONAL_LOCKS=0 git status --porcelain` | empty | pass (round-28 defect 1 closed) |
| prompt carries the template contract | `grep -nE '^## ' .ufo/prompts/kaidoku-round-29.md` | §1 MISSION/AXES, §2 Claims, §2b Frontier, §3 L2 floor, §4 Report contract, §5 Commit/push, §6 hyaku addendum | pass |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | `kaidoku ok`, six W04 (S033, S047, S054, S062, S069, S083), exit 0 | pass, equal to the report |

Frozen inputs are unchanged since the freeze (GateEvidence). All 12 pinned paths in `claims.json` (`instruments`, `loaded_by_counter`, `producers_not_counters`) hash to their pinned sha256 at `33570c3a`. `git diff --quiet dbd87cfa 33570c3a -- .ufo/waves/round-29/claims.json <12 paths>` gives exit 0. Order by committer time: freeze `dbd87cfa` at 20:03:06Z; earliest REA run in `c1/runs.tsv` at 20:03:21Z; earliest lookup in the manifest at 20:03:39Z; data commit `4fcea978` at 20:09:09Z. Every counted data file is first added in `4fcea978`.

## Per-claim re-check

Both counters are lane-owned gates (PROTOCOL §Gate standard), so this session did not execute them. It verified their committed evidence, and re-measured the counted quantities from the committed bytes at `33570c3a` with independent jq/python.

Committed gate evidence:
- Selftests (`before/` and `after/c1-selftest.txt`): C1 `selftest cases=22 failures=0`, exit 0. The 22nd case is the silent planted-wrong check at `c1-fresh-naming.py:582-585`.
- Selftests (`before/` and `after/c2-selftest.txt`): C2 `selftest cases=19 failures=0`, exit 0.
- Measured revisions: the after receipts name `--rev 2f18996d…`, and C1 is also measured at `18be864a`. The before receipts name `--rev bacbe9cc…` and record `PIN pinned input absent`, exit 2.

### R29-C1 (declared coverage): re-measured, statement holds, axis move not shown

- Inventory: `git ls-tree -r 33570c3a -- corpus/evidence/round-29/c1/` gives 16 carriers, 16 runs and 304 db lookups (152 4byte + 152 openchain). `awk -F'\t' 'NR>1{c[$3]++}' runs.tsv` gives 16 runs, all exit 0. `jq length db/manifest.json` gives 304, all status 200 with tries 1. `heldout.tsv` has 152 data rows and 152 distinct selectors.
- Triple: `jq '.tally.rules.openchain_sole_unfiltered_args_consistent' tally.json` gives `named 122, right 122, wrong 0, no_name 30`.
  - ReMeasureC1 recomputed the rule from the heldout ABI, the envelope-derived REA arguments and the saved openchain lookups, and got the same triple with 0 per-row disagreements.
  - This agrees with the report and with the entry `corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`, whose `source:` line cites S088. S088 is absent at `bacbe9cc` and present at `SOURCES.md:94`.
- Freshness: none of the 152 selectors is in the lane at the base, with or without `0x` (`git grep -i -c -F -e <sel> bacbe9cc` gives 0/152 hits each way). None overlaps round 25's 43 or round 28's 187.
- Discriminating power: `jq '.tally.rules'` shows `openchain_first` at named 152, right 152, wrong 0 (CriticAxisFit). The trivial baseline does at least as well as the primary rule. The frozen target counts completeness only; `w1/CriticTargets.md:69` says "A rule that named nothing, or named everything wrong, would still have met it".
- Unpinned instrument (M29-3): **not material to verification.**
  - The pinned counter (`6ad79d10…`) implements the rule itself (`rule_outputs`, `c1-fresh-naming.py:141-158`). Its only dynamic load is the pinned `tools/round-25/a2/resolve-selectors.py`.
  - The named-but-unpinned `tools/round-28/c1-heldout-naming.py` is not loaded. It is unchanged across the round: `git diff --stat bacbe9cc 33570c3a -- tools/round-28/` is empty, and its only commit, `87d3dfb6`, is an ancestor of the base.
  - An AST diff shows `rule_outputs` identical between the round-28 and round-29 counters (CriticAxisFit). So "unchanged" is true.
  - The flag remains a freeze-hygiene defect (receipt `after/freeze-gates-at-dbd87cfa.txt`, both gates exit 0 with round-29 flagged).
- **Axis ruling (the dead `CriticAxisFit` question): misfit.** AXES.md defines coverage as the fraction of the domain's real surfaces the skill governs. No surface, tool, operation or edge class entered governance this round:
  - The lane's own `PROVINCE.md:95` reads "Frontier status unchanged".
  - The coverage row is unchanged ("Owned axes rows above are unchanged").
  - The REA operation (`inspect_evm_interface`), the two databases and the compiler pin were all held before. `PROVINCE.md:92` lists real solc-0.8.37 carriers.
  - The 16 carriers are author-written stubs, and only n04's list rests on an opened source (S088).
  - What C1 adds is a replication of an already-held rule on new author-picked inputs. That is quality evidence, and the round-28 entry already held a held-out score of the same rule (137/137/0). This matches the round-28 closure's reading that a frontier bullet "annotated, not moved" leaves coverage `unchanged`.
- Verdict: the frozen statement verifies as measured, but as a coverage axis-move it **does not verify** (coverage `unchanged`).

### R29-C2 (depth): re-measured, target met, held-out

- Inventory: `corpus/evidence/round-29/c2/db/` has 178 `openchain-*.json` plus `manifest.json`. All are status 200 with tries 1, `ok:true`, and a sha256 equal to the bytes. Each response has exactly one `result.function` key. `selectors.tsv` has 178 data rows: canonical 26 and c1 152.
- Independent rule check (ReMeasureC2's own python, not the lane counter): `entries=252 pred_true=38 pred_false=214 mismatches=0`.
  - The canonical subset gives 53 entries (38 true, 15 false, 0 mismatches). The c1 subset gives 199 entries (all predicted false, 0 mismatches).
  - Four keys returned no candidates, as the entry states.
  - This agrees with `after/c2-at-2f18996d.txt` and with the entry `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md` ("mismatches 0 of 252 entries"; `source:` cites S087).
- Unseen: none of the 178 has an openchain response anywhere at `bacbe9cc`, while the 10 excluded keys each do (10/10). The 26 kept keys are the 36 pinned keys minus those 10. The pins are `canonical-signatures.json` `5572beb5…` and `selectors.tsv` `3a93f783…`.
- Separation: on the same 252 entries, the rival rule "filtered = selector is a canonical key" gives 15 mismatches, and "filtered always false" gives 38. The test could have failed and distinguishes the sourced rule from both rivals.
- Axis ruling: **fit.** A mechanism read from opened code (S084/S087 `filterResponse`) predicts a live flag on never-fetched selectors, and the bar can fail. Depth is tied lowest at 10, so the lowest-axis obligation is met (`SCORECARD.md:23-25`; no axis retired; the stagnation waiver does not apply because a capability entered in round 27).
- Separable from C1: yes. C2's counter reads only `corpus/evidence/round-29/c2` (`c2-filtered-unseen.py:53,150-153`). The shared 152 selectors are a frozen input, not a C1 result.
- Verdict: **verifies**. It supersedes the round-28 re-observation with a held-out test.

### Harm check

- `git diff --stat bacbe9cc 33570c3a`: 657 files, `+19790 -34`.
- Deletions occur only in `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md` (the settled seat report), `corpus/claim-freezes.tsv` (−3: disclosed ledger corrections of the round-26 and round-28 rows) and `tools/round-27/c2-xpin-check.py` (−15, confined to `selftest()`).
- `SCORECARD.md` (+34, a new round-29 section only), `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `LOG.md` and `corpus/knowledge/` have zero deleted lines.
- No owned axis is harmed.

| axis | verdict | reason |
|---|---|---|
| coverage | unchanged | C1 measures replication on new inputs; no surface moved (`PROVINCE.md:95` "Frontier status unchanged") |
| depth | improved | C2 held-out, re-measured 0/252 mismatches, rivals fail |
| calibration | unchanged | not claimed; limits disclosed, but the C1 axis label overreached |
| operability | unchanged | not claimed; the round-27 selftest returns to green (defect repair) |
| freshness | unchanged | not claimed; S084 re-opened at staging as S087, bytes identical |
| adjacency | unchanged | not claimed |

Admission: C1 does not verify as an axis-move, so `admitted=false`. With no axis harmed, the verdict is `rejected-honest-stop`. The lane hit every frozen number. The rejection rests on the axis fit, not on a missed target.

## Discernment spot-check

All re-opens were run at 20:45Z on 2026-10-22 with `curl -sSL <url> | sha256sum`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S087 Sourcify `handlers.ts` + `canonical-signatures.json` @ `0966a3bc` | admit | the S087 URLs; `sed -n '39p;47,48p;66p'`; `git ls-remote` gives HEAD = staging = `0966a3bc`, master = `189cd726` | agree | sha256 values `30981efb…6c5a38` and `5572beb5…78b3e2` equal the Gate row. `:39` opens `filterResponse`, `:47-48` read `signatureItem.filtered =` / `signatureItem.name !== expectedCanonical.signature;`, and `:66` closes it |
| S088 ERC-4626 text @ `3c0f7076` | admit | the S088 URL; `sed -n 18p` | agree | sha256 `698c05bf…51e10a` equals the row. `:18` is the quoted Abstract sentence. ERCs master has since moved to `6b7a48ff`, but the pinned commit still serves identical bytes |
| master copies of `handlers.ts` / canonical list | reject (not made rows) | `…/sourcify/189cd726/services/4byte/src/api/handlers.ts` | agree | sha256 `30981efb…` is byte-identical to S087 and to S084, so a row would duplicate S084 |
| the other 15 carrier interface lists | reject (not opened, not rows) | `git show 33570c3a:corpus/SOURCES.md` search log `:167` | agree | Contract v1 forbids a row for an unopened source. Consequence: 15 of 16 C1 carriers have no opened provenance (routed below) |
| Gate note: 6 of 31 kept signatures mis-keyed | finding | my keccak over the S087 bytes (`uv run --with pycryptodome`) | agree | `keys=36 kept=31 none=5 nohash_match=6`, equal to `after/canonical-keyhash.txt` |

New `corpus/SOURCES.md` rows re-opened: S087 and S088. Both quotes are contiguous served bytes and within the 25-word limit. S087's is 5 words over two consecutive lines `:47-48`. S088's is 15 words at `:18`.

## Trend verdicts

- **expansion: unprovable-but-better.**
  - Knowledge files went 112 → 114, and SOURCES rows went 86 → 88 (`grep -cE '^\| S[0-9]{3,} \|'` at `bacbe9cc` and `33570c3a`).
  - Both new rows re-opened with matching hashes. S088 is a new kind of source for carrier provenance (standards text).
  - But both entries sit on ground the lane already held (the round-25 rule, the round-28 held-out score, the round-28 `filtered` entry), and the frontier did not move.
- **quality: improved.**
  - C2's held-out test supersedes round 28's re-observation (stronger replaces weaker; re-measured).
  - The round-25 rule re-verifies on 152 fresh selectors (122/122/0, recomputed).
  - The mis-keyed-list finding re-checks independently.
  - The round-27 instrument went red → green with the change confined to `selftest()`.
  - Round-28 routed defects 1–6 are all closed (GateEvidence).
  - No admitted entry failed its re-check.
- **discernment: unprovable-but-better.**
  - All four sampled gate decisions agree on re-opening, and the wave caught real overreach before filing.
  - The lane's own claim-level self-assessment still labelled a replication as a coverage move (and reported expansion `improved`), which this outside check disagrees with.
  - That disagreement is not yet a lesson or a `QUALITY.md` criterion.

## Routed defects (lane must fix next round)

1. C1 axis misfit. A re-score of an already-held rule on new author-built inputs is not a coverage move. Mine this as a lesson with a grounded `QUALITY.md` criterion. A future coverage claim must move a surface (frontier → core, or a new tool/operation/edge class) under a bar that can fail.
2. The C1 target cannot fail on rule quality: `openchain_first` scored 152/152/0. Any further held-out naming test needs a target that both a rule naming nothing and the trivial baseline fail.
3. M29-3 is open. The round-29 freeze file names `tools/round-28/c1-heldout-naming.py` unpinned, and both freeze gates flag round 29. Record a supersession or pin note under `instrument_supersessions`, and make the run-before-freeze step an exit-code check rather than a procedure.
4. M29-1's fix (the seat-settled condition) is still not shown able to fail, and no tool enforces it.
5. 15 of 16 C1 carriers have unopened interface provenance; only n04 rests on S088. Open those sources, or stop calling the lists "published" in the entry and PROVINCE.
6. The S085 teaches-cell error (11 of 36 keys) is corrected in `corpus/lessons/round-29.md:40` and in the pointer at `corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md:94` (`git grep -n 'signature it keeps' 33570c3a`). `SCORECARD.md:3166` (round-28 section) still says the cell "covers 31 of 36 keys" and omits the 6 mis-keyed signatures. Append a named correction (append-only, §Evidence standard "Corrections sweep every mention").
7. The `c1-fresh-naming.py` docstring (`:14`, `:27`) still names round-28 paths. This affects readability only; fix it with any future counter revision.

Operator note: all four SHONEN boxes are `[~]` with concrete pointers. The executable-instructions box rests on author-dispatched seats, so this session did not judge any box fully checkable by a non-author. Promotion stays operator-owned.
