# CR-2 seat report — arc3-loop1-round3, chain c1, role critic

Seat CR-2 | chain c1 | critic | 2026-10-19 | repo HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`
Task: attacks on language/scope — "optimizer shapes held" generalization beyond
the two carriers; availability→holding inference; contradiction with r1's
Unknowns wording; check the drafted entry text.

Writes by this seat: this report + `claims/c1/CR-2/` only. No git mutation, no
LOG/SCORECARD/SHONEN/corpus/SKILL edit, custody paths read-only (hash capture not
even needed for my legs beyond the solc receipt which is wave-1's), scratch under
`/var/tmp/cr2r3/` (never `/tmp`). Probe legs ran `npx -y rea-agents@{6.4.0,6.7.0}`
off the host npx cache with `npm_config_offline=true` and a disk-backed `TMPDIR`.

## 1. Work performed (evidence pointers)

- Read: the freeze (`claims-frozen.md:16-36`), the r1 entry (all 33 lines), r1
  install receipt, `corpus/QUALITY.md`, SCORECARD recipes (`:86-124`), round-2
  C1 verdict + precedent CR-2 report, PL-1's plan/carriers, the SC-2 entry draft
  (rev 1 and rev 2) + map-token patch, and the EX-04/05/06/07/10 artifacts the
  draft cites.
- Independent instruments built by this seat (all copied under
  `claims/c1/CR-2/evidence/scripts/`): `cc.js` (solc-prefix standard-JSON
  compile of any source at opt off/on/runs-200), `disp.py` (prologue/selector
  census), `diffreg.py` (opt-off vs opt-on first-difference), `sels.js`
  (keccak selectors from ABI via the prefix's `js-sha3@0.8.0`), `cmdA-wt.py`
  (worktree form of recipe A, self-tested equal to recipe A on the pristine
  tree: identical JSON, 13:11Z).
- Receipt verification (rule: verify before reuse): tarball sha256
  `0e1a1ab6…575a51` (from the npm cache content file, 6,476,046 B), `soljson.js`
  `221d7a66…abad4c`, `solc.js` `188c3fdc…5146f`, `soljs --version`
  `0.8.37+commit.f401782d.Emscripten.clang` — all equal the wave-1 receipt
  (`claims/c1/EX-02/install-receipt.txt` §1/§5/§6); `solc/package.json`
  `b3a90035…3491` matches the draft's re-hash.
- Five carriers compiled by this seat (3 new, 2 recompiles of chain carriers):
  Rv2Token (r1 source), CrVault (payable receive/fallback + mixed mutability),
  CrWide (22 external fns), OptVault and MutMix (PL-1's sources — their pinned
  runtimes re-derived byte-exact: `544469b7…`, `6267ef53…`, `200bc9db…`).
  8 probe envelopes under `claims/c1/CR-2/evidence/probes/` (both pins where run;
  identities in §4/`attack-notes.md`).
- Byte-level census + shape analysis: `evidence/shape-analysis.txt`;
  overlay rehearsal of the 82→83 after-state (§3).
- Headline receipts: r1 recheck reproduced byte-identically (`ev_45849c8b…`,
  envelope sha `f2aec424…` — also equals SC-2's capture); the entry's own
  recheck reproduced (`ev_d409bd50b370c55c…`, 13 functions, decoded `b24a0115…`,
  envelope sha `05f76b33…` — byte-identical to SC-2's capture).
- Artifact identities (rule #14; re-derived after the final revision of each):
  `attack-notes.md 552c2602…`, `proposed-entry-text-fixes.patch.md 953b53f2…`,
  `evidence/shape-analysis.txt 8490cb54…`,
  `evidence/probes/recheck-vaultb-6.4.0.json 05f76b33…` (10,620 B),
  `recheck-rv2-6.4.0.json f2aec424…`, `rv2-on200-6.4.0.json c0f08dd9…`,
  `rv2-on200-6.7.0.json d73ca639…`, `crv-on200-6.4.0.json b69fe1d7…`,
  `crv-on200-6.7.0.json c7890da6…`, `crw-on200-6.4.0.json 7667fe92…`,
  `crw-on200-6.7.0.json 21cc3159…`, `crw-off-6.4.0.json b81310b9…`;
  scripts: `cc.js f95335cf…`, `disp.py 12e95f8d…`, `diffreg.py 48322c1b…`,
  `cmdA-wt.py ce954427…`, `sels.js 5d34e3cc…`. Draft revisions attacked:
  rev 2 `b9ca0310…`, rev 3 `9b0cb5b8…`.

## 2. Proposed changes (patch-text paths)

- `claims/c1/CR-2/proposed-entry-text-fixes.patch.md` — F1–F7 against the SC-2
  entry draft (revisions attacked: rev 2, 106 lines, sha256 `b9ca0310ca7ef099…`,
  13:14Z and rev 3, 108 lines, sha256 `9b0cb5b8459313f7…`, 13:20Z; all findings
  T1–T5/T9 still present at rev 3; apply by content match):
  - F1 (sustained): draft line 42's "r1's `60003560e01c`-class and non-binary
    prologues remain unvisited this round" contradicts the entry's own carrier-A
    control (that class, re-probed this round) and Rv2TokenOpt's linear tree.
  - F2 (sustained): `optB-…{,-rerun}.json` cites 6 rerun envelopes; 1 exists.
  - F3 (sustained): `EX-04/evidence/planted-B.txt` → actual `EX-04/planted-B.txt`
    (`f32393c0…` verified).
  - F4 (sustained): `offset-check-*.json` → actual `EX-04/evidence/probe/…`.
  - F5 (advisory): state the creation-identity convention (decoded bytes).
  - F6 (landing condition): `SC-2/README-identities.txt` — **resolved** (absent
    13:14Z, present 13:20Z).
  - F7 (advisory): "optimizer shapes" wording/title/stem — measured shape
    invariance (see §4 A1b); optional stem rename to `…-evm-optimizer-carriers`.
- No direct edits proposed to any real target; the map-token row text itself is
  sound (plural supported by ≥3 optimizer-enabled non-ERC-20 carriers). The one
  r1-entry-adjacent note (PROVINCE frontier staleness) is already named in the
  SC-2 draft's parent notes; I add nothing to it.

## 3. Before→after measurement for C1 (coverage claim)

Command A, verbatim recipe (git objects), at HEAD — before-state:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311", "rule_blocks": 14}
```

