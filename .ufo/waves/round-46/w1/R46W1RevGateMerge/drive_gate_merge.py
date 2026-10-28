#!/usr/bin/env python3
"""Round-46 wave-1 seat R46W1RevGateMerge: attack the freeze core's merge arm.

Drives the FROZEN gate.py bytes (git show <FREEZE>:tools/round-46/gate.py) over
fixture repos in scratch. Every git call names -C <fixture>. Every step records
{cmd, exit, stdout_sha256, utc}. Exit codes are semantic: 0 clean, 1 violation,
2 could-not-evaluate.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

S = os.environ["HYAKU_SCRATCH"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "31820472784284727546808acc31b3ea1e73919b"
FROZEN_FILES = [
    "plans/round-46-claims.md",
    "tools/round-46/gate.py",
    "tools/round-46/attest.py",
    "tools/round-46/registry.py",
    "tools/round-46/census.py",
    "tools/round-46/census.json",
]
GATE_PATH = os.path.join(S, "gate_frozen.py")
RECEIPTS = []


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(args, cwd=None, expect=None):
    """Run one command, record the receipt shape the contract demands."""
    r = subprocess.run(args, cwd=cwd, capture_output=True,
                       env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    rec = {"cmd": " ".join(args), "cwd": cwd, "exit": r.returncode,
           "stdout_sha256": sha(r.stdout), "stdout_bytes": len(r.stdout),
           "utc": utc()}
    if r.stdout:
        rec["stdout"] = r.stdout.decode("utf-8", "surrogateescape")
    if r.stderr.strip():
        rec["stderr"] = r.stderr.decode("utf-8", "surrogateescape")[:800]
    RECEIPTS.append(rec)
    if expect is not None and r.returncode not in (expect if isinstance(expect, (list, tuple)) else [expect]):
        raise SystemExit("unexpected exit %d for %s\n%s" % (
            r.returncode, rec["cmd"], rec["stderr"] if "stderr" in rec else ""))
    return r


def g(D, *args, expect=None):
    return run(["git", "-C", D, *args], expect=expect)


def write(D, rel, data):
    p = os.path.join(D, rel)
    os.makedirs(os.path.dirname(p) or D, exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(p, mode) as fh:
        fh.write(data)


def read(D, rel):
    with open(os.path.join(D, rel), "rb") as fh:
        return fh.read()


# --- frozen bytes, captured read-only from the lane -----------------------------
def capture_frozen():
    blobs = {}
    for rel in FROZEN_FILES:
        r = run(["git", "-C", LANE, "show", "%s:%s" % (FREEZE, rel)], expect=0)
        blobs[rel] = r.stdout
        print("frozen-byte %s sha256=%s" % (rel, sha(r.stdout)))
    with open(GATE_PATH, "wb") as fh:
        fh.write(blobs["tools/round-46/gate.py"])
    print("gate_frozen.py sha256=%s" % sha(blobs["tools/round-46/gate.py"]))
    return blobs


BLOBS = {}


def new_repo(name, with_frozen=True, extra=None):
    D = os.path.join(S, "fx", name)
    if os.path.isdir(D):
        shutil.rmtree(D)
    os.makedirs(D)
    g(D, "init", "-q", "-b", "main", expect=0)
    for k, v in (("user.email", "rev@gatemerge.invalid"),
                 ("user.name", "R46W1RevGateMerge"),
                 ("commit.gpgsign", "false"),
                 ("merge.conflictstyle", "diff3")):
        g(D, "config", k, v, expect=0)
    top = g(D, "rev-parse", "--show-toplevel", expect=0).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    write(D, "notes.txt", "base\n")
    if with_frozen:
        for rel, data in BLOBS.items():
            write(D, rel, data)
    if extra:
        for rel, data in extra.items():
            write(D, rel, data)
    g(D, "add", "-A", expect=0)
    g(D, "commit", "-q", "-m", "freeze", expect=0)
    return D, g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()


def tamper(D, rel="tools/round-46/gate.py", text="TAMPER\n"):
    write(D, rel, read(D, rel) + text.encode())


def restore(D, rel="tools/round-46/gate.py"):
    write(D, rel, BLOBS[rel])


def commit_all(D, msg):
    g(D, "add", "-A", expect=0)
    g(D, "commit", "-q", "-m", msg, expect=0)
    return g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()


GATE = None


def freeze_state(D, base, tip):
    code, rec = GATE.freeze_state(D, base, tip)
    keep = {k: rec.get(k) for k in
            ("reason", "frozen_derived", "frozen_path_changed", "blob_changed",
             "touched", "restored", "freeze", "rev")}
    return {"exit": code, "receipt": keep}


def log_breakdown(D, base, tip):
    """Per-commit view of the exact history arm, for attribution."""
    r = g(D, "log", "-m", "--diff-merges=first-parent", "--name-status",
          "--format=%h %s", "%s..%s" % (base, tip),
          "--", "plans/round-46-claims.md", "tools/round-46/", expect=0)
    return r.stdout.decode("utf-8", "surrogateescape")


def parse_tokens(raw):
    """Replica of gate.history_touched's token walk, for argv-variant probes."""
    toks = raw.decode("utf-8", "surrogateescape").split("\0")
    out, i = set(), 0
    import re
    pat = re.compile(r"^[ACDMRTUXB][0-9]*$")
    while i < len(toks):
        if pat.match(toks[i].strip()) and i + 1 < len(toks):
            if toks[i + 1]:
                out.add(toks[i + 1])
            i += 2
            continue
        i += 1
    return sorted(out)


