#!/usr/bin/env python3
"""Independent review of expected records e09-e12 (Kaidoku round34).

Parse the carrier ELF bytes directly (my own struct parser, not the
production reader) for SHT_GNU_verneed, resolve strings via the linked
.dynstr, compare against the frozen expected.json records.  Also parse the
retained readelf --version-info text outputs as a second oracle.
No carrier is executed; no production reader/counter is run.
"""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

SANDBOX = Path("/fast/scratch/hyaku/kaidoku-r34/w1/RevOracleC")
MANIFEST = SANDBOX / "corpus/evidence/round-34/elf"  # not used; manifest below
EXPECTED = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/expected.json")
CAPTURED = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/prep/R34Expected-files/captured")
ELF_DIR = SANDBOX / "corpus/evidence/round-34/elf"

SHT_GNU_VERNEED = 0x6FFFFFFE
SHT_STRTAB = 3
SHT_DYNAMIC = 6
DT_VERNEED = 0x6FFFFFFE
DT_VERNEEDNUM = 0x6FFFFFFF
DT_STRTAB = 5


def elf_hash(name: str) -> int:
    h = 0
    for b in name.encode("latin-1"):
        h = ((h << 4) + b) & 0xFFFFFFFF
        g = h & 0xF0000000
        if g:
            h ^= g >> 24
        h &= ~g
    return h & 0xFFFFFFFF


def parse_sections(data: bytes):
    assert data[:4] == b"\x7fELF", "not ELF"
    klass, ei_data = data[4], data[5]
    e = "<" if ei_data == 1 else ">"
    assert klass == 2, "not ELF64"
    shoff = struct.unpack_from(e + "Q", data, 0x28)[0]
    shentsize, shnum, shstrndx = struct.unpack_from(e + "HHH", data, 0x3A)
    assert shentsize == 64
    secs = []
    for i in range(shnum):
        off = shoff + i * shentsize
        name, typ, flags, addr, soff, sz, link, info, align, entsize = \
            struct.unpack_from(e + "IIQQQQIIQQ", data, off)
        secs.append(dict(index=i, name_off=name, type=typ, addr=addr,
                         offset=soff, size=sz, link=link, info=info,
                         align=align, entsize=entsize))
    shstr = data[secs[shstrndx]["offset"]:secs[shstrndx]["offset"] + secs[shstrndx]["size"]]
    for s in secs:
        z = shstr.find(b"\x00", s["name_off"])
        s["name"] = shstr[s["name_off"]:z].decode("latin-1")
    return secs


def extract_verneed(data: bytes):
    secs = parse_sections(data)
    vn_secs = [s for s in secs if s["type"] == SHT_GNU_VERNEED]
    results = []
    for vn in vn_secs:
        ds = secs[vn["link"]]
        assert ds["type"] == SHT_STRTAB
        dstr = data[ds["offset"]:ds["offset"] + ds["size"]]
        blob = data[vn["offset"]:vn["offset"] + vn["size"]]
        po = 0
        for i in range(vn["info"]):
            vn_version, vn_cnt, vn_file, vn_aux, vn_next = \
                struct.unpack_from("<HHIII", blob, po)
            z = dstr.find(b"\x00", vn_file)
            fname = dstr[vn_file:z].decode("latin-1")
            versions = []
            ap = po + vn_aux
            for j in range(vn_cnt):
                vna_hash, vna_flags, vna_other, vna_name, vna_next2 = \
                    struct.unpack_from("<IHHII", blob, ap)
                z2 = dstr.find(b"\x00", vna_name)
                vname = dstr[vna_name:z2].decode("latin-1")
                versions.append(dict(name=vname, flags=vna_flags,
                                     other=vna_other, hash=vna_hash,
                                     name_offset=vna_name,
                                     elf_hash=elf_hash(vname)))
                ap += vna_next2
            results.append(dict(file=fname, file_offset=vn_file,
                                versions=versions))
            po += vn_next
    return results, secs


def parse_readelf_vi(text: str):
    needs = []
    cur = None
    in_needs = False
    for line in text.splitlines():
        if line.startswith("Version needs section"):
            in_needs = True
            cur = None
            continue
        if line.startswith("Version definition section") or line.startswith("Version symbols section"):
            in_needs = False
            cur = None
            continue
        if not in_needs:
            continue
        m = re.match(r"^\s+(?:0x)?[0-9a-fA-F]+: Version: \d+\s+File: (\S+)\s+Cnt: (\d+)\s*$", line)
        if m:
            cur = {"file": m.group(1), "versions": []}
            needs.append(cur)
            continue
        m = re.match(r"^\s+0x[0-9a-fA-F]+:\s+Name: (\S+)\s+Flags: (\S+)\s+Version: (\d+)\s*$", line)
        if m and cur is not None:
            flags = 0 if m.group(2) == "none" else int(m.group(2), 16)
            cur["versions"].append({"name": m.group(1), "flags": flags,
                                    "other": int(m.group(3))})
    return needs


