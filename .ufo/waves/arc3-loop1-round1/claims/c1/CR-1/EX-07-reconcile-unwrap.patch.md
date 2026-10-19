# PATCH PROPOSAL (not applied) — EX-07 `reconcile.py`: unwrap wrapped probe legs, mark unreadable legs, add form invariants

- Seat: CR-1 (chain c1, critic). Date: 2026-10-19.
- Target: `.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconcile.py`
  (sha256 `c1be27319211a887b3df3f36799267cd9f773db155fb43903ca5927a1475ccef` —
  the revision EX-07's own report cites; mtime 07:09).
- Patch sha256: `a73f75976c7233015defa96b0c41c830d641cc486134af420fe992d6b755113f`.
- Verified: `patch -p1 --dry-run` clean from a repo-root-shaped scratch tree;
  patched driver sha256 `21d0d68af76883d608e61bd0060945b70be4cc63b561fafdca128361df3e2bd9`.

## Why

Three defects, all reproduced against the committed artifacts (evidence in
`CR-1/evidence/replay/`):

1. **Committed transcript is not reproducible from the committed command.**
   EX-05's four legs (`kdx.hex.json`, `kdx.raw.json`, `kdx.raw.rerun.json`,
   `kdx.raw.renamed.json`) are `{ok,data,meta}`-wrapped; `load_probe` reads
   `d.get("raw_result")` with no unwrap, so each leg parses as an empty set.
   Running EX-07's documented command against the committed inputs
   (`baseline-run.txt`) prints `PROBE:kdx.hex.json n= 0 MISMATCH` ×4 and
   `VERDICT: MISMATCH PRESENT` (exit 1), while the committed transcript
   (`reconciliation-run-all-legs.txt`, sha256 `a356c3a9…`) shows `n= 6 MATCH`
   and `ALL SOURCES AGREE`. Feeding unwrapped copies with the same basenames
   reproduces the committed transcript **byte-identically**
   (`unwrapped-all6.txt` sha256 `a356c3a9…`). So the recorded run used an
   unrecorded unwrap preprocessing step; the committed command alone does not
   reproduce it. (Not fabrication — the numbers are achievable.)
2. **Vacuous passes.** For an unreadable/empty leg the offsets section prints
   `all offsets equal` (no offsets ⇒ no mismatch) and the digest section skips
   the leg silently. Only the set-equality row catches it; the aggregate
   verdict was safe, but the per-leg lines mislead a reader.
3. **No form check.** Nothing verifies that a leg's carrier form is
   self-consistent (`artifact.encoding` vs the byte-count relation vs the
   decoded digest) — the raw/hex wrong-form class (CR-1 attack 1) has no
   in-driver detector.

## Fix

`load_probe` unwraps `{ok,data,meta}`; unreadable legs are marked and flip the
verdict instead of vacuously passing; a `probe form invariants` section checks
per leg: `hex` ⇒ `0 ≤ artifact.bytes − 2×decoded_bytes ≤ 2` (trailing newline
tolerated) and `artifact.sha256 ≠ bytecode.sha256`; `raw` ⇒ byte counts equal
and `artifact.sha256 == bytecode.sha256`.

## Behavior after patch (verified on the /var/tmp replay copies)

- Documented command with **wrapped** committed inputs: exit 0,
  `VERDICT: ALL SOURCES AGREE`, all six legs `FORM-OK`
  (`patched-wrapped.txt`) — the transcript now reproduces from the committed
  artifacts alone.
- Doctored legs still rejected (exit 1, `MISMATCH PRESENT`): dropped selector
  (`leg-partial`), phantom selector (`leg-phantom`), wrong-form leg
  (`leg-wrongform`, also `FORM-MISMATCH`), wrong decoded digest
  (`leg-baddigest`).

## Patch text

