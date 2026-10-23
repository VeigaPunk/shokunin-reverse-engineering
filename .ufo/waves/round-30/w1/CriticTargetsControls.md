# CriticTargetsControls — frozen-target shortcut review

## Scope and verdict

**Attack:** whether either target line, by the counter code alone, rules out junk documentation, fabricated committed records, id-keyed copies, input substitution, or runtime substitution.

**Attack verdict: fails as a blanket shortcut-resistance claim.** The live-value checks are substantial, but committed-record provenance, meaningful documentation, immutable input identity, and executable identity are not all enforced. Several shortcuts pass individual gates; some can coexist with a full target result. This is a source-review verdict, not admission or judgment of either round-30 claim.

- **[OBSERVATION]** Read both entire counters and the entire oracle, including measurement paths, argument handling, and selftests. Their working-file SHA-256 values equal the instrument values declared in the frozen claims (Q1–Q4, Q6).
- **[INFERENCE]** With the frozen inputs and a trusted REA executable, junk documentation or fabricated files cannot turn a failing live positive into a pass. C1 checks all 16 live positives; C2 checks three live acceptances and 16 live refusal-message conditions.
- **[INFERENCE]** That narrower property does not establish authentic committed envelopes or meaningful coverage/depth documentation. In particular, C2 accepts post-freeze `null` committed records for live refusals.
- **[UNKNOWN]** Neither complete frozen target has been exercised by this seat. No counter, selftest, REA, carrier, mutant, substitute runtime, or judge was executed. No predicted REA behavior below is reported as observed behavior.

Impacted frozen axes: **R30-C1 coverage** and **R30-C2 depth**. False provenance, identity drift, duplicate authorities, and premature saturation below are risk descriptions, not additional scoring axes.

## Source and evidence keys

All source aliases identify these absolute local paths:

- C1: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py`
- C2: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py`
- O: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py`
- F: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json`
- CT: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv`
- PT: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv`

Line references below come from numbered local reads. Q1–Q3 independently retrieved the frozen source text with read-only Git. Every table row cites its producing evidence command(s); their UTC times and exit codes are recorded below. **All admission/refusal conclusions in the table are [INFERENCE] from those observed source bytes, not executed controls.** “Admitted” describes the specified gate or conditional complete result, not permission under the frozen contract.

## Shortcut table

