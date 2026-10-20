# ProvincePins review — C2 pin-token slice

## Findings by severity

**No actionable finding in the assigned pin-token scope.** The live configured tokens match the current statements at the reviewed revision.

## Observations

- **[OBS] Live config tokens, reopened without printing secret values:** targeted JSON/TOML parsing located exactly one token in each REA entry's `args[1]`: Devin `/home/vgpnk/.config/devin/mcp_config.json:7` → `rea-agents@6.7.0`; OMP `/home/vgpnk/.omp/agent/mcp.json:8` → `rea-agents@6.7.0`; Kimi `/home/vgpnk/.kimi-code/config.toml:4126` → `rea-agents@6.7.0`. The pin probe reported all three files present, each with a single distinct token; their observed mtimes were Devin/OMP `2026-10-20T16:35:56Z` and Kimi `2026-10-19T19:09:51Z`. No config secret contents were emitted.
- **[OBS] Current statements match those tokens:** `PROVINCE.md:8-13` states all three current registrations are `6.7.0`; `PROVINCE.md:15-26` gives Devin, OMP, and Kimi configured pins as `6.7.0`; `PROVINCE.md:44` gives Devin/OMP/Kimi `6.7.0`. `SKILL.md:18-20` likewise states Devin/OMP and Kimi are `6.7.0`. The separate `6.5.0` carrier CLI pin in `PROVINCE.md:10` and historical `6.4.0` mention in `PROVINCE.md:11` / `SKILL.md:20` are explicitly distinguished from current client pins.
- **[OBS] Baseline-to-delivered probe:** at baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`, `mismatch_count=2`: Devin `6.5.0` at PROVINCE lines 9, 16, 44; OMP `6.5.0` at lines 9, 17, 44. At delivered tip `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, `mismatch_count=0`, `unstated_clients=[]`; the three live tokens are unchanged between the two probe runs.
- **[OBS] Commands and program exit codes** (`province-pins.py` reads the selected PROVINCE blob from Git and the current config files; see `.ufo/waves/round-19/tools/province-pins.py:203-231,244-319,639-670`):

  ```text
  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
  exit 0; mismatch_count=2

  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41
  exit 0; mismatch_count=0

  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
  exit 1; mismatch_count=2

  python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
  exit 0; mismatch_count=0
  ```

  The non-strict command's exit 0 does **not** mean its mismatches are zero; per `province-pins.py:41-44,646-669`, the count is informational unless `--strict` is supplied.

## Residual risk and verification gaps

- **[LIMITATION]** The pin probe identifies distinct `rea-agents@X.Y.Z` strings across each whole config file; it does not itself parse the JSON/TOML registration structure or prove that a running client has reloaded the file (`province-pins.py:203-231`). The separate targeted parse above verified the tokens are under each `rea` entry's `args[1]`, but no client runtime was started. This slice makes no runtime readiness, routing, same-identity rerouting, or saturation claim.
- **[LIMITATION]** The probe's three-region scan covers PROVINCE, not SKILL; `SKILL.md:18-20` was compared directly and matches, but future SKILL drift is not caught by this probe.
- **[GAP]** No LSP device was mounted (`xd://lsp` returned “No such tool”); no LSP references/definition/diagnostics were available. No grep was used as semantic proof. No build, broad suite, REA/Ghidra run, or production edit was performed; only this report is written.