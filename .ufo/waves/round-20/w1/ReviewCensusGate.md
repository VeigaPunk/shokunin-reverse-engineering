# ReviewCensusGate — `.ufo/gates/c1-census-v10.py` (round-20 w1, read-only seat)

- Written: 2026-10-20T18:05:44-03:00 (clock at write; battery run 18:01–18:05 -03:00).
- Seat: KaidokuR20.ReviewCensusGate-2, read-only; no installs; no lane writes except this report; all probes ran on `tempfile.mkdtemp()` copies under /tmp, removed on exit.
- Target identity: worktree sha256 `7567e36e9206b202…` (846 lines). **The file changed mid-session**: at session start it was `77eb391b4110…` (742 lines, 21 SCOPE rows) and read FAIL; the re-key landed during review first as an uncommitted worktree edit, then commit `808cbb3` put the identical bytes on `refs/heads/main` (verified: `git show refs/heads/main:.ufo/gates/c1-census-v10.py | sha256sum` = `7567e36e9206b202`). All line cites are against the 846-line version. Prior-version facts are labelled (pre-rekey).

## 1. Observed state arc (all commands pasted with exits)

```
$ git rev-parse refs/heads/main            # session start
d1d981d2cc041dda4656c5b01d2c8445d8d17124   # exit 0
$ python3 -I -B .ufo/gates/c1-census-v10.py --root . --quiet   # pre-rekey gate
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0) # EXIT=1
# undeclared: SCORECARD.md block 2380-2382 (bare 6.5.0 @:2380, 6.7.0 @:2381);
#            SKILL.md block 511-519 (bare 6.5.0 @:512) — both scope None
$ git blame -l refs/heads/main -L 2379,2383 -- SCORECARD.md   # provenance
8e7642c / d0ab299 (2026-10-20 round-19 integration) — the "Round 17" records band
$ python3 -I -B .ufo/gates/c1-census-v10.py --root . --quiet   # post-rekey gate
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0) # EXIT=0
# G2: current-ok per file PROVINCE.md=16 SCORECARD.md=13 SKILL.md=3; frontier 14 rows, 0 errors
$ python3 -I -B .ufo/gates/c1-census-v10.py --selftest
SELFTEST: CLEAN cases=3   # EXIT=0 (shifted_scope_anchor, live_value_not_sheltered, new_undeclared_block_fails)
```
Observation. The pre-rekey FAIL is exactly the D4/D5 debt claims.json C1 names ("c1-census-v10 VERDICT FAIL/exit 1 -> PASS/exit 0 at the delivered tip", `.ufo/waves/round-20/claims.json:16`).

## 2. What PASS requires (calibration)

- Precondition: all three client configs must yield a `rea-agents@x.y.z` pin, else `ANCHOR-FAIL` exit 2 (`:735-736`). [obs]
- `ok` conjunction `:801-802` (= docstring `:232-235`): `stale==0 AND ambiguous==0 AND undeclared==0 AND unresolved==0 AND scope_errors==0 AND g11==[] AND g2_ok AND no unreadable scoped file AND frontier_errors==0`. [obs]
- `scope_errors` has two sources: stable-anchor resolution errors (`:750`) and DATED marker assertions (`:762`, G15/G18 at `:441-462`).
- Exit mapping: 0 PASS, 1 FAIL, 2 anchor failure (`:845`, `:735-736`); `--json` mirrors the verdict exit. [obs]
- G7 (configured != held) is warning-only — collected `:661-662`, printed `:833`, not in `ok`. [obs]
- G20 floor (`:795-796`): `all(floor[f] > 0 …)` — every readable scoped file needs ≥ 1 current-ok DETECTION; unreadable files exempt (they already force FAIL via G19).

## 3. How SCOPE rows are graded (coverage)