```diff
--- a/.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconcile.py
+++ b/.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/reconcile.py
@@ -46,11 +46,19 @@
 
 def load_probe(path):
     d = json.load(open(path))
+    if isinstance(d.get("data"), dict):
+        d = d["data"]  # unwrap {ok,data,meta} CLI envelopes (EX-05-style legs)
     fns = d.get("raw_result", {}).get("functions", [])
     sels = norm([f["selector"] for f in fns])
     offsets = {f["selector"].lower().removeprefix("0x"): f["bytecodeOffset"] for f in fns}
-    sha = d.get("normalized_result", {}).get("bytecode", {}).get("sha256")
-    return sels, offsets, sha, d
+    nres = d.get("normalized_result", {})
+    sha = nres.get("bytecode", {}).get("sha256")
+    art = nres.get("artifact", {})
+    bc = nres.get("bytecode", {})
+    form = {"encoding": art.get("encoding"), "artifact_bytes": art.get("bytes"),
+            "artifact_sha": art.get("sha256"), "decoded_bytes": bc.get("bytes"),
+            "decoded_sha": bc.get("sha256"), "readable": bool(nres)}
+    return sels, offsets, sha, form
 
 
 def main():
@@ -82,10 +90,12 @@
     sources["PLANTED"] = planted
 
     probe_offsets = {}
+    probe_forms = {}
     for p in args.probe:
-        sels, offsets, sha, _ = load_probe(p)
+        sels, offsets, sha, form = load_probe(p)
         sources["PROBE:" + os.path.basename(p)] = sels
         probe_offsets[os.path.basename(p)] = offsets
+        probe_forms[os.path.basename(p)] = form
 
     # M2 keccak scan over ABI signatures: verify each selector's bytes are present
     m2_found = {}
@@ -116,6 +126,10 @@
     print("probe offsets vs my parsed JUMPDEST dests:")
     my_dest = {c["selector"]: c["dest"] for c in m1["dispatch_chain"]}
     for pname, offsets in probe_offsets.items():
+        if not offsets:
+            print(f"  {pname}: NO OFFSETS PARSED (leg unreadable or empty) -- not a pass")
+            verdict_all = False
+            continue
         mism = {sel: (my_dest.get(sel), off) for sel, off in offsets.items()
                 if my_dest.get(sel) != off}
         print(f"  {pname}: {'all offsets equal' if not mism else mism}")
@@ -123,11 +137,35 @@
     print()
     print("probe code-digest pins vs my sha256:")
     for p in args.probe:
-        _, _, sha, _ = load_probe(p)
+        _, _, sha, form = load_probe(p)
         if sha:
             same = sha == code_sha
             verdict_all &= same
             print(f"  {os.path.basename(p)}: pinned={sha} mine={code_sha} {'SAME' if same else 'DIFFER'}")
+        else:
+            print(f"  {os.path.basename(p)}: NO DIGEST PIN (leg unreadable) -- not a pass")
+            verdict_all = False
+    print()
+    print("probe form invariants (carrier form vs decoded bytecode):")
+    for pname, f in probe_forms.items():
+        if not f["readable"]:
+            print(f"  {pname}: UNREADABLE (no normalized_result) -- form not checkable")
+            verdict_all = False
+            continue
+        enc, ab, db = f["encoding"], f["artifact_bytes"], f["decoded_bytes"]
+        asha, dsha = f["artifact_sha"], f["decoded_sha"]
+        ok = True
+        if enc == "hex" and None not in (ab, db):
+            # hex text is 2 chars/byte; trailing newline (LF/CRLF) is tolerated by the tool
+            ok &= (0 <= ab - 2 * db <= 2)
+        if enc == "raw" and None not in (ab, db):
+            ok &= (ab == db) and (asha == dsha)
+        if enc == "hex" and asha and dsha:
+            ok &= (asha != dsha)  # hex file bytes are not the decoded bytes
+        verdict_all &= ok
+        print(f"  {pname}: encoding={enc} artifact_bytes={ab} decoded_bytes={db} "
+              f"artifact_sha={str(asha)[:8]} decoded_sha={str(dsha)[:8]} "
+              f"{'FORM-OK' if ok else 'FORM-MISMATCH'}")
     print()
     print("VERDICT:", "ALL SOURCES AGREE" if verdict_all else "MISMATCH PRESENT")
     return 0 if verdict_all else 1
```

Note for the applier: the note in EX-07's report ("EX-05's JSONs are
`{ok,data,meta}`-wrapped; the driver unwraps them") describes behavior the
committed revision does not have — apply this patch, or re-record the
transcript from unwrapped copies with the preprocessing step documented, so the
committed command and transcript agree.

Reproduce the replay: `CR-1/evidence/replay/` holds `baseline-run.txt`,
`unwrapped-all6.txt`, `wrapped-all6.txt`, `leg-*.json` (doctored inputs),
`leg-*-out.txt`, `patched-*.txt`, `reconcile-patched.py`, and the labeled patch.
