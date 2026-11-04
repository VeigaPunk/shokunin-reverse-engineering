# ScoutSource — r72/w1: S275 (`/proc/pid/environ`) warrant + the lane's environ census

Seat: ScoutSource (leaf, one v1 wave, 16 seats). Scope: open `proc(5)` once, locate the
`/proc/pid/environ` paragraph, quote it, check the registry for a duplicate row, and answer
whether any committed lane instrument reads `/proc/self/environ` or records child environments.
Nothing outside this directory and my scratch root was written; no registry byte was appended;
no instrument was edited.

| file | what |
|---|---|
| `.ufo/waves/round-72/w1/ScoutSource.md` | this report |
| `w1/ScoutSource/proc.5.html` | snapshot of `https://man7.org/linux/man-pages/man5/proc.5.html` (31 125 B) |
| `w1/ScoutSource/proc_pid_environ.5.html` | snapshot of the split page that holds the paragraph (7 747 B) |
| `w1/ScoutSource/fetch-receipt.txt` | status / bytes / sha256 / Last-Modified / ETag / access time for both, and why two URLs |
| `w1/ScoutSource/sources-row.md` | the exact 11-cell registry row for S275, insertion point, and the checks on that line |
| `w1/ScoutSource/environ-census.tsv` | every line matched by `grep -rn 'environ' tools/ corpus/`: path, line, family, 200-char evidence |
| `w1/ScoutSource/url-inventory.txt` | every source URL on all 181 registry rows, plus the 19 URLs that already repeat |
| `w1/ScoutSource/guard-proof.txt` | the census/URL guard proof on a scratch fixture (0–3 vs 4 leading spaces) |
| `w1/ScoutSource/shim-idiom-receipt.txt` | the four shim variants, the capsule bytes each recorded, and their digests |
| `w1/ScoutSource/fixture-sources.md` | that fixture |

---

## 1. Fetch evidence (observed, 2026-11-04)

| URL | method | status | bytes | sha256 | Last-Modified | ETag |
|---|---|---|---|---|---|---|
| `https://man7.org/linux/man-pages/man5/proc.5.html` | GET 06:01:39Z | HTTP/1.1 200 | 31 125 | `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` | Mon, 02 Nov 2026 20:20:30 GMT | `"7995-65f50e092bf80"` |
| `https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html` | GET 06:01:59Z | HTTP/1.1 200 | 7 747 | `93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46` | Mon, 02 Nov 2026 20:20:30 GMT | `"1e43-65f50e092bf80"` |

Server `Apache/2.4.58 (Ubuntu)` on both; headers captured with one HEAD each at 06:03:55Z and
06:03:56Z. One GET per page (the byte snapshot), no second body fetch — so byte stability across
fetches is **not** measured here and not claimed.

**The assignment's premise is now stale in one respect.** The served `proc.5.html` no longer
carries the per-file paragraphs: it is a 31 125-byte stub whose only `/proc/pid/environ` content is
a SEE ALSO link at line 386
(`<a href="../man5/proc_pid_environ.5.html">proc_pid_environ(5)</a>`). The strings
`initial environment` and `name=value` do not occur anywhere in that snapshot, while the split page
carries both the paragraph and the `Linux man-pages 6.19  2026-02-08` footline. [INFERENCE: the
per-file split is part of the 6.19 edition the host serves; observed are the stub, its link target,
and the absent text.] The paragraph is on the split page, fetched second (HTTP 200 as above). Both
pages share one `Last-Modified` (a whole-tree rebuild) but have distinct ETags, so the shared date
is not evidence that the text is on the stub.

## 2. The paragraph and the quote

Snapshot `proc_pid_environ.5.html`, page footline `Linux man-pages 6.19  2026-02-08`.
Paragraph: bytes **2465–3712** (0-based, raw HTML), lines **72–91**. Rendered text (tags removed,
line structure as served; the paragraph carries six `<a>` links and three `<i>` elements):