After-state — this seat's tree-level rehearsal (`evidence/scripts/cmdA-wt.py`
self-tested equal to recipe A on the unmodified worktree), a scratch copy of
`corpus/` + `SKILL.md` with (a) a stub entry named with the proposed stem
`2026-10-19-arc3-r3-evm-optimizer-shapes` and (b) the SC-2 primary map line
applied:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 83, "mapped": 83, "missing": [], "dangling": [], "rule_blocks": 14}
```

plus: README 190 → 190 lines, exactly 1 changed line, token set 82 → 83, **zero
prior tokens removed**, new token == the stub's stem. The parent must re-measure
"at the work commit" from real Git objects; my after-state is a rehearsal of the
landing pair (entry file + token must land together).

## 4. Attacks/refutations attempted, with verdicts

| # | Attack | Verdict |
|---|---|---|
| A1a | "K/K on optimizer-enabled carriers does not generalize beyond the round's two carriers" | **REFUTED** (supports the claim): 4 independent carriers this seat, both pins — Rv2Token opt200 5/5 `ed6c8a76…`; CrVault opt200 7/7 `2e636c0f…` (payable receive/fallback, mixed mutability, `payable` correctly inferred on `donate()`); CrWide opt200 22/22 `617c91cc…` and opt-off 22/22 `83040705…` (binary-search dispatch `8063…1161`, a shape the r1 chain never probed). Zero missing / zero extra everywhere; every offset on `0x5b` |
| A1b | "'Optimizer shapes held' names the measured variable" | **SUSTAINED as wording defect**: over 6 opt-off/opt-on pairs (incl. the chain's own VaultB `0x31`, carrierB@EX-04 `0x0b`) the common prefix always covers the prologue + calldatasize guard + `5f3560e01c` + leading compares; only jump targets/bodies differ. `5f3560e01c` in every dispatcher carrier at both settings; `60003560e01c` in none of mine; linear-vs-binary tracks selector count (22 fns → `1161` even opt-off). Fix F7 |
| A2 | Availability→holding leakage | **REFUTED for the artifacts/draft seen**: per-carrier envelopes only; `runtime_execution:"not-performed"` in every envelope; Scope carries "no availability→holding claim"; both-pin usage stated per carrier (EX-04 6.4.0-only visible in the draft's source line). The r1 recheck line reproduces (that was the recorded-invocation availability test) |
| A3 | Contradiction with r1's Unknowns wording | **REFUTED for the draft**: no "first optimizer-enabled compile" phrasing (r1's Smoke compile was `--optimize`, `…-arc3-r1-evm-real-solc.md:11`), the narrow residue (runs≠200, viaIR, other prologue classes, size class) is re-stated in this entry's Unknowns, and the parent note forbids rewriting r1's bytes. One optional strengthening: name the r1 Unknowns item as "narrowed" explicitly |
| T1–T5, T9 | Text-level attacks on the entry draft (internal contradiction; rerun citation overclaim; two wrong paths; creation-identity convention; title/stem wording) | **SUSTAINED** (F1–F5, F7) — receipts in `attack-notes.md` table + `proposed-entry-text-fixes.patch.md` |
| T6–T8, T10 | Recheck reproducibility; availability→holding; r1-Unknowns phrasing; map-row plural | **REFUTED** — recheck byte-identical (mine = SC-2's = declared), etc. |
| — | Decoy precision (peer EX-10): constants-no-dispatch → 0 fns; planted decoy selector → 1 fn | read; behavior consistent, no over-report |

## 5. Blockers

- None blocking this seat. Coordination notes: (a) the SC-2 draft is under active
  revision — my fixes are written by content match against rev 2 `b9ca0310…`
  (13:14Z) and rev 3 `9b0cb5b8…` (13:20Z), re-check against the landed bytes;
  (b) `SC-2/README-identities.txt` was absent at 13:14Z but landed by 13:20Z —
  landing condition F6 resolved; (c) my after-state is a rehearsal —
  the "at the work commit" numbers must be re-measured by the parent from real Git
  objects; (d) the map-token patch and the entry file must land together, stem ==
  token.