# R50 carry-over checklist — attempt 1 "Not landed" → attempt 2

Seat `ExecErrataSweep`, wave 3 (build). Base `f890bbead20ca2c549487167f56876ae47f1e1a4`;
lane tip observed during this seat: `03f852b9629cd21e593a8b73ccd7aa3e63f6bdea`.

Source of the list: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kaidoku.md`
(fleet repo, read-only) line 27 ("**Not landed:** …"), cross-read with
`corpus/lessons/round-50.md:50` ("Not landed (restored or never written)") and
`LOG.md:3471`. Plan audited:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-50-attempt2-claims.md`
(sections R50-C1, R50-C3, "Landing order and shared-file rules", "Frontier step",
"Round shape").

Legend: **YES** = the attempt-2 plan names the item and a wave-3 seat or an L1 step
owns it; **PARTIAL** = named but not fully owned / owned by a seat that only drafts;
**NO** = not named anywhere in the attempt-2 plan.

---

## A. Item-by-item verdict

| # | Attempt-1 not-landed item | Attempt-2 plan addresses it? | Owner (wave-3 seat / L1 step) | Verdict + evidence |
|---|---|---|---|---|
| A1 | **C1 knowledge entry** (`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`) | **YES** | seat `ScribeEntryC1` (draft) → L1 landing step 3 of "Landing order" | Plan step 3 names the entry path verbatim, pinned to the frozen counter's `ENTRY`/`STEM` (`tools/round-50/c1-counter.py:377-378`). Draft exists: `.ufo/waves/round-50/w3/ScribeEntryC1/entry-draft.md`, header pins the same stem, 4 `source:` lines (S243/S244/S245/S249) + `verified-at:` + `recheck:`. **Risk (P1):** the dispatch spec `w3-spec.json` still carries the OLD stem `2026-10-29-r50-le-avm-hsqs-core` in 6 seat prompts (ScribeEntryC1, ScribeRowsSources, ScribeProvinceBinding, ScribeReadmeMap, RevEntryBar, ConnCrossClaim) — the spec was generated 17:30:16, the correcting commit `6f4aba63` landed 17:32:55. The counter reads the stem from `c1-counter.py`, so the landed text must use the frozen stem; the drafts audited already do, but the LOG draft does not (see P2). |
| A2 | **PROVINCE binding** (`## Round-50 additions to Core` + frontier note) | **YES** | seat `ScribeProvinceBinding` → L1 landing step 3 | Plan step 3 names the section and the `Round-50 frontier note` mark. Draft `.ufo/waves/round-50/w3/ScribeProvinceBinding/province.md` uses the frozen stem and cites `c1-counter.py:377-378`; the seat also ships `check-bindings.py` that replays the binding checks. Frozen counter's `province_core_row` needs the row's first cell to match `squashfs_v4_le` **and** the row text to contain `AVM marker` **and** the entry path — the draft row carries all three. |
| A3 | **corpus/README.md coverage-map row** | **YES** | seat `ScribeReadmeMap` → L1 landing step 3 | Plan step 3 names the coverage-map row. Draft `.ufo/waves/round-50/w3/ScribeReadmeMap/readme.md` + `readme.appendonly.diff` + `readme.primary.diff` (both variants prepared) + `patch_readme.py`. `coverage_map_row` needs a `|`-line inside `## Coverage map` carrying the stem — the diff carries it. |
| A4 | **SCORECARD capability row + Owned-axes coverage head `140/140`** | **YES** | seat `ScribeCapabilityRow` (draft) → L1 landing step 3; cross-checked by `ExecB1Impact` + `CritB1Text` | Plan step 3 names both. `ExecB1Impact` produced `mklanding.py`; `CritB1Text` produced `receipts.md` — both are wave-3 attack seats on the `140/140` head text, which is what B1 reads. |
| A5 | **SKILL.md bindings** (attempt-1 report lists "SKILL" among the not-landed C1 bindings) | **NO / re-scoped** | attempt-2 routes SKILL.md to **C3 only** (rule block 22 + registry row) | The C1 counter binds **no** SKILL.md path: `grep -n SKILL tools/round-50/c1-counter.py` → 0 hits; `BINDINGS` (`c1-counter.py:432-434`) = `province_core_section, province_core_row, frontier_note, entry_present, sourced, coverage_map_row, carriers_spec_ok, gap_rule_ok, frozen_tables_valid` — no SKILL. The attempt-1 report's "SKILL bindings" therefore refers to the C1 *documentation* surface it named in the frozen plan (`plans/round-50-claims.md:124-131` lists PROVINCE/README/entry/SOURCES only) plus the registry rows — and the attempt-1 landing commit `11ccdb72` **did** land the 12 `instrument-registry v2` rows for `tools/round-49/**` and `tools/round-50/**` (SKILL.md:1762-1773). What attempt-1's wave-1 seat `C1LandingMap` finding 14 flags as a real SKILL-side defect is the stale live-limits block at `SKILL.md:1607` ("Big-endian and AVM SquashFS … are not claimed"), which a C1 promotion contradicts. **That specific fix is NOT in the attempt-2 plan** (grep `1601`/`limits` in the plan → 0 hits). Carried to the L1 as an open item below. |
| A6 | **SOURCES rows S243, S244, S245, S249** | **YES** | seats `ScribeRowsSources` (draft) + `SrcReopenFreetz`/`SrcReopenAvmIndex`/`SrcReopenUnblob`/`SrcReopenLicence` (re-open receipts) + `CritSourcingRules` (attack) → L1 landing step 3 + "Frontier step" | Plan step 3 names the four ids and the `opened 2026-10-28 / re-opened 2026-10-29` split. Ids are **free** in the live registry (ids present = S001-S149 + S246-S248; `grep -c '^| S243 |' corpus/SOURCES.md` = 0, same for S244/S245/S249). Draft `ScribeRowsSources/rows.md` carries 6 × the frozen-stem `used-by` cell (`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`) — required by the frozen `sourced` binding (`c1-counter.py:2475`: `ENTRY in used or STEM in used`). **One open decision for the L1 (not an id collision):** the plan's "Frontier step" says "staged S206 re-grounded as S243", and I verified the staged row `S206` in `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md:107` is the **same source** as the planned S243 (Freetz patch 101, same URL) but with a different **tier**: staged `A`, planned `B` (`rows.md`), and the wave-1 draft `w1/C1SrcFreetz/S150-registry-row-draft.md` also says tier B. The id re-grounding is therefore consistent — but the **tier change A→B** is a substantive difference the L1 must settle explicitly (the staged row was refused in attempt 1; `CritSourcingRules` was asked to check "is tier B right for a distro patch file (S243)?"). |
| A7 | **SHONEN promotion** (attempt-1's SHONEN section: all four boxes still `[ ]` unchecked) | **NO** | nobody | The attempt-2 plan does not mention SHONEN at all (`grep -ci shonen plans/round-50-attempt2-claims.md` = 0) and no wave-3 seat owns it (`grep -l SHONEN .ufo/waves/round-50/w3-spec.json` → only this seat's own prompt). **Also note the report is wrong about the file:** `SHONEN.md` in the lane has all four boxes as `- [~]` (`SHONEN.md:5,8,11,14`), while the fleet report prints them as `- [ ]`. So attempt-1 did not "leave the boxes unchecked" — they were already `[~]` and remain `[~]`. A `[~]`→`[x]` promotion needs a non-author verifier; the lane's own rule (`SHONEN.md` round-49 note: "no box moves to `[x]`" without one) means attempt-2 cannot promote. **Verdict: not carried over, and correctly so — but the L1 must not report SHONEN as "promoted" or as "regressed".** |
| A8 | **wave-2 seats** (attempt-1: wave 2 generated + validated, never dispatched, 37 seats, round total 38 < 64-seat floor) | **YES (replaced)** | wave-3 = 35 seats (this wave) + wave-4 (falsify) per the attempt-2 plan's "Round shape" | Plan: "Two v1 waves (policy `ufo-wave-policy.json`, band 32–64 each), round total 64–128: w3 build (~40 seats…) and w4 falsify (~36 seats…)". Actual wave-3 = **35 seats** (`w3-spec.json` 35 items; `w3-dispatch.json` `counts.spawn 35`), role mix `executor 10, scribe 7, scout 5, critic 4, reviewer 4, connector 2, mutation-tester 1, revenger 1, sentinel 1` → attack roles (critic+reviewer+mutation-tester+revenger+sentinel) 11/35 = **31.4%**, above the 25% floor attempt-1 missed. Attempt-1's wave-2 specs are **not preserved anywhere** (`git log --all --name-only | grep -c 'round-50.*w2'` → 0; no `w2-spec.json`/`w2-dispatch.json` for round-50 in the tree or history) — that content is unrecoverable, so "attempt-2 replaces wave 2" is the only available disposition. |
| A9 | **QUALITY row 94 dropped** (attempt-1 landed rows 90-93; row 94 was "optional, for the L1 to keep or drop" per `w1/C2QualityDraft/draft-quality-rows.md`) | **NO** | nobody (draft survives at `.ufo/waves/round-50/w1/C2QualityDraft/draft-quality-rows.md`, committed) | The attempt-2 plan does not mention QUALITY at all (`grep -c QUALITY plans/round-50-attempt2-claims.md` = 0) and no wave-3 seat owns landing a QUALITY row (`CritSourcingRules` and `RevEntryBar` only *cite* QUALITY rows as criteria). The **draft text is preserved and committed** (`git ls-tree … C2QualityDraft/` → `draft-quality-rows.md`, `receipts.txt`, `tools/round-50/c2q-probe.py`), so the row is one append away and its instrument (`c2q-probe.py`, with 8 red/green arms) is already green-checked. Live `corpus/QUALITY.md` ends at row 93 (`grep -oE '^\| [0-9]+ \|' corpus/QUALITY.md | sort -n | tail -1` → 93), so 94 is still the next free number. |
| A10 | **six wave-1 receipt files over 1 MiB skipped by the helper** (`w1/C1GapRule/census/a7530.{lls,oracle.tsv}`, `w1/C1OracleBuild/a7530\|a7590/oracle.tsv`, `w1/C1RevLayout/receipts/a7530.{auto,le}.files.tsv`) | **NO** (and the attempt-1 characterisation is wrong) | nobody | Attempt-1's report says "their content is the frozen oracle tables under `tools/round-50/oracle/`". **That is false for these six**: all six are `a7530`/`a7590` — the two carriers **dropped** before the freeze (7530/7590 were swapped out for 7581/7582; see `plans/round-50-claims.md` "Carrier swap, before the freeze"). The frozen oracle dir holds only the four kept carriers: `git ls-tree … tools/round-50/oracle/` → `c6430.*`, `c6490.*`, `g7581.*`, `g7582.*` — no `a7530`/`a7590` table exists. The six files are **absent from disk and from git history** (`git log --all --oneline -- <path>` = 0 commits each; `ls` → ABSENT). For the four kept carriers the wave-1 census copies **are** committed and byte-identical to the frozen tables (`sha256sum tools/round-50/oracle/c6430.oracle.tsv` = `f657ef51…b5165` = `w1/C1GapRule/census/c6430.oracle.tsv` = `w1/C1OracleBuild/c6430/oracle.tsv`). So the loss is the a7530/a7590 census/oracle detail, which the claim does not depend on. No wave-1 file over 1 MiB was committed (`git ls-tree -r --long … w1/ | awk '$4>1048576' | wc -l` → 0; largest committed = 904 638 B `unsq-l-a7530.txt`), so the ">1 MiB" filter behaved as described — it just dropped **dropped-carrier** detail, not the frozen tables. |
| A11 | **the attempt-1 report's own control-status wording** (`could_not_evaluate` vs the receipt's `misbehaved`) | see §B | L1's own controls run | Not a "not-landed" item, but the attempt-2 controls run must be read against the receipt truth, not the report prose. See §B below. |

