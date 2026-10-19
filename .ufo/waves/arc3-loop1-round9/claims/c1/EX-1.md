# EX-1 — C1 freshness: PROVINCE pacman row

Chain: `c1` (freshness). Measurement performed against repository HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. This artifact proposes text only; `PROVINCE.md`, the census gate, and all tracked files were left unchanged.

## First-hand re-derivation

Commands run from the lane repository:

```text
$ grep -n "1556" PROVINCE.md
50:| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true in live session`); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |

$ grep -n "Archive/package inventory" PROVINCE.md
50:| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true in live session`); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |

$ printf 'archive files: '; ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
archive files: 1350
$ printf 'signature files: '; ls /var/cache/pacman/pkg/*.sig | wc -l
signature files: 1350
$ printf 'PROVINCE lines: '; wc -l < PROVINCE.md
PROVINCE lines: 162

$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-19T18:19:35Z
$ grep -n 'rea-agents@' "$HOME/.kimi-code/config.toml"
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]

$ pacman -Q jq
jq 1.8.2-1
$ pacman -Qkk jq
jq: 25 total files, 0 altered files
$ sha256sum /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
$ tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
```

The live archive and `.sig` counts both re-derived to 1,350. Subtracting the dated text value gives `1,350 - 1,556 = -206`; the `1,556` historical count itself is not independently reproducible from the present cache, so I treat it as a dated record, not as a fresh observation. The dated erratum for discoverability is `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`; the live count and equality checks above are this seat's observations.

## Proposed same-line patch text (not applied)

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true in live session`); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 record; current live count 1,350 as of 2026-10-19, delta −206 vs recorded baseline; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
```

Scratch-only validation under `/var/tmp` applied that exact replacement to a copy of the current three census inputs: `scratch_PROVINCE_lines=162`. This is line-neutral; the real `PROVINCE.md` remains 162 lines and unmodified.

## Whole-row perishable census

| Row content | Verdict | Evidence / boundary |
|---|---|---|
| `1556 signed archives` | **CORRECTED** as a current count; proposed text retains it only as the 2026-10-13 record and adds the independently observed live count and delta. | Current command output above: 1,350 archive files and 1,350 `.sig` files. The historical 1,556 baseline is reported by the dated source but cannot be re-measured on today's cache. |
| `available:true in live session` | **UNVERIFIABLE** as a current availability claim in this seat. The Core table heading (`PROVINCE.md:40`) dates its surface verifications to 2026-10-13, and the cell says this was a live-session observation; I had no REA MCP-session tool to re-probe it. Do not infer present availability from the old observation. | `PROVINCE.md:40,50`; the local census's REA configuration anchors do not establish a live MCP session. |
| `installed jq verified byte-identical to signed archive member` | **VERIFIED** now. | `pacman -Q jq` reports `jq 1.8.2-1`; `pacman -Qkk jq` reports 25 files / 0 altered; installed and archived `/usr/bin/jq` SHA-256 outputs are identical (`e8156675…`). |
| `.MTREE` per-file sha256; `pacman -Qkk` verify; `binary_session {}` capabilities | **No additional perishable scalar found.** These identify a metadata format, verification command, and capability probe rather than asserting another live count/version. | Direct census of all four cells in the single physical row at `PROVINCE.md:50`. |

## Census-gate result / disposition

Ran the live instrument, `python3 .ufo/gates/c1-census-v10.py`, before any patch and ran the same instrument with the proposed row in a `/var/tmp` scratch root. Both return exit 1. The exact relevant live output is:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

The scratch run preserves the same failure and line count:

```text
scratch_PROVINCE_lines=162
scratch_gate_exit=1
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

**DISCREPANCY / cannot verify PASS held:** the current gate's declared SCORECARD scope ends before the current `:1834` locus, so the gate is already FAIL independently of the PROVINCE row patch. This seat did not edit the protected gate or SCORECARD. Consequently I can verify the candidate is line-neutral and adds no observed gate finding, but cannot report the required overall `PASS` after patch; integration must resolve the out-of-scope locus within authorized scope before claiming that criterion.
