#!/usr/bin/env python3
"""Locate the S252 anchor quote in the served mknod(2) bytes (offline, no network)."""
import html
import re
import sys

BODY = "mknod.2.stdout.html"

# The gate quote as it appears in the anchor cell (25 words).
QUOTE = ("other than a regular file, FIFO (named pipe), or UNIX domain socket, "
         "and the caller is not privileged (Linux: does not have the CAP_MKNOD capability)")

# Negative controls: strings that MUST NOT be present.
NEGATIVES = [
    # wrong: drops "the" before CAP_MKNOD -> must be absent from the page
    "does not have CAP_MKNOD capability",
    # wrong: claims the gate covers FIFOs/sockets -> the page says the opposite
    "FIFO (named pipe), or UNIX domain socket, and the caller is privileged",
    # wrong: attributes the gate to root rather than the capability
    "the caller is not root",
]


def main() -> int:
    raw = open(BODY, encoding="utf-8", errors="replace").read()
    plain = re.sub(r"<[^>]+>", " ", raw)
    plain = html.unescape(plain).replace("\xa0", " ")
    plain = re.sub(r"\s+", " ", plain)

    located = QUOTE in plain
    # The quote spans a line break + a <b> tag in the raw HTML, so locate the
    # sentence boundaries in the raw bytes instead of the flat form.
    raw_head = "EPERM  </b><i>mode</i> requested creation of something other than a regular"
    raw_loc = raw_head in raw
    words = len(QUOTE.split())
    sec = 'id="ERRORS"' in raw
    cap = "CAP_MKNOD" in raw
    neg = {n: (n in plain) for n in NEGATIVES}
    neg_ok = not any(neg.values())

    print(f"QUOTE words={words} (limit 25) -> {'OK' if words <= 25 else 'OVER'}")
    print(f"QUOTE located_in_flattened_text={located}")
    print(f"QUOTE located_in_raw_html={raw_loc}")
    print(f"section ERRORS present={sec}")
    print(f"CAP_MKNOD present={cap}")
    print(f"negatives absent={neg_ok} {neg}")
    ok = located and raw_loc and sec and cap and neg_ok and words <= 25
    print("QUOTE_CHECK", "located=1" if ok else "located=0",
          f"missing={0 if ok else 1}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
