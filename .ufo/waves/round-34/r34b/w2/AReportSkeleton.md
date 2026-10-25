# AReportSkeleton — fleet-report drafts for round 34, run-6 re-dispatch (R34-C2 stop)

Seat `L1Kaidoku34-2.AReportSkeleton` (scribe, wave 2). Assignment: draft the fleet report's
`Work performed`, `Landed changes`, `Before -> after measurements`, `Sources & frontier`,
`Trend verdicts` and `SHONEN` sections for this attempt, with an evidence pointer per claim, and
mark anything not groundable in committed bytes **UNPROVEN** instead of inventing a pointer.

Axes named for this seat: **evidence fidelity** (a pointer resolves to the bytes that carry the
claim), **pointer completeness** (no claim without a location), **non-overclaim** (unlanded work
never described as landed), **conflict preservation** (contradictions reported verbatim, not
resolved here).

## 0. Observation cutoff, and why this file has two states

- **Final cutoff HEAD:** `5a0435ffb9a8921206144e0b61fe3c12a89b59c2`
  (`2026-10-25T07:35:33Z`), parent `66b84027`. Everything asserted as landed below is at
  `5a0435ff` unless it names another revision.
- **The lane moved twice during this seat.** My first pass observed HEAD `66b84027`; two
  findings I recorded there (an asserted-but-absent freeze-integrity receipt, and a
  three-vs-four-seed undercount in the stop record) were **fixed by `5a0435ff`** before this
  report was finished. Both states are recorded: the finding, then its resolution, with the fix
  pointer. I have not deleted my own findings to make the record look cleaner.
- **An earlier revision of this file (381 lines) was snapshotted into `5a0435ff` by the L1
  while I was working; this text supersedes it and is uncommitted.**
- **Still moving at the cutoff:** `corpus/SOURCES.md` (+1 line, restoring S105), `LOG.md`,
  `SCORECARD.md`, and the `w2/` reports are uncommitted deltas (`git status --porcelain`,
  07:36:07Z). Nothing uncommitted is described as landed.
- Paths are relative to `kaidoku-shokunin/.ufo/waves/round-34/r34b/` unless they start with
  `corpus/`, `tools/` or `SKILL.md`/`LOG.md`/`SCORECARD.md` (lane root).
- **UNPROVEN** = the claim could not be resolved to committed bytes at the cutoff. It is not an
  assertion that the work is false, only that the report may not cite it as evidence yet.
- I executed no reader, counter, gate, fixture or ELF carrier. Probes were read-only (`git` read
  subcommands, `sha256sum`, `wc`, `sed -n`, `grep`, inline `python3` over static bytes). No tool
  installed, upgraded or removed. Exact commands, exits, UTC in §8.

---

## Draft 1 — Work performed

**One claim this round: R34-C2, recorded as capability acquisition on axis depth**
(`claims.json:claims[0].axis`, `:claims[0].type`; the axis label is contested — conflict C1).
The surface is a pre-freeze shortcut-replay gate that makes the prior round's QUALITY 67
executable (`corpus/QUALITY.md:77`). Predicate `P34-shortcut-replay` in the claim file: 31 words,
sha256 `7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b`
(`predicate-reconciliation.json:sites.A_claims_and_configs`; recomputed by me, §8). Target 8,
six clauses `gate_present`, `selftest_clean`, `mutants_killed`, `red_refused`, `green_clean`,
`green_positive_meets_target` (`tools/round-34/c2-shortcut-gate-counter.py:112-120`).

**Freeze before any of its data.** `c79bbe7b0959132b9873ff3431cf5eb313b58b33`, 27 files,
1345 insertions, 0 deletions (`git show --stat c79bbe7b`; independently recounted in
`w1/RevFreezeOrder.md:57`): the gate `tools/round-34/replay-gate.py` (313 lines), the six-clause
driver `tools/round-34/c2-shortcut-gate-counter.py` (137), red and green configs, eight synthetic
512-byte `MREC` fixtures, `expected.json` (25 records), eight readers including the structural
positive control, `mini-fix/spec.json`, and 26 pins in `claims.json:claims[0].pins`.

**Before.** `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…`, exit 2
(`before/c2-at-base.txt:1`). Reproduced independently: `git cat-file -e
ec3125ad:tools/round-34/replay-gate.py` exits 128; the same path at `c79bbe7b` exits 0 (§8).

