# SentinelScope — round-80 adapters: live-file reads, paths, child environments, wave bounds, forgery

Seat: SentinelScope (leaf sentinel, `r80-w1`). Scope: adversarial security and scope review of the
round-80 instruments **as landed** and of this wave's bounds. No lane production file was edited;
every write is under `.ufo/waves/round-80/w1/SentinelScope/` plus this report. Read-only git only.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Base `16dfa009bf143080dfcdfc5f9ec34bd359536d90`; declaration guard
  `84d68e90f8a1ea3a3a7f94a208695c21023c0472` (`log -1 -- plans/round-80-claims.md`)
- Measured lane head during this review: `b00419fb8c3d083761034605fec2eed1897f60ad`
  (instruments at `tools/round-80/`, gate cases + SKILL block at `b8260107`, C2 repair at `b00419fb`);
  final head `6037f599552ad574bf9b3e7fddacb788f725944b` (record/closure commit) — the four
  instrument digests, the gate and `SKILL.md` are byte-identical, so every arm below still holds.
- Landed instrument digests (sha256):
  `pointer-bind.py 2e4a7852…`, `strictness-battery.py 2b26d75a…`,
  `receipt-provenance.py b59068d6…`, `guard-battery.py b9b3b10c…`
- Scratch: `/fast/scratch/hyaku/kaidoku-r80/SentinelScope/` (removed before yield; probe receipts
  copied to this dir)

The three predicate arms were re-measured from the landed files before any judgment:

| arm | command | observed |
|---|---|---|
| R80-C1 fixtures | `strictness-battery.py --root . --impl tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py --fixtures …/strictness.json` | `cases 4`, `green_cases 2`, `candidate_false_greens 0`, `control_false_greens 4`, both `green_refusals 0`, `--validate` `[]`, exit 0 |
| R80-C1 live | `pointer-bind.py --root . --rev b00419fb --json-out …` | `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`, `duplicates []`, exit 0 |
| R80-C2 target | `receipt-provenance.py --root . --rev b00419fb --from-round 60 --to-round 79` | `receipts 34`, `flagged 1`, `expected_control_flags 1`, `unexpected 0`, `--validate` `[]`, exit 0 |
| R80-C3 target | `guard-battery.py --root . --rev b00419fb --work … --json-out …` | `guards 9`, `rows 9`, `bound 9`, `survivors_count 0`, `pristine 37/0`, exit 0 |
| C1 base arm | same battery, `--impl tools/round-79/pointer-bind.py` | `candidate_false_greens 4`, exit 1 |
| C2 base arm | same sweep at `16dfa009` | `flagged 2`, `expected 1`, `unexpected 1` = `.ufo/waves/round-79/l1/scores/c2-at-landing.json`, exit 1 |
| C3 base arm | same battery at `16dfa009` | `guards 9`, `rows 0`, `bound 0`, `survivors_count 9`, `pristine 29/0`, exit 1 |
| selftests | all four | `8/0`, `33/0`, `14/0`, `19/0` (cases/failures), matching the SKILL rows |

Every arm in the table was re-measured a second time at the final head `6037f599` with identical
results; the C3 as-printed run again reported `ok true` with `target_pin.matched false`.

## 1. leaks

**The instruments do not retain pointed-line bytes; one *scout receipt and its derivatives do.***

- `pointer-bind.py` (landed) keeps, per cell: `pointer`, `tokens`, `path`, `declared_path`,
  1-based range, `line_sha256` (sha256 of the pointed slice), and `delimiter_evidence` entries of
  `{token, occurrences, delimited, reason}`. A refusal appends the maximal `[A-Za-z0-9._-@]+` run
  around the match (`longer`), e.g. `rea-agents@6.7.05`. That run cannot contain `=`, `"`, space,
  `/` or `:`, so it cannot carry a key/value pair; the residual is "a token-shaped run from the
  live line", not free-form content.
  Verified on a live run at `b00419fb`: `live-at-head.json` is 3 426 bytes, contains **zero** of the
  five pointed lines' non-token text, no `disabledServers`, no `"mcp"`, no `$HOME`/JDK path, and no
  `env` key.
