#!/usr/bin/env python3
"""CR-3 (arc3-loop1-round3, chain c2) — type-swap matrix around the EACCES class.

Runs the LANDED custody-pair.py (byte-identical copy) against scratch fixtures:
  A. broken symlink (dangling, loop, referent-drift, file->symlink swap)
  B. directory at path (content change, subdir blind spot, dir->file swap, fifo)
  C. chmod-000 (dir component, file, --out parent, selftest scratch, receipts)
Every case prints rc + stdout + stderr verbatim. Scratch: /var/tmp/cr3/work only.
"""
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
SRC = Path(os.environ.get("CR3_SRC",
                          str(REPO / ".ufo/gates/custody-pair/custody-pair.py")))
BASE = Path("/var/tmp/cr3/work")
TOOLDIR = BASE / "tool"
TOOL = TOOLDIR / "custody-pair.py"
FIX = BASE / "fix"
REC = BASE / "rec"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def setup():
    if BASE.exists():
        for dirpath, dirnames, filenames in os.walk(BASE):
            for d in dirnames:
                try:
                    os.chmod(os.path.join(dirpath, d), 0o755)
                except OSError:
                    pass
            for f in filenames:
                try:
                    os.chmod(os.path.join(dirpath, f), 0o644)
                except OSError:
                    pass
        shutil.rmtree(BASE)
    TOOLDIR.mkdir(parents=True)
    FIX.mkdir(parents=True)
    REC.mkdir(parents=True)
    (BASE / "tmp").mkdir(exist_ok=True)
    (BASE / "scratch").mkdir(exist_ok=True)
    shutil.copy2(SRC, TOOL)

    assert sha(TOOL) == sha(SRC), "tool copy is not byte-identical"
    print("# tool copy sha256 %s == landed revision" % sha(TOOL))

    # A fixtures
    (FIX / "regularfile").write_bytes(b"regular content v1\n")
    os.utime(FIX / "regularfile", (1000000000, 1000000000))
    (FIX / "dangling").symlink_to("missing-target")
    (FIX / "dangling2").symlink_to("made-later")
    (FIX / "loopb").symlink_to("loopa")
    (FIX / "loopa").symlink_to("loopb")
    (FIX / "mutable.conf").write_bytes(b"referent v1\n")
    (FIX / "linkmutable").symlink_to("mutable.conf")
    (FIX / "psym").symlink_to("blocked/target")  # referent under a 000 dir

    # B fixtures
    for name in ("dirA", "dirB", "dirC"):
        (FIX / name / "sub").mkdir(parents=True)
        (FIX / name / "sub" / "inner.txt").write_bytes(b"inner\n")
    os.mkfifo(FIX / "fifo")
    (FIX / "outdir").mkdir()

    # C fixtures
    (FIX / "blocked").mkdir()
    (FIX / "blocked" / "inner.txt").write_bytes(b"blocked inner\n")
    (FIX / "secretfile").write_bytes(b"secret v1\n")
    (FIX / "secretreceipt.txt").write_text("PATH: /x\nEXISTS: no\n", encoding="utf-8")
    (FIX / "blockedrec").mkdir()
    (FIX / "blockedrec" / "r.txt").write_text(
        "PATH: /x\nEXISTS: no\n", encoding="utf-8")
    (FIX / "pfile.txt").write_bytes(b"i am a file, not a dir\n")
    (FIX / "plainfile").write_bytes(b"plain v1\n")


