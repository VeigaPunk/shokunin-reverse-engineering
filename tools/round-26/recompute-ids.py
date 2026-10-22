#!/usr/bin/env python3
"""Recompute rea-agents 6.5.0 evidence ids from saved envelopes.

Reimplements the minting function found in the installed 6.5.0 package:

  dist/domain/evidence.js:156  semanticProjection(evidence)
  dist/domain/evidence.js:182  computeEvidenceId = "ev_" + digestCanonicalValue(projection)
  dist/domain/canonicalDigest.js:7  digestCanonicalValue = sha256 over canonical JSON

Only the standard library is used. Canonical JSON follows the JS emitter in
dist/domain/canonicalDigest.js (RFC 8785 style: object keys ordered by UTF-16
code unit, arrays in order, JSON string escapes of JSON.stringify).

Usage:
  recompute-ids.py ENVELOPE [ENVELOPE ...]
  recompute-ids.py --dir DIR        (all *.json / *.json.gz under DIR)
  recompute-ids.py --all            (the known wave-26 seat envelope roots)

Exit code 0 when every envelope matches, 1 on any mismatch, 2 on input error.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import sys

# ---------------------------------------------------------------- canonical JSON


def _js_number(value):
    """Format a number the way JSON.stringify does."""
    if isinstance(value, bool):
        raise TypeError("bool is not a number here")
    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        raise ValueError("non-finite number")
    if value == int(value) and abs(value) < 1e21:
        return str(int(value))
    text = repr(float(value))
    if "e" in text or "E" in text:
        mantissa, _, exponent = text.partition("e")
        if not exponent:
            mantissa, _, exponent = text.partition("E")
        sign = ""
        if exponent.startswith("-"):
            sign = "-"
            exponent = exponent[1:]
        elif exponent.startswith("+"):
            exponent = exponent[1:]
        exponent = exponent.lstrip("0") or "0"
        text = mantissa + "e" + sign + exponent
    return text


def _js_string(value):
    """Format a string the way JSON.stringify does."""
    out = ['"']
    for char in value:
        code = ord(char)
        if char == '"':
            out.append('\\"')
        elif char == "\\":
            out.append("\\\\")
        elif char == "\b":
            out.append("\\b")
        elif char == "\f":
            out.append("\\f")
        elif char == "\n":
            out.append("\\n")
        elif char == "\r":
            out.append("\\r")
        elif char == "\t":
            out.append("\\t")
        elif code < 0x20:
            out.append("\\u%04x" % code)
        elif 0xD800 <= code <= 0xDFFF:
            # Lone surrogate: JSON.stringify emits an escaped surrogate.
            out.append("\\u%04x" % code)
        else:
            out.append(char)
    out.append('"')
    return "".join(out)


def _utf16_key(text):
    """Sort key reproducing JavaScript's default string ordering (UTF-16 units)."""
    return text.encode("utf-16-be", "surrogatepass")


def canonical_json(value):
    """Canonical JSON exactly as emitCanonical in canonicalDigest.js writes it."""
    parts = []

    def emit(text):
        parts.append(text)

    def walk(node):
        if node is None:
            emit("null")
            return
        if isinstance(node, bool):
            emit("true" if node else "false")
            return
        if isinstance(node, str):
            emit(_js_string(node))
            return
        if isinstance(node, (int, float)):
            emit(_js_number(node))
            return
        if isinstance(node, list):
            emit("[")
            for index, item in enumerate(node):
                if index > 0:
                    emit(",")
                walk(item)
            emit("]")
            return
        if isinstance(node, dict):
            emit("{")
            first = True
            for key in sorted(node.keys(), key=_utf16_key):
                item = node[key]
                if item is None and key in node and not isinstance(item, (dict, list)):
                    # JSON null is a real value and must be kept.
                    pass
                if not first:
                    emit(",")
                first = False
                emit(_js_string(key))
                emit(":")
                walk(item)
            emit("}")
            return
        raise TypeError("unsupported value type: %r" % type(node))

    walk(value)
    return "".join(parts)


