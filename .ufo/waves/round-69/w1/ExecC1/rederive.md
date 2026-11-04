# rederive.md — R69-C1 re-derived with ExecC1's own patch applier

Seat `ExecC1` (executor, round-69 / w1 / attempt 1). Claim attacked as frozen: **R69-C1**.
Targets (read-only, never edited): `tools/round-69/packed-elf.py`, `tools/round-68/packed-elf.py`.
Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`; operative freeze
`f15998102f1ce3569e61faa2ac6f286bc414538e` (the commit that first adds `.ufo/waves/round-69/claims.json`).
Environment: Python 3.14.8, Linux 7.2.11-arch1-1, lane HEAD `3f3d20fc065b5be62f676028b9a38d316ddfe8fd`.

No file of `tools/round-69/`, `tools/round-68/`, the fleet repo, another lane or the jj/git index was
written. `git status --porcelain -- tools/round-69 tools/round-68` in the lane is empty (observation).
All mutation happened on scratch copies under `/fast/scratch/hyaku/kaidoku-r69/ExecC1/`, removed at yield.

## 1. Provenance — the bytes actually scored

| object | source | sha256 | pin | match |
|---|---|---|---|---|
| r69 route | `git show f159981:tools/round-69/packed-elf.py` | `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` | `claims.json.instrument_pins` | yes |
| r68 route at base | `git show d7d9a62:tools/round-68/packed-elf.py` | `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` | `c1-at-base.json.target_sha256` | yes |
| r68 route at freeze | `git show f159981:tools/round-68/packed-elf.py` | `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` | same bytes as base | yes |
| r69 route on disk | worktree file | `4ac0d83b…` | equal to the freeze blob | yes |
| mutation battery (cross-check only) | `git show f159981:tools/round-69/mutation-check.py` | `51b64c56c48899d5d2d707298431861f8465e5422e53ee7dceb903d1b56d33c2` | `instrument_pins` | yes |

`git diff f159981..HEAD -- tools/round-69/packed-elf.py` is empty → no post-freeze edit of the
instrument up to the current lane HEAD (observation, exit 0, no output).
`git cat-file -e d7d9a62:tools/round-69/packed-elf.py` fails (rc 128, "exists on disk, but not in") →
the after-arm has no base-revision object; the before-arm must run the r68 file, which is what the
frozen sentence says (observation).

## 2. Method — an applier that shares no code with `mutation-check.py`

`mutapply.py` (this directory) is written for this seat. It does not import, shell out to, or read
`tools/round-69/mutation-check.py`; its patch strings were derived by reading the two frozen blobs.
For each (blob, family) it asserts the old text occurs **exactly once**, writes the mutant copy,
computes its sha256, runs `python3 -I -B <copy> --selftest`, parses the JSON payload from stdout or
stderr, and classifies with its own spelled-out rule:

* `rc == 0 and ok is True` → **survived**
* parsed payload and `expect_case in failed` → **killed_named**
* parsed payload and the declared case absent → **killed_other_cases** (a kill that does not name its
  case is not the kill the predicate asks for)
* no parsed payload (syntax/import/KeyError) → **unevaluable_no_payload** (a crash is not a gate)
* patch site matching 0 or >1 times → **patch_site_N_matches** (refused, never a silent no-op)

Two families per blob so the result does not depend on the battery's mutant strength:

* **constant** — each arm expression replaced by the literal `True`; the gate is blind. This is the
  strongest kill target a selftest can be handed and the reading the seat card gives
  ("patch the expression to a constant").
* **literal** — the exact textual mutants the frozen battery's patch sets `r68`/`r69` declare, typed
  out again here, so the battery's own patch table is independently match-counted and re-run.

Every family was run twice on the same pristine copy; the two pristine selftest transcripts are
byte-identical (`det-r69-1.json` == `det-r69-2.json`,
`642e777eae597d01dd8d720eff853a35bf5776e6ff6e8c48dcaecc3deeae41a6`; `det-r68-*` ==
`cc5ce534f105aa4c330a5df7f4a39125dad17528390755c679f88f92395e5b0d`) → deterministic (observation).

## 3. Patches actually applied

### r69 — `evaluate_carrier()` in `tools/round-69/packed-elf.py` (lines 155–175)

| id | declared case | old text | new text (constant family) |
|---|---|---|---|
| M1_identity | `arm-pack-identity-false` | `identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]` | `identity_ok = True` |
| M2_recovery | `arm-pack-recovery-false` | `recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]` | `recovery_ok = True` |
| M3_detected | `arm-pack-detected-false` | `detected = model["upx_list_rc"] == 0 and model["section_count"] == 0` | `detected = True` |
| M4_before | `arm-pack-before-false` | `before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]` | `before_ok = True` |
| M5_control | `arm-pack-control-false` | `control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0` | `control_ok = True` |

Literal family differs only at M2/M3/M4 (they drop one conjunct instead of collapsing to `True`):
M2 → `recovery_ok = bool(model["recovered_counts"])`, M3 → `detected = model["upx_list_rc"] == 0`,
M4 → `before_ok = model["packed_procedures"] is not None`. M1 and M5 are identical in both families.

### r68 — `score()` in `tools/round-68/packed-elf.py`

| id | old text | new text (constant family) |
|---|---|---|
| M1_identity | `identity_ok = (unpack["rc"] == 0 and os.path.exists(unpacked)` + continuation `and sha256_file(unpacked) == c["sha256"])` | `identity_ok = True` |
| M2_recovery | `recovery_ok = bool(rec_counts) and rec_counts == orig_counts` | `recovery_ok = True` |
| M3_detected | `detected = listing["rc"] == 0 and secs == 0` | `detected = True` |
| M4_before | `before_ok = before_procedures is not None and before_procedures < floor` | `before_ok = True` |
| M5_control | the two-line `fold(carriers, all(c["control"]["list_rc"] != 0 and c["control"]["decompress_rc"] != 0` / `for c in carriers), len(CARRIERS))` | `fold(carriers, True, len(CARRIERS))` |

Literal family is the battery's own text: M1 `and sha256_file(unpacked) == c["sha256"])` → `and True)`,
M2 `and rec_counts == orig_counts` → `and rec_counts == rec_counts`, M3
`detected = listing["rc"] == 0 and secs == 0` → `detected = listing["rc"] == 0 and True`,
M4 `and before_procedures < floor` → `and before_procedures == before_procedures`, M5 as above.

## 4. Result matrix — every run, rc and failed list

Pristine r69: `cases 20`, `failed []`, `ok true`, rc 0.
Pristine r68: `cases 13`, `failed []`, `ok true`, rc 0.

### r69 constant family — after-arm (blob `4ac0d83b…`)

| mutant | site matches | mutant sha256 | rc | cases | failed | verdict |
|---|---|---|---|---|---|---|
| M1_identity | 1 | `614b1ea356dc7355…` | 1 | 20 | `['arm-pack-identity-false']` | killed_named |
| M2_recovery | 1 | `d3ba75ad3fe02d39…` | 1 | 20 | `['arm-pack-recovery-false']` | killed_named |
| M3_detected | 1 | `97fcce5bbc6e53f5…` | 1 | 20 | `['arm-pack-detected-false']` | killed_named |
| M4_before | 1 | `1a8a7511932547e1…` | 1 | 20 | `['arm-pack-before-false']` | killed_named |
| M5_control | 1 | `0e1bb2bbaa366c28…` | 1 | 20 | `['arm-pack-control-false']` | killed_named |

Survivor set: `[]`. Every kill names exactly its declared arm-false case and **only** that case — no
collateral case fails, so the binding is one-case-per-arm (observation).

### r69 literal family — the battery's own patch text

| mutant | site matches | mutant sha256 | rc | cases | failed | verdict |
|---|---|---|---|---|---|---|
| M1_identity | 1 | `614b1ea356dc7355…` | 1 | 20 | `['arm-pack-identity-false']` | killed_named |
| M2_recovery | 1 | `e16654ef53fab4fa…` | 1 | 20 | `['arm-pack-recovery-false']` | killed_named |
| M3_detected | 1 | `88b9fb051170132a…` | 1 | 20 | `['arm-pack-detected-false']` | killed_named |
| M4_before | 1 | `295eda9adf2cab0a…` | 1 | 20 | `['arm-pack-before-false']` | killed_named |
| M5_control | 1 | `0e1bb2bbaa366c28…` | 1 | 20 | `['arm-pack-control-false']` | killed_named |

Survivor set: `[]`. Same failed lists as the constant family.

### r68 constant family — before-arm (blob `48ef4c68…`)

| mutant | site matches | mutant sha256 | rc | cases | failed | verdict |
|---|---|---|---|---|---|---|
| M1_identity | 1 | `85d34a25387a6763…` | 0 | 13 | `[]` | survived |
| M2_recovery | 1 | `8690ee2492826b07…` | 0 | 13 | `[]` | survived |
| M3_detected | 1 | `df1210c04621a3cf…` | 0 | 13 | `[]` | survived |
| M4_before | 1 | `b73c30f424e096c7…` | 0 | 13 | `[]` | survived |
| M5_control | 1 | `0c501fa8779360e8…` | 0 | 13 | `[]` | survived |

Survivor set: exactly `['M1_identity','M2_recovery','M3_detected','M4_before','M5_control']`.
M1's and M5's mutant bytes hash to the *same* files the round-68 wave scored (`85d34a25…`,
`0c501fa8…` in `.ufo/waves/round-68/w1/MutPacked/mutants.md`) — independent corroboration that the
before-arm is the same object (observation).

### r68 literal family

| mutant | site matches | mutant sha256 | rc | cases | failed | verdict |
|---|---|---|---|---|---|---|
| M1_identity | 1 | `6101c20f29a147d1…` | 0 | 13 | `[]` | survived |
| M2_recovery | 1 | `855dbb269442ab74…` | 0 | 13 | `[]` | survived |
| M3_detected | 1 | `23069d3d114817a9…` | 0 | 13 | `[]` | survived |
| M4_before | 1 | `541311a19ba7040d…` | 0 | 13 | `[]` | survived |
| M5_control | 1 | `0c501fa8779360e8…` | 0 | 13 | `[]` | survived |

Survivor set: the same five. M2/M4/M5 shas equal the round-68 wave's recorded mutant shas
(`855dbb26…`, `541311a1…`, `0c501fa8…`) → the battery's r68 patch text is byte-identical to the
round-68 wave's mutants (observation).

## 5. Cross-check against the frozen battery's receipt

Run for comparison only, at the freeze, into scratch:

```
python3 -I -B tools/round-69/mutation-check.py --root <lane> \
  --rev f15998102f1ce3569e61faa2ac6f286bc414538e \
  --tool tools/round-69/packed-elf.py --patch-set r69 --work <scratch> --json-out <scratch>
