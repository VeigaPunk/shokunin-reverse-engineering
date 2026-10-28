# ScribeSources — round-48 SOURCES append draft (scoped findings)

Seat: `ScribeSources` (leaf member, scribe). Deliverable:
`.ufo/waves/round-48/w1/ScribeSources/sources.md` — two registry rows (one admitted, one
rejected) in the 11-column schema plus the `## Gate` block text for the lesson. Receipts copied
to `.ufo/waves/round-48/w1/ScribeSources/receipts/` (fetched page bytes, sha256-manifest below).

## What was drafted

| row | source | verdict |
|---|---|---|
| S147 | Python `exec()` — `docs.python.org/3/builtins/functions.html#exec` | **admit** (`docs`, tier A, `mined`, `on-release`, `used-by corpus/lessons/round-48.md`) — `exec` accepts a source string or code object: the exact primitive `record2.py`'s oracle uses to execute `tools/round-47/record.py` from committed `git show` bytes, grounding the R48-C2 oracle clause and the R47-CL1 "bytes, not worktree" discipline |
| S148 | Python `runpy` — `docs.python.org/3/library/runpy.html` | **reject** (`docs`, tier C) — every runpy primitive resolves a filesystem path or module name, i.e. the worktree-execution indirection R47-CL1 routed; `exec` occurs 0 times in the page. Flip: an edition accepting a source string or code object |

## Key findings for the L1

- **Peer reconciliation (ScribeLesson-2).** It drafted a *different* pair at S145/S146:
  admit `docs.python.org/3/library/argparse.html` (HTTP 200, 334,734 B, sha256 `521adff6…`,
  anchor `exit_on_error`, quote "it will print a message to sys.stderr and exit with a status
  code of 2") and reject `man.openbsd.org/sysexits.3` (HTTP 200, 12,147 B, sha256 `4cf3eb9d…`,
  EX_USAGE is 64 not 2); screened `sys.html` (`867b5a26…`) as not a row. Families are disjoint
  from mine (exec/runpy) and from the L1's staged pair (Popper/sysexits-man7): if the L1 keeps
  all three, ids S147–S152 suffice; if it drops its own pair, renumbering is mechanical.
  Notably the peer's reachable OpenBSD sysexits page *fires the flip condition* the L1's
  rejected S146 recorded ("open `man 3 sysexits` locally or the FreeBSD handbook page and quote
  the `EX_USAGE` line") — the man7 404 row could now be grounded instead of rejected.
- **Converged via ScribeLesson-2.** Its lesson draft
  (`.ufo/waves/round-48/w1/ScribeLesson/lesson.md`) keeps the L1's staged S145/S146, files my
  pair verbatim as S147/S148, adds ScoutSources-4's argparse admit as provisional S149 (scoped
  to `ArgumentParser.error` → exit 2 as a usage refusal), and merges the sysexits mirror
  captures (FreeBSD `51978a07…`, OpenBSD `4cf3eb9d…`, EX_USAGE=64) into S146's flip note rather
  than a second reject row — I checked the table against this draft: identical digests/quotes
  except one transcription slip I flagged (its S147 note writes the 301 direction backwards:
  `library/functions.html` → `builtins/functions.html`, not the reverse).
1. **Id collision, resolved by continuing.** Committed registry tail is S144, but the *uncommitted*
   worktree `corpus/SOURCES.md` already carries S145 (SEP Popper, `mined`) and S146 (sysexits(3)
   man page, `rejected` 404), and an untracked `corpus/lessons/round-48.md` already has the matching
   `## Gate` table. I did **not** touch those files (read-only lane). The draft continues at
   **S147/S148**; if the L1's uncommitted pair is dropped, renumbering is mechanical. My two picks
   are disjoint URL families from S145/S146 — no dup even if all four land.
2. **`functions.html` moved.** `docs.python.org/3/library/functions.html` now returns HTTP 301 →
   `3/builtins/functions.html` (the builtin docs were split). The row's source URL is the final
   page with the `#exec` anchor; the redirect is recorded in the row and Gate entry.
3. **Prompt-vs-schema tension, decided.** "status `mined`" read over both rows conflicts with
   "one rejected row": rejected rows carry `rejected` (S144/S146 convention). S148 uses
   `rejected`; its `used-by` still names the round-48 lesson per the prompt (the Gate records the
   rejection). S144/S146 use `—`; the L1 may prefer `—` for consistency.
4. **Both sources actually fetched** (not fabricated): HTTP 200 each, page sha256 recorded, located
   quotes ≤25 words (18 and 15 words). runpy screened out by direct text scan — no `exec` token,
   `run_module`/`run_path` are name/path resolvers only.

## Receipts (commands run, exits, digests)

All times UTC 2026-10-28. Exit codes: 0 = success throughout; no counter was run (out of scope).

| command | exit | stdout sha256 / artifact |
|---|---|---|
| `bash scripts/hyaku/disk-guard.sh status` | 0 | ran at 18:50Z; output showed scratch idle entries only (no capacity warning) |
| `curl -sS https://docs.python.org/3/library/functions.html` | 0 | HTTP 301, 162 B, sha256 `9e17cb15dd75bbbd5dbb984eda674863c3b10ab72613cf8a39a00c3e11a8492a` |
| `curl -sSL` (final `3/builtins/functions.html`) at 18:51:04Z | 0 | HTTP 200, 331,328 B, sha256 `41a0311cc1d5a7dcdeba4fe80a9ffda90c770b77e1a30b4434502f62a118c084` → `receipts/functions-final.html` |
| `curl -sS https://docs.python.org/3/library/runpy.html` at 18:51:00Z | 0 | HTTP 200, 38,257 B, sha256 `69465f0d5587d68437b735018335ddbc8db625122e36453a928259ce59b56bde` → `receipts/runpy.html` |
| `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | 0 | `146` (live worktree; committed = 144 at `caafeffa`) |
| `git diff corpus/SOURCES.md` / `git status --porcelain` | 0 | showed the uncommitted S145/S146 rows and untracked `corpus/lessons/round-48.md` |
| `git log --format=%H -3 -- tools/round-48/ plans/round-48-claims.md` | 0 | freeze chain `7fe11332` → A1 `dc73587a` → A2 `ac02a79f`; declared freeze per claims file = `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` |
| `grep` on `tools/round-48/record2.py` / `meanings.py` / `round-46/gate.py` | 0 | located `oracle()` at `record2.py:62-71` (`exec(compile(body, ORACLE, "exec"), ns)`) and `gate.show` → `git show <rev>:<path>` at `gate.py:47-49` |

`scripts/sources-census.sh validate` — **not run** (census validation is the L1's post-landing
step; noted in the draft's Gate text).

## Out of scope / not touched

- No edits to `corpus/SOURCES.md`, `corpus/lessons/round-48.md`, SKILL.md, plans/, tools/, or any
  frozen path. No commits, no staging, no mutating git/jj. Scratch `$S` removed after receipts
  were copied into the report dir.
- Claim verification/attack is other seats' scope; this seat's contribution is the source
  grounding for the C2 oracle primitive only.
- No installs performed or needed (curl/python3/git preinstalled). RULES.md read guidance noted;
  nothing installed means nothing recorded beyond this line.

Report: `.ufo/waves/round-48/w1/ScribeSources.md`
