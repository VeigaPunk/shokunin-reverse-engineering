#!/usr/bin/env python3
"""invocation-audit.py --root LANE --rev REV

Round-17 R16-INVOCATION counting tool (contract.md section
"W/tools/invocation-audit.py"). Read-only over Git objects: it shells out to
`git ls-tree` / `git show` against REV and never touches the working tree.

Registry rows = SKILL.md table rows whose 2nd cell matches
`(probe|gate|tool) / kaidoku`. Command = first backticked span in the 3rd cell.
Receipts = every `verification.json`, `final-recheck.json`, `*receipt*.json`,
`gate-results.json` (all basename matches) under `.ufo/` at REV. An exercised
argv = any JSON array of strings under a key named `argv` or `orig_argv`.

Row classes:
  exercised_match      normalized command (tokens; `<...>` placeholders are
                       one-token wildcards; `[...]`-bracketed tokens are
                       optional; a leading `pythonX` interpreter token and
                       absolute paths under --root are normalized away) equals
                       some exercised argv.
  labelled_unexercised row text contains `unexercised` (checked only when the
                       command matched no exercised argv; a matched row is
                       reported exercised_match with `row_says_unexercised`).
  unlabelled_variant   otherwise.

Output: {"rev", "rows":[{name, command, class, matched_receipt, ...}], "counts"}
Exit 0 = reported, 2 = could-not-evaluate (bad args, git failure, missing
SKILL.md). A receipt file that is not parseable JSON is counted under
`unreadable_receipts` and skipped -- it cannot contribute an exercised argv.
`--selftest` builds a throwaway git repo under tempfile.mkdtemp(), runs the
same audit path against it, asserts the four classes, and removes it.
"""

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

RECEIPT_EXACT = {"verification.json", "final-recheck.json", "gate-results.json"}
RECEIPT_GLOB = "*receipt*.json"
ROW_KIND_RE = re.compile(r"^(probe|gate|tool)\s*/\s*kaidoku$", re.IGNORECASE)
BACKTICK_RE = re.compile(r"`([^`]*)`")
PLACEHOLDER_RE = re.compile(r"^<[^<>]*>$")
INTERPRETER_RE = re.compile(r"^(?:python[\d.]*|pypy[\d.]*)$")


# ---------------------------------------------------------------- git access

class GitError(Exception):
    pass


