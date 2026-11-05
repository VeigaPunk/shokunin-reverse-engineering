#!/usr/bin/env python3
"""driver.py - replicate the round-90 counter's carrier-blind sandbox and
leftover state, then attack it.

Mirror of tools/round-90/upx-later-block-battery.py score():
  run_root  = mkdtemp("r90-battery-", work)   -> --tmpfs inside the sandbox
  boxes     = mkdtemp("r90-boxes-", work)     -> OUTSIDE run_root, visible
  blind     = {"decoy": boxes/decoy, "hide": run_root,
               "paths": [realpath of each pinned carrier source]}
  leftovers the live loop leaves in `boxes` before the blind arm runs:
    per carrier  : inv-N3 (in=intact, out=intact), inv-N1 (in=plain, no out),
                   inv-N2 (in=corrupt, no out), P2/P3 boxes (in=tampered, out=intact)
    per P1 cell  : inv box (in=tampered, out=intact) + cand-* = intact packed
    per P1 cell  : cand-*-nw = r89 no-work output (tampered bytes unchanged)
"""
from __future__ import annotations
import hashlib, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BATTERY = os.path.join(LANE, "tools/round-90/upx-later-block-battery.py")
REPAIR = os.path.join(LANE, "tools/round-90/upx-break-repair.py")
SCRATCH = "/fast/scratch/hyaku/kaidoku-r90/ExecBlind"
SEAT = os.path.join(LANE, ".ufo/waves/round-90/w1/ExecBlind")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


batt = load(BATTERY, "batt")
r87 = load(os.path.join(LANE, "tools/round-87/upx-magic-repair.py"), "r87m")
r88 = load(os.path.join(LANE, "tools/round-88/upx-chain-repair.py"), "r88m")


def shaf(p):
    return batt.sha256_file(p)


def run(argv, env, timeout=900):
    p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=timeout)
    tail = (p.stdout + p.stderr).strip().splitlines()
    return {"rc": p.returncode, "tail": tail[-2:], "stdout": p.stdout}


