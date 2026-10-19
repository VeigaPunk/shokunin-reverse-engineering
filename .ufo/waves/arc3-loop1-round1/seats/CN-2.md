# SEAT CN-2 — chain cross, role connector — records reconciliation (arc3-loop1-round1)

Wave: arc3-loop1-round1 | Date: 2026-10-19 | Repo HEAD at every sample:
`e845c2b524ad2e59871e004c51a1386e192a74ab` (immobile; this seat made no git
mutations, no repo edits outside its two allowed areas). Scratch: `/dev/shm/cn2-probe`
(host `/tmp` is EDQUOT-broken — the standing quota hazard; cleaned at close).

Status: **DELIVERABLE v5 COMPLETE** — the merged parent-records package outline is at
`claims/cross/records-outline.md` (sha256 `e0cc392f6ef012fadcf2e876907aafd926070ce3901e042cd6943ba292e40314`,
400 lines; hard-rule-directory copy at `claims/cross/CN-2/records-outline.md`).
SC-5's C2 records prose had not landed at report-write time — the ⟨C2⟩ prose slot stays
pending and is named below; the C2 after-state itself is measured and folded (EX-16's
guard landed and was independently verified), as is EX-28's census landing (which
supersedes SC-7's "re-key branch not taken" draft wording).

## 1. Work performed (each bullet with an evidence pointer)

- Read the frozen claims, roster, and seat rules: `claims-frozen.md:1-104` (three
  claims, cross-cutting rules, 64-seat roster).
- Captured the record-format authorities: LOG entries (`LOG.md:1258-1394`), SCORECARD
  round sections (`SCORECARD.md:636-702`, `:1220-1336`), round report skeleton
  (`.ufo/reports/arc2-loop1-round10/kaidoku.md`), SHONEN boxes (`SHONEN.md:5-12`),
  command-A recipe (`SCORECARD.md:86-124`).
- Mapped the instruments' couplings by reading them directly: `pointer-table.json`
  (13 exact/extracted entries + 4 quoted + 3 exempt; `readme22-*` pins target
  `corpus/README.md:22`, `readme175-*` target `:175`, `shonen-*` target `SHONEN.md:6/:12`,
  SCORECARD pins at `:59/:60/:68/:69/:72/:270/:622/:699`); `expected.json` (frozen-run +
  selftest case table, 11 cases); census v10 SCOPE ranges + unit/REA_GATE rules;
  README line map (`:38` EVM row, lessons table ends `:168`, frontier bullet `:175`).
- Folded the three chains' records material into the merged outline:
  - **C1** — SC-3 drafts (`claims/c1/records-drafts/LOG-entry-draft.md`,
    `SCORECARD-section-draft.md`), reconciled against the sealed legs:
    EX-05 (`claims/c1/EX-05/evidence-ids.txt`: `ev_4dd5ea20…` raw / `ev_2a79dd25…`
    hex, K=6), EX-06 (`run-hex-6.7.0.json` `ev_56d89cb4…` / `run-raw-6.7.0.json`
    `ev_9259f412…`), RV-2 (`probe-runtime-hex-6.4.0.json` `ev_45849c8b…`,
    `probe-runtime-raw-6.4.0.json` `ev_3aacd424…`, `probe-runtime-hex-6.7.0.json`
    `ev_19d7d3cb…`; `ex07-reconcile-rv2.txt` "ALL SOURCES AGREE"), EX-02 install patch,
    EX-13 map patch, RV-4 frozen verification (`frozen-verification.out`: VERDICT PASS).
  - **C2** — EX-16's LANDED real-target write (settled shas: probe `e2665074…`,
    expected `ff47bfd6…`, table unchanged `738b3a56…`; `git diff` +11/-1 probe, +1/-1
    expected) + coupling material: SC-4 `changeset.md` §1/§5 (targets A–E, token
    reconciliation, re-pin coupling), EX-20 registry-row patch (verified by SC-4 §3),
    RV-6 harness/§4 (silent-rc-0 matrix), EX-25 before battery
    (`logs/before-{selftest,probe,sha256,strict}.txt`), EX-16 before/after captures
    (`before-tampered-silent.txt`: emptied table ran silent `findings=0 exit=0`).
  - **C3** — EX-28's LANDED census edit (settled sha `6f1d19ff…`: disposition stanza +
    one stale marker row re-keyed `PROVINCE.md:45-62` `:40`→`:45` + G18 added), plus the
    drafting chain: SC-6 `e22-disposition.draft.md` §6 (P1/P2), SC-7 literal drafts
    (`claims/c3/SC-7/{log-entry,scorecard-section,census-header}-draft.md`; simulation
    §3: PASS + planted-locus FAIL undeclared=1), EX-26 census capture, EX-26 patch text.
