# SEAT CR-2 | CHAIN c1 | ROLE critic — attacks on language/scope of the C1 entry draft

Wave arc3-loop1-round1 (kaidoku-shokunin). Snapshot 2026-10-19T10:20Z, HEAD
`e845c2b524ad2e59871e004c51a1386e192a74ab`. Task: attacks on language/scope —
(1) availability→holding inference in the entry draft; (2) generalizing one
contract shape to "real EVM bytecode held"; (3) contradiction with r3-07's
recorded limits. Actual patch text checked: `claims/c1/EX-12/knowledge-entry.patch.md`
(hunks A+B) + `claims/c1/EX-13/_scratch/README.patched` (map token) +
`claims/c1/records-drafts/*` + `claims/c1/PL-1/plan.md`. Read-only on the repo;
my only writes are this report, `claims/c1/CR-2/` artifacts, and scratch under
`/var/tmp` (declared deviation — `/tmp` is EDQUOT-broken this wave). No git
mutations in the repo; scratch-repo commits were made only in my own clones.

## 0. Verdicts (summary)

- **(1) availability→holding: PASS.** The entry carries an explicit scope line
  ("RESULT-class exercise only — no Core promotion, no availability→holding
  claim") and a clean language scan (no held/works/supported/available/
  capability/proves/proven anywhere in it). Every "recovered" claim traces to a
  sealed envelope id, not to capability/availability text. One caveat: the
  entry's *only* check that does not pass when run as written is its own
  `recheck:` command (F1 below).
- **(2) generalization from one contract shape: PASS WITH A SCOPE-LANGUAGE NOTE.**
  The entry names three independently authored carriers (K=5/6/11), two REA pins,
  and lists vyper/optimizer/prologue/size/deployment as unknowns. The gap is in
  the *map row*, not the entry: after the token edit the EVM row still says
  "held — EVMole selectors recovered from synthetic dispatcher; positional
  encoding quirk" — a state summary that now understates the row (F4).
- **(3) contradiction with r3-07's recorded limits: PASS — none found.** Offset
  semantics, bare-hash selectors, no-name-resolution, SHA-256 ≠ Keccak, worker
  limits, kind/hardfork/deployment `unknown`, raw≡hex convergence: all either
  restated correctly or extended without contradiction. One omission: r3-07's
  candidate-2 hypothesis ("classification needs richer bytecode to engage") is
  refuted by measurement but not recorded as refuted (F3). One label nit (F5).
- **Two hard defects found by measurement, independent of the three attack
  lines:** the entry's recorded file identity is stale against its own patch
  text (F2), and the `recheck:` line fails as written (F1). Both are in
  `claims/c1/CR-2/proposed-fixes.patch.md`.

## 1. Work performed (each bullet with an evidence pointer)

- Read the frozen claims/roster (`claims-frozen.md:14-38,90-104`); r3-07 incl.
  its errata (`corpus/knowledge/2026-10-13-r3-evm-interface.md:47-76,133-155`);
  `corpus/QUALITY.md` (criteria 4,5,7,10,12,13); `PROVINCE.md:91-93`; recipes A/B
  (`SCORECARD.md:86-142`); `corpus/lessons/2026-10-18-wave-dispatch-counting.md`.
- Read the C1 patch texts: EX-12's entry patch (both revisions — the on-disk
  patch vs EX-12's scratch-tree file), EX-13's map-token patch
  (`_scratch/map-token.patch`, `README.patched`, scratch-repo commit `295cd30a`),
  SC-3's LOG/SCORECARD drafts, PL-1's plan (incl. its §S12 state-text variant),
  EX-14's `MANIFEST.draft.txt`, SC-1's `receipts/chain-ledger.draft.md`.
- Read the probe evidence base directly (not from prose): RV-2's
  `probe-runtime-{hex,raw}-6.4.0.json`, `probe-runtime-hex-6.7.0.json`,
  `probe-rerun-{a,b}.json`, `probe-cwd-root-6.4.0.json`,
  `probe-creation-hex-6.4.0.json`, `probe-EX02-smoke-bin-6.4.0.json`,
  `attack/probe-many.json` + `attack/expected-many.txt`; EX-06's
  `evidence/run-{hex,raw}-6.7.0.json`, `planted-K.json`, `transcript.txt`,
  `repro.sh`; EX-07's `reconciliation.md`, `m1-*`, `m2-*`, `reconciliation-run.txt`;
  RV-1's `independent-verification.txt`; RV-3's `independent-verification.txt`.
