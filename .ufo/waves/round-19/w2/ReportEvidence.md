# Round 19 — wave 2 `ReportEvidence`: draft evidence table

Seat: `KaidokuR19.ReportEvidence-3` (leaf; author-side, not an outside verifier). Scope: claims, count commands, verdicts, limits. Only this file was written. No production edits, no REA/Ghidra, no carrier execution, no installs, no delegation, no builds, no broad suite. Mutation tests ran only in my own `mkdtemp` clones.

Labels: **OBS** = observed in a command below (exit code given). **INF** = inference from observed text. Anchors are `path:line` in the lane unless noted.

## 0. Observed state

- Baseline `B` = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. Observed `refs/heads/main` = `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (OBS, exit 0). Commits `B..main` = 5 (`85589ac`, `a1140e7`, `4f6c73f`, `5e364bd`, `d0690fd`; OBS, exit 0).
- **Live drift during this seat:** my first read showed lane `HEAD` detached at `5e364bd`; a later read showed `HEAD` = `d0690fd`. The lane is being edited by L1. Uncommitted at last check (OBS, `git status --short`, exit 0): ` M` `.ufo/waves/round-19/wave2-registration.json`, ` M` `…/wave2-registry.json`, ` M` `SKILL.md`, ` M` `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`, ` M` `corpus/lessons/round-19.md`, `??` `.ufo/waves/round-19/evidence/wave-outcomes/w1-terminal.json`, `??` `.ufo/waves/round-19/w2/`. None of these are mine. Every result below is on **committed `d0690fd`** via a clean clone unless marked *live*.
- Clones (disposable, mine): `/tmp/kr19-w2-clean-pBrx0X/main` (clean at `d0690fd`), `/tmp/kr19-w2-JgyKLh/base` (clean at `8a8da7e`), `/tmp/kr19-w2-JgyKLh/main` (`d0690fd` plus one local mutant commit `24a6cac3d913ebe426bc436a7d16249fec75212a`, used only in §4).
- Installs/updates by this seat: **none**. The only git writes were local commits inside `/tmp/kr19-w2-JgyKLh/main`.

## 1. Draft evidence table

| Claim (`claims.json`) | Count command | Before → after (committed) | Verdict | Principal limit |
|---|---|---|---|---|
| **C1 calibration** (`:10-15`) routed R18 defects | `routed-r18.py --root <abs> --rev <REV> --strict` | open **7** (named 7, subst 7) at `B` → open **0** at `d0690fd` | **MET as stated**, with absolute `--root`. | Tool verdict depends on how `--root` is spelled (§2, L1). Not a claim failure. |
| **C2 freshness** (`:18-22`) stated-vs-live pins | `province-pins.py --root <abs> --rev <REV> --strict` | mismatches **2** (Devin, OMP) at `B` → **0** at `d0690fd` | **MET** | Covers pins only; "doctor alignment, Ghidra/JDK" (`claims.json:19`) has no probe here. |
| **C2** c1-census stale loci | `c1-census-v10.py --root <clone@REV>` | stale **4** (undeclared 2) at `B` → stale **0** (undeclared 2) at `d0690fd`; VERDICT **FAIL** exit 1 | **MET as amended** (`claims.json:39`): PASS is *not* reached. | The tool has no `--rev`; the claim's `--root LANE --rev REV` (`:20`) is not a valid invocation (exit 2). |
| **C3 depth** (`:24-29`) go1.25.0 held-out | count = labels with bound retained log + `compare.json` (`decision-rule.json:6`) | **0 → 8** (OBS) | **Count MET**. Mechanism **CONFIRMED** under `decision-rule.json:5`. **Binding gate RED**: 0 of 8 labels pass `decision-rule.json:3` at the tip. | Conflict between the count rule and the binding gate; left for L1 (§3). |

## 2. Commands and exit codes (OBS)

All runs `python3 -I -B`. The tool reports `rc` as the process exit.

```
# selftests (lane)
routed-r18.py --selftest                      -> SELFTEST: CLEAN cases=13   exit 0
province-pins.py --selftest                   -> SELFTEST: CLEAN cases=35   exit 0
wave-outcomes.py --selftest                   -> SELFTEST: CLEAN cases=33   exit 0
rea-catalog.py --selftest                     -> SELFTEST: CLEAN cases=7    exit 0

# C1
routed-r18.py --root . --rev 8a8da7e…        --strict -> open 7 named 7 subst 7   exit 1
routed-r18.py --root <LANE abs> --rev d0690fd… --strict -> open 0 named 0 subst 0 exit 0
routed-r18.py --root <clone d0690fd> --rev d0690fd… --strict -> open 0 named 0 subst 0 exit 0
routed-r18.py --root . --rev refs/heads/main --strict    -> open 1 (R18-HEAD-ALIASES subst False) exit 1   [relative-root artifact, §2 L1]
routed-r18.py --root <abs> --rev 8a8da7e…   --strict -> open 7                      exit 1

