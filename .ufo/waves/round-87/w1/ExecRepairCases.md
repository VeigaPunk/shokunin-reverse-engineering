# ExecRepairCases (executor) — R87-C1 report

- Candidate: `.ufo/waves/round-87/w1/ExecRepairCases/candidate/upx-magic-repair.py`, sha256 `c2083af51712080e4bf196300aef576df14a0e9537e8bd9fb9ec7f3ed0e4fdca` (base b5c7a49e `f4ebd152…`). Diff: `ExecRepairCases/receipts/candidate.diff`.
- Selftest: `SELFTEST cases=33 failures=0` (9 original + 24 new structural edge cases; `receipts/selftest.txt`).
- Production-logic change, named "mixed-method chain": a b_info block's method may equal the first block's **or the PackHeader method**. Changed lines in the candidate: L70, L75-81, L92, L109-116, L123-126, L143. This fixes the out-of-population refusal on libz packed `--lzma` / `--best --brute` (an NRV2B first block followed by LZMA blocks).
- Frozen counter, `--no-rea` (`ExecRepairCases/counter-norea.json`, counter sha `0f2d2bd8…`): in all 8 cases repair_rc0, windows_only, test_ok and identity are true. `rea_recover` is false only because REA is disabled, so the label reads `recovered 0 of 8`, as expected. Controls N1, N2 and N3 are all true. The results match the run before the fix.
- Out-of-population probe (`-1`, `--lzma`, `--best --brute`, plus a `--best` baseline; T1 and T2): candidate 32/32 rows pass `upx -t` and `upx -d` identity, base tool 28/32. Table in `ExecRepairCases/notes.md`.
- Findings:
  - (a) jq and xxd `--best` carry a 4th `UPX!` inside the loader that the repair does not restore. Test and identity still pass; repaired ≠ packed bytes.
  - (b) Tampered executables still run normally, so execution does not discriminate repaired from tampered files.
  - (c) N2 is enforced by upx, not by the repair, which returns rc 0 on those inputs.
  - (d) Of 5369 plain ELFs, 10 have a chance-valid PackHeader window, and the repair accepts 0 of them.
- Risks: the mixed-method rule widens plausibility by one method value. No plain-ELF false accept appeared. The REA arm was not run by this seat.
- Tools installed: none. Frozen files untouched; no VCS mutation; scratch removed.
