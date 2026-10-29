# ScoutQuietWindow — host-load window for the REA-dependent R50-C1 steps

Seat: ScoutQuietWindow (wave 3, round 50 attempt 2) · 2026-10-29T20:33–20:44Z · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

## Verdict

**Do not start the REA battery in the current window. Gate: two consecutive checks 60 s apart with `load1 < 16` AND `load15 < 24` AND vmstat `r < 32`; never start at `load1 ≥ 40`; between 16 and 40 only behind a canary.** Every recorded `provider_timeout` fired at `load1 ≥ 42.5`, and each attempt dies just past REA's fixed 120 s budget (attempts measured 124–129.3 s ≈ +4–8 %), so the margin is thin, not a cliff: uncontended the same extractions take 28.7–63.1 s. Sampled window (wave 3 in flight): `load1` 32–73, `load15` 39–46, idle ≤ 13 %, `wa = 0` in all five samples — pure CPU contention from the ~30 wave-3 seats, storage is not a factor. After wave 3 drains, `load15 ≈ 44` needs ~30–60 min to decay; plan the battery for late-UTC-evening like the only recorded success window (23:33–23:36Z, 2026-10-28).

**Monitoring one-liner for the L1 (brace-safe; float compare in awk):**

```bash
while :; do read -r L1 L5 L15 _ < /proc/loadavg; set -- $(LC_ALL=C vmstat 1 2 | tail -n 1); G=WAIT; [ "$(awk -v a="$L1" -v c="$L15" 'BEGIN{print (a<16 && c<24)}')" = 1 ] && [ "${1}" -lt 32 ] && G=GO; printf '%sZ load1=%s load5=%s load15=%s r=%s us=%s sy=%s id=%s wa=%s -> %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$L1" "$L5" "$L15" "${1}" "${13}" "${14}" "${15}" "${16}" "$G"; sleep 60; done
```

## Findings table

