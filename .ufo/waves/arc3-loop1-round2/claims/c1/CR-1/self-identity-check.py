#!/usr/bin/env python3
"""Rule-#14 discipline, mechanized: re-derive an artifact's byte-identity and
compare it against the identity the artifact declares about itself.

usage: self-identity-check.py <file> <declared_sha256> <declared_bytes> <declared_lines>
exit 0 = FRESH, 1 = STALE (any field disagrees), 2 = unusable input.
"""
import hashlib
import pathlib
import sys

def main(argv):
    if len(argv) != 5:
        print(__doc__)
        return 2
    path, want_sha, want_bytes, want_lines = argv[1], argv[2].lower(), int(argv[3]), int(argv[4])
    data = pathlib.Path(path).read_bytes()
    got_sha = hashlib.sha256(data).hexdigest()
    got_bytes = len(data)
    got_lines = data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)
    fresh = (got_sha == want_sha) and (got_bytes == want_bytes) and (got_lines == want_lines)
    print(f"declared: sha256={want_sha[:16]}… bytes={want_bytes} lines={want_lines}")
    print(f"derived : sha256={got_sha[:16]}… bytes={got_bytes} lines={got_lines}")
    print("VERDICT: FRESH" if fresh else "VERDICT: STALE — declared identity does not describe the artifact")
    return 0 if fresh else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
