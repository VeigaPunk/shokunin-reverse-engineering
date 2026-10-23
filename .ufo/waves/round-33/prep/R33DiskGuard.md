# Round 33 prep — R33DiskGuard

**Report UTC:** 2026-10-23T08:16:09Z. Tool execution receipts below are exact: selftest 08:16:03Z, explicit-file scan 08:16:03Z, retained-pointer check 08:14:14Z.
**Seat:** R33DiskGuard (leaf executor).
**Axes:** audit recall for the disk directive; lexical precision; retained-evidence preservation; bounded read-only execution.
**Base:** `428315a8f5674b952def862910af6e07a6c2224b` (prep contract).
**Corrections:** `--selftest` now runs 14 lexical + 3 outer CLI cases; the appended sections supersede the earlier 14/14 count, argv, tool size, and digests, and pin fixture writes to the authorized scratch root.

## Result

Authored `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/disk_guard.py`, a small stdlib-only Python command-audit tool. It reads only explicit UTF-8 transcript/receipt paths given on argv (never a recursive scan), detects unqualified `find`/`du` invocations whose same simple-command arguments contain `/fast/scratch`, accepts exactly `/usr/bin/find` and `/usr/bin/du`, and ships a built-in `--selftest`.

The required selftest ran **14/14 PASS, exit 0** at **08:16:03Z**. An explicit-file scan over one retained round-32 receipt and two clean controls ran at **08:16:03Z** with **exit 1**, returning exactly two RED `bare-find` hits at `A2AttemptForensics.md:79` and `:80`; both controls yielded zero hits. No `/fast/scratch` directory walk, no `find`/`du` execution over `/fast/scratch`, no Git/JJ write, and no package/tool install or update occurred.

## Tool

| Item | Value |
|---|---|
| Path | `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/disk_guard.py` |
| SHA-256 | `52aeb5742f5d29cd7418cff23701f69fc9b3a66b07ce15835addc32f73f97177` |
| Size / lines | 7,997 bytes / 234 lines |
| Interpreter | Python 3.14.8, invoked `python3 -I -B` |
| Invocation | `python3 -I -B disk_guard.py FILE [FILE ...]` or `python3 -I -B disk_guard.py --selftest` |
| Install/update | none; no package manager, no `uv`, no remote fetch |

**Input model.** Files are explicit regular-file paths. There is no directory recursion, no glob expansion, no `/fast` walk, and no use of `find`/`du` by the tool. Non-regular paths and non-UTF-8 inputs produce `ERROR` and exit 2. Files are opened read-only and decoded strict UTF-8.

**Detection semantics.**

- Command tokens are matched lexically: bare `find`/`du` (including after `sudo`, `env`, `time`, backticks, pipes, or a bullet) are RED `bare-*`; path-qualified forms beginning with `/`, `./`, `../`, or `~/` that are not exactly the accepted paths are RED `other-path-*`; exactly `/usr/bin/find` and `/usr/bin/du` are GREEN `absolute-*`. Relative multi-segment paths without a dot prefix (`bin/find`) are not recognized and are named as a scope limit.
- A hit requires `/fast/scratch` as a path-segment-bounded argument in the remainder of the same simple command, cut at `;`, `&&`, `||`, `|`, or a backtick. Options may precede the path (`du --max-depth=1 /fast/scratch`).
- `/fast/scratchpad` is not a hit; `/fast/scratch` followed by `/`, whitespace, quote, end, or shell punctuation is a hit.
- Backslash continuations are joined and reported at the first physical line number.
- Exit precedence: `0` no red, `1` red hit(s), `2` could-not-evaluate (usage, non-regular file, non-UTF-8). Errors dominate red.

**Built-in selftest matrix (all PASS).** Red: `red-literal-find`, `red-literal-du`, `red-env-wrapper`, `red-relative-path`, `red-du-option`, `red-after-and`, `quoted-prose-limitation`, `joined-continuation`. Green: `green-absolute-find`, `green-absolute-du`, `green-unrelated-path`, `green-prefix-boundary`, `green-prose-slash-compound`, plus the GREEN half of `green-red-mixed`. The exact ordered results are in the receipt stdout below.

## Selftest receipt

