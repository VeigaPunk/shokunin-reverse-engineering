"""Independent static audit of frozen expected records e01-e04 vs carrier bytes.

Read-only byte inspection of the sandbox private copies. Never executes the
carrier; parses ELF structures with stdlib struct. Prints per-check PASS/FAIL.
"""
import json
import struct
import sys

SAND = "/fast/scratch/hyaku/kaidoku-r34/w1/RevOracleA"
MANIFEST = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/expected.json"
TARGETS = {"e01": 0, "e02": 1, "e03": 2, "e04": 3}
if "--all" in sys.argv:
    TARGETS = {f"e{i+1:02d}": i for i in range(12)}

fails = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def elf_hash(name: str) -> int:
    h = 0
    for b in name.encode("latin-1"):
        h = ((h << 4) + b) & 0xFFFFFFFF
        g = h & 0xF0000000
        if g:
            h ^= g >> 24
        h &= ~g & 0xFFFFFFFF
    return h


def read_cstr(blob, off):
    end = blob.index(b"\x00", off)
    return blob[off:end].decode("latin-1")


def sections(blob):
    _, e = blob[:4], "<" if blob[5] == 1 else ">"
    shoff, = struct.unpack_from(e + "Q", blob, 0x28)
    shentsize, shnum, shstrndx = struct.unpack_from(e + "HHH", blob, 0x3A)
    hdrs = []
    for i in range(shnum):
        base = shoff + i * shentsize
        nameoff, shtype, flags, addr, offset, size, link, info, align, entsize = \
            struct.unpack_from(e + "IIQQQQIIQQ", blob, base)
        hdrs.append(dict(nameoff=nameoff, type=shtype, addr=addr, offset=offset,
                         size=size, link=link, info=info, entsize=entsize))
    strtab = hdrs[shstrndx]
    names_blob = blob[strtab["offset"]:strtab["offset"] + strtab["size"]]
    for h in hdrs:
        h["name"] = read_cstr(names_blob, h["nameoff"])
    return hdrs, e


