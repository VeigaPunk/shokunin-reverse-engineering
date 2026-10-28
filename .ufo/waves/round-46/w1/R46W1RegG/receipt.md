# R46W1RegG receipts

Seat R46W1RegG, round 46 wave 1. Task: three ready-to-paste instrument-registry rows.
Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze read-only at
`31820472784284727546808acc31b3ea1e73919b` (all three instrument sources byte-identical at
freeze and at lane HEAD `8757865679e62dac1f50efb33f583de0be884bf3`).

Scratch: `S=/fast/scratch/hyaku/kaidoku-r46/R46W1RegG`, `TMPDIR=$S`, `HYAKU_SCRATCH=$S`.
Removed after these receipts were copied here. Every tool ran as `python3 -I -B` (no
`__pycache__` written into the read-only lane tree).

Raw machine receipts: `receipts/commands.tsv` (sha256 `e0809561e952fac2e7f03a62e2e6aa16a9566a3a6099d5e2433a5763dc8cfc17`),
tab-separated `utc | label | exit | stdout-sha256 | command`.
Captured stdout: `receipts/{gen,eval,c2c}-selftest.out`, `receipts/validate.out`,
`receipts/audit.out`, `receipts/c2c-real.out`.

## Frozen instrument identity

| instrument | sha256 at `31820472` | lines |
|---|---|---|
| `tools/round-41/gen-squashfs.py` | `309c502d21dfeef9b7b2a5a9a62bfa875270fdf79eec671461070996d291042e` | 651 |
| `tools/round-42/indep-eval-v4.py` | `7a135dd36b3cab29d4dfa5b5d6dcf2199c026989549683933f4e6c1fa64dd301` | 765 |
| `tools/round-45/c2-counter.py` | `50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025` | 268 |

Derivation: `git show <freeze>:<path> | sha256sum` and `| wc -l`, both exit 0.

## Commands run (exit codes as observed)

| # | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-41/gen-squashfs.py --selftest` | 0 | `4edff26e…79c366` | 2026-10-28T16:54:45Z |
| 2 | `python3 -I -B tools/round-41/gen-squashfs.py --endian bogus` | 2 | `91c43aa4…b12e6a9` | 2026-10-28T16:54:45Z |
| 3 | `python3 -I -B tools/round-41/gen-squashfs.py` (no tree/out) | 2 | `cb28c5ad…6e68176` | 2026-10-28T16:54:45Z |
| 4 | `python3 -I -B tools/round-41/gen-squashfs.py --help` | 0 | `30f59390…c1ecd943` | 2026-10-28T16:54:45Z |
| 5 | `python3 -I -B tools/round-41/gen-squashfs.py $S/tree $S/tiny.sqsh` | 0 | `80941209…0d6eb831` | 2026-10-28T16:54:45Z |
| 6 | `python3 -I -B tools/round-42/indep-eval-v4.py --selftest` | 0 | `782c7679…7e652823` | 2026-10-28T16:54:45Z |
| 7 | `python3 -I -B tools/round-42/indep-eval-v4.py --help` | 0 | `5c5d92c7…eae22a7b` | 2026-10-28T16:54:45Z |
| 8 | `python3 -I -B tools/round-42/indep-eval-v4.py` (no args) | 2 | `21b1cc14…e763d39` | 2026-10-28T16:54:45Z |
| 9 | `python3 -I -B tools/round-42/indep-eval-v4.py $S/nope.json` | 2 | `8922909c…cb74ab85` | 2026-10-28T16:54:45Z |
| 10 | `python3 -I -B tools/round-42/indep-eval-v4.py --envelopes $S/nodir` | 2 | `e7c507ee…faf3158c` | 2026-10-28T16:54:45Z |
| 11 | `python3 -I -B tools/round-42/indep-eval-v4.py --envelopes $S/emptydir` | 0 | `c34f624e…b89ec5921` | 2026-10-28T16:54:45Z |
| 12 | `python3 -I -B tools/round-45/c2-counter.py --selftest` | 0 | `aea7e363…b40b0f2d` | 2026-10-28T16:54:46Z |
| 13 | `python3 -I -B tools/round-45/c2-counter.py` (no args) | 2 | `0848cd31…25187436` | 2026-10-28T16:54:46Z |
| 14 | `python3 -I -B $S/validate_rows.py` (frozen `score()` on `rows.md`) | 0 | `1f746333…d6b2ab607` | 2026-10-28T16:54:46Z |
| 15 | `python3 -I -B $S/audit.py` (row shape + landed-rows rescore) | 0 | `239e423e…253b6316341256` | 2026-10-28T16:54:46Z |

### Extra probes (calibration — impossible inputs and IO failure)

| # | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| 16 | `gen-squashfs.py $S/NOSUCHTREE $S/empty.sqsh` | 1 | `06ad0406…0e7ccb7ae7` | 2026-10-28T16:55:17Z |
| 17 | `gen-squashfs.py $S/tree/a/f.txt $S/filetree.sqsh` (tree is a file) | 1 | `06ad0406…0e7ccb7ae7` | 2026-10-28T16:55:17Z |
| 18 | `gen-squashfs.py $S/tree $S/nodir/out.sqsh` (out dir missing) | 1 | `924cb8c7…2ca88a1e2` | 2026-10-28T16:55:17Z |
| 19 | `indep-eval-v4.py $S/bare.json` (`{"operation":"x"}`) | 0 | `64faf0bc…015a4b5028` | 2026-10-28T16:55:17Z |
| 20 | `indep-eval-v4.py $S/list.json` (`[1,2]`) | 2 | `29192377…fea3abfec` | 2026-10-28T16:55:17Z |
| 21 | `indep-eval-v4.py $S/bad.txt` (not JSON) | 2 | `bac0d4c0…5ea79e779` | 2026-10-28T16:55:17Z |
| 22 | `c2-counter.py --root . --freeze 31820472 --rev deadbeef` | 2 | `18fef53d…4e8f57` | 2026-10-28T16:55:17Z |
| 23 | `c2-counter.py --root . --freeze HEAD --rev 31820472` (freeze not ancestor) | 2 | `c1b9db74…f3efe59` | 2026-10-28T16:55:17Z |
| 24 | `c2-counter.py … --rev HEAD --json-out $S/nodir/o.json` | 1 | `528ec682…3bf9911` | 2026-10-28T16:55:17Z |
| 25 | `c2-counter.py --root . --freeze 31820472 --rev HEAD` (read-only lane score) | 0 | `fa00db27…4ec4e7c45c` | 2026-10-28T16:55:17Z |

`$S` above is `/fast/scratch/hyaku/kaidoku-r46/R46W1RegG`; the full command lines are in
`receipts/commands.tsv`.

## Self-test summary lines (the stable part of each stdout)

- `gen-selftest` → `selftest: 71 passed, 0 failed`
- `eval-selftest` → `45/45 cases; 0 failure(s)` (plus `PASS every step 1-15 is exercised`,
  `PASS every (label, action) pair is exercised`)
- `c2c-selftest` → `C2_SELFTEST: cases=7 failures=0`

Caveat on stdout sha256: `gen-squashfs.py --selftest` prints the randomised
`tempfile.mkdtemp` path (`sqfs-selftest-<random>`), so its stdout is NOT byte-stable across
runs — two runs gave `4edff26e…` and `113ef98b…`. The stdout sha pins *this run's* bytes only;
the stable evidence is the summary line above, which both runs carry.

## Row validation with the frozen scorer (took no part in writing the rows)

`receipts/validate.out` — imports `tools/round-46/registry.py` from a scratch copy of the
freeze and calls `score(skill, files, "r46", "v2", rev, battery=None)`:

- **A, census = my three paths:** exit **0**; `scope_size 3`, `registry_rows 3`,
  `registered` = all three, `unregistered []`, `thin []`, `absent_at_rev []`, `failing []`,
  `header` = the house 7-cell schema.
- **B, census = all 38 frozen paths, only my three rows present:** exit **1** with the single
  failing clause `unregistered: 35 of 38` — i.e. my three rows are counted and pass
  clauses 3/4/5, and the remaining 35 are other seats' rows, not a defect in mine.

`receipts/audit.out` — per-row shape: each row `cells=7`, `backticks=2` (only the cell-0
path), `cell0_ok=True`, `exitmap=['0','1','2']`.

## Freeze-arm evidence (found while validating; decisive for the C2 scoring command)

`python3 -I -B $S/freeze_evidence.py` → exit 0, stdout sha256
`82ff273490de3600bb549f859cfe1c6d25e278e7b0554e25cd487922a005bfb4`
(`receipts/freeze-evidence.out`), 2026-10-28T16:57:12Z. It imports `gate`/`registry` from
scratch copies of `65678df0` (the lane's measured freeze) and calls `gate.freeze_state`
read-only:

```
[FREEZE=31820472 REV=31820472]        exit=0
[FREEZE=31820472 REV=50862e4a]       exit=2  frozen_path_changed
[FREEZE=31820472 REV=HEAD(e3dfdbad)] exit=2  frozen_path_changed
[FREEZE=65678df0 REV=HEAD]           exit=0
[rows scored by 65678df0 registry.py, 3-path census] exit=0  thin=[]  unregistered=[]
```

i.e. the freeze named in the prompt cannot score any rev at or after `50862e4a`. Remaining
caveat: this sha pins this run of the script; the script prints no scratch paths, so it is
reproducible byte-for-byte given the same revs.

## Read-only guarantee

No mutating git/jj command was run in the lane. The only writes are under
`.ufo/waves/round-46/w1/R46W1RegG/` and the scratch dir (now removed). `git status
--porcelain` was read only. Nothing under `/tmp` was written or cited.