Row = `(file, start, end, CURRENT|DATED, marker_line, marker_regex)` (`:255`, 23 rows). Grading is **per-locus, not per-row** [obs]: `units()` folds prose into blocks; `REA_GATE` prefilter; PIN/VER/PTR occurrences mapped to physical lines (`line_of`); `scope_of` finds the containing row; per-occurrence ladder `:609-633`:
- client-attributed value == live anchor → `current-ok`; else DATED-scope or same-line inline marker → `historical`; else `STALE`;
- ptr stale inside DATED → `historical "dated scope"`; no-client clause → G17 version-intrinsic cache check or `AMBIGUOUS`;
- G16 `:628-632` promotes `historical`→`current-ok` when the value equals **any** live anchor (`6.4.0` excepted — magic constant, see F3).
Block rollup priority `:638-651`: UNDECLARED > STALE > UNRESOLVED > AMBIGUOUS; mixed historical/current-ok → `info` (non-failing); `current-ok` blocks require RECEIPT language (G11) else fail. DATED shelter is the load-bearing danger: any non-live value inside a DATED row reads `historical` and can never fail the run — so the **truth of the class** is the crux of every re-key. [obs code; inference for the emphasis]

## 4. Re-key: declaration vs suppression (depth)

**Declaration — what landed, and it is load-bearing** [obs]:
- `scope-diff.py` (CR-5 tool) d1d981d→landed: `rows before=21 after=23`, `ADDED (2)`: `SCORECARD.md 2374-2382 DATED marker_line=2374 marker="round-17"`, `SKILL.md 511-519 DATED marker_line=511 marker="r17-go-carrier-diagnostics"`; `REMOVED (0)`, `CHANGED (0)`, `CREEP FLAGS: []`, diff-exit 1 (change, not creep). Both ranges are tight to the two round-17 record blocks; both markers carry the section's own token on a line inside the range (G18); both blocks are records of the past round-17 measurement, so DATED is their true class. [obs + inference on class truth]
- Counterfactual: flipping both new rows to CURRENT → `VERDICT: FAIL (ambiguous=2)`, exit 1 — CURRENT misclass is self-punishing here (no client token in clause → AMBIGUOUS), so DATED is the only passing class and the declaration does real grading work. [obs]

**Suppression shapes** (keep/produce PASS without declaring):
- S1 delete/shrink rows or drop a file from SCOPE — loci vanish silently (classify never sees the file); differ's REMOVED report is the only witness. D4 forbids. [obs code]
- S2 CURRENT→DATED flip of a reconciled surface — shelter follows; creep-flagged; refused precedent in the instrument header (`:38-40`). [obs]
- S3 widen a DATED end or add a wide/to-EOF band — launders everything inside under one marker ("Tail expansion" refused `:27-34`; planted `rea-agents@6.3.0` in DATED reads historical → PASS, per header). Differ flags end-widening of CHANGED rows and ADDED rows >150 lines. [obs]
- S4 marker gaming — marker line outside its range (G18 `:454`), stripped marker (G15), or a strength-free regex like `r"."`: the differ parses the regex string but never judges marker strength; the standing rule (`:41-43`) requires the section's own date/round token. Measured: stripping all 3 `round-17` occurrences on `:2374` → `SCOPE-ERRORS: ["SCORECARD.md:2374 marker 'round-17' absent …"]`, FAIL exit 1. [obs]
- S5 **inline-word laundering (live channel, measured)**: a locus past the bound carrying `historical|not re-probed|superseded|baseline|…` on the same physical line reads `historical` (`:611`) and is exempt from UNDECLARED (`:638` exempts `disp=="historical"`). Probe: appending ` (historical)` to SCORECARD `:2380,:2381` and SKILL `:512` dropped `undeclared 2→1` — the 6.5.0 dets stayed silenced; the 6.7.0 det re-armed only because G16 promotes it (6.7.0 == live) back to current-ok, which re-fires UNDECLARED. So the word trick fully launders non-live-valued loci; live-equal values need the value text altered too (a visible diff). This is the header's named-not-closed H2 residual (pre-rekey header `:82-84`; unchanged). A records commit can launder by word choice; only the external diff/locus audit sees it. [obs probe; inference for the generalization]
- S6 anchor-rotation watch item: the new stable-anchor mechanism (`scopes_by_file`, `:738-762`; selftest `shifted_scope_anchor`) resolves volatile ranges by text anchor — I did not fuzz it; flagging as a watch item, not a defect. [inference, unmeasured]

