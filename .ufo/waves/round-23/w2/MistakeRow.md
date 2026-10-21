# MistakeRow: source review of the round-23 metadata-ancestry Mistakes row

Seat `KaidokuR23.MistakeRow` (reviewer, leaf, author-side). Round 23, claim R23-C1. Paths below are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Candidate `2838351450ff1ee4baa620c962a1153450d53311`; baseline B `aa1450b82f9ede35aada63efe8a34e01c6e02f72`; producer source V `6615aeae642aec36959180e7ea940b2794c7f1cb`. Author-side only; not outside admission, not authentication.

Scope item: the first Mistakes row of `corpus/lessons/round-23.md` ("vacuous / attribution, metadata ancestry was discarded before binding", line 48), with its W1 evidence, QUALITY31, the expected-v2 controls and the metadata red/green record.

Boundary: static reading of candidate bytes only (`git show`, `git ls-tree`, `git log`, `git grep`), a read-only `jq` key census on envelopes, `sha256sum`/`diff`/`grep` on extracted copies. No counter, selftest, verify producer, binder, fixture, REA/MCP call, debugger, device, network access or install was executed. Candidate bytes were extracted into the ignored `.ufo/waves/round-23/runtime/MistakeRow/` directory. Target-derived text is treated as data.

## Verdict

- The row's classification holds. QUALITY31 (`corpus/QUALITY.md:41`) covers the metadata case under its typed-refusal-ancestry wording (reading caveat in F5), and no new criterion was added (QUALITY.md is byte-identical at B and at the candidate).
- The row's Evidence column reproduces the W1 finding accurately (F4).
- Legacy red to strengthened green is attributable at the bind level for `meta_false` and `meta_array`: identical inputs, and the wrapper is the only difference. The sibling case and the counter-level red are not recorded in any retained record (F4).
- Needs correction: a causal sentence at lesson line 87 (F2), and a historical-scope disclosure missing from row 48 (F3).
- Adjacent, but in the frozen set the row cites: expected-v2 changed the `old_source` expectation from v1 with no retained rationale, and the S058 floor is no longer pinned by any frozen case (F1, Medium).

## Findings

### F1. Medium. Oracle superseded without a record; the S058 floor is no longer pinned

