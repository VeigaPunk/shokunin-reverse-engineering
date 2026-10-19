#!/usr/bin/env python3
"""RV-7 (chain c2, reviewer) — replay of the round-1 recorded readings.

Purpose: cross-check EX-11's round-2 baseline reproduction against the round-1
recorded readings in `.ufo/waves/arc3-loop1-round1/claims/c3/VZ-3/attack-log.txt`
(plus the companion `census-at-HEAD-vz3.txt`, sha 3b677b8e…). Method: rebuild
VZ-3's exact inputs from git (round-1 rev e845c2b: instrument sha 36e96cd5…,
PROVINCE/SCORECARD/SKILL), replay the recorded injection classes, then replay
the same classes on the round-2 trees. Every run writes verbatim stdout + exit.

Scratch/work root defaults to /var/tmp/rv7-baseline (never /tmp).
"""
import hashlib, os, re, shutil, subprocess, sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R1 = "e845c2b524ad2e59871e004c51a1386e192a74ab"
WORK = "/var/tmp/rv7-baseline"
R1IN = "36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48"
R1SC = "3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418"
FILES = ["PROVINCE.md", "SCORECARD.md", "SKILL.md"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def git_show(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (rev, path)],
                          capture_output=True).stdout


def run(census, root, home=None, tag=""):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if home:
        env["HOME"] = home
    p = subprocess.run([sys.executable, census, "--root", root],
                       capture_output=True, text=True, env=env)
    return p.stdout + p.stderr, p.returncode


def save(name, out, rc):
    path = os.path.join(WORK, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
        fh.write("EXIT=%d\n" % rc)
    tail = [l for l in out.splitlines() if l.startswith(
        ("VERDICT", "SCOPE-ERRORS", "G2 ", "ANCHOR-FAIL"))]
    print("[%-34s] exit=%d  %s" % (name, rc, " | ".join(tail)))
    return path


def tree(dst, rev_or_head="head"):
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    heads = {}
    for fn in FILES:
        raw = git_show(R1, fn) if rev_or_head == "r1" else \
            subprocess.run(["git", "-C", REPO, "show", "HEAD:%s" % fn],
                           capture_output=True).stdout
        p = os.path.join(dst, fn)
        open(p, "wb").write(raw)
        heads[fn] = (sha(p), len(raw.split(b"\n")) - 1)
    return heads


def neuter(src, dst):
    txt = open(src, encoding="utf-8").read()
    subs = [
        ('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
         'PIN = re.compile(r"(?!x)x-neutered-pin")'),
        ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
         'VER = re.compile(r"(?!x)x-neutered-ver")'),
        ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
         'PTR = re.compile(r"(?!x)x-neutered-ptr")'),
    ]
    for old, new in subs:
        assert old in txt, "anchor missing: %r" % old[:50]
        txt = txt.replace(old, new, 1)
    open(dst, "w", encoding="utf-8").write(txt)
    return sha(dst)


