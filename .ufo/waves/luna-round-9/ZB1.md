## CLAIM
Independent landing list for the four carried-spill items, built from primary sources, then diffed against Z5.

## METHOD
At HEAD a280e07: read r4-16:728-796,875-925; r12-01:97-120; jq-shadow :10-20,200-242; PROVINCE:114-116; SCORECARD:68-80,88-123,380-460,534-559; round-4/5 reports; X1:32; CB4:11; PROTOCOL.md:341-344 (fleet root); seats Z1-Z6, H-H4, D2-D4, X4, F3, P0, G2. Command A rerun per SCORECARD:92-123 at HEAD: mapped 79/79, knowledge_files 79, missing [], dangling [], 9/9, 10.0/10.0. Static only; no probes, network, /tmp access, or deletions.

## FINDINGS
Landing list L1-L4, diffed vs Z5:
- **L1:** append one short tail errata section to r4-16 ("round-9 freshness", mirroring r12-01's round-5 erratum form) naming r12-01:99-104 and :110-120; do not restate the four sites or "7 values" — the defect is a stale duplicated summary, and recopying corrected detail re-creates that hazard (`H4.md:8`). `Z5.md:8` keeps the four-site restatement; attribution belongs at the cited loci. Tail append shifts no cited line; tracked refs reach :913-915 (`corpus/README.md:177`) and :751-752 (`SCORECARD.md:557`) — a mid-block insert at :796 would mis-resolve the former.
- **L2:** agree with `Z5.md:9`/X4 — SCORECARD round-9 learning, not QUALITY.md; trim Z2's closing imperative to a recording; no score change (`X1.md:32`; `CB4.md:11`; round-4 report :43-46; round-5 report :50-56,63-67).
- **L3:** agree no pre-existing-/tmp requirement (Z3; `H.md:10,13`). Add the brief's conservative proposal, absent from `Z5.md:10`: lane performs no cleanup; operator-owned review of namespaced scratch only; shared-/tmp caution `SKILL.md:39-40`; tmpfs non-durability `PROTOCOL.md:341-344`. Unresolved: l7-01 npm-cache pre-existence (`2026-10-16-l7-01-inspect-go-binary.md:5`); size/ownership (~1.2 GB is a round-6 snapshot, `LOG.md:808-809`).
- **L4:** diverge from `Z5.md:11` on scope — disavow :217 "benign payload", :219 "not binary compromise", :236-237 "benign, intentional agent-installed" as present safety/trust conclusions; state only the recorded SHA-256 identity match (:10-13,204-219); cite `PROVINCE.md:114-116` (`D4.md:8`; `H4.md:11`; `D3.md:8-10`). r3 bleed (:59-66,:136-137) stays follow-up.
- **Framing:** agree with `Z5.md:13`/H1-H3 — no aggregate freshness claim; only L1 is freshness-adjacent; rerun command A post-integration. `Z6.md:2-5` ("Z5/F3 absent") is already stale — both exist.

## THREATS
Dispositions, not landed text; pre-state only. "7 values" not re-derivable; upstream identity/safety not re-checked; no /tmp inspection. PROVINCE untouched; no deletions authorized.

## VERDICT
FINDING: Z5 items 1-3 confirmed with trims; item 4 must scope :217-219 and :236-237, not "benign" alone; item 1 lands as a pointer, not a restatement.
