import json, os, sys
open(os.path.join(os.getcwd(), "env-seen.json"), "w").write(json.dumps(
    {"env": dict(sorted(os.environ.items())), "argv": sys.argv, "cwd": os.getcwd(),
     "executable": sys.executable, "isolated": sys.flags.isolated}, indent=1, sort_keys=True))
print("ENVPROBE written")
sys.exit(0)
