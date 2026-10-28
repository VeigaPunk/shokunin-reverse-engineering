# R44C2Counter — P44-C2 calibration counter (round 44, wave 1, pre-freeze)

Seat `R44C2Counter` (executor). Lane `kaidoku-shokunin`, base `c29360e3ba5381a5ab69e372d0d9577970f85018`.

## What I built

| item | value |
|---|---|
| artifact | `.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py` (1719 lines) |
| sha256 | `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` |
| installed path (L1) | `tools/round-44/c2-counter.py` |
| rubric it reads | `tools/round-44/c2-rubric.json` (frozen at the freeze commit) |
| dev-arm fixtures | `…/artifacts/R44C2Counter/dev-rubric.json`, `dev-rubric-landing-bound.json`, `dev-rubric-landing-unbound.json` |
| receipts | `…/artifacts/R44C2Counter/receipts/*.json` (7) + 5 score JSONs beside them |

I did **not** write anything under `tools/round-44/` (the L1 installs the counter), did not
touch a lane tracked file, and did not run `tools/round-44/c1-run.sh` (the after-side C1
data procedure). Only my seat's artifact/report paths and my scratch under
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Counter/` were written.

```
python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> \
    --work <SCRATCH> --json-out <OUT> [--rubric <FILE>] [--export auto|full|<glob,glob>] [--seat <NAME>]
python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <BASE> --work <SCRATCH> \
    --json-out <OUT> --rubric <FILE> --pre-freeze          # base census (CTL-C2-0 gate)
