#!/usr/bin/env python3
"""receipt-forge.py -- wave-2 falsification harness for receipt-validate.py.

Copies the real retained run dir W/runs/pro-notesmd-cli to a fresh /tmp dir
per forgery, mutates file bytes and/or the recorded receipt.json, then runs
W/tools/receipt-validate.py on each forged copy. Prints a JSON verdict map:
which forgeries the validator catches (exit 1/2 with targeted findings) and
which it accepts (exit 0, or rejects only via the unrelated unrecognized_shape
finding that fires on every real round-17 receipt).

Never mutates anything under the lane. Read-only against W/runs and W/tools.
Run: python3 -I -B <this file> [--keep]
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17")
SRC = W / "runs" / "pro-notesmd-cli"
DONOR = W / "runs" / "pro-op"          # second real run, for log/stdout swaps
VALIDATOR = W / "tools" / "receipt-validate.py"
SRC_PREFIX = str(SRC) + "/"
SESSION = "rea-ghidra-eKKJuy"
LOG_REL = Path("logs") / SESSION
DONOR_LOG_REL = Path("logs") / "rea-ghidra-yRmWqx"


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def rewrite_paths(node, dst_prefix):
    """Rewrite every string starting with SRC_PREFIX to dst_prefix, so the
    copied receipt stays internally bound to the copied files."""
    if isinstance(node, dict):
        return {k: rewrite_paths(v, dst_prefix) for k, v in node.items()}
    if isinstance(node, list):
        return [rewrite_paths(v, dst_prefix) for v in node]
    if isinstance(node, str) and node.startswith(SRC_PREFIX):
        return dst_prefix + node[len(SRC_PREFIX):]
    return node


def log_slots(receipt):
    """Yield every recorded {bytes, path, sha256} dict for ghidra.log."""
    for entry in receipt.get("retained_logs") or []:
        f = (entry.get("files") or {}).get("ghidra.log")
        if isinstance(f, dict):
            yield f
    steps = receipt.get("steps") or {}
    step_items = steps.values() if isinstance(steps, dict) else steps
    for step in step_items or []:
        for entry in (step.get("retained_logs") or []):
            f = (entry.get("files") or {}).get("ghidra.log")
            if isinstance(f, dict):
                yield f


def rehash_log(receipt, log_path):
    """Update every recorded ghidra.log entry to the file's live digest."""
    digest = sha256_file(log_path)
    size = Path(log_path).stat().st_size
    for slot in log_slots(receipt):
        slot["sha256"] = digest
        slot["bytes"] = size


def normalize_steps(receipt):
    """Rewrite the dict-shaped steps to the list shape classify() expects."""
    steps = receipt.get("steps")
    if isinstance(steps, dict):
        receipt["steps"] = [dict(v, step=k) for k, v in steps.items()]


# --- forgery definitions ---------------------------------------------------
# Each mutator(dst_dir, receipt) -> description of what it changed.


def f_control(dst, r):
    return "pristine copy (path rewrite only)"


def f_shape_normalize(dst, r):
    normalize_steps(r)
    return "steps dict -> list; probes whether shape alone blocks acceptance"


def f_edit_ghidra_log(dst, r):
    p = dst / LOG_REL / "ghidra.log"
    with open(p, "a", encoding="utf-8") as fh:
        fh.write("2026-10-20 14:00:00 ERROR  (GolangSymbolAnalyzer) forged line\n")
    return "appended forged line to ghidra.log; receipt untouched"


def f_edit_ghidra_log_rehash(dst, r):
    p = dst / LOG_REL / "ghidra.log"
    with open(p, "a", encoding="utf-8") as fh:
        fh.write("2026-10-20 14:00:00 ERROR  (GolangSymbolAnalyzer) forged line\n")
    rehash_log(r, p)
    return "forged ghidra.log line + receipt digests updated to match"


def f_swap_log_other_run(dst, r):
    donor = DONOR / DONOR_LOG_REL / "ghidra.log"
    p = dst / LOG_REL / "ghidra.log"
    shutil.copyfile(donor, p)
    rehash_log(r, p)
    return ("swapped in pro-op's ghidra.log + receipt digests updated; "
            "session_dir still claims /tmp/kr17-rea-odi4abuq/rea-ghidra-eKKJuy")


