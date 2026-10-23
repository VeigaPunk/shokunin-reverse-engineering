# WHonestStop — read-only adversarial audit

## Axes and evidence boundary

Axes: **depth** (assigned learning axis), calibration, provenance/identity, coverage/scope containment, and gate/promotion status. These are review dimensions, not new claim predicates or numerical credits.

Assignment pin: `d7076120e4f00c6d18aa77b8764d14861e820eb2`; base: `428315a8f5674b952def862910af6e07a6c2224b`. Evidence below is retained lane text read through `read`/`grep`, not a newly executed measurement or an independent Git-object authentication of the working-copy snapshots. No code, tests, shell commands, other runtime, subagents, or background jobs were run. Consequently this review has no experiment argv, execution UTC interval, stdout/stderr, or exit status of its own. Historical run details are attributed below to their retained receipts. No tools were installed or updated. Only this report was written.

This is lane advice, not outside verification, admission, or a canonical judgment.

## Strongest local counterexample

The same retained record contains **107 passing parser selftest cases**, a passing counter selftest, two located primary-source quotes, and nevertheless **no frozen original claim, no admissible expected-fixture manifest, and null before/after measurements**. Thus even accepting every reachable source/selftest result would not supply the missing 32 independently expected carrier rows.

Evidence:

- `.ufo/waves/round-33/claim-stop.json:8-21` preserves the conjunctive predicate and planned target, says `NOT FROZEN`, sets before/after/counting command to `null`, and records `target_changed:false`, `exploratory_relabel:false`, `numeric_axis_gain:0`.
- `repairs/parser/selftest-chpe_profile.json:2-8` under that wave records 107 cases, 45 defined/produced finding IDs, and `pass:true`. These are instrument cases, not 107 independently frozen carrier outcomes.
- `repairs/parser/selftest-measure_driver.json:45-57` explicitly records a hash-lookup stub matching all four seen selftest items, then failing unseen equivalents. This existing isolated test is a concrete counterexample to interpreting finite selftest agreement as generalized reader knowledge. No additional control was constructed or run here.
- `document-spec.json` specifies byte/quote/section/line checks; its presence is not an execution receipt, and its document predicates cannot discharge the fixture conjunct.

**Impacted axes:** depth and calibration if these unlike quantities are exchanged; provenance if selftest results are described as independent carrier results.

**Smallest safe correction:** preserve the honest stop and keep source, repair, and isolated-instrument evidence in separately named categories. Do not sum, relabel, rescale, or promote their counts into the original target. The missing admissible input manifest is a substantive prerequisite, not a wording defect; this assignment forbids reconstructing or replacing it.

## Exact wording requiring narrow status/scope

No inspected LOG/SCORECARD/SKILL/knowledge sentence asserts that R33-C1 attained 32 rows, or that the source/selftest work replaces that target. The following are narrower wording risks, not evidence that the stopped claim was revived.

### H1 — premature-looking permanent-gate status

Exact registry cells at `SKILL.md:1092`:

> Selftested selectable freeze integrity
>
> gate; active successor to the round-32 selectable variant

Counterevidence: `corpus/lessons/round-33.md:22` explicitly says:

> The permanent round-33 copy requires its own final measured run before any green gate is asserted for that copy.

`prep/R33FreezeSelftest.md:35-49,64-72,86-96` records five cases against the **scratch copy**, SHA-256 `2afc7f8ee751cb497bbec57f601c41ff4080182ec633d7280da143a06b6d4fda`, and leaves ported-copy verification separate. Therefore the registry's terse “Selftested”/“active successor” wording should not stand alone as permanent-copy green provenance. Registration and tested preparation source are defensible; completed installed-copy verification is not established by that receipt.

**Impacted axes:** instrument provenance and promotion status, not a newly measured depth result.

**Smallest safe correction:** label the row “registered successor; preparation copy selftested; permanent-copy measured run pending,” retaining its gate classification. This review does not request or execute a run. This is a fixable status ambiguity, not proof that the predicate is defective.

### H2 — controls phrased as a production chronology

Exact sentence at `corpus/lessons/round-33.md:16`:

> The proposed depth surface is parsed structural facts, not prose agreement; denial and word-bag controls still precede production measurement.

There was no admitted original production measurement (`claim-stop.json:12-16`; lesson `:38`). The independently retained counter selftest does include denial/word-bag cases (`selftest-measure_driver.json:35-42`), but that does not establish a carrier-study control/data sequence. The quoted sentence can be read as a procedural requirement, so it is **not** proof that held controls were admitted; its present-tense chronology is unnecessarily ambiguous after the stop.

