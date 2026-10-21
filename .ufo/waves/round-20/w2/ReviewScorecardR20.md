PARTIAL — the SCORECARD addition is append-only and C2/C3 counts re-derive; C1 is not closed at source S.

## Findings (by severity)

- **High — C1 zero-open target is unmet at S.** `SCORECARD.md:2596` gives routed items `11→0 target` and census `FAIL/1→PASS/0`; `:2578` says final measured records will be appended later. At S, `routed-r19.py:47,55,644-650,1037-1045` includes D5 and counts it open when its substance check fails. The check requires `.ufo/waves/round-20/verify/final-census.json`; the Git object is absent at S (`git cat-file -e S:<path>` exit 128; exact command below), so D5 cannot pass and the counter's open count cannot be zero at S. This establishes an unmet target, not that a live census run would itself fail.
- **Medium — measured revision/evidence identity is omitted.** `SCORECARD.md:2571-2578` names baseline B, declaration, and freeze F, but not measured source S or the verification-evidence revision; `:2578` remains a forward reference. The assignment pin supplies S for this review, but the scorecard section is not independently self-contained on measured commits.

## Re-derived observations

- **Append-only:** `git diff --no-ext-diff --unified=0 B S -- SCORECARD.md` exited 0: 31 insertions, 0 deletions.
- **QUALITY count:** `git diff --no-ext-diff --unified=3 B S -- corpus/QUALITY.md` exited 0 and contains only new rows 23–25 (`corpus/QUALITY.md:33-35`); rows 1–22 are unchanged. Thus 22→25 re-derives.
- **C2 (`SCORECARD.md:2597`):** the source-S `verb-coverage.py` run exited 0 for both revisions: B = 128/153 named, 0/5 targets exercised; S = 133/153 named, 5/5 exercised. Exact commands and summaries are below.
- **C3 (`SCORECARD.md:2598`):** a read-only harness loaded `measure.py` from S's Git blob and called its `_claim_c3` for B and S; exit 0. B had 0 predictions/receipts/comparisons bound; S had 19 freeze-equal predictions, 19 valid receipts, 19 comparison records, 19 bound, 19 matched. A separate Git-object parse exited 0: 8 `invalid_index` forecasts, 11 silent forecasts, 19/19 comparisons matched; retained retro CSV had 8 rows, all yes. No Go toolchain, REA analyze, or Ghidra was run.
- **Version-scope question:** the appended 31 SCORECARD lines contain no `X.Y.Z` token (scan exit 0, zero matches). They are outside the census `SCORECARD.md` ranges (`c1-census-v10.py:255-280`), but the new line `:2590` uses only the placeholder `rea-agents@<v>`, not a version. The census's pin/version patterns are at `c1-census-v10.py:328-332`. I did not execute the live census: its source reads client configuration files including `~/.omp/agent/mcp.json` (`:243-246,342-352`), prohibited by the contract.

## Commands and exits

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=0 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- SCORECARD.md
# exit 0; 31 insertions, 0 deletions

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=3 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- corpus/QUALITY.md
# exit 0; rows 23–25 added only

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/verify/final-census.json
# exit 128: path absent

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/verify/final-census.json
# exit 0; no row
```

C2 commands (each exit 0):

```sh
set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/tools/verb-coverage.py | python3 -I -B - --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 14f0260ad319ecc26994381b2415d5a999003375 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({"rev":d["rev"],"catalog":len(d["cli_commands"]),"mentioned":len(d["mentioned"]),"targets":{k:v["exercised"] for k,v in d["targets"].items()},"exercised":sum(v["exercised"] for v in d["targets"].values())},sort_keys=True))'
# {catalog:153, mentioned:128, exercised:0, all five targets false}