python3 -I -B tools/round-44/c2-counter.py --selftest
python3 -I -B tools/round-44/c2-counter.py --schema          # the rubric contract, printed
```

## The rubric contract the counter implements

Top level (object): `predicate`, optional `freeze` (the rubric may name the commit it is
bound to; a mismatch is exit 2), `frozen_paths` (list of strings or of
`{"path": …, "expected_edit": {…}}`), `expected_edits` (map form), `frozen_dirs`
(directory pathspecs — every file under them that existed at FREEZE is frozen),
`export_paths` (globs), `entries` (list; also accepted: `checks`, `items`, `statements`).

Entry (object) — `check`, `command` and `asserted` are **required** (a missing `check` or
`command` is a malformed rubric → exit 2):

```json
{
  "id": "<stable id>",
  "check": "json | text | exit | <descriptive label>",
  "command": ["python3", "-I", "-B", "tools/round-44/c2-checks.py", "<kind>"],
  "asserted": <the expected observation>,
  "compare": "eq | set_eq | numeric_eq | subset | ge | le",
  "observed_key": "observed",
  "file": "SCORECARD.md",
  "files": ["corpus/knowledge"],
  "timeout": 600,
  "repair_command": ["python3", "-I", "-B", "…"],
  "expected_edit": {"append": ["<line>"], "append_text": "<bytes>",
                    "preserve": ["<sha256 of a cited line>"], "marker": "<text>"}
}
```

**Check-command contract.** The command runs with the exported tree of REV as its working
directory and prints the observation on stdout. `check: "json"` parses stdout as JSON and
reads `observed_key` (default `observed`, then `value`, `result`, `match`, `ok`); `check:
"text"` takes stdout verbatim; `check: "exit"` maps the exit status to a boolean; a
descriptive label behaves like `json` with a text fallback. A command that cannot start,
times out, or exits non-zero with empty stdout **cannot be evaluated** → the whole score is
exit 2, never a pass. The counter exports the tree into a scratch clone (`git clone --shared
--no-checkout` + `git archive`, read-only); the env carries `HYAKU_TREE`, `HYAKU_REPO`,
`HYAKU_ROOT`, `HYAKU_REV`, `HYAKU_FREEZE`, `HYAKU_RUBRIC`, `HYAKU_WORK`, `HYAKU_SEAT`, and
`{rev} {freeze} {root} {tree} {repo} {work} {rubric} {seat}` are substituted in argv.

## Predicate behaviour (P44-C2)

1. **Freeze integrity.** FREEZE must be an ancestor of REV. Every frozen path — the rubric
   file itself, the counter file, the rubric's `frozen_paths`, the `frozen_dirs` pathspecs,
   and `SCORECARD.md`/`SHONEN.md`/`corpus/README.md`/`SKILL.md` (the R44-C2 frozen surface
   the claim names) — is walked in `FREEZE..REV` with merge diffs
   (`--diff-merges=first-parent`), a name-only union walk as a cross-check, and per-path
   status (`M/D/R/T/U` are changes; `A` is a change whenever the path existed at FREEZE).
   A frozen path whose blob differs from FREEZE, or that was touched and restored, is
   `frozen_path_changed` → **exit 2**, never a pass. `corpus/SOURCES.md` is deliberately not
   frozen: C1 appends its S138/S139 rows there and the claim pins no SOURCES row count.
2. **Repairs.** A repair is admissible only when the rubric binds it: the blob at REV must
   be the blob at FREEZE **plus** the bound block — byte-for-byte (`append_text`), or
   line-identity over the appended lines (`append`, blank separator lines ignored), plus
   cited-line digests that must still occur (`preserve`) and/or a marker line. The freeze
   blob must be a prefix of the REV blob, so nothing may be edited in place and nothing may
   be deleted. A suffix-containment check is **not** used: an in-place fabrication inside the
   frozen file is rejected (measured, see receipts).
3. **Evaluation.** Each entry's check argv runs in the scratch export of REV; the
   observation is compared with the asserted value under the entry's `compare` mode.
4. **A note is never evidence.** When a check fails, an appended correction note does **not**
   repair the entry. The entry may declare `repair_command`: a second argv that re-derives
   the value from REV state; only when that re-derived value equals the asserted value is
   the entry repaired (`repaired_by_rederived_value`). Without it, the note leaves the entry
   a mismatch.
5. **Exit codes.** `0` iff `mismatches == 0`, no entry is unevaluable and at least one entry
   was evaluated (`entries_evaluated > 0`); `1` on a mismatch; `2` for a malformed rubric, an
   absent frozen file, a frozen path that changed, an empty rubric, a check that cannot run,
   or a freeze that is not an ancestor. **Exit 2 means could-not-evaluate, never "not a
   pass"; it never counts toward the target.** The receipt always carries `mismatches`,
   `mismatches_count`, `entries_evaluated`, `unevaluable`, `frozen_path_changed`,
   `pre_freeze`, `claim_score`, `counter_sha256` and `counter_sha256_at_freeze`.
6. **`--pre-freeze`** runs the base census (CTL-C2-0's honest-stop gate): the freeze walk
   is reported but not enforced, because at the base the freeze is not yet an ancestor of
   REV. The receipt carries `pre_freeze: true` and `claim_score: false`, so a census can
   never be mistaken for a claim score.

## Evidence (receipts: seat, command, exit code, stdout sha256, wall time)

| receipt | exit | stdout sha256 | wall s | what it shows |
|---|---|---|---|---|
| `receipts/selftest.json` | 0 | `a5e942a1efa3172ba522a2174c68f62f80b01c009f9495027d4bbfde7558fbc3` | 1.34 | the 24-arm self-test matrix is green |
| `receipts/dev-arm-lane.json` | 1 | `baf3d281d9bebf912a054d58cec617256b3fd27ee118a00b443d11b54be99de1` | 0.81 | the counter runs on the real lane at the base and reports mismatches |
| `receipts/pre-freeze-census.json` | 1 | `45dfefc52da4e53e089f6383eb94a52e7344a467f8b04c51af76f2deb8dcf058` | 0.75 | the base census runs pre-freeze and reports `entries_evaluated` + `mismatches` |
| `receipts/no-rubric-at-base.json` | 2 | `003bd8577716559be8d91fbb097063f70fb4ba05ed7c430e58ac59ce3372c5b3` | 0.06 | no frozen rubric at FREEZE → `rubric_absent_at_freeze`, exit 2 (never a pass) |
| `receipts/landing-bound.json` | 0 | `febea36aac95c7a50e566c828fc3052ca09a01134df876f91c76f128c5f084e2` | 0.65 | a bound appended repair to `SCORECARD.md` is admissible |
| `receipts/landing-unbound.json` | 2 | `843e2ef4e2256b0350e818b57cdcef34e34c874926690818d92fd922050e82ce` | 0.09 | the same append **without** a bound `expected_edit` → `frozen_path_changed` |
| `receipts/in-place-fabrication.json` | 2 | `56abc64d05bee901ea297cfbaae4efa4d2be9c380eaba0c8e515f3b74782e245` | 0.09 | an in-place fabrication ("R43-C2 met" rewritten into the frozen blob) is rejected |
| `receipts/real-rubric-census.json` | 1 | `1f323cb871edc253b0239efefbce76cfee2d6fd8906cec619d6738f6c95dacc9` | 7.02 | **interop**: the rubric author's frozen rubric (80 entries, sha256 `89dad28b…`) over my counter — 80 evaluated, 3 mismatches, 0 unevaluable, `frozen_path_changed []` (the same three ids they measured) |
| `receipts/landed-claim-freeze.json` | 1 | `ecdaf58ea76544c050b669f9e93ae51943cd37a7945419984dec7aff46d60c55` | 6.81 | **claim mode at the freeze** (counter + rubric committed in the freeze commit): exit 1, 80 evaluated, the 3 stale `## Owned axes` observables, `claim_gate.usable_as_claim_score` **false** — the do-nothing control is red |
| `receipts/landed-claim-repaired.json` | 0 | `c48c1190e641bc13b29aabbf890d34e5b50eecd529cbfc59e8b3e4cab256b506` | 6.75 | **the landing**: the rubric's bound `SCORECARD.md` correction block appended **and** a C1-style coverage-map row inserted into `corpus/README.md` → exit 0, 80 evaluated, 0 mismatches, `frozen_path_changed []`, `claim_gate.usable_as_claim_score` **true** — no ordering dependence on C1 |
| `receipts/shipped-rubric-freeze.json` | 1 | `feedd66772fea1fdd2439ace491b77acbc2d5d4cd3b512f2f4dc6a34528d2e01` | 6.52 | **the SHIPPED rubric** (sha256 `a6ae1c1b…`): claim mode at the freeze, counter + rubric committed in the freeze commit → exit 1, 80 evaluated, the 3 stale `## Owned axes` observables, `claim_gate.usable_as_claim_score` **false** |
| `receipts/shipped-rubric-repaired.json` | 0 | `9f7a292024982eacd6e63e245843444a3e1928177e4d500fe84b5b30eef00535` | 6.62 | the SHIPPED rubric after the bound `SCORECARD.md` block + a C1-style README map row → exit 0, 80 evaluated, 0 mismatches, `frozen_path_changed []`, gate **true** |
| `receipts/shipped-rubric-census.json` | 1 | `1f323cb871edc253b0239efefbce76cfee2d6fd8906cec619d6738f6c95dacc9` | 6.82 | base census with the SHIPPED rubric → exit 1, 80 evaluated, the same three mismatch ids, 0 unevaluable |

