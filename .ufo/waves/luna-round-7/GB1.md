## CLAIM
G1/G2 vs Z1/Z2: Z1 dropped two guards that should be restored in entry 1; Z2's block on entry 2 rests on a now-stale, partly non-reproducible absence claim, and G2's landing elements must survive.

## METHOD
Read G1, G2, Z1, Z2, E1D, E2D, G3, E6D, SC1/SC2, CC4, `corpus/QUALITY.md`, and both lanes' leg-3/leg-4 receipts. Reproduced Z2's globs today. No probes, network, or write outside this file.

## FINDINGS
1. Entry 1, restore negative-evidence guard. Receipt verbatim: "Missing metadata is reported as unknown, not proof that an image is not Go" (`receipts/leg-3.md:8`). G1 keeps it (`G1.md:10`); Z1's recommended text shrinks it to "says absent metadata is unknown" (`Z1.md:18`). This is the over-read G1's CLAIM names; restore inside the description-only observation.
2. Entry 1, restore provenance line. G1's "`file` output establishes ELF format, not language attribution" (`G1.md:16`; `SC1.md:13,16`) is absent from Z1, which cites SC1 only as carrier source (`Z1.md:23`).
3. Entry 2, Z2 stale. Z2's unverified-convergence verdict rests on drafts being absent (`Z2.md:5,11`). Reproduced `Glob("**/E2D.md")` → `.ufo/waves/luna-round-7/E2D.md`; E2D mtime 19:57:52 predates Z2.md 19:59:10 by ~78s, so that claim was false at write time. G2.md landed 19:59:26, 16s after Z2.md — a race, but the verdict no longer holds.
4. Entry 2, restore G2's landing elements Z2's text lacks: Evidence ID `ev_9ea97685…` (`G2.md:19`; verified `receipts-B/leg-4.md:47,67` — QUALITY criterion 6), the SC2-preflight-is-not-provenance guard (`G2.md:15`; `SC2.md:12,14-15`), numeric bounds (`G2.md:22`; `receipts-B/leg-4.md:47`). Keep G2's lane-B-only entry shape (`G2.md:10-25`) per ruling (c); E2D merges both carriers in one Observation (`E2D.md:12-14`).
5. Entry 2, add Z2's compiler-inference note to G2's distinct-carrier threat: lane A's rustc hash is `evidence_kind:"inferred"` (`receipts/leg-4.md:28`); `G2.md:28` cites it only as a hash.
6. Integration must-check: neither Z1's recommended text (`Z1.md:11-23`) nor G2's body carries `source:`/`verified-at:`/`recheck:`; add per ruling (d), pattern `E6D.md:12-14` (G3 flags the same gap, `G3.md:10`).

## THREATS
Today's glob reproduction does not prove Z2's historical glob failed; the G2/Z2 race is inferred from mtimes. Command A, map rows, counters, and prior-corpus byte identity are parent-side and unverified here. Receipts are HEAD-pinned records, not re-executed probes.

## VERDICT
FINDING: restore entry 1's "not proof not-Go" clause and SC1 provenance line; land entry 2 on G2's lane-B shape with its Evidence ID, preflight-provenance guard, and bounds — Z2's E2D-absence rationale is stale.
