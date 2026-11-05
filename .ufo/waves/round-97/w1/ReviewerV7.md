# ReviewerV7 — unbound receipt fields at landing 867ed98 → w1 review

Seat: kaidoku round-97 w1, reviewer. Scope: `tools/round-97/stop-boundary-repair-battery-v7.py`
`verify_receipt` and `main` at L = 867ed98d85f45a18265441c1760386ef353b3d43, plus the
R97-C1 rule receipt's own verifier (`verify_own_receipt` in the frozen
`tools/round-97/kill-rule-v3.py` blob at L): the artifact that lands under
`.ufo/waves/round-97/l1/scores/c1-at-*.json` is a KILL-RULE receipt, not a
v7-counter receipt — v7's `verify_receipt` runs inside the rule's run on the
embedded v7 result, while the rule's own `--json-out` file is bound only by
`verify_own_receipt`.

Method: every forged receipt was written with the frozen writer's own `write_receipt`
(import from the blob bytes: v7 blob sha256
2cd984f3a949520965487992c1c3917ff33a37bcf4221fe411fb990033ee8b58 = live file at L)
and fed to the frozen verifiers via importlib in `python3 -I -B` runs. Drivers and
results: `/fast/scratch/hyaku/kaidoku-r97/ReviewerV7/py/{forge_driver2,forge_driver3}.py`
→ `py/{forge-results-v2,forge-results-v3}.json`. Honest base: frozen blob pins at L
+ frozen counts `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6;
far-refused 12 of 12; fresh-roundtrip 2 of 2`; the honest base verifies clean as a
positive control in both batteries.

## A. v7 verify_receipt — field | bound by | forged receipt | verifies clean

| field | bound by | forged receipt | verifies clean (yes/no) |
|---|---|---|---|
| counts (9 keys) | recomputed (allow-list COUNT_KEYS; missing/extra refused) | n/a (baseline) | n/a |
| met_target | typed (bool required) | met_target=None / "true" | no (met-not-typed) |
| label | recomputed + frozen expect + met gate | label≠recompute / ≠expect / met=False w/ expect label → label-not-recomputed, label-not-frozen, met-not-recomputed | no (refused) |
| revision, head | bound to `--rev`; head==revision | revision≠L / head≠revision | no (revision-not-bound, head-not-bound) |
| counter_sha256, verdict_sha256, repair_sha256 | pin + byte-pin against `git cat-file blob` at `--rev` | counter_sha256="0"*64 | no (byte-pin-not-bound:counter) |
| repair_cmd | bound to the run's `--repair-cmd` | "tools/round-87/upx-magic-repair.py" | no (repair-cmd-not-bound) |
| imported_r92_battery_sha256, imported_v2_sha256 | pin | "0"*64 | no (imported-pin-not-bound) |
| public_met, public_label | mirrored to met / label | public_met=False | no (public-met-not-bound, public-label-not-bound) |
| **exit** | **nothing** | exit=1 on an otherwise-honest receipt | **yes — CLEAN VERIFIES** |
| **class** | **nothing** | "forged class" | **yes** |
| **tool** (v7 layer) | **nothing** | "tools/round-93/FORGED.py" | **yes** |
| **fresh_cells** | **nothing** | [{"output": "<forged escape>", "rc": 1}] and absent | **yes** |
| **public_carriers** | **nothing** | "forged" | **yes** |
| **public_cells** | **nothing** | "forged" | **yes** |
| **public_intact** | **nothing** | 999 | **yes** |
| **fresh_intact** | **nothing** | 999 | **yes** |
| **fresh_provenance** | **nothing** | {"marker_in_mutated": False, …} and absent | **yes** |

Negative controls (bound-field flips): counter-pin → `byte-pin-not-bound:counter`;
public-met → `public-met-not-bound`; met-lying → `met-not-recomputed` +
`public-met-not-bound`; head → `head-not-bound`; revision → `revision-not-bound`,
`head-not-bound`. Every bound-field flip refused with the expected reason; every
unbound-list flip verified clean.

## B. The artifact that actually lands: kill-rule receipt layer (verify_own_receipt)

Command A's `--json-out` (the c1-at-*.json artifact) is the RULE receipt; it goes
through `verify_own_receipt`, not `verify_receipt`. Fields bound there:

- met_target: typed (bool required) → ownrec-met-not-typed
- world_revision: bound to the 40-hex HEAD this run resolved → ownrec-world-not-bound
- counts.mutants_killed == counts.mutants and counts.forgeries_refused ==
  counts.forgeries (only when met is True) → ownrec-counts-inconsistent

