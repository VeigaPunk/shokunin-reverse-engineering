# Records drafts — LOG.md entry + SCORECARD.md round-section (arc3-loop1-round4, C1 chain)

Seat SC-1 · chain c1 · role scribe · 2026-10-19. **DRAFT for the PARENT; NOT
APPLIED — neither `LOG.md` nor `SCORECARD.md` was touched by this seat.**
Revision 1 (~14:20Z). `⟨FILL: …⟩` / `⟨PARENT-FILL⟩` = parent-fill slots (the
producing seat or chain is named); the **C1 bullets and the C1 axis rows are
drafted complete from this seat's own first-hand measurements** (ledger §R2–R7,
`chain-ledger.draft.md` in this dir). The C2 and C3 slots are **not blanks** —
they name the landed sibling drafts this round, so the parent merges three
files rather than inventing text.

**Voice rules applied (r1/r3 precedent): pin-free on both sides.** No
`rea-agents@x.y.z` literal, no bare client-version literal (`6.x.y` form), no
absolute `path.json|toml|yaml:line` pointer, no client config filename
anywhere in the literal text below; artifact identities by sha256 fragment or
by file stem; the five custody paths are named as what they are — "three client
configs + two shell profiles". The SCORECARD side is census-scanned; the LOG
side is not today (same voice anyway — the r3/r4 precedent). Compiler versions
of the form `0.4.3` / `0.8.37` are outside the census's version-literal family
(that family is the client-version shape) and are safe; they are kept because
the entry's own claim is compiler-scoped.

**Merge map for the parent** (all three landed in this wave's tree):

| chain | LOG-side source | SCORECARD-side source |
|---|---|---|
| c1 (this file) | the literal block below | the literal block below |
| c2 | `claims/c2/records-drafts/LOG-entry-draft.md` | `claims/c2/records-drafts/scorecard-section-draft.md` |
| c3 | `claims/c3/records-drafts/LOG-entry-draft.md` | `claims/c3/records-drafts/scorecard-section-draft.md` |

Each of those files carries its own literal markers and its own parent notes;
the C1 slots inside them are the slots the text below fills. The cross chain's
`claims/cross/CN-2/project.py` is the mechanized fold for the SCORECARD side
(project the merged section onto a scratch tree, run the census, read the
verdict).

---

<!-- BEGIN LITERAL TEXT -->
### arc3-loop1-round4 — coverage: the Vyper compiler leg + freshness: PROVINCE surface staleness census + operability: custody residual closures (2026-10-19)

- Dispatch: 48 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  16 + 14 + 14 + 4, every name exactly once; the items-array assertion
  `len(items) == 48` held at dispatch, per the counting lesson). Lane: the hyper
  lane returned 402 out-of-credits on all 48 seats (zero delivered, ~30 s); per
  the round schedule's declared fallback and the operator directive the full
  roster re-dispatched on the devin lane — **recorded with cause and per-lane
  delivery counts, not a lane signal**. Delivered ⟨PARENT-FILL: N⟩/48 per the
  roster reconciliation (count the items array, never the intent).
