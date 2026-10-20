# RegistryDraft — round 16 w1 report

Scope: draft the quote-fidelity pinned-values cell addition for the round-15 boundary baseline, and align the go-snapshot-inventory command. Draft text is in `RegistryDraft.candidate.md` (this directory). No existing doc was edited. No command was executed by this seat: no gate, selftest, sha256, measure, or inventory run. All verdicts below are read from source or from retained round-15 artifacts.

## Behavior

Adds one supplemental reference to the quote-fidelity pinned-values cell (`SKILL.md:450`): `.ufo/waves/round-15/boundary-fixtures/expected.json`, invoked as a separate `--frozen` run. Adds no gate semantics, classifier, or capability claim.

Aligns the go-snapshot-inventory entry (`SKILL.md:487`) and the knowledge `recheck:` line (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3`) to the argv that was actually retained (`python3 -I <abs script> --ghidra … --select 1.24.7 1.25.7 1.26.8`).

## Evidence read

- Frozen schema: `quote-fidelity.py:48-54` (`manifests` entries carry `path, sha256, exit, findings`; `sources` carries `path, sha256`); `parse_frozen` `:300-347`; every manifest source must be pinned, `:368-381`. The r15 `expected.json` matches this shape: two manifests, one pinned source (`raw-source.md`).
- Manifest keys: `parse_manifest` `:173-209` reads only `sources` and `quotes`; the extra `provenance` block in the r15 manifests is ignored.
- Finding ID: `grade_quote` `:250-258` emits `quote_not_contiguous` with `ident = quote["id"]`. The rendered-rejected fixture's quote id is `raw-literal` (`rendered-rejected.json:18`), so its finding is `quote_not_contiguous@raw-literal`.
- Retained round-15 run (`.ufo/waves/round-15/verification.json`, revision `7ad23fe1…`): `rendered-rejected` standalone stdout `QUOTE_FIDELITY: quote_not_contiguous ident=raw-literal`, exit 1 (`:97`); `boundary-frozen` argv `python3 -I …/round-14/tools/quote-fidelity.py --frozen …/round-15/boundary-fixtures/expected.json`, exit 0, both pins `match`, `mode=frozen manifests=2 findings=0` (`:108-123`).
- Inventory argv: `verification.json` labels `snapshot-inventory` and `inventory-determinism` both use `python3 -I /home/vgpnk/…/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`, exit 0; stdout SHA-256 `ad06fadc…2fe` (`:180`).
- Script defaults: `DEFAULT_SELECT = ("1.25.0", "1.26.0")` (`snapshot-inventory.py:66`, `:414`). Exit map: 0 complete, 2 could-not-evaluate (`:40-44`).
- Lesson routed defects 1 and 2: `corpus/lessons/round-15-verifier-spotcheck.md:185-186`.

## Findings

**F1 — Wrong finding ID circulates in round-15 seat prose.** The correct ID is `quote_not_contiguous@raw-literal`: the fixture quote id, the frozen pin (`expected.json:14`), and retained stdout (`verification.json:97,123`) all agree. Several round-15 drafts instead say `@rendered-text`, or in BoundaryFixtures.md:82 print `ident=rendered-text`:
- `w1/BoundaryFixtures.md:65,82,101`
- `w1/AttackManualBoundary.md:170`
- `w1/SiblingBoundary.md:101,220`
- `w1/CriterionDraft.md:37,81`; `w1/CriterionDraft.candidate.md:25`
- `w1/SourceCustody.md:103`
- `w1/AttackAdmission.md:162,188`

The `w1` list is from a grep whose output was paged (20 of 25 files shown), so it is not exhaustive. The draft cell uses `raw-literal` only; none of these prose strings should be copied into the registry.

**F2 — Stale rendered-rejected digest in prose.** `BoundaryFixtures.md:22`, `SourceCustody.md:19`, and `SiblingBoundary.md:101` cite `rendered-rejected.json` as `bc97c469…` at 620 B. The current pin in `expected.json:11` and `measurement-pins.json:7` is `92c8904b…`; the listing shows 618 B. The retained frozen run matched the `92c8904b…` pin (`verification.json:123`). Cause: [INFERENCE] the fixture was changed after the prose was drafted; the change matches the id change above. Not confirmed from git history (not run). The registry must cite only `expected.json`'s pin.

**F3 — Inventory row command does not match the retained argv.** Current `SKILL.md:487` entry is `python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra …`. It has no `-I`, a relative path, and no `--select`. Run as written, it selects `1.25.0 1.26.0`, a different inventory, and cannot reproduce `ad06fadc…`. Same defect in the knowledge `recheck:` line (`:3`), which lesson defect 1 flagged. Draft B and C align both to the retained argv.

**F4 — Verdict wording in the inventory row is loose.** "0 emitted, nonzero could-not-evaluate" does not match the script's own EXIT table (`:40-44`). Draft B uses "exit 0 inventory complete, exit 2 could-not-evaluate". This is wording only; the probe's verdict map is unchanged.

**F5 — Path resolution.** Frozen-manifest paths resolve against the expected file's directory (`evaluate_frozen` takes `base_real` from the expected path, `:353`). The `--frozen` argument itself is cwd-relative. The retained run used an absolute `--frozen` path; the draft's repo-relative form is not separately exercised. Recorded in the candidate.

## Integration (L1)

1. Apply Draft A to the pinned-values cell of `SKILL.md:450`, the only cell change in that row.
2. Apply Draft B to `SKILL.md:487`, the whole row.
3. Apply Draft C to `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` (line 3 only).
4. Optional, not drafted here: correct the `@rendered-text` and `bc97c469` prose listed in F1 and F2, in the round-15 seat files that carry them, and record the stale fixture in the round-15 closure if it is cited.
5. Verify once after integration (L1's job): `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --frozen .ufo/waves/round-15/boundary-fixtures/expected.json` should exit 0 with both pins `match`; the inventory argv should reproduce stdout SHA-256 `ad06fadc…`. Neither was run by this seat.

## Limits

- No execution. Retained results are from revision `7ad23fe1…`; current bytes of the fixtures and the installed Ghidra data were not re-hashed. The `expected.json` pins were read, not recomputed.
- The F2 cause is an inference. The F1 list is partial.
- Draft C alters a corpus knowledge file. It is an L1-integrated change, not applied here.
- Round-15 `no-harm-controls` count-provenance (lesson defect 3) and the SHONEN wording (defect 4) are out of scope.

## Tools

None installed or updated by this seat.
