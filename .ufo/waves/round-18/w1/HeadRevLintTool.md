# HeadRevLintTool — `head-rev-lint.py` (C2 counting command)

Seat: `KaidokuR18.HeadRevLintTool` (leaf executor). Axis worked: operability, with
calibration depth. Delivered file:
`.ufo/waves/round-18/tools/head-rev-lint.py`
(sha256 `5ada7b837368a92e9b7813a37529e476acbf7ce6b1fa62dc9d3ee63ee6c68e36`, 928 lines,
stdlib only, `#!/usr/bin/env python3`).

## 0. Result

- `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --selftest`
  → last line `SELFTEST: CLEAN cases=3`, **exit 0**.
- `... --root LANE --rev 9011581d84527ba34c675f9cf912e54d2e72d470`
  → exit 0, `live_count=3`, `fixture_count=8`, `annotated_count=0`,
  `files_scanned=27`, `excluded` = 10 files / 4 would-be sites.
- Same rev with `--strict` → **exit 1** (live_count > 0), as specified.
- The three live sites are exactly the routed ones:
  `citation-drift-probe.py:477` (default-HEAD), `custody-pair.py:327`
  (rev-parse-HEAD), `verify.py:59` (rev-parse-HEAD).

**Baseline buckets** (amendment: "report baseline numbers for every bucket"):

| bucket | count |
|---|---|
| in-scope files scanned (`gates`, `rounds`, `round-1[4-8]`, no seat dirs) | 27 |
| live sites | **3** |
| fixture sites | **8** |
| annotated sites | **0** |
| seat-dir files excluded (listed, not counted) | 10 |
| would-be sites inside excluded files | 4 (2 live-classified, 2 `fixture` by `/fixtures/`) |
| routed sites listed in `routed_sites` | 3 |

## 1. Rule implementation (amendment 1–5) with anchors

1. **Scope** — `SITE_DIRS` (`head-rev-lint.py:78`) covers `.ufo/gates/`,
   `.ufo/rounds/`, `.ufo/waves/round-14/` … `round-18/`; `is_seat_path`
   (`:187`) rejects any `w[0-9]+` path segment (`SEAT_DIR_RE`, `:85`).
   Seat-dir files are still read and reported in `excluded` with
   `reason: "seat wave output, not a lane instrument"` and their would-be
   sites (`lint`, `:606`). Nothing is silently dropped.
2. **Context** — `python_context` (`:524`), priority order: annotation → path
   `/fixtures/` → any enclosing function name containing `selftest`/`fixture`
   → the function is *called-only-from* fixture code. The transitive rule
   (`:496`–`:525`) uses **all references**, not just calls. That detail is
   load-bearing: with call-only edges, `custody-pair.py` `repo_head` became
   `fixture` because its only visible caller chain ends in `cmd_capture`,
   which is wired by `p.set_defaults(func=cmd_capture)` (`custody-pair.py:1319`)
   and has no named call site. Counting the `func=` reference keeps
   `cmd_capture` → `render_receipt` → `repo_head` live. `_commit` in
   `round-17/controls.py` still resolves fixture (its only callers are
   `selftest`, lines 452/454/474), i.e. the amendment's named example holds.
3. **Site detection** — `classify_argv` (`:312`) over tokens from
   `["git", …]` literals and wrapper calls (`_tokens_from_argv_expr`, `:249`;
   `_tokens_from_wrapper_call`, `:268`). Kinds: `rev-parse-HEAD`,
   `other-HEAD` (non-rev-parse revision subcommand, e.g. `rev-list HEAD`),
   `HEAD-colon`, `default-HEAD`, `upstream`. HEAD literals include `HEAD`,
   `HEAD^{commit}`, `HEAD~N`, `@`; `HEAD:` prefixes are detected even when the
   rest of an f-string is dynamic (`_arg_token`, `:223`). Shell scanning
   (`scan_shell`, `:562`) handles `$(git …)` and a simple variable table so
   `V=${X:-HEAD}; git rev-parse "$V"` classifies (fixed during this wave:
   the RHS parser had kept the trailing command, `_shell_assignment_value`,
   `:549`).
4. **Annotations** — `head-rev-lint: compare-only` / `red-before`
   (`ANNOTATION_RE`, `:113`; applied at `:530` and `:631`) set context
   `annotated` with `reason` and never count live; annotation wins over
   fixture.
