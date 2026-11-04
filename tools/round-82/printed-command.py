#!/usr/bin/env python3
"""R82-C2: the round's printed counting commands execute as printed.

The frozen round-76 helper (tools/round-76/plan-command.py) hardcodes
SAFE_SCRIPT_PREFIX = "tools/round-76/", so every later round's printed
counting command is refused -- the routed dead end (round-81 outside defect
4). This instrument re-implements the printed-command contract with the
script allowlist taken from the round claims container's pinned `instruments`
keys: a block's script must be a pinned full path (SCRIPT_NOT_PINNED
otherwise) and its bytes at the revision must hash to the pin at run time
(SCRIPT_PIN_MISMATCH otherwise). Static grammar, four-key child environment
and work-root containment are carried over unchanged from round 76.

A record-layer instrument for the lane's own evidence; no domain coverage is
granted or claimed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile

PLAN = "plans/round-82-claims.md"
CLAIMS = ".ufo/waves/round-82/claims.json"
R76 = "tools/round-76/plan-command.py"
R76_REFUSAL = "script outside tools/round-76/"
ENTRY = "corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md"
SOURCES = "corpus/SOURCES.md"
SOURCED_ROW = "S299"
BASE = "9cc8fbbc893d4f76ced1ac8cf66a6239cde91770"
FIXTURES = ".ufo/waves/round-82/pre/fixtures"
ALLOWED_VARS = {"REV", "WORK", "OUT", "ROOT"}
ENV_KEYS = ("PATH", "HOME", "TMPDIR", "LANG")
METACHARS = (";", "|", "&", "$(", "`", ">", "<")
BLOCK_RE = re.compile(
    r"<!--\s*counting-command:\s*(?P<name>[A-Za-z0-9_-]+)\s*-->(?P<body>.*?)"
    r"<!--\s*/counting-command\s*-->", re.S)
FENCE_RE = re.compile(r"```(?:sh|bash)\n(?P<cmd>.*?)```", re.S)
ELLIPSIS = ("\u2026", "...")
UNBOUND_RE = re.compile(r"<[^>\n]{1,120}>")
VAR_RE = re.compile(r"\$(?:\{([A-Z_]+)\}|([A-Z_]+))")
ROW_RE = re.compile(r"^\|\s*(?P<id>S[0-9]{3,})\s*\|", re.M)
SCHEMA = "kaidoku-r82-printed-command-v1"


class Refused(Exception):
    """The block is unsafe, unpinned or escapes its work root."""


class Unevaluable(Exception):
    """Nothing to score."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get(root: str, rev: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", root, "show", f"{rev}:{path}"])


# --------------------------------------------------------------------------
# static grammar (round-76 semantics, unchanged)
# --------------------------------------------------------------------------

def read_text(root: str, rev: str, path: str) -> str:
    return get(root, rev, path).decode("utf-8")


def extract_block(text: str, name: str) -> str:
    for match in BLOCK_RE.finditer(text):
        if match.group("name") != name:
            continue
        fence = FENCE_RE.search(match.group("body"))
        if not fence:
            raise Unevaluable(f"block {name} carries no sh fence")
        return fence.group("cmd").strip()
    raise Unevaluable(f"block {name} absent")


def static_defects(command: str) -> list[str]:
    defects = []
    hit = UNBOUND_RE.search(command)
    if hit:
        defects.append("PLACEHOLDER_UNBOUND: " + hit.group(0))
    for ell in ELLIPSIS:
        if ell in command:
            defects.append(f"PLACEHOLDER_UNBOUND: abbreviation {ell!r}")
    for var in VAR_RE.finditer(command):
        name = var.group(1) or var.group(2)
        if name not in ALLOWED_VARS:
            defects.append(f"VARIABLE_UNBOUND: ${name}")
    for token in METACHARS:
        if token in command:
            defects.append(f"SHELL_METACHAR: {token}")
    return defects


# --------------------------------------------------------------------------
# pinned allowlist
# --------------------------------------------------------------------------

def claim_pins(root: str, rev: str) -> dict:
    container = json.loads(read_text(root, rev, CLAIMS))
    pins = container.get("instruments")
    if not isinstance(pins, dict) or not pins:
        raise Unevaluable(f"claims container has no instruments map: {CLAIMS}")
    return {k: v for k, v in pins.items()
            if isinstance(k, str) and isinstance(v, str)}


