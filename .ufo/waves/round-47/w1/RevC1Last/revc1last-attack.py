#!/usr/bin/env python3
"""RevC1Last — attack the `block_is_last` and `24. ` title clauses of tools/round-47/exact.py.

Every case builds its own two-commit fixture repo under $HYAKU_SCRATCH, copies the
lane's byte-identical helper files at REV, mutates ONLY SKILL.md, and runs the FROZEN
counter as a CLI. The lane tree is never written.

    S=/fast/scratch/hyaku/kaidoku-r47/RevC1Last; mkdir -p "$S"
    TMPDIR=$S HYAKU_SCRATCH=$S S=$S python3 -B revc1last-attack.py [--case NAME]

REV is the measured revision whose SKILL.md carries the landed block 24 (62e33f7d at
the time of the seat; the frozen counter is unchanged since the freeze, so any rev
carrying block 24 reproduces the same clause verdicts).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "62e33f7dd75c8e3285967b26419842c106f6c965"
S = os.environ.get("HYAKU_SCRATCH") or os.environ.get("S")
if not S:
    sys.exit("set HYAKU_SCRATCH (or S) to a non-/tmp scratch dir; refusing to build fixtures in cwd")
S = os.path.realpath(S)
for bad in ("/tmp", "/var/tmp"):
    if S == bad or S.startswith(bad + "/"):
        sys.exit("scratch root is a temporary partition: " + S)
if S == os.path.realpath(LANE) or S.startswith(os.path.realpath(LANE) + os.sep):
    sys.exit("scratch root is inside the lane tree: " + S)
os.makedirs(S, exist_ok=True)
FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-47/record.py", "tools/round-46/gate.py",
         "corpus/lessons/round-46.md", "corpus/lessons/round-45.md"]
MARKER = "<!-- exactness-table v3 -->"
CRAFT = "## Queue-drain craft "


def lane_show(path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


base = {p: lane_show(p) for p in FILES}
missing = [p for p, v in base.items() if v is None]
assert not missing, missing
SKILL = base["SKILL.md"]

sec_start = SKILL.index(CRAFT)
sec_end = SKILL.index("\n## ", sec_start + len(CRAFT)) + 1
section = SKILL[sec_start:sec_end]
b_off = section.index("- **24. ")
b_start = sec_start + b_off
nxt = section[b_off + 5:]
cands = [i for i in (nxt.find("\n- **"), nxt.find("\n## ")) if i != -1]
b_end = b_start + 5 + min(cands) if cands else sec_start + len(section)
BLOCK = SKILL[b_start:b_end]
assert BLOCK.startswith("- **24. ") and MARKER in BLOCK
HEADER_LINE = "| trigger | v2 hole | v3 arm | exit |"
assert HEADER_LINE in BLOCK


def span(skill, num):
    start = skill.index(f"- **{num}. ")
    nxt = skill[start + 5:]
    cands = [i for i in (nxt.find("\n- **"), nxt.find("\n## ")) if i != -1]
    return start, (start + 5 + min(cands) if cands else len(skill))


BLOCK23 = SKILL[slice(*span(SKILL, 23))]


def sub(text, old, new):
    assert old in text, old[:60]
    return text.replace(old, new, 1)


def title_nospace(s):   return sub(s, "- **24. ", "- **24.")
def title_dbl(s):       return sub(s, "- **24. ", "- **  24. ")
def title_nbsp(s):      return sub(s, "- **24. ", "- **24.\u00a0")
def title_tab(s):       return sub(s, "- **24. ", "- **24.\t")
def title_dot(s):       return sub(s, "- **24. ", "- **24.** ")
def title_empty(s):     return sub(s, "- **24. ", "- **24. ** ")


def comment_after(s):
    return s[:b_end] + "\n- **<!-- craft section ends here; block 24 is the last rule -->**\n" + s[b_end:]


def bare_dash_after(s):
    return s[:b_end] + "\n- **\n" + s[b_end:]


def comment_before(s):
    return s[:b_start] + "- **<!-- editorial: block 24 follows -->**\n" + s[b_start:]


def dup25_after_nomarker(s):
    dup = BLOCK.replace(MARKER, "").replace("- **24. ", "- **25. ", 1)
    return s[:b_end] + "\n" + dup + "\n" + s[b_end:]


def dup25_after_marker(s):
    dup = BLOCK.replace("- **24. ", "- **25. ", 1)
    return s[:b_end] + "\n" + dup + "\n" + s[b_end:]


def dup25_before(s):
    dup = BLOCK.replace(MARKER, "").replace("- **24. ", "- **25. ", 1)
    return s[:b_start] + dup + "\n" + s[b_start:]


def dup8_before(s):
    dup = BLOCK.replace(MARKER, "").replace("- **24. ", "- **8. ", 1)
    return s[:b_start] + dup + "\n" + s[b_start:]


def indent25_after(s):
    dup = BLOCK.replace(MARKER, "").replace("- **24. ", "- **25. ", 1)
    ind = "\n".join(("  " + l) if l else l for l in dup.splitlines())
    return s[:b_end] + "\n" + ind + "\n" + s[b_end:]


def fence_inside_block(s):
    ins = "```text\n- **24. an example of the table format**\n```\n\n"
    i = BLOCK.index("\n  Refs: ")
    return s[:b_start] + BLOCK[:i + 1] + ins + BLOCK[i + 1:] + s[b_end:]


def fence_hides_25(s):
    hide = ("\n```md\n## Worked example\n```\n\n"
            "- **25. A visibly landed extra rule block.** It follows block 24 in the file.\n")
    return s[:b_end] + hide + s[b_end:]


def continuation_25(s):
    return s[:b_end] + "\n## Queue-drain craft (continued)\n\n- **25. A visible extra craft rule.** body\n" + s[b_end:]


def continuation_dup(s):
    dup = BLOCK.replace(MARKER, "").replace("- **24. ", "- **25. ", 1)
    return s[:b_end] + "\n## Queue-drain craft (continued)\n\n" + dup + s[b_end:]


def eof_25(s):
    return s.rstrip("\n") + "\n\n- **25. A rule block appended at end of file.** body\n"


def fence_table(s):
    out = sub(s, "\n" + HEADER_LINE + "\n", "\n```text\n" + HEADER_LINE + "\n")
    i = out.index("| R46-CL6", out.index(HEADER_LINE))
    j = out.index("\n", i)
    return out[:j] + "\n```" + out[j:]


def fenced_whole_block(s):
    return s[:b_start] + "```md\n" + s[b_start:b_end] + "\n```\n" + s[b_end:]


def unclosed_fence(s):
    return s[:b_start] + "```md\n" + s[b_start:b_end] + "\n" + s[b_end:]


def block23_relabelled(s):
    forged = BLOCK23.replace("- **23. ", "- **24. ", 1)
    i = forged.index("**", 4)
    forged = forged[:i + 2] + " " + MARKER + forged[i + 2:]
    return s[:b_start] + forged + s[b_end:]


def section_in_fence_early(s):
    """A fenced sample of the craft heading + a 24. block at the top of SKILL.md."""
    ins = ("```md\n## Queue-drain craft (excerpt)\n\n"
           "- **24. Sample of the matrix.** " + MARKER + "\n\n"
           "| trigger | v2 hole | v3 arm | exit |\n|---|---|---|---|\n"
           "| R46-CL2 | x | symbol | 1 |\n\n```\n\n")
    return _top(s, ins)


def _top(s, text):
    """Insert `text` immediately before the document's first `## ` heading."""
    k = s.index("\n## ")
    return s[:k + 1] + text + s[k + 1:]


