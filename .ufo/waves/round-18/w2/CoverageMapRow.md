HOLDS

# CoverageMapRow: README coverage-map row 35 (r18 edit) and knowledge-index completeness

Seat: `KaidokuR18.CoverageMapRow`, an author-side advisory seat (round 18, wave 2 falsify). It is not an outside reviewer.
Revisions: R = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, B = `9011581d84527ba34c675f9cf912e54d2e72d470`, F (C3 freeze) = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
Anchors are `git show R:path` line numbers unless marked otherwise. I ran no REA or Ghidra, executed no carrier, installed nothing, and wrote nothing in the lane except this file.
Lane state while I worked: `git rev-parse HEAD` = R. `git status --porcelain` showed 9 untracked wave-2 entries and no modified tracked files.
Axes checked: row accuracy (calibration), index completeness (coverage), reproducibility with the lane's own recipe (operability), and the evidence chain behind "confirmed" (depth).

## Verdict

- **Row 35 edit: holds.** The edit only appends text: each of the three cells in B is a byte prefix of the matching cell in R. The row was added in the same commit as its file. Every factual token in the added text reproduces from retained Git objects (§1).
- **Index: holds.** `## Coverage map` indexes all 96 `corpus/knowledge/*.md` stems, with 0 missing and 0 dangling. The lane's canonical SCORECARD recipe A gives B 95/95 and R 96/96 (§2).
- **Recorded, not a break:** the second table, `## Knowledge`, lists only 79 of the 96 files. 16 were already missing at B, and this round adds 1 (r18). Under the old r14-02 "check 1" reading that table must be complete, so the index would be PARTIAL at both B and R. The current lane measure counts only the coverage map (§2).

## 1. Row 35 claims vs evidence (OBSERVATION unless labelled)

Edit shape: the diff B..R changes exactly one line, `corpus/README.md:35`. The cell count stays at 3. Cell lengths grow 205→240, 916→1290 and 578→756 characters, and each B cell is a prefix of its R cell (C2). In commit `b2aad08` the README is `M` and `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` is `A` (C3). That satisfies `corpus/README.md:9` and fleet `CORPUS.md:46` ("write the row when the file exists").

