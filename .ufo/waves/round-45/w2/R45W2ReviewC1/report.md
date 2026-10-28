# R45W2ReviewC1 — falsification of `tools/round-45/c1-counter.py`

Seat R45W2ReviewC1 (reviewer, leaf member — no subagent dispatch). Wave 2, round 45.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`;
amendment A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`; HEAD at review time
`a63d109faa050207d4c184471889049741c9ebbf`.

Target: the R45-C1 interpreter `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/c1-counter.py`
(366 lines), attacked through hostile `SKILL.md` inputs in throwaway git fixtures. The reader under
test is the byte-frozen copy `evidence/c1-counter.py`,
`sha256 2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509`, identical to
`git show f762b72:tools/round-45/c1-counter.py` (both hashes computed, see
`evidence/SHA256SUMS`).

**Read-only attestation.** No write outside this seat directory and
`/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC1`. Mutating git ran only inside `mktemp -d` fixtures
under that scratch (`init`, `config`, `add`, `commit`, `update-index`, `hash-object`,
`checkout`, `merge`), each fixture asserted with `git -C "$D" rev-parse --show-toplevel` = `$D`
before its first commit. On the lane tree only `show`, `log`, `cat-file`, `rev-parse`,
`ls-tree`, `status --porcelain` were used. `plans/round-45-claims.md` and `tools/round-45/` were
never written; that is why every receipt below carries `frozen_path_changed: []` except the two
fixtures built to exercise the arm itself (`A6`, `B1`).

**Installs.** None. Nothing was needed; pacman was not touched.

Scratch `$S` was removed after `evidence/` was copied here.

---

## 0. Baseline: the landing's green is reproducible

| what | command | exit | receipt values | stdout sha256 |
|---|---|---|---|---|
| freeze → landing | `python3 -I -B tools/round-45/c1-counter.py --root $PWD --freeze f762b72 --rev e715263 --json-out …` | **0** | `rule_blocks 22, block22_present 1, block22_rows 10, block22_refs 6, block22_unresolved_citations [], block22_cites {S140:true,interpreter:true}, block22_header_ok true, preflight_selftest {cases:11, failures:0, exit:0}, met_target true, frozen_path_changed []` | `03200e3b92f01f7a03a1f19a40b1d2bd89850fa9f883db231eac7a2d56b3b590` |
| freeze → HEAD | same with `--rev a63d109` | **0** | same, `block22_refs 8`, `met_target true` | `23c0326099b7c201d07e2754465accb77f6ecca120328f4d96175eb5f4ad80aa` |
| counter selftest | `python3 -I -B tools/round-45/c1-counter.py --selftest` | **0** | `C1_SELFTEST: cases=9 failures=0` | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` |

Receipts: `evidence/realreceipts/c1-freeze-to-landing.{json,stdout}`,
`…-to-head.{json,stdout}`, `c1-selftest.stdout`. UTC of capture 2026-10-28T16:02Z.

I also checked, on the real `SKILL.md` at both revisions, that the six defects below are **latent**
(not triggered) at the measured revision: fence-aware count of `^- **` items in
`## Queue-drain craft` = 22 = the counter's `rule_blocks`; zero `^- **` lines inside fences; zero
`## ` lines inside the section; block 22 carries exactly one marker and it is the 22nd item; its
header is exactly `| trigger | arm | exit | receipt |`; its 6 (landing) / 8 (HEAD) `path:line`
citations are all inside the REF grammar and all resolve.

So the disagreeable part of this report is **not** "the landing is red". It is: several clauses of
the R45-C1 predicate are satisfiable by inputs that do not have the property the clause names, and
the freeze arm can be bypassed — i.e. the green is weaker evidence than the claims file asserts.

---

## 1. Verdict by attack

