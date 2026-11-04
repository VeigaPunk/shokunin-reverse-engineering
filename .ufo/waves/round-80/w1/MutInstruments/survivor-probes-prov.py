#!/usr/bin/env python3
"""Provenance survivor proofs, on a git fixture repo under TMPDIR.

Each probe returns True only when the module still enforces the rule the
selftest is missing. The fixture repo is created under $TMPDIR (never a fixed
path) and its toplevel is asserted to be the fixture dir before the first commit.
Run: survivor-probes-prov.py <pristine> <mutant.py>...
"""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile


def load(path: str):
    spec = importlib.util.spec_from_file_location("prov_probe_" + pathlib.Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build_repo() -> tuple[str, str]:
    base = tempfile.mkdtemp(prefix="prov-probe-", dir=os.environ.get("TMPDIR") or None)
    repo = os.path.join(base, "fixture")
    os.makedirs(repo)

    def run(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True)

    run("init", "-q", "-b", "main")
    toplevel = run("rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(toplevel) == os.path.realpath(repo), (toplevel, repo)
    run("config", "user.name", "mut-probe")
    run("config", "user.email", "mut@example.invalid")
    run("config", "commit.gpgsign", "false")

    def write(relative: str, text: str) -> None:
        target = os.path.join(repo, relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)

    def commit(message: str) -> str:
        run("add", "-A")
        run("commit", "-qm", message)
        return run("rev-parse", "HEAD").stdout.decode().strip()

    write("inst.py", "one\n")
    commit("v1")
    write("inst.py", "two\n")
    commit("v2")
    scores = ".ufo/waves/round-60/l1/scores"
    write(f"{scores}/ok.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": "f" * 64}}))
    write(f"{scores}/attacks/forged.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": "e" * 64}}))
    tip = commit("receipts")
    run("branch", "deadbeef")  # a hex-looking symbolic ref, RE_ABBREV-legal
    return repo, tip


def p2_attacks(mod, repo: str, tip: str) -> bool:
    """The /attacks/ receipt never enters the population.

    Equivalent-mutant probe: the mutant is expected to pass this too, because
    `discover()` never enumerates a subdirectory (the `isfile` gate skips it) —
    the `/attacks/` string filter is unreachable, so the case is green for the
    wrong reason and no assertion can pin the filter.
    """
    rows = mod.sweep(repo, tip, 60, 60)["rows"]
    return not any("/attacks/" in row["path"] for row in rows)


def p3_hex_branch(mod, repo: str, tip: str) -> bool:
    """A branch whose name is legal abbreviation hex is still a symbolic ref."""
    try:
        mod.resolve_commit(repo, "deadbeef")
    except mod.Unevaluable:
        return True
    return False


def p10_checked_at(mod, repo: str, tip: str) -> bool:
    """A receipt with checked_at deleted must be a defect."""
    receipt = mod.sweep(repo, tip, 60, 60)
    receipt.pop("checked_at", None)
    return any("checked_at" in defect for defect in mod.validate_receipt(receipt)["defects"])


PROBES = {"p2-attacks-not-excluded": p2_attacks,
          "p3-symbolic-rev-accepted": p3_hex_branch,
          "p10-drop-checked-at": p10_checked_at}


def main(argv: list[str]) -> int:
    repo, tip = build_repo()
    try:
        pristine = load(argv[0])
        rows = []
        for path in argv[1:]:
            mutant = load(path)
            mid = pathlib.Path(path).stem
            probe = PROBES[mid]
            before = bool(probe(pristine, repo, tip))
            after = bool(probe(mutant, repo, tip))
            rows.append({"mutant": mid,
                         "pristine_asserts_correct": before,
                         "mutant_asserts_correct": after,
                         "proved": before and not after,
                         "equivalent_mutant": before and after})
        for row in rows:
            print(json.dumps(row, sort_keys=True))
        proved = sum(1 for r in rows if r["proved"])
        print("PROBES proved=%d/%d equivalent=%d"
              % (proved, len(rows), sum(1 for r in rows if r["equivalent_mutant"])))
        return 0 if proved + sum(1 for r in rows if r["equivalent_mutant"]) == len(rows) else 1
    finally:
        shutil.rmtree(os.path.dirname(repo), ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
