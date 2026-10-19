# proposed registry row — SKILL.md "Local round-evidence gate registry" (patch text)

Authored by SEAT PL-3 (chain c3, planner). **Patch text only** — SKILL.md is not a
seat write target (wave rule; proposed changes land as `*.patch.md`). Intended
placement: the registry table at `SKILL.md:360-371`, as a new row after
`citation-drift`. Measured values from
`claims/c3/PL-3/measurements.txt` (tool sha `112d01dc…`, 2026-10-19).

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| custody-pair | gate / kaidoku | `python3 .ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label L] [--paths P...]` and `… verify <receipt> [--live \| <receipt-b>]`; **exit map (extended, declared in the tool docstring): 0 MATCH / 10 CONTENT-DRIFT / 11 REWRITE-DRIFT (sha256 equal, inode or mtime/ctime moved — same-content rewrite) / 12 METADATA-DRIFT (mode·uid·gid·size·type, LABEL-DEFECT, EXTRA-PATH) / 13 ABSENT / 2 USAGE / 3 SELFTEST-FAIL**; capture exits 13 on an absent requested path and still writes the receipt; severity precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH | same tool with `selftest` (15 fixture cases, never touches a custody path; scratch defaults `/dev/shm`→`/var/tmp`, refuses `/tmp` — EDQUOT hazard) | Read-only over the 5 custody paths (sha256 + stat only; atime deliberately not captured). v2 receipt fields per path: `EXISTS, TYPE, SIZE, SHA256, MTIME_EPOCH, MTIME_NS, MTIME_UTC_RENDER, MTIME_LOCAL_RENDER, CTIME_EPOCH, CTIME_NS, CTIME_UTC_RENDER, CTIME_LOCAL_RENDER, INODE, MODE, UID, GID`; header pins the producing tool's sha256 — **any tool revision requires a fresh capture or a recorded revision mapping** (C1 rule-#14 discipline). v1 shapes (`sums-v1` sha256sum form, `v1-stanza`, `pipe-v1`) verify on the sha256 contract (`SHA256-CONTRACT n/n`); time-carrying v1 receipts carrying the round-1 local-render defect report `LABEL-DEFECT` and exit 12, never a clean pass. Never writes over a custody path (exit 2 if told to), never edits a receipt it reads. |

## Evidence for the row

- Tool: `.ufo/gates/custody-pair/custody-pair.py` sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`.
- Selftest: `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0` (12:06Z).
- Claim-level classes measured by PL-3 on `/var/tmp` replicas (C0-C13): 0 / 11 / 11 / 12 / 10 / 13 / 10 / 11 as tabulated in `plan.md` §4.
- v1 live checks: `sums-v1` → exit 0 (`MATCH-V1-PARTIAL 5/5`, `SHA256-CONTRACT 5/5`); `v1-stanza` → exit 12 (`SHA256-CONTRACT 5/5` + `LABEL-DEFECT` ×5); `pipe-v1` → exit 12 (`compared=3/11`).
- Live pair: `claims/c3/receipts/config-pre-pair-v2.txt` (sha256 `fa9706c6…`), captured 12:04:06Z by tool revision `4862f642…`; landed revision `112d01dc…` — re-capture recommended (field-level diff vs this seat's 12:07:30Z capture: all 11 fields equal, drift-free).