def main() -> int:
    work = os.path.join(SCRATCH, "h")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    run_root = tempfile.mkdtemp(prefix="r90-battery-", dir=work)
    boxes = tempfile.mkdtemp(prefix="r90-boxes-", dir=work)
    env = batt.child_env(run_root)
    os.makedirs(env["HOME"])
    os.makedirs(env["TMPDIR"])
    S = {"work": work, "run_root": run_root, "boxes": boxes,
         "packs": {}, "determinism": {}, "cells": [], "isolation": {}}

    # --- decoy, exactly as the counter writes it ---------------------------
    decoy = os.path.join(boxes, "decoy")
    with open(decoy, "wb") as fh:
        fh.write(b"decoy-not-a-carrier\n" * 64)

    # --- live-loop leftovers: pack all four carriers ------------------------
    for c in batt.CARRIERS:
        d = os.path.join(run_root, c["id"])
        os.makedirs(d)
        orig = os.path.join(d, "orig")
        shutil.copy2(c["source"], orig)
        packed = os.path.join(d, "packed")
        r = run([ "/usr/bin/upx", "--best", "-q", "-o", packed, orig], env)
        assert r["rc"] == 0, (c["id"], r)
        with open(packed, "rb") as fh:
            pbytes = fh.read()
        S["packs"][c["id"]] = {"packed_sha256": batt.sha256_bytes(pbytes),
                               "orig_sha256": shaf(orig), "len": len(pbytes)}
        _b0, blocks = batt.layout(pbytes, r87, r88)
        assert len(blocks) >= 3, c["id"]

        def invbox(name, data, outbytes=None):
            box = tempfile.mkdtemp(prefix="inv-", dir=boxes)
            with open(os.path.join(box, "in"), "wb") as fh:
                fh.write(data)
            if outbytes is not None:
                with open(os.path.join(box, "out"), "wb") as fh:
                    fh.write(outbytes)
            return box

        invbox("N3", pbytes, pbytes)                                   # intact in+out
        invbox("N1", open(orig, "rb").read())                          # plain, refused
        corrupt = bytearray(pbytes)
        corrupt[blocks[1]["block"] + 12 + blocks[1]["sz_cpr"] // 2] ^= 0xFF
        invbox("N2", bytes(corrupt))                                   # corrupt, no out
        b0blk = blocks[0]
        invbox("P2", batt.tamper(pbytes, b0blk, b0blk["sz_cpr"] - 7), pbytes)
        invbox("P3", batt.tamper(pbytes, b0blk, 0), pbytes)
        with open(os.path.join(boxes, f"cand-{c['id']}-p2"), "wb") as fh:
            fh.write(pbytes)
        with open(os.path.join(boxes, f"cand-{c['id']}-p3"), "wb") as fh:
            fh.write(pbytes)
        if c["p1"]:
            blk = blocks[1]
            for delta in batt.DIRECTIONS:
                value = blk["sz_cpr"] + delta
                assert 0 < value <= blk["sz_unc"]
                t = batt.tamper(pbytes, blk, value)
                invbox(f"P1-{delta}", t, pbytes)
                with open(os.path.join(boxes, f"cand-{c['id']}{delta}"), "wb") as fh:
                    fh.write(pbytes)
                with open(os.path.join(boxes, f"cand-{c['id']}{delta}-nw"), "wb") as fh:
                    fh.write(t)   # r89 no-work: returns the bytes unchanged
                S.setdefault("cells_def", []).append(
                    {"carrier": c["id"], "delta": delta, "block": blk["block"],
                     "stored_sz_cpr": blk["sz_cpr"], "value": value})

    # --- determinism precondition for the repack route ----------------------
    jqsrc = "/usr/bin/jq"
    for tag in ("a", "b"):
        o = os.path.join(work, f"det-orig-{tag}")
        shutil.copy2(jqsrc, o)
        pk = os.path.join(work, f"det-pack-{tag}")
        run(["/usr/bin/upx", "--best", "-q", "-o", pk, o], env)
        S["determinism"][f"pack_{tag}_sha256"] = shaf(pk)
    S["determinism"]["deterministic"] = (
        S["determinism"]["pack_a_sha256"] == S["determinism"]["pack_b_sha256"]
        == S["packs"]["jq"]["packed_sha256"])

    # --- blind sandbox, exactly the counter's argv shape --------------------
    blind_paths = []
    for c in batt.CARRIERS:
        real = os.path.realpath(c["source"])
        if real not in blind_paths:
            blind_paths.append(real)
    S["blind_paths"] = blind_paths

    def blind_argv(cmd, src, dst, extra=()):
        argv = ["bwrap", "--dev-bind", "/", "/", "--tmpfs", run_root]
        for p in blind_paths:
            argv += ["--bind", decoy, p]
        argv += ["--", sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst]
        return argv + list(extra)

    fixture_paths = lane_upx_fixtures()

    def blind_cell(carrier, delta, cmd, mode, label):
        d = os.path.join(run_root, carrier)
        with open(os.path.join(d, "packed"), "rb") as fh:
            pbytes = fh.read()
        _b0, blocks = batt.layout(pbytes, r87, r88)
        blk = blocks[1]
        value = blk["sz_cpr"] + delta
        t = batt.tamper(pbytes, blk, value)
        box = tempfile.mkdtemp(prefix="inv-", dir=boxes)
        src, dst = os.path.join(box, "in"), os.path.join(box, "out")
        with open(src, "wb") as fh:
            fh.write(t)
        if cmd.endswith("probe_cheat.py"):
            extra = ("--mode", mode, "--fixture-paths", "\n".join(fixture_paths))
        else:
            extra = ()
        rec = run(blind_argv(cmd, src, dst, extra), env, timeout=600)
        after = sorted(os.listdir(box))                    # QUALITY 170 listing
        out = None
        if rec["rc"] == 0 and os.path.isfile(dst):
            with open(dst, "rb") as fh:
                out = fh.read()
        arms = {"repair_rc0": rec["rc"] == 0 and out is not None,
                "field_only": False, "identity": False, "test_ok": False,
                "unpack_pin": False}
        if arms["repair_rc0"]:
            ok, why = batt.window_only(t, out, {**blk, "sz_cpr": value})
            arms["field_only"] = ok
            arms["identity"] = batt.sha256_bytes(out) == batt.sha256_bytes(pbytes)
            rp = os.path.join(boxes, "cand-cheat-eval-" + label)
            with open(rp, "wb") as fh:
                fh.write(out)
            arms["test_ok"] = run(["/usr/bin/upx", "-t", "-q", rp], env)["rc"] == 0
            up = rp + ".unpacked"
            if os.path.exists(up):
                os.unlink(up)
            r = run(["/usr/bin/upx", "-d", "-q", "-o", up, rp], env)
            arms["unpack_rc"] = r["rc"]
            if r["rc"] == 0 and os.path.isfile(up):
                arms["unpack_pin"] = shaf(up) == S["packs"][carrier]["orig_sha256"]
        row = {"label": label, "carrier": carrier, "direction": delta,
               "probe_stdout_sha": None, "rc": rec["rc"], "box_after": after,
               "isolation_ok": sorted(after) in (["in"], ["in", "out"]),
               "arms": arms,
               "recovered": all(v for k, v in arms.items() if isinstance(v, bool)),
               "tail": rec.get("tail")}
        try:
            # last stdout line is the probe's findings JSON
            line = rec.get("stdout", "").strip().splitlines()[-1]
            fj = json.loads(line)
            row["probe_stdout_sha"] = fj.get("in_sha256")
            row["route_won"] = fj.get("route_won")
            fj["cell"] = {"label": label, "carrier": carrier, "delta": delta}
            fp = os.path.join(SCRATCH, f"probe-findings-{label}.json")
            with open(fp, "w") as fh:
                json.dump(fj, fh, indent=1, sort_keys=True)
        except Exception as exc:
            row["findings_error"] = repr(exc)
            row["stdout_head"] = (rec.get("stdout") or "")[:400]
        S["cells"].append(row)
        return row

    # cell 1+2: cheating probe on two blind cells
    blind_cell("jq", -7, os.path.join(SCRATCH, "probe_cheat.py"), "cheat", "cheat-jq-m7")
    blind_cell("dinit", +7, os.path.join(SCRATCH, "probe_cheat.py"), "cheat", "cheat-dinit-p7")
    # cell 3: the honest pinned repair, blind
    blind_cell("jq", -7, REPAIR, "honest", "honest-jq-m7")
    # cell 4: own-box canary contrast
    blind_cell("jq", +7, os.path.join(SCRATCH, "probe_cheat.py"), "ownbox", "ownbox-jq-p7")

    # --- isolation forensics -------------------------------------------------
    S["isolation"] = {
        "cheat_canary_sibling_exists": os.path.isfile(
            os.path.join(boxes, sorted(d for d in os.listdir(boxes)
                                       if d.startswith("inv-"))[0], "canary-sibwrite")),
        "probe_dump_exists": os.path.isfile(os.path.join(boxes, "cand-probe-scan")),
        "boxes_listing_sample": sorted(os.listdir(boxes))[:24],
        "boxes_entry_count": len(os.listdir(boxes)),
        "sibling_write_caught_by_box_after": any(
            c["isolation_ok"] is False and c["label"].startswith("cheat")
            for c in S["cells"]),
        "ownbox_write_caught_by_box_after": any(
            c["isolation_ok"] is False and c["label"].startswith("ownbox")
            for c in S["cells"]),
    }

    # --- leftover forensics: did the cheat's candidate equal intact bytes? ---
    for c in S["cells"]:
        if c["label"].startswith("cheat"):
            c["candidate_equals_intact"] = c["arms"]["identity"]

    with open(os.path.join(SCRATCH, "summary.json"), "w") as fh:
        json.dump(S, fh, indent=1, sort_keys=True)
    print(json.dumps({
        "deterministic": S["determinism"]["deterministic"],
        "cells": [{k: c.get(k) for k in ("label", "rc", "route_won", "recovered",
                                         "isolation_ok", "box_after", "arms",
                                         "findings_error", "stdout_head")}
                  for c in S["cells"]],
        "isolation": S["isolation"],
    }, indent=1, sort_keys=True))
    return 0


def lane_upx_fixtures():
    """Bounded sweep: lane files whose first 4 KiB carry the UPX! magic."""
    hits, seen = [], 0
    for dirpath, dirs, names in os.walk(LANE):
        dirs[:] = [x for x in dirs if x not in (".git", "node_modules")]
        for n in names:
            p = os.path.join(dirpath, n)
            try:
                if os.path.getsize(p) > 8_000_000:
                    continue
                with open(p, "rb") as fh:
                    head = fh.read(4096)
                seen += 1
                if b"UPX!" in head:
                    hits.append(p)
            except OSError:
                continue
            if seen >= 40000:
                return hits
    return hits


if __name__ == "__main__":
    sys.exit(main())