def _git(root, args, decode=True):
    try:
        proc = subprocess.run(
            ["git", "-C", root] + args,
            capture_output=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitError(f"git {' '.join(args[:2])} failed to run: {exc}")
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        raise GitError(f"git {' '.join(args[:2])} exit {proc.returncode}: {err}")
    return proc.stdout.decode("utf-8", "replace") if decode else proc.stdout


def resolve_rev(root, rev):
    return _git(root, ["rev-parse", "--verify", f"{rev}^{{commit}}"]).strip()


def list_ufo_paths(root, rev):
    out = _git(root, ["ls-tree", "-r", "--name-only", rev, "--", ".ufo/"])
    return [line for line in out.splitlines() if line]


def show(root, rev, path):
    return _git(root, ["show", f"{rev}:{path}"], decode=False)


# -------------------------------------------------------- command tokenizing

def tokenize_command(raw):
    """Split a registry command cell into [(token, optional)].

    Whitespace splits tokens; single/double quotes group; backslash escapes the
    next char. Square brackets mark every token they enclose as optional, e.g.
    `[--label <L>]` -> ('--label', True), ('<L>', True). Bracket characters are
    not part of token text.
    """
    tokens = []
    buf = []
    depth = 0
    tok_optional = False
    quote = None
    escape = False
    started = False

    def flush():
        nonlocal buf, tok_optional, started
        if started:
            tokens.append(("".join(buf), tok_optional))
        buf, tok_optional, started = [], False, False

    for ch in raw:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\" and quote != "'":
            escape = True
            started = True
            continue
        if quote:
            if ch == quote:
                quote = None
            else:
                buf.append(ch)
            continue
        if ch in ("'", '"'):
            quote = ch
            started = True
            continue
        if ch == "[":
            depth += 1
            tok_optional = True
            started = True
            continue
        if ch == "]":
            depth = max(0, depth - 1)
            started = True
            continue
        if ch.isspace():
            flush()
            continue
        if depth > 0:
            tok_optional = True
        buf.append(ch)
        started = True
    flush()
    return tokens


def first_backtick_span(cell):
    match = BACKTICK_RE.search(cell)
    return match.group(1) if match else None


def parse_registry(skill_text):
    rows = []
    for lineno, line in enumerate(skill_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.split("|")]
        # ['', name, kind, command_cell, ... , '']
        if len(cells) < 5:
            continue
        if not ROW_KIND_RE.match(cells[2]):
            continue
        command = first_backtick_span(cells[3])
        rows.append(
            {
                "name": cells[1].strip("`"),
                "line": lineno,
                "command": command,
                "raw": stripped,
            }
        )
    return rows


# ------------------------------------------------------------- normalization

def _relpath(token, root):
    if os.path.isabs(token):
        rel = os.path.relpath(token, root)
        if not rel.startswith(".."):
            return rel
    return token


def normalize_tokens(tokens, root):
    """Drop a leading interpreter token; relpath absolute tokens under root."""
    toks = list(tokens)
    while toks and os.path.basename(toks[0]) and INTERPRETER_RE.match(
        os.path.basename(toks[0])
    ):
        toks = toks[1:]
    return [_relpath(t, root) for t in toks]


def argv_matches(pattern_tokens, argv_tokens):
    """pattern_tokens: [(text, optional)]; argv_tokens: [str].

    `<...>` placeholder tokens match exactly one argv token; optional tokens
    may be skipped wholesale (each bracketed token is independently optional).
    """
    memo = {}

    def rec(pi, ai):
        key = (pi, ai)
        if key in memo:
            return memo[key]
        if pi == len(pattern_tokens):
            result = ai == len(argv_tokens)
        else:
            text, optional = pattern_tokens[pi]
            result = False
            if optional and rec(pi + 1, ai):
                result = True
            elif ai < len(argv_tokens):
                if PLACEHOLDER_RE.match(text) or text == argv_tokens[ai]:
                    result = rec(pi + 1, ai + 1)
        memo[key] = result
        return result

    return rec(0, 0)


# -------------------------------------------------------------- receipt scan

def iter_exercised_argvs(obj, keypath=""):
    """Yield (keypath, argv_list) for every `argv` list-of-strings that ran.

    Round-17 L1 integration (w2 InvocationAuditAttack F1/F4): `orig_argv` is the
    receipt producer's own command line, not an exercised registry command, so it
    is ignored; an `argv` whose sibling `exit` is recorded and is neither 0 nor 1
    (2 = could-not-evaluate, null = could not start/timeout) did not run as
    advertised and is not counted."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = f"{keypath}/{key}"
            if (
                key == "argv"
                and isinstance(value, list)
                and all(isinstance(x, str) for x in value)
                and ("exit" not in obj or obj.get("exit") in (0, 1))
            ):
                yield child, value
            yield from iter_exercised_argvs(value, child)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from iter_exercised_argvs(value, f"{keypath}[{index}]")


def receipt_eligible(path):
    base = path.rsplit("/", 1)[-1]
    return base in RECEIPT_EXACT or fnmatch.fnmatchcase(base, RECEIPT_GLOB)


# ---------------------------------------------------------------- audit core

def audit(root, rev):
    resolved = resolve_rev(root, rev)
    paths = list_ufo_paths(root, resolved)
    receipt_paths = [p for p in paths if receipt_eligible(p)]
    pathglob_extras = [
        p
        for p in paths
        if p.endswith(".json")
        and fnmatch.fnmatchcase(p, "*receipt*.json")
        and not receipt_eligible(p)
    ]

    exercised = []  # (receipt_path, keypath, argv_list)
    unreadable = []
    for path in sorted(receipt_paths):
        try:
            doc = json.loads(show(root, resolved, path))
        except (GitError, json.JSONDecodeError, UnicodeDecodeError):
            unreadable.append(path)
            continue
        for keypath, argv in iter_exercised_argvs(doc):
            exercised.append((path, keypath, argv))

    try:
        skill_text = show(root, resolved, "SKILL.md").decode("utf-8", "replace")
    except GitError as exc:
        raise GitError(f"SKILL.md at {resolved}: {exc}")
    registry = parse_registry(skill_text)

    norm_argvs = [
        (path, keypath, argv, normalize_tokens(argv, root))
        for path, keypath, argv in exercised
    ]

    rows = []
    counts = {"exercised_match": 0, "labelled_unexercised": 0, "unlabelled_variant": 0}
    for entry in registry:
        row = {
            "name": entry["name"],
            "line": entry["line"],
            "command": entry["command"],
            "class": None,
            "matched_receipt": None,
        }
        if entry["command"] is None:
            row["class"] = "unlabelled_variant"
            row["note"] = "no backticked span in command cell"
            counts["unlabelled_variant"] += 1
            rows.append(row)
            continue
        pattern_raw = tokenize_command(entry["command"])
        pattern = [
            (_relpath(t, root), opt) for t, opt in pattern_raw
        ]
        # interpreter strip on the pattern side as well
        while pattern and INTERPRETER_RE.match(os.path.basename(pattern[0][0])):
            pattern = pattern[1:]

        matches = [
            (path, keypath, argv)
            for path, keypath, argv, norm in norm_argvs
            if argv_matches(pattern, norm)
        ]
        row_says_unexercised = "unexercised" in entry["raw"].lower()
        if matches:
            row["class"] = "exercised_match"
            matches.sort(key=lambda m: (m[0], m[1]))
            row["matched_receipt"] = matches[0][0]
            row["matched_keypath"] = matches[0][1]
            row["matched_argv"] = " ".join(matches[0][2])
            row["matched_receipt_count"] = len(matches)
            if row_says_unexercised:
                row["row_says_unexercised"] = True
            counts["exercised_match"] += 1
        elif row_says_unexercised:
            row["class"] = "labelled_unexercised"
            counts["labelled_unexercised"] += 1
        else:
            row["class"] = "unlabelled_variant"
            counts["unlabelled_variant"] += 1
        rows.append(row)

    return {
        "rev": resolved,
        "rows": rows,
        "counts": {
            "rows": len(rows),
            **counts,
            "receipt_files": len(receipt_paths),
            "argv_records": len(exercised),
            "unreadable_receipts": len(unreadable),
            "unreadable_receipt_paths": unreadable,
            "receipt_glob_pathform_excluded": len(pathglob_extras),
        },
    }


# ------------------------------------------------------------------ selftest

SELFTEST_SKILL = """# fixture skill

| name | kind | command | selftest | pins |
| --- | --- | --- | --- | --- |
| alpha-probe | probe / kaidoku | `python3 .ufo/tools/alpha.py --rev <REV>`; 0 ok | x | y |
| beta-gate | gate / kaidoku | `python3 -I {root}/.ufo/tools/beta.py capture --out <receipt> [--label <L>]`; 0 ok | x | y |
| gamma-tool | tool / kaidoku | `python3 .ufo/tools/gamma.py run`; recorded unexercised in wave 3 | x | y |
| delta-probe | probe / kaidoku | `python3 .ufo/tools/delta.py --fast`; 0 ok | x | y |
| other-row | probe / other | `python3 .ufo/tools/alpha.py --rev <REV>` | x | y |
"""


def selftest():
    tmp = tempfile.mkdtemp(prefix="invocation-audit-selftest-")
    cases = 0
    try:
        root = tmp
        _git(root, ["init", "-q"])
        _git(root, ["config", "user.email", "selftest@example.invalid"])
        _git(root, ["config", "user.name", "selftest"])
        _git(root, ["config", "commit.gpgsign", "false"])

        def put(rel, text):
            dest = os.path.join(root, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as fh:
                fh.write(text)

        put("SKILL.md", SELFTEST_SKILL.format(root=root))
        put(
            ".ufo/waves/round-16/verification.json",
            json.dumps(
                {
                    "commands": [
                        {
                            "label": "alpha",
                            "argv": [
                                "python3",
                                ".ufo/tools/alpha.py",
                                "--rev",
                                "deadbeef",
                            ],
                        },
                        {
                            "label": "beta",
                            "argv": [
                                "python3",
                                "-I",
                                os.path.join(root, ".ufo/tools/beta.py"),
                                "capture",
                                "--out",
                                "/tmp/r.json",
                            ],
                        },
                        {
                            "label": "not-an-argv-shape",
                            "argv": ["python3", 7],
                        },
                    ],
                    "orig_argv": ["python3", "-I", "ignored.py"],
                }
            ),
        )
        put(".ufo/receipts/nested/not-basename.json", json.dumps({"argv": ["x"]}))
        put(".ufo/notes/run-receipt-v1.json", "{not json")
        _git(root, ["add", "-A"])
        _git(root, ["commit", "-q", "-m", "fixture"])
        rev = _git(root, ["rev-parse", "HEAD"]).strip()

        result = audit(root, rev)
        by_name = {r["name"]: r for r in result["rows"]}
        cases = 6
        problems = []
        if by_name["alpha-probe"]["class"] != "exercised_match":
            problems.append("alpha-probe not exercised_match")
        if by_name["beta-gate"]["class"] != "exercised_match":
            problems.append("beta-gate not exercised_match")
        if by_name["gamma-tool"]["class"] != "labelled_unexercised":
            problems.append("gamma-tool not labelled_unexercised")
        if by_name["delta-probe"]["class"] != "unlabelled_variant":
            problems.append("delta-probe not unlabelled_variant")
        if "other-row" in by_name:
            problems.append("non-kaidoku row leaked into registry")
        if result["counts"]["unreadable_receipts"] != 1:
            problems.append("corrupt receipt not counted")
        if problems:
            print("SELFTEST: FAILED " + "; ".join(problems))
            return 1
        print(f"SELFTEST: CLEAN cases={cases}")
        return 0
    except GitError as exc:
        print(f"SELFTEST: FAILED git fixture unusable: {exc}")
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------- cli

def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Audit SKILL.md registry rows against exercised argv/orig_argv "
            "arrays in .ufo/ receipt JSON at a revision. Reads Git objects "
            "only; never touches the working tree. Exit 0 reported, "
            "2 could-not-evaluate."
        )
    )
    parser.add_argument("--root", help="lane repo root")
    parser.add_argument("--rev", help="revision to read")
    parser.add_argument(
        "--selftest", action="store_true", help="build temp fixtures and verify"
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.root or not args.rev:
        print(json.dumps({"error": "--root and --rev are required"}, indent=2, sort_keys=True))
        return 2
    if not os.path.isdir(args.root):
        print(json.dumps({"error": f"root not a directory: {args.root}"}, indent=2, sort_keys=True))
        return 2
    try:
        result = audit(args.root, args.rev)
    except GitError as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
