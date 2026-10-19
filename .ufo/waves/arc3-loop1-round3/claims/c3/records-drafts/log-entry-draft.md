# LOG.md entry draft — C3 records (SC-5, arc3-loop1-round3)

Seat SC-5 · chain c3 · role scribe · 2026-10-19. **Draft for the PARENT; LOG.md
was not touched by this seat.** Append at EOF (after the `arc3-loop1-round2`
entry, which ends `LOG.md:1455`; HEAD at draft time `c07af80`, file 1455 lines).
`⟨…⟩` = parent-fill slots; the **C3 bullet is drafted complete** with the
wave-start baseline measured by this seat; values that only other C3 seats can
produce are marked `⟨FILL: …⟩` with the producing seat named.

LOG.md is not census-scanned (its SCOPE table names only `PROVINCE.md`,
`SKILL.md`, `SCORECARD.md` — `.ufo/gates/c1-census-v10.py:215-236`), and an EOF
append shifts no line, so no pin moves. The SCORECARD-side section for this
round is drafted in `scorecard-section-draft.md` (same directory) and **is**
census-scoped past the declared bound: it is written pin-free and measured with
the instrument (see that file §3). This draft keeps the same pin-free voice for
consistency (no client version literal, no `@`-pin, no `path:line` pointer into
an operator-mutable file).

## Literal entry text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL ENTRY TEXT -->
### arc3-loop1-round3 — EVM optimizer dispatch shapes + custody-pair hardening (D2/D3/write-guard/D6) + citation-drift table extension (2026-10-19)

- Wave: 64 seats frozen PRE-DISPATCH (roster = the round's `claims-frozen.md`;
  items array == roster, the r9/r10 assertion held before dispatch);
  `alibaba-token-plan/deepseek-v4.1-flash` — the deepseek-v4.1-flash swarm
  waves ride the token-plan lanes per the operator directive recorded in the
  round-2 records and ledger (round 3 = token-plan key 1 of 3). Delivered
  ⟨PARENT-FILL: N⟩/64 per the roster reconciliation (count the items array,
  never the intent).
- C1 coverage — EVM family extension, optimizer-enabled dispatch shapes:
  ⟨PARENT-FILL from the C1 records draft (`claims/c1/records-drafts/`): the
  optimizer-enabled carrier and the non-ERC-20-shaped carrier, compiled on-host
  with the reused receipted wave solc prefix, planted selectors recovered K/K
  with zero extras, the landed corpus knowledge entry + line-neutral map token,
  and command A re-measured 82 → 83 with the prior 82 byte-identical⟩.
- C2 operability — custody-pair hardening (D2 + D3 + write-guard scope + D6):
  ⟨PARENT-FILL from the C2 records draft (`claims/c2/records-drafts/`): the four
  injections reproducing as their declared exit classes (no fail-open MATCH; the
  EACCES path declared; verify coverage declared; the write-guard extended to
  the scoped set union the custody set; the selftest scratch-guard → USAGE);
  selftest 15 → ⟨N ≥ 17⟩ at exit 0; registry row + README updated in the same
  commit; the round's live pre/post pair verifying MATCH 5/5; v1 receipts
  sha256-verifiable; every receipt self-pinning the revised tool's digest⟩.
