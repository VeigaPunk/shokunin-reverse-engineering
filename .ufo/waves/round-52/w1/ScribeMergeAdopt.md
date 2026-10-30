# ScribeMergeAdopt — kaidoku round 52, wave 1 (build+attack), seat report

**Role:** scribe (assimilation adoption). **Verdict: settled** — one ADMIT (re-grounded, narrowed),
one REJECT (already-held ground), the id-collision analysis and the renumber map are delivered as
drafts for the L1. Nothing was appended to the lane; no REA run; no vendor byte fetched.

## 1. Behaviour delivered

| artifact | content |
|---|---|
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/plan.md` | the adoption plan: candidate ranking (12 theme candidates), the Gate, the corrections, the re-grounding plan, the id-collision analysis, the renumber map, the landing edits, the limits |
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/sources-rows.md` | the normalized 11-column `corpus/SOURCES.md` rows (S253–S260), validated: 11 cells each, **no pipe character in any cell**, ISO `opened`/`recheck`, `status` = `mined`, `used-by` = the adopted entry path |
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/entry.md` | the transformed entry text (sources re-pointed to the renumbered rows), with its `## Gate` block and the seven recheck commands |
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/gate-receipts.txt` | exact command, exit code, stdout sha256 and UTC time for all seven re-opened documents |
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/census-mirror.txt` + `census-after.txt` | the scratch-mirror census gate: command, exit code (**0**), output sha256, full validator output (0 errors, the lane's known 19 W04) |
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/collision/{reg-ids,staged-ids,collisions}` | the collision artefacts (158 / 132 / 44) |
| `.ufo/waves/round-52/w1/ScribeMergeAdopt/status.json` | seat, role, status, summary, artefacts |

## 2. The gates that were run (and what they decided)

- **Theme scan (read-only):** `MERGE-REPORT.md`, `SOURCES.append.md`, all 77 staged entries,
  `corpus/README.md` (coverage map + Knowledge table), `corpus/SOURCES.md`, and the lane's round-36 →
  round-43 lessons/spot-checks for the standing verdicts. 11 staged entries touch the
  SquashFS/AVM/unblob/sasquatch theme; 10 are already held or standing-refused.
- **Source re-open (2026-10-30, 6 upstream documents + 2 campaign-local tables, scratch only):**
  Freetz-NG at commit `86c23d96d76585825fa81b5cb29105e9d2ad6654` — `docs/make/README.md` (85 254 B,
  sha256 `11477511…`), `613-avm_format_as_option.patch` (1 601 B, `9af3b3de…`),
  `550-mkfs_time__AVM_BE_AVM_LE.patch` (1 080 B, `603c36c9…`),
  `250-mksquashfs__AVM_BE.patch` (2 775 B, `f5964ad9…`),
  `tools/make/squashfs4-host-le/squashfs4-host-le.mk` (2 622 B, `6d2abb49…`),
  `tools/make/squashfs4-host-le/patches` (28 B symlink, `6008eb3f…`); plus the two campaign-local
  tsvs (940 B `523637c8…`, 964 B `4c962bac…`). Every recheck count in the drafts is an observed
  output (1, except the 250 patch's guard count of 2), not a written expectation.
- **Collision gate:** the addendum's `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` over both files,
  `comm -12` → **44** collisions, plus a permissive second extractor proving the 0–3-space guard misses
  **0** registry rows (every row is indented by exactly 2 spaces).

## 3. Touched surfaces

Only inside `.ufo/waves/round-52/w1/ScribeMergeAdopt/` and this report file. **Not** touched:
`corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, the
fleet repo, `.ufo/state/`, `.ufo/watchdog.log`, any sibling lane. No git/jj mutation of any kind.

## 4. Out of scope (and why)

- **No REA run and no vendor fetch** (contract: the L1 alone runs REA; the AVM licence keeps vendor
  bytes out of the lane). The adoption therefore cites published upstream documents and the lane's
  committed measurements only.
- **The staged package was not appended.** The plan gives the L1 the rows; the freeze commit lands
  them.
- **`considerthese/` does not exist in this lane** (checked: absent from the tree and the worktree) —
  one report line, per the claims' Frontier step.
- **No census mirror was run** — the scratch-mirror `sources-census.sh validate --file` gate belongs
  to the append the L1 performs; the plan states it as a required pre-append step (round-36
  precedent, including the E11 mirror artefact).

## 5. Findings (for the canonical judge)

1. **ADMIT — `avm-le-image-genuine-marker` (staged S212/S213/S214), narrowed and re-grounded.** It is
   the only theme entry that is neither already held nor standing-refused, and it fills a gap the
   lane names itself: the round-50 entry's limit 1 says *"No registered `corpus/SOURCES.md` row cited
   by this entry describes an LE AVM layout."* Upstream does describe it — Freetz-NG
   `docs/make/README.md` § `squashfs4-le`: *"The only difference of this format to the original LE
   format is that the value of the mkfs_time superblock field is equal to the bytes_used field."*
   The staged entry's own claims are re-grounded on five pinned upstream documents; the marker-blindness
   and re-stampability observations stay cited as held (r50, S245), not restated.
2. **The staged S214 citation is sound only with S257.** `613-avm_format_as_option.patch` lives in the
   **AVM-BE** recipe's patch directory; the LE recipe reaches it through the git symlink
   `tools/make/squashfs4-host-le/patches → ../squashfs4-host-be/patches`. A row that cites the patch
   without the symlink is mis-grounded — the exact failure mode of the round-38/39 `avm-*` refusals.
   **The marker is a writer switch**: with `AVM_FORMAT_AS_OPTION` upstream emits it only under
   `-no-mkfs-time` ("use AVM format (length instead of timestamp)").
3. **REJECT — `avm-image-extraction` (staged S200/S201), the next-best candidate.** Already-held
   ground: the staged rows name `lanes/kaidoku/round11/work/lead1-avm-image.tsv`, and the lane
   **already registers that exact file as row S126** (sha256 `f205807d…`, re-verified today); r40/r41
   hold the strictly stronger result — the same AVM-BE layout end-to-end on four real vendor carriers.
   It is also the wrong endianness for round 52 (BE; the class is LE). Flip: a new upstream BE-recipe
   document the lane lacks, or a lane-retained built AVM-BE image under `corpus/evidence/`.
4. **Id-collision correction to the claims' expectation.** The claims say "mass id drift is expected";
   the measured reality is sharper: the registry holds **158** ids = `S001–S149` **plus** `S243–S251`,
   and `S150–S242` (93 ids) are **unused**, while the staged package occupies `S106–S237`
   contiguously. So only **44** staged ids collide today (`S106–S149`) — and **88 staged ids would
   land silently inside the lane's free band**, where the next package refresh can reuse them for
   different documents. Every staged id must therefore be renumbered into the lane's own space;
   the map continues at **S253** (S252 is reserved by the claims for the man7 `mknod(2)` row) and is
   by **document**, not by count.
5. **Scope correction the L1 must not lose.** Upstream names AVM-LE's users as *"some cable boxes,
   e.g. 6490, 6590"* — but the round-50 census found the marker on 28 LE members across **16 models**,
   and two of the four round-52 carriers (7581, 7582) are **not** cable boxes. The adopted row teaches
   the **format**, not the device population; the round-52 Core row must not be phrased as "AVM-LE is
   the cable-box format".
6. **Method lesson worth mining into `corpus/lessons/round-52.md`:** a changed `-D` define is **not** a
   make dependency — `make` reported *"'mksquashfs' is up to date."* and the binary's sha256 was
   unchanged (`1a7cfcf7…`), so an earlier AVM_LE measurement was taken with a stale binary. The rule:
   assert the instrument's digest changed before reading its output.
7. **Defect caught and fixed before the freeze (sibling `SentSecrets-2`, 2026-10-30).** My first draft
   put prose in the `recheck` cell; the census validator's rule is
   `recheck !~ /^[0-9]+d$/ && !symbolic(recheck)`, so the mirror run exited **1** with **8 × E09** on
   S253–S260 (the lane baseline alone exited 0). Fixed: the cell now holds the bare cadence `180d`
   and the ISO run date, command and observed count live in the entry's `recheck:` header and
   `## Gate` block. A second placement rule surfaced in the same gate: the rows must be inserted
   **after the last registry row** (the S251 row) — appending at EOF raises **8 × E12** "row outside
   Registry section". **This seat then re-ran the gate: exit 0, 0 error codes, the lane's known 19 W04
   only** (`receipts/census-mirror.txt`). **Independently re-verified by the sentinel
   `SentSecrets-2`** on its own scratch mirror (rows sha256 prefix `beb6c67d703ab0da`, all 12 pipes,
   `recheck='180d'`, inserted after the last registry row): `validate --file … --today 2026-10-30`
   → exit 0, 0 error codes, `ok` + 19 W04, stdout sha256 `d8d9e092508d9ce2…`; the same 8 rows
   appended at EOF → exit 1 with 8 × E12, reproducing the placement rule. Their finding F1 is marked
   **CLOSED**; the credential re-scan of this seat's 10 files is clean (live_hits 0,
   `placeholder_hits 0`). Receipts: `.ufo/waves/round-52/w1/SentSecrets/receipts/{census-sibling-rows-S253-S260-FIXED.tsv,census-sibling-rows-EOF-append-E12.tsv,credscan-sibling-seat-after-fix.json}`.
      The sentinel also digest-verified the two own-work rows' pinned artefacts against the bytes on disk
      (`523637c885bb50c6…`, 940 B; `4c962bacd24af813…`, 964 B — both match) and flagged the **path
      convention**: my rows cite the **absolute** existing path under
      `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/`, while the package's staged rows use
      the relative `lanes/kaidoku/roundN/work/…` form, which does not resolve in this lane (no `lanes/`
      directory here). The L1 must keep the absolute form — it matches the lane's own precedent S126.

