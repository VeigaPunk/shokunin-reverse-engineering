# StrictBaselineReceipts — R18-STRICT-BASELINE (C1 calibration)

Seat: `KaidokuR19.StrictBaselineReceipts` (executor). Target `corpus/lessons/round-18-verifier-spotcheck.md:195`.
Base observed: `git -C /tmp/kr19-StrictBaselineReceipts rev-parse HEAD` → `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`
(exit 0). Clone: `/tmp/kr19-StrictBaselineReceipts` (`git clone --no-hardlinks` of LANE, detached at base; the
contract's `Writers` clone name — contract `.ufo/waves/round-19/contract.md:8-17`).
Tool: round-18 `routed-defects.py` as committed at `a245bb00c581ae3423a10a055c77d4bc873918df`, extracted with
`git show`, sha256 `b004c3ed76fd72aca7667e85d335c8296257e8b7e4891ef53113043950e72b03`.

## Result (observation)

Both expected exits reproduce exactly:

| rev | strict exit | open_count | named_open | substance_open | stdout sha256 |
|---|---|---|---|---|---|
| `9011581d84527ba34c675f9cf912e54d2e72d470` | **1** | 6 | 6 | 6 | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| `454dee6923750698cc36041236db13b52c6fcade` | **0** | 0 | 0 | 0 | `7873566c4c95374be4306b5d6461dd717eb7508c251b46c20d2d8070f5ab92d4` |

`open_count` rule per the tool: a defect is open when any `named` **or** any `substance` check fails
(`/tmp/kr19-sb-tool/routed-defects.py:1290-1292`, same text as `a245bb00` blob). `--strict` exit rule:
`if args.strict and doc["open_count"] > 0: return 1` (`/tmp/kr19-sb-tool/routed-defects.py:1326-1327`).
At `9011581` the six open defects are R17-PINMAP, R17-VALIDATE16, R17-PRODUCER-REV, R17-SUMS-RUNLOG,
R17-REGISTRY, R17-S032-DIGEST (each: named_open=True, substance_open=True). At `454dee6` all six are closed
(named=False, substance=0). This matches the SCORECARD claim under test, `SCORECARD.md:2451`
("exit 1 at `9011581`, exit 0 at `454dee6`").

Non-strict control at `9011581` (same tool, no `--strict`): exit **0**, `open_count` 6, stdout sha256
`48266a3e…54316` — byte-identical stdout to the strict run. Therefore the exit 1 is attributable exclusively to
`--strict`, not to any tool/input difference. (Observation; both stderr files are empty, sha256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.)

Determinism: each strict command was run a second time; stdout sha256 equalled the retained first run for both revs
(`48266a3e…`, `7873566c…`), exit codes 1 and 0. The tool output carries no timestamps, so receipts are pure
function of `(tool blob, root Git objects, rev)`.

## Retained evidence (in the patch; materialized by `git apply`)

`.ufo/waves/round-19/evidence/strict-baseline/`:

| file | bytes | sha256 |
|---|---|---|
| `9011581d8452.receipt.json` | 705 | `dc7d3836012c93231367f6fc81fdadbe2beca29213994de54d7f344c8a2c7f50` |
| `9011581d8452.stdout.txt` | 9428 | `48266a3efa091356612a297f090d3bb0e3a82ca686ba52c97074b0fbf2154316` |
| `9011581d8452.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `454dee692375.receipt.json` | 705 | `3d050410976838560b6a5b8dd3d1a0aa136355f097a41cc127e51d5415cab2b1` |
| `454dee692375.stdout.txt` | 11511 | `7873566c4c95374be4306b5d6461dd717eb7508c251b46c20d2d8070f5ab92d4` |
| `454dee692375.stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Receipt keys are exactly the requested set: `{argv, tool_rev, tool_sha256, rev, exit, stdout_sha256,
stderr_sha256, started_utc, ended_utc}` (`.ufo/waves/round-19/gen-wave1.py:57-59,99-100`). Example (`9011581`):
`argv = ["python3","-I","-B","/tmp/kr19-sb-tool/routed-defects.py","--root",
"/tmp/kr19-StrictBaselineReceipts","--rev","9011581d84527ba34c675f9cf912e54d2e72d470","--strict"]`,
`exit=1`, `tool_rev=a245bb00…`, `started_utc=2026-10-20T18:38:02.267761Z`,
`ended_utc=2026-10-20T18:38:02.507916Z`; `454dee6`: `started_utc=…18:38:02.508160Z`, `ended_utc=…18:38:03.094318Z`.
A self-check recomputed every file digest, name/rev agreement, argv↔rev equality, `--strict` presence, tool digest,
and the exit rule: `RECEIPT_SELFCHECK: CLEAN`, exit 0.

Patch (per `Writers`, contract `:14`): `.ufo/waves/round-19/w1/patches/StrictBaselineReceipts.patch`,
sha256 `ec53f1c31be4b16d12c4a4f3f346d0da6c0296a0a50286e71c479d9008e2176a`. `git diff --cached --stat B`:

```
 .../strict-baseline/454dee692375.receipt.json      |  21 ++
 .../strict-baseline/454dee692375.stderr.txt        |   0
 .../strict-baseline/454dee692375.stdout.txt        | 302 +++++++++++++++++++++
 .../strict-baseline/9011581d8452.receipt.json      |  21 ++
 .../strict-baseline/9011581d8452.stderr.txt        |   0
 .../strict-baseline/9011581d8452.stdout.txt        | 296 ++++++++++++++++++++
 6 files changed, 640 insertions(+)
```

`git apply --check` on a second fresh clone at `8a8da7e…` → exit 0; `git apply` → exit 0; the six applied files
re-hash to the values above (empty files included). No `__pycache__`, `.pyc`, or files outside the assignment are
in the patch. Integration: `git -C LANE apply .ufo/waves/round-19/w1/patches/StrictBaselineReceipts.patch`
(new directory only; touches no existing file).

## Selftest (required paste)

```
$ python3 -I -B /tmp/kr19-sb-tool/routed-defects.py --selftest
SELFTEST: CLEAN cases=17
exit 0
```

## Commands run (all, with exits)

| command | exit |
|---|---|
| `git clone -q --no-hardlinks LANE /tmp/kr19-StrictBaselineReceipts && git -C … checkout -q --detach 8a8da7e… && git -C … rev-parse HEAD` (→ `8a8da7e…`) | 0 |
| `git -C LANE show a245bb00…:.ufo/waves/round-18/tools/routed-defects.py \| head -120` | 0 |
| `git -C LANE show a245bb00…:<tool> \| sed -n '120,240p'` and `\| sed -n '1003,1060p;1280,1340p'` | 0 / 0 |
| `git -C LANE show a245bb00…:<tool> \| grep -n 'def main\|add_argument\|def _selftest\|SELFTEST\|argv'` | 0 |
| rev check `git cat-file -t` for `9011581…`, `454dee6…`, `a245bb00…` in clone (→ all `commit`) + `git show a245bb00…:<tool> \| sha256sum` | 0 |
| `git -C clone show a245bb00…:<tool> > /tmp/kr19-sb-tool/routed-defects.py && sha256sum … && wc -l` (→ 1332 lines, `b004c3ed…`) | 0 |
| `python3 -I -B /tmp/kr19-sb-tool/routed-defects.py --selftest` | 0 (`CLEAN cases=17`) |
| `python3 -I -B /tmp/kr19-sb-run.py` (driver: both strict runs + receipt/stdout/stderr writes) | 0 (tool exits 1, 0 recorded) |
| `python3 -c` summarize both stdout JSON + `sha256sum *.stdout.txt *.stderr.txt *.receipt.json` | 0 |
| rerun strict `--rev 9011581…` → `/tmp/kr19-sb-rerun-9011581.json`; `sha256sum` | 1; digest equals first run |
| rerun strict `--rev 454dee6…` → `/tmp/kr19-sb-rerun-454dee6.json`; `sha256sum` | 0; digest equals first run |
| `git status --porcelain` (→ `?? .ufo/waves/round-19/`) + `find …strict-baseline -type f` | 0 |
| `git add -A && git diff --cached --binary 8a8da7e… > …/patches/StrictBaselineReceipts.patch` + `diff --cached --stat` + `sha256sum patch` | 0 |
| `git clone … /tmp/kr19-sb-applycheck && checkout 8a8da7e… && git apply --check <patch>` | 0 |
| `git apply <patch>` + `ls -la` + `sha256sum` applied files | 0 (digests match) |
| ancestry: `git merge-base --is-ancestor 9011581… 454dee6…`; `… 454dee6… 8a8da7e…`; `git log -1 --format=…` for the three revs | 0/0/0; both ancestries yes |
| `grep -rn 9011581 SCORECARD.md corpus/lessons/round-18.md .ufo/waves/round-18/*.md` | 0 |
| `git show 454dee6… --stat --format=…` + `git diff --stat 454dee6… a245bb00… -- <tool>` (→ no output: tool identical) | 0 |
| receipt self-check (`python3 - <<'PY' …`) | 0 (`RECEIPT_SELFCHECK: CLEAN`) |
| non-strict control `--rev 9011581…` (no `--strict`) | 0 (`open_count` 6, stdout sha `48266a3e…`) |

No installs (no pacman/uv/npx), no REA/Ghidra run, no carrier executed, no `jj`, no LANE working-tree write except
this report and the patch file.

## Risks and limits

- [observation] Receipt `argv` records the ephemeral extraction path `/tmp/kr19-sb-tool/routed-defects.py` and the
  clone path; reproducibility rests on `tool_rev` + `tool_sha256` (the blob is not retained in the patch, keeping it
  to the requested six files). Recreate with
  `git -C LANE show a245bb00c581ae3423a10a055c77d4bc873918df:.ufo/waves/round-18/tools/routed-defects.py` and check
  sha256 `b004c3ed…`.
- [observation] The tool at `a245bb00` (extraction rev) is byte-identical to the tool at `454dee6`
  (`git diff --stat` empty), so the closure rev was evaluated by exactly the tool revision in the receipt.
- [inference] Commit subjects (`9011581` = round-17 spot-check; `454dee6` = post-integration verification pass) and
  ancestry (both `yes`) support reading the pair as pre-closure → post-closure; the receipts assert only the counts
  and exits, not that interpretation.
- [observation] Exit 1 is exclusively from `--strict`: non-strict at `9011581` produced identical stdout with exit 0.
- No blockers. Evidence exists in the lane only after the L1 applies the patch (contract `:17` forbids writing the
  LANE tree); apply order is independent of other seats (new directory, no existing file touched).
