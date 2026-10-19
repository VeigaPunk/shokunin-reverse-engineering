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
| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |
| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps — the paired demonstrations: r7 wall-fall (ev_a4aa9b0d…) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |

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
  coupling) — all nine stale literals cleared, 162→162 lines held, no line
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
