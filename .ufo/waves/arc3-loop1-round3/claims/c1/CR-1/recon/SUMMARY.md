# CR-1 — arc3-loop1-round3 critic (chain c1): measurements and verdicts

Seat CR-1 · chain c1 · role critic · 2026-10-19. Scratch: `/var/tmp/cr1-round3/`.
All numbers below are re-derivable with the scripts in this directory (re-run recipes at the end).
No git mutations; custody paths untouched; corpus/SKILL/README not written.

## 1. Own adversarial carrier set (compiled on-host, pinned solc 0.8.37 prefix)

`src/` (sources) + `out/` (runtime hex / ABI / meta). Optimizer legs `--optimize --optimize-runs 200`
via standard-JSON (`compile.js`).

| carrier | shape under attack | K (ABI functions) | opt200 probe | noopt probe | hex==raw payload |
|---|---|---|---|---|---|
| Cr1OptToken (O1) | ERC-20 + error/event ABI entries + `receive()` | 11 | 11/11, 0 extra | 11/11 | true |
| Cr1Vault (O2) | non-ERC-20: payable receive+fallback, mixed mutability | 9 | 9/9, 0 extra | 9/9 | true |
| Cr1Dedup (O3) | identical bodies + overloads + error/event mix | 8 | 8/8, 0 extra | 8/8 | true |
| Cr1Lib (O4) | library runtime (unlinked `PUSH20 0…` prologue) | 3 | 3/3, 0 extra | 3/3 | true |
| Cr1Big (O5) | 25 functions (binary-search dispatch pressure) | 25 | 25/25, 0 extra | — | true |

Carrier identity (runtime bytes sha256, first 12): O1 `bc29d9538e04`, O2 `a07088b382fd`,
O3 `e1b16d200f6b`, O4 `6d0d46e8a53c`, O5 `34d04d6873e6`. Probe envelopes: `probe/`.

## 2. Attack 1 — optimizer drops/transforms the dispatch table (shrunken K? inlined selectors?)

**Verdict: refuted for the probe path at every measured size; the hazard lands on the
reconciliation layer instead.**

- Byte-level census (EQ;PUSH2;JUMPI sites, metadata excluded) == planted function set on
  every runtime leg measured: my 5 carriers × opt/noopt, plus 6 landed c1 carriers
  (EX-03 carrierA 9, EX-04 carrierB 11, EX-05 CarrierB 8, EX-07 Rv2TokenOpt 5,
  EX-10 VaultB 13/13, EX-12 VaultA 7) and the landed 22-function carriers (2 groups).
  Zero planted-but-absent, zero dispatch-entry extras. See `recon/audit-c1.txt`,
  `recon/abi-vs-dispatch.txt`.
- **Dispatch shape does transform with table size** — one GT bound/split node appears at
  K=7 and the count grows: K≤6 → 0 GT; K=7–11 → 1 GT; K=13 → 2 GT; K=22 → 3 GT; K=25 → 4 GT
  (measured across 59 decoded digests + my carriers; my own identical-bodies carrier O3 shows the
  optimizer's body-merge as shared dispatch targets — `dest 176 <- b44030ab/bc9748a1/5c36b186` —
  the only such flag in the tree, and on the critic's own carrier). The split selector therefore appears
  **twice** as a PUSH4 (GT node + EQ node). Consequence: a reconciliation that counts PUSH4
  immediates as K over-counts (12 legs for 11 selectors, 14 for 13, 30 for 25).
- Optimizer **merges identical bodies** (measured on O3: three selectors share one dispatch
  target 176) but keeps one EQ leg per selector; the probe reports all.
- Unplanted-but-present constants in the code region are real in optimizer legs: custom-error
  selectors (`db42144d`×2, `30cd7471`×2), `Panic(uint256)` `4e487b71`, and unidentified
  constants (`3c3332b9`, `6508d58f`, `1182d3d5`, `245aecd3`, `7a65726f`). The probe never
  reported any of them (extras=[] on every leg) — the extractor distinguishes dispatch PUSH4
  from ABI-encoder PUSH4. Do not reuse a raw PUSH4 census as "the dispatch table".
- Metadata defect (inherited recipe): the CBOR tail is swept as code by the r1 scanner
  (`recon/r1-claim-refutations.txt`). r1's cited "sole non-dispatch PUSH4 constant
  `16ee4b79@1900`" is a metadata byte-chunk (codeEnd=1890 for Rv2Token.runtime.hex; the code
  region has **zero** non-dispatch PUSH4 constants — a stronger, cleaner statement). Round-3
  carriers carry the same class of phantom: `43000825@codeEnd+46` (the `solc`+version CBOR
  bytes read as a PUSH4) in 3 of 5 carriers; EX-07's round-3 reconciliation code has no
  metadata exclusion (`grep -iE 'metadata|cbor' compare-carrierA.py analyze.py` → no hits).
  Latent risk, not observed: a metadata byte-window could collide with a planted selector and
  be counted as "present" (0 observed collisions in 59 decoded digests).

