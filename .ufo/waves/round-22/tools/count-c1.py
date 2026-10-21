#!/usr/bin/env python3
"""R22-C1 counter: frozen T1 catalog verbs exercised by retained, bound Evidence.

A T1 verb counts only when a knowledge entry at REV names the verb and exact
retained CLI-envelope file under EVIDENCE_PREFIX. The envelope must carry
ok:true, matching meta.command, and one direct Evidence data record binding
the cited evidence_id and actual operation (debugger aliases from REA6.5.0
cliCommandNames.js, retained evidence/sources/cli-aliases.json). Producer,
metadata and nested-record refusals block counting; bare extractions do not
count. The first source: line cites a mined tier A/B S051+ row opened
2026-10-21 whose used-by names that entry; duplicate source ids are ambiguous.
Helpers are extracted at one resolved revision and must match reviewed digest
pins; inherited Git routing/replacement refs cannot redirect the CLI.
This is local association, not authentication or semantic/source-scope
admission. The original envelope is not compared with run.stdout by this
counter; final provenance controls retain that separate comparison.

Exit 0 when every T1 verb is exercised, 1 when any is not, 2 unevaluable.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import os
import hashlib

T1 = ("identify-flutter-build", "inspect-dart-aot", "debug-with-gdb",
      "debug-with-rizin", "inspect-signal-decoders", "decode-signal-recording")
EVIDENCE_PREFIX = ".ufo/waves/round-22/evidence/c1/"
CLI_BIND_VERB = {"debug-with-gdb": "gdb-console",
                 "debug-with-rizin": "rizin-debug-command"}
HELPER_SHA256 = {
    ".ufo/waves/round-20/tools/verb-coverage.py": "cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f",
    ".ufo/waves/round-21/tools/verb-coverage.py": "615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b",
}
SELFTEST_MANIFEST_SHA256 = "1abdd9df347610a77f01afbe157c7fdbfb4c90bc2e26b6b3ecebd08fbd930bb8"


def load(root, rel, name):
    spec = importlib.util.spec_from_file_location(name, Path(root) / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def revision_helpers(root, rev):
    """Load the requested revision's helpers, never mutable worktree code."""
    paths = (".ufo/waves/round-20/tools/verb-coverage.py",
             ".ufo/waves/round-21/tools/verb-coverage.py")
    with tempfile.TemporaryDirectory(prefix="kaidoku-r22-helpers-") as directory:
        for rel in paths:
            proc = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{rel}"],
                                  capture_output=True, check=False)
            if proc.returncode:
                raise ValueError("helper_revision_unreadable: " + rel)
            if hashlib.sha256(proc.stdout).hexdigest() != HELPER_SHA256[rel]:
                raise ValueError("helper_source_untrusted: " + rel)
            target = Path(directory) / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(proc.stdout)
        r21 = load(directory, paths[1], "kaidoku_r21_bind")
        return r21, r21.legacy_helpers(directory)


def bind_cli(r21, text, verb, evidence_id):
    """Bind the original CLI envelope, preserving producer refusal ancestry."""
    try:
        envelope = r21.decode(text)
        json.dumps(envelope, allow_nan=False)
        if not isinstance(envelope, dict) or "ok" not in envelope or "data" not in envelope:
            return 2
        if envelope["ok"] is not True or r21.refused(envelope):
            return 1
        meta = envelope.get("meta")
        if not isinstance(meta, dict) or meta.get("command") != verb or r21.refused(meta):
            return 1
        record = envelope["data"]
        if not isinstance(record, dict) or "evidence_id" not in record or "operation" not in record:
            return 2
        pending = [record]
        while pending:
            node = pending.pop()
            if isinstance(node, list):
                pending.extend(node)
                continue
            if not isinstance(node, dict):
                continue
            if ("ok" in node and node["ok"] is not True) or r21.refused(node):
                return 1
            pending.extend(node.values())
        binding_verb = CLI_BIND_VERB.get(verb, verb)
        return r21.bind(json.dumps(record), binding_verb, evidence_id)[1]
    except (ValueError, RecursionError):
        return 2