| # | attack | verdict | decisive receipt |
|---|---|---|---|
| 1 | `craft_blocks` split stability with a fenced `## ` in a rule body | **falsified** | `A1b` 2 markers / 23 blocks read as `1 / 22`, exit 0; `A1d` 21 blocks read as 22, exit 0; `A1a` 22 blocks read as 5, exit 1; `A1c` heading variant → `IndexError`, exit 1 |
| 2 | does `block_table` grade the FIRST table / can a later table be mistaken for the decision table | **holds** for the question asked (a later table cannot be substituted for the decision table: `A2a`, `A2c` both fail closed). **falsified** for row accounting: rows of a second table are counted as rows of the decision table (`A2b`, 2 decision rows → `block22_rows 9`, exit 0) | `A2a` exit 1, `A2c` exit 1, `A2b` exit 0 |
| 3 | header check satisfied by substrings | **falsified** | `A3a`: one header cell `triggeralarmexitreceipt` satisfies all four keys, exit 0; `A3b`: `triggering event / alarm / exit-status / receipts`, exit 0 |
| 4 | REF line check accepts an in-file range beyond the intended content; `refs >= 4` counting | **falsified** | `A4a` one citation ×4 → `block22_refs 4`; `A4b` 7 citations incl. three unresolvable non-`.md` paths → `4 refs, unresolved []`; `A4c` `plans/round-45-claims.md.bak:9999` counted as a resolving ref; `A4d` lines 58-60 of a 60-line filler file → `unresolved []`. Bounds math itself holds (`A4e` exit 1) |
| 5 | can a hostile `SKILL.md` make `run_preflight` run something else | **holds** for injection (no path from `SKILL.md` bytes to a process: `A5a` marker absent, exit 0). **falsified** for what the run proves: the "cases >= 11, failures == 0" claim is read from stdout only (`A5b`: a six-line stub that writes outside the work dir and spawns a subprocess → exit 0, `met_target true`), and a non-UTF-8 frozen blob makes the counter crash with exit 1 and no receipt (`A7b`) | `A5a`, `A5b`, `A7b` |
| B1 | bonus, same file: `frozen_path_changed` vs merge commits | **falsified** | evil merge replaces the frozen interpreter with a zero-test stub; `git log --name-only` (as used) prints nothing for the merge, `git log -m --name-only` prints the path twice; counter exit **0**, `met_target true`, `preflight_selftest {cases:11,failures:0}` |

Every fixture is reproducible from the scripts in `evidence/` (`attack.py`, `attack_extra.py`,
`a5b.py`, `a7b.py`); each per-case counter receipt is in `evidence/results/`.

---

## 2. Findings, by severity

### F1 — S1 — the selftest clause is satisfied by a print statement, and the counter's own green fixture is a stub

**Attacks 5.** Clause 6 of the claim: *"The interpreter extracted from `--rev` runs `--selftest`
with exit 0 and `cases >= 11`, `failures == 0`"*. The counter does not observe cases — it greps the
child's stdout:

```python
# tools/round-45/c1-counter.py:108-111
m = re.search(r"PREFLIGHT_SELFTEST: cases=(\d+) failures=(\d+)", proc.stdout)
cases = int(m.group(1)) if m else -1
failures = int(m.group(2)) if m else -1
ok = proc.returncode == 0 and cases >= 11 and failures == 0
```

**Input (`evidence/a5b.py`).** An interpreter blob of six lines (shebang, `import os, sys`, one
`open()` write, one `os.system()`, one `print()`, `sys.exit(0)`):
`open('<scratch>/PWNED-preflight','w').write('executed')`, `os.system('touch <scratch>/PWNED-preflight-subprocess')`,
`print('PREFLIGHT_SELFTEST: cases=11 failures=0')`, `sys.exit(0)` — no arms, no cases, no
assertions. `SKILL.md` is otherwise the green fixture.

**Command / result.** exit **0**, `met_target true`,
`preflight_selftest {cases: 11, failures: 0, exit: 0, ok: true}`, stdout sha
`97575e1768cf24874da1d52429ae9685a76cd37c6f4f548d575eead46be9d698`, UTC 2026-10-28T16:03:59Z.
The stub did run arbitrary code (`wrote_outside_work true`, `ran_subprocess true`).
Record: `evidence/results/A5b.record.json`.

**Why this is not a hypothetical.** The counter's own selftest feeds exactly such a stub to the
green case: `STUB_OK` (`c1-counter.py:251-254`) prints the magic line and exits 0, and `green()`
(`:274-276`) scores that as `expect 0`. So the instrument demonstrates, in its own selftest, that
it cannot distinguish a real 11-case preflight selftest from a three-line print. Clause 6 is
therefore not evidence that the arms are proven red; the evidence for that lives in whoever reads
`frozen-path-preflight.py`, not in the counter's receipt.

**Worst case.** Any `REV` whose `tools/round-45/frozen-path-preflight.py` blob has been replaced by
such a stub scores green — see F2 for how that blob can be replaced while the frozen arm stays
silent.

