# ConnSources — scoped cross-source consistency scan

## Axes and evidence

Declared axes: R51-C1 **coverage**, R51-C2 **depth**, with **calibration** also owned (plans/round-51-claims.md:13–20). This proposal improves calibration of the coverage claim without changing runtime behavior, carrier scope, counters, or C2 depth. It does not establish the coverage predicate.

Read-only evidence: corpus/SOURCES.md rows S108 (:114), S112 (:118), S138 (:144), S245 (:161), and the directly relevant append-only correction S248 (:158); corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md:35,48,52,72–78; plans/round-51-claims.md:35–45,90–99,187–191. Input fingerprints and the exact command, exit status, UTC time and stdout digest are in input-receipt.json. No external sources opened and no extraction, controls, REA, or synthetic probes run.

## 1. Existing publication claims and their boundaries

| Row | What it actually grounds | Boundary the new law must respect |
|---|---|---|
| S108 | Pinned unblob 26.6.4 extractor selection, LE/BE argv, AVM test and dependency names; its takeaway explains the missing-dependency gap. | Explicitly **not traversal, REA gap wording, or any carrier**. It is not source evidence that device nodes are omitted or that symlinks are rewritten/removed. |
| S112 | Pinned v4 **BE** extractor dependency and argv, including sasquatch-v4be. | Not the binaries themselves, other versions, or the LE publication law. |
| S138 | Upstream v1/v2 expected member bytes and path/hash agreement on those historical carriers, not an independent producer. | Explicitly **not handler code or extractor behavior**; 22-file census grounding has the new correction row S248. It cannot establish v4 AVM special-node behavior. |
| S245 | Pinned v4 LE handler name and `-le` argv; standard LE and AVM-marker LE use the same handler/argv. | Explicitly **not the extractor**, BE AVM branch, or other versions. It grounds invocation identity, not filesystem materialization or REA publication policy. |

Thus none of the four rows directly establishes the proposed special-node/symlink publication law. S138 is closest to an output-tree claim, but only for its v1/v2 regression dataset. S108's gap takeaway does not widen its explicit evidence scope. Existing scopes and used-by cells must remain untouched; a newly opened source claim or correction needs a NEW row. S248 is a concrete local precedent: it says `supersedes S138` for census grounding, without converting that dataset into extractor-behavior evidence.

The round-50 entry itself supplies narrower carrier observations: :35 says oracle regular paths are mapped by equality into the chunk root and symlink targets are compared only by path/kind; :52 says no char-device oracle path has a disposition on the FRITZ!Box receipts and labels the producer-wide explanation **inference**. The same paragraph discloses g7581 rerun instability. These are not upstream source rows and must not be silently promoted into a universal law for fifos/sockets.

## 2. Contradictions, explicitly separated

**Between the requested source rows: no device-node or symlink-behavior contradiction found.** None makes a device-node or symlink materialization claim. S108 includes LE/BE invocation scope while S245 references S108/S112 as the BE AVM context; that shorthand does not negate S108's LE argv coverage. Their overlap is invocation identity, not publication semantics.

**Within the round-50 knowledge entry there is an epistemic contradiction:** :35 explicitly says the retained receipts do not establish a universal symlink rewrite rule and carries readdir-order dependence as **inference**, whereas :48 labels removed-set readdir-order dependence **observation**, and limit 7 (:78) labels `unblob rewrites targets` plus order dependence **observation**. Preserve this historical entry; the new entry should state the narrower :35 qualification and cite the older overstatement as superseded, not inherit it as fact.

**Between the round-51 declaration and its historical evidence:** claims :26–31 attributes the whitelist to generalization from the Cable class, but the round-50 entry :52 explicitly says the receipts cannot establish whether it was derived from Cable or simply wrong. The mismatch is causal attribution, not the measured 13-versus-1 census or 2-of-4 miss. Also, claims :38–40 generalizes to devices/fifos/sockets and explains it with `an unprivileged extraction cannot mknod`; none of the four scoped rows supports that explanation. In particular, evidence about device creation alone does not establish FIFO omission or absence of REA gap records. Newly opened source rows must carry each additional step, otherwise mark it unestablished rather than obtaining it from S245.

## 3. Round-51 citation / used-by routing

- **Do not add the round-51 entry to S112**: BE-only dependency/argv scope is mismatched to the LE law.
- **Do not add it to S138 or S248**: old v1/v2 expected-tree/census evidence is neither this carrier set nor extractor publication semantics.
- **Do not add it to S108 merely to support devices, symlinks or REA gaps**. Its LE argv portion is compatible if explicitly discussed, but S245 is the direct, required LE handler citation; duplicate S108 is unnecessary for this entry's claimed law.
- **Cite S245 for handler/argv identity only**, as required by claims :94, not as support for omitted special nodes or symlink safety. Per the append-only contract, do not retrofit its existing used-by cell; the new source row(s) opened for the law should carry the new entry in used-by. Existing S243/S244/S249 citations remain required, each within its symbol/listing/licence scope.

## One bounded proposed move: source-to-claim attribution block

Add one compact block to the round-51 knowledge-entry draft, leaving historical rows/entry unchanged:

> S245 grounds only the pinned `squashfs_v4_le` / sasquatch `-le` invocation. New round-51 source row(s) ground the extractor's special-node and symlink implementation; the committed carrier receipts ground REA's observed disposition projection. The rule change repairs the observed one-versus-thirteen char-device census mismatch; the historical receipts do not prove how the old whitelist was derived. Symlink comparison remains path/kind-only; neither universal target rewriting nor readdir-order causality is established by the retained round-50 receipts. Any additional fifo/socket rule is implementation-derived, not four-carrier empirical coverage, unless a corresponding oracle census exists.

Use this same attribution boundary when L1 amends the freeze's law wording. This is one documentation/contract clarification, not a new extractor design or admission decision.

Second-order surfaces: runtime stays unchanged; contract separates invocation, extractor implementation and REA envelope facts; substrate retains append-only source history and historical miss evidence; verification must pair each sentence with the proper new-source locator or committed receipt rather than accepting a citation-presence binding as semantic proof.

Risks: a citation-only binding may still pass an overbroad sentence; new upstream implementation evidence can differ from the installed pinned sasquatch version; `required=false` can relax accounting more broadly than an empirically established silence law. This scan does not resolve those implementation questions or prescribe counter changes.

Verification for L1 (not run here): inspect the new source rows' version/locator and exact claims; ensure no old row was edited; inspect the round-51 entry's used-by placement and attribution; independently check class-specific nonregular census and old/new controls. A new observation about symlink order needs a reproducer, not the old entry's label. No coverage/depth result is asserted by this report.

## Self-evaluation

Accuracy 4/5: exact local scopes and contradictory labels cited; implementation truth was deliberately not tested. Completeness 5/5: all four rows, the three requested questions and one bounded move covered. Clarity 4/5: separates source-row disagreement from entry/claim disagreements, at some length. Actionability 4/5: pasteable attribution block; new source identities remain the source-opening seats' output. Conciseness 4/5: detailed evidence retained in findings rather than terminal handoff. Overall 4.2/5. Highest-impact improvement is L1 matching the new rows to the law before freeze; no unsupported source or runtime claim is presented as verified. User-alignment check: all requested answers are explicit, with no lane edits or runtime invocations.
