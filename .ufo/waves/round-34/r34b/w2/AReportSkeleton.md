# AReportSkeleton — fleet-report drafts for round 34, run-6 re-dispatch (R34-C2 stop)

Seat `L1Kaidoku34-2.AReportSkeleton` (scribe, wave 2). Assignment: draft the fleet report's
`Work performed`, `Landed changes`, `Before -> after measurements`, `Sources & frontier`,
`Trend verdicts` and `SHONEN` sections for this attempt, with an evidence pointer per claim, and
mark anything not groundable in committed bytes **UNPROVEN** instead of inventing a pointer.

Axes named for this seat: **evidence fidelity** (pointer resolves to the bytes that carry the
claim), **pointer completeness** (no claim without a location), **non-overclaim** (unlanded work
never described as landed), **conflict preservation** (contradictions reported verbatim, not
resolved).

## 0. Observation cutoff and conventions

- **Cutoff HEAD:** `66b84027` (`2026-10-25T07:33:19Z`), parent `cd75b92e`
  (`git log --oneline -6`, run 07:33:19Z, exit 0).
- The L1 was **still landing** while this report was written: `66b84027` appeared between two
  of my `git status` calls, and three corrections (`corpus/SOURCES.md` +1 line restoring S105,
  `corpus/QUALITY.md` row 73→74, `corpus/lessons/round-34.md` M34-12) were uncommitted at
  07:33:28Z. Everything below is stated **at the cutoff**; nothing uncommitted is described as
  landed. Where the working tree differs, it is named as a working-tree delta with its own
  pointer.
- Paths are relative to `kaidoku-shokunin/.ufo/waves/round-34/r34b/` unless they start with
  `corpus/`, `tools/` or `SKILL.md`/`LOG.md`/`SCORECARD.md` (relative to the lane root).
- **UNPROVEN** means: I could not resolve the claim to committed bytes at the cutoff. It is not
  a claim that the work is false — only that the report may not cite it as evidence until a
  pointer exists.
- I executed no reader, counter, gate, fixture or ELF carrier. My probes were read-only
  (`git` read subcommands, `sha256sum`, `wc`, `sed -n`, `grep`, inline `python3` over static
  bytes). No tool installed, upgraded or removed. Exact commands, exits and UTC in §8.

---

## Draft 1 — Work performed

**One claim this round: R34-C2, recorded as capability acquisition on axis depth**
(`claims.json:claims[0].axis`, `:claims[0].type`; the axis label is contested — see conflict C1).
The surface is a pre-freeze shortcut-replay gate that makes the prior round's QUALITY 67
executable (`corpus/QUALITY.md:77`). Predicate `P34-shortcut-replay` in the claim file: 31 words,
sha256 `7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b`
(`predicate-reconciliation.json:sites.A_claims_and_configs`; recomputed by me, §8). Target 8,
six clauses `gate_present`, `selftest_clean`, `mutants_killed`, `red_refused`, `green_clean`,
`green_positive_meets_target` (`tools/round-34/c2-shortcut-gate-counter.py:112-120`).

**Freeze before any of its data.** `c79bbe7b0959132b9873ff3431cf5eb313b58b33`, 27 files,
1345 insertions, 0 deletions (`git show --stat c79bbe7b`; independently recounted in
`w1/RevFreezeOrder.md:57`): the gate `tools/round-34/replay-gate.py` (313 lines), the six-clause
driver `tools/round-34/c2-shortcut-gate-counter.py` (137), red and green configs, eight
synthetic 512-byte `MREC` fixtures, `expected.json` (25 records), eight readers including the
structural positive control, `mini-fix/spec.json`, and 26 pins in `claims.json:claims[0].pins`.

**Before.** `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…`, exit 2
(`before/c2-at-base.txt:1`). Reproduced independently: `git cat-file -e
ec3125ad:tools/round-34/replay-gate.py` exits 128, the same path at `c79bbe7b` exits 0 (§8).

