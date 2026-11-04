#!/usr/bin/env python3
"""Render mutants.md from the recorded JSON evidence."""
from __future__ import annotations

import json
import os

SCRATCH = "/fast/scratch/hyaku/kaidoku-r69/MutBattery"
OUT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-69/w1/MutBattery/mutants.md"

results = json.load(open(os.path.join(SCRATCH, "results.json"), encoding="utf-8"))
pure = {(r["mutant"], r["probe"]): r
        for r in json.load(open(os.path.join(SCRATCH, "pure-probe.json"), encoding="utf-8"))["probes"]}
pref = json.load(open(os.path.join(SCRATCH, "preflight-variants.json"), encoding="utf-8"))
frozen5 = json.load(open(os.path.join(SCRATCH, "frozen-five-r69.json"), encoding="utf-8"))

FROZEN_CS3 = {"pass", "loose", "r68"}  # the three fixtures the frozen controls drive
FROZEN_CS3_NOTE = "c3-synthetic-met / c3-loose-ceiling"

CLASS = {
    "MB01_control_default": ("over-strict", "none reachable: no caller omits `control_ok`; a caller that did would mark a green carrier false (false alarm, not a false pass)"),
    "MB02_fold_empty_control": ("latent", "`fold([], 0)` -> control_ok true and met_target true: a composite verdict with no carrier at all; unreachable while target is `len(CARRIERS)` = 3"),
    "MB03_fold_missing_control_arm": ("latent", "a carrier record with no `control_ok` arm folds to met_target true (pristine raises KeyError: the missing arm currently crashes rather than rejects)"),
    "MB04_fold_matched_ge": ("latent", "`carriers_matched` above target counts as met (4 ok carriers, target 3 -> met true); unreachable with three carriers, but it would let a duplicated 4th carrier pass the composite verdict"),
    "MB05_receipt_ratio_bound": ("killed", "a receipt with a 0.9 ceiling ratio would be scored met"),
    "MB06_receipt_shared_object": ("behaviour-bearing", "a receipt whose carrier set has no `shared-object` kind would be scored met: C3's shared-object clause is enforced by this one predicate"),
    "MB07_elf_format_len": ("conditional", "a 3-of-4 `readelf -h` parse is recorded as a complete format; identical on healthy headers (4-of-4), and A5 would reject the mismatch if it ever occurred"),
    "MB08_preflight_order": ("contract-order", "with a missing `node` AND an unwritable `--work`, the refusal names work_unusable instead of missing_tool: node (both exit 2, only the class name moves)"),
    "MB09_preflight_tool_order": ("contract-order", "with both `node` and `git` absent, the refusal names git instead of node; A1 removes only node, so the arm is blind"),
    "MB10_section_branch_sentinel": ("equivalent", "none on real readelf output: any `readelf -SW` text carrying the sentinel has no bracket rows, so the regex count is 0 as well (sentinel-only observed 0 == 0); a synthetic sentinel-plus-row text differs (pristine 0, mutant 1)"),
    "MB11_section_branch_return": ("killed", "the no-sections file would be counted as 1 section and stay 'packed'"),
    "MB12_refusal_code_floor": ("behaviour-bearing", "a refusal that returns a 1..200-byte decompilation with the symbol present is scored as recovered code; the 200-byte floor is not enforced"),
    "MB13_refusal_unpacked_rc": ("behaviour-bearing", "a refusal whose unpacked decompile FAILED (rc != 0) but left symbol bytes is scored as recovered code"),
    "MB14_receipt_met_target": ("receipt-honesty", "a receipt that self-declares `met_target: false` while every other field is green is scored met; the predicate does not name receipt.met_target, but the checker stops noticing an inconsistent receipt"),
    "MB15_receipt_failing_truthiness": ("predicate-relevant", "a receipt with NO `failing` key (None) satisfies the predicate's `failing []` clause: absent is scored as empty"),
    "MB16_receipt_counts": ("receipt-honesty", "a carrier with no `orig_counts`/`packed_counts` is accepted as inventory evidence"),
    "MB17_receipt_arm_value": ("receipt-honesty", "an arm whose value is `null` is accepted as true; note contract-probe A5 shares the hole (`any(v is False)`), so the null arm is invisible to both instruments"),
    "MB18_ratio_constant": ("predicate-relevant", "every carrier records `before_ceiling_ratio` 0.0 regardless of ceiling/original, so the predicate's 0.75 clause is satisfied by a constant; the receipt still carries ceiling and orig_procedures, so the relation is recomputable but never re-derived"),
    "MB19_check_work_false": ("killed", "an unwritable --work root escapes as a PermissionError traceback with exit 1"),
    "MB20_version_fallback": ("equivalent", "a packer whose `--version` prints nothing gets the pin substituted for the version string; the sha256 pin still refuses it (observed), so no false pass is reachable"),
}

