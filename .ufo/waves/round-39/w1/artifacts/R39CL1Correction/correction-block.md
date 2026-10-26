## Corrections to round 38

Append-only. Two refusals in the round-38 lesson (`## Gate` → `### Assimilation — theme
sasquatch / unblob`, `:80-82` and `:96-97`) rest partly on a provenance ground that does not
hold, and one trend sentence overstates a receipt. The round-38 text is not rewritten; each
refusal is restated below on the grounds that survive, each re-checked on 2026-10-26 by a
non-author seat (`corpus/lessons/round-38-verifier-spotcheck.md` §3 R38-CL1 and §5;
`.ufo/waves/round-39/w1/artifacts/R39CL1Correction/receipts/`). No entry is admitted on the
strength of this block, and no round-38 score changes.

- **Correction — `sasquatch-unblob-compatibility-precondition` (round-38 `:80-82`).**
  Withdrawn: "its only source, `lanes/kaidoku/round7/work/r7-local-measurements.tsv`, exists
  nowhere on this host". The file exists: 1204 B, mtime 2026-10-24 01:07, sha256
  `d8fa9eae176afd371a930acaca94991d841084f3a50929935a7ada0dbd98af6d`, at
  `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round7/work/r7-local-measurements.tsv`. The path
  is relative to the **shokuknow root**; the round-38 `find` was rooted at
  `/home/vgpnk/Projects/shokunin`, a *sibling* of that root, so it could not return the file
  (`find` at the fleet root → no output, exit 0; the same `find` at the shokuknow root → the
  file). The refusal stands on grounds that do hold:
  - *Host state, dated.* The staged row M5 ("sasquatch is absent from PATH and unblob is not
    importable on this host") was true at the 2026-10-24 snapshot and false from
    2026-10-26T01:22:37, when this lane's round 36 installed `~/.local/bin/sasquatch` (382824 B,
    sha256 `ad02d27a…4754`) and `sasquatch-v4be` (436232 B, sha256 `fac88740…14c6`); all three
    binaries now resolve on PATH. The second clause still holds for the host default python
    3.14.8 (`ModuleNotFoundError: No module named 'unblob'`), and `/usr/bin` and `/usr/local/bin`
    hold none of the three.
  - *Load-bearing sentence falsified by lane bytes.* "running them requires the operator's own
    installation … unobtainable from the lane host" is contradicted by
    `corpus/evidence/round-38/c1/K1/after.json` (5 files, all 5 `oracle.tsv` rows matched,
    0 gaps) against `K1/before.json` (0 files, one `missing-extractor-dependency` gap whose
    dependency is `sasquatch-v4be`): the dependency is the only difference between the arms.
  - *Provenance class.* The source is a campaign-local measurement tsv, not a published document,
    and it lives outside the lane in a read-only sibling project; an admitted entry would rest on
    a snapshot whose central row has flipped. That, not unreachability, is the ground.
  - Flip unchanged: an entry re-grounded on lane receipts with a published source.
- **Correction — `sasquatch-unblob-avm-branch` (round-38 `:96-97`).**
  Withdrawn: "S190/S191 are campaign-local `lanes/kaidoku/round9/work/lead2-avm-branch.tsv` rows
  that exist nowhere on this host". The tsv exists: 1177 B, mtime 2026-10-24 07:15, sha256
  `709cddc7aa37b143da9607a8183b48878b33b1c33d015db1463b76d4dea1ea43`, same base and the same
  rooting error as above. Surviving grounds, re-checked:
  - *Pin policy.* S189 cites the unpinned `unblob/main` handler. `main` and tag `26.6.4` are
    byte-identical today (both `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`,
    equal to the installed copy; `diff` empty), so the reference is refused because it can move,
    not because its content disagrees.
  - *Closing premise false.* "a real AVM image still needs a tool this host does not have" — AVM
    publishes the image: `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/`
    → HTTP 200, 592 B, `FRITZ.Box_6490_Cable-07.57.image` 39741440 B.
  - *Branch mechanics reproduce first-hand.* Dev carriers from `tools/round-37/gen-squashfs.py`
    on a fresh scratch tree (`--endian be`: mkfs_time 1700000000, bytes_used 382; `--endian avm`:
    382/382). unblob 26.6.4 runs `sasquatch-v4be -be -no-exit-code -f -d …` on the control and
    publishes 3 files with no gap; on the marker it runs `sasquatch-v4be -no-exit-code -f -d …`
    (no `-be`), exits 1, publishes 0 files, and reports one `extractor-failure` gap with stderr
    "suggests a SquashFS image of a different endianess / read_id_table: failed to read id table
    block / FATAL ERROR: File system corruption detected". The pinned handler carries the branch
    at lines 40-51: `is_avm = header.bytes_used == header.mkfs_time`, then
    `if not is_avm: commands_args.append("-be")`.
  - *Provenance class.* Every row of the staged tsv re-derives from public bytes and the pinned
    handler (its own `fixture_header_bytes_used 307` is K4's `bytes_used`), so the entry adds
    nothing S113/S114 and the round-38 BE entry do not already carry; it is refused as a
    campaign-local snapshot, not as an unfindable file.
  - Flip unchanged: an entry re-grounded on lane receipts with the source repinned to 26.6.4.
- **Correction — trend sentence (R38-CL3).** `.ufo/reports/round-38/kaidoku.md:88` says the
  attempt-1 v3 amendment "would have turned C1 green (v3: 4/4)". It would have made C1
  **carrier-green**: `c1-v3-at-3b960fe5-NOT-THE-RULE.json` reads `carriers_matched 4`,
  `met_target false`, because no Core row exists. Read "carrier-green".