## Self-test matrix (`--selftest`, all green)

| arm | expected | got |
|---|---|---|
| clean rubric at the base | 0 | 0 |
| seeded mismatch on the reality side | 1 | 1 |
| seeded mismatch on the claim side | 1 | 1 |
| rubric entry with no command | 2 | 2 |
| the committed rubric edited after the freeze | 2 | 2 |
| appended repair bound by `expected_edit` | 0 | 0 |
| the same append without a bound `expected_edit` | 2 | 2 |
| a note alone never repairs | 1 | 1 |
| a note plus an independent re-derivation | 0 | 0 |
| empty rubric (`entries_evaluated == 0`) | 2 | 2 |
| a file changed under a frozen directory pathspec | 2 | 2 |
| a file **added** under a frozen directory pathspec | 2 | 2 |
| a weak `expected_edit` (marker only) | 2 | 2 |
| a self-referential check (it reads the rubric) | 2 | 2 |
| pre-freeze census at the base | 1 (mismatch reported) | 1 |
| pre-freeze census of a rubric that declares the freeze | 1 (census runs) | 1 |
| a C1-style mid-table row insertion bound by an `insert` clause | 0 | 0 |
| the same row insertion without a bound insert clause | 2 | 2 |
| uppercase placeholders (`{REV}`) resolve | 0 | 0 |
| a script pin that does not match the blob | 2 | 2 |
| an inline payload pinned by digest (correct) | 0 | 0 |
| an inline payload with a wrong digest pin | 2 | 2 |
| a clean claim run — the claim gate is usable | 0 | 0 (gate usable) |
| a claim run with a mismatch — the gate is NOT usable | 1 | 1 (gate not usable) |

