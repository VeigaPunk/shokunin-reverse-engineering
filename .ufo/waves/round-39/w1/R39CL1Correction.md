# R39CL1Correction — routed defect R38-CL1 (negative existence claim) + R38-CL3

**Verdict: CONFIRMED.** Both staged sources exist at the shokuknow root; the round-38 "exists nowhere on this host" provenance grounds are false and are withdrawn. Both refusals survive on independently re-checked grounds. Four drafts delivered: the append-only `## Corrections to round 38` block, QUALITY row 82, the `## Mistakes` row, and the R38-CL3 one-line correction.

- Item: routed defect R38-CL1 (`corpus/lessons/round-38-verifier-spotcheck.md` §5, restated in §3) and R38-CL3 (§4).
- Base: `a2f64e1da78afcf8cc39287106604dbcc270844c`. No VCS mutation, no product edit. Read-only access to `/home/vgpnk/Projects/shokuknow`.
- All artifacts under `.ufo/waves/round-39/w1/artifacts/R39CL1Correction/`.

## 1. Both files exist (the routed claim)

```
$ ls -l /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round7/work/r7-local-measurements.tsv \
        /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round9/work/lead2-avm-branch.tsv
-rw-r--r-- 1 vgpnk vgpnk 1204 Oct 24 01:07 .../round7/work/r7-local-measurements.tsv
-rw-r--r-- 1 vgpnk vgpnk 1177 Oct 24 07:15 .../round9/work/lead2-avm-branch.tsv
exit=0

$ sha256sum <both>
d8fa9eae176afd371a930acaca94991d841084f3a50929935a7ada0dbd98af6d  .../r7-local-measurements.tsv
709cddc7aa37b143da9607a8183b48878b33b1c33d015db1463b76d4dea1ea43  .../lead2-avm-branch.tsv
```

First lines: the round-7 tsv is `measure_id / pipeline / … / observation`, 5 rows, and row **M5** reads `sasquatch-unblob-probe  host  not installed  0  0  0  No module named 'unblob'  sasquatch is absent from PATH and unblob is not importable on this host; the compatibility fact stays operator-side`. The round-9 tsv is `item / value`, 16 data rows, carrying `fixture_header_bytes_used 307`, `patched_probe_is_avm_by_unblob_parser True`, `original_be_command sasquatch-v4be -be …`, `avm_branch_command sasquatch-v4be -no-exit-code …`, `avm_branch_result extraction failed: 'suggests a SquashFS image of a different endianess' …`.

The header and the rows quoted here are reproduced in `receipts/staged-sources.txt`.

**Rooting error, reproduced.** `lanes/kaidoku/...` is relative to the shokuknow root `/home/vgpnk/Projects/shokuknow`. The round-38 `find` was rooted at `/home/vgpnk/Projects/shokunin`, a **sibling** of that root:

```
$ find /home/vgpnk/Projects/shokunin -name r7-local-measurements.tsv -o -name lead2-avm-branch.tsv
(no output, exit 0)
$ find /home/vgpnk/Projects/shokuknow -name r7-local-measurements.tsv -o -name lead2-avm-branch.tsv
/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round7/work/r7-local-measurements.tsv
/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round9/work/lead2-avm-branch.tsv
```

So the negative was true *of the swept subtree* and false *of the host*, which is what both the lesson and `w2/R38W2AssimRejects.md` D3 asserted.

## 2. Surviving grounds, re-checked one by one

### Refusal 1 `sasquatch-unblob-compatibility-precondition`

| ground as filed | re-check | holds? |
|---|---|---|
| source "exists nowhere on this host" | file present, 1204 B, sha256 `d8fa9eae…af6d` | **false — withdrawn** |
| staged M5 "sasquatch is absent from PATH and unblob is not importable" | `command -v sasquatch sasquatch-v4be unblob` → all three under `~/.local/bin`, mtime `2026-10-26 01:22:37`, sha256 `ad02d27a…4754` / `fac88740…14c6`, sizes 382824 / 436232 (equal to the lesson). `python3 -V` → 3.14.8; `python3 -c 'import unblob'` → `ModuleNotFoundError`. `/usr/bin` and `/usr/local/bin` hold none of the three | **partly holds** — the PATH clause flipped at the round-36 install (dated), the import clause still holds |
| load-bearing "requires the operator's own installation … unobtainable from the lane host" | `corpus/evidence/round-38/c1/K1/after.json` → 5 files, **5/5 oracle rows matched**, 0 gaps; `K1/before.json` → 0 files, one `missing-extractor-dependency` gap, `dependencies ["sasquatch-v4be"]` | **false — falsified by lane bytes**; the dependency is the only difference between the arms |
| "no published source states the compatibility condition" | README @26.6.4 (sha256 `6544d60f…3716`), line 49: `For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):` — a declared dependency, not a version-pair condition | **holds** in the narrow reading |

