#!/usr/bin/env python3
"""recompute_evidence_id.py — pure-stdlib recomputation of a REA 6.5.0 `evidence_id`.

Derived from the installed package (not guessed):
  rea-agents@6.5.0  dist/domain/evidence.js:182
      computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`
  rea-agents@6.5.0  dist/cli-runtime/reconstructionObligationLedgerSchemas-*.js:30-92 (emitCanonical)
      canonical JSON = object keys sorted by JS code-unit order, no whitespace, primitives via
      JSON.stringify semantics (non-ASCII emitted literally), arrays in index order.

`semanticProjection` (evidence.js:161-181) keeps subject.{digest,format,architecture} (dropping
subject.name and subject.local_path), provider, analysis_profile, predicate_type, operation,
parameters, raw_result, normalized_result, confidence, authority, environment, limitations,
relationship_coverage (only when not null), locations, evidence_links.

usage: recompute_evidence_id.py FILE...   FILE may be a whole `{ok,data,meta}` envelope or the
       `data` object (an after.json).  Prints one TSV row per file; exit 0 when every file
       matches, 1 otherwise.
"""
import hashlib
import json
import sys


def canon(v):
    if v is None or not isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, allow_nan=False)
    if isinstance(v, list):
        return "[" + ",".join(canon(x) for x in v) + "]"
    return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + canon(v[k])
                          for k in sorted(v)) + "}"


def projection(e):
    s = e.get("subject")
    p = {
        "subject": None if s is None else {"digest": s["digest"], "format": s["format"],
                                           "architecture": s["architecture"]},
        "provider": e["provider"],
        "analysis_profile": e.get("analysis_profile"),
        "predicate_type": e.get("predicate_type"),
        "operation": e.get("operation"),
        "parameters": e.get("parameters"),
        "raw_result": e.get("raw_result"),
        "normalized_result": e.get("normalized_result"),
        "confidence": e.get("confidence"),
        "authority": e.get("authority"),
        "environment": e.get("environment"),
        "limitations": e.get("limitations"),
        "locations": e.get("locations"),
        "evidence_links": e.get("evidence_links"),
    }
    if e.get("relationship_coverage") is not None:
        p["relationship_coverage"] = e["relationship_coverage"]
    return p


def evidence_data(path):
    d = json.load(open(path))
    return d["data"] if isinstance(d, dict) and "data" in d and isinstance(d["data"], dict) else d


if __name__ == "__main__":
    bad = 0
    print("file\trecomputed\trecorded\tverdict")
    for path in sys.argv[1:]:
        data = evidence_data(path)
        want = data.get("evidence_id")
        got = "ev_" + hashlib.sha256(canon(projection(data)).encode()).hexdigest()
        ok = got == want
        bad += 0 if ok else 1
        print("%s\t%s\t%s\t%s" % (path, got, want, "MATCH" if ok else "MISMATCH"))
    sys.exit(0 if bad == 0 else 1)
