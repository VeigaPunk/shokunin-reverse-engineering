#!/usr/bin/env python3
"""Round-84 prefreeze claim-metadata gate: a claim names its counter, the container pins it.

The maintained post-hoc audit (`tools/round-29/freeze-gate.py`) reports a freeze whose claim
strings name no script as FLAGGED/INSTRUMENT_NONE but exits 0 when that finding is disclosed:
round 83's first container `af20aff3` pinned `tools/round-83/attribution-audit.py` at the top
level while its predicate sentence named only the condition. The round-83 outside review
routed "retain explicit full counter-path claim metadata before the next freeze" to this lane.
This gate is the prefreeze refusal, run before the declaration commit.

Per container (a `.ufo/waves/round-N/claims*.json` blob at --rev), for every entry of its
`claims` array:

  CLAIM_NO_COUNTER_PATH:<claim-id>   no lane-relative script path (tools/|corpus/|.ufo/ +
                                     .py/.sh/.mjs/.js) inside the claim object's strings
  COUNTER_BLOB_ABSENT:<path>         the claim names a path that is not a blob at --rev
  COUNTER_PATH_NOT_PINNED:<path>     the container does not pin the named path
  COUNTER_PIN_MISMATCH:<path>        the pinned digest != the blob digest at --rev

Verdict CLEAN when a container has no findings, FLAGGED otherwise.

Exit: 0 when every container's verdict equals its --expect (without --expect: every container
CLEAN); 1 when a verdict mismatches or a container is FLAGGED without an expectation; 2 when a
container cannot be read or parsed.

--control instruments-only scores the cheap rule that skips the claimed work (a container with a
non-empty `instruments` map is accepted); it must accept the round-83 container, which proves
the target is failable rather than satisfied by the container's shape.
--selftest proves every finding reachable and the cheap rule insufficient, on fixtures only.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "kaidoku-r84-freeze-precheck-v1"
SCRIPT_RE = re.compile(
    r"(?<![\w./-])((?:tools|corpus|\.ufo)/[A-Za-z0-9_./-]+\.(?:py|sh|mjs|js))")
PIN_KEYS = ("instruments", "loaded_by_counter", "producers_not_counters")


def git_blob(root: str, rev: str, path: str) -> bytes | None:
    done = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    if done.returncode != 0:
        return None
    return done.stdout


def strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [s for item in value for s in strings(item)]
    if isinstance(value, dict):
        return [s for item in value.values() for s in strings(item)]
    return []


def pins(container: dict) -> dict:
    observed: dict[str, str] = {}
    for key in PIN_KEYS:
        block = container.get(key)
        if isinstance(block, dict):
            for path, digest in block.items():
                if isinstance(path, str) and isinstance(digest, str):
                    observed[path] = digest
    return observed


def check_container(text: str, rev: str, blob) -> dict:
    """Score one container. `blob(path) -> bytes|None` reads the container's revision."""
    findings: list[str] = []
    try:
        container = json.loads(text)
    except json.JSONDecodeError as error:
        return {"verdict": "FLAGGED", "findings": [f"CONTAINER_UNPARSABLE:{error}"],
                "claims": 0, "rev": rev}
    claims = container.get("claims")
    if not isinstance(claims, list) or not claims:
        findings.append("CONTAINER_NO_CLAIMS")
        claims = []
    pinned = pins(container)
    for claim in claims:
        cid = claim.get("id") if isinstance(claim, dict) else None
        label = cid if isinstance(cid, str) and cid else "<unnamed-claim>"
        named = sorted(set(SCRIPT_RE.findall("\n".join(strings(claim)))))
        if not named:
            findings.append(f"CLAIM_NO_COUNTER_PATH:{label}")
            continue
        for path in named:
            body = blob(path)
            if body is None:
                findings.append(f"COUNTER_BLOB_ABSENT:{path}")
                continue
            if path not in pinned:
                findings.append(f"COUNTER_PATH_NOT_PINNED:{path}")
                continue
            import hashlib
            if pinned[path] != hashlib.sha256(body).hexdigest():
                findings.append(f"COUNTER_PIN_MISMATCH:{path}")
    return {"verdict": "CLEAN" if not findings else "FLAGGED",
            "findings": findings, "claims": len(claims), "rev": rev}


def cheap_rule(text: str) -> dict:
    """The control: skip the per-claim work, accept on a non-empty `instruments` map."""
    try:
        container = json.loads(text)
    except json.JSONDecodeError:
        return {"accepted": False, "rule": "instruments-only"}
    accepted = isinstance(container.get("instruments"), dict) and bool(container["instruments"])
    return {"accepted": accepted, "rule": "instruments-only"}


# --------------------------------------------------------------------------
# selftest: fixtures only; no lane write, no live container
# --------------------------------------------------------------------------

def fixture_container(claim_text: str, instruments: dict, claim_id: str = "R84-C1") -> str:
    return json.dumps({"schema": "fixture", "round": 84, "instruments": instruments,
                       "claims": [{"id": claim_id, "axis": "calibration",
                                   "predicate": claim_text}]}, sort_keys=True)


