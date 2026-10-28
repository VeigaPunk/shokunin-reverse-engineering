# kaidoku-shokunin — Scorecard

## Current assessment — 2026-10-15, operator-steered round 1

One move: **calibration**, reconciling the current assessment with landed REA
work. Historical rounds 1–14 retain their original numbering. The previous
scorecard is preserved at `6645585873c4e66372b15687c47000abf8d91978:SCORECARD.md`;
its expired round-5 snapshot is not the current work queue.

The legacy card recorded **no numeric axis scores**. The baseline below is a
retrospective measurement, not an old score recovered from history. `[INFERENCE]`
calibration is the lowest axis under these heterogeneous, bounded proxies;
this comparison is not a calibrated ranking of domain expertise. Numeric axis
fields satisfy fleet `AXES.md:33-39`; learning-trend verdicts remain nonnumeric.

Line citations to pre-existing lane files refer to the baseline revision unless
explicitly marked current; the added lesson-index row shifts later README lines.

## Owned axes

| Axis | Baseline → current score, 0–10 | Observable and limitation | Evidence / counting command | Last-change round |
|---|---|---|---|---|
| coverage | 9.72 → 10.0 | 138/138 knowledge files mapped after the round-41 landing (three entries added and mapped: `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`, `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`, `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md`; command A at `e1c83313`, `missing []`, `dangling []`; R41-C1 moved genuine AVM-layout BE SquashFS v4 Frontier → Core, `## Round 41` below); 130/130 knowledge files mapped after the round-40 landing (two entries added and mapped: `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`; command A at `4d62ee5a`, `missing []`, `dangling []`, `.ufo/waves/round-40/w2/R40W2DepthCount.md`); 128/128 after the round-39 landing (two entries added and mapped: `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`, `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`; 126/126 after the round-38 landing, which added `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`, `corpus/knowledge/2026-10-26-unblob-format-matrix.md`; 124/124 after the round-36 landing, which added `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`; 122/122 at `cab59f221fe19726b5692bfa4d9a9679e96b8a73`, round 36 recount with the command-A observable in `tools/round-36/c2-counter.py`; 116/116 at `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31; 109/109 at `ebe2cb4a`, round 26); index integrity only, **not** fraction of the REA domain held. History: 78/78 at `3395b6d` (luna-round-7; the row kept that revision until round 26), 107/107 at `7ef837a473ae65d924b9ea34e7748f722a6cd7d5`, 108/108 after the round-25 EVM selector-naming entry | `corpus/README.md` `## Coverage map`; command A (`tools/round-38/c2-counter.py`); measured after the round-39 landing (command A at `52b0eb2907c704ed5f184c47b14c723208e5cbbc`, `missing []`, `dangling []`) and after the round-38 landing (`plans/round-38-claims.md` R38-C2) and after the round-36 landing (round 36, `plans/round-36-claims.md` R36-C2); `cab59f221fe19726b5692bfa4d9a9679e96b8a73`; earlier `c369242fee9f559f895e3f7956b1242076c7b1be` (round 31, `.ufo/waves/round-31/w1/ScribeScorecardRows.md`); baseline `a79945c4` | luna-round-1 + luna-round-7; count refreshed rounds 25, 26, 31, 36, 38, 39 and 40 |
| depth | 10 → 10 | 23/23 queue-drain rule blocks have resolvable file/range citations at `e1c83313f33a3d97edbd8fef402db2d06172fcdc` (round 41, command A, new block 20 at `SKILL.md:387-449` with table v3; craft section `SKILL.md:81-449`; R41-C2 itself stopped, `## Round 41`); 19/19 queue-drain rule blocks have resolvable file/range citations at `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` (round 40, command A, new block 19 at `SKILL.md:348-375` with table v2; `.ufo/waves/round-40/w2/R40W2DepthCount.md`); 18/18 at `52b0eb2907c704ed5f184c47b14c723208e5cbbc` (round 39, command A, `citation_resolved_rules 18`, new block 18 at `SKILL.md:316-343` with its citations resolving; 17/17 at `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31; also 17/17 at `ebe2cb4a`, round 26). History: 9/9 at `638fb211` (luna-round-3); rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and 2026-10-19), and the row kept 9/9 until round 25 added a recount at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. **not** semantic correctness, generality, or fresh execution — the r3 semantic contradiction removal is measured by the contradiction census, not this proxy | craft section `SKILL.md:81-343` (heading line 81, last non-blank line 343 at `52b0eb29`; the baseline range was `SKILL.md:77-191` at `a79945c4`); command A; measured `52b0eb2907c704ed5f184c47b14c723208e5cbbc` (round 39; prior recount `c369242fee9f559f895e3f7956b1242076c7b1be`, round 31); baseline `a79945c4` | r1 measurement + luna-round-3; rule blocks added 2026-10-18 and 2026-10-19; count refreshed rounds 25, 26, 39 and 40 |
| calibration | 0 → 10 | 9/9 preselected reconciliation obligations aligned (2026-10-15); 2026-10-16 per-client REA surface reconciled to live receipts — **failure-selected completeness**, not unbiased accuracy or mastery | Frozen `evidence/round-1-2026-10-15/rubric.json`; command B; count measured at `c265db9bd3c0883fbaf4487f839559c85a736826` (`evidence/round-1-2026-10-15/result.json` `measured_revision`; the row said `75af886a` until round 26, which is the luna-round-2 receipt reconciliation, not command B's revision); luna-round-2 receipts `.ufo/waves/luna-round-2/receipts/` | operator-steered r1 + luna-round-2; later calibration claims are in the round sections (outside closures: round 24 rejected-honest-stop, round 25 admitted) |

Baseline source revision: `6645585873c4e66372b15687c47000abf8d91978`.
`result.json` records the post-change source commit, observations and reviews;
the later bookkeeping commit records that measured revision without circularly
claiming to contain its own hash. Scores use `round(10 * numerator / denominator, 2)`.
A perfect finite proxy retires no domain axis and closes no promotion gate.

## Reconciled current state

The nine obligations were frozen before edits. Their detailed old locations,
expected states and independent pre-existing sources are in `rubric.json`.
They are assessment obligations, not nine independent domain discoveries.

| ID | Current assessment | Source |
|---|---|---|
| C1 | Historical r5 closed locally; historical work through r14 landed. Today's r1 is a new operator steer, not a rewrite of those rounds. | `LOG.md:172-194,402-423` |
| C2 | The next move is the still-open version-pinned surface reconciliation below, not re-integrating r5. | `LOG.md:172-194`; live drift recorded in the r1 lesson |
| C3 | R5 LOG and RISC-V/call-target corpus entries exist. Missing historical fleet report/ledger closure remains separate, outside local completion. | `LOG.md:107-194`; `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:156-169` |
| C4 | The three r5 audit errata landed; they are not pending uncommitted work. | `LOG.md:172-188`; final-sweep entry `:156-161` |
| C5 | The named r5 province repairs landed. This does not establish today's provider-version alignment or complete province accuracy. | `LOG.md:176-183`; `PROVINCE.md:23-26,68-73,144-153` |
| C6 | Current map is 70/72, missing r14-01 and r14-02. R14's 70/70 measured its pre-integration cohort. No map rows were repaired this round. | command A; final-sweep entry `:22-48`; `corpus/README.md:126-127` |
| C7 | Local zstd/count/asar fixes landed. Fleet count slips and the current contradictions listed below remain open; r13 applied two integration fixes, not three/four. | `LOG.md:111-114,179-183,395-401`; final-sweep entry `:164-169` |
| C8 | Numeric fields, finite rubrics, evidence, counting commands, measured revisions and round are explicit; no legacy score, saturation or mastery is invented. | this card; `rubric.json`; `result.json` |
| C9 | Promotion assertions are author assessments until a genuine outside verifier is identified. This round's nine workers cannot close SHONEN gates; ten goal-era rounds is a quota, not a score. | `SHONEN.md`; `LOG.md:395-423`; canonical protocol, Promotion gates |

## Open gaps — deliberately not closed by this move

- **Coverage map:** closed at 72/72 by luna-round-1 (2026-10-16); the two
  r14 rows are labeled partial per their files' own limiting language. All
  72 files stay in the denominator. Historical 70/70 is not current 72/72.
- **Version drift:** closed by luna-round-2 (2026-10-16) — per-client pins and
  receipted inventories (Devin/OMP 6.5.0 207/153, Kimi historical 6.4.0 170/127; both
  catalog digests; skill v42 installed / v37 expected by 6.4.0). Superseded 2026-10-18
  (arc2-loop1-round2): Kimi pin is `rea-agents@6.7.0` in `config.toml`'s `[mcp_servers.rea]` per the
  16:57:35Z custody receipt (207/153, `tools_sha256 af39310c…`; configured + package-identity, not holdings — no live Kimi 6.7.0 MCP session opened). Receipts: `.ufo/waves/luna-round-2/receipts/` + `arc2-loop1-round2/receipts/`.
- **Authority contradiction:** closed by luna-round-3 (2026-10-16) — both
  summary sites now state verb-family-specific id identity with corpus
  citations (revenger-verifier path-sensitive per r4; `analyze`/`inspect`/
  `analyze_function` content+params-keyed per r5-01/r9-02; unauthenticated
  `subject` warning retained). QUALITY #15 supersedes #14. The family-specific
  counterexample at r9-02:146-169 stays the authority for `analyze_function`;
  no family beyond the recorded ones is claimed.
- **Other stale summaries:** discharged by luna-round-5 (`7125dd4`) — the
  frontier bullet now reads "held, not frontier" (`corpus/README.md:180`;
  the luna-round-4 "correction" to `:160` was stale at write, and the debt it
  names is discharged) and the r13 row now reads "4 nits: 2 fixes applied at
  integration" (`corpus/README.md:138`; recorded `:128`). Closed; kept as a record.
- **Fleet-only history:** historical `.ufo/reports/round-5/kaidoku.md` is absent
  in the inspected fleet HEAD; `MANIFEST.json` has historical kaidoku training
  rows only through r4. Neither fact erases landed local r5–14 work. Historical
  r4 report/ledger count slips remain fleet-owned; this lane does not alter them.
- **Historical scope bleed:** the old jq provenance entry calls its payload
  “benign” (`corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:217,236-237`),
  while `PROVINCE.md:107-109` refuses safety/trust verdicts. Provenance evidence
  does not justify that safety label; the old entry remains correction debt.
- **Domain frontier:** device-dependent ADB, alternate providers, real compiled
  EVM input, oversized cores, large PE analysis, `.jsc` source mapping and
  runtime-capture limits remain as documented. Availability is not holding;
  historical successful probes are not all freshly re-executed today.

## Measurement recipes

**A — source-derived controls.** Run from this lane repo; set `REV` to either
source commit in `result.json`. This reads immutable Git objects, not a moving
worktree, and never executes the inspected native library.

```bash
python3 - "$REV" <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev,
                                 '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
print(json.dumps({'revision': rev, 'mapped': len(files & mapped),
 'knowledge_files': len(files), 'missing': sorted(files - mapped),
 'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
 'rule_blocks': len(rules), 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
PY
```

**B — count reviewed alignment, not automatic semantic truth.** `rubric.json`
freezes the nine baseline review results and source locations; `result.json`
records the matching post-change IDs and evidence. Review those sources before
accepting the count. A changed status flag without source support is not an improvement.

```bash
/usr/bin/jq --slurpfile r evidence/round-1-2026-10-15/result.json '
  . as $b | [
    {stage:"baseline", revision:$b.baseline_revision,
     aligned:([$b.obligations[]|select(.baseline=="aligned")]|length),
     total:($b.obligations|length)},
    {stage:"after", revision:$r[0].measured_revision,
     aligned:([$r[0].obligations[]|select(.status=="aligned")]|length),
     total:($r[0].obligations|length)}
  ] | map(. + {score:(10*.aligned/.total)})
' evidence/round-1-2026-10-15/rubric.json
```

## Verdicts, planned, retired

- **Axis verdicts:** calibration **improved** within the declared finite
  reconciliation scope; coverage and depth **unchanged**. No claim is made that
  restoring numeric formatting alone increased expertise.
- **Learning trends:** expansion **unchanged** (no new knowledge surface);
  quality **improved** for the superseded self-assessment, not a corpus-wide
  re-verification; discernment **unchanged** (no outside admit/reject spot-check).
- **planned:** calibration — reconcile the still-historical province/skill
  surface summaries against the live version-pinned REA inventory, with an
  explicit old/new-name set and no availability→holding inference.
- **retired:** none. Neither a perfect selected proxy nor ten completed
  goal-era rounds demonstrates saturation or promotion eligibility.

## Interactive round-1 recovery — current admission status, 2026-10-15

This section governs completion claims above. The interrupted worker landed
`c265db9bd3c0883fbaf4487f839559c85a736826`, but its promised `result.json`
and local round report had not landed. The successor recovered **that same
round 1**, not round 2. Historical r1–14 and ten goal-era rounds keep their
original labels. No literal LIVE flags exist on this card; calibration is
the interrupted axis selected from its frozen failure-selected baseline,
not an inference that 10 on a structural proxy means domain saturation.

`evidence/round-1-2026-10-15/result.json` now names the measured work commit,
fresh source-control measurements and **L1-author** reviews of all nine
obligations. It does not reconstruct unrecorded worker reviews or pretend
to exist inside its own measured source commit. Command A was freshly
executed for both source revisions; command B returned 0/9 → 9/9. The gate
checks package integrity, not semantic truth of those reviewed outcomes.

| Owned axis | Before → inherited work, freshly checked | Recovery verdict / limit |
|---|---|---|
| calibration | 0/9 → 9/9 reviewed obligations (0 → 10 finite proxy) | improved for the inherited move, author-assessed; no newly admitted round |
| coverage | 70/72 → 70/72 map tokens (9.72 → 9.72) | unchanged; the r14 pair remains unmapped |
| depth | 9/9 → 9/9 citation-resolution blocks (10 → 10) | unchanged; authority contradictions still prevent a semantic-depth claim |

Full fresh observations: `.ufo/rounds/interactive-r1/source-measurements.json`.
Learning trends: expansion **unchanged**, quality **improved** only for the
assessment evidence chain, discernment **unchanged** without outside review.
Recovery bookkeeping is not a second axis-move or extra round.

- **Wave:** exactly 32 distinct scopes validated, exit 0; **0 dispatched,
  0 settled**. Full output: `.ufo/rounds/interactive-r1/wave-validation.json`.
  Required existing role bindings are missing: executor/scribe must select
  `@m_composer` (observed `@m_mid`/`@m_fast`), reviewer/critic `@m_grok`
  (observed `@m_mid`/`@m_strong`), connector `@m_antigravity` with `@m_zfl`
  fallback (observed `@m_mid`; named antigravity chain empty). Existing cards
  supplied no alternative. No unauthorized dispatch or config mutation occurred.
- **Local gate:** before repair exit 2, `missing_result`; after repair
  `RECOVERY_EVIDENCE: CLEAN`, exit 0. Nine isolated fixture cases passed,
  `RECOVERY_SELFTEST: CLEAN cases=9 exit=0`. `--admission` returned
  `ROUND_ADMISSION: COULD_NOT_EVALUATE finding=required_alias_bindings_missing+applicable_receipt_binding_missing exit=2`.
  Full lines/exit codes: `.ufo/rounds/interactive-r1/gate-results.json`.
- **Smoke:** current closed REA session → owned libjq open → `0x117070`
  decoded as `f30f1efa` / `ENDBR64` → complete evidence export → owned close.
  Fresh bundle: `.ufo/rounds/interactive-r1/rea-bundle.json`. SHA-256 and
  objdump independently matched. Static observation is not target execution.
- **Receipt:** selected launch/Sighting metadata has run/session/mission/pane
  IDs and an argv launch, but no applicable taskKey or dispatcher
  prompt/config/receipt binding. No receipt was fabricated, minted or
  validated; no Sighting completion was attempted.
- **Current status:** blocked recovery; **verified-round increment 0**.
  No native judgment, promotion, saturation or progress toward the 100-round
  target is inferred from this evidence pass.

**Immediate unblock:** operator/integrator supplies the required existing
role bindings and connector fallback, plus applicable receipt-bound dispatch
metadata. Redispatch/recover round 1 in a fresh authorized L1 session, one
complete native 32-member batch; do not increment the round before admission.
The previously planned version reconciliation remains the next content move
only after this recovery closes. All Open gaps above remain named debt with
their cited sources; shared fleet history/ledgers stay integrator-owned.

### Admission-diagnostic correction — same blocked round 1

The earlier `--admission` exit 2 in `gate-results.json` was unconditional;
it recorded the known blockers but did not verify the observation contents.
That interpretation of the prior gate is superseded, not its historical
output. The corrected gate parses the pinned routing/receipt observations,
cross-checks canonical wave role aliases and zero dispatch/settlement fields,
and rejects inconsistent observation contents before reporting blockers.

Current evidence: `.ufo/rounds/interactive-r1/gate-correction-results.json`.
Evidence gate exit 0; self-invocation **12/12** expected exit/finding pairs,
exit 0; evidence-derived prerequisite diagnostic exit 2, unchanged missing
alias/receipt findings. The three added contradictory-observation fixtures
are re-pinned only inside isolated trees to exercise semantic checks.
This verifies consistency of the recorded state, not live routing health,
native admission or receipt applicability. Axes/trends, blocked status and
verified-round increment 0 are unchanged. Correction lesson:
`corpus/lessons/2026-10-15-round-1-admission-correction.md`.

## luna-round-1 — coverage map completion, 2026-10-16

One move on the coverage axis. Claim: coverage map 70/72 → 72/72, no new
dangling rows, depth unchanged. Wave: 64 parent-dispatched verification
seats on `openai-codex/gpt-6-luna-max`, reports at `.ufo/waves/luna-round-1/`
(64/64 delivered); parent-integrated, no seat commits, two lane commits.

- Baseline `a79945c4`: mapped 70, missing both r14 files, coverage 9.72,
  depth 10.0 (command A; reproduced pre-integration by seats R1, C1, P2, R4).
- Work commit `2abd30f5` (lane identity): two map rows added after r12-02,
  both labeled **partial** — r14-01 retains device/operator-gated residue
  (adb/JEB/IDA/Hopper), r14-02 has checks 3/4/6/7 not re-run and a
  fleet-attested but corpus-unanchored evidence id, reported not fixed.
  Critic C5 forced both qualifiers; D3's four-cell row-format claim was
  refuted by direct pipe count (every map row is 3 cells).
- Measured at `2abd30f5`: mapped 72, missing [], dangling [], coverage 10.0,
  depth 10.0 (9/9 rules). Before → after: 9.72 → 10.0; denominator 72 both sides.

| Owned axis | Before → after | Verdict |
|---|---|---|
| coverage | 9.72 → 10.0 (map completeness only) | improved |
| depth | 10.0 → 10.0 (9/9 rules both sides) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged (no new knowledge surface); quality
improved only for map/index completeness, not content truth — 12 V-seat
map-row drift findings and further README drift are named debt in the round
report, deliberately not fixed (one-axis move); discernment unchanged (no
outside admit/reject spot-check of domain claims). Planned item carries
forward; retired: none. The 2026-10-15 reconciliation table above stays
frozen; its "current map is 70/72" row is superseded on that point by this
section. The coverage row's README range pointer was updated 11-58 → 11-60
as this row's own evidence-field hygiene; the stale-summaries bullet's
`:157` pointer (at `:160` in HEAD, per seat C7) is recorded as named debt,
not silently fixed.

## luna-round-2 — per-client REA surface calibration, 2026-10-16

One move on the calibration axis: the SCORECARD's registered 'planned' move
(version reconciliation), taken on a three-way proxy tie at 10.0 by the
most-falsifiable-next-claim rule. Claim: after the round's commit, every
current-surface version/tool-count/skill/catalog statement in the declared
edit targets states per-surface resolved values backed by a 2026-10-16 live
receipt, or is explicitly marked historical; historical evidence cells stay
byte-identical; no availability→holding inference.

- Wave: 64 seats total on `openai-codex/gpt-6-luna-max` — 58 in the initial
  batch + 6 backfill (the parent's short-count error, recorded here, in the
  round report, and the fleet ledger; repaired in-round, round count kept at
  one). Reports `.ufo/waves/luna-round-2/`, receipts
  `.ufo/waves/luna-round-2/receipts/`.
- Receipted: Devin `~/.config/devin/mcp_config.json:7` and OMP
  `~/.omp/agent/mcp.json:8` → 6.5.0 (207 MCP / 153 CLI / catalog
  805433f17bb4… / installed skill v42, doctor aligned); Kimi
  `~/.kimi-code/config.toml:1478` → 6.4.0 (170 / 127 / 25802f6d… / expects
  v37, doctor stale). Both doctor receipts exit 1, `live_server: unknown`:
  receipts prove configured pins and package inventories, not running-client
  identity. MCP `tools/list` counts reproduced twice each way (L7/L8 and
  L15): 207 and 170. Operator configs hash-identical before/after (S2/S5).
- Work commit `75af886a` (lane identity): PROVINCE.md surface summary,
  drift-prone values, Core per-client spawn clause; SKILL.md Domain sentence
  + inventory paragraph + two checklist rewordings. Core probe cells (dated
  2026-10-13 table) untouched; coverage-map evidence cells untouched;
  LOG/lessons append-only untouched.
- Counting (F2 census — a guard, not the acceptance test, per F2's own
  residual-hole finding): PROVINCE surface {6.4.0} → {6.4.0, 6.5.0};
  drift-prone {6.4.0, skill:v37} → {6.4.0, 6.5.0 ×2}; SKILL domain
  {6.4.0 ×2} → {6.4.0 ×2, 6.5.0}. Acceptance carried by G2/G3/G9 receipt
  fidelity and F1/F7 guard passes; F7 found no wrong-client pairing and no
  holding promotion. Mid-round correction: the first drift-prone heading
  draft broke the census anchor and was amended before the records commit;
  the work commit was amended accordingly (never rewritten after records).
- Command A at `75af886a` (side-harm check): mapped 72, missing [],
  dangling [], coverage 10.0, depth 10.0 (9/9 rules) — both prior axes'
  measured values held.

| Owned axis | Before → after | Verdict |
|---|---|---|
| calibration | 10 → 10 (current surface reconciled to receipts; proxy saturated) | improved (fresh failure-selected alignment) |
| coverage | 10.0 → 10.0 | unchanged |
| depth | 10.0 → 10.0 | unchanged |

Learning trends: expansion unchanged; quality improved (current surface
matches receipts; A6's 6.5-only name set — 37 tools + 27 CLI verbs — is
recorded inventory, not holdings); discernment exercised and unchanged
(wrong-client-assignment and availability-to-holding attacks ran; none
survived). Planned next: depth — reconcile the SKILL.md universal
path-sensitive-ID summary with the r9-02 family-specific counterexample.
Retired: none.

## luna-round-3 — family-scoped evidence-id identity, 2026-10-16

One move on the depth axis: the registered planned move from luna-round-2 —
remove the false universal. Claim: after the round's commit, no universal
path-sensitivity claim remains in current-surface text; every id-identity
mention is family-scoped with corpus citations; command A unchanged.
Measurement (adopting seat C8's observable, which the parent accepted in
substance while rejecting the re-scope to calibration — a false domain claim
is depth work): active universal hits 3 sites → 0.

- Wave: 64 seats on `openai-codex/gpt-6-luna-max` (one batch; reports
  `.ufo/waves/luna-round-3/`). Corpus-textual round: no live probes by design.
- Adjudicated from primary sources: r4 lineage
  (`corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:244-250`)
  verifies the revenger-verifier family path-sensitive (same bytes, different
  paths → different ids; jadx per-run; apktool deterministic); r5-01:83-85 and
  r9-02:146-169 verify `analyze`/`inspect`/`analyze_function` content+params-
  keyed, with r9-02's sharper result: the same id across two paths, and a
  subject-only rewrite bit-identical to the honest renamed-path request —
  module attribution travels in `subject`, unauthenticated.
- Work commit `638fb211` (lane identity): SKILL.md Known limits bullet +
  corpus/README.md Known gaps line rewritten family-scoped (anti-substitution
  and pinned-byte guidance retained per seat C1's guard); corpus/QUALITY.md
  criterion 15 added superseding 14 per that file's never-rewrite governance.
  PROVINCE untouched; seat C7's conditional request-byte pin for
  module-identity probes is named debt for a future round.
- Measured at `638fb211`: command A unchanged (mapped 72, missing [],
  dangling [], coverage 10.0, depth 10.0, 9/9 rules); active-surface
  universal hits 0 (the one remaining literal `f(content, path, params)` is
  QUALITY row 14, retained by design as the superseded row); r9-02 cited
  mentions 3.

| Owned axis | Before → after | Verdict |
|---|---|---|
| depth | 10 → 10 proxy; semantic contradiction removed (3 active universals → 0) | improved |
| coverage | 10.0 → 10.0 | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (the corpus's own
acceptance bar no longer admits a disproven universal); discernment improved
locally (C1/C2/C4/C5 attacks refined the wording: two-sided scope, no
exhaustive-family claim, attributed-not-reverified provenance). Planned
next: freshness — repair the 12 named map-row drift findings from
luna-round-1's V-seats (now receipted debt) + the README drift rows
(libsignal 188MB vs 24.9MB; README:130 stale SKILL range; README:170 stale
v37 line). Retired: none.

## luna-round-4 — freshness debt-drain, 2026-10-16

One move on the **freshness** axis (fleet `AXES.md` axis; NOT a lane-owned
proxy — the owned set is coverage/depth/calibration). Parent recording ruling
(seat B6 recommended an unscored disposition; the parent overruled in shape
only): the move is recorded as a fleet-axis freshness improvement, measured by
the wave's census, with owned axes explicitly unchanged — no owned proxy is
re-scored. Claim: after the round's commit, every named drift finding is
REPAIRED or ADJUDICATED-with-cause, the map token set is unchanged (72), and
command A is unchanged.

- Wave: 64 seats on `openai-codex/gpt-6-luna-max` (58 + 6 backfill — the
  parent's short-count error, recorded here and in the fleet ledger, repaired
  in-round; second occurrence of this defect class, see Process). Reports
  `.ufo/waves/luna-round-4/`, canonical census receipt
  `.ufo/waves/luna-round-4/receipts/census-pre.txt`.
- Work commit `6a71cd5` (lane identity; amended once pre-records — eight
  wording tweaks, each reviewed as more faithful to the knowledge files, to
  satisfy the wave's own census matchers): 14 repair groups in
  `corpus/README.md` covering 15 findings; asar row and crash row adjudicated
  NO-CHANGE with evidence (V01a, D01).
- Measured at `6a71cd5`: command A unchanged (mapped 72, missing [],
  dangling [], coverage 10.0, depth 10.0, 9/9 rules); wave census 14/19 PASS
  + 5 ADJUDICATED-with-cause (F01/F02/F05/F16/F18 — reasons in the round
  report); token set 72/72.

| Axis | Before → after | Verdict |
|---|---|---|
| freshness (fleet axis, unowned proxy) | 19 named findings → 14 repaired + 5 adjudicated; census 14 PASS, 0 true debt | improved |
| coverage | 10.0 → 10.0 (measured) | unchanged |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (map/Known-gaps text
now matches the knowledge files it summarizes; the census's own overreach —
five structurally unsatisfiable or refuted-encoding checks — is recorded as
instrument debt, not finding debt); discernment improved locally (V01a
refuted a round-1 seat finding; C05 inverted the authority question onto a
knowledge file). Planned next: luna-round-5 begins the operator's 128-seat
two-lane contract (64 luna + 64 deepseek-v4.1-flash) — the carried debt
queue (r1 asar file framing, r4u-01 size decimals, PROVINCE request-byte pin,
README stale frontier content) is the candidate worklist. Retired: none.

## luna-round-5 — freshness: seven debt dispositions, 2026-10-16

One move on the **freshness** axis (fleet axis, unowned proxy — same
recording ruling as luna-round-4). First round under the operator's updated
128-seat two-lane contract: 64 luna + 64 deepseek-v4.1-flash seats (one
wave, two back-to-back batched dispatches per lane). Claim: after the
round's commit, all seven recorded debt items are dispositioned with
append-only knowledge errata or declared current-surface edits; command A,
map rows, and the token set are unchanged.

- Wave: 128 seats total (parent under-dispatched lane B 58/64 — third
  short-count, repaired with a 6-seat backfill before integration; the
  defect class is now recorded three times and the parent added a counting
  self-check to subsequent dispatches). Reports `.ufo/waves/luna-round-5/`.
- Cross-lane convergence (the point of the two-lane contract): item 2
  unanimous across 30 independent readings; items 1/3-7 converged after
  Z-seat diffs, with lane-B-exclusive catches (r12-01's existing erratum;
  r5-02's exact form; revenger's open governance question).
- Work commit `7125dd4` (lane identity; one pre-records amend: the
  Runtime-obs bullet opener renamed to 'Runtime-obs depth' — the census's
  stale-detector matched the retained opener, not the corrected content):
  five append-only knowledge errata + two PROVINCE same-physical-line
  additions + two README row repairs. No historical bytes rewritten; the
  append-only tails were verified seat-independently (F/SB seats).
- Measured at `7125dd4`: wave census 6/7 PASS + SIZES ADJUDICATED (raw
  comma token vs normalized text — structurally unsatisfiable; arithmetic
  established by 30 readings + inline recheck); TOKENSET 72/72; MAP-ROWS
  byte-identical; command A unchanged (72/72, 9/9, 10.0/10.0).

| Axis | Before → after | Verdict |
|---|---|---|
| freshness (fleet axis, unowned proxy) | 7 debt items → 7 dispositioned (5 errata + 2 README + 2 PROVINCE additions; 1 item adjudicated existing-erratum) | improved |
| coverage | 10.0 → 10.0 (measured) | unchanged |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (the corpus's
records now match their own evidence on all seven items; the '~26
self-provisionable' spent driver is retired); discernment improved
meaningfully — the two-lane design caught one already-satisfied item, one
exact-form correction, one cross-lane governance answer, and the parent's
own third counting defect. Two census checks now adjudicated as instrument
debt (comma-token normalization; opener-detector breadth) — recorded for
the instrument's owning round. Planned next: luna-round-6 — the deepest
remaining queue is live-probe re-verification of stale-held surfaces (the
round-2 receipts prove package inventory, not running processes; a
battery of e2e re-runs on 6.5.0 would convert availability claims toward
holdings — an operability/deep-freshness hybrid, to be framed at round
open). Retired: none.

## luna-round-6 — operability: pre-registered 6.5.0 battery, 2026-10-16

One move on the **operability** axis (fleet axis, unowned proxy — same
recording ruling as rounds 4-5). Claim shape: a 10-leg battery executes on
the live 6.5.0 surface with hashed receipts per lane, ≥8/10 match the frozen
outcome classes, cross-lane agreement, zero config drift, invariants intact.
Predictions frozen parent-side before dispatch (prereg itself audited).

- Wave: two-lane battery, 64 luna + 64 deepseek-v4.1-flash seats = 127
  distinct seats (parent short-counted lane A 53/64 — fourth occurrence —
  and an interruption cost a double-counted slot; both recorded in the
  round report and fleet ledger).
- Landed at `bc91424` (lane identity): the 20-leg receipt bundle committed
  TRACKED (durability deviation disclosed — see LOG). Measurement-only
  round: map/PROVINCE/SKILL untouched.
- Measured: lane A 10/10, lane B 10/10 (independent recounts AC1/BC1);
  cross-lane class agreement 10/10 (byte-identical L1/L2/L7/L10);
  frozen census PASS twice byte-identical (AC3/BC4); command A + token set
  unchanged (AC8); zero availability→holding upgrades (AC4); zero config
  drift, no live MCP residue (BC3).

| Axis | Before → after | Verdict |
|---|---|---|
| operability (fleet axis, unowned proxy) | no live-process evidence → 20 hashed, replay-verified receipts across two model lanes; 10/10 + 10/10 vs frozen classes | improved |
| coverage | 10.0 → 10.0 (measured) | unchanged |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged this round (the battery's six newly
exercised 6.5.0 verbs become round-7 knowledge entries); quality improved
(durable receipts replace /tmp ephemera; custody defects recorded); discernment
improved (forgery attacks, copy-vs-run attacks, and class-vs-byte agreement
distinctions all exercised and recorded). Planned next: luna-round-7 =
coverage — knowledge entries + map rows for the six exercised 6.5.0 verbs
(denominator 72 → 78; command A must re-measure 78/78). Retired: none.

## luna-round-7 — coverage: six 6.5.0-verb entries, 2026-10-16

One move on the coverage axis: convert luna-round-6's exercised verbs into
admitted knowledge. Claim: after landing, command A re-measures
knowledge_files=78, mapped=78, missing=[], dangling=[], 9/9 rules; every
entry passes corpus/QUALITY.md; the prior 72 entries byte-identical.

- Wave: two-lane (64 luna + 59+5 deepseek backfill = 128). Cross-lane
  drafting with convergence; FINAL-MANIFEST compiled by the integration
  seat with all wave corrections applied (see LOG).
- Work commit `3395b6d` (lane identity; two commits: six files, then twelve
  README rows).
- Measured at `3395b6d`: command A 78/78, 9/9, 10.0/10.0; prior-72 diff
  empty. The numeric proxy stays a finite index measure — 10.0 at 78 files
  is index completeness, not domain fraction.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage | 10.0 → 10.0 (denominator 72 → 78; index completeness held at the larger denominator) | improved (six RESULT-class verbs became admitted, quality-gated knowledge) |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |
| freshness/operability | n/a this round | unchanged |

Learning trends: expansion improved (six new verified surfaces); quality
improved (QUALITY-12 enforcement excluded an unreproducible result;
metadata fields now standard for new entries); discernment unchanged.
Planned next: luna-round-8 — operability symmetry battery on the Kimi
6.4.0 pin (round 6 covered 6.5.0; the kimi-resolved 6.4.0 surface gets the
same preregistered treatment, closing the per-client evidence asymmetry).
Retired: none.

## luna-round-8 — operability: 6.4.0 symmetry battery, 2026-10-16

One move on the operability axis (fleet axis, unowned proxy): the mirror
battery on the Kimi-resolved 6.4.0 pin. Claim: 10 hashed receipts, ≥9/10
frozen predictions, cross-lane verification, invariants intact.

- Wave: two-lane 128 seats. Scored 10/10 (CA6; PB0 re-verified every
  hash; QB gates on the landed entry).
- Landed at `18dc397d` (lane identity): one consolidated knowledge entry
  (denominator 78→79, command A 79/79 re-measured) + tracked receipts.
- Measured: command A 79/79, 9/9, 10.0/10.0 at `18dc397d`; config hashes
  match the round-6 baseline (no round-8 pre-pair — recorded).

| Axis | Before → after | Verdict |
|---|---|---|
| operability (fleet axis, unowned proxy) | 6.5.0-only live evidence → both pins live-evidenced; six per-name refusals corroborate A6 | improved |
| coverage | 10.0 → 10.0 (denominator 78 → 79) | unchanged (the entry is the round's expansion side-effect, recorded) |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion +1 verified entry; quality improved (tracked
receipts now standard; stale-verdict adjudication table); discernment
unchanged. Planned next: luna-round-9 — the carried spill queue (r4-16
frontier-rescan staleness at :751-752 flagged by BB1 in round 5; census
instrument debt from rounds 4-5; the /tmp hygiene question) as a
freshness/quality round. Retired: none.

## luna-round-9 — freshness: carried-spill queue, 2026-10-16

One move on the freshness axis: four carried debt items dispositioned
(r4-16 erratum cross-reference; census instrument limits; /tmp-dependence
audit; jq-shadow safety-verdict scope). Claim: after landing, command A
re-measures 79/79 + 9/9 + 10.0/10.0; both knowledge appends prefix-identical
(append-only); PROVINCE untouched.

- Wave: two-lane 128 seats; four item chains each with verifier, drafter,
  adversary, reviewer, convergence, and two independent lane-B gates.
- Work commit `40162fc` (lane identity): the two append-only knowledge
  errata (see LOG for texts). Item 2 and item 3 land here + the report.
- Measured at `40162fc`: command A 79/79, 9/9, 10.0/10.0; prefix-identity
  True for both appends.

Known census-instrument limits (rounds 4–5, carried; ADJUDICATED, not PASS).
The round-5 SIZES check passed comma-grouped needles (`29,367,752` /
`84,258,816`) into comma-normalizing text, so no correct input could pass
(`.ufo/waves/luna-round-5/X1.md:12,32`; `.ufo/waves/luna-round-5/CB4.md:11`;
`.ufo/reports/luna-round-5/kaidoku.md:50-56`). Round-4 F18's predicate was
structurally unsatisfiable — its unsatisfiable conjunct is the
replacement-pair/refuted-encoding test — while the stale wording was absent,
and the round-5 README-opener detector matched the retained "Runtime-obs
extended" opener, not the corrected content
(`.ufo/reports/luna-round-4/kaidoku.md:43-46`;
`.ufo/reports/luna-round-5/kaidoku.md:63-67`). These are instrument limits,
not corpus-content verdicts; documentation only — no score change and no
waiver: new mismatches stay evidence-adjudicated until the affected matcher
is repaired and retested.

**/tmp dependence (round-9 audit):** no current kaidoku instruction,
registered gate, or landed `recheck:` requires pre-existing `/tmp` contents;
`/tmp` is transient scratch (`PROVINCE.md:48`). Labeled residuals:
historical `verify:` recipes cite prior `/tmp` outputs
(`corpus/knowledge/2026-10-13-r3-renderer-asar.md:11,19`;
`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:40-42`) — archival
debt, not a current dependency; L7-01's npm-cache pre-existence untested
(`corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:5`). The ~1.2 GB
litter remains operator hygiene; no deletion authorized or performed.

| Axis | Before → after | Verdict |
|---|---|---|
| freshness (fleet axis, unowned proxy) | four carried items dispositioned (2 append-only errata + 2 documented dispositions) | improved |
| coverage | 10.0 → 10.0 (denominator 79, measured) | unchanged |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (instrument limits
documented with a retest trigger; safety-language scope enforced); discernment
unchanged. Planned next: luna-round-10 — the arc closeout: full debt-ledger
reconciliation across rounds 1-9, SHONEN final assessment, the arc
measurement census (command A + receipts + verdicts), and the final report.
Retired: none.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `.ufo/waves/luna-round-6/receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `.ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |
| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps — the paired demonstrations: r7 wall-fall (ev_a4aa9b0d…) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |
| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |
| curated source registry for existing REA frontier | Keeps opened, scoped study sources, ordered paths, recheck cadences, an auditable bounded search, and a source rejection with evidence and flip; source text is not held-capability evidence | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | arc3-loop1-round13 |
| local raw-quote/heading regression audit | Rejects the retained S017 splice and S018 wrong section, accepts corrected controls, and refuses malformed/tampered inputs; frozen runs pin every manifest/source input | `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest`; `--frozen .ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/verification.json` | round-14 |
| retained REA Ghidra-session log capture | Runs REA analyze on a pinned carrier in a private-TMPDIR session and keeps ghidra.log/script.log before close; the receipt validates offline. Stored mid-run pin checks are verdicts, not full maps | `bash .ufo/waves/round-17/run-carriers.sh <LABEL>`; `.ufo/waves/round-17/verification.json`; `corpus/lessons/round-17-verifier-spotcheck.md` | round-17 |
| REA SquashFS recursion through sasquatch (LE v4) | `extract-firmware` publishes every regular file of a little-endian SquashFS v4 payload (bare image or appended to an AppImage runtime) once the official sasquatch 4.5.1 binary is on `PATH`; without it REA reports a `missing-extractor-dependency` gap naming sasquatch and publishes no member. Big-endian/AVM not demonstrated | `corpus/evidence/round-36/c1/`; `tools/round-36/c1-run.sh`; `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` | round-36 |
| standard big-endian SquashFS v4 recursion (`squashfs_v4_be`) | `extract-firmware` on a standard big-endian SquashFS v4 image publishes every regular file of an independent oracle (same relative-path suffix and sha256) once `sasquatch-v4be` 4.5.1 is on the unblob 26.6.4 child `PATH`, records one `unpublished-entry` gap per in-tree symlink, publishes no path for an escaping link (which unblob removes with `MaliciousSymlinkRemoved`), and has no failed chunk; gzip blocks and genuinely compressed xz blocks (`comp_id 4`) both decode. AVM-marked BE bodies, vendor-mangled images and extra published files are not claimed | `PROVINCE.md:378-384` (round-39 Core row naming `squashfs_v4_be` and the round-39 frontier note); entry `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`; carriers `.ufo/waves/round-39/c1/carriers.json` (sha256 pins); receipts `corpus/evidence/round-39/c1/K{1..6}/{after,run}.json`; frozen counter `tools/round-39/c1-counter.py` (6/6, exit 0 at `6fdaf4f1`); independent post-landing re-runs `.ufo/waves/round-39/w2/R39W2C1AxisFit.md` §0 (all six), `.ufo/waves/round-39/w2/R39W2Repro{K1,K2,K3,K4,K6}.md`, `.ufo/waves/round-39/w2/R39W2K5K6Rebuild.md` | round 39 |
| executable SquashFS `extract-firmware` outcome triage | a frozen interpreter (`tools/round-39/sqfs-triage.py`) reads one machine-readable SKILL craft table and nothing else, and labels an REA 6.5.0 envelope from six fields — squashfs chunk handler, gap kinds, gap `dependencies`, the recorded `-be` token in the sasquatch argv, `MaliciousSymlinkRemoved`, published file count — into eight labels; scored 20/20 on a held-out set generated after the freeze with seed = the freeze hash, and the labels come from the table, not from the envelope (no class/label token leaks). Bounded to ten generator classes; no AVM-BE body, no `unknown-chunk-handler`/`encrypted-chunk`/`depth-limited` envelope; the smallest table that also reaches 20/20 is 8 rows / 7 non-`*` cells, so the target does not yet mean "triage" in general | `SKILL.md:316-343` (rule block 18; table after `<!-- sqfs-triage-table v1 -->`); interpreter `tools/round-39/sqfs-triage.py` (`--selftest` 35 cases); generator `tools/round-39/heldout-gen.py`; manifest `corpus/evidence/round-39/c2/heldout/manifest.json` (H01–H20, seed `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`); envelopes `corpus/evidence/round-39/c2/heldout/H*/{envelope,run,tree}.json`; counter `tools/round-39/c2-counter.py` (20/20, exit 0 at `6fdaf4f1`); floor, leakage and ceiling measurements `.ufo/waves/round-39/w2/R39W2C2Shortcut.md`; envelope provenance `.ufo/waves/round-39/w2/R39W2HeldRepro{A,C,D}.md` | round 39 |
| executable SquashFS `extract-firmware` outcome triage v2 (label and action) | a frozen interpreter (`tools/round-40/sqfs-triage-v2.py`) reads one machine-readable SKILL table (rule block 19) with an `operation`/`provider` domain guard and a closed action vocabulary, and returns the (label, action) pair for an REA envelope; non-firmware envelopes read `unclassified` | `python3 -I -B tools/round-40/c2-counter.py --root <LANE> --rev 42c10a58cb2cae3a4a0122af35a0cf95ac718043 --freeze 7fce308631a8b457d6b7c5a4b39a923c4e9a49de` → 26/26, exit 0 (`.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`; reproduced `.ufo/waves/round-40/w2/R40W2C2Rescore.md`) | 40 |
| genuine AVM-layout big-endian SquashFS v4 recursion (`squashfs_v4_be`, AVM layout) | `extract-firmware --max-depth 1` on a genuine AVM-layout image (big-endian fields, little-endian metadata block lengths, `mkfs_time == bytes_used`) publishes every regular file of an independent oracle at its exact path relative to the chunk extract root and accounts for every symlink as one `unpublished-entry` gap or one `MaliciousSymlinkRemoved` removal, on two vendor members (FRITZ!Box 5490 wrapper, 5491 nested rootfs of 6349 files) and two lane-built images with both-direction path collisions | `tools/round-41/c1-counter.py` 4/4, exit 0, `.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json`; receipts `corpus/evidence/round-41/c1/` | 41 |

Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.

Round-32 summary repair restores the three already-demonstrated append-only records (base `283aad7f` lines 2136, 2208, 2375), not three new acquisitions. Evidence was reopened in `.ufo/waves/round-32/a2audit/A2Capability13.md`, `A2Capability14.md`, `A2Capability17.md`, `A2Capability27.md` (same directory). The round-17 wording retains QUALITY 21's distinction between comparison verdicts and full pin maps. C2v3's lexical counter is falsified by negative prose and word bags (`.ufo/waves/round-32/controls/c2-negative/receipt.json`); a passing numerical alignment is not calibration improvement.

## Saturation

Saturation line: 10.0 on the three finite owned proxies (coverage/depth/
calibration) — reached by luna-round-3 and held through luna-round-9, with
every improvement after that recorded as proxy-saturated + measurement-named.
Stagnation window N: 10 lane-rounds. Capabilities entered the table in
rounds 6-8 (inside the window), so the nudge did not trigger during the arc.
Declared at luna-round-10, the conformance scaffold's named 'next round';
window resets from here.

## arc2-loop1-round1 — freshness + operability + depth: three claims, 2026-10-18

One round, three claims (arc 2, loop 1) — the first round of the reset
stagnation window (`## Saturation`, above). The three finite owned proxies
remain saturated at 10.0; the freshness and operability moves are fleet-axis
(unowned proxy — the standing recording ruling, :376-380) and the depth move
is recorded proxy-saturated + measurement-named.

- Wave: 64 seats, parent-integrated (no seat commits); seat reports
  `.ufo/waves/arc2-loop1-round1/`; round report
  `.ufo/reports/arc2-loop1-round1/kaidoku.md` landed.
- Dispatch (operator-directed): recovery dispatch — the first attempt
  delivered 18 seats (P1, P4, E1, E6, E7, E8, E11, E14, E17, E18, E20, E24,
  E25, SC1, R7, V3, V4, V5); the remaining 46 seats were dispatched as
  replacements on the devin provider per the operator directive of 2026-10-18
  (provider substitution directed by the operator, not a lane choice).
  Provider identity is substrate-neutral (`PROTOCOL.md:14-17`); 18+46 = 64
  seat slots = the declared wave size.
- Landed at `58116aa` + `df31bfb` (lane identity, append-only): r3-jq-provenance
  EOF "Safety-verdict scope" note naming `:60` and `:136` (byte-identity +
  recorded-provenance scope, explicit non-endorsement per
  `PROVINCE.md:114-116`; form of
  `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`); lessons round-1
  EOF correction note (the `:152` `PROVINCE.md:107-109` token is
  baseline-correct under `SCORECARD.md:16-17`, read at HEAD as `:114-116`;
  drift commit `7125dd4`); `SKILL.md` queue-drain craft rule #10 + config
  custody SOP section; `SHONEN.md` pointer refresh (same commit); receipts
  `.ufo/waves/arc2-loop1-round1/receipts/` committed
  (`config-pre-pair.txt` + `config-post-pair.txt` + battery leg artifacts +
  `MANIFEST.txt`).
- Measured at `df31bfb` (re-measured at that revision): command A
  79/79 mapped, rules 9 → 10, 10/10 resolvable, coverage 10.0 / depth 10.0 /
  calibration 10; r3 file-scoped safety-label census 2 → 0 (`:60`, `:136`
  both named by the appended note; historical bytes retained); post-pair
  hashes byte-equal to the pre-pair — zero drift (receipt
  2026-10-18T16:52:56Z; corroborating captures 16:41:57Z E26, 16:42:22Z E23,
  16:44:29Z CR3, 16:45:06Z P3).
- Adjudicated NO-CHANGE-with-cause: `SCORECARD.md:79`'s `PROVINCE.md:107-109`
  token — baseline-revision-correct under the card's own convention (:16-17)
  and located in `## Open gaps` (:51-84), not in the frozen :39-49 table
  (freeze sentence :266-267; earlier "frozen table" wording restated per the
  round's E4); carried at `LOG.md:883-886`.

| Axis | Before → after | Verdict |
|---|---|---|
| freshness (fleet axis, unowned proxy) — C1 | r3-jq-provenance unscoped safety-label loci 2 → 0 (`corpus/knowledge/2026-10-13-r3-jq-provenance.md:60` "benign, intentional install"; `:136` "no malicious or accidental pathway indicated"; both named by the EOF erratum; file-scoped census, scope stated per `CR5.md:341-389` — `corpus/README.md:90,:160` deferred, `LOG.md:21` frozen) + lessons stale-pointer correction note absent → present (`corpus/lessons/2026-10-15-round-1.md:152`, `:107-109` → `:114-116`); `SCORECARD.md:79` byte-identical | improved |
| operability (fleet axis, unowned proxy; capability acquisition) — C2 | no same-round pre-pair custody (luna-round-8 defect, `SCORECARD.md:544-545`; `LOG.md:856-858`) → pre-pair `receipts/config-pre-pair.txt` (2026-10-18T14:49:13Z; 3-way corroborated E11/V4/V5) + post-pair `config-post-pair.txt` (2026-10-18T16:52:56Z); zero drift 0/3 across the battery window (captures 16:39–16:52Z); capability row entered below | improved |
| depth — C3 | 10.0 → 10.0 (proxy saturated + measurement-named); queue-drain rules 9 → 10, resolvable 9/9 → 10/10 (`SKILL.md` rule #10 measured at `df31bfb`; citations = the already-landed luna-round-8 record only: `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15` + `SCORECARD.md:544-545` + `LOG.md:856-858`) | improved (rule gain; proxy unchanged) |
| coverage | 10.0 → 10.0 (command A at `df31bfb`: 79/79, missing [], dangling []) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged (no new knowledge surface; deliberate —
all three claims close carried debt or record practice); quality improved
(the r3/lesson records now match their evidence; custody receipts durable and
tracked; SHONEN pointers refreshed); discernment improved (CR1's
disguised-verdict attack, CR3's security-theater attack, CR5's census
instrument defects, and SC2's live Kimi-pin refutation all adjudicated from
recorded evidence, not vibes).
Planned: unchanged — the luna-round-10 closeout registered no next move and
its final debt ledger stays carried (`.ufo/reports/luna-round-10/kaidoku.md:39-44`;
the card's last planned line, :610-613, named that closeout, now discharged).
Carried debt (named, not landed): `corpus/README.md:90,:160` label
qualification (deferred with cause); `PROVINCE.md:10,:18` Kimi-pin correction
(live config now pins `rea-agents@6.7.0` at `config.toml:2940`, SC2-refuted);
`SCORECARD.md:68`'s drifted `:160` pointer; `.bashrc`/`~/.profile` into the
custody pair from the next round's pre-pair (E15 — retro-append void).
Retired: none.

## arc2-loop1-round2 — calibration + freshness + operability: three claims, 2026-10-18

Round 2 of the reset stagnation window (2/10). Owned proxies stay saturated;
calibration worked as the owned axis (most-falsifiable tie-break — the live
Kimi pin refuted the current surface); freshness and operability ride the
fleet-axis recording ruling (:376-380). Parent-integrated; no seat commits.

- Wave: 64 seats dispatched on `devin/deepseek-v4-1-flash-max`; 60 seat reports
  delivered (4 non-completions recorded as a dispatch defect; every claim
  verified via convergent seats regardless). Reports `.ufo/waves/arc2-loop1-round2/`.
- Landed at `b3cd790` + `b21c0da` (lane identity, line-neutral — every in-place
  edit same-line-count; PROVINCE 162 / SCORECARD 701 / README 187 lines held,
  no landed citation shifted): PROVINCE.md surface summary + drift-prone values
  + two Core cells (spawn→registers per CR1's grade ladder); SKILL.md inventory
  paragraph; SCORECARD Version-drift supersession bullet; SCORECARD.md:68-72
  discharged-pointer reword (5-for-5); corpus/README.md:90,:160 in-cell
  safety-label qualification (byte-certified to the reviewer's predicted whole-
  file hash `ba7265eb…`); SKILL custody SOP 3-path→5-path amendment (+24 lines,
  craft section byte-identical). Receipts: 5-path pre/post-pair (in-window zero
  drift 0/5), 6.7.0 doctor + census legs, post-window drift record.
- Measured at `b21c0da`: command A 79/79, rules 10/10, 10.0/10.0 (unchanged —
  no craft or map edit); C1 census instrument (E22 v9, anchors re-derived live)
  **VERDICT PASS — stale=0 ambiguous=0 undeclared=0 unresolved=0** at the work
  tree; C2 instrument (E23 form) n_unqualified 2→0; config drift: 0/5 in-window
  (receipts 16:57:35Z / 17:08:57Z, five captures aggregate-matching); post-window
  `config.toml` rewrite at 17:32:20Z detected and recorded verbatim
  (`receipts/drift-config-toml-20261018T173220Z.txt`; pin value unchanged,
  relocated :2938→:3225; not repaired, per SOP — operator-owned surface).
- Battery (REA 6.7.0, local npx cache; one registry packument revalidation
  observed, payload cache-served): leg 1 `doctor` exit 1, 27 scope_checks,
  identity 6.7.0, counts 153/207/6, `tools_sha256 af39310c…` (differs from
  6.5.0's `805433f1…` — the digest is a build-recorded constant per
  `recordedCatalogDigests.js`); leg 2 `binary_session {}` census PASS — 207
  tools byte-identical name set to 6.5.0, clean close, server exit 0. SC2's
  "6.7.0 unprobed" unknown resolved.

| Axis | Before → after | Verdict |
|---|---|---|
| calibration — C1 | 6 hard-stale current-surface Kimi-pin loci (PROVINCE.md:10,:18,:44, SKILL.md:20, SCORECARD.md:58) + 1 receipt-contradicted (:24 doctor-aligned) + 1 ambiguous (:67) → 0/0/0 (census PASS at the work tree); every statement receipt-backed or historical-marked; grade ladder enforced (configured/resolvable/available — no holding claims; PROVINCE :44 "spawn"→"registers") | improved |
| freshness (fleet axis, unowned proxy) — C2 | unqualified safety-label loci in editable corpus files 2 → 0 (README :90,:160 qualified, certified hash `ba7265eb…`; r3 file clean since round 1) + drifted README pointers inside the SCORECARD:68 bullet 2 → 0 (:160→:177, :128→:138 — both debts discharged at 7125dd4; 5-for-5 reword, net-zero) | improved |
| operability (fleet axis; capability acquisition) — C3 | 3-path custody → 5-path custody demonstrated end-to-end (pre-pair 16:57:35Z bracketing the 6.7.0 battery; post-pair 17:08:57Z; zero drift 0/5 in-window) + SOP amended to match + capability row entered (replaces the r1 3-path row); post-window drift detected, recorded, unrepaired — the detector's first live catch | improved |
| coverage | 10.0 → 10.0 (command A at `b21c0da`) | unchanged |
| depth | 10.0 → 10.0 (command A at `b21c0da`) | unchanged |

Learning trends: expansion unchanged (no new knowledge surface); quality
improved (the current surface now matches the live pins byte-for-byte against
frozen receipts; discharged debts recorded accurately, false sentences
avoided — R2's 5-for-5 reword over the tempting bare re-point); discernment
improved (CR1's four-grade configured/resolvable/available/held ladder plus the
wire-log finding — 0 of 2195 Kimi tool-logs declare `mcp__rea__*`, so the 6.7.0
server is configured-but-not-held, plausibly never loaded; CR7's +18-line shift
attack — landed line-neutral so no landed citation moved; CR3's carrier-mode
ambiguity bounded as a named limitation).
Planned: none declared. Carried debt (named, not landed): SCORECARD.md:270's
stale `:157` parenthetical (third drifted-pointer reading, V5); MINT.md:10 and
corpus/QUALITY.md:18 + lessons/2026-10-15-round-1.md:82 +
corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80,:88 (dead `:1284/:1287`
pointers) + r4-16-frontier-rescan.md:43 (stale-pin loci outside C1's declared
scope); SCORECARD.md:291 (dated record, classified historical — E6's
reconciliation note not needed given the :58 supersession); grok/codex rea
registrations (5 total) outside the 5-path custody set — zero-drift claim
scoped to the five named paths; Kimi client-side rea load probe (the wire-log
finding's natural follow-up); systemd user env / ~/.bash_profile carrier
limits. Retired: none.

## arc2-loop1-round3 — freshness verified; coverage inconclusive; operability form-refuted, 2026-10-18

Round 3 of the reset window (3/10; no capability entered — the stagnation nudge
does not fire before N=10). Owned axis worked: coverage, via the most-
falsifiable tie-break. **Round not admitted: 1 of 3 claims verified** — the
other two are reported as honest stops, not trades. Parent-integrated; 64
seats dispatched, 60 reports delivered (4 non-completions, second consecutive
round — a named dispatch defect).

- Wave: 64 seats on `devin/deepseek-v4-1-flash-max`; reports
  `.ufo/waves/arc2-loop1-round3/`. Landed at `fd30b9c` + `dbba2dd` (lane
  identity).
- Landed (C1): PROVINCE.md:18 and SCORECARD.md:59 re-anchored in place
  (single-line, line-neutral — 162/766 held); append-only errata at
  `corpus/knowledge/2026-10-13-mcp-registrations.md` (88→111 lines,
  prefix-identical) and `2026-10-13-r4-16-frontier-rescan.md` (936→975,
  prefix-identical) — every erratum content-anchored (`[mcp_servers.rea]`
  stanza key + receipt sha256), never a bare line number, because the live
  stanza walked :1284→:2938→:3225→:3296 across 2026-10-18's operator rewrites
  and the round's own declared re-point target (:2938/:2940) was dead at write
  time. Dated records adjudicated, not edited: SCORECARD.md:270 (:157 is
  baseline-correct under :16-17; its bullet's live pointer was discharged by
  round-2's :68-72 reword) and SCORECARD.md:698 (round-2's dated text).
- Measured at `dbba2dd`: C1 pointer-census instrument (E23 form, sha256
  `7cd2a760…`) — **unwarned dead loci 6 → 0** (all six discharged by the
  errata), **minted dead pointers 0**, current-surface wide-dead 4 → 3
  (SCORECARD:59 repaired; :291/:698 are dated), SCORECARD:270 region reading
  discharged-by-adjudication; command A 79/79, 10/10, 10.0/10.0 (unchanged —
  the C2 entry did NOT land).
- C2 (coverage — INCONCLUSIVE, honest stop): the bisect leg HELD (2.5MB
  decompile.exe, exit 0, 44.117s, 6,337 procedures, `ev_92dea347…`,
  deterministic rerun byte-identical, peak RSS 1.63GiB — the recipe works).
  The 91.6MB Godot ARM64 leg ran 30m01s under `REA_GHIDRA_STARTUP_TIMEOUT_MS=
  3600000` + `GHIDRA_HEADLESS_MAXMEM=8G` and died at its OWN outer 1800s cap:
  typed `cancelled` envelope (`cleanup:complete`), no evidence sealed. The
  raised REA deadline was never reached — the outcome is neither HELD nor the
  pre-accepted typed refusal, so the claim cannot verify. Knowledge accrued
  and recorded (survived 2× r4-12's kill still analyzing; RSS 8.89GB >
  -Xmx8G proves the heap knob load-bearing; decisive run needs a scoped,
  contained >5400s window per CR2/CR3) — but per CR3 a knowledge entry here
  would be a re-run dressed as a move; not landed, coverage stays 79/79.
- C3 (operability — NOT VERIFIED, form refuted on evidence): both gate
  implementations work (E14: 6 modes, selftest 15/15; E15: selftest 10/10,
  live red→green), but the gate form fails the Gate standard on measured
  grounds: config.toml line-numbers are unpinnable (operator-owned, churned 4+
  states today), a committed gate would fire on the lane's own honest
  receipt-anchored citations (CR4's false-positive census), and the frozen-run
  clause fails as shipped (R3 F2, 8-vs-9-line block). Adjudication: land as a
  PROBE in a future round over in-repo pinneable citations only (E16's
  BASELINE/QUOTED/SYMBOL row classes), with R6's exit-expression and
  anchor-fragility fixes; this round lands the durable half — the
  content-anchor repairs (C1's errata), which no gate can enforce.
- Custody: pre-pair 17:55:49Z verified 5/5 (re-baselined config.toml
  `bd5a78d1…` per round-2's disposition). In-window **witnessed
  mutate-and-revert** (18:01:40Z `9ac8023b…` +14 lines → reverted 18:02:33Z,
  mtime+inode restored; writer resolved by CR8: interactive Kimi session
  afa2dd53, not a wave seat): the config.toml zero-drift claim is VOID as bare
  per the SOP; other four paths held every capture; post-pair 5/5 endpoint;
  excursion recorded verbatim at
  `receipts/drift-config-toml-mutate-revert-20261018T180140Z.txt`.

| Axis | Before → after | Verdict |
|---|---|---|
| freshness (fleet axis) — C1 | undischarged dead config.toml pointer loci 6 → 0 (E23 instrument unit, measured at `dbba2dd` vs `679af5d`); current-surface wide-dead 4 → 3 (PROVINCE:18 + SCORECARD:59 re-anchored; dated records adjudicated with cause); minted 0 | improved |
| coverage (owned) — C2 | claim unverifiable as observed: 91.6MB leg inconclusive (outer-cap kill, deadline untested); recipe held on the 2.5MB leg; NO knowledge entry landed (re-run-dressed-as-a-move refused); command A 79/79 both sides | unprovable (honest stop — not harmed) |
| operability (fleet) — C3 | gate form refuted (unpinnable targets, false-positive surface, frozen clause defect); implementations proven but not committed; durable repair = content-anchor citations landed under C1; probe registration + conformant gate = named debt | not verified (honest stop) |
| depth | 10.0 → 10.0 (command A at `dbba2dd`) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (the pointer class is
now discharged content-anchored with receipts — the durable form the churn
itself demanded); discernment improved (three separate refutations landed
without injury: the declared re-point target was dead, the C2 outcome class
didn't match the pre-accepted branches, and the C3 gate form failed its own
standard — each caught by the wave's critics and reported rather than forced).
Planned: the C2 decisive run (scoped, systemd-contained, >5400s, deadline-
only) is the next frontier/capability candidate; the C3 probe registration
follows. Carried debt (named): LOG.md:1005/:1018 + round-2's PROVINCE/SCORECARD
receipt-anchored :2940 references (correct at record time; correction = this
entry, append-only); lessons/2026-10-15-round-1.md:82; corpus/knowledge
dead-token rise inside the errata themselves (instrument-predicted; the unit
is "unwarned", stated); E11's two unreproduced 0-byte probe runs; E22 census
scope-table drift (FAIL undeclared=2 at 766-line HEAD vs PASS at 701-line
`b21c0da` — re-key or retire next calibration round); SC1's registry-vs-probe
row for the citation-drift implementation; round-2 drift record's
alibaba-token characterization correction (real diff: opencode-go-7 tables,
CR8 §3b). Retired: none.

## arc2-loop1-round4 — depth + operability + freshness: three claims admitted, 2026-10-18

Round 4 of the reset window (4/10). **All three claims verify — round
admitted.** Parent-integrated; 64 seats dispatched, 60 reports delivered
(4 non-completions, third consecutive — the dispatch defect class is now
standing; root cause uninvestigated, named debt).

- Wave: 64 seats on `devin/deepseek-v4-1-flash-max`; reports
  `.ufo/waves/arc2-loop1-round4/`. Landed at `265e1aa` + `fc8e53c` (lane
  identity; a mid-round artifact-only commit `1692acb` under a non-lane
  identity `v <v@x>` pre-exists — see Defects below).
- Landed (C1): `SKILL.md` queue-drain rule #11 — citations into
  operator-mutable files anchor by stanza key + receipt, never bare line
  numbers (the :1284→:2938→:3225→:3296 churn chain as evidence; text
  token-free per E21 so the census reads no new locus). Same commit:
  `SHONEN.md:6` refresh (`81-217`, 11/11).
- Landed (C2): the citation-drift **probe** committed at
  `.ufo/gates/citation-drift/` (probe `7989ed4e…`, 453 lines; table
  `edaa4e59…`; expected `6ebada28…`) + registry row in `SKILL.md` — kind=probe
  per PROTOCOL:363-364 (drift reported at rc 0, never failed; 2 =
  could-not-evaluate; `--strict` restores the gate map). Built from Z1's
  convergence seat (R3's F1/F2/F3 + the false-clean root path Z1 found and
  fixed applied); zero graded config.toml line numbers (rule #11 form).
  Capability row entered below.
- Landed (C3): census v10 (`.ufo/gates/c1-census-v10.py`, v9
  `213fe679…` re-keyed per Z1 §4d: two fixed-bound DATED rows + RECEIPT
  widening) — **PASS 0/0/0/0 at the work tree**; the open-ended-bound
  laundering path (CR3/P3/R3, measured) was refused. Plus the lessons:82
  append-only erratum (18-line content-anchored block, prefix-identity
  proven, 206-line result).
- Measured at `265e1aa`: command A **rules 10 → 11, 11/11 resolvable**,
  79/79, coverage 10.0 / depth 10.0; probe selftest 10/10 CLEAN + findings=0
  exit 0 at `1692acb`; census v10 PASS. Custody: pre-pair 19:03:02Z 5/5;
  **in-window drift 19:17:21Z** (7th config state today, `e0634d8c…`, stanza
  :3155, 141 model-table lines deleted, pin value unchanged; writer =
  interactive Kimi session `session_2a39273f`, V1) — config.toml zero-drift
  VOID as bare (second consecutive in-window event); other four paths held;
  post-pair 19:44:52Z 5/5 against the new baseline; drift record committed.
- Round infrastructure: the decisive 91.6MB PE run (contained per CR2:
  systemd scope 7G/1G-swap, disk TMPDIR, 7200s deadline) **OOM-killed itself
  at its own memory cap in 4m42s** — the containment worked exactly as
  designed (kernel `CONSTRAINT_MEMCG`, one in-scope victim, zero bystander
  kills, REA's envelope mislabels it `cancelled`). The wall is memory (10
  decompile workers 3.6GiB + JVM 3.2GiB), not time; next attempt carries the
  `REA_GHIDRA_DISABLED_ANALYZERS` lead with worker reduction. `reset-failed`
  executed (CR4's residue duty).

| Axis | Before → after | Verdict |
|---|---|---|
| depth — C1 | queue-drain rules 10 → 11, resolvable 10/10 → 11/11 (command A at `265e1aa`); rule #11 carries the round-3 churn chain + errata citations; craft rules 1-10 byte-identical | improved |
| operability (fleet; capability acquisition) — C2 | no citation-drift tooling → committed probe (selftest 10/10, findings=0 at HEAD, could-not-evaluate paths each exit 2 with a verdict line) + SKILL.md registry row + capability row entered; probe/report semantics per PROTOCOL:363-364 | improved |
| freshness (fleet) — C3 | census verdict FAIL(undeclared=2, unreproducible at HEAD) → v10 PASS 0/0/0/0 at the work tree (fixed-bound re-key; laundering path refused) + lessons:82 discharged (content-anchored erratum) | improved |
| coverage | 10.0 → 10.0 (79/79 at `265e1aa`) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (the pointer class now
has a standing detector + a durable citation rule; the census instrument is
revision-stable again); discernment improved (three-way convergence culture:
four rule drafts measured identical, one landed; the false-clean probe path
caught by Z1 and fixed before landing; CR1's over-breadth attack scoped the
rule to asserting citations).
Capabilities: `| citation-drift probe | reports (never fails) drift on the
lane's pinned in-repo citations; --strict restores gate semantics | .ufo/gates/citation-drift/ (registry entry SKILL.md); selftest 10/10 at 265e1aa | arc2-loop1-round4 |` entered.
Planned: the memory-scoped PE retry (disabled-analyzers + worker reduction);
C1's blast-radius debts (below). Carried debt (named): `lessons:37` and
`LOG.md:685`'s SKILL citations moved onto rule #11's text by the +12 shift
(already drifted pre-round; S1/E18 verified); `evidence/round-1-2026-10-15/
rubric.json:61` same class; the 60/64 dispatch defect class (3 rounds
running); the probe's frozen-run guard (R6: expected.json pins no digest of
pointer-table.json — probe-exempt by kind, gate-blocking if ever promoted);
GhidraClient.js:607's version-relative line citations (E7); E22 v9's
superseded fence (v10 is canonical now). Defects recorded: **`1692acb` — a
non-lane-identity commit (`v <v@x>`) landed mid-wave by seat V5's scratch
chain (a /tmp-quota abort skipped its `cd`; `git add -A && git commit` ran at
the repo root): 4 pure additions, zero modifications, no custody path; kept
in history per the no-rewrite rule; stray `e16-table.json` removed in
`265e1aa`; seat pipelines must never run git mutations (next dispatch
reinforces).** Retired: none.

## arc2-loop1-round5 — verification round: calibration audit, 2026-10-18

Round 5 of the reset window (5/10). Per schedule: the loop-1 verification
round (64 declared seats, `openai-codex/gpt-6-luna-max`), auditing rounds
1-4. **Round admitted: all three claims verify** — on the strength of the
discrepancies found, not despite them.

- Wave: the dispatch carried 60 seat items (the declaration said 64 — see
  C2); 60 reports delivered, 100% completion. Reports
  `.ufo/waves/arc2-loop1-round5/`. Landed at `9ce9ff9` + `3f4a685`.
- C1 calibration (owned) — measurement audit. Authoritative matrix (C1
  connector, 20 rows): **20 audited / 13 confirmed / 7 dispositioned**, all
  re-derived from `git archive` trees at the cited commits (archive fidelity
  independently verified 1,458 paths byte-identical, V4). Confirmed: command A
  at all four work commits (10/10 at df31bfb, b21c0da, dbba2dd; 11/11 at
  265e1aa); r4's probe selftest 10/10 + findings=0; r4's census v10 PASS at
  265e1aa and 0e8c96b; r3's E23 unwarned metric 6→0 (scoped, E8); r1's
  receipt MANIFEST 8/8 + prefix identities intact at HEAD; r1's battery
  receipt hashes; README certification at b3cd790; r4's SHONEN refresh;
  archive methodology. Dispositioned (7): **(1) the arc's dispatch counts —
  see C2 (corrections naming the superseded lines in this section); (2)** r2's
  "6 hard-stale" re-derives as **5 stale + 1 ambiguous** (P1/S2/R1
  convergent; the r2 section's count overstated by one — this entry is the
  append-only correction; the reconciliation itself is unaffected); **(3)** r2's
  census PASS is receipt-scoped: v10 cannot replay the r2 tree (scope-marker
  incompatibility, E5) — v9's own fence records the PASS and replays PASS at
  `b21c0da` (S2); adjudicated, not falsified; **(4)** r3's raw dead loci
  6→12 (append-only keeps dead lines; the claim's unit was "unwarned",
  stated) and historical minted=0 unreplayable without the `bd5a78d1…` config
  snapshot (receipt-scoped; the 19:17Z/19:44Z churn moved the stanza again);
  **(5)** r4's probe on `--rev deadbeef` reports findings at rc 0 instead of
  could-not-evaluate exit 2 (registry row's declared map — named debt, fix in
  a future operability round); **(6)** CR4's axis honesty point accepted in
  part: cited-commit reruns test reproducibility; the calibration content
  comes from the disposition of the discrepancies (this section); **(7)** the
  r3 honest-stop verdicts affirmed in retrospect (E15: the r3 gate-form
  NOT-VERIFIED and C2 INCONCLUSIVE both remain correct given r4's evidence).
- C2 operability (fleet) — the dispatch-count defect class **identified and
  corrected**: rounds 2-4 (and the round-5 declaration) claimed 64 seats; the
  items arrays carried 60; all 60 completed every wave; the "4 non-completions"
  recorded in three round sections were fictional. Root cause: parent counts
  the intent, not the items array; the census caught it only because the
  verification wave reconstructed the roster from round 1's complete 64-name
  set (P3/E16/E17, archived-tree set differences). Mitigation landed:
  `corpus/lessons/2026-10-18-wave-dispatch-counting.md` (freeze the roster,
  count the items array, correct records append-only; re-dispatch protocol
  for true shortfalls). The lesson's README index row is **deliberately
  deferred** — inserting it at :165 shifts `corpus/README.md:177`, staling
  SCORECARD's landed pointer (caught pre-commit, reverted; lands with the
  next README-touching round's re-point).
- C3 freshness (fleet) — missed-item register per-item dispositioned (E19-E21,
  R3's exclusion of closed items applied): drifted-citation trio adjudicated
  (lessons:37 baseline-valid under :7 — NO-CHANGE; LOG:685 dated history —
  NO-CHANGE; rubric.json:61 frozen at baseline — NO-CHANGE); probe frozen-guard
  = named debt (probe-exempt by kind); E22-v9 fence = CLOSED (v10 canonical);
  GhidraClient.js version-relative citations = named debt; /tmp quota hazard =
  standing (seats relocated, evidence intact); lessons:82 erratum-internal
  tokens = instrument-predicted, unit stated. Zero unsafe source edits landed.
- Measured at `3f4a685`: command A 79/79, 11/11, 10.0/10.0 (unchanged — the
  lesson lives in corpus/lessons, outside the denominator); custody pre-pair
  19:50:16Z... (receipt at `config-pre-pair.txt`; V3's independent capture
  19:52:46Z matched 5/5; no live probes this round per the verification
  shape; post-pair 5/5 at close; SC2: no custody-path churn since the r4
  post-pair).

| Axis | Before → after | Verdict |
|---|---|---|
| calibration — C1 | R1-R4 measurement record unaudited → 20-row audit matrix: 13 confirmed at cited commits, 7 dispositioned (count corrections, the 5+1 restatement, receipt-scoping adjudications, named debts) — self-assessment now matches re-derived state | improved |
| operability (fleet) — C2 | "60/64 non-completion" defect (fictional, 3 rounds) → class identified as parent counting slip + roster-freeze/count-the-items protocol landed as a standing lesson; README index row deferred with cause | improved |
| freshness (fleet) — C3 | mixed carried-debt register → every item dispositioned (adjudicated / closed / named / operator-owned); zero unsafe edits | improved |
| depth | 10.0 → 10.0 (command A at 3f4a685) | unchanged |
| coverage | 10.0 → 10.0 | unchanged |

Learning trends: expansion unchanged; quality **improved materially** (the
verification round caught the arc's own records inventing a defect for three
rounds — the strongest possible argument for scheduled audit rounds);
discernment improved (CR4's axis-honesty attack accepted in part; the
re-dispatch protocol was drafted for the wrong premise and the audit rewrote
it before landing).
Corrections named here (append-only convention): SCORECARD round-2/3/4
sections' "64 seats / 60 reports / 4 non-completions" lines are superseded
(this section); the r2 "6 hard-stale" count is superseded by 5+1 (P1/S2/R1).
Planned: round 6 per schedule. Carried debt (named): probe --rev handling;
README lessons-index row + :177 re-point; GhidraClient citations; the memory-
scoped PE retry (disabled-analyzers); E11's unreproduced 0-byte probes; the
17.7MB rung. Process deviations recorded: seat P2 appended a LOG entry
mid-wave (content accurate, retained; seats do not write LOG — parent owns
records). Retired: none.

## arc2-loop1-round6 — coverage + operability + freshness: three claims admitted, 2026-10-18

Round 6 of the reset window (6/10). **Round admitted: all three claims
verify.** First wave of the arc at full declared strength: the items array
carried 128 seats, 128/128 reports delivered (the r5 counting lesson applied
— E26 froze the roster, E51 counted the dispatch, R6 reviewed the method).

- Wave: 128 seats on `xai-oauth/grok-4.7-fast`; reports
  `.ufo/waves/arc2-loop1-round6/`. Landed at `045c1b8` (C2) + `596df1c`
  (C1+C3) + `b910a33` (artifacts).
- C1 coverage (owned) — the scale-wall ladder advanced on two legs:
  **mid-rung HELD**: the 17.7MB agent-browser PE (17,694,720 B, sha256
  `a6a9a365…`) analyzed end-to-end in 2479 s at 6G heap — exit 0, evidence
  `ev_8b688ce7…`, 11 segments / 19,012 procedures / 4,382 strings, NATURAL
  (the envelope's `analyzer_preset` reads plain `ghidra-default` — the
  disabled-analyzers env was not in force; the hold is unmitigated).
  Landed as `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md` + the
  line-neutral map-token append (E8's r4 form — same physical line, no row
  insert): denominator **79 → 80**, command A at `b910a33` reads 80/80,
  missing [], dangling [], 11/11, 10.0/10.0. **Big leg honest-negative**:
  the 91.6MB retry (caller-independent user service `arc2-r6-pe`, 9G cap)
  sealed a typed refusal in 7.554 s — `execution_failure`, no evidence_id;
  my guessed analyzer name `Decompiler Parallel Convention Analysis` does
  not exist in Ghidra's registry (the registered name for that class is
  `Call Convention ID`, E3/E4), and REA aborts before disabling ANY name.
  Wall taxonomy now: round-4 memory-kill at 7G (10 decompile workers), this
  round's name-validation refusal — and the ladder brackets the wall with
  two live points (2.5MB/44s, 17.7MB/2479s natural). No token for the big
  leg; the refusal envelope is committed as a receipt.
- C2 operability — the citation-drift probe's `--rev` handling now matches
  its registry row: a dead/absent revision is a preflight could-not-evaluate
  (exit 2, finding `revision_unresolvable`) instead of seven bogus
  `citation_file_absent` rows at rc 0. Selftest 11/11 (P3's scratch-verified
  fix landed verbatim: preflight `git rev-parse --verify REV^{commit}` +
  one expected.json case + the SKILL.md self-invocation cell 10→11); frozen
  run and all other behaviors byte-stable (V4 re-ran the wave's bytes).
- C3 freshness — the r5-deferred pair landed together (Z2 measured the
  coupling: the insert alone stales the probe): README lessons-index row for
  the counting lesson (after :165, 187→188) + SCORECARD's
  `corpus/README.md:177`→`:178` re-point in the same commit; probe
  findings=0 and census v10 PASS verified post-landing.
- Measured at `b910a33`: command A 80/80, 11/11, 10.0/10.0; probe selftest
  11/11 + `--rev deadbeef` → exit 2 + `--rev HEAD` findings=0; census v10
  PASS (the section below is deliberately pin-free per Z1's measurement —
  a version literal in an undeclared append was measured `undeclared=1`).
  Custody: pre/post pairs 5/5 against their own baselines; the two
  user-service runs touched no custody path (C6/E28 fd scans); zero host OOM
  events (containment corroboration, SC1/E44).

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | knowledge 79/79 → **80/80** (mid-rung HELD, natural, ev-sealed; ladder: 2.5MB/44s → 17.7MB/2479s → 91.6MB wall with two named wall classes); big leg typed refusal recorded with envelope receipt | improved |
| operability (fleet) — C2 | probe dead-rev → 7 bogus findings at rc 0 → exit 2 `revision_unresolvable` matching the declared map; selftest 10 → 11 cases | improved |
| freshness (fleet) — C3 | r5-deferred index row + re-point landed as a coupled pair; zero probe/census regression | improved |
| depth | 10.0 → 10.0 (command A at b910a33) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion **improved** (a new verified surface — the first
denominator growth of the arc); quality improved (the wall taxonomy is now
three-class with live evidence; the honest-negative branches pre-written by
the wave meant neither refusal nor costume cost a round); discernment
improved (CR9's "costume retry" attack was verified in the envelope before
any claim; my own sed-pattern no-op on the token append was caught by the
grep gate, not by review).
Capabilities: no new row (the contained-run recipe remains round
infrastructure, not yet a demonstrated standalone capability).
Planned: round 7 per schedule. Carried debt (named): the renamed-analyzer
retry (`Call Convention ID` + `Decompiler Parameter ID`/`Decompiler Switch
Analysis` with validated names — E4's registry work); E62's capability-row
candidate (deferred — the recipe is not yet standalone-demonstrated);
README index row for the r6 lesson (same deferred-pair shape as r5's); the
round-4 E22-v9... closed (r5). Retired: none.

## arc2-loop1-round7 — coverage (the wall falls) + depth + freshness: three claims admitted, 2026-10-18

Round 7 of the reset window (7/10). **Round admitted: all three claims
verify.** Light round per schedule: 24 seats on `zai-coding-plan/glm-5.3-flash`,
24/24 delivered (items array counted at 24 — the r5 lesson holds).

- Wave: reports `.ufo/waves/arc2-loop1-round7/`. Landed at `8cc81a8` +
  `bd3b962` (artifacts).
- C1 coverage (owned) — **the 91.6MB scale wall falls**. Third engagement,
  first with registry-validated analyzer names: user service `arc2-r7-pe`
  (caller-independent per rule-#12's own prescription), 9G cap, raised
  deadline, three validated names disabled. Sealed HELD (mitigated):
  envelope 5204 B (sha256 `a77ebee8…`, committed as a receipt), exit 0, wall
  1424.663s (deadline unused), journal 42m35.7s CPU / 7.9G peak with zero
  OOM lines, `ev_a4aa9b0d…`, 9 segments / **75,218 procedures** / 137,345
  strings, `analyzer_preset` recording all three disabled names. The disable
  is proven honored (E3: ghidra.log:276 pre-script validation, re-read false
  before `ANALYZING`), the memory driver is identified (E1: **zero decompile
  workers** at all watch samples vs round-4's 10 workers/3.6GiB; peak past
  round-4's 7G death point under the 9G cap). Landed as
  `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + line-neutral map token:
  denominator **80 → 81** (command A at `bd3b962`: 81/81, missing [],
  dangling []). Two honest unknowns recorded: natural unmitigated hold at
  this size, rerun id-stability.
- C2 depth (owned) — queue-drain rule #12: long Ghidra analyze runs are
  transient caller-independent user services, not launcher-bound scopes —
  in the adjudicated form (R2/CR2/CR3's corrections applied: bounded
  preference, not a "never --scope" ban; the corrected round-4 story —
  containment worked, lifetime failed; caller-kill survival a named
  unknown). Cites the r6 mid-rung + r7 wall entries. Command A at `bd3b962`:
  **rules 11 → 12, 12/12 resolvable**; SHONEN:6 refreshed same commit
  (81-237, 12/12); token-free per E21 (census PASS).
- C3 freshness — the caller-independent-services lesson (adjudicated against
  the round-6 CR14 generic-advice attack: artifact-anchored, domain-bounded)
  + README lessons-index row + SCORECARD `corpus/README.md:178`→`:179`
  re-point as the Z2-measured coupled pair; probe findings=0 + census PASS
  post-landing.
- Measured at `bd3b962`: command A 81/81, 12/12, 10.0/10.0; probe selftest
  11/11 + findings=0; census v10 PASS (records below are pin-free per the
  measured constraint). Custody: pre-pair == service-start second (21:40:26Z,
  SC1); post-pair 5/5; the service touched no custody/repo path (fd scans);
  `reset-failed` executed on the spent r6 unit.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | knowledge 80/80 → **81/81** (the 91.6MB wall HELD, mitigated and proof-backed: 75,218 procedures, zero decompile workers, analyzer-disable honored); wall taxonomy closed — time, memory, name-validation classes all defeated by mechanism-matched responses | improved |
| depth — C2 | queue-drain rules 11 → 12, 12/12 resolvable (rule #12: caller-independent services, adjudicated bounded form, two corpus citations) | improved |
| freshness — C3 | r6-deferred lesson + index row + coupled re-point landed; zero probe/census regression | improved |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion **improved** (the arc's second denominator growth,
and the first mitigated hold); quality improved (the wall taxonomy is closed
with per-class mechanisms and receipts; every claimed number converged across
six independent seats); discernment improved (CR9's costume-attack class was
pre-empted by validated names; CR1's sunk-cost attack answered with a stop
rule — a fifth engagement without a new mechanism retires the thread).
Capabilities: no new row. Planned: round 8 per schedule. Carried debt
(named): the natural-preset 91.6MB control; rerun id-stability; E4's open
`getNumAddresses()` question; the r7-lesson's own index row (same deferred
coupled-pair shape); probe-table coverage of the new citations (gap analysis
E41 — non-blocking, probe is advisory). Retired: none.

## arc2-loop1-round8 — operability + freshness + calibration: three claims admitted, 2026-10-18

Round 8 of the reset window (8/10). **Round admitted: all three claims
verify.** Light round per schedule: 20 seats on `zai-coding-plan/glm-5.3-flash`,
20/20 delivered (items counted at dispatch; the roster-freeze file is still
not wired — 4th wave, named debt).

- Wave: reports `.ufo/waves/arc2-loop1-round8/`. Landed at `6bc4c29` +
  `d0d2575` (artifacts).
- C3 calibration (owned) — the natural control, sealed decisively: user
  service `arc2-r8-ctl` ran the same 91.6MB target with NO disabled analyzers
  (absence verified on both channels — unit env + options pre-script) under
  the identical cap/deadline/heap as round 7, and was kernel-OOM-killed at
  the 9G cap in 4m42.945s with 10-12 decompile workers — round-4's kill
  profile reproduced (journal `decompile invoked oom-killer`; envelope typed
  `cancelled`, no evidence_id — the r4 mislabel class; receipt committed).
  Attribution per the pre-registered dichotomy: **the disable is proven
  NECESSARY**; round 7's attribution sentence was scoped, not corrected, by
  append-only erratum on the wall entry (the worker-elimination mechanism is
  corroborated by the mitigated run's zero-worker profile). The r7 entry's
  named unknown "natural unmitigated hold" resolves: none exists at this cap.
  R1's fairness matrix: only the disable differed. In-window custody drift
  (config.toml, operator-side churn class) recorded; post-pair re-baselines.
- C1 operability (fleet; capability) — the contained user-service analyze
  capability row enters (AXES.md §Capabilities): scoped per the wave's
  constraints (R2/CR2) to the analyzer-disable recipe, first-working round 7,
  with the r8 kill cited as the necessity proof, not containment evidence.
  Insertion coupled with the instrument re-keys the wave measured (census
  v10 SCOPE +1 on three DATED rows; probe sc698 re-pin) — all in the same
  commit, both instruments green post-commit.
- C2 freshness (fleet) — re-scoped mid-wave (the wave caught that the
  declared reading was already landed in round 7 — double-count avoided):
  the mechanism-matched-walls lesson + README index row + SCORECARD
  `corpus/README.md:179`→`:180` coupled re-point; probe findings=0 post-landing.
- Measured at `d0d2575`: command A 81/81, 12/12, 10.0/10.0 (the capability
  row and lessons ride outside the measured surfaces); probe selftest 11/11
  + findings=0; census v10 PASS with the re-keyed scope.

| Axis | Before → after | Verdict |
|---|---|---|
| calibration — C3 | r7 attribution single-arm (three variables changed vs r4) → controlled confirmation: kill at 4m42.945s/9G/10-12 workers vs hold at 1424.663s/7.9G/zero workers; r7 entry errata'd append-only; the lane's self-assessment is now experiment-backed | improved |
| operability (fleet; capability) — C1 | no contained-analyze capability → capability row entered (scoped, evidenced by the paired sealed demonstrations) | improved |
| freshness (fleet) — C2 | no r8 lesson/index row → mechanism-matched-walls lesson + row + coupled re-point (double-count of r7's row avoided by the wave's catch) | improved |
| coverage / depth | 10.0 / 10.0 (command A at d0d2575) | unchanged |

Learning trends: expansion unchanged; quality improved (attribution by
controlled experiment — the strongest evidence class the lane has produced);
discernment improved (the wave re-scoped its own freshness claim when the
records contradicted the premise; the probe-vs-worktree grading lesson is
recorded).
Capabilities: `| contained user-service analyze of oversized PEs
(analyzer-disable recipe) | ... | arc2-loop1-round7 |` entered.
Planned: round 9 per schedule. Carried debt (named): roster-freeze file (4th
wave); natural control at the old 7G cap (does the cap alone matter? —
lower-value, named); r8 "zero workers" claim unverified for the natural run
(R3's note — the claim is about the mitigated run only); README:22/:174 stale
pre-fall wall text (R2 — next README-touching round); rerun id-stability.
Retired: the 91.6MB wall thread per CR1's stop rule (a ninth engagement needs
a genuinely new mechanism).

## arc2-loop1-round9 — freshness + depth + operability: three claims admitted, 2026-10-18

Round 9 of the reset window (9/10). **Round admitted: all three claims
verify.** Light round per schedule: 24 seats on `openai-codex/gpt-6-luna-max`
(operator substitution, recorded), 24/24 delivered (items counted; the roster
was frozen retrospectively this round — the pre-dispatch wiring lands via C3's
lesson amendment).

- Wave: reports `.ufo/waves/arc2-loop1-round9/`. Landed at `ba06c4d` +
  `3fb6803` (artifacts).
- C1 freshness — the stale pre-fall wall text, with CR1's correction applied:
  the current-state rows (`corpus/README.md:22` map row, `:175` frontier
  bullet) now state the fall (r7 mitigated hold + r8 natural control, with
  the r8 attribution carried via the erratum/journal — the receipt's
  `cancelled` wrapper is not itself the OOM diagnosis, R1's limit observed);
  the dated r4 synopsis at `:117` stays historical. Same-line rewords, zero
  shift; stale-wall-state rows 2 → 0.
- C2 depth (owned) — queue-drain rule #13: a mitigation claim carries its
  natural control (same target, caps, deadline; only the treatment absent;
  compare paired outcomes before attributing necessity) — bounded to the
  tested envelope, two corpus citations, token-free per E21. Command A at
  `3fb6803`: rules 12 → 13, 13/13 resolvable; SHONEN:6 refreshed same commit
  (81-243, 13/13).
- C3 operability — the roster-freeze debt closes honestly: the round-9 roster
  is frozen as `receipts/roster-frozen.txt` (retrospective — stated in its
  header), and the counting lesson gains the wire-it amendment: pre-dispatch
  roster + a `len(items) == roster rows` assertion in the dispatch command;
  rounds 10+ freeze pre-dispatch.
- Measured at `3fb6803`: command A 81/81, 13/13, 10.0/10.0; probe selftest
  11/11 + findings=0; census v10 PASS; custody pre/post pairs 5/5 on their own
  baselines (no live probes this round).

| Axis | Before → after | Verdict |
|---|---|---|
| freshness — C1 | stale pre-fall wall-state rows 2 → 0 (current-state cells reworded same-line; dated synopsis preserved) | improved |
| depth — C2 | queue-drain rules 12 → 13, 13/13 resolvable (rule #13: mitigation carries its natural control) | improved |
| operability — C3 | roster-freeze unwired (4 rounds of debt) → frozen roster artifact + the wire-it amendment (pre-dispatch gate for rounds 10+) | improved |
| coverage / calibration | 10.0 / 10 (command A at 3fb6803) | unchanged |

Learning trends: expansion unchanged; quality improved (the README now
matches the sealed record; the dated/current boundary is explicit); discernment
improved (CR1 caught the wrong-second-row in the round's own claim and the
parent folded it pre-landing; R1's receipt-vs-journal attribution limit is
preserved in the reworded text).
Planned: round 10 per schedule (hyper/deepseek-v4.1-flash, 64-128 seats).
Carried debt (named): roster pre-dispatch wiring (lands operationally at
round 10); rerun id-stability; README:117 stays dated (correct); the r4-row
capability backfill (r8's E3 observation — r4's citation-drift row never
entered the capabilities table; low value, named). Retired: none.

## arc2-loop1-round10 — calibration + freshness + adjacency: three claims admitted, 2026-10-18

Round 10 of the reset window (10/10 — window complete; capabilities entered
at rounds 4/8, so the stagnation nudge does not fire). **Round admitted: all
three claims verify** (C1 as a split verdict: one scale point closed, one
named debt — pre-accepted in the round declaration).

- Wave: 64 seats frozen PRE-DISPATCH (the r9 gate's first operational run —
  roster + items assertion held); ~59/64 reports delivered — the operator
  interrupted the wave (44 completed at interruption + late writes); the
  deficit is recorded per the counting lesson, not backfilled. First wave on
  `hyper/deepseek-v4.1-flash` (operator substitution, recorded).
- C1 calibration (owned) — rerun id-stability, split per the pre-accepted
  shape: **BIG leg CLOSES the question** — `arc2-r10-big` re-ran the exact r7
  request (identical target bytes, analyzer set, caps, heap; only the scratch
  TMPDIR differed) and sealed a 5204-byte envelope **byte-identical to the r7
  receipt** (`cmp` exit 0, parent-verified), same `ev_a4aa9b0d…`: id stability
  is STABLE at the 91.6MB scale point, the id is scratch-path-independent and
  carries no timing term (wall 1424.663s → 1438.082s, envelope unchanged).
  The r7 entry is errata'd + its recheck line corrected (same commit as the
  C2 table — Z1's measured coupling). **MID leg = named debt** — `arc2-r10-mid`
  was kernel-OOM-killed at 9G in 53.602s: the rerun added a 9G cgroup cap that
  the r6 run never had (r6 ran uncapped at a measured 18.26 GiB tree peak), so
  the kill is a recipe-provenance error, not a reproducibility result; the r6
  entry's erratum names the containment requirement (a faithful retest runs
  uncapped or above 18.3G). Z1's discipline note: do NOT claim "two scale
  points" — one was answered.
- C2 freshness — the citation-drift probe table extends 13 → 31 entries (E8's
  draft, CR2-constrained: the "frozen-run" leg restated as a manual rerun at
  the pinned revision; the advisory classification preserved). The extension's
  first live catch fired in-round: `readme175-sc1217`'s needle expected the
  retirement line at SCORECARD:1216 where the id-stability debt line lives —
  corrected and re-verified (findings=0, selftest 11/11). Coupled re-point:
  README:175's SCORECARD citation :1217 → :1216 (P3's catch, same commit).
- C3 adjacency — the hyper-lane substitution census, recorded operator-facing
  (not absorbed): delivery ~59/64 under interruption (vs devin-lane 100%
  completion — the interruption is operator-side, not lane-side; no
  provider-quality conclusion is drawn from an interrupted wave); report
  quality/convergence spot-checks comparable to devin-lane patterns (E10/E11
  samples); the full census rides in the round report. The kimi config's
  drifted state (hyper-era) is harness config, recorded not attributed.
- Measured at the records commit: command A 81/81, 13/13, 10.0/10.0; probe
  selftest 11/11 + findings=0 (post-fix); census v10 PASS. Custody: pre/post
  pairs 5/5 on their own baselines; both services touched no custody path;
  containment corroborated (both kills in-scope, zero bystanders).

| Axis | Before → after | Verdict |
|---|---|---|
| calibration — C1 | r7/r6 "rerun id-stability UNKNOWN" → r7's unknown CLOSED (byte-identical re-derivation; id domain measured — RFC 8785 canonical JSON, excludes subject.name/local_path); r6's unknown = named debt with the containment requirement measured (uncapped 18.26 GiB peak) | improved (split per the pre-accepted shape) |
| freshness — C2 | probe table 13 → 31 entries (r7/r8 citations + SHONEN pointers; advisory semantics preserved); the extension's first live catch fixed in-round | improved |
| adjacency — C3 | no hyper-lane evidence → operator-facing census recorded (delivery under interruption, quality samples, no absorption) | improved |
| coverage / depth | 10.0 / 10.0 (command A at the records commit) | unchanged |

Learning trends: expansion unchanged; quality **improved materially** (id
stability by byte-identical re-derivation — the strongest reproducibility
evidence the lane holds; the id domain itself measured from source);
discernment improved (Z1's "reject two scale points" discipline; the mid-leg
kill read as provenance, not reproducibility; the wave's interrupted state
prevented any provider-quality conclusion — recorded as operator-side).
Planned: round 11 per schedule. Carried debt (named): the mid-leg faithful
retest (uncapped or >18.3G — operator-host-cost gated); the 5-seat r10
deficit (interruption, not re-dispatched per the counting lesson's
operator-decision rule); the C3 census's full table (wave-interrupted, the
samples stand). **Operator directive this round: PUSH to remote authorized by
the operator ("finish this round and push to remote") — executed after the
records commit; the standing no-push scope rule yields to the explicit
instruction and is restated here for the ledger.** Retired: none this round.

## arc3-loop1-round1 — coverage + operability + freshness: three claims admitted, 2026-10-19

Round 1 of a new stagnation window (1/10; the arc2 window closed 10/10). First
wave of the arc on the opencode-go lane (key 1 of 7, round robin). All three
owned proxies stay saturated at 10.0; coverage is the owned axis (three-way tie,
most-falsifiable-next-claim tie-break per luna-round-2 precedent); operability
and freshness ride the standing fleet-axis recording ruling. The wave was
interrupted by the harness at its tail; the delivered fraction is recorded, not
backfilled (the r10 precedent — interruption is operator-side, not lane-side).

- Wave: 64 seats, roster + items-array assertion held pre-dispatch (the r9
  amendment's first arc3 run). 54/64 seat reports delivered. Undelivered:
  EX-03 (source only), EX-14 (artifacts, no report), EX-25, EX-27, EX-28 (edit
  landed; report missing), EX-31 (artifact, no report), RV-9, SC-5, VZ-2, VZ-3,
  VZ-4 (verdict packets landed; reports missing). Seat artifacts covered most
  gaps; the wave integrator's first-hand re-verification covered both
  authorized real-target edits.
- C1 coverage (owned) — EVM real-bytecode leg, the r3-07 frontier. Landed at the
  work commit: solc installed on-host under an isolated wave prefix (receipt:
  tarball sha256 `0e1a1ab6…`; an ambient global copy pre-existed — the receipted
  prefix carries the provenance); four ERC-20-shaped carriers compiled on-host;
  probe recovered planted selectors K/K, zero extras, on every runtime leg
  (5/5, 6/6, 9/9, and an 11-selector attack carrier), creation-code legs
  honestly parsed-and-empty; raw/hex legs agree; rerun ids re-derive; an
  independent keccak + linear-sweep disassembler recon reproduced every set and
  offset (ALL SOURCES AGREE). The new knowledge entry landed with the critic's
  recheck fix (disk-backed TMPDIR — the host's `/tmp` quota fails this probe),
  the refuted-hypothesis note (r3-07's candidate-2, measured dead), and its
  fresh identity recorded (10,225 B, sha256 `dd986f56…` — the wave's own
  claimed hash was stale after a mid-wave revision; fresh hash recorded per the
  critic's F2). The map row gained the token + a state-cell refresh, one
  physical line (190 → 190).
- C2 operability (fleet) — citation-drift frozen-run guard (arc2 r4/r5 named
  debt). Landed at the work commit: `expected.json` pins the pointer table's
  sha256; tampered / absent / unpinned baselines each hit the declared
  preflight exit-2 class; selftest 11 → 13; probe findings = 0 at HEAD in both
  modes; the registry row states the guard semantics (one merged row, the
  planner's v3 text with the code-true finding ids — two rival patch texts
  deliberately not landed). Named: custom-table experiment recipes must now
  carry a custom pinned expected (behavior change, recorded in the row).
- C3 freshness (fleet) — census E22 disposition, honestly framed PASS→PASS: the
  debt's FAIL class reproduces only on historical trees (v9 recovered
  byte-exact from the round-2 evidence; FAIL at the 766-line tree, PASS at the
  701-line tree); at HEAD the census already reads PASS (the r4/r8 re-keys
  closed the debt — manufactured FAIL→PASS correctly not staged). The wave
  found one latent marker-line defect (a committed PROVINCE row's marker sat
  outside its own range), re-keyed it, and added a G18 assertion that fired on
  its own intermediate state (live non-vacuity, parent-verified). Disposition
  stated in the instrument header; creep audit clean (0 flags).
- Custody: 5-path pre-pair before any install/probe; post-pair at close; 5/5
  byte-identical across the wave (parent capture + five seats).
- Measured at the work commit: command A **82/82, missing [], dangling [], 13/13
  rules, 10.0/10.0**, prior-81 byte-identical (one file added, one README line
  reworded); probe selftest 13/13 + findings=0; census PASS 0/0/0/0. Instruments
  re-run green at the records commit (this section is pin-free per the
  connector's injection test — no bare version pin, no absolute `path:line`).

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | 81/81 → 82/82 (real-solc EVM leg admitted, quality-gated; proxy held at the larger denominator) | improved |
| operability — C2 | no frozen-run guard → guard committed and independently re-verified (13/13; declared exit-2 classes) + registry row states semantics | improved |
| freshness — C3 | E22 open since r4 → disposition measured (historical-tree reproduction), latent marker defect re-keyed, header record landed, PASS 0/0/0/0 | improved |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion **improved** (first denominator growth since arc2
r7); quality improved (fresh-hash discipline on a churned artifact; one merged
registry row out of three candidates; the recheck line carries its host
requirement); discernment improved (a manufactured verdict flip refused; the
planner's text chosen by code-truth over rival patches; the wave caught its own
stale self-verification and the parent landed the fix).
Planned: round 2 per schedule (opencode-go key 2 of 7). Carried debt (named):
the ten-seat report deficit under interruption (no backfill per the counting
lesson); EX-03's seat-level delivery gap (its work covered by other seats);
creation-code legs parsed-and-empty (scope stated in the entry); census latent
holes (absent-file fail-open; inline-marker excusal; blind-instrument pass;
self-certification — each with patch text in the wave); the pre-existing dirty
path `.ufo/waves/arc2-loop1-round10/C3.md` (not this round's, left
uncommitted); host `/tmp` quota exhaustion (environmental; recipes must carry
disk-backed scratch). Retired: none.

## arc3-loop1-round2 — depth + freshness + operability: three claims admitted, 2026-10-19

Round 2 of the reset stagnation window (2/10). Wave: 64 seats, opencode-go key 2
of 7; **64/64 seat reports delivered** (first full-delivery wave of the arc).
Owned axis worked: depth (three-way tie at 10.0, most-falsifiable tie-break).

- C1 depth (owned) — queue-drain rule #14: self-identity re-derivation
  discipline, from the measured arc3-r1 incident (a revised entry patch whose
  self-verification hash went stale; caught by the wave's critics). Landed as a
  **form-fixed** payload (the planner/reviewer citation-form fix: the SCORECARD
  reference anchors by section key, not a bare range — landing the seat's raw
  text verbatim would have failed the claim's own rule-#11 clause, measured).
  Before → after: rules 13 → 14, 14/14 citation-resolved at the work commit
  (command A); prior 13 rules: pure insertion, 0 modified bytes,
  rstrip-normalized byte-identical (the raw block-split reads 12/13 on
  separator attribution — the precise phrasing, per the chain verdict).
  SHONEN.md:6 refreshed in the same commit (range 81-255, 14/14). Landed
  SKILL.md identity re-derived at landing (390 lines, `c134afcb…`) per the rule
  the round lands. Not instrument-enforced: the census and probe are blind to a
  stale self-identity (measured) — compliance is reviewer-enforced plus the
  chain's mechanized replay; the record says so.
- C2 freshness (fleet) — census fail-closures H1+H3 (arc3-r1 named debt, patch
  texts from that wave). Landed at fresh identity `d0772ce8…` (610 lines): an
  absent scoped file now FAILs `UNREADABLE` (named, every shape: absent,
  zero-byte, truncated, directory, EACCES); neutered needles now FAIL
  `BLIND-INSTRUMENT` (per-readable-file floor over current-ok detections).
  Every round-1 silent-PASS injection in the two classes reproduces as a
  declared FAIL; the ordinary run stays PASS 0/0/0/0; scope bounds byte-stable
  (two independent creep audits, 0 flags); guard cost measured neutral. A
  mid-wave revision (block-unit floor) false-FAILed the ordinary run and was
  caught in-wave by four seats — recorded as a caught defect, not shipped.
  Residuals stay named: H2 (inline-marker excusal), H4 (self-certification —
  the external diff audit remains the certificate), H5/H6.
- C3 operability (fleet) — custody receipt v2: `.ufo/gates/custody-pair/`
  committed (tool `112d01dc…`, 889 lines; README `fa484d57…`); selftest 15/15;
  receipts carry sha256 + mtime epoch with a TZ-independent UTC render (the v1
  local-under-UTC label defect is gone — and the tool *detects* the defect when
  re-reading v1 receipts, exit 12 with the sha256 contract intact) + inode +
  ctime_ns. Same-content rewrite visibility: 0/13 attack forms under v1-style
  sha256-only custody → 13/13 detected under v2 (rename and in-place classes;
  for restore-tool replays that preserve the inode, ctime_ns is the
  load-bearing pin — measured). v1 receipts remain verifiable on the sha256
  fields: a sums-form v1 reads MATCH-V1-PARTIAL exit 0; a label-defective v1
  stanza reads exit 12 with SHA256-CONTRACT 5/5 — both numbers quoted by
  design. One merged registry row landed (planner/executor texts merged; the
  real exit map stated). Threat-model boundary, recorded in the row's round:
  the tool is a tripwire for attribution, not an integrity control against an
  actor sharing its trust domain. Named debt D1-D7 (capture TOCTOU measured
  2/300; EACCES fail-open; partial-reference verify; receipt self-authentication
  out of band; write-guard scope).
- Custody outcome: 4/5 paths byte-identical across the wave and integration;
  the Kimi client config (custody path 3 of 5) drifted between the parent's
  integration captures — the v2 tool's first **live** catch, on exactly the
  operator-side interactive-session churn class documented since arc2;
  recorded verbatim, not repaired (operator-owned surface).
- Measured at the work commit `28aa7a9`: command A 82/82, missing [], dangling
  [], **rules 14, 14/14**, 10.0/10.0; census PASS 0/0/0/0; probe findings=0
  (both modes) + selftest 13/13; custody selftest 15/15.

| Axis | Before → after | Verdict |
|---|---|---|
| depth — C1 | rules 13 → 14, 13/13 → 14/14 citation-resolved at the work commit (pure insertion; prior rules rstrip-byte-identical) | improved |
| freshness — C2 | absent-file + blind-instrument classes silent-PASS → declared FAILs (`UNREADABLE`, `BLIND-INSTRUMENT`); ordinary run PASS; scope byte-stable | improved |
| operability — C3 | no committed custody tool → v2 tool committed (15/15; rewrite visibility 0/13 → 13/13; label defect gone and detected; v1 sha256-compatible) + registry row | improved |
| coverage | 10.0 → 10.0 (measured, 82/82) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion unchanged; quality improved (form-fixed landing
over verbatim seat text — the freeze's own clause caught a defect the metrics
would have passed; fresh identities re-derived at landing across all four
shipped objects; the caught-in-wave floor revision recorded, not smoothed);
discernment improved (the v2 tool's first live catch recorded as operator-side
with the writer class named, not absorbed as lane debt).
Planned: round 3 per schedule on the amended rotation — operator directive: the deepseek-v4.1-flash swarm waves ride the token-plan lanes (round 3 = token-plan key 1 of 3). Carried debt (named):
census residuals H2/H4/H5/H6 + partial-needle narrowing; custody D1-D7; the
pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` (not this round's);
host `/tmp` quota exhaustion (standing); the config.toml custody drift
(operator-owned, recorded). Retired: none.

## arc3-loop1-round3 — coverage + operability + freshness: three claims admitted, 2026-10-19

Round 3 of the reset stagnation window (3/10). Wave: 64 seats frozen pre-dispatch
on token-plan key 1; the lane hit its **monthly quota mid-run** (43 reports
landed); per the operator directive the remaining seats re-dispatched on the devin
lane (18 of 21 backfilled; final census 62/64 — EX-14 and SC-3 reports pending
with complete artifact trees). Substitution recorded with cause, not a lane
signal. Owned axis worked: coverage.

- C1 coverage (owned) — EVM optimizer-enabled + non-ERC-20-shaped carriers, the
  r1 entry's named Unknown. Landed at work commit `c418be0`: the new entry
  (18,596 B / 37 lines, fresh identity `bf39c584…`) with **seven reviewer fix
  sets applied pre-landing** — a false JUMPDEST-offsets line (the hand-assembled
  control's declared immediates sit 2 bytes before its JUMPDESTs), an internal
  contradiction, a citation overclaim (five nonexistent files), dead paths, two
  size labels, and the id-comparator advice (compare by decoded bytecode sha,
  not the costume-carrying subject digest); the additive map token kept the row
  line-neutral (README `a451ad16…`, exactly the four-seat-projected hash). The
  r1 entry received an **append-only erratum** (creation blobs do embed their
  runtime dispatch tables; the `16ee4b79` constant is a CBOR-trailer metadata
  artifact) — fresh identity `5761003f…`, historical records untouched. Measured:
  optimizer-on/off same-source controls recover identical selector sets across
  two pins; binary-search dispatch layouts at K=8/11/13; zero false positives on
  decoy constants; K/K on 8 carrier families.
- C2 operability (fleet) — custody-pair hardening (the round-2 verdict's own D
  series). Landed: tool `7cd19c3c…` (1155 lines) + README `f30df42e…` (185
  lines) + one registry-row voice in the same commit. The four holes closed with
  declared classes: exists-but-unreadable → `UNEVALUABLE` (exit 14, never a
  fail-open MATCH); reference coverage gated (`--require-paths`, USAGE exit 2
  naming the unaccounted canonical paths); the write guard now covers
  `set(paths) ∪ CUSTODY_PATHS` by resolved path and inode (hardlink and symlink
  aliases refused); selftest scratch-base → USAGE. Selftest 15 → 22, every new
  case proven load-bearing by sabotage arms; the full round-2 regression matrix
  re-run (41/41 hold). The round's live pair (both receipts self-pinning the
  revised tool) verifies MATCH 5/5.
- C3 freshness (fleet) — citation-drift table arc3 coverage. Landed: 31 → 57
  entries (+26, 0 removed/modified/duplicated) + the quoted class 4 → 5. The
  acceptance census (every pinnable arc3 citation covered or adjudicated) reads
  12/12 on the durable surfaces; the one uncovered row (`LOG.md`'s record of the
  r2 SHONEN re-point) closed by the proposed quoted entry in the same commit.
  The C2↔C3 collision (the table anchored the custody row's precedence clause
  that C2's row revision rewrites — measured by four seats as a guaranteed
  `citation_dead` at the coupled landing) is resolved by the re-anchored
  optional-group needle + digest re-pin + same-commit landing; probe re-run
  clean. Residuals named: the exempt ledger's first clause is falsified by the
  table's own anchor rows (review-enforced, not instrument-enforced); anchor
  substring semantics; fragility ratings advisory.
- Custody: 4/5 byte-identical across the wave; the Kimi client config drifted
  pre-wave (12:57:45Z — the same operator-side interactive-session class the
  tool first caught in round 2; v1 re-reads therefore show their contract as
  4/5, recorded verbatim). The revised-tool pair is unaffected (drift
  predates its pre receipt; zero in-window drift).
- Measured at the work commit `c418be0`: command A **83/83, missing [],
  dangling [], rules 14, 14/14, 10.0/10.0** (prior 82 byte-identical: one file
  added, one README line reworded, one r1 append); census PASS 0/0/0/0; probe
  findings=0 in both modes + selftest 13/13; custody selftest 22/22; the
  five-path pair MATCH.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | 82/82 → 83/83 (optimizer-enabled + non-ERC-20 EVM carriers admitted, quality-gated; r1 errata appended) | improved |
| operability — C2 | four named fail-open/clobber/traceback holes → declared exit classes; selftest 15 → 22; guard extended; one row voice | improved |
| freshness — C3 | probe table 31 → 57 (+R1 quoted closure); arc3 citation census 12/12; collision re-anchored same-commit; findings=0 both modes | improved |
| depth | 10.0 → 10.0 (14/14 measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion **improved** (second denominator growth of the arc);
quality improved materially (seven fix sets applied pre-landing — two of them
claim-blocking false statements the metrics could not see; the r1 erratum
landed append-only with fresh identities per rule #14); discernment improved
(the C2↔C3 collision was predicted pre-landing by four seats, measured
end-to-end, and resolved by a coupled landing — the strongest cross-chain
coordination of the arc; the provider substitution was recorded with cause and
per-lane delivery counts, not smoothed).
Planned: round 4 per schedule (hyper lane, 32–64 seats; with token-plan
exhausted, any further deepseek-flash substitution rides the devin lane per the
operator directive). Carried debt (named): custody residuals (sidecar scope,
mkdir guard, coverage counting by stanza, both-sides-absent MATCH adjudicated
as declared design); census H2/H4/H5/H6 + partial-needle narrowing; the EX-12
control-expectation delta (pre-registered refusal vs measured parsed-and-empty);
EX-14/SC-3 reports pending (artifacts complete); the pre-existing dirty
`.ufo/waves/arc2-loop1-round10/C3.md`; host `/tmp` quota (standing). Retired:
none.

## arc3-loop1-round4 — coverage + freshness + operability: three claims admitted, 2026-10-19

Wave: 48 seats on `devin/deepseek-v4-1-flash-max` (the declared R4 fallback —
hyper exhausted at the provider, 402 on all seats within ~30s of dispatch;
token-plan monthly quota died mid-R3). All 48 seat reports delivered; three
chains VERIFIED. Claims measured at work commit `40de383`.

- C1 coverage — the r3-named Unknown (Vyper-compiled EVM bytecode) closed:
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` records
  vyper-0.4.3+commit.bff19ea2 (the round's one authorized install), runtime
  1,562 B, `inspect-evm-interface` 15/15 K/K at both pins (`ev_405e2a2a…`),
  `dispatch:"abi"`, a third dispatch shape (modulo-indexed jump table). The
  entry carries four review fix sets (the `69656e74` PUSH32-substring fix, the
  same-path sentence, the argument-count inference mechanism, the QUALITY.md
  citation) + EX-07's line-neutral 6.5.0-boundary correction applied to the r3
  sibling entry; `corpus/README.md` map token landed (84 files mapped).
- C2 freshness — PROVINCE staleness census + repairs. The wave's census grew
  6→9 under peer correction (F2's sub-cap organic core inspects exit 0; C2's
  "35 features" is a corpus miscount of its own 34-name list; C3's asar row
  names 9 where the host holds 12). Landed: EX-15's 8-hunk same-line set + EX-12's
  Core-asar-row patch + PL-2's coupled corpus erratum (the PROVINCE↔corpus
  coupling) — eight stale literals cleared + one adjudicated NO-CHANGE
  (`JEB (unprobed)` survives at :88 as shorthand for "no JEB surface held",
  the verb having been probed at r2 — corrected from "all nine cleared" by
  the round-5 sweep), 162→162 lines held, no line
  shifts above :116 (the SHONEN:12 clause at :114-116 preserved), B2 cites
  r12-02 AND r14-01 (the third input sub-class). `JEB (unprobed)` adjudicated
  NO-CHANGE-with-cause (the verb was probed; no JEB install exists).
- C3 operability — custody-pair residuals closed at commit `520341d`: sidecar
  scope, mkdir guard, distinct-path gate, both-absent ruling; selftest 22→28;
  registry row now carries the 28-case form. Probe findings=0 both modes.

Instruments at `40de383`: command A 83→**84/84** mapped, 14/14 rules,
10.0/10.0; census PASS 0/0/0/0; probe findings=0 both modes; pair MATCH 5/5.

| axis | evidence | verdict |
|---|---|---|
| coverage — C1 | corpus 83→84; the r3-named Unknown closed; 15/15 K/K both pins | improved |
| freshness — C2 | 9 stale rows → 0 (clause audit; the census gate cannot grade the Frontier region — named residual R1); PROVINCE 162 held | improved |
| operability — C3 | custody residuals closed; selftest 22→28; pair MATCH 5/5 | improved |
| depth | 10.0 → 10.0 | unchanged |
| calibration | 10 → 10 | unchanged |
| adjacency | no bleed (PROVINCE boundary untouched) | unchanged |

Learning trends: expansion improved; discernment improved (the wave caught and
corrected its own census three times by first-hand re-measurement — the exact
honesty discipline rule #14 exists for); quality improved (five independent
repair voices produced, the convergence verdict picked the complete composition
and named the malformed/defective candidates rather than averaging).
Carried debt (named): the census blind spot (Frontier region UNDECLARED — the
repairs are clause-audited, not instrument-graded); `ptr_check` unreachable on
pinned clauses (R2); the pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md`;
`/tmp` quota standing. Retired: none.

## arc3-loop1-round5 — calibration + coverage + freshness: the scheduled correctness sweep, 2026-10-19

Wave: 64 seats on `openai-codex/gpt-6-luna-max` — the scheduled R5 sweep, all
64 reports delivered (16 c1 + 16 c2 + 16 c3 + 12 verdicts + 4 unrostered TB
mapped to c1). Claims measured at work commit `58c3db7`. The sweep's job was
to re-derive arc3 rounds 1–4 and disposition the arc2 carried debt — it did
both, and it earned its keep by catching real defects the landings carried.

- C1 calibration (sweep) — every scoped number re-derived first-hand:
  command A reproduces at all seven revisions (82→84 mapped, missing/dangling
  []); census PASS; citation-drift 0/0 both modes; custody selftest 28/28;
  PROVINCE 162 held; Vyper 15/15 K/K + runtime sha `57d6fd0a…` + modulo
  table at `0x600` all reproduce. **Five discrepancies named and corrected** —
  a reporting overstatement ("all nine literals cleared" → 8/9 + adjudicated
  NO-CHANGE), an invocation syntax (`--selftest` flag → positional
  `selftest`), a revision-grouping mislabel (`5be4a26` is r3-hygiene, not r2;
  `520341d` is r4-C3 work, parent of `40de383`), a Vyper CODECOPY wording
  (2-byte entry copied, not the 26-byte table), and a roster-table gap
  (TB-1..4 omitted from the printed table, mapped to c1 in the text).
- C2 coverage (corpus audit) — the three dated arc3 entries audited per
  claim: selector sets, byte identities, dispatch shapes all VERIFIED; two
  real defects + two domain/wording corrections landed append-only — the
  r4 initcode-absence sentence (runtime IS byte-embedded in initcode at +20 —
  parsed-and-empty is the probe result, not byte absence), the r4 "no Core
  promotion" sentence (superseded by the same commit `40de383`'s PROVINCE
  `Core, arc3-r4` wording), the r4 CODECOPY wording, and the r1 Smoke
  digest domain (685 B decoded ↔ `08299f31…`; `530efc7b…` is the 1,370 B
  hex file). The r3 initcode line corrected the same way; the r3
  matrix-only rows recorded UNVERIFIABLE (evidence not retained).
- C3 freshness (debt disposition) — three rulings, none dropped: mid-leg
  retest **STOPPED-with-reason** (MemAvailable ~20.5 GiB passes the RAM
  reading but the operator host-cost gate is not evidenced — honest stop);
  r10 5-seat deficit **DISCHARGED-BY-PRECEDENT** (corrected missing set
  E1,E17,E28,R7,CR1 — the older receipt wrongly named P1; caveat recorded
  that the counting lesson carries no interruption exception — the basis is
  the frozen R5 option); the full hyper-vs-devin census **CARRIED-forward**
  (report files r1:64/r2:60/r3:60/r4:60/r10:59 measured, but dispatch
  denominators aren't reconstructible in-repo).

Instruments at `58c3db7`: command A 84/84, 14/14, 10.0/10.0; census PASS;
probe findings=0 both modes; custody 28/28; PROVINCE 162 held.

| axis | evidence | verdict |
|---|---|---|
| calibration — C1 | every scoped number re-derived; 5 discrepancies caught + corrected | improved |
| coverage — C2 | corpus audited per-claim; 2 real defects + 2 domain fixes landed | improved |
| freshness — C3 | 3 debt rulings recorded, none dropped | improved |
| depth | 10.0 → 10.0 | unchanged |
| operability | custody 28/28, probe 0/0 | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Learning trends: the sweep is the arc's strongest evidence for the fleet's
honesty discipline — a 64-seat wave dispatched specifically to *find* errors
found five, including two the landings genuinely carried (the initcode and
Core-promotion defects). Recorded as discernment + calibration improved; no
sweep defect was smoothed into an unverifiable. Carried debt: the mid-leg
retest stays open as operator-gated (the one substantive debt); the census
Frontier blind spot (R1) and ptr_check blind spot (R2) stand; the r3
matrix-only rows and r3-07 Carrier-3 offsets remain UNVERIFIABLE (evidence
not retained); `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp`
quota standing.

## arc3-loop1-round6 — operability + coverage + depth: three claims admitted, 2026-10-19

Wave: 48 seats, delivered as 3 zai + 45 opencode-go-7 after two provider
substitutions and two interruptions — the scheduled `xai-oauth/grok-4.7-fast`
returned 403 on all 48 seats (~30s), the zai `glm-5.3-flash-low` wave was
interrupted after 3 seats delivered verified artifacts (kept), then
`antigravity/gemini-3.8-flash` and `cursor/grok-4.7-xhigh-fast` were each
interrupted at dispatch (0 delivered); the 45 remaining seats completed on
`opencode-go-7/deepseek-v4.1-flash`. Claims measured at work commit `2fba56f`.

- C1 operability (fleet) — the census Frontier blind spot (R1 residual carried
  since r4) **closed**: PL-4's G21 frontier-register patch applied to
  `c1-census-v10.py` (sha `d0772ce8…` → `80027570…`, 713 lines). The register
  pins each Frontier bullet's span and asserts REQUIRED earning anchors +
  FORBIDDEN retracted literals — measured on a scratch tree: the reintroduced
  stale literal ("real solc/vyper-compiled bytecode untested" back in :91-93)
  now FAILs `FRONTIER-STALE` where v10 read PASS; clean tree still PASS,
  14 rows asserted, errors []. All 17 shared JSON counters unchanged.
- C2 coverage (owned) — the r3/r4 named `viaIR` Unknown **closed**:
  `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md` (EX-7's entry,
  VZ-3's three text corrections applied — CBOR `73`→`64` verified against the
  runtime bytes, the 15-functions census, the SUB-leg scoping). viaIR
  compiles a **fourth dispatcher class** (inverted calldatasize guard +
  linear ascending EQ chain + `SUB`-terminated final leg, distinct from the
  r1 linear, r3 binary-search, r4 modulo classes); probe K/K 15/15 at both
  pins; the `5f3560e01c` prologue does NOT identify the pipeline — the
  compare-tree class does. Map token landed; command A 84 → 85.
- C3 depth (owned) — **rule #15** landed (the corrected `a1bceb40…` text,
  not the verbatim `763c44b5…` draft — the `:34`→`:29` citation fix and the
  `r1:24`→`:31` containment fix both applied): "a parsed-and-empty result is
  a statement about the parser's scope, never proof of byte absence — settle
  byte questions with a census, not with the probe's function count." Eight
  citations, all in-bounds. `rule_blocks` 14 → 15, all 15 resolved.

Instruments at `2fba56f`: command A 84→**85/85** mapped, 14→**15/15** rules,
10.0/10.0; census PASS with G21 register (14 rows asserted, errors []);
probe findings=0 both modes; custody 28/28; PROVINCE 162 held.

| axis | evidence | verdict |
|---|---|---|
| operability — C1 | census Frontier blind spot closed; seeded stale literal caught (FRONTIER-STALE); clean PASS held | improved |
| coverage — C2 | corpus 84→85; viaIR Unknown closed with a fourth dispatcher class measured | improved |
| depth — C3 | rule_blocks 14→15; the arc's biggest recurring lesson codified | improved |
| freshness | corpus errata from r5 still hold; no staleness reintroduced | unchanged |
| calibration | 10 → 10 | unchanged |
| adjacency | PROVINCE boundary untouched; gate edit in-lane | unchanged |

Learning trends: the round's real yield is the instrument fix — the blind
spot that made r4's PROVINCE repairs clause-audited-by-hand is now graded by
the instrument itself (G21 register). Discernment improved (the convergence
seats caught that only PL-4's design, of five candidates, closes the whole
fault set; the verbatim rule draft had two citation defects the corrected
text fixes). Provider resilience recorded honestly: the round survived two
full provider outages (xai 403, two dispatch interruptions) and landed on
its third effective lane — substitution with cause recorded each time.
Carried debt: the append-past-:162 register residual (named in PL-4's patch
text — a new bullet beyond the last declared line sits outside the register
until re-keyed); the census's `ptr_check` blind spot (R2) stands; the mid-leg
retest stays operator-gated; `.ufo/waves/arc2-loop1-round10/C3.md` still
dirty; `/tmp` quota standing.

## arc3-loop1-round7 — coverage + calibration + operability: two claims verified, one adjudicated-partial, 2026-10-19

Wave: 24 seats on `openai-codex/gpt-6-luna-max` (the scheduled zai slot — the
lane is usage-exhausted, operator directive substitutes luna-max for all
remaining zai slots). All 24 reports delivered. Claims measured at work
commit `7deeb36`.

- C1 operability (fleet) — the `ptr_check` blind spot (R2 residual): the wave
  confirmed the mechanism is buildable (candidate patches catch seeded dead
  pointers on scratch, G21 + the 19-key JSON contract intact) **but the
  landing is genuinely blocked** — the frozen claim named `config.toml:3298`
  while the live `PROVINCE.md:18` pointer is `:3546` (the 2026-10-19 re-read),
  and `ptr_check` on the live target reads `stale`. No patch satisfies
  "clean PASS" without either a fake receipt anchor or failing the live tree.
  Adjudicated **partial**: mechanism proven, landing withheld; the pointer
  itself needs a re-anchored receipt before the instrument can grade it.
  Recorded in `claims/c1/C1-ADJUDICATION.md`.
- C2 coverage (owned) — the `ev_` Evidence-ID formula Unknown **closed**:
  `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md` (EX-3's
  entry — the verdicts converged it directly derives the named formula:
  `ev_` + lowercase sha256 of UTF-8 canonical JSON over the semantic
  projection, per `rea-agents@6.4.0`/`6.7.0` package source; path-bearing
  fields affect the id, display-only `subject.name`/`local_path` do not;
  8/8 envelopes recomputed to their claimed ids). Map token landed; command
  A 85 → 86.
- C3 calibration (owned) — pacman archive inventory re-derived: **1350** live
  `.pkg.tar.zst` (delta −206 from the dated 1556 receipt — cache eviction,
  retention-varying inventory, not a capability change). Adjudicated no-edit
  on the dated corpus value; append-only erratum landed on the pacman entry
  recording the delta + the `PROVINCE.md:50` unqualified-count residual.

Instruments at `7deeb36`: command A 85→**86/86** mapped, 15/15 rules,
10.0/10.0; census PASS + G21 register; probe findings=0 both modes; custody
28/28; PROVINCE 162 held.

| axis | evidence | verdict |
|---|---|---|
| coverage — C2 | corpus 85→86; the `ev_` formula Unknown closed | improved |
| calibration — C3 | live delta measured first-hand; dated receipt preserved by adjudication | improved |
| operability — C1 | mechanism proven; landing withheld on a measured discrepancy (honest, not forced) | unchanged |
| depth | 15 → 15 | unchanged |
| freshness | r5/r6 errata hold; the pacman drift recorded | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Learning trends: the round's most instructive outcome is the honest partial —
the instrument extension is provably buildable but the acceptance criterion
was written against a receipt that had already drifted, so the correct move
was to withhold the patch and name the blocker rather than land a fake anchor
or a failing gate. That is the honesty discipline the arc trains. Discernment
improved (the verdicts caught that the frozen claim's own pointer was stale —
the claim was written before the pointer's own drift). Carried debt: the
C1 `ptr_check` extension (mechanism proven; needs a re-anchored receipt
first); `PROVINCE.md:50`'s unqualified count; the mid-leg retest
(operator-gated); the register append-past-:162 residual;
`.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## arc3-loop1-round8 — operability + freshness + coverage: three claims admitted, 2026-10-19

Wave: 24 seats on `openai-codex/gpt-6-luna-max` (the second zai slot — lane
usage-exhausted, operator substitution). All 24 reports delivered; the wave
caught a pre-existing gate FAIL (the r7 SCORECARD section at :1776-1783 sat
outside declared scope) and folded its fix into the coupled landing. Claims
measured at work commit `53fcf0c` + probe fix `227443e`.

- C1 operability (fleet) — the `ptr_check` blind spot (R2 residual, the r7
  adjudicated-partial) **closed, done right**: EX-1's candidate applied to
  `c1-census-v10.py` (sha `80027570…` → `e4fb740c…`). The `if not occ`
  suppression removed so `path:line` pointers are collected even in
  pin-carrying clauses; a new DATED-scope SCORECARD row (1759-1813) fixes the
  undeclared FAIL the wave caught; DATED-scope stale pointers class
  `historical` (preserving the receipt-stamped adjudication). Measured: the
  live `:4126` pointer evaluates `current-ok` on the clean tree; a re-keyed
  dead pointer (`:3546`) FAILs `stale=1` on a scratch tree; G21 + the 19-key
  JSON contract + all prior counters intact.
- C2 freshness (fleet) — PROVINCE pin pointer re-anchored **in the same
  commit**: `:3546` → `:4126` (the live `rea-agents@6.7.0` line — re-derived;
  `:3546` had already drifted to a Copilot block). Receipt landed at
  `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt` carrying the live
  line's content sha (`eb237377…` ex-LF / `eb1c7da7…` incl-LF). The probe's
  `prov18-stamp-named` needle (`17:55:49Z receipt`) restored contiguous in
  `227443e` after the first rewrite dropped it.
- C3 coverage (owned) — the Vyper non-default-optimizer Unknown **closed**:
  `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md`
  (EX-8's entry — the most complete re-derived evidence): `--no-optimize`
  compiles an EQ/ISZERO chain (8 PUSH4 legs, offsets `PUSH4 pc + 12` →
  CALLVALUE); `-O codesize` compiles a packed selector/target table (no
  opcode-boundary PUSH4, 61-byte tail, all offsets shared `DUP1`); explicit
  `-O none` ≡ `--no-optimize` resolved (the r7 discrepancy). Map token
  landed; command A 86 → 87.

Instruments at `227443e`: command A 86→**87/87** mapped, 15/15 rules,
10.0/10.0; census PASS + G21 register + the live `:4126` pointer evaluated
`current-ok`; probe findings=0 both modes; custody 28/28; PROVINCE 162 held.

| axis | evidence | verdict |
|---|---|---|
| operability — C1 | `ptr_check` blind spot closed on a real anchor; seeded dead-pointer caught; undeclared FAIL fixed | improved |
| freshness — C2 | PROVINCE pointer re-anchored to live line; receipt landed; probe needle restored | improved |
| coverage — C3 | corpus 86→87; Vyper optimizer-forms Unknown closed | improved |
| depth | 15 → 15 | unchanged |
| calibration | 10 → 10 | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Learning trends: the arc's first adjudicated-partial resolved correctly —
the r7 claim's mechanism was buildable but its anchor was stale, and r8's
coupled landing (re-receipt + extension + re-anchor in one commit) is exactly
the fix the adjudication named. Discernment improved (the wave caught the
pre-existing undeclared FAIL before it could ship as a "clean PASS").
Carried debt: the register append-past-:162 residual; the mid-leg retest
(operator-gated); the perishable pin-line class will drift again (the receipt
now carries the live line's content hash so the next drift is detectable);
`.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## arc3-loop1-round9 — freshness + coverage + calibration: three claims admitted, 2026-10-19

Wave: 48 seats on `openai-codex/gpt-6-luna-max` — the scheduled R9 provider,
no substitution. All 48 reports delivered; the wave caught a second
pre-existing gate FAIL (`SCORECARD.md:1834`, the r8 section's `6.7.0` pin
outside the 1759-1813 scope row) and its fix folded into the landing. Claims
measured at work commit `eb5a2c4`.

- C1 freshness (fleet) — the `PROVINCE.md:50` perishable-value residual
  repaired same-line: "pacman `.pkg.tar.zst` corpus 1556 signed archives"
  now carries the dated qualifier + the live delta ("cache: 1,556 signed
  archives (2026-10-13 snapshot); current cache: 1,350 archive files, each
  with a matching `.sig` sidecar (arc3-loop1-round9 recount; −206 vs
  snapshot)") + the `available:true` clause dated to the survey, not read as
  a fresh check. The SCORECARD scope re-key (1759-1813 → 1759-1870) fixes
  the r8-section undeclared FAIL the wave caught; the instrument now reads
  PASS with the row's loci evaluated.
- C2 coverage (owned) — the viaIR final-selector-miss residual **closed**:
  `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md` (EX-8's entry
  — byte-level evidence): the `SUB`-leg mismatch branch at PC `0xc2`/`0xcf`
  distinguishes the no-fallback revert path (`PUSH0; DUP1; REVERT`) from the
  payable-fallback storage-write path (`CALLVALUE` → `SSTORE` slot 2 →
  `STOP`); 15/15 selectors at both variants, both pins. Map token landed;
  command A 87 → 88.
- C3 calibration (owned) — the pin-line drift class characterized
  end-to-end: the pin is the **sole** `rea-agents@` match at `:4126` (the
  ptr extension evaluates it `current-ok`); the class is **position-
  sensitive, not content-sensitive** (a one-line insertion above the pin
  reads `stale`; a duplicate pin line stays `current-ok`). Recorded
  append-only on the r8 receipt — the next drift is now not just detected
  but understood.

Instruments at `eb5a2c4`: command A 87→**88/88** mapped, 15/15 rules,
10.0/10.0; census PASS + G21 + live `:4126` `current-ok`; probe findings=0
both modes; custody 28/28; PROVINCE 162 held.

| axis | evidence | verdict |
|---|---|---|
| freshness — C1 | `PROVINCE.md:50` dated + live-delta repaired; scope re-key fixes undeclared FAIL | improved |
| coverage — C2 | corpus 87→88; viaIR fallback-miss residual closed | improved |
| calibration — C3 | drift class measured end-to-end; position-sensitivity characterized | improved |
| depth | 15 → 15 | unchanged |
| operability | census PASS + G21 + ptr `current-ok`; probe 0/0 | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Learning trends: the arc's instrument-driven correction loop is now the
steady state — each round's wave catches the prior round's own scope drift
(the r7 and r8 SCORECARD sections each undeclared) and the fix folds into
the same commit that lands the claim. That is exactly the discipline the
gates exist to enforce. Carried debt: the register append-past-:162
residual; the mid-leg retest (operator-gated); the `available:true` class
stays dated, not re-probed (no live REA session this round);
`.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## arc3-loop1-round10 — coverage + depth + operability: three claims admitted, 2026-10-19

Wave: 48 seats on `openai-codex/gpt-6-luna-max` (the scheduled devin-deepseek
slot — the devin lane is exhausted, operator substitution). All 48 reports
delivered. Claims measured at work commit `9c1d1fe`.

- C1 coverage (owned) — a second verb family's `ev_` Evidence-ID formula
  **closed**: `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md`
  (EX-4's entry — the verdicts converged on it over the Vyper multi-target
  drafts): `inspect_rust_binary` is path-sensitive because its semantic
  projection carries `parameters.path`, `normalized_result.artifact.path`,
  and an `artifact-path` location (`dist/application/rust/
  RustBinaryService.js:55-80`); all four envelope IDs recomputed; display
  fields (`subject.name`/`local_path`) excluded. Map token landed on the
  Rust row; command A 88 → 89.
- C2 depth (owned) — **rule #16** landed (SC-2's "Co-land every truth
  dependency" — the verdicts' majority pick): before repairing a statement
  whose truth depends on another deliverable, name the dependency and land
  the complete set in one commit; a scratch projection is not a landed
  result. Cites the r4 Vyper-wording↔C1 and r8 receipt↔extension couplings.
  `rule_blocks` 15 → 16, all 16 resolved.
- C3 operability (fleet) — the G21 register's named residual **closed**:
  PL-3's unregistered-bullet guard applied to `c1-census-v10.py` (sha
  `e4fb740c…` → `d6b4deaa…`). `FRONTIER_SECTIONS` + a bullet-start check
  flags any `[-*+]` bullet inside a Frontier section that no G21 row keys —
  measured: a seeded bullet appended at :163 now FAILs
  `FRONTIER-UNEVALUABLE`; clean tree PASS, 14 rows asserted, errors [].

Instruments at `9c1d1fe`: command A 88→**89/89** mapped, 15→**16/16** rules,
10.0/10.0; census PASS + G21 register + unregistered-bullet guard + live
`:4126` `current-ok`; probe findings=0 both modes; custody 28/28; PROVINCE
162 held.

| axis | evidence | verdict |
|---|---|---|
| coverage — C1 | corpus 88→89; second verb family's ev_ formula closed | improved |
| depth — C2 | rule_blocks 15→16; the coupled-landing discipline codified | improved |
| operability — C3 | register append-past-:162 residual closed; seeded bullet caught | improved |
| freshness | corpus errata hold; no staleness reintroduced | unchanged |
| calibration | 10 → 10 | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Learning trends: the arc's three recurring disciplines are now codified —
coupled landing (rule #16, the lesson the r4 and r8 couplings earned),
parsed-and-empty ≠ byte-absence (rule #15), and instrument-graded vs
clause-audited (the G21 register + its new append guard). The wave kept the
honesty standard: every claim's before-state measured, every landing
re-derived at the commit. Carried debt: the mid-leg retest (operator-gated);
the `available:true` class stays dated; `.ufo/waves/arc2-loop1-round10/C3.md`
still dirty; `/tmp` quota standing.

## arc3-loop1-round11 — coverage + freshness + calibration: three claims admitted, 2026-10-19

Wave: 32 seats on `openai-codex/gpt-6-luna-max` (the scheduled zai-max slot —
lane usage-exhausted, operator substitution). All 32 reports delivered.
Claims measured at work commit `5ee13b3`.

- C1 coverage (owned) — a third verb family's `ev_` Evidence-ID formula
  **closed**: `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`
  (CR-2's entry — the verdicts' plurality + CN-1/VZ-2 corroboration):
  `inspect_artifact` is path-sensitive on the *outer* id because the
  semantic projection nests the inventory Evidence inside `normalized_result`
  (`dist/domain/artifactInspection.js:111-155`); the nested
  `inventory_artifact` id is path-stable while the outer id changes on a
  same-basename alternate path. All four envelope IDs recomputed. Map token
  landed on the Evidence-model row; command A 89 → 90.
- C2 freshness (fleet) — three receipts re-derived first-hand, all honest:
  Ghidra **34 features / 39 processors** (delta 0/0 — the r4 "35" miscount
  stays corrected); pacman **1,350 archives + 1,350 sig sidecars** (delta 0
  vs the r9 live count, −206 vs the dated 1556); ASAR **12** within the
  searched roots (host-wide completeness bounded by the unreadable
  `/opt/containerd` subtree). No errata needed — the dated values hold.
- C3 calibration (owned) — the `available:true` class re-derived: a fresh
  `binary_session {}` reports the provider group `rea-artifact-graph`
  `available:true` (covering `inspect_artifact`/`extract_artifact`), while
  the targetless per-tool entries read `available:false` /
  `reason:"target_required"` — the provider group is available, per-tool
  readiness needs a target. The attached Kimi session is
  `unknown`/`config_drift`. Recorded append-only on the pacman entry.

Instruments at `5ee13b3`: command A 89→**90/90** mapped, 16/16 rules,
10.0/10.0; census PASS + G21 + guard + live `:4126` `current-ok`; probe
findings=0 both modes; custody 28/28; PROVINCE 162 held.

| axis | evidence | verdict |
|---|---|---|
| coverage — C1 | corpus 89→90; third verb family's ev_ formula closed | improved |
| freshness — C2 | three receipts re-derived; dated values hold | improved |
| calibration — C3 | `available:true` scope re-derived; provider-vs-per-tool distinction measured | improved |
| depth | 16 → 16 | unchanged |
| operability | census PASS + G21 + guard + ptr `current-ok`; probe 0/0 | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Learning trends: the arc's evidence discipline is now deep enough that a
wave can derive a third Evidence-ID formula from package source + measured
envelopes — the `ev_` domain is now closed for three verb families
(inspect-evm-interface, inspect_rust_binary, inspect_artifact), each
path-sensitive by its own projection, not by a universal rule. Carried debt:
the mid-leg retest (operator-gated); the ASAR host-wide count stays bounded
by the unreadable `/opt/containerd` subtree; the Kimi-session availability
stays unverified (config_drift);
`.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## arc3-loop1-round12 — coverage + depth + operability: three claims land (pending non-author verification), 2026-10-19

Steered round 12 (kaika steer table: "finish exactly as frozen"). Wave: 48 seats
frozen pre-dispatch on `openai-codex/gpt-6-luna-max` (scheduled
`antigravity/gemini-3.8-flash` slot; antigravity lane down, operator
substitution — `.ufo/waves/arc3-loop1-round12/claims-frozen.md:3-9`); 47/48
reports delivered, `CN-1` the named non-completion. The wave halted at `de77d75`
with no integration; this session (kaika W2a) integrated it with a 10-member L2
swarm in one batched call (planner, connector, 3 executors, scribe, scout,
reviewer, critic, mutation-tester). Work commit `4072ebb`; fix commit `6a35398`
(see C3 harm check); all after-numbers measured at `6a35398`
(`.ufo/waves/arc3-loop1-round12/integration/measurements-6a35398.txt`).

- C1 coverage (owned) — fourth verb family's `ev_` formula **closed**:
  `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` —
  `inspect_go_binary` (REA 6.7.0 pinned cache, package-source SHA-256 receipt
  `CR-4/evidence/package-source-hashes.txt`) is path-sensitive through `parameters.path`,
  `normalized_result.artifact.path`, `locations[0].path`; display subject
  fields excluded. Fresh live rerun reproduced the stored same-path id
  `ev_87621921…055dcd`; retained reconciliation `records=27 matched=27`
  across seven seat bundles (`integration/c1/reconcile-all-go-ids.txt`).
  Token on the Evidence-model row. Command A knowledge_files/mapped 90 → 91,
  missing [], dangling [].
- C2 depth (owned) — queue-drain rule #17 (`SKILL.md:293-314`): evidence-id
  field sensitivity is projection-local; isolate the field set and diff the
  residual projection when a mutation does not reproduce the alternate id
  (r11's nested `local_path` + `inspection_id` confounder). Cites r7/r10/r11
  corpus ranges only (not the r12 entry). Command A rule_blocks /
  citation_resolved_rules 16 → 17. SHONEN box-1 count co-landed at EOF.
- C3 operability (fleet) — citation-drift pointer table grades the r7/r10/r11
  `recheck:` lines: rows grading a recheck line 0 → 3, entries 57 → 60, sha256
  `1b3ab955…` → `7994eec7…` (re-pinned in `expected.json`). Deviation from the
  verdict seat's pick (PL-4's exact rows, `7470c3f6…`), on measurement: PL-4's
  substring needles killed 17/24 breaking mutants; full-line pins killed 24/24
  but false-alarmed on harmless rewording; the landed order-free
  delimited-token lookaheads keep the three seeds caught (control exit 0, each
  seed one `citation_dead`, strict exit 1 — `integration/c3/seeded-run-lookahead.txt`)
  and kill 20/20 breaking text mutants (+6 positional) with 0/12 harmless false
  alarms (`integration/mutation/lookahead-regex-check.{py,txt}`; per-version
  history in `integration/mutation/table1-rerun.md`). Scope: fixed-line
  text-token drift only; the rows never execute a recipe.

Harm check (caught before records): the work commit `4072ebb` inserted a
lessons-index row into `corpus/README.md` and an inline line into `SHONEN.md`;
the strict probe at `4072ebb` read `failed findings=5`
(`integration/probe-at-4072ebb.txt`). Fix `6a35398` removed the README row and
moved the SHONEN correction to EOF → strict probe `clean findings=0`. The
round-12 lesson stays unindexed in `corpus/README.md` (the index cannot grow
above `## Frontier` while `SCORECARD.md:69` pins `corpus/README.md:180`).

Instruments at `6a35398`: command A 91/91 + 17/17, 10.0/10.0; census PASS
(stale/ambiguous/undeclared/unresolved 0/0/0/0) run as
`python3 <tree>/.ufo/gates/c1-census-v10.py --root <tree>` on a `git archive
6a35398` tree — the census's default `--root` is the lane main checkout, so a
bare run from a worktree measures the wrong tree (lesson round-12 #10);
citation-drift strict clean findings=0, selftest 13/13; custody selftest 28/28;
PROVINCE 162 held.
Custody: no pre-pair (live CLI legs in r11 and r12 ran unpaired — lesson
`corpus/lessons/round-12.md` #3); two post-only receipts bracket a `~/.bashrc`
content change at 21:46:35Z, after the last live leg (operator-owned; no
zero-drift claim made).

| axis | evidence | verdict |
|---|---|---|
| coverage — C1 | corpus 90 → 91, mapped 91/91; fourth `ev_` family | improved (pending non-author verification) |
| depth — C2 | rule blocks 16 → 17, citations 17/17 | improved (pending non-author verification) |
| operability — C3 | recheck-grading rows 0 → 3; probe clean at `6a35398` | improved (pending non-author verification) |
| calibration | no claim; 10.0 | unchanged |
| freshness | live recheck re-derived the stored Go id; no claim | unchanged |
| adjacency | PROVINCE boundary untouched | unchanged |

Saturation note (appended; `## Saturation` above is not rewritten): the arc3
window opened at r1 (1/10, `:1340`); sections r4–r11 stopped stating the count;
r12 is 12/10. All owned proxies sit at 10.0 and no capability row has entered
since arc2-r8, so the `AXES.md` §stagnation nudge applies (a "should": the round
should be a frontier/capability move). The frozen r12 claim set predates this
record and was finished as frozen; the next round honours the nudge.

Planned: arc3-loop1-round13 — capability/frontier move. Primary: ARM64X hybrid
PE analysis via Ghidra on one real host carrier (`PROVINCE.md` PE reserve;
capability rows 4 → 5 only if it runs and its output verifies). Also: create
`corpus/SOURCES.md` per sources contract v1 (opened rows only; first leads:
Ghidra GP-6528 / `GoRttiMapper.java`, RARE, Decompile-Diverge, V8-snapshot
surface — connector scan, kaika W1 ART dossier); QUALITY rows for lesson
round-12 #3 (custody pre-pair before any probing L2) and #5 (stale status in
cited ranges). Freeze the custody pre-pair before the first probe.

Carried debt: `CN-1` non-completion; D7 draft headers on three landed entries
plus the r11 entry's stale "remains pending" clause (`:23`); the path-free
`search_bytes` candidate stays an open Unknown (VZ-1:32-34); the r12 entry's
own `recheck:` line is not yet graded by a pointer row (kept out of C3 for
separability); QUALITY #15's recorded-family list predates r7/r10/r11/r12;
mid-leg retest (operator-gated); Kimi session `config_drift`;
`.ufo/waves/arc2-loop1-round10/C3.md` dirty; `/tmp` quota standing.

## arc3-loop1-round13 — source-curation capability only, 2026-10-19

The r12 claims stay frozen. This round follows the stagnation nudge with one
capability claim: keep where-to-learn evidence for the existing REA frontier.
It does not add a domain-analysis result, a knowledge entry, or an ARM64X
capability. The prior planned ARM64X run is not pursued under this steer.

### Capability addition (append-only)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| curated source registry for existing REA frontier | Keeps opened, scoped study sources, ordered paths, recheck cadences, an auditable bounded search, and a source rejection with evidence and flip; source text is not held-capability evidence | `corpus/SOURCES.md`; `corpus/lessons/round-13.md`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-19 --root /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin` | arc3-loop1-round13 |

This is an append-only capability record; the earlier line-addressed summary
table is unchanged.

### Per-axis and learning-trend verdicts

| axis | evidence | verdict |
|---|---|---|
| coverage (owned) | No knowledge-map or province-frontier change; no owned score was changed | unchanged |
| depth (owned) | No domain finding or durable analysis rule was admitted; no owned score was changed | unchanged |
| calibration (owned) | No outside admit/reject spot-check yet; no owned score was changed | unchanged |
| operability (not owned) | No REA operation or target route added | unchanged |
| freshness (not owned) | Source revision and access anchors are recorded; no live provider drift probe | unchanged |
| adjacency (not owned) | All new paths stay within the shipped-artifact RE boundary | unchanged |

Learning trends: expansion **improved** by entry of the separately recorded
capability, not by source-row count; the uncovered-ground knowledge-entry
submeasure is unchanged. Quality **unchanged** (no knowledge entry was
re-verified or superseded). Discernment **unchanged** pending the
orchestrator-owned fresh non-author re-open of an admit and the rejection.

Planned: arc3-loop1-round14 — after the orchestrator's fresh non-author source
sample, admit one source-backed knowledge entry only if a matching uncovered
coverage-map question remains. ARM64X stays a frontier candidate requiring a
real carrier and explicit steer; no unavailable sample is assumed.

## Post-review correction — arc3-loop1-round13 (append-only, 2026-10-19)

The pre-review trend line above is superseded: **expansion is unchanged** for
r13. No uncovered-ground knowledge entry was admitted; source rows and the
separately recorded curation capability are not knowledge expansion. Quality
remains unchanged. **Discernment is improved**: the non-author
`KaidokuR13Review` re-opened representative admits S003/S008 and rejection
S022, and agreed with those source dispositions. The two quote-fidelity
defects found in that review are corrected by the round-13 lesson addendum.

The earlier calibration axis note and round-14 plan described the pre-review
state. The outside sample is now complete; calibration's numeric axis score
remains unchanged. Round 14 may mine one source-backed knowledge entry only
if the matching uncovered coverage-map question remains.

## Round 14 — source diagnosis and quote-regression capability, 2026-10-20

Measured source commit: `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`.
Baseline: `767adafb97e2eef6980e2ad873d357e16721c467`.
Motivation and landed work: LOG round-14; prior verifier spotcheck and
`corpus/lessons/round-14.md`. `claims-review.json` (under this round's wave
directory) records the pre-integration coverage→depth reclassification.
The same Go symptom was already held; its missing source-backed bootstrap
diagnosis is a deepening, not an earned broad-coverage increase.

| Claim / axis | Numeric proxy delta | Supplemental before→after / counting command | Evidence and author-side verdict |
|---|---|---|---|
| C1 depth | 10.0→10.0, delta 0; existing finite citation proxy stays saturated | source-diagnostic entries 0→1; `python3 .ufo/waves/round-14/measure.py <revision>` against the two hashes above | new Go diagnosis plus append-only causal correction; **improved** technical depth, no historical-cause proof or provider execution |
| C2 calibration / capability | 10.0→10.0, delta 0; the old failure-selected proxy is not relabeled | quote instrument 0→1 and grounded criterion 0→1, same measurement command; defect controls exit 1→0 with only quote/section changed | quote CLI selftest and frozen run in `.ufo/waves/round-14/verification.json`; **improved**, bounded regression capability, not a population accuracy estimate |
| coverage | 10.0→10.0 | map integrity 91/91→92/92, missing/dangling remain empty, same command | unchanged domain coverage; token added on the existing Go row without moving pinned lines |
| operability | no owned numeric proxy | new instrument runs; no independent claim | no harm; no new held REA operation |
| freshness | no owned numeric proxy | named sources reopened; no provider replay | unchanged, no stale live-capability assertion introduced |
| adjacency | no owned numeric proxy | local source/evidence checks only | unchanged; no sibling gate, config, or domain source-tree ownership taken |

The table's boolean counts are not axis scores. Existing command A, with REV
set to the measured source commit, still resolves 17/17 craft rule blocks.
The craft section's bytes are identical to baseline; proof in
`.ufo/waves/round-14/command-a-control.json`. Strict citation drift is clean
with zero findings, and the scoped census is PASS with zero stale,
ambiguous, undeclared and unresolved loci (`verification.json`).

### Capability addition (demonstrated before this row)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| local raw-quote/heading regression audit | Rejects the retained S017 splice and S018 wrong section, accepts corrected controls, and refuses malformed/tampered inputs; frozen runs pin every manifest/source input | `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` → 28/28; same script `--frozen .ufo/waves/round-14/fixtures/expected.json` → seven expected verdicts matched; source commit above, `.ufo/waves/round-14/verification.json` | round-14 |

Limits: captured raw UTF-8 substrings and Markdown/single-line HTML headings,
not source authenticity, full-document completeness, semantic support,
whole-registry validation, outside admission, or target execution.
The source-diagnosis entry does not depend on this local parser.

Sources remain 22 rows (A20/B1/C1, mined21/rejected1); no row quota.
Required validation before and after exits 0. Six permitted used-by cell
changes and their exact old→new values are in the lesson.

Learning trends: expansion **unchanged** (deepening held Go ground, not a
new broad surface); quality **improved** (unsupported causal inference
superseded by source-conditional diagnosis); discernment **improved** only
because the prior genuine outside quote findings became grounded QUALITY
criterion 16 and exercised regressions. No author-side seat counts as the
current round's independent reviewer; closure sampling remains pending.

Saturation: the three owned finite proxies remain at their line; this
demonstrated capability resets the capability stagnation interval. No axis
is retired or declared mastered. The tied-lowest calibration obligation is
worked by C2, and the capability move honors the stagnation nudge.

Planned: after the fresh non-author sample, one depth/capability claim to
discriminate bootstrap failure on a caller-selected real Go carrier with
retained analyzer diagnostics; no implicit upgrade, recovery promise, or
next-round execution is made here.

## Round 15 — installed snapshot evidence and review-duty calibration, 2026-10-20

Baseline: `9719dd232687f5ee78a4ed323b37f8810e833d10`.
Final measured source/evidence revision:
`ba3b2195d080d3083d339a67c35359855ad164a5`.
Probe repair source: `7ad23fe1735cd868ec203d93deb13bb2c42889ad`.
Motivation and accepted/rejected candidates: LOG round-15 and
`corpus/lessons/round-15.md`; refinements in
`.ufo/waves/round-15/claims-review.json`.

| Claim / axis | Existing proxy delta | Supplemental before→after, command and revision | Author-side verdict and limits |
|---|---|---|---|
| C1 depth | 10.0→10.0, delta 0 | Entry/tool presence 0/0→1/1; `python3 .ufo/waves/round-15/measure.py <revision>` on baseline and final measured hash above. Actual inventory command is the new entry's `recheck:`; retained output and exits in `verification.json`, measured probe source above | **improved** by persisted per-file installed-data pins, patch histogram, generic bootstrap definitions and requested-version/fallback-byte distinction; not by repeated filenames or mere file presence. Two repaired-probe runs exit 0, byte-identical. No target recovery or historical causality claim |
| C2 calibration | 10.0→10.0, delta 0 | Explicit manual-only criterion and named advisory correction 0/0→1/1; same immutable measurement command/revisions. Boundary red/raw-fixed commands in `verification.json` exit 1→0; only quote text differs, same source and ID | **improved**, two outside duties discharged through corrected active wording and source trace. Existing raw gate unchanged; no classifier, new capability, independent review or stagnation reset |
| coverage | 10.0→10.0 | Map 92/92→93/93, missing/dangling empty; same measure command | unchanged domain ground; Go was already held |
| operability | no owned numeric proxy | Actual first inventory run failed exit 1 at `856d193`; numeric/dict patch-key collision repaired; final script runs clean | no residual harm; initial red and repair retained, not silently treated as first-run success |
| freshness | no owned numeric proxy | Installed resources reopened and byte-pinned; no provider replay | unchanged; no live runtime freshness claim |
| adjacency | no owned numeric proxy | Local source/data and evidence wording only | unchanged; no sibling research method, configuration, engine or domain-target ownership taken |

The before/after booleans are presence controls, not expertise scores or
semantic proof. Source anchors and actual installed-data output supply C1's
substance; the prior genuine outside lesson and explicit criterion supply C2's.
No capability table row is added; no proxy is relabeled or retired.
The three-way lowest-axis tie is worked through calibration.

### Executed checks and honest repairs

- Inventory: 11 base JSONs, 123 patch diffs; every base has generic `all`,
  errors/skipped empty. Requested 1.25.7 has base 1.25.0 and no diff;
  requested 1.26.8 has no base. These are selected source/data inputs,
  not current-target observations. Full output SHA-256
  `ad06fadc0166e172d65325e3366375e2d4a9730d714d154bbcd98137539bb2fe`.
- Quote selftest 28/28, original frozen expectations seven matched, new
  boundary frozen expectations two matched; all clean exit 0. The direct
  rendered fixture produces exit 1 `quote_not_contiguous@raw-literal`;
  the quote-only raw form is clean. This exposes the representation limit.
- Craft bytes unchanged, command-A control 17/17 on both source revisions;
  `no-harm-controls.json`. Append-only logs/old lesson/old knowledge retained;
  outside verifier/advisory and existing raw-gate inputs unchanged.
- Strict citation check first detected the SHONEN evidence-line wording
  regression, exit 1. A wording-only correction preserved the truthful
  pinned craft phrase; final revision check clean findings 0, exit 0,
  `final-recheck.json`. Pointer baseline unchanged.
- Required source census start/end exit 0; rows 22→23,
  A20/B1/C1→A21/B1/C1, mined21/rejected1→mined22/rejected1.
  S023 adds one opened code source; S003/S007 only permitted used-by appends.

Learning trends: **expansion unchanged** (same Go ground), **quality improved**
(stronger pinned data/selection diagnosis and corrected active source wording),
**discernment improved** by learning both prior outside-routed defects into
grounded criterion/lessons. This is not a new outside spotcheck: all 32 seats
are author-side and current-round independent admit/reject sampling remains
the closure duty. All four SHONEN marks remain `[~]`.

Planned: only with an explicitly selected real Go carrier, retain new analyzer
diagnostics and distinguish requested-version labels from fallback data in
that run. No next-round execution, target choice, recovery success, or
operator-authorization blocker is inferred from this source-only round.

## Round 16 — computable Go selection and outside-route provenance, 2026-10-20

Baseline: `6235498b4112350eebce0812a74af1781fc0ee88`.
Measured source revision, committed and pushed before checks:
`27b8fc13156230981312c44380cddab1f2bd318d`.
Full producer argv/cwd/stdout/stderr/exits/input hashes:
`.ufo/waves/round-16/verification.json`; motivating evidence and
admit/reject decisions: LOG round-16 and `corpus/lessons/round-16.md`.

| Claim / axis | Existing numeric proxy | Falsifiable supplemental before→after, command and measured revision | Author-side verdict / limits |
|---|---|---|---|
| C1 depth | 10.0→10.0, delta 0; craft range proxy still 17/17 | Entry/probe/fixtures/runner presence 0→1 each; `python3 -I .ufo/waves/round-16/measure.py <REV>` on baseline and measured source above; actual source-model commands in `verification.json`, labels `selection-*`; developer runner `all-developer-fixtures` 154/154 exit0 | **improved** by materializing the already-held source law into request-bounded selected-file identities and ordered unpatched-base projection: 1.24.5 selects5 despite installed6; 1.24.7 selects6, numeric multi-digit and platform contrasts run. No new selector law, patch application, compiled-provider parity, target recovery or historical-cause proof |
| C2 calibration | 10.0→10.0, delta 0; legacy selected rubric not relabeled | Four route markers 0/4→4/4; identical `python3 -I -c <snippet> <lane> <REV>` exits1→0, complete snippet in `documentation-red.json` and after argv in `verification.json`; row18/supplement/named correction/historical line/producer 0→1 each via same immutable measure command | **improved** by learning all four prior genuine outside routes into actual corrections, grounded #18 and an executed structural producer. Marker green alone is explicitly insufficient; content review and retained `controls.py` invocation provide the provenance. No new outside review or promotion |
| coverage | 10.0→10.0 | 93/93→94/94 mapped, missing/dangling empty; immutable measure command above | unchanged domain ground; the new entry deepens held Go, not expansion |
| operability | no owned numeric proxy | one fixture invocation154/154; quote selftest28/28, frozen7+2; strict citation clean0; full exits/output retained | unchanged domain capability; no residual harm in these controls, no held REA operation added |
| freshness | no owned numeric proxy | installed source/data reopened and per-file identities emitted; no provider replay | unchanged; no broad current runtime-freshness claim |
| adjacency | no owned numeric proxy | local source-model/data and documentation evidence only | unchanged; no sibling research method, domain target, upstream/provider configuration or engine ownership absorbed |

The supplemental booleans and developer-case count are **not** expertise
scores or unbiased calibration measures. The three-way lowest-axis tie is
worked through calibration; no proxy is retired or relabeled.
Saturation line remains 10.0 and stagnation window remains 10; round 14's
demonstrated local quote instrument remains the last capability entry.
This round adds **no capability-table row or stagnation reset**.

### Executed controls and frontier

- `controls.py BASELINE SOURCE`: all18 prior lesson prefixes and all93 prior
  knowledge prefixes retained, LOG old prefix retained, four outside verifier
  files unchanged, 126/126 pre-existing frozen/evidence blobs byte-identical.
  Craft digest `e12b60ce0c71316e457680c65ae8273487deac9c68db3f80a084814a8ad765e6`
  and bounded 17/17 knowledge-file/range blocks unchanged. These controls do
  not inspect new frozen-root files/modes or establish semantic correctness.
- Metadata counting command retained as `source-contract-wave-counts`:
  QUALITY rows1–17 unchanged; canonical SHONEN seed with four `[~]` assertions;
  exact raw S003 quotes resolve; spec/dispatch/registered counts64+32=96.
- Sources23→23, tiersA21/B1/C1 unchanged, mined22/rejected1 unchanged.
  Required census starts/ends exit0. S003/S023 only permitted used-by
  extensions, exact old→new logged in lesson; zero new rows or frontier
  promotion. New entry explicitly cites reopened S003/S023.
- W1 64 seats, completed36/failed28; W2 32, completed32/failed0.
  Credit/capacity failures are retained, not replaced or called passes.
  L1 holds canonical planner seat; author seats do not become outside
  reviewers. Complete role mix and receipts under `.ufo/waves/round-16/`.

Learning trends: **expansion unchanged**, **quality improved** through the
new computable source-model detail and qualified prior overclaims,
**discernment improved** by converting prior genuine outside routes into
lesson-backed criterion18 and fixes. Current-round independent admit/reject
sampling and admission remain non-author closure work. SHONEN stays `[~]`.

Planned: after the next non-author sample, depth/capability on a caller-selected
real Go carrier with retained analyzer diagnostics; calibration on any routed
source/evidence disagreement. No carrier is silently chosen, no recovery
success promised, and no following round is started here.

## Round 17 — retained Go carrier diagnostics and routed r16 defects, 2026-10-20

Baseline: `b563c799d97774aae4351276fe43cb897311e349`. Predictions frozen:
`271167473d87ef710f07ecdd98caf0ce12091686`. Measured source revision (committed
and pushed before the single verification pass):
`d0ab2992149a38794e5ef2474ba5d4ef5ee1e905`; verification evidence revision
`b31975de62de5413a6f2d244f2690eaeb3d18c25`. Producer argv/cwd/exit/stdout/stderr
and pre/post pins: `.ufo/waves/round-17/verification.json` (79 commands, all
expected exits) and `.ufo/waves/round-17/final-recheck/*.receipt.json`.
Motivation and decisions: LOG round-17 and `corpus/lessons/round-17.md`.

| Claim / axis | Existing numeric proxy | Falsifiable before→after, command and measured revision | Author-side verdict / limits |
|---|---|---|---|
| C1 calibration | 10.0→10.0, delta 0 | R16-PROVENANCE: unqualified in-lane temporal sites 4→0, `temporal-sweep.py --root <LANE> --rev <REV> --sites-rev b563c79` (baseline exit 0 at `b563c79`; 4/4 corrected at `d0ab299` and `b31975d`). R16-INVOCATION: registry rows `unlabelled_variant` 2/7→0/17, `invocation-audit.py --root <LANE> --rev <REV>` at `b563c79` and `b31975d` (17/17 `exercised_match`). QUALITY rows 18→20 (rows 1–18 byte-identical, `controls.py`). Red-before: `pins.py --selftest` mutated-file case exit 1; `receipt-validate.py --selftest` mid-run-drift case exit 1 | **improved**: both routed outside defects discharged in-lane, with tools shown able to fail; the fleet-report site is carried by the round-17 report. The round's own mid-run overclaim (caught by w2) was corrected before close. No outside review is implied |
| C2 depth + capability | 10.0→10.0, delta 0 | Retained run-bound carrier runs 0→16 (8 carriers × 2 passes), 8/8 compare exit 0 per pass against predictions frozen at `2711674`; all 16 receipts `receipt-validate.py` exit 0 (MD5-anchored binding); replicate run `calib-shfmt` exit 0 with the identical Evidence ID; capability rows 6→7 (`measure.py <REV>` `C2_scorecard_capability_row` 0→1) | **improved**: runtime-retained discrimination of the none/info/fallback/no-build-info routes, with three of six prospective carriers on routes unseen at freeze. Frozen replicate expectation falsified for aether's Evidence ID (string_count 29118→29117); aether's post-bootstrap EOF is a labelled INFERENCE, not replayed |
| coverage | 10.0→10.0 | map 94/94→95/95, missing/dangling empty (`measure.py`) | unchanged ground: Go is held; the entry deepens it |
| operability | no owned numeric proxy | 11 tool selftests clean; replicate carrier run exit 0; citation-drift strict clean 0; quote-fidelity frozen 7+2 matched; custody-pair capture exit 0 | improved through the capability below, otherwise no harm in these controls |
| freshness | no owned numeric proxy | installed Ghidra source/data reopened; current `op` 2.41.0-1 observed; upstream Ghidra/GoReSym release status re-read (S029/S030) | unchanged as an axis; no broad runtime-freshness claim |
| adjacency | no owned numeric proxy | sibling scan: no lane retains REA analyzer logs (w1 `ConnSiblingOverlap`, w2 `ConnSiblingRows`); revenger/kaidoku shipped-artifact contest unchanged | unchanged; nothing absorbed |

### Capability addition (demonstrated before this row)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| retained REA Ghidra-session log capture | Runs REA `analyze` on a pinned carrier in a private-TMPDIR, allowlisted-environment session and keeps that session's `ghidra.log`/`script.log`. The log is retained before REA's close deletes it, is bound to the run by its own records (log path, imported target, full MD5), and carries pre/mid/post pin maps with instants. The receipt validates offline | `bash .ufo/waves/round-17/run-carriers.sh <LABEL>`; receipts `.ufo/waves/round-17/runs/*/receipt.json` (16 across two passes, 8 retained at HEAD, 8 at `da64646`); `receipt-validate.py` exit 0 ×8 in `verification.json`; replicate `verify/replicate/calib-shfmt` | round-17 |

Limits:
- The capture is a polling prefix. REA kills the post-script analysis pass,
  so absence claims hold only up to the last retained line. All 16 logs reach
  `REPORT: Analysis succeeded`.
- The capture reads REA 6.5.0's private, undocumented session directory.
  REA 6.7.0 adds no keep-log knob (w2 `ScoutReaLogKnob`). Re-check on every
  REA/Ghidra release.
- The log is outside REA's Evidence model. The receipt asserts the Evidence-ID
  link.
- `receipt-validate` proves consistency now, not authenticity against a
  forger who rewrites and rehashes.
- Process-group stop does not reach a grandchild in its own session (w2
  `StopGroupTest`); no run timed out.
- Only `ghidra.log`/`script.log` are copied, never `session.json`.

Saturation line remains 10.0 and the stagnation window remains 10. This
capability resets the capability stagnation interval (last entry round 14).
The three owned proxies tie at 10.0, and calibration (C1) works that
tied-lowest axis.

### Waves

W1 had 78 seats (executor14/scout20/reviewer12/scribe10/connector8/critic6/
revenger4/sentinel2/simplifier2), all completed. Dispatch was refused twice at
the host job cap and spawned on the third identical payload. W2 had 69 seats
(reviewer18/executor16/scout9/critic8/scribe5/mutation-tester4/connector3/
revenger3/sentinel2/simplifier1): 67 completed and 2 died on an m_swe rate
limit (`PinsAttack`, `TemporalSweepAttack`). The round total is 147 seats.
The L1 holds the planner seat. Records: `wave-outcomes.json`,
`wave*-registration.json`.

Learning trends:
- **Expansion unchanged.** The new entry deepens held Go ground. The new
  capability row and new source kinds (official Go source/docs, upstream
  release status) are repertoire, not uncovered ground.
- **Quality improved.** Source-model predictions were superseded by
  runtime-retained observations. One r16 knowledge site was corrected
  line-exactly. The mid-run overclaim was caught and fixed before close.
- **Discernment improved.** Both prior outside routes became grounded
  criteria and fixes (QUALITY #19). This round's gate rejected its own
  overreach, and the pre-registered aether Evidence-ID expectation was
  reported as falsified rather than dropped.

All SHONEN marks stay `[~]`. Current-round non-author admit/reject sampling
remains the closure's duty.

Planned: after the next non-author sample, either (a) depth on Go 1.24/1.25
Swiss-map markup, a replay that confirms or refutes the aether inference with
a second Swiss-map carrier that has method-carrying map types, or (b)
calibration on any routed disagreement from this round's closure. No carrier
is chosen here.

## Round 18 — routed r17 defects, jj-safe revision pins, Swiss-map replay, 2026-10-20

Baseline: `9011581d84527ba34c675f9cf912e54d2e72d470`. C3 predictions frozen and
pushed: `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Claims and amendments:
`.ufo/waves/round-18/claims.json`; motivation in LOG round-18 and
`corpus/lessons/round-18.md`. Measured values and revisions are recorded in the
"Measured records" subsection appended after the verification pass.

### Routed r17 corrections (append-only)

- R17-PINMAP: `SCORECARD.md:2374` ("pre/mid/post pin maps with instants") is wrong for mid-run instants: they retain the comparator verdict against the retained pre map, not the map; round-18 receipts retain each mid map with `map_sha256`.
- R17-VALIDATE16: `SCORECARD.md:2364` ("all 16 receipts `receipt-validate.py` exit 0") had 8 retained validations; the 8 `da64646` receipts now validate 8/8 exit 0 via remapped copies (`.ufo/waves/round-18/evidence/validate16/summary.json`).
- R17-PRODUCER-REV: `SCORECARD.md:2352-2356` names the verification revision; the receipts were produced by 271167473d87ef710f07ecdd98caf0ce12091686 (pass 1) and 95e34db62f2693c455d7ee4dfef24b8f3ebc007d (pass 2).

### Measured records (round 18)

Verification source `db4bdb16b842a93f8ec07523c1275c6dfe0f5229`; evidence
`454dee6923750698cc36041236db13b52c6fcade` (`.ufo/waves/round-18/verification.json`,
69 commands, all expected exits); final rechecks at `454dee6`
(`.ufo/waves/round-18/final-recheck/*.receipt.json`). Baseline `9011581`.

| Claim / axis | Existing numeric proxy | Falsifiable before→after, command and measured revision | Author-side verdict / limits |
|---|---|---|---|
| C1 calibration | 10.0→10.0, delta 0 | Open routed R17 defects 6→0 (named 6→0, substance 6→0): `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root <LANE> --rev <REV> --strict` (exit 1 at `9011581`, exit 0 at `454dee6`). QUALITY admission rows 20→21, rows 1–20 byte-identical (`controls.py 9011581 454dee6`) | **improved**: all six outside-routed defects discharged with named corrections and substance fixes; the r17 partial disagreement became QUALITY #21 with red-before. Limits: wave 2 closed defects by fabrication against the first substance checks; hardened, but the validator digest stays format-only and S033's head / producer-pass attribution are not resolvable offline, so 6→0 is reported with the w2 Truth* re-derivations (`corpus/lessons/round-18.md` Mistakes 6) |
| C2 operability (fleet axis; no owned numeric proxy) | none | Live HEAD-as-revision pins 3→0 (fixture 8→15, annotated 0→6): `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root <LANE> --rev <REV> --strict` (exit 1 at `9011581`, exit 0 at `454dee6`); jj sandbox red-before 14/14 held (`tools/jj-red-before.py`, verification pass); each fixed file restored alone to its baseline bytes reports exactly 1 live site (w2 `LintMutation.md`) | **improved**: the three routed jj risks (round-17 `verify.py` source, citation-drift default `--rev`, custody-pair repo-HEAD) read the branch tip and refuse or flag an off-branch HEAD. Limits: two compare-only HEAD reads behind nested wrappers are invisible to the lint; citation-drift refuses only the literal `HEAD` |
| C3 depth (sourced: S034/S035, with S023/S003/S033) | 10.0→10.0, delta 0 | Labels with a bound retained log and a compare carrying `extra.eof_reads`: 0→15 (`python3 -I -B .ufo/waves/round-18/measure.py <REV>`, field `c3.compare_jsons_with_extra`); 15/15 compare exit 0 against predictions frozen at `eb6c266` before any `analyze`; mechanism status unreplayed INFERENCE → confirmed under the frozen rule (`predictions/decision-rule.json`) | **improved**: both held-out diagnostic carriers (synthetic go1.24.6, real go1.24.13) failed with the exact predicted `Invalid index`; noswiss sibling and 11 non-diagnostic synthetics silent. Limits: held-out confirmation is Go 1.24.x only; one pass; one Ghidra release |
| coverage | 10.0→10.0 | map 95/95→96/96 (`measure.py`, w2 `CoverageMapRow.md`) | unchanged ground: the Go row is held; the entry deepens it |
| freshness | no owned numeric proxy | PR #9348 state re-read (open, head `a214355`); PROVINCE pin drift found (client configs now 6.7.0), not fixed | unchanged; drift routed to the lesson's Open list |
| adjacency | no owned numeric proxy | sibling scan: no lane holds Go map/Ghidra-Go knowledge; jj fact triple-registered (S036/tameshi S061/tabi S049), routed to kumitate | unchanged; nothing absorbed |

No capability row entered (w2 `CapabilityCandidate.md`: `swiss-misread.py` is C3's instrument, not a new repertoire item). Saturation line 10.0 and stagnation window 10 unchanged; last capability entry round 17.

### Waves

W1: 89 seats (executor19/scout23/reviewer15/scribe10/connector8/critic6/revenger4/sentinel2/simplifier2), 89/89 reports; one seat (SwissMisreadTool) ended aborted after writing its report. W2: 98 seats (reviewer53/executor9/scout9/critic8/mutation-tester4/revenger4/connector4/scribe3/sentinel2/simplifier2); 1 dead (GateSUMSRUNLOG, provider usage-policy refusal), 4 not returned at integration (GatePRODUCERREV, TruthREGISTRY, DecisionRuleApply, ShonenLines). Round total 187 seats. The L1 holds the planner seat. Records: `wave1-*.json`, `wave2-*.json`, `w1/`, `w2/`.

Learning trends:
- **Expansion unchanged.** The Swiss-map entry deepens held Go ground (README row 35, PROVINCE Core); no new coverage-map row (w2 `TrendVerdicts.md`).
- **Quality improved.** The r17 aether INFERENCE is replaced by a frozen-before-run replay; six r17 overstatements corrected append-only; S032 superseded by S033.
- **Discernment improved (author-side).** The r17 partial disagreement became QUALITY #21 with red-before; wave 2's falsifications became Mistakes rows 6, 9, 10 and fixes. Outside sampling remains the closure's duty.

All SHONEN marks stay `[~]`.

Planned: after the next non-author sample, (a) depth: a held-out Go 1.25.x Swiss carrier that the emulator predicts to fail (candidates: toolchain binaries under `~/.local/opt/go-1.25.0`), or (b) freshness: PROVINCE pin/cache drift and the census, or (c) calibration on any routed disagreement from this round's closure.

## Round 19 — routed r18 defects, province freshness, toolchain replay, 2026-10-20

Baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; declaration
`85589ac757f9ca3cb25efcd702d0963e25c9c4df`; predictions frozen and pushed
`a1140e76fffdc1be032d9d813dbb686157803bbc`. Claims and in-round amendment:
`.ufo/waves/round-19/claims.json`. Motivation: LOG round-19, lesson round-19.
Final measured revision and verification records are appended after integration.

### Routed r18 corrections (append-only)

- R18-MIDMAP-LISTSTEP: only analyze-step pin checks satisfy the list branch under `--require-mid-maps`; red/green list fixtures in `routed-r18.py`.
- R18-VALIDATOR-DIGEST: round-18 gate recomputes the pinned validator blob digest; eight remapped copies retained and re-hashed under round-19 `evidence/validate16-remap/`.
- R18-STRICT-BASELINE: strict baseline at `9011581` retained (exit 1, open 6), paired with `454dee6` strict exit 0 (`evidence/strict-baseline/`).
- R18-HEAD-ALIASES: citation-drift refuses HEAD-derived/mutable aliases with exit 2; nested compare-only lint limits registered in SKILL.
- R18-DEADSEAT-RECORD: supersedes line 2462's integration snapshot. At `a245bb0`, W2 had 98 registered / 94 reports: GateSUMSRUNLOG (Devin quota after cyber refusals), GatePRODUCERREV and TruthREGISTRY (zai rate limit), ShonenLines (aborted) lacked reports; DecisionRuleApply returned late. Causes retained in round-19 `evidence/r18-dead-seats.json`.
- R18-REGISTRY-PINNED: pins explicitly has no persisted baseline; buildinfo-probe names its source file containing the constants.
- R18-INSTALL-RECORD: Go install versions, full archive hashes, channel, date and reason recorded in round-19 lesson `## Installs`.

| Claim / axis | Numeric proxy | Before → after; counting command | Verdict and limits |
|---|---|---|---|
| C1 calibration | 10.0→10.0 (delta 0, tied-lowest) | Open routed R18 defects 7→0 target: `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root <LANE> --rev <REV> --strict`; B red 7/7/7 named/substance retained | Final measured verdict appended after verification; QUALITY #22 grounds retained per-seat cause records |
| C2 freshness (fleet axis, no owned proxy; sourced S037) | none | `province-pins.py --root <LANE> --rev <REV> --strict` mismatched clients 2→0; c1-census stale 4→0, undeclared unchanged 2 | Freshness of client statements, installed-skill/cache identity and host anchors; not a clean census PASS |
| C3 depth (sourced S038/S035/S023/S003) | 10.0→10.0 (delta 0) | Held-out artifacts with bound logs and compare.json 0→8; `find .ufo/waves/round-19/runs -name compare.json \| wc -l`; revisions B and freeze/run | Mechanism confirmed under frozen index-membership rule: vet index 13902080 is H1-only, seven controls silent. Full read-list prediction falsified for vet: compares 7/8, aggregate exit 1 |

No capability row enters: this deepens held Go ground. Coverage unchanged; no
new coverage-map ground is claimed. Saturation 10.0 / window 10 unchanged.
All SHONEN marks remain `[~]`; outside sampling belongs to closure.

Planned: calibration on outside-routed disagreements, the census's two
undeclared round-17 blocks, and the r12 operability add/withdraw decision;
depth on the emulator's whole-walk versus first-failure read-list discrepancy.

### Round-19 measured records (supersedes preliminary target language above)

Verification source: `b26a6c42207a859e70bd892c7e89a5befedf379b`.
Retained execution evidence: `2a6229f2fb415ba8efecbc2ae24e69ec89b64986`,
`.ufo/waves/round-19/verification.json`: 62 commands with expected exits,
26 content checks, no failed check, identical tool bytes at the two recorded
pin instants, and zero source/tool integrity mismatches. Expected nonzero
results remain explicit: census FAIL/1 and vet full-list compare/1.

| Claim / axis | Measured before → after at B=`8a8da7e` and source `b26a6c4` | Counting command / evidence | Verdict |
|---|---|---|---|
| C1 calibration (owned, tied-lowest) | open/named/substance 7/7/7 → 0/0/0; strict exit 1→0; admission criteria 21→22, old 21 byte-identical | `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root <LANE> --rev <REV> --strict`; `verify/routed-r18-{baseline,source}-strict.stdout`, `controls-r19.stdout` | **improved**, numeric proxy 10.0→10.0 (delta 0); trusted-code counter, not adversarial execution authenticity |
| C2 freshness (fleet axis; no owned numeric proxy) | mismatched clients 2→0, final 9 stated claims / 0 unstated; stale loci 4→0, ambiguous/unresolved 0, undeclared unchanged 2 | `province-pins.py --root <LANE> --rev <REV> --strict`; baseline retained census and final `verify/c1-census-v10.stdout`; no SCOPE/DATED widening | **improved**; census still FAIL/1 on the two carried undeclared blocks, no new marker defect |
| C3 depth (owned, sourced S038 provenance plus S035/S023/S003 mechanism) | frozen labels with current validated bound receipts + comparison 0→8; pass2 validation 8/8 exit 0; compare 7/8, both pass aggregate exits 1 | `python3 -I -B .ufo/waves/round-19/measure.py <REV>` field `c3.bound_validated` (prefers pass2); `verify/receipt-validate-*.stdout`; fresh log extraction and frozen membership checks | **improved**, numeric proxy 10.0→10.0 (delta 0); H1-specific index confirmed in two passes, full-list model rejected, compile's extra RTTI NPE retained |

- R19-C3COUNT: supersedes the preliminary recursive `find runs` count in the
  C3 row above: it counts 16 comparison files after pass2, not eight unique
  labels. The measured command is `measure.py <REV>` field
  `c3.bound_validated`, 0→8; raw pass1/pass2 artifacts remain separate.
- R12-AXIS-DECISION: withdraw operability as an owned-axis improvement from
  the author's r12 scorekeeping, rather than add a new owned proxy.
  Historical outside admission is not rewritten; lesson round-19 records
  the decision. Its source/custody debt is indexed by S039 and disclosed.
- Post-fix falsification: `verify/postfix-mutations.stdout` reports 10 killed,
  0 survived, pristine/relative-root exit 0. The paired strict receipt mutant
  records its intermediate red restoration until the companion receipt is
  also restored; no failed state is concealed.
- No-harm: command A map 96/96→97/97, missing/dangling empty, depth 17/17→17/17;
  scores stay 10.0. LOG/SCORECARD and the r12/r18 knowledge entries retain
  baseline bytes as prefixes. Prior lessons and r17/r18 runs/predictions are
  unchanged; round-19 frozen prediction tree unchanged. No capability row
  added. Sources 36→39 (A 31→34, B4/C1 unchanged, mined34→37/rejected2 unchanged).
- Waves: W1 90 (executor17/scout23/revenger4/connector8/scribe10/critic6/
  sentinel2/reviewer18/simplifier2), 48 reports, 42 reportless with causes
  (9 direct 429 errors, 33 parent-session aborts). Raw terminal records also
  distinguish 20 report-present non-clean last messages. W2 72 (reviewer48/
  mutation-tester4/scout10/connector2/critic4/sentinel2/scribe2), 72 reports,
  72 normal stop records, no dead seat. Two job-cap refusals spawned none;
  the third identical payload spawned W2. Total 162; L1 holds planner seat.

Learning trends (author-side): expansion **unchanged** (held Go ground);
quality **improved** (sourced re-verification, raw anomalies and model
rejections retained); discernment **improved** through outside-routed
R18-DEADSEAT-RECORD → lesson → grounded QUALITY #22. Current outside
admit/reject sampling remains pending, never self-attested. SHONEN stays `[~]`.

Planned (supersedes the preliminary plan): learn from the next outside
sample; census's two undeclared blocks and registered nested-lint limit
remain open. Future model work must forecast first failure and mask the
variadic bit before claiming whole-walk equivalence; no such fix is claimed here.

Exact command forms (run with REV set to baseline or verification source above):

```sh
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B "$LANE/.ufo/waves/round-19/tools/routed-r18.py" --root "$LANE" --rev "$REV" --strict
python3 -I -B "$LANE/.ufo/waves/round-19/tools/province-pins.py" --root "$LANE" --rev "$REV" --strict
python3 -I -B "$LANE/.ufo/waves/round-19/measure.py" "$REV"
```

The census comparison uses the retained baseline output and the current
`python3 -I -B "$LANE/.ufo/gates/c1-census-v10.py" --root "$LANE"` output,
not an unsupported census `--rev` option. C2 is live-host time-indexed.

## Round 20 — routed r19 defects, first-held static tool verbs, first-failure Go forecasts, 2026-10-20

Baseline `14f0260ad319ecc26994381b2415d5a999003375`; declaration
`d1d981d2cc041dda4656c5b01d2c8445d8d17124`; C3 predictions frozen and pushed
`808cbb31a1e24656da5ba4967497e602fbca7415` before the first analyze. Claims:
`.ufo/waves/round-20/claims.json`. Motivation: LOG round-20, lesson round-20,
`corpus/lessons/round-19-verifier-spotcheck.md:178-190`. Attempt 1 ended without a
report (watchdog `lane-dead-no-report kaidoku round=20`); the recovery coordinator
(attempt 2) re-verified and reused the attempt-1 commits listed in the lesson.
Final measured revision and verification records are appended after integration.

### Routed r19 corrections (append-only)

- R19-D1: custody-pair selftest refuses in-worktree scratch (exit 2 `scratch_inside_worktree`) and cleans up; nested residue recorded and removed.
- R19-D2: `tools/evidence-timestamps.py` flags zoned timestamps later than their line's introducing commit; baseline red on round-18/19 claims.
- R19-D3: `tools/carrier-guard.py` arm/check/disarm on all toolchain carriers; per-label clean checks retained before each run.
- R19-D4: `c1-census-v10.py` declares the two round-17 blocks as DATED by stable text anchors; no check deleted or widened.
- R19-D5: `tools/final-census.py` writes `verify/final-census.json` + stdout at the delivered tip; the record commit adds only those two files.
- R19-D6a: `head-rev-lint.py` reports nested compare-only HEAD reads (round-17 `verify.py`, round-18 `revpin.py`) in a `nested` class.
- R19-D6b: `tools/revexec.py` runs revision-extracted Python in a `systemd-run --user` unit (private network, private /tmp, read-only except its work dir).
- R19-D6c: `citation-drift-probe.py` refuses unsafe snapshot slugs (`slug_unsafe`, realpath containment).
- R19-D6d: `receipt-validate.py` authenticates analyze only directly after the `rea-agents@<v>` token (`argv_decoy_refused`).
- R19-D6e: `wave-outcomes.py` keeps a seat named `causes` distinct from the wrapper key (`seat_named_causes`).
- R19-D6f: `jj-red-before.py` selftest gains `jj_relative_traversal_refused` and `jj_tmpdir_scrubbed`.

| Claim / axis | Numeric proxy | Before → after; counting command | Verdict and limits |
|---|---|---|---|
| C1 calibration (owned, tied-lowest) | 10.0→10.0 (delta 0) | routed r19 items open 11→0 target: `python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --root <LANE> --rev <REV> --strict --live`; census FAIL/1→PASS/0; QUALITY 22→25, rows 1-22 identical | Final measured verdict appended after verification |
| C2 coverage (owned; sourced S040-S046) | 10.0→10.0 (delta 0) | CLI verbs named in admitted knowledge 128/153→133/153; targets exercised 0/5→5/5: `python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --root <LANE> --rev <REV>` | Mention-level catalog coverage; `exercised` binds the ev id into retained evidence bytes |
| C3 depth (owned; sourced S047 + S003/S023/S035) | 10.0→10.0 (delta 0) | frozen first-failure labels bound + compared 0→19, matched 19/19: `python3 -I -B .ufo/waves/round-20/measure.py <REV> --freeze 808cbb31a1e24656da5ba4967497e602fbca7415` field `c3.first_failure_bound` | 8 exact `Invalid index` values, 11 predicted-silent; retro 8/8 on r19 logs is a consistency check only |

### Round-20 measured records (2026-10-21; supersedes the tentative target language above)

Verification source **V=`37e10c545a05cf8ede9a2da0e45d44eb13c7835f`** (all integration fixes committed; D5 is open at V by construction and is
closed only by its final-census record commit). Receipts: `.ufo/waves/round-20/verify/round20/`. The record commit adds only
`verify/final-census.json` and `verify/final-census.stdout`; the L1's post-record counter run is retained in the fleet report.

| Claim / axis | Measured result at V | Counting command / receipt | Verdict and limits |
|---|---|---|---|
| C1 calibration | routed items 11 → **1** at V (only D5, the record witness this row's commit is designed to add); census PASS (stale/ambiguous/undeclared/unresolved 0/0/0/0); controls pass; QUALITY rows 1–22 byte-identical, 23–25 appended | `routed-r19.py --root <LANE> --rev V --strict --live` exit1 (`verify/round20/routed-b1b.json`); `c1-census-v10.py` exit0 (`c1-census.stdout`); `controls-r20.py` exit0 (`controls.json`) | **improved**, numeric proxy 10.0→10.0 (delta 0); D5 closes at the record commit (counter run in the report). D6d fix is the successor validator; the pinned W17 bytes are unchanged |
| C2 coverage | mentioned **128/153 → 133/153**; five targets `exercised`; README map 102/102 | `verb-coverage.py --root <LANE> --rev V` exit0 (`verb-coverage.json`) | **improved**, numeric proxy 10.0→10.0 (delta 0); mention-level catalog coverage, not mastery; `list-objdump-architectures` is pathless (`subject: null`) |
| C3 depth | frozen first-failure bound **0 → 19**, matched **19/19**; 19/19 bound receipts valid; freeze `808cbb3` | `measure.py V --freeze 808cbb31a1e24656da5ba4967497e602fbca7415` exit0 (`measure.json`) | **improved**, numeric proxy 10.0→10.0 (delta 0); exact-artifact outcome-held-out only, not version-held-out; comparator checks kind+index |

No-harm: `controls-r20.py` exit 0 (`pass: true`, no failed checks); `evidence-timestamps.py --strict` exit 0 over the round-20 tree
(975 text files scanned, 15 binary blobs reported as skipped, one applied `--allow` for a seat's fixture literal); append-only prefixes
hold; prior runs/predictions unchanged. SOURCES rows 39→48 (S040–S048, all mined; S048 is the installed non-Harmony REA source); the
sources census exits 0 with the carried W04 for S033/S047. No capability row is added. Saturation 10.0 / window 10 unchanged; all
SHONEN marks remain `[~]`.

Corrections to the rows above: C1's counting command must carry `--live` (the leftover check); C2's universal carrier/subject wording is
narrowed for the pathless target; C3's "held out" is limited to prior first-failure outcomes for the exact artifacts; C1 and C3 share
the receipt validator as a verification authority (claim-separability residual, w2 `CriticSeparabilityS.md`).

## Round 21 — record-bound evidence and bounded first-failure observations

Baseline B=`2dd430cb6bcad60ff4db720c052074f1f75eecbc`;
declaration `f4e95af909d692156e984bf2049e1c7fb4a2a836`.
C1 calibration (tied-lowest finite proxy) and C2 depth are distinct predicates,
not two labels for the same move. Claim names below are round-qualified:
R21-C2 is the comparator, **not** R20-C2's five-verb coverage claim.

| Claim / axis | Falsifiable finite move | Counting command | Score delta / limits |
|---|---|---|---|
| R21-C1 calibration, sourced S049/S050 | Frozen twelve record decisions: remove baseline false accepts while retaining positive controls; independent C1 receipt control avoids C3 fixtures | `python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C1`; `tools/isolated-control.py --root <LANE>` | 10.0→10.0, delta 0; finite error discrimination, not mastery/authentication |
| R21-C2 depth | Frozen twenty bounded-observation/failure decisions: malformed input cannot become clean or crash; valid mismatch remains exit 1; nineteen retained matches survive | same battery with `--claim C2 --regression` | 10.0→10.0, delta 0; exact-artifact retrospective compatibility, not new forecast/type-recovery capability |

Frozen contract `53166ab0aae495c964d956050ca0ca3a4f29014a`, concrete fixture
bytes `d93c85887d9ae77d224c82c8f56bc8cca86d1a75`; both precede measurements.
Measured revision/results are appended after the stable implementation lands.
No capability is pre-claimed; saturation 10.0/window 10 and retired axes stay
unchanged. Coverage is not claimed this round; no new knowledge entry or source
row count alone becomes expansion.

Planned (supersedes prior queue): finish the two declared finite improvements,
then take the independent outside admit/reject sample. R20 source-anchor,
lint/sandbox, timestamp exclusions, census/guard bypass and adjacency residuals
remain named in `corpus/lessons/round-21.md`, not silently closed.

### Round-21 measured records — 2026-10-21

Source V=`a75c3c67e4e658a232e1842ab1aceb383b711269`.
Producer: `python3 -I -B .ufo/waves/round-21/verify.py --root <LANE>
--before 2dd430cb6bcad60ff4db720c052074f1f75eecbc --after V`.
Raw argv/stdout/stderr/expected and observed exits: `round-21/verify/*.json`;
summary: **13/13 expected exits**, no failed check.

| Claim / axis | Observed before → after at B/V | Verdict / score |
|---|---|---|
| R21-C1 calibration, sourced S049/S050 | Frozen cases passed 3/12→12/12; false-clean accepts 9→0; crashes 0→0. `verify/before-C1.json`, `after-C1.json`, battery `--claim C1` at B/V. Separate `verify/isolated-without-C3.json`: positive exit0 and decoy exit1 with `analyze_step_unauthenticated`; root holds only validator/pins, no C3 run/prediction | improved, finite record discrimination; 10.0→10.0 delta0 |
| R21-C2 depth | Frozen cases passed 14/20→20/20; false-clean 5→0; undeclared crashes 1→0. `verify/before-C2.json`, `after-C2.json`, battery `--claim C2` at B/V (after adds `--regression`). Nineteen retained R20-C3 log/prediction pairs: 19/19 exit0 and log digests equal | improved, bounded observation semantics; 10.0→10.0 delta0 |

No-harm recount (`controls.py --root <LANE> --before B --after V`,
`verify/no-harm.json`): map102/102→102/102, citations17/17→17/17,
1134 prior R20/knowledge/lesson files checked with zero byte changes,
LOG/SCORECARD prefixes retained, prior25 QUALITY admission rows identical;
new rows26–27 follow. `verify/verb-coverage.json` rebinds all five historical
targets using exact record ids; mentions remain133/153. Pathless objdump and
synthetic Harmony stay limited; no new coverage claim is made.

Frozen-input mutation (`verify/frozen-input-red.json`) exits2 with
`snapshot_tampered`. Self-invocation selftests for binding, comparison,
controls and isolated receipt control all exit0, retaining finding ids.
Manifest inputs are bound to the two named frozen Git commits; these are
snapshot identity checks, not authentication or continuous custody.

SOURCES48→50 (A42→44, B5/C1 unchanged; mined46→48/rejected2 unchanged),
command/outputs in `verify/source-rows.json`; start and final source censuses
exit0 with carried W04 scope warnings. No prior registry cells changed.
No capability row added; no promotion or non-author claim admission asserted.
Current-round outside admit/reject sampling remains the closure's duty.

Planned: learn from that outside sample; retain every explicitly open residual
in lesson round-21. The declared finite work is complete; source-only or proxy
measurements never close the separate provider, authentication or adjacency gaps.

### Round-21 delivered correction measurements

Final measured source F=`2f351728f961f3a9a4f53cd1706ad594bf5b5f9a`.
This supersedes the initial control-independence wording, not the retained
initial V observations. W2 `R21Attack63.md` identified the validator-owned
fixture-builder coupling; independent v1 then failed its positive on missing
metadata (14/16 at `93c931a205e2e52b2a4257e9f895a175ea5f0727`,
`verify/final/summary.json`). Neither failure is hidden.

Actual final command:
`python3 -I -B .ufo/waves/round-21/verify.py --root <LANE> --before
2dd430cb6bcad60ff4db720c052074f1f75eecbc --after F --out-dir
<LANE>/.ufo/waves/round-21/verify/final-fixed`
exited0 with **16/16 expected checks** (`verify/final-fixed/summary.json`).

- **R21-C1 calibration: improved**, delta0 at10.0. Frozen3/12→12/12,
  false-clean9→0, crashes0→0, battery `--claim C1` at B/F; raw records under
  `verify/final-fixed/before-C1.json`, `after-C1.json`. Separate genuinely
  independent positive0/decoy1 succeeds in a root without C3 inputs
  (`isolated-without-C3.json`); v2 template freeze
  `ae73ec7734c8edc70350995267ddc1f0d2f603e4`,
  SHA256 `5346426d237cc56dc8cf7d25187206cab561b91e8b37bd402e85338d112da25c`.
  Both validator/pins digests are retained. Altering that template returns2
  `snapshot_tampered`; the old helper's invalid-revision crash1 now maps2,
  a supplementary compatibility case, not a new frozen-denominator case.
- **R21-C2 depth: improved**, delta0 at10.0. Frozen14/20→20/20,
  false-clean5→0 and undeclared-crash1→0, battery `--claim C2` at B/F;
  final adds `--regression`,19/19 old log pairs match with bound digests.
  C2 source SHA256 stays `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c`.
- **No observed harm in committed controls:**1134 prior files unchanged,
  map102/102, citations17/17, LOG/SCORECARD prefixes, prior25 QUALITY rows
  identical; rows26–28 now present (`verify/final-fixed/no-harm.json`).
  Sources48→50, old48 rows unchanged (`source-rows.json`,
  `source-integrity.json` in that same directory); final census exit0.
  Four schema mutants killed with positives retained/restoration checked
  (`w2/R21Attack65.md`–`68.md`); no general gate-correctness claim.

Waves: W1=64 (executor3/reviewer20/scout20/connector8/scribe6/critic6/sentinel1),
26 reports,19 errors,19 aborts. W2=68 (reviewer56/scout7/connector1/
mutation-tester4),49 reports,19 errors. Total132 seats/75 reports/57
reportless, all causes recorded, no dead-seat replacement. L1 holds the
canonical planner seat. Verdicts remain author-side until independent closure;
all SHONEN marks remain `[~]`, capability table unchanged.

## Round 22 — uncovered catalog evidence and calibrated dispositions

Baseline B=`7787fea4d6fd718726de92ed20759d11ce7b8b48`;
declaration `75f04a446c61761182145c058e545551ca4ecd76`.
Owned coverage/depth/calibration finite proxies remain10.0; C1 and C2
work tied-lowest axes. Stagnation nudge not invoked (last capability17,
window10). No capability, promotion, dynamic ownership or mastery is added.

| Claim / axis | Frozen falsifiable move | Counting command | Baseline / limits |
|---|---|---|---|
| R22-C1 coverage, sourced S051–S053 | T1 bound/sourced exercised count0→k of6; frozen improvement target k>=1, not6/6 | `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev <REV>` | B count0/6, catalog mentions133/153 and zero20, exit1 (`verify/before-c1.json`); after verdict records follow source-revision measurement. Score10.0→10.0 delta0 |
| R22-C2 calibration | T2 receipt-matched dispositions0→14/14, mismatched[]; explicit controls are not claims of actual device/provider absence | same path `tools/count-c2.py --root <LANE> --rev <REV>` | B count0/14, exit1 (`verify/before-c2.json`); score10.0→10.0 delta0 |

Causal separation contract: C1 reads sourced knowledge/evidence-c1 and its
source registry; C2 reads PROVINCE/evidence-c2. `verify.py` applies each
claim's data diff alone onto B in removed private clones and records both
counters, rather than inferring separation from filenames.

Planned (supersedes r21 queue): complete these frozen finite predicates and
the new independent closure's admit/reject sample; retain all explicit
R20/R21 residuals. Kaidoku/revenger overlap remains open, not waived.

### Round-22 read-set / counter-authority correction

Supersedes only the abbreviated `touches`/separability wording in frozen
claims.json: C1 includes the new SOURCES/knowledge/map rows, evidence/c1,
evidence/sources and the static PROVINCE section; C2 includes evidence/c2
and the dispositions section. The old retained catalog and reviewed
R20/R21 helper bytes are immutable shared measurement dependencies, not
C2 data. Source and section partitions are checked explicitly by verify.py;
cross-cell outputs except rev must equal their baselines. Common round
bookkeeping is not claimed as independent domain data.

Current C1 consumes original CLI envelopes only; copies cannot erase parent
refusals. Both gates resolve trustworthy Git inputs; v2 selftest authority
is frozen/expected-v2.json with a digest pinned in each executable. Old
counter sources/v1 inputs are retained for exact original red reproductions.
The original source-link intermediate and the envelope correction get
separate positive/negative records; no old failure or fixture is overwritten.

S051–S057 support this round's entry/source/identifier qualifications; own-work
is permitted by CORPUS, but tier C alone is not admitted. Actual Saber work
adds a partial Flutter positive and an inspect-dart-aot refusal, not a second
held target. Debugger identifiers are corrected in the metric without
claiming tracer ownership or execution. Final measured verdicts and source
revision are recorded after the committed recount; no scalar/capability row
is pre-claimed.

### Round-22 delivered measurements

Measured source V=`e9db7e2d5798ff3d5f1ba5ccd76bb86f2cc5c1bb`;
producer `python3 -I -B .ufo/waves/round-22/verify.py --root <LANE>
--rev V --out <LANE>/.ufo/waves/round-22/verify/final`: exit0,
30/30 expected checks. Raw argv/stdout/stderr/exit and source digests are
retained under verify/final; no whole-wave success is inferred from intent.

| Claim / axis | Actual before → after at B/V | Verdict / score |
|---|---|---|
| R22-C1 coverage, sourced S051–S057 | Held0/6→1/6, only identify-flutter-build. Count command `tools/count-c1.py --root <LANE> --rev B` or V; both exit1 because the completeness gate requires6. Frozen improvement predicate k>=1 verifies. Catalog mentions133/153→135/153, zeros20→18 | improved within finite scope;10.0→10.0 delta0. Positive Saber is partial; inspect-dart-aot is refused, not held |
| R22-C2 calibration | Accounted0/14→14/14, no mismatched/foreign rows. `tools/count-c2.py --root <LANE> --rev B` exits1, at V exits0 | improved, receipt-field/control calibration only;10.0→10.0 delta0 |

No-harm: prior1135 files byte-identical; LOG/SCORECARD prefixes and28 old
admission rows preserved; map102/102→104/104, citation rules17/17.
Causal data partitions pass full cross-output checks;18 run/envelope pairs
and five ADB overrides agree. Selftests32/32 and31/31; changed frozen input
returns2 snapshot_tampered. Source50→57 (A44→51, B5/C1 retained;
mined48→55/rejected2 retained), old rows identical, census exit0.
All evidence: verify/final/{summary,after-c1,after-c2,prior-controls,
separability,provenance,source-rows}.json.

No new capability/promotion/ownership row. Completeness still1/6 and the
remaining five T1 verbs are not claimed. Outside admit/reject sampling
remains pending; no author-side seat becomes a non-author verifier.

## Round 23 — cumulative frozen completeness

Declared R23-C1 coverage only, baseline
`aa1450b82f9ede35aada63efe8a34e01c6e02f72`; finite owned proxies
coverage/depth/calibration remain10.0, so coverage is tied-lowest.
`.ufo/waves/round-23/claims.json` freezes the same six T1 verbs and target
1/6→k/6 with k>=2, never a preclaimed6/6. Counting command:
`python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE> --rev <REV>`.
The inherited counter's actual baseline output is retained in
`before-r22-c1.json`, exit1 and count1. The cumulative implementation will
preserve the original-envelope/source binding and accept the two explicitly
named round evidence roots, not broaden target ownership.

Planned: finish this declared finite move and retain every unheld verb,
R22 reportless-seat uncertainty and outside-review duty explicitly.
No capability, retirement, promotion or mastery is preclaimed.

### Round-23 initial committed measurements

Measured source V=`6615aeae642aec36959180e7ea940b2794c7f1cb`.
Producer `python3 -I -B .ufo/waves/round-23/verify.py --root <LANE>
--rev V --out <LANE>/.ufo/waves/round-23/verify/initial` actually exits0,
12/12 expected conditions; raw argv/stdout/stderr in verify/initial and
verify-initial-producer.json.

R23-C1 coverage: cumulative sourced held1/6→4/6, both counter exits1;
completeness remains incomplete. Exact held set is inherited identify,
inspect-dart-aot, inspect-signal-decoders and decode-signal-recording.
Both debugger verbs remain unheld/Adjacent. Frozen k>=2 improvement verifies
author-side; finite coverage proxy10.0→10.0, delta0. Mentions135/153→137/153
are a separate lexical measure, never the held numerator.

No-harm controls: old1138 files unchanged, old32 QUALITY rows retained,
LOG/SCORECARD prefixes preserved; map104/104→106/106, citations17/17,
SKILL/PROVINCE prefixes retained. Source57→61, A51→55, B5/C1 unchanged,
mined55→59/rejected2 unchanged; old57 rows identical, census exit0 with
carried W04 warnings. R22 counters stay C1=1/6 and C2=14/14.
Independent21-case selftest exits0; changed frozen input returns2;
same metadata input keeps legacy/current positive0/0 but the two named
legacy false accepts0 become current1. Evidence is retained, not inferred.

No new capability, retirement or promotion. W1=64 seats,52 nonempty reports,
12 named provider failures, zero replacements (wave1-outcomes.json).
Fresh W2 falsification and non-author closure remain distinct duties;
author-side verdicts do not certify outside admission.

### Round-23 final delivered measurements

Final measured source F=`fe18f13f79847d88af1efd8e23df3157d70c0171`.
The coordinator materialized verify.py from that exact Git object before
execution; argv/stdout/stderr/executed SHA are in verify-final-producer.json.
`verify.py --root <LANE> --rev F --out <LANE>/.ufo/waves/round-23/verify/final`
actually exits0, **15/15** expected conditions, no failed check.

R23-C1 coverage: **1/6→4/6**, exact unchanged six-verb denominator,
both counter exits1/c1_incomplete. Held set: historical identify plus
inspect-dart-aot, inspect-signal-decoders and decode-signal-recording.
Only debug-with-gdb/debug-with-rizin remain unheld/Adjacent. Frozen k>=2
improvement verifies author-side; coverage finite proxy10.0→10.0, delta0.
Lexical catalog mentions135/153→137/153, not a held-coverage denominator.
Counting command is the declared tools/count-c1.py --root <LANE> --rev B/F;
both immutable outputs are retained under verify/final.

V3 selftest **25/25**; same v3 fixtures against the exact pre-v3 counter
give21/25 with the four named false accepts, positives preserved.
Input tamper, forced Git setup failure and nonroot invocation each produce
declared exit2, not clean. Original-run comparisons and metadata red/green
hold. R22 predicates still1/6 and14/14. All raw records are under verify/final.

No-harm:1138 prior files unchanged;32 old criteria retained; map104/104→106/106,
citations17/17; prefixes and all prior README nonempty lines preserved;
prior round20/21/22 wave trees identical. Source57→63, A51→57/B5/C1,
mined55→61/rejected2; old57 rows identical. S062/S063 correct S058/S061
without rewriting immutable cells. Snapshot census and actual live end census
both exit0; carried W04 plus S062 scope-duplicate warning are disclosed.

W1=64/52 reports/12 reportless; W2=64/64 reports/0 reportless,128 unique
spawns total. Three same-identity successful-critic follow-ups add no seat.
RunBefore's wrong-target run is not credited as a baseline measurement.
No new capability, retirement, promotion or outside admission. Planned:
learn from the independent closure's admit/reject sample; retain all explicit
SOURCE/TIME/LINT-SANDBOX/CENSUS-GUARD/ADJACENCY and unexplained-seat debt.

## Round 24 — frozen instruments, claim-freeze audit, saved-capture family

Declared two claims (`.ufo/waves/round-24/claims.json`), baseline
B=`fe10219ec6e92c32b7eb40d83fbcac888756c6c1`. Instruments were committed at
`97ade2e5` and pinned by sha256 before the freeze commit `5dc49bfe`
(routed r23 defect). Owned finite proxies coverage/depth/calibration tie at
10.0; C1 works coverage (tied-lowest). Last capability round 17, window 10:
no stagnation waiver. Saturation 10.0 / window 10 unchanged; retired: none.

| Axis | Claim | Before → after (counting command, measured revision in the final section below) | Evidence |
|---|---|---|---|
| coverage | R24-C1 | packet-capture family held 0/4 → 4/4 (`python3 -I -B .ufo/waves/round-24/tools/count-c1.py --root <LANE> --rev <REV>`); lexical catalog zero-mention 16 → 12 (a separate measure). Finite proxy 10.0 → 10.0, delta 0. The frozen R23 T1 stays 4/6 | `corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md`; `.ufo/waves/round-24/evidence/c1/`; S064–S067 |
| calibration | R24-C2 | retained claim freezes disclosed with machine-checked instrument status 0/10 → 11/11, round-24 CLEAN (`python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <LANE> --rev <REV> --require-clean round-24 --disclosures corpus/claim-freezes.tsv`). Finite proxy 10.0 → 10.0, delta 0 | `corpus/claim-freezes.tsv`; QUALITY33; S068; lesson M24-1 |
| depth | — | unchanged | — |

Routed r23 defects: README blank separators restored (3); instruments frozen
before claims (one disclosed supersession `9fb4eacd`); reproduction inputs
pinned with official URLs and re-verified 6/6 (`.ufo/waves/round-24/repro/`).
No capability row is entered: the pcap verbs are coverage holdings of an
existing REA route and the freeze gate is a calibration instrument, not a new
repertoire item.

Planned (round 25): learn from the outside closure's admit/reject sample of
S064–S068 and the freeze ledger; consider extending the freeze gate to
instruments named outside `claims.json`; debugger verbs wait on the
kaidoku/revenger L0 ruling.

### Round-24 final measured outcome

Measured revision `5c88c05b8cff9ebd63521c1395fc5295eaded8c3`.
Executed committed `tools/final-measure.py` bytes, producer receipt
`.ufo/waves/round-24/final-producer.json`: exit0, 12/12 expected finite
conditions (`final/summary.json`), not independent admission.

- C1: 0/4 → 4/4, catalog zero16→12; baseline exit1, final exit0.
- C2: original frozen gate after-result 9/11 exact, exit1 (R17/R18 mismatch);
  disclosed revised gate 11/11 exact, exit0. Unchanged prior cohort 0/10→10/10
  disclosed, all FLAGGED; round24 adds one CLEAN author-assessed row. Thus
  C2 is **not met with unchanged frozen bytes**, met under the disclosed
  supersession; independent closure must adjudicate, not silently substitute.
- Post-hoc L1 selftest17/17; R23 stays4/6, R22 stays1/6 and14/14.
- No-harm: 1141 prior files identical, old32 criteria retained + QUALITY33,
  LOG/SCORECARD prefixes; mapping106/106→107/107, citations17/17.
  Whole old SOURCES lines and old README nonempty rows retained;
  all README h2 separators blank, with loss controls red.
- Registry63→72; end census exit0, five W04 (four inherited plus S069's
  duplicate manual URL). Start census is a disclosed later BASE reconstruction.

All finite proxy scores stay10.0. Neither a green producer nor ledger
transcription confers independent admission or mastery.


## Round 25 — prospective explicit-reference custody

Baseline `18e7eb6d9fe8842678af5f1cffbd680ead4ad473`; Parent-landed
prerequisite authority I=`62feef9c0cbd5aadafa453456c55c28832175206`.
One proposed claim R25-C1, **calibration**, a tied-lowest owned finite proxy
(coverage/depth/calibration all10). No score delta, retirement, capability
admission, mastery or promotion is recorded at this prospective phase.

The prospective complete target is every one of the fixed34 exact
process-exit/primary-finding pairs in
`corpus/evidence/round-25/oracle/cases.json`, measured by
`tools/round-25/ruler.py` from I. It is a new explicit caller-selected
reference API, not arbitrary-shell/cohort discovery or an old R24 re-score.
Before availability must come from Main's actual receipt: an absent
candidate means cases not observed/executed0, not34 observed failures.
No after value or verdict is preclaimed.

Planned, superseding the earlier round25 queue: receive the real before
receipt, complete qualified proposal distillation, and have Main decide and
land `reports/round-25/claims.json` with I and all authority digests before
any `tools/round-25/instrument-custody.py` implementation. All original34
targets and full no-harm duties remain; a failed/unprovable target is not
converted to a narrower or exploratory claim.

Original R24 frozen C2 remains **unmet9/11 exit1**; replacement11/11 is
only disclosed ledger agreement. R23 six-verb4/6 and R24 four-verb4/4
remain distinct. QUALITY33's literal subject/measurement cycle is unmet
conformance debt, and its unchanged R24 detector does not discover the new
durable claims path: undetected, not CLEAN. See
`corpus/lessons/round-25.md` for S073, source/rejection decisions, conduct
limits, exact prerequisite digests and Parent-only admission authority.


### Actual round25 prerequisite before

Main's actual I ruler over B returned exit2/candidate_unavailable:
declared34, executed0, exact0, all34 not_observed, candidate SHA null.
Receipts: `corpus/evidence/round-25/prerequisite/parent-before-process.json`
and `parent-proof.json`. Wrong oracle SHA returned exit2,
finding=`could_not_evaluate`, error=`snapshot_tampered:oracle`
(`parent-tamper-process.json`). This establishes
unavailable-before, not34 empirical old failures or an after verdict.
Prospective full SRT: `reports/round-25/claims.json`; implementation remains
stopped until qualified distillation, Main decision and actual SRT landing.


### Prospective round25 claims path correction

Before any SRT freeze, Main corrected its earlier categorical `.ufo/**`
helper-scope premise. The exactly named future claims file
`.ufo/waves/round-25/claims.json` is not ignored (actual own check-ignore
exit1/unmatched record); it is prospectively selected instead of the
unlanded reports-path draft. I and the complete34 targets stay unchanged.
This removes the planned reports-path discovery mismatch, not QUALITY33's
literal cyclic debt. No old-detector CLEAN or old-matrix rerun is claimed.
Full correction and retained earlier phase statements: lesson round25,
Prospective path erratum before claims freeze.


### Round25 full preregistration handoff, no after verdict

The actual planner and distiller are terminal completed; total66 actual seats
retains the POSTproposal planner chronology and W1 executor0/required3 UNMET
debt. Distillation retains one calibration claim and all34 I wants, not
broader discovery, alternate labels, basename guessing or a prior-round rescue.
Pin scope is63/64 reported matches plus P55's unqualified post-barrier mismatch;
scratch/draft/role limitations are retained, not cleared by report counts.

The exact prospective SRT is `.ufo/waves/round-25/claims.json` WITH dash.
The selected subject is openly named inside claims[] as a post-freeze
candidate, not a preexisting counting authority. Main B2 permits only a later
truthful R25 FLAGGED ledger append after actual F and full measured metadata
findings, preserving the header/all11 old rows. No anticipated row, matrix
rerun, actual twelfth-freeze observation or old-detector CLEAN is claimed now.
Any eventual exit0 from disclosure agreement is not12 clean rounds or
original R24 C2 rescue; cyclic debt remains unmet.

All34 full after targets, exact pinned authority, actual unavailable-before
receipt and explicit no-harm duties (including that narrow additive exception)
are submitted for Main's decision. No SRT or code approval follows from this
entry. `corpus/lessons/round-25.md` and
`corpus/evidence/round-25/proposal/{distillation.md,qualification-erratum.json,actual-seat-budget.json}`
carry complete qualified evidence; the original distillation is unchanged.


### Pre-F v2 — full contract is not the34 score

Main's outside critic held F. Frozen v1 files/hashes remain preserved;
I/original34 and the real before2/executed0/not_observed34 remain unchanged.
Separate prospective Main-held H01–H16 and variants are now defined at
`corpus/evidence/round-25/main-held-contract-controls.json`; their outcomes
are not yet observed and are never folded into34. C1 also requires real
first-add/ancestry/at-before/unique-parent blob+mode, nonregular/history,
duplicate/unknown-member, direct Git-ENV and semantic scope/output behavior.

Even34/34 fails C1 for oracle/test/ruler/gate/fixture expected-answer logic,
imports/execution or case-keyed answer tables. Explicitly selected Git blobs
may only be read opaquely as custody data. Main-held dataflow/consumer
evidence, not a source-word test, decides this rule. Shared-state quiescence
is required; a guard/resource/setup abort is CNE, not candidate failure.

The distiller's own outside scratch/pickle write and false sole-file claim
are added as unqualified provenance, with original report unchanged and no
pickle access or replacement. All role/pin/epoch/old9/11 debts survive.
S073 is narrow; new S074 supplies additional primary primitives, with local
policy/census URL limits explicit. No after score, capability admission,
F or implementation permission is claimed at this handoff.


## Round 25 attempt 3 — repair the round-24 outside verdict, then name EVM selectors

Round-24 outside decision: `corpus/lessons/round-24-verifier-spotcheck.md` records round 24 as **not admitted, rejected-honest-stop** (R24-C1 coverage improved and finite; R24-C2 calibration unmet at 9/11 on its original frozen gate). This card accepts that verdict; no round-24 score or verdict above is rewritten.

Claims (frozen by attempt 2 at `7ef837a473ae65d924b9ea34e7748f722a6cd7d5`, instruments at `9dcd11ecb412fe4828f274580018039b8edbc05a`, kept unchanged by attempt 3): R25-C1 calibration, 5 fixed self-assessment items, mismatches 5 → target 0; R25-C2 coverage, knowledge Markdown 107 → target 108 with the EVM selector-naming entry sourced by a row opened 2026-10-22. Attempt 1's prospective 34-case custody claim (`.ufo/waves/round-25/claims.json`) was not continued and has no after value.

| claim | axis | score delta | before → after | counting command | measured commit | evidence |
|---|---|---|---|---|---|---|
| R25-C1 | calibration | finite proxy 10 → 10, delta 0 | 5 → 0 mismatches of 5 fixed items (exit 1 → 0) | `python3 -I -B tools/round-25/a2/c1-calibration.py --root <LANE> --rev <REV>` | before `9dcd11ec`; after `0e333eb2fc25f538a99058761f379845f2534c42` (C1 alone) and `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (both claims) | `corpus/evidence/round-25/a2/before/c1-calibration.json`; `corpus/evidence/round-25/a3/after/c1-at-0e333eb2.json`, `c1-at-08c7a729.json` |
| R25-C2 | coverage | finite proxy 10 → 10, delta 0 | knowledge Markdown 107 → 108; entry sourced 0 → 1 (S075, S076, S077 qualify) | `python3 -I -B tools/round-25/a2/c2-coverage.py --root <LANE> --rev <REV>` | before `9dcd11ec`; after `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` | `corpus/evidence/round-25/a2/before/c2-coverage.json`; `corpus/evidence/round-25/a3/after/c2-at-08c7a729.json`; `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` |

Command A at `08c7a729`: mapped 108/108, missing [], dangling [], rule blocks 17/17. A green C1 shows five fixed statements agree with the repository; it is not a full audit of SCORECARD or SHONEN. C2's counter checks presence, count and source linkage, not the entry's truth; the falsify seats and the closure judge the content. No axis is retired; no capability row is added.

Wave 1 found further self-assessment statements outside the five frozen items that disagree with the repo (seat report `.ufo/waves/round-25/a3/w1/C1Cherrypick.md`): the depth row's 9/9 and `SKILL.md:77-191` (recounted above as 17/17, `SKILL.md:81-318`), the coverage and calibration rows' measured-revision cells, and SHONEN's "province-version alignment is contested" clause. Only the depth row was refreshed; the rest stay open. Both frozen instruments accept some false statements and reject some true ones (seat reports `C1Mutation.md`, `C2Mutation.md`): for example I4 takes the first `| coverage |` row and never reads the README map, and the C2 counter checks the `opened` cell, not that the page was opened. The landed bytes do not use those gaps (command A 108/108 at `dc31f9c4`; saved page copies in `corpus/evidence/round-25/a3/sources/`).

- **planned:** depth — one-pin evidence-id identity table for the eight native readers at `rea-agents@6.5.0` (wave-1 seat report `PlannerWalk.md`, candidate C-C; before 0/8 rows at that pin), with the counting script and expected values committed before any REA run. Second choice: score a frozen EVM naming rule on carriers not used in round 25 (lesson M25-8).


## Round 26 — native reader evidence-ID identity at 6.5.0, and six stale self-assessment items

Base `a0639d8e61e486e2a716ff94cddd89a73200a02c`. Claims frozen definitions-first at `c27f445e70cedbaf5300b2fd0a53e821d9b659a9` (`.ufo/waves/round-26/claims.json`); one pre-freeze REA probe (`inspect-binary-layout` on `/usr/bin/jq`, 11:59:16Z) is disclosed there and was not used as a table row. The round-25 planned field asked for the counting script and expected values before any REA run: the counting rules and target values were frozen first, but the scripts were written in wave 1 and committed after the runs (C2 instrument at `81f63f36`, before any repair; C1 instrument at `bd0c84bc`, after the C1 data at `ebe2cb4a`). This is the round-24 freeze gate's INSTRUMENT_ABSENT case and is recorded as such in `corpus/claim-freezes.tsv`.

| claim | axis | score delta | before → after | counting command | measured commit | evidence |
|---|---|---|---|---|---|---|
| R26-C1 | depth (learning claim) | finite proxy 10 → 10, delta 0 | rows complete 0 → 8 of 8; entry_ok 0 → 1 (exit 1 → 0) | `python3 -I -B tools/round-26/c1-id-identity.py --root <LANE> --rev <REV>` (sha256 `11c27422…18fa`) | before `a0639d8e`; after `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` | `corpus/evidence/round-26/before/c1-at-a0639d8e.json`, `corpus/evidence/round-26/after/c1-at-ebe2cb4a.json`; `corpus/evidence/round-26/c1/table.tsv`; entry `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`; S079, S080 |
| R26-C2 | calibration | finite proxy 10 → 10, delta 0 | 5 → 0 mismatches of 6 fixed items K1–K6 (exit 1 → 0) | `python3 -I -B tools/round-26/c2-calibration.py --root <LANE> --rev <REV>` (sha256 `3b0f6507…7e8e`) | before `a0639d8e`; after `46ebfd2f0170266646d7cd525be4d46929e953fc` | `corpus/evidence/round-26/before/c2-at-a0639d8e.json`, `corpus/evidence/round-26/after/c2-at-46ebfd2f.json`; seat report `.ufo/waves/round-26/w1/C2BeforeManual.md` (5 of 6 by hand) |

What R26-C1 adds: seven of the eight native reader verbs (`analyze`, `inspect`, `decompile`, `xrefs`, `read-bytes`, `function`, `instructions`) mint content-keyed ids at 6.5.0 on this carrier, and `inspect-binary-layout` is path-sensitive because it writes the run path into hashed fields; ids differ between 6.5.0 and 6.7.0. Its counter re-derives verdicts from committed envelopes; it does not check the pin, the run paths or the verb argv (wave-1 critic `C1Sizing.md`), which the falsify wave checks directly.

What R26-C2 shows: the six fixed statements agree with the repository at `46ebfd2f`. It is not a full audit. Wave-1 critic `.ufo/waves/round-26/w1/C2Cherrypick.md` found 11 further self-assessment statements in this card (round-1 sections, capabilities pointers, the round-25 planned field) that disagree with the repository; they stay open and are disclosed here. The frozen K6 rule does not read the SHONEN box mark, so a box flipped to `[x]` would pass it (wave-1 mutation report `MutR25Calib.md`, M6 and M9).

Outside decision on round 25 (`corpus/lessons/round-25-verifier-spotcheck.md`): admitted, both claims verified. Its routed defects were worked this round: the SKILL.md custody note, the round-25 entry correction (138 responses are 2 per 69 carrier-selector rows; up to three carriers, not four), QUALITY row 35, new counters with red fixtures instead of reusing the round-25 instruments, and Sources counted from the lane-round base. Round-24 outside source decision (QUALITY row 35): the round-24 spot-check disagreed with the initial capinfos rejection and agreed with the later S071 flip (`corpus/lessons/round-24-verifier-spotcheck.md:44`, `:61`).

No axis is retired; no capability row is added.

- **planned:** depth — a renamed-copy and second-carrier extension of the identity table (does a different file name or extension change the seven content-keyed ids; one non-jq ELF), measured by the same counter pattern; second choice: calibration on the 11 disclosed statements from `C2Cherrypick.md`.

### Round-26 falsify-wave corrections (wave 2, 32 seats, `.ufo/waves/round-26/w2/`)

- R26-C2 wording (seat `C2Width.md`): read "the six fixed items K1–K6 pass their frozen claims.json rules at `46ebfd2f` (and at the later commits); 5 of the 6 failed at `a0639d8e`". The rules check counts, revisions, a substring and the absence of the word "contested", not whether each statement is true; K5 checks a revision prefix and does not run command B. Of the 11 further statements from `C2Cherrypick.md`, 8 are observed disagreements and 3 (its items 1, 8 and 9) are partly inference; the grouping above was loose (they sit in the header lines 12 and 14, the round-1 sections, Open gaps lines 78-83 and the planned field at 152-154, not in the capability pointers, which hold).
- SHONEN line 12 was refreshed again after the measured commit: it said the 6.5.0/207/v42 observations were "superseded" at `PROVINCE.md:8-14`, but v42 is current at `PROVINCE.md:24` (seat `ScorecardRowsTruth.md`); it now says they agree. K6 passes either way and could not catch this.
- R26-C1: both counters have disclosed false accepts (lesson `corpus/lessons/round-26.md`, M26-5 and "Falsify-wave findings kept as disclosures"). The committed envelopes themselves were checked directly: 24 of 24 match their frozen argv, paths, call-record sha256 and the 6.5.0 id rule, and none is the probe (seats `ArgvAndPaths.md`, `RecomputeIndependent.md`, `PinEvidence.md`).

## Round 27 — renamed-copy evidence-ID identity on two carriers (honest stop, 15 of 16) and a cross-pin attribution capability

Base `cd32264f7ee356a9c0f48bd8e3fcdac222db22a0`. Claims, both counters, their red selftests and before receipts frozen together at `a4f674b343d8564e21f7eb8984630a95089c82d6` (`.ufo/waves/round-27/claims.json`), before any data. C1 data `9dca26df135a2c558aaa575534ad42662b372d5d`; entry `c6d619a3c50e39dbb830de28146362e360d170d7`; C2 tool and capability row `97358f759a531f7ebc0354fb937d546da8d3b8bd` (measured revision for both claims). Receipts: `.ufo/waves/round-27/before/`, `.ufo/waves/round-27/after/`.

| claim | axis | before (at `cd32264f`) | after (at `97358f75`) | counting command | verdict |
|---|---|---|---|---|---|
| R27-C1 renamed-copy and second-carrier identity table plus entry | depth (learning claim) | rows_complete 0/16, entry_ok 0, exit 1 | rows_complete 15/16, entry_ok 1, exit 1 | `python3 -I -B tools/round-27/c1-rename-identity.py --root <LANE> --rev <REV>` | target missed: honest stop. The tinyxxd `inspect-binary-layout` base and repeat runs returned byte-identical envelopes (`meta.duration` `132ms` twice) and the frozen counter refuses shared envelope bytes (lesson M27-2, QUALITY row 40). No run was substituted. |
| R27-C2 cross-pin attribution tool, capability row, S081 | operability (fleet axis, unowned proxy; capability acquisition) | r26_rows_ok 0/24, red_ok 0/3, capability_row 0, source_row 0, exit 1 | r26_rows_ok 24/24, red_ok 3/3, capability_row 1, source_row 1 (S081), exit 0 | `python3 -I -B tools/round-27/c2-xpin-check.py --root <LANE> --rev <REV>` | target met |

Owned axes rows above are unchanged this round. Coverage recipe A at `97358f75` gives 110/110 knowledge files mapped (`missing []`) and depth 17/17 rule blocks; the coverage row keeps its round-26 measurement (109/109 at `ebe2cb4a`), and this line is the current count.

What R27-C1 still adds although it missed: the 6.5.0 id of `analyze` and `inspect` depends on the file extension through `normalized_result.document` (`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`; SKILL.md section "Evidence-ID identity under a renamed copy and on a second carrier — round 27"). The claim as frozen is not met, and this card does not count it.

Width disclosures (wave-1 critics `CriticClaimWidth.md`, `ReviewC2Checker.md`, `MutC2Checker.md`): "At rea-agents@6.5.0" rests on the invocation and the per-call `package.json` read; the C2 checker does not count the tool's exit code and cannot see a retyped projection; "each round-26 envelope" means the 24 committed under `corpus/evidence/round-26/c1/envelopes/`.

### Round-27 hygiene corrections (not a claim)

The 11 statements from `.ufo/waves/round-26/w1/C2Cherrypick.md`, disclosed at the round-26 section above, re-derived by wave-1 reviewer `.ufo/waves/round-27/w1/ReviewHygieneTargets.md` (8 observed disagreements; items 1, 8 and 9 are partly inference) and drafted by scribes `HygieneA.md` (items 1-6) and `HygieneB.md` (items 7-11). Old lines stay as written; each bullet gives the corrected reading.

- SCORECARD.md:12 says "`[INFERENCE]` calibration is the lowest axis under these heterogeneous, bounded proxies"; observed the three Owned axes rows at SCORECARD.md:23-25 all score 10 (coverage 9.72 → 10.0, depth 10 → 10, calibration 0 → 10) and SCORECARD.md:2941-2942 says "a tied-lowest owned finite proxy (coverage/depth/calibration all10)" (`grep -n "^| coverage | \|^| depth | \|^| calibration | " SCORECARD.md`; `sed -n '2941,2942p' SCORECARD.md`; exit 0); corrected reading: the line is a baseline-era [INFERENCE] claim, and the current card reads calibration as tied-lowest at 10/10/10, not lowest.
- SCORECARD.md:46 says "Current map is 70/72, missing r14-01 and r14-02"; observed recipe A at main gives `{"mapped":109,"knowledge_files":109,"missing":[],"revision":"a4f674b3…"}` (`python3 -I -B recipeA.py a4f674b343d8564e21f7eb8984630a95089c82d6`; exit 0); corrected reading: the C6 row is a round-1 baseline record; at main the map is 109/109 with no missing entry.
- SCORECARD.md:55 says "Historical 70/70 is not current 72/72"; observed recipe A at main gives mapped 109/109, missing [] (same command, exit 0); corrected reading: the current map is 109/109, so the "72/72" figure and the "All 72 files stay in the denominator" clause at SCORECARD.md:53-55 are stale.
- SCORECARD.md:77-80 says the old jq provenance entry's payload "remains correction debt"; observed the r2 shadow-verdict file carries a "Safety-verdict scope (round 9)" note at line 244 (commit 40162fc7, 2026-10-16) and the r3 provenance file carries the "Safety-verdict scope (arc2-loop1-round1)" note at line 141, and SCORECARD.md:681 already records "r3-jq-provenance unscoped safety-label loci 2 → 0" (`git show a4f674b3:corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md`; `git show a4f674b3:corpus/knowledge/2026-10-13-r3-jq-provenance.md`; exit 0); corrected reading: the benign phrasing is qualified by explicit scope notes appended in the corpus files themselves (r2:244, r3:141), so the named correction debt is discharged, and the PROVINCE.md:107-109 pointer holds under the card's baseline-citation rule (SCORECARD.md:16-17) with the identical refusal block at baseline 107-109 and current 114-116 (sha256 78f40919e4dc…00b3).
- SCORECARD.md:81-83 says "real compiled EVM input … large PE analysis … remain as documented"; observed PROVINCE.md:91-93 holds real solc-0.8.37 EVM carriers (Core, arc3-r1/r3) and PROVINCE.md:139-144 marks ">90 MB PE scale wall — CLOSED", with SCORECARD.md:622 capability row "runs REA/Ghidra analyzes of 91.6MB-class PEs" (`git show a4f674b3:PROVINCE.md`; `sed -n '622p' SCORECARD.md`; exit 0); corrected reading: "real compiled EVM input" and "large PE analysis" are no longer open frontier items; "oversized cores" (PROVINCE.md:84-86), "device-dependent ADB" (PROVINCE.md:149-150), "alternate providers" (PROVINCE.md:87-88), ".jsc source mapping" (PROVINCE.md:145-146) and "runtime-capture limits" (PROVINCE.md:103-104, SKILL.md:61) remain as documented.
- SCORECARD.md:152-154 says "planned: calibration — reconcile the still-historical province/skill surface summaries against the live version-pinned REA inventory, with an explicit old/new-name set"; observed SCORECARD.md:56 says "Version drift: closed by luna-round-2 (2026-10-16)", while PROVINCE.md:45 still lists `npx -y rea-agents@6.4.0 --version` → `6.4.0` (2026-10-13 receipt) and SKILL.md:12 still names 6.4.0/170/127 as the owned surface, and no explicit old/new-name set is found in SKILL.md/PROVINCE.md (`grep -rn -i "old/new\|old name\|new name\|verb rename\|renamed verb" SKILL.md PROVINCE.md`; exit 1); corrected reading: the version-drift close at SCORECARD.md:56 covers the per-client pin and receipt inventory, while the province/skill surface-summary reconciliation is still outstanding (historical 6.4.0 wording remains at SKILL.md:12 and PROVINCE.md:45; no old/new-name set exists).
- SCORECARD.md:907 says "capability row entered" for the citation-drift probe (arc2-loop1-round4: "no citation-drift tooling → committed probe (selftest 10/10, findings=0 at HEAD, could-not-evaluate paths each exit 2 with a verdict line) + SKILL.md registry row + capability row entered"); observed no capability table row mentions citation-drift — the card holds four capability tables (:617, :2133, :2205, :2372) with 7 rows card-wide (:619-622, :2135, :2207, :2374), none of them a citation-drift row, and the row text appears only inline at :918-919 (`grep -n '^| Capability | What it can now do' SCORECARD.md` → 617, 2133, 2205, 2372; awk over those tables → 7 rows, 0 mentioning citation-drift); the card already names the gap at :1267-1268 ("r4's citation-drift row never entered the capabilities table; low value, named"); corrected reading: the probe and its SKILL.md registry row landed, but the capability row never entered the Capabilities tables; :907 reads as the round-4 claim and the carried debt is disclosed at :1267-1268.
- SCORECARD.md:615-624 says the `## Capabilities` section lists the lane's capabilities; observed the section holds 4 rows (:619-622) while the card holds 7 capability rows card-wide (:619, :620, :621, :622, :2135, :2207, :2374), and the section has no pointer to the appended tables — the only related note, at :2137-2138 ("This is an append-only capability record; the earlier line-addressed summary table is unchanged"), points backwards from the round-13 section, not forward from `## Capabilities` (awk count over the four table headers → 7 rows; sed -n '2137,2138p' SCORECARD.md); corrected reading: the section is the 4-row summary; the card-wide count of 7 is recorded by :2364 ("capability rows 6→7"), so a reader of `## Capabilities` alone undercounts by 3 — read the three appended `### Capability addition` tables at :2131, :2203 and :2370 for the full repertoire.
- SCORECARD.md:631-632 says "Capabilities entered the table in rounds 6-8 (inside the window), so the nudge did not trigger during the arc"; observed the same table now carries rows first working in arc2-loop1-round2 (:621) and arc2-loop1-round7 (:622), and three further rows were added in rounds 13, 14 and 17 (:2135, :2207, :2374); the sentence was true when declared at luna-round-10 (`git show 661ce3e3:SCORECARD.md` → capability header at :617 with exactly two rows, first-working rounds luna-round-6 and luna-round-8); corrected reading: this is a luna-round-10 declaration about the luna arc, not a current description of the table — the table today spans first-working rounds luna-round-6 through round-17.
- SCORECARD.md:14 says "Numeric axis fields satisfy fleet `AXES.md:33-39`"; observed the fleet AXES.md (sha256 04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993) lines 33-39 are now the round-admission rules ("At least one claim works the lane's lowest-scoring non-retired axis…"), and the numeric field spec lives at AXES.md:79 ("| axes | Axis name → score 0–10 + evidence pointer … → last-change round |") — while the fleet revision in force when the pointer was written (c265db9b, 2026-10-15) had the SCORECARD.md contract table at exactly 33-39 with the axes rule at 37 (`git -C /home/vgpnk/Projects/shokunin show e867f78:AXES.md`); AXES.md moved on 2026-10-16 in fleet commit 84bade0; corrected reading: the numeric-axis fields satisfy the fleet contract, but the live pointer is AXES.md:75-82 (specifically :79), not :33-39; the pointer was correct when written and drifted with the fleet file, which is outside the lane tree so the baseline-scoped citation rule at :15-16 does not shield it.
- SCORECARD.md:3061 says the planned depth claim runs "with the counting script and expected values committed before any REA run"; observed round 26 departed from that order — a pre-freeze REA 6.5.0 `inspect-binary-layout` probe ran at 2026-10-22T11:59:16Z (exit 0) and `tools/round-26` was absent from the freeze commit (`git cat-file -e c27f445:tools/round-26` → exit 128), a departure now disclosed in the card at :3066 and in `corpus/claim-freezes.tsv:14`; round 27 repeats the shape — one probe at 2026-10-22T14:45:23Z ahead of its 14:51:23Z freeze commit (claims.json `pre_freeze_probe`), excluded by the C1 counter which refuses runs whose utc_start is not after the counter commit (`grep 'not after counter commit' tools/round-27/c1-rename-identity.py`); corrected reading: :3061 is a round-25 plan text that round 26 did not follow in order (disclosed at :3066 and claim-freezes.tsv:14), and the current planned field is :3081.

- **planned:** coverage — move one `PROVINCE.md` `## Frontier` bullet (for example one PE subtype) into Core with a counter, red and green selftest cases (including a legitimate look-alike, QUALITY row 40) committed before any data; the evidence-ID surface has now run two rounds (26, 27) and round 28 must work a different frontier area (session drift sentinel). Second choice: a repaired duplicate-bytes gate (QUALITY row 40) committed before new runs on a third carrier, declared as a new claim with its own freeze.

### Round-27 falsify-wave corrections (wave 2, `.ufo/waves/round-27/w2/`; appended)

- Hygiene bullets above: their line numbers refer to `a4f674b343d8564e21f7eb8984630a95089c82d6`, and "at main" in two bullets means that revision. From `97358f75` on, every line after 622 is one higher (the capability row went in at 623). At the tip the `## Capabilities` section holds 5 rows and the card 8; the current map count is 110/110 (the round-27 line above), not 109/109; the current planned field is the round-27 one (`CriticNoCalibrationClaim.md`).
- Capability row "cross-pin evidence-ID attribution": the result is a fit of the stored id to each package's projection-and-digest rule on the `.data` record, not a 6.7.0 run. A record whose `relationship_coverage` is set, or whose key is missing, always prints `both`; `--parse` shows each package's own accept or reject and separates the 37 keyless lane records (6.7.0 rejects all 37). Bare records without an envelope exit 2. Receipts hold no real `6.7.0` label yet; a wave-2 seat ran the tool on 95 round-26 arc3 envelopes and got 83 `6.7.0` and 12 `both`, matching round 26 (`CriticCapabilityRow.md`; not committed as a receipt). The six `both` rows among the round-27 C1 envelopes are the `function` verb (operation `analyze_function`) (`XpinOnR27Envelopes.md`).
- `python3 -I -B tools/round-27/c2-xpin-check.py --selftest` exits 1 at and after `97358f75` (case `correct-stub` expected exit 1 while the rows were absent); this is a fixture anchored to the pre-row state, not a claim failure (`RecountC2.md`).
- planned (supersedes the planned field above; `CriticPlanned.md`): coverage — the `PROVINCE.md` Frontier bullet "EVM bytecode (extended)": freeze, before any lookup or REA run, the round-25 naming rule, a held-out carrier list from the committed runtime-plus-ABI directories not in `corpus/evidence/round-25/a2/c2/carriers.tsv`, an offline counter that scores rule output against each compiler ABI, and red and green selftests. The PE-subtype example is not runnable here (no ARM64X carrier on this host). Second choice (not evidence-ID): reconcile the historical 6.4.0 wording at `SKILL.md:12` and `PROVINCE.md:45` (hygiene item 6). A third evidence-ID round would trip the session drift sentinel.
- Wave 2 had 34 seats; 6 mutation-tester seats died at spawn with "Error: No model selected." (`MutQualityRow38`, `MutQualityRow39`, `MutQualityRow40`, `MutXpinTool`, `MutLessonM27`, `MutC1DupGate`); not replaced or rerouted (Main route notice 15:40Z: the role's route was degraded from 15:14Z).
- Hygiene bullets, further errors found by `.ufo/waves/round-27/w2/ReviewHygieneLanded.md` (8 of 11 bullets fail as written; read them with these corrections): bullet 1 rests on a round-25 sentence written "at this prospective phase" (`:2938`, `:2944`) and "tied-lowest … not lowest" contradicts itself, so the line-12 reading stays inference; bullets 2 and 3 measured recipe A at `a4f674b3` (109/109), not at main (110/110 from `97358f75` on); bullet 8's "undercounts by 3" is a reading of a split layout (the card keeps capability rows in four tables at 617, 2134, 2206 and 2373), not an observed error; bullet 9's span is now through round 27 (row 623) and the rows sit in separate appended tables; bullet 10's "fleet revision c265db9b" is a lane commit and the AXES rule lines are 16-17; bullet 11's probe was never a `runs.tsv` row, so "excluded by the C1 counter" is wrong (the counter never saw it). The "current planned field" is the one in this corrections list, which supersedes the field at the end of the round-27 section.
- QUALITY row 36 pointer (`ReviewGate.md`): round 27 reverses the round-26 Gate decision that left the 6.7.0 installed code without a row (`corpus/lessons/round-26.md:37`); the round-26 spot-check disagreed at `corpus/lessons/round-26-verifier-spotcheck.md:165` and routed it as defect 1 (`:197`); S081 is the new code row.

## Round 28 — held-out test of the round-25 EVM naming rule (honest stop, 60 of 61) and openchain's `filtered` flag from code

Base `935c36608008f79e3dea4f1ed191df3c89e3b848`. Outside decision on round 27 recorded first: `corpus/lessons/round-27-verifier-spotcheck.md` rules round 27 not admitted, `rejected-honest-stop` (R27-C1 15/16; R27-C2 met), with discernment `improved` (spot-check `:140`). Attempt 1 froze R28-C1 at `87d3dfb65fec4b636664bd5727822feba5d35317` (`.ufo/waves/round-28/claims.json`) and R28-C2 at `86fa8526aeaf98704f22a17dcb9965fb087b0be1` (`.ufo/waves/round-28/claims-c2.json`), each with counter, selftest and before receipt and with every file the counter loads pinned (routed defect 4). It then collected C1 runs (`ca4069a4`), C1 lookups and tally (`cb8d495e`) and the C2 fetch, and died at 17:26Z. Attempt 2 committed the C2 fetch and attempt 1's unsent wave files (`a267311678309fd17772407e8afa122ec3219289`), then the entries, rows and lesson (`9db24c9e10287d44d9f780d782ab608f3c84ff5a`, the measured revision for both claims). Receipts: `.ufo/waves/round-28/before/`, `.ufo/waves/round-28/after/`.

| claim | axis | before (at `935c3660`) | after (at `9db24c9e`) | counting command | verdict |
|---|---|---|---|---|---|
| R28-C1 round-25 naming rule scored on 61 held-out carriers / 187 held-out selectors, plus entry | coverage (learning claim; PROVINCE Frontier "EVM bytecode (extended)") | runs_ok 0, rows_complete 0, tally_equal 0, entry_ok 0, exit 2 (frozen lists absent) | runs_ok 60/61, rows_complete 186/187, tally_equal 1, entry_ok 1, exit 1 | `python3 -I -B tools/round-28/c1-heldout-naming.py --root <LANE> --rev <REV>` | target missed: honest stop. REA 6.5.0 refused carrier h09 (`invalid_format`: an unlinked-library placeholder `__$a2bad930…$__`, S086). The carrier list was frozen without a hex screen (M28-1, QUALITY row 43). No re-run, no list or counter edit, no narrowed target. Observed triple: named 137, right 137, wrong 0 |
| R28-C2 openchain `filtered` flag follows Sourcify `filterResponse` (S084, S085), plus entry | depth (learning claim) | responses_complete 0/230, entries 0, mismatches 0, predicted_true 0, entry_ok 0, exit 2 (pinned inputs absent) | responses_complete 230/230, entries 246, mismatches 0, predicted_true 59, entry_ok 1, exit 0 | `python3 -I -B tools/round-28/c2-filtered-flag.py --root <LANE> --rev <REV>` | target met |

Owned axes rows above are unchanged this round: the coverage claim missed, and C2 is a learning claim recorded here, not a change to the depth proxy (17/17 rule blocks). Knowledge files 110 → 112 (`git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` at `935c3660` and at `9db24c9e`); both new entries have coverage-map and knowledge-index rows (`corpus/README.md:77-78`, `:171-172`).

Width disclosures: C2's 0 mismatches cover the 10 canonical keys among the 230 selectors (69 entries), not all 36 keys, and none of the 187 held-out selectors is a canonical key, so for them the rule only predicts `false`. The deployed revision behind `api.openchain.xyz` is assumed. C2 was declared after attempt 1 had seen the C1 refusal of h09 and after a disclosed pre-freeze probe over committed round-25 responses (`claims-c2.json` `pre_freeze_probe`); its counted data is only the fetch made after its own freeze (17:22:05Z–17:25:57Z, freeze 17:21:55Z).

R28-C2 relabel after the wave (`.ufo/waves/round-28/a2w/CriticC2PreFreeze.md`, `CriticC2Width.md`; M28-4, M28-5): the counter's target is met, but the test is a re-observation of a rule read from code, not a held-out prediction. 168 of the 230 selectors already had responses in the lane before the freeze (`tools/round-28/preseen-overlap.py`, exit 1). All 59 predicted-true entries come from the 10 round-25 canonical selectors that the pre-freeze probe had scored, and the probe time recorded in the frozen file ("17:24Z") is later than the freeze. The frozen `limits` sentence ("a different deployed list would show up as mismatches") is wrong: the service's first 35-key list also scores 0. The depth verdict is the outside reviewer's call. This card's own reading is `unprovable-but-better`, not `improved`. C2 does not offset the C1 miss, and the round does not meet the every-claim-verifies rule (fleet `AXES.md` admission).

### Round-27 routed defects (hygiene, not claims)

1. Corrections sweep: round-28 pointer appended to `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` (`## Pointer appended in round 28`); QUALITY row 41 supersedes row 37 for `analyze` and `inspect`.
2. Red round-27 C2 selftest: see the wave findings below.
3. Registry rows: see the wave findings below.
4. Pinning: both round-28 freezes list every file their counter loads (`loaded_by_counter` in each claims file), and each counter refuses a pin mismatch with exit 2 (selftest case `red-pin-refusal`).
5. Duplicate-bytes gate: round 27's C1 stays a miss and is not re-scored. The round-28 C1 counter ships the green look-alike case `green-identical-4byte-bodies-across-selectors` in its freeze commit (QUALITY row 40).
6. Gate quotes from rendered HTML: QUALITY row 42. The round-28 Gate quotes are from raw files, not rendered HTML.
7. Clarification of `SCORECARD.md:3125` and `:3130`: "the AXES rule lines are 16-17" (`:3130`) is wrong. Lines 16-17 are this file's own baseline-citation rule ("Line citations to pre-existing lane files refer to the baseline revision unless explicitly marked current"), not AXES lines. "The current planned field is the round-27 one" (`:3125`) and "the current planned field" (`:3130`) both mean the field at `:3128`, which supersedes `:3121`.
8. Mutation tests: see the wave findings below.

### Round-28 wave findings (`a2w`, 36 seats, `.ufo/waves/round-28/a2w/`)

- Recounts: both counters were re-run by executors at `a2673116` (`ExecRecountC1.md`, `ExecRecountC2.md`), and by critics at `9db24c9e` (`CriticRoundHonesty.md`). Independent scripts that share no counter code agree. C1 gives named 137, right 137, wrong 0, no_name 50, using pycryptodome keccak (`ExecIndependentC1.md`). C2 gives 230/246/0/59 (`ExecIndependentC2.md`). The four tally slices re-derive all 187 rows, with 187 agreeing and 0 disagreeing (`ReviewTallySlice1-4.md`). The C2 manifest has 230 of 230 entries with valid sha256, status, URL and utc (`ReviewManifestC2.md`). The flag biconditional holds: 59 true entries and 10 canonical names, 0 exceptions (`ReviewPredictedTrue.md`).
- h09: one placeholder at bytes 97-116, the operand of a `PUSH20`. A scratch copy linked with zero bytes runs and recovers `395c1d44`. This is diagnostic only and never counted (`ExecH09Probe.md`).
- Freeze order holds for both claims. `freeze-gate.py` flags round 28 for pin-schema reasons (ledger row `round-28` in `corpus/claim-freezes.tsv`), and C2 was audited by hand (`ExecFreezeGate.md`).
- Defect 3 (registry): rows for the four round-27 and round-28 counters are appended at the end of `SKILL.md` (`### Round-27/28 measurement registry`, drafted by `ScribeRegistryRows.md`).
- Defect 8 (mutation tests). QUALITY row 40: 1 mutant killed, 3 survived (the green case does not check itself, there is no reused-run case, and the C2 counter has no look-alike case; `MutQualityRow40.md`). Row 39: 3 killed, 2 survived (a prefix match and a case-folded digest compare pass the selftest; `MutQualityRow39.md`). C2 counter: 12 of 16 killed, and the 4 survivors are missing selftest cases (`MutC2Counter.md`). The entry source-row check: 10 of 10 killed (`MutLessonGate.md`). These are coverage findings. The frozen counters are not edited; the cases go to the next counter design.
- Source rows: S084, S085 and S086 admitted by `CriticSourceRows.md`, with grounding notes kept in the lesson Gate. S085's "the signature it keeps for each" covers 31 of 36 keys; 5 `system:magic` keys have none (`SourceCanonicalList.md`, `SourceFilterCode.md`).
- Sibling overlap: the only substantive overlap is in revenger, which the lane cites and does not absorb (`ConnectorSiblings.md`).
- Defect 8, continued. QUALITY row 38: 10 mutants, 4 killed by the selftests and 6 survived. The selftests test the timestamp clauses but have no case for the commit-order clauses. A separate behavioural probe kills all 6 survivors, and on real bytes neither counter refuses anything under row 38 (`MutQualityRow38.md`). `tools/round-27/xpin-attribute.mjs`: 17 mutants, 17 killed. The committed checker `c2-xpin-check.py` does not fail on a non-zero tool exit code; only the receipt's `exit=0` catches that (`MutXpinTool.md`).
- Defect 2 (red round-27 C2 selftest): still open at filing. Seat `ExecR27SelftestFix` returned a fixture diff (`ExecR27SelftestFix.md`) after the hard stop. The diff was not applied or verified in the lane, and the selftest stays red (`ReviewSpotcheckRouting.md`, `FAIL correct-stub`, exit 1 at 18:39Z).

## Round 29 — the round-25 EVM naming rule on fresh published-interface carriers, and openchain's `filtered` flag on never-fetched selectors

Base `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`. Outside decision on round 28 recorded first: `corpus/lessons/round-28-verifier-spotcheck.md` rules round 28 not admitted, `rejected-honest-stop` (R28-C1 60/61), depth `unprovable-but-better` (R28-C2 a re-observation). Both round-29 claims were frozen together at `dbd87cfa09eb89306c4e07d3171a4556eb732024` (`.ufo/waves/round-29/claims.json`), with both counters and their selftests (C1 22 cases, C2 19 cases), the frozen inputs, the producers and the before receipts, before any REA run, lookup or fetch; no pre-freeze probe was made. Inputs were screened before the freeze and the targets sized to the screened sets: hex screen `carriers=16 fail=0` (QUALITY row 43), pre-seen screens `overlap=0` for the C1 list (selectors written anywhere in the lane) and the C2 list (selectors with an openchain response in the lane) (QUALITY row 44; `.ufo/waves/round-29/before/`). Data was collected once, after the freeze, and committed at `4fcea97875a7fe1d816fb871cbc60a1c3632efa0` (16 of 16 REA runs exit 0; 304 of 304 lookups and 178 of 178 fetches HTTP 200 on the first try). Entries, rows and lesson at `18be864a528873b2b70d8c94e31f880290249e90`.

| claim | axis | before (at `bacbe9cc`) | after (at `18be864a`) | counting command | verdict |
|---|---|---|---|---|---|
| R29-C1 round-25 naming rule scored on 16 fresh hex-screened carriers / 152 never-written selectors, plus entry citing S088 | coverage (learning claim; PROVINCE Frontier "EVM bytecode (extended)", the round-27 planned field at `:3128`) | runs_ok 0, rows_complete 0, tally_equal 0, entry_ok 0, exit 2 (frozen lists absent) | runs_ok 16/16, rows_complete 152/152, tally_equal 1, entry_ok 1, exit 0 | `python3 -I -B tools/round-29/c1-fresh-naming.py --root <LANE> --rev <REV>` | target met as measured. Observed triple: named 122, right 122, wrong 0, no name 30 |
| R29-C2 `filtered` rule (S084, S087) on 178 selectors with no prior openchain response, plus entry citing S087 | depth (learning claim) | responses_complete 0/178, entries 0, mismatches 0, predicted_true 0, predicted_false 0, entry_ok 0, exit 2 (pinned inputs absent) | responses_complete 178/178, entries 252, mismatches 0, predicted_true 38, predicted_false 214, entry_ok 1, exit 0 | `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <LANE> --rev <REV>` | target met as measured |

Receipts: `.ufo/waves/round-29/before/c1-at-bacbe9cc.txt`, `c2-at-bacbe9cc.txt`; `.ufo/waves/round-29/after/c1-at-18be864a.txt`, `c2-at-18be864a.txt`, `c1-selftest.txt`, `c2-selftest.txt`. Owned axes rows above are unchanged: the three finite proxies stay saturated at 10, and both claims are learning claims recorded here, not changes to the proxies. Knowledge files 112 → 114 (`git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` at `bacbe9cc` and `18be864a`); both new entries have coverage-map and knowledge-index rows (`corpus/README.md:79-80`, `:175-176`).

Width disclosures: the C1 carriers are compiled stubs holding published function lists, written from the L1's knowledge of the standards (only n04 has a source row, S088), so C1 measures the rule on public names; its no-name rows come from REA inferring `uint256` for `bytes32` (24), `bytes` for `string` (3), and from spam ties (3). C2's 214 predicted-false entries are the c1 set (all non-canonical) and its 38 predicted-true entries come from 19 of the 26 never-fetched canonical keys; the deployed revision behind `api.openchain.xyz` is assumed. After the fetch the L1 found that 6 of the 31 kept canonical signatures do not hash to their key (C2 entry, Rule); that is a reading of the pinned list, not a counter output.

### Round-28 routed defects (hygiene, not claims)

1. Live seat at filing: the seat's final report `.ufo/waves/round-28/a2w/ExecR27SelftestFix.md` (rewritten after the round-28 filing) is committed as evidence in `7431096b`, unedited. A lane check cannot see a seat that writes after the filing (M29-1, corrected after the wave by `CriticMistakes`); the pre-file gate `tools/round-29/prefile-check.sh` checks the tree and both freeze gates with `--disclosures` (QUALITY row 47, M29-4) and is red on clean clones at the round-26, 27 and 28 filing commits (`.ufo/waves/round-29/after/prefile-gate-at-filings.txt`). The live-seat condition is a session check, recorded in the round report.
2. Red round-27 selftest: the seat's scratch patch (sha256 `1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783`, re-verified) applied in `7431096b`; every line outside `selftest()` is byte-identical to the frozen `d8de667f`. Selftest `cases=6 failures=1` exit 1 before (`.ufo/waves/round-29/before/r27-c2-xpin-selftest-unpatched.txt`), `cases=6 failures=0` exit 0 after (`.ufo/waves/round-29/after/r27-c2-xpin-selftest-patched.txt`). Disclosed as INSTRUMENT_REVISED under `instrument_supersessions` in `.ufo/waves/round-27/claims.json` and in the `round-27` ledger row. The round-27 C2 measurement is not re-scored.
3. Hex-screened C1: done before the freeze (above).
4. Real held-out test of the `filtered` rule: R29-C2, with predicted-false and predicted-true unseen entries and the pre-seen screen at exit 0.
5. Freeze gate over every `claims*.json`: `tools/round-29/freeze-gate.py` (also reads `loaded_by_counter` and `producers_not_counters` as pins), ledger `corpus/claim-freezes-v2.tsv`; both gates exit 0 with `--disclosures` at `18be864a` (`.ufo/waves/round-29/after/freeze-gates-v2.txt`). The round-24 ledger's round-26 and round-28 rows disagreed with their gate (M29-2) and are corrected. Round 29 itself is FLAGGED `INSTRUMENT_UNPINNED` by both gates for a script its claim text names without pinning (M29-3).
6. Claim-specific Gate row: both round-29 counters require the claim's own row (`claim_row` S088 and S087) and ship the red case `red-cites-other-new-row` (QUALITY row 45).

### Round-29 wave findings (`w1`, 44 seats, `.ufo/waves/round-29/w1/`)

- Shape: one v1 wave of 44 (executor 15, reviewer 10, critic 7, mutation-tester 5, scout 3, scribe 3, connector 1), validated by `ufo-swarm-wave.mjs run` under policy v1 and dispatched as one task call at 20:20:36Z (`w1-dispatch.json`, exact payload `w1-payload.json`); 43 returned, 1 dead (`CriticAxisFit`: "Cursor OPENAI: Unable to reach the model provider"), not replaced. No residual call.
- Recounts: both counters re-run in clones at `18be864a` (`ExecRecountC1.md`, `ExecRecountC2.md`; tally diff empty). Independent scorers that share no counter code agree: C1 named 122, right 122, wrong 0, no_name 30 (`ExecIndependentC1.md`, pycryptodome keccak); C2 252 entries, 0 mismatches, 38/214 (`ExecIndependentC2.md`). Envelopes 16/16 (`ExecEnvelopeAudit.md`), manifests 304/304 and 178/178 (`ExecManifestC1.md`, `ExecManifestC2.md`), carriers rebuild byte-identical (`ExecRebuildCarriers.md`), freeze order and pins hold and no frozen input changed after the freeze (`ExecFreezeOrder.md`, `CriticTargets.md`), every count in `claims.json` holds (`ReviewClaimsJson.md`).
- Held-out status: C1's 152 selectors are absent from every base blob in four spellings and as raw bytes (`ExecPreseenIndependent.md`), but the names were author-selected and some name strings were in the lane (`token1()` in the canonical-list copy), so C1 is a completeness-targeted score on author-selected public names, not a blind test (`CriticHeldOutC1.md`; entry Limits). C2 is a held-out test, but only `mismatches` tests the rule; 37 entries under 15 keys test the name comparison, the c1 set tests only the "false outside the list" branch (`CriticHeldOutC2.md`; entry corrected).
- Separability: each counter exits 0 with only its own claim's data present (`CriticSeparability.md`); the C2 counter cannot tell its fetch from a copy of C1's byte-identical lookups (entry Limits; fetch logs committed).
- Mis-keyed list: 6 of 31 kept signatures confirmed with two independent keccak implementations; "hides the true name" holds for 4 keys, is inference for `0x8abf6077`, and does not apply to `0x0d0f30c6` (no candidate) (`CriticMisKeyed.md`, `ExecCanonicalHash.md`; entry corrected).
- Source rows: S087 and S088 re-opened, hashes and quotes equal, admitted (`ReopenS087.md`, `ReopenS088.md`; S088's 16 methods equal n04's ABI). Earlier statements the round corrects got appended pointers (round-28 and round-25 entries; S085 teaches cell via the lesson Gate note) (`ScoutCorrectionSites.md`).
- Mutation (coverage findings; frozen counters not edited): C1 counter 4 of 8 killed (survivors: dropping the new-since-base check, TARGET off by one, `<` for `<=` on run time, dropping the tally_equal gate; `MutC1Counter.md`); C2 counter 6 of 7 killed (a case-insensitive name compare survives; `MutC2Counter.md`); v2 gate 3 of 4 killed and it has no selftest (`MutFreezeGateV2.md`); pre-seen screen 3 of 5 killed (`MutPreseen.md`); pre-file check: the untracked-file omission is caught only by an untracked-only probe (`MutPrefile.md`).
- Other: r27 patch selftest-only and measurement-identical (`ExecR27Patch.md`); the supersession append is a legitimate disclosure (`ReviewR27Supersession.md`); ledgers agree with both gates (`ReviewLedger.md`); QUALITY rows 45-47 hold (`ReviewQualityRows.md`); mistakes M29-1 and M29-2 rewritten and M29-4 added after `CriticMistakes.md`; sibling overlap: revenger direct overlap and an unresolved ADJ-06 ownership question, cited not absorbed (`ConnectorSiblings.md`).
- planned: coverage or depth — a blind naming test: interface lists drawn by a rule the L1 does not control (for example verified contracts from a Sourcify repository snapshot listed by address before any lookup), with name strings screened as well as selector tokens; add the missing selftest cases from the round-29 mutation survivors and a selftest for `tools/round-29/freeze-gate.py` before its next use. Second choice: calibration on the 11 SCORECARD statements disclosed in round 26.


## Round 30 — `inspect-rust-binary` positive class on ELF, PE and thin Mach-O, and its refusal signatures predicted from code

Base `d210fb8fa62d2af04d009cfa0c65a4e8137dc742`. Outside decision on round 29 recorded first: `corpus/lessons/round-29-verifier-spotcheck.md` rules round 29 `rejected-honest-stop` for axis misfit (R29-C1 a replication, its target also met by the trivial baseline); depth `improved` (R29-C2). This round is repair-first and leaves the rejected streak's areas (EVM naming, evidence-ID identity). Instruments at `0dbabf78`; both claims frozen at `4ee65c67` (02:35:13Z) with predicates, labels, targets, the 16-carrier list and the 19 predictions; before receipts at `d210fb8f` exit 2 for both (`.ufo/waves/round-30/before/`). Pre-data control wave `w1` (39 seats); 10 control receipts committed at `f39f4530` (`.ufo/waves/round-30/controls/receipts.tsv`), none met a target; `tools/round-30/axis-fit-gate.py` exit 0 before data. Data at `24da3459` (runs 02:59Z–03:01Z).

| claim | axis (surface moved) | before (at `d210fb8f`) | after (at `92b1dd2d`) | counting command | verdict |
|---|---|---|---|---|---|
| R30-C1 `inspect-rust-binary` on the positive class (images with a cargo-auditable `.dep-v0` section), entry citing S089/S091 | coverage — PROVINCE Core gains the verb's positive input class on three containers; unmoved command `git show <REV>:PROVINCE.md \| grep -c inspect-rust-binary` gives 0 at the base | exit 2 (`PIN pinned input absent`); PROVINCE names the verb 0 times; 0 committed envelopes | `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, exit 0 (`.ufo/waves/round-30/after/c1-rust-positive-at-92b1dd2d.txt`); also at `24da3459` | `python3 -I -B tools/round-30/c1-rust-positive.py --root <LANE> --rev <REV>` | target met as measured |
| R30-C2 refusal signatures of the 6.5.0 reader predicted from code (S090), entry and SKILL decision table | depth — SKILL.md gains a decision table of 19 input conditions with exact messages, error codes and thresholds | exit 2 (predictions absent at base); SKILL names the verb 0 times | `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`, exit 0 (`after/c2-rust-refusals-at-92b1dd2d.txt`) | `python3 -I -B tools/round-30/c2-rust-refusals.py --root <LANE> --rev <REV>` | target met as measured at `92b1dd2d`; at `24da3459` the same counter printed `skill_ok=0`, exit 1 (M30-4), before the SKILL lead line named the verb and the entry |

Owned axes rows above are unchanged: the three finite proxies stay at 10; both claims are recorded here. Knowledge files 114 → 116 (recipe A at `92b1dd2d`: mapped 116/116, depth 17/17 rule blocks), both new entries in the coverage map and knowledge index. Selftests: C1 25 cases, C2 16 cases, 0 failures (`after/*-selftest.txt`).

Width disclosures: C1's 16 carriers are one producer's release (uv 0.13.0), 5 distinct package lists and 7 distinct dependency documents, one per wheel (uv, uvx and uvw of one wheel share one; wave-2 `ReDeriveElfX86.md`, `ReviewProvince.md`); the oracle shares the format spec (S089) with REA, not code. C2's mutants are ELF x86_64 only and three message pairs are shared by two mutants each. For refusals, P2's committed-record clause compares only `ok` (M30-3, a fabricated-refusal control scored 16 of 19 committed matches); the live re-run decides. The entry and PROVINCE/SKILL gates are token checks; the Core row and the table were written to be read, and wave 2 reviews them.

### Round-29 routed defects (hygiene, not claims)

1. Axis misfit: mistake M30-1, QUALITY row 48, `tools/round-30/axis-fit-gate.py` (round 29 exit 1; round 30 exit 1 at the freeze, 0 after the control receipts).
2. Target that controls cannot meet: the pre-data control wave; `controls/receipts.tsv`.
3. M29-3: `instrument_supersessions` entry appended to `.ufo/waves/round-29/claims.json` (3 lines, append-only; `w1/ExecM293Disclosure.md`); round 29 stays `FLAGGED INSTRUMENT_UNPINNED` by design. Run-before-freeze as an exit code: `tools/round-30/prefreeze-gate.py` (round 29 exit 1 naming `tools/round-28/c1-heldout-naming.py`; round 30 exit 0).
4. M29-1: `tools/round-30/settle-gate.py` (round 29 exit 1, missing ledger; the real round-28 rewrite caught by hash). Round 30 files its own `settle.tsv`.
5. "Published" carriers: correction appended at PROVINCE.md, the round-29 entry, corpus/README.md, here (below) and LOG.md.
6. SCORECARD:3166: correction below.
7. `c1-fresh-naming.py` docstring: not revised (no round-29 counter revision this round).

- **Correction — round-28 S085 teaches cell (round 30):** At `SCORECARD.md:3166`, the old line says “S085's ‘the signature it keeps for each’ covers 31 of 36 keys; 5 `system:magic` keys have none.” Observation: 31 of 36 keys carry a signature, and 6 of those 31 signatures do not hash to their own key; the five remaining keys are `system:magic` keys with no `signature`. Inference from `31 - 6`: only 25 keys keep their own signature. Evidence: `corpus/lessons/round-29.md:27-42`; `.ufo/waves/round-29/after/canonical-keyhash.txt:2-10`; `.ufo/waves/round-29/w1/ExecCanonicalHash.md:20-48`; `.ufo/waves/round-29/w1/ReopenS087.md:56-63,77-87`; `corpus/lessons/round-29-verifier-spotcheck.md:95-99,127-129`; `corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md:89-95`.
- Correction (R29-C1 carrier provenance, round 30): only carrier n04 rests on an opened source (S088); the other 15 lists were written from the L1's knowledge of the standards and are author-selected names, not opened published interfaces (`SCORECARD.md:3171`, `:3182`).

### Round-30 wave-1 findings (`w1`, 39 seats, `.ufo/waves/round-30/w1/`)

- Shape: one v1 control wave of 39 (scribe 9, mutation-tester 8, critic 7, reviewer 7, executor 4, scout 2, connector 1, sentinel 1), validated under policy v1, dispatched as one task call at 02:41:55Z; 39 returned, 0 dead.
- Controls (none met a target): C1 do-nothing 0/16, junk-row 0/16, all-false 0/16, no-reader 0/16, id-keyed shortcut 1/16; C2 do-nothing, junk-row, generic message, all-accept and rotated messages 0/19, empty predictions PIN exit 2, predictions copied as observations 16/19.
- Predictions traced to code before data: 19 of 19 agree (`RevPredRefuseA.md`, `RevPredRefuseB.md`); predicate sentence equals code clauses except the M30-3 refusal gap (`RevPredicateIdentity.md`); oracle agrees with llvm-readobj on 16/16 (`RevOracleVsReadobj.md`); carrier provenance 16/16 (`RevCarrierProvenance.md`); freeze order holds (`RevFreezeOrder.md`).
- Mutation (findings; frozen counters not edited): C1 judge 14/14 killed, committed clause 9/9, oracle 3/7 (4 invisible on these carriers), C2 judge 7/14 (7 missing selftest cases), builder 7/9 (one byte-identical, one message-only change not pinned by the builder).
- Axis fit before data: C1 fit narrowly (positive extraction is new governed ground, not a new verb; token gates do not prove Core governance), C2 fit (trivial predictors 0–2 of 19) (`CriticAxisFitC1.md`, `CriticAxisFitC2.md`).
- Containment: a seat tool rewrote 4 carriers in place (M30-2, caught by the pin check, restored, `chattr +i`); sentinel mediums on GIT_DIR redirection and record-controlled paths (`SentinelNoExec.md`); runs unset GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE.
- planned: depth or coverage — `inspect-rust-binary` refusal signatures on PE and Mach-O containers (section-table edits) and the 256 MiB/8 MiB bounds, with a counter that compares the full refusal envelope (M30-3) and distinct-branch mutants for the shared-message pairs; second choice: calibration on the lane's SHONEN/SCORECARD pointer set with `axis-fit-gate.py` run before data.


## Round 31 — `inspect-sqlite-database`: database-scope schema on 12 published SQLite files, and 23 refusal/edge outcomes predicted from code

Base `c369242fee9f559f895e3f7956b1242076c7b1be`. Outside decision on round 30 (`corpus/lessons/round-30-verifier-spotcheck.md`): admitted, coverage and depth improved, calibration unchanged; its 8 routed defects are dispositioned in `corpus/lessons/round-31.md`. Anti-loop: leaves REA's Rust reader for its SQLite reader. Instruments, carriers, predictions and claims frozen at `35ba7c52` (04:05Z); before receipts at `c369242f` exit 2 for both (`.ufo/waves/round-31/before/`). Pre-data control wave `w1` (44 seats); control receipts committed at `7474d269`, none met a target; data `f368a101`; docs `0007731e`.

Lowest-axis basis: coverage, depth and calibration are tied at 10 at the base (owned-axes rows above), none retired (`Verdicts, planned, retired`: "retired: none"); on a tie every owned axis is a lowest axis, so both claims satisfy the rule. Recorded in `claims.json` before data (round-30 routed defect 5).

| claim | axis (surface moved) | before (at `c369242f`) | after (at `0007731e`) | counting command | verdict |
|---|---|---|---|---|---|
| R31-C1 `inspect-sqlite-database --schema-scope database` on 12 published files vs an independent reader; entry citing S096 | coverage — PROVINCE Core gains the operation (unmoved: `git show <REV>:PROVINCE.md \| grep -c -E 'inspect[_-]sqlite[_-]database'` gives 0 at the base) | exit 2 (`PIN pinned input absent`); PROVINCE 0 rows; one inventory-scope run in knowledge (l7-04) | `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)`, exit 0 (`.ufo/waves/round-31/after/c1-sqlite-positive-at-0007731e.txt`) | `python3 -I -B tools/round-31/c1-sqlite-positive.py --root <LANE> --rev <REV>` | target met as measured; pre-data axis ruling narrow fit (`w1/CriticAxisFitC1.md`) |
| R31-C2 refusal/edge signatures of the 6.5.0 SQLite reader predicted from code (S092); SKILL decision table | depth — SKILL.md gains a 23-row decision table (unmoved: `git show <REV>:SKILL.md \| grep -c inspect-sqlite-database` gives 0 at the base) | exit 2 (predictions absent) | `requests=23 matches=23 target=23 entry_ok=1 (ok) skill_ok=1 (ok)`, exit 0 (`after/c2-sqlite-refusals-at-0007731e.txt`) | `python3 -I -B tools/round-31/c2-sqlite-refusals.py --root <LANE> --rev <REV>` | target met as measured; pre-data axis ruling fit (`w1/CriticAxisFitC2.md`) |

Correction to R31-C1's frozen surface sentence (M31-1): "a verb the lane has never run or named" is false; `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` holds one path-only inventory run (luna-round-6/7). The PROVINCE zero holds under every spelling; the new ground is the first Core row and the database-scope reading on 12 files.

Owned-axes rows: coverage and depth refreshed to their `c369242f` recount (116/116, 17/17; routed defect 5), scores unchanged at 10; both claims are recorded here. Freeze integrity: `tools/round-31/freeze-integrity.py` CLEAN at `0007731e` (`after/freeze-integrity-at-0007731e.txt`).

Width disclosures: C1's 12 carriers are 12 distinct schemas in 3 families (PROJ, Chinook, GeoPackage), all UTF-8 without WAL; kinds and columns in the oracle come from libsqlite3 (shared upstream with REA, different build), names/declarations/root pages from a pure-Python file parser. C2's mutants derive from one carrier; five messages are shared by 2–3 requests; at 6.7.0 two budget rows would change (static reading).

### Round-31 wave-1 findings (`w1`, 44 seats, `.ufo/waves/round-31/w1/`)

- Shape: one v1 control-and-build wave of 44 (scribe 11, critic 10, mutation-tester 9, reviewer 5, executor 3, revenger 2, scout 2, sentinel 1, connector 1), validated under policy v1, dispatched as one task call at 04:09Z.
- Controls (none met a target): C1 do-nothing 0/12, junk-row 0/12, all-false 0/12, no-reader 0/12, id-rotated shortcut 0/12, Core-placement shortcut `province_ok=0`; C2 do-nothing, junk-row, all-accept and predictions-copied-as-observations 0/23 (round 30's copied-predictions control scored 16/19), id-rotated shortcut 1/23, after-freeze amendment 0/23 (caught only by the new freeze-integrity gate, M31-2).
- Predictions traced to code before data: 13 of 13 `m-*` rows agree (`RevPredTraceB.md`); pointers 21 exact, 14 contain, 1 adjacent, 0 wrong (`ReviewPointers.md`).
- Mutation (findings; frozen counters not edited): C1 judge 8/18 killed, C2 judge 9/24, oracle 8/12 (4 invisible on these carriers).
- Counter limits found: write mode prints the target line without the committed clause (M31-3); post-freeze edits of frozen inputs unseen by the counters and the round-30 prefreeze gate (M31-2); doc gates are substring checks.
- Containment: carriers, mutants and downloads `chattr +i` before dispatch, every pin intact (`SentinelContainment.md`); one seat ran `git commit` in the fleet repo (no commit; M31-7).

## Round 32 — ARM64X native-view coverage; repertoire calibration honest stop

Abbreviated `a2audit/`, `a2residual/`, `a2before/` and `a2after/` evidence paths in this section are relative to `.ufo/waves/round-32/`.

Base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`; inherited freezes `9a73680a` (C1/C2v1), `9d54070b` (C2v2), `f382e3b7` (C2v3). The outside round-31 decision was **admitted** (`corpus/lessons/round-31-verifier-spotcheck.md`); its seven routed defects were handled first. Full predicates/labels remain frozen in `.ufo/waves/round-32/claims.json` (`P1-pass`) and `claims-v3.json` (`P2-match`); the summaries below do not replace them.

Lowest-axis basis: the three owned proxies are tied at 10 at the base, none retired. Existing owned-proxy scores remain **10 → 10**; no new domain-wide fraction or mastery score is invented.

| claim / axis surface | before | after at measured `9ef97f08b655d951650ba5d32f41f1b1cf9653f4` | counting command | verdict / score delta |
|---|---|---|---|---|
| R32-C1 / coverage — ARM64X hybrid PE native-view import/overview enters bounded Core | counter exit 2 (pinned inputs absent); base PROVINCE has only a Frontier reserve. Its `province_ok` is not evaluated by that run | `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)`, exit 0; twelve original envelopes/IDs in the sourced entry; 0 → 1 bounded Core row | `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC JAVA_HOME=/usr/lib/jvm/java-21-openjdk python3 -I -B tools/round-32/c1-arm64x-positive.py --root <LANE> --rev <REV>` | **verifies, narrowly**; coverage surface improved, existing numeric proxy delta 0. Before `.ufo/waves/round-32/a2before/c1-base.txt`; after `a2after/c1-at-9ef97f08.txt` under the same wave root |
| R32-C2 / calibration — four outside-recorded credits versus Capabilities summary | `statements=4 match=1 target=4 reverse_mismatch=0`, exit 1 at base | repaired summary `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0, **but explicit-denial and word-bag controls also attain 4/4** | `python3 -I -B tools/round-32/c2-capability-calibration-v3.py --root <LANE> --rev <REV>` | **falsified measure / honest stop**, no calibration score gain. Before `a2before/c2v3-base.txt`; after `a2after/c2v3-at-9ef97f08.txt`; false accept `.ufo/waves/round-32/controls/c2-negative/receipt.json` landed `411f3a80` |

The C2 summary restoration is supported by reopened historical anchors (`.ufo/waves/round-32/a2residual/FinalSummaryTruth.md`), but its numerical target cannot distinguish truthful descriptions from denial. Round verdict: **rejected-honest-stop**; no exploratory relabel, target rescale, counter amendment, or new capability acquisition.

C1's independent evidence: `.ufo/waves/round-32/a2audit/A2BuildRecheck.md` (12/12 exact rebuild), `A2PEIndependent.md` (372/372 bounded structural comparisons), `.ufo/waves/round-32/a2residual/FinalC1Measure.md` (fresh live counter at product `bb0af56c`, 12/12; own byte/envelope comparison 144/144). The actual width is twelve author-built exported-leaf DLLs on one host/pin. Published hybrids, EC/dual-view recovery, internal functions, runtime behavior and the virtual-size-greater-than-raw case remain Frontier.

### Custody, sources, corrections and residuals

- All ten pre-data controls landed `33393e59` before production `bb0af56c`; C1's first run starts 22 seconds after that controls commit (`.ufo/waves/round-32/a2residual/FinalCustodyOrder.md`). Five C1 controls score 0/12; two C2 shortcuts meet the frozen target, deciding the honest stop.
- Freeze-integrity at the measured revision is CLEAN for all three claim files (8/2/2 pins); both disclosure audits exit 0 with exact ledgers (19/19 and 24/24). The v3 custody audit still flags three historical evidence anchors as unpinned instruments; this is disclosed, not waived or called clean.
- Sources 97 → 100: A 91 → 94, B 5 → 5, C 1 → 1; mined 95 → 97, rejected 2 → 3; malformed 0 → 0. Counting command and immutable revisions are retained in `.ufo/waves/round-32/a2after/source-count-{base,after}.txt`. New S098/S099 mined, S100 scoped rejection; existing rows unchanged. Start/end census exits 0.
- All seven r31 routed defects map to landed repairs (`FinalR31Routing.md`, same residual directory). NoGitguard remains an intentional limit, not a claimed tool-enforced repair. The old 3/23, “not run,” w2 attribution, controls timestamp and unstamped census instant have named corrections.
- Timestamp strict gate at the measured revision exits **1**, with four unexempted planned-deadline occurrences, not future run instants (`.ufo/waves/round-32/a2after/timestamps-strict-at-9ef97f08.txt`). No allowlist or green verdict is claimed. Auxiliary A2Capability17's 2/4 private probe has no per-call UTC, so its order against the control commit is unknown.
- Frozen-gate limits are recorded in the lesson: lexical source doc gates, metadata-only hybrid classification, committer-time ordering proxy, five surviving selftest mutants, and archived secondary gates without separate selftest modes. These are not hidden repairs.
- Shape: one validated v1 audit/control wave of 32 plus one ordinary residual call of 8 reviewer/critic seats. All 40 accepted attempt-2 seats returned; zero dead/cancelled. One residual call was refused 8/8, then the same payload was authorized/retried and accepted. Prior w1 had 36 planned items, only a 12-start count reported in untrusted logs, and no usable reports; all old items remain excluded. Exact model histories, 429 backoffs and statuses are retained in the wave evidence.
- Trends (author assessment): expansion improved for bounded hybrid Core coverage; quality improved for sourced reader evidence and r31 repairs, with conformance limits disclosed; discernment improved for turning the outside r31 disagreement into QUALITY 57 and stopping on C2. Current outside admission/spot-check remains pending.
- planned (only after a new steer): calibration — a prospectively frozen, evidence-backed repertoire assessment that rejects denial, off-topic descriptions and fixture-label shortcuts before data. Do not reuse C2v3's lexical success as admission.

## Round 33 — outside verdict acknowledged before measurement

Base `428315a8f5674b952def862910af6e07a6c2224b`. The outside round-32 decision is **rejected-honest-stop** (`corpus/lessons/round-32-verifier-spotcheck.md:59-84`): bounded native-view coverage improved; calibration remained unprovable because denial and word bags also met C2v3's frozen target; no axis was harmed. This supersedes the round-32 section's pending-outside-decision sentence, not its recorded measurements.

Repair routing is in `corpus/lessons/round-33.md`. C2v3 is excluded as admission evidence. The planned round-33 learning surface is depth: sourced structural CHPE bounds and failure decisions absent from the base's metadata-only classifier, with no hybrid coverage widening. All three owned proxies remain tied at 10, none retired; depth satisfies the lowest-axis obligation. Scores remain unchanged until a measured surface and frozen claim are recorded; no calibration gain is inferred from repairs alone.

### R33-C1 stopped; no measurement substituted

Declared surface: depth, a source-traceable CHPE structural-profile decision table/reader on the already bounded hybrid-PE ground. Planned target: 32 independent fixture rows matched, errors 0 and source/table checks true, under P33-structural-match. The exact unchanged sentence is retained in `.ufo/waves/round-33/claim-stop.json`.

The input-author item received a provider cyber-policy refusal and later automatic model switch. Main confirmed the hold. Its outputs and derivative controls were removed from the lane and are not evidence; the same task is not rebuilt or rerouted. The claim was stopped before freeze: **before/after counts not evaluated**, no admissible fixture manifest and therefore no legal counting command for the missing study. **Verdict unprovable; honest stop.** This is not an exploratory claim or a rescaled source-text/selftest target. Owned scores remain 10→10, delta 0; no calibration gain or new capability row.

Reachable source/repair work is recorded in LOG and `corpus/lessons/round-33.md`: S101/S102 support a technical table and knowledge entry, while timestamp, disk and selectable-freeze selftest fixes retain separate red/green evidence. Source fidelity and isolated instrument selftests are not the original 32-row claim.

- planned (only after a new steer): work another admissible frontier; do not recreate or reroute the held fixture-author item, reuse C2v3, or widen hybrid coverage from metadata alone.

### Final independent evidence, not the original target

Measured `49a6a1c52ccbaad0e747e2e64a8a7e85988ad29a`: isolated selftests 107/36/11 and repair selftests 5/17/3 pass; source-text quality 15/15 after the asymmetric-normalization fix; strict round-33 timestamps exit 0 without exemptions, and the legacy round-32 scope exits 0 only with five exact-line hash-bound allowances. Commands, immutable revision and all streams are `.ufo/waves/round-33/after/main-verification.json`. Source rows 100→102 are curation, not expansion or an axis score. These unlike quantities do not discharge R33-C1: before/after remain not evaluated, target unchanged, verdict unprovable / honest stop, scores 10→10, delta 0.

## Round 34 — prospective GNU ELF version-needs depth

Base `ec3125ad3d130d92f888a4128dfaa2982f36fff7`. Outside round 33 is **rejected-honest-stop** (`corpus/lessons/round-33-verifier-spotcheck.md`): depth unprovable, quality/discernment improved, no harm. R33-C1 stays stopped; the held builder and derivatives and U064N008Hf47eb933 are not inputs. Append-only correction to report:8: SKILL gained 72 lines, not unchanged; PROVINCE was unchanged. The historical parser pin now links to its normalization-only supersession.

One planned claim, **R34-C1 / depth**: source-grounded GNU Verneed/Vernaux decoding and a technical decision table, on the native ELF surface already owned. The three owned numeric proxies are tied at 10, none retired; depth is tied-lowest without a stagnation waiver. No coverage, calibration or repertoire credit is inferred from finite row counts. Existing scores stay 10→10.

P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Target 12: each carrier matches its independently authored canonical record on both schedules, with all exact source/table/document bindings true. Eleven carriers have GNU requirements; the static empty-requirement carrier repeats its empty record without inventing a string table. This is static field interpretation, never loader behavior/authenticity. Counting command: `python3 -I -B tools/round-34/version-needs-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze <freeze-revision> --rev <measured-commit>`. S103/S104 ground the new knowledge entry and SKILL table; S105 is a real retained scoped rejection.

Independent authoring, source opening, profile-development probes and selftests are preparation, not P34 measurements. The twelve production carrier digests exclude the reader's four development binaries. Before any production target run, fresh adversarial seats score the unchanged counter on do-nothing/junk/all-false/no-reader/label-keyed/original-SHA replay controls; those receipts must land first. A target-met shortcut stops the claim; no post-data rule change or exploratory relabel.

### R34-C1 decisive control — honest stop

Frozen claims `54a87a51a865ab931fd355e767303337b05cccf4`; instruments `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0`. The predicate above is unchanged. `w1/CtlLabels` scored a structure-blind adaptive replay: size selects fixed templates, names come from fixed slices, every scalar/association is memorized. Counter hash `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`.

| claim / surface | before at base `ec3125ad` | production after | decisive adversarial score at `54a87a51` | verdict / score delta |
|---|---|---|---|---|
| R34-C1 / depth — sourced GNU version-needs decision table and structural reader | matched 0/12, documents false, exit 1, `reader_absent`; `.ufo/waves/round-34/before/c1-at-base.json` | **not run**; original kill rule stops before production | size/fixed-slice replay matched 12/12, both schedules 12/12, documents true, exit 0; `.ufo/waves/round-34/w1/CtlLabels-files/size-pristine.receipt.json` | **falsified measure / rejected-honest-stop**; owned scores 10→10, delta 0; no capability |

Counting command remains `python3 -I -B tools/round-34/version-needs-counter.py --root <lane> --freeze 54a87a51a865ab931fd355e767303337b05cccf4 --rev <measured-commit>`. Exact exercised control command, source hash and full receipt are bound by `.ufo/waves/round-34/claim-stop.json`; a portable replay supplies `--control-reader <lane>/.ufo/waves/round-34/w1/CtlLabels-files/size_lookup.pristine.py` and `--rev 54a87a51a865ab931fd355e767303337b05cccf4`. This is a counterexample score, never the production reader's score.

Main approved the stop. This is the third straight rejection after r32 text presence and r33 provider hold, now a fixed-offset replay meeting the counter: same “structure versus shape” family as r32. QUALITY 67 and lesson M34-4 route the structure-blind replay before the next counter freeze. No target/counter/predicate change, re-freeze or exploratory relabel is made. Source-supported detail, repairs and independent expected-record audits remain quality work, not a substitute successful claim.

## Round 34, run-6 re-dispatch (2026-10-25) — R34-C2 frozen, six clauses met, stopped on an unregistered class

Base `ec3125ad3d130d92f888a4128dfaa2982f36fff7`; the attempt-1 work and its C1 stop above are inherited through `f432c8e3` and are not rewritten. The run-6 orchestrator re-dispatched round 34 because no closure was written for that report; nothing in this section re-scores or re-opens R34-C1, whose frozen artifacts are byte-identical from `54a87a51` onward and whose production reader and twelve carriers were not executed (`corpus/lessons/round-34.md`, `## Mistakes` M34-5..M34-11; no-run proof `.ufo/waves/round-34/r34b/w1/RevR34C1Untouched.md`).

| claim / surface | before at `ec3125ad` | after at the frozen `c79bbe7b` | counting command | verdict |
|---|---|---|---|---|
| R34-C2 / depth — capability acquisition: a pre-freeze structure-blind shortcut-replay gate built to make QUALITY 67 executable | `GATE_COUNTER_UNEVALUABLE finding=gate_absent`, exit 2; no gate, no configs, no fixtures | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit 0; five controls MISS (max 5 of 6 clauses) | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>` | **falsified measure / honest stop** — five unregistered structure-blind classes reach the green 8/8, so the surface does not force record traversal |

Freeze `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; stop record `.ufo/waves/round-34/r34b/claim-stop.json` (landed `cd75b92e`); receipts `.ufo/waves/round-34/r34b/{before,after,controls}/` (landed `b917ea64`). Decisive counterexample: `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` (sha256 `2e8feaea92ee…`), 8/8 at three seeds without reading a header, a record entry or a `name_off`; four further classes from independent seats reach the same target (payload with names zeroed, value/offset, record signature, transform/digest identity leak). Registering any of them flips the same gate to `REFUSED`, so the refusal mechanism is sound and the registered set was unfaithful to the class it names.

Defect disposition (Landed = repaired or bound by a later commit; Open = disclosed only): **F1** Landed as a documentary pin container (`instruments.json`, CLEAN 26) and **Open** as enforcement — no counted run reads a pin; **F2** Open (three predicate sentences, `predicate-reconciliation.json`); **F3** Open (count is not identity; a count-preserving swap still clears); **F4** Open (gate mutant M3 survives its selftest, and a class relabelled `structural` clears the red case); **F5** Landed (`b917ea64` tracks the receipts); **F6** Open (deterministic seed and digest-named copies allow identity replay); **Y1-Y5, N1-N5** Open, recorded in `.ufo/waves/round-34/r34b/claim-stop-addendum.json` with the validated next-round repairs. `l1_rerun_utc` in the stop record is forward-dated and is superseded by the bound receipt (`w1/CtlMultiset-files/nameset-green-receipt.json`, 07:34:01Z) — Y4.

Record defects, disclosed and routed rather than repaired in frozen bytes: (1) pins were declarative and in a container the lane's own freeze gate rejects (`instruments_missing`, exit 3; enforced container `.ufo/waves/round-34/r34b/instruments.json`); (2) the frozen `predicate_identity` is false — claims/config 31 words `7c6c17f0…` vs counter/receipts 46 words `8340aea5…` (`predicate-reconciliation.json`); (3) dropping classes to the `MIN_SHORTCUTS` floor still prints CLEAN; (4) a shortcut relabelled `structural` prints CLEAN even on the red config; (5) a gate that runs no reader satisfies all six clauses, and `met_target` is never cross-checked with `matched`; (6) `--rev` is an echo and receipts carried no argv. QUALITY 68-74 encode each (seven rows; 68 also carries the pin-container and predicate-identity obligations, 74 the registry-edit check).

| Owned axis | Before → after | Verdict |
|---|---|---|
| coverage | 10 → 10 (map/index only; one knowledge entry added, no domain surface) | unchanged |
| depth | 10 → 10 (no numeric proxy moved; the capability was denied) | unchanged |
| calibration | 10 → 10 (defects disclosed against interest, but no measured self-assessment claim) | unchanged |

Learning trends: expansion **unchanged** (the entry documents an instrument and its stop, not new domain ground); quality **improved** for instrument disclosure and the six routed criteria, with the capability explicitly denied; discernment **improved** for stopping on the round's own counterexample instead of crediting a registry-relative CLEAN. No row enters the **capabilities** table: a capability needs a passing demonstration in the round that enters it, and this round's demonstration failed. The claim table above is the round's record of that stop, not a capability notice, and the owned-axis rows stay at 10.

- **planned (round 35, after a steer):** depth or coverage — the fresh-content replay counter (`w1/CtlMultiset-files/mini-counter-fresh.py`: 8/8 structural, 0/8 for all nine structure-blind classes) plus the forced-payload-perturbation surface demonstrated by `w1/MutShortcutClasses.md`, frozen with the class set asserted against the pinned set, `met_target == (matched == target)`, digest-bound class entries and a reserved positive-control label; the green surface must vary size, order, payload and name vocabulary together, and the class set must include one class per keyable invariant. Second choice: calibration over the six record defects, counted as mismatches against observed repo state.
- **retired:** none. Coverage, depth and calibration stay tied at 10; no axis is saturated by a finite proxy.


## Round 35 — stopped on frozen counter falsification

Base `aa04633a686d49756763b1feed4be6830d5bb479`; claims `plans/round-35-claims.md`; canonical snapshot `2323d197456f1328459d9420aff025cffbcb3e27`.

| claim | axis | before | measured evidence | verdict |
|---|---|---|---|---|
| R35-C1: assimilate jsc2js `.jsc -> source mapping` frontier through S125/S129 | coverage | C1 do-nothing counter fails at base, exit 1; `.ufo/waves/round-35/controls/c1-do-nothing.json` | Not scored on post-freeze data; no source entries/rows admitted. C1 remains unprovable / stopped for this round; do not credit coverage. | unprovable |
| R35-C2: close round-34 D1-D4 record defects | calibration | C2 do-nothing counter fails at base, exit 1; `.ufo/waves/round-35/controls/c2-do-nothing.json` | Frozen counter falsified: D1 couples to C1's SOURCES change; fake census substrings pass; D3 accepts S1060; D4 exact heading/table shape does not fit existing records (`.ufo/waves/round-35/w1/R35CriticClaims.md:9-45`). | unprovable / honest stop |

The counter selftests are mechanism checks only (C1 and C2 each green=0/red=1); they do not rescue a falsified claim. No score delta or capability is claimed; owned proxy scores remain coverage/depth/calibration 10→10. No axes harmed. Round-35 trend verdicts are not inferred from claim counters alone; outside spot-check remains pending. Retired: none.

## Round 36 — fresh start: sasquatch SquashFS recursion to Core; self-assessment drift repaired

Base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`; freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0` (`plans/round-36-claims.md`); controls `6a870b9290e9566468d7d9e6d1b8308daf025b12`. The previous three closures were rejected (r33 unprovable; r34, r35 honest stops); both claims below were scored against do-nothing and skip controls with their frozen counters before any claimed data, all seven controls exit 1 (`.ufo/waves/round-36/controls/`).

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R36-C1 | coverage — `PROVINCE.md` Frontier bullet sasquatch → `## Round-36 additions to Core` | `carriers_matched 0`, every binding false, exit 1 at base (`controls/ctl-c1-0-do-nothing.json`) | `carriers_matched 4`, all five bindings true, `met_target true`, exit 0 (`.ufo/waves/round-36/after/c1-at-ffc81341.json`) | `python3 -I -B tools/round-36/c1-counter.py --root <lane> --rev <REV> --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` | met under the frozen rule; provenance by four independent reproductions; the counter checks receipt integrity, not provenance (QUALITY 78) |
| R36-C2 | calibration — SCORECARD `## Owned axes` / `## Capabilities` rows and SHONEN boxes vs observed repo state | 3 mismatches, exit 1 at base (`controls/ctl-c2-0-do-nothing.json`) | 0 mismatches, `guards_ok`, exit 0 at `d2e46ef5` (before C1's entry existed, `.ufo/waves/round-36/c2/after-at-d2e46ef5.json`) and at `ffc81341` (`.ufo/waves/round-36/after/c2-at-ffc81341.json`) | `python3 -I -B tools/round-36/c2-counter.py --root <lane> --rev <REV> --base cab59f221fe19726b5692bfa4d9a9679e96b8a73` | `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`, `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` | met under the frozen rule; the counter admits shadow-row and decoy shortcuts (QUALITY 77), so the verdict also rests on a stricter non-counter re-derivation in wave 2 |

Owned scores: coverage 10 → 10 (finite map proxy 122/122 → 124/124, two entries added and mapped), depth 10 → 10 (17/17 unchanged), calibration 10 → 10 (proxy saturated; the move is the 3 → 0 mismatch count). Capability row entered: REA SquashFS recursion through sasquatch (LE v4), demonstrated by the C1 receipts. Assimilation: one entry admitted (`2026-10-26-unblob-sasquatch-dependency`, S110/S111 renumbered by document), three refused (`corpus/lessons/round-36.md` `## Gate`). Not claimed: big-endian/AVM SquashFS, vendor-mangled images, 7z fallback.

- **planned (round 37):** coverage — big-endian SquashFS v4 through `sasquatch-v4be` (unblob's `squashfs_v4_be` handler, S108 lines 40-50) on a frozen carrier set with an independent expected record, the C1 counter's successor fixed per QUALITY 77/78 before data (every-occurrence matching, intended-document repair, package-root pin, reproduction as provenance); second choice: the `.jsc` frontier lead recorded in the round-36 lesson.
- **retired:** none. Saturation line and stagnation window unchanged; last capability entry round 36.

## Round 38 — BE SquashFS v4 measured but not promoted (honest stop); self-assessment pointer repaired

Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`; first freeze `e059ca9391642d5b71b6662cabcbdce0d9308719` (`plans/round-38-claims.md`; its bytes are restored at that path in the round's final commit); controls `efd5c47a72a50b3a434783f82268fb4a96e636a1`. Attempt 1 amended the C1 predicate and counter twice after wave-1 seats had scored carriers (`79f69347`, `f1010f67`). Attempt 2 judges both claims by the first-freeze bytes (QUALITY 79; `tools/round-38/freeze-drift.py` exit 1 at `077e212b`, `.ufo/waves/round-38/l1/freeze-drift-077e212b.json`). The v2/v3 counters are not the rule, and their score is reported for information only.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R38-C1 | coverage — PROVINCE Frontier bullet *sasquatch* (big-endian) → Core | `carriers_matched 0`, exit 1 at the freeze (CTL-C1-0 as scored at `efd5c47a`: `git show efd5c47a:.ufo/waves/round-38/controls/ctl-c1-0-do-nothing.json`; the working copy holds attempt 1's v3 re-score) | `carriers_matched 3`, `met_target false`, exit 1. K2 fails on one `unpublished-entry` gap from its symlink that resolves inside the tree, and the Core-row bindings are false (`.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json`; reproduced by `.ufo/waves/round-38/w2/R38W2C1RescoreV1.md`). The v3 counter, which is not the rule, gives 4/4 with the bindings false (`…/c1-v3-at-3b960fe5-NOT-THE-RULE.json`) | first-freeze counter `tools/round-38/c1-counter.py` (sha256 `a7a62b09…`; equal to `git show e059ca93:tools/round-38/c1-counter.py`) `--root <lane> --rev <REV> --freeze e059ca93… --pkg65 <rea-agents 6.5.0 root>` | `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` | **honest stop** — no Core row; BE v4 stays Frontier |
| R38-C2 | calibration — SCORECARD `## Owned axes`/`## Capabilities`, SHONEN boxes, PROVINCE Core/Frontier rows vs observed repo state | 1 mismatch (`evidence/doctor/` unresolved), exit 1 at base (`.ufo/waves/round-38/controls/ctl-c2-0-do-nothing.json`) | 0 mismatches, `guards_ok`, exit 0 at `0fc61133` (`.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`; the final-commit re-measure is named in the report). The pointer now names the same document, `.ufo/waves/round-19/evidence/doctor/` | `python3 -I -B tools/round-38/c2-counter.py --root <lane> --rev <REV> --base 77091b49… --json-out <RECEIPT>` | `0fc6113376a156fddc3ec385386d71c3a4a9f690` | **met by the frozen counter, which is shown non-discriminating.** A stub at the unresolved path also scores 0 (`.ufo/waves/round-38/w2/R38W2C2Controls.md` §3). The claim therefore rests on an independent re-derivation (`.ufo/waves/round-38/w2/R38W2C2Rederive.md`, CONFIRMED) and on `tools/round-38/intended-doc.py` (`bound` at `0fc61133`, `not-bound` for the base and the stub). The closure rules on admission |

Owned scores: coverage 10 → 10 (map proxy 124/124 → 126/126: one measured-not-promoted entry and one assimilated entry, both mapped; no domain surface moved because C1 stopped), depth 10 → 10 (17/17 unchanged), calibration 10 → 10 (proxy saturated; the move is the 1 → 0 mismatch count). No capabilities row enters: the BE v4 run is real but its claim did not verify. Assimilation: `unblob-format-matrix` admitted (staged S122 → S116, staged S106 → S117); `sasquatch-unblob-compatibility-precondition` and `sasquatch-unblob-avm-branch` refused (`corpus/lessons/round-38.md` `## Gate`). Mistakes mined: M38-1..M38-9, among them the post-scoring amendment, controls fixed after the freeze, the existence-only C2 counter, a false admission-time correction, an in-place registry edit, and a tip that did not ship the rule. Each has a fix shown able to fail; QUALITY 79–81 were added.

- **planned (round 39):** coverage — standard BE v4 promotion. The predicate states the symlink behaviour before data (a symlink resolving inside the tree is `unpublished-entry`; an escaping symlink is removed). A fabricated-receipt control (`.ufo/waves/round-38/w1/R38CriticClaimsC1.md` §3) and a "materialise the path" control are scored before the freeze. At the measured revision `freeze-drift.py` must show `ships_freeze_bytes true` with an empty commit list. Second choice: the AVM-BE branch (`bytes_used == mkfs_time`, S112/S114) on a lane-built carrier, or the published AVM image (`.ufo/waves/round-38/w2/R38W2AssimRejects.md` D5).
- **retired:** none. Saturation line and stagnation window unchanged; last capability entry round 36.

## Round 39 — standard BE SquashFS v4 promoted to Core with the symlink rule stated before data; an executable outcome-triage table scored on a freeze-seeded held-out set

Base `a2f64e1da78afcf8cc39287106604dbcc270844c`; freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` (`plans/round-39-claims.md`, every round-39 tool, carrier, oracle and symlink table, the SKILL triage table and its entry, S118–S121, wave-1 evidence); controls `72359309a052284029f8e0331ef211a67fe4b13b`; C2 held-out data `3c07eed7da595b815ce3064dcb12bd5c0788e564`; C1 after-receipts, Core row, entry, README rows and S122 `6fdaf4f162aff156fcef0e52998a5469c64fd6f0`; lesson/QUALITY 82/instrument registry `52b0eb2907c704ed5f184c47b14c723208e5cbbc`. Wave 1: 43 seats, pre-freeze build, recon and attack of the draft (`.ufo/waves/round-39/w1/`). Wave 2: 39 seats attacking the landing after data (`.ufo/waves/round-39/w2/`).

Both claims carry the freeze-integrity rule added this round (routed defect R38-CL4): a score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path, a later restore does not un-block, and a touch makes the counter exit 2 `frozen_path_changed` without reporting `met_target`. Both counters report `frozen_path_changed []` at `6fdaf4f1` and `52b0eb29`; the C1 counter, C2 counter, triage interpreter, held-out generator and claims file are the same blobs at the freeze, both measured revisions and the lane tip (`182308e4`, `bc20933b`, `b5c5379a`, `08869713`, `f6707233`), and the SKILL triage block (marker → next heading, 3084 bytes) is byte-identical at the freeze, `6fdaf4f1` and `52b0eb29`.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R39-C1 | coverage — standard big-endian SquashFS v4 Frontier → Core: `PROVINCE.md` `## Round-39 additions to Core` row naming `squashfs_v4_be`, round-39 frontier note, entry, `corpus/README.md` coverage-map row, S122 | `carriers_matched 0`, `met_target false`, exit 1 at the freeze with the six carriers present and every documentation binding false (`.ufo/waves/round-39/controls/ctl-c1-0-do-nothing.json`; exit reproduced `.ufo/waves/round-39/w2/R39W2C1Rescore.md`); at the base the counter is `unevaluable: carriers.json absent at freeze` (exit 2, `.ufo/waves/round-39/l1/scores/c1-at-base.json`) | `carriers_matched 6`, `target 6`, every binding true, `frozen_path_changed []`, exit 0 (`.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`). Published file counts (5, 3, 4, 4, 10, 8) and gap counts (0, 1, 0, 0, 2, 1); every gap is of kind `unpublished-entry` and sits exactly on an oracle in-tree link; escaping links (K1 1, K5 1, K6 2) publish no path; K6 is xz (compression id 4, 4 xz streams). Reproduced unchanged at `52b0eb29` (`.ufo/waves/round-39/w2/R39W2C1Rescore.md`) | `python3 -I -B tools/round-39/c1-counter.py --root <LANE> --rev <REV> --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>` | `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` | **met under the frozen rule.** Provenance is not counter-testable and does not rest on it: an independent REA 6.5.0 after-run of all six committed carriers reproduces every receipt field (`w2/R39W2C1AxisFit.md` §0), five further per-carrier seats reproduce K1/K2/K3/K4/K6 (`w2/R39W2ReproK1/K2/K3/K4/K6.md`), and K5/K6 rebuild byte-for-byte from their committed source trees (`w2/R39W2K5K6Rebuild.md`); no carrier is left with one run only. The fabricated-receipt limit is disclosed, not laundered: CTL-C1-3 reaches 6/6 carriers and fails only on `frontier_note` (`.ufo/waves/round-39/controls/ctl-c1-3.json`, `expected_exit 0`, `verdict unexpected-exit`) |
| R39-C2 | depth — SKILL `## Queue-drain craft` rule block 18 with the machine-readable triage table after `<!-- sqfs-triage-table v1 -->` (`SKILL.md:316-343`), interpreter `tools/round-39/sqfs-triage.py`, held-out set seeded by the freeze | at the freeze the counter exits 2 `no_manifest_at_rev` (`l1/scores/c2-at-freeze.json`); at the base `SKILL.md` the interpreter exits 2 and labels 0 of 20 development envelopes (`.ufo/waves/round-39/controls/ctl-c2-dev-scores.json`, `CTL-C2-0-base-SKILL`); the best pre-data shortcut table reaches 12/20 (`CTL-C2-6-no-be-no-sr.formatfix`) | `matched 20` of `n 20`, every binding true, `met_target_consistent true`, exit 0 (`.ufo/waves/round-39/l1/scores/c2-at-6fdaf4f1.json`); 10 generator classes × 2, `seed == freeze`, carriers and manifest regenerate byte-identically with no `--run`; reproduced at `52b0eb29` (`w2/R39W2C2Rescore.md`) | `python3 -I -B tools/round-39/c2-counter.py --root <LANE> --rev <REV> --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --json-out <RECEIPT>` | `6fdaf4f162aff156fcef0e52998a5469c64fd6f0` | **met under the frozen rule**, with the discrimination shown thin: 20/20 is unreachable without both the `-be` and `symlink removed` features (16/20 without either, 18/20 without one), the smallest grammar table that also scores 20/20 is 8 rows / 7 non-`*` cells, and no label or class token leaks from the envelopes (`w2/R39W2C2Shortcut.md`). Held-out envelopes H01–H20 re-derive from their own carrier bytes in three independent seats (`w2/R39W2HeldReproA/C/D.md`) |

Owned scores: coverage 10 → 10 (map proxy 126/126 → 128/128: two entries added and both mapped, `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md` and `…-r39-sqfs-outcome-triage.md`; measured with command A at `52b0eb29`, `missing []`, `dangling []`), depth 10 → 10 (rule blocks 17/17 → 18/18 with the new block's citations resolving, craft section `SKILL.md:81-343`; command A at `52b0eb29`), calibration 10 → 10 (no calibration claim this round; the r1 rubric value 9/9 stands, and the move is the finding below). Saturation line and stagnation window unchanged; a perfect finite proxy retires no axis. Capabilities rows entered: **standard big-endian SquashFS v4 recursion** (`squashfs_v4_be`) and **executable SquashFS `extract-firmware` outcome triage**, both demonstrated in this round (rows and pointers in `## Capabilities`). Assimilation: **none adopted** — two AVM candidates deferred with a stated flip (one entry re-grounded on lane receipts against a real AVM image) and two rejected; the quarantine slice stays at 5 rows, byte-identical to round 38 (`corpus/lessons/round-39.md` `### Assimilation`). Mistakes mined: M39-1..M39-8; new criterion QUALITY 82 (root-named negative-existence sweeps) with gate `tools/round-39/absence-sweep.py` (`--selftest` 18 cases). Routed: R38-CL1–CL4 and R36-CL2/CL4/CL6 fixed, R36-CL3 superseded, R36-CL5 open.

### Wave-2 falsification record (after the landing)

Both author verdicts reproduce under the frozen counters and nothing in the scored surfaces was falsified; the defects wave 2 did find are bookkeeping and documentation: the one omission a scorecard can repair is discharged here, and the rest are recorded open. (1) *No axis move was recorded where the lane scores it*: at the landing, `git log a2f64e1d..HEAD -- SCORECARD.md LOG.md` was empty and the coverage row still read 126/126 while the observable was 128/128 (`w2/R39W2C1AxisFit.md` D1) — this section and the `## Owned axes`/`## Capabilities` rows enter that record; the row numbers here are command A's at `52b0eb29`, the same values it gives at `6fdaf4f1`. (2) *Repaired after wave 2:* `PROVINCE.md:157` and the round-38 note at `:376` asserted big-endian SquashFS stays Frontier with no inline round-39 pointer (`w2/R39W2C1AxisFit.md` D2); both now end with a dated round-39 pointer to `## Round-39 additions to Core` (round-39 final commit). (3) *Open (frozen bytes, erratum only):* `tools/round-39/heldout-gen.py`'s `corruption_bad_minor` docstring claims an `s_minor` 5 image matches no v4 handler, while the landed class is measured as handler `squashfs_v4_be` with `extraction_failed` true and gap `extractor-failure`; the recipe and the frozen claims agree with the measurement, so the docstring is the wrong text and may be corrected only at a later freeze (`w2/R39W2C2Shortcut.md` D1). (4) *Repaired / open (minor wording):* the entry's "the same carriers" for the stripped-`PATH` arm now reads K1–K4 (`w2/R39W2C1EntryReview.md` D2); open: and two SOURCES quote anchors are loose — S118's quote spans wrapped lines 53–55 of a docstring closing at 57, and S121's quoted string lives in `debian/rules:17`, not in the row's `unsquashfs.c` URL (`w2/R39W2SrcReopen.md`). (6) *Repaired after wave 2:* S112's used-by now also lists the triage entry that cites it (old → new logged in `corpus/lessons/round-39.md`), and the SKILL registry row for `registry-immutable.sh` states its measured unknown-revision behaviour (`w2/R39W2Census.md`). (7) *Disclosed:* a re-minted fabrication reaches 6/6 carriers on the C1 counter (`w2/R39W2C1Fabricate.md`); provenance rests on six independent re-runs that reproduced every receipt (`w2/R39W2ReproK{1..6}.md`) and on four held-out re-run seats (`w2/R39W2HeldRepro{A,B,C,D}.md`). (5) *Disclosed, not evidence:* the production table scores 20/20 on the 20 development envelopes (`FREEZE-table-informational` in the control file) — that row is the design data, not a control, and carries no evidence; and a table whose last row is all `*` also reaches 20/20 while mis-labelling an out-of-set envelope, so this target cannot yet mean "triage" in general (`w2/R39W2C2Shortcut.md` D2, with the landed table on the safe side).

- **planned (round 40, after a steer):** depth or calibration — make the two disclosures executable rather than documented: (a) a counter clause that binds a C1 receipt to an in-round re-run of its carrier (or a custody chain that a byte-copy cannot satisfy), so a re-minted fabrication cannot reach 6/6; and (b) an out-of-set envelope the triage table must label `unclassified`, so a default-row table cannot reach 20/20. Second choice: coverage on the AVM-BE branch (`bytes_used == mkfs_time`, S112/S114) with the deferred AVM assimilation flip scored on lane receipts against a real AVM image; R36-CL5 remains open.
- **retired:** none. Coverage, depth and calibration stay tied at 10; no axis is saturated by a finite proxy, and the last capability entries are round 39.

## Round 40 — genuine AVM-layout big-endian SquashFS v4 measured but not promoted (counter suffix false negative); SKILL triage table v2 with a domain guard and a scored action reaches 26/26 on a freeze-seeded held-out set

Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`; freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de` (`plans/round-40-claims.md`, every round-40 tool, the four C1 carriers' pins/oracles and the gap rule, SKILL rule block 19 and its entry, S123, the C2 controls, wave-1 evidence); controls `45e89864e967d7501110b529cb8517b26b92c7ef`; C2 held-out data `2d1ac5bcd08f6828dbfdee9054bbeec0ea211b33`; C1 receipts `73c7bf9c73bd7b4891c4e46c93d1d29c287e4541`; landing `42c10a58cb2cae3a4a0122af35a0cf95ac718043` (measured revision); scores `c17565bc772dd296deeaf1699fbe737c6afbea3c`; honest-stop record `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`. Wave 1: 42 seats (`.ufo/waves/round-40/w1/`); wave 2: 38 seats (`.ufo/waves/round-40/w2/`). Every score receipt records its exit code (routed R39-CL6).

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R40-C1 | coverage — genuine AVM-layout BE SquashFS v4 Frontier → Core (PROVINCE row, frontier note, entry `2026-10-26-r40-avm-be-squashfs-core`, README map row, S124–S126) | at the freeze `carriers_matched 0`, exit 1, every documentation binding false, carrier preconditions true (`.ufo/waves/round-40/controls/c1/ctl-c1-0-do-nothing.full.json`) | `carriers_matched 3` of 4, exit 1: V1, V2, L1 match every clause incl. the rerun projection; L2 fails only `nonregular_unpublished_ok` (path-suffix false positive `usr/bin/busy` vs symlink `bin/busy`); `c1-extra.py` met, exit 0 (`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`, `c1-extra-at-42c10a58.json`) | `python3 -I -B tools/round-40/c1-counter.py --root <LANE> --rev <REV> --freeze 7fce3086… --pkg65 <rea-agents 6.5.0> --carrier-cache <CACHE> --json-out <OUT>` and `tools/round-40/c1-extra.py … --base fa6a8a3f…` | `42c10a58` | **not met — honest stop**; the target was unsatisfiable under the frozen counter with the frozen L2 (`.ufo/waves/round-40/w2/R40W2C1Fabricate.md` Defect B); Core row demoted at `4d62ee5a` |
| R40-C2 | depth — SKILL `## Queue-drain craft` rule block 19 (`<!-- sqfs-triage-table v2 -->`, `SKILL.md:348-375`), interpreter `tools/round-40/sqfs-triage-v2.py`, held-out set seeded by the freeze | at the freeze exit 2 `no_manifest_at_rev` (`.ufo/waves/round-40/controls/c2-counter-at-freeze.json`); base SKILL has no v2 table (CTL-C2-0 exit 2); best control 24/26, v1 transcribed 18/26 on dev envelopes (`controls/c2-dev-scores.json`) | `matched 26` of `n 26`, every binding true, `distinct_decisions 12`, exit 0 (`.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`) | `python3 -I -B tools/round-40/c2-counter.py --root <LANE> --rev <REV> --freeze 7fce3086… --json-out <OUT>` | `42c10a58` | **met**; increment bounded: 18/26 envelopes were already decided by v1 and the expected labels come from the generator's class map (`.ufo/waves/round-40/w2/R40W2C2AxisFit.md`) |

Owned scores: coverage 10 → 10 (map proxy 128/128 → 130/130; command A at `4d62ee5a`); depth 10 → 10 (rule blocks 18/18 → 19/19, citations resolving; command A at `4d62ee5a`); calibration 10 → 10 (no calibration claim; the honest-stop demotion keeps PROVINCE from asserting a Core row the counter did not admit). Saturation line and stagnation window unchanged; a perfect finite proxy retires no axis. Capability row entered: **executable SquashFS `extract-firmware` outcome triage v2 (label and action)**. No capability row for AVM-BE recursion: R40-C1 stopped.

### Wave-2 falsification record (after the landing)

Neither author verdict was overturned: C1 3/4 reproduces with zero divergence (`w2/R40W2C1Rescore.md`), every receipt reproduces from an independent REA run (`w2/R40W2ReproV1.md`, `ReproV2.md`, `ReproL.md`), the oracle holds on all four carriers (`w2/R40W2C1Oracle.md`: 718/718 files, 352/352 symlinks), and a sandbox counter with exact extract-root matching scores 4/4 on the same receipts (`w2/R40W2C1Refreeze.md`). C2 26/26 reproduces, regenerates byte-identically, re-runs and labels identically under an independent evaluator (`w2/R40W2C2Rescore.md`, `RegenA.md`, `RegenB.md`, `IndepEval.md`). Defects found and their state: the rerun binding admits an oracle-only fabrication on L1 (R39-CL5 only partly closed, routed R40-CL2); seven AVM package/download-page texts were committed in the freeze (removed from the tree in this round's last commit, `.ufo/waves/round-40/w1/vendor-files-removed.sha256`); C2 freeze-integrity gaps for the writer path and restore-after-touch (R40-CL3); table-v2 cause/action prose (R40-CL5). Full list: `corpus/lessons/round-40.md` `## Routed defects into round 41`.

- **planned (round 41, after a steer):** coverage — re-freeze the R40-C1 counter with exact extract-root path matching and both-direction selftest cases (R40-CL1), keep the four round-40 carriers and receipts as data, and score AVM-BE Frontier → Core; bind `member_sha256` in `fetch-vendor.py` (R40-CL6). Second choice: depth — table v3 repairing R40-CL5 with a held-out class whose expected answer is not derivable from the generator's class map alone (e.g. combined gap sets). R36-CL5 and R40-CL2 remain open.
- **retired:** none.

## Round 41 — genuine AVM-layout BE SquashFS v4 promoted to Core on four fresh carriers with an exact-path counter; triage table v3 matches its independent evaluator 52/52 but stops on a declared-tuple key mismatch

Base `49096c7e6f226af0c750c4b003be58883cb6049f`; freeze `d764389e9cbe61b9d1b07538ff3bff02d50bb34f` (`plans/round-41-claims.md`, `tools/round-41/*`, C1 carriers/oracles/gap rule, SKILL rule block 20 and its entry, C2 control tables and dev set, wave-1 evidence); controls `9a8fb26001307bc2159934ed53c5fc43e5c8d615`; C1 receipts `5ca6941b061591748c6755c1dcfc188941fcbd35` (+ V4 `after.json` at `e9a24d07`); C2 held-out `8a1f4c73057405a4b470af11d1d351a0f03f6c34`; C1 landing documents `042b87697e7d94e9fc2d3cbcf03541bfd5c03b98`; measured revision `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`; scores `bf5286c9832142a2ceabe2076883dfa2a8e99356`; assimilation `e1c83313f33a3d97edbd8fef402db2d06172fcdc`. Wave 1: 41 seats (`.ufo/waves/round-41/w1/`); wave 2: 33 seats (`.ufo/waves/round-41/w2/`).

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R41-C1 | coverage — genuine AVM-layout BE SquashFS v4 Frontier → Core (PROVINCE `## Round-41 additions to Core`, frontier note, entry `2026-10-26-r41-avm-be-squashfs-core`, README rows, S127/S128) | at the freeze `carriers_matched 0`, exit 1, every carrier precondition true and every documentation binding false (`.ufo/waves/round-41/controls/c1/ctl-c1-0-do-nothing.json`); the round-40 receipts copied to the round-41 paths 0/4 (`ctl-c1-1-relabel-r40.json`) | `carriers_matched 4` of 4, every binding true, `frozen_path_changed []`, exit 0, with a counter-time REA rerun (`.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json`); `c1-extra.py` met, exit 0 | `python3 -I -B tools/round-41/c1-counter.py --root <LANE> --rev <REV> --freeze d764389e… --pkg65 <rea-agents 6.5.0> --carrier-cache <CACHE> --json-out <OUT>` + `c1-extra.py … --base 49096c7e…` | `e9a24d07` | **met** (at `042b8769` 3/4: V4 `after.json` not yet committed, M41-3) |
| R41-C2 | depth — SKILL rule block 20 (`<!-- sqfs-triage-table v3 -->`, `SKILL.md:387-449`), interpreter `tools/round-41/sqfs-triage-v3.py`, evaluator `tools/round-41/indep-eval-v3.py`, held-out seeded by the freeze | exit 2 `no_manifest_at_rev` at the freeze (`.ufo/waves/round-41/controls/c2-counter-at-freeze.json`); base SKILL exit 2; dev controls 0, 4, 34, 2, 38, 31, 42, 44 of 52 vs SKILL 52 (`controls/c2/dev-scores-prefreeze.json`) | `matched 52` of 52 vs the evaluator, `distinct_decisions 13`, real-receipt binding true, `observed_features_match_declared` false (combos' tuples under manifest key `declared`, not read by the counter), exit 1 (`.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`) | `python3 -I -B tools/round-41/c2-counter.py --root <LANE> --rev <REV> --freeze d764389e… --json-out <OUT>` | `e9a24d07` | **not met — honest stop** (M41-1) |

Owned scores: coverage 10 → 10 (map proxy 130/130 → 133/133; command A at `e1c83313`); depth 10 → 10 (rule blocks 19/19 → 20/20 with citations resolving; command A at `e1c83313`; the depth claim itself stopped, so no depth improvement is claimed); calibration 10 → 10 (no calibration claim; stale SKILL ranges in SHONEN and the depth row repaired in this landing). Saturation line and stagnation window unchanged; a perfect finite proxy retires no axis. Capability row entered: **genuine AVM-layout big-endian SquashFS v4 recursion**. No capability row for triage v3 (R41-C2 stopped).

- **planned (round 42, after a steer):** depth — refreeze R41-C2 with one declared-tuple key shared by generator and counter and a frozen-counter dry run on the dev arm (QUALITY 84), keep the v3 table bytes, and widen the combo family until a named-class lookup cannot reach the target on held-out combos (`w2/R41W2C2Combos.md`: CTL-C2-7 8/12 on combos). Second choice: calibration — the 18 host-local SOURCES rows (R41-CL3). R36-CL5, R40-CL2 remain open.
- **retired:** none.

## Round 42 — SquashFS v3 promoted to Core on four published LZMA rootfs images; triage table v4 matches its evaluator 78/78 but stops on one combo's declared gap set

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`; freeze `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` (`plans/round-42-claims.md`); controls `b024051c`; data `d5e22b51`; C1 landing and measured revision `eb8215ac87860f0e52745a4f842485bf8a6fe3b8`; scores `d4b4b4fb`. Wave 1: 43 seats (`.ufo/waves/round-42/w1/`). Lesson `corpus/lessons/round-42.md`.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R42-C1 | coverage — SquashFS v3 (`squashfs_v3`, `squashfs_v3_ddwrt`) Frontier → Core: PROVINCE `## Round-42 additions to Core`, entry `2026-10-26-r42-squashfs-v3-core`, README rows, S131–S134 | `carriers_matched 0`, exit 1 at the freeze (CTL-C1-0); round-41 receipts relabelled 0/4 (CTL-C1-1) | `carriers_matched 4`, every binding true, `frozen_path_changed []`, exit 0 with a counter-time REA rerun (`.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json`, `counter_sha256 0f5052f9…`) | `python3 -I -B tools/round-42/c1-counter.py --root <LANE> --rev <REV> --freeze d1681696… --pkg65 <rea-agents 6.5.0> --carrier-cache <CACHE> --work <S> --json-out <OUT>` | `eb8215ac` | **met** |
| R42-C2 | depth — SKILL rule block 21 (`<!-- sqfs-triage-table v4 -->`, 13 columns, 15 rules), interpreter `tools/round-42/sqfs-triage-v4.py`, evaluator `tools/round-42/indep-eval-v4.py` | exit 2 `no_manifest_at_rev` at the freeze; base SKILL and the v3 table under the v4 marker 0/78 on the dev arm | `matched 78` of 78, `combo_unseen_majority` 19/24, but `observed_features_match_declared` false (combo C02 declared gap set lacks `depth-limited`), exit 1 (`l1/scores/c2-at-eb8215ac.json`) | `python3 -I -B tools/round-42/c2-counter.py --root <LANE> --rev <REV> --freeze d1681696… --json-out <OUT>` | `eb8215ac` | **not met — honest stop** |

Owned scores: coverage 10 → 10 (map proxy 133/133 → 135/135, command A at `d4b4b4fb`); depth 10 → 10 (rule blocks 20 → 21; the block-21 citation was added after scoring so command A resolves 21/21 — measured in the report; the depth claim itself stopped, so no depth improvement is claimed); calibration 10 → 10 (no calibration claim). Capability row entered: **SquashFS v3 recursion through REA (`squashfs_v3`, `squashfs_v3_ddwrt`, LZMA bodies, both byte orders) with a non-sasquatch LZMA oracle (backhand-cli v3_lzma + 7-Zip)**, demonstrated by the C1 receipts. No capability row for triage v4 (R42-C2 stopped).

### Capability addition (demonstrated before this row)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| SquashFS v3 recursion through REA | extract published SquashFS 3.0 LZMA rootfs images (`squashfs_v3`, `squashfs_v3_ddwrt`, LE and BE) through REA `extract-firmware`, with the extractor command logged and an oracle from two readers that are not sasquatch | `.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json`; `corpus/evidence/round-42/c1/` | 42 |
| Freeze-seeded observed-tuple refusal | Build a fresh 27×2 + 24-combo held-out set, measure each carrier's six-field tuple from its REA envelope, refuse to write the manifest on any mismatch, and retain per-carrier verdicts | `tools/round-43/heldout-gen-v4r43.py` selftest 17/17; `tools/round-43/c1-counter.py` at `77d196c6` | 43 |

## Round 43 — held-out tuple refusal calibrated and scored 78/78; C2 source-copy landing is green but the frozen score tool stops on an overstrict registry-line count

Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`; freeze `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`; C2 controls `681360e6`; C2 landing `09ab56b8`; held-out data and measured revision `77d196c6`; C1/C2 score receipts `.ufo/waves/round-43/l1/scores/`. Wave 1: 32 seats, all settled; wave 2: 32 seats dispatched and pending final settlement.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R43-C1 | calibration — generator honesty for the existing SKILL rule block 21 / v4 table; QUALITY 85 / R42-CL1 | at the freeze counter exits 2 `no_manifest_at_rev`; round-42 C02 had `observed_features_match_declared` false | 78/78 matched, every C1 binding true, `observed_features_match_declared` true, `generator.tuple_check` 78/78 all equal (effective n=76; H25/H26 OOD tuples disclosed), `combo_unseen_majority` 21/24, exit 0 | `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze f3f8db38… --json-out <OUT>` | `77d196c6` | **met** |
| R43-C2 | coverage — 18 host-local SOURCES paths resolved by the map and 17 in-lane copies (S126 preserved) | at the freeze gate exit 1, `rows_failed` 18 | gate exit 0, `rows_checked 19`, `rows_total 137`, copy audit 136 checks / 0 failures; the frozen `c2-score-r43.py` nevertheless exits 1 solely because it expected `SOURCES.md` `numstat` to be 3 insertions while the actual diff is 4 insertions / 0 deletions (three S135–S137 rows plus a blank separator) | `python3 -I -B tools/round-43/c2-score-r43.py --root <LANE> --rev <REV> --freeze f3f8db38… --scratch <S> --upstream-dir <GO-TREES> --tarball-67 <T67> --tarball-65 <T65> --json-out <OUT>` | `77d196c6` | **not met — frozen counter false-negative on raw numstat** |

Owned scores remain saturated: coverage `10 → 10` (R43-C2 not met under the frozen scorer; the actual gate/linter evidence is retained but does not override the target), depth `10 → 10` (no depth claim), calibration `10 → 10` (R43-C1 met; numerical score cannot rise above 10). New capability: **a freeze-seeded held-out generator that records each run's declared/observed tuples and refuses to write the manifest on any mismatch**, first-working round 43 (`tools/round-43/heldout-gen-v4r43.py`, C1 score receipt). No C2 capability row is credited until its score instrument is corrected and the frozen target is met.

- **planned (round 43, after a steer):** depth — refreeze R42-C2 with the generator refusing any manifest whose declared tuple differs from its own observed run (QUALITY 85, R42-CL1), table v4 bytes kept; and a wave 2 that attacks the round-42 C1 landing (R42-CL2). Second choice: land R41-CL3's prepared in-lane copies (`w1/R42LocalSrc.md`). R40-CL2 remains open.
- **retired:** none.

### Round-43 closure corrections (append-only)

- **C2 verdict wording:** the frozen scorer is not overstrict relative to its frozen plan. Both require `git diff --numstat BASE..REV -- corpus/SOURCES.md` to equal `3\t0`; the committed append is `4\t0` (S135–S137 plus one blank separator). The scorer correctly exits 1, so R43-C2 is not met; no frozen counter or target was changed.
- **Coverage-map proxy:** after the R43 scored-entry coverage-map row lands, re-run command A at the recorded final lane commit. Keep the proxy distinct from R43-C2: a complete knowledge index does not turn the host-local-source claim green.
- **C1 limits from wave 2:** the C1 receipt meets the frozen target, but it does not bind S135 row content; `run.json` is not an out-of-band REA provenance record, a self-consistent authored envelope can score green, and manifest-supplied carrier IDs need path validation. These are routed instrument limitations, not post-freeze amendments.
- **C2 limits from wave 2:** although the gate and 136-check audit are green on the committed pack, the scorer stops on the frozen 3-vs-4 insertion mismatch. The linter also accepts a parent-directory symlink and an escaping `copy` path under tested controls; source/tarball input pins are not retained by the score receipt. No C2 green or capability is credited.
- **planned (round 44, after steer):** re-evaluate the lowest owned axis under the next prompt; do not reuse or alter the frozen R43 predicates. Carry the C2 target mismatch and C1/C2 instrument findings as explicit candidate fixes.
- **Command A, final indexed tree:** at `8de80f1daec68260eb256eb68375e2c33af759a9`, the frozen command-A recipe prints `knowledge_files=137`, `mapped=137`, `missing=[]`, `dangling=[]`, `coverage_score=10.0`, `citation_resolved_rules=21/21`, `depth_score=10.0`. Base `6b9e64fe` was 135/135. The proxy is unchanged at saturation; it does not override the unmet R43-C2 score.
- **Text erratum:** the Round 43 heading's “overstrict” wording is superseded by the correction above: counter and plan agree on 3 insertions; the committed delta is 4 because of the blank separator. The `planned (round 43)` line is historical; the explicit round-44 planned item above is current.

- **Round-44 calibration correction (2026-10-28):** the `## Owned axes` current observables are re-derived from the round-44 freeze tree: command A reports 137/137 knowledge files mapped (`missing []`, `dangling []`), 21/21 rule blocks with resolvable file/range citations, and the `## Queue-drain craft` section spans `SKILL.md:81-543`. The round-41 pins quoted above (`e1c83313`, `52b0eb29`) remain true at their own revisions.
<!-- c2-correction: C2-a1-owned-coverage-count -->
c2-correction-value: 137/137
<!-- c2-correction: C2-a2-owned-depth-count -->
c2-correction-value: 21/21
<!-- c2-correction: C2-a4-owned-depth-craft-range -->
c2-correction-value: 81-543

## Round 45 — the freeze rule becomes an instrument with four red arms; the registry names the six claim-carrying instruments

Base `149133d47aa7e90796f96047afe6d251a3e65b2c`; freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`
(`plans/round-45-claims.md` + `tools/round-45/` as a directory pathspec); landing
`e715263cb51b713c342ab992d527fe9d61d6f8ff`; amendment A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`
(block 22 cites `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`, because
command A counts only `corpus/knowledge/` references and without one the new block would have
scored the depth proxy 21/22 — the round measured that and repaired it before claiming);
measured revision `1f4b27f8`. Wave 1: 40 seats; wave 2: 36 seats (counts from
`.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`).

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R45-C1 | depth — `SKILL.md` `## Queue-drain craft` rule block 22 (`<!-- freeze-integrity-table v1 -->`, 10 rows, interpreter `tools/round-45/frozen-path-preflight.py` with arms commit/restored/blob/dirty/pathspec) | at the freeze exit 1: `rule_blocks 21 != 22`, `block22_present 0`, `block22_rows 0`, `block22_refs 0` (`.ufo/waves/round-45/controls/ctl-c1-0-do-nothing.json`) | `rule_blocks 22`, `block22_present 1`, `block22_rows 10`, `block22_refs 7`, `block22_unresolved_citations []`, `block22_cites {S140, interpreter} true`, `preflight_selftest cases 11 failures 0`, `frozen_path_changed []`, `met_target true`, exit 0 (`.ufo/waves/round-45/l1/scores/c1-at-1f4b27f8.json`) | `python3 -I -B tools/round-45/c1-counter.py --root <LANE> --freeze f762b727 --rev <REV> --json-out <OUT>` | `1f4b27f8` | **met** |
| R45-C2 | calibration — `SKILL.md` instrument registry vs the six instruments the round-44 and round-45 frozen claim files name (`tools/round-45/registry-scope.json`) | at the freeze exit 1 with `unregistered` = all six paths, `registered []`, `scope_size 6` (`.ufo/waves/round-45/controls/ctl-c2-0-do-nothing.json`); at the base exit 2 `scope file absent at rev` (`.ufo/waves/round-45/controls/ctl-c2-0-base-unevaluable.json`) | `registered` = all six, `unregistered []`, `thin []`, `scope_size 6`, `frozen_path_changed []`, `met_target true`, exit 0 (`.ufo/waves/round-45/l1/scores/c2-at-1f4b27f8.json`); the four r44/r45 counters' exit maps were read from source by one seat each | `python3 -I -B tools/round-45/c2-counter.py --root <LANE> --freeze f762b727 --rev <REV> --json-out <OUT>` | `1f4b27f8` | **met** |

Owned scores: coverage `10 → 10` (command A at `1f4b27f8`: `knowledge_files=138`, `mapped=138`,
`missing []`, `dangling []`, `coverage_score 10.0`; this round adds no domain surface — the two
new source rows document an instrument, not a reverse-engineering surface); depth `10 → 10`
(rule blocks `21 → 22` with `citation_resolved_rules 22/22`, `depth_score 10.0`; the move is the
block and its red-case instrument, not a number above the ceiling); calibration `10 → 10`
(unregistered `6 → 0`, thin `0`; the numeric axis cannot rise above 10).

Learning trends: expansion **unchanged** (no new domain ground; S140/S141 are instrument
documentation and the round adds no knowledge entry); quality **improved on the artefact only**
(rule block 22's ten-row table and its interpreter are red on real history — the `c86ea508`
sweep, eight paths — and green on this round's frozen range, with an 11-case selftest; the
wave-2 distiller struck the earlier wording's registry credit (that is calibration) and its
"depth proxy held" clause (a hold, not an improvement)); discernment **improved** (wave 1
attacked both measures before data and found the discrimination defects and the merge-blindness;
the record was corrected from seat measurements three times — A1's proxy harm, A2's quote/`W04`
counts, wave 2's refs/size/l0 sentences — and the round mined the counterexample to its own
control set as M45-3; R44-CL10 is only partly closed and is stated as such).
No capability row enters: the four-arm gate is an instrument cited by R45-C1, not a
reverse-engineering capability, and this round demonstrates no new domain ground.

**Freeze-integrity disclosure.** Both round-45 counters enforce the freeze by commit history, so a
later restore cannot un-block them by construction; only the preflight carries an explicit
`red-restored` test case. The counters hard-code their frozen set
(`plans/round-45-claims.md`, `tools/round-45`) and it happens to equal the claim's `## Frozen paths`
— derivation from the claim file is routed (R45-CL6). Appending this section to `SCORECARD.md`
also adds that path to the round-44 counters' `frozen_path_changed` list at any post-round-45 tip:
round 44's rubric binds a file every round must edit, which is a limit of that rubric, not an
edit of this round's claims.

- **planned (round 46):** calibration or depth from the routed list — (a) make the counters derive
  their frozen set from the claim file's `## Frozen paths` and add a restore case to each counter
  selftest (R45-CL6, R45-CL7); (b) widen the registry scope to the rounds 41–43 instruments with a
  committed census (R45-CL3) and bind `tool_present_at_rev` (R45-CL2). Second choice: coverage —
  resume the SquashFS v1/v2 promotion with a single, mutually consistent provenance clause
  (R44-CL2). R36-CL5, R40-CL2, R41-CL3 remain open.
- **retired:** none. Coverage, depth and calibration stay tied at 10; no finite proxy saturates an
  axis, and the last capability entries are rounds 42–43.

**Amendment A2 and final measurement (append-only).** A2 `fedd11bf5ff9fe42d061169f78d77df59af4eca1`
corrects the lesson's S141 quote word count (23 → 20) and its round-end `W04` count (16 → 14, the
measured value), routes the wave-1 instrument findings as R45-CL6..R45-CL12, and states in block 22
that the gate's commit arm uses the plain tab-separated `--name-status` form, that its exit column is
the gate's (a scorer reports the same condition as `2`), that a directory freeze reports a subtree
oid in `blob_changed`, and that an invocation must name both frozen pathspecs. Re-measured at A2:
R45-C1 exit 0, `rule_blocks 22`, `block22_rows 10`, `block22_refs 8`, `block22_unresolved_citations []`,
`met_target true` (`.ufo/waves/round-45/l1/scores/c1-at-A2.json`); R45-C2 exit 0, `registered` all six,
`unregistered []`, `thin []` (`…/c2-at-A2.json`). The gate over both frozen pathspecs from the freeze to
A2 is `clean`, exit 0 (`…/l1/preflight-round45-frozen-both.json`). The measured revision for the round
is therefore A2; `1f4b27f8` is the first met measurement, and `rule_blocks`, `rows`, `unresolved`
and `met_target` are identical at both (`block22_refs` grew 6 → 8 as citations were added).

**Amendment A3 and the final measured revision (append-only).** A3 `f59565b782c18b0eb691bec12f52d2f80d9f5032`
corrects the `tools/round-44/c1-run.sh` registry row (the script does not run the oracle, and
`--dry-run` exits 0 without writing), states in block 22 that the preflight's red cases are
arm-covering but not arm-isolating and that `--dirty-pathspec` replaces the dirty arm's scope
(a false-clean, routed), and routes R45-CL15/CL16. Re-measured at A3: R45-C1 exit 0, `rule_blocks 22`,
`block22_rows 10`, `block22_refs 8`, `unresolved []`, `met_target true`
(`.ufo/waves/round-45/l1/scores/c1-at-A3.json`); R45-C2 exit 0, `unregistered []`, `thin []`,
`met_target true` (`…/c2-at-A3.json`). **The measured revision for the round is A3**; `rule_blocks`, `rows`, `unresolved` and
`met_target` are identical at `e715263c`, `1f4b27f8`, `fedd11bf` and A3, while `block22_refs` reads
6 / 7 / 8 / 8 as citations were added (wave-2 `R45W2Immutable` R-1 caught the earlier "the values are
identical" sentence; corrected here), and both counters are shown non-discriminating by wave 1
(R45-CL13/C14) — the verdicts are `met (instrument non-discriminating)`.

## Round 46 — the freeze-integrity matrix and its discriminating counter; the registry names the 38-instrument census

Base `5382acc85f9d8617fe242fc116819b8055dfc4c7`. Frozen claims `plans/round-46-claims.md` +
`tools/round-46/` first landed at `31820472784284727546808acc31b3ea1e73919b` and were corrected at
`50862e4a`, `65678df0` and `0425224756791b414454df28a9abf93dcdf154ce` — the **declared freeze is
`0425224`**, and the four-commit series is a recorded defect (M46-3), not a single commit as the
plan defines it. Landings: block 23 `227d6982`, A1 `87578656`, A2 `6e018068`, A3 `7bf33e31`;
registry section `781e19ae`; measurements `1e32827b`. Waves: 40 + 40 = 80 seats.

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R46-C1 | depth — `SKILL.md` `## Queue-drain craft` rule block 23, the freeze-integrity discrimination matrix (13 rows, one per routed v1 defect, `trigger` naming the id, `v2 arm` naming the check, exit in {0,1,2}), 9 line-selected citations, the interpreter's sha256 pin, and the nine-mutation battery | at the freeze exit 1: `marker_occurrences 0`, `block_present 0`, `rows 0`, `rule_blocks 22` (`.ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json`); the round-45 clause set accepts all nine forgeries (`v1_green 9`) | exit 0, `rule_blocks 23`, `rows 13`, `refs 9`, `unresolved_citations []`, `pin` equal to the bytes at rev, battery `forgeries_total 9 / v1_green 9 / v2_green 0 / genuine_green 1`, `met_target true` (`.ufo/waves/round-46/l1/scores/c1-at-F4.json`) | `python3 -I -B tools/round-46/attest.py --root . --freeze 0425224 --rev 0425224` | `0425224` | met |
| R46-C2 | calibration — the marker-bound `<!-- instrument-registry v2 -->` section over the 38-path census `tools/round-46/census.json`, exact cell-0 equality, verdict maps binding 0/1/2, presence at the revision, and the seven-mutation battery | at the freeze the round-45 counter covers 6 of the 38 census instruments (`registered` six, `scope_size 6`; `.ufo/waves/round-46/controls/ctl-c2-1-v1-scope.json`); the v1 clause set accepts all seven forgery classes | exit 0, `scope_size 38`, `registry_rows 38`, `registered` 38, `unregistered []`, `thin []`, `absent_at_rev []`, battery `7 / 7 / 0 / 1`, `met_target true` (`.ufo/waves/round-46/l1/scores/c2-at-F4.json`) | `python3 -I -B tools/round-46/registry.py --root . --freeze 0425224 --rev 0425224` | `0425224` | met |

Owned scores: coverage `10 → 10` (command A at `7bf33e31`: `knowledge_files 138`, `mapped 138`,
`missing []`, `dangling []`, `coverage_score 10.0`; this round adds no domain surface — S142 is
instrument documentation); depth `10 → 10` (rule blocks `22 → 23` with `citation_resolved_rules
23/23`, `depth_score 10.0`; the move is the discriminating block and its counter, not a number above
the ceiling); calibration `10 → 10` (registered `6 → 38` of the census with `thin []`,
`absent_at_rev []`, and 0 of 7 forgery classes accepted; the numeric axis cannot rise above 10).

Learning trends: expansion **unchanged** (no new domain ground, no admitted knowledge entry, the
coverage map and `## Frontier` byte-unchanged); quality **improved on the instruments** (both
counters score their own 9 and 7 forgery classes red while the genuine artefacts stay green, and both
reproduce round 45's verdicts on the round-45 artefact — `22/10/8` and `45/6`; the bound is that this
is measure quality, not new reverse-engineering ground); discernment **improved** (four of the
round's own defects were found before the operator did — M46-1 a control naming a measurement that
could not exist at the freeze, M46-2 a frozen denominator no digest pins, M46-3 the four-commit
freeze, M46-4 the depth-proxy harm — and two became `QUALITY.md` row 77). No capability row enters:
both artefacts are instruments cited by their own claims, and this round demonstrates no new domain
ground.

**Freeze-integrity disclosure.** The frozen set is derived from this round's claims file
(`plans/round-46-claims.md`, `tools/round-46/`) and feeds the history arm
(`-m --diff-merges=first-parent`), an independent blob arm, the restored classifier and the dirty
scope, so R45-CL18 cannot re-enter by construction. `git log --name-status
31820472..31820472 -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.
The arm's correctness depends on the two flags' order (R46-CL6), the mutation list is a fixed count
no digest pins (R46-CL4), and the registry validates shape rather than truth (R46-CL5).

- **planned (round 47):** calibration or depth from the routed list — (a) pin the mutation list with
  a `mutations_sha256` and make the routed-id and arm-vocabulary checks exact rather than
  substring/one-of (R46-CL2, R46-CL3, R46-CL4); (b) bind the registry's `purpose` cell to a value
  the counter derives, so a false description fails (R46-CL5); (c) assert the `-m
  --diff-merges=first-parent` flag order in a selftest case (R46-CL6). Second choice: coverage —
  resume the SquashFS v1/v2 promotion with a single, mutually consistent provenance clause
  (R44-CL2). R36-CL5, R40-CL2, R41-CL3 remain open.
- **retired:** none. Coverage, depth and calibration stay tied at 10; no finite proxy saturates an
  axis, and the last capability entries are rounds 42–43.

**Amendment F5/A4/B1 (append-only).** The measured freeze is `332f4884` (not `0425224`) and the
measured revision is `58eb04b6`; both claims re-measure identically there
(`l1/scores/{c1,c2}-at-A4.json`: `rule_blocks 23`, `rows 13`, `refs 9`, battery `9/9/0/1`;
`scope_size 38`, `registered` 38, `thin []`, `absent_at_rev []`, battery `7/7/0/1`). Wave 1 found
two HIGH instrument defects that the round closed: the frozen set was derived at the measured
revision and could be shrunk by the revision it checked (R46-CL9), and the counters executed from
the worktree with no dirty arm although the claims file promised one (R46-CL10) — F5 unions the set
at both ends and refuses a dirty frozen path, with `cases=18 failures=0`. The R45-CL19 row's exit
cell was wrong and is corrected (R46-CL11), and the L1's three fallback registry rows were replaced
by the seat's source-derived rows (B1). **Open, and the round's sharpest limit:** the C2
verdict-map clause binds the digits 0/1/2 rather than their meanings, so a contentless row with
`0=banana; 1=nope; 2=whatever` still scores met (R46-CL7) — sixteen forgery classes caught, row
content not checked.

## Record corrections — round 47

- corrects seats round-45: 2 waves, 76 seats total
- corrects window round-46: empty in 31820472..31820472 -- tools/round-46 plans/round-46-claims.md
- corrects seats round-40: 2 waves, 80 seats total
