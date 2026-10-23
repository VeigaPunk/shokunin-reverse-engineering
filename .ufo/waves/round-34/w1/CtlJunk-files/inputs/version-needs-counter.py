#!/usr/bin/env python3
"""Revision-bound P34-version-needs counter. Static metadata only; never executes carriers."""
import argparse
import hashlib
import json
import os
import secrets
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

PREDICATE = "P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present."
CLAIMS = ".ufo/waves/round-34/claims.json"
READER = "tools/round-34/elf-version-needs.py"

class Unevaluable(Exception):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key:" + key)
        result[key] = value
    return result

def decode(data):
    return json.loads(data, object_pairs_hook=unique)

def canonical(value):
    if not isinstance(value, dict) or set(value) != {"schema", "needed"} or type(value["schema"]) is not int or value["schema"] != 1:
        return False
    if not isinstance(value["needed"], list):
        return False
    files = []
    for record in value["needed"]:
        if not isinstance(record, dict) or set(record) != {"file", "versions"} or not isinstance(record["file"], str) or not record["file"] or not isinstance(record["versions"], list):
            return False
        files.append(record["file"])
        versions = []
        for version in record["versions"]:
            if not isinstance(version, dict) or set(version) != {"name", "flags", "other", "hash"} or not isinstance(version["name"], str) or not version["name"]:
                return False
            if any(type(version[k]) is not int or version[k] < 0 for k in ("flags", "other", "hash")):
                return False
            if version["flags"] > 65535 or version["other"] > 65535 or version["hash"] > 4294967295:
                return False
            versions.append((version["name"], version["other"]))
        if versions != sorted(versions) or len(set(versions)) != len(versions):
            return False
    return files == sorted(files) and len(set(files)) == len(files)

def safe_path(path):
    p = PurePosixPath(path)
    if not path or p.is_absolute() or ".." in p.parts or ":" in path or "\x00" in path:
        raise Unevaluable("unsafe_path")
    return path

def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and not k.startswith("PYTHON")}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["LC_ALL"] = "C"
    return env

