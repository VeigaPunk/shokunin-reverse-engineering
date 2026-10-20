#!/usr/bin/env python3
"""routed-r18.py — round-19 C1 counting command (kaidoku, L1-authored).

Counts the seven defects routed by corpus/lessons/round-18-verifier-spotcheck.md:191-199 that
are still OPEN at a revision. A defect is closed only when BOTH hold at REV:
  named      `SCORECARD.md` and `corpus/lessons/round-19.md` each carry a line starting
             `- R18-<ID>:` (the append-only named correction);
  substance  a behavioural check that runs code or recomputes digests from REV's Git objects
             (never the working tree, never a token alone; see each _s_* function).
Usage:
  python3 -I -B routed-r18.py --root LANE --rev REV [--strict]
  python3 -I -B routed-r18.py --selftest
Exit: 0 printed (or --strict and open_count 0); 1 --strict with open defects; 2 unusable input.
The live checks read only Git objects of REV plus, for DEADSEAT-RECORD, the fixed round-18
delivered revision a245bb0 (report presence at integration). Tools taken from REV run from a
mkdtemp copy; nothing is written to the lane.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

IDS = ["MIDMAP-LISTSTEP", "VALIDATOR-DIGEST", "STRICT-BASELINE", "HEAD-ALIASES",
       "DEADSEAT-RECORD", "REGISTRY-PINNED", "INSTALL-RECORD"]
B18 = "9011581d84527ba34c675f9cf912e54d2e72d470"
A18 = "a245bb00c581ae3423a10a055c77d4bc873918df"
LESSON = "corpus/lessons/round-19.md"
GO_SHA = {"go1.24.6": "bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712",
          "go1.25.0": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613"}
ALIASES = ["@", "HEAD~0", "HEAD^{commit}", "HEAD@{0}", "@~0", "HEAD^0"]
EV = ".ufo/waves/round-19/evidence"


class Git:
    def __init__(self, root):
        self.root = root

    def run(self, *args, binary=False):
        p = subprocess.run(["git", "--no-optional-locks", "-C", self.root, *args],
                           capture_output=True)
        return p.returncode, (p.stdout if binary else p.stdout.decode("utf-8", "replace"))

    def show(self, rev, path):
        rc, out = self.run("show", "%s:%s" % (rev, path), binary=True)
        return out if rc == 0 else None

    def text(self, rev, path):
        b = self.show(rev, path)
        return None if b is None else b.decode("utf-8", "replace")

    def ls(self, rev, path):
        rc, out = self.run("ls-tree", "--name-only", "%s:%s" % (rev, path))
        return out.split() if rc == 0 else None

    def extract(self, rev, path, dest):
        """git archive REV PATH into dest; returns True on success."""
        rc, out = self.run("archive", "--format=tar", rev, path, binary=True)
        if rc != 0:
            return False
        with tarfile.open(fileobj=io.BytesIO(out)) as t:
            t.extractall(dest, filter="data")
        return True


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    return mod


# ---------------- substance checks: each returns (ok, why) ----------------

def s_midmap(g, rev, tmp):
    if not g.extract(rev, ".ufo/waves/round-17/tools", tmp):
        return False, "round-17/tools absent at REV"
    try:
        mod = load_module(os.path.join(tmp, ".ufo/waves/round-17/tools/receipt-validate.py"), "rv_r18")
    except Exception as e:  # noqa: BLE001 - any import failure is a red result
        return False, "receipt-validate.py does not import: %r" % (e,)
    pc = [{"taken_at_utc": "2026-10-20T00:00:00Z", "equal": True, "entries": 1,
           "changed": [], "missing": []}]
    red = {"steps": [{"argv": ["npx", "-y", "rea-agents@6.5.0", "inspect-go-binary"], "pin_checks": pc},
                     {"argv": ["npx", "-y", "rea-agents@6.5.0", "analyze"]}]}
    green = {"steps": [{"argv": ["npx", "-y", "rea-agents@6.5.0", "inspect-go-binary"]},
                       {"argv": ["npx", "-y", "rea-agents@6.5.0", "analyze"], "pin_checks": pc}]}
    out = {}
    for name, rc in (("red", red), ("green", green)):
        f = []
        try:
            mod.verify_mid_maps(rc, {}, f, require_mid_maps=True)
        except Exception as e:  # noqa: BLE001
            return False, "verify_mid_maps raised on %s fixture: %r" % (name, e)
        out[name] = any(x.get("code") == "mid_checks_absent" for x in f)
    if not out["red"]:
        return False, "list-shaped receipt with pin_checks only on a non-analyze step is accepted"
    if out["green"]:
        return False, "list-shaped receipt with pin_checks on the analyze step is rejected (always-red)"
    return True, "non-analyze-only list receipt -> mid_checks_absent; analyze-carrying list receipt clean"


def s_validator_digest(g, rev, tmp):
    src = g.show(rev, ".ufo/waves/round-18/tools/routed-defects.py")
    if src is None:
        return False, "round-18 routed-defects.py absent at REV"
    p = os.path.join(tmp, "routed_defects_rev.py")
    open(p, "wb").write(src)
    try:
        mod = load_module(p, "rd_rev")
    except Exception as e:  # noqa: BLE001
        return False, "routed-defects.py does not import: %r" % (e,)
    fn = getattr(mod, "_validator_pin", None)
    vrev = getattr(mod, "VALIDATOR_REV", None)
    vpath = getattr(mod, "RECEIPT_VALIDATE", None)
    if fn is None or vrev is None or vpath is None:
        return False, "no _validator_pin/VALIDATOR_REV/RECEIPT_VALIDATE at REV (format-only check)"
    blob = g.show(vrev, vpath)
    if blob is None:
        return False, "pinned validator blob unreadable"
    good = sha(blob)
    wrong = ("0" if good[0] != "0" else "1") + good[1:]
    ok_wrong, _ = fn(g.root, {"validator_rev": vrev, "validator_sha256": wrong})
    ok_good, _ = fn(g.root, {"validator_rev": vrev, "validator_sha256": good})
    if ok_wrong:
        return False, "a well-formed wrong validator_sha256 is accepted"
    if not ok_good:
        return False, "the true validator digest is rejected"
    dj = g.text(rev, EV + "/validate16-remap/digests.json")
    if dj is None:
        return False, "validate16-remap/digests.json absent at REV"
    try:
        doc = json.loads(dj)
    except ValueError:
        return False, "digests.json unparseable"
    copies = doc.get("copies") or []
    if len(copies) != 8:
        return False, "digests.json lists %d copies, want 8" % len(copies)
    if doc.get("validator_sha256") != good:
        return False, "digests.json validator_sha256 != pinned validator blob digest"
    for c in copies:
        b = g.show(rev, "%s/validate16-remap/copies/%s.receipt.json" % (EV, c.get("label")))
        if b is None or sha(b) != c.get("sha256"):
            return False, "copy %s missing or does not re-hash" % c.get("label")
        if c.get("validator_exit") != 0:
            return False, "copy %s validator_exit %r" % (c.get("label"), c.get("validator_exit"))
    return True, "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"


def s_strict_baseline(g, rev, tmp):
    base = EV + "/strict-baseline/" + B18[:12]
    t = g.text(rev, base + ".receipt.json")
    if t is None:
        return False, "strict-baseline receipt for %s absent" % B18[:12]
    try:
        r = json.loads(t)
    except ValueError:
        return False, "receipt unparseable"
    if r.get("rev") != B18 or "--strict" not in (r.get("argv") or []) or r.get("exit") != 1:
        return False, "receipt is not a --strict run at %s with exit 1" % B18
    out = g.show(rev, base + ".stdout.txt")
    err = g.show(rev, base + ".stderr.txt")
    if out is None or sha(out) != r.get("stdout_sha256") or err is None or sha(err) != r.get("stderr_sha256"):
        return False, "retained stdout/stderr do not re-hash to the receipt"
    tool = g.show(r.get("tool_rev") or "", ".ufo/waves/round-18/tools/routed-defects.py")
    if tool is None or sha(tool) != r.get("tool_sha256"):
        return False, "tool_sha256 does not equal the tool blob at tool_rev"
    try:
        doc = json.loads(out)
    except ValueError:
        return False, "retained stdout is not the tool's JSON"
    if not doc.get("open_count"):
        return False, "retained strict stdout reports open_count %r (red baseline needs >0)" % doc.get("open_count")
    return True, "strict run at %s exit 1 (open %s), bytes and tool bound" % (B18[:7], doc.get("open_count"))


def s_head_aliases(g, rev, tmp):
    if not g.extract(rev, ".ufo/gates/citation-drift", tmp):
        return False, "citation-drift gate absent at REV"
    d = os.path.join(tmp, ".ufo/gates/citation-drift")
    probe = os.path.join(d, "citation-drift-probe.py")
    base = [sys.executable, "-I", probe, "--root", g.root, "--table", os.path.join(d, "pointer-table.json"),
            "--expected", os.path.join(d, "expected.json"), "--strict"]
    accepted = []
    for a in ALIASES:
        p = subprocess.run(base + ["--rev", a], capture_output=True, cwd=tmp)
        if p.returncode != 2:
            accepted.append("%s->%d" % (a, p.returncode))
    if accepted:
        return False, "HEAD aliases not refused: " + ", ".join(accepted)
    p = subprocess.run(base + ["--rev", "refs/heads/main"], capture_output=True, cwd=tmp)
    if p.returncode == 2:
        return False, "refs/heads/main also refused (always-red)"
    skill = g.text(rev, "SKILL.md") or ""
    row = [l for l in skill.splitlines() if l.startswith("| head-rev-lint |")]
    if not row or not all(k in row[0] for k in ("round-17/verify.py", "revpin.py", "nested")):
        return False, "head-rev-lint registry row does not register the nested compare-only reads"
    return True, "%d aliases exit 2, refs/heads/main evaluates; lint limit registered" % len(ALIASES)


def s_deadseat(g, rev, tmp):
    want = set()
    for wave in ("wave1", "wave2"):
        reg = g.text(A18, ".ufo/waves/round-18/%s-registration.json" % wave)
        rep = g.ls(A18, ".ufo/waves/round-18/%s" % ("w1" if wave == "wave1" else "w2"))
        if reg is None or rep is None:
            return False, "round-18 %s registration/reports unreadable at a245bb0" % wave
        names = set(json.loads(reg).get("members", {}))
        have = {n[:-3] for n in rep if n.endswith(".md")}
        want |= {(wave, n) for n in names - have}
    t = g.text(rev, EV + "/r18-dead-seats.json")
    if t is None:
        return False, "r18-dead-seats.json absent"
    try:
        seats = json.loads(t).get("seats", [])
    except ValueError:
        return False, "r18-dead-seats.json unparseable"
    got = {(s.get("wave"), s.get("name")) for s in seats}
    if got != want:
        return False, "seats %s != recomputed missing-report set %s" % (sorted(got), sorted(want))
    bad = [s.get("name") for s in seats if not str(s.get("cause") or "").strip()
           or not str(s.get("source") or "").strip()]
    if bad:
        return False, "seats without cause/source: %s" % bad
    return True, "%d seats without a report at a245bb0, each with cause and source" % len(seats)


def s_registry(g, rev, tmp):
    skill = g.text(rev, "SKILL.md")
    if skill is None:
        return False, "SKILL.md absent"
    rc, files = g.run("ls-tree", "-r", "--name-only", rev)
    paths = set(files.split())
    why = []
    for name in ("pins", "go-buildinfo-probe"):
        rows = [l for l in skill.splitlines() if l.startswith("| %s |" % name)]
        if len(rows) != 1:
            why.append("%s: %d rows" % (name, len(rows)))
            continue
        m = re.search(r"Pinned values:(.*)", rows[0])
        cell = m.group(1).split("|")[0] if m else ""
        if "probe; no persisted baseline" in cell:
            continue
        cited = re.findall(r"`?(\.ufo/[^\s`;,()]+|corpus/[^\s`;,()]+)`?", cell)
        if not any(c.rstrip(".:") in paths for c in cited):
            why.append("%s: Pinned values names no path that exists at REV" % name)
    return (not why), ("; ".join(why) or "both rows name an existing path or state no persisted baseline")


def s_install(g, rev, tmp):
    t = g.text(rev, LESSON)
    if t is None:
        return False, "round-19 lesson absent"
    sec = re.search(r"^## Installs[ \t]*\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if sec is None:
        return False, "lesson has no `## Installs` section"
    body = sec.group(1)
    miss = [v for v, h in GO_SHA.items() if v not in body or h not in body]
    if miss or "go.dev" not in body:
        return False, "install record lacks version/full sha256/channel for %s" % (miss or "go.dev channel")
    return True, "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"


SUBSTANCE = {"MIDMAP-LISTSTEP": s_midmap, "VALIDATOR-DIGEST": s_validator_digest,
             "STRICT-BASELINE": s_strict_baseline, "HEAD-ALIASES": s_head_aliases,
             "DEADSEAT-RECORD": s_deadseat, "REGISTRY-PINNED": s_registry, "INSTALL-RECORD": s_install}


def named(g, rev, did):
    out = []
    for path in ("SCORECARD.md", LESSON):
        t = g.text(rev, path) or ""
        out.append(any(l.startswith("- R18-%s:" % did) for l in t.splitlines()))
    return all(out)


def evaluate(root, rev):
    g = Git(root)
    rc, full = g.run("rev-parse", "--verify", "%s^{commit}" % rev)
    if rc != 0:
        raise SystemExit(2)
    full = full.strip()
    defects = []
    for did in IDS:
        tmp = tempfile.mkdtemp(prefix="kr19-routed-")
        try:
            try:
                ok, why = SUBSTANCE[did](g, full, tmp)
            except Exception as e:  # noqa: BLE001 - a crash is an open defect, named
                ok, why = False, "check crashed: %r" % (e,)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        n = named(g, full, did)
        defects.append({"id": "R18-" + did, "named": n, "substance": ok, "why": why})
    return {"rev": full, "open_count": sum(1 for d in defects if not (d["named"] and d["substance"])),
            "named_open": sum(1 for d in defects if not d["named"]),
            "substance_open": sum(1 for d in defects if not d["substance"]), "defects": defects}


def selftest():
    """Fixture repo: copy of nothing but the files the checks read, built per case."""
    fails, cases = [], 0

    def check(cond, msg):
        nonlocal cases
        cases += 1
        if not cond:
            fails.append(msg)

    root = tempfile.mkdtemp(prefix="kr19-routed-selftest-")
    try:
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                   GIT_COMMITTER_EMAIL="t@t")
        for k in list(env):
            if k.startswith("GIT_") and k not in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL",
                                                  "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL"):
                env.pop(k)

        def git(*a):
            return subprocess.run(["git", "-C", root, *a], capture_output=True, env=env, check=True)

        git("init", "-q", "-b", "main")
        open(os.path.join(root, "SCORECARD.md"), "w").write(
            "".join("- R18-%s: token only\n" % i for i in IDS))
        os.makedirs(os.path.join(root, "corpus/lessons"))
        open(os.path.join(root, LESSON), "w").write(
            "".join("- R18-%s: token only\n" % i for i in IDS) + "## Installs\ngo1.24.6 go1.25.0 go.dev\n")
        open(os.path.join(root, "SKILL.md"), "w").write(
            "| pins | probe | x | y | Pinned values: none |\n| go-buildinfo-probe | probe | x | y | Pinned values: constants |\n"
            "| head-rev-lint | gate | nested round-17/verify.py revpin.py |\n")
        git("add", "-A")
        git("commit", "-q", "-m", "tokens")
        doc = evaluate(root, "refs/heads/main")
        check(doc["named_open"] == 0, "token named corrections not recognised")
        check(doc["open_count"] == 7, "token-only fixture closed %d defects" % (7 - doc["open_count"]))
        for d in doc["defects"]:
            check(not d["substance"], "token-only fixture closed substance of %s: %s" % (d["id"], d["why"]))
        # install record green case: full hashes in the Installs section
        open(os.path.join(root, LESSON), "a").write(
            "".join("%s %s\n" % (v, h) for v, h in GO_SHA.items()))
        # registry green case: name an existing path
        open(os.path.join(root, "SKILL.md"), "w").write(
            "| pins | probe | x | y | Pinned values: probe; no persisted baseline |\n"
            "| go-buildinfo-probe | probe | x | y | Pinned values: `corpus/lessons/round-19.md` |\n")
        git("add", "-A")
        git("commit", "-q", "-m", "green install+registry")
        doc = evaluate(root, "refs/heads/main")
        st = {d["id"]: d["substance"] for d in doc["defects"]}
        check(st["R18-INSTALL-RECORD"], "full-hash install record not accepted")
        check(st["R18-REGISTRY-PINNED"], "path/no-baseline registry rows not accepted")
        check(doc["open_count"] == 5, "expected 5 open after two green fixes, got %d" % doc["open_count"])
        # named-correction red: drop the lesson line for INSTALL-RECORD
        t = open(os.path.join(root, LESSON)).read().replace("- R18-INSTALL-RECORD: token only\n", "")
        open(os.path.join(root, LESSON), "w").write(t)
        git("add", "-A")
        git("commit", "-q", "-m", "drop named")
        doc = evaluate(root, "refs/heads/main")
        d = [x for x in doc["defects"] if x["id"] == "R18-INSTALL-RECORD"][0]
        check(not d["named"] and d["substance"], "missing named correction not detected")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    if fails:
        for f in fails:
            print("FAIL:", f)
        print("SELFTEST: FAILED routed-r18 cases=%d fails=%d" % (cases, len(fails)))
        return 1
    print("SELFTEST: CLEAN cases=%d" % cases)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.root or not a.rev:
        ap.error("--root and --rev are required")
    if a.rev in ("HEAD", "@") or a.rev.startswith(("HEAD~", "HEAD^", "HEAD@", "@~", "@^")):
        print("routed-r18: refusing HEAD-derived --rev %r; pass a commit id or refs/heads/main" % a.rev,
              file=sys.stderr)
        return 2
    doc = evaluate(a.root, a.rev)
    print(json.dumps(doc, indent=2, sort_keys=True))
    return 1 if a.strict and doc["open_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
