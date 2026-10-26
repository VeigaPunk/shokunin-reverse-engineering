#!/usr/bin/env python3
"""registry-body-reach.py -- does every evidence body a registry row cites live where the
lane can reach and verify it?

Rule checked (all findings fatal):
  1. external-body   : a row cites an absolute path outside the lane root, outside a tool or
                       OS-package channel (`/usr`, `/opt`, `/srv`, `<home>/.local|.agents|.npm|
                       .cache|.config`, `/var/lib|/var/cache`) and outside scratch.  The lane's
                       own checkout cannot contain that body, so the row's sha256 pin cannot be
                       checked from the lane at all.
  2. scratch-body    : a cited body under scratch (`/fast/scratch`, `/tmp`, `/var/tmp`) -- the
                       lane's seat rules delete scratch at exit, so the body is gone by design.
  3. lane-untracked  : a cited lane path (absolute or `corpus|tools|plans|.ufo`-relative) that is
                       neither a blob nor a tree at REV.
  4. pin-mismatch    : a cited lane blob whose bytes hash to something other than the sha256
                       pinned in the same cell.  This is what makes a repair real: a same-named
                       stub stays red.

Surfaces: the SOURCES registry table (columns `source` and `anchor`) and every `source:` line
of a knowledge document.

Exit: 0 no finding; 1 finding; 2 could-not-evaluate (usage, missing/rowless surface, bad rev).

Scratch: none in production; `--selftest` builds its fixtures under TMPDIR and removes them.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROW_RE = re.compile(r"^\|\s*(S\d{3,})\s*\|")
SOURCE_LINE_RE = re.compile(r"^source:\s*(S\d{3,})\s*[—–-]\s*(.*)$")
ABS_PATH_RE = re.compile(r"(?<![\w./-])/(?:[A-Za-z0-9._+@%~-]+/)*[A-Za-z0-9._+@%~-]+")
REL_PATH_RE = re.compile(r"(?<![\w./-])((?:corpus|tools|plans|\.ufo)/[A-Za-z0-9._+@%~/-]+)")
PIN_RE = re.compile(r"sha256\s+([0-9a-fA-F]{64})")
TRAIL = ".,;:)]}>'\"`*"

ABS_ROOTS = re.compile(r"^/(?:home|Users|opt|usr|srv|mnt|media|var|fast|tmp)/")
TOOL_RE = re.compile(
    r"^/(?:usr|opt|srv)/"
    r"|^/(?:home|Users)/[^/]+/\.(?:local|agents|npm|cache|config)/"
    r"|^/var/(?:lib|cache)/"
)
SCRATCH_RE = re.compile(r"^/(?:fast/scratch|tmp|var/tmp)/")


def git(root, *argv):
    p = subprocess.run(["git", "-C", root, *argv],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout, p.stderr


def probe(root, rev, rel):
    """('blob', bytes) | ('tree', None) | (None, None)."""
    rc, out, _ = git(root, "cat-file", "blob", "%s:%s" % (rev, rel))
    if rc == 0:
        return "blob", out
    rc, out, _ = git(root, "cat-file", "tree", "%s:%s" % (rev, rel))
    if rc == 0:
        return "tree", None
    return None, None


def classify(root, path):
    real = os.path.realpath(path)
    if real == root or real.startswith(root + os.sep):
        return "lane", os.path.relpath(real, root)
    if TOOL_RE.search(path):
        return "tool", None
    if SCRATCH_RE.search(path):
        return "scratch", None
    return "external", None


def pointers_in(text, origin, root):
    taken = []
    for m in ABS_PATH_RE.finditer(text):
        path = m.group(0).rstrip(TRAIL)
        if not ABS_ROOTS.match(path):
            continue
        if any(t[0] == "abs" and path.startswith(t[1] + "/") for t in taken):
            continue
        taken.append(("abs", path, m.start()))
    for m in REL_PATH_RE.finditer(text):
        rel = m.group(1).rstrip(TRAIL + "/")
        if any(t[0] == "abs" and t[1].endswith("/" + rel) for t in taken):
            continue
        taken.append(("rel", rel, m.start()))
    taken.sort(key=lambda t: t[2])

    obs = []
    for idx, (kind_s, value, pos) in enumerate(taken):
        end = taken[idx + 1][2] if idx + 1 < len(taken) else len(text)
        # A pin binds only to the text immediately after its path: same clause (no `;`),
        # close (<=120 chars), and before any URL that would own the digest instead.
        span = text[pos:end]
        cut = span.find(";")
        if cut >= 0:
            span = span[:cut]
        url_at = span.find("http")
        pin = None
        if url_at < 0 or url_at > 120:
            m = PIN_RE.search(span[:len(value) + 120])
            if m:
                pin = m.group(1).lower()
        if kind_s == "abs":
            kind, rel = classify(root, value)
        else:
            kind, rel = "lane", value
        obs.append({"origin": origin, "path": value, "kind": kind, "rel": rel,
                    "pin": pin})
    return obs


def check(root, rev, sources_rel, knowledge_glob):
    src_path = os.path.join(root, sources_rel)
    if not os.path.isfile(src_path):
        raise ValueError("missing surface %s" % src_path)

    rows = 0
    obs_all = []
    with open(src_path, "r", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            m = ROW_RE.match(line)
            if not m:
                continue
            rows += 1
            cells = line.split("|")
            text = " | ".join(cells[2:4] + cells[6:7]) if len(cells) > 6 else line
            obs_all += pointers_in(text, "%s:%d %s" % (sources_rel, lineno, m.group(1)), root)

    for kpath in sorted(glob.glob(os.path.join(root, knowledge_glob))):
        krel = os.path.relpath(kpath, root)
        with open(kpath, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                sm = SOURCE_LINE_RE.match(line)
                if not sm:
                    continue
                obs_all += pointers_in(line, "%s:%d %s" % (krel, lineno, sm.group(1)), root)

    if rows == 0:
        raise ValueError("rowless surface %s" % sources_rel)

    tallies = {"lane": 0, "tool": 0, "scratch": 0, "external": 0}
    findings = []
    for ob in obs_all:
        tallies[ob["kind"]] += 1
        if ob["kind"] == "external":
            findings.append(dict(ob, cls="external-body",
                                 why="body outside the lane and outside any re-obtainable channel"))
        elif ob["kind"] == "scratch":
            findings.append(dict(ob, cls="scratch-body",
                                 why="body under scratch, which the lane deletes at seat exit"))
        elif ob["kind"] == "lane":
            typ, blob = probe(root, rev, ob["rel"])
            if typ is None:
                findings.append(dict(ob, cls="lane-untracked",
                                     why="cite is not a blob or tree at %s" % rev[:12]))
                continue
            if typ == "blob" and ob["pin"]:
                got = hashlib.sha256(blob).hexdigest()
                if got != ob["pin"]:
                    findings.append(dict(ob, cls="pin-mismatch",
                                         why="blob %s != row pin %s"
                                             % (got[:12], ob["pin"][:12])))
    meta = {"rows": rows, "pointers": len(obs_all), "tallies": tallies, "rev": rev}
    return findings, meta


def emit(findings, meta, as_json):
    if as_json:
        print(json.dumps({"findings": findings, "meta": meta}, indent=1, sort_keys=True))
        return
    t = meta["tallies"]
    print("rows=%d pointers=%d lane=%d tool=%d scratch=%d external=%d rev=%s"
          % (meta["rows"], meta["pointers"], t["lane"], t["tool"], t["scratch"],
             t["external"], meta["rev"][:12]))
    for f in findings:
        print("FATAL %-14s %-42s sha=%s %s"
              % (f["cls"], f["origin"], (f["pin"] or "-")[:12], f["path"]))
    print("findings=%d" % len(findings))


# ---------------------------------------------------------------- selftest

HEAD = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n")


def fx_repo(tmp, name):
    d = os.path.join(tmp, name)
    os.makedirs(os.path.join(d, "corpus", "knowledge"), exist_ok=True)
    subprocess.run(["git", "init", "-q", d], check=True)
    rc, out, _ = git(d, "rev-parse", "--show-toplevel")
    if rc != 0 or os.path.realpath(out.decode().strip()) != os.path.realpath(d):
        raise SystemExit("crr: fixture toplevel mismatch at %s" % d)
    return d


def fx_commit(d, msg):
    for extra in (["add", "-A"], ["commit", "-q", "-m", msg]):
        subprocess.run(["git", "-C", d, "-c", "user.name=fx", "-c", "user.email=fx@fx", *extra],
                       check=True)
    rc, out, _ = git(d, "rev-parse", "HEAD")
    return out.decode().strip()


def fx_write(d, rel, text):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p) or d, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def fx_bytes(d, rel, data):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p) or d, exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(data)
    return hashlib.sha256(data).hexdigest()


def row(source, anchor):
    return ("| S900 | %s | own-work | A | scope text | %s | teaches text | mined |"
            " 2026-10-26 | 180d | corpus/knowledge/k.md |\n" % (source, anchor))


def run(d):
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--root", d,
                        "--rev", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode()


def selftest(tmp):
    cases = []

    def case(name, want, d):
        got, out = run(d)
        cases.append((name, want, got, out.strip().splitlines()[-1] if out.strip() else ""))

    d = fx_repo(tmp, "c1")
    fx_write(d, "corpus/SOURCES.md",
             HEAD + row("/home/x/otherproject/work/a.tsv (sha256 %s)" % ("a" * 64), "-"))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — x\n")
    fx_commit(d, "c1")
    case("external sibling body is fatal", 1, d)

    d = fx_repo(tmp, "c2")
    sha = fx_bytes(d, "corpus/evidence/r/body.bin", b"body-bytes\n")
    fx_write(d, "corpus/SOURCES.md",
             HEAD + row("lane copy `corpus/evidence/r/body.bin`", "sha256 %s" % sha))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — lane\n")
    fx_commit(d, "c2")
    case("tracked lane copy with matching pin is clean", 0, d)

    d = fx_repo(tmp, "c3")
    want = hashlib.sha256(b"true-body\n").hexdigest()
    fx_bytes(d, "corpus/evidence/r/body.bin", b"stub-substitute\n")
    fx_write(d, "corpus/SOURCES.md",
             HEAD + row("lane copy `corpus/evidence/r/body.bin`", "sha256 %s" % want))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — lane\n")
    fx_commit(d, "c3")
    case("stub with the right name stays red", 1, d)

    d = fx_repo(tmp, "c4")
    fx_write(d, "corpus/SOURCES.md",
             HEAD + row("lane copy `corpus/evidence/r/missing.bin`", "sha256 %s" % ("b" * 64)))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — lane\n")
    fx_commit(d, "c4")
    case("lane path absent from the revision is fatal", 1, d)

    d = fx_repo(tmp, "c5")
    fx_write(d, "corpus/SOURCES.md",
             HEAD + row("/fast/scratch/hyaku/r41/x/body.bin", "sha256 %s" % ("c" * 64)))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — scratch\n")
    fx_commit(d, "c5")
    case("scratch body is fatal", 1, d)

    d = fx_repo(tmp, "c6")
    fx_write(d, "corpus/SOURCES.md",
             HEAD + row("`/home/u/.local/opt/tool/lib/x.c`", "sha256 %s" % ("d" * 64)))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — tool\n")
    fx_commit(d, "c6")
    case("installed tool path is not a finding", 0, d)

    d = fx_repo(tmp, "c7")
    fx_write(d, "corpus/SOURCES.md", HEAD + row("https://example.invalid/a.txt", "-"))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — https://example.invalid/a.txt\n")
    fx_commit(d, "c7")
    case("URL-only row is clean", 0, d)

    d = fx_repo(tmp, "c8")
    fx_write(d, "corpus/SOURCES.md", HEAD + row("https://example.invalid/a.txt", "-"))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — /home/x/sibling/work/b.tsv\n")
    fx_commit(d, "c8")
    case("knowledge lineage pointer is scored", 1, d)

    d = fx_repo(tmp, "c9")
    fx_write(d, "corpus/SOURCES.md", "no table here\n")
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — x\n")
    fx_commit(d, "c9")
    case("rowless surface is could-not-evaluate", 2, d)

    d = fx_repo(tmp, "c10")
    fx_bytes(d, "corpus/evidence/r/one.bin", b"1\n")
    fx_write(d, "corpus/SOURCES.md", HEAD + row("`corpus/evidence/r/` (dir cite)", "-"))
    fx_write(d, "corpus/knowledge/k.md", "source: S900 — lane dir\n")
    fx_commit(d, "c10")
    case("tracked lane directory citation is clean", 0, d)

    bad = 0
    for name, want, got, tail in cases:
        ok = want == got
        bad += 0 if ok else 1
        print("%s want=%d got=%d %-45s %s" % ("ok  " if ok else "FAIL", want, got, name, tail))
    print("selftest cases=%d failed=%d" % (len(cases), bad))
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--sources", default="corpus/SOURCES.md")
    ap.add_argument("--knowledge", default="corpus/knowledge/*.md")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        tmp = tempfile.mkdtemp(prefix="crr-selftest-")
        try:
            return selftest(tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    if not a.root:
        print("crr: --root is required", file=sys.stderr)
        return 2
    rc, out, _ = git(a.root, "rev-parse", "--verify", a.rev + "^{commit}")
    if rc != 0:
        print("crr: cannot resolve %s in %s" % (a.rev, a.root), file=sys.stderr)
        return 2
    rev = out.decode().strip()
    try:
        findings, meta = check(a.root, rev, a.sources, a.knowledge)
    except ValueError as e:
        print("crr: %s" % e, file=sys.stderr)
        return 2
    emit(findings, meta, a.json)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