- **Finding L1 (low) — the scout's receipt retains all five pointed live lines verbatim.**
  `.ufo/waves/round-80/w1/ScoutRecord/receipt.json` → `cells[i].pointed_line`, five values:
  the Devin and OMP pin lines (`        "rea-agents@6.7.0",`), the Kimi argv line
  (`args = [ "-y", "rea-agents@6.7.0", "mcp" ]`), `application.version=12.1.4`, and the two
  `.bashrc` exports (`export GHIDRA_INSTALL_DIR="$HOME/.local/opt/ghidra_12.1.4_PUBLIC"`,
  `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk`). The same bytes are copied to
  `.ufo/waves/round-80/w1/ScoutRecord/probe.json` (`cells[i].pointed_lines`),
  `probe.out`, `report.md`, and `.ufo/waves/round-80/w1/ScoutRecord.md`.
  Impact: no secret class (pin strings, version string, export paths; no token, no `env` block, no
  key value), but the wave's own rule — a pointer binder retains a pointed line's digest, never its
  bytes — is broken by a *receipt* in the evidence tree, so the convention cannot be cited as held.
  Smallest remediation: keep `line_sha256` and drop `pointed_line`/`pointed_lines` from the scout's
  receipt and probe (the report prose may quote the *record* cell, which is already committed in
  `PROVINCE.md`).
- **Secret sweep: clean.** `grep -rIlE 'sk-[A-Za-z0-9]{12}|Bearer …|api_key|apiKey|"password":|"env":'`
  over `.ufo/waves/round-80/` and `tools/round-80/` returns nothing. No receipt carries an `env`
  object; all JSON files scanned have no `env`/`environment` key.
- `tools/round-80/pointer-bind.py:433` contains `rea-agents@6.7.00` — the **frozen fixture rb02**
  (two trailing digits), not the live `@6.7.0` line; the record text it carries is `PROVINCE.md`'s
  own public cell, not a live config line.

## 2. path_checks

