# ConnectorOverlap — scoped report (R96-W1, read-only sibling-overlap scan)

Full findings and tables: `.ufo/waves/round-96/w1/ConnectorOverlap/overlap.md`.

## Summary & Verdict

1. **No sibling round-96 declaration overlaps kaidoku round-96.**
   - Only three sibling lanes have active or landed round-96 wave directories:
     - `kake-shokunin` (round 96): claims HTTP cache revalidation exchange contract v1 (`scripts/reval_exchange.py`, RFC 9111 §4.3) and strict self-assessment conformance (`c96_selfassess.py`, E1–E5).
     - `mori-shokunin` (round 96): claims SCORECARD `Last change` cells against fleet record (`tools/mori-scorecard-calibration.py`) and SOURCES registry pinned-copy re-verification (`tools/mori-source-digest.py`).
     - `lore-shokunin` (round 96, landed Oct 18): claimed obligation maps and dependency freeze over fictional response fixtures.
   - None of these siblings touches binary reverse engineering, UPX packing, kill-rule gate coverage, mandatory receipt enforcement, or receipt symlink write escapes.

2. **Fleet recurrence of unremediated receipt writers:**
   - The vulnerable v4 writer pattern (`temporary = destination + ".tmp"`, plain `open(temporary, "w")`, `os.replace(temporary, destination)`) that kaidoku discovered and remediated in R95/R96 remains live and unmitigated in sibling repositories.
   - Cleanest live instance: `kake-shokunin/scripts/instrument_receipts.py:643-646` (destination + ".tmp", plain open) at commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d` (active r96 tip), blob sha256 `162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7`.
   - Also live in: `tabi-shokunin` `aria-loopback-round13.mjs:103-105,805-807`, `tameshi-shokunin` `bash-witness-study.py:795-797`, `mori-shokunin` `mori-round13-regressions.py:572-574`, `kumitate-shokunin` `make-dispatch-actual.mjs:384-386`, and `kotodama-shokunin` `costume-era-consistency-gate.py:1494`.

3. **Fleet precedents for architectural solutions:**
   - **Durability (`fsync`):** `souji-shokunin` (round 60 amendment 3, `souji-receipt-write.py:530-575`) established the fleet's complete durability model: file-payload fsync (`os.fsync(f.fileno())`) followed by enclosing-directory fsync (`dfd = os.open(outdir, os.O_RDONLY); os.fsync(dfd)`), accompanied by `os.link` to fail on `FileExistsError` and prevent race clobbering.
   - **Receipt binding:** `kumitate-shokunin` (round 87–90, `scripts/receipt-bind.mjs`) solved the dirty-worktree laundering loophole exposed by Critic A14 by hashing instrument bytes from Git's object database (`git cat-file blob <rev>:<path>`) rather than reading disk bytes. `chousa-shokunin` (`tools/digest-in-tree.py` / `receipt-pin.py`) similarly enforces that all pinned digests exist as committed Git blobs.

---

## Scan Results Summary (20 sibling lanes, read-only)

Explicit scans across 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kaidoku-shokunin`):
- `tools/` (8 lanes) and `scripts/` (3 lanes):
  - `'kill rule'`: 9 files, 13 matches (exit 0)
  - `'mutant'`: 98 files, 983 matches (exit 0)
  - `'survivor'`: 73 files, 350 matches (exit 0)
  - `'gate coverage'`: 3 files, 4 matches (exit 0)
  - `'fsync'`: 17 files, 19 matches (exit 0)
  - `'json-out'`: 4 files, 5 matches (exit 0)
  - `'selfverify'`: 0 files (exit 1)
  - `'receipt-required'`: 0 files (exit 1)
  - `'fresh'`: 293 files, 1392 matches (exit 0)
  - `'held-out'`: 39 files, 48 matches (exit 0)
  - `'upx'`: 0 files (exit 1)
