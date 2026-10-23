from pathlib import Path
import sys
if Path(sys.argv[1]).read_bytes() != b'isolated benign document-binding fixture\n':
    raise SystemExit(3)
print('{"schema":1,"needed":[]}')
