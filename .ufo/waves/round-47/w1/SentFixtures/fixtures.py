#!/usr/bin/env python3
"""SentFixtures fixture battery: rename / symlink / submodule / bare + identity probes.

Every mutating git call is asserted to target a repo under $S.  Read-only calls against
the lane are never made here (the counters are executed separately).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S, L, REV = sys.argv[1:4]
REC = os.path.join(S, "receipts")
MUTATING = {"init", "add", "commit", "mv", "rm", "submodule", "checkout", "clone",
            "config", "update-ref", "symbolic-ref", "fetch", "merge", "switch"}
audit = []


def run(args, check=True, cwd=None):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    if check and r.returncode != 0:
        raise RuntimeError(f"{args} -> {r.returncode}: {r.stderr[:400]}")
    return r


def git(d, *args, check=True):
    top = run(["git", "-C", d, "rev-parse", "--show-toplevel"], check=False).stdout.strip()
    if top and top != os.path.realpath(d):
        raise RuntimeError(f"toplevel {top} != {d}")
    if args and any(a in MUTATING for a in args[:4]):
        assert os.path.realpath(d).startswith(os.path.realpath(S) + os.sep), \
            f"mutating git outside scratch: {d} {args[:2]}"
        audit.append({"dir": d, "argv": list(args)})
    return run(["git", "-C", d, *args], check=check)


def clone(name):
    d = os.path.join(S, name)
    shutil.rmtree(d, ignore_errors=True)
    run(["git", "clone", "-q", "--no-local", L, d])
    git(d, "checkout", "-q", "-B", "main", REV)
    git(d, "config", "user.email", "sent-fixtures@round47.invalid")
    git(d, "config", "user.name", "SentFixtures fixture")
    return d


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def head(d):
    return git(d, "rev-parse", "HEAD").stdout.strip()


results = {}

# ---------------------------------------------------------------- F2 rename -------
D = clone("F2")
git(D, "mv", "tools/round-47/exact.py", "tools/round-47/exact-core.py")
git(D, "mv", "corpus/lessons/round-45.md", "tools/round-47/round-45-lesson.md")
git(D, "commit", "-q", "-m", "rename out of and into the frozen directory")
R2 = head(D)
ns = git(D, "diff", "--name-status", "-z", REV, R2, "--", "tools/round-47/",
         "corpus/lessons/").stdout
toks = [t for t in ns.split("\0") if t]
sys.path.insert(0, L + "/tools/round-46")
import gate  # noqa: E402

touched, err = gate.history_touched(D, REV, R2, ["tools/round-47/"])
correct = set()
i = 0
while i < len(toks):
    if toks[i][:1] in "RC" and i + 2 < len(toks):
        correct.update(toks[i + 1:i + 3])
        i += 3
    else:
        if i + 1 < len(toks):
            correct.add(toks[i + 1])
        i += 2
code2, rec2 = gate.freeze_state(D, REV, R2, "plans/round-47-claims.md")
results["F2-rename"] = {
    "rev": R2, "name_status_tokens": toks,
    "history_touched": touched,
    "correct_two_sided_paths": sorted(correct),
    "new_side_paths_missed_by_gate": sorted(correct - set(touched)),
    "freeze_state_exit": code2,
    "freeze_state_reason": rec2.get("reason"),
    "blob_changed": rec2.get("blob_changed"),
    "touched": rec2.get("touched"),
    "restored": rec2.get("restored"),
    "frozen_path_changed": rec2.get("frozen_path_changed"),
}

# --------------------------------------------------------------- F3 symlink -------
D = clone("F3")
git(D, "mv", "SKILL.md", "skill-real.md")
os.symlink("skill-real.md", os.path.join(D, "SKILL.md"))
os.makedirs(os.path.join(D, "probe"), exist_ok=True)
os.symlink("../../nowhere.md", os.path.join(D, "probe/dangling.md"))
git(D, "add", "SKILL.md", "probe/dangling.md", "skill-real.md")
git(D, "commit", "-q", "-m", "SKILL.md becomes a symlink; a dangling symlink appears")
R3 = head(D)
raw_show = git(D, "show", f"{R3}:SKILL.md").stdout
raw_dangle = git(D, "show", f"{R3}:probe/dangling.md").stdout
tgt = run(["readlink", os.path.join(D, "probe/dangling.md")]).stdout.strip()
os.path.exists(os.path.join(D, "probe/dangling.md"))
sys.path.insert(0, L + "/tools/round-47")
import record  # noqa: E402

f3 = lambda p: gate.show(D, R3, p)  # noqa: E731
atom = {"class": "path", "key": "probe/dangling.md", "atom": "probe/dangling.md",
        "path": "probe/dangling.md"}
ok_path, detail_path = record.derive(atom, f3, D, R3, lambda r: (None, "unused"))
dangling_target_exists = os.path.exists(os.path.realpath(
    os.path.join(D, "probe/dangling.md")))
results["F3-symlink"] = {
    "rev": R3,
    "git_show_SKILL_md": raw_show,
    "git_show_dangling": raw_dangle,
    "dangling_target_exists_on_disk": dangling_target_exists,
    "path_atom_ok": ok_path, "path_atom_detail": detail_path,
}

# second commit on a side branch: the frozen claims file becomes a symlink
git(D, "checkout", "-q", "-B", "claims-link", REV)
git(D, "mv", "plans/round-47-claims.md", "plans/round-47-claims-real.md")
os.symlink("round-47-claims-real.md", os.path.join(D, "plans/round-47-claims.md"))
git(D, "add", "plans/round-47-claims.md", "plans/round-47-claims-real.md")
git(D, "commit", "-q", "-m", "the frozen claims path becomes a symlink")
R3b = head(D)
code3b, rec3b = gate.freeze_state(D, REV, R3b, "plans/round-47-claims.md")
results["F3-symlink-claims"] = {
    "rev": R3b, "freeze_state_exit": code3b, "reason": rec3b.get("reason"),
    "show_claims": gate.show(D, R3b, "plans/round-47-claims.md"),
}

# ------------------------------------------------------------- F4 submodule -------
child = os.path.join(S, "subchild")
shutil.rmtree(child, ignore_errors=True)
os.makedirs(child)
run(["git", "-C", child, "init", "-q", "-b", "main"], check=True)
run(["git", "-C", child, "config", "user.email", "sent-fixtures@round47.invalid"])
run(["git", "-C", child, "config", "user.name", "SentFixtures fixture"])
write(child, "asset.txt", "child asset v1\n")
run(["git", "-C", child, "add", "-A"])
run(["git", "-C", child, "commit", "-q", "-m", "child v1"])
child1 = run(["git", "-C", child, "rev-parse", "HEAD"]).stdout.strip()
write(child, "asset.txt", "child asset v2\n")
run(["git", "-C", child, "add", "-A"])
run(["git", "-C", child, "commit", "-q", "-m", "child v2"])
child2 = run(["git", "-C", child, "rev-parse", "HEAD"]).stdout.strip()

D = clone("F4")
git(D, "-c", "protocol.file.allow=always", "submodule", "add", "-q", child, "evidence/sub")
git(D, "commit", "-q", "-m", "add a submodule at evidence/sub")
R4 = head(D)
show_sub = run(["git", "-C", D, "show", f"{R4}:evidence/sub"], check=False)
rev_parse_sub = git(D, "rev-parse", f"{R4}:evidence/sub").stdout.strip()
gitmodules = git(D, "show", f"{R4}:.gitmodules").stdout
f4 = lambda p: gate.show(D, R4, p)  # noqa: E731
atom_sub = {"class": "path", "key": "evidence/sub", "atom": "evidence/sub",
            "path": "evidence/sub"}
ok_sub, detail_sub = record.derive(atom_sub, f4, D, R4, lambda r: (None, "unused"))
# make the submodule worktree disagree with the gitlink
git(D, "-c", "protocol.file.allow=always", "submodule", "update", "--init", "-q")
run(["git", "-C", os.path.join(D, "evidence/sub"), "fetch", "-q", "origin"])
run(["git", "-C", os.path.join(D, "evidence/sub"), "checkout", "-q", child2])
status_full = git(D, "status", "--porcelain").stdout.strip()
dirty_frozen = gate.dirty(D, ["plans/round-47-claims.md", "tools/round-47/"])
dirty_all = gate.dirty(D, [])
results["F4-submodule"] = {
    "rev": R4, "child1": child1, "child2": child2,
    "gitmodules": gitmodules,
    "git_show_submodule_rc": show_sub.returncode,
    "git_show_submodule_out": show_sub.stdout[:200],
    "rev_parse_submodule": rev_parse_sub,
    "path_atom_ok": ok_sub, "path_atom_detail": detail_sub,
    "status_porcelain": status_full,
    "gate_dirty_on_frozen_pathspec": dirty_frozen,
    "gate_dirty_no_pathspec": dirty_all,
}

# F4c: the frozen directory itself is a gitlink
D = clone("F4c")
shutil.rmtree(os.path.join(D, "tools/round-47"))
git(D, "rm", "-q", "-r", "--cached", "tools/round-47")
git(D, "commit", "-q", "-m", "drop the frozen tool directory")
git(D, "-c", "protocol.file.allow=always", "submodule", "add", "-q", child,
    "tools/round-47")
git(D, "commit", "-q", "-m", "the frozen directory becomes a gitlink")
R4c = head(D)
code4c, rec4c = gate.freeze_state(D, REV, R4c, "plans/round-47-claims.md")
results["F4c-submodule-frozen"] = {
    "rev": R4c, "freeze_state_exit": code4c, "reason": rec4c.get("reason"),
    "blob_changed": rec4c.get("blob_changed"),
    "frozen_path_changed": rec4c.get("frozen_path_changed"),
    "show_exact_py": gate.show(D, R4c, "tools/round-47/exact.py"),
}

# ------------------------------------------------------------------ F5 bare -------
bare = os.path.join(S, "F5.git")
shutil.rmtree(bare, ignore_errors=True)
run(["git", "clone", "-q", "--bare", "--no-local", L, bare])
run(["git", "-C", bare, "update-ref", "refs/heads/main", REV])
run(["git", "-C", bare, "symbolic-ref", "HEAD", "refs/heads/main"])
results["F5-bare"] = {
    "path": bare,
    "is_bare": run(["git", "-C", bare, "rev-parse", "--is-bare-repository"]).stdout.strip(),
    "head": run(["git", "-C", bare, "rev-parse", "HEAD"]).stdout.strip(),
    "status_rc": run(["git", "-C", bare, "status", "--porcelain"], check=False).returncode,
    "status_err": run(["git", "-C", bare, "status", "--porcelain"],
                      check=False).stderr.strip(),
}

# ---------------------------------------------------------------- audit -----------
barrier = json.load(open(os.path.join(REC, "pre-cross.json")))
results["_meta"] = {"scratch": S, "lane": L, "pinned_rev": REV,
                    "mutating_calls": len(audit),
                    "all_mutating_under_scratch": all(
                        os.path.realpath(a["dir"]).startswith(os.path.realpath(S) + os.sep)
                        for a in audit),
                    "git_audit": audit, "barrier": barrier}
with open(os.path.join(REC, "fixtures-structural.json"), "w") as fh:
    json.dump(results, fh, indent=1, sort_keys=True)
print(json.dumps({k: (v if k == "_meta" else
                      {kk: vv for kk, vv in v.items() if kk != "git_audit"})
                  for k, v in results.items()}, indent=1)[:6000])