5. **Output** — `{rev, files_scanned, sites, live_count, fixture_count,
   annotated_count, routed_sites, excluded, limits}`; each site carries
   `path, line, kind, context, code` plus `reason` when not live. `--strict`
   exits 1 iff `live_count > 0`; git/parse failures exit 2
   (`evaluate`, `:677`).

## 2. Baseline sites at `9011581d` (exact)

```
live     default-HEAD    .ufo/gates/citation-drift/citation-drift-probe.py:477  ap.add_argument("--rev", default="HEAD")
live     rev-parse-HEAD  .ufo/gates/custody-pair/custody-pair.py:327           ["git", "rev-parse", "HEAD"],
fixture  rev-parse-HEAD  .ufo/waves/round-17/controls.py:442                   return git(root, "rev-parse", "HEAD").strip()
fixture  rev-parse-HEAD  .ufo/waves/round-17/measure.py:223                    return run("rev-parse", "HEAD").strip()
fixture  rev-parse-HEAD  .ufo/waves/round-17/tools/invocation-audit.py:424     rev = _git(root, ["rev-parse", "HEAD"]).strip()
fixture  rev-parse-HEAD  .ufo/waves/round-17/tools/temporal-sweep.py:261       ["git", "-C", repo, "rev-parse", "HEAD"],
fixture  rev-parse-HEAD  .ufo/waves/round-17/tools/temporal-sweep.py:289       ["git", "-C", repo, "rev-parse", "HEAD"],
fixture  rev-parse-HEAD  .ufo/waves/round-17/tools/temporal-sweep.py:308       ["git", "-C", repo, "rev-parse", "HEAD"],
fixture  rev-parse-HEAD  .ufo/waves/round-17/tools/temporal-sweep.py:332       rev4 = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
fixture  other-HEAD      .ufo/waves/round-17/tools/temporal-sweep.py:343       ["git", "-C", repo, "rev-list", "--max-parents=0", "HEAD"],
live     rev-parse-HEAD  .ufo/waves/round-17/verify.py:59                      source = git("rev-parse", "HEAD")
```

Excluded bucket (not counted):

```
live     rev-parse-HEAD  .ufo/waves/round-17/w2/audit-attack.py:91
live     rev-parse-HEAD  .ufo/waves/round-17/w2/audit-attack.py:349
fixture  rev-parse-HEAD  .ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh:9
fixture  rev-parse-HEAD  .ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh:11
```

## 3. Every live site beyond the three

**None in scope at the baseline.** After the fixture rules, the remaining
HEAD-keyed sites are all fixture repos or selftest bodies. The two
live-classified would-be sites are in the excluded seat dir:

- `w2/audit-attack.py:91` and `:349` — the `build_repo` helper and a
  re-commit path. Both run `git rev-parse HEAD` against a repository created
  by `git init` under `tempfile.mkdtemp()` in the same file (observed
  `audit-attack.py:70-95`, `:349`). They are **lint true positives but
  semantic non-risks**: the repo is a throwaway fixture. They are excluded by
  rule 1 (seat wave output), not because the scan missed them.
- `w2/temporal-attack/fixtures/rebuild.sh:9,11` are `fixture` by the
  `/fixtures/` path segment; the script `mkdir`s `${1:-/tmp/tsw-attack-rebuilt}`
  and commits there (`rebuild.sh:4-12`).

The audit's 32 "live" call sites are not comparable: 31 of them are non-HEAD
(`git show`, `ls-tree`, `rev-parse --verify <arg>`, `status`). This lint
counts **HEAD-keyed revision pins**, so its 3 is the HEAD subset of the
audit's live table, not a contradiction of it.

### Why "8" is not reproducible (bucket table)

| reading | live |
|---|---|
| amendment as delivered (in-scope, context rules) | **3** |
| + seat dirs counted, context rules kept | 5 |
| + seat dirs counted, `/fixtures/` rule off | 7 |
| in-scope, context ignored (every HEAD-keyed site live) | 11 |
| everything scanned, context ignored | 15 |

