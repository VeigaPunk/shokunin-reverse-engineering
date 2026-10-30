# CritTriV6 — R52-C2 pre-freeze attack (round 52, wave 1)

Subject: `plans/round-52-claims.md` R52-C2 at `ab0eafedc41402b43b41a4362084119578dfe7ce`
(triage table v6 as SKILL rule block 27, instrument `tools/round-52/sqfs-triage-v6.py`,
executability audit, embedded census clause). Read-only. Nothing built, committed, or run
against the lane; no REA, no downloads, no installs.

Receipts (all under `receipts/`, each with command, exit, UTC, stdout sha256):
- `probe_v6_attack.json` / `probe_v6_attack.receipt.txt` — `probe_v6_attack.py` (this seat), exit 0, out sha `630073ed…65369`.
- `census-coupling.receipt.txt` — registry-row simulation in a scratch clone at the claims base (base exit 0; after 7 round-52 rows exit 1).

## Answers to the four questions

1. **New row and envelope set.** `legacy-body-unreadable`/`preserve-unresolved` is an
   action that the vocabulary already holds, but the *label* overstates what is measured, and
   the row duplicates `no-reader-failure` (see F4, F5). The envelope change is exactly one
   pair: `{dmg_Z3_v3ddwrt_inode_table}` (P1). The other 125 labels do not move under the
   proposed condition (FAILED-only, P=0, `squashfs_v3_ddwrt` in HF). Verified from the envelopes
   and from `.ufo/waves/round-50/c3/c3-after.json`; it is the only FAILED envelope with ddwrt in F.
2. **Audit red-before for a reason other than ddwrt.** Yes, under the readings a builder would
   naturally take. The claimed before=1 holds only under one unfrozen mapping (F3).
3. **census_outside inside v6.** Scope creep and a claims-separability breach. It cannot be
   0 after landing without an unnamed census regeneration (F1). Keep census3.py as its own gate.
4. **`clean` on the two nopad `_ddefault` envelopes.** Not on valid grounds. No receipt shows
   any independent reader succeeded on those bytes; the receipts show the opposite. The residue
   is seven envelopes, not two (F2).

## Findings

### F1 — HIGH — The census clause in v6 makes C2 depend on C1, and cannot pass "after" as written
- Claim: v6 "embeds the census clause … reports `census_outside 0` at both before and after"; the
  claims also say the two claims are "verifiable without the other having landed".
- Evidence: at `ab0eafed` `census3.py --check` exits 0 (census_outside []). Adding the seven
  round-52 registry rows the claims require (`gap-rule.json`, `c1-counter.py`, `c1-controls.py`,
  `c1-run.sh`, `fetch-vendor.py`, `misroot-sweep.sh`, `sqfs-triage-v6.py`) with the census
  unchanged gives `registry_paths 63`, `census_outside` = all seven, exit 1
  (`receipts/census-coupling.receipt.txt`). The census artifact `tools/round-51/census3.json` is
  a snapshot at 96aee1a5; any new registry row flips it red.
- Consequences: (a) C2's "after" census clause is red unless a second census artifact is
  regenerated at the landing REV — the claims name none; (b) C2 now fails when C1 lands alone,
  breaching the separability sentence; (c) a registry snapshot is zero at its generating REV by
  construction (r51 CritTriV6 finding 5), so "census_outside 0" measures nothing new.
- Smallest fix: drop the census clause from the v6 predicate and audit; keep `census3.py --check`
  as the separate registry gate with its own receipt and ordering. If the clause stays, name a
  round-52 census artifact regenerated at landing, the landing order, and the separability
  exception in the claims text.

### F2 — HIGH — "Their readers succeeded" is false; the residue is 7 envelopes, not 2; the Z3 rationale is inconsistent with keeping `clean`
- Claim (R52-C2, last bullet): "The two clean ddwrt no-pad `_ddefault` envelopes keep `clean`
  (their readers succeeded; no route change)."
