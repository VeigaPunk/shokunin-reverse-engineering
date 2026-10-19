# RV-14 — review plan: EX-36's custody-pair registry row vs the actual tool

Seat RV-14, chain c3, role reviewer. Task: every behavior claimed in EX-36's
registry row must exist in the actual tool. Written before the artifacts landed
(so the check list is not fitted to the text).

Inputs (each must exist before a verdict is possible):
- row artifact: `.ufo/waves/arc3-loop1-round2/claims/c3/EX-36/` (patch text for
  the SKILL.md registry table, third row)
- tool: `.ufo/gates/custody-pair/` (EX-31, the only permitted writer)

## Method

1. Read the row; split it into atomic claims (name / entry command / verdict map
   / self-invocation / pinned values / write scope — the SKILL.md row schema).
2. For each atomic claim, run the *stated* command and compare against the
   *code* (source read) and against independent ground truth
   (`python3 os.lstat` + `hashlib.sha256`), never against the tool's own
   summary of itself.
3. Synthetic fixtures only (no real custody path is copied); real paths are
   hash/stat-captured read-only. Fixture + attack suite:
   `/var/tmp/rv14/harness/behavior-probe.py` (copy in `receipts/`).
   - capture fixture set, then same-content rewrite (`os.replace` a fresh copy
     of identical bytes over a fixture) → the tool must detect inode/ctime
     movement while sha256 is unchanged.
4. Attacks/refutations: run the same-content-rewrite attack against the tool's
   *own claim* (does it really detect it?); try to falsify the "label defect is
   gone" claim by feeding a local-timezone rendering; try to falsify the v1
   compatibility claim with the committed round-1 receipt
   (`arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`,
   self-sha256 `b8ed1936…`).

## Claim checklist (pre-drafted from the frozen C3 claim; extended on landing)

- [ ] tool dir exists at the row's stated path; every file the row names exists
- [ ] stated entry command runs from the stated cwd, exit code as declared
- [ ] v2 receipt carries sha256 (verified == independent `sha256sum`)
- [ ] v2 receipt carries mtime epoch (verified == `os.lstat().st_mtime`)
- [ ] v2 receipt renders mtime in UTC and labels it truthfully (no -03 local
      rendering under a UTC label; the round-1 label defect)
- [ ] v2 receipt carries inode (== `os.lstat().st_ino`)
- [ ] v2 receipt carries ctime (== `os.lstat().st_ctime`)
- [ ] same-content rewrite detected (inode/ctime movement), sha256 unchanged
- [ ] v1 receipts remain verifiable against the tool's sha256 fields
- [ ] live pre/post pair (exit 0, 5/5) reproducible by the tool
- [ ] self-invocation flag (if claimed): exists, case count as claimed, stable
      finding ids
- [ ] pinned values (if claimed): pin file exists, digest matches the artifact
- [ ] write-scope claim: tool writes nothing under the custody paths; selftest
      writes only isolated fixtures

## Pre-landing reproductions (already measured by this seat)

- Label defect (C3 measured origin) independently reproduced:
  `receipts/label-defect-repro.txt` — devin/omp epoch `1792011200` =
  `2026-10-14T20:53:20Z` = local `17:53:20 -03`, while the v1 receipt prints
  `2026-10-14 17:53:20` under an `MTIME_UTC` label (3 h).
- Live 5-path capture (read-only) `2026-10-19T12:02:57Z` byte-identical to the
  round-1 CU-1 pre-pair (5/5) — so v1-receipt compatibility can be tested
  against live state: `receipts/rv14-live-5path-*.txt`.