- Receipt: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-receipt.txt`, SHA-256 `cacd8f9ce1dc559db43a4734259923b777e8d9a6e4612e91e35978fd03353700`.
- Raw stdout: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest.stdout.txt`, SHA-256 `9aa37e59e495dcc9781a9e8ae1f9cc028ba3d8be7d9bb13b7c519a67c8a6e468`.
- Raw stderr: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest.stderr.txt`, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty).
- Exact argv: `timeout --kill-after=5s 60 python3 -I -B disk_guard.py --selftest`; cwd `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard`; exit `0`.

```text
LIMITATION	quoted-prose	quoted-prose limitation: the scan is lexical, so a command quoted, echoed, commented, or cited in prose is indistinguishable from an executed command. RED hits can be false positives, and GREEN lines do not prove execution.
LIMITATION	scope	scope limitation: only an explicit /fast/scratch argument in the same simple command is seen; cwd (cd /fast/scratch && find .), variables, aliases, and command substitution are not resolved.
SELFTEST	PASS	red-literal-find	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	red-literal-du	[(1, 'RED', 'bare-du')]
SELFTEST	PASS	green-absolute-find	[(1, 'GREEN', 'absolute-find')]
SELFTEST	PASS	green-absolute-du	[(1, 'GREEN', 'absolute-du')]
SELFTEST	PASS	green-unrelated-path	[]
SELFTEST	PASS	green-prefix-boundary	[]
SELFTEST	PASS	red-env-wrapper	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	red-relative-path	[(1, 'RED', 'other-path-find')]
SELFTEST	PASS	red-du-option	[(1, 'RED', 'bare-du')]
SELFTEST	PASS	red-after-and	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	green-red-mixed	[(1, 'GREEN', 'absolute-du'), (1, 'RED', 'bare-du')]
SELFTEST	PASS	quoted-prose-limitation	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	joined-continuation	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	green-prose-slash-compound	[]
SELFTEST SUMMARY	cases=14	pass=14	fail=0
RESULT	PASS
```

## Explicit-file scan receipt

- Receipt: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/scan-receipt.txt`, SHA-256 `b7f6acd79ae2f70b87c4bdd46ead6e72ab39f8fde9f7b31eb19647d4c8205d7b`.
- Raw stdout: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/scan.stdout.txt`, SHA-256 `18cdcabc90ec61cf256d4913582d8c1ec7d6490003100b14548daa1940778b73`; raw stderr empty.
- Exact argv: `timeout --kill-after=5s 60 python3 -I -B disk_guard.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2AttemptForensics.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2NoHarmBaseline.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-33/prep-contract.txt`
- Exit `1`; summary `files=3 lines=159 hits=2 red=2 green=0 errors=0`.

| Input | Lines (tool) | SHA-256 before | SHA-256 after | Unchanged |
|---|---:|---|---|---|
| `.ufo/waves/round-32/a2audit/A2AttemptForensics.md` | 88 | `122b1ddd09d0c31f22f17affd1edd305f0ca472edb45e8b9c172e9c511dcd5b2` | same | yes |
| `.ufo/waves/round-32/a2audit/A2NoHarmBaseline.md` | 65 | `a6a2325792ae5f2a92a334cf6f4759af2b8fa6887dd6a07912fa79ac19307a52` | same | yes |
| `.ufo/waves/round-33/prep-contract.txt` | 6 | `883c057fa46113e172789ec0570fcb983dc4c62186eb250de2e3d4d8abe35682` | same | yes |

```text
LIMITATION	quoted-prose	quoted-prose limitation: the scan is lexical, so a command quoted, echoed, commented, or cited in prose is indistinguishable from an executed command. RED hits can be false positives, and GREEN lines do not prove execution.
LIMITATION	scope	scope limitation: only an explicit /fast/scratch argument in the same simple command is seen; cwd (cd /fast/scratch && find .), variables, aliases, and command substitution are not resolved.
RED	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2AttemptForensics.md:79	bare-find	- `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1DoNothing /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1JunkRow /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1IdRotated /fast/scratch/hyaku/kaidoku-r32/seats/w1/MutC1Counter -type f !...
RED	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/a2audit/A2AttemptForensics.md:80	bare-find	- `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1DoNothing/clone/.git /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1JunkRow/clone/.git /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1IdRotated/clone/.git -type f -printf '%p\n' | wc -l...
SUMMARY	files=3	lines=159	hits=2	red=2	green=0	errors=0
RESULT	FAIL
```

The two controls (the round-32 no-harm baseline and the round-33 prep contract containing `du/find` prose) produced no hits. The two RED hits are the retained round-32 forensics commands, not a new violation.

## Preserved red round-32 forensics evidence pointer

- Red command evidence: `.ufo/waves/round-32/a2audit/A2AttemptForensics.md:79` and `:80` retain the two literal unqualified `find /fast/scratch/...` inventory commands; current SHA-256 `122b1ddd09d0c31f22f17affd1edd305f0ca472edb45e8b9c172e9c511dcd5b2`.
- The same report at `:81` preserves retention pointers `artifact://779` (20,336 worktree-file hashes) and `artifact://1165` (11,094 `.git` metadata-file hashes). At `:83` it records the scratch index `w1-discard-sha256-index.txt` with SHA-256 `e4a25c09d24f88656de9ead24fe3444a206c50be512fe88890a63ad356edf711`.
- The fleet round-32 report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-32/kaidoku.md:145` records the M32-4 limit: `A2AttemptForensics` used scoped `find` under inherited scratch contrary to the disk directive; that inventory supports no claimed outcome.
- Pointer re-check at 08:14:14Z: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2AttemptForensics/w1-discard-sha256-index.txt` exists, size 1,781 bytes, SHA-256 `e4a25c09d24f88656de9ead24fe3444a206c50be512fe88890a63ad356edf711`, matching the recorded hash. Receipt `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/pointer-check-receipt.txt`, SHA-256 `571d30bc305fff325848477c2a9c1695440132378837c54c26669ce619f65654`, exit 0.
- **No cleaning of old history:** no round-32 file, scratch directory, index, report, or artifact was deleted, renamed, or rewritten by this seat. The only old-scratch access was the explicit `stat`/`sha256sum` on the cited index. The new work is confined to one new round-33 scratch directory and this report.

