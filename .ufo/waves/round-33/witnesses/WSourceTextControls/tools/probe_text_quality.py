#!/usr/bin/env python3
"""Bounded TEXT-quality probe: drives measure_driver.check_document_spec over a Source.

Scratch evidence only. Not a carrier measurement, not R33-C1, no classifier, no binary fixture.
"""

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import sys


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_driver(path):
    spec = importlib.util.spec_from_file_location("measure_driver_pinned", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--driver", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--spec", required=True, help="repo-relative document spec path")
    ap.add_argument("--spec-sha256", default=None)
    ap.add_argument("--case", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    started = utc_now()
    md = load_driver(a.driver)
    receipt = {
        "case": a.case,
        "probe": "measure_driver.check_document_spec",
        "scope": "text-quality probe over Source; not a carrier/claim measurement",
        "argv": [sys.executable, "-I", "-B", os.path.abspath(__file__)] + list(argv),
        "driver": {"path": os.path.abspath(a.driver), "sha256": sha256_file(a.driver)},
        "started_utc": started,
        "source": {"repo": os.path.abspath(a.repo), "rev": a.rev, "commit": None},
        "spec_path": a.spec,
        "spec_sha256_arg": a.spec_sha256,
        "docs_ok": None,
        "checks": [],
        "exit": None,
        "refusal": None,
    }
    try:
        src = md.Source(a.repo, a.rev)
        receipt["source"]["commit"] = src.commit
        raw = src.read(a.spec)
        receipt["spec_sha256_observed"] = md.sha256(raw)
        res = md.check_document_spec(raw, a.spec_sha256, src)
        receipt["docs_ok"] = res["docs_ok"]
        receipt["checks"] = res["checks"]
        receipt["check_count"] = len(res["checks"])
        receipt["ok_count"] = sum(1 for c in res["checks"] if c["ok"])
        failed = [c for c in res["checks"] if not c["ok"]]
        receipt["fail_count"] = len(failed)
        receipt["failures"] = [{"kind": c["kind"], "path": c["path"], "detail": c["detail"]} for c in failed]
        receipt["by_kind"] = {}
        for c in res["checks"]:
            bucket = receipt["by_kind"].setdefault(c["kind"], {"total": 0, "ok": 0})
            bucket["total"] += 1
            bucket["ok"] += 1 if c["ok"] else 0
        receipt["exit"] = 0 if res["docs_ok"] else 1
    except md.Refuse as e:
        receipt["refusal"] = str(e)
        receipt["exit"] = 2
    except FileNotFoundError as e:
        receipt["refusal"] = "input unreadable: %s" % e
        receipt["exit"] = 2
    receipt["ended_utc"] = utc_now()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({
        "case": a.case,
        "exit": receipt["exit"],
        "docs_ok": receipt["docs_ok"],
        "check_count": receipt.get("check_count"),
        "fail_count": receipt.get("fail_count"),
        "failures": receipt.get("failures"),
        "refusal": receipt.get("refusal"),
        "source_commit": receipt["source"]["commit"],
        "spec_sha256": receipt.get("spec_sha256_observed"),
        "out": a.out,
    }, indent=2))
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
