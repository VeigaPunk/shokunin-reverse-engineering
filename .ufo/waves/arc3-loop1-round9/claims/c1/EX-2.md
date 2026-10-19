# EX-2 — C1 freshness: pacman row census

## Finding

The live pacman inventory count is **VERIFIED at 1,350 archives**, with 1,350 matching `.sig` files and no missing or orphan signature names. `PROVINCE.md:50` still describes the stored `1556` snapshot without an as-of qualifier. I supply a same-line replacement below; it is proposal text only, and `PROVINCE.md` remains untouched.

The stored `1556` historical count itself is **UNVERIFIABLE from the current checkout**: its original staging source (`.ufo/waves/kaidoku-r1/12-archives-pkgs.md`) is referenced by the corpus but is absent from `.ufo/waves/kaidoku-r1/`. The archived corpus assertion is not independent evidence under rule #14. Thus `−206` is arithmetic conditional on that stored baseline (`1350 − 1556`), not a fresh observation of the 2026-10-13 cache. The corpus erratum at `corpus/knowledge/2026-10-13-pacman-packages.md:73-83` is the requested pointer for the recorded live delta; its cache-eviction explanation was not independently tested here.

## First-hand measurements

Checkout identity: `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.

Commands and exact output:

```text
$ date -I; grep -n '1556' PROVINCE.md; wc -l PROVINCE.md; ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l; ls /var/cache/pacman/pkg/*.sig | wc -l
2026-10-19
50:| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
162 PROVINCE.md
1350
1350

$ python3 signature-name census
archives=1350 signatures=1350 missing_signatures=0 orphan_signatures=0
```

`wc -l` confirms the requested 162-line file. The candidate below replaces only line 50, so the line count remains 162; the scratch copy measured `candidate_line=50; province_lines=162`.

## Whole-row perishable census (`PROVINCE.md:40,50`)

`PROVINCE.md:40` dates the Core table as “each verified on this host 2026-10-13.” Against that dated context:

- **`1556 signed archives` — CORRECTED (proposal only); historic value UNVERIFIABLE here.** It is a retention-varying count and reads as current on line 50 absent a local qualifier. The live count is independently measured above. Proposed text explicitly dates both counts and points at the corpus erratum.
- **`available:true in live session` — perishable; current status UNVERIFIABLE by this seat.** The table header supplies a 2026-10-13 verification date, but this cell can read as live/current when separated from the header. The proposal makes its recorded date explicit. No REA live-session capability probe was available/performed for this claim.
- **`installed jq verified byte-identical to signed archive member` — perishable verification result; current status UNVERIFIABLE by this seat.** It is a past-tense result under the same 2026-10-13 table date, not a fresh 2026-10-19 check. The proposal makes that historical date local to the value.
- **Not perishable values:** `.MTREE per-file sha256` is a format/property statement; `pacman -Qkk verify` and `binary_session {}` are probe/capability descriptions, not claims of a current measured result.

The v10 census does not measure pacman counts or these availability/byte-identity claims: its value patterns are pins, bare `6.x.y` versions, and `.json/.toml/.yaml` `path:line` pointers (`.ufo/gates/c1-census-v10.py:310-314`). Its PASS cannot establish this row’s freshness.

## Proposed same-line replacement (NOT applied)

```diff
-| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
+| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session; verified 2026-10-13); pacman `.pkg.tar.zst` corpus 1556 signed archives as of 2026-10-13 (live re-count 2026-10-19: 1350; delta −206 vs. snapshot; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member (2026-10-13 verification) |
```

## Instrument checks and discrepancy

- `sha256sum .ufo/gates/c1-census-v10.py` → `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`; this is the v10 gate read-only. The live `:4126` pointer is independently visible in `~/.kimi-code/config.toml`, but is outside this seat’s pacman row claim.
- Actual worktree run, `python3 .ufo/gates/c1-census-v10.py --root .`, **FAILS**, rather than PASS: `UNDECLARED` contains `SCORECARD.md` block `1833-1839`, with line `1834` `rea-agents@6.7.0` (`.ufo/gates/c1-census-v10.py:274-277` declares the last SCORECARD span only through `1813`; `SCORECARD.md:1833-1839` is beyond it). Other reported checks: stale=0, ambiguous=0, unresolved=0, scope-errors=[], G21 14 rows/errors=[], G2 ok, unreadable=[], G11=[], declared fail classes=[]. The command ends `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`, exit 1.
- I applied the proposed line only in a scratch copy under `/var/tmp/kaidoku-ex2-r9.RITWkR`; the census still returned `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`, exit 1. This isolates the blocker: the PROVINCE-only proposal leaves the unrelated SCORECARD scope error unchanged. I cannot claim the frozen requirement “instrument still PASS” is met at this checkout; that requires an authorized gate-scope reconciliation outside my write scope.
- Command A was run against immutable HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006` using the recipe at `SCORECARD.md:88-124`. Exact JSON: `{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}`. No corpus entry/map token was added by this seat.

## Per-item verdicts

- Live archive count: **VERIFIED** — 1,350, directly counted on this host.
- Matching signature-name count: **VERIFIED** — 1,350 signatures; zero missing and zero orphan names.
- PROVINCE line-50 stale/current interpretation: **CORRECTED in proposal only** — replacement text provided, not applied.
- Historic 1,556 snapshot and causal `−206` cache-eviction account: **UNVERIFIABLE as historical observations** from this checkout; delta arithmetic is conditional on the stored 1,556 assertion.
- Other mutable row values (`available:true`, installed-jq byte identity): **UNVERIFIABLE as current**; both are dated 2026-10-13 context, and the replacement explicitly retains that date.
- Census PASS-after condition: **DISCREPANCY** — independently run gate fails on the undeclared SCORECARD tail, both before and after the scratch-only candidate.
