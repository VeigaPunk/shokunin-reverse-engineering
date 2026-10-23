# R30-C1 / R30-C2 causal separability review

## Verdict and review boundary

**Attack verdict: HOLDS for separation of measured results, with shared frozen inputs retained.** Neither canonical counter consumes the other claim's envelopes, run receipts, knowledge entry, or pass/match count. Each counter's success condition can be satisfied without the other claim's measured evidence. This is a **source-level inference**, not an observed target-reaching run. Actual target attainment is **unknown**: no counter, selftest, builder, REA command, or carrier/mutant was executed for this review.

**The literal file-inventory wording in `separability` is incomplete.** Both counters also read their own knowledge/documentation gates, shared source-registry content, package metadata, oracle code, and Git history. C2 reads the base carrier's bytes and working-tree manifest, not merely a SHA value. Consequently, separation does **not** mean either whole evidence directory may be deleted: C2 still requires the frozen C1 manifest and base carrier.

Axes examined: C1 coverage, C2 depth, causal result independence, and accuracy of dependency/provenance reporting. This review neither admits nor rejects either claim under the canonical judge.

Scope: all explicit file reads and project-code imports in the three Python files listed below; canonical measure commands with default envelope locations and without `--write-evidence`. Git reads are distinguished from working-tree reads. This is not an OS syscall trace: Python/Git/npm/REA implementation files, caches, configuration and dynamic-loader reads are not enumerable from these three sources alone. Their transitive behavior was not exercised.

Reviewed frozen revision: `4ee65c6771058284aa947a266475839d196ed4d4`. Source identity and frozen-revision receipts: E1–E3 below. All opened evidentiary sources were local primary files, accessed on **2026-10-23**.

## File-read table: R30-C1

All paths below are expanded for the assigned lane. For another `--root`, root-relative project reads move to that root; the oracle is instead loaded beside the executing counter (`HERE`). Rows describe reads inferred from source, not observed runtime I/O. `BASE` is `d210fb8fa62d2af04d009cfa0c65a4e8137dc742`.

| File / finite file set | Read authority and purpose | Located source |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py` | Executing counter code; it does not import the C2 counter. | C1:28–54,334–351 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py` | Imported from `HERE`, not from the measured Git revision. Its only explicit input-file read is the supplied carrier. | C1:50–54; O:130–135 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv` | Entire working-tree file and `git show <REV>:…`; equality and 16-row check. | C1:207–223 |
| The 16 absolute carrier paths in set A below | Each is existence-checked, SHA-256-read, read again by the oracle, and passed to the live REA CLI. | C1:57–62,125–130,220–236; O:130–135 |
| `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` | Read for SHA-256 and JSON version; version must be `6.5.0`. | C1:41,224–228 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` | `git show <REV>:…`; entry source line must name S089; entry text must contain each committed evidence ID. | C1:142–155,182–204,231–248 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` | Entire file via Git at `<REV>` and `BASE`; only presence/newness of S089 is tested. No S090 requirement. | C1:149–154 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` | Entire file via Git at `<REV>` and `BASE`; tests a new line naming the operation and C1 entry. | C1:158–166 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json` | **Addition history only**, through path-filtered `git log <REV> --diff-filter=A --format=%ct`; JSON content, including `separability`, is not loaded by the counter. | C1:169–173 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/envelopes/<carrier-id>.json`, for the 16 IDs in set A | Git blob at `<REV>` and first-addition history, when the live P1 predicate passes and this is not collection mode. Agreement with live evidence ID/packages and post-freeze addition are required. | C1:176–204,242–250,346 |

C1 does **not** read either claim's `runs.tsv` or saved `.stderr` files: those are collection-mode outputs (C1:254–262). It has no explicit read of C2 predictions, mutants, envelopes, refusal entry, or `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md`. The PyPI JSON named in frozen inputs is not read by either counter. The optional C1 `--envelopes-dir` can redirect its envelope lookup; the frozen canonical command does not use that override (C1:339,346).

## File-read table: R30-C2

