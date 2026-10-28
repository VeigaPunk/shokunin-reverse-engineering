#!/usr/bin/env python3
"""R46W1RevRestoredUnion: does a restore-only history still read `restored` and exit 2?

Imports gate.freeze_state from a scratch COPY of the frozen gate.py; the lane copy is
never opened for write. Every fixture repo is created under S and every git call names
`-C <that repo>`; toplevel is asserted before the first commit.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevRestoredUnion"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
GATE = os.path.join(LANE, "tools/round-46/gate.py")
LIB = os.path.join(S, "lib")

os.makedirs(LIB, exist_ok=True)
shutil.copyfile(GATE, os.path.join(LIB, "gate.py"))
sys.path.insert(0, LIB)
import gate  # noqa: E402

CLAIMS = "plans/round-46-claims.md"

CLAIMS_BODY = (
    "# fixture claims\n"
    + "filler line\n" * 40
    + "\n## Frozen paths (exact)\n\n"
    "- `plans/round-46-claims.md`\n"
    "- `tools/round-46/`\n"
    "\n## After\n\ntail\n"
)

FILES = {
    CLAIMS: CLAIMS_BODY,
    "tools/round-46/attest.py": "print('attest v1')\n",
    "tools/round-46/gate.py": "print('gate v1')\n",
    "SKILL.md": "# skill\n\ntext\n",
}

receipts = []


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run(argv, cwd=None, check=True):
    r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit("command failed: %r rc=%d err=%s" % (argv, r.returncode, r.stderr))
    return r


def gitcall(d, *args):
    return run(["git", "-C", d, *args])


def sha(text):
    return hashlib.sha256(text.encode("utf-8", "surrogateescape")).hexdigest()


def rec(name, argv_text, rc, stdout):
    receipts.append({"case": name, "cmd": argv_text, "exit": rc,
                     "stdout_sha256": sha(stdout), "utc": now()})


def new_repo():
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    run(["git", "-C", d, "init", "-q"])
    for k, v in (("user.email", "r46@fixture"), ("user.name", "r46 fixture"),
                 ("commit.gpgsign", "false")):
        gitcall(d, "config", k, v)
    top = gitcall(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    for p, text in FILES.items():
        put(d, p, text)
    commit(d, "fixture freeze")
    return d, heads(d)


def put(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def read(d, rel):
    with open(os.path.join(d, rel)) as fh:
        return fh.read()


def commit(d, msg):
    gitcall(d, "add", "-A")
    gitcall(d, "commit", "-q", "-m", msg)
    return heads(d)


def heads(d):
    return gitcall(d, "rev-parse", "HEAD").stdout.strip()


def verdict(name, d, freeze, rev, expect_exit=None):
    code, receipt = gate.freeze_state(d, freeze, rev, CLAIMS)
    rec(name, "gate.freeze_state(%s, freeze=%s, rev=%s)" % (d, freeze[:8], rev[:8]),
        code, json.dumps(receipt, sort_keys=True))
    slim = {k: receipt.get(k) for k in
            ("frozen_derived", "touched", "blob_changed", "restored",
             "frozen_path_changed", "reason")}
    ok = "n/a" if expect_exit is None else (code == expect_exit)
    print("\n== %s ==" % name)
    print("exit=%s expect=%s ok=%s" % (code, expect_exit, ok))
    print(json.dumps(slim, indent=1, sort_keys=True))
    return code, receipt


def main():
    out = {}

    # C0 — control: freeze == rev, nothing between. Must be clean.
    d, fz = new_repo()
    out["C0_clean_control"] = verdict("C0_clean_control", d, fz, fz, 0)[0]
    shutil.rmtree(d, ignore_errors=True)

    # C1 — file tamper, NO restore: the arm must fire, restored empty.
    d, fz = new_repo()
    put(d, CLAIMS, read(d, CLAIMS) + "tampered\n")
    rev = commit(d, "tamper claims")
    out["C1_file_tamper_only"] = verdict("C1_file_tamper_only", d, fz, rev, 2)[0]
    shutil.rmtree(d, ignore_errors=True)

    # C2 — file tamper + restore: the assignment's core case.
    d, fz = new_repo()
    put(d, CLAIMS, read(d, CLAIMS) + "tampered\n")
    commit(d, "tamper claims")
    put(d, CLAIMS, CLAIMS_BODY)
    rev = commit(d, "restore claims")
    code, r = verdict("C2_file_tamper_restore", d, fz, rev, 2)
    out["C2_file_tamper_restore"] = {"exit": code, "restored": r["restored"],
                                     "touched": r["touched"], "blob_changed": r["blob_changed"]}
    shutil.rmtree(d, ignore_errors=True)

    # C3 — tamper of a file inside the frozen DIRECTORY, no restore.
    d, fz = new_repo()
    put(d, "tools/round-46/attest.py", "print('attest v1')\n# tampered\n")
    rev = commit(d, "tamper tool")
    code, r = verdict("C3_dir_tamper_only", d, fz, rev, 2)
    out["C3_dir_tamper_only"] = {"exit": code, "restored": r["restored"],
                                 "blob_changed": r["blob_changed"]}
    shutil.rmtree(d, ignore_errors=True)

    # C4 — tamper + restore of a file inside the frozen DIRECTORY: core case.
    d, fz = new_repo()
    put(d, "tools/round-46/attest.py", "print('attest v1')\n# tampered\n")
    commit(d, "tamper tool")
    put(d, "tools/round-46/attest.py", FILES["tools/round-46/attest.py"])
    rev = commit(d, "restore tool")
    code, r = verdict("C4_dir_tamper_restore", d, fz, rev, 2)
    out["C4_dir_tamper_restore"] = {"exit": code, "restored": r["restored"],
                                    "touched": r["touched"], "blob_changed": r["blob_changed"]}
    shutil.rmtree(d, ignore_errors=True)

    # C5 — commit that only ADDS a file inside the frozen directory.
    d, fz = new_repo()
    put(d, "tools/round-46/extra.py", "print('extra')\n")
    rev = commit(d, "add tool")
    code, r = verdict("C5_dir_add_only", d, fz, rev, 2)
    out["C5_dir_add_only"] = {"exit": code, "restored": r["restored"],
                              "touched": r["touched"], "blob_changed": r["blob_changed"]}
    shutil.rmtree(d, ignore_errors=True)

    # C6 — delete then restore a file inside the frozen directory.
    d, fz = new_repo()
    os.unlink(os.path.join(d, "tools/round-46/gate.py"))
    commit(d, "delete tool")
    put(d, "tools/round-46/gate.py", FILES["tools/round-46/gate.py"])
    rev = commit(d, "restore tool")
    code, r = verdict("C6_dir_delete_restore", d, fz, rev, 2)
    out["C6_dir_delete_restore"] = {"exit": code, "restored": r["restored"],
                                    "blob_changed": r["blob_changed"]}
    shutil.rmtree(d, ignore_errors=True)

    # C7 — rename out of and back into the frozen directory (history_touched has no
    # --no-renames, so R<score> records only the first path of the pair).
    d, fz = new_repo()
    gitcall(d, "mv", "tools/round-46/attest.py", "tools/round-46/attest2.py")
    commit(d, "rename out")
    gitcall(d, "mv", "tools/round-46/attest2.py", "tools/round-46/attest.py")
    rev = commit(d, "rename back")
    code, r = verdict("C7_dir_rename_roundtrip", d, fz, rev, 2)
    out["C7_dir_rename_roundtrip"] = {"exit": code, "restored": r["restored"],
                                      "touched": r["touched"], "blob_changed": r["blob_changed"]}
    shutil.rmtree(d, ignore_errors=True)

    # C8 — self-shrink: one commit rewrites the claims file's frozen section to a decoy
    # path AND tampers a tool. Derivation happens at rev, so the decoy set is what both
    # arms see.
    d, fz = new_repo()
    shrunk = CLAIMS_BODY.replace(
        "- `plans/round-46-claims.md`\n- `tools/round-46/`\n",
        "- `corpus/`\n")
    assert shrunk != CLAIMS_BODY
    put(d, CLAIMS, shrunk)
    put(d, "tools/round-46/attest.py", "print('attest v1')\n# tampered\n")
    rev = commit(d, "shrink the frozen set and tamper")
    code, r = verdict("C8_selfshrink_bypass", d, fz, rev, 0)
    out["C8_selfshrink_bypass"] = {"exit": code, "restored": r["restored"],
                                   "frozen_derived": r["frozen_derived"],
                                   "touched": r["touched"], "blob_changed": r["blob_changed"]}
    # C8b — the same history scored with the set derived at the FREEZE (union arm).
    base_entries, err = gate.frozen_set(d, fz, CLAIMS)
    base_paths = [p + "/" for p, dd in base_entries if dd] + [p for p, dd in base_entries if not dd]
    btouched, berr = gate.history_touched(d, fz, rev, base_paths)
    bchanged = gate.blob_changed(d, fz, rev, base_entries)
    rec("C8b_union_arm", "gate.frozen_set(%s, %s) + history_touched/blob_changed" % (d, fz[:8]),
        0 if btouched or bchanged else 1, json.dumps([base_paths, btouched, bchanged]))
    print("\n== C8b_union_arm (set derived at FREEZE) ==")
    print(json.dumps({"base_paths": base_paths, "touched": btouched,
                      "blob_changed": bchanged, "err": err or berr}, indent=1))
    out["C8b_union_arm"] = {"base_paths": base_paths, "touched": btouched,
                            "blob_changed": bchanged}
    shutil.rmtree(d, ignore_errors=True)

    # C9 — partial shrink: only the directory line removed, claims still self-listed.
    d, fz = new_repo()
    partial = CLAIMS_BODY.replace("- `tools/round-46/`\n", "- `corpus/`\n")
    put(d, CLAIMS, partial)
    put(d, "tools/round-46/attest.py", "print('attest v1')\n# tampered\n")
    rev = commit(d, "drop the directory line")
    code, r = verdict("C9_partial_shrink", d, fz, rev, 2)
    out["C9_partial_shrink"] = {"exit": code, "touched": r["touched"],
                                "frozen_derived": r["frozen_derived"]}
    shutil.rmtree(d, ignore_errors=True)

    with open(os.path.join(S, "receipts.json"), "w") as fh:
        json.dump(receipts, fh, indent=1, sort_keys=True)
    with open(os.path.join(S, "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("\nSUMMARY", json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
