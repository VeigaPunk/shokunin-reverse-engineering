#!/usr/bin/env python3
"""Isolated text/JSON binding detector; never invokes the ELF reader or measures ELF."""
import argparse
import ast
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
FREEZE = "54a87a51a865ab931fd355e767303337b05cccf4"
COUNTER_REL = "tools/round-34/version-needs-counter.py"
CLAIMS_REL = ".ufo/waves/round-34/claims.json"
ACTIVE = HERE / "private-counter.py"
DATA = b"isolated benign document-binding fixture\n"
MAX_FILE = 1048576

def sha(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def put(path, data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    if len(data) > MAX_FILE or HERE not in path.resolve().parents:
        raise RuntimeError("fixture write outside size/scope bound")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    path.chmod(0o644)

def dump(path, value):
    put(path, json.dumps(value, indent=2, sort_keys=True) + "\n")

def bounded():
    resource.setrlimit(resource.RLIMIT_AS, (536870912, 536870912))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8388608, 8388608))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    _, hard = resource.getrlimit(resource.RLIMIT_NPROC)
    process_cap = 8192 if hard == resource.RLIM_INFINITY else min(8192, hard)
    resource.setrlimit(resource.RLIMIT_NPROC, (process_cap, process_cap))

def env():
    result = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and not k.startswith("PYTHON")}
    result.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "LC_ALL": "C"})
    return result

