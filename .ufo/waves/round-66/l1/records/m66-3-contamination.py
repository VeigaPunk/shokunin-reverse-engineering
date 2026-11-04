#!/usr/bin/env python3
"""M66-3 red/green: a control that reuses one fixture between its arm and its
r65-order emulation scores the a2 arm green on nothing.

Contaminated: one root, arm probe first (writes __pycache__), then the
r65-order emulation scans that same root BEFORE its own probe and sees the
leftover cache -> ok false -> the control "meets" the a2 arm without any
counter defect being present.

Corrected: two roots, so the r65-order emulation sees the empty cache it is
actually entitled to see -> ok true -> the control does not meet the arm.
"""
import argparse, importlib.util, json, os, shutil, sys, tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def main():
    v1 = load(LANE / "tools/round-65/jsc-closure-matrix.py", "v1")
    v2 = load(LANE / "tools/round-66/closure-boundary.py", "v2")
    v1_pin = v2.V1_PIN
    import hashlib
    got = hashlib.sha256((LANE / v2.V1_PATH).read_bytes()).hexdigest()
    scratch = Path(tempfile.mkdtemp(prefix="r66-m663-", dir=os.environ.get("TMPDIR") or None))
    try:
        def r65_order(root):
            cache = v1.cache_entries(root)
            ok, msg = v2.fixture_probe(v1, "/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python",
                                       root, guarded=False)()
            return {"cache_present": cache, "probe_ok": ok, "ok": not cache and ok}

        # contaminated: one shared root
        shared = scratch / "shared"; v2.write_fixture(shared)
        v2.closure_state(v1, shared, shared / "probe.jsc", shared / "node", shared / "interp",
                         v2.pins_for(shared, v2.FIXTURE_RELS), len(v2.FIXTURE_RELS) + 3,
                         v2.fixture_probe(v1, "/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python",
                                          shared, guarded=False),
                         {"probe": v2.sha256_file(shared / "probe.jsc"),
                          "node": v2.sha256_file(shared / "node"),
                          "interpreter": v2.sha256_file(shared / "interp")})
        contaminated = r65_order(shared)
        # corrected: separate roots
        arm = scratch / "arm"; v2.write_fixture(arm)
        v2.closure_state(v1, arm, arm / "probe.jsc", arm / "node", arm / "interp",
                         v2.pins_for(arm, v2.FIXTURE_RELS), len(v2.FIXTURE_RELS) + 3,
                         v2.fixture_probe(v1, "/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python",
                                          arm, guarded=False),
                         {"probe": v2.sha256_file(arm / "probe.jsc"),
                          "node": v2.sha256_file(arm / "node"),
                          "interpreter": v2.sha256_file(arm / "interp")})
        ctl = scratch / "ctl"; v2.write_fixture(ctl)
        corrected = r65_order(ctl)
        result = {
            "v1_path": v2.V1_PATH, "v1_pin_expected": v1_pin, "v1_sha256_observed": got,
            "contaminated": {"r65_order_state": contaminated,
                             "control_meets_a2_arm": contaminated["ok"] is False,
                             "arm": "a2-unguarded-fixture-red"},
            "corrected": {"r65_order_state": corrected,
                          "control_meets_a2_arm": corrected["ok"] is False,
                          "arm": "a2-unguarded-fixture-red"},
            "red_demonstrated": (contaminated["ok"] is False) and (corrected["ok"] is True),
        }
        text = json.dumps(result, indent=1, sort_keys=True) + "\n"
        out = LANE / ".ufo/waves/round-66/l1/records/m66-3-contamination.json"
        out.write_text(text)
        sys.stdout.write(json.dumps({k: result[k] for k in ("red_demonstrated",)} ) + "\n")
        return 0 if result["red_demonstrated"] else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
