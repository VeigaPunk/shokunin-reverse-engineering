# Province doctor review — round 19 wave 2

Axes: **freshness** (primary); calibration/depth are outside this assignment.

## Findings (severity ordered)

### Low — Kimi pin is presented as a registration without disclosing the doctor’s contrary status

**Observation:** `PROVINCE.md:8-11` says the per-client surfaces “resolve” and that Devin, OMP, and Kimi “all register” `rea-agents@6.7.0`. The accompanying pin evidence establishes a narrower fact: `evidence/province-pins-integrated.json:28-37` records the Kimi config file `/home/vgpnk/.kimi-code/config.toml` as existing with a `rea-agents@6.7.0` pin. Its `rules` at `:60-65` describe textual stated-pin/live-pin comparison, not a doctor-recognized registration or a live client session.

The 6.7.0 doctor snapshot is `audit-wide` (`evidence/doctor/doctor-6.7.0.txt:1-9`) and its registration inventory explicitly reports Kimi `state: missing`, `command: []`, at `/home/vgpnk/.kimi-code/mcp.json` (`:337-341`). The doc instead cites `config.toml` (`PROVINCE.md:17-18`). Devin and OMP are explicitly `aligned` in that same 6.7.0 inventory (`:315-319`, `:342-347`).

**Inference:** The pin is current, but the unqualified word “register” blurs “a config file contains this pin” with “REA doctor recognizes this client registration.” Readers could infer Kimi has the same doctor-validated status as Devin/OMP. Keep the pin claim scoped to the config file and state that this doctor snapshot reports Kimi missing; the differing config paths are material. This finding does **not** establish that Kimi cannot use the config.toml registration at runtime.

The narrower sentence `PROVINCE.md:24` / table row `:44`—that 6.7.0 has no Devin/OMP registration finding and 6.5.0 reports their 6.7.0 requests—is supported: the 6.7.0 inventory marks Devin/OMP aligned, while the 6.5.0 inventory marks them stale (`evidence/doctor/doctor-6.7.0.txt:315-319,342-347`; `doctor-6.5.0.txt:336-341,363-368`).

## Residual risk

- There is no whole-environment-healthy conclusion in the changed doctor wording. Both retained outputs say `healthy: false` and `environment_healthy: false` (`evidence/doctor/doctor-6.5.0.txt:1-2`; `doctor-6.7.0.txt:1-2`). The 6.7.0 capture is audit-wide, has 21 scoped checks with 10 failing, and includes seven missing registrations (including Kimi); it must not be summarized as environment health merely because Devin/OMP have no registration finding.
- The registration inventories each have 13 rows. The 6.5.0 capture has 5 stale, 7 missing, 1 manual; 6.7.0 has 5 aligned, 7 missing, 1 manual. Scope-check denominators differ (26 versus 21), so aggregate failure-count change alone is not a like-for-like measure.
- These are versioned doctor snapshots, not live-client attestations. Both say `live_server.state: unknown` and direct the operator to `binary_session` (`doctor-6.5.0.txt:303-305`; `doctor-6.7.0.txt:282-284`). `PROVINCE.md:28-35` already distinguishes the environment verdict from the live-server verdict; retain that boundary.

## Verification gaps

- The LSP route is unavailable in this session: reading `xd://lsp` returned “No such tool.” No LSP references/definition/diagnostics were available; I used direct anchored reads, not grep.
- No live doctor or `binary_session` was run. Conclusions are bounded to the retained round-19 outputs and pin evidence above. No production edits, mutation tests, build, or broad suite were run.

## Commands and exit codes

Observed main tip:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
=> d0690fd44f46d8a7fe9da5f01c6be723d12abd41
exit 0
```

Reviewed the Province change from the declared round-19 baseline:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=0 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- PROVINCE.md
exit 0
```

Counted retained doctor scopes and registration-state categories (read-only):

```text
python3 -I -B -c 'from pathlib import Path
import sys
for name in sys.argv[1:]:
 lines=Path(name).read_text().splitlines()
 scope=False; checks=failures=0; regs={}; active=False; client=None
 for line in lines:
  if line.startswith("scope_checks["): scope=True
  elif scope and line.startswith("informational_checks:"): scope=False
  elif scope:
   if line.startswith("  - name: "): checks+=1
   if line == "    ok: false": failures+=1
  if line.startswith("  registrations["): active=True; client=None
  elif active and line.startswith("    - client: "): client=line.split(": ",1)[1]
  elif active and client is not None and line.startswith("      state: "): regs[client]=line.split(": ",1)[1]
 counts={state:sum(value==state for value in regs.values()) for state in sorted(set(regs.values()))}
 print(f"{name}: scope_checks={checks} scope_failures={failures} registration_rows={len(regs)} states={counts}")' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/doctor/doctor-6.5.0.txt /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/doctor/doctor-6.7.0.txt

/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/doctor/doctor-6.5.0.txt: scope_checks=26 scope_failures=15 registration_rows=13 states={'manual': 1, 'missing': 7, 'stale': 5}
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/doctor/doctor-6.7.0.txt: scope_checks=21 scope_failures=10 registration_rows=13 states={'aligned': 5, 'manual': 1, 'missing': 7}
exit 0
```
