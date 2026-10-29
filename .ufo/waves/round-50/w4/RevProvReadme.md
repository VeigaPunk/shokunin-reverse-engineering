# RevProvReadme — round-50 attempt-2 wave-4 (falsify) seat report

Seat: RevProvReadme. Scope: the landed `PROVINCE.md` `## Round-50 measured, not promoted (R50-C1 honest stop)` section + round-50 frontier note, and `corpus/README.md` coverage-map row 106, knowledge row 228, frontier note (line 300). Lane tip reviewed `c67b741e8f6bd8d64adbdb15e059d47fde004c77`; the two later commits (`a3615f70`, `db61a907`) touch only wave orchestration files — `git diff c67b741e..HEAD -- PROVINCE.md corpus/README.md corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` is empty, so the review is valid at both revs.

## Verdict

**PASS WITH FINDINGS.** Every scored number in the two sections traces to a committed receipt, every cited path resolves, the frontier statements match the entry's Still-Frontier list, the supersession wording is accurate and matches the round-49 precedent, the placement matches the round-40/44 precedent, and there is no sibling-ground bleed. One evidence sentence in the PROVINCE section overclaims against its own cited receipt (Finding 1, medium); two low items (Findings 2–3). The measured-not-promoted record itself — 2/4, gap-rule miss, Frontier holding — survives the attack.

## Findings

### F1 (medium) — "the counter's own REA rerun reproduced every receipt's projection" is contradicted by the cited receipt

Three landed documents state the rerun reproduced all projections:

- `PROVINCE.md:442`: "the counter's own REA rerun reproduced every receipt's projection"
- `SCORECARD.md:3796`: "the counter's rerun reproduced every projection"
- `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md:52`: "the counter's own REA rerun reproduced the projection on all four carriers"

The receipt they cite, `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`, says otherwise for g7581:

- `failing` = `["g7581:gaps_ok", "g7581:projection_ok", "g7582:gaps_ok"]`
- `carriers.g7581.projection_ok` = `false`; `projection_error.error.code` = `execution_failure` — `ENOENT: no such file or directory, readlink '…/rerun-g7581/…/usr/www.myfritz/avme/cgi-bin/luacgi'` — with `replayed.attempts` = 1 (the counter retries only `provider_timeout`, `tools/round-50/c1-counter.py:2066-2076`).

The rerun reproduced **3 of 4** projections (g7582, c6490, c6430: `projection_ok` true, `projection_diff []`). The miss verdict is unaffected — g7581 fails `gaps_ok` deterministically and the projection crash is a single-attempt runtime flake on one symlink, not a projection mismatch — but the sentence as written is false against its own receipt, in the exact document whose purpose is the honest record. Suggested repair: "reproduced every projection where the rerun completed; the g7581 rerun crashed once with a readlink ENOENT (`execution_failure`), recorded as `g7581:projection_ok` in the same receipt". Attacked: the claim does not survive; the L1 should amend or disclose.

### F2 (low, entry-adjacent) — "its 636 `unpublished-entry` gaps name no `dev/*` path" is literally false

`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md:52` (in the sentence supporting the twelve-no-disposition claim): two of g7581's 636 `unpublished-entry` gaps **do** name dev paths — `firmware.bin_extract/dev/kdsld_misc` and `firmware.bin_extract/dev/new_led` (verified from the committed envelope; both are symlinks in `tools/round-50/oracle/g7581.nonregular.tsv`, a kind the frozen rule does admit as `unpublished-entry`). The load-bearing assertion — the twelve `char-device` entries (`dev/pts/0-7`, `dev/tiatm`, `dev/ttyp0-2`) carry no gap and no removal — holds and is what PROVINCE/README actually state ("no disposition for the other twelve"). Out of this seat's two-file scope; recorded for the L1's entry errata.

### F3 (low) — "generalised from the Cable-carrier class" is an unstated inference

