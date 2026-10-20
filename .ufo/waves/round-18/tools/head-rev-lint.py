#!/usr/bin/env python3
"""head-rev-lint.py --root LANE --rev REV [--strict]

Round-18 C2 counting command. Implements the L1 contract amendment
(2026-10-20): the written rule, not a target number, defines the count.

Scope (lane instruments): tracked ``*.py``/``*.sh`` at REV under
``.ufo/gates/**``, ``.ufo/rounds/**``, ``.ufo/waves/round-1[4-8]/`` EXCEPT
any path containing a seat-dir segment ``w[0-9]+/`` (``w1/``, ``w2/``...).
Seat-dir files are never silently dropped: they are scanned anyway and
reported in ``excluded`` with their would-be sites and the reason
``seat wave output, not a lane instrument``.

Site kinds (rule 3): a git argv is any literal ``["git", ...]`` argv (a
call whose first positional arg is such a list/tuple) or a call to a
git-wrapper function — a function whose own body builds a ``["git", ...]``
literal, e.g. ``git("rev-parse","HEAD")``, ``git_in(repo,"rev-parse",...)``,
``_git(root,[...])``. String-literal args are classified:

- ``rev-parse-HEAD``: subcommand ``rev-parse`` (or ``rev-parse`` co-present
  in the argv) plus a HEAD revision literal: ``HEAD``, ``HEAD^{...}``,
  ``HEAD~N``, or ``@``.
- ``other-HEAD``: a HEAD revision literal operand of another revision-taking
  subcommand in {show, log, ls-tree, cat-file, diff, archive, rev-list}
  (the audit's class-D shape; ``git rev-list HEAD`` is not rev-parse).
- ``HEAD-colon``: a literal ``HEAD:`` revision-path token, or a constant
  f-string whose rendered prefix is ``HEAD:``, when a revision-taking
  subcommand co-occurs.
- ``default-HEAD``: argparse ``add_argument(default="HEAD")`` on a rev-like
  option (dest in REV_LIKE_OPTIONS).
- ``upstream``: ``@{...}`` literal tokens, ``--abbrev-ref``,
  ``--show-current``, ``symbolic-ref``.
A ``--`` operand boundary and flag-value consumption (``-C``, ``-c``...)
suppress HEAD-operand matching after them.

Context (rules 2+4), in priority order:
- ``annotated``: the site line carries ``head-rev-lint: compare-only``
  (HEAD read solely to compare with the branch tip) or
  ``head-rev-lint: red-before`` (deliberate baseline reproduction). Listed
  with ``reason``, never counted live.
- ``fixture``: the path has a ``/fixtures/`` segment, OR any enclosing
  Python function name contains ``selftest``/``fixture``, OR the innermost
  enclosing function is called (same file, transitively) only from
  selftest/fixture functions (e.g. round-17/controls.py ``_commit``).
  Call-graph: intra-file name callers; a function with zero callers is a
  live entry point; "called only from" requires >=1 caller.
- ``live``: everything else. Shell files default to live but the
  ``/fixtures/`` path rule and line annotations still apply.

Shell scanning: each non-comment line's ``git ...`` runs (split at
``&|;<>()#``) are tokenized like a Python argv; ``${X:-HEAD}`` parameter
expansions count as a HEAD literal.

Output (sort_keys, indent=2):
    {rev, files_scanned, sites: [{path, line, kind, context, code,
      reason?}], live_count, fixture_count, annotated_count,
      routed_sites: [3 audited paths], excluded: [{path, reason, sites}],
      limits: [...]}
Exit 0 emitted, 1 under --strict iff live_count > 0, 2 could-not-evaluate.
Read-only git only: rev-parse --verify / ls-tree / show.

--selftest builds a fixture repo under tempfile.mkdtemp(), commits
revisions exercising every kind, fixture contexts (name, nested, called-
only-from-selftest, /fixtures/ path), both annotations, and a seat-dir
exclusion, then prints SELFTEST: CLEAN cases=N or SELFTEST: FAILED ....
"""

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SITE_DIRS = (
    [".ufo/gates/", ".ufo/rounds/"]
    + [".ufo/waves/round-%d/" % n for n in range(14, 19)]
)