| README:35 claim | Evidence at R | Status |
|---|---|---|
| entry `2026-10-20-r18-swiss-map-replay` | File exists (119 lines). Recipe A maps it (C4). | holds |
| "r18 replays it" (aether's EOF) | The calib-aether log has 1 `read past EOF` (C9). In compare.json, `extra.eof_reads` is observed `[[17645861,111938854]]`, which equals the prediction (C8). Knowledge entry `:74`. | holds |
| "predicted per carrier before the run" | All 15 `producer.json` record `branch_tip` = F (C10), so the freeze commit existed when each run was produced. `predictions/` is unchanged F..R: 0 files differ, and F is an ancestor of R (C11). F was committed at 13:23:55 -0300; the first run started at 13:24:07-03:00 (`runs/run-log.txt:2`). See also `LOG.md:2150-2152`. | holds |
| "confirmed on two held-out carriers" | `predictions/decision-rule.json` sets held_out_D = {s1246-swiss-nethttp, real-kimi-webbridge}. Only 3 of 15 logs contain `Go analysis failure`: calib-aether plus the two held-out labels. The noswiss sibling and the 11 non-D synthetic labels are clean (C9). That meets the frozen "confirmed" clause. Knowledge entry `:83-87`. | holds |
| synthetic go1.24.6 `Invalid index: 22386945` | inspect-go reports `"go1.24.6"` (C10). `ghidra.log` (`rea-ghidra-zHRS1l`) has the failure at l.408 and the index at l.451 (C12). The frozen F prediction lists `invalid_index_reads [22386945]` (C13). | holds |
| real go1.24.13 kimi-webbridge `Invalid index: 15606016` | inspect-go reports `"go1.24.13"`. `ghidra.log` (`rea-ghidra-ZSUHpG`) has the failure at l.73 and the index at l.206. The frozen prediction lists `[15606016]`. | holds |
| "15/15 labels matched" | `compare.exit` is 0 for all 15. `all_match` is true for all 15, and each compare carries `extra.eof_reads` (C8). `receipt-validate.py --require-mid-maps` exits 0 on 15/15 receipts, with 360–372 checks each (C7). All 15 receipts carry the frozen prediction's carrier sha256 in `carrier/sha256_pre` and `sha256_post`, which is the binding gate (C14). | holds |
| "first observed intermediate patch fallback (1.24.13→1.24.6)" | The kimi `ghidra.log` has `WARN … Falling back from 1.24.13 to 1.24.6` at l.68 (C12). Ghidra's installed diffs for 1.24 are go1.24.1–go1.24.6, so 1.24.6 is a non-base diff (C15). The 8 retained r17 logs show only (1.25.14→1.25.0) and (1.25.8→1.25.0) (C16). r17 `:129` says "fallback to an intermediate diff was never observed". The only earlier lane mentions at B were worked out from source code, not seen in logs: `.ufo/waves/round-15/w1/PatchLookup.md:155-160` (Case C) and `.ufo/waves/round-17/w1/ScoutGoDataInventory.md:140`, which itself says "derived, not observed" (C17). | holds against the lane record; "first" beyond that is INFERENCE |
| cell 3: `run-carriers.sh <LABEL>`, receipts in `runs/`, predictions frozen at `eb6c266` | `.ufo/waves/round-18/run-carriers.sh:1-13` takes labels from `predictions/carriers.tsv` and supports `RUNS_DIR` for a non-destructive recheck. There are 15 `receipt.json` under `runs/`. F's subject is "frozen C3 predictions and decision rule … (pre-run)". | holds |

The "first observed" claim does not appear in the r18 entry itself. It is supported jointly by two entries indexed in this same row (r17 `:129` and r18 `:81`) and by `LOG.md:2157-2158`.

## 2. Index completeness: files vs indexed names

Denominator: 96 `corpus/knowledge/*.md` files at R. `.gitkeep` is excluded. Four files under `.ufo/waves/round-17/w2/temporal-attack/fixtures/rev*/corpus/knowledge/` are also excluded; that they are test fixtures is an INFERENCE from their path.

| Measure | B | R |
|---|---|---|
| knowledge files | 95 | 96 |
| `## Coverage map` (README:11-68), SCORECARD recipe A (`SCORECARD.md:92-124`) | 95/95, missing [], dangling [] | 96/96, missing [], dangling [] |
| coverage map, entry cells only (my parser) | n/a | 96/96; 0 files cited only outside entry cells |
| `## Knowledge` table, first cell (README:70-153) | 79/95, 16 missing | 79/96, 17 missing |

The 17 files missing from `## Knowledge` at R:
- arc2-r6-pe-midrung and arc2-r7-pe-wall
- arc3 r1, r3, r4, r6, r7, r8, r9, r10, r11 and r12
- the Go entries r14, r15, r16 and r17
- r18-swiss-map-replay

All 17 are in the coverage map. The last `## Knowledge` row is dated 2026-10-16 (README:153), so no file landed since 2026-10-18 has been added to that table. The r18 edit follows the precedent set by r14–r17.

Which table is the index:
- Fleet `CORPUS.md:11` calls README "index: what's here, coverage map, known gaps, frontier".
- `LEARNING.md:65` says "the coverage map plus a `## Frontier` list".
- Recipe A splits only the `## Coverage map` section (`SCORECARD.md:101`).
- `## Knowledge` completeness was last checked as r14-02 "check 1": `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:78` reports 70/70.
- No current rule requires it: grepping SKILL.md, MINT.md, AGENTS.md, PROVINCE.md and corpus/QUALITY.md for such a rule found nothing (C18).

INFERENCE: the split between the two tables is old convention drift. This edit did not introduce it.

Latent blind spot (INFERENCE): recipe A counts a dated token anywhere in the section, including state and source cells. A file cited only in passing would count as mapped. My entry-cell parser finds no such case at R.

## 3. Calibration and depth notes (none breaks the row)

**a. Held-out scope.**
- Both held-out D carriers are Go 1.24 (1.24.6 and 1.24.13).
- For Go 1.25 the mechanism rests only on calibration (calib-aether, listed as `calibration_only` in decision-rule.json) and on source S023.
- All four s1250 Swiss labels are non-diagnostic: H1 and H0 both predict no failure.
- README:35 reads "Go 1.24/1.25 … confirmed on two held-out carriers". Its parenthetical shows both carriers are go1.24.x, so the sentence is not false.
- INFERENCE: a quick read could take it as held-out confirmation for 1.25 as well. The entry's own limit is narrower: "Observed on 3 carriers (1 calibrated, 2 held out)" (r18 `:94`).

**b. Passes.** The r17 part of the same cell says "two passes each". The r18 part does not say it ran one pass only, which the entry records at r18 `:116` ("Determinism: one pass only").

**c. Where the exception is thrown.**
- Neither held-out stack contains a `GoMapType` frame; the grep for `GoMapType` returns 0 lines in both logs (C12).
- s1246-swiss-nethttp: `GoTypeManager.markupGoTypes` → nested `MarkupSession.markup` calls → `GoName.getPkgPath` (l.428–465).
- kimi: the same inner chain, reached through recursive `GoStructType.additionalMarkup:94` and `GoInterfaceType.additionalMarkup:77` calls (l.100–176, l.220).
- So "confirmed" rests on the exact frozen values matching, which is how decision-rule.json defines it. It does not rest on a logged map-type frame.
- The r18 entry's INFERENCE about a struct/interface path (r18 `:101-106`) names only aether, but kimi shows the same outer recursion.

**d. Stale limit next to this row.** r17 `:129` still says "fallback to an intermediate diff was never observed". The round-18 correction appended to r17 (`:200-206`) covers only R17-PINMAP and R17-PRODUCER-REV.

## 4. Proposed move (one, bounded)

**Move.** Append one line to the existing `## Round-18 correction` section of `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, after `:206`, qualifying `:129`. Suggested text:

> the WARN row's limit "fallback to an intermediate diff was never observed" holds through round 17 only; round 18 observed `Falling back from 1.24.13 to 1.24.6` once, predicted before the run (`.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:68`; `2026-10-20-r18-swiss-map-replay.md:81`); one carrier, one Ghidra release.

**Axes.**
- Calibration improves: the only decision-table row for this WARN line stops contradicting row 35's "first observed".
- Coverage, depth and operability are unchanged: no new entry, row or tool.

**Risks.**
- It touches a filed entry. The change is append-only, in the form the section itself declares (`:200`).
- INFERENCE: any revision-pinned digest of this file has to be re-pinned. That path is already exercised, because the round appended to this file at R.

**Verification.**
- `git show NEW:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'Falling back from 1.24.13'` returns exactly 1 hit at a line > 206.
- `git diff --numstat R NEW -- <file>` prints `1 0`.
- Recipe A still reports 96/96.

## Commands (run from the lane root; exit codes observed)

Short commands are shown with `$B`/`$R`/`$F`. I ran them with the literal full hashes, so substituting those values reproduces them exactly. Long scripts are pasted verbatim.

```bash
# C1  exit 0
git diff 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- corpus/README.md; echo "EXIT=$?"
# C2  exit 0 → cells baseline: 3 rev: 3; cell1-3 baseline_prefix_of_rev=True (205->240, 916->1290, 578->756)
python3 -I -B -c '
import subprocess
BASE="9011581d84527ba34c675f9cf912e54d2e72d470"; REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True,check=True); return r.stdout
def row(rev):
    t=git("show",rev+":corpus/README.md").splitlines()
    return t[34]
