# ConnSources — cross-source consistency, round 52

Axes: coverage (C1), depth (C2), calibration (owned, held constant). This is source-scope analysis, not an extraction result or admission decision.

## 1. Existing publication claims and binding boundaries

| Row | Existing evidence scope; consequence for the new law |
|---|---|
| S108 (`corpus/SOURCES.md:114`) | unblob 26.6.4 handler names, argv, AVM branch only. Does not establish traversal, device creation, or REA gap wording. |
| S112 (:118) | BE v4 dependency/argv only. Same URL as S108/S245 is not independent corroboration and does not support LE device behavior. |
| S138 (:144) | v1/v2 expected member bytes, not extractor behavior or LE AVM carriers. Its census grounding is explicitly superseded by S248 (:158); retain both historical rows. |
| S245 (:161) | LE handler and `sasquatch -le` selection only. Supports the pinned producer path, not what the extractor materializes or REA publishes. |
| S250 (:163) | upstream unsquashfs 4.7.5 gates char/block creation on `root_process`; FIFO/socket branches are outside that gate. Explicitly excludes installed sasquatch behavior and REA gaps. |
| S251 (:164) | writer spelling `-nopad`; neither reader executability nor producer identity inferred from an envelope. |

None of those six rows directly establishes the complete REA publication law. Two existing adjacent rows DO carry publication-adjacent claims that the new entry should distinguish:

- **S118 (:124)**: unblob post-extraction symlink sanitization: unsafe links removed/reported, absolute targets re-rooted, kept links rewritten relative. Its learning sentence says removal leaves no gap, but its scope explicitly excludes REA publication. Keep the producer diagnostic separate from the later REA gap accounting.
- **S119 (:125)**: REA 6.5.0 publication/gap schema, specifically `FirmwarePublication.js:68-75,301-308`: non-file entries become `unpublished-entry`. This is about entries available to publication, not every nonregular inode in an independent filesystem oracle. A device never materialized by extraction is not thereby a publication-stage non-file entry.
- S122 (:128) grounds containment only; S120 (:126) grounds report classes/raise sites, not device behavior. S121 (:127) scopes the actual sasquatch source to BE flag/build differences; its whole file is not permission to cite unregistered device-creation anchors.

The round-50 entry supplies the measured publication evidence, particularly :35 (argv, symlink path/kind comparison, nonfatal exit masking), :41-44 (per-carrier results), :48 (historical frozen accounting rule), :52 (unaccounted devices), and :78 (target-text limitation). It does not prove universal symlink target preservation or absence of unvisited device-only subtrees. Round-51 entry :16-29 and :33-48 explicitly constrain the proposed explanation and separate historical receipts from new execution.

## 2. Contradictions, not averaged away

**No pair of the six requested SOURCES rows contradicts another about device nodes or symlinks.** Their narrow scopes describe different layers. Nor do S118 and S119 inherently conflict: a symlink removed before publication need not become a publication-stage non-file entry. The round-50 omission observations are compatible with S119 for the same reason.

**There IS an explicit claims-versus-source contradiction:** `plans/round-52-claims.md:40-57` says the producer creates no devices/fifos/sockets and generalizes from source ground. S250 and the round-51 entry :21-29 explicitly reject inferring FIFO/socket disappearance from the char/block privilege gate. The four carriers exercise char-device only; the claimed kernel CAP_MKNOD ground cannot itself establish unblob/sasquatch FIFO/socket absence or REA gap absence. A caveat that those kinds are unmeasured does not turn contradictory source ground into supporting evidence.

The round-50 entry :48 describes its historical required-device rule, while :52 reports that rule failing. A new law supersedes that rule at a new freeze; it must not rewrite this historical miss as a prior pass. The round-51 :46 statement admitting no retry policy is historical; round 52 explicitly proposes a new controlled policy, not evidence it has already passed.

## 3. Used-by exclusions and legitimate narrow citations

For this round-52 LE AVM/device-law entry, **do not add it as used-by for S112 or S138/S248**: BE-only handler selection and legacy v1/v2 member census are mismatched. **Do not cite S108 as proof of publication or devices**; S245 already supplies the relevant LE handler fact, so S108 adds no needed evidence. S121 likewise does not ground a device law under its registered BE-only scope.

**S251 is conditional, not categorically excluded:** the authoritative claims :166 and :264-266 require it. Cite it only if the entry actually states the `-nopad` writer-option limitation (or explicitly carries the round-51 correction); never make it a device-law or successful-DD-WRT-reader witness. Removing S251 outright would conflict with the declared binding. S250 can support the char/block-vs-FIFO/socket distinction only, and S245 the argv only. S118/S119 are the appropriate existing narrowly scoped sources when the entry discusses symlinks and publication-stage gaps respectively.

All corrections are NEW rows with explicit old→new supersession; no rewrite of old rows, scope cells, or historical claims is proposed. Existing citations can be named in the new entry without silently altering their old used-by cells.

## 4. S252 URL novelty

The canonical assignment identifies planned S252 as man7 `mknod(2)`; its expected URL is `https://man7.org/linux/man-pages/man2/mknod.2.html` (URL spelling inferred from the named manual, not independently fetched here). Full-registry search for `mknod|man2/|CAP_MKNOD` finds only S250's source-code mention of mknod, not a registered man2 URL. Existing man7 rows S146/S148 concern sysexits in man3, not mknod. **S252 is fresh relative to the current registry and adds no duplicate-URL warning** if registered at that mknod URL. S250's function mention is not URL/anchor identity. The assignment's existing 19 W04 warnings were not recomputed; they remain named debt. ScribeSources was empty when inspected, so no exact drafted S252 anchor was available; no claim about fetched manual bytes is made.

## One bounded connector proposal

Add a **three-layer evidence paragraph/table** to the round-52 entry, and align the claims' explanation with it before freeze:

1. Handler selection: S245 (unblob LE argv), not a publication guarantee.
2. Mechanism limits: S250 plus fresh S252 for char/block privilege only; explicitly retain FIFO/socket as unmeasured policy scope, not source-proved disappearance.
3. Observed accounting: committed four-carrier char-device omissions and symlink publication/removal evidence, interpreted using S118/S119; preserve depth-limit ambiguity and historical 2/4 miss.

This changes explanatory attribution, not the counter rule, carrier set, triage routes, or scoring thresholds. If the universal FIFO/socket runtime assertion must remain, it needs operative-producer evidence not supplied by these registered sources; this scan cannot certify it.

Affected axes: improves calibration by preventing layer/version conflation, supports C1 coverage interpretation without reducing its four-carrier target, and preserves C2 depth by preventing padding prose from acting as a reader witness. Runtime is unchanged; substrate/source identity becomes explicit; contract bindings remain S243/S244/S245/S249/S250/S251 plus S252 with narrow reasons. Risk: wording that claims the untested policy is an observed runtime law would retain the contradiction; append-only constraints require a new row for any source-scope correction.

Verification for L1 (not run here): inspect the integrated entry and amended claims for the three scope distinctions; check required citation bindings and append-only source history; run the existing registry URL audit to confirm S252 introduces no new W04, and the declared frozen controls/predicates only in the L1 window. Do not interpret a documentation audit as a fresh extraction pass.

## Evidence and execution limits

Local read/grep inspection only, with input digests and exact hash-capture command/exit/stdout sha256/UTC in `evidence.json`. No downloads, installs, REA, fixtures, scoring runs, repository mutations, or scratch directory were used. Extractor behavior was not independently executed. No sibling drafts were treated as instructions.