SEAT_DIR_RE = re.compile(r"^w[0-9]+$")
EXCLUDED_REASON = "seat wave output, not a lane instrument"

UPSTREAM_FLAGS = ("--abbrev-ref", "--show-current", "symbolic-ref")
UPSTREAM_RE = re.compile(r"^@\{")

HEAD_LIT_RE = re.compile(r"^(?:@|HEAD(?:\^\{?[0-9a-zA-Z]*\}?|~[0-9]*)?)$")
SHELL_HEAD_RE = re.compile(
    r"^(?:@|HEAD(?:\^\{?[0-9a-zA-Z]*\}?|~[0-9]*)?|\$\{[^}]*HEAD[^}]*\})$"
)

# Amendment rule 3's subcommand set. Extra revision-taking subcommands a
# HEAD literal could ride are listed so `other-HEAD` stays conservative.
REV_COMMANDS = {
    "rev-parse", "show", "log", "ls-tree", "cat-file", "diff", "archive",
    "rev-list", "merge-base", "describe", "blame", "annotate", "checkout",
    "reset", "cherry-pick", "rebase", "format-patch", "reflog", "grep",
    "name-rev", "shortlog", "switch", "restore", "branch", "tag", "bisect",
    "commit-tree", "update-ref", "for-each-ref", "whatchanged", "merge",
}
VALUE_FLAGS = {"-C", "-c", "--git-dir", "--work-tree", "--exec-path",
               "--namespace", "-o", "--output", "-m", "--format", "--date"}

REV_LIKE_OPTIONS = {
    "rev", "revision", "commit", "ref", "base", "source", "branch", "tag",
    "since", "until", "start", "end", "from", "to", "before", "after",
    "old", "new", "parent", "ancestor", "baseline", "target", "pin",
    "head", "sites-rev", "start-rev", "end-rev", "range",
}

ANNOTATION_RE = re.compile(
    r"head-rev-lint:\s*(compare-only|red-before)"
)
ANNOTATION_REASONS = {
    "compare-only": "head-rev-lint: compare-only",
    "red-before": "head-rev-lint: red-before",
}

# The three HEAD-keyed live sites routed by
# .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md section 5 (L1 C2 claim).
ROUTED_SITES = [
    ".ufo/waves/round-17/verify.py",
    ".ufo/gates/citation-drift/citation-drift-probe.py",
    ".ufo/gates/custody-pair/custody-pair.py",
]

LIMITS = [
    "static AST/token scan: git argvs built outside a literal list or "
    "wrapper-call site (e.g. assembled via lists of Names, .format(), or "
    "f-strings whose HEAD appears only after rendering a variable) are "
    "invisible",
    "wrapper detection is intra-file: a helper that builds git argv in "
    "another module is not resolved",
    "the called-only-from-selftest rule is intra-file and name-based; "
    "methods, aliases, and cross-module callers are not followed",
    "shell lines are tokenized on whitespace inside git runs split at "
    "&|;<>()# — complex quoting or multiline commands can hide tokens",
    "excluded seat dirs are listed with would-be sites but never counted, "
    "even when a seat file is an instrument another wave re-runs",
    "annotated contexts are trusted comments: the lint cannot verify a "
    "compare-only/red-before claim",
]


class LintError(Exception):
    pass


# ----------------------------------------------------------------- git read

def _git(root, args, decode=True):
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + args,
            capture_output=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise LintError(f"git {' '.join(args[:2])} failed to run: {exc}")
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        raise LintError(f"git {' '.join(args[:2])} exit {proc.returncode}: {err}")
    return proc.stdout.decode("utf-8", "replace") if decode else proc.stdout


def resolve_rev(root, rev):
    return _git(root, ["rev-parse", "--verify", f"{rev}^{{commit}}"]).strip()