| File / finite file set | Read authority and purpose | Located source |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py` | Executing counter and built-in mutant builder; it does not import the C1 counter. | C2:29–62,111–168,435–453 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py` | Imported from `HERE`; reads each mutant supplied by the counter. Its mention of S089 is a docstring, not a source-registry read. | C2:58–62,323,343–346; O:1–19,130–135 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv` | Entire **working-tree** TSV parsed into a dictionary; selects `elf-x86_64-uvx`, using its `path` and full `sha256`. Unlike C1, C2 does not `git show` this manifest. | C2:45–49,280–286 |
| `/fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx` | Entire base image read and SHA-checked against the selected manifest row plus the hardcoded prefix. Its actual section/document bytes generate all mutants. This is a shared frozen input, not a C1 inspection result. | C2:105–168,280–292 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv` | Working-tree read during rebuild for mutant hash checks; read again for measurement predictions; entire text compared with `git show <REV>:…`. | C2:293–317,324–328 |
| The 19 absolute mutant paths in set B below | Builder first rewrites files under its fixed mutant directory; measure reads each prediction's `path`, oracle reads it again, and REA receives that path. All 19 get an oracle attempt, including predicted refusals; oracle exceptions become `reading=None`. | C2:299–309,320–323,340–357; O:130–135 |
| `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` | JSON version and byte hash; version must be `6.5.0`. | C2:44,329–333 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` | `git show <REV>:…`; entry must exist and its source line must name S090. | C2:258–270 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` | Entire file via Git at `<REV>` and `BASE`; only presence/newness of S090 is tested. No S089 requirement. | C2:265–269 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md` | Entire file via Git at `<REV>` and `BASE`; tests a new line naming the operation and C2 entry. | C2:273–277 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json` | **Addition history only**, not JSON contents; provides the shared freeze time. | C2:334–336 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/envelopes/<mutant-id>.json`, for the 19 IDs in set B | Git blob at `<REV>` and first-addition history, when the live prediction matches and this is not collection mode. | C2:240–255,337,358–366 |

C2 does **not** read C1 envelopes, C1 run receipts, C1 evidence IDs, the positive knowledge entry, or `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md`. Its own saved `.stderr` and `runs.tsv` are write-only collection outputs, not measurement inputs (C2:370–378). Rebuilding precedes all measurement pin checks and REA calls; therefore using measure mode as an allegedly read-only probe would be unsafe (C2:289–324). None was run.

### Exact carrier path set A

The corresponding envelope ID is each path's final component.

```text
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-aarch64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-aarch64-uvx
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-riscv64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/elf-riscv64-uvx
/fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uvx
/fast/scratch/hyaku/kaidoku-r30/carriers/pe-x86_64-uvw
/fast/scratch/hyaku/kaidoku-r30/carriers/pe-arm64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/pe-arm64-uvx
/fast/scratch/hyaku/kaidoku-r30/carriers/pe-arm64-uvw
/fast/scratch/hyaku/kaidoku-r30/carriers/macho-x86_64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/macho-x86_64-uvx
/fast/scratch/hyaku/kaidoku-r30/carriers/macho-arm64-uv
/fast/scratch/hyaku/kaidoku-r30/carriers/macho-arm64-uvx
```

### Exact mutant path set B

These are both the frozen prediction paths and builder output paths. The corresponding envelope ID is each path's final component.

```text
/fast/scratch/hyaku/kaidoku-r30/mutants/g-relocated
/fast/scratch/hyaku/kaidoku-r30/mutants/g-recompressed
/fast/scratch/hyaku/kaidoku-r30/mutants/g-no-root
/fast/scratch/hyaku/kaidoku-r30/mutants/r-empty
/fast/scratch/hyaku/kaidoku-r30/mutants/r-nobits
/fast/scratch/hyaku/kaidoku-r30/mutants/r-compressed-flag
/fast/scratch/hyaku/kaidoku-r30/mutants/r-two-sections
/fast/scratch/hyaku/kaidoku-r30/mutants/r-not-zlib
/fast/scratch/hyaku/kaidoku-r30/mutants/r-trailing-bytes
/fast/scratch/hyaku/kaidoku-r30/mutants/r-over-1mib
/fast/scratch/hyaku/kaidoku-r30/mutants/r-inflate-ratio
/fast/scratch/hyaku/kaidoku-r30/mutants/r-not-utf8
/fast/scratch/hyaku/kaidoku-r30/mutants/r-bad-json
/fast/scratch/hyaku/kaidoku-r30/mutants/r-nesting-33
/fast/scratch/hyaku/kaidoku-r30/mutants/r-format-negative
/fast/scratch/hyaku/kaidoku-r30/mutants/r-extra-field
/fast/scratch/hyaku/kaidoku-r30/mutants/r-kind-dev
/fast/scratch/hyaku/kaidoku-r30/mutants/r-two-roots
/fast/scratch/hyaku/kaidoku-r30/mutants/r-index-outside
```

## Findings, counterexample and smallest safe correction

### F1 — No other-claim result gate found: HOLDS

**Observation:** C1's return condition is its own 16 passes, entry gate and province gate. C2's is its own 19 matches/19 predictions, entry gate and skill gate. Each uses only its own claim-row constant. The complete explicit read sites are tabulated above. Producing commands: E2 (exit 0, UTC `2026-10-23T02:42:57Z`) and E3 (exit 0, UTC `2026-10-23T02:44:07Z`), with exact output excerpts below.

**Inference:** For C1, removing C2 envelopes, run receipts, refusal entry, S090 row and C2-specific SKILL material does not remove a required result input. For C2, removing C1 envelopes, run receipts, positive entry, S089 row and C1-specific PROVINCE material does not remove a required result input. Preserve common instruments, frozen manifest/base carrier, predictions, package/runtime, shared source-registry file with the surviving claim's row, and freeze history. Own envelope histories must remain post-freeze. Under those conditions, the other's results are not prerequisites for either success gate.

Both counters physically fetch the complete shared source-registry blob, so it can contain the other's source row; neither requires or interprets that other row as a result. Likewise, shared freeze history is not a dependency on the other's successful measurement. This is semantic/result independence, not disjoint file access, disjoint specimens, independent runtimes, or statistical independence.

**Impacted axes:** No source-level cross-result coupling found between coverage and depth. **Unknown:** whether actual live REA runs can satisfy all frozen predicates; no success receipt is claimed.

### F2 — Strongest boundary counterexample: whole C1 tree absence FAILS

**Observation:** C2 calls `do_build(root)` before measurement, which calls `base_carrier(root)`, opens the C1 manifest, selects the base row, and opens its image bytes. Producing commands: E2 (exit 0, UTC `2026-10-23T02:42:57Z`) and E3 (exit 0, UTC `2026-10-23T02:44:07Z`).

**Inference / static counterexample, not an executed mutation:** A root retaining C2 predictions/results but missing `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv` would fail at the unguarded `open` in C2:281 before its measurement loop. Keeping that TSV but removing `/fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx` would fail at C2:283. Thus a promise that C2 works with the *entire* C1 evidence tree absent is false. Merely retaining the SHA scalar is also insufficient: deterministic mutant construction needs the base bytes.

This does **not** refute result separability: the frozen contract explicitly allows the C1 carrier-list input, and the base image is input material rather than a C1 REA observation. It does refute an unrestricted reading of “reads only” and “evidence absent.” The documented inventory also omits the knowledge/registry/documentation/package/history reads in both tables.

**Impacted axes:** Dependency-reporting precision and the interpretation of the coverage/depth separation boundary; no demonstrated consumption of the other's measured result.

**Smallest safe correction:** In review/measurement receipts, state **“result-separable with shared frozen manifest, base-image bytes, oracle, runtime and freeze metadata retained”** and use the tables above as the actual read inventory. An absence control must remove the other claim's result files/rows, not its shared frozen inputs or the entire common source-registry file. Do not amend the frozen claims, predicates, counters, or targets to resolve a wording ambiguity. No implementation edit is needed to remove a cross-result dependency because none was found. Shared-input reuse is a design limit, not evidence that either axis has passed.

## Evidence receipts

Commands below were bounded, completed synchronously, and used only read-only Git operations or hashes. The reported UTC is the command's initial timestamp. All reported exits are tool-observed. No background process was started.

### E1 — Current source hashes

UTC `2026-10-23T02:42:57Z`; exit **0**.

```sh
timeout 10 date -u +%Y-%m-%dT%H:%M:%SZ && timeout 20 sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv
```

Exact stdout:

```text
2026-10-23T02:42:57Z
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py
1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py
f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py
65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json
c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv
6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv
```

The three instrument hashes and both TSV hashes equal those recorded in the opened claims file; this is an observation of the listed identities, not a live-counter result.

### E2 — Frozen-revision file-read sites

UTC `2026-10-23T02:42:57Z`; exit **0**.

```sh
timeout 10 date -u +%Y-%m-%dT%H:%M:%SZ && timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -E 'separability|PKG_JSON =|CARRIERS =|PRED =|MUT_DIR =|ENTRY =|spec_from_file_location|def (entry_ok|province_ok|skill_ok|freeze_time|added_time|first_add|base_carrier|do_build|measure|read_file)|show\(root|git\(root, "(show|log)"|open\(|oracle.read_file|sha256_file\(|return 0 if|subprocess.run\(argv' 4ee65c6771058284aa947a266475839d196ed4d4 -- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json
```

Exact stdout excerpts:

```text
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:149:    sources = show(root, rev, "corpus/SOURCES.md") or ""
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:159:    text = show(root, rev, "PROVINCE.md") or ""
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:234:        sec, doc = oracle.read_file(r["path"])
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:245:                committed = json.loads(git(root, "show", rev + ":" + rel).stdout or "null")
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:265:    srcs = show(root, rev, "corpus/SOURCES.md") or ""
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:281:    rows = {r["id"]: r for r in csv.DictReader(open(os.path.join(root, CARRIERS)), delimiter="\t")}
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:283:    data = open(r["path"], "rb").read()
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:361:                committed = json.loads(show(root, rev, rel) or "null")
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/rust_dep_oracle.py:131:    with open(path, "rb") as f:
```

### E3 — Frozen-revision gates and builder dependency

UTC `2026-10-23T02:44:07Z`; exit **0**.

```sh
timeout 10 date -u +%Y-%m-%dT%H:%M:%SZ && timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -E 'CLAIM_ROW =|BASE_ID =|BASE_SHA =|r = rows\[BASE_ID\]|if do_build\(root\)|base = base_carrier\(root\)|if sha\(data\)|if re.search|if not re.search|if not src or CLAIM_ROW|lines = \[l for l|if cid not in entry_text|if verdict ==|env_dir =|envelopes-dir|return 0 if passed|return 0 if matches' 4ee65c6771058284aa947a266475839d196ed4d4 -- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py
```

Exact stdout excerpts:

```text
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:42:CLAIM_ROW = "S089"
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:267:    return 0 if passed == TARGET and e_ok and p_ok else 1
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c1-rust-positive.py:346:    env_dir = a.envelopes_dir or os.path.join(a.root, "corpus/evidence/round-30/c1/envelopes")
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:51:CLAIM_ROW = "S090"
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:282:    r = rows[BASE_ID]
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:290:    base = base_carrier(root)
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:321:    if do_build(root) != 0:
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:337:    env_dir = os.path.join(root, "corpus/evidence/round-30/c2/envelopes")
4ee65c6771058284aa947a266475839d196ed4d4:tools/round-30/c2-rust-refusals.py:383:    return 0 if matches == TARGET and len(preds) == TARGET and e_ok and s_ok else 1
```

## Opened-source register

Each URL identifies the bytes read locally with ordinary file tools. Access date for every row: **2026-10-23**. Hashes are the E1 whole-file byte hashes. Located quotations contain at most 25 contiguous words each. Labels C1, C2 and O used above resolve here.

| Label / source URL | SHA-256 | Located quote |
|---|---|---|
| C1 — [positive counter](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py) | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | L209: `frozen = show(root, rev, CARRIERS)` |
| C2 — [refusal counter](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py) | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | L321: `if do_build(root) != 0:` |
| O — [independent oracle](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py) | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` | L131: `with open(path, "rb") as f:` |
| [Frozen claims](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json) | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | L38: “Each counter can exit 0 with the other claim's evidence absent.” |
| [Carrier manifest](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv) | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | L3: `elf-x86_64-uvx` |
| [Mutant predictions](file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv) | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | L2: `g-relocated` |

## Execution and artifact accounting

- No live counter, REA, builder or selftest run; no target line was observed or claimed.
- No foreign artifact was executed. No agent was spawned and no runtime/judge was invoked.
- No installation or tool update.
- No scripts, drafts, raw-output files, or other scratch artifacts were created; therefore there are no additional artifact hashes to list.
- The only lane write is this scoped report. All investigation commands completed; no background process was started.
