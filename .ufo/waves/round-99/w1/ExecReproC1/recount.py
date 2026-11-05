#!/usr/bin/env python3
"""ExecReproC1 independent recount (own script, NOT the frozen counter).

Per revision R in {B0, A, Bk}, all content read via `git -C CLONE show/ls-tree R:...`:
  stems        = basenames (minus .md) of corpus/knowledge/*.md at R
  table rows   = corpus/README.md lines starting '|' inside the '## Coverage map'
                 section (until the next '^## ' heading), >= 3 cells, not a
                 pure separator row
  backticked   = stem S is counted iff some table row contains '`' + S + '`'
  registry     = direct-child *.py of tools/round-97|98|99 at R; pinned iff the
                 blob's full sha256 appears in SKILL.md at R (both: anywhere,
                 and inside a registry-section row whose first cell has the
                 backticked path)
"""
import hashlib, json, os, re, subprocess

CLONE = "/fast/scratch/hyaku/kaidoku-r99/ExecReproC1/clone"
W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ExecReproC1"
REVS = {
    "B0": "de098f51cd73d3b9b4a895840da8f2bb0a386db8",
    "A": "64cc3e10c5d615c6454570674a265b7290b8919c",
    "Bk": "c19d57cd2e65a036478b9e78f6c5397dedfb2bcb",
}


def git_lines(*argv):
    out = subprocess.run(["git", "-C", CLONE, *argv], capture_output=True, check=True)
    return out.stdout.decode().splitlines()


def blob(rev, path):
    return subprocess.run(["git", "-C", CLONE, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout


results = {}
for tag, rev in REVS.items():
    names = git_lines("ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge/")
    stems = sorted(os.path.basename(n)[:-3] for n in names if n.endswith(".md"))
    readme = blob(rev, "corpus/README.md").decode(errors="replace")
    rows, inmap = [], False
    for line in readme.splitlines():
        if line.startswith("## "):
            inmap = line.strip() == "## Coverage map"
            continue
        if inmap and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and not all(set(c) <= set("-: ") for c in cells):
                rows.append(line)

    def row_tokens(line):
        toks = set()
        for span in re.findall(r"`([^`]+)`", line):
            for part in span.split(","):
                p = part.strip()
                if p.startswith("knowledge/"):
                    p = p[len("knowledge/"):]
                if p.endswith(".md"):
                    p = p[:-3]
                if p:
                    toks.add(p)
        return toks

    ticked = sorted(s for s in stems if any(s in row_tokens(r) for r in rows))
    hit_rows = sum(1 for r in rows if row_tokens(r) & set(stems))
    # A3-style residual test, reimplemented: a row only maps its matched stems
    # if what remains after removing them (and pipes/backticks/commas/space)
    # still keeps >= 20 characters (rejects stem-only rows).
    def row_maps_a3(line):
        toks = row_tokens(line) & set(stems)
        if not toks:
            return set()
        rest = line
        for t in toks:
            rest = rest.replace("knowledge/" + t, "").replace(t, "")
        rest = re.sub(r"[\s|`,]", "", rest)
        return toks if len(rest) >= 20 else set()

    ticked_a3 = sorted(s for s in stems if any(s in row_maps_a3(r) for r in rows))
    skill = blob(rev, "SKILL.md").decode(errors="replace")
    at = skill.find("## Local round-evidence gate registry")
    reg = skill[at:] if at >= 0 else ""
    files = []
    for d in ("tools/round-97", "tools/round-98", "tools/round-99"):
        for e in git_lines("ls-tree", "--name-only", rev, "--", d + "/"):
            if e.endswith(".py"):
                files.append(e)
    pinned_any, pinned_row, digests = [], [], {}
    for p in sorted(files):
        hexd = hashlib.sha256(blob(rev, p)).hexdigest()
        digests[p] = hexd
        if hexd in skill:
            pinned_any.append(p)
        for r in reg.splitlines():
            if r.strip().startswith("|") and ("`" + p + "`") in r and hexd in r:
                pinned_row.append(p)
                break
    results[tag] = {
        "rev": rev, "stems": len(stems), "table_rows": len(rows),
        "stems_backticked_in_table_row": len(ticked),
        "stems_backticked_a3style": len(ticked_a3),
        "missing_a3style": sorted(set(stems) - set(ticked_a3)),
        "rows_with_a_backticked_stem": hit_rows,
        "missing_backtick": sorted(set(stems) - set(ticked)),
        "registry_files": len(files),
        "registry_sha_in_skill_anywhere": len(pinned_any),
        "registry_sha_in_own_row": len(pinned_row),
        "registry_missing_own_row": sorted(set(files) - set(pinned_row)),
        "sha256": digests,
    }

with open(os.path.join(W, "recount.json"), "w") as fh:
    json.dump(results, fh, indent=1)
for tag, r in results.items():
    print(f"{tag}: stems {r['stems']} table_rows {r['table_rows']} "
          f"stems_backticked {r['stems_backticked_in_table_row']} "
          f"stems_backticked_a3style {r['stems_backticked_a3style']} "
          f"rows_with_stem {r['rows_with_a_backticked_stem']} "
          f"registry_own_row {r['registry_sha_in_own_row']} of {r['registry_files']} "
          f"registry_anywhere {r['registry_sha_in_skill_anywhere']}")
