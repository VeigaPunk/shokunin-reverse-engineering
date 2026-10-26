#!/usr/bin/env python3
"""Independent evaluator for the round-40 SKILL `sqfs-triage-table v2` grammar.

Written from (a) the column header line of the table, (b) the prose of
corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md, and (c) the envelope shape that
REA 6.5.0 emits.  It imports nothing from, and never reads, tools/round-40/sqfs-triage-v2.py.

Grammar implemented (first match over table rows, top to bottom):

  columns, in header order:
    label | operation | provider | handler | gap kinds | dependencies |
    -be in child argv | symlink removed | published files | action | cause | source

  cell forms
    `*`          any value
    `none`       the empty set / "no chunk handler at all" (set predicate, not a value)
    `n/a`        feature not observable (no child command was recorded)
    `path/*`     glob over names, `*` matching any run
    `>0`, `0`    numeric comparison on the published regular-file count
    bare token   exact string equality (after stripping enclosing backticks)

  features, per envelope (all from `envelope.json`):
    operation        envelope.operation
    provider         envelope.provider.id
    handler          set of normalized_result.chunks[].handler, non-null
    gap kinds        set of normalized_result.extraction_gaps[].kind
    dependencies     set union of normalized_result.extraction_gaps[].dependencies
    -be in argv      yes | no | n/a   (yes: a recorded child command carries the exact
                                      token -be; no: a command was recorded and none does;
                                      n/a: no command recorded)
    symlink removed  present of a MaliciousSymlinkRemoved diagnostic report
    published files  count of normalized_result.files

  no row matches              -> ("unclassified", "none")

Deliberate, declared reading choices (each is reported by --ambiguities):
  A1 gap kinds / dependencies: cell token vs observed set -- exact set equality is the
     primary reading (`--gap-match eq`); membership (`member`) is the alternative.
  A2 handler `none` is a set predicate (empty handler set); a pattern cell requires a
     non-empty handler set, so the empty set never satisfies `squashfs_v4_*`.
  A3 `-be ... no` requires a recorded child command without the token `-be`
     (`--be-absent-is-no` widens `no` to also cover an unrecorded command).
  A4 operation/provider are matched literally; `--no-domain-guard` removes them.
  A5 published-file count counts every entry of normalized_result.files, nested carves
     included; only 0 vs >0 is ever asked of it here.

Exit: 0 every envelope matched, 1 mismatch, 2 table missing/malformed.
"""

import argparse
import fnmatch
import gzip
import json
import os
import re
import shlex
import sys

MARKER = "<!-- sqfs-triage-table v2 -->"
ACTIONS_RE = re.compile(r"<!--\s*sqfs-triage-actions:\s*(.*?)\s*-->")
COLUMNS = [
    "label",
    "operation",
    "provider",
    "handler",
    "gap kinds",
    "dependencies",
    "-be in child argv",
    "symlink removed",
    "published files",
    "action",
    "cause",
    "source",
]


class TableError(Exception):
    pass


def unquote(cell):
    cell = cell.strip()
    if len(cell) >= 2 and cell[0] == "`" and cell[-1] == "`":
        return cell[1:-1].strip()
    return cell