- C1 coverage (owned) — the **Vyper leg** of the named Unknown "Vyper and solc
  versions other than 0.8.37" (the r3 entry's own Unknowns line). The round's
  one authorized install landed: `vyper` **0.4.3** in the wave-isolated venv
  (wheel `vyper-0.4.3-py3-none-any.whl` sha256 `3b967172…`, 403,104 B, four
  independent derivations across two seats and equal to the registry's own
  published digest; interpreter Python 3.14.7; the host has no system pip
  module and no pip on PATH — the venv was made with the stdlib module).
  Five Vyper carriers were compiled on-host with that compiler and probed with
  `inspect-evm-interface`: a fee/pause vault (K=15), a second independent vault
  (K=7), an ERC-20-bearing steward token (K=22), a four-mutability planner
  carrier (K=9) and the install smoke leg (K=4). **Every runtime leg recovered
  its planted set K/K — zero missing, zero extra, `dispatch:"abi"` on all** —
  across both pins and both encodings, against Vyper's own ABI-derived selector
  sets; the raw-on-hex-text and hex-on-rawbin traps reproduce as
  parsed-and-empty (exit 0, 0 functions, decoded digest equal to the input
  file's own), and creation-code legs are uniformly parsed-and-empty. Three
  measured deltas beyond K/K, each independently corroborated by three or more
  seats: (i) Vyper 0.4.3's dispatcher is a **third shape** — a modulo-indexed
  jump table (`bucket = selector % 13`, a 13-entry uint16 table copied from the
  runtime tail, three empty-bucket sentinel entries, then a fall-through chain
  comparing with XOR-equals-zero rather than the solc carriers' EQ/GT tree);
  (ii) the reported `bytecode_offset` on this family is **not a JUMPDEST** —
  0 of 15 land on one; each is the fall-through handler body at the compare
  site's push + 11, so the r1/r3 "offsets land on JUMPDESTs" reading is
  solc-scoped and was re-derived byte-for-byte on two carriers by this seat;
  (iii) the mutability inference reads payable for 8 of the 15 vault functions
  whose compiled ABI says view/nonpayable/pure (no case reads a more
  restrictive class; no selector misassigned) — an upstream-inference delta on
  this dispatcher family, recorded as observed, not as a defect. Zero false
  positives at byte level: the runtime's non-selector four-byte constants (the
  `Error(string)` revert selector, an ASCII fragment) were not reported, and
  Vyper's `method_identifiers` carries one phantom non-function key per carrier
  (`__default__()`) whose bytes do not occur in the runtime at all. The result
  lands as `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
  (RESULT-class, family-scoped, no availability→holding) + the coverage-map
  token **additive-only and line-neutral** (README 190 → 190, exactly one line
  differs); command A **83/83 → 84/84**, missing [], dangling [], rules 14/14,
  prior 83 byte-identical (this seat's scratch-tree rehearsal of the pair;
  ⟨PARENT-FILL: parent re-measure at the records commit from real Git
  objects⟩).
- C2 freshness (fleet) — ⟨FILL from `claims/c2/records-drafts/`: the PROVINCE
  Frontier + surface-summary staleness census run first-hand by the C2 scribe
  at HEAD with the committed instrument (baseline PASS `0/0/0/0`); **stale
  count 7 → 0**, each item repaired same-line as a patch text applied by the
  parent (PROVINCE 162 → 162 lines) or adjudicated NO-CHANGE with cause;
  cross-chain coupling recorded: the Frontier EVM bullet's repair wording
  cannot be frozen before C1's leg result is known — this round's leg HELD, so
  both halves of that bullet repair (the "untested" clause is retired, not
  re-stated); item (vii) (a false host-absence claim in a Core row) is outside
  the instrument's declared scope and the parent decides repair vs named
  debt⟩.
- C3 operability (fleet) — ⟨FILL from `claims/c3/records-drafts/`: the
  custody-pair residual closures with declared classes — the derived sidecar
  path now scope-checked (the pre-round spelling let a sidecar replace the
  measured file, reproduced first-hand by the C3 scribe on a scratch copy), the
  parent-directory creation moved inside the guarded write region (the raw
  traceback class is gone), the coverage gate now counts distinct paths rather
  than stanzas (a padded reference that examined nothing no longer reads clean),
  and the both-sides-absent MATCH semantics adjudicated with the ruling text
  landed; selftest 22 → ⟨FILL: n⟩ with the new fixtures plus sabotage arms; the
  registry row and README re-derived in the same commit; the round's live pair
  verifies MATCH 5/5 and every receipt self-pins the revised tool's sha256⟩.
- Custody: the five custody paths (three client configs + two shell profiles)
  stayed READ-ONLY (hash/stat capture only) for every seat this round; the
  clobber-attack demonstrations ran on scratch copies only. Pre-pair
  ⟨PARENT-FILL: capture path + utc + n/5⟩; post-pair ⟨PARENT-FILL⟩; in-window
  drift ⟨PARENT-FILL: state the measured comparison⟩. ⟨PARENT-FILL: C3's live
  pair receipts under the revised tool⟩.
- Process notes: scratch discipline `/var/tmp` + `/dev/shm` (host `/tmp`
  EDQUOT standing; every probe recipe carries a disk-backed `TMPDIR` — this
  round's own legs needed it again); the freeze's items-array assertion held at
  dispatch; the hyper-lane 402 was recorded with cause and the roster
  re-dispatched whole, so no seat slot is lost to the substitution.
  ⟨PARENT-FILL: any wave-caught defects the parent wants recorded⟩.
- Carried debt (named): the `ev_` id domain measured only as path-sensitive for
  this verb family (no formula); Vyper versions other than 0.4.3 and solc
  versions other than 0.8.37; the `viaIR` pipeline and optimizer runs other
  than 200; whether the payable-read inference delta and the
  `offset = push4_pc + 11` rule generalize to other Vyper versions; the
  r3/r4 census residual classes (H2/H4/H5/H6) and the custody residual set the
  C3 chain names; ⟨PARENT-FILL: C2/C3 residues⟩.
- Retired: ⟨FILL: none / named⟩.
- Scope: kaidoku repo only; no pushes; the round's one install is the wave-local
  venv; custody read-only.

## arc3-loop1-round4 — coverage + freshness + operability: ⟨FILL: verdict phrase, e.g. "three claims admitted"⟩, 2026-10-19

Round 4 of the reset window (4/10). Axis set: **coverage (owned)**,
**freshness (fleet)**, **operability (fleet)**; all three owned proxies remain
tied at 10.0 with none retired, so the owned claim was selected by the standing
most-falsifiable-next-claim tie-break. Claims are causally separable: a corpus
knowledge entry + map token, a set of PROVINCE surface repairs, and the custody
tool share no edit target. Roster frozen PRE-DISPATCH: 48 seats enumerated
mechanically (16 + 14 + 14 + 4, every name exactly once; the items-array
assertion held at dispatch). Lane: the hyper lane returned 402 out-of-credits
on all 48 seats (zero delivered); per the schedule's declared fallback and the
operator directive the roster re-dispatched on the devin lane — **recorded with
cause and per-lane delivery counts, not smoothed into a lane signal**.

- Wave: ⟨PARENT-FILL: reports path, work / wave-artifacts / records commits,
  delivery ⟨N⟩/48 per the roster reconciliation⟩.
- C1 coverage (owned) — **the Vyper leg of the compiler-family Unknown.** Five
  Vyper 0.4.3 carriers compiled on-host with the round's one authorized install
  (wave-local venv; wheel sha256 `3b967172…` with four independent derivations)
  and probed across two pins and both encodings: every runtime leg K/K, zero
  missing / zero extra, `dispatch:"abi"` — 15/15, 7/7, 22/22 (an
  ERC-20-bearing surface does not defeat the extractor on this family), 9/9 and
  4/4; traps reproduce as parsed-and-empty; creation legs parsed-and-empty.
  Three deltas measured and corroborated: a **third dispatcher shape**
  (modulo-indexed jump table + XOR compare chain), an **offset reading that
  does not generalize** (0 of 15 offsets are JUMPDESTs on this family; each is
  the compare site's fall-through body at push + 11 — the r1/r3 reading is
  solc-scoped), and a **mutability inference delta** (8 of 15 read payable
  against a view/nonpayable/pure ABI, one direction only). Zero false positives
  at byte level incl. a phantom non-function key in Vyper's own method
  identifiers. Landed as `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
  + the **additive-only line-neutral** map token (README 190 → 190, one line
  differs). Measured before → after: command A knowledge files **83/83 →
  84/84**, missing [], dangling [], rules 14/14, prior 83 byte-identical
  (⟨FILL: parent re-quote at the records commit⟩; this seat's scratch
  rehearsal of the pair reads 84/84 with the prior 83 byte-identical).
- C2 freshness (fleet) — ⟨FILL from `claims/c2/records-drafts/`: the surface
  staleness census — Frontier bullets and surface-summary claims each checked
  against admitted corpus state, stale 7 → 0, repairs as same-line patch texts
  (PROVINCE 162 → 162) applied by the parent, adjudications with cause, census
  PASS at the settled tree; the census PASS certifies locus hygiene, not claim
  truth, and the C2 draft's table is the certificate⟩.
- C3 operability (fleet) — ⟨FILL from `claims/c3/records-drafts/`: the four
  named residuals closed with declared classes and sabotage arms; selftest
  22 → ⟨n⟩; the absence ruling landed in the README; registry row + README
  re-derived same-commit; live pair MATCH 5/5; every receipt self-pins the
  revised tool sha256; command A unchanged⟩.
- Custody: the five custody paths stayed READ-ONLY (hash/stat capture only) for
  every seat; pre-pair ⟨FILL⟩; post-pair ⟨FILL⟩; in-window drift ⟨FILL: state
  the measured comparison⟩. Scratch on `/var/tmp` + `/dev/shm` (host quota
  hazard standing; every probe recipe carried a disk-backed TMPDIR).
- Measured at the records commit: command A ⟨FILL: quote the run⟩; probe
  selftest + findings ⟨FILL⟩; census ⟨FILL: verdict + the instrument's sha at
  read time⟩; custody selftest ⟨FILL: re-quote at landing⟩. The landed
  artifacts' fresh identities are recorded at landing, per the standing
  identity discipline (rule #14): ⟨FILL: entry file lines/sha256, README
  sha256, re-derived after the final write⟩.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | knowledge 83/83 → 84/84 (the Vyper compiler leg of the named Unknown recovered K/K on five carriers incl. an ERC-20-bearing one; zero false positives at byte level; three measured dispatcher/inference deltas recorded with their scope; proxy held at the larger denominator) | improved ⟨FILL: parent confirm⟩ |
| freshness — C2 | ⟨FILL from C2: PROVINCE stale count 7 → 0, repairs as same-line patch texts, census PASS at the settled tree⟩ | ⟨FILL⟩ |
| operability — C3 | ⟨FILL from C3: the four named residuals → declared classes; selftest 22 → n; live pair MATCH 5/5⟩ | ⟨FILL⟩ |
| depth | 10.0 → 10.0 (command A at the records commit) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: coverage — the compiler-family Unknown narrows by measurement
rather than by argument: a third dispatcher shape is now characterized
end-to-end (modulo-indexed jump table, bucket collisions resolved by an XOR
fall-through chain), and two readings that had been stated unconditionally are
now scoped to the convention they were measured on (the JUMPDEST offset reading
is solc-scoped; the mutability inference diverges one-directionally on the
Vyper family). The convergence across independent seats — the dispatch shape
was found by four seats from different starting points and the offset rule
proved byte-for-byte on two carriers by one seat and two more by another — is
the round's strongest agreement class. ⟨FILL: operability/freshness one-liners
from the C2/C3 records⟩. Planned: round 5 per schedule ⟨PARENT-FILL: lane per
the operator directive⟩. Carried debt (named): the compiler-family residues
(Vyper versions other than the one installed; solc versions other than the
r1/r3 pin; the `viaIR` pipeline; optimizer runs other than 200); the `ev_` id
domain for this verb family (path-sensitivity measured, formula not derived);
whether the payable-read delta and the offset rule generalize across Vyper
versions; ⟨FILL: C2/C3 residues⟩. Retired: ⟨FILL: none / named⟩.
<!-- END LITERAL TEXT -->

## Notes for the parent (not part of the drafts)

1. **C1 evidence basis** (all re-derived first-hand by this seat; full
   inventory in `chain-ledger.draft.md` and `SC-1/c1-inventory.txt`): command A
   before at HEAD = 83/83, 14/14, 10.0/10.0 (`SC-1/evidence/command-A-before.json`);
   five probe envelopes of this seat's own (`SC-1/evidence/probe-*.json`);
   scratch-tree rehearsal with entry + token = 84/84, 14/14, prior 83
   byte-identical (compared against RV-2's `prior-83.sha256`).
2. **The three draft files in this dir are the round's C1 record set.** The
   entry's literal text is between its markers in
   `knowledge-entry-draft.md`; the token patch is `map-token-patch.md`; the
   ledger is `chain-ledger.draft.md`. Entry stem
   `2026-10-19-arc3-r4-evm-vyper-leg` must equal the map token.
3. **Merge, do not paste over.** The C2 and C3 drafts named in the merge map
   above carry their own literal markers, their own parent notes, and their own
   measured pin-free simulations. This file's C2/C3 bullets are pointers, not
   substitutes; take their text from those files.
4. **What the parent must NOT take from these drafts without re-measuring:**
   any count at the records commit; the landed entry's byte-identity; the
   README after-state sha256; the census verdict; the custody pair. Carried per
   the wave's identity discipline (rule #14 — an unrun check has not passed).
5. **Delivery count and custody post-pair** come from the wave's own
   reconciliation artifacts (roster + receipts), never from the declared 48.
