# kaidoku round 44 — DRAFT claims (pre-freeze; frozen bytes land when the freeze commit is made)

Base `c29360e3ba5381a5ab69e372d0d9577970f85018` (lane `main` at round start; the round-43
verifier spot-check `corpus/lessons/round-43-verifier-spotcheck.md` is an ancestor).
L1 `KaidokuR44` holds the §3 planner seat (orchestrator ruling 2026-10-19: the wave validator
rejects `planner` as a swarm role; bounded planning data-walks ride scouts/connectors/revengers —
recorded here per the round contract). Fresh-start posture (run-10 directive + the cycle-2
addendum): the last three round closures (rounds 41, 42, 43 verifier spot-checks under
`corpus/lessons/`) were read before declaring; every claim below carries a do-nothing control
scored before any claim data (§9).

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis
is a lowest axis. R44-C1 works coverage; R44-C2 works calibration. They are causally separable:
C1 moves SquashFS v1/v2 extraction (REA receipts, PROVINCE rows, README map, S138/S139);
C2 counts self-assessment mismatches between the lane's own statements and committed repo state
(SCORECARD capability rows, SHONEN pointers, `planned` rows) and repairs a frozen rubric of them.

## Freeze-integrity rule (both claims; carried from rounds 39–43)

A score at `REV` is admissible only if `FREEZE` is an ancestor of `REV`, no commit in
`FREEZE..REV` touches a frozen path of that claim, and each frozen regular-file blob at FREEZE
equals the blob at REV; a later restore does not un-block (exit 2 `frozen_path_changed`, never
`met_target`). The path walk includes merge diffs (`-m --diff-merges=first-parent`); M/D/R/T/U
are changes, and A is a change whenever the path existed at FREEZE. Control tables and their
development inputs are committed in the freeze. Every score receipt records the scorer's exit
code, `counter_sha256` (the sha256 of the counter file it ran) and `counter_sha256_at_freeze`
(round-41 closure D4), plus sha256 of every post-freeze control receipt it cites. Both counters
are dry-run end to end, as frozen, with dev-arm inputs before the freeze, and the dry-run
receipts show every binding evaluated (QUALITY 84).

## R44-C1 — coverage: SquashFS v1 and v2 through REA `extract-firmware` → Core

Surface moved: `PROVINCE.md` names `SquashFS v1/v2` as still-Frontier (`## Round-42 additions
to Core` frontier note and the round-42 frontier bullet). The claim moves
`squashfs_v1` + `squashfs_v2` (both byte orders) Frontier → Core: a new
`## Round-44 additions to Core` row, a knowledge entry, a `corpus/README.md` coverage-map row,
and SOURCES rows S138 (the `__output__` expected trees, opened this round) and S139
(squashfs-tools release page, the oracle identity), each opened this round. Command that shows
it unmoved: the round-44 C1 counter at the freeze exits 1 with `carriers_matched 0` (receipts
absent, documentation bindings false) and no commit in `FREEZE..REV` may substitute a v3/v4
receipt for a v1/v2 one.

**Frozen carriers** (ids frozen in `tools/round-44/carriers.json`, bytes already committed under
`corpus/evidence/round-42/c2/fixtures/` — MIT unblob 26.6.4 fixtures, `tools/round-42/fixtures.json`
pins; they were round-42 C2 held-out *inputs*, never a C1 carrier):

| id | file | handler | endian | oracle |
|---|---|---|---|---|
| V1LE | `corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin` | `squashfs_v1` | le | `unsquashfs` 4.7.5 `-lls` + `__output__` member digests |
| V1BE | `.../v1-be--squashfs_v1.0_be.bin` | `squashfs_v1` | be | same |
| V2LE | `.../v2-le--squashfs_v2.0_le.bin` | `squashfs_v2` | le | same |
| V2BE | `.../v2-be--squashfs_v2.0_be.bin` | `squashfs_v2` | be | same |

`v2ns-*` (`squashfs_v2_nonstandard`) stays Frontier: no independent reader was found
(`unsquashfs` 4.7.5 and `7z` 26.04 both refuse it; backhand has no v2ns profile), and a
same-tool oracle is not an oracle. `squashfs_v1`/`v2` superblock probe (magic, s_major,
endianness, compression) is implemented in the counter, verified against `file` output.

