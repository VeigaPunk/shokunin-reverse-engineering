#!/usr/bin/env python3
"""Independent re-derivation of a REA evidence_id from an envelope JSON file.

Python re-implementation of rea-agents id function (read from the pinned package):
  dist/domain/evidence.js:129-152  semanticProjection()
  dist/domain/canonicalDigest.js:11-86  digestCanonicalValue()  (RFC 8785 canonical JSON, sha256)

Usage: python3 reid.py <envelope.json>
Prints canonical byte length, derived id, recorded id, MATCH/MISMATCH.
"""
import hashlib
import json
import sys


def _js_number(value: float) -> str:
    """ECMAScript Number::toString-ish for JSON.stringify (shortest round-trip)."""
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("NaN/Infinity not allowed")
    if value == int(value) and abs(value) < 1e21:
        return str(int(value))
    r = repr(value)
    if "e" in r:
        mant, exp = r.split("e")
        exp_i = int(exp)
        return f"{mant}e{'+' if exp_i >= 0 else '-'}{abs(exp_i)}"
    return r


def _key_sort(key: str) -> bytes:
    """RFC 8785 / JS Object.keys().sort(): UTF-16 code-unit order."""
    return key.encode("utf-16-be")


def canon(value) -> str:
    if value is None or isinstance(value, (bool, int, str)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, float):
        return _js_number(value)
    if isinstance(value, list):
        return "[" + ",".join(canon(v) for v in value) + "]"
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda kv: _key_sort(kv[0]))
        return "{" + ",".join(
            json.dumps(k, ensure_ascii=False) + ":" + canon(v) for k, v in items
        ) + "}"
    raise TypeError(f"unsupported type: {type(value)}")


def semantic_projection(ev: dict) -> dict:
    subject = ev.get("subject")
    return {
        "subject": None if subject is None else {
            "digest": subject.get("digest"),
            "format": subject.get("format"),
            "architecture": subject.get("architecture"),
        },
        "provider": ev.get("provider"),
        "analysis_profile": ev.get("analysis_profile"),
        "predicate_type": ev.get("predicate_type"),
        "operation": ev.get("operation"),
        "parameters": ev.get("parameters"),
        "raw_result": ev.get("raw_result"),
        "normalized_result": ev.get("normalized_result"),
        "confidence": ev.get("confidence"),
        "authority": ev.get("authority"),
        "environment": ev.get("environment"),
        "limitations": ev.get("limitations"),
        # rea-agents >= 6.5.0 hashes relationship_coverage; 6.4.0 does not.
        **({"relationship_coverage": ev.get("relationship_coverage")}
           if "relationship_coverage" in ev else {}),
        "locations": ev.get("locations"),
        "evidence_links": ev.get("evidence_links"),
    }


def derive(ev: dict) -> tuple:
    body = canon(semantic_projection(ev))
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return "ev_" + digest, len(body.encode("utf-8"))


def main() -> int:
    path = sys.argv[1]
    with open(path, "rb") as fh:
        ev = json.loads(fh.read().decode("utf-8"))
    if isinstance(ev, dict) and "evidence_bundle" in ev:
        ev = ev["evidence_bundle"]["records"][0]
    derived, nbytes = derive(ev)
    recorded = ev.get("evidence_id")
    print(f"canonical_bytes: {nbytes}")
    print(f"derived:  {derived}")
    print(f"recorded: {recorded}")
    print("MATCH" if derived == recorded else "MISMATCH")
    return 0 if derived == recorded else 1


if __name__ == "__main__":
    raise SystemExit(main())
