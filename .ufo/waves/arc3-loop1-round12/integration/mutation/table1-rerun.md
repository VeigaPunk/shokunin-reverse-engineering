# Table-1 rerun — `pl4-*` needle variants: PL-4 → tightened → final

Seat: R12Mutation. Method identical across all three passes: `git archive
de77d75` → `/var/tmp/kaidoku-r12-mut/tree`, `git init`, one throwaway commit
per mutant, `run_check`/`report(strict=True)` imported from the probe module;
table and `expected.json` passed via scratch paths, never the repo copies.
W was read-only except this file. Scratch deleted after each run.

Three table variants measured:

- **old** = PL-4 rows (`claims/c3/PL-4.md:36-60`), entries 57→60, sha256
  `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2`.
- **tightened** = worktree table v2, sha256
  `ec3ae3aa2a6191029ed069f8d1b8de3b510147acc65410a8c6cda67353bd59fc`.
- **final** = worktree table v3 (r7 needle drops literal `expect ` and the
  trailing `; \`TMPDIR\` must be disk-backed` clause), sha256
  `e62102189f6bccbf849288232690b39329938f64d2b7bcafed32b5c0afe20120`.

Command per mutant (all runs):

```text
git reset --hard <baseline> && apply-mutant && git commit
probe.run_check(scratch_root, "HEAD", scratch_table, scratch_expected, None)
probe.report(..., strict=True)   # exit 1 + citation_dead = killed; exit 0 = survived
```

Control on pristine baseline: `clean findings=0 exit=0` in all three runs.

## Per-mutant results (24 breaking, 9 harmless)

| mutant (target line) | old | tightened | final |
|---|---|---|---|
| r7:5 TMPDIR dir → `/tmp` | killed | killed | killed |
| r7:5 expected `ev_ffd8f0b9…` one-hex swap | killed | killed | killed |
| r7:5 recheck line deleted | killed | killed | killed |
| r7:5 line shifted (:5→:6) | killed | killed | killed |
| r7:5 expected-id clause dropped | killed | killed | killed |
| r7:5 `inspect-evm-interface-legacy` (prefix suffix) | survived | killed | killed |
| r7:5 `arc3-loop1-round7`→`round99` | survived | killed | killed |
| r7:5 scratch dir `…-recheck`→`…-recheck-old` | survived | killed | killed |
| r10:7 `recompute-ids.mjs`→`.py` | killed | killed | killed |
| r10:7 recompute-script clause dropped | killed | killed | killed |
| r10:7 `rederive-commands.txt`→`.md` | killed | killed | killed |
| r10:7 recheck line deleted | killed | killed | killed |
| r10:7 line shifted (:7→:8) | killed | killed | killed |
| r10:7 `evidence/`→`evidence-old/` | killed | killed | killed |
| r10:7 `arc3-loop1-round10`→`round99` | survived | killed | killed |
| r10:7 `claims/c1`→`claims/c2` | survived | killed | killed |
| r11:7 `TMPDIR` pointed at `/tmp` | survived | killed | killed |
| r11:7 `recompute-ids.py` clause dropped | killed | killed | killed |
| r11:7 `calls.txt`→`calls.md` | killed | killed | killed |
| r11:7 recheck line deleted | killed | killed | killed |
| r11:7 line shifted (:7→:8) | killed | killed | killed |
| r11:7 `identity.txt`→`identity.md` | killed | killed | killed |
| r11:7 "Do not use `/tmp` for scratch." tail dropped | killed | killed | killed |
| r11:7 `arc3-loop1-round11`→`round99` | survived | killed | killed |
| r7:5 trailing whitespace (harmless) | survived | survived | survived |
| r7:5 `expect`→`yield` reword (harmless) | survived | **killed (FA)** | survived |
| r7:5 trailing note appended (harmless) | survived | survived | survived |
| r10:7 trailing whitespace (harmless) | survived | survived | survived |
| r10:7 `read-only`→`non-mutating` (harmless) | survived | survived | survived |
| r10:7 trailing note appended (harmless) | survived | survived | survived |
| r11:7 trailing whitespace (harmless) | survived | survived | survived |
| r11:7 `byte-identical copies`→`identical copies` (harmless) | survived | survived | survived |
| r11:7 trailing note appended (harmless) | survived | survived | survived |

## Kill rates

- **Breaking:** old 17/24 (71%) → tightened 24/24 → **final 24/24 (100%)**.
  All seven old survivors (substring-prefix renames + unpinned path tokens +
  r11's bare-`TMPDIR` token) are killed by both tightened variants.
- **False alarms:** old 0/9 → tightened 1/9 (`r7-reword`: `expect`→`yield`,
  pinned by the literal word `expect`) → **final 0/9**. Dropping the literal
  `expect ` and the `disk-backed` tail from the r7 needle removed the one
  precision regression at zero recall cost.

Verdict: the final table `e6210218…` achieves perfect discrimination on this
matrix — 24/24 breaking killed, 0/9 harmless flagged. No surviving breaking
mutant; no coverage gap remains on the pinned instruction surface. The only
residual weakness is inherent to `exact`-kind substring needles: tokens
between pinned literals (e.g. rewordings inside `.*` spans, or a wholesale
line rewrite that preserves every pinned token in order) are ungradeable —
acceptable per the probe's stated contract.
