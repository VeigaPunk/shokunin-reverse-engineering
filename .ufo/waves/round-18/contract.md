# Round 18 shared implementation contract (L1-authored, 2026-10-20)

All paths absolute. `LANE` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `W17` = `LANE/.ufo/waves/round-17`;
`W18` = `LANE/.ufo/waves/round-18`; baseline `B` = `9011581d84527ba34c675f9cf912e54d2e72d470` (branch `main`).
Go data: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`; Ghidra source:
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`.

Tools: Python 3 stdlib only, `#!/usr/bin/env python3`, runnable as `python3 -I -B <abs path> ...`, JSON on
stdout (`sort_keys=True, indent=2`), exit 0 emitted/clean, 1 failed/mismatch (only where stated), 2
could-not-evaluate. Never execute a carrier binary. No network unless the item says so. Each new tool has
`--selftest` that builds fixtures under `tempfile.mkdtemp()` (outside LANE), removes them, prints
`SELFTEST: CLEAN cases=N` or `SELFTEST: FAILED ...`, exits 0/1, and includes at least one red case that
must fail for the named reason. Executors MAY run their own tool's `--selftest` and read-only runs named in
their item; never REA `analyze`/`search`/`decompile`, never Ghidra/analyzeHeadless (the L1 runs every
carrier analysis once, sequentially, after predictions are frozen in Git).

**VCS rule (jj lane).** LANE is jj-colocated (jj 0.45.1). Git HEAD is detached after a helper commit; the
branch tip is `refs/heads/main`. Lane tools pin revisions as the branch tip, never bare `HEAD`, and never use
`@{u}`, `--abbrev-ref`, `--show-current`, `symbolic-ref`. Read-only git in LANE only (`show`, `ls-tree`,
`cat-file`, `rev-parse`, `log`, `diff`, `merge-base`, `archive` to a temp dir). Never `jj` in LANE; any jj
or git write runs in a throwaway clone under `tempfile.mkdtemp()`.

## C1 — routed R17 defects

### W18/tools/routed-defects.py
`routed-defects.py --root LANE --rev REV [--strict]` reads Git objects at REV only (`git show REV:path`).
Output `{rev, defects: [{id, open, checks: [{name, ok, detail}]}], open_count}`; exit 0 reported (with
`--strict`: 1 if open_count > 0), 2 could-not-evaluate. A defect is closed only if all its checks pass:
- **R17-PINMAP**: (a) `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` has a line containing
  `R17-PINMAP` and `comparator verdict`; (b) `SCORECARD.md` has such a line; (c) `corpus/QUALITY.md` has an
  admission-table data row whose why-cell contains `round-17-verifier-spotcheck.md` and `R17-PINMAP`;
  (d) `.ufo/waves/round-17/tools/carrier-run.py` contains the literal `map_sha256`.
- **R17-VALIDATE16**: `.ufo/waves/round-18/evidence/validate16/summary.json` parses, has `rev` =
  `da64646adcb19c1ede7537b799b8c7d283fe43da` and `receipts` with exactly 8 entries each carrying an int
  `exit`; `SCORECARD.md` and `LOG.md` each have a line containing `R17-VALIDATE16`.
- **R17-PRODUCER-REV**: `SCORECARD.md` and the r17 knowledge entry each have a line containing
  `R17-PRODUCER-REV` and at least two distinct 40-hex hashes.
- **R17-SUMS-RUNLOG**: `.ufo/waves/round-17/predictions/SHA256SUMS` has a line `<sha>  predictions/carriers.tsv`
  whose sha equals sha256 of blob `REV:.ufo/waves/round-17/predictions/carriers.tsv`; `LOG.md` has a line
  containing `R17-SUMS-RUNLOG` and `7/8`.
- **R17-REGISTRY**: in `SKILL.md`, the table rows whose first cell is `go-route-compare`, `receipt-validate`,
  `pins`, `go-buildinfo-probe` each have a 5th cell containing `Write scope:`; the `citation-drift` row's 2nd
  cell starts with `gate`.
- **R17-S032-DIGEST**: `corpus/SOURCES.md` has an 11-column registry row whose teaches cell starts with
  `supersedes S032 —` and whose anchor cell contains `fetch-time`.
Selftest: a fixture repo with one commit where all six are open (open_count 6, strict exit 1) and a second
commit where all six are closed (open_count 0), plus one case per defect where exactly one check is broken.

## C2 — jj-safe revision pins

### W18/tools/revpin.py (module + CLI)
`resolve_source(lane, branch="main", require_pushed=True, require_head=True) -> dict` returns
`{branch, source, head, head_equals_source, remote, pushed}` using `git rev-parse --verify
refs/heads/<branch>^{commit}`, `git rev-parse --verify HEAD^{commit}`, `git rev-parse --verify
refs/remotes/origin/<branch>^{commit}` (absent remote → `remote: null`); raises `RevPinError` with a named
finding (`branch_missing`, `head_not_branch_tip`, `branch_not_pushed`) when a required condition fails.
CLI `revpin.py --root DIR [--branch main] [--no-require-pushed] [--no-require-head]` prints the dict, exit 0
ok, 2 finding. Selftest: fixture repo with a detached off-branch HEAD → `head_not_branch_tip`; tip ahead of
origin → `branch_not_pushed`; clean → 0.

