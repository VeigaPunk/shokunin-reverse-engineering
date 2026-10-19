#!/bin/bash
# VZ-3 independent custody capture (read-only: stat + sha256 only).
# Usage: vz3-independent-capture.sh [path ...]   (default: none -> exits 2)
# Emits one block per path: sha256, size, mtime epoch, mtime UTC ISO, ctime epoch,
# ctime UTC ISO, inode, mode. Local-time rendering is shown separately, never
# under a UTC label (the v1 label defect is checked here by construction).
set -u
if [ "$#" -eq 0 ]; then echo "usage: $0 <path>..." >&2; exit 2; fi
for p in "$@"; do
  if [ ! -e "$p" ]; then echo "PATH: $p"; echo "EXISTS: no"; continue; fi
  sha=$(sha256sum "$p" | cut -d' ' -f1)
  read -r size ino mode mepoch cepoch <<<"$(stat -c '%s %i %a %Y %Z' "$p")"
  mutc=$(date -u -d "@$mepoch" +%Y-%m-%dT%H:%M:%SZ)
  cutc=$(date -u -d "@$cepoch" +%Y-%m-%dT%H:%M:%SZ)
  mlocal=$(date -d "@$mepoch" +'%Y-%m-%d %H:%M:%S')
  echo "PATH: $p"
  echo "EXISTS: yes"
  echo "SIZE: $size  MODE: $mode  INODE: $ino"
  echo "SHA256: $sha"
  echo "MTIME_EPOCH: $mepoch"
  echo "MTIME_UTC: $mutc"
  echo "CTIME_EPOCH: $cepoch"
  echo "CTIME_UTC: $cutc"
  echo "MTIME_LOCAL(-03, informational only, never a UTC label): $mlocal"
done
