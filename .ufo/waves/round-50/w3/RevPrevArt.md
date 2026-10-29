# RevPrevArt — round 50 attempt 2 wave 3: R41→R50 counter port audit

## Verdict

**PASS — no scoring-time drift in the round-41 → round-50 `c1-counter.py` port.**
All 19 round-41 clauses ported (4 new added); all 9 non-`compression_coverage`
bindings ported (that one removed deliberately, disclosed PORT-DELTA C13). All
eight named behavioural deltas (handler, superblock layout, sasquatch binary,
target ids, round tokens, provider_timeout retry, fetch containment, oracle
re-derivation) confirmed present. Both counters are byte-frozen at the base
revision and both offline selftests pass against a stub rea-agents package (no
REA invoked). Full analysis: `.ufo/waves/round-50/w3/RevPrevArt/port-audit.md`.

## Findings table

| # | finding | evidence (exact command) | exit | receipt sha256 |
|---|---|---|---|---|
| F1 | No clause/binding dropped. r41 19 clauses ⊂ r50 23; only removal is `compression_coverage` (disclosed). | `python3` CLAUSES/BINDINGS tuple diff over both counters (port-audit §2) | 0 | — |
| F2 | r50 offline selftest passes (scoring logic coherent). | `python3 tools/round-50/c1-counter.py --selftest --pkg65 $S/stub-rea --work $S/work` | 0 | `8c3476fa…d008705` (169 cases, green 17 / red 152, failures 0) |
| F3 | r41 control selftest passes (stub is a valid stand-in; port source coherent). | `python3 tools/round-41/c1-counter.py --selftest --pkg65 $S/stub-rea` | 0 | `34c4f06e…e3d741` (97 cases, green 12 / red 85, failures 0) |
| F4 | Frozen bytes confirmed. | `git diff --stat f890bbe… -- tools/round-4{1,5}/c1-counter.py` (empty); r50 `9820811b…9bd813` | 0 | — |
| F5 | Docs-binding literals verified (exact regex/heading values quoted in port-audit §4 for the landing text). | `python3` regex probe of `AVM_MARKER_RE`/`LE_AVM_RE`/`HANDLER_RE` + `section()` read | 0 | — |
| F6 | CALIBRATION (not drift): plan says "sasquatch 4.5.1" but the counter enforces sasquatch *presence* on FIXED_PATH + sha256-record, not version-equality (unblob 26.6.4 / REA 6.5.0 / unsquashfs 4.7.5 ARE pinned). L1 may pin sasquatch version or record a disclosed limit. | read `toolchain_record` r50:1968-2003 | — | — |

Selftests ran offline against a stub rea-agents 6.5.0 package (xpin-compatible
`dist/domain/canonicalDigest.js` + `evidence.js`), NOT the npx package; `node`,
`sasquatch`, `unsquashfs 4.7.5`, `mksquashfs 4.7.5` are the real host tools. The
stub `semanticProjection` excludes `evidence_id` (as the real rule must), which is
what makes mint-vs-recompute consistent while the stale-evidence-id case still
fails. Receipts copied to `.ufo/waves/round-50/w3/RevPrevArt/`. Not run: any REA
data run or `--selftest-rea` (wave-forbidden); selftest not run against the real
npx package (constraint).

## Deliverable

`.ufo/waves/round-50/w3/RevPrevArt/port-audit.md` — (1) confirmed deltas, (2)
un-ported clauses (none), (3) LE-specific clauses + selftest cases, (4) the four
documentation-binding clauses with verbatim literals. No edits to the lane tree.
