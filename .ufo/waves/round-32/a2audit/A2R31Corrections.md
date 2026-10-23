# A2R31Corrections — forensic report

Report time: 2026-10-23T06:51:02Z  
Seat: `A2R31Corrections`  
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

## Axes and behavior

Round-32 claim metadata read: R32-C1 is **coverage** (ARM64X hybrid PE enters PROVINCE Core); R32-C2 is **calibration** (SCORECARD `Capabilities` versus non-author closure). This seat's task is a round-31 documentation/novelty audit; it produces no measurement or verdict for either round-32 claim.

No REA command, carrier binary, counter, gate, build, test, or selftest was run. No production file, claim, predicate, or target was edited, and no lane/fleet Git or jj state was changed. The sandbox clone was created only under this seat's scratch path; searches thereafter were read-only. No tool was installed or updated.

## Findings

1. **Routed defect 1 — row 56/C1 entry scope is too narrow.** At R31 base `c369242f`, the exact hyphen-only `git grep` over `PROVINCE.md`, `SKILL.md`, and `corpus/knowledge` is empty (exit 1). It is not a corpus-wide naming result: the widened content query returns 7 matching lines—3 in base `corpus/README.md`, 3 in the l7-04 knowledge entry, and 1 in l8-01—and the tracked knowledge-path query returns 1 filename, `2026-10-16-l7-04-inspect-sqlite-database.md`. The l7-04 content records a prior `rea-agents@6.5.0` inventory-scope run; that entry says columns were not requested and rows were null. Counts are matching lines per file, not token occurrences. The R31 measurement's narrower result remains: PROVINCE had no Core SQLite row at base; the novelty is Core placement and database-scope reading, not first use or naming. This does not alter the frozen predicate, counter, or target.
2. **Routed defect 2 — lesson C2 summary.** `corpus/lessons/round-31.md:21` says “at most 3 of 23”; the verifier spot-check at `:89` re-computes ceilings 3/23, 5/23, and 7/23. The lesson should append that the best trivial predictor is 7/23.
3. **Routed defect 3 — stale SKILL evidence description.** `SKILL.md:1038` says the 6.7.0 budget drift was “static reading, not run.” The committed `w2/ProbePin670.md` records live probes of exactly `m-over-256mib`, `m-wal-over`, and `m-journal-hot`; only 3 of the 23 rows were run live at 6.7.0.
4. **Routed defect 4 — report erratum.** M31-7 was the **wave-1** `CriticSeparability` seat, not a wave-2 seat (`settle.tsv:26`; `.ufo/waves/round-31/w1/CriticSeparability.md:178-187`). Its attempted fleet `git commit` exited 1 with no commit. The wave prohibited fleet writes, but no tool enforced that restriction; retain “not shown able to fail.” This report carries that erratum. The round-31 lesson itself already names w1.
5. **Routed defect 7 — timestamps.** `7474d26951ea03bb73f59050fa1fb77ee0d3e36b` has committer time `2026-10-23T01:18:47-03:00` (`04:18:47Z`), not `04:18:49Z`. The committed census-start receipt is a 9-line census result ending `exit=0`; it has no timestamp for the lesson's stated 04:21Z. Keep 04:21Z as attributed prose only, not as a time authenticated by that receipt.

## Exact append-only drafts (not applied)

### Append to `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`

```markdown
## Verifier spot-check correction (appended)

- **R31-C1 novelty scope.** The frozen “never run or named” wording and this entry's “the zero count holds only for the hyphenated CLI spelling” are not corpus-wide novelty findings. At base `c369242f`, `PROVINCE.md` still has zero mentions under either spelling and no Core SQLite row, but `corpus/README.md` has three matching content lines and the tracked `corpus/knowledge` tree has one matching filename. The l7-04 entry records one prior live `rea-agents@6.5.0` inventory-scope run (`columns` not requested; `rows:null`). The earlier zero was a literal-hyphen content search limited to `PROVINCE.md`, `SKILL.md`, and `corpus/knowledge`; it omitted README content and pathname matches. R31 adds Core placement and the database-scope reading on 12 published files, not first use or naming. The base-revision counts and commands are retained in `.ufo/waves/round-32/a2audit/A2R31Corrections.md`.
```

### Append to `corpus/lessons/round-31.md`