| field | bound by | forged receipt | verifies clean (yes/no) |
|---|---|---|---|
| **exit** | **nothing** | exit=1 | **yes** |
| **class** | **nothing** | "forged" | **yes** |
| **decl / decl_full** | **nothing** | "1"*40 / "2"*40 | **yes** |
| **identity_not_killed VALUE** | **nothing** (typed only; flipping True→False verifies) | False | **yes** |
| **kill_classes** | **nothing** | {"semantic_killed": 0, "crash_killed": 99, "classes_match": False} | **yes** |
| **counter (path string)** | **nothing** | "tools/round-97/FORGED.py" | **yes** |
| **counts.negctl_refused** | **nothing** | 0 (label still says "negctl refused 3 of 3") | **yes** |
| **counts.probe_consistent** | **nothing** | 0 | **yes** |
| **counts.honest_accepted** | **nothing** | 0 | **yes** |
| **counts.wlink** | **nothing** | 0 | **yes** |
| **counts.durability** | **nothing** | 0 | **yes** |
| **counts.bytes_bound** | **nothing** | 0 (label still says "bytes 5 of 5") | **yes** |
| **counts.dirtyrefuse** | **nothing** | 0 | **yes** |
| **counts.cwd_ok** | **nothing** | 0 | **yes** |
| **honest (K-check map)** | **nothing** | every K-check flipped to {"ok": False} | **yes** |
| mutants (22 rows) | **nothing** | rows replaced with a single forged row | **yes** (map-level; per-row kill_class semaphore not re-derivable from the receipt alone) |
| counts.mutants_killed < counts.mutants | ownrec-counts-inconsistent | 20 vs 21 | no |
| met_target=None | ownrec-met-not-typed | None | no |
| world_revision≠resolved HEAD | ownrec-world-not-bound | "3"*40 | no |

Mega-forgery: a receipt flipping every unbound field at once (negctl_refused 0,
probe_consistent 0, honest_accepted 0, wlink 0, durability 0, bytes_bound 0,
dirtyrefuse 0, cwd_ok 0, classes_match False, identity_not_killed False, exit 1,
decl/counter at forged paths, honest map all ok:False) while keeping met_target=True,
world_revision=L, label="…mutants killed 21 of 21…ownrec 1 of 1",
counts.mutants_killed==counts.mutants, forgeries_refused==forgeries —
**verifies clean: `MEGAFORGERY ok: True reasons: []`** (heredoc run against the
frozen blob import `py/r97kill.py` in scratch).

## C. Severity and what actually binds

Ownrec admits a receipt in which 8 of the 11 numeric K-gates (negctl_refused,
probe_consistent, honest_accepted, wlink, durability, bytes_bound, dirtyrefuse,
cwd_ok), the tool-path fields, the entire honest K-check map and all 22 mutant rows
are unbound, provided `met_target=True`, `world_revision` = the run's own resolved
HEAD, `mutants_killed==mutants`, `forgeries_refused==forgeries`, and
`identity_not_killed` present as bool. The label is built by f-string
(r97kill.py:733) from those same unbound counters, so it is not an independent
binding; ownrec never checks the R97-C1 label against a frozen constant.

Mitigating fact: command A passes `--decl e859a88d…` and the frozen mutants file, so
the rule re-derives the K-gates from the frozen instrument pins at runtime — a
forged-while-running receipt still carries what the rule just computed. The exposed
surface is **post-hoc receipt rewriting** (edit the landed JSON), exactly the class
R97-C1 nominally closed ("byte binding closes M96-a": a receipt naming R while
carrying pins differing from R's bytes refuses). Round-97 byte binding covers only
counter/verdict/repair pins + revision/head; everything else forgeable post-write.

## D. Reproduction commands (all run this session; receipts under scratch)

- v7 blob at L → sha256 `2cd984f3…ee8b58` (= live file at L and HEAD).
- Battery A (v7 layer): `cd /fast/scratch/hyaku/kaidoku-r97/ReviewerV7 && TMPDIR=$PWD python3 -I -B py/forge_driver2.py` → rc=0, 18 cases, 12 clean (1 honest control + 11 unbound-field forgeries), 5 refused.
- Battery B (rule layer): same with `py/forge_driver3.py` → rc=0, 20 cases, 17 clean (1 honest control + 16 unbound-field forgeries), 3 refused.
- Mega-forgery heredoc → `MEGAFORGERY ok: True reasons: []`.

## E. Tooling record

No tools installed/upgraded. No pacman/sysctl/host change. All work in the shared
clone (ro verified); lane only read via `git cat-file blob`; no mutating git command.