## 5. The anti-vacuity test a rekey must keep

**Primary (in-instrument, must survive byte-identical): G2/G20 per-readable-file positive floor** — after the rekey, `g2_ok` true with `current_ok_per_file` all > 0 in `--json`, counted over current-ok **detections, not blocks** (`:788-796`); the floor unit must not be re-keyed (per-row, per-block, and global variants are all measured-refuted in the comment `:765-779`). Landed measurement: PROVINCE 16 / SCORECARD 13 / SKILL 3. This is the tripwire that makes "declare everything historical" laundering FAIL (a whole-file DATED flip zeroes the file's floor → BLIND-INSTRUMENT).

**Four negative controls, each must FAIL after any rekey** (all re-measured against the landed instrument, exit codes observed):
1. marker strip → SCOPE-ERROR, FAIL exit 1 (§4 S4);
2. past-bound growth (locus line appended at SCORECARD EOF) → UNDECLARED, FAIL exit 1;
3. stale needle in a CURRENT row (`rea-agents@6.7.0`→`6.0.0` in PROVINCE.md) → FAIL stale=2 exit 1;
4. scoped file removed → `DECLARED FAIL CLASSES: ['UNREADABLE']` + marker-uncheckable, FAIL exit 1.

**External certificate** (the instrument cannot certify its own rekey — H4): `scope-diff.py` before/after with 0 CREEP FLAGS, additions only, plus a manual check that no ADDED/CHANGED DATED row's end equals the file's line count (see F1), plus locus-count invariance on untouched surfaces.

## 6. Findings by severity

- **F1 (medium, differ tool)** — `scope-diff.py:6` documents an open-ended flag "end >= 9000 **or end is the last line of file**"; the code (`:40-43`) implements only `e >= 9000` and ADDED-row width >150. Measured: an ADDED `("SKILL.md", 505, 623, "DATED", …)` row (ends at EOF 623, 119 lines) gets `CREEP FLAGS: []`, diff-exit 1; the gate run on that variant still FAILed (undeclared=1 — only the SKILL block was laundered; the SCORECARD block remained), but a two-block laundering rekey would PASS differ-clean. Compensating control until fixed: assert `end != line_count(file)` for every ADDED/CHANGED DATED row. [obs]
- **F2 (medium, gate; named residual, still open)** — same-line inline-marker excusal (§4 S5) launders past-bound loci without any declaration; measured partial silence 2→1 undeclared. The records-commit standing rule (`:41-43`) is the only guard. [obs]
- **F3 (low, calibration)** — G16's hardcoded `6.4.0` exemption (`:630-631`) is a baked constant with no inline rationale; if live ever returns to 6.4.0, DATED 6.4.0 mentions stay historical (probably intended) but the carve-out is undocumented and unaudited by the differ. [obs code; inference on intent]
- **F4 (low, dead code)** — `n_current_ok` (`:782-784`) is computed and never used; the floor uses the per-file `floor` dict. Dead weight. [obs]
- **F5 (info)** — the landed floor count SCORECARD=13 includes a G16-promoted detection inside a DATED row (`:2381`, "REA 6.7.0 adds no keep-log knob" → current-ok "value equals a live anchor"). A future live bump 6.7.0→6.8.0 drops it to historical and the floor to 12 — no break (>0), but floor counts are version-sensitive; the >0-per-file rule is what is load-bearing. [obs counts; inference on consequence]
- **F6 (info)** — PASS does not require `g7==[]` (warning-only); docstring and code agree; stating it because "what PASS requires" is easy to over-read. [obs]

## 7. Residual risk and verification gaps

- PASS is measured at commit `808cbb3` bytes; the wave is still landing — D4/D5 require the gate re-run at the final delivered tip (claims C1 `counting_command` already names it).
- S5 probed only for bare-version loci; pin/ptr laundering variants unprobed. [gap]
- F1's manual to-EOF check is not automated anywhere in-repo. [gap]
- The stable-anchor path (S6) and `--selftest` case coverage beyond the 3 built-ins were not fuzzed. [gap]
- No tool installs were made (none needed).

Report: .ufo/waves/round-20/w1/ReviewCensusGate.md
