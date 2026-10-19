#!/usr/bin/env python3
"""SC-2 independent cross-check of MANIFEST.draft (arc3-loop1-round1, chain c1).

Usage: manifest-crosscheck5.py <manifest> <wave-root> [<repo-root>] [<audit-root>]

Verifies, independently of sha256sum (hashlib.sha256), every listed entry:
  SHA256  SIZE_BYTES  MTIME_UTC  PATH      (path relative to wave root)
  footer: generator|check-file|verify-log  <hex>  <path>
  section-2 live custody lines:  <hex>  /abs/path

Header cross-checks:
  # entries: N total-bytes: B vanished-during-scan: V
    -> N vs section-1 row count; B vs sum of section-1 SIZE_BYTES
Declared-scope audit:
  section 1b `roots:` paths are treated as declared exclusions (EX-14 excludes
  seat-local _scratch/ trees); every other in-scope file present but unlisted
  is flagged, classified by **ctime** (copy-preserved mtimes are not reliable:
  a `cp -a` keeps an old mtime; ctime is the write-instant proxy).
Exit 0 iff listed entries all resolve+match, header counts agree, and no
undeclared unlisted in-scope file exists.
"""
import hashlib
import os
import re
import sys
import time

HEX = re.compile(r"\b([0-9a-fA-F]{64})\b")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
DERIVED = {"MANIFEST.draft.txt", "MANIFEST.draft.check.sha256", "verify.log"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def utc(ts):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def parse_line(raw):
    m = HEX.search(raw)
    if not m:
        return None
    digest = m.group(1).lower()
    rest = (raw[: m.start()] + " " + raw[m.end():]).replace("|", " ").replace("`", " ")
    toks = rest.split()
    if not toks:
        return None
    path = toks[-1]
    size = None
    mtime = None
    for t in toks[:-1]:
        if size is None and t.isdigit():
            size = int(t)
        elif mtime is None and ISO.match(t):
            mtime = t
    return path, digest, size, mtime


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    manifest, wave_root = sys.argv[1], sys.argv[2].rstrip("/")
    repo_root = sys.argv[3] if len(sys.argv) > 3 else None
    audit_root = sys.argv[4] if len(sys.argv) > 4 else os.path.join(wave_root, "claims", "c1")
    dirs = [wave_root, repo_root]

    with open(manifest, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    gen = None
    hdr_entries = hdr_bytes = None
    section_of = {}
    declared_excl = []
    cur = "header"
    for i, line in enumerate(lines, 1):
        if line.startswith("# generated-utc:"):
            gen = line.split(":", 1)[1].strip()
        if line.startswith("# entries:"):
            m = re.search(r"entries:\s*(\d+)\s+total-bytes:\s*(\d+)", line)
            if m:
                hdr_entries, hdr_bytes = int(m.group(1)), int(m.group(2))
        if line.startswith("## "):
            cur = line.strip()
        section_of[i] = cur
        if cur.startswith("## section 1b") and "roots:" in line:
            tail = line.split("roots:", 1)[1].strip()
            for tok in tail.split():
                tok = tok.strip()
                if tok in ("none", ""):
                    continue
                if tok.startswith(wave_root):
                    tok = os.path.relpath(tok, wave_root)
                if tok.startswith(".ufo/waves/"):
                    tok = tok.split("/", 3)[3]
                declared_excl.append(tok.rstrip("/"))

    entries, unparsed = [], []
    for i, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        p = parse_line(line)
        if p is None:
            if line.strip():
                unparsed.append((i, line.rstrip()))
            continue
        entries.append((i, *p))

    sec1 = [e for e in entries if section_of[e[0]].startswith("## section 1 ")]
    sum1 = sum(e[3] for e in sec1 if e[3] is not None)

    ok, bad = 0, []
    for lineno, path, digest, size, mtime in entries:
        real = None
        for d in dirs:
            if not d:
                continue
            c = path if os.path.isabs(path) else os.path.join(d, path)
            if os.path.isfile(c):
                real = c
                break
        if real is None:
            bad.append(("MISSING", lineno, path, digest, None, size, None, None, None))
            continue
        st = os.stat(real)
        actual = sha256_file(real)
        amtime, actime = utc(st.st_mtime), utc(st.st_ctime)
        problems = []
        if actual != digest:
            problems.append("digest")
        if size is not None and st.st_size != size:
            problems.append("size")
        if problems:
            bad.append(("MISMATCH", lineno, path, digest, actual, size, st.st_size, amtime, actime))
        else:
            ok += 1
        if mtime and mtime != amtime:
            print(f"MTIME-NOTE line {lineno}: {path} manifest={mtime} actual={amtime}")

    seen = {}
    for lineno, path, *_ in entries:
        seen.setdefault(path, []).append(lineno)
    dups = {p: ls for p, ls in seen.items() if len(ls) > 1}
    by_digest = {}
    for lineno, path, digest, *_ in entries:
        by_digest.setdefault(digest, []).append(path)
    shared = {d: ps for d, ps in by_digest.items() if len(set(ps)) > 1}

    listed = set(seen)
    unlisted, excluded = [], []
    for root, _dirs, files in os.walk(audit_root):
        for name in files:
            if name in DERIVED:
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, wave_root)
            if rel in listed:
                continue
            if any(rel == x or rel.startswith(x + "/") for x in declared_excl):
                excluded.append(rel)
                continue
            st = os.stat(full)
            unlisted.append((rel, st.st_size, utc(st.st_mtime), utc(st.st_ctime)))

    print(f"MANIFEST: {manifest}")
    print(f"generated-utc: {gen}   checked-at: {utc(time.time())}")
    print(f"wave-root: {wave_root}   audit-root: {audit_root}")
    print(f"declared exclusions (section 1b roots): {declared_excl or 'none'}")
    print(f"entries parsed: {len(entries)}  verified: {ok}  problems: {len(bad)}")
    print(f"header check: entries header={hdr_entries} section-1 rows={len(sec1)}"
          f"  {'MATCH' if hdr_entries == len(sec1) else 'MISMATCH'}")
    print(f"header check: total-bytes header={hdr_bytes} section-1 sum={sum1}"
          f"  {'MATCH' if hdr_bytes == sum1 else 'MISMATCH'}")
    for kind, lineno, path, exp, act, esz, asz, amt, act_ in bad:
        print(f"{kind}  line {lineno}: {path}")
        if kind == "MISMATCH":
            print(f"        digest exp {exp}")
            print(f"        digest act {act}")
            print(f"        size   exp {esz} act {asz}")
            print(f"        mtime act {amt}   ctime act {act_}"
                  + ("  POST-GENERATION" if gen and act_ > gen else "  PRE-GENERATION"))
    for p, ls in sorted(dups.items()):
        print(f"DUPLICATE-PATH lines {ls}: {p}")
    for d, ps in sorted(shared.items()):
        print(f"SHARED-DIGEST {d}: {ps}")
    pre_gen = 0
    for rel, sz, mt, ct in sorted(unlisted):
        marker = " POST-GENERATION" if (gen and ct > gen) else " PRE-GENERATION"
        pre_gen += marker == " PRE-GENERATION"
        print(f"UNLISTED-IN-SCOPE: {rel}  {sz}B  mtime={mt} ctime={ct}{marker}")
    print(f"declared-excluded (section 1b): {len(excluded)} files")
    for lineno, line in unparsed:
        print(f"UNPARSED line {lineno}: {line}")

    hdr_ok = hdr_entries == len(sec1) and hdr_bytes == sum1
    clean = not bad and not unlisted and hdr_ok
    print(f"VERDICT: {'PASS' if clean else 'FAIL'} "
          f"(listed={len(entries)} verified={ok} problems={len(bad)} "
          f"unlisted={len(unlisted)} unlisted-pre-generation={pre_gen} "
          f"declared-excluded={len(excluded)} header={'ok' if hdr_ok else 'bad'})")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
