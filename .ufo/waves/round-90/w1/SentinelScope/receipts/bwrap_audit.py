#!/usr/bin/env python3
"""Round-90 sentinel: audit of the carrier-blind sandbox the counter builds.

argv under audit, verbatim from tools/round-90/upx-later-block-battery.py
(invoke() and the carrier-blind arm):

  bwrap --dev-bind / / --tmpfs <run_root> --bind <decoy> <carrier>... -- <python> ...

`bind_targets` are the pins the counter blinds; `script_args` are the paths the
payload inspects (never bound, so they are the sandbox's own view).
"""
import json, os, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
B = os.path.join(S, "bwrap")
REC = []


def probe(name, payload, hide, decoy, bind_targets, script_args,
          no_tmpfs=False, timeout=60):
    argv = ["bwrap", "--dev-bind", "/", "/"]
    if not no_tmpfs:
        argv += ["--tmpfs", hide]
    for p in bind_targets:
        argv += ["--bind", decoy, p]
    argv += ["--", sys.executable, "-c", payload] + list(script_args)
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    rec = {"probe": name, "sandbox_argv": argv,
           "rc": p.returncode, "stdout": p.stdout.strip(),
           "stderr": p.stderr.strip()[-400:]}
    REC.append(rec)
    print(json.dumps({"probe": name, "rc": rec["rc"]}))
    for line in (rec["stdout"] or "").splitlines():
        print("   ", line[:240])
    if rec["stderr"]:
        print("   err:", rec["stderr"][:300].replace("\n", " | "))
    return rec


def main():
    shutil.rmtree(B, ignore_errors=True)
    os.makedirs(B)
    hide = os.path.join(B, "runroot")
    os.makedirs(hide)
    secret = os.path.join(hide, "packed-original")
    open(secret, "wb").write(b"THE-PACKED-ORIGINAL-THE-SANDBOX-MEANT-TO-HIDE\n")
    decoy = os.path.join(B, "decoy")
    open(decoy, "wb").write(b"decoy-not-a-carrier\n" * 64)
    paths = []
    for src in ("/usr/bin/jq", "/usr/bin/xxd", "/usr/lib/libz.so.1.3.2",
                "/usr/bin/docker-init"):
        rp = os.path.realpath(src)
        if rp not in paths:
            paths.append(rp)
    REC[:] = []
    print("bwrap:", subprocess.run(["bwrap", "--version"], capture_output=True,
                                   text=True).stdout.strip())

    probe("B0-baseline-decoys", (
        "import hashlib,sys\n"
        "for p in sys.argv[1:]:\n"
        "    print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()[:16])\n"),
        hide, decoy, paths, paths)

    probe("B1-hidden-run-root", (
        "import os,sys\n"
        "h=sys.argv[1]\n"
        "print('pid', os.getpid(), 'ppid', os.getppid())\n"
        "print('direct-secret', os.path.exists(h))\n"
        "print('runroot-listing', os.listdir(h) if os.path.isdir(h) else 'not-a-dir')\n"),
        hide, decoy, paths, [hide])

    probe("B1b-proc-peers", (
        "import os\n"
        "print('pid-ns-view', sorted(int(x) for x in os.listdir('/proc') if x.isdigit())[:12])\n"
        "print('host-pids-visible', any(os.path.exists('/proc/%d' % p) for p in (1000, 2000, 3000, 4000)))\n"
        "print('ppid-present', os.path.exists('/proc/%d' % os.getppid()))\n"),
        hide, decoy, paths, [])

    probe("B2-mountinfo", (
        "import sys\n"
        "for line in open('/proc/self/mountinfo'):\n"
        "    f=line.split()\n"
        "    if len(f)>4 and (f[4]=='/' or 'runroot' in line or 'decoy' in line):\n"
        "        print(line.strip()[:200])\n"),
        hide, decoy, paths, [])

    probe("B3-umount-tmpfs", (
        "import ctypes, os, sys\n"
        "h=sys.argv[1]\n"
        "print('before', os.path.exists(h))\n"
        "libc=ctypes.CDLL('libc.so.6', use_errno=True)\n"
        "rc=libc.umount2(h.encode(), 2)\n"
        "print('umount2 rc', rc, 'errno', ctypes.get_errno())\n"
        "print('after', os.path.exists(h))\n"
        "try:\n"
        "    print('secret', open(h,'rb').read()[:48] if os.path.isfile(h) else sorted(os.listdir(h)))\n"
        "except OSError as e:\n"
        "    print('secret', repr(e))\n"),
        hide, decoy, paths, [hide])

    probe("B4-namespaces", (
        "import os\n"
        "def ns(p):\n"
        "    try: return os.readlink(p)\n"
        "    except OSError as e: return 'absent'\n"
        "pp=os.getppid()\n"
        "for k in ('mnt','pid','user','ipc','net','uts'):\n"
        "    print(k, 'self', ns('/proc/self/ns/'+k), 'ppid', ns('/proc/%d/ns/'%pp+k))\n"
        "st=open('/proc/self/status').read()\n"
        "print('CapEff', st.split('CapEff:')[1].split()[0])\n"
        "print('uid', os.getuid(), 'euid', os.geteuid())\n"
        "print('no_new_privs', open('/proc/self/status').read().split('NoNewPrivs:')[1].split()[0])\n"),
        hide, decoy, paths, [])

    probe("B5-decoy-readback", (
        "import sys\n"
        "d=open(sys.argv[1],'rb').read(64)\n"
        "print('decoy-bytes', d[:32])\n"
        "print('is-decoy', d.startswith(b'decoy-not-a-carrier'))\n"),
        hide, decoy, paths, [decoy])

    probe("B6-write-into-hidden-root", (
        "import os, sys\n"
        "h=sys.argv[1]\n"
        "print('listdir', os.listdir(h) if os.path.isdir(h) else 'not-a-dir')\n"
        "open(os.path.join(h,'child-marker'),'w').write('x')\n"
        "print('wrote', os.path.exists(os.path.join(h,'child-marker')))\n"),
        hide, decoy, paths, [hide])

    probe("B7-no-tmpfs-control", (
        "import os, sys\n"
        "h=sys.argv[1]\n"
        "print('runroot-visible', os.path.isdir(h))\n"
        "print('secret-visible', os.path.isfile(h))\n"),
        hide, decoy, paths, [hide], no_tmpfs=True)

    # B8: the packed bytes are also reachable if the counter ever leaves a copy
    # outside run_root -- prove the sandbox does not hide a second copy.
    outside = os.path.join(B, "copy-of-carrier")
    shutil.copy2("/usr/bin/jq", outside)
    probe("B8-second-copy-outside", (
        "import hashlib,sys\n"
        "p=sys.argv[1]\n"
        "print('readable', os.path.isfile(p))\n"
        "print('sha256', hashlib.sha256(open(p,'rb').read()).hexdigest())\n"),
        hide, decoy, paths, [outside])

    json.dump({"probes": REC}, open(os.path.join(S, "bwrap.json"), "w"),
              indent=1, sort_keys=True)


main()
