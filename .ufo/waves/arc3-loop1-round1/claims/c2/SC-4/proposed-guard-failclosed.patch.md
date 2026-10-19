# Proposed change (PATCH TEXT — not applied) — SC-4 / chain c2

Candidate landing kit for the C2 claim's guard, assembled by the scribe seat from
EX-21's prototype plus SC-4's fail-closed measurement. **NOT APPLIED to the real
gate by this seat.** EX-16 (the seat that owns `.ufo/gates/citation-drift/`) had
not landed at 07:14; this artifact exists so the parent can land a verified
change instead of an absent one, or hand it to EX-16.

Provenance: EX-21's `tmp/proto/probe.py` (sha
`776cef6af5b7404f6a0d0667727ecf99a6bb32a6db357b443e6fa5c1585ca283`) with the
unpinned branch made fail-closed by SC-4; measured end-to-end in
`claims/c2/SC-4/verify-failclosed.txt`.

Targets: `.ufo/gates/citation-drift/citation-drift-probe.py` (part 1) and
`.ufo/gates/citation-drift/expected.json` (part 2). The pointer table itself is
NOT touched — its bytes are what part 2 pins.

## Part 1 — probe patch (unified diff, applies with `patch -p1` from the repo root)

Verified by SC-4: applying this diff to a pristine `git show HEAD:` copy
reproduces the measured candidate exactly, sha256
`28cc118799a51b5cc56b44a9ee5d468001d7550f40bab19f952399399cd7a7e5`.

```diff
--- a/.ufo/gates/citation-drift/citation-drift-probe.py
+++ b/.ufo/gates/citation-drift/citation-drift-probe.py
@@ -70,7 +70,9 @@
         if not self.rows:
             return CLEAN
         if any(f in ("snapshot_tampered", "snapshot_missing",
-                     "pointer_table_unreadable", "unpinned_legacy",
+                     "pointer_table_unreadable", "pointer_table_tampered",
+                     "table_pin_absent",
+                     "unpinned_legacy",
                      "root_unreadable", "revision_unresolvable", "internal_error")
                for f, _, _ in self.rows):
             return CNE
@@ -278,15 +280,25 @@
                      "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
         return findings
     try:
-        table = json.load(open(table_path))
-    except (OSError, ValueError) as exc:
-        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
-        return findings
-    try:
         expected = json.load(open(expected_path))
     except (OSError, ValueError) as exc:
         expected = {}
         findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+    try:
+        table_bytes = open(table_path, "rb").read()
+        table = json.loads(table_bytes)
+    except (OSError, ValueError) as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
+    pinned_table = expected.get("table_sha256")
+    if pinned_table is None:
+        findings.add("table_pin_absent", os.path.basename(table_path),
+                     "expected.json pins no table digest (fail-closed)")
+        return findings
+    if sha256_bytes(table_bytes) != pinned_table:
+        findings.add("pointer_table_tampered", os.path.basename(table_path),
+                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pinned_table))
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
     for entry in table.get("entries", []):
         check_entry(entry, tree, findings)
@@ -392,14 +404,29 @@
         with tempfile.TemporaryDirectory(prefix="citation-drift-case-") as case_dir:
             root = None
             try:
-                if case == "table_unreadable":
-                    table = os.path.join(case_dir, "table.json")
-                    open(table, "w").write("{ not json")
+                if case in ("table_absent", "table_tampered", "table_unreadable"):
                     root = build_fixture("clean")
                 else:
                     root = build_fixture(case)
-                    table = os.path.join(case_dir, "table.json")
-                    json.dump(fixture_table(case), open(table, "w"))
+                table = os.path.join(case_dir, "table.json")
+                if case == "table_absent":
+                    # pin the digest of the table that is never written
+                    table_bytes = None
+                    pinned_digest = sha256_bytes(
+                        json.dumps(fixture_table("clean")).encode())
+                elif case == "table_tampered":
+                    # pin the honest digest, then write different bytes
+                    good = json.dumps(fixture_table("clean")).encode()
+                    pinned_digest = sha256_bytes(good)
+                    table_bytes = good + b" "
+                elif case == "table_unreadable":
+                    table_bytes = b"{ not json"
+                    pinned_digest = sha256_bytes(table_bytes)
+                else:
+                    table_bytes = json.dumps(fixture_table(case)).encode()
+                    pinned_digest = sha256_bytes(table_bytes)
+                if table_bytes is not None:
+                    open(table, "wb").write(table_bytes)
 
                 snapshot_dir = os.path.join(case_dir, "snap")
                 os.makedirs(snapshot_dir)
@@ -412,7 +439,7 @@
                     digests = {"external.cfg": "0" * 64}
                 else:
                     digests = {}
-                expected = {"snapshots": digests}
+                expected = {"snapshots": digests, "table_sha256": pinned_digest}
                 exp_file = os.path.join(case_dir, "expected.json")
                 json.dump(expected, open(exp_file, "w"))
 
```

