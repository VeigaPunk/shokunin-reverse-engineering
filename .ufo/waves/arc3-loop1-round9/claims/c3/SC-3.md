# SC-3 — live REA pin-line drift characterization

Claim: c3 calibration, re-derived against the live config and the current census gate. The config was not edited; the drift test used isolated synthetic HOME/config fixtures in `/var/tmp`.

## Findings and verdicts

- **Live Kimi pin and location — VERIFIED.** A targeted occurrence search of `~/.kimi-code/config.toml` returned exactly one match. Stanza context:
  ```text
  /home/vgpnk/.kimi-code/config.toml:4124:[mcp_servers.rea]
  /home/vgpnk/.kimi-code/config.toml:4125-command = "npx"
  /home/vgpnk/.kimi-code/config.toml:4126-args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  ```
  The occurrence-count result was `Found 1 total occurrence across 1 file.` The live line and its uniqueness were derived from the current config, not from the prior receipt. The receipt path is `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt`.
- **Census grading of the live pin and pointer — VERIFIED at assertion level.** On freshly measured HEAD `947091d`, the live run reports the pin and its pointer at `PROVINCE.md:18` as `current-ok`:
  ```text
  live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
  PROVINCE.md block 15-26 [scope CURRENT]
      :18 [pin] kimi=6.7.0 -> current-ok (matches live kimi)
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
  ```
- **Overall gate PASS — DISCREPANCY.** The same real-tree run exits 1 and ends `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`. Its single undeclared item is `SCORECARD.md:1834` (`rea-agents@6.7.0` without a client token, outside the declared census ranges). This is separate from the verified `PROVINCE.md:18` assertions; do not report the aggregate gate as PASS.
- **Line-position drift behavior — REPRODUCED in scratch.** The gate dynamically reads each configured pin value, but a `path:line` pointer is resolved at the literal line recorded in the province. In an isolated HOME with the same Kimi version at line 4126, the pin and pointer assertions were both `current-ok`. In a fixture with one comment inserted before the pin (pin moved to 4127), the gate still derived Kimi `6.7.0`; the pin remained `current-ok`, while the unchanged pointer to line 4126 became `STALE (line holds no rea-agents pin: '# isolated drift fixture')`. Thus the line number does not auto-follow config edits; the instrument detects this positional drift.
- **Version re-anchor behavior — REPRODUCED with a caveat.** In another isolated fixture, changing the configured pin to `6.7.1` at line 4126 changed the gate's derived `live.kimi` to `6.7.1`, and the pointer assertion then read `current-ok (pins 6.7.1)`. However, the unchanged `PROVINCE.md:18` `6.7.0` pin assertion was classified `historical (inline marker)`, not `STALE`: the line itself contains historical-receipt wording, and the instrument's line-scoped inline-marker rule permits that classification (gate `INLINE_MARKER` at `:315`; classification at `:518-521, :559-563`). This is a masking edge in addition to the positional pointer behavior.

## Reproduction details

Live-tree commands/evidence:

- Read-only stanza/occurrence search on `~/.kimi-code/config.toml`: output above; count was one.
- `python3 .ufo/gates/c1-census-v10.py` from the repo root: output excerpt above; aggregate verdict and failure location above.
- `git rev-parse --short HEAD` returned `947091d`.
- The tested `.ufo/gates/c1-census-v10.py` SHA-256 was `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`.

For the drift test, the gate was invoked with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` and HOME set to separate fixtures under `/var/tmp/kaidoku-r9-sc3-3dnj_8h8` (the real config remained untouched):

```text
baseline-4126 exit=1
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
      :18 [pin] kimi=6.7.0 -> current-ok (matches live kimi)
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)

shifted-4127 exit=1
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
      :18 [pin] kimi=6.7.0 -> current-ok (matches live kimi)
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> STALE (line holds no rea-agents pin: '# isolated drift fixture')
VERDICT: FAIL  (stale=1 ambiguous=0 undeclared=1 unresolved=0)

version-6.7.1 exit=1
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.1'}
      :18 [pin] kimi=6.7.0 -> historical (inline marker)
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.1)
```

Implementation basis: `c1-census-v10.py:324-334` derives `live_pins` from config contents; `:466-482` dereferences the literal pointer line; `:559-563` grades a mismatching pin historical when its physical line has an inline marker. No custody config, gate source, corpus, province, scorecard, skill, or log was changed by this seat.