## Lane dev-arm findings (probe grade — the frozen rubric is another seat's job)

The dev rubric I used to exercise the counter on the real lane at the base
(`dev-rubric.json`, four checks over `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`) is
**not** the frozen rubric and its checks are crude. It reports 2 of 4 mismatches:

* `dev-scorecard-map-count` — `SCORECARD.md`'s coverage headline claims **133** knowledge
  files mapped; `corpus/knowledge/*.md` holds **137** at the base. A real candidate for the
  frozen rubric (category b), and a candidate C2 repair.
* `dev-readme-map-coverage` — my probe's regex also matches lesson/evidence stems quoted in
  `corpus/README.md` (`2026-10-13-round-1`, …), so its "dangling" list is a **probe
  artefact**, not necessarily a lane defect. The rubric author must scope the stem pattern.
* `dev-shonen-path-line` — all 8 `path:line` assertions in `SHONEN.md` resolve at the base
  (match).
* `dev-scorecard-evidence-pointer` — all 36 `corpus/knowledge/…` pointers in `SCORECARD.md`
  resolve (match).

**The honest-stop gate is not yet run**: this is a four-check dev probe, not the enumerated
frozen rubric, so it cannot decide whether R44-C2 stops (zero mismatches at base). The
census mechanism that would decide it is in place and measured (`--pre-freeze`).

## Sentinel blockers addressed (`R44C2Sentinel`, wave-1 review, two rounds)

1. *"A note must never be evidence."* The `supersession` escape hatch is **removed** from the
   counter. A failed check is repaired only by an independent re-derivation
   (`repair_command`), never by the presence of a note. Measured: `note_alone_does_not_repair`
   → 1, `note_with_rederived_value` → 0.
2. *"`expected edit bytes` cannot exist pre-freeze; a suffix-containment check accepts an
   in-place fabrication."* The binding is containment-free: the REV blob must be the FREEZE
   blob **plus** the bound block (`append_text` byte-for-byte; `append` line identity;
   `preserve` cited-line digests), and the freeze blob must be a prefix (nothing edited in
   place, nothing deleted). Measured on the real `SCORECARD.md` blob: an in-place
   "R43-C2 met" fabrication → exit 2 `bound_edit_violation`. `tools/round-44` is also
   freezable as a directory pathspec (`frozen_dirs`), and the counter ships with
   `tools/round-44/c2-counter.py` and `tools/round-44/c2-rubric.json` in its frozen set.
3. *"The counting command has no pre-freeze mode."* `--pre-freeze` added: the base census
   runs (freeze walk reported, not enforced), and the receipt carries `pre_freeze`,
   `claim_score: false`, `entries_evaluated` and `mismatches` — so CTL-C2-0's honest-stop
   gate can actually run instead of dying on `freeze_not_ancestor`.
4. *"Exit 2 must never be reachable as 'not a pass'; an empty rubric must be exit 2."*
   `entries_evaluated == 0` → exit 2 (`no_evaluable_entries`); every other exit-2 reason is
   a genuine could-not-evaluate (malformed rubric, absent frozen file, frozen path changed,
   check that cannot run). Exit 1 is reserved for a measured mismatch.

