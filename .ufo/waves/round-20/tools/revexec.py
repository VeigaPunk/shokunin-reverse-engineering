#!/usr/bin/env python3
"""Execute revision-pinned lane Python in a systemd OS sandbox.

Usage: revexec.py run --root LANE --rev REV --entry PATH [--extra PATH ...] -- ARGS

The selected blobs are read from Git at REV, copied to a fresh /tmp work
 directory, and executed by python3 -I -B inside a transient user systemd unit.
The unit has a private network namespace, a read-only filesystem except for
that work directory, and no writable home/runtime directories. The residual
trust is explicit: executed code runs as the same uid; kernel bugs may bypass
the restrictions; this is not a security boundary against root.
"""

import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile


class RevExecError(Exception):
    """A revision, path, or required sandbox capability could not be used."""


# `-I` deliberately excludes the script directory from Python's implicit
# import path. Add only the extracted workspace and entry directory explicitly
# so `--extra` blobs remain usable without consulting caller PYTHONPATH.
_PYTHON_BOOTSTRAP = (
    "import os, runpy, sys\n"
    "script = os.path.abspath(sys.argv[1])\n"
    "workspace = os.path.abspath(sys.argv[2])\n"
    "sys.argv = [script, *sys.argv[3:]]\n"
    "sys.path[:0] = [os.path.dirname(script), workspace]\n"
    "runpy.run_path(script, run_name='__main__')\n"
)


