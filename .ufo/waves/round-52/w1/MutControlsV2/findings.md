# MutControlsV2 — dead-control table for round-52 (w1)

Scope: every control named in `plans/round-52-claims.md` (R52-C1 pre-freeze controls and rule
mutations M1–M4; R52-C2 controls), plus the r50 driver `ExecControls/c1-controls.py`.
All numbers below are measured offline on committed lane bytes (read-only) unless marked
`[INFERENCE]` or `[code-read]`. No REA run, no download, no lane write, no git mutation.

Probe sources (scratch copies in this seat dir): `probe_disposition.py`, `probe_law_surface.py`,
`probe_failclosed.py`, `probe_carrier_set.py`, `mutation_probe.py`; receipts in `receipts/`
(`SHA256SUMS`), `mutation-probe.json`. Each probe imports the round-50 counter's own
`parse_nonregular`, `gap_rule_model`, `subject_root`, `disposition_check`, `nonregular_published`.

Terminology: "disposition verdict" = `gaps_ok AND nonregular_unpublished_ok` for one carrier, which
is the only thing the claims' pre-freeze controls can observe. "Arm" = one control.

---

## 0. Headline findings (read first)

1. **No claimed control detects the central defect class.** Mutant M-DEFECT-1 (`mutation_probe.py`:
   the counter treats an empty `allowed[kind]` as allow-all) moves exactly one arm: the injected
   device-gap arm DEVGAP goes 0/4 -> 4/4. CTL-OLD (2->2), CTL-NEW (4->4), M1 (4->4), CTL-JUNK (0->0),
   M2law (4->4), M2white (0->0) are all **unchanged**. DEVGAP is not in the claims' control list.
2. **The disposition layer cannot tell the law from a permissive rule.** Rule with
   `required` all false and every gap kind allowed scores 4/4 (`probe_failclosed.py` F). CTL-NEW's
   green therefore says nothing about shape.
3. **M1's expected RED is unreachable in the current draft.** Under the round-50 disposition
   logic, the all-thirteen whitelist scores **4/4 GREEN** (`probe_law_surface.py` B). Its only
   witness is `law_shape_ok`, which does not exist: `grep -c law_shape_ok ExecCounterV2/c1-counter.py` = 0.
4. **Identity is not bound.** Of 35 four-carrier multisets, 9 pass both CTL-OLD (2/4) and CTL-NEW
   (4/4); 8 of those 9 score the wrong carrier set (`probe_carrier_set.py` Q1). CTL-NEW alone is 4/4
   for four copies of one carrier (`{c6430 x4}`, `{g7581 x4}` under LAW) [measured in probe H].
5. **The before-arm and the predicate command, as written, cannot run.** `--table tools/round-50-c3`
   does not exist in v5 (argparse exit 2, verified). `--freeze` must be an ancestor of `--rev`; the
   claims-draft base `ab0eafe` with the round-52 freeze as `--freeze` exits 2 (verified). Before-arm
   must omit `--freeze` (or use `c525de54`) and must read the v5 table via `--rev`.
6. **Predicate-level: `census_outside` will not be 0 at landing unless `census3.json` is
   regenerated in the freeze commit.** Simulated (not committed): 56 registry paths + the 7
   round-52 instrument rows, census not regenerated -> `census_outside` 7, exit 1. Regenerated -> 0.
   The claims name no regeneration step.
7. **The controls depend on a mode that does not exist.** `tools/round-50/c1-counter.py` has no
   `controls` subcommand (0 matches for `add_subparsers` / `'controls'`); ExecCounterV2 is marked
   `failed`. No pre-freeze arm is runnable as written.

---

## 1. R52-C1 controls — per-arm table

Expected verdicts are the claims' values. "Observed" is the measured value from the probes.