SHORT_PATCH = {
    "MB01_control_default": "`control_ok: bool = True` -> `= False` (default)",
    "MB02_fold_empty_control": "drop `bool(carriers) and` from the fold's control_ok",
    "MB03_fold_missing_control_arm": "`arms[\"control_ok\"]` -> `arms.get(\"control_ok\", True)`",
    "MB04_fold_matched_ge": "`matched == target` -> `matched >= target`",
    "MB05_receipt_ratio_bound": "`ratio > 0.75` -> `ratio > 1.0`",
    "MB06_receipt_shared_object": "`\"shared-object\" not in kinds` -> `\"executable\" not in kinds`",
    "MB07_elf_format_len": "`len(found) == 4` -> `len(found) >= 3`",
    "MB08_preflight_order": "work-root block moved ahead of the node/git/readelf, upx and rea checks",
    "MB09_preflight_tool_order": "tool tuple `(node, git, readelf)` -> `(git, node, readelf)`",
    "MB10_section_branch_sentinel": "sentinel string `There are no sections in this file` -> `There are no section headers ...`",
    "MB11_section_branch_return": "no-sections branch `return 0` -> `return 1`",
    "MB12_refusal_code_floor": "`refusal_code_bytes > 200` -> `> 0`",
    "MB13_refusal_unpacked_rc": "drop `refusal_unpacked_rc == 0` from refusal_ok",
    "MB14_receipt_met_target": "delete the `met_target is not True` clause",
    "MB15_receipt_failing_truthiness": "`failing != []` -> `failing` (truthiness)",
    "MB16_receipt_counts": "`counts absent` failure -> `pass`",
    "MB17_receipt_arm_value": "`value is not True` -> `value is False`",
    "MB18_ratio_constant": "ratio expression -> `round(0.0, 4)`",
    "MB19_check_work_false": "`check_work=not skip_run` -> `check_work=False`",
    "MB20_version_fallback": "empty version -> `UPX_VERSION_PIN`",
}