The Sentinel's second pass found four residual holes; all are closed and covered by new
self-test arms:

5. *A file **added** under a frozen directory pathspec was only noted.* An addition under a
   frozen pathspec is now a change (`frozen_path_changed`), because the claim freezes
   `tools/round-44/*`. The same rule applies to the rubric and the counter themselves: a
   post-freeze addition of `tools/round-44/c2-rubric.json` or `tools/round-44/c2-counter.py`
   is `added_after_freeze` → exit 2. (Arms `frozen_dir_added`.)
6. *`expected_edit` with only a `marker`, or an empty `append`, admitted arbitrary appended
   content.* A binding must now carry `append_text` (byte-for-byte) or a non-empty `append`
   (line identity); `marker` and `preserve` are additional only. A rubric with a
   contentless binding is **malformed** → exit 2 at freeze time, not a silent hole. (Arm
   `weak_expected_edit`.)
7. *`--pre-freeze` refused a rubric that declares the canonical freeze.* The declared
   freeze is now **recorded** (`declared_freeze`) and not enforced in the census, so
   CTL-C2-0 can score the frozen rubric at the base. (Arm
   `pre_freeze_with_declared_freeze`.)
8. *`--rubric` still yielded `claim_score: true`.* A claim score now requires
   `rubric_source == 'freeze'`; every `--rubric` run is a census/dev arm and reports
   `claim_score: false`.

The Sentinel's third pass left three items open that it classified as **rubric-level**
(O1 pin binding, O2 asserted provenance + self-referential check, O3 frozen check scripts).
Two of them have counter-side support, added here so the rubric cannot fake them:

9. *Self-referential checks (O2).* A check whose argv mentions the rubric itself
   (`c2-rubric.json`, the rubric path, or the `{rubric}` placeholder) reads the asserted
   value it is supposed to verify: its observation is circular, so the counter **refuses**
   the entry — `unevaluable: self_referential_check` → exit 2, never a pass. (Arm
   `self_referential_check`.)
10. *Frozen check scripts (O3) and the claim gate.* Every entry now records
    `check_scripts`: the repo paths its command names, each with `scope` (frozen /
    unfrozen) and its sha256 at FREEZE and at REV, so a cited receipt shows which script
    produced the observation and whether that script moved. The summary carries an
    explicit `claim_gate`: `usable_as_claim_score` is true only when `claim_score` is true,
    `rubric_source == 'freeze'` **and** `counter_sha256_at_freeze` and
    `rubric_sha256_at_freeze` are non-null. A dev or census run may exit 0 with
    `met_target: true` while `claim_gate.usable_as_claim_score` is false — the claim gate,
    not `met_target`, decides what may be cited.