### W18/tools/head-rev-lint.py
`head-rev-lint.py --root LANE --rev REV [--strict]` scans tracked `*.py`/`*.sh` at REV (`git ls-tree`) under
`.ufo/gates/`, `.ufo/rounds/`, `.ufo/waves/round-14/` … `.ufo/waves/round-18/`. Site kinds: `rev-parse-HEAD`
(a git argv with `rev-parse` and literal `HEAD` as a revision), `default-HEAD` (argparse `default="HEAD"` on
a rev-like option), `HEAD-colon` (literal `HEAD:` revision path), `upstream` (`@{u}`, `--abbrev-ref`,
`--show-current`, `symbolic-ref`). Context `fixture` iff the enclosing Python function name contains
`selftest` or `fixture` (AST), else `live`; shell files are always `live`. Output `{rev, files_scanned,
sites: [{path, line, kind, context, code}], live_count, fixture_count}`; exit 0 reported (`--strict`: 1 if
live_count > 0), 2 could-not-evaluate. Selftest: one live site per kind (strict 1), fixture-only (0),
clean (0).

### In-place fixes (exactly one owner each)
- `LANE/.ufo/gates/citation-drift/citation-drift-probe.py`: `--rev` default is no longer `HEAD`; omitted →
  the branch tip (`--branch`, default `main`) via revpin-equivalent logic inlined (no import from W18);
  literal `--rev HEAD` is accepted only when HEAD equals the branch tip, else exit 2 with finding
  `head_not_branch_tip`. Output records `rev_requested`, `rev_resolved`, `branch`. Existing selftest cases
  keep their exits; add the two new cases. Explicit 40-hex `--rev` behaves exactly as before.
- `LANE/.ufo/gates/custody-pair/custody-pair.py`: `capture` gains `--repo DIR` (default: the lane root two
  levels above the script, never `Path.cwd()`); the receipt keeps `# repo-HEAD:` and adds `# repo-root:`,
  `# repo-branch:`, `# repo-branch-tip:`, `# repo-HEAD-is-branch-tip: yes|no`, `# repo-dirty: yes|no`
  (tracked modifications only). `compare` must treat these as metadata exactly as it treats `# repo-HEAD:`.
  Selftest red case: off-branch detached HEAD → `repo-HEAD-is-branch-tip: no`.
- `LANE/.ufo/waves/round-17/verify.py`: `source` = branch tip, and before any command it exits 2 unless
  HEAD equals the branch tip, the tip equals `refs/remotes/origin/main`, and `git status --porcelain
  --untracked-files=no` is empty; record `source_branch`, `head_equals_source`. Inline the logic (stdlib).
  Header comment names the round-18 change and that its d0ab299 run used the pre-change bytes.

### W18/tools/jj-red-before.py
Builds a throwaway clone under mkdtemp: `git clone --no-local LANE sb`, then in `sb` only: `jj git init
--colocate`, identity via `--config`, write a file, `jj commit -m off` without moving `main`, so HEAD is an
off-branch commit. Runs, each with argv/exit/stdout/stderr retained: (1) baseline citation-drift
(`git show B:.ufo/gates/citation-drift/citation-drift-probe.py` to a temp file) with `--root sb` and no
`--rev` → red if it evaluates the off-branch commit; (2) the fixed probe from LANE's working tree with no
`--rev` → green if it resolves `main`; with `--rev HEAD` → green if exit 2 `head_not_branch_tip`; (3) baseline
vs fixed custody-pair `capture` against `sb`; (4) baseline expression `git -C sb rev-parse HEAD` vs
`revpin.resolve_source(sb)` (raises `head_not_branch_tip`). Writes `--out RECEIPT.json`
`{steps, expectations: [{name, expected, observed, held}], all_held}`; exit 0 all held, 1 any not held, 2
setup failure. Removes the sandbox. Never writes LANE.

## C3 — Swiss-map minimal pair

Carriers (built by L1, deterministic, never executed): `/home/vgpnk/.local/share/kaidoku-r18/carriers/` with
`SHA256SUMS`; recipe `W18/carriers/build.sh`, sources `W18/carriers/src/{methods,nomethods}/`. Labels
`s1246-{swiss,noswiss}-{methods,nomethods}`, `s1250-…` (go1.24.6 / go1.25.0 official tarballs in
`~/.local/opt/go-<ver>`, `GOEXPERIMENT=noswissmap` for noswiss). Calibration carriers: `/usr/bin/aether`
(r17 log: `Go analysis failure`, `Unable to read past EOF: 17645861, 111938854`) and
`/home/vgpnk/.local/bin/notesmd-cli` (no failure). Verify their sha256 against W17 receipts first.