| Shortcut | Code admits or refuses it | Located code / exact output excerpt | Impact |
|---|---|---|---|
| Envelopes first added in the freeze commit | **Refused by both standard measurement paths.** Their addition timestamp equals the freeze timestamp, so equality fails. Existing files cannot be rescued merely by modifying them later. Collection mode is a separate exception below. | Q1, C1:184–187: `if env_added is None or env_added <= freeze_ct:`; Q2, C2:247–248: `if freeze_ct is None or added is None or added <= freeze_ct:` | Both axes; the same-commit guard holds. |
| Later-committed envelope copied unchanged from another carrier/mutant | **C1: conditionally refused, not universally proved refused.** A different evidence ID or package multiset fails. If both happen to agree, it passes; the code alone does not prove cross-carrier ID uniqueness. Committed operation, subject digest, offset, and size are not checked. **C2: admitted for any live refusal if the copied record is also non-ok.** For live acceptances only ok and evidence-ID equality are checked; copied packages/subject are not checked. | Q1, C1:190–203: `if not cid or cid != lid:` and `if rea_tuples(metas[0]) != tuples:`; Q2, C2:249–255: `if c_ok != l_ok:` and `if l_ok and (committed.get("data") or {}).get("evidence_id") != (live.get("data") or {}).get("evidence_id"):` | Both axes; id equality is not origin authentication. An arbitrary unchanged positive copy is not guaranteed green. |
| Entry names evidence IDs only in an HTML comment | **Admitted by C1's naming gate.** It searches the entire raw entry string, not visible prose or a structured citation. An otherwise qualifying entry can put all IDs in a comment. **C2 does not require the entry to name IDs at all.** Live and other gates still apply. | Q1, C1:202: `if cid not in entry_text:`; Q2, C2:258–270 checks only entry presence, a source token, and source-row existence. | Coverage documentation / depth provenance. |
| PROVINCE line appears only inside a fenced code block | **Admitted by C1** if a physical line contains the operation token and entry path and no matching candidate line is identical to a base line. **The analogous SKILL code-block line is admitted by C2.** Neither parser recognizes Markdown structure or requires Core placement / a decision table. | Q1, C1:161: `lines = [l for l in text.splitlines() if "inspect-rust-binary" in l and ENTRY in l]`; Q2, C2:276: `lines = [l for l in text.splitlines() if "inspect-rust-binary" in l and ENTRY in l and l not in base]` | C1 coverage and C2 depth can be claimed by inert example text. |
| S089 row added while the rest of SOURCES is broken | **Admitted by C1's entry gate** if one physical line starts with the expected pipe-delimited row prefix, the first `source:` line contains S089, and the base has no such row. Row completeness, table validity, URLs, source identity, and unrelated corruption are not inspected. **C2 has the same issue for S090.** | Q1, C1:146–155, especially `if not src or CLAIM_ROW not in src[0]:`; Q2, C2:262–270 uses the same substring and row-prefix checks. The row-prefix regexes are at C1:150 and C2:266. | Both axes; a token is not a functioning source registry. |
| Predictions replaced in the measured revision and working tree together | **Admitted by C2 within limits.** It compares the working file to the measured revision, not to the freeze-commit bytes or frozen SHA-256. The builder requires each generated ID's expected SHA-256, but does not compare predicted kind, message, path, size, or code pointer to the generated tuple. Retaining ID/hash pairs while changing outcomes/paths therefore survives these pins. A working-tree-only edit is refused; altering expected generated hashes is refused. | Q2, C2:306: `if frozen and frozen.get(mid, {}).get("sha256") != h:`; C2:326: `if frozen_text is None or frozen_text != open(os.path.join(root, PRED)).read():`; C2:340–357 reads each row's path and judges its actual bytes, without comparing those bytes to the row's SHA-256. | C2 depth / frozen predicate identity. This is forbidden by F:6 even though the counter lacks the freeze-byte check. |
| Clone whose branch `main` points elsewhere | **With the specified explicit `--rev <REV>`: not a shortcut.** Content and addition-history reads use the supplied revision; moving `main` alone does not redirect them. Working input files must still agree with that revision. **If `--rev` is omitted: admitted as measuring the other `main`**, provided its inputs/history satisfy the remaining checks. No check binds that default ref to an intended commit. | Q1, C1:337 and Q2, C2:438: `ap.add_argument("--rev", default="main")`; Q1, C1:138 and Q2, C2:236: `p = git(root, "show", rev + ":" + rel)` | Both axes; explicit revision identity matters. Do not attribute the implicit-default variant to the canonical explicit command. |
| REA cache contents or `npx` resolution swapped | **Not authenticated by either counter.** Both check that one fixed package.json says version 6.5.0; both calculate its hash but never compare it to the frozen expected hash. The executable comes from inherited process resolution, not a verified package entry point, and package code bytes are not hashed. A swap still must emit outputs satisfying the live predicates, but the code cannot prove those outputs came from REA 6.5.0. | Q1, C1:40–41, 127–128, 224–228; Q2, C2:42–44, 329–333, 348–349. Exact gates: `if pkg_ver != "6.5.0":`; exact launch: `p = subprocess.run(argv, capture_output=True, timeout=300, cwd="/tmp")` (C1:128). | Both axes; package metadata and the launched executable are duplicate, unbound authorities. No actual swap was investigated or performed. |
| Junk row + entry + PROVINCE/SKILL token, but no committed envelopes | **Refused as a complete target in ordinary measure mode.** Even when document gates pass and live runs succeed, the missing paths have no post-freeze first-add time. C2's permissive refusal-content check does not remove this path-history requirement. | Q1, C1:242–250 and 184–187; Q2, C2:358–366 and 247–248. Exact message in both: `committed envelope absent or not added after the freeze` | Both axes; document-only junk does not suffice. |
| All committed records are false/refusal records or null metadata | **C1 refused.** It requires a committed ok record with the expected packages and matching nonempty ID. **C2 cannot reach all 19 with every committed record false:** its three live acceptance cases require committed ok=true. Non-ok filler can nevertheless satisfy the 16 refusal record gates. | Q1, C1:188–201: `if not isinstance(committed, dict) or committed.get("ok") is not True:`; Q2, C2:249–254: `if c_ok != l_ok:`; Q5 / PT:2–4 identifies three acceptance predictions. | Both axes; “all-false control fails” is weaker than “every committed record is authentic.” |
| Oracle-fabricated positive record never produced by REA | **Cannot replace the required live call.** However, **its committed-record gate admits a fabrication** if C1's package tuples and live ID agree, or C2's live ok/ID agree. Neither counter checks how the committed bytes were produced. Matching content is not a production receipt. | Q1, C1:234–248 and 182–204; Q2, C2:348–364 and 246–255; Q3, O:130–135: `doc = decode(data[sec["offset"]:sec["offset"] + sec["size"]])` | Both axes; live value fidelity holds narrowly, committed production provenance does not. |
| Post-freeze C2 files containing `null`, or invalid JSON, for refusal IDs | **Admitted when the corresponding live refusal condition matches.** The loader produces `None`; the agreement function maps that and the live refusal to the same false ok bit, then skips all evidence-ID checking. A null record is not a refused REA envelope, but it passes this gate. An absent path still fails its first-add test. | Q2, C2:361–363: `committed = json.loads(show(root, rev, rel) or "null")` and `committed = None`; C2:249–255: `c_ok = isinstance(committed, dict) and committed.get("ok") is True` followed by the l_ok-conditional ID comparison. | C2 depth / strongest fixed-input committed-record counterexample. |
| Refusal message appears in process output but no refusal envelope exists | **Admitted by the C2 live refusal predicate.** A non-dict JSON value or JSON parse failure is not ok=true; a nonempty predicted substring in stdout/stderr suffices. Refusal judging does not require a nonzero exit, a structured error, operation, subject, or evidence ID. The acceptance branch does require live identity and oracle agreement. | Q2, C2:200–208: `if isinstance(env, dict) and env.get("ok") is True:` and `if not message or (message not in out_text and message not in err_text):`; C2:353–357 converts parse failure to `None`. | C2 depth; this is a frozen predicate limitation, not permission to reinterpret a noisy failure as established parser depth. |
| C1 carrier list replaced with 16 repeated rows / one carrier under different IDs | **Admitted by C1's input checks if committed and working copies agree and row hashes match actual files.** It checks row count, not uniqueness or the freeze-commit list hash. A full result would still require live success and qualifying committed records, but could represent one carrier repeatedly rather than the frozen 16. | Q1, C1:209–223: `if len(rows) != TARGET:`; C1:213 compares only measured revision with working file; C1:233 iterates every row. No set-of-IDs / frozen-byte validation occurs. | C1 coverage / premature saturation. This violates the frozen input contract and is not an admissible claim result. |
| Local oracle changed while using the same counter | **Not pinned by the counter.** Both import the neighboring working-file oracle through `HERE`, not the oracle blob at the measured revision, and never check its frozen hash. Unchanged oracle code is meaningful independent container parsing, not an id lookup. | Q1, C1:50–54 and Q2, C2:58–62: `spec.loader.exec_module(mod)`; Q3, O:99–110 locates exactly one section and O:130–135 reads its bytes. | Both axes; input/measurement authority can drift outside the revision. External frozen-instrument enforcement is required. |
| Use `--write-evidence` and present its green line as final measurement | **Admitted by the collection-mode code, not the canonical measurement command.** The flag skips committed-record and freeze-timing checks but shares the same final target formatter and success return. Genuine live results and document token gates remain necessary. A collection result can therefore be green before qualifying committed records exist. | Q1, C1:242: `if verdict == PASS_LABEL and not write_evidence:` and C1:265–267; Q2, C2:358: `if verdict == MATCH and not write_evidence:` and C2:381–383 | Both axes; command identity must distinguish collection from measurement. |
| Treat commit timestamps as proof of graph ordering | **Not robust.** Both choose minimum numerical committer timestamps from addition events, then compare integers. A graph-earlier addition can have a later timestamp than the freeze, and a graph-later addition can share its timestamp and be refused. This does not defeat the same-freeze-commit case above. | Q1, C1:169–179: `return min(times) if times else None`; Q2, C2:240–243 and 334–336: `freeze_ct = min(t) if t else None` | Both axes; chronology is an unauthenticated proxy for first-added-after ancestry. |

