import hashlib, json, os, subprocess, sys, textwrap
S = "/fast/scratch/hyaku/kaidoku-r47/CritC2Corrections"
D = os.path.join(S, "fx")
REC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py"
def sh(*a): return subprocess.run(list(a), capture_output=True, text=True)
def commit(msg):
    sh("git","-C",D,"add","-A"); sh("git","-C",D,"commit","-q","-m",msg)
    return sh("git","-C",D,"rev-parse","HEAD").stdout.strip()
base = sh("git","-C",D,"rev-list","--max-parents=0","HEAD").stdout.split()[0]
T = base[:8]
card = textwrap.dedent(f"""\
    # fixture card

    ## Owned axes

    | Axis | Baseline to current | Observable | Evidence | Round |
    |---|---|---|---|---|
    | coverage | 9.7 -> 10.0 | 1/1 knowledge files mapped | x | r1 |
    | depth | 9.5 -> 10.0 | 1/1 craft blocks resolved | x | r1 |

    ## Round 8

    An earlier round with no atoms.

    ## Round 9

    Base `{T}`. Waves: 1 + 1 = 2 seats. Wave 1 \u2014 7 seats; wave 2 \u2014 9 seats.
    `git log {T}..{T} -- tools/x/keep.md` is empty, and the wave-1 evidence is in
    `.ufo/waves/round-9/w1-dispatch.json`.

    ## Record corrections \u2014 round 47

    - corrects seats round-7: 1 waves, 2 seats total
    - corrects seats round-7: 1 waves, 2 seats total
    - corrects window round-9: empty in {T}..{T} -- tools/x/keep.md
    """)
open(os.path.join(D,"SCORECARD.md"),"w").write(card)
open(os.path.join(D,"tools/x/keep.md"),"a").write("H\n")
rev = commit("H-grammar-evasion")
r = sh(sys.executable,"-I","-B",REC,"--root",D,"--rev",rev)
rec = json.loads(r.stdout)
print(json.dumps({"card":"H-grammar-evasion","rev":rev,"exit":r.returncode,
  "stdout_sha256":hashlib.sha256(r.stdout.encode()).hexdigest(),
  "failing":rec.get("failing"),"mismatches":rec.get("mismatches"),
  "corrections":rec.get("corrections"),"corrections_bad":rec.get("corrections_bad"),
  "exempted":rec.get("exempted"),"atoms_by_class":rec.get("atoms_by_class"),
  "battery":{k:(rec.get("battery") or {}).get(k) for k in ("correction_forgeries","forgeries_green")}}, indent=1))
