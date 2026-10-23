# FinalAxesBounds — residual critic review

Review evidence window: **2026-10-23T07:12:10Z–2026-10-23T07:16:00Z**. Reviewer: `KaidokuR32A2.FinalAxesBounds-2`.

Target product: `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26`; tree `b6372d2da1c4d26643c09563aa36529de3cf6c04`. Base: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.

**Advisory author-side evidence only. No canonical admission decision.** No production, counter, predicate, routing, MANIFEST, Git or jj state was changed. Only this report was written. No build, test, live reader, carrier execution, clone, package installation, or other review runtime was invoked. All subprocesses were finite read-only queries with 30-second deadlines; none remain owned. There was no clone/build requiring a `/fast` space check.

## Axes and result

- **Coverage / C1:** the proposed move is a previously reserved *input edge class*, not a new verb: synthetic exported-leaf ARM64X DLLs, native-view import/`binary_overview` only. The ordinary ARM64 PE capability already existed at the base.
- **Calibration / C2:** the four-item summary restoration is maintenance. The unchanged lexical measure is falsified; a numerical match cannot establish a calibration improvement.
- **Depth:** no new dual-view, EC recovery, decompilation, internal/call-reached-function, or runtime holding follows from this experiment.
- **Evidence/provenance constraint:** byte-oracle hybrid classification, upstream input provenance, REA output, writer output and full committed/live measurement must remain distinct authorities.

**Residual finding:** one fixable baseline-provenance wording defect remains in frozen C1 motivation: it says the counter gives `province_ok=0` at the base, whereas the retained base execution exits 2 before that gate. Independent immutable-document evidence still establishes the reserved surface. Do not rewrite the freeze; append an explicit erratum when carrying that baseline into the final report.

The reopened final Core/Frontier wording does not make the broader recovery claims attacked below. C2's honest stop remains explicit. Separability is supported by static dependencies, not by a new executed ablation in this review.

## 1. Strongest C1 counterexample: k05 defeats an EC/dual-view interpretation

**Observed in retained, committed evidence; not freshly executed here:**

- `corpus/evidence/round-32/c1/carriers.tsv:6`: k05 has **1 native / 4 EC exports**, `-O1`, subject SHA-256 `cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf`.
- `predictions.tsv:6`: predicted procedure count **1**, eight segments, document `target-cc5c644a515b.dll`.
- `envelopes/k05.json`: `ok=true`, operation `binary_overview`, subject architecture `arm64`, normalized `procedure_count=1`, `segment_count=8`, evidence ID `ev_fec48cb3a4bee51c883fb18ae569f6ceffc0e7f3251c048af095ee479f23bee5`.
- `runs.tsv:6`: UTC `2026-10-23T06:57:07+00:00` to `2026-10-23T06:57:19+00:00`, exit **0**, exact producing argv:

```json
["npx","-y","rea-agents@6.5.0","inspect","/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll","--format","json","--full-output"]
```

