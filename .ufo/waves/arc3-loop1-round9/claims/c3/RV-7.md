# RV-7 — C3 pin-line drift characterization

**Disposition:** the live pin is **VERIFIED**; its gate grading is **REPRODUCED**; pin-locator movement is **REPRODUCED** in a scratch-only edit and corroborated by retained config snapshots. The gate’s *overall* run is **DISCREPANCY / FAIL**, for an unrelated undeclared SCORECARD locus. No operator config, gate, PROVINCE, corpus, or tracked file was edited.

## First-hand re-derivation

- `Grep(pattern="rea-agents@", path="/home/vgpnk/.kimi-code/config.toml")` returned exactly one result:

  ```text
  /home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  ```

  `wc -l /home/vgpnk/.kimi-code/config.toml` returned `4150 /home/vgpnk/.kimi-code/config.toml`. Thus the currently observed file has one matching `rea-agents@` line, at 4126, pinning 6.7.0. This is a targeted literal search, not a claim that no differently spelled or indirect provider reference exists.

- Read-only `Grep(pattern="rea-agents@", path="/home/vgpnk/.kimi-code", glob="config.toml*")` returned the following current-file and backup hits (one hit per listed path):

  ```text
  /home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-201656.bak:3157:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-161746.bak:3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-150133.bak:3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-085645.bak:2915:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-145016.bak:3227:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-143236.bak:2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  /home/vgpnk/.kimi-code/config.toml.20261018-114557.bak:2932:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  ```

  These observed snapshots hold the same pin text/version while its physical line varies, including a non-monotonic move (3298 to 3157). Snapshot positions establish locator volatility, not the cause or exact edit history of each movement.

- The checked-in pointer is `PROVINCE.md:18`: `~/.kimi-code/config.toml:4126`. The current gate source is SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4` (measured with `sha256sum .ufo/gates/c1-census-v10.py`). Its `ptr_check()` reads the named physical line and validates the version against the live anchor (`.ufo/gates/c1-census-v10.py:466-482`); `classify()` maps a successful pointer check to `current-ok` (`:538-545`).

- Ran the unmodified instrument: `python3 .ufo/gates/c1-census-v10.py`. Decisive output:

  ```text
  live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
  PROVINCE.md    lines=162  loci=6
  SCORECARD.md   lines=1870 loci=11
  SKILL.md       lines=413  loci=2
  -- UNDECLARED (1) --
    SCORECARD.md block 1833-1839 [scope None]
        :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
  -- INFO (8) --
    PROVINCE.md block 15-26 [scope CURRENT]
        :18 [pin] kimi=6.7.0 -> current-ok (matches live kimi)
        :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
  SCOPE-ERRORS (marker assertions): []
  FRONTIER register (G21): 14 rows asserted, errors: []
  UNREADABLE (could-not-evaluate): []
  G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
  G7 configured!=held warnings: []
  G11 current-ok without receipt language: []
  DECLARED FAIL CLASSES: []
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
  ```

  **REPRODUCED:** the target locator at `PROVINCE.md:18` is evaluated `current-ok`. **DISCREPANCY:** the whole instrument is not PASS; it exits 1 because the newly present `SCORECARD.md:1833-1839` block is outside declared scope. This does not negate the pointer-level disposition.

## Drift mechanism

Ran the actual gate `classify()` and `ptr_check()` on a disposable `/var/tmp/kaidoku-rv7-*` fixture containing only the observed pin line; inserted three comment lines *in the fixture only*. Output:

```json
{"fixture_only": true, "initial_pin_line": 1, "initial_pointer_disposition": "current-ok", "inserted_lines": 3, "moved_pin_line": 4, "old_pointer_disposition_after_insert": "STALE", "updated_pointer_disposition_after_insert": "current-ok"}
```

**REPRODUCED:** the locator is a physical line number, not a stable key. An edit before the pin leaves the pin text/version unchanged but makes a retained old pointer stale; re-keying the pointer to the moved line restores `current-ok`. The gate re-derives the version anchor, but a document pointer still has to track the line. This test changed no operator-owned file. The actual edit cause for each archived snapshot remains **UNVERIFIABLE** from line-only matches; the fixture establishes the mechanism, not those historical causes.

## Verdicts

- **VERIFIED — current match/line:** exactly one `rea-agents@` hit was returned in the current Kimi config, at line 4126, `6.7.0`.
- **VERIFIED — retained snapshot positions:** current + seven discovered backups each returned one identical pin line at the positions quoted above; the observations show that the line coordinate is mutable even when the pin string stays constant.
- **REPRODUCED — instrument disposition:** current `PROVINCE.md:18` pointer is `current-ok` in the unmodified live gate run.
- **REPRODUCED — edit sensitivity:** a three-line insertion before the pin in `/var/tmp` moves its locator and causes the former pointer to grade `STALE`; the corrected fixture pointer grades `current-ok`.
- **DISCREPANCY — instrument-wide verdict:** exit 1 / FAIL from `SCORECARD.md:1833-1839` undeclared scope, independently of the successfully graded Kimi pointer.
- **UNVERIFIABLE — exact historical edit causes / same-round zero-drift:** backups expose line positions, not edit diffs; no same-round pre-pair predates this seat’s initial read. I make no zero-config-drift claim.

**Identity:** `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. Gate SHA above was re-derived from the current file. All inspection was read-only; scratch was confined to `/var/tmp` and automatically removed.
