# RV-6 — C3 pin-line drift characterization

## First-hand measurements

- **VERIFIED — live pin and match count.** Read-only extraction of only `rea-agents@` matches from `~/.kimi-code/config.toml`:

  ```text
  file_lines=4150 matches=1
  /home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  ```

  The independent pattern count also returned `1 total occurrence`. Thus, `:4126` is the sole `rea-agents@` match in the current Kimi config, and the pinned version is `6.7.0`.

- **VERIFIED — the instrument grades the live pointer `current-ok`.** I ran `python3 .ufo/gates/c1-census-v10.py --root .` against the current repository. Relevant output:

  ```text
  live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
  PROVINCE.md block 15-26 [scope CURRENT]
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
  ```

  This is an assertion-level `current-ok` result; the containing block is rendered under `INFO` because it mixes current and historical assertions.

- **DISCREPANCY — the overall gate run is not PASS.** The same invocation exited `1` and printed:

  ```text
  -- UNDECLARED (1) --
    SCORECARD.md block 1833-1839 [scope None]
        :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
  DECLARED FAIL CLASSES: []
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
  ```

  The pointer assertion itself is current-ok, but the complete instrument result must not be reported as PASS. The independently observed blocker is the out-of-scope pin at `SCORECARD.md:1834`, outside the gate's declared SCORECARD range (`.ufo/gates/c1-census-v10.py:264-276`).

- **VERIFIED — captured config layouts show the line is mutable.** I counted exact `rea-agents@` regex matches in each extant `~/.kimi-code/config.toml*` file and recorded their physical lines; each file had exactly one:

  ```text
  config.toml: count=1 lines=[4126]
  config.toml.20261018-085645.bak: count=1 lines=[2915]
  config.toml.20261018-114557.bak: count=1 lines=[2932]
  config.toml.20261018-143236.bak: count=1 lines=[2940]
  config.toml.20261018-145016.bak: count=1 lines=[3227]
  config.toml.20261018-150133.bak: count=1 lines=[3298]
  config.toml.20261018-161746.bak: count=1 lines=[3298]
  config.toml.20261018-201656.bak: count=1 lines=[3157]
  ```

  This directly establishes positional variation across available snapshots, not a complete edit-by-edit chronology. No available `config.toml*` snapshot had a match at `3546`; a current read-only gate `ptr_check('~/.kimi-code/config.toml', 3546, live_pins())` returned `('stale', "line holds no rea-agents pin: 'max_output_size = 64000'")`. I cannot independently verify from these snapshots that `3546` was once the live pin line, so I do not use that historical state as evidence.

- **REPRODUCED — inserting lines makes an old pointer stale; re-anchoring restores it.** I passed a minimal scratch-only config (the live pin line under `[mcp_servers.rea]`) to the gate's `ptr_check`; then prepended two lines in a `TemporaryDirectory` under `/var/tmp` (no live-config edit):

  ```text
  fixture: only stanza/pin line copied; live-version=6.7.0
  before-edit pointer-line=2 -> ('ok', 'pins 6.7.0')
  after-two-line-insert old-pointer-line=2 -> ('stale', "line holds no rea-agents pin: '# inserted B'")
  after-two-line-insert re-anchored-line=4 -> ('ok', 'pins 6.7.0')
  ```

## Characterization

The perishable item is the **line-number pointer**, not necessarily the package version: inserting/removing material before the stanza moves the target line while the `rea-agents@6.7.0` value can remain unchanged. The stored pointer does not follow the stanza automatically; it must be re-anchored. The gate reads exactly the referenced line, returns stale when that line has no pin or a different live version, and returns unresolved if the target is unreadable or beyond EOF (`.ufo/gates/c1-census-v10.py:466-482`). It applies that check to pointer assertions at `.ufo/gates/c1-census-v10.py:538-544`.

## Identity and scope

Fresh identity checks: `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`; `sha256sum .ufo/gates/c1-census-v10.py` → `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`; `wc -l` → `716`. The gate's live-anchor extraction is at `.ufo/gates/c1-census-v10.py:324-334`. No live config, gate source, corpus, or other tracked file was changed; the only deliverable is this RV-6 artifact.
