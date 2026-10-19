# RV-5 — C3 pin-line drift characterization

## Measurement scope

Re-derived on checkout `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. The gate read was `.ufo/gates/c1-census-v10.py`, SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4` (716 lines). No operator config, gate, PROVINCE, or corpus file was changed. The line-shift control used a synthetic config under `/var/tmp`, then removed it.

## Per-item findings

- **VERIFIED — the current Kimi config has one pin occurrence, at line 4126.** A focused search of `/home/vgpnk/.kimi-code/config.toml` returned `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`; the focused-search count was `Found 1 total occurrence across 1 file.` An independent byte-line scan returned:

  ```text
  file_lines=4150 bytes=135709 matches=1
  4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  line_sha256_no_eol=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
  ```

- **VERIFIED — the live pointer is graded `current-ok` by the instrument.** A fresh `python3 .ufo/gates/c1-census-v10.py` run printed live anchors `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}` and, in the `PROVINCE.md` block `15-26`, the assertion `:18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)`. This is an assertion-level result: that mixed block is listed under `INFO`, not aggregate `CURRENT-OK`. Its line reference is `.ufo/gates/c1-census-v10.py:538-544`; the evaluator reads the nominated file and line and compares the extracted version with the client live anchor at `:466-483`.

- **VERIFIED — current uniqueness; not a gate-enforced uniqueness invariant.** The live file had one `rea-agents@` occurrence in the focused search and in the independent scan. The gate's `live_pins()` uses `re.search()` per config (`.ufo/gates/c1-census-v10.py:324-334`), while `ptr_check()` checks the nominated line (`:466-483`); neither performs a whole-file uniqueness check. Thus “only match” is confirmed for this capture, not guaranteed by the instrument for future config contents.

- **REPRODUCED — a line-number pointer does not follow an insertion.** I imported the current gate and exercised its `classify()`/`ptr_check()` on synthetic `PROVINCE.md:18` units, using the current live anchors. Starting with a synthetic `config.toml` whose pin was line 1, pointer `:1` was `current-ok (pins 6.7.0)`. Inserting one comment above that pin made the unchanged `:1` pointer `STALE (line holds no rea-agents pin: '# operator edit inserted above the REA pin')`; re-keying to `:2` returned `current-ok (pins 6.7.0)`. The exact probe result was:

  ```json
  {"baseline_config_line1":[{"disp":"current-ok","line":18,"value":"/var/tmp/kaidoku-rv5-pin-drift-meczp3bt/config.toml:1","why":"pins 6.7.0"}],"shift_inserted_old_pointer_line1":[{"disp":"STALE","line":18,"value":"/var/tmp/kaidoku-rv5-pin-drift-meczp3bt/config-shifted.toml:1","why":"line holds no rea-agents pin: '# operator edit inserted above the REA pin'"}],"shift_inserted_rekeyed_pointer_line2":[{"disp":"current-ok","line":18,"value":"/var/tmp/kaidoku-rv5-pin-drift-meczp3bt/config-shifted.toml:2","why":"pins 6.7.0"}]}
  ```

  This establishes the tested drift class: the stored line number is positional and must be re-derived/re-keyed after edits that move the pin; it is not an auto-following locator. The test used a synthetic file, not an edit to operator config. Scratch was `/var/tmp/kaidoku-rv5-pin-drift-meczp3bt` and was removed (`scratch_removed=True`).

- **DISCREPANCY — the whole census invocation is not PASS.** The same unmodified gate command exited 1 and printed `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`. The unrelated blocker is `UNDECLARED` `SCORECARD.md` block `1833-1839`, assertion `:1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)`; the pointer assertion above still graded `current-ok`. This seat did not alter the gate or its scope.

## Conclusion

The live pin is currently a unique `rea-agents@` match at Kimi config line 4126 and the gate grades the `PROVINCE.md:18` pointer `current-ok`. The perishable value is the numeric line location: an insertion above it makes the old pointer stale until re-keyed. The gate validates the pointed-to line/version, but does not enforce that the config contains only one pin. Whole-gate PASS is not established because of the separate undeclared SCORECARD locus reported above.
