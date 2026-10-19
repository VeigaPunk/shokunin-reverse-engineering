# EX-32 pre-pair metadata — arc3-loop1-round2 (chain c3, executor)

Seat task: FIRST ACTION after EX-31 lands — run the tool's capture mode as the
round's authoritative PRE-PAIR (before any other C3 live work); save to
`claims/c3/receipts/config-pre-pair-v2.txt`. Artifact + seat report.

- **Authoritative PRE-PAIR**: `.ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt`
  - captured-utc `2026-10-19T12:04:06Z`, exit 0, `paths=5/5`
  - receipt sha256 `fa9706c6f036e882ee1fe9e8589c4aa9fa7e60de65c6eaf4e2c8ac0949eba1c9`
  - sidecar (tool-written) `config-pre-pair-v2.txt.sha256` = same digest, 89 B
  - receipt embedded `repo-HEAD: 14b1682b1128d2e41085ebc79c9addeb8786d420`
  - receipt embedded `tool sha256 4862f6426a7589cf239da9c46af6db4140c381d2d6bfe0cbc06bcc84a62f2a29`
- **Tool**: `.ufo/gates/custody-pair/custody-pair.py` (EX-31's authorized real target)

## Tool revision timeline (observed, first-sight samples)

| t (UTC) | sha256 (12 hex) | size (B) | note |
|---|---|---|---|
| 12:03:47 (sighted) | `9aad4c5a6330` | 38917 | first sight after landing; in-flight |
| 12:04:00 (mtime) | `4862f6426a75` | 38651 | **revision that produced the authoritative receipt** |
| 12:04:38 (recapture) | `72d5231f7cfc` | — | recapture at this revision is payload-identical (see below) |
| 12:04:40 (mtime) | `b10ad1c8…` | 38981 | mid-edit state: `verify --live` crashed (KeyError `'sha_agree'`, `custody-pair.py:512`); selftest DIRTY 6/15; capture still exit 0 |
| 12:05:19 (mtime) | `112d01dc034c` | 39157 | healthy; stable through 12:07:22+ (`verify` MATCH, selftest CLEAN 15/15) |

Evidence: capture header (self-recorded tool sha), `battery-B1-B2.log`,
`churn-snapshot-1207Z.log`, `recapture-drift.log`.

## Commands run (verbatim key lines; full logs in this directory)

```sh
python3 .ufo/gates/custody-pair/custody-pair.py capture \
  --out .ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt \
  --label "arc3-loop1-round2 PRE-PAIR authoritative (EX-32; before any other C3 live work)"
# → CUSTODY_PAIR_CAPTURE: OK paths=5/5 label=… exit=0        (12:04:06Z)

python3 .ufo/gates/custody-pair/custody-pair.py verify <receipt> --live   # rev 112d01dc, 12:07:03Z
# → VERDICT: MATCH  paths=5  MATCH=5  exit=0 ; SHA256-CONTRACT: 5/5 paths agree

python3 .ufo/gates/custody-pair/custody-pair.py selftest                  # rev 112d01dc
# → CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0
```

## Receipt content (per-stanza fields)

`PATH, EXISTS, TYPE, SIZE, SHA256, MTIME_EPOCH, MTIME_NS, MTIME_UTC_RENDER,
MTIME_LOCAL_RENDER, CTIME_EPOCH, CTIME_NS, CTIME_UTC_RENDER, CTIME_LOCAL_RENDER,
INODE, MODE, UID, GID`; header declares `receipt-version: 2`, the label contract
(UTC renders = `gmtime(epoch)`; local renders separate) and the compare contract
(sha256 = content identity; inode+ctime(+ns) = rewrite identity; atime
deliberately not captured). 5/5 stanzas, all `EXISTS: yes`.

## Cross-checks (all independent of the tool)

- **sha256 5/5 identical** to round-1 pinned digests
  (`.ufo/waves/arc3-loop1-round1/claims/c1/receipts/config-pre-pair.txt:29-33`)
  and to RV-12's 12:01:12Z independent capture
  (`claims/c3/RV-12/independent-pre.txt`): 15/15 digests agree.
- **inode/size/mode 5/5 equal** to round-1 metadata table and to my own lstat at
  12:01:48Z (`lstat-ground-truth-120148Z.txt`); ctime_epoch == mtime_epoch on
  all 5 paths at baseline.
- **Label arithmetic PASS 5/5** (`label-arithmetic.log`): every
  `MTIME_UTC_RENDER` equals `date -u -d @epoch` and every
  `MTIME_LOCAL_RENDER` equals the local `%:z` render — the round-1 label defect
  is gone in v2 output.
- **Cross-revision payload stability**: recapture at 12:04:38 (rev `72d5231f`)
  and 12:07:34 (rev `112d01dc`) are byte-identical to the authoritative receipt
  except the `# tool:` + `# captured-utc/local:` header lines
  (`recapture-drift.log`).
- **Receipt integrity re-checked** at 12:07:49Z: sha256 still `fa9706c6…`,
  sidecar matches.

## Scratch attacks (own scratch file; no custody path touched)

Log `battery-A-rewrite.log`. Byte copies of real custody paths were NOT made by
this seat (EX-33 carries the full attack); the scratch file carries my own
content.

| # | Injection | Tool verdict | Exit |
|---|---|---|---|
| A0 | control: capture vs live | MATCH 1/1 | 0 |
| A1 | in-place same-content rewrite | REWRITE-DRIFT, `moved=mtime_ns` | 11 |
| A2 | mv same-content rewrite (new inode) | REWRITE-DRIFT, `moved=inode,mtime_ns` | 11 |
| A3 | round-1 v1-stanza receipt vs live | `SHA256-CONTRACT: 5/5 paths agree` + per-path `LABEL-DEFECT` diagnosis; verdict METADATA-DRIFT | 12 |
| A4 | v1-stanza receipt vs my v2 receipt (cross-format) | same as A3 | 12 |

ns-level evidence: A1 moved `MTIME_NS` and `CTIME_NS` (epoch seconds equal, so
seconds-only comparison would have been blind); A2 also moved `INODE`
(10992341 → 10992346) while sha256 stayed `e49c81e2…`.

## Named risks / caveats

1. **Cross-revision pair**: the pre-pair was produced by rev `4862f642` (mtime
   12:04:00). If EX-31 revises again, the post-pair will come from a later
   revision; payload stability across three revisions is measured (all
   recaptures byte-identical modulo header), and `verify` compares payload
   fields, not tool identity — so the pair remains comparable, but downstream
   records must quote the receipt's embedded tool sha, not "the tool hash".
2. **Mid-edit crash window**: rev `b10ad1c8` (12:04:40) crashed `verify --live`
   and failed 9/15 selftest cases while `capture` still returned exit 0. Seats
   racing an in-flight EX-31 revision can observe transient failures; re-run
   `selftest` before trusting any run.
3. This seat did not re-capture the pre-pair after the tool's first revision
   because the mandate is "the first C3 live use, before other C3 live work" —
   the 12:04:06 capture holds that position; the 12:07:34 recapture corroborates
   it.
