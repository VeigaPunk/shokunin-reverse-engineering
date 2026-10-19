import hashlib
import json
import os
from pathlib import Path
import subprocess
from io import BytesIO
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "K8.vy"
ORIGINAL_SOURCE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy")
VYPER = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper")
VYPER_PYTHON = VYPER.parent / "python3"
REA_ROOT = Path("/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents")
REA = REA_ROOT / "scripts/rea.mjs"
FORMATS = (
    "bytecode",
    "bytecode_runtime",
    "blueprint_bytecode",
    "abi",
    "abi_python",
    "source_map",
    "source_map_runtime",
    "method_identifiers",
    "userdoc",
    "devdoc",
    "metadata",
    "combined_json",
    "layout",
    "ast",
    "annotated_ast",
    "cfg",
    "cfg_runtime",
    "interface",
    "external_interface",
    "solc_json",
    "integrity",
    "opcodes",
    "opcodes_runtime",
    "ir",
    "ir_json",
    "ir_runtime",
    "bb",
    "bb_runtime",
    "asm",
    "settings",
    "archive",
)
VARIANTS = {
    "noopt": ["--no-optimize"],
    "none": ["-O", "none"],
}
TMPDIR = Path(os.environ.get("TMPDIR", "/var/tmp/kaidoku-r9-ex10-tmp")).resolve()
OUT = ROOT / "compile"
PROBE = ROOT / "probe"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def run(args, env):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=90)


