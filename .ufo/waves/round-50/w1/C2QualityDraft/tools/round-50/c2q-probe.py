#!/usr/bin/env python3
"""C2QualityDraft probe (DRAFT, wave 1 of round 50; not frozen, not a lane instrument).

Three read-only checks behind the draft QUALITY rows 90-93 (see the seat report):

  registry  Census of tools/round-<N>/**.{py,sh} (control-fixtures excluded) at REV against the
            cell-0 paths of SKILL.md's `## Local round-evidence gate registry` at REV.
            Row 92 (a counter is registered at landing). Exit 0 all registered, 1 some
            unregistered, 2 could not evaluate.
  locator   For a quote and its snapshot file: the quote must occur contiguously in the
            normalised snapshot text, and the nearest preceding heading (an <hN> element OR a
            man-page section label such as ERRORS, DESCRIPTION) must be the heading the row's
            anchor names. Row 91 (locator names the actual heading). Exit 0 match, 1 mismatch,
            2 quote not found / unreadable.
  selftest  Runs the locator on committed round-49 snapshots (green and red arms) and the
            registry check on a synthetic SKILL.md (green and red arms). Exit 0 when every
            arm gives its expected exit, 1 otherwise.

Normalisation follows corpus/lessons/round-49.md Gate: tags removed (block tags become
spaces), HTML entities decoded, whitespace collapsed.
"""
import argparse
import html
import re
import subprocess
import sys

MAN_LABELS = [
    "NAME", "LIBRARY", "SYNOPSIS", "DESCRIPTION", "RETURN VALUES", "ERRORS", "EXIT STATUS",
    "EXAMPLES", "ENVIRONMENT", "FILES", "SEE ALSO", "HISTORY", "STANDARDS", "CAVEATS",
    "BUGS", "AUTHORS", "COLOPHON", "NOTES", "OPTIONS", "ATTRIBUTES",
]
H_RE = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.S | re.I)


def git_show(root, rev, path):
    r = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git show {rev}:{path} exit {r.returncode}")
    return r.stdout.decode("utf-8", "replace")


def normalise(raw):
    """Return (text, heading_positions) where heading markers are inline `\x01H:<label>\x01`."""
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)

    def hrep(m):
        label = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        return f"\n\x01H:{label}\x01\n"

    s = H_RE.sub(hrep, s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s)
    # man-page section labels rendered as plain words: a label is a known label word-run
    # followed by a capital letter run boundary; we only mark occurrences that are followed
    # by a space and a word starting with a capital or a known token (kept conservative).
    for lab in sorted(MAN_LABELS, key=len, reverse=True):
        s = re.sub(r"(?<=\s)(" + re.escape(lab) + r")(?=\s)", lambda m: f" \x01H:{m.group(1)}\x01 ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def nearest_heading(text, pos):
    hs = re.findall(r"\x01H:(.*?)\x01", text[:pos])
    if not hs:
        return None
    # man7 renders each section heading with a trailing "top" back-link
    return re.sub(r"\s+top$", "", hs[-1]).strip()


def strip_text(text):
    return re.sub(r"\x01H:(.*?)\x01", "", text)


def anchor_names(anchor, heading):
    a = re.sub(r"[`*]", "", anchor).strip().lower()
    h = heading.strip().lower()
    return h in a


def cmd_locator(snapshot_text, quote, anchor):
    text = normalise(snapshot_text)
    plain = strip_text(text)
    # quote must be contiguous in the normalised text (heading markers are removed first)
    q = re.sub(r"\s+", " ", quote).strip()
    idx = plain.find(q)
    if idx < 0:
        return 2, f"quote not found contiguously: {q[:60]!r}", None
    # position in marker-bearing text: find the matching marker-bearing offset
    mpos = 0
    seen = 0
    # walk the marked text, counting plain characters, until plain offset idx
    i = 0
    while seen < idx and i < len(text):
        if text[i] == "\x01":
            j = text.find("\x01", i + 1)
            i = j + 1
            continue
        seen += 1
        i += 1
    mpos = i
    head = nearest_heading(text, mpos)
    if head is None:
        return 1, "no heading precedes the quote", None
    ok = anchor_names(anchor, head)
    return (0 if ok else 1), f"nearest heading {head!r}; anchor {anchor!r}", head


def skill_registry_paths(skill_text):
    # Registry rows live in several sections (`## Local round-evidence gate registry` and
    # per-round `### Round-N ... registry` headings), so every table row counts; a row
    # registers a path only through its cell 0, never through prose.
    paths = set()
    for line in skill_text.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if m:
            paths.add(m.group(1))
    return paths


def cmd_registry(root, rev, min_round):
    files = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--", "tools"],
        capture_output=True, text=True,
    )
    if files.returncode != 0:
        return 2, f"ls-tree exit {files.returncode}", []
    cands = []
    for p in files.stdout.splitlines():
        m = re.match(r"^tools/round-(\d+)/(?!.*control-fixtures/).+\.(py|sh)$", p)
        if m and int(m.group(1)) >= min_round:
            cands.append(p)
    skill = git_show(root, rev, "SKILL.md")
    reg = skill_registry_paths(skill)
    missing = [p for p in cands if p not in reg]
    if not cands:
        return 2, "no candidate tools found", []
    return (1 if missing else 0), f"candidates {len(cands)} registered {len(cands) - len(missing)} unregistered {len(missing)}", missing


