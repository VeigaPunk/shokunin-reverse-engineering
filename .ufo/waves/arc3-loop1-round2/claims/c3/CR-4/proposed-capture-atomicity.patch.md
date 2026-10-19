# CR-4 proposed change — capture atomicity + optional identity hardening

Target (real target owned by seat EX-31, **not** edited by this seat):
`.ufo/gates/custody-pair/custody-pair.py`
attacked revision `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`.

Status: **proposal (patch text)**. Nothing under `.ufo/gates/` was written by CR-4.

## 1. Why (measured)

`capture_path(path)` takes `os.lstat(path)` (`:193`) and then calls
`sha256_file(path)` (`:224`), which opens the path **by name again** (`:166-172`)
and is never followed by a re-stat of what was read. Reproduced on the identical
pattern, 300 captures against a writer alternating 4 KiB/200 KiB contents:

```
{"captures": 300, "replica_internal_inconsistency": 2, "replica_unstable_read": 30,
 "replica_pre_stat_mismatch": 4}
```

i.e. 2/300 receipts carried a `SIZE` (from the stat) that did not belong to the
`SHA256` (from the read) — a receipt that is internally false. Not a silent
bypass (a mixed tuple still needs inode+ctime equality with the reference to
return `MATCH`), but a custody certificate must not assert a tuple that never
existed as a state, and the misclassification lands on real paths under load.

## 2. Patch text (minimal, behaviour-preserving)

```diff
-def sha256_file(path: Path) -> str:
-    h = hashlib.sha256()
-    with open(path, "rb") as fh:
-        for chunk in iter(lambda: fh.read(1 << 20), b""):
-            h.update(chunk)
-    return h.hexdigest()
+def sha256_fd(fh) -> str:
+    h = hashlib.sha256()
+    for chunk in iter(lambda: fh.read(1 << 20), b""):
+        h.update(chunk)
+    return h.hexdigest()
+
+
+def sha256_file(path: Path) -> str:
+    with open(path, "rb") as fh:
+        return sha256_fd(fh)
@@ capture_path
-    if os.path.islink(path):
-        fields["type"] = "symlink"
-        target = os.readlink(path)
-        fields["symlink_target"] = target
-        fields["sha256"] = hashlib.sha256(target.encode()).hexdigest()
-    elif os.path.isfile(path):
-        fields["type"] = "file"
-        fields["sha256"] = sha256_file(path)
-    else:
-        fields["type"] = "other"
-    return fields
+    if os.path.islink(path):
+        fields["type"] = "symlink"
+        target = os.readlink(path)
+        fields["symlink_target"] = target
+        fields["sha256"] = hashlib.sha256(target.encode()).hexdigest()
+    elif os.path.isfile(path):
+        fields["type"] = "file"
+        with open(path, "rb") as fh:              # one open, then stat THAT fd
+            st_open = os.fstat(fh.fileno())
+            fields["sha256"] = sha256_fd(fh)
+            st_after = os.fstat(fh.fileno())
+        # (inode, size, ctime, mtime) must be stationary across the read, and the
+        # fd we hashed must be the inode we are about to pin.
+        fields["stable"] = (st_open.st_ino == st_after.st_ino
+                            and st_open.st_size == st_after.st_size
+                            and st_open.st_ctime_ns == st_after.st_ctime_ns
+                            and st_open.st_mtime_ns == st_after.st_mtime_ns
+                            and st.st_ino == st_open.st_ino
+                            and st.st_ctime_ns == st_open.st_ctime_ns)
+        if not fields["stable"]:
+            # keep the capture honest: do not certify a tuple that never existed
+            fields["unstable"] = "yes"
+    else:
+        fields["type"] = "other"
+    return fields
```

Recommended companion changes (small, one line each):

* render `STABLE: yes|no` in the stanza (`render_receipt`) and add `stable` to
  `COMPARE_KEYS`; classify `stable=no` as a declared class (e.g. extend
  `METADATA-DRIFT` notes, or a new `UNSTABLE-CAPTURE` exit) so an unstable
  capture can never read as `MATCH`.
* `capture` should return non-zero (a declared class, not 0) when any stanza is
  `unstable=no`, so a caller cannot silently bank an internally false receipt.
* when present, `verify` should check `<receipt_a>.sha256` and fail closed on
  mismatch (independently recommended by `seats/EX-33.md` §2). Necessary but not
  sufficient: the forger regenerates the sidecar — the real anchor is the commit
  or an independent capture.

Note on `sha256_file(path)`: keep the wrapper — the selftest and the sidecar
paths call it (`:566-568`, `:820`), and the guard case depends on its behaviour.

## 3. Optional identity hardening (each cheap; none required for the claim)

The measured residual (see `residual-threat-model.md` §4) is only reachable by an
actor with raw-device/metadata control or receipt-store write access. Two cheap
pins raise the cost in that class, and both are *free* to record:

1. `st_dev` (`fields["dev"] = st.st_dev`, compared). Today a receipt cannot tell
   two different files with equal inode numbers apart; a device pin also makes a
   bind-mounted or foreign-FS path visible as a custody event.
2. `st_nlink` (`fields["nlink"]`, compared). Guards the alias channel: a hardlink
   added by an actor who can also forge ctime is otherwise invisible; nlink is a
   field the alias creation must move.
3. `statx` birth time (`STATX_BTIME`, available on this host — measured:
   `statx` returns mask `0x9fff` with `btime` for a btrfs file). btime cannot be
   set by `utimensat` and survives nothing that recreates the inode; pinning it
   adds a second userspace-unforgeable field next to ctime. Record it, compare
   it when both sides carry it, and keep it out of `COMPARE_KEYS` for v1 interop
   (report `MATCH-V1-PARTIAL` as today).

## 4. Explicitly NOT proposed

* No change to the declared exit-code table or severity precedence — the current
  shape (10/11/12/13/2/3, worst-finding-wins) is coherent and already documented.
* No widening of the 5-path set, no scope change (the r4 laundering precedent).
* No claim of tamper-proofness: the instrument stays a tripwire against
  userspace writers. Over-promising here would be the largest defect available.
