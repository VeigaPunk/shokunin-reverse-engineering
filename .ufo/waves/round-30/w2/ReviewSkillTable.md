# ReviewSkillTable — round-30 SKILL section and registry, attacked against the C2 envelopes and the instruments

Seat: KaidokuR30.ReviewSkillTable (reviewer, wave 2). Lane HEAD `3502b94c5b93d86c5d67866035fd150899456295`; `SKILL.md` clean against HEAD (blob `c9a3445f17e09d092003302468a1ccc83ff6d0b1`, file sha256 `7cbc725b8f7907e90e7bd23a639309d81f20c464bbd45c97b7f9679d3b3635b4`). Targets: `SKILL.md:966-1006`, which is `## Rust dependency metadata (\`inspect-rust-binary\`) — round 30` and `### Round-30 measurement registry`. No REA run, no C2 measure mode, and no tool touched a carrier or a shared mutant (the copy of carrier bytes I altered is in my scratch). All times are UTC.

**Verdict.** Every refusal row agrees with its committed envelope on error code and message (16 of 16), and every acceptance row agrees on its package graph (3 of 3). The selftest counts are right (5 of 5). The section **fails** the "act on it alone" test, and the registry **fails** two of its factual cells:

- One table row is broken when rendered as GitHub-flavoured Markdown (GFM).
- One gate cell contradicts the REA code.
- The registry's exit code 2 and its round-29 exit code for `prefreeze-gate` are both contradicted by live runs.

## Row table (decision table, `SKILL.md:972-993`, against `corpus/evidence/round-30/c2/envelopes/`)

Producing command: `timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewSkillTable/extract.py corpus/evidence/round-30/c2/envelopes`, exit 0, 2026-10-23T03:12:35Z. For the acceptance rows: `pkgeq.py`, exit 0, 03:14:00Z, comparing against the C1 envelope `elf-x86_64-uvx.json`, whose base is 584 packages, root 463, offset 319695, 9870 compressed bytes and 55724 inflated. All rows are observations unless marked otherwise.

