#!/usr/bin/env python3
"""v3-refparse.py - reference reader/classifier for the DRAFT SquashFS triage table v3.

Seat R41C2TableDraft (round 41, wave 1). This is a *draft* artifact, not the round-41
interpreter: it exists so the block in ``block20.md`` is proved to parse and to decide
before the freeze, the failure mode round 40 hit (``R40C2Shortcuts.md`` D1: a draft block
the interpreter refused with exit 2).

It is a v2-grammar reader (``tools/round-40/sqfs-triage-v2.py`` docstring, read
2026-10-26) with exactly three deltas, all listed in ``rationale.md`` §2:

  D1  marker ``<!-- sqfs-triage-table v3 -->``.
  D2  a ``kind+`` cell (a single name with one trailing ``+``) in ``gap kinds`` and in
      ``dependencies`` is a CONTAINS test: the feature set holds ``kind``. Every other
      non-``*`` cell in those two columns stays exact-set equality, ``none`` is the empty
      set, and ``a+b+`` is malformed (exit 2), because the precedence text never asks for
      two simultaneous contains.
  D3  a ``none-v4`` cell in ``handler`` matches when no handler starts with
      ``squashfs_v4_`` (precedence clause 2 reads "no ``squashfs_v4_*`` handler in H",
      which a v1-v3 chunk does not satisfy).

Everything else is the frozen v2 grammar: the twelve columns in order, the marker and the
closed action vocabulary inside ``## Queue-drain craft``, first full match top to bottom,
unique labels, ``unclassified`` reserved for the no-match pair, ``*`` for any, exact
operation/provider, ``none``/fnmatch handler, ``yes|no|n/a|*``, ``0|>0|*``, a ``cause``
cell that must contain ``->``, malformed anything -> exit 2.

Usage
  python3 -I -B v3-refparse.py --skill SKILL.md ENVELOPE.json...      -> path<TAB>label<TAB>action
  python3 -I -B v3-refparse.py --skill SKILL.md --json ENVELOPE...    -> features + row per envelope
  python3 -I -B v3-refparse.py --skill SKILL.md --table-only          -> parsed rules + vocabulary
  python3 -I -B v3-refparse.py --selftest                             -> grammar selftest, exit 1 on failure
Exit codes: 0 ok, 2 table missing/malformed or envelope unreadable, 1 failed --selftest.
"""

import argparse
import fnmatch
import json
import shlex
import sys

MARKER = "<!-- sqfs-triage-table v3 -->"
OLD_MARKERS = ("<!-- sqfs-triage-table v1 -->", "<!-- sqfs-triage-table v2 -->")
ACTIONS_PREFIX = "<!-- sqfs-triage-actions:"
SECTION = "## Queue-drain craft"
HEADER = [
    "label", "operation", "provider", "handler", "gap kinds", "dependencies",
    "-be in child argv", "symlink removed", "published files", "action", "cause", "source",
]
NOMATCH = ("unclassified", "none")


class TableError(Exception):
    pass


# --------------------------------------------------------------------------- table parse