**Production (the gate, not a reader).** `GATE_COUNTER_OK finding=shortcut_gate_discriminates
selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN
green_positive_matched=8 clauses_failed=-`, exit 0 at `c79bbe7b`
(`after/c2-at-instruments.json`; `after/c2-at-instruments.txt:1`). Green: CLEAN, 8 matched, 7
classes below target; red: REFUSED naming `label-memorization`; selftest 12 cases, 3/3 mutants
killed (`after/c2-at-instruments.json:clauses, selftest_line`).

**Five controls, all MISS** (`controls/*.json`; exits read from the receipts, not inferred):

| control | exit | failing clauses |
|---|---|---|
| do-nothing (`--root` without gate) | 2 | none reported — `gate_absent`, no clause block |
| always-clean gate | 1 | `red_refused`, `selftest_clean` |
| junk clean-printing stub | 1 | `red_refused` |
| no-positive-check gate | 1 | `mutants_killed`, `selftest_clean` |
| vacuous gate without the shortcut floor | 1 | `selftest_clean` |

**Enforced pins.** `after/freeze-integrity-instruments.txt` (landed `5a0435ff`) is a 26-line
`ok … commits_after_freeze=0` table ending `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe
rev=66b84027…`. The 26-pin container's equality with `claims[0].pins` I verified directly
(dict equality true; 26 entries, §8). Two nuances the report must keep: the receipt's
`freeze=` names `b917ea64` (the commit that added the container), not `c79bbe7b`, and the file
records no argv or exit code — the CLEAN assertion is the tool's own printed line
(`claim-stop-addendum.json:enforced_pin_receipt.note` says exactly this).

**Wave 1 — the first falsifiers.** 34 seats in one validated `task` call (`w1-spec.json`,
`w1-seat-map.json`): executor 7, reviewer 6, scribe 5, mutation-tester 4, critic 4, scout 3,
sentinel 2, revenger 2, connector 1. All 34 reports are now landed (`66b84027`); the wave still
has **no settle or provider-provenance record** — every `w1/swarm-registry.json:members` entry
carries `agentId: null`, and `w1-payload.json` holds only name/role/task. "34/34 completed, 0
dead, 0 holds" is therefore **UNPROVEN** and must not be written (finding G4).

**Stop, with its receipts now bound.** The green surface's only perturbation is a per-run
name-pool permutation, so record order, count, every `flags`/`value` byte and the name multiset
survive it. The decisive class is content-multiset memorisation:
`w1/CtlMultiset-files/nameset.py`, sha256
`2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` (recomputed by me). It
**decodes no header field, no record entry and no `name_off`** — it reads the file into a buffer
and scans or hashes it (`nameset.py:48-55`). That wording is the addendum's correction of "reads
no header": blindness is content-contingent, not constructional
(`claim-stop-addendum.json:wording_corrections[0]`; `w2/AStaticBlindness.md`).

Measured results, each with a retained receipt:
- **nameset**: `matched 8/8` at four seeds (`kaidoku-r34-mini-v1`, `alt-1`, `alt-2`, `alt-3`),
  exit 0, receipt sha256 `fa6e8f09…`
  (`w1/CtlMultiset-files/nameset-green-receipt.json`;
  `claim-stop-addendum.json:decisive_receipts[0]`). The original stop record listed three seeds
  (`claim-stop.json:observed.seeds`); the addendum binds four — finding G3, now resolved.
- **payload-signature** (count + ordered `(flags,value)`, no name byte read):
  `matched 8/8` plain and `8/8` with every name byte zeroed, while the pinned structural reader
  scores `0/8` on the same zeroed bytes; receipt sha256 `23e26fe4…`
  (`w1/CtlMultiset-files/payload-keyed-receipt.json`, source
  `w1/CtlMultiset-files/payload_keyed.py`, landed `5a0435ff`;
  `claim-stop-addendum.json:decisive_receipts[1]`).

**Further unregistered classes at 8/8, report-only.** These are executed scores in seat reports,
but their sources are **not committed** (`claim-stop-addendum.json:classes_without_committed_source`):
value/offset memorisation `s2d_fixed_slice_offsets_memo` and record signature `s2b_record_sig`
(`w1/MutShortcutClasses.md:100`, `:107`); transform/digest replay `s2b_digest_replay`
(`w1/MutShortcutClasses.md:102`; `w1/MutFixtures.md`); `$HOME`-accumulating hybrid
(`w1/RevengerGateFailModes.md:60,73`; cited as E1 in the addendum). Further 8/8 variants are also report-only: prefix-keyed (`w1/CritCounterLimits.md:32`), a scribe
topology probe (`w1/ScribeKnowledgeEntry.md:127-133`), name-pool keyed and label-hash replay
(`w1/MutShortcutClasses.md:104-105,109`). Count: **two** met-target classes with committed
source, **at least six** further met-target variants with none. "Five unregistered classes" in
the stop record and SKILL is therefore a floor, not a census, and every count must carry the
provenance qualifier (finding G12).

