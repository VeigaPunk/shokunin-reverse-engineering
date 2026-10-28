#!/usr/bin/env python3
"""Round-48 C1 counter — verdict maps bound to MEANINGS, not to digits.

Routed defects this counter closes (both HIGH, `corpus/lessons/round-47.md`):

- **R46-CL7** the round-46 registry counter binds the digits 0/1/2 rather than their
  meanings, so a row whose verdict cell reads `0=banana; 1=nope; 2=whatever` still
  scores met.  Here every row's verdict cell is split into its three segments and each
  segment must carry the meaning class its digit claims, drawn from a frozen vocabulary.
- **R47-CL10** the round-47 block scored a *membership* test and an at-least-once id
  test, so four rows naming the wrong arm for every routed defect still passed.  Here
  each routed id maps to exactly one expected arm (`EXPECTED_ARM`) and the row's arm
  cell must equal it.

Profiles:
  v3 (default) — meaning classes, per-id expected arms, a mutation digest over each
                 mutation's name *and body*, the interpreter pin, the census re-derivation
                 and the registry meaning binding.
  v2           — the round-46/47 semantics ported (digits present, arm membership,
                 at-least-once ids, no digest/pin/census/meaning clause); used only to
                 score the round's own forgeries against the holes it measures.

Exit codes: 0 met; 1 not met; 2 could-not-evaluate.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round-46"))
import gate  # noqa: E402

SELF = "tools/round-48/meanings.py"
CLAIMS = "plans/round-48-claims.md"
CENSUS = "tools/round-48/census2.json"
CENSUS_TOOL = "tools/round-48/census2.py"
CRAFT = "## Queue-drain craft "
MALFORMED = "## Queue-drain craft\n"
MARKER = "<!-- verdict-meaning-table v1 -->"
HEADER = ["trigger", "v1 hole", "v2 arm", "exit"]
ROUTED = ["R46-CL7", "R47-CL10"]
EXPECTED_ARM = {"R46-CL7": "meaning", "R47-CL10": "floor"}
VOCAB = ("meaning", "floor")
ALLOW = ("corpus/lessons/", "corpus/knowledge/", "plans/", "tools/round-48/")
MUST_CITE = "corpus/lessons/round-47.md"
MUST_KNOW = "corpus/knowledge/"
REG_OPEN = "<!-- instrument-registry v2 -->"
REG_CLOSE = "<!-- /instrument-registry -->"
HARD_REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")
MUT_PIN = re.compile(r"mutations_sha256:([0-9a-f]{64})")
SELF_PIN = re.compile(r"interpreter_sha256:([0-9a-f]{64})")
ID = re.compile(r"R4[67]-CL\d+")
SEG = re.compile(r"(?<![0-9])([012])\s*=\s*")
SUCCESS = re.compile(r"\b(met|clean|ok|green|pass|passed|verified|succeeded|wrote)\b")
NOTMET = re.compile(r"(not met|violation|red|fail|failed|no verdict|refusal|refused|unresolved)")
UNEVAL = re.compile(r"(could-not-evaluate|unevaluable|could not evaluate|\busage\b|"
                    r"\berror\b|absent|unreadable|refus)")
NEGATED = re.compile(r"\bnot\s+met\b|\bno\s+verdict\b")
BANANA = re.compile(r"\b(banana|nope|whatever)\b")


class Malformed(Exception):
    pass


# --- the mutation list, and the digest the block must pin -------------------------

def _table_span(block):
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    if not idx:
        raise ValueError("no table in the block")
    return lines, idx[0], idx[-1]


def rewrite_rows(block, rows):
    lines, start, end = _table_span(block)
    header, _ = table(block)
    body = ["| " + " | ".join(header) + " |",
            "|" + "|".join(["---"] * len(header)) + "|"]
    body += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines[:start] + body + lines[end + 1:])


def _m_gold_meaning(skill, spec):
    return _rewrite_registry(skill, lambda cells: cells[:2] + [
        "0=banana; 1=nope; 2=whatever"] + cells[3:]), {}


def _m_swapped_meaning(skill, spec):
    def swap(cells):
        segs = _segments(cells[2])
        if len(segs) != 3:
            return cells
        cells = list(cells)
        cells[2] = f"0={segs['2']}; 1={segs['1']}; 2={segs['0']}"
        return cells
    return _rewrite_registry(skill, swap), {}


def _m_duplicate_meaning(skill, spec):
    def dup(cells):
        segs = _segments(cells[2])
        if len(segs) != 3:
            return cells
        cells = list(cells)
        cells[2] = f"0={segs['0']}; 1={segs['0']}; 2={segs['2']}"
        return cells
    return _rewrite_registry(skill, dup), {}


def _m_permuted_arm(skill, spec):
    block = [b for b in blocks_of(skill) if MARKER in b][0]
    rows = [r[:] for r in _rows(block)]
    if len(rows) >= 2:
        rows[0][2], rows[1][2] = rows[1][2], rows[0][2]
    return skill.replace(block, rewrite_rows(block, rows), 1), {}


MUTATIONS = [("gold-meaning", _m_gold_meaning),
             ("swapped-meaning", _m_swapped_meaning),
             ("duplicate-meaning", _m_duplicate_meaning),
             ("permuted-arm", _m_permuted_arm)]


def _mut_digest():
    """sha256 over each mutation's NAME and its own source body (closes R47-CL4)."""
    import inspect
    h = hashlib.sha256()
    for name, fn in MUTATIONS:
        h.update(name.encode())
        h.update(b"\n")
        h.update(inspect.getsource(fn).encode())
        h.update(b"\n---\n")
    return h.hexdigest()