b=row(BASE); r=row(REV)
bc=[c.strip() for c in b.strip().strip("|").split("|")]
rc=[c.strip() for c in r.strip().strip("|").split("|")]
print("cells baseline:",len(bc),"rev:",len(rc))
for i,(x,y) in enumerate(zip(bc,rc)):
    print(f"cell{i+1}: baseline_prefix_of_rev={y.startswith(x)} len {len(x)}->{len(y)}")
'; echo "EXIT=$?"
# C3  exit 0 → b2aad08 … M corpus/README.md, A corpus/knowledge/2026-10-20-r18-swiss-map-replay.md
git log --format='%h %ci %s' --name-status $B..$R -- corpus/README.md corpus/knowledge/2026-10-20-r18-swiss-map-replay.md; echo "EXIT=$?"
# C4  SCORECARD recipe A body (SCORECARD.md:94-122). First run via a /tmp copy for both revs (exit 0, 0), then via stdin for R (exit 0):
#     B → {"knowledge_files": 95, "mapped": 95, "missing": [], "dangling": [], "coverage_score": 10.0, …}
#     R → {"knowledge_files": 96, "mapped": 96, "missing": [], "dangling": [], "coverage_score": 10.0, …}
git show $R:SCORECARD.md | sed -n '94,122p' > /tmp/coveragemaprow-recipeA.py && for REV in $B $R; do python3 -I -B /tmp/coveragemaprow-recipeA.py "$REV"; echo "EXIT=$?"; done
git show $R:SCORECARD.md | sed -n '94,122p' | python3 -I -B - $R; echo "EXIT=$?"   # /tmp copy removed afterwards (rm exit 0)
```

```bash
# C5  exit 0 → B: coverage 95/95, Knowledge table 79 (16 unlisted); R: coverage 96/96, Knowledge table 79 (17 unlisted, list in §2)
python3 -I -B -c '
import subprocess, re
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True,check=True); return r.stdout
DATED=re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")
ANY=re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+")
R14=re.compile(r"2026-10-1[0-9]-[a-z0-9-]+")
def sec(lines,title):
    s=next(i for i,l in enumerate(lines) if l.strip()=="## "+title)+1
    e=next((j for j in range(s,len(lines)) if lines[j].startswith("## ")),len(lines))
    return s,e
