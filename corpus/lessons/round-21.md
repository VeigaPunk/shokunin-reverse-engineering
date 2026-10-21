# Round 21 — record-bound evidence and bounded first-failure observations

Author: KaidokuR21, attempt 1. Baseline `2dd430cb6bcad60ff4db720c052074f1f75eecbc`; claims frozen and pushed at `f4e95af909d692156e984bf2049e1c7fb4a2a836` before tool measurements. The outside round-20 verifier is non-author MadoR20Recovery; its narrow admission is retained, not rewritten. This round owns calibration C1 and depth C2, with calibration tied-lowest under the existing finite 10.0 proxies. Neither proxy measures mastery.

## Gate

Source opening by the author on 2026-10-21:

| Row | URL and location | Located contiguous quote (at most 25 words) | Decision / scope |
|---|---|---|---|
| S049 | https://www.rfc-editor.org/rfc/rfc8259 — section 4 Objects, page 6 | “The names within an object SHOULD be unique.” | admit as JSON interoperability support; local Evidence binding additionally requires application fields. A string containing a verb is not the verb's operation member. The RFC does not authenticate Evidence. |
| S050 | https://docs.python.org/3/library/json.html — Repeated Names Within an Object, Python 3.15.0 documentation | “The object_pairs_hook parameter can be used to alter this behavior.” | admit as documentation of explicit decoder ambiguity policy; no host-version or execution claim. The preceding paragraph says default decoding retains the last name/value pair. |

Registry changes: S049/S050 added as mined tier A, used-by this lesson. Existing S001–S048 cells intentionally unchanged. Source rows are not counted as knowledge expansion. Bounded search: two official documents identified, screened and included; zero excluded documents. Stop: JSON mapping/decoder ambiguity is answered; REA-specific producer semantics remain grounded in retained REA records, not inferred from the JSON specification.

Candidate rejection rules frozen with the claims: reject a matching id/operation spread across unrelated records; reject a typed refusal as held success; reject missing or malformed observation metadata as bounded silence. Admit valid same-record success and valid bounded-null observations only within their declared scope. Actual decisions and exercised evidence are appended after integration; author-side workers cannot supply the required outside admit/reject spot-check.

## Mistakes

| Class | Motivating evidence | Captured-by | Fix and failure requirement |
|---|---|---|---|
| vacuous — record association mistaken for token co-occurrence | round-20 verifier R20-EVIDENCE; round-20 tools/verb-coverage.py bound_evidence | QUALITY #25, whose registered limitation is only token checking | C1 successor must associate the cited id and exact operation within one supported Evidence record and reject typed refusal records. A frozen independent negative must false-pass at baseline and fail under the successor, with a genuine positive retained. |
| vacuous — absent observation confused with bounded silence | round-20 tools/compare-first-failure.py run_extractor accepts bare JSON null without last_line | QUALITY #7 and #11; existing extractor documentation bounds absence through its last retained line | C2 requires the extractor envelope, explicit first_failure, and valid last_line. A frozen bare-null case must expose the old false clean; valid bounded silence and both asymmetric-null mismatches remain distinct. |
| scope — aggregate C1 harness reuses C3 carrier receipt | round-20 verifier R20-SEP and Causal separation ruling | causal separation is about independent verifiability, not mere helper sharing | Replace the current positive-control authority with a C1-owned isolated fixture, retaining both positive and package-decoy checks. The old aggregate remains historical. Shared validator use alone neither proves nor disproves causal coupling. |

## Routed residual dispositions

- R20-SEP: addressed within C1; actual correction and test evidence must be appended before closure.
- R20-EVIDENCE: record binding and refusal negatives are C1; bounded comparator negatives are C2. No cryptographic Evidence authentication claim is made.
- R20-TIME: exact two 2030 fixture/diagnostic allowances remain historical. Binary and zoneless text exclusions remain exclusions; no full-tree timestamp claim.
- R20-LINT-SANDBOX: duplicate-name nested-read D6a and host-HOME/AF_UNIX D6b remain open. No private HOME inspection, no sandbox/security certification.
- R20-CENSUS-GUARD: DATED shelter/same-line laundering and loader/copy/memfd/same-owner bypasses remain open. Green guard records attest instants only.
- R20-SOURCE: S041/S045/S046 rendered-quote caveats and S043 unrowed -c anchors remain documentation debt unless a fresh superseding source row is explicitly landed. Existing rows are not silently rewritten.
- R20-ADJACENCY: REA overlap with revenger remains unresolved; evidence-tool maintenance does not confer province ownership.
- R20 C3 remains nineteen exact-artifact outcome-held-out forecasts, not general Go-version prediction. This round's replay of those observations is retrospective regression, not new prediction. Pathless objdump subject:null, synthetic Harmony, and later objdump OOM remain explicit boundaries.

No native carrier, REA producer, provider probe, account/configuration, host package/service/boot, or secret material is in this round's planned execution. No tool installation is required.