def selftest(json_out: str | None) -> int:
    import hashlib
    body = b"#!/usr/bin/env python3\nprint('counter')\n"
    digest = hashlib.sha256(body).hexdigest()
    path = "tools/round-84/counter.py"
    blobs = {path: body}
    cases: dict[str, bool] = {}

    def score(text: str) -> dict:
        return check_container(text, "fixture", lambda p: blobs.get(p))

    def check(name: str, cond: bool) -> None:
        cases[name] = bool(cond)

    clean = score(fixture_container(f"Counter {path} scores it.", {path: digest}))
    check("clean-accepted", clean["verdict"] == "CLEAN")

    no_path = fixture_container("attribution mismatches 0 across eight cases",
                                {path: digest})
    check("no-path-refused",
          score(no_path)["findings"] == ["CLAIM_NO_COUNTER_PATH:R84-C1"])

    bare = fixture_container("attribution-audit.py scores it", {path: digest})
    check("bare-name-refused", "CLAIM_NO_COUNTER_PATH:R84-C1" in score(bare)["findings"])

    unpinned = fixture_container(f"Counter {path} scores it.", {})
    check("unpinned-refused",
          score(unpinned)["findings"] == [f"COUNTER_PATH_NOT_PINNED:{path}"])

    wrong = fixture_container(f"Counter {path} scores it.", {path: "0" * 64})
    check("pin-mismatch-refused",
          score(wrong)["findings"] == [f"COUNTER_PIN_MISMATCH:{path}"])

    absent = fixture_container("Counter tools/round-84/missing.py scores it.", {})
    check("absent-blob-refused",
          score(absent)["findings"] == ["COUNTER_BLOB_ABSENT:tools/round-84/missing.py"])

    two = json.dumps({"instruments": {path: digest}, "claims": [
        {"id": "R84-C1", "predicate": f"Counter {path} scores it."},
        {"id": "R84-C2", "predicate": "mutants 0"}]})
    two_findings = score(two)["findings"]
    check("second-claim-named",
          two_findings == ["CLAIM_NO_COUNTER_PATH:R84-C2"])

    empty = json.dumps({"claims": []})
    check("no-claims-refused", "CONTAINER_NO_CLAIMS" in score(empty)["findings"])

    control = cheap_rule(no_path)
    check("cheap-rule-accepts-defective", control["accepted"] is True)
    check("cheap-rule-rejects-empty", cheap_rule(json.dumps({"instruments": {}}))["accepted"] is False)

    failures = sorted(name for name, ok in cases.items() if not ok)
    summary = {"schema": SCHEMA + "-selftest", "cases": len(cases),
               "case_names": sorted(cases), "failures": failures,
               "control": control}
    text = json.dumps(summary, indent=1, sort_keys=True)
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(text + "\n")
    print(text)
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", required=False)
    ap.add_argument("--container", action="append", default=[])
    ap.add_argument("--expect", action="append", default=[],
                    help="<container>=<CLEAN|FLAGGED>; repeatable")
    ap.add_argument("--control", choices=["instruments-only"])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.json_out)
    if not args.rev or not args.container:
        ap.error("--rev and at least one --container are required")

    expectations = {}
    for item in args.expect:
        if "=" not in item:
            ap.error("--expect wants <container>=<CLEAN|FLAGGED>")
        path, verdict = item.rsplit("=", 1)
        if verdict not in ("CLEAN", "FLAGGED"):
            ap.error("--expect verdict must be CLEAN or FLAGGED")
        expectations[path] = verdict

    receipt: dict = {"schema": SCHEMA, "rev": args.rev, "containers": [],
                     "control": None, "mismatches": [], "met": False}
    code = 0
    for path in args.container:
        body = git_blob(args.root, args.rev, path)
        if body is None:
            receipt["containers"].append({"container": path, "verdict": "UNREADABLE",
                                          "findings": ["CONTAINER_BLOB_ABSENT"]})
            receipt["mismatches"].append(f"{path}:unreadable")
            code = 2
            continue
        text = body.decode("utf-8", "replace")
        result = check_container(text, args.rev,
                                 lambda p: git_blob(args.root, args.rev, p))
        entry = {"container": path, **result}
        if path in expectations:
            entry["expect"] = expectations[path]
            if result["verdict"] != expectations[path]:
                receipt["mismatches"].append(f"{path}:{result['verdict']}")
        elif result["verdict"] != "CLEAN":
            receipt["mismatches"].append(f"{path}:{result['verdict']}")
        receipt["containers"].append(entry)
        if args.control:
            receipt["control"] = cheap_rule(text)
    refused = sum(1 for c in receipt["containers"]
                  if c["verdict"] == "FLAGGED" and c.get("expect") == "FLAGGED")
    accepted = sum(1 for c in receipt["containers"]
                   if c["verdict"] == "CLEAN" and c.get("expect", "CLEAN") == "CLEAN")
    receipt["refused_expected"] = refused
    receipt["accepted_expected"] = accepted
    receipt["met"] = (not receipt["mismatches"] and code == 0 and refused >= 1
                      and accepted >= 1
                      and (receipt["control"] is None or receipt["control"]["accepted"]))
    if not receipt["met"] and code == 0:
        code = 1
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(text + "\n")
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
