import sys, struct, urllib.request, datetime, json, hashlib
BASE = "https://download.avm.de/fritzbox/"
def rng(url, start, length):
    req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{start+length-1}", "User-Agent": "kaidoku-r50-src"})
    with urllib.request.urlopen(req, timeout=60) as r:
        code = r.status
        data = r.read()
        return code, data
def octal(b):
    s = b.rstrip(b"\x00 ").decode() or "0"
    return int(s, 8)
def walk(path):
    url = BASE + path
    off = 0; members = []; pending_name = None
    while True:
        code, hdr = rng(url, off, 512)
        if len(hdr) < 512 or hdr == b"\x00" * 512:
            break
        name = hdr[0:100].split(b"\x00")[0].decode("utf-8", "replace")
        size = octal(hdr[124:136]); typ = chr(hdr[156]) if hdr[156] else "0"
        magic = hdr[257:263]
        if typ == "L":  # GNU long name: payload is the name
            _, payload = rng(url, off + 512, ((size + 511)//512)*512)
            pending_name = payload[:size].split(b"\x00")[0].decode("utf-8", "replace")
            off += 512 + ((size + 511)//512)*512; continue
        full = pending_name or name; pending_name = None
        data_off = off + 512
        rec = {"name": full, "typeflag": typ, "size": size, "data_offset": data_off, "http": code}
        if full.endswith("filesystem.image") and size > 96:
            _, sb = rng(url, data_off, 96)
            magic_ = sb[0:4]
            e = "<" if magic_ == b"hsqs" else (">" if magic_ == b"sqsh" else None)
            if e is None:
                rec["superblock"] = {"magic": magic_.decode("latin1"), "http": code}
            else:
                ver_major, ver_minor = struct.unpack_from(e+"HH", sb, 28)
                mkfs_time = struct.unpack_from(e+"I", sb, 8)[0]
                comp = struct.unpack_from(e+"H", sb, 20)[0]
                bytes_used = struct.unpack_from(e+"Q", sb, 40)[0]
                rec["superblock"] = {"magic": magic_.decode("latin1"), "endian": "LE" if e=="<" else "BE",
                                     "major": ver_major, "minor": ver_minor,
                                     "mkfs_time": mkfs_time, "compression_id": comp, "bytes_used": bytes_used,
                                     "mkfs_eq_bytes_used": mkfs_time == bytes_used, "http": code}
        members.append(rec)
        off += 512 + ((size + 511)//512)*512
        if len(members) > 400: break
    return members
if __name__ == "__main__":
    out = {}
    for p in sys.argv[1:]:
        d = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        m = walk(p)
        out[p] = {"utc": d, "members": m}
        print(p, "utc", d, "members", len(m))
        for r in m:
            if r["name"].endswith("filesystem.image") or r["name"].endswith("kernel.image") or r["name"] in ("./var/info.txt","./var/content","./var/version"):
                print("  ", r["name"], r["typeflag"], r["size"], r["data_offset"], r.get("superblock", ""))
    json.dump(out, open("/fast/scratch/hyaku/kaidoku-r50/C1SrcAvmIndex/walk/walk.json", "w"), indent=1)
