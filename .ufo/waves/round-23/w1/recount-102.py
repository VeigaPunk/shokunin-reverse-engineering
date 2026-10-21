#!/usr/bin/env python3
"""Independent recount of R22 reportless seats (author-side, read-only).

Reads R22 wave artifacts and inherited seat transcripts; writes recount-102.json.
No production files are modified. Exit 0 only when the recount reproduces:
  W1 93/93 reportless, W2 9/64 reportless, total 102.
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R22 = os.path.join(ROOT, ".ufo/waves/round-22")
SESS = ("/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/"
        "2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22")
OUT = os.path.join(ROOT, ".ufo/waves/round-23/w1/recount-102.json")

W2_MISSING = [
    "RecoverReceipts", "RecoverFlutter", "CounterSelfInvocation", "SourceGateDraft",
    "SchemaInspectSignalDecoders", "PrimaryDart", "C1Split", "C1Partial", "CriticLowest",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load(name):
    with open(os.path.join(R22, name), encoding="utf-8") as fh:
        return json.load(fh)


def transcript(path):
    """Return (errorMessages, session_exit tuples) from a seat jsonl."""
    errs, exits = [], []
    for line in open(path, encoding="utf-8", errors="replace"):
        if '"errorMessage"' in line:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            carriers = [obj.get("message"), obj.get("data"), obj]
            msg = next((c["errorMessage"] for c in carriers
                        if isinstance(c, dict) and c.get("errorMessage")), None)
            if msg:
                errs.append((obj.get("timestamp"), msg))
        if '"session_exit"' in line:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            d = obj.get("data", {})
            exits.append((d.get("recordedAt"), d.get("reason"), d.get("kind")))
    return errs, exits


def classify(msg):
    if "turn_rate_limit_exceeded" in msg or "Codex is at capacity" in msg:
        return "codex_capacity_retry_exhausted"
    if "RESOURCE_EXHAUSTED" in msg or "resource_exhausted" in msg:
        return "provider_resource_exhausted"
    if re.search(r"rate limit|429", msg, re.I):
        return "429_rate_limit"
    if "aborted" in msg.lower():
        return "request_aborted"
    return "other"


def main():
    w1_spec = load("wave1-spec.json")
    w2_spec = load("wave2-spec.json")
    w1_reg = load("w1/swarm-registry.json")
    final = load("final-wave-outcomes.json")
    correction = load("wave1-terminal-correction.json")
    w2_initial = load("wave2-terminal-initial.json")
    w1_terminal = load("wave1-terminal.json")
    recovery = load("recovery-authority.json")

    w1_names = [i["name"] for i in w1_spec["items"]]
    w2_names = [i["name"] for i in w2_spec["items"]]
    w1_ids = {m["agentId"] for m in w1_reg["members"].values()}
    dispatch_ids = set(re.findall(
        r"KaidokuR22\.[A-Za-z0-9._-]+",
        open(os.path.join(R22, "wave1-dispatch-result.txt"), encoding="utf-8",
             errors="replace").read()))
    w2_ack_ids = set(re.findall(
        r"KaidokuR22R\.[A-Za-z0-9._-]+",
        json.dumps(load("wave2-spawn-try6.json"))))
    final_w1 = {m["id"] for m in final["wave1"]["members"]}
    final_w2 = {m["id"] for m in final["wave2"]["members"]}

    w1_expected = [f".ufo/waves/round-22/w1/{n}.md" for n in w1_names]
    w2_expected = [f".ufo/waves/round-22/w2/{n}.md" for n in w2_names]
    w1_present = [p for p in w1_expected if os.path.isfile(os.path.join(ROOT, p))]
    w2_present = [p for p in w2_expected if os.path.isfile(os.path.join(ROOT, p))]

    w1_out = [f for f in os.listdir(os.path.join(SESS, "KaidokuR22")) if f.endswith(".md")]
    w1_out_nonzero = [f for f in w1_out
                      if os.path.getsize(os.path.join(SESS, "KaidokuR22", f))]
    w2_out = [f for f in os.listdir(os.path.join(SESS, "KaidokuR22R")) if f.endswith(".md")]
    w2_out_zero = [f for f in w2_out
                   if os.path.getsize(os.path.join(SESS, "KaidokuR22R", f)) == 0]

    w1_jsonl = sorted(f for f in os.listdir(os.path.join(SESS, "KaidokuR22"))
                      if f.endswith(".jsonl"))
    w1_roles = {i["name"]: i["role"] for i in w1_spec["items"]}
    w1_error_class_by_role = {}
    w1_exits = []
    for f in w1_jsonl:
        name = f[len("KaidokuR22."):-len("-4.jsonl")]
        errs, exits = transcript(os.path.join(SESS, "KaidokuR22", f))
        cls = classify(" ".join(m for _, m in errs))
        role = w1_roles.get(name, "?")
        key = f"{role}/{cls}"
        w1_error_class_by_role[key] = w1_error_class_by_role.get(key, 0) + 1
        w1_exits.extend(e[0] for e in exits if e[0])
    w1_parent_errs, w1_parent_exit = transcript(os.path.join(SESS, "KaidokuR22.jsonl"))

    w2_seat_causes = {}
    for name in W2_MISSING:
        errs, exits = transcript(os.path.join(SESS, "KaidokuR22R", f"KaidokuR22R.{name}-6.jsonl"))
        cause = errs[-1][1] if errs else None
        w2_seat_causes[name] = {
            "terminal_id": f"KaidokuR22R.{name}-6",
            "transcript_last_error_utc": errs[-1][0] if errs else None,
            "transcript_error_class": classify(cause) if cause else None,
            "transcript_error_text": (cause or "")[:220],
            "session_exit_utc": exits[-1][0] if exits else None,
            "in_wave2_terminal_initial": f"KaidokuR22R.{name}-6" in w2_initial,
            "in_final_wave_outcomes_terminal": any(
                m["id"] == f"KaidokuR22R.{name}-6" and m.get("terminal")
                for m in final["wave2"]["members"]),
        }

    sources = [
        "final-wave-outcomes.json", "wave1-terminal-correction.json",
        "wave1-terminal.json", "wave2-terminal-initial.json",
        "wave2-missing-causes.json", "recovery-authority.json",
        "wave1-spec.json", "wave2-spec.json", "wave1-dispatch-attempts.json",
        "w1/swarm-registry.json", "wave1-dispatch.json", "wave2-dispatch.json",
        "wave2-spawn-try6.json",
    ]

    result = {
        "schema": "kaidoku-r23-historical-recount-v1",
        "generated_at_utc": "2026-10-21T14:40:48Z",
        "scope": "R22 reportless recount (author-side, read-only)",
        "recount": {
            "w1": {
                "spec_items": len(w1_names),
                "registry_members": len(w1_reg["members"]),
                "dispatch_result_ids": len(dispatch_ids),
                "dispatch_registry_id_sets_equal": w1_ids == dispatch_ids == final_w1,
                "expected_report_paths": len(w1_expected),
                "reports_present": len(w1_present),
                "reportless": len(w1_names) - len(w1_present),
                "report_dir_entries": sorted(os.listdir(os.path.join(R22, "w1"))),
                "seat_output_md_files": len(w1_out),
                "seat_output_md_nonzero": len(w1_out_nonzero),
                "seat_jsonl_files": len(w1_jsonl),
                "seat_transcripts_with_dispose_normal": sum(
                    1 for f in w1_jsonl
                    if transcript(os.path.join(SESS, "KaidokuR22", f))[1]
                    and transcript(os.path.join(SESS, "KaidokuR22", f))[1][-1][1:] == ("dispose", "normal")),
                "seat_exit_window_utc": [min(w1_exits), max(w1_exits)] if w1_exits else None,
                "parent_exit_utc": w1_parent_exit[-1][0] if w1_parent_exit else None,
                "parent_error_text": w1_parent_errs[-1][1][:220] if w1_parent_errs else None,
                "parent_error_count": len(w1_parent_errs),
                "transcript_error_class_by_role": dict(sorted(w1_error_class_by_role.items())),
                "per_seat_terminal_notification_receipts": 0,
                "per_seat_causal_records_superseded": len(w1_terminal["seats"]),
            },
            "w2": {
                "spec_items": len(w2_names),
                "spawn_ack_ids": len(w2_ack_ids),
                "dispatch_ack_id_set_matches_final": w2_ack_ids == final_w2,
                "expected_report_paths": len(w2_expected),
                "reports_present": len(w2_present),
                "reportless": len(w2_names) - len(w2_present),
                "seat_output_md_files": len(w2_out),
                "seat_output_md_zero": len(w2_out_zero),
                "missing_names": [n for n in w2_names
                                  if not os.path.isfile(os.path.join(ROOT, f".ufo/waves/round-22/w2/{n}.md"))],
            },
            "total_reportless": (len(w1_names) - len(w1_present)) + (len(w2_names) - len(w2_present)),
        },
        "classification": {
            "known_terminal_failures": len(W2_MISSING),
            "known_terminal_failures_w2": w2_seat_causes,
            "retained_intermediate_notification": sorted(w2_initial),
            "final_summary_only": [n for n, v in w2_seat_causes.items()
                                   if not v["in_wave2_terminal_initial"]],
            "unknown_per_child_w1": len(w1_names),
            "unknown_per_child_total": len(w1_names),
            "note": ("W2 nine are known terminal provider failures (final-wave-outcomes status "
                     "terminal_provider_failure); five of them have no retained intermediate "
                     "notification but each transcript carries the matching error text. "
                     "W1 has no per-seat terminal notification; 93 remain per-seat unknown. "
                     "W1 transcript error text is activity evidence, not terminal-cause proof."),
        },
        "superseded_assertions": [
            {
                "file": "wave1-terminal.json",
                "sha256": sha256(os.path.join(R22, "wave1-terminal.json")),
                "assertion_seats": len(w1_terminal["seats"]),
                "assertion_authority": w1_terminal["authority"],
                "status": "superseded by wave1-terminal-correction.json",
            },
            {
                "file": "recovery-authority.json",
                "sha256": sha256(os.path.join(R22, "recovery-authority.json")),
                "assertion": recovery["inherited_wave"]["cause"],
                "status": "superseded by wave1-terminal-correction.json",
            },
        ],
        "correction": {
            "sha256": sha256(os.path.join(R22, "wave1-terminal-correction.json")),
            "dispatched": correction["dispatched"],
            "initial_reports": correction["initial_reports"],
            "status_at_parent_observation": correction["status_at_parent_observation"],
            "cause": correction["cause"],
        },
        "sources": [
            {"path": f".ufo/waves/round-22/{p}", "sha256": sha256(os.path.join(R22, p))}
            for p in sources
        ],
        "limits": [
            "Author-side recount; not outside verification.",
            "Transcript error text proves model-call errors occurred, not that they caused seat disposal.",
            "R22 w1 late-report rule remains open; any fresh W1 report would reclassify.",
            "No claim about provider availability over time.",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")

    ok = (result["recount"]["w1"]["reportless"] == 93
          and result["recount"]["w2"]["reportless"] == 9
          and result["recount"]["total_reportless"] == 102)
    print(json.dumps({
        "w1_reportless": result["recount"]["w1"]["reportless"],
        "w2_reportless": result["recount"]["w2"]["reportless"],
        "total_reportless": result["recount"]["total_reportless"],
        "known_terminal_failures": result["classification"]["known_terminal_failures"],
        "unknown_per_child": result["classification"]["unknown_per_child_total"],
        "identity_checks": {
            "w1_ids_equal": result["recount"]["w1"]["dispatch_registry_id_sets_equal"],
            "w2_ack_equal": result["recount"]["w2"]["dispatch_ack_id_set_matches_final"],
        },
        "out": OUT,
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
