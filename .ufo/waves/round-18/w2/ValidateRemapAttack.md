HOLDS
The remap validated only da64646 (pass-1) bytes and ran every check those receipts carry. I reproduced it independently, 8/8. I also found three fixable defects next to it: the gate does not bind the summary to its evidence, one lesson clause gives the wrong cause, and the summary under-retains QUALITY #18 fields. None of them changes the 8/8 result.

# ValidateRemapAttack: R17-VALIDATE16 remapped validation (round 18, wave 2, falsify)

Seat: `KaidokuR18.ValidateRemapAttack`. Critic, author-side advisory seat, leaf.
REV: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`.
Target: `REV:.ufo/waves/round-18/evidence/validate16/summary.json` plus its 16 stdout/stderr blobs. The worktree is clean for that directory (C2).
Validator: `9011581:.ufo/waves/round-17/tools/receipt-validate.py` (written `RV:` below). Its blob is `2762496…`, the same blob as at d0ab299. Its sha256 is `618448829b…`, which equals `summary.json` `validator_sha256` (C3).
Labels: **[O]** is an observation from a command, **[I]** is an inference. `C<n>` refers to the command appendix.

Axes:
- **Calibration:** is "8/8 exit 0, 341 checks" true of the pass-1 bytes?
- **Operability:** can the run be replayed from what was retained?
- **Depth:** the pass-2 leak surface and the skipped-check surface.

## Q1. Could the remap have validated pass-2 bytes? No.

- **[O] Independent replay.** In my own mkdtemp I built the tree from `git archive da64646 .ufo/waves/round-17` plus `da64646:.ufo/waves/round-16/selection.py`. I took `receipt-validate.py` and `pins.py` from 9011581. I remapped the prefix to `$T/tree`, a different target than w1 used.
  - pro-aether: exit 0, `checks_performed` 341, 0 findings (C10).
  - All 8: exit 0, 341, 0 findings. After path normalization, the stdout is byte-equal to the retained `<label>.stdout` for 8/8 (C16).
- **[O] Open trace (audit hook) of the pro-aether run (C11, C13):**
  - 0 opens under the live lane.
  - Outside the mkdtemp, the only opens were `/usr/bin/aether`, 143 Ghidra typeinfo files and the Python stdlib.
  - 0 write-mode opens.
  - [I] Pass-2 receipts and logs live in the lane worktree and in commits from d0ab299 on (C20), and no file from either location was opened, so no pass-2 bytes were read.
- **[O] Counter-tests.** I ran the same pass-1 receipt two more ways: remapped onto a d0ab299 tree (C14), and unremapped against the live lane (C15). Both exit 1 with 333 checks and the same 6 findings:
  - 4 `missing_file` on `runs/pro-aether/logs/rea-ghidra-JpGezV/{ghidra,script}.log`.
  - 1 `binding_mismatch`, with `logfile_ok`, `target_ok` and `md5_ok` all false.
  - 1 `sha256_mismatch` on `analyze.json`.
  - So the validator does tell the passes apart. [I] For these receipts, a pass-2 leak would show as exit 1 with `missing_file`/`sha256_mismatch`, not as exit 0.
- **[O] Fingerprint.** The 9011581 validator on the 8 pass-2 receipts (REV tree) gives 343–349 checks. Each count is 341 plus that receipt's mid-run `pin_checks` (2–8). No pass-2 receipt yields 341 (C24). The retained 341×8 is the pass-1 shape.
- **[O] w1's tmp dir still exists** (`/tmp/r17-validate16.MWZBce`, `summary.json:77`):
  - Its 259 round-17 files hash-equal the da64646 blobs, with 0 mismatches. The only extra file is `selection.py`, which equals the da64646 blob `62df54d` (C6).
  - Its 8 receipts reverse-remap byte-equal to the da64646 receipt blobs: 16 replacements each, 0 live prefixes left. None of them equals the REV pass-2 blob (C7).
  - Its `val/` files equal the 9011581 validator and pins blobs (C7).
  - Its `out/` files equal the 16 lane evidence files (C8).
- **[O] Timeline (C4, C23):**

  | Event | UTC |
  |---|---|
  | Pass-1 steps | 13:47:05Z–14:00:05Z |
  | da64646 committed | 14:06:06Z |
  | 95e34db committed | 14:27:35Z |
  | Pass-2 steps | 14:27:41Z–14:40:02Z |

  da64646 is an ancestor of 95e34db, so the archived tree predates pass 2.

## Q2. Did it skip checks? No, relative to what the pass-1 receipts commit to.

- **[O] 341 decomposes exactly** (pro-aether, C12):

  | Component | Checks |
  |---|---|
  | `check_required` | 30 |
  | `check_binding` | 5 |
  | `rerun_pins_compare` | 1 |
  | `pins_pre` | 0 |
  | `pins_post` (146 × sha+size) | 292 |
  | `walk_pairs` | 13 |
  | **Total** | **341** |

  `pins_pre` is 0 because all 146 of its keys are also in `pins_post`, and post is authoritative (`RV:267-269`). The 146 pinned files are 143 Ghidra typeinfo files, the carrier and 2 lane files (C9). The recomputed `pins_compare` is equal, so the pre digests equal the post digests.
- **[O] Every path commitment carries a digest.** Across the 8 receipts there are 72 commitments: 40 `path`+sha nodes and 32 `<stem>_path`+`<stem>_sha256` pairs. None lacks a digest, and no node has both forms (that case would skip the stem branch at `RV:294-314`) (C21).
- **[O] No silent skips:**
  - 0 pin entries with `error`, which is the silent skip at `RV:276-278` (C19).
  - The `md5_ok is not False` escape (`RV:173-177`) did not fire. Every carrier still hashes to its recorded sha256 (`RV:143-150`), and its full MD5 appears in the bound log's `Loading …?MD5=` line: `md5_ok=True` for 8/8 (C19).
- **[O] What pass-1 validation cannot cover.** The pass-1 receipts carry 0 mid-run `pin_checks` (8/8), so the 341 includes no mid-run drift check (C19).
  - REV's validator flags this only under `--require-mid-maps`: exit 1 with `mid_checks_absent`. By default it gives exit 0 and 341 (tested on 2 of the 8, C22).
  - This is not a skip: the checks do not exist in these receipts. No landed line claims otherwise (C32).
- **[O] Counting note (not a defect).** The 155 `verify_file` calls cover 152 distinct files (C12):
  - Both log files are verified twice, via `$.retained_logs` and via `$.steps.analyze.retained_logs`.
  - The carrier is verified twice, via pins and via `$.carrier`.
  - 288 of the 341 checks are host pin digests.
  - No SCORECARD/LOG/corpus/README/PROVINCE/SKILL line cites a 341 or 344 check figure (C30).
  - The w1 draft text `REV:.ufo/waves/round-18/w1/ScoutValidate16Sites.md:162` says "344 checks each" for pass 2. The measured counts are 343–349 (C24). The draft did not land.

## Defects next to the evidence (each fixable)

### D1. Calibration: the gate does not bind R17-VALIDATE16 to its evidence [O]

**Repro.** I made a mkdtemp clone at REV and removed its origin remote. There I replaced `summary.json` with `{rev, validator_sha256:"f"*64, receipts:[{label, exit:0}×8]}` and deleted all 16 stdout/stderr files (commit `75a1708`).

**Result.** `routed-defects.py --strict` still exits 0 with `open_count 0`. All 7 R17-VALIDATE16 checks pass, including `validator-sha256-pinned True validator_sha256='ffff…'` (C25–C28).

**Cause.**
- `REV:.ufo/waves/round-18/tools/routed-defects.py:458-462` checks only that the digest is 64 hex characters.
- No check reads the stdout blobs or the validator blob.
- The tool's own green fixture uses `"validator_sha256": "f" * 64` (`:945`).
- The docstring defines substance as "anchors, code, retained evidence" (`:9-10`), and this check does not meet that.
- So "substance check derives k/8 from the summary" (`REV:corpus/lessons/round-18.md:63`) only counts self-reported exits.

**Smallest correction.** Add one substance check to `_d_validate16`:
- sha256 of `git show <validator_rev>:.ufo/waves/round-17/tools/receipt-validate.py` must equal `validator_sha256`.
- For each entry, the blob `<label>.stdout` must exist at the revision, its sha256 must equal `stdout_sha256`, and it must parse with `exit` equal to the entry's exit and exactly one receipt.

The prototype passes at REV and fails at `75a1708`: the validator digest does not match and all 8 stdout blobs are absent (C29). Also replace the `"f"*64` fixture with real blobs and add the fabricated summary as a red selftest case.

### D2. Calibration: the lesson line gives the wrong cause [O]

`REV:corpus/lessons/round-18.md:52` says the in-place replay "is red 8/8 because pass 2 replaced the logs at the same paths (w1 `RevValidatorPaths.md`)".

"Red 8/8" is right (C18). The cause is wrong:
- For 8/8 receipts, the pass-1 and pass-2 log directories have different session names (for example `JpGezV` vs `J5bcRT`).
- The in-place findings are 32 `missing_file` on log paths, 8 `binding_mismatch` that follow from them, and 1 `sha256_mismatch` on `pro-aether/analyze.json`.
- 0 log paths hold changed bytes.
- `git diff --name-status da64646 d0ab299 -- .ufo/waves/round-17/runs/` shows 16 D and 16 A (the log files) plus 27 M (C20).
- The cited source says "the pass-1 `logs/` directories were deleted" (`REV:.ufo/waves/round-18/w1/RevValidatorPaths.md:103-104`).

**Correction.** Replace the clause with: "…red 8/8 because pass 2 deleted the pass-1 `logs/rea-ghidra-*` directories (its logs carry new session names): 32/32 retained-log paths `missing_file`, plus `pro-aether/analyze.json` `sha256_mismatch`". If the lesson is already append-only, append this as a correction.

### D3. Operability / QUALITY #18: the summary under-retains the execution

`REV:corpus/QUALITY.md:28` requires "the producing argv/snippet, measured revision, stdout/stderr and exit".

What the summary has [O]:
- Per-receipt keys: `{checks_performed, exit, findings, kind, label, stdout_sha256}` (`summary.json:3-10`).

What it lacks [O]:
- argv, cwd, timestamps, `stderr_sha256`, the remap snippet and receipt blob ids.
- `remap.to` points at a tmp dir (`summary.json:77`).

The lane already has a convention that would cover this, and it was not reused [O]. The r17 `verification.json` command records carry `argv, cwd, started_at_utc, ended_at_utc, env_overrides, exit, expected_exit, stdout/stderr path+sha256` (C31).

[I] The impact is low today: the prose at `summary.json:76-78` was enough for my replay (C10, C16).

**Correction.** Add those keys to each entry, plus `receipt_blob` (the da64646 ls-tree oid) and `remapped_sha256`, and add the one-line remap snippet.

## Tradeoffs, not defects

- **Live host bytes.** Carriers and Ghidra files are checked against the bytes present now; that is the validator's stated limitation (`RV:34-37`). For lane files the remap narrows this to immutable da64646 blobs.
- **Unscoped verdict.** `LOG.md:2159` and `SCORECARD.md:2439` state only "validate 8/8 exit 0". Under QUALITY #21 (`REV:corpus/QUALITY.md:31`), a scope clause would be stricter. It would name the recomputed fields: 146 pin digests and sizes, 6 run files, the log binding with live MD5, and `pins_compare`, and note that pass-1 has no mid-run checks. This is optional.

## Impacted axes and verdict basis

- Calibration: D1 and D2.
- Operability: D3.
- Depth: not harmed. Q1 and Q2 hold, so the canonical judge has no reason to reject the 8/8 result.

## Hygiene, installs, tools

- **Lane access.** Read-only git only: rev-parse, ls-tree, status, show, log, merge-base, archive, diff, grep, and clone as a source.
  - [O] `.git/index` mtime is 13:38:12 -0300.
  - [I] That is before my first command, so my one `git status` did not rewrite it.
- **Scratch dir.** mkdtemp `/tmp/kr18-vra.72rnp3d2` held `tree/`, `tree2/` (d0ab299), `treerev/` (REV), `val/`, `valrev/`, `receipts/`, `out/` and `clone/`. The clone's origin was removed before its one commit (`75a1708`, the fabricated fixture). I removed the whole dir after writing this report.
- **w1's dir.** `/tmp/r17-validate16.MWZBce` was read only.
- **Not run.** No REA, no Ghidra. No carrier was executed: the validator only hashed the carriers, opening them with mode `r`.
- **Installs.** None.
- **Tools.** git 2.56.0, Python 3.14.8 (`python3 -I -B`), GNU tar 1.35 (C33).

## Command appendix (verbatim, run order; key output; exit)

C1 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git rev-parse HEAD da64646 2>&1; echo "EXIT=$?"` → `b2aad08c…`, `da64646adcb19c1ede7537b799b8c7d283fe43da`; EXIT=0