**Registration, not the mechanism, was the hole.** Registering a class flips the same gate:
the payload probe → `REPLAY_GATE_REFUSED`, exit 2 (`w1/LabratSeedSensitivity.md:143-145`);
`prefix-keyed` → `REPLAY_GATE_REFUSED`, exit 2 (`w1/CritCounterLimits.md:34`). Two roster defects
compound it: the registered `fixed-slice` reader is a printable-run scanner, not a fixed-slice
replay (`w1/CritCounterLimits.md:37-38`; `tools/round-34/gate-config-mini.json:15`), and a drop
to `MIN_SHORTCUTS=3` still prints CLEAN (`w1/RevPredicateIdentity.md:75`;
`tools/round-34/replay-gate.py:31,58`).

**Record defects, disclosed not repaired in frozen bytes**
(`claim-stop.json:record_defects_disclosed`; addendum F6):
F1 pins were declarative and in a container the lane's own freeze gate rejects — repaired by the
container **and now a retained receipt** (`after/freeze-integrity-instruments.txt`); F2 the frozen
`predicate_identity` is false, A=31 words vs B=46 words (both digests recomputed by me), with the
green counter's `P34-mini-records` counted as a third scoring site by the QUALITY correction
(`corpus/QUALITY.md`, corrections section) while `predicate-reconciliation.json` treats it as a
separate namespace — both readings preserved (finding G14); F3 class drop invisible; F4 mutant M3
survives its own selftest and turns the red case CLEAN (`w1/MutGateBranches.md`); F5 receipts
untracked at first audit (repaired `b917ea64`); F6 the transform is deterministic under a public
default seed and publishes the transformed copy's digest in the copy name, so an offline replay
reaches 8/8 (`claim-stop-addendum.json:additional_record_defect`).

**Disclosed instrument limits** (each with a committed pointer): `met_target` trusted and never
cross-checked with `matched` (`replay-gate.py:93-101,119-127`; `w1/CritCounterLimits.md:52`);
per-reader rows dropped at the gate boundary (`replay-gate.py:100`;
`w1/CritCounterLimits.md:53`); a crashing reader scored "below target"
(`w1/CritCounterLimits.md:54`); refusal filtered by free-text class label (`replay-gate.py:123`;
`w1/RevengerGateFailModes.md` D1); the floor is not an equality (`replay-gate.py:31,58`); a gate
that runs no reader satisfies all six clauses (`w1/CritCounterLimits.md` probe E); `--rev` is a
pure echo (`c2-shortcut-gate-counter.py:67,73`; `w1/ExecRecountC2.md` F2); readers are arbitrary
uid-1000 code and a clean verdict cannot absorb that (`w1/SentinelContainment.md:147-151`); one
fixture format, one size class (`w1/ExecGreenIndependence.md:162`) with tautological
fixture↔expected agreement (`:139`); trailing NUL padding lets single-record fixtures draw the
identity permutation (10/5000 beta, 13/5000 epsilon: `w1/ExecPermuteAudit.md:150-151`).

**Wave 2 (this wave) is not settled at the cutoff.** 32 seats (`w2-spec.json`: reviewer 10,
critic 6, executor 6, scribe 5, mutation-tester 2, sentinel 1, connector 1, revenger 1). Ten
wave-2 reports plus this file were snapshotted into `5a0435ff`; more were in flight. Several
wave-2 findings already forced corrections in `5a0435ff` (the addendum's `why` names
`w2/AStopCompleteness.md`), so wave-2 is **partially effective, not settled**: no
"stop falsified"/"stop sustained" verdict may be written before settle (finding G11).

**Inherited claim untouched.** R34-C1's five frozen artifacts are byte-identical from
`54a87a51`; its reader and carriers were not executed
(`w1/RevR34C1Untouched.md:120-122`: 183 execve, every one `/usr/bin/python3`, fixtures static).
R34-C1 is not reopened, re-scored or relabelled (`claims.json:retained_claim`).

---

## Draft 2 — Landed changes

Five commits carry this attempt. Identity/author fields are not re-asserted here (not re-checked
by me).