| # | finding | exact command | exit | evidence (sha256) |
|---|---|---|---|---|
| F1 | Harness caps are not CPU throttles: `async.maxJobs: 450` (config.yml:567), `task.maxConcurrency: 400` (:413). They cap agent fanout, not host load; the wave-3 fanout is the load source. | `grep -nE 'maxJobs\|maxConcurrency' /home/vgpnk/.omp/agent/config.yml` | 0 | config.yml `772c82179be4eb87df94ce07eaa8e32d25c411cf2600c46cdba908e465a2175f` |
| F2 | Dev-arm failures are timestamped: a7530 00:49:25→00:55:36Z, a7590 00:55:39→01:01:48Z (2026-10-29), 3 REA attempts each, all `provider_timeout`, `timeout_ms: 120000`; L1 recorded `load average 42.5-54 (uptime at run)`; timeout "not tunable" (REA 6.5.0 `FIRMWARE_LIMITS`, `dist/cli-runtime`). | read `.ufo/waves/round-50/l1/dev-arm-timeouts.txt` + `l1/dev-arm-timeouts/{a7530,a7590}.run.json` | — | txt `7418a027c33fca412c41727ccb83a2620753e7beef0c0221c5046422c8128dcb`; a7530 `4d7b5ea807ead098607443467c4d280295976c294fe44c25ec8cc28696a44990`; a7590 `9cb71cf6ce09abc34a2edd6e57e50cc08d84eb1c3a34ead0526a0faffb3c7a72` |
| F3 | Same op succeeded earlier the same evening: extract 48.05 s (exit 0, 40 % of budget); later "gen/score passes" at load 48–72 → pos gen 5 attempts 126.4/129.3/127.7/126.4/126.2 s, **all** `provider_timeout`. `FIRMWARE_LIMITS` pinned: `inputBytes 128 MiB … timeoutMs 120000` (`dist/firmware/FirmwareRelease.js:27-33`). | read `.ufo/waves/round-50/w1/C1ControlsBuild/receipts/a7530-rea-probe.txt` | — | `05c0d760b86ab37ad7e6e1250b47e435308e573322a64ad396235373b77bf8a2` |
| F4 | Wave-1 success walls: 4 ok runs 28 710–63 113 ms (plus one 40 237 ms), 23:33–23:36Z 2026-10-28, "host loaded by other seats (run-to-run 29-63 s)"; **no loadavg recorded for any success**. L1's note: "under lower load (wave-1 C1DevArmA, ~21:00 -03): 40-48 s". | read `.ufo/waves/round-50/w1/C1DevArmA.md` (run table + start times) | — | `31eb168d0848dda527ee5a0e8214f338131dc580d7dd3b9c4b8fc318fb5e37e6` |
| F5 | Attempt-1 controls battery (01:41–02:27Z): c0 8.05 s exit 1 `as_expected` (offline, no REA); c1 546.8 s exit 1 `as_expected` with `rerun_errors {}` (BE receipts fail subject-pin before any REA rerun — no REA dependency observed); **c2/c3/c4/pos exit 2** `rerun_env_error` "REA provider_timeout on <carrier> after 3 attempt(s); repeat on a quieter host", control walls 372.3–759.2 s. `kill_rule_fires: false`. | read `controls-attempt1/summary.json` + `c{1,2,3,4,pos}/receipt.json` | — | summary `45bfa9f29fa8fbb117156ee078a5fdf008b1446af93dd8106dc17b8207946348`; c1 `0375e174…140044`; c2 `11066a61…7b418`; c3 `cedeb61f…845c8`; c4 `8ad3eec6…cdb`; pos `7865b8b6…cd38e` |
| F6 | 10-minute sample (5 × `vmstat 5 5` + `/proc/loadavg`, ~2 min apart): `load1` 69.3 → 73.4 → 61.0 → 31.8 → 36.4; `load15` 39.2 → 44.0; `r` 17–89; `wa = 0` and `b = 0` in all samples. At 20:43:27Z: `26.97 40.20 42.18`. | `bash <scratch>/sample.sh` (script kept as receipt) | 0 | `load-samples.tsv` `263141339706b05fc401cbb0e2a4484101aa223433a99c8c28d4669507ee9e27`; `vmstat-raw.txt` `73da16c638a5dc67bcc7cbcfd64a432050747b296261e2598ca3925e1d3fd91e` |
| F7 | Disk is a non-issue: `/fast/scratch/hyaku` 39 % used (493 GB free), `/tmp` 23 %. Consistent with `wa = 0`. | `scripts/hyaku/disk-guard.sh status` | 0 | output in session transcript |
| F8 | Offline contention inflation ≈ 3×: the 40-case round-49 C2 selftest 23 s on a light host → 74.7 s at load 54 (C2Selftest49 F1); "wall times load-dependent 49–62". Extract walls inflate the same way (29–40 s → 124–129 s, ≈ 3.2–3.4×). | read `.ufo/waves/round-50/w1/C2Selftest49.md` F1/limits | — | cited in that report |

## Load vs 120 s `provider_timeout` — attempt-1 + wave-1 tabulation

