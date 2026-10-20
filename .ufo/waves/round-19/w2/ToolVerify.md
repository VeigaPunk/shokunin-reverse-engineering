# Round-19 verifier audit — ToolVerify

Reviewed axes: freshness (C2), depth (C3), and calibration of the verifier's exit policy. Observed `refs/heads/main` at `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; baseline B is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.

## Findings

### High — C2's expected census failure can hide additional failures or scope drift

**Observation:** The amendment says the census must remain FAIL only on the two carried undeclared blocks, with stale/ambiguous/unresolved at zero and no SCOPE/DATED row added or widened (`.ufo/waves/round-19/claims.json:37-40`). The expected exit is correctly set to 1 in the table and execution plan (`.ufo/waves/round-19/verify.py:114,617-618`). But the post-run content check only searches for the four-count substring `stale=0 ambiguous=0 undeclared=2 unresolved=0` (`verify.py:684-687`). The gate's FAIL conditions also include scope errors, unreadable files, G2, G11, and frontier errors (`.ufo/gates/c1-census-v10.py:231-237,691-710`); its text output reports those independently (`:726-738`). The verifier does not assert those conditions are clean or compare the source SCOPE/DATED table to the baseline.

**Inference:** A gate run with those four counts unchanged but an additional scope/G2/G11/frontier/unreadable failure still exits 1 as expected and can satisfy the verifier's substring check. A scope-table change that leaves the four summary counts unchanged is also not rejected. The expected red result therefore does not establish the amendment's “only the carried undeclared blocks” or no-scope-widening conditions.

### High — Vet's expected exit 1 is checked, but its H1 discriminator is not

**Observation:** The decision rule requires a D label's bound log to report at least one H1-only invalid index and no index outside the frozen H1 list (`.ufo/waves/round-19/predictions/decision-rule.json:5,21-28`). The verifier correctly expects `compare-t1250-vet` to exit 1 (`.ufo/waves/round-19/verify.py:112,612-615`), but its content check only requires the list of mismatching field names to equal `["extra.invalid_index_reads"]` (`verify.py:688-690`). It does not inspect the mismatching field's predicted/observed values against the decision rule or assert the bound-log relationship for an existing observation file (`verify.py:577-615`).

The retained current vet result is consistent with the decision rule: `runs/t1250-vet/compare.exit:1`; `compare.json:2-3,51-60` has `all_match: false` and the sole mismatch is `extra.invalid_index_reads`, predicted `[13902080, 852107777, 1801722468838924630]` versus observed `[13902080]`; the H1-only set contains `13902080` (`decision-rule.json:21-25`). This validates the current expected exit, not the completeness of the verifier check.

**Bound-log cross-check:** The vet receipt's `bound_sessions` includes `rea-ghidra-CSKBVG`; `observation.json:79-81` names the corresponding retained Ghidra log and digest `a5de762231722468bcf265d5cd13ad9669f3a6d59a2746c73373e18a1a1a79c2`. `sha256sum` of that file returned the same digest, and `ghidra.log:229` reports `Invalid index: 13902080`. Thus the present retained result has the required binding and an H1-only value; the gap is that `verify.py` does not enforce this chain/value.


**Inference:** An observation containing only the shared walk index (H0-consistent), or an unsupported index, can produce the same sole mismatching field and satisfy `bad == ["extra.invalid_index_reads"]`. The verifier could then accept the expected exit without enforcing the amended H1 confirmation criterion. Check the actual observed values against the frozen H1/shared sets and ensure the compared observation is bound to the required retained log.

### Medium — `EXPECTED_EXITS` is descriptive, not authoritative

**Observation:** The table is documented as covering every command and refusing unplanned labels (`.ufo/waves/round-19/verify.py:85-86`), and `expected_for()` resolves it (`:169-176`). However, the full pass supplies expected exits as literals at its call sites (`:489-499,539-557,569-615,617-632`); it does not resolve those labels through `expected_for()`. The helper is exercised only by the selftest's sample cases (`:315-326`). A literal search for `expected_for` found only its definition and those selftest calls. The table is also copied into output as metadata (`:716`).

**Inference:** Changing a table entry does not change or fail the actual pass; changing a call-site expectation does not update or fail the table. An unplanned runtime label is not refused by the table as promised. The current C2 and vet table values (both 1) do match their call-site literals, but that agreement is not enforced.

## Exit calibration

No incorrect numeric expectation found for the two scoped commands:

- C2 `c1-census-v10`: exit 1 is consistent with the amended “FAIL on two carried undeclared blocks” claim and the gate's exit contract (`claims.json:39`; `c1-census-v10.py:231-237`).
- Vet `compare-t1250-vet`: exit 1 is consistent with the retained mismatch; `compare.py:228-245` returns 1 when any compared field mismatches, and the retained `compare.exit` is 1.

## Verification and gaps

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify refs/heads/main^{commit}` — **exit 0**; stdout `279e8b19c51658bfd05b9e31a1c0894ab2e70537`.
- Command: `python3 -I -B .ufo/waves/round-19/verify.py --selftest` — **exit 0**; `SELFTEST: CLEAN cases=2`.
- The full verifier and standalone C2 census were **not run**. No production files were edited and no mutation test was run.
- LSP status/references/definition/diagnostics were unavailable: `xd://lsp` returned “No such tool,” and the mounted-tool inventory had no LSP device. Source review used line-range reads; the literal `expected_for` search was only a fallback locator, not semantic proof.