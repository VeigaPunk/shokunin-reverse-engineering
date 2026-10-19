# PL-1 — chain c1, planner (arc3-loop1-round3)

Seat line: plan C1 (EVM optimizer-leg) — carrier designs (A: optimizer-enabled
`--optimize --optimize-runs 200` with a payable/receive path; B: non-ERC-20 shape with
mixed mutability), planted-selector methodology, prologue-class expectations vs the r1
recorded classes, honest-stop branches. Artifact: `claims/c1/PL-1/plan.md`.
Repo HEAD at work: `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`. Date: 2026-10-19.
Scratch under `/var/tmp/pl1-r3` (never `/tmp`); no git mutations; no corpus/LOG/
SCORECARD/SHONEN/README/SKILL writes; custody paths never touched.

## 1. Work performed (evidence pointers)

- Context read: frozen claims; `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
  (Unknowns + recheck line); SCORECARD command-A recipe (git-`show`-based census);
  r1 c1 artifacts (Rv2Token/KdxToken compile idioms, planted-K.json shape,
  EX-07 selector-recon.py); QUALITY.md; SKILL.md queue-drain rules.
- Baseline command A at HEAD (exact SCORECARD stanza, read-only):
  `knowledge_files 82, mapped 82, missing [], dangling [], citation_resolved_rules 14,
  rule_blocks 14, coverage 10.0, depth 10.0` → `evidence/commandA-head.json`.
- Solc receipt re-verification (no install): npm-cache content sha256
  `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51` (6,476,046 B) =
  r1 receipt; `solcjs --version` and `require('solc').version()` both
  `0.8.37+commit.f401782d.Emscripten.clang` → `evidence/receipt-recheck.txt`.
- Three prototype carriers compiled on scratch with the receipted prefix:
  A `OptVault` (optimizer on, runs 200, payable receive+fallback, mixed mutability;
  runtime 776 B `544469b7…`), B `MutMix` (optimizer off, non-ERC-20, library-bound,
  four mutability classes; runtime 1061 B `6267ef53…`), B′ `MutMix`-opt (497 B
  `200bc9db…`) → `evidence/compile-summary.json`, sources staged verbatim.
- Planted sets derived **pre-probe** with two keccak oracles (r1 pure-Python scanner +
  js-sha3) and a probe-independent linear-sweep extractor → `evidence/scan-*.txt`,
  `keccak-js-sha3.txt`, `extract-*.txt`; signature-list mtimes 10:07:38 precede the
  first probe envelope 10:07:39 (`stat` receipt in report run, §3 commands below).
- Seven probe envelopes, all exit 0, stderr empty: 6.4.0 hex+raw for A/B/B′, 6.7.0 hex
  for A/B → `evidence/{OptVault,MutMix,MutMixOpt}-*.json` (ids quoted in plan §3).
- After-recipe validation: worktree-overlay command A with the planned entry filename
  and a stub entry → `83/83, missing [], dangling [], 14/14, coverage 10.0, depth 10.0`,
  README 190 lines → `evidence/overlay-commandA.json`.
- Compile-mechanics measurement: source-key metadata drift + CLI-form equivalence →
  `evidence/cli-json-equivalence.txt`.
- Mid-round cross-check of seat EX-04 (c1 executor, landed during planning): its
  optimizer-enabled `VaultB` leg (K=11) shows a binary-search dispatch layout with the
  same prologue class; folded into plan §4 as a measured layout-variance note with
  citation (`seats/EX-04.md` §Work performed).

## 2. Proposed changes (patch-text pointers)

- None written by this seat (planner; write scope is the report + plan).
- Specified for the chain (plan §6, to be realized by executors/critics as `*.patch.md`):
  entry path `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` and the exact
  line-neutral README EVM-row before/after token text (`plan.md` §6.2), plus the entry
  skeleton mapped to QUALITY.md rows (`plan.md` §6.1).

## 3. Before→after measurement for the chain's claim (commands + outputs)

- **Before** — command A at `c07af80f` (SCORECARD stanza verbatim, `REV` passed as argv):
  `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 82, "missing": [], "mapped": 82,
  "rule_blocks": 14, ...}` (`evidence/commandA-head.json`). The claim's prior-82 baseline
  is real and green at HEAD.
- **After (mechanics validated; authoritative re-measure stays at the work commit)** —
  overlay worktree-mode census (same logic, reading the overlay): stub entry + token →
  `{"knowledge_files": 83, "mapped": 83, "missing": [], "dangling": [],
  "citation_resolved_rules": 14, "coverage_score": 10.0, "depth_score": 10.0}`
  (`evidence/overlay-commandA.json`); README stayed 190 lines (`wc -l`).
- **K/K pre-measurement** — planted vs probe, zero extras, both legs, decoded bytecode
  sha256 = pinned runtime sha256: OptVault 5/5 (`ev_13a039e7…` hex / `ev_64149aa1…` raw;
  6.7.0 `ev_faa9e12e…`), MutMix 6/6 (`ev_913cb961…` / `ev_8df6ecd3…`; 6.7.0
  `ev_f8690ffc…`), MutMix-opt 6/6 (`ev_df117360…`).
- **Ordering receipt** — `stat` order: sigs 10:07:38 < first envelope 10:07:39;
  runtime hex written 10:07:29.

## 4. Attacks / refutations attempted (with verdicts)

| # | attack | verdict |
|---|---|---|
| A1 | "the optimizer changes the dispatcher prologue class" | REFUTED: `5f3560e01c` on opt-on and opt-off carriers; anchor offset 13 (vs r1's 25 — carrier-dependent); legacy `60003560e01c` = −1 everywhere (`extract-*.txt`) |
| A2 | "the literal CLI flag form and standard-JSON produce identical bytes" | PARTIALLY REFUTED: identical only when the JSON source key equals the CLI-given path (creation `b425e968…` both, measured `EQUAL=true`); key `OptVault.sol` → creation `919fdef4…` / runtime `393b2891…` drift (`cli-json-equivalence.txt`) |
| A3 | "payable receive/fallback appear as pseudo-selector entries" | REFUTED: 5 functions only, no pseudo-entries (`OptVault-6.4.0-hex.json`) |
| A4 | "the non-dispatch error selector `4e487b71` (Panic) is reported as an extra function" | REFUTED: zero extras; the PUSH4 inventory records it as the trap (`extract-OptVault.txt`) |
| A5 | "mutability inference distinguishes `pure` from `nonpayable`" | REFUTED: MutMix `poke()` (source-ABI pure) reported `nonpayable` on all three legs — recorded upstream-inference delta |
| A6 | "command A's 82 → 83 needs a commit to measure" | REFUTED for measurement purposes: the worktree-overlay mode reproduces the census logic (83/83, §3); prior-82 identity checkable by manifest |
| A7 | "same carrier at 6.4.0 and 6.7.0 mints the same `ev_` id" | REFUTED: `ev_13a039e7…` vs `ev_faa9e12e…` for identical bytes — consistent with r1's unknown-domain note; compare by `subject.digest.sha256` (hex-leg subject digest = hex-text sha `421401f3…`; raw-leg = byte sha `544469b7…`) |

Identity discipline (rule #14): `plan.md`'s byte-identity was re-derived **after** its
final revision — 396 lines, sha256
`854b88d050438c2a8c614100471504dc862836601441d46ccc3936a724aa433e` (`sha256sum` run after
the last edit). Every `evidence/` file is pinned in `evidence/SHA256SUMS` (28 rows,
generated after the last evidence write; the manifest excludes itself by construction —
a first generation self-included and was caught by `sha256sum -c`, then re-derived).

## 5. Blockers

None. Notes for the parent/chain: (a) the prototypes are pre-measurements — executors
must re-derive every identity on their own pinned bytes per rule #14; (b) the README
patch before-text must be re-read from `git show <work-commit>:corpus/README.md` at
landing; (c) `.ufo/gates/custody-pair/custody-pair.py` shows modified in `git status`
(C2's authorized implementer, not this seat — untouched by me); (d) the freeform
`/tmp`-EDQUOT constraint applies to every compile/probe recipe (disk-backed TMPDIR
carried in all plan recipes).