O1 (pin binding: the asserted values' provenance pins) remains a rubric-authoring duty —
the counter records the rubric's declared freeze and the digests, but it cannot invent the
pins.

## Round-44 integration fixes (L1 + rubric-author requests, measured)

* **Placeholders are case-insensitive now.** `{rev}`/`{REV}`, `{freeze}`/`{FREEZE}`,
  `{repo}`/`{REPO}` … all resolve (the rubric author's commands end with
  `["{rev}","{freeze}","{repo}"]` in upper case; before this fix every git read in their
  checks failed). Inline payloads are never mangled: only the known names are substituted.
* **`corpus/README.md` is no longer auto-frozen.** C1 inserts a coverage-map row into it
  after the freeze; with README in the frozen set every C2 score was exit 2 (measured:
  `c1-readme-insertion` → exit 2). The default frozen set is now `SCORECARD.md`,
  `SHONEN.md`, `SKILL.md`; a rubric that really pins README must declare it in
  `frozen_paths` — and then it must also bind the insertion, which is now possible:
  `expected_edit.insert` = `{"after": "<exact anchor line>"}` or
  `{"after_sha256": "<digest of the anchor line>"}` plus `{"lines": [...]}`; the REV blob
  must be the FREEZE blob with exactly those lines spliced in after the unique anchor —
  every original line preserved in order, byte for byte. Measured: `bound_row_insertion`
  → 0, `unbound_row_insertion` → 2. With the README row dropped from the rubric's
  `frozen_paths`, the C1 insertion is invisible to C2 (exit 0, measured).
* **Script pinning / fitness gate (counter-side, opt-in).** A rubric entry may declare
  `"script": {"path": "tools/round-44/checks/x.py", "sha256": "<digest>"}`; the counter
  then verifies the blob at REV equals the pin and that the command actually invokes that
  script (`script_pin_mismatch` / `script_absent_at_rev` / `script_not_invoked` →
  could-not-evaluate, exit 2). A rubric may also declare
  `"allowed_script_dirs": ["tools/round-44/checks"]` (any `.py`/`.sh` the command runs from
  outside those dirs → `script_not_allowlisted`) and `"require_declared_script": true`
  (an inline `-c` payload with no declared script → `undeclared_inline_script`). Without
  those declarations the current 80-inline-command rubric keeps working — pinning is
  opt-in, so the L1 can narrow the rubric to concrete frozen check scripts without
  breaking the enumeration.
* **Inline payloads are visible.** Every entry's receipt carries `argv_digests` (the
  sha256 and length of every argv element) and `inline_payload`, so a `-c` script is
  visible in the receipt instead of being invisible to `check_scripts`. `reads_subject`
  and the subject's sha256 at FREEZE and at REV are recorded too, so a reviewer can see
  when a check reads the very file it is judging.
* **`claim_gate` is in the receipt.** The json-out file now carries `claim_gate`
  (`claim_score`, `rubric_source`, `counter_sha256_at_freeze`,
  `rubric_sha256_at_freeze`, `usable_as_claim_score`) as well as on stdout.

### Interop with the rubric author's frozen rubric (measured)

Their **shipped** rubric (80 entries, sha256 `a6ae1c1b633083992bbce4144b2976a4def8002270998ce4c97ef544d3032060`)
scored with this counter (receipts `shipped-rubric-*.json`):

| run | result |
|---|---|
| base census (`--rev <BASE> --pre-freeze`) | exit 1, entries_evaluated 80, mismatches 3 (`C2-a1-owned-coverage-count`, `C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range`), unevaluable 0, `frozen_path_changed []` — identical to their own measurement |
| claim mode, counter + rubric committed in the freeze commit | exit 1, `claim_score: true`, `claim_gate.usable_as_claim_score: true`, `counter_sha256_at_freeze` and `rubric_sha256_at_freeze` non-null — the do-nothing control is red, as CTL-C2-0 requires |
| with the rubric's bound correction block appended to `SCORECARD.md` | exit 0, mismatches 0, `met_target: true`, freeze note `bound_edit_applied` |
| a C1-style README row inserted after the freeze | exit 0, 80 evaluated, 0 mismatches — the shipped rubric no longer freezes README and the counter no longer adds it by default |

(The earlier rubric revision, sha256 `048e9df6…`, still listed `corpus/README.md` in
`frozen_paths`: the same insertion then scored exit 2 `frozen_path_changed
['corpus/README.md']`, and exit 0 once README was dropped from the rubric's
`frozen_paths` — that is the measurement that motivated the default change.)

## Claim-gate fixes (Sentinel round 4) and the inline-payload pin

* **R7 — the gate was true on a failing run.** `usable_as_claim_score` is now a
  conjunction over the whole measurement: `claim_score` AND `rubric_source == 'freeze'` AND
  non-null `counter_sha256_at_freeze` AND non-null `rubric_sha256_at_freeze` AND
  `exit_code == 0` AND `met_target` AND no `frozen_path_changed` AND no unevaluable entry.
  The gate also reports `exit_code`, `met_target`, `mismatches_count`,
  `entries_evaluated`, `unevaluable_count` and `frozen_path_changed`, so a reviewer does
  not have to recompute it. Measured on the landed rubric: the do-nothing claim run at the
  freeze (exit 1) reports `usable_as_claim_score: false`; the repaired run (exit 0) reports
  `true`.
