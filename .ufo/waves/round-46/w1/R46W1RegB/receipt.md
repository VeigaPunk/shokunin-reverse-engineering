# R46W1RegB — receipts

Seat: `R46W1RegB` (round-46 C2 census, tag `reg-b`). Read-only on the lane tree; every
write went to `/fast/scratch/hyaku/kaidoku-r46/R46W1RegB` (removed after this file and
`rows.md` were written) or to this wave dir.

- Freeze: `31820472784284727546808acc31b3ea1e73919b`
- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Scratch: `/fast/scratch/hyaku/kaidoku-r46/R46W1RegB` (`TMPDIR` / `HYAKU_SCRATCH` set to it)
- Host: `linux 7.2.11-arch1-1`; `python3` from PATH; `git`, `jq`, `unsquashfs`, `7z`,
  `sasquatch` all resolvable. No install, no upgrade, no pacman/uv/npm transaction.

## Frozen bytes read (copied with `git show <freeze>:<path>`, then hashed)

| path | sha256 of the freeze blob |
|---|---|
| `tools/round-41/c1-extra.py` | `531724e1c7215ed602a06648525cc375b4c9d86370f8e37ea59657a087ceacae` |
| `tools/round-42/c1-run.sh` | `a79ab3cd3ab30f1b6aa3dedccbda0cab2127bf031f43a37adf6497067d48da4d` |
| `tools/round-43/verify-copies-r43.py` | `00b3f7a4c7a2ee7f5a6654f12211cbf2a12e0fe10e9de7fc35ff088ce8f3b020` |
| `tools/round-46/registry.py` (validator) | `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449` |
| `tools/round-46/gate.py` (registry import) | `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` |
| `tools/round-46/census.json` (scope) | 38 paths; the three assigned ids present, `named_but_absent == []` |
| `tools/round-42/sqfs3-oracle.py` (used by the c1-run oracle-arm probes) | `9e03f9349db21c6a92a82ba96321401746df6fc7deb47fc739d1d99311547bdb` |
| `tools/round-41/{gen-squashfs,sqfs-list}.py` (c1-extra selftest tools dir) | read at the same freeze |

Frozen-path presence at the freeze (`git cat-file -e`): all three instrument paths plus
`.ufo/waves/round-41/c1/carriers.json` and `corpus/evidence/local-sources.json` are present.

## Commands actually run (exit code, stdout sha256, UTC)

Raw rows: `receipts/receipt.tsv` (`name<TAB>rc<TAB>stdout_sha256<TAB>utc<TAB>stderr_bytes`).
Stdout/stderr bodies: `receipts/<name>.stdout|.stderr`.

| # | command | rc | stdout sha256 | UTC | verified claim |
|---|---|---|---|---|---|
| 1 | `python3 -I -B frozen/c1-extra.py --help` | 0 | `784725ab854c7c17…` | 2026-10-28T16:51:14Z | CLI surface exists |
| 2 | `python3 -I -B frozen/c1-extra.py` | 2 | `e3b0c442…` (empty) | 16:51:14Z | missing `--root/--rev/--freeze/--base` → 2 (`usage: --root --rev --freeze --base required`) |
| 3 | `python3 -I -B frozen/c1-extra.py --selftest --tools frozen/tools41 --work $S/work` | 0 | `b2ed17d2…` | 16:51:14Z | self-test green: `SELFTEST cases=17 pass=17 fail=0` |
| 4 | `python3 -I -B frozen/c1-extra.py --root $D --rev $FRZ --freeze $FRZ --base $BASE --work $S/work` (fixture repo, 2 commits) | 1 | `eaf42b32…` | 16:53:34Z | `met=false`, all three bindings false, `exit_code=1` |
| 5 | same with `--rev deadbeef` | 2 | `7c9b4016…` | 16:53:34Z | `unevaluable: not a commit: deadbeef`, `exit_code=2` |
| 6 | `bash frozen/c1-run.sh` | 2 | empty | 16:51:16Z | no argv → usage header → 2 |
| 7 | `bash frozen/c1-run.sh bogus args here` | 2 | empty | 16:51:16Z | unknown mode → 2 |
| 8 | `bash frozen/c1-run.sh oracle /nonexistent/carrier.bin S` | 2 | empty | 16:51:16Z | `carrier is not a regular file` → 2 |
| 9 | `bash frozen/c1-run.sh oracle carrier.txt $S/probe-out` | 2 | empty | 16:53:24Z | `OUTDIR … outside the round-42 evidence root` → 2 (and nothing created in the lane) |
| 10 | `C1_ALLOW_FOREIGN_OUTDIR=1 bash frozen/c1-run.sh oracle carrier.txt $S/probe-out2` | 2 | empty | 16:53:24Z | `no SquashFS magic …` → 2 |
| 11 | `C1_ALLOW_FOREIGN_OUTDIR=1 bash frozen/c1-run.sh oracle v4.sqsh $S/probe-out3` (genuine v4 image) | 2 | empty | 16:53:25Z | `oracle could not read the carrier (exit 2 …)` → 2 |
| 12 | `python3 -I -B frozen/verify-copies-r43.py --help` | 0 | `4b3a8778…` | 16:51:16Z | CLI surface exists |
| 13 | `python3 -I -B frozen/verify-copies-r43.py` | 2 | empty | 16:51:16Z | argparse: required `--root/--rev/--freeze` missing → 2 |
| 14 | `python3 -I -B frozen/verify-copies-r43.py --root <lane> --rev <freeze> --freeze <freeze>` | 1 | `211f60b9…` | 16:51:16Z | `checks: 136, failures: 3` → 1; the 3 FAILs are `host-state` S035 ×2 and S081 |
| 15 | `python3 -I -B validate.py` (frozen `registry.py` parser + `HOUSE` + `EXITMAP`) | 0 | `42fb3290…` | 16:53:39Z | `VALIDATE failures=0` (header, 3 rows, 7 cells each, exact cell 0, `{0,1,2}` per verdict map, presence at freeze) |