MUT_DIGEST = _mut_digest()


# --- parse helpers ----------------------------------------------------------------

def craft_section(skill):
    if CRAFT not in skill:
        if MALFORMED in skill:
            raise Malformed("craft heading lacks its trailing space")
        raise Malformed("no `## Queue-drain craft ` section")
    return skill.split(CRAFT, 1)[1].split("\n## ", 1)[0]


def blocks_of(skill):
    return re.split(r"(?m)^- \*\*", craft_section(skill))[1:]


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(block):
    lines = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    rows, header = [], None
    for line in lines:
        cells = _cells(line)
        if all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells):
            continue
        if header is None:
            header = cells
            continue
        rows.append(cells)
    return header or [], rows


def _rows(block):
    return table(block)[1]


def registry_rows(skill):
    if REG_OPEN not in skill or REG_CLOSE not in skill:
        raise Malformed("registry markers absent or doubled")
    if skill.count(REG_OPEN) != 1 or skill.count(REG_CLOSE) != 1:
        raise Malformed("registry markers doubled")
    body = skill.split(REG_OPEN, 1)[1].split(REG_CLOSE, 1)[0]
    rows = []
    for line in body.splitlines():
        if ROW_START.match(line.strip()):
            cells = _cells(line)
            if len(cells) != 7:
                raise Malformed(f"registry row has {len(cells)} cells, not 7: {line[:60]}")
            rows.append({"path": cells[0].strip("` "), "purpose": cells[1],
                         "verdict": cells[2], "selftest": cells[3],
                         "pinned": cells[4], "write": cells[5], "owner": cells[6]})
    return rows


ROW_START = re.compile(r"^\|\s*`")


def _rewrite_registry(skill, fn):
    head, rest = skill.split(REG_OPEN, 1)
    body, tail = rest.split(REG_CLOSE, 1)
    out = []
    for line in body.splitlines():
        if ROW_START.match(line.strip()):
            cells = _cells(line)
            if len(cells) == 7:
                cells = fn(cells)
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return head + REG_OPEN + "\n".join(out) + REG_CLOSE + tail