* **R8 — the gate was incomplete on early returns.** Every return path (freeze not an
  ancestor, rubric changed, frozen path changed, and the normal path) now goes through one
  `finalize()` that completes the gate, `met_target`, the counts and the exit code, so an
  early-return receipt carries the same fields as a complete one.
* **Inline payloads can now be pinned.** A rubric entry may declare
  `"check_script_sha256": "<digest>"` — the sha256 of the inline script text (the argv
  element after `-c`); the counter hashes that element and refuses the entry on a mismatch
  (`script_pin_mismatch`) or when there is no inline payload to hash
  (`script_pin_unresolved`). The rubric author's 80 entries already carry that field, so
  the fitness gate is enforceable over inline scripts without moving them to disk; the
  file-script pin (`script.path` + `script.sha256`) remains for scripts that do live in
  `tools/round-44/checks/`.

## Finding on the shipped rubric: one entry's statement is vacuously true

The rubric's own fitness gate reported 79/80 entries witnessed failing on their own
statement, with `C2-c16-cap-pointer` the exception. I measured that exception with this
counter (rev = freeze = the mutated commit, so no freeze-range drift):

* **The entry can fail.** Injecting one unresolvable lane-repo pointer into the row it
  inspects (base `SCORECARD.md` line 2385, the `## Round 17 …` row keyed
  `retained REA Ghidra-session log capture`) makes it report
  `UNSUPPORTED:unresolved:corpus/knowledge/does-not-exist-2099.md` and appear in the
  counter's mismatches — receipt `receipts/fitness-probe-c16.json` (exit 1, stdout sha256
  `9b551058454e6055f91720e6ce1f7066050e254142666ea9b39444c1def3ca24`, 8.94s; mismatches =
  the three target ids + `C2-c16-cap-pointer`). So the entry is fitness-proven.
* **But its statement is vacuously true as shipped.** That row's backticked tokens
  (`analyze`, `ghidra.log`, `script.log`, the command with a space, the `*` glob, and the
  bare `receipt-validate.py` / `verification.json` names) all fail the entry's own pointer
  filters, so the entry examines an **empty** pointer set and reports `resolved` whatever
  the repo state is. The rubric author's witness missed it because it mutated the pointer
  in the *other* row carrying the same key (line 626) — replayed, that mutation flips
  `C2-c08-cap-pointer` and leaves `C2-c16-cap-pointer` at `resolved`.

The entry sits in the rubric's excluded-census-candidate scope, so the claim score does not
depend on it; but a frozen rubric that carries a vacuously-true entry is itself a
calibration defect on the surface C2 measures. The fix is rubric-side (widen the pointer
filter to the row's real evidence pointers, or restate the entry's note to say what it
actually checks) and was sent to the rubric author. This counter does not author rubric
statements.

## Limits and risks (honest)

* The rubric's **enumeration** is another seat's (`R44C2Rubric`); this counter only
  re-derives what the rubric names. A check outside the frozen set is not counter ground.
