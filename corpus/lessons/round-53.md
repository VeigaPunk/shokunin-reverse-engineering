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
| M53-5 | controls-scope (the real table was never scored against the real corpus pre-landing) | the v6 after-run at the first landing (exit 1): `MISMATCH dep_A2_squashfs_v4_le: table unclassified vs evaluator clean` — the landed clean row's `partial,readable` census cell cannot carry the evaluator's unknown-census else-branch; the 10 corpus controls score MUTANT tables only, and the selftest's synthetic census has no unknown status | this round's L1 | the landed cell is corrected to `*` under the two precedence rows above (A10, plans file); the instrument stays frozen and re-scores the corrected table; fix rule: pre-landing, score the REAL table against the REAL corpus with the frozen instrument, not only mutants |
| M53-6 | container-shape (two pin mechanisms, one detector) | the R29 gate at the landing audited round-53 as INSTRUMENT_NONE: the gate extracts instrument paths from claim-string values only (tools/round-29/freeze-gate.py strings()/paths), while the round-53 container carries the paths as instruments-map KEYS for the lane oracle's T1 | this round's L1, by running the gate before filing | the verdict is disclosed verbatim in the ledger row and the gate receipt; the container shape is not rewritten after the freeze; rule: a container built for a new reader must be audited by the gates it must agree with before it freezes |

## Claim disposition (filled at the record commits)

C1 (depth, triage table v6 + fixture-level census + executability audit): the
before-arm is the witness receipt above; the after-state is the v6 run at the
landing revision. C2 (calibration, the record oracle): before at the freeze
(mismatches 8), after at the record revision (mismatches 0). Verdicts are recorded
in SCORECARD's round-53 section and LOG; this lesson's header carries the declared
freeze once it exists (see `## Freeze` below).

## Freeze

Recorded 2026-10-31 (append-only correction of the placeholder above): the first
freeze was `94efae0d8722626a71eed6ec1091692b558878d8`; the operative freeze after
the pre-data amendments A8/A9 is `6ead6f1bc8cfe7dd74f39ed3a4880a3ad5c90c04`; the
triage instrument's after-run cites `764e6ed8042160af28caa14f65c7bd358533afae`
(whose claims file carries the A10 binding lines). The chain, each commit's role
and the two FLAGGED findings the freeze gate audited are named in LOG and in
SCORECARD's round-53 section; every after-counter's `--freeze` names one of these
three commits, all descendants of the first.

## Gate — correction (round 54, appended 2026-11-01; the section above stays as filed)

The `## Gate` table above records the admitted row and the receipt rows but no explicit
rejected-candidate rows (routed defect 8 of `corpus/lessons/round-53-verifier-spotcheck.md`;
LEARNING.md's Gate format wants candidates/admitted/rejected/spot-check). The round's
rejected candidates, recorded here from the round's own records (plans `## Fresh-start
compliance`, the report's ruled-out list, amendment A8):

| row | candidate | decision and reason |
|---|---|---|
| R53 reject 1 | re-attempt the AVM LE-SquashFS Frontier→Core claim (the r50/r51/r52 twin) | reject — REA 6.5.0, sasquatch, unblob and vendor fetches are absent on this host (PROVINCE `## Host migration — 2026-10-31`); three consecutive rounds died re-attempting it; the routed findings stay routed, untouched |
| R53 reject 2 | patch the frozen v5 instrument for the host's cp1252 text decoding | reject — the frozen bytes are pinned by the container; the port landed as the new encoding-explicit v6 instrument instead (M53-2) |
| R53 reject 3 | satisfy the first freeze's T2 `claims-commit` self-reference by editing LOG in place | reject — append-only violation (a commit cannot cite its own hash in LOG); the pre-data re-freeze (A8/A9) replaced the clause with `claims-file-cited` instead |

Spot-check: performed post-filing by the non-author closure
(`corpus/lessons/round-53-verifier-spotcheck.md`) — **admitted**; its §7 table re-opened
S253, the AVM reject, the A10 cell correction and the freeze-gate INSTRUMENT_NONE
disclosure, and agreed with all four.
