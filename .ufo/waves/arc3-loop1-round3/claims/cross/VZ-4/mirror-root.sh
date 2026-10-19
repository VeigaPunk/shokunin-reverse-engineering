#!/bin/bash
# VZ-4 command-A tree mirror — builds a scratch root whose command-A read set
# (corpus/knowledge/*.md, corpus/README.md, SKILL.md) mirrors the live worktree,
# so a patch text can be applied to a COPY and scored before anything lands.
# usage: mirror-root.sh <repo> <dest>            # build/refresh mirror
#        mirror-root.sh <repo> <dest> --apply <patch>   # apply a git-style patch
set -eu
REPO=$(readlink -f "$1"); DEST=$2; shift 2
mkdir -p "$DEST/corpus/knowledge"
# real copies (not symlinks): `patch` refuses symlinked targets
for f in "$REPO"/corpus/knowledge/*.md; do
  cp -L "$f" "$DEST/corpus/knowledge/$(basename "$f")"
done
cp -L "$REPO/corpus/README.md" "$DEST/corpus/README.md"
cp -L "$REPO/SKILL.md" "$DEST/SKILL.md"
if [ "${1:-}" = "--apply" ]; then
  patch=$2
  ( cd "$DEST" && patch -p1 --dry-run < "$patch" && patch -p1 < "$patch" )
fi
echo "mirror: $DEST (knowledge files: $(ls "$DEST/corpus/knowledge" | wc -l))"