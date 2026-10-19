# manifest-crosscheck.md — independent re-hash of chain-c1 MANIFEST.draft

Seat **SC-2** (scribe), wave `arc3-loop1-round1`, chain **c1**. Task: independently
recompute the sha256 of every file EX-14 lists and flag mismatches/missing files.

Method: Python `hashlib.sha256` per file (not `sha256sum`), size-byte comparison
against the manifest's own SIZE_BYTES column, header arithmetic (entries /
total-bytes), declared-scope audit, staleness classified by **ctime**.
Instrument: `claims/c1/SC-2/manifest-crosscheck5.py`
(sha256 `cf56eab33ae3e9d501b5f1feb9ec1682115118b4a92f526a259817b819e46477`).
Raw outputs: `claims/c1/SC-2/crosscheck-run3.txt`, `crosscheck-run5.txt`,
`checkfile-run4.txt`.

## Snapshot under test

`claims/c1/receipts/MANIFEST.draft.txt`
sha256 `0afdb34e650237600267acd96254bf5111777eb87ec039f31ce44323c3bbeef6`,
generated 2026-10-19T10:04:54Z, repo-HEAD `e845c2b`.
Bytes verified at 10:06:30Z (run3) and 10:07:4xZ (run5); hash unchanged across
both runs. Copy of the exact bytes checked:
`claims/c1/SC-2/MANIFEST.draft.snapshot-S2-0afdb34e.txt` (sha256 matches).

## Verdict

**Snapshot internally consistent; 7 of 116 listed lines do not reproduce at
check time, all classified as live-wave churn, none as tamper or scan error.**

- 116 listed lines parsed = 107 section-1 rows + 1 custody pre-pair + 5 live
  custody lines + 3 footer lines.
- Header arithmetic **MATCH**: `entries: 107` = 107 section-1 rows;
  `total-bytes: 434028` = Σ SIZE_BYTES of those rows (independently summed).
- 107/116 reproduce (digest + size) at the final measurement (run6, 10:14Z);
  9 problems: 1 MISSING, 8 MISMATCH. Earlier run5 (10:07:4xZ) read 109/116.
- Scope audit: **0 undeclared unlisted files predating generation** — no scan
  misses. 220 unlisted at run6, all ctime > generated-utc (live writes).
- Declared exclusions honored: 360 files under `claims/c1/EX-13/_scratch`
  (section 1b `roots:`) are declared-excluded and were excluded by this audit.
- Custody entry `claims/cross/receipts/config-pre-pair.txt` verifies
  (`b8ed1936…`, 2045 B); the 5 live custody digests in section 2 reproduce
  against the live files at check time.

### Problems flagged (run6, 10:14Z — final measurement on snapshot 0afdb34e)

| class | path | evidence |
|---|---|---|
| MISSING | `claims/c1/EX-08-search.js` (line 42) | path moved: content now at `claims/c1/EX-08/EX-08-search.js`, digest `d4a21a24…` and 2145 B **identical to the manifest's row** — path churn, not data loss |
| MISMATCH | `claims/c1/EX-06/evidence/repro.sh` | ctime 10:09:09Z > gen; 5791 B → 6033 B |
| MISMATCH | `claims/c1/EX-06/evidence/transcript.txt` | ctime 10:09:31Z > gen; **same size 9442 B, different digest** — caught only by hashing |
| MISMATCH | `claims/c1/EX-14/attack-manifest-integrity.sh` | ctime 10:05:32Z > gen |
| MISMATCH | `claims/c1/EX-15/containment.md` | ctime 10:06:01Z > gen |
| MISMATCH | `claims/c1/RV-2/poll-log.txt` | ctime 10:06:08Z > gen |
| MISMATCH | `claims/c1/receipts/chain-ledger.draft.md` | ctime 10:13:26Z > gen; 11401 B → 15811 B |
| MISMATCH | `claims/c1/records-drafts/LOG-entry-draft.md` | ctime 10:05:21Z > gen (9818 B → 9817 B) |
| MISMATCH | `claims/c1/records-drafts/SCORECARD-section-draft.md` | ctime 10:05:14Z > gen (6057 B → 7818 B) |

Resolutions from the earlier run5 set (same snapshot): run5's MISSING
`claims/c1/EX-07/__pycache__/selector-recon.cpython-314.pyc` reappeared at
10:10:13Z with matching content (recompiled byte-identical), and run5's
`EX-07/reconcile.py` mismatch is superseded — both are the transient-bytecode /
rewrite churn class. EX-14's own `sha256sum -c` at 10:07 agreed on the
then-current 7 failures (`checkfile-run4.txt`).

