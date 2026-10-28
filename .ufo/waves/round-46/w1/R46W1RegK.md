# R46W1RegK — reg-k registry rows (round-46 C2 census)

Seat: round-46 wave 1, tag `reg-k`. Deliverable: three ready-to-paste instrument-registry
rows for `tools/round-41/mk-l-carriers.py`, `tools/round-42/unblob-logtee.sh` and
`tools/round-46/gate.py`, each derived from the frozen source and each claim backed by a
command actually run. Lane tree read-only; nothing outside this directory was written.

## Delivered

| artefact | sha256 |
|---|---|
| `.ufo/waves/round-46/w1/R46W1RegK/rows.md` (3 rows, exact 7-cell house format) | `c0b4be1ae77dd7166050f6d5242b28ec842d0dc41e7702875b8f1cf6368c3e35` |
| `.ufo/waves/round-46/w1/R46W1RegK/receipt.md` (38 probes + hash-checked replay) | `359370c309a1c0166d93551eab9725202ff825520bfab0da9639ff3a7f68405b` |

Instrument bytes read at freeze `31820472784284727546808acc31b3ea1e73919b`:

| path | sha256 at the freeze | lines |
|---|---|---|
| `tools/round-41/mk-l-carriers.py` | `fa2debc06264cf9decd590c74eb64f0b7aa5d1e3b3a4c3835ae633ec26232205` | 282 |
| `tools/round-42/unblob-logtee.sh` | `a1f26ec59214e09237d0826ff86e05fec7440fd9f7a2d789a9a0215e0e4c23c4` | 29 |
| `tools/round-46/gate.py` | `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` | 225 |

All three are in `tools/round-46/census.json` (`paths` length 38, `named_but_absent []`,
membership checked by command, exit 0), and all three resolve at the freeze
(`git show <freeze>:<path>` exit 0), so clause 5 (`absent_at_rev == []`) holds for them.

## Row format, verified by the frozen counter's own parser

`rows.md` was scored with `registry.score(..., spec_name="r46", profile="v2")` from the
frozen `tools/round-46/registry.py`, with the census replaced by exactly these three paths
(probe 38): exit 0, `registry_rows 3`, `unregistered []`, `thin []`, `absent_at_rev []`,
`failing []`. A separate shape probe (probe 37) reports, per line,
`cells=7 backticks=2 cell0=<backticked path> exitmap=['0','1','2']` — so every row has
exactly seven cells, exactly two backticks (cell 1 only), and a verdict map that binds all
three codes under the counter's `\b([012])\s*[=:]` test.

## How each exit map was derived, and how it was exercised

### `tools/round-41/mk-l-carriers.py`