def selftest(root, rev):
    results = []

    def check(name, got, want):
        results.append((name, got, want, got == want))

    # locator arms on the committed round-49 SEP/man-page snapshots, read from REV bytes
    # (corpus/evidence/round-49/c2/*.html), never from a scratch copy
    base = "corpus/evidence/round-49/c2/"
    pop = git_show(root, rev, base + "popper.html")
    sys_ = git_show(root, rev, base + "sysexits.html")
    fb = git_show(root, rev, base + "freebsd-sysexits.html")
    q147 = "falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific"
    check("S147 green: §2 heading", cmd_locator(pop, q147, "`2. Backdrop to Popper’s Thought`, the heading above")[0], 0)
    check("S147 red: §3 heading named", cmd_locator(pop, q147, "`3. The Problem of Demarcation`")[0], 1)
    check("S149 red: DESCRIPTION named, quote under ERRORS", cmd_locator(fb, "EX_USAGE (64) The command was used incorrectly", "`DESCRIPTION`")[0], 1)
    check("S149 green: ERRORS named", cmd_locator(fb, "EX_USAGE (64) The command was used incorrectly", "`ERRORS`")[0], 0)
    check("S148 green: SYNOPSIS named", cmd_locator(sys_, "#define EX_USAGE 64 /* command line usage error */", "`SYNOPSIS` heading")[0], 0)
    check("fabricated quote: exit 2", cmd_locator(fb, "EX_USAGE (64) The command was used politely", "`ERRORS`")[0], 2)

    # registry arms on a synthetic SKILL.md
    skill_green = "## Local round-evidence gate registry\n\n| Name | Kind |\n|---|---|\n| `tools/round-49/c1-counter.py` | gate |\n"
    skill_red = "## Local round-evidence gate registry\n\n| Name | Kind |\n|---|---|\n| `tools/round-48/meanings.py` | gate |\n"
    check("registry green arm: path present", "tools/round-49/c1-counter.py" in skill_registry_paths(skill_green), True)
    check("registry red arm: path absent", "tools/round-49/c1-counter.py" in skill_registry_paths(skill_red), False)

    width = max(len(r[0]) for r in results)
    for name, got, want, ok in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}  got={got} want={want}")
    return (0 if all(r[3] for r in results) else 1), f"{sum(r[3] for r in results)}/{len(results)} arms as expected", None


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("registry")
    r.add_argument("--root", required=True)
    r.add_argument("--rev", required=True)
    r.add_argument("--min-round", type=int, default=41)
    l = sub.add_parser("locator")
    l.add_argument("--snapshot", required=True)
    l.add_argument("--quote", required=True)
    l.add_argument("--anchor", required=True)
    s = sub.add_parser("selftest")
    s.add_argument("--root", required=True)
    s.add_argument("--rev", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "registry":
            code, msg, missing = cmd_registry(a.root, a.rev, a.min_round)
            print(msg)
            for p in missing:
                print("UNREGISTERED", p)
        elif a.cmd == "locator":
            code, msg, _ = cmd_locator(open(a.snapshot, encoding="utf-8", errors="replace").read(), a.quote, a.anchor)
            print(msg)
        else:
            code, msg, _ = selftest(a.root, a.rev)
            print(msg)
    except (RuntimeError, OSError) as e:
        print(f"could-not-evaluate: {e}")
        code = 2
    sys.exit(code)


if __name__ == "__main__":
    main()