| commit | content | anchor |
|---|---|---|
| `c79bbe7b0959132b9873ff3431cf5eb313b58b33` | the freeze: `claims.json` (90 lines), gate, six-clause counter, two configs, eight fixtures, nine readers, `spec.json`, `expected.json` — 27 files, +1345/−0 | `claims.json`; `LOG.md:3094-3103` |
| `b917ea64ebbeab49b8258d71ffb34e700715ffe6` | after wave-1 record audits: before/production/control receipts (13 files), `instruments.json`, `predicate-reconciliation.json`, `w1-payload.json`, `w1-seat-map.json`, `w1-spec.json`, the then-written w1 reports, all 30 prompts, `w1/swarm-registry.json`, the id-assimilation guard (105 registered vs 132 staged ids, `assimilation/collisions` empty) — 77 files, +6001 | `LOG.md:3094-3103`; `w1/ExecRecountC2.md:132` (F6) |
| `cd75b92e583735729546b0ea3b250f2df6d0652a` | the stop: `claim-stop.json` (87 lines), `w1/CtlMultiset-files/{nameset,pathkey,mini-counter-fresh}.py` — 4 files, +352 | `LOG.md:3098-3100`; `SCORECARD.md:3347-3369` |
| `66b84027` | the stopped claim's record: SCORECARD run-6 section (+26), LOG run-6 block (+11), lesson M34-5..M34-11, QUALITY 68-73 (+6), SKILL instrument registry (+14), S106 row, knowledge entry, README (+4), the remaining w1 reports, `census-start.txt`, `w2-spec.json`, `w2-seat-map.json`, 32 w2 prompts | `SKILL.md:1209-1222`; `corpus/QUALITY.md:78-83`; `corpus/SOURCES.md:111`; `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` |
| `5a0435ffb9a8921206144e0b61fe3c12a89b59c2` | the stop's binding: `after/freeze-integrity-instruments.txt` (26-pin receipt), `claim-stop-addendum.json` (96 lines: decisive receipts, artifact shas, F6, report-only classes, wording corrections), `nameset-green-receipt.json`, `payload-keyed-receipt.json`, `payload_keyed.py`, `census-end.txt`, lesson M34-12, the QUALITY 68/70 corrections, and the first ten w2 reports — 18 files, +3118/−1 | `claim-stop-addendum.json`; `corpus/QUALITY.md` corrections section; `LOG.md:3094-3103` |

**Inherited state.** Base `ec3125ad3d130d92f888a4128dfaa2982f36fff7`; the attempt-1 (R34-C1) stop
is inherited through `f432c8e3` and not rewritten (`claims.json:inherited_tip`;
`SCORECARD.md:3349`). `corpus/lessons/round-34.md` gained the new attempt as an appended section
and now also M34-12; the attempt-1 text is untouched.

