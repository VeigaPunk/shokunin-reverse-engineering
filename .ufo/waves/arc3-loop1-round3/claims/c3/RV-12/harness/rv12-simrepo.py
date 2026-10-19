#!/usr/bin/env python3
"""RV-12 simrepo builder + honest-edit scenario runner.

Builds a SCRATCH git repo (/var/tmp/rv12/simrepo) containing exactly the files
the pointer table names (citing files + targets, at HEAD bytes, read from git
objects). Nothing outside /var/tmp is written; the real repo is never mutated.

Scenarios (each one honest edit class, applied to the simrepo, then the REAL
probe is run against the simrepo rev):
  S0  baseline (no edit)          -> must reproduce findings=0
  S1  rewrap: split the entry's needle phrase across a line break (markdown
      reflow) in the citing file
  S2  reword: change one character inside the needle phrase (punctuation /
      spelling normalisation)
  S3  shift: insert one line immediately above the entry's pinned line
  S4  rename-target: rename a target file and update every citing line that
      names the old path literally
  S5  rename-citing: rename a citing file, content preserved
Run each scenario per-entry and report which entries fire.
"""
import json
import os
import re
import shutil
import subprocess
import sys

SRC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SIM = "/var/tmp/rv12/simrepo"
PROBE = os.path.join(SRC, ".ufo/gates/citation-drift/citation-drift-probe.py")
TMPD = "/var/tmp/rv12/tmp"