Exact original stdout bytes are the committed `corpus/evidence/round-32/c1/envelopes/k05.json`, SHA-256 `8a945d4812794f045935573ff39d6c56ebe7b59942a4a023d99174f6916a0ffd`; its stderr file is empty. Recorded package version is `6.5.0`, package.json SHA-256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`.

**Inference:** one reported procedure is not a recovery of the four EC exports or a union of both export sets. This directly defeats an expanded reading of “ARM64X coverage” as dual-view recovery. It does **not** prove an inability to recover EC under some other request or provider. The roster has seven asymmetric rows (`k04,k05,k07,k08,k09,k10,k12`), not the frozen motivation's six; the lesson and entry already disclose that erratum.

There is also an authority boundary: `arm64x_oracle.py:104-109` supplies the hybrid classification from raw machine and declared code-map tags. REA's retained overview says `arm64`; it is not itself an ARM64X classifier receipt. The metadata-only validity limitation is already explicit in the lesson (`Producer and instrument limits`) and `SKILL.md:1056-1060`. Do not turn a successful native import into proof of EC ABI validity, Windows loading or execution.

### Does final wording survive that counterexample?

The bounded wording does:

| Surface at the target | Actual bound |
|---|---|
| `PROVINCE.md:82-83` | Synthetic exported-leaf native-view import/overview is bounded Core; published hybrids, dual-view/EC recovery and internal-function analysis remain Frontier. |
| `PROVINCE.md:353-359` | Core holding is native-view `binary_overview` on twelve pinned author-built leaf DLLs; explicitly not dual-view recovery, decompilation or execution. Published hybrids, internal functions and EC view remain unverified Frontier. |
| `corpus/README.md:85` | Twelve synthetic exported-leaf DLLs; published hybrids, EC recovery, internal functions **and runtime** remain Frontier. |
| `corpus/README.md:221` | Published ARM64X, dual-view/EC recovery and internal-function analysis remain unverified. |
| Hybrid entry `:35-37,49` | Structural classification is not loader/runtime proof; k05 bounds the view; dual-view/internal/runtime remain Frontier; no published third-party hybrid or execution was tested. |
| `SKILL.md:1058-1060` | Explicit k05 warning; published hybrids, internal-function counts and runtime are untested. |

The builder (`build-arm64x-carriers.sh:26-41`) generates exported arithmetic leaves, compiles native and EC objects separately and links both. That is fixture construction, not evidence of internal-function coverage. The entry additionally discloses that the inputs do not separate `max(VirtualSize, SizeOfRawData)` from raw size, and that the LLVM witness shares the builder's toolchain release.

**Impacted axes if widened:** coverage would be overstated; depth and calibration would acquire unsupported gains. **Smallest safe correction:** retain these bounds, and describe hybrid identity as the separate byte-oracle/build witness rather than a new REA classification capability. No new corpus breadth, EC recovery or runtime claim should be inferred from the generic first cell of the Core table. This is a limit on the admissible interpretation, not a canonical ruling on the bounded move.

## 2. Fixable defect: the base counter did not observe `province_ok=0`

Frozen `.ufo/waves/round-32/claims.json:16` includes:

> the counter's province_ok=0 at the base

The retained base receipt, `.ufo/waves/round-32/a2before/c1-base.txt`, instead contains exactly:

```text
utc_start=2026-10-23T06:45:22+00:00
argv=["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/c1-arm64x-positive.py", "--root", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "--rev", "283aad7f"]
PIN pinned input absent: corpus/evidence/round-32/c1/carriers.tsv at 283aad7f
exit=2
utc_end=2026-10-23T06:45:22+00:00
```

`c1-arm64x-positive.py:166-170` returns immediately on that missing input. The `province_ok` call and printed gate fields are only at `:219-223`. There is no observed base gate field in this run. This is a documentary provenance defect, **not** evidence of a different measured predicate result.

Independent base-document evidence is sufficient for the narrower unmoved-surface statement. The read-only immutable comparison of base to target shows exactly this old content under `## Frontier` (`PROVINCE.md:73`):

```text
- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
  procedures via Ghidra). Reserve: ARM64X hybrids (the 91MB Godot ARM64 template is held, arc2-r7).
```

The target adds the separate `## Round-32 additions to Core` table and replaces the reserve with the bounded split quoted above. Thus the new Core row is not a restoration of an existing ARM64X Core row. This document proof does not establish a universal historical absence of ARM64X experiments; the entry appropriately restricts its history claim and acknowledges prior linker exploration.

**Impacted axes:** provenance of C1's coverage baseline and calibration of the accompanying assessment. The independent Frontier-to-Core document evidence is not invalidated.

**Smallest safe correction, without changing any frozen byte:** append an erratum to the lesson/final report:

> The base C1 counter could not evaluate because pinned inputs were absent (exit 2); it did not print `province_ok`. The base PROVINCE heading and reserve text independently show no bounded ARM64X Core row.

`LOG.md:3038` already records the real exit 2. Do not replace the frozen claim, invent a base count, or rerun merely to overwrite this failure.

## 3. Lowest-axis tie is supported; finite proxies are not saturation evidence

