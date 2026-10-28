# R46W1RegM — receipt (round-46 C2 census rows, tag reg-m)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only).
Freeze: `31820472784284727546808acc31b3ea1e73919b`.
Scratch: `/fast/scratch/hyaku/kaidoku-r46/R46W1RegM` (`TMPDIR`/`HYAKU_SCRATCH`), removed at yield.
Installs: **none** (no package, tool or binary installed; pacman not touched).

## Blobs read at the freeze

| path | sha256 of `git show <FREEZE>:<path>` |
|---|---|
| `tools/round-41/sqfs-triage-v3.py` | `6ad2b4e1638a2b5f883d7bed14f8863ad5396dbc1af64b7cd521720ea42b6aa4` |
| `tools/round-43/c2-score-r43.py` | `459cbccbb2bf172376357b7e72549add1d99c5d9ed70fecc8acec1ea93432faa` |
| `tools/round-46/registry.py` (validator) | `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449` |
| `tools/round-46/gate.py` | `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` |
| `tools/round-46/census.json` | `573ec008fc3f9173da04589c013484485758e9cf1c901a254bf1d6286d62133e` |
| `plans/round-46-claims.md` | `a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01` |

Scratch copies of the two instruments are byte-identical to the freeze blobs (same sha256, verified).

## Command log (every command actually run)

`stdout sha256` is of the captured stdout; `e3b0c442…` is the empty-stream digest.

| # | command | exit | stdout sha256 | UTC | what it establishes |
|---|---|---|---|---|---|
| A | `python3 -I -B frozen/sqfs-triage-v3.py --selftest` | 0 | `57342801…` | 16:55:35Z | `SELFTEST cases=69 pass=69 fail=0`; the row's self-test cell is real and green |
| B | `… --table-only` (no `--skill`) | 2 | `e3b0c442…` | 16:55:30Z | `sqfs-triage-v3: --skill is required with envelopes or --table-only` → 2 = could-not-evaluate |
| C | `… --skill work/absent.md --table-only` | 2 | `e3b0c442…` | 16:55:30Z | unreadable document → 2, never 1 |
| D | `… --print-table` | 2 | `e3b0c442…` | 16:55:30Z | argparse rejects the removed v2 surface → 2 |
| E | `… --skill skill-ok.md --table-only` | 0 | `a9b3308c…` | 16:55:42Z | `rules: 1`; a valid v3 table is exit 0 |
| F | `… --skill skill-ok.md env-ok.json` | 0 | `390cf5f3…` | 16:55:42Z | one envelope → `env-ok.json\tclean\tnone`; the labelled path is exit 0 |
| G | `… --skill skill-v2.md --table-only` (v2 marker) | 2 | `e3b0c442…` | 16:55:42Z | `refused marker '<!-- sqfs-triage-table v2 -->'` → 2 |
| H | `python3 -I -B frozen/c2-score-r43.py` (no args) | 2 | `e3b0c442…` | 16:55:42Z | argparse: required `--root/--rev/--freeze/--scratch/…` missing → 2 |
| I | `python3 -I -B frozen/c2-score-r43.py --selftest` | 2 | `e3b0c442…` | 16:55:42Z | **unrecognized arguments: --selftest** — the tool has no self-test; `grep -c -- --selftest` on the blob prints 0 |
| J | `python3 -I -B frozen/c2-score-r43.py --help` | 0 | `fc8c933b…` | 16:55:42Z | CLI surface: 8 required/optional flags, no selftest flag |
| K | `c2-score-r43.py --root <empty dir> --rev deadbeef --freeze deadbeef --scratch … --upstream-dir … --tarball-67 … --tarball-65 … --json-out …` | 2 | `e3b0c442…` | 16:55:47Z | clone failure → receipt `exit_code 2`, `clone.exit 128`: 2 = could-not-evaluate |
| L | same, `--root <fixture repo containing only the tool>` at the fixture HEAD | 1 | `1cdc8006…` | 16:55:58Z | checks that run come back false → `checks_ok false`, `exit_code 1`: 1 = a check failed |
| M0 | `registry.py … --json-out /fast/scratch/…/rows-registry.json` | 2 | (overwritten by M) | 16:57:5x | `{"reason": "--json-out outside the lane root: …"}` — the counter refuses an out path outside `--root` |
| M | `registry.py --root <fixture d-rows> --freeze <rev> --rev <rev> --no-battery --json-out <fixture>/receipt.json` | 0 | `b17d5969…` | 16:58:13Z | **my two rows pass the frozen R46-C2 clause set**: `registered` = both, `unregistered []`, `thin []`, `absent_at_rev []`, `failing []`, `met_target true` |
| N | registry, verdict-map cell replaced by `0 of 1, 2` | 1 | `cf4e98fa…` | 16:58:21Z | `thin ['tools/round-41/sqfs-triage-v3.py']` — a prose cell binds nothing (discrimination control) |
| O | registry, cell 0 rewritten `see \`path\` (wrapper)` | 1 | `c01c871c…` | 16:58:21Z | `unregistered ['tools/round-41/sqfs-triage-v3.py']` — exact cell equality (discrimination control) |
| P | registry, honest rows restored | 0 | `5a008967…` | 16:58:21Z | control N and O were the only change; honest rows are green again |
| Q | registry with the battery, same 2-row fixture | 1 | `c6e4ca8a…` | 16:58:26Z | `battery v1_green 5 != 7`, `v2_green 0`, `forgeries_total 7`, `genuine_green 1` |
| R | registry with the battery, synthetic **full census** (38 rows, all 38 census paths present, `unregistered []`, `thin []`, `absent_at_rev []`) | 1 | `70b95e9b…` | 16:59:32Z | `failing ['battery v1_green 5 != 7']` — the red is independent of my rows: clause 6 is unsatisfiable |
| T | same 38-row fixture, `registry.py` **scratch copy patched** so `strict_cell`/`strict_exit` are gated on `profile v2` like `strict_header` | 0 | `5469a66f…` | 16:59:59Z | `v1_green 7`, `v2_green 0`, `forgeries_total 7`, `genuine_green 1`, `failing []` → root cause is the two ungated strict flags, not the artefact |
| U | `python3 - <rows.md>` structural checker | 0 | `ece92280…` | 17:00:27Z | `row1 cells=7 cell1_exact_path=True exitmap=['0','1','2']`, same for row2, `ROWS_OK count=2` |
| V | `… --skill skill-ok.md env-domain.json` (domain-mismatched envelope) | 0 | `8f157e11…` | 17:00:55Z | `env-domain.json\tunclassified\tnone` — no match is still exit 0, so 0 means "evaluated", not "labelled" |
| W | `grep -n "return 3\|return 4\|exit(3\|exit(4"` over both scratch blobs | 1 | (grep: no match) | 17:00:55Z | neither instrument returns an exit code outside {0,1,2}; also `len(receipt['checks']) == 13` for `c2-score-r43.py` (command L receipt) |