- Evidence:
  - P2 (`receipts/probe_v6_attack.json`, `P2_ddwrt_clean_residue`): seven envelopes with F
    containing `squashfs_v3_ddwrt` are `clean/none`: `dep_A2_squashfs_v3.be.nopad`,
    `squashfs_v3_ddwrt_squashfs_v3.{be,le}.{1kpad,4kpad,nopad}_ddefault`. Each subject digest
    maps to a NO-READER row in the round-50 census (`reader-census.txt`, sha bb539f02…).
  - Three of the seven are nopad (`be.nopad_ddefault`, `le.nopad_ddefault`, `dep_A2`), so the
    claim's "the two" omits one nopad residue and five 1kpad/4kpad residues.
  - The nopad bytes `daa8e72d355d…` (BE) and `e7482db480f9…` (LE) read `unsquashfs` 1 / `7z` 2 in
    `reader-census.txt`. The round-49 receipt `.ufo/waves/round-49/w1/C1ScribeEntry/v3-readers.out`
    records the same for `v3ddwrt-be--squashfs_v3.be.nopad.bin` (unsquashfs exit 1, 7z exit 2).
    No receipt in the tree records any independent reader succeeding on any ddwrt nopad
    envelope. What succeeded is sasquatch (the REA run).
- Inconsistency: Z3 is moved to `preserve-unresolved` because its bytes are reader-refused
  ("no reader, so no cross-read"). The healthy nopad bytes are refused by the same readers and
  stay `clean/none` ("match files to the oracle"). A reader refusal cannot be treated as
  disqualifying for the damaged body and as irrelevant for the healthy one.
- Verdicts and options. (a) Keep the seven `clean` only as a disclosed residue of the
  reader-backed family routing: state "sasquatch succeeded; no independent reader validated for
  this variant", name all seven, and accept that the routing is a choice. Scope stays one pair.
  (b) Move the seven to `clean-unverified`/`record-unverified` (step 15): eight pairs total, which
  is outside the one-pair scope and needs a claims amendment before freeze. Choose one and write
  it; the current text takes neither.
- Note: the Z3 "damaged" verdict is true by construction (the recipe zeroes bytes 144..203).
  The defect is the evidence basis for the verdict, not the verdict.

### F3 — HIGH — The audit's before=1 is reproducible only under one mapping the claims do not freeze
- Claim: "before 1 violation at `ab0eafed` over the v5 table bytes, after 0"; the audit reads
  "the frozen reader-census table from the round-49 entry, cited by block 26".
- Evidence:
  - P1 (`FAILED` envelopes): nine extractor-failure envelopes (`probe_v6_attack.json`, `P3`).
  - P3: no damaged subject digest has a row in the round-50 census, for any of the nine
    (`subject_has_census_row` false for all). Families `squashfs_v1` (dmg_Z1) and `squashfs_v2`
    (dmg_Z2) have no family row in that census at all. The census covers only the v3 families.
  - The round-49 entry (`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`) contains no
    per-fixture table (grep: no `family | fixture` table). Its only ddwrt statement is the
    no-pad refusal at line 104. The 6/7 family figure and the per-fixture rows exist only in
    `.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`, which is not under
    `tools/` or `corpus/` and which block 26 does not cite by path.
  - Under an exact-digest rule, all nine are "unknown"; under a family rule that lacks v1/v2,
    dmg_Z1 and dmg_Z2 are "unknown"; in both, the before count is not 1 and the after count can
    never reach 0 without a new table. Only the majority-family rule (ddwrt = no-reader, v1/v2/v3
    = reader-backed) gives 1 → 0, and that rule contradicts the v5 evaluator, which classes ddwrt
    as reader-backed (`READER_BACKED_V1V3`). The audit would then be a second authority for the
    same family.
  - Lineage (Z3 derives from the ddwrt nopad parent) lives only in
    `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json`, which is outside the
    envelope features the v5 evaluator reads ("a fixed function of the envelope's own tuple").
- Smallest fix: freeze a committed family→reader-status table (v1, v2, v2ns, v3, v3_ddwrt,
  v3_broadcom, v3_nonstandard, v4 rows) with provenance, the lineage rule, the audit scope (name
  the actions checked), and the missing-evidence rule. Recompute before=1 from that table and
  report the complete violation-ID set (the claims require it to equal the singleton).

