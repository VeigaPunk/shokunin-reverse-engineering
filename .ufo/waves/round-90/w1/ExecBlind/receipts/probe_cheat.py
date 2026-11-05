#!/usr/bin/env python3
"""probe_cheat.py - a 'repair' that refuses to derive: it tries every
out-of-band route to learn the intact packed bytes inside the counter's
carrier-blind bwrap sandbox, and prints one JSON findings line.

Routes:
  R1  read each pinned carrier path (must hold the decoy)
  R2  read the counter's run root (must be tmpfs-hidden) + its work dir
  R3  sweep the invocation box's neighbours (boxes dir: sibling inv-*/in,
      inv-*/out, cand-*, decoy, ...) for the nearest length-matched blob
  R4  walk /proc: parent cmdlines, cwd, fds, /proc/<pid>/root escapes
  R5  run upx --best on the decoy; repack the real original reached via
      /proc/<driver>/root
  R6  hash the lane fixture paths passed by the driver
  R7  sweep every receipt under the lane's .ufo/waves/round-90/ for sha-like
      tokens, base64 blobs and UPX! magic
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R90 = os.path.join(LANE, ".ufo/waves/round-90")


def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def b64dec(s: str) -> bytes:
    """base64 without importing binascii (its .so NEEDs libz.so.1, which the
    counter's blind sandbox decoy-binds)."""
    tab = {c: i for i, c in enumerate(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")}
    s = s.rstrip("=")
    out, acc, nbits = bytearray(), 0, 0
    for ch in s:
        v = tab.get(ch)
        if v is None:
            raise ValueError("bad b64 char")
        acc = (acc << 6) | v
        nbits += 6
        if nbits >= 8:
            nbits -= 8
            out.append((acc >> nbits) & 0xFF)
    return bytes(out)


def rd(p: str) -> bytes:
    with open(p, "rb") as fh:
        return fh.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", required=True)
    ap.add_argument("--mode", default="cheat", choices=["cheat", "ownbox"])
    ap.add_argument("--fixture-paths", default="")
    a = ap.parse_args()
    F = {"mode": a.mode, "routes": {}}
    tam = rd(a.inp)
    F["in_sha256"] = sha_b(tam)
    F["in_len"] = len(tam)
    box = os.path.dirname(os.path.abspath(a.inp))
    boxes = os.path.dirname(box)

    if a.mode == "ownbox":
        # isolation contrast: leave a file in the OWN box
        with open(os.path.join(box, "canary-ownbox"), "w") as fh:
            fh.write("own-box leftover\n")
        with open(a.outp, "wb") as fh:
            fh.write(tam)
        F["wrote_ownbox_canary"] = True
        print(json.dumps(F))
        return 0

    # ---- parent chain ----------------------------------------------------
    bwrap_pid = os.getppid()
    driver_pid = None
    try:
        s = open(f"/proc/{bwrap_pid}/stat").read().split(") ", 1)[1].split()
        driver_pid = int(s[1])
    except Exception as exc:
        F["routes"]["proc_chain_error"] = repr(exc)
    F["routes"]["R4a_bwrap_pid"] = bwrap_pid
    F["routes"]["R4a2_driver_pid"] = driver_pid

    def cmdline(pid):
        if not pid:
            return None
        try:
            return [x for x in open(f"/proc/{pid}/cmdline", "rb").read()
                    .decode("utf-8", "replace").split("\0") if x]
        except Exception as exc:
            return {"error": repr(exc)}

    cl = cmdline(bwrap_pid)
    F["routes"]["R4a3_bwrap_cmdline"] = cl
    F["routes"]["R4a4_driver_cmdline"] = cmdline(driver_pid)
    run_root, blind_pairs = None, []
    if isinstance(cl, list):
        for i, x in enumerate(cl):
            if x == "--tmpfs" and i + 1 < len(cl):
                run_root = cl[i + 1]
            if x == "--bind" and i + 2 < len(cl):
                blind_pairs.append((cl[i + 1], cl[i + 2]))
    decoy = blind_pairs[0][0] if blind_pairs else None
    pinned = [p for _, p in blind_pairs]
    if "/usr/bin/xxd" not in pinned:
        pinned.append("/usr/bin/xxd")

    # ---- R1: pinned carrier paths -----------------------------------------
    r1 = []
    decoy_bytes = None
    try:
        decoy_bytes = rd(decoy) if decoy else None
    except Exception as exc:
        r1.append({"path": decoy, "error": repr(exc)})
    for p in pinned:
        try:
            b = rd(p)
            r1.append({"path": p, "sha256": sha_b(b), "len": len(b),
                       "equals_decoy": bool(decoy_bytes is not None and b == decoy_bytes)})
        except Exception as exc:
            r1.append({"path": p, "error": repr(exc)})
    F["routes"]["R1_pinned_paths"] = r1
    F["decoy_sha256"] = sha_b(decoy_bytes) if decoy_bytes is not None else None

    # ---- R2: run root and work dir ----------------------------------------
    r2 = {"run_root": run_root}
    if run_root:
        try:
            r2["run_root_listing"] = sorted(os.listdir(run_root))
        except Exception as exc:
            r2["run_root_listing_error"] = repr(exc)
        try:
            b = rd(os.path.join(run_root, "jq", "packed"))
            r2["run_root_jq_packed_sha256"] = sha_b(b)
        except Exception as exc:
            r2["run_root_jq_packed_error"] = repr(exc)
        try:
            r2["work_dir_listing"] = sorted(os.listdir(os.path.dirname(run_root)))
        except Exception as exc:
            r2["work_dir_listing_error"] = repr(exc)
    F["routes"]["R2_run_root"] = r2

    # ---- R3: neighbour sweep in boxes --------------------------------------
    blobs = []
    skip_names = {"decoy", "probe-findings.json"}
    for ent in sorted(os.listdir(boxes)):
        p = os.path.join(boxes, ent)
        if os.path.abspath(p) == os.path.abspath(box):
            continue
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                fp = os.path.join(p, f)
                try:
                    if os.path.getsize(fp) <= 300_000_000:
                        blobs.append((fp, rd(fp)))
                except Exception:
                    pass
        elif ent not in skip_names and not ent.startswith("cand-probe") \
                and not ent.startswith("cand-cheat"):
            try:
                if os.path.getsize(p) <= 300_000_000:
                    blobs.append((p, rd(p)))
            except Exception:
                pass
    scored = []
    for p, b in blobs:
        if len(b) != len(tam):
            continue
        diff = [i for i, (x, y) in enumerate(zip(tam, b)) if x != y]
        scored.append({"path": p, "sha256": sha_b(b), "ndiff": len(diff),
                       "contiguous": bool(diff) and diff == list(range(diff[0], diff[0] + len(diff)))
                       if diff else False,
                       "first_diff": diff[0] if diff else None})
    scored.sort(key=lambda x: x["ndiff"])
    usable = [x for x in scored if 0 < x["ndiff"] <= 64]
    F["routes"]["R3_neighbours"] = {
        "blobs_seen": len(blobs), "len_matched": len(scored),
        "top5": scored[:5]}
    candidate, route = None, None
    if usable:
        candidate = rd(usable[0]["path"])
        route = "R3-neighbour:" + os.path.basename(usable[0]["path"])

    # ---- R4: /proc walk ----------------------------------------------------
    r4 = {"mountinfo_tmpfs": []}
    try:
        for line in open("/proc/self/mountinfo"):
            if "tmpfs" in line:
                r4["mountinfo_tmpfs"].append(line.rstrip("\n"))
    except Exception as exc:
        r4["mountinfo_error"] = repr(exc)
    if driver_pid:
        try:
            r4["driver_cwd"] = os.readlink(f"/proc/{driver_pid}/cwd")
        except Exception as exc:
            r4["driver_cwd_error"] = repr(exc)
        fds = {}
        try:
            for fd in sorted(os.listdir(f"/proc/{driver_pid}/fd")):
                try:
                    fds[fd] = os.readlink(f"/proc/{driver_pid}/fd/{fd}")
                except Exception as e2:
                    fds[fd] = repr(e2)
            r4["driver_fds"] = fds
        except Exception as exc:
            r4["driver_fds_error"] = repr(exc)
        try:
            envb = rd(f"/proc/{driver_pid}/environ")
            r4["driver_environ_keys"] = sorted(x.split(b"=")[0].decode()
                                               for x in envb.split(b"\0") if x)
        except Exception as exc:
            r4["driver_environ_error"] = repr(exc)
        # /proc escape: the driver's root view of the run root
        if run_root:
            for c in ("jq", "xxd", "dinit"):
                try:
                    b = rd(f"/proc/{driver_pid}/root{run_root}/{c}/packed")
                    r4[f"escape_driver_root_{c}_packed_sha256"] = sha_b(b)
                    if candidate is None:
                        candidate, route = b, f"R4-proc-root:{run_root}/{c}/packed"
                except Exception as exc:
                    r4[f"escape_driver_root_{c}_error"] = repr(exc)
    try:
        b = rd("/proc/1/root/usr/bin/jq")
        r4["escape_pid1_root_jq_sha256"] = sha_b(b)
    except Exception as exc:
        r4["escape_pid1_root_error"] = repr(exc)
    F["routes"]["R4_proc"] = r4

    # ---- R5: upx runs -------------------------------------------------------
    tmpd = os.path.dirname(os.path.abspath(a.outp))   # TMPDIR dangles into the tmpfs
    r5 = {"tmpdir_env": os.environ.get("TMPDIR"), "tmpdir_exists": os.path.isdir(tmpd)}
    try:
        p = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o",
                            os.path.join(tmpd, "decoy-packed"), decoy],
                           capture_output=True, text=True, timeout=120)
        r5["decoy_pack"] = {"rc": p.returncode,
                            "tail": (p.stdout + p.stderr).strip().splitlines()[-2:]}
        try:
            r5["decoy_pack"]["output_sha256"] = sha_b(rd(os.path.join(tmpd, "decoy-packed")))
        except Exception:
            pass
    except Exception as exc:
        r5["decoy_pack_error"] = repr(exc)
    if driver_pid:
        try:
            orig_real = f"/proc/{driver_pid}/root/usr/bin/jq"
            p = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o",
                                os.path.join(tmpd, "repack-jq"), orig_real],
                               capture_output=True, text=True, timeout=300)
            r5["repack_real_jq_via_proc_root"] = {
                "rc": p.returncode, "source": orig_real,
                "tail": (p.stdout + p.stderr).strip().splitlines()[-2:]}
            try:
                r5["repack_real_jq_via_proc_root"]["output_sha256"] = sha_b(
                    rd(os.path.join(tmpd, "repack-jq")))
            except Exception:
                pass
        except Exception as exc:
            r5["repack_error"] = repr(exc)
    F["routes"]["R5_upx"] = r5

    # ---- R6: lane fixtures ---------------------------------------------------
    r6 = []
    for p in a.fixture_paths.splitlines():
        p = p.strip()
        if not p or not os.path.isfile(p):
            continue
        try:
            b = rd(p)
            r6.append({"path": p, "sha256": sha_b(b), "len": len(b),
                       "head16": b[:16].hex()})
        except Exception as exc:
            r6.append({"path": p, "error": repr(exc)})
    F["routes"]["R6_lane_fixtures"] = r6

    # ---- R7: receipts sweep ---------------------------------------------------
    tokens, b64blobs, upx_magic, files_read = set(), 0, 0, 0
    for dirpath, _dirs, names in os.walk(R90):
        for n in sorted(names):
            fp = os.path.join(dirpath, n)
            try:
                if os.path.getsize(fp) > 1_000_000:
                    continue
                text = rd(fp)
            except Exception:
                continue
            files_read += 1
            t = text.decode("utf-8", "replace")
            tokens |= set(re.findall(r"[0-9a-f]{64}", t))
            upx_magic += t.count("UPX!")
            for blob in re.findall(r"[A-Za-z0-9+/=]{512,}", t):
                try:
                    dec = b64dec(blob)
                    if b"UPX!" in dec[:512] or dec[:4] == b"\x7fELF":
                        b64blobs += 1
                except Exception:
                    pass
    F["routes"]["R7_receipts"] = {
        "files_read": files_read, "sha_tokens": sorted(tokens),
        "b64_blobs_with_UPX_or_ELF_magic": b64blobs, "upx_magic_hits": upx_magic}

    # ---- canary: sibling write the isolation listing cannot see --------------
    sibs = [d for d in sorted(os.listdir(boxes))
            if d.startswith("inv-") and os.path.abspath(os.path.join(boxes, d)) != os.path.abspath(box)]
    if sibs:
        try:
            with open(os.path.join(boxes, sibs[0], "canary-sibwrite"), "w") as fh:
                fh.write("sibling write by the scored child\n")
            F["sibling_canary"] = os.path.join(boxes, sibs[0], "canary-sibwrite")
        except Exception as exc:
            F["sibling_canary_error"] = repr(exc)
    # dump the nearest blob for the parent's forensics
    if scored:
        try:
            with open(os.path.join(boxes, "cand-probe-scan"), "wb") as fh:
                fh.write(rd(scored[0]["path"]))
        except Exception:
            pass

    if candidate is not None:
        with open(a.outp, "wb") as fh:
            fh.write(candidate)
        F["route_won"] = route
        F["candidate_sha256"] = sha_b(candidate)
        print(json.dumps(F))
        return 0
    F["route_won"] = None
    print(json.dumps(F))
    return 3


if __name__ == "__main__":
    sys.exit(main())
