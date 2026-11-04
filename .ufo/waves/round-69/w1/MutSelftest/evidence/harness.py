#!/usr/bin/env python3
"""Counter mutation harness for round 69 wave w1 (seat MutSelftest).

Copies only: the frozen counters are read from the lane repo and every mutant
is written under this scratch dir.  Every git operation happens inside a
fixture repo created here; the lane repo is only ever read with `git show`.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r69/MutSelftest"
FIX = os.path.join(S, "fixtures")
MUT = os.path.join(S, "mutants")
LOG = os.path.join(S, "logs")
TS = ["tools/round-69/mutation-check.py", "tools/round-69/contract-probe.py",
      "tools/round-69/controls.py"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def reset(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------- mutations
MUTATIONS = {
    "mutation-check/row-drop": (
        "tools/round-69/mutation-check.py",
        ['        ("M5_control",\n'
         '         \'control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0\',\n'
         '         \'control_ok = True\', "arm-pack-control-false"),\n'],
        [""],
        "drop the whole M5_control row from PATCH_SETS r69"),
    "mutation-check/weak-verdict": (
        "tools/round-69/mutation-check.py",
        ['elif result["failed"] is not None and expect_case and expect_case in result["failed"]:'],
        ['elif expect_case and result["rc"] != 0:'],
        "count any non-zero rc as a kill when a case is declared (failed list not required)"),
    "mutation-check/ok-drops-wrong": (
        "tools/round-69/mutation-check.py",
        ["    ok = len(survivors) == expected and not wrong"],
        ["    ok = len(survivors) == expected"],
        "ok ignores the killed_wrong_case/unevaluable list"),
    "mutation-check/validate-empty": (
        "tools/round-69/mutation-check.py",
        ["    if not isinstance(mutants, list) or not mutants:"],
        ["    if not isinstance(mutants, list):"],
        "receipt validation accepts an empty mutant list"),
    "contract-probe/a3-rc-only": (
        "tools/round-69/contract-probe.py",
        ['    arms.append(arm("A3_packer_version",\n'
         '                    a3["rc"] == 2 and "packer" in str(a3["unevaluable"] or "")\n'
         '                    and "version" in str(a3["unevaluable"] or ""), a3))'],
        ['    arms.append(arm("A3_packer_version", a3["rc"] == 2, a3))'],
        "A3 passes on any exit 2, dropping the packer/version substring check"),
    "contract-probe/a5-skip-format": (
        "tools/round-69/contract-probe.py",
        ['        missing = [k for k in ("name", "format", "packing_mode", "pin", "source", "runs")\n'
         '                   if not c.get(k)]',
         '        if derived_format != c["format"]:',
         '"format": c["format"],'],
        ['        missing = [k for k in ("name", "packing_mode", "pin", "source", "runs")\n'
         '                   if not c.get(k)]',
         '        if c.get("format") is not None and derived_format != c["format"]:',
         '"format": c.get("format"),'],
        "A5 tolerates a carrier with no format record"),
    "contract-probe/a5-drop-carrier-ok": (
        "tools/round-69/contract-probe.py",
        ['        if c.get("ok") is not True or any(v is False for v in (c.get("arms") or {}).values()):\n'
         '            failures.append(f"{cid}: carrier not ok or an arm false")\n'],
        [""],
        "A5 stops requiring the carrier ok flag and its arms"),
    "contract-probe/validate-no-observation": (
        "tools/round-69/contract-probe.py",
        ['        if not isinstance(a.get("observed"), dict) or not a.get("observed"):'],
        ['        if not isinstance(a.get("observed"), dict):'],
        "arm receipts with an empty observation validate"),
    "packed-elf/control-ok-drop": (
        "tools/round-69/packed-elf.py",
        ['    if receipt.get("control_ok") is not True:\n'
         '        failing.append("control_ok not true")\n'],
        [""],
        "check_receipt stops requiring control_ok"),
    "packed-elf/ceiling-075-drop": (
        "tools/round-69/packed-elf.py",
        ['        if not isinstance(ratio, (int, float)) or ratio > 0.75:\n'
         '            failing.append(f"{cid}: before_ceiling_ratio {ratio} > 0.75")\n'],
        ['        if not isinstance(ratio, (int, float)):\n'
         '            failing.append(f"{cid}: before_ceiling_ratio {ratio} absent")\n'],
        "check_receipt stops comparing the ratio against 0.75"),
    "controls/c3-do-nothing-flip": (
        "tools/round-69/controls.py",
        ['        "ok": c3["rc"] == 1,'],
        ['        "ok": c3["rc"] == 0,'],
        "c3-do-nothing is ok exactly when the do-nothing receipt is met"),
    "controls/c3-loose-ceiling-zero": (
        "tools/round-69/controls.py",
        ['                              ("c3-loose-ceiling", True, 1)):'],
        ['                              ("c3-loose-ceiling", True, 0)):'],
        "c3-loose-ceiling demands the loose ceiling be met"),
    "controls/c1-do-nothing-flip": (
        "tools/round-69/controls.py",
        ['        "ok": survivors == 5 and (c1["json"] or {}).get("survivors") != [],'],
        ['        "ok": survivors == 0,'],
        "c1-do-nothing is ok exactly when a battery reports zero survivors"),
}


def build_mutants() -> dict:
    reset(MUT)
    index = {}
    for name, (tool, olds, news, note) in MUTATIONS.items():
        src = open(os.path.join(LANE, tool), "rb").read()
        text = src.decode()
        for old, new in zip(olds, news):
            n = text.count(old)
            assert n == 1, f"{name}: site matched {n} times: {old[:60]!r}"
            text = text.replace(old, new, 1)
        out = os.path.join(MUT, name + ".py")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(text)
        # line of the first changed site, measured against the frozen text
        frozen = src.decode()
        line = 1
        for old, new in zip(olds, news):
            off = frozen.index(old)
            line = frozen[:off].count("\n") + 1
            break
        index[name] = {"tool": tool, "frozen_sha256": sha(src),
                       "mutant_sha256": sha(text.encode()),
                       "first_site_line": line, "note": note,
                       "path": out}
    return index


# ----------------------------------------------------------------- fixtures
def fixture_repo(path: str, files: dict[str, bytes]) -> str:
    """Create a scratch git repo holding `files` and return its commit sha."""
    reset(path)
    for rel, data in files.items():
        dst = os.path.join(path, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(data)
    subprocess.run(["git", "-C", path, "init", "-q"], check=True, capture_output=True)
    top = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(path), f"fixture toplevel {top!r}"
    for argv in (["-c", "user.name=fixture", "-c", "user.email=fixture@local",
                                 "add", "-A"],
                 ["-c", "user.name=fixture", "-c", "user.email=fixture@local",
                  "commit", "-q", "-m", "fixture"]):
        subprocess.run(["git", "-C", path, *argv], check=True, capture_output=True)
    head = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    assert subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() == os.path.realpath(path)
    return head


CRASH = r'''#!/usr/bin/env python3
"""fixture: pristine selftest green; any patched arm crashes without a case."""
import json
import sys


def evaluate(model):
    identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]
    recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]
    detected = model["upx_list_rc"] == 0 and model["section_count"] == 0
    before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]
    control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0
    assert identity_ok == (model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"])
    assert recovery_ok == (bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"])
    assert detected == (model["upx_list_rc"] == 0 and model["section_count"] == 0)
    assert before_ok == (model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"])
    assert control_ok == (model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0)
    return all([identity_ok, recovery_ok, detected, before_ok, control_ok])


def main():
    model = {"upx_list_rc": 0, "section_count": 2, "packed_procedures": 150,
             "before_max_procedures": 10, "unpack_rc": 1, "unpacked_sha256": "bb" * 32,
             "pin": "aa" * 32, "recovered_counts": {"procedure_count": 166},
             "orig_counts": {"procedure_count": 167}, "control_list_rc": 0,
             "control_decompress_rc": 0}
    evaluate(model)
    print(json.dumps({"selftest": "fixture", "cases": 20, "failed": [], "ok": True},
                     indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


FAKE_ROUTE_A3 = r'''#!/usr/bin/env python3
"""fixture route: refuses both bad packers, but reports the version refusal as a work problem."""
import json
import os
import shutil
import sys

args = sys.argv[1:]


def arg(name):
    return args[args.index(name) + 1] if name in args else None


def die(message):
    print(json.dumps({"schema": "fixture-route", "unevaluable": message}))
    sys.exit(2)


work, upx = arg("--work"), arg("--upx")
if shutil.which("node") is None:
    die("node_absent: node is not on PATH")
if work and not os.access(work, os.W_OK):
    die("work_unusable: work root is not writable")
if upx:
    if os.path.basename(upx) == "upx-5.1.0":
        die("work_unusable: work root is not writable")
    die("packer_mismatch: sha256 fixture != pin")
die("no_run: nothing to do")
'''


FAKE_ROUTE_OK = r'''#!/usr/bin/env python3
"""fixture route: a contract-compliant refusal for both bad packers."""
import json
import os
import shutil
import sys

args = sys.argv[1:]


def arg(name):
    return args[args.index(name) + 1] if name in args else None


def die(message):
    print(json.dumps({"schema": "fixture-route", "unevaluable": message}))
    sys.exit(2)


work, upx = arg("--work"), arg("--upx")
if shutil.which("node") is None:
    die("node_absent: node is not on PATH")
if work and not os.access(work, os.W_OK):
    die("work_unusable: work root is not writable")
if upx:
    if os.path.basename(upx) == "upx-5.1.0":
        die("packer_mismatch: version 'upx 5.1.0' != pin 'upx 5.2.0'")
    die("packer_mismatch: sha256 fixture != pin")
die("no_run: nothing to do")
'''


def m5_survivor_bytes() -> bytes:
    src = subprocess.run(["git", "-C", LANE, "show",
                          "HEAD:tools/round-69/packed-elf.py"],
                         capture_output=True, check=True).stdout.decode()
    case = ('    ctl = evaluate_carrier(_model(control_list_rc=0))\n'
            '    cases.append(("arm-pack-control-false",\n'
            '                  ctl["arms"]["control_ok"] is False and ctl["ok"] is False))\n')
    assert src.count(case) == 1
    src = src.replace(case, "", 1)
    entry = '    "arm-pack-control-false",\n'
    assert src.count(entry) == 1
    src = src.replace(entry, "", 1)
    return src.encode()


def build_fixtures() -> dict:
    reset(FIX)
    out = {}
    out["crash"] = fixture_repo(os.path.join(FIX, "crash"),
                                {"tools/fake-elf.py": CRASH.encode()})
    out["route_a3"] = fixture_repo(os.path.join(FIX, "route-a3"),
                                   {"tools/fake-route.py": FAKE_ROUTE_A3.encode()})
    out["route_ok"] = fixture_repo(os.path.join(FIX, "route-ok"),
                                   {"tools/fake-route.py": FAKE_ROUTE_OK.encode()})
    out["m5"] = fixture_repo(os.path.join(FIX, "m5"),
                             {"tools/round-69/packed-elf.py": m5_survivor_bytes()})
    # receipts
    probe = load_module(os.path.join(LANE, "tools/round-69/contract-probe.py"),
                        "probe_for_receipts")
    carriers = []
    for cid, name, kind, source in (
            ("jq", "jq", "executable", "/usr/bin/jq"),
            ("xxd", "xxd", "executable", "/usr/bin/xxd"),
            ("libz", "libz", "shared-object", "/usr/lib/libz.so.1.3.2")):
        fmt = probe.elf_format(source)
        assert fmt is not None, source
        with open(source, "rb") as fh:
            digest = sha(fh.read())
        carriers.append({"id": cid, "name": name, "kind": kind, "source": source,
                         "format": fmt, "packing_mode": "upx --best", "pin": digest,
                         "ok": True,
                         "arms": {"detected": True, "before_ok": True,
                                  "identity_ok": True, "recovery_ok": True,
                                  "control_ok": True},
                         "runs": {"pack": {"argv": ["upx", "--best", source]}}})
    host_sha = sha(open("/usr/bin/upx", "rb").read())
    host_version = subprocess.run(["/usr/bin/upx", "--version"], capture_output=True,
                                  text=True).stdout.strip().splitlines()[0]
    base = {"packer": {"upx": "/usr/bin/upx", "sha256": host_sha,
                       "version": host_version, "sha256_pin": host_sha,
                       "version_pin": host_version, "pin_enforced": True},
            "carriers": carriers}
    os.makedirs(os.path.join(S, "receipts"), exist_ok=True)
    def dump(name, obj):
        path = os.path.join(S, "receipts", name + ".json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=1, sort_keys=True)
        return path
    out["receipt_complete"] = dump("c2-complete", json.loads(json.dumps(base)))
    missing = json.loads(json.dumps(base))
    del missing["carriers"][2]["format"]
    out["receipt_missing_format"] = dump("c2-missing-format", missing)
    notok = json.loads(json.dumps(base))
    notok["carriers"][1]["ok"] = False
    out["receipt_carrier_notok"] = dump("c2-carrier-notok", notok)
    # probe receipt with six arms and no observations
    arms = [{"id": aid, "ok": True, "observed": {}} for aid in
            ("A1_missing_node", "A2_work_unusable", "A3_packer_version",
             "A4_packer_sha256", "A5_carrier_record", "A6_packer_pin")]
    out["probe_no_observation"] = dump(
        "probe-no-observation",
        {"arms": arms, "arms_passed": 6, "failed": [], "ok": True})
    synth_rows = [("jq", "executable", 167, 3, 10),
                  ("xxd", "executable", 99, 3, 10),
                  ("libz", "shared-object", 184, 98, 120)]
    def synth(loose=False, control=True):
        rows = []
        for cid, kind, orig, packed, ceiling in synth_rows:
            ratio = 0.9 if (loose and cid == "libz") else ceiling / orig
            rows.append({"id": cid, "kind": kind, "ok": True,
                         "arms": {"detected": True, "before_ok": True,
                                  "identity_ok": True, "recovery_ok": True,
                                  "control_ok": True},
                         "before_ceiling": ceiling,
                         "before_ceiling_ratio": round(ratio, 4),
                         "orig_counts": {"procedure_count": orig},
                         "packed_counts": {"procedure_count": packed}})
        return {"target": 3, "carriers_matched": 3, "control_ok": control,
                "met_target": True, "failing": [], "carriers": rows}
    out["c3_met"] = dump("c3-met", synth())
    out["c3_loose"] = dump("c3-loose", synth(loose=True))
    out["c3_control_false"] = dump("c3-control-false", synth(control=False))
    out["fake_battery"] = dump(
        "fake-battery",
        {"pristine_ok": True, "mutants": [], "survivors": [], "ok": True,
         "survivor_count": 0})
    # controls stub roots
    stubs = {
        "mutation-5": 'import json, sys\n'
                      'if "--validate" in sys.argv:\n'
                      '    print(json.dumps({"validate": "mutation-receipt", "ok": False,'
                      ' "defects": ["mutants absent or empty"], "mutants": 0}))\n'
                      '    sys.exit(1)\n'
                      'print(json.dumps({"ok": True, "survivor_count": 5, "survivors":'
                      ' ["M1_identity", "M2_recovery", "M3_detected", "M4_before",'
                      ' "M5_control"]}))\n'
                      'sys.exit(0)\n',
        "mutation-0": 'import json, sys\n'
                      'if "--validate" in sys.argv:\n'
                      '    print(json.dumps({"validate": "mutation-receipt", "ok": False,'
                      ' "defects": ["mutants absent or empty"], "mutants": 0}))\n'
                      '    sys.exit(1)\n'
                      'print(json.dumps({"ok": True, "survivor_count": 0, "survivors": []}))\n'
                      'sys.exit(0)\n',
        "probe-0": 'import json, sys\n'
                   'if "--validate" in sys.argv:\n'
                   '    print(json.dumps({"validate": "contract-probe-receipt", "ok": False,'
                   ' "defects": ["arms absent or empty"], "arms": 0}))\n'
                   '    sys.exit(1)\n'
                   'print(json.dumps({"ok": False, "arms_passed": 0, "target": 4,'
                   ' "failed": ["A1_missing_node", "A2_work_unusable", "A3_packer_version",'
                   ' "A4_packer_sha256", "A5_carrier_record", "A6_packer_pin"]}))\n'
                   'sys.exit(1)\n',
        "packed-accept-donothing": 'import json, sys\n'
                                   'if "--check-receipt" in sys.argv:\n'
                                   '    path = sys.argv[sys.argv.index("--check-receipt") + 1]\n'
                                   '    try:\n'
                                   '        r = json.load(open(path))\n'
                                   '    except Exception:\n'
                                   '        r = {}\n'
                                   '    loose = [c.get("id") for c in (r.get("carriers") or [])\n'
                                   '             if isinstance(c.get("before_ceiling_ratio"),'
                                   ' (int, float)) and c["before_ceiling_ratio"] > 0.75]\n'
                                   '    if loose:\n'
                                   '        print(json.dumps({"check": "R69-C3", "met": False,'
                                   ' "failing": [str(i) + ": before_ceiling_ratio > 0.75"'
                                   ' for i in loose]}))\n'
                                   '        sys.exit(1)\n'
                                   '    print(json.dumps({"check": "R69-C3", "met": True,'
                                   ' "failing": []}))\n'
                                   '    sys.exit(0)\n',
        "packed-accept-loose": 'import json, sys\n'
                               'if "--check-receipt" in sys.argv:\n'
                               '    path = sys.argv[sys.argv.index("--check-receipt") + 1]\n'
                               '    r = json.load(open(path))\n'
                               '    kinds = {c.get("kind") for c in (r.get("carriers") or [])}\n'
                               '    if "shared-object" not in kinds:\n'
                               '        print(json.dumps({"check": "R69-C3", "met": False,'
                               ' "failing": ["no shared-object carrier"]}))\n'
                               '        sys.exit(1)\n'
                               '    print(json.dumps({"check": "R69-C3", "met": True,'
                               ' "failing": []}))\n'
                               '    sys.exit(0)\n',
        "packed-correct": 'import json, sys\n'
                          'if "--check-receipt" in sys.argv:\n'
                          '    path = sys.argv[sys.argv.index("--check-receipt") + 1]\n'
                          '    r = json.load(open(path))\n'
                          '    cs = r.get("carriers") or []\n'
                          '    kinds = {c.get("kind") for c in cs}\n'
                          '    loose = [c.get("id") for c in cs\n'
                          '             if isinstance(c.get("before_ceiling_ratio"),'
                          ' (int, float)) and c["before_ceiling_ratio"] > 0.75]\n'
                          '    fail = []\n'
                          '    if "shared-object" not in kinds:\n'
                          '        fail.append("no shared-object carrier")\n'
                          '    fail += [str(i) + ": before_ceiling_ratio > 0.75" for i in loose]\n'
                          '    if fail:\n'
                          '        print(json.dumps({"check": "R69-C3", "met": False,'
                          ' "failing": fail}))\n'
                          '        sys.exit(1)\n'
                          '    print(json.dumps({"check": "R69-C3", "met": True,'
                          ' "failing": []}))\n'
                          '    sys.exit(0)\n',
    }
    roots = {
        "C1": {"mutation": "mutation-5", "probe": "probe-0",
               "packed": "packed-accept-donothing"},
        "C2": {"mutation": "mutation-5", "probe": "probe-0",
               "packed": "packed-accept-loose"},
        "C3": {"mutation": "mutation-0", "probe": "probe-0",
               "packed": "packed-correct"},
    }
    for root, mapping in roots.items():
        rdir = os.path.join(FIX, "root-" + root)
        reset(rdir)
        for key, stub in mapping.items():
            dst = os.path.join(rdir, "tools", "round-69",
                               {"mutation": "mutation-check.py",
                                "probe": "contract-probe.py",
                                "packed": "packed-elf.py"}[key])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(stubs[stub])
        out["root_" + root] = rdir
    return out


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# -------------------------------------------------------------------- runs
def run(argv: list[str], env_extra: dict | None = None) -> dict:
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=1800, env=env)
    payload = None
    for text in (proc.stdout, proc.stderr):
        try:
            payload = json.loads(text)
            break
        except json.JSONDecodeError:
            continue
    return {"argv": argv, "rc": proc.returncode, "json": payload,
            "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-2000:]}


def summarize_counter_payload(payload: dict | None) -> dict:
    if not isinstance(payload, dict):
        return {}
    keys = ("ok", "survivors", "killed", "killed_wrong_case", "mutant_count",
            "pristine_ok", "arms_passed", "failed", "met", "validate", "defects",
            "controls_ok")
    out = {k: payload.get(k) for k in keys if k in payload}
    if isinstance(payload.get("mutants"), list):
        out["mutant_ids"] = [m.get("id") for m in payload["mutants"]]
        out["verdicts"] = {m.get("id"): m.get("verdict") for m in payload["mutants"]}
    if isinstance(payload.get("pristine"), dict):
        out["pristine_cases"] = payload["pristine"].get("cases")
    if isinstance(payload.get("controls"), list):
        out["controls"] = {c.get("id"): c.get("ok") for c in payload["controls"]}
        out["controls_failing"] = [c.get("id") for c in payload["controls"]
                                   if not c.get("ok")]
    return out


def record(test: str, label: str, result: dict) -> dict:
    rec = {"test": test, "label": label, "rc": result["rc"],
           "summary": summarize_counter_payload(result["json"]),
           "stderr_tail": result["stderr"][-600:]}
    os.makedirs(LOG, exist_ok=True)
    with open(os.path.join(LOG, f"{test}--{label}.json"), "w", encoding="utf-8") as fh:
        json.dump(result["json"] if result["json"] is not None else
                  {"rc": result["rc"], "stdout": result["stdout"],
                   "stderr": result["stderr"]}, fh, indent=1, sort_keys=True)
    return rec


def workdir(name: str) -> str:
    path = os.path.join(S, "work", name)
    reset(path)
    return path


def main() -> int:
    reset(LOG)
    index = build_mutants()
    fx = build_fixtures()
    results = {"mutants": index, "tests": []}
    py = sys.executable
    frozen = {t: os.path.join(LANE, t) for t in TS}
    mut = lambda name: os.path.join(MUT, name + ".py")

    def add(test, label, res):
        r = record(test, label, res)
        results["tests"].append(r)
        print(f"[{test}/{label}] rc={r['rc']} {json.dumps(r['summary'])[:300]}")

    # ---------------- M-A1: dropped mutant row
    for label, checker in (("frozen", frozen["tools/round-69/mutation-check.py"]),
                           ("mutant", mut("mutation-check/row-drop"))):
        add("A1-row-drop--m5-survivor", label,
            run([py, "-I", "-B", checker, "--root", os.path.join(FIX, "m5"),
                 "--rev", fx["m5"], "--tool", "tools/round-69/packed-elf.py",
                 "--patch-set", "r69", "--work", workdir("A1-" + label)]))
    for label, checker in (("frozen", frozen["tools/round-69/mutation-check.py"]),
                           ("mutant", mut("mutation-check/row-drop"))):
        add("A1-row-drop--real-instrument", label,
            run([py, "-I", "-B", checker, "--root", LANE, "--rev", "HEAD",
                 "--tool", "tools/round-69/packed-elf.py",
                 "--patch-set", "r69", "--work", workdir("A1r-" + label)]))
    # validate the mutant's 4-row receipt with both validators
    receipt = os.path.join(S, "receipts", "A1-mutant-receipt.json")
    res = run([py, "-I", "-B", mut("mutation-check/row-drop"), "--root", LANE,
               "--rev", "HEAD", "--tool", "tools/round-69/packed-elf.py",
               "--patch-set", "r69", "--work", workdir("A1-receipt"),
               "--json-out", receipt])
    for label, checker in (("frozen-validate", frozen["tools/round-69/mutation-check.py"]),
                           ("mutant-validate", mut("mutation-check/row-drop"))):
        add("A1-validate-4rows", label,
            run([py, "-I", "-B", checker, "--validate", receipt]))

    # ---------------- M-A2 / M-A4: weak verdict, ok drops wrong
    for test, mu in (("A2-weak-verdict", "mutation-check/weak-verdict"),
                     ("A4-ok-drops-wrong", "mutation-check/ok-drops-wrong")):
        for label, checker in (("frozen", frozen["tools/round-69/mutation-check.py"]),
                               ("mutant", mut(mu))):
            add(test + "--crash-fixture", label,
                run([py, "-I", "-B", checker, "--root", os.path.join(FIX, "crash"),
                     "--rev", fx["crash"], "--tool", "tools/fake-elf.py",
                     "--patch-set", "r69", "--work", workdir(test + label)]))

    # the mutants' own receipts, scored by the FROZEN validator
    for test, mu in (("A2-weak-verdict", "mutation-check/weak-verdict"),
                     ("A4-ok-drops-wrong", "mutation-check/ok-drops-wrong")):
        receipt = os.path.join(S, "receipts", test + "-receipt.json")
        run([py, "-I", "-B", mut(mu), "--root", os.path.join(FIX, "crash"),
             "--rev", fx["crash"], "--tool", "tools/fake-elf.py",
             "--patch-set", "r69", "--work", workdir(test + "-receipt"),
             "--json-out", receipt])
        add(test + "-mislabeled-receipt", "frozen-validate",
            run([py, "-I", "-B", frozen["tools/round-69/mutation-check.py"],
                 "--validate", receipt]))

    # ---------------- M-A3: validate accepts empty mutants
    for label, checker in (("frozen", frozen["tools/round-69/mutation-check.py"]),
                           ("mutant", mut("mutation-check/validate-empty"))):
        add("A3-validate-empty", label,
            run([py, "-I", "-B", checker, "--validate", fx["fake_battery"]]))

    # ---------------- M-B1: A3 on any rc 2
    for label, checker in (("frozen", frozen["tools/round-69/contract-probe.py"]),
                           ("mutant", mut("contract-probe/a3-rc-only"))):
        add("B1-a3-rc-only--route-a3", label,
            run([py, "-I", "-B", checker, "--root", os.path.join(FIX, "route-a3"),
                 "--rev", fx["route_a3"], "--tool", "tools/fake-route.py",
                 "--pkg", "/nonexistent-pkg", "--work", workdir("B1-" + label),
                 "--receipt", fx["receipt_complete"]]))
    for label, checker in (("frozen", frozen["tools/round-69/contract-probe.py"]),
                           ("mutant", mut("contract-probe/a5-skip-format")),
                           ("mutant2", mut("contract-probe/a5-drop-carrier-ok"))):
        add("B0-positive-control--route-ok-complete", label,
            run([py, "-I", "-B", checker, "--root", os.path.join(FIX, "route-ok"),
                 "--rev", fx["route_ok"], "--tool", "tools/fake-route.py",
                 "--pkg", "/nonexistent-pkg", "--work", workdir("B0-" + label),
                 "--receipt", fx["receipt_complete"]]))

    # ---------------- M-B2: A5 skips missing format
    for receipt_name in ("receipt_complete", "receipt_missing_format"):
        for label, checker in (("frozen", frozen["tools/round-69/contract-probe.py"]),
                               ("mutant", mut("contract-probe/a5-skip-format"))):
            add("B2-a5-format--" + receipt_name, label,
                run([py, "-I", "-B", checker, "--root", os.path.join(FIX, "route-ok"),
                     "--rev", fx["route_ok"], "--tool", "tools/fake-route.py",
                     "--pkg", "/nonexistent-pkg", "--work",
                     workdir("B2-" + receipt_name + label),
                     "--receipt", fx[receipt_name]]))

    # ---------------- M-B4: A5 drops the carrier ok/arm check
    for label, checker in (("frozen", frozen["tools/round-69/contract-probe.py"]),
                           ("mutant", mut("contract-probe/a5-drop-carrier-ok"))):
        add("B4-a5-carrier-ok--notok-receipt", label,
            run([py, "-I", "-B", checker, "--root", os.path.join(FIX, "route-ok"),
                 "--rev", fx["route_ok"], "--tool", "tools/fake-route.py",
                 "--pkg", "/nonexistent-pkg", "--work", workdir("B4-" + label),
                 "--receipt", fx["receipt_carrier_notok"]]))

    # ---------------- M-B3: validate accepts an empty observation
    for label, checker in (("frozen", frozen["tools/round-69/contract-probe.py"]),
                           ("mutant", mut("contract-probe/validate-no-observation"))):
        add("B3-validate-no-observation", label,
            run([py, "-I", "-B", checker, "--validate", fx["probe_no_observation"]]))

    # ---------------- M-D1/D2: the C3 counter (packed-elf --check-receipt)
    packed = os.path.join(LANE, "tools/round-69/packed-elf.py")
    for test, mu, receipt in (
            ("D1-control-ok-drop", "packed-elf/control-ok-drop", "c3_control_false"),
            ("D2-ceiling-drop", "packed-elf/ceiling-075-drop", "c3_loose")):
        for label, checker in (("frozen", packed), ("mutant", mut(mu))):
            add(test + "--" + receipt, label,
                run([py, "-I", "-B", checker, "--check-receipt", fx[receipt]]))
    for label, checker in (("frozen", packed), ("mutant", mut("packed-elf/ceiling-075-drop")),
                           ("mutant2", mut("packed-elf/control-ok-drop"))):
        add("D0-met-receipt-control", label,
            run([py, "-I", "-B", checker, "--check-receipt", fx["c3_met"]]))

    # ---------------- M-C1 / M-C2 / M-C3: controls expectation flips
    ctl_work = workdir("controls")
    for test, root, mu in (("C1-c3-do-nothing-flip", "root_C1", "controls/c3-do-nothing-flip"),
                           ("C2-loose-ceiling-zero", "root_C2", "controls/c3-loose-ceiling-zero"),
                           ("C3-c1-do-nothing-flip", "root_C3", "controls/c1-do-nothing-flip")):
        for label, checker in (("frozen", frozen["tools/round-69/controls.py"]),
                               ("mutant", mut(mu))):
            add(test + "--stub-root", label,
                run([py, "-I", "-B", checker, "--root", fx[root], "--rev", "HEAD",
                     "--work", ctl_work]))

    with open(os.path.join(S, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print("wrote", os.path.join(S, "results.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