### F4 — MEDIUM — The new row duplicates `no-reader-failure`, and the precedence is unspecified
- The v6 row (`legacy-body-unreadable`/`preserve-unresolved`) has the same action and the same
  cause text as `no-reader-failure`, applied to a family that the classification elsewhere keeps
  reader-backed. The result is two labels for one condition, distinguished only by family
  membership in two different cells.
- The one-pair result requires the new row to sit above `legacy-body-failure`, or the legacy
  cell to be narrowed to exclude ddwrt. The claims state neither. Under first-match, the outcome
  differs.
- Smallest fix: write the precedence (or the narrowed legacy cell) into the claims text, and
  state the new row as a failure-only exception with its own cause text, not as a reader-census
  consequence.

### F5 — MEDIUM — `legacy-body-unreadable` names a damage-like property the evidence does not show
- What is measured is reader refusal: `unsquashfs` 1 and `7z` 2 on the nopad parent (P4,
  `v3-readers.out`), and on the Z3 bytes (r51 CritTriV6 reconstruction, exit 1/2). "Unreadable"
  reads as a verdict on the body. The round-51 finding asked that the label not imply corruption.
- The claims also say the cross-read "cannot be executed". It can be executed; it returns
  refusal, and the v5 cause text maps refusal to "damage stands". The defect is an unsupported
  inference from refusal, not a non-executable action. The claims text overstates it.
- Smallest fix: rename to a reader-refusal label (for example `legacy-body-readers-refused`), and
  state the defect as an evidence-basis error.

### F6 — MEDIUM — The swapped-new-row-action kill control is vacuous as written
- P5: the new row's action (`preserve-unresolved`) is identical to `no-reader-failure`'s action.
  Swapping the two actions flips zero pairs. The v5 selftest rule says "none a no-op", so the
  control cannot be red, and the freeze would fail its own kill rule.
- Smallest fix: define the mutant as swapping the new row's action with `cross-read-legacy`,
  which flips the Z3 pair, and pin the expected flipped set in the selftest.

### F7 — MEDIUM — The reader-census table is not captured to the honest-capture standard
- `reader-census.txt` header shows `$ unsquashfs -version` and `$ 7z i`, but the per-row commands,
  per-row exit codes and per-row UTC are not recorded. Only the file's own sha and a payload sha
  appear. Block 26 cites the round-49 entry for this table, which does not contain it (F3).
- Smallest fix: recapture the 8-family × fixture matrix at landing with per-row command, exit,
  UTC and stdout sha, commit it under a frozen path, and cite it by path in block 27.

### F8 — LOW — The embedded v5 draft and the landed SKILL block differ in text
- `--print-v5-block` (embedded `V5_ROWS`) and the landed block in `SKILL.md` differ in leading
  indentation and prose in the `cause`/`source` columns. Scoring uses the condition and action
  cells, so the pairs are unaffected. I did not run a cell-level comparison. v6 should derive its
  baseline from the landed bytes, not from the instrument's embedded text.

### F9 — LOW — Circularity is disclosed but still shapes the claim
- The fixed evaluator, the v6 table, and the audit all read the same 126 envelopes that the v5
  rule was designed from. The claims disclose "depth, not held-out generalization". The v6 result
  says nothing about bytes outside the corpus.

## Verified, not contested
- The one-pair envelope set (P1) and its basis in `c3-after.json`.
- The base census (`census3.py --check` at `ab0eafed` exit 0; census_outside []).
- The nine FAILED envelopes and their v5 labels (P1/P3).
- The reader refusals on the nopad fixture bytes (`v3-readers.out` and `reader-census.txt`
  agree, and the nopad subject digests match the committed fixture bytes).

## Smallest safe correction set (ordered)
1. Drop the census clause from v6; keep census3 as a separate gate (F1).
2. Choose the residue option for the seven clean ddwrt envelopes and rewrite the premise (F2).
3. Freeze a family→reader table with lineage and an explicit audit scope; recompute before=1 (F3).
4. Specify the precedence and the failure-only exception for the new row (F4).
5. Rename the label to a reader-refusal label; fix the "cannot be executed" wording (F5).
6. Redefine the swap mutant so it flips a pair (F6).
7. Recapture the reader matrix with per-row capture (F7).