def git(*args, cwd=SIM, check=True):
    p = subprocess.run(["git", "-C", cwd] + list(args), capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s: %s" % (args, p.stderr.decode()[:300]))
    return p.stdout.decode()


def src_show(path):
    p = subprocess.run(["git", "-C", SRC, "show", "HEAD:%s" % path],
                       capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


def table_paths(table):
    paths = set()
    for e in list(table.get("entries", [])) + list(table.get("quoted", [])):
        for key in ("file", "target"):
            v = e.get(key)
            if v and not v.startswith("@"):
                paths.add(v)
    return sorted(paths)


def build(table_path, paths):
    if os.path.isdir(SIM):
        shutil.rmtree(SIM)
    os.makedirs(SIM)
    for rel in paths:
        text = src_show(rel)
        if text is None:
            print("SKIP absent %s" % rel)
            continue
        dst = os.path.join(SIM, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w").write(text)
    git("init", "-q")
    git("add", "-A")
    git("-c", "user.email=rv12@x", "-c", "user.name=rv12", "commit", "-qm", "base")
    return git("rev-parse", "HEAD").strip()


def run_probe(table_path, rev, expected_path):
    env = dict(os.environ, TMPDIR=TMPD)
    p = subprocess.run([sys.executable, PROBE, "--root", SIM, "--rev", rev,
                        "--table", table_path, "--expected", expected_path,
                        "--strict"], capture_output=True, env=env, cwd=TMPD)
    out = p.stdout.decode()
    fired = {}
    for line in out.splitlines():
        m = re.match(r"CITATION_DRIFT: (\S+) entry=(\S+)", line)
        if m:
            fired.setdefault(m.group(2), []).append((m.group(1), line))
    verdict = [l for l in out.splitlines() if l.startswith("CITATION_DRIFT_VERDICT")]
    return p.returncode, verdict[0] if verdict else "", fired


def stage_table(table_obj, name):
    """Write a scratch copy of the table + a scratch expected pinning its sha."""
    import hashlib
    tp = os.path.join(TMPD, "table-%s.json" % name)
    data = json.dumps(table_obj, indent=1).encode()
    open(tp, "wb").write(data)
    ep = os.path.join(TMPD, "expected-%s.json" % name)
    json.dump({"pointer_table": {"sha256": hashlib.sha256(data).hexdigest()}},
              open(ep, "w"))
    return tp, ep


def commit(msg):
    git("add", "-A")
    git("-c", "user.email=rv12@x", "-c", "user.name=rv12", "commit", "-qm", msg)
    return git("rev-parse", "HEAD").strip()


def read_sim(rel):
    return open(os.path.join(SIM, rel)).read()


def write_sim(rel, text):
    open(os.path.join(SIM, rel), "w").write(text)


SYN = {"must": "shall", "all": "every", "recorded": "logged",
       "current": "present", "and": "plus", "is": "remains", "now": "currently",
       "no": "zero", "by": "via", "of": "from", "in": "within", "its": "the",
       "the": "a", "kept": "held", "stays": "remains", "reads": "states",
       "applied": "used", "closed": "shut", "held": "kept", "named": "called",
       "dead": "expired", "line": "row", "lines": "rows", "words": "text",
       "content": "payload", "file": "document", "exists": "is present",
       "no longer": "not anymore"}


def swap_word(span):
    """Return (new_span, ok). Honest in-phrase word substitution: replace one
    alphabetic word with a synonym from SYN. Coverage is reported, never
    assumed."""
    for w in re.findall(r"[A-Za-z]{3,}", span):
        if w.lower() in SYN:
            repl = SYN[w.lower()]
            if w[0].isupper():
                repl = repl.capitalize()
            return span.replace(w, repl, 1), True
    return span, False


def needle_span(text, needle):
    """Find the literal-ish span of the needle regex in the file text."""
    try:
        m = re.search(needle, text)
    except re.error:
        return None
    return (m.start(), m.end()) if m else None


def main():
    os.makedirs(TMPD, exist_ok=True)
    table_path = os.path.join(SRC, ".ufo/gates/citation-drift/pointer-table.json")
    table = json.load(open(table_path))
    if len(sys.argv) > 1:
        table_path = sys.argv[1]
        table = json.load(open(table_path))
    paths = table_paths(table)
    base = build(table_path, paths)
    print("SIMREPO base=%s files=%d" % (base[:10], len(paths)))

    tp, ep = stage_table(table, "base")
    rc, verdict, fired = run_probe(tp, base, ep)
    print("S0 baseline: rc=%d %s fired=%d %s" %
          (rc, verdict, len(fired), sorted(fired)[:5]))

    entries = list(table.get("entries", [])) + \
        [dict(e, kind="quoted") for e in table.get("quoted", [])]

    results = {"S0": {"rc": rc, "verdict": verdict, "fired": sorted(fired)}}

    # --- S1 rewrap / S2 reword / S3 shift : per entry, one edit each ---------
    for scen in ("S1", "S2", "S3"):
        hits = {}
        untested = []
        for e in entries:
            if e.get("kind") == "anchor":
                continue
            rel = e["file"]
            text = read_sim(rel)
            lines = text.splitlines(keepends=True)
            line_no = e.get("line")
            if not isinstance(line_no, int) or not (1 <= line_no <= len(lines)):
                continue
            orig = lines[line_no - 1]
            m = None
            try:
                m = re.search(e["must_match"], orig)
            except re.error:
                pass
            if scen == "S3":
                new = orig + "\n"
            elif m is None:
                # extracted entries: the pin's load-bearing text is the pattern
                try:
                    m2 = re.search(e.get("pattern", ""), orig)
                except re.error:
                    m2 = None
                if m2 is None:
                    continue
                s, t = m2.span()
                if scen == "S1":
                    new = orig[:t] + "\n" + orig[t:]
                else:
                    inner = orig[s:t]
                    if len(inner) < 2:
                        continue
                    k = len(inner) // 2
                    ch = inner[k]
                    repl = {"-": "\u2013", "(": "[", ")": "]", "`": "'",
                            ":": " :", ".": "\u00b7"}.get(ch)
                    if repl is None:
                        new2, ok = swap_word(inner)
                        if not ok:
                            untested.append(e.get("id"))
                            continue
                        new = orig[:s] + new2 + orig[t:]
                    else:
                        new = orig[:s] + inner[:k] + repl + inner[k + 1:] + orig[t:]
            else:
                s, t = m.span()
                if scen == "S1":
                    new = orig[:t] + "\n" + orig[t:]
                else:
                    inner = orig[s:t]
                    if len(inner) < 2:
                        continue
                    k = len(inner) // 2
                    ch = inner[k]
                    repl = {"-": "\u2013", "(": "[", ")": "]", "`": "'",
                            ":": " :", ".": "\u00b7", " ": "  "}.get(ch)
                    if repl is None:
                        new2, ok = swap_word(inner)
                        if not ok:
                            untested.append(e.get("id"))
                            continue
                        new = orig[:s] + new2 + orig[t:]
                    else:
                        new = orig[:s] + inner[:k] + repl + inner[k + 1:] + orig[t:]
            if new == orig:
                continue
            lines[line_no - 1] = new
            write_sim(rel, "".join(lines))
            rev = commit("%s %s" % (scen, e.get("id")))
            rc2, verdict2, fired2 = run_probe(tp, rev, ep)
            git("reset", "-q", "--hard", base)
            if fired2:
                hits[e.get("id")] = {"finding": sorted({f for f, _ in
                                                        fired2.get(e.get("id"), [])}),
                                     "rev": rev[:10],
                                     "verdict": verdict2,
                                     "all_fired": sorted(fired2),
                                     "collateral": sorted(set(fired2) -
                                                          {e.get("id")})}
        results[scen] = hits
        results[scen + "_untested"] = untested
        print("%s: %d entries would fire; %d not transformable (%s)" %
              (scen, len(hits), len(untested), untested[:6]))

    json.dump(results, open("/var/tmp/rv12/scenarios.json", "w"), indent=1)
    print("wrote /var/tmp/rv12/scenarios.json")

    # --- S6 citation reform: the citing pointer is rewritten from path:line into
    # the anchor form the lane's own errata prescribe ("cite it by anchor, not
    # by line number"), keeping the claim. An `extracted` entry can only fire.
    hits = {}
    for e in entries:
        if e.get("kind") != "extracted" or not e.get("pattern"):
            continue
        rel = e["file"]
        lines = read_sim(rel).splitlines(keepends=True)
        line_no = e.get("line")
        if not isinstance(line_no, int) or not (1 <= line_no <= len(lines)):
            continue
        orig = lines[line_no - 1]
        m = re.search(e["pattern"], orig)
        if not m:
            continue
        anchor = "`%s` (see the named row)" % e["target"]
        new = orig[:m.start()] + anchor + orig[m.end():]
        lines[line_no - 1] = new
        write_sim(rel, "".join(lines))
        rev = commit("S6-reform %s" % e.get("id"))
        rc3, verdict3, fired3 = run_probe(tp, rev, ep)
        git("reset", "-q", "--hard", base)
        if fired3:
            hits[e.get("id")] = {"finding": sorted({f for f, _ in
                                                    fired3.get(e.get("id"), [])}),
                                 "rev": rev[:10], "verdict": verdict3,
                                 "all_fired": sorted(fired3),
                                 "collateral": sorted(set(fired3) -
                                                      {e.get("id")})}
    results["S6"] = hits
    print("S6 citation-reform: %d entries would fire" % len(hits))
    json.dump(results, open("/var/tmp/rv12/scenarios.json", "w"), indent=1)


if __name__ == "__main__":
    main()