```
          /proc/pid/environ
                This file contains the initial environment that was set
                when the currently executing program was started via
                execve(2).  The entries are separated by null bytes ('\0'),
                and there may be a null byte at the end.  Thus, to print
                out the environment of process 1, you would do:

                    $ cat /proc/1/environ | tr '\000' '\n'

                If, after an execve(2), the process modifies its
                environment (e.g., by calling functions such as putenv(3)
                or modifying the environ(7) variable directly), this file
                will not reflect those changes.

                Furthermore, a process may change the memory location that
                this file refers via prctl(2) operations such as
                PR_SET_MM_ENV_START.

                Permission to access this file is governed by a ptrace
                access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2).
```

**Quoted for the row (18 whitespace-separated words, limit 25), verbatim:**

> This file contains the initial environment that was set when the currently executing program was started via execve(2).

Locator: starts at raw byte **2511** (0-based; 1-based 2512), line **73**, 0-based column 14;
ends at byte 2693; raw span 183 bytes. **A raw byte-substring search for the rendered sentence
fails**, because the sentence carries one anchor — `<a href="../man2/execve.2.html">execve(2)</a>`
starting at byte 2680. In the tag-stripped render the sentence starts at plain-text offset 840.
Second sentence of the paragraph (`The entries are separated by null bytes ('\0'), and there may be
a null byte at the end.`): bytes 2696–2797, line 75; also 18 words.

### The presupposition that does not survive

The assignment says the quote grounds "NUL-separated name=value". Measured: `name=value`,
`name = value`, `NAME=VALUE` occur **0** times in this snapshot (`grep -c` = 0). The page grounds
**NUL separation** and the **optional trailing NUL**; it does not say the entries are `name=value`
pairs. That shape comes from `execve(2)` ("conventionally of the form key=value") or `environ(7)`,
neither of which is a registry row today (`grep -n 'execve' corpus/SOURCES.md` and
`grep -n 'environ.7' corpus/SOURCES.md` both exit 1). The lane's only exec-boundary parser already
depends on it — `tools/round-72/seam-probe.py:200` does `entry.partition(b"=")` — so that split is
currently a capsule-format convention, not a source-grounded kernel property. **Open gap:** register
`execve(2)` (or `environ(7)`) before citing the `=` split as documented.

## 3. Item 4 — what the quote grounds, and its limits

**Grounds.** A read of `/proc/pid/environ` is a read of the environment block the parent installed
at `execve(2)`. So a capsule captured at a child's exec boundary measures the *handing decision*
(the allowlist the caller built), not the child's runtime state. That is exactly the object
`build_child_env()` is supposed to control.

**Limits, all four readable in the same paragraph (so the quote alone is narrower than the page):**

1. The quoted sentence says nothing about **later modifications**; the paragraph's third block does,
   negatively: after an `execve(2)`, `putenv(3)` / direct `environ(7)` modification is **not**
   reflected. A `/proc` read after interpreter start therefore still shows the initial block: a
   reader can see a stale value long after the process changed its environment, and (measured in
   §5) a read issued through a re-exec'd opener can return zero bytes — neither is a caller error.
2. A process may relocate the block via `prctl(2)` `PR_SET_MM_ENV_START`; the kernel may then
   report bytes from a different address range. Nothing in the lane's shims sets it; this is a
   limit of the measurement, not an observation about the lane.
3. Reads are gated by `PTRACE_MODE_READ_FSCREDS`; a failure to read is not evidence of an empty
   environment.
4. The page is about `/proc/pid/environ`, **not** about `os.environ`. An in-process `os.environ`
   view is a different object (libc's copy, order- and duplicate-collapsing, may postdate
   modifications), so a capsule produced by an interpreter's own `os.environ` and one produced from
   `/proc` are not interchangeable evidence. [INFERENCE from the page's "initial environment" +
   "not reflect those changes" pair; the page does not discuss `os.environ`.]

## 4. Item 2 — registry: no duplicate, next free id S275

Commands and results (`.ufo/waves/round-72/w1/ScoutSource/guard-proof.txt`):

