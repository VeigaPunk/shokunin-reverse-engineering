#!/usr/bin/env python3
"""EX-22 pinning-correctness experiments (scratch under /var/tmp/ex22).

E1 newline/encoding normalization (text-mode hash vs binary hash)
E2 TOCTOU: naive two-open pin-then-parse vs single-read (hook + real race)
E3 symlink: follow, realpath, O_NOFOLLOW, mid-run retarget
E4 hardlink: inode identity, tamper-through-other-name, git visibility
E5 FIFO: blocking open vs fstat S_ISREG
E6 torn/truncated table
"""
import errno
import hashlib
import json
import os
import stat
import subprocess
import threading
import time

W = "/var/tmp/ex22/exp"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def p(*a):
    print(*a, flush=True)


LF = b'{"entries": []}\n'
CRLF = LF.replace(b"\n", b"\r\n")
BOM = b"\xef\xbb\xbf" + LF
EVIL = b'{"entries": [{"id": "EVIL"}]}\n'


def w(name, data):
    with open(os.path.join(W, name), "wb") as fh:
        fh.write(data)
    return os.path.join(W, name)


def r(name):
    with open(os.path.join(W, name), "rb") as fh:
        return fh.read()


# ---------------------------------------------------------------- E1
def e1():
    lf_path, crlf_path = w("t-lf.json", LF), w("t-crlf.json", CRLF)
    w("t-bom.json", BOM)
    h_lf_bin, h_crlf_bin = sha(r("t-lf.json")), sha(r("t-crlf.json"))
    # text-mode read applies universal-newline translation (newline=None)
    with open(crlf_path) as fh:
        crlf_text_bytes = fh.read().encode()
    h_crlf_text = sha(crlf_text_bytes)
    with open(lf_path) as fh:
        h_lf_text = sha(fh.read().encode())
    p("E1 sha256sum crlf   :", subprocess.run(["sha256sum", crlf_path],
      capture_output=True, text=True).stdout.split()[0])
    p("E1 binary hash lf   :", h_lf_bin)
    p("E1 binary hash crlf :", h_crlf_bin)
    p("E1 text-mode hash crlf:", h_crlf_text)
    p("E1 NORMALIZATION TRAP: text_hash(crlf) == bin_hash(lf):",
      h_crlf_text == h_lf_bin)
    p("E1 text-mode hash lf==bin hash lf:", h_lf_text == h_lf_bin)
    p("E1 json parses CRLF file (json.load):",
      json.load(open(crlf_path)) == json.loads(LF))
    try:
        json.load(open(os.path.join(W, "t-bom.json")))
        p("E1 BOM: parsed (unexpected)")
    except ValueError as exc:
        p("E1 BOM json.load raises:", type(exc).__name__)
    try:
        json.loads(BOM.decode("utf-8"))
        p("E1 BOM: json.loads parsed (unexpected)")
    except ValueError as exc:
        p("E1 BOM json.loads raises:", type(exc).__name__)


# ---------------------------------------------------------------- E2
def naive_two_open(path, pinned, hook=None):
    """The pattern a naive pin implementation takes: hash one read, parse
    another."""
    with open(path, "rb") as fh:
        h = sha(fh.read())
    if hook:
        hook()
    with open(path) as fh:
        table = json.load(fh)
    return h == pinned, table


def single_read(path, pinned, hook=None):
    """Pin and parse the SAME bytes object."""
    with open(path, "rb") as fh:
        data = fh.read()
    h = sha(data)
    if hook:
        hook()
    return h == pinned, json.loads(data.decode("utf-8"))


def e2():
    PIN = sha(LF)
    w("swap.json", LF)

    def swap():
        w("swap.tmp", EVIL)
        os.replace(os.path.join(W, "swap.tmp"), os.path.join(W, "swap.json"))

    ok, t = naive_two_open(os.path.join(W, "swap.json"), PIN, hook=swap)
    p("E2 hook naive  : pin_ok=%s parsed=%s" % (ok, t))
    w("swap.json", LF)  # reset: the hook above left the file swapped
    ok2, t2 = single_read(os.path.join(W, "swap.json"), PIN, hook=swap)
    p("E2 hook single : pin_ok=%s parsed=%s  (swap fired mid-run; parsed bytes "
      "are the hashed bytes)" % (ok2, t2))

    # real race, no hook: a swapper thread alternates the file under the reader
    def first_id(table):
        entries = table.get("entries") or [{}]
        return entries[0].get("id")

    w("race.json", LF)
    stop = threading.Event()

    def loop():
        while not stop.is_set():
            w("race.tmp", EVIL)
            os.replace(os.path.join(W, "race.tmp"), os.path.join(W, "race.json"))
            w("race.tmp", LF)
            os.replace(os.path.join(W, "race.tmp"), os.path.join(W, "race.json"))

    th = threading.Thread(target=loop, daemon=True)
    th.start()
    n = bad_naive = bad_single = 0
    deadline = time.time() + 2.0
    while time.time() < deadline and n < 50000:
        n += 1
        ok, t = naive_two_open(os.path.join(W, "race.json"), PIN)
        if ok and first_id(t) == "EVIL":
            bad_naive += 1
        ok2, t2 = single_read(os.path.join(W, "race.json"), PIN)
        if ok2 and first_id(t2) == "EVIL":
            bad_single += 1
    stop.set()
    time.sleep(0.05)
    p("E2 RACE iters=%d  naive: pin_ok+evil_parsed=%d   single-read: %d"
      % (n, bad_naive, bad_single))


