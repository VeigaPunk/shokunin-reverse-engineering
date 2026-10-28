# kaidoku round 44 — claims (freeze-review corrected; the FREEZE commit pins these bytes)

Base `c29360e3ba5381a5ab69e372d0d9577970f85018` (lane `main` at round start; the round-43
verifier spot-check `corpus/lessons/round-43-verifier-spotcheck.md` is an ancestor).
L1 `KaidokuR44` holds the §3 planner seat (orchestrator ruling 2026-10-19: the wave validator
rejects `planner` as a swarm role; bounded planning data-walks ride scouts/connectors/revengers —
recorded here per the round contract). Fresh-start posture (run-10 directive + the cycle-2
addendum): the last three round closures (rounds 41, 42, 43 verifier spot-checks under
`corpus/lessons/`) were read before declaring; every claim carries a do-nothing control scored
before any claim data (§9).

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis
is a lowest axis. R44-C1 works coverage; R44-C2 works calibration. They are causally separable:
C1 moves SquashFS v1/v2 extraction (REA receipts, PROVINCE rows, README map, S138/S139);
C2 counts self-assessment mismatches between the lane's own statements and committed repo state
(SCORECARD capability rows, SHONEN pointers, `planned` rows) and repairs a frozen rubric of them.

## Wave-1 amendment record (folded into this text before the freeze)

This file was rewritten after wave-1 review landed. Changes folded in (each is named again in
`## Changes from the draft` at the foot):

1. The initial frozen carrier target is the four v1.0/v2.0 fixtures listed below. The v2.1
   LE/BE `__input__` and `__output__` artifacts were fetched during wave-1 exploration, and
   an unretained REA scratch probe was run after the draft; they are explicitly EXCLUDED from
   R44-C1, are not scored, and provide no claim evidence. They remain unbound exploratory
   assets only. No carrier expansion after observed data.
2. Freeze-walk port source: `tools/round-43/c1-counter.py` (merge-aware `git log -m
   --diff-merges=first-parent`, status filter, tree blob backstop) — NOT round-42's walk, which
   misses merge-commit edits (R44ConnPattern probe, control scored red on the round-42 walk).
3. D1 (R44RevFreeze): the four round-42-carrier bytes already have committed REA envelopes
   (round-42 `c2/heldout` H41/H43/H44/H45; round-43 `c1/heldout` H41 = v2-le). A `cp` of a
   pre-freeze envelope would satisfy the naive "descendant of the freeze" clause → new control
   CTL-C1-4 + provenance binding (the receipt's `parameters.output_directory` must name a
   `corpus/evidence/round-44/c1/` path and the evidence id must be minted over that path; the
   counter rejects any after-receipt byte-identical to a pre-freeze committed envelope).
4. R44EntryDraft + FixtureAudit N1 + R44SrcOracle F1/F2: `file(1)` mislabels both BE carriers
   "uncompressed" while `unsquashfs -s` reports inodes/data/fragments compressed on all four
   target carriers. Root cause (measured by R44SrcOracle, controlled flip): `file`'s
   "compressed/uncompressed" token is byte-20's value, which is the low byte of
   `inode_table_start` in the legacy v1/v2 packed superblock — there is NO `compression` field
   in v1/v2 (zlib/gzip is the only compressor; `flags` @36 SQUASHFS_NOD clear ⇒ compressed).
   The counter binds `compression_family == 'zlib(gzip)'` from the inode-table metadata block
   (metadata header high bit selects raw vs compressed; compressed body begins `78xx`) and
   frozen oracle evidence, never from `file` text. `superblock_layout` is v1/v2 (bytes_used
   u32@8, s_major@28, s_minor@30, flags@36 — unblob `squashfs.py:124-140`, squashfs-tools
   `squashfs_compat.h:38-64`), NOT the v4 layout the draft first wrote. `unsquashfs --version`
   exits 1 (parse its version output, not its code).
5. The four target carriers have ZERO non-regular members (no symlink, device, subdirectory —
   census frozen in carriers.json): the gap rule for R44-C1 is `gaps == []` and
   `unpublished_entries == []`; ANY gap or diagnostic is a failed carrier, not a tolerated one.
6. Sentinel B1–B5 C2 redesign (below): pin_rev, asserted ⊂ BASE line, frozen check scripts,
   notes-never-evidence, expected_append exact-bytes, directory-freeze prefix, line_sha256 for
   cited lines, per-entry fitness gate.
