#!/usr/bin/env python3
"""R43W2AssimFlip flip-limb comparison: fresh API/page bytes vs committed round-42/43 receipts.

Read-only: reads scratch fetches + committed lane receipts, writes JSON verdict to scratch.
"""
import json, hashlib, re, sys
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kaidoku-r43/w2/R43W2AssimFlip")
LANE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
R43_RECEIPT = LANE / ".ufo/waves/round-43/w1/artifacts/R43AssimGround/receipts/rel-r43-assimground.json"
R42_RECEIPT = LANE / ".ufo/waves/round-42/w1/artifacts/R42Assim/receipts/rel.json"
ENTRY = LANE / "corpus/knowledge/2026-10-27-sasquatch-release-matrix.md"

fresh = json.loads((SCRATCH / "rel-r43w2.json").read_text())
r43 = json.loads(R43_RECEIPT.read_text())
r42 = json.loads(R42_RECEIPT.read_text())
page2 = json.loads((SCRATCH / "rel-r43w2-page2.json").read_text())
tags = json.loads((SCRATCH / "tags-r43w2.json").read_text())

V = {"measured_rev": "5856614ac4bf7f2363bbcd1956644474a82108e5",
     "freeze": "f3f8db389416d094b1ddeb1215ddcf914bfc0d1c"}