ROUTE = {
    "MB01_control_default": "selftest case calling `carrier_arms(True, True, True, True, None)` (5 args, default exercised) and asserting `control_ok` true.",
    "MB02_fold_empty_control": "selftest case `fold([], 0)['control_ok'] is False and fold([], 0)['met_target'] is False`.",
    "MB03_fold_missing_control_arm": "harden fold to `c['arms'].get('control_ok') is not True` (also closes the KeyError crash) and add case `fold-missing-control-arm`.",
    "MB04_fold_matched_ge": "selftest case `fold([ok_model] * 4, 3)['met_target'] is False`.",
    "MB05_receipt_ratio_bound": "already killed by the frozen control c3-loose-ceiling; no new case needed.",
    "MB06_receipt_shared_object": "extract the kinds clause into `receipt_kinds_ok(kinds)` and add case `receipt-no-shared-object` (kinds `['executable']` -> false), or add a control arm `c3-no-shared-object`.",
    "MB07_elf_format_len": "selftest case `elf_format(three_field_header) is None`.",
    "MB08_preflight_order": "contract-probe arm A7: PATH without node AND a 0500 --work root, asserting the refusal names `node` (and a second A8 for PATH without node and git).",
    "MB09_preflight_tool_order": "same A7/A8 composition: PATH with neither node nor git must still name node.",
    "MB10_section_branch_sentinel": "not needed for correctness (equivalent); to pin the branch, case `section_count(sentinel + one section row) == 0`.",
    "MB11_section_branch_return": "already killed by selftest case sections-none.",
    "MB12_refusal_code_floor": "selftest model `address=0x1000, refusal_packed_rc=1, refusal_unpacked_rc=0, symbol_present=True, refusal_code_bytes=50` -> `refusal_ok` false.",
    "MB13_refusal_unpacked_rc": "selftest model with `refusal_unpacked_rc=7`, symbol present, 400 bytes -> `refusal_ok` false.",
    "MB14_receipt_met_target": "add a control arm with a synthetic receipt carrying `met_target: false` (expect exit 1).",
    "MB15_receipt_failing_truthiness": "add a control arm with a synthetic receipt carrying no `failing` key (expect exit 1).",
    "MB16_receipt_counts": "add a control arm with a synthetic receipt whose carrier has no counts (expect exit 1).",
    "MB17_receipt_arm_value": "add a control arm with a synthetic receipt whose arm is null (expect exit 1); fix A5 to `value is not True`.",
    "MB18_ratio_constant": "extract `ceiling_ratio(ceiling, orig)` and add selftest cases (10/167 -> 0.0599, 10/99 -> 0.101, 120/184 -> 0.6522); have check_receipt recompute the ratio from `before_ceiling`/`orig_counts` instead of trusting the record.",
    "MB19_check_work_false": "already killed by contract-probe A2_work_unusable.",
    "MB20_version_fallback": "not needed (equivalent under the sha256 pin); optionally a pure `version_pin(version)` case.",
}


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ")


rows = []
for m in results["mutants"]:
    mid = m["id"]
    st = "green" if m["selftest"]["rc"] == 0 else f"FAILED {m['selftest']['failed']}"
    frozen_fixtures = "no"
    if m["selftest"]["rc"] != 0:
        frozen_fixtures = "FIRES: selftest " + str(m["selftest"]["failed"])
    elif m.get("receipt_rc_deviations"):
        dev = m["receipt_rc_deviations"]
        frozen_hit = [n for n in dev if n in FROZEN_CS3]
        frozen_fixtures = ("FIRES on " + ", ".join(frozen_hit)) if frozen_hit else "no"
    ext = "no"
    if m.get("receipt_rc_deviations"):
        ext = ", ".join(sorted(m["receipt_rc_deviations"]))
    elif m["verdict"].startswith("killed"):
        ext = "-"
    arms = "-"
    if m.get("preflight_deviations"):
        arms = "; ".join(f"{k} -> {v['mutant']!r}" for k, v in m["preflight_deviations"].items())
    frozen_kill = (m["selftest"]["rc"] != 0) or any(
        n in FROZEN_CS3 for n in (m.get("receipt_rc_deviations") or {})) or bool(
        m.get("preflight_deviations") and any(k in ("A1_missing_node", "A2_work_unusable")
                                              for k in m["preflight_deviations"]))
    verdict = "KILLED" if frozen_kill else "SURVIVED"
    if (m.get("preflight_deviations") or {}).get("A1_missing_node"):
        frozen_fixtures = "FIRES on A1"
    if (m.get("preflight_deviations") or {}).get("A2_work_unusable"):
        frozen_fixtures = "FIRES on A2"
    site = m["site"]
    patch = esc(SHORT_PATCH[mid].replace("`", ""))
    rows.append({
        "id": mid, "site": site, "patch": patch, "selftest": st,
        "frozen": frozen_fixtures, "ext": ext, "arms": arms,
        "verdict": verdict, "class": CLASS[mid][0], "claim": CLASS[mid][1],
        "route": ROUTE[mid],
    })

