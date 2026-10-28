#!/usr/bin/env python3
"""Round-46 freeze-integrity core, shared by `attest.py` and `registry.py`.

Round 45 routed four defects into this core and each has a named arm here:

- **R45-CL6** the round-45 freeze arms read `git log --name-only`, which prints no
  diff for a merge, so a resolution edit on a frozen path was invisible.  Here the
  history arm is `git log -m --diff-merges=first-parent --name-status -z`, and a
  second, independent blob arm compares `freeze:path` against `rev:path`; the two
  must agree (`restored` names a path the history arm saw and the blob arm finds
  clean).
- **R45-CL18** a path named only by `--freeze-path` never entered `touched`, so a
  tamper-then-restore of it read `clean`.  Here the frozen set is DERIVED from the
  claims file and used for both arms, so the two scopes cannot differ.
- **R45-CL20** the scratch root fell back to `/tmp`.  `scratch()` refuses a bare
  `/tmp`, `/var/tmp` or unset root instead of degrading.
- **R45-CL22** `--json-out` trusted the caller and could overwrite the graded
  surface.  `out_path()` refuses any output inside the lane's graded or frozen
  bytes and any path outside the lane root.

Exit contract, used by both counters: 0 clean/met, 1 violation, 2 could-not-evaluate.
An unhandled exception is a defect, never a verdict: every entry point catches it
and returns 2 (`R45-CL13` (f): a malformed heading crashed the round-45 counter).

Reads Git objects only; never writes inside the repo it measures.
"""
import os
import re
import subprocess
import sys
import tempfile

CLAIMS = "plans/round-46-claims.md"
FROZEN_HEADING = "## Frozen paths (exact)"
GRADED = ("SKILL.md", "LOG.md", "SCORECARD.md", "PROVINCE.md", "SHONEN.md",
          "plans", "tools", "corpus", "evidence")
STATUS = re.compile(r"^[ACDMRTUXB][0-9]*$")
# Any real partition works; only the shared temporary partitions are refused, because
# the driver reaps them after 45 idle minutes and nothing there is citable evidence.
TEMP_PARTITIONS = ("/tmp", "/var/tmp")


def git(root, *args, binary=False, timeout=120):
    return subprocess.run(["git", "-C", root, *args], capture_output=True,
                          text=not binary, timeout=timeout)