def raw_arm(D, base, tip, *flags):
    r = g(D, "log", *flags, "--name-status", "-z", "--format=",
          "%s..%s" % (base, tip), "--",
          "plans/round-46-claims.md", "tools/round-46/", expect=0)
    return {"argv": ["git", "-C", D, "log", *flags, "--name-status", "-z",
                     "--format=", "%s..%s" % (base, tip), "--",
                     "plans/round-46-claims.md", "tools/round-46/"],
            "stdout_sha256": sha(r.stdout),
            "parsed_touched": parse_tokens(r.stdout),
            "utc": utc()}


RESULTS = {}


def record(name, D, base, tip, expected, note):
    res = freeze_state(D, base, tip)
    res["expected_by_claims"] = expected
    res["note"] = note
    res["history_breakdown"] = log_breakdown(D, base, tip)
    res["fixture"] = D
    res["base"], res["tip"] = base, tip
    RESULTS[name] = res
    print("\n== %s  exit=%d  touched=%s blob=%s restored=%s" % (
        name, res["exit"], res["receipt"]["touched"],
        res["receipt"]["blob_changed"], res["receipt"]["restored"]))
    print(res["history_breakdown"])
    return res


def scenario_a1():
    """Conflict directly on the frozen file; resolution restores original bytes."""
    D, F = new_repo("a1-conflict-frozen")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: edit frozen gate.py")
    g(D, "checkout", "-q", "main", expect=0)
    tamper(D, text="MAIN-EDIT\n")
    commit_all(D, "main: edit frozen gate.py differently")
    g(D, "merge", "--no-ff", "--no-edit", "side", expect=1)  # conflict
    restore(D)                                               # resolution edit
    commit_all(D, "merge: resolve by restoring original bytes")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    return record("a1-conflict-on-frozen-restore", D, F, tip, 2,
                  "two branches both edit the frozen file; conflict resolved by "
                  "restoring the freeze bytes. Main's own commit also touches, so "
                  "this shape does not isolate the side commit.")


def scenario_a2():
    """One-sided frozen edit, clean auto-merge, resolution edit reverts to freeze bytes."""
    D, F = new_repo("a2-evilmerge-revert")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: edit frozen gate.py")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "notes.txt", "base\nmain\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "--no-ff", "--no-commit", "side", expect=0)  # clean auto-merge
    restore(D)                                                 # resolution edit
    commit_all(D, "merge: revert side's frozen edit")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("a2-one-sided-tamper-merge-revert", D, F, tip, 2,
               "only the side commit touched the frozen path; the merge's own "
               "resolution restored the bytes. Isolates the side commit as the "
               "detector (merge diff vs first parent is empty here).")
    r["merge_diff_vs_first_parent"] = g(
        D, "diff", "--name-status", "HEAD^1", "HEAD", expect=0).stdout.decode()
    return r


