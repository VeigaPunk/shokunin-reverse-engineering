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

1. Carriers 4 → 6: `squashfs_v2.1` LE/BE added (unblob 26.6.4 `__input__` fetched 2026-10-28,
   `unsquashfs` oracle + committed `__output__` tree exist; REA extracts them — measured probe
   `.ufo/waves/round-44/l1/`). This closes debt row D-10 (the fetched oracle set already held
   the two v2.1 trees with no carrier bound).
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
   "uncompressed" while `unsquashfs -s` reports inodes/data/fragments compressed on all six.
   Root cause (measured by R44SrcOracle, controlled flip): `file`'s "compressed/uncompressed"
   token is byte-20's value, which is the low byte of `inode_table_start` in the legacy v1/v2
   packed superblock — there is NO `compression` field in v1/v2 (zlib/gzip is the only
   compressor; `flags` @36 SQUASHFS_NOD clear ⇒ compressed). The counter binds
   `compression_family == 'zlib(gzip)'` to the frozen `carriers.json` expectation plus the
   `flags`-NOD-clear condition — never to `file` text. `superblock_layout` in carriers.json is
   the v1/v2 layout (bytes_used u32@8, s_major@28, s_minor@30, flags@36 — unblob
   `squashfs.py:124-140`, squashfs-tools `squashfs_compat.h:38-64`), NOT the v4 layout the
   draft first wrote. `unsquashfs --version` exits 1 (parse the version line, not the code).
5. These six carriers have ZERO non-regular members (no symlink, device, subdirectory — census
   frozen in carriers.json): the gap rule for R44-C1 is `gaps == []` and
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
    clean); plain `cmp`/`cmp -s` exit 1 correctly. All six carriers are exactly 4096 B — the
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
(`squashfs_v1`, `squashfs_v2`) as still-Frontier. The claim moves the `squashfs_v1` and
`squashfs_v2` handler families (versions 1.0, 2.0 and 2.1, both byte orders) Frontier → Core:
a `## Round-44 additions to Core` row (appended after the last line of PROVINCE.md only), a
knowledge entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, a `corpus/README.md`
coverage-map row mapping that stem, and SOURCES rows S138 (unblob 26.6.4 `__output__` expected
trees) + S139 (squashfs-tools upstream release page, grounding `/usr/bin/unsquashfs` 4.7.5),
both landed in the freeze commit with `used-by` naming the entry. "Frontier" here means no
mapped Core row — REA envelopes of these bytes already exist in the tree (round-42 c2/heldout,
round-43 c1/heldout); what does not exist is a promotion binding + oracle comparison. Command
that shows it unmoved: the counter at the freeze exits 1 with `carriers_matched 0`.

**Frozen carriers** (ids frozen in `tools/round-44/carriers.json`; the four v1/v2.0 bytes are
the committed MIT unblob 26.6.4 fixtures under `corpus/evidence/round-42/c2/fixtures/` —
round-42 C2 held-out inputs, never a C1 carrier; the two v2.1 bytes are new, fetched from the
same MIT fixture set 2026-10-28 and committed under `corpus/evidence/round-44/carriers/`):

| id | file | handler | endian | s_ver | oracle |
|---|---|---|---|---|---|
| v1le | `corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin` | `squashfs_v1` | le | 1.0 | `unsquashfs` -lls census + `__output__` digests |
| v1be | `.../v1-be--squashfs_v1.0_be.bin` | `squashfs_v1` | be | 1.0 | same |
| v2le | `.../v2-le--squashfs_v2.0_le.bin` | `squashfs_v2` | le | 2.0 | same |
| v2be | `.../v2-be--squashfs_v2.0_be.bin` | `squashfs_v2` | be | 2.0 | same |
| v21le | `corpus/evidence/round-44/carriers/squashfs_v2.1_le.bin` | `squashfs_v2` | le | 2.1 | same |
| v21be | `corpus/evidence/round-44/carriers/squashfs_v2.1_be.bin` | `squashfs_v2` | be | 2.1 | same |

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