def digest_canonical_value(value):
    """sha256 hex digest of the canonical JSON encoding."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- projection


def semantic_projection(evidence):
    """Mirror of semanticProjection in dist/domain/evidence.js (6.5.0)."""
    subject = evidence.get("subject")
    if subject is None:
        projected_subject = None
    else:
        projected_subject = {
            "digest": subject.get("digest"),
            "format": subject.get("format"),
            "architecture": subject.get("architecture"),
        }
    projection = {
        "subject": projected_subject,
        "provider": evidence.get("provider"),
        "analysis_profile": evidence.get("analysis_profile"),
        "predicate_type": evidence.get("predicate_type"),
        "operation": evidence.get("operation"),
        "parameters": evidence.get("parameters"),
        "raw_result": evidence.get("raw_result"),
        "normalized_result": evidence.get("normalized_result"),
        "confidence": evidence.get("confidence"),
        "authority": evidence.get("authority"),
        "environment": evidence.get("environment"),
        "limitations": evidence.get("limitations"),
    }
    coverage = evidence.get("relationship_coverage")
    if coverage is not None:
        projection["relationship_coverage"] = coverage
    projection["locations"] = evidence.get("locations")
    projection["evidence_links"] = evidence.get("evidence_links")
    return projection


def compute_evidence_id(evidence):
    """Mirror of computeEvidenceId in dist/domain/evidence.js (6.5.0)."""
    return "ev_" + digest_canonical_value(semantic_projection(evidence))


# ---------------------------------------------------------------- envelopes


def load_envelope(path):
    """Return (envelope_dict, source_bytes_sha256)."""
    if path.endswith(".gz"):
        with gzip.open(path, "rb") as handle:
            raw = handle.read()
    else:
        with open(path, "rb") as handle:
            raw = handle.read()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


def evidence_record(envelope):
    """Extract the Evidence record from a CLI envelope or a bare record."""
    if isinstance(envelope, dict) and "evidence_id" in envelope and "operation" in envelope:
        return envelope
    if isinstance(envelope, dict) and isinstance(envelope.get("data"), dict):
        return envelope["data"]
    raise ValueError("no Evidence record found in envelope")


def path_fields(value, prefix=""):
    """Collect JSON pointer-ish paths of string values that look like filesystem paths."""
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            found.extend(path_fields(item, prefix + "/" + str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(path_fields(item, prefix + "/" + str(index)))
    elif isinstance(value, str):
        if value.startswith("/") and len(value) > 1:
            found.append((prefix, value))
    return found


def check(path, verbose=False):
    """Recompute one envelope's id. Returns (ok, detail_lines)."""
    lines = []
    try:
        envelope, envelope_sha = load_envelope(path)
    except Exception as cause:  # noqa: BLE001 - report every read/parse failure
        return False, ["READ-OR-PARSE-ERROR %s: %s" % (path, cause)]
    try:
        record = evidence_record(envelope)
    except Exception as cause:  # noqa: BLE001
        return False, ["NO-RECORD %s: %s" % (path, cause)]
    stored = record.get("evidence_id")
    try:
        recomputed = compute_evidence_id(record)
    except Exception as cause:  # noqa: BLE001
        return False, ["RECOMPUTE-ERROR %s: %s" % (path, cause)]
    ok = recomputed == stored
    lines.append("MATCH" if ok else "MISMATCH")
    lines.append("  path        : %s" % path)
    lines.append("  envelope_sha: %s" % envelope_sha)
    lines.append("  operation   : %s" % record.get("operation"))
    lines.append("  stored_id   : %s" % stored)
    lines.append("  recomputed  : %s" % recomputed)
    projection = semantic_projection(record)
    paths = path_fields(projection)
    if paths:
        lines.append("  path-bearing fields in the hashed projection:")
        for pointer, value in paths:
            lines.append("    %s = %s" % (pointer or "/", value))
    else:
        lines.append("  path-bearing fields in the hashed projection: none")
    if verbose:
        canonical = canonical_json(projection)
        lines.append("  canonical_len: %d bytes" % len(canonical.encode("utf-8")))
    return ok, lines


def iter_dir(directory):
    for root, _dirs, files in os.walk(directory):
        for name in sorted(files):
            if name.endswith(".json") or name.endswith(".json.gz"):
                yield os.path.join(root, name)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Recompute rea-agents 6.5.0 evidence ids.")
    parser.add_argument("envelopes", nargs="*", help="envelope paths")
    parser.add_argument("--dir", action="append", default=[], help="scan a directory tree")
    parser.add_argument("--verbose", action="store_true", help="extra diagnostics")
    args = parser.parse_args(argv)

    targets = list(args.envelopes)
    for directory in args.dir:
        targets.extend(iter_dir(directory))
    if not targets:
        parser.error("no envelope given")

    matches = 0
    total = 0
    for target in targets:
        total += 1
        ok, lines = check(target, args.verbose)
        if ok:
            matches += 1
        print("\n".join(lines))
    print("")
    print("recomputed ids: %d match of %d total" % (matches, total))
    return 0 if matches == total else 1


if __name__ == "__main__":
    sys.exit(main())
