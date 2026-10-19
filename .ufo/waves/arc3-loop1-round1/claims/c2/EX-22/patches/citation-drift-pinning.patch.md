# EX-22 — patch text: citation-drift pinning hardening (NOT applied)

Seat EX-22 | chain c2 | executor | 2026-10-19 | HEAD `e845c2b`
Owner: `.ufo/gates/citation-drift/` is **EX-16's** real target. Nothing here was
applied or committed; everything was measured on scratch copies under
`/var/tmp/ex22`. Shape: EX-23's reference recipe (`guard-recipe.patch.md`) plus
the pinning-correctness hardening analysed in `../pinning-analysis.md` §1–§5.

## Landing notes (read first)

1. **Two files, one commit.** The pin and the guard land together; a revision
   with the guard but no pin reads `unpinned_legacy` exit 2 for every run
   (EX-23 W2). The pin value below is the digest of the table as committed at
   `e845c2b`; re-measure with `sha256sum .ufo/gates/citation-drift/pointer-table.json`
   if the table changes before landing.
2. **Pin value:** `frozen_run.table_sha256 =
   738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`.
3. **Findings classes emitted:** `pointer_table_tampered` (digest mismatch),
   `unpinned_legacy` (no pin), `pointer_table_unreadable` (absent / undecodable
   / non-regular), `pointer_table_unsafe` (symlink). All exit 2 in both
   semantics; all registered in the CNE tuple.
4. **Verify after applying:** `--selftest` → `cases=13 passed=13 failed=0 exit=0`
   (run with `TMPDIR` on a filesystem with room — `/tmp` is quota-blocked this
   wave); live run at HEAD with the pinned expected → `findings=0 exit=0`;
   `patch -p1 --dry-run` verified OK from a repo-shaped tree.
5. **Differs from EX-23's recipe** in five places — see `../pinning-analysis.md`
   §7. The one census row that shifts: EX-23's C9 (non-UTF8 table) reads
   `pointer_table_tampered` here instead of `pointer_table_unreadable`; the C6
   and C8 rows keep their measured ids. EX-16 may fold `pointer_table_unsafe`
   to `pointer_table_unreadable` if zero new ids beyond the claim are wanted.

## Diff 1 — `.ufo/gates/citation-drift/citation-drift-probe.py`

sha256 of the raw diff: `ea60e0bbb3680e2bd9fd6ec554f0e42f2cdfcd37ba783e1b286dc1a8ae227d61`
(raw copy: `../evidence/probe.repo.patch.diff`; patched-file sha256
`93f2bead2ef20090dfc2a72ad33081c738df23bc076115645993bc6cac6bf017`)