* **Export coverage.** `auto` exports the rubric-named paths, the path-like literals inside
  the check commands, the rubric's `export_paths` globs and the C2 default surface
  (`SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `SKILL.md`, `LOG.md`, `corpus/README.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/*`, `corpus/lessons/*`, `corpus/evidence/*.json`).
  A check that discovers paths at runtime and reads something outside that set sees a
  missing file → the check fails → exit 2 (honest, never a false pass). `--export full`
  exports the whole tree (34 183 files, ~511 MB) when needed.
* A check that crashes is *not* a mismatch: non-zero exit with empty stdout is
  could-not-evaluate → exit 2. A crashing check must be fixed, not counted as a defect.
* `expected_edit` binds the *repair*, not the *result*: the L1 must write the rubric's
  bound append lines before the freeze, or the landing will be inadmissible (exit 2). The
  bound lines are the appended block's non-blank lines, in order.
* `frozen_dirs: ["tools/round-44"]` couples the two claims: if C1's landing adds any
  file under `tools/round-44/` after the freeze, C2's score is exit 2
  (`added_under_frozen_dir`). The Separability section of the claim file must state that
  dependency, and every round-44 tool (both counters, `carriers.json`, `c1-run.sh`, the
  rubric, any check script the rubric names) has to land in the freeze commit.
* The rubric has since dropped `corpus/README.md` from `frozen_paths` (sha256 `89dad28b…`),
  and the landing run above measures the result end to end: a C1-style coverage-map row
  inserted into `corpus/README.md` after the freeze, together with the bound `SCORECARD.md`
  correction, scores exit 0 with 0 mismatches and `frozen_path_changed []`.
* If the L1 installs `tools/round-44/c2-counter.py` or `tools/round-44/c2-rubric.json`
  **after** the freeze commit, the score is exit 2 `added_after_freeze` (a post-freeze
  addition of a frozen path), and `frozen_dirs: ["tools/round-44"]` extends that to any
  file added under the directory. Both files must land **in** the freeze commit.
* The counter reads committed bytes only: it cannot verify that a repaired *statement* is
  true, only that the check re-derives it. Every rubric check must re-derive the value
  independently (recount, re-resolve), never re-read the number it is checking. The
  measured `C2-c16-cap-pointer` case shows the limit: the counter can show that an entry
  FAILS, it cannot show that an entry is MEANINGFUL.
* A bound `expected_edit.append` must enumerate **every** non-blank line the landing
  appends, in order. A landing section appended to `SCORECARD.md` next to the rubric's
  correction block therefore needs the bound list extended (rubric-side, no counter
  change) or must land elsewhere; the counter does not loosen the binding on request.
* `python3` here is 3.14 on this host; the counter uses only the standard library and runs
  under `-I -B`.

## For the L1

> **Installed.** At the L1's direction this seat copied the artifact to
> `tools/round-44/c2-counter.py` (mode 755, sha256
> `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277`, 1719 lines,
> byte-identical to this artifact); nothing was committed. The installed
> `tools/round-44/c2-rubric.json` is the rubric author's current file
> (`e8cc0ded…`); the interop receipts below were measured against its predecessor
> (`a6ae1c1b…`) and are not re-measured here by the L1's instruction.
>
> **Install the current on-disk artifact, not the wave-1 snapshot.** An earlier version of
> the counter was picked up by commit `9a8de923` ("round-44 wave-1 receipts … seat outputs
> so far"); the file changed after that (the Sentinel's eight contract fixes). The version to
> install is the working-tree one, sha256
> `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277`, 1719 lines. Verify
> the digest before freezing.
>
> The counter and the rubric must land **in the freeze commit**: a post-freeze addition of
> `tools/round-44/c2-counter.py` or `tools/round-44/c2-rubric.json` is now
> `added_after_freeze` → exit 2, and `frozen_dirs: ["tools/round-44"]` makes any file added
> under that directory after the freeze a `frozen_path_changed` too.

1. Install `…/artifacts/R44C2Counter/c2-counter.py` → `tools/round-44/c2-counter.py` **in the
   freeze commit** (so the counter and the rubric are frozen).
2. Freeze the rubric at `tools/round-44/c2-rubric.json`; the rubric must declare
   `frozen_paths` (SCORECARD.md, SHONEN.md, corpus/README.md, and every file it repairs),
   `frozen_dirs: ["tools/round-44"]`, and an `expected_edit` for every file the landing
   appends to.
3. Run the base census before the freeze: `--pre-freeze --rev <BASE> --rubric <rubric>`.
   **If it reports `mismatches == 0`, R44-C2 stops (honest stop)** — report that instead of
   loosening the rubric.
4. After the freeze and the landing, the claim score is
   `--rev <REV> --freeze <FREEZE>`; exit 0 requires `mismatches == 0`,
   `entries_evaluated > 0` and `frozen_path_changed []`.