def toks_bt(text):
    out=set()
    for t in re.findall(r"`([^`]+)`",text):
        if t.startswith("knowledge/"): t=t[len("knowledge/"):]
        if t.endswith(".md"): t=t[:-3]
        if DATED.match(t): out.add(t)
    return out
for name,REV in [("BASE","9011581d84527ba34c675f9cf912e54d2e72d470"),("REV","b2aad08ceeee8dd125ce0d316056d8bd766c7f94")]:
    lines=git("show",REV+":corpus/README.md").splitlines()
    files={p.split("/")[-1][:-3] for p in git("ls-tree","--name-only",REV,"corpus/knowledge/").splitlines() if p.endswith(".md")}
    cs,ce=sec(lines,"Coverage map"); ks,ke=sec(lines,"Knowledge")
    ctext="\n".join(lines[cs:ce]); ktext="\n".join(lines[ks:ke])
    # knowledge table: first cell only
    kfirst=set()
    for l in lines[ks:ke]:
        if l.startswith("|"):
            c=[x.strip() for x in l.strip().strip("|").split("|")]
            kfirst|=toks_bt(c[0])
    cbt=toks_bt(ctext); cany=set(ANY.findall(ctext)); cany_f={t for t in cany if t in files}
    print(f"== {name} {REV[:7]} files={len(files)}")
    print(f"  coverage_map backtick-tokens={len(cbt)} covered_files={len(cbt&files)} unmapped={sorted(files-cbt)} dangling={sorted(cbt-files)}")
    print(f"  coverage_map any-text tokens matching a file={len(cany_f)} unmapped_by_anytext={sorted(files-cany_f)}")
    print(f"  knowledge_table first-cell tokens={len(kfirst)} covered_files={len(kfirst&files)} dangling={sorted(kfirst-files)}")
    print(f"  knowledge_table unlisted ({len(files-kfirst)}): {sorted(files-kfirst)}")
    r14c={t for t in R14.findall(ctext)}; 
    print(f"  r14-02 literal regex 2026-10-1[0-9]: coverage tokens={len(r14c&files)}; files invisible to it={len([f for f in files if not R14.fullmatch(f)])}")