```diff
--- a/.ufo/gates/citation-drift/citation-drift-probe.py
+++ b/.ufo/gates/citation-drift/citation-drift-probe.py
@@ -31,6 +31,15 @@
                            against expected.json `snapshots` (a mismatched
                            snapshot is `snapshot_tampered`, exit 2).
 
+PINNING  expected.json `frozen_run.table_sha256` pins the exact on-disk bytes
+         of the table (`sha256sum` of the file: no newline translation, no
+         re-encode). The table is read once, in binary; that same bytes object
+         is both hashed and parsed. A mismatch is `pointer_table_tampered`
+         (exit 2) before any entry is evaluated; a missing pin is
+         `unpinned_legacy`; an absent, undecodable or non-regular table is
+         `pointer_table_unreadable`; a symlinked table is `pointer_table_unsafe`
+         -- all exit 2, never silent findings.
+
 VERDICT  exit 0 clean, 1 failed, 2 could-not-evaluate. Every finding carries a
 stable id so the self-test can assert on it.
 
@@ -40,11 +49,13 @@
   citation-drift-gate.py --selftest [--expected PATH]
 """
 import argparse
+import errno
 import hashlib
 import json
 import os
 import re
 import shutil
+import stat
 import subprocess
 import sys
 import tempfile
@@ -70,7 +81,8 @@
         if not self.rows:
             return CLEAN
         if any(f in ("snapshot_tampered", "snapshot_missing",
-                     "pointer_table_unreadable", "unpinned_legacy",
+                     "pointer_table_unreadable", "pointer_table_tampered",
+                     "pointer_table_unsafe", "unpinned_legacy",
                      "root_unreadable", "revision_unresolvable", "internal_error")
                for f, _, _ in self.rows):
             return CNE
@@ -88,6 +100,40 @@
     return hashlib.sha256(data).hexdigest()
 
 
+class TableUnsafe(Exception):
+    """The table path is a symlink: refused (identity, not content)."""
+
+
+def read_table_bytes(path):
+    """Read the pointer table EXACTLY ONCE. The bytes returned are the bytes
+    hashed and the bytes parsed, so no window exists in which the file can
+    change between the pin check and its use (hash one read, parse another is
+    measurably racy). The open refuses to follow a symlink (O_NOFOLLOW) and
+    refuses non-regular files (FIFO/device/directory); O_NONBLOCK keeps a FIFO
+    from blocking the open before that check can run. Never raises; returns
+    (bytes, error), the error being a TableUnsafe for a symlink refusal (the
+    non-regular refusal stays in the unreadable class the census measured)."""
+    try:
+        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
+    except OSError as exc:
+        if exc.errno == errno.ELOOP:
+            return None, TableUnsafe("refused: %s is a symlink (O_NOFOLLOW)" % path)
+        return None, exc
+    try:
+        st = os.fstat(fd)
+        if not stat.S_ISREG(st.st_mode):
+            return None, "refused: %s is not a regular file (mode %o)" % (path, st.st_mode)
+        fh = os.fdopen(fd, "rb")
+        fd = -1
+        with fh:
+            return fh.read(), None
+    except OSError as exc:
+        return None, exc
+    finally:
+        if fd >= 0:
+            os.close(fd)
+
+
 def git_show(root, rev, path):
     """Return (text, error). Never raises."""
     proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
@@ -277,16 +323,39 @@
         findings.add("revision_unresolvable", rev,
                      "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
         return findings
+    # expected.json first: it carries the frozen-run pin, and the table bytes
+    # are read ONCE (hash == parse) so no window exists between the check and
+    # its use
     try:
-        table = json.load(open(table_path))
-    except (OSError, ValueError) as exc:
-        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
-        return findings
-    try:
-        expected = json.load(open(expected_path))
-    except (OSError, ValueError) as exc:
+        with open(expected_path, "rb") as fh:
+            expected = json.loads(fh.read().decode("utf-8"))
+    except (OSError, ValueError, UnicodeDecodeError) as exc:
         expected = {}
         findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+    data, err = read_table_bytes(table_path)
+    if err:
+        findings.add("pointer_table_unsafe" if isinstance(err, TableUnsafe)
+                     else "pointer_table_unreadable",
+                     os.path.basename(table_path), str(err))
+        return findings
+    # frozen-run guard: the table is the contract, so its bytes are pinned in
+    # expected.json. The run cannot tell an honest in-flight re-key from a
+    # tamper, so a digest mismatch is could-not-evaluate, never a finding set.
+    pinned = (expected.get("frozen_run") or {}).get("table_sha256")
+    if pinned is None:
+        findings.add("unpinned_legacy", os.path.basename(table_path),
+                     "no table digest pinned in expected.json")
+        return findings
+    if sha256_bytes(data) != pinned:
+        findings.add("pointer_table_tampered", os.path.basename(table_path),
+                     "sha256 %s != pinned %s (a table edit and its re-pin land "
+                     "in the same commit)" % (sha256_bytes(data), pinned))
+        return findings
+    try:
+        table = json.loads(data.decode("utf-8"))
+    except (ValueError, UnicodeDecodeError) as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
     for entry in table.get("entries", []):
         check_entry(entry, tree, findings)
@@ -396,6 +465,9 @@
                     table = os.path.join(case_dir, "table.json")
                     open(table, "w").write("{ not json")
                     root = build_fixture("clean")
+                elif case == "table_absent":
+                    table = os.path.join(case_dir, "no-such-table.json")
+                    root = build_fixture("clean")
                 else:
                     root = build_fixture(case)
                     table = os.path.join(case_dir, "table.json")
@@ -412,7 +484,17 @@
                     digests = {"external.cfg": "0" * 64}
                 else:
                     digests = {}
-                expected = {"snapshots": digests}
+                # every fixture run pins the digest of the table it was built
+                # with, so the guard stays universal; an unpinned run is the
+                # declared unpinned_legacy class (exit 2)
+                if case == "table_tampered":
+                    table_pin = "0" * 64
+                elif case == "table_absent":
+                    table_pin = sha256_bytes(b"absent on purpose")
+                else:
+                    table_pin = sha256_bytes(open(table, "rb").read())
+                expected = {"snapshots": digests,
+                            "frozen_run": {"table_sha256": table_pin}}
                 exp_file = os.path.join(case_dir, "expected.json")
                 json.dump(expected, open(exp_file, "w"))
 
```

