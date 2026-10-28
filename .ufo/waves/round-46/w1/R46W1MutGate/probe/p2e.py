#!/usr/bin/env python3
"""P2e: empirical matrix — is the blob arm ever decisive for the VERDICT?

`restored` and `blob_changed` differ trivially (P2b, and the real-lane receipt), but
a coverage argument needs a shape where base exits 2 and the blob-less gate exits 0.
Enumerate tamper shapes against a frozen FILE entry and a frozen DIRECTORY entry.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
WHICH = sys.argv[1]
sys.path.insert(0, os.path.join(S, WHICH, "tools", "round-46"))
import gate  # noqa: E402


def claims_for(entry):
    return ("# claims\n\n## Frozen paths (exact)\n\n- `%s`\n\n## After\n\ntail\n" % entry)


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def run(entry, files, mutate):
    d = tempfile.mkdtemp(dir=S, prefix="p2e-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "p2e@r46"), ("user.name", "p2e")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d
        allf = dict(files)
        allf["plans/round-46-claims.md"] = claims_for(entry)
        for rel, text in allf.items():
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full) or d, exist_ok=True)
            open(full, "w").write(text)
        sh(d, "add", "-A")
        sh(d, "commit", "-q", "-m", "base")
        freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
        mutate(d)
        rev = sh(d, "rev-parse", "HEAD").stdout.strip()
        code, rec = gate.freeze_state(d, freeze, rev)
        return {"entry": entry, "exit": code, "touched": rec.get("touched"),
                "blob_changed": rec.get("blob_changed"),
                "restored": rec.get("restored"),
                "frozen_path_changed": rec.get("frozen_path_changed"),
                "dir_same": (sh(d, "rev-parse", f"{freeze}:{entry.rstrip('/')}").stdout.strip()
                             == sh(d, "rev-parse", f"{rev}:{entry.rstrip('/')}").stdout.strip())
                if entry.endswith("/") else None}
    finally:
        shutil.rmtree(d, ignore_errors=True)


F = "tools/round-46/gate.py"
D_ = "tools/round-46/"
BASE_FILES_F = {F: "v0\n", "u.txt": "u0\n"}
BASE_FILES_D = {F: "v0\n", "tools/round-46/other.py": "o0\n", "u.txt": "u0\n"}


def sh_shape(fn):
    return fn


cases = []


def add(lst, entry, files, name, fn):
    try:
        r = run(entry, files, fn)
        r["shape"] = name
        lst.append(r)
    except Exception as exc:  # noqa: BLE001
        lst.append({"shape": name, "entry": entry, "error": f"{type(exc).__name__}: {exc}"})


def edit(d):
    open(os.path.join(d, F), "a").write("TAMPER\n")
    sh(d, "commit", "-q", "-am", "edit")


def edit_restore(d):
    open(os.path.join(d, F), "a").write("T")
    sh(d, "commit", "-q", "-am", "t")
    open(os.path.join(d, F), "w").write("v0\n")
    sh(d, "commit", "-q", "-am", "r")


def same_bytes_new_commit(d):
    os.utime(os.path.join(d, F), None)
    sh(d, "commit", "-q", "--allow-empty", "-m", "empty")
    open(os.path.join(d, "u.txt"), "a").write("x\n")
    sh(d, "commit", "-q", "-am", "unrelated")


def move_away(d):
    sh(d, "mv", F, "tools/round-46/moved.py")
    sh(d, "commit", "-q", "-m", "rename out of the frozen name")


def copy_in_dir(d):
    shutil.copyfile(os.path.join(d, F), os.path.join(d, "tools/round-46/new.py"))
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "add a file to the frozen dir")


def rename_within(d):
    sh(d, "mv", "tools/round-46/other.py", "tools/round-46/renamed.py")
    sh(d, "commit", "-q", "-m", "rename within the frozen dir")


def delete_and_readd(d):
    os.remove(os.path.join(d, "tools/round-46/other.py"))
    sh(d, "commit", "-q", "-am", "delete")
    open(os.path.join(d, "tools/round-46/other.py"), "w").write("o0\n")
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "re-add identical bytes")


def chmod_only(d):
    os.chmod(os.path.join(d, F), 0o755)
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "mode change only")


def chmod_inside_dir(d):
    os.chmod(os.path.join(d, "tools/round-46/other.py"), 0o755)
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "mode change inside the frozen dir")


def symlink_swap(d):
    p = os.path.join(d, "tools/round-46/other.py")
    os.remove(p)
    os.symlink("other.py", p + ".link")
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "add a symlink inside the frozen dir")


for name, fn in (("edit", edit), ("edit-then-restore", edit_restore),
                 ("unrelated-only", same_bytes_new_commit), ("rename-away", move_away),
                 ("chmod-only", chmod_only)):
    add(cases, F, BASE_FILES_F, name, fn)
for name, fn in (("edit", edit), ("edit-then-restore", edit_restore),
                 ("copy-into-dir", copy_in_dir), ("rename-within", rename_within),
                 ("delete-readd", delete_and_readd), ("rename-away", move_away),
                 ("chmod-inside", chmod_inside_dir), ("symlink-add", symlink_swap)):
    add(cases, D_, BASE_FILES_D, name, fn)

print(json.dumps({"mutant_dir": WHICH,
                  "gate_sha256": hashlib.sha256(
                      open(os.path.join(S, WHICH, "tools/round-46", "gate.py"), "rb")
                      .read()).hexdigest(), "cases": cases}, indent=1))
