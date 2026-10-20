# w2 / ToolPinsAntiVacuity — province-pins.py falsification report

Seat: KaidokuR19.ToolPinsAntiVacuity-3 · Round 19 wave 2 · 2026-10-20
Axes: calibration · freshness · depth. No installs performed. No production edits.
All mutations ran in my own clone `/tmp/kr19-w2-ToolPinsAntiVacuity` (no subagents).

## 0. Ground truth observed (freshness)

```
git -C LANE rev-parse refs/heads/main          # exit 0 → 279e8b19c51658bfd05b9e31a1c0894ab2e70537
git -C LANE cat-file -t 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0   # exit 0 → commit
git -C LANE cat-file -e 8a8da7e…:.ufo/waves/round-19/tools/province-pins.py
# exit 1: "path … exists on disk, but not in '8a8da7e…'"  → TOOL_AT_B=absent
git clone -q --no-hardlinks LANE /tmp/kr19-w2-ToolPinsAntiVacuity && \
git -C /tmp/kr19-w2-ToolPinsAntiVacuity checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537
# rev-parse HEAD → 279e8b19c51658bfd05b9e31a1c0894ab2e70537  (observed main tip)
sha256sum clone-tool LANE-tool
# fce2f47df0f1db512a9619a7b0360702f403c97d442c7fcbfdab2a9db062315a  (both identical)
python3 -I -B clone/.ufo/waves/round-19/tools/province-pins.py --selftest; echo rc=$?
# SELFTEST: CLEAN cases=35 / selftest_rc=0
env | grep -c PROVINCE_PINS   # 0 → no fixture overrides active in my environment
```