def main():
    manifest = json.loads(EXPECTED.read_text())
    carriers = {c["id"]: c for c in manifest["carriers"]}
    ids = ["e09", "e10", "e11", "e12"]
    problems = []
    for cid in ids:
        rec = carriers[cid]
        path = ELF_DIR / f"{cid}.bin"
        data = path.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        if h != rec["sha256"]:
            problems.append(f"{cid}: carrier sha256 mismatch {h} != {rec['sha256']}")
        if len(data) != rec["size"]:
            problems.append(f"{cid}: size mismatch")
        # e12: no verneed
        verneed, secs = extract_verneed(data)
        raw_map = {}
        for n in verneed:
            for v in n["versions"]:
                raw_map[(n["file"], v["name"], v["other"])] = v
        real_needs = []
        for n in verneed:
            real_needs.append({
                "file": n["file"],
                "versions": [{"name": v["name"], "flags": v["flags"],
                              "other": v["other"], "hash": v["hash"]}
                             for v in n["versions"]],
            })
        real_needs.sort(key=lambda x: x["file"])
        for n in real_needs:
            n["versions"].sort(key=lambda v: (v["name"], v["other"]))
        manifest_needs = rec["expected"].get("needed", [])
        if manifest_needs != real_needs:
            problems.append(f"{cid}: expected.needed differs from direct parse")
        # string_table vs .dynstr
        dynstr = next((s for s in secs if s["name"] == ".dynstr"), None)
        if rec["string_table"] is None:
            if dynstr is not None and any(s["type"] == SHT_GNU_VERNEED for s in secs):
                problems.append(f"{cid}: string_table null but verneed section present")
        else:
            if dynstr is None or rec["string_table"]["offset"] != dynstr["offset"] or \
                    rec["string_table"]["size"] != dynstr["size"]:
                problems.append(
                    f"{cid}: string_table {rec['string_table']} != .dynstr "
                    f"{None if dynstr is None else (dynstr['offset'], dynstr['size'])}")
        # retained readelf oracle
        vi_path = CAPTURED / cid / "readelf-version-info.txt"
        rf = parse_readelf_vi(vi_path.read_text())
        # readelf reports binary (Verneed) order; normalize by set
        rf_set = {(n["file"], v["name"], v["flags"], v["other"])
                  for n in rf for v in n["versions"]}
        dir_set = {(n["file"], v["name"], v["flags"], v["other"])
                   for n in real_needs for v in n["versions"]}
        if rf_set != dir_set:
            problems.append(f"{cid}: retained readelf -V set differs from binary parse")
            only_rf = rf_set - dir_set
            only_dir = dir_set - rf_set
            problems.append(f"{cid}: only_readelf={sorted(only_rf)[:10]}")
            problems.append(f"{cid}: only_binary={sorted(only_dir)[:10]}")
        # hash field vs SysV recompute; count hash coincidences
        mismatch = []
        for n in real_needs:
            for v in n["versions"]:
                v = raw_map.get((n["file"], v["name"], v["other"]))
                if v is not None and v["hash"] != v["elf_hash"]:
                    mismatch.append((n["file"], v["name"], v["hash"], v["elf_hash"]))
        nfiles = len(real_needs)
        nvers = sum(len(n["versions"]) for n in real_needs)
        print(f"--- {cid} sha256={h}")
        print(f"    files={nfiles} versions={nvers} string_table={rec['string_table']}")
        if mismatch:
            print(f"    HASH_NON_SYSV entries: {len(mismatch)}")
            for m in mismatch[:10]:
                print(f"      {m}")
        else:
            print("    all vna_hash == SysV ELF hash of name (field value consistent)")
        if cid == "e12":
            dyn_text = (CAPTURED / cid / "readelf-dynamic.txt").read_text()
            if re.search(r"\((VERNEED|VERNEEDNUM)\)", dyn_text):
                problems.append("e12: dynamic carries VERNEED/VERNEEDNUM tags")
            if any(s["type"] == SHT_GNU_VERNEED for s in secs):
                problems.append("e12: verneed section present in binary")
            if dynstr is not None and dynstr["size"] != 1:
                problems.append(f"e12: .dynstr size {dynstr['size']} != 1")
    print()
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" ", p)
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