**Impacted axes:** calibration and provenance.

**Smallest safe correction:** “Denial and word-bag cases are retained only within the independent counter selftest; no original R33-C1 production measurement followed, and no held-derived control is admitted.”

### H3 — unqualified “admission evidence” in a repair report

Exact sentence at `prep/R33TimestampRepair.md:187`:

> Only the final historical-fixture run receipts are admission evidence.

The surrounding section concerns timestamp-repair fixtures, not the stopped CHPE carrier claim. The historical timestamp gate measures base `428315a8` and scope `.ufo/waves/round-32`, not an R33-C1 after-state. Read with that context the sentence does not actually assert 32-row success, but “admission evidence” without an object is broader than this wave's authorized evidence-only role.

**Impacted axes:** provenance and promotion/admission clarity.

**Smallest safe correction:** replace “admission evidence” with “retained timestamp-repair evidence, not R33-C1 measurement or round-admission evidence.” No repair-result count needs changing.

## Executed versus pending evidence

All paths abbreviated below are under `.ufo/waves/round-33/` unless otherwise stated. “Records” means the inspected historical artifact says this; nothing was replayed by this seat.

| Item | What the retained evidence actually records | Boundary/pending status |
|---|---|---|
| Original R33-C1 | `claim-stop.json:12-21`: stopped before freeze; no before/after or counting command; numeric gain 0 | Not a failed measured 0/32, not a completed 32-row study, and not a pending benchmark to reconstruct |
| Actual source text | Opened the two quote locations: `corpus/evidence/round-33/sources/Object-COFF.h:734-773`, especially `:768`; `pe-format.md:129-141`, especially `:133` | Confirms these located words and field declarations by reading; no fresh source-digest computation, full source audit, or actual-revision document-spec run was performed here |
| Parser instrument | `repairs/parser/selftest-chpe_profile.json:2-8`: 107 cases, 45/45 finding vocabulary produced, `pass:true` | Original isolated recipes; not an independent carrier sample. JSON does not contain its own start/end UTC or argv, so those execution details are not inferred |
| Counter instrument | `repairs/parser/selftest-measure_driver.json:4-160`: 35 named checks, `pass:true`, including outer CLI, document-check, denial, bag, type, and hash-lookup cases | Internal instrument results only; synthetic `matched:4` values are not the target and `green_docspec_docs_ok` is not a receipt against the lane's actual `document-spec.json` |
| Legacy adapter instrument | `repairs/parser/selftest-r32_oracle_adapter.json:4-81`: 11 named results, `pass:true` | A produced legacy report is not a measured R33 baseline; the adapter's permissive outcomes remain visible |
| Freeze successor | `prep/R33FreezeSelftest.md:37-49`: `timeout 600 python3 -I -B freeze-integrity.py --selftest`, scratch cwd, start/end `2026-10-23T08:11:00Z`, five PASS, exit 0 | Preparation-copy evidence. Permanent-copy final run explicitly pending in lesson `:22`; no original R33 claim exists to certify |
| Disk audit red scan | `repairs/disk/scan-receipt.txt:2-23`: start/end `2026-10-23T08:16:03Z`; exact argv names three explicit retained records; exit 1, two red historical commands, zero errors | This is the original red lexical scan, not a clean wave-wide compliance result; no tree walk or execution enforcement is proved |
| Disk audit extended selftest | `repairs/disk/selftest-receipt.txt:2-11,29-39`: `timeout --kill-after=5s 60 python3 -I -B disk_guard.py --selftest`; start/end `2026-10-23T08:22:57Z`; 14 lexical + 3 outer = 17 PASS; empty stderr; exit 0; tool SHA-256 `a7253d24a3e2fa848ec472bf5be388c5df78e7c48a989373c87956ee89a40573` | `prep/R33DiskGuard.md:175-181` then changes the scratch-root selection, gives source SHA-256 `e61217206fe2a815ff3a2316e87370bfa430a6268900c108ee76f941de8d7f67`, and says no selftest rerun. Installed-copy verification remains pending (`LOG.md:3067`; `SKILL.md:1108`) |
| Timestamp repaired historical gate | `repairs/timestamps/receipts-hashed-repaired/receipt.txt`: exact forwarded argv retained; start `2026-10-23T08:19:09Z`, end `08:19:10Z`, exit 0, stderr 0 bytes; measured revision `428315a8f5674b952def862910af6e07a6c2224b`; scope `.ufo/waves/round-32`; stdout records 179 files, 6 findings, 0 unexempted, 5 applied allowances | Green is explicitly after exact hash-bound allowances, not strict/no-exemption green, and not a scan of round-33 evidence or the assignment pin |
| Timestamp relocatable-copy check | `prep/R33TimestampRepair.md:164-174` reports installed-copy selftest at `2026-10-23T08:29:27Z`, three cases, exit 0; base gate at `08:29:32Z`, exit 0 | Copy is a private scratch installation, still measuring base/round-32. Its reported success cannot silently transfer to a later lane revision or a different scan scope |
| Historical debts | `SKILL.md:1088,1096-1104` preserves missing selftests in archived verdict scripts and five un-killed wrapper mutants | New metadata reader/selftests do not close these by implication |