Source: `main()` returns `0` at the end; `2` for `writer not found`, `outdir must exist and be
empty`, `outdir is not empty` (and argparse's own usage error); `3` when `build()` yields
`None` (a spec problem or a non-zero writer); `4` when build 2 differs from build 1. There is
no `return 1` anywhere in the file.

Exercised: `--help` → **0**; no arguments → **2**; missing outdir → **2**; non-empty outdir →
**2**; `--writer /no/such/writer` → **2**; full build `--lane <lane> --builds 2 --json …` →
**0** with `L3 build2-equal`/`L4 build2-equal` on stderr and the TSV
`L3 xz 04cfb4cd… 187892 13 3 20`, `L4 gzip 4c0e5459… 169545 14 3 17` on stdout; stub writer
exiting 3 → **3**; writer writing 64 random bytes → **4**; writer exiting 0 without writing
the image → **1** (uncaught `FileNotFoundError` at the sha256 read).

The `1` arm is real, so the row does not claim the tool never emits it: it says 1 is never a
verdict and is reached only by an uncaught exception. This differs from the round-46 counters,
which wrap every entry point in `gate.main_guard`; `mk-l-carriers.py` has no such guard, so a
crash there would read as "not met". Recorded as a calibration fact, not a defect to fix in a
frozen round-41 file.

The `--builds 2` arm is a determinism check, not a selftest — the row says `none` and names
the flag with its own observed rc.

### `tools/round-42/unblob-logtee.sh`

Source: `2` is the script's only own verdict (`C1_REAL_UNBLOB` must be an absolute path);
otherwise it runs `"$real" "$@"`, keeps `rc=$?`, copies the log only when
`[[ -n ${C1_LOG_COPY:-} && -n $log && -f $log ]]`, and `exit "$rc"`. It has no notion of
met/not-met, so the row states that 0 and 1 are the wrapped unblob's codes propagated
unchanged.

Exercised: relative `C1_REAL_UNBLOB` → **2**; stub unblob exiting 5 with `C1_LOG_COPY` set and
the `--log` file written → **5**, argv recorded byte-for-byte as `-e <input> --log <log>`
(`--log` and its value untouched, arguments not reordered), copy body
`extractor: sasquatch -le`; the same without `C1_LOG_COPY` → **5**, no copy; `C1_LOG_COPY` set
but the stub writes no log file → **0** and no copy created (the `-f $log` conjunct);
absolute-but-missing binary → **127**.

### `tools/round-46/gate.py`

Source: `freeze_state()` returns `0` when the history arm and blob arm agree and the freeze is
an ancestor, `2` for an unknown revision, a non-ancestor, a missing claims file or
`## Frozen paths (exact)` section, or a failing `git log`; `main_guard()` converts any
exception to `2`; `out_path()` returns `(None, reason)` for a refused target; `scratch()`
returns `(None, reason)` for a `/tmp` or `/var/tmp` root; the module's `__main__` is
`sys.exit("gate.py is a library; use attest.py or registry.py")`, i.e. **1**. No library entry
point returns `1`.

Exercised: module run as a program → **1** with that message; `freeze_state(lane, F, F)` →
**0**, `frozen_derived ["tools/round-46/", "plans/round-46-claims.md"]`,
`frozen_path_changed []`, `restored []`; unknown rev → **2** `unknown rev revision`; the round's
base `5382acc8` as rev → **2** `freeze is not an ancestor of rev`; `out_path` → refused for
`SKILL.md` and `tools/round-46/x.json` (`inside a graded or frozen surface`), accepted for
`.ufo/waves/round-46/w1/ok.json`, refused for `/tmp/x.json` (`outside the lane root`);
`HYAKU_SCRATCH=/tmp` → `scratch root is a temporary partition`; a raising callable through
`main_guard` → **2**.

## Exit codes outside {0,1,2} (reported here, deliberately not in the rows)

- `mk-l-carriers.py`: **3** (writer failure or a spec problem) and **4** (determinism failure);
  additionally **1** on any uncaught exception, as exercised above.
- `unblob-logtee.sh`: whatever the wrapped unblob returns — **5** observed — plus **127** when
  `C1_REAL_UNBLOB` is absolute but absent (bash's own "not found"). Neither is a lane verdict.
- `gate.py`: no code outside {0,1,2}.

## Findings for the L1 (nothing edited; the frozen bytes are the rule)

**F1 — the v2 section does not exist yet, and the existing headers are not the house schema.**
At tip `87578656`, `SKILL.md` contains **0** occurrences of `<!-- instrument-registry v2 -->`
and **0** of `<!-- /instrument-registry -->`. Its four registry headers (lines 1573, 1616,
1644, 1670) are all `| tool | gate or probe | verdict map (exit codes) | self-test command |
pinned-value path | write scope | owner |`, i.e. cell 1 is `gate or probe`, not the house
schema's `gate or probe - purpose`; compared against `registry.HOUSE` each is `False` (command
in this seat's transcript, exit 0). Consequences for landing C2: the markers and the exact
seven-cell header must be written fresh, and because rows register only *between* the markers,
the six round-44/45 rows (which are in the census) do not carry over — they need rows inside
the marked section as well, or `unregistered` will be non-empty on their six paths.

**F2 — the claims file's registry selftest prose is not reproducible as written.**
`plans/round-46-claims.md:194` says `registry.py --selftest` prints `cases=11 failures=0`.
Measured: bare `--selftest` exits **2** (argparse requires `--root`, `--freeze` and `--rev`
before the flag is honoured), and with those three supplied it prints
`REGISTRY_SELFTEST: cases=12 failures=0` (exit 0). Two differences: the missing required
arguments and the case count (12, not 11). The file is frozen, so this is reported, not
changed. Effect on the C2 target: none — no predicate clause reads the selftest count; clause 6
reads the forgery battery. It is a satisfiability-preflight accuracy defect.

**F3 — `gate.py`'s `1` is a misuse signal, not a violation.** A row that read
`1=not met` for `gate.py` would be false: the sole `1` is program-mode refusal. The landed row
says so explicitly, so the registry does not advertise a verdict the core cannot emit.

**F4 — round-46 counters refuse `--json-out` outside the lane root.** `gate.out_path` accepts
`<lane>/.ufo/...` and refuses `<lane>/SKILL.md`, `<lane>/tools/...` and anything outside the
lane, including scratch (verified above). Executors who follow "write receipts under
`$HYAKU_SCRATCH`" literally will get exit 2 from `attest.py`/`registry.py`; the JSON receipt
must be written inside the lane and copied, or generated there directly.

## Coverage and limits

- Covered 3 of the census's 38 paths; the other 35 belong to sibling reg seats.
- Not run: `tools/round-46/attest.py` (not this seat's instrument), the forgery battery (it
  requires the complete section with all 38 rows), and `mk-l-carriers.py`'s spec-problem arm
  (reachable only by editing `TREES`; by source it returns the same 3 as a writer failure —
  `[INFERENCE]`, not observed).
- Probe 30's stdout hash cannot repeat because `gate.scratch()` uses a random `mkdtemp`
  suffix; the receipt verifies its four `out_path` lines literally and records the drift.
- Every probe number's exit in `receipt.md` was re-read programmatically and matches the
  semantic claimed in its row; the replay appendix reports `all hashes matched`.

## Lane hygiene

- Wrote only `.ufo/waves/round-46/w1/R46W1RegK/{rows.md,receipt.md}` (this file included).
- `git -C <lane> status --porcelain -- SKILL.md plans tools corpus LOG.md SCORECARD.md
  PROVINCE.md SHONEN.md` → empty, exit 0: no frozen or graded byte touched.
- No installs were needed; python3 3.14.0, git and sha256sum were already present. Nothing was
  written under `/tmp`; the `/tmp` probe is a refusal test that creates nothing.