- **`instrument.path` is vetted before git (C2).** Landed `receipt-provenance.py` classifies
  `not path or path.startswith("/") or ".." in path.split("/")` as `unsafe-instrument-path` and
  never passes it to git. Probed on a synthetic root with seven receipts: `/etc/passwd` →
  `unsafe-instrument-path`; `../../../../etc/passwd` → `unsafe-instrument-path`; no `git show`
  was issued for either (the run's `git_calls` only cover clean paths).
- **No option injection.** A path of the form `--output=<abs>/PWN.txt` reaches git only as an
  object expression (`git show <rev>:--output=…`) and as a `--`-terminated pathspec
  (`git rev-list --all -- <path>`); it classifies `uncommitted-digest` and **no file is created**
  (`PWN.txt` absent after the run). `git show`, `rev-list --`, `cat-file --batch` (object
  expressions on stdin) are the only git surfaces; none takes a bare path argument.
- **No working-tree fallback (C2).** A receipt whose `instrument.sha256` equals the sha256 of an
  *untracked* working-tree file classifies `uncommitted-digest` and is flagged — reproduced on a
  fixture with a genuinely untracked instrument (`tools/demo/wt.py`).
- **Symbolic rev (C2) refused.** `--rev main` → `{"unevaluable": "--rev 'main' is not a 40-hex
  commit"}`, exit 2. (The binder resolves `--rev main` to a 40-hex commit and stores the resolved
  value, never the name — a deliberate cross-instrument difference, not a C1 defect.)
- **The guard battery executes only scratch copies.** `battery()` reads
  `git show <rev>:tools/round-78/attack-gate.py` and writes `pristine.py` plus `m<NN>.py` under
  `--work`, then runs those copies. The lane path `tools/round-78/attack-gate.py` is never executed
  and never written.
- **Writes stay in `--json-out` and `--work`** for the guard battery and the provenance sweep (the
  latter has no `--work` at all). No instrument writes beside `--json-out`.
- **Finding P1 (medium) — the C1 battery falls back to a literal `/tmp`.**
  `tools/round-80/strictness-battery.py`:
  `work = args.work or os.path.join(os.environ.get("TMPDIR", "/tmp"), "strictness-battery")`, and
  `selftest()` uses `os.environ.get("TMPDIR", "/tmp") + "/strictness-selftest"`. The frozen C1
  command omits `--work`, so a reproduction with `TMPDIR` unset creates a **git fixture repo at
  `/tmp/strictness-battery`** (and `make_fixture_repo` `rmtree`s `work/fixture-repo` first).
  Impact: a bound violation of "scratch is one dir under `/fast/scratch/…`, passed explicitly" and
  a fixed-name delete inside `/tmp`. Smallest remediation: make `--work` required (or default to
  `tempfile.mkdtemp(prefix="strictness-battery-")`, which honours `TMPDIR`).
- **Finding P2 (low) — fixed child name under `--work`.** `make_fixture_repo` deletes and recreates
  `<work>/fixture-repo`; a caller reusing a `--work` that already holds a `fixture-repo` loses it.
  Prefer `tempfile.mkdtemp(dir=work)`.
- The C1 battery imports both implementations **in-process** (module API `bind` / `battery`); that is
  the instrument under test, not a stray execution, but it does mean `-B` matters: without it the
  import would write `tools/round-80/__pycache__`. None exists now; the frozen command carries
  `-I -B`.
- A pointer read is not restricted to the declared object before it happens (`read_lines` opens the
  path named in `PROVINCE.md`; `declared_ok` only vetoes the *match*). With a tampered record this is
  a file-existence/sha256 oracle over an arbitrary path. The record is the lane's committed file, so
  the severity is informational; the smallest hardening is to resolve and compare the pointer to
  `DECLARED` **before** reading.

## 3. child_env

- **Guard battery: allowlist held in code.** `child_env(tmpdir)` returns exactly
  `{HOME, LANG, PATH, TMPDIR}` with `TMPDIR = --work`, and every `run_selftest` (pristine and each
  mutant) is spawned with it. `HOME` falls back to the literal `/tmp` only when the parent has no
  `HOME`; `python3` is taken from `PATH` (not `sys.executable`), so the allowlist's `PATH` selects
  the interpreter.
- **Finding E1 (low) — no child environment is recorded.** The C3 receipt carries `pristine`
  (exit/cases/failures/summary) but no `child_env_keys`/`TMPDIR` field, although the battery's own
  code and docstring claim the four-key environment. The gate whose receipts this battery
  validates *does* require `env_keys == ["HOME","LANG","PATH","TMPDIR"]`; by that convention the
  battery should record what it observed. Smallest remediation: add `child_env_keys` and
  `child_env_tmpdir_is_work: true` to the receipt and gate on it in `validate_receipt`.
- **Finding E2 (medium) — the provenance sweep's git children inherit the whole environment.**
  Every call in `tools/round-80/receipt-provenance.py` is
  `subprocess.run(["git", "-C", root, …], capture_output=True)` with **no `env=`**. Consequences:
  `GIT_DIR` overrides `-C` for the whole sweep; `GIT_OBJECT_DIRECTORY` /
  `GIT_ALTERNATE_OBJECT_DIRECTORIES` can make an arbitrary object store the source of "committed"
  blobs, so a digest that is not a blob of this lane can resolve `bound`; `GIT_CONFIG_*` can inject
  config. The receipt records no environment, so a reader cannot tell which store was read.
  This is not reachable from a receipt (the environment is the caller's), but it defeats the
  sweep's "committed in *this* lane" claim under a hostile shell. Smallest remediation: pass
  `env={"HOME":…,"LANG":"C.UTF-8","PATH":…,"TMPDIR":…}` (the same four-key `child_env` the gate
  and guard battery use), and record the key list.
- The binder's `git show`/`rev-parse` children inherit the full environment the same way; its live
  file reads are `open()`. Same remediation, lower impact (the binder has no "committed" claim).
- The C1 battery's fixture git calls (`git init/add/commit` in `make_fixture_repo`) and its
  in-process imports also inherit the full environment; the fixture commit hash is not depended on.

## 4. wave_bounds

- **No seat git/jj write.** `git reflog` holds only the three `export from jj` entries plus the
  L1's round-80 commits; `git stash list` empty; one worktree; no new local branches. The `.jj` op
  store's two newest ops are at 10:41:43/10:41:45 — the L1's own `jj commit -m 'round-80: the
  declaration…'` and `jj … git push --remote origin --bookmark main` (op strings read from the op
  store), i.e. before the first seat write (10:43). No jj op appears after seat work began.
- **No nested repository** anywhere in the lane (`find . -name .git` returns only the lane's), so
  no seat created a fixture repo inside the tree.
- **Every seat write is inside its own evidence dir** plus the sanctioned `w1/<Seat>.md` report
  files (`ExecBinder.md`, `ExecGate.md`, `ExecGuard/…`, `ExecProv.md`, `ReviewerC1.md`,
  `ReviewerC3.md`, `ScoutGate.md`, `ScoutRecord.md`, `ScribeKnowledge.md`, `ScribeLesson.md`,
  `ScribeSources.md`, `ConnectorSibling.md`); `swarm-registry.json` is the harness's,
  `r80-w1.ready.dispatched` is the dispatch marker.
- **Landed production changes came only through the L1's commits** `253fc817` (four instruments +
  base receipts), `b8260107` (gate cases + SKILL block), `b00419fb` (C2 repair + disclosure) and
  `6037f599` (record/closure: `LOG.md`, `SCORECARD.md`, `corpus/`, claims, round-80 `l1/scores/`) —
  the sanctioned integration route. **The tracked tree is clean at `6037f599`**; the two earlier
  working-tree modifications (`M corpus/SOURCES.md`, `M .ufo/waves/round-79/l1/scores/c2-at-landing.json`,
  the latter a disclosure-only `reason` edit) were integrated by that commit. No seat-authored
  change to `tools/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or `plans/`
  is visible outside the L1's commits.
- **`/tmp` writes after 10:35 belong to other lanes** (`kama-r82`, `r83`, `alma`, `mori-r87`
  artefacts). The only *code path* to `/tmp` in this wave is finding P1.
- **Observation B1 (low) — a compiled artefact inside a seat dir**:
  `.ufo/waves/round-80/w1/ExecBinder/__pycache__/pointer-bind.cpython-314.pyc` (an import without
  `-B`). Inside its own dir, so not a bound breach; it is binary noise in the evidence tree.
- **Observation B2 (low) — one stale evidence artefact was rewritten mid-wave.**
  `ExecProv/selftest.txt` recorded `SELFTEST cases=19 failures=3` against the 10:46:24 revision of
  the candidate; the instrument changed at 10:46:52 and the file was rewritten at 10:47:17 to
  `failures=0`. Nothing in the landed tree depends on it, but a retained selftest log without the
  instrument digest cannot be tied to a revision.

## 5. forgery_limit

`--validate` is a **consistency** check in all four instruments, never an authenticity check.
Demonstrated, not argued:

| instrument | what `--validate` re-derives | proven forgery |
|---|---|---|
| `pointer-bind.py` | counts, `duplicates`, per-check `line_sha256` non-empty, `path_is_declared`, 1-based range, `delimiter_evidence` shape, `record.rev` 40-hex, instrument digest == its own file | a hand-authored receipt with 5 checks, `line_sha256 = d*64`, `record.rev = e*40`, `record.sha256 = f*64` → `{"defects": [], "checks": 5, "matched": 5}`, exit 0 |
| `strictness-battery.py` | `false_greens`/`green_refusals` from its own red/green rows, `cases` from its own `fixture.red_ids`, `ok` implies candidate 0/0 and control == 4 | a receipt may carry any rows and `candidate.false_greens 0`; nothing re-reads the fixtures or either impl |
| `receipt-provenance.py` | `receipts/flagged/expected/unexpected` from `rows`, `ok` from `unexpected`, `rev` 40-hex, instrument digest; and one non-empty guard: `ok true over an empty population` | a fabricated row `{receipt: …/invented.json, instrument: tools/round-70/invented.py, sha256: b*64, verdict: bound, matched_rev: c*40}` → `defects []`, exit 0. (The landed version *does* reject `receipts 0` with `ok true` — an improvement over the earlier candidate, which accepted it.) |
| `guard-battery.py` | `guards/rows/bound/survivors_count` from its own lists, killed entries must have `present && failed`, pristine summary present, `rev` 40-hex, instrument digest | the validator never reads the repo, so a receipt with fabricated `clauses`/`table_rows`/`per_clause` and a consistent `ok` would validate; only the **run** binds |

What *does* bind to an artefact is the run itself:
- C1 reads `PROVINCE.md` at the resolved `--rev` and the five live files;
- C2 reads the receipts and instrument blobs **from git at `--rev`**, `git rev-list --all -- <path>`,
  never the working tree, and refuses a symbolic `--rev`;
- C3 reads the gate and `SKILL.md` blobs at `--rev` and executes one mutant per clause.

A receipt is therefore **reproducible, not authenticated**: a reviewer must re-run the same command
at the same `rev`. Two shapes are still unguarded by the instruments themselves and depend on the
reviewer reading the counts:
- **empty population (C2)** — only `ok true over an empty population` blocks the degenerate
  `receipts 0` receipt; a claiming receipt with a small population is caught only by the predicate's
  `receipts 34`;
- **empty clause set / fewer than nine guards (C3)** — `would_pass` requires `guards > 0`, not
  `guards == 9`. Reproduced: a one-clause gate with one row, one killed, zero survivors and a
  matched pin yields `ok true`, **exit 0**, `guards 1`. The frozen kill rule calls this
  empty-set gaming; the landed CLI has no `--expect-guards` (an earlier candidate did). Smallest
  remediation: require `guards == 9` in `would_pass` (or reinstate `--expect-guards` and pin it to 9
  in the counted command).

### Predicate reproducibility defect (C3)

The frozen sentence runs
`python3 -I -B tools/round-80/guard-battery.py --root . --rev <measured> --json-out <receipt>`
and requires `target_pin.matched true`. The landed CLI only sets that field when
`--expect-sha256 <digest>` is passed (`matched = bool(expect_sha256) and expect_sha256 == actual`).
Reproduced at `b00419fb`: the printed command exits 0 with `ok true` and `target_pin.matched false`
(`c3-at-head.json`); with `--expect-sha256 <gate digest>` it reports `true`
(`c3-at-head-pinned.json`). The L1's `l1/scores/c3-at-landing.json` carries
`expected == actual == df6fb856…`, so the landing arm used the flag — but the sentence as frozen
cannot be reproduced from its own command. Smallest remediation: append
`--expect-sha256 <gate blob digest>` to the frozen command, or default the expectation to the gate
blob at `--rev`.

Related shape mismatch: the receipt's survivor count is `survivors_count`, while the frozen sentence
says `survivors 0`; `survivors` in the JSON is the list.

## Findings (severity · evidence · impact · smallest remediation)

| # | sev | finding | evidence | remediation |
|---|---|---|---|---|
| P1 | medium | C1 battery defaults scratch to literal `/tmp` and `rmtree`s a fixed child | `tools/round-80/strictness-battery.py` `work = args.work or os.path.join(os.environ.get("TMPDIR", "/tmp"), "strictness-battery")`, `selftest()` likewise; frozen command omits `--work` | require `--work` or `tempfile.mkdtemp` |
| E2 | medium | provenance git children inherit the full environment | `receipt-provenance.py` `subprocess.run(["git", …], capture_output=True)` — no `env=`; `GIT_DIR`/`GIT_OBJECT_DIRECTORY` are reachable | pass the four-key `child_env`, record it |
| C3-a | medium | frozen C3 command cannot produce `target_pin.matched true` | `guard-battery.py` `matched = bool(expect_sha256) and …`; run without the flag: exit 0, `ok true`, pin false | add `--expect-sha256` to the sentence or default it |
| C3-b | medium | `survivors 0` reachable with fewer than 9 guards | one-clause synthetic gate → `ok true`, exit 0, `guards 1`; `would_pass` tests `guards > 0` | require `guards == 9` |
| L1 | low | scout receipt/probe keep all five pointed live lines verbatim | `ScoutRecord/receipt.json` `cells[i].pointed_line` + 4 derivative files | drop the bytes, keep `line_sha256` |
| E1 | low | C3 receipt records no child environment | `c3-at-landing.json` has no `child_env_keys` | add and gate on it |
| B1 | low | compiled `.pyc` inside a seat dir | `ExecBinder/__pycache__/pointer-bind.cpython-314.pyc` | delete; run with `-B` |
| B2 | low | a retained selftest log was stale until rewritten | `ExecProv/selftest.txt` 10:46:24 (`failures=3`) vs instrument 10:46:52 | record the instrument digest with the log |
| P2 | low | fixed `fixture-repo` name deleted under `--work` | `make_fixture_repo` `shutil.rmtree(work/"fixture-repo")` | `tempfile.mkdtemp(dir=work)` |

## Limits of this review

- I did not re-derive the *content* of the 34 historical receipts; I re-ran the sweep and checked
  its verdicts and counts against the frozen arms, plus a synthetic root for the hostile cases.
- The `/tmp` attribution for other lanes is by filename and mtime only; I read no other lane's data.
- The forgery demonstrations are receipts I authored under my own scratch; they show what
  `--validate` accepts, not that any filed receipt is forged.
- I did not exercise the C2 sweep under a hostile `GIT_OBJECT_DIRECTORY` (I did not want to
  manufacture object stores in the lane's git dir); the exploit path is stated from the code.
