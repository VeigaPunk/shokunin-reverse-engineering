# WDiskOuter — disk-command audit instrument run + A2 text scan

Executor seat, round 33 w1. Axes: instrument fidelity (isolated selftest), scan
classification fidelity (red findings vs clean absolute-command control), and
evidence provenance. This is reachable instrument/repair evidence only. R33-C1 is
stopped unprovable per `.ufo/waves/round-33/claim-stop.json`; nothing here is a
replacement admission benchmark, a revived carrier claim, or a 32-row measurement.

Observed lane revision: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (assignment pin;
base `428315a8`). No Git/JJ command was run, so the pin is cited, not re-derived.

## 1. Instrument identity and invocation

- Installed tool: `tools/round-33/disk-command-audit.py`
  - size 13252 bytes, mode 644, SHA-256
    `e61217206fe2a815ff3a2316e87370bfa430a6268900c108ee76f941de8d7f67`
- Interpreter `/usr/bin/python3` -> `/usr/bin/python3.14`, `Python 3.14.8
  (main, Oct 2 2026, 10:23:31)`; invoked with `-I -B`.
- Outer guard: `/usr/bin/timeout` (GNU coreutils) 9.12, SHA-256
  `629cb6e82df4bb47188eec340f2ceb5f45def2e7b1aac1bd7443beecdcb42a6a`,
  `120s` cap. Internally the tool caps each outer child at 30 s.
- Scratch binaries used: `find (GNU findutils) 4.11.0-modified`, `du (GNU
  coreutils) 9.12`; both `--version` exited 0. No install or update was performed
  by this seat.

Retained argv files are byte-exact (`*.argv.txt` under the seat scratch root).

## 2. Selftest — one run, exit 0, 17/17

Exact argv (`selftest.argv.txt`):

```
timeout 120s /usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/disk-command-audit.py --selftest
```

| Field | Value |
|---|---|
| UTC start | `2026-10-23T09:31:13.682677973Z` |
| UTC end | `2026-10-23T09:31:13.799731279Z` |
| Wall duration | 0.117053306 s |
| Exit | 0 |
| stderr | empty, 0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| stdout | 1921 bytes, SHA-256 `dcc567228ff67fe837dc57bf737ac8c8489e64bad1606c73595dc61c9aa789a8` |

Terminal rows:

```
SELFTEST SUMMARY	lexical=14	outer=3	cases=17	pass=17	fail=0	cleanup=PASS
RESULT	PASS
```

All 14 lexical cases passed, including the two rows that define the
quoted-prose distinction:

```
SELFTEST	PASS	quoted-prose-limitation	[(1, 'RED', 'bare-find')]
SELFTEST	PASS	green-prose-slash-compound	[]
```

All three outer CLI cases passed with the asserted child exits: red literal fixture
exit 1 (`bare-find`), absolute green fixture exit 0
(`absolute-find`+`absolute-du`), missing file exit 2 (`ERROR ... not a regular
file`). `CLEANUP PASS` removed the unique fixture tree
`/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-fixtures-0ch2jp0v`; a
post-run listing of that authorized root contains no `selftest-fixtures-*` entry.

Timing defect disclosed: the first receipt recorded `duration_s=76` from the
shell's `SECONDS` counter. A probe (`SECONDS=0; sleep 2; echo $SECONDS` -> `171`)
shows that counter is inherited/unreset in this temporary shell, so it is invalid.
The UTC start/end difference above is the authoritative duration; the original
`selftest.exit.txt` is retained unmodified and the correction is in
`selftest.timing-correction.txt`.

An earlier `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard/selftest-receipt.txt`
(08:22:57Z) reports the same 17-case battery `RESULT PASS`, but for a different
file, `disk_guard.py` SHA-256 `a7253d24...`. It is not a receipt for the installed
tool above and was not used as this run's evidence.

## 3. Scans — explicit files only, no directory walked

Three explicit-path invocations; no path was a directory. A2 refers to
`.ufo/waves/round-32/a2audit/A2AttemptForensics.md` (12413 bytes, mtime
`2026-10-23T06:54:03.333424805Z`, SHA-256
`122b1ddd09d0c31f22f17affd1edd305f0ca472edb45e8b9c172e9c511dcd5b2`).

| Run | argv | UTC window | Exit | Summary |
|---|---|---|---|---|
| A2 alone | `/usr/bin/python3 -I -B <tool> <A2>` | 09:31:37.363910181–09:31:37.396088138Z | 1 | files=1 lines=88 hits=2 red=2 green=0 errors=0; `RESULT FAIL` |
| clean receipt alone | `/usr/bin/python3 -I -B <tool> <seat>/clean-abs-receipt.txt` | 09:32:15.857843391–09:32:15.885447702Z | 0 | files=1 lines=25 hits=2 red=0 green=2 errors=0; `RESULT PASS` |
| pair | `/usr/bin/python3 -I -B <tool> <A2> <seat>/clean-abs-receipt.txt` | 09:33:03.445104102–09:33:03.477420751Z | 1 | files=2 lines=113 hits=4 red=2 green=2 errors=0; `RESULT FAIL` |

