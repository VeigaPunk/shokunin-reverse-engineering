#!/usr/bin/env python3
"""Fake TEXT reader used only for the isolated mutation lifecycle, never ELF."""
import json
from pathlib import Path
import sys


def read_text_fixture():
    file_name, version_name = Path(sys.argv[1]).read_text(encoding='ascii').strip().split('|')
    return {'schema': 1, 'needed': [{'file': file_name, 'versions': [
        {'name': version_name, 'flags': 0, 'other': 2, 'hash': 1}]}]}


print(json.dumps({'needed': [], 'schema': 1}, sort_keys=True, separators=(',', ':')))