def list_site_files(root, rev):
    out = _git(
        root,
        ["ls-tree", "-r", "--name-only", rev, "--"] + SITE_DIRS,
    )
    return [
        line for line in out.splitlines()
        if line.endswith(".py") or line.endswith(".sh")
    ]


def show(root, rev, path):
    return _git(root, ["show", f"{rev}:{path}"], decode=False)


def is_seat_path(path):
    return any(SEAT_DIR_RE.match(seg) for seg in path.split("/"))


# ------------------------------------------------------------ token helpers

def _const_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _joined_str_text(node):
    """Render a JoinedStr to a string iff every part is constant; else None."""
    if not isinstance(node, ast.JoinedStr):
        return None
    parts = []
    for part in node.values:
        text = _const_str(part)
        if text is None:
            return None
        parts.append(text)
    return "".join(parts)


def _joined_leading_text(node):
    """Literal prefix text before the first dynamic part of a JoinedStr."""
    if not isinstance(node, ast.JoinedStr) or not node.values:
        return None
    first = node.values[0]
    text = _const_str(first)
    if text is None:
        return ""
    return text


def _arg_token(node):
    """(text, lineno) for one argv element; text None when dynamic.

    A dynamic f-string whose leading literal starts with ``HEAD:`` yields
    the marker token ``HEAD:`` (the revision path can be completed only at
    render time, but the pin shape is already present)."""
    text = _const_str(node)
    if text is not None:
        return text, node.lineno
    joined = _joined_str_text(node)
    if joined is not None:
        return joined, node.lineno
    leading = _joined_leading_text(node)
    if leading and leading.startswith("HEAD:"):
        return "HEAD:", node.lineno
    return None, None


def _tokens_from_list(node):
    """Token list for ["git", ...] literal, or None if not a git argv."""
    elts = node.elts
    if not elts or _const_str(elts[0]) != "git":
        return None
    return [_arg_token(elt) for elt in elts[1:]]


def _tokens_from_argv_expr(node):
    """Ordered tokens for an argv expression: a ["git", ...] literal, or a
    `+`-concatenation containing one (e.g. ["git","-C",root] + args).
    Returns None when no git literal participates. The leading "git" is
    kept as a marker token (never classifies)."""
    if isinstance(node, (ast.List, ast.Tuple)):
        sub = _tokens_from_list(node)
        if sub is None:
            return None
        return [("git", node.lineno)] + sub
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _tokens_from_argv_expr(node.left)
        right = _tokens_from_argv_expr(node.right)
        if left is None and right is None:
            return None
        return (left or [(None, None)]) + (right or [(None, None)])
    return None


def _tokens_from_wrapper_call(call):
    """Tokens from a call to a git-wrapper function.

    Positional args only. A leading non-constant, non-list argument is a
    repo/root slot and is skipped. List literals are expanded; an arg that
    carries a literal ["git", ...] argv (including a `+` concatenation) is
    treated as the full argv itself."""
    tokens = []
    args = list(call.args)
    if args:
        first = args[0]
        if _const_str(first) is None and not isinstance(
            first, (ast.List, ast.Tuple)
        ):
            args = args[1:]  # skip the root/repo argument
    for arg in args:
        whole = _tokens_from_argv_expr(arg)
        if whole is not None:
            return whole  # a literal ["git", ...] arg is the argv
        if isinstance(arg, (ast.List, ast.Tuple)):
            tokens.extend(_arg_token(elt) for elt in arg.elts)
            continue
        tokens.append(_arg_token(arg))
    return tokens


# ------------------------------------------------------------- classify

def _operand_indices(tokens):
    """Indices of tokens before `--` not consumed as a flag value."""
    boundary = len(tokens)
    for i, (text, _) in enumerate(tokens):
        if text == "--":
            boundary = i
            break
    out = []
    for i in range(boundary):
        prev = tokens[i - 1][0] if i > 0 else None
        if prev in VALUE_FLAGS:
            continue
        out.append(i)
    return out