def run(argv, timeout):
    start = utc()
    done = subprocess.run(argv, cwd=ROOT, env=env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if len(done.stdout) + len(done.stderr) > MAX_FILE:
        raise RuntimeError("subprocess receipt exceeds output bound")
    return {"argv": argv, "cwd": str(ROOT), "started_utc": start, "ended_utc": utc(), "exit": done.returncode, "stdout": done.stdout.decode("utf-8"), "stderr": done.stderr.decode("utf-8")}

def prepare():
    if ACTIVE.exists():
        raise RuntimeError("private counter already exists; refusing to overwrite evidence")
    revision = run(["git", "--no-replace-objects", "-c", "core.fsmonitor=false", "-C", str(ROOT), "rev-parse", "HEAD", FREEZE + "^{commit}"], 20)
    if revision["exit"] != 0 or revision["stdout"].splitlines() != [FREEZE, FREEZE]:
        dump(HERE / "revision-error.json", revision)
        raise RuntimeError("sandbox HEAD is not the assigned freeze")
    claims_bytes = (ROOT / CLAIMS_REL).read_bytes()
    contract = json.loads(claims_bytes)
    original = (ROOT / COUNTER_REL).read_bytes()
    if sha(original) != contract["instruments"][COUNTER_REL]:
        raise RuntimeError("sandbox counter differs from frozen reviewed digest")
    put(ACTIVE, original)
    put(HERE / "private-counter.pristine.py", original)
    put(HERE / "frozen" / CLAIMS_REL, claims_bytes)
    paths = set(contract["documents"]) | set(contract["sources"]) | {contract["skill_section"]["approved"]}
    pins = dict(contract["documents"])
    pins.update(contract["sources"])
    inventory = {}
    for path in sorted(paths):
        data = (ROOT / path).read_bytes()
        if path in pins and sha(data) != pins[path]:
            raise RuntimeError("frozen source/document pin mismatch:" + path)
        put(HERE / "frozen" / path, data)
        inventory[path] = {"size": len(data), "sha256": sha(data)}
    approved = (HERE / "frozen" / contract["skill_section"]["approved"]).read_text()
    heading = contract["skill_section"]["heading"]
    skill = "# Isolated source/document binding fixture\n\n" + approved.strip() + "\n\n## Following section\n\nUnrelated fixture text.\n"
    registry = "# Isolated source registry fixture\n\n" + "\n".join(contract["source_rows"].values()) + "\n"
    put(HERE / "canonical" / "SKILL.md", skill)
    put(HERE / "canonical" / "corpus/SOURCES.md", registry)
    knowledge = next(path for path in contract["documents"] if path.startswith("corpus/knowledge/"))
    knowledge_text = (HERE / "frozen" / knowledge).read_text()
    denied = knowledge_text.replace("`vna_other` is the version identifier", "`vna_other` is not the version identifier", 1)
    if denied == knowledge_text:
        raise RuntimeError("denial anchor not found")
    source_id = "S103"
    old_url = "https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html"
    wrong_registry = registry.replace(old_url, "https://example.invalid/off-topic-source", 1)
    if wrong_registry == registry:
        raise RuntimeError("source URL anchor not found")
    source_path = next(path for path in contract["sources"] if path.endswith("lsb-symversion.html"))
    source_text = (HERE / "frozen" / source_path).read_text()
    quote = source_text.splitlines()[936].removeprefix(">").removesuffix("</P")
    if not quote.startswith("Object file version identifier used in the .gnu.version"):
        raise RuntimeError("source quote anchor not found")
    off_topic = "<!doctype html>\n<title>Garden watering calendar</title>\n<h1>Tomato watering schedule</h1>\n<p>This page concerns gardening, not ELF structures.</p>\n<blockquote>" + quote + "</blockquote>\n"
    bag = heading + "\n\n" + " ".join(sorted(approved.splitlines()[2:][0].split() + "\n".join(approved.splitlines()[3:]).split())) + "\n"
    cases = [
        {"name": "green-canonical", "expected_documents_ok": True, "overrides": {}, "expected_failed_paths": []},
        {"name": "red-duplicate-heading", "expected_documents_ok": False, "overrides": {"SKILL.md": skill + "\n" + approved.strip() + "\n"}, "expected_failed_paths": ["SKILL.md#" + heading]},
        {"name": "red-denial", "expected_documents_ok": False, "overrides": {knowledge: denied}, "expected_failed_paths": [knowledge]},
        {"name": "red-word-bag", "expected_documents_ok": False, "overrides": {"SKILL.md": "# Isolated fixture\n\n" + bag + "\n## Following section\n"}, "expected_failed_paths": ["SKILL.md#" + heading]},
        {"name": "red-wrong-source", "expected_documents_ok": False, "overrides": {"corpus/SOURCES.md": wrong_registry}, "expected_failed_paths": ["corpus/SOURCES.md#" + source_id]},
        {"name": "red-off-topic-same-quote", "expected_documents_ok": False, "overrides": {source_path: off_topic}, "expected_failed_paths": [source_path]},
    ]
    for case in cases:
        for path, text in case.pop("overrides").items():
            put(HERE / "cases" / case["name"] / path, text)
    dump(HERE / "cases.json", cases)
    put(HERE / "source-quote.txt", quote + "\n")
    put(HERE / "text-input.txt", DATA)
    reader = "from pathlib import Path\nimport sys\nif Path(sys.argv[1]).read_bytes() != " + repr(DATA) + ":\n    raise SystemExit(3)\nprint('{\"schema\":1,\"needed\":[]}')\n"
    put(HERE / "fake-text-reader.py", reader)
    dump(HERE / "preparation.json", {"observed_utc": utc(), "revision_receipt": revision, "measured_revision": FREEZE, "counter_sha256": sha(original), "predicate": contract["predicate"], "frozen_inventory": inventory, "source_quote": quote, "scope": "isolated text/JSON only; no production parser/data/score", "axes": ["unique exact section binding", "complete affirmative document bytes", "exact source identity and capture bytes", "false-accept sensitivity", "bounded reversible isolation"], "model_visible_in_session": "openai-codex/gpt-6.1-sol", "tools_installed_or_updated": []})
    print(json.dumps({"prepared": True, "counter_sha256": sha(original), "cases": len(cases), "revision": FREEZE}, sort_keys=True))
    return 0

def binding_function(module):
    source = ACTIVE.read_text()
    tree = ast.parse(source, filename=str(ACTIVE))
    measure = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "measure")
    start = next(i for i, node in enumerate(measure.body) if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "docs" for t in node.targets))
    end = next(i for i in range(start + 1, len(measure.body)) if isinstance(measure.body[i], ast.Try) and any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "reader" for t in n.targets) for n in measure.body[i].body))
    body = measure.body[start:end]
    segment = "\n".join(source.splitlines()[body[0].lineno - 1:body[-1].end_lineno]) + "\n"
    fn = ast.FunctionDef(name="bind_documents", args=ast.arguments(posonlyargs=[], args=[ast.arg(arg=name) for name in ("root", "rev", "frozen", "contract")], kwonlyargs=[], kw_defaults=[], defaults=[]), body=body + [ast.Return(value=ast.Name(id="docs", ctx=ast.Load()))], decorator_list=[])
    isolated = ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[]))
    namespace = dict(vars(module))
    exec(compile(isolated, str(ACTIVE) + "#measure-document-block", "exec"), namespace)
    return namespace, segment, (body[0].lineno, body[-1].end_lineno)

