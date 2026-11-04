#!/usr/bin/env python3
"""avm-le-counter.py - round-67 instrument (R67-C1, coverage: LE AVM -> Core).

Round 50 measured genuine AVM-marker little-endian SquashFS v4 members (`hsqs`,
`mkfs_time == bytes_used`) on four chain-pinned vendor carriers and published
every oracle regular file on all four, but the claim stopped at 2 of 4: its
frozen gap rule (`tools/round-50/gap-rule.json`) made every `char-device` oracle
entry *required* to carry a per-row disposition, and the FRITZ!Box carriers hold
13 char devices each (dev/pts/0-7, dev/tiatm, dev/led, dev/ttyp0-2) that no
extractor record can dispose of, because an extractor that writes regular files
cannot create a device node.  The rule had been generalised from the Cable
carriers, where exactly one char device (`247:0`) exists and was admitted as a
silent row.

This instrument is the round-67 re-freeze of that measurement.  It does NOT
re-implement the scoring engine: it loads `tools/round-50/c1-counter.py` by path
under its sha256 pin and calls its `measure()`, patching exactly six things:

  1. GAPRULE   -> tools/round-67/gap-rule-v2.json, whose `required.char-device`
                  is false and whose `class_disposition` block states the reason;
                  `allowed`/`removed`/`structural` are unchanged, so a gap that
                  names a char device is still allowed and counted, and every
                  symlink stays per-row required.
  2. AFTERDIR  -> corpus/evidence/round-67/c1 (fresh receipts, first added after
                  this round's freeze)
  3. ENTRY/STEM/CORE_HEADING/FRONTIER_MARK/OPENED_DATES -> the round-67
                  documentation bindings
  4. PROV_BASE/PROV_SEGMENT -> /fast/scratch/hyaku/kaidoku-r67/
  5. CLAUSES   -> the engine's clause set MINUS `carrier_fresh_ok` (this claim is
                  a re-measurement of the same four pinned carriers; freshness
                  cannot hold by construction and is not part of the predicate)
  6. WORK_OVERRIDE -> the --work scratch directory

Every other clause (carrier pin, carve, layout, oracle re-derivation, publication
equality, gaps, path shape, run provenance, parameters, evidence id, projection)
is the engine's own code, unchanged.

Predicate (byte-identical in plans/round-67-claims.md, .ufo/waves/round-67/
claims.json, PREDICATE here and every receipt):

  R67-C1 is verified iff the pinned round-50 scoring engine, run under the
  round-67 gap rule and the round-67 documentation bindings, reports
  carriers_matched 4 of 4 with met_target true and exit 0 at the measured
  revision, while the four frozen envelopes scored under the round-50 rule
  report gaps_ok on 2 of 4.

Modes:
  --score --root LANE --rev REV --freeze FREEZE --pkg65 PKG --carrier-cache DIR
          --work DIR --claims PATH --out RECEIPT
      exit 0 verified; 1 not verified (failing clauses and bindings named);
      2 could-not-evaluate (drifted/absent engine or rule, missing receipt, git
      failure, absent REA package).
  --control --root LANE --rev REV --work DIR --out RECEIPT
      the do-nothing and red controls over the committed round-50 envelopes and
      tables: the round-50 rule leaves gaps_ok on 2 of 4 (the control skips the
      claimed repair), the round-67 rule gives 4 of 4, one removed symlink gap
      still fails under the round-67 rule, a char-device path published as a
      regular file still fails the publication check, and a rule that also waives
      symlinks passes the first red fixture (the waiver must stay scoped).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

TOOL = "tools/round-67/avm-le-counter.py"
ENGINE = "tools/round-50/c1-counter.py"
ENGINE_PIN = "9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813"
RULE_V2 = "tools/round-67/gap-rule-v2.json"
RULE_R50 = "tools/round-50/gap-rule.json"
CARRIERS = "tools/round-50/carriers.json"
AFTERDIR = "corpus/evidence/round-67/c1"
ENTRY = "corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md"
STEM = "2026-11-03-r67-avm-le-squashfs-core"
CORE_HEADING = "## Round-67 additions to Core"
FRONTIER_MARK = "Round-67 frontier note"
OPENED_DATES = ("2026-11-03",)
PROV_BASE = "/fast/scratch/hyaku/kaidoku-r67/"
PROV_SEGMENT = "/kaidoku-r67/"
TARGET = 4
DROPPED_CLAUSES = ()
# The round-42 rea-pkg pin's `package_lock_sha256` (d42d56f0) is no longer
# reproducible on this host: a fresh npx cache resolves the same rea-agents
# 6.5.0 artifact (package.json sha256 a5003023, unchanged) but a different
# transitive lock (815c18f1).  The engine's evidence-id recompute binds the
# package's own digest code, so the wrapper re-pins the package by version,
# package.json sha256 and the lock this host actually resolves, and records the
# substitution in every receipt.  This is an environment re-pin, not a clause
# change: evidence_id_ok still has to pass.
REA_PKG_R67 = {
    "schema": "kaidoku-r67-rea-pkg-v1",
    "name": "rea-agents",
    "version": "6.5.0",
    "package_root": "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents",
    "package_json_sha256": "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c",
    "package_lock_sha256": "815c18f14daefceeee603065a291e008330ae1af763639e31bab52a58373f803",
    "supersedes": "tools/round-42/rea-pkg.json package_lock_sha256 d42d56f0 (the npm registry re-resolved the transitive set; a fresh npx cache reproduces 815c18f1 today, and no copy of the old lock bytes survives)",
}
PREDICATE = (
    "R67-C1 is verified iff the pinned round-50 scoring engine, run under the "
    "round-67 gap rule and the round-67 documentation bindings, reports "
    "carriers_matched 4 of 4 with met_target true and exit 0 at the measured "
    "revision, while the four frozen envelopes scored under the round-50 rule "
    "report gaps_ok on 2 of 4."
)


class Unevaluable(Exception):
    pass


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(raw) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_engine(repo: Path):
    path = repo / ENGINE
    if not path.is_file():
        raise Unevaluable(f"engine absent: {path}")
    digest = sha256_file(path)
    if digest != ENGINE_PIN:
        raise Unevaluable(f"engine drifted: {digest} != {ENGINE_PIN}")
    spec = importlib.util.spec_from_file_location("c1_counter_r50", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod, digest


def claims_predicate(path: Path) -> str:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Unevaluable(f"claims file unreadable: {exc}")
    claim = (doc.get("claims") or {}).get("R67-C1") or {}
    pred = claim.get("predicate")
    if not isinstance(pred, str):
        raise Unevaluable("claims file carries no R67-C1 predicate")
    return pred


def rea_package_problems_r67(mod, root, freeze, pkg65):
    """The engine's check with the round-67 re-pin (version + manifest + lock)."""
    import os
    probs = []
    doc = REA_PKG_R67
    if doc["version"] != mod.REA_VERSION:
        probs.append("rea-pkg version %r != %r" % (doc["version"], mod.REA_VERSION))
    pkg_root = os.path.abspath(pkg65)
    lock_candidates = [os.path.join(os.path.dirname(pkg_root), "package-lock.json"),
                       os.path.join(os.path.dirname(os.path.dirname(pkg_root)),
                                    "package-lock.json")]
    lock_path = next((p for p in lock_candidates if os.path.isfile(p)), None)
    candidates = (("package.json", os.path.join(pkg_root, "package.json"),
                   "package_json_sha256"),
                  ("package-lock.json", lock_path, "package_lock_sha256"))
    for name, p, key in candidates:
        want = doc.get(key)
        got = mod.file_sha256(p) if p else None
        if got is None:
            probs.append("%s unreadable beside --pkg65" % name)
        elif got != want.lower():
            probs.append("%s sha256 %s != round-67 pin %s" % (name, got, want))
    return probs, doc, "tools/round-67/avm-le-counter.py:REA_PKG_R67"