- Read the landed seat reports relevant to the chain: EX-01, EX-02, EX-07, EX-10,
  EX-11, EX-15, PL-1, RV-1, RV-2, RV-3 (via claims), SC-1 (ledger), SC-2, SC-3.
- Independently ran command A (recipe `SCORECARD.md:94-122`) at HEAD →
  81/81, 13/13 (`claims/c1/CR-2/command-A-runs.txt` §1).
- Built two scratch clones of HEAD in `/var/tmp/cr2-arc3l1r1-scratch/` (no repo
  writes): applied EX-12's patch → 82/82; built the naming-mismatch state (file
  named per PL-1's plan `…-evm-solc.md`, token per EX-13 `…-evm-real-solc`) →
  82 files / 81 mapped / 9.88. All three outputs in `command-A-runs.txt`.
- Reconstructed the entry from the patch's hunk A and compared against EX-12's
  scratch-tree file: `claims/c1/CR-2/entry-file-identity.txt`,
  `entry-version-diff.txt`.
- Ran the entry's `recheck:` command verbatim in three environment variants
  (cwd=/tmp, cwd=repo root, TMPDIR=disk-backed):
  `claims/c1/CR-2/recheck-fail-cdtmp.json`, `recheck-fail-root.json`,
  `recheck-ok-disk-tmpdir.json`.
- Measured planted-set pre-probe ordering by mtime:
  `claims/c1/CR-2/planted-ordering.txt`.
- Language scan on the applied entry text (held/works/supported/available/
  capability/proves/proven) → no matches; one "closes" phrase (scoped).
- Wrote `claims/c1/CR-2/proposed-fixes.patch.md` (F1–F5, not applied).

## 2. Proposed changes (patch-text artifact paths — NOT applied)

- `claims/c1/CR-2/proposed-fixes.patch.md`:
  - **F1 (required)** — replace the entry's `recheck:` line: it fails as written
    (measured exit 1, typed `execution_failure`, EDQUOT errno -122 in the EVMole
    worker); the replacement carries `mkdir -p` + a disk-backed `TMPDIR`.
  - **F2 (recommended)** — re-derive the entry file's sha256 at landing; the
    patch text's step-4 identity (8,316 B / `f95c5a05…`) is stale against the
    patch's own output (8,598 B / `d8d85949…`). Land the patch as-is; fix the
    recorded hash.
  - **F3 (optional)** — record r3-07's candidate-2 hypothesis as refuted by
    measurement (kind stays `unknown` on real solc output).
  - **F4 (optional)** — same-line (still line-neutral) map-row state text update
    so the row summary covers both entries; otherwise record as named debt.
  - **F5 (nit)** — "r3 erratum" → "the r3-07 entry's round-4 erratum".
- No repo file was created or modified by this seat beyond the allowed surfaces.

## 3. Before→after measurement relevant to chain c1's claim

Before (independent, mine): command A at HEAD →
`{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
"depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
"revision": "HEAD", "rule_blocks": 13}` — matches EX-11's sealed artifact.

After (simulated at the patch level, scratch clone + EX-12 patch committed) →
`{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [],
"citation_resolved_rules": 13, "coverage_score": 10.0, "depth_score": 10.0,
"rule_blocks": 13}`; README line count 190 → 190 (line-neutral); prior-81 diff
(`git diff --name-only e845c2b5 HEAD -- corpus/knowledge`) lists only the new
entry file. All in `claims/c1/CR-2/command-A-runs.txt`.

Names must match byte-for-byte (mismatch experiment): file
`…-evm-solc.md` against token `…-evm-real-solc` →
`{"knowledge_files": 82, "mapped": 81, "coverage_score": 9.88,
"missing": ["2026-10-19-arc3-r1-evm-solc"],
"dangling": ["2026-10-19-arc3-r1-evm-real-solc"]}`. The landed drafts agree on
`2026-10-19-arc3-r1-evm-real-solc` (EX-12 hunk A filename = hunk B token); PL-1's
plan name (`…-evm-solc`) is superseded and must not be used.

The entry's own recorded check, run as written (three variants):