def build_argv(command: str, rev: str, work: str, out: str, root: str,
               pins: dict) -> list[str]:
    joined = command.replace("\\\n", " ")
    argv = shlex.split(joined)
    argv = [tok.replace("$REV", rev).replace("${REV}", rev)
            .replace("$WORK", work).replace("${WORK}", work)
            .replace("$OUT", out).replace("${OUT}", out)
            .replace("$ROOT", root).replace("${ROOT}", root)
            for tok in argv]
    if len(argv) < 4:
        raise Refused(f"argv too short: {argv}")
    if argv[0:3] != ["python3", "-I", "-B"]:
        raise Refused(f"argv is not `python3 -I -B <script>`: {argv[0:3]}")
    script = argv[3]
    if ".." in script:
        raise Refused(f"script escapes the lane tree: {script}")
    if script not in pins:
        raise Refused(f"SCRIPT_NOT_PINNED: {script} is not a claims instrument")
    return argv


def pin_matches(root: str, rev: str, script: str, digest: str) -> None:
    data = get(root, rev, script)
    if sha256_bytes(data) != digest:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} bytes differ from the pin")
    path = Path(root) / script
    if path.resolve() != Path(os.path.abspath(path)):
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} resolves through a symlink")
    try:
        actual = path.read_bytes()
    except OSError as exc:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} unreadable: {exc}") from exc
    if sha256_bytes(actual) != digest:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} executed path differs from the pin")


def containment(path: str, work_root: str) -> str:
    real = os.path.realpath(path)
    base = os.path.realpath(work_root)
    if os.path.commonpath([real, base]) != base:
        raise Refused(f"path escapes the work root: {path}")
    return real