| mutant | SKILL outcome / code | envelope `error.code` | where the specific text sits in the envelope | input condition vs builder (`c2-rust-refusals.py:111-168`) | gate cell vs REA 6.5.0 code | row |
|---|---|---|---|---|---|---|
| g-relocated | accepted, packages equal / ok | ok, 584 packages, root 463, offset 332016, 9870 compressed | — | `relocate(base, raw)`: 332008 + 8 pad = 332016 ✓ | ✓ | holds; packages ordered-equal to the base |
| g-recompressed | accepted, packages equal / ok | ok, 584 packages, root 463, 9797 compressed, 55724 inflated | — | `z(js(doc))` at level 9 ✓ | ✓ "any complete zlib stream" | holds; packages ordered-equal to the base |
| g-no-root | accepted, packages equal / ok | ok, 584 packages, `root_package_index` null, 0 roots | — | ✓ | ✓ `RustAuditableReader.js:308` `roots[0] ?? null` | holds as "equal to the oracle's reading of the mutant". Not equal to the base: the `root` flags differ, everything else is equal (D6) |
| r-empty | not file-backed / invalid_request | invalid_request | `details.issues[0].message` | sh_size=0 at shdr+0x20 ✓ | ✓ `GoBinaryContainer.js:80` | holds |
| r-nobits | not file-backed / invalid_request | invalid_request | issues | sh_type=8 ✓ | ✓ `GoElfImage.js:186` | holds |
| r-compressed-flag | Compressed … unsupported / unsupported_target | unsupported_target | `error.message` (`Unsupported target for inspect_rust_binary at <path>: …`), `details.reason`; no issues | flags \| 0x800 ✓ | ✓ `GoElfImage.js:187` | data holds; **the row renders broken** (D1) |
| r-two-sections | more than one dependency section / invalid_request | invalid_request | issues | `.comment` sh_name := `.dep-v0` name offset ✓ | **✗ "exactly one `.dep-v0`"** (D2) | message holds; gate cell wrong |
| r-not-zlib | not a complete zlib stream / invalid_request | invalid_request | issues | junk of len(raw) = 341886−332016 = 9,870 ✓ | ✓ | holds |
| r-trailing-bytes | not a complete zlib stream / invalid_request | invalid_request | issues | raw + `00 01 02 03`, size 341890 ✓ | ✓ only on a Node with `rejectGarbageAfterEnd`; other runtimes give a different message (D5) | holds on node v24.21.0 (host `node --version` = v24.21.0) |
| r-over-1mib | exceeds the 1 MiB compressed limit / resource_constraint | resource_constraint | `error.message`; `details.reported_limits.maximum_bytes` = 1048576 | 1,048,577 bytes ✓ | ✓ `:53-57` | holds |
| r-inflate-ratio | Inflated … exceeds the size limit / resource_constraint | resource_constraint | `error.message`; `reported_limits.maximum_bytes` = 896576 | 346025−332016 = 14,009 compressed; ×64 = 896,576 ✓ | the 64× half is exercised; the 8 MiB half was not (D6) | holds |
| r-not-utf8 | not valid UTF-8 / invalid_request | invalid_request | issues | ✓ | ✓ `:152` | holds |
| r-bad-json | JSON is invalid / invalid_request | invalid_request | issues | ✓ | ✓ `:160` | holds |
| r-nesting-33 | nesting exceeds 32 / invalid_request | invalid_request | issues | ✓ | ✓ `:284-285` | holds |
| r-format-negative | does not match the format schema / invalid_request | invalid_request | issues | ✓ | partial: the code is `int().nonnegative().max(0xffff_ffff).optional()` (`:24`) (D7) | holds |
| r-extra-field | package 0 … package schema / invalid_request | invalid_request | issues | `features: []` ✓ | partial: name, version and source must also be non-empty strings, `root` boolean, dependencies non-negative ints (`:239-262`) (D7) | holds |
| r-kind-dev | package 0 … package schema / invalid_request | invalid_request | issues | ✓ | ✓ `:251-254` | holds |
| r-two-roots | more than one root package / invalid_request | invalid_request | issues | `other`=0 since base root is 463 ✓ | ✓ `:301-302` | holds |
| r-index-outside | Dependency index 584 … / invalid_request | invalid_request | issues | n = 584 ✓ | ✓ `:303-307` | holds |

Totals: 16 of 16 refusal rows match their envelope's code and message substring, and 3 of 3 acceptance rows match. The 19 of 19 count agrees with `.ufo/waves/round-30/after/c2-rust-refusals-at-92b1dd2d.txt`, whose last line is `mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)`, `exit=0`. The g-* `evidence_id`s in the envelopes equal those in `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`. The lead sentence (`SKILL.md:968`), "for `invalid_request` refusals the message field is generic", holds on all 13 `invalid_request` envelopes (`message='Analysis input is invalid. Check the arguments and try again.'`).

My scratch rebuild of all 19 mutants (copy of the counter with `MUT_DIR` pointing to my scratch) reproduced the frozen sha256 column exactly (`diff out/mut-sha.tsv out/pred-sha.tsv` is empty; build line `mutants=19 rebuilt pin_mismatch=0`). This is an observation, 03:15:28Z.

## Registry table (`SKILL.md:996-1006`)

The five `--selftest` runs were made in parallel with `TMPDIR=<scratch>/tmp timeout 900 python3 -I -B tools/round-30/<t>.py --selftest`, 03:12:20Z–03:12:21Z:

| tool | registry says | observed last line | exit | cell |
|---|---|---|---|---|
| c1-rust-positive.py | `--selftest` 25 cases | `selftest cases=25 failures=0` | 0 | holds |
| c2-rust-refusals.py | `--selftest` 16 cases | `selftest cases=16 failures=0` | 0 | holds |
| axis-fit-gate.py | 18 cases; round 29 exit 1 | `selftest cases=18 failures=0`; `--round 29 --rev HEAD` → findings SURFACE_MISSING, UNMOVED_COMMAND_MISSING, RECEIPTS_ABSENT | 0; 1 | holds |
| prefreeze-gate.py | 20 cases; **round 29 exit 1** | `selftest cases=20 failures=0`; `--round 29` → `verdict=CLEAN` | 0; **0** | **fails** (D3) |
| settle-gate.py | 13 cases; round 29 exit 1 | `selftest cases=13 failures=0`; `--round 29` → `settle: MISSING_LEDGER .ufo/waves/round-29/settle.tsv`, `FAIL (1 findings)` | 0; 1 | holds |