**Production (the gate, not a reader).** `GATE_COUNTER_OK finding=shortcut_gate_discriminates
selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN
green_positive_matched=8 clauses_failed=-`, exit 0 at `c79bbe7b`
(`after/c2-at-instruments.json`; `after/c2-at-instruments.txt:1`). Green: CLEAN, 8 matched,
7 classes below target; red: REFUSED naming `label-memorization`; selftest 12 cases, 3/3 mutants
killed (`after/c2-at-instruments.json:clauses, selftest_line`).

**Five controls, all MISS** (`controls/*.json`, exits read from the receipts):

| control | exit | failing clauses |
|---|---|---|
| do-nothing (`--root` without gate) | 2 | none reported — `gate_absent`, no clause block |
| always-clean gate | 1 | `red_refused`, `selftest_clean` |
| junk clean-printing stub | 1 | `red_refused` |
| no-positive-check gate | 1 | `mutants_killed`, `selftest_clean` |
| vacuous gate without the shortcut floor | 1 | `selftest_clean` |

**Wave 1 — the first falsifiers.** 34 seats in one validated `task` call
(`w1-spec.json`, `w1-seat-map.json`): executor 7, reviewer 6, scribe 5, mutation-tester 4,
critic 4, scout 3, sentinel 2, revenger 2, connector 1. 33 seat reports exist at the cutoff; the
34th seat, `CritControlAdequacy`, has a prompt and **no report**, and the wave has **no settle or
provider-provenance record** (all 34 `w1/swarm-registry.json:members` entries carry
`agentId: null`; `w1-payload.json` holds only name/role/task). Seat outcome accounting for this
wave is therefore **UNPROVEN** (finding G4).

**Stop.** The green surface's only perturbation is a per-run name-pool permutation, so record
order, count, every `flags`/`value` byte and the name multiset survive it. A content-multiset
memoriser (`w1/CtlMultiset-files/nameset.py`, sha256
`2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`, recomputed by me) reads no
header, no record entry and no `name_off` (source header `nameset.py:9-15`; key construction
`:49-55`) and scores **8/8** on the green counter. The producer seat recorded four green seeds
(default, `alt-1`, `alt-2`, `alt-3`: `w1/ExecRedReproduce.md:81-85`); the stop record lists three
(`claim-stop.json:decisive_counterexample.observed.seeds`) — an undercount, not a contradiction
(finding G3).

**Further unregistered classes at 8/8** (each an executed receipt in its report, not a
projection):
- payload-keyed, every name byte NUL-ed: `matched=8` at five seeds, with `structural.py` at 0/8
  on the same bytes (`w1/LabratSeedSensitivity.md:132`, `:135-138`);
- fixed-slice+memorised payload hybrid `s2d_fixed_slice_offsets_memo`, and record-signature
  `s2b_record_sig`: `w1/MutShortcutClasses.md:100`, `:107`;
- name-pool keyed `s2b_string_name_keyed` / `s2c_string_pool_noheader`:
  `w1/MutShortcutClasses.md:104-105`;
- prefix-keyed reader: `matched=8 target=8 met_target=True`, exit 0
  (`w1/CritCounterLimits.md:32`);
- topology-keyed (scribe probe, not an independent executed control):
  `w1/ScribeKnowledgeEntry.md:127-133`.

**Registration, not the mechanism, was the hole.** Registering a class flips the same gate:
payload probe → `REPLAY_GATE_REFUSED`, exit 2 (`w1/LabratSeedSensitivity.md:143-145`);
`prefix-keyed` → `REPLAY_GATE_REFUSED`, exit 2 (`w1/CritCounterLimits.md:34`). Two roster defects
compound it: the registered `fixed-slice` reader is a printable-run scanner, not a fixed-slice
replay (`w1/CritCounterLimits.md:37-38`), and the class drop to `MIN_SHORTCUTS=3` still prints
CLEAN (`w1/RevPredicateIdentity.md:75`; `tools/round-34/replay-gate.py:31,58`).

