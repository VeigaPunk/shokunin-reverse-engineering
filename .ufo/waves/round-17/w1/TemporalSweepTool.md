# TemporalSweepTool — temporal-sweep.py implementation report

Seat: KaidokuR17.TemporalSweepTool-3 (wave 1, round 17). Scope: implement the
contract.md `W/tools/temporal-sweep.py` section only.

## Files changed
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/temporal-sweep.py`
  (new, executable, Python 3 stdlib only; only file written besides this report)

## Implementation (contract anchors)
- Site sources, site regex, correction sources, marker, output fields, and exit
  codes implemented verbatim from `.ufo/waves/round-17/contract.md:90-96`.
- `git show REV:path` object reads only (`temporal-sweep.py:60-77`); absent
  paths are distinguished from read failure via `git cat-file -e` and contribute
  zero lines — no error.
- `--rev` resolved with `rev-parse --verify REV^{commit}` (`:112-121`); the
  canonical hex is emitted as `rev`, the caller string as `requested_rev`.
- `corrected` iff a correction-source line contains literal `R16-PROVENANCE`
  and the site's repo-relative path (`correction_hits`, `:89-99`); one
  correction line corrects every site in the named file (per-file granularity —
  the contract names only "the site's repo-relative path").
- `--extra` files read from disk, included in correction scanning; unreadable →
  exit 2 (`:123-131`).
- Output: `{rev, requested_rev, root, site_sources, correction_sources,
  extra_files, corrected_paths, sites[{file, line, file:line, text,
  corrected}], counts{sites, corrected, unqualified}}`, `sort_keys=True,
  indent=2`. Exit 0 reported, 2 bad input/unreadable/git failure; exit 1 unused
  (contract assigns 1 only "where stated", and does not state it here).

## Runs (each executed once)
- `--selftest` → `SELFTEST: CLEAN cases=6`, exit 0. Cases: 3 sites / 0
  corrected on rev1; named LOG.md correction → 1 corrected / 2 unqualified on
  rev2; `--extra` adds a second correction; absent-source tolerance; bad rev →
  exit 2; unreadable `--extra` → exit 2.
- Baseline run `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev
  b563c799d97774aae4351276fe43cb897311e349` → exit 0, counts
  `{"sites": 2, "corrected": 0, "unqualified": 2}`:

  | file:line | text | corrected |
  |---|---|---|
  | `corpus/lessons/round-16.md:154` | `All producer/fixture pins remained unchanged during execution.` | false |
  | `.ufo/waves/round-16/verification.json:419` | `"pins_unchanged_during_run": true,` | false |

  Independently confirmed by direct grep on the same git objects: exactly these
  two matches; zero `R16-PROVENANCE` lines in LOG.md/SCORECARD.md at that rev;
  `corpus/lessons/round-17.md` absent (expected — the round-17 lessons file is
  new this round). LOG.md and SCORECARD.md contain no literal matches for the
  four site patterns at baseline (observation: the pattern vocabulary is narrow;
  e.g. SCORECARD phrasing that does not use these exact strings is invisible to
  the sweep — matches the contract regex, noted for L1 calibration).

## Observations vs inference
- Observation: C1 baseline candidate = 2 unqualified sites, both uncorrected;
  the falsifiable target `N -> 0` needs two named corrections.
- Inference: a correction authored in `corpus/lessons/round-16.md` itself would
  NOT count — round-16.md is a site source, not a correction source; corrections
  must land in LOG.md, SCORECARD.md, corpus/lessons/round-17.md, or an `--extra`
  file, and must name the repo-relative path (e.g. `LOG.md`) on the same line as
  `R16-PROVENANCE`.
- Inference: `verification.json:419` can only be marked corrected by a naming
  correction line (the committed JSON blob is immutable history); its text is a
  retained field name, so the correction wording must explicitly map it (e.g.
  "map matches only endpoint bytes").

## Limits
- No tool installs; no deps beyond stdlib + git binary.
- Did not run REA, Ghidra, any carrier binary, or another seat's tool.
- Reported checks: `--selftest` and the single baseline run above; no other
  verification executed (L1 owns post-integration re-runs).
- The regex is fixed by contract; semantically equivalent but differently
  worded claims are out of scope by design.
