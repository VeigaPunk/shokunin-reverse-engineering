#!/usr/bin/env python3
"""CN-2 (arc3-loop1-round4) census projection harness.

Projects the merged records text onto a scratch tree of the three census-scoped
files and runs the landed instrument (.ufo/gates/c1-census-v10.py) over it.

Usage:
  project.py <scratch-root> <merged-section-file> [--skill-patch <patch.md>]
             [--inject <token>]

Appends the literal body (between the BEGIN/END LITERAL markers if present,
else the whole file) to the scratch SCORECARD.md, optionally applies a
registry-row patch text to the scratch SKILL.md, runs the census, and prints a
one-screen verdict. Nothing outside the scratch root is written.
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys

BASE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
CENSUS = BASE / ".ufo/gates/c1-census-v10.py"
SCOPED = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]


def literal_body(path):
    txt = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(r"<!-- BEGIN LITERAL [A-Z ]+ -->\n(.*?)<!-- END LITERAL [A-Z ]+ -->",
                  txt, re.S)
    return m.group(1) if m else txt


def run_census(root):
    p = subprocess.run([sys.executable, str(CENSUS), "--root", str(root), "--json"],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def verdict_line(rc, out):
    try:
        d = json.loads(out)
    except ValueError:
        return "exit=%d UNPARSEABLE-OUTPUT" % rc
    return ("exit=%d verdict=%s stale=%d ambiguous=%d undeclared=%d unresolved=%d "
            "scope_errors=%r unreadable=%r declared=%r current_ok_per_file=%r" % (
                rc, d["verdict"], len(d["stale"]), len(d["ambiguous"]),
                len(d["undeclared"]), len(d["unresolved"]), d["scope_errors"],
                d["unreadable"], d["declared_fail_classes"], d["current_ok_per_file"]))


def apply_unified_diff(root, patch_file, target):
    """Apply the first fenced unified diff in a patch text to root/target."""
    txt = pathlib.Path(patch_file).read_text(encoding="utf-8")
    m = re.search(r"```diff\n(.*?)```", txt, re.S)
    if not m:
        sys.exit("no fenced diff in %s" % patch_file)
    diff = m.group(1)
    p = subprocess.run(["patch", "-p1", "--no-backup-if-mismatch", "-s"],
                       input=diff, text=True, cwd=str(root), capture_output=True)
    if p.returncode != 0:
        sys.exit("patch failed (%d) applying %s to %s: %s" %
                 (p.returncode, patch_file, target, (p.stdout + p.stderr).strip()[:400]))
    print("applied diff from %s to %s (rc=0)" % (pathlib.Path(patch_file).name, target))


def main():
    args = sys.argv[1:]
    root = pathlib.Path(args[0]); root.mkdir(parents=True, exist_ok=True)
    section = pathlib.Path(args[1])
    skill_patch = None
    province_patch = None
    inject = None
    i = 2
    while i < len(args):
        if args[i] == "--skill-patch":
            skill_patch = pathlib.Path(args[i + 1]); i += 2
        elif args[i] == "--province-patch":
            province_patch = pathlib.Path(args[i + 1]); i += 2
        elif args[i] == "--inject":
            inject = args[i + 1]; i += 2
        else:
            sys.exit("unknown arg %r" % args[i])

    for f in SCOPED:
        shutil.copyfile(BASE / f, root / f)

    if province_patch:
        apply_unified_diff(root, province_patch, "PROVINCE.md")

    body = literal_body(section)
    if inject:
        body = body + "\n" + inject + "\n"
    with open(root / "SCORECARD.md", "a", encoding="utf-8") as fh:
        fh.write("\n" + body)

    if skill_patch:
        txt = pathlib.Path(skill_patch).read_text(encoding="utf-8")
        if txt.startswith("---\nname: kaidoku-shokunin"):
            # whole-file patched SKILL.md
            shutil.copyfile(skill_patch, root / "SKILL.md")
            print("replaced SKILL.md from whole-file patch %s" % pathlib.Path(skill_patch).name)
        elif re.search(r"```diff\n", txt):
            apply_unified_diff(root, skill_patch, "SKILL.md")
        else:
            # literal-block replacement of the custody-pair registry row
            m = re.search(r"<!-- BEGIN LITERAL [A-Z ]+ -->\n(.*?)<!-- END LITERAL [A-Z ]+ -->",
                          txt, re.S)
            if not m:
                sys.exit("skill patch has no literal block: %s" % skill_patch)
            new_row = m.group(1).strip("\n")
            skill = (root / "SKILL.md").read_text(encoding="utf-8").splitlines(keepends=True)
            hit = [k for k, ln in enumerate(skill) if "custody-pair" in ln and ln.lstrip().startswith("|")]
            if not hit:
                sys.exit("no custody-pair row found in SKILL.md")
            k = hit[0]
            skill[k] = new_row + "\n"
            (root / "SKILL.md").write_text("".join(skill), encoding="utf-8")

    rc, out = run_census(root)
    print("projection root: %s" % root)
    print("section: %s  (%d lines, sha256 %s)" % (
        section, len(body.splitlines()), hashlib.sha256(body.encode()).hexdigest()[:16]))
    if inject:
        print("injected: %r" % inject)
    print("PROVINCE lines: %d" % len((root / "PROVINCE.md").read_text(encoding="utf-8").splitlines()))
    print("SKILL lines: %d" % len((root / "SKILL.md").read_text(encoding="utf-8").splitlines()))
    print(verdict_line(rc, out))
    print("---- full census output ----")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
