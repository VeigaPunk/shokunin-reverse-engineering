#!/usr/bin/env python3
"""EX-27 round-4 harness self-test: build a SCRATCH-ONLY simulated r4 revision.

Purpose: validate the harness's `--phase r4` expectations and its leg-H sabotage
patterns *before* EX-21's real revision lands, so that a red row in the after-phase
is a property of the tool and not a harness bug. This writes NOTHING to the real
target: it reads the round-3 landed bytes and emits a modified copy under /var/tmp.

The simulated edits are the round-3 patch texts' shapes (EX-24 one-line basis fix,
CR-3/RV-8 guarded-mkdir, CR-4 sidecar-in-candidate-paths). EX-21's real revision may
differ in shape; only the leg-H sabotage patterns depend on that shape, and they
degrade to an observed-only row (not a failure) when a pattern does not match.

usage: sim-r4-revision.py <in-tool> <out-tool>
"""
import re
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
edits = []

old_guard = """        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        if out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded):
            print("USAGE: refusing to write a receipt over a path it measures or a custody path"
                  " (path or inode): %s" % out, file=sys.stderr)
            return EXIT_USAGE
        out.parent.mkdir(parents=True, exist_ok=True)
"""
new_guard = """        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        candidate_paths = (out, out.with_name(out.name + ".sha256"))
        for cand in candidate_paths:
            if cand.resolve() in {g.resolve() for g in guarded} or any(_same_file(cand, g) for g in guarded):
                print("USAGE: refusing to write a receipt over a guarded path (path or inode): %s"
                      % cand, file=sys.stderr)
                return EXIT_USAGE
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print("USAGE: cannot create the receipt directory (%s): %s" % (exc, out.parent),
                  file=sys.stderr)
            return EXIT_USAGE
"""
src, n = re.subn(re.escape(old_guard), new_guard, src)
edits.append(("guard+mkdir", n))

src, n = re.subn(r"return len\(ref_sections\) >= required, line",
                 "return len(have) >= required, line", src)
edits.append(("coverage-basis", n))

out = Path(sys.argv[2])
out.write_text(src, encoding="utf-8")
out.chmod(0o755)
print("sim edits: " + ", ".join("%s=%d" % e for e in edits))
if any(n == 0 for _, n in edits):
    sys.exit("SIM INCOMPLETE — a pattern did not match; harness smoke test would be invalid")
