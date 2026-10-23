# R31-C1 pre-data control: junk-row (entry citing S096 + a PROVINCE Core row, no envelopes)

CONTROL CtlC1JunkRow: met=no score=0/12

**Attack verdict: fails (as a false-positive attack).** Under the frozen counter command the committed junk entry and junk PROVINCE Core row satisfy both auxiliary doc gates (`entry_ok=1`, `province_ok=1`) but the control passes **0/12** carriers and exits **1**; every carrier is downgraded by the committed-envelope clause. A second, non-frozen invocation of the *same frozen instrument* (`--write-evidence`, a flag present in the script but absent from the frozen counter string and from the frozen target) prints `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)` and exits **0** on the identical junk docs and no committed envelope. That is a false-pass channel in the receipt protocol, not in the frozen invocation; it is named below with the smallest safe correction. No `PIN ... absent or altered` line was printed by any run.

Axes: frozen C1 coverage; evidence/provenance integrity; resistance to keyword-only saturation. This is a control receipt, not collected claim evidence and not a canonical judgment.

## Construction

Sandbox clone, created at `2026-10-23T04:10:15Z`, branch `ctl` at the freeze commit, clean working tree:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone -c advice.detachedHead=false checkout -q -B ctl 35ba7c522dba55f9be27eb161d4254eacaa24330
```

`git rev-parse HEAD` printed `35ba7c522dba55f9be27eb161d4254eacaa24330`; `git status --porcelain` printed nothing.

Exactly two changes, no envelopes:

- created `clone/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` (sha256 `2fcd4c1d1271267f28f34a23369685d69cb17612bd22da13f3ce085068695383`):
  ```text
  cites S096
  junk row: this entry asserts nothing and carries no evidence id
  ```
- appended to `clone/PROVINCE.md` (post-append content sha256 `350346dd4cf49dc43d554a6fd42d3a109fcde5d444563932e3af9df2bc3e6e32`, blob `ad6382d86c87cd756ef1469af8ca33af95a2f8f5`; diff captured in `control.patch`, sha256 `542933f27d7ac4ea81d3cfa40a45555638f63f81811899b039545ad95be79ece`):
  ```text
  ### Round-31 additions to Core
  | `inspect-sqlite-database` | junk | junk | `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` |
  ```

**Observation:** commit `74b56413ff8056f6b436ff13f8bee1730c4dd7a8` (epoch `1792728641` = `2026-10-23T04:10:41Z`), parent `35ba7c522dba55f9be27eb161d4254eacaa24330`; `git diff --stat` shows `PROVINCE.md | 3 +++` and `corpus/knowledge/2026-10-23-r31-sqlite-positive.md | 2 ++`; `git ls-tree -r HEAD -- corpus/evidence/round-31/c1/` lists `carriers.tsv` and six `pypi-*.json` files only — no `envelopes/` path exists at the control commit.

## Run A — same counter at the freeze rev, before the control commit (comparison)

Working directory `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow`; started `2026-10-23T04:10:22Z`, ended `04:10:32Z`.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout, exit code **1**:

```text
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)
```

**Observation:** `P1-fail ... committed envelope absent` is emitted only after `judge()` already returned `P1-pass` (counter L180–183), so the live REA/oracle half matched all 12 carriers at this rev; the failure is entirely the committed-record clause plus the absent doc surface. The frozen tree contains no already-passing doc surface.

## Run B — frozen-command control

Working directory as above; started `2026-10-23T04:10:43Z`, ended `04:10:55Z`.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone --rev HEAD
```

Full stdout, exit code **1**:

```text
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

Frozen target: `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1, exit 0`. **NOT MET.**

**Observation:** the two doc gates accept junk without reservation: `entry_ok` only requires the substring `S096`, and `province_ok` only requires a line beginning `|` containing `inspect-sqlite-database` and the entry path under a heading whose text contains `Core`. Neither reads an evidence id, a table shape, or any claim sentence.

## Run C — strongest counterexample: the instrument's own evidence-writing flag

Working directory as above; started `2026-10-23T04:11:14Z`, ended `04:11:26Z`. Same binary, same `--root`, same `--rev HEAD`, one extra flag:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone --rev HEAD --write-evidence
```

Full stdout, exit code **0**:

```text
proj-341	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-350	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-361	P1-pass	tables=36 indexes=21 views=7 triggers=35 columns=385
proj-370	P1-pass	tables=37 indexes=21 views=7 triggers=36 columns=395
proj-371	P1-pass	tables=38 indexes=21 views=7 triggers=36 columns=396
chinook	P1-pass	tables=11 indexes=11 views=0 triggers=0 columns=64
chinook-autoinc	P1-pass	tables=12 indexes=11 views=0 triggers=0 columns=66
gpkg-curve	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-curvepolygon	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-line-zm	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-multisurface	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=53
gpkg-test-gpkg-nulls	P1-pass	tables=13 indexes=8 views=0 triggers=18 columns=64
carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

**Observation:** on the same junk docs, with **no committed envelope anywhere in the history**, this invocation exits 0 and prints a line whose numeric fields equal the frozen target. The clause that let it through is the write guard at counter L180: `if verdict == LABEL and not write:` — `committed_check` is skipped entirely whenever `--write-evidence` is passed, while `entry_ok`/`province_ok` still pass on junk. The `pass` field silently changes meaning between "live match **and** committed record" and "live match only", under an identical printed label. This property is inherited from round 30 (`tools/round-30/c1-rust-positive.py:242`, same `and not write_evidence` guard); round 30's junk-row control never tested write mode.

**Observation:** the envelopes this run wrote into the clone working tree were copied out before cleanup and are retained under the seat directory (hashes below); the clone working tree was then restored with `git clean -fdq`, leaving `git status --porcelain` empty. Nothing was committed into the clone beyond the control commit `74b56413`.

## Second instrument weakness: `province_ok` matches the substring `Core`

Called the frozen function directly (no file change, no counter run):

```text
### Non-Core provisional           -> (True, 'ok')
### Core-adjacent                  -> (True, 'ok')
### Round-31 additions to Core     -> (True, 'ok')
## Frontier (Core?)                -> (False, "row sits under '## Frontier (Core?)', not a Core heading")
```

**Observation:** `"Core" in heading` accepts a heading that explicitly negates Core (`Non-Core`) or names adjacency (`Core-adjacent`), because the exclusion regex only matches the capitalised words `Frontier|Adjacent|exclusion`. This control's own heading is a legitimate Core heading, so it does not affect this verdict; it is a placement-gate false positive available to a less honest author.

## Third point: the frozen target line is not reproducible as a literal string

Every counter run, in both modes, prints `entry_ok=%d (%s) province_ok=%d (%s)`. The frozen target (`claims.json:16`) is `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1, exit 0`, with no parentheticals. A verifier that requires byte equality with the frozen line accepts no run at all; the binding signal is the four numeric fields plus the exit code. Round 30's counter has the identical format (`tools/round-30/c1-rust-positive.py:265`), so this is lane convention, not a round-31 regression — but the L1 receipt must compare fields, not the literal line.

## Impacted axes

- **Coverage (C1):** cannot be falsely saturated by junk docs under the frozen argv — the committed-envelope clause holds. It *can* be falsely reported if a write-mode run is quoted, so the receipt must pin the argv.
- **Evidence/provenance integrity:** the `strip_meta` full-envelope comparison (the M30-3 repair) is exercised and holds; the live half already passed 12/12 at both revs, so this control adds no claim data and no provenance.
- **Doc gates:** `entry_ok` and `province_ok` are syntactic and proved junk-satisfiable here; they must never be promoted to standalone success.

## Smallest safe correction

Frozen instruments are not amended this wave (`claims.json` freeze rule). For the receipt:

1. Quote the C1 counter exactly as frozen (`claims.json:15`), with **no** `--write-evidence`; never quote Run C's line as the claim result, and compare fields + exit code rather than the literal target string.

For the next round, routed as a defect (not applied here):

2. Make write-mode output unquotable as a pass: in the `if write:` branch, before the final print, emit `WRITE-EVIDENCE (unsealed)` and print a line that cannot equal the frozen target, e.g. `WROTE carriers=12 target=12 committed=0`; keep exit 0 for the write itself. Two changed print statements, no judgement logic touched.
3. Tighten `province_ok` to a token match, `re.search(r"(?<![\w-])Core(?![\w-])", heading)` plus a `Non-Core` exclusion, so `### Non-Core provisional` and `### Core-adjacent` stop passing.

## Retained artifacts and SHA-256