## Diff 2 — `.ufo/gates/citation-drift/expected.json`

sha256 of the raw diff: `50326b8505c3c74face6b15d7b9e914a8243e6ebb2bdbb19560d027e8636d433`
(raw copy: `../evidence/expected.repo.patch.diff`; patched-file sha256
`663be45d60c5d95659e6ca2705c1c02f66741554841ff90996f4bc9a1840f89a`)

```diff
--- a/.ufo/gates/citation-drift/expected.json
+++ b/.ufo/gates/citation-drift/expected.json
@@ -1 +1 @@
-{"_doc": "Committed expected values for the citation-drift gate. Per the PROTOCOL Gate standard: the frozen-run baseline pins the digest of every snapshot input file, and the self-test's expected exit codes and finding ids live here rather than in the script, so the expected values are independent of the recomputation.", "frozen_run": {"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "note": "the revision the committed verdict was measured against; a run over a different revision is a different measurement", "verdict": "failed", "expected_findings": ["citation_dead"]}, "snapshots": {"config-toml-landmarks": "387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154"}, "selftest": [{"case": "clean", "exit_code": 0, "finding": "citations_clean"}, {"case": "dead", "exit_code": 1, "finding": "citation_dead"}, {"case": "out_of_range", "exit_code": 1, "finding": "citation_out_of_range"}, {"case": "file_absent", "exit_code": 1, "finding": "citation_file_absent"}, {"case": "moved", "exit_code": 1, "finding": "citation_moved"}, {"case": "stamped", "exit_code": 0, "finding": "citation_historical_ok"}, {"case": "no_snapshot_dir", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "snapshot_missing", "exit_code": 2, "finding": "snapshot_missing"}, {"case": "snapshot_tampered", "exit_code": 2, "finding": "snapshot_tampered"}, {"case": "table_unreadable", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "rev_unresolvable", "exit_code": 2, "finding": "revision_unresolvable"}]}
\ No newline at end of file
+{"_doc": "Committed expected values for the citation-drift gate. Per the PROTOCOL Gate standard: the frozen-run baseline pins the digest of every snapshot input file, and the self-test's expected exit codes and finding ids live here rather than in the script, so the expected values are independent of the recomputation.", "frozen_run": {"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "note": "the revision the committed verdict was measured against; a run over a different revision is a different measurement", "verdict": "failed", "expected_findings": ["citation_dead"], "table_sha256": "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f", "table_sha256_note": "the frozen-run guard: the exact on-disk bytes of pointer-table.json, measured with `sha256sum` (no newline translation, no re-encode); an edit to the table and its re-pin land in the same commit"}, "snapshots": {"config-toml-landmarks": "387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154"}, "selftest": [{"case": "clean", "exit_code": 0, "finding": "citations_clean"}, {"case": "dead", "exit_code": 1, "finding": "citation_dead"}, {"case": "out_of_range", "exit_code": 1, "finding": "citation_out_of_range"}, {"case": "file_absent", "exit_code": 1, "finding": "citation_file_absent"}, {"case": "moved", "exit_code": 1, "finding": "citation_moved"}, {"case": "stamped", "exit_code": 0, "finding": "citation_historical_ok"}, {"case": "no_snapshot_dir", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "snapshot_missing", "exit_code": 2, "finding": "snapshot_missing"}, {"case": "snapshot_tampered", "exit_code": 2, "finding": "snapshot_tampered"}, {"case": "table_unreadable", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "rev_unresolvable", "exit_code": 2, "finding": "revision_unresolvable"}, {"case": "table_tampered", "exit_code": 2, "finding": "pointer_table_tampered"}, {"case": "table_absent", "exit_code": 2, "finding": "pointer_table_unreadable"}]}
\ No newline at end of file
```

Note: the file has no trailing newline today; the patch preserves that (the
`\ No newline at end of file` markers are intentional and match the raw diff).

## Optional, beyond the frozen claim (do not fold without amending)

A selftest meta-assert so a *deleted pin* fails loudly even though a probe run
classifies it as the declared `unpinned_legacy`:

```python
    # in selftest(), after expected_root is loaded:
    pin = ((expected_root.get("frozen_run") or {}).get("table_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", pin):
        print("SELFTEST_CASE: FAILED case=live_pin_present exit=2 expected=0 "
              "finding=pointer_table_unpinned")
        return 1
```

This would move the selftest count from 13 to 14; the frozen claim says 13, so
it is offered only as a named residual mitigation (`../pinning-analysis.md` §8).
