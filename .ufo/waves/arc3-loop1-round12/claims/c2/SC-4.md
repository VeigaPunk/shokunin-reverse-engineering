# SC-4 — C2 depth claim: proposed queue-drain rule #17

**Chain:** `c2` (depth)  
**Status:** draft only; no `SKILL.md`, corpus, or gate changes made.

## Proposed rule #17

> **Sensitivity is local to the semantic projection, not the REA domain.** For each operation and call shape, identify the exact Evidence projection and test candidate-field changes against it (for path questions, compare a same-path repeat with a controlled same-byte alternate path; independently recompute the digest). Name the semantic path fields that participate, and distinguish outer from nested Evidence. Report sensitivity or stability only for the operation/version/shape measured; never transfer a field-stability label across verbs. If the projection or field contribution is not established, leave it unknown.

This is a draft, not a claim that `rule_blocks` has reached 17. The proposed rule is narrower than a universal `ev_` formula: three different operation projections were measured, and `inspect_artifact` demonstrates why outer subject display paths and paths inside a nested semantic result must not be conflated.

## Citation list for the proposed rule

- `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:11,22,26` — semantic projection definition; path-bearing semantic fields account for the measured ID change; explicit operation/package scope limits.
- `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15,21,28` — projection and Rust path fields; full-envelope recomputation and controlled path-only substitution; bounded scope.
- `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:19,23` — nested inventory path changes the outer ID while top-level display-only mutation does not; bounded operation/target scope.

I checked these citation targets against immutable `HEAD` (`0436f4940283072db08e73c0117195847c50d31d`): the source files have respectively 26, 30, and 24 lines, and each cited line is in range. They use the `corpus/knowledge/<name>.md[:line[-line]]` form consumed by Command A (`SCORECARD.md:103-123`).

## First-hand re-derivation and verdicts

- **VERIFIED — baseline rule count.** Independently parsed the Queue-drain section from immutable `HEAD:SKILL.md`; the exact output was `HEAD rule_blocks=16`. This artifact alone does not change that count.
- **REPRODUCED — `inspect-evm-interface` projection.** Independently recomputed the canonical semantic digest from the eight retained full envelopes in `.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/probes/`. Same-path repeat IDs match; all three same-byte alternate-path comparisons retain equal carrier/decoded-bytecode/function payloads while IDs differ; changing only subject display fields preserves the ID.
- **REPRODUCED — `inspect_rust_binary` projection.** Independently recomputed all four retained envelopes in `.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/`. The same-path repeat is stable; same-byte copies at alternate paths differ; substituting only the measured semantic path fields reproduces the copy ID; display-only subject mutation leaves the ID stable.
- **REPRODUCED — `inspect_artifact` projection.** Independently recomputed all four retained envelopes in `.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/`. The same-path repeat is stable; the same-name, same-byte alternate path changes the outer ID; top-level display-only mutation leaves it stable, while changing only the nested inventory subject path changes the outer ID.
- **UNVERIFIABLE — post-integration `rule_blocks=17`.** Integration is outside this seat's write scope; the proposed rule has not been added to `SKILL.md`.

Re-derivation command (run from the repository root):

```bash
node .ufo/waves/arc3-loop1-round12/claims/c2/SC-4/evidence/recompute-projections.mjs
```

Exact output:

```text
r7: digest_matches=8/8; same_path_repeat=true; same_bytes_altpath_pairs=3/3; display_only_stable=true
r10: digest_matches=4/4; same_path_repeat=true; same_bytes_altpath_copies=2/2; path_fields_only_reproduce_copy=true; display_only_stable=true
r11: digest_matches=4/4; same_path_repeat=true; same_name_same_bytes_altpath_differs=true; outer_display_only_stable=true; nested_inventory_path_changes_outer_id=true
```

The verifier recomputes from retained envelopes; it does not execute any inspected target or make a fresh REA probe. Its code is included at `claims/c2/SC-4/evidence/recompute-projections.mjs`. No scratch was written to `/tmp`.
