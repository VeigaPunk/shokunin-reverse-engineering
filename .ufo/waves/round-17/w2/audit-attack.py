#!/usr/bin/env python3
"""audit-attack.py -- adversarial fixture probe for round-17
tools/invocation-audit.py.

WAVE 2 falsification lane (contract.md bounds: read-only over the lane,
scratch only under tempfile.mkdtemp(), never executes a carrier, never
edits the tool under test).

Part A reruns the real audit at the integrated lane revision so the
per-row classes are captured next to the attack results.

Part B builds one throwaway git repo per case under a mkdtemp root,
plants a fixture SKILL.md plus receipt-shaped JSON under .ufo/, then
runs the tool as a subprocess exactly as the contract specifies
(`python3 -I -B <tool> --root <repo> --rev HEAD`).

Each row carries an `honest` class: what an accurate auditor would
report given what actually ran.  Verdicts:

  FALSE-MATCH       tool says exercised_match, honest class differs
  FALSE-LABEL       tool says labelled_unexercised, honest class differs
  FALSE-VARIANT     tool says unlabelled_variant, honest class differs
  SILENT-OMISSION   a registry row is absent from rows[] entirely
  OK                tool class equals honest class

The honest class encodes the round-17 claim being falsified: a row is
honestly exercised iff the documented command (modulo the documented
placeholder/optional/interpreter rules) was actually run with a
retained argv; honestly labelled only when the row affirmatively marks
the command unexercised.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/invocation-audit.py"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "da64646adcb19c1ede7537b799b8c7d283fe43da"

EM, LU, UV, OMIT = "exercised_match", "labelled_unexercised", "unlabelled_variant", "omitted"

SKILL_HEAD = """# fixture skill