Read-only immutable base `SCORECARD.md` provenance gives current values **coverage 10.0, depth 10, calibration 10** at lines 23–25, and `retired: none` at 155–156. Its line 31 says:

> A perfect finite proxy retires no domain axis and closes no promotion gate.

The introductory historical `[INFERENCE] calibration is the lowest axis` concerns its older baseline comparison; it does not change the three equal current values at the round-32 base. The frozen tie statement chooses coverage and calibration among tied lowest current axes, rather than retiring another axis or relabelling a measure.

**Observed:** the base-to-target SCORECARD diff adds only the three old capability-summary rows and the honest-stop explanation. It does not increase any owned-axis score. The restored rows retain historical first-working rounds 13, 14 and 17; the text explicitly says they are not three new acquisitions.

**Smallest safe correction:** none to the tie. Preserve the distinction between the score-10 structural proxies and domain mastery/promotion. Whether this bounded new input surface is sufficient for a canonical coverage improvement remains outside this review.

## 4. C2 honest stop remains explicit despite 4/4 lexical alignment

The strongest retained counterexample is not ambiguous prose. The committed negative fixture's four capability cells all begin:

> This capability was never demonstrated and cannot capture anything.

It then denies the source registry, quote audit, session-log capture and cross-pin attribution. Example full row from `.ufo/waves/round-32/controls/c2-negative/SCORECARD.md:621`:

```text
| retained REA Ghidra-session log capture | This capability was never demonstrated and cannot capture anything. It does not run analyze on a pinned carrier in a private-TMPDIR session and never keeps ghidra.log or script.log; no receipt validates offline. | `.ufo/waves/round-17/run-carriers.sh` | round-17 |
```

The retained receipt records measured sandbox revision `42d814ff5f46ac45bf2b6f9b659ac094bca88f61`, fixture SHA-256 `201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796`, unchanged counter SHA-256 `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`, UTC **2026-10-23T06:47:20.941072Z–06:47:21.012394Z**. Exact argv:

```json
["timeout","--kill-after=5s","300","prlimit","--as=4294967296","--","python3","-I","-B","tools/round-32/c2-capability-calibration-v3.py","--root","/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone","--rev","42d814ff5f46ac45bf2b6f9b659ac094bca88f61","--fleet","/home/vgpnk/Projects/shokunin"]
```

Exact stdout, exit **0**, stderr empty:

```text
round-13	P2-match	row 1 anchor evidence corpus/SOURCES.md, corpus/lessons/round-13.md; description words 8
round-14	P2-match	row 2 anchor evidence .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json; description words 12
round-17	P2-match	row 3 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 12
round-27	P2-match	row 4 anchor evidence tools/round-27/xpin-attribute.mjs; description words 11
statements=4 match=4 target=4 reverse_mismatch=0
```

The full fixture and receipt are committed in the target tree, not supported only by the sandbox path in the historical argv. Their immutable hashes were measured below. I did not repeat that run.

Final surfaces preserve the consequence:

- `corpus/lessons/round-32.md:10,18,38`: **Honest stop**, failed discrimination, no calibration improvement and no relabelled/re-frozen predicate.
- `SKILL.md:1069,1075`: v3 is a **falsified semantic measure**, exit 0 means lexical target only; the round stops honestly on C2.
- `SCORECARD.md:630`: “a passing numerical alignment is not calibration improvement.”
- `corpus/README.md:211` and `LOG.md:3041`: C2 honest stop remains explicit.

**Impacted axis:** calibration. **Smallest safe correction:** no change to the frozen C2v3 instrument, target or status. Keep the honest stop beside any numerical after value. Summary usefulness is not a repair of the falsified measure.

## 5. Separability: disjoint claim inputs, with an explicit execution limit