Refusal stands: the entry is a date-limited host snapshot whose central row has flipped, sourced from a campaign-local measurement tsv outside the lane. That is a provenance-class ground, not an unreachability ground.

### Refusal 2 `sasquatch-unblob-avm-branch`

| ground as filed | re-check | holds? |
|---|---|---|
| S190/S191 "exist nowhere on this host" | file present, 1177 B, sha256 `709cddc7…ea43` | **false — withdrawn** |
| S189 is the unpinned `unblob/main` handler vs pin 26.6.4 | raw tag and `main` both `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, equal to the installed copy; `diff` empty | **holds as policy** (the ref can move; content identical today) |
| closing premise "a real AVM image still needs a tool this host does not have" | index `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/` → HTTP 200, 592 B, `FRITZ.Box_6490_Cable-07.57.image` 39741440 B | **false** |
| branch mechanics reproduce on lane bytes | re-derived first-hand on dev carriers (§3) | **holds** |

Also checked: the pinned handler carries the branch at lines 40-51 — `case Endian.BIG, 4:` → `V4BE_EXECUTABLE`, `is_avm = header.bytes_used == header.mkfs_time`, `if not is_avm: commands_args.append("-be")`. Refusal stands as a campaign-local snapshot whose every row re-derives from public bytes (its `fixture_header_bytes_used 307` is K4's `bytes_used`).

## 3. Branch ground re-derived this wave (dev carriers, my own bytes)

Built with `tools/round-37/gen-squashfs.py` on a fresh 3-file tree, `--comp gzip`:

| carrier | mkfs_time | bytes_used | is_avm | unblob 26.6.4 child argv (from `unblob.log`) | outcome |
|---|---|---|---|---|---|
| `be.sqsh` (sha256 `45a14a93…e61f`) | 1700000000 | 382 | false | `sasquatch-v4be -be -no-exit-code -f -d …` | 3 files, no gap |
| `avm.sqsh` (sha256 `d37cd95d…7f38`) | 382 | 382 | true | `sasquatch-v4be -no-exit-code -f -d …` | exit 1, 0 files, `ExtractCommandFailedReport`, stderr "suggests a SquashFS image of a different endianess / read_id_table: failed to read id table block / FATAL ERROR: File system corruption detected" |

Direct `sasquatch-v4be` runs cross-check both carriers in both flag states: `-be` → 3 files; no flag → 0 files and the same endianess error. REA `extract-firmware` (CLI, fresh outdirs, `REA_UNBLOB_COMMAND` absolute) agrees: control 3 files / 0 gaps; marker 0 files / 1 `extractor-failure` gap on handler `squashfs_v4_be`.

Limits of this reproduction: the dev carriers are 382-byte gzip singletons (no fragments/xattrs/export table), and the AVM marker is the generator's `mkfs_time = bytes_used` form, not a real 39.7 MB AVM image. It re-derives the *decision* and the *loud failure*, not the full AVM layout. The FS-access-restricted child could not write my shim log (permission denied inside the extract root), so argv comes from `unblob.log`, which records the command unblob actually ran.

## 4. Gate for QUALITY 82, shown able to fail

`neg-existence-check.py` + `claims.jsonl` + `bases.json`; verdicts from `receipts/gate-as-filed.json` (exit **1**, `failed 6`):

| claim | verdict |
|---|---|
| R38-A as filed (`exists nowhere on this host`, find root fleet, path relative to shokuknow) | `host-claim-subtree-root+misrooted` |
| R38-B as filed | `host-claim-subtree-root+misrooted` |
| CTL-C fleet-scoped wording, same argv | `misrooted` |
| CTL-D correctly rooted at the shokuknow base, negative false | `negative-refuted` (returns the tsv) |
| CTL-E true negative under the same root | `ok` (exit-0 case) |
| CTL-F ancestor root `/home/vgpnk/Projects`, negative false | `negative-refuted` |
| CTL-G host claim with ancestor root `/home/vgpnk/Projects`, file present | `host-claim-subtree-root+negative-refuted` |

The as-filed rows fail on **rooting**, not on existence: the fleet-root `find` really is empty, which is exactly why an existence-only check would have passed the false claim. The green control proves the gate is not a blanket reject.

Gate limits: one `-name` per claim (no `-o`, no globs); the base of a cited relative path comes from a declared map (`bases.json`), so the gate enforces consistency, not discovery; the host rule accepts only `/` as a host-wide root and has no path to a declared host-wide root set; it shells out to `find` with a 120 s cap and follows no mount boundaries.

## 5. Drafts (for the L1 to integrate; nothing here is committed)

1. **`correction-block.md`** — the append-only `## Corrections to round 38` block: two refusal restatements (withdrawn sentence + surviving grounds + unchanged flip) and the R38-CL3 line.
2. **`quality-row-82.md`** — row 82 in the rows 79-81 format, plus a short "why 82 and not an existing row" note (56/57 cover spelling and scope but not the root/base axis; 65 covers "unchanged", not "absent").
3. **`mistakes-row.md`** — the `## Mistakes` row: class (negative existence claim rooted at a sibling tree) · evidence (both `find` runs, both files with size/mtime/sha256, lesson lines) · captured-by (`round-38-verifier-spotcheck.md` §3/§5; wave-2 D3 wrote the same command) · fix (QUALITY 82 + gate, with the three verdicts).
4. **`cl3-correction.md`** — the one-line correction: `.ufo/reports/round-38/kaidoku.md:88` "would have turned C1 green" → "carrier-green", with `carriers_matched 4` / `met_target false` from `c1-v3-at-3b960fe5-NOT-THE-RULE.json`.

