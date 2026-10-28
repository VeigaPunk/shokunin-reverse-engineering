# Round-48 SOURCES append — draft for the L1

Seat `ScribeSources`, wave w1.

**Registry tail (live worktree, read 2026-10-28T18:55Z): last id is S146, not S144.** Committed
HEAD ends at S144 (`caafeffa`); the uncommitted worktree `corpus/SOURCES.md` diff already appends
**S145** (SEP Popper, falsifiability/demarcation, `mined`) and **S146** (sysexits(3) man page,
`rejected`, 404) and an untracked `corpus/lessons/round-48.md` already carries the matching
`## Gate` rows. Counted rows: 146
(`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 146).

Because those rows are uncommitted L1 staging, they are ground truth for id continuation but not
for conflict resolution: this draft appends **S147/S148**, the next free ids, and if the L1 drops
its own pair the renumbering is mechanical (S147→S145, S148→S146). Both of this seat's picks are
new URL families, disjoint from S145/S146.

## Rows to append under `## Registry`

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S147 | Python `exec()` builtin documentation — https://docs.python.org/3/builtins/functions.html#exec (served from https://docs.python.org/3/library/functions.html, HTTP 301 → `3/builtins/functions.html`) | docs | A | `exec`'s accepted input types — a source string or a code object — the primitive `tools/round-48/record2.py`'s oracle clause uses to run `tools/round-47/record.py` from `git show <rev>` bytes; not module resolution, not the security warning's consequences, not `eval`/`compile` semantics | fetched 2026-10-28T18:51Z, HTTP 200, 331,328 B, sha256 `41a0311cc1d5a7dcdeba4fe80a9ffda90c770b77e1a30b4434502f62a118c084`; anchor `#exec`; signature `exec(source, /, globals=None, locals=None, *, closure=None)` | `exec` runs code the caller already holds as a string or code object, so a counter can execute exactly the committed bytes it fetched with no path or module lookup to resolve into the worktree — the mechanism R47-CL1's "execute committed bytes, not worktree" needs | mined | 2026-10-28 | on-release | corpus/lessons/round-48.md |
| S148 | Python `runpy` documentation — https://docs.python.org/3/library/runpy.html | docs | C | candidate grounding for the R48-C2 oracle-execution primitive, refused because every runpy entry point resolves code by filesystem path or import module name | fetched 2026-10-28T18:51Z, HTTP 200, 38,257 B, sha256 `69465f0d5587d68437b735018335ddbc8db625122e36453a928259ce59b56bde`; `runpy.run_module(mod_name, …)` "first located using the standard import mechanism", `runpy.run_path(path_name, …)` "Execute the code at the named filesystem location"; the token `exec` occurs 0 times in the rendered text | REJECTED: a path or module name is exactly the worktree-execution indirection R47-CL1 routed, so runpy cannot ground an execute-from-committed-bytes clause; flip: an edition that accepts a source string or code object directly | rejected | 2026-10-28 | on-release | corpus/lessons/round-48.md |

## `## Gate` additions for `corpus/lessons/round-48.md`

The untracked lesson already has `## Gate` → `### Sources opened this round` with S145/S146 rows.
The block below is the continuation the L1 merges (or drops with this seat's pair).

```markdown
| S147 | https://docs.python.org/3/builtins/functions.html#exec (via https://docs.python.org/3/library/functions.html, 301 → `3/builtins/functions.html`; sha256 `41a0311cc1d5a7dcdeba4fe80a9ffda90c770b77e1a30b4434502f62a118c084`) | 2026-10-28 | "This function supports dynamic execution of Python code. source must be either a string or a code object." (18 words) | **admit** (tier A, `mined`). Grounds R48-C2's oracle clause: `tools/round-48/record2.py:62-71` reads `git show <rev>:tools/round-47/record.py` and runs `exec(compile(body, ORACLE, "exec"), ns)` — the committed bytes themselves, never the worktree file (R47-CL1). |
| S148 | https://docs.python.org/3/library/runpy.html (HTTP 200, 38,257 B, sha256 `69465f0d5587d68437b735018335ddbc8db625122e36453a928259ce59b56bde`) | 2026-10-28 | "Execute the code at the named filesystem location and return the resulting module's globals dictionary." (15 words) | **reject** (tier C, `rejected`). Reason: every entry point resolves a path or module name — the worktree-execution indirection R47-CL1 routed; the rendered text contains no `exec` token and no from-bytes primitive. Flip: an edition that accepts a source string or code object directly. |

- **Census before → after this pair:** 146 → 148
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`), one admitted, one rejected.
  Status / recheck / used-by changes to existing rows: none.
```

## Rejected-row note

The prompt reads "status `mined`" over both rows; the rejected row takes `rejected` instead,
matching the S144/S146 convention (a rejected row's status column is its verdict). Its `used-by`
still names `corpus/lessons/round-48.md` per the prompt, since the Gate records the rejection —
unlike S144/S146's `—`, a defensible difference if the L1 prefers `—`.