def git(root, args):
    result = subprocess.run(["git", "--no-replace-objects", "-c", "core.fsmonitor=false", "-C", str(root), *args], env=clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    if result.returncode:
        raise Unevaluable("git_read:" + result.stderr.decode(errors="replace")[:200])
    return result.stdout

def blob(root, rev, path):
    return git(root, ["show", rev + ":" + safe_path(path)])

def renamed(data, expected, table):
    """Benign never-executed metadata challenge, not a loader-valid image."""
    offset, size = table["offset"], table["size"]
    if type(offset) is not int or type(size) is not int or offset < 0 or size < 1 or offset + size > len(data):
        raise Unevaluable("string_table_bounds")
    original = data[offset:offset + size]
    names = [record["file"] for record in expected["needed"]]
    names += [version["name"] for record in expected["needed"] for version in record["versions"]]
    if any(name.encode("ascii") + b"\0" not in original for name in names):
        raise Unevaluable("expected_string_absent")
    alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-"
    shuffled = list(alphabet)
    # Sattolo's bounded single-cycle shuffle has no fixed points.
    for index in range(len(shuffled) - 1, 0, -1):
        other = secrets.randbelow(index)
        shuffled[index], shuffled[other] = shuffled[other], shuffled[index]
    translate = bytes.maketrans(alphabet, bytes(shuffled))
    changed = data[:offset] + original.translate(translate) + data[offset + size:]
    prediction = decode(json.dumps(expected))
    for record in prediction["needed"]:
        record["file"] = record["file"].encode("ascii").translate(translate).decode("ascii")
        for version in record["versions"]:
            version["name"] = version["name"].encode("ascii").translate(translate).decode("ascii")
        record["versions"].sort(key=lambda version: (version["name"], version["other"]))
    prediction["needed"].sort(key=lambda record: record["file"])
    return changed, prediction, translate.hex()

def score(carriers, fetch, reader, documents_ok, target, production=True):
    """The sole pass condition is the literal predicate above, not receipt labels."""
    rows = []
    with tempfile.TemporaryDirectory(prefix="kaidoku-r34-score-") as temp:
        directory = Path(temp)
        program = directory / "reader.py"
        program.write_bytes(reader)
        for row in carriers:
            data = fetch(row["path"])
            if len(data) != row["size"] or digest(data) != row["sha256"]:
                raise Unevaluable("carrier_pin:" + row["id"])
            attempts = []
            for schedule in range(2):
                # Neither basename, carrier id, source path nor expected JSON is given to the reader.
                path = directory / ("opaque-" + secrets.token_hex(12) + ".data")
                candidate, expected, translation = renamed(data, row["expected"], row["string_table"]) if schedule == 1 and row.get("string_table") else (data, row["expected"], None)
                path.write_bytes(candidate)
                path.chmod(0o644)
                argv = [sys.executable, "-I", "-B", str(program), str(path)]
                try:
                    run = subprocess.run(argv, cwd=directory, env=clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                    observed = decode(run.stdout) if run.returncode == 0 and len(run.stdout) <= 1048576 else None
                    matched = run.returncode == 0 and canonical(observed) and observed == expected
                    attempts.append({"schedule": schedule, "exit": run.returncode, "matched": matched, "observed": observed, "stderr": run.stderr.decode(errors="replace")[:4096], "stdout_sha256": digest(run.stdout), "input_sha256": digest(candidate), "string_translation": translation})
                except (ValueError, UnicodeError) as error:
                    attempts.append({"schedule": schedule, "matched": False, "finding": "reader_json", "detail": str(error)})
                except subprocess.TimeoutExpired:
                    attempts.append({"schedule": schedule, "matched": False, "finding": "reader_timeout"})
                path.unlink()
            rows.append({"id": row["id"], "matched": all(a["matched"] for a in attempts), "attempts": attempts})
    matched = sum(row["matched"] for row in rows)
    met = matched == target and len(rows) == target and documents_ok
    finding = "version_needs_match" if met else "version_needs_mismatch" if matched != target else "document_mismatch"
    return {"predicate": PREDICATE if production else "isolated comparator fixture; not a P34 production score", "target": target, "matched": matched, "documents_ok": documents_ok, "met_target": met, "finding": finding, "rows": rows}, 0 if met else 1

def validate_manifest(manifest, target):
    if not isinstance(manifest, dict) or manifest.get("schema") != 1 or not isinstance(manifest.get("carriers"), list) or len(manifest["carriers"]) != target:
        raise Unevaluable("manifest_schema")
    ids, hashes = set(), set()
    for row in manifest["carriers"]:
        if not isinstance(row, dict) or not all(k in row for k in ("id", "path", "size", "sha256", "expected")):
            raise Unevaluable("manifest_row")
        safe_path(row["path"])
        if row["id"] in ids or row["sha256"] in hashes:
            raise Unevaluable("manifest_duplicate")
        ids.add(row["id"])
        hashes.add(row["sha256"])
        if type(row["size"]) is not int or row["size"] < 1 or row["size"] > 16777216 or not isinstance(row["sha256"], str) or len(row["sha256"]) != 64 or not canonical(row["expected"]):
            raise Unevaluable("manifest_row_schema")
    return manifest["carriers"]

def section(text, title):
    lines = text.splitlines()
    if lines.count(title) != 1:
        return None
    start = lines.index(title)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]).strip()

