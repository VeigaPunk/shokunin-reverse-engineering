# c1-run.sh port deltas

Exact source-line changes relative to `tools/round-50/c1-run.sh`:

```diff
-# R50-C1 run harness (kaidoku round 50; ported from tools/round-41/c1-run.sh, hardened
+# R52-C1 run harness (kaidoku round 50; ported from tools/round-41/c1-run.sh, hardened
-# Scratch (both arms): `$HYAKU_SCRATCH/kaidoku-r50` (default /fast/scratch/hyaku) or the
-# --scratch BASE; BASE MUST carry a /kaidoku-r50/ path segment (the receipt's
-# parameters.output_directory is hashed into the evidence id and the counter requires it
-# to start with /fast/scratch/hyaku/kaidoku-r50/). A private `c1-run.XXXXXX` directory is
+# Scratch (both arms): `$HYAKU_SCRATCH/kaidoku-r52` (default /fast/scratch/hyaku) or the
+# --scratch BASE; BASE MUST carry a /kaidoku-r52/ path segment (the receipt's
+# parameters.output_directory is hashed into the evidence id and the counter requires it
+# to start with /fast/scratch/hyaku/kaidoku-r52/). A private `c1-run.XXXXXX` directory is
-ROUND_SEGMENT=kaidoku-r50
-SCRATCH_PREFIX=/fast/scratch/hyaku/kaidoku-r50/
-EVIDENCE_SEGMENT=/corpus/evidence/round-50/
+ROUND_SEGMENT=kaidoku-r52
+SCRATCH_PREFIX=/fast/scratch/hyaku/kaidoku-r52/
+EVIDENCE_SEGMENT=/corpus/evidence/round-52/
-    --outdir DIR      output directory (default <lane>/corpus/evidence/round-50/c1/ID,
+    --outdir DIR      output directory (default <lane>/corpus/evidence/round-52/c1/<id>,
-    --scratch BASE    scratch base; MUST contain a /kaidoku-r50/ segment
-                      (default ${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r50)
+    --scratch BASE    scratch base; MUST contain a /kaidoku-r52/ segment
+                      (default ${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r52)
-  outdir=$lane_root/corpus/evidence/round-50/c1/$cid
+  outdir=$lane_root/corpus/evidence/round-52/c1/$cid
-      echo "$PROG: warning: scratch $scratch_base lacks a /$ROUND_SEGMENT/ segment; the R50-C1 output_directory clause will not hold" >&2
+      echo "$PROG: warning: scratch $scratch_base lacks a /$ROUND_SEGMENT/ segment; the R52-C1 output_directory clause will not hold" >&2
-      err "scratch $scratch_base lacks a /$ROUND_SEGMENT/ segment: a receipt written from it fails the R50-C1 run-provenance clause (parameters.output_directory is hashed into the evidence id). C1_ALLOW_FOREIGN_SCRATCH=1 permits a dev run."
+      err "scratch $scratch_base lacks a /$ROUND_SEGMENT/ segment: a receipt written from it fails the R52-C1 run-provenance clause (parameters.output_directory is hashed into the evidence id). C1_ALLOW_FOREIGN_SCRATCH=1 permits a dev run."
-    jq -n --arg schema kaidoku-r50-c1-run-v1 --arg mode oracle --arg claim R50-C1 --arg id "$cid" \\
+    jq -n --arg schema kaidoku-r52-c1-run-v1 --arg mode oracle --arg claim R52-C1 --arg id "$cid" \\
-    --arg schema kaidoku-r50-c1-run-v1 --arg mode oracle --arg claim R50-C1 --arg id "$cid" \\
+    --arg schema kaidoku-r52-c1-run-v1 --arg mode oracle --arg claim R52-C1 --arg id "$cid" \\
-  --arg schema kaidoku-r50-c1-run-v1 --arg mode after --arg claim R50-C1 --arg id "$cid" \\
+  --arg schema kaidoku-r52-c1-run-v1 --arg mode after --arg claim R52-C1 --arg id "$cid" \\
```

No other changes intended. Pins, `FIXED_PATH`, guards, retry loop, superblock condition, and three-producer oracle are retained from the source.