## 6. Artifact paths (absolute)

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt.md` (this file)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/plan.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/sources-rows.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/entry.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/status.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/gate-receipts.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/collision/{reg-ids,staged-ids,collisions}`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/census-mirror.txt`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeMergeAdopt/receipts/census-after.txt`

## 7. Checks the L1 should run (and what this seat already ran)

- **Scratch-mirror census gate — RUN and CLOSED by this seat** on 2026-10-30:
  `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` on a mirror of the lane tree
  at HEAD carrying S253–S260 (inserted after the last registry row) and the new entry → **exit 0**,
  **0** error codes, the lane's known 19 W04 only. Receipt `receipts/census-mirror.txt`.
- **Registry pipe invariant:** every appended row must have exactly **12** pipe characters
  (11 cells). The drafted rows are validated to that rule; the S255 anchor had to drop the source's
  `||` for it, and the L1's copy must keep that change.
- **The `recheck` cell must stay a bare cadence** (`180d`) — prose raises E09; the run detail lives
  in the entry's `recheck:` header and `## Gate` block.
- **Row placement:** the new rows go **after the last registry row** (the S251 row), not at EOF,
  which raises E12.
- The freeze-commit consistency: the adopted entry is **adjacent** ground to R52-C1's entry
  (`2026-10-30-r52-avm-le-squashfs-core.md`); it must not duplicate, and must not be cited for, the
  device-accounting law (S250/S251/S252).