**Fix (minimal).** Do not accept a self-report. Either
(a) pin the interpreter: add `--interpreter-sha256` to the counter, take the expected hash from
`plans/round-45-claims.md` (frozen), and fail clause 6 unless
`git rev-parse --verify "$REV:tools/round-45/frozen-path-preflight.py"` equals it and the child
exits 0; or
(b) require a machine-readable case list and assert it: the preflight prints one
`PREFLIGHT_CASE <name> expect=<n> got=<n>` line per case, the counter parses those and requires
the exact case-name set the claims file enumerates (touched, restored, dirty, pathspec-required,
unknown freeze, non-ancestor, bulk sweep, plus the greens) with `got == expect` for each.
(a) is two lines and closes the substitution hole; (b) additionally detects a tampered selftest.

### F2 — S1 — `frozen_path_changed` is blind to merge commits, so the frozen arm can be bypassed

**Bonus, same file, directly contradicts the claim's kill rule** (*"A commit in `FREEZE..REV`
touching a frozen path makes the counter exit 2"*).

```python
# tools/round-45/c1-counter.py:52-57
log = git(root, "log", "--name-only", "--format=", f"{freeze}..{rev}", "--", *FROZEN)
```

`git log --name-only` prints **no file list for merge commits** (no `-m` / `--diff-merges`).

**Input (`attack_extra.py:case_b1_evil_merge`).** Fixture: freeze commit with the green `SKILL.md`
and `STUB_OK` interpreter; a side branch with an unrelated file; `git merge --no-commit --no-ff side`;
then, inside the merge, `tools/round-45/frozen-path-preflight.py` is overwritten with a zero-test
stub; commit the merge. `REV` = the merge.

**Command / result.** exit **0**, `met_target true`, `failing []`,
`preflight_selftest {cases:11, failures:0}`, stdout sha
`1f61d62e482083a8b110053cd6e56a0d9a60c554b89be9a0f4c7c424919c41db` (UTC 2026-10-28T16:02:10Z).
The same range scanned with `-m` prints the frozen path twice:
`git_log_name_only []` vs `git_log_m_name_only ["tools/round-45/frozen-path-preflight.py",
"tools/round-45/frozen-path-preflight.py"]`. Record: `evidence/results/B1-evil-merge.json`.

**Expected.** exit 2, `verdict could_not_evaluate`, `frozen_path_changed:
["tools/round-45/frozen-path-preflight.py"]`, no `met_target`. (The honest, non-merge touch path
does behave: `A6` exit 2, `frozen_path_changed ["plans/round-45-claims.md"]`, no `met_target`,
`evidence/results/A6-honest-touch-exit2.json`.)

**Differing value.** `frozen_path_changed` = `[]` where it must be a non-empty list; exit 0 where it
must be 2. An evil merge is exactly the shape a non-author sweep would take in this repo (the
round-44 incident was a 432-path bulk commit), so the arm's blind spot is the same class of event it
exists to catch.

**Fix.** `git log -m --first-parent --name-only --format=` … `--` `*FROZEN`. `-m` makes merges
contribute their diff against each parent (fine: any touch counts); `--first-parent` keeps the walk
on the integration line. Apply the identical change in `tools/round-45/frozen-path-preflight.py`'s
commit arm, which the claim says parses `git log --name-status` (same default-merge blindness).

### F3 — S1 — `craft_blocks` is not fence-aware: a fenced `## ` or `- **` line silently redefines the document

```python
# tools/round-45/c1-counter.py:59-61
section = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
return re.split(r"(?m)^- \*\*", section)[1:]
```

Both splits are plain text splits at column 0; a fenced code block is invisible to them.

**(a) false pass on clauses 1+2 (`A1b`).** Fixture: 21 plain blocks, then the marked block, whose
body ends with
```
  ```markdown
## Worked example heading
  ```
```
followed by a **second** `- **23. Duplicate rule.** <!-- freeze-integrity-table v1 --> …` block.
Ground truth (fence-aware count of `^- **` items and of marker occurrences in the section):
**23 blocks, 2 markers**. Counter: `rule_blocks 22, block22_present 1, met_target true`, exit 0,
stdout sha `7b9a7fb2711db4a215585f17d9f23f1bb3fe9156cb7b390f9bff9f613ca9c76a`
(`evidence/results/A1b-fence-hides-second-marker.json`). Differing values: `rule_blocks` 22≠23,
`block22_present` 1≠2. The duplicate marker and the duplicate block are simply not in the string
the counter parses.