def _cells(line):
    stripped = line.strip()
    if not stripped.startswith("|"):
        raise TableError("not a table row: %r" % line)
    body = stripped[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def _section_lines(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == SECTION:
            start = i
            break
    if start is None:
        raise TableError("no %r heading: the marker must sit inside the craft section" % SECTION)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return start, end, lines


def _strip_cell(text):
    value = text.strip()
    while len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        value = value[1:-1].strip()
    return value


def parse_set_cell(raw, column, lineno):
    value = _strip_cell(raw)
    if value == "*":
        return ("any", None)
    if value == "none":
        return ("exact", frozenset())
    if value.endswith("+"):
        name = value[:-1]
        if not name or "+" in name or name == "*" or name == "none" or "|" in name:
            raise TableError("line %d: malformed contains cell %r in %s" % (lineno, raw, column))
        return ("contains", name)
    names = value.split("+")
    for name in names:
        if not name or name == "*" or "|" in name or name == "none":
            raise TableError("line %d: malformed exact-set cell %r in %s" % (lineno, raw, column))
    return ("exact", frozenset(names))


def parse_handler_cell(raw, lineno):
    value = _strip_cell(raw)
    if value == "*":
        return ("any", None)
    if value == "none":
        return ("none", None)
    if value == "none-v4":
        return ("none-v4", None)
    if "|" in value or value == "":
        raise TableError("line %d: malformed handler cell %r" % (lineno, raw))
    return ("pattern", value)


def parse_enum_cell(raw, allowed, column, lineno):
    value = _strip_cell(raw)
    if value not in allowed:
        raise TableError("line %d: %s cell %r not in %s" % (lineno, column, raw, sorted(allowed)))
    return value


def parse_table(text):
    start, end, lines = _section_lines(text)
    marker = None
    for i in range(start + 1, end):
        if lines[i].strip() == MARKER:
            marker = i
            break
        if lines[i].strip() in OLD_MARKERS:
            raise TableError("line %d: %r marker is not the v3 marker" % (i + 1, lines[i].strip()))
    if marker is None:
        raise TableError("marker %r absent from the craft section" % MARKER)

    header_at = None
    for j in range(marker + 1, end):
        if lines[j].strip().startswith("|"):
            header_at = j
            break
    if header_at is None:
        raise TableError("no table after the v3 marker")

    header = [h.lower() for h in _cells(lines[header_at])]
    if header != HEADER:
        raise TableError("header %r != expected %r" % (header, HEADER))

    k = header_at - 1
    while k > marker and lines[k].strip() == "":
        k -= 1
    actions_line = lines[k].strip()
    if not actions_line.startswith(ACTIONS_PREFIX) or not actions_line.endswith("-->"):
        raise TableError("line %d: action vocabulary line missing directly above the table" % (k + 1))
    tokens = actions_line[len(ACTIONS_PREFIX):-3].split()
    vocabulary = []
    for token in tokens:
        if not token or not all(c.islower() or c.isdigit() or c == "-" for c in token):
            raise TableError("action token %r is not a lowercase dashed word" % token)
        if token in vocabulary:
            raise TableError("duplicate action token %r" % token)
        vocabulary.append(token)

    sep_at = header_at + 1
    sep = _cells(lines[sep_at])
    if len(sep) != len(HEADER) or not all(set(c) <= set("-: ") and c for c in sep):
        raise TableError("line %d: bad separator row" % (sep_at + 1))

    rules = []
    labels = set()
    row = 0
    for j in range(sep_at + 1, end):
        line = lines[j]
        if not line.strip().startswith("|"):
            if rules:
                break
            raise TableError("line %d: table body interrupted" % (j + 1))
        cells = _cells(line)
        if len(cells) != len(HEADER):
            raise TableError("line %d: %d cells, expected %d" % (j + 1, len(cells), len(HEADER)))
        row += 1
        label = _strip_cell(cells[0])
        if not label:
            raise TableError("line %d: empty label" % (j + 1))
        if label in labels:
            raise TableError("line %d: duplicate label %r" % (j + 1, label))
        if label == NOMATCH[0]:
            raise TableError("line %d: label %r is reserved for the no-match pair" % (j + 1, label))
        labels.add(label)
        operation = _strip_cell(cells[1])
        provider = _strip_cell(cells[2])
        action = _strip_cell(cells[9])
        cause = cells[10]
        source = cells[11]
        if action not in vocabulary:
            raise TableError("line %d: action %r not declared in the vocabulary line" % (j + 1, action))
        if not cause.strip() or "->" not in cause:
            raise TableError("line %d: cause cell must be prose containing '->'" % (j + 1))
        if not source.strip():
            raise TableError("line %d: empty source cell" % (j + 1))
        rules.append({
            "row": row,
            "label": label,
            "operation": ("any", None) if operation == "*" else ("exact", operation),
            "provider": ("any", None) if provider == "*" else ("exact", provider),
            "handler": parse_handler_cell(cells[3], j + 1),
            "gap_kinds": parse_set_cell(cells[4], "gap kinds", j + 1),
            "dependencies": parse_set_cell(cells[5], "dependencies", j + 1),
            "be": parse_enum_cell(cells[6], {"yes", "no", "n/a", "*"}, "-be", j + 1),
            "sr": parse_enum_cell(cells[7], {"yes", "no", "n/a", "*"}, "symlink removed", j + 1),
            "published": parse_enum_cell(cells[8], {"0", ">0", "*"}, "published files", j + 1),
            "action": action,
            "cause": cause.strip(),
            "source": source.strip(),
        })
    if not rules:
        raise TableError("table has no data rows")
    return {"rules": rules, "vocabulary": vocabulary, "marker_line": marker + 1,
            "header_line": header_at + 1}


# --------------------------------------------------------------------------- features

def _commands(obj, sink):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "command":
                sink.append(value)
            else:
                _commands(value, sink)
    elif isinstance(obj, list):
        for value in obj:
            _commands(value, sink)


def _carries_be(token_list):
    return "-be" in token_list


def envelope_data(payload):
    if not isinstance(payload, dict):
        raise TableError("envelope is not an object")
    if "data" in payload and isinstance(payload["data"], dict):
        return payload["data"]
    return payload


def features(envelope):
    data = envelope_data(envelope)
    result = data.get("normalized_result")
    operation = data.get("operation") if isinstance(data.get("operation"), str) else ""
    provider = data.get("provider")
    if isinstance(provider, dict):
        provider_id = provider.get("id") if isinstance(provider.get("id"), str) else ""
    elif isinstance(provider, str):
        provider_id = provider
    else:
        provider_id = ""
    if operation == "extract_firmware" and not isinstance(result, dict):
        raise TableError("extract_firmware envelope without a normalized_result object")
    result = result if isinstance(result, dict) else {}
    handlers = set()
    for chunk in result.get("chunks") or []:
        if isinstance(chunk, dict) and isinstance(chunk.get("handler"), str):
            handlers.add(chunk["handler"])
    handlers = {h for h in handlers if h.startswith("squashfs")}
    gaps = [g for g in (result.get("extraction_gaps") or []) if isinstance(g, dict)]
    kinds = {g.get("kind") for g in gaps if isinstance(g.get("kind"), str)}
    deps = set()
    for gap in gaps:
        for dep in gap.get("dependencies") or []:
            if isinstance(dep, str):
                deps.add(dep)
    commands = []
    for report in result.get("diagnostics") or []:
        if isinstance(report, dict):
            _commands(report.get("report"), commands)
    for report in data.get("diagnostics") or []:
        if isinstance(report, dict):
            _commands(report.get("report"), commands)
    _commands(data.get("raw_result"), commands)
    sasquatch = []
    for command in commands:
        tokens = shlex.split(command) if isinstance(command, str) else [str(t) for t in command]
        if not tokens:
            continue
        if any("sasquatch" in t for t in tokens[:1]) or any("sasquatch" in t for t in tokens):
            sasquatch.append(tokens)
    if not sasquatch:
        be = "n/a"
    elif any(_carries_be(tokens) for tokens in sasquatch):
        be = "yes"
    else:
        be = "no"
    removed = False
    for report in result.get("diagnostics") or []:
        if isinstance(report, dict) and isinstance(report.get("report"), dict):
            if report["report"].get("__typename__") == "MaliciousSymlinkRemoved":
                removed = True
    if not removed and "MaliciousSymlinkRemoved" in json.dumps(data.get("raw_result") or {}):
        removed = True
    files = result.get("files") or []
    return {
        "OP": operation, "PV": provider_id, "H": handlers, "G": kinds, "D": deps,
        "BE": be, "SR": "yes" if removed else "no", "P": len(files),
    }


# --------------------------------------------------------------------------- match

def _set_matches(cell, observed, feature):
    mode, value = cell
    if mode == "any":
        return True
    if mode == "exact":
        return frozenset(observed) == value
    if mode == "contains":
        return value in observed
    raise TableError("unknown set cell mode %r for %s" % (mode, feature))


def _handler_matches(cell, handlers):
    mode, value = cell
    if mode == "any":
        return True
    if mode == "none":
        return not handlers
    if mode == "none-v4":
        return not any(h.startswith("squashfs_v4_") for h in handlers)
    return any(fnmatch.fnmatchcase(h, value) for h in handlers)


def rule_matches(rule, feat):
    if rule["operation"][0] == "exact" and rule["operation"][1] != feat["OP"]:
        return False
    if rule["provider"][0] == "exact" and rule["provider"][1] != feat["PV"]:
        return False
    if not _handler_matches(rule["handler"], feat["H"]):
        return False
    if not _set_matches(rule["gap_kinds"], feat["G"], "G"):
        return False
    if not _set_matches(rule["dependencies"], feat["D"], "D"):
        return False
    if rule["be"] != "*" and rule["be"] != feat["BE"]:
        return False
    if rule["sr"] != "*" and rule["sr"] != feat["SR"]:
        return False
    if rule["published"] == "0" and feat["P"] != 0:
        return False
    if rule["published"] == ">0" and feat["P"] == 0:
        return False
    return True


def classify(table, envelope):
    feat = features(envelope)
    for rule in table["rules"]:
        if rule_matches(rule, feat):
            return feat, rule, (rule["label"], rule["action"])
    return feat, None, NOMATCH


# --------------------------------------------------------------------------- selftest

MINI = """## Queue-drain craft

- test block.

  <!-- sqfs-triage-table v3 -->
  <!-- sqfs-triage-actions: none red blue green -->
  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | a-nochunk | `extract_firmware` | `unblob` | `none-v4` | `*` | `*` | `*` | `*` | `*` | `none` | a test row -> act | S1 :1 |
  | b-contains | `extract_firmware` | `unblob` | `squashfs_v4_*` | `fail+` | `*` | `*` | `*` | `>0` | `red` | b test row -> act | S1 :2 |
  | c-exact | `extract_firmware` | `unblob` | `squashfs_v4_*` | `keep` | `*` | `*` | `*` | `*` | `blue` | c test row -> act | S1 :3 |
  | d-depplus | `extract_firmware` | `unblob` | `squashfs_v4_*` | `dep+` | `sasquatch-v4be+` | `*` | `*` | `*` | `green` | d test row -> act | S1 :4 |
"""


def _env(handler="squashfs_v4_le", kinds=(), deps=(), files=0, operation="extract_firmware",
         provider="unblob", be=None, removed=False):
    result = {"chunks": [], "extraction_gaps": [], "files": [{"path": "f%d" % i} for i in range(files)],
              "diagnostics": []}
    if handler:
        result["chunks"].append({"handler": handler})
    for kind in kinds:
        result["extraction_gaps"].append({"kind": kind, "dependencies": list(deps) if kind == "dep" else []})
    if be is not None:
        argv = ["sasquatch-v4be"] + (["-be"] if be else []) + ["-no-exit-code", "-f"]
        result["diagnostics"].append({"report": {"command": " ".join(argv)}})
    if removed:
        result["diagnostics"].append({"report": {"__typename__": "MaliciousSymlinkRemoved"}})
    data = {"operation": operation, "provider": {"id": provider}, "normalized_result": result}
    return {"ok": True, "data": data, "meta": {}}


def selftest():
    cases = []

    def case(name, expect_label, expect_action, envelope, table_text=MINI):
        try:
            table = parse_table(table_text)
        except TableError as exc:
            cases.append((name, False, "parse: %s" % exc))
            return
        _, rule, pair = classify(table, envelope)
        ok = pair == (expect_label, expect_action)
        cases.append((name, ok, "row=%s got=%s want=%s" % (
            rule["row"] if rule else None, pair, (expect_label, expect_action))))

    def case_error(name, table_text):
        try:
            parse_table(table_text)
        except TableError as exc:
            cases.append((name, True, "refused: %s" % exc))
            return
        cases.append((name, False, "accepted a malformed table"))

    # D3: none-v4 fires on an empty handler set and on a v1-v3 chunk, not on a v4 chunk.
    case("none-v4 on empty H", "a-nochunk", "none", _env(handler=None, files=0))
    case("none-v4 on v3 chunk", "a-nochunk", "none", _env(handler="squashfs_v3", files=2))
    case("v4 chunk skips row 1", "c-exact", "blue", _env(handler="squashfs_v4_le", kinds=("keep",), files=1))
    # D2: contains matches a superset, exact does not.
    case("contains on superset", "b-contains", "red",
         _env(kinds=("fail", "keep"), files=2))
    case("exact refuses superset", "unclassified", "none",
         _env(kinds=("keep", "extra"), files=1))
    case("exact singleton", "c-exact", "blue", _env(kinds=("keep",), files=1))
    case("contains misses absent", "c-exact", "blue", _env(kinds=("keep",), files=1))
    case("dependency contains", "d-depplus", "green",
         _env(kinds=("dep",), deps=("sasquatch-v4be",), files=0))
    case("dependency contains absent falls through", "unclassified", "none",
         _env(kinds=("dep",), deps=("sasquatch",), files=0))
    # order: the contains row above the exact row wins when both can match.
    case("order first match", "b-contains", "red", _env(kinds=("fail",), files=3))
    # domain guard.
    case("domain guard", "unclassified", "none", _env(operation="inspect_firmware_regions"))
    case("provider guard", "unclassified", "none", _env(provider="binwalk"))
    # grammar errors.
    case_error("two contains rejected", MINI.replace("`fail+` | `*`", "`fail+keep+` | `*`"))
    case_error("cause without arrow", MINI.replace("a test row -> act", "a test row act"))
    case_error("duplicate label", MINI.replace("| c-exact |", "| b-contains |"))
    case_error("unknown action", MINI.replace("| `blue` |", "| `mauve` |"))
    case_error("reserved label", MINI.replace("| c-exact |", "| unclassified |"))
    case_error("v2 marker only", MINI.replace(MARKER, "<!-- sqfs-triage-table v2 -->"))
    case_error("no craft heading", MINI.replace(SECTION, "## Something else"))
    case_error("bad header", MINI.replace("| published files |", "| files |"))
    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, detail in cases:
        print("%-5s %-34s %s" % ("ok" if ok else "FAIL", name, detail))
    print("\ncases=%d pass=%d fail=%d" % (len(cases), passed, len(cases) - passed))
    return 0 if passed == len(cases) else 1


# --------------------------------------------------------------------------- main

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as exc:
        raise TableError("unreadable envelope %s: %s" % (path, exc))


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("envelopes", nargs="*")
    parser.add_argument("--skill", required=False)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--table-only", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.skill:
        parser.error("--skill is required")
    try:
        with open(args.skill, "r", encoding="utf-8") as handle:
            table = parse_table(handle.read())
    except OSError as exc:
        print("v3-refparse: %s" % exc, file=sys.stderr)
        return 2
    except TableError as exc:
        print("v3-refparse: %s" % exc, file=sys.stderr)
        return 2
    if args.table_only:
        print("marker line %d, header line %d, rules %d" % (
            table["marker_line"], table["header_line"], len(table["rules"])))
        print("vocabulary: %s" % " ".join(table["vocabulary"]))
        for rule in table["rules"]:
            print("row %2d %-28s %-20s %s" % (
                rule["row"], rule["label"], rule["action"],
                "gap=%s deps=%s be=%s sr=%s pub=%s" % (
                    rule["gap_kinds"], rule["dependencies"], rule["be"], rule["sr"],
                    rule["published"])))
        return 0
    payloads = []
    for path in args.envelopes:
        try:
            payloads.append((path, load_json(path)))
        except TableError as exc:
            print("v3-refparse: %s" % exc, file=sys.stderr)
            return 2
    rows = []
    for path, payload in payloads:
        try:
            feat, rule, pair = classify(table, payload)
        except TableError as exc:
            print("v3-refparse: %s: %s" % (path, exc), file=sys.stderr)
            return 2
        rows.append({"path": path, "label": pair[0], "action": pair[1],
                     "row": rule["row"] if rule else None,
                     "features": {k: (sorted(v) if isinstance(v, set) else v) for k, v in feat.items()}})
    if args.json:
        print(json.dumps(rows, indent=1, sort_keys=True))
    else:
        for row in rows:
            print("%s\t%s\t%s" % (row["path"], row["label"], row["action"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