# C2
province-pins.py --root . --rev 8a8da7e… --strict -> mismatch_count 2 (Devin lines [9,16,44] 6.5.0; OMP lines [9,17,44] 6.5.0 vs live 6.7.0)  exit 1
province-pins.py --root <abs> --rev d0690fd… --strict -> mismatch_count 0          exit 0
c1-census-v10.py --root <clone @8a8da7e>  -> VERDICT: FAIL (stale=4 ambiguous=0 undeclared=2 unresolved=0)  exit 1
c1-census-v10.py --root <clone @d0690fd>  -> VERDICT: FAIL (stale=0 ambiguous=0 undeclared=2 unresolved=0)  exit 1
c1-census-v10.py --root . --rev 8a8da7e… -> "unrecognized arguments: --rev"            exit 2
c1-census-v10.py --root . (live)           -> VERDICT: FAIL (stale=0 … undeclared=2)  exit 1

# C3 (OBS; read-only)
sha256sum -c .ufo/waves/round-19/predictions/SHA256SUMS   (run from wave dir) -> 19 OK  exit 0
sha256sum <8 carriers + link>                          -> all 8 equal predictions/carriers.tsv; link a4286eaf… equals decision-rule excluded entry  exit 0
git diff --quiet a1140e7 d0690fd -- predictions gen-predictions.py run-carriers.sh -> exit 0
sha256(decision-rule.json) at a1140e7 == at d0690fd = 3d94a7c0fc92d9af71fd3d670349acd18ce4b9ad6ccfa161b406a23d6620c8f8   exit 0
runs/<label>/carrier-run.exit = 0 (×8);  observation.exit = 0 (×8);  compare.exit = 0 (asm,cgo,compile,cover,go,gofmt,preprofile), 1 (vet)
runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log  sha256 a5de7622… == observation.json log_sha256   exit 0
receipt-validate.py <runs/t1250-<label>/receipt.json> --require-mid-maps -> exit 1 for all 8 labels
receipt-validate.py <evidence/validate16-remap/copies/*.json> --require-mid-maps -> exit 0 for all 8 copies (round-18 receipts; not C3)

# SOURCES
scripts/sources-census.sh validate --root <fleet> kaidoku -> "kaidoku W04 S033 duplicate url…" + "kaidoku ok corpus/SOURCES.md"  exit 0
grep rows S### in corpus/SOURCES.md -> 38 (B had 36; S037, S038 added: 3 insertions, git diff exit 0)
```

Not run: `rea-catalog.py` beyond selftest; any REA/Ghidra command; `doctor`; builds; the wider suite.

## 3. C3 detail (observation vs decision rule)

- **Binding gate (`decision-rule.json:3`) is red at the tip.** Each receipt fails `receipt-validate.py --require-mid-maps` with `sha256_mismatch` on `.ufo/waves/round-17/tools/receipt-validate.py` (expected `70672eb3…`, actual `9276b198…`) and `size_mismatch` (46047 vs 51075 bytes). OBS: `/tmp/kr19-w2-rv-go.txt:18,25`. INF: the validator was edited by the R18-MIDMAP fix (`4f6c73f`), so the receipts' pins are stale.
- **The exit-0 evidence used an out-of-lane pins file.** `evidence/receipt-validation/t1250-go.json:10` records `"pins_path": "/tmp/pins.py"`. That file exists outside the repo (`/tmp/pins.py`, mtime 16:07). The `lessons/round-19.md` C3 section (`:112-118`) describes the validator being run "from an extracted file" with bytes restored. So the retained exit-0 evidence is not reproducible from the lane.
- **Mechanism verdict (`decision-rule.json:5`), applied to logs:**
  - D = {`t1250-vet`}. Its log has one Invalid index, `13902080` (`runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:229`), which is in `h1_only_invalid_indexes` (`decision-rule.json`).
  - No index outside the frozen H1 list appears.
  - `Go analysis failure` appears only in the vet log (`:186`). A grep of the seven non-D logs returned no matches.
  - So the frozen mechanism clause gives **CONFIRMED**.
- **Prediction vs observation for vet (`runs/t1250-vet/compare.json`, `extra.invalid_index_reads`, match false):** predicted `[13902080, 852107777, 1801722468838924630]`, observed `[13902080]`. Two of three predicted indices are absent. The "at least one h1-only value" threshold is what makes it confirmed. INF: the rule is lenient.
- **Count:** 8 labels have log + compare.json + receipt + observation, per the count rule (`decision-rule.json:6`, `claims.json:40`). The gate-count under `binding_gate` is 0.
- **Excluded:** `t1250-link` (no build info; no run dir; `decision-rule.json` excluded).

## 4. Mutation tests (own clone only)

Clone: `/tmp/kr19-w2-JgyKLh/main`, mutant commit `24a6cac3…` (two edits: `PROVINCE.md:16` Devin pin `6.7.0`→`6.5.0`; `.ufo/gates/citation-drift/citation-drift-probe.py:335` `if rev == "@":` → `if rev == "@" and False:`).

| Probe | Control at `d0690fd` | Mutant `24a6cac3` | Reading |
|---|---|---|---|
| M1 `province-pins.py --rev <mutant> ` | mismatch 0 | mismatch **1** (Devin, lines [16], stated 6.5.0, live 6.7.0) | detects the drift |
| M1 `c1-census-v10.py --root <mutant clone>` | stale 0 | stale **1** (`:16 [pin] devin=6.5.0 -> STALE`), VERDICT FAIL | detects the drift |
| M2 `routed-r18.py --rev <mutant>` | open 0 | open **1**, `R18-HEAD-ALIASES` subst False: "HEAD aliases not refused: @->1" | the substance check discriminates |

Both mutants were red on the expected check and returned to green on the control. Clone selftests on the mutant: `routed-r18` CLEAN 13, `province-pins` CLEAN 35.

## 5. Limits and findings for the L1

1. **C3 binding gate vs count rule (highest priority).** The frozen `binding_gate` (`decision-rule.json:3`) requires `receipt-validate --require-mid-maps` exit 0; it fails 8/8 at the tip (§3). The `count_rule` (`:6`) ignores that gate. The `claims.json:40` count of 8 is therefore only true under `count_rule`. The mechanism verdict (CONFIRMED) is also conditional on that gate. I report both verbatim; the choice is L1's.
2. **`routed-r18.py` root-spelling defect (L1 to decide).** With `--root .` and `--rev d0690fd`, the result is open 1 (R18-HEAD-ALIASES, "refs/heads/main also refused") in both the live lane and a clone. With an absolute root the same tool gives open 0. Cause: `routed-r18.py:197,201,206` pass `g.root` to the probe with `cwd=tmp`, so a relative root does not resolve and the probe exits 2 (verified: probe exit 2 from `/tmp` with `--root .`, `refs/heads/main`). The claim's own command (`claims.json:13`, `--root LANE`) is absolute, so C1 stands, but the gate is not reproducible from a relative root.
3. **Live-tree dependence.** The substance check runs the probe against `--root` (the live working tree), not `--rev`. So R18-HEAD-ALIASES can change with L1's uncommitted edits. Measured results here are committed-tree.
4. **`c1-census-v10.py` has no `--rev`** (exit 2). Its claim command (`claims.json:20`) is therefore not runnable as written; I measured "at 8a8da7e" by checking out the baseline in a clone.
5. **C2 PASS not reached.** The amendment (`claims.json:39`) says FAIL remains on the two pre-existing undeclared blocks (`SCORECARD.md:2380-2382`, `SKILL.md:511-519`). Observed: undeclared 2. The original falsifiable text (`claims.json:20`, "-> PASS (exit 0)") is superseded. The census warns `G11 current-ok without receipt language: PROVINCE.md:44` (OBS, census output).
6. **Gate scope.** `.ufo/gates/c1-census-v10.py` is unchanged `8a8da7e..d0690fd` (OBS, `git diff --stat` empty). So the scope table was not widened. I did not audit every DATED block of the 27+32 changed SKILL/PROVINCE lines.
7. **Process disclosures already in the lesson, not re-verified by me:** `corpus/lessons/round-19.md:87` (row 5) says w1 `InstallRecordDraft` ran `go version` with the C3 carrier `bin/go`, contrary to `contract.md` ("Never execute a carrier binary"). The lesson states no C3 measurement uses it. I did not grep the run logs for it (INF from lesson text only). `:88` (row 6): 42 of 90 wave-1 seats left no report.
8. **Wave-2 landing (OBS).** `wave2-result.txt` and `wave2-result-attempt2.txt` both fail with "Background job limit reached (100)". `wave2-result-attempt3.txt` spawned 72 agents. At last check `w2/` held `MutMidmap.md` and `ReopenS038.md` only.
9. **No outside verifier.** `corpus/lessons/round-19.md` "Outside spot-check" is "Pending" (OBS). This table is author-side seat evidence, not outside verification.
10. **Unexplained observation, not relied on.** One early `province-pins.py --rev HEAD` run in the mutant clone wrote non-JSON (the JSON parse failed). It did not recur: a later `--rev HEAD` in the lane gave 2951 bytes of JSON, exit 0. I did not diagnose it.

## 6. Checks the main agent should run once

- `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root <abs LANE> --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict` (expect exit 0, open 0).
- `python3 -I -B .ufo/gates/c1-census-v10.py --root <abs LANE>` (expect exit 1, stale 0, undeclared 2).
- `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-19/runs/t1250-go/receipt.json --require-mid-maps` (currently exit 1; this is the C3 binding gate).

## 7. Artifacts

- This report: `.ufo/waves/round-19/w2/ReportEvidence.md`.
- Clones (disposable): `/tmp/kr19-w2-clean-pBrx0X/main`, `/tmp/kr19-w2-JgyKLh/{base,main}`.
- Scratch outputs: `/tmp/kr19-w2-*.json|txt`.