All three exited in under 33 ms; each was wrapped in `timeout 60s`, which never
fired (its exit mirrors the child: 1, 0, 1). stdout digests: A2 run
`622060110a3ea284444c4a5df429c6710bac76935f66040ff913fcb6dd6f517f`, clean run
`b26a58209b02215e0eaca5efb0f9dcc28be3f665c767f9a0c6ca89a8c728f6b1`, pair run
`14b11e7a922203a96e66a2b088dc42d2495dc80a7956aaedd2cb2e49b862fc95`. stderr was
empty for all three.

### 3a. Red findings (A2 lines 79–80, rule `bare-find`)

```
RED	.../A2AttemptForensics.md:79	bare-find	- `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1DoNothing /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1JunkRow /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1IdRotated /fast/scratch/hyaku/kaidoku-r32/seats/w1/MutC1Counter -type f !...
RED	.../A2AttemptForensics.md:80	bare-find	- `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1DoNothing/clone/.git /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1JunkRow/clone/.git /fast/scratch/hyaku/kaidoku-r32/seats/w1/CtlC1IdRotated/clone/.git -type f -printf '%p\n' | wc -l...
```

No other lines hit; the scan reports errors=0. These two commands are recorded in
A2's "Commands, hashes, and provenance" section with returned counts `20336` and
`11094`, not in a prohibition or hypothetical example.

### 3b. Clean absolute-command control

`clean-abs-receipt.txt` (SHA-256
`9254ed978391dd70d73d4f7c3fac9989e3fdfc377eac9fab943e86bc51355bce`, identical
before and after the scan) records two commands this seat actually ran:

```
GREEN	.../clean-abs-receipt.txt:8	absolute-find	$ /usr/bin/find /fast/scratch/hyaku/kaidoku-r33/w1/WDiskOuter -maxdepth 1 -type f -printf '%f\n'
GREEN	.../clean-abs-receipt.txt:22	absolute-du	$ /usr/bin/du -sb /fast/scratch/hyaku/kaidoku-r33/w1/WDiskOuter/abs-fixture.txt
```

`find` exit 0, stdout 11 file names, stderr empty
(`abs-find.start.txt` `09:31:21.818872559Z` / `abs-find.end.txt`
`09:31:21.820225748Z`); `du` exit 0, stdout `127\t<path>` (127 bytes), stderr empty
(`abs-du.start.txt` `09:31:21.820524528Z` / `abs-du.end.txt`
`09:31:21.821700678Z`). The two commands were executed before the receipt was
written, so the `find` listing reflects that earlier file set and does not include
the receipt itself. This is a clean lexical control (`red=0`), not an execution
proof supplied by the scanner.

## 4. Quoted prose vs actual execution

The tool states its own limit verbatim in every run:

> quoted-prose limitation: the scan is lexical, so a command quoted, echoed,
> commented, or cited in prose is indistinguishable from an executed command. RED
> hits can be false positives, and GREEN lines do not prove execution.

The selftest demonstrates both directions: the prohibition sentence "Never run
`find /fast/scratch` from a shell builtin." is `RED bare-find`, while the slash
compound "du/find over /fast/scratch" is green. Therefore the A2 rows cannot be
classified by the scanner; the classification below uses the document's own
record and derivative artifacts.

Classified as **executed inventory records**, not quoted prose:

1. A2 places both lines under "Commands, hashes, and provenance" and pairs each
   with a returned count (`20336`, `11094`) plus completion times
   (`06:48:03Z–06:48:05Z`, `06:49:47Z–06:49:48Z`). A prohibition quote would not
   carry counts or completion times.
2. A2 cites its derived index at
   `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2AttemptForensics/w1-discard-sha256-index.txt`.
   That file exists, is 1781 bytes, has mtime `2026-10-23T06:52:55.430197296Z`,
   and its measured SHA-256
   `e4a25c09d24f88656de9ead24fe3444a206c50be512fe88890a63ad356edf711` equals A2's
   stated value. A2's parenthetical "(hash command output at 06:52:59Z)" is then
   consistent with hashing the index 3.6-4.6 s after it was written (that citation
   is second-granularity).
3. The four cited inventory directories exist (`stat`, not walked) with mtimes
   `06:17:46.135Z` (CtlC1DoNothing), `06:18:44.284Z` (CtlC1JunkRow),
   `06:18:09.895Z` (CtlC1IdRotated), `06:18:28.012Z` (MutC1Counter), matching
   A2's dispatch chronology (first accepted chunk at `06:17:19Z`).