set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/tools/verb-coverage.py | python3 -I -B - --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 | python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({"rev":d["rev"],"catalog":len(d["cli_commands"]),"mentioned":len(d["mentioned"]),"targets":{k:v["exercised"] for k,v in d["targets"].items()},"exercised":sum(v["exercised"] for v in d["targets"].values())},sort_keys=True))'
# {catalog:153, mentioned:133, exercised:5, all five targets true}
```

C3 derivation command (exit 0; loads only S's `measure.py` blob and invokes its C3 helper):

```sh
python3 -I -B -c 'import json,subprocess,tempfile; from pathlib import Path; root=Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin"); baseline="14f0260ad319ecc26994381b2415d5a999003375"; source="5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9"; freeze="808cbb31a1e24656da5ba4967497e602fbca7415"; code=subprocess.check_output(["git","-C",str(root),"show",f"{source}:.ufo/waves/round-20/measure.py"]); filename="/tmp/review-measure-r20.py"; ns={"__name__":"review_measure_r20","__file__":filename}; exec(compile(code,filename,"exec"),ns); results=[]; exec("for rev in (baseline, source):\n paths=ns[\"_tree\"](root,rev)\n with tempfile.TemporaryDirectory(prefix=\"review-c3-\") as d:\n  c3=ns[\"_claim_c3\"](root,rev,freeze,paths,Path(d))\n results.append({\"rev\":rev,\"status\":c3[\"status\"],\"first_failure_bound\":c3[\"first_failure_bound\"],\"matched\":c3[\"matched\"],\"prediction_files\":c3[\"raw_counts\"][\"prediction_files\"],\"freeze_equal_predictions\":c3[\"raw_counts\"][\"freeze_equal_predictions\"],\"receipt_valid\":c3[\"raw_counts\"][\"receipt_valid\"],\"compare_records\":c3[\"raw_counts\"][\"compare_records\"]})"); print(json.dumps(results,sort_keys=True))'
# exit 0; B: 0/0, S: 19/19 bound and 19/19 matched; predictions, valid receipts, comparisons all 19
```

The X.Y.Z scan command was:
```sh
set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=0 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- SCORECARD.md | python3 -c 'import re,sys; rows=[(line,re.findall(r"\b\d+\.\d+\.\d+\b",line)) for line in sys.stdin.read().splitlines() if line.startswith("+") and not line.startswith("+++")]; hits=[(line,values) for line,values in rows if values]; print("added_version_loci:",hits); print("added_lines_scanned:",len(rows))'
# exit 0; 31 lines scanned, no matches
```
The C3 forecast distribution and retro comparison were parsed from Git objects at S with:
```sh
python3 -I -B -c 'import csv,io,json,subprocess; root="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; rev="5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9"; files=subprocess.check_output(["git","-C",root,"ls-tree","-r","--name-only","-z",rev]).decode().split("\0"); paths=[p for p in files if p.startswith(".ufo/waves/round-20/evidence/compare-rerun/") and p.endswith(".json")]; records=[json.loads(subprocess.check_output(["git","-C",root,"show",f"{rev}:{p}"])) for p in paths]; predicted=[r.get("predicted") for r in records]; retro=subprocess.check_output(["git","-C",root,"show",f"{rev}:.ufo/waves/round-20/evidence/retro-v2/retro-v2.csv"]).decode(); rows=list(csv.DictReader(io.StringIO(retro))); print(json.dumps({"comparison_files":len(records),"invalid_index_predictions":sum(isinstance(p,dict) and p.get("kind")=="invalid_index" for p in predicted),"silent_predictions":sum(p is None for p in predicted),"matches":sum(r.get("match") is True for r in records),"retro_rows":len(rows),"retro_yes":sum(r.get("match")=="yes" for r in rows)},sort_keys=True))'
# exit 0; 19 comparisons, 8 invalid_index, 11 silent, 19 matches; retro 8/8
```

## Residual risk / verification gap

The final live census PASS remains unverified here: running it would read protected client configuration. Since D5's required record is absent from S, the claimed C1 zero-open result is not attained by the revision-scoped counter regardless. No installs, lane mutations other than this report, REA runtime, Go binary, Ghidra, or `jj` command were used.