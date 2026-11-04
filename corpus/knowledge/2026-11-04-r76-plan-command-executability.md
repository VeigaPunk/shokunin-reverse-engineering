source: S286 (https://docs.python.org/3/library/shlex.html#shlex.split) and S287 (https://docs.python.org/3/library/argparse.html); instrument `tools/round-76/plan-command.py`; receipts `.ufo/waves/round-76/l1/scores/c2-at-landing.json`, `.ufo/waves/round-76/pre/r75-printed-exec.txt`
verified-at: 2026-11-04
recheck: `python3 -I -B tools/round-76/plan-command.py --root . --rev <rev> --work <scratch> --battery`

# A printed counting command is a runnable artifact, or it is prose

Round 75 printed its R75-C1 counter in the report as

```
python3 -I -B tools/round-75/probe-mutation.py --root . --rev 538b8b81 --tool
tools/round-75/seam-probe.py --patch-set r75probe --expect-survivors 0
--expect-target-sha256 1fc1c8fc… --expect-sole b-drop-canary-field
```

Pasted as printed it does not run: the digest is abbreviated with a Unicode ellipsis and no `--work` is given, so
the instrument's own preflight answers `{"unevaluable": "missing required arguments: work"}` at rc 2
(`.ufo/waves/round-76/pre/r75-printed-exec.txt`). The number the report printed was real — it came from a run whose
full argv lived only in the L1's shell — but a reader of the record could not reproduce it.

## What the gate does

`tools/round-76/plan-command.py` reads a fenced `sh` block between `<!-- counting-command: NAME -->` markers out of
a committed plan, and makes that block the command it executes:

1. **Static grammar before any execution.** Every `<...>` placeholder, every ellipsis abbreviation and every
   variable outside `$REV`/`$WORK`/`$OUT`/`$ROOT` is refused (`PLACEHOLDER_UNBOUND`, `VARIABLE_UNBOUND`), and the
   shell metacharacters `;`, `|`, `&`, `$(` and the two redirect signs are refused outright (`SHELL_METACHAR`).
   A refused block is never executed — the round-75 printed command is refused at this step, not at rc 2.
2. **No shell.** The block is tokenised with `shlex.split` and run with `subprocess.run(argv, shell=False)`. S286
   grounds what that buys: the documented splitter is *shell-like* syntax, not a shell grammar — it produces
   tokens and performs no expansion, substitution, globbing or execution. A block that carries a shell construct
   is therefore refused, never silently interpreted.
3. **A four-key child environment.** `PATH`, `HOME`, `TMPDIR`, `LANG` only, with `HOME` and `TMPDIR` created inside
   the work root, and `$WORK`/`$OUT` resolved through `realpath` + `commonpath` against that root before the run.
4. **The counter is read from the receipt the command wrote.** `--counter-field` selects a dotted path in the
   receipt JSON and the value is compared with the declared target.
5. **Executability is separable from a counter's value.** The battery's green arm accepts rc 0 or 1 and requires an
   integer in the counter field: whether the number is right is the other claim's business, so two claims can be
   scored without reading each other.

## Why rc 2 is the right before-arm

S287 documents the parser's error path: an invalid invocation "terminates the program with a status code of 2".
The round-75 command's missing `--work` is exactly that case, so the observed rc 2 is the documented outcome of
the printed command, not an instrument quirk. The gate's `r75-argv` arm binds the digest (so the static grammar
passes) and still observes rc 2 with the missing-argument message: the two failure modes are separable and each
is named.

## Limits

- The gate is not a shell parser and does not claim to be: it refuses shell constructs instead of interpreting
  them. `shlex.split` accepts quoting forms a shell would also accept; that is a tokenisation overlap, not a
  shell-semantics claim.
- The allowlist is a lane-relative `tools/` prefix (fixtures declare `tools/round-75/`); a plan block that names
  any other script is refused. This is a policy bound, not a sandbox.
- Executing a committed document's bytes is a trust boundary: a plan block is code. The gate reduces the surface
  (fixed argv head, no shell, four-key env, containment) but does not authenticate the plan's author.
- The counter comparison is exact string equality on the JSON value; a receipt that carries the counter as a
  string `"0"` and a declared target `0` match, and a float does not. That is a deliberate strictness, recorded
  here so a reader does not read it as semantic equality.
