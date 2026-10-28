# W2C2Mutate — round 49 wave 2: 30 record mutations scored by the frozen R49-C2 counter

## Verdict

At `29883d4ec35a31a8393c4ffb220888c44c0bb022` the frozen counter re-runs green on the landed record (`atoms_total 9`, `mismatches 0`, battery 16/16, do-nothing red x9). **30 of 30 new mutations scored exactly as predicted; no mutation turned an atom red that I did not expect.** But **13 of 30 mutations leave all nine atoms green**, so the counter does not bind those parts of the record. Two of the 13 are counter defects against a plan sentence (M22, M23); one is a gap against the QUALITY row 88 failure clause (M02); the rest are unbound surfaces or disclosed limits. Nothing was patched; every finding is a miss to route.

## Setup and controls (exact)

- Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` was read only (`git show 29883d4…:<path>`, `git ls-tree`, `git rev-parse`). No lane or fleet file was written; no commit, stage or stash in the lane.
- Frozen counter used unchanged: `tools/round-49/c2-mismatch.py` at `29883d4…`; scratch copy sha256 `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` = the FREEZE blob (`git show decc5697…:tools/round-49/c2-mismatch.py | sha256sum`).
- Scratch clone (`git clone -q --shared`, clone-local identity, `rev-parse --show-toplevel` asserted equal) holds one commit per mutation on top of REV. Driver: `mutate.py` (artifact copy at `.ufo/waves/round-49/w2/W2C2Mutate/mutate.py`, sha256 `a9560341afbc09aa1a6389263ee384a2be4e1a61ba26916b58f213597452bd85`). The driver is a scratch fixture writer, not a lane edit.
- Every score: `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B c2-mismatch.py --root <CLONE> --rev <commit> --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --json-out <f>`.

| control | command (rev) | exit | mismatches | red | stdout sha256 (first 16) | verdict |
|---|---|---|---|---|---|---|
| C0 lane REV, read in lane root (`--battery`) | `--root $L --rev 29883d4… --freeze decc5697… --battery` | 0 | 0 | none; battery `failing []`, 16 mutations each red on own atom, do-nothing red x9 | `0cad6d5cfb525227` (full stdout sha `0cad6d5c…f490f86`) | as expected |
| C0' REV in clone | `--root CLONE --rev 29883d4…` | 0 | 0 | none | `5f403b7479a9ee5a` | as expected |
| C1 empty commit on REV | same, rev = empty commit `7412dc41a4` | 0 | 0 | none | `bf1d79c909058322` | as expected |
| CF FREEZE itself | `--rev decc5697…` | 1 | 9 | A1–A9 | `7aa900e1f004d3f1` (full `7aa900e1…2e37f4`) | as expected (`mismatches 9`, exit 1) |

Full stdout sha256 for the other rows: `results.json` (`mut/results.json`, sha256 `4334954ab2bd6ebe8ff72d9d4191820924fc9d9ce92e97ab30898591a8cb94d3`). The `rev` field in the counter's stdout is the clone commit, so these hashes replay only with the same commit bytes; `mutate.py` regenerates the content, not the hashes.

## Findings table (30 mutations; exact scope of each edit)

Expected red set is what I predicted from the counter source before running. All 30 matched. Exit = counter exit code.

| id | edit (file, exact change) | attacks | expected red | exit | mism. | red observed | stdout sha256 (first 16) | verdict |
|---|---|---|---|---|---|---|---|---|
| M01 | `corpus/lessons/round-49.md` A1 `declared=b6f7…` → `decc5697…` | A1 | A1 | 1 | 1 | A1 | f2b0475d67388505 | match |
| M02 | same file, round-49 **header** `Declared freeze \`decc5697…\`` → `\`b6f7ca2a…\`` (a real commit, the stale A8 freeze) | header not an atom | none | **0** | **0** | none | faa658c337e2277b | **UNDETECTED** |
| M03 | A2 `dead=663f30ee…822` → `decc5697…` | A2 | A2 | 1 | 1 | A2 | eedf72a250bca550 | match |
| M04 | A2 `actual=663f30ee…822` → `663f30ee7516942a…` (= dead) | A2 | A2 | 1 | 1 | A2 | 5245504a6a709892 | match |
| M05 | A3 `unnamed=…,7fe11332` → `…,2e785632` | A3 | A3 | 1 | 1 | A3 | d9f8127d7f096b81 | match |
| M06 | A3 `log_33f65a91=3440,3441,3444` → `…3443` | A3 | A3 | 1 | 1 | A3 | 4951a83757ffc661 | match |
| M07 | A4 `missing=…,ScribeReportNumbers` → drop last | A4 | A4 | 1 | 1 | A4 | 42b870c8f57141ce | match |
| M08 | A5 `report_c2=c30628ae` → `d1bb87d8` (raw prefix) | A5 | A5 | 1 | 1 | A5 | e1549e3ee574bcd6 | match |
| M09 | lesson gains a second, empty `## Corrections to round 48` | A1–A7 | A1–A7 | 1 | 7 | A1–A7 | 2e54e6e75f864f67 | match (multi-atom, as designed) |
| M10 | lesson S147 Gate row `it is scientific` → `it is unscientific` (lesson only) | lesson vs registry | none | **0** | **0** | none | 0e24b98fadac6345 | **UNDETECTED** |
| M11 | lesson S147 Gate row pinned sha last digit `…6ec207` → `…6ec208` (lesson only) | lesson vs registry | none | **0** | **0** | none | 27a0ed407c8be37c | **UNDETECTED** |
| M12 | SOURCES S147 anchor, second quote → another true 9-word passage under the same heading (`"A number of biographical features may be identified as"`… , count 9) | registry anchor | none | **0** | **0** | none | 72a7c175ea5d64e9 | **UNDETECTED** (true passage; lesson Gate does not cite it) |
| M13 | SOURCES S147 `opened 2026-10-28` → `2026-10-27` | A6 | A6 | 1 | 1 | A6 | 854acc3c9017d58e | match |
| M14 | SOURCES S147 `scope` cell (column 5) rewritten | none (column unchecked) | none | **0** | **0** | none | b068ef2979517bca | **UNDETECTED** (unchecked column) |
| M15 | SOURCES S148 `used-by` lesson link → `—` | A7 | A7 | 1 | 1 | A7 | 2a8fb891add4397e | match |
| M16 | `corpus/evidence/round-49/c2/freebsd-sysexits.html` comment appended; S149 anchor sha not updated | S149 pin | none | **0** | **0** | none | 21f7251cff1106cb | **UNDETECTED** (S149 sha pin read by no atom) |
| M17 | SOURCES S149 row duplicated | row-id uniqueness | none | **0** | **0** | none | aee23a832e7f3756 | **UNDETECTED** (dup check only for S147/S148) |
| M18 | SOURCES S147 row duplicated | A6 | A6 | 1 | 1 | A6 | 5eb8f0179cabb7e9 | match |
| M19 | SOURCES S145 scope `demarcation of` → `demarcations of` | A6 (S145 byte-identical) | A6 | 1 | 1 | A6 | b3e5cab65d9ff282 | match |
| M20 | SOURCES S149 status `rejected` → `mined` | A8 | A8 | 1 | 1 | A8 | 8b07869a8e2509f0 | match |
| M21 | search log round-49 `Identified 3` → `Identified 300` | A8 (identified asserted) | none | **0** | **0** | none | 7739cf5e9ca624b9 | **UNDETECTED** (disclosed limit) |
| M22 | search log: second round-49 entry with marker `round-49` (hyphen) appended | A8 "exactly one round-49 entry" | none | **0** | **0** | none | 08f99e66e4442da7 | **UNDETECTED — counter defect** (line 514 is a space-only prefix) |
| M23 | search log: second round-48 entry **without** `late entry` appended | A8 "exactly one round-48 entry (marked late entry)" | none | **0** | **0** | none | f5f7bf4dbfccaf95 | **UNDETECTED — counter defect** (lines 516–517 filter before the count) |
| M24 | search log round-49 `rows 146 → 149` → `→ 150` | A8 | A8 | 1 | 1 | A8 | e635bf8d983c93ca | match |
| M25 | SCORECARD A9 `verdict=rejected-harmed` → `verdict=admitted` | A9 | A9 | 1 | 1 | A9 | b5ea9a2976067a5e | match |
| M26 | SCORECARD `## Round 48` `**Declared freeze:**` `b6f7…` → `decc5697…` (base input) | immunity: A1 reads SCORECARD at base | none | **0** | **0** | none | 446f78a4ea5888ce | **immune as designed** |
| M27 | `corpus/lessons/round-48.md` header freeze → `decc5697…` (base input; must be byte-identical at REV) | A1 | A1 | 1 | 1 | A1 | eff69b067cf8152d | match |
| M28 | `LOG.md` line 3440 edited in place (not an append) | A3 (append-only prefix) | A3 | 1 | 1 | A3 | f9ab46422f2f5ef2 | match |
| M29 | `corpus/QUALITY.md` row 88 `Fails when a lesson header and the SCORECARD disagree` → `… agree` | row not read | none | **0** | **0** | none | a4c3dcb0472f139a | **UNDETECTED** (unread surface) |
| M30 | popper snapshot comment appended **and** S147 anchor sha re-pinned to `e63e4135…3347` (lesson's sha not updated) | A6 snapshot binding | none | **0** | **0** | none | 07365d9c61940090 | **UNDETECTED** (consistent snapshot forgery; disclosed only as live-page limit) |

Counts: 17 of 30 turned exactly the expected atom(s) red; 13 of 30 green (listed above). No mutation turned an unexpected atom red. No no-op: `changed_paths` non-empty for all 30 (`results.json`).

## Undetected changes, classified (the 13)

1. **Counter defects against a plan sentence (route as misses; counter frozen).**
   - **M22** (`c2-mismatch.py` line 514: `startswith('- %s %s' % (ROUND_DATE, tag))` with tag `round 49`). The plan says "exactly one round-49 entry". A second entry with the hyphen marker `round-49` is not counted. Exit 0.
   - **M23** (lines 514, 516–517: the round-48 `late entry` filter runs before `len(ent) != 1`). The plan says "exactly one round-48 entry (marked `late entry`)". A second, unmarked round-48 entry is not counted. Exit 0.
2. **Plan-sentence gap for the freeze header (route; QUALITY row 88 condition).**
   - **M02**. QUALITY row 88 says: "Fails when a lesson header and the SCORECARD disagree." The counter reads the freeze header only from `corpus/lessons/round-48.md` (line 292). The round-49 lesson header is never read. Setting it to `b6f7ca2a…` (the stale A8 commit) gives exit 0. The landed header is currently correct (`decc5697…`), so this is a counter gap, not a landed defect.
3. **Record surfaces no atom binds.**
   - **M10, M11, M12**: the lesson's S147 Gate row is not compared to registry anchors or the snapshot. A changed quote, a changed sha, or a re-pointed registry quote all pass when the lesson and registry disagree.
   - **M14**: S147 `scope` (column 5) is unchecked.
   - **M16**: the S149 registry anchor pins `freebsd-sysexits.html` by sha256, but no atom reads S149 or that snapshot. Editing the snapshot passes.
   - **M17**: duplicate-id detection is applied only to S147/S148 (`_snapshot_row`, lines 424 and 428). A duplicate S149 row passes.
   - **M29**: QUALITY row 88 is not read.
4. **Disclosed by the plan but worth stating precisely.**
   - **M21**: `identified` is asserted by the lane and never derived (the plan discloses this).
   - **M30**: a consistent forgery of a committed snapshot (snapshot bytes plus the anchor sha256 changed together) passes. The plan's disclosed limit covers "snapshot vs live page", not "snapshot forged to match its own pin".
5. **Immune by design (confirmed).**
   - **M26**: a round-48 base input edited at REV leaves all nine atoms green (A1 reads SCORECARD at base).
   - **M27** (same class) red only on A1 via the byte-identical clause, as the plan says.

## Calibration

- Predicted expected-red sets for 30/30 mutations matched the counter's output. Reds that I did not predict: none. Greens that I did not predict: none beyond the 13 listed, and each was predicted from the counter's read set before scoring.
- Routed for the L1 (no patch; counter frozen): fix M22/M23 (counter misses), add a round-49 header atom or extend A1 to read the REV lesson header (M02), bind lesson Gate rows to registry anchors (M10–M12), bind S149 and all registry rows to uniqueness and their snapshot pins (M14, M16, M17), read QUALITY row 88 or drop the claim from it (M29), and record the snapshot-forgery limit (M30) beside the live-page limit.

## Restoration / cleanup

- No lane file changed. The scratch clone and copied `rec/` under `/fast/scratch/hyaku/kaidoku-r49/W2C2Mutate/` were copied to `.ufo/waves/round-49/w2/W2C2Mutate/` (`mutate.py`, `c2-mismatch.py`, `results.json`, `run.log`, `mut/` 33 receipts, `rec/` baseline and freeze receipts) and the scratch directory was removed after copying.
- No tool was installed or upgraded; no pacman transaction was run.

## Command receipts

- Baseline REV: `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B c2-mismatch.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 29883d4ec35a31a8393c4ffb220888c44c0bb022 --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --battery --json-out rec/rev-battery.json` → exit 0, stdout sha256 `0cad6d5cfb525227…f490f86`, `atoms_total 9`, `mismatches 0`, `battery.failing []`.
- FREEZE: same command, `--rev decc5697…` → exit 1, `mismatches 9`, stdout sha256 `7aa900e1f004d3f1…2e37f4`.
- Mutations: `python3 -I -B mutate.py` (scratch) → 33 scored commits (C0, C1, CF, M01–M30), `run.log`, `mut/results.json`.
- Times (UTC): baseline 2026-10-28 22:37; mutation run 22:42:32–22:42:49.