**Predicate P44-C1** (implemented by `tools/round-44/c1-counter.py`, a port of
`tools/round-42/c1-counter.py` with the v3 superblock probe replaced by the v1/v2 probe, the
v3 LZMA oracle path replaced by the `unsquashfs` member census, and the handler family binding
frozen per carrier to `squashfs_v1`/`squashfs_v2`). At the measured revision, for each frozen
carrier, the committed round-44 REA 6.5.0 `extract-firmware` after-receipt (unblob 26.6.4,
sasquatch 4.5.1 on the child PATH) — first added in a commit that descends from the freeze —
names the carrier's frozen `squashfs_v1`/`squashfs_v2` handler with no failed chunk, publishes
every regular file of the frozen independent oracle at its exact relative path under the chunk
extract root (segment-bounded, round-41 closure D5) with the same sha256 and size, accounts for
every non-regular oracle row by the frozen gap rule (one `unpublished-entry` gap or one
`MaliciousSymlinkRemoved` diagnostic per symlink; at most one structural `depth-limited`; no
`unknown-chunk-handler`), has a subject digest equal to the carrier pin and recomputes its
evidence id; the carrier bytes hash to the pin and their superblock reads the frozen
magic/major/minor/endianness/compression; **and** a counter-time REA rerun of the same bytes has
the same semantic projection as the committed receipt (a fabricated receipt cannot equal a real
run); `PROVINCE.md` holds the `## Round-44 additions to Core` row naming `squashfs_v1` and
`squashfs_v2` and citing the entry; a round-44 frontier note supersedes the `SquashFS v1/v2`
Frontier text only; `corpus/README.md` maps the entry stem; SOURCES S138 (the unblob
`__output__` expected trees dataset URL, opened this round) and S139 (squashfs-tools upstream
release/download page identifying `/usr/bin/unsquashfs`, opened this round) exist with the
entry's `source:` citing them and `used-by` naming the entry; no frozen C1 path changed after
the freeze.

- The independent oracle is `unsquashfs` 4.7.5 (`/usr/bin/unsquashfs`, squashfs-tools): a
  different producer than sasquatch (squashfs-tools 4.3 patchset). Its `-lls` member list and
  the extracted member digests are frozen per carrier in `carriers.json`; the unblob `__output__`
  expected tree (S138) is a second, cross-checking oracle. `v2be` is uncompressed (measured
  2026-10-28: `file` reports "version 2.0, uncompressed"); that is an oracle property, not a
  counter assumption.
- Target: `carriers_matched == 4` (ids frozen in `carriers.json`), every binding true,
  `frozen_path_changed []`, `met_target true`, exit 0.
- Counting command: `python3 -I -B tools/round-44/c1-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --json-out <OUT>`
- Data procedure (after the freeze, never before): the L1 runs `tools/round-44/c1-run.sh`
  (REA 6.5.0 `extract-firmware --format json --full-output` on each frozen carrier into fresh
  outdirs under `corpus/evidence/round-44/c1/`, plus `run.json` receipts), seats never run it.
- Controls scored at the freeze (before data):
  - CTL-C1-0 do-nothing: the counter at the freeze exits 1, `carriers_matched 0`, every
    documentation binding false (a do-nothing round cannot reach the target);
  - CTL-C1-1 round-42 C1 receipts copied to the round-44 evidence paths: counter exits
    non-zero (`subject.digest` / superblock / handler bindings fail — v3 receipts cannot pass
    a v1/v2 predicate);
  - CTL-C1-2 a fabricated "oracle-only" receipt (synthesized envelope whose published-file
    claims are computed from the oracle without a real REA run): counter exits non-zero on the
    rerun-projection binding (R40-CL2/R43-CL-witness class — the counter-time REA rerun must
    produce the same projection, which a fabricated envelope cannot);
  - CTL-C1-3 the sasquatch-absent control: a receipt captured with `sasquatch` stripped from
    the child PATH is scored by the frozen counter and exits non-zero with a
    `missing-extractor-dependency` gap, not a clean carrier match.
- Kill rule: any counterfactual control (CTL-C1-0/1/2/3) reaching `carriers_matched == 4` with
  every binding true stops C1 before data.
- Disclosed limits: four 4 KiB fixtures with 3–4 regular files each is a thin carrier set —
  the claim promotes the *handler family through REA on the frozen carriers*, not every v1/v2
  image; published v1/v2 rootfs images (e.g. OpenWrt White Russian, Linksys v4.x) were probed
  and were not fetchable (404 at `archive.openwrt.org/whiterussian/rc6/openwrt-brcm-2.4-squashfs.trx`,
  DD-WRT beta listing empty), so this claim uses the MIT fixtures only; a later round may add a
  published carrier. `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`,
  `squashfs_v3_nonstandard`, `squashfs_v4_broadcom`, gzip v3, LE AVM (`hsqs`), AVM kernels and
  nested sub-images below depth 1 stay Frontier.