def measure(args):
    root = Path(args.root)
    # The contract comes from the explicitly supplied immutable freeze revision,
    # not from the measured tree and never from a candidate-reader stdout field.
    frozen = git(root, ["rev-parse", "--verify", args.freeze + "^{commit}"]).decode().strip()
    rev = git(root, ["rev-parse", "--verify", args.rev + "^{commit}"]).decode().strip()
    contract = decode(blob(root, frozen, CLAIMS))
    if contract.get("predicate") != PREDICATE or contract.get("target") != 12 or contract.get("reader") != READER:
        raise Unevaluable("contract_schema")
    for path, expected in contract["instruments"].items():
        if digest(blob(root, frozen, path)) != expected:
            raise Unevaluable("instrument_pin:" + path)
    if digest(Path(__file__).read_bytes()) != contract["instruments"].get("tools/round-34/version-needs-counter.py"):
        raise Unevaluable("running_counter_pin")
    manifest_bytes = blob(root, frozen, contract["manifest"])
    if digest(manifest_bytes) != contract["manifest_sha256"]:
        raise Unevaluable("manifest_pin")
    rows = validate_manifest(decode(manifest_bytes), 12)
    if any(row["expected"]["needed"] and (not isinstance(row.get("string_table"), dict) or set(row["string_table"]) != {"offset", "size"}) for row in rows):
        raise Unevaluable("string_table_schema")
    docs = []
    for path, expected in contract["documents"].items():
        try:
            ok = digest(blob(root, rev, path)) == expected
        except Unevaluable:
            ok = False
        docs.append({"path": path, "ok": ok})
    try:
        skill = blob(root, rev, "SKILL.md").decode("utf-8")
        approved = blob(root, frozen, contract["skill_section"]["approved"]).decode("utf-8")
        docs.append({"path": "SKILL.md#" + contract["skill_section"]["heading"], "ok": section(skill, contract["skill_section"]["heading"]) == approved.strip()})
    except (Unevaluable, UnicodeError):
        docs.append({"path": "SKILL.md#version-needs", "ok": False})
    try:
        registry = blob(root, rev, "corpus/SOURCES.md").decode("utf-8").splitlines()
        for source_id, expected_row in contract["source_rows"].items():
            docs.append({"path": "corpus/SOURCES.md#" + source_id, "ok": registry.count(expected_row) == 1})
    except (Unevaluable, UnicodeError):
        docs.append({"path": "corpus/SOURCES.md#round34", "ok": False})
    for path, expected in contract["sources"].items():
        if digest(blob(root, frozen, path)) != expected:
            raise Unevaluable("source_pin:" + path)
        try:
            source_ok = digest(blob(root, rev, path)) == expected
        except Unevaluable:
            source_ok = False
        docs.append({"path": path, "ok": source_ok})
    try:
        reader = Path(args.control_reader).read_bytes() if args.control_reader else blob(root, rev, READER)
    except Unevaluable:
        return {"predicate": PREDICATE, "measured_revision": rev, "freeze_revision": frozen, "matched": 0, "target": 12, "met_target": False, "documents_ok": all(d["ok"] for d in docs), "finding": "reader_absent"}, 1
    if not args.control_reader and digest(reader) != contract["instruments"][READER]:
        raise Unevaluable("reader_pin")
    result, code = score(rows, lambda p: blob(root, frozen, p), reader, all(d["ok"] for d in docs), 12)
    result.update({"measured_revision": rev, "freeze_revision": frozen, "reader_sha256": digest(reader), "documents": docs, "mode": "control" if args.control_reader else "production"})
    return result, code

def fixture_measure(args):
    spec = decode(Path(args.fixture_spec).read_bytes())
    base = Path(args.fixture_spec).parent
    rows = validate_manifest(spec["manifest"], spec["target"])
    return score(rows, lambda p: (base / safe_path(p)).read_bytes(), Path(args.fixture_reader).read_bytes(), spec["documents_ok"], spec["target"], production=False)

