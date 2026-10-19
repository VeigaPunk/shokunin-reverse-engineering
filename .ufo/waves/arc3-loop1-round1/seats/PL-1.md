# PL-1 — seat report (chain c1, planner)

Wave `arc3-loop1-round1`; seat line: draft C1's execution plan (install solc →
author contract → compile → probe raw/hex → 3-way selector reconciliation →
control → rerun → receipts → records) with honest-stop branches and per-executor
task splits.

Artifact: `.ufo/waves/arc3-loop1-round1/claims/c1/PL-1/plan.md` — sha256
`e9a3921f8503d0cdf5c6b6c8e48b262ef3f50cf7142c9153b5161423ab6e10ff`, 540 lines.
No other repo path was written by this seat.

---

## 1. Work performed

- Read the frozen claim, roster and rules; mapped C1's claim and its
  before-state. Evidence: `claims-frozen.md:14-38,73-104`.
- Recon of every C1 context pointer: the r3-07 synthetic-carrier entry
  (`corpus/knowledge/2026-10-13-r3-evm-interface.md`, incl. its r4 offset
  errata at :149-155), PROVINCE EVM rows (`PROVINCE.md:54,91-93`), SCORECARD
  measurement recipes A/B (`SCORECARD.md:86-143`), the arc2 rounds that set the
  claim's baseline (r4 probe debt, r6-r8 map-token form, r9-r10 rules count),
  QUALITY.md's 16-criterion admission bar (`corpus/QUALITY.md:9-25`) and the
  wave-counting lesson (`corpus/lessons/2026-10-18-wave-dispatch-counting.md`).
- **De-risked the entire pipeline on scratch copies** (not `/tmp` — see §5):
  npm `solc@0.8.37` install into an isolated prefix → contract authoring
  (K=10 selectors) + control contract → standard-JSON compile → probe on `hex`
  and `raw` → 3-way reconciliation → empty/mutation controls → rerun/id check.
  All commands and raw outputs: `plan.md` §8 (8.1-8.12); evidence files retained
  at `/var/tmp/pl1/` (sources, carriers, compile summary, six probe envelopes,
  `reconciliation.txt`).
- Discovered and recorded 9 plan-critical environment facts (F1-F9, `plan.md`
  §2), including two silent failure modes (F2 `solcjs` is the binary name; F3
  `solcjs --standard-json` prints a `>>> …` SMT line on stdout before the JSON)
  and the `/tmp` EDQUOT wall (F4) with its fix (F5 `TMPDIR` disk-backed).
- Authored the plan: steps S1-S12 with exact commands, owners, acceptance
  values and receipts; honest-stop branches H1-H8; per-executor splits
  (EX-01..EX-15, SC, RV, CR, VZ); records plan with the exact line-neutral
  map-token form for `corpus/README.md:38`; risks; integration note. Evidence:
  `plan.md` §3-§9.
- Reconciled the plan with the chain's in-flight artifacts at close and synced
  the deltas (install prefix `tools/solc-prefix/`, `/dev/shm` scratch precedent,
  multi-contract evidence superseding the single-source recommendation):
  `plan.md` §9. Cited by EX-05 in its own divergence note
  (`claims/c1/EX-05/README.md:4-16`).

## 2. Proposed changes

- **None authored by this seat.** The plan specifies, but does not write, the
  round's patch text: knowledge entry `corpus/knowledge/2026-10-19-arc3-r1-evm-solc.md`
  (owner EX-12), the line-neutral map token at `corpus/README.md:38` (owner
  EX-13; exact before/after line in `plan.md` §3 S12), LOG/SCORECARD patch text
  (owner EX-14), optional PROVINCE Frontier annotation (`plan.md` §6.5).
- This seat's only repo writes: this report and `claims/c1/PL-1/plan.md`.

## 3. Before→after measurement relevant to C1's claim

**Before (measured by me, and independently by EX-11).** Command A (recipe
`SCORECARD.md:86-124`) at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`:

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
 "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}
```

Corroboration: `claims/c1/EX-11/command-A-before.txt` is byte-equivalent
(81/81, 13/13, empty missing/dangling). `which solc` → not found (before).

