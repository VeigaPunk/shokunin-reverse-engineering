"""Probe 3: the remaining refusal arms of kaidoku r78 `receipt_auth`.

Given the fixture repo probe.py built (real file, symlink, directory, data file),
feed receipts that pin a directory, a symlink, a data blob, and a well-formed but
unresolvable 40-hex rev, and see what auth_findings() says.
"""
import argparse, hashlib, importlib.util, json, os, subprocess, sys


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--gate", required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("attack_gate", a.gate)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    repo = os.path.join(a.scratch, "fixture")
    rev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                         capture_output=True).stdout.decode().strip()

    def auth(path, rev_, text):
        return m.auth_findings(repo, rev_, path,
                               {"rev": rev_, "instrument": {"path": path,
                                                            "sha256": hashlib.sha256(text).hexdigest()}})

    out = {
        "rev": rev,
        "pin_non_instrument_blob": auth("tools/pkg/data.txt", rev,
                                        show(repo, rev, "tools/pkg/data.txt")),
        "pin_symlink": auth("tools/link.py", rev, show(repo, rev, "tools/link.py")),
        "pin_tree": auth("tools/pkg", rev, show(repo, rev, "tools/pkg")),
        "pin_40hex_unresolvable_rev": auth("tools/instrument.py", "0" * 40,
                                           show(repo, rev, "tools/instrument.py")),
        "pin_leading_slash_path": auth("/tools/instrument.py", rev,
                                       show(repo, rev, "tools/instrument.py")),
        "ls_tree_modes": subprocess.run(
            ["git", "-C", repo, "ls-tree", rev, "tools/link.py", "tools/pkg",
             "tools/instrument.py"], capture_output=True).stdout.decode(),
    }
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
