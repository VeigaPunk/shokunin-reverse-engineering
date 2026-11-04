import json, pathlib, re, subprocess, sys
S = pathlib.Path("/fast/scratch/hyaku/kaidoku-r79/ExecCaseInventory")
src = (S / "attack-gate-freeze.py").read_text()
mutants = {
 "near-miss-re-dead": ('r"^(?:mismatch|survivor|atom|pristine|validate|match|matches)\\s+\\S+$"',
                       'r"^(?:mismatch|survivor|atom|pristine|validate|match|matches)\\s+ZZZ$"'),
 "atom-absent-bound": ('                return False, "defect", {"reason": "no_atoms", "field": field}',
                       '                return False, "bound", {"reason": "no_atoms", "field": field}'),
 "validate-no-refusal-guard": ('        if fixture.get("refused") and not fixture.get("reasons"):\n'
                               '            defects.append(f"{fixture.get(\'id\')}: refused without a reason")\n',
                               ''),
}
out = {}
for name, (old, new) in mutants.items():
    n = src.count(old)
    assert n == 1, (name, n)
    p = S / f"mut-{name}.py"
    p.write_text(src.replace(old, new))
    r = subprocess.run([sys.executable, str(p), "--selftest"], capture_output=True,
                       text=True, env={"PATH": "/usr/bin:/bin", "TMPDIR": str(S)})
    cases = [json.loads(l) for l in r.stdout.splitlines() if l.startswith('{"case"')]
    fails = [c["case"] for c in cases if not c["pass"]]
    summary = [l for l in r.stdout.splitlines() if l.startswith("SELFTEST")]
    out[name] = {"exit": r.returncode, "cases": len(cases), "failures": fails,
                 "summary": summary[0] if summary else None,
                 "stderr": r.stderr.strip()[:200]}
print(json.dumps(out, indent=1, sort_keys=True))