7. R44RevFreeze missing-inputs: `tools/round-27/xpin-attribute.mjs` (vendored into
   tools/round-44/), `rea-pkg.json`, `prior-pins.json` re-minted through round 43,
   `toolchain.{sasquatch,unblob,unsquashfs}` digests in carriers.json, controls + dev inputs
   under `.ufo/waves/round-44/controls/**`, heldout envelope sets enumerated, v3 C1 receipts
   under `corpus/evidence/round-42/c1/**` (CTL-C1-1 inputs).
8. Frozen-file model corrected (R44RevFreeze B1–B4): SCORECARD.md, SHONEN.md,
   corpus/README.md, PROVINCE.md, LOG.md, corpus/knowledge/* are NOT byte-frozen; they are
   BASE-pinned in the C2 rubric (each entry reads `git show <BASE>:<file>`) and C1's edits are
   append-only (PROVINCE: append after the last line only + prefix-preserved binding).
   SOURCES.md IS byte-frozen, with S138 + S139 landed in the freeze commit naming the final
   entry stem in `used-by` (round-43 pattern).
9. Entry stem fixed: `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` (wildcard removed).
10. Probe-404 receipt committed at `.ufo/waves/round-44/l1/probe-fixture-404.txt` (debt D-27;
    M44-1's red arm now has committed evidence).
11. **Instrument hazard (R44EntryDraft `cmpprobe`, 2026-10-28):** `/usr/bin/cmp -l` exits **0** for
    differing inputs of 4096 bytes or more on this host (diffutils 3.12-2, `pacman -Qkk diffutils`
    clean); plain `cmp`/`cmp -s` exit 1 correctly. All four target carriers are exactly 4096 B — the
    boundary case. Counters, controls and the C2 rubric MUST compare bytes via `cmp -s`, `cmp`,
    or sha256 digests — never `cmp -l`. (Receipt: `.ufo/waves/round-44/w1/artifacts/R44EntryDraft/receipt.json`.)

## Freeze-integrity rule (both claims)

A score at `REV` is admissible only if `FREEZE` is an ancestor of `REV`, no commit in
`FREEZE..REV` touches a frozen path of that claim, and each frozen regular-file blob at FREEZE
equals the blob at REV; a later restore does not un-block (exit 2 `frozen_path_changed`, never
`met_target`). The path walk is the round-43 implementation: merge diffs
(`git log -m --diff-merges=first-parent --name-status`), M/D/R/T/U are changes, A is a change
whenever the path existed at FREEZE, plus a tree-level blob backstop comparing every frozen
blob at FREEZE vs REV. `tools/round-44/` is frozen as a DIRECTORY pathspec — a file added under
it after the freeze is a change. Control tables and their development inputs are committed in
the freeze. Every score receipt records the scorer's exit code, `counter_sha256` (sha256 of the
counter file's own bytes) and `counter_sha256_at_freeze` (round-41 closure D4), plus sha256 of
every post-freeze control receipt it cites. Both counters are dry-run end to end, as frozen,
with dev-arm inputs before the freeze, and the dry-run receipts show every binding evaluated
(QUALITY 84).

## R44-C1 — coverage: SquashFS v1 and v2 through REA `extract-firmware` → Core

Surface moved: `PROVINCE.md:416` (the round-42 frontier note) names `SquashFS v1/v2`
(`squashfs_v1`, `squashfs_v2`) as still-Frontier. The claim moves these two handler families
to Core on the four frozen standard fixtures (v1.0 and v2.0, both byte orders), not on every
version/carrier. A `## Round-44 additions to Core` row (appended after the last line of
PROVINCE.md only), knowledge entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`,
a `corpus/README.md` coverage-map row, and SOURCES S138 (unblob 26.6.4 `__output__` trees) +
S139 (squashfs-tools release page) document the result. S138/S139 land in the freeze commit
with `used-by` naming the entry. "Frontier" means no mapped Core row — REA envelopes for these
four bytes already exist in earlier heldout rounds; what does not exist is a promotion binding
+ oracle comparison. Command showing no promotion at freeze: counter exits 1 with
`carriers_matched 0`.

**Frozen carriers** (ids in `tools/round-44/carriers.json`; all four are committed MIT unblob
26.6.4 fixtures under `corpus/evidence/round-42/c2/fixtures/`, held-out inputs, never prior C1
carriers):

| id | file | handler | endian | s_ver | oracle |
|---|---|---|---|---|---|
| v1le | `corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin` | `squashfs_v1` | le | 1.0 | `unsquashfs` -lls census + `__output__` digests |
| v1be | `.../v1-be--squashfs_v1.0_be.bin` | `squashfs_v1` | be | 1.0 | same |
| v2le | `.../v2-le--squashfs_v2.0_le.bin` | `squashfs_v2` | le | 2.0 | same |
| v2be | `.../v2-be--squashfs_v2.0_be.bin` | `squashfs_v2` | be | 2.0 | same |

`v2ns-*` (`squashfs_v2_nonstandard`) stays Frontier: no independent reader exists (`unsquashfs`
4.7.5 FATALs, `7z` 26.04 refuses, backhand has no v2ns profile — all measured this round), and a
same-tool oracle is not an oracle. R44LabV2ns re-verifies.

**Predicate P44-C1** (`tools/round-44/c1-counter.py`; a port of `tools/round-42/c1-counter.py`
with the freeze walk taken from `tools/round-43/c1-counter.py`, the v3 superblock probe replaced
by a v1/v2 probe, the v3 LZMA oracle path replaced by the unsquashfs census + `__output__`
digest binding, and the handler binding frozen per-carrier to `squashfs_v1`/`squashfs_v2`).
At the measured revision, for each frozen carrier, the committed round-44 REA 6.5.0
`extract-firmware` after-receipt (unblob 26.6.4, sasquatch 4.5.1 on the child PATH) — first
added in a commit that descends from the freeze — names the carrier's frozen
`squashfs_v1`/`squashfs_v2` handler with no failed chunk, publishes every regular file of the
frozen independent oracle at its exact relative path under the chunk extract root
(segment-bounded, round-41 closure D5) with the same sha256 and size, carries
`gaps == []` and `unpublished_entries == []` (zero non-regular members on these carriers —
any gap or diagnostic is a failed carrier), has a subject digest equal to the carrier pin and
recomputes its evidence id; the carrier bytes hash to the pin and their superblock reads the
frozen magic/s_major/s_minor/endianness values in carriers.json (the v1/v2 layout — there is
no `compression` field; `compression_family == zlib(gzip)` is bound to the frozen expectation
plus `flags`-NOD-clear, never to `file` text); **and** a counter-time REA rerun of the same
bytes has the same semantic projection as the committed receipt (a receipt fabricated from the
oracle cannot equal a real run); the receipt's `parameters.output_directory` names a
`corpus/evidence/round-44/c1/` path and its evidence id is minted over that provenance, and the
receipt bytes are not identical to any pre-freeze committed envelope (D1 relabel refusal);
`PROVINCE.md` holds the `## Round-44 additions to Core` row appended after the last line naming
`squashfs_v1` + `squashfs_v2` and citing the entry, with PROVINCE bytes `1..<last_line_at_base>`
unchanged at REV (prefix-preserved, so SHONEN's `PROVINCE.md` line pointers do not drift); a
round-44 frontier note supersedes the `SquashFS v1/v2` Frontier text only; `corpus/README.md`
maps the entry stem; SOURCES S138 + S139 rows cite the entry in `used-by`; no frozen C1 path
changed after the freeze.

- Independent-reader check: `unsquashfs` 4.7.5 (`/usr/bin/unsquashfs`, squashfs-tools,
  sha256 frozen in `carriers.json.toolchain.unsquashfs`) and 7-Zip 26.04 (`/usr/bin/7z`,
  sha256 frozen in toolchain) both list/extract the four target carriers; member digests agree
  across the v1/v2.0 fixture pairs. They are distinct implementations but share some
  squashfs-tools lineage risk; do not describe either as proof of complete producer independence.
  Unblob `__output__` trees (S138) are pinned regression expectations, not an independent oracle.
  Carrier identity binds exact image sha256/superblock fields; the v2.1 output trees remain
  unbound exploratory dataset assets.
- Target: `carriers_matched == 4`, every binding true, `frozen_path_changed []`,
  `met_target true`, exit 0.
- Counting command: `python3 -I -B tools/round-44/c1-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --json-out <OUT>`
- Data procedure (after the freeze, never before): the L1 runs `tools/round-44/c1-run.sh`
  (REA 6.5.0 `extract-firmware --format json --full-output` on each frozen carrier into fresh
  outdirs under `corpus/evidence/round-44/c1/`, plus `run.json` receipts); seats never run it.
- Controls scored at the freeze (before data):
  - CTL-C1-0 do-nothing: counter at the freeze exits 1, `carriers_matched 0`, every doc binding
    false;
  - CTL-C1-1 round-42 C1 (v3) after-receipts copied to `.ufo/waves/round-44/controls/c1-1/` and
    scored → non-zero (subject.digest/handler/superblock fail: v3 receipts cannot pass a v1/v2
    predicate);
  - CTL-C1-2 fabricated "oracle-only" envelope (published-file claims computed from
    carriers.json oracle, no real REA run) → non-zero on the counter-time rerun-projection
    binding;
  - CTL-C1-3 sasquatch-absent: receipt captured pre-freeze with sasquatch stripped from the
    child PATH → non-zero with `missing-extractor-dependency`, not a clean match;
  - CTL-C1-4 relabelled-envelope (D1): committed pre-freeze envelopes of the same bytes
    (round-42 c2/heldout H41/H43/H44/H45, round-43 c1/heldout H41) copied into
    `.ufo/waves/round-44/controls/c1-4/` under round-44 receipt names and scored → non-zero
    (the counter refuses bytes/projection identical to a pre-freeze committed envelope and any
    `output_directory` not under `corpus/evidence/round-44/c1/`);
  - CTL-C1-5 mutated-superbytes (debt D-11): each carrier's superbytes mutated (bad magic,
    swapped s_major, compression outside the frozen set) → superblock probe reds each mutation;
- Kill rule: any counterfactual control reaching `carriers_matched == 4` with every binding
  true stops C1 before data.
- Disclosed limits: four 4 KiB fixtures with 3–4 ≤7-byte regular files each is a thin carrier
  set — the claim promotes the *handler family through REA on the frozen carriers*, not every
  v1/v2 image (debt D-01); all four target carriers are zlib-compressed but no carrier exercises
  a multi-block member, fragment, symlink, device or subdirectory (D-07, D-08 — members are
  6–7-byte single-block files); no published v1/v2 rootfs image was fetchable this round
  (OpenWrt White Russian 404, DD-WRT beta listing empty — D-02); v2.1 outputs and scratch probe
  are unbound exploratory data, not claim evidence; `squashfs_v2_nonstandard`,
  `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, `squashfs_v4_broadcom`, gzip v3, LE AVM
  (`hsqs`), AVM kernels and nested sub-images below depth 1 stay Frontier; the counter-time rerun
  proves projection equality, not which process wrote the committed receipt (R40-CL2, D-13);
  using the round-42 held-out inputs removes them from any future held-out set (D-14).

## R44-C2 — calibration: a frozen rubric of self-assessment statements counts and repairs mismatches

Surface moved: calibration of three concrete current self-assessment assertions in
the `## Owned axes` cells of `SCORECARD.md`: coverage count (133/133 vs the freeze-tree
count 137/137), depth count (20/20 vs 21/21), and craft range (`SKILL.md:81-449` vs the
freeze-tree craft range `81-543`). These are the three mismatches the frozen rubric binds;
the pinned historical claims (133/133 and 20/20 at `e1c83313`) remain true at their pins
and are NOT rewritten. Wave-1 census found 16 candidate mismatches across several classes;
all other candidates are explicitly dispositioned by id as excluded (historical/pinned
semantics, uncertain grammar, or outside this claim). This is a narrow calibration claim,
not a claim that all 16 candidates are repaired. If the frozen per-id census finds zero
mismatches among the three named entries at BASE, C2 STOPS.

**Rubric design (sentinel-corrected; every clause mandatory):**

- Each entry: `{id, file, line_at_base, line_sha256, pin_rev?, asserted, check:{script,
  script_sha256, args}, observed_at_base, expected:'match', note}`.
- `asserted` must be a byte substring of the BASE blob's `line_at_base` and
  `line_sha256 == sha256(that line)`; else exit 2 `asserted_not_in_base_line` (B2: the rubric
  cannot be authored to match the wrong value or manufacture a base mismatch).
- `pin_rev` is extracted from the same base line (`at \`<hex>\``); a pinned entry is checked
  ONLY at its pin (the historical pin is immutable); a REV-state entry only when the line
  carries no rev qualifier. `evaluate_at = pin` for historical count/receipt assertions, `rev`
  only for current-state pointers and derived invariants; never compare a pinned historical
  value to the current tree (CritC2 F5).
- The counter re-runs every check at BASE and requires `observed_at_base` to equal the
  check's own output (drift = exit 2, not a mismatch). Census records a per-id
  `verdict_at_base` vector for all enumerated and dropped rows; no mismatching row may
  be dropped without an exact `not-checkable-because` disposition reviewed before freeze.
  At FREEZE^, re-derive each asserted string and require byte equality with the census,
  and CTL-C2-0 compares the per-id vector, not just aggregate counts.
- A note is never evidence: a repaired entry must re-derive its value at REV through its
  own check; an appended `correction:` line is a declaration, and a note value that
  disagrees with the re-derivation is a mismatch (`note_value_disagrees`), not a pass.
- Fitness gate at freeze: every check is shown able to fail on its own entry (mutate the
  asserted value in a scratch tree → expect mismatch). One mutation per entry.
- Cited lines of `SCORECARD.md`, `SHONEN.md` and `SKILL.md` carry `line_sha256`; statements
  are checked at their pinned revision or by row identity, never by bare line number after
  another claim inserts text. `corpus/README.md` is not byte-frozen by C2: its checks
  re-derive current rows at REV and tolerate exactly C1's one new knowledge entry/map row
  (C2 does not repair README). `SOURCES.md` is frozen for C1's S138/S139 freeze-commit rows,
  but no C2 entry checks SOURCES counts or numstat.
- The three C2 target repairs are bound by `expected_edit` exact bytes:
  `blob_at_REV == blob_at_FREEZE + expected_append`; any other file edit is a freeze violation.
- `tools/round-44/` is a directory freeze pathspec only after all round-44 scripts, counters,
  checks, rubric and carriers are present in FREEZE; no later tool is added there.
- Dynamic-count checks (e.g. coverage-map row count, `N/N knowledge files`) are evaluated at
  REV against the re-derived count (tolerating the C1 README row), and a present-but-wrong map
  row reds via a content arm binding each map row to its knowledge stem's `source:` (debt D-24
  mitigation).
- Target: `mismatches == 0` over the frozen rubric at REV, `entries_evaluated >= 1`, every
  check evaluable, `frozen_path_changed []`, exit 0.
- Counting command: `python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --work <SCRATCH> --json-out <OUT>`.
- Controls: CTL-C2-0 do-nothing (counter `--pre-freeze` at BASE: non-zero iff frozen rubric
  shows mismatches > 0 at base; if 0, claim stops); CTL-C2-1 seeded mismatch (scratch clone,
  corrupt the rubric-named seeded entry → non-zero with that entry id); CTL-C2-2 malformed
  rubric (entry with no check script → exit 2); CTL-C2-3 rubric immutability (mid-round rubric
  edit → `frozen_path_changed` on `tools/round-44/c2-rubric.json`); CTL-C2-4 wrong-value note
  (append a correction note carrying a wrong value → `note_value_disagrees`, never a pass —
  sentinel B3 / RevKill K6).
- Landing scope: appended dated corrections and the rubric's `expected_append` blocks only —
  never a rewrite of frozen claim text, never a LOG/SCORECARD history edit (append-only corpus
  discipline; existing `corpus/knowledge/*` blobs must be a byte-prefix of their REV blobs).
- Kill rule: CTL-C2-0 green before data OR any seeded/wrong-note control green stops C2.
- Disclosed limits: the rubric enumerates only frozen statements (D-15); check-pass ≠ truth
  (D-16); appended corrections leave the original wrong line standing for readers unaware of
  the convention (D-17); category-(d) markers must cite a resolving receipt or the row is
  enumerated as a mismatch (D-22); receipt-derived verdicts are not re-executed (D-23).

## Separability

C1 reads `corpus/evidence/round-4*/c1/` receipts, `PROVINCE.md` (append-after-last-line only),
`corpus/README.md` (one coverage-map row), `corpus/SOURCES.md` (S138/S139), the fixed C1
entry stem, and its tools. C2 reads SCORECARD, SHONEN, README, SKILL, and the frozen C2
rubric/check scripts. Shared README/SOURCES landing edits MUST be exactly represented in the
rubric's content-bound expected-edit set (README's inserted map row by exact row identity;
SOURCES' S138/S139 rows by exact append bytes); any additional change to either file reds
`frozen_path_changed`. C2 must be measurable at a REV both with or without C1's landing;
ordering is not an implicit exemption. All C1 tools, C2 counter/rubric, and every rubric check
script must exist in the freeze commit. Since `tools/round-44/` directory-freezing would reject
post-freeze additions, every file under it is pre-landed before freeze and the directory scope
is explicit only if no later tool additions occur. Otherwise use exact frozen paths and do not
declare a directory freeze. Cited historical receipts are pinned by path + digest in the rubric
and read at their committed measured revision, not from mutable worktree bytes.

## Frontier step (inside the claim cap)

- S138: unblob 26.6.4 SquashFS `__output__` expected trees (dataset, tier A; grounds the second
  oracle tree; NOT handler code, NOT extractor behaviour, NOT a C1 carrier). Landed in the
  freeze commit with `used-by` = the C1 entry.
- S139: squashfs-tools upstream release page `https://github.com/plougher/squashfs-tools/releases`
  (docs/tool, tier A; grounds `/usr/bin/unsquashfs` 4.7.5). Same commit.
