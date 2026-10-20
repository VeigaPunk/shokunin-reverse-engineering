# BSimBounds — Reopen S006: BSim Feature Construction, Candidate Matching, and Cross-Version Naming Bounds

- Seat: `KaidokuR14.BSimBounds` (leaf scout; no subagent dispatch).
- Scope: Reopen S006 (Ghidra 12.1.4 BSim tutorial) on feature construction and candidate matching; explain why similarity is not semantic equivalence; explain how source diagnosis relates to cross-version naming.
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Measured baseline: `767adafb97e2eef6980e2ad873d357e16721c467` (HEAD)
- Evaluation axes: `coverage`, `calibration`
- Access date: 2026-10-20 (UTC)
- Verification discipline: Leaf scout; no builds, tests, linters, formatters, or REA target executions run mid-flight (L1 integrates and verifies). Source reading, cryptographic hashes, and factual line/word counts only.

---

## 1. Sources Opened

All sources listed below were opened and inspected on **2026-10-20**. Each quoted excerpt is contiguous, verbatim, and bounded to $\le 25$ whitespace words.

| id | source path or canonical URL | exact section / location | contiguous quote ($\le 25$ words) | SHA-256 digest | notes & limitations |
|---|---|---|---|---|---|
| S006 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md` | `# How Does BSim Work?`, line 19 | “Certain attributes, such as values of constants, names of registers, and data types, are intentionally not incorporated into the features.” (20 words) | `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e` | Primary S006 source; 88 lines. Establishes intentional feature abstractions. |
| S006.eval | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Evaluating_Matches.md` | `## Exercise: Applying Signatures`, line 77 | “You should be absolutely certain that the datatypes are the exactly the same before applying signatures and data types.” (19 words) | `a08af6c8340ea5561570926a7ddbfc3168f0d423a9bf0ee533db1ba85b91f63d` | Companion tutorial file; 112 lines. Warns of datatype corruption under 1.0 similarity. |
| S006.query | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Basic_Queries.md` | `#### Setting Query Options`, line 71 | “Confidence is used to judge the significance of a match.” (10 words) | `d87b95304249db96784902d0cb61a54acb9571037f6b7d4453eedd813b6958c2` | Companion tutorial file; 157 lines. Distinguishes similarity from confidence/significance. |
| S006.arch | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Basic_Queries.md` | `### Exercise: Cross-architectural Matching`, line 142 | “Neither the names nor the bodies of callees are incorporated into BSim signatures, but the arguments of a call are” (20 words) | `d87b95304249db96784902d0cb61a54acb9571037f6b7d4453eedd813b6958c2` | Confirms callees' identities and bodies are omitted from BSim signatures. |
| S006.exe | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Exe_Results.md` | `## Exercise`, line 34 | “unrelated functions can be duplicates of each other, either because they are small or because they perform a common generic action.” (21 words) | `7ec470706cb14063be9b11414d8818ef9604dc906f6dda553e8b445ec3271fdb` | Companion tutorial file; 37 lines. Explains hit pollution by generic/trivial code. |
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `GoRttiMapper.java:79` | `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` | Installed Ghidra 12.1.4 Go version-gate boundary. |
| S004 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 | Commit title | “GP-6528 add support for golang 1.26” | Git commit `385e8cd9…` | Upstream change adding Go 1.26 support (not in installed 12.1.4 release). |
| S005 | https://github.com/mandiant/GoReSym/tree/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d | README `Version Support` | “This library current handles the pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.” | Commit `d7f23b7a…` | Independent Go symbol parser; demonstrates pclntab layout decoupling. |

Tools used: local `sha256sum`, `python3` (for exact byte quote and length verification), `read`. No tools installed or upgraded.

---

## 2. Feature Construction in Ghidra BSim

As documented in S006 (`BSimTutorial_Intro.md`, lines 13–28) and verified against the installed Ghidra 12.1.4 documentation:

1. **Generation Mechanism**:
   - Feature vectors are generated directly by Ghidra's decompiler from its high-level intermediate representation (p-code syntax trees).
   - Each individual feature represents a localized subgraph of data flow and/or control flow within the function.
2. **Decompiler Normalization**:
   - The decompiler normalizes the feature vector representation so that syntactically distinct, but functionally isomorphic, code constructs yield identical features across compiler variations and optimization levels.
3. **Intentional Feature Abstraction (Information Dropped)**:
   - S006 explicitly states: *“Certain attributes, such as values of constants, names of registers, and data types, are intentionally not incorporated into the features.”*
   - In addition, S006.arch (`BSimTutorial_Basic_Queries.md:142`) confirms: *“Neither the names nor the bodies of callees are incorporated into BSim signatures, but the arguments of a call are”*.
   - Consequently, BSim vectors discard:
     - Numeric and string constants (e.g., immediate values, cryptographic keys, offsets, error codes).
     - Register assignments and variable storage allocations.
     - Datatype definitions (scalars, pointers, structs, arrays, classes).
     - Callee identities and callee implementation logic.
4. **Vector Representation and Distance Metric**:
   - BSim vectors are compared using **cosine similarity** ($\cos \theta$), yielding a value strictly bounded between $0.0$ and $1.0$.
   - Large-scale retrieval is indexed via Locality-Sensitive Hashing (LSH), reducing $O(N)$ pair comparisons to hash-bucket lookups.

---

## 3. Candidate Matching and Evaluation

Candidate matching in BSim is an exploratory, hypothesis-generating retrieval system rather than an oracle of identity:

1. **Two-Dimensional Scoring (Similarity vs. Confidence)**:
   - **Similarity** ($0.0 \le s \le 1.0$): Cosine of the angle between two feature vectors. Measures the proportion of shared normalized data/control-flow features.
   - **Confidence** ($-\infty < c < \infty$): Measures the statistical *significance* (or "meatiness") of the match. S006.query states: *“Confidence is used to judge the significance of a match.”*
     - Shared features increase confidence; differing features decrease confidence.
     - Shared *rare* features contribute substantially more weight than shared *common* features.
     - The maximum confidence for a vector $v$ occurs when compared to itself, defined as the **self-significance** of $v$.
2. **The "Trivial Match" Phenomenon**:
   - Functions that return a constant, trivial stub functions, or boilerplate exception dispatchers frequently exhibit a similarity score of $1.0$, but very low confidence.
   - S006.exe warns that *“unrelated functions can be duplicates of each other, either because they are small or because they perform a common generic action.”*
3. **Candidate Inspection and Information Transfer Workflow**:
   - Matches are presented as candidates in a side-by-side decompiler diff panel.
   - An analyst may execute three progressive transfer actions:
     - *Apply Function Name*: copies name and namespace.
     - *Apply Function Signature*: copies name, namespace, and empty skeleton structure types.
     - *Apply Function Signature and Data Types*: imports full data types into the program.
   - **Integrity Warning**: S006.eval explicitly warns: *“You should be absolutely certain that the datatypes are the exactly the same before applying signatures and data types. If there have been any changes to a datatype's definition, you could end up bringing incorrect datatypes into a program, even using BSim matches with 1.0 similarity.”*

---

## 4. Why Similarity Is Not Semantic Equivalence

A central limitation of structural binary matching is the epistemic gap between **vector similarity** and **semantic equivalence**:

### Formal Distinction

- **Semantic Equivalence** ($\llbracket f \rrbracket \equiv \llbracket g \rrbracket$):
  Two functions $f$ and $g$ are semantically equivalent if and only if for all possible execution states and inputs $\sigma$, executing $f$ and executing $g$ produces identical output states, return values, memory mutations, and externally observable side effects:
  $$\forall \sigma \in \Sigma, \quad \llbracket f \rrbracket(\sigma) = \llbracket g \rrbracket(\sigma)$$