---

## B. Controls tabulation — attempt 1 (`controls-attempt1/`), and what attempt 2 must re-score

Read from `.ufo/waves/round-50/controls-attempt1/` (committed at `8ccc05e6…`). Machine
source of truth = `summary.json` (sha256 `45bfa9f29fa8fbb117156ee078a5fdf008b1446af93dd8106dc17b8207946348`)
and the six `receipt.json` / `counter.json` pairs. **The attempt-1 fleet report and
`corpus/lessons/round-50.md:47` describe CTL-C1-2/-3/-4/POS as "`could_not_evaluate`".
The receipts say `verdict: "misbehaved"` with `why: "counter reported could-not-evaluate
(exit 2)"` — the driver never set the `could_not_evaluate` status field.** The
distinction matters: `c1-controls.py` only assigns `status: could_not_evaluate` when
the counter's receipt still contains `carriers` (so `rerun_errors` is derivable);
on an exit-2 `rerun_env_error` the counter writes a receipt with **no** `carriers`
key, so `summarize()` returns `present: False` and the driver's `dependent` branch
(`c1-controls.py:1554-1567`) is never reached. The control is then judged by
`judge()` → exit 2 with no `accept_refusal` → `misbehaved`.

**Verbatim per control (attempt 1):**

| control | receipt dir | exit | verdict (receipt) | `summary.json` verdict | carriers_matched | stdout_sha256 | counter `reason` | counter `unevaluable` (exact text) | wall_s | utc |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-C1-0 (do-nothing at the freeze) | `c0/` | 1 | `as_expected` | `as_expected` | 0 | `6d7f383453d0c84b2170c1c3625cbf29164e98eba0f40b9ac42c7098a082efc2` | — | — | 8.05 | 2026-10-29T01:41:17Z |
| CTL-C1-1 (round-41 BE receipts in the LE slots) | `c1/` | 1 | `as_expected` | `as_expected` | 0 | `cfa58b34fa299b34547fb2ad2ff57b5b2c78ce43789bed80d6f20535431ae765` | — | — | 546.829 | 2026-10-29T01:50:38Z |
| CTL-C1-2 (oracle-only fabrication, re-minted evidence id) | `c2/` | 2 | `misbehaved` | `misbehaved` | null | `50f279f48f9f35fe2fccdaf5194e004bf1a1c177f7098c28c71d9935b3eb4c6c` | `rerun_env_error` | `REA provider_timeout on c6490 after 3 attempt(s); repeat on a quieter host` | 611.485 | 2026-10-29T02:01:13Z |
| CTL-C1-3 (sasquatch absent → missing extractor) | `c3/` | 2 | `misbehaved` | `misbehaved` | null | `107d32bb1042bc242dff194758717b008b48b6dc06dc63a3f8f75454c9050421` | `rerun_env_error` | `REA provider_timeout on g7581 after 3 attempt(s); repeat on a quieter host` | 381.369 | 2026-10-29T02:07:46Z |
| CTL-C1-4 (standard LE carrier with a genuine receipt) | `c4/` | 2 | `misbehaved` | `misbehaved` | null | `50f279f48f9f35fe2fccdaf5194e004bf1a1c177f7098c28c71d9935b3eb4c6c` | `rerun_env_error` | `REA provider_timeout on c6490 after 3 attempt(s); repeat on a quieter host` | 759.219 | 2026-10-29T02:20:41Z |
| CTL-C1-POS (real receipts + landing blocks) | `pos/` | 2 | `misbehaved` | `misbehaved` | null | `107d32bb1042bc242dff194758717b008b48b6dc06dc63a3f8f75454c9050421` | `rerun_env_error` | `REA provider_timeout on g7581 after 3 attempt(s); repeat on a quieter host` | 372.311 | 2026-10-29T02:27:03Z |

