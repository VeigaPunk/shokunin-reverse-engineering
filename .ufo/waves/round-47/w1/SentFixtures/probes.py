#!/usr/bin/env python3
"""Cross-cutting probes: root symlink, json-out containment, env identity, submodule
worktree dirt, trace2 mutation audit, post-cross barrier."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import datetime

S, L, REV = sys.argv[1:4]
REC = os.path.join(S, "receipts")
codes = {"commit": [], "init": [], "add": [], "update-ref": []}


def run(argv, env=None, timeout=900):
    e = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    if env:
        e.update(env)
    r = subprocess.run(argv, capture_output=True, env=e, timeout=timeout)
    return r


def counter(tool, root, extra, env=None):
    argv = [sys.executable, "-I", "-B", os.path.join(L, "tools", "round-47", tool),
            "--root", root, *extra]
    r = run(argv, env=env)
    try:
        payload = json.loads(r.stdout.decode())
    except ValueError:
        payload = {"unparsed": r.stdout.decode()[:1000]}
    return {"argv": argv, "rc": r.returncode,
            "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
            "receipt": payload, "stderr": r.stderr.decode()[:400]}


out = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "scratch": S, "lane": L, "pinned_rev": REV}

# ---- root symlink: does --root follow a symlink into the real fixture? -----------
link = os.path.join(S, "rootlink")
if os.path.islink(link):
    os.unlink(link)
os.symlink(os.path.join(S, "F1"), link)
out["root_symlink"] = counter("exact.py", link, ["--freeze", REV, "--rev", REV,
                                                 "--no-battery"])
out["root_symlink_realpath"] = os.path.realpath(link)

# ---- --json-out containment: refused outside the given root and inside graded ----
out["jsonout_outside_root"] = counter(
    "exact.py", os.path.join(S, "F1"),
    ["--freeze", REV, "--rev", REV, "--no-battery",
     "--json-out", os.path.join(REC, "should-not-exist.json")])
out["jsonout_inside_graded"] = counter(
    "exact.py", os.path.join(S, "F1"),
    ["--freeze", REV, "--rev", REV, "--no-battery",
     "--json-out", os.path.join(S, "F1", "SKILL.md")])
allowed_target = os.path.join(S, "F1", "sentfixtures-out.json")
if os.path.exists(allowed_target):
    os.unlink(allowed_target)
out["jsonout_inside_root_allowed"] = counter(
    "exact.py", os.path.join(S, "F1"),
    ["--freeze", REV, "--rev", REV, "--no-battery", "--json-out", allowed_target])
out["jsonout_inside_root_written"] = os.path.exists(allowed_target)
out["jsonout_outside_root_created"] = os.path.exists(
    os.path.join(REC, "should-not-exist.json"))
if os.path.exists(allowed_target):
    os.unlink(allowed_target)

# ---- bare repo json-out ----------------------------------------------------------
bare = os.path.join(S, "F5.git")
out["bare_jsonout"] = counter("record.py", bare,
                              ["--rev", REV, "--no-battery",
                               "--json-out", os.path.join(bare, "sentfixtures-out.json")])
out["bare_jsonout_written"] = os.path.exists(os.path.join(bare, "sentfixtures-out.json"))

# ---- env identity: does the fixture commit inherit GIT_AUTHOR_* from the caller? --
sys.path.insert(0, L + "/tools/round-47")
import exact  # noqa: E402


def repo_authors(env):
    saved = {k: os.environ.get(k) for k in
             ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME",
              "GIT_COMMITTER_EMAIL")}
    try:
        for k, v in env.items():
            os.environ[k] = v
        d, rev = exact._repo({"probe.txt": "probe\n"}, S, prefix="ident-")
        row = {
            "dir": d, "rev": rev,
            "authors": subprocess.run(["git", "-C", d, "log", "--format=%an <%ae>|%cn <%ce>"],
                                      capture_output=True, text=True).stdout.strip(),
            "local_user_email": subprocess.run(
                ["git", "-C", d, "config", "--local", "--get", "user.email"],
                capture_output=True, text=True).stdout.strip(),
            "show_origin": subprocess.run(
                ["git", "-C", d, "config", "--show-origin", "--get-all", "user.email"],
                capture_output=True, text=True).stdout.strip(),
        }
        shutil.rmtree(d, ignore_errors=True)
        return row
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


out["identity_control"] = repo_authors({})
out["identity_poisoned"] = repo_authors({
    "GIT_AUTHOR_NAME": "Operator Real Name", "GIT_AUTHOR_EMAIL": "operator@example.invalid",
    "GIT_COMMITTER_NAME": "Operator Real Name",
    "GIT_COMMITTER_EMAIL": "operator@example.invalid"})

# ---- submodule worktree dirt ----------------------------------------------------
D = os.path.join(S, "F4")
child1 = json.load(open(os.path.join(REC, "fixtures-structural.json")))[
    "F4-submodule"]["child1"]
sub = os.path.join(D, "evidence/sub")
r = subprocess.run(["git", "-C", sub, "checkout", "-q", child1], capture_output=True,
                   text=True)
status = subprocess.run(["git", "-C", D, "status", "--porcelain"], capture_output=True,
                        text=True).stdout.strip()
sys.path.insert(0, L + "/tools/round-46")
import gate  # noqa: E402
out["submodule_worktree_dirt"] = {
    "checkout_rc": r.returncode, "status_porcelain": status,
    "dirty_no_pathspec": gate.dirty(D, []),
    "dirty_frozen_pathspec": gate.dirty(D, ["plans/round-47-claims.md", "tools/round-47/"])}

# ---- trace2 mutation audit ------------------------------------------------------
def audit_trace(path):
    commits, inits, dirs, bad = [], [], set(), []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            argv = ev.get("argv")
            if not argv or argv[0] != "git":
                continue
            # reconstruct the effective -C target
            target = None
            if "-C" in argv:
                target = argv[argv.index("-C") + 1]
            sub = [a for a in argv[1:] if a in ("commit", "init", "add", "submodule")]
            if sub:
                dirs.add(target)
                if target and not os.path.realpath(target).startswith(
                        os.path.realpath(S) + os.sep):
                    bad.append({"argv": argv, "target": target})
                if "commit" in sub:
                    commits.append({"target": target, "argv": argv})
                if "init" in sub:
                    inits.append({"target": target, "argv": argv})
    return {"commits": len(commits), "inits": len(inits),
            "distinct_targets": sorted(d for d in dirs if d), "outside_scratch": bad,
            "commit_targets_sample": [c["target"] for c in commits[:6]]}


out["trace2_c1_baseline"] = audit_trace(os.path.join(REC, "trace2-c1-baseline.json"))
out["trace2_c2_baseline"] = audit_trace(os.path.join(REC, "trace2-c2-baseline.json"))

# ---- post-cross barrier ---------------------------------------------------------
cfg = os.path.expanduser("~/.config/git/config")


def sh(argv):
    r = subprocess.run(argv, capture_output=True, text=True)
    return {"rc": r.returncode, "stdout": r.stdout.strip()[:1500],
            "stderr": r.stderr.strip()[:300]}


out["post_cross"] = {
    "global_config_sha256": hashlib.sha256(open(cfg, "rb").read()).hexdigest(),
    "dot_gitconfig_exists": os.path.exists(os.path.expanduser("~/.gitconfig")),
    "lane_head": sh(["git", "-C", L, "rev-parse", "HEAD"]),
    "lane_status_frozen": sh(["git", "-C", L, "status", "--porcelain", "--", "SKILL.md",
                              "SCORECARD.md", "plans/round-47-claims.md",
                              "tools/round-47/"]),
    "lane_grep_scratch_at_head": sh(["git", "-C", L, "grep", "-F", S, "HEAD"]),
    "lane_worktrees": sh(["git", "-C", L, "worktree", "list", "--porcelain"]),
    "fixture_commits_absent_from_lane": {
        name: sh(["git", "-C", L, "cat-file", "-e", oid + "^{commit}"])["rc"]
        for name, oid in {
            "F1-merge": open(os.path.join(REC, "f1-merge-oid.txt")).read().strip(),
            "F1b-merge": open(os.path.join(REC, "f1b-merge-oid.txt")).read().strip(),
            "F2-rename": json.load(open(os.path.join(REC, "fixtures-structural.json")))[
                "F2-rename"]["rev"],
        }.items()},
    "battery_dirs_left": sorted(d for d in os.listdir(S)
                                if d.startswith("kaidoku-r47-battery-")),
    "tmp_battery_dirs": sorted(d for d in os.listdir("/tmp")
                               if d.startswith("kaidoku-r47-")),
    "scratch_entries": sorted(os.listdir(S)),
}

json.dump(out, open(os.path.join(REC, "probes.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({k: (v if not isinstance(v, dict) or "receipt" not in v else
                      {"rc": v["rc"], "reason": v["receipt"].get("reason"),
                       "failing": v["receipt"].get("failing")})
                  for k, v in out.items()}, indent=1)[:7000])
