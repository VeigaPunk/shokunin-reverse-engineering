#!/usr/bin/env python3
"""Recompute REA catalog identities from an installed ``rea-agents`` package.

Method (recorded in this lane, round-18 wave ``arc2-loop1-round2``):

  node --input-type=module -e <PROBE> <package-dir>

The probe imports the package's own compiled modules and prints:

  * ``CATALOG_IDENTITY.counts``   -- cli_commands = CLI_COMMAND_NAMES.length,
                                     mcp_tools = sortedToolContracts.length;
  * ``createCatalogDigests()``    -- tools_sha256 over the default full-schema catalog;
  * ``CATALOG_IDENTITY.digests``  -- 6.7.0 serves its build-time recorded constant;
  * independent counts            -- CLI_COMMAND_NAMES / TOOL_CONTRACTS / PROMPT_CONTRACTS lengths.

Anchors: ``.ufo/waves/arc2-loop1-round2/R3.md:166`` (the exact node argv),
``.ufo/waves/arc2-loop1-round2/E14.md`` section 2.5 (createCatalogDigests reproduces the
live digests; source ``dist/catalogIdentity.js:51-66``), and ``dist/recordedCatalogDigests.js``
(present in 6.7.0 only, served by ``dist/catalogIdentity.js:71-75``).

``node scripts/rea.mjs --version`` is also read (read-only) and must agree with the
``package.json`` version; a disagreement is a finding, not a refusal.

Every count printed carries its rule; every refusal names its cause.
Exit 0 clean, 1 findings under ``--strict``, 2 unusable input/refusal.
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

DEFAULT_VERSIONS = ("6.7.0", "6.5.0")
FIELDS = ("version", "npx_cache_dir", "cli_commands", "mcp_tools", "tools_sha256", "method_argv")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PROBE_TIMEOUT = 180

RULES = (
    "rule: cli_commands = CATALOG_IDENTITY.counts.cli_commands = CLI_COMMAND_NAMES.length",
    "rule: mcp_tools = CATALOG_IDENTITY.counts.mcp_tools = sortedToolContracts.length",
    "rule: tools_sha256 = createCatalogDigests().tools_sha256 over the default full-schema catalog",
)

# process.argv[1] is the package directory passed after the -e script.
PROBE = """const d = process.argv[1];
const m = await import("file://" + d + "/dist/catalogIdentity.js");
const cli = await import("file://" + d + "/dist/cliCommandNames.js");
const tc = await import("file://" + d + "/dist/contracts/toolContracts.js");
const pc = await import("file://" + d + "/dist/contracts/promptContracts.js");
console.log(JSON.stringify({
  counts: m.CATALOG_IDENTITY.counts,
  recomputed: m.createCatalogDigests(),
  identity: m.CATALOG_IDENTITY.digests,
  independent: {
    cli_commands: cli.CLI_COMMAND_NAMES.length,
    mcp_tools: tc.TOOL_CONTRACTS.length,
    mcp_prompts: pc.PROMPT_CONTRACTS.length
  }
}));"""


class Refusal(Exception):
    """Unusable input; exit 2 with the cause named."""


def find_caches(npx_root):
    """Map version -> sorted list of resolved ``_npx/<hash>`` cache directories."""
    root = Path(npx_root).expanduser()
    if not root.is_dir():
        raise Refusal(f"npx root is not a directory: {root}")
    found = {}
    for entry in sorted(root.iterdir(), key=lambda path: path.name):
        manifest = entry / "node_modules" / "rea-agents" / "package.json"
        if not manifest.is_file():
            continue
        try:
            version = json.loads(manifest.read_text(encoding="utf-8"))["version"]
        except (OSError, ValueError, KeyError) as exc:
            raise Refusal(f"unreadable rea-agents manifest {manifest}: {exc}")
        if not isinstance(version, str) or not version:
            raise Refusal(f"rea-agents manifest without a string version: {manifest}")
        found.setdefault(version, []).append(entry.resolve())
    return found


def resolve_cache(found, version):
    caches = found.get(version, [])
    if not caches:
        installed = ", ".join(sorted(found)) or "none"
        raise Refusal(f"rea-agents@{version} not installed under the npx root (installed: {installed})")
    if len(caches) > 1:
        raise Refusal(
            f"rea-agents@{version} has {len(caches)} cache installs: "
            + ", ".join(str(cache) for cache in caches)
        )
    return caches[0]


def run_probe(cache_dir):
    package_dir = cache_dir / "node_modules" / "rea-agents"
    argv = ["node", "--input-type=module", "-e", PROBE, str(package_dir)]
    try:
        done = subprocess.run(argv, capture_output=True, text=True, timeout=PROBE_TIMEOUT)
    except FileNotFoundError:
        raise Refusal("node is not on PATH")
    except subprocess.TimeoutExpired:
        raise Refusal(f"node probe timed out after {PROBE_TIMEOUT}s for {package_dir}")
    if done.returncode != 0:
        tail = (done.stderr or done.stdout).strip().splitlines()
        raise Refusal(
            f"node probe exited {done.returncode} for {package_dir}: "
            f"{tail[-1] if tail else '<no output>'}"
        )
    lines = [line for line in done.stdout.splitlines() if line.strip()]
    if not lines:
        raise Refusal(f"node probe produced no JSON for {package_dir}")
    try:
        payload = json.loads(lines[-1])
    except ValueError as exc:
        raise Refusal(f"node probe JSON is unparseable for {package_dir}: {exc}")
    if not isinstance(payload, dict):
        raise Refusal(f"node probe JSON is not an object for {package_dir}")
    return argv, payload


def run_cli_version(cache_dir, version):
    """Read-only version corroboration; returns None when the shim is absent."""
    shim = cache_dir / "node_modules" / "rea-agents" / "scripts" / "rea.mjs"
    if not shim.is_file():
        return None
    try:
        done = subprocess.run(
            ["node", str(shim), "--version"], capture_output=True, text=True, timeout=PROBE_TIMEOUT
        )
    except FileNotFoundError:
        raise Refusal("node is not on PATH")
    except subprocess.TimeoutExpired:
        raise Refusal(f"rea --version timed out after {PROBE_TIMEOUT}s for {cache_dir}")
    lines = [line.strip() for line in done.stdout.splitlines() if line.strip()]
    if done.returncode != 0 or not lines:
        tail = (done.stderr or done.stdout).strip().splitlines()
        raise Refusal(
            f"rea --version exited {done.returncode} for rea-agents@{version}: "
            f"{tail[-1] if tail else '<no output>'}"
        )
    return lines[-1]


def collect(npx_root, versions):
    found = find_caches(npx_root)
    entries = []
    for version in versions:
        cache_dir = resolve_cache(found, version)
        argv, payload = run_probe(cache_dir)
        counts = payload.get("counts")
        if not isinstance(counts, dict):
            raise Refusal(f"probe payload lacks counts for rea-agents@{version}")
        for key in ("cli_commands", "mcp_tools"):
            if not isinstance(counts.get(key), int):
                raise Refusal(f"probe counts.{key} is not an integer for rea-agents@{version}")
        record = {
            "version": version,
            "npx_cache_dir": str(cache_dir),
            "cli_commands": counts["cli_commands"],
            "mcp_tools": counts["mcp_tools"],
            "tools_sha256": (payload.get("recomputed") or {}).get("tools_sha256"),
            "method_argv": argv,
        }
        entries.append((record, payload, run_cli_version(cache_dir, version)))
    return entries


def evaluate(entries):
    """Return (findings, notes); both are deterministic lists of strings."""
    findings = []
    notes = []
    for record, payload, cli_version in entries:
        version = record["version"]
        counts = payload.get("counts") or {}
        recomputed = payload.get("recomputed") or {}
        identity = payload.get("identity") or {}
        independent = payload.get("independent")
        digest = record["tools_sha256"]
        if not isinstance(digest, str) or not HEX64.match(digest):
            findings.append(f"{version}: tools_sha256 is not 64 lowercase hex: {digest!r}")
        if identity.get("tools_sha256") != recomputed.get("tools_sha256"):
            findings.append(
                f"{version}: CATALOG_IDENTITY.digests.tools_sha256 {identity.get('tools_sha256')} "
                f"!= createCatalogDigests().tools_sha256 {recomputed.get('tools_sha256')}"
            )
        if not isinstance(independent, dict):
            notes.append(f"{version}: independent count cross-check unavailable")
        else:
            for key in ("cli_commands", "mcp_tools", "mcp_prompts"):
                if independent.get(key) != counts.get(key):
                    findings.append(
                        f"{version}: counts.{key}={counts.get(key)} "
                        f"!= independent {key}={independent.get(key)}"
                    )
        if cli_version is None:
            notes.append(f"{version}: scripts/rea.mjs absent; version corroboration skipped")
        elif cli_version != version:
            findings.append(f"{version}: package.json version != rea --version {cli_version}")
    return findings, notes


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="rea-catalog.py",
        description="Recompute REA catalog counts and tools_sha256 from installed npx caches.",
    )
    parser.add_argument("--npx-root", default=str(Path.home() / ".npm" / "_npx"),
                        help="npx cache root (default: ~/.npm/_npx)")
    parser.add_argument("--version", action="append", dest="versions", metavar="VERSION",
                        help="rea-agents version to probe; repeatable (default: %s)" % " ".join(DEFAULT_VERSIONS))
    parser.add_argument("--out", help="write the JSON records here instead of stdout only")
    parser.add_argument("--strict", action="store_true", help="exit 1 when any finding is raised")
    parser.add_argument("--selftest", action="store_true", help="run hermetic fixture cases and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    versions = args.versions or list(DEFAULT_VERSIONS)
    try:
        entries = collect(args.npx_root, versions)
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    findings, notes = evaluate(entries)
    for note in notes:
        print(f"NOTE: {note}", file=sys.stderr)
    for finding in findings:
        print(f"FINDING: {finding}", file=sys.stderr)
    for rule in RULES:
        print(rule, file=sys.stderr)
    for record, _, cli_version in entries:
        print(
            f"{record['version']}: cli_commands={record['cli_commands']} "
            f"mcp_tools={record['mcp_tools']} tools_sha256={record['tools_sha256']} "
            f"cache={record['npx_cache_dir']} rea --version={cli_version}",
            file=sys.stderr,
        )

    text = json.dumps([record for record, _, _ in entries], indent=2) + "\n"
    sys.stdout.write(text)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(prefix=".rea-catalog-", suffix=".tmp",
                                     dir=str(out_path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp_path, out_path)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        print(f"WROTE: {out_path}", file=sys.stderr)

    return 1 if (args.strict and findings) else 0


def selftest():
    """Hermetic fixture cases; node runs against stub packages, no network."""
    trials = 0
    failures = []

    def check(name, body):
        nonlocal trials
        trials += 1
        root = Path(tempfile.mkdtemp(prefix="rea-catalog-selftest-"))
        try:
            body(root)
        except AssertionError as exc:
            failures.append(f"{name}: {exc}")
        except Exception as exc:  # a harness fault must not look clean
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def clean(root):
        make_fixture(root, "cacheone", "9.9.9")
        done = run_tool(["--npx-root", str(root), "--version", "9.9.9", "--strict"])
        assert done.returncode == 0, f"exit {done.returncode}: {done.stderr.strip()}"
        records = json.loads(done.stdout)
        assert isinstance(records, list) and len(records) == 1, f"records={records!r}"
        record = records[0]
        assert tuple(record) == FIELDS, f"field order/keys={tuple(record)}"
        assert record["version"] == "9.9.9", record["version"]
        assert record["npx_cache_dir"] == str((root / "cacheone").resolve()), record["npx_cache_dir"]
        assert (record["cli_commands"], record["mcp_tools"]) == (3, 4), record
        assert record["tools_sha256"] == DIGEST_A, record["tools_sha256"]
        assert record["method_argv"][0] == "node" and "--input-type=module" in record["method_argv"]
        assert "rule: cli_commands" in done.stderr, done.stderr
        assert "tools_sha256=" + DIGEST_A in done.stderr, done.stderr

    def digest_mismatch(root):
        make_fixture(root, "cacheone", "9.9.9", identity_tools=DIGEST_A, recomputed_tools=DIGEST_B)
        done = run_tool(["--npx-root", str(root), "--version", "9.9.9", "--strict"])
        assert done.returncode == 1, f"exit {done.returncode}: {done.stderr.strip()}"
        assert "FINDING:" in done.stderr and "!=" in done.stderr, done.stderr
        records = json.loads(done.stdout)
        assert records[0]["tools_sha256"] == DIGEST_B, records[0]["tools_sha256"]

    def counts_mismatch(root):
        make_fixture(root, "cacheone", "9.9.9", count=(3, 4, 1), independent=(5, 4, 1))
        done = run_tool(["--npx-root", str(root), "--version", "9.9.9", "--strict"])
        assert done.returncode == 1, f"exit {done.returncode}: {done.stderr.strip()}"
        assert "counts.cli_commands=3 != independent cli_commands=5" in done.stderr, done.stderr

    def missing_version(root):
        make_fixture(root, "cacheone", "9.9.9")
        done = run_tool(["--npx-root", str(root), "--version", "1.2.3"])
        assert done.returncode == 2, f"exit {done.returncode}: {done.stderr.strip()}"
        assert "REFUSED:" in done.stderr and "1.2.3" in done.stderr and "9.9.9" in done.stderr, done.stderr

    def duplicate_cache(root):
        make_fixture(root, "cacheone", "9.9.9")
        make_fixture(root, "cachetwo", "9.9.9")
        done = run_tool(["--npx-root", str(root), "--version", "9.9.9"])
        assert done.returncode == 2, f"exit {done.returncode}: {done.stderr.strip()}"
        assert "cacheone" in done.stderr and "cachetwo" in done.stderr and "2 cache installs" in done.stderr, done.stderr

    def bad_root(root):
        done = run_tool(["--npx-root", str(root / "absent"), "--version", "9.9.9"])
        assert done.returncode == 2, f"exit {done.returncode}: {done.stderr.strip()}"
        assert "not a directory" in done.stderr, done.stderr

    def out_file(root):
        make_fixture(root, "cacheone", "9.9.9")
        out_path = root / "out" / "rea-catalog.json"
        done = run_tool(["--npx-root", str(root), "--version", "9.9.9", "--out", str(out_path)])
        assert done.returncode == 0, f"exit {done.returncode}: {done.stderr.strip()}"
        written = out_path.read_text(encoding="utf-8")
        assert written == done.stdout, "file bytes differ from stdout"
        assert json.loads(written) == json.loads(done.stdout), "file JSON differs"

    check("clean", clean)
    check("digest-mismatch", digest_mismatch)
    check("counts-mismatch", counts_mismatch)
    check("missing-version", missing_version)
    check("duplicate-cache", duplicate_cache)
    check("bad-root", bad_root)
    check("out-file", out_file)

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"SELFTEST: FAILED cases={trials} fails={len(failures)}")
        return 1
    print(f"SELFTEST: CLEAN cases={trials}")
    return 0


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64
DIGEST_P = "c" * 64
DIGEST_C = "d" * 64


def make_fixture(root, cache_name, version, *, count=(3, 4, 1), identity_tools=DIGEST_A,
                 recomputed_tools=DIGEST_A, independent=(3, 4, 1)):
    """Write a stub rea-agents package with the four modules the probe imports."""
    package_dir = Path(root) / cache_name / "node_modules" / "rea-agents"
    (package_dir / "dist" / "contracts").mkdir(parents=True, exist_ok=True)
    (package_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (package_dir / "package.json").write_text(
        json.dumps({"name": "rea-agents", "version": version}), encoding="utf-8"
    )
    (package_dir / "scripts" / "rea.mjs").write_text(
        f'console.log("{version}");\n', encoding="utf-8"
    )
    (package_dir / "dist" / "catalogIdentity.js").write_text(
        "export const CATALOG_IDENTITY = Object.freeze({\n"
        f"  counts: {{cli_commands: {count[0]}, mcp_tools: {count[1]}, mcp_prompts: {count[2]}}},\n"
        f'  digests: {{tools_sha256: "{identity_tools}", prompts_sha256: "{DIGEST_P}", '
        f'combined_sha256: "{DIGEST_C}"}}\n'
        "});\n"
        "export const createCatalogDigests = () => ({\n"
        f'  tools_sha256: "{recomputed_tools}", prompts_sha256: "{DIGEST_P}", '
        f'combined_sha256: "{DIGEST_C}"\n'
        "});\n",
        encoding="utf-8",
    )
    (package_dir / "dist" / "cliCommandNames.js").write_text(
        "export const CLI_COMMAND_NAMES = Object.freeze("
        + json.dumps([f"c{index}" for index in range(independent[0])]) + ");\n",
        encoding="utf-8",
    )
    (package_dir / "dist" / "contracts" / "toolContracts.js").write_text(
        "export const TOOL_CONTRACTS = Object.freeze("
        + json.dumps([{"name": f"t{index}"} for index in range(independent[1])]) + ");\n",
        encoding="utf-8",
    )
    (package_dir / "dist" / "contracts" / "promptContracts.js").write_text(
        "export const PROMPT_CONTRACTS = Object.freeze("
        + json.dumps([{"name": f"p{index}"} for index in range(independent[2])]) + ");\n",
        encoding="utf-8",
    )
    return package_dir


def run_tool(args):
    return subprocess.run(
        [sys.executable, "-I", "-B", str(Path(__file__).resolve()), *args],
        capture_output=True, text=True, timeout=300,
    )


if __name__ == "__main__":
    sys.exit(main())
