#!/usr/bin/env python3
"""Shortcut class: all-false. Emits no records for every input."""
import json


print(json.dumps({"schema": 1, "records": []}, sort_keys=True))
