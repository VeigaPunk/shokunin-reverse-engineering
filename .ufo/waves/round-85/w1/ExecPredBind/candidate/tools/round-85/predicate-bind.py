#!/usr/bin/env python3
"""Round-85 predicate-bind gate: a claim's counter is named, unpinned-nowhere, in its predicate.

The round-84 prefreeze gate (`tools/round-84/freeze-precheck.py`) accepts a counter
path anywhere in a claim's strings, so a path that appears only in `kill_rule`, or
only inside a negated sentence, satisfies it. This gate binds the naming to the
claim's `predicate` sentence and to an affirmative reading of it.

Per container (a `.ufo/waves/round-N/claims*.json` blob at --rev), for every entry
of its `claims` array, the claim's `predicate` string must name at least one
lane-relative script path (`tools/|corpus/|.ufo/` + `.py/.sh/.mjs/.js`, the same
SCRIPT_RE as freeze-precheck) that is

  (a) a blob at --rev,
  (b) pinned in the container's `instruments`/`loaded_by_counter`/
      `producers_not_counters` at its blob digest, and
  (c) not negated: the predicate is split into sentences on `.`, `;` and newline
      (path spans are masked first, so a path never straddles a sentence boundary
      and tokens inside a path never count), and a path is negated when a negation
      token appears in the same sentence as that path. Negation tokens, matched
      with word boundaries, case-sensitively lowercase: `not`, `no`, `never`,
      `without`, `neither`, `nor`, `cannot`. `none` is deliberately NOT a token:
      the round-84 predicates read "mismatches none".

Findings:

  PB_NO_PREDICATE_PATH:<claim-id>    the predicate names no script path (a path
                                     in `kill_rule` alone does not satisfy it)
  PB_PREDICATE_NEGATED:<claim-id>    at least one predicate path shares its
                                     sentence with a negation token
  PB_PATH_NOT_BLOB:<path>            an affirmative predicate path is not a blob
                                     at --rev
  PB_PATH_NOT_PINNED:<path>          an affirmative predicate path is not pinned
  PB_PIN_MISMATCH:<path>             an affirmative predicate path's pinned digest
                                     differs from the blob digest at --rev
  CONTAINER_UNPARSABLE:<err>         the container is not valid JSON
  CONTAINER_NO_CLAIMS                the container has no non-empty `claims` array

Decision (declared with the plan): a claim is refused if ANY predicate path is
negated; otherwise one affirmative, pinned, blob-verified path carries the claim —
but every defective affirmative path is reported on its own finding and flags the
verdict, so a good path never offsets a bad one. This matches the claim's kill
rule: any predicate path that is not a blob or not pinned at its digest must be
reported.

Verdict CLEAN when a container has no findings, FLAGGED otherwise.

Exit: 0 when every container's verdict equals its --expect (without --expect: every
container CLEAN); 1 when a verdict mismatches or a container is FLAGGED without an
expectation; 2 when a container cannot be read or parsed.

--control instruments-only scores the cheap rule that skips the per-claim work (a
container with a non-empty `instruments` map is accepted); scored per container, it
must accept the defective fixtures, which proves the target is failable rather than
satisfied by the container's shape.
--selftest proves every finding reachable and the cheap rule insufficient, on
fixtures only.

Limits (declared): this is a naming-and-negation lint, not semantics. A predicate
that names the counter in an affirmative but meaningless sentence still passes, and
the naive sentence split cuts version numbers ("REA 6.5.0") into fragments, so a
negation token after such a dot is read into a different fragment than the path.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "kaidoku-r85-predicate-bind-v1"
SCRIPT_RE = re.compile(
    r"(?<![\w./-])((?:tools|corpus|\.ufo)/[A-Za-z0-9_./-]+\.(?:py|sh|mjs|js))")
SENTENCE_SPLIT_RE = re.compile(r"[.;\n]")
NEGATION_RE = re.compile(r"\b(?:not|no|never|without|neither|nor|cannot)\b")
PLACEHOLDER_RE = re.compile(r"\x00(\d+)\x00")
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


def predicate_sentences(predicate: str) -> tuple[list[str], dict[int, str]]:
    """Split a predicate into sentences with every path span masked.

    Returns (sentences, holders): each path occurrence becomes the placeholder
    `\x00<index>\x00` inside its sentence and holders maps that index to the
    path, so a path never straddles a sentence boundary and a negation token
    inside a path never counts. Dots inside the path are therefore protected;
    dots elsewhere (`.`/`;`/newline) split sentences.
    """
    holders: dict[int, str] = {}
    parts: list[str] = []
    pos = 0
    for index, match in enumerate(SCRIPT_RE.finditer(predicate)):
        parts.append(predicate[pos:match.start()])
        holders[index] = match.group(1)
        parts.append(f"\x00{index}\x00")
        pos = match.end()
    parts.append(predicate[pos:])
    sentences = [s for s in SENTENCE_SPLIT_RE.split("".join(parts)) if s.strip()]
    return sentences, holders


def negated_paths(predicate: str) -> set[str]:
    """Paths sharing a sentence with a negation token (word-boundary, lowercase)."""
    sentences, holders = predicate_sentences(predicate)
    poisoned: set[str] = set()
    for sentence in sentences:
        if not NEGATION_RE.search(sentence):
            continue
        for found in PLACEHOLDER_RE.finditer(sentence):
            poisoned.add(holders[int(found.group(1))])
    return poisoned


def predicate_text(claim) -> str:
    """The claim's predicate as one string; a non-string predicate is stringified."""
    if not isinstance(claim, dict):
        return ""
    raw = claim.get("predicate")
    if isinstance(raw, str):
        return raw
    if raw is None:
        return ""
    return "\n".join(strings(raw))


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
        predicate = predicate_text(claim)
        named = sorted(set(SCRIPT_RE.findall(predicate)))
        if not named:
            findings.append(f"PB_NO_PREDICATE_PATH:{label}")
            continue
        poisoned = negated_paths(predicate)
        if poisoned:
            findings.append(f"PB_PREDICATE_NEGATED:{label}")
        for path in named:
            if path in poisoned:
                continue  # the negation already refuses this claim
            body = blob(path)
            if body is None:
                findings.append(f"PB_PATH_NOT_BLOB:{path}")
                continue
            if path not in pinned:
                findings.append(f"PB_PATH_NOT_PINNED:{path}")
                continue
            if pinned[path] != hashlib.sha256(body).hexdigest():
                findings.append(f"PB_PIN_MISMATCH:{path}")
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

