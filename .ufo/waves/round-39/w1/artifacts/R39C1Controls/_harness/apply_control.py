#!/usr/bin/env python3
"""Apply one R39-C1 control to a scratch clone and score it with the round-39 counter.

This tool never touches the lane.  Point it at a *clone* (or fixture repo) in
scratch; it commits only inside that clone.  The lane's git is read-only here.

Required freeze content in the clone (authored by L1):
  .ufo/waves/round-39/c1/carriers.json  (six carriers; fields id, sha256, path,
      oracle, symlinks, optional size)
  tools/round-39/c1-counter.py
  tools/round-27/xpin-attribute.mjs
  corpus/SOURCES.md, corpus/README.md, PROVINCE.md

Usage (post-freeze controls 0,1,2,3,4,6,7,8,9)
  apply_control.py --control <CTL-DIR> --clone <DIR> --freeze <SHA> \
      --pkg65 <REA650_PKG> [--counter tools/round-39/c1-counter.py] \
      [--entry corpus/knowledge/<stem>.md] [--skip-counter]

Usage (CTL-C1-5, receipts in the freeze commit)
  # stage the freeze content in the clone's working tree first, then:
  apply_control.py --control <CTL-DIR> --clone <DIR> --mode in-freeze \
      --pkg65 <REA650_PKG> [--counter ...]

Exit 0 when the counter's exit equals control.json expected.exit, 1 when the
control defeated/changed the counter verdict, 2 on tooling failure.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_ENTRY = "corpus/knowledge/2026-10-26-r39-sasquatch-be-squashfs-promotion.md"
CARRIERS = ".ufo/waves/round-39/c1/carriers.json"
BLOCKS = {
    "core": ("PROVINCE.md", "PROVINCE.round39-core.md", "eof"),
    "frontier": ("PROVINCE.md", "PROVINCE.round39-frontier-note.md", "eof"),
    "sources": ("corpus/SOURCES.md", "SOURCES.round39-rows.md", "registry"),
    "readme": ("corpus/README.md", "README.round39-row.md", "coverage"),
    "entry": (None, "entry.md", "file"),
}
HERE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(os.path.dirname(HERE), "_shared")


def die(msg):
    print("apply_control: " + msg, file=sys.stderr)
    sys.exit(2)


def git(clone, *args, check=True):
    p = subprocess.run(["git", "-C", clone, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        die("git %s: %s" % (" ".join(args), p.stderr.strip()))
    return p


def git_show(clone, rev, path):
    p = git(clone, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def next_sids(text):
    import re
    ids = [int(m) for m in re.findall(r"\|\s*S(\d{3,})\s*\|", text or "")]
    n = max(ids) + 1 if ids else 1
    return "S%03d" % n, "S%03d" % (n + 1)


def subst(text, mapping):
    for k, v in mapping.items():
        text = text.replace("{{%s}}" % k, v)
    return text


def block(name, mapping):
    path = os.path.join(SHARED, BLOCKS[name][1])
    return subst(open(path, encoding="utf-8").read(), mapping)


def append_eof(path, text):
    cur = open(path, encoding="utf-8").read()
    if not cur.endswith("\n"):
        cur += "\n"
    open(path, "w", encoding="utf-8").write(cur + text)


def insert_after_table(path, heading, text):
    lines = open(path, encoding="utf-8").read().splitlines()
    if heading not in lines:
        die("heading %r absent from %s" % (heading, path))
    i = lines.index(heading)
    last = None
    j = i + 1
    while j < len(lines):
        s = lines[j]
        if s.startswith("|"):
            last = j
        elif s.strip() == "":
            pass
        else:
            break
        j += 1
    if last is None:
        die("no table under %r in %s" % (heading, path))
    lines[last + 1:last + 1] = text.splitlines()
    if not lines or lines[-1] != "":
        lines.append("")
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def fabricate(clone, carriers, ids, mode, pkg65, out):
    tool = os.path.join(HERE, "fabricate_receipts.py")
    cmd = [sys.executable, tool, "--carriers", carriers, "--lane-root", clone,
           "--mode", mode, "--out", out, "--only", ",".join(ids)]
    if mode != "copy38":
        cmd += ["--pkg65", pkg65,
                "--template", os.path.join(clone, "corpus/evidence/round-38/c1/K1/after.json")]
    p = subprocess.run(cmd, cwd=clone, capture_output=True, text=True)
    if p.returncode != 0:
        die("fabricate %s: %s" % (mode, p.stderr.strip()))
    got = []
    for cid in ids:
        src = os.path.join(out, cid, "after.json")
        if os.path.exists(src):
            got.append((cid, src))
    return got


def copy_overlay(control, clone, mapping):
    src = os.path.join(control, "overlay")
    if not os.path.isdir(src):
        return []
    written = []
    for root, _, names in os.walk(src):
        for name in names:
            s = os.path.join(root, name)
            rel = os.path.relpath(s, src)
            rel = subst(rel, mapping)
            d = os.path.join(clone, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)
            written.append(rel)
    return written


def apply_docs(control, spec, clone, mapping, entry):
    written = []
    for name in spec.get("docs", []):
        if name == "entry":
            d = os.path.join(clone, entry)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            open(d, "w", encoding="utf-8").write(block("entry", mapping))
            written.append(entry)
            continue
        target, _, anchor = BLOCKS[name]
        path = os.path.join(clone, target)
        text = block(name, mapping)
        if anchor == "eof":
            append_eof(path, "\n" + text)
        elif anchor == "registry":
            insert_after_table(path, "## Registry", text)
        elif anchor == "coverage":
            insert_after_table(path, "## Coverage map", text)
        written.append(target)
    return sorted(set(written))


def commit(clone, msg):
    git(clone, "add", "-A")
    p = subprocess.run(
        ["git", "-C", clone, "-c", "user.name=fx", "-c", "user.email=fx@fx",
         "commit", "-q", "-m", msg], capture_output=True, text=True)
    if p.returncode != 0:
        die("commit: " + (p.stderr or p.stdout).strip())
    return git(clone, "rev-parse", "HEAD").stdout.strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", required=True)
    ap.add_argument("--clone", required=True)
    ap.add_argument("--freeze")
    ap.add_argument("--mode", default="post-freeze", choices=["post-freeze", "in-freeze"])
    ap.add_argument("--pkg65", required=True)
    ap.add_argument("--carriers")
    ap.add_argument("--counter", default="tools/round-39/c1-counter.py")
    ap.add_argument("--entry", default=DEFAULT_ENTRY)
    ap.add_argument("--json-out")
    ap.add_argument("--receipt-dir")
    ap.add_argument("--skip-counter", action="store_true")
    a = ap.parse_args(argv)

    pv = None
    try:
        pv = json.load(open(os.path.join(a.pkg65, "package.json"))).get("version")
    except (OSError, ValueError):
        pass
    if pv is not None and pv != "6.5.0":
        print("warning: --pkg65 package.json version is %s, not 6.5.0; "
              "the counter's xpin rule is that pin" % pv, file=sys.stderr)
    print("note: xpin runs with --pkg67 = --pkg65 (no 6.7.0 root on this host); "
          "the 6.7.0 column is the 6.5.0 rule and is not evidence of a 6.7.0 rule",
          file=sys.stderr)

    clone = os.path.abspath(a.clone)
    control = os.path.abspath(a.control)
    spec = json.load(open(os.path.join(control, "control.json")))
    entry = a.entry
    stem = os.path.splitext(os.path.basename(entry))[0]
    carriers = a.carriers or os.path.join(clone, CARRIERS)
    if not os.path.exists(carriers):
        die("carriers.json absent: " + carriers)

    src = open(os.path.join(clone, "corpus/SOURCES.md"), encoding="utf-8").read()
    sid, sid2 = next_sids(src)
    mapping = {"ENTRY": entry, "STEM": stem, "SID": sid, "SID2": sid2,
               "LANE": clone}
    out = {"control": spec["control"], "mode": a.mode, "entry": entry,
           "source_ids": [sid, sid2], "commits": [], "written": []}

    if a.mode == "post-freeze":
        if not a.freeze:
            die("--freeze required for post-freeze")
        branch = "ctl/" + spec["control"]
        git(clone, "checkout", "-q", "-B", branch, a.freeze)
        freeze = git(clone, "rev-parse", "HEAD").stdout.strip()
        split = spec.get("commit", {}).get("split", [])
        if "receipts" in split:
            out["written"] += copy_overlay(control, clone, mapping)
            gen = spec.get("generate")
            if gen:
                with tempfile.TemporaryDirectory(prefix="ctlgen.") as tmp:
                    for cid, path in fabricate(clone, carriers, gen["ids"], gen["mode"],
                                               a.pkg65, tmp):
                        dst = os.path.join(clone, "corpus/evidence/round-39/c1", cid,
                                           "after.json")
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copyfile(path, dst)
                        out["written"].append(os.path.relpath(dst, clone))
            msgs = spec["commit"]["commits"]
            out["commits"].append(commit(clone, msgs[0]))
        if "docs" in split:
            out["written"] += apply_docs(control, spec, clone, mapping, entry)
            msgs = spec["commit"]["commits"]
            out["commits"].append(commit(clone, msgs[1] if len(msgs) > 1 else msgs[0]))
        rev = git(clone, "rev-parse", "HEAD").stdout.strip()
    else:
        out["written"] += copy_overlay(control, clone, mapping)
        gen = spec.get("generate")
        if gen:
            with tempfile.TemporaryDirectory(prefix="ctlgen.") as tmp:
                for cid, path in fabricate(clone, carriers, gen["ids"], gen["mode"],
                                           a.pkg65, tmp):
                    dst = os.path.join(clone, "corpus/evidence/round-39/c1", cid,
                                       "after.json")
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copyfile(path, dst)
                    out["written"].append(os.path.relpath(dst, clone))
        out["written"] += apply_docs(control, spec, clone, mapping, entry)
        out["commits"].append(commit(clone, spec["commit"]["commits"][0]))
        freeze = rev = git(clone, "rev-parse", "HEAD").stdout.strip()

    out["freeze"] = freeze
    out["rev"] = rev
    if not a.skip_counter:
        cpath = os.path.join(clone, a.counter)
        ctl = a.receipt_dir or os.path.join(os.path.dirname(clone), "probe-receipts")
        os.makedirs(ctl, exist_ok=True)
        receipt = os.path.join(ctl, spec["control"] + ".json")
        cmd = [sys.executable, "-I", "-B", cpath, "--root", clone, "--rev", rev,
               "--freeze", freeze, "--pkg65", a.pkg65, "--json-out", receipt]
        p = subprocess.run(cmd, capture_output=True, text=True)
        out["counter_cmd"] = cmd
        out["counter_exit"] = p.returncode
        out["counter_stdout"] = p.stdout.strip()
        out["counter_stderr"] = p.stderr.strip()
        out["expected_exit"] = spec["expected"]["exit"]
        out["verdict"] = ("as-expected" if p.returncode == spec["expected"]["exit"]
                          else "CONTROL-DEFEATS-COUNTER" if p.returncode == 0
                          else "unexpected-exit")
        out["counter_receipt"] = receipt

    print(json.dumps(out, indent=1, sort_keys=True))
    if a.json_out:
        json.dump(out, open(a.json_out, "w"), indent=1, sort_keys=True)
    if not a.skip_counter and out.get("verdict") != "as-expected":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