```
cd /tmp   + TMPDIR unset          → exit 1  execution_failure (errno -122, worker)
repo root + TMPDIR unset          → exit 1  same class
cd /tmp   + TMPDIR=/var/tmp/...   → exit 0  ev_45849c8b…, 5/5 functions, dispatch:"abi"
```

## 4. Attacks/refutations attempted, with verdicts

**Attack line 1 — availability→holding inference in the entry draft.**

- Scanned the applied entry text for holding-adjacent vocabulary
  (`held|works|supported|available|capability|proves|proven`) → **no matches**;
  the only `held` in the patch is pre-existing row text in hunk B. The entry's
  scope line: "RESULT-class exercise only — no Core promotion, no
  availability→holding claim. Family-scoped to solc-0.8.37-compiled runtime
  carriers compiled on this host this round, under the two REA pins named."
  Every recovery claim cites an envelope id (ev_45849c8b…, ev_3aacd424…,
  ev_19d7d3cb…, ev_56d89cb4…, ev_9259f412…, ev_d0d0b054…) — run-evidence, not
  availability. **Verdict: PASS.**
- Sub-attack: is any *stated* check unrun? Yes — the `recheck:` command, run
  verbatim, exits 1 (EDQUOT; F1). Its content expectation (5 functions,
  `dispatch:"abi"`, decoded sha `c1081a56…`) does reproduce once a disk-backed
  `TMPDIR` is set, so the defect is the recorded command, not the claim.
  **Verdict: defect confirmed, fix supplied (F1).**
- Sub-attack: does the entry lean on the *ambient* solc? No — it pins the
  receipted prefix and records the ambient-install fact ("tree byte-identical to
  the pre-existing ambient install"), consistent with EX-02's correction of
  PL-1's "no solc exists on this host" premise (`PL-1/plan.md:34` vs
  `seats/EX-02.md` §4.2). **Verdict: PASS.**
- Sub-attack: availability of `capabilities[].available:true` used as holding?
  Not present in the entry. QUALITY #10 upheld.

**Attack line 2 — generalizing one contract shape to "real EVM bytecode held".**

- The entry's own scope: family-scoped to solc-0.8.37 runtime carriers compiled
  on this host this round, two REA pins; unknowns list vyper, optimizer-enabled
  shapes, other prologues, sizes above the probed ~1.8–1.9 KB class, CBOR-decode
  generality, deployment/chain identity. Three carriers with per-carrier K
  (5/6/11) — the claim's "one contract shape" is not silently widened.
  **Verdict: PASS for the entry.**
