# SEAT VZ-1 | CHAIN c1 | ROLE convergence — arc3-loop1-round1

Window 2026-10-19T06:57→07:19-03 (09:57→10:19Z). Repo HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
at every sample (`git rev-parse HEAD`, re-checked at each phase). This report and
`claims/c1/VZ-1/*` (+ the mirror `claims/c1/verdict.md`) are this seat's only writes.
No git mutations; no LOG/SCORECARD/SHONEN/corpus/SKILL/PROVINCE/README edit; custody
paths read-only sha256-capture-only. Scratch: `/dev/shm/vz1` (see §5 — `/tmp` is
EDQUOT-broken on this host). One evidence id was minted by this seat (`ev_92b7e2fc…`,
§3/E6) — disclosed.

## 1. Work performed

- **Polled the wave** per the seat line: own 60 s loop, 18 logged samples
  06:57:33→07:15:xx (scratch log `/dev/shm/vz1/poll.log`, cleaned after use per the
  scratch rule — the sample count here is the evidence) plus targeted re-lists; the
  seats dir was empty at 06:56:39 and reached 45 other-seat reports by my close
  (46 with this one). No seat blocked on me; I never blocked waiting
  (`claims/c1/VZ-1/verdict.md` §header).
- **Reconciled every landed c1 seat output** into `claims/c1/VZ-1/verdict.md`
  (mirrored byte-identical at `claims/c1/verdict.md`, final sha256
  `75cc664a609fab4c06e69b2a14c42044b063737bd38cb510356c27c9ab4bc8aa`) — per-seat verdict
  table, evidence table C1-a…C1-i, debts D1-D9, integration conditions 1-4, attack log.
  (This report's own hash is not cited — it would be self-referential.)
- **Independently recomputed, first-hand** (not taken from reports): before-state
  recipe A at HEAD (§3/E1); keccak-256 selector sets for three carriers (E2);
  full parse of 7 probe envelopes incl. payloads/offsets/digests (E3); evidence-id
  re-derivation on 6 envelopes via `claims/c1/EX-09/reid.py` (E4); custody 5-path
  sha256 (E5); a fourth carrier compiled + probed by this seat (E6); the after-state
  applied twice on fresh scratch trees (E7); citation resolution for every path the
  entry cites (E8).
- **Closed the gap RV-1 named**: EX-03's `token.sol` landed only at 07:11 (after
  RV-1's polls closed, no compile artifacts, no report). I compiled it with the
  wave's solc and probed it → 9/9, `ev_92b7e2fc…` (§3/E6). Artifacts:
  `claims/c1/VZ-1/ex03-kdktoken-probe.json`, `…-expected.txt`.
- **Resolved two cross-seat discrepancies** rather than passing them through:
  (a) the entry-stem split (PL-1 plan `evm-solc` vs EX-12/EX-13/RV-3/RV-4/SC-3
  `evm-real-solc`) — resolved in the landed artifacts, plan text stale (D4);
  (b) RV-1's carrier-vs-decoded-digest conflation (`08299f31…` vs `530efc7b…`) —
  labeling defect, the envelope distinguishes the two (D5).
- **Caught a mid-wave artifact revision**: EX-12's entry patch changed under the
  wave (three applied identities observed: 8,598 B / 8,316 B / 9,513 B); its
  self-verification block and `recheck:` line are stale against the current
  revision, and CR-2 independently measured the `recheck:` line failing with
  EDQUOT (D9, integration conditions 3).

## 2. Proposed changes

- **`claims/c1/VZ-1/verdict.md`** (the deliverable; mirror `claims/c1/verdict.md`).
  It is a verdict document, not a repo patch. No patch text is proposed by this
  seat for any repo file: the c1 landings belong to EX-12/EX-13 (patch text already
  landed) and the round records to the parent. Concretely, my verdict *requires*
  three fixes to other seats' artifacts (CR-2's F1 `recheck:` line, the stale
  step-4 identity claim, one application of the duplicated README hunk) — those are
  named in the verdict's D9/integration conditions, not re-drafted here.
- Evidence artifacts written by this seat: `claims/c1/VZ-1/ex03-kdktoken-probe.json`,
  `claims/c1/VZ-1/ex03-kdktoken-expected.txt`, `claims/c1/VZ-1/applied-entry-copy.md`
  (rev-A applied entry, 8316 B, sha256 `f95c5a05…`).

## 3. Before→after measurement relevant to the chain claim

All commands run by this seat from the repo root unless noted.

**E1 — before (recipe A verbatim, `SCORECARD.md:92-124`, REV=`e845c2b…`):**

```
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
 "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}
```
Matches EX-11's landed artifact, RV-3, SC-2 and PL-1 (five independent captures).

