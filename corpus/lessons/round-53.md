# Round 53 — the fixture-level reader census closes the ddwrt executability debt; L1-inline on a new Windows host

Lane kaidoku, round 53, fresh-start round, attempt 1 on the new Windows host
(2026-10-31). Round base `6697518f0ad8e8399567ae4c9cd0207fc7c04d8b`; the inherited
declaration and dispatch (`4cb12b41368c83ac6e04a0ae44788622dd26c79e`,
`5c25d9cc45f083daf031f437fa291b3a67ce7247`) were authored by the prior L1 on the
dead Linux host; the r53-w1 wave never executed (no seat dirs, no results file).
This session continues the same round on this host: no REA, no vendor fetch, both
declared claims offline over committed bytes, all work L1-inline.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S253 | https://github.com/onekey-sec/sasquatch/tree/b34aa5ef67068a2137ac04e2272915bd45388260 — cloned read-only into round scratch 2026-10-31 (HEAD `b34aa5ef67068a2137ac04e2272915bd45388260`); snapshot bytes and sha256s: `.ufo/waves/round-53/l1/s253/` (USAGE `23193399…`, control `89ff4a11…`, README `ce4b10a9…`) | `debian/control:15` Description: "Tool to extract vendor specific SquashFS images" (8 words) | admit, tier A code (the project's own packaging description), mined: the reader-category fact that a packaged reader for vendor-specific SquashFS exists; `USAGE:246` carries the writer-side `-nopad` text. It is not evidence any reader validates the round-42 fixtures. Used by `corpus/knowledge/2026-10-31-r53-triage-v6-reader-census.md`. |
| census receipts | `scripts/sources-census.sh validate --root <fleet root> <explicit lane dir>` at round start and at the filing tip; start receipt `.ufo/waves/round-53/l1/census-start.txt` (this host; the lane id `kaidoku` maps to a directory that does not exist here, so the explicit lane directory is passed) | 19 standing W04 warnings; exit recorded in the receipt | the census command is host-adapted; W04 stays debt |
| do-nothing controls | `tools/round-53/v5-baseline-witness.py` at the declared base over the frozen round-42 corpus (before any data commit, receipt `.ufo/waves/round-53/l1/scores/c1-before.json`); `tools/round-53/r53-record.py` at the freeze (expected exactly the 8 landing-only atoms red, receipt `.../c2-before.json`) | witness exit 1, `executability_violations 1` naming `dmg_Z3_v3ddwrt_inode_table`, `clean_residue 7` | measured on this host pre-freeze; the numbers equal the inherited declaration's before-arm |

Assimilation: none — the shokuknow register and `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`
are unreachable from this host (no such tree exists); the report carries
`Assimilation: none — shokuknow unreachable`. `considerthese/` does not exist in
this lane; one report line says so.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M53-1 | host-drift (stale-path counting commands) | `.ufo/reports/round-52/kaidoku.md:45-48` and the r51/r52 SCORECARD record their counting commands with `/home/vgpnk/...` absolute roots and `python3`, which do not exist on this host | this round's L1, sweeping the last three rejected closures per the fresh-start rule | the round's counting commands are committed relative to the lane root and run with `python -X utf8 -I -B` (receipt `.ufo/waves/round-53/l1/host-probes/`); the r53 claims file's commands were amended pre-freeze accordingly; commands that cannot be adapted are recorded as historical, never rerun |
| M53-2 | host-drift (cp1252 text decoding) | `.ufo/waves/round-53/l1/host-probes/v5-at-base-cp1252.txt`: the frozen v5 instrument exits 2 (`UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 80044`) reading SKILL.md through `subprocess.run(..., text=True)`; the same command completes under `python -X utf8` (`v5-at-base-utf8.txt`, exit 0, 126 envelopes) | this round's L1 | the v6 port passes `encoding='utf-8'` on every subprocess and file read; the frozen v5 bytes stay untouched and refuse honestly on this host; recorded in PROVINCE's dated host-migration note and the knowledge entry |
| M53-3 | landing/checkout (NTFS reserved name) | `.ufo/waves/round-53/l1/host-probes/ntfs-aux-checkout.txt`: full `git clone` of the lane fails checkout — `error: invalid path '.ufo/waves/arc3-loop1-round3/claims/c1/EX-08/aux/CarrierB.abi.json'` — the tracked `EX-08/aux/` directory (50 files, the only reserved-name collision in `git ls-tree -r --name-only HEAD`) collides with the Windows device name `aux`; a pathspec checkout excluding it succeeds | this round's L1 | containment by procedure (plumbing-only reads, pathspec checkout in the sandbox); no history rewrite attempted; recorded in PROVINCE's dated host-migration note; the round contract's plumbing-only rule is this measured constraint |
| M53-4 | census-order (source row before its used-by targets) | first round-start census run after writing S253 exited 1: `E11 S253 missing used-by corpus/lessons/round-53.md` (the census checks used-by paths on disk); the receipt is retained in the start receipt's earlier revision | this round's L1 | the lesson file was written before the census-start receipt was taken; fix: a new SOURCES row lands only when every used-by path exists on disk, or the row and its targets land in one commit |

## Claim disposition (filled at the record commits)

C1 (depth, triage table v6 + fixture-level census + executability audit): the
before-arm is the witness receipt above; the after-state is the v6 run at the
landing revision. C2 (calibration, the record oracle): before at the freeze
(mismatches 8), after at the record revision (mismatches 0). Verdicts are recorded
in SCORECARD's round-53 section and LOG; this lesson's header carries the declared
freeze once it exists (see `## Freeze` below).

## Freeze

Recorded after the freeze commit lands: FREEZE = (this line is completed in the
same commit that creates `.ufo/waves/round-53/l1/FREEZE`; the single-line rule of
QUALITY 88 applies from that commit).
