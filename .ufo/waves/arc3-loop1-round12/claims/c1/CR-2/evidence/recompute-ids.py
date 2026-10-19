from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def semantic_projection(data: dict) -> dict:
    subject = data["subject"]
    return {
        "subject": None if subject is None else {
            "digest": subject["digest"],
            "format": subject["format"],
            "architecture": subject["architecture"],
        },
        "provider": data["provider"],
        "analysis_profile": data["analysis_profile"],
        "predicate_type": data["predicate_type"],
        "operation": data["operation"],
        "parameters": data["parameters"],
        "raw_result": data["raw_result"],
        "normalized_result": data["normalized_result"],
        "confidence": data["confidence"],
        "authority": data["authority"],
        "environment": data["environment"],
        "limitations": data["limitations"],
        "relationship_coverage": data["relationship_coverage"],
        "locations": data["locations"],
        "evidence_links": data["evidence_links"],
    }


def absolute_path_strings(value):
    if isinstance(value, str):
        if value.startswith("/"):
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from absolute_path_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from absolute_path_strings(item)


def path_named_fields(value, prefix="$"):
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from path_named_fields(item, f"{prefix}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            location = f"{prefix}.{key}"
            if "path" in key.lower():
                yield location
            yield from path_named_fields(item, location)


def main() -> None:
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    names = ("base.json", "copy-a.json", "copy-b.json")
    envelopes = [json.loads((directory / name).read_text()) for name in names]
    assert all(envelope["ok"] is True for envelope in envelopes)
    rows = [envelope["data"] for envelope in envelopes]
    assert all(row["operation"] == "analyze_function" for row in rows)
    assert all(row["parameters"] == {"procedure": "0x1091f0"} for row in rows)
    assert all(row["provider"]["version"] == "12.1.4" for row in rows)
    assert all(row["subject"]["digest"]["sha256"] == rows[0]["subject"]["digest"]["sha256"] for row in rows)
    projections = [semantic_projection(row) for row in rows]
    canonical = [json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) for value in projections]
    assert all(text.isascii() for text in canonical)
    recomputed = ["ev_" + hashlib.sha256(text.encode("utf-8")).hexdigest() for text in canonical]
    reported = [row["evidence_id"] for row in rows]
    assert recomputed == reported
    assert len(set(recomputed)) == 1
    assert len(set(canonical)) == 1
    changed_display = dict(rows[0])
    changed_display["subject"] = {**rows[0]["subject"], "name": "renamed-display-only", "local_path": "/display-only/renamed-jq"}
    display_projection = json.dumps(semantic_projection(changed_display), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    assert display_projection == canonical[0]
    semantic_paths = sorted({path for projection in projections for path in absolute_path_strings(projection)})
    semantic_path_fields = sorted({field for projection in projections for field in path_named_fields(projection)})
    assert not semantic_paths
    assert not semantic_path_fields
    print("operation=analyze_function")
    print("rea_version=6.7.0")
    print("ghidra_provider_version=12.1.4")
    print(f"procedure={rows[0]['parameters']['procedure']} name={rows[0]['normalized_result']['procedure']['name']}")
    print(f"target_sha256={rows[0]['subject']['digest']['sha256']}")
    print("subject_paths=" + json.dumps([row["subject"]["local_path"] for row in rows], separators=(",", ":")))
    print("reported_ids=" + json.dumps(reported, separators=(",", ":")))
    print("recomputed_ids=" + json.dumps(recomputed, separators=(",", ":")))
    print("canonical_projection_sha256=" + hashlib.sha256(canonical[0].encode("utf-8")).hexdigest())
    print(f"projection_equal_across_calls={len(set(canonical)) == 1}")
    print(f"display_only_subject_change_preserves_projection={display_projection == canonical[0]}")
    print("path_named_fields_in_semantic_projection=" + json.dumps(semantic_path_fields, separators=(",", ":")))
    print("absolute_paths_in_semantic_projection=" + json.dumps(semantic_paths, separators=(",", ":")))
    print("verdict=REPRODUCED_PATH_STABLE_FOR_THIS_VERB_TARGET_CALL_SHAPE")


if __name__ == "__main__":
    main()