**E7 — after (tree-level, run twice on two patch revisions):**

```
$ git -C <repo> archive HEAD corpus/knowledge corpus/README.md SKILL.md | tar -x -C /dev/shm/vz1/after
$ cd /dev/shm/vz1/after && git init -q . && git add -A && git commit -qm before   # f11b03de…
recipe A → {"knowledge_files": 81, "mapped": 81, "missing": [], "dangling": [], "rules": 13}
$ git apply ex12.patch        # rev A block sha256 4b569fb4…  → 03a263be…
recipe A → {"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
            "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
            "rule_blocks": 13}
$ git diff --name-only HEAD~1 HEAD
corpus/README.md
corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md
entry sha256 f95c5a05f0500ab9…  8316 B 31 lines

# rev B (current patch sha256 d662c195…, block 1bd7d54c…, mtime 07:14:01):
recipe A → {"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [], "rules": "13/13"}
entry sha256 a5119120ee6a6142…  9513 B 32 lines
```

**E2/E6 — independent selector recomputation (js-sha3, wave prefix):**
Smoke 5/5, Rv2Token 5/5, KdkToken (EX-03's source, compiled by this seat) 9/9 —
each selector present exactly once as a `PUSH4` dispatch immediate; the probe
recovered the same sets (`dispatch:"abi"` throughout, inferred args = the ABI's
parameter types). Rv2Token runtime 1943 B `c1081a56…`; KdkToken runtime 3457 B
`46ccaae1…`; probe `ev_92b7e2fc1dbccd5e…`.

**E4 — id re-derivation:** 6/6 MATCH (`ev_45849c8b…`, `ev_3aacd424…`, rerun-a,
`ev_d0d0b054…`, `ev_56d89cb4…`, `ev_c80379e1…`).

**E5 — custody:** 5/5 sha256 identical to CU-1's pre-pair at ~07:10-03
(`config.toml 8cbacd48…c38d`); no drift across the wave.

## 4. Attacks / refutations attempted (verdicts)

| Attack | Method | Verdict |
|---|---|---|
| probe output transcribed, not produced | re-derived 6 evidence ids from envelope bytes (E4) | **refuted** |
| selectors copied from a planted table | own keccak from ABI + PUSH4 scan; EX-07's independent disassembler | **refuted** |
| carriers hand-assembled, not compiler output | solc CBOR trailer `000825` + ipfs in every probed runtime (E3/E6) | **refuted** |
| after-state asserted, not measured | fresh tree, independent apply, 82/82 twice (E7) | **refuted** |
| map token breaks line-neutrality | 190→190, single-line diff, prior tokens byte-identical (E9/RV-4) | **refuted** |
| entry citations drift | all cited paths resolve (E8) | **refuted** |
| entry's identity claim is current | re-applied the current patch: 9,513 B ≠ claimed 8,316 B | **SUSTAINED** (D9) |
| EX-03's contract was never a real compile | compiled + probed it myself | **refuted** (9/9, E6) |
| the entry-name split would silently pass | CR-2's mismatch negative `001487c` shows missing+dangling; my E7 shows the matching pair is required | **refuted** (resolved in artifacts) |
| RV-1's report is fully accurate | found the carrier-vs-decoded digest conflation | **partially sustained** (D5, cosmetic) |
| PL-1's plan is current | stale entry stem + "16 criteria" count | **partially sustained** (D4/D8) |

## 5. Blockers / named gaps (partial evidence stands)

- **`/tmp` is EDQUOT-broken on this host** (my first scratch write failed with
  `Disk quota exceeded`; tmpfs 16 G at 80 %). Deviation: all scratch under
  `/dev/shm/vz1`, cleaned after use. Corroborated by EX-02, EX-06, RV-1, PL-1,
  CR-2 — it is a fleet-wide environmental hazard, not a seat error.
- **Seats that did not deliver at my close (07:19-03):** `SC-1` (no artifacts, no
  report), `EX-03` (source only at 07:11, no compile receipt/carriers/report — I
  closed the probe gap), `RV-3` (artifacts landed, report not written),
  `EX-14` (manifest churning, no report), `CR-1` (60+-file evidence dir + manifest,
  no report). `CR-2`'s report landed at 07:17 and is reconciled in the verdict.
  Gaps are named per-seat in the verdict's debts D1/D3/D6.
- **Not mine to fix:** the entry patch's stale self-hash and `cd /tmp` recheck line
  (D9) — the fix belongs to EX-12/CR-2 and the integrator.
- Residual for the parent: command A **at the records commit** is still owed
  (EX-15's `command-a-after.txt`); tree-level proof is E7.
