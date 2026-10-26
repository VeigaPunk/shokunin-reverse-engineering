# Round 39 — standard BE SquashFS v4 to Core with the symlink rule stated before data; an executable outcome-triage table scored on a held-out set seeded by the freeze

Base `a2f64e1da78afcf8cc39287106604dbcc270844c`. Freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`
(`plans/round-39-claims.md`, all round-39 tools, carriers, oracles, symlink tables, the SKILL triage
table and its entry, SOURCES S118–S121, wave-1 evidence). Control receipts
`72359309a052284029f8e0331ef211a67fe4b13b` (C1: 9 controls, C2: 8 controls; none meets its target).
Data: C2 held-out `3c07eed7da595b815ce3064dcb12bd5c0788e564`, C1 receipts and Core landing
`6fdaf4f162aff156fcef0e52998a5469c64fd6f0`. L1 `KaidokuR39`. Wave 1: 43 seats, pre-freeze build,
recon and attack of the draft (`.ufo/waves/round-39/w1/`).

Author verdicts (closure pending):

- **R39-C1 met.** `tools/round-39/c1-counter.py` at `6fdaf4f1`: `carriers_matched 6`, every binding
  true, exit 0 (`.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json`). Before: 0/6, exit 1 at the
  freeze (`.ufo/waves/round-39/controls/ctl-c1-0-do-nothing.json`). The counter cannot refuse a
  fabricated receipt whose evidence id is re-minted: control CTL-C1-3 reaches 6/6 carriers and fails
  only on a documentation binding (`controls/ctl-c1-3.json`). That limit was disclosed in the freeze;
  provenance rests on the wave-2 independent re-runs.
- **R39-C2 met.** `tools/round-39/c2-counter.py` at `6fdaf4f1`: `matched 20` of `n 20`, every binding
  true, exit 0 (`l1/scores/c2-at-6fdaf4f1.json`). Before: exit 2 `no_manifest_at_rev` at the freeze and
  no table at the base. The best pre-data shortcut table scored 12/20 on the development envelopes
  (`controls/ctl-c2-dev-scores.json`).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M39-1 | negative existence claim swept from the wrong root (routed R38-CL1) | round-38 lesson `:80-82`, `:96-97`: "exists nowhere on this host" from a `find` rooted at `/home/vgpnk/Projects/shokunin`; both tsvs exist under `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round{7,9}/work/` | none (56/57 cover spellings and scope, not the root) | QUALITY 82 + `tools/round-39/absence-sweep.py`: fleet root → exit 0 ABSENT, adding the shokuknow root → exit 1 PRESENT on both claims (`.ufo/waves/round-39/l1/absence/summary.txt`); `--selftest` 18 cases |
| M39-2 | routed defects dropped between rounds instead of carried with a state | `R36-CL2..CL6` named in `corpus/lessons/round-36-verifier-spotcheck.md:196-212`, absent from the round-38 lesson and report; `R38-CL1..CL4` absent from the round-39 draft (`w1/artifacts/R39MistakeHunt/routed-ledger-runs.txt`, exit 1) | none | the `## Routed defects` ledger below carries every id with a state; `w1/artifacts/R39MistakeHunt/routed-ledger.py --selftest` green/red |
| M39-3 | wave reports uncommitted until the round's last commits, so an L1 death depends on the workspace surviving | round-38 attempt-1 tip `077e212b` holds 0 files under `w1/` (`git ls-tree -r 077e212b -- .ufo/waves/round-38/`) | none | round 39 commits wave 1 in the freeze commit `8fcda41c` (43 reports); `w1/artifacts/R39MistakeHunt/wave-checkpoint.py` red on `077e212b`, green on a committed wave |
| M39-4 | control receipts re-scored in place after an amendment; a drop-one-carrier control degenerated to do-nothing while still exiting 1 | round-38 `controls/ctl-c1-1-three-carriers.json` 3 → 0 between `efd5c47a` and `7e979514` (`w1/artifacts/R39MistakeHunt/control-bind-runs.txt` C1/C2) | QUALITY 80 (partly) | round-39 control receipts name the freeze in their argv and land in their own commit `72359309` before data; `control-bind.py --selftest` green/red |
| M39-5 | a fix typed into one wave context lapses next round (recurrence of M36-6) | "No `find`/`du` under `/fast/scratch`" present in the round-36 w2 spec only (`w1/artifacts/R39MistakeHunt/context-rules-runs.txt` D1–D3) | none | the round-39 wave-2 generator carries both rules; `context-rules.py` red on `w1-spec.json`, green on `w2-spec.json` |
| M39-6 | a draft predicate's classification sentence would have failed an honest carrier: "POSIX join against the image root /" clamps `..` and calls K1's escaping link in-tree | `w1/R39C1SymlinkK1K4.md` §5, `w1/R39C1AxisFit.md` (d.0) | wave-1 pre-freeze attack | frozen rule is extraction-root containment (S122 `is_safe_path`, no clamping); `tools/round-39/sqfs-list.py` symlink tables equal the frozen K1/K2 tables |
| M39-7 | the lane's own carrier writer mis-encoded non-ASCII names and labelled raw LZMA2 as compression id 2 ("xz"), so a carrier called xz exercised no xz decoding | `w1/R39Sentinel.md` 1–2; `w1/R39C1CarrierK5.md` §7; `w1/R39C2HeldoutGen.md` §3 | none | `tools/round-39/gen-squashfs.py`; K6 rebuilt with a compressible file: `sqfs-list.py --inspect` reports compression `xz`, 4 compressed data blocks; the C1 `xz_leg` binding reads the superblock id |
| M39-8 | a seat's shell fell back to the fleet root and wrote three curl outputs there | `w1/R39SrcSasquatch.md` §8 (self-reported, removed by the seat) | the §3 misroot sweep | `git -C /home/vgpnk/Projects/shokunin status --porcelain` before the report shows no round-39 file |
| M39-9 | a wave-2 seat wrote its report into the fleet repo (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-39/w2/R39W2HeldReproB.md`): every prompt carried a lane-relative `Report:` trailer and the context's absolute anchor | `w2/R39W2Sentinel.md` F1 | the §3 misroot sweep | moved into the lane (`cmp` equal, sha256 `d37db669430d681e84e8543fbae6fc4c870a23e417158473497d5f13f120482a`), fleet copy deleted; `git -C /home/vgpnk/Projects/shokunin status --porcelain` shows no round-39 file afterwards |
| M39-10 | two wave-1 seats kept editing their reports and one artifact after the freeze commit had captured them, and one committed carrier was deleted from the worktree | `w2/R39W2Sentinel.md` F2 (edits 14:13:30-14:14:45 after `8fcda41c` at 14:12:51) | none | freeze bytes restored at the original paths; late edits and diffs kept in `.ufo/waves/round-39/w1/_post-freeze-edits/`; `git status --porcelain` on `w1/` empty before the final commit |

## Gate

### Sources opened this round (2026-10-26)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S118 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py | 2026-10-26T16:39:23Z (`w1/R39SrcUnblobSymlink.md`) | "either removed it it attempts to traverse outside of the extraction directory or rewritten to be fully portable" (docstring, lines 51-56) |
| S119 | https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | 2026-10-26 (`w1/R39SrcReaGapKinds.md`) | "Extractor executables named by the producer; empty when it named none." (`dist/domain/firmware/firmwareAnalysis.js:100`) |
| S120 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py | 2026-10-26 (`w1/R39SrcUnblobReports.md`) | "Describes an error when failed to run the extraction command" (`report.py:91-98`) |
| S121 | https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c | 2026-10-26 (`w1/R39SrcSasquatch.md`) | "CFLAGS=-DFIX_BE dh_auto_build" (`debian/rules` lines 15-18 at the same tag) |
| S122 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/file_utils.py | 2026-10-26T17:09:05Z (L1) | "basedir.joinpath(path).resolve().relative_to(basedir.resolve())" (`is_safe_path`, lines 34-39) |

Registry: 117 → 122 rows, appends plus one used-by change: S112 used-by
`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` → that entry plus
`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`, which cites S112 (found by `w2/R39W2Census.md`;
CORPUS rule 2 allows used-by changes; `tools/round-38/registry-immutable.sh` exits 0). Admitted as sources, all tier A, status `mined`. Rejected candidates: the sasquatch
seat's draft row carried an escaped `\|`, rewritten without pipes; the unblob-reports seat's
one-row-for-five-files draft was narrowed to `report.py` + `command.py`.

### Assimilation

`Assimilation: none` adopted this round. The AVM theme in `/home/vgpnk/Projects/shokuknow/merge/kaidoku`
was scanned (`w1/R39AssimAvmScout.md`, `w1/R39AssimAvmCritic.md`). The two seats disagree on the one
admissible entry: the scout would admit `avm-firmware-image-unblob` with four corrections, one of them a
falsified headline; the critic finds its shared mechanism sentence ("the AVM marker is invisible to
unblob") falsified by the pinned handler and would admit only `avm-image-extraction` after
re-grounding. Both reject `avm-image-build-blocker` and `avm-le-variant-reachability` (stale premises,
refuted by bytes opened this round). Decision: reject those two; defer both admit candidates (flip: one
entry re-grounded on lane receipts against a real AVM image). Id-collision guard proven on an indented
fixture (`w1/artifacts/R39AssimAvmScout/`). Quarantine slice: 5 rows, byte-identical to round 38, all
five verdicts re-opened (`w1/R39Quarantine.md`). Correction (`w2/R39W2Quarantine.md`): four hold; S150's
"refuse (fabrication)" holds only for the register's tested heading — the row's gate quote and second quote
are present on the live page, so under this prompt's rule (present → adopt with the anchor located) the
defensible disposition is re-anchor, not refuse. Nothing is appended this round; the flip is recorded for
the next assimilation round.

## Corrections to round 38

Append-only; the round-38 text is not rewritten.

- `sasquatch-unblob-compatibility-precondition` (round-38 lesson `:80-82`): withdrawn — "exists nowhere
  on this host". `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round7/work/r7-local-measurements.tsv`
  exists (1204 B, sha256 `d8fa9eae176afd371a930acaca94991d841084f3a50929935a7ada0dbd98af6d`). The refusal
  stands on the surviving grounds: its central row (sasquatch absent from PATH) was true on 2026-10-24
  and false since the round-36 install; the lane's own BE receipts falsify its load-bearing sentence;
  it is a campaign-local snapshot, not a published source.
- `sasquatch-unblob-avm-branch` (round-38 lesson `:96-97`): withdrawn — "exist nowhere on this host".
  `…/round9/work/lead2-avm-branch.tsv` exists (1177 B, sha256
  `709cddc7aa37b143da9607a8183b48878b33b1c33d015db1463b76d4dea1ea43`). The refusal stands on the unpinned
  `unblob/main` reference, the falsified closing premise (AVM publishes images: HTTP 200) and the
  campaign-local provenance. Detail: `w1/artifacts/R39CL1Correction/correction-block.md`.
- Round-38 report `:88` (R38-CL3): "would have turned C1 green (v3: 4/4)" should read "would have made
  C1 carrier-green (v3: 4/4 carriers), not claim-green: `met_target false`, no Core row".

## Routed defects

| id | state | where |
|---|---|---|
| R38-CL1 | fixed | corrections above; QUALITY 82; `tools/round-39/absence-sweep.py` |
| R38-CL2 | fixed | `tools/round-38/{freeze-drift.py,intended-doc.py,registry-immutable.sh}` gain `--selftest` (8, 9, 5 cases); `SKILL.md` `### Round-35/37/38/39 instrument registry`; `registry-immutable.sh` now also refuses a deleted or reordered row |
| R38-CL3 | fixed | corrections above (the fleet report is not edited) |
| R38-CL4 | fixed | `plans/round-39-claims.md` `## Freeze-integrity rule`: any touch of a frozen path after the freeze blocks a score; both counters exit 2 `frozen_path_changed` |
| R36-CL2 | fixed | `PROVINCE.md` round-39 frontier note names `2026-10-26-r36-sasquatch-squashfs-recursion` |
| R36-CL3 | superseded | round-39 counters: C1 selftest red cases fail on their own clause (`w1/R39C1Counter.md`); the re-minted fabrication limit stays disclosed |
| R36-CL4 | fixed for round 39 | the freeze lists every frozen path (claims `## Freeze-integrity rule`) and `carriers.json` pins them |
| R36-CL5 | open | not addressed this round |
| R36-CL6 | fixed for round 39 | C1 binds receipts by `subject.digest.sha256` (`subject_pin_ok`), never by `local_path` |

## Criteria added

- QUALITY 82 (M39-1).

## Wave 2 (39 seats, after the landing)

Both claims reproduce: C1 6/6 and C2 20/20 re-scored at `6fdaf4f1` and `52b0eb29`
(`w2/R39W2C1Rescore.md`, `w2/R39W2C2Rescore.md`); six independent REA re-runs reproduce every C1 receipt
(`w2/R39W2ReproK{1..6}.md`), four seats reproduce all 20 held-out envelopes and their labels
(`w2/R39W2HeldRepro{A,B,C,D}.md`), K5/K6 rebuild byte-for-byte (`w2/R39W2K5K6Rebuild.md`), the held-out set
regenerates from the freeze seed, and the two claims are separable (`w2/R39W2Separability.md`). Limits found,
recorded rather than repaired in frozen bytes: a re-minted fabrication reaches 6/6 on the C1 counter
(`w2/R39W2C1Fabricate.md`, the disclosed limit); a table with no `-be` and no `symlink removed` cell reaches
16/20, an 8-row table reaches 20/20, and the `cause -> action` column is unscored (`w2/R39W2C2Shortcut.md`,
`w2/R39W2C2AxisFit.md`); 18 of 39 interpreter mutants and 9 counter mutants survive their detectors
(`w2/R39W2TriageMutants.md`, `w2/R39W2C2Mutants.md`); two table rows exclude measured outcomes and two causes
are over-specific (`w2/R39W2C2TableReview.md`, recorded in the triage entry). Repaired in the final commit:
the SCORECARD round-39 record, PROVINCE `:157`/`:376` pointers, the S112 used-by, the registry-immutable
registry cell, the BE entry's before-arm wording, M39-9 and M39-10.