def classify_argv(tokens, head_re=HEAD_LIT_RE):
    """Return {kind: lineno} for one git argv's tokens ((text, line) pairs)."""
    kinds = {}
    literal = {t for t, _ in tokens if t}

    def put(kind, line):
        kinds.setdefault(kind, line)

    operands = _operand_indices(tokens)

    for i, (text, line) in enumerate(tokens):
        if text is None:
            continue
        if UPSTREAM_RE.match(text) or text in UPSTREAM_FLAGS:
            put("upstream", line)

    if literal & REV_COMMANDS:
        has_rev_parse = "rev-parse" in literal
        has_other_rev = bool((literal & REV_COMMANDS) - {"rev-parse"})
        for i in operands:
            text, line = tokens[i]
            if text is None:
                continue
            if text.startswith("HEAD:"):
                put("HEAD-colon", line)
            elif head_re.match(text):
                if has_rev_parse:
                    put("rev-parse-HEAD", line)
                elif has_other_rev:
                    put("other-HEAD", line)
    return kinds


def annotation_for_line(line_text):
    match = ANNOTATION_RE.search(line_text)
    return match.group(1) if match else None


# ------------------------------------------------------------- py scanner

class SiteScanner(ast.NodeVisitor):
    """Collects sites, enclosing function chains, and the intra-file call
    graph (caller function name -> callee names, in one walk)."""

    def __init__(self, lines):
        self.lines = lines
        self.func_stack = []
        self.wrappers = set()
        self.sites = []          # (line, kind, enclosing_names_tuple)
        self._calls = []         # (caller_name_or_module, callee_name)
        self._refs = []          # (referrer_name_or_module, referenced_name)

    MODULE = "<module>"

    def _referrer(self):
        return self.func_stack[-1] if self.func_stack else self.MODULE

    def visit_Name(self, node):
        # every Load of a defined function name, not just calls: passing a
        # helper as a callback / set_defaults(func=...) is a live use
        if isinstance(node.ctx, ast.Load):
            self._refs.append((self._referrer(), node.id))
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.ctx, ast.Load):
            self._refs.append((self._referrer(), node.attr))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.func_stack.append(node.name)
        self.generic_visit(node)
        self.func_stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def _emit(self, kinds):
        enclosing = tuple(self.func_stack)
        for kind, line in sorted(kinds.items()):
            self.sites.append((line, kind, enclosing))

    def visit_Call(self, node):
        # graph edge for the called-only-from-selftest rule
        callee = None
        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            callee = node.func.attr
        if callee:
            caller = self.func_stack[-1] if self.func_stack else self.MODULE
            self._calls.append((caller, callee))
        # (a) literal ["git", ...] argv as first positional arg
        argv_node = node.args[0] if node.args else None
        if argv_node is None:
            for kw in node.keywords:
                if kw.arg == "args":
                    argv_node = kw.value
        if argv_node is not None:
            tokens = _tokens_from_argv_expr(argv_node)
            if tokens is not None:
                self._emit(classify_argv(tokens))
                self.generic_visit(node)
                return
        # (b) call to a known git wrapper
        name = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if name in self.wrappers:
            tokens = _tokens_from_wrapper_call(node)
            self._emit(classify_argv(tokens))
        # (c) argparse default="HEAD" on a rev-like option
        if name == "add_argument":
            self._check_add_argument(node)
        self.generic_visit(node)

    def _check_add_argument(self, node):
        default_node = None
        for kw in node.keywords:
            if kw.arg == "default" and _const_str(kw.value) == "HEAD":
                default_node = kw.value
        if default_node is None:
            return
        for arg in node.args:
            text = _const_str(arg)
            if not text or not text.startswith("-"):
                continue
            dest = text.lstrip("-").replace("_", "-").split("=", 1)[0]
            if dest in REV_LIKE_OPTIONS:
                self._emit({"default-HEAD": default_node.lineno})
                return


