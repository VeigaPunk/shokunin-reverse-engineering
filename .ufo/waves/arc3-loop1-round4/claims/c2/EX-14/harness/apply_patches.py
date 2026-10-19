#!/usr/bin/env python3
"""EX-14 harness: apply C2 patch texts to a scratch copy, then census.

Patch-text format accepted (all fenced blocks in one .md file are tried, in
order; the first block that applies wins for each file target):

  A. unified diff  (--- a/<path> / +++ b/<path> / @@ hunks)
  B. bare hunks    (@@ hunks with no ---/+++ header; target from --default-target)

Apply is content-anchored with a search window, so a stale line number in the
patch text still lands if the context is unique. Every applied hunk is recorded
with its resolved offset. Nothing is written outside --root.
"""
import argparse, os, re, sys, hashlib, shutil

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
DIFF_HDR = re.compile(r"^--- (?:a/)?(\S+)")
FENCE = re.compile(r"^```(\w*)")


def read_blocks(path):
    """Yield (kind, lang, text) for each fenced block; kind='diff'|'other'."""
    out, cur, lang, inblock = [], [], None, False
    for raw in open(path, encoding="utf-8", errors="replace").read().splitlines():
        m = FENCE.match(raw)
        if m and not inblock:
            inblock, lang, cur = True, m.group(1).lower(), []
            continue
        if raw.startswith("```") and inblock:
            out.append((lang, "\n".join(cur)))
            inblock = False
            continue
        if inblock:
            cur.append(raw)
    return out


def parse_unified(text):
    """-> list of (target, [(ctx_start, old_lines, new_lines, raw_old, raw_new)])"""
    files, target, hunks = [], None, None
    for line in text.splitlines():
        m = DIFF_HDR.match(line)
        if m:
            target = m.group(1)
            hunks = []
            files.append((target, hunks))
            continue
        m = HUNK.match(line)
        if m:
            if hunks is None:
                hunks = []
                files.append((None, hunks))
            hunks.append({"start": int(m.group(1)), "old": [], "new": []})
            continue
        if not hunks:
            continue
        h = hunks[-1]
        if line.startswith("\\"):
            continue
        if line.startswith("+"):
            h["new"].append(line[1:])
        elif line.startswith("-"):
            h["old"].append(line[1:])
        elif line.startswith(" "):
            h["old"].append(line[1:])
            h["new"].append(line[1:])
        elif line.strip() == "":
            h["old"].append("")
            h["new"].append("")
    return files


def parse_prose(text):
    """RV-4 format: a fenced block whose body carries `-` lines (search) and
    `+` lines (replacement).  Target file from a `# file: <path>` line, a
    `# <path>` comment, or a `path` mention introducing the fence.

    A block that carries `@@` markers is split at them, one hunk per section —
    otherwise every `-` line in a multi-hunk block would collapse into a single
    search string that matches nothing.  A block with no `@@` markers stays one
    hunk (the plain RV-4 form).

    -> list of (target_or_None, minus_lines, plus_lines)
    """
    lines = text.splitlines()
    hint_re = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh|json|toml|txt))`")
    out, cur_file, i = [], None, 0
    while i < len(lines):
        m = hint_re.search(lines[i])
        if m:
            cur_file = m.group(1)
        if lines[i].startswith("```"):
            body, j = [], i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                body.append(lines[j])
                j += 1
            hint = cur_file
            for b in body[:3]:
                if b.startswith("# file:"):
                    hint = b.split(":", 1)[1].strip()
                elif b.startswith("# ") and "/" in b:
                    hint = b[2:].strip().split()[0].rstrip(":")
            sections = []
            cur = []
            for b in body:
                if b.startswith("@@"):
                    if cur:
                        sections.append(cur)
                    cur = []
                    continue
                cur.append(b)
            if cur:
                sections.append(cur)
            for sec in sections:
                minus = [b[1:] for b in sec if b.startswith("-") and not b.startswith("---")]
                plus = [b[1:] for b in sec if b.startswith("+") and not b.startswith("+++")]
                if minus and plus:
                    out.append((hint, minus, plus))
            i = j + 1
            continue
        i += 1
    return out


