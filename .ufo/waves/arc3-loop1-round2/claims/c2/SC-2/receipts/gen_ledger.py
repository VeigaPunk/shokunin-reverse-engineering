#!/usr/bin/env python3
"""Emit the SC-2 injection-ledger tables from the measured run JSONs."""
import json
import os

B = "/var/tmp/sc2-ledger/runs"
FAM = {f: json.load(open(os.path.join(B, f + ".json"))) for f in ("before", "landed4", "landed4-json", "cand", "landed", "landed2", "landed3", "landed3-json")}
MAIN_SHA = {"before": "6f1d19ff", "landed": "82fb807e", "landed2": "c95a5cf3",
            "landed3": "df9ffdf9", "landed3-json": "df9ffdf9",
            "landed4": "a4c16763", "landed4-json": "a4c16763", "cand": "patch-text cand"}


def row(fam, fixture):
    for r in FAM[fam]["rows"]:
        if r["fixture"] == fixture:
            return r
    raise SystemExit("missing %s in %s" % (fixture, fam))


def cell(r, mode="text"):
    v = r.get("verdict", "?")
    if r.get("crash"):
        return "**CRASH** (%s)" % r.get("crash_error", "")[:40]
    extra = ""
    if r.get("unreadable"):
        extra = " UNREADABLE×%d" % len(r["unreadable"])
    if r.get("scope_errors"):
        extra += " SCOPE-ERR×%d" % len(r["scope_errors"])
    if r.get("g2") == "SUSPECT":
        extra += " G2-SUSPECT"
    return "%s exit=%d%s" % (v, r["exit"], extra)


# (fixture, class, recipe, evidence pointer)
ROWS = [
    ("base-clean", "control", "pristine copies of the three scoped files at HEAD",
     "receipts/{f}/base-clean.out; EX-16 receipts/before|after/t0-baseline.out; VZ-2 before/t0-baseline.out"),
    ("h1-missing-skill", "H1 (closed)", "SKILL.md omitted from the root",
     "receipts/{f}/h1-missing-skill.out; EX-16 before/h1-skill-absent.out; VZ-2 before/t1-absent-skill.out; EX-11 receipts/cA-absent-skill.out"),
    ("h1-skill-as-dir", "H1 (closed)", "SKILL.md replaced by a directory (IsADirectoryError)",
     "receipts/{f}/h1-skill-as-dir.out; EX-16 before/h1-skill-isdir.out"),
    ("h1-skill-chmod000", "H1 (closed)", "SKILL.md mode 000 (PermissionError)",
     "receipts/{f}/h1-skill-chmod000.out; EX-16 before/h1-skill-eacces.out"),
    ("h1-skill-symlink-loop", "H1 (closed)", "SKILL.md self-referential symlink (ELOOP)",
     "receipts/{f}/h1-skill-symlink-loop.out; CR-2 evidence/landed__symlink_skill.txt"),
    ("ctl-missing-province", "control", "PROVINCE.md omitted",
     "receipts/{f}/ctl-missing-province.out; EX-16 before/h1-province-absent.out; VZ-2 before/t3"),
    ("ctl-missing-scorecard", "control", "SCORECARD.md omitted",
     "receipts/{f}/ctl-missing-scorecard.out; EX-16 before/h1-scorecard-absent.out; EX-11 receipts/cB2-absent-scorecard.out"),
    ("ctl-empty-dir", "control", "all three scoped files omitted",
     "receipts/{f}/ctl-empty-dir.out; VZ-2 before/t4-no-checks.out"),
    ("inj-undeclared-append", "injection", "CR-5 t2: stale pin appended past the declared bound",
     "receipts/{f}/inj-undeclared-append.out; EX-16 before/t2-undeclared-append.out"),
    ("inj-marker-strip", "injection", "CR-5 t3: DATED marker text removed (PROVINCE.md:40)",
     "receipts/{f}/inj-marker-strip.out; EX-16 before/t3-marker-strip.out"),
    ("inj-ptr-out-of-range", "injection", "CR-5 t6: pointer at ~/.kimi-code/config.toml:9999 appended",
     "receipts/{f}/inj-ptr-out-of-range.out; EX-16 before/t6-ptr-out-of-range.out"),
    ("inj-false-current-pin", "injection", "CR-5 t1: SKILL.md CURRENT pin 6.5.0 -> 6.3.0",
     "receipts/{f}/inj-false-current-pin.out; EX-16 before/t1-false-current-pin.out; EX-11 receipts/cD0"),
    ("res-missing-root", "H1 extension", "root path itself absent",
     "receipts/{f}/res-missing-root.out; CR-2 evidence/landed__live-repo.txt (control)"),
    ("res-empty-skill", "H1 extension", "SKILL.md present but 0 bytes (VZ-2 t2)",
     "receipts/{f}/res-empty-skill.out; EX-16 before/h1-skill-zero-byte.out; VZ-2 before/t2-empty-skill.out; CR-2 evidence/landed__empty_skill.txt"),
    ("res-skill-decoy-historical", "H1 extension", "SKILL.md replaced by a 1-line 'historical stub' (rows beyond EOF)",
     "receipts/{f}/res-skill-decoy-historical.out; CR-2 evidence/landed__trunc_skill.txt"),
    ("inj-dated-shelter", "by design", "CR-5 t5 / VZ-2 t8: planted pin inside a DATED range",
     "receipts/{f}/inj-dated-shelter.out; EX-16 before/t5-dated-shelter.out; VZ-2 before/t8-dated-shelter.out"),
    ("res-h2-inline-marker", "H2 residual", "VZ-2 t6: PROVINCE.md:17 pin -> 6.3.0 plus ' (historical)' on the same physical line",
     "receipts/{f}/res-h2-inline-marker.out; VZ-2 before/t6-inline-marker.out; VZ-3 (c3) A3/A3b"),
    ("res-h5-eof-no-gate-token", "H5 residual", "VZ-2 t7 / RV-11 A2: appended line with no gate token",
     "receipts/{f}/res-h5-eof-no-gate-token.out; VZ-2 before/t7-gate-free-eof.out"),
    ("blind-all-needles", "H3 (closed)", "CR-5: PIN/VER/PTR all replaced by never-matching patterns",
     "receipts/{f}/blind-all-needles.out; EX-16 before/h3-blind-all.out; VZ-2 before/t5-blind-instrument.out; EX-11 receipts/cC-neutered-needles.out"),
    ("blind-pin-only", "H3 partial residual", "PIN alone neutered (VER/PTR live)",
     "receipts/{f}/blind-pin-only.out; EX-16 before/h3-blind-pin.out"),
    ("blind-rea-gate", "H3 (closed)", "REA_GATE neutered: no unit is ever classified",
     "receipts/{f}/blind-rea-gate.out; EX-16 before/h3-blind-gate.out; CR-3 receipts/v-blind-head.out"),
    ("widened-scope", "H4 residual", "CR-5 widen: last DATED row end extended over the appended records",
     "receipts/{f}/widened-scope.out; EX-16 before/w1-scope-widen-tail.out; CR-5 receipts/widen-swallow.out"),
    ("anchor-fail-empty-home", "anchor", "HOME pointed at an empty dir: no live anchors re-derivable (CR-5 t4)",
     "receipts/{f}/anchor-fail-empty-home.out; EX-16 before/t4-anchor-fail.out"),
]

