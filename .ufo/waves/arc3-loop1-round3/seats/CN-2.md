# SEAT CN-2 — chain cross — connector — late join (arc3-loop1-round3)

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Task as given: LATE JOIN —
verify or complete `claims/cross/records-outline.md` (merge the chains'
records-drafts into one parent-records outline enforcing PIN-FREE discipline;
run the census against a projection with the drafted SCORECARD sections
appended).

Writes by this seat: this report; `claims/cross/records-outline.md` (revised
v1.3 → v1.4, see §1); `claims/cross/CN-2/**` (2 new receipts + 10 v6/v7 fold
receipts + refreshed late-join receipt + refreshed identity.txt). Scratch
`/dev/shm/cn2r3*`; `/tmp` never written. No git mutation. Custody paths
read-only (sha256/stat + `verify` reads); the collision demos ran on scratch
clones only. No LOG/SCORECARD/SHONEN/corpus/SKILL/README edit — proposed
changes are patch texts under the chains' trees (referenced, not authored by
this seat) and the outline itself.

## 1. Work performed (evidence pointers)

**Inputs read first:** `claims-frozen.md`; the pre-existing
`claims/cross/records-outline.md` (v1.3 `0c9d3a52…` full
`0c9d3a529eceb4fdf5f0d75102af818d9ed0f010874b1390bd270b5c1f5a39ca`, 22679 B,
310 L — re-hashed before the first edit) and `claims/cross/CN-2/**`; the three
chains' literal drafts; the landed instruments; `claims/cross/CN-1/consistency.md`
and `claims/cross/CN-1/receipts/latejoin-collision.txt`.

**Disposition — VERIFIED + COMPLETED (both, explicitly):**

- The pre-existing connector package was **verified**: the v1.3 merged texts
  existed, the fold script existed, the v4/v5 receipts existed. **But the v5
  fold was stale**: C2's drafts were revised after it (mtime evidence: v5 fold
  13:17Z; C2 SCORECARD block revised to 13:26–13:28Z; LOG block to 13:28Z).
  A chain revision voids the earlier projection receipt (the outline's own
  §7.1 rule), so re-fold was **COMPLETED**: v6 fold (13:24Z, after the
  token-plan-lane interruption) then v7 fold (13:29Z, after C2's last
  revision). The fold script's placeholder normalizer was extended
  (`assemble-merge.py` v4: `⟨PARENT: …⟩` accepted alongside
  `⟨FILL⟩`/`⟨PARENT-FILL⟩`; a new form still fails loudly at exit 1).
- All gates re-run on the v7 texts (PIN-FREE CLEAN; projection PASS 0/0/0/0;
  injection control FAIL undeclared=1; SKILL-row projection PASS).