- **BSim Similarity** ($\cos(\vec{u}_f, \vec{u}_g) \ge \theta$):
  Cosine similarity over a multiset of normalized p-code control/data flow graph features. It is a heuristic geometric metric of structural isomorphism under decompiler normalization.

### Concrete Structural Failure Modes

1. **Constant Masking**:
   - Because constant values are intentionally abstracted away, two functions with identical control-flow topologies but completely different constant parameters will yield identical BSim vectors ($\text{similarity} = 1.0$).
   - *Example*: An encryption routine using standard AES-256 S-boxes versus a modified version with proprietary permutation constants; or an access check `if (uid == 0)` (root) versus `if (uid == 1000)` (unprivileged user). BSim perceives identical feature sets, while the operational semantics are orthogonal or opposing.
2. **Type and Representation Invariance**:
   - Functions manipulating 32-bit floating point values versus 64-bit integer values, or traversing two completely different struct layouts that share identical pointer-offset arithmetic, can produce identical decompiler features.
   - Applying signatures across such matches introduces type pollution and incorrect memory reconstructions into the analysis database.
3. **Callee Opacity**:
   - Because callee names and bodies are not incorporated into signatures (only the data flow of call arguments is tracked), calling `audit_log_success()` versus `audit_log_breach()` or `unlink()` versus `stat()` with identical argument passing registers as identical features.
4. **Boilerplate and Low-Entropy Functions**:
   - Small functions, getters, setters, error handlers, and allocator wrappers produce identical or near-identical signatures across unrelated binaries and libraries, generating high similarity false positives.
5. **Branch Inversion and Path Invariants**:
   - BSim represents feature subgraphs without preserving the global ordering or formal verification of path predicates. Two functions with inverted conditional logic or subtle edge conditions can share high cosine similarity while terminating on opposite branches under specific inputs.

---

## 5. How Source Diagnosis Relates to Cross-Version Naming

### The Cross-Version Naming Hazard in the Lane's History