def audit(cidx, rec):
    path = f"{SAND}/corpus/evidence/round-34/elf/{rec['id']}.bin"
    blob = open(path, "rb").read()
    print(f"== {rec['id']} ({rec['source_path']}) bytes={len(blob)}")
    check(len(blob) == rec["size"], f"{rec['id']} size {len(blob)}=={rec['size']}")

    hdrs, e = sections(blob)
    byname = {h["name"]: h for h in hdrs}
    d = byname.get(".dynstr")
    vr = byname.get(".gnu.version_r")
    vs = byname.get(".gnu.version")
    ds = byname.get(".dynsym")
    check(d is not None and vr is not None, f"{rec['id']} has .dynstr/.gnu.version_r")
    if d is None or vr is None:
        return 0, 0
    check(d["offset"] == rec["string_table"]["offset"] and d["size"] == rec["string_table"]["size"],
          f"{rec['id']} string_table offset/size == sh(.dynstr) "
          f"({rec['string_table']['offset']},{rec['string_table']['size']}) vs ({d['offset']},{d['size']})")
    check(vr["link"] == next(i for i, h in enumerate(hdrs) if h["name"] == ".dynstr"),
          f"{rec['id']} .gnu.version_r link -> .dynstr")
    dstr = blob[d["offset"]:d["offset"] + d["size"]]

    # verneed walk
    vbase = vr["offset"]
    needs = []
    for i in range(vr["info"]):
        vvn, vcnt, vfile, vaux, vnext = struct.unpack_from(e + "HHIII", blob, vbase)
        check(vvn == 1, f"{rec['id']} verneed[{i}] vn_version==1")
        auxs = []
        ap = vbase + vaux
        for j in range(vcnt):
            vh, vf, vo, vn, vnx = struct.unpack_from(e + "IHHII", blob, ap)
            auxs.append(dict(hash=vh, flags=vf, other=vo, name=read_cstr(dstr, vn),
                             name_off=vn, next=vnx))
            if vnx == 0:
                ap_end = ap
                break
            ap += vnx
        else:
            ap_end = ap + 16
        needs.append(dict(file=read_cstr(dstr, vfile), file_off=vfile, cnt=vcnt,
                          aux=auxs, tail_off=ap_end))
        if vnext == 0:
            break
        vbase += vnext

    # compare with frozen expected (needed compared keyed by file, not position)
    exp = rec["expected"]["needed"]
    check(len(needs) == len(exp), f"{rec['id']} needed count {len(needs)}=={len(exp)}")
    check(sorted(n["file"] for n in needs) == sorted(x["file"] for x in exp),
          f"{rec['id']} needed file multiset equality")
    bin_order = [n["file"] for n in needs]
    check(bin_order == sorted(bin_order),
          f"{rec['id']} binary verneed order {bin_order} (informational)")
    check([x["file"] for x in exp] == sorted(x["file"] for x in exp),
          f"{rec['id']} manifest needed sorted by file (canonicalization)")
    for n, x in zip(sorted(needs, key=lambda n: n["file"]),
                    sorted(exp, key=lambda x: x["file"])):
        tag = f"{rec['id']}[{x['file']}]"
        check(n["file"] == x["file"], f"{tag} vn_file string == {x['file']!r}")
        got = sorted(n["aux"], key=lambda a: (a["name"], a["other"]))
        want = sorted(x["versions"], key=lambda v: (v["name"], v["other"]))
        check(len(n["aux"]) == len(x["versions"]), f"{tag} aux count {len(n['aux'])}=={len(x['versions'])}")
        check([(a["name"], a["other"]) for a in got] == [(v["name"], v["other"]) for v in want],
              f"{tag} (name,other) multiset equality after (name,other) sort")
        check([(a["name"], a["other"]) for a in got] == [(v["name"], v["other"])
              for v in sorted(x["versions"], key=lambda v: v["name"])],
              f"{tag} manifest order is lexicographic by name")
        for a, v in zip(got, want):
            check(a["flags"] == v["flags"], f"{tag} {v['name']} flags {a['flags']}=={v['flags']} (raw vna_flags)")
            check(a["hash"] == v["hash"], f"{tag} {v['name']} hash stored {a['hash']}==manifest {v['hash']} (direct read)")
            check(elf_hash(v["name"]) == v["hash"],
                  f"{tag} {v['name']} manifest hash == SysV elf_hash(name) "
                  f"({elf_hash(v['name'])}) [inference check]")
            check(0 <= a["name_off"] < d["size"], f"{tag} {v['name']} vna_name offset {a['name_off']} inside .dynstr")
            check(all(b != 0 for b in dstr[a['name_off']:a['name_off'] + len(v['name'])])
                  and dstr[a["name_off"] + len(v["name"])] == 0,
                  f"{tag} {v['name']} NUL-terminated at offset {a['name_off']}")
        idxs = {a["other"] for a in n["aux"]}
        check(len(idxs) == len(n["aux"]), f"{tag} vna_other indexes unique")
        # .gnu.version cross-check (correct direction): every symbol version
        # reference >=2 must be covered by some verneed aux index.
        if vs is not None and ds is not None:
            cnt = ds["size"] // 24
            vrefs = set(struct.unpack_from(e + f"{cnt}H", blob, vs["offset"]))
            used = {v for v in vrefs if v >= 2}
            covered = {a["other"] for n2 in needs for a in n2["aux"]}
            check(used <= covered,
                  f"{rec['id']} all .gnu.version refs {sorted(used)} covered by verneed {sorted(covered)}")
            unref = sorted(idxs - vrefs)
            print(f"   {tag} aux indexes not referenced by any dynsym (expected for RELR): {unref}")

    total_aux = sum(len(n["aux"]) for n in needs)
    total_need = len(needs)
    print(f"   {rec['id']}: needed={total_need} aux={total_aux}")
    return total_need, total_aux


manifest = json.load(open(MANIFEST))
tn = ta = 0
for cid, i in TARGETS.items():
    r = manifest["carriers"][i]
    assert r["id"] == cid
    a, b = audit(i, r)
    tn += a
    ta += b
print(f"TOTAL e01-e04: needed={tn} aux={ta}")
print("FAILURES:", len(fails))
sys.exit(1 if fails else 0)
