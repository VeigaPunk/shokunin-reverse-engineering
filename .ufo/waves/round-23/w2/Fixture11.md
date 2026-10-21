# Fixture11: R23 `wrong_operation` control, source review

Scope: candidate 2838351450ff1ee4baa620c962a1153450d53311 (baseline aa1450b82f9ede35aada63efe8a34e01c6e02f72).
Case: `wrong_operation` in `frozen/expected-v2.json`, the `frozen/fixture.json` template, and the `wrong_operation` branch of `tools/counter-fixtures.py`.
Method: source review only. Candidate bytes were read with `git show <candidate>:PATH` into the ignored seat runtime. No suite, selftest, counter, fixture, or producer run was executed. Nothing was installed.

## Verdict

- **Expected triple `exit 1 / count 1 / c1_incomplete` is correct** for the candidate counter. No wrong expectation found (F2).
- **The case distinguishes the stated fault at candidate source.** The fault is an envelope whose `data.operation` names another verb's operation while it is cited under `inspect-signal-decoders`. The candidate binder rejects it (traced from source, F2), so the count stays at the baseline 1. A counter that accepted it would count 2 and fail this case.
- **Weak mutation (F1, Low).** The chosen operation `identify_flutter_build` belongs to the verb already held at baseline. This case therefore cannot detect operation-keyed crediting or partial-match operation tolerance. Recommended value: `inspect_dart_aot`. Changing it re-pins the frozen chain, so it needs a new candidate, not an in-place edit.

## Findings

### F1 [Low, weak mutation; no candidate counter defect observed]

