#!/usr/bin/env python3
"""Generate one-behavior mutants of the pristine absence-sweep.py into mut/.

Each mutant is pristine bytes with exactly one literal replacement (asserted
unique). Anchors taken verbatim from
kaidoku-shokunin/tools/round-39/absence-sweep.py sha256
3a7a4abf2f7f0bc89f7b4a630f0458133752fe7da11c80d89443f11d92280775.
"""
import hashlib
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(S, "pristine.py"), "r", encoding="utf-8").read()

MATCH_OLD = """\
                parts = ent.path.split(os.sep)
                if parts[-n:] != claim_parts:
                    continue
"""

MUTANTS = [
    # --- suffix matching ---
    ("m01-tail-endswith",
     MATCH_OLD,
     """\
                parts = ent.path.split(os.sep)
                if not ent.path.endswith(os.sep.join(claim_parts)):
                    continue
"""),
    ("m02-basename-only",
     MATCH_OLD,
     """\
                parts = ent.path.split(os.sep)
                if parts[-1:] != claim_parts[-1:]:
                    continue
"""),
    ("m03-case-insensitive",
     MATCH_OLD,
     """\
                parts = ent.path.split(os.sep)
                if [p.lower() for p in parts[-n:]] != [p.lower() for p in claim_parts]:
                    continue
"""),
    # --- root walking ---
    ("m04-follow-dir-symlinks",
     "                    is_dir = ent.is_dir(follow_symlinks=False)",
     "                    is_dir = ent.is_dir(follow_symlinks=True)"),
    ("m05-scandir-error-uncounted",
     """\
            except OSError:
                stats["skipped_dirs"] += 1
                continue
""",
     """\
            except OSError:
                continue
"""),
    ("m06-no-recursion",
     """\
                if is_dir:
                    stack.append(ent.path)
                    continue
""",
     """\
                if is_dir:
                    continue
"""),
    ("m07-root-probe-dropped",
     """\
        try:
            with os.scandir(r):
                pass
        except OSError as exc:
            errors.append("root is unreadable: %s (%s)" % (r, exc.strerror or exc))
            continue
""",
     ""),
    # --- exit mapping ---
    ("m08-incomplete-certified-absent",
     '        verdict, code = "INCOMPLETE", EXIT_ERROR',
     '        verdict, code = "ABSENT", ABSENT'),
    ("m09-present-exit-zero",
     '        verdict, code = "PRESENT", PRESENT',
     '        verdict, code = "PRESENT", ABSENT'),
    ("m10-error-code-three",
     "ABSENT, PRESENT, EXIT_ERROR = 0, 1, 2",
     "ABSENT, PRESENT, EXIT_ERROR = 0, 1, 3"),
    ("m15-constants-swapped",
     "ABSENT, PRESENT, EXIT_ERROR = 0, 1, 2",
     "ABSENT, PRESENT, EXIT_ERROR = 1, 0, 2"),
    ("m16-present-constant-five",
     "ABSENT, PRESENT, EXIT_ERROR = 0, 1, 2",
     "ABSENT, PRESENT, EXIT_ERROR = 0, 5, 2"),
    # --- multi-root handling ---
    ("m11-nested-dedup-dropped",
     "        if any(rp == k or rp.startswith(k.rstrip(os.sep) + os.sep) for k in kept_real):",
     "        if any(rp == k for k in kept_real):"),
    ("m12-duplicate-dedup-dropped",
     "        if any(rp == k or rp.startswith(k.rstrip(os.sep) + os.sep) for k in kept_real):",
     "        if any(rp.startswith(k.rstrip(os.sep) + os.sep) for k in kept_real):"),
    ("m13-no-length-sort",
     "    for r in sorted(prepared, key=lambda p: (len(root_of(p)), p)):",
     "    for r in prepared:"),
    ("m14-first-root-only",
     "    for root in roots:\n        stack = [root]",
     "    for root in roots[:1]:\n        stack = [root]"),
    ("m17-dedup-no-realpath",
     "        rp = root_of(r)",
     "        rp = os.path.abspath(r)"),
]

mutdir = os.path.join(S, "mut")
os.makedirs(mutdir, exist_ok=True)
for name, old, new in MUTANTS:
    n = src.count(old)
    if n != 1:
        sys.exit("mutant %s: anchor occurs %d times, expected exactly 1" % (name, n))
    out = src.replace(old, new, 1)
    path = os.path.join(mutdir, name + ".py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
    digest = hashlib.sha256(out.encode("utf-8")).hexdigest()
    print("%-32s sha256=%s" % (name, digest))
print("generated %d mutants" % len(MUTANTS))