```markdown
## Verifier spot-check corrections (appended)

- **R31-C1 novelty scope.** The frozen “never run or named” wording was false. At base `c369242f`, the l7-04 entry records one prior live `rea-agents@6.5.0` inventory-scope run; the base README has three matching content lines, and the knowledge tree has one matching filename. The zero from the earlier literal-hyphen content search was limited to its selected paths and did not cover README content or pathname matches. R31's measured move remains the first PROVINCE Core row and database-scope reading, not first use or naming. See `.ufo/waves/round-32/a2audit/A2R31Corrections.md` for the red-before sweep.
- **R31-C2 trivial-predictor ceiling.** The statement at `:21` (“at most 3 of 23”) is incorrect: the verifier re-measurement gives ceilings 3/23, 5/23, and 7/23, so the best trivial predictor is 7/23 (`corpus/lessons/round-31-verifier-spotcheck.md:89`). This is a lesson correction; frozen predictions and claim inputs remain unchanged.
- **Timing.** The committer time of `7474d269` is `2026-10-23T01:18:47-03:00` (`04:18:47Z`), not `04:18:49Z`. The committed `.ufo/waves/round-31/before/sources-census-start.txt` does not carry the stated 04:21Z timestamp; that time is not authenticated by this receipt.
```

M31-7 should be corrected in the next report, not duplicated in the lesson: use the erratum in this report's Finding 4. No correction to routed defects 5 or 6 was drafted in this seat.

### Replace the final sentence of `SKILL.md:1038`

```text
At `rea-agents@6.7.0`, the 256 MiB budget refusal was observed as `resource_constraint`/`file-size` on `m-over-256mib` and `m-wal-over`; `m-journal-hot` was identical to its 6.5.0 envelope outside `meta.duration`. These were the only 3 of 23 rows run live at 6.7.0 (`.ufo/waves/round-31/w2/ProbePin670.md`).
```

### Append QUALITY row 57; leave row 56 intact

```markdown
| 57 | Supersedes row 56 for novelty/absence claims. A claim that a command or surface is “never run”, “never named”, or “0 at base” names the immutable revision, content roots, pathname roots, and spellings searched. A corpus-wide naming sweep searches tracked text under all of `corpus/` (including `corpus/README.md` and `corpus/knowledge`) and tracked pathnames under all of `corpus/` (including knowledge filenames), in addition to any claimed catalogs such as `PROVINCE.md` and `SKILL.md`; it covers CLI kebab-case, tool snake_case, and known aliases. A zero from one spelling, content-only scope, path-only scope, or a subset of roots supports only that bounded negative. A naming search alone does not prove “never run”; that requires searching retained execution records. Round-31 M31-1: at `c369242f`, the narrow hyphen-only content search missed README matches and the l7-04 pathname; the red-before demonstration is retained in `.ufo/waves/round-32/a2audit/A2R31Corrections.md`. | `corpus/lessons/round-31-verifier-spotcheck.md:150`; this report's red-before sweep | 56 |
```

## Red-before sweep: exact commands and observed outputs

The sandbox clone is `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections/repo`; the R31 base resolved to `c369242fee9f559f895e3f7956b1242076c7b1be`, and sandbox `HEAD` resolved to `f382e3b7978e6091a19ca93277c15a75c0016b43`. All listed Git commands used the literal prefix `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections/repo`; no Git routing environment variables were set.

| Exact command suffix | Exit | Observed stdout |
|---|---:|---|
| `rev-parse --verify 'c369242f^{commit}'` | 0 | `c369242fee9f559f895e3f7956b1242076c7b1be` |
| `rev-parse HEAD` | 0 | `f382e3b7978e6091a19ca93277c15a75c0016b43` |
| `grep -c -F -e inspect-sqlite-database c369242f -- PROVINCE.md SKILL.md corpus/knowledge` | 1 | empty |
| `grep -n -E 'inspect[_-]sqlite[_-]database' c369242f -- PROVINCE.md SKILL.md corpus/README.md corpus/knowledge` | 0 | 7 matching source lines at `corpus/README.md:65,68,163`; `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:1,5,9`; and `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:12`. Full source lines are not duplicated here; the base blobs and hashes are listed below. |
| `grep -c -E 'inspect[_-]sqlite[_-]database' c369242f -- PROVINCE.md SKILL.md corpus/README.md corpus/knowledge` | 0 | `c369242f:corpus/README.md:3`<br>`c369242f:corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:3`<br>`c369242f:corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:1` |
| `ls-tree -r --name-only c369242f -- corpus/knowledge | grep -E -c 'inspect[-_]sqlite[-_]database'` | 0 | `1` |
| `ls-tree -r --name-only c369242f -- corpus/knowledge | grep -E 'inspect[-_]sqlite[-_]database'` | 0 | `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` |
| `log -1 --format='%H %cI' 7474d269` | 0 | `7474d26951ea03bb73f59050fa1fb77ee0d3e36b 2026-10-23T01:18:47-03:00` |