def main():
    TMPDIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    PROBE.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TMPDIR"] = str(TMPDIR)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = []
    results = {}
    for variant, flags in VARIANTS.items():
        for repetition in (1, 2):
            for fmt in FORMATS:
                args = [str(VYPER), *flags, "-f", fmt, str(SOURCE)]
                result = run(args, env)
                prefix = f"{variant}.{repetition}.{fmt}"
                write(OUT / f"{prefix}.stdout", result.stdout)
                write(OUT / f"{prefix}.stderr", result.stderr)
                commands.append(f"exit={result.returncode} {' '.join(args)}")
                results[prefix] = {
                    "exit": result.returncode,
                    "stdout_bytes": len(result.stdout),
                    "stdout_sha256": sha256(result.stdout),
                    "stderr_bytes": len(result.stderr),
                    "stderr_sha256": sha256(result.stderr),
                }
    def canonical_json(data):
        try:
            return json.dumps(json.loads(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

    def zip_payload(data):
        try:
            with zipfile.ZipFile(BytesIO(data)) as archive:
                contents = {info.filename: archive.read(info.filename) for info in archive.infolist()}
                times = {info.filename: info.date_time for info in archive.infolist()}
                return contents, times
        except zipfile.BadZipFile:
            return None, None

    comparisons = {}
    for fmt in FORMATS:
        n1 = results[f"noopt.1.{fmt}"]
        n2 = results[f"noopt.2.{fmt}"]
        z1 = results[f"none.1.{fmt}"]
        z2 = results[f"none.2.{fmt}"]
        n1_bytes = (OUT / f"noopt.1.{fmt}.stdout").read_bytes()
        n2_bytes = (OUT / f"noopt.2.{fmt}.stdout").read_bytes()
        z1_bytes = (OUT / f"none.1.{fmt}.stdout").read_bytes()
        z2_bytes = (OUT / f"none.2.{fmt}.stdout").read_bytes()
        n1_json = canonical_json(n1_bytes)
        n2_json = canonical_json(n2_bytes)
        z1_json = canonical_json(z1_bytes)
        z2_json = canonical_json(z2_bytes)
        n1_zip, n1_times = zip_payload(n1_bytes)
        n2_zip, n2_times = zip_payload(n2_bytes)
        z1_zip, z1_times = zip_payload(z1_bytes)
        z2_zip, z2_times = zip_payload(z2_bytes)
        if fmt == "archive" and n1_zip is not None and z1_zip is not None:
            repeat_equal = n1_zip == n2_zip and z1_zip == z2_zip
            cross_equal = n1_zip == z1_zip
            basis = "archive member payloads; ZIP timestamps excluded"
            archive_facts = {
                "noopt_member_sha256": {name: sha256(value) for name, value in sorted(n1_zip.items())},
                "none_member_sha256": {name: sha256(value) for name, value in sorted(z1_zip.items())},
                "noopt1_timestamps": n1_times,
                "noopt2_timestamps": n2_times,
                "none1_timestamps": z1_times,
                "none2_timestamps": z2_times,
            }
        elif n1_json is not None and z1_json is not None:
            repeat_equal = n1_json == n2_json and z1_json == z2_json
            cross_equal = n1_json == z1_json
            basis = "canonical JSON values"
            archive_facts = {}
        else:
            repeat_equal = n1_bytes == n2_bytes and z1_bytes == z2_bytes
            cross_equal = n1_bytes == z1_bytes
            basis = "raw stdout bytes"
            archive_facts = {}
        comparisons[fmt] = {
            "all_compile_calls_exit_zero": all(item["exit"] == 0 for item in (n1, n2, z1, z2)),
            "noopt_repeat_raw_equal": n1_bytes == n2_bytes,
            "none_repeat_raw_equal": z1_bytes == z2_bytes,
            "cross_flag_raw_equal": n1_bytes == z1_bytes,
            "repeat_content_equal": repeat_equal,
            "cross_flag_content_equal": cross_equal,
            "comparison_basis": basis,
            "noopt_sha256": n1["stdout_sha256"],
            "none_sha256": z1["stdout_sha256"],
            "stdout_bytes": n1["stdout_bytes"],
            **archive_facts,
        }
    probe_facts = {}
    for variant, flags in VARIANTS.items():
        runtime = (OUT / f"{variant}.1.bytecode_runtime.stdout").read_bytes()
        write(OUT / f"{variant}.runtime.hex", runtime)
        args = ["node", str(REA), "inspect-evm-interface", str(OUT / f"{variant}.runtime.hex"), "hex", "--format", "json", "--full-output"]
        result = run(args, env)
        write(PROBE / f"{variant}.json", result.stdout)
        write(PROBE / f"{variant}.stderr", result.stderr)
        commands.append(f"exit={result.returncode} {' '.join(args)}")
        data = json.loads(result.stdout)["data"]
        normalized = data["normalized_result"]
        functions = normalized["functions"]
        function_bytes = json.dumps(functions, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        facts = {
            "exit": result.returncode,
            "stdout_bytes": len(result.stdout),
            "stdout_sha256": sha256(result.stdout),
            "stderr_bytes": len(result.stderr),
            "stderr_sha256": sha256(result.stderr),
            "evidence_id": data["evidence_id"],
            "artifact_sha256": normalized["artifact"]["sha256"],
            "decoded_bytecode_sha256": normalized["bytecode"]["sha256"],
            "decoded_bytecode_bytes": normalized["bytecode"]["bytes"],
            "function_count": len(functions),
            "function_payload_sha256": sha256(function_bytes),
            "selectors": sorted(function["selector"] for function in functions),
            "confidence": data["confidence"],
            "authority": data["authority"],
            "discovery_completeness": normalized["discovery_completeness"],
            "runtime_execution": normalized["runtime_execution"],
        }
        probe_facts[variant] = facts
        results[f"probe.{variant}"] = facts
    probe_comparison = {
        "decoded_bytecode_sha256_equal": probe_facts["noopt"]["decoded_bytecode_sha256"] == probe_facts["none"]["decoded_bytecode_sha256"],
        "decoded_bytecode_bytes_equal": probe_facts["noopt"]["decoded_bytecode_bytes"] == probe_facts["none"]["decoded_bytecode_bytes"],
        "artifact_sha256_equal": probe_facts["noopt"]["artifact_sha256"] == probe_facts["none"]["artifact_sha256"],
        "function_payload_equal": probe_facts["noopt"]["function_payload_sha256"] == probe_facts["none"]["function_payload_sha256"],
        "evidence_ids_distinct": probe_facts["noopt"]["evidence_id"] != probe_facts["none"]["evidence_id"],
    }
    probe_summary = [
        f"decoded-bytecode-equal={probe_comparison['decoded_bytecode_sha256_equal']} bytes-equal={probe_comparison['decoded_bytecode_bytes_equal']} sha256={probe_facts['noopt']['decoded_bytecode_sha256']} bytes={probe_facts['noopt']['decoded_bytecode_bytes']}",
        f"artifact-input-equal={probe_comparison['artifact_sha256_equal']} sha256={probe_facts['noopt']['artifact_sha256']}",
        f"function-payload-equal={probe_comparison['function_payload_equal']} count={probe_facts['noopt']['function_count']} payload-sha256={probe_facts['noopt']['function_payload_sha256']}",
        f"selectors={','.join(probe_facts['noopt']['selectors'])}",
        f"noopt-evidence-id={probe_facts['noopt']['evidence_id']}",
        f"none-evidence-id={probe_facts['none']['evidence_id']}",
        f"evidence-ids-distinct={probe_comparison['evidence_ids_distinct']} (the request paths differ)",
        f"confidence={probe_facts['noopt']['confidence']} authority={probe_facts['noopt']['authority']} discovery-completeness={probe_facts['noopt']['discovery_completeness']} runtime-execution={probe_facts['noopt']['runtime_execution']}",
    ]
    (PROBE / "comparison.json").write_text(json.dumps(probe_comparison, indent=2, sort_keys=True) + "\n")
    (ROOT / "probe-summary.txt").write_text("\n".join(probe_summary) + "\n")
    if not all(probe_comparison.values()):
        raise SystemExit("REA result payload discrepancy detected")
    identity = []
    identity.append(f"source.original={ORIGINAL_SOURCE}")
    identity.append(f"source.copy={SOURCE}")
    original_bytes = ORIGINAL_SOURCE.read_bytes()
    source_bytes = SOURCE.read_bytes()
    identity.append(f"source.original_bytes={len(original_bytes)}")
    identity.append(f"source.copy_bytes={len(source_bytes)}")
    identity.append(f"source.original_sha256={sha256(original_bytes)}")
    identity.append(f"source.copy_sha256={sha256(source_bytes)}")
    identity.append(f"source_copy_matches_original={source_bytes == original_bytes}")
    version = run([str(VYPER), "--version"], env)
    identity.append(f"vyper.version={version.stdout.decode().strip()}")
    identity.append(f"vyper.wrapper={VYPER}")
    identity.append(f"vyper.wrapper_sha256={sha256(VYPER.read_bytes())}")
    python_identity = run(
        [str(VYPER_PYTHON), "-c", "import importlib.metadata,sys; print(importlib.metadata.version('vyper')); print(sys.version.replace('\\n',' '))"],
        env,
    )
    identity.append("vyper_python=" + python_identity.stdout.decode().replace("\n", " | ").strip())
    identity.append(f"rea.package={REA_ROOT}")
    identity.append(f"rea.version={json.loads((REA_ROOT / 'package.json').read_text())['version']}")
    identity.append(f"rea.package_json_sha256={sha256((REA_ROOT / 'package.json').read_bytes())}")
    identity.append(f"rea.cli_sha256={sha256(REA.read_bytes())}")
    identity.append(f"evmole.version={json.loads((REA_ROOT / 'package.json').read_text())['dependencies']['evmole']}")
    (ROOT / "identity.txt").write_text("\n".join(identity) + "\n")
    (ROOT / "commands.txt").write_text("\n".join(commands) + "\n")
    (OUT / "comparison.json").write_text(json.dumps(comparisons, indent=2, sort_keys=True) + "\n")
    (OUT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    lines = []
    lines.append(f"source-copy-equal={source_bytes == original_bytes} bytes={len(source_bytes)} sha256={sha256(source_bytes)}")
    lines.append(f"vyper-version={version.stdout.decode().strip()}")
    lines.append(f"formats-tested={len(FORMATS)} compile-calls={len(FORMATS) * len(VARIANTS) * 2}")
    for fmt, result in comparisons.items():
        lines.append(
            f"{fmt}: exits-zero={result['all_compile_calls_exit_zero']} "
            f"repeat-content-equal={result['repeat_content_equal']} "
            f"cross-flag-content-equal={result['cross_flag_content_equal']} "
            f"cross-flag-raw-equal={result['cross_flag_raw_equal']} "
            f"basis={result['comparison_basis']} bytes={result['stdout_bytes']} "
            f"noopt-sha256={result['noopt_sha256']} none-sha256={result['none_sha256']}"
        )
    for variant in VARIANTS:
        lines.append(f"rea-probe-{variant}: {json.dumps(results[f'probe.{variant}'], sort_keys=True)}")
    (ROOT / "measure.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not source_bytes == original_bytes:
        raise SystemExit("source copy differs from original")
    if any(
        not item["all_compile_calls_exit_zero"]
        or not item["repeat_content_equal"]
        or not item["cross_flag_content_equal"]
        for item in comparisons.values()
    ):
        raise SystemExit("compiler output content discrepancy detected")
    if any(results[f"probe.{variant}"]["exit"] != 0 for variant in VARIANTS):
        raise SystemExit("REA probe failed")


if __name__ == "__main__":
    main()
