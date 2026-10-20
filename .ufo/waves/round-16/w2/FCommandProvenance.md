# FCommandProvenance — round-16 producer command and documentation-red predicates

Scope: source and content read of `controls.py` (302 lines), `documentation-red.json`, and the docs those predicates read (`SKILL.md:450,487`, `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3,76-91`, `SHONEN.md:10`, `corpus/QUALITY.md` row 18, `corpus/lessons/round-16.md:56,61,91`), cross-checked against `round-15/verification.json`, `corpus/SOURCES.md`, `SCORECARD.md:88-124`, and `w1/NoHarmProducer.md`. Nothing built, tested, linted, or run as a producer. `controls.py` was not executed; no output for it exists. Predicate results are from the retained baseline record only.

Commands I ran, all read-only: `git show`/`ls-tree`/`for-each-ref`/`config --list`/`cat-file -t`/`status`, `grep`, `sed`, small `python3` JSON and text parses of retained files, and `env | cut` to list GIT_* variable names. No installs. No tool was installed or upgraded.

## Findings (severity order)

### F1 — MEDIUM: `producing_command_retained` is a false-green substring test
- `documentation-red.json` line 6 (the `-c` payload): `'producing_command_retained': bool(co) and 'argv' in co`.
- `controls.py` contains `argv` in at least 11 places, including the unconditional `"argv": sys.argv` at `controls.py:282`, `argv_note` at `:284-288`, and the docstring at `:13-14`. Deleting the `producing_command` key (`:292-294`) leaves this predicate green.
- The predicate also does not check `orig_argv`, `isolated`, or `executable`. It proves the word appears, not that the producing command is emitted.
- Calibration: `corpus/lessons/round-16.md:61` says the documentation red-before "is able to detect the named omissions." For this predicate that is false. The predicate is red at `6235498b` only because `controls.py` is absent there (`co == ''`), which is absence-based red, not omission-based red.
- Suggested tightening: require the emitted key names as literals, for example `'"producing_command"' in co and 'orig_argv' in co and '"isolated"' in co`. Or better, run the producer and check the JSON keys. Do not treat the current red-before as evidence the producing-command omission is detected.

### F2 — MEDIUM: producing command is cwd-relative and cwd is not recorded
- `controls.py:282-283` and `:292-294` record `sys.argv`/`sys.orig_argv` verbatim. The script is invoked by relative path in the usage line (`:4`), in `NoHarmProducer.md:11`, and in the L1 smoke command `NoHarmProducer.md:90` (`python3 -I .ufo/waves/round-16/controls.py 6235498b HEAD`).
- `invocation` has no `cwd` field. `repo_root` (`:291`) is the only location anchor. A reader cannot reconstruct the spelling without knowing the working directory was the repo root.
- This is the exact class routed by round-15 defect 1 (`corpus/lessons/round-15-verifier-spotcheck.md:185`), which the round's own correction treats as requiring an absolute path. `round-15/verification.json` `commands[2]` uses `python3 -I /home/.../snapshot-inventory.py`. The round-16 producer's own documented spelling does not meet that standard.
- Fix options for the author: record `os.getcwd()`, or record the absolute script path in `producing_command`, or document the exact absolute spelling as the only recorded form.

### F3 — MEDIUM: producer identity is not pinned in the output
- Top-level keys emitted: `revisions`, `log_old_prefix`, `old_lessons_prefix`, `old_knowledge_prefix`, `prior_verifiers_unchanged`, `frozen_baselines`, `craft`, `sources_registry`, `evidence_class`, `invocation`, `conformance_gate`. There is no SHA-256 or blob identity of `controls.py` itself.
- `controls.py` is untracked (`git ls-files .ufo/waves/round-16` is empty; `git status` shows `?? .ufo/waves/round-16/`). It is read from the worktree (`__file__`, `:30`), not from a revision. After the first commit, the report pins its inputs by commit but not the code that produced it.
- `corpus/QUALITY.md` row 18 (as drafted in the worktree) says structural tallies "retain the producer and immutable inputs." The producer half is not met by the emitted fields. The fix is to emit the script's SHA-256 (and ideally commit it before the L1 run).