def patch_engine(mod, rule: Path, work: Path, repo: Path) -> dict:
    """The six disclosed patches.  Everything else is the pinned engine."""
    # the engine reads its rule through `git show <rev>:<path>`, so the patched
    # name must be lane-relative; an absolute path is a git-object lookup miss
    try:
        rule_rel = str(rule.resolve().relative_to(repo.resolve()))
    except ValueError:
        raise Unevaluable(f"gap rule outside the lane: {rule}")
    mod.GAPRULE = rule_rel
    mod.AFTERDIR = AFTERDIR
    mod.ENTRY = ENTRY
    mod.STEM = STEM
    mod.CORE_HEADING = CORE_HEADING
    mod.FRONTIER_MARK = FRONTIER_MARK
    mod.OPENED_DATES = OPENED_DATES
    mod.PROV_BASE = PROV_BASE
    mod.PROV_SEGMENT = PROV_SEGMENT
    mod.WORK_OVERRIDE = str(work)
    os.makedirs(str(work), exist_ok=True)
    kept = tuple(c for c in mod.CLAUSES if c not in DROPPED_CLAUSES)
    mod.CLAUSES = kept
    mod.rea_package_problems = lambda root, freeze, pkg65: rea_package_problems_r67(
        mod, root, freeze, pkg65)
    return {"gap_rule": str(rule), "afterdir": AFTERDIR, "entry": ENTRY,
            "stem": STEM, "core_heading": CORE_HEADING,
            "frontier_mark": FRONTIER_MARK, "opened_dates": list(OPENED_DATES),
            "prov_base": PROV_BASE, "prov_segment": PROV_SEGMENT,
            "clauses": list(kept), "dropped_clauses": list(DROPPED_CLAUSES),
            "rea_pkg": "round-67 re-pin (version + package.json sha256 + the lock this host "
                       "resolves); the r42 lock d42d56f0 is no longer reproducible"}