- Produced the merged outline (v1 → v3) with: package inventory (R1–R10), commit
  sequence + gate order, merged LOG entry, SCORECARD section order + merged bullets,
  report skeleton, the consistency contract (numbers / pin couplings / digest
  couplings / census gate), merge-slot map, gaps, environment notes.
- Independent checks at HEAD (own runs, `PYTHONDONTWRITEBYTECODE=1`,
  `TMPDIR=/dev/shm/cn2-probe`):
  - probe normal: `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`
  - probe selftest: `CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0`
  - census v10: `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0
  - command A (recipe extracted verbatim from `SCORECARD.md`, script sha256
    `e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247`):
    `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
    "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
    "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}`
- After-state verification at the SETTLED worktree (EX-16 + EX-28 landed; every run
  re-done after the writers stopped):
  - probe selftest: `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`
  - probe normal: `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`
  - tampered table (one byte flipped in a /dev/shm copy):
    `pointer_table_tampered … CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2`
  - absent table → `pointer_table_unreadable … exit=2`; unpinned expected →
    `pointer_table_unpinned … exit=2`; `--strict` clean → `clean findings=0 exit=0`
  - census v10 (post-EX-28): `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0
    unresolved=0)`, exit 0

## 2. Proposed changes

- **Deliverable (not applied to any real target):**
  `.ufo/waves/arc3-loop1-round1/claims/cross/records-outline.md` (v5, sha256
  `e0cc392f…`; copy `claims/cross/CN-2/records-outline.md`). This is the merged
  parent-records package outline the parent executes at integration.
- No patch text of my own for `LOG.md` / `SCORECARD.md` / `corpus/` — the pasteable
  blocks referenced in the outline are the chains' own drafts (SC-3, SC-7; SC-5's
  prose pending) plus EX-16/EX-28's landed edits, assembled there.
- No other file created or modified; no git mutations.

## 3. Before→after measurement (cross/records claim)

- **Before:** no merged records package existed — three chains' material scattered
  across `claims/c1/records-drafts/`, `claims/c3/SC-7/`, `claims/c3/SC-6/`, and
  `claims/c2/SC-4/changeset.md`; no single spec for LOG/SCORECARD/report ordering, no
  consistency contract for numbers/pins/digests.
- **After (v5):** one outline carrying §1 inventory (R1–R10), §2 commit sequence +
  post-commit gate order (+ the writer-settle rule), §3 merged LOG entry (C1 + C2 +
  C3 after-states folded; SC-5 prose slot), §4 SCORECARD section order + merged
  bullets, §5 report skeleton, §6 consistency contract (10 number rows; 6 pin groups;
  4 digest couplings; census gate; the resolved row-token substitution), §7 merge-slot
  map (C1 LANDED, C2 after-state LANDED/prose pending, C3 LANDED + wording
  correction), §8 gaps, §9 environment notes.
- Counting commands: `wc -l` → 400 lines; `sha256sum` → `e0cc392f…`; slot statuses:
  C1 + C3 landed, C2's after-state landed with prose pending. (The round's claim
  measurements themselves are the parent's records-commit runs; the outline only fixes
  where they land and how they must agree.)

## 4. Attacks / refutations attempted, with verdicts

