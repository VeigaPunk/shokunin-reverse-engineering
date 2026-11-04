#!/usr/bin/env python3
"""Turn raw-results.json into mutation.json + mutation.md (verdict rules below)."""
import json, os, sys

D = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(D, "raw-results.json")))
res, st, meta = raw["results"], raw["selftests"], raw["meta"]


def key(s):
    s = dict(s); s.pop("label", None) if False else None
    return json.dumps(s, sort_keys=True)


def nonrea_ok(s):
    return (s.get("exit") in (0, 1) and s.get("nonrea_recovered") == 8
            and all(s.get("controls_ok", {}).values()))


base = {r: res[f"B-{r}"]["summary"] for r in ("repair", "identity", "naive")}
baseline_ok = nonrea_ok(base["repair"]) and st["R00"]["rc"] == 0 and st["C00"]["rc"] == 0
rows = []
for mid, m in sorted(meta.items()):
    if m["kind"] == "repair":
        s = res[mid]["summary"]
        st_fail = st[mid]["rc"] != 0
        ctr_fail = not nonrea_ok(s)
        verdict = "inconclusive" if not baseline_ok else ("killed" if st_fail or ctr_fail else "survived")
        rows.append({"mutant": mid, "kind": "repair", "desc": m["desc"], "anchor_old": m["old"], "anchor_new": m["new"],
                     "mutant_sha256": m["sha256"], "selftest_rc": st[mid]["rc"],
                     "selftest_out": st[mid]["out"].splitlines()[-1] if st[mid]["out"] else "",
                     "counter_nonrea_recovered": s.get("nonrea_recovered"), "counter_controls_ok": s.get("controls_ok"),
                     "counter_exit": s.get("exit"), "killed_by": [x for x, f in (("selftest", st_fail), ("counter", ctr_fail)) if f],
                     "verdict": verdict})
    else:
        diffs = {}
        for r in ("repair", "identity", "naive"):
            s = res[f"{mid}-{r}"]["summary"]
            if key(s) != key(base[r]):
                diffs[r] = {k: (base[r].get(k), s.get(k)) for k in set(s) | set(base[r]) if s.get(k) != base[r].get(k)}
        st_fail = st[mid]["rc"] != 0
        ident = res[f"{mid}-identity"]["summary"]
        rows.append({"mutant": mid, "kind": "counter", "desc": m["desc"], "anchor_old": m["old"], "anchor_new": m["new"],
                     "mutant_sha256": m["sha256"], "selftest_rc": st[mid]["rc"],
                     "selftest_out": st[mid]["out"].splitlines()[-1] if st[mid]["out"] else "",
                     "summaries": {r: res[f"{mid}-{r}"]["summary"] for r in ("repair", "identity", "naive")},
                     "reference_diffs": diffs,
                     "identity_green": bool(ident.get("met")),
                     "killed_by": (["selftest"] if st_fail else []) + [f"ref-{r}" for r in diffs],
                     "verdict": "inconclusive" if not baseline_ok else ("killed" if st_fail or diffs else "survived")})

out = {"seat": "MutationR87", "round": 87, "claim": "R87-C1",
       "repair": {"path": "tools/round-87/upx-magic-repair.py", "commit": "b5c7a49e20647bb73117ed1ffb4f68dd69916cd8",
                  "sha256": raw["before"]["tools/round-87/upx-magic-repair.py"]},
       "counter": {"path": "tools/round-87/upx-tamper-battery.py", "sha256": raw["before"]["tools/round-87/upx-tamper-battery.py"]},
       "verdict_rules": {
           "repair": "killed iff mutant --selftest rc!=0, or frozen counter --no-rea with --repair-cmd <mutant> has any of the 8 cases failing a non-REA arm (repair_rc0, windows_only, test_ok, identity) or any control false, or exit 2",
           "counter": "killed iff mutant counter --selftest rc!=0, or any reference run (committed repair --no-rea; identity with REA on; naive-global --no-rea) yields a summary (exit, met, recovered, non-REA recovered, controls_ok, per-case false arms, repaired==packed count) different from the pristine counter's"},
       "baselines": base, "baseline_ok": baseline_ok,
       "selftest_pristine": {"repair": st["R00"]["out"], "counter": st["C00"]["out"]},
       "restoration": {"production_before": raw["before"], "production_after": raw["after"],
                       "pristine_scratch_copies_after": raw["pristine_copies_after"],
                       "identical": raw["before"] == raw["after"]},
       "rows": rows,
       "survivors": [r["mutant"] for r in rows if r["verdict"] == "survived"],
       "identity_turned_green": [r["mutant"] for r in rows if r.get("identity_green")],
       "counts": {k: {v: sum(1 for r in rows if r["kind"] == k and r["verdict"] == v) for v in ("killed", "survived", "inconclusive")}
                  for k in ("repair", "counter")}}
json.dump(out, open(os.path.join(D, "mutation.json"), "w"), indent=1, sort_keys=True)

L = ["# MutationR87 - R87-C1 mutation table", "",
     f"Pristine baselines: repair selftest `{st['R00']['out']}`, counter selftest `{st['C00']['out']}`; "
     f"committed repair --no-rea non-REA {base['repair']['nonrea_recovered']}/8 controls {base['repair']['controls_ok']}; "
     f"identity (REA on) `{base['identity']['label']}` met={base['identity']['met']}; naive-global --no-rea non-REA {base['naive']['nonrea_recovered']}/8.", "",
     "## Repair mutants (frozen counter, `--no-rea`)", "",
     "| mutant | anchor (old -> new) | selftest | counter non-REA / controls | verdict |", "|---|---|---|---|---|"]
for r in rows:
    if r["kind"] != "repair":
        continue
    bad = [k for k, v in (r["counter_controls_ok"] or {}).items() if not v]
    L.append(f"| {r['mutant']} {r['desc']} | `{r['anchor_old']}` -> `{r['anchor_new'] or '(deleted)'}` | rc {r['selftest_rc']} | "
             f"{r['counter_nonrea_recovered']}/8, {'controls ok' if not bad else 'fail ' + ','.join(bad)} | **{r['verdict']}** {'+'.join(r['killed_by'])} |")
L += ["", "## Counter mutants (committed repair / identity / naive-global)", "",
      "| mutant | anchor (old -> new) | selftest | repair | identity | naive-global | identity green? | verdict |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["kind"] != "counter":
        continue
    cell = lambda s: f"{s.get('nonrea_recovered')}/8 nonREA, rec {s.get('recovered')}, met {s.get('met')}, ctl-fail {[k for k, v in s.get('controls_ok', {}).items() if not v]}"
    sm = r["summaries"]
    L.append(f"| {r['mutant']} {r['desc']} | `{r['anchor_old'][:60]}` -> `{r['anchor_new'][:60]}` | rc {r['selftest_rc']} | "
             f"{cell(sm['repair'])} | {cell(sm['identity'])} | {cell(sm['naive'])} | {r['identity_green']} | **{r['verdict']}** {'+'.join(r['killed_by'])} |")
L += ["", f"Survivors: {', '.join(out['survivors'])}", f"Identity (do-nothing) turned green by: {out['identity_turned_green'] or 'none'}",
      f"Counts: {out['counts']}", f"Restoration: production sha256 before == after: {out['restoration']['identical']}"]
open(os.path.join(D, "mutation.md"), "w").write("\n".join(L) + "\n")
print(json.dumps({"survivors": out["survivors"], "green": out["identity_turned_green"], "counts": out["counts"],
                  "baseline_ok": baseline_ok}, indent=0))
