# SC-4 — C3 pin-line drift measurement

Scope: independently re-derive the live Kimi REA pin, inspect the current census-gate disposition, and test the gate's line-pointer behavior without editing the live config. All config reads were read-only; the drift probe used a temporary config copy under `/var/tmp`.

## Live pin — REPRODUCED

A content search for `rea-agents@` in `/home/vgpnk/.kimi-code/config.toml` returned exactly:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

Independent read-only Python census output:

```text
config path: /home/vgpnk/.kimi-code/config.toml
line count: 4150
rea-agents@ line count: 1
version tokens: ['6.7.0']
match: 4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
977da8727fff68f0a9a139ebdde7e01f09fb3557378990815ac7d7e2d0e583a9  /home/vgpnk/.kimi-code/config.toml
```

The one observed match is the only current `rea-agents@` occurrence in this file. The measurement is bound to config SHA-256 `977da8727fff68f0a9a139ebdde7e01f09fb3557378990815ac7d7e2d0e583a9` (read-only `sha256sum`).

## Instrument disposition — REPRODUCED for the pin; global gate DISCREPANCY

Source identity at measurement: `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`; `sha256sum .ufo/gates/c1-census-v10.py` → `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`.

Command: `python3 .ufo/gates/c1-census-v10.py --root .` (exit status 1). Relevant exact stdout:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6

-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)

-- INFO (8) --
  PROVINCE.md block 15-26 [scope CURRENT]
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)

SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
G11 current-ok without receipt language: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

Thus the requested pointer is specifically `current-ok`. Do not report the whole census as PASS: the same run fails on the independent undeclared `SCORECARD.md` block shown above. The pointer logic is at `.ufo/gates/c1-census-v10.py:466-482` (`ptr_check` dereferences the physical line, requires a pin there, then checks the client live version); live anchors are obtained at `:324-334`.

## Drift class — REPRODUCED on isolated copies

I imported the checked-in gate, obtained its `live_pins()`, and called its `ptr_check()` first against the actual read-only path, then against temporary copies named `config.toml` under `/var/tmp`. The probe inserted only an inert TOML comment; it did not write the live config.

Exact output:

```text
gate source: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py
live anchors: {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
actual pointer 4126 -> ('ok', 'pins 6.7.0')
temp copy, inserted one inert line before target: old pointer 4126 -> ('stale', "line holds no rea-agents pin: '# inert drift probe'")
temp copy, inserted one inert line before target: re-anchored pointer 4127 -> ('ok', 'pins 6.7.0')
temp copy, inserted one inert line after target: unchanged pointer 4126 -> ('ok', 'pins 6.7.0')
```

Characterization: this is a mutable physical-line pointer, not a stable stanza/key anchor. A net line insertion before the pin moves the pin and makes the old pointer stale; the pointer must be re-anchored to the new line. Edits after the pin do not move its line. The gate independently checks the version at that line against the current Kimi anchor. The current single-match census also means `live_pins()`'s first-match search is unambiguous for this config now; behavior with duplicate future matches was not exercised.

**C3 seat result:** REPRODUCED for the live pin, its `current-ok` gate disposition, and the line-sensitive drift class. **Global-gate caveat:** DISCREPANCY/FAIL remains due to the separate undeclared `SCORECARD.md` locus; no out-of-scope file was changed to mask it.