**Record defects F1–F5, disclosed not repaired** (`claim-stop.json:record_defects_disclosed`):
pins live under `claims[0].pins` and no instrument hashes them (F1); the frozen
`predicate_identity` is false, A=31 words vs B=46 words (F2; `predicate-reconciliation.json`;
both digests recomputed by me); class drop invisible (F3); mutant M3 survives its own selftest and
turns the red case CLEAN (F4, `w1/MutGateBranches.md` — landed at `66b84027`); receipts were
untracked at first audit (F5, repaired by `b917ea64`). Repairs landed: 26-pin container
`instruments.json`, byte-identical to `claims[0].pins` (my check: dict equality true, 26 entries),
and the receipt set.

**Disclosed instrument limits** (each with a committed pointer): `met_target` trusted and never
cross-checked with `matched` (`replay-gate.py:93-101,119-127`; `w1/CritCounterLimits.md:52`);
per-reader rows dropped at the gate boundary (`replay-gate.py:100`;
`w1/CritCounterLimits.md:53`); a crashing reader scored "below target"
(`w1/CritCounterLimits.md:54`); refusal filtered by free-text class label
(`replay-gate.py:123`; `w1/RevengerGateFailModes.md` D1); the floor is not an equality
(`replay-gate.py:31,58`); a gate that runs no reader satisfies all six clauses
(`w1/CritCounterLimits.md` probe E); `--rev` is a pure echo (`c2-shortcut-gate-counter.py:67,73`;
`w1/ExecRecountC2.md` F2); readers are arbitrary uid-1000 code and the clean verdict cannot
absorb that (`w1/SentinelContainment.md:147-151`); one fixture format, one size class
(`w1/ExecGreenIndependence.md:162`), and fixture↔expected agreement is tautological because
`expected.json` derives from the writer's spec (`w1/ExecGreenIndependence.md:139`); trailing NUL
padding lets single-record fixtures draw the identity permutation (18/5000 beta, 13/5000 epsilon:
`w1/ExecPermuteAudit.md:147-155`).

**Wave 2 (this wave) is not settled at the cutoff.** 32 seats (`w2-spec.json`: reviewer 10,
critic 6, executor 6, scribe 5, mutation-tester 2, sentinel 1, connector 1, revenger 1); zero
reports at `2026-10-25T07:32:42Z`, the first appearing immediately after. No wave-2 verdict may
enter this report until the wave settles; a report filed before settle must say so (finding G11).

**Inherited claim untouched.** R34-C1's five frozen artifacts are byte-identical from
`54a87a51` and its reader/carriers were not executed (`w1/RevR34C1Untouched.md:120-122`:
183 execve, every one `/usr/bin/python3`, all fixtures static). R34-C1 is not reopened,
re-scored or relabelled (`claims.json:retained_claim`).

---

## Draft 2 — Landed changes

Four commits carry this attempt. All are in `main` at the cutoff; author/committer identity is
not re-asserted here (not re-checked by me).

| commit | content | report/LOG anchor |
|---|---|---|
| `c79bbe7b0959132b9873ff3431cf5eb313b58b33` | the freeze: `claims.json` (90 lines), gate, six-clause counter, two configs, eight fixtures, nine readers, `spec.json`, `expected.json` — 27 files, +1345/−0 | `claims.json`; `LOG.md:3094-3103` (round block) |
| `b917ea64ebbeab49b8258d71ffb34e700715ffe6` | after the wave-1 record audits: before/production/control receipts (13 files), `instruments.json`, `predicate-reconciliation.json`, `w1-payload.json`, `w1-seat-map.json`, `w1-spec.json`, the then-written w1 reports, all 30 prompts, `w1/swarm-registry.json`, the id-assimilation guard (105 registered vs 132 staged ids, `assimilation/collisions` empty) — 77 files, +6001 | `LOG.md:3094-3103`; `w1/ExecRecountC2.md:132` (F6) |
| `cd75b92e583735729546b0ea3b250f2df6d0652a` | the stop: `claim-stop.json` (87 lines), `w1/CtlMultiset-files/{nameset,pathkey,mini-counter-fresh}.py` — 4 files, +352 | `LOG.md:3098-3100`; `SCORECARD.md:3347-3369` |
| `66b84027` (subject: "land the stopped claim's record …") | SCORECARD run-6 section (+26), LOG run-6 block (+11), lesson M34-5..M34-11, QUALITY 68-73 (+6), SKILL instrument registry (+14), S106 row, knowledge entry, README rows (+4), all 26 remaining w1 reports, `census-start.txt`, `w2-spec.json`, `w2-seat-map.json`, 32 w2 prompts | `SKILL.md:1209-1222`; `corpus/QUALITY.md:78-83`; `corpus/SOURCES.md:111`; `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`; `SCORECARD.md:3347`; `LOG.md:3094` |