8 matches none of them. The only composition I found that reaches 8 is
`3 routed + 2 audit-attack + 2 rebuild.sh + 1 citation-drift-probe.py:451`,
where the last is `rev = "deadbeef…" if case == "rev_unresolvable" else "HEAD"`
(`citation-drift-probe.py:451`), passed as `run_check(root, rev, …)` and
rendered into `git rev-parse --verify "%s^{commit}" % rev`
(`citation-drift-probe.py:274`). That is a HEAD literal flowing through a
variable into a git argv: invisible to a literal-argv scan, and inside
`selftest`, so fixture under rule 2. **[INFERENCE]** this is the most likely
source of the critic's 8 if seat dirs and non-argv literals were counted with
context ignored. Under the amendment's rule 3 it is not a site (no
string-literal arg of a git call), and rule 2 makes it fixture if it were.
The gap it exposes is real and is listed in `limits`.

## 4. Every fixture site classification (8)

| site | reason emitted by the tool | evidence |
|---|---|---|
| `round-17/controls.py:442` | called only from selftest/fixture functions (`_commit()`) | `_commit` callers are `selftest` only (`controls.py:452,454,474`); it writes into a `mkdtemp` root |
| `round-17/measure.py:223` | enclosing function `_git_fixture()` | `root` is a `tempfile.mkdtemp` per case (`measure.py:238,255`) |
| `round-17/tools/invocation-audit.py:424` | enclosing function `selftest()` | fixture repo from `tempfile.mkdtemp` (`invocation-audit.py:370-371`) |
| `round-17/tools/temporal-sweep.py:261` | enclosing function `selftest()` | `selftest` commits rev1 in `workdir/"lane"` (`:234-261`) |
| `…:289` | same | rev2 commit |
| `…:308` | same | rev3 commit |
| `…:332` | same | rev4 commit added by `95e34db` (w2 hardening) |
| `…:343` | enclosing function `selftest()`, kind `other-HEAD` | `rev-list --max-parents=0 HEAD` on the same fixture repo |

At baseline these are the only fixture sites; none touches a lane revision.
Line numbers differ from the audit's table because of later commits
(§5), not because of a classification difference.

## 5. Calibration against `JjAuditKaidoku.md` §3.2

At the audit's reading revision `da64646`:

```
live 2  fixture 7  annotated 0  files 26  excluded 0
fixture lines: measure 222, invocation-audit 417, controls 442,
               temporal-sweep 254, 282, 301, 315 (rev-list)
```

That is **exactly** the audit's seven HEAD-keyed fixture anchors. `live 2`
(not 3) because `verify.py` has no `rev-parse` line at all at `da64646`
(`git show da64646:.ufo/waves/round-17/verify.py | grep rev-parse` → empty);
`verify.py:59` first exists at `95e34db`.

History is linear: `2711674 → da64646 → 95e34db → d0ab299 → b31975d →
8e7642c → de6c721 → 9011581` (source `git log --graph --oneline`).
`95e34db` added the `rev4` case (new site at 332) and shifted the others to
261/289/308/343; `d0ab299` shifted `measure.py` to 223 and
`invocation-audit.py` to 424.

Consequence: the audit's anchors cannot all come from one commit — the
temporal anchors price `da64646`, `verify.py:59` prices `>= 95e34db`.
**[INFERENCE]** the audit read a dirty working tree straddling the `95e34db`
edit (its own §9 records 8 pre-existing dirty entries). The delivered
`live_count=3` is correct at the round-18 baseline `9011581d`; it is not a
property of "round 17" as a whole (2 at `da64646`, 3 from `95e34db` on).

## 6. Working-tree snapshot (observation only, not a fix claim)

A copy of the seven in-scope dirs committed into a `mkdtemp` repo
(`/tmp/tmp.QlUkdtSUKG`, rev `d307803…`) gives:

```
live 0  fixture 15  annotated 6  files 38  excluded 10 files / 4 would-be sites
annotated: citation-drift-probe.py:304 compare-only
           custody-pair.py:381, :1350, :1353 compare-only
           round-18/tools/jj-red-before.py:377, :659 red-before
```

The single remaining live site found before the last fix
(`round-18/measure.py:660`) classified fixture after the reference-based rule:
`_commit` ← `_git_fixture` ← `_with_fixture` ← `selftest`, plus `case_h`, a
nested callback inside `selftest`. The tool's **own file produces zero
sites** in this snapshot (self-application clean). This snapshot is evidence
that the annotation and fixture rules work on in-flight C2 edits; it is not a
claim that those edits are complete or correct — that is the L1's pass.

## 7. Commands run (exact, with exits)