Semantics this patch lands: pin key `expected.json["table_sha256"]`; the guard
runs after `expected.json` is read and before any entry is evaluated; an absent
pin is `table_pin_absent` (fail-closed, exit 2 in both modes); a digest mismatch
is `pointer_table_tampered` (exit 2 in both modes); an absent/unreadable table
keeps the pre-existing `pointer_table_unreadable` (exit 2); the guard hashes the
table path that is actually loaded, so `--table <other>` cannot bypass it.

## Part 2 — expected.json

Two edits, both append-style (no existing value changes):

1. add top-level `"table_sha256": "<sha256 of pointer-table.json at landing>"`;
2. append to `selftest`:
   `{"case": "table_tampered", "exit_code": 2, "finding": "pointer_table_tampered"}`
   and
   `{"case": "table_absent", "exit_code": 2, "finding": "pointer_table_unreadable"}`.

Resulting file, constructed by SC-4 from the pristine `expected.json` plus these
two edits: 1776 bytes, sha256
`376f9fc54fd5af22e77f0eda1b317905760ffe14b48f176feb1feb130160170f` — byte-identical
to EX-21's own 13-case `expected.json` as fingerprinted in
`claims/c2/SC-4/verify-proto.txt` at 07:05:55, so the case table is EX-21's
design, not an SC-4 invention. With the table unchanged
(`738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`) the pin
value is that digest; if any later edit changes the table, recompute the pin in
the same commit.

## Part 3 — acceptance run (candidate gate dir, default paths)

Evidence: `claims/c2/SC-4/verify-failclosed.txt` and `verify-proto.txt`;
reproduce with `bash claims/c2/SC-4/verify-failclosed.sh`.

| # | Run | Result |
|---|---|---|
| 1 | `citation-drift-probe.py --selftest` | `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0` |
| 2 | `--root <repo> --rev HEAD` (default table/expected) | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` |
| 3 | `--table <emptied table>` | `pointer_table_tampered … exit=2` |
| 4 | `--expected <expected.json without the pin>` | `table_pin_absent … exit=2` |
| 5 | `--table <absent path>` | `pointer_table_unreadable … exit=2` |

## Part 4 — what this kit does not do

- It does not touch `pointer-table.json`, the corpus, SKILL.md, SCORECARD.md or
  LOG.md (those are other seats' patch texts / the parent's records).
- It does not fix the residual limit that `expected.json` carries no self-digest:
  a same-privilege writer can still co-mutate the pin, forge `--expected`, or
  edit the probe (EX-24 T2/T5/T6). Fail-closed only closes the one-field-deletion
  hole.
- It does not name `table_pin_absent` in EX-20's row text; the row's "unpinned"
  clause is generic, so the row applies as written with this shape (with the
  `table_tampered` → `pointer_table_tampered` substitution from
  `changeset.md` §5.1).
