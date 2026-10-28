# R44C2Plan — planned-vs-actual census over SCORECARD.md `## Round <N>` sections

**Seat:** `R44C2Plan` (scout, wave 1, read-only). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Census revision `9a8de923053978342fdba6ce047e1cca4eda9dd2`; `SCORECARD.md` sha256
`13a3c621f76a03cd3be1dcbac4ddcb2ba4d68dfbfc87dcf2d399e48f7d4576a7` — byte-identical to its
blob at round base `c29360e3ba5381a5ab69e372d0d9577970f85018` (base is an ancestor; zero
post-base commits touch SCORECARD.md).

Companion machine-readable data: `.ufo/waves/round-44/w1/R44C2Plan.json`.

## Rule applied (from seat spec)

For each `## Round <N>` section, extract its `planned (round <N+1>)` row text and compare
against what round N+1 actually worked (its `## Round N+1` heading + claim table). A plan row
is flagged **mismatch** iff the promised work was NOT done in N+1 **and** the row carries no
`(after a steer)` / `superseded` / `historical` marker.

## Headline

- Numbered `## Round <N>` sections: **31** (Rounds 14–43; no `## Round 37` section exists —
  the only numbering gap).
- Plan rows found: **16** (list items starting `- planned…` / `- **planned…**`).
- Sections with no plan row: **17**.
- **Mismatches (dangling plans): 2** — rounds 29 and 30.
- In-flight / not evaluable: 1 (the `planned (round 44)` row, target section not yet written).

## Mismatch rows (dangling plans — candidate C2 rubric entries)

| Round | Line | Planned (round N+1) text | Actual N+1 | Evidence |
|---|---|---|---|---|
| 29 | :3213 | `coverage or depth — a blind naming test: interface lists drawn by a rule the L1 does not control … with name strings screened …; add the missing selftest cases from the round-29 mutation survivors and a selftest for tools/round-29/freeze-gate.py before its next use. Second choice: calibration on the 11 SCORECARD statements disclosed in round 26.` | Round 30 worked `inspect-rust-binary` positive class (coverage) + refusal signatures predicted from code (depth). No blind naming test; no EVM/naming content in any section after :3300. | `grep rust-binary/EVM/naming` on sections 31–43: no later resumption. `tools/round-29/freeze-gate.py` contains **no** selftest code (0 matches for `selftest`) and its last commit is `7431096b` (round 29) — the "before its next use" selftest was never added. No marker on the row → **dangling**. |
| 30 | :3250 | `depth or coverage — inspect-rust-binary refusal signatures on PE and Mach-O containers (section-table edits) and the 256 MiB/8 MiB bounds, with a counter that compares the full refusal envelope (M30-3) and distinct-branch mutants …; second choice: calibration on the lane's SHONEN/SCORECARD pointer set with axis-fit-gate.py run before data.` | Round 31 worked `inspect-sqlite-database` schema + refusals instead (anti-loop steer). The rust-binary PE/Mach-O refusal work never resumed in rounds 32–43. The second-choice SHONEN/SCORECARD calibration was also not run as a claim. | `grep 'rust-binary' SCORECARD.md` after :3253 → nothing. No marker on the row → **dangling**. |

## Full census

