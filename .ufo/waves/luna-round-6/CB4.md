# CB4 — substrate adversary: registry-down / cache eviction / quota

## CLAIM
Would lane-B's re-runs have survived registry-down, npx-cache eviction, and quota/rate limiting? Judged from receipts-B fetch evidence plus probes.

## METHOD
Read all 10 receipts-B + MANIFEST (leg-1 hash spot-verified). Audited host npm debug logs (`~/.npm/_logs`; snapshots `/tmp/cb4-logs-1,2`), the npx cache, npm config, `/tmp` cache dirs. Probes (npx from /tmp, CLI-only, no config edits, ps-verified no leftovers, ≤240s caps): warm cache + dead proxy (real URL) at stock/reduced retries; warm cache + dead registry URL; empty-cache install; 2.5h-stale entry (120s cap fired).

## FINDINGS
- Every lane-B invocation touched the live registry: surviving logs show `GET 200 https://registry.npmjs.org/rea-agents (cache revalidated)` per exec (10+ lines). Receipt "npx cache hit" (leg-1:13, ~0.6s; leg-10:13, 0.669s) means install reuse only — not network independence; fetch evidence in receipts is otherwise timing + cache-env notes (leg-2:1-2, leg-6:12, leg-9:22).
- Registry-down + warm cache: SURVIVES via stale fallback. Dead proxy honored (`attempt 1-3 failed … ECONNREFUSED`), then `200 … (cache stale)` at 70028ms → exit 0, `6.5.0` (log 2026-10-16T22_07_42:14-17,24). Cost ≈ +70s/startup at stock retries (10s+60s backoff); 0.9s with retries=1 (`22_03_23:14-16,23`).
- Cache eviction + registry up: SURVIVES. Empty cache → 173 tarball GETs, exit 0 in 3.45s, 336MB; plus 38MB frida prebuild into `_prebuilds` (prebuild-install; host not in npm's log).
- Eviction + registry down: impossible — dead-URL probes exit 1 (ECONNREFUSED / ENOTCACHED). Receipts-B show ≥3 legs ran on `/tmp` caches cold-built seconds earlier (BB2/BB6 `/tmp/kaidoku-luna-round-6B-npm-cache` 19:00:35; CC3 `/tmp/kaidoku-luna-round-6-npm-cache` 19:00:49). An outage crossing those pre-probes fails them; receipts record no fetch-layer artifact for this.
- Quota: zero 429/5xx/timeouts in all preserved logs; ≈1 revalidation per exec; cold builds add ~174 GETs (2-4 observed today).

## THREATS
npm logs rotate (logs-max:10 cleaned evidence mid-audit — snapshots cited). Probe env overrides annotated. Dead proxy emulates connection failure, not DNS/5xx (untested class). The 2.5h-stale probe never completed (second ~70s retry cycle pending at kill). 3.45s rebuild is host/network-speed specific.

## VERDICT
FINDING: re-runs survive registry-down only via stale-cache fallback (+70s) and eviction only with the registry up; three legs' caches were cold-built seconds before first use, so an outage crossing their pre-probe window would have failed them — a dependency receipts-B don't record.