def detect(phase):
    if phase not in {"pristine", "mutated", "restored"}:
        raise RuntimeError("unknown phase")
    out = HERE / "receipts" / phase
    if out.exists():
        raise RuntimeError("phase already recorded; refusing to overwrite")
    counter = ACTIVE.read_bytes()
    put(out / "private-counter.py", counter)
    spec = importlib.util.spec_from_file_location("private_counter", ACTIVE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    namespace, segment, lines = binding_function(module)
    put(out / "document-binding-block.py.txt", segment)
    contract = module.decode((HERE / "frozen" / CLAIMS_REL).read_bytes())
    cases = json.loads((HERE / "cases.json").read_text())
    records = []
    for case in cases:
        name = case["name"]
        accesses = []
        def fixture_blob(root, rev, path):
            module.safe_path(path)
            if rev == "fixture-frozen":
                candidate = HERE / "frozen" / path
            elif rev == "fixture-measured":
                override = HERE / "cases" / name / path
                canonical = HERE / "canonical" / path
                candidate = override if override.exists() else canonical if canonical.exists() else HERE / "frozen" / path
            else:
                raise module.Unevaluable("non-fixture revision denied")
            data = candidate.read_bytes()
            accesses.append({"fixture_revision": rev, "logical_path": path, "fixture_path": str(candidate.relative_to(HERE)), "size": len(data), "sha256": sha(data)})
            return data
        namespace["blob"] = fixture_blob
        documents = namespace["bind_documents"](ROOT, "fixture-measured", "fixture-frozen", contract)
        documents_ok = all(row["ok"] for row in documents)
        failed = sorted(row["path"] for row in documents if not row["ok"])
        fixture = {"target": 1, "documents_ok": documents_ok, "manifest": {"schema": 1, "carriers": [{"id": "text-doc-binding", "path": "text-input.txt", "size": len(DATA), "sha256": sha(DATA), "expected": {"schema": 1, "needed": []}}]}}
        case_out = out / name
        put(case_out / "text-input.txt", DATA)
        dump(case_out / "spec.json", fixture)
        argv = [sys.executable, "-I", "-B", str(ACTIVE), "--fixture-spec", str(case_out / "spec.json"), "--fixture-reader", str(HERE / "fake-text-reader.py")]
        receipt = run(argv, 15)
        dump(case_out / "command.json", receipt)
        observed = module.decode(receipt["stdout"])
        expected_ok = case["expected_documents_ok"]
        expected_exit = 0 if expected_ok else 1
        expected_finding = "version_needs_match" if expected_ok else "document_mismatch"
        ok = documents_ok == expected_ok and failed == sorted(case["expected_failed_paths"]) and receipt["exit"] == expected_exit and observed.get("finding") == expected_finding and observed.get("met_target") is expected_ok and observed.get("matched") == 1 and observed.get("target") == 1 and observed.get("documents_ok") is documents_ok and all(attempt["matched"] for row in observed.get("rows", []) for attempt in row["attempts"])
        record = {"case": name, "expected_documents_ok": expected_ok, "documents_ok": documents_ok, "expected_failed_paths": sorted(case["expected_failed_paths"]), "failed_paths": failed, "documents": documents, "blob_accesses": accesses, "exit": receipt["exit"], "finding": observed.get("finding"), "matched": observed.get("matched"), "target": observed.get("target"), "met_target": observed.get("met_target"), "detector_ok": ok}
        dump(case_out / "binding.json", record)
        records.append(record)
    result = {"phase": phase, "observed_utc": utc(), "counter_sha256": sha(counter), "sandbox_source_counter_sha256": sha((ROOT / COUNTER_REL).read_bytes()), "measured_revision": FREEZE, "predicate_preserved_verbatim": contract["predicate"] == module.PREDICATE, "predicate": contract["predicate"], "binding_source_lines": lines, "binding_source_sha256": sha(segment.encode()), "interfaces_exercised": ["private frozen counter section(text,title)", "unchanged measure() documents/source rows/source pins AST block with file-backed blob shim", "outer counter CLI --fixture-spec --fixture-reader", "fixture_measure -> validate_manifest -> score -> two fake TEXT reader schedules"], "interfaces_not_exercised": ["production measure CLI --root/--rev/--freeze", "Git blob lookup as a binding transport", "instrument/manifest pin gates in measure()", "production parser", "production carriers", "production score", "semantic source authority adjudication"], "cases": records, "passed": sum(r["detector_ok"] for r in records), "total": len(records)}
    dump(out / "result.json", result)
    print(json.dumps({"phase": phase, "counter_sha256": result["counter_sha256"], "passed": result["passed"], "total": result["total"], "cases": [{k: row[k] for k in ("case", "documents_ok", "exit", "finding", "detector_ok")} for row in records]}, sort_keys=True))
    return 0 if result["passed"] == result["total"] else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "pristine", "mutated", "restored"])
    args = parser.parse_args()
    bounded()
    raise SystemExit(prepare() if args.mode == "prepare" else detect(args.mode))
