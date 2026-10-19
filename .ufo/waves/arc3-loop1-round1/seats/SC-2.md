# SC-2 — manifest cross-check (chain c1, scribe)

Seat **SC-2**, wave `arc3-loop1-round1`, chain **c1** (coverage). Task: poll for
EX-14's `claims/c1/receipts/MANIFEST.draft.txt`, independently recompute the
sha256 of every file it lists, and flag mismatches / missing files at
`claims/c1/receipts/manifest-crosscheck.md`.

## 1. Work performed

- Polled the wave dir (60 s cadence): the manifest first appeared at
  09:59:40Z and was regenerated twice more — three snapshots observed:
  S0 09:59:40Z (`entries: 0`), S1 10:01:21Z (`d6336a17…`, 34 rows),
  S2 10:04:54Z (`0afdb34e…`, 107 rows).
- Built an independent checker, Python `hashlib` (not `sha256sum`), with size
  comparison, header arithmetic, declared-scope audit, ctime-based staleness:
  `claims/c1/SC-2/manifest-crosscheck5.py`
  (sha256 `cf56eab33ae3e9d501b5f1feb9ec1682115118b4a92f526a259817b819e46477`).
- Fixture-tested it before use: a planted fixture (1 tampered, 1 missing,
  1 unlisted extra, 1 markdown-table row) was caught exactly (2/5 verified,
  exit 1); the clean fixture passed (exit 0) — no false positives.
- Ran it against S2 twice: `claims/c1/SC-2/crosscheck-run3.txt` (10:06:30Z,
  110/116), `claims/c1/SC-2/crosscheck-run5.txt` (10:07:4xZ, 109/116); and ran
  EX-14's own check-file through `sha256sum -c` as corroboration
  (`claims/c1/SC-2/checkfile-run4.txt`).
- Wrote the deliverable `claims/c1/receipts/manifest-crosscheck.md`
  (+ mirror `claims/c1/SC-2/manifest-crosscheck.md`), with the snapshot table,
  per-class findings, digests, and reproduce commands.