def f_swap_log_keep_meta(dst, r):
    donor = DONOR / DONOR_LOG_REL / "ghidra.log"
    shutil.copyfile(donor, dst / LOG_REL / "ghidra.log")
    return "swapped in pro-op's ghidra.log; receipt digests untouched"


def f_pins_pre_forge_nofix(dst, r):
    carrier = r["carrier"]["path"]
    r["pins_pre"]["entries"][carrier]["sha256"] = "0" * 64
    return "pins_pre carrier sha forged to 0..0; pins_compare left equal=true"


def f_pins_pre_forge_consistent(dst, r):
    carrier = r["carrier"]["path"]
    r["pins_pre"]["entries"][carrier]["sha256"] = "0" * 64
    r["pins_pre"]["entries"][carrier]["size"] = 1
    r["pins_compare"]["equal"] = False
    r["pins_compare"]["changed"] = [carrier]
    return ("pins_pre carrier sha+size forged AND pins_compare forged to "
            "{equal:false, changed:[carrier]}: receipt now claims the carrier "
            "mutated mid-run; pins_pre of a doubly-pinned path is never "
            "re-verified against live bytes")


def f_delete_bound_sessions(dst, r):
    del r["bound_sessions"]
    return "deleted bound_sessions key entirely"


def f_carrier_sha_lie(dst, r):
    r["carrier"]["sha256_post"] = "f" * 64
    return "carrier.sha256_post forged to f..f; path unchanged"


def f_carrier_path_swap(dst, r):
    other = Path("/usr/bin/shfmt")
    r["carrier"]["path"] = str(other)
    digest = sha256_file(other)
    r["carrier"]["sha256_pre"] = digest
    r["carrier"]["sha256_post"] = digest
    return ("carrier.path+sha swapped to /usr/bin/shfmt while every step argv "
            "still says notesmd-cli; carrier<->argv never cross-checked")


def f_evidence_id_receipt(dst, r):
    steps = r["steps"]
    steps["analyze"]["evidence_id"] = (
        "ev_3d7ba7eca7ad3fbc187431def31c5e32079f1689d1441752511afef8a3743f41")
    return "steps.analyze.evidence_id replaced with pro-op's evidence id"


def f_evidence_id_file(dst, r):
    p = dst / "analyze.json"
    doc = json.loads(p.read_text(encoding="utf-8"))
    doc["evidence_id"] = "ev_" + "0" * 64
    p.write_text(json.dumps(doc, sort_keys=True, indent=2), encoding="utf-8")
    digest = sha256_file(p)
    r["steps"]["analyze"]["stdout_sha256"] = digest
    return ("analyze.json file edited (evidence_id -> ev_00..0) and "
            "stdout_sha256 updated; receipt evidence_id field left stale")


def f_step_exit_flip(dst, r):
    r["steps"]["analyze"]["exit"] = 1
    r["steps"]["analyze"]["argv"][3] = "definitely-not-rea"
    return "steps.analyze.exit forged to 1 and argv mutated"


def f_binding_flags_flip(dst, r):
    r["retained_logs"][0]["binding"] = {
        "logfile_ok": False, "target_ok": False}
    return "retained_logs[0].binding forged to {logfile_ok:false,target_ok:false}"


def f_delete_retained_logs(dst, r):
    del r["retained_logs"]
    shutil.rmtree(dst / "logs")
    return ("deleted retained_logs key AND the logs/ dir; "
            "CARRIER_REQUIRED only applies to carrier-shaped receipts")


def f_stdout_swap(dst, r):
    donor = DONOR / "analyze.json"
    p = dst / "analyze.json"
    shutil.copyfile(donor, p)
    r["steps"]["analyze"]["stdout_sha256"] = sha256_file(p)
    return ("analyze.json replaced by pro-op's analyze.json + recorded sha "
            "updated; receipt evidence_id still notesmd-cli's")


def f_timestamps_scramble(dst, r):
    r["steps"]["analyze"]["ended_at_utc"] = "2026-10-20T13:00:00.000000+00:00"
    r["pins_post"]["taken_at_utc"] = "2026-10-20T13:00:00.000000+00:00"
    return "ended_at_utc and pins_post.taken_at_utc moved before start"


def f_normalize_log_forge(dst, r):
    f_shape_normalize(dst, r)
    f_edit_ghidra_log_rehash(dst, r)
    return "shape-normalize + forged ghidra.log (rehashed): seeks exit 0"


