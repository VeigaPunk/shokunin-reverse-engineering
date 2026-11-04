#!/bin/sh
# Cheapest rule that meets the R85-C1 target: path-in-predicate + negation (none excluded).
# Inputs: F1.json F2.json R84.json (blobs at 91eeb72f). Run in this directory.
for f in F1 F2 R84; do
  if ! grep -qE '"predicate": "[^"]*(tools|corpus|\.ufo)/[^"]*\.(py|sh|mjs|js)' $f.json; then echo "$f FLAGGED PB_NO_PREDICATE_PATH"
  elif grep -qE '"predicate": "[^"]*\b(not|no|never|without|neither|nor|cannot)\b' $f.json; then echo "$f FLAGGED PB_PREDICATE_NEGATED"
  else echo "$f CLEAN"; fi
done
echo "--- same rule with none in the negation list:"
for f in F1 F2 R84; do
  if ! grep -qE '"predicate": "[^"]*(tools|corpus|\.ufo)/[^"]*\.(py|sh|mjs|js)' $f.json; then echo "$f FLAGGED NO_PATH"
  elif grep -qE '"predicate": "[^"]*\b(not|no|never|without|neither|nor|cannot|none)\b' $f.json; then echo "$f FLAGGED NEGATED"
  else echo "$f CLEAN"; fi
done
