# R36ScribeSkill — SKILL.md draft: SquashFS recursion through sasquatch (round 36)

Seat: leaf scribe, advisory only. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read at
`d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (HEAD, `main`, 2026-10-26). Only this file was written.
No VCS mutation, no install, no REA/unblob/sasquatch run, no counter or selftest executed, no
subagent. No scratch directory was created and nothing was written under `/tmp`: every command in
this seat was a read (`git show`/`ls-tree`/`status`, `jq`, `wc`, `grep`) over committed or working-tree
bytes, so no temporary storage was needed and none was left behind.

Read first, as instructed: `plans/round-36-claims.md` (frozen claims), PROTOCOL
`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:388-437` (`## Gate standard`,
Registry home = the child lane's own `SKILL.md`), then `SKILL.md` (registry home section at
`SKILL.md:438` and the round-22…34 per-round registry precedent), `tools/round-36/c1-counter.py`,
`tools/round-36/c2-counter.py`, `tools/round-36/c1-run.sh`, `.ufo/waves/round-36/controls/*`, and the
committed round-36 envelopes `corpus/evidence/round-36/c1/K{1..4}/{before,after,*-run}.json`.

## 1. Behavior

The draft below is one new top-level section, `## SquashFS recursion through sasquatch — round 36`,
intended for append at the end of `SKILL.md` (after `### Round-34 run-6 instrument registry — the
shortcut-replay gate (stopped capability)`, the current last section). It does three things:

1. turns the round-36 REA surfaces into a **signal → meaning → action** decision table whose rows are
   each anchored to a committed envelope field and a committed evidence path;
2. fixes the **order of operations** for a sasquatch recursion measurement (oracle → before arm →
   install → after arm → counter) so a later run cannot retrofit a before-arm;
3. registers the two round-36 counters at this repo's registry home in the §Gate standard field order
   (`tool | gate or probe | verdict map | self-test command | pinned-value path | write scope | owner`).

It states no new capability: every claim in it is a reading of committed bytes, and the limits
paragraph keeps it below "sasquatch recursion works everywhere".

## 2. Draft section (verbatim, ready to append to `SKILL.md`)

````markdown
## SquashFS recursion through sasquatch — round 36

