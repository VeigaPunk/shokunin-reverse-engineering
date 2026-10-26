# kaidoku round 38 — frozen claims (freeze v2)

Base `77091b492cc53f8743bd0701b1e7d5e66123dd84` (lane `main`; the verifier's round-37
spot-check commit `67632844` sits above it and changes no scored surface). L1 `KaidokuR38`
holds the §3 planner seat; the round is a relaunch of round 37 (honest stop at the pre-freeze
probe stage, `plans/round-37-claims.md`), carrying the routed defects R37-CL1..CL3 and
R36-CL1..CL6.

**Freeze v2 note (pre-scoring amendment):** the first freeze (v1) declared the round-37
missing-extractor-dependency before-arm "does not reproduce" and framed the after-arm as "no
external extractor dependency". Wave-1 discovery (R38CrossToolK1, measured) falsified that
premise: unblob 26.6.4's `SquashFSExtractor` requires `sasquatch-v4be` on PATH for BE v4;
the dependency-gap before-arm reproduces when `~/.local/bin` is absent from PATH (the L1's
v1 probes never actually stripped `~/.local/bin` — `grep -v sasquatch` filters PATH component
names, not the binaries inside them). This v2 freeze restates P38-C1 with paired before
receipts and the dependency premise. No claim was scored under v1; v2 is the frozen bytes
every receipt and score now complies with. Kill rules apply to the v2 controls.

Owned axes coverage/depth/calibration are tied at 10, none retired; R38-C1 works coverage
(lowest-axis rule met), R38-C2 works calibration.

## R38-C1 — coverage: standard big-endian SquashFS v4 moves from Frontier to Core

