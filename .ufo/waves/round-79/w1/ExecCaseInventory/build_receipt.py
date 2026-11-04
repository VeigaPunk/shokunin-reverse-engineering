import hashlib, json, pathlib, subprocess
S = pathlib.Path("/fast/scratch/hyaku/kaidoku-r79/ExecCaseInventory")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
OUT = LANE / ".ufo/waves/round-79/w1/ExecCaseInventory"
BASE_REV = "29d2ca30b83a6a0d85b0aa979de0138fde1660e6"
FREEZE_REV = "ed68cd0a6cc790cca342380a2d80d1927a668c8c"
TOOL = "tools/round-78/attack-gate.py"

def read_run(path):
    cases, summary = [], None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("SELFTEST "):
            summary = line
            continue
        cases.append(json.loads(line))
    return cases, summary

def sha(b):
    return hashlib.sha256(b).hexdigest()

def names_digest(names):
    return sha("\n".join(sorted(names)).encode())

def rev_tool(rev):
    return subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{TOOL}"],
                          capture_output=True, check=True).stdout

b_cases, b_sum = read_run(S / "base-selftest.out")
f_cases, f_sum = read_run(S / "freeze-selftest.out")
bn = [c["case"] for c in b_cases]
fn = [c["case"] for c in f_cases]
added = [n for n in fn if n not in set(bn)]
removed = [n for n in bn if n not in set(fn)]

def dup(names):
    seen, out = set(), []
    for n in names:
        if n in seen and n not in out:
            out.append(n)
        seen.add(n)
    return out

ablation = json.loads((S / "ablation.json").read_text())
expected_added = ["red-near-miss-unparsed", "red-atom-absent",
                  "red-validate-refused-no-reason"]

receipt = {
    "seat": "ExecCaseInventory",
    "round": 79,
    "instrument": TOOL,
    "method": ("git show <rev>:tools/round-78/attack-gate.py into scratch, then "
               "python3 <copy> --selftest; case list = JSON lines keyed 'case'; "
               "counts from the SELFTEST summary line; names_digest = sha256 of "
               "sorted names joined by '\\n' with no trailing newline"),
    "base": {
        "rev": BASE_REV,
        "instrument_sha256": sha(rev_tool(BASE_REV)),
        "cases": len(bn),
        "failures": sum(1 for c in b_cases if not c["pass"]),
        "summary_line": b_sum,
        "names_digest": names_digest(bn),
        "names_digest_emitted_order": sha("\n".join(bn).encode()),
        "names": bn,
    },
    "freeze": {
        "rev": FREEZE_REV,
        "instrument_sha256": sha(rev_tool(FREEZE_REV)),
        "cases": len(fn),
        "failures": sum(1 for c in f_cases if not c["pass"]),
        "summary_line": f_sum,
        "names_digest": names_digest(fn),
        "names_digest_emitted_order": sha("\n".join(fn).encode()),
        "names": fn,
    },
    "added": added,
    "removed": removed,
    "expected_added": expected_added,
    "added_matches_declared_claim": added == expected_added,
    "duplicates": {"base": dup(bn), "freeze": dup(fn)},
    "count_delta": len(fn) - len(bn),
    "base_is_prefix_of_freeze": fn[:len(bn)] == bn,
    "case_to_path": [
        {"case": "red-near-miss-unparsed",
         "function": "judge_group",
         "path": TOOL,
         "line": 394,
         "branch": ("near is None and NEAR_MISS_RE.match(clause) -> "
                    "'near_miss_field' finding"),
         "ablation": "near-miss-re-dead"},
        {"case": "red-atom-absent",
         "function": "bind_clause",
         "path": TOOL,
         "line": 311,
         "branch": ("kind == 'field' and ATOM_ID_RE.match(field) and "
                    "not isinstance(receipt.get('atoms'), list) -> "
                    "(False, 'defect', {'reason': 'no_atoms'})"),
         "ablation": "atom-absent-bound"},
        {"case": "red-validate-refused-no-reason",
         "function": "validate_receipt",
         "path": TOOL,
         "line": 794,
         "branch": ("fixture.refused and not fixture.reasons -> defect "
                    "'<id>: refused without a reason'"),
         "ablation": "validate-no-refusal-guard"},
    ],
    "ablation": {
        "method": ("each mutant is one exact single-occurrence edit of the freeze "
                   "copy; the copy's --selftest is run and its failing cases listed"),
        "results": ablation,
        "each_declared_case_sole_failure": all(
            v["failures"] == [k] for k, v in {
                "red-near-miss-unparsed": ablation["near-miss-re-dead"],
                "red-atom-absent": ablation["atom-absent-bound"],
                "red-validate-refused-no-reason":
                    ablation["validate-no-refusal-guard"]}.items()),
    },
    "cwd_independence": {
        "checked": True,
        "identical_output_from_scratch_cwd": (S / "freeze-selftest-cwdscratch.out")
            .read_bytes() == (S / "freeze-selftest.out").read_bytes(),
    },
    "landing_receipt": {
        "path": ".ufo/waves/round-79/pre/selftest-gate.txt",
        "byte_identical_to_freeze_selftest_output":
            (LANE / ".ufo/waves/round-79/pre/selftest-gate.txt").read_bytes()
            == (S / "freeze-selftest.out").read_bytes(),
    },
    "paths_present_at_base": {
        "judge_group_near_miss_branch": 394,
        "bind_clause_atom_absent_return": 311,
        "validate_receipt_refusal_guard": 794,
        "note": ("the three exercised branches exist at base at the same lines; "
                 "the round-79 delta is 25 added lines inside selftest() only "
                 "(+3 cases), so the instrument grew 949 -> 974 lines"),
        "instrument_lines_base": 949,
        "instrument_lines_freeze": 974,
    },
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "inventory.json").write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
print(json.dumps({k: receipt[k] for k in ("added", "removed", "count_delta",
                                          "added_matches_declared_claim",
                                          "base_is_prefix_of_freeze")}, indent=1))
print("base", receipt["base"]["cases"], receipt["base"]["failures"],
      receipt["base"]["names_digest"])
print("freeze", receipt["freeze"]["cases"], receipt["freeze"]["failures"],
      receipt["freeze"]["names_digest"])
print("sole-failure ablation:", receipt["ablation"]["each_declared_case_sole_failure"])
print("wrote", OUT / "inventory.json")
