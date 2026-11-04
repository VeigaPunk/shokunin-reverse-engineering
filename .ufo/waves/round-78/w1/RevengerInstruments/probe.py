#!/usr/bin/env python3
"""Round-78 seat RevengerInstruments: independent materialiser and probe.

Reads the committed fixture trees under `.ufo/waves/round-78/attacks/` and the
two frozen round-77 instruments, materialises each fixture as a private
two-commit git repo under `--work`, runs the frozen instrument the round-78
gate's base arm names, and records the field that proves acceptance.

Every fixture file is read through `git show <fixtures-rev>:<path>`, so the
probe measures committed bytes, not the working tree.  `--mutants` reconstructs
the two round-77 mutation survivors and asks the frozen round-78 gate's own
rule functions (loaded from `git show <gate-rev>:tools/round-78/attack-gate.py`)
what they see.

Every fixture repo is created under --work; the script refuses to commit
anywhere whose `rev-parse --show-toplevel` is not the fixture directory.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

FIXTURE_ROOT = ".ufo/waves/round-78/attacks"
GATE = "tools/round-29/prefile-check.sh"
ATTACK_GATE = "tools/round-78/attack-gate.py"
INSTRUMENTS = {
    "verdict-bind": "tools/round-77/verdict-bind.py",
    "prefile-receipt": "tools/round-77/prefile-receipt.py",
}
FIXED_ENV = {
    "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@localhost",
    "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@localhost",
    "GIT_AUTHOR_DATE": "2026-11-04T00:00:00 -0300",
    "GIT_COMMITTER_DATE": "2026-11-04T00:00:00 -0300",
}

CLASSES = [
    {
        "id": "receipt-unauth", "fixture": "a1-forged-receipt",
        "instrument": "verdict-bind", "base": "record_clean",
        "rule": "receipt_auth",
        "code_path": (
            "verdict-bind.py:118-136 Resolver.receipt reads `git show rev:path` "
            "and json.loads it; :361-405 bind_cell passes that dict to bind; "
            ":197-222 bind compares atoms[id].ok (201-215) and receipt[field] "
            "(216-222); :447 "
            "`ok = not defects and bound > 0`. No code reads receipt.rev or "
            "receipt.instrument, so a hand-authored receipt with the claimed "
            "values is accepted."),
        "would_refuse_if": (
            "the receipt's atoms[].ok or mismatch_count differed from the "
            "claimed value (value_mismatch), the file were absent at rev "
            "(absent_receipt), or the binder required a 40-hex rev plus an "
            "instrument pin that re-derives from the blob at that rev"),
    },
    {
        "id": "qualified-atom", "fixture": "a2-repunctuated",
        "instrument": "verdict-bind", "base": "record_clean",
        "rule": "qualified_atom",
        "code_path": (
            "verdict-bind.py:74 QUALIFIER_RE `^[A-Za-z][A-Za-z0-9_-]*:\\s*` "
            "strips `D24:` leaving the clause `true`; :156-175 parse_clause "
            "matches none of its seven regexes and returns None; :368 "
            "`parsed = [c for c in clauses if c is not None]` drops it. "
            "`mismatch 0` matches no regex either (MISMATCH_RE is "
            ":81 `^(\\d+)\\s+mismatches$`); only `D24 true` binds."),
        "would_refuse_if": (
            "the one surviving clause (`D24 true`) were false, or the qualifier "
            "stripping were removed so `D24: true` parsed as an atom claim and "
            "`mismatch 0` as `mismatch_count 0` against a receipt that says 1"),
    },
    {
        "id": "near-miss-field", "fixture": "a3-near-miss",
        "instrument": "verdict-bind", "base": "record_clean",
        "rule": "near_miss_field",
        "code_path": (
            "verdict-bind.py:156-175 parse_clause: `mismatch 0` matches no "
            "grammar rule (MISMATCH_RE :81 wants `0 mismatches`; FIELD_RE :77 "
            "wants `field value` with a bare field name) -> None -> dropped at "
            ":368. `D24 true` binds through :196-211."),
        "would_refuse_if": (
            "the clause were spelled in the defined grammar (`0 mismatches` or "
            "`mismatch_count 0`) against a receipt that says otherwise, or an "
            "unparsable clause counted as a defect instead of being skipped"),
    },
    {
        "id": "negated-verdict", "fixture": "a4-negated",
        "instrument": "verdict-bind", "base": "record_clean",
        "rule": "negated_verdict",
        "code_path": (
            "verdict-bind.py:156-175 parse_clause returns None for the English "
            "clause `the receipt does not record D24 false`; it is dropped at "
            ":368. There is no negation rule anywhere; the second clause "
            "`D24 true` binds (:196-211) and carries the group."),
        "would_refuse_if": (
            "the negated claim were scored as its opposite, or any prose clause "
            "produced a defect instead of being skipped"),
    },
    {
        "id": "nested-hidden-mismatch", "fixture": "a5-nested-field",
        "instrument": "verdict-bind", "base": "record_clean",
        "rule": "value_mismatch",
        "code_path": (
            "verdict-bind.py:197-222 bind's field branch: `forged_detected` is "
            "not an atom id (ATOM_ID_RE :75 `^[A-Z][0-9]`), and the lookup is "
            "`receipt[field]` on the top level, so :217 returns "
            "`(False, 'unbound', {'reason': 'unknown_field'})`; bind_cell "
            ":399-400 counts it as unbound (not a defect) and the receipt's "
            "nested `arms[0].observed.verdict.forged_detected: false` is never "
            "read."),
        "would_refuse_if": (
            "the binder resolved nested keys (the round-78 `resolve_field` "
            "does) and compared the nested `false` to the claimed `true`"),
    },
    {
        "id": "dropped-defect", "fixture": "a6-dropped-defect",
        "instrument": "verdict-bind", "base": "record_clean",
        "rule": "unbound_verdict",
        "code_path": (
            "verdict-bind.py:200-203 `atoms` absent -> "
            "`return False, 'defect', {'reason': 'no_atoms'}`; bind_cell "
            ":394-402 only routes `status == 'bound'` into `result['defects']` "
            "and sends every other status to `result['unbound'] += 1`, so the "
            "defect row is dropped and :447 sees `not defects`."),
        "would_refuse_if": (
            "bind_cell routed the `defect` status into `result['defects']` "
            "(the round-78 `unbound_verdict` rule), i.e. the receipt lost the "
            "atom the clause names"),
    },
    {
        "id": "unclean-clone-run", "fixture": "b1-fail-run",
        "instrument": "prefile-receipt", "base": "arm:clone-run",
        "rule": "clean_run",
        "code_path": (
            "prefile-receipt.py:214-223 arm A1: "
            "`ok = (receipt['exit'] in (0, 1) and receipt['prefile_line'] is "
            "not None and not check_receipt(receipt))` -- exit 1 with "
            "`prefile: FAIL` is a valid receipt, so a failing gate run counts "
            "as a clean one."),
        "would_refuse_if": (
            "A1 required `exit == 0` and the PASS token "
            "(`receipt['prefile_line'] == 'prefile: PASS'`), or the run left "
            "no verdict line / a malformed receipt"),
    },
    {
        "id": "stale-filing-rev", "fixture": "b2-stale-filing",
        "instrument": "prefile-receipt", "base": "arm:record-receipt",
        "rule": "filing_rev",
        "code_path": (
            "prefile-receipt.py:226-239 arm A2: `defects = "
            "check_receipt(receipt)`, i.e. `expect_rev` is not passed; "
            ":158-160 in check_receipt compares `rev` only when `expect_rev` is "
            "given, so a filing receipt at rev 000...0 with exit 0 is met."),
        "would_refuse_if": (
            "A2 called `check_receipt(receipt, expect_rev=rev)` (the routed "
            "one-line fix) or required the receipt rev to be an ancestor of "
            "the measured rev"),
    },
    {
        "id": "gate-receipt-schema", "fixture": "b3-one-key-gate",
        "instrument": "prefile-receipt", "base": "arm:gate-exits",
        "rule": "gate_receipt_schema",
        "code_path": (
            "prefile-receipt.py:241-276 arm A3: for each `gate-*.json` it "
            "parses the JSON and accepts any dict with an integer `exit` "
            "(:265-266), falling back to an `^exit=(\\d+)$` text grep (:268); "
            "`ok = bool(gate_files) and not missing` (:274). A one-key "
            "`{\"exit\": 0}` is therefore a valid gate receipt."),
        "would_refuse_if": (
            "A3 applied the receipt contract (argv naming the gate, stdout "
            "digest, verdict line, four-key env) to each gate receipt, as the "
            "round-78 `gate_receipt_schema` rule does"),
    },
    {
        "id": "gate-receipt-stale-rev", "fixture": "b4-stale-gate-rev",
        "instrument": "prefile-receipt", "base": "arm:gate-exits",
        "rule": "gate_receipt_rev",
        "code_path": (
            "prefile-receipt.py:241-276 arm A3 reads only the `exit` field of "
            "each gate receipt; `rev` is never read, so a full receipt whose "
            "`rev` is 000...0 is met."),
        "would_refuse_if": (
            "A3 required a 40-hex `rev` that is an ancestor of the measured "
            "rev (the round-78 `gate_receipt_rev` rule)"),
    },
]


class Fatal(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def child_env(work: str) -> dict:
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(work), "TMPDIR": str(work), "LANG": "C.UTF-8"}


def git(dest, *args, env=None):
    return subprocess.run(["git", "-C", str(dest), *args],
                          capture_output=True, text=True, env=env)


def git_blob(lane: pathlib.Path, rev: str, path: str) -> bytes:
    proc = subprocess.run(["git", "-C", str(lane), "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise Fatal(f"{path} absent at {rev}")
    return proc.stdout


def read_tree(lane: pathlib.Path, rev: str, prefix: str) -> dict[str, bytes]:
    proc = git(lane, "ls-tree", "-r", "--name-only", rev, "--", prefix)
    paths = [p for p in proc.stdout.splitlines() if p]
    if not paths:
        raise Fatal(f"no committed files under {prefix} at {rev}")
    return {p: git_blob(lane, rev, p) for p in paths}


def assert_toplevel(dest: pathlib.Path, env) -> None:
    top = git(dest, "rev-parse", "--show-toplevel", env=env).stdout.strip()
    if not top or pathlib.Path(top).resolve() != dest.resolve():
        raise Fatal(f"refusing to commit: toplevel {top!r} != {dest}")


def commit_all(dest: pathlib.Path, message: str, work: pathlib.Path) -> str:
    env = dict(FIXED_ENV, **child_env(work))
    if not (dest / ".git").exists():
        proc = git(dest, "init", "--quiet", env=env)
        if proc.returncode != 0:
            raise Fatal(f"git init failed: {proc.stderr[-200:]}")
    assert_toplevel(dest, env)
    for argv in (("add", "-A"), ("commit", "--quiet", "-m", message)):
        proc = git(dest, *argv, env=env)
        if proc.returncode != 0:
            raise Fatal(f"git {argv[0]} failed: {proc.stderr[-300:]}")
    return git(dest, "rev-parse", "HEAD", env=env).stdout.strip()


def materialise(lane: pathlib.Path, fixture: str, work: pathlib.Path,
                fixtures_rev: str) -> tuple[pathlib.Path, str, dict]:
    """Copy one committed fixture tree into a private two-commit repo."""
    prefix = f"{FIXTURE_ROOT}/{fixture}"
    blobs = read_tree(lane, fixtures_rev, prefix)
    dest = pathlib.Path(work, "fx", fixture)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for path, data in blobs.items():
        target = dest / path[len(prefix) + 1:]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    if not (dest / GATE).is_file():
        (dest / GATE).parent.mkdir(parents=True, exist_ok=True)
        (dest / GATE).write_bytes(git_blob(lane, fixtures_rev, GATE))
    first = commit_all(dest, f"fixture {fixture}: tree", work)
    rewrote = []
    for path in sorted(dest.rglob("*.json")):
        text = path.read_text()
        if "@HEAD@" in text:
            path.write_text(text.replace("@HEAD@", first))
            rewrote.append(str(path.relative_to(dest)))
    if rewrote:
        commit_all(dest, f"fixture {fixture}: receipts bound to {first[:8]}", work)
    rev = git(dest, "rev-parse", "HEAD", env=child_env(work)).stdout.strip()
    return dest, rev, {"first_commit": first, "rebound": rewrote}


def run_instrument(lane: pathlib.Path, instrument: str, root: pathlib.Path,
                   rev: str, work: pathlib.Path, out: pathlib.Path) -> dict:
    script = pathlib.Path(lane, INSTRUMENTS[instrument]).resolve()
    if not script.is_file():
        raise Fatal(f"{INSTRUMENTS[instrument]} absent")
    out.parent.mkdir(parents=True, exist_ok=True)
    argv = [sys.executable, "-I", "-B", str(script), "--root", str(root),
            "--rev", rev, "--json-out", str(out)]
    if instrument == "prefile-receipt":
        argv += ["--work", str(pathlib.Path(work, "base-work", out.stem)),
                 "--battery"]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          env=child_env(work), cwd=work)
    receipt = json.loads(out.read_text()) if out.is_file() else None
    return {"exit": proc.returncode, "stdout_tail": proc.stdout[-400:],
            "stderr_tail": proc.stderr[-300:], "receipt": receipt}


def acceptance(spec: dict, run: dict) -> tuple[bool, dict]:
    receipt = run.get("receipt") or {}
    if spec["base"] == "record_clean":
        accepted = run["exit"] == 0 and receipt.get("mismatch_count") == 0
        scored = []
        for cell in receipt.get("cells") or []:
            for row in cell.get("clauses") or []:
                if row.get("status") in ("bound", "defect"):
                    scored.append({"label": cell.get("label"),
                                   "clause": row.get("clause"),
                                   "status": row.get("status"),
                                   "path": row.get("path"),
                                   "claimed": row.get("claimed"),
                                   "actual": row.get("actual"),
                                   "reason": row.get("reason")})
        return accepted, {
            "exit": run["exit"],
            "mismatch_count": receipt.get("mismatch_count"),
            "defects": receipt.get("defects"),
            "population": receipt.get("population"),
            "scored_rows": scored}
    arm_name = spec["base"].split(":", 1)[1]
    arm = next((a for a in (receipt.get("arms") or [])
                if a.get("arm") == arm_name), None)
    accepted = bool(arm and arm.get("met"))
    return accepted, {"exit": run["exit"],
                      "arms_ok": receipt.get("arms_ok"),
                      "arms_total": receipt.get("arms_total"),
                      "arm": arm,
                      "all_arms": [{"arm": a.get("arm"), "met": a.get("met"),
                                    "observed": a.get("observed")}
                                   for a in (receipt.get("arms") or [])]}


def probe(lane: pathlib.Path, work: pathlib.Path, fixtures_rev: str) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    classes = []
    for spec in CLASSES:
        dest, rev, meta = materialise(lane, spec["fixture"], work, fixtures_rev)
        out = pathlib.Path(work, "receipts", spec["id"] + ".json")
        run = run_instrument(lane, spec["instrument"], dest, rev, work, out)
        accepted, evidence = acceptance(spec, run)
        classes.append({
            "id": spec["id"], "fixture": spec["fixture"],
            "instrument": spec["instrument"], "base_name": spec["base"],
            "declared_rule": spec["rule"],
            "code_path": spec["code_path"],
            "would_refuse_if": spec["would_refuse_if"],
            "accepted": accepted,
            "evidence": dict(evidence, fixture_rev=rev,
                             first_commit=meta["first_commit"],
                             rebound=meta["rebound"],
                             instrument_exit=run["exit"],
                             instrument_stdout=run["stdout_tail"]),
        })
    return {"fixtures_rev": fixtures_rev, "classes": classes}


def load_gate(lane: pathlib.Path, rev: str, work: pathlib.Path):
    """Load the frozen round-78 gate from committed bytes."""
    path = pathlib.Path(work, "gate-frozen.py")
    path.write_bytes(git_blob(lane, rev, ATTACK_GATE))
    spec = importlib.util.spec_from_file_location("r78_attack_gate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_vb(script, demo: pathlib.Path, rev: str, work: pathlib.Path,
           label: str, out_name: str) -> dict:
    out = pathlib.Path(work, "mut", out_name)
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, "-I", "-B", str(script), "--root", str(demo),
         "--rev", rev, "--json-out", str(out)],
        capture_output=True, text=True, env=child_env(work), cwd=work)
    data = json.loads(out.read_text()) if out.is_file() else None
    return {"label": label, "exit": proc.returncode,
            "mismatch_count": (data or {}).get("mismatch_count"),
            "defects": (data or {}).get("defects"),
            "receipt": data}


def mutant_c1(lane: pathlib.Path, work: pathlib.Path, gate_rev: str,
              gate) -> dict:
    """Reconstruct `c1-rev-show-to-worktree` and ask what the gate sees."""
    source = pathlib.Path(lane, INSTRUMENTS["verdict-bind"]).read_text()
    old = (
        'def show(root: str, rev: str, path: str) -> str | None:\n'
        '    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],\n'
        '                          capture_output=True)\n'
        '    if proc.returncode != 0:\n'
        '        return None\n'
        '    return proc.stdout.decode("utf-8", "replace")\n')
    new = (
        'def show(root: str, rev: str, path: str) -> str | None:\n'
        '    # mutation: read the working tree, never the revision\n'
        '    target = pathlib.Path(root, path)\n'
        '    if not target.is_file():\n'
        '        return None\n'
        '    return target.read_text(encoding="utf-8", errors="replace")\n')
    if old not in source:
        raise Fatal("c1 mutation anchor not found - instrument drifted")
    mutant_path = pathlib.Path(work, "mut", "verdict-bind-worktree.py")
    mutant_path.parent.mkdir(parents=True, exist_ok=True)
    mutant_path.write_text(source.replace(old, new, 1))
    st = subprocess.run([sys.executable, "-I", "-B", str(mutant_path),
                         "--selftest"], capture_output=True, text=True,
                        env=child_env(work), cwd=work)
    selftest = {"exit": st.returncode, "stdout_tail": st.stdout.strip()[-500:]}

    demo = pathlib.Path(work, "demo-c1")
    if demo.exists():
        shutil.rmtree(demo)
    scores = ".ufo/waves/round-78/l1/scores"
    (demo / scores).mkdir(parents=True)
    (demo / "tools/round-77").mkdir(parents=True)
    (demo / "SCORECARD.md").write_text(
        "# demo scorecard\n\n## Capabilities\n\n"
        "| Capability | What it can now do | Evidence pointer | "
        "First-working round |\n|---|---|---|---|\n")
    # the true record at rev A: the receipt says 1, the cell claims 0
    (demo / scores / "r.json").write_text(json.dumps(
        {"mismatch_count": 1}, indent=1) + "\n")
    province_a = (
        "# demo province\n\n## Core\n\n"
        "- **Core — demo:** `.ufo/waves/round-78/l1/scores/r.json` records the "
        "verdict (mismatch_count 0).\n")
    (demo / "PROVINCE.md").write_text(province_a)
    shutil.copy2(mutant_path, demo / "tools/round-77/verdict-bind.py")
    rev_a = commit_all(demo, "demo: the true record at rev A", work)

    original = pathlib.Path(lane, INSTRUMENTS["verdict-bind"]).resolve()
    mutant_in_demo = demo / "tools/round-77/verdict-bind.py"
    runs = [
        run_vb(original, demo, rev_a, work,
               "original, at rev A, worktree clean", "c1-original-clean.json"),
        run_vb(mutant_in_demo, demo, rev_a, work,
               "mutant, at rev A, worktree clean", "c1-mutant-clean.json"),
    ]
    # the seat edits the worktree so the audit is clean, then files the receipt
    # it produced; `git show rev:path` would still have read the true record.
    (demo / "PROVINCE.md").write_text(
        province_a.replace("(mismatch_count 0)", "(mismatch_count 1)"))
    dirty = subprocess.run(["git", "-C", str(demo), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    emitted_run = run_vb(mutant_in_demo, demo, rev_a, work,
                         "mutant, at rev A, worktree dirty", "c1-mutant-dirty.json")
    emitted = emitted_run["receipt"] or {}
    pin_at_a = sha256_bytes(git_blob(demo, rev_a,
                                     INSTRUMENTS["verdict-bind"]))
    pin_ok = (emitted.get("instrument") or {}).get("sha256") == pin_at_a
    # file the emitted receipt under a new name and cite it at rev B
    (demo / scores / "e.json").write_text(json.dumps(emitted, indent=1) + "\n")
    (demo / "PROVINCE.md").write_text(
        "# demo province\n\n## Core\n\n"
        "- **Core — demo:** `.ufo/waves/round-78/l1/scores/e.json` records the "
        "verdict (mismatch_count 0).\n")
    rev_b = commit_all(demo, "demo: file the receipt, cite it at rev B", work)
    province_at_a = git_blob(demo, rev_a, "PROVINCE.md").decode()
    receipt_at_a = json.loads(git_blob(demo, rev_a, f"{scores}/r.json"))
    rerun_original_at_a = run_vb(original, demo, rev_a, work,
                                 "original, re-run at the receipt's own rev A",
                                 "c1-original-rerun-a.json")
    auth = gate.auth_findings(str(demo), rev_b, f"{scores}/e.json", emitted)
    scan = gate.scan_record(str(demo), rev_b,
                            {"receipt_auth", "value_mismatch",
                             "unbound_verdict", "qualified_atom",
                             "near_miss_field", "negated_verdict"})
    original_at_b = run_vb(original, demo, rev_b, work,
                           "original, at rev B, worktree clean",
                           "c1-original-b.json")
    return {
        "survivor": "c1-rev-show-to-worktree",
        "mutation": "verdict-bind.py show() reads the working tree instead of "
                    "`git show rev:path`",
        "selftest_on_mutant": selftest,
        "runs": runs + [emitted_run, original_at_b],
        "dirty_worktree_at_acceptance": dirty,
        "emitted_receipt": {k: emitted.get(k) for k in
                            ("rev", "mismatch_count", "population", "defects")},
        "emitted_pin_is_blob_at_its_rev": pin_ok,
        "receipt_it_audited": {"path": f"{scores}/r.json",
                               "blob_at_rev_a": receipt_at_a},
        "province_at_rev_a_claimed": "(mismatch_count 0)" in province_at_a,
        "provenance_contradiction": (
            bool(emitted.get("rev")) and emitted.get("rev") == rev_a
            and rerun_original_at_a["exit"] == 1),
        "rerun_original_at_receipt_rev": rerun_original_at_a,
        "rev_a": rev_a, "rev_b": rev_b,
        "round78_gate_rev": gate_rev,
        "round78_receipt_auth_on_emitted_receipt": auth,
        "round78_scan_record_at_b": {
            k: scan[k] for k in ("in_scope_cells", "groups", "bound_clauses",
                                 "mismatch_count", "findings")},
        "round78_sees_the_mutation": bool(auth) or bool(scan["findings"]),
    }


def mutant_c2(lane: pathlib.Path, work: pathlib.Path, gate) -> dict:
    """Reconstruct `c2-nonint-exit-accepted` and ask what the gate sees."""
    source = pathlib.Path(lane, INSTRUMENTS["prefile-receipt"]).read_text()
    old = (
        '    exit_code = receipt.get("exit")\n'
        '    if not isinstance(exit_code, int) or isinstance(exit_code, bool):\n'
        '        defects.append(f"exit is not an integer: {exit_code!r}")\n'
        '        return defects\n')
    new = (
        '    exit_code = receipt.get("exit")\n'
        '    # mutation: any present exit is accepted\n')
    if old not in source:
        raise Fatal("c2 mutation anchor not found - instrument drifted")
    mutant_path = pathlib.Path(work, "mut", "prefile-nonint.py")
    mutant_path.parent.mkdir(parents=True, exist_ok=True)
    mutant_path.write_text(source.replace(old, new, 1))
    st = subprocess.run([sys.executable, "-I", "-B", str(mutant_path),
                         "--selftest"], capture_output=True, text=True,
                        env=child_env(work), cwd=work)
    selftest = {"exit": st.returncode, "stdout_tail": st.stdout.strip()[-500:]}

    stdout = "prefile: tree clean\nprefile: PASS\n"
    base = {
        "rev": "a" * 40,
        "argv": ["bash", f"/lane/{GATE}", "/lane"],
        "passed": True, "prefile_line": "prefile: PASS", "stdout": stdout,
        "stdout_sha256": sha256_bytes(stdout.encode()),
        "env_keys": ["HOME", "LANG", "PATH", "TMPDIR"],
    }
    cases = {}
    for label, exit_value in (("float-0.0", 0.0), ("bool-false", False),
                              ("string-0", "0")):
        receipt = dict(base, exit=exit_value)
        path = pathlib.Path(work, "mut", f"c2-{label}.json")
        path.write_text(json.dumps(receipt, indent=1) + "\n")
        observed = {}
        for who, script in (
                ("frozen", pathlib.Path(
                    lane, INSTRUMENTS["prefile-receipt"]).resolve()),
                ("mutant", mutant_path)):
            proc = subprocess.run(
                [sys.executable, "-I", "-B", str(script),
                 "--check-receipt", str(path)],
                capture_output=True, text=True, env=child_env(work), cwd=work)
            observed[who] = {"exit": proc.returncode,
                             "defects": json.loads(proc.stdout)["defects"]}
        cases[label] = observed

    gate_copy = {label: gate.check_receipt_like(dict(base, exit=exit_value))
                 for label, exit_value in (("float-0.0", 0.0),
                                           ("bool-false", False),
                                           ("string-0", "0"))}
    demo = pathlib.Path(work, "demo-c2")
    if demo.exists():
        shutil.rmtree(demo)
    (demo / ".ufo/waves/round-78/l1/scores").mkdir(parents=True)
    bad = dict(base, exit="0", schema="kaidoku-r77-prefile-receipt-v1")
    (demo / ".ufo/waves/round-78/l1/scores/gate-bad.json").write_text(
        json.dumps(bad, indent=1) + "\n")
    rev = commit_all(demo, "demo: gate receipt with a string exit", work)
    findings = gate.judge_receipt_fixture(str(demo), rev, "gate_receipt_schema")
    return {
        "survivor": "c2-nonint-exit-accepted",
        "mutation": "check_receipt's `isinstance(exit, int) and not bool` guard "
                    "deleted",
        "selftest_on_mutant": selftest,
        "check_receipt_on_nonint_exit": cases,
        "round78_check_receipt_like": gate_copy,
        "round78_gate_receipt_schema_on_string_exit": findings,
        "round78_closes_the_shape_at_the_record": bool(gate_copy["string-0"])
                                                and bool(
            gate_copy["float-0.0"]) and bool(findings),
        "round77_selftest_still_13_cases": "cases: 13" in st.stdout
                                          or '"cases": 13' in st.stdout,
    }


def populations(lane: pathlib.Path, rev: str, work: pathlib.Path,
                gate) -> dict:
    out = pathlib.Path(work, "receipts", "lane-verdict-bind.json")
    run = run_instrument(lane, "verdict-bind", lane, rev, work, out)
    receipt = run["receipt"] or {}
    scan = gate.scan_record(str(lane), rev,
                            {"receipt_auth", "qualified_atom",
                             "near_miss_field", "negated_verdict",
                             "unbound_verdict"})
    return {
        "rev": rev,
        "verdict_bind": {"exit": run["exit"],
                         "mismatch_count": receipt.get("mismatch_count"),
                         "defects": receipt.get("defects"),
                         "population": receipt.get("population")},
        "round78_scan_record": {k: scan[k] for k in
                                ("in_scope_cells", "groups", "bound_clauses",
                                 "mismatch_count")},
        "round78_scan_record_findings": scan["findings"],
        "round78_scope": {"min_round": gate.SCOPE_MIN_ROUND,
                          "province_filter": "PROVINCE Core bullets naming "
                                             "tools/round-78/ or "
                                             ".ufo/waves/round-78/"},
        "verdict_bind_scope": {"min_round": 73,
                               "province_filter": "every `- **Core — ` bullet"},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--fixtures-rev", required=True)
    ap.add_argument("--gate-rev", required=True)
    ap.add_argument("--rev", help="record revision for the population block")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--populations", action="store_true")
    args = ap.parse_args(argv)
    lane = pathlib.Path(args.lane).resolve()
    work = pathlib.Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    head_before = git(lane, "rev-parse", "HEAD").stdout.strip()
    try:
        gate = load_gate(lane, args.gate_rev, work)
        data = probe(lane, work, args.fixtures_rev)
        data["instrument_pins"] = {
            p: sha256_bytes(git_blob(lane, args.gate_rev, p))
            for p in INSTRUMENTS.values()}
        data["instrument_worktree_pins"] = {
            p: sha256_bytes(pathlib.Path(lane, p).read_bytes())
            for p in INSTRUMENTS.values()}
        data["instruments_match_frozen"] = (
            data["instrument_pins"] == data["instrument_worktree_pins"])
        if args.mutants:
            data["survivors"] = [mutant_c1(lane, work, args.gate_rev, gate),
                                 mutant_c2(lane, work, gate)]
        if args.populations:
            data["populations"] = populations(
                lane, args.rev or head_before, work, gate)
    except Fatal as exc:
        print(json.dumps({"fatal": str(exc)}))
        return 2
    head_after = git(lane, "rev-parse", "HEAD").stdout.strip()
    data["lane"] = str(lane)
    data["head_before"] = head_before
    data["head_after"] = head_after
    data["head_moved_during_run"] = head_before != head_after
    pathlib.Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.json_out).write_text(json.dumps(data, indent=1,
                                                      sort_keys=True) + "\n")
    print(json.dumps({
        "classes": len(data["classes"]),
        "accepted": sum(1 for c in data["classes"] if c["accepted"]),
        "survivors": [s["survivor"] for s in data.get("survivors", [])],
        "head_moved": data["head_moved_during_run"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
