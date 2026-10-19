#!/usr/bin/env python3
"""EX-27 round-4 regression battery — re-run round-3's full battery against the revised tool.

Seat EX-27, chain c3, wave arc3-loop1-round4, 2026-10-19.
READ-ONLY over every custody path. Scratch under /var/tmp/ex27-r4. /tmp never used.

Legs
  A  matrix18  — the 13 CR-4/battery.py rewrite forms + 5 same-content/fencing forms,
                 driven through the REAL tool (round-2/round-3 recorded classes).
  B  v1shapes  — round-1 canonical stanza / cross-format / pipe sidecar / sums, the
                 EX-35 fixtures, synthetic v1 anchors (stanza/sums/pipe), junk.
  C  label     — v1 label defect declared, v2 UTC render correct + TZ-invariant.
  D  selftest  — case count, case NAMES (prior 22 must all still be present), and the
                 missing-scratch-dir declared class.
  E  holes     — D2 EACCES probes (capture + verify), write-guard --paths X --out X.
  F  identity  — live pair capture-vs-capture (real paths, read-only) + receipt self-pin.
  G  inject    — the four round-3 named injections, probed independently:
                 (a) sidecar path scope, (b) out.parent.mkdir outside the guarded try,
                 (c) coverage gate counts stanzas not distinct paths,
                 (d) both-sides-absent semantics + the README ruling text.
  H  sabotage  — non-vacuity: each G check must go RED on the pre-revision bytes and on
                 a byte-sabotaged copy of the revision under test.

Profiles
  --phase r3   expectations = the round-3 landed classes (7cd19c3c): the four injections
               are OPEN (declared residuals), selftest 22, etc.
  --phase r4   expectations = the round-4 declared classes: (a)-(c) CLOSED, (d) ruled in
               the README, selftest >= 24 with the prior 22 names retained.

The tool under test is either the working-tree path or a pinned copy (--tool-src); its
sha256 is recorded before/after every leg and any mid-run movement aborts the run
(identity discipline, rule #14). Receipts self-record the tool sha (`# tool:` header);
the harness cross-checks that line against the pinned bytes.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
TOOL_WORK = REPO / ".ufo/gates/custody-pair/custody-pair.py"
README_WORK = REPO / ".ufo/gates/custody-pair/README.md"
R2 = REPO / ".ufo/waves/arc3-loop1-round2"
R1 = REPO / ".ufo/waves/arc3-loop1-round1"
ROOT = Path("/var/tmp/ex27-r4")

ORIG = b'{"mcp": {"servers": {"alpha": {"cmd": "a"}}}}\n'
MAL = b'{"mcp": {"servers": {"alpha": {"cmd": "EVIL"}}}}\n'
FIXTURE_EPOCH = 1792011200  # 2026-10-14T20:53:20Z, the round-1 defect epoch

# The 22 case names the round-3 landed revision reports CLEAN (D-leg cross-check).
# Captured from the landed revision's own `case <name> PASS` lines
# (`/var/tmp/ex27-r4/runs/r3-baseline-7cd19c3c/scratch/raw/selftest-good.txt`), not typed
# from memory — a mis-transcribed expectation would be a harness bug, not a regression.
R3_CASE_NAMES = [
    "capture-ok-exit-0", "receipt-shape-v2-fields", "sidecar-self-hash",
    "verify-receipt-vs-live-clean", "same-content-rewrite-inplace-ctime-pin",
    "same-content-rewrite-rename-inode-pin", "content-drift-detected",
    "absent-path-detected", "metadata-drift-detected", "label-utc-render-tz-independent",
    "v1-stanza-compat-and-mutation", "sums-v1-compat", "pipe-v1-compat",
    "unparsable-receipt-usage-exit", "refuses-to-write-over-custody-path",
    "unreadable-path-is-unevaluable", "unevaluable-never-matches",
    "parsed-unevaluable-reference-never-matches", "partial-reference-require-paths-gate",
    "refuses-to-write-over-scoped-path", "selftest-missing-scratch-usage-exit",
    "refuses-write-through-hardlink-alias",
]

A_EXPECT = {
    "A1_cp_a": "REWRITE-DRIFT", "A2_cp_a_remove_dest": "REWRITE-DRIFT", "A3_cp_p": "REWRITE-DRIFT",
    "A4_rsync_a_default": "REWRITE-DRIFT", "A5_rsync_a_inplace": "REWRITE-DRIFT",
    "A6_tar_restore": "REWRITE-DRIFT", "A7_copy_new_then_mv": "REWRITE-DRIFT",
    "A8_inplace_modify_no_restore": "CONTENT-DRIFT", "A9_inplace_modify_then_restore": "CONTENT-DRIFT",
    "A10_restore_bytes_plus_touch_r": "CONTENT-DRIFT", "A11_hardlink_alias_restore": "CONTENT-DRIFT",
    "A12_reflink_replace": "REWRITE-DRIFT", "A13_rename_swap_pristine_hardlink": "CONTENT-DRIFT",
    "A9s_truncate_restore": "REWRITE-DRIFT", "A10s_truncate_restore_touch": "REWRITE-DRIFT",
    "A11s_hardlink_truncate_restore": "REWRITE-DRIFT", "A14_chmod_only": "METADATA-DRIFT",
    "A15_delete_after_capture": "ABSENT",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, cwd=cwd)
    return r.returncode, (r.stdout + r.stderr)


def pick(phase, r3, r4):
    return r3 if phase == "r3" else r4


class Battery:
    def __init__(self, phase, scratch, tool_path, baseline_tool):
        self.phase = phase
        self.scratch = Path(scratch)
        self.tool = Path(tool_path)
        self.baseline_tool = Path(baseline_tool)
        self.raw = self.scratch / "raw"
        self.raw.mkdir(parents=True, exist_ok=True)
        self.rows = []
        self.tool_start = sha256_file(self.tool)
        self.baseline_sha = sha256_file(self.baseline_tool) if self.baseline_tool.exists() else None

    # ---- helpers ----------------------------------------------------------
    def row(self, leg, name, **kw):
        kw.update({"leg": leg, "name": name})
        self.rows.append(kw)
        return kw

    def lograw(self, name, text):
        (self.raw / name).write_text(text, encoding="utf-8")

    def tool_cmd(self, *args, tool=None):
        rc, out = sh([sys.executable, str(tool or self.tool)] + [str(a) for a in args])
        return rc, out

    @staticmethod
    def field(text, key):
        m = re.search(r"^%s:\s*(\S+)\s*$" % key, text, re.M)
        return m.group(1) if m else None

    def cap(self, out, path):
        rc, txt = self.tool_cmd("capture", "--out", out, "--label", Path(out).stem, "--paths", path)
        self.lograw(Path(out).name + ".stdout", txt)
        return rc, txt

    def verify(self, a, b=None, live=False, extra=()):
        args = ["verify", a] + ([] if live else [b]) + (["--live"] if live else []) + list(extra)
        return self.tool_cmd(*args)

    def tool_check(self):
        now = sha256_file(self.tool)
        if now != self.tool_start:
            raise SystemExit("TOOL MOVED MID-RUN: %s -> %s (abort)" % (self.tool_start, now))

    def receipt_tool_pin(self, receipt_text):
        m = re.search(r"^#\s*tool:\s*(\S+)\s+sha256\s+([0-9a-f]{64})", receipt_text, re.M)
        return m.group(2) if m else None

    # -----------------------------------------------------------------------
    # Leg A — attack matrix (18 forms)
    # -----------------------------------------------------------------------
    def fresh(self, name):
        d = self.scratch / "bench" / name
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        p = d / "target.json"
        p.write_bytes(ORIG)
        os.utime(p, (FIXTURE_EPOCH, FIXTURE_EPOCH))
        b = d / "backup.json"
        b.write_bytes(ORIG)
        shutil.copystat(p, b)
        shutil.copy2(p, d / "pristine.json")
        sh(f"cp -a {b} {d}/backup-cp-a.json")
        sh(f"mkdir -p {d}/srcdir {d}/dstdir && cp -a {p} {d}/srcdir/target.json && cp -a {p} {d}/dstdir/target.json")
        sh(f"tar -C {d} -cf {d}/backup.tar --format=gnu target.json")
        return d, p

    def attack_bodies(self):
        def A1(d, p): return sh(f"cp -a {d}/backup.json {p}")
        def A2(d, p): return sh(f"cp -a --remove-destination {d}/backup.json {p}")
        def A3(d, p): return sh(f"cp -p {d}/backup.json {p}")
        def A4(d, p):
            open(p, "wb").write(MAL)
            return sh(f"rsync -a --checksum {d}/backup.json {p}")
        def A5(d, p):
            open(p, "wb").write(MAL)
            return sh(f"rsync -a --inplace --checksum {d}/backup.json {p}")
        def A6(d, p):
            open(p, "wb").write(MAL)
            return sh(f"tar -C {d} --overwrite -xf {d}/backup.tar target.json")
        def A7(d, p):
            sh(f"cp -a {d}/backup.json {d}/stage.json")
            return sh(f"mv -f {d}/stage.json {p}")
        def A8(d, p):
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            return 0, "in-place rewrite (attacker bytes persist)"
        def A9(d, p):
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.flush(); os.fsync(f.fileno())
            return 0, "in-place rewrite then original bytes re-written (no truncate; battery.py verbatim)"
        def A10(d, p):
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.flush(); os.fsync(f.fileno())
            sh(f"touch -r {d}/backup.json {p}")
            return 0, "restore bytes (no truncate) + touch -r backup (mtime/atime restored)"
        def A11(d, p):
            sh(f"ln {p} {d}/alias")
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.flush(); os.fsync(f.fileno())
            sh(f"touch -r {d}/backup.json {p}")
            return 0, f"hardlink alias {d}/alias; in-place modify+restore (no truncate); touch -r"
        def A12(d, p): return sh(f"cp --reflink=always {d}/backup.json {p}")
        def A13(d, p):
            sh(f"ln {p} {d}/pristine_link")
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            sh(f"mv -f {d}/pristine_link {p}")
            sh(f"touch -r {d}/backup.json {p}")
            return 0, "hardlink swap-back (same inode; battery.py verbatim)"
        def A9s(d, p):
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.truncate(); f.flush(); os.fsync(f.fileno())
            return 0, "in-place truncate+write, bytes restored with truncate (same content)"
        def A10s(d, p):
            A9s(d, p)
            sh(f"touch -r {d}/backup.json {p}")
            return 0, "same-content restore + touch -r mtime forgery (ctime residue)"
        def A11s(d, p):
            sh(f"ln {p} {d}/alias")
            A9s(d, p)
            sh(f"touch -r {d}/backup.json {p}")
            return 0, "hardlink alias present; same-content restore via same inode; touch -r"
        def A14(d, p):
            os.chmod(p, 0o600)
            return 0, "chmod-only, content untouched (EX-33 R-K class)"
        def A15(d, p):
            os.unlink(p)
            return 0, "path deleted after capture (EX-33 R-I class)"
        return [
            ("A1_cp_a", A1), ("A2_cp_a_remove_dest", A2), ("A3_cp_p", A3),
            ("A4_rsync_a_default", A4), ("A5_rsync_a_inplace", A5), ("A6_tar_restore", A6),
            ("A7_copy_new_then_mv", A7), ("A8_inplace_modify_no_restore", A8),
            ("A9_inplace_modify_then_restore", A9), ("A10_restore_bytes_plus_touch_r", A10),
            ("A11_hardlink_alias_restore", A11), ("A12_reflink_replace", A12),
            ("A13_rename_swap_pristine_hardlink", A13),
            ("A9s_truncate_restore", A9s), ("A10s_truncate_restore_touch", A10s),
            ("A11s_hardlink_truncate_restore", A11s), ("A14_chmod_only", A14),
            ("A15_delete_after_capture", A15),
        ]

    def leg_a_matrix(self):
        caught = 0
        for name, fn in self.attack_bodies():
            d, p = self.fresh(name)
            A = self.scratch / "logs" / f"{name}.A.txt"
            B = self.scratch / "logs" / f"{name}.B.txt"
            A.parent.mkdir(parents=True, exist_ok=True)
            rc_pre, pre = self.cap(A, p)
            rc_atk, atk_note = fn(d, p)
            rc_post, post = self.cap(B, p)
            rc_ab, out_ab = self.verify(A, B)
            self.lograw(f"{name}.verifyAB.txt", out_ab)
            m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)\s+(.*?)\s+exit=(\d+)", out_ab, re.M)
            verdict, exitv = (m.group(1), int(m.group(4))) if m else ("?", None)
            moved_m = re.search(r"moved=([^\s]+)", out_ab)
            moved = moved_m.group(1) if moved_m else ""
            pre_text = A.read_text() if A.exists() else ""
            post_text = B.read_text() if B.exists() else ""
            sha_pre, sha_post = self.field(pre_text, "SHA256"), self.field(post_text, "SHA256")
            sha_same = bool(sha_pre is not None and sha_pre == sha_post)
            expect = A_EXPECT[name]
            ino_same = self.field(pre_text, "INODE") == self.field(post_text, "INODE")
            ct_same = self.field(pre_text, "CTIME_NS") == self.field(post_text, "CTIME_NS")
            mt_same = self.field(pre_text, "MTIME_NS") == self.field(post_text, "MTIME_NS")
            hold = (verdict == expect)
            caught += 1 if hold else 0
            self.row("A", name, rc_pre=rc_pre, rc_post=rc_post, rc_attack=rc_atk,
                     sha_same=sha_same, inode_same=ino_same, ctime_ns_same=ct_same,
                     mtime_ns_same=mt_same,
                     sha_only_view=("BLIND" if sha_same else "caught"),
                     verdict=verdict, exit=exitv, moved=moved, expect=expect, hold=hold)
        self.tool_check()
        return {"forms": len(self.rows), "verdict_matches": caught}

    # -----------------------------------------------------------------------
    # Leg B — v1 shapes
    # -----------------------------------------------------------------------
    def live_sections(self, tag):
        rc, out = self.tool_cmd("capture", "--out", "-", "--label", tag)
        self.lograw(f"live-capture-{tag}.txt", out)
        secs = {}
        for part in re.split(r"^PATH: ", out, flags=re.M)[1:]:
            lines = part.split("\n", 1)
            secs[lines[0].strip()] = lines[1] if len(lines) > 1 else ""
        return secs

    def drift_reconcile(self, ref_receipt):
        text = ref_receipt.read_text()
        ref = {}
        for part in re.split(r"^PATH: ", text, flags=re.M)[1:]:
            lines = part.split("\n", 1)
            p = lines[0].strip()
            body = lines[1] if len(lines) > 1 else ""
            mv = re.search(r"^MTIME_UTC:\s*(.+?)\s*$", body, re.M)
            ref[p] = {"sha": self.field(body, "SHA256"), "mtime_v1": mv.group(1) if mv else None}
        live = self.live_sections("drift-reconcile")
        exp = {"content_drift": [], "label_defect": [], "sha_agree": 0, "paths": len(ref)}
        for p, r in ref.items():
            lsec = live.get(p, "")
            lsha = self.field(lsec, "SHA256")
            epoch = self.field(lsec, "MTIME_EPOCH")
            if r["sha"] and lsha:
                if r["sha"] == lsha:
                    exp["sha_agree"] += 1
                else:
                    exp["content_drift"].append(p)
            if r["mtime_v1"] and epoch:
                loose = r["mtime_v1"].replace("T", " ").replace("Z", "").strip()
                lt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(epoch)))
                gt = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(epoch)))
                if loose == lt and loose != gt:
                    exp["label_defect"].append(p)
        return exp

    def leg_b_v1shapes(self):
        live = {}
        for p in (Path.home() / ".config/devin/mcp_config.json",
                  Path.home() / ".omp/agent/mcp.json",
                  Path.home() / ".kimi-code/config.toml",
                  Path.home() / ".bashrc", Path.home() / ".profile"):
            live[str(p)] = sha256_file(p)
        self.lograw("live-protein-shas.json", json.dumps(live, indent=1))
        r1 = R1 / "claims/cross/receipts/config-pre-pair.txt"
        r1_meta = R1 / "claims/cross/receipts/config-pre-pair-metadata.txt"
        r1_sums = R1 / "claims/c3/EX-26/custody-sha256.txt"
        ex35 = R2 / "claims/c3/EX-35/fixtures"

        exp = self.drift_reconcile(r1)
        self.lograw("drift-expectation.json", json.dumps(exp, indent=1))
        ndrift = len(exp["content_drift"])
        exp_exit = 10 if ndrift else 12

        def v1_case(name, ref, want_labels):
            rc, out = self.verify(str(ref), live=True)
            self.lograw(f"v1shape-{name}.txt", out)
            nlabel = out.count("LABEL-DEFECT")
            m = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out)
            sha_agree = int(m.group(1)) if m else None
            hold = (rc == exp_exit and sha_agree == exp["sha_agree"] and
                    (not want_labels or nlabel >= len(exp["label_defect"])))
            self.row("B", name, ref=str(ref), exit=rc, sha_agree=sha_agree, label_defect=nlabel,
                     expect_exit=exp_exit, expect_sha_agree=exp["sha_agree"],
                     expect_labels=len(exp["label_defect"]) if want_labels else None,
                     content_drift=[Path(p).name for p in exp["content_drift"]], hold=bool(hold))
            return rc, out

        v1_case("r1-canonical-vs-live", r1, True)
        v2cap = self.scratch / "logs" / "custody-live-v2.txt"
        self.tool_cmd("capture", "--out", v2cap, "--label", "ex27-b2")
        rc2, out2 = self.verify(str(r1), str(v2cap))
        self.lograw("v1shape-crossformat.txt", out2)
        n2 = out2.count("LABEL-DEFECT")
        m2 = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out2)
        hold2 = (rc2 == exp_exit and (int(m2.group(1)) if m2 else None) == exp["sha_agree"]
                 and n2 >= len(exp["label_defect"]))
        self.row("B", "r1-canonical-vs-fresh-v2", exit=rc2,
                 sha_agree=int(m2.group(1)) if m2 else None, label_defect=n2,
                 expect_exit=exp_exit, expect_sha_agree=exp["sha_agree"], hold=bool(hold2))
        rc3, out3 = self.verify(str(r1_meta), live=True)
        self.lograw("v1shape-pipe.txt", out3)
        m3 = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out3)
        hold3 = (rc3 == exp_exit and (int(m3.group(1)) if m3 else None) == exp["sha_agree"])
        self.row("B", "r1-metadata-pipe-vs-live", exit=rc3,
                 sha_agree=int(m3.group(1)) if m3 else None, label_defect=out3.count("LABEL-DEFECT"),
                 expect_exit=exp_exit, expect_sha_agree=exp["sha_agree"], hold=bool(hold3))
        rc4, out4 = self.verify(str(r1_sums), live=True)
        self.lograw("v1shape-sums.txt", out4)
        m4 = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out4)
        hold4 = ((int(m4.group(1)) if m4 else None) == exp["sha_agree"] and
                 rc4 == (10 if ndrift else 0))
        self.row("B", "r1-sums-vs-live", exit=rc4, sha_agree=int(m4.group(1)) if m4 else None,
                 expect_exit=(10 if ndrift else 0), hold=bool(hold4))
        # partial 1-of-5: declared default unchanged in BOTH profiles (r3: exit 0 default)
        p5 = ex35 / "v1-partial-1of5.txt"
        rc5, out5 = self.verify(str(p5), live=True)
        self.lograw("v1shape-partial-default.txt", out5)
        rc5r, out5r = self.verify(str(p5), live=True, extra=("--require-paths", "5"))
        self.lograw("v1shape-partial-require5.txt", out5r)
        r5_supported = "REFERENCE-COVERAGE" in out5r
        hold5 = (rc5 == 0 and r5_supported and rc5r == 2)
        self.row("B", "ex35-partial-1of5-default-vs-require5", exit=rc5, require5_exit=rc5r,
                 require5_supported=r5_supported, expect_default=0, expect_require5=2,
                 hold=bool(hold5))
        for nm, fx, base_agree, expx in (("ex35-corrupt-sha", "v1-corrupt-sha.txt", 4, 10),
                                         ("ex35-swap-sha", "v1-swap-sha.txt", 3, 10),
                                         ("ex35-absent-path", "v1-absent-path.txt", None, 13)):
            rc, out = self.verify(str(ex35 / fx), live=True)
            self.lograw(f"v1shape-{nm}.txt", out)
            m = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out)
            agree = int(m.group(1)) if m else None
            if nm == "ex35-absent-path":
                want_exit = 10 if ndrift else 13
                hold = (rc == want_exit and "ABSENT" in out)
            else:
                want_exit = expx
                hold = (rc == want_exit and agree == base_agree - ndrift)
            self.row("B", nm + "-vs-live", exit=rc, sha_agree=agree, expect_exit=want_exit,
                     expect_sha_agree=(None if base_agree is None else base_agree - ndrift), hold=bool(hold))
        junk = self.scratch / "logs" / "junk.txt"
        junk.write_text("not a receipt at all\n")
        rc9, out9 = self.verify(str(junk), live=True)
        self.lograw("v1shape-junk.txt", out9)
        self.row("B", "junk-receipt", exit=rc9, expect_exit=2, hold=(rc9 == 2))
        # remaining EX-35 fixtures: classes derived at run time from the drift
        # expectation (fixed counts would encode the operator-side config.toml drift)
        for nm, fxname, expect in (("ex35-empty", "empty.txt", "usage"),
                                   ("ex35-comment-only", "comment-only.txt", "usage"),
                                   ("ex35-v1-compact-only", "v1-compact-only.txt", "content-or-match"),
                                   ("ex35-v1-no-time", "v1-no-time.txt", "content-or-match"),
                                   ("ex35-v1-sums", "v1-sums.txt", "content-or-match")):
            rc, out = self.verify(str(ex35 / fxname), live=True)
            self.lograw(f"v1shape-{nm}.txt", out)
            m = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out)
            agree = int(m.group(1)) if m else None
            if expect == "usage":
                hold = (rc == 2 and "USAGE" in out)
                want = "USAGE exit 2"
            else:
                want = "exit 10 + sha %d/%d (drift-derived)" % (exp["sha_agree"], exp["paths"])
                hold = (rc == 10 and agree == exp["sha_agree"])
            self.row("B", nm + "-vs-live", exit=rc, sha_agree=agree, expect=want, hold=bool(hold))
        # synthetic v1 anchors (drift-free, scratch)
        fx = self.scratch / "v1anchor.conf"
        fx.write_bytes(b"v1 anchor fixture\n")
        os.utime(fx, (FIXTURE_EPOCH, FIXTURE_EPOCH))
        _, sec_txt = self.tool_cmd("capture", "--out", "-", "--paths", str(fx))
        sha = self.field(sec_txt, "SHA256")
        size = self.field(sec_txt, "SIZE")
        local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(FIXTURE_EPOCH))
        utc = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(FIXTURE_EPOCH))
        stanza = self.scratch / "logs" / "synth-v1-stanza.txt"
        stanza.write_text("PATH: %s\nEXISTS: yes\nSIZE: %s\nMTIME_UTC: %s\n"
                          "MODE: 644  UID: %d  GID: %d\nSHA256: %s\n"
                          % (fx, size, local, os.getuid(), os.getgid(), sha))
        rc10, out10 = self.verify(str(stanza), live=True)
        self.lograw("v1shape-synth-stanza.txt", out10)
        self.row("B", "synth-v1-stanza-vs-live", exit=rc10, label_defect=out10.count("LABEL-DEFECT"),
                 expect_exit=12, expect_labels=1, expect_sha_agree=1, expect_uttc=utc,
                 hold=(rc10 == 12 and out10.count("LABEL-DEFECT") == 1 and
                       "SHA256-CONTRACT: 1/1" in out10))
        sums = self.scratch / "logs" / "synth-v1-sums.txt"
        sums.write_text("%s  %s\n" % (sha, fx))
        rc11, out11 = self.verify(str(sums), live=True)
        self.lograw("v1shape-synth-sums.txt", out11)
        self.row("B", "synth-v1-sums-vs-live", exit=rc11, expect_exit=0, expect_sha_agree=1,
                 hold=(rc11 == 0 and "SHA256-CONTRACT: 1/1" in out11))
        pipe = self.scratch / "logs" / "synth-v1-pipe.txt"
        inode = self.field(sec_txt, "INODE")
        pipe.write_text("%s | %s | %s | %s | %s | 8 | %s\n" % (fx, inode, local, local, size, sha))
        rc12, out12 = self.verify(str(pipe), live=True)
        self.lograw("v1shape-synth-pipe.txt", out12)
        self.row("B", "synth-v1-pipe-vs-live", exit=rc12, label_defect=out12.count("LABEL-DEFECT"),
                 expect_exit=12, hold=(rc12 == 12 and out12.count("LABEL-DEFECT") >= 1 and
                                       "SHA256-CONTRACT: 1/1" in out12))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg C — label
    # -----------------------------------------------------------------------
    def leg_c_label(self):
        fx = self.scratch / "label-fixture.conf"
        fx.write_bytes(b"label fixture\n")
        os.utime(fx, (FIXTURE_EPOCH, FIXTURE_EPOCH))
        rc, txt = self.tool_cmd("capture", "--out", "-", "--paths", str(fx))
        self.lograw("label-v2-stdout.txt", txt)
        utc = self.field(txt, "MTIME_UTC_RENDER")
        loc = self.field(txt, "MTIME_LOCAL_RENDER")
        dtu = sh("date -u -d @%d '+%%Y-%%m-%%dT%%H:%%M:%%SZ'" % FIXTURE_EPOCH)[1].strip()
        ok_utc = bool(utc and utc == dtu and re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", utc))
        ok_loc = bool(loc and re.search(r"[+-]\d{2}:\d{2}$", loc))
        self.row("C", "v2-utc-render-correct", exit=rc, utc_render=utc, local_render=loc,
                 expected=dtu, hold=(rc == 0 and ok_utc and ok_loc))
        env = dict(os.environ)
        renders = {}
        for tz in ("UTC", "Asia/Tokyo", "America/St_Johns"):
            env["TZ"] = tz
            r = subprocess.run([sys.executable, str(self.tool), "capture", "--out", "-",
                                "--paths", str(fx)], capture_output=True, text=True, env=env)
            m = re.search(r"^MTIME_UTC_RENDER: (\S+)\s*$", r.stdout, re.M)
            renders[tz] = m.group(1) if m else None
        self.lograw("label-tz-renders.json", json.dumps(renders, indent=1))
        self.row("C", "v2-utc-render-tz-invariant", renders=renders,
                 hold=(len(set(renders.values())) == 1 and None not in renders.values()))
        r1 = R1 / "claims/cross/receipts/config-pre-pair.txt"
        exp = self.drift_reconcile(r1)
        rc, out = self.verify(str(r1), live=True)
        self.lograw("label-v1-declared.txt", out)
        sample = re.search(r"LABEL-DEFECT: .*", out)
        delta_ok = bool(sample and "localtime(epoch" in sample.group(0) and "gmtime(epoch) is" in sample.group(0))
        self.row("C", "v1-label-defect-declared", exit=rc, label_defect=out.count("LABEL-DEFECT"),
                 expect_labels=len(exp["label_defect"]), sample=sample.group(0) if sample else None,
                 hold=(delta_ok and out.count("LABEL-DEFECT") == len(exp["label_defect"]) and
                       rc == (10 if exp["content_drift"] else 12)))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg D — selftest (count + NAMES + missing scratch)
    # -----------------------------------------------------------------------
    def leg_d_selftest(self):
        good = self.scratch / "selftest-good"
        good.mkdir(parents=True, exist_ok=True)
        rc, out = self.tool_cmd("selftest", "--scratch", good)
        self.lograw("selftest-good.txt", out)
        m = re.search(r"CUSTODY_PAIR_SELFTEST: (\S+) cases=(\d+) passed=(\d+) failed=(\d+) exit=(\d+)", out)
        cases = int(m.group(2)) if m else None
        names = re.findall(r"^case\s+(\S+)\s+(PASS|FAIL)", out, re.M)
        name_map = {n: s for n, s in names}
        (self.scratch / "selftest-case-names.json").write_text(
            json.dumps(name_map, indent=1), encoding="utf-8")
        missing_names = [n for n in R3_CASE_NAMES if n not in name_map]
        failed_names = [n for n, s in name_map.items() if s == "FAIL"]
        exp_cases = pick(self.phase, 22, 24)
        count_hold = bool(m and m.group(1) == "CLEAN" and not failed_names and
                          (cases == 22 if self.phase == "r3" else cases >= 24))
        self.row("D", "selftest-case-count", exit=rc, cases=cases, names_found=len(name_map),
                 expect_cases=exp_cases, failed_names=failed_names,
                 summary=m.group(0) if m else None, hold=count_hold)
        # Name retention is its own row: a revision that renames a prior case keeps the
        # count while losing a declared class, and that must be visible, not absorbed.
        self.row("D", "selftest-prior-case-names-retained", prior_names_missing=missing_names,
                 names_found=len(name_map), expect="all 22 r3 case names still present",
                 hold=(not missing_names))
        missing = self.scratch / "no-such-dir-xyz" / "sub"
        rc, out = self.tool_cmd("selftest", "--scratch", missing)
        self.lograw("selftest-missing-dir.txt", out)
        tb = "Traceback (most recent call last)" in out
        self.row("D", "selftest-missing-scratch", exit=rc, traceback=tb, expect="usage2",
                 hold=(rc == 2 and not tb))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg E — D2 / guard probes
    # -----------------------------------------------------------------------
    def leg_e_holes(self):
        f = self.scratch / "eacces-file.conf"
        f.write_bytes(b"eacces probe\n")
        os.chmod(f, 0o000)
        rec = self.scratch / "logs" / "eacces-receipt.txt"
        rc_cap, cap_out = self.tool_cmd("capture", "--out", rec, "--paths", str(f))
        text = rec.read_text() if rec.exists() else ""
        rc_v, v_out = self.verify(str(rec), live=True) if rec.exists() else (None, "")
        self.lograw("eacces-capture.txt", cap_out + "\n--- receipt ---\n" + text + "\n--- verify ---\n" + v_out)
        self.row("E", "d2-eacces-capture", exit=rc_cap, receipt_exists=rec.exists(),
                 exists_no=("EXISTS: no" in text), read_error=("READ-ERROR:" in text),
                 stat_error=("STAT-ERROR:" in text),
                 verify_live_exit=rc_v,
                 verify_verdict=(re.search(r"VERDICT: (\S+)", v_out) or [None, None])[1],
                 hold=(rc_cap == 14 and "READ-ERROR:" in text and "EXISTS: yes" in text and rc_v == 14),
                 note="r3 declared: capture exit 14 + READ-ERROR; verify UNEVALUABLE 14")
        os.chmod(f, 0o644)
        fa = self.scratch / "logs" / "failopen-A.txt"
        fb = self.scratch / "logs" / "failopen-B.txt"
        stanza_text = ("PATH: %s\nEXISTS: no\nSTAT-ERROR: [Errno 13] Permission denied: '%s'\n" % (f, f))
        fa.write_text(stanza_text)
        fb.write_text(stanza_text)
        rc_fa, out_fa = self.verify(str(fa), str(fb))
        self.lograw("failopen-AB.txt", out_fa)
        self.row("E", "d2-failopen-both-absent", exit=rc_fa,
                 verdict=(re.search(r"VERDICT: (\S+)", out_fa) or [None, None])[1],
                 hold=(rc_fa == 14 and "MATCH" not in out_fa),
                 note="round-2 D2 fail-open; r3+ declared: UNEVALUABLE 14")
        f2 = self.scratch / "eacces-live.conf"
        f2.write_bytes(b"eacces live probe\n")
        rec2 = self.scratch / "logs" / "eacces-live-receipt.txt"
        self.tool_cmd("capture", "--out", rec2, "--paths", str(f2))
        os.chmod(f2, 0o000)
        rc_v2, v2_out = self.verify(str(rec2), live=True)
        tb2 = "Traceback (most recent call last)" in v2_out
        self.lograw("eacces-live.txt", v2_out)
        self.row("E", "d2-live-unreadable", exit=rc_v2, traceback=tb2,
                 hold=(rc_v2 == 14 and not tb2))
        os.chmod(f2, 0o644)
        g = self.scratch / "guard" / "target.conf"
        g.parent.mkdir(parents=True, exist_ok=True)
        g.write_bytes(b"guard probe original\n")
        before = g.read_bytes()
        rc_g, g_out = self.tool_cmd("capture", "--out", str(g), "--paths", str(g))
        after = g.read_bytes() if g.exists() else b""
        clobbered = before != after
        self.lograw("writeguard-scratch.txt", g_out + "\n--- after-bytes ---\n" + after.decode("utf-8", "replace"))
        self.row("E", "writeguard-paths-eq-out", exit=rc_g, clobbered=clobbered,
                 hold=(rc_g == 2 and not clobbered),
                 note="scratch-only probe; r3+: refused USAGE 2, not clobbered")
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg F — live pair + receipt self-pin
    # -----------------------------------------------------------------------
    def leg_f_identity(self):
        cap1 = self.scratch / "logs" / "live-pair-1.txt"
        cap2 = self.scratch / "logs" / "live-pair-2.txt"
        rc1, _ = self.tool_cmd("capture", "--out", cap1, "--label", "ex27r4-livepair-1")
        rc2, _ = self.tool_cmd("capture", "--out", cap2, "--label", "ex27r4-livepair-2")
        rc_v, out_v = self.verify(str(cap1), str(cap2))
        self.lograw("live-pair-verify.txt", out_v)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)\s+(.*?)\s+exit=(\d+)", out_v, re.M)
        self.row("F", "live-pair-capture-vs-capture", capture_exits=[rc1, rc2], exit=rc_v,
                 verdict=m.group(1) if m else None, paths=m.group(2) if m else None,
                 expect="MATCH 5/5 exit 0",
                 hold=bool(m and m.group(1) == "MATCH" and m.group(2) == "5" and rc_v == 0))
        # scratch-only live-pair form: same tool, scratch scope, no custody path read
        s1 = self.scratch / "logs" / "scratch-pair-1.txt"
        s2 = self.scratch / "logs" / "scratch-pair-2.txt"
        fx = self.scratch / "v1anchor.conf"
        self.tool_cmd("capture", "--out", s1, "--paths", str(fx))
        self.tool_cmd("capture", "--out", s2, "--paths", str(fx))
        rc_s, out_s = self.verify(str(s1), str(s2))
        self.lograw("scratch-pair-verify.txt", out_s)
        ms = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)\s+(.*?)\s+exit=(\d+)", out_s, re.M)
        self.row("F", "scratch-live-pair-form", exit=rc_s, verdict=ms.group(1) if ms else None,
                 paths=ms.group(2) if ms else None, expect="MATCH 1/1 exit 0",
                 hold=bool(ms and ms.group(1) == "MATCH" and rc_s == 0))
        pin = self.receipt_tool_pin(cap1.read_text())
        self.row("F", "receipt-self-pin", receipt_pin=(pin or "")[:12], tool_sha=self.tool_start[:12],
                 hold=(pin == self.tool_start),
                 note="receipt header must self-record the exact tool bytes")
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg I — CLI-level equivalents of the five selftest cases that the CLI can
    # reach (an in-process case can pass while the CLI path is broken: the
    # `_run_verify` kwarg defect of round 3 was exactly that shape)
    # -----------------------------------------------------------------------
    def leg_i_selftest_equivalents(self):
        d = self.scratch / "i"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        fx = d / "fixture.conf"
        payload = b"custody-pair selftest fixture\n"
        fx.write_bytes(payload)
        os.utime(fx, (1000000000, 1000000000))
        pre = d / "pre.txt"
        rc_pre, _ = self.cap(pre, fx)
        self.row("I", "eq-capture-ok", exit=rc_pre, expect=0, hold=(rc_pre == 0))

        # ctime-pin: same-content in-place write, mtime restored by hand
        mtime_ns = fx.stat().st_mtime_ns
        fx.write_bytes(payload)
        os.utime(fx, ns=(mtime_ns, mtime_ns))
        rc, out = self.verify(str(pre), live=True)
        self.lograw("eq-ctime-only.txt", out)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)", out, re.M)
        self.row("I", "eq-same-content-rewrite-inplace-ctime-pin", exit=rc,
                 verdict=m.group(1) if m else None, expect="REWRITE-DRIFT exit 11",
                 hold=(rc == 11 and bool(m) and m.group(1) == "REWRITE-DRIFT"))

        # inode-pin: same-content rewrite through a rename (fresh inode)
        fx.write_bytes(payload)
        os.utime(fx, ns=(mtime_ns, mtime_ns))
        stage = d / "stage.conf"
        stage.write_bytes(payload)
        os.utime(stage, ns=(mtime_ns, mtime_ns))
        os.replace(stage, fx)
        rc, out = self.verify(str(pre), live=True)
        self.lograw("eq-rename-inode.txt", out)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)", out, re.M)
        self.row("I", "eq-same-content-rewrite-rename-inode-pin", exit=rc,
                 verdict=m.group(1) if m else None, expect="REWRITE-DRIFT exit 11",
                 hold=(rc == 11 and bool(m) and m.group(1) == "REWRITE-DRIFT"))

        # content drift
        fx.write_bytes(b"DIFFERENT BYTES\n")
        rc, out = self.verify(str(pre), live=True)
        self.lograw("eq-content.txt", out)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)", out, re.M)
        self.row("I", "eq-content-drift", exit=rc, verdict=m.group(1) if m else None,
                 expect="CONTENT-DRIFT exit 10",
                 hold=(rc == 10 and bool(m) and m.group(1) == "CONTENT-DRIFT"))

        # metadata drift (mode only; content restored)
        fx.write_bytes(payload)
        os.utime(fx, ns=(mtime_ns, mtime_ns))
        pre2 = d / "pre2.txt"
        self.cap(pre2, fx)
        os.chmod(fx, 0o600)
        rc, out = self.verify(str(pre2), live=True)
        self.lograw("eq-metadata.txt", out)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)", out, re.M)
        self.row("I", "eq-metadata-drift", exit=rc, verdict=m.group(1) if m else None,
                 expect="METADATA-DRIFT exit 12",
                 hold=(rc == 12 and bool(m) and m.group(1) == "METADATA-DRIFT"))
        os.chmod(fx, 0o644)

        # absent
        ghost = d / "ghost.conf"
        ghost.write_bytes(b"ghost\n")
        pre3 = d / "pre3.txt"
        self.cap(pre3, ghost)
        os.unlink(ghost)
        rc, out = self.verify(str(pre3), live=True)
        self.lograw("eq-absent.txt", out)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)", out, re.M)
        self.row("I", "eq-absent", exit=rc, verdict=m.group(1) if m else None,
                 expect="ABSENT exit 13", hold=(rc == 13 and bool(m) and m.group(1) == "ABSENT"))

        # usage: unparsable reference
        bad = d / "bad.txt"
        bad.write_text("nothing to parse here\n")
        rc, out = self.verify(str(bad), live=True)
        self.lograw("eq-unparsable.txt", out)
        self.row("I", "eq-unparsable-receipt-usage", exit=rc, expect=2, hold=(rc == 2))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg J — declared-surface consistency (README vs tool)
    # -----------------------------------------------------------------------
    def leg_j_surface(self):
        """The README's exit map and the tool's exit constants must agree, and the
        README's selftest case-count sentence must match the measured case count."""
        tool_text = self.tool.read_text(encoding="utf-8", errors="replace")
        readme_text = README_WORK.read_text(encoding="utf-8", errors="replace")
        constants = {m.group(1): int(m.group(2))
                     for m in re.finditer(r"^EXIT_([A-Z_]+)\s*=\s*(\d+)\s*$", tool_text, re.M)}
        readme_rows = {int(m.group(1)) for m in
                       re.finditer(r"^\|\s*(\d+)\s*\|", readme_text, re.M)}
        declared = set(constants.values())
        missing = sorted(declared - readme_rows)
        self.row("J", "readme-exit-map-covers-tool-constants",
                 tool_constants=sorted(declared), readme_rows=sorted(readme_rows),
                 missing_in_readme=missing, expect="every declared EXIT_* present",
                 hold=(not missing))
        # exit-map row for UNEVALUABLE=14 must be present in both profiles (r3 landed it)
        self.row("J", "readme-row-14-unevaluable", has_row=(14 in readme_rows),
                 expect="present since r3", hold=(14 in readme_rows))
        # selftest case-count sentence in the README
        counts = [int(m.group(1)) for m in re.finditer(r"cases?\D{0,24}?(\d{1,3})", readme_text)]
        self.row("J", "readme-case-count-mentions", counts=counts,
                 expect=pick(self.phase, "22 named or absent", ">=24 named"),
                 hold=pick(self.phase, True, any(c >= 24 for c in counts)))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg G — the four round-3 injections (independent probes)
    # -----------------------------------------------------------------------
    def g1_sidecar_scope(self, tool=None):
        """(a) `--out X --paths X.sha256`: the derived sidecar lands on a measured file."""
        d = self.scratch / "g1"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        vic = d / "vic.sha256"                      # the file being measured
        payload = b"victim-CLOBBERED\n"
        vic.write_bytes(payload)
        out = d / "vic"                             # sidecar will be out.name + ".sha256"
        rc, txt = self.tool_cmd("capture", "--out", out, "--paths", vic, tool=tool)
        after = vic.read_bytes() if vic.exists() else b""
        clobbered = after != payload
        self.lograw("g1-sidecar-scope.txt", txt + "\n--- vic.sha256 after ---\n" + after.decode("utf-8", "replace"))
        closed = (rc == 2 and not clobbered)
        return rc, clobbered, closed

    def g1b_sidecar_hardlink(self, tool=None):
        """(a2) the sidecar path is a HARDLINK ALIAS of a measured file (inode arm).

        `--out` is a fresh file (so the existing `--out` guard cannot fire); the
        derived sidecar `out.name + '.sha256'` is a hardlink of the measured file,
        so a sidecar write reaches the measured inode without ever naming it.
        """
        d = self.scratch / "g1b"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        measured = d / "measured.sha256"
        payload = b"measured-through-sidecar-alias\n"
        measured.write_bytes(payload)
        out = d / "out.txt"                          # fresh --out: not the measured inode
        out.write_bytes(b"fresh out\n")
        os.link(measured, d / "out.txt.sha256")      # sidecar path == hardlink of measured
        rc, txt = self.tool_cmd("capture", "--out", out, "--paths", measured, tool=tool)
        after = measured.read_bytes() if measured.exists() else b""
        clobbered = after != payload
        self.lograw("g1b-sidecar-hardlink.txt", txt + "\n--- measured after ---\n" + after.decode("utf-8", "replace"))
        closed = (rc == 2 and not clobbered)
        return rc, clobbered, closed

    def g1c_control(self, tool=None):
        """control: an ordinary capture into a fresh scratch path still works."""
        d = self.scratch / "g1c"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        fx = d / "src.conf"
        fx.write_bytes(b"control fixture\n")
        out = d / "receipt.txt"
        rc, txt = self.tool_cmd("capture", "--out", out, "--paths", fx, tool=tool)
        ok = (rc == 0 and out.exists() and out.with_name("receipt.txt.sha256").exists())
        self.lograw("g1c-control.txt", txt)
        return rc, ok

    def g2_out_parent_not_dir(self, tool=None):
        """(b) `--out <regular-file>/sub/r.txt` -> declared USAGE 2, no traceback."""
        d = self.scratch / "g2"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        pfile = d / "pfile.txt"
        pfile.write_bytes(b"not a directory\n")
        out = pfile / "sub" / "r.txt"
        rc, txt = self.tool_cmd("capture", "--out", out, "--paths", pfile, tool=tool)
        tb = "Traceback (most recent call last)" in txt
        self.lograw("g2-out-parent-not-dir.txt", txt)
        closed = (rc == 2 and not tb and "USAGE" in txt)
        return rc, tb, closed

    def g2b_out_empty(self, tool=None):
        """(b2) `--out ''` (CR-4 item 6 self-refutation guard) -> USAGE 2, no traceback."""
        d = self.scratch / "g2b"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        fx = d / "src.conf"
        fx.write_bytes(b"empty-out fixture\n")
        rc, txt = self.tool_cmd("capture", "--out", "", "--paths", fx, tool=tool)
        tb = "Traceback (most recent call last)" in txt
        self.lograw("g2b-out-empty.txt", txt)
        closed = (rc == 2 and not tb)
        return rc, tb, closed

    def g3_coverage_basis(self, tool=None):
        """(c) 5x duplicate stanza for ONE path + --require-paths 5 -> must be refused."""
        d = self.scratch / "g3"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        fx = d / "one.conf"
        fx.write_bytes(b"coverage basis fixture\n")
        _, sec = self.tool_cmd("capture", "--out", "-", "--paths", fx, tool=tool)
        dupe = d / "dupe-5x.txt"
        dupe.write_text(sec * 5 if sec.strip() else "")
        rc, txt = self.tool_cmd("verify", dupe, "--live", "--require-paths", "5", tool=tool)
        line = re.search(r"REFERENCE-COVERAGE: .*", txt)
        self.lograw("g3-dupe-5x.txt", txt)
        closed = (rc == 2 and bool(line))
        return rc, line.group(0) if line else None, closed

    def g3b_coverage_distinct5(self, tool=None):
        """(c2) control: 5 DISTINCT scratch paths + --require-paths 5 -> gate passes."""
        d = self.scratch / "g3b"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        secs = []
        for i in range(5):
            f = d / f"p{i}.conf"
            f.write_bytes(b"distinct %d\n" % i)
            _, sec = self.tool_cmd("capture", "--out", "-", "--paths", f, tool=tool)
            secs.append(sec)
        ref = d / "distinct-5.txt"
        ref.write_text("".join(secs))
        rc, txt = self.tool_cmd("verify", ref, "--live", "--require-paths", "5", tool=tool)
        self.lograw("g3b-distinct-5.txt", txt)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)", txt, re.M)
        ok = (rc == 0 and bool(m) and m.group(1) == "MATCH" and m.group(2) == "5")
        return rc, m.group(0) if m else None, ok

    def g4_both_absent(self, tool=None):
        """(d) both-sides-absent semantics, both arms, measured on plain receipts."""
        d = self.scratch / "g4"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        ghost = d / "ghost.conf"                     # never created
        plain = "PATH: %s\nEXISTS: no\n" % ghost
        a, b = d / "plain-A.txt", d / "plain-B.txt"
        a.write_text(plain); b.write_text(plain)
        rc_p, out_p = self.tool_cmd("verify", a, b, tool=tool)
        self.lograw("g4-plain-both-absent.txt", out_p)
        v_p = (re.search(r"VERDICT: (\S+)", out_p) or [None, None])[1]
        err = "PATH: %s\nEXISTS: no\nSTAT-ERROR: [Errno 13] Permission denied\n" % ghost
        c, e = d / "err-A.txt", d / "err-B.txt"
        c.write_text(err); e.write_text(err)
        rc_e, out_e = self.tool_cmd("verify", c, e, tool=tool)
        self.lograw("g4-err-both-absent.txt", out_e)
        v_e = (re.search(r"VERDICT: (\S+)", out_e) or [None, None])[1]
        return (rc_p, v_p), (rc_e, v_e)

    def readme_ruling(self):
        """(d2) the README must carry the adjudication text for the both-absent semantics."""
        text = README_WORK.read_text(encoding="utf-8", errors="replace")
        hits = []
        for m in re.finditer(r"(?im)^.*(both[- ]sides|both sides).*$", text):
            hits.append(m.group(0).strip())
        for m in re.finditer(r"(?im)^.*(EXISTS: no|error-carrying|error carrying).*$", text):
            if m.group(0).strip() not in hits:
                hits.append(m.group(0).strip())
        return hits

    def leg_g_injections(self):
        # (a) sidecar scope
        rc, clob, closed = self.g1_sidecar_scope()
        self.row("G", "a-sidecar-path-of-scoped-file", exit=rc, clobbered=clob,
                 expect=pick(self.phase, "OPEN: exit 0 + clobber", "CLOSED: exit 2 + intact"),
                 hold=pick(self.phase, (rc == 0 and clob), closed))
        rc, clob, closed = self.g1b_sidecar_hardlink()
        self.row("G", "a2-sidecar-hardlink-alias", exit=rc, clobbered=clob,
                 expect=pick(self.phase, "OPEN: exit 0 + clobber", "CLOSED: exit 2 + intact"),
                 hold=pick(self.phase, (rc == 0 and clob), closed))
        rc, ok = self.g1c_control()
        self.row("G", "a3-control-ordinary-capture", exit=rc, receipt_and_sidecar_written=ok,
                 expect="exit 0", hold=ok)
        # (b) mkdir outside the guarded try
        rc, tb, closed = self.g2_out_parent_not_dir()
        self.row("G", "b-out-parent-not-a-directory", exit=rc, traceback=tb,
                 expect=pick(self.phase, "OPEN: traceback exit 1", "CLOSED: USAGE exit 2"),
                 hold=pick(self.phase, (tb and rc == 1), closed))
        rc, tb, closed = self.g2b_out_empty()
        self.row("G", "b2-out-empty-arg", exit=rc, traceback=tb,
                 expect=pick(self.phase, "USAGE exit 2", "USAGE exit 2"),
                 hold=pick(self.phase, (rc == 2 and not tb), closed))
        # (c) coverage gate basis
        rc, line, closed = self.g3_coverage_basis()
        self.row("G", "c-coverage-gate-duplicate-stanzas", exit=rc, coverage_line=line,
                 expect=pick(self.phase, "OPEN: exit 0, no line", "CLOSED: exit 2 + line"),
                 hold=pick(self.phase, (rc == 0 and line is None), closed))
        rc, verdict, ok = self.g3b_coverage_distinct5()
        self.row("G", "c2-coverage-gate-distinct-five", exit=rc, verdict=verdict,
                 expect="exit 0 MATCH 5/5", hold=ok)
        # (d) both-absent semantics
        (rc_p, v_p), (rc_e, v_e) = self.g4_both_absent()
        self.row("G", "d-both-absent-plain", exit=rc_p, verdict=v_p,
                 expect="MATCH exit 0 (declared design: only error-carrying stanzas are UNEVALUABLE)",
                 hold=(rc_p == 0 and v_p == "MATCH"))
        self.row("G", "d2-both-absent-error-carrying", exit=rc_e, verdict=v_e,
                 expect="UNEVALUABLE exit 14", hold=(rc_e == 14 and v_e == "UNEVALUABLE"))
        ruling = self.readme_ruling()
        self.row("G", "d3-readme-ruling-text", hits=len(ruling), excerpt=(ruling[0] if ruling else None),
                 expect=pick(self.phase, "OPEN: no ruling text", "CLOSED: ruling text present"),
                 hold=pick(self.phase, not ruling, bool(ruling)))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg H — sabotage / non-vacuity arms
    # -----------------------------------------------------------------------
    def sabotage_copy(self, pattern, repl, tag):
        """Byte-sabotage a copy of the tool under test; returns (path, applied) or (None, reason).

        `pattern` may be a single regex or a list of alternatives (first match wins) —
        the r4 revision's exact guard spelling is EX-21's choice, so the arm declares a
        family of shapes rather than one guessed line.

        A sabotage copy that does not even parse is NOT a valid non-vacuity arm: a
        SyntaxError proves nothing about the check under test. Every sabotage copy is
        therefore compile-checked; an uncompilable result is reported as an observed-only
        row (reason recorded), never as a passing arm.
        """
        src = self.tool.read_text(encoding="utf-8")
        patterns = pattern if isinstance(pattern, list) else [pattern]
        for pat in patterns:
            new, n = re.subn(pat, repl, src)
            if n:
                break
        else:
            return None, "no pattern matched: %s" % " | ".join(patterns)
        out = self.scratch / "sabotage" / ("%s.py" % tag)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(new, encoding="utf-8")
        out.chmod(0o755)
        try:
            compile(new, str(out), "exec")
        except SyntaxError as exc:
            return None, "sabotage copy does not compile (%s) — arm invalid" % exc
        return out, "applied %d substitution(s)" % n

    def sabotage_body(self, tag, pattern, repl, probe, expect_red_when, note):
        """Apply a sabotage edit, run `probe(tool)`, and require the check to go RED.

        `expect_red_when(result)` returns True when the check reads CLOSED; the arm holds
        when the sabotaged copy makes it read OPEN (i.e. the check is non-vacuous).
        """
        sab, why = self.sabotage_copy(pattern, repl, tag)
        if sab is None:
            self.row("H", "sabotage-%s" % tag, sabotage=why, hold=None, note=note)
            return
        result = probe(sab)
        red = not expect_red_when(result)
        self.row("H", "sabotage-%s" % tag, sabotage=why, probe_result=repr(result),
                 check_goes_red=red, hold=bool(red), note=note)

    def leg_h_sabotage(self):
        b = self.baseline_tool
        if b.exists():
            rc, clob, closed = self.g1_sidecar_scope(tool=b)
            self.row("H", "nonvacuity-baseline-sidecar", tool_sha=self.baseline_sha[:12], exit=rc,
                     clobbered=clob, check_says_closed=closed,
                     hold=(not closed and rc == 0 and clob))
            rc, line, closed = self.g3_coverage_basis(tool=b)
            self.row("H", "nonvacuity-baseline-coverage", tool_sha=self.baseline_sha[:12], exit=rc,
                     check_says_closed=closed, hold=(not closed))
            rc, tb, closed = self.g2_out_parent_not_dir(tool=b)
            self.row("H", "nonvacuity-baseline-mkdir", tool_sha=self.baseline_sha[:12], exit=rc,
                     traceback=tb, check_says_closed=closed, hold=(not closed))
        else:
            self.row("H", "nonvacuity-baseline", hold=None, note="baseline copy absent")
        if self.phase != "r4":
            self.tool_check()
            return
        # H2: targeted sabotage of the revision under test. Shape-dependent: each arm
        # declares a FAMILY of patterns; an unmatched family is an observed-only row,
        # not a pass.
        sidecar_family = [
            r"candidates = \(\(out, out\.resolve\(\)\), \(sidecar, sidecar\.resolve\(\)\)\)",
            r"for cand in \(out, out\.with_name\(out\.name \+ \"\.sha256\"\)\):",
            r"candidate_paths = \(out, out\.with_name\(out\.name \+ \"\.sha256\"\)\)",
            r"candidate_paths = \(out, sidecar\)",
            r"for cand in \(out, sidecar\):",
            r"guarded_paths = \(out, sidecar\)",
        ]
        sidecar_alias_family = [
            r"candidates = \(\(out, out\.resolve\(\)\), \(sidecar, sidecar\.resolve\(\)\)\)",
            r"candidate_paths = \(out, out\.with_name\(out\.name \+ \"\.sha256\"\)\)",
            r"candidate_paths = \(out, sidecar\)",
            r"for cand in \(out, sidecar\):",
            r"guarded_paths = \(out, sidecar\)",
        ]
        # (a) sidecar arm removed — probe g1 (the direct clobber)
        self.sabotage_body(
            "sidecar-arm-removed", sidecar_family,
            "candidates = ((out, out.resolve()),)",
            lambda t: self.g1_sidecar_scope(tool=t),
            lambda r: r[2],
            "(a) removing the sidecar candidate from the guard must turn the direct "
            "clobber check RED")
        # (a2) sidecar arm removed — probe g1b (the alias clobber, inode arm)
        self.sabotage_body(
            "sidecar-alias-arm-removed", sidecar_alias_family,
            "candidates = ((out, out.resolve()),)",
            lambda t: self.g1b_sidecar_hardlink(tool=t),
            lambda r: r[2],
            "(a2) removing the sidecar candidate must turn the alias clobber check RED")
        # (c) coverage basis reverted to stanza multiplicity
        self.sabotage_body(
            "coverage-basis-reverted",
            [r"return len\(have\) >= required, line",
             r"return len\(have\) >= required"],
            "return len(ref_sections) >= required, line",
            lambda t: self.g3_coverage_basis(tool=t),
            lambda r: r[2],
            "(c) reverting the basis to stanza count must turn the duplicate-stanza "
            "gate check RED")
        # (d) UNEVALUABLE arm removed -> the fail-closed check must go RED
        self.sabotage_body(
            "unevaluable-arm-removed",
            [r"if ref_uneval or cand_uneval:"],
            "if False:",
            lambda t: self.g4_both_absent(tool=t),
            lambda r: (r[1][0] == 14 and r[1][1] == "UNEVALUABLE"),
            "(d) removing the UNEVALUABLE arm must turn the error-carrying both-absent "
            "check RED")
        self.tool_check()

    def run(self):
        s = {"A": self.leg_a_matrix()}
        self.leg_b_v1shapes()
        self.leg_c_label()
        self.leg_d_selftest()
        self.leg_e_holes()
        self.leg_f_identity()
        self.leg_g_injections()
        self.leg_i_selftest_equivalents()
        self.leg_j_surface()
        self.leg_h_sabotage()
        self.tool_check()
        return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("r3", "r4"), required=True)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--tool-src", default=None, help="tool path to run (default: working tree)")
    ap.add_argument("--baseline-src", default=None, help="pre-revision tool copy for the sabotage leg")
    a = ap.parse_args()
    tool_path = Path(a.tool_src) if a.tool_src else TOOL_WORK
    sha = sha256_file(tool_path)
    tag = a.tag or (a.phase + "-" + sha[:12])
    outdir = ROOT / "runs" / tag
    outdir.mkdir(parents=True, exist_ok=True)
    run_tool = outdir / "tool-under-test" / "custody-pair.py"
    run_tool.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(tool_path, run_tool)
    run_tool.chmod(0o755)
    if sha256_file(run_tool) != sha:
        raise SystemExit("copy drift")
    baseline = Path(a.baseline_src) if a.baseline_src else (outdir / "baseline-tool" / "custody-pair.py")
    if baseline.exists() and baseline.resolve() != run_tool.resolve():
        bcopy = outdir / "baseline-tool" / "custody-pair.py"
        if baseline.resolve() != bcopy.resolve():
            bcopy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(baseline, bcopy)
            bcopy.chmod(0o755)
            baseline = bcopy
    b = Battery(a.phase, outdir / "scratch", run_tool, baseline)
    t0 = time.time()
    summary = b.run()
    took = time.time() - t0
    result = {
        "seat": "EX-27", "chain": "c3", "phase": a.phase, "tag": tag,
        "tool_src": str(tool_path), "tool_sha": sha,
        "tool_sha_realpath": sha256_file(TOOL_WORK) if TOOL_WORK.exists() else None,
        "readme_sha_realpath": sha256_file(README_WORK) if README_WORK.exists() else None,
        "baseline_sha": b.baseline_sha,
        "host": {"kernel": sh("uname -r")[1].strip(), "tz": sh("date +%z")[1].strip(),
                 "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
        "took_s": round(took, 1), "summary": summary, "rows": b.rows,
    }
    holds = [r for r in b.rows if r.get("hold") is True]
    fails = [r for r in b.rows if r.get("hold") is False]
    na = [r for r in b.rows if r.get("hold") is None]
    result["tally"] = {"rows": len(b.rows), "hold": len(holds), "fail": len(fails), "observed": len(na)}
    (outdir / "regress.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    lines = ["EX-27 round-4 regression battery — phase=%s tool=%s (realpath %s)" % (
                 a.phase, sha, result["tool_sha_realpath"]),
             "baseline=%s  host %s tz %s at %s; took %.1fs" % (
                 b.baseline_sha, result["host"]["kernel"], result["host"]["tz"],
                 result["host"]["utc"], took),
             "tally rows=%d hold=%d fail=%d observed-only=%d" % (
                 result["tally"]["rows"], result["tally"]["hold"], result["tally"]["fail"],
                 result["tally"]["observed"]), ""]
    for r in b.rows:
        st = {True: "HOLD", False: "FAIL", None: "obs "}[r.get("hold")]
        keys = " ".join("%s=%s" % (k, v) for k, v in r.items()
                        if k not in ("leg", "name", "hold", "note") and v not in (None,))
        lines.append("[%s] %s/%s %s" % (st, r["leg"], r["name"], keys))
    (outdir / "regress.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("\nwrote %s/regress.json" % outdir)


if __name__ == "__main__":
    main()