def _segments(cell):
    """{digit: text} for the three verdict-map segments, or {} when malformed."""
    text = cell.strip()
    marks = list(SEG.finditer(text))
    if [m.group(1) for m in marks] != ["0", "1", "2"]:
        return {}
    out = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[m.group(1)] = text[m.end():end].strip().rstrip(";").strip()
    return out


def meaning_classes(cell):
    """{digit: class} or {'error': reason}."""
    segs = _segments(cell)
    if not segs:
        return {"error": "verdict map does not parse as 0=;1=;2="}
    low = {k: v.lower() for k, v in segs.items()}
    if BANANA.search(" ".join(low.values())):
        return {"error": "verdict map names no meaning class (placeholder text)"}
    cls = {}
    # A success class may not be negated in the same segment: `0=not met` is the
    # opposite polarity, and `\bmet\b` matches inside it (wave-1 C1Gold).
    cls["0"] = "success" if SUCCESS.search(low["0"]) and not NEGATED.search(low["0"]) else None
    cls["1"] = "not-met" if NOTMET.search(low["1"]) else None
    cls["2"] = "unevaluable" if UNEVAL.search(low["2"]) else None
    if cls["0"] is None:
        return {"error": "exit 0 segment names no success meaning"}
    if cls["1"] is None:
        return {"error": "exit 1 segment names no not-met meaning"}
    if cls["2"] is None:
        return {"error": "exit 2 segment names no unevaluable meaning"}
    if len(set(low.values())) != 3:
        return {"error": "verdict segments are not three distinct meanings"}
    return cls


def line_count(files, path):
    body = files(path)
    return None if body is None else len(body.splitlines())


def check_refs(block, files, hard):
    bad, cited = [], set()
    for name, first, last in HARD_REF.findall(block):
        if not name.startswith(ALLOW):
            bad.append(f"{name}: outside the validated path set")
            continue
        cited.add(name)
        if name == SELF:
            continue
        if hard and not first:
            bad.append(f"{name}: no line selector")
            continue
        count = line_count(files, name)
        if count is None:
            bad.append(f"{name}: absent at rev")
            continue
        start, end = int(first or 1), int(last or first or 1)
        if not (1 <= start <= end <= count):
            bad.append(f"{name}:{start}-{end} outside 1..{count}")
    return bad, cited


def census_doc(files):
    body = files(CENSUS)
    if body is None:
        raise Malformed(f"{CENSUS} absent at rev")
    try:
        doc = json.loads(body)
    except ValueError as exc:
        raise Malformed(f"{CENSUS} unreadable: {exc}")
    if not isinstance(doc.get("paths"), list):
        raise Malformed(f"{CENSUS} has no paths list")
    return doc


def census_rederive(files):
    """Re-run the census rule over the claims files at rev (rule from census2.py)."""
    tool = files(CENSUS_TOOL)
    if tool is None:
        raise Malformed(f"{CENSUS_TOOL} absent at rev")
    ns = {"__name__": "census2_mod"}
    exec(compile(tool, CENSUS_TOOL, "exec"), ns)  # noqa: S102 - frozen lane bytes
    read = lambda p: files(p)  # noqa: E731
    return ns["census_text"](read)


# --- score ------------------------------------------------------------------------