lines = ["| # | fixture (recipe) | class | BEFORE v10 6f1d19ff | AFTER landed r6 a4c16763 | AFTER r6 --json | patch-text-only cand | evidence pointers |",
         "|---|---|---|---|---|---|---|---|"]
for i, (fx, cls, recipe, ev) in enumerate(ROWS, 1):
    b, a, aj, c = row("before", fx), row("landed4", fx), row("landed4-json", fx), row("cand", fx)
    lines.append("| %d | `%s` — %s | %s | %s | %s | %s | %s | %s |" % (
        i, fx, recipe, cls, cell(b), cell(a), cell(aj), cell(c), ev))
table = "\n".join(lines)

resid = ["| fixture | landed verdict | why it is not a closure |", "|---|---|---|"]
for fx in ("inj-dated-shelter", "res-h2-inline-marker", "res-h5-eof-no-gate-token", "blind-pin-only", "widened-scope"):
    r = row("landed4", fx)
    why = {"inj-dated-shelter": "DATED rows are historical by construction (documented refusal of tail expansion)",
           "res-h2-inline-marker": "G12/INLINE_MARKER excuses a locus whose own physical line says 'historical' (H2, named in the landed header)",
           "res-h5-eof-no-gate-token": "unit has no gate token, so it is not a locus at all (H5/unit boundary; scanner-level, not fixable by a verdict guard)",
           "blind-pin-only": "one live needle family still yields current-ok loci, so the tree-level floor cannot see the loss (H4/self-certification)",
           "widened-scope": "scope widening is fail-open by construction; only the external scope-diff audit sees it (H4)",
           }[fx]
    resid.append("| `%s` | %s | %s |" % (fx, cell(r), why))
resid = "\n".join(resid)

open("/var/tmp/sc2-ledger/table.md", "w").write(table + "\n\n" + resid + "\n")
print(table)
print()
print(resid)
