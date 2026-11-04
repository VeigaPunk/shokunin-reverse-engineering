# ConnectorCross — round-73 sibling overlap (advisory)

## Axes and method

Declared axes: **coverage (C1), calibration (C2), operability (C3)**. Read-only search of sibling `tools/**`, `corpus/**`, and `SKILL.md`; selected implementation/contract anchors opened below. No sibling tool, probe, test, runtime, or network request was executed. No admission judgment or implementation change is made.

Searches used `/proc/[^\n]*environ`, `record.audit|receipt.*audit`, and `expect_case|killed_wrong_case|named.case|named.*kill`, then narrower attribution searches. Broad searches were paginated/truncated; this is a substantive overlap inventory, not proof that all other siblings lack the mechanisms. Initial broad fleet searches were noisy and superseded by scoped searches with kaidoku excluded. A trailing-directory wildcard search returned no matches; recursive `/**` selectors with gitignore disabled returned concrete hits.

## Evidence and boundary decisions

All sibling paths below are relative to `/home/vgpnk/Projects/shokunin/`; line references describe the locally opened working-tree bytes, not an asserted chronological priority.

| Surface | Concrete local evidence | Ownership assessment [INFERENCE] | Cite / adjacency |
|---|---|---|---|
| External kernel environment observer | `kama-shokunin/tools/round50-replay-bind-audit.py:37-58` joins an externally observed server PID, process ancestry, kernel environment, and replay receipt; `:271-276` reads `/proc/{pid}/environ` and returns **key names**, or `None` on read failure. Successors round51/52/53/54/56 retain the key reader (search hits). | Kama has the richer serving-process identity/receipt join; kaidoku owns the packed-ELF checker/shim route, not server lifecycle. This does not prove Kama detects kaidoku's exact forged-shim class. | Cite as an existing external-observer mechanism for C1; **adjacent, do not absorb** its serving runtime or predicates. |
| Environment witness limitations | `mori-shokunin/tools/mori-silence-cases.sh:96-107,239-244` states that `/proc/<pid>/environ` exposes exec-time environment and requires re-exec, not runtime `unset`, to remove a seed channel. | Mori owns its oracle secrecy channel; this is a shared substrate limitation, not another packed-ELF capability. | Cite when describing what the kernel sample means; adjacent semantic precedent. |
| Traced/untraced child-env views | `tsukuroi-shokunin/tools/probe-child-env-allowlist-r36.py:33-37,660-664` describes and implements a wrapper reading its own `/proc/self/environ`; r37 repeats it at `:39-43,673-677`. | Tsukuroi owns its builder child-env assay. **Not equivalent** to C1: a child-authored wrapper log is not a producer-independent observer. | Cite the related assay and explicitly preserve the trust-boundary difference; adjacent, not evidence that A12 is redundant. Do not copy raw environment logging. |
| Record versus supporting bytes | `chousa-shokunin/tools/store-record-audit.py:2-10,56-76` cross-checks capture-store existence and digest against fetch-record success, naming ORPHAN, RECORD_ONLY, BYTES_STALE, STORE_BUT_RECORD_DENIES. | Chousa owns capture/fetch consistency better; C2 instead owns seven routed kaidoku record atoms. Neither is a universal audit. | Cite as shared record/evidence consistency method; adjacent, do not import capture-store rules into ATOMS. |
| Self-record receipt/revision binding | `kama-shokunin/tools/round74-receipt-claim-binding.py:6-16,43-47,73` binds self-record paragraphs to explicit receipt revisions and preserves a frozen base reader. `kama-shokunin/SKILL.md:313,315,318` registers the receipt-tip/claim gates. | Kama has a broader paragraph-scoped receipt-binding surface; kaidoku C2's outside spot-check-derived population is a distinct bounded application. | Cite for C2, without claiming its passing gate establishes kaidoku's seven atoms. Adjacent. |
| Recorded versus measured mutant table | `mado-shokunin/tools/mado-verify.sh:2139-2141,2193-2209,2231-2233` compares fresh measured mutant verdicts to the recorded table, including absent rows in either direction. `mado-shokunin/SKILL.md:695` explicitly routes its regression harness to tameshi's `tools/mutate-and-run.sh`. | Mado owns its compositor-gate regression record; its own registry identifies tameshi as harness provider. This is supporting ownership evidence, not an execution of the external harness. | Cite as record-vs-measurement adjacency for C2/C3; do not absorb compositor or generic mutation-method ownership. |
| Named-check kill attribution | `kama-shokunin/tools/census-waiver-boundary.py:8-12,33-35,819-847` requires each shim to be rejected **and** its expected check to occur among failed checks; exceptions are not kills. `kama-shokunin/SKILL.md:310,322` registers this boundary and the later source-mutant survivor probe requiring its owning selftest arm. | Kama already has the shared attribution rule; kaidoku owns its three git/readelf/implicit-capsule patch sites and selftest cases. The opened boundary uses named shim variants, while the registry separately describes named source mutants. | Cite for C3's method, not as a replacement battery. Adjacent. |