def score(skill, files, profile, rev, battery=None):
    hard = profile == "v3"
    try:
        blocks = blocks_of(skill)
    except Malformed as exc:
        return 2, {"reason": str(exc)}
    occurrences = skill.count(MARKER)
    marked = [b for b in blocks if MARKER in b]
    receipt = {"counter": "round-48-c1", "profile": profile, "rev": rev,
               "rule_blocks": len(blocks), "marker_occurrences": occurrences,
               "block_present": len(marked)}
    failing = []
    if hard:
        if occurrences != 1:
            failing.append(f"marker_occurrences {occurrences} != 1")
        if len(marked) != 1:
            failing.append(f"marker_block_count {len(marked)} != 1")
    else:
        if not marked:
            failing.append("marker_block_count 0")
    if not marked:
        receipt.update(met_target=False, failing=failing)
        return 1, receipt
    block = marked[0]
    header, rows = table(block)
    receipt.update({"block_is_last": blocks[-1] is block,
                    "block_title": block.split("**", 1)[0][:24],
                    "header": header, "rows": len(rows)})
    if hard and not receipt["block_is_last"]:
        failing.append("marker block is not the last craft block")
    if hard and not block.startswith("25. "):
        failing.append("marker block title does not start with '25. '")
    header_ok = header == HEADER if hard else all(
        any(t in h.lower() for h in header) for t in (x.lower() for x in HEADER))
    receipt["header_ok"] = header_ok
    if not header_ok:
        failing.append(f"header {header} != {HEADER}")
    if hard:
        if len(rows) != 2:
            failing.append(f"rows {len(rows)} != 2")
        if any(len(r) != 4 for r in rows):
            failing.append("a row does not have exactly 4 cells")
    elif len(rows) < 2:
        failing.append(f"rows {len(rows)} < 2")
    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in {"0", "1", "2"}]
    if bad_exit:
        failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")

    # clause: routed ids, and the per-id expected arm (closes R47-CL10) --------------
    per_row = [ID.findall(r[0]) if r else [] for r in rows]
    counts = {}
    for ids in per_row:
        for i in ids:
            counts[i] = counts.get(i, 0) + 1
    receipt["routed_counts"] = counts
    arm_by_id = {}
    for ids, r in zip(per_row, rows):
        if len(ids) == 1 and len(r) > 2:
            arm_by_id[ids[0]] = r[2].strip("` ")
    receipt["arm_by_id"] = arm_by_id
    if hard:
        if [n for n, ids in enumerate(per_row) if len(ids) != 1]:
            failing.append("a row does not name exactly one routed id")
        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:
            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")
        wrong = {k: v for k, v in arm_by_id.items() if EXPECTED_ARM.get(k) != v}
        if wrong or sorted(arm_by_id) != sorted(ROUTED):
            failing.append(f"row arm does not equal the arm expected for its routed id: {wrong}")
    else:
        missing = [i for i in ROUTED if i not in counts]
        if missing:
            failing.append(f"routed ids not named by any row: {missing}")

    arm = [r[2].strip("` ") if len(r) > 2 else "" for r in rows]
    receipt["arm_tokens"] = arm
    if hard:
        if any(a not in VOCAB for a in arm):
            failing.append(f"arm cells not exact vocabulary tokens: {arm}")
    elif any(not any(t in a.lower() for t in VOCAB) for a in arm):
        failing.append("arm cells outside the vocabulary")

    # digest, pin, refs ------------------------------------------------------------
    if hard:
        m = MUT_PIN.search(block)
        receipt["mutations_sha256"] = m.group(1) if m else None
        receipt["mutations_sha256_expected"] = MUT_DIGEST
        if not m or m.group(1) != MUT_DIGEST:
            failing.append("mutations_sha256 does not match the counter's own "
                           "name+body mutation digest")
        unnamed = [n for n, _ in MUTATIONS if n not in block]
        if unnamed:
            failing.append(f"mutation names not stated in the block: {unnamed}")
    bad_refs, cited = check_refs(block, files, hard)
    receipt["refs"] = len(HARD_REF.findall(block))
    receipt["cited"] = sorted(cited)
    receipt["unresolved_citations"] = bad_refs
    if receipt["refs"] < (5 if hard else 3):
        failing.append(f"refs {receipt['refs']} < {5 if hard else 3}")
    if bad_refs:
        failing.append(f"unresolved or unvalidated citations: {len(bad_refs)}")
    if hard:
        if MUST_CITE not in cited:
            failing.append(f"does not cite {MUST_CITE}")
        if not any(c.startswith(MUST_KNOW) and HARD_REF.search(block) for c in cited):
            failing.append(f"does not cite a {MUST_KNOW} entry with a line range")
        m = SELF_PIN.search(block)
        body = files(SELF)
        want = hashlib.sha256(body.encode()).hexdigest() if body else None
        receipt["interpreter_sha256"] = m.group(1) if m else None
        receipt["interpreter_sha256_expected"] = want
        if want is None:
            failing.append("interpreter absent at rev")
        elif not m or m.group(1) != want:
            failing.append("interpreter sha256 pin does not match the bytes at rev")

    # registry meaning binding (closes R46-CL7) ------------------------------------
    if hard:
        try:
            rows_reg = registry_rows(skill)
            doc = census_doc(files)
            derived = census_rederive(files)
        except Malformed as exc:
            failing.append(f"registry/census malformed: {exc}")
            receipt["met_target"] = False
            receipt["failing"] = failing
            return 1, receipt
        paths = [r["path"] for r in rows_reg]
        receipt.update({"registry_rows": len(paths), "census_paths": len(doc["paths"]),
                        "census_rederived_equal": derived.get("paths") == doc["paths"]})
        dup = sorted({p for p in paths if paths.count(p) > 1})
        missing = sorted(set(doc["paths"]) - set(paths))
        extra = sorted(set(paths) - set(doc["paths"]))
        receipt.update({"registry_duplicates": dup, "registry_missing": missing,
                        "registry_extra": extra})
        if dup:
            failing.append(f"registry rows duplicated: {dup}")
        if missing:
            failing.append(f"census paths with no registry row: {missing}")
        if extra:
            failing.append(f"registry rows outside the census: {extra}")
        if not receipt["census_rederived_equal"]:
            failing.append("committed census2.json does not equal a fresh derivation")
        bad_meaning = []
        for r in rows_reg:
            cls = meaning_classes(r["verdict"])
            if "error" in cls:
                bad_meaning.append({"path": r["path"], "error": cls["error"]})
        receipt["meaning_rows_failed"] = len(bad_meaning)
        receipt["meaning_failures"] = bad_meaning[:10]
        if bad_meaning:
            failing.append(f"verdict maps not bound to meanings: {len(bad_meaning)}")

    if battery is not None:
        receipt["battery"] = battery
        for key, want in (("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),
                          ("genuine_green", 1), ("crash", 0)):
            if battery.get(key) != want:
                failing.append(f"battery {key} {battery.get(key)} != {want}")
    receipt["met_target"] = not failing
    receipt["failing"] = failing
    return (0 if not failing else 1), receipt


# --- battery ----------------------------------------------------------------------

def _fixture_files(root, rev):
    files = {}
    for p in (CLAIMS, SELF, CENSUS, CENSUS_TOOL, MUST_CITE,
              "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md"):
        body = gate.show(root, rev, p)
        if body is not None:
            files[p] = body
    # The census rule reads every claims file it names AND checks that each named tool
    # exists; a fixture missing either re-derives a shorter census and scores the genuine
    # block red (A5, A6).
    try:
        doc = json.loads(files.get(CENSUS, "{}"))
        for path in list(doc.get("per_claims_file", {})) + list(doc.get("paths", [])):
            if path in files:
                continue
            body = gate.show(root, rev, path)
            if body is not None:
                files[path] = body
    except ValueError:
        pass
    skill = gate.show(root, rev, "SKILL.md")
    if skill is not None:
        files["SKILL.md"] = skill
        try:
            marked = [b for b in blocks_of(skill) if MARKER in b]
        except Malformed:
            marked = []
        if marked:
            for name, _, _ in HARD_REF.findall(marked[0]):
                if name not in files:
                    body = gate.show(root, rev, name)
                    if body is not None:
                        files[name] = body
    return files


def run_battery(root, rev, scratch_root=None):
    skill = gate.show(root, rev, "SKILL.md")
    if skill is None:
        return {"error": "SKILL.md absent at rev"}
    try:
        marked = [b for b in blocks_of(skill) if MARKER in b]
    except Malformed as exc:
        return {"error": f"cannot build a battery: {exc}"}
    if len(marked) != 1:
        return {"error": f"cannot build a battery: marker blocks {len(marked)}"}
    block = marked[0]
    base = _fixture_files(root, rev)
    files = lambda p: base.get(p)  # noqa: E731
    out = {"fixtures": [], "forgeries_total": 0, "v2_green": 0, "v3_green": 0,
           "genuine_green": 0, "crash": 0, "mutations_sha256": MUT_DIGEST}
    code, _ = score(skill, files, "v3", rev, battery=None)
    out["genuine_green"] = 1 if code == 0 else 0
    out["genuine_exit"] = code
    out["crash"] += 1 if code == 2 else 0
    for name, fn in MUTATIONS:
        text, overrides = fn(skill, None)
        if text == skill and not overrides:
            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
            out["forgeries_total"] += 1
            out["v2_green"] += 1
            continue
        fx = dict(base)
        fx["SKILL.md"] = text
        c2, r2 = score(text, lambda p: fx.get(p), "v2", rev, battery=None)
        c3, r3 = score(text, lambda p: fx.get(p), "v3", rev, battery=None)
        out["forgeries_total"] += 1
        out["v2_green"] += 1 if c2 == 0 else 0
        out["v3_green"] += 1 if c3 == 0 else 0
        out["crash"] += 1 if c3 == 2 else 0
        out["fixtures"].append({"name": name, "v2_exit": c2, "v3_exit": c3,
                                "v2_failing": r2.get("failing", r2.get("reason")),
                                "v3_failing": r3.get("failing", r3.get("reason"))})
    return out


# --- CLI --------------------------------------------------------------------------

def evaluate(root, freeze, rev, profile="v3", with_battery=True):
    flat, fs = gate.freeze_state(root, freeze, rev, CLAIMS)
    if flat == 2:
        return 2, dict(fs, counter="round-48-c1", profile=profile)
    skill = gate.show(root, rev, "SKILL.md")
    if skill is None:
        return 2, {"reason": "SKILL.md absent at rev", "counter": "round-48-c1"}
    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    code, receipt = score(skill, files, profile, rev, battery=None)
    if with_battery and code == 0:
        battery = run_battery(root, rev)
        if "error" in battery:
            return 2, {"reason": "battery: " + battery["error"], "counter": "round-48-c1"}
        code, receipt = score(skill, files, profile, rev, battery=battery)
    elif with_battery:
        receipt["battery"] = {"skipped": "artefact fails a structural clause first"}
    receipt.update({"freeze": fs["freeze"], "frozen_derived": fs["frozen_derived"],
                    "frozen_path_changed": fs["frozen_path_changed"],
                    "touched": len(fs["touched"]), "restored": fs["restored"]})
    return code, receipt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root")
    ap.add_argument("--freeze")
    ap.add_argument("--rev")
    ap.add_argument("--profile", default="v3", choices=("v2", "v3"))
    ap.add_argument("--no-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    missing = [k for k in ("root", "freeze", "rev") if not getattr(args, k)]
    if missing:
        ap.error("missing required arguments: " + ", ".join("--" + k for k in missing))
    out, err = gate.out_path(args.root, args.json_out)
    if err:
        print(json.dumps({"reason": err}))
        return 2
    code, receipt = gate.main_guard(
        lambda: evaluate(args.root, args.freeze, args.rev, args.profile,
                         not args.no_battery))
    gate.emit(receipt, out)
    return code


# --- selftest ---------------------------------------------------------------------

GOOD_ROWS = [("R46-CL7", "`0=banana; 1=nope; 2=whatever` scores met", "meaning", "1"),
             ("R47-CL10", "four rows name the wrong arm and still pass", "floor", "1")]
GOOD_VERDICT = ("0=met, the target holds; 1=not met, a clause is false; "
                "2=could-not-evaluate, the revision or a frozen file is unusable")
GOOD_REFS = ("`corpus/lessons/round-47.md:30-50`, `corpus/lessons/round-46.md:57-66`, "
             "`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`, "
             "`plans/round-48-claims.md:20`, `plans/round-48-claims.md:40`")
CLAIMS_BODY = ("# claims\n\n" + "filler line\n" * 60 +
               "\n## Frozen paths (exact)\n\n- `plans/round-48-claims.md`\n"
               "- `tools/round-48/`\n\n## After\n\ntail\n")


def good_registry(paths, verdict=GOOD_VERDICT):
    body = ("intro\n\n" + REG_OPEN + "\n\n"
            "| tool | gate or probe - purpose | verdict map (exit codes) | self-test | "
            "pinned-value path | write scope | owner |\n"
            "|---|---|---|---|---|---|---|\n")
    for p in paths:
        body += f"| `{p}` | gate — test | {verdict} | none | none | none | kaidoku |\n"
    return body + "\n" + REG_CLOSE + "\n"


def good_block(rows=None, header="| trigger | v1 hole | v2 arm | exit |",
               refs=GOOD_REFS, digest=None, pin=None, marker=MARKER,
               title="25. A verdict map binds meanings, and a denominator is a floor."):
    rows = GOOD_ROWS if rows is None else rows
    digest = digest or MUT_DIGEST
    pin = pin or hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    body = (f"- **{title}** {marker} `tools/round-48/meanings.py` interpreter_sha256:{pin} "
            f"mutations_sha256:{digest} names gold-meaning, swapped-meaning, "
            f"duplicate-meaning, permuted-arm.\n\n{header}\n|---|---|---|---|\n")
    for r in rows:
        body += "| " + " | ".join(r) + " |\n"
    return body + f"\n  Refs: {refs}\n"


def skill_text(block, registry, before=24, heading="## Queue-drain craft (test) "):
    text = "# SKILL\n\nintro\n\n" + heading + "\n\n"
    for i in range(1, before + 1):
        text += f"- **{i}. Plain rule {i}.** body text\n"
    return (text + block + "\n## Instrument registry\n\n" + registry +
            "\n## Next section\n\ntail\n")


def selftest():
    root, err = gate.scratch("kaidoku-r48-selftest-")
    if err:
        print(json.dumps({"reason": err}))
        return 2
    paths = ["tools/round-41/c1-counter.py", "tools/round-48/meanings.py"]
    census = {"rule": "selftest", "paths": paths}
    base_files = {"plans/round-48-claims.md": CLAIMS_BODY,
                  "corpus/lessons/round-47.md": "lesson line\n" * 240,
                  "corpus/lessons/round-46.md": "lesson line\n" * 240,
                  "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md":
                      "knowledge line\n" * 240,
                  CENSUS: json.dumps(census),
                  CENSUS_TOOL: ("def census_text(read):\n"
                                "    return {'paths': %r}\n" % (paths,)),
                  SELF: open(__file__).read()}
    cases = []

    def run(name, expect, skill, overrides=None, profile="v3"):
        files = dict(base_files)
        files.update(overrides or {})
        try:
            got, rec = score(skill, lambda p: files.get(p), profile, "selftest",
                             battery=None)
        except Exception as exc:  # noqa: BLE001
            got, rec = "crash", {"reason": f"{type(exc).__name__}: {exc}"}
        cases.append({"case": name, "expect": expect, "got": got, "ok": got == expect,
                      "failing": rec.get("failing") or rec.get("reason")})
        return got

    good = skill_text(good_block(), good_registry(paths))
    run("green", 0, good)
    run("red-marker-missing", 1, skill_text(good_block(marker=""), good_registry(paths)))
    run("red-title-unnumbered", 1, skill_text(
        good_block(title="A verdict map, unnumbered."), good_registry(paths)))
    run("red-header-inexact", 1, skill_text(
        good_block(header="| trigger | v1 hole | arm | exit |"), good_registry(paths)))
    run("red-rows-not-two", 1, skill_text(
        good_block(rows=GOOD_ROWS[:1]), good_registry(paths)))
    run("red-permuted-arm", 1, skill_text(
        good_block(rows=[(GOOD_ROWS[0][0], GOOD_ROWS[0][1], "floor", "1"),
                         (GOOD_ROWS[1][0], GOOD_ROWS[1][1], "meaning", "1")]),
        good_registry(paths)))
    run("red-digest-stale", 1, skill_text(
        good_block(digest=hashlib.sha256(b"gold-meaning").hexdigest()),
        good_registry(paths)))
    run("red-pin-mismatch", 1, skill_text(good_block(pin="0" * 64), good_registry(paths)))
    run("red-gold-meaning", 1, skill_text(
        good_block(), good_registry(paths, "0=banana; 1=nope; 2=whatever")))
    run("red-swapped-meaning", 1, skill_text(
        good_block(), good_registry(paths, GOOD_VERDICT.replace("0=met,", "0=zzz,")
                                    .replace("2=could-not-evaluate,", "2=could-not-evaluate,"))))
    run("red-opposite-polarity", 1, skill_text(
        good_block(), good_registry(paths, "0=not met; 1=violation; 2=usage")))
    hidden = ("|  `" + paths[0] + "` | gate — hidden | " + GOOD_VERDICT +
              " | none | none | none | kaidoku |\n")
    run("red-hidden-row", 1, skill_text(
        good_block(), good_registry(paths).replace(
            "| `" + paths[0] + "`", hidden + "| `" + paths[0] + "`", 1)))
    run("red-registry-missing-row", 1, skill_text(good_block(), good_registry(paths[:1])))
    run("red-registry-extra-row", 1, skill_text(
        good_block(), good_registry(paths + ["tools/round-40/ghost.py"])))
    run("red-census-stale", 1, skill_text(good_block(), good_registry(paths)),
        overrides={CENSUS: json.dumps({"rule": "selftest", "paths": paths + ["x.py"]})})
    run("red-ref-no-selector", 1, skill_text(
        good_block(refs=GOOD_REFS.replace(":20", "")), good_registry(paths)))
    run("red-malformed-heading-is-exit-2", 2, skill_text(
        good_block(), good_registry(paths), heading="## Queue-drain craft"))

    # the battery, in memory: every forgery green under v2, red under v3
    files = dict(base_files)
    files["SKILL.md"] = good
    bat = {"fixtures": [], "forgeries_total": 0, "v2_green": 0, "v3_green": 0,
           "genuine_green": 0, "crash": 0}
    code, _ = score(good, lambda p: files.get(p), "v3", "selftest", battery=None)
    bat["genuine_green"] = 1 if code == 0 else 0
    for name, fn in MUTATIONS:
        text, _ = fn(good, None)
        if text == good:
            bat["fixtures"].append({"name": name, "error": "no-op"})
            bat["forgeries_total"] += 1
            continue
        c2, _ = score(text, lambda p: files.get(p), "v2", "selftest", battery=None)
        c3, _ = score(text, lambda p: files.get(p), "v3", "selftest", battery=None)
        bat["forgeries_total"] += 1
        bat["v2_green"] += 1 if c2 == 0 else 0
        bat["v3_green"] += 1 if c3 == 0 else 0
        bat["crash"] += 1 if c3 == 2 else 0
        bat["fixtures"].append({"name": name, "v2_exit": c2, "v3_exit": c3})
    ok = (bat["forgeries_total"] == 4 and bat["v2_green"] == 4 and bat["v3_green"] == 0
          and bat["genuine_green"] == 1 and bat["crash"] == 0)
    cases.append({"case": "battery-discriminates", "expect": True, "got": bool(ok),
                  "ok": bool(ok), "failing": None if ok else bat})

    failures = [c for c in cases if not c["ok"]]
    print("MEANINGS_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    print(json.dumps({"cases": cases, "failures": len(failures)}, indent=1))
    shutil.rmtree(root, ignore_errors=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