## Strongest fixed-input counterexample: C2 null records

**[INFERENCE, static trace only; Q2, UTC 2026-10-23T02:43:48Z, source command exit 0.]** Take any frozen predicted-refusal row whose genuine live run matches its predicted message. Add its committed record path after the freeze, but make its bytes `null` rather than a REA envelope.

1. C2:361 parses those bytes to `None`.
2. C2:247 passes if the recorded addition timestamp is greater than the freeze timestamp.
3. C2:249 computes c_ok=false; C2:250 computes l_ok=false for the live refusal.
4. C2:251 does not reject equality; C2:253 skips the ID comparison because l_ok is false.
5. C2:255 returns `True, "ok"`; C2:367 increments the match count.

No changed carrier, prediction, oracle, or runtime is needed for this record-content shortcut. It applies independently to all 16 refusal rows if their genuine live outputs match. With three qualifying acceptance records, all live matches, and the token-only entry/SKILL gates, the ordinary C2 target can coexist with 16 non-envelopes. **This is not an observed target pass**; the genuine live matches remain unknown. It falsifies the stronger claim that a green counter alone authenticates all committed envelopes.

C1 is stronger here: `None` is rejected at C1:188–189. Nevertheless, C1 only proves agreement of selected fields in its committed record, not that REA produced those committed bytes.

