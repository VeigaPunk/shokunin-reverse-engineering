# CtlC2JunkRow — R31-C2 pre-data control (junk row)

Seat: leaf control. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Target attacked: the frozen R31-C2 counter `tools/round-31/c2-sqlite-refusals.py` at
freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`: can an entry citing S092 plus one
SKILL.md table row per request, built only from `predictions.tsv`, with **no REA
envelopes**, reach `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1` with exit 0?

Answer: **no**. The control reaches every document gate but zero live matches, because
the counter folds the committed-envelope check into `matches`.

## Control built

Sandbox clone (Contract clone command, branch `ctl` at the freeze):

```
/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow/clone
```

- clone base: `35ba7c522dba55f9be27eb161d4254eacaa24330` (branch `ctl`)
- control commit: `39d255b2d836ea71d3bf361bafb873b81e71de72`
  (`control: C2 junk-row (entry cites S092 + SKILL rows, no envelopes)`,
  commit time `1792728683` / `2026-10-23T01:11:23-03:00`)
- no envelope of any request exists at `HEAD`:
  `git -C <clone> ls-tree -r --name-only HEAD -- corpus/evidence/round-31/c2`
  printed exactly `corpus/evidence/round-31/c2/predictions.tsv` (observation).
- only two files changed (`git show --stat HEAD`): `SKILL.md` (+30),
  `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` (+29).

Files created (sha256; seat-dir artifacts unless the path is inside the clone):

| file | sha256 |
|---|---|
| `clone/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` (blob at HEAD: `b9ad574c…`) | `b9ad574c001843da2fd881b745f8f7cb501313ca557e88561ce1e54330f26d14` |
| `clone/SKILL.md` (blob at HEAD: `cb619afe…`, 30 appended lines) | `cb619afe1aa62ffde49c93e6c6aff25dd3ae9b78f39c33db86a8a2b5c53e18b1` |
| `make_control.py` (generator, appended rows verbatim from `predictions.tsv`) | `d43d3bfef7ff6d2a688a922de9fcb9689172089be3895bae678f580d737b28c2` |
| `baseline-35ba.stdout` | `cb6ff04bcb71f78fa354dd54fe1503491d6b7c63ed932a81bae2312df17ad6b0` |
| `baseline-35ba.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| `baseline-35ba.times` | `a1d4adf12ea0fded0127cef5def28cf119e4ff1ad8bddd2e20e58e7cfef35fa5` |
| `control-HEAD.stdout` | `1108c9d27ce2818c8f07e09b72d0cc35a432628ae1b35943da04a23fd158eb1f` |
| `control-HEAD.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| `control-HEAD.times` | `a20e68b6eef0e2f2db998b3f045c651d031e20c99eb4d76725bf1b45f08c0674` |

Entry content: heading, the literal line `cites S092`, a junk line
(`junk row: this entry is a pre-data control, no envelope exists for any request.`)
and the 23 request ids. SKILL.md appendix: a heading naming `inspect-sqlite-database`,
the literal entry path `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`, and 23 rows
`| \`<id>\` | <code or accept> | <message> |` with code and message copied verbatim
from `corpus/evidence/round-31/c2/predictions.tsv` (`{P}` kept literal). No envelope was
fabricated and no file under `corpus/evidence/round-31/c2/envelopes/` exists.

Pin checks before the runs (observations): `tools/round-31/c2-sqlite-refusals.py` sha256
`d23948959835038f4622261b551616863af1e47f3c66a558b8f3b5a232e28223`,
`predictions.tsv` sha256
`acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8`,
`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` version `6.5.0` sha256
`a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` — all equal the
`claims.json` freeze pins. No `PIN … absent or altered` line was printed.