The round-29 gate runs were read-only (Git objects only; writes occur only inside the selftest fixtures: `axis-fit-gate.py:316-320`, `prefreeze-gate.py:260-263`, `settle-gate.py:253-262`). They ran at 03:15:44Z with `GIT_OPTIONAL_LOCKS=0`.

The remaining registry cells:
- **Commands.** All five argument shapes match their `argparse` blocks. C1 and C2 default `--rev` to `main`, which resolves to HEAD here; the three gates default to `HEAD`.
- **Oracle row.** Holds. The oracle was checked against llvm-readobj, objdump and llvm-objcopy on 16 hash-verified, `chattr +i` carriers at 02:46Z, after the M30-2 restore (`w1/RevOracleVsReadobj.md:30-44`).
- **C2 `--build` mode.** Exists (`c2-rust-refusals.py:447-448`).

## Defects (by severity)

### D1 — high (the reader-facing table is wrong when rendered): the `sh_flags |= …` row splits into 5 cells

- **Observation.** `SKILL.md:979` reads `| sh_flags |= SHF_COMPRESSED (0x800) | …`. The `|` in `|=` is unescaped, so GFM ends the cell there. I rendered `SKILL.md:966-1007` with GitHub's cmark-gfm (`render.py`, exit 0, 03:14:35Z). The rendered cells were `ROW ['sh_flags', '= SHF_COMPRESSED (0x800)', 'refused: Compressed dependency sections are unsupported', 'unsupported_target']`.
- **Effect.** The rendered row puts the refusal text under "error code", puts `unsupported_target` under "Threshold / gate", and drops the gate text `SHF_COMPRESSED (0x800) refused`. A reader of the rendered SKILL gets the error code for the only `unsupported_target` row from the wrong column.
- **Same defect in the knowledge entry.** `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` (results table row r-compressed-flag) renders as `['r-compressed-flag', 'sh_flags', '= SHF_COMPRESSED (0x800)', 'refuse: …', 'unsupported_target', '1']`. Its `P2-match` cell is dropped and `unsupported_target` lands under "exit".
- **Fix.** Escape the pipe (`sh_flags \|= SHF_COMPRESSED`) or reword it as `sh_flags OR 0x800`.

### D2 — medium (a gate cell contradicts the code): "exactly one `.dep-v0`"

