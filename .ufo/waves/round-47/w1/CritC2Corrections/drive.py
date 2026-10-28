import json, os, subprocess, sys, textwrap
S = "/fast/scratch/hyaku/kaidoku-r47/CritC2Corrections"
D = os.path.join(S, "fx")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REC = os.path.join(LANE, "tools/round-47/record.py")

def sh(*a, cwd=None):
    r = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    return r

def write(rel, body):
    p = os.path.join(D, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(body)

def commit(msg):
    sh("git", "-C", D, "add", "-A"); sh("git", "-C", D, "commit", "-q", "-m", msg)
    return sh("git", "-C", D, "rev-parse", "HEAD").stdout.strip()

subprocess.run(["rm", "-rf", D])
os.makedirs(D, exist_ok=True)
sh("git", "-C", D, "init", "-q")
top = sh("git", "-C", D, "rev-parse", "--show-toplevel").stdout.strip()
assert os.path.realpath(top) == os.path.realpath(D), (top, D)
sh("git", "-C", D, "config", "user.email", "fx@r47"); sh("git", "-C", D, "config", "user.name", "r47 fx")

# base tree
write("corpus/knowledge/2026-10-01-x.md", "x\n")
write("corpus/README.md", "# readme\n\n## Coverage map\n\n- 2026-10-01-x - fixture\n\n## Gaps\n\ntail\n")
write("tools/x/keep.md", "x\n")
write("SKILL.md", "## Queue-drain craft (fixture)\n\n- **24. Exactness.** See `corpus/README.md:1`.\n")
for rnd, spawns in (("7", (2,)), ("9", (1, 1))):
    for i, sp in enumerate(spawns, 1):
        write(f".ufo/waves/round-{rnd}/w{i}-dispatch.json",
              json.dumps({"counts": {"spawn": sp, "resume": 0, "total": sp}}))
base = commit("base")

def card(window_line, seats_sum, seats_pair, corrections):
    return textwrap.dedent(f"""\
        # fixture card

        ## Owned axes

        | Axis | Baseline to current | Observable | Evidence | Round |
        |---|---|---|---|---|
        | coverage | 9.7 -> 10.0 | 1/1 knowledge files mapped | x | r1 |
        | depth | 9.5 -> 10.0 | 1/1 craft blocks resolved | x | r1 |

        ## Round 8

        An earlier round with no atoms.

        ## Round 9

        Base `{base[:8]}`. {seats_sum}. {seats_pair}. Wave 1 evidence is in
        `.ufo/waves/round-9/w1-dispatch.json`.
        {window_line}

        """) + corrections

WINDOW_PLACEHOLDER = "`git log 0425224..<tip> -- tools/x/keep.md` is empty at every measurement above."
WINDOW_STATED = "`git log 0000000..0000000 -- tools/x/` is empty."   # resolves nowhere, no pair match

C_TRUE_SUM = "Waves: 1 + 1 = 2 seats"
C_FALSE_PAIR = "Wave 1: 7 seats; wave 2: 9 seats"

cards = {}
cards["A-cheapest-false"] = card(
    WINDOW_PLACEHOLDER, C_TRUE_SUM, C_FALSE_PAIR,
    "## Record corrections — round 47\n\n"
    "- corrects seats round-9: 2 waves, 2 seats total\n"
    "- corrects window round-9: empty in {t}..{t} -- tools/x/keep.md\n".format(t=base[:8]))
cards["B-padded"] = card(
    WINDOW_PLACEHOLDER, C_TRUE_SUM, C_FALSE_PAIR,
    "## Record corrections — round 47\n\n"
    "- corrects seats round-9: 2 waves, 2 seats total\n"
    "- corrects window round-9: empty in {t}..{t} -- tools/x/keep.md\n"
    "- corrects seats round-7: 1 waves, 2 seats total\n".format(t=base[:8]))
cards["C-uncorrected"] = card(
    WINDOW_PLACEHOLDER, C_TRUE_SUM, C_FALSE_PAIR, "")
cards["D-axes-arm"] = (card(
    WINDOW_PLACEHOLDER, C_TRUE_SUM, C_FALSE_PAIR,
    "## Record corrections — round 47\n\n"
    "- corrects seats round-9: 2 waves, 2 seats total\n"
    "- corrects window round-9: empty in {t}..{t} -- tools/x/keep.md\n"
    "- corrects axes coverage: 1/1\n".format(t=base[:8]))
    .replace("| coverage | 9.7 -> 10.0 | 1/1 knowledge files mapped | x | r1 |",
             "| coverage | 9.7 -> 10.0 | 0/1 knowledge files mapped | x | r1 |"))

order = ["A-cheapest-false", "B-padded", "C-uncorrected", "D-axes-arm"]
revs = {}
for name in order:
    write("SCORECARD.md", cards[name])
    write("tools/x/keep.md", "x\n%s\n" % name)
    revs[name] = commit(name)

out = {"fixture": D, "base": base, "revs": revs, "runs": []}
for name in order:
    r = sh(sys.executable, "-I", "-B", REC, "--root", D, "--rev", revs[name])
    rec = {}
    try:
        rec = json.loads(r.stdout)
    except Exception:
        rec = {"unparsed": r.stdout[:400], "stderr": r.stderr[:400]}
    out["runs"].append({
        "card": name, "rev": revs[name], "exit": r.returncode,
        "stdout_sha256": __import__("hashlib").sha256(r.stdout.encode()).hexdigest(),
        "counter": json.loads(r.stdout).get("counter") if r.returncode != 2 else None,
        "failing": rec.get("failing"), "mismatches": rec.get("mismatches"),
        "corrections": rec.get("corrections"),
        "corrections_bad": rec.get("corrections_bad"),
        "exempted": rec.get("exempted"),
        "battery": rec.get("battery"),
        "atoms": rec.get("atoms"),
    })
print(json.dumps(out, indent=1))
