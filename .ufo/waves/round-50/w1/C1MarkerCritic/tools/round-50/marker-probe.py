#!/usr/bin/env python3
"""C1MarkerCritic draft probe (wave 1, not frozen, not a lane instrument).

Reads a FRITZ!OS tar image, extracts NOTHING into the lane tree: it streams the
named member into a scratch file, reports the SquashFS superblock fields the
AVM-marker clause reads, the number of non-zero bytes after round_up(bytes_used,
4096) (the trailer residue), and the member sha256. Vendor bytes stay in scratch.

usage: marker-probe.py SCRATCH_DIR IMAGE [MEMBER ...]
  default MEMBER: ./var/tmp/filesystem.image
exit: 0 probed every member; 2 usage/environment error (member missing counts).
"""
import hashlib
import os
import struct
import sys
import tarfile


def sb(head, size):
    magic = head[:4]
    if magic not in (b"hsqs", b"sqsh"):
        return {"magic": magic.decode("latin1")}
    e = "<" if magic == b"hsqs" else ">"
    mk = struct.unpack_from(e + "I", head, 8)[0]
    bu = struct.unpack_from(e + "Q", head, 40)[0]
    return dict(
        magic=magic.decode("latin1"),
        version=(struct.unpack_from(e + "H", head, 28)[0], struct.unpack_from(e + "H", head, 30)[0]),
        compression=struct.unpack_from(e + "H", head, 20)[0],
        inodes=struct.unpack_from(e + "I", head, 4)[0],
        block_size=struct.unpack_from(e + "I", head, 12)[0],
        mkfs_time=mk,
        bytes_used=bu,
        marker=(mk == bu),
        round_up_4096_minus_bytes_used=((bu + 4095) // 4096) * 4096 - bu,
        member_size=size,
    )


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    scratch, image, members = argv[1], argv[2], argv[3:] or ["./var/tmp/filesystem.image"]
    os.makedirs(scratch, exist_ok=True)
    tf = tarfile.open(image)
    rc = 0
    for name in members:
        try:
            m = tf.getmember(name)
        except KeyError:
            print(f"{os.path.basename(image)} {name} MISSING")
            rc = 2
            continue
        f = tf.extractfile(m)
        head = f.read(96)
        out = os.path.join(scratch, "probe-member.bin")
        h = hashlib.sha256()
        f.seek(0)
        bu = None
        with open(out, "wb") as w:
            while True:
                c = f.read(1 << 20)
                if not c:
                    break
                h.update(c)
                w.write(c)
        info = sb(head, m.size)
        if "bytes_used" in info:
            with open(out, "rb") as r:
                r.seek(info["bytes_used"])
                tail = r.read()
            info["tail_len"] = len(tail)
            info["tail_nonzero"] = sum(1 for b in tail if b)
        info["member_sha256"] = h.hexdigest()
        print(os.path.basename(image), name, info)
        os.remove(out)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
