"""Run the real scoring CLI while refusing host-home file opens before I/O."""
import json
import os
from pathlib import Path
import runpy
import sys

script, output, work = sys.argv[1:4]
denied = []

def guard(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.path.realpath(os.fsdecode(args[0]))
        if path == "/home/vgpnk" or path.startswith("/home/vgpnk/"):
            denied.append(path)
            raise PermissionError("ExecAttr host-home read prohibited")

sys.addaudithook(guard)
sys.argv = [script, "--root", str(Path(script).parents[2]),
            "--work", work, "--json-out", output]
try:
    runpy.run_path(script, run_name="__main__")
finally:
    print(json.dumps({"host_home_opens_refused_before_io": len(denied),
                      "unique_refused_paths": sorted(set(denied))}))