- C3 freshness (fleet) — citation-drift pointer-table extension to the arc3-era
  citations. **Wave-start baseline measured independently by this scribe at
  `c07af80`** (matches the chain's own before-receipt EX-44 byte-for-byte, two
  separate runs): table `.ufo/gates/citation-drift/pointer-table.json` sha256
  `738b3a56…` carrying 31 entries (+4 quoted, 3 exempt); `expected.json` sha256
  `ff47bfd6…` pinning the table digest; probe `.ufo/gates/citation-drift/
  citation-drift-probe.py` sha256 `e2665074…`; probe findings 0 in **both**
  modes (`reported` rc 0 / `--strict` `clean` rc 0); selftest 13/13 exit 0;
  command A 82/82, rules 14/14. The named gap (round-1 C2 note + the round-10
  extension precedent): the 31 entries did not cover the arc3-era in-repo
  citations — the round-1 EVM knowledge entry and its map row, the arc3
  scorecard sections' pinned needles where applicable, the round-2 registry
  rows, and the custody receipt conventions.
  Landed at the work tree (EX-41; re-measured by this scribe): entries
  31 → 57 (+26 added, none removed), quoted unchanged (4), exemptions 3 → 8 —
  the NO-ENTRY causes materialized (append-only round reports; wave-internal
  provenance as a class; the five operator paths, which rule #11 forbids
  pinning; current-state count tokens; LOG prose) — with every pinnable arc3
  citation table-covered or NO-ENTRY with cause per the r10/r4 precedent
  (EX-41 `claims/c3/EX-41/03-census-dispositions.md` maps each row; the census
  surface is the four arc3 r1/r2 commits' non-wave added lines; one measured
  stale row is a round record's citation — `SKILL.md:371` moved to `:389`
  when round 2 inserted the rule-#14 block; adjudicated NO-ENTRY as an
  append-only round record, not repaired). The table digest is re-pinned in
  the expected-values file in the SAME commit (the F3 coupling) — measured:
  its only change is the pinned table digest, from `738b3a56…` to
  `bfc42f1b…` (expected-file sha256 `d97dd60a…`, re-derived after EX-41's final
  rewrite of that file at 13:13:28Z — an earlier measurement in this draft read
  a mid-window revision `179db3c7…` and was corrected by re-derivation per rule
  #14); the frozen-run revision,
  verdict and expected finding, the snapshot digest and the 13-case selftest
  table are byte-unchanged, and the frozen-run baseline was re-derived at its
  pinned revision (`failed findings=32 exit=1` with the expected
  `citation_dead` present — `06-frozen-run.txt`, 13:12:50Z).
  Post-landing measurements (this scribe, independently + EX-41
  `04-after-probe-and-selftest.txt`): probe findings 0 in both modes at the
  work tree; selftest 13/13 unchanged; digest re-derivation MATCH through
  EX-46's independent check tool; tamper checks re-run — a byte-changed table,
  an absent table, an unpinned baseline and a dead revision each hit
  could-not-evaluate exit 2 (`08-tamper-checks.txt`); command A unchanged
  (82/82, 14/14, 10.0/10.0, measured against the pre-round commit archive).
  Attacks attempted with verdicts: the extension has teeth where the old table
  was blind — at the same real drift revision the 31-entry table reads clean
  while the extension reports 2 dead citations (EX-43
  `drift-blind.txt`/`drift-caught.txt`); a needle+pointer mutation battery
  reddens every new entry (EX-41 `07-nonvacuity.txt` — "OK" on every case,
  rc 1, `citation_dead`); a neutered needle reports rather than repairing
  (EX-44 `neuter-proof.txt`); a stale pin and a one-byte tamper each exit 2
  (EX-46 simulations). ⟨FILL: RV-11/RV-12/CR-5/VZ-3 verifier confirmations and
  any residual they raise — not all landed at this draft's last poll⟩. Scribe
  cross-check (not the chain's verification): an independent append simulation
  of the round's scorecard section measured 0 new census loci, PASS 0/0/0/0,
  with a planted-pin control FAILing (see
  `claims/c3/records-drafts/scorecard-section-draft.md` §3).
- Custody: pre-pair ⟨PARENT-FILL per CU-1: capture time, 5/5, receipt path⟩;
  post-pair ⟨PARENT-FILL⟩; in-window drift ⟨PARENT-FILL: expected none — state
  the measured comparison; if the operator-side churn class fires again, record
  it verbatim and do not repair⟩. All five custody paths stayed READ-ONLY for
  every seat (hash/stat capture only).
- Carried debt (named): ⟨PARENT-FILL C1/C2 merges⟩; C3 adds: no landed-and-open
  table rows — the census's NO-ENTRY row-groups are adjudicated in the table's
  exemption ledger (part of the table, not debt); ⟨FILL: any residual the
  verifier seats measured; if none, say so and keep the probe's own standing
  exemptions named⟩. Standing: the host `/tmp` quota exhaustion
  (recipes must carry disk-backed scratch); the pre-existing dirty
  `.ufo/waves/arc2-loop1-round10/C3.md` (not this round's).
- Scope: kaidoku repo only; no pushes; no installs this round (C1 reuses the
  round-1 receipted compiler prefix — record the reuse); scratch under
  `/var/tmp` or `/dev/shm` (`/tmp` quota-exhausted — standing).
<!-- END LITERAL ENTRY TEXT -->

## Notes for the parent

- The C3 bullet's numbers are **measured** (SC-5): the wave-start baseline at
  HEAD `c07af80` (corroborated byte-for-byte by EX-44's before-receipts
  `claims/c3/EX-44/before-probe.txt` + `before-selftest.txt`) and the
  post-landing block re-measured at the work tree after EX-41's landing
  (corroborated by EX-41's own `04-after-probe-and-selftest.txt`,
  `06-frozen-run.txt`, `07-nonvacuity.txt`, `08-tamper-checks.txt`). The only
  remaining `⟨FILL⟩` in the bullet is the verifier set (RV-11/RV-12/CR-5/VZ-3),
  whose artifacts had not all landed at this draft's last write; if a verifier
  seat lands after this draft, add its receipt to that slot rather than
  rewriting the measured numbers.
- Do not restate client version pins or `config.toml`-style `path:line`
  pointers in the C3 bullet (kept out for consistency with the scorecard-side
  section, which must stay pin-free past the census bound). The bullet names no
  client config path and no version literal.
- The C1/C2 bullets must come from this round's C1/C2 records drafts
  (`claims/c1/records-drafts/`, `claims/c2/records-drafts/`); if those seats did
  not land, mark their evidence as a named gap rather than paraphrasing the
  frozen claim as if measured.
- Delivery count: take it from the roster reconciliation, never from the
  declared 64 (counting lesson
  `corpus/lessons/2026-10-18-wave-dispatch-counting.md`).
- The C3 bullet deliberately does not claim "every arc3 citation covered" as a
  count — the frozen claim's own acceptance test is the census with
  adjudications; keep that phrasing when filling.
- Further landed C3 wave-tree evidence for the splice: EX-43's census
  `claims/c3/EX-43/census.out` + `candidate-entries.json` (its scratch
  extension measured 48 entries / 5 quoted, sha `0b01f521…`, `--strict` rc 0;
  teeth control rc 1; drift-injection pair `drift-blind.txt` /
  `drift-caught.txt` — the 31-entry table blind at a real drift revision, the
  extension catching 2 `citation_dead`); EX-44's `neuter-proof.txt`; EX-46's
  `pin-check.py` plus stale-pin / one-byte-tamper simulations.
- Verifier state at this draft's last poll: RV-12's seat report landed
  (`seats/RV-12.md` — independent re-verification of the landed pair plus a
  fragility battery: 34 entries fire on an honest rename even with citing
  lines updated, 14 of them new; advisory patch text
  `claims/c3/RV-12/fragility-mitigations.patch.md`); RV-11's checkers/runs
  partially landed (`claims/c3/RV-11/runs/`; one checker crashed mid-run — a
  seat-level defect, not a table finding); CR-5/VZ-3 artifacts not yet on
  disk. Add each landed verifier's receipt to the C3 bullet's verifier slot at
  records time.