def scenario_a3():
    """Conflict on a non-frozen file; one-sided frozen tamper; resolution restores it."""
    D, F = new_repo("a3-conflict-elsewhere-restore")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    write(D, "notes.txt", "base\nside\n")
    commit_all(D, "side: tamper frozen + edit notes")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "notes.txt", "base\nmain\n")
    commit_all(D, "main: edit notes")
    g(D, "merge", "--no-ff", "--no-edit", "side", expect=1)  # conflict on notes.txt
    write(D, "notes.txt", "base\nresolved\n")
    restore(D)
    commit_all(D, "merge: resolve notes, restore frozen bytes")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    return record("a3-conflict-elsewhere-one-sided-restore", D, F, tip, 2,
                  "the conflict is on notes.txt; the frozen edit is one-sided and "
                  "the merge's resolution restores it. Most faithful to the seat "
                  "brief's (a).")


def scenario_b():
    """Same conflict, resolution keeps the tampered bytes."""
    D, F = new_repo("b-conflict-keep")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: edit frozen gate.py")
    g(D, "checkout", "-q", "main", expect=0)
    tamper(D, text="MAIN-EDIT\n")
    commit_all(D, "main: edit frozen gate.py differently")
    g(D, "merge", "--no-ff", "--no-edit", "side", expect=1)
    write(D, "tools/round-46/gate.py", b"TAMPER\n")  # resolution keeps the edit
    commit_all(D, "merge: resolve keeping the edit")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    return record("b-conflict-keep-edit", D, F, tip, 2,
                  "resolution keeps a tampered frozen file: both arms must fire.")


def scenario_c():
    """Squash merge folds a tamper+restore away."""
    D, F = new_repo("c-squash-fold")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: tamper")
    restore(D)
    commit_all(D, "side: restore")
    write(D, "notes.txt", "base\nside\n")
    commit_all(D, "side: unrelated notes change")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "other.txt", "main\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "--squash", "side", expect=0)
    commit_all(D, "squash-merge side")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("c-squash-tamper-then-restore", D, F, tip, 0,
               "claims file states this is the inherent limit: nothing survives in "
               "history for either arm. Landed block-23 row R45-CL19 advertises "
               "exit 2 with a blob arm -> compare.")
    r["squash_commit_diff"] = g(D, "show", "--name-status", "--format=%h %s",
                                tip, expect=0).stdout.decode()
    r["diff_freeze_to_tip_frozen"] = g(
        D, "diff", "--name-status", F, tip, "--", "plans/round-46-claims.md",
        "tools/round-46/", expect=0).stdout.decode()
    r["frozen_tree_equal"] = g(
        D, "diff", "--quiet", F, tip, "--", "plans/round-46-claims.md",
        "tools/round-46/").returncode
    return r


def scenario_c2():
    """Control: squash folds a tamper that is NOT restored."""
    D, F = new_repo("c2-squash-kept")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: tamper")
    write(D, "notes.txt", "base\nside\n")
    commit_all(D, "side: unrelated notes change")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "other.txt", "main\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "--squash", "side", expect=0)
    commit_all(D, "squash-merge side")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    return record("c2-squash-tamper-kept-control", D, F, tip, 2,
                  "control proving the arm is not blind to squash in general: the "
                  "squashed commit's own diff names the frozen path.")