def main():
    global WORK
    if len(sys.argv) > 1:
        WORK = sys.argv[1]
    os.makedirs(WORK, exist_ok=True)

    print("== input identity ==")
    r1in = os.path.join(WORK, "r1-instrument.py")
    open(r1in, "wb").write(git_show(R1, ".ufo/gates/c1-census-v10.py"))
    r2in = os.path.join(REPO, ".ufo/gates/c1-census-v10.py")
    print("  r1 instrument  %s  (%d lines)" % (sha(r1in), len(open(r1in).read().splitlines())))
    print("  r2 instrument  %s  (%d lines)" % (sha(r2in), len(open(r2in).read().splitlines())))

    r1root = os.path.join(WORK, "r1-tree")
    r2root = os.path.join(WORK, "r2-tree")
    h1 = tree(r1root, "r1")
    h2 = tree(r2root, "head")
    for fn in FILES:
        print("  r1 %-13s %s lines=%d | r2 %s lines=%d" %
              (fn, h1[fn][0][:16], h1[fn][1], h2[fn][0][:16], h2[fn][1]))

    print("\n== 1. round-1 control (record: census-at-HEAD-vz3.txt sha %s) ==" % R1SC[:16])
    out, rc = run(r1in, r1root)
    p = save("replay-r1-control.out", out, rc)
    print("  sha256(control) = %s  match=%s" % (sha(p.replace(".out", ".out")), "see diff below"))

    print("\n== 2. round-1 fidelity replays (VZ-3 attack-log.txt classes) ==")
    # A4 — SKILL.md absent
    d = os.path.join(WORK, "r1-a4"); shutil.copytree(r1root, d)
    os.remove(os.path.join(d, "SKILL.md"))
    save("replay-r1-A4-absent-skill.out", *run(r1in, d))
    # A5 — PROVINCE.md absent
    d = os.path.join(WORK, "r1-a5"); shutil.copytree(r1root, d)
    os.remove(os.path.join(d, "PROVINCE.md"))
    save("replay-r1-A5-absent-province.out", *run(r1in, d))
    # blind — needles neutered (H3 class, CR-5 fixture shape)
    blind = os.path.join(WORK, "r1-blind.py")
    print("  r1 blind instrument sha256 %s" % neuter(r1in, blind))
    save("replay-r1-blind.out", *run(blind, r1root))
    # A1 — planted tail locus at :1337 (SCORECARD r1 = 1336 lines)
    for idx, plant in enumerate(["kimi rea-agents@6.4.0", "kimi pin: rea-agents@6.4.0"]):
        d = os.path.join(WORK, "r1-a1-c%d" % idx); shutil.copytree(r1root, d)
        with open(os.path.join(d, "SCORECARD.md"), "a") as fh:
            fh.write(plant + "\n")
        save("replay-r1-A1-c%d.out" % idx, *run(r1in, d))
    # A2 — marker stripped at :704 heading
    d = os.path.join(WORK, "r1-a2"); shutil.copytree(r1root, d)
    sc = os.path.join(d, "SCORECARD.md")
    lines = open(sc, encoding="utf-8").read().splitlines(True)
    before = lines[703]
    lines[703] = before.replace("arc2-loop1-round2", "arc2-loop1-r2-STRIPPED")
    open(sc, "w", encoding="utf-8").write("".join(lines))
    save("replay-r1-A2-marker-stripped.out", *run(r1in, d))

    print("\n== 3. round-2 baseline (instrument at HEAD; EX-11's before-state) ==")
    save("rv7-r2-control.out", *run(r2in, r2root))
    d = os.path.join(WORK, "r2-a4"); shutil.copytree(r2root, d)
    os.remove(os.path.join(d, "SKILL.md"))
    save("rv7-r2-A4-absent-skill.out", *run(r2in, d))
    d = os.path.join(WORK, "r2-empty-skill"); shutil.copytree(r2root, d)
    open(os.path.join(d, "SKILL.md"), "w").close()
    save("rv7-r2-empty-skill.out", *run(r2in, d))
    d = os.path.join(WORK, "r2-a5"); shutil.copytree(r2root, d)
    os.remove(os.path.join(d, "PROVINCE.md"))
    save("rv7-r2-A5-absent-province.out", *run(r2in, d))
    blind2 = os.path.join(WORK, "r2-blind.py")
    print("  r2 blind instrument sha256 %s" % neuter(r2in, blind2))
    save("rv7-r2-blind.out", *run(blind2, r2root))
    # A1 analogue on the grown file: same plant text, lands at :1337 (in-file now)
    d = os.path.join(WORK, "r2-a1-1337"); shutil.copytree(r2root, d)
    sc = os.path.join(d, "SCORECARD.md")
    lines = open(sc, encoding="utf-8").read().splitlines(True)
    lines.insert(1336, "kimi rea-agents@6.4.0\n")     # becomes line 1337
    open(sc, "w", encoding="utf-8").write("".join(lines))
    save("rv7-r2-A1-at-1337.out", *run(r2in, d))
    # A1 at the true tail of the grown file (:1418)
    d = os.path.join(WORK, "r2-a1-tail"); shutil.copytree(r2root, d)
    with open(os.path.join(d, "SCORECARD.md"), "a") as fh:
        fh.write("kimi rea-agents@6.4.0\n")
    save("rv7-r2-A1-at-tail.out", *run(r2in, d))

    # H2 control: marker-excused fabricated pin (round-1 A3b class, out of C2 scope)
    d = os.path.join(WORK, "r2-a3b"); shutil.copytree(r2root, d)
    sk = os.path.join(d, "SKILL.md")
    txt = open(sk, encoding="utf-8").read()
    txt = txt.replace("rea-agents@6.5.0", "rea-agents@9.9.9", 1)
    open(sk, "w", encoding="utf-8").write(txt)
    save("rv7-r2-A3b-marker-excused-9.9.9.out", *run(r2in, d))


if __name__ == "__main__":
    main()
