"""Probe: does kaidoku r78 `receipt_auth` admit an instrument pin that is not bytes?

Builds a throwaway git repo under --scratch, commits an instrument, a symlink to it,
a directory, then feeds receipts to auth_findings() loaded from the lane's frozen
attack-gate.py.  Read-only against the lane: the module is imported by path.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    return p.returncode, p.stdout, p.stderr


def load_gate(path):
    spec = importlib.util.spec_from_file_location("attack_gate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--gate", required=True)
    a = ap.parse_args()
    gate = load_gate(a.gate)
    repo = os.path.join(a.scratch, "fixture")
    os.makedirs(os.path.join(repo, "tools", "pkg"), exist_ok=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "probe@example.invalid")
    git(repo, "config", "user.name", "probe")
    top = git(repo, "rev-parse", "--show-toplevel")[1].decode().strip()
    assert os.path.realpath(top) == os.path.realpath(repo), top

    with open(os.path.join(repo, "tools", "instrument.py"), "w") as fh:
        fh.write("print('instrument')\n")
    with open(os.path.join(repo, "tools", "pkg", "data.txt"), "w") as fh:
        fh.write("data\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    rev = git(repo, "rev-parse", "HEAD")[1].decode().strip()

    os.symlink("instrument.py", os.path.join(repo, "tools", "link.py"))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "symlink")
    rev_link = git(repo, "rev-parse", "HEAD")[1].decode().strip()

    def show(rev_, path):
        return git(repo, "show", "%s:%s" % (rev_, path))[1]

    # git mode of the symlink and of the directory
    _, ls_link, _ = git(repo, "ls-tree", rev_link, "tools/link.py")
    _, ls_dir, _ = git(repo, "ls-tree", rev_link, "tools/pkg")
    link_blob = show(rev_link, "tools/link.py")
    dir_blob = show(rev_link, "tools/pkg")
    real_blob = show(rev, "tools/instrument.py")

    results = {}

    def auth(path, rev_, text):
        receipt = {"rev": rev_, "instrument": {"path": path,
                                               "sha256": hashlib.sha256(text).hexdigest()}}
        return gate.auth_findings(repo, rev_, path, receipt)

    results["ls_tree_symlink"] = ls_link.decode().strip()
    results["ls_tree_dir"] = ls_dir.decode().strip()
    results["show_symlink_bytes"] = link_blob.decode("utf-8", "replace").strip()
    results["show_dir_bytes_head"] = dir_blob.decode("utf-8", "replace")[:120]
    results["real_bytes_sha"] = hashlib.sha256(real_blob).hexdigest()[:16]

    results["pin_real_file_at_own_rev"] = auth("tools/instrument.py", rev, real_blob)
    results["pin_symlink_hashed_as_link_text"] = auth("tools/link.py", rev_link, link_blob)
    results["pin_symlink_at_real_rev"] = auth("tools/instrument.py", rev_link, real_blob)
    results["pin_tree_listing"] = auth("tools/pkg", rev_link, dir_blob)
    results["control_wrong_sha"] = auth("tools/instrument.py", rev,
                                        b"not the instrument\n")
    results["control_absent_path"] = auth("tools/absent.py", rev, b"x")
    results["control_bad_rev"] = auth("tools/instrument.py", "deadbeef", real_blob)
    print(json.dumps(results, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