def canon(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def strip_dc(rel):
    rel = dict(rel)
    rel["assets"] = [{k: v for k, v in a.items() if k != "download_count"} for a in rel.get("assets", [])]
    for k in ("reactions",):
        rel.pop(k, None)
    return rel

# Limb (a): ninth release
V["limb_a_ninth_release"] = {
    "fresh_count": len(fresh),
    "r43_count": len(r43),
    "r42_count": len(r42),
    "page2_item_count": len(page2),
    "fresh_tags": [r["tag_name"] for r in fresh],
    "r43_tags": [r["tag_name"] for r in r43],
    "tag_set_equal_r43": sorted(r["tag_name"] for r in fresh) == sorted(r["tag_name"] for r in r43),
    "tags_endpoint_count": len(tags),
    "tags_endpoint_names": [t["name"] for t in tags],
    "sasquatch_v_tags": sorted(t["name"] for t in tags if t["name"].startswith("sasquatch-v")),
    "new_sasquatch_v_tags_vs_r43": sorted(set(t["name"] for t in tags if t["name"].startswith("sasquatch-v")) - set(r["tag_name"] for r in r43)),
}

# Limb (b): changed asset set (field-by-field vs r43 retained; and vs r42)
def field_diffs(a, b):
    """returns list of (release_tag, asset_name|None, field, val_a, val_b)"""
    out = []
    by_tag_a = {r["tag_name"]: r for r in a}
    by_tag_b = {r["tag_name"]: r for r in b}
    for tag in sorted(set(by_tag_a) | set(by_tag_b)):
        if tag not in by_tag_a:
            out.append((tag, None, "RELEASE_MISSING_IN_FRESH", None, "present"))
            continue
        if tag not in by_tag_b:
            out.append((tag, None, "RELEASE_MISSING_IN_BASE", "present", None))
            continue
        ra, rb = by_tag_a[tag], by_tag_b[tag]
        for f in sorted(set(ra) | set(rb)):
            if f == "assets":
                continue
            if ra.get(f) != rb.get(f):
                out.append((tag, None, f, ra.get(f), rb.get(f)))
        aa = {x["name"]: x for x in ra.get("assets", [])}
        bb = {x["name"]: x for x in rb.get("assets", [])}
        for name in sorted(set(aa) | set(bb)):
            if name not in aa:
                out.append((tag, name, "ASSET_MISSING_IN_FRESH", None, "present"))
                continue
            if name not in bb:
                out.append((tag, name, "ASSET_MISSING_IN_BASE", "present", None))
                continue
            for f in sorted(set(aa[name]) | set(bb[name])):
                if aa[name].get(f) != bb[name].get(f):
                    out.append((tag, name, f, aa[name].get(f), bb[name].get(f)))
    return out

diffs_r43 = field_diffs(fresh, r43)
diffs_r42 = field_diffs(fresh, r42)
V["limb_b_asset_set"] = {
    "fresh_vs_r43_diff_count": len(diffs_r43),
    "fresh_vs_r43_diffs": diffs_r43,
    "fresh_vs_r42_diff_count": len(diffs_r42),
    "fresh_vs_r42_non_download_count_diffs": [d for d in diffs_r42 if d[2] != "download_count"],
    "canonical_hash_fresh_dc_stripped": canon([strip_dc(r) for r in fresh]),
    "canonical_hash_r43_dc_stripped": canon([strip_dc(r) for r in r43]),
    "canonical_hash_r42_dc_stripped": canon([strip_dc(r) for r in r42]),
    "asset_name_set_equal_r43": sorted(n for r in fresh for n in [a["name"] for a in r["assets"]]) == sorted(n for r in r43 for n in [a["name"] for a in r["assets"]]),
    "asset_count_per_release_fresh": [len(r["assets"]) for r in fresh],
    "asset_count_per_release_r43": [len(r["assets"]) for r in r43],
}

# Limb (c): body version-pair — standalone 1.0 token
tok = re.compile(r"(?<![0-9.])1\.0(?![0-9.])")
bodyinfo = []
for r in fresh:
    b = r.get("body") or ""
    m = tok.search(b)
    bodyinfo.append({"tag": r["tag_name"], "body_len": len(b), "standalone_1.0": bool(m),
                     "match": m.group(0) if m else None})
V["limb_c_body_pair"] = {
    "bodies": bodyinfo,
    "any_standalone_1.0": any(b["standalone_1.0"] for b in bodyinfo),
    "bodies_with_text": [b["tag"] for b in bodyinfo if b["body_len"] > 0],
}

# Limb (d): digest-presence pattern
DIGEST_PINS = {
    "sasquatch_1.0_amd64.deb": "efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95",
    "sasquatch_1.0_arm64.deb": "28e57a4ff545da32a65c3e061ff8a51e5ebaa5d170985c49f0b3eef08923476e",
    "sasquatch_1.0_armhf.deb": "29c721598df93dcdf3c876b61d9941764f40af8f0ec4f0f8ac3d2fe75b8f1c22",
    "sasquatch-dbgsym_1.0_amd64.deb": "73d44ca506e3273784091f3092839e8e8c162a81bb7d5af757201b0b1d41c54e",
    "sasquatch-dbgsym_1.0_arm64.deb": "7891831a7cd7111d7d2380ef2df3dcb32295ea5093eff5ceec15e407e7be49c4",
    "sasquatch-dbgsym_1.0_armhf.deb": "9d82e6d4320957e2491603aa00f9c55fd816770a5f8926eaf7c454e98e74686a",
}
digest_counts_fresh = [sum(1 for a in r["assets"] if a.get("digest")) for r in fresh]
digest_counts_r43 = [sum(1 for a in r["assets"] if a.get("digest")) for r in r43]
v6 = next(r for r in fresh if r["tag_name"] == "sasquatch-v4.5.1-6")
digest_check = {}
for a in v6["assets"]:
    pin = DIGEST_PINS.get(a["name"])
    digest_check[a["name"]] = {"api_digest": a.get("digest"), "entry_pin": pin,
                               "matches_entry": a.get("digest") == ("sha256:" + pin if pin else None)}
V["limb_d_digest_pattern"] = {
    "digest_counts_fresh": digest_counts_fresh,
    "digest_counts_r43": digest_counts_r43,
    "projection_fresh": [len(fresh), [len(r["assets"]) for r in fresh], digest_counts_fresh],
    "expected_projection": [8, [6, 6, 6, 6, 6, 6, 6, 2], [6, 0, 0, 0, 0, 0, 0, 0]],
    "v6_digest_values_match_entry_pins": digest_check,
}

# Page checks (S137)
html = (SCRATCH / "sasq-releases-r43w2.html").read_text()
taglinks = sorted(set(re.findall(r"sasquatch/releases/tag/([^\"?#<]+)", html)))
V["page_check"] = {
    "bytes": len(html.encode()),
    "asset_filename_occurrences": {n: html.count(n) for n in [
        "sasquatch_1.0_amd64.deb", "sasquatch_1.0_arm64.deb", "sasquatch_1.0_armhf.deb",
        "sasquatch-dbgsym_1.0_amd64.deb"]},
    "distinct_tag_links": taglinks,
    "distinct_tag_link_count": len(taglinks),
}

# Entry table cross-check (sizes per release/arch)
EXPECTED_SIZES = {  # from committed entry table
    "sasquatch-v4.5.1-6": {"amd64": 187244, "arm64": 170080, "armhf": 164428},
    "sasquatch-v4.5.1-5": {"amd64": 187040, "arm64": 170556, "armhf": 164376},
    "sasquatch-v4.5.1-4": {"amd64": 186968, "arm64": 169824, "armhf": 164524},
    "sasquatch-v4.5.1-3": {"amd64": 187024, "arm64": 169828, "armhf": 164452},
    "sasquatch-v4.5.1-2": {"amd64": 187076, "arm64": 169504, "armhf": 164724},
    "sasquatch-v4.5.1-1": {"amd64": 187016, "arm64": 169360, "armhf": 164716},
    "sasquatch-v1.0.1": {"amd64": 185724, "arm64": 168184, "armhf": 162288},
    "sasquatch-v1.0": {"amd64": 185708},
}
size_mismatches = []
for r in fresh:
    exp = EXPECTED_SIZES.get(r["tag_name"], {})
    for a in r["assets"]:
        m = re.match(r"sasquatch(_-dbgsym)?_1\.0_(amd64|arm64|armhf)\.deb", a["name"])
        if m and "dbgsym" not in a["name"]:
            arch = m.group(2)
            if arch in exp and a["size"] != exp[arch]:
                size_mismatches.append((r["tag_name"], a["name"], a["size"], exp[arch]))
V["entry_size_crosscheck"] = {"mismatches": size_mismatches, "checked": True}

(SCRATCH / "verdict.json").write_text(json.dumps(V, indent=2, sort_keys=True) + "\n")
print(json.dumps(V, indent=2, sort_keys=True))
