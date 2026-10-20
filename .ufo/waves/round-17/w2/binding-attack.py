#!/usr/bin/env python3
"""Round-17 W2 falsification: attack bind_session + LogPoller in
W/tools/carrier-run.py (lane rev da64646a).

Imports carrier-run.py by path only. No REA, no Ghidra, no carrier execution.
All fixtures live under tempfile.mkdtemp(dir="/tmp"); Python run with -B.

bind_session (carrier-run.py:124-139) decides "this retained session dir
belongs to this carrier" by two substring tests against the CURRENT bytes of
the retained ghidra.log:
  logfile_ok: "Using log file: <session_dir>/ghidra.log" in text   (line 136)
  target_ok:  "IMPORTING: file://<session_dir>/target-<sha12>.bin" (lines 137-138)
Cases b01..b09 show which inputs bind that should not.

LogPoller.scan (carrier-run.py:198-230) discovers NEW dirs under
session_glob and copies ghidra.log/script.log to out_dir/logs/<basename>/.
Cases p01..p06 show silent drops, stale tracking, an uncaught crash, and a
shared-output-path collision.

Exit 0: every refusal expected held and no crash observed (attack failed).
Exit 1: at least one FALSE_BIND, STALE_DIGEST bind, silent drop, or crash.
JSON report on stdout.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17"
CARRIER_RUN = os.path.join(W, "tools", "carrier-run.py")
PINS = os.path.join(W, "tools", "pins.py")
# Real retained round-17 run, discovered at runtime (peers regenerate
# runs/ between waves, so nothing here is hardcoded).
RUNS = os.path.join(W, "runs")
LOGFILE_RE = re.compile(r"Using log file: (\S+)/ghidra\.log")
TARGET_RE = re.compile(r"target-([0-9a-f]{12})\.bin")


def load_tool(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cr = load_tool(CARRIER_RUN, "kr17_carrier_run")

CASES = []
def find_real_run():
    """Return (log_text, session_dir, carrier_sha256) from the first retained
    run that has a receipt with carrier sha and a logs/*/ghidra.log naming
    its own dir, or (None, None, None)."""
    try:
        run_dirs = sorted(os.listdir(RUNS))
    except OSError:
        return None, None, None
    for rd in run_dirs:
        rdir = os.path.join(RUNS, rd)
        rcp = os.path.join(rdir, "receipt.json")
        try:
            with open(rcp, "r", encoding="utf-8") as f:
                receipt = json.load(f)
            csha = receipt["carrier"]["sha256_pre"]
        except (OSError, ValueError, KeyError):
            continue
        logs_root = os.path.join(rdir, "logs")
        try:
            sess_names = sorted(os.listdir(logs_root))
        except OSError:
            continue
        for sn in sess_names:
            lp = os.path.join(logs_root, sn, "ghidra.log")
            try:
                with open(lp, "rb") as f:
                    text = f.read().decode("utf-8", "replace")
            except OSError:
                continue
            m = LOGFILE_RE.search(text)
            t = TARGET_RE.search(text)
            if m and t and csha.startswith(t.group(1)):
                return text, m.group(1), csha
    return None, None, None

def record(cid, kind, expected, observed, verdict, detail):
    CASES.append({
        "id": cid, "kind": kind, "expected": expected,
        "observed": observed, "verdict": verdict, "detail": detail,
    })
    print("[%s] %s: %s" % (verdict, cid, detail), file=sys.stderr)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_log(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = text.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    return data


def bind_case(cid, session_dir, log_text, carrier_sha, expect_bind,
              detail, mutate=None):
    """Write log_text as ghidra.log, optional mutate(path) hook (e.g. swap
    to symlink after recording the digest), call bind_session."""
    lp = os.path.join(SCRATCH, "logs", cid, "ghidra.log")
    data = write_log(lp, log_text)
    entry = {"path": lp, "sha256": sha(data), "bytes": len(data)}
    if mutate:
        mutate(lp)
        # digest recorded by the poller no longer describes the bytes
        entry["sha256_at_bind"] = sha(open(lp, "rb").read())
    files = {"ghidra.log": entry}
    got = cr.bind_session(session_dir, files, carrier_sha)
    bound = got["logfile_ok"] and got["target_ok"]
    verdict = "REFUSE_OK" if (not expect_bind and not bound) else \
              "BIND_OK" if (expect_bind and bound and
                            entry["sha256"] == entry.get("sha256_at_bind",
                                                         entry["sha256"])) \
              else ("FALSE_BIND" if bound else "WRONG_REFUSE")
    obs = dict(got)
    if "sha256_at_bind" in entry:
        obs["recorded_sha256"] = entry["sha256"]
        obs["bound_bytes_sha256"] = entry["sha256_at_bind"]
        if bound and entry["sha256"] != entry["sha256_at_bind"]:
            verdict = "FALSE_BIND_STALE_DIGEST"
    record(cid, "bind_session", ("bind" if expect_bind else "refuse"),
           obs, verdict, detail)


def genuine_log(session_dir, sha12):
    return (
        "2026-10-20 10:50:05 INFO  (LoggingInitialization) Using log file: "
        "%s/ghidra.log  \n"
        "2026-10-20 10:50:05 INFO  (ClassSearcher) Class search complete\n"
        "2026-10-20 10:50:05 INFO  (HeadlessAnalyzer) IMPORTING: "
        "file://%s/target-%s.bin  \n"
        "2026-10-20 10:51:11 INFO  (HeadlessAnalyzer) ANALYZING changes\n"
    ) % (session_dir, session_dir, sha12)


def main():
    global SCRATCH
    SCRATCH = tempfile.mkdtemp(prefix="kr17-bindfuzz-", dir="/tmp")
    try:
        # Carrier sha fixture: the real one from a retained run when present,
        # else a fixed 64-hex stand-in (b01-b08 only need internal
        # consistency between the log and the queried sha).
        real_text, real_session, real_csha = find_real_run()
        REAL_SHA = real_csha or ("0a1b2c3d4e5f" + "9" * (64 - 12))
        sess = os.path.join(SCRATCH, "rea-ghidra-VICTIM")
        other = os.path.join(SCRATCH, "rea-ghidra-OTHER")

        # --- bind_session ---------------------------------------------
        # b01 control: genuine-format log binds (expected).
        bind_case("b01", sess, genuine_log(sess, REAL_SHA[:12]), REAL_SHA,
                  True, "control: real-format log binds")

        # b02 assigned: log names a DIFFERENT session dir, correct sha.
        bind_case("b02", sess, genuine_log(other, REAL_SHA[:12]), REAL_SHA,
                  False, "log names rea-ghidra-OTHER, queried as VICTIM")

        # b03 assigned: correct dir, wrong sha prefix.
        wrong_sha = "ff" + REAL_SHA[2:]
        bind_case("b03", sess, genuine_log(sess, wrong_sha[:12]), REAL_SHA,
                  False, "log targets ff%10s..., queried sha %12s..."
                  % (wrong_sha[2:12], REAL_SHA[:12]))

        # b04: 12-hex prefix collision. carrier sha differs in all remaining
        # hex chars; bind_session only tests sha[:12] (carrier-run.py:137-138).
        collided_sha = REAL_SHA[:12] + "0" * (64 - 12)
        assert collided_sha != REAL_SHA
        bind_case("b04", sess, genuine_log(sess, REAL_SHA[:12]),
                  collided_sha, False,
                  "carrier sha differs at chars 13-64; needle only tests "
                  "sha[:12] -> target_ok on a different carrier")

        # b05: filename suffix. Log names target-<sha12>.bin.bak (e.g. a
        # rotated/imported-copy mention); needle "target-<sha12>.bin" is an
        # unanchored substring (carrier-run.py:137-138).
        txt = ("INFO  (HeadlessAnalyzer) backup copy IMPORTING: file://%s/"
               "target-%s.bin.bak\n" % (sess, REAL_SHA[:12]))
        txt += ("INFO  (LoggingInitialization) Using log file: %s/ghidra.log\n"
                % sess)
        bind_case("b05", sess, txt, REAL_SHA, False,
                  "only target-<sha12>.bin.bak present; substring match")

        # b06 assigned: both needles appear ONLY inside a stack trace, never
        # as real LoggingInitialization/IMPORTING lines.
        txt = (
            "2026-10-20 10:50:09 ERROR (HeadlessAnalyzer) Import failed\n"
            "java.lang.RuntimeException: prior attempt used "
            "Using log file: %s/ghidra.log\n"
            "\tat ghidra.app.util.headless.HeadlessAnalyzer.importFile\n"
            "Caused by: java.io.IOException: IMPORTING: file://%s/"
            "target-%s.bin\n"
        ) % (sess, sess, REAL_SHA[:12])
        bind_case("b06", sess, txt, REAL_SHA, False,
                  "needles only inside exception text; bind is substring-"
                  "based, not line-anchored")

        # b07: logfile suffix. Only the ROTATED name ghidra.log.1 is named;
        # needle ".../ghidra.log" is an unanchored substring.
        txt = (
            "INFO  (LoggingInitialization) rolled over; Using log file: "
            "%s/ghidra.log.1\n"
            "INFO  (HeadlessAnalyzer) IMPORTING: file://%s/target-%s.bin\n"
        ) % (sess, sess, REAL_SHA[:12])
        bind_case("b07", sess, txt, REAL_SHA, False,
                  "only ghidra.log.1 named; no line-end anchor")

        # b08 assigned-ish: retained ghidra.log replaced by a symlink to a
        # foreign file AFTER the poller recorded its digest. bind_session
        # (line 133) follows the symlink and binds bytes whose sha256 was
        # never recorded. Contrast: scan() refuses symlink SOURCES (line 210)
        # but nothing rechecks the retained path.
        foreign = os.path.join(SCRATCH, "foreign-real.log")
        write_log(foreign, genuine_log(sess, REAL_SHA[:12]))

        def to_symlink(p):
            os.unlink(p)
            os.symlink(foreign, p)

        bind_case("b08", sess,
                  "placeholder bytes recorded by poller\n", REAL_SHA, False,
                  "retained log swapped to symlink of a foreign log after "
                  "digest was recorded; bind_session follows it",
                  mutate=to_symlink)
        # b09 assigned: a log copied from another run. Fixture: verbatim
        # ghidra.log retained by a real round-17 run (discovered at runtime).
        if real_text is None:
            record("b09", "bind_session", "a retained run log",
                   "no runs/*/logs/*/ghidra.log found", "SKIPPED",
                   "no retained run log available to replay")
        else:
            # 9a: verbatim log queried with ITS OWN embedded session dir +
            #     carrier sha -> binds even though that dir no longer exists
            #     and was never tracked by this run: bind_session never
            #     checks the dir exists.
            bind_case("b09a", real_session, real_text, REAL_SHA, False,
                      "verbatim foreign-run log (%s); its session dir is "
                      "deleted; binds anyway -> replayed logs are "
                      "indistinguishable" % real_session)
            # 9b: same foreign log with the session-dir string rewritten to
            #     claim OUR dir and carrier -> binds; identity = "log claims
            #     it", nothing cryptographic or run-scoped.
            rewritten = real_text.replace(real_session, sess)
            bind_case("b09b", sess, rewritten, REAL_SHA, False,
                      "foreign run log naming VICTIM; no run-id/pid/nonce "
                      "check despite ownership.json existing per w1 "
                      "SentinelPollRace F2")


        # --- LogPoller -------------------------------------------------
        root = os.path.join(SCRATCH, "sessroot")
        out = os.path.join(SCRATCH, "out")
        os.makedirs(root)
        os.makedirs(out)
        globpat = os.path.join(root, "rea-ghidra-*")

        # p01 assigned: symlinked session dir -> silently dropped.
        real_d = os.path.join(SCRATCH, "elsewhere", "rea-ghidra-REAL")
        write_log(os.path.join(real_d, "ghidra.log"),
                  genuine_log(real_d, REAL_SHA[:12]))
        link_d = os.path.join(root, "rea-ghidra-LNK")
        os.symlink(real_d, link_d)
        poller = cr.LogPoller(out, globpat, set())
        poller.scan()
        obs = {"tracked": sorted(poller.tracked), "retained": poller.retained()}
        record("p01", "LogPoller", "session recorded or skip logged", obs,
               "SILENT_DROP" if not obs["tracked"] else "OK",
               "symlinked session dir excluded by list_session_dirs "
               "islink filter (carrier-run.py:73); nothing in the receipt "
               "records that a dir was skipped")
        os.unlink(link_d)

        # p02: real dir, ghidra.log itself is a symlink -> file skipped,
        # dir still tracked -> unbound_sessions entry with no explanation.
        d = os.path.join(root, "rea-ghidra-FILELINK")
        os.makedirs(d)
        os.symlink(foreign, os.path.join(d, "ghidra.log"))
        with open(os.path.join(d, "script.log"), "wb") as f:
            f.write(b"script line\n")
        poller = cr.LogPoller(out, globpat, set())
        poller.scan()
        ent = poller.retained()
        obs = {"session_files": sorted(ent[0]["files"]) if ent else None,
               "polls": ent[0]["polls"] if ent else None}
        verdict = "OK" if ent and sorted(ent[0]["files"]) == ["script.log"] \
            else "UNEXPECTED"
        record("p02", "LogPoller",
               "dir tracked, symlinked ghidra.log skipped", obs, verdict,
               "file-level islink skip (carrier-run.py:210) is silent: the "
               "session lands in unbound_sessions with no reason recorded")

        # p03 assigned: dir deleted mid-scan -> no crash, but the tracked
        # entry is NEVER pruned: retained() still reports a session dir that
        # no longer exists, and run() would count it in unbound_sessions.
        d2 = os.path.join(root, "rea-ghidra-VANISH")
        write_log(os.path.join(d2, "ghidra.log"),
                  genuine_log(d2, REAL_SHA[:12]))
        poller = cr.LogPoller(out, globpat, set())
        poller.scan()
        shutil.rmtree(d2)
        try:
            poller.scan()
            crash = None
        except Exception as e:  # noqa: BLE001 - reporting exact failure
            crash = "%s: %s" % (type(e).__name__, e)
        ret = poller.retained()
        dirs = [e["session_dir"] for e in ret]
        obs = {"crash": crash,
               "retained_dirs": dirs,
               "still_listed_after_delete": d2 in dirs,
               "dir_exists_on_disk": os.path.exists(d2)}
        record("p03", "LogPoller",
               "no crash; vanished dir should be dropped or marked", obs,
               "STALE_RETENTION" if not crash and obs[
                   "still_listed_after_delete"] else
               ("CRASH" if crash else "OK"),
               "tracked is keyed by dir and never reconciled against the "
               "filesystem (carrier-run.py:196,198-241); a dir deleted mid-"
               "run stays in retained_logs and unbound_sessions forever")

        # p04: dir replaced by a symlink mid-scan -> same stale retention;
        # also last scan silently keeps binding against the OLD copied bytes.
        d3 = os.path.join(root, "rea-ghidra-SWAP")
        write_log(os.path.join(d3, "ghidra.log"),
                  genuine_log(d3, REAL_SHA[:12]))
        poller = cr.LogPoller(out, globpat, set())
        poller.scan()
        shutil.rmtree(d3)
        os.symlink(os.path.join(SCRATCH, "elsewhere", "rea-ghidra-REAL"), d3)
        try:
            poller.scan()
            crash = None
        except Exception as e:  # noqa: BLE001
            crash = "%s: %s" % (type(e).__name__, e)
        ret = poller.retained()
        obs = {"crash": crash,
               "still_listed": d3 in [e["session_dir"] for e in ret],
               "dir_is_symlink_now": os.path.islink(d3)}
        record("p04", "LogPoller", "no crash; swapped dir flagged", obs,
               "STALE_RETENTION" if not crash and obs["still_listed"]
               else ("CRASH" if crash else "OK"),
               "dir->symlink swap between scans: dir vanishes from "
               "list_session_dirs but the stale tracked entry is retained")

        # p05 crash probe: out_dir/logs/<basename> pre-exists as a regular
        # file -> os.makedirs(exist_ok=True) at carrier-run.py:216 raises
        # FileExistsError, and NOTHING in scan/_run_polled/run catches it ->
        # traceback escapes run(); receipt.json is never written.
        root2 = os.path.join(SCRATCH, "sessroot2")
        out2 = os.path.join(SCRATCH, "out2")
        os.makedirs(root2)
        os.makedirs(out2)
        d4 = os.path.join(root2, "rea-ghidra-CRASH")
        write_log(os.path.join(d4, "ghidra.log"),
                  genuine_log(d4, REAL_SHA[:12]))
        blocker = os.path.join(out2, "logs", "rea-ghidra-CRASH")
        os.makedirs(os.path.dirname(blocker))
        with open(blocker, "wb") as f:
            f.write(b"not a dir")
        poller = cr.LogPoller(out2, os.path.join(root2, "rea-ghidra-*"),
                              set())
        try:
            poller.scan()
            crash = None
        except Exception as e:  # noqa: BLE001
            crash = "%s: %s" % (type(e).__name__, e)
        record("p05a", "LogPoller", "graceful skip or clear error", crash or
               "scan returned", "CRASH" if crash else "OK",
               "os.makedirs at carrier-run.py:216 is outside the OSError "
               "guards; a file at out/logs/<basename> kills scan")

        # p05b: same crash via the full run() path (injected fake runner, no
        # subprocess): the session dir appears AFTER the baseline
        # (carrier-run.py:321) exactly as a real REA session dir would, then
        # scan hits the blocker file -> exception escapes run(); no receipt.
        carrier = os.path.join(SCRATCH, "carrier.bin")
        with open(carrier, "wb") as f:
            f.write(b"fake carrier bytes")

        class FakeProc:
            def __init__(self):
                self.returncode = 0
                self._n = 0

            def poll(self):
                self._n += 1
                if self._n == 1:
                    # REA "starts": create the session dir with its log now,
                    # i.e. after run() already froze the baseline. Fresh
                    # basename plus its own blocker file.
                    d5 = os.path.join(root2, "rea-ghidra-CRASH2")
                    write_log(os.path.join(d5, "ghidra.log"),
                              genuine_log(d5, REAL_SHA[:12]))
                    b2 = os.path.join(out2, "logs", "rea-ghidra-CRASH2")
                    os.makedirs(os.path.dirname(b2), exist_ok=True)
                    with open(b2, "wb") as bf:
                        bf.write(b"not a dir")
                return None if self._n <= 2 else 0

            def wait(self, timeout=None):
                return 0

            def kill(self):
                return None

        def fake_runner(argv, cwd, out_f, err_f):
            return FakeProc()

        receipt = exc = None
        try:
            receipt, code = cr.run(
                carrier, "fuzz", out2, runner=fake_runner,
                session_glob=os.path.join(root2, "rea-ghidra-*"),
                pin_paths=[carrier], pins_path=PINS)
        except Exception as e:  # noqa: BLE001
            exc = "%s: %s" % (type(e).__name__, e)
        receipt_on_disk = os.path.exists(os.path.join(out2, "receipt.json"))
        record("p05b", "run()",
               "receipt written or recorded error", {
                   "exception": exc,
                   "receipt_written": receipt_on_disk,
               }, "CRASH" if (exc or not receipt_on_disk) else "OK",
               "uncaught FileExistsError in LogPoller.scan propagates "
               "through _run_polled's poll loop (carrier-run.py:415) and out "
               "of run() (carrier-run.py:331); receipt.json is never "
               "written -> exit is an interpreter traceback, not the "
               "contract's 0/1/2")

        # p06: basename collision under a nested session_glob. Two session
        # dirs with the same basename in different parents share
        # out/logs/<basename>/ (carrier-run.py:215); sorted order makes the
        # second the last writer -> session A's recorded sha256 describes
        # bytes that are no longer at the recorded path, and bind_session
        # reads the OTHER session's bytes.
        nest = os.path.join(SCRATCH, "nested")
        p1 = os.path.join(nest, "p1", "rea-ghidra-SAME")
        p2 = os.path.join(nest, "p2", "rea-ghidra-SAME")
        write_log(os.path.join(p1, "ghidra.log"),
                  genuine_log(p1, REAL_SHA[:12]))
        # foreign content naming p1 (as a copied/forged log would):
        write_log(os.path.join(p2, "ghidra.log"),
                  genuine_log(p1, REAL_SHA[:12]).replace(
                      "LoggingInitialization", "ForgedInit"))
        out3 = os.path.join(SCRATCH, "out3")
        os.makedirs(out3)
        poller = cr.LogPoller(out3,
                              os.path.join(nest, "*", "rea-ghidra-*"), set())
        poller.scan()
        ret = {e["session_dir"]: e for e in poller.retained()}
        ent1, ent2 = ret[p1], ret[p2]
        shared = ent1["files"]["ghidra.log"]["path"]
        now_sha = sha(open(shared, "rb").read())
        bind1 = cr.bind_session(p1, ent1["files"], REAL_SHA)
        obs = {
            "paths_equal": shared == ent2["files"]["ghidra.log"]["path"],
            "recorded_sha_p1": ent1["files"]["ghidra.log"]["sha256"],
            "sha_now_at_path": now_sha,
            "binding_p1": bind1,
        }
        false_bind = (bind1["logfile_ok"] and bind1["target_ok"] and
                      ent1["files"]["ghidra.log"]["sha256"] != now_sha)
        record("p06", "LogPoller", "each session retains its own bytes",
               obs, "FALSE_BIND" if false_bind else "OK",
               "logs_dir keyed by basename only (carrier-run.py:215): "
               "same-named session dirs share one output file; last writer "
               "wins and bind_session(p1) reads p2's bytes while the "
               "recorded digest attests p1's overwritten copy")

        defects = [c for c in CASES
                   if c["verdict"] not in ("BIND_OK", "REFUSE_OK", "OK")]
        report = {
            "tool_under_test": CARRIER_RUN,
            "tool_sha256": sha(open(CARRIER_RUN, "rb").read()),
            "rev": "da64646adcb19c1ede7537b799b8c7d283fe43da",
            "cases": CASES,
            "summary": {
                "total": len(CASES),
                "defects": len(defects),
                "defect_ids": [c["id"] for c in defects],
            },
        }
        print(json.dumps(report, sort_keys=True, indent=2))
        return 1 if defects else 0
    finally:
        shutil.rmtree(SCRATCH, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
