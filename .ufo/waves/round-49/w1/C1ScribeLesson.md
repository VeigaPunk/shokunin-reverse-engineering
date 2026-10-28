# C1ScribeLesson — round 49 wave 1 (pre-freeze) — lesson skeleton and C2 instrument check

Seat: `C1ScribeLesson` (leaf scribe; no subagent dispatch). Lane `kaidoku`, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Drafted 2026-10-28, UTC 21:11–21:16. Installs or updates: none. Lane tree, drafts and fleet repo: read only. Scratch `/fast/scratch/hyaku/kaidoku-r49/C1ScribeLesson` removed after receipts were copied.

## Verdict

**Skeleton drafted** at `.ufo/waves/round-49/w1/C1ScribeLesson/lesson-skeleton.md`, with `<FREEZE>` and `<AFTER>` left for the L1. Every factual claim in it was re-derived from bytes this seat read. Three points need the L1's decision before the freeze:

1. **M49-1 is confirmed and its fix is shown red.** Battery mutation `A1 swap declared/stale` turns only `A1` red at a pre-freeze dev fixture. The battery also reports 9 mismatches at the freeze, as the plan says.
2. **Round-48 items R48-CL2, CL3 and CL5 are not in the round-49 claims and have no written decline.** The round-48 SCORECARD lists them as `planned (round 49)`. CL5 is measured still open: at the freeze the `--battery` flag runs zero of 11 mutants. The skeleton lists them as open. The L1 either adds them to the plan or accepts them as open.
3. **Two wave-1 draft findings are carried as marker row M49-2** (not yet a row): `frozen_tables_valid` is a tautology at `c1-counter.py:1995`, and the provenance control CTL-C1-4 reaches 4/4 under relabel plus re-mint. Both come from peer reports. This seat confirmed the first from source and did not re-run the second.

## Findings

