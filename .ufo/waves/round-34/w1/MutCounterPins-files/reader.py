import json, sys
from pathlib import Path
raw = Path(sys.argv[1]).read_bytes()
if not raw.startswith(b"TEXT\n"):
    raise SystemExit(3)
print(json.dumps(json.loads(raw[5:]), sort_keys=True))
