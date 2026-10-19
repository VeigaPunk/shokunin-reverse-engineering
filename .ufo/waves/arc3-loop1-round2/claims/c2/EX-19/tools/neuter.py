#!/usr/bin/env python3
"""EX-19 fixture — neutered-needle injections against the census instrument (H3).

Applies exact literal replacements to a census source, asserts each replacement
landed exactly once (fail-closed), writes the copy, runs it against a scratch
corpus root, and records verdict / G2 line / exit code.

Usage:
  neuter.py --src INSTR.py --tag TAG --root DIR --outdir DIR [--spec SPEC ...]

Specs (needles PIN / VER / PTR are the three value regexes of the instrument):
  full        all three neutered to never-match
  pin|ver|ptr one needle neutered
  pin+ver|pin+ptr|ver+ptr   two of three neutered ("half of the needles", reading A)
  h-ver67     VER narrowed to the 6.7.x value class only (drops 6.5.0 loci);
              partial mute, reading B ("half of each needle's coverage")
  h-all67     PIN and VER narrowed to the 6.7 value class, PTR narrowed to
              config.toml -- the instrument keeps seeing the newest class only
"""
import argparse, hashlib, json, os, subprocess, sys

PIN = 'PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)'
VER = 'VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")'
PTR = 'PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")'

DEAD = {
    "pin": 'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)',
    "ver": 'VER = re.compile(r"(?<![\\d.])9\\.\\d+\\.\\d+")',
    "ptr": 'PTR = re.compile(r"((?:~|/)ZZZ\\.(?:json|toml|ya?ml)):(\\d+)")',
}
NARROW = {
    "pin67": 'PIN = re.compile(r"rea-agents@(6\\.7\\.\\d+)", re.I)',
    "ver67": 'VER = re.compile(r"(?<![\\d.])6\\.7\\.\\d+")',
    "ptr-toml": 'PTR = re.compile(r"((?:~|/)[\\w./+-]*config\\.toml):(\\d+)")',
}
SPECS = {
    "full":      [(PIN, DEAD["pin"]), (VER, DEAD["ver"]), (PTR, DEAD["ptr"])],
    "pin":       [(PIN, DEAD["pin"])],
    "ver":       [(VER, DEAD["ver"])],
    "ptr":       [(PTR, DEAD["ptr"])],
    "pin+ver":   [(PIN, DEAD["pin"]), (VER, DEAD["ver"])],
    "pin+ptr":   [(PIN, DEAD["pin"]), (PTR, DEAD["ptr"])],
    "ver+ptr":   [(VER, DEAD["ver"]), (PTR, DEAD["ptr"])],
    "h-ver67":   [(VER, NARROW["ver67"])],
    "h-all67":   [(PIN, NARROW["pin67"]), (VER, NARROW["ver67"]), (PTR, NARROW["ptr-toml"])],
}


def apply(src_text, pairs, spec):
    out = src_text
    for old, new in pairs:
        n = out.count(old)
        if n != 1:
            raise SystemExit("FIXTURE-ERROR %s: pattern occurs %d times, want 1: %r" % (spec, n, old))
        out = out.replace(old, new)
    return out


def json_field(stdout, key):
    for line in stdout.splitlines():
        s = line.strip()
        if s.startswith('"') and key in s and s.rstrip(",").endswith("**"):
            pass
    # robust: parse if --json used; here stdout is text report
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--spec", action="append")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    src_text = open(args.src, encoding="utf-8").read()
    src_sha = hashlib.sha256(src_text.encode()).hexdigest()
    specs = args.spec or list(SPECS)
    rows = []
    for spec in specs:
        inst = apply(src_text, SPECS[spec], spec)
        ipath = os.path.join(args.outdir, "%s.%s.py" % (args.tag, spec))
        open(ipath, "w", encoding="utf-8").write(inst)
        isha = hashlib.sha256(inst.encode()).hexdigest()
        p = subprocess.run([sys.executable, ipath, "--root", args.root],
                           capture_output=True, text=True)
        out = p.stdout + p.stderr
        opath = os.path.join(args.outdir, "%s.%s.out" % (args.tag, spec))
        open(opath, "w", encoding="utf-8").write(out + "\n[exit=%d]\n" % p.returncode)
        g2 = next((l for l in out.splitlines() if l.startswith("G2 ")), "<no G2 line>")
        verdict = next((l for l in out.splitlines() if l.startswith("VERDICT:")), "<no verdict line>")
        loci = next((l for l in out.splitlines() if "loci=" in l), "")
        rows.append({"spec": spec, "exit": p.returncode, "g2": g2, "verdict": verdict,
                     "counts": [l for l in out.splitlines() if "loci=" in l],
                     "instrument_sha256": isha, "receipt": opath})
    manifest = {"src": args.src, "src_sha256": src_sha, "root": args.root, "tag": args.tag,
                "rows": rows}
    mpath = os.path.join(args.outdir, "%s.matrix.json" % args.tag)
    open(mpath, "w", encoding="utf-8").write(json.dumps(manifest, indent=1) + "\n")
    for r in rows:
        print("%-9s exit=%d %-4s | %s" % (r["spec"], r["exit"],
              "PASS" if r["verdict"].startswith("VERDICT: PASS") else "FAIL", r["g2"]))
    print("manifest: %s" % mpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
