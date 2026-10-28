# C1PortAudit — R49-C1 port audit (round 49, wave 1, pre-freeze)

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Old: `tools/round-44/*` (lane). New: `.ufo/waves/round-49/draft/tools/round-49/*`. Read-only on the lane; scratch removed; artifacts in `w1/C1PortAudit/artifacts/`.

## Verdict

**The tool port is mechanically sound but the draft is NOT freeze-ready.** The counter and controls drivers pass their own selftests, and the dry-run resolves only round-42 carriers into round-49 evidence paths. Three problems survive the port and must be folded in before the freeze:

1. **The real C1 landing fails the `sourced` binding.** No draft block writes `corpus/SOURCES.md` `used-by`. Only the POS control plants that edit, so POS hides the gap (F1).
2. **The landing text carries round-44 provenance and a pre-written measured result** (F2, F3).
3. **Smaller stale tokens**: a frozen `"round": 44` in `carriers.json`, round-44 fixture search dirs, a mis-attributed seat comment (F4-F6).

Everything else in the delta is a clean round-44 to round-49 token rename, or a deliberate round-44 retention (oracle trees, history, argv records).

## Method and receipts

| step | command (abridged) | exit | evidence |
|---|---|---|---|
| sha pairs | `sha256sum tools/round-44/<f> .ufo/.../draft/tools/round-49/<f>` | 0 | `artifacts/sha256-port-pairs.txt` |
| raw delta | `diff -u tools/round-44/<f> draft/<f>` | 1 (diff differs) | counts below |
| mechanical normalisation | `sed -E 's/([Rr])44/\149/g; s#round-44#round-49#g; s/kaidoku-r44/kaidoku-r49/g'` on round-44 copy, then diff vs draft | 1 (residual hunks) | `artifacts/residual-diffs/*.residual.diff` |
| dev freeze clone | `.ufo/waves/round-49/draft/mkclone.sh <scratch>/dev` | 0 | `DEV_FREEZE=9580c3c9c7298003fd7442e484134da7603f6a79`, toplevel asserted |
| counter selftest | `python3 -I -B tools/round-49/c1-counter.py --selftest --root <dev> --freeze <dev HEAD> --pkg65 <rea 6.5.0> --work <scratch>` | 0 | 47 cases, `failures []`; stdout sha256 `2b2c6dcb21cc0f36b575e940716cbd88af9339a7a7d907c8217310325fcfb4fa` |
| controls selftest | `python3 -I -B tools/round-49/c1-controls.py --selftest --root <dev> --freeze <dev HEAD> …` | 0 | 11/11 passed; stdout sha256 `c5dbab2a6aa8659f2d1159fd514d1cb6e31bc139a82104f0457250cf2cda29e1` |
| harness dry-run, lane | `c1-run.sh --dry-run --lane-root <lane>` (no dev freeze) | 2 | `c1-run: carriers.json not found: …/tools/round-49/carriers.json`, expected before freeze |
| harness dry-run, dev | `c1-run.sh --dry-run --lane-root <dev>` | 0 | `artifacts/dryrun2.out` sha256 `e2b181190998a7ce67622185dcbd4f47929446cc58f1678f686071a1a829a459`; zero `r44` tokens in output |
| POS doc probe | import `c1-controls._doc_landing` and `c1-counter.cells`, replay the counter `sourced` rule on base vs POS-planted SOURCES | 0 | `artifacts/pos_probe.out` sha256 `09832e6f…`; see F1 |
| fixture resolver probe | `c1-run.resolve_fixture` with no `path` field | 0 | `artifacts/fix_probe.out`; see F5 |
| lane git | `git status --porcelain` | 0 | only the pre-existing `?? .ufo/waves/round-49/`; no mutation by this seat |

Not run: the full CTL-C1-0..5/POS controls (real REA runs; the L1 owns them after the freeze); `c1-run.sh --data-run` (forbidden).

Raw delta size: counter 138 changed lines, run.py 62, run.sh 8, controls.py 110, oracle.py 28, carriers.json 6 hunks. After the mechanical normalisation, residue: counter 30, run.py 8, run.sh 2, controls 14, oracle 14, carriers 34.