- `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → **181 matched rows**;
  numeric max **S274** (`corpus/SOURCES.md:191`); `grep -c 'S275\|S276'` → **0**. Next free id:
  **S275** (S276 stays free).
- URL duplicate: `grep -n 'proc_pid_environ' corpus/SOURCES.md` and
  `grep -n 'man5/proc.5.html' corpus/SOURCES.md` both exit **1**. The three existing `man7.org`
  rows are different pages (S146, S148 `sysexits.h`; S252 `mknod.2`); same host is not a duplicate.
- Row shape: S274 has 11 cells (`awk -F'|'` NF-2 = 11), which is the schema my row satisfies
  (verified the same way on the row itself: 11 cells, 12 pipes, 0 escaped pipes, backticks balanced).

**Guard proof on the fixture (indent tolerance).** `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
matches rows with 0, 1, 2 and 3 leading spaces (S900–S903, 4 matches) and **misses** the 4-space
row S904. The URL scan restricted to census-shaped rows (`^ {0,3}\|.*proc_pid_environ`) therefore
returns **nothing**, while the plain substring scan over all lines finds the 4-space duplicate. So:
the census tolerates 0–3 spaces and silently drops deeper indentation, and a URL-duplicate check
must scan *every* line, not only the lines the census matches. Both behaviours are demonstrated on
`fixture-sources.md` in this directory.

