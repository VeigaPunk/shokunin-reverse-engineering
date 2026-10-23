#!/usr/bin/env python3
"""Supplementary probe: the CtlHashReplay hash map also misses every mutant of
the optional frozen author schedule.

The optional author schedule (a fixed, published transformation) is NOT the
schedule the production counter uses, so this probe is supplementary evidence
about the hash map's discriminating power, not a production score. It reads
already-frozen artifacts from the freeze revision. It authors no binary
fixture, writes no ELF, and runs only the control reader.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FREEZE = "54a87a51a865ab931fd355e767303337b05cccf4"
READER = ROOT / "controls" / "round-34" / "ctl-hash-replay.py"


def git(args):
    env = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C", "PATH": "/usr/bin:/bin"}
    run = subprocess.run(["git", "--no-replace-objects", "-C", str(ROOT), *args], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True)
    return run.stdout


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ctl_hash_replay", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = git(["ls-tree", "-r", "--name-only", FREEZE]).decode().split("\n")
    mutants = sorted(p for p in names if "/elf-meta/m" in p and p.endswith(".bin"))
    rows = []
    for path in mutants:
        data = git(["show", FREEZE + ":" + path])
        digest = hashlib.sha256(data).hexdigest()
        hit = digest in module.TABLE
        rows.append({"path": path, "sha256": digest, "bytes": len(data),
                     "in_hash_map": hit,
                     "lookup_result": module.TABLE.get(digest, {"schema": 1, "needed": []})})
    report = {
        "kind": "ctl_hash_replay_author_schedule_miss",
        "freeze": FREEZE,
        "note": "optional frozen author schedule; NOT the production counter schedule",
        "mutants": len(rows),
        "all_miss": all(not r["in_hash_map"] for r in rows),
        "rows": rows,
    }
    print(json.dumps(report, sort_keys=True, indent=1))
    return 0 if report["all_miss"] else 1


if __name__ == "__main__":
    sys.exit(main())