## R44-C2 — calibration: a frozen rubric of self-assessment statements counts and repairs mismatches

Surface moved: the lane's self-assessment surface — `SCORECARD.md` (`## Capabilities` rows and
their `Evidence pointer` cells, the `## Owned axes` headline values and their revision pins),
`SHONEN.md` (its `path:line` and count assertions), `corpus/README.md` (coverage-map row count
vs `corpus/knowledge/` file count), and the `planned` rows of each `## Round <N>` section vs
what the next round actually worked. A calibration claim counts mismatches between the lane's
self-assessment and observed repo state (prompt §9); it is not a coverage assertion. Command
that shows it unmoved: at the freeze the frozen `tools/round-44/c2-counter.py --rev <BASE>`
exits non-zero with the frozen rubric's mismatch count equal to the frozen value (the counter
reads rubric.json; a no-op round repairs nothing).

**Rubric (to be enumerated and frozen).** Wave-1 seats R44ScoutCalib and R44C2Rubric enumerate
every checkable self-assessment statement in scope, each with its check command and its
observed-vs-asserted verdict at the base; the L1 freezes the list into
`tools/round-44/c2-rubric.json` before the freeze. Categories already probed (pre-freeze
evidence): (a) evidence-pointer existence — every `## Capabilities` row's file/command pointer
resolves at REV; (b) headline numbers — the `## Owned axes` row's pinned counts reproduce under
its own `command A` at REV; (c) SHONEN `path:line`/`N of M` assertions resolve at their pinned
revision qualifier, and the bare pointers still resolve at REV or are marked superseded;
(d) `## Round <N>` `planned (round <N+1>)` rows match what round N+1 actually worked or carry an
explicit `(after a steer)`/`superseded` marker; (e) the SCORECARD `## Round <N>` claim table's
`met`/`not met` verdicts agree with the cited receipt's exit code and headline fields;
(f) `corpus/README.md` coverage-map row count equals the `corpus/knowledge/*.md` count with
`missing []`/`dangling []` under command A.

- The counter reads the rubric and re-runs every check at REV in a scratch clone of the repo
  (read-only `git show`/`git ls-tree`; no network, no REA); it reports `mismatches` and exits
  0 iff the frozen rubric shows `mismatches == 0` at REV and no rubric check is unevaluable.
  A rubric entry the landing cannot satisfy is refused at freeze time, not loosened later.
- Red-before controls (each shown able to fail at the freeze):
  - CTL-C2-0 do-nothing: counter at the freeze scores the base and exits non-zero iff
    mismatches > 0 (if the frozen rubric finds 0 mismatches at base, this claim stops —
    a do-nothing control reaching the target proves the predicate wrong);
  - CTL-C2-1 a seeded mismatch: in a scratch clone one rubric statement is edited wrong
    (e.g. an evidence path deleted or a count decremented); the counter must report the
    mismatch and exit non-zero;
  - CTL-C2-2 rubric self-check: the counter exits 2 on a malformed rubric (missing check or
    absent check command);
  - CTL-C2-3 a check that repairs by broadening the rubric mid-round is impossible: the rubric
    is itself a frozen path (hash bound); any edit re-reds via `frozen_path_changed`.
- Target: `mismatches == 0` over the frozen rubric at the measured revision, every check
  evaluable, `frozen_path_changed []`, exit 0.
- Counting command: `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --work <SCRATCH> --json-out <OUT>`.
- Landing scope: text-only repairs of the rubric's flagged statements (pointer corrections,
  supersession notes, count fixes) plus the rubric itself; never a rewrite of frozen claims
  text, never a LOG/SCORECARD history edit (append-only corrections only, as new lines).
- Kill rule: CTL-C2-0 green before data (0 mismatches at base) OR any seeded-mismatch control
  green stops C2.
- Disclosed limits: the rubric enumerates only the statements it froze; a mismatch outside the
  frozen set is a new-found defect for the lesson, not counter ground. Counter reads committed
  bytes; it cannot verify that a repaired statement is *true*, only that the check passes —
  every rubric check re-derives the asserted value independently (e.g. it recounts map rows,
  re-resolves the pointer), so a "repair" that rewrites the number without fixing reality fails.
  This claim is deliberately frozen against enumerated checks; if the wave-1 census finds zero
  mismatches the claim stops and the round reports that honestly.

## Separability