`summary.json` aggregate: `controls: 6`, `failures: ["CTL-C1-2","CTL-C1-3","CTL-C1-4","CTL-C1-POS"]`,
`unevaluated: []`, `kill_rule_fires: false`, `kill_rule_detail: []`, `fixtures_verified_against_freeze: 21`,
`counter_sha256: 9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`.
`score.out.txt` (sha256 `b7e4249d86a37ff828d6d76102b7f9f743467775bffa019bbe1895d07e425b30`) printed
`{"controls": 6, "failures": [...], "kill_rule_fires": false, "unevaluated": []}` and **exit 1**.

Two controls (c2, c4) share stdout_sha256 `50f279f4…` and two (c3, pos) share `107d32bb…`:
their stdout is the same one-line `{"detail": …, "frozen_path_changed": [], "reason": "rerun_env_error"}`.
The **timeout carrier differs** (c6490 for c2/c4, g7581 for c3/pos) — so it is not one
stuck carrier, it is host load.

**What attempt-2's controls run must re-score:** CTL-C1-2, CTL-C1-3, CTL-C1-4, CTL-C1-POS.
All four failed for an environmental reason (REA's own fixed 120 s `provider_timeout`
after 3 attempts), **not** because the counter misbehaved — the counter's `reason` field
says `rerun_env_error` and `frozen_path_changed: []`, i.e. nothing about the frozen
bytes moved. `kill_rule_fires` was false and stays false: none of the four reached
`carriers_matched == 4` with every binding true, and CTL-C1-0's `diag.receipt_clauses_green`
was `{}` (no carrier clause scored green on the do-nothing tree). The attempt-2 run must
therefore re-score those four and expect `as_expected` **only if the REA rerun actually
ran**; a fourth `provider_timeout` is again exit 2, and the attempt-1 report/lesson/LOG
wording "`could_not_evaluate`" must not be repeated as a driver status it never had.