PATH = "tools/round-84/counter.py"
PATH2 = "tools/round-84/helper.py"
BODY = b"#!/usr/bin/env python3\nprint('counter')\n"
BODY2 = b"#!/usr/bin/env python3\nprint('helper')\n"
DIGEST = hashlib.sha256(BODY).hexdigest()
DIGEST2 = hashlib.sha256(BODY2).hexdigest()


def fixture(predicate, pinned: dict, claim_id: str = "R85-C1", extra: dict | None = None) -> str:
    claim: dict = {"id": claim_id, "axis": "calibration", "predicate": predicate}
    if extra:
        claim.update(extra)
    return json.dumps({"schema": "fixture", "round": 85, "instruments": pinned,
                       "claims": [claim]}, sort_keys=True)


def selftest(json_out: str | None) -> int:
    blobs = {PATH: BODY, PATH2: BODY2}
    cases: dict[str, bool] = {}

    def score(text: str) -> dict:
        return check_container(text, "fixture", lambda p: blobs.get(p))

    def check(name: str, cond: bool) -> None:
        cases[name] = bool(cond)
        print(f"{name}: {'ok' if cond else 'FAIL'}")

    clean = score(fixture(f"Counter {PATH} scores it.", {PATH: DIGEST}))
    check("clean-accepted", clean["verdict"] == "CLEAN")

    kill_only = score(fixture("Every verdict mismatch refuses the round.",
                              {PATH: DIGEST},
                              extra={"kill_rule": f"Refuse when {PATH} reports any mismatch."}))
    check("kill-rule-only-path-refused",
          kill_only["findings"] == [f"PB_NO_PREDICATE_PATH:R85-C1"])

    negated_same = score(fixture(f"Counter {PATH} does not score this container.",
                                 {PATH: DIGEST}))
    check("negated-same-sentence-refused",
          negated_same["findings"] == [f"PB_PREDICATE_NEGATED:R85-C1"])

    negated_second = score(fixture(f"{PATH} scores it. {PATH2} does not score it.",
                                   {PATH: DIGEST, PATH2: DIGEST2}))
    check("negated-path-in-second-sentence-refused",
          negated_second["findings"] == [f"PB_PREDICATE_NEGATED:R85-C1"])

    check("negation-second-sentence-path-first-accepted",
          score(fixture(f"Counter {PATH} scores it. This run does not replace the audit.",
                        {PATH: DIGEST}))["verdict"] == "CLEAN")
    check("negation-after-semicolon-accepted",
          score(fixture(f"{PATH} scores it; the audit does not move.",
                        {PATH: DIGEST}))["verdict"] == "CLEAN")
    check("negation-after-newline-accepted",
          score(fixture(f"{PATH} scores it.\nThe runner does not pause.",
                        {PATH: DIGEST}))["verdict"] == "CLEAN")
    check("none-token-is-not-negation",
          score(fixture(f"{PATH} reports mismatches none.", {PATH: DIGEST}))["verdict"] == "CLEAN")
    check("cannot-token-negates",
          score(fixture(f"{PATH} cannot be skipped.", {PATH: DIGEST}))["findings"]
          == [f"PB_PREDICATE_NEGATED:R85-C1"])

    absent = score(fixture("Counter tools/round-84/missing.py scores it.", {}))
    check("not-blob-refused",
          absent["findings"] == ["PB_PATH_NOT_BLOB:tools/round-84/missing.py"])

    check("unpinned-refused",
          score(fixture(f"Counter {PATH} scores it.", {}))["findings"]
          == [f"PB_PATH_NOT_PINNED:{PATH}"])
    check("pin-mismatch-refused",
          score(fixture(f"Counter {PATH} scores it.", {PATH: "0" * 64}))["findings"]
          == [f"PB_PIN_MISMATCH:{PATH}"])
    check("multi-path-one-unpinned-refused",
          score(fixture(f"{PATH} and {PATH2} score it.", {PATH: DIGEST}))["findings"]
          == [f"PB_PATH_NOT_PINNED:{PATH2}"])

    listed = json.dumps({"schema": "fixture", "round": 85, "instruments": {PATH: DIGEST},
                         "claims": [{"id": "R85-C1", "axis": "calibration",
                                     "predicate": [f"Counter {PATH} scores it."]}]},
                        sort_keys=True)
    check("predicate-list-accepted", score(listed)["verdict"] == "CLEAN")

    check("relative-path-guard",
          score(fixture("xtools/round-84/counter.py scores it", {}))["findings"]
          == [f"PB_NO_PREDICATE_PATH:R85-C1"])

    unparsable = score("{not json")
    check("unparsable-refused",
          unparsable["verdict"] == "FLAGGED"
          and unparsable["findings"][0].startswith("CONTAINER_UNPARSABLE:"))

    empty = score(json.dumps({"instruments": {PATH: DIGEST}, "claims": []}))
    check("no-claims-refused",
          empty["verdict"] == "FLAGGED" and "CONTAINER_NO_CLAIMS" in empty["findings"])

    two = json.dumps({"instruments": {PATH: DIGEST}, "claims": [
        {"id": "R85-C1", "predicate": f"Counter {PATH} scores it."},
        {"id": "R85-C2", "predicate": "mismatches 0"}]})
    check("second-claim-named",
          score(two)["findings"] == ["PB_NO_PREDICATE_PATH:R85-C2"])

    defective = fixture(f"Counter {PATH} does not score this container.", {PATH: DIGEST})
    check("cheap-rule-accepts-defective", cheap_rule(defective)["accepted"] is True)
    check("control-per-container", cheap_rule(
        fixture(f"Counter {PATH} scores it.", {PATH: DIGEST}))["accepted"] is True
        and cheap_rule(json.dumps({"claims": []}))["accepted"] is False)
    check("cheap-rule-rejects-empty",
          cheap_rule(json.dumps({"instruments": {}}))["accepted"] is False)

    failures = sorted(name for name, ok in cases.items() if not ok)
    summary = {"schema": SCHEMA + "-selftest", "cases": len(cases),
               "case_names": sorted(cases), "failures": failures,
               "control": {"rule": "instruments-only",
                           "accepts_defective": cheap_rule(defective)["accepted"]}}
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
                     "controls": [], "control": None, "mismatches": [], "met": False}
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
            # the control is scored on every container; the claim's control is the
            # defective container's own acceptance, never a neighbour's
            control = cheap_rule(text)
            control["container"] = path
            control["expected"] = expectations.get(path)
            receipt["controls"].append(control)
            receipt["control"] = control
    refused = sum(1 for c in receipt["containers"]
                  if c["verdict"] == "FLAGGED" and c.get("expect") == "FLAGGED")
    accepted = sum(1 for c in receipt["containers"]
                   if c["verdict"] == "CLEAN" and c.get("expect", "CLEAN") == "CLEAN")
    receipt["refused_expected"] = refused
    receipt["accepted_expected"] = accepted
    receipt["control_fired"] = all(c["accepted"] for c in receipt["controls"]
                                   if c.get("expected") == "FLAGGED") \
        if receipt["controls"] else None
    receipt["met"] = (not receipt["mismatches"] and code == 0 and refused >= 1
                      and accepted >= 1
                      and (receipt["control"] is None
                           or receipt["control_fired"] is True))
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
