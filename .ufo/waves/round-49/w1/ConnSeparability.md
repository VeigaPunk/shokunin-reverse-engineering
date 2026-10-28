# ConnSeparability — R49-C1 / R49-C2 causal separability (wave 1, pre-freeze)

Seat: ConnSeparability (leaf connector, no dispatch). Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Dev freeze `352e24c6728df9da4b7aa2e410cfbc4ab4a70622` (both clones built by `mkclone.sh`, identical hash). Receipts: `.ufo/waves/round-49/w1/ConnSeparability/` (`MANIFEST.sha256` lists all 58 files).

## Verdict

**Separable on verdict; not separable on read set.** Verdict-level: C1 is green on X only (exit 0), C2 is green on Y only (exit 0), and both are green together on Z = X + Y (exit 0 / exit 0). Read-level: the only shared content path is `corpus/SOURCES.md`, and C1 is sensitive to 2 of its 148 rows (S138, S139) while C2 is sensitive to 4 (S145–S148). **Two read-set statements in the plan are false as written**: (a) C2's `--battery` do-nothing overlay reads content and names of C1's landing paths (`PROVINCE.md`, `corpus/README.md`, the four `corpus/evidence/round-49/c1/*/after.json`, the knowledge entry); (b) C1's `frozen_drift` runs an unpathspec'd `git log --name-status FREEZE..REV`, so it names C2's landing paths (`SCORECARD.md`, `corpus/lessons/round-49.md`, `corpus/evidence/round-49/c2/*`). Both are verdict-neutral (Z proves it on the current bytes), but the plan's sentence "neither counter reads a path the other's landing writes, except `corpus/SOURCES.md`" is not true of the drafts. Fix before freeze (F3, F4).

## Constructions

| Tree | Built from | HEAD | Landing content |
|---|---|---|---|
| X | `run-ctl.sh <clone> <W> --controls pos` (CTL-C1-POS sandbox, `ctlX/ctl-work/run.oosncacy/sandbox-pos`) | `af056786b86525518973a1f34a5fb217a732854b` (parent 352e24c6) | C1 only: 4 real REA 6.5.0 after.json receipts (`corpus/evidence/round-49/c1/{v1le,v1be,v2le,v2be}/after.json`), `knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, PROVINCE.md +8, README +1, SOURCES.md S138/S139 `used-by` +entry (4 +/-). Caveat: the POS plant replaces `<AFTER-DATA>` with the POS fixture headline, so this is a fixture, not the data landing. |
| Y | `mkclone.sh Y` then `c2-after.py Y` | `3addb6d694401e178a57757cc6f2950732b8dbcd` (parent 352e24c6) | C2 only: `corpus/lessons/round-49.md`, SCORECARD.md `## Record corrections — round 49`, SOURCES.md S147/S148 + two search-log lines, `corpus/evidence/round-49/c2/{popper,sysexits}.html`. 5 files, 2759 insertions. |
| Z | X clone + `git fetch Y HEAD` + `git cherry-pick 3addb6d6` | `97513487…` (auto-merged SOURCES.md, no conflict) | X ∪ Y, 12 files changed |
| F | the freeze itself | `352e24c6…` | nothing |

Both clones' toplevels were asserted equal to their dirs before any commit. Identities were set in clones only (`r49-dev`, `r49-c1-controls`, `r49-z`).

## Findings table

Exit codes are the counters' own (0 met / 1 not met). Full receipts in `out/`. Counter sha256 for C1 (`d6d70cb7…`) and C2 (`90fa4722…`) are the frozen-tree copies in the X clone.