---

## C. Items the attempt-1 report did NOT list, found by this sweep (carried to the L1)

| # | Finding | Why it matters | Owner |
|---|---|---|---|
| C1 | **The frozen `tools/round-50/gap-rule.json` cannot admit the 7581/7582 carriers' device nodes.** The rule sets `required["char-device"] = true`, `allowed["char-device"] = ["unpublished-entry"]`, and `removed.silent["char-device"] = ["247:0"]`. The kept carriers' frozen non-regular tables hold **13** char-devices each for g7581/g7582 (`dev/led 247:0`, `dev/pts/0..7 136:0..136:7`, `dev/tiatm 230:0`, `dev/ttyp0..2 3:0..3:2`) versus **one** for c6430/c6490 (`dev/led 247:0`). Only `247:0` is silent; the other 12 carry **no** `unpublished-entry` gap (unblob cannot create a device node unprivileged and reports none) and are not removals → `disposition_check` returns "required entry with no disposition" → `gaps_ok` False → `carriers_matched` caps at **2 of 4**. The wave-1 seat that wrote the rule said so itself: `w1/C1GapRule.md:66` "Only c6430 and a7530 censused (task cap) … any `b`/`p`/`s` row or **a second device major:minor needs a rule edit before the freeze**" — and no seat ever re-censused g7581/g7582 before the freeze. The rule is **byte-frozen** (`tools/round-50/`), so under the plan's own discipline this is a **miss, not a patch** ("a counter bug found after the freeze is reported as a miss, never patched", `plans/round-50-claims.md` header). | The claim's target `carriers_matched == 4` is **unreachable** with the frozen bytes and the four kept carriers. | L1 decision (new freeze vs. reported miss) — see the report for the reproduction |
| C2 | **`SKILL.md:1607`'s live-limits line still contradicts a C1 Core promotion** ("Big-endian and AVM SquashFS … are not claimed"). Flagged by `w1/C1LandingMap.md` finding 14 as "annotate/supersede in the round-50 landing or the entry"; **not** in the attempt-2 plan. | The lane would claim Core for LE AVM while its own limits block denies it. | L1 (step 3, alongside A2) |
| C3 | **The wave-3 dispatch spec (`w3-spec.json`, `w3-dispatch.json`, `w3.ready`) was generated at 17:30:16, before the L1's two plan commits** (`6f4aba63` 17:32:55 stem fix; `03f852b9` 17:38:32 C3 path move). Six seats' prompts still name the old entry stem; three still name the old C3 instrument path. | Sibling drafts must not be integrated verbatim. | L1 (re-check every draft's stem/path before integration) |
| C4 | **The attempt-2 plan names the C3 instrument at `tools/round-50/sqfs-triage-v5.py` in the C3 section but the L1's `03f852b9` moved it to `tools/round-50-c3/`** — and the *built* instrument (`w3/ExecTriageV5/tools/round-50/sqfs-triage-v5.py`, 88 704 B, `INSTRUMENT_RELPATH = 'tools/round-50/sqfs-triage-v5.py'`) still carries the old path. | The freeze commit must land it at the path the plan now names, or the plan and the file disagree. | L1 + `ExecTriageV5` |
| C5 | The attempt-1 report's "load 95-176" is **not backed by any receipt in the lane**: `grep -rn "load\|uptime\|nproc" controls-attempt1/` → 0 hits; the only load evidence is `l1/dev-arm-timeouts.txt` ("load average 42.5-54"). The figure appears only in prose (`corpus/lessons/round-50.md:47`, `LOG.md:3471`, the attempt-2 plan, the w3 spec). | The quiet-window decision rests on an unsourced number; the attempt-2 controls run should record load with the receipts. | `ScoutQuietWindow` + L1 |

---

## D. Attempt-2 controls (already run by the L1 in this wave) — observed, for the L1's file

Observed on disk at `.ufo/waves/round-50/controls-attempt2/` + `controls-attempt2.json`
(untracked; written 17:34–17:43 local). The four attempt-1 failures were re-scored and
**all four now behave as planned**; CTL-C1-POS does not.

| control | exit | verdict | carriers_matched | why |
|---|---|---|---|---|
| CTL-C1-0 | 1 | `as_expected` | 0 | behaved as the plan states |
| CTL-C1-1 | 1 | `as_expected` | 0 | behaved as the plan states |
| CTL-C1-2 | 1 | `as_expected` | 0 | behaved as the plan states (failing: `projection_ok` on all four slots) |
| CTL-C1-3 | 1 | `as_expected` | 0 | behaved as the plan states (slot `g7581` fails `chunks`, `hits`) |
| CTL-C1-4 | 1 | `as_expected` | 2 | behaved as the plan states (slot `g7581` fails `layout_ok` **only**, as `slot_fails_exactly` demands) |
| CTL-C1-POS | 1 | **`misbehaved`** | 2 | "expected exit 0, got 1" — every documentation binding is **true** (`bindings_false: []`, `entry_present: true`, `sourced: true`, `coverage_map_row: true`, `province_core_row: true`), but `failing: ["g7581:gaps_ok","g7582:gaps_ok"]` → `carriers_matched 2` of `target 4` |

**The POS failure is the C1 finding (C1 above), reproduced by the L1's own run**: the two
7581/7582 carriers fail `gaps_ok` under the frozen gap rule, so the positive control
cannot reach exit 0. `kill_rule_fires` is `false` (no control reached the target), so the
kill rule does not fire — but the C1 **target of 4 is not reachable** without a new
freeze. A live data run already exists for all four carriers
(`corpus/evidence/round-50/c1/{g7581,g7582,c6490,c6430}/after.json` + `run.json`, written
17:51–17:52), and the same two carriers fail `gaps_ok` there.
