DONE — `absence-sweep.py` ships with an 18-case selftest, 7 mutants all killed, and the real R38-CL1
case demonstrated: fleet-root-only sweep exits 0 ABSENT (the false green), adding the shokuknow base
exits 1 PRESENT, for both staged paths.

# R39CL1AbsenceGate — an absence sweep that can be shown to fail

Item: a fix for routed defect **R38-CL1** (`corpus/lessons/round-38-verifier-spotcheck.md:127`, the
"false absence sweep": `round-38.md:80-82,96-97` and `w2/R38W2AssimRejects.md` claimed two staged
sources "exist nowhere on this host" from a `find` rooted at the fleet root only).
Measured at lane HEAD `a2f64e1da78afcf8cc39287106604dbcc270844c` (read-only `git rev-parse`).
Pass paths are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; the artifact directory
shortens to `$A` below = `.ufo/waves/round-39/w1/artifacts/R39CL1AbsenceGate/`.

## 1. Deliverable

| file | bytes | sha256 | role |
|---|---|---|---|
| `$A/absence-sweep.py` | 361 lines | `3a7a4abf2f7f0bc89f7b4a630f0458133752fe7da11c80d89443f11d92280775` | the instrument |
| `$A/mutants.py` | 137 lines | `a78a6762114de0df6af2a8a2232431850dfdd92e7b1e901b674caa78ca822a88` | falsifier for the selftest itself |
| `$A/selftest.txt` | — | `4717ac0ef548a2d19c735678e039592099aba069a6be0252655577a3c845cabe` | 18/18 |
| `$A/mutants.txt` | — | `d25a2d11543c24eb43e9f6e92dc442caafdbf1325c943037784d4fba67a64ebd` | 7/7 killed, M0 green |
| `$A/demo-real.txt` | — | `68159a780020da8382b4efbc4228d7eb7b465b99d938b1717965a7ef7695c63e` | the real case, exit 0 then 1 |
| `$A/demo-find.txt` | — | `f2724126552e55c964743fcd0170e6e49f7b5d3ed6a0140fcd0222853db8e694` | the round-38 `find` reproduced, plus its two-root form |
| `$A/file-facts.txt` | — | `f287a10fb02cd687c71123f4497a6a1fc10dbfda33b9de3e56f21aec4753ea68` | `ls -l`, sha256, head, tracking, `lanes/` absence |
| `$A/cli-contract.txt` | — | `a1b4441f864b0ee97c7c62c489df04c477793df9265f3986fb8f1e4a99bcff97` | exit-code matrix |
| `$A/hashes.txt` | — | — (it lists the others) | `sha256sum` pin list for the L1 |

CLI: `python3 -I -B absence-sweep.py --claim RELPATH --root R1 [--root R2 ...] [--json]
[--max-hits N] | --selftest`.
Exit codes, and no others: `0 ABSENT` · `1 PRESENT` (every hit printed) · `2` usage, missing/
unreadable root, **or** `ABSENT` with unreadable subtrees (reported as `INCOMPLETE`, never certified).
`--selftest` ends with `SELFTEST cases=18 pass=18 fail=0`.
A claim containing a glob metacharacter (`*`, `?`, `[`) is a usage error, because a glob matches
nothing and would certify a false `ABSENT`.

Why it addresses the defect rather than restating it: the roots are a mandatory repeated argument, so
a one-root sweep cannot be mistaken for a host-wide one; a sweep that could not read part of a root
cannot return `ABSENT`; and an `ABSENT` whose roots hold no directory named after the claim's leading
component emits `NOTE claim is unanchored: no root holds a 'lanes' directory, so ABSENT only covers
these roots and not the base the staged path is relative to` (`--json` carries `anchored_roots`).
The note is advisory and does not change the exit code, which is what keeps the required
fleet-root-only demo at exit 0 while still naming the mechanism out loud.

## 2. The real round-38 case (exact commands, outputs, exit codes)

From `$A/demo-real.txt`:

```
$ python3 -I -B absence-sweep.py --claim lanes/kaidoku/round7/work/r7-local-measurements.tsv \
    --root /home/vgpnk/Projects/shokunin
NOTE claim is unanchored: no root holds a 'lanes' directory, so ABSENT only covers these roots and
     not the base the staged path is relative to
VERDICT ABSENT claim=lanes/kaidoku/round7/work/r7-local-measurements.tsv roots=1 hits=0 \
        dirs_walked=119607 skipped_dirs=0 elapsed=1.741s
exit=0                                  <- the false green the round-38 lesson relied on

$ ... same claim ... --root /home/vgpnk/Projects/shokunin --root /home/vgpnk/Projects/shokuknow
HIT /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round7/work/r7-local-measurements.tsv kind=file \
    size=1204 root=/home/vgpnk/Projects/shokuknow
VERDICT PRESENT ... roots=2 hits=1 dirs_walked=122475 elapsed=1.235s
exit=1

$ ... --claim lanes/kaidoku/round9/work/lead2-avm-branch.tsv --root /home/vgpnk/Projects/shokunin
NOTE claim is unanchored ...
VERDICT ABSENT ... roots=1 hits=0 dirs_walked=119608 elapsed=1.185s
exit=0

$ ... same claim ... --root /home/vgpnk/Projects/shokunin --root /home/vgpnk/Projects/shokuknow
HIT /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round9/work/lead2-avm-branch.tsv kind=file \
    size=1177 root=/home/vgpnk/Projects/shokuknow
VERDICT PRESENT ... roots=2 hits=1 dirs_walked=122476 elapsed=1.204s
exit=1
```

Full sweep cost (both roots, 122 476 dirs / 991 884 entries): 1.2-1.7 s wall, no network. Every number
above is from `$A/demo-real.txt`.

`$A/demo-find.txt` shows the original instrument is still green-red-blind today:
`find /home/vgpnk/Projects/shokunin -name r7-local-measurements.tsv` → no output, `find_exit=0`;
the same `find` with both roots prints the shokuknow path. So the defect was never the tool, it was
the unnamed root scope — which is exactly what the new CLI makes non-optional.

Corroboration (`$A/file-facts.txt`, all read-only): r7 tsv `1204 B`, mtime `2026-10-24
01:07:30 -0300`, sha256 `d8fa9eae…8af6d`, row `M5 sasquatch-unblob-probe … "sasquatch is absent from
PATH and unblob is not importable on this host"`; lead2 tsv `1177 B`, mtime `2026-10-24 07:15:43
-0300`, sha256 `709cddc7…a1ea43`, rows `original_be_command` / `avm_branch_command` at lines 11/13.
Both are tracked in shokuknow (`git -C … ls-files --error-unmatch` exit 0, read-only). The fleet root
has **no** `lanes` directory (`ls -d` exit 2); the shokuknow root has one — that is the anchoring
fact the note reads.

## 3. Self-test (18 cases, `$A/selftest.txt`)

Fixtures are built under `$TMPDIR` (`TMPDIR=/fast/scratch/hyaku/kaidoku-r39/R39CL1AbsenceGate` here)
and removed by the selftest; each case runs the shippable CLI as a subprocess and asserts **the exit
code** plus required/forbidden output substrings.

| # | case | pins |
|---|---|---|
| 1 | `absent-empty-root` | exit 0 on a genuinely empty root |
| 2 | `present-exact` | exit 1, one hit, hit path printed |
| 3 | `present-second-root` | the R38 shape: clean root first, real file under root 2 → exit 1 |
| 4 | `multi-root-only-clean-is-absent` | the same tree with one root → exit 0 (the false green, reproducible) |
| 5 | `substring-decoy` | `xr7-…`, `…tsv.bak`, and component-tail decoy `xlanes/…/r7-…` never match |
| 6 | `missing-root` | exit 2, never a silent `ABSENT` |
| 7 | `file-root` | a root that is a regular file → exit 2 |
| 8 | `missing-claim` | usage → exit 2 |
| 9 | `absolute-claim` | absolute claim → exit 2 |
| 10 | `dotdot-claim` | `..` claim → exit 2 |
| 11 | `glob-claim` | a glob claim → exit 2 (never a silent `ABSENT`) |
| 12 | `nested-roots-dedup` | root nested inside another listed once |
| 13 | `duplicate-roots-dedup` | same `--root` twice listed once |
| 14 | `symlink-hit` | a symlink whose own path matches is a hit, `kind=symlink`, not followed |
| 15 | `unreadable-subtree-incomplete` | live `EACCES` subtree → `INCOMPLETE`, exit 2, never `ABSENT` |
| 16 | `same-tree-readable-absent` | same tree once readable → exit 0 (15/16 differ only by the mode) |
| 17 | `unanchored-note` | wrong-base `ABSENT` carries the anchoring note |
| 18 | `json-shape` | `--json` carries `verdict` and `exit_code` |