C2 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git ls-tree -r --long b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/evidence/validate16/ 2>&1; echo "EXIT=$?"; git status --porcelain=v1 -- .ufo/waves/round-18/evidence/ 2>&1; echo "EXIT=$?"` → 17 blobs (8 stderr = empty blob `e69de29`); status empty; EXIT=0, EXIT=0

C3 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && for r in da64646 d0ab299 9011581 b2aad08ceeee8dd125ce0d316056d8bd766c7f94; do printf '%s ' "$r"; git rev-parse "$r:.ufo/waves/round-17/tools/receipt-validate.py" 2>&1; printf '  pins: '; git rev-parse "$r:.ufo/waves/round-17/tools/pins.py" 2>&1; done; echo "EXIT=$?"; git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum; echo "EXIT=${PIPESTATUS[0]}"` → validator d0ab299=9011581=`2762496c…`, REV `bf043886…`, da64646 `8e2f6d27…`; pins `6568a493…` at all four; sha256 `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`; EXIT=0, EXIT=0

C4 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git log -1 --format='%H %cI %s' da64646; git log -1 --format='%H %cI %s' 95e34db; git log -1 --format='%H %cI %s' d0ab299; git merge-base --is-ancestor da64646 95e34db; echo "da64646<95e34db EXIT=$?"; git merge-base --is-ancestor 95e34db d0ab299; echo "95e34db<d0ab299 EXIT=$?"; git merge-base --is-ancestor d0ab299 b2aad08ceeee8dd125ce0d316056d8bd766c7f94; echo "d0ab299<REV EXIT=$?"` → 2026-10-20T11:06:06-03:00 / 11:27:35-03:00 / 11:47:24-03:00; all three EXIT=0

C5
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show da64646:.ufo/waves/round-17/runs/pro-aether/receipt.json | python3 -I -B -c '
import json,sys
raw=sys.stdin.read()
P="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
print("prefix_occurrences", raw.count(P))
print("kaidoku-shokunin occurrences", raw.count("kaidoku-shokunin"))
print("escaped-slash occurrences", raw.count("\\/"))
d=json.loads(raw)
print("top keys", sorted(d.keys()))
def walk(n,w):
    if isinstance(n,dict):
        for k,v in n.items():
            if k in ("pins_pre","pins_post"): 
                continue
            walk(v,w+"."+k)
    elif isinstance(n,list):
        for i,v in enumerate(n): walk(v,"%s[%d]"%(w,i))
    elif isinstance(n,str):
        if "/" in n and len(n)<400:
            print(w, "=", n[:200])
walk(d,"$")
'; echo "EXIT=$?"
```
→ prefix 16, kaidoku-shokunin 16, escaped 0; steps `analyze`, `inspect-go-binary`; bound `/tmp/kr17-rea-0o3ukbw2/rea-ghidra-JpGezV`; EXIT=0

