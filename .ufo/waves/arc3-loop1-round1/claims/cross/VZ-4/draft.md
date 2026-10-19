# DRAFT (working copy) — wave-summary inputs, VZ-4

NOT the deliverable. Final artifact: claims/cross/wave-summary.md.
Written incrementally during the poll; numbers refreshed at close.

## Inputs gathered (with pointers)

- Roster: claims-frozen.md:90-98 — C1 26, C2 20, C3 14, Cross 4 = 64.
- Census script: claims/cross/VZ-4/roster-census.sh (mechanical, per-chain).
- Poll log: claims/cross/VZ-4/poll-log.txt (checks 1..25).
- Custody: CU-1 pre-pair claims/cross/receipts/config-pre-pair.txt (5/5,
  capture 2026-10-19T09:57:18Z, HEAD e845c2b); independent recompute by VZ-4 at
  10:03:33Z — byte-identical 5/5; EX-01/EX-10 corroborations; EX-15 T0/T1 pair;
  TZ-label defect in CU-1 metadata (EX-01 A4, EX-10 nit) — digests unaffected.
- C1: EX-02 solc 0.8.37 install receipt (+ ambient-solc pre-existence note);
  EX-06 K=6 planted set + probe run (6.7.0); RV-2 K=6/6 CONFIRMED dispatch:"abi";
  RV-1 independent keccak recompute MATCH on 3 landed sets; EX-03 NEVER LANDED
  (primary target absent — RV-1); EX-11 before-state command A 81/81 13/13;
  RV-4 map-token line-neutral PASS (81→82, prior 81 byte-identical); EX-09 id
  STABLE across 4 runs; EX-14 manifest 107 entries OK; EX-15 containment clean.
- C2: PL-2 guard prototype (13/13, tampered→exit 2, unpinned→exit 2); RV-6
  pre-state silent-rc-0 class CONFIRMED; RV-8 guard-compat matrix (D1 vs D2);
  SC-4 changeset (EX-16 pending); EX-24 pin-mutability (recommendation only).
- C3: EX-26 census at HEAD PASS 0/0/0/0 (exit 0, sha 3b677b8e…); SC-6 E22
  disposition draft; RV-11 v9/v10 lineage; EX-30 T0; CR-5 EX-28 pending.
- Environment: /tmp EDQUOT fleet-wide (pre-existing 12.1G per-UID quota; EX-15
  containment §4); 147 zero-byte casualties; .ufo/gates/__pycache__ leak
  (06:58:37, removed 07:03, re-appeared 07:04:16 per PL-2).

## Pending at draft time

- VZ-1/VZ-2/VZ-3 packets (per-chain verdicts) — not landed.
- EX-16 (C2 real target) and EX-28 (C3 real target) — not landed.
- CU-1 post-pair — pending.
- Final census count + undelivered names — at close.
