#!/usr/bin/env python3
"""ReviewerC1 — independent re-derivation of R80-C1.

No executor driver is imported. The module under test is loaded by path with
importlib and exercised through its own `bind(pointer, tokens, lines)` and
`battery(root, rev, control)` surface, exactly as the round-80 seat spec names
them. Record fixtures are built as throw-away git repos under --work.

Usage:
  reviewer-strictness.py --fixtures F --control-impl P [--candidate-impl P]
      --work DIR --json-out OUT [--lane-root LANE --base REV]

The receipt keeps token strings, paths, digests, counts and reasons only:
never a pointed line's bytes and never file contents.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

TOKEN_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
RE_PIN = re.compile(r"(Devin|OMP|Kimi)\s+`rea-agents@([0-9][0-9.]*)`\s*\(`([^`]+)`\)")
RE_GHIDRA_PTR = re.compile(r"`([^`]*Ghidra/application\.properties):(\d+)`")
RE_GHIDRA_VALUE = re.compile(r"application\.version=([0-9][0-9.]*)")
RE_BASHRC_PTR = re.compile(r"`([^`]*\.bashrc):(\d+)(?:-(\d+))?`")
RE_POINTER = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")
CLIENT_ID = {"Devin": "devin-pin", "OMP": "omp-pin", "Kimi": "kimi-pin"}


def base_cell_count(text: str) -> int:
    """The five check ids a single-cell record parses to (3 pins + Ghidra + .bashrc)."""
    names = {name for name, _pin, _pointer in RE_PIN.findall(text)}
    count = len(names)
    if RE_GHIDRA_PTR.search(text) and RE_GHIDRA_VALUE.search(text):
        count += 1
    if RE_BASHRC_PTR.search(text):
        count += 1
    return count


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    return sha256_bytes(pathlib.Path(path).read_bytes())


def load_module(path: str, label: str):
    spec = importlib.util.spec_from_file_location(f"reviewer_{label}", path)
    if spec is None or spec.loader is None:
        return None, "no loader"
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except BaseException as exc:  # a non-importable implementation is a finding
        return None, f"{type(exc).__name__}: {exc}"
    return module, None


def maximal_run(line: str, start: int, end: int) -> str:
    a = start
    while a > 0 and line[a - 1] in TOKEN_CHARS:
        a -= 1
    b = end
    while b < len(line) and line[b] in TOKEN_CHARS:
        b += 1
    return line[a:b]


def occurrences(token: str, line: str) -> list[dict]:
    """Every occurrence of token on line, with its two outside neighbours."""
    out: list[dict] = []
    start = 0
    while True:
        i = line.find(token, start)
        if i < 0:
            break
        j = i + len(token)
        left = line[i - 1] if i > 0 else None
        right = line[j] if j < len(line) else None
        delimited = ((left is None or left not in TOKEN_CHARS)
                     and (right is None or right not in TOKEN_CHARS))
        out.append({
            "start": i,
            "delimited": delimited,
            "left": "BOL" if left is None else left,
            "right": "EOL" if right is None else right,
            "longer_token": None if delimited else maximal_run(line, i, j),
        })
        start = i + 1
    return out


def strict_bind(pointer: str, tokens: list[str], lines: list[str] | None) -> dict:
    """The frozen R80-C1 rule: every token, every occurrence, delimited both sides."""
    if not RE_POINTER.match(pointer):
        return {"matched": False, "reason": "pointer carries no line number", "unparsed": True}
    if lines is None:
        return {"matched": False, "reason": "pointed lines are absent", "unparsed": False}
    for token in tokens:
        found: list[dict] = []
        for line in lines:
            found.extend(occurrences(token, line))
        if not found:
            return {"matched": False,
                    "reason": f"token {token!r} occurs in no pointed line",
                    "unparsed": False}
        bad = [o for o in found if not o["delimited"]]
        if bad:
            return {"matched": False,
                    "reason": (f"token {token!r} is not delimited on both sides "
                               f"(longer token {bad[0]['longer_token']!r} at "
                               f"offset {bad[0]['start']})"),
                    "unparsed": False}
    return {"matched": True, "reason": "", "unparsed": False}


def git_env(work: str) -> dict:
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["TMPDIR"] = work
    return env


def make_fixture_repo(work: str, case: dict, template: str) -> str:
    """PROVINCE.md = record_template + append_cell, committed at HEAD."""
    repo = os.path.join(work, case["id"])
    if os.path.isdir(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    env = git_env(work)

    def run(cmd: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    proc = run(["git", "init", "-q", repo])
    if proc.returncode != 0:
        raise RuntimeError(f"git init failed: {proc.stderr.strip()}")
    pathlib.Path(repo, "PROVINCE.md").write_text(
        template + case["append_cell"] + "\n", encoding="utf-8")
    top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise RuntimeError(f"git toplevel {top!r} != fixture repo {repo!r}")
    for cmd in (
        ["git", "-C", repo, "add", "PROVINCE.md"],
        ["git", "-C", repo, "-c", "user.name=ReviewerC1",
         "-c", "user.email=reviewer@example.invalid",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m",
         "r80 strictness fixture"],
    ):
        proc = run(cmd)
        if proc.returncode != 0:
            raise RuntimeError(f"{' '.join(cmd[:3])} failed: {proc.stderr.strip()}")
    return repo


def declared_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, _pin, _pointer in RE_PIN.findall(text):
        counts[name] = counts.get(name, 0) + 1
    return counts


def score_bind(module, case: dict) -> dict:
    try:
        result = module.bind(case["pointer"], list(case["tokens"]), list(case["lines"]))
    except BaseException as exc:
        return {"matched": None, "reason": f"raised {type(exc).__name__}: {exc}",
                "unparsed": None, "raised": True}
    if not isinstance(result, dict):
        return {"matched": None,
                "reason": f"returned {type(result).__name__}, not a dict",
                "unparsed": None, "raised": True}
    return {
        "matched": bool(result.get("matched")),
        "reason": result.get("reason") or "",
        "unparsed": bool(result.get("unparsed")),
        "raised": False,
    }


def score_record(module, repo: str) -> dict:
    try:
        receipt = module.battery(repo, "HEAD", None)
    except BaseException as exc:
        return {"raised": True, "error": f"{type(exc).__name__}: {exc}"}
    if not isinstance(receipt, dict):
        return {"raised": True, "error": f"returned {type(receipt).__name__}, not a dict"}
    checks = receipt.get("checks") or []
    return {
        "raised": False,
        "checks_total": receipt.get("checks_total"),
        "matched": receipt.get("matched"),
        "mismatches": receipt.get("mismatches"),
        "unparsed": receipt.get("unparsed"),
        "ok": receipt.get("ok"),
        "would_pass": receipt.get("would_pass"),
        "duplicates": list(receipt.get("duplicates") or []),
        "has_duplicates_key": "duplicates" in receipt,
        "ids": [c.get("id") for c in checks],
        "entries": [
            {"id": c.get("id"), "pointer": c.get("pointer"),
             "cell": c.get("cell"), "matched": c.get("matched"),
             "reason": c.get("reason") or ""}
            for c in checks
        ],
        "client_entries": [
            {"id": c.get("id"), "pointer": c.get("pointer"),
             "matched": c.get("matched"), "reason": c.get("reason") or ""}
            for c in checks
            if c.get("id") in set(CLIENT_ID.values())
        ],
        "first_nonmatch_reason": next(
            (c.get("reason") for c in checks if not c.get("matched")), ""),
    }


def run_cli_live(impl_path: str, lane_root: str, base: str, work: str, label: str) -> dict:
    out = os.path.join(work, f"live-{label}.json")
    cmd = [sys.executable, "-I", "-B", impl_path, "--root", lane_root,
           "--rev", base, "--json-out", out]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          env=dict(os.environ, TMPDIR=work))
    printed: dict = {}
    if proc.stdout.strip():
        try:
            printed = json.loads(proc.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError:
            printed = {"unparsed_stdout": True}
    receipt: dict = {}
    if os.path.exists(out):
        try:
            receipt = json.loads(pathlib.Path(out).read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            receipt = {}
    validation: dict = {}
    if os.path.exists(out):
        vproc = subprocess.run([sys.executable, "-I", "-B", impl_path,
                                "--validate", out], capture_output=True, text=True,
                               env=dict(os.environ, TMPDIR=work))
        try:
            validation = {"exit": vproc.returncode,
                          "result": json.loads(vproc.stdout.strip() or "{}")}
        except json.JSONDecodeError:
            validation = {"exit": vproc.returncode, "unparsed_stdout": True}
    return {
        "exit": proc.returncode,
        "printed": printed,
        "receipt_summary": {k: receipt.get(k) for k in
                            ("schema", "checks_total", "matched", "mismatches",
                             "unparsed", "duplicates", "ok", "would_pass")},
        "validation": validation,
        "stderr_tail": proc.stderr.strip().splitlines()[-3:],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--control-impl", required=True)
    ap.add_argument("--candidate-impl")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--lane-root", default=".")
    ap.add_argument("--base", default="")
    args = ap.parse_args(argv)

    lane_root = os.path.abspath(args.lane_root)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    fixture_path = os.path.abspath(args.fixtures)
    fixture_text = pathlib.Path(fixture_path).read_text(encoding="utf-8")
    fixtures = json.loads(fixture_text)
    fixture_sha = sha256_bytes(fixture_text.encode("utf-8"))

    lane_rel_fixture = os.path.relpath(fixture_path, lane_root)
    declaration_commit = subprocess.run(
        ["git", "-C", lane_root, "log", "-1", "--format=%H", "--", lane_rel_fixture],
        capture_output=True, text=True).stdout.strip()
    committed_blob = subprocess.run(
        ["git", "-C", lane_root, "show", f"{declaration_commit}:{lane_rel_fixture}"],
        capture_output=True).stdout if declaration_commit else b""
    head = subprocess.run(["git", "-C", lane_root, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()

    control_mod, control_err = load_module(os.path.abspath(args.control_impl), "control")
    candidate_path = os.path.abspath(args.candidate_impl) if args.candidate_impl else None
    candidate_mod = None
    candidate_err = None
    if candidate_path:
        candidate_mod, candidate_err = load_module(candidate_path, "candidate")

    red_cases = fixtures.get("red_cases") or []
    green_cases = fixtures.get("green_cases") or []
    template = fixtures.get("record_template") or ""

    cases_out: list[dict] = []
    for kind, case_list in (("red", red_cases), ("green", green_cases)):
        for case in case_list:
            entry: dict = {
                "id": case["id"],
                "kind": kind,
                "case_kind": case["kind"],
                "why": case.get("why", ""),
            }
            if case["kind"] == "bind":
                expected = strict_bind(case["pointer"], case["tokens"], case["lines"])
                entry["expected"] = expected
                ctrl = score_bind(control_mod, case) if control_mod else {
                    "matched": None, "reason": f"control not loadable: {control_err}",
                    "unparsed": None, "raised": True}
                entry["control_matched"] = ctrl["matched"]
                entry["control_reason"] = ctrl["reason"]
                entry["control_detail"] = ctrl
                if ctrl["matched"] is True:
                    entry["judgement"] = "false-green" if kind == "red" else "bound"
                else:
                    entry["judgement"] = "refused"
                # Attribution: the match must come from the substring, not a bug.
                occs = [o for line in case["lines"] for o in occurrences(case["tokens"][0], line)]
                entry["attribution"] = {
                    "occurrences": len(occs),
                    "occurrence_undelimited": (not all(o["delimited"] for o in occs)) if occs else None,
                    "longer_token": next((o["longer_token"] for o in occs
                                          if not o["delimited"]), None),
                    "unparsed": ctrl.get("unparsed"),
                }
                if candidate_mod:
                    cand = score_bind(candidate_mod, case)
                    entry["candidate_matched"] = cand["matched"]
                    entry["candidate_reason"] = cand["reason"]
                    entry["candidate_detail"] = cand
                    longer = entry["attribution"]["longer_token"]
                    entry["candidate_reason_names_longer_token"] = bool(
                        longer and longer in cand["reason"])
                    if cand["matched"] is True:
                        entry["candidate_judgement"] = "false-green" if kind == "red" else "bound"
                    else:
                        entry["candidate_judgement"] = (
                            "refused" if kind == "red" else "green-refusal")
            else:  # record
                repo = make_fixture_repo(work, case, template)
                counts = declared_counts(template + case["append_cell"] + "\n")
                dup_ids = sorted(CLIENT_ID[n] for n, c in counts.items() if c > 1)
                base_cells = base_cell_count(template)
                expected_checks = base_cells + (sum(counts.values()) - len(counts))
                entry["expected"] = {
                    "pin_declarations": counts,
                    "declared_pins_total": sum(counts.values()),
                    "base_cells": base_cells,
                    "duplicate_ids": dup_ids,
                    "expected_checks_total": expected_checks,
                }
                ctrl = score_record(control_mod, repo) if control_mod else {
                    "raised": True, "error": f"control not loadable: {control_err}"}
                entry["control_detail"] = ctrl
                if not ctrl["raised"]:
                    collapse = (ctrl["checks_total"] == expected_checks - 1
                                and not ctrl["duplicates"])
                    entry["control_matched"] = not bool(ctrl["duplicates"])
                    entry["control_collapsed_to_5"] = bool(
                        ctrl["checks_total"] == 5 and expected_checks == 6)
                    entry["control_reason"] = (
                        f"checks_total={ctrl['checks_total']} "
                        f"(expected {expected_checks} after expansion; "
                        f"pin_declarations={sum(counts.values())}, "
                        f"duplicate_ids={dup_ids}, collapsed={collapse}); "
                        f"duplicates={ctrl['duplicates']}; "
                        f"ok={ctrl['ok']}; matched={ctrl['matched']}")
                else:
                    entry["control_matched"] = None
                    entry["control_collapsed_to_5"] = None
                    entry["control_reason"] = ctrl["error"]
                if entry["control_matched"] is True:
                    entry["judgement"] = "false-green" if kind == "red" else "bound"
                elif entry["control_matched"] is False:
                    entry["judgement"] = "refused"
                else:
                    entry["judgement"] = "error"
                if candidate_mod:
                    cand = score_record(candidate_mod, repo)
                    entry["candidate_detail"] = cand
                    if not cand["raised"]:
                        # The claim's definition: every declared cell counted, the
                        # duplicate id carried in `duplicates`, ok false.
                        detected = (case["cell_id"] in cand["duplicates"]
                                    and cand["checks_total"] == expected_checks
                                    and cand["ok"] is False)
                        entry["candidate_matched"] = not bool(cand["duplicates"])
                        entry["candidate_detects_duplicate"] = bool(detected)
                        dupe_cells = [c for c in cand.get("entries") or []
                                      if c["id"] == case["cell_id"]
                                      or c["id"].startswith(case["cell_id"] + "#")]
                        entry["candidate_duplicate_cells"] = dupe_cells
                        entry["candidate_duplicate_cells_bound"] = sum(
                            1 for c in dupe_cells if c["matched"])
                        entry["candidate_duplicate_cells_expected"] = len(dupe_cells)
                        entry["candidate_reason"] = (
                            f"checks_total={cand['checks_total']}; "
                            f"duplicates={cand['duplicates']}; ok={cand['ok']}; "
                            f"ids={cand['ids']}")
                    else:
                        entry["candidate_matched"] = None
                        entry["candidate_detects_duplicate"] = False
                        entry["candidate_reason"] = cand["error"]
                    if entry["candidate_matched"] is True:
                        entry["candidate_judgement"] = "false-green"
                    else:
                        entry["candidate_judgement"] = (
                            "refused" if kind == "red" else "green-refusal")
            cases_out.append(entry)

    # Template-only record: the control's acceptance baseline. If the duplicate
    # reds report the same checks_total/ok as this baseline, the appended cell is
    # invisible to the control (the fixture's stated false-green).
    record_baseline = None
    if any(c["case_kind"] == "record" for c in cases_out) and control_mod:
        baseline_repo = make_fixture_repo(
            work, {"id": "_baseline-record", "append_cell": ""}, template)
        record_baseline = score_record(control_mod, baseline_repo)

    # ------- summary counters -------
    def counters(prefix: str) -> dict:
        reds = [c for c in cases_out if c["kind"] == "red"]
        greens = [c for c in cases_out if c["kind"] == "green"]
        return {
            "red_cases": len(reds),
            "green_cases": len(greens),
            "false_greens": sum(1 for c in reds if c.get(f"{prefix}_matched") is True),
            "green_refusals": sum(1 for c in greens
                                  if c.get(f"{prefix}_matched") is False),
            "errors": sum(1 for c in cases_out
                          if c.get(f"{prefix}_matched") is None),
        }

    summary = {"control": counters("control")}
    if candidate_mod:
        summary["candidate"] = counters("candidate")
        summary["candidate"]["duplicate_detections"] = sum(
            1 for c in cases_out if c.get("candidate_detects_duplicate") is True)
        summary["candidate"]["red_duplicate_cases"] = sum(
            1 for c in cases_out if c["kind"] == "red" and c["case_kind"] == "record")
        summary["candidate"]["duplicate_cells_bound"] = sum(
            c.get("candidate_duplicate_cells_bound") or 0
            for c in cases_out if c["case_kind"] == "record")
        summary["candidate"]["duplicate_cells_expected"] = sum(
            c.get("candidate_duplicate_cells_expected") or 0
            for c in cases_out if c["case_kind"] == "record")

    # ------- degenerate models -------
    per_case: list[dict] = []
    for entry in cases_out:
        if entry["case_kind"] == "bind":
            bind_all = {"accepted": True}
            refuse_all = {"accepted": False}
            observed_strict = entry["expected"]["matched"]
        else:
            bind_all = {"accepted": True}      # collapses/ignores the duplicate
            refuse_all = {"accepted": False}   # flags a duplicate on every record
            # the correct rule refuses a record that carries a duplicate cell
            observed_strict = not bool(entry["expected"]["duplicate_ids"])
        per_case.append({
            "id": entry["id"],
            "kind": entry["kind"],
            "bind_all": "accepted" if bind_all["accepted"] else "rejected",
            "bind_all_meets_requirement": bool(
                (not bind_all["accepted"]) if entry["kind"] == "red" else bind_all["accepted"]),
            "refuse_all": "accepted" if refuse_all["accepted"] else "rejected",
            "refuse_all_meets_requirement": bool(
                (not refuse_all["accepted"]) if entry["kind"] == "red" else refuse_all["accepted"]),
            "strict_reference": "accepted" if observed_strict else "rejected",
            "strict_reference_meets_requirement": bool(
                (not observed_strict) if entry["kind"] == "red" else observed_strict),
        })

    bind_all_fails = [c["id"] for c in per_case if not c["bind_all_meets_requirement"]]
    refuse_all_fails = [c["id"] for c in per_case if not c["refuse_all_meets_requirement"]]

    # Weak rules that isolate which side of the delimiter test the fixtures exercise.
    def right_digit_only_accepts(case: dict) -> bool:
        """True iff some occurrence is not immediately followed by an ASCII digit."""
        token = case["tokens"][0]
        for line in case["lines"]:
            start = 0
            while True:
                i = line.find(token, start)
                if i < 0:
                    break
                j = i + len(token)
                right = line[j] if j < len(line) else None
                if right is None or not right.isdigit():
                    return True
                start = i + 1
        return False

    def left_delimited_only_accepts(case: dict) -> bool:
        """True iff some occurrence has a non-token character (or BOL) on its left."""
        token = case["tokens"][0]
        for line in case["lines"]:
            start = 0
            while True:
                i = line.find(token, start)
                if i < 0:
                    break
                left = line[i - 1] if i > 0 else None
                if left is None or left not in TOKEN_CHARS:
                    return True
                start = i + 1
        return False

    weak_right: list[dict] = []
    weak_left: list[dict] = []
    for entry in cases_out:
        if entry["case_kind"] != "bind":
            continue  # a delimiter rule has no bearing on a record duplicate
        case = next(c for c in red_cases + green_cases if c["id"] == entry["id"])
        ra = right_digit_only_accepts(case)
        la = left_delimited_only_accepts(case)
        need = (not ra) if entry["kind"] == "red" else ra
        need_left = (not la) if entry["kind"] == "red" else la
        weak_right.append({"id": entry["id"], "kind": entry["kind"],
                           "accepted": ra, "meets_requirement": bool(need)})
        weak_left.append({"id": entry["id"], "kind": entry["kind"],
                          "accepted": la, "meets_requirement": bool(need_left)})

    degenerate = {
        "bind_all": {
            "description": "every bind matches; every record accepted with no duplicate signal",
            "passes_all_six": not bind_all_fails,
            "fails_on": bind_all_fails,
            "verdict": ("REJECTED: fails %d case(s)" % len(bind_all_fails)
                        if bind_all_fails else "PASSES (fixture set too weak)"),
        },
        "refuse_all": {
            "description": "every bind refused; every record flagged duplicate",
            "passes_all_six": not refuse_all_fails,
            "fails_on": refuse_all_fails,
            "verdict": ("REJECTED: fails %d case(s)" % len(refuse_all_fails)
                        if refuse_all_fails else "PASSES (fixture set too weak)"),
        },
        "strict_reference": {
            "description": "ReviewerC1's own both-sides-delimited token rule + duplicate count",
            "passes_all_six": all(c["strict_reference_meets_requirement"] for c in per_case),
            "fails_on": [c["id"] for c in per_case
                         if not c["strict_reference_meets_requirement"]],
        },
        "weak_right_digit_rule": {
            "description": "token accepted iff some occurrence is not followed by an ASCII "
                           "digit; the left neighbour is ignored (weaker than both-sides)",
            "bind_cases_checked": len(weak_right),
            "passes_bind_cases": all(c["meets_requirement"] for c in weak_right),
            "fails_on": [c["id"] for c in weak_right if not c["meets_requirement"]],
            "per_case": weak_right,
        },
        "weak_left_only_rule": {
            "description": "token accepted iff some occurrence has a delimiter or BOL on its "
                           "left; the right neighbour is ignored (weaker than both-sides)",
            "bind_cases_checked": len(weak_left),
            "passes_bind_cases": all(c["meets_requirement"] for c in weak_left),
            "fails_on": [c["id"] for c in weak_left if not c["meets_requirement"]],
            "per_case": weak_left,
        },
        "per_case": per_case,
    }

    # ------- live arm (supplementary) -------
    live = {}
    if args.base:
        live["control"] = run_cli_live(os.path.abspath(args.control_impl),
                                       lane_root, args.base, work, "control")
        if candidate_path:
            live["candidate"] = run_cli_live(candidate_path, lane_root, args.base,
                                             work, "candidate")

    # ------- fixture integrity -------
    ids = [c["id"] for c in red_cases + green_cases]
    integrity = {
        "schema": fixtures.get("schema"),
        "round": fixtures.get("round"),
        "declared_base": fixtures.get("base"),
        "expected_base": args.base,
        "base_field_matches": fixtures.get("base") == args.base if args.base else None,
        "red_case_count": len(red_cases),
        "green_case_count": len(green_cases),
        "counts_are_4_and_2": len(red_cases) == 4 and len(green_cases) == 2,
        "unique_ids": len(ids) == len(set(ids)),
        "kinds": sorted({c["kind"] for c in red_cases + green_cases}),
        "fixture_sha256": fixture_sha,
        "declaration_commit": declaration_commit,
        "head": head,
        "declaration_is_head": declaration_commit == head if declaration_commit else None,
        "committed_blob_matches_worktree": sha256_bytes(committed_blob) == fixture_sha,
    }

    # ------- flat findings -------
    flat: list[str] = []
    ctrl_sum = summary["control"]
    if ctrl_sum["false_greens"] == 4 and ctrl_sum["green_refusals"] == 0:
        flat.append("PASS fixture-control: round-79 control reproduces the before state "
                    "(4/4 reds false-green, 0/2 green refusals)")
    else:
        flat.append(f"FAIL fixture-control: control scores false_greens="
                    f"{ctrl_sum['false_greens']}, green_refusals={ctrl_sum['green_refusals']} "
                    f"(expected 4 and 0)")
    if degenerate["bind_all"]["passes_all_six"]:
        flat.append("FAIL degenerate: a bind-everything implementation would pass the fixture set")
    else:
        flat.append("PASS degenerate: a bind-everything implementation fails "
                    f"{len(degenerate['bind_all']['fails_on'])} case(s) "
                    f"({', '.join(degenerate['bind_all']['fails_on'])})")
    if degenerate["refuse_all"]["passes_all_six"]:
        flat.append("FAIL degenerate: a refuse-everything implementation would pass the fixture set")
    else:
        flat.append("PASS degenerate: a refuse-everything implementation fails "
                    f"{len(degenerate['refuse_all']['fails_on'])} green control(s) "
                    f"({', '.join(degenerate['refuse_all']['fails_on'])})")
    if not degenerate["strict_reference"]["passes_all_six"]:
        flat.append("FAIL strict-reference: the frozen rule itself does not separate the six cases")
    else:
        flat.append("PASS strict-reference: both-sides delimitation + duplicate count separates "
                    "all four reds from both greens")

    for entry in cases_out:
        if entry["case_kind"] == "bind":
            if entry["control_detail"].get("raised"):
                flat.append(f"FAIL {entry['id']}: control raised instead of returning")
            elif entry["kind"] == "red" and not entry["attribution"]["occurrence_undelimited"]:
                flat.append(f"FAIL {entry['id']}: red is not red for a delimitation reason")
            elif entry["kind"] == "green" and entry["control_matched"] is not True:
                flat.append(f"FAIL {entry['id']}: green control not bound by the control")
        else:
            if entry["control_detail"].get("raised"):
                flat.append(f"FAIL {entry['id']}: control battery raised instead of returning")
            elif not entry.get("control_collapsed_to_5"):
                flat.append(f"FAIL {entry['id']}: control did not collapse the duplicate to 5")
    if degenerate["weak_right_digit_rule"]["passes_bind_cases"]:
        flat.append("GAP fixture-sensitivity: a right-digit-only rule (left neighbour "
                    "ignored) passes all four bind cases; no bind red exercises a left-side "
                    "boundary or a non-digit continuation")
    else:
        flat.append("PASS fixture-sensitivity: the right-digit-only weak rule is caught by "
                    f"({', '.join(degenerate['weak_right_digit_rule']['fails_on'])})")
    if degenerate["weak_left_only_rule"]["passes_bind_cases"]:
        flat.append("GAP fixture-sensitivity: a left-only rule also passes all four bind cases")
    else:
        flat.append("PASS fixture-sensitivity: the left-only weak rule is caught by "
                    f"({', '.join(degenerate['weak_left_only_rule']['fails_on'])})")
    flat.append("NOTE fixture-attribution: the two record append cells repeat the existing "
                "cell byte-identically, so the fixtures prove the 5-vs-6 count and the absent "
                "duplicate signal, not first-vs-last survivor identity")
    if record_baseline and not record_baseline.get("raised"):
        dup_rows = [c for c in cases_out if c["case_kind"] == "record"
                    and not c["control_detail"].get("raised")]
        same = [c["id"] for c in dup_rows
                if c["control_detail"]["checks_total"] == record_baseline["checks_total"]
                and c["control_detail"]["matched"] == record_baseline["matched"]
                and c["control_detail"]["ok"] == record_baseline["ok"]]
        if len(same) == len(dup_rows) and dup_rows:
            flat.append(
                "PASS fixture-attribution: the template-only record baseline is "
                f"checks_total={record_baseline['checks_total']}, "
                f"matched={record_baseline['matched']}, ok={record_baseline['ok']}; "
                "every duplicate red reports the same verdict, so the appended duplicate "
                "is invisible to the control")
        else:
            flat.append("FAIL fixture-attribution: a duplicate red differs from the "
                        f"template-only baseline ({same})")
    if candidate_mod:
        cand_sum = summary["candidate"]
        flat.append(f"{'PASS' if cand_sum['false_greens'] == 0 and cand_sum['green_refusals'] == 0 else 'FAIL'} "
                    f"candidate: false_greens={cand_sum['false_greens']}, "
                    f"green_refusals={cand_sum['green_refusals']}, "
                    f"duplicate_detections={cand_sum.get('duplicate_detections')}"
                    f"/{cand_sum.get('red_duplicate_cases')}")
        for c in cases_out:
            if c["case_kind"] != "record":
                continue
            bound = c.get("candidate_duplicate_cells_bound")
            expected = c.get("candidate_duplicate_cells_expected")
            if bound is None:
                continue
            if bound < expected:
                unbound = [e for e in c["candidate_duplicate_cells"]
                           if not e["matched"]]
                detail = "; ".join(
                    f"{e['id']} ({e['reason'].strip()})" for e in unbound)
                flat.append(f"FINDING duplicate-cell binding {c['id']}: "
                            f"{bound}/{expected} cells bound; unbound: {detail}")
            else:
                flat.append(f"PASS duplicate-cell binding {c['id']}: "
                            f"{bound}/{expected} cells bound")
    elif args.candidate_impl:
        flat.append(f"FAIL candidate: not loadable ({candidate_err})")
    else:
        flat.append("NOTE candidate: no ExecBinder candidate was present at scoring time; "
                    "control and fixture attacks scored only")

    receipt = {
        "schema": "kaidoku-r80-c1-reviewer-v1",
        "round": 80,
        "seat": "ReviewerC1",
        "role": "independent re-derivation of R80-C1 (no executor driver imported)",
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "lane_root": lane_root,
        "fixtures_path": fixture_path,
        "impls": {
            "control": {"path": os.path.abspath(args.control_impl),
                        "sha256": sha256_file(os.path.abspath(args.control_impl)),
                        "load_error": control_err},
            "candidate": ({"path": candidate_path,
                           "sha256": sha256_file(candidate_path),
                           "load_error": candidate_err}
                          if candidate_path else None),
        },
        "fixture_integrity": integrity,
        "control_scores": {
            "cases": len(cases_out),
            "red_false_greens": ctrl_sum["false_greens"],
            "green_refusals": ctrl_sum["green_refusals"],
        },
        "cases": cases_out,
        "summary": summary,
        "degenerate_checks": degenerate,
        "record_baseline": record_baseline,
        "live_arm": live,
        "flat_findings": flat,
    }
    text = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
    pathlib.Path(args.json_out).write_text(text, encoding="utf-8")
    print(json.dumps({
        "out": args.json_out,
        "control": receipt["control_scores"],
        "candidate": summary.get("candidate"),
        "degenerate_bind_all": degenerate["bind_all"]["verdict"],
        "degenerate_refuse_all": degenerate["refuse_all"]["verdict"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