| # | Arm | Claimed work it stands for | What it observes | Claimed expected | Observed | How it passes while the claim is false | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **CTL-OLD** (r50 rule, `gap-rule.json`) | reproduces the committed miss; proves the r50 rule fails FRITZ!Box | disposition verdict over `corpus/evidence/round-50/c1/*/after.json` | 2/4, exit 1 | **2/4** (c6430 T, c6490 T, g7581 F, g7582 F) — matches `RevGrammarOffline` and my probe | Any multiset with two cable members scores 2 (see §0.4); the arm never binds which carriers were scored. It also reproduces only the `gaps_ok` cause: the committed `c1-after-attempt2.json` g7581 also fails `projection_ok` (`matched false`, failing `[gaps_ok, matched, projection_ok]`), which this arm cannot reproduce. The claim's "reproducing the committed miss receipt" is over-stated. | **Weak**: reproduction only; no identity binding; over-claimed scope |
| 2 | **CTL-NEW** (law rule) | derivation consistency | disposition verdict, same envelopes | 4/4, exit 0 | **4/4** | (a) **Overpermissive rule** (`required` all false, all gap kinds allowed) -> 4/4 (probe F). (b) **Shape-neutral mutants**: `allowed[char-device] = [unpublished-entry]` -> 4/4 (probe E); a non-empty `removed.silent` device list with `required[char-device]=false` is disposition-neutral [code-read: `disposition_check` consults `silent` only when `need` is true, lines ~1552–1559]. Only `law_shape_ok` could red these. (c) **Identity**: `{c6430 x4}` and `{g7581 x4}` both 4/4 under LAW (probe H). | **Dead** for shape and identity; weak as a law control |
| 3 | **CTL-DN** (do-nothing, absent receipts) | semantic red | exit code only | exit 1 or 2 | not run; driver `ExecControls/c1-controls.py` line: `if name == "CTL-DN": ok = result.returncode in (1, 2)` | **Any crash passes.** The driver ignores the payload for this arm, so a counter that exits 2 on every input (import error, bad argv, missing mode) is green. r50's CTL-C1-0 required exit 1 with `carriers_matched 0`; r52 dropped that. | **DEAD** |
| 4 | **CTL-JUNK** (all kinds required, impossible allowance) | junk rule scores 0/4 | any gaps_ok failure | 0/4, exit 1 | **0/4** (reds on "gap kind 'unpublished-entry' not allowed for 'symlink'") | Any counter whose `gaps_ok` is always False passes; but CTL-OLD=0 for that counter too. Its failure reason is the symlink allowance, not any device logic. | **Redundant with CTL-OLD** |
| 5 | **M1** all-thirteen detail whitelist | red by `law_shape_ok` | disposition verdict (law_shape_ok not in the draft) | RED | **4/4 GREEN** under disposition; `law_shape_ok` absent (0 hits) | Passes everything the draft implements. Red iff `law_shape_ok` exists and is correct; the claim does not say which M1 clause fires. | **DEAD until `law_shape_ok` exists**; needs its own mutant test |
| 6 | **M2** 14th unlisted device (`dev/ttyS0 4:64`) | law GREEN, whitelist RED | (a) full counter on a fixture carrier; (b) my proxy: row appended to nonreg | law 4/4, whitelist 0/4 | (b) law 4/4 (M2law), whitelist 0/4 (M2white) | (a) **Not executable pre-freeze**: scoring a fixture carrier needs the counter-time REA rerun (`projection_ok`), which the claims forbid pre-freeze. (b) the law GREEN half is **tautological** (devices carry no disposition, so a device row can never fail the law); it tells nothing about the counter. Fixture is buildable: `mksquashfs -pf` with `dev/ttyS0 c 644 0 0 4 64` yields `crw… 4, 64` (verified); `sqfs-list.py --files` emits `4:64`. | **Not executable pre-freeze**; green half tautological; whitelist half OK |
| 7 | **M3** (regression: `required char-device=true`, silent `247:0`) | reproduces 2/4 | disposition verdict | 2/4 | 2/4 | Identical to CTL-OLD on all four carriers (probe G, `identical=True` x4). Adds no discrimination. | **Redundant with CTL-OLD** |
| 8 | **M4** (strict-subset whitelist) | red (M50 partial-widening trap) | disposition verdict | 0/4-ish, exit 1 | 0/4 (`required entry with no disposition`) | Red for the same mechanism as M3 (`required=true`, unaccounted rows). It does not exercise the silent path separately. | **Redundant with M3** |

---

## 2. R52-C1 — controls that are MISSING

Each row names the defect the claims' control set cannot see, with the measurement.

