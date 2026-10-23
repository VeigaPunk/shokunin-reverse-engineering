#!/usr/bin/env python3
"""Author reader-independent expected GNU ELF version-needs metadata (round 34).

Frozen predicate: "expected" is the set of GNU ELF Verneed/Vernaux records
(SHT_GNU_verneed / DT_VERNEED) carried by each selected host ELF, expressed as

    {schema: 1, needed: [{file: str,
                          versions: [{name: str, flags: int,
                                      other: int, hash: int}]}]}

sorted by file, then by (name, other).

Two extraction paths are used and MUST agree:
  A) authoritative  - direct ELF structure parse with struct (this file)
  B) cross-check    - `readelf --version-info --wide` text parse
Independent offset evidence comes from `readelf --section-headers --wide`
and the version-info section header ("Link: N (.dynstr)").

`hash` is the stored vna_hash field. It is independently checked against the
SysV ELF string hash of the referenced name, and the result of that check is
recorded (direct field read, not an inferred value).

No target binary is ever executed. Carriers are byte-exact mode-0644 copies.

Usage:
  ./author_expected.py            # (re)write manifest, carriers, evidence
  ./author_expected.py --verify   # re-derive from carriers, compare to manifest
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ELF_REL = Path("corpus/evidence/round-34/elf")
CAP = ROOT / "captured"
READELF = "/usr/bin/readelf"
CAP_BYTES = 16 * 1024 * 1024

SHT_STRTAB = 3
SHT_DYNAMIC = 6
SHT_GNU_VERNEED = 0x6FFFFFFE
DT_NEEDED = 1
DT_STRTAB = 5
DT_VERNEED = 0x6FFFFFFE
DT_VERNEEDNUM = 0x6FFFFFFF

# Frozen carrier selection: diverse version-needs shapes, all benign host ELF.
# e10 uses the resolved regular file (libstdc++.so.6 is a symlink).
CARRIERS = [
    ("e01", "/usr/bin/true"),
    ("e02", "/usr/bin/perl"),
    ("e03", "/usr/bin/curl"),
    ("e04", "/usr/bin/xz"),
    ("e05", "/usr/bin/bash"),
    ("e06", "/usr/bin/fwupdtool"),
    ("e07", "/usr/bin/fwupdmgr"),
    ("e08", "/usr/lib/libsmbclient.so.0.8.1"),
    ("e09", "/usr/lib/libssl3.so"),
    ("e10", "/usr/lib/libstdc++.so.6.0.36"),
    ("e11", "/usr/bin/net"),
    ("e12", "/usr/bin/sln"),
]


# --------------------------------------------------------------------------- #
# ELF parsing (authoritative path A)
# --------------------------------------------------------------------------- #
def parse_elf(data: bytes) -> dict:
    if len(data) < 52 or data[:4] != b"\x7fELF":
        raise ValueError("not an ELF file")
    ei_class, ei_data = data[4], data[5]
    if ei_class == 2:
        is64 = True
    elif ei_class == 1:
        is64 = False
    else:
        raise ValueError(f"unsupported EI_CLASS {ei_class}")
    if ei_data == 1:
        e, endian = "<", "little"
    elif ei_data == 2:
        e, endian = ">", "big"
    else:
        raise ValueError(f"unsupported EI_DATA {ei_data}")

    if is64:
        e_type, e_machine = struct.unpack_from(e + "HH", data, 0x10)
        e_phoff = struct.unpack_from(e + "Q", data, 0x20)[0]
        e_shoff = struct.unpack_from(e + "Q", data, 0x28)[0]
        e_phentsize, e_phnum = struct.unpack_from(e + "HH", data, 0x36)
        e_shentsize, e_shnum, e_shstrndx = struct.unpack_from(e + "HHH", data, 0x3A)
        sh_fmt, sh_size = e + "IIQQQQIIQQ", 64
    else:
        e_type, e_machine = struct.unpack_from(e + "HH", data, 0x10)
        e_phoff = struct.unpack_from(e + "I", data, 0x1C)[0]
        e_shoff = struct.unpack_from(e + "I", data, 0x20)[0]
        e_phentsize, e_phnum = struct.unpack_from(e + "HH", data, 0x2A)
        e_shentsize, e_shnum, e_shstrndx = struct.unpack_from(e + "HHH", data, 0x2E)
        sh_fmt, sh_size = e + "IIIIIIIIII", 40

    if e_shoff == 0 or e_shnum == 0:
        raise ValueError("no section header table")
    if e_shentsize != sh_size:
        raise ValueError(f"unexpected section header size {e_shentsize}")
    if e_shoff + e_shentsize * e_shnum > len(data):
        raise ValueError("section header table out of bounds")
    if e_shstrndx >= e_shnum:
        raise ValueError("bad e_shstrndx")

    sections = []
    for i in range(e_shnum):
        off = e_shoff + i * e_shentsize
        (sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_sz,
         sh_link, sh_info, sh_addralign, sh_entsize) = struct.unpack_from(sh_fmt, data, off)
        sections.append({
            "index": i, "name_off": sh_name, "type": sh_type, "flags": sh_flags,
            "addr": sh_addr, "offset": sh_offset, "size": sh_sz, "link": sh_link,
            "info": sh_info, "addralign": sh_addralign, "entsize": sh_entsize,
        })

    shstr = sections[e_shstrndx]
    shstr_data = data[shstr["offset"]:shstr["offset"] + shstr["size"]]

    def sec_name(idx: int) -> str:
        raw = shstr_data[idx:]
        z = raw.find(b"\x00")
        if z < 0:
            raise ValueError("unterminated shstrtab name")
        return raw[:z].decode("latin-1")

    for s in sections:
        s["name"] = sec_name(s["name_off"])

    return {
        "is64": is64, "endian": endian, "e": e,
        "e_type": e_type, "e_machine": e_machine,
        "e_phoff": e_phoff, "e_phnum": e_phnum,
        "e_shoff": e_shoff, "e_shnum": e_shnum, "e_shstrndx": e_shstrndx,
        "sections": sections,
    }


def read_cstr(table: bytes, off: int, what: str) -> tuple[str, int]:
    if off < 0 or off >= len(table):
        raise ValueError(f"{what} offset {off} outside string table")
    end = table.find(b"\x00", off)
    if end < 0:
        raise ValueError(f"{what} at {off} is not NUL-terminated")
    return table[off:end].decode("latin-1"), end


def extract_needs(data: bytes) -> tuple[list[dict], dict]:
    """Return (raw needs, evidence) from the ELF structures."""
    elf = parse_elf(data)
    secs = elf["sections"]
    e = elf["e"]
    needs: list[dict] = []
    strings: list[dict] = []
    verneed_sections: list[dict] = []
    dynstr_info = None
    chain_ok = True

    for s in secs:
        if s["type"] != SHT_GNU_VERNEED:
            continue
        if s["offset"] + s["size"] > len(data):
            raise ValueError("verneed section out of bounds")
        blob = data[s["offset"]:s["offset"] + s["size"]]
        if s["link"] >= len(secs):
            raise ValueError("verneed sh_link out of range")
        ds = secs[s["link"]]
        if ds["type"] != SHT_STRTAB:
            raise ValueError("verneed sh_link is not a string table")
        if ds["offset"] + ds["size"] > len(data):
            raise ValueError("linked dynstr out of bounds")
        dstr = data[ds["offset"]:ds["offset"] + ds["size"]]
        dynstr_info = {
            "index": ds["index"], "name": ds["name"],
            "offset": ds["offset"], "size": ds["size"],
        }
        verneed_sections.append({
            "index": s["index"], "name": s["name"], "addr": s["addr"],
            "offset": s["offset"], "size": s["size"],
            "link": s["link"], "info": s["info"], "entsize": s["entsize"],
        })

        po = 0
        last_vn_next = 0
        for i in range(s["info"]):
            if po + 16 > len(blob):
                raise ValueError("truncated Verneed record")
            vn_version, vn_cnt, vn_file, vn_aux, vn_next = struct.unpack_from(e + "HHIII", blob, po)
            fname, fend = read_cstr(dstr, vn_file, "vn_file")
            strings.append({
                "kind": "file", "record": i, "table_offset": vn_file,
                "value": fname, "length": fend - vn_file,
            })
            versions = []
            ap = po + vn_aux
            last_vna_next = 0
            for j in range(vn_cnt):
                if ap + 16 > len(blob):
                    raise ValueError("truncated Vernaux record")
                vna_hash, vna_flags, vna_other, vna_name, vna_next = \
                    struct.unpack_from(e + "IHHII", blob, ap)
                vname, vend = read_cstr(dstr, vna_name, "vna_name")
                strings.append({
                    "kind": "name", "record": i, "aux": j, "table_offset": vna_name,
                    "value": vname, "length": vend - vna_name,
                })
                versions.append({
                    "name": vname, "flags": int(vna_flags),
                    "other": int(vna_other), "hash": int(vna_hash),
                    "name_offset": vna_name,
                })
                last_vna_next = vna_next
                if j < vn_cnt - 1:
                    if vna_next == 0:
                        raise ValueError("Vernaux chain terminated early")
                    ap += vna_next
            if last_vna_next != 0:
                chain_ok = False
            needs.append({
                "file": fname, "file_offset": vn_file, "cnt": vn_cnt,
                "versions": versions,
            })
            last_vn_next = vn_next
            if i < s["info"] - 1:
                if vn_next == 0:
                    raise ValueError("Verneed chain terminated early")
                po += vn_next
        if last_vn_next != 0:
            chain_ok = False

    dynsec = next((s for s in secs if s["type"] == SHT_DYNAMIC), None)
    dynamic = {}
    if dynsec is not None:
        entsize = dynsec["entsize"] or (16 if elf["is64"] else 8)
        count = dynsec["size"] // entsize
        fmt = e + ("qQ" if elf["is64"] else "iI")
        for i in range(count):
            off = dynsec["offset"] + i * entsize
            if off + entsize > len(data):
                raise ValueError("dynamic entry out of bounds")
            tag, val = struct.unpack_from(fmt, data, off)
            if tag == DT_NEEDED:
                dynamic.setdefault("NEEDED", []).append(int(val))
            elif tag in (DT_STRTAB, DT_VERNEED, DT_VERNEEDNUM):
                dynamic[{DT_STRTAB: "STRTAB", DT_VERNEED: "VERNEED",
                         DT_VERNEEDNUM: "VERNEEDNUM"}[tag]] = int(val)

    evidence = {
        "elf": {
            "class": 64 if elf["is64"] else 32, "endian": elf["endian"],
            "type": elf["e_type"], "machine": elf["e_machine"],
            "shnum": elf["e_shnum"],
        },
        "verneed_sections": verneed_sections,
        "dynstr": dynstr_info,
        "strings": strings,
        "dynamic": dynamic,
        "chain_terminated": chain_ok,
    }
    return needs, evidence


def canonical_needed(needs: list[dict]) -> list[dict]:
    out = []
    for n in sorted(needs, key=lambda x: x["file"]):
        vs = [{"name": v["name"], "flags": v["flags"],
               "other": v["other"], "hash": v["hash"]} for v in n["versions"]]
        vs.sort(key=lambda v: (v["name"], v["other"]))
        out.append({"file": n["file"], "versions": vs})
    return out


def elf_hash(name: str) -> int:
    """System V ABI ELF string hash (as used for vna_hash)."""
    h = 0
    for b in name.encode("latin-1"):
        h = ((h << 4) + b) & 0xFFFFFFFF
        g = h & 0xF0000000
        if g:
            h ^= g >> 24
        h &= ~g
    return h & 0xFFFFFFFF


# --------------------------------------------------------------------------- #
# readelf parsing (independent path B)
# --------------------------------------------------------------------------- #
def run_readelf(args: list[str]) -> dict:
    p = subprocess.run([READELF] + args, capture_output=True, timeout=180)
    return {
        "argv": [READELF] + args,
        "exit": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
    }


def parse_readelf_version_info(text: str) -> tuple[list[dict], dict]:
    needs: list[dict] = []
    header: dict = {}
    in_needs = False
    cur = None
    declared = None
    for line in text.splitlines():
        if line.startswith("Version needs section"):
            in_needs = True
            cur = None
            m = re.search(r"contains (\d+) entr", line)
            declared = int(m.group(1)) if m else None
            continue
        if line.startswith("Version definition section") or \
                line.startswith("Version symbols section"):
            in_needs = False
            cur = None
            continue
        if not in_needs:
            continue
        m = re.match(r"^ Addr: 0x([0-9a-fA-F]+)\s+Offset: 0x([0-9a-fA-F]+)\s+"
                     r"Link: (\d+) \((\S+)\)\s*$", line)
        if m:
            header = {"addr": int(m.group(1), 16), "offset": int(m.group(2), 16),
                      "link": int(m.group(3)), "link_name": m.group(4)}
            continue
        m = re.match(r"^\s+(?:0x)?[0-9a-fA-F]+: Version: \d+\s+File: (\S+)\s+Cnt: (\d+)\s*$",
                     line)
        if m:
            cur = {"file": m.group(1), "cnt": int(m.group(2)), "versions": []}
            needs.append(cur)
            continue
        m = re.match(r"^\s+(?:0x)?[0-9a-fA-F]+:\s+Name: (\S+)\s+Flags: (\S+)\s+"
                     r"Version: (\d+)\s*$", line)
        if m and cur is not None:
            flags = 0 if m.group(2) == "none" else int(m.group(2), 16)
            cur["versions"].append({"name": m.group(1), "flags": flags,
                                    "other": int(m.group(3))})
    header["declared_entries"] = declared
    return needs, header


def parse_readelf_sections(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\s*\[\s*(\d+)\]\s+(.*)$", line)
        if not m:
            continue
        idx = int(m.group(1))
        parts = m.group(2).split()
        if len(parts) < 9:
            continue
        name, typ = parts[0], parts[1]
        try:
            addr = int(parts[2], 16)
            off = int(parts[3], 16)
            size = int(parts[4], 16)
            es = parts[5]
            if re.fullmatch(r"[0-9a-fA-F]{2}", parts[-4] or ""):
                flags, link, info, align = "", int(parts[-3], 10), int(parts[-2], 10), int(parts[-1], 10)
            else:
                flags, link, info, align = parts[-4], int(parts[-3], 10), int(parts[-2], 10), int(parts[-1], 10)
        except (ValueError, IndexError):
            continue
        rows.append({"index": idx, "name": name, "type": typ, "addr": addr,
                     "offset": off, "size": size, "es": es,
                     "flags": flags, "link": link, "info": info, "align": align})
    return rows


def sections_match(a: list[dict], b: list[dict]) -> bool:
    return [(x["file"], x["cnt"],
             [(v["name"], v["flags"], v["other"]) for v in x["versions"]]) for x in a] == \
           [(x["file"], x["cnt"],
             [(v["name"], v["flags"], v["other"]) for v in x["versions"]]) for x in b]


def parse_readelf_dynamic(text: str) -> dict:
    out: dict = {}
    for line in text.splitlines():
        m = re.match(r"^\s*0x[0-9a-fA-F]+\s+\((NEEDED|STRTAB|VERNEED|VERNEEDNUM)\)"
                     r"\s+(.*?)\s*$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2)
        hx = re.match(r"^0x([0-9a-fA-F]+)(?:\s+\(.*\))?$", val)
        if hx:
            out[tag] = int(hx.group(1), 16)
        elif re.fullmatch(r"[0-9]+", val):
            # VERNEEDNUM is printed in decimal, addresses in hex.
            out[tag] = int(val, 10)
        elif tag == "NEEDED":
            m2 = re.match(r"^.*?\[(.*?)\]$", val)
            out.setdefault("NEEDED_NAMES", []).append(m2.group(1) if m2 else val)
    return out


# --------------------------------------------------------------------------- #
# Serialisation helpers
# --------------------------------------------------------------------------- #
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def write_bytes(p: Path, b: bytes) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "wb") as f:
        f.write(b)


def store_probe(capdir: Path, name: str, probe: dict) -> dict:
    fname = f"{name}.txt"
    write_bytes(capdir / fname, probe["stdout"])
    meta = {
        "argv": probe["argv"],
        "exit": probe["exit"],
        "stdout_file": fname,
        "stdout_sha256": sha256_bytes(probe["stdout"]),
        "stderr_sha256": sha256_bytes(probe["stderr"]),
        "stderr_utf8": probe["stderr"].decode("utf-8", "replace"),
    }
    return meta


# --------------------------------------------------------------------------- #
# Core authoring
# --------------------------------------------------------------------------- #
def build_carrier(cid: str, source: str) -> tuple[dict, dict]:
    src = Path(source).resolve()
    if not src.is_file():
        raise SystemExit(f"{cid}: source is not a regular file: {src}")
    raw = src.read_bytes()
    src_sha = sha256_bytes(raw)

    dest_rel = ELF_REL / f"{cid}.bin"
    dest = ROOT / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(raw)
    os.chmod(dest, 0o644)
    dest_sha = sha256_file(dest)
    if dest_sha != src_sha:
        raise SystemExit(f"{cid}: copy digest mismatch")
    if dest.stat().st_size != len(raw):
        raise SystemExit(f"{cid}: copy size mismatch")
    if (dest.stat().st_mode & 0o777) != 0o644:
        raise SystemExit(f"{cid}: copy mode is not 0644")

    needs, ev = extract_needs(raw)
    expected = {"schema": 1, "needed": canonical_needed(needs)}

    capdir = CAP / cid
    probes = {
        "version-info": run_readelf(["--version-info", "--wide", str(src)]),
        "dynamic": run_readelf(["--dynamic", "--wide", str(src)]),
        "sections": run_readelf(["--section-headers", "--wide", str(src)]),
        "file-header": run_readelf(["--file-header", "--wide", str(src)]),
    }
    if probes["version-info"]["exit"] != 0:
        raise SystemExit(f"{cid}: readelf --version-info failed")
    probe_meta = {k: store_probe(capdir, f"readelf-{k}", v) for k, v in probes.items()}
    write_text(capdir / "probes.json", canonical_json(probe_meta))

    vi_text = probes["version-info"]["stdout"].decode("utf-8")
    sw_text = probes["sections"]["stdout"].decode("utf-8")
    dyn_text = probes["dynamic"]["stdout"].decode("utf-8")
    rf_needs, rf_header = parse_readelf_version_info(vi_text)
    rf_sections = parse_readelf_sections(sw_text)
    rf_dynamic = parse_readelf_dynamic(dyn_text)

    raw_needs = [{"file": n["file"], "cnt": n["cnt"], "versions": n["versions"]}
                 for n in needs]
    declared = rf_header.get("declared_entries")
    if not ev["verneed_sections"]:
        declared_ok = declared is None and not needs and not rf_needs
    elif len(ev["verneed_sections"]) == 1:
        # "contains N entries" counts Verneed records (one per needed file).
        declared_ok = (declared == len(needs) == ev["verneed_sections"][0]["info"]
                       and len(rf_needs) == len(needs))
    else:
        declared_ok = declared == ev["verneed_sections"][-1]["info"] \
            and len(rf_needs) == len(needs)

    cross = {
        "readelf_needs_match": sections_match(raw_needs, rf_needs),
        "declared_entries_match": declared_ok,
        "readelf_needs_exit": probes["version-info"]["exit"],
        "readelf_dynamic_exit": probes["dynamic"]["exit"],
        "readelf_sections_exit": probes["sections"]["exit"],
        "readelf_file_header_exit": probes["file-header"]["exit"],
    }

    sec_ok = True
    st = None
    if ev["verneed_sections"]:
        vn = ev["verneed_sections"][0]
        ds = ev["dynstr"]
        st = {"offset": ds["offset"], "size": ds["size"]}
        rf_vn = next((r for r in rf_sections if r["name"] == ".gnu.version_r"), None)
        rf_ds = next((r for r in rf_sections if r["name"] == ".dynstr"), None)
        sec_ok = bool(
            rf_vn and rf_ds
            and rf_vn["offset"] == vn["offset"] and rf_vn["size"] == vn["size"]
            and rf_vn["link"] == vn["link"]
            and rf_ds["index"] == ds["index"]
            and rf_ds["offset"] == ds["offset"] and rf_ds["size"] == ds["size"]
            and rf_header.get("offset") == vn["offset"]
            and rf_header.get("addr") == vn["addr"]
            and rf_header.get("link") == vn["link"]
            and rf_header.get("link_name") == ds["name"]
        )
    else:
        sec_ok = (".gnu.version_r" not in sw_text)
        if rf_dynamic.get("VERNEEDNUM") is not None:
            sec_ok = False
        st = None

    dyn_ok = True
    if ev["verneed_sections"]:
        vn = ev["verneed_sections"][0]
        dyn_ok = (rf_dynamic.get("VERNEED") == vn["addr"]
                  and rf_dynamic.get("VERNEEDNUM") == vn["info"])
    else:
        dyn_ok = rf_dynamic.get("VERNEED") is None and rf_dynamic.get("VERNEEDNUM") is None

    hashes_checked = 0
    hash_mismatch = []
    for n in needs:
        for v in n["versions"]:
            hashes_checked += 1
            if elf_hash(v["name"]) != v["hash"]:
                hash_mismatch.append({"name": v["name"], "stored": v["hash"],
                                      "recomputed": elf_hash(v["name"])})

    nul_ok = all(s["table_offset"] + s["length"] < ev["dynstr"]["size"]
                 for s in ev["strings"]) if ev["dynstr"] else True

    checks = {
        "id": cid,
        "source_path": str(src),
        "carrier_path": str(ELF_REL / f"{cid}.bin"),
        "carrier_sha256": dest_sha,
        "source_sha256": src_sha,
        "size": len(raw),
        "string_table": st,
        "verneed_section": ev["verneed_sections"][0] if ev["verneed_sections"] else None,
        "needed_count": len(expected["needed"]),
        "version_count": sum(len(n["versions"]) for n in expected["needed"]),
        "expected_sha256": sha256_bytes(canonical_json(expected).encode("utf-8")),
        "cross_checks": {
            "readelf_needs_match": cross["readelf_needs_match"],
            "declared_entries_match": cross["declared_entries_match"],
            "section_link_offsets_match": sec_ok,
            "dynamic_tags_match": dyn_ok,
            "verneed_chain_terminated": ev["chain_terminated"],
            "linked_strings_nul_terminated": nul_ok,
            "readelf_exits": {k: v["exit"] for k, v in probes.items()},
        },
        "hash_provenance": {
            "policy": "vna_hash field read directly from Vernaux (not inferred)",
            "sysv_hash_checked": hashes_checked,
            "sysv_hash_mismatches": hash_mismatch,
            "all_match": not hash_mismatch,
        },
        "dynamic": ev["dynamic"],
        "string_offsets": ev["strings"],
        "readelf_probes": probe_meta,
        "elf": ev["elf"],
    }

    carrier = {
        "id": cid,
        "path": str(ELF_REL / f"{cid}.bin"),
        "sha256": dest_sha,
        "size": len(raw),
        "source_path": str(src),
        "string_table": st,
        "expected": expected,
    }
    return carrier, checks


def author() -> int:
    version_probe = run_readelf(["--version"])
    write_bytes(CAP / "readelf-version.txt", version_probe["stdout"] + version_probe["stderr"])
    write_text(CAP / "run.json", canonical_json({
        "argv": version_probe["argv"],
        "exit": version_probe["exit"],
        "stdout_file": "readelf-version.txt",
        "stdout_sha256": sha256_bytes(version_probe["stdout"] + version_probe["stderr"]),
    }))

    carriers, all_checks = [], []
    for cid, source in CARRIERS:
        carrier, checks = build_carrier(cid, source)
        carriers.append(carrier)
        all_checks.append(checks)

    total = sum(c["size"] for c in carriers)
    ids = [c["id"] for c in carriers]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate carrier ids")
    shas = [c["sha256"] for c in carriers]
    if len(set(shas)) != len(shas):
        raise SystemExit("duplicate carrier content")
    if total > CAP_BYTES:
        raise SystemExit(f"carrier bytes {total} exceed cap {CAP_BYTES}")

    manifest = {"schema": 1, "carriers": carriers}
    write_text(ROOT / "manifest.json", canonical_json(manifest))
    manifest_sha = sha256_file(ROOT / "manifest.json")
    write_text(ROOT / "MANIFEST.sha256", f"{manifest_sha}  manifest.json\n")

    summary = {
        "schema": 1,
        "carrier_count": len(carriers),
        "carrier_bytes_total": total,
        "cap_bytes": CAP_BYTES,
        "within_cap": total <= CAP_BYTES,
        "manifest_sha256": manifest_sha,
        "all_cross_checks_pass": all(
            all(v for k, v in c["cross_checks"].items() if k != "readelf_exits")
            and c["hash_provenance"]["all_match"] for c in all_checks),
        "checks": all_checks,
    }
    write_text(ROOT / "checks.json", canonical_json(summary))
    print(f"carriers={len(carriers)} bytes={total} manifest_sha256={manifest_sha}")
    print("all_cross_checks_pass=", summary["all_cross_checks_pass"])
    return 0 if summary["all_cross_checks_pass"] else 1


def verify() -> int:
    manifest_p = ROOT / "manifest.json"
    if not manifest_p.is_file():
        raise SystemExit("manifest.json missing; run authoring first")
    manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
    problems = []
    total = 0
    for carrier in manifest["carriers"]:
        cid = carrier["id"]
        dest = ROOT / carrier["path"]
        if not dest.is_file():
            problems.append(f"{cid}: carrier missing")
            continue
        if (dest.stat().st_mode & 0o777) != 0o644:
            problems.append(f"{cid}: mode != 0644")
        if dest.stat().st_size != carrier["size"]:
            problems.append(f"{cid}: size mismatch")
        if sha256_file(dest) != carrier["sha256"]:
            problems.append(f"{cid}: sha256 mismatch")
        needs, ev = extract_needs(dest.read_bytes())
        expected = {"schema": 1, "needed": canonical_needed(needs)}
        if expected != carrier["expected"]:
            problems.append(f"{cid}: expected re-derivation differs from manifest")
        vi = run_readelf(["--version-info", "--wide", str(dest)])
        rf_needs, _ = parse_readelf_version_info(vi["stdout"].decode("utf-8"))
        if not sections_match(
                [{"file": n["file"], "cnt": n["cnt"], "versions": n["versions"]} for n in needs],
                rf_needs):
            problems.append(f"{cid}: readelf cross-check differs")
        st = carrier["string_table"]
        if st is not None and ev["dynstr"] and (
                st["offset"] != ev["dynstr"]["offset"] or st["size"] != ev["dynstr"]["size"]):
            problems.append(f"{cid}: string_table differs")
        total += carrier["size"]
    if total > CAP_BYTES:
        problems.append(f"total {total} exceeds cap {CAP_BYTES}")
    if sha256_file(manifest_p) != sha256_file(ROOT / "manifest.json"):
        problems.append("manifest unreadable")
    expected_sha = (ROOT / "MANIFEST.sha256").read_text().split()[0]
    if sha256_file(manifest_p) != expected_sha:
        problems.append("MANIFEST.sha256 does not match manifest.json")
    if problems:
        for p in problems:
            print("FAIL", p)
        return 1
    print(f"verify OK carriers={len(manifest['carriers'])} bytes={total}")
    return 0


def main(argv: list[str]) -> int:
    if "--verify" in argv[1:]:
        return verify()
    return author()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