def selftest():
    # Text-only isolated fixtures exercise the outer CLI. They are not ELF cases.
    empty = {"schema": 1, "needed": []}
    named = {"schema": 1, "needed": [{"file": "libA", "versions": [{"name": "VER_1", "flags": 0, "other": 2, "hash": 1}]}]}
    cases = [
        ("green-empty", "print('{\"schema\":1,\"needed\":[]}')", True, 0, "version_needs_match"),
        ("red-junk", "print('{}')", True, 1, "version_needs_mismatch"),
        ("red-all-false", "print('false')", True, 1, "version_needs_mismatch"),
        ("red-duplicate-json", "print('{\"schema\":1,\"schema\":1,\"needed\":[]}')", True, 1, "version_needs_mismatch"),
        ("red-exit", "raise SystemExit(1)", True, 1, "version_needs_mismatch"),
        ("red-documents", "print('{\"schema\":1,\"needed\":[]}')", False, 1, "document_mismatch"),
        ("red-boolean-schema", "print('{\"schema\":true,\"needed\":[]}')", True, 1, "version_needs_mismatch"),
        ("red-pin", "print('{\"schema\":1,\"needed\":[]}')", True, 2, "carrier_pin:t"),
        ("red-manifest-count", "print('{}')", True, 2, "manifest_schema"),
        ("green-translated", "import json,sys;from pathlib import Path;s=Path(sys.argv[1]).read_bytes().split(bytes([0]));print(json.dumps({'schema':1,'needed':[{'file':s[0].decode(),'versions':[{'name':s[1].decode(),'flags':0,'other':2,'hash':1}]}]}))", True, 0, "version_needs_match"),
        ("red-replay", "print(" + repr(json.dumps(named)) + ")", True, 1, "version_needs_mismatch"),
    ]
    records = []
    with tempfile.TemporaryDirectory(prefix="kaidoku-r34-selftest-") as temp:
        base = Path(temp)
        for name, code, docs, expected_exit, finding in cases:
            data = b"libA\0VER_1\0" if name in ("green-translated", "red-replay") else b"benign text only\n"
            (base / "input.txt").write_bytes(data)
            row = {"id": "t", "path": "input.txt", "size": len(data), "sha256": digest(data), "expected": named if name in ("green-translated", "red-replay") else empty}
            if name in ("green-translated", "red-replay"):
                row["string_table"] = {"offset": 0, "size": len(data)}
            if name == "red-pin":
                row["sha256"] = "0" * 64
            spec = {"target": 1, "documents_ok": docs, "manifest": {"schema": 1, "carriers": [row]}}
            if name == "red-manifest-count":
                spec["manifest"]["carriers"] = []
            (base / "spec.json").write_text(json.dumps(spec))
            (base / "reader.py").write_text(code + "\n")
            argv = [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--fixture-spec", str(base / "spec.json"), "--fixture-reader", str(base / "reader.py")]
            run = subprocess.run(argv, env=clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
            observed = decode(run.stdout)
            ok = run.returncode == expected_exit and observed.get("finding") == finding and observed.get("met_target") == (expected_exit == 0)
            records.append({"case": name, "expected_exit": expected_exit, "exit": run.returncode, "finding": observed.get("finding"), "ok": ok})
    return {"kind": "selftest", "cases": records, "passed": sum(r["ok"] for r in records), "total": len(records)}, 0 if all(r["ok"] for r in records) else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--freeze")
    parser.add_argument("--control-reader", help="Score one explicitly labelled adversarial reader with the SAME predicate")
    parser.add_argument("--fixture-spec", help=argparse.SUPPRESS)
    parser.add_argument("--fixture-reader", help=argparse.SUPPRESS)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.selftest:
            result, code = selftest()
        elif args.fixture_spec and args.fixture_reader:
            result, code = fixture_measure(args)
        elif args.root and args.rev and args.freeze:
            result, code = measure(args)
        else:
            raise Unevaluable("arguments")
    except (Unevaluable, ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as error:
        result, code = {"predicate": PREDICATE, "met_target": False, "finding": str(error)}, 2
    print(json.dumps(result, sort_keys=True))
    return code

if __name__ == "__main__":
    sys.exit(main())