4. A2's "Out of scope / not verified" section lists the gates it did not run; it
   does not retract the scratch inventories.

Limits of that classification: execution is inferred from A2's self-record plus
one derivative file's existence/hash/mtime; the counts `20336` and `11094` were
not reproduced, because reproducing them would require re-running the same bare
command over scratch (prohibited here). No scratch file body was read; only
`stat` metadata and one SHA-256 were taken. Markdown backtick quoting is
formatting, not a claim of non-execution, and it is the only reason the rows are
lexically indistinguishable from prose.

Contextual note, not a verdict on round 32: a text search of the stored
`.ufo/waves/round-32/` metadata for `/usr/bin/(find|du)`, `disk-command-audit`, or
`bare-find` returned no match. The absolute-binary requirement is stated in the
round-33 containment, so these two rows are a lexical RED under the current rule,
not evidence of a then-documented rule breach.

Corollary: retaining the RED snippets verbatim in this report means this report
will itself scan RED. Those lines are quotations of A2's executed commands; this
seat executed no bare `find` or `du` and no directory walk at any point.

## 5. Retained evidence

All under `/fast/scratch/hyaku/kaidoku-r33/w1/WDiskOuter/` (total 10012 bytes):

| File | SHA-256 (or role) |
|---|---|
| `selftest.argv.txt` / `.start.txt` / `.end.txt` / `.exit.txt` | argv + UTC + exit 0 |
| `selftest.stdout.txt` | `dcc567228ff67fe837dc57bf737ac8c8489e64bad1606c73595dc61c9aa789a8` |
| `selftest.stderr.txt` | empty, `e3b0c442...b855` |
| `selftest.timing-correction.txt` | invalid `SECONDS` counter, authoritative wall |
| `a2-scan.argv/stdout/stderr/start/end/exit` | exit 1; stdout `62206011...f517f` |
| `clean-scan.argv/stdout/stderr/start/end/exit` | exit 0; stdout `b26a5820...f6b1` |
| `pair-scan.argv/stdout/stderr/start/end/exit` | exit 1; stdout `14b11e7a...fc95` |
| `clean-abs-receipt.txt` | `9254ed97...55bce` (before = after) |
| `clean-receipt.sha256-before/after.txt` | identical `3ddad47f...` |
| `abs-fixture.txt` | `89c737f4...` (127-byte `du` target) |
| `abs-find.argv/stdout/stderr/start/end/exit` | find exit 0, stderr empty |
| `abs-du.argv/stdout/stderr/start/end/exit` | du exit 0, stderr empty |
| `find.version.txt` / `du.version.txt` | GNU findutils 4.11.0-modified / coreutils 9.12 |

Source artifacts measured read-only: A2 report `122b1ddd...` (12413 bytes), A2
index `e4a25c09...` (1781 bytes), installed tool `e6121720...` (13252 bytes).

## 6. Findings, risks, blockers

- Instrument: installed audit tool passes its isolated contract 17/17 with clean
  fixture cleanup; the lexical red/green rules are reproducible from retained
  stdout.
- Scan: A2 contains exactly two red `bare-find` rows (lines 79–80), both with
  explicit `/fast/scratch` arguments; the clean absolute-command receipt scans
  `red=0`, `green=2`, exit 0. The paired scan reproduces both results in one
  summary.
- Classification risk: RED/GREEN is lexical only. The A2 execution classification
  rests on A2's self-record, one matching derivative hash/mtime, and directory
  mtimes; it does not independently reproduce the inventory counts, and the
  scanner cannot distinguish the quoted rows from prose.
- Measurement risk: the `SECONDS` duration in the first receipt is invalid; the
  UTC difference (0.117 s) is used instead. The selftest shares
  `R33DiskGuard/` with another round-33 tool; no concurrent mutation was observed,
  cleanup removed only its own `mkdtemp` child, and no residue remains.
- The clean receipt proves only a clean lexical result and that this seat's two
  absolute invocations ran; it does not prove execution for any GREEN line in
  another document.
- No blockers for this scoped item. R33-C1 remains stopped and unprovable; no
  fixture manifest, carrier row, or replacement benchmark was created or implied.

## 7. Containment

No access to R33FixtureBuilder artifacts, quarantine contents, or the held item;
no carrier-study manifest or native execution; no REA/MCP, upstream/domain writes,
config/routing edits, or host service changes; no subagents or background jobs; no
lane/fleet Git or JJ writes; no builds/tests/linters/formatters beyond the single
assigned selftest. No bare `find`/`du` and no recursive scratch walk was executed
by this seat; explicit paths were `stat`ed and one index file was hashed without
reading its body. Scratch writes total 10012 bytes, each file well under 1 MiB.
The only lane write is this report.

Report: `.ufo/waves/round-33/w1/WDiskOuter.md`