- Chain-before evidence, independently reproduced: command A
  (`SCORECARD.md:92-123` verbatim) at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
  → `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
  "rule_blocks": 13}` (matches EX-11's `claims/c1/EX-11/command-A-before.txt`).
- Custody cross-check: `claims/cross/receipts/config-pre-pair.txt`
  `b8ed1936…` 2045 B reproduces; the 5 live custody digests in the manifest's
  section 2 reproduce against the live files.

## 2. Proposed changes

- **Patch text only** (not applied), inside
  `claims/c1/receipts/manifest-crosscheck.md` §"Proposed change": add
  `! -path '*/__pycache__/*'` to EX-14's generator exclusion array, so
  transient bytecode caches stop entering the manifest (a listed `.pyc` was
  deleted mid-wave, producing the snapshot's one MISSING row).
- No repo file was created or modified by this seat outside its two allowed
  areas (seat report + `claims/c1/SC-2/` artifacts + the task-specified
  `claims/c1/receipts/manifest-crosscheck.md`). No git mutations; LOG.md /
  SCORECARD.md / corpus untouched.

## 3. Before → after measurement (chain c1 relevant)

- **Before** (06:57 local, wave open): `claims/c1/receipts/` did not exist —
  nothing to cross-check; command A 81/81, 13/13, 10.0/10.0 at `e845c2b`.
- **After** (10:07:4xZ), against S2 `0afdb34e…`:

```
entries parsed: 116  verified: 107  problems: 9
header check: entries header=107 section-1 rows=107  MATCH
header check: total-bytes header=434028 section-1 sum=434028  MATCH
VERDICT: FAIL (listed=116 verified=107 problems=9 unlisted=220
         unlisted-pre-generation=0 declared-excluded=360 header=ok)
```
(run6, 10:14Z; the earlier run5 at 10:07:4xZ read 109/116 with 7 problems)

- 9 flagged at run6: 1 MISSING, 8 MISMATCH.
  - MISSING = `claims/c1/EX-08-search.js`: a **path move**, not data loss — the
    content now sits at `claims/c1/EX-08/EX-08-search.js` with digest
    `d4a21a24…` and 2145 B identical to the manifest's row (verified by hand).
  - All 8 MISMATCH carry `ctime > generated-utc` (live rewrites by owning
    seats, e.g. `EX-06/evidence/transcript.txt` **same size 9442 B, different
    digest** — a size-only check would have missed it). **No file with
    ctime ≤ generated-utc failed to reproduce** → no snapshot-internal error,
    no tamper signature. run5's MISSING `.pyc` reappeared at 10:10:13Z
    byte-identical (transient bytecode class).
- Scope audit: 0 undeclared unlisted files predating generation (no scan
  misses); 220 unlisted at run6, all post-generation live writes; 360 files
  under `claims/c1/EX-13/_scratch` correctly covered by the manifest's own
  section-1b declared exclusion.
- S0 defect quantified: the 09:59:40Z snapshot listed 0 files while 12+ existed;
  its own verification passed vacuously ("all 0 entries OK",
  `claims/c1/EX-14/verify.log:1-3`), and its check-file digest `e3b0c442…` is
  the empty-file digest. Root cause: generator v1's `mktemp` temp files under a
  quota-exhausted `/tmp` (this seat's own `/tmp` writes fail `EDQUOT` at the
  same time while `df` shows 3.1 GiB free); generator v2 removed temp files and
  documents the relocation. S1/S2 are clean of the class.

## 4. Attacks / refutations attempted

- **Fixture attack** (planted tampered/missing/extra): all caught, exit 1;
  clean fixture exit 0. Verdict: instrument detects the classes, no false
  positives on a clean tree.
- **"146 scan misses" hypothesis** (S1): 146 unlisted files had mtimes hours
  before generation. Refuted by ctime forensics — those files were copied in
  at 10:02:39Z with preserved mtimes (`EX-13/_scratch/repo.git` object store;
  mtime 2026-10-19T01:50Z vs ctime 10:02:39Z). Verdict: post-generation writes,
  not misses; mtime-only audits are unsound here.
- **Vacuous-PASS attack**: the empty S0 snapshot self-reported PASS. An
  independent count of in-scope files (12+ at that time) refutes the PASS.
  Verdict: confirmed defect class — "0 entries OK" is a vacuous check; S0's own
  verify.log now records the FAIL, and v2's check-file verifies 107 rows.
- **Tamper-signature search**: scanned all 116 listed lines for
  ctime ≤ generated-utc failures → none. Verdict: no evidence of tampering.
- **Header-arithmetic attack**: recomputed entries count and byte sum from the
  rows → both MATCH (107 / 434028). Verdict: header self-consistent.
- **Self-reference check**: the manifest is not listed inside itself (footer
  says its sha256 is recorded in `seats/EX-14.md`). Verdict: unverifiable at
  report time — named gap in §5.
- **Duplicate/shared-digest review**: `EX-01/config-pre-pair.txt` ≡
  `receipts/config-pre-pair.txt` (`28491903…`, 4576 B — two identical c1
  pre-pair copies; the cross-chain pre-pair is a different artifact,
  `b8ed1936…`, 2045 B); RV-2 rerun probes share digests (`f2aec424…` ×4,
  `12e5d171…` ×2). Verdict: reproducibility evidence / redundant copy, not
  integrity defects.

## 5. Blockers and gaps

- `seats/EX-14.md` had not landed by 10:08Z, so the footer claim "manifest
  self: sha256 recorded in seats/EX-14.md" is **unverified by this seat**.
- The manifest is "regenerated until wave close": this report verifies snapshot
  S2 (`0afdb34e…`) only. If a later regeneration lands, re-run
  `claims/c1/SC-2/manifest-crosscheck5.py` (commands in the deliverable) — a
  live wave will exit 1 on post-generation churn; read the classified lines.
- `/tmp` on this host is quota-exhausted (`EDQUOT` with 3.1 GiB reported free)
  — fleet hazard for any seat writing scratch to `/tmp`; this seat's scratch
  lives in `/var/tmp/sc2/` and is not part of the repo.
- No other blockers; all checks that were run are reported with their outputs.