Surface moved: `PROVINCE.md` `### Round-4 frontier (post-unlock)` bullet **sasquatch** notes
"big-endian/AVM stays here" (`PROVINCE.md:156-157`), the round-36 Core row's aside
"`sasquatch-v4be` is its big-endian sibling, unmeasured" (`PROVINCE.md:372`), and
`corpus/README.md` `## Frontier` bullet ("Still frontier: big-endian/AVM (`sasquatch-v4be`)
and vendor-mangled images"). REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4) with
`sasquatch-v4be` 4.5.1 available runs the `squashfs_v4_be` handler and publishes every oracle
file on standard BE v4 carriers.

Command that shows it unmoved: the counter below at the base exits non-zero.

**Predicate P38-C1.** At the measured revision, for each of the four frozen big-endian
SquashFS v4 carriers, the committed REA extract-firmware after-receipt (run with
`sasquatch-v4be` available, as unblob 26.6.4's `SquashFSExtractor` requires) publishes every
regular file of the frozen independent oracle (same relative-path suffix, same sha256), names
the `squashfs_v4_be` handler, carries no extraction gap, and recomputes to its stored evidence
id under the rea-agents 6.5.0 rule; the paired committed before-receipt (run with
`sasquatch-v4be` unavailable) publishes none of them and names `sasquatch-v4be` as a missing
extractor dependency; `PROVINCE.md` holds a round-38 Core row naming `squashfs_v4_be` that
cites the round-38 knowledge entry, which cites a `SOURCES.md` row opened 2026-10-26 whose
used-by lists that entry; the round-38 frontier note supersedes the big-endian Frontier bullet;
and `corpus/README.md` holds a coverage-map row naming the entry stem.

- Carriers (frozen, `.ufo/waves/round-38/c1/carriers.json`): K1/K2 synthetic standard-BE v4
  gzip images (`tools/round-37/gen-squashfs.py`); K3/K4 the unblob 26.6.4 `squashfs_v4_be`
  integration fixtures. All four are committed bytes at the base; sha256 pins frozen.
- Oracle (frozen, committed at the base): K1/K2 = the source trees (`K*/src`), K3/K4 = the
  expected `__output__` apple1..4 regular files — `corpus/evidence/round-37/c1/K*/oracle.tsv`.
- Before receipts (frozen with the claim; `sasquatch-v4be` absent from PATH):
  `corpus/evidence/round-38/c1/K*/before.json`.
- After receipts (claim data, produced after the freeze with `sasquatch-v4be` available):
  `corpus/evidence/round-38/c1/K*/after.json`.
- Entry path `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`; Core heading
  `## Round-38 additions to Core`.
- **Target:** `carriers_matched == 4` and every binding true (`met_target`).
- **Counting command:**
  `python3 -I -B tools/round-38/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>`
- Selftest: `python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65 <same>` — 18 cases
  (1 green; red: do-nothing, missing before/after receipt, wrong (LE) handler, after carrying
  the dependency gap, before without the gap, before := after, oracle or carriers changed after
  freeze, Core row outside the round-38 section, row without `squashfs_v4_be` in its first
  cell, row absent, frontier note absent, `S1120` substring, source opened earlier, used-by
  lacking the entry, coverage map lacking the stem). Development inputs are the round-36
  selftest fixture envelopes, never a carrier.
- Harness: `tools/round-38/c1-run.sh after|oracle CARRIER OUTDIR [SCRATCH]` (honours
  `$HYAKU_SCRATCH`, removes its scratch on exit).
- **Kill rule:** a frozen control meeting the target stops C1 before any after-run: CTL-C1-0
  do-nothing at the v2 freeze, CTL-C1-1 three carriers only, CTL-C1-2 wrong chunk handler — all
  exit 1. If the counter at the measured revision does not meet the target, C1 is an honest
  stop; the counter, predicate, carriers and oracle are never changed after the v2 commit.
- Not claimed: AVM-BE, vendor-mangled images, anything about the extracted programs. The
  dependency shape (unblob calls `sasquatch-v4be -be -no-exit-code -f -d`) is part of the
  before/after receipts, not an extra claim.

## R38-C2 — calibration: self-assessment surfaces vs observed repo state

**Predicate P38-C2.** At the measured revision, the lane's current self-assessment surfaces —
the SCORECARD `## Owned axes` rows, the SCORECARD `## Capabilities` table rows, the SHONEN.md
boxes, and the PROVINCE.md `## Core` and `## Frontier` rows — carry zero mismatches with
observed repo state: every backticked lane-repo pointer in them resolves at that revision (path
exists, line range inside the file), the four stated counts equal the counts the lane's command
A / command B observe at that revision, and the three stated section ranges equal the observed
heading-to-last-non-blank-line ranges; with no unit removed, no fewer pointers than at the
base, and every pointer unresolved at the base repaired by a resolving pointer to the same
document.

- Before (base `77091b49`): **1 mismatch** — `evidence/doctor/` in the PROVINCE Core `REA MCP
  server` row does not resolve; the intended document is the committed
  `.ufo/waves/round-19/evidence/doctor/` tree (doctor-6.5.0.txt, doctor-6.7.0.txt).
- **Target:** `mismatches == 0` and `guards_ok` (`met_target`).
- **Counting command:**
  `python3 -I -B tools/round-38/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 --json-out <RECEIPT>`
- Selftest: `python3 -I -B tools/round-38/c2-counter.py --selftest` — 14 cases (1 green; red:
  do-nothing, junk count, deleted count, deleted pointer, substitution by another document,
  unresolved province pointer kept, box removed, craft range off by one, Adjacent range wrong,
  range beyond file, new unresolved pointer, wrong calibration count, wrong SHONEN count).
  Wave-1 disclosure (R38ExecSelftests): several red cases fail via `guards_ok` rather than the
  named clause, and three cases use paths the LANE allowlist rejects — disclosed, not repaired
  in frozen bytes.
- **Kill rule:** a frozen control meeting the target stops C2 before data: CTL-C2-0
  do-nothing at the base, CTL-C2-1 junk counts, CTL-C2-2 delete the bad pointer, CTL-C2-3
  substitute other resolving documents — all exit 1. A miss at the measured revision is an
  honest stop; no counter change after this commit.
- Separability: C2 reads SCORECARD/SHONEN/PROVINCE/SKILL/README/knowledge/result.json only,
  and never touches C1's receipts or carriers. C1 reads none of SCORECARD/SHONEN.

## Frontier step (§2b), assimilation, routed defects

- Census start captured before any registry edit: `.ufo/waves/round-38/census-start.txt` (exit
  0, 9 W04). End census is pasted in the report.
- Sourced claim: C1's entry cites rows opened 2026-10-26 (unblob `squashfs.py` handler source,
  unblob test-fixture provenance, Freetz AVM-BE note — candidates; admit/reject decided through
  the lesson Gate).
- Assimilation theme: `merge/kaidoku/` sasquatch/unblob/AVM entries — per-entry gate with ≥1
  admit and ≥1 reject; id-collision check and quarantine slice hand-check per addendum §10
  before any append; scratch-mirror census exit 0 before the first registry append.
- Routed defects: R37-CL1 (commit every receipt the report cites; cite only what is committed),
  R37-CL2 (register `avm.txt` and `be-squashfs_v4{,.nopad}.bin` provenance through the
  SOURCES gate), R37-CL3 (file `## Gate` decisions incl. the 7-Zip rejection), R36-CL1
  (commit the `w2.ready.dispatched` stamp), R36-CL2 (dated pointer names the entry stem),
  R36-CL4 (instrument map shipped in this freeze), R36-CL6 (receipt identity = subject digest,
  not local_path) are landed as fixes; R36-CL3/R36-CL5 blind spots are disclosed against the
  successor counters and left for the wave to falsify.
- `considerthese/` is absent in this lane (one report line).