| window (UTC) | load1 at run | REA runs | outcome |
|---|---|---|---|
| 10-28 23:33–23:36 (wave-1 dev arm + probe) | not recorded; L1 calls it "lower load"; probe's one in-band success at 48.05 s | 8 extract-firmware on a7530/a7590 (2 staging-budget refusals at 2.3–3.2 s are not REA timeouts) | **8/8 ok**, walls 28.7–63.1 s (40–48 s for the dev-arm bytes) |
| 10-28 23:49 → 10-29 00:57 (gen/score passes, local 20:49–21:57 -03) | 48–72 | pos-gen on a7530 ×5 | **5/5 provider_timeout**, 126.2–129.3 s each (~ +5–8 % over budget) |
| 10-29 00:49–01:01 (L1 dev arm) | 42.5–54 (recorded "uptime at run") | a7530 + a7590, 3 attempts each | **6/6 provider_timeout**, 371.5 / 369.5 s total (≈ 124 s/attempt) |
| 10-29 01:50–02:27 (controls battery) | 95–176 (L1's recorded range; no per-control loadavg receipt exists) | 4 REA-dependent controls (c2→c6490, c3→g7581, c4→c6490, pos→g7581), 3 attempts per carrier | **4/4 controls exit 2** `rerun_env_error`; control walls 372.3–759.2 s |

Dispatch phrasing note: "40-48 s at load 40-54" compresses two receipts — the 40–48 s successes are wave-1 at *unrecorded, lower* load; the 42.5–54 band has **one** success (probe 48.05 s, before the "later" passes) and six timeouts. The band is the knife edge; ≥ 48–72 is reliably fatal.

Mechanism: uncontended extract of a 28–36 MB xz member ≈ 29–40 s; ≈ 3× CPU-contention inflation (F8) crosses the fixed 120 s budget at roughly `load1 ≈ 45–65` on 32 cores — consistent with the observed floor 42.5. REA retries 3× but the host stays loaded, so retries never rescue; the timeout is not tunable (F2/F3).

## Sample (wave 3 in flight)

```
utc                 load1   load5   load15   r   b  us  sy  id  wa
2026-10-29T20:33:54Z 69.29  42.76   39.21    39  0  52  40   8   0
2026-10-29T20:35:54Z 73.37  53.31   43.55    84  0  66  31   3   0
2026-10-29T20:37:55Z 61.02  56.17   45.86    40  0  63  32   5   0
2026-10-29T20:39:55Z 31.82  48.25   44.35    89  0  67  21  13   0
2026-10-29T20:41:55Z 36.41  45.82   44.01    17  0  36  16  47   0
```

Artifact disclosure: `sample.sh` wrote the original TSV with unbraced positional refs (`$14` → bash expands as `${1}4`, empirically confirmed: `set -- a…n; echo $14` → `a4` on bash 5.2.37), so its cpu columns were garbage. `load-samples.tsv` was rebuilt from the untouched `vmstat-raw.txt` (full `vmstat 5 5` captures) by `rebuild-load-tsv.sh` (kept as receipt); load columns were always read from `/proc/loadavg` directly and are unchanged. Verification: sample 1 raw line `39 0 18977408 4111548 36 9574220 4593 355 133086 131094 274258 629961 52 40 8 0 0 0` → r=39 b=0 us=52 sy=40 id=8 wa=0 = rebuilt row. vmstat here emits 18 columns (us=13 sy=14 id=15 wa=16).

## Recommendation (for the L1's quiet window)

1. **Gate** (two consecutive checks 60 s apart): `load1 < 16` AND `load15 < 24` AND vmstat `r < 32` (≈ 0.5 load/core). **Never start at `load1 ≥ 40`** — observed failure floor 42.5. 16–40: only behind step 2. Margin rationale: ≤ 16 keeps expected inflation ≈ ≤ 1.5× → 45–60 s walls, 2–2.7× budget headroom; the threshold is derived from the failure floor + inflation, not from a recorded success at 16 (no success ever had its load recorded — see limits).
2. **Canary before the battery**: one `extract-firmware` on the smallest carrier (g7581, 4.5k files, 29–40 s uncontended); proceed only if exit 0 and wall < 90 s; abort the window on any `provider_timeout`. Advisory — the L1 owns the schedule; frozen order (controls before data) is unaffected.
3. **Stay serial, pause on drift**: controls are serial by design. If `load1` rises above 24 mid-battery, pause between controls — each is independently restartable, and a persistent timeout is exit 2 "repeat on a quieter host", recorded, never a verdict (frozen recheck rule, `land_c1.py:88`).
4. **Expected healthy battery**: 4 REA-dependent controls + 4 data-run carriers ≈ 15–25 min of REA wall time at uncontended speeds (28.7–63.1 s per carrier), so a 30–45 min quiet stretch suffices. C3 controls are offline instrument runs and need no window.
5. **Time of day**: the only recorded success window is 23:33–23:36Z (late UTC evening); schedule likewise after wave-3 seats drain (`load15 ≈ 44` at 20:44Z decays over ~30–60 min).

## Not run / limits

- No REA run, no downloads, no installs (no tool changes to record), no fixture repos, no heavy processes started — per contract.
- The 95–176 load range for the controls window is the L1's recorded figure (attempt-2 claims line 5–6); receipts corroborate the failures (4/4 `rerun_env_error`, 01:50–02:27Z) but no per-control loadavg was captured, so the exact band is not independently verified here.
- No success run ever had its load recorded; `< 16` is a margin-derived threshold (failure floor 42.5, ≈ 3× inflation, budget 120 s), stated as such.
- The sample covers 8 min of wave-3 load only; the quiet window itself was not observed (nothing quiet to observe at dispatch time).
- Scratched: `/fast/scratch/hyaku/kaidoku-r50/w3-ScoutQuietWindow` removed at 20:43Z after receipts were copied into the seat dir (`sample.sh`, `rebuild-load-tsv.sh`, `vmstat-raw.txt`, `load-samples.tsv`).
