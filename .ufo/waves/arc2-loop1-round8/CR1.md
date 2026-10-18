# CR1 — critic report: attack C3 (arc2-loop1-round8)

Seat: CR1 (critic) · 2026-10-18 · writes limited to this file; no repo edits,
no git mutations, no service signals (WATCH only), no config/network changes.
No /var/tmp scratch written (all observation was read-only).

## 1. Verdict

**KEEP — the natural control was worth its cost, and the attack resolved
empirically mid-round: the kill branch sealed in 4m42.9s, ~1/5 the budgeted
~25 min. C3 verifies on the kill branch: disable proven necessary (attribution
confirmed); the r7 entry needs NO correction.** Both premises of the attack
dissolve on inspection:

- **"~25 min" was the success-branch expectation**, and a correct one: r7's
  mitigated wall was 1424.663s ≈ 23.7 min
  (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13`). The realized branch
  (natural kill) cost 4m42.945s wall.
- **"Host memory" was never a cumulative drain**: 9G is a cgroup cap, not a
  reservation. Observed at 19:51:54 -03 with the control running: 4.7G
  current / 5.8G peak vs MemAvailable 19.7G; bystander harm zero (constraint
  kill, in-unit only; same containment class as r4, SCORECARD.md:896-901).
- **"Profits either way" is true operationally but misses the stake**: r7's
  sentence "The disabled analyzers removed the memory driver"
  (`...arc2-r7-pe-wall.md:17`) is a *single-arm causal claim* — r7 changed
  three variables vs round-4's death (cap 7G→9G, raised deadline,
  analyzer-disable). The control is r7's own named unknown #1 (:19) and the
  only instrument that could seal C3 at all. Skipping it would leave a
  confounded recipe standing in the corpus — precisely the standing-claim
  class the r5 verification round caught compounding for three rounds
  (SCORECARD.md:1008-1011). The honest-stop alternative (r3 precedent) was
  admissible but strictly worse: same calibration debt, zero evidence gained.

Pre-registered residual attack that *survives*: the control is single-run and
says nothing about r7 unknown #2 (rerun id-stability) — the C3 seal must not
claim it. Recorded below as scope qualifiers, not as a reason to skip.

## 2. Evidence

Commands and observed outputs (all read-only; local time -03):

1. `systemctl --user status arc2-r8-ctl --no-pager -l` (19:51:54): active
   3min 27s; `Memory: 4.7G (max: 9G, swap max: 1G, available: 4.2G, peak:
   5.8G)`; argv of PID 3883315 shows postScripts `ReaGhidraNoReturnFix.java` +
   `ReaGhidraBridge.java` only — **no `ReaGhidraAnalysisOptions.java`** (r7's
   disable pre-script), i.e. natural preset at process level.
2. `systemctl --user show arc2-r8-ctl -p Environment`:
   `REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 GHIDRA_HEADLESS_MAXMEM=6G
   TMPDIR=/var/tmp/arc2-l8r8-ctl ...` — **no `REA_GHIDRA_DISABLED_ANALYZERS`**
   — natural preset at env level. MemorySwapMax=1073741824 (1G swap cap).
3. `systemctl --user show arc2-r8-ctl -p Result,ExecMainStatus,ExecMainExitTimestamp`
   (19:57:26): `Result=oom-kill`, `ExecMainStatus=1`,
   `ExecMainExitTimestamp=Sun 2026-10-18 19:53:10 -03`.
4. `journalctl --user -u arc2-r8-ctl --no-pager | tail -6`: "The kernel OOM
   killer killed some processes in this unit." / "Failed with result
   'oom-kill'." / **"Consumed 11min 54.335s CPU time over 4min 42.945s wall
   clock time, 9G memory peak, 1G memory swap peak."** Start 19:48:27 -03 →
   kill 19:53:10 -03.
5. `systemctl --user show arc2-r8-ctl -p MemoryPeak` → `9663676416` =
   byte-exact the 9G cap (peak-at-cap signature of a constraint kill).
6. `head -3 /proc/meminfo; free -h`: MemTotal 30Gi, MemAvailable 19.7G — the
   9G cap was absorbable; no bystander pressure observed.
7. `du -sh /var/tmp/arc2-l8r8-ctl` → 2.6M mid-run; session dir
   `rea-ghidra-QgVQcR` absent at 19:57 (cleaned on failure — no envelope json
   found in TMPDIR or journal).
8. Custody cross-check (scope did not require it; done as corroboration):
   `sha256sum` of the five pre-pair paths returns the five hashes in
   `.ufo/waves/arc2-loop1-round8/receipts/config-pre-pair.txt:2-6` byte-
   identical — 5/5, zero drift as of 19:52 -03. Receipt timestamp :1
   (22:48:27Z) equals the service start second (same pattern as r7,
   SCORECARD.md:1136-1137).

Resolved pointers: attribution target `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:17`;
r7's two named unknowns `:19`; r7 wall/deadline data `:13`, preset `:15`;
r4 natural kill 4m42s at 7G + reset-failed residue duty SCORECARD.md:896-901;
r7 section + carried debt naming this control SCORECARD.md:1153-1156; r5
standing-claim precedent SCORECARD.md:1008-1011; capability-table rule
`AXES.md:57-64` (fleet skill dir, read-only).

Controlled comparison now in hand (same artifact sha `7a2ccd68…`, same host,
same service recipe, only preset differs): **natural = memcg kill in
4m42.945s at the 9G cap; disabled (r7 `arc2-r7-pe`) = exit-0 hold in
1424.663s, 7.9G peak.** The kill time matching r4's 4m42s at a *7G* cap
indicates the natural profile is cap-bound wherever the cap sits — so the
disable is necessary a fortiori at 7G too [INFERENCE].

## 3. Verbatim-landable text

Draft seal paragraph (round report / SCORECARD r8 section, C3 row support):

```
C3 (calibration, kill branch — attribution confirmed, sealed 19:53:10 -03
2026-10-18): the natural-preset control (user service `arc2-r8-ctl`; the r7
recipe minus `REA_GHIDRA_DISABLED_ANALYZERS`; 9G cap, 1G swap cap, 7200s
deadline, TMPDIR=/var/tmp/arc2-l8r8-ctl) was kernel-OOM-killed at its memory
cap in 4m42.945s (start 19:48:27 -03; systemd resource record: 11min 54.335s
CPU, 9G memory peak, 1G memory swap peak; Result=oom-kill, ExecMainStatus=1;
MemoryPeak byte-equal the cap). Same artifact, host, and service recipe, only
the analyzer preset differs: natural = cap-bound kill in ~4m43s; disabled
(r7) = exit-0 hold in 1424.663s at 7.9G peak. The disable is proven necessary
for the 9G-cap hold; `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:17`
stands — no append-only correction. R7 unknown #1 (natural unmitigated hold)
RESOLVED; unknown #2 (rerun id-stability) remains open — this control makes
no rerun claim. Scope qualifiers: single run, one host, 2026-10-18 ambient
load; the kill is evidenced by systemd/journal records and seat observations
(no sealed envelope or evidence_id — none was emitted before death; r4
precedent stands that REA does not produce a typed envelope for memcg kills).
Residue: `arc2-r8-ctl` rests in failed state — `reset-failed` is the parent's
residue duty (r4 form, SCORECARD.md:901); the journal excerpt is the kill
receipt candidate for committing.
```

Draft axis-table cell (r8 C3 row):

```
| calibration — C3 | r7 attribution single-arm/uncontrolled (three variables changed vs r4: cap, deadline, disable) → controlled kill: natural preset memcg-killed at the 9G cap in 4m42.945s vs r7's disabled-preset exit-0 hold (1424.663s, 7.9G peak), same artifact/host/recipe — disable proven necessary; r7 unknown #1 resolved, #2 (rerun stability) still open | improved |
```

## 4. Labels

- **OBSERVATION**: every systemctl/journal/du/sha256sum output above; file
  reads at the resolved pointers; the failed-unit residue state.
- **INFERENCE**: preset-natural (from Environment + argv postScript list; the
  in-session ghidra.log was not captured — session dir cleaned before a log
  grep, so this is config-level, not log-level evidence); the r4 "7G death
  point" reading as a cap artifact; attribution scope (artifact/host/recipe/
  date/9G-cap).
- **UNKNOWN**: rerun id-stability (r7 unknown #2 — untouched, stays open);
  whether any envelope text was emitted anywhere (none found in the user
  journal or TMPDIR at 19:57); which in-unit process the kernel killed (java
  presumed, not captured); sensitivity of the 4m43s kill time to ambient load
  (single run).
