#!/usr/bin/env python3
"""EX-27 regression battery — re-run the round-2 attack matrix on the (revised) custody tool.

Seat EX-27, chain c2, wave arc3-loop1-round3, 2026-10-19.
READ-ONLY over every custody path. Scratch under /var/tmp/ex27-r3. /tmp untouched.

The tool under test is either the working-tree path or a pinned scratch copy
(--tool-src); its sha256 is recorded before/after every leg and any movement
aborts the run (identity discipline, rule #14). Receipts self-record the tool sha
(`# tool:` header) and the harness cross-checks that line against the pinned bytes.

Legs
  A  matrix13   — the 13 CR-4/battery.py rewrite forms, driven through the REAL tool
                  (+ same-content variants, chmod-only, delete-after-capture).
  B  v1shapes   — round-1 canonical stanza / pipe sidecar / sums (drift-aware), the
                  EX-35 fixtures, synthetic v1 anchors (stanza/sums/pipe on scratch).
  C  label      — v1 label defect declared (wording + delta), v2 UTC render correct + TZ-invariant.
  D  selftest   — case count + missing-scratch-dir behaviour.
  E  holes      — D2 EACCES probes, write-guard scope probe (scratch only).
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
R2 = REPO / ".ufo/waves/arc3-loop1-round2"
R1 = REPO / ".ufo/waves/arc3-loop1-round1"
ROOT = Path("/var/tmp/ex27-r3")

ORIG = b'{"mcp": {"servers": {"alpha": {"cmd": "a"}}}}\n'
MAL = b'{"mcp": {"servers": {"alpha": {"cmd": "EVIL"}}}}\n'
FIXTURE_EPOCH = 1792011200  # 2026-10-14T20:53:20Z, the round-1 defect epoch

PHASE_EXPECT = {
    "baseline": {"partial_default_exit": 0, "selftest_cases": 15, "scratch_missing": "traceback"},
    "revised": {"partial_default_exit": None, "selftest_cases": ">=17", "scratch_missing": "usage2"},
}

# expected verdict classes for leg A (content-state driven; round-2 record)
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


class Battery:
    def __init__(self, phase, scratch, tool_path):
        self.phase = phase
        self.scratch = Path(scratch)
        self.tool = Path(tool_path)
        self.raw = self.scratch / "raw"
        self.raw.mkdir(parents=True, exist_ok=True)
        self.rows = []
        self.tool_start = sha256_file(self.tool)

    # ---- helpers ----------------------------------------------------------
    def row(self, leg, name, **kw):
        kw.update({"leg": leg, "name": name})
        self.rows.append(kw)
        return kw

    def lograw(self, name, text):
        (self.raw / name).write_text(text, encoding="utf-8")

    def tool_cmd(self, *args):
        rc, out = sh([sys.executable, str(self.tool)] + [str(a) for a in args])
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
    # Leg A — attack matrix
    # -----------------------------------------------------------------------
    def fresh(self, name):
        d = self.scratch / "bench" / name
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        p = d / "target.json"
        p.write_bytes(ORIG)
        os.utime(p, (FIXTURE_EPOCH, FIXTURE_EPOCH))
        # battery.py layout, verbatim: backup.json (copystat of p), pristine.json, srcdir/dstdir, backup.tar
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
        def A9(d, p):  # battery.py verbatim: restore WITHOUT truncate -> trailing bytes
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.flush(); os.fsync(f.fileno())
            return 0, "in-place rewrite then original bytes re-written (no truncate; battery.py verbatim)"
        def A10(d, p):  # battery.py verbatim
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.flush(); os.fsync(f.fileno())
            sh(f"touch -r {d}/backup.json {p}")
            return 0, "restore bytes (no truncate) + touch -r backup (mtime/atime restored)"
        def A11(d, p):  # battery.py verbatim
            sh(f"ln {p} {d}/alias")
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            with open(p, "r+b") as f:
                f.write(ORIG); f.flush(); os.fsync(f.fileno())
            sh(f"touch -r {d}/backup.json {p}")
            return 0, f"hardlink alias {d}/alias; in-place modify+restore (no truncate); touch -r"
        def A12(d, p): return sh(f"cp --reflink=always {d}/backup.json {p}")
        def A13(d, p):  # battery.py verbatim
            sh(f"ln {p} {d}/pristine_link")
            with open(p, "r+b") as f:
                f.write(MAL); f.truncate(); f.flush(); os.fsync(f.fileno())
            sh(f"mv -f {d}/pristine_link {p}")
            sh(f"touch -r {d}/backup.json {p}")
            return 0, "hardlink swap-back (same inode; battery.py verbatim)"
        # same-content variants (EX-33 ladder classes: R-B, R-B2, hardlink alias)
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
        """Fresh per-path live capture (scratch receipt) -> {path: section-text}."""
        r1 = R1 / "claims/cross/receipts/config-pre-pair.txt"
        rc, out = self.tool_cmd("capture", "--out", "-", "--label", tag)
        self.lograw(f"live-capture-{tag}.txt", out)
        secs = {}
        for part in re.split(r"^PATH: ", out, flags=re.M)[1:]:
            lines = part.split("\n", 1)
            secs[lines[0].strip()] = lines[1] if len(lines) > 1 else ""
        return secs

    def drift_reconcile(self, ref_receipt):
        """Independent per-path expectation for a v1 reference vs live."""
        text = ref_receipt.read_text()
        ref = {}
        for part in re.split(r"^PATH: ", text, flags=re.M)[1:]:
            lines = part.split("\n", 1)
            p = lines[0].strip()
            body = lines[1] if len(lines) > 1 else ""
            mv = re.search(r"^MTIME_UTC:\s*(.+?)\s*$", body, re.M)
            ref[p] = {
                "sha": self.field(body, "SHA256"),
                "mtime_v1": mv.group(1) if mv else None,
            }
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

        # independent drift expectation, recomputed at run time
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
        # B2 cross-format: v1 stanza vs fresh v2 capture of the 5 real paths
        v2cap = self.scratch / "logs" / "custody-live-v2.txt"
        self.tool_cmd("capture", "--out", v2cap, "--label", "ex27-b2")
        rc2, out2 = self.verify(str(r1), str(v2cap))
        self.lograw("v1shape-crossformat.txt", out2)
        n2 = out2.count("LABEL-DEFECT")
        m2 = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out2)
        hold2 = (rc2 == exp_exit and (int(m2.group(1)) if m2 else None) == exp["sha_agree"] and n2 >= len(exp["label_defect"]))
        self.row("B", "r1-canonical-vs-fresh-v2", exit=rc2,
                 sha_agree=int(m2.group(1)) if m2 else None, label_defect=n2,
                 expect_exit=exp_exit, expect_sha_agree=exp["sha_agree"], hold=bool(hold2))
        # B3 round-1 pipe sidecar (time labels on both clocks)
        rc3, out3 = self.verify(str(r1_meta), live=True)
        self.lograw("v1shape-pipe.txt", out3)
        m3 = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out3)
        hold3 = (rc3 == exp_exit and (int(m3.group(1)) if m3 else None) == exp["sha_agree"])
        self.row("B", "r1-metadata-pipe-vs-live", exit=rc3,
                 sha_agree=int(m3.group(1)) if m3 else None, label_defect=out3.count("LABEL-DEFECT"),
                 expect_exit=exp_exit, expect_sha_agree=exp["sha_agree"], hold=bool(hold3))
        # B4 round-1 sums (sha-only, no labels)
        rc4, out4 = self.verify(str(r1_sums), live=True)
        self.lograw("v1shape-sums.txt", out4)
        m4 = re.search(r"SHA256-CONTRACT: (\d+)/(\d+)", out4)
        hold4 = ((int(m4.group(1)) if m4 else None) == exp["sha_agree"] and
                 rc4 == (10 if ndrift else 0))
        self.row("B", "r1-sums-vs-live", exit=rc4, sha_agree=int(m4.group(1)) if m4 else None,
                 expect_exit=(10 if ndrift else 0), hold=bool(hold4))
        # B5 EX-35 partial 1-of-5 (the D3 shape)
        p5 = ex35 / "v1-partial-1of5.txt"
        rc5, out5 = self.verify(str(p5), live=True)
        self.lograw("v1shape-partial-default.txt", out5)
        rc5r, out5r = self.verify(str(p5), live=True, extra=("--require-paths", "5"))
        self.lograw("v1shape-partial-require5.txt", out5r)
        exp_default = PHASE_EXPECT[self.phase]["partial_default_exit"]
        r5_supported = "REFERENCE-COVERAGE" in out5r
        hold5 = (rc5 == exp_default) if exp_default is not None else (rc5 != 0 or (r5_supported and rc5r == 2))
        self.row("B", "ex35-partial-1of5-default", exit=rc5, require5_exit=rc5r,
                 require5_supported=r5_supported, expect_default=exp_default, hold=bool(hold5))
        # B6/B7/B8 fixtures with fixed classes (drift-aware: round-2 base counts minus live drift)
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
        # B9 junk receipt
        junk = self.scratch / "logs" / "junk.txt"
        junk.write_text("not a receipt at all\n")
        rc9, out9 = self.verify(str(junk), live=True)
        self.lograw("v1shape-junk.txt", out9)
        self.row("B", "junk-receipt", exit=rc9, expect_exit=2, hold=(rc9 == 2))
        # B10-B12 synthetic v1 anchors on a scratch fixture (drift-free)
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
        # v1 defect declared (count + wording + delta); drift-aware count
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
    # Leg D — selftest
    # -----------------------------------------------------------------------
    def leg_d_selftest(self):
        good = self.scratch / "selftest-good"
        good.mkdir(parents=True, exist_ok=True)
        rc, out = self.tool_cmd("selftest", "--scratch", good)
        self.lograw("selftest-good.txt", out)
        m = re.search(r"CUSTODY_PAIR_SELFTEST: (\S+) cases=(\d+) passed=(\d+) failed=(\d+) exit=(\d+)", out)
        cases = int(m.group(2)) if m else None
        exp = PHASE_EXPECT[self.phase]["selftest_cases"]
        if exp == ">=17":
            hold = bool(m and m.group(1) == "CLEAN" and cases >= 17 and int(m.group(5)) == 0)
        else:
            hold = bool(m and m.group(1) == "CLEAN" and cases == exp and int(m.group(5)) == 0)
        self.row("D", "selftest-existing-scratch", exit=rc, cases=cases,
                 summary=m.group(0) if m else None, expect_cases=exp, hold=hold)
        missing = self.scratch / "no-such-dir-xyz" / "sub"
        rc, out = self.tool_cmd("selftest", "--scratch", missing)
        self.lograw("selftest-missing-dir.txt", out)
        tb = "Traceback (most recent call last)" in out
        exp_kind = PHASE_EXPECT[self.phase]["scratch_missing"]
        hold = (tb and rc == 1) if exp_kind == "traceback" else (rc == 2 and not tb)
        self.row("D", "selftest-missing-scratch", exit=rc, traceback=tb, expect=exp_kind, hold=bool(hold))
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg E — hole probes (record-only; the implementer owns the fix)
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
        if self.phase == "revised":
            hold_cap = (rc_cap == 14 and "READ-ERROR:" in text and "EXISTS: yes" in text
                        and rc_v == 14)
        else:
            hold_cap = None
        self.row("E", "d2-eacces-capture", exit=rc_cap, receipt_exists=rec.exists(),
                 exists_no=("EXISTS: no" in text), read_error=("READ-ERROR:" in text),
                 stat_error=("STAT-ERROR:" in text),
                 verify_live_exit=rc_v, verify_verdict=(re.search(r"VERDICT: (\S+)", v_out) or [None, None])[1],
                 hold=hold_cap, note="round-2: exists=no + STAT-ERROR + fail-open MATCH; revised: exit 14 + UNEVALUABLE")
        os.chmod(f, 0o644)
        # E1b: the fail-open shape — receipts that record exists=no + STAT-ERROR on both sides
        fa = self.scratch / "logs" / "failopen-A.txt"
        fb = self.scratch / "logs" / "failopen-B.txt"
        stanza_text = ("PATH: %s\nEXISTS: no\nSTAT-ERROR: [Errno 13] Permission denied: '%s'\n" % (f, f))
        fa.write_text(stanza_text)
        fb.write_text(stanza_text)
        rc_fa, out_fa = self.verify(str(fa), str(fb))
        self.lograw("failopen-AB.txt", out_fa)
        self.row("E", "d2-failopen-both-absent", exit=rc_fa,
                 verdict=(re.search(r"VERDICT: (\S+)", out_fa) or [None, None])[1],
                 hold=((rc_fa == 14 and "MATCH" not in out_fa) if self.phase == "revised" else None),
                 note="round-2 D2: both-sides absent verifies MATCH exit 0 (fail-open); revised: UNEVALUABLE 14")
        f2 = self.scratch / "eacces-live.conf"
        f2.write_bytes(b"eacces live probe\n")
        rec2 = self.scratch / "logs" / "eacces-live-receipt.txt"
        self.tool_cmd("capture", "--out", rec2, "--paths", str(f2))
        os.chmod(f2, 0o000)
        rc_v2, v2_out = self.verify(str(rec2), live=True)
        tb2 = "Traceback (most recent call last)" in v2_out
        self.lograw("eacces-live.txt", v2_out)
        self.row("E", "d2-live-unreadable", exit=rc_v2, traceback=tb2,
                 hold=((rc_v2 == 14 and not tb2) if self.phase == "revised" else None),
                 note="round-2: raw traceback; revised: declared class")
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
                 hold=((rc_g == 2 and not clobbered) if self.phase == "revised" else None),
                 note="scratch-only probe; revised: refused USAGE 2, not clobbered")
        self.tool_check()

    # -----------------------------------------------------------------------
    # Leg F — live pair self-consistency + receipt self-pin (identity discipline)
    # -----------------------------------------------------------------------
    def leg_f_identity(self):
        cap1 = self.scratch / "logs" / "live-pair-1.txt"
        cap2 = self.scratch / "logs" / "live-pair-2.txt"
        rc1, _ = self.tool_cmd("capture", "--out", cap1, "--label", "ex27-livepair-1")
        rc2, _ = self.tool_cmd("capture", "--out", cap2, "--label", "ex27-livepair-2")
        rc_v, out_v = self.verify(str(cap1), str(cap2))
        self.lograw("live-pair-verify.txt", out_v)
        m = re.search(r"^VERDICT: (\S+)\s+paths=(\d+)\s+(.*?)\s+exit=(\d+)", out_v, re.M)
        self.row("F", "live-pair-capture-vs-capture", capture_exits=[rc1, rc2], exit=rc_v,
                 verdict=m.group(1) if m else None, paths=m.group(2) if m else None,
                 expect="MATCH 5/5 exit 0", hold=bool(m and m.group(1) == "MATCH" and rc_v == 0))
        pin = self.receipt_tool_pin(cap1.read_text())
        self.row("F", "receipt-self-pin", receipt_pin=(pin or "")[:12], tool_sha=self.tool_start[:12],
                 hold=(pin == self.tool_start), note="receipt header must self-record the exact tool bytes")
        self.tool_check()

    def run(self):
        s = {"A": self.leg_a_matrix()}
        self.leg_b_v1shapes()
        self.leg_c_label()
        self.leg_d_selftest()
        self.leg_e_holes()
        self.leg_f_identity()
        self.tool_check()
        return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=("baseline", "revised"), required=True)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--tool-src", default=None, help="tool path to run (default: working tree)")
    a = ap.parse_args()
    tool_path = Path(a.tool_src) if a.tool_src else TOOL_WORK
    sha = sha256_file(tool_path)
    tag = a.tag or (a.phase + "-" + sha[:12])
    outdir = ROOT / "runs" / tag
    outdir.mkdir(parents=True, exist_ok=True)
    # always run --tool-src copies via a stable basename (selftest re-invokes __file__)
    run_tool = outdir / "tool-under-test" / "custody-pair.py"
    run_tool.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(tool_path, run_tool)
    run_tool.chmod(0o755)
    if sha256_file(run_tool) != sha:
        raise SystemExit("copy drift")
    b = Battery(a.phase, outdir / "scratch", run_tool)
    t0 = time.time()
    summary = b.run()
    took = time.time() - t0
    result = {
        "seat": "EX-27", "phase": a.phase, "tag": tag,
        "tool_src": str(tool_path), "tool_sha": sha,
        "tool_sha_realpath": sha256_file(TOOL_WORK),
        "host": {"kernel": sh("uname -r")[1].strip(), "tz": sh("date +%z")[1].strip(),
                 "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
        "took_s": round(took, 1), "summary": summary, "rows": b.rows,
    }
    holds = [r for r in b.rows if r.get("hold") is True]
    fails = [r for r in b.rows if r.get("hold") is False]
    na = [r for r in b.rows if r.get("hold") is None]
    result["tally"] = {"rows": len(b.rows), "hold": len(holds), "fail": len(fails), "observed": len(na)}
    (outdir / "regress.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    lines = ["EX-27 regression battery — phase=%s tool=%s (realpath %s)" % (a.phase, sha, result["tool_sha_realpath"]),
             "host %s tz %s at %s; took %.1fs" % (result["host"]["kernel"], result["host"]["tz"],
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