| ID | Missing control | Why it is needed (measured) | What the control must assert |
|---|---|---|---|
| MISS-1 | **Carrier identity / wrong carrier set** | 8 of 9 multisets pass CTL-OLD=2 and CTL-NEW=4 while scoring the wrong set (probe Q1). The claimed count-only controls cannot tell `{c6430,c6490,g7581,g7582}` from `{c6430 x2, c6490 x2}`. | Score receipts whose subject pin does not match the carrier slot (e.g. g7581's receipt in the c6430 slot) -> red on `subject_pin_ok`; assert set equality of carrier ids with `carriers.json`. |
| MISS-2 | **Foreign-round / wrong-round receipt** | Pre-freeze controls waive `run_provenance_ok`, `receipt_fresh`, `carrier_pin_ok` by design (claims F2). So **no pre-freeze control binds provenance at all**. `provenance_ok` is a pure prefix test on `output_directory` (verified in the r50 counter at line 1061) and is cheap to exercise offline. | Plant round-41 V3/V4 big-endian receipts (or any receipt with a non-`/fast/scratch/hyaku/kaidoku-r50` output_directory) in the r50 slots -> red on `run_provenance_ok`; plant a receipt with `after.json` from a commit that does not descend from the freeze -> red on `receipt_fresh`. |
| MISS-3 | **Device fail-closed fixture** (the law's own clause) | **0 of 28** device census rows carry any gap in the committed corpus (probe Q2). The law clause "a gap on a device row is a violation" has no witness. DEVGAP is the only arm that detects M-DEFECT-1 (see §0.1). | Inject an `unpublished-entry` gap on a char-device row (`dev/led`) into a committed envelope -> red under the law rule (`gap kind 'unpublished-entry' not allowed for 'char-device'`, verified: probe D and DEVGAP). Must be added to the control set. |
| MISS-4 | **Shape-neutral mutants** | `allowed[char-device]` non-empty (probe E: 4/4) and device `silent` with `required` false (code-read) are disposition-neutral. Only `law_shape_ok` can red them. The claims list only M1. | Two mutants, each must be RED under `law_shape_ok`: (i) `allowed[char-device]=[unpublished-entry]` with `required` false; (ii) `removed.silent` naming a device kind with `required` false. |
| MISS-5 | **Retry-policy controls** | The claims require a deterministic-ENOENT control (red after all attempts) and "a rerun failing with any other error is red". Neither is in the claim's control list or the driver's `CONTROLS` tuple. Without the ENOENT control the retry clause can green-wash a real failure. | (a) deterministic-ENOENT fixture tree -> red after 2 attempts, attempt count and diagnostic recorded; (b) non-ENOENT `execution_failure` -> 0 retries, red; (c) `provider_timeout` -> up to 3 attempts. |
| MISS-6 | **Census re-derivation (F7)** | No control. **Format trap measured:** `unsquashfs -lln` emits device details as `4, 64` (comma-space; verified on a fixture); the committed oracle and `sqfs-list.py` use `4:64`. A re-derivation that compares details verbatim cannot match the frozen table. | A device detail mismatch -> red on `census_rederived_ok`; the normalised form (`major:minor`) must match the committed `*.nonregular.tsv` both directions. |
| MISS-7 | **depth_gap_recorded (F8)** | No control. Verified: every `depth-limited` gap has `relative_path: null` and `input_path: "$output/firmware.bin_extract"` in g7581/c6430. Entries under an unreached subtree are indistinguishable from "reached, no gap" (the claims' own stated limit). | A receipt lacking `input_path` or `continuation_id` on its `depth-limited` gap -> red on `depth_gap_recorded`. |
| MISS-8 | **Positive control of the full counter pre-freeze** | r50's CTL-C1-POS was the arm that exposed the g7581 miss (exit 1, 2 carriers). The r52 pre-freeze set has no positive arm for the full predicate; the data run is the only positive. | State explicitly that pre-freeze arms are rule-scoped and that the full-counter positive exists only post-freeze; or add a fixture that exercises every clause offline. |
| MISS-9 | **Freeze-drift (routed defect 3)** | Named as a selftest in the claims, but absent from the pre-freeze control table. | Mutated frozen byte at REV -> exit 2 with `frozen_path_changed` naming the path. |

---

## 3. R52-C2 controls — per-arm table

Observed numbers: v5 table at `ab0eafe` and `c525de54` (same SKILL.md bytes, sha256 `874d7292…`):
`pair_mismatches 0`, 126 envelopes, exit 0 (`receipts/v5-corpus.json`,
`receipts/v5-before-frozenc.json`). The r51 battery (`.ufo/waves/round-51/w1/MutTriV6/battery.md`)
measured D2 = 1 at base, D3 = 13 at base — those numbers are the r51 census state and are not
re-derived here.

| # | Arm | Claimed work | What it observes | Pass-while-false | Verdict |
|---|---|---|---|---|---|
| C2-A | **do-nothing** (v5 table at base -> audit red) | audit catches the ddwrt route | D2 on the FAILED body | It is the same measurement as the before-arm. An audit that flags any ddwrt FAILED body passes this without checking the action. | **Redundant with before-arm** |
| C2-B | **junk table** (wrong labels -> `pair_mismatches > 0`, exit 1) | evaluator/table comparison works | D1 only | Covers only D1. A coordinated table+evaluator change (the r51 M1 class, measured `D1 1 / D2 0` for the no-row deletion) is invisible to it. | **Redundant with D1; does not touch the audit** |
| C2-C | **audit-guard-deleted** -> red | audit is fail-closed | exit code | A deleted audit call that leaves `executability_violations = 0` as a default exits 0 and reads as a pass. The r51 battery required a receipt key and exit 2 `audit_missing` (its M11); the r52 claim text states neither. | **Weak until the fail-closed gate is specified** |
| C2-D | **swapped-new-row-action** -> red | action mutant | D1 and D2 both fire (r51 M2: 1 / 1) | Caught by D2 alone for the action; a second witness, not an independent one. | **Redundant with D2, acceptable** |
| C2-E | **census-guard-deleted** -> red | census guard is fail-closed | exit code | Same shape as C2-C: a deleted census comparison defaulting to `census_outside 0` exits 0. Needs a `census_missing` exit 2 gate and the receipt key. | **Weak until the gate is specified** |
| MISS-C2-1 | **Precedence / row-placement** control | the ddwrt route only holds if the new row sits **below** `legacy-body-failure` | r51 battery §1 measured: new row placed **above**, legacy glob broadened to `squashfs_v[123]*` -> D1 0, D2 0 (GREEN, a no-op) | Without a placement arm, a mis-ordered table is green. | **Missing**; add the r51 precedence mutant with its measured expectation (below -> red) |
| MISS-C2-2 | **Before-arm command** | the claims' before-arm (`--table tools/round-50-c3`) | `--table` is not a v5 flag (verified, argparse exit 2); `--freeze` descendant of `--rev` exits 2 (verified) | The before-arm as literally written exits 2, not 1, and the kill rule would misread an instrument error as a claim miss. | **Defect in the claim's command** |
| MISS-C2-3 | **Mis-frozen expectations from r50** | CTL-DN and CTL-ACT numbers | r51 battery: CTL-DN D1 19 -> 20 and CTL-ACT 51 -> 52 under the v6 evaluator (the ddwrt route moves one pair) | Re-using the r50 receipt numbers as v6 expectations makes two arms read as misses | **Risk**; freeze the v6-evaluator numbers |

---

## 4. Predicate-level defect (not a control, but it kills a control)

**census_outside at landing.** Simulated with the lane's own `census3.compare_paths`:
the seven round-52 instrument rows the claims require (`tools/round-52/{gap-rule.json,
c1-counter.py, c1-controls.py, c1-run.sh, fetch-vendor.py, sqfs-triage-v6.py, misroot-sweep.sh}`)
are absent from the committed `census3.json`. With the registry grown and the census not regenerated:
`registry_paths 63, census_paths 56, census_outside [7 paths], exit 1`. With the census regenerated
from the staged SKILL.md: `63/63, census_outside [], exit 0`. The claims require `census_outside 0`
at the landing REV and name no regeneration. [INFERENCE on the freeze-commit ordering; the arithmetic is measured.]

---

## 5. Recommended changes to the claims (for the L1 to decide; not applied here)

1. Replace CTL-DN's `exit 1 or 2` with exit 1 + `carriers_matched 0` + `receipt_present` false named.
2. Add DEVGAP (MISS-3) and make it a required red; add the identity control (MISS-1), the
   foreign-round receipt control (MISS-2), and the shape-neutral pair (MISS-4).
3. Specify `law_shape_ok` and its mutant tests before M1 is claimed; state which clause M1 reds on.
4. Retire CTL-JUNK (redundant with CTL-OLD) and M3/M4 as separate arms (keep one regression arm).
5. Fix the R52-C2 before-arm: drop `--table`, drop `--freeze` (or use an ancestor), and name the v6 precedence mutant.
6. Add the census regeneration step to the freeze commit, or change the landing predicate.
7. Add the audit and census fail-closed gates (exit 2 + receipt key) to the C2 control text.

---

## 6. What was not run (honest limits)

- No REA invocation, no `--data-run`, no carrier download, no network (per contract).
- The full counter's controls mode does not exist; all counter-level arms above were replaced by
  rule-scoped probes that import the round-50 counter's own functions. Results are therefore
  rule-scoped, not full-predicate.
- The M2 fixture image was built in scratch only and was not scored by the counter (requires a rerun).
- `[code-read]` items (silent-consulted-only-when-required; the driver's CTL-DN `in (1,2)`) were read,
  not executed as separate probes.
- No tool was installed or upgraded in this seat.