'; echo "EXIT=$?"
# C6  exit 0 → files 96 entry_cell_indexed 96 missing_from_entry_cells []; files_cited_only_outside_entry_cells: []
python3 -I -B -c '
import subprocess, re
REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
def git(*a): return subprocess.run(["git"]+list(a),capture_output=True,text=True,check=True).stdout
lines=git("show",REV+":corpus/README.md").splitlines()
files={p.split("/")[-1][:-3] for p in git("ls-tree","--name-only",REV,"corpus/knowledge/").splitlines() if p.endswith(".md")}
s=lines.index("## Coverage map")+1; e=next(j for j in range(s,len(lines)) if lines[j].startswith("## "))
DATED=re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+")
entry=set(); elsewhere={}
for i in range(s,e):
    l=lines[i]
    if not l.startswith("|") or l.startswith("|---") or l.startswith("| section"): continue
    c=[x.strip() for x in l.strip().strip("|").split("|")]
    ecell = c[0] if c[0].startswith("`knowledge/") else c[1]
    ent=set()
    for t in re.findall(r"`([^`]+)`",ecell):
        t=t[len("knowledge/"):] if t.startswith("knowledge/") else t
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+",t): ent.add(t)
    entry|=ent
    for t in set(DATED.findall(l))-ent: elsewhere.setdefault(t,[]).append(i+1)
print("files",len(files),"entry_cell_indexed",len(entry&files),"missing_from_entry_cells",sorted(files-entry))
only_cited=sorted(t for t in elsewhere if t in files and t not in entry)
print("files_cited_only_outside_entry_cells:",only_cited)
print("non-entry citations of files (name:lines):",{t:v for t,v in elsewhere.items() if t in files})
'; echo "EXIT=$?"
```

```bash
# C7  exit 0 → validated_ok: 15 / 15 (checks 360–372 each). Worktree run: HEAD = R, no tracked modifications.
python3 -I -B -c '
import subprocess, json
out=subprocess.run(["git","ls-tree","--name-only","HEAD",".ufo/waves/round-18/runs/"],capture_output=True,text=True).stdout.splitlines()
labels=[p for p in out if p.split("/")[-1]!="run-log.txt"]
print("labels:",len(labels))
ok=0; bad=[]
for full in sorted(labels):
    L=full.split("/")[-1]
    r=subprocess.run(["python3","-I","-B",".ufo/waves/round-17/tools/receipt-validate.py","--require-mid-maps",full+"/receipt.json"],capture_output=True,text=True)
    try:
        j=json.loads(r.stdout); st=j["exit"]; n=j["counts"]["valid"]; chk=j["receipts"][0].get("checks_performed")
    except Exception: st=f"parse_err rc={r.returncode}"; n="?"; chk="?"
    if r.returncode==0 and st==0: ok+=1
    else: bad.append((L,r.returncode,(r.stderr or r.stdout)[-160:]))
    print(L,"rc",r.returncode,"validator_exit",st,"valid",n,"checks",chk)
print("validated_ok:",ok,"/ 15")
print("failures:",bad)
'; echo "EXIT=$?"
# C8  exit 0 → all_match_true: 15 / 15; every label exit 0 and has_extra.eof_reads True
python3 -I -B -c '
import subprocess, json
REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr)
    return r.stdout
labels=sorted(p.split("/")[-1] for p in git("ls-tree","--name-only",REV,".ufo/waves/round-18/runs/").splitlines() if not p.endswith("run-log.txt"))
n=0
for L in labels:
    cj=json.loads(git("show",f"{REV}:.ufo/waves/round-18/runs/{L}/compare.json"))
    ex=git("show",f"{REV}:.ufo/waves/round-18/runs/{L}/compare.exit").strip()
    has=any(f["field"]=="extra.eof_reads" for f in cj["fields"])
    n+= cj["all_match"] is True
    print(L,"all_match",cj["all_match"],"exit",ex,"has_extra.eof_reads",has)
