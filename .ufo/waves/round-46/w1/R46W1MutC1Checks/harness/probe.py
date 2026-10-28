#!/usr/bin/env python3
"""Probe harness: score ONE crafted artefact with ONE instrument build.

usage: probe.py --instrument DIR --probe NAME [--scratch ROOT]

Builds a one-commit fixture repo (SKILL.md, claims, lessons, the instrument itself) and runs
`attest.py --root <fixture> --freeze <rev> --rev <rev> --no-battery`, printing the receipt.
The artefact is built with the instrument's OWN good_block(), so the sha256 pin is the
bytes of the instrument under test.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC1Checks"

IDS = ["R45-CL2", "R45-CL6", "R45-CL7", "R45-CL9", "R45-CL13", "R45-CL14",
       "R45-CL15", "R45-CL18", "R45-CL19", "R45-CL20", "R45-CL22", "R45-CL23",
       "R45-CL24"]


def build_skill(m, probe):
    """Return (skill_text, extra_files) for the probe."""
    extra = {}
    kw = {}
    if probe == "p-g4-rows8-all-ids":
        rows = []
        for k in range(0, 12, 2):
            rows.append((" ".join(IDS[k:k + 2]), "two routed ids on one trigger",
                         "presence", "1"))
        rows.append((IDS[12], "the last routed id", "presence", "1"))
        rows.append((IDS[0], "duplicate trigger for the eighth row", "presence", "1"))
        kw["rows"] = tuple(rows)
    elif probe == "p-g7-vocab-wrong-column":
        kw["rows"] = tuple((i, "merge-introduced edit described here", "zzz", "1") for i in IDS)
    elif probe == "p-g9-outside-allow":
        kw["refs"] = m.GOOD_REFS + ", `corpus/QUALITY.md:3`"
        extra["corpus/QUALITY.md"] = "row\n" * 8
    elif probe == "p-g10-refs3":
        kw["refs"] = ("`corpus/lessons/round-45.md:12-30`, `plans/round-46-claims.md:20`, "
                      "`plans/round-46-claims.md:40`")
    elif probe == "p-g11-no-selector":
        import re
        kw["refs"] = re.sub(r":\d+(?:-\d+)?", "", m.GOOD_REFS)
    elif probe == "p-g12-no-round45":
        kw["refs"] = ", ".join(f"`plans/round-46-claims.md:{n}`"
                               for n in (10, 12, 14, 20, 40, 50))
    elif probe == "p-h3-header-prefix":
        kw["header"] = "| trigger | v1 hole | v2 arm code | exit |"
    elif probe == "p-genuine":
        pass
    elif probe == "p-arm-substring":          # pristine-only: clause-4 substring weakness
        kw["rows"] = tuple((i, "hole", "unpinned", "1") for i in IDS)
    elif probe == "iso-ref-selector":          # pristine-only diagnostic
        kw["refs"] = m.GOOD_REFS.replace(":12-30", "").replace(":20", "")
    elif probe == "iso-ref-allow":             # pristine-only diagnostic
        kw["refs"] = m.GOOD_REFS.replace("corpus/lessons/round-45.md:140-150",
                                         "corpus/QUALITY.md:3")
    else:
        raise SystemExit(f"unknown probe {probe}")
    return m.skill_text(m.good_block(**kw)), extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--probe", required=True)
    ap.add_argument("--scratch", default=os.path.join(S, "probe-root"))
    ap.add_argument("--battery", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, a.instrument)
    import attest as m  # noqa: E402

    skill, extra = build_skill(m, a.probe)
    root = tempfile.mkdtemp(dir=a.scratch, prefix="fx-")
    files = dict(extra)
    files.update({"SKILL.md": skill, "plans/round-46-claims.md": m.CLAIMS_BODY,
                  "corpus/lessons/round-45.md": "lesson line\n" * 240,
                  "tools/round-46/attest.py": open(os.path.join(a.instrument, "attest.py")).read(),
                  "tools/round-46/gate.py": open(os.path.join(a.instrument, "gate.py")).read()})
    for p, text in files.items():
        full = os.path.join(root, p)
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    for cmd in (["init", "-q"], ["config", "user.email", "pr@round46"],
                ["config", "user.name", "round46 probe"]):
        subprocess.run(["git", "-C", root, *cmd], check=True)
    top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == root, (top, root)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", "probe"], check=True)
    rev = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    env = dict(os.environ, TMPDIR=os.path.join(a.scratch, "tmp"),
               HYAKU_SCRATCH=os.path.join(a.scratch, "scr"))
    for k in ("TMPDIR", "HYAKU_SCRATCH"):
        os.makedirs(env[k], exist_ok=True)
    r = subprocess.run([sys.executable, "-I", "-B",
                        os.path.join(a.instrument, "attest.py"),
                        "--root", root, "--freeze", rev, "--rev", rev,
                        ] + ([] if a.battery else ["--no-battery"]), capture_output=True, text=True, env=env)
    out = {"instrument": a.instrument, "probe": a.probe, "exit": r.returncode,
           "sha_instrument": m.hashlib.sha256(open(os.path.join(a.instrument,
                                                                "attest.py"), "rb").read()).hexdigest()}
    try:
        rec = json.loads(r.stdout)
        out["failing"] = rec.get("failing")
        out["unresolved_citations"] = rec.get("unresolved_citations")
        out["rows"] = rec.get("rows")
        out["refs"] = rec.get("refs")
        out["header_ok"] = rec.get("header_ok")
        out["reason"] = rec.get("reason")
    except Exception:  # noqa: BLE001
        out["stdout_head"] = (r.stdout + r.stderr).splitlines()[:6]
    print(json.dumps(out, sort_keys=True))
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