| Counter | Inputs that decide its claim | Does not require |
|---|---|---|
| C1 (`c1-arm64x-positive.py:35-46,109-150,166-223`) | Frozen c1 carrier/prediction TSVs, carrier bytes, byte oracle, REA package/live output, original-claim first-add timestamp, C1 entry/evidence IDs, c1 committed envelopes and PROVINCE Core row | SCORECARD summary rows, C2v3 claim/counter, fleet capability descriptions or the summary-restoration outcome |
| C2v3 (`c2-capability-calibration-v3.py:42-56,117-137,144-211`) | Pinned fleet MANIFEST; base and target SCORECARD; four historical keys/description words; resolving historical anchor paths | New C1 entry, PROVINCE, ARM64X carriers, oracle, envelopes, REA runs or new Core row |

C2 obtains the tree's path set, but its accepted anchors are frozen historical paths, not C1's new artifacts. C1 uses the original claims file for freeze timing; its embedded superseded C2v1 prose is not read as a second active C2 authority.

**Inference:** removing only the summary-restoration edits cannot directly improve or damage C1's evaluated fields; removing only the new C1 artifacts cannot directly change C2's four matching rows or historical anchors. This is structural separability, not a reported counterfactual execution. Shared lesson/LOG/index maintenance does not merge the claim surfaces.

**Unknown in this review:** executed ablation exits, a fresh full committed/live C1 target measurement at `bb0af56c`, and canonical axis/admission outcomes. No fresh exit 0 is claimed for them. The committed producer receipt is explicitly writer-only: `2026-10-23T06:56:33+00:00` to `06:58:38+00:00`, exit **3**, with twelve per-carrier `P1-pass` lines followed by:

```text
WRITE-MODE carriers=12 written=12 at 2026-10-23T06:58:38+00:00 (not a receipt; no target line)
```

Its exact outer argv is:

```json
["env","GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC","JAVA_HOME=/usr/lib/jvm/java-21-openjdk","timeout","--kill-after=10s","900","python3","-I","-B","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/c1-arm64x-positive.py","--root","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","--rev","33393e594f1e278777fa49020b42c66ac4fa352e","--write-evidence"]
```

Full retained stdout/exit/UTC bytes: `.ufo/waves/round-32/a2after/c1-write.txt`, SHA-256 `11699de222c03458b3f89cf331b7d6b5ba3c57fc72bac3ff5e5249e17bace768`. Writer results do not satisfy the committed/live clause by themselves; the entry already says so. No need to couple C2 to a later C1 result.

## Evidence identity and command receipts

All paths below are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless absolute. No claim relies solely on a scratch or tool-artifact citation.

### Own read-only identity query

Exact argv:

```json
["git","-C","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","rev-parse","HEAD","bb0af56c29e7b4c11d0583ed6697d0e17aba9d26^{tree}"]
```

Exit **0**, exact stdout:

```text
bb0af56c29e7b4c11d0583ed6697d0e17aba9d26
b6372d2da1c4d26643c09563aa36529de3cf6c04
```

The bracketing `date` argv was `["date","-u","+%Y-%m-%dT%H:%M:%SZ"]`, exit 0 both times; exact stdout was respectively `2026-10-23T07:12:10Z\n` and `2026-10-23T07:16:00Z\n`.

### Immutable-object SHA-256 queries

