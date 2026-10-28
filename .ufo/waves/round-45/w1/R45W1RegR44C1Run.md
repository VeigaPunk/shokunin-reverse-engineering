# R45-W1 — `tools/round-44/c1-run.sh`: registry row and exit-path verification

Seat `R45W1RegR44C1Run`. Measured rev `faa875bc0eb839d15b83c4afa6078819e5a7b381`;
freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`. Read-only with respect to the lane
tree: no edit to `SKILL.md`, `plans/`, `tools/`, `corpus/`, no git mutation. No tool was
installed.

Deliverables: `w1/R45W1RegR44C1Run/row.md` (the row), `receipt.md` (probes, hashes,
static citations), `probes.tsv`, `outputs/`, `pin-mismatch-manifest.json`,
`c2-counter-at-head.json`.

## The row

The exact 7-cell row is in `row.md` inside a fenced block; its first cell is
`` `tools/round-44/c1-run.sh` `` and its third cell names `0`, `1`, `2` with meanings.
It was validated against the frozen parser rather than by eye:
`c2-counter.py`'s `parse_rows` + `exits_ok` on the single row print
`cells 7`, `tool tools/round-44/c1-run.sh`, `exits_ok True`.

Measured exit contract (all probes in `receipt.md`):

- **0** — every carrier exited 0 and wrote its receipt, **or** `--dry-run` printed the
  plan and wrote nothing (`c1-run.py:952`). Probe: `--dry-run` → 0, 22 stdout lines,
  no manifest; `--help` → 0.
- **1** — at least one carrier failed (pin mismatch, REA exit ≠ 0, or no receipt;
  `c1-run.py:1045`). Probe: bad-pin carriers copy + `--carrier v1le` → 1, REA never
  invoked (scratch stayed empty), manifest `summary.failed=["v1le"]`.
- **2** — usage or environment refusal: `err()` (`c1-run.sh:43,45,52`), argparse usage
  error, missing lane root (`:819`), unreadable carriers (`:847`), `--carrier` matching
  nothing (`:853`), unknown scope ids (`:879`), committed-evidence-root refusal
  (`:835`). Probes: `--definitely-not-an-option` → 2, `C1_RUN_PY=/nonexistent` → 2,
  `--carrier NOSUCHCARRIER` → 2, bare `c1-run.sh` on the default evidence root → 2.

## Findings

1. **Yes, this script has an UNDECLARED 1 as well** — two, both reproducible without a
   data run, and both outside the header's `1 = at least one carrier failed`
   (`c1-run.sh:30`):
   - `env -u HOME bash tools/round-44/c1-run.sh --help` → **exit 1**, stderr
     `tools/round-44/c1-run.sh: line 50: HOME: unbound variable`. `set -u` aborts on the
     unguarded `$HOME` in `FIXED_PATH` (`c1-run.sh:32,50`); the `err()` contract (2) is
     bypassed because the abort is not routed through `err()`.
   - an uncaught Python exception propagates as 1: `--scratch /proc/kaidoku-r45-nope`
     → `FileNotFoundError` at `c1-run.py:841`, traceback, **exit 1**, no classification.
     `c1-run.py:1049-1050` has no top-level guard, so any unhandled `OSError` in the
     receipt writers is indistinguishable from "a carrier failed".
   The second class matters for scoring: a caller reading exit 1 concludes a carrier
   failed and may go looking for a receipt that was never attempted.
2. **The landed row already exists and passes the counter, but is inaccurate.** SKILL.md
   at HEAD (`e715263c`, amended `1f4b27f8`, line 1637) carries a row for this path. The
   frozen `c2-counter.py` at HEAD exits **0** (`met_target: true`, `unregistered: []`,
   `thin: []`, `scope_size: 6`, 45 registry rows): the claim's predicate is satisfied.
   My six deltas in `row.md` are accuracy, not scoring:
   - exit 1 also covers harness aborts (probes above);
   - exit 0 also covers `--dry-run`, which produces no receipt at all;
   - exit 2's set is broader than "`err()` in the script header";
   - the pinned-value cell names `corpus/evidence/round-44/c1/carriers.json`, **which does
     not exist**; the pin file is `tools/round-44/carriers.json` (`c1-run.py:111`), while
     `corpus/evidence/round-44/c1/` is the produced-evidence root (`c1-run.py:112`);
   - "plus the independent oracle arm" is not this script: `grep -c oracle
     tools/round-44/c1-run.py` → `0` (rc 1); the oracle is `tools/round-44/c1-oracle.py`,
     driven by the counter;
   - `--freeze` is recorded, never verified (`c1-run.py:784-785,897,965`); the freeze
     guard is an assertion flag (`--data-run`/`KAIDOKU_C1_DATA_RUN=1`), not a check, so
     "probe" is the right classification and "gate" would be wrong.
3. **Calibration consequence for R45-C2.** The frozen predicate checks path equality and
   that the third cell contains `\b0\b`, `\b1\b`, `\b2\b` (`c2-counter.py:59-60`), so a
   row that names a nonexistent pin file and omits two real exit-1 arms still scores
   green. This is a second instance of the claim's own declared limit (the counter does
   not check that the named instrument exists at `--rev`) extended to row content: it
   cannot check that the verdict map is *true*. If L1 lands my row it stays green —
   validated at parse level — but the counter cannot be the evidence that the map is
   correct; this receipt is.

## Not run

No data run (no `--data-run`, no `KAIDOKU_C1_DATA_RUN=1`, no REA extraction); the
default evidence root was untouched (`manifest.json` mtime 09:36:45 -0300, probes at
15:40–15:41 UTC). No self-test exists in either file (`grep -n selftest` → rc 1). The
frozen instruments were read/executed read-only; nothing under `tools/round-45/` or
`plans/round-45-claims.md` was modified.

## Risks / caveats

- Line numbers are at HEAD and at the freeze for the two instrument files (identical
  sha256 `c35d4b9b…` / `55e2692a…`), so the citations are stable while only `SKILL.md`
  moves.
- The pin-mismatch probe ran the real `c1-run.py` with a mutated carriers copy in scratch
  and a non-default evidence root, deliberately without `--data-run`. The pin gate sits
  before the subprocess call (`c1-run.py:358,979-984`), which the empty scratch tree
  confirms; it is not a data run and produced no receipt tree.
- Scratch `$S` was removed after `outputs/` was copied here.