C6
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,os
W="/tmp/r17-validate16.MWZBce"
ls=subprocess.run(["git","ls-tree","-r","da64646",".ufo/waves/round-17"],capture_output=True,text=True,check=True).stdout.splitlines()
tree={}
for ln in ls:
    meta,path=ln.split("\t",1); mode,typ,oid=meta.split()
    tree[path]=(mode,oid)
paths=sorted(tree)
res=subprocess.run(["git","hash-object","--no-filters","--stdin-paths"],input="\n".join(W+"/"+p for p in paths)+"\n",capture_output=True,text=True,check=True).stdout.split()
diff=[p for p,h in zip(paths,res) if h!=tree[p][1]]
extra=[]
for root,dirs,files in os.walk(W+"/.ufo"):
    for f in files:
        rel=os.path.relpath(os.path.join(root,f),W)
        if rel not in tree: extra.append(rel)
sel=subprocess.run(["git","rev-parse","da64646:.ufo/waves/round-16/selection.py"],capture_output=True,text=True,check=True).stdout.strip()
selh=subprocess.run(["git","hash-object","--no-filters",W+"/.ufo/waves/round-16/selection.py"],capture_output=True,text=True,check=True).stdout.strip()
print("da64646 round-17 blobs", len(paths), "content mismatches", len(diff), diff[:5])
print("extra files in tmp tree", extra)
print("selection.py tmp==da64646 blob", selh==sel, sel)
'; echo "EXIT=$?"
```
→ `da64646 round-17 blobs 259 content mismatches 0 []`; extra `['.ufo/waves/round-16/selection.py']`; `selection.py tmp==da64646 blob True 62df54d5…`; EXIT=0

C7
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,hashlib,os
P="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W="/tmp/r17-validate16.MWZBce"
labels=sorted(l.split("/")[-1] for l in subprocess.run(["git","ls-tree","--name-only","da64646",".ufo/waves/round-17/runs/"],capture_output=True,text=True,check=True).stdout.split() if not l.endswith(".txt"))
print(labels)
for l in labels:
    blob=subprocess.run(["git","show",f"da64646:.ufo/waves/round-17/runs/{l}/receipt.json"],capture_output=True,check=True).stdout
    tmp=open(f"{W}/receipts/{l}.json","rb").read()
    back=tmp.replace(W.encode(),P.encode())
    n_orig=blob.count(P.encode()); n_tmp=tmp.count(W.encode()); n_live=tmp.count(P.encode())
    rev=subprocess.run(["git","show",f"b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-17/runs/{l}/receipt.json"],capture_output=True,check=True).stdout
    print(l, "orig_prefix", n_orig, "tmp_prefix", n_tmp, "live_prefix_left", n_live, "reverse_remap_equals_da64646_blob", back==blob, "blob_equals_REV_pass2", blob==rev, "len_delta", len(tmp)-len(blob))
'; echo "EXIT=$?"; for f in receipt-validate.py pins.py; do sha256sum /tmp/r17-validate16.MWZBce/val/$f; git show 9011581:.ufo/waves/round-17/tools/$f | sha256sum; done; echo "EXIT=$?"
```
→ 8× `orig_prefix 16 tmp_prefix 16 live_prefix_left 0 reverse_remap_equals_da64646_blob True blob_equals_REV_pass2 False`; val/ `618448829b…`=`618448829b…`, `9e9c7250…`=`9e9c7250…`; EXIT=0, EXIT=0

C8 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/evidence/validate16 && for f in *.stdout *.stderr; do cmp -s "$f" "/tmp/r17-validate16.MWZBce/out/$f" && echo "same $f" || echo "DIFF $f"; done; sha256sum *.stdout; echo "EXIT=$?"` → `same` ×16; stdout sha256 values equal `summary.json` `stdout_sha256` ×8; EXIT=0

C9
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show da64646:.ufo/waves/round-17/runs/pro-aether/receipt.json | python3 -I -B -c '
import json,sys,collections
d=json.load(sys.stdin)
P="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
for snap in ("pins_pre","pins_post"):
    e=d[snap].get("entries",{})
    lane=[k for k in e if k.startswith(P)]
    rel=[k for k in e if not k.startswith("/")]
    err=[k for k,v in e.items() if isinstance(v,dict) and "error" in v]
    nosize=[k for k,v in e.items() if isinstance(v,dict) and "size" not in v]
    print(snap, "entries", len(e), "lane", lane, "relative", rel, "error_entries", err, "no_size", len(nosize))
    print("  snapshot keys", sorted(d[snap].keys()))
pre=set(d["pins_pre"]["entries"]); post=set(d["pins_post"]["entries"])
print("pre-only", sorted(pre-post), "post-only", sorted(post-pre))
print("pins_compare", {k:v for k,v in d["pins_compare"].items()})
print("steps", list(d["steps"].keys()))
for n,s in d["steps"].items():
    print(n, sorted(s.keys()), "pin_checks", len(s.get("pin_checks") or []), "started", s.get("started_at_utc"), "ended", s.get("ended_at_utc"))
print("bound", d["bound_sessions"], "unbound", d.get("unbound_sessions"))
print("carrier", {k:v for k,v in d["carrier"].items()})
print("retained_logs", json.dumps(d["retained_logs"])[:600])
'; echo "EXIT=$?"
```
→ pins_pre/post 146 entries each, lane pins = `round-16/selection.py` and `round-17/predictions/pro-aether.prediction.json`, 0 relative, 0 error, pre-only/post-only empty; pin_checks 0 for both steps; EXIT=0

