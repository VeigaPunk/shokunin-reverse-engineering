#!/usr/bin/env python3
"""R46-C1 counter: the freeze-integrity evidence class, scored by a discriminating check.

Frozen target (`plans/round-46-claims.md`, R46-C1).  Two profiles live here:

- `--profile v1` is the round-45 clause set (R45-CL13 a-f), ported so the same
  battery can be scored both ways; `--spec r45` reproduces the round-45 verdict on
  the round-45 artefact (fidelity receipt: `--fidelity`).
- `--profile v2` (default) is the hardened check, and it is the claim: it must
  score the genuine artefact green and every forgery the v1 clause set accepts red.

The artefact is `SKILL.md` `## Queue-drain craft` rule block 23, marker
`<!-- freeze-integrity-table v2 -->`, columns `trigger | v1 hole | v2 arm | exit`,
at least thirteen rows, each naming a routed `R45-CL<n>` id and an arm from the
fixed vocabulary, at least six line-selected citations inside the allowlist that
resolve at `--rev`, and a `sha256:<64 hex>` pin of this file's own bytes.

The battery builds each forgery by mutating THIS file's block 23 in the measured
`SKILL.md`, one defect class per forgery, so the battery can never drift from the
landed artefact.  `met_target` requires `forgeries_total == 9`, `v1_green == 9`
(the v1 clause set is shown to accept every forgery), `v2_green == 0` and
`genuine_green == 1`.

Exit codes: 0 met; 1 not met (each false clause named in `failing`); 2
could-not-evaluate (unknown revision, freeze not an ancestor, claims file or
`## Queue-drain craft ` heading malformed, frozen path changed, no scratch root).
`R45-CL13` (f): a malformed heading is exit 2 with a reason, never a traceback.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate  # noqa: E402  (local module, resolved beside this file)

SELF = "tools/round-46/attest.py"
CLAIMS = "plans/round-46-claims.md"
CRAFT = "## Queue-drain craft "
MALFORMED = "## Queue-drain craft\n"
ARMS = ("commit", "blob", "restored", "dirty", "pathspec", "merge", "marker",
        "header", "rows", "refs", "pin", "battery", "output", "presence")
ROUTED = ["R45-CL2", "R45-CL6", "R45-CL7", "R45-CL9", "R45-CL13", "R45-CL14",
          "R45-CL15", "R45-CL18", "R45-CL19", "R45-CL20", "R45-CL22", "R45-CL23",
          "R45-CL24"]
ALLOW = ("corpus/lessons/", "corpus/knowledge/", "plans/", "tools/round-46/")
# Every path-like citation is seen, so a citation OUTSIDE the validated set is
# rejected rather than silently unmatched (`R45-CL13` (b)).
HARD_REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)"
                      r"(?::(\d+)(?:-(\d+))?)?")
# The round-45 clause set's own citation regex: only these two trees are even seen,
# which is why a `tools/…` or `SKILL.md` citation was invisible to it (R45-CL9 A2).
LOOSE_REF = re.compile(r"((?:corpus/(?:knowledge|lessons)|plans)/[A-Za-z0-9._-]+\.md)"
                       r"(?::(\d+)(?:-(\d+))?)?")
PIN = re.compile(r"sha256:([0-9a-f]{64})")

SPECS = {
    "r46": {
        "marker": "<!-- freeze-integrity-table v2 -->", "block": 23,
        "header": ["trigger", "v1 hole", "v2 arm", "exit"], "min_rows": 13,
        "refs_min": 6, "require_line": True, "allow": ALLOW,
        "must_cite": [("literal", "S142"), ("path", SELF)],
        "must_cite_refs": ["corpus/lessons/round-45.md"],
        "pin": SELF, "routed": True, "vocab": True, "v1_blocks": "ge",
        "v1_min_rows": 8, "claims": CLAIMS,
    },
    "r45": {
        "marker": "<!-- freeze-integrity-table v1 -->", "block": 22,
        "header": ["trigger", "arm", "exit", "receipt"], "min_rows": 8,
        "refs_min": 4, "require_line": False,
        "allow": ("corpus/lessons/", "corpus/knowledge/", "plans/"),
        "must_cite": [("literal", "S140"), ("path", "tools/round-45/frozen-path-preflight.py")],
        "must_cite_refs": [], "pin": None, "routed": False, "vocab": False,
        "v1_blocks": "eq", "v1_min_rows": 8, "claims": "plans/round-45-claims.md",
    },
}


class Malformed(Exception):
    pass


def craft_section(skill):
    if CRAFT not in skill:
        if MALFORMED in skill:
            raise Malformed("craft heading lacks its trailing space")
        raise Malformed("no `## Queue-drain craft ` section")
    return skill.split(CRAFT, 1)[1].split("\n## ", 1)[0]


def craft_blocks(skill):
    return re.split(r"(?m)^- \*\*", craft_section(skill))[1:]


def table(block):
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    rows, header = [], None
    for line in lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells):
            continue
        if header is None:
            header = cells
            continue
        rows.append(cells)
    return header or [], rows


def refs_in(block, hard=True):
    return (HARD_REF if hard else LOOSE_REF).findall(block)


def line_count(files, path):
    body = files(path)
    return None if body is None else len(body.splitlines())


def check_refs(block, files, spec, hard=True):
    refs = refs_in(block, hard)
    bad, cited, in_allow = [], set(), []
    for name, first, last in refs:
        if not name.startswith(spec["allow"]):
            bad.append(f"{name}: outside the validated path set")
            continue
        in_allow.append(name)
        cited.add(name)
        if spec["pin"] and name == spec["pin"]:
            # The interpreter carries its own identity (sha256 pin), not a line selector.
            continue
        if hard and spec["require_line"] and not first:
            bad.append(f"{name}: no line selector")
            continue
        count = line_count(files, name)
        if count is None:
            bad.append(f"{name}: absent at rev")
            continue
        start, end = int(first or 1), int(last or first or 1)
        if not (1 <= start <= end <= count):
            bad.append(f"{name}:{first or 1}-{end} outside 1..{count}")
    return in_allow, cited, bad


def score(skill, files, spec_name, profile, rev, battery=None):
    """Score one artefact. `files(path)` returns text at the measured revision or None."""
    spec = SPECS[spec_name]
    hard = profile == "v2"
    try:
        blocks = craft_blocks(skill)
    except Malformed as exc:
        return 2, {"reason": str(exc)}
    marker = spec["marker"]
    occurrences = skill.count(marker)
    marked = [b for b in blocks if marker in b]
    receipt = {
        "counter": "round-46-c1", "profile": profile, "spec": spec_name, "rev": rev,
        "rule_blocks": len(blocks), "marker_occurrences": occurrences,
        "block_present": len(marked),
    }
    failing = []
    if hard:
        if occurrences != 1:
            failing.append(f"marker_occurrences {occurrences} != 1")
        if len(marked) != 1:
            failing.append(f"marker_block_count {len(marked)} != 1")
    else:
        if len(marked) < 1:
            failing.append("marker_block_count 0")
        if spec["v1_blocks"] == "eq" and len(blocks) != spec["block"]:
            failing.append(f"rule_blocks {len(blocks)} != {spec['block']}")
        elif spec["v1_blocks"] == "ge" and len(blocks) < spec["block"]:
            failing.append(f"rule_blocks {len(blocks)} < {spec['block']}")

    if marked:
        block = marked[0]
        receipt["block_is_last"] = blocks[-1] is block
        receipt["block_title"] = block.split("**", 1)[0][:24]
        header, rows = table(block)
        receipt["header"] = header
        receipt["rows"] = len(rows)
        if hard and not receipt["block_is_last"]:
            failing.append("marker block is not the last craft block")
        if hard and not block.startswith(f"{spec['block']}. "):
            failing.append(f"marker block title does not start with '{spec['block']}. '")
        if hard:
            header_ok = header == spec["header"]
        else:
            # The v1 hole: substring containment, over the spec's own tokens.
            header_ok = all(any(t in h.lower() for h in header)
                            for t in (x.lower() for x in spec["header"]))
        receipt["header_ok"] = header_ok
        if not header_ok:
            failing.append(f"header {header} != {spec['header']}")
        floor = spec["min_rows"] if hard else spec.get("v1_min_rows", spec["min_rows"])
        if len(rows) < floor:
            failing.append(f"rows {len(rows)} < {floor}")
        width = len(spec["header"])
        exit_col = next((i for i, h in enumerate(header) if "exit" in h), None)
        bad_exit = [r for r in rows if exit_col is None or exit_col >= len(r)
                    or r[exit_col].strip("` ") not in {"0", "1", "2"}]
        if bad_exit:
            failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")
        if hard and any(len(r) != width for r in rows):
            failing.append("a row does not have exactly %d cells" % width)
        if spec["routed"] and hard:
            found = {m.group(0) for r in rows for m in re.finditer(r"R45-CL\d+", r[0])}
            missing = [i for i in ROUTED if i not in found]
            receipt["routed_ids"] = sorted(found)
            if missing:
                failing.append(f"routed ids not named by any row: {missing}")
            arm_col = 2
            novocab = [r for r in rows if len(r) > arm_col
                       and not any(t in r[arm_col].lower() for t in ARMS)]
            if novocab:
                failing.append(f"arm cells outside the vocabulary: {len(novocab)}")
        refs, cited, bad_refs = check_refs(block, files, spec, hard)
        receipt["refs"] = len(refs)
        receipt["cited"] = sorted(cited)
        receipt["unresolved_citations"] = bad_refs
        if len(refs) < spec["refs_min"]:
            failing.append(f"refs {len(refs)} < {spec['refs_min']}")
        if bad_refs:
            failing.append(f"unresolved or unvalidated citations: {len(bad_refs)}")
        if hard:
            for name in spec["must_cite_refs"]:
                if name not in cited:
                    failing.append(f"does not cite {name}")
        cites = {}
        for kind, token in spec["must_cite"]:
            cites[token] = token in block
            if not cites[token]:
                failing.append(f"does not cite {token}")
        receipt["cites"] = cites
        if spec["pin"] and hard:
            body = files(spec["pin"])
            if body is None:
                failing.append(f"pinned interpreter absent: {spec['pin']}")
            else:
                m = PIN.search(block)
                got = m.group(1) if m else None
                want = hashlib.sha256(body.encode()).hexdigest()
                receipt["pin"] = got
                receipt["pin_expected"] = want
                if got != want:
                    failing.append("interpreter sha256 pin does not match the bytes at rev")
    if battery is not None:
        receipt["battery"] = battery
        req = {"forgeries_total": 9, "v1_green": 9, "v2_green": 0, "genuine_green": 1,
               "v2_crash": 0}
        for key, want in req.items():
            if battery.get(key) != want:
                failing.append(f"battery {key} {battery.get(key)} != {want}")
    receipt["met_target"] = not failing
    receipt["failing"] = failing
    return (0 if not failing else 1), receipt


# --- battery: mutate this file's own block, one defect class per forgery ----------

def _rows_lines(block):
    out = []
    for line in block.splitlines():
        out.append(line)
    return out


def _table_line_indexes(block):
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    data = [i for i in idx if not all(re.fullmatch(r":?-{2,}:?", c.strip() or "") for c in lines[i].strip().strip("|").split("|"))]
    return lines, data[1:] if data else []


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def m_garbage(block, spec):
    lines, data = _table_line_indexes(block)
    for n, i in enumerate(data):
        lines[i] = f"| lorem {n} | ipsum | dolor | 1 |"
    return "\n".join(lines) + "\n"


def m_thin(block, spec):
    lines, data = _table_line_indexes(block)
    for i in data[8:]:
        lines[i] = None
    return "\n".join(l for l in lines if l is not None) + "\n"


def m_lineless(block, spec):
    return re.sub(r"(\.(?:md|py)):\d+(?:-\d+)?", r"\1", block)


def m_header_substring(block, spec):
    """Last header cell `exit` -> `exit-code`: a substring test still passes, equality fails."""
    lines, data = _table_indexes_lines(block)
    hdr = [i for i, l in enumerate(lines) if l.strip().startswith("|")][0]
    lines[hdr] = lines[hdr].rstrip().rstrip("|").rstrip() + "code |"
    return "\n".join(lines) + "\n"


def _table_indexes_lines(block):
    lines = block.splitlines()
    _, data = _table_line_indexes(block)
    return lines, data


def m_two_markers(block, spec):
    return block.replace(spec["marker"], spec["marker"] + "\n" + spec["marker"], 1)


def m_stub_pin(block, spec):
    out, n = PIN.subn("sha256:" + "0" * 64, block)
    if not n:
        raise ValueError("no pin in the block to stub")
    return out


def m_self_refs(block, spec):
    lines, data = _table_line_indexes(block)
    tail = [i for i in range(len(lines)) if lines[i].strip().startswith("Refs:")]
    if not tail:
        raise ValueError("no reference paragraph found")
    for i in tail:
        lines[i] = "  Refs: " + ", ".join(f"plans/round-46-claims.md:{k}" for k in range(1, 7)) + "\n"
    return "\n".join(lines) + "\n"


def m_missing_id(block, spec):
    lines, data = _table_line_indexes(block)
    hit = [i for i in data if "R45-CL18" in lines[i]]
    if not hit:
        raise ValueError("no R45-CL18 row to drop")
    lines[hit[0]] = None
    return "\n".join(l for l in lines if l is not None) + "\n"


def m_no_vocab(block, spec):
    lines, data = _table_line_indexes(block)
    for i in data:
        c = _cells(lines[i])
        c[2] = "zzz"
        lines[i] = "| " + " | ".join(c) + " |"
    return "\n".join(lines) + "\n"


MUTATIONS = [("garbage-rows", m_garbage), ("thin-rows", m_thin),
             ("lineless-refs", m_lineless), ("header-substring", m_header_substring),
             ("two-markers", m_two_markers), ("stub-pin", m_stub_pin),
             ("self-refs", m_self_refs), ("missing-routed-id", m_missing_id),
             ("no-vocab-arm", m_no_vocab)]


def fixture_repo(root, rev, skill_text, paths, scratch_root):
    """A one-commit repo holding the mutated SKILL plus the files its refs name."""
    d = tempfile.mkdtemp(dir=scratch_root, prefix="fx-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "fx@round46"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "round46 fixture"], check=True)
    if subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip() != d:
        raise RuntimeError("fixture toplevel mismatch")
    for p in paths:
        body = gate.show(root, rev, p)
        if body is None:
            continue
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    full = os.path.join(d, "SKILL.md")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(skill_text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    return d, subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()


def run_battery(root, rev, spec_name, scratch_root):
    spec = SPECS[spec_name]
    skill = gate.show(root, rev, "SKILL.md")
    if skill is None:
        return {"error": "SKILL.md absent at rev"}
    blocks = craft_blocks(skill)
    marked = [b for b in blocks if spec["marker"] in b]
    if len(marked) != 1:
        return {"error": f"cannot build a battery: marker blocks {len(marked)}"}
    block = marked[0]
    need = {"SKILL.md", spec["pin"] or "", CLAIMS, "corpus/lessons/round-45.md"}
    need |= {name for name, _, _ in refs_in(block, True)}
    need = sorted(p for p in need if p)
    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    out = {"fixtures": [], "forgeries_total": 0, "v1_green": 0, "v2_green": 0,
           "genuine_green": 0, "v2_crash": 0}
    code, rec = score(skill, files, spec_name, "v2", rev, battery=None)
    out["genuine_green"] = 1 if code == 0 else 0
    out["genuine_exit"] = code
    if code == 2:
        out["v2_crash"] += 1
    for name, fn in MUTATIONS:
        try:
            text = fn(block, spec)
        except ValueError as exc:
            out["fixtures"].append({"name": name, "error": str(exc)})
            out["forgeries_total"] += 1
            continue
        if text == block:
            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
            out["forgeries_total"] += 1
            out["v2_green"] += 1
            continue
        d, frev = fixture_repo(root, rev, skill.replace(block, text), need, scratch_root)
        try:
            f = lambda p, d=d: gate.show(d, frev, p)  # noqa: E731
            c1, r1 = score(skill.replace(block, text), f, spec_name, "v1", frev, battery=None)
            c2, r2 = score(skill.replace(block, text), f, spec_name, "v2", frev, battery=None)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out["forgeries_total"] += 1
        out["v1_green"] += 1 if c1 == 0 else 0
        out["v2_green"] += 1 if c2 == 0 else 0
        out["v2_crash"] += 1 if c2 == 2 else 0
        out["fixtures"].append({"name": name, "v1_exit": c1, "v2_exit": c2,
                                "v1_failing": r1.get("failing", r1.get("reason")),
                                "v2_failing": r2.get("failing", r2.get("reason"))})
    return out


# --- CLI ------------------------------------------------------------------------

def evaluate(root, freeze, rev, spec_name="r46", profile="v2", with_battery=True):
    flat, fs = gate.freeze_state(root, freeze, rev, SPECS[spec_name]["claims"])
    if flat == 2:
        return 2, dict(fs, counter="round-46-c1", profile=profile, spec=spec_name)
    skill = gate.show(root, rev, "SKILL.md")
    if skill is None:
        return 2, {"reason": "SKILL.md absent at rev", "counter": "round-46-c1"}
    files = lambda p: gate.show(root, fs["rev"], p)  # noqa: E731
    structural, receipt = score(skill, files, spec_name, profile, fs["rev"], battery=None)
    if with_battery and structural == 0:
        scratch_root, err = gate.scratch("kaidoku-r46-battery-")
        if err:
            return 2, {"reason": err, "counter": "round-46-c1"}
        try:
            battery = run_battery(root, fs["rev"], spec_name, scratch_root)
        finally:
            shutil.rmtree(scratch_root, ignore_errors=True)
        if "error" in battery:
            return 2, {"reason": "battery: " + battery["error"], "counter": "round-46-c1"}
        structural, receipt = score(skill, files, spec_name, profile, fs["rev"],
                                    battery=battery)
    elif with_battery:
        receipt["battery"] = {"skipped": "artefact fails a structural clause first"}
    code = structural
    receipt.update({"freeze": fs["freeze"], "frozen_derived": fs["frozen_derived"],
                    "frozen_path_changed": fs["frozen_path_changed"],
                    "touched": len(fs["touched"]), "restored": fs["restored"]})
    return code, receipt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--spec", default="r46", choices=sorted(SPECS))
    ap.add_argument("--profile", default="v2", choices=("v1", "v2"))
    ap.add_argument("--no-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    out, err = gate.out_path(args.root, args.json_out)
    if err:
        print(json.dumps({"reason": err}))
        return 2
    code, receipt = gate.main_guard(
        lambda: evaluate(args.root, args.freeze, args.rev, args.spec, args.profile,
                         not args.no_battery))
    gate.emit(receipt, out)
    return code




# --- selftest: one red case per clause -------------------------------------------

PIN_SELF = hashlib.sha256(open(__file__, "rb").read()).hexdigest()

GOOD_ROWS = [
    ("R45-CL2", "ghost instrument row", "presence", "1"),
    ("R45-CL6", "merge-introduced edit on a frozen path", "merge", "2"),
    ("R45-CL7", "`>=` block count survives the selftest", "rows", "1"),
    ("R45-CL9", "regex-valid but off-topic citation", "refs", "1"),
    ("R45-CL13", "structural proxy accepts garbage rows", "header", "1"),
    ("R45-CL14", "fenced registry row registers", "marker", "1"),
    ("R45-CL15", "dirty scope replaced instead of unioned", "dirty", "1"),
    ("R45-CL18", "pathspec boundary hides a restore", "restored", "1"),
    ("R45-CL19", "squashed side branch is invisible", "blob", "2"),
    ("R45-CL20", "scratch falls back to the temporary partition", "output", "2"),
    ("R45-CL22", "`--json-out` overwrites the graded surface", "output", "2"),
    ("R45-CL23", "C-quoted pathname kills the restored arm", "commit", "1"),
    ("R45-CL24", "record wording drifts from the instrument", "marker", "1"),
]
GOOD_REFS = ("`corpus/lessons/round-45.md:12-30`, `corpus/lessons/round-45.md:90-101`, "
             "`plans/round-46-claims.md:20`, `plans/round-46-claims.md:40`, "
             "`corpus/lessons/round-45.md:140-150`, `corpus/lessons/round-45.md:200-210`")


def good_block(rows=GOOD_ROWS, header="| trigger | v1 hole | v2 arm | exit |",
               refs=GOOD_REFS, pin=None, marker="<!-- freeze-integrity-table v2 -->",
               title="23. Freeze integrity is a discriminating instrument."):
    pin = pin or PIN_SELF
    body = (f"- **{title}** {marker} S142 `tools/round-46/attest.py` sha256:{pin}\n\n"
            f"{header}\n|---|---|---|---|\n")
    for r in rows:
        body += "| " + " | ".join(r) + " |\n"
    return body + f"\n  Refs: {refs}\n"


def skill_text(block, before=22, heading="## Queue-drain craft (test) ", after=""):
    text = "# SKILL\n\nintro\n\n" + heading + "\n\n"
    for i in range(1, before + 1):
        text += f"- **{i}. Plain rule {i}.** body text\n"
    return text + block + after + "\n## Next section\n\ntail\n"


CLAIMS_BODY = ("# claims\n\n" + "filler line\n" * 60 +
               "\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
               "- `tools/round-46/`\n\n## After\n\ntail\n")


def _case_repo(scratch_root, skill, heading="## Queue-drain craft (test) "):
    d = tempfile.mkdtemp(dir=scratch_root, prefix="self-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "st@round46"), ("user.name", "round46 selftest")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    here = os.path.dirname(os.path.abspath(__file__))
    files = {"SKILL.md": skill, "plans/round-46-claims.md": CLAIMS_BODY,
             "corpus/lessons/round-45.md": "lesson line\n" * 240,
             "tools/round-46/attest.py": open(os.path.join(here, "attest.py")).read(),
             "tools/round-46/gate.py": open(os.path.join(here, "gate.py")).read()}
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    return d, subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()


def selftest():
    root, err = gate.scratch("kaidoku-r46-selftest-")
    if err:
        print(json.dumps({"reason": err}))
        return 2
    cases = []

    def case(name, expect, maker, battery=False):
        d = None
        try:
            d, freeze, rev = maker()
            code, rec = evaluate(d, freeze, rev, "r46", "v2", with_battery=battery)
        except Exception as exc:  # noqa: BLE001
            code, rec = "crash", {"error": f"{type(exc).__name__}: {exc}"}
        finally:
            if d:
                shutil.rmtree(d, ignore_errors=True)
        cases.append({"case": name, "expect": expect, "got": code,
                      "ok": code == expect,
                      "failing": rec.get("failing") or rec.get("reason")})
        return code

    def plain(skill, heading="## Queue-drain craft (test) "):
        def maker():
            d, rev = _case_repo(root, skill, heading)
            return d, rev, rev
        return maker

    def touched():
        d, freeze = _case_repo(root, skill_text(good_block()))
        with open(os.path.join(d, "plans/round-46-claims.md"), "a") as fh:
            fh.write("late edit\n")
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "commit", "-q", "-m", "touch"], check=True)
        rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        return d, freeze, rev

    case("green", 0, plain(skill_text(good_block())))
    case("red-no-marker", 1,
         plain(skill_text(good_block().replace("<!-- freeze-integrity-table v2 -->", ""))))
    case("red-two-markers", 1,
         plain(skill_text(good_block().replace(
             "<!-- freeze-integrity-table v2 -->",
             "<!-- freeze-integrity-table v2 --> <!-- freeze-integrity-table v2 -->", 1))))
    case("red-marker-not-last", 1,
         plain(skill_text(good_block(), after="- **24. A later scratch block.** body\n")))
    case("red-title-unnumbered", 1,
         plain(skill_text(good_block(title="Freeze integrity, unnumbered."))))
    case("red-header-inexact", 1,
         plain(skill_text(good_block(header="| trigger | v1 hole | arm | exit |"))))
    case("red-rows-thin", 1, plain(skill_text(good_block(rows=GOOD_ROWS[:12]))))
    case("red-exit-cell", 1, plain(skill_text(good_block(
        rows=GOOD_ROWS[:12] + [("R45-CL24", "record drift", "marker", "0/1")]))))
    case("red-routed-id-missing", 1, plain(skill_text(good_block(
        rows=[r for r in GOOD_ROWS if r[0] != "R45-CL18"] + [("R45-CL2", "duplicate trigger", "presence", "1")]))))
    case("red-arm-vocabulary", 1,
         plain(skill_text(good_block(rows=[(a, b, "zzz", c) for a, b, _, c in GOOD_ROWS]))))
    case("red-ref-no-selector", 1,
         plain(skill_text(good_block(refs=GOOD_REFS.replace(":12-30", "").replace(":20", "")))))
    case("red-ref-outside-allowlist", 1,
         plain(skill_text(good_block(refs=GOOD_REFS.replace(
             "corpus/lessons/round-45.md:140-150", "corpus/QUALITY.md:3")))))
    case("red-pin-mismatch", 1,
         plain(skill_text(good_block(pin="0" * 64))))
    case("red-malformed-heading-is-exit-2", 2,
         plain(skill_text(good_block(), heading="## Queue-drain craft")))
    case("red-frozen-touched-is-exit-2", 2, touched)
    case("green-with-battery", 0, plain(skill_text(good_block())), battery=True)

    failures = [c for c in cases if not c["ok"]]
    print("ATTEST_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    print(json.dumps({"cases": cases, "failures": len(failures)}, indent=1))
    shutil.rmtree(root, ignore_errors=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
