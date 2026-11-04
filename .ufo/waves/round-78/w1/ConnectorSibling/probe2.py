"""Probe 2 (read-only): (a) the genuine record's receipt_auth coverage at the base
rev, (b) a vacuity fixture — an in-scope record with zero receipt citations.
"""
import argparse, hashlib, importlib.util, json, os, subprocess, sys


def git(repo, *a):
    p = subprocess.run(["git", "-C", repo] + list(a), capture_output=True)
    return p.returncode, p.stdout, p.stderr


def load(path):
    spec = importlib.util.spec_from_file_location("attack_gate", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--gate", required=True)
    a = ap.parse_args()
    gate = load(a.gate)

    live = gate.scan_record(a.lane, a.rev, {"receipt_auth"})
    out = {"live": {"in_scope_cells": live["in_scope_cells"],
                    "groups": live["groups"],
                    "bound_clauses": live["bound_clauses"],
                    "receipt_auth_findings": len([f for f in live["findings"]
                                                  if f.get("rule") == "receipt_auth"])}}

    # vacuity fixture: one in-scope SCORECARD row + one PROVINCE core bullet,
    # no receipt citation and no verdict group at all.
    repo = os.path.join(a.scratch, "vacuous")
    os.makedirs(os.path.join(repo, "tools", "round-78"), exist_ok=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "probe@example.invalid")
    git(repo, "config", "user.name", "probe")
    assert os.path.realpath(git(repo, "rev-parse", "--show-toplevel")[1]
                            .decode().strip()) == os.path.realpath(repo)
    with open(os.path.join(repo, "tools", "round-78", "attack-gate.py"), "w") as fh:
        fh.write("print('x')\n")
    with open(os.path.join(repo, "SCORECARD.md"), "w") as fh:
        fh.write("## Capabilities\n\n| id | what | state | round |\n|---|---|---|---|\n"
                 "| r78-cap | the attack gate | landed | 78 |\n\n## Next\n")
    with open(os.path.join(repo, "PROVINCE.md"), "w") as fh:
        fh.write("- **Core — tools/round-78/attack-gate.py** the gate.\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "vacuous")
    vrev = git(repo, "rev-parse", "HEAD")[1].decode().strip()
    vac = gate.scan_record(repo, vrev, {"receipt_auth", "qualified_atom",
                                        "near_miss_field", "negated_verdict",
                                        "unbound_verdict"})
    out["vacuous"] = {"in_scope_cells": vac["in_scope_cells"],
                      "groups": vac["groups"],
                      "bound_clauses": vac["bound_clauses"],
                      "findings": vac["findings"]}
    out["ok_terms_are"] = "fixtures_total==10 and base_accepted==10 and refused==10 " \
                          "and not genuine.mismatch_count and not genuine.defects " \
                          "and not validate.defects"
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