| # | Command (abridged; full in `tools/score.sh`) | Exit | Key result | stdout/receipt sha256 |
|---|---|---|---|---|
| 1 | `c1-counter.py --root X --rev af056786 --freeze 352e24c6 --pkg65 rea-agents-6.5.0 --json-out out/c1-X.json` | **0** | `met_target true`, `carriers_matched 4`, `frozen_path_changed []`, all 12 bindings true | `out/c1-X.json` a3fcb0da5c1d70bd… |
| 2 | `c1-counter.py --root Y --rev 3addb6d6 --freeze 352e24c6 …` | **1** | `carriers_matched 0`; bindings false: `province_core_section`, `province_core_row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row` | `out/c1-Y.json` b8de1925… |
| 3 | `c1-counter.py --root Y --rev 352e24c6 --freeze 352e24c6 …` (do-nothing at freeze) | **1** | same six bindings false, `carriers_matched 0` (plan's do-nothing claim holds) | `out/c1-F.json` 2d4e8634… |
| 4 | `c1-counter.py --root Z --rev 97513487 --freeze 352e24c6 …` | **0** | `met_target true`, `carriers_matched 4`, no false binding — C1 unaffected by C2's landing | `out/c1-Z.json` 2115b89f… |
| 5 | `c2-mismatch.py --root X --rev af056786 --freeze 352e24c6 --battery` | **1** | `mismatches 9`; battery `failing: [genuine REV is not green, mutation set incomplete: 0 of 11]` — expected, C2 landing absent | `out/c2-X.json` fd1c951f… |
| 6 | `c2-mismatch.py --root Y --rev 3addb6d6 --freeze 352e24c6 --battery` | **0** | `atoms_total 9`, `mismatches 0`, `battery.failing []`, 11/11 single mutations red on exactly their atom, do-nothing (5 paths) red = all nine | `out/c2-Y.json` 21bb4877… |
| 7 | `c2-mismatch.py --root Y --rev 352e24c6 --freeze 352e24c6` (do-nothing at freeze) | **1** | `mismatches 9` (matches plan) | `out/c2-F.json` 32057f6e… |
| 8 | `c2-mismatch.py --root Z --rev 97513487 --freeze 352e24c6 --battery` | **0** | `mismatches 0`, `battery.failing []`, 11/11 ok, do-nothing red = all nine over **12** paths (C1's paths included) — C2 unaffected by C1's landing | `out/c2-Z.json` 90b16031… |
| 9 | `c1-counter.py` / `c2-mismatch.py` run under a git shim logging every `git` argv (`tools/git`, `TRACE_LOG`) for rows 1, 2, 5, 6, 4, 8 | — | read-set traces `trace/*.log` (sha256 in MANIFEST); parsed by `tools/readset.py` → `out/readsets.json` | `out/readsets.json` 16984139… |
| 10 | row-sensitivity sweep, in-process: for each of 148 SOURCES.md rows, (P1) `opened` cell → `2026-10-27`, (P2) trailing space; C1 via `measure(..., rerun=<disabled>)` (bindings only, no REA rerun), C2 via `score(Overlay(...))` | 0 | C1 sensitive rows under P1: **S138, S139 only**; under P2: none. C2 red atoms: **S145 → A6** and **S146 → A7** under P1 and P2; **S147 → A6** and **S148 → A7** under P1 only; other 144 rows: none | `out/rowdep.json` 72452dfb… (`tools/rowdep.py`) |
| 11 | `c1-controls.py … --controls pos` via `run-ctl.sh` (POS arm only) | 0 | `CTL-C1-POS as_expected exit 0`, `kill_rule_fires false`, `failures []` (the counterfactual controls CTL-C1-0..5 were **not run** by this seat) | `ctl/ctl.json` b9284ac0… |
| 12 | `c2-after.py Y` | 0 | `DEV_AFTER=3addb6d6…` | `Y.after.out` (tools/) |

Shared-path check (from `out/readsets.json` and `git diff --name-only FREEZE REV`):

| Set | Members | Note |
|---|---|---|
| W(X) C1 landing writes | PROVINCE.md, corpus/README.md, corpus/SOURCES.md, corpus/evidence/round-49/c1/{v1le,v1be,v2le,v2be}/after.json, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md | `out/W_X.txt` 3ccd8572… |
| W(Y) C2 landing writes | SCORECARD.md, corpus/SOURCES.md, corpus/lessons/round-49.md, corpus/evidence/round-49/c2/{popper,sysexits}.html | `out/W_Y.txt` d73cf7fe… |
| R(C1) content reads (X, Y traces) ∩ W(Y) | **{corpus/SOURCES.md}** | C1 reads whole file; verdict uses rows S138/S139 only (row 10) |
| R(C2) content reads at YREV ∩ W(X) | **{corpus/SOURCES.md}** | verdict uses rows S145–S148 bytes/cells and the ID set (row 10); C1 adds no IDs |
| R(C2) battery do-nothing (FREEZE content, REV names) ∩ W(X) | PROVINCE.md, corpus/README.md, the four c1 after.json, the knowledge entry | **violates the plan sentence**; verdict-neutral (row 8) |
| C1 `frozen_drift` log names (no pathspec) ∩ W(Y) | SCORECARD.md, corpus/lessons/round-49.md, corpus/evidence/round-49/c2/* (names only) | **violates the plan sentence**; filtered by frozen-set membership, verdict-neutral (row 4) |

## Read sets (traced, not assumed)

**C1 (`c1-counter.py`) content reads at REV**: `corpus/SOURCES.md` (whole file, effective rows S138/S139: `c[8]==2026-10-28` and entry in `used-by`), `PROVINCE.md`, `corpus/README.md` (`## Coverage map`), the entry at `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, `corpus/evidence/round-49/c1/{id}/after.json` (absent at FREEZE), the four carrier bytes `corpus/evidence/round-42/c2/fixtures/*.bin` and oracle trees `corpus/evidence/round-44/oracle/**` at FREEZE and REV. **Also read, missing from the plan's enumerated list**: `tools/round-27/xpin-attribute.mjs`, `tools/round-39/gen-squashfs.py`, `tools/round-42/{c1-counter.py,fixtures.json,prior-pins.json,rea-pkg.json}`, `plans/round-49-claims.md`, `tools/round-49/carriers.json`, `tools/round-49/c1-run.sh`, `tools/round-49/c1-counter.py`. **Candidate reads that are absent at the freeze**: `tools/round-49/rea-pkg.json` and `tools/round-49/prior-pins.json` (not in the draft `tools/round-49/`). The counter falls back silently to the round-42 files (`REA_PKG_CANDIDATES`, `PRIOR_PIN_CANDIDATES`). Since `tools/round-49/` is frozen, the fallback is permanent.

**C2 (`c2-mismatch.py`) content reads**: `corpus/SOURCES.md` at REV and at LANE_BASE and at R48_BASE/R48_TIP (all row IDs for the A8 set difference; rows S145/S146 byte-equal to base; S147/S148 cells; search-log section), `corpus/lessons/round-49.md`, `SCORECARD.md`, `corpus/lessons/round-48.md` (LANE_BASE and REV, A1), `corpus/lessons/round-48-verifier-spotcheck.md` (A9), `LOG.md` (LANE_BASE and REV, A3), `.ufo/waves/round-48/r48-w1-results.json` and the `.ufo/waves/round-48/w1/` tree listing (A4), `.ufo/waves/round-48/l1/scores/c{1,2}-final-33f65a91.json` (A5), `corpus/evidence/round-49/c2/{popper,sysexits}.html` (A6, A7), and `tools/round-49/**`, `plans/round-49-claims.md` (freeze check). **Battery-only**: `git diff --name-only FREEZE REV` followed by FREEZE content reads of every changed path.

The plan names S145–S148, the search log, LOG.md and the round-48 receipts for C2. It omits the lesson files, the round-48 `w1` listing, `r48-w1-results.json`, and the full ID-set read that A8 performs.

## Findings (ordered by weight)

**F1 — separability holds on verdict (high confidence, measured).** Rows 1–8. Neither landing changes the other claim's verdict: C1 0 on X and on Z; C2 0 on Y and on Z; C1 1 on Y; C2 1 on X. Every cross-tree C1 run reports `frozen_path_changed []`, and every C2 run reports no freeze-check reason.

**F2 — the only shared content path is `corpus/SOURCES.md`, and the verdict-sensitive rows are disjoint (high, measured).** Row 10. C1 is sensitive to S138/S139 only, C2 to S145–S148 only. The rest of the 148 rows are inert to both counters under both perturbations. The plan sentence "C1 reads only rows S138/S139, C2 reads only rows S145–S148 and the search log and the id set" is correct for verdict-sensitivity; the ID set itself (A8) is read by C2 over all rows, which C1 does not change (C1 adds no IDs).

**F3 — C2 battery's do-nothing overlay reads C1's landing paths (medium, violates plan sentence; verdict-neutral).** `c2-mismatch.py` `battery()`: `p = r._run('diff', '--name-only', freeze, rev)` then `r.show(freeze, x)` for every changed path. At X this reads `PROVINCE.md`, `corpus/README.md`, the four c1 after.json and the knowledge entry at FREEZE (see `trace/c2-X.log`, FREEZE group). At Z it restores 12 paths (row 8). Verdict-neutral because the atoms that go red are C2 atoms, but the plan says "neither counter reads a path the other's landing writes, except `corpus/SOURCES.md`". Either restrict the do-nothing set to C2's own landing paths, or amend the sentence to say the do-nothing overlay enumerates every path changed since FREEZE. Decide before freeze.

**F4 — C1 `frozen_drift` names C2's landing paths (medium, violates plan sentence; verdict-neutral).** `c1-counter.py` `frozen_drift()` runs `git log -m --diff-merges=first-parent --name-status FREEZE..REV` with no pathspec (see `trace/c1-X.log`, op `log 352e24c6..af056786 ''`). It names every path in the range and filters to frozen membership. Verdict-neutral (row 4). Option: add the frozen pathspec, as C2's `freeze_check` already does (`git log -- tools/round-49 plans/round-49-claims.md`), and keep the blob backstop. This changes the counter, so it is a pre-freeze fix only.

**F5 — C1 has silent candidate fallbacks to round-42 pins (low, plan omission).** `tools/round-49/rea-pkg.json` and `tools/round-49/prior-pins.json` are absent from the draft (`out/readsets.json`, FREEZE group, shows the reads returning None). The fallback to `tools/round-42/rea-pkg.json` and `tools/round-42/prior-pins.json` is deliberate in the code (`REA_PKG_CANDIDATES`), but the plan does not say so, and the frozen directory forbids adding the round-49 files later. Either add them to the freeze with their intended bytes, or state the fallback in the plan's frozen-paths list.

**F6 — C2 read set is wider than the plan's enumeration (low, plan omission).** See the C2 read-set paragraph above. The verdict-relevant additions are the full ID set in A8 and LOG.md/lesson/w1-tree reads. None touches C1's landing.

**F7 — X is a POS fixture, so the landing text must replace the POS headline (low, for L1).** The POS plant writes `POS control fixture — four real REA 6.5.0 extract-firmware receipts … not the after-side data run` into the PROVINCE and README rows. The real landing must carry the measured headline from the data run, not this string. Separately, `R49C1Doc/block-c-readme-coverage-map-row.md` is labelled `SquashFS v1/v2 through REA (round 44)`. No counter reads that label (C1 checks the `squashfs_v1`/`squashfs_v2` tokens, the entry stem and the frontier note), so it does not break the bindings, but it is a round-44 label on a round-49 row.

**F8 — control coverage of this seat is partial (scope note).** Only the POS arm (CTL-C1-POS) was run here (row 11). The counterfactual C1 controls CTL-C1-0..5 and the C2 do-nothing at freeze on the freeze tree were not run by this seat, except the equivalent do-nothing runs in rows 3 and 7.

## Non-separability caveats, stated

- The rowdep sweep (row 10) used `rerun=<disabled>` for C1 (no REA rerun). It measures bindings only. Carrier matching was not re-measured inside the sweep; it was measured separately in rows 1, 2, 4.
- Both clones built at the same dev-freeze hash `352e24c6…` because `mkclone.sh` is deterministic on the same tree. Each clone's HEAD was confirmed (`git log` in X and Y) before scoring.
- The trace shim only logs `git` argv; it does not catch Python-level file reads. The counters read the lane only through `git` (`show`, `rev-parse`, `ls-tree`, `log`, `diff`, `cat-file`); their non-git reads are the carrier/REA scratch files under `--work`, plus the counter's own source file and `pkg65` package on disk.

## Tools and installs

No tool was installed or upgraded. The REA 6.5.0 package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `unblob` and `sasquatch` at `/home/vgpnk/.local/bin` and `unsquashfs` at `/usr/bin` were used as found. `disk-guard.sh status` was run before the heavy pass (no action needed). No pacman, no fleet-repo write, no commit or stage in the lane.

## Verification to run after the freeze

- `c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 <rea 6.5.0> --work <scratch> --json-out <out>`: expect exit 0, `carriers_matched 4`.
- `c2-mismatch.py --root <LANE> --rev <REV> --freeze <FREEZE> --battery`: expect exit 0, `mismatches 0`, `battery.failing []`.
- Do not rerun `c1-run.sh --data-run` from a seat (L1 only).

## Artifacts

- `.ufo/waves/round-49/w1/ConnSeparability/out/` — `c1-{X,Y,F,Z}.json`, `c2-{X,Y,F,Z}.json`, `*.exit`, `*.stdout`, `*.stderr`, `readsets.json`, `rowdep.json`, `W_X.txt`, `W_Y.txt`, `revs.txt`, `Z.cherry`
- `.ufo/waves/round-49/w1/ConnSeparability/trace/` — eight git-argv traces
- `.ufo/waves/round-49/w1/ConnSeparability/tools/` — `score.sh`, `readset.py`, `rowdep.py`, `git` (shim), mkclone/after/POS logs
- `.ufo/waves/round-49/w1/ConnSeparability/ctl/` — `ctl.json`, `summary.json`, `POS-after-v1le.json`
- `.ufo/waves/round-49/w1/ConnSeparability/MANIFEST.sha256` — 58 files
