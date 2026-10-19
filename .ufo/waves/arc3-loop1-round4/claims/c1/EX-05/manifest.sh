#!/usr/bin/env bash
# manifest.sh — seat EX-05 (chain c1, arc3-loop1-round4).
# Regenerates manifest.sha256.txt over every file in this seat's directory
# (excluding the manifest and its verify output), then re-derives it with
# sha256sum -c into manifest-verify.txt (rule #14: the quoted number must be
# the one re-derived after the last write).
set -eu
SEAT="$(cd "$(dirname "$0")" && pwd)"
cd "$SEAT"
rm -f manifest.sha256.txt manifest-verify.txt
find . -type f ! -name 'manifest.sha256.txt' ! -name 'manifest-verify.txt' | LC_ALL=C sort | sed 's|^\./||' > /var/tmp/ex05-r4/manifest-files.txt
while IFS= read -r f; do sha256sum "$f"; done < /var/tmp/ex05-r4/manifest-files.txt > manifest.sha256.txt
{
  echo "# manifest-verify — seat EX-05 arc3-loop1-round4"
  echo "# generated: $(date -Is)   files: $(wc -l < manifest.sha256.txt)"
  echo "# manifest sha256: $(sha256sum manifest.sha256.txt | cut -d' ' -f1)"
  echo "# command: sha256sum -c manifest.sha256.txt"
  sha256sum -c manifest.sha256.txt
} > manifest-verify.txt
tail -2 manifest-verify.txt