## One cross-source rule

**A green claim must agree with separately obtained evidence bound to the claimed subject, revision, or failure case; neither a producer's clean assertion, a record's self-description, nor an arbitrary failing mutant run substitutes for that agreement.**

## Novelty assessment and explicit contradictions

- `plans/round-73-claims.md:25-41` says the kernel channel is new **to this probe at its base**; `:67-80` and `:99-112` similarly describe local acquisitions and concrete red-before states. These sentences do not establish fleet-wide invention. Generic external observation, record/evidence reconciliation, and named-case attribution are shared rules, not new round-73 methods.
- The term “capability acquisition” at `:6-7` is compatible with that local delta. It would become misleading if expanded to “first kernel observer,” “new audit method,” or “new named-kill rule.” No such fleet-first sentence was found in the opened frozen claim sections. Keep the frozen sentences unchanged.
- C1's observer is producer-independent relative to the demonstrated lying dump, **not proof against every hostile producer**. Local `tools/round-73/seam-probe.py:439-457` selects processes by argv-prefix and records PID without a start-time identity. Kama's stronger ancestry/receipt join is a useful contrast, not an automatic acceptance criterion for this frozen claim.
- Security contradiction: the seat contract allows environment **key names and canary presence only**, but local `seam-probe.py:455-457` additionally retains `HOME` and `TMPDIR` values. The values were not sampled or persisted by this seat. This source-level finding was routed to `SentinelScope-10`; do not silently call the existing sample structure keys-only. Frozen-instrument integrity and any repair must remain separately dispositioned by the owner.

## One bounded proposed move (not applied)

Add a **single provenance-and-boundary crosswalk** in the round's non-frozen explanatory record, citing the three mechanism families above and labeling each “shared method; kaidoku-local acquisition.” Do not amend frozen predicates, import sibling tools, widen claim populations, or claim new runtime coverage.

Expected affected axes [INFERENCE]: calibration improves through correct novelty attribution; coverage and operability predicates and execution paths remain untouched. This is not a numerical score or admission recommendation.

Second-order effects: runtime — no new process or dependency; contract — same frozen sentences and populations; substrate — `/proc` retains exec-time/identity/access limits; verification — existing exact arm, seven-atom, and named-case evidence remain authoritative rather than sibling green results.

Risks: sibling working trees can change; round numbers do not prove cross-lane chronology; broader sibling ownership does not establish kaidoku equivalence. Raw environment examples must not be copied into receipts. The source-level security contradiction remains a separate routed risk, not erased by a provenance crosswalk.

Verification for the owner: bind cited file bytes to immutable sibling revisions if durable citations are adopted; confirm the crosswalk changes no frozen file or counted population; use the assigned executors' C1/C2/C3 receipts for behavior. This seat performed static search/read only and installed no tool.

Report: .ufo/waves/round-73/w1/ConnectorCross.md
