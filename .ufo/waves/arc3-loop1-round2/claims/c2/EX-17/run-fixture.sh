#!/bin/bash
# usage: run-fixture.sh <instrument.py> <root> <outfile>
inst="$1"; root="$2"; out="$3"
{
  echo "\$ python3 $(basename "$inst") --root $root --quiet"
  python3 "$inst" --root "$root" --quiet 2>&1
  echo "exit=$?"
  echo "--- instrument sha256: $(sha256sum "$inst" | cut -d' ' -f1)"
} > "$out"
