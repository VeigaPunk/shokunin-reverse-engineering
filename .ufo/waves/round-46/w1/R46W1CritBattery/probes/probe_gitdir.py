"""(c)/(f) probe: registry.run_battery's fixture driver has no toplevel assertion.

Run it with GIT_DIR/GIT_WORK_TREE pointing at decoy repos INSIDE scratch and report
where the fixture commit lands.  attest.fixture_repo asserts `rev-parse
--show-toplevel == d`; registry.run_battery does not (its inline loop has no such
call), so the same environment is only caught on one side.
"""
import json
import os
import sys

S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(S, "tools", "round-46"))
import registry  # noqa: E402
import attest  # noqa: E402

fx = os.path.join(S, "fx", "F4")
rev = "4263a332614ee6efb37cfb813232c247efc87aed"
scratch = os.path.join(S, "sc-gitdir")
os.makedirs(scratch, exist_ok=True)

rep = {"GIT_DIR": os.environ.get("GIT_DIR"), "GIT_WORK_TREE": os.environ.get("GIT_WORK_TREE"),
       "registry_has_toplevel_assert": "rev-parse" in open(
           os.path.join(S, "tools", "round-46", "registry.py")).read().split(
               "def run_battery")[1].split("def evaluate")[0],
       "attest_has_toplevel_assert": "show-toplevel" in open(
           os.path.join(S, "tools", "round-46", "attest.py")).read()}
try:
    out = registry.run_battery(fx, rev, "r46", scratch)
    rep["registry_run_battery"] = ({k: v for k, v in out.items() if k != "fixtures"}
                                   if "error" in out else
                                   {k: v for k, v in out.items() if k != "fixtures"})
    rep["registry_error"] = out.get("error")
except Exception as exc:  # noqa: BLE001
    rep["registry_exception"] = "%s: %s" % (type(exc).__name__, str(exc)[:200])
rep["decoy_commits"] = __import__("subprocess").run(
    ["git", "-C", os.environ.get("GIT_REPO_FOR_TEST", scratch), "log", "--oneline"],
    capture_output=True, text=True).stdout.strip()[:400]
print(json.dumps(rep, indent=1, sort_keys=True))