| # | check | command (cwd = scratch clone unless stated) | exit | sha256 / value | result |
|---|---|---|---|---|---|
| 1 | Round-48 lesson freeze line | `sed -n 4p corpus/lessons/round-48.md` | 0 | line 4: `Declared freeze 0f06251bf6a3a6964c715f67243d4df12e854258` ("series A1–A4") | confirms M49-1 evidence |
| 2 | SCORECARD round-48 declared freeze | `grep -n "Declared freeze" SCORECARD.md` | 0 | line 3730 (`## Round 48`): `**Declared freeze:** b6f7ca2a6391964dfdedd477cd560bd42159873a` | confirms M49-1 evidence; `LOG.md:3439` also names b6f7ca2a as final |
| 3 | dev freeze build | `bash .ufo/waves/round-49/draft/mkclone.sh $S/clone` | 0 | `DEV_FREEZE=2020aa0bfcbc01b07e87b0b85953ea01746f9091` | ok (throwaway fixture) |
| 4 | green C2 fixture | `python3 -I -B .ufo/waves/round-49/draft/c2-after.py $S/clone` | not captured (output piped through `tail -3`) | `DEV_AFTER=b6312f0d3b0cba7d25e7be69b460f3f98b8c6ff8` from `git rev-parse HEAD` in the clone | ok; exit code not recorded, the commit hash is ground truth |
| 5 | C2 at freeze, no battery | `python3 -I -B tools/round-49/c2-mismatch.py --root $S/clone --rev 2020aa0b… --freeze 2020aa0b…` | 1 | stdout sha256 `dd4b2072018f7bfae34b0ba2698157214318fbab2c72606847cf441179fc5893`; `mismatches 9`, `atoms_total 9`, every atom `lesson line … absent` | matches plan "at FREEZE 9, exit 1" |
| 6 | C2 battery at green REV | `… --rev b6312f0d… --freeze 2020aa0b… --battery --json-out $S/c2-battery.json` | 0 | stdout = json, sha256 `e4fe1ae516c035f9737bf0f00ba9757b17d6a148f4769a32d99a2931ea7584c9`; `mismatches 0`; `battery.failing []`; 11 mutations, each `red` = its own atom, each `noop []`; `do_nothing_paths 5`, `do_nothing_red` = A1–A9 | matches plan: 11 single mutations + do-nothing; M49-1 mutation `A1 swap declared/stale` red |
| 7 | R48-CL5 at freeze with battery | `… --rev 2020aa0b… --freeze 2020aa0b… --battery` | 1 | stdout sha256 `52425b3415d2fc5fb64b1e8f3513cd1ac84e81423bab0d60c28d2a2b98479db5`; `battery.failing ["genuine REV is not green", "mutation set incomplete: 0 of 11"]`; no mutant verdicts | **CL5 open**, measured |
| 8 | draft counter identity | `sha256sum .ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py` | — | `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f` (equals `counter_sha256` in the JSON) | pins what was tested |
| 9 | draft C1 counter identity | `sha256sum .../draft/tools/round-49/c1-counter.py` | — | `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779` | recorded for the L1 |
| 10 | draft plan identity | `sha256sum .../draft/plans/round-49-claims.md` | — | `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492` | recorded for the L1 |
| 11 | tautology | `grep -n frozen_tables_valid .../c1-counter.py`; `sed -n 1988,1998p` | 0 | line 1995 `res['frozen_tables_valid'] = True`, set before `cur = show(...)`; only other path raises `Unevaluable`; line 2209 `b['frozen_tables_valid'] = bool(res.get(...))` | **confirms** C1SelfTest's claim; becomes marker M49-2(a) |
| 12 | round-start census file | `sha256sum .ufo/waves/round-49/l1/sources-census-start.txt`; `wc -l`; `tail -n2` | — | sha256 `653a3be854ae6f923dceb33d412ad0615a213fedcc6e4ae1f0a10b03a7890c96`; 17 lines; 15 `W04` lines; penultimate `kaidoku ok …corpus/SOURCES.md`; final line `exit=0` | recorded exit 0 (the file's own trailer; the census command's exit is not otherwise recorded in it) |
| 13 | census re-run | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` (2026-10-28T21:13:11Z) | 0 | stdout sha256 `065a45eb8e760d65d76e55e35e49efc44ee47466c1ffa147205757ea2589a2ea`; final line `kaidoku ok …`; first 15 lines identical to the start file | confirms round-start census |
| 14 | sweep (assimilation) | `test -e considerthese`; `test -e merge/kaidoku`; `git ls-tree -d e4f2cfa5… -- considerthese merge \| wc -l` | 1; 1; 0 lines | — | `Assimilation: none`, `considerthese` absent |
| 15 | base row count | `git show e4f2cfa5…:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` | 0 | `146`; `grep -c '\| S14[78] '` at base → 0 | census before = 146; S147/S148 do not exist yet |
| 16 | base rows for the claims | `git show e4f2cfa5…:corpus/SOURCES.md \| grep -E '^\|[[:space:]]*S(138\|139\|145\|146)[[:space:]]*\|'` | not captured | four rows printed: S138 and S139 (`opened` per plan), S145 and S146 (round-48 admit and reject rows) | S138/S139 exist at base; S147/S148 do not |
| 17 | S147 locator | snapshot `.ufo/waves/round-49/draft/snapshots/popper.html` tag-stripped | — | quote found at offset 12373 of the unescaped text; nearest headings before it: `1. Life`, `2. Backdrop to Popper&rsquo;s Thought` (`id=BackPoppThou`) | confirms closure defect 2: the locator is §2 "Backdrop to Popper's Thought", not §3 |
| 18 | plan carries CL items | `grep -n "R48-CL\|CL2\|CL3\|CL5\|quote-correction\|gate.py" plans/round-49-claims.md` | 0 | the only matching line is 148 (`gate.py` in the closure-6 text); the `R48-CL` string and the CL2/CL3/CL5 items do not appear | **CL2, CL3, CL5 absent from the plan**; no written decline |
| 19 | battery mutation count from plan | count of battery entries in receipt 6 | — | 11 | matches plan text ("eleven single-mutation overlays") |

Not run by this seat, by design: the freeze commit, `c1-counter.py` scoring, `c1-run.sh --data-run` (forbidden to seats), round-end census, peer reports' controls. Peer claims cited in M49-2 were not re-run.

## Landing-text check

- `lesson-skeleton.md` header: states the freeze is one commit and that there is no amendment series; `<FREEZE>` placeholder. The round-48 lesson's `Declared freeze \`<hex>\`` form is kept, because atom A1's regex reads that form.
- `## Mistakes`: M49-1 (`reference-drift`, evidence and fix as above, captured-by `none`), M49-2 as a marker row.
- `## Gate`: assimilation `none` with the sweep command from finding 14; sources marker for L1; census before 146.
- `## Corrections to round 48`: placeholder pointing at `w1/C2ScribeCorrections/`; expected line shapes taken from the counter's regexes, values not copied from any fixture.
- `## Census before -> after`: round-start exit 0 and final line `exit=0` (finding 12), with the re-run (finding 13).
- `## Routed defects (for round 49)`: closure items 1–8 mapped to atoms or declined (5, 6), items 7–8 partly not atomized (disclosed open), and R48-CL2/CL3/CL5 open.

## Open items for the L1

1. Decide whether R48-CL2, CL3 and CL5 enter the round-49 claims or are declined in writing. This seat's recommendation: name them open in the lesson (done in the skeleton); do not claim them.
2. Fold or remove M49-2(a) and (b). For (a), the fix is to compute `frozen_tables_valid` from the parse result and add a red selftest that forces a non-dict or missing key.
3. C2 closure items not atomized (receipt timestamp; cross-domain-evidence statement) are open, not counted.
4. The S147 locator should cite `2. Backdrop to Popper's Thought`, not `§3`.

## Receipts

`.ufo/waves/round-49/w1/C1ScribeLesson/receipts/` (`SHA256SUMS` lists every file): `c2-battery.json`, `c2-battery.out`, `c2-at-freeze.out`, `c2-freeze-battery.out`, `c2after.out`, `census-validate-now.out`, `census-validate-now.err` (empty), `sources-census-start.copy.txt`.

Artifacts: `.ufo/waves/round-49/w1/C1ScribeLesson/lesson-skeleton.md`.
