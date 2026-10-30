# ScoutCensusRecheck — R51-C2 registry-census drift, independent re-derivation

Seat `ScoutCensusRecheck` (scout, leaf member — no subagent dispatch). Round 51, wave 1 (BUILD).
Base revision for the C2 before-arm: `1aa27369`. Claims-draft commit: `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.
No REA run. No lane write. No git mutation (read-only `git show` / `ls-tree` only).

**Verdict: the claim's numbers are CONFIRMED (55 registered / 42 census paths / 13 outside / 0 vanished),
but the claim's proposed CENSUS RULE is wrong — it cannot reach `census_outside 0`. F1-F3 below are
the actionable findings for the L1's instrument port.**

Artifacts (receipts, full command / exit code / stdout sha256 / UTC per step):
- `.ufo/waves/round-51/w1/ScoutCensusRecheck/census-recheck.py` — the re-derivation script (re-runnable, read-only)
- `.ufo/waves/round-51/w1/ScoutCensusRecheck/census-recheck.json` — 13 receipts + machine-readable findings
- `.ufo/waves/round-51/w1/ScoutCensusRecheck/the-13.txt` — the 13-path list

Tooling: none installed, none needed. `python3` (system) only. No pacman transaction. No `uv`/`npx`/`cargo`.

---

## The parse (question 1 — "show your parse")

Two independent parses, both agreeing on **55**:

1. **`meanings.py`'s own parser** (`tools/round-48/meanings.py`, `registry_rows()`), fed
   `git show <rev>:SKILL.md`: the marker region `<!-- instrument-registry v2 -->` …
   `<!-- /instrument-registry -->` (exactly 1 open + 1 close marker, no doubled markers),
   then `ROW_START = ^\|\s*\`` rows, then cell-0 backtick path.
