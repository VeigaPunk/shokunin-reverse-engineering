#!/usr/bin/env python3
"""c1-landing-extra-checks.py - round-94 LANDING-TIME verification (advisory, not a frozen counter).

The wave's CriticC1 found that the frozen agreement counter reads only label/met/exit and cannot
bind a receipt to the frozen label, to its own counts, or to the pinned tool chain (attacks 2/3).
This script is the lane's option-2 answer for the landing: it re-checks, from the committed
receipts alone, everything the receipts themselves assert:

  1. the positive receipt's `label` equals the frozen label string exactly;
  2. every forgery receipt's `label` differs from the frozen label;
  3. every receipt's `label` is byte-equal to the label recomputed from its own `counts`;
  4. `repair_sha256` (positive) equals the round-92 repair pin; `verdict_sha256` equals the v3
     pin; `counter_sha256` equals the v4 pin; the imported-battery pins match `claims.json`;
  5. `revision` equals the full measured revision;
  6. the positive receipt's fresh provenance atoms are all true and its near cells are repaired
     with `roundtrip` true.

Exit 0 iff every check passes. Receipt: JSON with one row per check.
"""

from __future__ import annotations

import hashlib
import json
import sys

DIR = ".ufo/waves/round-94/l1/scores"
CLAIMS = ".ufo/waves/round-94/claims.json"
FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
FORMAT = ("repaired {repaired} of {scored}; wrong {wrong}; unsafe {unsafe}; "
          "intact {intact} of 6; far-refused {far_refused} of {far}; "
          "fresh-roundtrip {fresh_roundtrip} of {fresh_scored}")
NAMES = ("pos", "F1", "F2", "F3")


def label_from_counts(counts: dict) -> str:
    return FORMAT.format(**counts)


def main() -> int:
    claims = json.load(open(CLAIMS))
    c1 = claims["claims"][0]
    measured = open(f"{DIR}/c1-measured-revision.txt").read().strip()
    checks = []
    ok = True

    def add(name: str, passed: bool, detail) -> None:
        nonlocal ok
        ok = ok and bool(passed)
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    for name in NAMES:
        rec = json.load(open(f"{DIR}/c1-v4-{name}.json"))
        add(f"{name}:label-recomputed-from-counts",
            rec["label"] == label_from_counts(rec["counts"]),
            {"label": rec["label"][:60], "counts_ok": rec["label"] == label_from_counts(rec["counts"])})
        add(f"{name}:revision-is-measured", rec["revision"] == measured,
            {"revision": rec["revision"]})
        add(f"{name}:verdict-sha-pin", rec["verdict_sha256"] == c1["verdict_counter_sha256"], None)
        add(f"{name}:counter-sha-pin", rec["counter_sha256"] == c1["counter_sha256"], None)
        add(f"{name}:import-sha-pins",
            rec["imported_r92_battery_sha256"] == c1["imports_sha256"]["tools/round-92/stop-boundary-repair-battery.py"]
            and rec["imported_v2_sha256"] == c1["imports_sha256"]["tools/round-92/stop-boundary-battery-v2.py"],
            None)
        if name == "pos":
            add("pos:label-equals-frozen-label", rec["label"] == FROZEN_LABEL, None)
            add("pos:repair-sha-pin", rec["repair_sha256"] ==
                "ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1", None)
            prov = rec["fresh_provenance"]
            add("pos:fresh-provenance-atoms-true",
                prov["marker_in_mutated"] and prov["marker_absent_in_original"]
                and prov["deterministic"] and not prov["collides_public_packed"],
                {k: prov[k] for k in ("marker_in_mutated", "marker_absent_in_original",
                                      "deterministic", "collides_public_packed")})
            near = [c for c in rec["fresh_cells"] if c.get("kind") == "near"]
            add("pos:fresh-near-cells-repaired-and-roundtrip",
                len(near) == 2 and all(c["class"] == "repaired" and c.get("roundtrip") is True
                                       for c in near),
                [{"kind": c.get("kind"), "class": c["class"], "roundtrip": c.get("roundtrip")}
                 for c in near])
        else:
            add(f"{name}:label-differs-from-frozen-label", rec["label"] != FROZEN_LABEL, None)
    out = {"tool": "tools/round-94/c1-landing-extra-checks.py",
           "advisory": True, "measured_revision": measured,
           "ok": ok, "checks": checks}
    with open(f"{DIR}/c1-v4-landing-extra-checks.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({"ok": ok, "failed": [c["check"] for c in checks if not c["passed"]]}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