### W18/tools/swiss-misread.py
`swiss-misread.py --carrier PATH --golang-root DIR [--go-version X]` emulates, from the binary's bytes and the
installed snapshot JSON selected for its Go version (r16 `selection.py` law), how Ghidra 12.1.4 lays out each
runtime map type descriptor (`runtime.maptype` alias target and its struct size from the JSON) and where it
reads the uncommon/method data (as `GoType`/`GoMapType`/`GoUncommonType`/`GoName` in Base-src.zip do), versus
the binary's true layout (Swiss iff the build setting `GOEXPERIMENT` lacks `noswissmap` and Go ≥ 1.24).
Output `{carrier: {path, sha256}, go_version, snapshot_file, layout: {ghidra_maptype, ghidra_size, true_kind,
true_size}, map_types: n, uncommon_map_types: n, misread_map_types: n, predicted_eof_reads: [[index,
length]], predicted_failure: bool, basis: [Base-src.zip member:line ...], limits: [...]}`; exit 0 emitted, 2
unparseable. `predicted_failure` is true iff the emulated reads raise the same EOF Ghidra's reader would.
Calibration acceptance: aether → `predicted_eof_reads` contains `[17645861, 111938854]`; notesmd-cli →
`predicted_failure: false`. Selftest uses small synthetic byte fixtures.

### In-place additive fixes (exactly one owner each)
- `W17/tools/log-extract.py`: add `eof_reads: [[int, int]]` from every `Unable to read past EOF: A, B` (any
  line, including stack traces) and `symbol_analysis_failures: [msg]` (messages containing `Go analysis
  failure`); existing fields unchanged for all 16 retained r17 logs (prove by re-extraction diff).
- `W17/tools/compare.py`: `extra_expectations` gains `analyzer_errors_empty: bool` and `eof_reads:
  [[a,b]...]` (exact list equality); red selftest cases.
- `W17/tools/carrier-run.py`: each mid-run pin check writes its full map to `DIR/pins/mid-<n>.json` and records
  `map_path`, `map_sha256` in its `pin_checks` entry; `W17/tools/receipt-validate.py` recomputes that digest
  and recompares each mid map with the pre map when present (absent fields keep r17 behaviour); red
  selftest: tampered mid map.

### W18/run-carriers.sh
Adapt `W17/run-carriers.sh`: labels from `W18/predictions/carriers.tsv`, tools from `W17/tools`, output
`${RUNS_DIR:-W18/runs}/<label>`, pins the carrier, its prediction, `W18/tools/swiss-misread.py`, r16
`selection.py` and all Go data files.

## Shared outputs
- `W18/measure.py REV` (Git objects at REV): C1 `open_count` via routed-defects, C2 `live_count` via
  head-rev-lint, C3 count of `W18/runs/*/compare.json` that carry an `extra.eof_reads` or
  `extra.analyzer_errors_empty` field, with `all_match` per label; `--selftest`.
- `W18/controls.py BEFORE AFTER`: no-harm (LOG/SCORECARD old-prefix, prior knowledge/lesson/verifier files
  byte-identical or old-prefix for the one appended r17 knowledge entry, QUALITY rows 1–20 identical, SOURCES
  S001–S032 identical except status/recheck/used-by, W17 predictions identical except the restored
  SHA256SUMS line, SKILL.md deleted lines listed); `--selftest`.
- `W18/verify.py`: the single post-integration pass, source pinned by `revpin.resolve_source`.

## Amendments at wave-1 integration (L1, 2026-10-20 ~12:40 -03:00; reasons in w1 reports)
- C1 (CriticC1, RevBase*): routed-defects.py reports `named_correction` AND `substance` checks per defect; a defect closes only if both hold; the claim counts `open_count` (either failing). Substance definitions were sent to the RoutedDefectsTool seat and are restated in the tool's docstring.
- C2 (CriticC2, ConnSiblingOverlap, ScoutLaneGitSitesNow): lint scope excludes seat dirs `w[0-9]/` (listed under `excluded`), `/fixtures/` paths and same-file fixture-only callees are `fixture`, wrapper calls are detected, and a `head-rev-lint: compare-only` / `red-before` comment marks an `annotated` site (listed, not live). The baseline number is whatever this rule yields; it is not tuned to 3.
- C3 (CriticC3, RevGhidraMapTypeRead, ScoutGhidraGoStructMapping): the methods/nomethods pair is predicted non-diagnostic (every named type carries an uncommon block; Ghidra's +88 read takes SlotSize as pkgPath). Four `nethttp` carriers (http.Header, url.Values, textproto.MIMEHeader: 40-byte slots, as in aether) were added: 12 synthetic + 2 calibration labels. swiss-misread.py predicts per carrier under H1 (OldMapType bound for Swiss) and H0 (true layout); D = carriers where H1 and H0 differ on a logged field. The verdict rule is frozen with the predictions (W18/predictions/decision-rule.json).
- Sandbox (SentinelSandbox): jj-red-before removes the clone's origin remote immediately and isolates HOME/XDG_CONFIG_HOME.