def whole_landing_in_fence_early(s):
    """The whole block 24 moved into a fenced excerpt at the top; no real block 24."""
    stripped = s[:b_start] + s[b_end:]
    ins = "```md\n## Queue-drain craft (excerpt)\n\n" + BLOCK + "\n```\n\n"
    return _top(stripped, ins)


def marker_fenced_early(s):
    return _top(s, "```md\n- **24. Example of a marked block** " + MARKER + "\n```\n\n")


def marker_prose_early(s):
    return _top(s, "A later block carries `" + MARKER + "`.\n\n")


def comment_inside_indented(s):
    i = BLOCK.index("\n  Refs: ")
    return s[:b_start] + BLOCK[:i + 1] + "  <!-- block 24 ends here -->\n" + BLOCK[i + 1:] + s[b_end:]


# (name, what it is, mutator, expected exit under v3 — the claim's own expectation)
CASES = [
    ("genuine", "landed SKILL.md unchanged", lambda s: s, 0),
    ("title-nospace", "`- **24.An exact...` — no space after the number", title_nospace, 1),
    ("title-double-space", "`- **  24. An exact...` — two spaces after the dash", title_dbl, 1),
    ("title-nbsp", "`- **24.<NBSP>An exact...` — NBSP instead of a space", title_nbsp, 1),
    ("title-tab", "`- **24.<TAB>An exact...` — tab instead of a space", title_tab, 1),
    ("title-dot-only", "`- **24.** An exact...` — `24.` with no trailing space", title_dot, 1),
    ("title-empty", "title is exactly `24. ` with no title text", title_empty, 0),
    ("comment-after", "block 24 followed by a comment-only `- **` line", comment_after, 0),
    ("bare-dash-after", "block 24 followed by a bare `- **` line", bare_dash_after, 0),
    ("comment-before", "a comment-only `- **` line immediately BEFORE block 24", comment_before, 0),
    ("comment-inside-indented", "an indented HTML comment inside block 24 (harmless control)", comment_inside_indented, 0),
    ("dup25-after-nomarker", "a 25. block carrying block 24's text (marker stripped), AFTER 24", dup25_after_nomarker, 1),
    ("dup25-after-marker", "a 25. block carrying block 24's text (marker kept), AFTER 24", dup25_after_marker, 1),
    ("dup25-before", "a 25. block carrying block 24's text, BEFORE 24", dup25_before, 0),
    ("dup8-before", "a second copy of block 24's text numbered 8, before 24", dup8_before, 0),
    ("indent25-after", "a 25. copy of block 24 indented two spaces, after 24", indent25_after, 1),
    ("fence-inside-block", "a fenced `- **24. ...**` example inside block 24's own body", fence_inside_block, 0),
    ("fence-hides-25", "fenced `## ` line after 24 truncates the section; a real 25 follows", fence_hides_25, 0),
    ("continuation-25", "a real 25. block under `## Queue-drain craft (continued)` after 24", continuation_25, 0),
    ("continuation-dup", "block 24's own text as 25. under a continuation heading", continuation_dup, 0),
    ("eof-25", "a 25. block appended at end of SKILL.md", eof_25, 0),
    ("fence-table", "the matrix table wrapped in a ```text fence (not a rendered table)", fence_table, 0),
    ("fenced-whole-block", "block 24 entirely inside a ```md fence opened in block 23's tail", fenced_whole_block, 0),
    ("unclosed-fence-whole-block", "same, fence never closed", unclosed_fence, 0),
    ("whole-landing-in-fence-early", "block 24 moved wholesale into a fenced excerpt early in the file; the real craft section keeps 23 blocks", whole_landing_in_fence_early, 0),
    ("section-in-fence-early", "a fenced sample of the `## Queue-drain craft ` heading + a merged 24. block, earlier in the file", section_in_fence_early, 0),
    ("marker-fenced-early", "a fenced example in an early block quoting the marker line", marker_fenced_early, 0),
    ("marker-prose-early", "an early block's prose naming the marker in backticks", marker_prose_early, 0),
    ("block23-relabelled", "block 23's text relabelled `24. ` + marker (the C1 kill rule's case)", block23_relabelled, 1),
]