| Section (start line) | planned row | target | marker / exempt | fulfillment | mismatch? |
|---|---|---|---|---|---|
| Round 14 (:2188) — … | — | — | — | no plan row in section | — |
| Rounds 15–24 (:2246–:2947) | — | — | — | no plan rows | — |
| `## Round 25 — prospective explicit-reference custody` (:2948) | — | — | — | no plan row | — |
| `## Round 25 attempt 3` (:3057) | :3072 | 26 | none | **done** — R26-C1 depth evidence-id identity table (disclosed INSTRUMENT_ABSENT ordering deviation) | False |
| Round 26 (:3075) | :3092 | 27 | none | **done** — R27-C1 renamed-copy + second-carrier table | False |
| Round 27 (:3100) | :3131 | 28 | superseded by :3138 | superseded in-section (CriticPlanned) | False (exempt) |
| Round 27 (:3100) | :3138 | 28 | `(supersedes the planned field…)` | **done** — R28-C1 held-out test of the r25 naming rule (honest stop 60/61) | False |
| Round 28 (:3143) | — | — | — | no plan row | — |
| Round 29 (:3181) | :3213 | 30 | none | **not done in any round** | **True** |
| Round 30 (:3216) | :3250 | 31 | none | **not done in any round** | **True** |
| Round 31 (:3253) | — | — | — | no plan row | — |
| Round 32 (:3279) | :3306 | 33 | `(only after a new steer)` | calibration repertoire assessment not done in r33 (r33 worked depth CHPE) | False (exempt) |
| Round 33 (:3308) | :3322 | 34 | `(only after a new steer)` | r34 worked another admissible frontier (GNU version-needs); guard held | False (exempt) |
| `## Round 34` (:3328) | — | — | — | no plan row (plan lives in the run-6 re-dispatch section) | — |
| `## Round 34, run-6 re-dispatch` (:3352) | :3374 | 35 | `(round 35, after a steer)` | primary not done; second choice partially attempted (R35-C2 closed D1–D4 of six, unprovable) | False (exempt) |
| Round 35 (:3378) | — | — | — | no plan row | — |
| Round 36 (:3389) | :3400 | 37 | none | **done in next existing section** — no Round 37 section; Round 38 worked BE SquashFS v4 (honest stop) | False |
| Round 38 (:3403) | :3414 | 39 | none | **done** — R39-C1 standard BE v4 promoted, symlink rule stated before data | False |
| Round 39 (:3417) | :3434 | 40 | `(round 40, after a steer)` | **done** — R40-C2 triage v2 w/ domain guard; C1 rerun clause added | False (exempt) |
| Round 40 (:3437) | :3452 | 41 | `(round 41, after a steer)` | **done** — R41-C1 AVM-BE → Core, exact-path counter | False (exempt) |
| Round 41 (:3455) | :3466 | 42 | `(round 42, after a steer)` | **done** — R42-C2 refrozen w/ shared declared-tuple key + dev-arm dry run | False (exempt) |
| Round 42 (:3469) | — | — | — | **no plan row in its own section** (the `planned (round 43)` line is inside the Round 43 section at :3498) | — |
| Round 43 (:3487) | :3498 | 43 | `(round 43, after a steer)`; declared **historical** by erratum :3509 | **done** — R43-C1 met 78/78; R42-CL2 wave-2 attack discharged via w1 R43C1Regress + w2 falsification wave (plan:18) | False (exempt) |
| Round 43 (:3487) | :3507 | 44 | `(round 44, after steer)` | target round in flight — **not evaluable** | — |

## Receipt

| seat | command | exit | stdout sha256 | wall |
|---|---|---|---|---|
| R44C2Plan | `python3 -I -B /fast/scratch/hyaku/kaidoku-r44/probe-r44c2plan/planned-vs-actual.py > R44C2Plan.json` | 0 | `cb7bb214c41887fdf59b05052d261b48f17136265f6bf47f16f0765d4304a4d5` | 21.5 ms |

Auxiliary checks (all exit 0): `git show c29360e3:SCORECARD.md | sha256sum` →
`13a3c621f7…` (equals worktree); `merge-base --is-ancestor c29360e3 9a8de923` → true;
`grep selftest tools/round-29/freeze-gate.py` → 0 matches; round-43 w2-spec task scan for
`round-42|R42` → only `R43W2C1C02` (re-opens committed r42 C02 records).

## Unresolved / method notes

1. **Orphaned round-42 plan**: the `## Round 42` section has no `planned` row; the
   `planned (round 43)` line sits inside `## Round 43` (:3498) and the :3509 erratum calls it
   "historical". Attributed to section 43 in the JSON; fulfillment recorded against round 43
   anyway (done, exempt).
2. **Duplicate section numbers**: `## Round 25` / `## Round 25 attempt 3` and `## Round 34` /
   `## Round 34, run-6 re-dispatch` are separate sections; plan rows live in the "attempt 3"
   and "run-6" variants only.
3. **Sub-clause spot checks**: `bind member_sha256 in fetch-vendor.py` (r41 plan sub-clause)
   and the freeze-gate "before its next use" selftest were grep-checked where cheap
   (freeze-gate: dormant, no selftest, no later commit); deeper sub-clause audits left to the
   rubric if the L1 enumerates them.
4. **Marker reading**: `(only after a new steer)` (:3306, :3322) is treated as the
   steer-conditioned class of `(after a steer)`; the JSON keeps both the raw marker string
   and the exemption so the rubric can re-decide if it wants a stricter reading (under a
   strict reading, :3306 would join the mismatch set).
5. Excluded scope: non-numbered eras (`luna-round-*`, `arc2-loop1-round*`,
   `arc3-loop1-round*`) and the `## Verdicts, planned, retired` row :152 — not `## Round <N>`
   sections.