python3 -I -B tools/round-69/mutation-check.py --root <lane> \
  --rev d7d9a62cc70935304e600ed0dee864fc4f1751f7 \
  --tool tools/round-68/packed-elf.py --patch-set r68 --work <scratch> --json-out <scratch>
```

| field | battery r69 arm | ExecC1 derivation | same |
|---|---|---|---|
| `survivors` | `[]` | `[]` | yes |
| `killed` | five, each `failed` naming its declared case | five, same lists | yes |
| `killed_wrong_case` | `[]` | `[]` | yes |
| `pristine.cases` / `pristine.ok` | `20` / `true` | `20` / `true` | yes |
| `target_sha256` | `4ac0d83b…` | `4ac0d83b…` | yes |
| `ok` | `true` | — | — |

| field | battery r68 arm | ExecC1 derivation | base receipt `c1-at-base.json` |
|---|---|---|---|
| `survivors` | the five | the five | the five |
| `survivor_count` | 5 | 5 | 5 |
| `pristine.cases` / `pristine.ok` | `13` / `true` | `13` / `true` | `13` / `true` |
| `target_sha256` | `48ef4c68…` | `48ef4c68…` | `48ef4c68…` |
| per-mutant verdicts / `failed` | survived / `[]` ×5 | survived / `[]` ×5 | survived / `[]` ×5 |

**Mismatches with the battery's receipt: none on any field both sides report.** The base receipt
`c1-at-base.json` likewise matches. The battery's receipt is *corroborated*, not trusted.

## 6. Verdict on the frozen predicate sentence

The frozen sentence, clause by clause, at `f15998102f1ce3569e61faa2ac6f286bc414538e`:

1. "survivors []" — **holds** (both families; the battery agrees).
2. "all five mutants killed" — **holds** (rc 1, five mutants, both families).
3. "each kill's `failed` list naming its declared arm-false case" — **holds**; each list is exactly
   the one declared case (`arm-pack-{identity,recovery,detected,before,control}-false`).
4. "pristine.cases 20 with pristine.ok true" — **holds** (rc 0, `failed []`).
5. "the same battery against `tools/round-68/packed-elf.py` at the base revision … with patch set
   r68 reports exactly the five survivors … and pristine.cases 13" — **holds** (both families; the
   r68 blob is `48ef4c68…` at both the base and the freeze).

**Verdict: the R69-C1 predicate sentence holds at the freeze**, for both the constant-`True` mutants
(stronger than declared) and the battery's literal patch text. No clause is carried by an artefact of
my tooling: the patch sites each matched once, the pristine runs are green and deterministic, and a
crash (no JSON) is classified as unevaluable rather than a kill.

Caveat on clause wording, not on the result: the predicate says "run at the measured revision". Per
`claims.json` atom A9 the measured revision is the landing commit, which does not exist yet. The
derivation above is over committed bytes at the freeze; because the freeze blob, the worktree file
and `instrument_pins` all hash to `4ac0d83b…`, any landing commit that carries those bytes satisfies
the same sentence (inference, contingent on the landing not touching the four instruments — A1).

## 7. Observations beyond the predicate (report-only; never claim input)

Six extra mutants were run against the r69 blob to test whether the 20-case selftest has teeth beyond
the five declared sites, and one against r68 to prove a dead store. Full rows in
`receipts/r69-extra.json`, `receipts/r68-extra.json`.

| probe | patch | result |
|---|---|---|
| X1_ok_hardwired | `evaluate_carrier` tail `ok: all(arms.values())` → `ok: True` | **killed**, `failed` = all five `arm-pack-*-false` cases |
| X2_fold_all_matched | `matched = sum(1 for c in carriers if c["ok"])` → `matched = len(carriers)` | **killed**, `failed ['fold-not-met']` |
| X3_sections_zero | `section_count` body → `return 0` | **killed**, `failed ['sections-some']` |
| X4_refusal_dropped | `if model.get("address"):` → `if False and …` | **no payload**, `KeyError: 'refusal_ok'` at the `arm-pack-refusal` case → rc 1, classified unevaluable (a crash, not a named gate) |
| X5_arm_case_deleted | delete the `arm-pack-identity-false` `cases.append` | **killed**, `failed ['case-inventory']` → an omitted case is caught by the registry comparison |
| X6_control_unwired | `carrier_arms(…, control_ok)` → `carrier_arms(…, True)` | **killed**, `failed ['arm-pack-control-false']` → the seam plumbing is bound, not only the expression |
| X7_r68_dead_control_store | r68 `control_ok = ctrl_l["rc"] != 0 and ctrl_d["rc"] != 0` → `control_ok = True` | **survived** (rc 0, 13/13) → that local is a dead store; r68's live control expression is the inline `all(...)` inside the `fold()` call |

Consequences worth carrying (observation unless marked):

* The r69 selftest is bound to the whole `evaluate_carrier` seam and to its registry, not just to the
  five expressions. X1–X3, X5 and X6 all kill.
* X4 is the one weak shape: removing the refusal evaluation is caught only as a `KeyError` inside the
  case, so `failed` is unparsable and a battery would report `killed_wrong_case` — still non-zero, but
  an arm-false case that names its arm would be cleaner. Not reachable from the five declared sites.
* r68's `control_ok` local (line 277) is a dead store **by measurement**, which explains why the
  round-68 wave's M5 had to patch the `fold()` call rather than that line; patching the local alone
  changes nothing.
* The r69 patch set's M2/M4 mutants are *weaker* than the round-68 ones (drop one conjunct / drop the
  equality instead of a self-compare). The claim's prose ("the same five patches") is therefore true
  of the *sites*, not of the mutant text. Because the constant-`True` family also kills all five, the
  weaker literal mutants cannot be manufacturing the kills (observation + inference).
* `score()` feeds `evaluate_carrier` all 16 keys it reads (AST check; `unfed = []`), and `score()`
  calls `evaluate_carrier(model)` at line 427, so the seam the selftest binds is the seam production
  scores (observation). The selftest kill is therefore causally connected to the route, not to a
  parallel copy of the logic.

## 8. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r69/ExecC1 ; L=<lane>
git -C $L show f15998102f1ce3569e61faa2ac6f286bc414538e:tools/round-69/packed-elf.py > $S/bin/r69-packed-elf.py
git -C $L show d7d9a62cc70935304e600ed0dee864fc4f1751f7:tools/round-68/packed-elf.py > $S/bin/r68-packed-elf.py
python3 -I -B mutapply.py --blob $S/bin/r69-packed-elf.py --family constant --target r69 --outdir $S/mut --json-out $S/rec/r69-constant.json
python3 -I -B mutapply.py --blob $S/bin/r69-packed-elf.py --family literal  --target r69 --outdir $S/mut --json-out $S/rec/r69-literal.json
python3 -I -B mutapply.py --blob $S/bin/r68-packed-elf.py --family constant --target r68 --outdir $S/mut --json-out $S/rec/r68-constant.json
python3 -I -B mutapply.py --blob $S/bin/r68-packed-elf.py --family literal  --target r68 --outdir $S/mut --json-out $S/rec/r68-literal.json
python3 -I -B mutapply.py --blob $S/bin/r69-packed-elf.py --family extra    --target r69 --outdir $S/mut --json-out $S/rec/r69-extra.json
python3 -I -B mutapply.py --blob $S/bin/r68-packed-elf.py --family extra    --target r68 --outdir $S/mut --json-out $S/rec/r68-extra.json
```

## 9. Evidence in this directory

`mutapply.py` — the applier; `receipts/*.json` — every run above (six derivation receipts, two battery
cross-checks, two determinism pairs); `receipts/mutants-r69-constant/` and
`receipts/mutants-r68-constant/` — the ten constant-family mutants and the two pristine copies exactly
as scored; `receipts/MANIFEST.sha256` — sha256 of every file in `receipts/` plus this applier.

Scratch `/fast/scratch/hyaku/kaidoku-r69/ExecC1/` was created, used, and deleted before yield; the
receipts and mutants above were copied out first.
