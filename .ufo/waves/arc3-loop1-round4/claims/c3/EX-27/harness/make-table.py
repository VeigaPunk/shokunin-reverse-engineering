#!/usr/bin/env python3
"""Build EX-27's before→after table from the two battery runs (round-3 vs round-4)."""
import json
from pathlib import Path

BASE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c3/EX-27/runs")
before = json.loads((BASE / "regress-r3-baseline-7cd19c3c.json").read_text())
after = json.loads((BASE / "regress-r4-final-29bb45ae.json").read_text())

key = lambda r: (r["leg"], r["name"])
b = {key(r): r for r in before["rows"]}
a = {key(r): r for r in after["rows"]}
names = list(b) + [k for k in a if k not in b]

INTEREST = {
    ("A", "A1_cp_a"), ("A", "A8_inplace_modify_no_restore"), ("A", "A12_reflink_replace"),
    ("A", "A14_chmod_only"), ("A", "A15_delete_after_capture"),
    ("B", "r1-canonical-vs-live"), ("B", "ex35-partial-1of5-default-vs-require5"),
    ("B", "synth-v1-stanza-vs-live"), ("B", "synth-v1-sums-vs-live"),
    ("C", "v2-utc-render-tz-invariant"), ("C", "v1-label-defect-declared"),
    ("D", "selftest-case-count"), ("D", "selftest-prior-case-names-retained"),
    ("D", "selftest-missing-scratch"),
    ("E", "d2-eacces-capture"), ("E", "d2-failopen-both-absent"),
    ("E", "writeguard-paths-eq-out"),
    ("F", "live-pair-capture-vs-capture"), ("F", "scratch-live-pair-form"),
    ("F", "receipt-self-pin"),
    ("G", "a-sidecar-path-of-scoped-file"), ("G", "a2-sidecar-hardlink-alias"),
    ("G", "a3-control-ordinary-capture"), ("G", "b-out-parent-not-a-directory"),
    ("G", "b2-out-empty-arg"), ("G", "c-coverage-gate-duplicate-stanzas"),
    ("G", "c2-coverage-gate-distinct-five"), ("G", "d-both-absent-plain"),
    ("G", "d2-both-absent-error-carrying"), ("G", "d3-readme-ruling-text"),
    ("I", "eq-same-content-rewrite-inplace-ctime-pin"), ("I", "eq-content-drift"),
    ("I", "eq-metadata-drift"), ("I", "eq-absent"), ("I", "eq-unparsable-receipt-usage"),
    ("J", "readme-exit-map-covers-tool-constants"), ("J", "readme-case-count-mentions"),
    ("H", "nonvacuity-baseline-sidecar"), ("H", "sabotage-sidecar-arm-removed"),
    ("H", "sabotage-sidecar-alias-arm-removed"), ("H", "sabotage-coverage-basis-reverted"),
    ("H", "sabotage-unevaluable-arm-removed"),
}


def fmt(r):
    if r is None:
        return "—"
    st = {True: "HOLD", False: "FAIL", None: "obs"}[r.get("hold")]
    parts = []
    for k in ("exit", "cases", "verdict", "require5_exit", "clobbered", "traceback",
              "coverage_line", "label_defect", "sha_agree", "hits", "names_found",
              "prior_names_missing", "check_goes_red", "receipt_pin", "sabotage",
              "receipt_and_sidecar_written", "has_row", "counts"):
        if k in r and r[k] not in (None, "", []):
            v = r[k]
            if k == "coverage_line":
                v = v.split(";")[0]
            parts.append("%s=%s" % (k, v))
    return "%s %s" % (st, " ".join(parts))


lines = ["# EX-27 round-4 regression — before → after (measured, not asserted)", "",
         "before  = round-3 landed tool `%s` (%d lines)" % (before["tool_sha"], 1155),
         "after   = round-4 landed tool `%s` (%d lines)" % (after["tool_sha"], 1343),
         "",
         "| leg/row | before (`7cd19c3c`) | after (`29bb45ae`) |",
         "|---|---|---|"]
for k in names:
    if k not in INTEREST:
        continue
    lines.append("| %s/%s | %s | %s |" % (k[0], k[1], fmt(b.get(k)), fmt(a.get(k))))
lines += ["", "Tally: before rows=%d hold=%d fail=%d obs=%d; after rows=%d hold=%d fail=%d obs=%d" % (
    before["tally"]["rows"], before["tally"]["hold"], before["tally"]["fail"],
    before["tally"]["observed"], after["tally"]["rows"], after["tally"]["hold"],
    after["tally"]["fail"], after["tally"]["observed"]), ""]
out = BASE / "before-after-table.md"
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines[:8]))
print("...")
print(lines[-4])
print("wrote", out)
