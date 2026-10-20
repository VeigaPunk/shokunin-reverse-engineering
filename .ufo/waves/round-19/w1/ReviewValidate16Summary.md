# Validate16 summary and producer review

## Findings (by severity)

### Medium — validator identity is recorded and independently matches, but the closure check does not bind it

- **[Observation]** The summary records `validator_rev=9011581…` and `validator_sha256=618448…` (`.ufo/waves/round-18/evidence/validate16/summary.json:80-82`). I recomputed the hash from that Git-object path; it equals the recorded full hash (commands below). The producer reports it ran that pinned validator and gives the per-label commands/results (`.ufo/waves/round-18/w1/Validate16Run.md:3-5,46-58`).
- **[Observation]** The closure contract requires parseable summary, the expected receipt revision, 8 integer exits, and marker lines (`.ufo/waves/round-18/contract.md:33-35`). The implementation checks `validator_sha256` only for 64 hexadecimal characters and explicitly calls it “format only”; separately, it verifies each retained stdout file against its `stdout_sha256` (`.ufo/waves/round-18/tools/routed-defects.py:463-485`).
- **[Inference]** The observed artifact is correctly pinned to the stated validator bytes, but the closure check would not reject a different validator hash if it remained well-formed. Thus the evidence establishes the validator identity by this review's independent Git-object comparison and producer record, not by the gate itself.

### Low — receipt-copy reconstruction is deterministic only under fixed path and live-input conditions

- **[Observation]** The remap is exact prefix substitution in copied receipt JSON: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` → `/tmp/r17-validate16.MWZBce`, 16 occurrences per receipt, using byte-for-byte `str.replace`. The copied source tree is `git archive da64646 .ufo/waves/round-17`, plus `git show da64646:.ufo/waves/round-16/selection.py` (`.ufo/waves/round-18/w1/Validate16Run.md:17-30`; summary `:68-78`). The producer reports that the added `selection.py` has SHA-256 `6917da09…`, matching its pinned value (`Validate16Run.md:28-30`); my command below confirms the full digest.
- **[Observation]** The producer intentionally left carrier binaries, Ghidra typeinfo and esbuild `node_modules` paths live; `/tmp/kr17-rea-*` session-directory strings are needles in retained log content, not file reads (`Validate16Run.md:31-36`). The validator reads absolute paths and hashes the recorded files (`Validate16Run.md:19-22`).
- **[Observation]** The retained stdout digest is a digest of the stdout artifact, not of a remapped receipt: the sample stdout prints the temporary `pins_path` and `receipt` path (`.ufo/waves/round-18/evidence/validate16/calib-esbuild-0.25.12.stdout:8-21`). The eight current stdout files' SHA-256 values match the eight `stdout_sha256` values in the summary (`summary.json:2-65`), as shown below. The summary contains no digest for each rewritten receipt copy.
- **[Inference]** With the same Git revisions, exact source prefix, destination prefix, and unchanged live dependencies, the byte replacement is deterministic. A fresh `mkdtemp` path changes receipt path strings and stdout path strings, so recreated copies and stdout digests are not byte-identical by default. The report records one run; it does not report a second recreation-and-compare test. Since external files were not retained in the copy, the validation result is also not reproducible from the Git tree alone. Therefore end-to-end determinism is **not established**; it is conditional on a fixed destination and matching live inputs.

### No result-level contradiction observed

- **[Observation]** The summary has 8 receipts, each with `exit: 0`, `findings: []`, and `checks_performed: 341` (`.ufo/waves/round-18/evidence/validate16/summary.json:2-65`). The producer reports all eight per-label runs exited 0 and that it restored the missing pinned `selection.py` after the first run batch produced `missing_file` (`Validate16Run.md:9-15,28-30,53-58`). This review did not rerun the validator.

## Verification commands

Commands run read-only; each exited 0. The stdout hashes below match the summary entries in label order.

```text
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f  -
exit=0

$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-16/selection.py | sha256sum
6917da09fe61644a0e091e4e1763eda89c32db9de02aa29dad9d275cd50ef430  -
exit=0

$ sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/*.stdout
e3440b09f90a4bb8c510df973ab4de88d25fef8b43cb4024bb57b1e3489a5c72  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/calib-esbuild-0.25.12.stdout
21a3998938bba3862e9f48c7e719b061078b482cb025c311b2163905a49c23c0  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/calib-shfmt.stdout
0a013505ff51fd850458ee56603ae1a752dc1504dbee67c7535fd3429dd88038  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/pro-aether.stdout
f059df402642adc8d47a46b8e4b8768466779e9f298aee454f2365af15dd384f  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/pro-containerd-shim.stdout
1f12a1a8e50e4639a8af17416deb89cb0684c99b09adbdeff72210093f74a742  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/pro-esbuild-0.21.5.stdout
6ee30ebb79269192bd90ebc18b5f5b08072070d6606fd574a111c8f987bfd870  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/pro-esbuild-0.27.7.stdout
6d5bcc7d6ba7c87f475f1bb5a0deb72a7bfb5eef95a8d57b2d9ff9943ebcadaa  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/pro-notesmd-cli.stdout
ab2e90e80acda9d0a15bd264a96f0d46cfbb311aeafea74fd26fca4539c44562  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16/pro-op.stdout
exit=0
```

No tools installed.