Observation: the tool postdates baseline B; findings below are against the observed main tip
`279e8b1` (assignment's "observed main tip"), not B. PROVINCE.md changed 8a8da7e→279e8b1
(17 ins/17 del — the C2 rewrite); `PROVINCE_AT_B=present`.

Baseline red state re-measured by me (not trusted from claims):

```
python3 -I -B <clone>/…/province-pins.py --root LANE --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 ; echo rc=$?
# mismatch_count=2 — Devin stated 6.5.0 lines [9,16,44]; OMP 6.5.0 lines [9,17,44];
# Kimi 6.7.0 clean; unstated=[] ; baseline_rc=0
python3 -I -B <clone>/…/province-pins.py --root LANE --rev 279e8b1 [--strict]
# mismatch_count=0, unstated=[], rc=0, strict rc=0 (after-state reproduced)
```

Calibration note (positive): this exactly matches claims.json amendment C2 ("2: Devin, OMP;
3 stale statements each at PROVINCE.md:9,16/17,44") — the declared red state is accurate.

## 1. Findings by severity

### F1 HIGH — three parse shapes silently hide a STALE claim; output identical to the fixed state (mismatch 0, unstated [], exit 0 even under `--strict`)

All three reproduce with a genuinely stale PROVINCE.md that no output field distinguishes from a
correctly fixed one. Driver: `/tmp/kr19-w2-ToolPinsAntiVacuity/mutdrive.py` + `mutdrive2.py`
(commits on top of tip in my clone; probes run `python3 -I -B <clone tool> --root <clone> --rev <mut>`).

| id | mutation (in clone PROVINCE.md at tip) | observed |
|---|---|---|
| F1a | Core row `(Devin/OMP/Kimi 6.7.0 since …)` → `(Devin/OMP 6.5.0. Kimi 6.7.0; …)` — stale bare pins followed by a sentence period | `M9_bare_trailing_period`: rc_plain=0, rc_strict=0, mismatch_count=0, unstated=[], line-44 stated = Kimi only |
| F1a′ | control: same stale pins with `,` instead of `. ` | `M9b_bare_comma_control`: mismatch_count=2 (Devin/OMP 6.5.0 lines [44]), rc_strict=1 |
| F1b | drift Devin pin → 6.5.0 and the words `(historical context)` inserted earlier in the same clause | `M8b_stale_silenced_by_historical`: rc 0/0, mismatch 0, unstated=[], Devin stated only at lines 9,44 (6.7.0) |
| F1c | drift Kimi pin → 6.5.0 and gap "Kimi"→token inflated to 161 chars (newline+160 `x`, no `. `/`;`) | `M6c_stale_beyond_gap`: rc 0/0, mismatch 0, unstated=[], Kimi stated only at lines 9,44 |
| F1c′ | boundary control: gap = 160 (newline+159 `x`) | `M6b_gap160_captured`: Kimi line-18 statement present |

Root cause (observation, tool lines at 279e8b1):
- F1a: `_BARE_STMT` lookahead `(?![\w.])` at
  `.ufo/waves/round-19/tools/province-pins.py:87` rejects a trailing `.`; bare statements ending a
  sentence are silently unmatched (and `_PREFIX_STMT` can't rescue them — no `rea-agents@` token).
- F1b: `province-pins.py:187` (`if "historical" in _clause(text, m.start(), m.end()).lower(): continue`)
  drops ANY current statement whose `_SEP`-bounded clause (:90) contains the substring
  "historical" — one word anywhere in the sentence exempts a live stale claim. Documented as
  design (RULES :96-97), but its interaction with stale pins is silent: no counter, no flag.
- F1c: `_PREFIX_STMT` gap cap `{0,160}?` at :84 — boundary measured exactly at 160/161
  (M6b captured, M6a/M6c dropped). An over-long gap yields NO statement and NO unstated flag as
  long as the client is stated elsewhere at the correct version.

Why this matters (inference): C2's falsifiable form (`… province-pins.py --root LANE --rev REV`,
no `--strict`, measure mismatch count 2→0) cannot distinguish any F1 mutation from the real fix.
`--strict` does not help either (exit 0, unstated empty). A regression that re-stales one region
inside a sentence, bare-with-period, or beyond the gap cap re-opens drift invisibly.

### F2 MEDIUM — deleting all stated clients yields the claim's exact pass observable under the measured (plain) form

```
M1_delete_all_pins:   rc_plain=0 rc_strict=1 mismatch=0 unstated=[Devin,OMP,Kimi]
M2_delete_kimi:       rc_plain=0 rc_strict=1 mismatch=0 unstated=[Kimi]
```

Tool behavior is per contract (RULES :101-103 "strict: exit 1 when mismatch_count > 0 or
unstated_clients is non-empty"; `main` :667-669) — deletion is NOT a clean zero under `--strict`
and `unstated_clients` is reported. The defect is in the claim's measured form: C2's
falsifiable command omits `--strict`, so "0 mismatches, exit 0" is produced identically by a fix
and by stripping statements (assignment's "missing statements must not yield a clean zero" holds
only at strict level). Recommendation (inference): measure `--strict` exit 0 AND
`unstated_clients == []` AND a stated-count floor (≥9 statements / ≥3 per client) in C2's after-state.

### F3 LOW — asymmetric/case-sensitive capture leaves one client of a shared sentence unmeasured

- `M11b_lowercase_hides_stale` (surface `devin, OMP and Kimi all register rea-agents@6.5.0`):
  OMP/Kimi flagged (2 mismatches, rc_strict=1) but lowercase `devin` is silently unmeasured in the
  very same sentence — Devin's stale mention produces neither mismatch nor unstated (he remains
  stated 6.7.0 at lines 16,44). `_CLIENT` :79 is case-sensitive by design; no diagnostic fires.
- `M7_oxford_comma`: group regex :80 stops before ", and" (`M7`: Kimi unstated → strict catches,
  rc_strict=1). Caught, but only via the strict/unstated channel.

### F4 LOW — empty env override silently selects the real operator config

```
PROVINCE_PINS_DEVIN_CONFIG="" python3 -I -B <tool> --root <clone> --rev TIP
# M10_empty_env_override: path=/home/vgpnk/.config/devin/mcp_config.json exists=True version=6.7.0
```

`province-pins.py:276` `os.environ.get(...) or DEFAULT_CONFIGS[client]` — empty string is falsy, so
an "emptied" override falls back to the live config instead of refusing (`exit 2`) or reporting.
Fixture-isolation hazard for any wrapper that unsets-by-empty; docstring :46-48 presents the
overrides as the selftest fixture mechanism without this caveat.

### F5 Verified-correct behaviors (no defect; depth evidence)

- `M3` contradictory duplicate (surface 6.7.0 + drift 6.5.0): 1 mismatch lines [16] — intra-doc
  contradiction is not itself flagged, per RULES :98-100 (only live drift counts). Calibrated.
- `M4` same stale version in two regions: ONE mismatch, lines merged [9,16]/[9,17] — dedupe by
  (client, version) correct, no double count.
- `M5` two stale versions per client (added token in drift tail): 4 mismatches
  (Devin 6.4.0@18 + 6.5.0@16; OMP 6.4.0@18 + 6.5.0@17) — matches the documented
  per-(client, version) rule exactly.
- `M13` structural deletion (drift paragraph removed): exit 2 `region_missing` — structural
  deletion is refused, not a clean zero.
- `M14` unreadable config (chmod 000 fixture): `error=file_unreadable`, `exists` flips false,
  mismatch cause `live_file_unreadable`, rc_strict=1 — named-cause contract holds.
- True-historical omission still works on the real tip doc: baseline/tip runs show lines 12-13
  (`rea-agents@6.5.0` carrier-run sentence without client group; `Historical: Kimi … 6.4.0`
  clause) produce no statements — no false positives there.

## 2. Residual risk and verification gaps

- Gap: I bounded the gap-cap probe to the 160/161 boundary (M6a/M6b/M6c); intermediate lengths and
  dot-containing fillers untested. Inference from the regex: any length >160 behaves like M6c.
- Gap: CRLF/`!`/`?`/unicode-quote `_SEP` boundaries and `m.start("ver")` line attribution under
  CRLF were not exercised; selftest and my battery are LF-only.
- Gap: live configs were read at battery time (sha256/mtime recorded in the probe output); a
  mid-run config change would have skewed `live` but none occurred (mtimes stable across runs).
- Risk (accepted): mutations M1-M13 committed 14 extra commits in my clone only
  (`/tmp/kr19-w2-ToolPinsAntiVacuity`, detached at 279e8b1 + mutation chain; fixtures in
  `/tmp/kr19-w2-ToolPinsAntiVacuity-fixtures/`). LANE untouched except this report.
- Inference, clearly labelled: F1's exploitability against the real pipeline assumes a future
  regression edits PROVINCE.md in one of the three shapes; I did not observe such a regression at
  279e8b1 (tip measures clean, all 9 statements present and 6.7.0).

## 3. Commands (all exit codes inline above)

Drivers: `python3 -I -B /tmp/kr19-w2-ToolPinsAntiVacuity/mutdrive.py` (driver_rc=0),
`python3 -I -B /tmp/kr19-w2-ToolPinsAntiVacuity/mutdrive2.py` (driver2_rc=0, after pinning its
base to 279e8b1 — first run mistakenly read the mutated HEAD as base and hit region_missing rc=2;
rerun on the correct base). Each probe: `python3 -I -B <clone>/…/province-pins.py --root
/tmp/kr19-w2-ToolPinsAntiVacuity --rev <mutation-rev> [--strict]`.
