# arc3-loop1-round4 — frozen claims, 2026-10-19

Wave: 48 seats (within the scheduled 32–64 band), `hyper/deepseek-v4.1-flash` —
declared fallback on usage exhaustion: the devin lane (`devin/deepseek-v4-1-flash-max`),
same seat count, operator-directed (the token-plan quota is exhausted; recorded in
the round-3 records). Roster frozen PRE-DISPATCH; the items array must carry
exactly the 48 names below. Roster enumerated mechanically: 16 + 14 + 14 + 4 = 48,
every seat name appearing exactly once.


Lane substitution at dispatch: the hyper lane returned 402 out-of-credits on all
48 seats (zero delivered, ~30 s). Per the round-4 schedule's declared fallback and the
operator directive, the full roster re-dispatched on the devin lane
(devin/deepseek-v4-1-flash-max). Recorded with cause, not a lane signal. The roster,
claims, and assertions below are unchanged.

Axis set: **coverage (owned)**, **freshness (fleet)**, **operability (fleet)**.
Lowest-axis rule: owned proxies tied at 10.0, none retired; most-falsifiable
tie-break. Claims are causally separable: corpus/knowledge (new entry), PROVINCE
surface text (patch texts only), the custody tool.

## C1 — coverage (owned): EVM family closure — the Vyper leg

Named Unknown (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`):
"Vyper and solc versions other than 0.8.37". Install authorized (goal scope):
`pip install vyper` into an isolated venv under the wave dir
(`.ufo/waves/arc3-loop1-round4/tools/vyper-venv/`); record name/version/wheel
sha256. Environment risk pre-accepted: if no host/venv python is vyper-compatible
after one bounded attempt (recorded), the claim honestly stops.

Claim: after the round's commit, at least one Vyper-compiled contract's selectors
are recovered by `inspect-evm-interface` (K/K against Vyper's own ABI-derived
selector set), OR the extractor's behavior on Vyper dispatch shapes is sealed as a
typed result (parsed-empty / partial recovery) with the exact envelope; the result
lands as a corpus knowledge entry + line-neutral map token; command A re-measures
83 → 84 with the prior 83 byte-identical.

Falsifiable before → after: command A at the work commit — knowledge_files 83 →
84, mapped 84, missing [], dangling [], rules 14/14. Planted-K recorded pre-probe.
Honest stops pre-written: venv infeasible (record, not verified); typed refusal;
partial recovery (land the exact partial set, no costume).

## C2 — freshness (fleet): PROVINCE Frontier/surface staleness census + repairs

Named debt (arc3-loop1-round3 CR-1 Edit 3 parent note): the PROVINCE Frontier
bullet "real solc/vyper-compiled bytecode untested" is stale since arc3-r1.

Claim: after the round's commit, every PROVINCE Frontier bullet and surface-summary
claim is census-checked against the admitted corpus state; every stale item is
repaired same-line (line count held) or adjudicated NO-CHANGE with cause; the
census instrument reads PASS at the records commit (PROVINCE is a scoped file —
repairs must stay pin-conformant); the repairs land as patch texts applied by the
parent (seats never write PROVINCE).

Falsifiable before → after: the staleness census (each checked bullet: stale /
current / adjudicated, with evidence) → stale count N → 0; PROVINCE line count
unchanged; census PASS at the work tree after the parent applies the patches.

## C3 — operability (fleet): custody-pair residual closures (r3 named debt)

Named debt (arc3-loop1-round3 records + c2/c3 verdicts): (a) sidecar path not
scope-checked (`--out X.sha256 --paths X` can aim a derived sidecar at a measured
file's neighbour); (b) `out.parent.mkdir` outside the guarded try (traceback
class); (c) coverage gate counts stanzas, not distinct paths; (d) the
both-sides-absent MATCH semantics — adjudicate and document (declared design:
only error-carrying stanzas are UNEVALUABLE) or close with a flag, per the wave's
evidence. Patch texts exist: `.ufo/waves/arc3-loop1-round3/claims/c2/EX-24/`,
`CR-3/`, `CR-4/`, `RV-8/`.

Claim: after the round's commit, (a)-(c) are closed with declared classes (selftest
22 → ≥24 with the new fixtures; sabotage arms), (d) is adjudicated with the ruling
text landed in the README; the registry row + README re-derived same-commit; the
round's live pair (revised tool) verifies MATCH 5/5; every receipt self-pins the
new tool sha256; command A unchanged.

Falsifiable before → after: the three injections reproduce as their declared
classes (before: measured residuals); selftest 22 → ≥24; live pair MATCH.

## Cross-cutting rules (frozen)

- One authorized install: vyper into the wave venv (C1 only). No other installs.
- Scratch under `/var/tmp` or `/dev/shm` (`/tmp` EDQUOT — standing).
- Custody paths READ-ONLY for all seats; custody-tool demos on scratch copies.
- Seat discipline: seats write ONLY their seat report at
  `.ufo/waves/arc3-loop1-round4/seats/<SEAT>.md` and artifacts under
  `.ufo/waves/arc3-loop1-round4/claims/{c1,c2,c3,cross}/<SEAT>/`; NO git
  mutations; no LOG/SCORECARD/SHONEN/corpus/SKILL/PROVINCE/README writes — patch
  texts only. Only the designated implementer writes its chain's real target:
  C3's EX-21 (`.ufo/gates/custody-pair/`).
- Identity discipline (rule #14): re-derive every self-claimed byte-identity
  after revision; the parent re-derives at landing.
- Seat reports: work performed (evidence pointers), proposed changes, before→after
  measurement, attacks, blockers.
- Round report: `.ufo/reports/arc3-loop1-round4/kaidoku.md` (parent-written).

## Roster (48 seats, enumerated)

C1 chain (16): PL-1, EX-01, EX-02, EX-03, EX-04, EX-05, EX-06, EX-07, EX-08,
  EX-09, EX-10, SC-1, RV-1, RV-2, CR-1, VZ-1
C2 chain (14): PL-2, EX-11, EX-12, EX-13, EX-14, EX-15, EX-16, EX-17, SC-2,
  RV-3, RV-4, RV-5, CR-2, VZ-2
C3 chain (14): PL-3, EX-21, EX-22, EX-23, EX-24, EX-25, EX-26, EX-27, SC-3,
  RV-6, RV-7, RV-8, CR-3, VZ-3
Cross (4): CN-1, CN-2, CU-1, VZ-4

Counts: C1 = 1+10+1+2+1+1 = 16. C2 = 1+7+1+3+1+1 = 14. C3 = 1+7+1+3+1+1 = 14.
Cross = 4. Total = 16+14+14+4 = 48.

Assertions at dispatch: len(items) == 48; every item name in this roster; no
duplicate names.