print("all_match_true:",n,"/",len(labels))
'; echo "EXIT=$?"
# C9  exit 0 → GoAnalysisFailure only in calib-aether (ReadPastEOF:1), real-kimi-webbridge (InvalidIndex:1), s1246-swiss-nethttp (InvalidIndex:1); 12 others "-"
python3 -I -B -c '
import subprocess
REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return r.stdout
paths=[p for p in git("ls-tree","-r","--name-only","-z",REV,"--",".ufo/waves/round-18/runs/").split("\0") if p.endswith("ghidra.log")]
from collections import defaultdict
d=defaultdict(list)
for p in paths: d[p.split("/")[4]].append(p)
for L in sorted(d):
    for p in sorted(d[L]):
        t=git("show",REV+":"+p)
        print(L, p.split("/")[6], "GoAnalysisFailure" if "Go analysis failure" in t else "-", "InvalidIndex:"+str(t.count("Invalid index")), "ReadPastEOF:"+str(t.count("read past EOF")))
'; echo "EXIT=$?"
# C10 exit 0 → distinct_tips: {eb6c2668…: 15}; inspect-go versions match the labels (go1.24.6, go1.24.13, go1.25.14, …, "X:noswissmap" on noswiss)
python3 -I -B -c '
import subprocess, json
REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return r.stdout
labels=sorted(p.split("/")[-1] for p in git("ls-tree","--name-only",REV,".ufo/waves/round-18/runs/").splitlines() if not p.endswith("run-log.txt"))
tips={}
for L in labels:
    pj=json.loads(git("show",f"{REV}:.ufo/waves/round-18/runs/{L}/producer.json"))
    ig=git("show",f"{REV}:.ufo/waves/round-18/runs/{L}/inspect-go.json")
    import re
    gv=sorted(set(re.findall(r"\"go1\.[0-9]+\.[0-9]+[^\"]*\"",ig)))[:3]
    cj=json.loads(git("show",f"{REV}:.ufo/waves/round-18/runs/{L}/compare.json"))
    tips.setdefault(pj.get("branch_tip"),[]).append(L)
    keys=[k for k in cj.keys()][:12]
    print(L,"tip",pj.get("branch_tip")[:12],"go",gv,"compare_keys",keys, "match" , cj.get("match", cj.get("matched", cj.get("status"))))
print("distinct_tips:",{k:len(v) for k,v in tips.items()})
'; echo "EXIT=$?"
```

```bash
# C11 exit 0 → 0 / ANCESTOR_OK / BASELINE_OK
git diff --name-only $F $R -- .ufo/waves/round-18/predictions/ | wc -l && git merge-base --is-ancestor $F $R && echo ANCESTOR_OK; git merge-base --is-ancestor $B $R && echo BASELINE_OK; echo "EXIT=$?"
# C12 exit 0 (each) → nethttp l.408 failure / l.451 Invalid index: 22386945; kimi l.73 / l.206 Invalid index: 15606016; kimi l.68 WARN Falling back from 1.24.13 to 1.24.6; 0 GoMapType lines in either log
git show $R:.ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log | nl -ba | sed -n '408p;451p'; echo "EXIT=$?"
git show $R:.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log | nl -ba | sed -n '73p;206p'; echo "EXIT=$?"
for p in .ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log .ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log; do echo "== $p"; git show $R:$p | grep -nE 'Falling back|Using Go API snapshot|GoMapType|GoStructType|GoInterfaceType|GoName\.|GoType\.|GoUncommonType|Invalid index' | sed -n '1,30p'; done; echo "EXIT=$?"
# C13 exit 0 → 1 / 1 / 19
git show $F:.ufo/waves/round-18/predictions/s1246-swiss-nethttp.prediction.json | grep -c 22386945; git show $F:.ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json | grep -c 15606016; git ls-tree --name-only $F .ufo/waves/round-18/predictions/ | wc -l; echo "EXIT=$?"
git show $F:.ufo/waves/round-18/predictions/decision-rule.json; echo "EXIT=$?"   # exit 0; held_out_D, calibration_only, confirmed clause
```

```bash
# C14 exit 0 → labels_with_pred_sha_in_receipt: 15 / 15 (paths /carrier/sha256_pre, /carrier/sha256_post)
python3 -I -B -c '
import subprocess, json
REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"; FRZ="eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0"
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr)
    return r.stdout