The literal pipe (`|`) shown in the two filename command suffixes above separates `git ls-tree` from `grep`. The count query is over tracked knowledge filenames, as routed defect 1 requested; it is not a full `corpus/` pathname census. The broadened content query covered the old roots plus README, and its `-c` result counts matching lines, not total tokens.

Clone creation command: `mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections clone --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections/repo`; exit 0; stdout `Cloning into '/fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections/repo'...` then `done.`

Timestamp command: `date -u +'%Y-%m-%dT%H:%M:%SZ'`; stdout `2026-10-23T06:51:02Z`; exit 0.

## Provenance: file hashes

Each hash command used the literal Git prefix given above, followed by the shown `show <REV>:<path> | sha256sum`; exit 0 for every row; stdout was `<SHA-256>  -`.

| Revision / path | SHA-256 |
|---|---|
| `c369242f:corpus/README.md` | `f93ef20546fca73f1b1e4bbe945a8f140bb6ee4f3a60e5c772ea1756e2659ec5` |
| `c369242f:PROVINCE.md` | `a26910dc65d03d149aba79500025750e57d305f24b9c9c2bec13e482e4d0d4e8` |
| `c369242f:SKILL.md` | `3e5cbfbc44c30fe686abe1177fe501c1c0c9e1ab141be97ed83b787b6401c31a` |
| `c369242f:corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` | `bf4ab45d7a921c276fb432f7c5c587f8623fa94bd2866aec7408cee5410b2e63` |
| `c369242f:corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | `04ed1be1ae202893ff52e5dce523e6274da10e9457cde27a81bd5ab316a3d5a8` |
| `HEAD:corpus/lessons/round-31.md` | `1ddc66dc137aa4861619c2e00e453d5c25d6a0e193d96745987e28aba6987a0a` |
| `HEAD:corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `6e4b4c6b7327ea9e630d971e43a71e46872be172dac0bce17c2dfe12b7b5d3b1` |
| `HEAD:SKILL.md` | `efc57e7601669a06de5d994f1ff64654dfd0069fd88199d4c22dc351f0f5e860` |
| `HEAD:corpus/QUALITY.md` | `1fd860879e15de2ed4360a324e5c6179b25728052d5455bd935ec75e255277bf` |
| `HEAD:corpus/lessons/round-31-verifier-spotcheck.md` | `1008caca1204df4f3a7bdb5c8b571b56b51512c79c654804e11bf0c87b5d2768` |
| `HEAD:.ufo/waves/round-31/w2/ProbePin670.md` | `118049c0c437a1fec11d2fd3739a966eaca005440c26fdffb931bc4200c642e5` |
| `HEAD:.ufo/waves/round-31/w1/CriticSeparability.md` | `064284075bed1644af900d87243173931d24b2f751cec28999451d00cb32625c` |
| `HEAD:.ufo/waves/round-31/settle.tsv` | `9c664fd2ef1df606acefdb7633c0906a9f54f67535d6a2700830218c6193c774` |
| `HEAD:.ufo/waves/round-31/before/sources-census-start.txt` | `9ddc45a36c52316932bb92ff6ce0461cc59eeacb8a7703c3125b6dcac2b8dac8` |

The Git commit-time observation was separate from file hashes: the exact command and stdout are recorded above. Local source locations reopened for findings: verifier spot-check `:27,34-37,89,148-157`; lesson `:6,21,53,65-67`; positive entry `:9,63-70`; `SKILL.md:1038`; QUALITY row 56; probe `:9-16,94-116`; census receipt (9 lines); settlement `:26`; M31-7 incident `:178-187`. No external source was opened.

## Gates, surfaces, limits, artifacts

- **Gate exercised:** red-before documentation sweep at R31 base `c369242f`: old literal-hyphen content query red/empty, expanded content and filename queries identify the omissions above. This is not a lane counter, claim gate, or assertion that all corpus paths were exhaustively enumerated.
- **Touched surfaces:** only this owned report at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2R31Corrections.md` and the private read-only clone `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections/repo`.
- **Out of scope:** no production edits; no change to R31/R32 claims, frozen predicates, counters, targets, QUALITY row 56, or SKILL; no fixes for routed defects 5/6; no cited-runs-gate or counter execution; no held item inspection or retry. No source installation/update.
- **Limits:** this was a bounded historical-text and tracked-name sweep for the R31 routed defect, not an execution-record census or full `corpus/` sweep. The prior run is established from the committed l7-04 record, not by a run performed in this seat. The draft changes remain unapplied.
- **Artifacts:** report path above; sandbox clone at `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2R31Corrections/repo`.
