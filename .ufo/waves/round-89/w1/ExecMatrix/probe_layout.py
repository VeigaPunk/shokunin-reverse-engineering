#!/usr/bin/env python3
"""probe_layout.py - ExecMatrix r89 scratch probe: anchor layout of the packed carriers.

Packs the four pinned carriers exactly as the frozen battery does
(`upx --best -q -o packed orig`), locates PackHeader/l_info/sentinel/block0 via
the round-87 module's own locators, and dumps the 8 bytes between l_info and
block 0 so the p_info field offsets are read off the bytes, not asserted.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")
UPX = "/usr/bin/upx"
WORK = "/fast/scratch/hyaku/kaidoku-r89/ExecMatrix/probe"
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq",
     "sha256": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"},
    {"id": "xxd", "source": "/usr/bin/xxd",
     "sha256": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"},
    {"id": "libz", "source": "/usr/lib/libz.so.1.3.2",
     "sha256": "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9"},
    {"id": "dinit", "source": "/usr/bin/docker-init",
     "sha256": "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"},
]
PRE_PACKED = {  # from pre/c1-base-r88-repair.json (frozen population)
    "jq": "e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a",
    "xxd": "1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff",
    "libz": "a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b",
    "dinit": "b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7",
}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(argv, env):
    p = subprocess.run(argv, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def main():
    rep = load_module(R87, "r87repair")
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(os.path.join(WORK, "home"))
    os.makedirs(os.path.join(WORK, "tmp"))
    env = {"HOME": os.path.join(WORK, "home"), "LANG": "C",
           "PATH": os.environ.get("PATH") or "/usr/bin",
           "TMPDIR": os.path.join(WORK, "tmp")}
    print(sys.version.split()[0])
    for c in CARRIERS:
        d = os.path.join(WORK, c["id"])
        os.makedirs(d)
        orig = os.path.join(d, "orig")
        shutil.copy2(c["source"], orig)
        packed = os.path.join(d, "packed")
        rc, txt = run([UPX, "--best", "-q", "-o", packed, orig], env)
        with open(packed, "rb") as fh:
            data = fh.read()
        ph_off, ph = rep.find_packheader(data)
        m, s, walk = rep.find_linfo(data, ph_off, ph)
        b0 = m + 20
        sz_unc, sz_cpr = struct.unpack_from("<II", data, b0)
        rec = {
            "pack_rc": rc,
            "pack_tail": txt.strip().splitlines()[-1:],
            "orig_size": os.path.getsize(orig),
            "packed_sha256": hashlib.sha256(data).hexdigest(),
            "matches_pre": PRE_PACKED.get(c["id"], "n/a") == hashlib.sha256(data).hexdigest(),
            "ph_off": ph_off, "l_off": m, "sentinel": s,
            "b0": b0,
            "ph": {k: v for k, v in ph.items() if isinstance(v, (int, str, bool))},
            "l_hex_m4": data[m - 4:m + 44].hex(),
            "l_version": data[m + 10], "l_format": data[m + 11],
            "at_l12": hex(struct.unpack_from("<I", data, m + 12)[0]),
            "at_l16": hex(struct.unpack_from("<I", data, m + 16)[0]),
            "b0_sz_unc": sz_unc, "b0_sz_cpr": sz_cpr,
            "b0_method": data[b0 + 8], "b0_ftid": data[b0 + 9],
            "b0_cto8": data[b0 + 10], "b0_unused": data[b0 + 11],
            "cpr_plus8_fits": bool(sz_cpr + 8 <= sz_unc),
            "t_rc": None,
        }
        rc2, txt2 = run([UPX, "-t", "-q", packed], env)
        rec["t_rc"] = rc2
        rec["t_tail"] = txt2.strip().splitlines()[-1:]
        print(json.dumps({c["id"]: rec}, indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
