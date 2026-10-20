PARTIAL — all three before→after numbers reproduce exactly at b2aad08, but there are three problems. (1) The C1 counting tool was amended after the freeze, and its selftest fails at REV. (2) C2's zero depends on the lint missing `round-17/verify.py:82`. (3) The C2 jj receipt is not bound to REV's bytes. The draft rows below include all three as limits.

# ScorecardMeasuredDraft — round-18 w2 (author-side advisory scribe)

- **Revisions.** Measured `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (REV), baseline `9011581d84527ba34c675f9cf912e54d2e72d470`, freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
- **Lane state [OBS].** Lane HEAD = REV. At the start of this seat, the only untracked entries were 9 round-18 paths: `carriers/bin/`, `w2/`, `gen-wave2.py` and six `wave2-*` dispatch files (`git status --porcelain`). By the end `carriers/bin/` was gone; this seat did not remove it. The tools ran from a worktree that is byte-identical to REV (`git diff --quiet b2aad08 -- .ufo/waves/round-18/tools .ufo/waves/round-18/measure.py .ufo/waves/round-18/controls.py` exit 0).
- **Environment.** Python 3.14.8, git 2.56.0. `jq` resolves to jaq 3.1.1. No tools were installed or updated.
- **Insertion point.** `SCORECARD.md:2428-2440` at REV holds the round-18 header and corrections but no claim table yet. The file ends at :2440. The row format follows `SCORECARD.md:2361-2362`.

## Draft

Measured revision `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Baseline `9011581d84527ba34c675f9cf912e54d2e72d470`. C3 predictions were frozen at `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. That commit was pushed at 13:23:57-03:00 (origin/main reflog), before the first carrier run at 13:24:07-03:00 (`runs/run-log.txt:2`).

| Claim / axis | Existing numeric proxy | Falsifiable before→after, command and measured revision | Author-side verdict / limits |
|---|---|---|---|
| C1 calibration | 10.0→10.0, delta 0 (carried from round-17 section, not re-measured) | Routed r17 defects open 6→0. Command: `routed-defects.py --root <LANE> --rev <REV>`, using the REV tool for both revisions (the tool is absent at `9011581`). At `9011581`: `open_count` 6 (named 6, substance 6; 38/40 checks red; `--strict` exit 1). At `b2aad08`: 0 (40/40 green; `--strict` exit 0). `measure.py <REV>` copies `c1_open_count` 0. QUALITY admission rows 20→21, rows 1–20 byte-identical (`corpus/QUALITY.md:11-31`) | **Improved** on the count: six routed defects closed, each with named and substance checks. Limits: (1) The tool was amended after the freeze, in `b2aad08` (`routed-defects.py:278-282`): the `mid_map_mismatch` placeholder became the two as-built ids. The `eb6c266` tool still reports 1 open at `b2aad08`. (2) At REV, `--selftest` exits 1 with 7 failing cases, because the fixtures at `:914` and `:1145` keep the placeholder. (3) `r18-receipt-pinmaps` passes on a single receipt (`:365-366`). The universal claim in `SCORECARD.md:2438` was checked separately: 22/22 mid maps match from Git objects |
| C2 operability | no owned numeric proxy | Live HEAD-as-revision sites 3→0. Command: `head-rev-lint.py --root <LANE> --rev <REV>` (REV tool). At `9011581`: live 3 (`citation-drift-probe.py:477`, `custody-pair.py:327`, `round-17/verify.py:59`; `--strict` exit 1). At `b2aad08`: 0 (`--strict` exit 0). Fixture 8→15; all 7 new sites are round-18 selftest/fixture code. Annotated 0→6. Seat-dir exclusions are 10 files / 4 sites at both revisions. The zero was already reached at `eb6c266`, and the C2 sources are unchanged from there to REV. `jj-red-before` receipt: 14/14 held (`evidence/jj-red-before.json:2`) | **Improved** under the as-built rule. Limits: (1) Annotations are trusted comments (`head-rev-lint.py:142-143`). Without its comment, 4 of the 6 annotated sites would count live. (2) The lint misses `round-17/verify.py:82` (`HEAD^{commit}` called through `_git_or_none`→`git`). Its compare-only comment sits on `:81`, not on the site line. Under a transitive-wrapper rule REV counts live 1; the baseline stays 3. By reading, the site is compare-only (`:92-93`). (3) The jj receipt ran worktree bytes while the lane tip was `9011581` (`:176-179`). It records no digest of those sources, so it is not bound to REV's bytes |
| C3 depth | 10.0→10.0, delta 0 (carried, not re-measured) | Labels with a bound retained log and a `compare.json` carrying `extra.eof_reads`: 0→15. Command: `measure.py --root <LANE> <REV>`, field `c3_compare_jsons_with_extra`. It reads 0 at `9011581` and at the freeze `eb6c266`, and 15 at `b2aad08` (`extra.eof_reads` 15, `extra.analyzer_errors_empty` 12; `all_match` true ×15, copied from the artifacts). The frozen binding gate (`predictions/decision-rule.json:2`) was re-checked at REV: `receipt-validate.py --require-mid-maps` reports 15/15 valid (exit 0); carrier sha256 in receipt = prediction for 15/15; predictions are unchanged from `eb6c266` to REV. Mechanism status: unreplayed INFERENCE → **confirmed** under the frozen rule (`:7`) | **Improved**. Both held-out D carriers failed exactly as frozen: s1246-swiss-nethttp `Invalid index: 22386945` (`ghidra.log:451`) and real go1.24.13 kimi-webbridge `Invalid index: 15606016` (`:206`). The noswiss sibling and the 11 non-D synthetic labels show 0 `Go analysis failure` lines, and all 15 logs reach `REPORT: Analysis succeeded`. Limits: (1) `measure.py` counts field names only (`measure.py:66-68`). (2) The receipt leg reads host carrier paths outside Git. (3) Coverage is one Ghidra release, x86-64 ELF, 3 failing carriers. (4) The silent-misread case is still INFERENCE |

## Commands and exit codes (all observed; `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, run in `$LANE`)

