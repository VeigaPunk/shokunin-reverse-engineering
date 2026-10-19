# proposed-hardlink-inode-key — patch-text addendum for `.ufo/gates/custody-pair/custody-pair.py`

Authored by SEAT EX-25 (chain c3, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — the real target is EX-21's write path. This is an
*addendum* to `arc3-loop1-round3/claims/c2/EX-24/proposed-coverage-count.patch.md`,
not a replacement.

Measured against the frozen baseline
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` and against
that patch text applied to a scratch copy
(`63e67631f6dd5be2730823040181c409011f93347a9fc3047a16a9706df581bb`).
Evidence: `out/before/attacks.out` A1/A2, `out/candidate/attacks.out` A1/A2,
fixture `fixtures/hardlink5-pre.txt`.

## The residual (measured, reproducible in 2 commands)

```
python3 tools/before/custody-pair.py capture --out /var/tmp/x/hl5.txt --paths \
    /var/tmp/x/hl-0 /var/tmp/x/hl-1 /var/tmp/x/hl-2 /var/tmp/x/hl-3 /var/tmp/x/hl-4
python3 tools/before/custody-pair.py verify /var/tmp/x/hl5.txt --live --require-paths 5
```

with `hl-1 … hl-4` hardlinks of `hl-0`: **exit 0, `MATCH 5/5`, no coverage line**
(both revisions). The receipt is tool-produced — no field is forged; it simply
names five hardlink names for one inode. The r3 patch text's own wording is
"distinct **resolved paths**", and `Path.resolve()` does collapse spelling and
symlinks (A3/A12) but **not hardlinks** — so the unit is still "path name", not
"file".

## Change (one key-set swap)

```python
# custody-pair.py, reference_coverage()
-    have = {Path(s["path"]).expanduser().resolve() for s in ref_sections}
-    unaccounted = [p for p in CUSTODY_PATHS if Path(p).expanduser().resolve() not in have]
-    line = ("REFERENCE-COVERAGE: %d/%d paths present in reference; unaccounted: %s"
-            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
-    return len(have) >= required, line
+    def _key(p: Path) -> tuple:
+        """Distinct-file key: (st_dev, st_ino) when the path stats, else the
+        resolved name (a missing path cannot alias a present one)."""
+        try:
+            st = os.stat(p)
+            return ("ino", st.st_dev, st.st_ino)
+        except OSError:
+            return ("name", str(p.resolve()))
+
+    have = {_key(Path(s["path"]).expanduser()) for s in ref_sections}
+    unaccounted = [p for p in CUSTODY_PATHS
+                   if _key(Path(p).expanduser()) not in have]
+    line = ("REFERENCE-COVERAGE: %d/%d distinct files present in reference; unaccounted: %s"
+            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
+    return len(have) >= required, line
```

Notes for the implementer:

- `os.stat` (not `lstat`) is the deliberate choice for the **alias** question —
  a symlink and its target are one file for coverage purposes, matching the
  write-guard's `_same_file` inode arm.
- A **hardlink to a custody path** then also stops being able to pad the gate
  (`~/.bashrc` vs a hardlink of it collapse to one key), which is the same
  boundary the write guard already refuses (`refuses-to-write-over-scoped-path`,
  selftest case 17).
- The `unaccounted:` list stays in canonical-path spelling, so the operator-
  facing text is unchanged apart from the `distinct files` wording.
- Cost: one `stat` per stanza — the tool already `lstat`s every path it captures,
  so this is within the existing cost envelope.

## Selftest vector to add with the change

```
case coverage-gate-rejects-hardlink-padding  # 5 hardlinks of one file, --require-paths 5 -> exit 2
```

Fixture-only (scratch dir); never touches a custody path. Sibling vector in
`arc3-loop1-round3/claims/c2/EX-24/proposed-coverage-count.patch.md`
(`coverage-gate-rejects-duplicate-stanzas`, `coverage-gate-passes-distinct-five`).