def show(root, rev, path):
    r = git(root, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def blob(root, rev, path):
    r = git(root, "rev-parse", "--verify", "--quiet", f"{rev}:{path}")
    return r.stdout.strip() if r.returncode == 0 else None


def resolve(root, ref):
    r = git(root, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    return r.stdout.strip() if r.returncode == 0 else None


def frozen_set(root, rev, claims=CLAIMS):
    """Derive the frozen paths from the claims file at `rev`.

    Returns (entries, error) where entries is [(path, is_dir)] in file order.
    The file is the rule: nothing here knows a round's paths in advance.
    """
    body = show(root, rev, claims)
    if body is None:
        return None, f"claims file absent at rev: {claims}"
    if FROZEN_HEADING not in body:
        return None, f"claims file has no '{FROZEN_HEADING}' section"
    section = body.split(FROZEN_HEADING, 1)[1].split("\n## ", 1)[0]
    entries, seen = [], set()
    for line in section.splitlines():
        m = re.match(r"^- `([^`]+)`", line.strip())
        if not m:
            continue
        raw = m.group(1).strip()
        is_dir = raw.endswith("/")
        path = raw.rstrip("/")
        if path and path not in seen:
            seen.add(path)
            entries.append((path, is_dir))
    if not entries:
        return None, "frozen section lists no path"
    return entries, None


def history_touched(root, base, tip, paths):
    """Every path under `paths` that any commit in base..tip touched, merges included.

    `--diff-merges=first-parent` makes a merge show the diff it introduced on the
    first-parent side, which is exactly the resolution edit R45-CL6 could not see.
    """
    if not paths:
        return [], None
    r = git(root, "log", "--diff-merges=first-parent", "-m", "--name-status", "-z",
            "--format=", f"{base}..{tip}", "--", *paths, binary=True)
    if r.returncode != 0:
        return None, "git log failed"
    tokens = r.stdout.decode("utf-8", "surrogateescape").split("\0")
    touched = set()
    i = 0
    while i < len(tokens):
        if STATUS.match(tokens[i].strip()) and i + 1 < len(tokens):
            path = tokens[i + 1]
            if path:
                touched.add(path)
            i += 2
            continue
        i += 1
    return sorted(touched), None


def blob_changed(root, base, tip, entries):
    """Paths whose object differs between the two revisions (a directory by its tree)."""
    changed = []
    for path, is_dir in entries:
        if is_dir:
            a = git(root, "rev-parse", "--verify", "--quiet", f"{base}:{path}")
            b = git(root, "rev-parse", "--verify", "--quiet", f"{tip}:{path}")
            if a.returncode != b.returncode or a.stdout != b.stdout:
                changed.append(path + "/")
        else:
            if blob(root, base, path) != blob(root, tip, path):
                changed.append(path)
    return changed


def dirty(root, pathspecs):
    """Uncommitted paths under the union of the given pathspecs (R45-CL15: union, not replace)."""
    args = ["status", "--porcelain", "-z", "--no-renames"]
    if pathspecs:
        args += ["--", *pathspecs]
    r = git(root, *args, binary=True)
    if r.returncode != 0:
        return None
    out = r.stdout.decode("utf-8", "surrogateescape").split("\0")
    return sorted({t[3:] for t in out if len(t) > 3 and t[2] == " "})


def freeze_state(root, freeze, rev, claims=CLAIMS):
    """The full freeze verdict. Returns (exit_code, receipt)."""
    base, tip = resolve(root, freeze), resolve(root, rev)
    for label, oid in (("freeze", base), ("rev", tip)):
        if oid is None:
            return 2, {"reason": f"unknown {label} revision"}
    if git(root, "merge-base", "--is-ancestor", base, tip).returncode != 0:
        return 2, {"reason": "freeze is not an ancestor of rev"}
    # The set is derived at BOTH ends and unioned: a measured revision that rewrites its own
    # `## Frozen paths` section cannot shrink the scope of the arms that check it (wave-1
    # R46W1RevRestoredUnion F2: a tip-only derivation let one commit erase the real entries,
    # add a decoy, and score the tampered tool clean).
    base_entries, err = frozen_set(root, base, claims)
    if err:
        return 2, {"reason": "at freeze: " + err}
    tip_entries, err = frozen_set(root, tip, claims)
    if err:
        return 2, {"reason": "at rev: " + err}
    entries, seen = [], set()
    for entry in base_entries + tip_entries:
        if entry[0] not in seen:
            seen.add(entry[0])
            entries.append(entry)
    paths = [p + "/" for p, d in entries if d] + [p for p, d in entries if not d]
    touched, err = history_touched(root, base, tip, paths)
    if err:
        return 2, {"reason": err}
    changed = blob_changed(root, base, tip, entries)
    restored = [p for p in touched if p.rstrip("/") not in {c.rstrip("/") for c in changed}]
    dirty_paths = dirty(root, paths)
    if dirty_paths is None:
        return 2, {"reason": "git status failed"}
    receipt = {
        "freeze": base, "rev": tip,
        "frozen_derived": paths,
        "frozen_from": {"freeze": [p for p, _ in base_entries],
                        "rev": [p for p, _ in tip_entries]},
        "frozen_path_changed": sorted(set(changed) | set(touched)),
        "blob_changed": changed,
        "touched": touched,
        "restored": restored,
        "dirty": dirty_paths,
    }
    if dirty_paths:
        # The counters grade committed bytes, but they EXECUTE from the worktree: an
        # uncommitted change to a frozen tool is a different instrument (F3).
        receipt["reason"] = "frozen_worktree_dirty"
        return 2, receipt
    if receipt["frozen_path_changed"]:
        receipt["reason"] = "frozen_path_changed"
        return 2, receipt
    return 0, receipt


def out_path(root, path):
    """Resolve a `--json-out` target, or return (None, reason) when it is refused."""
    if not path:
        return None, None
    full = os.path.realpath(path)
    lane = os.path.realpath(root)
    if os.path.commonpath([full, lane]) != lane:
        return None, f"--json-out outside the lane root: {path}"
    rel = os.path.relpath(full, lane).replace(os.sep, "/")
    head = rel.split("/", 1)[0]
    if rel in GRADED or head in GRADED:
        return None, f"--json-out inside a graded or frozen surface: {rel}"
    return full, None


def scratch(prefix):
    """A scratch dir under an explicit non-/tmp root (R45-CL20: never a bare /tmp)."""
    base = os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR")
    if not base:
        return None, "no HYAKU_SCRATCH/TMPDIR root set"
    base = os.path.realpath(base)
    if any(base == t or base.startswith(t + "/") for t in TEMP_PARTITIONS):
        return None, f"scratch root is a temporary partition: {base}"
    try:
        os.makedirs(base, exist_ok=True)
        return tempfile.mkdtemp(dir=base, prefix=prefix), None
    except OSError as exc:
        return None, f"scratch root unusable: {exc}"


def emit(receipt, path=None):
    import json
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if path:
        with open(path, "w") as fh:
            fh.write(text + "\n")
    print(text)
    return receipt


def main_guard(fn):
    """Run `fn` and turn any unexpected exception into exit 2 (never a crash verdict)."""
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 - a crash is a could-not-evaluate, not a verdict
        return 2, {"reason": "unhandled %s: %s" % (type(exc).__name__, str(exc)[:300])}


if __name__ == "__main__":
    sys.exit("gate.py is a library; use attest.py or registry.py")