1. **"The map-token edit is line-neutral"** — checked the delivered patch and RV-4's
   harness: 190→190 lines, tokens 81→82, prior 81 byte-identical, applied sha
   `b74b8d34…`; the row-insert counter-case (`README.rowinsert`, 191 lines) would
   break the three `readme175-*` pins. **Verdict: confirmed; in-place edit is the
   only pin-safe shape.**
2. **"Append-only records keep all probe pins valid"** — checked each pin's line
   against the append points (SCORECARD pins ≤`:699` vs append ≥`:1337`; LOG pin
   `:1012` vs append ≥`:1395`; SHONEN pins vs no SHONEN edit planned). **Verdict:
   holds, provided R6 stays line-neutral and the axes table (`:19-33`) is untouched.**
3. **"SC-3's C1 before-numbers match the sealed evidence"** — my independent command A
   run reproduces 81/81, 13/13, missing [], dangling []; RV-2's `ex07-reconcile-rv2.txt`
   pins the runtime sha `c1081a56…` on all three probe legs. **Verdict: match.**
4. **"SC-3's canonical leg choice is complete"** — **partially refuted**: SC-3's drafts
   cite the Rv2Token legs only; the KdxToken legs (EX-05 `ev_4dd5ea20…`/`ev_2a79dd25…`,
   EX-06 `ev_56d89cb4…`/`ev_9259f412…`, both re-run byte-identically by RV-2) are also
   sealed. Flagged in outline §3/§7/§8 as a parent citation-set choice; R1/R2/R3 must
   match whichever set is cited. **Verdict: discrepancy recorded, not resolved here.**
5. **"The records append is census-safe"** — SC-7's records-tree simulation (PASS;
   planted tail locus → FAIL undeclared=1) plus my census run at HEAD (PASS 0/0/0/0).
   **Verdict: constraint confirmed live; the merged text must stay locus-free in the
   census unit (pin-free discipline in SC-7's draft notes).**
6. **"C2's before-state is 11/11 + findings=0"** — independently reproduced by my own
   probe runs at HEAD. **Verdict: confirmed.**
7. **"EX-16's guard closes the silent path"** — verified against the SETTLED landing:
   selftest 13/13; normal findings=0; injected tampered/absent/unpinned each exit 2
   with the declared finding ids; the pre-state silent-clean gap reproduced from
   EX-16's own capture. **Verdict: confirmed; the row-text substitution
   (`table_tampered` → `pointer_table_tampered`) is folded into §6.3.**
8. **"Gate runs are valid whenever the files exist"** — refuted twice in-wave: a
   selftest read during EX-16's write failed 12/13, and a census read during EX-28's
   write failed G18 — both re-ran clean once writers stopped. **Verdict: mid-write
   races are real; the outline's §2 now carries the writer-settle rule.**
9. **"SC-7's C3 wording survives the landed instrument"** — refuted: EX-28 found one
   stale marker row (`PROVINCE.md:45-62` dated itself by `:40`) and re-keyed it + added
   G18, so the re-key branch WAS taken; SC-7's "not taken" sentence is superseded.
   **Verdict: correction folded into outline §3/§4/§7/§8 — the records must state the
   marker re-key, nothing retired.**

## 5. Blockers (partial evidence still delivered)

- **SC-5's C2 records prose not landed** at report-write time — the ⟨C2⟩ prose slot in
  §3/§4/§7 remains; the after-state is measured and folded (EX-16 + the §6.3
  couplings), so the fold is mechanical.
- **C1 knowledge-entry patch undrafted by any seat** — no seat may write `corpus/`;
  the parent must author `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` from
  the sealed evidence; entry + token must land in the same commit (dangling pre-flight
  measured by EX-13).
- **Delivery count (VZ-4 roster reconciliation) and post-pair custody (CU-1) pending** —
  their slots are named in §3/§7.
- **EX-16 and EX-28 landed in the worktree but are UNCOMMITTED** — the parent commits
  them; gate re-runs must follow the writer-settle rule (see §4 attack 8).
- Host `/tmp` EDQUOT (standing hazard, `SCORECARD.md:991`) — scratch relocated to
  `/dev/shm`; no evidence lost.
