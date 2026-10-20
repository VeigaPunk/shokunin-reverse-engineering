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
RUNS = W / "runs"
SRC = RUNS / "pro-notesmd-cli"
VALIDATOR = W / "tools" / "receipt-validate.py"
SRC_PREFIX = str(SRC) + "/"


def pick_donor():
    """Pick a complete retained run dir (receipt + analyze.json + a session
    dir under logs/ with a nonempty ghidra.log) other than SRC. Peer waves
    regenerate runs mid-flight, so discovery happens at call time."""
    for cand in sorted(RUNS.iterdir()):
        if not cand.is_dir() or cand == SRC:
            continue
        logs = cand / "logs"
        if not (cand / "receipt.json").is_file() \
                or not (cand / "analyze.json").is_file() \
                or not logs.is_dir():
            continue
        for sess in sorted(logs.iterdir()):
            log = sess / "ghidra.log"
            if sess.is_dir() and log.is_file() and log.stat().st_size:
                return cand
    return None


DONOR = pick_donor()


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def first_log_dir(run_dir):
    """Discover the single session dir under RUN/logs/ (peer waves may
    regenerate run dirs, so the name is never hardcoded)."""
    logs = Path(run_dir) / "logs"
    kids = sorted(p.name for p in logs.iterdir() if p.is_dir())
    if not kids:
        raise SystemExit(f"no session dir under {logs}")
    return Path("logs") / kids[0]


LOG_REL = first_log_dir(SRC)
DONOR_LOG_REL = first_log_dir(DONOR) if DONOR else None


class NoDonor(Exception):
    """Raised by forgeries that need a second complete run when none exists."""


def need_donor():
    if DONOR is None:
        raise NoDonor("no complete donor run under W/runs at call time")


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
    need_donor()
    donor = DONOR / DONOR_LOG_REL / "ghidra.log"
    p = dst / LOG_REL / "ghidra.log"
    shutil.copyfile(donor, p)
    rehash_log(r, p)
    sess = r["retained_logs"][0]["session_dir"]
    return ("swapped in pro-op's ghidra.log + receipt digests updated; "
            f"session_dir still claims {sess}")


def f_swap_log_keep_meta(dst, r):
    need_donor()
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
    need_donor()
    steps = r["steps"]
    donor_r = json.loads((DONOR / "receipt.json").read_text(encoding="utf-8"))
    steps["analyze"]["evidence_id"] = donor_r["steps"]["analyze"]["evidence_id"]
    return "steps.analyze.evidence_id replaced with pro-op's evidence id"


def _all_log_entries(receipt):
    """Yield every retained-logs entry dict (top level + per step)."""
    for entry in receipt.get("retained_logs") or []:
        if isinstance(entry, dict):
            yield entry
    steps = receipt.get("steps") or {}
    step_items = steps.values() if isinstance(steps, dict) else steps
    for step in step_items or []:
        for entry in (step.get("retained_logs") or []):
            if isinstance(entry, dict):
                yield entry


def f_edit_log_content_keep_binding(dst, r):
    p = dst / LOG_REL / "ghidra.log"
    lines = p.read_text(encoding="utf-8").splitlines()
    lines = ["2026-10-20 11:30:08 INFO  (GolangSymbolAnalyzer) "
             "Go version 1.99.0" if "Go version" in ln else ln
             for ln in lines]
    lines.append("2026-10-20 11:30:09 INFO  (GoApiSnapshot) "
                 "Using Go API snapshot for go1.99 (forged)")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    rehash_log(r, p)
    return ("edited ghidra.log Go-version line + appended a forged snapshot "
            "line, preserving the two substrings check_binding re-derives "
            "(receipt-validate.py:142-143); digests updated to match")