| # | Command | Exit | Key output |
|---|---|---|---|
| 1 | `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root $LANE --rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0 | open 6, named 6, substance 6; failing checks 38/40 |
| 2 | same, `--strict` | 1 | — |
| 3 | same, `--rev eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` | 0 | open 6; failing 31/40 |
| 4 | same, `--rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (plain and `--strict`) | 0 / 0 | open 0, named 0, substance 0; failing 0/40 |
| 5 | `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root $LANE --rev 9011581…` | 0 | files 27, live 3, fixture 8, annotated 0, excluded 10/4 |
| 6 | same, `--strict` | 1 | — |
| 7 | same, `--rev eb6c266…` / `--rev b2aad08…` (`--strict` at REV) | 0 / 0 (0) | files 39, live 0, fixture 15, annotated 6, excluded 10/4 |
| 8 | `python3 -I -B .ufo/waves/round-18/measure.py --root $LANE b2aad08…` (also without `--root`) | 0 / 0 | c1 0, c2 0, c3 15/15, eof_reads 15, analyzer_errors_empty 12, `could_not_evaluate` false |
| 9 | `python3 -I -B .ufo/waves/round-18/measure.py --root $LANE 9011581…` | 0 | c1/c2 `could-not-evaluate` `tool_absent_at_rev`; c3 0/0 |
| 10 | `python3 -I -B .ufo/waves/round-18/measure.py --root $LANE eb6c266…` | 0 | c1 6, c2 0, c3 0/0 |
| 11 | `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest` | **1** | `SELFTEST: FAILED closed-fixture-cli … closed-fixture-inprocess: open_count=1 broken=['receipt-validate-mid-finding']; token-only-R17-{VALIDATE16,PRODUCER-REV,SUMS-RUNLOG,REGISTRY,S032-DIGEST}: … extra_open=['R17-PINMAP']` |
| 12 | `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --selftest` | 0 | `SELFTEST: CLEAN cases=3` |
| 13 | `python3 -I -B .ufo/waves/round-18/measure.py --selftest` | 0 | `SELFTEST: CLEAN cases=68` |
| 14 | `git show eb6c266…:.ufo/waves/round-18/tools/routed-defects.py > $T/routed-defects.py && python3 -I -B $T/routed-defects.py --selftest` | 0 | `SELFTEST: CLEAN cases=17` |
| 15 | `python3 -I -B $T/routed-defects.py --root $LANE --rev b2aad08…` (eb6c266 tool) | 0 | open 1: `R17-PINMAP substance receipt-validate-mid-finding: 'mid_map_mismatch' only in comments/docstrings or absent` |
| 16 | `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $(git ls-tree -r --name-only b2aad08 .ufo/waves/round-18/runs/ \| grep '/receipt.json$')` | 0 | counts `{receipts 15, valid 15, invalid 0, unreadable 0}` |
| 17 | `git diff --quiet eb6c266… b2aad08… -- .ufo/waves/round-18/predictions` | 0 | predictions unchanged since freeze |
| 18 | `git diff --stat eb6c266… b2aad08… -- .ufo/gates/citation-drift .ufo/gates/custody-pair .ufo/waves/round-17/verify.py .ufo/waves/round-18/tools/revpin.py .ufo/waves/round-18/tools/jj-red-before.py` | 0 | empty (C2 sources unchanged after eb6c266) |
| 19 | `git diff --stat eb6c266… b2aad08… -- .ufo/waves/round-18/tools/ .ufo/waves/round-18/measure.py` | 0 | `routed-defects.py \| 13 +++++++++----` only |
| 20 | Per-receipt loop: `git show b2aad08:<map_path rel> \| sha256sum` vs `map_sha256` for every `steps.*.pin_checks[]` | 0 | `22/22` verified; every receipt has `with_map == pin_checks` |
| 21 | Per-label loop: `receipt.carrier.sha256_pre` vs `<label>.prediction.json .carrier.sha256`; `retained_logs[].binding` all true | 0 | 15/15 equal; 15/15 bindings true |
| 22 | QUALITY: `git show <rev>:corpus/QUALITY.md \| awk '/^## Admission criteria/{f=1;next} /^## /{f=0} f && /^\| *[0-9]+ *\|/'`, then `head -20 <REV rows> \| cmp - <base rows>` | 0 | 20 rows at base, 21 at REV; cmp exit 0 |
| 23 | `git log -3 --format='%h ad=%ad cd=%cd' --date=iso-strict`; `git reflog show --date=iso-strict refs/remotes/origin/main` | 0 | eb6c266 committed 13:23:55, pushed 13:23:57; b2aad08 committed 13:38:07, pushed 13:38:11 (-03:00) |
| 24 | Logs: `git show b2aad08:<ghidra.log> \| grep -c 'Go analysis failure'` / `'REPORT: Analysis succeeded'` for all 15 | 0 | failure lines only in calib-aether, s1246-swiss-nethttp, real-kimi-webbridge; `Analysis succeeded` 1 in each of 15 |
| 25 | Annotation-stripped context and transitive-wrapper counterfactuals (scripts below) | 0 / 0 | see F5, F6 |

