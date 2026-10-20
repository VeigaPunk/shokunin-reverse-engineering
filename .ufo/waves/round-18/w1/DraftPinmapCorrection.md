# R17-PINMAP correction draft (DraftPinmapCorrection)

Author-side advisory draft for the L1 (KaidokuR18). Read-only: no lane file edited; no jj, no git write, no REA, no Ghidra, no carrier executed. The only write is this report.

## Findings

- **Defect confirmed on `refs/heads/main` (= 9011581).** Mid-run checks keep only `taken_at_utc`, `equal`, `entries` (a count), `changed`, `missing`; the mid snapshot `mid` is a local and is discarded. Evidence: `git show refs/heads/main:.ufo/waves/round-17/tools/carrier-run.py` lines 479-487 (also the working tree, identical: `git diff --stat refs/heads/main -- <4 files>` is empty, exit 0).
- **Receipts agree.** 29 mid-run checks across the 8 second-pass receipts (`.ufo/waves/round-17/runs/*/receipt.json`, key `steps.analyze.pin_checks`; no other step carries `pin_checks`). Every check has `equal: true`; each has the keys `changed, entries, equal, missing, taken_at_utc`. No `pins/` directory exists under `.ufo/waves/round-17/runs/` (`find ... -path '*pins*'` empty).
- **Pre and post maps are real.** `pins_pre` and `pins_post` carry `entries` with 146 paths in every second-pass receipt. This is what the knowledge entry's pre/post claim rests on, so it stays.
- **First pass.** At `da64646`, the 8 receipts have `pins_pre` and `pins_post` (146 entries) and no `pin_checks` key in `steps.analyze`. Knowledge line 33 ("The first-pass receipts kept only pre/post maps") is accurate.
- **Cadence.** `PIN_CHECK_S = 30.0` (`carrier-run.py:37`); the three aether checks are 30 s apart (`14:30:47.79`, `14:31:17.88`, `14:31:47.96`). Knowledge line 30-31 "every 30 s during analyze (2–8 checks per run)" matches: counts are 2,2,3,4,4,4,2,8.
- **Forward fix not landed.** `git show refs/heads/main:.ufo/waves/round-17/tools/carrier-run.py | grep -c map_sha256` returns `0`. Contract `W18/...` item (`.ufo/waves/round-18/contract.md:128-131`) names the in-place change. So the forward-fix sentence is true only after that commit; it must not say "now" before then.
- **QUALITY #19 is the governing rule.** `corpus/QUALITY.md:29` requires the per-path map with its UTC timestamp and verdict for every named instant, including mid-run. With no mid map retained, only the verdict can be admitted for mid-run instants.

## Calibration notes for L1

- The routed-defects check (a) (`.ufo/waves/round-18/contract.md:29-32`) is met by the knowledge line below, since it contains both `R17-PINMAP` and `comparator verdict`. Check (b) is met by the SCORECARD line. Check (d) (`map_sha256` literal in carrier-run.py) stays open until the in-place fix lands.
- Check (c) (a QUALITY.md admission row whose why-cell cites `round-17-verifier-spotcheck.md` and `R17-PINMAP`) is not in the three items assigned to me and is not drafted here. L1 owns it.
- SCORECARD has no round-18 heading yet (`grep -n 'round-18' SCORECARD.md` empty); the L1 creates the placement. The line below is the body only.
- I did not run `routed-defects.py`, which the contract places in W18 and which may not exist yet. Checks (a) and (b) are evaluated by reading the drafted text, not by running the tool.

## Draft

### 1. Knowledge file — append to `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (after line 198)

