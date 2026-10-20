# Round 19 scorecard claims review

**Axes:** calibration, freshness, depth. **Observed `refs/heads/main`:** `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. The SCORECARD diff from B appends the round-19 block at `SCORECARD.md:2473-2503`; it has no final-measurement block after its `:2479` promise. No production files were changed by this review.

## Findings (by severity)

### High — C3 count command conflates runs, while the committed scorecard lacks the amended final pass

**Observation.** The latest committed amendment (`.ufo/waves/round-19/claims.json:43-47`) says the round-19 predictions/rule stay frozen, a second pass uses final validator bytes at `279e8b1`, and final counts must use live receipt validation rather than treating first-pass exit-0 records as current. The frozen rule requires `receipt-validate.py --require-mid-maps` to exit 0 and counts labels with a bound log plus `compare.json` (`predictions/decision-rule.json:3-6`).

All eight first-pass receipts under `runs/t1250-*/receipt.json` now fail the live validator: each has only the validator `sha256_mismatch` and `size_mismatch` (receipt pin `70672eb3…`, 46,047 bytes; delivered validator `6afb7ef6…`, 52,682 bytes). The eight second-pass receipts in the current worktree validate exit 0 against the delivered validator; their eight compare files are complete. The second-pass run log records seven compare exits 0 and vet exit 1 (`runs/pass2/run-log.txt:2-18`). Vet's second-pass raw log reports `Go analysis failure` at `:186` and `Invalid index: 13902080` at `:229`; the latter is in the frozen H1-only set (`decision-rule.json:21-25`). The literal `Go analysis failure|Invalid index` search over pass-two artifacts found only the vet label. Thus, **in the current worktree**, the distinct conclusions remain: the full-list compare is 7/8, while the separate mechanism rule is confirmed. The 7/8 mismatch is not itself a mechanism refutation.

But pass two is not present in the observed main commit: `git ls-tree -r --name-only refs/heads/main -- .ufo/waves/round-19/runs/pass2` counts zero paths. `SCORECARD.md:2495` remains unchanged, its `find ... -name compare.json | wc -l` counts files rather than uniquely bound labels, and it does not identify pass two. With both passes in the live worktree that exact command returns **16**, not 8. `measure.py` at the committed tip reports the eight root-level first-pass compares and seven matches, but its selector is only `runs/<label>/compare.json` (`measure.py:73-76,579-657`), so it omits nested `runs/pass2/<label>` and does not perform receipt validation. The scorecard still says final records will be appended after integration (`SCORECARD.md:2479`), although its C3 row already presents a confirmed mechanism and `0→8` count.

**Inference / required correction:** the second pass now supports the frozen mechanism conclusion and the same 7/8 full-compare result, but the scorecard's committed evidence and counting command do not establish the amended, live-validated 0→8 label count. Integrate the eight pass-two records and final measured revision, then count distinct labels that pass both the current receipt gate and compare-file requirement; do not count both attempts as 16 observations or present the invalid first pass as the final cohort.

### Low — “silent” is broader than the rule's actual diagnostic predicate

`SCORECARD.md:2495` calls the seven non-D controls “silent.” The rule is narrower: `decision-rule.json:5` requires no **Go analysis failure**, not absence of all Go-related diagnostics. For example, the non-D `t1250-compile` second-pass log has `ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred)` at `runs/pass2/t1250-compile/logs/rea-ghidra-07WMDZ/ghidra.log:347`. That does not meet the rule's named failure predicate, so it does not refute the mechanism result; it does make unqualified “silent” misleading. Prefer the exact rule wording (“no predicate-defined Go analysis failure”) and retain the diagnostic scope.

### Low — the scorecard's source shorthand drops the identity/mechanism split

`SCORECARD.md:2494-2495` labels C2 “sourced S037” and C3 “sourced S038/S035/S023/S003” without assigning which evidence supports which subclaim. The source rows and amendment are narrower: S037 is npm publish identity/integrity only (`corpus/SOURCES.md:43`, `claims.json:41`); S038 establishes archive/carrier provenance, not analyzer behavior (`corpus/SOURCES.md:44`, the r19 knowledge entry `:1`); S035/S023/S003 and the bound Ghidra logs support the mechanism/outcome. The detailed claim amendment and knowledge header preserve that distinction, but the scorecard shorthand can read as if the registry/release metadata establishes live pin equality or the Swiss-map result. Keep the scorecard attribution split by subclaim.

## Reconciled claims and residual risk

- **C1 calibration** (`SCORECARD.md:2493`, `claims.json:12-13`): reproduced `routed-r18.py` baseline open 7/named 7/substance 7, exit 1; at `279e8b1`, open 0/named 0/substance 0, exit 0. The 10.0→10.0 axis proxy is explicitly unchanged; the defect count is a separate measure, not a claimed score increase.
- **C2 freshness** (`SCORECARD.md:2494`, `claims.json:39`): the pin probe reports 2 mismatched clients (Devin, OMP) at B, exit 1, and 0 at `279e8b1`, exit 0. The retained baseline census output at `.ufo/waves/round-19/evidence/c1-census-v10-before.txt:6-43,112-113` has stale=4/undeclared=2, exit 1; the current census has stale=0, undeclared=2, no G11 finding, and remains FAIL, exit 1. This matches the amendment's no-PASS claim. `PROVINCE.md:44` expressly says a live attached-client `binary_session` was not exercised; the result is configured-pin freshness, not proof of a running REA 6.7.0 session.
- **Numeric proxies / coverage:** C2 correctly has no owned score proxy. The inherited depth proxy is citation resolution (SCORECARD `:24`), not the C3 full-compare fraction; 10.0→10.0 must not be read as 8/8 C3 prediction accuracy. The source-derived coverage score is 96/96→97/97 = 10.00→10.00: the r19 Go entry is now present in the existing README Go-chain row (`corpus/README.md:35`). Thus “coverage unchanged” is true for the score/domain ground, not a claim that the raw numerator and denominator are unchanged.
- **Saturation / runtime:** the 10.0/window-10 line is honestly bounded: no capability row enters, the last capability entry remains round 17, and SCORECARD `:31` says a perfect finite proxy does not retire a domain axis. SHONEN marks remain `[~]`. C3 records eight sequential sessions with the same REA 6.5.0/Ghidra 12.1.4 pair (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:2`); C2's 6.7.0 config pins are a distinct fact. No same-identity rerouting claim or changed routing path is asserted in the SCORECARD diff.