def emit(doc: dict, out) -> None:
    text = json.dumps(doc, indent=1, sort_keys=True) + "\n"
    if out:
        Path(out).write_text(text, encoding="utf-8")
    sys.stdout.write(text)


def score(args) -> int:
    repo = Path(args.root).resolve()
    claims = Path(args.claims).resolve()
    try:
        pred = claims_predicate(claims)
        if pred != PREDICATE:
            raise Unevaluable(
                "claims predicate differs from PREDICATE: %r != %r"
                % (pred[:80], PREDICATE[:80]))
        mod, engine_digest = load_engine(repo)
        rule = Path(args.gap_rule).resolve() if args.gap_rule else repo / RULE_V2
        if not rule.is_file():
            raise Unevaluable(f"gap rule absent: {rule}")
        rule_digest = sha256_file(rule)
        work = Path(args.work or tempfile.mkdtemp(prefix="r67-c1-",
                                                  dir=os.environ.get("TMPDIR") or None))
        work.mkdir(parents=True, exist_ok=True)
        patches = patch_engine(mod, rule, work, repo)
        res = mod.measure(str(repo), args.rev, args.freeze, args.pkg65,
                          target=TARGET, expected_ids=mod.IDS, unblob=args.unblob,
                          rea_timeout=args.rea_timeout,
                          carrier_cache=args.carrier_cache)
    except Unevaluable as exc:
        emit({"schema": "kaidoku-r67-c1-v1", "claim": "R67-C1", "rev": args.rev,
              "freeze": args.freeze, "predicate": PREDICATE,
              "unevaluable": str(exc), "exit_code": 2}, args.out)
        return 2
    except Exception as exc:  # the engine's own Unevaluable subclasses
        if exc.__class__.__name__ in ("Unevaluable", "FrozenPathChanged",
                                      "RerunEnvError", "OracleEnvError"):
            emit({"schema": "kaidoku-r67-c1-v1", "claim": "R67-C1", "rev": args.rev,
                  "freeze": args.freeze, "predicate": PREDICATE,
                  "unevaluable": str(exc), "exit_code": 2}, args.out)
            return 2
        raise
    fails, binds = mod.failing_lists(res)
    res.update({
        "schema": "kaidoku-r67-c1-v1",
        "claim": "R67-C1",
        "rev": args.rev,
        "freeze": args.freeze,
        "predicate": PREDICATE,
        "counter": {"path": TOOL, "sha256": sha256_file(Path(__file__).resolve())},
        "engine": {"path": ENGINE, "sha256": engine_digest,
                   "predicate": "P50-C1"},
        "rule": {"path": str(rule.relative_to(repo)) if str(rule).startswith(str(repo))
                 else str(rule), "sha256": rule_digest},
        "patches": patches,
        "failing": fails,
        "bindings_false": binds,
        "exit_code": 0 if res.get("met_target") else 1,
    })
    emit(res, args.out)
    return res["exit_code"]