- The independent oracle is `unsquashfs` 4.7.5 (`/usr/bin/unsquashfs`, squashfs-tools, sha256
  `461e1fd9…` frozen in `carriers.json.toolchain.unsquashfs`): a different producer than
  sasquatch (squashfs-tools 4.3 patchset). Its `-lls` member census and extracted member
  sha256s are frozen per carrier in carriers.json by `tools/round-44/c1-oracle.py`; the unblob
  `__output__` expected tree (S138) is a second, cross-checking oracle (same-project; debt row
  D-09 records that producer-independence rests on unsquashfs alone).
- Target: `carriers_matched == 6`, every binding true, `frozen_path_changed []`,
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
- Kill rule: any counterfactual control reaching `carriers_matched == 6` with every binding
  true stops C1 before data.
- Disclosed limits: six 4 KiB fixtures with 3–4 ≤7-byte regular files each is a thin carrier
  set — the claim promotes the *handler family through REA on the frozen carriers*, not every
  v1/v2 image (debt D-01); all six carriers are zlib-compressed but no carrier exercises a
  multi-block member, fragment, symlink, device or subdirectory (D-07, D-08 — members are
  6–7-byte single-block files); no published v1/v2
  rootfs image was fetchable this round (OpenWrt White Russian 404, DD-WRT beta listing empty —
  D-02); `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`,
  `squashfs_v4_broadcom`, gzip v3, LE AVM (`hsqs`), AVM kernels and nested sub-images below
  depth 1 stay Frontier; the counter-time rerun proves projection equality, not which process
  wrote the committed receipt (carried R40-CL2, debt D-13); consuming the round-42 held-out
  inputs removes them from any future held-out set (D-14).

## R44-C2 — calibration: a frozen rubric of self-assessment statements counts and repairs mismatches

Surface moved: the lane's self-assessment surface — `SCORECARD.md` (`## Capabilities` evidence
pointers, `## Owned axes` headline pins, `## Round <N>` claim-table verdicts, `planned` rows),
`SHONEN.md` (`path:line` / `N of M` assertions), `corpus/README.md` (coverage-map row count vs
`corpus/knowledge/*.md`), `SKILL.md` instrument-registry text. Wave-1 census
(R44ScoutCalib/R44C2Shonen/R44C2Readme/R44C2Plan + R44ScoutSkill drift rows) enumerates the
checkable statements; the L1 freezes the rubric before data. If the census finds zero
mismatches at base the claim STOPS (honest stop — a do-nothing control reaching the target
proves the predicate wrong; debt D-19).

**Rubric design (sentinel-corrected; every clause mandatory):**

- Each entry: `{id, file, line_at_base, line_sha256, pin_rev?, asserted, check:{script,
  script_sha256, args}, observed_at_base, expected:'match', note}`.
- `asserted` must be a byte substring of the BASE blob's `line_at_base` and
  `line_sha256 == sha256(that line)`; else exit 2 `asserted_not_in_base_line` (B2: the rubric
  cannot be authored to match the wrong value or manufacture a base mismatch).
- `pin_rev` is extracted from the same base line (`at \`<hex>\``); a pinned entry is checked
  ONLY at its pin (the historical pin is immutable); a REV-state entry only when the line
  carries no rev qualifier (B1: rev-mixing cannot produce false mismatches).
- `check` is never free argv: `{script: tools/round-44/checks/<name>.py, script_sha256, args}`;
  the counter requires blob(REV, script).sha256 == script_sha256 else exit 2
  `check_script_drift`, runs `[python3, -I, -B, script, *args]` with shell=False, cwd = the
  materialised REV tree, minimal env (no HOME/proxy; TMPDIR under --work), rejecting args that
  resolve outside the tree (B4: no trivially-green `echo`, no data-supplied execution).
- The counter re-runs every check at BASE and requires `observed_at_base` to equal the check's
  own output (drift = exit 2, not a mismatch); `observed_at_rev != asserted` at the entry's
  evaluation rev is a mismatch ONLY when re-derived by the frozen check — never from a note.
- A note is never evidence (B3): a repaired entry must re-derive its value at REV through its
  own check; an appended `correction:` line is a declaration, and a note value that disagrees
  with the re-derivation is a mismatch (`note_value_disagrees`), not a pass.
- Fitness gate at freeze: every check is shown able to fail on its own entry (mutate the
  asserted value in a scratch tree → expect mismatch). One mutation per entry.
