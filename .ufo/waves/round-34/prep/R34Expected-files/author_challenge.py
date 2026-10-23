#!/usr/bin/env python3
"""Author the pre-frozen metamorphic challenge for the round-34 expectation set.

Transform (benign, metadata-only, never executed):
  On a private byte-copy of each carrier that has GNU version-needs, replace the
  NUL-terminated strings referenced by .gnu.version_r (i.e. vn_file and vna_name)
  with random same-length ASCII names, in place, ONLY inside the linked string
  table (.dynstr).  No offset, size, section, program header, Rust-like structure
  or vna_hash field is modified.  Expected metadata is transformed by the same
  name mapping, so a reader that actually reads the linked string table at the
  recorded offsets must reproduce it; a reader that keys on original bytes,
  filename, sha256 or hard-coded names cannot.

Hash policy (pinned): `hash` in `expected` is the stored vna_hash field of the
Vernaux record.  Renaming a string does not rewrite the hash field, so the
stored hash is unchanged and no longer equals the SysV hash of the new name.
`challenge/checks.json` records both values per changed name; the originals are
verified to satisfy elf_hash(original_name) == stored_hash.

The mapping is frozen here (fixed per-carrier seeds) so no Python RNG version
drift can alter the schedule.  Carriers are written byte-exact, mode 0644, and
are never executed.

Usage:
  ./author_challenge.py            # (re)write schedule, carriers, evidence
  ./author_challenge.py --verify   # reapply frozen schedule, compare everything
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import string
import sys

sys.dont_write_bytecode = True
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from author_expected import (  # noqa: E402
    CAP_BYTES, ROOT, canonical_json, canonical_needed, elf_hash,
    extract_needs, parse_elf, parse_readelf_sections, parse_readelf_version_info,
    run_readelf, sha256_bytes, sha256_file, store_probe, write_bytes, write_text,
)

SEED_TAG = "kaidoku-r34-metamorphic-v1"
META_REL = Path("corpus/evidence/round-34/elf-meta")
CHAL = ROOT / "challenge"
ALPHA = string.ascii_letters + string.digits + "._"
FIRST = string.ascii_letters


def linked_table_strings(data: bytes, elf_ev: dict) -> set[str]:
    """All NUL-terminated strings in the linked .dynstr table (for collision checks)."""
    ds = elf_ev["dynstr"]
    if ds is None:
        return set()
    blob = data[ds["offset"]:ds["offset"] + ds["size"]]
    out = set()
    for part in blob.split(b"\x00"):
        if part:
            out.add(part.decode("latin-1"))
    return out


def gen_name(rng: random.Random, n: int, forbidden: set[str]) -> str:
    if n < 1:
        raise ValueError("empty name")
    for _ in range(10000):
        s = rng.choice(FIRST) + "".join(rng.choice(ALPHA) for _ in range(n - 1))
        if s not in forbidden:
            return s
    raise RuntimeError("could not generate collision-free replacement")


def name_mapping(cid: str, originals: list[str], forbidden: set[str]) -> dict[str, str]:
    rng = random.Random(int.from_bytes(
        hashlib.sha256(f"{SEED_TAG}|{cid}".encode()).digest()[:8], "big"))
    used = set(forbidden)
    mapping: dict[str, str] = {}
    for orig in sorted(set(originals)):
        if orig in mapping:
            continue
        new = gen_name(rng, len(orig), used)
        used.add(new)
        mapping[orig] = new
    return mapping


def transform_expected(expected: dict, mapping: dict[str, str]) -> dict:
    raw = []
    for f in expected["needed"]:
        raw.append({
            "file": mapping.get(f["file"], f["file"]),
            "versions": [dict(v, name=mapping.get(v["name"], v["name"]))
                         for v in f["versions"]],
        })
    return {"schema": 1, "needed": canonical_needed(raw)}


def apply_patch(data: bytes, string_table: dict, subs: list[dict]) -> bytes:
    buf = bytearray(data)
    tbl_lo, tbl_hi = string_table["offset"], string_table["offset"] + string_table["size"]
    for s in subs:
        off = s["file_offset"]
        orig = s["original"].encode("latin-1")
        new = s["replacement"].encode("latin-1")
        if s["table_offset"] + len(orig) >= string_table["size"]:
            raise ValueError(f"{s['original']}: name crosses string-table end")
        if not (tbl_lo <= off and off + len(orig) < tbl_hi):
            raise ValueError(f"{s['original']}: substitution outside linked table")
        if bytes(buf[off:off + len(orig)]) != orig:
            raise ValueError(f"{s['original']}: original bytes mismatch")
        if buf[off + len(orig)] != 0:
            raise ValueError(f"{s['original']}: missing NUL terminator")
        if len(new) != len(orig) or not new.decode("latin-1").isascii():
            raise ValueError("replacement is not same-length ASCII")
        buf[off:off + len(orig)] = new
        if buf[off + len(orig)] != 0:
            raise ValueError("terminator damaged")
    return bytes(buf)


def build_challenge_carrier(carrier: dict) -> tuple[dict, dict]:
    cid = carrier["id"]
    mid = "m" + cid[1:]
    src_copy = ROOT / carrier["path"]
    data = src_copy.read_bytes()
    if sha256_bytes(data) != carrier["sha256"]:
        raise SystemExit(f"{cid}: carrier copy digest mismatch")
    st = carrier["string_table"]
    if st is None or not carrier["expected"]["needed"]:
        raise SystemExit(f"{cid}: no version-needs; must be excluded, not transformed")

    needs, ev = extract_needs(data)
    if canonical_needed(needs) != carrier["expected"]["needed"]:
        raise SystemExit(f"{cid}: re-derived expected differs from manifest")
    ds = ev["dynstr"]
    if ds["offset"] != st["offset"] or ds["size"] != st["size"]:
        raise SystemExit(f"{cid}: string_table does not match parsed .dynstr")

    refs: dict[int, tuple[str, str]] = {}
    terminator_ok = True
    for n in needs:
        refs[n["file_offset"]] = (n["file"], "file")
        for v in n["versions"]:
            refs[v["name_offset"]] = (v["name"], "name")
    for off, (name, _kind) in refs.items():
        if off + len(name.encode("latin-1")) >= ds["size"]:
            terminator_ok = False
        elif data[ds["offset"] + off + len(name.encode("latin-1"))] != 0:
            terminator_ok = False
    if not terminator_ok:
        raise SystemExit(f"{cid}: an original referenced name is not NUL-terminated")

    forbidden = linked_table_strings(data, ev)
    mapping = name_mapping(cid, [name for name, _k in refs.values()], forbidden)
    for name, _k in refs.values():
        if len(mapping[name]) != len(name):
            raise SystemExit(f"{cid}: length-changing mapping")

    subs = [{"kind": kind, "table_offset": off, "file_offset": ds["offset"] + off,
             "original": name, "replacement": mapping[name]}
            for off, (name, kind) in sorted(refs.items())]
    patched = apply_patch(data, st, subs)

    expected = transform_expected(carrier["expected"], mapping)
    pneeds, pev = extract_needs(patched)
    derived = {"schema": 1, "needed": canonical_needed(pneeds)}
    if derived != expected:
        raise SystemExit(f"{cid}: patched-file parse does not match transformed expected")

    dest_rel = META_REL / f"{mid}.bin"
    dest = ROOT / dest_rel
    write_bytes(dest, patched)
    os.chmod(dest, 0o644)
    if sha256_file(dest) != sha256_bytes(patched):
        raise SystemExit(f"{cid}: patched copy digest mismatch")
    if dest.stat().st_size != len(patched):
        raise SystemExit(f"{cid}: patched size changed")
    if (dest.stat().st_mode & 0o777) != 0o644:
        raise SystemExit(f"{cid}: patched mode is not 0644")

    capdir = CHAL / "captured" / mid
    probes = {
        "version-info": run_readelf(["--version-info", "--wide", str(dest)]),
        "sections": run_readelf(["--section-headers", "--wide", str(dest)]),
    }
    probe_meta = {k: store_probe(capdir, f"readelf-{k}", v) for k, v in probes.items()}
    write_text(capdir / "probes.json", canonical_json(probe_meta))
    rf_needs, rf_header = parse_readelf_version_info(
        probes["version-info"]["stdout"].decode("utf-8"))
    readelf_ok = [(n["file"], n["cnt"],
                   [(v["name"], v["flags"], v["other"]) for v in n["versions"]])
                  for n in pneeds] == \
                 [(n["file"], n["cnt"],
                   [(v["name"], v["flags"], v["other"]) for v in n["versions"]])
                  for n in rf_needs]

    orig_sections = parse_readelf_sections(
        run_readelf(["--section-headers", "--wide", str(src_copy)])["stdout"].decode("utf-8"))
    new_sections = parse_readelf_sections(probes["sections"]["stdout"].decode("utf-8"))
    sect_ok = orig_sections == new_sections

    diffs = [i for i in range(len(data)) if data[i] != patched[i]]
    lo, hi = st["offset"], st["offset"] + st["size"]
    diff_in_table = all(lo <= i < hi for i in diffs)
    allowed = set()
    for s in subs:
        allowed.update(range(s["file_offset"], s["file_offset"] + len(s["original"])))
    diff_within_names = all(i in allowed for i in diffs)
    if not (diff_in_table and diff_within_names):
        raise SystemExit(f"{cid}: byte diff escaped substituted names")

    structure_ok = (len(data) == len(patched)
                    and pcmp_headers(parse_elf(data), parse_elf(patched)))

    stored_by_name = {v["name"]: v["hash"]
                      for n in carrier["expected"]["needed"] for v in n["versions"]}
    diagnostics = {
        "hash_changed_names": [
            {"name": s["replacement"], "stored_hash": stored_by_name[s["original"]],
             "elf_hash_of_new_name": elf_hash(s["replacement"]),
             "elf_hash_of_original_name": elf_hash(s["original"])}
            for s in subs if s["kind"] == "name"
        ],
    }

    schedule_row = {
        "id": mid,
        "origin_id": cid,
        "path": str(dest_rel),
        "sha256": sha256_bytes(patched),
        "size": len(patched),
        "source_path": carrier["source_path"],
        "origin_sha256": carrier["sha256"],
        "string_table": st,
        "substitutions": subs,
        "hash_policy": "stored_vna_hash_unchanged",
        "expected": expected,
    }
    checks = {
        "id": mid,
        "origin_id": cid,
        "transform_applied": True,
        "substitution_count": len(subs),
        "distinct_names": len(mapping),
        "original_names_nul_terminated": terminator_ok,
        "patched_names_nul_terminated": True,
        "expected_from_patched_file_matches": derived == expected,
        "readelf_cross_check": readelf_ok,
        "section_headers_identical": sect_ok,
        "elf_skeleton_identical": structure_ok,
        "byte_diffs": len(diffs),
        "byte_diffs_only_inside_linked_table": diff_in_table,
        "byte_diffs_only_inside_substituted_names": diff_within_names,
        "readelf_probes": probe_meta,
        "hash_diagnostics": diagnostics,
        "verneed_meta": {
            "offset": pev["verneed_sections"][0]["offset"] if pev["verneed_sections"] else None,
            "size": pev["verneed_sections"][0]["size"] if pev["verneed_sections"] else None,
            "link": pev["verneed_sections"][0]["link"] if pev["verneed_sections"] else None,
            "entries": len(pneeds),
        },
        "elf": pev["elf"],
    }
    return schedule_row, checks


def pcmp_headers(a: dict, b: dict) -> bool:
    ka = [(s["index"], s["name"], s["type"], s["addr"], s["offset"], s["size"],
           s["link"], s["info"], s["entsize"]) for s in a["sections"]]
    kb = [(s["index"], s["name"], s["type"], s["addr"], s["offset"], s["size"],
           s["link"], s["info"], s["entsize"]) for s in b["sections"]]
    return ka == kb


def author() -> int:
    manifest_p = ROOT / "manifest.json"
    manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
    rows, checks, excluded = [], [], []
    for carrier in manifest["carriers"]:
        if carrier["string_table"] is None or not carrier["expected"]["needed"]:
            excluded.append({
                "id": carrier["id"],
                "reason": "no .gnu.version_r / DT_VERNEED; no linked strings to substitute",
            })
            continue
        row, chk = build_challenge_carrier(carrier)
        rows.append(row)
        checks.append(chk)

    total = sum(r["size"] for r in rows) + sum(c["size"] for c in manifest["carriers"])
    if total > CAP_BYTES:
        raise SystemExit(f"retained binary bytes {total} exceed cap {CAP_BYTES}")

    schedule = {
        "schema": 1,
        "transform": {
            "kind": "gnu-elf-version-needs-string-substitution",
            "scope": "linked_string_table_only",
            "rules": {
                "same_length_ascii": True,
                "only_within_string_table": True,
                "no_offset_or_size_changes": True,
                "no_header_or_record_changes": True,
                "never_executed": True,
                "carrier_mode": "0644",
            },
            "seed_tag": SEED_TAG,
            "seed_derivation": "random.Random(first 8 bytes of sha256(seed_tag + '|' + origin_id))",
            "hash_policy": "hash is the stored vna_hash field; substitution does not rewrite it",
            "expected_rule": "expected names transformed by the recorded name mapping; "
                             "flags/other/hash unchanged; needed sorted by file, "
                             "versions sorted by (name, other)",
        },
        "excluded": excluded,
        "carriers": rows,
    }
    write_text(CHAL / "schedule.json", canonical_json(schedule))
    schedule_sha = sha256_file(CHAL / "schedule.json")
    write_text(CHAL / "SCHEDULE.sha256", f"{schedule_sha}  schedule.json\n")

    summary = {
        "schema": 1,
        "schedule_sha256": schedule_sha,
        "challenge_carrier_count": len(rows),
        "challenge_bytes": sum(r["size"] for r in rows),
        "original_bytes": sum(c["size"] for c in manifest["carriers"]),
        "retained_bytes_total": total,
        "cap_bytes": CAP_BYTES,
        "within_cap": total <= CAP_BYTES,
        "all_checks_pass": all(
            c["expected_from_patched_file_matches"] and c["readelf_cross_check"]
            and c["section_headers_identical"] and c["elf_skeleton_identical"]
            and c["byte_diffs_only_inside_linked_table"]
            and c["byte_diffs_only_inside_substituted_names"]
            and c["patched_names_nul_terminated"] for c in checks),
        "checks": checks,
    }
    write_text(CHAL / "checks.json", canonical_json(summary))
    print(f"challenge_carriers={len(rows)} bytes={summary['challenge_bytes']} "
          f"retained_total={total} schedule_sha256={schedule_sha}")
    print("all_checks_pass=", summary["all_checks_pass"])
    return 0 if summary["all_checks_pass"] else 1


def verify() -> int:
    schedule_p = CHAL / "schedule.json"
    if not schedule_p.is_file():
        raise SystemExit("challenge/schedule.json missing; run authoring first")
    schedule = json.loads(schedule_p.read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in manifest["carriers"]}
    problems = []
    total = sum(c["size"] for c in manifest["carriers"])
    for row in schedule["carriers"]:
        origin = by_id.get(row["origin_id"])
        if origin is None:
            problems.append(f"{row['id']}: unknown origin {row['origin_id']}")
            continue
        data = (ROOT / origin["path"]).read_bytes()
        patched = apply_patch(data, row["string_table"], row["substitutions"])
        if sha256_bytes(patched) != row["sha256"]:
            problems.append(f"{row['id']}: reapplied schedule digest mismatch")
        dest = ROOT / row["path"]
        if not dest.is_file():
            problems.append(f"{row['id']}: carrier missing")
            continue
        if (dest.stat().st_mode & 0o777) != 0o644:
            problems.append(f"{row['id']}: mode != 0644")
        if sha256_file(dest) != row["sha256"]:
            problems.append(f"{row['id']}: stored carrier digest mismatch")
        if dest.read_bytes() != patched:
            problems.append(f"{row['id']}: stored carrier differs from reapplied patch")
        pneeds, _ = extract_needs(patched)
        derived = {"schema": 1, "needed": canonical_needed(pneeds)}
        if derived != row["expected"]:
            problems.append(f"{row['id']}: expected re-derivation differs")
        rf = run_readelf(["--version-info", "--wide", str(dest)])
        rf_needs, _ = parse_readelf_version_info(rf["stdout"].decode("utf-8"))

        def norm(ns):
            out = []
            for n in sorted(ns, key=lambda n: n["file"]):
                vs = sorted([(v["name"], v["flags"], v["other"]) for v in n["versions"]],
                            key=lambda t: (t[0], t[2]))
                out.append((n["file"], vs))
            return out

        if norm(derived["needed"]) != norm(rf_needs):
            problems.append(f"{row['id']}: readelf cross-check differs")
        for s in row["substitutions"]:
            if len(s["original"]) != len(s["replacement"]) or not s["replacement"].isascii():
                problems.append(f"{row['id']}: non-ASCII or length-changing substitution")
            off = s["file_offset"]
            if patched[off:off + len(s["replacement"])] != s["replacement"].encode("latin-1"):
                problems.append(f"{row['id']}: substitution not present at recorded offset")
        total += row["size"]
    if total > CAP_BYTES:
        problems.append(f"retained total {total} exceeds cap {CAP_BYTES}")
    expected_sha = (CHAL / "SCHEDULE.sha256").read_text().split()[0]
    if sha256_file(schedule_p) != expected_sha:
        problems.append("SCHEDULE.sha256 does not match schedule.json")
    if problems:
        for p in problems:
            print("FAIL", p)
        return 1
    print(f"verify OK challenge_carriers={len(schedule['carriers'])} retained_total={total}")
    return 0


def main(argv: list[str]) -> int:
    if "--verify" in argv[1:]:
        return verify()
    return author()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