def scan_python(source):
    """(sites, fixture_funcs). sites = [(line, kind, context_key)] where
    context_key is decided by the caller via fixture_funcs + annotations."""
    tree = ast.parse(source)
    scanner = SiteScanner(source.splitlines())

    # pass 1: git-wrapper function names (contain a literal git argv)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and sub.args and (
                _tokens_from_argv_expr(sub.args[0]) is not None
            ):
                scanner.wrappers.add(node.name)
                break
        # a wrapper may also build argv in a local assignment
        for sub in ast.walk(node):
            if isinstance(sub, ast.Assign) and isinstance(
                sub.value, (ast.List, ast.Tuple, ast.BinOp)
            ) and _tokens_from_argv_expr(sub.value) is not None:
                scanner.wrappers.add(node.name)
                break

    scanner.visit(tree)

    # pass 3: fixture-context functions.
    # seeded: names containing selftest/fixture AND functions defined
    # lexically inside them (callbacks like a `case_h` passed to a helper).
    # iterate: a function is fixture iff it has >=1 caller and every caller
    # is already fixture (transitively).
    defs = set()
    lexical_parent = {}

    def walk_defs(node, parent):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defs.add(child.name)
                lexical_parent[child.name] = parent
                walk_defs(child, child.name)
            else:
                walk_defs(child, parent)

    walk_defs(tree, None)

    callers = {name: set() for name in defs}
    referrers = {name: set() for name in defs}
    for caller, callee in scanner._calls:
        if callee in callers:
            callers[callee].add(caller)
    for referrer, name in scanner._refs:
        if name in referrers:
            referrers[name].add(referrer)

    fixture = set()
    for name in defs:
        probe, seen = name, set()
        while probe and probe not in seen:
            seen.add(probe)
            if "selftest" in probe.lower() or "fixture" in probe.lower():
                fixture.add(name)
                break
            probe = lexical_parent.get(probe)
    changed = True
    while changed:
        changed = False
        for name in defs - fixture:
            cs = callers[name]
            # every reference to the helper -- call, callback pass, or
            # argparse set_defaults(func=...) -- must come from fixture
            # code; a function with no callers is a live entry point.
            refs = referrers[name] - {name}
            if cs and cs <= fixture and (not refs or refs <= fixture):
                fixture.add(name)
                changed = True
    return scanner.sites, fixture


def python_context(path, line, enclosing, fixture_funcs, lines):
    note = annotation_for_line(lines[line - 1]) if 1 <= line <= len(lines) else None
    if note:
        return "annotated", ANNOTATION_REASONS[note]
    if "/fixtures/" in path:
        return "fixture", "path contains /fixtures/"
    for name in enclosing:
        lowered = name.lower()
        if "selftest" in lowered or "fixture" in lowered:
            return "fixture", f"enclosing function {name}()"
    if enclosing and enclosing[-1] in fixture_funcs:
        return "fixture", (
            f"called only from selftest/fixture functions ({enclosing[-1]}())")
    return "live", None


# ------------------------------------------------------------ sh scanner

GIT_RUN_RE = re.compile(r"\bgit\b\s+([^&|;<>()\n]*)")
SHELL_ASSIGN_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$")
SHELL_VAR_RE = re.compile(
    r'^(?:"?\$\{([A-Za-z_][A-Za-z0-9_]*)\}"?|"?\$([A-Za-z_][A-Za-z0-9_]*)"?)$')

# Value of an assignment RHS, or None: literal text, `${X:-default}`, or
# `${X-default}` contribute their fallback (the only statically known arm).
def _shell_assignment_value(rhs):
    # an assignment may share the line with a command (`V=${X:-HEAD}; git ...`)
    text = rhs.split(";", 1)[0]
    text = text.split("#", 1)[0].strip().rstrip(";").strip()
    if not text:
        return None
    match = re.fullmatch(r'"\$\{[^}:]+:?-([^}]*)\}"', text) or \
        re.fullmatch(r"\$\{[^}:]+:?-([^}]*)\}", text)
    if match:
        return match.group(1)
    if re.fullmatch(r'"[^"$`]*"', text) or re.fullmatch(r"[^$`\"']*", text):
        return text.strip('"')
    return None