Fixture repo for #4/#5: `git -C "$D" rev-parse --show-toplevel` printed `$D` before the first
commit (asserted equal); commits used `-c user.name=fx -c user.email=fx@fx`. `D` lived inside
`$S`.

## Claims per row: what was exercised and what was only source-read

**Row 1 `tools/round-41/c1-extra.py`**
- `0` — exercised by the self-test (#3, 17/17, rc 0).
- `1` — exercised by the all-bindings-false fixture (#4, rc 1, `met=false`).
- `2` — exercised twice: missing required argv (#2) and a non-commit revision (#5).
- `2` from "carriers.json / reader absent at `--freeze`" — **source-read, not run** (`oracle_rederived` raises `Unevaluable('absent at freeze: …')`, line 80 of the freeze blob). The self-test does not have a case for an absent reader; it does have `bad-rev-unevaluable`.
- `2` from "selftest tools dir missing `gen-squashfs.py`/`sqfs-list.py`" — **source-read only** (`tool_dir() is None → print ... tool_dir_missing, return 2`, line 195).
- No exit code outside {0,1,2}: the only `return`/`exit` sites are lines 195 (`2`), 361 (`0`/`1`), 375 (`2`), 378 (`0`/`1`), 380 (`2`), 385.

**Row 2 `tools/round-42/c1-run.sh`**
- `2` — exercised five ways (#6, #7, #8, #9, #10, #11). The header's exit contract is
  `0 ok, 2 usage/environment error, 3 tool failure`.
- `0` — **source-read, not run**: both arms end with `exit 0` after writing their artefacts
  (`exit 0` at the end of the oracle arm, `exit 0` after a written receipt in the after arm).
  Not exercised because no v1–v3 carrier is available offline: `tools/round-41/gen-squashfs.py`
  writes 4.0 only (`--endian {le,be,avm,avm-genuine}` over a v4 superblock), the round-42
  fixtures are network LFS (`tools/round-42/fixtures.json`), and `corpus/evidence/round-42/c1/*`
  holds no carrier bytes. Exercise it before this row is cited as evidence for `0`.
- `1` — **not a designed verdict**. The script contains no `exit 1`; the only occurrence of the
  string is the comment `REA exit 1` (line 764, the child's status). Under `set -euo pipefail`
  an unguarded command failure aborts with that command's status, which can be 1, so the row
  says so instead of inventing a meaning.
- **Flagged, reported here and not in the row (seat spec):** the tool takes an exit code
  outside {0,1,2} — **`3` = tool failure** (`fail()`, lines 78 and 929: oracle exit ∉ {0,2}, or
  unusable tables). A `3` is a real failure, a `2` is an environment/usage refusal; neither is
  a verdict on the claim.
- Side effect noticed, not a defect: on the oracle-exit-2 path (#11) the harness still writes
  `oracle-run.json` into OUTDIR before refusing, so a receipt can exist under an exit-2 OUTDIR;
  consumers must read `oracle.exit` in that JSON rather than infer from the directory.

**Row 3 `tools/round-43/verify-copies-r43.py`**
- `1` — exercised by the real lane run at the freeze (#14, `checks: 136, failures: 3`, rc 1).
- `2` — exercised by the argparse probe (#13).
- `0` — **source-read, not run**: `return 0 if failures == 0 else 1`. On this host it cannot be
  reached without out-of-band `--upstream-dir`/`--tarball`/`--tarball-650`: the three FAILs are
  `host-state` S035 (go1.25.0, go1.24.6 host dirs absent) and S081 (npx dist absent), exactly
  the round-43 finding. So the row's `0` is reachable only with those inputs supplied.
- `1` also covers an unhandled error (an absent `--map` raises `FileNotFoundError` →
  interpreter exit 1 with a traceback, not 2) — **source-read, not run**.
- The `expect-source-frozen` check passed here (`work=freeze=rev=1f790e10…`), so the imported
  round-42 verifier bytes are the freeze blobs.

## Not run (stated, not passed)

- No real v1–v3 SquashFS data run of `c1-run.sh` (see above); no exit-3 perturbation of it.
- No `c1-extra.py` measure run against the real round-41 revisions (the 17-case self-test
  covers the green and each red arm on one-commit fixtures).
- No `verify-copies-r43.py` run with `--upstream-dir`/`--tarball`, i.e. no green run.
- The registry row check ran through the frozen `registry.py` parser on a synthetic section with
  the house header; it did not run the full `registry.py --profile v2` scoring, which would also
  require the other 35 census rows and the 7-forgery battery (the L1's integration step).