def f_synthesize_bound_session(dst, r):
    """Fabricate a complete session from scratch: forged bound_sessions dir,
    self-authored ghidra.log containing the two magic substrings, copied
    script.log, all recorded paths/digests updated."""
    fake_sess = "/tmp/kr17-forged-aaaaaa/rea-ghidra-ZZfake"
    new_rel = Path("logs") / "rea-ghidra-ZZfake"
    carrier = r["carrier"]["path"]
    sha12 = r["carrier"]["sha256_post"][:12]
    newdir = dst / new_rel
    newdir.mkdir(parents=True, exist_ok=True)
    # self-authored log satisfying check_binding's substring test
    (newdir / "ghidra.log").write_text(
        f"2026-10-20 11:30:06 INFO  (LoggingInitialization) "
        f"Using log file: {fake_sess}/ghidra.log  \n"
        f"2026-10-20 11:30:07 INFO  (HeadlessAnalyzer) "
        f"IMPORTING: file://{fake_sess}/target-{sha12}.bin  \n"
        f"2026-10-20 11:30:08 INFO  (GolangSymbolAnalyzer) "
        f"Go version 1.42.0-forged  \n",
        encoding="utf-8")
    old_logdir = next(p for p in (dst / "logs").iterdir()
                      if p.is_dir() and p != newdir)
    # retain real script.log bytes at the forged path (bytes are real;
    # recorded path lies about provenance)
    shutil.copyfile(old_logdir / "script.log", newdir / "script.log")
    for entry in _all_log_entries(r):
        entry["session_dir"] = fake_sess
        for name, slot in (entry.get("files") or {}).items():
            np = dst / new_rel / name
            slot["path"] = str(np)
            slot["sha256"] = sha256_file(np)
            slot["bytes"] = np.stat().st_size
    r["bound_sessions"] = [fake_sess]
    shutil.rmtree(old_logdir)
    return ("synthesized a never-existent bound session: self-authored "
            "ghidra.log containing the two substrings check_binding looks "
            "for, bound_sessions replaced, every recorded digest updated; "
            "original session log deleted")


def f_normalize_delete_bound(dst, r):
    f_shape_normalize(dst, r)
    del r["bound_sessions"]
    return ("carrier-shaped receipt without bound_sessions: "
            "check_binding returns immediately at receipt-validate.py:124-125; "
            "bound_sessions is not in CARRIER_REQUIRED")


def f_bound_to_unbound(dst, r):
    r["unbound_sessions"] = r.get("bound_sessions") or []
    del r["bound_sessions"]
    return ("real session moved from bound_sessions to unbound_sessions; "
            "check_binding only fires when the key is present")



def f_synthesize_carrier_lie(dst, r):
    """Full fabrication: swap carrier to shfmt AND synthesize a fake bound
    session whose log names target-<shfmt sha[:12]>.bin. Receipt passes
    while claiming an analyze of shfmt that never happened; every step argv
    and stdout still belongs to notesmd-cli bytes."""
    other = Path("/usr/bin/shfmt")
    digest = sha256_file(other)
    r["carrier"]["path"] = str(other)
    r["carrier"]["sha256_pre"] = digest
    r["carrier"]["sha256_post"] = digest
    f_synthesize_bound_session(dst, r)
    return ("carrier swapped to /usr/bin/shfmt AND a fake bound session "
            "synthesized with a log naming target-" + digest[:12] +
            ".bin: receipt 'proves' an analyze of shfmt that never ran")

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
    need_donor()
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



def f_normalize_empty_retained(dst, r):
    f_shape_normalize(dst, r)
    r["retained_logs"] = []
    for step in r["steps"]:
        step["retained_logs"] = []
    shutil.rmtree(dst / "logs")
    return ("shape-normalize + retained_logs emptied at top level and in "
            "steps, logs/ removed: receipt retains zero log evidence; "
            "CARRIER_REQUIRED only checks key presence")

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
    ("bound-to-unbound", f_bound_to_unbound),
    ("normalize+delete-bound", f_normalize_delete_bound),
    ("synthesize-bound-session", f_synthesize_bound_session),
    ("synthesize-carrier-lie", f_synthesize_carrier_lie),
    ("edit-log-keep-binding", f_edit_log_content_keep_binding),
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
    ("normalize+empty-retained", f_normalize_empty_retained),
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
        try:
            desc = mutator(dst, receipt)
        except NoDonor as error:
            results[name] = {"forgery": "needs donor run",
                             "dir": str(dst), "skipped": str(error)}
            continue
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
                "exit0: validator accepted; rejected_only_by_unrecognized_"
                "shape: rejected only by the pre-hardening misclassification "
                "(steps dict vs list, fixed at 95e34db in classify()) — such "
                "forgeries are otherwise undetected."),
        },
    }
    print(json.dumps(out, sort_keys=True, indent=2))
    if not keep:
        shutil.rmtree(workroot, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