def measure(root, rev):
    resolved = subprocess.run(["git","-C",str(root),"rev-parse","--verify","--end-of-options",f"{rev}^{{commit}}"],
                              capture_output=True,text=True,check=False)
    if resolved.returncode:
        raise ValueError("invalid_revision")
    rev = resolved.stdout.strip()
    r21, r20 = revision_helpers(root, rev)
    r20.DEFAULT_TARGETS = ()
    r20.EVIDENCE_PREFIX = EVIDENCE_PREFIX
    r20.CITED = re.compile(re.escape(EVIDENCE_PREFIX) + r"[A-Za-z0-9._/-]*", re.ASCII)
    try:
        result = r21._measure(r20, root, rev)
    except r20.Refusal as error:
        raise ValueError(str(error)) from error
    def read_blob(path):
        proc = subprocess.run(["git","-C",str(root),"show",f"{result['rev']}:{path}"],
                              capture_output=True,check=False)
        if proc.returncode:
            raise ValueError("blob_revision_unreadable: " + path)
        return proc.stdout.decode("utf-8")
    source_rows = {}
    source_ids = set()
    for line in read_blob("corpus/SOURCES.md").splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 13 and re.fullmatch(r"S[0-9]{3,}", cells[1]):
            if cells[1] in source_ids:
                raise ValueError("duplicate_source_id: " + cells[1])
            source_ids.add(cells[1])
            if int(cells[1][1:]) >= 51 and cells[4] in ("A", "B") and cells[8] == "mined" and cells[9] == "2026-10-21":
                source_rows[cells[1]] = cells[11].split(",")
    paths = [path for path, _ in r20.tree_entries(root, result["rev"])]
    texts = []
    eligible = set()
    for path in paths:
        if not path.startswith(r20.KNOWLEDGE_PREFIX):
            continue
        text = read_blob(path)
        texts.append(text)
        source = text.partition("\n")[0]
        ids = re.findall(r"\bS[0-9]{3,}\b", source) if source.startswith("source:") else []
        if any(path in [part.strip() for part in source_rows.get(sid, [])] for sid in ids):
            eligible.add(text)
    result["targets"] = {}
    for verb in T1:
        witnesses, unevaluable = [], []
        entries = 0
        for text in texts:
            if not r20.command_pattern(verb).search(text):
                continue
            entries += 1
            cited = r20.cited_prefixes(text)
            ids = sorted(set(match.group(0) for match in r20.HEX64.finditer(text)))
            for path in paths:
                if not path.startswith(EVIDENCE_PREFIX) or path not in cited:
                    continue
                blob = read_blob(path)
                for evidence_id in ids:
                    if evidence_id not in blob:
                        continue
                    code = bind_cli(r21, blob, verb, evidence_id)
                    if code == 0 and text in eligible:
                        witnesses.append([evidence_id, path])
                    elif code == 2:
                        unevaluable.append(path)
        result["targets"][verb] = {
            "entries": entries,
            "exercised": bool(witnesses),
            "bound_evidence": witnesses[:5],
            "unsupported_candidates": sorted(set(unevaluable)),
        }
    exercised = [verb for verb in T1 if result["targets"][verb]["exercised"]]
    return {
        "rev": result["rev"],
        "claim": "R22-C1",
        "finding": "c1_complete" if len(exercised) == len(T1) else "c1_incomplete",
        "t1": list(T1),
        "t1_exercised": exercised,
        "t1_exercised_count": len(exercised),
        "t1_total": len(T1),
        "targets": result["targets"],
        "catalog_zero": result["zero"],
        "catalog_zero_count": len(result["zero"]),
        "catalog_mentioned_count": len(result["mentioned"]),
        "catalog_total": len(result["cli_commands"]),
        "limit": "CLI envelope/entry/source linkage only; source relevance and scope admission remain manual; no cryptographic authentication",
    }


def main():
    for key in tuple(os.environ):
        if key.startswith("GIT_"):
            del os.environ[key]
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        root = Path(args.root).resolve() if args.root else next(
            (path for path in Path(__file__).resolve().parents if
             (path / ".ufo/waves/round-22/tools/counter-fixtures.py").is_file()), None)
        if root is None:
            print(json.dumps({"finding":"unevaluable","error":"selftest_root_required"}))
            return 2
        try:
            manifest_bytes=(root/".ufo/waves/round-22/frozen/expected-v2.json").read_bytes()
            if hashlib.sha256(manifest_bytes).hexdigest()!=SELFTEST_MANIFEST_SHA256:
                raise ValueError("manifest_digest")
            manifest=json.loads(manifest_bytes)
            observed_inputs={}
            for rel,digest in manifest["inputs"].items():
                observed_inputs[rel]=hashlib.sha256((root/rel).read_bytes()).hexdigest()
                if observed_inputs[rel]!=digest:
                    raise ValueError("input_digest: "+rel)
        except (OSError,UnicodeError,ValueError,KeyError) as error:
            print(json.dumps({"finding":"snapshot_tampered","error":str(error)}))
            return 2
        fixtures = load(root, ".ufo/waves/round-22/tools/counter-fixtures.py", "r22_c1_fixtures")
        result, code = fixtures.run("C1", Path(__file__).resolve(), root)
        result["selftest_manifest_sha256"]=SELFTEST_MANIFEST_SHA256
        result["selftest_input_sha256"]=observed_inputs
        print(json.dumps(result, sort_keys=True))
        return code
    if not args.root or not args.rev:
        parser.error("--root and --rev required unless --selftest")
    try:
        out = measure(args.root, args.rev)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(json.dumps({"finding": "unevaluable", "error": str(error)}))
        return 2
    print(json.dumps(out, sort_keys=True))
    return 0 if out["t1_exercised_count"] == out["t1_total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
