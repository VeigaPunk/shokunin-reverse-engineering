#!/usr/bin/env python3
"""Measure REA CLI command mentions and retained C2 evidence at a Git revision.

Knowledge entries are regular files tracked below ``corpus/knowledge/`` at the
selected commit. A command is mentioned when its hyphenated name or complete
underscore form occurs at an ASCII token boundary. Entry counts count files,
not repeated mentions. A target is exercised only if one naming entry contains
an ``ev_<64 hex>`` ID and names a C2 evidence path that exists at that commit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_PACKAGE_VERSION = "6.5.0"
DEFAULT_PACKAGE_DIR = Path(
    "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
)
DEFAULT_TARGETS = (
    "inspect-wasm-artifact",
    "compare-wasm-interfaces",
    "execute-rizin-command",
    "list-objdump-architectures",
    "project-harmony-application-graph",
)
KNOWLEDGE_PREFIX = "corpus/knowledge/"
EVIDENCE_PREFIX = ".ufo/waves/round-20/evidence/c2/"
HEX64 = re.compile(r"(?<![A-Za-z0-9_])ev_[0-9a-fA-F]{64}(?![A-Za-z0-9_])", re.ASCII)
PROBE = """const m = await import(process.argv[1]);
if (!Array.isArray(m.CLI_COMMAND_NAMES)) throw new Error('CLI_COMMAND_NAMES is not an array');
console.log(JSON.stringify(m.CLI_COMMAND_NAMES));"""


class Refusal(Exception):
    """Unusable input; exit 2 with the cause named."""


def run_process(argv, *, cwd=None, timeout=120, input_bytes=None):
    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Refusal(f"command_failed {argv[0]}: {exc}") from exc
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise Refusal(f"command_failed {argv[0]} exit={result.returncode}: {detail}")
    return result.stdout


def git(root, *args):
    return run_process(["git", "--no-optional-locks", *args], cwd=root)


def resolve_revision(root, revision):
    raw = git(root, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    resolved = raw.decode("ascii", "strict").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", resolved):
        raise Refusal("invalid_resolved_revision")
    return resolved


def tree_entries(root, revision):
    raw = git(root, "ls-tree", "-r", "-z", "--full-tree", revision)
    result = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, path_bytes = record.split(b"\t", 1)
            mode, object_type, object_id = metadata.decode("ascii").split(" ")
            path = path_bytes.decode("utf-8", "strict")
        except (UnicodeDecodeError, ValueError) as exc:
            raise Refusal("malformed_git_tree_entry") from exc
        if object_type == "blob" and mode in ("100644", "100755"):
            result.append((path, object_id))
    return result


def git_show(root, revision, path):
    raw = git(root, "show", f"{revision}:{path}")
    return raw.decode("utf-8", "replace")


def command_pattern(name):
    forms = sorted({name, name.replace("-", "_")}, key=len, reverse=True)
    alternatives = "|".join(re.escape(form) for form in forms)
    return re.compile(
        rf"(?<![a-z0-9_-])(?:{alternatives})(?![a-z0-9_-])",
        re.IGNORECASE | re.ASCII,
    )


def existing_evidence_path(text, paths):
    for path in paths:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9._/-]){re.escape(path)}(?![A-Za-z0-9_/-]|\.[A-Za-z0-9_-])",
            re.ASCII,
        )
        if pattern.search(text):
            return True
    return False


def load_cli_commands(package_dir):
    package_dir = Path(package_dir).expanduser().resolve()
    if not package_dir.is_dir():
        raise Refusal(f"package_dir_not_found {package_dir}")
    package_json = package_dir / "package.json"
    try:
        package = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"package_metadata_unreadable {package_json}: {exc}") from exc
    version = package.get("version") if isinstance(package, dict) else None
    if version != EXPECTED_PACKAGE_VERSION:
        raise Refusal(f"package_version_mismatch expected={EXPECTED_PACKAGE_VERSION} observed={version!r}")
    module = (package_dir / "dist" / "cliCommandNames.js").resolve()
    if not module.is_file():
        raise Refusal(f"cli_command_module_not_found {module}")
    try:
        module_uri = module.as_uri()
    except ValueError as exc:
        raise Refusal(f"cli_command_module_invalid {module}") from exc
    output = run_process(
        ["node", "--input-type=module", "-e", PROBE, module_uri], timeout=60
    )
    try:
        names = json.loads(output.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal("cli_command_probe_invalid_json") from exc
    if not isinstance(names, list) or any(not isinstance(name, str) or not name for name in names):
        raise Refusal("cli_command_catalog_invalid")
    if len(names) != len(set(names)):
        raise Refusal("cli_command_catalog_duplicate_names")
    return version, names


def measure(root, revision, commands, targets=DEFAULT_TARGETS):
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise Refusal(f"root_not_found {root}")
    resolved_rev = resolve_revision(root, revision)
    tree = tree_entries(root, resolved_rev)
    paths = {path for path, _ in tree}
    knowledge = [path for path, _ in tree if path.startswith(KNOWLEDGE_PREFIX)]
    evidence_paths = sorted(path for path in paths if path.startswith(EVIDENCE_PREFIX))
    patterns = {name: command_pattern(name) for name in commands}
    per_command = {name: 0 for name in commands}
    target_entries = {name: [] for name in targets}

    for path in knowledge:
        text = git_show(root, resolved_rev, path)
        for name, pattern in patterns.items():
            if pattern.search(text):
                per_command[name] += 1
                if name in target_entries:
                    target_entries[name].append(text)

    mentioned = [name for name in commands if per_command[name] > 0]
    zero = [name for name in commands if per_command[name] == 0]
    target_results = {}
    for name in targets:
        exercised = any(
            HEX64.search(text) and existing_evidence_path(text, evidence_paths)
            for text in target_entries[name]
        )
        target_results[name] = {
            "entries": len(target_entries[name]),
            "exercised": exercised,
        }
    return {
        "rev": resolved_rev,
        "package_version": EXPECTED_PACKAGE_VERSION,
        "cli_commands": commands,
        "mentioned": mentioned,
        "zero": zero,
        "per_command": per_command,
        "targets": target_results,
    }


def write_fixture_file(root, relpath, content):
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def selftest():
    scratch = Path(tempfile.mkdtemp(prefix="verb-coverage-selftest-"))
    cases = []
    try:
        root = scratch / "fixture-repo"
        root.mkdir()
        run_process(["git", "init", "-q", str(root)])
        evidence_path = EVIDENCE_PREFIX + "wasm/run.json"
        ev_id = "ev_" + "a" * 64
        write_fixture_file(root, "corpus/knowledge/hyphen.md",
                           f"Ran inspect-wasm-artifact; retained {ev_id} at {evidence_path}.\n")
        write_fixture_file(root, "corpus/knowledge/underscore.md",
                           "compare_wasm_interfaces naming entry.\n")
        write_fixture_file(root, "corpus/knowledge/no-target.md", "No command names in this entry.\n")
        write_fixture_file(root, "corpus/knowledge/substring-trap.md",
                           "inspect-artifact-x must not count.\n")
        write_fixture_file(root, "corpus/knowledge/evidence-id-only.md",
                           f"execute-rizin-command {ev_id}.\n")
        write_fixture_file(root, "corpus/knowledge/evidence-path-only.md",
                           f"execute-rizin-command {evidence_path}.\n")
        write_fixture_file(root, "corpus/knowledge/missing-evidence-path.md",
                           f"project_harmony_application_graph {ev_id} at {EVIDENCE_PREFIX}missing.json.\n")
        write_fixture_file(root, evidence_path, '{"retained":true}\n')
        run_process(["git", "-C", str(root), "add", "--all"])
        run_process([
            "git", "-C", str(root), "-c", "user.name=verb-coverage-selftest",
            "-c", "user.email=verb-coverage-selftest@invalid", "commit", "-q", "-m", "fixture",
        ])
        revision = git(root, "rev-parse", "HEAD").decode("ascii").strip()
        commands = [
            "inspect-wasm-artifact",
            "compare-wasm-interfaces",
            "inspect-artifact",
            "execute-rizin-command",
            "project-harmony-application-graph",
        ]
        result = measure(root, revision, commands)
        cases.extend([
            ("hyphen_name_counts_entry", result["per_command"]["inspect-wasm-artifact"] == 1),
            ("underscore_form_counts_entry", result["per_command"]["compare-wasm-interfaces"] == 1),
            ("not_mentioned_is_zero", "inspect-artifact" in result["zero"]),
            ("substring_trap_rejected", result["per_command"]["inspect-artifact"] == 0),
            ("evidence_id_and_existing_path_exercise",
             result["targets"]["inspect-wasm-artifact"]["exercised"] is True),
            ("id_and_path_must_share_entry",
             result["targets"]["execute-rizin-command"]["exercised"] is False),
            ("evidence_path_must_exist",
             result["targets"]["project-harmony-application-graph"]["exercised"] is False),
        ])
        failed = [name for name, passed in cases if not passed]
        if failed:
            print(
                f"SELFTEST: FAILED {','.join(failed)} cases={len(cases)} fails={len(failed)}",
                file=sys.stderr,
            )
            return 1
        print(f"SELFTEST: CLEAN cases={len(cases)}")
        return 0
    except (Refusal, OSError, subprocess.SubprocessError) as exc:
        failed = [name for name, passed in cases if not passed]
        label = ",".join(failed) if failed else "fixture_setup"
        print(f"SELFTEST: FAILED {label} ({exc}) cases={len(cases)} fails=1", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="lane repository path")
    parser.add_argument("--rev", help="commit or revision to measure")
    parser.add_argument("--package-dir", default=str(DEFAULT_PACKAGE_DIR),
                        help="rea-agents@6.5.0 package directory")
    parser.add_argument("--selftest", action="store_true", help="run hermetic fixture cases")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root:
        print("refusal: missing_required_argument --root", file=sys.stderr)
        return 2
    if not args.rev:
        print("refusal: missing_required_argument --rev", file=sys.stderr)
        return 2
    try:
        version, commands = load_cli_commands(args.package_dir)
        result = measure(args.root, args.rev, commands)
        result["package_version"] = version
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return 0
    except Refusal as exc:
        print(f"refusal: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