| name | kind | command | notes | pins |
| --- | --- | --- | --- | --- |
"""


def row(name, cell3, cell4="x", cell5="y", trailing="|"):
    return "| {} | tool / kaidoku | {} | {} | {} {}".format(
        name, cell3, cell4, cell5, trailing)


def R(name, cmd, honest, note=""):
    """Registry fixture row: name, 3rd-cell text, honest class, note."""
    return {"name": name, "cmd": cmd, "honest": honest, "note": note,
            "raw_row": None}


def put(root, rel, text):
    dest = os.path.join(root, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)


def build_repo(base, case_name, rows, receipts):
    root = os.path.join(base, case_name)
    os.makedirs(root)
    for args in (["init", "-q"],
                 ["config", "user.email", "attack@fixture.invalid"],
                 ["config", "user.name", "attack"],
                 ["config", "commit.gpgsign", "false"]):
        subprocess.run(["git", "-C", root] + args, check=True,
                       capture_output=True)
    body = SKILL_HEAD + "\n".join(r["raw_row"] for r in rows) + "\n"
    put(root, "SKILL.md", body)
    for path, content in receipts.items():
        if isinstance(content, str):
            put(root, path, content)
        else:
            put(root, path, json.dumps(content))
    subprocess.run(["git", "-C", root, "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", root, "commit", "-q", "-m", case_name],
                   check=True, capture_output=True)
    rev = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                         check=True, capture_output=True,
                         text=True).stdout.strip()
    return root, rev


CASES = [
    # --- label gaming -------------------------------------------------
    ("label-denial", [
        R("denial", "`python3 tools/t1.py --run`; this row documents that "
          "there is no unexercised variant of this command", UV,
          "negated 'unexercised' still trips the substring label check: "
          "a row asserting every variant is exercised is credited as "
          "labelled_unexercised with no argv anywhere"),
    ], {}),
    ("label-stale-vs-exercised", [
        R("stale", "`python3 tools/t1b.py --run`; the shorter form is an "
          "unexercised variant", EM,
          "row text says unexercised yet the command was run"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/t1b.py", "--run"]}]}}),

    # --- interpreter flag normalization -------------------------------
    ("interp-flags", [
        R("i-kept", "`python3 -I tools/iso.py --x`", EM,
          "control: same spelling matches"),
        R("i-dropped", "`python3 tools/iso.py --x`", EM,
          "doc drops -I that the retained argv kept; normalize_tokens "
          "only strips the interpreter token, not its flags"),
        R("ib-combo", "`python3 -I -B tools/iso2.py --y`", EM,
          "doc keeps -I -B; retained argv kept only -B"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [
            {"argv": ["python3", "-I", "tools/iso.py", "--x"]},
            {"argv": ["python3", "-B", "tools/iso2.py", "--y"]},
        ]}}),

    # --- --opt=val spellings ------------------------------------------
    ("opt-eq-doc-vs-space", [
        R("eq-doc", "`python3 tools/opt.py --limit=5`", EM,
          "doc =-form, retained argv split form: same invocation, "
          "two spellings"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/opt.py", "--limit",
                               "5"]}]}}),
    ("opt-space-doc-vs-eq", [
        R("space-doc", "`python3 tools/opt.py --limit 5`", EM,
          "inverse spelling of the same invocation"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/opt.py",
                               "--limit=5"]}]}}),
    ("opt-eq-placeholder", [
        R("eq-ph", "`python3 tools/opt.py --limit=<N>`", EM,
          "whole-token placeholders cannot express --opt=<VAL>; literal "
          "'--limit=<N>' never equals '--limit=5'"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/opt.py",
                               "--limit=5"]}]}}),

    # --- quoted arguments ---------------------------------------------
    ("quoted-args", [
        R("quoted-ok", "`python3 tools/q.py --name \"hello world\"`", EM,
          "control: quotes preserved in doc"),
        R("doc-unquoted", "`python3 tools/q.py --name hello world`", EM,
          "doc dropped the quotes; argv kept one token"),
        R("unclosed-quote", "`python3 tools/q.py --name \"oops --extra`",
          EM, "unclosed quote silently merges '--extra' into the value "
          "token; tokenizer emits no diagnostic"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [
            {"argv": ["python3", "tools/q.py", "--name", "hello world"]},
            {"argv": ["python3", "tools/q.py", "--name", "oops",
                      "--extra"]},
        ]}}),

    # --- command cell position / backtick picking ---------------------
    ("cell-position", [
        R("cmd-in-4th", "see the notes column for the command", EM,
          "backticked command sits in the 4th cell; 3rd cell is prose "
          "-> command parsed as None"),
        R("decoy-first", "`python3 tools/decoy.py`; the exercised form is "
          "`python3 tools/real.py --run`", EM,
          "first backtick wins; the real command in the same cell is "
          "never audited"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [
            {"argv": ["python3", "tools/real.py", "--run"]},
        ]}}),

    # --- argv provenance ----------------------------------------------
    ("orig-argv-recorder", [
        R("writer", "`python3 tools/writer.py`", UV,
          "only the child ran; orig_argv is the receipt producer's own "
          "command line (same shape as runs/*/receipt.json orig_argv)"),
    ], {".ufo/waves/round-99/verification.json": {
        "argv": ["python3", "tools/child.py"],
        "orig_argv": ["python3", "tools/writer.py"]}}),
    ("argv-failed-step", [
        R("dead", "`python3 tools/dead.py --go`", UV,
          "recorded argv whose step exit=2 (never ran) still counts as "
          "exercised; iter_exercised_argvs ignores exit/status"),
    ], {".ufo/waves/round-99/verification.json": {
        "steps": {"dead": {"argv": ["python3", "tools/dead.py", "--go"],
                           "exit": 2, "error": "spawn failed"}}}}),
    ("argv-skipped-plan", [
        R("planned", "`python3 tools/planned.py --later`", UV,
          "argv recorded under a skipped:true plan entry counts as "
          "exercised"),
    ], {".ufo/waves/round-99/verification.json": {
        "planned": [{"argv": ["python3", "tools/planned.py", "--later"],
                     "skipped": True}]}}),

    # --- receipt eligibility glob -------------------------------------
    ("glob-planted", [
        R("never", "`python3 tools/never.py`", UV,
          "basename *receipt*.json admits a non-receipt file anywhere "
          "under .ufo/"),
    ], {".ufo/waves/round-99/w2/attack-notes-receipt.json": {
        "argv": ["python3", "tools/never.py"]}}),
    ("glob-blindspot", [
        R("hidden", "`python3 tools/hidden.py`", EM,
          "real argv inside a receipts/ dir is excluded because the "
          "basename lacks 'receipt' (lane counterpart: "
          ".ufo/rounds/interactive-r1/gate-before.json)"),
    ], {".ufo/receipts/leg-2-binary-session.json": {
        "argv": ["python3", "tools/hidden.py"]}}),

    # --- matcher semantics --------------------------------------------
    ("optional-collapse", [
        R("opt2", "`python3 tools/opt2.py [--deep --verify]`", UV,
          "every bracketed token independently optional: bare argv "
          "credits a command never run as documented"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/opt2.py"]}]}}),
    ("placeholder-eats-flag", [
        R("ph", "`python3 tools/ph.py <FILE>`", UV,
          "<FILE> matches any single token, including a flag; the "
          "positional was never supplied"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/ph.py", "--delete-all"]}]}}),
    ("literal-bracket-arg", [
        R("lb", "`python3 tools/lb.py --filter name[0]`", EM,
          "literal [0] in an argument is parsed as an optional block: "
          "token 'name0' marked optional, real argv token 'name[0]' "
          "never equal"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/lb.py", "--filter",
                               "name[0]"]}]}}),
    ("placeholder-arity", [
        R("mt", "`python3 tools/mt.py <ARGS>`", EM,
          "placeholder is exactly one token; a real multi-token tail "
          "cannot match"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "tools/mt.py", "--a", "1",
                               "--b", "2"]}]}}),
    ("empty-pattern", [
        R("bare-interp", "`python3`", UV,
          "pattern empties after interpreter strip and matches an "
          "interpreter-only normalized argv"),
    ], {".ufo/waves/round-99/verification.json": {
        "orig_argv": ["python3"]}}),

    # --- row-level coverage holes -------------------------------------
    ("row-shape", [
        R("no-trailing-pipe", "`python3 tools/tp.py`", EM,
          "row without trailing '|' splits into <5 cells and is dropped "
          "before classification"),
        R("short-row", "", EM,
          "2-cell row is dropped entirely"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [
            {"argv": ["python3", "tools/tp.py"]},
            {"argv": ["python3", "tools/short.py"]},
        ]}}),
    ("abs-vs-rel", [
        R("absdoc", "`python3 tools/rel.py --z`", EM,
          "control: argv keeps the in-lane absolute path, doc uses "
          "relative; _relpath on both sides converges"),
    ], {".ufo/waves/round-99/verification.json": {
        "commands": [{"argv": ["python3", "{ROOT}/tools/rel.py", "--z"]}]}}),
]


def fix_rows(case_name, rows):
    """Materialize raw_row text for each fixture row."""
    del case_name  # per-case isolation makes the name informational
    out = []
    for r in rows:
        r = dict(r)
        if r["name"] == "cmd-in-4th":
            r["raw_row"] = (
                "| cmd-in-4th | tool / kaidoku | see the notes column "
                "for the command | `python3 tools/real.py --run` | y |")
        elif r["name"] == "short-row":
            r["raw_row"] = "| short-row | tool / kaidoku |"
        elif r["name"] == "no-trailing-pipe":
            r["raw_row"] = ("| no-trailing-pipe | tool / kaidoku | "
                            "`python3 tools/tp.py`")
        else:
            r["raw_row"] = "| {} | tool / kaidoku | {} | x | y |".format(
                r["name"], r["cmd"])
        out.append(r)
    return out


def run_tool(root, rev):
    proc = subprocess.run(
        ["python3", "-I", "-B", TOOL, "--root", root, "--rev", rev],
        capture_output=True, text=True, timeout=120)
    return proc


def classify(row_result, honest):
    got = row_result["class"] if row_result else OMIT
    if got == honest:
        return "OK", got
    if got == OMIT:
        return "SILENT-OMISSION", got
    if got == EM:
        return "FALSE-MATCH", got
    if got == LU:
        return "FALSE-LABEL", got
    return "FALSE-VARIANT", got


def main():
    report = {"tool": TOOL, "lane_rev": REV, "lane_rows": None,
              "cases": []}

    lane = run_tool(LANE, REV)
    if lane.returncode == 0:
        lane_doc = json.loads(lane.stdout)
        report["lane_rows"] = [
            {"name": r["name"], "class": r["class"],
             "matched_receipt": r.get("matched_receipt"),
             "row_says_unexercised": r.get("row_says_unexercised", False)}
            for r in lane_doc["rows"]]
        report["lane_counts"] = lane_doc["counts"]
    else:
        report["lane_error"] = lane.stdout.strip() or lane.stderr.strip()

    tmp = tempfile.mkdtemp(prefix="audit-attack-")
    try:
        for case_name, rows, receipts in CASES:
            root, rev = build_repo(tmp, case_name, fix_rows(case_name, rows), receipts)
            # rewrite receipts containing {ROOT} then re-commit
            changed = False
            for path, content in list(receipts.items()):
                text = content if isinstance(content, str) else json.dumps(content)
                if "{ROOT}" in text:
                    put(root, path, text.replace("{ROOT}", root))
                    changed = True
            if changed:
                subprocess.run(["git", "-C", root, "add", "-A"],
                               check=True, capture_output=True)
                subprocess.run(["git", "-C", root, "commit", "-q", "-m",
                                "rootfix"], check=True, capture_output=True)
                rev = subprocess.run(["git", "-C", root, "rev-parse",
                                      "HEAD"], check=True,
                                     capture_output=True,
                                     text=True).stdout.strip()
            proc = run_tool(root, rev)
            case_out = {"case": case_name, "exit": proc.returncode,
                        "rows": []}
            if proc.returncode != 0:
                case_out["error"] = (proc.stdout + proc.stderr).strip()[-300:]
            else:
                doc = json.loads(proc.stdout)
                by_name = {r["name"]: r for r in doc["rows"]}
                case_out["counts"] = doc["counts"]
                for r in rows:
                    res = by_name.get(r["name"])
                    verdict, got = classify(res, r["honest"])
                    case_out["rows"].append({
                        "name": r["name"], "honest": r["honest"],
                        "got": got, "verdict": verdict,
                        "tool_class_detail": res,
                        "note": r["note"]})
            report["cases"].append(case_out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for case in report["cases"]:
        for r in case["rows"]:
            print("{verdict:15} {case:22} {name:18} honest={honest:<20} "
                  "got={got:<20} {note}".format(case=case["case"], **r))
        if case["exit"] != 0:
            print("TOOL-EXIT-{}   {}".format(case["exit"], case["case"]))
    findings = [r for c in report["cases"] for r in c["rows"]
                if r["verdict"] != "OK"]
    print("\n=== audit-attack summary ===")
    print(json.dumps({
        "cases": len(report["cases"]),
        "rows": sum(len(c["rows"]) for c in report["cases"]),
        "findings": len(findings),
        "by_verdict": {v: [r["name"] for r in findings
                           if r["verdict"] == v]
                       for v in sorted({r["verdict"] for r in findings})},
    }, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
