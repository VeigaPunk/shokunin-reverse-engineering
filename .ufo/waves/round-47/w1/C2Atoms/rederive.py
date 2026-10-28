#!/usr/bin/env python3
"""C2Atoms independent re-derivation of every R47-C2 atom.

Deliberately does not import record.py or gate.py: every value is recomputed from
raw `git` calls (show/cat-file/ls-tree/rev-parse/merge-base) plus json/re.
"""
import json
import os
import re
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = os.environ.get("C2_REV", "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)


def file_at(path):
    r = git("show", f"{REV}:{path}")
    return r.stdout if r.returncode == 0 else None


def exists(path):
    return git("cat-file", "-e", f"{REV}:{path}").returncode == 0


def main():
    card = file_at("SCORECARD.md")
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", card)]
    secs = []
    for pos, rnd in heads[-2:]:
        end = card.find("\n## ", pos + 1)
        secs.append((rnd, card[pos:end if end >= 0 else len(card)]))
    out = {"rev": REV, "sections": [r for r, _ in secs], "atoms": []}

    # --- seats -------------------------------------------------------------
    def dispatch(rnd):
        spawns = []
        for i in (1, 2, 3, 4):
            body = file_at(f".ufo/waves/round-{rnd}/w{i}-dispatch.json")
            if body is None:
                break
            spawns.append(json.loads(body)["counts"]["spawn"])
        return spawns

    for rnd, text in secs:
        for m in re.finditer(r"Waves?:\s*(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*seats", text):
            claim = tuple(int(x) for x in m.groups())
            d = dispatch(rnd)
            got = (d[0] if d else 0, d[1] if len(d) > 1 else 0, sum(d))
            out["atoms"].append({"class": "seats", "key": rnd, "atom": m.group(0),
                                 "derived": list(got), "ok": claim == got})
        for m in re.finditer(r"Wave 1:\s*(\d+)\s*seats;\s*wave 2:\s*(\d+)\s*seats", text):
            claim = (int(m.group(1)), int(m.group(2)))
            d = dispatch(rnd)
            got = (d[0] if d else 0, d[1] if len(d) > 1 else 0)
            out["atoms"].append({"class": "seats", "key": rnd, "atom": m.group(0),
                                 "derived": list(got), "ok": claim == got})

        # --- window ---------------------------------------------------------
        for line in text.splitlines():
            if "is empty" not in line:
                continue
            m = re.search(r"([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})", line)
            if not m:
                out["atoms"].append({"class": "window", "key": rnd,
                                     "atom": line.strip()[:160],
                                     "derived": "unverifiable: no concrete A..B",
                                     "ok": False})
                continue
            tail = line[m.end():]
            pm = re.findall(r"--\s+([A-Za-z0-9._/ -]+)", tail)
            paths = pm[0].split() if pm else []
            r = git("log", "--name-status", "--format=",
                    f"{m.group(1)}..{m.group(2)}", "--", *paths)
            empty = r.returncode == 0 and r.stdout.strip() == ""
            out["atoms"].append({"class": "window", "key": rnd,
                                 "atom": line.strip()[:160],
                                 "derived": {"window": f"{m.group(1)}..{m.group(2)}",
                                             "pathspec": paths, "empty": empty},
                                 "ok": empty})

        # --- path / rev -----------------------------------------------------
        for m in re.finditer(r"\.ufo/waves/round-[0-9]+/[A-Za-z0-9._/-]*", text):
            tok = m.group(0).rstrip(".,;:)`")
            out["atoms"].append({"class": "path", "key": tok, "atom": tok,
                                 "derived": exists(tok), "ok": exists(tok)})
        for m in re.finditer(r"`([0-9a-f]{7,40})`", text):
            tok = m.group(1)
            e = git("cat-file", "-e", f"{tok}^{{commit}}")
            if e.returncode != 0:
                out["atoms"].append({"class": "rev", "key": tok, "atom": f"`{tok}`",
                                     "derived": "does not resolve", "ok": False})
                continue
            oid = git("rev-parse", f"{tok}^{{commit}}").stdout.strip()
            anc = git("merge-base", "--is-ancestor", oid, REV).returncode == 0
            out["atoms"].append({"class": "rev", "key": tok, "atom": f"`{tok}`",
                                 "derived": {"oid": oid, "ancestor": anc}, "ok": anc})

    # --- axes ---------------------------------------------------------------
    body = card.split("## Owned axes", 1)[1].split("\n## ", 1)[0]
    claimed = {}
    for m in re.finditer(r"(?m)^\|\s*(coverage|depth)\s*\|(.*)$", body):
        f = re.search(r"\b(\d+)/(\d+)\b", m.group(2))
        claimed[m.group(1)] = (int(f.group(1)), int(f.group(2))) if f else None

    # coverage: knowledge files at REV vs tokens in corpus/README.md coverage map
    tree = git("ls-tree", "-r", "--name-only", REV, "--", "corpus/knowledge").stdout
    stems = {os.path.basename(p)[:-3] for p in tree.splitlines() if p.endswith(".md")}
    readme = file_at("corpus/README.md")
    cmap = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    tokens = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", cmap))
    cov = (len(stems & tokens), len(stems))

    # depth: craft rule blocks whose every citation resolves inside its file
    skill = file_at("SKILL.md")
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")
    resolved, detail = 0, []
    for rule in rules:
        refs = REF.findall(rule)
        ok = bool(refs)
        for name, first, last in refs:
            b = file_at(name)
            if b is None:
                ok = False
                detail.append(f"missing {name}")
                break
            if first:
                start, end = int(first), int(last or first)
                if not (1 <= start <= end <= len(b.splitlines())):
                    ok = False
                    detail.append(f"range {name}:{first}-{last} > {len(b.splitlines())}")
                    break
        resolved += ok
    dep = (resolved, len(rules))

    for axis, got in (("coverage", cov), ("depth", dep)):
        out["atoms"].append({"class": "axes", "key": axis,
                             "atom": claimed.get(axis), "derived": list(got),
                             "ok": claimed.get(axis) == got})

    out["counts"] = {"atoms": len(out["atoms"]),
                     "ok": sum(1 for a in out["atoms"] if a["ok"]),
                     "by_class": {c: sum(1 for a in out["atoms"] if a["class"] == c)
                                  for c in ("seats", "window", "path", "rev", "axes")}}
    out["failing"] = [{"class": a["class"], "key": a["key"], "atom": a["atom"],
                       "derived": a["derived"]} for a in out["atoms"] if not a["ok"]]
    out["depth_detail"] = detail
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