## Delta classification

**Mechanical (round-44 to round-49 token):** claim `R44-C1`→`R49-C1`; seats `R44C1Counter/Run/Controls/Oracle`→`R49…`; schema ids `kaidoku-r44-*`→`kaidoku-r49-*`; scratch segment `/kaidoku-r44/`→`/kaidoku-r49/` (PROV_SEGMENT, default work dirs, rehost root, selftest roots); `ENTRY`/`STEM`/`CORE_HEADING`/`FRONTIER_MARK`; `CARRIERS`/`DEFAULT_CARRIERS` and `tools/round-44/`→`tools/round-49/` in FROZEN_PATHS, FROZEN_PREFIXES (tools family), REA_PKG/PRIOR_PIN candidates; `corpus/evidence/round-44/c1`→`round-49/c1` (AFTERDIR, EVIDENCE, round_evidence_segment); `GAP_RULE['claim']`; docstring prose; `carriers.json` `claim`, `note`, `schema`; argparse defaults; control doc-dir and fixture root names.

**Non-mechanical (logic):**
- `c1-controls.py` `_doc_landing`: new `corpus/SOURCES.md` rewrite that appends the round-49 entry to the S138/S139 `used-by` cell (new lines ~918-933). The only logic change in the whole port. See F1.
- Everything else in counter, run.py, run.sh, oracle.py is token-only. I checked the residual hunks one by one.

**Deliberate round-44 retentions (correct):**
- `corpus/evidence/round-44/oracle/` in counter `FROZEN_PREFIXES`, oracle `--oracle-root` default and `default_root`, and all `carriers.json` `output_tree`/`extract_root`/`root`/`expected_tree_source` values. These are the committed S138 trees; `corpus/evidence/round-44/oracle/` exists with `squashfs_v1/`, `squashfs_v2/` and `manifest.json`, and the named extract roots exist.
- `carriers.json` oracle `argv` records under `kaidoku-r44/l1-oracle-final` (history of the run that produced the oracle blocks).
- History attributions: `R44RevKill K3` (counter lines 228, 2411), `R44-SCR-TMP` (line 456), `R44SrcOracle` (oracle line 21), `H41/H43/H44/H45` (controls line 40), `.ufo/waves/round-44/…` receipts cited as history in the entry draft (line 101, 248).
- Selftest synthetic paths `corpus/evidence/round-44/carriers/…` and `…/oracle/selftest/…` (counter 2822-3193): sandbox-only.

## Findings

