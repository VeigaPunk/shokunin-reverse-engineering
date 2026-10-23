#!/usr/bin/env python3
"""Degenerate comparison baseline: always print the empty version-needs record.

This is NOT the CtlHashReplay control. It exists only as a comparison
baseline so the report can attribute the counter's matched count: the
aggregate count alone does not distinguish a hash-replay reader (which matches
the original schedule on eleven carriers) from a reader that always prints the
empty record (which matches nothing but the empty carrier). The per-row
schedule detail does distinguish them.
"""
import json
import sys

sys.stdout.write(json.dumps({"schema": 1, "needed": []}, sort_keys=True))