**(b) false pass on clause 1 the other way (`A1d`).** Fixture: 19 plain blocks, a block whose body
contains a fenced `- **not a rule, a sample bullet**` line, then the marked block. Ground truth:
**21 rule blocks** (the fenced line is not a list item). Counter: `rule_blocks 22, met_target true`,
exit 0, sha `6f746aa500f7bcac05b00a4e6706f95c0b9227d2eab9047d1a94c1a568df3c02`
(`evidence/results/A1d-fence-inflates-block-count.json`). A sample bullet inside an example block
counts as a rule.

**(c) false negative (`A1a`).** A fenced `## Not a section heading, an example` inside block 5 of a
22-block document truncates the section at block 5: `rule_blocks 5`, `block22_present 0`, exit 1,
sha `c17c783cb57a2d82b6e11e97157c16dea12763daacb08f3529a1b19d346911a0`.

**(d) crash on a heading variant (`A1c`).** `## Queue-drain craft` (no trailing qualifier — the
split needle includes the trailing space) → `skill.split(...)[1]` raises `IndexError: list index
out of range`; exit **1**, stdout empty (sha `e3b0c442…`), `--json-out` file **not written**. See F7
for why exit 1 here is a semantics violation, not just a crash.

**Fix.** One line-oriented pass, taking the section boundaries and the block starts only at fence
depth 0:

```python
def craft_blocks(skill):
    out, cur, in_section, fence = [], None, False, False
    for line in skill.splitlines(keepends=True):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
        if not fence:
            if line.startswith("## "):
                if in_section:
                    break
                in_section = line.startswith("## Queue-drain craft")
                continue
            if in_section and line.startswith("- **"):
                if cur is not None:
                    out.append(cur)
                cur = line
                continue
        if in_section and cur is not None:
            cur += line
    if in_section and cur is not None:
        out.append(cur)
    return out
```

Also make the heading match tolerant of a missing qualifier (`line.startswith("## Queue-drain
craft")`), so a rename cannot crash the counter.

### F4 — S2 — the header check is a substring test over cells, and one cell can satisfy all four keys

```python
# tools/round-45/c1-counter.py:161
header_ok = all(any(k in h for h in header) for k in ("trigger", "arm", "exit", "receipt"))
```

Each key needs *some* cell that *contains* it; the same cell may serve every key, and the match is
`in`, not equality. Substring facts (measured): `"arm" in "alarm"` ✓, `"trigger" in "triggering"` ✓,
`"receipt" in "receipts"` ✓, `"exit" in "extraction"` ✗.

**Input (`A3a`).** Header `| triggeralarmexitreceipt | note | a | b |`, rows `| 1 | n | x | y |` ×8.
`header_ok true` (all four substrings live in cell 0), and because the exit column resolves to that
same cell 0, every "exit cell" is the literal `1`. Counter exit 0, `met_target true`, sha
`088cb2f187d74ed9bc8618d68d2db6f3ed584574b68983b27c03071297be69f6`. A table with **no**
trigger/arm/exit/receipt columns scores as the decision table.

**Input (`A3b`, realistic).** `| triggering event | alarm | exit-status | receipts |` with eight
numeric rows: `header_ok true`, exit 0, sha
`63c2d3af177377d663db1a1090436762d3aeefc2ad428a0d5e51f99632a6078d`. "Alarm" is accepted as the
`arm` column.

**Fix.** Exact cell equality, distinct columns, and a column map instead of a positional guess:

