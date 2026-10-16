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
| coverage | 9.72 → 10.0 | 72/72 knowledge files mapped; index integrity only, **not** fraction of the REA domain held | `corpus/README.md:11-60`; command A; baseline `a79945c4`, measured `2abd30f5` | luna-round-1 |
| depth | 10 → 10 | 9/9 existing queue-drain rule blocks have resolvable file/range citations; **not** semantic correctness, generality, or fresh execution | `SKILL.md:77-191`; command A; measured revisions in `evidence/round-1-2026-10-15/result.json` | r1 measurement; no depth change |
| calibration | 0 → 10 | 9/9 preselected reconciliation obligations aligned (2026-10-15); 2026-10-16 per-client REA surface reconciled to live receipts — **failure-selected completeness**, not unbiased accuracy or mastery | Frozen `evidence/round-1-2026-10-15/rubric.json`; command B; luna-round-2 receipts `.ufo/waves/luna-round-2/receipts/`; measured at `75af886a` | operator-steered r1 + luna-round-2 |

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
- **Version drift:** closed by luna-round-2 (2026-10-16) — current-surface
  summaries now state the per-client pins and receipted inventories (Devin/OMP
  6.5.0 207/153, Kimi 6.4.0 170/127; both catalog digests; skill v42 installed
  / v37 expected by 6.4.0). No configuration changed and no 37-tool holdings
  increase is claimed; receipts at `.ufo/waves/luna-round-2/receipts/`.
- **Authority contradiction:** `SKILL.md:207-210` and `corpus/README.md:164`
  universally describe path-sensitive IDs; the later counterexample at
  `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169` is family-specific
  and disproves that universal summary. The citation-resolution score does
  **not** certify these summaries. Request/module identity is not authenticated
  by an evidence ID alone. These two summaries remain unresolved, not silently fixed.
- **Other stale summaries:** `corpus/README.md:157` still lists already-held
  process/managed/call-target operations as frontier; `:128` says four r13
  nits fixed although `LOG.md:395-401` corrects integration fixes to two.
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