def _git(root, *args, stdout=subprocess.PIPE):
    env = dict(os.environ)
    env.update({
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
        "GIT_TERMINAL_PROMPT": "0",
    })
    try:
        return subprocess.run(
            ["git", "-C", root, "--no-optional-locks", *args],
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
    except OSError as exc:
        raise RevExecError(f"git could not run: {exc}") from exc


def _git_error(args, proc):
    detail = proc.stderr.decode("utf-8", "replace").strip()
    if not detail:
        detail = "no diagnostic"
    return RevExecError(
        f"git {' '.join(args[:2])} exited {proc.returncode}: {detail}"
    )


def _resolve_revision(root, revision):
    selector = revision + "^{commit}"
    args = ("rev-parse", "--verify", "--quiet", "--end-of-options", selector)
    proc = _git(root, *args)
    if proc.returncode != 0:
        raise _git_error(args, proc)
    commit = proc.stdout.decode("ascii", "strict").strip()
    if not commit or any(char not in "0123456789abcdefABCDEF" for char in commit):
        raise RevExecError("Git returned an invalid commit id")
    return commit


def _repo_path(value):
    if not value or "\0" in value or value.startswith("/"):
        raise RevExecError(f"lane path is not a relative Git path: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise RevExecError(f"lane path contains an unsafe component: {value!r}")
    return parts


def _extract_blob(root, commit, lane_path, destination):
    parts = _repo_path(lane_path)
    object_name = f"{commit}:{lane_path}"
    type_args = ("cat-file", "-t", object_name)
    proc = _git(root, *type_args)
    if proc.returncode != 0:
        raise _git_error(type_args, proc)
    object_type = proc.stdout.decode("ascii", "replace").strip()
    if object_type != "blob":
        raise RevExecError(f"revision path is not a blob: {lane_path}")

    output_path = os.path.join(destination, *parts)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    show_args = ("show", "--no-ext-diff", "--no-textconv", object_name)
    try:
        with open(output_path, "xb") as output:
            proc = _git(root, *show_args, stdout=output)
    except OSError as exc:
        raise RevExecError(f"could not materialize {lane_path}: {exc}") from exc
    if proc.returncode != 0:
        raise _git_error(show_args, proc)
    return output_path


def _sandbox_command(workdir, entry_path, script_args):
    runner = shutil.which("systemd-run")
    if runner is None:
        raise RevExecError("systemd-run is required; refusing unsandboxed execution")
    env = shutil.which("env")
    if env is None:
        raise RevExecError("env is required to clear the child environment")

    command = [
        runner, "--user", "--pipe", "--wait", "--collect", "--quiet",
        "--property=PrivateNetwork=yes",
        "--property=ProtectSystem=strict",
        "--property=ProtectHome=read-only",
        "--property=ReadWritePaths=" + workdir,
        "--property=WorkingDirectory=" + workdir,
        "--property=NoNewPrivileges=yes",
        "--property=RestrictNamespaces=yes",
        "--property=PrivateDevices=yes",
        "--property=ProtectProc=invisible",
        "--property=ProcSubset=pid",
        "--property=ProtectKernelTunables=yes",
        "--property=ProtectKernelModules=yes",
        "--property=ProtectKernelLogs=yes",
        "--property=ProtectControlGroups=yes",
        "--property=InaccessiblePaths=/run/user /dev/mqueue",
        "--property=TemporaryFileSystem=/dev/shm:ro",
        "--",
        env, "-i",
        "HOME=" + workdir,
        "PATH=/usr/bin:/bin",
        "TMPDIR=" + workdir,
        "TMP=" + workdir,
        "TEMP=" + workdir,
        sys.executable, "-I", "-B", "-c", _PYTHON_BOOTSTRAP,
        entry_path, workdir, *script_args,
    ]
    return command


def _run_revision(root, revision, entry, extra, script_args, capture=False):
    root = os.path.realpath(root)
    if not os.path.isdir(root):
        raise RevExecError(f"repository root is not a directory: {root}")
    commit = _resolve_revision(root, revision)
    paths = [entry, *extra]
    normalized = [_repo_path(path) for path in paths]
    if len({tuple(parts) for parts in normalized}) != len(normalized):
        raise RevExecError("entry and extra paths must be unique")

    # Keep extracted blobs and all intentional child writes in one allowlisted
    # directory; the systemd unit makes every other filesystem location RO.
    workdir = tempfile.mkdtemp(prefix="revexec-work-", dir="/tmp")
    try:
        extracted = {}
        for lane_path in paths:
            extracted[lane_path] = _extract_blob(root, commit, lane_path, workdir)
        command = _sandbox_command(workdir, extracted[entry], script_args)
        try:
            return subprocess.run(
                command,
                stdin=None if not capture else subprocess.DEVNULL,
                stdout=subprocess.PIPE if capture else None,
                stderr=subprocess.PIPE if capture else None,
                check=False,
            )
        except OSError as exc:
            raise RevExecError(f"systemd-run could not start: {exc}") from exc
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _check_output(proc, marker):
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", "replace").strip()
        return False, f"exit={proc.returncode} stderr={stderr!r}"
    stdout = proc.stdout.decode("utf-8", "replace")
    if marker not in stdout:
        return False, f"missing marker {marker!r}; stdout={stdout!r}"
    return True, ""


def _selftest():
    base = tempfile.mkdtemp(prefix="revexec-selftest-", dir="/tmp")
    repo = os.path.join(base, "repo")
    os.mkdir(repo)
    outside = os.path.join(base, "outside.txt")
    cases = []
    listener = None
    try:
        for path, contents in (
            ("write_outside_refused.py", (
                "from pathlib import Path\n"
                f"target = Path({outside!r})\n"
                "try:\n"
                "    target.write_text('escape', encoding='utf-8')\n"
                "except OSError:\n"
                "    print('WRITE_REFUSED')\n"
                "else:\n"
                "    print('WRITE_SUCCEEDED')\n"
            )),
            ("net_refused.py", ""),
            ("runs_ok.py", (
                "import sys\n"
                "from pathlib import Path\n"
                "from helper import VALUE\n"
                "Path('inside.txt').write_text('inside', encoding='utf-8')\n"
                "print('RUNS_OK', VALUE, repr(sys.argv[1:]))\n"
            )),
            ("helper.py", "VALUE = 'EXTRA_OK'\n"),
        ):
            file_path = os.path.join(repo, path)
            with open(file_path, "w", encoding="utf-8") as output:
                output.write(contents)

        git_init = _git(repo, "init", "--quiet")
        if git_init.returncode != 0:
            raise _git_error(("init",), git_init)
        for key, value in (
            ("user.name", "revexec selftest"),
            ("user.email", "revexec-selftest.invalid"),
        ):
            config = _git(repo, "config", key, value)
            if config.returncode != 0:
                raise _git_error(("config", key), config)
        added = _git(repo, "add", "--", ".")
        if added.returncode != 0:
            raise _git_error(("add",), added)
        committed = _git(repo, "commit", "--quiet", "-m", "revexec selftest fixture")
        if committed.returncode != 0:
            raise _git_error(("commit",), committed)

        write_proc = _run_revision(
            repo, "HEAD", "write_outside_refused.py", [], [], capture=True
        )
        write_ok, write_detail = _check_output(write_proc, "WRITE_REFUSED")
        write_ok = write_ok and not os.path.exists(outside)
        if not write_ok and not write_detail:
            write_detail = "outside sibling was created despite WRITE_REFUSED"
        cases.append(("write_outside_refused", write_ok, write_detail))

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        net_path = os.path.join(repo, "net_refused.py")
        with open(net_path, "w", encoding="utf-8") as output:
            output.write(
                "import socket\n"
                "try:\n"
                f"    socket.create_connection(('127.0.0.1', {port}), timeout=1)\n"
                "except OSError:\n"
                "    print('NET_REFUSED')\n"
                "else:\n"
                "    print('NET_CONNECTED')\n"
            )
        added = _git(repo, "add", "--", "net_refused.py")
        if added.returncode != 0:
            raise _git_error(("add",), added)
        committed = _git(repo, "commit", "--quiet", "-m", "add network fixture")
        if committed.returncode != 0:
            raise _git_error(("commit",), committed)
        net_proc = _run_revision(repo, "HEAD", "net_refused.py", [], [], capture=True)
        net_ok, net_detail = _check_output(net_proc, "NET_REFUSED")
        cases.append(("net_refused", net_ok, net_detail))

        run_proc = _run_revision(
            repo, "HEAD", "runs_ok.py", ["helper.py"],
            ["value with space", "--child"], capture=True,
        )
        run_ok, run_detail = _check_output(run_proc, "RUNS_OK EXTRA_OK")
        if run_ok and "['value with space', '--child']" not in run_proc.stdout.decode(
            "utf-8", "replace"
        ):
            run_ok = False
            run_detail = "script arguments were not preserved"
        cases.append(("runs_ok", run_ok, run_detail))
    except Exception as exc:
        cases.append(("fixture_setup", False, str(exc)))
    finally:
        if listener is not None:
            listener.close()
        shutil.rmtree(base, ignore_errors=True)

    failures = 0
    for name, passed, detail in cases:
        print(f"CASE {name}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            failures += 1
            if detail:
                print(f"  {detail}")
    if failures:
        print(f"SELFTEST: FAILED cases={len(cases)} fails={failures}")
        return 1
    print(f"SELFTEST: CLEAN cases={len(cases)}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run revision-pinned lane Python inside an OS sandbox."
    )
    parser.add_argument("--selftest", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--root", required=True)
    run_parser.add_argument("--rev", required=True)
    run_parser.add_argument("--entry", required=True)
    run_parser.add_argument("--extra", action="append", default=[])
    run_parser.add_argument("script_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if args.selftest:
        return _selftest()
    if args.command != "run":
        parser.error("expected 'run' or --selftest")
    script_args = args.script_args
    if script_args and script_args[0] == "--":
        script_args = script_args[1:]
    try:
        proc = _run_revision(
            args.root, args.rev, args.entry, args.extra, script_args, capture=False
        )
    except RevExecError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
