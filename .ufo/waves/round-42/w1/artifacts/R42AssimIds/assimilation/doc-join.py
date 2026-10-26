#!/usr/bin/env python3
"""R42AssimIds — join staged rows to lane registry rows, id and document keys.

Why: the 0-3-space id extractor (`reg-ids` / `staged-ids` / `comm`) only proves
that ids collide. It cannot say whether a colliding staged id names the same
document as the lane row of that id (a real duplicate) or a different one
(positional drift: renumber by document). This join answers that, and emits the
renumber map an adopting round needs.

Three document keys, strongest first; only the first two are verdicts:

  url      the first URL in the `source` cell, unchanged. Equality is the
           `sources-census.sh` duplicate-URL condition (E03/E04), so a hit here
           would be refused by the census gate even though the ids differ.
  source   the whole `source` cell, backticks stripped, whitespace collapsed,
           lower-cased. Equality means the same citation, phrased identically.
  weak     ref-insensitive family: host + URL basename, plus the first two path
           segments for code-hosting hosts. A hit is a HAND-CHECK CANDIDATE,
           never a verdict: round 41 repaired a staged row's URL by pinning a
           commit (`…/binwalk/HEAD/README.md` -> `…/binwalk/<sha>/README.md`),
           so a held document can sit behind a different ref and both stronger
           keys miss it.

Output TSV columns:
  staged_id  registry_id  source_verdict  url_match  weak_matches  source  url  weak_key
source_verdict: drift-different-document (the id is reused by another document:
renumber by document), same-document (the staged id already names this
document), new-document (no registry row carries this source cell).

Usage: doc-join.py <registry.md> <staged.md> <out.tsv>
Reads only its two arguments, writes only its third; no temp files.
"""
import re
import sys

ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|(.*)$")
URL = re.compile(r"https?://[^\s`)\]]+")
REF_HOSTS = ("raw.githubusercontent.com", "github.com", "gitlab.com",
             "android.googlesource.com", "media.githubusercontent.com")


def rows(path):
    """id -> source cell, first occurrence wins; 0-3 leading spaces per census."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.rstrip("\n"))
            if not m:
                continue
            cells = m.group(2).split("|")
            if len(cells) < 2:
                continue
            out.setdefault(m.group(1), cells[0].strip())
    return out


def norm(source):
    """Citation identity: strip backtick decoration, collapse whitespace, lower."""
    return re.sub(r"\s+", " ", source.replace("`", "")).strip().lower()


def url_of(source):
    m = URL.search(source.replace("`", ""))
    return m.group(0).rstrip(".,;") if m else ""


def weak_key(source):
    """Ref-insensitive document family, or '' when the cell carries no URL."""
    url = url_of(source)
    if not url:
        return ""
    host, _, path = url.split("://", 1)[1].partition("/")
    parts = [p for p in path.split("/") if p]
    if not parts:
        return host.lower()
    base = parts[-1].lower()
    if host.lower() in REF_HOSTS:
        return "/".join([host.lower()] + [p.lower() for p in parts[:2]] + [base])
    return f"{host.lower()}/{base}"


def main(argv):
    if len(argv) != 4:
        sys.stderr.write(__doc__)
        return 2
    reg, staged, out = argv[1], argv[2], argv[3]
    reg_rows, staged_rows = rows(reg), rows(staged)
    by_doc, by_url, by_weak = {}, {}, {}
    for rid, src in sorted(reg_rows.items()):
        by_doc.setdefault(norm(src), rid)
        url = url_of(src)
        if url:
            by_url.setdefault(url, []).append(rid)
        key = weak_key(src)
        if key:
            by_weak.setdefault(key, []).append(rid)
    lines = ["staged_id\tregistry_id\tsource_verdict\turl_match\tweak_matches\tsource\turl\tweak_key"]
    counts = {"same-document": 0, "drift-different-document": 0, "new-document": 0}
    url_exact = weak_only = 0
    for sid, src in sorted(staged_rows.items()):
        rid = by_doc.get(norm(src), "-")
        if rid == "-":
            verdict = "new-document"
        elif rid == sid:
            verdict = "same-document"
        else:
            verdict = "drift-different-document"
        counts[verdict] += 1
        url = url_of(src)
        umatch = ",".join(by_url.get(url, [])) if url else ""
        umatch = umatch or "-"
        key = weak_key(src)
        weak = ",".join(by_weak.get(key, [])) if key else ""
        weak = weak or "-"
        if umatch != "-":
            url_exact += 1
        elif weak != "-":
            weak_only += 1
        lines.append(f"{sid}\t{rid}\t{verdict}\t{umatch}\t{weak}\t{src}\t{url or '-'}\t{key or '-'}")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"staged={len(staged_rows)} registry={len(reg_rows)} "
          + " ".join(f"{k}={v}" for k, v in counts.items())
          + f" url_duplicates={url_exact} weak_only_candidates={weak_only}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
