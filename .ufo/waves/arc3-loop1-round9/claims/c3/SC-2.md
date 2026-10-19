# SC-2 — C3 pin-line drift characterization

## Verdicts

- **REPRODUCED — live Kimi pin:** a fresh grep and an independent script read found one `rea-agents@` match in `~/.kimi-code/config.toml`, at line 4126: `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. The exact output and fresh line hashes are in `SC-2/evidence/live-pin-drift-receipt.txt`.
- **REPRODUCED — pointer is current-ok:** the v10 gate independently derived Kimi 6.7.0 and classified the pointer at `PROVINCE.md:18` (`~/.kimi-code/config.toml:4126`) as `current-ok (pins 6.7.0)`. Its containing block is `info`, not `current-ok`, because that block also has historical assertions; the assertion-level result is explicit in the receipt. Gate source identity: SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`.
- **REPRODUCED — positional drift:** in a temporary copy under `/var/tmp`, inserting one line before the pin moved its line from 4126 to 4127 while the live pin remained 6.7.0. `ptr_check()` rejected the old line as stale and accepted the re-anchored line. This establishes that the pointer is perishable under preceding-line edits; it does not establish behavior for every possible config rewrite. The original config was not edited.
- **DISCREPANCY — overall gate:** `python3 .ufo/gates/c1-census-v10.py` exits 1 / reports FAIL at this HEAD, despite the tested PROVINCE assertion being current-ok. Its JSON summary has `undeclared=1`: the new pin-containing record at `SCORECARD.md:1833-1839` is beyond the last declared SCORECARD scope ending at line 1813 (`.ufo/gates/c1-census-v10.py:276`). No SCORECARD or gate change is within this seat's write scope, so this remains for integration to resolve.

## Characterization

The live package version and the cited physical line are separate values. The instrument's anchor reads the first `rea-agents@x.y.z` occurrence in each client config (`.ufo/gates/c1-census-v10.py:324-334`); its pointer check then opens the named file and line, requires a pin there, and for the Kimi path compares that version with the live anchor (`:466-482`). In the measured insertion, the package value stayed constant but the pointer's line number became stale. The current file had exactly one matching line, so the first-match anchor is unambiguous at measurement time; this does not census other client configs or establish uniqueness after future edits.

The full direct grep, gate disposition, aggregate FAIL detail, and synthetic before/after output are preserved in `SC-2/evidence/live-pin-drift-receipt.txt`. The reusable read-only re-derivation and scratch-copy experiment is `SC-2/evidence/rederive_drift.py`. This measured receipt note records the drift class without changing the canonical corpus or any custody file.

## Scope and verification

This seat wrote only its SC-2 artifact directory. The config was read-only; the synthetic edit existed only in a temporary `/var/tmp` copy. No `/tmp` scratch, Git mutation, canonical corpus, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, or gate-source edit was made. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched. The v10 gate was run against HEAD and returned FAIL for the separate undeclared SCORECARD locus described above.