def scan_shell(source):
    """[(line, kind)] — tokens per git run on each line.

    Simple intra-script variable table: `V=${REV:-HEAD}` then
    `git rev-parse "$V"` classifies the fallback HEAD, per amendment rule 3.
    """
    sites = []
    known = {}
    for lineno, raw in enumerate(source.splitlines(), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        assign = SHELL_ASSIGN_RE.match(raw)
        if assign:
            value = _shell_assignment_value(assign.group(2))
            if value is not None:
                known[assign.group(1)] = value
        for match in GIT_RUN_RE.finditer(raw):
            words = []
            for word in match.group(1).split():
                var = SHELL_VAR_RE.match(word)
                if var:
                    name = var.group(1) or var.group(2)
                    words.append(known.get(name, word))
                else:
                    words.append(word)
            tokens = [(w, lineno) for w in words]
            for kind in classify_argv(tokens, head_re=SHELL_HEAD_RE):
                sites.append((lineno, kind))
    return sites


# ------------------------------------------------------------------- lint

def _site_record(path, line, kind, context, code, reason=None):
    rec = {
        "path": path, "line": line, "kind": kind,
        "context": context, "code": code,
    }
    if reason:
        rec["reason"] = reason
    return rec


def lint(root, rev):
    resolved = resolve_rev(root, rev)
    paths = list_site_files(root, resolved)
    sites = []
    excluded = []
    scanned = 0
    for path in paths:
        blob = show(root, resolved, path)
        try:
            source = blob.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise LintError(f"{path}: not UTF-8: {exc}")
        seat_path = is_seat_path(path)
        lines = source.splitlines()

        if path.endswith(".sh"):
            found = []
            for line, kind in scan_shell(source):
                code = lines[line - 1].strip() if line <= len(lines) else ""
                note = annotation_for_line(lines[line - 1]) \
                    if line <= len(lines) else None
                if note:
                    found.append(_site_record(
                        path, line, kind, "annotated", code,
                        ANNOTATION_REASONS[note]))
                else:
                    context = "fixture" if "/fixtures/" in path else "live"
                    reason = ("path contains /fixtures/"
                              if context == "fixture" else None)
                    found.append(_site_record(path, line, kind, context,
                                              code, reason))
        else:
            try:
                py_sites, fixture_funcs = scan_python(source)
            except SyntaxError as exc:
                raise LintError(f"{path}: unparseable Python: {exc}")
            found = []
            for line, kind, enclosing in py_sites:
                context, reason = python_context(
                    path, line, enclosing, fixture_funcs, lines)
                found.append(_site_record(
                    path, line, kind, context,
                    lines[line - 1].strip() if line <= len(lines) else "",
                    reason))

        if seat_path:
            excluded.append({
                "path": path,
                "reason": EXCLUDED_REASON,
                "sites": found,
            })
            continue
        scanned += 1
        sites.extend(found)

    sites.sort(key=lambda s: (s["path"], s["line"], s["kind"]))
    live = sum(1 for s in sites if s["context"] == "live")
    annotated = sum(1 for s in sites if s["context"] == "annotated")
    return {
        "rev": resolved,
        "files_scanned": scanned,
        "sites": sites,
        "live_count": live,
        "fixture_count": len(sites) - live - annotated,
        "annotated_count": annotated,
        "routed_sites": ROUTED_SITES,
        "excluded": excluded,
        "limits": LIMITS,
    }


def evaluate(root, rev, strict):
    result = lint(root, rev)
    code = 1 if (strict and result["live_count"] > 0) else 0
    return result, code


# --------------------------------------------------------------- selftest

FIXTURE_LIVE_PY = '''import argparse
import subprocess


def main():
    subprocess.run(["git", "-C", ".", "rev-parse", "HEAD"])
    subprocess.run(["git", "branch", "--show-current"])
    subprocess.run(["git", "show", "HEAD:LOG.md"])
    subprocess.run(["git", "rev-list", "HEAD"])
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")


def compare_head():
    subprocess.run(["git", "rev-parse", "HEAD"])  # head-rev-lint: compare-only
'''

FIXTURE_EDGE_PY = '''import subprocess


def main(path):
    subprocess.run(["git", "show", f"HEAD:{path}"])
    subprocess.run(["git", "rev-parse", "HEAD^{commit}"])
    subprocess.run(["git", "log", "--format=%H", "HEAD~3"])
    subprocess.run(["git", "rev-parse", "@"])
    subprocess.run(["git", "show", f"{path}:LOG.md"])
'''

FIXTURE_CTX_PY = '''import subprocess


def selftest():
    subprocess.run(["git", "rev-parse", "HEAD"])

    def _inner():
        subprocess.run(["git", "rev-parse", "HEAD"])


def build_fixture_repo():
    subprocess.run(["git", "-C", "r", "rev-parse", "HEAD"])


def _commit(repo):
    # called only from selftest -> fixture by the transitive-caller rule
    return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])
'''

FIXTURE_CTX2_PY = '''import subprocess


def selftest():
    _commit("/tmp/x")


def _commit(repo):
    return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"])


def live_helper():
    subprocess.run(["git", "-C", ".", "rev-parse", "HEAD"])
'''

FIXTURE_CLEAN_PY = '''import argparse
import subprocess


def main():
    subprocess.run(["git", "-C", ".", "rev-parse", "--verify",
                    "abc123" + "^{commit}"])
    subprocess.run(["git", "show", "abc123:LOG.md"])
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="main")
    rev = "HEAD"  # a bare string is not a git argv: no site
    return rev
'''

FIXTURE_SEAT_PY = '''import subprocess


def seat_probe():
    subprocess.run(["git", "rev-parse", "HEAD"])
'''

FIXTURE_RUN_SH = """#!/bin/sh
# rebuild fixture
R=$(git rev-parse HEAD)
git rev-parse @{u}
V=${REV:-HEAD}; git rev-parse "$V"
git show HEAD:LOG.md
"""


def _fixture_git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, "-c", "user.email=selftest@invalid",
         "-c", "user.name=selftest", "-c", "commit.gpgsign=false",
         *args],
        check=True, capture_output=True, timeout=60,
    )