```python
WANT = ("trigger", "arm", "exit", "receipt")
norm = [c.strip().strip("`* ").lower() for c in header]
cols = {k: norm.index(k) for k in WANT if k in norm}
header_ok = len(cols) == 4 and len({cols[k] for k in WANT}) == 4
exit_col = cols.get("exit")
```

### F5 — S2 — `block22_refs` counts occurrences, the REF regex matches prefixes, and three citation classes are invisible

```python
# :33
REF = re.compile(r"((?:corpus/(?:knowledge|lessons)|plans)/[A-Za-z0-9._-]+\.md)(?::(\d+)(?:-(\d+))?)?")
# :78-95  unresolved_refs: total += 1 per findall hit; bounds check only
```

Four independent demonstrations, all `met_target true`:

| case | input added to the graded block | reported | why |
|---|---|---|---|
| `A4a` (`1a3d5ca6…`) | the same citation `corpus/lessons/round-44.md:38` four times | `block22_refs 4`, `unresolved []` | `refs >= 4` counts repetitions; "four or more located citations" is satisfied by one citation |
| `A4b` (`eedaef1c…`) | four valid refs **plus** `corpus/SOURCES.md:9999`, `SKILL.md:9999`, `tools/round-45/c1-counter.py:9999` | `block22_refs 4`, `unresolved []` | the grammar only matches `corpus/{knowledge,lessons}/*.md` and `plans/*.md`; the three unresolvable citations are not seen at all (the block contains 7 citations, 3 broken) |
| `A4c` (`0a40e62f…`) | `plans/round-45-claims.md.bak:9999` | `block22_refs 4`, `unresolved []` | the regex is unanchored at the right edge, so it matches the prefix `plans/round-45-claims.md`, the optional `:line` group then fails on `.bak`, and a citation to a **non-existent file and a non-existent line** resolves |
| `A4d` (`586307f6…`) | `corpus/lessons/round-44.md:58-60`, `…:59`, `spotcheck.md:40`, `knowledge/…:30` in a 60/40/30-line file of filler | `block22_refs 4`, `unresolved []` | the check is `1 <= first <= end <= count`: bounds only. It cannot know the lines say what the block claims; a range whose start is past the intended content is accepted whenever it is ≤ `len(file)` |

The bounds arithmetic itself is correct in the direction that matters for typos: `A4e` cites
`corpus/lessons/round-44.md:61` in a 60-line file → `unresolved
["corpus/lessons/round-44.md:61-61"]`, exit 1, sha `e9902958…`. And `first > end` is rejected.

**Fix.**
1. Dedupe: `total = len({(n, f, l) for n, f, l in REF.findall(block)})`.
2. Anchor: `(?<![A-Za-z0-9._/-])` before the path and `(?![A-Za-z0-9._-])` after `\.md`, with the
   `:line` group mandatory for the four cited ranges (`A4c` then becomes unresolved).
3. Grade every citation the block contains, not just the convenient class: run one generic
   `([A-Za-z0-9_./-]+\.(?:md|py|sh|json))(?::(\d+)(?:-(\d+))?)?` scan, count each hit, and resolve
   each hit (`A4b` then reports 7 refs and 3 unresolved). The block's own citations to
   `tools/round-45/frozen-path-preflight.py` and `SKILL.md` are exactly the ones today's grammar
   ignores.
4. Either state in the claim that refs are "in-file, bounds-checked" rather than "resolve", or add a
   content check: require each cited line range to contain a token the row names (e.g. the ref's
   row's `receipt` word). Anything weaker does not distinguish `A4d` from a real citation.

### F6 — S2 — rows of a second table are counted as rows of the decision table

`block_table` (`:64-76`) takes the header from the first `|` line in the block and then appends
**every** subsequent `|` line in the block as a data row, skipping only lines that fullmatch
`\|[\s:|-]+\|`. A second table's rows are therefore rows of the "first" table, and a second table's
header is itself a data row.

**Input (`A2b`, `evidence/results/A2b-concat-two-tables.json`).** Decision table with header +
**2** rows, then a second table
`| rank | item | 1 | note |` + 6 rows `| r{i} | item {i} | {i%3} | note |`. Counter:
`block22_rows 9`, `block22_header_ok true`, `bad_exit []`, exit **0**, `met_target true`, sha
`d630eeea106fee4830c3bef30db897c84cf3e7d7e9fe2c203a18a861431c1bf2`. The decision table has two
rule rows; the claim's clause is "at least eight rule rows".

This also answers the literal question: because the first table is what supplies the header and the
exit column, a later table **cannot** be substituted for the decision table (`A2c`: an 8-row example
table followed by a 2-row decision table containing `depends` → `block22_rows 11`, 2 bad exit
cells, exit 1; `A2a`: a one-column decoy first table → `header_ok false`, exit 1). The failure is
permissive counting, not mis-selection.

**Fix.** Split the block into tables: a table is a maximal run of `|` lines; grade only run 0; rows
are run 0 minus its separator. If the block legitimately carries a second table, name it (e.g.
`<!-- freeze-integrity-table v1 -->` must be immediately above the graded table, and the table is
the first table *after* the marker).

### F7 — S3 — two could-not-evaluate conditions report exit 1 with no receipt

Exit codes are semantic in this round ("2 could-not-evaluate; a 2 is never a pass"). Two inputs
produce a crash instead: Python's default exit status for an uncaught exception is **1**, and
`main()` has no handler around `evaluate()`.

| case | input | exit | stdout | `--json-out` |
|---|---|---|---|---|
| `A1c` | `SKILL.md` whose heading is `## Queue-drain craft` (no qualifier) | **1** | empty (`e3b0c442…`) | **not written** |
| `A7b` | `tools/round-45/frozen-path-preflight.py` blob containing one non-UTF-8 byte, present at both FREEZE and REV (so the frozen arm is silent) | **1** | empty (`e3b0c442…`) | **not written** |

`A7b` stderr tail: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 74: invalid
start byte` (the failure is `git(..., text=True)` in `show()`; the byte never reaches
`run_preflight`). Record `evidence/results/A7b-non-utf8.record.json`, UTC 2026-10-28T16:03:34Z.

A scorer that treats "exit 1" as "not met" records these as scored failures rather than
unmeasurable; a scorer that requires `--json-out` finds no file at all. Note that the same crash
class also covers the `timeout=300` in `run_preflight` (`subprocess.TimeoutExpired` is uncaught) —
**[INFERENCE]** from code reading; I did not wait 300 s to observe it (see §6).

**Fix.** In `main()`:
```python
try:
    code, receipt = evaluate(os.path.abspath(args.root), args.freeze, args.rev)
except Exception as exc:
    code, receipt = 2, {"reason": f"internal error: {type(exc).__name__}: {exc}"}
```
and make `git()` decode with `errors="surrogateescape"` (or keep the interpreter blob as **bytes**:
`git cat-file -p` → write bytes → no decoding at all), so non-UTF-8 at a frozen path is not a crash.

### F8 — S3 — "rule block 22" is only a count and a marker, never an identity; the selftest case name overstates coverage

The predicate checks `rule_blocks == 22` and `block22_present == 1`; it never looks at the block's
number. Fixture `A1e`: 20 plain blocks, the marked block labelled **`- **3. Freeze integrity.**`**,
then `- **22. Unrelated rule.** body`. Counter: `rule_blocks 22, block22_present 1, met_target true`,
exit 0, sha `91c466536ac05a73689e96bb5e6bdb884453c8c78d4f362abe9a327b41ea88dc`
(`evidence/results/A1e-marker-not-on-block-22.json`). The document's rule block 22 is not the
decision table, and the decision table is rule 3.

Related: the selftest case `red-relabelled-21-block` (`:278-281`) relabels the block **and** rebuilds
the document with 20 plain blocks, so it fails on the count, not on the relabel; relabelling alone
is green (`A1e`). The case name claims coverage it does not have.

At the measured revisions this is latent in the good direction: the marked block *is* the 22nd
`^- **` item at both `e715263` and `a63d109`.

**Fix.** Assert identity: take the block whose first line matches `^- \*\*22\.` and require the
marker inside it (and if a second marker exists anywhere, fail); or drop the number from the claim
and name the surface by marker only. Rename the selftest case to
`red-twenty-one-blocks-not-22`.

---

## 3. What holds (and how I know)

| probe | expectation | result |
|---|---|---|
| `A5a` — a graded block whose text contains `__import__('subprocess').run(['touch', …])` | nothing executes | marker file absent, `met_target true`, exit 0, sha `3ac1ce9c…`. `SKILL.md` bytes reach only `re`/`str`; the only executed bytes are `show(root, rev, PREFLIGHT)` |
| `A5e` — `PYTHONPATH` pointing at a directory whose `json.py` writes a marker | `-I` ignores it | `pythonpath_module_imported false`; the receipt is byte-identical to the clean baseline (`bf27acf607cd19fe4953839e1160fee591720669e1b3954cccb9a431e49f1712`, same as `A0`; both fixtures carry the same content and were committed in the same second, so the commit ids coincide and the only difference between the two runs is the injected env), which is the cleanest possible statement that the child's env was neutralised |
| `A5f` — the interpreter path committed as a **symlink** (`git show` returns the link target text) | no redirect | counter writes the target string as a regular file, Python raises `SyntaxError`: `preflight_selftest {cases:-1, exit:1}`, counter exit 1, sha `f62c7a78…`. A symlink cannot make it run a different file |
| `A5g` — `.gitattributes` `*.py text eol=crlf filter=evil` with a hostile smudge `tr 'P' 'X'` | blob bytes, un-filtered | exit **0** with the untouched stub: `git show rev:path` emits the blob verbatim, so ASCII-armouring the executed bytes is not a bypass, sha `a3f2af10…` |
| `A5h` — the interpreter blob starts `#!/bin/sh` | executed as Python regardless | exit 1 (`cases -1`); the shebang is inert because the child is `sys.executable -I -B <path>` |
| `A5c` / `A5d` — `cases=10`, and `cases=11` with exit 3 | both refused | exit 1 in both (`ede8cac0…`, `80f13376…`); the `cases >= 11` and `returncode == 0` gates work in that direction |
| `A6` — an honest post-freeze commit touching `plans/round-45-claims.md` | exit 2, no `met_target` | exit 2, `verdict could_not_evaluate`, `frozen_path_changed ["plans/round-45-claims.md"]`, no `met_target`, sha `5aafaa6e…` |
| `A2a`/`A2c` | a later table cannot replace the decision table | both fail closed (exit 1) |
| `A4e` | out-of-range line is caught | `unresolved ["corpus/lessons/round-44.md:61-61"]`, exit 1 |

---

## 4. Calibration

1. **The landing is green on its own bytes and I could not make it red without changing them.**
   Both real receipts (`freeze→landing`, `freeze→HEAD`) are exit 0, `failing []`, and the
   `--selftest` is 9/9. Nothing in this report disputes the value at `e715263`; it disputes what
   that value proves.
2. **Six of the eight findings are latent at the measured revision** (§0's checks: fence-aware
   count 22, no fenced bullets, one table, exact header, all citations inside the grammar and
   resolving). They are not "the landing is wrong"; they are "the predicate would not notice if it
   became wrong in these six ways", which is the depth claim's own subject: *"a table whose arms are
   proven red"*. The arms are proven red inside `frozen-path-preflight.py`; the counter's receipt is
   not a proof of them (F1).
3. **Two findings are not latent in the same sense.** F1 (`STUB_OK` is the counter's own green
   fixture) is visible in the frozen source at `:251-254` and `:274-276`; F2 (merge blindness) is a
   property of the `git log` invocation, not of any particular tree — it applies to the measured
   revision just as much as to HEAD, and the round-44 incident it cites was a bulk commit, i.e. the
   family of event that can be shaped into an evil merge.
4. **Severity is about what a false green would license.** F1+F2 compose into this scenario: a
   merge commit replaces the preflight with a stub (arm silent, F2) whose stdout line the counter
   accepts as 11 passing cases (F1) → `met_target true`. That path needs no bug in the fixture
   design and leaves `frozen_path_changed []`. Nothing else in this report composes that far: F3–F6
   need the graded surface itself to be malformed, and a malformed `SKILL.md` in `FREEZE..REV` is
   not caught by either arm by design (`SKILL.md` is "the graded surface and is **not** frozen").
   That design choice is the reason F3–F6 matter: the surface is deliberately mutable, so the
   reader is the only gate on it, and the reader is permissive in exactly those four ways.
5. **The claim's "kill rule" is accurate for the cases it lists** (relabelled/thin/bad-citation/
   no-S140/failing-interpreter) — I reproduced all five through the selftest — but each listed red
   case is a *reduction* of the surface (fewer blocks, fewer rows, a broken number, a missing string,
   a failing stub). None of them is a *substitution*: a structurally different document that still
   "looks" like 22 blocks with a table. F3–F6 are substitutions, and every one of them is green.

---

## 5. Residual risk

1. **`run_preflight` executes rev bytes with the caller's full privilege.** `-I -B` isolates imports
   only (verified `A5e`); it is not a sandbox. `A5b` shows the child can write outside its work dir
   and spawn processes. The `HYAKU_SCRATCH`/`TMPDIR` base is caller-controlled, so the *work
   directory* is not a containment boundary either.
2. **`FREEZE == REV` is a legitimate scoring shape** (the counter's own selftest uses it; the
   claims' "at the freeze" control does too). In that shape nothing authenticates the interpreter
   bytes beyond the freeze commit itself, so the integrity of clause 6 rests entirely on F1's fix.
3. **`git log` blindness is not only a merge problem.** Any commit whose diff is suppressed by the
   walk's options (merges today) is invisible; the same invocation is duplicated in
   `frozen-path-preflight.py` per the claim, so a fix must land in both or the two gates disagree.
4. **The REF grammar is a whitelist of two directories.** A future block that cites
   `corpus/SOURCES.md` or a `tools/…py:` line — both natural for a gate rule — would have those
   citations silently ungraded while still counting as "cited" prose (F5).

## 6. Verification gaps / not run

- **`timeout=300` path — not run.** Exercising it means a 300 s hang per attempt; the conclusion
  (`TimeoutExpired` uncaught → exit 1, no receipt) is read from `:107` and is labeled
  **[INFERENCE]** in F7. It is the same defect class as the two observed crashes.
- **Rename/delete of a frozen path across a merge — not run.** `--name-only` with renames would list
  both sides on a normal commit; the merge case is already covered by F2, so I did not add a second
  fixture.
- **`frozen-path-preflight.py`'s own arms — not attacked here.** This seat's target is
  `c1-counter.py`; the preflight's arm semantics (including its own `git log --name-status` merge
  blindness) belong to the seat that owns the interpreter. F2's fix note flags it because the claim
  makes the two counters responsible for the same arm.
- **No claim-file or SCORECARD numbers were re-derived.** Out of this seat's scope (the record is
  another seat's target); I only used the claims file as the rule, per the assignment.

## 7. Evidence inventory

All paths relative to `.ufo/waves/round-45/w2/R45W2ReviewC1/evidence/`.

| file | sha256 |
|---|---|
| `c1-counter.py` (frozen copy under test) | `2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509` |
| `attack.py` (driver, cases A0-A6) | `10175c9a60983202926c046b362f60d0292a96aa216ca632e8ec08e36224e637` |
| `attack_extra.py` (A1d, A1e, B1) | `accb548df4bae63b356c402da00a2f99c2df8c6ad8af4d0db41cd155e2a817e8` |
| `a5b.py` (corrected A5b receipt) | `4b94d011d05f477d345f1b02798eb1b86c0324870796db4e6ead78733b5811e1` |
| `a7b.py` (non-UTF-8 fixture) | `a16191e68b5af49a9deea927007adf13b453c26cab5d6cf80a57a11784263470` |
| `results/results.json` (all cases) | `769088030ed7eaa96db7f5058fcae6a2015068276dd4b3a02c24b336c3b55dc1` |
| `results/results_extra.json` | `1941ff68619a2d0f26aff13954295fa8592f1329831916b7b65ecec9d58d4316` |
| `results/A5b.record.json` | `546a0b24b3112ce3999f7b3447fda145206e6877d6d2ac30d3d2f5ef6e097c7d` |
| `results/A7b-non-utf8.record.json` | `527dc0bb98e4875a201e5bfc70d2fb1f0b1d6c589c4911bb3cd6583bb77f6a84` |
| `results/B1-evil-merge.json` | `73356e83348e768d2f51959ceae027103befeafa70ab4fd8fd64debaff4eeda2` |
| `realreceipts/c1-freeze-to-landing.json` | `03200e3b92f01f7a03a1f19a40b1d2bd89850fa9f883db231eac7a2d56b3b590` |
| `realreceipts/c1-freeze-to-head.json` | `23c0326099b7c201d07e2754465accb77f6ecca120328f4d96175eb5f4ad80aa` |
| `realreceipts/c1-selftest.stdout` | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` |

Per-case counter receipts `results/A0-base-green.json` … `results/A6-honest-touch-exit2.json`,
`results/A7b-non-utf8.json`, `results/B1-evil-merge.json`; `results/A7-non-utf8.json` is the
superseded first attempt at the non-UTF-8 fixture (it exited 2 `frozen_path_changed` because the
blob was introduced *after* the freeze — the arm working correctly; kept for honesty, superseded by
`A7b`).

## 8. Reproduction

```sh
S=/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC1
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show \
  f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/c1-counter.py > "$S/c1-counter.py"
export S TMPDIR="$S" HYAKU_SCRATCH="$S"
cd "$S" && python3 -I -B attack.py && python3 -I -B attack_extra.py \
  && python3 -I -B a5b.py && python3 -I -B a7b.py
```

Each case prints `{case, expect, exit, ok, met_target}` and writes its receipt under `results/`.
`ok` is `exit == expect` for the shape the fixture was built to show; the findings are the rows
where `expect` was chosen to be the *claim-faithful* verdict and `exit 0` was observed.

## Verdict summary for the L1

- attack 1: **falsified** (F3) — fence-unaware split; false pass on the marker count and the block
  count, plus a crash on a heading rename.
- attack 2: **holds** on "a later table cannot be mistaken for the decision table"; **falsified** on
  row accounting across tables (F6).
- attack 3: **falsified** (F4) — substring header check, one cell can satisfy all four keys.
- attack 4: **falsified** (F5) — repetition, prefix-matching, three invisible citation classes, and
  a bounds-only line check.
- attack 5: **holds** on "`SKILL.md` cannot make it run something else"; **falsified** on what the
  run proves (F1, stdout-only) and on exit-code semantics for a non-UTF-8 frozen blob (F7).
- bonus: **falsified** (F2) — the frozen arm does not see merge diffs; composition with F1 yields a
  green score over a replaced interpreter.
