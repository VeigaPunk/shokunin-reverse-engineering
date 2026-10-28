# Round 48 registry attack — ReviewerRegistry

## Axis
Depth: whether instrument-registry verdict maps truthfully bind exit digits to distinct semantic classes, with purpose consistent with those semantics.

## Scope and evidence
Read the full frozen claims file `plans/round-48-claims.md` (declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`) and inspected frozen `tools/round-48/meanings.py` plus `census2.json`. The registry parser reads each row as path, purpose, verdict, selftest, pins, write, owner. The hard classifier checks only (a) a success token in exit 0, (b) a not-met token in exit 1, (c) an unevaluable token in exit 2, (d) absence of banana/nope/whatever, and (e) three distinct segment strings. It does **not** compare the purpose cell to the verdict-map classes, nor establish that the described meaning is implemented by the row’s tool. `census2.json` enumerates 42 paths; a full 12-row sampled semantic audit across rounds 41–48 and executable mutation battery were not run. LSP status/device unavailable in this session; no semantic reference/definition/diagnostics results are claimed.

## Findings

### Actionable predicate gap — purpose is not bound to verdict semantics
`meanings.py:182-197, 445-453` parses and scores verdict maps but never validates `purpose`; thus a row can have a purpose describing exit 2 as usage-only while its exit-2 segment says `unevaluable`, or otherwise contradict the map, yet pass this specific clause. Exact probe shape (apply only to a scratch copy; not run against frozen originals): replace one registry row’s purpose with `gate (exit 2 means usage only)` while retaining `0=met; 1=not met; 2=unevaluable`; run `python tools/round-48/meanings.py --root <fixture> --freeze <freeze> --rev <rev>`. Expected current behavior by code inspection: no failure for that inconsistency. This is a code-level gap, not a claimed observed green score; fixture not created.

### Actionable purpose/tool contract gap — classifier accepts token classes, not tool implementations
The lexical predicates allow broad generic words (e.g. `met`, `fail`, `usage`, `error`) and never inspect tool behavior. A registry row can claim a meaning unsupported by the named tool while satisfying the lexical classification. The rule’s requested “meaning its tool does not implement” check therefore is not entailed by `meaning_classes`; the frozen counter verifies labels, not tool semantics. Need a per-tool sampled audit / mutation fixture to establish a concrete row-level contradiction; not run, so no specific row is asserted.

## Verification and residual risk
No counter, controls, fixture, or 12-row sample was executed. No stdout/exit/hash/time receipts were generated; preserve this explicitly as not run. The two gaps above are derived from the inspected scoring code, not from a passing forgery. Residual risk: purpose contradictions and semantic mismatches remain admissible under the current hard clause, despite digit-to-token-class checking. No installation performed.
