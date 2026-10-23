#!/usr/bin/env python3
"""CtlNoReader control reader: strongest no-reader oracle (never opens input).

Threat model: a reader that NEVER opens the carrier input file, yet is given
every advantage a hostile local process could extract:

  * the carrier identity, recovered from os.stat().st_size alone, because the
    frozen manifest assigns a distinct byte size to each of the twelve
    carriers;
  * the frozen root of the measured tree, recovered from the parent process
    command line (/proc/<ppid>/cmdline), which the counter passes on its own
    command line;
  * the complete expected record set, read from the frozen manifest
    <root>/.ufo/waves/round-34/expected.json.

It then emits the exact frozen expected record for the carrier it was handed.

The question this control answers: with unrestricted local knowledge of the
frozen expected data, can a reader that never opens the input still satisfy
the predicate?  The answer decides whether the counter's randomized
same-length string-table renaming (schedule 1) is the load-bearing defence or
whether something else stops the replay.

Control, not a candidate implementation.
"""
import json
import os
import sys


def find_root():
    """Recover the measured root from the parent process command line."""
    ppid = os.getppid()
    argv = []
    try:
        with open("/proc/%d/cmdline" % ppid, "rb") as handle:
            argv = handle.read().decode("utf-8", "replace").split("\x00")
    except OSError:
        argv = []
    for index, value in enumerate(argv):
        if value == "--root" and index + 1 < len(argv):
            root = argv[index + 1]
            if not os.path.isabs(root):
                # The counter runs the reader with cwd set to its own temp
                # directory, so a relative --root must be resolved against the
                # counter's working directory, not the reader's.
                try:
                    root = os.path.join(os.readlink("/proc/%d/cwd" % ppid), root)
                except OSError:
                    root = os.path.abspath(root)
            return root
    return "/fast/scratch/hyaku/kaidoku-r34/w1/CtlNoReader"


def main():
    path = sys.argv[1]
    root = find_root()
    manifest_path = os.path.join(root, ".ufo", "waves", "round-34", "expected.json")
    with open(manifest_path, "rb") as handle:
        manifest = json.loads(handle.read().decode("utf-8"))
    by_size = {row["size"]: row["expected"] for row in manifest["carriers"]}
    # os.stat only: the carrier bytes are never opened.
    size = os.stat(path).st_size
    record = by_size[size]
    sys.stdout.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