| id | sev | finding | evidence |
|---|---|---|---|
| **F1** | **high** | **The real landing cannot satisfy the `sourced` binding.** The counter requires the S138 and S139 rows of `corpus/SOURCES.md` to be 11-cell rows, with `opened == 2026-10-28` and the entry path in `used-by` (counter ~2180-2185). At base the `used-by` cell holds only `…r44-squashfs-v1v2-core.md`, so `sourced` is `[]`. The four landing blocks (R49C1Doc a/b/c, R49EntryDraft) contain no SOURCES edit. The plan's file list (`draft/plans/round-49-claims.md` ~line 169) says the landing writes `corpus/SOURCES.md`. The only writer is CTL-C1-POS, which plants the edit, so POS goes green while the real landing exits 1 on `sourced`. | `pos_probe.out`: base `sourced = []`; POS-planted `['S138','S139']`; S138 `used-by` base=`…r44…`, planted=`…r44…, …r49…`. **Fix:** add a SOURCES.md used-by block to the landing, and make POS plant that same block rather than a self-generated rewrite. |
| **F2** | **high** | **Entry draft pre-writes a measured result and round-44 provenance.** The status line (`R49EntryDraft/…core.md` line 5) states `carriers_matched 4/4, met_target true, exit 0, every boolean binding true, failing [], frozen_path_changed []` against freeze `c48f8a4b…`, before any data run. Its counter sha `9f2cc140e1fa7875…` is the **round-44** `c1-counter.py` (the round-49 draft is `d6d70cb7…`). Lines 7 and 9 cite `.ufo/waves/round-44/controls/pos/counter.json` and `…/summary.json` as the round-49 scored receipt. The counter does not read the status text, so POS accepts it. | sha table; `grep -n 44` on `R49EntryDraft` lines 5, 7, 9. **Fix:** strip all measured headlines and round-44 receipt pointers from the draft; fill them only from the L1's measured run. |
| **F3** | med | Round-44 text in landing blocks. Entry title `(round 44, Core)`; body line 21 `Round 44 adds the ## Round-49 additions to Core row`; README row block-c `SquashFS v1/v2 through REA (round 44)`. The counter's coverage-map check only tests `STEM in row`, so this passes. | `grep -n 44` on `R49C1Doc/*` and `R49EntryDraft/*`. |
| **F4** | med-low | `carriers.json:1055` `"round": 44` in the frozen blob (every other round field says 49). No tool reads it (`grep` finds no `'round'`/`"round"` reader in the five tools), so it is inert, but it is a frozen-bytes round-44 token. Fix before freeze. | `grep -n '"round"'` on draft carriers. |
| **F5** | low (latent) | `c1-run.py` `FIXTURE_DIRS` still lists `corpus/evidence/round-44/carriers` (live directory holding exploratory `squashfs_v2.1_{le,be}.bin`) and `corpus/evidence/round-44/fixtures` (absent). Probe: no-`path` entries `v1le/v1be/v2le/V2LE` resolve to round-42 fixtures; `v21le/v21be/v2.1le` raise `Unevaluable`. All four scored carriers carry an explicit `path`, so the listing is never reached today. Recommend dropping round-44 entries from `FIXTURE_DIRS`. | `fix_probe.out`; `c1-run.py:116-120`. |
| F6 | low | Counter comment line 57: `(R49C1Oracle / R44ConnRouted measured it` relabels the round-44 measurement's oracle seat as `R49C1Oracle`. The original was `R44C1Oracle`. Comment only; correct the attribution. | diff line `-…R44C1Oracle` / `+…R49C1Oracle`. |
| F7 | low | Counter comment line 88: `…does not exist in round 44 and is dropped with it` is a round-44 history sentence sitting in a round-49 predicate doc. Ambiguous; reword as history. | `sed -n 80,95p`. |
| F8 | low | Controls `--doc-dir` default `.ufo/waves/round-49/w1/artifacts` is relative to cwd, so CTL-C1-POS must run from the lane root. The POS bytes come from an uncommitted `.ufo/**` directory; they are only frozen if `control_pos` writes them into `control-fixtures` via `write_fixtures` (line ~1419). The L1 should confirm the fixture copy exists before trusting POS. | `c1-controls.py:1264-1266`; `write_fixtures` call at 1419. |
| F9 | med (calibration) | `opened` vacuity. The counter checks `c[8] == 2026-10-28`. S138/S139 were opened by round 44 on the same calendar date, so the check passes without any round-49 re-open. The plan says "re-opened this round (access date in `corpus/lessons/round-49.md` `## Gate`)", but the counter never reads the lesson. A stale row passes the binding. Either bind the re-open receipt or stop claiming it. | `pos_probe.out` base `opened='2026-10-28'`; plan line ~154. |

## Residual verification gaps

- The full controls run (CTL-C1-0..5, POS real REA) was not run. F1 means CTL-C1-POS will pass even though the real landing would fail, so POS cannot clear F1.
- No dry-run against the frozen tree (the freeze does not exist yet).
- Tool installs: none. No channel was used, no host service touched, pacman not touched.

## Artifacts

`.ufo/waves/round-49/w1/C1PortAudit/artifacts/`: `sha256-port-pairs.txt`, `residual-diffs/*.residual.diff`, `dryrun2.out/.err/.rc`, `counter-selftest.out/.err/.rc`, `controls-selftest.out/.err/.rc`, `pos_probe.py/.out`, `fix_probe.py/fix_probe.out`, `mkclone.out`, `SHA256SUMS.txt`.