def f_normalize_pins_forge(dst, r):
    f_shape_normalize(dst, r)
    f_pins_pre_forge_consistent(dst, r)
    return "shape-normalize + consistent pins_pre/pins_compare forgery"


def f_normalize_carrier_swap(dst, r):
    f_shape_normalize(dst, r)
    f_carrier_path_swap(dst, r)
    return "shape-normalize + carrier path/sha swap to /usr/bin/shfmt"


def f_normalize_delete_retained(dst, r):
    f_shape_normalize(dst, r)
    del r["retained_logs"]
    shutil.rmtree(dst / "logs")
    return "shape-normalize + retained_logs key and logs/ dir removed entirely"


FORGERIES = [
    ("control", f_control),
    ("shape-normalize", f_shape_normalize),
    ("edit-ghidra-log", f_edit_ghidra_log),
    ("edit-ghidra-log-rehash", f_edit_ghidra_log_rehash),
    ("swap-log-other-run", f_swap_log_other_run),
    ("swap-log-keep-meta", f_swap_log_keep_meta),
    ("pins-pre-forge-nofix", f_pins_pre_forge_nofix),
    ("pins-pre-forge-consistent", f_pins_pre_forge_consistent),
    ("delete-bound-sessions", f_delete_bound_sessions),
    ("delete-retained-logs", f_delete_retained_logs),
    ("carrier-sha-lie", f_carrier_sha_lie),
    ("carrier-path-swap", f_carrier_path_swap),
    ("evidence-id-receipt", f_evidence_id_receipt),
    ("evidence-id-file", f_evidence_id_file),
    ("step-exit-flip", f_step_exit_flip),
    ("binding-flags-flip", f_binding_flags_flip),
    ("stdout-swap", f_stdout_swap),
    ("timestamps-scramble", f_timestamps_scramble),
    ("normalize+log-forge", f_normalize_log_forge),
    ("normalize+pins-forge", f_normalize_pins_forge),
    ("normalize+carrier-swap", f_normalize_carrier_swap),
    ("normalize+delete-retained", f_normalize_delete_retained),
]


def main():
    keep = "--keep" in sys.argv
    workroot = Path(tempfile.mkdtemp(prefix="kr17-forge-"))
    results = {}
    for name, mutator in FORGERIES:
        dst = workroot / name
        shutil.copytree(SRC, dst)
        receipt_path = dst / "receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt = rewrite_paths(receipt, str(dst) + "/")
        desc = mutator(dst, receipt)
        receipt_path.write_text(
            json.dumps(receipt, sort_keys=True, indent=2) + "\n",
            encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-I", "-B", str(VALIDATOR), str(receipt_path)],
            capture_output=True, text=True)
        try:
            report = json.loads(proc.stdout)
            rec = report["receipts"][0]
            codes = sorted({f["code"] for f in rec.get("findings", [])})
            wheres = sorted({f["where"] for f in rec.get("findings", [])})
            results[name] = {
                "forgery": desc,
                "dir": str(dst),
                "exit": proc.returncode,
                "kind": rec.get("kind"),
                "valid": rec.get("valid"),
                "checks": rec.get("checks_performed"),
                "finding_codes": codes,
                "finding_wheres": wheres[:12],
            }
        except Exception:
            results[name] = {
                "forgery": desc,
                "dir": str(dst),
                "exit": proc.returncode,
                "stdout": proc.stdout[:2000],
                "stderr": proc.stderr[:2000],
            }
    passed_clean = [n for n, v in results.items() if v.get("exit") == 0]
    shape_only = [
        n for n, v in results.items()
        if v.get("finding_codes") == ["unrecognized_shape"]]
    out = {
        "source": str(SRC),
        "donor": str(DONOR),
        "validator": str(VALIDATOR),
        "workroot": str(workroot),
        "workroot_retained": keep,
        "results": results,
        "verdicts": {
            "exit0": passed_clean,
            "rejected_only_by_unrecognized_shape": shape_only,
            "note": (
                "unrecognized_shape fires on every real round-17 receipt: "
                "steps is a dict but classify() requires a list "
                "(receipt-validate.py:98). Forgeries in "
                "rejected_only_by_unrecognized_shape are otherwise "
                "undetected."),
        },
    }
    print(json.dumps(out, sort_keys=True, indent=2))
    if not keep:
        shutil.rmtree(workroot, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