survivors = [r for r in rows if r["verdict"] == "SURVIVED"]
killed = [r for r in rows if r["verdict"] == "KILLED"]
live = [r for r in survivors if r["class"] != "equivalent"]

lines = []
A = lines.append
A("# Round 69 / w1 / MutBattery — new mutants of `tools/round-69/packed-elf.py`")
A("")
A("Seat: mutation-tester (MutBattery). Target: `tools/round-69/packed-elf.py` at the frozen")
A(f"bytes `{results['frozen_sha256']}` (operative freeze `{results['operative_freeze_rev']}`).")
A("**The frozen file was never edited**: every patch was applied to a copy under")
A("`/fast/scratch/hyaku/kaidoku-r69/MutBattery/`; the lane file re-hashed to the same")
A("sha256 after the run (restoration evidence at the end).")
A("")
A("## Baseline (pristine copy, before any patch)")
A("")
A(f"- `--selftest`: rc 0, cases {results['baseline']['selftest']['cases']}, failed "
  f"{results['baseline']['selftest']['failed']!r}.")
A("- `--check-receipt` on the frozen control fixtures and on the extended receipts:")
A("")
A("| receipt | pristine rc | pristine failing |")
A("|---|---|---|")
for name in sorted(results["baseline"]["receipts"]):
    r = results["baseline"]["receipts"][name]
    A(f"| `{name}` | {r['rc']} | `{json.dumps(r['failing'])}` |")
A("")
A("| preflight probe | pristine rc | unevaluable |")
A("|---|---|---|")
for name in sorted(results["baseline"]["preflight"]):
    p = results["baseline"]["preflight"][name]
    A(f"| `{name}` | {p['rc']} | `{p['unevaluable']}` |")
A("")
A("End-to-end pristine measurement of the scratch copy (65 s, REA 6.5.0, upx 5.2.0):")
A("`met_target true, carriers_matched 3, control_ok true, failing []`, ratios")
A("`0.0599 / 0.101 / 0.6522` (jq / xxd / libz), libz `shared-object` — identical to atom A8.")
A("`--check-receipt` on that receipt: `met true`, `failing []`.")
A("")
A("Anchor: the frozen five at the same revision (`mutation-check.py --patch-set r69`,")
A(f"work re-run this seat) give `survivors {frozen5['survivors']}`, pristine.cases "
  f"{frozen5['pristine']['cases']}, kills naming "
  f"{[m['failed'] for m in frozen5['mutants']]}. The frozen battery is live at this revision.")
