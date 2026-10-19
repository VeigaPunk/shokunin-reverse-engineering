# proposed-verify-key-resolved — patch-text addendum for `.ufo/gates/custody-pair/custody-pair.py`

Authored by SEAT EX-25 (chain c3, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — the real target is EX-21's write path.

Measured against the frozen baseline
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` and the
distinct-path patch applied to a scratch copy (`63e67631…`). Evidence:
`out/before/attacks.out` A3/A4, `out/candidate/attacks.out` A3/A4,
fixtures `dupe5-bad-second-pre.txt`, `dupe5-bad-last-pre.txt`,
`spelling5-one-path-pre.txt`.

## The residual (measured, pre-existing — NOT introduced by the distinct-path fix)

`verify_sets()` keys both sides by the **raw path string**:

```python
ref_by = {s["path"]: s for s in ref_sections}
cand_by = {s["path"]: s for s in cand_sections}
```

Two consequences, both measured identically on the baseline and on the patched
copy:

| vector | command | result |
|---|---|---|
| 5 stanzas of one path, the 2nd carrying `READ-ERROR` | `verify dupe5-bad-second-pre.txt --live` | **`MATCH exit 0`** — the bad copy is masked by the later clean copies (last-wins) |
| the same, bad copy **last** | `verify dupe5-bad-last-pre.txt --live` | `UNEVALUABLE exit 14` |
| 5 lexical spellings of one path | `verify spelling5-one-path-pre.txt --live` | exit 13, `ABSENT=3 MATCH=2` — three spellings read ABSENT against the live filesystem although all five resolve to one existing file |

The distinct-path coverage fix does **not** repair this: the gate now refuses a
padded reference *when the flag is passed*, but a flag-absent run still reads the
raw-string rows. This is a *verification* defect, not a coverage defect, so it is
filed here rather than folded into the coverage patch.

## Change (key by resolved identity, and detect duplicate stanzas)

```python
# custody-pair.py, verify_sets()
-    ref_by = {s["path"]: s for s in ref_sections}
-    cand_by = {s["path"]: s for s in cand_sections}
-    rows = []
-    for path in list(ref_by) + [p for p in cand_by if p not in ref_by]:
+    def _rkey(s: dict) -> str:
+        return str(Path(s["path"]).expanduser().resolve())
+
+    def _dupes(sections: list, side: str, name: str) -> list:
+        seen: dict = {}
+        notes = []
+        for s in sections:
+            k = _rkey(s)
+            if k in seen:
+                notes.append("DUPLICATE-STANZA: %s lists %s more than once (%s)" % (name, s["path"], side))
+            seen[k] = s
+        return notes
+
+    ref_by = {_rkey(s): s for s in ref_sections}
+    cand_by = {_rkey(s): s for s in cand_sections}
+    rows = []
+    for path in list(ref_by) + [p for p in cand_by if p not in ref_by]:
```

and print the duplicate notes as a declared class (severity ≥ METADATA-DRIFT,
so a padded reference can never read a bare `MATCH` even flag-absent):

```python
+    for note in _dupes(ref_sections, "reference", a_name) + _dupes(cand_sections, "candidate", b_name):
+        print("    note: %s" % note)
```

Design notes for the implementer:

- `_rkey` is the same basis as the (patched) `reference_coverage`, so the gate
  and the comparison stop disagreeing about what "a path" is.
- The duplicate-stanza note is the *declared class* half of the r3 residual
  "coverage gate counts stanzas, not distinct paths": even a caller who never
  passes `--require-paths` sees that the reference is padded, which closes the
  opt-in gap for this specific shape without changing the flag contract.
- Keep the printed `PATH <path>` spelling as the receipt wrote it (operator
  recognisability); only the key changes.
- If the parent prefers a smaller step, ship `_rkey` alone (fixes the spelling
  ABSENT shape and the last-wins masking across spellings) and leave the
  duplicate note as a follow-up.

## Selftest vectors to add with the change

```
case duplicate-stanza-in-reference-is-declared      # padded reference -> note + non-MATCH
case spelling-aliases-resolve-to-one-path           # 5 spellings -> 1 row, MATCH
```

Fixture-only (scratch dir); never touches a custody path.
