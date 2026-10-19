# CR-1 — chain c1, critic (arc3-loop1-round3)

Seat line: attacks — (1) optimizer drop/transform of the dispatch table (shrunken
K? inlined selectors?; unplanted-but-present / planted-but-absent in the
reconciliations), (2) planted-from-ABI vs actual dispatch mismatch (unreachable
functions), (3) costume retry on partial recovery. Verdicts below.

Repo HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (unchanged through this
seat's work; re-checked with `git rev-parse HEAD`). No git mutations; custody
paths untouched (read-only evidence only); corpus/SKILL/README not written.
Scratch: `/var/tmp/cr1-round3/` (disk-backed; `/tmp` never used). Tools: pinned
wave-1 solc prefix (receipt re-verified first: npm-cache tarball sha256
`0e1a1ab6…575a51` = `EX-02/install-receipt.txt` §1; `solcjs --version` →
`0.8.37+commit.f401782d`), probe `npx -y rea-agents@6.4.0` with
`TMPDIR=/var/tmp/cr1-round3/tmp`.

Artifact set (my write scope): `claims/c1/CR-1/` — 68 files,
`MANIFEST.sha256` sha256 `0b104b7a578d50e4de9de4d9a713c1dee3d0bbe1ad45fbe803e2ff70e7942459`,
`sha256sum -c` → 68/68 OK, manifest generated last over the frozen set.

## 1. Work performed (evidence pointers)

**Own adversarial carriers** (`claims/c1/CR-1/src/`, `out/`, `probe/`): five
shapes compiled on-host with the receipted solc, opt200 (`--optimize
--optimize-runs 200`) + noopt controls (`src/compile.js`, standard-JSON):
`Cr1OptToken` (ERC-20 + error/event ABI entries + `receive()`, K=11, opt
`bc29d953…`), `Cr1Vault` (non-ERC-20: payable receive+fallback, mixed
mutability, K=9, `a07088b3…`), `Cr1Dedup` (identical bodies + overloads, K=8,
`e1b16d20…`), `Cr1Lib` (library runtime, unlinked `PUSH20 0…` prologue, K=3,
`6d0d46e8…`) and `Cr1Big` (25 external functions, K=25, `34d04d68…`). 13 probe
envelopes in `probe/` (hex+raw per pin where run).

**Instrumentation built for the attacks** (`claims/c1/CR-1/src/`):
`census2.js` (metadata-aware PUSH4/EQ/GT census; CBOR codeEnd via last-2-bytes
length + `0xa2` check), `abi-vs-dispatch.js` (attack 2 checker),
`audit-seat.js` (tree-wide envelope grouping by *decoded* digest,
partial→full detector, per-digest probe-vs-dispatch reconcile), `legcmp.js`
(costume agreement), `meta-count.js`, `meta-check.js`, `forensic.js`,
`planted.js`, `sweep.py`.

**Audit of the landed chain**: `recon/audit-c1.txt` (final run: 233 envelopes /
59 decoded-digest groups over the whole c1 tree, each group re-censused from the
envelope's own echoed bytecode), `recon/abi-vs-dispatch.txt` (9 carriers),
`recon/meta-count.txt`, `recon/legcmp.txt`, `recon/census.json`,
`recon/census.txt`, `recon/forensic.txt`, `recon/command-A.txt`,
`recon/r1-claim-refutations.txt`, `recon/SUMMARY.md`.

**Read (not written)**: all c1 seat evidence; `EX-07` round-3 reconciliation
code + compare files; `SC-2`'s entry draft rev 2 and map-token patch;
`CR-2/attack-notes.md` (sibling critic — my angles are complementary; no
duplication: CR-2 owns shape-class generalization and entry-wording A1b/A2/A3,
I own the metadata/CBOR defect, the creation-blob refutation, the identity
domain, and the costume/partial detector).

## 2. Proposed changes

`claims/c1/CR-1/proposed-entry-corrections.patch.md` — three verbatim edits to
`claims/c1/records-drafts/knowledge-entry-draft.md` rev 2 (draft unchanged by
this seat):

1. line ~45 id-domain comparator: replace "compare by `subject.digest.sha256` +
   payload" with the decoded `normalized_result.bytecode.sha256` comparator
   (measured: `subject` = input-file digest; hex leg `a07bef2e…` vs decoded
   `ed6c8a76…` for Rv2TokenOpt).
2. line ~41: state that `43000825` is read out of the terminal CBOR trailer
   (code region ends at byte 925, 6 immediates = 5 selectors + panic).
3. line ~68-70: "no erratum is needed" → append-only correction sentence for
   r1's two measured-false statements (creation blobs; the `16ee4b79`
   "sole non-dispatch PUSH4 constant").

Nothing else in the draft conflicts with my independent census (its CBOR note
`cborLength 51 … bytecodeOffset 1568` equals my computed codeEnd for VaultB
opt200; its GT/EQ shape observation matches my pivot counts).

## 3. Before → after measurement (chain's claim)

- **Before-state re-derived first-hand** (`recon/command-A.txt`, recipe
  `.ufo/waves/arc3-loop1-round2/claims/c1/PL-1/command-a-recipe.py`,
  read-only `git show`): at `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` **and**
  at HEAD → `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling":
  [], "citation_resolved_rules": 14, "rule_blocks": 14, "coverage_score": 10.0,
  "depth_score": 10.0}` — identical to every seat's recorded before-state.
- **Claim substance re-measured at byte level** (the K/K half): planted-function
  set == EQ;PUSH2;JUMPI dispatch set on every landed runtime carrier
  (VaultB 13/13 opt+nopt, carrierB@EX-04 11/11 ×2 legs, CarrierB 8/8,
  CarrierBErr 8/8, Rv2TokenOpt 5/5, carrierA 9/9, VaultA 7/7, 22-selector
  carriers ×2, carrier-A 3/3) and on my five carriers (11, 9, 8, 3, 25) at both
  optimizer settings — `missing=[]`, `extra=[]` everywhere (probe extras vs
  dispatch = none; see §4 attack 1 for the PUSH4-census caveat).
- **Optimizer effect measured**: same recovered set, runtime bytes change
  (my O1 3863→2027 B, O2 2428→1145 B, O3 910→409 B; chain carriers
  3872→1850, 3163→1621, 1943→978).
- **Not measurable by this seat (parent's landing step)**: the 82→83 flip, the
  token/entry landing, and their coupling — the entry draft existed only as
  rev 2 at my write time; command A after-state is 82 until the parent lands.

## 4. Attacks / refutations attempted, with verdicts

**Attack 1 — optimizer drops/transforms the dispatch table; unplanted-but-present
/ planted-but-absent.**
Verdict: **refuted for the probe path; hazard relocated to the reconciliation
layer.**
- No shrunken K, no inlined/dropped selector: dispatch EQ set == planted set at
  K = 3, 5, 8, 9, 10, 11, 13, 22, 25 (opt200 + noopt), solc 0.8.37, default
  evmVersion.
- Dispatch *shape* transforms monotonically with size (measured on 59 decoded
  digests + my carriers): GT split nodes — K≤6: 0; K=7–11: 1; K=13: 2; K=22: 3;
  K=25: 4, so the pivot selector is a PUSH4 **twice** (GT node + EQ leaf). A
  reconciliation that counts PUSH4 immediates as K over-counts (12 legs/11,
  14/13, 30/25, 2× for the pivot). Optimizer also merges identical bodies
  (my O3: 3 selectors → shared target 176, the only such flag in the tree) while
  keeping one EQ leg each — the probe reports all.
- Unplanted-but-present is real in optimized code: custom-error selectors
  (`db42144d`×2, `30cd7471`×2), `4e487b71` (panic), unidentified constants
  (`3c3332b9`, `6508d58f`, `1182d3d5`, `245aecd3`, `7a65726f`). The probe
  reported none of them on any leg — zero false positives extended to
  optimizer-enabled carriers.
- **Recipe defect found (inherited)**: whole-file sweeps read the CBOR trailer
  as code. r1's cited "sole non-dispatch PUSH4 constant (`16ee4b79` @1900)" is a
  metadata artifact — `Rv2Token.runtime.hex` code region ends at byte 1890 and
  holds **zero** non-dispatch immediates; the constant sits at byte 1901. The
  r1 extractor's own `push4_all` includes `[1900, "16ee4b79"]` with
  `code_len: 1943`. Round-3 carriers carry the same phantom `43000825@
  codeEnd+46` (3 of 5 round-3 runtimes checked), and EX-07's round-3
  reconciliation code has no metadata exclusion (`grep -iE 'metadata|cbor'`
  → no hits). Latent risk, not observed: a metadata window colliding with a
  planted selector (0 collisions in 59 digests).

**Attack 2 — planted-from-ABI vs actual dispatch (unreachable functions).**
Verdict: **no mismatch found; two false-plant classes and one false r1 claim
identified.**
- 9 carriers cross-checked (`recon/abi-vs-dispatch.txt`): every
  `type=="function"` ABI selector has a dispatch site; no dispatch selector is
  absent from the ABI. `receive`/`fallback`/`constructor` correctly excluded
  from every landed planted set; `receive()` (EX-04, EX-05, my O1/O2) changes
  the empty-calldata branch, not the selector set.
- Naive planted-from-ABI would add 2-7 phantom "selectors" per carrier (error
  entries are real hashes but never dispatch entries; event entries' 4-byte
  prefixes are not selectors). No landed artifact made this error.
- **r1 claim refuted**: "Creation blobs carry no runtime dispatch table"
  (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`, creation-code
  observation) — `Rv2Token.creation.hex` (1,971 B) embeds the runtime and its 5
  EQ sites; round-3 creation legs embed 7/9/10/11/13 EQ sites. The probe's
  0-function result is tool scope (parsed-and-empty), not byte absence.
  Patch text §2 edit 3.
- EX-12's empty-file control: their pre-registered expectation (typed refusal)
  is falsified by their own measurement (parsed-and-empty, n=0, decoded
  `e3b0c442…`); EX-12 already recorded it as FALSIFIED in `seats/EX-12.md:99` —
  credited, no gap.

**Attack 3 — costume retry on partial recovery.**
Verdict: **not observed in 233 envelopes / 59 digests; detector shipped.**
- Within every decoded-digest group all envelopes have identical function sets
  and counts — no partial→full transition anywhere in the c1 tree. The only
  set-changing leg is the deliberate tamper (VaultCourt `d0e30db1`), where the
  probe followed the bytes (10/10 incl. the tampered selector) — byte-truth
  ahead of planted-truth, no laundering.
- Costume invariance measured: hex vs raw, 6.4.0/6.5.0/6.7.0, rerun, renamed
  file, alternate CWD keep `.normalized_result.bytecode.sha256` fixed while
  `.subject.digest.sha256` changes (input-file digest; `a07bef2e…` =
  sha256(hex text incl. trailing `\n`) vs `ed6c8a76…` = bytes). Re-run
  detector: `audit-seat.js <tree>` (prints per-digest reconcile and flags
  PARTIAL→FULL).
- Self-refutation recorded: my first EQ-site detector required `PUSH2`
  destinations and missed carrier-A's `PUSH1`-dest stub (84 B, 3 selectors) —
  patched to accept `PUSH1..PUSH3` before the final run; the only nonzero-extras
  line in the final audit is my own O3 carrier's dedup flag.

## 5. Blockers

None. Named residuals for the parent:
1. The three draft edits (§2) are unapplied; the draft was rev 2 at 13:15Z and
   its own identity line still says "final — after last write".
2. Round-3 reconciliation code has no CBOR-metadata exclusion (latent class,
   §4 attack 1); my `census2.js`/`audit-seat.js` implement it if the parent
   wants the recipe fixed at landing.
3. Landed planted-set ordering rests on scratch mtimes for some seats (EX-04
   §5.1 names it); the *sets* are compiler/ABI-derivable and oracle-matched
   (EX-07's v1/v2 hash-primitive bugs corrected pre-report; set unchanged,
   `oracle_set_match: true` against r1's pre-existing expected-selectors).
4. `via-ir`, other `--optimize-runs` values, other solc versions, and sizes
   above the ~3.9 KB class remain unmeasured (my K=25 leg is 1.7 KB runtime;
   the chain's largest is 3.9 KB) — r1's Unknowns survive r3.