2. **A pure-regex parse** with no import of `meanings.py` at all: `^\|\s*`([^`]+)`` over the same
   marker region — 55 rows, 55 unique paths.

Structural facts, all at `1aa27369`, at `f04b51dd`, and at `HEAD` (identical at all three):
- 55 data rows, 55 unique paths (no duplicates), **every row has exactly 7 cells** (the PROTOCOL
  row shape), every registered path exists on disk at the measured rev (0 absent).
- Rows per `tools/<dir>`: round-41 13, round-42 11, round-43 4, round-44 3, round-45 3,
  round-46 4, round-47 2, round-48 2, round-49 6, round-50 6, round-50-c3 1 = **55**.

## The 13 (question 2 — registered paths absent from `census2.json`)

`census2.json` = 42 paths. Registry = 55. **13 registered paths absent** — the claim's number is
exactly right, and the breakdown matches lesson **M50-2** ("12 rows (six round-49, six round-50)
inside the `instrument-registry v2` markers" + the round-50 C3 instrument = 13):

```
tools/round-49/c1-controls.py   tools/round-50/c1-controls.py
tools/round-49/c1-counter.py    tools/round-50/c1-counter.py
tools/round-49/c1-oracle.py     tools/round-50/c1-run.sh
tools/round-49/c1-run.py        tools/round-50/c2-record.py
tools/round-49/c1-run.sh        tools/round-50/fetch-vendor.py
tools/round-49/c2-mismatch.py   tools/round-50/selftest-r49-c2.py
                                tools/round-50-c3/sqfs-triage-v5.py
```
(6 × round-49, 6 × round-50, 1 × round-50-c3.)

**Question 3 — vanished path: NONE FOUND.** `census2.json`'s 42 paths are all present in the current
registry at every rev checked (0 vanished). Also `tools/round-46/census.json` (38 paths) is a strict
subset of `census2.json`'s 42, so the union of the two committed census artifacts is still 42, and
**union \ registry = 0**. There is no stale path in either direction except the forward drift.

**Fresh-derivation check (bonus).** `census2.json` still equals a fresh `census2.census_text()`
derivation of its own rule at all three revs (42 = 42, `named_but_absent` empty). So `census2.json`
is **not stale** — it is *frozen at a scope that stopped matching the registry*. That distinction
matters for the L1's wording (see F3).

## Question 4 — does the frozen battery consume `census2.json`?

**NO — not directly, and not at all.** `tools/round-50/selftest-r49-c2.py` contains **0** occurrences
of the string `census` (case-insensitive); the counter it drives, `tools/round-49/c2-mismatch.py`,
also contains **0**. The selftest's freeze scope is `tools/round-49/` + `plans/round-49-claims.md`
(`c2-mismatch.py:583`); it never reads `tools/round-48/census2.json`. The *only* consumer of
`census2.json` in the lane is `tools/round-48/meanings.py` (`CENSUS` at line 39, `CENSUS_TOOL` at
line 40), which `exec`s `census2.py` and compares `doc["paths"]` to a fresh derivation.

**Consequence for the L1:** the frozen round-49 selftest battery is *not* a consumer of the census
and will not move when `census3.json` lands. The R51-C2 census clause must be measured by the
**new round-51 instrument**, not by re-running the round-49 battery.

---

## F1 — The frozen round-48 counter is ALREADY RED at the base and at HEAD (severity: high)

`tools/round-48/meanings.py`'s registry↔census equality clause fails at **`1aa27369` AND at `HEAD`**,
exit 1, on the same 13 paths:

```
failing: ["registry rows outside the census: ['tools/round-49/c1-controls.py', ... 13 paths]"]
registry_rows 55   census_paths 42   census_rederived_equal True
registry_missing []   registry_extra [13 paths]
```

This is *not* a round-51 regression — the drift predates the round and is acknowledged in
`plans/round-50-claims.md` ("added rows in the `instrument-registry v2` block of `SKILL.md` are rows
outside the frozen round-48 `census2.json`; both older counters … are not re-run as gates this round").
**But the R51-C2 plan must not silently inherit it.** Two things follow for the L1:

- `plans/round-51-claims.md` says the landing "adds `tools/round-51/census3.json` (the re-derived
  census)". If `census3.json` lands while `census2.json` stays the artifact `meanings.py` reads
  (`CENSUS` is a hard-coded path constant), **the round-48 counter stays red** — the new census does
  not help it, because `meanings.py` is byte-frozen and `tools/round-48/` is a frozen path
  (round-48 claims freeze `tools/round-48/`). So the R51 landing **cannot** make the round-48 counter
  green, and the R51-C2 claim must not be scored by it.
- Conversely: `meanings.py`'s red at HEAD is the *proof* the drift is real, and it is the natural
  second reader for the R51 census clause. The L1 should state in the claims file that the R51-C2
  census clause is measured by the **round-51 instrument against `census3.json`**, and that the
  round-48 counter's redness is a *pre-existing, out-of-scope* condition (or, better, gets its own
  routed-defect entry — the round-50 closure's own precedent). Leaving it unstated is a
  "known-red frozen counter" trap of exactly the kind QUALITY rows 90-93 were written for.

## F2 — The claim's stated census RULE cannot reach `census_outside 0` (severity: high — blocks the claim)

The plan says the census re-derivation is "ported from the `meanings.py` census surface". `meanings.py`'s
census surface delegates to `census2.py`, whose rule is **claims-file naming**:

> every path matching `tools/round-4[1-8]/**.{py,sh}` named in a `plans/round-4[1-8]-claims.md` at
> `--rev`, restricted to paths present there

Ported forward to rounds 41-51 (i.e. `tools/round-4[1-9]` + `tools/round-5[0-1]` + `-c3`, claims files
`round-41..49` + `round-50` + `round-50-attempt2` + `round-51`), the rule yields **52** present paths,
and:

```
registry \ census3  ->  3, NOT 0
    tools/round-49/c1-controls.py
    tools/round-49/c1-oracle.py
    tools/round-49/c1-run.py
census3 \ registry  ->  0
```

**Three round-49 instruments are registered but named in NO claims file** (verified by grep over
`plans/`: zero hits for `round-49/c1-oracle.py`, `round-49/c1-run.py`, `round-49/c1-controls.py`).
A claims-naming census therefore *cannot* cover the registry, and the claim's stated before→after
(13 → 0) is unreachable under it.

**The rule that does reach 0 is registry-driven**: enumerate the registered instrument paths from the
`instrument-registry v2` markers at REV. This is also what the plan's own wording says the re-derive
command must do — "enumerates the registered instrument paths from the registry markers at REV and
reports `census_outside` = registered paths absent from the active census artifact". **So the plan's
*predicate* is right and its *"ported from the `meanings.py` census surface"* parenthetical is the
wrong pointer.** The L1 should:

1. Define `census3.json` by the **registry-driven** rule (registry markers at REV → sorted paths),
   not by claims naming. The re-derivation then reads the *registry*, and `census_outside` is the
   registry rows the census does not list.
2. **Choose the census scope deliberately.** The only scope that yields `census_outside == 0` is
   "every registered instrument path" (registry-driven). A scope of "every `tools/**.py|.sh` at REV"
   also gives 0 (173 paths) but inverts the metric's meaning — it makes `census_outside 0` vacuous
   (nothing can be outside it) while the *real* drift is the **118 files with no registry row**
   (9 of them in the `tools/round-41..50` scope: `round-42/c1-extra.py`, `round-43/build-copies-r43.py`,
   `round-43/c2-controls-r43.py`, `round-43/receipt-wrap.py`, `round-44/c1-controls.py`,
   `round-44/c1-oracle.py`, `round-44/c1-run.py`, `round-44/c2-controls.py`, `round-48/census2.py`).
   Note `tools/round-48/census2.py` is itself unregistered — the very generator of the drift.
   **Recommendation: score BOTH directions** — `census_outside` (registry row with no census path)
   *and* `census_unregistered` (census path with no registry row) — so the metric cannot be made
   vacuous by widening the scope. The `meanings.py` surface already computes both
   (`registry_missing` / `registry_extra`); the R51 instrument should port both.
3. **Fix the fixed point.** `census3.json` must list **all 62** registered paths at the R51 freeze rev
   (55 + 7 new `tools/round-51/` rows: `c1-counter.py`, `c1-controls.py`, `c1-run.sh`,
   `fetch-vendor.py`, `misroot-sweep.sh`, `sqfs-triage-v6.py`, and the census re-derive tool).
   A `census3.json` generated at the **pre-freeze base** (55 paths) leaves `census_outside == 7`, not
   0. Generate it **after** the new registry rows are drafted, in the same wave.

## F3 — the before-arm needs the base-arm artifact pinned, not the new one (severity: medium)

The claim says at the declared base `1aa27369` the same command exits 1 with `census_outside 13`.
That is exactly right **only if the base arm reads `census2.json`** (42 paths) against the base
registry (55 rows): `55 − 42 = 13`. ✓ (verified at `1aa27369`, at `f04b51dd`, and at `HEAD` — the
registry did not grow between the base and HEAD).

But `tools/round-51/census3.json` **does not exist at the base rev**. So the instrument's census
selection rule must be: *at REV, use `tools/round-51/census3.json` if present, else
`tools/round-48/census2.json`* — or, more robustly, the instrument must be told which census artifact
to score and the base arm must be pinned to `census2.json` explicitly. Otherwise the base arm exits 2
(could-not-evaluate: "census absent at rev") instead of 1 with `census_outside 13`, and the claim's
before-state is unreproducible. **The L1 must state the artifact-selection rule in the claims file**,
because "the census" is ambiguous between the two files.

## F4 — scope hygiene for the L1's landing (severity: low, mechanical)

- `tools/round-48/` is a **frozen path** (round-48 claims) → `census2.json` and `census2.py` must
  stay byte-identical. The plan already says "the frozen round-48 census bytes stay untouched" — good.
- `tools/round-50/` is byte-frozen and the round-50 counters freeze the whole tree; the round-50 C3
  instrument lives in `tools/round-50-c3/` precisely because `tools/round-50/` is frozen
  (`tools/round-50-c3/sqfs-triage-v5.py:308-316`). New round-51 files belong in `tools/round-51/`,
  which is outside every frozen walk — confirmed: round-50's `FROZEN_PREFIXES = ('tools/round-50/',)`.
- The round-50 counter's **B9** atom re-derives its own census from `ls-tree` over
  `tools/round-49/**` (at BASE) + `tools/round-50/**` (at REV) — 12 paths — and checks each has
  exactly one registry row with 7 cells. **B9 is green** (0 violations) and it does **not** cover
  `tools/round-50-c3/` (prefix `tools/round-50`), which is why the C3 instrument needed no B9 row.
  B9 is a *third, independent* census surface from `census2.json` and from the new `census3.json`;
  landing `tools/round-51/` does not perturb it (prefix `tools/round-49`/`tools/round-50` only).
- Round-51 will add **7** new registered rows, so the registry at the freeze rev is **62** — the L1's
  own census3 must be generated against 62 (F2 item 3).
- `plans/round-51-claims.md` names `tools/round-51/census3.json`, `gap-rule.json`, `c1-controls.py`,
  `c1-counter.py`, `c1-run.sh`, `fetch-vendor.py`, `misroot-sweep.sh`, `sqfs-triage-v6.py` — 8 paths,
  of which the 6 `.py`/`.sh` need registry rows ("no other code files land there"); `census3.json` and
  `gap-rule.json` are data, not instruments. My "7" above counts the census re-derive tool as a
  separate file per the plan's own conditional ("one for the census re-derive tool (if it is a
  separate file)") — if the re-derive is folded into `sqfs-triage-v6.py`, the count is **6** and
  census3 must list **61**. The L1 should fix this number explicitly and make the census3 path list
  match it exactly.

## What I did NOT do (honest stops)

- **No REA run** (per the wave contract). Nothing here depends on one.
- **No mutation testing** of the round-51 v6 instrument — it does not exist yet; F2 is a static
  analysis of the census rule the plan specifies, not a measured counter run.
- **No `census3.json` drafted.** It must be generated against the *post-amendment* registry (61 or 62
  rows) at the freeze rev; generating it now would bake in the wrong fixed point (F2 item 3). The
  derivation script that produces it is `census-recheck.py` step 6 (rule A), ready to adapt.
- **The 118 unregistered `tools/**` code files** (9 in the round-41..50 scope) are reported, not
  fixed. Fixing them is outside R51-C2's claim cap (the plan names only the census re-derivation) and
  would need its own routed-defect entry.

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
TMPDIR=/fast/scratch/hyaku/kaidoku-r51/w1-ScoutCensusRecheck \
  python3 -I -B .ufo/waves/round-51/w1/ScoutCensusRecheck/census-recheck.py \
    --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --out  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-51/w1/ScoutCensusRecheck
```
Exit codes are semantic (0 met/clean, 1 not met/violation, 2 could-not-evaluate). Step
`r48-counter-red@*` exits **1** by design — that is the measured redness of the frozen round-48
counter (F1), not a script failure. All other steps exit 0.

Receipt sha256 (stdout of each step) is in `census-recheck.json` under `receipts[].stdout_sha256`;
the script itself: `census-recheck.py`, and `census-recheck.json` sha256
`41a447e3f4209ad8762bbac1b8bcc62e66fc264e364f530e166de0df3494f654`,
`the-13.txt` sha256 `c8562f5168ad84a84ebe930decbfc064b7211d57f229a177fcfba0e9db17d436`.
