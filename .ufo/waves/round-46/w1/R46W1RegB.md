# R46W1RegB — round-46 C2 census registry rows (tag `reg-b`)

Seat: registry-row drafter for the round-46 C2 census. Three census instruments read at the
freeze, each claim in each row exercised with a command that was actually run. Read-only on the
lane tree; writes only to `.ufo/waves/round-46/w1/R46W1RegB/` (this report, `rows.md`,
`receipt.md`, `receipts/`).

- Freeze: `31820472784284727546808acc31b3ea1e73919b`
- Census read at the freeze: `tools/round-46/census.json` — 38 paths,
  `named_but_absent == []`; the three assigned ids are in scope.
- Frozen blobs (sha256): `c1-extra.py` `531724e1…`, `c1-run.sh` `a79ab3cd…`,
  `verify-copies-r43.py` `00b3f7a4…`.
- Installs/upgrades: **none** (no pacman/uv/npm transaction; nothing added to PATH directories).

## Rows (ready to paste — also in `rows.md`, exactly three lines)

| `tools/round-41/c1-extra.py` | gate — R41-C1 supplementary bindings the counter does not enforce: oracle_rederived re-runs the frozen sqfs-list.py reader on every pinned carrier and reproduces oracle.tsv and nonregular.tsv as row sets, sourced_new requires an S-id absent at --base and present at --rev with the round-41 entry in its used-by cell, frontier_content requires the round-41 frontier note to name the heading, the entry stem, a supersede verb and the round-40 measured-not-promoted record | 0=all three bindings true, or a selftest in which every case passes; 1=a binding false, or at least one selftest case fails; 2=unevaluable, from a non-commit --rev/--freeze/--base, carriers.json or the reader absent at --freeze, a missing --root/--rev/--freeze/--base, or a selftest whose tools dir lacks gen-squashfs.py and sqfs-list.py | python3 -I -B tools/round-41/c1-extra.py --selftest --tools tools/round-41 --work "$HYAKU_SCRATCH" — 17 cases, 17 pass, exit 0 on 2026-10-28 | .ufo/waves/round-41/c1/carriers.json (per-carrier sha256, oracle and nonregular paths) | --json-out FILE; scratch under $HYAKU_SCRATCH/kaidoku-r41 or --work | kaidoku |
| `tools/round-42/c1-run.sh` | probe — the R42-C1 data harness: the after arm runs REA extract-firmware (rea-agents 6.5.0, unblob 26.6.4, plain sasquatch under a fixed PATH) and writes after.json plus run.json, the oracle arm runs sqfs3-oracle.py and writes oracle.tsv, nonregular.tsv, oracle-inner.json and oracle-run.json | 0=ok, the arm wrote its receipt and tables; 1=no designed verdict, an unguarded command under set -e aborts with that command's status, which may be 1; 2=usage or environment refusal (bad argv, missing python3 or jq, carrier not a regular file, OUTDIR outside the round-42 evidence root, SCRATCH without a /kaidoku-r42/ segment, plain sasquatch not resolvable) | none — no self-test mode; bad-argument probes only (no args, unknown mode and a missing carrier each exit 2) | none — the carrier sha256 is taken from the argv file and the tool pins (rea-agents 6.5.0, unblob, sasquatch) are host paths recorded in run.json, not repo files | OUTDIR (corpus/evidence/round-42/c1/<id>: after.json, run.json, extract-env.json, or oracle.tsv, nonregular.tsv, oracle-inner.json, oracle-run.json) plus scratch under $HYAKU_SCRATCH/kaidoku-r42 | kaidoku |
| `tools/round-43/verify-copies-r43.py` | gate — R43-C2 landing verifier for the local-sources pack: map shape and key set against the frozen gate's own path extraction, copy regularity, stated dir, digest and byte-identity, member pins from the round-42 EXPECT table plus the S048 extension, host or upstream identity, and the freeze binding of the imported verifier | 0=every emitted check OK (exit 0 only when the failure count is 0); 1=at least one emitted check FAIL, or an unhandled error such as an absent map; 2=argparse usage error, a required --root, --rev or --freeze missing | none — no --selftest; probe with --help (0) or no args (2) | corpus/evidence/local-sources.json (--map: per-entry sha256 and source_sha256 pins) | none — stdout only | kaidoku |

House-format check, run against the **frozen** `tools/round-46/registry.py` parser plus its
`HOUSE` header and `EXITMAP` regex (`python3 -I -B validate.py`, rc 0,
`VALIDATE failures=0`): exactly 3 data rows, 7 cells each, cell 0 exactly the backticked census
path, cell 2's `EXITMAP` key set exactly `{0,1,2}` per row, every path present at the freeze,
no stray `|` inside a cell, no row outside the three assigned ids. Raw stdout:
`receipts/rows-validate.stdout`.