## Strongest identity counterexample: mutable predictions and row paths

**[INFERENCE, static trace only; Q2 and Q5, source commands exit 0 at the UTC times below.]** C2's builder validates generated bytes against the ID/hash pairs in the current predictions file, but measurement executes the paths from that file without binding those paths' actual hashes to those pairs. A later committed predictions file could retain all 19 generated ID/hash pairs while redirecting all row paths to one refusal mutant and making all predicted outcomes/messages that one refusal. The generated-file checks at C2:306 still pass; the revision/working equality check at C2:326 also passes. Measurement would run that one path 19 times. If that one genuine refusal matches and post-freeze non-ok records plus token-only docs exist, the count can saturate without exercising the frozen 19 cases.

The local evidence supplies an actual frozen refusal candidate, `/fast/scratch/hyaku/kaidoku-r30/mutants/r-empty`, and its frozen message, “Dependency section is not file-backed” (PT:5, Q5). Its REA outcome was **not** run or assumed established here. This counterexample tests the source's identity binding, not the prediction's correctness.

**Contract distinction:** F:6 fixes predictions from the freeze commit. Such a replacement is therefore an invalid receipt under the assignment, even if the counter prints green. It is an enforcement gap requiring rejection by the canonical admission/judgment route, not a permissible way to improve the round's depth result. The analogous repeated-carrier C1 variant is likewise a frozen-input violation.

## Smallest safe corrections / disposition

No edits to the frozen counters, inputs, predicates, or targets are proposed for this round.

1. **Frozen identity and route defects — fixable at admission:** before relying on a receipt, bind the explicit measured commit, freeze-commit input/instrument hashes, unchanged neighboring oracle, and actual launched REA package code. The claims already record instrument/input hashes and package.json identity; the counters do not enforce all of them. Do not accept changed predictions/carriers, a collection-mode command, a moved implicit ref, or a substituted runtime as a canonical measurement.
2. **Committed-envelope defect — expose, do not silently amend P2:** reject `null`/invalid/non-envelope receipts as provenance evidence. A future instrument can require a real envelope and compare the intended identity/error fields for refusals as well as acceptances. Requiring full selected-field agreement for C1 committed subjects/operation/range would also prevent misleading copied fields. Those changes would be a new instrument, not a retroactive tightening of this freeze.
3. **Documentation shortcuts — canonical axis review remains necessary:** a comment containing IDs, a fenced PROVINCE example, a token-only SKILL line, or a broken source registry is not the claimed coverage/depth deliverable. Review the actual Core addition and decision table against the source material; do not infer them from `entry_ok`, `province_ok`, or `skill_ok`. These are surface-validity defects the canonical Rust judge must reject, not score-preserving tradeoffs that this seat may admit.
4. **Chronology — future implementation:** use the fixed freeze commit and graph relationships for first addition, not minimum committer time. For this round retain and disclose the timestamp limitation; do not rewrite history or manufacture dates.