```
## Round-18 correction — R17-PINMAP mid-run pin maps

Lines 28–33 say that in the second pass "each pin map is retained with its UTC instant: pre, every 30 s during analyze (2–8 checks per run, `steps.analyze.pin_checks`), and post. All maps are equal." That holds for the pre and post maps only. Each mid-run check keeps its snapshot in a local variable and writes `taken_at_utc`, `equal`, `entries` (a count), `changed` and `missing` into `pin_checks` (`.ufo/waves/round-17/tools/carrier-run.py:479-487`). No mid-run map is retained: no `pins/` directory exists under `.ufo/waves/round-17/runs/`.

R17-PINMAP: mid-run instants retain the comparator verdict against the retained pre map, not the map.

Scope: the 29 mid-run checks in the eight second-pass receipts (`.ufo/waves/round-17/runs/*/receipt.json`, `steps.analyze.pin_checks`) all have `equal: true`. So "all maps are equal" reads as "all mid-run comparator verdicts are equal". The pre and post maps (146 entries each, `pins_pre` and `pins_post`) are unchanged. The first-pass receipts at `da64646` kept only pre and post maps, as line 33 says. Under QUALITY #19 (`corpus/QUALITY.md:29`), a mid-run byte claim needs the per-path map, so "identical bytes at those instants" is not admitted for mid-run instants; only the verdict is. This correction does not re-measure any run.

Forward fix: once the round-18 in-place change to `.ufo/waves/round-17/tools/carrier-run.py` is committed, the sentence "carrier-run.py now retains each mid map with map_sha256" is true (mid maps at `DIR/pins/mid-<n>.json`, digest in `pin_checks`, recomputed by `receipt-validate.py`; contract `.ufo/waves/round-18/contract.md:128-131`). Until that commit, the forward fix is not in effect: `git show refs/heads/main:.ufo/waves/round-17/tools/carrier-run.py | grep -c map_sha256` is 0.
```

### 2. SCORECARD — one round-18 line correcting `SCORECARD.md:2374`

```
- Round-18 correction (R17-PINMAP) to the Round 17 capability row at `SCORECARD.md:2374`: "carries pre/mid/post pin maps with instants" is narrowed to pre/post maps with instants. Mid-run instants retain the comparator verdict against the retained pre map, not the map (`.ufo/waves/round-17/tools/carrier-run.py:479-487`; 29 checks across the 8 second-pass receipts, all `equal: true`). Full text and forward fix: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, "Round-18 correction — R17-PINMAP mid-run pin maps".
```

### 3. Forward fix sentence (use only after the in-place commit lands)

```
carrier-run.py now retains each mid map with map_sha256 (`DIR/pins/mid-<n>.json`; `pin_checks[*].map_sha256`; recomputed by `receipt-validate.py`).
```

Pre-commit form, if the L1 must integrate before the commit: "carrier-run.py will retain each mid map with map_sha256 once the round-18 in-place change is committed; `refs/heads/main` has no `map_sha256` yet (`grep -c` = 0)."

## Evidence and commands (all read-only)

- `git rev-parse --verify refs/heads/main^{commit}` → `9011581d84527ba34c675f9cf912e54d2e72d470`.
- `git show refs/heads/main:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | sed -n '28,33p'` → lines quoted in the draft.
- `git show refs/heads/main:SCORECARD.md | sed -n '2374p'` → the row the SCORECARD line corrects.
- `git show refs/heads/main:.ufo/waves/round-17/tools/carrier-run.py | sed -n '479,487p'` and `| grep -c map_sha256` → `0`.
- `git diff --stat refs/heads/main -- corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md SCORECARD.md .ufo/waves/round-17/tools/carrier-run.py corpus/lessons/round-17-verifier-spotcheck.md` → empty, exit 0.
- `git show da64646:.ufo/waves/round-17/runs/{pro-aether,pro-op,calib-shfmt}/receipt.json` (python3 parse) → `pin_checks` absent, `pins_pre`/`pins_post` present, 146 entries.
- Python3 scan of `.ufo/waves/round-17/runs/*/receipt.json` → 29 mid checks, all `equal: True`, pre/post 146 entries each.
- `grep -n` of `PIN_CHECK_S` in `.ufo/waves/round-17/tools/carrier-run.py` → line 37 `= 30.0`.

## Out of scope / not done

- No lane file edited. No jj or git write in the lane. No REA, Ghidra, or carrier execution. No `--selftest` run.
- Not drafted: QUALITY.md admission row (routed check c), SKILL/SOURCES/LOG entries, and the in-place carrier-run.py change itself (owned by the W17/W18 executor).

## Host tooling

- No installs or updates. Read `/home/vgpnk/.omp/agent/RULES.md`; nothing needed installing for read-only parsing (python3 stdlib, git).

Report: `.ufo/waves/round-18/w1/DraftPinmapCorrection.md`
