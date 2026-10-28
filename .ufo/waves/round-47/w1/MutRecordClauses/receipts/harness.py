#!/usr/bin/env python3
"""Mutation harness for tools/round-47/record.py `failing.append` guards.

Scratch-only. Reads the pristine copy at $S/mut/tools/round-47/record.py, writes
one mutant per guard under $S/mutants/<name>/, and runs the tool's own `--selftest`
as the bounded behavioural detector (exit 0 = all cases pass).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
PRISTINE = os.path.join(S, "mut")
REC = "tools/round-47/record.py"
GATE = "tools/round-46/gate.py"

MUTATIONS = [
    # name, original bytes, replacement
    ("M0-control-comment", '"""Round-47 C2 counter — the lane\'s',
     '"""Round-47 C2 counter (mutant control) — the lane\'s'),
    ("M1-classes-guard",
     '    if missing_classes:\n'
     '        failing.append(f"no atoms of class(es) {missing_classes}")\n',
     '    pass\n'),
    ("M2-mismatches-guard",
     '    if mismatches:\n'
     '        failing.append(f"mismatches {len(mismatches)} != 0")\n',
     '    pass\n'),
    ("M3-corrections-min-guard",
     '    if len(corr) < CORR_MIN:\n'
     '        failing.append(f"corrections {len(corr)} < {CORR_MIN}")\n',
     '    pass\n'),
    ("M4-corrections-bad-guard",
     '    if corrections_bad:\n'
     '        failing.append(f"corrections that do not re-derive: {len(corrections_bad)}")\n',
     '    pass\n'),
    ("M5-exempt-max-guard",
     '    if len(exempted) > EXEMPT_MAX:\n'
     '        failing.append(f"exempted {len(exempted)} > {EXEMPT_MAX}")\n',
     '    pass\n'),
    ("M6-battery-guard",
     '        for key, want in (("correction_forgeries", 3), ("forgeries_green", 0)):\n'
     '            if battery.get(key) != want:\n'
     '                failing.append(f"battery {key} {battery.get(key)} != {want}")\n',
     '        pass\n'),
    ("M6b-battery-greenonly",
     '        for key, want in (("correction_forgeries", 3), ("forgeries_green", 0)):\n'
     '            if battery.get(key) != want:\n'
     '                failing.append(f"battery {key} {battery.get(key)} != {want}")\n',
     '        for key, want in (("correction_forgeries", 3),):\n'
     '            if battery.get(key) != want:\n'
     '                failing.append(f"battery {key} {battery.get(key)} != {want}")\n'),
    ("M6c-battery-countonly",
     '        for key, want in (("correction_forgeries", 3), ("forgeries_green", 0)):\n'
     '            if battery.get(key) != want:\n'
     '                failing.append(f"battery {key} {battery.get(key)} != {want}")\n',
     '        for key, want in (("forgeries_green", 0),):\n'
     '            if battery.get(key) != want:\n'
     '                failing.append(f"battery {key} {battery.get(key)} != {want}")\n'),
    ("M7-ghost-exemption-guard",
     '            if not historical:\n',
     '            if False:\n'),
    ("M8-two-sections-guard",
     '    if len(secs) != 2:\n'
     '        return 2, dict(receipt, reason="fewer than two `## Round N` sections")\n',
     '    pass\n'),
    ("M9-axes-correction-parse",
     'CORR = re.compile(r"^- corrects (seats|window|path|rev) (\\S+):\\s*(.+)$")',
     'CORR = re.compile(r"^- corrects (seats|window|path|rev|axes) (\\S+):\\s*(.+)$")'),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def build(name, old, new):
    text = open(os.path.join(PRISTINE, REC)).read()
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{name}: anchor occurs {n} times")
    d = os.path.join(S, "mutants", name)
    os.makedirs(os.path.join(d, "tools/round-47"), exist_ok=True)
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    out = os.path.join(d, REC)
    with open(out, "w") as fh:
        fh.write(text.replace(old, new, 1))
    shutil.copyfile(os.path.join(PRISTINE, GATE), os.path.join(d, GATE))
    return d, out


def selftest(d):
    env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
    r = subprocess.run([sys.executable, "-I", "-B", os.path.join(d, REC),
                        "--root", d, "--rev", "HEAD", "--selftest"],
                       capture_output=True, text=True, cwd=S, env=env)
    body = r.stdout.split("\n", 1)
    payload = body[1] if len(body) > 1 and body[1].strip().startswith("{") else r.stdout
    try:
        rec = json.loads(payload)
    except ValueError:
        rec = {"parse_error": True, "raw": r.stdout[-800:], "err": r.stderr[-800:]}
    failed = [c["case"] for c in rec.get("cases", []) if not c.get("ok")]
    return {"exit": r.returncode,
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "cases": len(rec.get("cases", [])),
            "failed_cases": failed,
            "battery": [c.get("battery") for c in rec.get("cases", [])
                        if c["case"] == "battery-discriminates"]}


def main():
    pristine_sha = sha(os.path.join(PRISTINE, REC))
    base = selftest(PRISTINE)
    out = {"pristine": {"record_sha256": pristine_sha, "selftest": base}, "mutants": []}
    for name, old, new in MUTATIONS:
        d, path = build(name, old, new)
        got = selftest(d)
        out["mutants"].append({"name": name, "record_sha256": sha(path),
                               "selftest": got,
                               "verdict": "killed" if got["exit"] != 0 else "survived"})
    out["pristine_sha_after"] = sha(os.path.join(PRISTINE, REC))
    with open(os.path.join(S, "mutations.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("pristine selftest exit", base["exit"], "sha", pristine_sha)
    print("%-32s %-5s %-9s %s" % ("mutation", "exit", "verdict", "failed cases"))
    for m in out["mutants"]:
        print("%-32s %-5d %-9s %s" % (m["name"], m["selftest"]["exit"], m["verdict"],
                                      ",".join(m["selftest"]["failed_cases"]) or "-"))
    print("pristine sha unchanged:", pristine_sha == out["pristine_sha_after"])


if __name__ == "__main__":
    main()