C10 (independent reproduction; this command created the mkdtemp)
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,tempfile,os,json,hashlib,sys
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T=tempfile.mkdtemp(prefix="kr18-vra.")
print("T", T)
def sh(args, **kw):
    r=subprocess.run(args, capture_output=True, **kw); return r
for d in ("tree","val","receipts","out"): os.makedirs(f"{T}/{d}")
a=subprocess.Popen(["git","-C",L,"archive","da64646",".ufo/waves/round-17"],stdout=subprocess.PIPE)
x=subprocess.run(["tar","-x","-C",f"{T}/tree"],stdin=a.stdout); a.stdout.close(); print("archive|tar exits", a.wait(), x.returncode)
os.makedirs(f"{T}/tree/.ufo/waves/round-16")
open(f"{T}/tree/.ufo/waves/round-16/selection.py","wb").write(sh(["git","-C",L,"show","da64646:.ufo/waves/round-16/selection.py"],check=True).stdout)
for f in ("receipt-validate.py","pins.py"):
    open(f"{T}/val/{f}","wb").write(sh(["git","-C",L,"show",f"9011581:.ufo/waves/round-17/tools/{f}"],check=True).stdout)
print("validator sha256", hashlib.sha256(open(f"{T}/val/receipt-validate.py","rb").read()).hexdigest())
lab="pro-aether"
blob=sh(["git","-C",L,"show",f"da64646:.ufo/waves/round-17/runs/{lab}/receipt.json"],check=True).stdout
new=blob.replace(L.encode(), (T+"/tree").encode())
print("replacements", blob.count(L.encode()), "left", new.count(L.encode()))
open(f"{T}/receipts/{lab}.json","wb").write(new)
r=sh(["python3","-I","-B",f"{T}/val/receipt-validate.py",f"{T}/receipts/{lab}.json"])
open(f"{T}/out/{lab}.stdout","wb").write(r.stdout); open(f"{T}/out/{lab}.stderr","wb").write(r.stderr)
print("validator exit", r.returncode, "stderr bytes", len(r.stderr))
mine=json.loads(r.stdout)
ret=json.loads(open(f"{L}/.ufo/waves/round-18/evidence/validate16/{lab}.stdout").read())
print(json.dumps(mine["receipts"][0], sort_keys=True))
def norm(s,root): return s.replace(root,"<ROOT>")
m=norm(r.stdout.decode(), T+"/tree").replace(T,"<ROOT>")
w=norm(json.dumps(ret,sort_keys=True,indent=2)+"\n","/tmp/r17-validate16.MWZBce")
print("normalized stdout equal to retained:", m==w)
' ; echo "EXIT=$?"
```
→ `T /tmp/kr18-vra.72rnp3d2`; `archive|tar exits 0 0`; validator sha256 `618448829b…`; `replacements 16 left 0`; `validator exit 0 stderr bytes 0`; `{"checks_performed": 341, "findings": [], "kind": "carrier", … "status": "valid", "valid": true}`; `normalized stdout equal to retained: True`; EXIT=0

C11
```
cd /tmp/kr18-vra.72rnp3d2 && python3 -I -B -c '
import sys,runpy,io,json,collections,contextlib
T="/tmp/kr18-vra.72rnp3d2"
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
opened=[]
def hook(ev,args):
    if ev=="open":
        p=args[0]
        if isinstance(p,(str,bytes)): opened.append((p if isinstance(p,str) else p.decode(), args[1]))
sys.addaudithook(hook)
sys.argv=[T+"/val/receipt-validate.py", T+"/receipts/pro-aether.json"]
buf=io.StringIO(); code=None
with contextlib.redirect_stdout(buf):
    try: runpy.run_path(T+"/val/receipt-validate.py", run_name="__main__")
    except SystemExit as e: code=e.code
out=json.loads(buf.getvalue())
print("exit", code, "checks", out["receipts"][0]["checks_performed"], "findings", len(out["receipts"][0]["findings"]))
cls=collections.Counter(); lane=[]; other=set()
for p,m in opened:
    if p.startswith(T): cls["under_mkdtemp"]+=1
    elif p.startswith(L): cls["under_live_lane"]+=1; lane.append(p)
    elif p.startswith("/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/"): cls["ghidra_install"]+=1
    else: cls["other"]+=1; other.add((p,str(m)))
print("open events", len(opened), dict(cls))
print("live lane opens", lane)
print("other opens", sorted(other))
print("distinct mkdtemp files opened", sorted({p.replace(T,"<T>") for p,m in opened if p.startswith(T)}))
print("write-mode opens", [(p,m) for p,m in opened if any(c in str(m) for c in "wax+")])
'; echo "EXIT=$?"
```
→ `exit 0 checks 341 findings 0`; `open events 246 {'other': 86, 'under_mkdtemp': 17, 'ghidra_install': 143}`; `live lane opens []`; `write-mode opens []`; EXIT=0

C12
```
cd /tmp/kr18-vra.72rnp3d2 && python3 -I -B -c '
import importlib.util,json,hashlib,collections,re
T="/tmp/kr18-vra.72rnp3d2"
spec=importlib.util.spec_from_file_location("rv",T+"/val/receipt-validate.py"); rv=importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
pins=rv.load_pins()
rec=json.load(open(T+"/receipts/pro-aether.json"))
calls=[]
orig=rv.verify_file
def vf(path,sha,findings,where,expected_size=None):
    n=orig(path,sha,findings,where,expected_size); calls.append((where,path,n)); return n
rv.verify_file=vf
parts={}
for name,fn in (("check_required",lambda f: rv.check_required(rec,"carrier",f)),("check_binding",lambda f: rv.check_binding(rec,f)),("rerun_pins_compare",lambda f: rv.rerun_pins_compare(rec,pins,f)),("pins_pre",lambda f: rv.verify_pin_entries(rec["pins_pre"],rec["pins_post"],"pins_pre",f)),("pins_post",lambda f: rv.verify_pin_entries(rec["pins_post"],None,"pins_post",f)),("walk_pairs",lambda f: rv.walk_pairs(rec,f,"$",set()))):
    f=[]; parts[name]=(fn(f),len(f))
