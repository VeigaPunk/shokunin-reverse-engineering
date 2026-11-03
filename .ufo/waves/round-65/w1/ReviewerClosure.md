# Seat report — ReviewerClosure (round 65, w1)

Read-only review of the R65-C1 closure instrument
(`tools/round-65/jsc-closure-matrix.py`, re-hashed `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`,
514 lines) against the frozen predicate and round 64's blocking findings F1/F2.
The matrix was not run; no scratch was created; nothing was written outside the seat
report directory and this file. No LSP server was available for the file (no lsp
device in this session) — all checks are text reads plus programmatic comparisons
(importlib constant load; read-only globs/greps over the toolchain tree).

## Answers (full detail in `.ufo/waves/round-65/w1/ReviewerClosure/review.md`)

- **Q1 closed.** Derived import closure (`^(import|from)` over
  `~/.local/share/kaidoku-jsc/jsc2js-src/View8`): the `--disassembled` route imports 9
  in-tree files — all pinned; no `__init__.py` exists (namespace packages); the View8
  dir holds exactly 12 files, all pinned; each d8 dir holds exactly `d8` +
  `snapshot_blob.bin` + `icudtl.dat`, all pinned; probe/typora/node/resolved-interpreter
  pinned. Spawned executables (3× d8, venv python, node) all pinned.
  Read-but-unpinned: interpreter stdlib/site bootstrap only (outside root and census;
  no `*.pth`, site-packages = parse only). Pinned-but-never-read: 6 of 30 (README.md,
  Bin/VersionDetector.exe, Parser/parse_v8cache.py, `__init__.pyi`, METADATA, RECORD) —
  harmless over-pinning, named as the question requires.
- **Q2 closed.** Exclusion is `jsc2js-src/.git/` (L77, applied L215-216). It can only
  hide a write into that directory; the run spawns only d8/python/node (none writes git
  metadata) and never invokes git — formal blind spot, no realistic hidden write.
  Census skips symlinks (L212) and is root-scoped; mtime-only rewrites invisible and
  stated (docstring L31-32).
- **Q3 closed.** `cache_entries` (L193-203) detects both `__pycache__` dirs and `*.pyc`;
  folded into `closure_findings.ok` (L244/L250-251/L254); fires on the operative path
  before any mutation (run gate L287-290 exits 2 before `work_root.mkdir` L304 and the
  before-census L305; `--manifest` exit 2 L500). Tree verified cache-free now (globs).
- **Q4 closed.** Predicate proven byte-identical across all three artifacts
  programmatically: plan L29-33 (quote-unwrapped) `==` claims.json L15 `==` instrument
  PREDICATE L68-73, both comparisons True.
- **Q5 closed.** `--skip-run` reachable (L501, before the required-args check L506-509),
  records 0/18 and exits 1 (`emit` L346-353). It does bypass the closure check —
  L502-505 fabricate `ok:True`/equal census — but L347's `and not skip_run` makes
  verified/exit 0 unreachable: not a claim hole; advisory A2 (synthetic receipt fields
  must not be cited as closure evidence).
- **Q6 closed.** Verdict (L175-190) requires exact string equality with the 18 frozen
  labels; `dump-ok` needs rc 0 + SFI marker (L145-153), `view8-ok` needs rc 0 +
  non-empty output (L156-162), skipped states arise only where predictions expect them
  (L169-172); `not-run` never equals a prediction. Semantic limit (frozen from r64,
  unchanged): the predicate certifies label reproduction, not reconstruction fidelity —
  probe rows predict `node-fail`, so content correctness is out of scope by design.

## Defects

Blocking: **none**. r64 F1 (unpinned D2/D3 snapshot/icudtl variants, View8 tree, node,
venv) and F2 (`__pycache__` into the frozen tree) are both repaired in this instrument.

Advisory (A1-A9, detail with lines in review.md): A1 `--manifest` without `--probe`
pins PROBE_PIN against the Typora artifact → guaranteed wrong-reason exit 2 (L496) —
every manifest call must pass `--probe`; A2 skip-run receipt's closure/census blocks are
synthetic; A3 carried r64-F4 (uncaught view8/node timeout/OS errors → exit 1 traceback,
no receipt, no false pass); A4 TOCTOU narrowed (after-census now covers all 27 root
entries; probe/node/interpreter outside the root remain single-check); A5 census skips
symlinks (unpinned `venv/bin/python` link); A6 stdlib/site unpinned (closure complete
only within the toolchain root); A7 docstring overstates env/-B coverage (Python spawns
only); A8 claims.json A3 miscounts venv identity files as 4 (map has 5; 27 total is
correct); A9 the 6 over-pinned entries.

VERDICT: instrument fit for the operative run; Q1-Q6 closed, nine advisory findings,
none blocking; enforce `--probe` on every `--manifest` invocation (A1).

Report: .ufo/waves/round-65/w1/ReviewerClosure.md