def run(args, cwd=BASE, timeout=30, env_extra=None):
    env = dict(os.environ)
    env["TMPDIR"] = str(BASE / "tmp")
    env["CUSTODY_PAIR_SCRATCH"] = str(BASE / "scratch")
    if env_extra:
        env.update(env_extra)
    try:
        p = subprocess.run([sys.executable, str(TOOL)] + args, cwd=str(cwd),
                           capture_output=True, text=True, timeout=timeout, env=env)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return "TIMEOUT", (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "TIMEOUT after %ss" % timeout


def case(name, args, cwd=BASE, timeout=30, note="", receipt=None):
    rc, out, err = run(args, cwd, timeout)
    print("=" * 78)
    print("CASE %s%s" % (name, ("  | " + note) if note else ""))
    print("$ custody-pair.py %s" % " ".join(args))
    print("rc=%s" % rc)
    if out:
        print(out.rstrip())
    if err:
        print("-- stderr --")
        print(err.rstrip())
    if receipt is not None:
        rp = Path(receipt) if str(receipt).startswith("/") else BASE / receipt
        print("-- receipt %s exists=%s --" % (rp, rp.exists()))
        if rp.exists():
            print(rp.read_text(encoding="utf-8").rstrip())
    sys.stdout.flush()
    return rc, out, err


def main():
    setup()
    print("# host: uid=%d  python=%s" % (os.getuid(), sys.version.split()[0]))
    print("# fixtures under %s ; receipts under %s" % (FIX, REC))

    case("C0-selftest-baseline", ["selftest", "--scratch", str(BASE / "scratch")],
         note="must be CLEAN 15/15")

    # ---------------- A: broken symlink ----------------
    case("A1-capture-dangling", ["capture", "--out", str(REC / "dangling-pre.txt"),
                                 "--paths", str(FIX / "dangling")],
         note="dangling symlink capture", receipt=REC / "dangling-pre.txt")
    case("A2-verify-dangling-live", ["verify", str(REC / "dangling-pre.txt"), "--live"],
         note="unchanged dangling symlink vs live")
    (FIX / "dangling").unlink()
    (FIX / "dangling").symlink_to("other-target")
    case("A3-retarget-dangling", ["verify", str(REC / "dangling-pre.txt"), "--live"],
         note="symlink retargeted to a different (also missing) target")
    (FIX / "dangling").unlink()
    (FIX / "dangling").symlink_to("missing-target")
    case("A4a-capture-dangling2", ["capture", "--out", str(REC / "dangling2-pre.txt"),
                                   "--paths", str(FIX / "dangling2")])
    (FIX / "made-later").write_bytes(b"i now exist\n")
    case("A4b-referent-materialized", ["verify", str(REC / "dangling2-pre.txt"), "--live"],
         note="referent created: symlink itself untouched")
    case("A5a-capture-live-symlink", ["capture", "--out", str(REC / "linkmutable-pre.txt"),
                                      "--paths", str(FIX / "linkmutable")])
    (FIX / "mutable.conf").write_bytes(b"referent v2 CHANGED\n")
    case("A5b-referent-drift", ["verify", str(REC / "linkmutable-pre.txt"), "--live"],
         note="referent content changed; symlink untouched")
    case("A6-capture-symlink-loop", ["capture", "--out", str(REC / "loop-pre.txt"),
                                     "--paths", str(FIX / "loopa")],
         timeout=15, note="symlink loop; must not hang")
    case("A6b-verify-symlink-loop", ["verify", str(REC / "loop-pre.txt"), "--live"], timeout=15)
    case("A7a-capture-regularfile", ["capture", "--out", str(REC / "file-pre.txt"),
                                     "--paths", str(FIX / "regularfile")])
    (FIX / "regularfile").unlink()
    (FIX / "regularfile").symlink_to("some-target")
    case("A7b-file-swapped-to-symlink", ["verify", str(REC / "file-pre.txt"), "--live"],
         note="type swap file -> symlink")

    # ---------------- B: directory at path ----------------
    case("B1-capture-dir", ["capture", "--out", str(REC / "dirA-pre.txt"),
                            "--paths", str(FIX / "dirA")],
         note="directory at path", receipt=REC / "dirA-pre.txt")
    case("B2-verify-dir-live-clean", ["verify", str(REC / "dirA-pre.txt"), "--live"],
         note="clean directory vs live")
    st_before = os.lstat(FIX / "dirA")
    (FIX / "dirA" / "newfile.txt").write_bytes(b"added\n")
    os.utime(FIX / "dirA", ns=(st_before.st_mtime_ns, st_before.st_mtime_ns))
    case("B3-dir-entry-added-mtime-restored", ["verify", str(REC / "dirA-pre.txt"), "--live"],
         note="entry added to captured dir; dir mtime restored via utime")
    case("B4a-capture-dirB", ["capture", "--out", str(REC / "dirB-pre.txt"),
                              "--paths", str(FIX / "dirB")])
    (FIX / "dirB" / "sub" / "inner2.txt").write_bytes(b"deep add\n")
    case("B4b-subdir-entry-added", ["verify", str(REC / "dirB-pre.txt"), "--live"],
         note="entry added inside captured/sub/ : top-level stat untouched?")
    case("B5a-capture-dirC", ["capture", "--out", str(REC / "dirC-pre.txt"),
                              "--paths", str(FIX / "dirC")])
    shutil.rmtree(FIX / "dirC")
    (FIX / "dirC").write_bytes(b"now a file\n")
    case("B5b-dir-swapped-to-file", ["verify", str(REC / "dirC-pre.txt"), "--live"],
         note="type swap directory -> file")
    case("B6a-capture-fifo", ["capture", "--out", str(REC / "fifo-pre.txt"),
                              "--paths", str(FIX / "fifo")], timeout=15,
         note="fifo at path; must not hang")
    case("B6b-verify-fifo-live", ["verify", str(REC / "fifo-pre.txt"), "--live"], timeout=15)
    case("B7-out-is-directory", ["capture", "--out", str(FIX / "outdir"),
                                 "--paths", str(FIX / "plainfile")],
         note="write target is a directory")

    # ---------------- C: chmod-000 ----------------
    os.chmod(FIX / "blocked", 0)
    case("C1-capture-eacces-dir-component", ["capture", "--out", str(REC / "blocked-pre.txt"),
                                             "--paths", str(FIX / "blocked" / "inner.txt")],
         note="path behind a chmod-000 dir component", receipt=REC / "blocked-pre.txt")
    case("C2-verify-eacces-vs-live", ["verify", str(REC / "blocked-pre.txt"), "--live"],
         note="both sides cannot evaluate -> ? (D2 fail-open)")
    os.chmod(FIX / "blocked", 0o755)
    case("C3-eacces-receipt-vs-now-readable", ["verify", str(REC / "blocked-pre.txt"), "--live"],
         note="capture said exists=no(STAT-ERROR); path now readable")
    os.chmod(FIX / "blocked", 0)
    case("C4a-capture-plainfile", ["capture", "--out", str(REC / "plainfile-pre.txt"),
                                   "--paths", str(FIX / "plainfile")])
    os.chmod(FIX / "plainfile", 0)
    case("C4b-verify-live-unreadable-file", ["verify", str(REC / "plainfile-pre.txt"), "--live"],
         note="candidate file exists but open() EACCES (D2 traceback)")
    case("C6a-capture-readable-file-control", ["capture", "--out", str(REC / "secret-ctl.txt"),
                                               "--paths", str(FIX / "secretfile")],
         note="control: readable file")
    os.chmod(FIX / "secretfile", 0)
    case("C6b-capture-unreadable-file", ["capture", "--out", str(REC / "unreadable2-pre.txt"),
                                         "--paths", str(FIX / "secretfile")],
         note="capture side against a chmod-000 file", receipt=REC / "unreadable2-pre.txt")
    os.chmod(FIX / "secretfile", 0o644)
    os.chmod(FIX / "plainfile", 0o644)  # restore: C4b left it 000; C7/C8 need a readable input
    case("C7-out-into-000-parent", ["capture", "--out", str(FIX / "blocked" / "out.txt"),
                                    "--paths", str(FIX / "plainfile")],
         note="write target's parent is chmod-000")
    case("C8-out-parent-is-file", ["capture", "--out", str(FIX / "pfile.txt" / "rec.txt"),
                                   "--paths", str(FIX / "plainfile")],
         note="path component of --out is a regular file")
    case("C9-selftest-scratch-000", ["selftest", "--scratch", str(FIX / "blocked")],
         note="scratch dir exists but is chmod-000")
    case("C10-selftest-scratch-missing", ["selftest", "--scratch", str(FIX / "no-such-dir")],
         note="D6: missing scratch dir")
    case("C11-selftest-scratch-is-file", ["selftest", "--scratch", str(FIX / "pfile.txt")],
         note="scratch path is a regular file")
    os.chmod(FIX / "secretreceipt.txt", 0)
    case("C12-verify-unreadable-receipt-file", ["verify", str(FIX / "secretreceipt.txt"), "--live"],
         note="receipt A itself chmod-000")
    os.chmod(FIX / "secretreceipt.txt", 0o644)
    os.chmod(FIX / "blockedrec", 0)
    case("C13-verify-receipt-in-000-dir", ["verify", str(FIX / "blockedrec" / "r.txt"), "--live"],
         note="receipt A behind a 000 dir component")
    os.chmod(FIX / "blockedrec", 0o755)
    case("C14a-capture-enoent", ["capture", "--out", str(REC / "enoent-pre.txt"),
                                 "--paths", str(FIX / "notthere")],
         note="path genuinely absent (ENOENT), no STAT-ERROR")
    (FIX / "notthere").write_bytes(b"appeared under EACCES\n")
    os.chmod(FIX / "notthere", 0)
    case("C14b-enoent-receipt-vs-eacces-live", ["verify", str(REC / "enoent-pre.txt"), "--live"],
         note="absent-at-capture vs EACCES-at-verify (file exists, chmod 000)")
    nf = FIX / "notthere2"
    case("C15a-capture-enoent2", ["capture", "--out", str(REC / "enoent2-pre.txt"),
                                  "--paths", str(nf)])
    nf.write_bytes(b"x\n")
    os.chmod(nf, 0)
    case("C15b-enoent-receipt-vs-chmod000-file-live",
         ["verify", str(REC / "enoent2-pre.txt"), "--live"],
         note="absent-at-capture vs chmod-000 file at verify")
    os.chmod(nf, 0o644)
    os.chmod(FIX / "blocked", 0)
    case("C16-capture-symlink-into-000-dir", ["capture", "--out", str(REC / "psym-pre.txt"),
                                              "--paths", str(FIX / "psym")],
         note="symlink whose referent is behind a 000 dir")
    case("C16b-verify-symlink-into-000-dir", ["verify", str(REC / "psym-pre.txt"), "--live"])
    os.chmod(FIX / "blocked", 0o755)

    # ---------------- D: round-3 declared classes + further type swaps ----------------
    case("D1-require-paths-5-on-1of5", ["verify", str(REC / "blocked-pre.txt"), "--live",
                                        "--require-paths", "5"],
         note="declared USAGE exit 2 when the reference carries fewer than N paths")
    case("D2-require-paths-1-on-1of5", ["verify", str(REC / "blocked-pre.txt"), "--live",
                                        "--require-paths", "1"],
         note="coverage satisfied -> normal classification")
    clob = FIX / "clobber-target.txt"
    clob.write_bytes(b"original bytes\n")
    case("D3-out-equals-paths", ["capture", "--out", str(clob), "--paths", str(clob)],
         note="write-guard scope: --paths X --out X refused? X must survive")
    print("-- clobber target after: %r --" % clob.read_bytes())
    os.chmod(FIX / "blocked", 0)
    case("D4a-capture-unevaluable-again", ["capture", "--out", str(REC / "blocked-post.txt"),
                                           "--paths", str(FIX / "blocked" / "inner.txt")])
    os.chmod(FIX / "blocked", 0o755)
    case("D4b-receipt-vs-receipt-unevaluable", ["verify", str(REC / "blocked-pre.txt"),
                                                str(REC / "blocked-post.txt")],
         note="both receipts carry STAT-ERROR -> fail-closed?")
    os.chmod(FIX / "blocked", 0)
    (FIX / "dirD" / "sub").mkdir(parents=True)
    (FIX / "dirD" / "sub" / "inner.txt").write_bytes(b"inner\n")
    case("D5a-capture-dirD", ["capture", "--out", str(REC / "dirD-pre.txt"),
                              "--paths", str(FIX / "dirD")])
    shutil.rmtree(FIX / "dirD")
    (FIX / "dirD").symlink_to("elsewhere")
    case("D5b-dir-swapped-to-symlink", ["verify", str(REC / "dirD-pre.txt"), "--live"],
         note="type swap directory -> symlink")
    (FIX / "file2").write_bytes(b"file2 content\n")
    case("D6a-capture-file2", ["capture", "--out", str(REC / "file2-pre.txt"),
                               "--paths", str(FIX / "file2")])
    (FIX / "file2").unlink()
    (FIX / "file2").mkdir()
    case("D6b-file-swapped-to-dir", ["verify", str(REC / "file2-pre.txt"), "--live"],
         note="type swap file -> directory")

    print("=" * 78)
    print("# MATRIX DONE; tool copy sha256 %s" % sha(TOOL))


if __name__ == "__main__":
    main()