`corpus/README.md:300` says "the rule was generalised from the Cable-carrier class". The entry (`:52`) says only "generalised at the freeze from one carrier class"; `plans/round-50-claims.md` names no class. The inference is solid (the frozen rule's sole silent allowance `247:0` is exactly the single char-device each Cable carrier carries) but the README note asserts it as fact. Cosmetic; no action required beyond awareness.

## Attacked and held (verification table)

| # | Claim checked | Evidence / command | Exit | Result |
|---|---|---|---|---|
| 1 | 2 of 4 carriers, exit 1, `frozen_path_changed []`, freeze `435d41fd` | `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` → `carriers_matched 2`, `target 4`, `exit_code 1`, `frozen_path_changed []`, `freeze 435d41fd…` | 0 | HELD |
| 2 | g7581/g7582 oracle tables carry 13 `char-device` each; Cable carriers 1 | `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/{g7581,g7582,c6490,c6430}.nonregular.tsv` → 13/13/1/1 | 0 | HELD |
| 3 | Frozen rule: `char-device` required, one silent allowance `247:0`; twelve undisposed | `tools/round-50/gap-rule.json` → `required.char-device true`, `removed.silent.char-device ["247:0"]`; 13−1=12 | 0 | HELD |
| 4 | 4 556 / 4 564 / 4 709 / 3 955 oracle regular files, published == oracle on all four | counter receipt `oracle_files`/`published_files` per carrier; entry results table lines 41–44 | 0 | HELD |
| 5 | 12.7 s run duration (g7581), 1 attempt each | `corpus/evidence/round-50/c1/g7581/run.json` `duration_ms 12687`, `rea_attempts 1` (g7582 21874, c6490 20282, c6430 8266 — all 1 attempt) | 0 | HELD |
| 6 | Toolchain pins REA 6.5.0 / unblob 26.6.4 / sasquatch 4.5.1 | counter receipt `rerun_toolchain` → `rea.version 6.5.0`, `unblob.version 26.6.4`, `sasquatch "unsquashfs version 4.5.1"` | 0 | HELD |
| 7 | Every cited path resolves | entry `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` ✓; `corpus/evidence/round-50/c1/` ✓; `tools/round-50/c1-counter.py` ✓; `tools/round-50/gap-rule.json` ✓; `tools/round-50/fetch-vendor.py` ✓; `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` ✓ | 0 | HELD |
| 8 | Data-receipt digests bind to the counter receipt | `sha256sum corpus/evidence/round-50/c1/*/after.json` == receipt `evidence_digests` (30db72bd…, 2c21f264…, ff481957…, f250f315…) | 0 | HELD |
| 9 | POS red PRE-data; kill rule silent | `.ufo/waves/round-50/controls-attempt2/summary.json` → `CTL-C1-POS verdict "misbehaved" (expected exit 0, got 1)`; `CTL-C1-4 as_expected` (2 matched, exit 1) | 0 | HELD |
| 10 | Frontier statements match the entry's Still-Frontier list | entry `## Still Frontier` (line 66): LE-AVM rootfs ~13k under 120 s, AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4 Broadcom. README note = that list + `LE AVM members (hsqs)` (the subject class, correctly kept Frontier after a miss). PROVINCE note lists the AVM-scoped subset and says so ("the LE-AVM clause … is unchanged by this round") | 0 | HELD |
| 11 | Supersession wording accurate | README note: "adds the round-50 measurement to the LE-AVM clause of the round-49 note and supersedes nothing else" — accurate (no other status changes); same shape as the round-49 note's "and nothing else" (`PROVINCE.md:438`) | 0 | HELD |
| 12 | Placement matches the round-40/44 precedent | `## Round-50 measured, not promoted (R50-C1 honest stop)` is the last section of `PROVINCE.md` (lines 440–448 of 448), same heading/table/dated-frontier-note shape as `## Round-44 measured, not promoted` (line 424); README frontier note appended at file end (line 300 of 300), after the R29 correction, matching prior dated-note placement | 0 | HELD |
| 13 | No sibling-ground bleed | landing commit `0f0eee3b` diffs of `PROVINCE.md` (+10) and `corpus/README.md` (+4) are purely SquashFS/firmware content; no runtime-debug arbitration statement anywhere in the round-50 additions | 0 | HELD |

Full command/exit/stdout-sha256/UTC receipts: `.ufo/waves/round-50/w4/RevProvReadme/receipts.json` (11 receipts, all exit 0 except none — the failed first attempt of the dev-gaps check was replaced by a corrected receipt).

## Residual risk and verification gaps

- The C1 counter was not re-run (REA is L1-only); the F1 projection failure is read from the committed receipt, which is the authoritative scoring artifact for the landed prose.
- The "12.7 s" figure is a single wall-clock observation from the committed `run.json`; host load at data-run time is unstated, but the entry presents it only as an observation, so no overclaim.
- `corpus/SOURCES.md` rows S243/S244/S245/S249 and the search-log/registry counts are another seat's scope; not re-opened here beyond confirming the four S-ids in the README knowledge row match the entry's `source:` rows.
- No tools were installed or upgraded this seat (read-only review; nothing needed).

Report path: `.ufo/waves/round-50/w4/RevProvReadme.md`. Scratch `/fast/scratch/hyaku/kaidoku-r50/w4-RevProvReadme` removed after receipts were copied.
