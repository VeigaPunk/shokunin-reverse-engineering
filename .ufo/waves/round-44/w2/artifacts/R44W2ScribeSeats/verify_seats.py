#!/usr/bin/env python3
"""R44W2ScribeSeats — verify round-44 wave shape from the wave files themselves.

Read-only over the lane. Emits one JSON object on stdout; every number in the
annex is re-derived here from the file, never copied from the prompt.
"""
import json, os, sys, hashlib, datetime

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
W = os.path.join(LANE, ".ufo/waves/round-44")
FLEET = "/home/vgpnk/Projects/shokunin"


def jload(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def tally(items, key):
    c = {}
    for i in items:
        c[i[key]] = c.get(i[key], 0) + 1
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


def dispatched_map(path):
    lines = open(path, "r", encoding="utf-8").read().splitlines()
    ts = lines[0].strip() if lines else None
    m = json.loads(lines[1]) if len(lines) > 1 else {}
    return {"timestamp_line": ts, "mappings": m, "count": len(m),
            "suffixed": {k: v for k, v in m.items() if k != v}}


def wave(path_prefix, spec_name, dispatch_name, results_name, registry_name,
         report_subdir, result_keys):
    spec = jload(os.path.join(W, spec_name))
    names = [i["name"] for i in spec["items"]]
    out = {
        "spec": {
            "path": os.path.join(W, spec_name),
            "wave": spec["wave"],
            "milestone": spec.get("milestone"),
            "reportDir": spec.get("reportDir"),
            "count": len(spec["items"]),
            "roles": tally(spec["items"], "role"),
            "duplicate_names": sorted({n for n in names if names.count(n) > 1}),
            "planner_seats": [i["name"] for i in spec["items"] if i["role"] == "planner"],
            "role_check": sum(tally(spec["items"], "role").values()) == len(spec["items"]),
        },
    }
    disp = jload(os.path.join(W, dispatch_name))
    tasks = disp["taskCall"]["tasks"]
    short = {t["name"]: t["agent"] for t in tasks}
    out["dispatch"] = {
        "path": os.path.join(W, dispatch_name),
        "counts": disp["counts"],
        "policy": disp["policy"],
        "taskcall_tasks": len(tasks),
        "names_equal_spec": set(short) == set(names),
        "task_roles_equal_spec_roles": short == {i["name"]: i["role"] for i in spec["items"]},
        "task_role_tally": tally([{"role": r} for r in short.values()], "role"),
        "no_planner_in_dispatch": "planner" not in short.values(),
    }
    reg = jload(os.path.join(W, registry_name))["members"]
    out["registry"] = {
        "path": os.path.join(W, registry_name),
        "members": len(reg),
        "roles": tally([{"role": v["role"]} for v in reg.values()], "role"),
        "role_mismatches_vs_spec": [
            [n, reg[n]["role"], next(i["role"] for i in spec["items"] if i["name"] == n)]
            for n in reg if reg[n]["role"] != next(i["role"] for i in spec["items"] if i["name"] == n)
        ],
        "name_set_equal_spec": set(reg) == set(names),
    }
    out["dispatched"] = dict(dispatched_map(os.path.join(W, path_prefix)),
                             path=os.path.join(W, path_prefix))
    out["dispatched"]["covers_spec"] = set(out["dispatched"]["mappings"]) == set(names)

    rpath = os.path.join(W, results_name)
    if os.path.exists(rpath):
        res = jload(rpath)
        rows = res["results"]
        agents = tally([{"role": r.get("agent")} for r in rows], "role")
        md_dir = os.path.join(W, report_subdir)
        mds = sorted(f for f in os.listdir(md_dir) if f.endswith(".md"))
        specnames = set(names)
        report = {
            "path": rpath,
            "seats_field": res.get("seats"),
            "result_count": len(rows),
            "agents": agents,
            "name_set_equal_spec": set(r["name"] for r in rows) == specnames,
            "agent_roles_equal_spec_roles": {r["name"]: r.get("agent") for r in rows}
                                            == {i["name"]: i["role"] for i in spec["items"]},
            "nonempty_notes": [r["name"] for r in rows if (r.get("note") or "").strip()],
            "error_outputs": [],
            "reports_present": 0,
            "reports_missing": [],
            "reports_empty": [],
            "reports_total_bytes": 0,
            "md_files_not_a_seat": sorted(m[:-3] for m in mds if m[:-3] not in specnames),
        }
        for r in rows:
            o = r.get("output") or ""
            try:
                d = json.loads(o)
            except Exception:
                report["error_outputs"].append([r["name"], "unparsable_output"])
            else:
                if d.get("error"):
                    report["error_outputs"].append([r["name"], str(d["error"])[:120]])
            p = os.path.join(md_dir, r["name"] + ".md")
            if not os.path.exists(p):
                report["reports_missing"].append(r["name"])
            else:
                sz = os.path.getsize(p)
                report["reports_present"] += 1
                report["reports_total_bytes"] += sz
                if sz == 0:
                    report["reports_empty"].append(r["name"])
        out["results"] = report
    else:
        out["results"] = {"path": rpath, "exists": False,
                          "note": "wave in flight at capture time; no results file"}
    return out


def share(roles, n, attack_set):
    k = sum(roles.get(r, 0) for r in attack_set)
    return {"count": k, "of": n, "pct": round(100.0 * k / n, 1)}


def main():
    out = {"seat": "R44W2ScribeSeats", "round": 44,
           "as_of_utc": datetime.datetime.now(datetime.timezone.utc)
           .strftime("%Y-%m-%dT%H:%M:%SZ"),
           "lane": LANE}
    w1 = wave("w1.ready.dispatched", "w1-spec.json", "w1-dispatch.json",
              "r44-w1-results.json", "w1/swarm-registry.json", "w1", None)
    w2 = wave("w2.ready.dispatched", "w2-spec.json", "w2-dispatch.json",
              "r44-w2-results.json", "w2/swarm-registry.json", "w2", None)
    out["w1"], out["w2"] = w1, w2

    n1, n2 = w1["spec"]["count"], w2["spec"]["count"]
    r1, r2 = w1["spec"]["roles"], w2["spec"]["roles"]
    NARROW = ["reviewer", "critic", "mutation-tester", "labrat"]
    WIDE = NARROW + ["sentinel", "revenger", "connector"]
    out["attack_share"] = {
        "narrow_role_set": NARROW,
        "narrow_source": "scripts/hyaku/lane-addendum.md:203 (v2 wave: reviewer, critic, mutation-tester, labrat)",
        "wide_role_set": WIDE,
        "wide_source": "R44Watchdog.md (w1) / addendum §2 wording connector+revenger+sentinel counted as attack",
        "w1_narrow": share(r1, n1, NARROW),
        "w2_narrow": share(r2, n2, NARROW),
        "round_narrow": share({k: r1.get(k, 0) + r2.get(k, 0) for k in set(r1) | set(r2)},
                              n1 + n2, NARROW),
        "w1_wide": share(r1, n1, WIDE),
        "w2_wide": share(r2, n2, WIDE),
        "round_wide": share({k: r1.get(k, 0) + r2.get(k, 0) for k in set(r1) | set(r2)},
                            n1 + n2, WIDE),
    }

    out["bands"] = {
        "v1_policy": jload(os.path.join(FLEET, "scripts/hyaku/ufo-wave-policy.json"))
        ["sighting"]["dispatch"]["swarm"],
        "v2_policy": jload(os.path.join(FLEET, "scripts/hyaku/ufo-wave-policy-v2.json"))
        ["sighting"]["dispatch"]["swarm"],
        "w1_in_v1_band": 32 <= n1 <= 64,
        "w2_in_v1_band": 32 <= n2 <= 64,
        "round_total": n1 + n2,
        "round_total_within_32_128": 32 <= n1 + n2 <= 128,
        "both_waves_one_taskcall": len(jload(os.path.join(W, "w1-dispatch.json"))
                                       ["taskCall"]["tasks"]) == n1
        and len(jload(os.path.join(W, "w2-dispatch.json"))["taskCall"]["tasks"]) == n2,
    }

    resid = [f for f in os.listdir(W) if "resid" in f.lower() or f.startswith("w3")]
    out["residual"] = {"round_dir_markers": sorted(resid),
                       "expected": "none (round total 79 <= 128 cap)",
                       "present": bool(resid)}

    add = os.path.join(FLEET, "scripts/hyaku/lane-addendum.md")
    lines = open(add, encoding="utf-8").read().splitlines()
    out["citations"] = {
        "lane-addendum.md:190": lines[189],
        "lane-addendum.md:193": lines[192],
        "lane-addendum.md:201": lines[200],
        "lane-addendum.md:203": lines[202],
        "lane-addendum.md:5": lines[4],
    }
    print(json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
