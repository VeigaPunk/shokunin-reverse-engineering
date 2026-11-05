# SquashFS triage table v6 — the fixture-level reader census closes the ddwrt executability debt

date: 2026-10-31
round: 53
claim: R53-C1 (depth)
source: S253 — https://github.com/onekey-sec/sasquatch — commit `b34aa5ef67068a2137ac04e2272915bd45388260`, `debian/control` Description "Tool to extract vendor specific SquashFS images" and `USAGE:246` (`-nopad  do not pad filesystem to a multiple of 4K`); snapshot digests `USAGE` sha256 `231933992a3b3ed29b613a4cd803db18c8eb295ce0d8b30085a09fb1110d7806`, `debian/control` sha256 recorded in `.ufo/waves/round-53/l1/s253/control-sha256.txt`
supersedes: the ddwrt routing of rule block 26 (table v5, round 50) for the corpus scopes named below; block 26 stays as history

## Observation (what was already committed)

The round-50 falsify wave measured the reader boundary as FIXTURE-level while the
landed v5 rule is FAMILY-level: the census receipt
`.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt` (UTC
2026-10-29T21:11:09Z, payload sha256 `0a7eb1f7…`, unsquashfs 4.7.5 `-lls` and
7-Zip 26.04 `l -tSquashFS` over the committed round-42 fixture bytes) holds 35
fixture/reader rows: `squashfs_v3` 8/8 readable by both; `squashfs_v3_nonstandard`
8/8 refused by both; `squashfs_v3_broadcom` 7/8 PARTIAL (7-Zip lists,
unsquashfs refuses) and 1/8 readable; `squashfs_v3_ddwrt` 6/7 refused by both and
1/7 readable (`squashfs_v3_le.bin`, digest prefix `0161351caec8` — the same bytes
the plain v3 family reads). Round 50 disclosed this as residue and did not fix it.

## Observation (the before-arm, measured on this host 2026-10-31)

`tools/round-53/v5-baseline-witness.py` replays the landed v5 table at the declared
base `6697518f0ad8e8399567ae4c9cd0207fc7c04d8b` over the frozen round-42 recon
corpus (126 envelopes) and audits the labels against the frozen census
`tools/round-53/reader-census.json` (schema 1; the census is read from git at the
freeze revision, never from a worktree). Measured before-state, exit 1:

- `executability_violations 1` — `dmg_Z3_v3ddwrt_inode_table`, routed
  `legacy-body-failure`/`cross-read-legacy` on bytes whose census status is
  NO-READER. Its carrier `Z3_v3ddwrt_inode_table.bin` (subject sha256 `839c17a83b70…`)
  is a derived body of the ddwrt `squashfs_v3.be.nopad.bin` fixture (census prefix
  `daa8e72d355d`, both readers refuse; recipe "zero bytes 144..203 (v3 inode table
  chain; BE image)" in `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json`).