- `corpus/` (20 lanes):
  - `'kill rule'`: 533 files, 1043 matches (exit 0)
  - `'mutant'`: 2929 files, 18779 matches (exit 0)
  - `'survivor'`: 970 files, 2585 matches (exit 0)
  - `'gate coverage'`: 13 files, 14 matches (exit 0)
  - `'fsync'`: 25 files, 69 matches (exit 0)
  - `'json-out'`: 5 files, 8 matches (exit 0)
  - `'selfverify'`: 0 files (exit 1)
  - `'receipt-required'`: 0 files (exit 1)
  - `'fresh'`: 5098 files, 38757 matches (exit 0)
  - `'held-out'`: 106 files, 282 matches (exit 0)
  - `'upx'`: 4 files, 4 matches (all non-packer tokens; exit 0)

---

## Proposed Move (One Bounded Synthesis across the Round's Proposals)

Synthesizing SentinelWrite F3/F5, CriticC1 A14/K3, ScoutS321, and the sibling scan evidence:
In the R96-C2 craft block 35 decision table, the round-96 knowledge entry (`corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md`), and the round-96 lesson (`corpus/lessons/round-96.md`) that the L1 lands at integration:
1. **Ground the `writer durability gate` row in block 35 and QUALITY 193 in the two-level durability model:** Cite `souji-shokunin` r60's precedent (`os.fsync(f.fileno())` payload sync + `os.fsync(dfd)` directory-entry sync), and explicitly document parent-directory fsync and fsync-before-replace call ordering as named architectural limits of the v6 in-process check.
2. **Ground the `head-not-bound` / unbound-field class in `kumitate`'s `receipt-bind.mjs` precedent:** Document in the round-96 lesson and knowledge entry that commit-id binding (`head == revision`) still admits dirty working-tree laundering (as demonstrated by Critic A14 on the pre-supersession honest receipt), whereas true byte-binding requires reading bytes via `git cat-file blob <rev>:<path>` as kumitate does. This elevates kaidoku's calibration limit from a single-lane accident into a fleet-standard architectural boundary.
3. **Cross-cite the persistent unremediated sibling writer (`kake-shokunin/scripts/instrument_receipts.py` at commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d`, blob sha256 `162dd685…`) in the round-96 knowledge entry alongside S320/S321:** Record that while kaidoku closed M95-i with `symlink-probe-v2` and `stop-boundary-repair-battery-v6`, the defect remains unmitigated across sibling tools.

**Affected Axes:**
- **Depth (R96-C2):** Gained by rooting craft block 35 and knowledge in fleet-wide durability and binding contracts rather than local single-lane anecdotes.
- **Freshness:** Anchored to live 2026-11-05 sibling commits and digests.
- **Calibration (R96-C1):** Properly bounds the v6 in-process `head` check against dirty-worktree laundering.
- **Zero harm to C1/C2 frozen surfaces:** Touches no frozen byte in `tools/round-96`, `mutants.json`, `forgery/`, or `pins.sha256`.

---

## Risks & Explicit Contradictions

- **Sibling mutability mid-wave:** `kake` is running an active round-96 wave; citations are pinned to commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d` and blob sha256 `162dd685…`.
- **Contradiction in `head` binding:** Kaidoku's v6 `head` binding claims to bind the measured world, but Critic A14 proved it binds only the Git commit pointer, not the working-tree bytes that actually ran. Kumitate's architecture contradicts kaidoku's in-process `head` check by proving that true binding requires `git cat-file blob`.
- **Contradiction in `K-fsync`:** `K-fsync` claims to verify the durability gate (killing M2), but Sentinel F3 proved it only checks call count >= 1 without checking whether fsync occurred before replace, and Sentinel F5 proved v6 lacks parent directory fsync.

---

## Files Written

- `.ufo/waves/round-96/w1/ConnectorOverlap/overlap.md` (full scan data, tables, second-order traces, and verification commands)
- `.ufo/waves/round-96/w1/ConnectorOverlap.md` (this report)