- Cited lines of `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `corpus/SOURCES.md` carry
  `line_sha256`: every cited line must be byte-identical at REV, `blob_at_REV` must start with
  `blob_at_FREEZE` (zero deletions), and every added line begins after the FREEZE blob's final
  byte (B5: append-only, no suffix/containment/numstat arm). A repair whose bytes are known
  pre-freeze is bound as `expected_append` exact bytes + `expected_append_sha256`:
  `blob_at_REV == blob_at_FREEZE + expected_append` byte-for-byte.
- `tools/round-44/` is a directory freeze pathspec; a post-freeze-added check script or rubric
  sibling is `frozen_path_changed`.
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
`corpus/README.md` (one map row), `corpus/SOURCES.md` (S138/S139 in the freeze commit),
`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, `tools/round-44/c1-*`. C2 reads
`SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `SKILL.md`, `tools/round-44/c2-*` and the
rubric. Shared files: `corpus/README.md` (C2's count check reads the count at REV, tolerating
the C1 row; C2's cited-line bindings avoid the lines C1 edits) and `corpus/SOURCES.md` (C1's
S138/S139 land in the freeze commit, before any C2 score). Each predicate names its own
frozen-path set; the shared plan file's bytes are frozen at the freeze.

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
`plans/round-44-claims.md`; `tools/round-44/` (DIRECTORY pathspec — counters, checks/,
`carriers.json` with `toolchain.{sasquatch,unblob,unsquashfs}` digests + frozen superblock
values, `gap-rule.json`, `prior-pins.json` re-minted through round 43, `rea-pkg.json`,
`c1-run.sh`, `c1-oracle.py`, ported `c1-extra.py`, `c2-counter.py`, `c2-rubric.json`,
`xpin-attribute.mjs` vendored); `tools/round-27/xpin-attribute.mjs` (audit-only if vendored);
`tools/round-42/fixtures.json`; `tools/round-42/c1-counter.py` (audit-only port source);
`tools/round-43/c1-counter.py` (audit-only freeze-walk source);
the six carrier `*.bin` files (four under `corpus/evidence/round-42/c2/fixtures/`, two under
`corpus/evidence/round-44/carriers/`); `corpus/evidence/round-44/oracle/**`;
`.ufo/waves/round-44/controls/**` (all control tables, dev inputs, dry-run receipts, the
sasquatch-stripped receipt for CTL-C1-3);
`corpus/evidence/round-42/c1/**` (CTL-C1-1 v3 receipt inputs);
`corpus/evidence/round-42/c2/heldout/{manifest.json,H41,H43,H44,H45}` and
`corpus/evidence/round-43/c1/heldout/{manifest.json,H41}` (CTL-C1-4 relabel inputs);
`tools/round-39/gen-squashfs.py` (only if CTL-C1-2's fabricator calls it);
`SKILL.md` (whole); `corpus/SOURCES.md` (whole, AFTER S138/S139 land in the freeze commit);
the score receipts enumerated by path+sha256 in the rubric's `inputs[]`.

NOT frozen — BASE-pinned in the C2 rubric (entries read `git show <BASE>:<file>`; cited lines
bound by `line_sha256`; append-only at REV):
`SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `corpus/SOURCES.md` *for C2 only* (C1's S-rows
land in the freeze commit; no later SOURCES edit is permitted by either claim),
`PROVINCE.md` (C1 append-after-last-line only + prefix-preserved binding), `LOG.md`,
`corpus/knowledge/*` (new entry only; existing blobs byte-preserved as prefixes at REV),
`corpus/evidence/round-44/c1/**` (first-added after the freeze — the receipts dir),
`corpus/lessons/round-44*.md` (the round's lesson, lands at close).

## Changes from the draft

(as of the wave-1 fold, listed at the top of this file: carriers 4→6 with v2.1; freeze-walk
port source round-43 not round-42; CTL-C1-4/CTL-C1-5 added; compression bound to the superblock
field; zero-gap rule for these carriers; sentinel B1–B5 C2 redesign; SOURCES pre-land S138/S139;
entry stem fixed; frozen-file model corrected to BASE-pinned + append-only for
SCORECARD/SHONEN/README/PROVINCE/LOG/knowledge; missing-inputs added.)