## Evidence per row (all commands in `receipt.tsv` with rc, stdout sha256, UTC)

**`tools/round-41/c1-extra.py`** — self-test green: `SELFTEST cases=17 pass=17 fail=0`, rc 0
(the 17 cases cover the green arm, six `oracle_rederived` red arms, three `sourced_new` red
arms, four `frontier_content` red arms, a restore, and `bad-rev-unevaluable`). Exit 1 verified
on a two-commit fixture repo (`--root $D --rev $FRZ --freeze $FRZ --base $BASE`): rc 1,
`met=false`, `bindings {frontier_content:false, oracle_rederived:false, sourced_new:false}`,
`exit_code=1`. Exit 2 verified twice: missing required argv (rc 2, `usage: --root --rev
--freeze --base required`) and `--rev deadbeef` (rc 2, `unevaluable: not a commit: deadbeef`).
Pinned-value path `.ufo/waves/round-41/c1/carriers.json` present at the freeze and read by
`oracle_rederived` (per-carrier `sha256` compared before the reader runs).

**`tools/round-42/c1-run.sh`** — exit 2 verified five ways: no argv (usage header), unknown
mode, non-regular carrier, OUTDIR outside the round-42 evidence root (refused **before** any
lane write; the probe OUTDIR was inside my scratch), no SquashFS magic in a 1 MiB scan, and an
oracle that rejects the image (`oracle could not read the carrier (exit 2 …)`). Exit 0 was
source-read only (see limits). The script has no self-test mode; the row says `none`.

**`tools/round-43/verify-copies-r43.py`** — real run at the freeze against the lane:
`checks: 136, failures: 3`, rc 1; the three FAILs are `host-state` S035 (both go toolchain dirs
absent on this host) and S081 (npx dist absent) with no `--upstream-dir`/`--tarball`. That is
the round-43 finding still true today, and it is why `0` is not reachable here without
out-of-band inputs. `expect-source-frozen` passed (`work=freeze=rev=1f790e10…`), so the
imported round-42 verifier is the freeze bytes. argparse probe with no args: rc 2.

## Calibration flags for the L1 (deliberately outside the rows)

1. **`c1-run.sh` takes an exit code outside {0,1,2}: `3` = tool failure** (`fail()` at the
   `oracle_rc ∉ {0,2}` branch and at the unusable-tables branch; header line `Exit: 0 ok, 2
   usage/environment error, 3 tool failure`). Per the seat spec this is reported here and is
   not bound in the row; the row binds `1` only as "no designed verdict". If the registry house
   rule is meant to admit a fourth code, this is the row that would need it.
2. **`1` in `c1-run.sh` is not designed.** The only `exit 1` string in the freeze blob is the
   comment `REA exit 1` (line 764). Under `set -euo pipefail` an unguarded command failure
   aborts with its own status, so 1 is reachable by accident, not by contract — a `1` from this
   tool is not a verdict.
3. **`c1-run.sh` writes `oracle-run.json` before refusing with exit 2** (verified: the probe
   OUTDIR held `oracle-inner.json` and `oracle-run.json` beside the refusal). A consumer that
   treats "exit 2 + artefacts present" as "early exit" will misread the receipt; read
   `oracle.exit` in that JSON instead.
4. **`0` not exercised for rows 2 and 3** (honest capture, not a pass): no v1–v3 carrier is
   available offline (`gen-squashfs.py` writes 4.0 only; round-42 fixtures are network LFS;
   `corpus/evidence/round-42/c1/` holds no carrier bytes), and `verify-copies-r43.py` cannot
   reach 0 on this host without `--upstream-dir`/`--tarball`/`--tarball-650`.
5. **`verify-copies-r43.py` maps an unhandled error (absent `--map`) to 1 via a traceback**, not
   to 2. The row says so under `1`; it is source-read, not run.

## Files written

- `.ufo/waves/round-46/w1/R46W1RegB/rows.md` — the three rows, nothing else.
- `.ufo/waves/round-46/w1/R46W1RegB/receipt.md` — per-command record, frozen hashes, what was
  source-read vs run.
- `.ufo/waves/round-46/w1/R46W1RegB/receipts/` — `receipt.tsv` plus every stdout/stderr body.
- `.ufo/waves/round-46/w1/R46W1RegB.md` — this report.
- Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1RegB` removed after the receipts were copied.

## Risks / blockers

- None blocking. The only open item is the unexercised `0` for rows 2 and 3 and the undesignated
  `1`/extra `3` of `c1-run.sh`; both are stated above rather than papered over.
- Observed external change, not mine: `tools/round-46/{registry,gate}.py` were dirty in the
  worktree at seat start and clean again by seat end; `tools/round-46/attest.py` is still dirty.
  I never touched `tools/` (all instruments were copied out of `git show` into scratch).
