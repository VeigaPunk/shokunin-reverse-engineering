# EX-40 — proposed edge-class patch for `custody-pair.py` (patch text, NOT applied)

Seat EX-40 · chain c3 · wave `arc3-loop1-round2`. Apply decision belongs to
EX-31 (the chain's only real-target writer) or the parent integrator — this seat
wrote nothing under `.ufo/gates/custody-pair/`.

- Base (only revision this applies to): `.ufo/gates/custody-pair/custody-pair.py`
  sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
  (889 lines).
- Machine form: `proposed-edge-classes.patch` (11 hunks, 167 lines).
- Apply: `cd <repo root> && patch -p1 < claims/c3/EX-40/proposed-edge-classes.patch`
- Generator (re-derives the diff from the base with asserted anchors):
  `gen-patch.py` — refuses if any anchor is not found exactly once, so a moved
  base cannot silently mis-apply.

## What it changes, and why (each item measured — `edge-cases.md` §1)

1. **New declared class `14 UNEVALUABLE`** (constants + docstring table):
   a path that exists but could not be evaluated. Severity
   `CONTENT-DRIFT(5) > UNEVALUABLE(4) > ABSENT(3) > REWRITE-DRIFT(2) >
   METADATA-DRIFT(1) > MATCH(0)`.
2. **`capture_path` no longer crashes on EACCES** (the measured defect:
   `PermissionError` traceback, exit 1, **no receipt written**, even in a mixed
   set). An unreadable regular file is recorded `EXISTS: yes`, `TYPE: file`,
   `READ-ERROR: <errno>` — the receipt survives, per the tool's own
   "failing closed still leaves the record" spirit.
3. **`cmd_capture` exit computation**: unevaluable count first → exit 14;
   else 0/13 as before. Summary line prints `UNEVALUABLE` instead of `PARTIAL`
   for that class.
4. **`compare_section` fail-closed**: a stanza that exists-but-is-unevaluable
   (either side) returns class `UNEVALUABLE` *before* the both-absent `MATCH`
   branch — this closes the measured fail-open where an EACCES path verified
   `MATCH exit 0`.
5. **`parse_receipt` format tag**: a receipt whose stanzas carry no `mtime_epoch`
   (e.g. all-unevaluable) was mis-tagged `v1-stanza` although it carries
   `# receipt-version: 2`; the tag now honors the header version. Display-only
   (the tag is printed by `cmd_verify`), included for honesty of the "A format:"
   line.
6. **Two selftest cases** (guarded `os.geteuid() == 0` → trivially pass, since
   mode 000 does not block root): `unreadable-path-is-unevaluable` (exit 14,
   `READ-ERROR` in the receipt, `EXISTS: yes`) and `unevaluable-never-matches`
   (capture and verify both 14; `MATCH` must not be printed).

## Proof this patch does what it claims (all scratch, `/var/tmp/ex40`)

```
$ cd /var/tmp/ex40/applytest && patch -p4 --dry-run < …/proposed-edge-classes.patch
checking file custody-pair.py                     # clean
$ patch -p4 < …/proposed-edge-classes.patch
patching file custody-pair.py
$ sha256sum custody-pair.py → 4aedb0307f8313e77f8d3b3cdf6df82e44ba6865748dda2d0fdf572e0cc349e2
  (byte-identical to the generator output custody-pair.patched.py)

$ python3 custody-pair.patched.py selftest --scratch /var/tmp/ex40/selftest-patched
CUSTODY_PAIR_SELFTEST: CLEAN cases=17 passed=17 failed=0 exit=0      # patched-selftest.txt

$ TOOL=<landed>  bash edge-matrix-real.sh   →  MATRIX: FAIL pass=11 fail=6   # before
$ TOOL=<patched> bash edge-matrix-real.sh   →  MATRIX: PASS pass=17 fail=0   # after
```

New behavior on the failing shapes (patched): `unreadable.txt` capture exit 14
with the receipt written (2 stanzas in the aggregate run); `blocked_dir/inner.txt`
capture exit 14; `verify blocked-pre.txt --live` exit 14, no `MATCH` printed.

## Fenced copy of the patch text

<!-- PATCH-TEXT-BELOW -->
```diff
--- a/.ufo/gates/custody-pair/custody-pair.py
+++ b/.ufo/gates/custody-pair/custody-pair.py
@@ -68,15 +68,19 @@
                           epoch/render pair is inconsistent, or a v1 label defect
                           is reproduced (LABEL-DEFECT)
     13  ABSENT            >=1 reference path missing on the candidate side
+    14  UNEVALUABLE       a path exists but could not be evaluated (EACCES on
+                          open, or a stat error other than ENOENT); the receipt
+                          is still written, carrying STAT-ERROR/READ-ERROR
     2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                           or failed write
     3   SELFTEST-FAIL     a selftest case failed
 
     capture exits 0 when every requested path is present (5/5 for the default
-    set) and 13 when >=1 requested path is absent; the receipt is still written.
+    set), 14 when >=1 path is present-but-unevaluable, else 13 when >=1
+    requested path is absent; the receipt is still written.
 
-SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > ABSENT > REWRITE-DRIFT >
-METADATA-DRIFT > MATCH.
+SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > UNEVALUABLE > ABSENT >
+REWRITE-DRIFT > METADATA-DRIFT > MATCH.
 
 v1 COMPATIBILITY. Three v1 receipt shapes are parsed and compared on the fields
 they actually carry (sha256 is the contract):
@@ -121,6 +125,7 @@
 EXIT_REWRITE_DRIFT = 11
 EXIT_METADATA_DRIFT = 12
 EXIT_ABSENT = 13
+EXIT_UNEVALUABLE = 14
 EXIT_USAGE = 2
 EXIT_SELFTEST_FAIL = 3
 
@@ -130,7 +135,8 @@
     "METADATA-DRIFT": 1,
     "REWRITE-DRIFT": 2,
     "ABSENT": 3,
-    "CONTENT-DRIFT": 4,
+    "UNEVALUABLE": 4,
+    "CONTENT-DRIFT": 5,
 }
 EXIT_FOR = {
     "MATCH": EXIT_MATCH,
@@ -138,6 +144,7 @@
     "METADATA-DRIFT": EXIT_METADATA_DRIFT,
     "REWRITE-DRIFT": EXIT_REWRITE_DRIFT,
     "ABSENT": EXIT_ABSENT,
+    "UNEVALUABLE": EXIT_UNEVALUABLE,
     "CONTENT-DRIFT": EXIT_CONTENT_DRIFT,
 }
 
@@ -216,7 +223,10 @@
         fields["sha256"] = hashlib.sha256(target.encode()).hexdigest()
     elif os.path.isfile(path):
         fields["type"] = "file"
-        fields["sha256"] = sha256_file(path)
+        try:
+            fields["sha256"] = sha256_file(path)
+        except OSError as exc:  # exists but not evaluable (e.g. EACCES)
+            fields["read_error"] = "%s" % exc
     else:
         fields["type"] = "other"
     return fields
@@ -269,6 +279,8 @@
             continue
         lines.append("TYPE: %s" % sec.get("type", "other"))
         lines.append("SIZE: %s" % sec.get("size", ""))
+        if sec.get("read_error"):
+            lines.append("READ-ERROR: %s" % sec["read_error"])
         if "sha256" in sec:
             lines.append("SHA256: %s" % sec["sha256"])
         if "symlink_target" in sec:
@@ -355,7 +367,7 @@
             sections.append(sec)
         if not sections:
             raise ValueError("no stanzas parsed from %s" % path)
-        fmt = "v2" if any("mtime_epoch" in s for s in sections) else "v1-stanza"
+        fmt = "v2" if (version >= 2 or any("mtime_epoch" in s for s in sections)) else "v1-stanza"
         return fmt, sections
 
     sections = []
@@ -425,6 +437,14 @@
     ref_exists = ref.get("exists", "no") == "yes" or "sha256" in ref
     cand_exists = cand.get("exists", "no") == "yes" or "sha256" in cand
     comparable = sum(1 for k in COMPARE_KEYS if k in ref and k in cand)
+    ref_uneval = bool(ref.get("stat_error") or ref.get("read_error"))
+    cand_uneval = bool(cand.get("stat_error") or cand.get("read_error"))
+    if ref_uneval or cand_uneval:
+        sides = "+".join(n for n, u in (("reference", ref_uneval), ("candidate", cand_uneval)) if u)
+        return {"finding": "UNEVALUABLE", "moved": ["unevaluable"], "compared": 0,
+                "comparable": comparable,
+                "notes": notes + ["exists but not evaluable on %s side" % sides],
+                "label_findings": label_findings}
     if not ref_exists and not cand_exists:
         return {"finding": "MATCH", "moved": [], "compared": 0, "comparable": 0,
                 "notes": notes, "label_findings": label_findings}
@@ -554,7 +574,15 @@
     now = time.time()
     text = render_receipt(sections, args.label, now)
     present = sum(1 for s in sections if s.get("exists") == "yes")
-    exit_code = EXIT_MATCH if present == len(sections) else EXIT_ABSENT
+    unevaluable = sum(1 for s in sections
+                      if s.get("stat_error") or s.get("read_error")
+                      or (s.get("exists") == "yes" and s.get("type") == "file" and "sha256" not in s))
+    if unevaluable:
+        exit_code = EXIT_UNEVALUABLE
+    elif present == len(sections):
+        exit_code = EXIT_MATCH
+    else:
+        exit_code = EXIT_ABSENT
 
     if args.out == "-":
         sys.stdout.write(text)
@@ -575,9 +603,9 @@
             return EXIT_USAGE
         print("RECEIPT: %s  sha256=%s" % (out, digest))
         print("SIDECAR: %s" % sidecar)
+    state = {EXIT_MATCH: "OK", EXIT_UNEVALUABLE: "UNEVALUABLE"}.get(exit_code, "PARTIAL")
     print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
-          % ("OK" if exit_code == EXIT_MATCH else "PARTIAL", present, len(sections),
-             args.label or "(none)", exit_code))
+          % (state, present, len(sections), args.label or "(none)", exit_code))
     return exit_code
 
 
@@ -823,6 +851,41 @@
         assert before == after, "custody path changed during the guard case"
     run_case(cases, "refuses-to-write-over-custody-path", case_guard)
 
+    # 13. exists-but-unreadable path: declared UNEVALUABLE, receipt kept, no crash
+    def case_unreadable():
+        if os.geteuid() == 0:
+            return  # mode 000 does not block root; the case is not meaningful
+        bad = root / "unreadable.conf"
+        bad.write_bytes(b"x\n")
+        os.chmod(bad, 0)
+        out = root / "unreadable.txt"
+        rc = cmd_capture(argparse.Namespace(out=str(out), paths=[str(bad)], label="selftest"))
+        os.chmod(bad, 0o644)
+        assert rc == EXIT_UNEVALUABLE, "expected UNEVALUABLE exit %d, got %d" % (EXIT_UNEVALUABLE, rc)
+        text = out.read_text()
+        assert "READ-ERROR:" in text, "read error not recorded in the receipt"
+        assert "EXISTS: yes" in text, "unevaluable path recorded as absent"
+    run_case(cases, "unreadable-path-is-unevaluable", case_unreadable)
+
+    # 14. an unevaluable path must never verify as MATCH (fail-open class)
+    def case_unevaluable_not_match():
+        if os.geteuid() == 0:
+            return
+        d = root / "blocked"
+        d.mkdir()
+        inner = d / "inner.conf"
+        inner.write_bytes(b"y\n")
+        os.chmod(d, 0)
+        out = root / "blocked-receipt.txt"
+        rc_cap = cmd_capture(argparse.Namespace(out=str(out), paths=[str(inner)], label="selftest"))
+        outv = root / "blocked-verify.out"
+        rc_ver = _run_verify([str(out), "--live"], outv)
+        os.chmod(d, 0o755)
+        assert rc_cap == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_cap
+        assert rc_ver == EXIT_UNEVALUABLE, "expected verify UNEVALUABLE (fail-closed), got %d" % rc_ver
+        assert "UNEVALUABLE" in outv.read_text(), "no UNEVALUABLE class printed"
+    run_case(cases, "unevaluable-never-matches", case_unevaluable_not_match)
+
     passed = sum(1 for _, ok, _ in cases if ok)
     for name, ok, why in cases:
         print("case %-42s %s%s" % (name, "PASS" if ok else "FAIL", ("  (%s)" % why) if why else ""))
```
