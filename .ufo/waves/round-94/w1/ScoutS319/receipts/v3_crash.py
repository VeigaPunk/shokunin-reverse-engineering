import json, io
receipt = {"exit": 0, "fresh_cells": [{"output": b"\x00\x01"}]}
try:
    json.dump(receipt, io.StringIO(), indent=1, sort_keys=True)
    print("NO-ERROR")
except TypeError as e:
    print("TypeError:", str(e))