## Findings

**F1 — C1 tool selftest fails at REV (calibration/operability) [OBS].**
- Reproduce with command 11 (exit 1).
- `routed-defects.py:282` now requires `("mid_map_sha256_mismatch", "mid_map_compare_mismatch")`. The closed fixture at `:914` (`FINDING = "mid_map_mismatch"`) and the token-only fixture at `:1145` still carry the placeholder.
- As a result, the closed fixture never closes R17-PINMAP, and all five token-only cases report R17-PINMAP as an extra open defect.
- The target-defect behavior in those cases is still correct: `target=(True, False, True)`.
- Consequence: at REV the tool shows it can stay red, but not that a fixture can reach 0.

**F2 — The C1 count definition changed after the freeze (calibration) [OBS].**
- Command 19 shows `routed-defects.py` is the only round-18 tool whose bytes changed from `eb6c266` to `b2aad08`.
- Command 15 shows the frozen `eb6c266` tool reports `open_count` 1 at REV.
- The change is grounded. The real validator ids exist at `.ufo/waves/round-17/tools/receipt-validate.py:514,566`. `mid_map_mismatch` occurs 0 times in that file (`git show b2aad08:.ufo/waves/round-17/tools/receipt-validate.py | grep -c mid_map_mismatch` → 0, exit 1).
- The row must disclose the change rather than present 0 as the frozen tool's output.