Every MISMATCH carries `ctime > generated-utc`: the file was rewritten by its
owning seat after the snapshot was taken. No file with `ctime <= generated-utc`
failed to reproduce, i.e. **no pre-generation content error and no
tamper signature** in this snapshot. The manifest is explicitly a DRAFT
("regenerated until wave close"), so these are staleness, not defects; they
still must be re-verified on the final regeneration.

Exact digests for every flagged row are in `claims/c1/SC-2/crosscheck-run6.txt`
(expected vs actual per line); run5's set is in `crosscheck-run5.txt`.

## Snapshot history (three generations observed in this seat)

| # | generated-utc | manifest sha256 | section-1 rows | cross-check result |
|---|---|---|---|---|
| S0 | 09:59:40Z | superseded (bytes not retained by this seat) | **0** | **defect: empty listing + vacuous PASS** |
| S1 | 10:01:21Z | `d6336a17…` | 34 | at 10:03:40Z: 37/43 lines verified, 6 post-generation rewrites, 227 unlisted |
| S2 | 10:04:54Z | `0afdb34e…` | 107 | 10:06:30Z 110/116; 10:07:4xZ 109/116 (7 problems); 10:14Z 107/116 (9 problems); no regeneration since 10:04:54Z as of 10:18Z |

S0 evidence (durable): `claims/c1/EX-14/verify.log:1-3` records
`status FAIL … no properly formatted checksum lines found`, and the S0
footer's check-file digest `e3b0c442…` is the empty-file digest. Root cause,
evidenced not guessed: generator v1 used `mktemp` temp files for the scan
(`claims/c1/EX-14/manifest-gen.sh` @ `658eb0d8…`, pass-1/pass-2 blocks);
`/tmp` on this host is a tmpfs under an exhausted per-user quota — this seat's
own writes to `/tmp` fail `EDQUOT` while `df` reports 3.1 GiB free (measured
10:0xZ). Generator v2 (`bcba2ad8…`) removed temp files entirely and documents
the scratch relocation in its section 1b rationale; S1/S2 are clean of the
class. The vacuous-PASS shape (a verification that passes because it checked
zero entries) is the fleet-relevant finding.

## Method findings worth carrying

1. **mtime is unsound for staleness classification; use ctime.** In S1, 146
   unlisted files looked pre-generation by mtime (e.g. 2026-10-19T01:50Z) but
   their ctime was 10:02:39Z — they were copied in with preserved mtimes
   (`claims/c1/EX-13/_scratch/repo.git` objects). An mtime-only audit would
   have reported 146 false "scan miss" alarms. ctime (write instant) is the
   discriminator; both are printed by the instrument.
2. **Shared digests are informational, and here they are corroboration.**
   `claims/c1/EX-01/config-pre-pair.txt` ≡ `claims/c1/receipts/config-pre-pair.txt`
   (`28491903…`, 4576 B — two identical copies of the c1 pre-pair; the
   cross-chain pre-pair is a different artifact, `b8ed1936…`, 2045 B).
   RV-2 probe reruns share digests (`f2aec424…` across 4 files; `12e5d171…`
   across 2) — reproducibility evidence, not duplication defects.
3. **Scope churn**: S2 listed a `__pycache__/*.pyc` that was deleted before
   run5 — transient bytecode is inside the declared scope and churns. EX-14
   already carved out `_scratch/`; `__pycache__` deserves the same treatment
   (patch text below).
4. Duplicate path `claims/c1/EX-14/manifest-gen.sh` at lines 47 and 143 is the
   intended footer self-reference, not a defect.

## Proposed change (patch text, NOT applied)

For `claims/c1/EX-14/manifest-gen.sh`, in the `scan()` exclusion array, add the
bytecode-cache exclusion beside the `_scratch` one:

```diff
-  [ "$INCLUDE_SCRATCH" = "1" ] || scratch_excl=( ! -path '*/_scratch/*' )
+  [ "$INCLUDE_SCRATCH" = "1" ] || scratch_excl=( ! -path '*/_scratch/*' ! -path '*/__pycache__/*' )
```

No other change proposed; nothing in the repo was modified by this seat.

## Reproduce

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$PWD/.ufo/waves/arc3-loop1-round1
sha256sum $W/claims/c1/receipts/MANIFEST.draft.txt      # expect 0afdb34e… for S2
python3 claims/c1/SC-2/manifest-crosscheck5.py \
  $W/claims/c1/receipts/MANIFEST.draft.txt $W "$PWD" $W/claims/c1
(cd $W && sha256sum -c claims/c1/EX-14/MANIFEST.draft.check.sha256)
```

Exit code is 0 only for a fully clean snapshot; a live wave will exit 1 on
post-generation churn — read the classified lines, not the exit code alone.
