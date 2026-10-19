# arc3-loop1-round3 — frozen claims, 2026-10-19

Wave: 64 seats, `alibaba-token-plan/deepseek-v4.1-flash` (token-plan key 1 of 3 —
operator directive: the deepseek-v4.1-flash swarm waves ride the token-plan lanes;
recorded in the round-2 records and ledger). Roster frozen PRE-DISPATCH; the
dispatch items array must carry exactly the 64 seat names below; the parent counts
the items array. Roster enumerated mechanically: 24 + 24 + 12 + 4 = 64, every seat
name appearing exactly once.

Axis set: **coverage (owned)**, **operability (fleet)**, **freshness (fleet)**.
Lowest-axis rule: owned proxies tied at 10.0, none retired; the owned claim is
selected by the standing most-falsifiable-next-claim tie-break. Claims are
causally separable: corpus/knowledge, the custody tool, and the probe's pointer
table — no shared edit targets.

## C1 — coverage (owned): EVM family extension — optimizer-enabled dispatch shapes

Named Unknown (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` Unknowns):
"optimizer-enabled dispatch shapes beyond the smoke compile". No new install: the
receipted wave solc prefix from arc3-loop1-round1 is reused (its install receipt
pins the compiler bytes; record the reuse).

Claim: after the round's commit, at least one **optimizer-enabled** carrier
(`--optimize --optimize-runs 200`) plus one non-ERC-20-shaped carrier (e.g. a
payable receive/fallback + mixed mutability, or a library-bound shape), compiled
on-host with the pinned solc, has its planted selectors recovered K/K by
`inspect-evm-interface` (both pins where feasible); the result lands as a corpus
knowledge entry + line-neutral map token; command A re-measures 82 → 83 with the
prior 82 byte-identical.

Falsifiable before → after: command A at the work commit — knowledge_files 82 →
83, mapped 83, missing [], dangling [], rules 14/14; planted-K recorded pre-probe;
K/K with zero extras per carrier. Honest-stop branches pre-written: optimizer
dispatch shape defeats the extractor (typed refusal or parse-empty → recorded,
claim reports honest stop); the probed prologue class differs from the r1
recorded classes (recorded as the round's delta, not a defect).

## C2 — operability (fleet): custody-pair hardening — D2 + D3 + write-guard scope + D6

Named debt (arc3-loop1-round2 C3 verdict; patch texts in that wave tree):
- D2: exists-but-EACCES path records `exists=no` + STAT-ERROR and a both-sides
  absent path verifies MATCH exit 0 (fail-open); `--live` against an unreadable
  candidate dies with a traceback outside the declared map.
- D3: `verify` only compares paths present in receipt A (a 1-of-5 receipt reads
  exit 0) — `EX-35/proposed-v1-verify-adapter.patch.md` (`--require-paths`).
- Write-guard scope (VZ-4 finding): `--paths X --out X` silently clobbers the
  scoped file it measures (canonical 5 guarded, override unguarded).
- D6: `selftest --scratch <missing dir>` raw FileNotFoundError traceback, exit 1
  outside the declared map.

Claim: after the round's commit, each named hole is closed with a declared exit
class (EACCES → its class, no fail-open MATCH; verify coverage declared;
write-guard extended to `set(paths) ∪ CUSTODY_PATHS`; selftest scratch-guard →
USAGE); the selftest grows 15 → ≥17 cases with the new fixtures; the registry row
+ README are updated in the SAME commit (revision-pinned clauses re-derived —
the r8 coupled-landing precedent); the round's live pre/post pair (captured by
the revised tool) verifies MATCH 5/5; v1 receipts remain sha256-verifiable; every
receipt self-pins the revised tool's sha256.

Falsifiable before → after: the four injections reproduce as their declared
classes (before: fail-open / traceback / clobber — measured in round 2); selftest
15 → ≥17 at exit 0; live pair MATCH 5/5; command A unchanged.

## C3 — freshness (fleet): citation-drift probe table — arc3-era coverage extension

Named debt (arc3-loop1-round1 C2 note + the r10 extension precedent): the probe
table's 31 entries do not cover the arc3-era citations (the r1 knowledge entry,
the arc3 SCORECARD sections' pinned needles where applicable, the round-2
registry rows, custody receipt conventions).

Claim: after the round's commit, the pointer table carries entries covering every
in-repo citation introduced by arc3 rounds 1-2 that is pinnable under rule #11
(no bare line numbers into operator-mutable files — entries that cannot conform
are adjudicated NO-ENTRY with cause, per the r4 precedent); the table's sha256 is
re-pinned in `expected.json` in the same commit (the F3 coupling); probe findings
= 0 at HEAD in both modes; selftest 13/13 unchanged; command A unchanged.

Falsifiable before → after: table entries 31 → N (N counted mechanically); the
arc3-citation census (every pinnable arc3 citation either table-covered or
adjudicated) is the acceptance test, not the count; findings = 0 at the work
commit; the digest pin matches the landed table.

## Cross-cutting rules (frozen)

- No installs. The round-1 solc prefix is reused under C1 (receipt re-verified).
- Scratch under `/var/tmp` or `/dev/shm` (`/tmp` EDQUOT — standing).
- Custody paths READ-ONLY for all seats (C2's live work is capture/verify only;
  the clobber-attack demo runs on scratch copies only).
- Seat discipline: seats write ONLY their seat report at
  `.ufo/waves/arc3-loop1-round3/seats/<SEAT>.md` and artifacts under
  `.ufo/waves/arc3-loop1-round3/claims/{c1,c2,c3,cross}/<SEAT>/`; NO git
  mutations; no LOG/SCORECARD/SHONEN writes; corpus/SKILL/README edits as patch
  text only. Only the designated implementer writes its chain's real target:
  C2's EX-21 (`.ufo/gates/custody-pair/`) and C3's EX-41 (`.ufo/gates/
  citation-drift/pointer-table.json` + `expected.json` — digest re-pin in the
  same artifact pair). Census scope rows are NOT widened (r4 precedent).
- Seat reports carry: work performed (evidence pointers), proposed changes (patch
  text paths or "none"), before→after measurement, attacks attempted, blockers.
- Round report: `.ufo/reports/arc3-loop1-round3/kaidoku.md` (parent-written).
- Identity discipline (rule #14): every artifact claiming its own byte-identity
  re-derives it after revision; the parent re-derives all identities at landing.

## Roster (64 seats, enumerated)

C1 chain (24): PL-1, EX-01, EX-02, EX-03, EX-04, EX-05, EX-06, EX-07, EX-08,
  EX-09, EX-10, EX-11, EX-12, EX-13, EX-14, SC-1, SC-2, RV-1, RV-2, RV-3, RV-4,
  CR-1, CR-2, VZ-1
C2 chain (24): PL-2, EX-21, EX-22, EX-23, EX-24, EX-25, EX-26, EX-27, EX-28,
  EX-29, EX-30, EX-31, EX-32, EX-33, SC-3, SC-4, RV-5, RV-6, RV-7, RV-8, RV-9,
  CR-3, CR-4, VZ-2
C3 chain (12): PL-3, EX-41, EX-42, EX-43, EX-44, EX-45, EX-46, SC-5, RV-11,
  RV-12, CR-5, VZ-3
Cross (4): CN-1, CN-2, CU-1, VZ-4

Counts: C1 = 1+14+2+4+2+1 = 24. C2 = 1+13+2+5+2+1 = 24. C3 = 1+6+1+2+1+1 = 12.
Cross = 4. Total = 24+24+12+4 = 64.

Assertions at dispatch: len(items) == 64; every item name in this roster; no
duplicate names.