Row 82 was the next free number (`grep -c '^| 82 |' QUALITY.md` → 0). No `corpus/lessons/round-39.md` exists yet, so the block is drafted for the L1 to append when that lesson is created; the round-38 lesson and the round-38 report are left untouched (criterion 65: measured correction in the next lesson, never a rewrite).

## 6. Out of scope / not done

- No admission, rescore, registry append, or carrier mutation. No REA run on K5/K6; no held-out carrier built. K1-K4 read from committed receipts only, no copies.
- The two refusals are **not** re-litigated beyond their grounds: I do not claim the staged entries should have been admitted, and F3 of `R38W2AssimRejects` (the silently skipped prebuilt-inventory entry) is not part of this item.
- No round-38 score or axis verdict changes. The correction block explicitly says no entry is admitted on its strength.
- Tool installs: none. The `npx -y rea-agents@6.5.0` run was served from the existing cache entry (`node_modules/rea-agents` package mtime `2026-10-26 01:12:52`, unchanged after the run); unblob 26.6.4, sasquatch 4.5.1 and sasquatch-v4be 4.5.1 were used as installed, untouched.
- Observed, not mine: the lane-root `unblob.log` (2652 B, 03:56, sha256 `2d651a4aa6ea3937872a249f7ed3509c4da5a5ca6dfab2d017f8767f69f16299`) is the copy round-38 M38-7 moved out of the fleet root — the digest is M38-7's own cited value, so it is the retained artefact, not a new leak. My unblob runs were confined to scratch directories (now removed), and no `unblob.log` was written to the lane or fleet root by this seat.

## 7. Findings

1. **R38-CL1 confirmed.** The false sentence is not a typo but a sweep-root error, and it recurs in the wave-2 artifact that was supposed to attack the refusals (D3), so the lane had no internal seat left to catch it. The refusals themselves are sound.
2. **The survival rests on different grounds than filed.** Both refusals keep their force from (a) a dated host-state flip plus lane receipts, and (b) a pin-policy/premise failure plus a first-hand reproduction — not from provenance unreachability. The corrected text says so.
3. **The criterion needs two clauses, not one.** Rooting and truth are independent: CTL-D/CTL-F show a correctly rooted sweep can still return the file, and R38-A shows a misrooted sweep can look clean. A one-clause criterion would have passed the false claim.
4. **R38-CL3 confirmed** on the receipt bytes: `carriers_matched 4` with `met_target false` is carrier-green, not claim-green.

## 8. Artifacts

Under `.ufo/waves/round-39/w1/artifacts/R39CL1Correction/`:

- `correction-block.md`, `quality-row-82.md`, `mistakes-row.md`, `cl3-correction.md`
- `neg-existence-check.py`, `claims.jsonl`, `bases.json`
- `receipts/staged-sources.txt` (existence, digests, first lines, both `find` runs)
- `receipts/host-and-upstream.txt` (PATH/import state, K1 before/after arms, pin vs main, README line 49, AVM index, v3 receipt)
- `receipts/branch-repro.txt` (dev carriers, header fields, sasquatch runs, unblob argv, REA envelopes, handler lines)
- `receipts/gate-as-filed.json` (exit 1, 6 of 7 claims failed with named reasons)

Scratch `/fast/scratch/hyaku/kaidoku-r39/R39CL1Correction` removed before close; nothing cited here depends on it.
