#!/usr/bin/env python3
"""R34LegacyGaps successor to the round-32 C1 acceptance-wrapper clauses.

The frozen round-32 counter (`tools/round-32/c1-arm64x-positive.py`,
sha256 7a534be6...0f1a) has four acceptance-wrapper clauses that its own
`--selftest` never exercises (A2SelftestHoles: C1-1..C1-4 survived). This file
re-states those four clauses as pure functions over text/JSON values and gives
each one the missing discriminatory cases:

  C1-1  entry cites the admitted source row (S099).
  C1-2  committed envelope equals the live envelope on every top-level key
        except `meta`; a non-object committed document is a clean fail, not a
        crash (the r32 mutant raised AttributeError there).
  C1-3  the live `data.evidence_id` is non-empty and appears in the entry text.
  C1-4  first-add commit time is strictly after the freeze commit time.

Inputs are isolated JSON records (see `--input`). Nothing here reads git, the
network, or binary content; the archived instrument is not modified and is not
declared conformant. `--selftest` uses embedded records and prints
`selftest cases=N failures=0`.

Exit: 0 all clauses pass (or selftest green), 1 any clause fails, 2 unusable
input record.
"""

import argparse
import json
import sys

CLAUSES = ("entry_cite", "committed_json", "envelope_equal", "evidence_id", "post_freeze")


def strip_meta(env):
    """Same exclusion as the frozen r32 wrapper: drop only the top-level `meta` key."""
    if not isinstance(env, dict):
        return env
    return {k: v for k, v in env.items() if k != "meta"}


def entry_cite(record):
    text = record.get("entry_text")
    claim_row = record.get("claim_row")
    if text is None:
        return False, "entry absent"
    if not isinstance(text, str):
        return False, "entry is not text"
    if not isinstance(claim_row, str) or not claim_row:
        return False, "claim row not supplied by the record"
    if claim_row not in text:
        return False, "entry does not cite %s" % claim_row
    return True, "ok"


def committed_json(record):
    text = record.get("committed_text")
    if text is None:
        return False, "committed envelope absent"
    try:
        obj = json.loads(text) if isinstance(text, str) else text
    except ValueError:
        return False, "committed envelope is not JSON"
    if not isinstance(obj, dict):
        return False, "committed envelope is not a JSON object"
    return True, "ok"


def envelope_equal(record):
    try:
        committed = json.loads(record["committed_text"]) if isinstance(record.get("committed_text"), str) \
            else record.get("committed_text")
    except ValueError:
        return False, "committed envelope is not JSON"
    live = record.get("live_envelope")
    if not isinstance(committed, dict):
        return False, "committed envelope is not a JSON object"
    if not isinstance(live, dict):
        return False, "live envelope absent or not an object"
    if strip_meta(committed) != strip_meta(live):
        return False, "committed envelope differs from the live envelope (full comparison)"
    return True, "ok"


def evidence_id(record):
    live = record.get("live_envelope")
    text = record.get("entry_text")
    if not isinstance(live, dict):
        return False, "live envelope absent or not an object"
    data = live.get("data")
    eid = data.get("evidence_id") if isinstance(data, dict) else None
    if not isinstance(eid, str) or not eid:
        return False, "live envelope carries no evidence_id"
    if not isinstance(text, str) or eid not in text:
        return False, "entry does not name %s" % eid
    return True, "ok"


def post_freeze(record):
    added = record.get("added")
    freeze_ct = record.get("freeze_ct")
    if not isinstance(added, int) or isinstance(added, bool):
        return False, "first-add commit time absent"
    if not isinstance(freeze_ct, int) or isinstance(freeze_ct, bool):
        return False, "freeze commit time absent"
    if added > freeze_ct:
        return True, "ok"
    return False, "committed envelope not added after the freeze"


CHECKS = {
    "entry_cite": entry_cite,
    "committed_json": committed_json,
    "envelope_equal": envelope_equal,
    "evidence_id": evidence_id,
    "post_freeze": post_freeze,
}


def evaluate(record):
    """Return [(clause, ok, why)]. Every clause is evaluated; a raising clause fails closed."""
    out = []
    for name in CLAUSES:
        try:
            ok, why = CHECKS[name](record)
        except Exception as exc:  # fail closed, never crash the checker
            ok, why = False, "clause raised %s: %s" % (type(exc).__name__, exc)
        out.append((name, bool(ok), why))
    return out


def run_record(record, label):
    results = evaluate(record)
    failed = 0
    for name, ok, why in results:
        if not ok:
            failed += 1
        print("%s\t%s\t%s" % ("ok" if ok else "FAIL", name, why))
    print("record=%s clauses=%d failures=%d" % (label, len(results), failed))
    return 0 if failed == 0 else 1


