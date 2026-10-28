import hashlib, json, os, subprocess, sys, textwrap
S = "/fast/scratch/hyaku/kaidoku-r47/CritC2Corrections"
D = os.path.join(S, "fx")
REC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py"
def sh(*a): return subprocess.run(list(a), capture_output=True, text=True)
def commit(msg):
    sh("git","-C",D,"add","-A"); sh("git","-C",D,"commit","-q","-m",msg)
    return sh("git","-C",D,"rev-parse","HEAD").stdout.strip()
base = sh("git","-C",D,"rev-list","--max-parents=0","HEAD").stdout.split()[0]

HEADER = textwrap.dedent("""\
    # fixture card

    ## Owned axes

    | Axis | Baseline to current | Observable | Evidence | Round |
    |---|---|---|---|---|
    | coverage | 9.7 -> 10.0 | 1/1 knowledge files mapped | x | r1 |
    | depth | 9.5 -> 10.0 | 1/1 craft blocks resolved | x | r1 |

    ## Round 8

    An earlier round with no atoms.

    ## Round 9

    Base `%s`. %%s. Wave 1 evidence is in
    `.ufo/waves/round-9/w1-dispatch.json`.
    %%s

    """ ) % base[:8]

def card(sum_line, pair_line, windows, corrections):
    body = HEADER % (sum_line + " " + pair_line, windows)
    return body + corrections

W = "`git log 0425224..<tip> -- tools/x/keep.md` is empty at every measurement above."
W2 = "`git log 0425224..<tip> -- tools/x/keep.md` is empty in the wave-1 window too."
T = base[:8]

variants = {
 "E-duplicate-padding": card("Waves: 1 + 1 = 2 seats", "Wave 1: 7 seats; wave 2: 9 seats", W,
   "## Record corrections \u2014 round 47\n\n"
   "- corrects seats round-9: 2 waves, 2 seats total\n"
   "- corrects seats round-9: 2 waves, 2 seats total\n"
   f"- corrects window round-9: empty in {T}..{T} -- tools/x/keep.md\n"),
 "F-four-false": card("Waves: 5 + 5 = 99 seats", "Wave 1: 7 seats; wave 2: 9 seats", W + "\n" + W2,
   "## Record corrections \u2014 round 47\n\n"
   "- corrects seats round-9: 2 waves, 2 seats total\n"
   f"- corrects window round-9: empty in {T}..{T} -- tools/x/keep.md\n"),
 "G-dup-shape": card("Waves: 1 + 1 = 2 seats", "Wave 1: 7 seats; wave 2: 9 seats", W,
   "## Record corrections \u2014 round 47\n\n"
   "- corrects seats round-9: 2 waves, 2 seats total\n"
   f"- corrects window round-9: empty in {T}..{T} -- tools/x/keep.md\n"),
}
out = []
for name in ("F-four-false",):
    open(os.path.join(D, "SCORECARD.md"), "w").write(variants[name])
    open(os.path.join(D, "tools/x/keep.md"), "a").write(name + "\n")
    rev = commit(name)
    r = sh(sys.executable, "-I", "-B", REC, "--root", D, "--rev", rev)
    rec = json.loads(r.stdout)
    out.append({"card": name, "rev": rev, "exit": r.returncode,
                "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
                "failing": rec.get("failing"), "corrections": rec.get("corrections"),
                "corrections_bad": rec.get("corrections_bad"),
                "exempted": [(e["class"], e["key"], e["atom"][:60]) for e in rec.get("exempted") or []],
                "battery": {k: (rec.get("battery") or {}).get(k) for k in ("correction_forgeries","forgeries_green")}})
print(json.dumps(out, indent=1))