## Exit-code surface derived from source (not guessed)

`tools/round-41/sqfs-triage-v3.py` (`_run`, `selftest`, `main`): `0` = table parsed and the
requested output produced (`--table-only` rules, one `path<TAB>label<TAB>action` line per
envelope, `--json` payload) or `--selftest` all-cases-pass; `1` = returned **only** by
`selftest()` when a case fails; `2` = `TableError`/`EnvelopeError`/`InvocationError`
(missing craft section, missing/refused marker, malformed header/cell/vocabulary, unreadable
envelope, `--skill` omitted) plus argparse usage errors. No exit code outside {0,1,2} exists
in the file. Caveat recorded: a successful run that leaves every envelope `unclassified`
still exits 0 — 0 means "evaluated", not "each envelope got a domain label".

`tools/round-43/c2-score-r43.py` (`main`): `0` = all 13 `checks` true; `1` = `checks_ok`
false; `2` = the clone could not be made (early return) or a usage/argument error (argparse).
Calibration caveat: a sub-receipt that could **not** be produced at all (the wrapper or the
gate absent from the clone) is reported as `receipt-unreadable` with `wrapper_exit 2` but is
folded into `gate_exit_zero: false`, so the outer process exits **1**, not 2 — measured in
command L (`gate.error = "receipt-unreadable: …gate-receipt.json"`, outer exit 1). An
uncaught Python exception would also land on 1 for the same reason. The row's verdict map
words exit 1 to include that case rather than claiming a purity the source does not have.

## Row count: 2, not 3, and why

The seat spec says "three rows" but lists two instruments, and
`.ufo/waves/round-46/w1-spec.json` item `R46W1RegM` lists exactly those two. The census holds
38 paths for 13 registry seats, i.e. twelve seats own 3 and one owns 2; the round-41 group
has 13 paths and the round-43 group's fourth path (`c2-score-r43.py`) is the one left after
RegA/RegB/RegL took the other three — so this seat's assignment is structurally 2, and the
`three` in the prompt is stale boilerplate. Every other census path is already assigned to a
sibling seat (RegK: `mk-l-carriers.py`, `unblob-logtee.sh`, `gate.py`; RegL: `sqfs-list.py`,
`c1-counter.py`, `registry.py`), so a third row here would duplicate a sibling's assignment.
`rows.md` therefore carries the two verified rows and nothing else.

## Frozen-instrument finding (reported, not fixed)

`tools/round-46/registry.py` computes `battery.v1_green` with
`score(text, f, spec_name, "v1", frev)` while `score()` reads `strict_cell` and `strict_exit`
off `SPECS[spec_name]` **without** the `hard` guard that gates `strict_header`, the section
binding and the header check. With `--spec r46` (the counting command's default) the v1
profile therefore still demands exact cell-0 equality and a real `0=/1=/2=` map, so the
`substring-cell` and `prose-exit` forgeries are rejected by v1 as well: v1_green is at most 5
of 7 on any section (commands Q and R), while clause 6 requires 7. Consequence: clause 6 is
unsatisfiable and `registry.py` can never exit 0, so R46-C2's target is unreachable as
frozen — and `tools/round-46/` is frozen, so a fix is itself a `frozen_path_changed`.
Command T shows the minimal repair (gate both flags on `profile v2`) turns the identical
38-row section green (exit 0, v1_green 7, v2_green 0, genuine_green 1).

Secondary: `plans/round-46-claims.md` cites `controls/ctl-c2-1-v1-profile.json` for "the v1
clause set scores all seven forgery classes green"; that file does not exist. The nearest
receipt, `controls/ctl-c2-1-v1-scope.json`, is the round-45 counter (`round-45-c2`,
`scope_size 6`, no `battery` key) and measures a six-row scope, not a seven-class battery.

## Notes

- `git -C <fixture> rev-parse --show-toplevel` was asserted before each fixture commit
  (`/fast/scratch/hyaku/kaidoku-r46/R46W1RegM/work/d-rows` and `…/d-full`).
- No mutating git verb was run in the lane; the only commits were in scratch fixtures with
  a `fixture@local` identity.
- Nothing was written under `/tmp`; `TMPDIR`/`HYAKU_SCRATCH` pointed at the scratch root.