**After — pipeline level (measured by me on scratch; this is the claim's
mechanism, not the claim's records move).** K = 10 selectors recorded
pre-probe; both encodings recover 10/10, and the four independent selector
sources are exactly equal:

```
K (solc methodIdentifiers): 10
solc == keccak (signature-derived): True | symmetric diff: set()
probe hex == solc: True | symmetric diff: set()
probe raw == solc: True | symmetric diff: set()
probe hex == probe raw: True
missing from probe: [] | extra in probe: []
```

Probe ids: hex `ev_911108c0270ce68d1bda9566148283a6eec008d27428d6606e399e72962d0bad`,
raw `ev_80d075d313f87c01a71d9b9fa82b6c538c75970b37c39822210922e2fc266d11`
(both exit 0; `plan.md` §8.6-§8.7). Control leg: compiled dispatch-less runtime
→ 0/0 functions, `ev_39e1526d…`; carrier-mutation leg → the mutated selector
`0xa9059cbc` recovered, `ev_7628d241…` (§8.8).

**After — claim level (NOT measurable by me; predicted, explicitly flagged).**
`knowledge_files 81 → 82, mapped 82, missing [], dangling [], rules 13/13,
prior-81 untouched` is the target to be measured at the parent's records commit
(owner EX-15 per the plan's S12; my plan states it as an acceptance value, and
I did not measure it). At my close the knowledge entry and map token had not
landed (EX-12/EX-13 artifacts still in flight).

## 4. Attacks / refutations attempted, with verdicts

| # | Attack | Result / verdict |
|---|---|---|
| A1 | "The probe replays an expected selector table rather than reading bytes." | **Attack failed (claim strengthened).** Carrier-mutation control: `a9059cbb`→`a9059cbc` in a copy → probe returns `0xa9059cbc` (10/10). `plan.md` §8.8. |
| A2 | "The evidence id is content-addressed (usable as a bytes-only identity)." | **Refuted.** Same bytes, renamed path → different id (`ev_911108c0…` vs `ev_62e889cf…`); same (content,path,params) re-run → same id. Corroborated by EX-05's `kdx.raw.renamed.json` (`ev_b29370…`). The knowledge entry must state the id domain as path-sensitive (QUALITY #14/#15). `plan.md` F7, §8.9. |
| A3 | My own weak leg: "selector byte-presence in the runtime is a sufficient check." | **Refuted by measurement.** `42966c68` occurs twice in the runtime hex → presence is necessary, not sufficient; demoted to the weak leg in S7. §8.12. |
| A4 | "The probe will hallucinate selectors on dispatch-less real bytecode." | **Not observed.** Compiled contract with zero external functions → 0/0 in both result views, exit 0. §8.8. |
| A5 | "These bytes might not be compiler output at all (hand-built carrier)." | **Corroborated as solc output.** CBOR trailer decodes `solc: 000825` (= 0.8.37) + an `ipfs` hash; creation blob yields 0 selectors / `kind` null. §8.10-§8.11. |
| A6 | The dispatch's "/tmp scratch" instruction. | **Refuted by measurement.** `/tmp` is usrquota-exhausted (5-byte write → EDQUOT); the probe fails closed with `execution_failure` / "Unknown system error -122 … write" until `TMPDIR` is disk-backed. Independently corroborated: EX-06 (`repro.sh:10,82-87`), EX-08 (`probe-recon-raw-noTMPDIR.json`), EX-15's casualty census. §8.4-§8.5. |
| A7 | The obvious command forms: `solc` binary, `JSON.parse` on stdout. | **Both refuted.** Binary is `solcjs`; stdout carries a `>>> …` SMT line first (RV-2's raw capture `claims/c1/RV-2/solc-out.raw:1` shows the line in the chain). §8.2-§8.3. |
| A8 | Attacks NOT attempted (named unknowns): optimizer-on builds (dispatch-table merging), vyper compilation (not installed), inline-assembly/custom dispatchers, chain/RPC authenticity (explicitly out of the envelope). | Left as named unknowns for the knowledge entry's limitations. |

## 5. Blockers

- **`/tmp` unusable (blocker for the wave, worked around).** Per-user quota
  exhausted on the 16 G `usrquota` tmpfs; even a 5-byte write fails. Scratch and
  `TMPDIR` were relocated to `/var/tmp/pl1` (disk-backed), per the lane's own
  standing rule (`corpus/lessons/2026-10-18-caller-independent-services.md:23-24`).
  My `/tmp` casualties appear in EX-15's census (`claims/c1/EX-15/tmp-quota-casualties.txt`,
  `/tmp/pl1/*.sol`, `/tmp/pl1-quota-probe.txt`) and are now removed; `/var/tmp/pl1`
  retains the de-risk evidence (236 K, evidence files only — node_modules and
  temp dirs deleted). No evidence lost. The substitution should be named once in
  the round report.
- **Harness note:** the Write tool refuses `/tmp` paths ("unrecognized filesystem
  error"); scratch was written via shell heredocs instead. Not a correctness
  issue, recorded for the next planner.
- **Seat-mapping divergence (coordination, not evidence).** My plan assigned S5
  (independent keccak) to EX-04; EX-04 landed nothing (EX-05's 25-check poll,
  `claims/c1/EX-05/README.md:8-13`) and EX-05 had to substitute EX-06's KdxToken
  as the probe subject. The chain absorbed it, but the parent should reconcile
  plan-assigned seats against the actual seat lines at dispatch.
- **Open at close (gaps named, not blocking my deliverable):** the records move
  (knowledge entry + map token + LOG/SCORECARD patch text) had not landed, so
  the claim's 82/82 remains a prediction; the three hardening legs I hold
  (carrier mutation, compiled dispatch-less control, CBOR-trailer decode) are
  not yet re-run on the chain's canonical KdxToken — a seat can do it in ~4
  probe invocations (seconds each), citing `plan.md` §8 for the expected
  verdicts. Seats with reports landed at my close: CU-1, EX-01, EX-02, EX-07,
  EX-10, EX-11, EX-15, EX-19, EX-24, EX-26, EX-30, PL-2, RV-1, RV-4, RV-6, RV-8,
  SC-3, SC-6 (+ this report) — C1 executors EX-03/EX-04/EX-05/EX-06/EX-08/EX-09/
  EX-12/EX-13/EX-14 and SC-1/SC-2, RV-2/RV-3, CR-1/CR-2, VZ-1 had artifacts but
  no seat report yet at 10:08Z.
