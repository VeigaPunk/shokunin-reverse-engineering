#!/usr/bin/env python3
"""RV-11 independent arc3-era citation census.

Enumerates citations of operator-mutable files introduced by the arc3-loop1
rounds 1-2 commits (work + records), mechanically, from `git show --unified=0`
added lines, and classifies each by rule #11 conformance:

  CONFORM-KEY     content key present, no line-number token
  CONFORM-STAMP   line-number token, but a capture stamp / named receipt in context
  BARE            line-number token into an operator-mutable file, no stamp/receipt
  NOTE-ONLY       the OM file is named without a line number (no pin at all)

Usage: arc3-citation-census.py --root REPO --revs H1 H2 ... [--json OUT]
"""
import argparse, json, re, subprocess, sys

OM = (r"(?:~|/home/vgpnk)/\.kimi-code/config\.toml|\bconfig\.toml|"
      r"(?:~|/home/vgpnk)/\.config/devin/mcp_config\.json|\bmcp_config\.json|"
      r"(?:~|/home/vgpnk)/\.omp/agent/mcp\.json|\bmcp\.json|"
      r"(?:~|/home/vgpnk)/\.bashrc|\b\.bashrc|"
      r"(?:~|/home/vgpnk)/\.profile|\b\.profile")
OM_TOKEN = re.compile(r"(%s)\s*:(\d+)(?:\s*-\s*(\d+))?" % OM)
OM_BARE = re.compile(OM)
KEY = re.compile(r"\[mcp_servers\.[a-z_]+\]|\bargs\b|rea-agents@\d|\bREA_[A-Z_]+\b|"
                 r"GHIDRA_INSTALL_DIR|JAVA_HOME|startup_timeout_sec")
STAMP = re.compile(r"\b\d{2}:\d{2}(?::\d{2})?Z\b|\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\b|receipt")


def added_lines(root, rev):
    p = subprocess.run(["git", "-C", root, "show", "--unified=0", "--format=", rev],
                       capture_output=True, text=True)
    cur = None
    out = []
    for line in p.stdout.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            out.append((cur, line[1:]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revs", nargs="+", required=True)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    hits = []
    for rev in a.revs:
        for path, line in added_lines(a.root, rev):
            if not line.strip():
                continue
            for m in OM_TOKEN.finditer(line):
                ctx = line
                cls = "CONFORM-STAMP" if STAMP.search(ctx) else "BARE"
                if not OM_TOKEN.search(line) and KEY.search(ctx):
                    cls = "CONFORM-KEY"
                hits.append({"rev": rev, "path": path, "class": cls,
                             "token": m.group(0), "text": line.strip()[:160]})
            if OM_BARE.search(line) and not OM_TOKEN.search(line):
                cls = "CONFORM-KEY" if KEY.search(line) else ("CONFORM-STAMP" if STAMP.search(line) else "NOTE-ONLY")
                hits.append({"rev": rev, "path": path, "class": cls,
                             "token": OM_BARE.search(line).group(0),
                             "text": line.strip()[:160]})
    # dedupe identical (path,text,class)
    seen, uniq = set(), []
    for h in hits:
        k = (h["path"], h["text"], h["class"])
        if k not in seen:
            seen.add(k)
            uniq.append(h)
    import collections
    counts = collections.Counter(h["class"] for h in uniq)
    out = {"revs": a.revs, "hits": len(uniq), "counts": dict(counts), "rows": uniq}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    print("arc3-era OM citations: %d  %s" % (len(uniq), dict(counts)))
    for h in uniq:
        print("[%s] %s: %s" % (h["class"], h["path"], h["text"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())