# R23-C1 cross-item falsifier — historical evidence re-entering the explicit new scan

## Finding

**Observed source gap:** the candidate keeps the historical and new witness lists separate, but does not make their evidence identities disjoint. A copied historical envelope can therefore be re-attributed by the explicit R23 scan as a new, source-linked witness. The per-verb union prevents a second coverage point, but the output can falsely imply that the historical evidence was newly produced or newly sourced.

This is a counter-path inference, not an observed exploit in candidate `2838351450ff1ee4baa620c962a1153450d53311`. The candidate's newly cited evidence IDs differ from the two historical identify IDs recorded in W1; no copied historical witness was observed in the entries reviewed.

## Axes

Frozen `.ufo/waves/round-23/claims.json:6-11` names **coverage 10**, **depth 10**, **calibration 10**; coverage is the tied-lowest working axis. The proposal below improves **calibration** and provenance depth; it does not increase `k`, change the six-verb denominator, or weaken the incomplete-unless-6/6 rule.

## Evidence (observed)

- Pinned candidate counter bytes: `2838351450ff1ee4baa620c962a1153450d53311:.ufo/waves/round-23/tools/count-c1.py`, SHA-256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`.
  - `:64-68` compares the R22 evidence-root tree at the measured revision with baseline `B`; this protects the historical root from edits.
  - `:81-84` measures the historical pass at fixed `B=aa1450b82f9ede35aada63efe8a34e01c6e02f72`, requires its sole held verb to be `identify-flutter-build`, then prepares helpers for the measured revision.
  - `:92-93` carries that baseline's `bound_evidence` into each target's `historical` field.
  - `:97-110` scans the R23 evidence-path namespace and marks an entry eligible if **any** first-line source ID resolves to an S058+ A/B mined row opened on 2026-10-21 whose `used-by` contains that exact entry path. It stores only `eligible = True`; it does not retain which row qualified.
  - `:111-124` independently loops over the entry's evidence IDs and cited R23 `.json` paths, binds the envelope, and emits only `{entry, evidence_id, path}`. There is no comparison of the new evidence ID or blob to historical evidence before append. `:125-133` then unions the historical/new booleans per verb, so a duplicated identify record cannot raise `k` but can appear in `new` as if it were a fresh witness.
- The source-linkage boundary was already correctly identified in W1: `w1/CounterSources.md:227-230` says new evidence must not be a copy of R22 envelopes; `:251-259` distinguishes exact linkage from manual relevance. That copy exclusion is not enforced by the candidate counter.
- W1's source-row proposal is also still absent from the candidate witness output: `w1/ConnectOutsideDebt.md:289-311` proposes retaining a qualifying source-row ID/media hint; candidate `count-c1.py:124` drops the row ID. This matters because the committed source rows include different kinds of provenance: candidate `corpus/SOURCES.md:64-67` has S058 manual, S059 dataset README, S060 own-work signal envelopes, and S061 own-work Dart output. The candidate Dart entry's first line is `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md:1` (`source: S061 ...`). The S061 link is eligible under the candidate's tier/status/date/used-by predicate, but the result record itself cannot say which source row admitted a witness. This is not a claim that the observed Dart parse needs an upstream semantics source: the entry confines its result to this REA observation.
- Historical identify evidence is specifically two R22 envelopes, `ev_6a84742a…` and `ev_3458b996…` (`w1/CounterSources.md:169-188`, especially `:174-176`). The candidate's retained `verify/initial/after-c1.json` names `source_rev` `6615aeae642aec36959180e7ea940b2794c7f1cb`, not `2838351450ff1ee4baa620c962a1153450d53311`; it is not treated here as a count at the candidate commit.

## Cross-item inference

A one-file review can accept each piece in isolation: the old R22 tree is unchanged; a new entry has an exact `used-by`; the new path is inside the R23 root; and `bind_new` accepts an otherwise valid original envelope. Together, however, a copy of a historical identify envelope placed under the R23 path and cited from an S058+-eligible entry satisfies the new scan. The historical award remains independently present from B. This is a provenance/recency misattribution, **not** a numerical duplicate-verb inflation: `exercised` remains one boolean per verb.

Current source linkage uses an any-row gate at entry granularity; the emitted witness is keyed by entry/evidence ID/path, not by qualifying S row. Therefore an own-work row can satisfy the mechanical source gate, and nothing in the output distinguishes that from an upstream semantics row. W1 `ConnectSourceChain.md:212-230` proposed splitting signal source layers, while `ConnectOutsideDebt.md:289-311` proposed carrying source identity; neither is present in the candidate's new-witness shape. Keep the source relevance judgment manual as the frozen claim does; this finding does not propose auto-admission of source semantics.

## One bounded move

Add a **source-attributed, history-disjoint new-witness record** to the R23 counter:

1. Retain the exact qualifying S058+ row ID(s) (and source kind) that made the entry eligible, and include them in each emitted new witness. This exposes whether a witness is linked through a manual, dataset, or own-work row without claiming that the row is semantically sufficient.
2. Before appending a new witness, exclude/flag any `evidence_id` already present among B's historical bound witnesses. Preserve the historical record as historical; do not let an R22 witness copied into an R23 path acquire a second “new” provenance label.

This changes neither the union-by-verb count nor the historical award. It improves calibration and auditability while leaving source relevance and evidence authenticity expressly manual/unknown. On the present candidate, the guard should be dormant: no historical ID reuse was observed in the reviewed R23 entries.

## Risks and verification

- Evidence-ID uniqueness is an identity boundary, not authentication. The output must retain the existing no-authentication limitation; a fresh ID or edited envelope is not proof of independent production.
- Multiple S058+ rows can qualify the same entry. Preserve the full qualifying set rather than silently selecting one; do not infer that every listed row supports every statement.
- Do not make upstream-source presence a new counter gate: that could reject the current scoped own-work observations and change coverage beyond this falsification.
- Verification required after any implementation: an isolated negative control copies one baseline identify envelope to an R23 evidence path and cites it from a valid S058+ entry. Expected: the baseline identify remains historical, no new identify witness is emitted, and `k` is unchanged. A distinct new evidence ID must still be eligible with its exact source-row link. **Not run here.** This seat performed source review only; it did not execute the counter or any tests.

## Produced files and installs

- `.ufo/waves/round-23/w2/ConnectFalsifiers.md` — this report; SHA-256 will be stated in the handoff (not embedded in itself).
- Installs/updates: none.
