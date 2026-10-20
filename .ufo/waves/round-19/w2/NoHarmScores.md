# Round 19 wave 2 — no-harm scores

Scope: immutable B `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` → observed `refs/heads/main` / `HEAD` `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git rev-parse refs/heads/main`, exit 0). The workspace had uncommitted integration changes; this report measures the two commit objects, not the moving worktree. No production files changed for this review.

## Findings, by severity

### High — coverage proxy drops; the no-harm and saturation statements are false at main

**Observation.** Re-running the source-derived recipe in `SCORECARD.md:93-123` over Git blobs gives B = 96 knowledge files / 96 mapped, no missing or dangling names, coverage 10.0; main = 97 files / 96 mapped, missing `2026-10-20-r19-go125-toolchain-replay`, no dangling names, coverage 9.9 (`round(10 * 96 / 97, 2)`). Depth is 17/17 citation-resolved rules at both revisions, score 10.0 at both.

The immutable README diff adds the R19 entry to the `Knowledge` index at `corpus/README.md:154` and the round index at `:170`; it does not add the R19 token to the `Coverage map` row at `:35`. The new knowledge file is `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`. The scorecard instead says coverage is unchanged and claims 10.0 saturation at `SCORECARD.md:2497-2498`. Its own prior round-18 map measure is 95/95→96/96 at `:2454`.

**Inference.** The command-defined index-completeness proxy regresses by 0.1 at main; this establishes a proxy/index regression, not a loss of domain knowledge. Because coverage is one of the three finite owned proxies, the claim that all three remain saturated at 10.0 is not supported. This is a concrete no-harm failure even though the round-19 entry deepens already-held Go ground.

**Reproduction, exit 0** (same source-blob algorithm as `SCORECARD.md:93-123`, adapted to take both revisions):

```bash
python3 -I -B -c 'import json,pathlib,re,subprocess,sys
for rev in sys.argv[1:]:
 def get(path): return subprocess.check_output(["git","show",f"{rev}:{path}"],text=True)
 paths=subprocess.check_output(["git","ls-tree","-r","--name-only",rev,"--","corpus/knowledge"],text=True).splitlines()
 files={pathlib.PurePosixPath(p).stem for p in paths if p.endswith(".md")}
 section=get("corpus/README.md").split("## Coverage map\n",1)[1].split("\n## ",1)[0]
 mapped=set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+",section))
 craft=get("SKILL.md").split("## Queue-drain craft ",1)[1].split("\n## ",1)[0]
 rules=re.split(r"(?m)^- \*\*",craft)[1:]
 pattern=r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
 resolved=0
 for rule in rules:
  refs=re.findall(pattern,rule); valid=bool(refs)
  for name,first,last in refs:
   try:
    count=len(get("corpus/knowledge/"+name).splitlines()); start,end=int(first or 1),int(last or first or 1); valid=valid and 1<=start<=end<=count
   except subprocess.CalledProcessError: valid=False
  resolved+=valid
 print(json.dumps({"revision":rev,"knowledge_files":len(files),"mapped":len(files & mapped),"missing":sorted(files-mapped),"dangling":sorted(mapped-files),"citation_resolved_rules":resolved,"rule_blocks":len(rules),"coverage_score":round(10*len(files & mapped)/len(files),2),"depth_score":round(10*resolved/len(rules),2)},sort_keys=True))
' 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 d0690fd44f46d8a7fe9da5f01c6be723d12abd41
```

Output:

```text
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 96, "mapped": 96, "missing": [], "revision": "8a8da7e19375aadc66c6bcbff0bbcbb596048fb0", "rule_blocks": 17}
{"citation_resolved_rules": 17, "coverage_score": 9.9, "dangling": [], "depth_score": 10.0, "knowledge_files": 97, "mapped": 96, "missing": ["2026-10-20-r19-go125-toolchain-replay"], "revision": "d0690fd44f46d8a7fe9da5f01c6be723d12abd41", "rule_blocks": 17}
EXIT: 0
```