**F3 — 2/40 checks are already green at baseline (calibration, minor) [OBS].**
- In command 1's JSON, `producer-revs-are-ancestors` and `carriers-tsv-identical` pass at `9011581`.
- This contradicts the wording of `claims.json:13`: "each check is a revision-scoped Git-object test whose red state is the baseline".
- Every defect is still open at baseline, so the 6→0 count is unaffected.

**F4 — The pin-map check is existential, the correction is universal (calibration) [OBS].**
- `_pinmaps_retained_check` returns on the first qualifying receipt (`routed-defects.py:365-366`). At REV that is calib-aether, with 3 pin_checks.
- `SCORECARD.md:2438` asserts "round-18 receipts retain each mid map".
- Command 20 confirms the universal claim: 22/22 digests match across 15 receipts. The claim holds; the tool's check is the weaker part.

**F5 — An unseen live-form site at REV (C2 calibration) [OBS].**
- `round-17/verify.py:82`, `head = _git_or_none("rev-parse", "--verify", "HEAD^{commit}")`, is invisible to the lint. Wrapper detection (`head-rev-lint.py:452-467`) marks only `git`, which builds the literal argv. `_git_or_none` (`:63-67`) forwards `*args` to `git`, so it is never marked.
- The author's `# head-rev-lint: compare-only` sits on `:81`, but `python_context` reads only the site line (`:524-525`).
- A transitive (`*args`-forwarding) wrapper counterfactual gives live 3 at `9011581` (unchanged) and live 1 at REV (`verify.py:82`).
- [INFERENCE from reading `verify.py:92-93`] HEAD here only feeds the `head_not_branch_tip` refusal. It is compare-only, so the claim's substance holds, but the zero depends on the blind spot.
- The lint's limits do not name this two-level wrapper case. `:130-133` covers argvs built outside a literal list or wrapper-call site only in generic terms, and `:134` names cross-module helpers.

```
python3 -I -B -c '
import ast, importlib.util, sys
L = sys.argv[1]
spec = importlib.util.spec_from_file_location("hrl", L + "/.ufo/waves/round-18/tools/head-rev-lint.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
orig = m.SiteScanner.visit
def visit(self, node):
    if isinstance(node, ast.Module):
        changed = True
        while changed:
            changed = False
            for fn in ast.walk(node):
                if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and fn.name not in self.wrappers:
                    for sub in ast.walk(fn):
                        if isinstance(sub, ast.Call):
                            nm = sub.func.id if isinstance(sub.func, ast.Name) else (sub.func.attr if isinstance(sub.func, ast.Attribute) else None)
                            if nm in self.wrappers and any(isinstance(a, ast.Starred) for a in sub.args):
                                self.wrappers.add(fn.name); changed = True; break
    return orig(self, node)
m.SiteScanner.visit = visit
for rev in ("9011581d84527ba34c675f9cf912e54d2e72d470", "b2aad08ceeee8dd125ce0d316056d8bd766c7f94"):
    r = m.lint(L, rev)
    print(rev[:7], "live", r["live_count"], "fixture", r["fixture_count"], "annotated", r["annotated_count"])
    for s in r["sites"]:
        if s["context"] == "live": print("   LIVE", s["path"] + ":" + str(s["line"]), s["kind"])
' "$LANE"
# exit 0 → 9011581 live 3 fixture 8 annotated 0; b2aad08 live 1 fixture 15 annotated 6; LIVE .ufo/waves/round-17/verify.py:82 rev-parse-HEAD
```