### F4 — MEDIUM-LOW: `invocation_correction` predicate matches only the script path, not the argv that matters
- `documentation-red.json` line 6: `'python3 -I /home/.../round-15/snapshot-inventory.py' in kn`. The match ends at `.py'`. It does not check `--ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`.
- `w1/RegistryDraft.md` F3 states the omitted `--select` changes the selection (default `1.25.0 1.26.0`, `snapshot-inventory.py:66,414`). A regression that drops `--select` from the correction block would still be green.
- Current content is correct: the knowledge correction block (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:83`) and `SKILL.md:487` both carry the full retained argv, and I confirmed it byte-for-byte against `round-15/verification.json` `commands[2]` (`label: snapshot-inventory`). This is a predicate-scope defect, not a content defect.
- Append-only is not checked by the predicate. `git diff HEAD --stat` shows the knowledge file as 17 insertions, 0 deletions, so the actual edit is pure append. The predicate does not enforce that; `controls.py` `old_knowledge_prefix` could.

### F5 — MEDIUM-LOW: predicates read committed blobs; the round's changes are uncommitted
- `documentation-red.json` evaluates `git show <rev>:<path>` at `6235498b`. Current `git status` shows `M SKILL.md`, `M SHONEN.md`, `M corpus/SOURCES.md`, `M corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`, and `?? .ufo/waves/round-16/`. `controls.py` is untracked.
- Any post-integration predicate run must target a commit that contains all of these. Otherwise it stays red for absence, not for the omission it claims to detect. L1 needs to commit before the after-run, and the documentation-red record must name that commit.
- No after-green record exists in the wave. `lessons/round-16.md:61` says "the identical snippet is run after integration and retained with its revision." That is a future action, not evidence. Report only as pending.

### F6 — LOW: `resolve()` does not separate options from revision names
- `controls.py:62`: `git rev-parse --verify {name}^{commit}`. No `--end-of-options` and no `--`. A name beginning with `-` is parsed as a git option. The result is still a non-zero exit (exit 2) in the cases I could reason about, so the impact is small. `round-15` `measure.py` was flagged for the same hardening (`PathSafety.md` step 4 mentions `--end-of-options`). Low priority.

### F7 — LOW: Git environment disclosure is partial
- Docstring `controls.py:18-20` discloses `GIT_*` variables. It does not disclose:
  - `git` is resolved through `PATH` (`:49`, `subprocess` with bare `"git"`), so `python3 -I` does not isolate the git binary;
  - `refs/replace/*` objects are honored by `ls-tree`/`show` (no `GIT_NO_REPLACE_OBJECTS`), so "immutable object bytes" can be altered by replace refs.
- Host state now: `git for-each-ref refs/replace` returns 0 refs. Environment has `GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT` only; no `GIT_DIR`/`GIT_OBJECT_DIRECTORY`/`GIT_ALTERNATE_OBJECT_DIRECTORIES`. No active redirection on this host. Latent only.
- Recommend adding PATH and replace-ref behavior to the limitation sentence.

### F8 — LOW: exit contract is not honored on decode failures
- Docstring `controls.py:16-17`: exit 2 means usage error, unresolvable revision, or missing structural anchor; exit 0 means report completed.
- `Rev.__init__` decodes `ls-tree` output with `encoding="utf-8"` (`:51`, `:71`), `craft_section` calls `.decode("utf-8")` (`:110`, `:125`), `source_rows` calls `.decode` (`:137`). Only `CalledProcessError`/`OSError` are caught (`:72`, `:98`, `:63`). A non-UTF-8 path or SKILL.md/SOURCES.md blob raises `UnicodeDecodeError` and exits 1 with a traceback. Not reachable on the current tree (I did not run it; I checked by reading the bytes encoding of the retained SKILL/SOURCES rows, which are ASCII-clean in the cells I read; not exhaustively verified).

### F9 — LOW (latent): duplicate source IDs collapse silently in the immutable-row guard
- `controls.py:143-150` builds `{row[1].strip(): cells}`. For duplicate IDs the last row wins; `rows_before`/`rows_after` count unique IDs (`:236-237`). A duplicated row in `before` or `after` can hide a change to the earlier row.
- Current `corpus/SOURCES.md`: 23 rows, 0 duplicate IDs (checked by parse). Latent only.

### F10 — LOW (host-inert): inconsistent `orig_argv` fallbacks
- `controls.py:283` falls back to `sys.argv` (no interpreter). `:293` falls back to `[sys.executable, *sys.argv]`. On Python < 3.10 the two fields disagree about the interpreter. Host is Python 3.14.7 (`python3 --version`), so not triggered. Harmless to unify; no action required for this round.

### F11 — LOW (stale draft): `w1/NoHarmProducer.md` describes behavior the code does not have
- `NoHarmProducer.md:20-21` says `producing_command` is "rendered with `-I` only when actually used"; `:57-59` says "Now the command interpolates `sys.flags.isolated`."
- Actual code (`controls.py:292-294`) uses `shlex.join(sys.orig_argv)`. The lesson text (`lessons/round-16.md:91`) matches the code, not the draft. The draft is uncommitted; the risk is that the entry repeats the stale description. Correct it before integration.
- `NoHarmProducer.md:11` documents the spelling as `python3 [-I] …` (optional `-I`). Round-15 defect 1 asked for either alignment or an explicit named variant. An optional bracket is neither. Use the exact retained spelling.

### F12 — NOT A DEFECT (recorded for calibration): isolation is recorded, not required
- `controls.py:290` records `isolated: bool(sys.flags.isolated)`. A non-isolated run still exits 0 and emits a complete report with `isolated: false`. This is consistent with the documented no-gate design (`:296`, `conformance_gate: False`). L1 must read `invocation.isolated` in the record and must not infer isolation from the exit code.
- `controls.py` needs no local imports, so `-I` changes only environment and `sys.path` handling. The isolation claim is about provenance, not correctness.

## No-finding checks (bounded)
- `USED_BY_COLUMN = 11` (`controls.py:45`) matches the SOURCES header: `split('|')` gives `['', 'id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches', 'status', 'opened', 'recheck', 'used-by', '']`, so index 11 is `used-by`. All 23 rows have 13 cells.
- `craft_section` (`:110-133`) replicates SCORECARD command A's knowledge-range check (`SCORECARD.md:88-124`) for the same regex, same `int(first or 1)` / `int(last or first or 1)` semantics, and same `1 <= start <= end <= count` rule. Command A's bare-path raise maps to `valid=False` here. Equivalent on the cases I traced.
- The knowledge correction argv (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:83`) matches `round-15/verification.json` `commands[2]` exactly (`label: snapshot-inventory`). The `inventory-determinism` label cited in the correction exists at `commands[3]`.
- `SKILL.md:450` row contains `.ufo/waves/round-15/boundary-fixtures/expected.json`; `round-15/verification.json` `commands[8]` ran that baseline with `--frozen` and exit 0. Discoverability claim matches.
- `SKILL.md:487` `go-snapshot-inventory` row now carries `python3 -I` absolute path and `--select`. Routed defect 1 is discharged in the registry as well as the knowledge file.
- `SHONEN.md:10` names "historical 2026-10-15 operator-steered round 1," matching routed defect 4.
- `sys.orig_argv` (Python ≥ 3.10) includes interpreter flags; `shlex.join` produces a POSIX-quoted string; `ROOT = Path(__file__).resolve().parents[3]` is the repo root for an in-tree invocation. Correct on 3.14.7 by reading the CPython contract; not executed.

## Residuals not in this seat's scope
- Historical lines still carry non-isolated spellings: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3`, `SCORECARD.md:2247`, `corpus/lessons/round-12.md:34,39`, `corpus/lessons/round-14.md:105,115`. Round-15 `verification.json` also records three non-`-I` invocations (`measure-before`, `measure-after`, `citation-strict`, per `w1/CriterionDraft.candidate.md:14`). These are historical; QUALITY #18 governs future guidance. Recorded here so the wave does not overstate "all invocations now use `-I`."

## Limits
- No run of `controls.py`, `documentation-red` predicate, `selection.py`, or `selfcheck.py`. All findings are read-only source/content findings.
- The F1/F4 false-green claims are derived by reading the predicate expressions against the file text; I did not execute the predicate against a mutated copy.
- F8 is by reading the encoding calls, not by feeding non-UTF-8 input.
- No judgment on semantic correctness of the corrections or the SHONEN/QUALITY wording beyond the predicate scope.
- Other seats own `selection.py` and `selfcheck.py` source-law behavior; I did not evaluate them here.