def apply_prose(root, hunks, dry_run=False):
    """Apply content-anchored `-`/`+` hunks. Returns (n_ok, n_fail, notes).
    `dry_run=True` resolves and reports every hunk but writes nothing."""
    notes, n_ok, n_fail = [], 0, 0
    for idx, (hint, minus, plus) in enumerate(hunks, 1):
        if not hint:
            notes.append("  hunk %d: no target file named" % idx)
            n_fail += 1
            continue
        f = os.path.basename(hint)
        path = os.path.join(root, f)
        if not os.path.isfile(path):
            notes.append("  hunk %d [%s]: not in scratch tree" % (idx, hint))
            n_fail += 1
            continue
        src = open(path, encoding="utf-8").read()
        search, repl = "\n".join(minus), "\n".join(plus)
        n = src.count(search)
        if n == 0:
            notes.append("  hunk %d [%s]: search text not found verbatim" % (idx, hint))
            n_fail += 1
            continue
        if n > 1:
            notes.append("  hunk %d [%s]: search text ambiguous (%d occurrences)" % (idx, hint, n))
            n_fail += 1
            continue
        if dry_run:
            notes.append("  hunk %d [%s]: WOULD apply (%d - / %d +) [dry-run, not written]"
                         % (idx, hint, len(minus), len(plus)))
            n_ok += 1
            continue
        open(path, "w", encoding="utf-8").write(src.replace(search, repl, 1))
        notes.append("  hunk %d [%s]: applied (%d - / %d +)" % (idx, hint, len(minus), len(plus)))
        n_ok += 1
    return n_ok, n_fail, notes


def apply_hunks(lines, hunks, window=400):
    """Content-anchored apply. Returns (newlines, offsets)."""
    ops = []
    for h in hunks:
        old = h["old"]
        if not old:
            continue
        anchor = h["start"] - 1
        lo = max(0, anchor - window)
        hi = min(len(lines), anchor + window + 1)
        cand = None
        # prefer the declared position, then widen
        for start in range(lo, hi):
            if lines[start:start + len(old)] == old:
                cand = start
                break
        if cand is None:
            # global search
            for start in range(0, len(lines) - len(old) + 1):
                if lines[start:start + len(old)] == old:
                    cand = start
                    break
        if cand is None:
            raise SystemExit("HUNK-NOT-FOUND @@ -%d: %r" % (h["start"], old[:3]))
        ops.append((cand, len(old), h["new"], cand - (h["start"] - 1)))
    ops.sort(key=lambda o: o[0])
    # overlap check
    for a, b in zip(ops, ops[1:]):
        if a[0] + a[1] > b[0]:
            raise SystemExit("HUNK-OVERLAP at %d" % b[0])
    out, cur, offs = [], 0, []
    for start, nold, new, off in ops:
        out.extend(lines[cur:start])
        out.extend(new)
        offs.append(off)
        cur = start + nold
    out.extend(lines[cur:])
    return out, offs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--patch", action="append", default=[])
    ap.add_argument("--default-target")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for p in args.patch:
        blocks = read_blocks(p)
        applied_any = False
        whole = open(p, encoding="utf-8", errors="replace").read()
        # RV-4 semantics: a file is applied as EITHER a prose patch (fenced
        # -/+ hunks) OR a unified diff — never both, so a unified diff whose
        # fenced block also matches the prose parser is not double-applied.
        prose = parse_prose(whole)
        if prose:
            n_ok, n_fail, notes = apply_prose(args.root, prose, dry_run=args.dry_run)
            for n in notes:
                print("PROSE %s: %s" % (os.path.basename(p), n))
            print("PROSE %s: applied=%d failed=%d" % (os.path.basename(p), n_ok, n_fail))
            if n_ok:
                applied_any = True
            if not applied_any:
                print("NO-APPLICABLE-BLOCK %s" % p)
            continue
        # -- unified diff ---------------------------------------------------
        for lang, text in blocks:
            files = parse_unified(text)
            if not any(h for _, h in files):
                continue
            for target, hunks in files:
                tgt = target or args.default_target
                if not tgt:
                    print("SKIP %s: bare hunks, no --default-target" % p)
                    continue
                tgt = os.path.basename(tgt)
                fpath = os.path.join(args.root, tgt)
                if not os.path.exists(fpath):
                    print("SKIP %s: no such scoped file %s" % (p, fpath))
                    continue
                lines = open(fpath, encoding="utf-8").read().splitlines()
                try:
                    new, offs = apply_hunks(lines, hunks)
                except SystemExit as ex:
                    print("FAIL %s -> %s: %s" % (p, tgt, ex))
                    continue
                print("APPLY %s -> %s: %d hunks, offsets %s, lines %d -> %d"
                      % (p, tgt, len(offs), offs, len(lines), len(new)))
                if not args.dry_run:
                    open(fpath, "w", encoding="utf-8").write("\n".join(new) + "\n")
                applied_any = True
        if not applied_any:
            print("NO-APPLICABLE-BLOCK %s" % p)


if __name__ == "__main__":
    main()