Each row was measured with this exact pipeline structure, with `REV` and `PATH` replaced by the literal row values (not a script or a test):

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show REV:PATH | sha256sum
```

Producer argv is `["env","-u","GIT_DIR","-u","GIT_WORK_TREE","-u","GIT_INDEX_FILE","git","-C","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","show","REV:PATH"]`; consumer argv is `["sha256sum"]`. Every pipeline exited **0**. Exact stdout for each is its hash below followed by two spaces, `-`, and newline. No stderr was reported.

| REV | PATH | SHA-256 |
|---|---|---|
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | tools/round-32/c1-arm64x-positive.py | 7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | tools/round-32/c2-capability-calibration-v3.py | 5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | tools/round-32/arm64x_oracle.py | 17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686 |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | PROVINCE.md | dc42da24b744c00cf61fd60577f5057a350700f8c3e283a183908db6cc2392b2 |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | SCORECARD.md | 147368d04410f2ced5725e24fba02a226bc7d89943fd8df85cb108f6f918f10c |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | corpus/evidence/round-32/c1/envelopes/k05.json | 8a945d4812794f045935573ff39d6c56ebe7b59942a4a023d99174f6916a0ffd |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | .ufo/waves/round-32/a2before/c1-base.txt | 7ba3c5c9c9ddcc7b71bba07248ea43063a4fda51fc4303ff7a5d2dfe2d5e7a31 |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | .ufo/waves/round-32/controls/c2-negative/SCORECARD.md | 201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796 |
| bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 | .ufo/waves/round-32/controls/c2-negative/receipt.json | dc2ca6a357defa83c60963a9bb61afa46fdc10d6e75b125473169d9e51dc9803 |
| 9a73680a | .ufo/waves/round-32/claims.json | 8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435 |
| f382e3b7 | .ufo/waves/round-32/claims-v3.json | a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d |

### Additional measured lane-byte hashes

Read-only `sha256sum` was invoked with the absolute lane paths corresponding to these rows. It exited 0; exact stdout used `HASH  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/PATH\n` for each argument, in order within the respective calls. These are worktree-byte measurements during the stated window, not claims about later edits.

| PATH | SHA-256 |
|---|---|
| .ufo/waves/round-32/claims.json | 8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435 |
| .ufo/waves/round-32/claims-v3.json | a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d |
| SKILL.md | d5a4cbd9fb208033f3dd4a963dc758608441e4a0009aa6d13ddbdf891474013e |
| corpus/README.md | a7adb58b95d71e6e26df3e83937b6af7d86a458391e8f785e2a90330d640df5b |
| corpus/lessons/round-32.md | a6eea0b454150269b83d717dd47963e0deb178a6f084f76a1498ad9c3e495ee6 |
| corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md | 2fe3ce11dfdc674be8934e9a0c6c614baebee0fd1e74f0fbdb81ca76b4be9229 |
| tools/round-32/build-arm64x-carriers.sh | 7da284da5986295263c69a8b7ee779638428d3bb6c9d5c9d8fb224c40a737ba3 |
| corpus/evidence/round-32/c1/carriers.tsv | 8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e |
| corpus/evidence/round-32/c1/predictions.tsv | fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b |
| corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s | 7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d |
| corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s | c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4 |
| corpus/evidence/round-32/c1/runs.tsv | 62df49f73c3a8da0caa94b4e93711edcb5bc21e30e77f79b8043d98a6e2856b9 |
| .ufo/waves/round-32/a2after/c1-write.txt | 11699de222c03458b3f89cf331b7d6b5ba3c57fc72bac3ff5e5249e17bace768 |

The two measured current claim hashes equal their respective immutable freeze hashes. This is byte evidence, not a substitute execution of a freeze-integrity gate.

### Immutable document queries used for the bounded baseline proof

Exact read-only Git argv tails, each exit 0, under `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

```text
blame -L 1,38 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 -- SCORECARD.md
blame -L 60,93 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 -- PROVINCE.md
```

The retirement query prepended `["env","-u","GIT_DIR","-u","GIT_WORK_TREE","-u","GIT_INDEX_FILE"]` and used:

```text
blame -L 144,156 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 -- SCORECARD.md
```

The movement query used the same sanitized prefix and exact Git arguments:

```text
diff --no-ext-diff --unified=2 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 -- PROVINCE.md SCORECARD.md corpus/README.md
```

The decisive document bytes are quoted above and reside at those immutable revisions; the queries did not run either claim counter. The three-file diff contains 20 insertions and four deletions. No dynamic separability or new target-met receipt is inferred from a document diff.

## Handoff boundary

The only proposed correction is the baseline execution erratum in section 2, outside frozen files. Keep C1's native-view/leaf/synthetic bounds and C2's honest stop unchanged. No counter/code/predicate change is proposed. Verification or canonical admission belongs to the assigned main/non-author process, not this critic.

Report: `.ufo/waves/round-32/a2residual/FinalAxesBounds.md`