def _write(repo, rel, text):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _commit(repo, msg):
    _fixture_git(repo, "add", "-A")
    _fixture_git(repo, "commit", "-q", "-m", msg)
    out = _fixture_git(repo, "rev-parse", "--verify", "main").stdout
    return out.decode("utf-8").strip()


def selftest():
    tmp = tempfile.mkdtemp(prefix="head-rev-lint-selftest-")
    try:
        repo = os.path.join(tmp, "lane")
        os.makedirs(repo)
        _fixture_git(repo, "init", "-q", "-b", "main")

        cases = 0
        # commit 1 (red, named reason: live_head_sites): every kind live,
        # every context exercised, one seat-dir exclusion.
        _write(repo, ".ufo/waves/round-17/live.py", FIXTURE_LIVE_PY)
        _write(repo, ".ufo/waves/round-17/edge.py", FIXTURE_EDGE_PY)
        _write(repo, ".ufo/waves/round-17/ctx.py", FIXTURE_CTX_PY)
        _write(repo, ".ufo/waves/round-17/ctx2.py", FIXTURE_CTX2_PY)
        _write(repo, ".ufo/waves/round-17/clean.py", FIXTURE_CLEAN_PY)
        _write(repo, ".ufo/waves/round-17/w2/seat.py", FIXTURE_SEAT_PY)
        _write(repo, ".ufo/gates/run.sh", FIXTURE_RUN_SH)
        rev1 = _commit(repo, "rev1")

        result, code = evaluate(repo, rev1, strict=True)
        cases += 1
        kinds_live = {s["kind"] for s in result["sites"]
                      if s["context"] == "live"}
        want_kinds = {"rev-parse-HEAD", "default-HEAD", "HEAD-colon",
                      "upstream", "other-HEAD"}
        # live: live.py x5 (rev-parse, upstream, HEAD-colon, other-HEAD,
        #       default-HEAD) + edge.py x4 (HEAD:{path}, HEAD^{commit},
        #       HEAD~3, @) + ctx.py uncalled _commit +
        #       ctx2.live_helper + run.sh x5 (rev-parse, upstream,
        #       ${V:-HEAD} rev-parse, rev-parse @{u}, HEAD-colon) = 15.
        assert code == 1, (result, code)
        assert result["live_count"] == 15, (
            result["live_count"], result["sites"])
        assert result["fixture_count"] == 4, result["fixture_count"]
        assert result["annotated_count"] == 1, result["annotated_count"]
        assert kinds_live == want_kinds, kinds_live
        assert result["files_scanned"] == 6, result["files_scanned"]
        assert len(result["excluded"]) == 1
        assert result["excluded"][0]["path"].endswith("/w2/seat.py")
        assert result["excluded"][0]["sites"], result["excluded"]
        assert result["routed_sites"], result["routed_sites"]

        # revision-literal edge forms (HEAD:{p}, HEAD^{commit}, HEAD~3, @)
        edge = [s for s in result["sites"] if s["path"].endswith("edge.py")]
        assert [(s["line"], s["kind"]) for s in edge] == [
            (5, "HEAD-colon"), (6, "rev-parse-HEAD"),
            (7, "other-HEAD"), (8, "rev-parse-HEAD"),
        ], edge

        # called-only-from-selftest exercised: ctx2._commit is fixture,
        # ctx.py._commit (uncalled) is live above.
        ctx2 = [s for s in result["sites"] if s["path"].endswith("ctx2.py")]
        assert [s["context"] for s in ctx2] == ["fixture", "live"], ctx2

        # commit 2: only fixture-context sites remain -> strict clean.
        _write(repo, ".ufo/waves/round-17/fixtures/rebuild.sh",
               "#!/bin/sh\nR=$(git rev-parse HEAD)\n")
        _write(repo, ".ufo/waves/round-17/ctx.py", '''import subprocess


def selftest():
    subprocess.run(["git", "rev-parse", "HEAD"])
''')
        _write(repo, ".ufo/waves/round-17/ctx2.py", FIXTURE_CLEAN_PY)
        _fixture_git(repo, "rm", "-q", ".ufo/waves/round-17/live.py",
                     ".ufo/waves/round-17/edge.py", ".ufo/gates/run.sh")
        rev2 = _commit(repo, "rev2")
        result, code = evaluate(repo, rev2, strict=True)
        cases += 1
        assert code == 0, (result, code)
        assert result["live_count"] == 0, result["live_count"]
        assert result["fixture_count"] == 2, result["fixture_count"]

        # commit 3: no sites at all.
        _fixture_git(repo, "rm", "-q", ".ufo/waves/round-17/ctx.py",
                     ".ufo/waves/round-17/fixtures/rebuild.sh")
        rev3 = _commit(repo, "rev3")
        result, code = evaluate(repo, rev3, strict=True)
        cases += 1
        assert code == 0, (result, code)
        assert result["live_count"] == 0 and result["fixture_count"] == 0
        assert result["annotated_count"] == 0
        assert result["sites"] == []

        return cases
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# -------------------------------------------------------------------- cli

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Count HEAD-keyed git revision sites in lane tooling "
                    "at a pinned revision."
    )
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)

    if args.selftest:
        try:
            cases = selftest()
        except AssertionError as exc:
            print(f"SELFTEST: FAILED {exc}")
            return 1
        except LintError as exc:
            print(f"SELFTEST: FAILED lint_error {exc}")
            return 1
        print(f"SELFTEST: CLEAN cases={cases}")
        return 0

    if not args.root or not args.rev:
        print("--root and --rev are required unless --selftest",
              file=sys.stderr)
        return 2
    try:
        result, code = evaluate(args.root, args.rev, args.strict)
    except LintError as exc:
        print(f"could-not-evaluate: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