**Uncommitted at the cutoff — NOT landed:** the S105 restoration in `corpus/SOURCES.md` (+1 line),
the `LOG.md`/`SCORECARD.md` deltas, and the `w2/` reports (including this file's current text).
`git status --porcelain` at 07:36:07Z is the pointer.

**Two findings from my first pass, both answered at `5a0435ff`:** the asserted-but-absent
freeze-integrity receipt (G1) is now a landed artifact, and the three-vs-four-seed undercount (G3)
is now bound as four seeds. **One is still open:** the S105 row was swapped out by the S106 insert
in `66b84027` and, at `5a0435ff`, `corpus/SOURCES.md` still holds 105 rows with S105 absent
(row-id diff, §8) — the lesson M34-12 and QUALITY 74 documenting the swap are landed, the
restoration is not (finding G2). The report may not print the LOG's "rows 105→106" as fact until
the restore lands.

**Repair receipt nuance (G1, narrowed).** The landed receipt's label is `freeze=b917ea64ebbe`, the
commit that added the container, not the frozen `c79bbe7b`; the file carries no argv and no exit
code, only the tool's printed `CLEAN pins=26` line. The addendum states this in
`enforced_pin_receipt.note`. So: the repair is now evidenced; the claim "receipt over the frozen
container" must name `b917ea64` as the container's commit.

---

## Draft 3 — Before → after measurements

Counting command (unchanged): `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root
<LANE> --rev <REV> --json-out <RECEIPT>` (`claims.json:claims[0].counting_command`;
`SCORECARD.md:3353`). A control run adds `--gate <alternative gate>`.

| claim / surface | before | after | measured revision | verdict |
|---|---|---|---|---|
| R34-C2 / depth — pre-freeze shortcut-replay gate making QUALITY 67 executable | `GATE_COUNTER_UNEVALUABLE finding=gate_absent`, exit 2 (`before/c2-at-base.txt:1`) | `GATE_COUNTER_OK … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit 0 (`after/c2-at-instruments.json`; `.txt:1`) | before `ec3125ad`; after `c79bbe7b` | **falsified measure / honest stop** — an unregistered structure-blind class reaches the green 8/8 |

**Decisive counterexample (a control score, never the production reader's score).**
- nameset: `matched 8/8`, exit 0 at four seeds, exact argv/UTC/fixture digests in
  `w1/CtlMultiset-files/nameset-green-receipt.json` (sha256 `fa6e8f09…`).
- payload-signature: `8/8` plain and `8/8` with every name byte zeroed; structural control `0/8`
  on the same zeroed bytes (`w1/CtlMultiset-files/payload-keyed-receipt.json`, sha256
  `23e26fe4…`).
- At least six further 8/8 variants are report-only (no committed source): see Draft 1, G12.

**Gate controls** — table in Draft 1; all five MISS, maximum 5 of 6 clauses. Caution: no shipped
control or mutant makes `green_positive_meets_target` the **failing** clause, so that clause is
asserted but never discriminated (`controls/gate-no-positive-check.py.txt` fails
`mutants_killed,selftest_clean`; `w1/MutCounterClauses.md:137`). It must not be described as
exercised (G6).

**Owned scores stay 10→10, delta 0** (`claims.json:claims[0].scores_unchanged`): coverage 10→10,
depth 10→10, calibration 10→10; `SCORECARD.md:3361-3363` records the same three rows. No
capability row entered, no exploratory relabel.

**Axis-label conflict (C1) — preserve verbatim.**
`w1/CritAxisFit.md:234-239` returns `AXIS_FIT_FAIL depth`: "the surface R34-C2 actually moves at
`c79bbe7b` is a structural-counter admission *instrument* (operability, unowned proxy) with a
self-reported-verdict boundary, not `depth`". The claim file and `SCORECARD.md:3353` label the row
`depth`. Both are committed. The fleet report must carry the disagreement rather than choose, and
must not convert "six clauses met" into an axis gain.

---

## Draft 4 — Sources & frontier

- **Row counts — S105 is still missing at HEAD (G2).** At `5a0435ff`, `corpus/SOURCES.md` holds
  105 rows, ids S001–S106 with **S105 absent**; the working tree at 07:36:07Z holds 106 with S105
  restored (uncommitted). The row swap is disclosed and routed (lesson M34-12; QUALITY 74), and
  the census stayed exit-0 throughout, which is the point of the lesson. Correct wording until
  the restore lands: "105 rows, S105 dropped by the S106 insert, restoration in flight"; after it
  lands: "105→106, tier A 99→100, mined 101→102, rejected 4→4, malformed 0" (M34-12's own first
  recount: `A 99→99`, `rejected 4→3`).
- **Rows added.** S106 only (`corpus/SOURCES.md:111`): GNU binutils `readelf.c`, tag
  `binutils-2_47`, tier A, status mined, scope limited to the `SHT_GNU_verneed` section-header
  decode. Verified against the capture: sha256 `7e81eedf…`, 689,644 bytes; `:14149` carries
  `warn (_("Missing Version Needs information\n"));`; the record walk at `:14056` (`endbuf`),
  `:14072-14076` (`vn_version…vn_next`) and `:14102-14106` (aux fields) is as cited. **Provenance
  limit:** the capture lives only in
  `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/`, not in the lane — the row is
  verifiable only while that scratch survives.
- **Census.** `census-start.txt` and `census-end.txt` are both now landed (`66b84027`,
  `5a0435ff`); each shows nine `W04` duplicate-URL warnings and a final
  `kaidoku ok …/corpus/SOURCES.md` line. Neither records an **exit code**, so "both exit 0"
  (`LOG.md:3100`) is UNPROVEN as a retained receipt — the bytes are consistent with 0, no more
  (G9).
- **Quote counts.** No `quote-counts.json` for this attempt. The lesson states the S106 quote is
  6 contiguous words (`corpus/lessons/round-34.md:67`) with no counted receipt in the lane — the
  count is UNPROVEN.
- **Frontier.** No frontier row advanced (`w1/ConnectorFrontier.md:76`, `:125`: gate home is the
  SKILL registry, not Core, not the bar). PROVINCE unchanged — last commit `bb0af56c` (round-32),
  clean at the cutoff.
- **Sourced claim.** The structure language rests on S106, cited in the knowledge entry and in
  the SKILL limits paragraph (`SKILL.md:1221`).
- **Rejected / leads.** Prior art (Chakraborty, Kapoor & Narayanan, Fioraldi WEIZZ, Adebayo,
  Segura, Geirhos, tmp.0ut) stays **leads, not rows**, because no admitted entry cites them
  (`w1/ScoutWebReplayPriorArt.md:85-91`; lesson `:69`). S105 remains the retained rejected row for
  GNU Verneed/Vernaux authority — once the restore lands (G2).
- **Sibling overlap.** kake's `lookup_control_check.py` is the earlier instrument in this family,
  with tsukuroi, mado, chousa, kama and mori adjacent; cited, not absorbed
  (`w1/ScoutSiblings.md`). The "who owns the shortcut-class list" question is raised, not
  exercised (`w1/ConnectorFrontier.md:88`).
- **Knowledge entry.** `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`
  (73 lines, landed). It denies capability and lists the classes; one lineage points at a wave-2
  file (`w1/ACounterexample2.md`) that did not exist when the entry was written — replace the
  pointer after settle (G8). A 0-byte untracked file
  `corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` existed at 07:35Z and was
  removed by 07:37:12Z; noted only so no empty entry is re-landed.

---

## Draft 5 — Trend verdicts

- **expansion: unchanged.** No frontier row, no capability, no new domain ground. PROVINCE at
  `bb0af56c` and clean; the only SKILL change is an instrument-registry row plus a limits
  paragraph (`SKILL.md:1209-1222`), which `w1/ConnectorFrontier.md:45,125` holds out of Core and
  out of the QUALITY bar.
- **quality: improved (author assessment).** Against interest, the attempt disclosed a false
  predicate identity, an unenforced pin map, a class-drop hole, a surviving mutant, a deterministic
  transform leak (F6) and an axis-fit objection; it landed five controls, a scoped source row, a
  per-limit pointer set, and — after wave-2 attack — bound the decisive receipts, disclosed four
  report-only classes and corrected its own blindness wording. The remaining gaps are stated, not
  hidden: S105 still dropped at HEAD, no seat-settle record, a clause never discriminated, and no
  admitted entry re-checked (so "no admitted entry failed re-check" is UNPROVEN). Phrase as
  "improved, with the row swap open at filing".
- **discernment: improved (author assessment; axis label contested).** The frozen rule was applied,
  not amended: no target, threshold, class, predicate or label changed after the freeze; the
  counterexample is published with source and receipt digests and independently reproduced
  (`w1/ExecRecountC2.md:143`: `RECOUNT_C2_REPRODUCES`, 30/30 fields identical). Keep the
  counter-signal: the standing description of R34-C2 as a **depth** acquisition is contradicted by
  a committed seat (`w1/CritAxisFit.md:234`; C1), and "six clauses met" is registry-relative
  (`w1/RevengerR34History.md:297`). Discernment credit is for stopping, not for the axis claim.
- **Inherited trend.** Fourth consecutive non-pass in the lane's series (r32 text-presence, r33
  provider hold, r34 attempt-1 fixed-offset replay, r34 attempt-2 unregistered class). Carry it as
  context, not as this attempt's measurement.

---

## Draft 6 — SHONEN

- [~] **SKILL.md contains real decision tables, error patterns, checklists, cited sources** —
  advanced this attempt by the instrument-registry row, three verdict/exit rows and the limits
  paragraph (`SKILL.md:1209-1222`), landed `66b84027`, citing S106 (`corpus/SOURCES.md:111`); the
  registry's "26 pins, CLEAN" is now backed by a landed receipt
  (`after/freeze-integrity-instruments.txt`) whose label names `b917ea64`. Not earned: no
  non-author has exercised the paragraph.
- [~] **At least one end-to-end domain task executed and logged in LOG.md** — unchanged: still
  rests on the historical round-1 libjq task; this attempt executed an instrument-only harness on
  eight synthetic fixtures, ran no carrier and no production reader
  (`claims.json:instrument_notes.no_production_reader_run`; `w1/RevR34C1Untouched.md:120-122`).
- [~] **Instructions executable by an agent without oral context** — improved: the counting
  command, gate argv and exit codes are written out (`claims.json:claims[0].counting_command`;
  `SCORECARD.md:3353`; `SKILL.md:1215`). Not earned: following the counting command still
  reproduces a verdict without verifying the claim's own identity — the counter hashes no pin
  (`c2-shortcut-gate-counter.py`: no `hashlib`, no VCS call; `w1/SentinelContainment.md:29`) and
  the predicate sentence differs between claim and receipt (F2). The pin receipt exists as a
  separate tool run, not inside the counted command.
- [~] **No cross-domain bleed (PROVINCE.md still accurate)** — PROVINCE unchanged (last commit
  `bb0af56c`; clean at cutoff); scope audit `SCOPE_CLEAN_NO_PREEXISTING_HARM`, 27 additions/0
  deletions confined to `tools/round-34/**` + `.ufo/waves/round-34/**`
  (`w1/RevScopeNoHarm.md:257-260`). The adjacent **ownership** question (who owns the
  shortcut-class list, a CLEAN being config-relative) is raised and left to PROVINCE's Adjacent
  bucket (`w1/ConnectorFrontier.md:88`) — raised, not exercised.

---

## 7. Findings, with status at the cutoff

| id | severity | status | finding | pointer |
|---|---|---|---|---|
| G1 | high | **resolved** at `5a0435ff` | Freeze-integrity receipt over the 26-pin container was asserted in the stop record, QUALITY 68 and SKILL but did not exist at `66b84027`. Now landed; label names `b917ea64` (container commit), not the freeze; no argv/exit recorded. | `after/freeze-integrity-instruments.txt`; `claim-stop-addendum.json:enforced_pin_receipt`; `SKILL.md:1221` |
| G2 | **high, open** | open at `5a0435ff` | S105 row replaced by S106 at `66b84027`; HEAD still 105 rows, S105 absent. M34-12/QUALITY 74 document the swap; the restore is uncommitted. "Rows 105→106" is false at HEAD. | `git show HEAD:corpus/SOURCES.md`; uncommitted `corpus/SOURCES.md`; `LOG.md:3100`; `corpus/QUALITY.md:74` |
| G3 | med | **resolved** at `5a0435ff` | Stop record listed three counterexample seeds; producer recorded four. Addendum binds four with exact argv/UTC. Use the addendum, never the bare stop record, for the seed count. | `claim-stop.json:observed.seeds`; `claim-stop-addendum.json:decisive_receipts[0]`; `w1/ExecRedReproduce.md:81-85` |
| G4 | med | open | 34 wave-1 seats, no settle/provider record; registry members all `agentId: null`. "34/34, 0 dead, 0 holds" is UNPROVEN; all 34 reports are landed, which is a different fact. | `w1-spec.json`; `w1/swarm-registry.json`; `w1-payload.json` |
| G5 | med | open | "Five independent seats produced structure-blind readers" overstates: the met-target set is two committed-source classes (nameset, payload) plus at least six report-only variants, one of which is a scribe draft. "Five" is a floor; name the seats and mark the provenance. | `claim-stop-addendum.json:classes_without_committed_source`; `w1/*.md` |
| G6 | med | open | `green_positive_meets_target` is never the failing clause of any shipped control or mutant; one of the six clauses is asserted, never discriminated. Do not call it exercised. | `controls/*.json`; `w1/MutCounterClauses.md:137` |
| G7 | low | open | The registered `fixed-slice` reader is a printable-run scanner, not a fixed-slice replay; "seven shortcut classes" overstates the registry even before the unregistered classes. | `w1/CritCounterLimits.md:37-38`; `tools/round-34/gate-config-mini.json:15` |
| G8 | low | open | The lander knowledge entry points at a wave-2 file for one class lineage; the wave-2 file postdates it. Replace after settle. Also: a 0-byte untracked knowledge file was removed before 07:37:12Z; do not re-land it empty. | knowledge entry class table; `corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` (0 bytes) |
| G9 | low | open | Census start/end artifacts carry no exit code; "both exit 0" is prose over artifacts that print `ok`. | `census-start.txt`; `census-end.txt`; `LOG.md:3100` |
| G10 | info | open | Axis-label conflict C1 (depth vs operability) is live between committed files. Preserve verbatim; do not resolve. | `w1/CritAxisFit.md:234-239`; `claims.json:claims[0].axis`; `SCORECARD.md:3353` |
| G11 | info | open | Wave 2 unsettled at the cutoff; ten reports landed in `5a0435ff`, more in flight. No falsification verdict before settle. | `w2-spec.json`; `w2/` |
| G12 | med | disclosed | Four of the met-target classes have no committed source; they may be reported only as report-only scores. | `claim-stop-addendum.json:classes_without_committed_source` |
| G13 | low | disclosed | "Reads no header" was the wrong blindness test; blindness is content-contingent. Use the addendum's wording (decodes no header field, no record entry, no `name_off`). | `claim-stop-addendum.json:wording_corrections[0]`; `nameset.py:48-55` |
| G14 | info | preserved | Predicate-site count has two readings: `predicate-reconciliation.json` treats `P34-mini-records` as a separate namespace; the QUALITY correction counts it as a third scoring site. Report both, pick neither. | `predicate-reconciliation.json:sites.C_mini_counter`; `corpus/QUALITY.md` corrections |

---

## 8. Commands run by this seat (exact argv, exit, UTC)

Read-only throughout; cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless shown. No reader,
counter, gate, fixture or carrier executed. No install.

| UTC | argv | exit | result |
|---|---|---|---|
| 07:28:00Z | `git log --oneline -15` | 0 | HEAD then `cd75b92e` |
| ~07:30Z | inline `python3`: sha256 of `claims.json` and `nameset.py`; `instruments.json.instruments == claims[0].pins`; sha256 of predicate A (claims) and B (after receipt) | 0 | claims `de3afbfb…` = declared; pins equal, 26; A `7c6c17f0…`/31 words; B `8340aea5…`/46 words; nameset `2e8feaea…` = declared |
| ~07:30Z | `git cat-file -e ec3125ad:tools/round-34/replay-gate.py` | 128 | absent at base |
| ~07:30Z | `git cat-file -e c79bbe7b:tools/round-34/replay-gate.py` | 0 | present at freeze |
| ~07:30Z | inline `python3` over `controls/*.json` | 0 | exits 2/1/1/1/1, all `met_target=False`, failing clauses as tabled |
| ~07:30Z | `sha256sum`, `wc -c`, `sed -n '14149p'`, `sed -n '14056,14060p;14072,14076p;14102,14106p'` on `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/readelf-2_47.c` | 0 | `7e81eedf…`, 689,644 B, quote line and record-walk lines as cited |
| 07:31:56Z | `date -u` + `git diff -- LOG.md SCORECARD.md` | 0 | first observation of the live doc appends |
| 07:31:59Z | inline `python3` row-id diff, working tree vs `HEAD:corpus/SOURCES.md` | 0 | 105 vs 105; missing `S105`, added `S106` |
| 07:32:42Z | inline `python3` over `w1-spec.json` and `w2-spec.json`; `ls w2/*.md` | 0 | w1 34 seats, w2 32 seats, w2 reports 0 at that instant |
| 07:33:19Z | `git log --oneline -6`, `git status --porcelain`, `git show --stat 66b84027` | 0 | HEAD `66b84027`; deltas as listed |
| 07:33:28Z | row-id diff again; `cat census-end.txt \| tail -1` | 0 | 106 vs HEAD 105, `S105` added in tree; census end `ok`, 9 W04 |
| 07:35:30Z | `git log --oneline -4`, `git show --stat HEAD`, `git show HEAD:corpus/knowledge/…stop.md \| wc -l`, `grep -n "1,979" w1/CritCounterLimits.md` | 0 | new HEAD `5a0435ff`; knowledge entry 73 lines; probe E gate size at `w1/CritCounterLimits.md:93` |
| 07:36:07Z | `date -u`, `git status --porcelain`, row-id diff, `sed -n '112,122p' corpus/QUALITY.md` | 0 | HEAD 105 rows (S105 absent), tree 106 (S105 restored); QUALITY corrections text read |
| 07:37:12Z | `sha256sum w1/CtlMultiset-files/nameset-green-receipt.json w1/CtlMultiset-files/payload-keyed-receipt.json`; `wc -l claim-stop-addendum.json after/freeze-integrity-instruments.txt` | 0 | receipts `fa6e8f09…` and `23e26fe4…` = addendum; addendum 96 lines; pin receipt 27 lines (26 `ok` rows + summary); the 0-byte knowledge file is gone |

Taken as given rather than re-derived (marked so the L1 can decide): the 30-field receipt identity
in `w1/ExecRecountC2.md`, the strace counts in `w1/RevR34C1Untouched.md` (183 execve), the
prior-art/lead classification in `w1/ScoutWebReplayPriorArt.md`, and the wave-2 reports' own
measurements (they are peers' evidence, not mine).

---

## 9. Out of scope for this seat

Did not: run the gate, counters, any reader or any fixture; re-run wave-1 or wave-2 measurements;
mutate the repo, `claims.json`, `claim-stop.json`, `claim-stop-addendum.json`, frozen instruments,
corpus/SCORECARD/LOG/SKILL docs; clone or copy the lane into scratch (every probe was read-only
over existing bytes); touch any sibling lane, the fleet root, `~/.omp`, `~/.config`,
`~/.kimi-code`; message other seats. Wave-2 verdicts, seal and scorecard credit belong to other
seats.

**Final verdict line:** `SKELETON_DRAFTED` — six sections drafted at HEAD `5a0435ff`
(2026-10-25T07:35:33Z) with a per-claim pointer; 14 findings recorded, of which **G2 (S105 still
dropped from `corpus/SOURCES.md` at HEAD, restore uncommitted)** must be resolved before filing,
G4/G5/G6/G12 must qualify the "34/34 seats" and "five classes" wording, and G1/G3 are resolved by
`5a0435ff` and should be cited from that commit, not from the bare stop record; wave 2 is
unsettled, so no falsification verdict on the stop is offered here.