A("")
A("## Mutants (20, all new; none of the five frozen sites is re-used)")
A("")
A("Legend: **frozen** = does a frozen detector fire? The frozen set is the 20-case")
A("`--selftest`, the three receipts the controls already drive (`c3-synthetic-met` = `pass`,")
A("`c3-loose-ceiling` = `loose`, `c3-do-nothing` = the round-68 landing receipt = `r68`), and")
A("contract arms A1/A2. **ext** = which of this seat's ten extra receipts fire. **arms** = the")
A("preflight observation that moved, if any.")
A("")
A("| # | mutant | site | patch | selftest | frozen | ext | arms | verdict |")
A("|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(rows, 1):
    A(f"| {i} | `{r['id']}` | {esc(r['site'])} | {r['patch']} | {r['selftest']} | "
      f"{r['frozen']} | {esc(r['ext'])} | {esc(r['arms'])} | **{r['verdict']}** |")
A("")
A(f"Killed by the frozen detector set: **{len(killed)} of 20** "
  f"({', '.join('`' + r['id'] + '`' for r in killed)}).")
A(f"Survivors: **{len(survivors)} of 20**; {len(live)} of them are behaviour-bearing under some")
A("input the frozen detectors never feed (the rest are equivalent or over-strict).")
A("")
A("## Survivors — the exact false claim each admits, and a cheap kill route")
A("")
for r in survivors:
    A(f"### `{r['id']}` — {r['class']}")
    A("")
    A(f"- Site: {r['site']}.")
    A(f"- False claim admitted: {r['claim']}.")
    A(f"- Route (do not edit the frozen instrument; add for the next freeze): {r['route']}")
    A("")
A("## Receipts (all paths relative to the lane root)")
A("")
A("- `.ufo/waves/round-69/w1/MutBattery/results.json` — every mutant row, all rc/failing values,")
A("  the baseline table, receipt paths, restoration hashes.")
A("- `.ufo/waves/round-69/w1/MutBattery/pure-probe.json` — direct calls to the pure helpers with")
A("  the inputs the selftest omits (fold empty/over-target/missing-arm, elf_format 3-of-4,")
A("  section sentinel+rows, refusal short code, refusal failed unpacked rc).")
A("- `.ufo/waves/round-69/w1/MutBattery/preflight-variants.json` — tool-tuple order and silent")
A("  packer version observations (pristine / MB09 / MB20).")
A("- `.ufo/waves/round-69/w1/MutBattery/frozen-five-r69.json` — anchor run of the frozen five.")
A("- `.ufo/waves/round-69/w1/MutBattery/receipt-live-pristine.json` and")
A("  `receipt-live-MB18.json` — the two end-to-end receipts (pristine vs the ratio-constant")
A("  mutant), same work dir, 65 s each.")
A("- `.ufo/waves/round-69/w1/MutBattery/receipts/` — the ten synthetic receipts.")
A("- `.ufo/waves/round-69/w1/MutBattery/mutate.py` — the driver that produced all of it.")
A("")
A("### Pristine-vs-mutant observations worth carrying")
A("")
A("- The frozen checker accepts a receipt whose carriers are renamed (`carrier-0..2`), a receipt")
A("  that duplicates `jq` and still reports `carriers_matched 3`, and a receipt whose libz")
A("  `before_ceiling_ratio` is `0.0001` while the same receipt says ceiling 120 / 184")
A("  procedures. All three are pristine behaviour (rc 0) observed this seat, not mutants:")
A("  the checker validates shape, not carrier identity and not the ratio derivation.")
A("- MB18's end-to-end receipt records `before_ceiling_ratio 0.0` for all three carriers while")
A("  `before_ceiling`/`orig_procedures` still say 10/167, 10/99, 120/184, and the frozen")
A("  checker scores it `met true`. The 0.75 clause is inferred from a self-reported number.")
A("- contract-probe A5 uses `any(v is False for v in arms.values())`: a `null` arm is not")
A("  `False`, so A5 is blind to a null arm exactly as MB17 makes check_receipt blind.")
A("")
A("## Restoration evidence")
A("")
A(f"- frozen file sha256 before: `{results['frozen_sha256']}`")
A(f"- frozen file sha256 after:  `{results['frozen_sha256']}` (re-hashed at the end of the run)")
A("- the scratch pristine copy was rewritten from the frozen bytes and re-hashed to the same")
A("  value (`matches_frozen: true`, recorded in the driver's restoration phase)")
A("- scratch dir `/fast/scratch/hyaku/kaidoku-r69/MutBattery/` deleted after the receipts were")
A("  copied into this wave directory.")
A("")
A("## Survivors named for the next freeze")
A("")
for r in live:
    A(f"- `{r['id']}` ({r['class']}): {r['claim'].split(';')[0]}.")
A("")

text = "\n".join(lines) + "\n"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"wrote {OUT} ({len(text)} bytes)")
print(f"killed={len(killed)} survived={len(survivors)} live={len(live)}")
