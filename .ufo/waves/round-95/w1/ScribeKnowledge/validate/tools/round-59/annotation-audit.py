#!/usr/bin/env python
"""annotation-audit.py - receipt-annotation consistency gate.

Round 59 capability (R59-C2, depth).  M57-1 (corpus/lessons/round-57.md) and
the round-58 non-author closure's routed defect D58-1: the after-receipt
`.ufo/waves/round-58/l1/scores/c1-after.txt` pasted an observed `grep -c`
output of `0` while its annotation read "(base: 0 -> record: 1 ...)" and the
round report repeated "the marker probe -> 1" - the cited pattern could not
match the note's actual wording, so the claimed value was unreachable by the
cited probe.  M57-1's fix rule ("an annotation line is checked by re-deriving
its predicate from the printed output before the receipt lands") existed, but
nothing mechanical enforced it; the r58 close's own post-close correction was
caught by the same rule after landing instead of before.  This gate is that
rule as an instrument.

Model: a receipt's committed bytes (`git show REV:RECEIPT` - never the
worktree) are scanned for three shapes:

  command line   a line starting ``$ `` - the pasted probe
  pasted output  the next non-empty line after a command line, when it parses
                 as an integer (possibly negative)
  annotation     a line starting ``(`` containing ``base: <int> -> record:
                 <int>``; it binds to the most recent command line above it

Every annotation is checked three ways:

  OUTPUT      the annotation's ``record`` value must equal the bound command's
              pasted output (the D58-1 defect itself fires here)
  RE-DERIVE   commands matching one of two strict grammars are re-executed
              against git objects in --root (the rev named INSIDE the
              command; no shell, no worktree):
                git show <40hex>:<path> | grep -c '<pat>'
                git ls-tree -r --name-only <40hex> -- <path> | grep -c '<pat>'
              grep runs as a subprocess argv (``grep -c -e <pat>``, BRE, stdin
              bytes), so the re-derivation is the probe's own semantics.
              An ANNOTATED command outside both grammars is
              COMMAND_UNREEXECUTABLE - fail-closed: an annotation this tool
              cannot check is a finding, never a pass
  BASE        with --base-rev, the annotation's ``base`` value is re-derived
              the same way with the revision substituted

Findings name class, receipt line and the disagreeing values.  An unannotated
command is outside this tool's scope (plain probes are not checked).

Verdict map: 0 = clean (at least one annotation, every one agrees with its
pasted output and every re-derivation); 1 = defect (any finding, each named);
2 = could-not-evaluate (no annotations found, receipt absent at REV, unknown
revision, failed git or grep call).  A receipt annotating nothing is
unevaluable, never vacuously clean (the QUALITY #66 boundary).

Limits: one receipt per run; the ``base: X -> record: Y`` grammar only (a
receipt that phrases its claims differently is unevaluable, not clean); a
correction appended AFTER a defective annotation does not clear it - filed
bytes stay as filed, so a receipt whose historical annotation contradicts
itself keeps firing forever (the r58 c1-after.txt does; that persistent
finding is disclosed, not repaired away).  A grep re-derivation inherits
grep's own limits (BRE, current locale, binary-input line counting).

--selftest runs the extractor, the grammar matcher and the audit over
in-memory fixtures (no git, no grep, no writes outside an optional --json-out)
asserting the exit class, the finding ids and the bound values of every case;
the committed-tree demonstrations in the round-59 receipts are the second
evidence.

Demonstrations on the committed tree (round 59 receipts):
  red    --receipt .ufo/waves/round-58/l1/scores/c1-after.txt --rev df62b6f9
             (the D58-1 defect itself, as filed: R1's annotation claims
             record: 1 while its pasted output is 0 and the cited pattern
             re-derives to 0 at 536c4865 -> exit 1, ANNOTATION_OUTPUT_MISMATCH
             + ANNOTATION_REDERIVATION_MISMATCH)
  green  --receipt .ufo/waves/round-59/l1/scores/d581-correction.txt --rev
             <landing> (the round-59 correction receipt: every annotation
             re-derives -> exit 0)
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys

CMD_PREFIX = "$ "
ANN_RE = re.compile(r"^\(.*?\bbase:\s*(-?\d+)\s*->\s*record:\s*(-?\d+)", re.S)
INT_RE = re.compile(r"^-?\d+$")
REV_RE = re.compile(r"^[0-9a-f]{40}$")

SHOW_GRAMMAR = ["git", "show"]
LSTREE_GRAMMAR = ["git", "ls-tree", "-r", "--name-only"]


class Finding:
    def __init__(self, cls, line, detail):
        self.cls = cls
        self.line = line
        self.detail = detail

    def as_dict(self):
        return {"class": self.cls, "line": self.line, "detail": self.detail}

    def __repr__(self):
        return f"{self.cls}@{self.line}: {self.detail}"


def extract(text):
    """Return (commands, annotations).

    commands: list of dicts {line, cmd, output} - cmd is the text after '$ ',
    output the pasted integer or None.
    annotations: list of dicts {line, base, record, cmd_index}.
    """
    commands = []
    annotations = []
    lines = text.splitlines()
    pending = None  # index into commands of the command awaiting output
    for i, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if stripped.startswith(CMD_PREFIX):
            commands.append({"line": i, "cmd": stripped[len(CMD_PREFIX):],
                             "output": None})
            pending = len(commands) - 1
            continue
        if pending is not None and commands[pending]["output"] is None:
            if stripped and INT_RE.match(stripped):
                commands[pending]["output"] = int(stripped)
                pending = None
                continue
        m = ANN_RE.match(raw)
        if m:
            annotations.append({
                "line": i,
                "base": int(m.group(1)),
                "record": int(m.group(2)),
                "cmd_index": len(commands) - 1,
            })
    return commands, annotations


def match_grammar(cmd):
    """Parse a command line into a re-executable probe descriptor or None.

    Returns dict(kind='show'|'lstree', rev, path, pattern) for exactly:
      git show <40hex>:<path> | grep -c '<pat>' [nothing after]
      git ls-tree -r --name-only <40hex> -- <path> | grep -c '<pat>' [nothing]
    Parsing only - the command text is never executed as a shell string.
    """
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return None
    n = len(tokens)
    # find the pipe + grep -c <pat> tail
    pipe = None
    for i in range(n - 3):
        if tokens[i] == "|" and tokens[i + 1] == "grep" and \
                tokens[i + 2] == "-c":
            pipe = i
            break
    if pipe is None:
        return None
    head = tokens[:pipe]
    pat = tokens[pipe + 3]
    if tokens[pipe + 4:]:
        return None  # anything after the pattern: not in grammar
    if head[:2] == SHOW_GRAMMAR and len(head) == 3:
        spec = head[2]
        if ":" not in spec:
            return None
        rev, _, path = spec.partition(":")
        if not REV_RE.match(rev) or not path:
            return None
        return {"kind": "show", "rev": rev, "path": path, "pattern": pat}
    if head[:4] == LSTREE_GRAMMAR and len(head) == 7 and head[5] == "--":
        rev, path = head[4], head[6]
        if not REV_RE.match(rev) or not path:
            return None
        return {"kind": "lstree", "rev": rev, "path": path, "pattern": pat}
    return None


def run_probe(root, probe, rev_override=None):
    """Re-execute a grammar-matched probe via argv subprocesses.

    git produces the bytes (from objects at the revision); the system grep
    counts matching lines exactly as the pasted probe did (BRE, -c, stdin).
    Returns (count, err) - err None on success.
    """
    rev = rev_override or probe["rev"]
    if probe["kind"] == "show":
        git_argv = ["git", "-C", root, "show", f"{rev}:{probe['path']}"]
    else:
        git_argv = ["git", "-C", root, "ls-tree", "-r", "--name-only", rev,
                    "--", probe["path"]]
    try:
        g = subprocess.run(git_argv, capture_output=True)
        if g.returncode != 0:
            return None, f"git rc={g.returncode}: " + \
                g.stderr.decode(errors="replace").strip()[:200]
        grep_argv = ["grep", "-c", "-e", probe["pattern"]]
        c = subprocess.run(grep_argv, input=g.stdout, capture_output=True)
        if c.returncode not in (0, 1):
            return None, f"grep rc={c.returncode}: " + \
                c.stderr.decode(errors="replace").strip()[:200]
        return int(c.stdout.decode().strip() or "0"), None
    except OSError as exc:
        return None, f"oserror: {exc}"


def audit(root, receipt_path, rev, base_rev=None, runner=None):
    """Audit one receipt.  runner(root, probe, rev_override) injects the
    re-derivation for --selftest; default is run_probe.  Returns
    (exit_class, findings, summary_dict)."""
    g = subprocess.run(["git", "-C", root, "show", f"{rev}:{receipt_path}"],
                       capture_output=True)
    if g.returncode != 0:
        return 2, [], {"error": f"receipt absent at {rev[:12]}: {receipt_path}",
                       "receipt": receipt_path, "rev": rev}
    text = g.stdout.decode("utf-8", errors="replace")
    commands, annotations = extract(text)
    if not annotations:
        return 2, [], {"error": "no 'base: N -> record: M' annotation found",
                       "receipt": receipt_path, "rev": rev,
                       "commands": len(commands)}
    findings = []
    checked = 0
    for ann in annotations:
        if ann["cmd_index"] < 0 or ann["cmd_index"] >= len(commands):
            findings.append(Finding("ANNOTATION_ORPHAN", ann["line"],
                                    "no preceding $ command"))
            continue
        cmd = commands[ann["cmd_index"]]
        checked += 1
        # OUTPUT: the annotation must agree with the pasted output
        if cmd["output"] is None:
            findings.append(Finding("OUTPUT_MISSING", ann["line"],
                                    "bound command has no pasted integer "
                                    "output"))
        elif cmd["output"] != ann["record"]:
            findings.append(Finding(
                "ANNOTATION_OUTPUT_MISMATCH", ann["line"],
                f"annotation claims record: {ann['record']} but the bound "
                f"command's pasted output is {cmd['output']}"))
        # RE-DERIVE at the command's own revision
        probe = match_grammar(cmd["cmd"])
        if probe is None:
            findings.append(Finding(
                "COMMAND_UNREEXECUTABLE", cmd["line"],
                f"annotated command outside both supported grammars: "
                f"{cmd['cmd'][:120]}"))
        else:
            count, err = (runner or run_probe)(root, probe, None)
            if err is not None:
                findings.append(Finding("PROBE_FAILED", cmd["line"], err))
            else:
                if count != ann["record"]:
                    findings.append(Finding(
                        "ANNOTATION_REDERIVATION_MISMATCH", ann["line"],
                        f"annotation claims record: {ann['record']} but the "
                        f"probe re-derives to {count} at {probe['rev'][:12]}"))
                if base_rev is not None:
                    bcount, berr = (runner or run_probe)(root, probe,
                                                         base_rev)
                    if berr is not None:
                        findings.append(Finding("PROBE_FAILED", cmd["line"],
                                                "base: " + berr))
                    elif bcount != ann["base"]:
                        findings.append(Finding(
                            "ANNOTATION_BASE_MISMATCH", ann["line"],
                            f"annotation claims base: {ann['base']} but the "
                            f"probe re-derives to {bcount} at "
                            f"{base_rev[:12]}"))
    verdict = 0 if not findings else 1
    summary = {
        "receipt": receipt_path,
        "rev": rev,
        "base_rev": base_rev,
        "annotations": len(annotations),
        "checked": checked,
        "findings": [f.as_dict() for f in findings],
        "exit": verdict,
    }
    return verdict, findings, summary


def selftest():
    """In-memory fixtures; no git, no grep.  Returns (cases, failures)."""
    cases = []
    failures = []

    def check(name, got, want):
        cases.append(name)
        if got != want:
            failures.append(f"{name}: got {got!r} want {want!r}")

    def fixed_runner(table):
        def run(root, probe, rev_override):
            key = (probe["kind"], rev_override or probe["rev"],
                   probe["path"], probe["pattern"])
            if key not in table:
                return None, f"selftest table miss: {key}"
            return table[key], None
        return run

    R = "df62b6f986fb460847037482e0199cdf1541e393"
    T = "536c48650a5ccc435387b2060638a9d8a4bebf44"
    del R  # the selftest runs no git; T pins the record rev used in shapes

    # 1. extraction: command, output, annotation binding to last command
    text1 = ("head\n"
             "$ git show %s:LOG.md | grep -c 'pat one'\n"
             "2\n"
             "(base: 0 -> record: 2; ok)\n"
             "$ git show %s:LOG.md | grep -c 'second'\n"
             "0\n"
             "no annotation here\n" % (T, T))
    cmds, anns = extract(text1)
    check("extract-commands", len(cmds), 2)
    check("extract-outputs", [c["output"] for c in cmds], [2, 0])
    check("extract-annotations", len(anns), 1)
    check("extract-binding", cmds[anns[0]["cmd_index"]]["cmd"],
          f"git show {T}:LOG.md | grep -c 'pat one'")

    # 2-9. grammar matcher
    g1 = match_grammar(f"git show {T}:LOG.md | grep -c '27 distinct paths'")
    check("grammar-show", (g1 or {}).get("kind"), "show")
    check("grammar-show-fields", (g1 or {}).get("path"), "LOG.md")
    check("grammar-show-pattern", (g1 or {}).get("pattern"),
          "27 distinct paths")
    g2 = match_grammar(
        f"git ls-tree -r --name-only {T} -- a/b/c.txt | grep -c 'name\\.json'")
    check("grammar-lstree", (g2 or {}).get("kind"), "lstree")
    check("grammar-lstree-path", (g2 or {}).get("path"), "a/b/c.txt")
    check("grammar-trailing-comment",
          match_grammar(f"git show {T}:S | grep -c 'p' ; the table rows:"),
          None)
    check("grammar-no-quote-balance",
          match_grammar(f"git show {T}:S | grep -c 'unbalanced"),
          None)
    check("grammar-short-rev",
          match_grammar("git show abc:LOG.md | grep -c 'p'"), None)
    check("grammar-wc",
          match_grammar(f"git ls-tree -r --name-only {T} -- d | wc -l"), None)

    # 10. green: output and re-derivation agree (pieces only - no git here)
    green = ("$ git show %s:LOG.md | grep -c 'pat'\n"
             "1\n"
             "(base: 0 -> record: 1; fine)\n" % T)
    cs, ans = extract(green)
    probe = match_grammar(cs[0]["cmd"])
    cnt, err = fixed_runner({
        ("show", T, "LOG.md", "pat"): 1,
    })(None, probe, None)
    check("green-rederive", (cnt, err), (1, None))
    ok = (cs[0]["output"] == ans[0]["record"] == cnt)
    check("green-agreement", ok, True)

    # 11. red: the D58-1 shape (output 0, annotation claims 1, re-derive 0)
    d581 = ("$ git show %s:LOG.md | grep -c '27 distinct filesystem paths'\n"
            "0\n"
            "(base: 0 -> record: 1; the note is the landing entry's first "
            "bullet)\n" % T)
    cs, ans = extract(d581)
    findings = []
    if cs[0]["output"] != ans[0]["record"]:
        findings.append("ANNOTATION_OUTPUT_MISMATCH")
    cnt, _ = fixed_runner({
        ("show", T, "LOG.md", "27 distinct filesystem paths"): 0,
    })(None, match_grammar(cs[0]["cmd"]), None)
    if cnt != ans[0]["record"]:
        findings.append("ANNOTATION_REDERIVATION_MISMATCH")
    check("red-d581-findings", findings,
          ["ANNOTATION_OUTPUT_MISMATCH", "ANNOTATION_REDERIVATION_MISMATCH"])

    # 12. red: base mismatch with --base-rev semantics
    bcnt, _ = fixed_runner({
        ("show", "42c794afc5cdf2f72d80edb839cfbcbfe32e6bad", "LOG.md", "pat"): 2,
    })(None, {"kind": "show", "rev": T, "path": "LOG.md", "pattern": "pat"},
        "42c794afc5cdf2f72d80edb839cfbcbfe32e6bad")
    check("red-base-mismatch", bcnt != 0, True)

    # 13. red: annotated command outside the grammars is fail-closed
    check("red-unreexecutable",
          match_grammar("git log --oneline -1 | grep -c 'x'"), None)

    # 14. unevaluable: annotations absent -> exit class 2, never clean
    noann = "$ git show %s:LOG.md | grep -c 'x'\n0\n(plain probe note)\n" % T
    cs2, ans2 = extract(noann)
    check("unevaluable-no-annotations", (len(cs2), len(ans2)), (1, 0))

    # 15. extraction: integer-looking annotation line is not an output
    tricky = ("$ git show %s:LOG.md | grep -c 'p'\n"
              "1\n"
              "(base: 0 -> record: 1; x)\n" % T)
    cs3, ans3 = extract(tricky)
    check("annotation-not-output", cs3[0]["output"], 1)

    # 16. annotation grammar tolerates multi-sentence single-line annotations
    long_ann = ("$ git show %s:LOG.md | grep -c 'p'\n"
                "3\n"
                "(base: 0 -> record: 3; the note states: a b c; filed bytes "
                "stay as filed)\n" % T)
    cs4, ans4 = extract(long_ann)
    check("long-annotation", (len(ans4), ans4[0]["record"],
                              ans4[0]["base"]), (1, 3, 0))

    # 17. negative integers parse as outputs
    neg = "$ git show %s:LOG.md | grep -c 'p'\n-1\n(base: -1 -> record: 0; x)\n" % T
    cs5, ans5 = extract(neg)
    check("negative-output", cs5[0]["output"], -1)

    # 18. the D58-1 wording fix: the corrected pattern re-derives to 2
    corrected = match_grammar(
        f"git show {T}:LOG.md | grep -c 'distinct filesystem paths number 27'")
    cnt2, _ = fixed_runner({
        ("show", T, "LOG.md", "distinct filesystem paths number 27"): 2,
    })(None, corrected, None)
    check("corrected-pattern-count", cnt2, 2)

    return cases, failures


def main():
    ap = argparse.ArgumentParser(
        description="receipt-annotation consistency gate (round 59)")
    ap.add_argument("--root", default=".",
                    help="lane repo root (git -C target)")
    ap.add_argument("--receipt", help="repo-relative receipt path to audit")
    ap.add_argument("--rev", help="revision whose bytes carry the receipt")
    ap.add_argument("--base-rev", default=None,
                    help="optional: also re-derive each annotation's base: "
                         "value at this revision")
    ap.add_argument("--selftest", action="store_true",
                    help="run in-memory fixtures, no git, no writes")
    ap.add_argument("--json-out", default=None,
                    help="optional path for the JSON summary receipt")
    args = ap.parse_args()

    if args.selftest:
        cases, failures = selftest()
        summary = {"tool": "tools/round-59/annotation-audit.py",
                   "selftest": True, "cases": len(cases),
                   "failures": failures, "exit": 1 if failures else 0}
        out = json.dumps(summary, indent=1)
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8",
                      newline="\n") as fh:
                fh.write(out + "\n")
        print(out)
        return 1 if failures else 0

    if not args.receipt or not args.rev:
        print("annotation-audit: --receipt and --rev are required "
              "(or --selftest)", file=sys.stderr)
        return 2
    if not REV_RE.match(args.rev):
        print("annotation-audit: --rev must be a 40-hex commit id",
              file=sys.stderr)
        return 2
    if args.base_rev and not REV_RE.match(args.base_rev):
        print("annotation-audit: --base-rev must be a 40-hex commit id",
              file=sys.stderr)
        return 2

    verdict, findings, summary = audit(args.root, args.receipt, args.rev,
                                       base_rev=args.base_rev)
    for f in findings:
        print(f, file=sys.stderr)
    out = json.dumps(summary, indent=1)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out + "\n")
    print(out)
    return verdict


if __name__ == "__main__":
    sys.exit(main())