- Mutation: `tools/counter-fixtures.py:56-57`, `elif name == 'wrong_operation': envelope['data']['operation'] = 'identify_flutter_build'`. Applied to the default member `inspect-signal-decoders` (`counter-fixtures.py:38`). Candidate blob sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`. Observed.
- The baseline held set is exactly `identify-flutter-build`. Hard guard: `tools/count-c1.py:82`. `claims.json` `before: 1`. Observed.
- Dedupe is per verb, not per operation: `count-c1.py:92-93` (`targets` keyed by verb), `:119-127` (`exercised`/`held` per verb). Observed.
- Consequence [inferred]: any operation-keyed crediting path (verb inferred from `data.operation`) would map `identify_flutter_build` to identify. Identify is already held, so count stays 1 and the mutant passes unnoticed.
- Consequence [inferred]: a partial-match check (for example, comparing the first `_` token) rejects identify against inspect. Again the mutant passes.
- Sibling `wrong_command` (`counter-fixtures.py:54-55`) keeps an inspect operation under an identify command. An operation-keyed crediting path would count it (count 2 against expected 1) [inferred]. So the suite still catches operation-keyed crediting, but only through `wrong_command`. Partial-match tolerance has no sibling control.
- Proposed mutant `inspect_dart_aot`. Why it is better:
  - It is a T1 verb not held at baseline (baseline is identify only, per `count-c1.py:82`).
  - It shares the leading token `inspect` with the cited verb, so partial-match tolerance is caught.
  - Its real producer string is already in candidate evidence: `.ufo/waves/round-23/evidence/c1/connect-dart-symbols/inspect-dart-aot-saber-1330203.envelope.json`, `"operation":"inspect_dart_aot"`. Observed.
  - Under the candidate binder it is still rejected (exact equality, see F2), so `expected-v2.json:58-62` stays unchanged [inferred].
- Repair cascade (observed). `expected-v2.json` pins `counter-fixtures.py` (line 4). `count-c1.py:25` pins `expected-v2.json` (`SELFTEST_MANIFEST_SHA256 = 458b30d5…`). Changing `counter-fixtures.py:57` therefore requires re-pinning both, which is a new candidate.

### F2 [None: expectation verified along the candidate path; trace inferred from source, not executed]

Trace of the `wrong_operation` member through the candidate counter:

1. `counter-fixtures.py:37` deep-copies `documents` per case. Only `data.operation` is altered (`:56-57`). `evidence_id` is unchanged (`:64`).
2. The synthetic knowledge entry cites `inspect-signal-decoders <ev_5555…> .ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json` (`:70`).
3. `count-c1.py:120` only attempts verbs whose command pattern appears in the entry, so only `inspect-signal-decoders` is tried.
4. `count-c1.py:42-56` (`bind_new`) finds no `ok`/refusal markers, then calls `r22.bind_cli`.
5. The legacy round-22 counter (sha256 `c925918f…`, equal to `LEGACY_SHA256` at `count-c1.py:23`) runs `bind_cli`. Line 82 only checks that `operation` is present. Line 96 delegates to `r21.bind`.
6. Round-21 `verb-coverage.py` (sha256 `615369…`, pinned by the legacy file's `HELPER_SHA256`) runs `bind`:
   - Line 85: `operation = verb.replace('-','_')`, which is `inspect_signal_decoders`.
   - Line 88: record operation `identify_flutter_build` does not match, so the record is skipped.
   - Line 96: `evidence_unbound`, code 1.
   `bind_new` returns 1, and `count-c1.py:123` (`== 0`) does not append the member.
7. `held` = {identify, from the historical measure}. Result: count 1, exit 1 (`count-c1.py:166`), `c1_incomplete` (`:129`).

Positive-preservation: `positive` (`expected-v2.json:8-12`, count 2) uses the same template with no mutation. Its only difference from `wrong_operation` is `data.operation`. Line 88 matches for positive (code 0), so it is counted. The pair therefore isolates operation equality, and the expected triple is consistent with that. Observed expectations; traced behavior [inferred].

Independence of the oracle, observed:
- Operation strings in `fixture.json` match real producer envelopes at the candidate commit. `fixture.json:11` (`identify_flutter_build`) matches `connect-dart-symbols/identify-flutter-build-saber-1330203.envelope.json`. `fixture.json:63` (`inspect_signal_decoders`) matches `uart-help.envelope.json` and `inventory.envelope.json`. The latter two also carry `meta.command: inspect-signal-decoders`, which matches the fixture template at `fixture.json:59`.
- `expected-v2.json` is a literal JSON file. No candidate writer was found: `gen-wave1.py` and `gen-wave2.py` write only seat specs, and `verify.py` only hashes it (its pins list, `verify.py:108`). `count-c1.py` `selftest` only reads and pins it, and `counter-fixtures.py` never references it. This is absence of a writer, not proof of hand authorship.
- The baseline value 1 is pinned by `claims.json` `before: 1` and the `count-c1.py:82` guard, not by the new decision logic.

### F3 [Info: recorded result applies to candidate inputs, but was not re-observed]

- `.ufo/waves/round-23/verify/initial/selftest.json` is absent at `6615aea` and present at the candidate. Its recorded `source_rev` is `6615aea`. Recorded: 21/21 passed, `wrong_operation` observed `{exit 1, count 1, c1_incomplete}`, `passed: true`.
- The inputs that row exercised are byte-identical at `6615aea` and at the candidate: `expected-v2.json` (`458b30d5…`), `fixture.json` (`a1f5aff8…`), `counter-fixtures.py` (`f2990b35…`), and `count-c1.py` (`f4b8d16a…`). Observed by `git show | sha256sum` at both commits.
- So the recorded row applies to the candidate's inputs, but I did not re-observe it. Unrun is not passed.

### F4 [Info, adjacent to the item, not a defect of `wrong_operation`]

- No case pins the absent-`data.operation` path. `r22 bind_cli` line 82 returns 2 for it. `count-c1.py:123` (`== 0`) then treats that member as not counted, and the top-level exit stays 1, not 2 [inferred].
- Member-level code 2 therefore collapses into "not counted". No case distinguishes it from code 1 (refusal or unbound). Only top-level exceptions produce exit 2.

### F5 [Info: v1 carry-over]

- `wrong_operation` is unchanged from v1. `expected-v1.json` has the same `{exit 1, count 1, c1_incomplete}`, and `counter-fixtures-v1.py:56-57` has the same branch. A per-case comparison found 8 differing cases between v1 and v2 (`old_source`, `sibling_refusal`, `meta_array`, `inherited_lost`, `catalog_changed`, `historical_root_injection`, `meta_false`, `absolute_citation`). `wrong_operation` is not among them.

## Checks not run

- Not run (per assignment): the suite, `--selftest`, `count-c1.py`, `counter-fixtures.py`, `verify.py`, and any fixture or clone. The `wrong_operation` pass is therefore recorded (F3), not observed by me.
- Commands used were read-only: `git show`, `git cat-file -t`, `git diff --name-only` between the two commits, `sha256sum`, and stdlib JSON parsing of recorded artifacts.
- Writes: only the seat runtime copies and this report. No peer report, tracked file, or repository state was touched.

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture11.md`: this report. Its hash is given in the hand-off message, since embedding it would change it.
- Ignored seat runtime `.ufo/waves/round-23/runtime/Fixture11/` (candidate bytes via `git show`, not tracked):
  - `cand-counter-fixtures.py` `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`
  - `cand-expected-v2.json` `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`
  - `cand-fixture.json` `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`
  - `legacy-r22-count-c1.py` `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`
  - `legacy-r21-verb-coverage.py` `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`
  - `legacy-r20-verb-coverage.py` `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`
  - `count-c1.py` `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`
  - `gen-wave1.py` `bb5f975f77d9ef9effe3255dc53b62529945729cf4ab5f6f74527d5a50f9bfe2`
  - `gen-wave2.py` `da2962bc77d964c09a9ac3ff06c8ea760d4001164974e48135c3b6404d5d009a`
  - `verify.py` `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a`
  - `make-uart.py` `8720ee4e5afdfd66630fe4f357aec1a574b1fe2ff7bb367c5284079ff1ab6c3c`
  - `describe-signals.py` `a669607c12fd2be84dd28c80d4826b415c21bae06ec28aa78b22f6fc564078c3`
  - `describe-dart.py` `145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f`

## Installs

- None. No tool was installed or updated. No pacman, uv, npm, or cargo action was taken.

## Open risks

- R1: The `wrong_operation` pass is recorded at `source_rev` `6615aea`, not re-observed at the candidate (F3).
- R2: The operation-keyed crediting and partial-match gaps are hypothetical. They are inferred from control design, not observed in candidate code (F1).
- R3: Any change to the `wrong_operation` value re-pins `counter-fixtures.py` → `expected-v2.json` → `count-c1.py:25`, so it must go through a new candidate (F1).
- R4: The absent-`operation` path and member-level code 2 are unpinned (F4). This is adjacent, not in this item.
- R5: Independence of `expected-v2.json` is established by absence of a candidate writer and by literal values. It is not proven by provenance records (F2).