| command | exit |
|---|---|
| `git rev-parse --verify 9011581d…^{commit}` | 0 |
| `git ls-tree -r --name-only REV -- .ufo/` (filtered to `.py`/`.sh`) | 0 |
| `git archive REV <7 dirs> \| tar -x` | 2 — my error: `round-18` does not exist at REV and stderr was suppressed; replaced with `git show` per path |
| `for p in <37 paths>; do git show REV:$p > $T/$p; done` | 0 (37 files) |
| `grep -rn 'HEAD'`, `grep -rnE 'symbolic-ref\|@\{u\}\|abbrev-ref\|show-current'` over the extracted tree | 0 when matches, 1 when none |
| `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --selftest` | **0**, `SELFTEST: CLEAN cases=3` |
| `… --root . --rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0 (live 3 / fixture 8) |
| `… --root . --rev 9011581d --strict` | **1** |
| `… --root . --rev da64646adcb19c1ede7537b799b8c7d283fe43da` | 0 (live 2 / fixture 7) |
| `… --root . --rev deadbeef` | **2** (`could-not-evaluate: git rev-parse --verify exit 128: fatal: Needed a single revision`) |
| `… --root .` (missing `--rev`) | **2** |
| two identical baseline runs + `cmp` | 0 (byte-identical) |
| `git log`, `git show`, `git diff --stat`, `git merge-base --is-ancestor`, `git status --porcelain` (read-only) | 0 |
| temp snapshot: `git init -b main`, `add -A`, `commit`; then tool on it | 0 / 0 |

## 8. Limits and known blind spots

Emitted in the JSON `limits` array, plus what this run observed:

- **Dynamic data flow is invisible**: a HEAD literal bound to a variable and
  formatted into an argv (`citation-drift-probe.py:451` → `:274`) is not
  detected. This is the strongest candidate for a disagreement about "8".
- **Wrappers are resolved intra-file only**; a helper in another module is
  not followed.
- **Function identity is name-based**; `round-18/measure.py` defines `main`
  six times (fixture strings), so same-name callers are merged for the
  fixture rule.
- **Lexical nesting is assumed fixture**: a helper defined inside `selftest`
  and *returned* to production would be misclassified (no such case at
  baseline; documented rather than special-cased).
- **Shell tokenization** splits git runs at `&|;<>()#` and on whitespace;
  quoted whitespace and multi-line commands can hide tokens.
- **Annotations are trusted comments**; the lint cannot verify a
  `compare-only`/`red-before` claim.
- **Excluded seat dirs are never counted**, even when another wave re-runs
  one as an instrument.

## 9. Risks, decisions for the L1, compliance

- **No blocker.** The tool and this report are the only LANE writes; every
  other write was under `/tmp`. No `jj`, no git write in LANE (read-only
  `show`/`ls-tree`/`rev-parse`/`log`/`diff`/`status` only), no REA, no
  Ghidra, no carrier execution, no network.
- **Decision to ratify**: seat-dir counting. Under the delivered amendment
  the baseline is 3 live; counting seat dirs *with* context rules gives 5
  (the two `audit-attack.py` sites; `rebuild.sh` stays fixture). The tool can
  be switched by deleting `is_seat_path` at `:187`, but I did not invent that
  reading.
- **Gate timing**: `--strict` is exit 1 at the baseline by construction. It
  becomes a usable gate only after the three C2 in-place fixes commit; the
  working-tree snapshot already shows 0 live, uncommitted.
- **Self-scan**: once this file exists at a scanned revision, it contributes
  no sites (verified against the working-tree snapshot).
- **Installs**: none. No pacman, `uv`, `npx`, or binary installs were needed
  or attempted.

## 10. Selftest cases (what the 3 cases prove)

1. **Red case, named reason `live_head_sites`**: one live site per kind
   (`rev-parse-HEAD`, `default-HEAD`, `HEAD-colon`, `upstream`,
   `other-HEAD`), revision-literal edge forms (`HEAD:{path}`,
   `HEAD^{commit}`, `HEAD~3`, `@`), fixture contexts (name, nested,
   called-only-from-selftest, `/fixtures/` path), one `compare-only`
   annotation, one seat-dir exclusion → `strict` exit 1, live 15, fixture 4,
   annotated 1, files 6; the test asserts the exact `(line, kind)` list for
   the edge file and the fixture/live split of the call-graph file.
2. **Fixture-only**: strict exit 0, live 0.
3. **Clean**: no sites, strict exit 0.
