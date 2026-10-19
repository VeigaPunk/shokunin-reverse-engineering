# SEAT CN-1 — chain cross — connector (arc3-loop1-round4)

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Task as given: cross-chain
consistency — the three chains' readings must not contradict (command A baseline
at HEAD `015e1ba`: 83/83, 14/14; custody digests; census/probe states) —
reconcile or flag at `claims/cross/consistency.md`.

Writes by this seat: this report and
`.ufo/waves/arc3-loop1-round4/claims/cross/consistency.md` (the canonical cross
record, `a281cd4b…` after the F-1 amendment) plus receipts under
`claims/cross/CN-1/receipts/`. Scratch `/var/tmp/cn1-arc3r4` (never `/tmp`);
scratch git fixtures are their own throwaway repos under that root — no git
mutation in the real repo. Custody paths read-only (sha256/stat; the two `verify`
runs read them, never write). No LOG/SCORECARD/SHONEN/corpus/SKILL/PROVINCE/README
writes by this seat; the registry-row repair is referenced as patch text, not applied.

## 1. Work performed (evidence pointers)

**Reads first:** `claims-frozen.md` (including the lane-substitution note —
hyper lane 402 on all 48 seats, full roster re-dispatched on devin; recorded with
cause, not a lane signal); `SCORECARD.md` measurement recipes; the r3 EVM entry
(`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` — its Unknowns
name the Vyper leg C1 works); the r3 c2 patch texts (`EX-24/`, `CR-3/`, `CR-4/`,
`RV-8/`); both instruments and the custody tool's README.

**CN-1 baseline re-derivations (all first-hand, receipts in
`claims/cross/CN-1/receipts/`):**

| Reading | Result |
|---|---|
| command A at `015e1ba` (recipe verbatim) | **83/83, missing [], dangling [], 14/14, 10.0/10.0** (`baseline-pins.txt`, `poll.log` session) |
| census (`c1-census-v10.py`, `d0772ce8…`) | **PASS 0/0/0/0**, exit 0 (`census-head.out`) |
| probe (`e2665074…`, table `1b3ab955…`, expected `9df0452c…`) | default + `--strict` **findings=0 exit 0**; selftest **13/13 CLEAN** (`probe-head-strict.out`) |
| custody tool before (r3 identity `7cd19c3c…`) | selftest **22/22 CLEAN** |
| custody 5-path t0 | `verify config-post-pair-v2r3.txt --live --require-paths 5` → **MATCH 5/5 exit 0** (`custody-t0.txt`) |
| prior-83 byte identity | `git show` blobs vs worktree: **0 differences** across all 83 knowledge files; README/SKILL/PROVINCE/SCORECARD also identical |

**Landing simulations (scratch git fixtures carrying the probe's 26 target files
at their current bytes; fixture baseline findings=0):**

- **C1 full landing** — entry draft (18,166 B) + PRIMARY line-neutral map token
  on a scratch tree: command A → **84/84, missing [], dangling [], 14/14**;
  prior-83 **byte-identical** (0 diffs); probe `--strict` **findings=0**
  (`c1-landing-sim.probe.out`).
- **C1 adversarial** — row insert variant: probe **failed, findings=5**
  (`sc69-readme-177`, `sc72-readme-nitrow`, `readme175-sc1217`, `readme175-r7range`,
  `readme175-r8e2`) — `adversarial-readme-row-insert.probe.out`.
- **C2 line-neutrality** — 3-line→3-line rewrite: census **PASS**; 4-line
  (+1 net): census **FAIL** at the `PROVINCE.md:119` marker; +1/−1 compensating
  (total 162 held): **FAIL**, same marker; +3 above the safety clause: probe
  **failed** on `shonen-province-range` (`adversarial-prov-shift3.probe.out`).
- **C2 token-freedom** — `rea-agents@6.7.0` in the line-neutral Frontier text:
  census **UNDECLARED** → FAIL (`adversarial-prov-token.census.out`); same class
  for a gated token appended to the SKILL.md custody row
  (`adversarial-skillrow-token.census.out`) — C2's RV-4 measured this
  independently (`attack-skillrow-gated-token.txt`, UNDECLARED=1).
- **C3 live revision** — tool `29bb45ae…` + README (settled `9d9400da…`, 272 L):
  selftest **28/28 CLEAN**; probe clean on a fixture carrying them; dropping the
  `never \`/tmp\`` anchor reddens `custody-readme-scratch-never-tmp` (control).
- **F-1 repair** — C3's registry-row patch text (`8e56f3d9…`, one line differs,
  :390): applied on scratch → census **PASS 0/0/0/0**; probe **findings=0**.

**Independent claim spot-checks:**