## 4. Shown able to fail (`$A/mutants.txt`)

`mutants.py` patches `absence-sweep.py` in `$TMPDIR` with one classic false-absence mechanism at a
time and demands that the mutant's **own** `--selftest` go red on the named case. A mutant surviving
would mean the covering case does not exist (reported as `SURVIVED` / `PATCH-SITE-NOT-UNIQUE`).

```
GREEN     M0-original                      SELFTEST cases=18 pass=18 fail=0  failed=-
KILLED    M1-substring-suffix              ... failed=substring-decoy
KILLED    M2-first-root-only               ... failed=present-second-root
KILLED    M3-swallow-root-errors           ... failed=missing-root,file-root
KILLED    M4-unreadable-subtree-as-absent  ... failed=unreadable-subtree-incomplete
KILLED    M7-no-glob-guard                 ... failed=glob-claim
KILLED    M6-no-anchor-note                ... failed=unanchored-note
KILLED    M5-no-root-dedupe                ... failed=nested-roots-dedup,duplicate-roots-dedup
```

`M2-first-root-only` is the R38-CL1 mechanism itself: with it the tool still exits 0 on the real
claim, so the selftest would have been worthless without case 3. `mutants_exit=0` means original
green and all seven mutants killed. This is the "shown able to fail" evidence the item asked for: the
harness is falsified by construction, not by assertion.

## 5. Proposed QUALITY criterion text (for R39CL1Correction to land)

> A **negative existence claim** (any statement that a path, entry or source "does not exist", or any
> refusal whose provenance ground is such a statement) is admitted only with an `absence-sweep.py`
> run whose exit is `0 ABSENT` **and** whose `anchored_roots` is non-empty — i.e. some named root
> actually holds the claim's leading directory. An `ABSENT` from roots that hold no such directory
> must be re-phrased as "absent from <root>" and cannot carry a refusal on its own. Gate command:
>
> ```
> python3 -I -B absence-sweep.py --claim <RELPATH> --root /home/vgpnk/Projects/shokunin \
>     --root /home/vgpnk/Projects/shokuknow --json
> # admit iff .verdict == "ABSENT" and .anchored_roots != [] ; PRESENT (exit 1) is not a defect,
> # it is the correction the claim needed
> ```

The two known bases on this host are the fleet root and the shokuknow root; any new base belongs in
the criterion's root list, which is the one thing the tool cannot infer.

## 6. Limits and risks

- Existence only. The tool says nothing about content, version or staleness; R38-CL1's surviving
  grounds (the `M5` host-state row that the round-36 installs superseded) still need the sibling
  seat's re-check. [INFERENCE] the sibling `R39CL1Correction` reaches the same row; I did not write
  any corpus text.
- Suffix semantics are component-aligned, so a claim must be the path **tail** as it appears on disk.
  A trailing slash is normalised away (measured: `…r7-local-measurements.tsv/` still gives
  `PRESENT`, exit 1); a wildcard is rejected with exit 2. Callers should pass the exact staged path.
- Directory symlinks are not followed (a hit *through* a symlinked root still works, because a root's
  own path is used and realpath-compared for dedupe); a file reached only through a symlinked
  subdirectory will not be seen. No such fixture exists in either searched tree today.
- Under `--json` the hit list caps at `--max-hits` (default 100) and says `truncated: true`; exit
  stays 1.
- `elapsed`/`dirs_walked` differ run to run (concurrent writers in the fleet tree; 119 573-119 608
  dirs observed). No number in this report depends on them.
- Not registered in `SKILL.md` (outside my bounds; R38-CL2 class). Recommend the L1 register it with
  its entry command, verdict map, selftest and this artifact path.

## 7. Bounds compliance

- Wrote only `$A/*` and this report. No writes to `corpus/`, `tools/`, `plans/`, `PROVINCE.md`,
  `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `LOG.md`, the fleet repo, siblings or shokuknow.
- No VCS mutation: only `git rev-parse` and `git ls-files --error-unmatch` (read-only).
- No network, no REA, no unblob, no sasquatch, no carrier built or run; no held-out material touched.
- No tool installed or upgraded (nothing was needed: `python3 3.14.8` present).
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39CL1AbsenceGate` created for `TMPDIR` fixtures and
  removed at the end of this seat; every cited byte lives in `$A/`.