- **Inference, code-read, not run** (no REA in this seat's scope). The cell `SKILL.md:980` states the gate as "exactly one `.dep-v0`". REA 6.5.0 refuses only more than one. With zero sections, `dependencySection` returns `null` (`dist/rust/RustBinaryImage.js:45-49`), and `readRustBinaryImage` returns `auditable_metadata: null` with no error (`:17-19`). File sha256 `08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681`, installed copy at `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustBinaryImage.js`; the entry and SOURCES S090 state that this copy is byte-identical to the tarball.
- **Effect.** A reader would expect a refusal for a Rust image built without cargo-auditable. The code says it gets an ok envelope with null metadata, so a "no refusal means dependencies were found" check would pass silently.
- **Not recorded anywhere in the lane.** A search for `auditable_metadata.{0,6}null|no \.dep-v0|negative class` over the lane, excluding envelopes, found no matches.
- **Fix.** Write "at most one `.dep-v0`; none gives `ok` with `auditable_metadata: null` (code-read)".

### D3 — medium (a registry fact is stale at its own commit): `prefreeze-gate` "round 29 exit 1"

**Observation.** I ran `python3 -I -B tools/round-30/prefreeze-gate.py --root <LANE> --round 29 --rev <r>` at 03:15:44Z and again across revisions (`out/prefreeze-r29-revs.txt`):

| revision | verdict | exit |
|---|---|---|
| `d210fb8f` | FLAGGED | 1 |
| `a6e7d9ce` | FLAGGED | 1 |
| `004053d6` | CLEAN | 0 |
| `f39f4530` | CLEAN | 0 |
| `24da3459` (adds the registry) | CLEAN | 0 |
| `92b1dd2d` | CLEAN | 0 |
| HEAD `3502b94c` | `pins=12 present=12 … tools_unpinned=0 findings=0`, `verdict=CLEAN` | 0 |

**Inference.** The round-29 M29-3 disclosure committed in `004053d6` (an `instrument_supersessions` entry for `tools/round-28/c1-heldout-naming.py`) turned the gate green, as `w1/ExecPrefreezeGate.md:88` predicted. The registry cell was written after that and still says exit 1. It should read "round 29 exit 1 before the M29-3 disclosure (`a6e7d9ce`), exit 0 from `004053d6`".

### D4 — medium (registry exit-code contract is false for two pin failures): "2 pin absent/altered"

The registry says "0 target met, 1 measured not met, 2 pin absent/altered" for C1, and "0/1/2 as above" for C2. Observed, in sandbox clone `<scratch>/clone` (03:15:26Z–03:15:29Z), with no REA started (`pgrep` empty afterwards):

- **(a) Altered base carrier, C2 exits 1, not 2.** `python3 -I -B c2-scratch.py --build --root <scratch>/clone`, where `c2-scratch.py` is the lane counter with only `MUT_DIR` repointed to my scratch. In the clone, the `carriers.tsv` row for `elf-x86_64-uvx` points to a copy with one byte flipped (sha256 `4558b17b…8393`). Output `PIN base carrier altered`, `exit=1`. The cause is `raise SystemExit("PIN base carrier altered")` (`c2-rust-refusals.py:285`), which exits 1. The same path runs in measure mode (`measure` → `do_build`, `:321`).
- **(b) REA `package.json` absent, both counters exit 1.** With `HOME=/nonexistent`, both counters died with `FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json'`, `exit=1`:
  - C2 scratch copy, measure mode `--rev HEAD`, at `:329`;
  - C1 lane counter `--root <clone> --rev HEAD`, at `:224` → `:59`.
- **(c) An altered `package.json` is not a pin failure. Inference, code-read.** Both counters compare only `version == "6.5.0"` (`c1-rust-positive.py:224-228`, `c2-rust-refusals.py:329-333`). The sha256 is recorded in runs.tsv but never checked against `claims.json` `rea_pin/package_json_sha256` (`a5003023…6c`). A modified 6.5.0 install does not give exit 2.

**Effect.** Exit 1 is documented as "measured, not met", so a reader cannot tell a broken pin from a real miss by exit code. The registry cell should say "2 for the C1 carrier list and carrier hashes and the C2 mutant and prediction pins; a changed C2 base carrier or a missing REA install exits 1 with `PIN …` or a traceback; package bytes are not pinned".

### D5 — low-medium (cannot act on it alone): the registry drops the write scope and host prerequisites that rounds 22–29 registries carried

Rounds 22–29 use `| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |`. Round 30 uses `| tool | purpose | command | exit codes | selftest |`, with no sha256 pins and no write scope. The following are observations from code:

- **C2 measure mode writes outside the lane on every run.** It rewrites all 19 files in `/fast/scratch/hyaku/kaidoku-r30/mutants/` (`chmod 0644`, write, `chmod 0444`; `c2-rust-refusals.py:299-304`, `MUT_DIR` `:47`). The only warning in the registry is "(one at a time)", and the reason for it is in the entry's `recheck:` line, not in SKILL.
- **`--write-evidence` overwrites lane files in both counters.** C1 writes envelopes and `runs.tsv` (`c1-rust-positive.py:254-262`); C2 does the same (`:370-377`).
- **Host-specific inputs are hard-coded.** `PKG_JSON` is `~/.npm/_npx/ad9a3fdbcad992c6/…` (C1 `:41`, C2 `:44`); `MUT_DIR` is a fixed `/fast/scratch` path; the carriers live outside the lane at the `carriers.tsv` paths.

On another host, or after an npx cache rehash, both counters die with a traceback (see D4(b)). The pins exist in `claims.json` (instruments: c1 `e07563d6…`, c2 `1c357fca…`, oracle `f0b144c6…`; these equal the current files' sha256) but are not cited in the registry.

The runtime limit is also missing from SKILL. The trailing-bytes row depends on `rejectGarbageAfterEnd`. On a Node without it, the code gives a different message, "Dependency section has bytes after the zlib stream" (`RustAuditableReader.js:82-87`). This is code-read. The SKILL Limits paragraph does not list "one host runtime (node v24.21.0)", although the entry's Limits does.

### D6 — low: limits and evidence labelling inside the table

- **The 8 MiB inflate cap is not flagged as code-read.** The `r-inflate-ratio` gate cell presents `min(8 MiB, 64 × section bytes)` as observed. Only the 64× branch fired (`reported_limits.maximum_bytes` = 896576; the inflated JSON is about 3.05 MiB, below 8 MiB). The absolute cap `RUST_UNCOMPRESSED_BYTES` (`:11`) was not exercised. The Limits sentence (`SKILL.md:995`) lists only "the 256 MiB input cap and 8 MiB report budget" as code-read, and so does the entry.
- **"Packages equal" has no stated reference.** For g-no-root the packages are not equal to the base carrier's; they are equal to the oracle's reading of the mutant (D6 observation in the row table). Name the comparison: "equal to an independent decode of the mutant".
- **Messages appear only as substrings.** Envelope texts are prefixed `Selected artifact <path>: ` (issues and resource) or `Unsupported target for inspect_rust_binary at <path>: `. The table does not say that it gives substrings, which matters for an exact-match consumer. It also does not say where the specific text lives for the two non-`invalid_request` codes (`error.message` / `details.reason`), or that the CLI exits 1 on every refusal and 0 on acceptance (runs.tsv).
- **Shared messages are not caveated.** The pairs r-empty/r-nobits, r-not-zlib/r-trailing-bytes and r-extra-field/r-kind-dev share a message, so a match does not show which branch fired. The entry's Limits says this; SKILL does not. SKILL also omits the gate order (container, then size, inflate, UTF-8, depth, parse, format, packages, roots and index), so a reader cannot predict which message a multi-defect input yields.

### D7 — low: partial gate cells

- `format`: the code requires a non-negative integer ≤ 0xFFFFFFFF, optional (`RustAuditableReader.js:24`); the cell omits the bound and the optionality.
- Package schema: also needs non-empty `name`/`version`/`source` strings, a boolean `root` and integer dependency indices ≥ 0 (`:239-262`).
- The report-budget refusal "Dependency graph exceeds the complete report byte budget before expansion" (`resource_constraint`, `:200-204`) is absent from the table. It is code-read only, which the Limits sentence partly covers.

### Outside the target (noted, not scored)

The `code_pointer` line numbers in `predictions.tsv` are off for several rows. For example, r-two-roots cites `:151-153` against the actual `:301-302`, and r-inflate-ratio cites `:73,128-129` against `:79,138-139`. The entry already discloses this.

## Residual risk and verification gaps

- **Unknown:** D2's zero-section behaviour was not run live; REA is outside this seat's item. A one-call check on an ELF with `.dep-v0` stripped, by a seat allowed to run REA, would settle it.
- I did not re-run REA on any mutant, so the row table compares SKILL with committed envelopes plus the `92b1dd2d` after receipt, not with a fresh live run (that is seat ReRunC2's job).
- GFM rendering was checked with cmark-gfm only. Other Markdown renderers were not tried.
- The working tree has uncommitted changes to `corpus/SOURCES.md` and `corpus/lessons/round-30.md` (observed via `git status --porcelain`; not mine). SKILL.md itself is clean against HEAD.

## Tool installs

- `cmarkgfm` 2025.10.22 (Python bindings for GitHub's cmark-gfm), installed with `uv venv` + `uv pip install` into `<scratch>/venv`. Reason: render the SKILL table with a GFM parser (D1). Nothing was installed host-wide.

## Scratch artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewSkillTable/`)

| file | sha256 |
|---|---|
| extract.py | 36fa7b7aeae8505380b2767acea49348dcb0664b45ee9f906d93f4a3df87ef35 |
| pkgeq.py | cf1a59894f217d0c51aebb1ac208fa6c7dcdd7833d1e73d3892482d48e1d7d0a |
| render.py | 15fd58adefd1a65c7f453cb4d116fa6c3b282d69bc6189275cd98ca9a4c85a51 |
| c2-scratch.py (lane C2 counter with `MUT_DIR` changed only) | 470dce1933801ca2b762988f509b85e25a8e700deafd2028a067800698742fe1 |
| rust_dep_oracle.py (copy) | f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d |
| altered/elf-x86_64-uvx (1 byte flipped at offset 100) | 4558b17b449f3ba879ce6b68089ff1d64ff248bd28caf60092d6c0fe598c8393 |
| out/extract.txt | dcf7853d1943403ac4bcb403b5f21302d9a6798b768b1c7f24baaa715a7c17c7 |
| out/pkgeq.txt | 5b0a6dbacc09e40c20f151c058e3fcf5038fb810c862ed2b9dfb5edf121aa59a |
| out/render-skill.txt | 14a78a9d0f5885fde5496bdaa63a85436b27f4d78537513943a2bccee9bc3482 |
| out/render-entry.txt | 4524efb3d108b7fc0f46b1516bed59d2e52bbfaf64182c87de249a4c58f977eb |
| out/skill-section.md (`SKILL.md:966-1007`) | 9512fd9e2051454ad8a310253ae437167ecda7b8d67dd1d0b2d4e259a522493f |
| out/A.txt (altered base → exit 1) | 9394b26d88e8a8d2fcd9cda5e1ffbfd509edecd729210ed6226fccc788550380 |
| out/B.txt (C2 copy, no package.json → exit 1) | 7f3dc4032d30fdbc3195142670f4961c42b9b311c3587c9ac049525c50a83087 |
| out/C.txt (C1, no package.json → exit 1) | 2cd265164ebcb1e3ebdb9405fd08eca2d6c3b3118326429cf74ffb33dbe4898e |
| out/mut-sha.tsv = out/pred-sha.tsv | e97289fbc0d5ee17dffd6278d0f843f9f58cc6ec0ed1e2379451295cb8bc0b4b |
| out/c1-rust-positive.selftest.txt | 0d22a019b1cbc1d056df1bfa90a8776e524888a965cfaa963631bb3b9dffca95 |
| out/c2-rust-refusals.selftest.txt | 8a1336ef1cecbd96cdb354f48f0088c306aacebef0d447eafb6e40530b30b11c |
| out/axis-fit-gate.selftest.txt | 5fe7931ba4474b2869c798a9edc5696297c21d3b961f602c30ace8963dfceedc |
| out/prefreeze-gate.selftest.txt | 50ec7061b0635a0d913493b03e01ad5a828bb79283390f42cd7c3010daa67777 |
| out/settle-gate.selftest.txt | e7132a3fa307e41d0066414c1589f54450a572b7ba67d21a6ae8c98b2394609d |
| out/axis-fit-gate-r29.txt | c49dac21fa6af8d3ceb328dc7a9fea230d5cbb703c72fede32158935e1b02d23 |
| out/prefreeze-gate-r29.txt | 178c01656b14639cdc828759290d465e1ab9e138bd2484cb3f819ec8befa3a07 |
| out/prefreeze-r29-revs.txt | 38eae859760c155c31f119e3bddb26f9f0a1b27f452e53756df8cfa40ac01741 |
| out/settle-gate-r29.txt | 24c6cef1cff0e5af6d8cb2646e8e325c83d15c34c33cc34fd69df6f42e0bf2c7 |

Also in scratch: `mut/` (19 scratch-built mutants, sha256 equal to `predictions.tsv`), `clone/` (sandbox clone at `3502b94c`; its `carriers.tsv` was restored with `git checkout` inside the clone), `venv/`, and `tmp/`.
