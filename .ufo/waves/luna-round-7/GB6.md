## CLAIM
Review of E1D–E6D against Z1–Z6 for E-draft content silently dropped before integration: itemized keep/drop list.

## METHOD
Read E1D–E6D, G1–G6, Z1–Z6 in `.ufo/waves/luna-round-7/`; checked on-disk mtimes via `ls --full-time E*.md G*.md Z*.md`. No probes, network, or tracked-file writes; only this seat file written.

## FINDINGS
1. **Z2 stale E2D-absence.** Z2 (mtime 19:59:10) records E2D absent (`Z2:5,8`); E2D was on disk from 19:57:52, 78s earlier. E2D was never reconciled; G2 (19:59:26) postdates Z2, so only the E2D half is stale. Keep from E2D: two-carrier split with per-carrier Evidence IDs (`E2D:12-13`), rustc hash `da80ed…` labeled inferred (`E2D:13`), RESULT-not-Core admission line (`E2D:17`), SC2 "candidate" caveat (`E2D:20`) — G2:15,20-22 carries part, but `G2:28` reduces lane A to a bare hash, losing the inferred-hash detail that ruling (c) needs for distinct carriers.
2. **Z5 stale E5D/G5-absence.** Z5 (19:59:38) records both absent (`Z5:5`); E5D (19:59:19) and G5 (19:59:18) predate it. E5D's exercised `limit=100` argument (`E5D:5`) appears in neither `Z5:8` nor `G5:8` — keep (part of the exercised call; recheck accuracy). E5D's `procedure=null` and reproducer (`E5D:5,8`) — drop-safe (receipts retain them).
3. **Z1.** Explicitly omits E1D's replay command (`Z1:5`); merged text (`Z1:10-24`) carries no source:/verified-at:/recheck: fields (ruling d). Keep the replay as `recheck:`. E1D's byte size/offset (`E1D:21`) — drop-safe (SHA-256 pins identity).
4. **Z4.** Correctly drops E4D's lane-A half and A/B comparative framing (`E4D:8`; synthetic fixture, ruling b); E4D's untested-case list survives via `G4:19-20`. Drop the lane-A receipt from E4D's proposed row sources (`E4D:11`).
5. **Z3.** Drops E3D's resource bounds (1 GiB, 262,144-byte windows, ≤32 sentinels; `E3D:11`) and reproducer (`E3D:8`) — keep both (limitations QUALITY-mandated; reproducer feeds recheck). E3D's raw-byte 48/49 and exit-0 detail — drop-safe.
6. **Z6.** Drops nothing material from E6D; map rows deferred, not dropped (`Z6:13`). Only E6D has source:/verified-at:/recheck: (`E6D:12-14`); E1D–E5D and Z1's merged text lack them — integration must add.

## THREATS
Mtime order is not proof of read order for near-simultaneous files; Z2/Z5 may have raced a live directory. Keep/drop calls are draft-level; I did not re-verify round-6 receipts.

## VERDICT
FINDING: Z2/Z5 stale absence claims leave E2D unreconciled and drop E5D's exercised `limit=100`; Z1/Z3 drop reproducer, size, and limitation detail needed for recheck and QUALITY compliance.