def child_env(work: str) -> dict:
    home = os.path.join(work, "home")
    tmp = os.path.join(work, "tmp")
    os.makedirs(home, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": home, "TMPDIR": tmp, "LANG": "C.UTF-8"}


# --------------------------------------------------------------------------
# execution
# --------------------------------------------------------------------------

def run_block(root: str, rev: str, command: str, work: str, out: str,
              counter_field: str, pins: dict,
              expect_counter: str | None = None) -> dict:
    result = {"command": command, "static_defects": static_defects(command),
              "executed": False, "rc": None, "stdout_tail": "",
              "stderr_tail": "", "counter": None, "defects": []}
    if result["static_defects"]:
        result["defects"] = list(result["static_defects"])
        return result
    try:
        argv = build_argv(command, rev, work, out, root, pins)
        script = argv[3]
        pin_matches(root, rev, script, pins[script])
        out_real = containment(out, work)
        work_real = containment(work, work)
        for index, token in enumerate(argv):
            if token.startswith("--json-out="):
                actual_out = token.split("=", 1)[1]
            elif token == "--json-out" and index + 1 < len(argv):
                actual_out = argv[index + 1]
            else:
                continue
            if containment(actual_out, work) != out_real:
                raise Refused("OUTPUT_ARG_MISMATCH: printed output is not the contained receipt")
        if Path(out_real).exists():
            raise Refused("OUTPUT_ALREADY_EXISTS: refusing a stale receipt")
    except Refused as exc:
        result["defects"].append(f"REFUSED: {exc}")
        return result
    env = child_env(work_real)
    try:
        proc = subprocess.run(argv, cwd=root, env=env, capture_output=True,
                              text=True, timeout=300)
    except subprocess.SubprocessError as exc:
        result["defects"].append(f"EXECUTION_ERROR: {exc}")
        return result
    result.update({"argv": argv, "executed": True, "rc": proc.returncode,
                   "stdout_tail": proc.stdout[-2000:],
                   "stderr_tail": proc.stderr[-2000:]})
    if proc.returncode != 0 and not (expect_counter is None
                                     and proc.returncode == 1):
        lines = (proc.stderr + proc.stdout).strip().splitlines()
        result["defects"].append(
            f"EXECUTION_FAILED: rc {proc.returncode}: "
            f"{lines[-1] if lines else ''}")
        return result
    try:
        receipt = json.loads(Path(out_real).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result["defects"].append(f"RECEIPT_UNREADABLE: {exc}")
        return result
    value = receipt
    for part in counter_field.split("."):
        value = value.get(part) if isinstance(value, dict) else None
    result["counter"] = {"field": counter_field, "value": value,
                         "expected": expect_counter,
                         "matched": (None if expect_counter is None
                                     else str(value) == expect_counter)}
    if expect_counter is None:
        # Executability arm: integer counter only; the VALUE is the other
        # claim's business, so the claims stay causally separable.
        if not isinstance(value, int):
            result["defects"].append(
                f"COUNTER_NOT_INTEGER: {counter_field} {value!r}")
    elif str(value) != expect_counter:
        result["defects"].append(
            f"COUNTER_MISMATCH: {counter_field} {value!r} != {expect_counter!r}")
    return result


# --------------------------------------------------------------------------
# sourced arm: the round's new source row binds this claim
# --------------------------------------------------------------------------

def sources_row(text: str, sid: str) -> str | None:
    for line in text.splitlines():
        if ROW_RE.match(line) and ROW_RE.match(line).group("id") == sid:
            return line
    return None


def entry_cites(text: str, sid: str) -> bool:
    for line in text.splitlines():
        if line.startswith("source:"):
            return sid in re.findall(r"\bS[0-9]+\b", line)
    return False


def sourced_arm(root: str, rev: str) -> dict:
    row = sources_row(read_text(root, rev, SOURCES), SOURCED_ROW)
    cells = [c.strip() for c in row.split("|")] if row else []
    row_ok = bool(len(cells) == 13 and cells[8] == "mined"
                  and cells[9] == "2026-11-04")
    base_text = read_text(root, BASE, SOURCES)
    base_absent = sources_row(base_text, SOURCED_ROW) is None
    plan_names = SOURCED_ROW in re.findall(r"\bS[0-9]+\b", read_text(root, rev, PLAN))
    try:
        entry_text = read_text(root, rev, ENTRY)
        entry_ok = entry_cites(entry_text, SOURCED_ROW)
    except subprocess.CalledProcessError:
        entry_ok = False
    defects = []
    if not row_ok:
        defects.append("SOURCED_ROW_UNMET")
    if not base_absent:
        defects.append("SOURCED_ROW_AT_BASE")
    if not plan_names:
        defects.append("SOURCED_ROW_NOT_IN_PLAN")
    if not entry_ok:
        defects.append("SOURCED_ENTRY_UNCITED")
    return {"arm": "sourced", "row_present": bool(row),
            "row_mined": row_ok, "base_absent": base_absent,
            "plan_names_row": plan_names, "entry_cites_row": entry_ok,
            "defects": defects, "met": not defects}


# --------------------------------------------------------------------------
# battery
# --------------------------------------------------------------------------

def battery(root: str, rev: str, work: str, json_out: str | None) -> int:
    os.makedirs(work, exist_ok=True)
    pins = claim_pins(root, rev)
    plan_text = read_text(root, rev, PLAN)
    out = os.path.join(work, "receipts")
    os.makedirs(out, exist_ok=True)

    def fixture(name: str) -> str:
        return extract_block(read_text(root, rev, f"{FIXTURES}/{name}"), "C1")

    c1 = run_block(root, rev, extract_block(plan_text, "C1"), work,
                   os.path.join(out, "c1.json"), "refused", pins,
                   expect_counter=None)
    c1_met = bool(c1["executed"] and c1["rc"] in (0, 1) and not c1["defects"])

    selftest_cmd = fixture("selftest-block.md")
    self_row = run_block(root, rev, selftest_cmd, work,
                         os.path.join(out, "selftest.json"), "cases", pins,
                         expect_counter=None)
    self_met = bool(self_row["executed"] and self_row["rc"] == 0
                    and not self_row["defects"])

    static_row = run_block(root, rev, fixture("unbound-placeholder.md"), work,
                           os.path.join(out, "placeholder.json"), "refused",
                           pins, expect_counter=None)
    static_met = bool(static_row["static_defects"]
                      and any(d.startswith("PLACEHOLDER_UNBOUND")
                              for d in static_row["static_defects"])
                      and not static_row["executed"])

    argv_row = run_block(root, rev, fixture("missing-arg.md"), work,
                         os.path.join(out, "missing-arg.json"), "refused",
                         pins, expect_counter=None)
    argv_met = bool(argv_row["executed"] and argv_row["rc"] == 2
                    and any(d.startswith("EXECUTION_FAILED")
                            for d in argv_row["defects"]))

    r76_out = os.path.join(work, "r76-run.json")
    r76_argv = [sys.executable, "-I", "-B", R76, "--root", root, "--rev", rev,
                "--plan", PLAN, "--block", "C1", "--run",
                "--work", os.path.join(work, "r76work"),
                "--json-out", r76_out]
    try:
        proc = subprocess.run(r76_argv, cwd=root, capture_output=True,
                              text=True, timeout=300)
        payload = proc.stdout + proc.stderr
        sentinel = R76_REFUSAL in payload
        try:
            stored = json.loads(Path(r76_out).read_text(encoding="utf-8"))
            sentinel = sentinel or R76_REFUSAL in json.dumps(stored)
        except (OSError, json.JSONDecodeError):
            pass
        r76_met = bool(proc.returncode == 1 and sentinel)
        r76_observed = f"rc {proc.returncode}, sentinel {sentinel}"
    except (OSError, subprocess.SubprocessError) as exc:
        r76_met, r76_observed = False, f"subprocess error: {exc}"
    r76_arm = {"arm": "r76-refusal",
               "expected": f"frozen helper refuses with {R76_REFUSAL!r}",
               "observed": r76_observed, "met": r76_met}

    sourced = sourced_arm(root, rev)

    arms = [
        {"arm": "c1-executed",
         "expected": "executed, rc in {0,1}, integer `refused`",
         "observed": f"rc {c1['rc']}, refused {(c1['counter'] or {}).get('value')!r}"
         if not c1["defects"] else "; ".join(c1["defects"]),
         "met": c1_met, "row": c1},
        {"arm": "selftest-fixture",
         "expected": "the instrument's own --selftest executes at rc 0 as a pinned script",
         "observed": f"rc {self_row['rc']}" if not self_row["defects"]
         else "; ".join(self_row["defects"]),
         "met": self_met, "row": self_row},
        {"arm": "static-refusal",
         "expected": "PLACEHOLDER_UNBOUND, no execution",
         "observed": "; ".join(static_row["defects"]) or "clean",
         "met": static_met, "row": static_row},
        {"arm": "argv-failure",
         "expected": "executed at rc 2, EXECUTION_FAILED",
         "observed": "; ".join(argv_row["defects"]) or "clean",
         "met": argv_met, "row": argv_row},
        r76_arm,
        sourced,
    ]
    ok = all(a["met"] for a in arms)
    receipt = {"schema": SCHEMA, "rev": rev,
               "instrument": {"path": "tools/round-82/printed-command.py",
                              "sha256": sha256_bytes(Path(__file__).read_bytes())},
               "plan": PLAN, "claims": CLAIMS,
               "allowlist": sorted(pins), "arms": arms,
               "arms_ok": sum(1 for a in arms if a["met"]),
               "arms_total": len(arms), "ok": ok}
    check = validate_battery(receipt)
    receipt["validate"] = check
    if check["defects"]:
        receipt["ok"] = False
    code = 0 if receipt["ok"] else 1
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(text + "\n")
    print(json.dumps({k: receipt[k] for k in
                      ("arms_ok", "arms_total", "ok")}, sort_keys=True))
    print(json.dumps({"validate_defects": check["defects"],
                      "unmet": [a["arm"] for a in arms if not a["met"]],
                      "observed": {a["arm"]: a.get("observed")
                                   for a in arms if not a["met"]}},
                     sort_keys=True))
    return code


def validate_battery(receipt: dict) -> dict:
    defects = []
    arms = receipt.get("arms") or []
    names = [a.get("arm") for a in arms]
    if names != ["c1-executed", "selftest-fixture", "static-refusal",
                 "argv-failure", "r76-refusal", "sourced"]:
        defects.append("arm_set")
    ok_count = sum(1 for a in arms if a.get("met"))
    if receipt.get("arms_ok") != ok_count:
        defects.append("arms_ok_mismatch")
    if receipt.get("arms_total") != len(arms):
        defects.append("arms_total_mismatch")
    if receipt.get("ok") != (ok_count == len(arms) and len(arms) == 6):
        defects.append("verdict_not_rederived")
    return {"defects": defects, "checked": True}


# --------------------------------------------------------------------------
# controls and selftest
# --------------------------------------------------------------------------

CONTROLS = {
    "escape-out": "a $OUT outside the work root: REFUSED by containment",
    "shell-meta": "a block carrying a shell metacharacter: SHELL_METACHAR",
    "bare-name": "a block naming the script bare: SCRIPT_NOT_PINNED",
    "unpinned-script": "a block naming an unpinned path: SCRIPT_NOT_PINNED",
}


def control(root: str, rev: str, work: str, name: str) -> dict:
    if name not in CONTROLS:
        raise Unevaluable(f"unknown control {name}")
    os.makedirs(work, exist_ok=True)
    pins = claim_pins(root, rev)
    if name == "escape-out":
        cmd = ("python3 -I -B tools/round-82/conjunction-gate.py --battery "
               "--root . --rev $REV --json-out $OUT")
        row = run_block(root, rev, cmd, work,
                        os.path.join(work, "..", "escape.json"), "refused",
                        pins, expect_counter=None)
        met = not row["executed"] and any(d.startswith("REFUSED")
                                          for d in row["defects"])
    elif name == "shell-meta":
        cmd = ("python3 -I -B tools/round-82/conjunction-gate.py --battery "
               "--root . --rev $REV --json-out $OUT; echo done")
        row = run_block(root, rev, cmd, work,
                        os.path.join(work, "out.json"), "refused",
                        pins, expect_counter=None)
        met = not row["executed"] and any(d.startswith("SHELL_METACHAR")
                                          for d in row["static_defects"])
    elif name == "bare-name":
        cmd = fixture_block(read_text(root, rev, f"{FIXTURES}/bare-name.md"))
        row = run_block(root, rev, cmd, work,
                        os.path.join(work, "out.json"), "refused",
                        pins, expect_counter=None)
        met = not row["executed"] and any("SCRIPT_NOT_PINNED" in d
                                          for d in row["defects"])
    else:
        cmd = fixture_block(read_text(root, rev, f"{FIXTURES}/unpinned-script.md"))
        row = run_block(root, rev, cmd, work,
                        os.path.join(work, "out.json"), "refused",
                        pins, expect_counter=None)
        met = not row["executed"] and any("SCRIPT_NOT_PINNED" in d
                                          for d in row["defects"])
    return {"control": name, "expected": CONTROLS[name], "met": bool(met),
            "ok": bool(met), "row": row, "exit": 0 if met else 1}


def fixture_block(text: str) -> str:
    return extract_block(text, "C1")


def selftest(root: str, rev: str, json_out: str | None = None) -> int:
    cases: dict[str, bool] = {}

    def check(name: str, cond: bool) -> None:
        cases[name] = bool(cond)

    check("placeholder-refused", any(
        d.startswith("PLACEHOLDER_UNBOUND")
        for d in static_defects("python3 -I -B tools/round-82/conjunction-gate.py --rev <measured>")))
    check("ellipsis-refused", any(
        d.startswith("PLACEHOLDER_UNBOUND")
        for d in static_defects("python3 -I -B tools/round-82/conjunction-gate.py --rev $REV\u2026")))
    check("metachar-refused", any(
        d.startswith("SHELL_METACHAR")
        for d in static_defects("python3 -I -B tools/round-82/conjunction-gate.py --rev $REV; echo done")))
    fake_pins = {"tools/round-82/conjunction-gate.py": "0" * 64,
                 "tools/round-82/printed-command.py": "1" * 64}
    try:
        build_argv("python3 -I -B conjunction-gate.py --rev $REV", "r", "/w",
                   "/w/o.json", "/root", fake_pins)
        check("bare-name-refused", False)
    except Refused as exc:
        check("bare-name-refused", "SCRIPT_NOT_PINNED" in str(exc))
    try:
        build_argv("python3 -I -B tools/round-82/other.py --rev $REV", "r",
                   "/w", "/w/o.json", "/root", fake_pins)
        check("unpinned-path-refused", False)
    except Refused as exc:
        check("unpinned-path-refused", "SCRIPT_NOT_PINNED" in str(exc))
    try:
        build_argv("python3 tools/round-82/conjunction-gate.py --rev $REV",
                   "r", "/w", "/w/o.json", "/root", fake_pins)
        check("prefix-refused", False)
    except Refused as exc:
        check("prefix-refused", "python3 -I -B" in str(exc))

    # pin re-check refuses a wrong digest against a scratch fixture repo
    scratch = tempfile.mkdtemp(prefix="printed-command-selftest-")
    try:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
               "HOME": scratch, "LANG": "C.UTF-8", "TMPDIR": scratch}
        subprocess.run(["git", "-C", scratch, "init", "-q"], env=env,
                       capture_output=True, check=True)
        toplevel = subprocess.run(
            ["git", "-C", scratch, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, env=env, check=True).stdout.strip()
        if toplevel != os.path.realpath(scratch):
            raise RuntimeError("fixture root mismatch")
        check("fixture-repo-top", True)
        member = os.path.join(scratch, "member.py")
        Path(member).write_text("print('member')\n")
        subprocess.run(["git", "-C", scratch, "add", "member.py"], env=env,
                       capture_output=True, check=True)
        subprocess.run(["git", "-C", scratch, "-c", "user.name=f",
                        "-c", "user.email=f@f", "commit", "-qm", "member"],
                       env=env, capture_output=True, check=True)
        good = sha256_bytes(Path(member).read_bytes())
        try:
            pin_matches(scratch, "HEAD", "member.py", good)
            check("pin-match-accepts", True)
        except Refused:
            check("pin-match-accepts", False)
        try:
            pin_matches(scratch, "HEAD", "member.py", "d" * 64)
            check("pin-mismatch-refused", False)
        except Refused as exc:
            check("pin-mismatch-refused", "SCRIPT_PIN_MISMATCH" in str(exc))
    finally:
        subprocess.run(["rm", "-rf", "--", scratch])

    # sourced-arm parsers on synthetic bytes
    row_line = ("| S299 | Python shlex module documentation "
                "— https://docs.python.org/3/library/shlex.html | docs | A | "
                "grounds | anchor | teaches | mined | 2026-11-04 | on-release"
                " | — |")
    check("row-parse-mined", bool(sources_row("x\n" + row_line, "S299")))
    check("row-parse-absent", sources_row("| S298 | other | docs | A | t | a "
                                          "| te | mined | 2026-11-01 | 90d | "
                                          "— |", "S299") is None)
    queued = row_line.replace("| mined |", "| queued |")
    row = sources_row(queued, "S299")
    check("row-parse-queued-unmet",
          bool(row) and not ("mined" in row and "2026-11-04" in row))
    check("entry-cites-true",
          entry_cites("source: S299 — https://example.com §x\nverified-at: y",
                      "S299"))
    check("entry-cites-wrong-row",
          not entry_cites("source: S260 — https://docs.python.org §x\n"
                          "verified-at: y", "S299"))
    check("entry-cites-no-source-line",
          not entry_cites("verified-at: y\nbody", "S299"))

    failures = sorted(k for k, v in cases.items() if not v)
    summary = {"selftest": "tools/round-82/printed-command.py",
               "cases": len(cases), "case_names": sorted(cases),
               "failures": failures}
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--plan", default=PLAN)
    ap.add_argument("--block")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--control")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--cli-selftest", action="store_true")
    ap.add_argument("--work")
    ap.add_argument("--out")
    ap.add_argument("--counter-field", default="refused")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    if a.cli_selftest:
        if not a.work:
            ap.error("--cli-selftest requires --work")
        argv = [sys.executable, "-I", "-B", str(Path(__file__).with_name("cli-fixtures.py")),
                "--root", a.root, "--rev", a.rev, "--work", a.work,
                "--which", "printed"]
        if a.json_out:
            argv += ["--json-out", a.json_out]
        return subprocess.run(argv).returncode
    if a.selftest:
        return selftest(a.root, a.rev, a.json_out)
    if a.control:
        if not a.work:
            print("--control requires --work", file=sys.stderr)
            return 2
        row = control(a.root, a.rev, a.work, a.control)
        print(json.dumps(row, indent=1, sort_keys=True))
        return row["exit"]
    if a.block and a.run:
        if not a.work:
            print("--run requires --work", file=sys.stderr)
            return 2
        pins = claim_pins(a.root, a.rev)
        out = a.out or os.path.join(a.work, f"{a.block}.json")
        row = run_block(a.root, a.rev, extract_block(read_text(
            a.root, a.rev, a.plan), a.block), a.work, out,
            a.counter_field, pins, expect_counter=None)
        receipt = {"schema": SCHEMA, "rev": a.rev, "plan": a.plan,
                   "instrument": {"path": "tools/round-82/printed-command.py",
                                  "sha256": sha256_bytes(
                                      Path(__file__).read_bytes())},
                   "block": a.block, "row": row,
                   "ok": not row["defects"] and row["executed"]}
        text = json.dumps(receipt, indent=1, sort_keys=True)
        if a.json_out:
            Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.json_out).write_text(text + "\n")
        print(text)
        return 0 if receipt["ok"] else 1
    if a.battery:
        if not a.work:
            print("--battery requires --work", file=sys.stderr)
            return 2
        return battery(a.root, a.rev, a.work, a.json_out)
    print("usage: --run | --battery | --control | --selftest", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