### Medium — calibration’s 7→0 closure is not verified by the committed final record

**Observation.** B’s retained routed-R18 result has `open_count=7`, `named_open=7`, `substance_open=7` (`.ufo/waves/round-19/evidence/routed-r18-B.json:46-49`). The first integrated result is bound to `4f6c73f81ae8d31de18377d7ff57e4e10140ce48`, an ancestor of main, but reports `open_count=1`, `named_open=0`, `substance_open=1`; the remaining `R18-INSTALL-RECORD` lacks version/full SHA-256/channel for Go 1.24.6 and 1.25.0 (`.ufo/waves/round-19/evidence/routed-r18-integrated.json:40-49`). The amended claim explicitly says a second pass must use final validator bytes and live receipt validation (`.ufo/waves/round-19/claims.json:44-46`). There is no `runs/pass2` or `verify/` entry in the main tree (`git ls-tree -r --name-only <main> -- .ufo/waves/round-19/runs/pass2`, exit 0 with empty output; same for `.ufo/waves/round-19/verify`). `SCORECARD.md:2479` says final measured records are to be appended after integration; `:2493` likewise leaves the final verdict pending. The R19 numeric calibration proxy is stated as 10.0→10.0 at `:2493`; freshness has no owned numeric proxy at `:2494`.

**Inference.** No numeric calibration-score decrease is shown, but the C1 claim that all seven defects close to zero is not demonstrated at the delivered main revision. The first-pass result is insufficient to call C1 complete; the referenced second pass is outside the main tree. Calibration should remain “unverified” until the final-revision result is committed. This is a verification gap, not evidence that the first-pass residual remains after the later uncommitted work.

Commands: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 4f6c73f81ae8d31de18377d7ff57e4e10140ce48 d0690fd44f46d8a7fe9da5f01c6be723d12abd41` — exit 0; `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only d0690fd44f46d8a7fe9da5f01c6be723d12abd41 -- .ufo/waves/round-19/runs/pass2` — exit 0, empty.

## Re-derived status and other checks

- **Coverage:** B 10.0 → main 9.9, as above. **Depth:** 10.0 → 10.0 (17/17 citation-resolved queue-drain rules at each revision). **Calibration:** the finite numeric proxy is stated as 10.0 → 10.0, but is not newly recomputed by the round-19 artifacts; the seven-defect C1 outcome is pending the final-revision check above. Calibration is therefore not shown numerically harmed, but C1’s claimed closure is not verified.
- **Saturation/window:** observation at `SCORECARD.md:2458`: the round-18 record says saturation 10.0, window N=10, last capability entry round 17, and no capability row entered in round 18. At `:2497-2498`, round 19 says no capability row enters and repeats 10.0/window 10. Inference: by consecutive lane-round counting, the stagnation interval is 1/10 at the end of R18 and 2/10 at R19; the nudge is inactive. The “all owned proxies saturated” statement is contradicted by the 9.9 coverage result.
- **Capabilities:** no R19 capability-table row is added (`SCORECARD.md:2497`); therefore the capability count/last-entry round do not change B→main. The knowledge addition is not a newly demonstrated capability row.
- **S001–S036 evidence cells:** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --unified=0 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 d0690fd44f46d8a7fe9da5f01c6be723d12abd41 -- corpus/SOURCES.md` — exit 0; only S037/S038 and the round-19 search-log entry are additions. No rows S001–S036 changed or were deleted (`corpus/SOURCES.md:7-42`); the new rows are `:43-44`.

## Residual risk and verification gaps

The LSP device is unavailable: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics were possible. Grep results were used only to locate text, not as semantic proof. No build, broad test suite, REA/Ghidra analysis, or carrier execution was run. The metric check reads immutable Git blobs; C1 final verification is absent from the committed main tree.