def scenario_d():
    """Plain fast-forward merge, nothing frozen touched."""
    D, F = new_repo("d-ff-clean")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    write(D, "notes.txt", "base\nside\n")
    side = commit_all(D, "side: unrelated")
    g(D, "checkout", "-q", "main", expect=0)
    g(D, "merge", "--ff-only", "side", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("d-fast-forward-clean", D, F, tip, 0,
               "no merge commit is created; the side commit is in FREEZE..REV and "
               "is read directly by the history arm.")
    r["ff_equals_side"] = tip == side
    r["merge_commit_created"] = g(D, "rev-list", "--merges", "--count",
                                  "%s..%s" % (F, tip), expect=0).stdout.decode().strip()
    return r


def scenario_d2():
    """Control: fast-forward that carries a frozen tamper."""
    D, F = new_repo("d2-ff-tamper")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: tamper frozen")
    g(D, "checkout", "-q", "main", expect=0)
    g(D, "merge", "--ff-only", "side", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    return record("d2-fast-forward-tamper-control", D, F, tip, 2,
                  "control: a fast-forward is not a blind spot when it carries the "
                  "frozen change.")


def scenario_e():
    """The merge itself introduces the frozen edit (R45-CL6's exact shape)."""
    D, F = new_repo("e-evil-merge-own-edit")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    write(D, "notes.txt", "base\nside\n")
    commit_all(D, "side: unrelated only")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "other.txt", "main\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "--no-ff", "--no-commit", "side", expect=0)
    tamper(D, text="EVIL-MERGE\n")     # the merge's own resolution introduces it
    commit_all(D, "merge: resolution adds a frozen edit")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("e-merge-only-frozen-edit", D, F, tip, 2,
               "no branch commit touched the frozen path: only the merge's own "
               "first-parent diff can see it. This is the R45-CL6 discriminator.")
    r["arm_variants"] = {
        "v2_exact": raw_arm(D, F, tip, "-m", "--diff-merges=first-parent"),
        "without_dash_m": raw_arm(D, F, tip, "--diff-merges=first-parent"),
        "v1_no_diff_merges": raw_arm(D, F, tip),
        "diff_merges_separate": raw_arm(D, F, tip, "--diff-merges=separate"),
    }
    return r


def scenario_f():
    """Tamper committed then restored by a later commit, no merge at all."""
    D, F = new_repo("f-later-restore")
    tamper(D, text="TAMPER\n")
    commit_all(D, "main: tamper")
    restore(D)
    commit_all(D, "main: restore")
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    return record("f-later-restore-no-merge", D, F, tip, 2,
                  "control for the 'a later restore does not un-block' sentence: "
                  "touched names it, blob arm is clean, restored names it.")


def scenario_g():
    """Conflict resolved on the side branch, then main fast-forwards to the merge."""
    D, F = new_repo("g-reverse-parent-order")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: edit frozen")
    g(D, "checkout", "-q", "main", expect=0)
    tamper(D, text="MAIN-EDIT\n")
    commit_all(D, "main: edit frozen differently")
    g(D, "checkout", "-q", "side", expect=0)
    g(D, "merge", "--no-ff", "--no-edit", "main", expect=1)  # first parent = side
    restore(D)
    commit_all(D, "merge (on side): restore freeze bytes")
    g(D, "checkout", "-q", "main", expect=0)
    g(D, "merge", "--ff-only", "side", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("g-reverse-parent-order-restore", D, F, tip, 2,
               "the merge's first parent is the tampered side branch, so the "
               "first-parent diff itself shows the revert.")
    r["first_parent"] = g(D, "rev-parse", tip + "^1", expect=0).stdout.decode().strip()
    return r


def scenario_h():
    """False-positive probe: merge whose second parent predates the freeze."""
    D = os.path.join(S, "fx", "h-old-ancestor")
    if os.path.isdir(D):
        shutil.rmtree(D)
    os.makedirs(D)
    g(D, "init", "-q", "-b", "main", expect=0)
    for k, v in (("user.email", "rev@gatemerge.invalid"),
                 ("user.name", "R46W1RevGateMerge"),
                 ("commit.gpgsign", "false")):
        g(D, "config", k, v, expect=0)
    assert os.path.realpath(g(D, "rev-parse", "--show-toplevel", expect=0)
                            .stdout.decode().strip()) == os.path.realpath(D)
    write(D, "notes.txt", "c0\n")
    g(D, "add", "-A", expect=0)
    g(D, "commit", "-q", "-m", "c0 pre-freeze", expect=0)
    c0 = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    g(D, "checkout", "-q", "-b", "stale", c0, expect=0)
    write(D, "docs/old.txt", "stale\n")
    g(D, "add", "-A", expect=0)
    g(D, "commit", "-q", "-m", "stale: predates the freeze", expect=0)
    g(D, "checkout", "-q", "main", expect=0)
    for rel, data in BLOBS.items():
        write(D, rel, data)
    write(D, "notes.txt", "c0\nfreeze\n")
    g(D, "add", "-A", expect=0)
    g(D, "commit", "-q", "-m", "freeze", expect=0)
    F = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    write(D, "notes.txt", "c0\nfreeze\nmain\n")
    g(D, "add", "-A", expect=0)
    g(D, "commit", "-q", "-m", "main: after freeze", expect=0)
    g(D, "merge", "--no-ff", "--no-edit", "stale", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("h-merge-second-parent-predates-freeze", D, F, tip, 0,
               "no commit in FREEZE..REV touches a frozen path; the merge's second "
               "parent predates the freeze. A second-parent diff would falsely "
               "report the freeze's own additions and exit 2.")
    r["arm_variants"] = {
        "v2_exact": raw_arm(D, F, tip, "-m", "--diff-merges=first-parent"),
        "without_dash_m": raw_arm(D, F, tip, "--diff-merges=first-parent"),
        "diff_merges_separate": raw_arm(D, F, tip, "--diff-merges=separate"),
    }
    r["merge_vs_second_parent"] = g(
        D, "diff", "--name-status", tip + "^2", tip, expect=0).stdout.decode()
    return r


def scenario_i():
    """`git merge -s ours`: the merge discards the tamper but the side commit stays."""
    D, F = new_repo("i-ours-merge")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    tamper(D, text="SIDE-EDIT\n")
    commit_all(D, "side: tamper")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "other.txt", "main\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "-s", "ours", "--no-ff", "--no-edit", "side", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("i-ours-merge-discards-edit", D, F, tip, 2,
               "-s ours keeps main's tree (blob arm clean) but the side commit is "
               "still in FREEZE..REV, so touched must name the path.")
    r["tree_equals_main"] = g(D, "diff", "--quiet", tip + "^1", tip).returncode
    return r


def scenario_j():
    """Parser attribution: rename out of / into the frozen directory."""
    D, F = new_repo("j-rename-attribution")
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    g(D, "mv", "tools/round-46/census.json", "tools/round-46/census-renamed.json",
      expect=0)
    commit_all(D, "side: rename inside the frozen dir")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "other.txt", "main\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "--no-ff", "--no-edit", "side", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("j-rename-inside-frozen-dir", D, F, tip, 2,
               "R status carries two paths; the token walk records only the first, "
               "so touched should name the old path and the blob arm must still fire.")
    r["raw_name_status"] = g(D, "log", "--diff-merges=first-parent", "--name-status",
                             "--format=%h %s", "%s..%s" % (F, tip), "--",
                             "tools/round-46/", expect=0).stdout.decode()
    r["arm_variants"] = {"v2_exact": raw_arm(D, F, tip, "-m",
                                             "--diff-merges=first-parent")}
    return r


def scenario_k():
    """Parser attribution: rename INTO the frozen directory from outside."""
    D, F = new_repo("k-rename-into-frozen", extra={"outside/thing.py": "x\n"})
    g(D, "add", "-A", expect=0)  # extra committed by new_repo already; no-op if same
    g(D, "checkout", "-q", "-b", "side", F, expect=0)
    g(D, "mv", "outside/thing.py", "tools/round-46/thing.py", expect=0)
    commit_all(D, "side: rename into the frozen dir")
    g(D, "checkout", "-q", "main", expect=0)
    write(D, "other.txt", "main\n")
    commit_all(D, "main: unrelated")
    g(D, "merge", "--no-ff", "--no-edit", "side", expect=0)
    tip = g(D, "rev-parse", "HEAD", expect=0).stdout.decode().strip()
    r = record("k-rename-into-frozen-dir", D, F, tip, 2,
               "the old path is outside the frozen scope: the token walk can name a "
               "non-frozen path in touched, which the blob arm must still cover.")
    r["raw_name_status"] = g(D, "log", "--diff-merges=first-parent", "--name-status",
                             "--format=%h %s", "%s..%s" % (F, tip), "--",
                             "tools/round-46/", expect=0).stdout.decode()
    r["arm_variants"] = {"v2_exact": raw_arm(D, F, tip, "-m",
                                             "--diff-merges=first-parent")}
    return r


def main():
    global BLOBS
    BLOBS = capture_frozen()
    spec = importlib.util.spec_from_file_location("gate_frozen", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    globals()["GATE"] = mod
    print("gate module __file__=%s" % mod.__file__)
    print("gate functions: freeze_state/history_touched/blob_changed present=%s" % all(
        hasattr(mod, n) for n in ("freeze_state", "history_touched", "blob_changed")))
    for fn in (scenario_a1, scenario_a2, scenario_a3, scenario_b, scenario_c,
               scenario_c2, scenario_d, scenario_d2, scenario_e, scenario_f,
               scenario_g, scenario_h, scenario_i, scenario_j, scenario_k):
        fn()
    out = {"freeze": FREEZE, "gate_sha256": sha(BLOBS["tools/round-46/gate.py"]),
           "results": RESULTS, "receipts": RECEIPTS, "utc": utc(),
           "scratch": S}
    p = os.path.join(S, "receipts.json")
    with open(p, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("\nwrote %s sha256=%s" % (p, sha(open(p, "rb").read())))


if __name__ == "__main__":
    main()