The timestamp receipt pins the unchanged underlying tool to `489ef6ca668ec5c8b3d7faed0e24e6bd3cbf616951f4d49dfbec438e392acc00` and allowance spec to `0ba984d64e98c8784974d852a89919ec54685188e68428c95c4953427d500332`. These are read receipt values, not newly computed hashes. Likewise `source-pins.json` declares LLVM revision `0d261d1ca552c95a8f007e061c787ac7132fbcbc`, Object-COFF digest `214d3f4a186be95dee7df0d19edaf04408b45f9d243152e2a4c2fb2f762f2320`, and PE Markdown digest `563f2dd952e16ca836036189ee82e46f1dbde29d716ee4ea5d2277e9562609d8`; this review does not authenticate those digests by execution.

## Stop, safety, scope, and promotion checks

- **No target exchange observed:** `SCORECARD.md:3311-3315`, `LOG.md:3071-3072`, `SKILL.md:1113-1115,1140-1149`, and the knowledge entry `:2,19-21` consistently separate the original claim from source/repair/selftest work. The card explicitly says not exploratory or rescaled, counts not evaluated, owned scores 10→10, delta 0, no new capability row. The lowest-axis wording at `SCORECARD.md:3307` is supportable as axis selection, not evidence of achieved depth improvement.
- **Held-output status is not transport status:** `safety-holds.json:5-15` records the provider refusal at `2026-10-23T08:30:15.264Z` and the original held item remaining untouched. `quarantine-record.json:3-17` records excluded dependent materials and removal outside the lane. Only this permitted metadata was inspected; neither quarantine nor excluded reports/code/fixtures/controls were opened. Metadata records removal; this review does not claim a forensic inspection of removed contents.
- **Independent retention is explicitly limited:** `prep-provenance-final.json:47-59,158-166` marks the parser item “independent artifacts only; mixed report excluded” and the input-author item “cyber_policy_hold; all outputs excluded,” despite returned transport. `prep/R33ChpeParser-independent.json:25,35,45,48-51` calls each retained selftest non-production and excludes the mixed report. Its four code digests agree textually with `parser-pins.json`; cryptographic recomputation and authorship reconstruction were outside this no-code audit. Thirteen returned transport jobs must not become thirteen admitted evidence items.
- **Source admission is scoped, not round admission:** `corpus/SOURCES.md:106-108` keeps S100 `rejected`, while S101/S102 are `mined` for LLVM structural/emitter/reader definitions and PE headers respectively. S102 expressly does not supply CHPE offset/tag authority. The knowledge entry `:15` marks strict exclusions and layout derivations as local policy/inference, not universal PE validity.
- **No Windows/ABI/coverage inference observed:** `SKILL.md:1119-1138`, knowledge entry `:21`, `corpus/README.md:86,188`, and lesson `:17,21,32,47` explicitly deny authenticated instructions, ABI correctness, Windows loadability, EC recovery, runtime proof, or widened Core. The affirmative PE-source wording about Windows is source documentation, not a run of this reader's candidates. `PROVINCE.md:357-359` retains the prior round-32 twelve-synthetic-leaf native-view boundary; it does not add a round-33 Core holding.
- **No promotion closure observed:** `SHONEN.md:5-12` remains asserted `[~]`, with no identified promotion verifier. `SCORECARD.md:31,49,3313` denies promotion from finite proxies and keeps this round's scores unchanged. Lesson `:32` reserves outside closure to a fresh non-author process, not these lane seats. No current gate/prose/selftest count can substitute for that authority.

## Smallest safe disposition

Keep the stopped claim, unchanged target, excluded held item, and all explicit coverage/ABI/Windows limits. Resolve H1's permanent-copy status label and narrow H2/H3's production/admission language; do not alter predicates, invent a new benchmark, promote source text to carrier evidence, or treat pending final runs as executed. There is no admissible numerical depth improvement demonstrated by this review, and no replacement study is proposed.

Report: `.ufo/waves/round-33/w1/WHonestStop.md`