# ---------------------------------------------------------------- E3
def e3():
    target = os.path.join(W, "t-lf.json")
    link = os.path.join(W, "link-table.json")
    if os.path.lexists(link):
        os.remove(link)
    os.symlink(target, link)
    st = os.lstat(link)
    p("E3 lstat S_ISLNK=%s realpath=%s" % (stat.S_ISLNK(st.st_mode),
                                           os.path.realpath(link)))
    p("E3 plain open follows symlink:", r("link-table.json") == LF)
    try:
        fd = os.open(link, os.O_RDONLY | os.O_NOFOLLOW)
        os.close(fd)
        p("E3 O_NOFOLLOW opened (unexpected)")
    except OSError as exc:
        p("E3 O_NOFOLLOW refused: errno=%s (%s)"
          % (exc.errno, errno.errorcode.get(exc.errno)))

    # mid-run retarget under single-read: parse still sees the hashed bytes
    other = w("other.json", EVIL)

    def retarget():
        os.remove(link)
        os.symlink(other, link)

    ok, t = single_read(link, sha(LF), hook=retarget)
    p("E3 retarget-mid-run single-read: pin_ok=%s parsed=%s (link now -> evil)"
      % (ok, t))


# ---------------------------------------------------------------- E4
def e4():
    a = w("hard-a.json", LF)
    b = os.path.join(W, "hard-b.json")
    if os.path.lexists(b):
        os.remove(b)
    os.link(a, b)
    sa, sb = os.stat(a), os.stat(b)
    p("E4 same inode=%s nlink=%d" % (sa.st_ino == sb.st_ino, sa.st_nlink))
    with open(b, "ab") as fh:
        fh.write(b" ")
    p("E4 after tamper through the OTHER name: sha(a)=%s matches pin=%s"
      % (sha(r("hard-a.json")), sha(r("hard-a.json")) == sha(LF)))
    # git visibility of the same tamper, in a throwaway repo
    d = "/var/tmp/ex22/exp/hardlink-repo"
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    subprocess.run(["git", "init", "-q", d], check=True)
    with open(os.path.join(d, "tbl.json"), "wb") as fh:
        fh.write(LF)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=e@x", "-c", "user.name=e",
                    "commit", "-qm", "x"], check=True)
    os.link(os.path.join(d, "tbl.json"), os.path.join(d, "alias.json"))
    with open(os.path.join(d, "alias.json"), "ab") as fh:
        fh.write(b" ")
    st = subprocess.run(["git", "-C", d, "status", "--porcelain"],
                        capture_output=True, text=True).stdout.strip()
    p("E4 git status after tamper through hardlink alias: %r" % st)


# ---------------------------------------------------------------- E5
def e5():
    fifo = os.path.join(W, "fifo-table.json")
    if os.path.lexists(fifo):
        os.remove(fifo)
    os.mkfifo(fifo)
    st = os.lstat(fifo)
    p("E5 lstat S_ISREG=%s S_ISFIFO=%s"
      % (stat.S_ISREG(st.st_mode), stat.S_ISFIFO(st.st_mode)))
    r_ = subprocess.run(["timeout", "2", "python3", "-c",
                         "open(%r,'rb').read()" % fifo],
                        capture_output=True, text=True)
    p("E5 blocking open on FIFO: exit=%s (124 = killed while blocked)" % r_.returncode)
    fd = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
    try:
        st2 = os.fstat(fd)
        p("E5 O_NONBLOCK open + fstat S_ISREG=%s (refusable without blocking)"
          % stat.S_ISREG(st2.st_mode))
    finally:
        os.close(fd)
    reg = w("reg.json", LF)
    fd = os.open(reg, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        with os.fdopen(fd, "rb") as fh:
            p("E5 O_NONBLOCK on a regular file is a no-op, read ok:",
              fh.read() == LF)
    except Exception as exc:  # noqa
        p("E5 regular+O_NONBLOCK failed:", exc)


# ---------------------------------------------------------------- E6
def e6():
    torn = w("torn.json", LF[:8])
    try:
        json.loads(open(torn, "rb").read().decode("utf-8"))
        p("E6 torn parsed (unexpected)")
    except ValueError as exc:
        p("E6 torn bytes: json parse raises %s (%s)" % (type(exc).__name__, exc))
    p("E6 torn digest != pin:", sha(r("torn.json")) != sha(LF))


for fn in (e1, e2, e3, e4, e5, e6):
    p("=" * 20, fn.__name__)
    fn()
p("DONE")