Observed:
- `.ufo/waves/round-23/frozen/expected.json` and `expected-v1.json` are the same bytes (sha256 `ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24`, schema `r23-independent-counter-controls-v1`, 14 cases). `expected-v2.json` (sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`, 21 cases) is the file the candidate counter pins at `.ufo/waves/round-23/tools/count-c1.py:25`.
- The only shared case with a different expectation is `old_source`: v1 `exit 1, count 1, c1_incomplete` (`expected-v1.json:33-36`), v2 `exit 2, count null, unevaluable` (`expected-v2.json:33-36`). v2 adds seven cases: `absolute_citation`, `catalog_changed`, `historical_root_injection`, `inherited_lost`, `meta_array`, `meta_false`, `sibling_refusal`.
- All oracle files, `frozen/counter-fixtures-v1.py` (sha256 `96e65034bcf2206c0e9c6335da264695f4741ed91e9a357c56484e6cd35e2849`), `tools/count-c1.py` and `tools/counter-fixtures.py` entered history in a single commit, `2b40aec`. `git log` shows no other commit touching them. `frozen/` and `tools/` are absent at declaration commit `a3c92eb`. No committed intermediate records why `old_source` changed.
- The `old_source` fixture code is the same in v1 and v2. It rewrites the S051 row (`.ufo/waves/round-23/tools/counter-fixtures.py:77-78,85-86`). The v1-to-current diff shows only added cases and the git-add list changed.
- The lesson never mentions `expected.json` or `expected-v1.json`. W1 treated the old case as the floor pin: `w1/CounterRefusals.md:265-267` ("the `old_source` S051 case (it already pins the S058 floor for new evidence)"). `w1/ReviewSourceReuse.md:11` reads it as "S051 cannot qualify a new entry". `w1/CriticSeparation.md:15` treats `frozen/expected.json` as the selftest oracle.

Inferred (source reading, not executed):
- The candidate counter rejects that fixture at `.ufo/waves/round-23/tools/count-c1.py:72-73` (`historical_sources_changed`), before the new-entry scan at `:123`. So `old_source` yields exit 2, and v1's expectation cannot be met by the candidate. Running v1 against the candidate would fail 1 of 14 cases.
- After the change, the floor check `int(sid[1:]) >= 58` (`count-c1.py:107`) decides no frozen case. The only fixture citing a source below S058 is `old_source`, and it stops at `:72-73` first. Deleting the floor would, by static reasoning, leave all 21 v2 cases passing. Under the current design the floor is not independently testable by the frozen suite: an S-row used-by edit trips the prefix guard, and a fixture cannot change the baseline rows.

Recommendation: name the supersession in the lesson (v1 retained, why the exit changed, which guard now preempts the case). State that the floor is guard-preempted rather than independently pinned. No new criterion is needed.

### F2. Low. Causal sentence and credit state around the metadata row

Observed:
- `corpus/lessons/round-23.md:85-88`: "changing only its copied input gives 2 snapshot_tampered. Thus the named fix is shown able to fail".
- `.ufo/waves/round-23/verify/initial/frozen-input-red.json` (sha256 `2ba7650db8511870e72a599dcd246d37089f488bf66d9cb134be44af133ebc4a`): `expected_exit 2`, `exit 2`, `passed true`, stdout `snapshot_tampered: .ufo/waves/round-23/frozen/fixture.json`. The check is the selftest manifest/input hash pin (`count-c1.py:139-144`, record at `verify.py:66`). It asserts a fixture hash and does not exercise refusal logic, so a tampered fixture fails identically under the legacy binder. It cannot show that the metadata fix discriminates.
- The discriminating record is `.ufo/waves/round-23/verify/initial/metadata-red-green.json` (sha256 `1286b8c41deff5892b2889073487b75c222a61fa1fa7eef8f3d1ad21ade97e79`; `source_rev` V; `legacy_sha256` `c925918f…`; `counter_sha256` `f4b8d16a…`, equal to the candidate counter). Legacy/current: `positive 0/0`, `meta_false 0/1`, `meta_array 0/1`, `passed true` (`verify.py:81-89`). It covers two of the four metadata controls. There is no sibling pair.
- Row 48 says a final producer must record red/green "before any fix credit". `.ufo/waves/round-23/verify/` in the candidate contains only `initial/`.

Recommendation: rewrite line 87 to say that metadata-red-green gives legacy 0 against current 1 for `meta_false` and `meta_array` on identical inputs at V; that the sibling and counter-level red are not recorded; and that no fix credit is given until the final producer runs.

### F3. Low. Historical R22 witnesses remain on the legacy binder; row 48 does not say so

Observed:
- `.ufo/waves/round-23/tools/count-c1.py:81` `historical = r22.measure(root, BASELINE)`. Its candidate loop calls the legacy `bind_cli` at `.ufo/waves/round-22/tools/count-c1.py:160`. `bind_new` is called only at `count-c1.py:123` (the new-root scan).
- Row 53 (`lesson-round-23.md:53`) discloses the scope: "Historical award is measured at immutable B … one explicit new-entry scan invokes the reviewed original-envelope binder". Row 48 says only "New wrapper traverses …".
- The historical root is pinned by tree identity (`count-c1.py:66-68`) and by a baseline check (`:82-83`).
- Key census on candidate bytes: `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json` and `identify-flutter-build-saber.envelope.json` have top-level keys `[ok,data,meta]` and meta keys `[command,duration]`. Below the top level, the only control-named paths are `ok`=true at top level and `data.raw_result`=null, plus `data.provider` (no control keys). No `error`, `errors`, `code`, `status`, `completion_status` or `exit_code` below top level.

Inferred: no current effect. `bind_new` would return the legacy result for these two bytes.

Recommendation: add one sentence to row 48: the historical baseline witnesses remain legacy-bound, their key census is clean, and the wrapper does not reach them.

### F4. Info, verified. Evidence accuracy and attribution

Observed:
- Mechanism. Legacy `bind_cli` (`.ufo/waves/round-22/tools/count-c1.py:76-80`) checks top-level `ok` and `refused(envelope)`. For `meta` it checks only that it is a dict, `meta.command`, and `refused(meta)` (`:79`). The DFS covers only the record (`:84-94`). Only `json.dumps(record)` reaches `r21.bind` (`:96`). So `meta.ok` and metadata lists are never inspected, and the row's causal sentence holds.
- `refused()` in `.ufo/waves/round-21/tools/verb-coverage.py:39-55` is list-blind: a non-dict returns False (`:41`), and recursion covers only `raw_result` and `normalized_result` (`:52-54`).
- Evidence column. W1 `ReviewEvidenceBinding` reports `meta.ok:false` → 0, a `meta.raw_result` list → 0, `meta.error` → 1, `meta.exit_code 1` → 1 (`w1/ReviewEvidenceBinding.md:13`). The same results follow from the source above.
- Attribution. `metadata-red-green.json` gives the same `text` to both binders. `bind_new` (`count-c1.py:42-56`) returns 1 from a pre-scan (`:45-53`), otherwise returns `r22.bind_cli(...)` unchanged (`:54`). So it returns 0 only where legacy returns 0: it can lower counts and cannot add a witness. This is established by reading.
- Sibling control. Legacy never reads top-level `result` (`.ufo/waves/round-22/tools/count-c1.py:74-96`), so legacy returns 0 for `sibling_refusal`. `bind_new` returns 1 through the pre-scan at `.ufo/waves/round-23/tools/count-c1.py:51`. [Inferred; not executed.]
- Counter-level red. Under the legacy binder, `meta_false`, `meta_array` and `sibling_refusal` would each give count 2 against an expected 1, with exit 1 unchanged. [Inferred; not executed. No legacy-counter run against the v2 fixtures is retained under `verify/initial/`.]
- Current effect. The four successful R23 witnesses carry no control keys below top level (census). For them `bind_new` equals legacy, so the 4/6 count is not changed by this fix.
- Frozen expectation: `sibling_refusal` expects exit 1 and count 1 (`.ufo/waves/round-23/frozen/expected-v2.json:88-91`), the result the candidate should produce for the refused new witness.

### F5. Info. QUALITY31 coverage and the no-new-criterion check

Observed:
- `corpus/QUALITY.md:41` (row 31): "…all typed refusal ancestry. A detached data copy cannot override a refused parent." QUALITY.md git blob `4af8644e042b459289d14511fc3a497f0e694a23` at B and at the candidate.
- `git diff --stat` between B and the candidate is empty for `corpus/QUALITY.md`, `.ufo/waves/round-21`, `.ufo/waves/round-22/tools`, `.ufo/waves/round-22/frozen`, `.ufo/waves/round-22/evidence/c1`, and `corpus/lessons/round-22.md`. Only `corpus/SOURCES.md` changed (+6 rows).

Inferred: the classification holds. An `error`-bearing metadata array is "typed" directly. A bare `meta.ok:false` is covered only under QUALITY31's "success status" reading. That is acceptable, but the reading should be named if it is challenged.

### F6. Info. Re-evaluation of stale W1 proposal findings against the candidate

- `w1/ReviewEvidenceBinding.md:7` ("Medium, refusal ancestry in meta only partially preserved"): closed for new-root witnesses by `bind_new`. Open-latent for historical witnesses (F3). Its pins and line cites for the R22 counter (`c925918f…`, `count-c1.py:76-96`) and for R21 (`615369384bf…`, `verb-coverage.py:39-55`) match the candidate bytes exactly. Its fixture cites (`counter-fixtures.py:82-89`, `:121-128`, `:131-134`, at `w1/ReviewEvidenceBinding.md:13`) cannot be reproduced from committed bytes: the committed `counter-fixtures-v1.py` has 99 lines and no metadata `ok`, array or sibling case. The substance (no metadata ok/array case in the committed C1 list) holds.
- `w1/CounterRefusals.md`: its pinned counter `count-c1.py` (sha256 `7c356b97…`) does not appear in the path's committed history. That history has one commit, `2b40aec`, blob `f4b8d16a…`. Its counter line cites (`:80-85`, `:153-164`, `:168`) do not apply to the candidate. Its `HEAD a3c92eb` pins were untracked worktree bytes: `frozen/` and `tools/` are absent at `a3c92eb`. N1 (meta `ok`) and N2 (sibling containers) are implemented by `bind_new` for the new root. N15 (`w1/CounterRefusals.md:237`, historical parity) is not implemented; the historical root stays legacy (F3). Its §5 item 4 (`:265-267`), which kept `old_source` as the floor pin, was not carried into v2 (F1).

## Produced files and hashes

Report: `.ufo/waves/round-23/w2/MistakeRow.md`. Its sha256 is recorded in the sidecar `.ufo/waves/round-23/w2/MistakeRow.md.sha256`, written after finalization.

Candidate bytes (`git show 2838351450ff1ee4baa620c962a1153450d53311:<path>`, sha256 of raw bytes):

| path | sha256 |
|---|---|
| `.ufo/waves/round-23/tools/count-c1.py` | `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` |
| `.ufo/waves/round-23/frozen/expected-v2.json` | `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` |
| `.ufo/waves/round-23/frozen/expected-v1.json` (= `expected.json`) | `ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24` |
| `.ufo/waves/round-23/frozen/counter-fixtures-v1.py` | `96e65034bcf2206c0e9c6335da264695f4741ed91e9a357c56484e6cd35e2849` |
| `.ufo/waves/round-23/frozen/fixture.json` | `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` |
| `.ufo/waves/round-22/tools/count-c1.py` (legacy, pinned) | `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` |
| `.ufo/waves/round-21/tools/verb-coverage.py` | `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b` |
| `.ufo/waves/round-23/verify.py` | `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a` |
| `.ufo/waves/round-23/verify/initial/metadata-red-green.json` | `1286b8c41deff5892b2889073487b75c222a61fa1fa7eef8f3d1ad21ade97e79` |
| `.ufo/waves/round-23/verify/initial/frozen-input-red.json` | `2ba7650db8511870e72a599dcd246d37089f488bf66d9cb134be44af133ebc4a` |
| `corpus/lessons/round-23.md` | `8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723` |
| `corpus/QUALITY.md` (git blob `4af8644e…` at B and candidate) | `ba6a20b3632f9f1a6f1e5ad50d9637bffa7933dfb9440d3faac9422b293b2c73` |
| `.ufo/waves/round-23/w1/ReviewEvidenceBinding.md` | `1aa11568b6fecbba79945d154446711d116cc154c1e4c39b5c2023ac4dcd98f2` |
| `.ufo/waves/round-23/w1/CounterRefusals.md` (equals its sidecar) | `a899d270309dc32bdc887e0534f6da37097c1cf689c5a0b42610f705411b370d` |

Runtime extracts (ignored, `.ufo/waves/round-23/runtime/MistakeRow/`), verbatim `git show` of the paths above: `r22-count-c1.py`, `r21-verb-coverage.py`, `r23-count-c1.py`, `r23-counter-fixtures.py`, `expected-v1.json`, `expected-v2.json`, `expected.json`, `counter-fixtures-v1.py`, `fixture.json`, `lesson-round-23.md`, `QUALITY.md`, `verify.py`, `metadata-red-green.json`, `frozen-input-red.json`. Their sha256 values match the table.

## Commands and exits (all read-only)

- `git rev-parse`, `git show`, `git ls-tree`, `git log`, `git diff --stat`, `git grep`: exit 0. `git show`/`git rev-parse` of `frozen/` and `tools/` at `a3c92eb`: `fatal`, expected, since those paths are absent at that commit.
- `jq` key census over six candidate envelopes (two R22 identify, four R23 successful, one R23 refusal): exit 0. One earlier `jq`/`diff` call failed on a relative path inside process substitution; it was re-run with absolute paths and the results above come from the re-run.
- `diff` on expected v1 against v2 cases: exit 1 (differences recorded in F1). `diff` on fixture v1 against candidate: exit 1 (recorded in F1).
- `ls` of `.ufo/waves/round-23/w2/MistakeRow.md` before writing: absent, as expected.
- No counter, selftest, verify producer, binder, fixture run, REA/MCP call, debugger, device or network access was made.

## Installs

None. `jq`, `python3` and `git` were already present. No pacman, uv, npm or cargo action and no config edit.

## Open risks and verification gaps

1. The sibling bind-level red and all counter-level legacy reds are source-derived. They need one legacy run against `expected-v2` fixtures, which only a designated Run seat may execute. Not run here.
2. The F1 exit-2 cause and the floor-insensitivity claim are inferences. A v1 run against the candidate and a floor-removal mutation would confirm or refute them. Not run here.
3. No final producer exists (`verify/` contains only `initial/`), so metadata-row fix credit is still pending.
4. Over-refusal (fail-closed undercount): the whole-tree predicate in `bind_new` refuses any non-true `ok`, truthy `error`/`errors`, refusal-token `code`/`status`/`completion_status`, or non-zero `exit_code` at any depth, including future metadata or sibling fields. No instance is present in the six envelopes sampled, and none raises a count.
5. Vocabulary limit: the pre-scan recognises R21 `REFUSALS` plus `ok`. Any other success-status field name would not be seen. None was observed in the sampled envelopes.
6. Independence: `fixture.json` is shared by `counter-fixtures.py` and `verify.py`, and the metadata pair's expected outcomes are hard-coded at `verify.py:89`. The controls are author-side and are not outside admission.
7. REA producer behaviour for `meta.ok` was not observed; no REA replay was made, per contract.