def commit(d, files, msg, allow_empty=False):
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", msg]
                   + (["--allow-empty"] if allow_empty else []), check=True)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def run(name, desc, fn, expect):
    attacked = fn(SKILL)
    d = subprocess.run(["mktemp", "-d", "-p", S], capture_output=True, text=True).stdout.strip()
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "rev@round47"), ("user.name", "r47 attack")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True).stdout.strip()
        assert top == os.path.realpath(d) or top == d, (top, d)
        freeze = commit(d, base, "base (block 24 as landed)")
        files = dict(base)
        files["SKILL.md"] = attacked
        rev = commit(d, files, f"attack: {name}", allow_empty=(attacked == SKILL))
        cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-47/exact.py"),
               "--root", d, "--freeze", freeze, "--rev", rev, "--no-battery"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout
        try:
            rec = json.loads(out)
        except Exception:
            rec = {"raw": out[:300]}
        utc = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                             capture_output=True, text=True).stdout.strip()
        return {"case": name, "desc": desc, "expect": expect, "exit": r.returncode,
                "ok": r.returncode == expect,
                "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(), "utc": utc,
                "cmd": " ".join(cmd), "freeze": freeze, "rev": rev,
                "block_is_last": rec.get("block_is_last"),
                "block_title": rec.get("block_title"),
                "rule_blocks": rec.get("rule_blocks"),
                "marker_occurrences": rec.get("marker_occurrences"),
                "failing": rec.get("failing") or rec.get("reason")}
    finally:
        shutil.rmtree(d, ignore_errors=True)


ap = argparse.ArgumentParser()
ap.add_argument("--case")
ap.add_argument("--json-out")
args = ap.parse_args()
sel = [c for c in CASES if not args.case or c[0] == args.case]
rows = [run(*c) for c in sel]
for r in rows:
    print(json.dumps({k: r[k] for k in ("case", "exit", "expect", "ok", "block_is_last",
                                        "rule_blocks", "marker_occurrences", "failing")}))
print("cases=%d exceeded_claim_or_missed_expectation=%d" %
      (len(rows), sum(1 for r in rows if not r["ok"])))
if args.json_out:
    json.dump(rows, open(args.json_out, "w"), indent=1)