def live_envelope():
    return {
        "ok": True,
        "data": {
            "evidence_id": "ev-k01-fixture",
            "operation": "binary_overview",
            "subject": {"digest": {"sha256": "a" * 64}, "format": "pe", "architecture": "arm64"},
            "normalized_result": {"document": "target-aaaaaaaaaaaa.dll", "image_base": "0x180000000",
                                  "segments": [{"name": "Headers"}], "segment_count": 1,
                                  "procedure_count": 2},
        },
        "meta": {"command": ["rea", "inspect"], "duration": 1.0},
    }


def base_record():
    live = live_envelope()
    return {
        "claim_row": "S099",
        "entry_text": "# entry\n\n> source: S099; evidence: ev-k01-fixture\n",
        "committed_text": json.dumps(live, sort_keys=True),
        "live_envelope": live,
        "added": 1001,
        "freeze_ct": 1000,
    }


def rec(**over):
    r = base_record()
    r.update(over)
    return r


def selftest():
    live = live_envelope()

    def committed_with(**over):
        e = json.loads(json.dumps(live))
        e.update(over)
        return json.dumps(e, sort_keys=True)

    def data_with(**over):
        e = json.loads(json.dumps(live))
        e["data"].update(over)
        return json.dumps(e, sort_keys=True)

    meta_only = json.loads(json.dumps(live))
    meta_only["meta"] = {"command": ["other"], "duration": 9.9}
    extra_outer = json.loads(json.dumps(live))
    extra_outer["extra"] = "present"
    ok_flipped = json.loads(json.dumps(live))
    ok_flipped["ok"] = False

    cases = [
        ("accept: cited row, equal envelope, named evidence, post-freeze time", rec(), True, None),
        ("meta-only difference is excluded from the full comparison",
         rec(committed_text=json.dumps(meta_only, sort_keys=True)), True, None),
        ("C1-1 kill: entry without the claim row", rec(entry_text="# entry\n\nevidence: ev-k01-fixture\n"), False,
         "does not cite S099"),
        ("C1-1 kill: entry absent", rec(entry_text=None), False, "entry absent"),
        ("C1-1 kill: entry is empty", rec(entry_text=""), False, "does not cite S099"),
        ("claim row not supplied", rec(claim_row=None), False, "claim row not supplied"),
        ("C1-2 kill: same data, committed top-level ok differs",
         rec(committed_text=json.dumps(ok_flipped, sort_keys=True)), False, "full comparison"),
        ("C1-2 kill: same data, committed envelope carries an extra outer field",
         rec(committed_text=json.dumps(extra_outer, sort_keys=True)), False, "full comparison"),
        ("data payload differs", rec(committed_text=data_with(operation="inspect_artifact")), False,
         "full comparison"),
        ("C1-2 crash path: committed JSON is a list, clean fail",
         rec(committed_text="[]"), False, "not a JSON object"),
        ("committed text malformed", rec(committed_text="{not json"), False, "not JSON"),
        ("live envelope is a list", rec(live_envelope=[]), False, "live envelope absent or not an object"),
        ("C1-3 kill: live evidence_id omitted from the entry",
         rec(entry_text="# entry\n\n> source: S099\n"), False, "does not name ev-k01-fixture"),
        ("C1-3 kill: live data has no evidence_id", rec(live_envelope={"ok": True, "data": {}}), False,
         "no evidence_id"),
        ("C1-3: evidence_id present but entry is not text", rec(entry_text=None), False, "entry does not name"),
        ("C1-4 kill: first-added exactly at the freeze commit time", rec(added=1000), False,
         "not added after the freeze"),
        ("added before the freeze", rec(added=999), False, "not added after the freeze"),
        ("added absent", rec(added=None), False, "first-add commit time absent"),
        ("freeze commit time absent", rec(freeze_ct=None), False, "freeze commit time absent"),
        ("added one second after the freeze", rec(added=1001), True, None),
    ]
    fails = 0
    for name, record, want, why_sub in cases:
        results = evaluate(record)
        got = all(ok for _, ok, _ in results)
        detail = "; ".join(w for _, ok, w in results if not ok) or "all clauses ok"
        ok = got == want and (why_sub is None or why_sub in detail)
        fails += not ok
        print("%s\t%s\t%s" % ("ok" if ok else "FAIL", name, detail))
    print("selftest cases=%d failures=%d" % (len(cases), fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="round-34 successor to the r32 C1 acceptance-wrapper clauses")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--input", metavar="RECORD.json",
                    help="one JSON record: claim_row, entry_text, committed_text, live_envelope, added, freeze_ct")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.input:
        ap.error("one of --selftest or --input is required")
    try:
        with open(a.input, encoding="utf-8") as fh:
            record = json.load(fh)
    except (OSError, ValueError) as exc:
        print("INPUT unusable: %s" % exc)
        sys.exit(2)
    if not isinstance(record, dict):
        print("INPUT unusable: record is not a JSON object")
        sys.exit(2)
    sys.exit(run_record(record, a.input))


if __name__ == "__main__":
    main()