**Inherited state.** Base `ec3125ad3d130d92f888a4128dfaa2982f36fff7`; the attempt-1 (R34-C1)
stop is inherited through `f432c8e3` and is not rewritten (`claims.json:inherited_tip`;
`SCORECARD.md:3349`). `corpus/lessons/round-34.md` gained the new attempt as an appended section;
the attempt-1 text is untouched.

**Working-tree deltas at the cutoff — NOT landed, must not be reported as landed:**
`corpus/SOURCES.md` (+1 line restoring S105), `corpus/QUALITY.md` (row 73 → 74), 
`corpus/lessons/round-34.md` (+M34-12), `census-end.txt`, `w1-validator-stderr.txt` (0 bytes),
`corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` (0 bytes, untracked), and
the whole `w2/` tree. `git status --porcelain` at 07:33:19Z is the pointer.

**Defect landed with this attempt (finding G2).** At `66b84027`, `corpus/SOURCES.md` holds 105
rows with S105 **absent** and S106 present; the L1's own row-id recount and the restoration are
in the uncommitted delta and are already disclosed as M34-12 ("the S106 edit used the S105 row as
its anchor and overwrote it"). The report must either land the restoration before filing or state
the swap as an open defect — it may not print the LOG's "rows 105→106" as fact at `66b84027`.

**Repair asserted but not landed (finding G1).** `claim-stop.json:record_defects_disclosed[0]`
says the F1 repair is `instruments.json (byte-identical 26-pin container) + freeze-integrity
receipt over it`; `corpus/QUALITY.md:78` says the same tool prints CLEAN on it; `SKILL.md:1221`
repeats "26 pins, CLEAN". No such receipt exists anywhere in the lane at the cutoff, and no seat
report shows that run: `w1/RevClaimsVsInstruments.md:63` ran the **C1** map (`--round 34`,
`CLEAN pins=21`), and `w1/RevFreezeOrder.md:174` states it did not re-run the tool. The pin set
is genuinely equal to the frozen map (my check, §8), so the container is sound; the **receipt
claim** is UNPROVEN. Either retain the receipt or drop the "receipt" and "CLEAN" wording from all
three sites before filing.

---

## Draft 3 — Before → after measurements

Counting command (unchanged): `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root
<LANE> --rev <REV> --json-out <RECEIPT>` (`claims.json:claims[0].counting_command`;
`SCORECARD.md:3352`). A control run adds `--gate <alternative gate>` and `--rev` naming the
revision it claims.

| claim / surface | before | after | measured revision | verdict |
|---|---|---|---|---|
| R34-C2 / depth — pre-freeze shortcut-replay gate making QUALITY 67 executable | `GATE_COUNTER_UNEVALUABLE finding=gate_absent`, exit 2 (`before/c2-at-base.txt:1`) | `GATE_COUNTER_OK … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit 0 (`after/c2-at-instruments.json`; `.txt:1`) | before `ec3125ad`; after `c79bbe7b` | **falsified measure / honest stop** — an unregistered structure-blind class reaches the green 8/8 |

**Decisive counterexample (a control score, never the production reader's score).**
`nameset.py`, sha256 `2e8feaea…`, green `matched=8 met_target=true`, exit 0, at three seeds in
the stop record and four in the producer report (`claim-stop.json`; `w1/ExecRedReproduce.md:81-85`).
Four further classes reach the same target (§Draft 1). Each is a score under the counter's own
predicate, not a capability result.

**Gate controls** (exit, clause failures) — table in Draft 1; all five MISS, maximum 5 of 6
clauses. Caution for the report: no shipped control or mutant makes
`green_positive_meets_target` the **failing** clause, so that clause is asserted but never
discriminated (`controls/gate-no-positive-check.py.txt` fails `mutants_killed,selftest_clean`;
`w1/MutCounterClauses.md:137`). It must not be described as exercised.

**Owned scores stay 10→10, delta 0** (`claims.json:claims[0].scores_unchanged`): coverage
10→10, depth 10→10, calibration 10→10; `SCORECARD.md:3364-3368` records the same three rows.
No capability row entered and no exploratory relabel was made.

**Axis-label conflict (C1) — report verbatim, do not resolve here.**
`w1/CritAxisFit.md:234-239` returns `AXIS_FIT_FAIL depth`: "the surface R34-C2 actually moves at
`c79bbe7b` is a structural-counter admission *instrument* (operability, unowned proxy) with a
self-reported-verdict boundary, not `depth`". The claim file and `SCORECARD.md:3351` label the row
`depth`. Both are committed; the fleet report must carry the disagreement rather than pick a
side, and must not convert "six clauses met" into an axis gain.

---

## Draft 4 — Sources & frontier

- **Row counts — do not print 105→106 at this cutoff (G2).** At `66b84027`, `corpus/SOURCES.md`
  has 105 rows, ids S001–S106 with **S105 missing**; the working tree at 07:33:28Z has 106 with
  S105 restored. LOG.md:3100's "rows 105→106, all-A tier unchanged, malformed 0" describes the
  intended, not the landed, blob. Correct wording at the cutoff: "105 rows landed (S105 swapped
  out by the S106 insert; restoration in flight, M34-12)"; after the restoration lands:
  "105→106, tiers A 99→100, status mined 101→102, rejected 4→4, malformed 0" (the tallies in
  M34-12's own text: `A 99→99`, `rejected 4→3` at the first recount).
- **Rows added.** S106 only (`corpus/SOURCES.md:111` at `66b84027`): GNU binutils `readelf.c`,
  tag `binutils-2_47`, tier A, status mined, scope limited to the `SHT_GNU_verneed`
  section-header decode. Verified by me against the capture: sha256 `7e81eedf…`, 689,644 bytes,
  `:14149` carries `warn (_("Missing Version Needs information\n"));`, and the record walk at
  `:14056` (`endbuf`), `:14072-14076` (`vn_version…vn_next`), `:14102-14106` (aux fields) is as
  cited. **Provenance limit:** the capture lives only in
  `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/` — not in the lane; the row is
  verifiable only while that scratch survives.
- **Census.** `census-start.txt` (landed, `66b84027`) and `census-end.txt` (working tree) each
  show nine `W04` duplicate-URL warnings and a final `kaidoku ok …/corpus/SOURCES.md` line.
  Neither artifact records an **exit code**, so "both exit 0" (`LOG.md:3101`) is UNPROVEN as a
  retained receipt — the retained bytes are consistent with 0, nothing more (G9).
- **Quote counts.** No `quote-counts.json` for this attempt. The lesson draft states the S106
  quote is 6 contiguous words (`corpus/lessons/round-34.md:67`); there is no counted receipt in
  the lane, so the count is UNPROVEN.
- **Frontier.** No frontier row advanced. `w1/ConnectorFrontier.md:76` ("Which frontier bullet:
  **none**") and `:125` (gate home = SKILL registry only; not Core, not the bar). PROVINCE is
  unchanged — last commit `bb0af56c` (round-32), clean at the cutoff.
- **Sourced claim.** R34-C2's structure-language rests on S106, cited in the knowledge entry and
  in the SKILL limits paragraph (`SKILL.md:1221`).
- **Rejected / leads.** Prior-art candidates (Chakraborty, Kapoor & Narayanan, Fioraldi WEIZZ,
  Adebayo, Segura, Geirhos, tmp.0ut) stay **leads, not rows**, because no admitted entry cites
  them (`w1/ScoutWebReplayPriorArt.md:85-91`; lesson draft `:69`). S105 remains the retained
  rejected row for GNU Verneed/Vernaux authority — provided the restoration lands (G2).
- **Sibling overlap.** kake's `lookup_control_check.py` is the earlier instrument in this family,
  with tsukuroi, mado, chousa, kama and mori adjacent; cited, not absorbed
  (`w1/ScoutSiblings.md`, landed at `66b84027`). The "who owns the shortcut-class list" question
  is raised, not exercised (`w1/ConnectorFrontier.md:88`).
- **Knowledge entry.** `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`
  (landed, 73 lines). It correctly denies capability and lists the five classes. One pointer is
  forward-dated: one class lineage is attributed to `w1/ACounterexample2.md` — a wave-2 report
  that did not exist at the cutoff (G8). Replace with a settled wave-2 pointer after the wave
  lands, or drop that row.

---

## Draft 5 — Trend verdicts

- **expansion: unchanged.** No frontier row, no capability, no new domain ground. PROVINCE is at
  `bb0af56c` and clean; the only SKILL change is an instrument-registry row plus a limits
  paragraph (`SKILL.md:1209-1222`), which `w1/ConnectorFrontier.md:45,125` explicitly holds out
  of Core and out of the QUALITY bar.
- **quality: improved (author assessment; one advertised receipt is missing).** Against interest,
  the attempt disclosed a false predicate identity, an unenforced pin map, a class-drop hole, a
  surviving mutant, and an axis-fit objection; it landed five controls, a scoped source row and a
  per-limit pointer set. The improvement is real in the bytes but bounded: the F1 "receipt" does
  not exist (G1), the landed source edit dropped S105 (G2), one wave-1 seat has no report and the
  wave has no settle record (G4), and no admitted entry was re-checked in this attempt, so "no
  admitted entry failed re-check" is UNPROVEN. Phrase as "improved, with two record defects
  disclosed at filing" rather than an unqualified gain.
- **discernment: improved (author assessment; axis label contested).** The frozen rule was
  applied, not amended: no target, threshold, class, predicate or label changed after the freeze;
  the counterexample is published with its source digest and reproduced by an independent seat
  (`w1/ExecRedReproduce.md`; `w1/ExecRecountC2.md:143` `RECOUNT_C2_REPRODUCES`, 30/30 fields
  identical). The counter-signal the report must keep: the standing description of R34-C2 as a
  **depth** acquisition is itself contradicted by a committed seat (`w1/CritAxisFit.md:234`;
  conflict C1), and "six clauses met" is registry-relative
  (`w1/RevengerR34History.md:297`). Discernment credit is for stopping, not for the axis claim.
- **Inherited trend.** This is the fourth consecutive non-pass in the lane's series
  (r32 text-presence, r33 provider hold, r34 attempt-1 fixed-offset replay, r34 attempt-2
  unregistered class). That line already exists in the filed round-34 report and may be carried
  forward; it is context, not this attempt's measurement.

---

## Draft 6 — SHONEN

- [~] **SKILL.md contains real decision tables, error patterns, checklists, cited sources** —
  advanced this attempt by the instrument-registry row, the three verdict/exit rows and the
  limits paragraph (`SKILL.md:1209-1222`), landed at `66b84027`, with S106 as the citation
  (`corpus/SOURCES.md:111`). Not earned: the registry's "26 pins, CLEAN" clause cites a receipt
  that is not retained (G1), and no non-author has exercised the paragraph.
- [~] **At least one end-to-end domain task executed and logged in LOG.md** — unchanged: still
  rests on the historical round-1 libjq task; this attempt executed an instrument-only harness on
  eight synthetic fixtures, ran no carrier and no production reader
  (`claims.json:instrument_notes.no_production_reader_run`; `w1/RevR34C1Untouched.md:120-122`).
- [~] **Instructions executable by an agent without oral context** — improved: the one-line
  counting command, the gate argv and its exit codes are written out
  (`claims.json:claims[0].counting_command`; `SCORECARD.md:3352`; `SKILL.md:1215`). Not earned:
  following the command reproduces a verdict but cannot verify the claim's own identity — pins
  are declared rather than read (F1) and the predicate sentence differs between claim and
  receipt (F2, `predicate-reconciliation.json`).
- [~] **No cross-domain bleed (PROVINCE.md still accurate)** — PROVINCE unchanged (last commit
  `bb0af56c`; clean at the cutoff); scope audit returns `SCOPE_CLEAN_NO_PREEXISTING_HARM`,
  27 additions/0 deletions confined to `tools/round-34/**` + `.ufo/waves/round-34/**`
  (`w1/RevScopeNoHarm.md:257-260`). The adjacent **ownership** question (who owns the
  shortcut-class list, a CLEAN being config-relative) is raised and left to PROVINCE's Adjacent
  bucket (`w1/ConnectorFrontier.md:88`); raised, not exercised — no bleed.

---

## 7. Findings the L1 must handle before filing

| id | severity | finding | pointer |
|---|---|---|---|
| G1 | **high** | The F1 repair's "freeze-integrity receipt over `instruments.json`" is asserted in the stop record, QUALITY 68 and SKILL, but no such receipt exists in the lane and no seat reports that run. The container equality is true (my check); the receipt claim is UNPROVEN. | `claim-stop.json:record_defects_disclosed[0].repair_landed`; `corpus/QUALITY.md:78`; `SKILL.md:1221`; `w1/RevClaimsVsInstruments.md:63`; `w1/RevFreezeOrder.md:174` |
| G2 | **high** | Landed `66b84027` replaced the S105 row with S106: 105 rows, S105 absent, so "rows 105→106" and "no existing row cell was touched" are false at HEAD. Restoration is in the working tree and disclosed as M34-12. | `git show 66b84027 -- corpus/SOURCES.md`; `LOG.md:3100`; uncommitted `corpus/SOURCES.md`/`QUALITY.md`/`round-34.md` |
| G3 | med | The stop record lists three counterexample seeds; the producer recorded four green seeds. Wording undercounts its own evidence. | `claim-stop.json:observed.seeds`; `w1/ExecRedReproduce.md:81-85` |
| G4 | med | 34 wave-1 seats, 33 reports (`CritControlAdequacy` missing); no settle/provider record for the wave; registry members all `agentId: null`. Any "34/34, no dead seats" phrasing is UNPROVEN. | `w1-spec.json`; `ls w1/*.md`; `w1/swarm-registry.json`; `w1-payload.json` |
| G5 | med | "Five independent seats produced structure-blind readers" overstates the count: four executed seats plus one scribe draft. Name them or say four. | `w1/ExecRedReproduce.md`, `w1/LabratSeedSensitivity.md`, `w1/MutShortcutClasses.md`, `w1/CritCounterLimits.md`, `w1/ScribeKnowledgeEntry.md` |
| G6 | med | `green_positive_meets_target` is never the failing clause of any shipped control or mutant, so the six-clause target contains one clause asserted but never discriminated. Do not call it exercised. | `controls/*.json`; `w1/MutCounterClauses.md:137`; `controls/gate-no-positive-check.py.txt` |
| G7 | low | The registered `fixed-slice` reader is a printable-run scanner, not a fixed-slice replay; "seven shortcut classes" overstates what was registered even before the unregistered classes appeared. | `w1/CritCounterLimits.md:37-38`; `tools/round-34/gate-config-mini.json:15` |
| G8 | low | The landed knowledge entry cites `w1/ACounterexample2.md` (a wave-2 file) for one class lineage; absent at the cutoff. | `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` (class table) |
| G9 | low | Census start/end artifacts carry no exit code; "both exit 0" is a prose claim over artifacts that print `ok`. | `census-start.txt`; `census-end.txt`; `LOG.md:3101` |
| G10 | info | Axis-label conflict C1 (depth vs operability) is live between committed files. Preserve verbatim; do not resolve. | `w1/CritAxisFit.md:234-239`; `claims.json:claims[0].axis`; `SCORECARD.md:3351` |
| G11 | info | Wave 2 is unsettled at the cutoff (0 reports at 07:32:42Z). No wave-2 verdict, "falsified" or "sustained", may be written before settle. | `w2-spec.json`; `w2/` |

---

## 8. Commands run by this seat (exact argv, exit, UTC)

All read-only; cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless shown. No reader,
counter, gate, fixture or carrier was executed. No install occurred.

| UTC | argv | exit | result |
|---|---|---|---|
| 07:28:00Z | `git log --oneline -15` | 0 | HEAD then `cd75b92e`; base lineage visible |
| ~07:30Z | inline `python3`: sha256 of `claims.json`, `nameset.py`; equality of `instruments.json.instruments` vs `claims[0].pins`; sha256 of predicate A (claims) and B (after receipt) | 0 | claims `de3afbfb…` = declared; pins equal, 26; A `7c6c17f0…`/31 words; B `8340aea5…`/46 words; nameset `2e8feaea…` = declared |
| ~07:30Z | `git cat-file -e ec3125ad:tools/round-34/replay-gate.py` | 128 | absent at base |
| ~07:30Z | `git cat-file -e c79bbe7b:tools/round-34/replay-gate.py` | 0 | present at freeze |
| ~07:30Z | inline `python3` over `controls/*.json` | 0 | exits 2/1/1/1/1, all `met_target=False`, failing clauses as tabled |
| ~07:30Z | `sha256sum`, `wc -c`, `sed -n '14149p'`, `sed -n '14056,14060p;14072,14076p;14102,14106p'` on `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/readelf-2_47.c` | 0 | `7e81eedf…`, 689,644 B, quote line and record-walk lines as cited |
| 07:31:56Z | `date -u` + `git diff -- LOG.md SCORECARD.md` | 0 | first observation of the live doc appends |
| 07:31:59Z | inline `python3` row-id diff working tree vs `HEAD:corpus/SOURCES.md` | 0 | 105 vs 105; missing `S105`, added `S106` |
| 07:32:42Z | inline `python3` over `w1-spec.json`, `w2-spec.json`; `ls w2/*.md` | 0 | w1 34 seats / w2 32 seats; w2 reports 0 |
| 07:33:19Z | `git log --oneline -6`, `git status --porcelain`, `git show --stat 66b84027` | 0 | HEAD `66b84027`; deltas as listed in Draft 2 |
| 07:33:28Z | inline `python3` row-id diff again; `cat census-end.txt \| tail -1` | 0 | 106 vs HEAD 105, `S105` added in tree; census end `ok`, 9 W04 |
| ~07:33Z | `grep -n` / `nl -ba` reads of the w1 reports, `SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md` | 0 | pointers cited above |

Assertion costs I took as given rather than re-derived (marked so the L1 can decide): the
`[INFERENCE]`-free parts of `w1/ExecRecountC2.md` (30-field receipt identity), the strace counts
in `w1/RevR34C1Untouched.md` (183 execve), and the prior-art/lead classification in
`w1/ScoutWebReplayPriorArt.md`.

---

## 9. Out of scope for this seat

Did not: run the gate, the counters, any reader or any fixture; re-run wave-1 measurements;
mutate the repo, `claims.json`, `claim-stop.json`, frozen instruments, corpus/SCORECARD/LOG/SKILL
docs; clone or copy the lane into scratch (every probe was read-only over existing bytes); touch
any sibling lane, the fleet root, `~/.omp`, `~/.config`, `~/.kimi-code`; message other seats.
Wave-2 verdicts, seal, and scorecard credit are other seats' assignments.

**Final verdict line:** `SKELETON_DRAFTED` — six sections drafted at HEAD `66b84027`
(2026-10-25T07:33:19Z) with per-claim pointers; 11 findings recorded, of which G1 (unretained
freeze-integrity receipt asserted in three landed docs) and G2 (landed S105→S106 swap, repair
uncommitted) must be resolved before the fleet report is filed; wave 2 unsettled, so no
falsification verdict on the stop is offered here.