## Limitations

- **Quoted-prose limitation (named in tool output and selftest):** the scan is lexical. A command quoted, echoed, commented, or cited in prose (including a report's fenced evidence block) is indistinguishable from an executed command. RED hits can be false positives; GREEN lines do not prove execution.
- **Scope limitation (named in tool output):** only an explicit `/fast/scratch` argument in the same simple command is detected. `cd /fast/scratch && find .`, shell variables, aliases, functions, scripts, and command substitution are not resolved.
- **Command-position limitation:** the detector does not fully parse shell grammar. A target word used as another command's argument (for example `grep find /fast/scratch`) can be flagged; a target invoked through a wrapper that separates it from the path by a pipeline or subshell can be missed.
- **Path-form limitation:** relative multi-segment path commands without a leading `/`, `./`, `../`, or `~/` (for example `bin/find /fast/scratch`) are not matched at all; such a transcript would need an explicit path or a bare/absolute invocation to be visible.
- **Boundary semantics:** `/fast/scratchpad` is intentionally not a hit; `/fast/scratch` inside an unrelated string, URL, or quoted path can be flagged if a target command token precedes it.
- **Green is not an execution receipt:** `/usr/bin/find` and `/usr/bin/du` are accepted lexically only; no process, argv, exit status, or path traversal is observed.
- **Selftest is in-memory:** `--selftest` exercises `audit_text` cases, not file opening, UTF-8 rejection, or exit-2 error paths. File mode is exercised once by the explicit-file scan receipt above. The empty-stderr and usage-error paths are not separately asserted.
- **Do not scan this report as a transcript:** this report quotes the forbidden forms in its tool description, selftest stdout, and scan stdout. A self-scan would produce expected quoted-prose false positives.
- **Read-only and bounded:** the tool never executes `find`/`du`; the scan read three files totaling 159 logical lines. No directory walk or `/fast/scratch` inventory was performed.

## Pins and artifacts

| Artifact | Value |
|---|---|
| Tool | `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/disk_guard.py`; SHA-256 `52aeb5742f5d29cd7418cff23701f69fc9b3a66b07ce15835addc32f73f97177`; 7,997 bytes; 234 lines |
| Selftest receipt | SHA-256 `cacd8f9ce1dc559db43a4734259923b777e8d9a6e4612e91e35978fd03353700`; exit 0; 14/14 PASS |
| Scan receipt | SHA-256 `b7f6acd79ae2f70b87c4bdd46ead6e72ab39f8fde9f7b31eb19647d4c8205d7b`; exit 1; 2 RED / 0 GREEN / 0 errors |
| Pointer check receipt | SHA-256 `571d30bc305fff325848477c2a9c1695440132378837c54c26669ce619f65654`; exit 0 |
| Contract | `883c057fa46113e172789ec0570fcb983dc4c62186eb250de2e3d4d8abe35682` |
| r32 forensics | `122b1ddd09d0c31f22f17affd1edd305f0ca472edb45e8b9c172e9c511dcd5b2` |
| r32 index pointer | `e4a25c09d24f88656de9ead24fe3444a206c50be512fe88890a63ad356edf711` |
| Versions | Python 3.14.8; GNU findutils 4.11.0-modified and GNU coreutils 9.12 (version checks only; no `find`/`du` over `/fast/scratch`) |
| Installs/updates | none |

**Files written:** `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/{disk_guard.py,selftest.stdout.txt,selftest.stderr.txt,selftest-receipt.txt,scan.stdout.txt,scan.stderr.txt,scan-receipt.txt,pointer-check-receipt.txt}` and this report. No production/lane file, LOG, SKILL, SCORECARD, QUALITY, SOURCES, Git, or JJ state was modified.

## Correction — outer CLI selftest (appended 2026-10-23T08:23:10Z)

**Supersedes:** the earlier 14/14 helper-only selftest statement, its argv/receipt/stdout digests, and the pre-correction tool size/digest in the "Selftest receipt" and "Pins and artifacts" sections. The 14 lexical cases are retained unchanged; the durable selftest receipt and raw stdout files were overwritten by the extended run. The explicit-file scan receipt was not rerun.

The gate standard's self-test clause (`.ufo/waves/round-12/exec-gate-standard.md:18-25`) requires isolated-fixture self-invocation asserting both the exit code and a stable expected finding token; a helper-only self-check does not satisfy it. `--selftest` now creates a unique fixture tree under `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-fixtures-*` with `tempfile.mkdtemp`, writes tiny UTF-8 fixture files, invokes the same script's normal CLI with `subprocess.run([...], timeout=30)`, and removes the tree in `finally` with `shutil.rmtree`. A cleanup failure fails the selftest. The outer run was bounded by `timeout --kill-after=5s 60`.

| Outer case | Fixture / target | Child exit | Asserted finding rows | Child RESULT |
|---|---|---:|---|---|
| `outer-red-literal-find` | `red-literal-find.txt` = `find /fast/scratch/hyaku -maxdepth 1` | 1 | exactly `RED <fixture>:1 bare-find` | `FAIL` |
| `outer-green-absolute` | `green-absolute.txt` = `/usr/bin/find /fast/scratch/hyaku -maxdepth 1` then `/usr/bin/du -sh /fast/scratch/hyaku` | 0 | exactly `GREEN <fixture>:1 absolute-find`, `GREEN <fixture>:2 absolute-du`; no RED | `PASS` |
| `outer-missing-file` | nonexistent `missing-file.txt` | 2 | no RED/GREEN rows; exact `ERROR <fixture> not a regular file` | `ERROR` |

Each case asserts the child return code, the exact ordered `(kind, path:line, rule)` rows, the child `RESULT` row, and (for the missing-file case) the exact ERROR row. The stable expected finding token is the rule column (`bare-find`), the same finding name used in the earlier tables.

**Result:** **17/17 PASS (14 lexical + 3 outer), cleanup PASS, exit 0** at **2026-10-23T08:22:57Z**.

- New tool: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/disk_guard.py`; SHA-256 `a7253d24a3e2fa848ec472bf5be388c5df78e7c48a989373c87956ee89a40573`; 12,784 bytes; 374 lines.
- New selftest receipt: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-receipt.txt`, SHA-256 `c638037a72ba2b8117e70c51fb785d097b0ba81da9a5a947a774a7e11fa8578b`; raw stdout SHA-256 `40136f5ec6419179fe690fc816b7ea6745bb1f154370ea7577210a6d4a7284d9`; raw stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty); exit `0`.
- Exact argv: `timeout --kill-after=5s 60 python3 -I -B disk_guard.py --selftest`; cwd `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard`.
- The explicit-file scan receipt `b7f6acd79ae2f70b87c4bdd46ead6e72ab39f8fde9f7b31eb19647d4c8205d7b` remains the historical pre-extension run and was not rerun per instruction. This extension edits only `--selftest`/outer helpers, imports, the timeout constant, and the docstring; the scan-path functions and regexes were not edited.
- Current limitation remains: quoted-prose lexical false positives and GREEN non-proof; same-simple-command explicit-path scope; cwd/variables/aliases/functions/command substitution unresolved; relative multi-segment paths not recognized; command-position parsing incomplete. The 3 outer cases exercise the CLI exit/finding contract, not the full shell surface.