- C1's K/K: CN-1 re-derived selectors from `EX-04/out/abi.json` via pycryptodome
  keccak and compared to the sealed envelope `probe-6.7.0-hex.json`:
  **ABI-derived == probe-recovered, 15/15, zero missing / zero extra**.
- C3's live pair: `verify live-pre live-post --require-paths 5` → **MATCH 5/5**;
  `verify live-post --live --require-paths 5` → **MATCH 5/5**.
- C2's census state and RV-4's blindness proofs re-read and matching my runs.

## 2. Proposed changes (patch-text paths)

- **none written by this seat.** The one repair the sweep flags (F-1) already
  exists as another chain's patch text:
  `.ufo/waves/arc3-loop1-round4/claims/c3/EX-21/patch/proposed-skill-registry-row.patch.md`
  (+ `patch/skill-registry-row.patched.md`, `8e56f3d9…`). Verified sound on
  scratch; application is the parent's, in the coupled landing.

## 3. Before → after measurement for the cross-chain claim

The cross-chain claim is consistency, not a quantity. Its before → after:

- **before**: three chains' readings unreconciled; the shared baseline
  (83/83, 14/14; custody digests; census/probe states) re-derived only per chain.
- **after**: every shared reading re-derived by CN-1 and matched to the chain
  records (agreement matrix, `consistency.md` §2): **all consistent**; each
  chain's landing simulated against the *other* chains' instruments, with four
  named conditions the landings must satisfy (line-neutral README token; exact
  line-neutral PROVINCE repairs; census-token freedom; registry-row application);
  **two divergences found (F-1 registry-row count; F-6 draft-vs-patch stale
  coverage), both with verified repairs**, plus **one ordering constraint
  (F-5: C1's entry and C2's PROVINCE repair must land same-commit)** and two
  informational notes (F-2, F-4). No contradiction on any shared reading.
- **F-6 resolution (measured, in-round)**: C2's chain shipped v2
  (`0b8ad045…`), which CN-1 measured to repair all six stale rows (162 lines
  held, `69ceea9b…`, census PASS, probe clean, Core-promotion defect dropped).
  CN-1's after-hash matches EX-14's own re-derivation byte-for-byte.
  Residual: three downstream records (CN-2's outline §R6/§236; VZ-4's
  wave-summary §C2, written 17 s after v2 landed) still describe the v1 state —
  named in `consistency.md` §4 F-6 so they are not quoted as final.

## 4. Attacks/refutations attempted, with verdicts

| Attack | Result | Verdict |
|---|---|---|
| C1 row insert instead of line-neutral token | probe failed, 5 `citation_dead` | **refuted** (line-neutral is load-bearing) |
| C2 +1 net line shift, and compensating +1/−1 at held total | census FAIL at :119 marker | **refuted** (total line count is not sufficient) |
| C2 +3 shift above the safety clause | probe `shonen-province-range` dead | **refuted** |
| C2/C3 gated token in new text | census UNDECLARED → FAIL | **refuted** (prose-only constraint real) |
| C3 README anchor dropped | probe `custody-readme-scratch-never-tmp` dead | **refuted** (anchors live) |
| C3 registry row left at 22 while tool runs 28 | no instrument fires; verified stale by direct read | **confirmed divergence → F-1**, repair verified sound (census PASS, probe clean) |
| **C2 records draft "stale 6 → 0" vs v1 patch** | **v1 repairs only 4 of 6** — F3 and C1 literals survive at :88/:62; VZ-2's census re-run on the real tree reproduces 6 stale | **confirmed divergence → F-6**; **v2 patch measured to repair all six** (162 lines held, census PASS, probe clean, Core-promotion defect dropped) |
| Census scratch root without the 3 scoped files | UNREADABLE + scope-errors, exit 1 | **confirmed** (fail-closed class working; reconciliation F-3) |
| Custody drift since r3 post-pair | live verify MATCH 5/5 | **no drift** (nothing to refute) |
| C1's K/K claim | ABI-derived set == probe set 15/15 | **confirmed** (independent oracle agrees) |
| C2's PROVINCE patch asserts C1's outcome | patch text discloses it; both must land same-commit | **confirmed coupling → F-5** |

## 5. Blockers

None. Three open items for the parent, all in `consistency.md`:
**F-1** — apply C3's registry-row patch in the coupled landing (the row's
"22 fixture cases" is stale against the 28-case tool/README; no instrument
grades it). **F-5** — C1's entry/token and C2's PROVINCE repair must land in the
same commit, or C2's Vyper clause must drop to the solc-only form. **F-6** —
C2's claim verifies only with the **v2** patch (`0b8ad045…`, all six stale rows
repaired, measured); the v1 patch leaves 6 → 2 and the records drafts' "6 → 0"
overstates it. F-2/F-4: re-derive the README and receipt identities at the
records commit (the README moved five times in-round; rule #14).