C1 reads `corpus/evidence/round-4*/c1/` receipts, `PROVINCE.md`, `corpus/README.md` map,
`corpus/SOURCES.md` (S138/S139), `corpus/knowledge/2026-10-28-r44-*`, `tools/round-44/c1-*`.
C2 reads `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `tools/round-44/c2-*` and the rubric.
They share only `corpus/README.md` (map row added by C1; row count check in C2's rubric is
written to tolerate the C1 landing by reading the count at REV, not a frozen integer) and
`corpus/SOURCES.md` (C1 appends; C2's rubric does not pin SOURCES row count). The plan file is
shared but each predicate names its own frozen-path set.

## Frontier step (this round, inside the claim cap)

- S138: unblob 26.6.4 SquashFS `__output__` expected trees (dataset; opened by wave-1 seat —
  located quote recorded in the lesson `## Gate`). Cited by the C1 entry as the second oracle.
- S139: squashfs-tools upstream release page `https://github.com/plougher/squashfs-tools/releases`
  (docs/tool; opened this round; grounds `/usr/bin/unsquashfs` 4.7.5 identity).
- Assimilation (§10): `Assimilation: none` this round — the kaidoku package's full 5-row
  quarantine slice was hand-checked in round 43 (`.ufo/waves/round-43/w1/R43Quarantine.md`) and
  no staged row has since been adopted; a fresh hand-check of the slice is re-derived in wave 1
  (R44Quarantine) and the lesson records the verdict table. `considerthese/`: no such directory
  — one report line.
- Mistake to mine (class `stale-premise`): this round's own pre-freeze probe fetched
  `squashfs_v2.0_be.expected` by guessing the fixture API shape (HTTP 404) before reading the
  directory listing — evidence: `.ufo/waves/round-44/l1/probe-fixture-404.txt`; captured-by: the
  frozen-URL convention (a URL is pinned only after a successful open, never guessed);
  fix: verify URL existence via the directory-listing API before pinning (red: 404 receipt;
  green: 200 listing receipt — shown able to fail).
- Sourced claim: R44-C1 cites S138/S139 rows opened this round; R44-C2's rubric cites
  `corpus/lessons/round-43.md` (own-work row S-series not required — the lesson is in-repo).

## Frozen paths (draft; wave-1 seat R44RevFreeze verifies completeness)

This file; `tools/round-44/*` (all round-44 tools, `carriers.json`, `c1-run.sh`,
`c2-rubric.json`); the four carrier files under `corpus/evidence/round-42/c2/fixtures/`
(v1-be/le, v2-be/le `*.bin`); `tools/round-42/fixtures.json`; `tools/round-42/c1-counter.py`
(the port source the L1 installs verbatim-ports from — frozen so the port diff is auditable);
`corpus/evidence/round-42/c2/heldout/` (CTL-C1-1's receipt copies read it); the `__output__`
fixture trees fetched pre-freeze into `corpus/evidence/round-44/oracle/` (committed before the
freeze, content-addressed by S138); `tools/round-39/gen-squashfs.py` (referenced by the C1
control writer if a synthetic arm is needed); `.ufo/waves/round-43/l1/scores/*.json` and the
round-42 receipts the controls replay; `SKILL.md` (C2's rubric cites its instrument-registry
rows; the whole file is byte-frozen so a mid-round instrument row can't silently move);
`SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `corpus/SOURCES.md` (C2's rubric targets —
frozen to pin the statement text the rubric checks; repairs land as NEW lines/notes at REV, the
frozen blobs are compared at the rubric's declared revision, not REWRITTEN — see the C2 landing
rule below).

**C2 landing mechanics (repair without rewriting frozen text).** `SCORECARD.md`, `SHONEN.md`,
`corpus/README.md` are frozen at the base text the rubric checks; the C2 repair lands as
appended dated notes/lines (append-only corpus discipline) so the frozen blobs stay equal at
FREEZE and REV while the rubric's checks read the appended correction. Where the honest repair
is a line edit (e.g. a wrong count), the counter treats `(frozen-text mismatch at BASE)` +
`(appended correction at REV)` as repaired: the rubric's check is re-run against the appended
note and must pass. If an unavoidable edit is needed to fix a statement, the counter's
`frozen_path_changed` arm for that file is relaxed ONLY for the rubric-named paths and the diff
is bound to equal exactly the rubric's expected edit bytes (M43-2 repair: diff expectations are
row-identity checks over the appended block, never raw numstat).

## Changes from the draft
(to be filled by wave-1 amendments before the freeze — none yet)