## Counter command 1 — control at HEAD

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow/clone --rev HEAD
```

Run A (plain, under `set -e`): started 2026-10-23T04:11:26Z, counter exited **1**,
stdout sha256 `1108c9d2…`.
Run B (timed wrapper, `set +e`, same counter argv): started 2026-10-23T04:12:29Z,
**exit 1**, ended 2026-10-23T04:12:56Z. Both runs produced byte-identical stdout
(same sha256), i.e. deterministic over 23 live REA runs each.

Full stdout (verbatim; TAB-separated fields):

```
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=1 (ok) skill_ok=1 (ok)
```

stderr: empty (`e3b0c442…`).

## Counter command 2 — comparison run at the freeze commit (no control commit)

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow/clone/tools/round-31/c2-sqlite-refusals.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Run A (plain, before the control commit): started 2026-10-23T04:10:40Z, counter
exited **1**, stdout sha256 `cb6ff04b…`.
Run B (timed wrapper; `TMPDIR` set to the seat's `tmp/`, `set +e`): started
2026-10-23T04:12:03Z, **exit 1**, ended 2026-10-23T04:12:24Z. Byte-identical stdout
to Run A.

Full stdout (verbatim):

```
q-rowlimit-no-table	P2-miss	committed envelope absent
q-columns-no-table	P2-miss	committed envelope absent
q-scope-no-table	P2-miss	committed envelope absent
q-missing-table	P2-miss	committed envelope absent
q-case-table	P2-miss	committed envelope absent
q-view-as-table	P2-miss	committed envelope absent
q-missing-column	P2-miss	committed envelope absent
q-virtual-rows	P2-miss	committed envelope absent
q-shadow-rows	P2-miss	committed envelope absent
q-ok-rows	P2-miss	committed envelope absent
m-missing	P2-miss	committed envelope absent
m-enotdir	P2-miss	committed envelope absent
m-not-sqlite	P2-miss	committed envelope absent
m-bad-pagesize	P2-miss	committed envelope absent
m-journal-hot	P2-miss	committed envelope absent
m-journal-short	P2-miss	committed envelope absent
m-journal-empty	P2-miss	committed envelope absent
m-journal-zero28	P2-miss	committed envelope absent
m-journal-symlink	P2-miss	committed envelope absent
m-db-symlink	P2-miss	committed envelope absent
m-directory	P2-miss	committed envelope absent
m-over-256mib	P2-miss	committed envelope absent
m-wal-over	P2-miss	committed envelope absent
requests=23 matches=0 target=23 entry_ok=0 (entry absent) skill_ok=0 (SKILL names neither the verb nor the entry)
```

stderr: empty (`e3b0c442…`).

## Verdict

```
CONTROL CtlC2JunkRow: met=no score=0/23
```

The control did not meet the frozen target line: `matches=0`, exit 1, at both the
freeze revision and the control commit. No clause let it through.

## Counter clauses exercised (observation + inference)

- **Stopping clause:** `committed_check()` looks up
  `corpus/evidence/round-31/c2/envelopes/<id>.json` via `git show`; absent → every
  request is re-labelled `P2-miss` with reason `committed envelope absent`
  (`tools/round-31/c2-sqlite-refusals.py:232-240`; absence branch at 235-236). This is the clause that carried
  the control's zero.
- **Doc gates are paper gates and both passed:**
  `entry_ok=1` needed only the substring `S092` in the entry, which a 29-line junk
  entry supplied. `skill_ok=1` needed the verb, the entry path, and a `|`-line per id
  containing the id, the code (or `accept`) and the message prefix before `{P}`; copying
  `predictions.tsv` verbatim satisfied all 23. Neither gate requires a run, an envelope
  or any content not already frozen in `predictions.tsv`.
- **Inference (evidence: the printed reason strings plus the code path at
  `c2-sqlite-refusals.py:341-346`): the printed reason is `committed envelope absent`,
  which is assigned only after `judge()` returned the match label. Therefore the live
  half of P2 agreed with all 23 frozen predictions in all four counter runs; the live
  runs cost ~21–27 s for 23 requests (all `npx -y rea-agents@6.5.0` invocations). This
  is a control by-product, **not** claim verification: no envelope is committed, so
  R31-C2 remains unverified under its predicate and kill rule.
- **Reporting opacity (inference):** `matches` conflates the live judgement and the
  committed-envelope check (`matches += verdict == LABEL` after the overwrite), so the
  target line cannot distinguish "live disagrees" from "live agrees but envelope not
  committed". Here the distinction is only visible in the per-row reasons.

## Attacks that ran and their results

- **Junk row passes the doc gates:** yes — `entry_ok=1`, `skill_ok=1` with zero evidence
  (observation). The gates carry no evidence weight; the target is still blocked by
  `matches`.
- **Could the control pass by committing anything cheaper than real envelopes?** No
  path exercised here: an envelope must exist at `ENV_DIR/<id>.json`, be added strictly
  after the freeze commit time, and equal the live envelope in every field but `meta`
  (`committed_check`). The fabricated-envelope shortcut is the separate no-reader
  control, not this one; not tested here.
- **Determinism / replay:** both counter runs of each revision produced byte-identical
  stdout (`cb6ff04b…`, `1108c9d2…`), so a future re-run that differs is a real signal.

## Environment and bounds

- REA was run only through the counter (23 requests per run, 4 runs), never directly on
  a carrier or mutant. Counters were capped with `timeout 900`; no background process
  was left running.
- No package was installed or updated; no tool outside `python3`, `git` and the
  counter's own `npx -y rea-agents@6.5.0` was used.
- Read-only on the lane: nothing was written under
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` except this report; no lane git/jj
  write, no fleet mutation. Lane HEAD read (read-only `rev-parse`) as
  `35ba7c522dba55f9be27eb161d4254eacaa24330`.
- All other artifacts live under
  `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC2JunkRow/` (clone, generator, raw
  stdout/stderr/times files listed with sha256 above).