**Extended selftest stdout (exact, from the receipt):**

```text
LIMITATION	quoted-prose	quoted-prose limitation: the scan is lexical, so a command quoted, echoed, commented, or cited in prose is indistinguishable from an executed command. RED hits can be false positives, and GREEN lines do not prove execution.
LIMITATION	scope	scope limitation: only an explicit /fast/scratch argument in the same simple command is seen; cwd (cd /fast/scratch && find .), variables, aliases, and command substitution are not resolved.
SELFTEST	PASS	red-literal-find	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	red-literal-du	[(1, 'RED', 'bare-du')]
SELFTEST	PASS	green-absolute-find	[(1, 'GREEN', 'absolute-find')]
SELFTEST	PASS	green-absolute-du	[(1, 'GREEN', 'absolute-du')]
SELFTEST	PASS	green-unrelated-path	[]
SELFTEST	PASS	green-prefix-boundary	[]
SELFTEST	PASS	red-env-wrapper	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	red-relative-path	[(1, 'RED', 'other-path-find')]
SELFTEST	PASS	red-du-option	[(1, 'RED', 'bare-du')]
SELFTEST	PASS	red-after-and	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	green-red-mixed	[(1, 'GREEN', 'absolute-du'), (1, 'RED', 'bare-du')]
SELFTEST	PASS	quoted-prose-limitation	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	joined-continuation	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	green-prose-slash-compound	[]
OUTER	PASS	outer-red-literal-find	exit=1	hits=[('RED', '/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-fixtures-rvo7owqk/red-literal-find.txt:1', 'bare-find')]
OUTER	PASS	outer-green-absolute	exit=0	hits=[('GREEN', '/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-fixtures-rvo7owqk/green-absolute.txt:1', 'absolute-find'), ('GREEN', '/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-fixtures-rvo7owqk/green-absolute.txt:2', 'absolute-du')]
OUTER	PASS	outer-missing-file	exit=2	hits=[]
CLEANUP	PASS	/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-fixtures-rvo7owqk
SELFTEST SUMMARY	lexical=14	outer=3	cases=17	pass=17	fail=0	cleanup=PASS
RESULT	PASS
```