Thus the narrow live/oracle guard **holds under trusted fixed inputs/runtime**, while the broader “any cheap shortcut is refused by the code” claim **fails**. No full target receipt is certified by this review.

## Producing commands, UTC, exit status, and exact excerpts

These were bounded read-only source observations. The quoted excerpts are actual output, not counter execution output.

### Q1 — C1 frozen source

Command:

```sh
timeout 30 date -u '+UTC %Y-%m-%dT%H:%M:%SZ' && timeout 30 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py
```

UTC output: `UTC 2026-10-23T02:43:48Z`. Exit: **0**. Exact excerpt (C1:202): `if cid not in entry_text:`.

### Q2 — C2 frozen source

Command:

```sh
timeout 30 date -u '+UTC %Y-%m-%dT%H:%M:%SZ' && timeout 30 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py
```

UTC output: `UTC 2026-10-23T02:43:48Z`. Exit: **0**. Exact excerpt (C2:249): `c_ok = isinstance(committed, dict) and committed.get("ok") is True`.

### Q3 — frozen oracle

Command:

```sh
timeout 30 date -u '+UTC %Y-%m-%dT%H:%M:%SZ' && timeout 30 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/rust_dep_oracle.py
```

UTC output: `UTC 2026-10-23T02:43:48Z`. Exit: **0**. Exact excerpt (O:108): `if len(hits) != 1:`.

### Q4 — opened-source byte identities

Command:

```sh
timeout 30 date -u '+UTC %Y-%m-%dT%H:%M:%SZ' && timeout 30 sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv
```

UTC output: `UTC 2026-10-23T02:43:48Z`. Exit: **0**. Exact excerpt:

```text
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py
```

The complete six returned hashes are transcribed in the source ledger below.

### Q5 — frozen predictions

Command:

```sh
timeout 30 date -u '+UTC %Y-%m-%dT%H:%M:%SZ' && timeout 30 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4ee65c6771058284aa947a266475839d196ed4d4:corpus/evidence/round-30/c2/predictions.tsv
```

UTC output: `UTC 2026-10-23T02:44:35Z`. Exit: **0**. Exact located excerpt (PT:5): `Dependency section is not file-backed`.

### Q6 — frozen claims

Command:

```sh
timeout 30 date -u '+UTC %Y-%m-%dT%H:%M:%SZ' && timeout 30 git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4ee65c6771058284aa947a266475839d196ed4d4:.ufo/waves/round-30/claims.json
```

UTC output: `UTC 2026-10-23T02:44:35Z`. Exit: **0**. Exact located excerpt (F:6): `a miss under them is reported, never amended, never re-scaled.`

## Opened primary sources

All accessed **2026-10-23** by ordinary local file reads; Q1–Q3/Q5/Q6 additionally used plain read-only Git retrieval. Each quote below is at most 25 contiguous words from the source. SHA-256 values describe the raw source file bytes, not tool formatting.

| URL | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | L202: `if cid not in entry_text:` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py` | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | L249: `c_ok = isinstance(committed, dict) and committed.get("ok") is True` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py` | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` | L108: `if len(hits) != 1:` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json` | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | L6: `a miss under them is reported, never amended, never re-scaled.` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv` | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | L3: `elf-x86_64-uvx` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv` | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | L5: `Dependency section is not file-backed` |

## Execution and artifact disposition

- Report is the only file written inside the lane. No lane/fleet index, history, working source, shared carrier, or shared mutant was modified.
- No scripts, drafts, raw-output files, or other scratch artifacts were created; therefore there are no auxiliary artifact paths or SHA-256 values to list. Evidence excerpts are retained directly in this report.
- No tools installed or updated. No services or continuing process trees started. All shell commands were finite and capped with `timeout` (30 seconds per invoked command; tool deadlines at most 70 seconds).
- No runtime/control results, target-line stdout, build/test/lint results, or claim admissions are asserted.