All under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/`, produced with `sha256sum` at `2026-10-23T04:11Z`.

| Path | SHA-256 |
|---|---|
| `prefreeze.stdout` (Run A full stdout) | `57469c31b8eea4faf65335ea8b319d290cc135d44f2b4454297e1272d4084fb2` |
| `prefreeze.meta` | `7cb2f7effaf35042d2bfd0a1af7db795c5c4a0752828b03def220b87dc771d29` |
| `control.stdout` (Run B full stdout) | `8de8a230e504b9ad0308658d5c590e1bd77e8d0336edfef93df135d4f808fc09` |
| `control.meta` | `faa64017c3f6a780247ab9c8f4107ecc7dcf15f2a7149ad39e03ba9b088f7be6` |
| `control.patch` (PROVINCE diff) | `542933f27d7ac4ea81d3cfa40a45555638f63f81811899b039545ad95be79ece` |
| `writebypass.stdout` (Run C full stdout) | `4360d9e51cf1e4d5e57718efad485d618c1339ca0d347e4b8978a242801aad05` |
| `writebypass.meta` | `cd813b6c3ec744530c6bed3120a169a8357887c5945dba87ada7fcf2df08bb92` |
| `writebypass.status` (clone dirt after Run C) | `8da0de71c1c87e4179969bbe1b79e535556a3d09819ef8e7589d0dc7c66524e1` |
| `writebypass.sha256` (envelope hashes) | `2b6f7505dd70198bf83d1ce538d73cd0edfcb6dadfbfbfdfc8c66604b847f878` |
| `writebypass-runs.tsv` (Run C runs table) | `59b4a724140d9e6354b4803bad70ecc0067393302a3ed6e0d1396e3d8f085231` |
| `instruments.sha256` (clone counter/oracle/claims/carriers hashes) | `b95e47f0357c53b15c1a147a75e751c399aa3b29f95a3fbe6d8e7d9ff972474e` |
| `writebypass-envelopes/proj-341.json` | `6fefe5f7acf8e2d6d0be9cdc9c3567890d3e96b5ea6a0ba31873d42273d8f33f` |
| `writebypass-envelopes/proj-350.json` | `9aad71bd63edabba910f11b236433337146b815cf36e7be69de3597750a27fe1` |
| `writebypass-envelopes/proj-361.json` | `b5f3c90226f83d55b4712b7975b319e1c297767b3a503ed63f9ed3f8d5a92170` |
| `writebypass-envelopes/proj-370.json` | `c8a44303525820bf522677d3fe9f9dcaab18a45561833a2575a694a72994dbd0` |
| `writebypass-envelopes/proj-371.json` | `f36cbbd37c54bde5dfc37bb759f32736bda6d210b860561727b1c1e3c1045fc9` |
| `writebypass-envelopes/chinook.json` | `5a4e5a1455ac2180003bbcd0959fee83383e1dba328e39ef4cc3e0d536ecb0e5` |
| `writebypass-envelopes/chinook-autoinc.json` | `cb6aeb1b097bcd32aa7d88699ca574971aedbdfaf528d8c61acef566c9bdbd54` |
| `writebypass-envelopes/gpkg-curve.json` | `342840b4d385c39e576bbe17a710865ab79503e7bf24c2bd3fbd73fdbf1d212e` |
| `writebypass-envelopes/gpkg-curvepolygon.json` | `7934d0ef3525592f3af4223048e7969851f3c5a982dd8f0ec66f104f85926173` |
| `writebypass-envelopes/gpkg-line-zm.json` | `28fe113882a0f5e100cd0ce50d1e36924871c99f14d1cd5055f3e35c77665362` |
| `writebypass-envelopes/gpkg-multisurface.json` | `e8d403c6ed1855eb69a3e539d136fddbea38da39d899ab2a1bc3154a29c8beae` |
| `writebypass-envelopes/gpkg-test-gpkg-nulls.json` | `012d4f418fad2703c606c0fda7b47118e88aa0d2d52ab496f14f571d636f4b3c` |

Clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone`, branch `ctl`, control commit `74b56413ff8056f6b436ff13f8bee1730c4dd7a8`, working tree clean at exit.

## Opened sources

All accessed 2026-10-23 by ordinary local file reads; hashes are of the complete file bytes read. Each quote is at most 25 contiguous words.

| URL | SHA-256 | Located quote |
|---|---|---|
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | L180: `if verdict == LABEL and not write:` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/.ufo/waves/round-31/claims.json` | `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` | L16: `"target": "carriers=12 pass=12 target=12 entry_ok=1 province_ok=1, exit 0",` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/corpus/evidence/round-31/c1/carriers.tsv` | `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211` | L1: `id	path	sha256	bytes	source_row	container	container_sha256	member` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/PROVINCE.md` (HEAD content) | `350346dd4cf49dc43d554a6fd42d3a109fcde5d444563932e3af9df2bc3e6e32` | L342: `### Round-31 additions to Core` |
| `file:///fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1JunkRow/clone/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `2fcd4c1d1271267f28f34a23369685d69cb17612bd22da13f3ce085068695383` | L1: `cites S096` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c1-sqlite-positive.py` | `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` | L249: `ap.add_argument("--write-evidence", action="store_true")` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | L242: `if verdict == PASS_LABEL and not write_evidence:` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC1JunkRow.md` | `f33fb54127dbf5a956649a31cb918eccbe859864af91ca0acd01f8dec8ff6279` | L128: `the mandatory post-freeze committed-envelope clause prevented false saturation` |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | L2: `name: godspeed` |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | L1: `# Tooling directive — operator, 2026-10-19 (always on, every agent)` |

Tool installs/updates: none issued by this seat. The counter invoked its prescribed `npx -y rea-agents@6.5.0` CLI (package.json version re-checked 6.5.0 by the counter's PIN clause). No subagent, no extra REA run outside the three counter invocations, no carrier/mutant write, no lane or fleet Git mutation; the only lane file written by this seat is this report. Sibling-seat processes observed in `pgrep` were not touched.