- Assimilation (§10): `Assimilation: none` — the kaidoku package's full 5-row quarantine slice
  was hand-checked in round 43 and re-derived this wave (R44Quarantine: no staged row adopted
  since); `considerthese/` does not exist.
- Mistake (mined): M44-1 `stale-premise` — the pre-freeze probe fetched
  `squashfs_v2.0_be.expected` by guessing the fixture API shape (HTTP 404, committed receipt
  `.ufo/waves/round-44/l1/probe-fixture-404.txt`) before reading the `__output__/` listing
  (HTTP 200 shows `<name>.bin_extract/` dirs; corroborating receipts in
  `.ufo/waves/round-44/w1/artifacts/R44MistakeHunt/`); captured-by: the frozen-URL convention —
  a URL is pinned only after a successful open, never guessed; fix verified by the red/green
  pair.
- Sourced claim: R44-C1 cites S138/S139 (opened this round); R44-C2's rubric cites
  `corpus/lessons/round-43.md` (in-repo, no S row needed).

## Frozen paths

Byte-frozen (change ⇒ `frozen_path_changed`, exit 2):
`plans/round-44-claims.md`; all round-44 tools and control inputs required by the counters
(`tools/round-44/` directory pathspec, populated before FREEZE); `tools/round-42/fixtures.json`;
`tools/round-42/c1-counter.py` and `tools/round-43/c1-counter.py` (audit-only port sources);
the four C1 carrier bins under `corpus/evidence/round-42/c2/fixtures/`;
the four target oracle trees under `corpus/evidence/round-44/oracle/` (v2.1 trees are unbound);
`.ufo/waves/round-44/controls/**`; the round-42 v3 C1 receipt inputs; round-42/43 heldout
receipts used by CTL-C1-4; `SKILL.md`; `corpus/SOURCES.md` after S138/S139 are added in FREEZE;
all historical score receipts explicitly pinned by path and digest in C2's rubric.

NOT frozen — BASE-pinned in the C2 rubric (entries read `git show <BASE>:<file>`; cited lines
bound by `line_sha256`; append-only at REV):
`SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `corpus/SOURCES.md` *for C2 only* (C1's S-rows
land in the freeze commit; no later SOURCES edit is permitted by either claim),
`PROVINCE.md` (C1 append-after-last-line only + prefix-preserved binding), `LOG.md`,
`corpus/knowledge/*` (new entry only; existing blobs byte-preserved as prefixes at REV),
`corpus/evidence/round-44/c1/**` (first-added after the freeze — the receipts dir),
`corpus/lessons/round-44*.md` (the round's lesson, lands at close).

## Changes from the draft

(as of the wave-1 fold: four preregistered v1.0/v2.0 target carriers; v2.1 artifacts retained
only as unbound exploration after an unretained scratch probe and excluded from C1; freeze-walk
port source round-43 not round-42; CTL-C1-4/CTL-C1-5 added; v1/v2 layout corrected; zero-gap rule
for target carriers; sentinel B1–B5 C2 redesign; S138/S139 pre-landed; entry stem fixed; C2
README excluded from byte-freeze; missing freeze inputs added.)