def split_row(line):
    """Split a markdown table line into cells, tolerating leading/trailing pipes."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [unquote(c) for c in body.split("|")]


def parse_table(text):
    lines = text.splitlines()
    marker_at = None
    for i, line in enumerate(lines):
        if MARKER in line:
            marker_at = i
            break
    if marker_at is None:
        raise TableError("no %s marker" % MARKER)

    actions = None
    header_at = None
    for i in range(marker_at + 1, min(len(lines), marker_at + 12)):
        line = lines[i]
        m = ACTIONS_RE.search(line)
        if m and actions is None:
            actions = m.group(1).split()
            continue
        cells = split_row(line) if line.strip().startswith("|") else None
        if cells and [c.lower() for c in cells] == COLUMNS:
            header_at = i
            break
    if header_at is None:
        raise TableError("no header row with the 12 expected columns after the marker")
    if actions is None:
        raise TableError("no <!-- sqfs-triage-actions: ... --> line after the marker")

    sep = lines[header_at + 1] if header_at + 1 < len(lines) else ""
    if not sep.strip().startswith("|") or not all(
        set(c) <= {"-", ":", " "} for c in split_row(sep)
    ):
        raise TableError("header not followed by a separator row")

    rows = []
    for i in range(header_at + 2, len(lines)):
        line = lines[i]
        if not line.strip().startswith("|"):
            break
        cells = split_row(line)
        if len(cells) != len(COLUMNS):
            raise TableError("row %d has %d cells, want %d: %r"
                             % (i + 1, len(cells), len(COLUMNS), line[:80]))
        rows.append(dict(zip(COLUMNS, cells)))
    if not rows:
        raise TableError("marker present but no data rows")

    # grammar sanity that does not depend on any envelope
    labels = [r["label"] for r in rows]
    if len(set(labels)) != len(labels):
        raise TableError("duplicate label: %r" % labels)
    vocab = set(actions)
    extra = sorted({r["action"] for r in rows} - vocab)
    if extra:
        raise TableError("row action(s) %r absent from the actions line" % extra)
    unused = sorted(vocab - {r["action"] for r in rows})
    return {
        "rows": rows,
        "actions": actions,
        "marker_line": marker_at + 1,
        "header_line": header_at + 1,
        "unused_actions": unused,
    }


def load_json(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rt") as fh:
            return json.load(fh)
    with open(path) as fh:
        return json.load(fh)


def envelope_features(env):
    nr = env.get("normalized_result") or {}
    chunks = nr.get("chunks") or []
    handlers = [c.get("handler") for c in chunks if c.get("handler")]
    gaps = nr.get("extraction_gaps") or []
    kinds = {g.get("kind") for g in gaps if g.get("kind")}
    deps = set()
    for g in gaps:
        for d in g.get("dependencies") or []:
            deps.add(d)
    diag = nr.get("diagnostics") or []
    sr = False
    argv = []
    for d in diag:
        rep = d.get("report") or {}
        if rep.get("__typename__") == "MaliciousSymlinkRemoved":
            sr = True
        cmd = rep.get("command")
        if isinstance(cmd, str) and cmd.strip():
            try:
                argv.append(shlex.split(cmd))
            except ValueError:
                argv.append(cmd.split())
    tokens = [t for a in argv for t in a]
    if not argv:
        be = "n/a"
    elif any(t == "-be" for t in tokens):
        be = "yes"
    else:
        be = "no"
    files = nr.get("files") or []
    return {
        "operation": env.get("operation"),
        "provider": (env.get("provider") or {}).get("id"),
        "handlers": handlers,
        "gap_kinds": sorted(kinds),
        "dependencies": sorted(deps),
        "be": be,
        "symlink_removed": sr,
        "published": len(files),
        "argv_count": len(argv),
        "gap_list": [{"kind": g.get("kind"), "deps": g.get("dependencies") or []} for g in gaps],
        "diagnostics": [((d.get("report") or {}).get("__typename__")) for d in diag],
        "coverage": nr.get("coverage"),
    }


def set_cell_match(cell, observed, mode, literal_none=False):
    observed = set(observed)
    if cell == "*":
        return True
    if cell == "none":
        if literal_none:
            return observed == {"none"}
        return len(observed) == 0
    if mode == "member":
        return cell in observed
    return observed == {cell}


def handler_cell_match(cell, handlers):
    if cell == "*":
        return True
    if cell == "none":
        return len(handlers) == 0
    if not handlers:
        return False
    return all(fnmatch.fnmatchcase(h, cell) for h in handlers)


def row_matches(row, f, opt):
    if not opt["no_domain_guard"]:
        for col, key in (("operation", "operation"), ("provider", "provider")):
            cell = row[col]
            if cell != "*" and cell != f[key]:
                return False
    if not handler_cell_match(row["handler"], f["handlers"]):
        return False
    ln = opt.get("literal_none", False)
    if not set_cell_match(row["gap kinds"], f["gap_kinds"], opt["gap_match"], ln):
        return False
    if not set_cell_match(row["dependencies"], f["dependencies"], opt["gap_match"], ln):
        return False
    be = row["-be in child argv"]
    if be == "*":
        pass
    elif be == "n/a":
        if f["be"] != "n/a":
            return False
    elif be == "no":
        ok = {"no"} | ({"n/a"} if opt["be_absent_is_no"] else set())
        if f["be"] not in ok:
            return False
    elif be == "yes":
        if f["be"] != "yes":
            return False
    else:
        return False
    sr = row["symlink removed"]
    if sr == "yes" and not f["symlink_removed"]:
        return False
    if sr == "no" and f["symlink_removed"]:
        return False
    pub = row["published files"]
    if pub == "*":
        pass
    elif pub == "0":
        if f["published"] != 0:
            return False
    elif pub == ">0":
        if not f["published"] > 0:
            return False
    else:
        return False
    return True


def decide(table, f, opt):
    for idx, row in enumerate(table["rows"], start=1):
        if row_matches(row, f, opt):
            return {"row": idx, "label": row["label"], "action": row["action"]}
    return {"row": None, "label": "unclassified", "action": "none"}


def ablate(table, columns):
    """Return a copy of the table with every cell of the named columns set to `*`."""
    rows = []
    for row in table["rows"]:
        r = dict(row)
        for col in columns:
            if col in r and col not in ("label", "action", "cause", "source"):
                r[col] = "*"
        rows.append(r)
    return dict(table, rows=rows)


def collect_envelopes(dirpath):
    out = []
    for name in sorted(os.listdir(dirpath)):
        d = os.path.join(dirpath, name)
        if not os.path.isdir(d):
            continue
        for cand in ("envelope.json", "envelope.json.gz"):
            p = os.path.join(d, cand)
            if os.path.exists(p):
                out.append((name, p))
                break
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True, help="file holding the v2 table block")
    ap.add_argument("--envelopes", help="directory of H*/envelope.json[.gz]")
    ap.add_argument("--manifest", help="manifest.json with expected label/action")
    ap.add_argument("--table-only", action="store_true")
    ap.add_argument("--json-out")
    ap.add_argument("--gap-match", choices=["eq", "member"], default="eq")
    ap.add_argument("--be-absent-is-no", action="store_true")
    ap.add_argument("--no-domain-guard", action="store_true")
    ap.add_argument("--ablate", default="", help="comma list of columns to neutralise")
    ap.add_argument("--literal-none", action="store_true",
                    help="read a `none` cell as the literal token 'none', not the empty set")
    ap.add_argument("--quiet", action="store_true")
    opt = ap.parse_args(argv)

    with open(opt.skill, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    try:
        table = parse_table(text)
    except TableError as exc:
        print("table error: %s" % exc, file=sys.stderr)
        return 2

    columns = [c.strip() for c in opt.ablate.split(",") if c.strip()]
    working = ablate(table, columns) if columns else table

    report = {
        "skill": os.path.abspath(opt.skill),
        "table": {
            "rows": len(table["rows"]),
            "labels": [r["label"] for r in table["rows"]],
            "actions_line": table["actions"],
            "unused_actions": table["unused_actions"],
            "row_actions": [r["action"] for r in table["rows"]],
            "marker_line": table["marker_line"],
            "header_line": table["header_line"],
        },
        "options": {
            "gap_match": opt.gap_match,
            "be_absent_is_no": opt.be_absent_is_no,
            "no_domain_guard": opt.no_domain_guard,
            "literal_none": opt.literal_none,
            "ablated": columns,
        },
        "ambiguous_readings": {
            "A1_gap_sets": "cell token vs observed gap-kind/dependency set read as exact "
                           "set equality (primary) or membership (alternative)",
            "A2_handler_none": "`none` is the empty-handler-set predicate; pattern cells "
                               "require a non-empty set (--literal-none tests the token reading "
                               "for the set columns)",
            "A3_be_no": "`no` means 'a child command was recorded and it lacks the token "
                        "-be'; an unrecorded command is `n/a`",
            "A4_domain": "operation/provider matched by exact string equality",
            "A5_published": "counts every normalized_result.files entry incl. nested carves; "
                            "only the 0 / >0 split is used",
        },
    }

    if opt.table_only:
        if not opt.quiet:
            print(json.dumps(report["table"], indent=1))
        if opt.json_out:
            with open(opt.json_out, "w") as fh:
                json.dump(report, fh, indent=1, sort_keys=True)
        return 0

    if not opt.envelopes:
        print("--envelopes is required unless --table-only", file=sys.stderr)
        return 2

    expected = {}
    if opt.manifest:
        man = load_json(opt.manifest)
        for c in man["carriers"]:
            expected[c["id"]] = {
                "class": c.get("class"),
                "label": c.get("label"),
                "action": c.get("action"),
                "sha256": c.get("sha256"),
            }

    results = []
    matched = 0
    for cid, path in collect_envelopes(opt.envelopes):
        env = load_json(path)
        feats = envelope_features(env)
        d = decide(working, feats, {
            "gap_match": opt.gap_match,
            "be_absent_is_no": opt.be_absent_is_no,
            "no_domain_guard": opt.no_domain_guard,
            "literal_none": opt.literal_none,
        })
        exp = expected.get(cid) or {}
        ok = (d["label"] == exp.get("label") and d["action"] == exp.get("action"))
        matched += 1 if ok else 0
        results.append({
            "id": cid,
            "class": exp.get("class"),
            "decided_label": d["label"],
            "decided_action": d["action"],
            "row": d["row"],
            "expected_label": exp.get("label"),
            "expected_action": exp.get("action"),
            "agree": ok,
            "features": feats,
            "evidence_id": env.get("evidence_id"),
            "subject_sha256": ((env.get("subject") or {}).get("digest") or {}).get("sha256"),
        })

    n = len(results)
    wrong = [r for r in results if not r["agree"]]
    report.update({
        "n": n,
        "matched": matched,
        "all_agree": matched == n and n > 0,
        "wrong": [
            {"id": r["id"], "class": r["class"],
             "decided": [r["decided_label"], r["decided_action"]],
             "expected": [r["expected_label"], r["expected_action"]],
             "row": r["row"]}
            for r in wrong
        ],
        "results": results,
    })

    if not opt.quiet:
        print("%-4s %-26s %-24s %-24s %-4s %s" % ("id", "class", "decided", "expected", "row", "ok"))
        for r in results:
            print("%-4s %-26s %-24s %-24s %-4s %s" % (
                r["id"], r["class"],
                "%s/%s" % (r["decided_label"], r["decided_action"]),
                "%s/%s" % (r["expected_label"], r["expected_action"]),
                r["row"], "ok" if r["agree"] else "MISMATCH"))
        print("\nmatched %d/%d (table rows %d, %s reading%s)"
              % (matched, n, len(table["rows"]),
                 "eq" if opt.gap_match == "eq" else "member",
                 "" if not columns else "; ablated " + ",".join(columns)))

    if opt.json_out:
        with open(opt.json_out, "w") as fh:
            json.dump(report, fh, indent=1, sort_keys=True)

    return 0 if report["all_agree"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