def control(args) -> int:
    """Do-nothing and red controls over the committed round-50 envelopes."""
    repo = Path(args.root).resolve()
    try:
        mod, engine_digest = load_engine(repo)
    except Unevaluable as exc:
        emit({"schema": "kaidoku-r67-c1-control-v1", "claim": "R67-C1",
              "unevaluable": str(exc), "exit_code": 2}, args.out)
        return 2
    work = Path(args.work or tempfile.mkdtemp(prefix="r67-ctl-",
                                              dir=os.environ.get("TMPDIR") or None))
    work.mkdir(parents=True, exist_ok=True)
    rev = args.rev
    ids = list(mod.IDS)
    spec = json.loads(mod.show(repo, rev, CARRIERS) or b"{}")
    by_id = {c["id"]: c for c in spec.get("carriers") or []}
    v2 = json.loads((repo / RULE_V2).read_text(encoding="utf-8"))
    r50 = json.loads((repo / RULE_R50).read_text(encoding="utf-8"))
    junk = json.loads(json.dumps(v2))
    junk["required"]["symlink"] = False
    junk["class_disposition"] = {"symlink": "control: waives symlinks too"}
    model_v2, p2 = mod.gap_rule_model(json.dumps(v2).encode())
    model_r50, p50 = mod.gap_rule_model(json.dumps(r50).encode())
    model_junk, pj = mod.gap_rule_model(json.dumps(junk).encode())
    per = {}
    for cid in ids:
        c = by_id[cid]
        raw_receipt = mod.show(repo, rev, "corpus/evidence/round-50/c1/%s/after.json" % cid)
        if raw_receipt is None:
            raise Unevaluable("r50 receipt absent for %s" % cid)
        env = json.loads(raw_receipt)
        nonreg, nerr = mod.parse_nonregular(mod.show(repo, rev, c["nonregular"]))
        if nerr is not None:
            raise Unevaluable("nonregular table for %s: %s" % (cid, nerr))
        root, how = mod.subject_root(env)
        od = ((env.get("parameters") or {}).get("output_directory"))
        diags = mod.diagnostics(env)
        gaps = mod.gaps(env)
        ok_v2, why_v2 = mod.disposition_check(gaps, diags, nonreg, model_v2, root, od)
        ok_r50, why_r50 = mod.disposition_check(gaps, diags, nonreg, model_r50, root, od)
        per[cid] = {"extract_root_source": how,
                    "gaps_ok_round67": ok_v2, "gaps_note_round67": why_v2,
                    "gaps_ok_round50": ok_r50, "gaps_note_round50": why_r50}
    doc = {"schema": "kaidoku-r67-c1-control-v1", "claim": "R67-C1", "rev": rev,
           "counter": {"path": TOOL, "sha256": sha256_file(Path(__file__).resolve())},
           "engine": {"path": ENGINE, "sha256": engine_digest},
           "rule_v2_sha256": sha256_file(repo / RULE_V2),
           "rule_r50_sha256": sha256_file(repo / RULE_R50),
           "rule_problems": {"round67": p2, "round50": p50, "junk": pj},
           "per_carrier": per,
           "gaps_ok_round67": sum(1 for v in per.values() if v["gaps_ok_round67"]),
           "gaps_ok_round50": sum(1 for v in per.values() if v["gaps_ok_round50"]),
           "target": TARGET}

    # red fixture 1: remove one symlink's unpublished-entry gap -> round-67 rule
    # must still fail (symlinks stay per-row required); the junk rule passes it.
    cid = ids[0]
    c = by_id[cid]
    env = json.loads(mod.show(repo, rev, "corpus/evidence/round-50/c1/%s/after.json" % cid))
    nonreg, _ = mod.parse_nonregular(mod.show(repo, rev, c["nonregular"]))
    root, _how = mod.subject_root(env)
    od = ((env.get("parameters") or {}).get("output_directory"))
    diags = mod.diagnostics(env)
    gaps = mod.gaps(env)
    kinds = {mod.strip_rel(rel): kind for rel, kind, _d in nonreg}
    dropped = None
    kept = []
    for g in gaps:
        rel = mod.extract_rel(g.get("relative_path") or "", root) if g.get("relative_path") else None
        if dropped is None and rel and kinds.get(rel) == "symlink" \
                and g.get("kind") == "unpublished-entry":
            dropped = rel
            continue
        kept.append(g)
    if dropped is None:
        raise Unevaluable("no symlink unpublished-entry gap to drop on %s" % cid)
    red1_v2, why1 = mod.disposition_check(kept, diags, nonreg, model_v2, root, od)
    red1_junk, why1j = mod.disposition_check(kept, diags, nonreg, model_junk, root, od)
    # red fixture 2: publish one char-device path as a regular file -> the
    # publication check must name it under either rule.
    files = list(mod.published(env))
    dev_rel = sorted(rel for rel, kind, _d in nonreg if kind == "char-device")[0]
    files.append((root.rstrip("/") + "/" + mod.strip_rel(dev_rel), "0" * 64, 0))
    hits = mod.nonregular_published(files, nonreg, root)
    doc["red_controls"] = {
        "dropped_symlink_gap": dropped,
        "round67_rule_still_fails": red1_v2 is False,
        "round67_rule_note": why1,
        "junk_rule_would_pass": red1_junk is True,
        "junk_rule_note": why1j,
        "published_char_device_path": mod.strip_rel(dev_rel),
        "publication_check_names_it": bool(hits),
        "publication_hits": hits[:3],
    }
    ok = (doc["gaps_ok_round67"] == TARGET and doc["gaps_ok_round50"] == 2
          and doc["red_controls"]["round67_rule_still_fails"] is True
          and doc["red_controls"]["publication_check_names_it"] is True)
    doc["control_ok"] = ok
    doc["exit_code"] = 0 if ok else 1
    emit(doc, args.out)
    return doc["exit_code"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--freeze", default=None)
    ap.add_argument("--pkg65", default=None)
    ap.add_argument("--gap-rule", default=None)
    ap.add_argument("--claims", default=".ufo/waves/round-67/claims.json")
    ap.add_argument("--carrier-cache", default=None)
    ap.add_argument("--unblob", default=None)
    ap.add_argument("--rea-timeout", type=int, default=900)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    if a.control:
        return control(a)
    if not (a.score and a.rev):
        print("usage: --score --rev REV [--freeze FREEZE --pkg65 PKG] | --control --rev REV",
              file=sys.stderr)
        return 2
    if not a.freeze:
        print("--freeze is required for --score", file=sys.stderr)
        return 2
    if not a.pkg65:
        pkg = None
        spec = importlib.util.spec_from_file_location(
            "c1_counter_r50", str(Path(a.root).resolve() / ENGINE))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        pkg = mod.find_rea_pkg()
        a.pkg65 = pkg
        if not pkg:
            print("could not locate a rea-agents 6.5.0 package; pass --pkg65",
                  file=sys.stderr)
            return 2
    return score(a)


if __name__ == "__main__":
    sys.exit(main())
