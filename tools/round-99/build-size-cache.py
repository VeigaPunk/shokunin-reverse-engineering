#!/usr/bin/env python3
"""build-size-cache.py - round-99 helper for forgery g5-size-cache.

Packs every pinned carrier of tools/round-99/pe-upx-trunc-battery.py with the
battery's own command (`upx --best -q -f`) and stores the pristine pack as
<cache>/<size>.upx, the strongest size-keyed cache an attacker who knows the
pinned population can hold.  Usage: build-size-cache.py --cache <dir>
"""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("battery", os.path.join(HERE, "pe-upx-trunc-battery.py"))
    bat = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bat)
    os.makedirs(a.cache, exist_ok=True)
    for name, src, _pin in bat.CARRIERS:
        tmp = os.path.join(a.cache, name + ".orig")
        shutil.copyfile(src, tmp)
        out = os.path.join(a.cache, name + ".pack")
        subprocess.run(["/usr/bin/upx", "--best", "-q", "-f", "-o", out, tmp], check=True,
                       capture_output=True)
        os.replace(out, os.path.join(a.cache, "%d.upx" % os.path.getsize(out)))
        os.unlink(tmp)
        print(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