def find(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from find(v,path+"/"+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from find(v,path+f"[{i}]")
    else: yield path,o
labels=sorted(p.split("/")[-1] for p in git("ls-tree","--name-only",REV,".ufo/waves/round-18/runs/").splitlines() if not p.endswith("run-log.txt"))
ok=0
for L in labels:
    pred=json.loads(git("show",f"{FRZ}:.ufo/waves/round-18/predictions/{L}.prediction.json"))["carrier"]["sha256"]
    rec=json.loads(git("show",f"{REV}:.ufo/waves/round-18/runs/{L}/receipt.json"))
    hits=sorted({p for p,v in find(rec) if v==pred})
    ok+= bool(hits)
    print(L, pred[:12], "receipt_paths_equal_to_pred_sha:", hits[:3])
print("labels_with_pred_sha_in_receipt:",ok,"/",len(labels))
'; echo "EXIT=$?"
# C15 exit 0 → golang/: go1.24.0.json go1.25.0.json; patchverdiffs/: go1.24.1 … go1.24.6 .json.diff
ls /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/ /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/ | grep -E 'go1\.2[45]|:$'; echo "EXIT=$?"
# C16 exit 0 → r17_ghidra_logs: 8; r17_fallback_pairs: [('1.25.14', '1.25.0'), ('1.25.8', '1.25.0')]
python3 -I -B -c '
import subprocess, re
REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
def git(*a):
    r=subprocess.run(["git"]+list(a),capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr.strip())
    return r.stdout
paths=[p for p in git("ls-tree","-r","--name-only","-z",REV,"--",".ufo/waves/round-17/runs/").split("\0") if p.endswith("ghidra.log")]
print("r17_ghidra_logs:",len(paths))
seen=set()
for p in sorted(paths):
    t=git("show",REV+":"+p)
    for m in re.findall(r"Falling back from (\S+) to (\S+)", t):
        seen.add((m[0],m[1]))
print("r17_fallback_pairs:",sorted(seen))
'; echo "EXIT=$?"
# C17 exit 0 → 2 hits at B, both source-derived: round-15/w1/PatchLookup.md:160, round-17/w1/ScoutGoDataInventory.md:140
git grep -nE 'Falling back from [0-9.]+ to [0-9]+\.[0-9]+\.[1-9]' $B -- . | sed -n '1,10p'; echo "EXIT_BASELINE=${PIPESTATUS[0]}"
# C18 exit 0 → hits only in SCORECARD.md and LOG.md (historical counts), none in SKILL/MINT/AGENTS/PROVINCE/QUALITY
R=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; for f in SKILL.md MINT.md AGENTS.md PROVINCE.md SCORECARD.md corpus/QUALITY.md LOG.md; do git show $R:$f | grep -nE 'Knowledge table|knowledge table|## Knowledge|Coverage map|coverage map|coverage-map' | cut -c1-260 | sed "s|^|$f:|" | sed -n '1,8p'; done; echo "EXIT=$?"
# C19 exit 0 → r17 :129 limit text; r17 diff B..R = 8 insertions (round-18 correction :200-206, no fallback line)
git diff --stat $B $R -- corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md; echo "EXIT=$?"
```

The fleet files `/home/vgpnk/Projects/shokunin/CORPUS.md:11,46` and `LEARNING.md:65` were read from the fleet worktree with the grep tool. They are not lane Git objects.

## Mistakes in my own checks (caught and fixed)

- My first receipt loop added the `runs/` prefix twice, so all 15 receipts came back "unreadable" (exit 2). The corrected loop C7 validates 15/15.
- My first index parser stripped the `knowledge/` prefix with `tok[11:]`, one character too many. That dropped every `knowledge/`-prefixed token and under-counted the coverage map at 61. C5 and C6 fix it, and recipe A agrees (96/96).

Tools installed or updated: none. Peer messages sent: none.
