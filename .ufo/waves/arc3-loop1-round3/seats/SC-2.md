# Seat report — SC-2 (chain c1, role scribe)

Wave `arc3-loop1-round3` · 2026-10-19 · HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`
at every read (`git rev-parse HEAD`; repo untouched — `git status --porcelain corpus/
SKILL.md LOG.md SCORECARD.md` empty at each check). Writes by this seat ONLY:
`.ufo/waves/arc3-loop1-round3/seats/SC-2.md` (this report) +
`.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/{knowledge-entry-draft.md,
map-token-patch.md,records-drafts.md}` (the seat line's three files) + the mirror and
evidence set in `.ufo/waves/arc3-loop1-round3/claims/c1/SC-2/`. No git mutations; no
LOG/SCORECARD/SHONEN/corpus edits; custody paths never touched. Scratch:
`/var/tmp/sc2/` only (`/tmp` EDQUOT standing hazard).

## 1. Work performed (evidence pointers)

- **Before-state, re-measured first-hand:** command A (SCORECARD recipe, verbatim) at
  HEAD → `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
  "revision": "c07af80f…", "rule_blocks": 14}` (`SC-2/command-A-before.txt`); matches
  EX-14, RV-4, VZ-1, EX-04's independent captures.
- **The three drafts** (the deliverable; parent lands, nothing applied):
  - `records-drafts/knowledge-entry-draft.md` — the round's corpus entry, RESULT-class,
    modeled on the r1 entry, family-scoped, no availability→holding, Unknowns updated
    (the r1 "optimizer-enabled dispatch shapes" unknown narrows by measurement);
    literal text between markers; rev 3 folds the convergence seat's full carrier
    roster. Staging: the wave's c1 artifacts + the reused r1 solc prefix.
  - `records-drafts/map-token-patch.md` — line-neutral `corpus/README.md:38` patch
    (190 → 190; one line differs; token `2026-10-19-arc3-r3-evm-optimizer-shapes` =
    proposed entry stem), with apply recipe and verification obligations.
  - `records-drafts/records-drafts.md` — LOG entry draft + SCORECARD round-section
    draft (C1 bullets complete; C2/C3 parent-merge slots; pin-free voice).
- **Independent carrier/probe verification by this seat** (not copied from seats'
  prose): sha256 recomputation of every carrier file; envelope parsing of every r3 c1
  envelope (EX-10/EX-05/EX-07/EX-06/EX-04/VZ-1; schema note recorded); byte-level
  PUSH4 census + JUMPDEST check at every envelope offset; two fresh recheck runs
  (`npx rea-agents@6.4.0`, disk-backed `TMPDIR=/var/tmp/sc2/recheck-tmp`) — the r1
  canonical command re-derived `ev_45849c8b…` and the r3 opt200 command re-derived
  `ev_d409bd50…`, both envelopes byte-identical to the executors' captures.
- **Rehearsal (scratch-tree form of command A; deviation stated):** HEAD `git archive`
  → scratch tree; entry literal added + map token substituted → 82/82 → **83/83**,
  14/14, missing [], dangling []; prior-82 knowledge files `cmp`-identical; README
  190 → 190, single line. `SC-2/commandA-rehearsal-{before,after}.txt`.
- **Identity discipline (rule #14):** all draft hashes re-derived after the final
  revision (the post-rev-3 fold-in included): the canonical table is
  `SC-2/README-identities.txt` (entry file re-hashed there; patch `333ca590…` ≡
  RV-4's reviewed hash and unchanged across revs; records `f49aa9ee…`; rehearsal
  literal entry 37 lines / 17,563 B / `189ac2a2…`; rehearsal README after-state
  `016b632e…` ≡ RV-4's independent PRIMARY measurement). Drafts point at the
  table rather than embedding a self-referential hash (the file's own hash churns
  with every log edit by construction).

## 2. Proposed changes

**Patch-text artifacts (not applied; parent integrates):**
`claims/c1/records-drafts/knowledge-entry-draft.md` (→ a new
`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`),
`claims/c1/records-drafts/map-token-patch.md` (→ `corpus/README.md:38`, line-neutral),
`claims/c1/records-drafts/records-drafts.md` (→ `LOG.md` EOF append + `SCORECARD.md`
EOF section). Landing pairs to keep consistent: entry stem == map token; the
SCORECARD/LOG drafts' `⟨FILL⟩` slots filled from the wave's own C2/C3 records and
roster reconciliation, never from the declared 64.

**Named, not proposed as patch text:** the stale `PROVINCE.md:91-93` EVM frontier
bullet ("real solc/vyper-compiled bytecode untested" — doubly stale after r1 and r3);
recorded as carried debt in both records drafts. Protected file, outside this chain's
edit target.

## 3. Before → after measurement for the chain's claim (c1: EVM optimizer extension)

Commands (verbatim form):

```bash
REV=$(git rev-parse HEAD); python3 - "$REV" <<'PY' … recipe A … PY      # before
python3 /var/tmp/sc2/rehearsal.py /var/tmp/sc2/rehearsal/tree-pre       # before (tree form)
python3 /var/tmp/sc2/rehearsal.py /var/tmp/sc2/rehearsal/tree           # after  (tree form)
```

| side | knowledge_files | mapped | missing | dangling | rules | resolved | coverage/depth |
|---|---|---|---|---|---|---|---|
| before (HEAD, Git objects) | 82 | 82 | [] | [] | 14 | 14 | 10.0 / 10.0 |
| before (scratch tree form) | 82 | 82 | [] | [] | 14 | 14 | 10.0 / 10.0 |
| after (entry + token, tree form) | **83** | **83** | [] | [] | 14 | 14 | 10.0 / 10.0 |

Map token: 190 → 190 lines, exactly one changed line (`:38`), prior 82 tokens
identical; RV-4 independently measured the same (PASS; its strict-additive variant
also available). Probe on the patched trees: RV-4's rehearsal reads `findings=0
exit=0` in both modes at before/primary-after/honest-stop-after. Honest-stop branch
of the claim not needed: every probed runtime leg recovered its planted set K/K
(13/13, 11/11, 9/9, 8/8 incl. the falsification carrier, 6/6, 5/5 ×3 families),
zero missing / zero extra, `dispatch:"abi"`, offsets JUMPDEST.

## 4. Attacks / refutations attempted, with verdicts

- **A1 — falsify "zero extras" by PUSH4 sweep.** My byte census finds non-selector
  4-byte constants in the carriers (VaultB: `4e487b71`, `1309a563`, `1dc930eb`,
  `30cd7471`, `3c3332b9`; Rv2TokenOpt: `4e487b71`, `43000825`; the CarrierBErr attack
  carrier's planted custom errors). **Verdict: the probe reported none of them as
  functions — zero false positives holds at byte level; confirmatory, recorded in
  the entry.** VZ-1's independent matrix agrees per carrier.
- **A2 — r1's "each selector occurs exactly once as a PUSH4 immediate".** **Refuted
  on the binary-search dispatchers**: VaultB has `69fe0e2d` and `8da5cb5b` twice
  (GT pivot + EQ leaf), CarrierB has `8da5cb5b` twice. The entry carries the
  corrected wording; the tool still deduplicates to one function per selector.
- **A3 — treat the `ev_` id as content-addressed.** **Refuted by measurement:**
  identical bytes at different absolute paths mint different ids (carrier-A 3-way;
  VZ-1's recompiles/re-runs add VaultB/CarrierB/Rv2TokenOpt instances; EX-07's own
  6.4.0/6.7.0 legs at scratch paths vs VZ-1's repo-path run). Entry carries the
  family-scoped, formula-free claim; cross-seat citations compare by
  `subject.digest.sha256` + payload.
- **A4 — raw-on-hex-text trap (r1 class, new carriers).** EX-04's two legs reproduce
  it: exit 0, 0 functions, decoded sha == the hex text file's sha. **Verdict:
  parsed-and-empty, a probe-input trap, not a carrier defect; entry states it.**
- **A5 — stale province claim.** `PROVINCE.md:91-93` still says "real
  solc/vyper-compiled bytecode untested" after two real-solc rounds. **Verdict:
  genuine stale-statement debt; named in the records drafts (not silently fixed).**
- **A6 — self-identity audit of my own artifacts.** All three drafts were revised
  after their first writes; every hash re-derived at close; the rehearsal re-run on
  the rev-3 text (83/83 holds). **Verdict: no stale self-identity shipped (rule
  #14); the identity table is `SC-2/README-identities.txt`.**

## 5. Blockers

None for the seat task. Named gaps (landed after my rev-3 fold-in or outside my
artifacts): EX-04 ran no 6.7.0 leg (its own named residual); EX-12's `VaultA`
creation-code scratch traps and SC-1's separate compiles (Rv2Token opt0/opt200,
VaultCourt, KdxToken) are in the wave tree but not folded beyond VZ-1's matrix rows;
the c1 chain verdict (VZ-1's report) had not landed at my close — my drafts stand on
first-hand measurements and name that gap rather than assuming it. Delivery count,
custody post-pair, and C2/C3 record merges are parent-fill by design (slots marked).