## Correction — fixed authorized scratch fixture root (appended 2026-10-23T08:25:49Z)

**Scope fix:** `_cli_selftest` previously used `dir=os.path.dirname(script)`, which would place fixtures inside the install/live tree after the tool ships. It now uses the fixed authorized scratch root `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard` (`_SELFTEST_ROOT`), created with `os.makedirs(..., exist_ok=True)`; `tempfile.mkdtemp(prefix="selftest-fixtures-", dir=_SELFTEST_ROOT)` creates a unique child per run, and cleanup removes only that child. An inline comment states the no-live-tree-write rule. Scan mode remains read-only.

- New source file: `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/disk_guard.py`; SHA-256 `e61217206fe2a815ff3a2316e87370bfa430a6268900c108ee76f941de8d7f67`; 13,252 bytes; 381 lines. The prior source digest was `a7253d24a3e2fa848ec472bf5be388c5df78e7c48a989373c87956ee89a40573`.
- No selftest was rerun per instruction; only an `ast.parse` syntax check was performed. The 17/17 PASS receipt `c638037a72ba2b8117e70c51fb785d097b0ba81da9a5a947a774a7e11fa8578b` and its embedded fixture path remain the pre-scope-fix run, and its `TOOL_SHA256` is superseded by this source digest. L1 final verification is to run the installed copy once.
- The scope fix changes the fixture-root constant/selection, creation comment, and related docstrings; the 14 lexical cases, 3 outer assertions, exit/finding contract, and scan-path functions/regexes are unchanged.
- Current limitation remains: quoted-prose lexical false positives and GREEN non-proof; same-simple-command explicit-path scope; cwd/variables/aliases/functions/command substitution unresolved; relative multi-segment paths not recognized; command-position parsing incomplete. The outer cases exercise the CLI exit/finding contract, not the full shell surface.

Report: `.ufo/waves/round-33/prep/R33DiskGuard.md`