**F6 — Four of the six annotated sites would be live (C2 calibration) [OBS].**
- Stripping `head-rev-lint: (compare-only|red-before)` from the three files and re-running the lint's own `scan_python`/`python_context` gives:
  - **Would be live:** `citation-drift-probe.py:304` (`head_commit`), `custody-pair.py:381` (`repo_context`), `jj-red-before.py:377` and `:659` (`evaluate`).
  - **Would be fixture:** `custody-pair.py:1350` and `:1353` (`cmd_selftest`).
- [INFERENCE from reading] `citation-drift-probe.py:299-308` and `custody-pair.py:381-382` read HEAD only to compare it with `refs/heads/<branch>`. The two `jj-red-before.py` sites deliberately reproduce the baseline.
- The lint cannot verify these comments (`:142-143`), so the row must carry this limit.

**F7 — The jj receipt is not bound to REV (C2 provenance) [OBS].**
- `evidence/jj-red-before.json:176-179` records `lane_tip` before and after as `9011581`.
- Its steps run `$LANE/.ufo/gates/citation-drift/citation-drift-probe.py` and `.../custody-pair.py` from the worktree.
- Its only 64-hex values (`:364`, `:552`, `:582`) are digests of `/tmp` custody receipts, not of tool sources. The REV source digests, `d3e24de4…` (citation-drift-probe.py) and `171d9089…` (custody-pair.py), do not appear.
- [INFERENCE] The fixed forms probably equal the bytes committed at `eb6c266`; command 18 shows no change from there to REV. The receipt itself does not prove it.
- I did not re-run `jj-red-before.py`.

**F8 — The C3 counter is weaker than the frozen count rule, but the rule holds at REV (C3 calibration) [OBS].**
- `measure.py:60-61,66-68` counts `compare.json` files carrying either extra field. It neither checks binding nor re-derives `all_match`.
- The frozen `count_rule`/`binding_gate` (`predictions/decision-rule.json:2,8`) requires: `receipt-validate --require-mid-maps` exit 0, carrier sha256 = prediction, and an unchanged prediction blob.
- Commands 16, 17 and 21 show all three legs hold for 15/15, and `extra.eof_reads` alone is 15. The 0→15 count therefore stands under the frozen rule.
- Leg 1 hashes host paths outside Git (`/usr/bin/aether`, `~/.local/bin/notesmd-cli`, `~/.kimi-webbridge/bin/kimi-webbridge`, `~/.local/share/kaidoku-r18/carriers/*`). It is a host-state check, not a REV-only check.

**F9 — The amendment timestamp postdates its own commit (calibration, minor) [OBS].**
- `claims.json:35` says `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)"`.
- The amendments block is already present at `eb6c266` (`git show eb6c266…:.ufo/waves/round-18/claims.json | jq -r '.amendments[0].at'` prints the 13:25:00 value; pipe exits 0 0). That commit was made at 13:23:55 and pushed at 13:23:57 (command 23), and the first run started at 13:24:07 (`runs/run-log.txt:2`).
- The content was frozen before the runs; only the written time is wrong.

## Out of scope / not done

- I did not re-measure the owned 10.0 proxies (commands A/B); the column is labelled "carried".
- I did not re-run `jj-red-before.py`.
- No REA or Ghidra run, no carrier execution: carriers were only hashed, via receipt-validate.
- No lane edits, no jj, no git writes.
- I did not adjudicate the C3 mechanism beyond the frozen rule's observable legs.

## Touched surfaces

- **Written:** this report only.
- **Scratch:** `/tmp/r18-scd-WLi5Oj` held tool stdout and the `eb6c266` tool copy; it was removed after writing.
- **Selftest temp dirs:** created by the tools under `tempfile.mkdtemp`; each tool removes its own.
