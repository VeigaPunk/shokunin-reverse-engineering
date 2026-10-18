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
| coverage | 9.72 → 10.0 | 78/78 knowledge files mapped; index integrity only, **not** fraction of the REA domain held | `corpus/README.md:11-67`; command A; baseline `a79945c4`, measured `3395b6d` | luna-round-1 + luna-round-7 |
| depth | 10 → 10 | 9/9 queue-drain rule blocks have resolvable file/range citations at `638fb211`; **not** semantic correctness, generality, or fresh execution — the r3 semantic contradiction removal is measured by the contradiction census, not this proxy | `SKILL.md:77-191`; command A; baseline `a79945c4`, measured `638fb211` | r1 measurement + luna-round-3 |
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
  frontier bullet now reads "held, not frontier" (`corpus/README.md:178`;
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
| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |

Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.

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