## 3. Attack 2 — planted-from-ABI vs actual dispatch entries (unreachable functions)

**Verdict: no mismatch found; latent false-plant classes identified.**

- ABI (`type=="function"`) → dispatch site set: exact match on all 12 carriers checked
  (`recon/abi-vs-dispatch.txt`). No ABI function is missing from the dispatch; no dispatch
  selector is absent from the ABI. `receive`/`fallback`/`constructor` have no dispatch entry
  and were correctly excluded from every landed planted set.
- Naive planted-from-ABI hazards (not realised in the landed artifacts): error entries are
  real 4-byte hashes but never dispatch entries; event entries' 4-byte prefixes are not
  selectors at all. Landed planted sets (EX-03/EX-05/EX-07 + methodIdentifiers cross-check)
  filter correctly.
- **New refutation of an inherited claim**: r1's "Creation blobs carry no runtime dispatch
  table" is false — `Rv2Token.creation.hex` embeds the runtime and its 5 EQ;PUSH2;JUMPI sites;
  round-3 creation legs embed 7/9/10/11/13 EQ sites. The probe returns 0 functions on them
  (parsed-and-empty) — tool scope, not byte absence. Wording in the r3 entry must not repeat
  the r1 claim.
- Also measured (EX-12 control, expectation delta): a 0-byte file is accepted as
  parsed-and-empty (n=0, decoded sha256 `e3b0c442…`), not the pre-registered
  `invalid_request` refusal — EX-12's `expectations-additional.txt` (i) expects the refusal;
  the seat must adjudicate the delta.

## 4. Attack 3 — costume retry on partial recovery

**Verdict: not observed; detection tool shipped.**

- 233 probe envelopes across the c1 tree (final re-run; 143 at the first run) were grouped by
  decoded bytecode sha256 (`recon/audit-c1.txt`). Within every group, all envelopes report identical function sets
  and counts; no partial→full transition; the only set-changing leg is the deliberately
  tampered VaultCourt selector (`d0e30db1`), where the probe followed the bytes (10/10
  including the tampered selector) — byte-truth, no laundering.
- Costume invariance measured: hex vs raw, 6.4.0/6.5.0/6.7.0, rerun, renamed file, alternate
  CWD all keep `.normalized_result.bytecode.sha256` fixed while `.subject.digest.sha256`
  (the *input file* digest) changes — e.g. EX-07 Rv2TokenOpt: subject `a07bef2e7980…` =
  sha256(hex text + `\n`), decoded `ed6c8a76d05b…` = sha256(runtime bytes). The r1 entry's
  recheck line advises comparing `subject.digest.sha256`; that advice is costume-dependent and
  wrong for hex carriers (it is only correct in the raw costume). Use the decoded digest.
- Detector: `audit-seat.js <dir>` flags `PARTIAL->FULL TRANSITION` and per-digest reconcile
  diffs; re-run it over the c1 tree at landing.

## 5. Chain acceptance state re-derived by this seat

- command A (recipe `.ufo/waves/arc3-loop1-round2/claims/c1/PL-1/command-a-recipe.py`,
  read-only `git show`): at `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` **and** at HEAD
  (= `c07af80`): `knowledge_files 82, mapped 82, missing [], dangling [], rules 14/14,
  10.0/10.0` (`recon/command-A.txt`) — matches every seat's recorded before-state.
- Nothing in this seat writes the C1 real target; the 82→83 flip and the corpus entry are
  the parent's landing step.

## 6. Re-run recipes

```bash
cd /var/tmp/cr1-round3
node compile.js src/O1.sol out opt200          # 2 modes for O1..O4
node planted.js out/<C>.<tag>.abi.json         # filtered vs naive planted sets
node census2.js out/<C>.<tag>.runtime.hex      # metadata-aware PUSH4/EQ/GT census
node abi-vs-dispatch.js <abi.json> <runtime.hex> <label>
node audit-seat.js <claims tree>               # envelope grouping + costume/partial detector
node legcmp.js                                 # per-decoded-digest costume agreement
PROBE: TMPDIR=/var/tmp/cr1-round3/tmp npx -y rea-agents@6.4.0 inspect-evm-interface \
        <file.runtime.hex> hex --format json   # raw leg: <file.runtime.bin> raw
```