## Commands and observed exits

Commands below were read-only. `B` is the full baseline hash above.

```text
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# open=7 named=7 substance=7; exit 1
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# open=0 named=0 substance=0; exit 0

python3 -I -B .ufo/waves/round-19/tools/province-pins.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# mismatches=2 (Devin, OMP); exit 1
python3 -I -B .ufo/waves/round-19/tools/province-pins.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# mismatches=0; exit 0

python3 -I -B .ufo/gates/c1-census-v10.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --json
# stale=0, ambiguous=0, undeclared=2, unresolved=0, g11=[]; VERDICT FAIL; exit 1
python3 -I -B .ufo/waves/round-19/measure.py 279e8b19c51658bfd05b9e31a1c0894ab2e70537
# exit 0; tool output: C1 open=0, C2 pin mismatches=0, census FAIL stale=0/undeclared=2,
# C3 root-level compare_jsons=8, matched=7. This is not a receipt-binding check.

find .ufo/waves/round-19/runs -name compare.json | wc -l
# 16 in the live worktree (8 first pass + 8 second pass); exit 0

git ls-tree -r --name-only refs/heads/main -- .ufo/waves/round-19/runs/pass2 | wc -l
# 0 committed pass-two paths at observed main; exit 0
```

Receipt validations, using the delivered `receipt-validate.py --require-mid-maps`:

```text
for f in .ufo/waves/round-19/runs/t1250-*/receipt.json; do
  python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py "$f" --require-mid-maps
 done
# first pass: exit 1 for each of 8 (validator SHA-256 and size mismatch)

for f in .ufo/waves/round-19/runs/pass2/t1250-*/receipt.json; do
  [ -f "$f" ] || continue
  python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py "$f" --require-mid-maps
 done
# second pass: exit 0 for each of 8; valid=8, invalid=0, unreadable=0
```

Coverage-map count (Git objects only; exit 0):

```text
python3 -I -B - <<'PY'
import pathlib, re, subprocess
revs = ['8a8da7e19375aadc66c6bcbff0bbcbb596048fb0',
        '279e8b19c51658bfd05b9e31a1c0894ab2e70537']
def get(rev, path):
    return subprocess.check_output(['git', '--no-optional-locks', 'show', f'{rev}:{path}'], text=True)
for rev in revs:
    paths = subprocess.check_output(['git','--no-optional-locks','ls-tree','-r','--name-only',rev,'--','corpus/knowledge'], text=True).splitlines()
    files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
    section = get(rev, 'corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    print(rev[:7], len(files & mapped), len(files), sorted(files-mapped), sorted(mapped-files), round(10*len(files & mapped)/len(files),2))
PY
# B: 96/96, missing/dangling []; 279e8b1: 97/97, missing/dangling []; exit 0
```

## Verification gaps

- The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”); no LSP status/references/definition/diagnostics were available. I made no semantic claim from grep output; source and log statements above are literal artifacts.
- No builds, tests, mutation tests, installs, REA/MCP/Ghidra actions, or carrier executions were performed. Receipt validation and Git-object counting only.
- Pass two is observed in the live worktree, not in `refs/heads/main` at `279e8b1`; conclusions about the committed deliverable are bounded to that tip.