- `clean_residue 7` — `dep_A2_squashfs_v3.be.nopad` plus the six pad-variant
  `_ddefault` envelopes, labelled `clean` (action `none`, "match files to the
  oracle") on fixtures the census marks NO-READER, so no oracle can exist.
- `pair_mismatches 0` — the v5 table still agrees with the v5 evaluator; the debt
  is executability, not table/evaluator drift.

## Inference and the v6 change

A prescribed action the frozen census says cannot run is a depth defect, and a
`clean` label a census says is unverifiable is the same defect mirrored. Table v6
(rule block 27, `<!-- sqfs-triage-table v6 -->`) therefore adds, above the
`legacy-body-failure` row, `legacy-body-refused` → `preserve-unresolved`: a FAILED
body (`extractor-failure+`, 0 published) whose census status is NO-READER is refused,
never prescribed a cross-read; the `legacy-body-failure` row narrows its census cell
to `partial,readable`; and the census-conditioned `clean` ground routes
`record-unverified` (new label `clean-unverified-fixture` below the v5 family row
`clean-unverified`, which keeps its v5 label byte-stable; the grammar refuses
duplicate labels). The evaluator (`tools/round-53/sqfs-triage-v6.py`) implements the
identical precedence as an independent code path over the same frozen census; the
instrument's audit counts `cross-read-legacy` prescriptions on NO-READER bytes and
`clean` labels on NO-READER bytes, and the claim requires 0/0 at the landing.

Census status resolves per `reader-census.json` `resolution_rule`: fixture digest
prefix match, else derived lineage (`dmg_Z3` is the only lineage row), else family
fallback to the v5 behaviour — so carriers outside the census resolve exactly as
v5 resolved them. A synthetic reader-backed ddwrt FAILED body still routes
`cross-read-legacy`: family-keyed mutants are red on that witness (declared
corpus-vacuous, the corpus holds no reader-backed ddwrt FAILED body).

## Measured after-state and controls

At the landing revision the v6 run exits 0 with `pair_mismatches 0`,
`evaluator_missing 0`, `executability_violations 0`, `clean_residue 0` over the same
126 envelopes; exactly eight labels moved against v5 (dmg_Z3 to
`legacy-body-refused`/`preserve-unresolved`; the seven residue envelopes to
`record-unverified`), everything else byte-stable. Ten committed mutant tables each
flip exactly their declared fixture set and all ten are red on the corpus
(`.ufo/waves/round-53/l1/scores/c1-controls.json`); the selftest is 7 cases
(`--selftest`); the do-nothing control is the witness receipt above.

## What was NOT examined

- No reader was rerun: this round's host (Windows, 2026-10-31) has neither
  unsquashfs nor 7z installed; every census row stays lineage-bound to the
  committed round-50 receipt, `recaptured: false`, and the declared kill rule (a
  recapture contradicting the lineage) never fired. S253 grounds that a reader for
  vendor-specific SquashFS variants exists as a category; it is not evidence that
  any reader validates these fixtures.
- The scored corpus is the frozen round-42 recon set; depth over the scored corpus,
  not held-out generalization (the same disclosed limit as R50-C3).
- The v6 labels are decision-table outputs over envelope bytes; no SquashFS
  superblock was parsed by this round, and no claim is made about the bodies'
  actual damaged/healthy state (`legacy-body-refused` records reader absence, not
  damage — CritTriV6 F5).

## Host note (the instrument port)

The frozen v5 instrument reads `git show` through `subprocess.run(..., text=True)`;
on this Windows host the pipe decodes with the ANSI codepage (cp1252) and dies on
SKILL.md's UTF-8 multibyte bytes: `UnicodeDecodeError: 'charmap' codec can't decode
byte 0x9d in position 80044` → `sqfs-triage-v5: could not evaluate: cannot read
SKILL.md at revision …`, exit 2 (receipt
`.ufo/waves/round-53/l1/host-probes/v5-at-base-cp1252.txt`; the same command under
`python -X utf8` completes). v6 passes `encoding='utf-8'` on every subprocess and
file read; the frozen v5 file stays byte-identical and refuses honestly here.

## Corrections (round 54, appended 2026-11-01 — append-only; everything above stays as filed)

- `verified-at:` 2026-10-31 (round 53) — the observation, before-arm and after-state
  sections were measured on this host against committed bytes, with the receipts the
  sections name (`.ufo/waves/round-53/l1/scores/c1-before.json`, `c1-after.json`,
  `c1-controls.json`, `c1-selftest.json`). The entry was filed without this field
  (routed defect 1 of `corpus/lessons/round-53-verifier-spotcheck.md` §6).
- `recheck:` on-release — the census is lineage-bound to committed round-50 receipt
  bytes and carries `recaptured: false` with a kill rule on a contradicting recapture;
  a recheck re-runs the frozen `tools/round-53/v5-baseline-witness.py` and
  `tools/round-53/sqfs-triage-v6.py` at their pinned revisions over the same corpus
  (they refuse on drift), not on a calendar.
- Source-pointer correction (routed defect 2): the `source:` line above cites
  `.ufo/waves/round-53/l1/s253/control-sha256.txt`, which does not exist. The digest
  lives in `.ufo/waves/round-53/l1/s253/digests.txt`, whose control line reads
  `89ff4a11fa260bcd411a7861d0bdac84dd0ec744ff0b3b371acfa3d4318154c4 *.ufo/waves/round-53/l1/s253/control`
  — the same value the `source:` line abbreviates as `89ff4a11…`. The absent path was
  never created; this block is the correction of record.
- Census-row count precision (routed defect 7, the lane-side half): the frozen
  `tools/round-53/reader-census.json` carries **31** fixture rows, 1 derived-lineage
  row and 4 family totals; the "35 rows" figure in the Observation section above is
  the round-50 receipt table's row count
  (`.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`), which is the
  census's declared source. Both counts stand; the JSON is authoritative for the
  instrument.