Round-36 moved sasquatch (unblob's `squashfs_v4_le` recursion extractor) from the PROVINCE Frontier
bullet into a Core row. The REA `extract-firmware` envelope is the only judge of whether recursion
happened; no amount of local `unsquashfs` success substitutes for it, and no receipt is ever edited to
look like a pass. Claims, target and kill rule: `plans/round-36-claims.md` (R36-C1); carrier, oracle
and before-arm evidence: `corpus/evidence/round-36/c1/`.

### Decision table — REA envelope signal to action

| Signal in the `extract-firmware` envelope | Meaning | Action |
|---|---|---|
| `extraction_gaps[]` entry with `kind` = `missing-extractor-dependency`, `dependencies` = `["sasquatch"]`, `handler` = `squashfs_v4_le` — recalled (`corpus/evidence/round-36/c1/K1/before.json`, `K3/before.json`) | The `squashfs_v4_le` handler reached a SquashFS 4.0 little-endian container and the extractor binary was not resolvable on `PATH` for that run. `range.offset`/`range.length` are the container's byte span; `root_file_range` repeats it when the container is the input root. The envelope does **not** say the image is unreadable | Install the official onekey-sec `sasquatch_1.0_amd64.deb` binaries into `~/.local/bin` (`sasquatch`, `sasquatch-v4be`; no pacman, no AUR, no rebuild — `plans/round-36-claims.md`), confirm `command -v sasquatch` resolves, then rerun `extract-firmware` on **the same input** with a **fresh `output_directory`**. Keep the old envelope as the paired before-arm; `K3/after-run.json` records `/home/vgpnk/.local/bin/sasquatch`, `unsquashfs version 4.5.1 (2022/03/17)`, sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` |
| No sasquatch gap, and every oracle regular file is present at a path whose suffix is the oracle's relative path with equal sha256 — recalled (`K1/after.json`: 3/3, 0 gaps) | Recursion published the filesystem's regular files. `publish = regular files only` | Nothing to install. Record both arms and the oracle unchanged; score with the counter, never by eye |
| Before arm publishes nothing, or publishes the container as one opaque file `…/<offset>-<end>.squashfs_v4_le` — recalled (`K1/before.json`: 0 files, `published_bytes` 0; `K3/before.json`: 2 files, the carved ELF and `944632-11454968.squashfs_v4_le`) | Blocked recursion is *opaque container publication*, not a partial extraction: the container's own bytes are published as a single file and no entry inside it is | Never compare file counts across arms, and never read the opaque range file as an extracted file. Compare the oracle's `(relative-path suffix, sha256)` rows only |
| `extraction_gaps[]` with `kind` = `unpublished-entry`, and/or `normalized_result.unpublished_entries[]` with `kind` = `symlink` and a `link_target` — recalled (`K2/after.json` `var/notice-link`; `K3`/`K4/after.json` `.DirIcon`, `nvim.png`) | Symlinks (and special files) are retained as metadata only: `extraction_continuations[].instruction` = "The entry is retained as metadata; only regular files are published, without executable permission bits" (`K3/after.json`). **Not** a sasquatch failure and **not** blocked recursion: an after-arm with recursion published still carries these gaps | Do not chase it, do not claim it as published, do not install anything. Filter gaps by `kind` + dependency name (`c1-counter.py` `sasquatch_gap()`), never by "gaps list is empty" |
| AppImage: `chunks[]` holds one `elf64` chunk starting at 0 and exactly one `squashfs_v4_le` chunk whose `range.offset` equals the ELF end — recalled (`K3/after.json`: `elf64` 0..944632, `squashfs_v4_le` 944632..11454968; `K4` 936456..) | Type-2 layout: an ELF runtime with the filesystem appended; `hsqs` sits at that offset, not at byte 0 | Run the independent oracle as `/usr/bin/unsquashfs -o <that offset>`. The harness rule `e_shoff + e_shnum*e_shentsize` (`tools/round-36/c1-run.sh`, oracle mode) is **one operand** of the type-2 runtime rule (the runtime takes the larger of it and the end of the last section header); the two coincide on K3/K4 (`K3/oracle-run.json` `squashfs_offset` 944632) — do not state the AppImage specification defines any offset |
| After-envelope `files` count exceeds the oracle's regular-file count — recalled (`K3`/`K4` 2147 vs 2130; nested `…/usr/bin/nvim_extract/0-11170568.elf64_extract/carved.elf`) | Nested carves and nested ELF extracts are published beside the squashfs files | Match by suffix + sha256. Extras are not extra extraction and are not evidence of a second filesystem; count equality is not identity |
| `operation` ≠ `extract_firmware`, or `provider.id` ≠ `unblob` — the counter's own binding | Wrong verb or wrong provider: the receipt is not comparable to a squashfs-recursion claim | Rerun `npx -y rea-agents@6.5.0 extract-firmware --format json <input> <fresh-outdir>`; do not relabel a receipt from another verb |
| An envelope whose `files` or `extraction_gaps` were edited by hand no longer recomputes to its stored `ev_…` id under the rea-agents 6.5.0 rule (`c1-counter.py` `evidence_ids()`, frozen `tools/round-27/xpin-attribute.mjs`; selftest case "forged oracle-copy envelope") | A patched envelope is not a receipt, however plausible its file list | Never patch, reorder or trim an envelope. A receipt that does not recompute is a failed measurement, and the remedy is a rerun, not an edit |

### Reproduction order (a later run must not retrofit a before-arm)

1. `tools/round-36/c1-run.sh oracle CARRIER OUTDIR` — independent `/usr/bin/unsquashfs` 4.7.5, offset
   0 for a bare image and the ELF end for an AppImage, regular files only.
2. `tools/round-36/c1-run.sh before CARRIER OUTDIR` — the harness strips every `PATH` directory that
   holds an executable `sasquatch` and refuses (exit 2) if one survives. Keep this envelope.
3. Install the two deb binaries into `~/.local/bin`; `command -v sasquatch` must resolve.
4. `tools/round-36/c1-run.sh after CARRIER OUTDIR` — `PATH` as given, fresh output directory; exit 0
   with `sasquatch_version` populated in `<mode>-run.json`.
5. Score at a named revision with the counter; a miss is an honest stop, and the counter, predicate,
   carriers and oracle are never changed after the freeze commit.

Harness exit map (`tools/round-36/c1-run.sh`): 0 ok, 2 usage/environment error, 3 tool failure.

### Round-36 instrument registry

| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-36/c1-counter.py` | gate — R36-C1 coverage, sasquatch squashfs recursion Frontier → Core | 0 clean (`carriers_matched == 4` and every binding true); 1 failed (target not met at the measured revision); 2 could-not-evaluate (missing `--root`/`--rev`/`--freeze`/`--pkg65`, unknown revision, git/node failure, `xpin` tool absent at the freeze). No other code | `python3 -I -B tools/round-36/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` — flag spelling `--selftest`; 14 isolated git-fixture cases (1 green, 13 red), exit 0 iff no case fails, 1 otherwise | Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0` pins `corpus/evidence/round-36/c1/carriers.json` (K1-K4 id + sha256), every `K*/oracle.tsv` and `tools/round-27/xpin-attribute.mjs`; `carriers_unchanged`/`oracle_frozen` compare measured-revision bytes against the freeze bytes, so a post-freeze edit is visible, not silent. Target `4` is a literal in the script. Selftest fixtures: `tools/round-36/selftest/dev-{before,after}.json`, `dev-oracle.tsv`, `dev-le-xz.sqsh`. Control verdicts committed at `6a870b9290e9566468d7d9e6d1b8308daf025b12` under `.ufo/waves/round-36/controls/ctl-c1-{0,1,2}-*.{json,out}` (each `CTL-C1-n exit=1`) | Reads git objects, `node`, and the rea-agents 6.5.0 package tree; writes only a private directory under `$HYAKU_SCRATCH/kaidoku-r36` (default `/fast/scratch/hyaku/kaidoku-r36`) and `--json-out`; `--selftest` creates and removes one `c1-selftest.*` git fixture repo per case under the same root (each fixture asserts `git -C <fixture> rev-parse --show-toplevel` equals the fixture) | kaidoku |
| `tools/round-36/c2-counter.py` | gate — R36-C2 calibration, self-assessment surfaces vs observed repo state | 0 clean (`mismatches == 0` and `guards_ok`); 1 failed; 2 could-not-evaluate (missing `--root`/`--rev`/`--base`, unknown revision, `SCORECARD.md`/`SHONEN.md` absent). No other code | `python3 -I -B tools/round-36/c2-counter.py --selftest` — flag spelling `--selftest`; 13 isolated git-fixture cases (1 green, 12 red), exit 0 iff no case fails, 1 otherwise | Base `cab59f221fe19726b5692bfa4d9a9679e96b8a73` is the guard baseline: no unit removed, no fewer pointers than at the base, and every pointer unresolved at the base repaired by a resolving pointer to the same document. Stated values live in SCORECARD `## Owned axes` / `## Capabilities` and the SHONEN boxes and are compared with command A (`corpus/knowledge` files ↔ `corpus/README.md` coverage map, queue-drain rule blocks ↔ resolvable `corpus/knowledge/…:line-range`) and command B (`evidence/round-1-2026-10-15/result.json` aligned/total obligations), plus two observed heading ranges (`SKILL.md` `## Queue-drain craft`, `PROVINCE.md` `## Adjacent`). Control verdicts under `.ufo/waves/round-36/controls/ctl-c2-{0,1,2,3}-*.{json,out}` (each `.out` ends `ctl-c2-n-… exit=1`) | Reads git objects only; `--json-out`; `--selftest` creates and removes one `c2-selftest.*` git fixture repo per case under `$HYAKU_SCRATCH/kaidoku-r36` | kaidoku |

Both rows are read-only over every surface they do not own and never act on an external surface. A
verdict names the revision it was measured against; a run over a moving worktree is not comparable to
one over the cited commit.

### Limits (read with every row above)

1. The blocked-recursion signal is byte range + dependency name only. The envelope does not say
   whether sasquatch of any version would parse a vendor-mangled table, and no such carrier exists.
2. Big-endian and AVM SquashFS, vendor-mangled images, loader behaviour, and the extracted programs are
   not claimed. `sasquatch-v4be` is installed but no carrier exercises it.
3. Published files carry no permission bits (`extraction_continuations[].instruction`); executing an
   extracted program needs its own evidence.
4. K3/K4 identity is `subject.digest.sha256`. `subject.local_path` in the committed envelopes points
   into scratch and is not durable evidence.
5. The AppImage offset caution above is observed equivalence on K3/K4 under the runtime's two-operand
   rule, not a general theorem about arbitrary ELF layouts.
6. The 7z fallback path was not retested in round 36.
7. No digest-pinned `expected.json` baseline exists for these two counters: input identity is pinned by
   the freeze commit (a git object the counter compares byte-for-byte), and the expected exits are the
   selftest case table in the script plus the committed control receipts — not a separate digest file.
8. This registry covers the two round-36 counters only. `tools/round-35/c1-coverage-counter.py` and
   `tools/round-35/c2-calibration-counter.py` still have **no** registry row at this home; that debt is
   reported in round 36 and is not discharged here.
````

## 3. Registry-row conformance notes (why each cell says what it says)

- **Field order** is exactly the §Gate standard list (`PROTOCOL.md:411-417`): name, `gate|probe`,
  entry command, verdict map, self-test command and spelling, pinned-value path, write scope, owner.
  Both tools are `gate` (each has a committed self-invocation over isolated fixtures with expected
  exits, and each returns a verdict against persisted expected values), so neither is registered as a
  probe.
- **Verdict maps** are read from the counters' docstrings and `main()`, not executed:
  `c1-counter.py` — `return 0 if res['met_target'] else 1`, `return 2` on missing flags, and `2` on
  `Unevaluable` (raised by `git`, `xpin` absence, node failure); `c2-counter.py` — same shape with
  `met_target` = `mismatches == 0 and guards_ok`. No other exit code exists in either `main()`.
- **Self-test tallies** (14 = 1 + 13; 13 = 1 + 12) match `plans/round-36-claims.md` and the `cases`
  list in each script. I did **not** run either selftest; the tallies are source-read, and the claim
  file is the committed expectation they must match.
- **Two evidences** (§Gate standard): the committed control receipts are the frozen-run evidence
  (`6a870b92`, all seven controls exit 1 — read from
  `.ufo/waves/round-36/controls/ctl-*.out`: `CTL-C1-0/1/2 exit=1` and
  `ctl-c2-0/1/2/3-… exit=1`), and the
  freeze/base commits pin the inputs. The one clause not satisfied in the §Gate standard's own
  vocabulary is the mandate that a frozen baseline's `expected.json` pin every snapshot input digest —
  here input identity is a commit hash, and expected exits are script literals plus those control
  receipts. Disclosed as limit 7 rather than papered over; a repair would change a frozen counter, so
  this seat reports it.
- **Pinned-value truth check on C1**: `carriers_unchanged` compares `carriers.json` at the measured
  revision with the freeze copy, and `oracle_frozen` does the same per `oracle.tsv`; the four carrier
  sha256 values in `carriers.json` are what `before_subject_ok`/`after_subject_ok` compare against the
  envelopes' `subject.digest.sha256`. So the row's claim "a post-freeze edit is visible, not silent" is
  a property of committed code, not an executed observation.
- **Registry home**: `SKILL.md:438` (`## Local round-evidence gate registry`) is the older r1 gate set;
  round sections carry their own `### Round-NN … registry` tables (round-22 through round-34). A new
  top-level round-36 section with its own registry table therefore follows the live convention, and
  §Gate standard's "registry home is its own `SKILL.md`" is satisfied by the section living in this
  file. No second inventory is created elsewhere.

## 4. Gates

- **Executed by this seat: none.** No counter, selftest, REA run, unblob, unsquashfs, sasquatch or
  harness invocation; no install or upgrade. The assignment forbids rerunning work to decorate a
  report, and the registry cells that describe verdicts are sourced from code and committed receipts.
- **Committed gate evidence cited** (not re-run): `.ufo/waves/round-36/controls/` — 7 receipts, one
  `.json` + one `.out` per control, all recorded `exit=1` at `6a870b92`, including
  `ctl-c1-1-no-sasquatch-pipeline.json` (`carriers_matched` 0, `carriers_unchanged` true,
  `met_target` false on a fixture repo) and `ctl-c2-0-do-nothing.json`.
- **Working-tree (uncommitted) evidence, not cited in the draft**: `.ufo/waves/round-36/interim/c1-after-receipts-only.json`
  reports `revision` `3310d8fa27bfaa95ad858c4aaad6f6377f853982`, `carriers_matched` 4,
  `carriers_unchanged` true, per-carrier `after_oracle_hits` = 3/4/2130/2130 and
  `before_oracle_hits` = 0, `after_sasquatch_gap` false, and **all five bindings false**
  (`entry_present`, `province_core_section`, `province_core_row`, `sourced`, `coverage_map_row`) →
  `met_target` false. `git status --porcelain` at HEAD lists that directory as `??`, so it is not a
  citable committed path and the draft does not use it.

## 5. Touched surfaces

- Written: `.ufo/waves/round-36/w1/R36ScribeSkill.md` (this file). Nothing else.
- Read only: `plans/round-36-claims.md`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`,
  `tools/round-36/{c1-counter.py,c2-counter.py,c1-run.sh}`,
  `corpus/evidence/round-36/c1/{carriers.json,K1..K4/{before,after,before-run,after-run,oracle-run}.json,K*/oracle.tsv}`,
  `.ufo/waves/round-36/controls/*`, PROTOCOL `## Gate standard`, and
  `git ls-tree`/`status`/`log` for HEAD state. No lane file was edited; `SKILL.md` was not modified —
  the section is delivered as a draft in §2 for the integration owner to land.

## 6. Out of scope (deliberately not done)

- Landing the section in `SKILL.md` (my write bound is this report; L1 is the integration owner).
- Any repair: C1's knowledge entry, PROVINCE Core row, `corpus/README.md` coverage-map row, SOURCES
  rows, and the counter/selftest code are untouched — a defect found is reported, not repaired.
- Running C1 or C2 at HEAD, or the carrier harness (executor work; the C1 bindings are still unmet at
  HEAD because the entry has not landed).
- Round-35 registry rows (finding F3), the AppImage/SOURCES drafting (scout seats' S110-S112 drafts),
  and the assimilation entries.
- Deciding whether the AppImage `max(sht_end, last_section_end)` nuance enters the knowledge entry; I
  only made the draft refuse to attribute an offset rule to the AppImage specification.

## 7. Findings

- **F1 (informational, for L1's landing order).** At HEAD `d2e46ef5`, `PROVINCE.md` still holds the
  Frontier bullet (`PROVINCE.md:149`, "sasquatch — unblob's squashfs recursion extractor (AUR-only)")
  and contains no `## Round-36 additions to Core` section; `corpus/README.md:44` still says "AppImage
  SquashFS carved but recursion blocked by missing sasquatch"; the round-36 knowledge entry does not
  exist at HEAD. So the C1 counter's five bindings are necessarily false at HEAD even though the
  after receipts are committed at `3310d8fa`. The draft therefore cites only committed envelope and
  harness paths for its table, and the registry row's "0 clean" verdict is the code's contract, not a
  measured HEAD verdict.
- **F2 (disclosed limit, PROTOCOL §Gate standard "Two evidences").** Neither round-36 counter has a
  frozen `expected.json` pinning snapshot-input digests; input identity is a freeze/base commit and
  expected exits are script literals plus the committed control receipts. Registered as limit 7. A
  fix would edit frozen counters, so it is routed rather than applied.
- **F3 (registry debt, pre-existing).** `tools/round-35/c1-coverage-counter.py` and
  `tools/round-35/c2-calibration-counter.py` are committed (`2323d197`, `a85ca674`, `13d7a815`) and
  round 35 was closed as an honest stop, but `SKILL.md` has no round-35 section and therefore no
  registry row for either — §Gate standard's "closure grades no gate conformant until its registry row
  exists at the lane's registry home" is unmet for r35. Not repaired here (my scope is the two r36
  counters); the draft discloses it as limit 8 so a reader does not read the round-36 table as a
  complete inventory.
- **F4 (draft-scope caution, AppImage).** The committed harness formula
  `e_shoff + e_shnum*e_shentsize` (`c1-run.sh`, oracle mode) is one operand of the type-2 runtime's
  rule (`max(sht_end, last_section_end)`); the operands coincide on K3/K4 (exactly one section table end
  = 944632/936456 equals `oracle-run.json` `squashfs_offset`). [INFERENCE] The runtime-rule statement
  is source-backed in the round-36 scout draft (S110) but that file is untracked, so the draft states
  only "one operand" and "coincide on K3/K4" with committed pointers, and makes no claim about the
  AppImage specification.
- **F5 (calibration note on the oracle/published ratio).** K3/K4 publish 2147 files against 2130 oracle
  regular files because nested carves (`carved.elf`, nested `elf64` extracts) are published in the same
  file list. The draft makes "match by suffix + sha256, never by count" explicit, because a future
  editor reading only the counts would conclude the extraction invented 17 files.

## 8. Artifact paths

- Deliverable (this seat): `.ufo/waves/round-36/w1/R36ScribeSkill.md`.
- Proposed landing target: `SKILL.md` (append the §2 section; no other edit).
- Committed anchors cited: `plans/round-36-claims.md`; `tools/round-36/c1-counter.py`,
  `tools/round-36/c2-counter.py`, `tools/round-36/c1-run.sh`, `tools/round-36/selftest/dev-{before,after}.json`,
  `tools/round-36/selftest/dev-oracle.tsv`; `corpus/evidence/round-36/c1/carriers.json` and
  `K1..K4/{before,after,before-run,after-run,oracle-run}.json` + `K*/oracle.tsv`;
  `.ufo/waves/round-36/controls/ctl-{c1-0,c1-1,c1-2,c2-0,c2-1,c2-2,c2-3}-*.{json,out}`;
  `PROVINCE.md:149`; `corpus/README.md:44`; `tools/round-27/xpin-attribute.mjs`.
- Commits: freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`; controls
  `6a870b9290e9566468d7d9e6d1b8308daf025b12`; C1 after receipts
  `3310d8fa27bfaa95ad858c4aaad6f6377f853982`; base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`;
  read HEAD `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`.
- Tooling: none installed, upgraded or removed (RULES.md read; pacman host-paused; no npx/uv/cargo
  channel used by this seat).

## 9. Command record (all read-only; temporary-shell execution noted where true)

| Purpose | Command |
|---|---|
| Lane pin and round commits | `git rev-parse HEAD`; `git log --oneline -8` |
| Committed round-36 artifact inventory | `git ls-tree -r --name-only HEAD -- corpus/evidence/round-36 corpus/knowledge`; `… -- .ufo/waves/round-36`; `… -- tools/round-36` |
| Untracked wave state (why interim receipts are not cited) | `git status --porcelain`; `git status --porcelain .ufo/waves/round-36` |
| Gap/chunk/file facts | `jq` over `corpus/evidence/round-36/c1/K{1..4}/{before,after}.json` (`extraction_gaps`, `unpublished_entries`, `extraction_continuations`, `chunks[].handler/range`, `files`, `published_bytes`, `subject`, `evidence_id`) |
| Oracle/run metadata | `jq` over `K3/{after-run,before-run,oracle-run}.json` |
| Surface state | `git show HEAD:PROVINCE.md`; `git show HEAD:corpus/README.md`; `git show HEAD:SCORECARD.md`; `git show HEAD:SHONEN.md` |
| Control verdicts | `cat .ufo/waves/round-36/controls/ctl-c1-1-no-sasquatch-pipeline.{json,out}` |
| Registry precedent | `grep -n '^#' SKILL.md`; `read SKILL.md:430-500,1180-1221`; `grep -n "Gate standard" -A 80 <PROTOCOL>` |

A few of those calls ran in a temporary shell (session-state warning in the output); all of them are
stateless reads, so nothing was lost.