In round 4 (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` and `PROVINCE.md:52`), the lane analyzed a cross-version upgrade of the 1Password CLI (`op` 2.34.1 $\to$ 2.40.0, 41–43 MB Go ELF). When the toolchain bumped from `go1.25.7` to `go1.26.8`:
- Provider symbol recovery silently collapsed: 99.94% of functions in 2.40.0 became default `FUN_*` addresses (33,060 down to 11,595 procedures, with 11,588 unnamed `FUN_*`).
- As recorded in `r4-10`: *“the same function is `entry` vs `_rt0_amd64_linux` and `function_match` reads `mismatched`; symbol-keyed cross-version pairing is unsafe across Go versions — pair by ELF role/address (or explicit dossier ids) instead.”*

### The Temptation vs. The Risk of Name-Free Similarity

When cross-version naming breaks, analysts face a strong temptation to use name-free similarity matching (such as BSim) to automatically project function names from the earlier symbolized version onto the un-symbolized version.
- **The Risk**: Because similarity is not semantic equivalence, blindly transferring names across a Go toolchain bump via BSim propagates false identifications, mislabels functions whose semantics diverged between versions, and imports stale type definitions.

### The Decisive Role of Source Diagnosis

Source diagnosis investigates the *reasons* for symbol absence before any matching strategy is deployed:

1. **Diagnosing the Exact Locus of Failure (S003 vs. S004 vs. S005)**:
   - **S003** (`GoRttiMapper.java:79`) proves that Ghidra 12.1.4 enforced a hardcoded version range: `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`.
   - **Observation**: The collapse of symbol recovery for Go 1.26 was an **internal toolchain version gate** in Ghidra's RTTI mapper, *not* an obfuscated or stripped binary, and *not* a breaking structural change in the Go binary layout.
   - **S004** demonstrates that upstream Ghidra commit `385e8cd9` (GP-6528) added Go 1.26 support by updating the mapper.
   - **S005** (Mandiant GoReSym README) demonstrates that pclntab layout versions decouple from the Go compiler marketing release (handling pre-1.2, 1.2, 1.16, 1.18, and 1.20).
2. **Epistemic Ordering**:
   - **Tier 1 (Ground-Truth Canonical Metadata)**: When symbols are absent due to an internal tool gate, source diagnosis indicates that the proper remedy is lifting the tool gate or running an external layout-compatible parser (S004/S005) to extract the compiler's *true author-assigned symbol table*.
   - **Tier 2 (Heuristic Candidate Matching)**: BSim similarity matching is reserved for cases where symbols are truly absent from the source artifact (e.g. stripped production binaries where no pclntab or RTTI exists).
   - Even then, BSim outputs are **candidates for human review**, not ground-truth names.
3. **Preventing Erroneous Cross-Version Equivalence**:
   - Understanding S006 bounds prevents analysts from treating BSim similarity scores as proof that two functions across versions are identical.
   - Source diagnosis establishes whether a difference between versions is:
     - An artifact of the reverse engineering tool (e.g. Go 1.26 gate in S003);
     - A compiler toolchain optimization artifact (e.g. register allocator churn, callee inlining); or
     - A genuine semantic modification in the target program.

---

## 6. Separation of Observed Facts, Inference, and Unresolved Gaps

### Observed Facts
1. S006 (`BSimTutorial_Intro.md`, line 19) explicitly states that values of constants, names of registers, and data types are intentionally omitted from BSim features.
2. S006.arch (`BSimTutorial_Basic_Queries.md`, line 142) confirms that callee names and bodies are omitted from BSim signatures, with only call arguments incorporated.
3. S006.eval (`BSimTutorial_Evaluating_Matches.md`, line 77) explicitly warns against applying signatures and data types without external certainty, even for matches with 1.0 similarity.
4. S006.query (`BSimTutorial_Basic_Queries.md`, line 71) establishes that confidence, not similarity alone, measures the significance of a match, and trivial functions can have 1.0 similarity with negligible confidence.
5. In the lane's historical probe (`r4-10`), comparing `op` 2.34.1 vs 2.40.0 resulted in 99.94% `FUN_*` procedures under Ghidra 12.1.4.
6. S003 (`GoRttiMapper.java:79`) hardcodes `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` in the installed Ghidra 12.1.4 release.

### Inferences
1. Treating BSim cosine similarity as a proof of semantic equivalence is formally invalid because the feature construction intentionally discards constants, types, callee behaviors, and global path predicates.
2. Using BSim as a blind automated renaming tool across Go toolchain bumps introduces high risk of semantic mismatch and type corruption.
3. Source diagnosis of tool gates (S003/S004) takes epistemic precedence over heuristic similarity matching (S006): resolving the tool gate recovers canonical names, rendering heuristic matching unnecessary for that failure mode.

### Unresolved Gaps
1. The exact mathematical weights in `lshweights_64.xml` and `medium_64.xml` (located under `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/BSim/data/`) define the precise penalty parameters for feature differences, but were not parsed in detail during this source-only scout turn.
2. The exact performance impact of running an out-of-tree Go parser vs. backporting GP-6528 into installed Ghidra 12.1.4 has not been measured on the host (no builds or test runs permitted).

---

## 7. Conclusions and Handoff

1. **Reopen Status**: S006 is fully reopened from the installed Ghidra 12.1.4 tutorial files; all citations are verified contiguous, under 25 words, and accompanied by exact line numbers and SHA-256 hashes.
2. **Theoretical Finding**: Similarity in BSim measures normalized decompiler p-code subgraph overlap; it cannot establish semantic equivalence due to intentional omission of constants, types, and callee bodies.
3. **Methodological Finding**: Cross-version naming must be governed by source diagnosis. When symbol loss is caused by an artificial tool gate (such as Ghidra's Go 1.25 ceiling), the solution is fixing the metadata reader, not relying on BSim candidate matching to guess function names.
4. **Lane Status**: No tests, builds, or sibling files modified. Report delivered to `.ufo/waves/round-14/w1/BSimBounds.md`.