- The outline was **COMPLETED to v1.4**: every identity/number re-derived at
  write time (rule #14); the R1–R8 inventory, §2 commit sequence, §3/§4 body
  counts (200 + 194), §6.1 single-source table, §6.2, **new §6.5 landing-order
  collision**, §7 slot map, §7.1 fold timeline (v6/v7 rows), §8 recipe (inline
  extractor + coupling step), §9 risks, §10 receipt index, §11 cross-reference.
- **The round's substantive finding — the §6.5 collision — was measured and
  the fix independently verified** (§4 below).
- Every landed claim in §6.1 was **re-derived, not quoted** (§3 below).

**New receipts** (`claims/cross/CN-2/receipts/`):

| file | what |
|---|---|
| `v7-fold.txt` | the current fold: source/segment shas, merged identities |
| `pin-free-merged-v7.txt` | PIN-FREE checker on both v7 bodies (`--units`) |
| `merged-projection-v7.txt` | v7 section appended to HEAD copies → census PASS 0/0/0/0 |
| `merged-injection-control-v7.txt` | same + planted pin → FAIL undeclared=1 (live test) |
| `skill-row-projection-v7.txt` | EX-30 v2 row applied + v7 section → PASS 0/0/0/0 |
| `collision-probe-patched.txt` | §6.5: real probe over patched-row clone → findings=1; HEAD control → 0 |
| `ex32-reanchor-verification.txt` | EX-32 digests re-derived; landed pair 1 finding vs re-anchor pair 0 at the full projection; teeth; tightened-variant table |
| `latejoin-v14-reverification.txt` | one transcript: command A, probe ×3, F3 coupling, custody selftest + live pair, C1 rehearsal, census |
| `identity.txt` | rule-#14 re-derivation of all 32 artifacts in this seat's tree (re-derived after the final edit) |
| v6 set (`v6-fold.txt`, `*-v6.txt`, `merged-*-body-v7.md` staged bodies) | fold provenance (v6 superseded by v7; bodies staged for the parent) |

## 2. Proposed changes (patch-text paths)

- **The outline is itself the parent-facing artifact** (not a patch): R1/R2
  pasteable texts at `claims/cross/CN-2/merged-LOG-entry.md` +
  `merged-SCORECARD-section.md` (v7 fold), preflight recipe §8.
- **None authored by this seat.** Referenced patch texts (chains' own, not
  mine): `claims/c2/EX-30/registry-row.patch.md` (v2, SKILL.md row),
  `claims/c2/EX-32/pointer-table-reanchor.patch.md` (§6.5 repair),
  `claims/c2/EX-32/proposed-tightened-anchor.md` (optional strengthening),
  `claims/c1/records-drafts/map-token-patch.md` (PRIMARY additive-only),
  `claims/c1/records-drafts/knowledge-entry-draft.md` (rev 3).

## 3. Before→after measurement for the chain's claim

The cross chain's deliverable is the merged records package; the measurable
gates at v1.4 (all re-run by this seat; receipts in §1 table):

| gate | before (v1.3/v5 state) | after (v1.4/v7 state) |
|---|---|---|
| merged section | 198 L `4db10215…` (v5 fold) | **213 L `83772cc4…`** (v7 fold) |
| merged entry | 192 L `9ca628e2…` (v5 fold) | **207 L `6e20b662…`** (v7 fold) |
| PIN-FREE | CLEAN (v5 bodies) | **CLEAN** (v7 bodies; 1 census-reachable unit in the section, classifies clean; 0 in the entry) |
| census projection (section appended) | PASS 0/0/0/0 (v4) | **PASS 0/0/0/0** (v7); injection control FAIL undeclared=1 (live) |
| SKILL-row + section projection | PASS (v4) | **PASS** (v7; row diff applies cleanly to HEAD → `03832723…`, matching EX-30's claim) |
| collision status | unmeasured by this seat at v1.3 | **measured: findings=1 with the landed pair + patched row; 0 with EX-32's re-anchor** (§4) |
| landing rehearsal (C1) | 83/83 (quoted from the chain) | **83/83 re-derived** + prior-82 slice byte-identical (82/82 files checked, 0 differing) |

Side-harm checks at v1.4 (all unchanged/clean): command A at HEAD 82/82,
14/14, 10.0/10.0; probe selftest 13/13, findings=0 both modes at HEAD; F3
coupling MATCH (`bfc42f1b…` = pin; expected `d97dd60a…`); custody selftest
22/22; live pre/post pair MATCH 5/5 in receipt-vs-live ×2 and pre-vs-post,
`--require-paths 5` each; census PASS at HEAD.

## 4. Attacks/refutations attempted, with verdicts

1. **Stale-fold attack (the interruption's residue).** Hypothesis: the v5
   merged texts still represent the chains' latest drafts. **Refuted** — C2
   revised its blocks after v5 (source shas moved `9858a850…`→`93b221ca…`,
   `ba95eba0…`→`f445a993…`); re-fold to v7 required, gates re-run.
2. **The §6.5 collision (adversarial cross-chain read).** Hypothesis (CN-1's
   §3g, independently re-tested here with the **real probe**, not an
   evaluator): C2's row patch + C3's landed table → findings=1. **Confirmed**:
   scratch clone rev `a13940f7` (patched SKILL.md `03832723…`) → `citation_dead
   entry=skill-registry-custody-pair-row`, failed exit 1; HEAD control 0; full
   work-commit projection (rev `da8ed548`) → same single finding.
3. **Fix validation (EX-32's re-anchor).** Applied their diff to the landed
   table → `a810bd17…` re-derived byte-exactly; expected re-pin → `e33f0e2d…`
   re-derived (only the digest string changes in the single-line JSON).
   **Probe over the full projection with the fixed pair: clean findings=0.**
   Verdict: the fix works as claimed; must land same-commit with the row.
4. **Fix non-vacuity (teeth).** Reordered-precedence mutant (rev `a1b0efab`)
   under the alternation anchor → `citation_dead`, failed exit 1. Verdict: the
   re-anchor does not neuter the entry.
5. **Tightened variant (§3 of EX-32).** Re-ran their discrimination table:
   `MATCH > UNEVALUABLE;` tail passes §2, fails §3-tightened; both real rows
   pass both. Verdict: §3 closes an inherited substring laxity; parent applies
   §2 or §3, never both.
6. **EX-32's stale citation.** Their §4 cites patched SKILL.md `8efd8a87…`
   (EX-30's v1 emission; CN-1's receipts used the same). **Refuted as
   load-bearing**: the v2 patch applies to `03832723…` and carries the
   identical precedence clause; my collision runs used the v2 output directly.
7. **Re-serialization hazard.** First fix attempt re-serialized
   `expected.json` (85 lines vs the landed single-line compact form) —
   **rejected and redone** as an in-place digest-string replacement so the F3
   "only the pin changes" property holds byte-for-byte (verified by character
   diff: 62 byte positions, all inside the 64-hex digest).
8. **Placeholder-form attack.** New `⟨PARENT: …⟩` form in C2's 13:28Z
   revision → fold exits 1 (fail-loud). Extended normalizer; re-fold clean;
   no raw angle brackets can reach the pasteable blocks (checker enforces).

## 5. Blockers

None for this seat's deliverables. Carried risks (parent-facing, all named in
outline §9): the §6.5 collision is **open until the re-anchor lands in the
same commit as the row** (the parent's landing call — options enumerated in
EX-32 §5); C1's work remains unlanded (83/83 is a rehearsal; land then
re-measure); chain churn may post-date the v7 fold (re-fold = §8 step 0, one
command); `__pycache__/` under `.ufo/gates/` must be excluded from commits;
the pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` is not this
round's.

**Status: COMPLETED missing work (re-fold v6→v7, outline v1.4, collision
measurement + fix verification, receipts) AND VERIFIED existing work
(all §3 rows re-derived first-hand, not quoted).**