**"Does not duplicate an existing URL" — true here, but URL uniqueness is not a registry invariant.**
`url-inventory.txt` lists every URL on all 181 rows. My URL is absent from it (0 rows). Separately,
**19 URLs already appear on 2–7 rows**: e.g. `https://github.github.com/gfm/` on S258 and S273,
the unblob squashfs handler URL on S108/S112/S245, the rea-agents 6.5.0 tarball on seven rows,
`https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz` on S037/S081. Each of those pairs is
a declared supersession or scope split, not a duplicate row. A validator that rejects a repeated
URL would flag 19 legitimate rows; the usable rule is scope-based (a new row must not restate an
existing row's claim), not URL-based.

## 5. Item 3 — who reads `/proc/self/environ`, and who records child environments

### Direct answer

- **Yes, one committed instrument reads `/proc/self/environ`:** `tools/round-72/seam-probe.py`.
  It is the **only** `/proc` read in the whole lane — the census finds exactly **3** such lines,
  all in that file (docstring at :190, docstring at :280, the shim body at :303 of the current
  working tree).
- **Yes, two committed instruments record child environments by another mechanism:** the observed-
  environment launcher in `tools/round-71/packed-elf.py:299` and `tools/round-72/packed-elf.py:317`,
  which writes `{"argv": …, "env": dict(os.environ)}` (JSON Lines) from inside the child's own
  interpreter.
- **No instrument reads `/proc/<pid>/environ` for another process**, and none captures with
  `printenv`/`env` (every `#!/usr/bin/env` hit is a shebang, family `G_text`). Nothing else in
  `tools/` stores an environment into evidence: the remaining hits are construction/scrubbing.

### Mechanism table (current working tree, 2026-11-04T06:08Z)

| # | site | measure | mechanism |
|---|---|---|---|
| 1 | `tools/round-72/seam-probe.py:303` | raw NUL-separated bytes handed to each PATH-shimmed child (`git`, `readelf`) — the A11 witness | `#!/usr/bin/perl`, `open(my $in,'<','/proc/self/environ')`, dump, then `exec` the real tool |
| 2 | `tools/round-72/seam-probe.py:189-201` (`parse_environ_file`) | capsule → dict, exact bytes | split on `b'\0'`, drop empties, `partition(b"=")`; no decoding of the block |
| 3 | `tools/round-72/packed-elf.py:309-322` (`LAUNCHER`) | child's own environment as its interpreter sees it | `os.environ.pop("PYTHONCOERCECLOCALE")`, write `{"argv","env": dict(os.environ)}`, `execvp` |
| 4 | `tools/round-72/packed-elf.py:351` (`observed_env`) | receipt-facing summary of that log: `keys`, `all_allowlisted`, `home_under_run`, `tmpdir_under_run`, `children` | parses the JSONL, compares `sorted(e) == sorted(CHILD_ENV_KEYS)` where `CHILD_ENV_KEYS = ("HOME","LANG","PATH","TMPDIR")` (:165) |
| 5 | `tools/round-72/capsule-audit.py` + `capsule_audit.py` | R72-C3: re-derives the seven clauses from capsule **bytes**; the producer's summary is never trusted | `capsule_audit.audit(capsule, summary)`; a lying summary fails with a named clause |
| 6 | `tools/round-72/controls.py:78` | the lying shape the audit must reject | injects a false `child_env_observed.log` into a receipt |
| 7 | `tools/round-72/packed-elf.py` `build_child_env`/`child_env_audit` (:210, :226) | the *intended* child environment, four keys, HOME/TMPDIR under work | constructs and describes; does not observe |
| 8 | `tools/round-25/instrument-custody.py:95-123` (`git_environment`) | protects git children from inherited `GIT_*` | copies `os.environ`, drops `GIT_*`, pins `GIT_CONFIG_*`/`GIT_NO_REPLACE_OBJECTS` — scrubs, never records |
| 9 | `tools/round-33/measure_driver.py:451` (`id_probe` stub) | a negative control whose verdict input is the environment | stub reads `os.environ.get(k,'')` for `R33_ID/FIXTURE_ID/EXPECTED/ID` — own-process read, the only instrument where the environment feeds a verdict rather than plumbing |

### Census of the grep (receipt holds every line)

`grep -rn 'environ' tools/ corpus/` → **2 104** output lines, of which **61** name a
`__pycache__` path (bytecode; one extra line merely mentions the directory in its text);
excluding those, **2 043** matched lines in **1 110** files
(`environ-census.tsv`, snapshot 06:08:06Z, with the six round-72 instrument digests in its header;
the working tree moved during this session — `packed-elf.py`'s digest changed between my two scans —
so treat round-72 line numbers as of that instant).

| family | tools/ | corpus/ | what it is |
|---|---|---|---|
| `A_proc_read` | 3 | 0 | the three `/proc/self/environ` lines above |
| `B_env_record` | 41 | 889 | an `"environment"` field in retained evidence / vendored JSON |
| `C_env_mutate` | 7 | 0 | `os.environ.pop`/`update`/`del` — scrubbing the own process before a child runs |
| `D_env_copy_child` | 76 | 0 | `dict(os.environ …)` / `os.environ.items()` filters — building a child environment |
| `E_env_read` | 205 | 43 | `os.environ.get`/`os.environ[...]` — path, HOME, scratch, tool overrides |
| `F_env_pass` | 1 | 0 | `env=self.environment` handed to `subprocess.run` |
| `G_text` | 113 | 654 | prose, comments, shebangs, docstrings |
| `H_binary` | 0 | 11 | byte-blob matches inside the vendored REA tarball |
| **total** | **446** | **1 597** | |

Within `tools/`, **398** hits are in committed instruments and **48** are inside fixture/control
trees (`tools/round-44/control-fixtures`, `tools/round-49/control-fixtures`, `selftest/`,
`oracle/`). Per-round totals (fixtures included, sum 446): r25 12, r26 3, r27 3, r28 3, r29 7,
r30 7, r31 4, r32 2, r33 7, r34 4, r36 7, r37 4, r38 14, r39 13, r40 29, r41 20, r42 28, r43 11,
r44 71, r45 4, r46 1, r49 43, r50 36, r50-c3 1, r51 2, r53 2, r64 1, r65 4, r66 5, r67 7, r69 3,
r70 17, r71 27, r72 44. Corpus: 1 481 in `corpus/evidence/` (vendored bytes; one REA tarball member
alone accounts for 353 lines and a minified JS bundle for 56), 79 in `corpus/knowledge/`, 26 in
`corpus/lessons/`, 11 in `corpus/{README,QUALITY,SOURCES}.md`. No corpus file *executes* anything;
the `E_env_read` corpus hits are quoted code inside knowledge/lesson text.

### The one thing worth acting on: the shim idiom decides what is measured (measured, not read)

The declaration (`6316c10`) and the operative freeze (`34fe7aa`) contain a **shell** shim — line 244
of the declaration revision, 245 of the freeze — and the frozen copies in `ExecC2/` still do:

```python
fh.write("#!/bin/sh\ncat /proc/self/environ > %s\nexec %s \"$@\"\n" % (record, real))
```

Four experiments on this host (`/bin/sh` → `/usr/bin/bash` 5.3.20, Perl 5.44.0), each shim exec'd
by Python `subprocess.run` with exactly `PATH/HOME/LANG/TMPDIR` and nothing else:

| idiom | entries recorded |
|---|---|
| `#!/bin/sh` + `cat /proc/self/environ > f` (declaration/freeze bytes) | **7**: `PATH, HOME, LANG, TMPDIR, PWD, SHLVL, _=/usr/bin/cat` |
| `#!/bin/sh` + `cat /proc/$$/environ > f` | **4**: exactly the passed allowlist |
| `#!/bin/sh` + `cat < /proc/self/environ > f` | **0 bytes** (the shell opens the file in the forked child, which then execs; the read sees nothing) |
| exact committed Perl shim (current `seam-probe.py:301-307`) | **4**: exactly the passed allowlist |

Receipt: `w1/ScoutSource/shim-idiom-receipt.txt` (each shim's source, exit, capsule bytes and digest).
The two correct idioms produced **byte-identical 48-byte capsules** (`sha256 d8cf5bb2…`), which is
the cross-check that the Perl fix measures the same block as the `/proc/$$` control, not merely a
four-key set.

Cause [INFERENCE]: `/proc/self` inside `cat` is **cat's** process, and bash exports `PWD`, `SHLVL`
and `_` into every command it runs, so the shell shim measures the shell's re-exported block one
exec beyond the checker's call. The Perl shim opens the file in the interpreter that *was* the
child, so it sees the exec-boundary block.

**Retained receipts confirm both sides of this** (read-only):

- `.ufo/waves/round-72/l1/pre/c1-at-base.json` (02:58:02) — `A11_checker_env: ok false`; shims
  recorded `["HOME","KAIDOKU_ENV_CANARY","LANG","PATH","PWD","SHLVL","TMPDIR","_"]`,
  `keys_exact: false`, `canary_present: true`. That is my 7-key set **plus the leaked canary**.
- `.ufo/waves/round-72/l1/scores/c1-at-landing.json` (03:03:46) — `A11_checker_env: ok true`;
  shims recorded exactly `["HOME","LANG","PATH","TMPDIR"]`, `keys_exact: true`.
- Commit `6284abeb` (03:03:08) subject: "round-72 supersession 2: the A11 shim is perl (a shell
  adds PWD/SHLVL/_ to the exec boundary) and the battery's scr…" — the same cause, already fixed in
  the working tree before I measured it.

So this is **independent confirmation of a landed fix**, not a new defect. What is still open:

1. The **frozen copies keep the shell idiom**: `ExecC2/seam-probe.frozen.py` (sha256
   `52b98fb1…`, byte-identical to declaration `6316c10:tools/round-72/seam-probe.py`) and
   `ExecC2/seam-probe.freeze.py` (`7f46e3ef…`, byte-identical to operative freeze `34fe7aa`).
   Any mutation battery run against those bytes has a **structurally red A11 baseline** on this
   host — a killed mutant there is not evidence about the current witness, and a survivor is not a
   calibration result. ExecC2's own note already reports one survivor from the frozen battery.
2. Any capsule that shows `keys_exact: true` while claiming to come from the shell shim is
   inconsistent with this measurement (the honest shell-shim capsule has 7–8 entries). That is a
   concrete lying-capsule shape for R72-C3's audit to reject, and for the mutation tester to plant.
3. `parse_environ_file` (:189-201) has no test for a block with an entry lacking `=`; it would map
   such an entry to `key=<empty>` and then fail `keys_exact` (fail-closed, but silently attributed
   to an allowlist breach rather than to a malformed capsule).

## 6. Unknowns and non-claims

- Byte stability of the man7 pages across fetches: **not measured** (one body fetch each).
- `name=value` remains ungrounded until `execve(2)`/`environ(7)` is registered (§2).
- The Perl shim's own environment: Perl does not rewrite its environment block for its own
  `/proc/self`, but it *does* pass an unchanged block to `exec`; I verified the four-key result
  empirically and did not read Perl's source.
- `/proc/$$/environ` and `<`-redirection results are measured on this host's bash only, not
  generalised to another `/bin/sh`.
- No claim about any receipt beyond the four files quoted by path; the wave was editing
  `tools/round-72/*` while this was written (digests in the census header).