- Map row (hunk B): state text unchanged ("…recovered from synthetic
  dispatcher; positional encoding quirk") while the row now lists the real-solc
  entry. The row is the surface a reader sees first; as written it understates
  the row and could be read as "the new entry is synthetic too". PL-1's plan
  §S12 already drafted the accurate same-line form; EX-13/EX-12 dropped it.
  Still line-neutral if fixed (same physical line). **Verdict: scope-language
  defect (F4) — fix or record as debt.**
- Cross-check of generalization risk from the evidence itself: the dispatcher
  prologue of real solc 0.8.37 is `5f3560e01c` (PUSH0), not r3-07's synthetic
  `60003560e01c` (EX-07 `reconciliation.md` §M1; RV-1). The entry does not claim
  prologue equivalence; its unknowns name prologue variance. **Verdict: PASS.**
- K-collapse risk: the LOG draft's single `[[FILL: K]]` would collapse 5/6/11;
  the entry names all three. Parent should fill the drafts per carrier.
  **Verdict: note.**

**Attack line 3 — contradiction with r3-07's recorded limits.**

- `bytecodeOffset` semantics: entry says "offsets 89/137/167/215/263 are
  dispatch-target JUMPDESTs (r3 erratum, …:149-155)". Measured: probe offsets =
  EX-07 M1 chain dests (89/137/167/215/263; KdxToken 100/148/178/226/254/302),
  PUSH4 sites are 31/42/53/64/75 (86); RV-1 confirms every offset byte is `0x5b`.
  **No contradiction; correct per errata.**
- Selectors stay bare hashes / no name resolution: entry says the
  argument/mutability strings are "upstream inferences consistent with the
  compiled ABIs — not verified ABI signatures, names, or source identity". The
  probe returns bare selector hashes; names come from the local ABI. **PASS.**
- `kind`/hardfork/deployment `unknown`; SHA-256 ≠ Keccak; worker limits
  (256 MiB heap / 3 GiB AS / 30 s / 16 MiB cap); no RPC/execution — all restated
  in the entry's Limitations line. **PASS.**
- r3-07 candidate 2's recorded suggestion ("classification appears to need
  richer bytecode (real solc output) to engage", `:44-45`) — refuted by
  measurement (kind stays `unknown` on real solc runtime and creation legs), but
  the entry does not record the refutation. **Verdict: omission (F3), not a
  contradiction.**
- Label nit: the errata is titled "Errata (round 4)" in the r3-07 file; the
  entry's "r3 erratum" is accurate as "the erratum in the r3-07 entry" but can
  be misread. **Verdict: nit (F5).**

**Extra attacks (cheap, beyond the seat line).**

- **Entry file identity (stale-hash attack).** Applying hunk A as written yields
  8,598 B / 31 lines / `d8d85949…`; the patch text claims 8,316 B /
  `f95c5a05…`; EX-12's own scratch file hashes `f95c5a05…`. The four-line diff
  (`entry-version-diff.txt`) is path-style only (fully-qualified attack paths;
  `corpus/knowledge/` added to the errata cite) — the patch was revised after
  hashing. **Verdict: defect confirmed; do not revert the patch, re-hash at
  landing (F2).**
- **Token-without-file / file-without-token.** SC-3 measured the token-only
  state (81/81 + dangling); I measured the file/token *mismatch* state
  (82/81 + both). Both confirm the entry and token must land in one commit.
  **Verdict: constraint confirmed.**
- **Planted-set pre-probe ordering (claim clause b).** mtimes:
  Rv2Token expected 07:00:46.98 < first probe 07:01:28.58 (41.6 s);
  Rv2Many expected 07:03:25.97 < probe 07:03:26.74 (0.77 s — thin margin);
  KdxToken planted-K 07:02:50.03 < probe 07:09:36.53. Ordering holds for all
  three; the entry's evidence map cites mtimes only for Rv2Token — recommend
  citing all three at landing. **Verdict: supported; citation gap.**
- **Evidence-base selection.** The entry cites RV-2's and EX-06's legs; EX-05's
  two sealed legs on the same KdxToken carrier (`ev_4dd5ea20…`, `ev_2a79dd25…`,
  re-run field-identically by RV-2) are not cited. Not a defect (selection is
  allowed) but the parent should know the chain holds more legs than the entry
  lists. **Verdict: note.**
- **Determinism.** `probe-rerun-a/b.json` and `probe-runtime-hex-6.4.0.json` are
  9,399 B and sha256 `f2aec424…` — byte-identical, same id. SC-1's ledger R7
  ("rerun VOID") was captured before the files settled; re-check at integration
  (the ledger's own footer says so). **Verdict: rerun leg closed; ledger row
  stale.**
- **Plan-vs-actual divergence.** EX-03/EX-04 never landed (RV-1's primary target
  absent; EX-05 substituted EX-06's byte-identical KdxToken; RV-2 documents
  this). The chain still holds the needed evidence, but the plan's S4/S5
  artifacts (compile receipt, keccak receipt) are gaps the parent should name in
  the records rather than assume. **Verdict: chain-level gap, recorded here.**
- **/tmp hazard.** My scratch: `/var/tmp/cr2-arc3l1r1-scratch` (declared
  deviation; `/tmp` write fails EDQUOT — measured). The probe worker inherits
  the failure with TMPDIR unset (measured; corroborated by RV-2 §5 and EX-06
  `repro.sh:11,85-90`).

## 5. Blockers

- None for this seat. `/tmp` is unusable (EDQUOT); scratch used `/var/tmp` and
  is cleaned at close. EX-12's seat report (`seats/EX-12.md`) had not landed at
  my close; my attacks are against the patch text itself, so no dependency is
  outstanding. EX-03/EX-04 artifacts remain absent (chain-level gap, §4).
- Gaps named for the parent: F1–F5 above; the drafts' `[[FILL]]` fields (install
  receipt path under `receipts/`, records-commit command-A numbers, custody
  post-pair) remain parent-side; EX-14's manifest must be regenerated at close
  (SC-2's crosscheck found post-generation churn, not tamper).