print(parts, "total", sum(v[0] for v in parts.values()))
walk=[(w,p.replace(T,"<T>"),n) for w,p,n in calls if not w.startswith("pins_")]
for c in walk: print("walk", c)
paths=[p for w,p,n in calls]
print("verify_file calls", len(calls), "distinct paths", len(set(paths)), "dup paths", sorted({p.replace(T,"<T>") for p in paths if paths.count(p)>1}))
# md5 binding reproduced independently
car=rec["carrier"]; sha=car["sha256_post"]; d=rec["bound_sessions"][0]
md5=hashlib.md5(open(car["path"],"rb").read()).hexdigest()
log=open(rec["retained_logs"][0]["files"]["ghidra.log"]["path"],"rb").read().decode("utf-8","replace").split("\n")
print("carrier sha now==recorded", hashlib.sha256(open(car["path"],"rb").read()).hexdigest()==sha)
print("md5_ok", any(l.startswith(f"Loading file://{d}/target-{sha[:12]}.bin?MD5={md5}") for l in log), "logfile_ok", any(re.fullmatch(r"\S+ \S+ INFO +\(LoggingInitialization\) Using log file: "+re.escape(d+"/ghidra.log"), l.rstrip()) for l in log), "target_ok", any(re.fullmatch(r"\S+ \S+ INFO +\(HeadlessAnalyzer\) IMPORTING: "+re.escape(f"file://{d}/target-{sha[:12]}.bin"), l.rstrip()) for l in log))
print("pin_checks per step", {k:len(v.get("pin_checks") or []) for k,v in rec["steps"].items()})
'; echo "EXIT=$?"
```
→ `{'check_required': (30, 0), 'check_binding': (5, 0), 'rerun_pins_compare': (1, 0), 'pins_pre': (0, 0), 'pins_post': (292, 0), 'walk_pairs': (13, 0)} total 341`; `verify_file calls 155 distinct paths 152`; `md5_ok True logfile_ok True target_ok True`; `pin_checks per step {'analyze': 0, 'inspect-go-binary': 0}`; EXIT=0

C13
```
cd /tmp/kr18-vra.72rnp3d2 && python3 -I -B -c '
import sys,runpy,io,contextlib
T="/tmp/kr18-vra.72rnp3d2"
opened=[]
sys.addaudithook(lambda ev,a: opened.append(a[0]) if ev=="open" and isinstance(a[0],str) else None)
sys.argv=[T+"/val/receipt-validate.py", T+"/receipts/pro-aether.json"]
with contextlib.redirect_stdout(io.StringIO()):
    try: runpy.run_path(T+"/val/receipt-validate.py", run_name="__main__")
    except SystemExit: pass
print(sorted({p for p in opened if not p.startswith("/usr/lib/python3") and not p.startswith("/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/") and not p.startswith(T)}))
'; echo "EXIT=$?"; ls -la /tmp/kr18-vra.72rnp3d2/val; echo "EXIT=$?"
```
→ `['/usr/bin/aether']`; `val/` holds only `pins.py`, `receipt-validate.py` (no `__pycache__`); EXIT=0, EXIT=0

C14
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,os,json,collections
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"
R2=T+"/tree2"; os.makedirs(R2)
a=subprocess.Popen(["git","-C",L,"archive","d0ab299",".ufo/waves/round-17"],stdout=subprocess.PIPE)
x=subprocess.run(["tar","-x","-C",R2],stdin=a.stdout); a.stdout.close(); print("archive d0ab299|tar exits", a.wait(), x.returncode)
os.makedirs(R2+"/.ufo/waves/round-16")
open(R2+"/.ufo/waves/round-16/selection.py","wb").write(subprocess.run(["git","-C",L,"show","d0ab299:.ufo/waves/round-16/selection.py"],capture_output=True,check=True).stdout)
print("pass-2 logs dir for pro-aether at d0ab299:", sorted(os.listdir(R2+"/.ufo/waves/round-17/runs/pro-aether/logs")))
blob=subprocess.run(["git","-C",L,"show","da64646:.ufo/waves/round-17/runs/pro-aether/receipt.json"],capture_output=True,check=True).stdout
open(T+"/receipts/pro-aether.pass2tree.json","wb").write(blob.replace(L.encode(),R2.encode()))
r=subprocess.run(["python3","-I","-B",T+"/val/receipt-validate.py",T+"/receipts/pro-aether.pass2tree.json"],capture_output=True)
o=json.loads(r.stdout)["receipts"][0]
print("exit", r.returncode, "status", o["status"], "checks", o["checks_performed"], "findings", len(o["findings"]))
print(collections.Counter((f["code"],f["where"].split(".entries.")[0]) for f in o["findings"]))
for f in o["findings"]: print({k:(v.replace(R2,"<R2>") if isinstance(v,str) else v) for k,v in f.items() if k in ("code","where","path","logfile_ok","target_ok","md5_ok")})
'; echo "EXIT=$?"
```
→ pass-2 logs `['rea-ghidra-J5bcRT']`; `exit 1 status invalid checks 333 findings 6`: binding_mismatch (logfile/target/md5 False), 4× missing_file `rea-ghidra-JpGezV/*`, sha256_mismatch `$.steps.analyze.stdout`; EXIT=0

C15
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json,collections
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"
blob=subprocess.run(["git","-C",L,"show","da64646:.ufo/waves/round-17/runs/pro-aether/receipt.json"],capture_output=True,check=True).stdout
open(T+"/receipts/pro-aether.unremapped.json","wb").write(blob)
r=subprocess.run(["python3","-I","-B",T+"/val/receipt-validate.py",T+"/receipts/pro-aether.unremapped.json"],capture_output=True)
o=json.loads(r.stdout)["receipts"][0]
print("exit", r.returncode, "status", o["status"], "checks", o["checks_performed"], "findings", len(o["findings"]))
for f in o["findings"]: print({k:(v.replace(L,"<LANE>") if isinstance(v,str) else v) for k,v in f.items() if k in ("code","where","path","logfile_ok","target_ok","md5_ok")})
'; echo "EXIT=$?"; ls /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/pro-aether/logs/; echo "EXIT=$?"
```
→ `exit 1 status invalid checks 333 findings 6` (same six as C14, `<LANE>` paths); live logs dir `rea-ghidra-J5bcRT`; EXIT=0, EXIT=0

C16
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"; W="/tmp/r17-validate16.MWZBce"
labs=["calib-esbuild-0.25.12","calib-shfmt","pro-aether","pro-containerd-shim","pro-esbuild-0.21.5","pro-esbuild-0.27.7","pro-notesmd-cli","pro-op"]
for lab in labs:
    blob=subprocess.run(["git","-C",L,"show",f"da64646:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout
    p=f"{T}/receipts/all8-{lab}.json"; open(p,"wb").write(blob.replace(L.encode(),(T+"/tree").encode()))
    r=subprocess.run(["python3","-I","-B",T+"/val/receipt-validate.py",p],capture_output=True)
    o=json.loads(r.stdout)
    mine=json.dumps(o,sort_keys=True,indent=2).replace(T+"/tree","<R>").replace(p,"<RECEIPT>").replace(T+"/val","<V>")
    ret=json.loads(open(f"{L}/.ufo/waves/round-18/evidence/validate16/{lab}.stdout").read())
    theirs=json.dumps(ret,sort_keys=True,indent=2).replace(W+f"/receipts/{lab}.json","<RECEIPT>").replace(W+"/val","<V>").replace(W,"<R>")
    rr=o["receipts"][0]
    print(lab, "exit", r.returncode, "stderr", len(r.stderr), "checks", rr["checks_performed"], "findings", len(rr["findings"]), "normalized==retained", mine==theirs)
'; echo "EXIT=$?"
```
→ 8× `exit 0 stderr 0 checks 341 findings 0 normalized==retained True`; EXIT=0

