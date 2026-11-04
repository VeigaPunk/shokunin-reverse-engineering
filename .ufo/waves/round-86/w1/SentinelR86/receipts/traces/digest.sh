#!/usr/bin/env bash
# metadata+size digest of the lane tree, excluding .git/.jj and the seat's own w1 dir (sibling writes)
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
find "$L" \( -path "$L/.git" -o -path "$L/.jj" -o -path "$L/.ufo/waves/round-86/w1" \) -prune -o -printf '%p\t%s\t%T@\t%i\n' | LC_ALL=C sort | sha256sum | cut -d' ' -f1
