# CritCensus — R51-C2 census re-derivation, pre-freeze attack

**Verdict: the `census_outside 13 → 0` closure is not re-derivable as written; two BLOCKERs and
four MAJOR findings, all measured against the lane's own frozen bytes.**

Full numbered findings with demanded fixes: `.ufo/waves/round-51/w1/CritCensus/findings.md`
(8 findings, F1–F8). Receipts: `.ufo/waves/round-51/w1/CritCensus/receipts/` (13 files, each
with exact command, exit code, stdout sha256, UTC time).

Base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`; the claim's declared base `1aa27369` was
re-measured too — every number below is identical at both revs. Read-only git only
(`log`/`show`/`ls-tree`/`cat-file`); no lane write, no REA, no install, no scratch left behind.

## The three findings that matter

**1 (F1, BLOCKER) — `census_outside 13` is unreachable by the rule the claim names.** `13` is
the count of registry rows against the **frozen `census2.json` artifact**. Against a
re-derivation — which is what `:211-216` specifies — the base count is **4** (census2's rule
widened to rounds 41..51) or **1** (round-50's draft `census3.py` directory rule), never 13.
Measured table, both revs, `receipts/measure.out` (sha256 `b6afbc7e…87c5e7`). So the
predicate at `:203` ("at the declared base … exits 1 with … `census_outside 13`") can only be
produced by comparing against the artifact the landing replaces: the before-arm and after-arm
use different denominators, which is not a measurement of drift closing. **Fix:** amend the
literal `13` to the number the stated rule actually yields, and state the rule (the
`CLAIMS` glob, the directory prefixes, the absent-but-named treatment) in the claims.

**2 (F2, BLOCKER) — landing `census3.json` does not clear the frozen atom, and the claim's own
registry clause makes it worse.** `tools/round-48/meanings.py:39` hard-codes
`CENSUS = "tools/round-48/census2.json"`; it compares the registry against *that* at `:441-443`.
Measured at base: it already exits **1** with `registry rows outside the census: [13 paths]`.
`census3.json` is never read by any frozen consumer. And `:171-172`/`:228-229` require one
`instrument-registry v2` row per new `tools/round-51/` `.py`/`.sh` (≥6 expected), so the
frozen red grows 13 → 19+. Measured: +3 synthetic rows → `registry_extra` 16, still exit 1.
**Fix:** the L1 must choose and say which — (a) repoint the consumer to `census3.json` (amends
a frozen round-48 file, so the claims must say so), or (b) add-only, in which case R48-C1 is
knowingly left red and the claims must say that, as `plans/round-50-claims.md:35-38` already
discloses for the same situation.

**3 (F3/F4, MAJOR) — the supersession is unread and the metric is one-sided.** A JSON field
recording a supersession is not a supersession: `meanings.py` reads `census2.json`,
`c2-record.py:845-849` reads **no** census JSON at all (it re-derives from `git ls-tree`), and
`tools/round-46/registry.py:38` binds a third artifact (`census.json`, 38 paths). Nothing reads
`census3.json`; the `0` would be self-certified by the code that writes it. Separately,
`census_outside` counts only *registry → absent from census*; the converse (*census → absent
from registry*) is uncounted, so a `census3.json` listing exactly the 55 registry rows scores
0/0 and detects nothing. **Fix:** name the surface and the artifact that serves it in the
claims, the instrument docstring and the registry row's pinned-value cell; require **both**
directions in the predicate; add a "census artifact carrying one unregistered extra path"
mutant to the control list.

Also measured: `tools/round-50-c3/sqfs-triage-v5.py` is named only in
`plans/round-50-attempt2-claims.md`, which no `plans/round-{n}-claims.md` glob matches, and
`git ls-tree -- tools/round-50` does not match `tools/round-50-c3/…` — the one path that
survives even the round-50 draft's whole-directory rule (F5). The two frozen registry parsers
disagree on escaped pipes: one cell with `\|` gives `meanings.py` 8 cells (whole registry
clause fails) and `c2-record.py` 7 (F6). 39 registry paths sit outside the marker block, so
"the registry" is ambiguous between 55 and 94 rows (F7).

## Limits (not run)

No REA, no `--data-run`, no fetch, no install. `meanings.py` was run `--no-battery` only (the
4-forgery battery was not run). `c2-record.py` / `selftest-r49-c2.py` were **read, not
executed**. The 19+ after-landing figure is extrapolated from a measured 3-row probe, not
simulated at the real landing. `disk-guard.sh status` exit 0 before the heavy pass.

## Report path

`.ufo/waves/round-51/w1/CritCensus.md`