C17 (pass-2 decomposition; builds `treerev/` from `git archive REV .ufo/waves/round-17` + REV `selection.py`, same pattern as C14, then the C12 per-function split on REV receipts) → `pro-aether pass-2 exit 0 checks 344 … check_binding 8 … pin_checks {'analyze': 3 …}`, `calib-shfmt pass-2 exit 0 checks 343 … check_binding 7 … pin_checks {'analyze': 2 …}`; EXIT=0. Verbatim:
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,os,json,importlib.util
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"; REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
R3=T+"/treerev"; os.makedirs(R3)
a=subprocess.Popen(["git","-C",L,"archive",REV,".ufo/waves/round-17"],stdout=subprocess.PIPE)
x=subprocess.run(["tar","-x","-C",R3],stdin=a.stdout); a.stdout.close(); print("archive REV|tar", a.wait(), x.returncode)
os.makedirs(R3+"/.ufo/waves/round-16")
open(R3+"/.ufo/waves/round-16/selection.py","wb").write(subprocess.run(["git","-C",L,"show",REV+":.ufo/waves/round-16/selection.py"],capture_output=True,check=True).stdout)
spec=importlib.util.spec_from_file_location("rv",T+"/val/receipt-validate.py"); rv=importlib.util.module_from_spec(spec); spec.loader.exec_module(rv); pins=rv.load_pins()
for lab in ("pro-aether","calib-shfmt"):
    blob=subprocess.run(["git","-C",L,"show",f"{REV}:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout
    p=f"{T}/receipts/pass2-{lab}.json"; open(p,"wb").write(blob.replace(L.encode(),R3.encode()))
    r=subprocess.run(["python3","-I","-B",T+"/val/receipt-validate.py",p],capture_output=True)
    o=json.loads(r.stdout)["receipts"][0]
    rec=json.loads(blob.replace(L.encode(),R3.encode()))
    parts={}
    for name,fn in (("check_required",lambda f: rv.check_required(rec,"carrier",f)),("check_binding",lambda f: rv.check_binding(rec,f)),("rerun_pins_compare",lambda f: rv.rerun_pins_compare(rec,pins,f)),("pins_pre",lambda f: rv.verify_pin_entries(rec["pins_pre"],rec["pins_post"],"pins_pre",f)),("pins_post",lambda f: rv.verify_pin_entries(rec["pins_post"],None,"pins_post",f)),("walk_pairs",lambda f: rv.walk_pairs(rec,f,"$",set()))):
        f=[]; parts[name]=fn(f)
    print(lab, "pass-2 exit", r.returncode, "checks", o["checks_performed"], "findings", len(o["findings"]), parts, "prefix count", blob.count(L.encode()), "pin_checks", {k:len(v.get("pin_checks") or []) for k,v in rec["steps"].items()}, "carrier keys", sorted(rec["carrier"].keys()))
'; echo "EXIT=$?"
```

C18
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json,collections,os,hashlib
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"; R3=T+"/treerev"
labs=["calib-esbuild-0.25.12","calib-shfmt","pro-aether","pro-containerd-shim","pro-esbuild-0.21.5","pro-esbuild-0.27.7","pro-notesmd-cli","pro-op"]
red_live=red_rev=0; agg=collections.Counter()
for lab in labs:
    blob=subprocess.run(["git","-C",L,"show",f"da64646:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout
    rec=json.loads(blob)
    logdir_p1=sorted(os.path.basename(e["session_dir"]) for e in rec["retained_logs"])
    p2=json.loads(subprocess.run(["git","-C",L,"show",f"b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout)
    logdir_p2=sorted(os.path.basename(e["session_dir"]) for e in p2["retained_logs"])
    res={}
    for tag,base in (("live",L),("revtree",R3)):
        p=f"{T}/receipts/inplace-{tag}-{lab}.json"; open(p,"wb").write(blob.replace(L.encode(),base.encode()))
        r=subprocess.run(["python3","-I","-B",T+"/val/receipt-validate.py",p],capture_output=True)
        o=json.loads(r.stdout)["receipts"][0]
        cnt=collections.Counter((f["code"], "log" if "/logs/" in (f.get("path") or "") else os.path.basename(f.get("path") or f["where"])) for f in o["findings"])
        res[tag]=(r.returncode,o["checks_performed"],dict(cnt))
        if tag=="live": red_live+= r.returncode!=0
        else: red_rev+= r.returncode!=0; agg.update(cnt)
    print(lab, "p1_logdirs", logdir_p1, "p2_logdirs", logdir_p2, "same_name", logdir_p1==logdir_p2, res["live"]==res["revtree"], res["revtree"])
print("in-place red live", red_live, "/8; red REV-tree", red_rev, "/8"); print("aggregate REV-tree findings", dict(agg))
'; echo "EXIT=$?"
```
→ 8× `same_name False`, live==REV-tree True; `in-place red live 8 /8; red REV-tree 8 /8`; `aggregate REV-tree findings {('binding_mismatch', 'log'): 8, ('missing_file', 'log'): 32, ('sha256_mismatch', 'analyze.json'): 1}`; EXIT=0

C19
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json,hashlib,re
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"
labs=["calib-esbuild-0.25.12","calib-shfmt","pro-aether","pro-containerd-shim","pro-esbuild-0.21.5","pro-esbuild-0.27.7","pro-notesmd-cli","pro-op"]
for lab in labs:
    rec=json.loads(subprocess.run(["git","-C",L,"show",f"da64646:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout.replace(L.encode(),(T+"/tree").encode()))
    car=rec["carrier"]; sha=car.get("sha256_post") or car.get("sha256"); data=open(car["path"],"rb").read()
    md5=hashlib.md5(data).hexdigest(); shaok=hashlib.sha256(data).hexdigest()==sha
    by={e["session_dir"]:e for e in rec["retained_logs"]}
    oks=[]
    for d in rec["bound_sessions"]:
        lines=[l.rstrip() for l in open(by[d]["files"]["ghidra.log"]["path"],"rb").read().decode("utf-8","replace").split("\n")]
        oks.append(any(l.startswith(f"Loading file://{d}/target-{sha[:12]}.bin?MD5={md5}") for l in lines))
    errs=sum(1 for s in ("pins_pre","pins_post") for v in rec[s]["entries"].values() if "error" in v)
    pc=sum(len(s.get("pin_checks") or []) for s in rec["steps"].values())
    print(lab, "carrier", car["path"], "sha_now_ok", shaok, "bound", len(rec["bound_sessions"]), "unbound", len(rec.get("unbound_sessions") or []), "md5_ok", oks, "pin_error_entries", errs, "pins", len(rec["pins_post"]["entries"]), "mid_run_pin_checks", pc, "md5_pre_field", "md5_pre" in car, "steps_started", sorted(s["started_at_utc"] for s in rec["steps"].values())[0])
'; echo "EXIT=$?"
```
→ 8× `sha_now_ok True bound 1 unbound 0 md5_ok [True] pin_error_entries 0 pins 146 mid_run_pin_checks 0 md5_pre_field False`; EXIT=0

C20 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git diff --no-renames --name-status da64646 d0ab299 -- .ufo/waves/round-17/runs/pro-aether/ 2>&1; echo "EXIT=$?"; git diff --no-renames --name-status da64646 d0ab299 -- .ufo/waves/round-17/runs/ | cut -f1 | sort | uniq -c; echo "EXIT=${PIPESTATUS[0]}"; du -sh .git 2>&1; echo "EXIT=$?"` → pro-aether: `A …/rea-ghidra-J5bcRT/{ghidra,script}.log`, `D …/rea-ghidra-JpGezV/{ghidra,script}.log`, `M analyze.json, carrier-run.stdout, observation.json, receipt.json`; runs/: `16 A, 16 D, 27 M`; `.git` 42M; EXIT=0 ×3

C21
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
labs=["calib-esbuild-0.25.12","calib-shfmt","pro-aether","pro-containerd-shim","pro-esbuild-0.21.5","pro-esbuild-0.27.7","pro-notesmd-cli","pro-op"]
SHA=("sha256_post","sha256","sha256_pre")
tot={"path_with_sha":0,"path_no_sha":0,"stem_path_with_sha":0,"stem_path_no_sha":0,"path_and_stem_path_same_node":0}
nos=set()
for lab in labs:
    rec=json.loads(subprocess.run(["git","-C",L,"show",f"da64646:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout)
    def walk(n,w):
        if isinstance(n,dict):
            if isinstance(n.get("path"),str):
                ok=any(isinstance(n.get(k),str) and len(n[k])==64 for k in SHA)
                tot["path_with_sha" if ok else "path_no_sha"]+=1
                if not ok: nos.add(w)
                if any(k.endswith("_path") for k in n): tot["path_and_stem_path_same_node"]+=1
            else:
                for k,v in n.items():
                    if isinstance(k,str) and k.endswith("_path"):
                        ok=isinstance(n.get(k[:-5]+"_sha256"),str)
                        tot["stem_path_with_sha" if ok else "stem_path_no_sha"]+=1
                        if not ok: nos.add(w+"."+k)
            for k,v in n.items():
                if k in ("pins_pre","pins_post"): continue
                walk(v,w+"."+k)
        elif isinstance(n,list):
            for i,v in enumerate(n): walk(v,"%s[%d]"%(w,i))
    walk(rec,"$")
print(tot); print("unverified path commitments", sorted(nos))
'; echo "EXIT=$?"
```
→ `{'path_with_sha': 40, 'path_no_sha': 0, 'stem_path_with_sha': 32, 'stem_path_no_sha': 0, 'path_and_stem_path_same_node': 0}`; `unverified path commitments []`; EXIT=0

C22
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json,os
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"; REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
V=T+"/valrev"; os.makedirs(V)
for f in ("receipt-validate.py","pins.py"):
    open(f"{V}/{f}","wb").write(subprocess.run(["git","-C",L,"show",f"{REV}:.ufo/waves/round-17/tools/{f}"],capture_output=True,check=True).stdout)
for lab in ("pro-aether","calib-shfmt"):
    p=f"{T}/receipts/all8-{lab}.json"
    for extra in ([],["--require-mid-maps"]):
        r=subprocess.run(["python3","-I","-B",V+"/receipt-validate.py",*extra,p],capture_output=True)
        o=json.loads(r.stdout)["receipts"][0]
        print(lab, "REV validator", extra or "(default)", "exit", r.returncode, "checks", o["checks_performed"], "codes", sorted({f["code"] for f in o["findings"]}))
'; echo "EXIT=$?"
```
→ both labels: default `exit 0 checks 341 codes []`; `--require-mid-maps` `exit 1 checks 342 codes ['mid_checks_absent']`; EXIT=0

C23
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
labs=["calib-esbuild-0.25.12","calib-shfmt","pro-aether","pro-containerd-shim","pro-esbuild-0.21.5","pro-esbuild-0.27.7","pro-notesmd-cli","pro-op"]
for rev in ("da64646","d0ab299"):
    ts=[]
    for lab in labs:
        rec=json.loads(subprocess.run(["git","-C",L,"show",f"{rev}:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout)
        for s in rec["steps"].values(): ts+= [s["started_at_utc"], s["ended_at_utc"]]
    print(rev, "step window", min(ts), "->", max(ts))
'; echo "EXIT=$?"
```
→ `da64646 step window 2026-10-20T13:47:05.973747+00:00 -> 2026-10-20T14:00:05.228761+00:00`; `d0ab299 step window 2026-10-20T14:27:41.944577+00:00 -> 2026-10-20T14:40:02.270081+00:00`; EXIT=0

C24
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c '
import subprocess,json
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; T="/tmp/kr18-vra.72rnp3d2"; R3=T+"/treerev"; REV="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
labs=["calib-esbuild-0.25.12","calib-shfmt","pro-aether","pro-containerd-shim","pro-esbuild-0.21.5","pro-esbuild-0.27.7","pro-notesmd-cli","pro-op"]
for lab in labs:
    blob=subprocess.run(["git","-C",L,"show",f"{REV}:.ufo/waves/round-17/runs/{lab}/receipt.json"],capture_output=True,check=True).stdout
    p=f"{T}/receipts/pass2all-{lab}.json"; open(p,"wb").write(blob.replace(L.encode(),R3.encode()))
    r=subprocess.run(["python3","-I","-B",T+"/val/receipt-validate.py",p],capture_output=True)
    o=json.loads(r.stdout)["receipts"][0]; rec=json.loads(blob)
    print(lab, "pass-2 exit", r.returncode, "checks", o["checks_performed"], "mid_run_pin_checks", sum(len(s.get("pin_checks") or []) for s in rec["steps"].values()))
'; echo "EXIT=$?"
```
→ calib-esbuild 345/4, calib-shfmt 343/2, pro-aether 344/3, pro-containerd-shim 343/2, pro-esbuild-0.21.5 345/4, pro-esbuild-0.27.7 345/4, pro-notesmd-cli 343/2, pro-op 349/8 (all exit 0); EXIT=0

C25 `cd /tmp/kr18-vra.72rnp3d2 && git clone --no-hardlinks --quiet /home/vgpnk/Projects/shokunin/kaidoku-shokunin clone && git -C clone remote remove origin && git -C clone remote -v && echo "remotes-listed EXIT=$?" && git -C clone checkout -q --detach b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && git -C clone rev-parse HEAD; echo "EXIT=$?"` → no remotes listed; HEAD `b2aad08c…`; EXIT=0

C26
```
cd /tmp/kr18-vra.72rnp3d2/clone && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr18-vra.72rnp3d2/clone --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 | python3 -I -B -c '
import json,sys
d=json.load(sys.stdin)
print("open_count", d["open_count"], "named_open", d["named_open_count"], "substance_open", d["substance_open_count"])
for x in d["defects"]:
    if x["id"]=="R17-VALIDATE16":
        print(x["id"], "open", x["open"])
        for c in x["checks"]: print(" ", c["set"], c["name"], c["ok"], c["detail"][:160])
'; echo "EXIT=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
```
→ `open_count 0`; R17-VALIDATE16 open False, 7/7 ok (`validator-sha256-pinned True validator_sha256='618448829b…'`); EXIT=0 0

C27
```
cd /tmp/kr18-vra.72rnp3d2/clone && python3 -I -B -c '
import json
p=".ufo/waves/round-18/evidence/validate16/summary.json"
d=json.load(open(p))
fake={"rev":d["rev"],"validator_sha256":"f"*64,"receipts":[{"label":r["label"],"exit":0} for r in d["receipts"]]}
open(p,"w").write(json.dumps(fake,indent=2)+"\n")
print(json.dumps(fake)[:300])
' && git rm -q .ufo/waves/round-18/evidence/validate16/*.stdout .ufo/waves/round-18/evidence/validate16/*.stderr && git add -A .ufo/waves/round-18/evidence/validate16 && git -c user.name=ValidateRemapAttack -c user.email=vra@invalid -c commit.gpgsign=false commit -q -m "fabricated VALIDATE16 summary (attack fixture)" && git rev-parse HEAD && git show --stat --format=%s HEAD | cat; echo "EXIT=$?"
```
→ commit `75a1708a9206647eaed1789949981176e5be76b7`; 17 files changed (16 stdout/stderr deleted, summary rewritten); EXIT=0

C28
```
cd /tmp/kr18-vra.72rnp3d2/clone && python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root /tmp/kr18-vra.72rnp3d2/clone --rev 75a1708a9206647eaed1789949981176e5be76b7 --strict | python3 -I -B -c '
import json,sys
d=json.load(sys.stdin)
print("rev", d["rev"], "open_count", d["open_count"], "named_open", d["named_open_count"], "substance_open", d["substance_open_count"])
for x in d["defects"]:
    if x["id"]=="R17-VALIDATE16":
        print(x["id"], "open", x["open"])
        for c in x["checks"]: print(" ", c["set"], c["name"], c["ok"], c["detail"][:110])
'; echo "EXIT=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
```
→ `open_count 0 named_open 0 substance_open 0`; `R17-VALIDATE16 open False`; all 7 checks True incl. `validator-sha256-pinned True validator_sha256='ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'`; EXIT=0 0 (`--strict` exit 0)

C29 (first attempt failed on my own shell quoting: `NameError: name 'label' is not defined`, EXIT=1; rerun:)
```
cd /tmp/kr18-vra.72rnp3d2/clone && python3 -I -B -c '
import subprocess,json,hashlib
root="/tmp/kr18-vra.72rnp3d2/clone"
D=".ufo/waves/round-18/evidence/validate16"; RV=".ufo/waves/round-17/tools/receipt-validate.py"
def show(rev,path):
    r=subprocess.run(["git","-C",root,"show",rev+":"+path],capture_output=True); return r.stdout if r.returncode==0 else None
for rev in ("b2aad08ceeee8dd125ce0d316056d8bd766c7f94","75a1708a9206647eaed1789949981176e5be76b7"):
    doc=json.loads(show(rev,D+"/summary.json")); probs=[]
    vrev=doc.get("validator_rev"); vblob=show(vrev,RV) if isinstance(vrev,str) else None
    if vblob is None or hashlib.sha256(vblob).hexdigest()!=doc.get("validator_sha256"): probs.append("validator_sha256 != sha256(validator_rev:receipt-validate.py)")
    for e in doc["receipts"]:
        lab=e.get("label"); b=show(rev,D+"/"+lab+".stdout")
        if b is None: probs.append(lab+": stdout blob absent"); continue
        if hashlib.sha256(b).hexdigest()!=e.get("stdout_sha256"): probs.append(lab+": stdout_sha256 mismatch")
        o=json.loads(b)
        if o.get("exit")!=e.get("exit") or len(o.get("receipts",[]))!=1: probs.append(lab+": stdout exit/receipt count disagrees")
    print(rev[:12], "bound-evidence check", "PASS" if not probs else "FAIL", probs[:3], "(+%d more)"%max(0,len(probs)-3))
'; echo "EXIT=$?"
```
→ `b2aad08ceeee bound-evidence check PASS [] (+0 more)`; `75a1708a9206 bound-evidence check FAIL ['validator_sha256 != sha256(validator_rev:receipt-validate.py)', 'calib-esbuild-0.25.12: stdout blob absent', 'calib-shfmt: stdout blob absent'] (+6 more)`; EXIT=0

C30 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git grep -n -I -E '34[1-9] checks|checks each' b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- SCORECARD.md LOG.md corpus/ README.md PROVINCE.md SKILL.md 2>&1 | cut -c1-400; echo "grep EXIT=${PIPESTATUS[0]}"` → one unrelated hit (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:123`); grep EXIT=0. (The same call chained a first `verification.json` reader that printed `unparsed` for all 8 records, because `stdout` is a path field. C31 supersedes it, so it is omitted here.)

C31
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-17/verification.json | python3 -I -B -c '
import json,sys,re
d=json.load(sys.stdin)
for c in d.get("commands") or []:
    if str(c.get("label","")).startswith("receipt-validate-"):
        s=c.get("stdout")
        txt=s if isinstance(s,str) else json.dumps(s)
        m=re.findall(r"checks_performed\D+(\d+)",txt)
        print(c["label"], "exit", c.get("exit"), "checks_performed", m, "keys", sorted(c.keys()))
'; echo "EXIT=${PIPESTATUS[1]}"
```
→ 8 records, keys `['argv', 'cwd', 'ended_at_utc', 'env_overrides', 'exit', 'exit_as_expected', 'expected_exit', 'label', 'started_at_utc', 'stderr_path', 'stderr_sha256', 'stdout_path', 'stdout_sha256']`; EXIT=0

C32 `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git grep -n -I -E 'R17-VALIDATE16|341 checks|validate16' b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- SCORECARD.md LOG.md corpus/ PROVINCE.md README.md SKILL.md .ufo/waves/round-18/contract.md .ufo/waves/round-18/verify.py .ufo/waves/round-18/measure.py 2>&1 | cut -c1-700; echo "EXIT=${PIPESTATUS[0]}"` → hits incl. `LOG.md:2159`, `SCORECARD.md:2439`, `corpus/lessons/round-18.md:8,52,63`, `contract.md:33,35`; EXIT=0

C33 `git --version; python3 --version; tar --version | sed -n 1p; stat -c '%y %n' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.git/index; date '+%Y-%m-%d %H:%M:%S %z'; ls -d /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/w2 2>&1; echo "EXIT=$?"` → git 2.56.0, Python 3.14.8, GNU tar 1.35; index mtime `2026-10-20 13:38:12 -0300`; now 13:58:26 -0300; EXIT=0

Anchors cited (REV unless prefixed):
- `.ufo/waves/round-18/evidence/validate16/summary.json:3-10,68-78`
- `.ufo/waves/round-18/tools/routed-defects.py:8-11,392-484,458-462,942-946`
- `corpus/lessons/round-18.md:52,63`
- `corpus/QUALITY.md:28,31`
- `LOG.md:2159`
- `SCORECARD.md:2439`
- `.ufo/waves/round-18/w1/RevValidatorPaths.md:103-104`
- `.ufo/waves/round-18/w1/ScoutValidate16Sites.md:162`
- `9011581:.ufo/waves/round-17/tools/receipt-validate.py:34-37,143-150,173-177,267-269,276-278,294-314`
