# MutReaders — frozen receipt-reader mutation battery

Freeze: `4737a542ae3b1b910d8fe43efbd572bc578b07c6`; tool: `tools/round-70/packed-elf.py`.
Pristine and all restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`.

Axes: binding-clause sensitivity, false-input reachability, scope isolation, exact-byte restoration.

## Method

Seven independent one-line mutations, beyond the frozen five evaluate_carrier arm mutants. Each started as an exact frozen git blob in seat-owned scratch. Nine identical receipt inputs were run against pristine, every mutant, and every restored copy: 135 CLI invocations, bounded to 20 seconds each with eight workers. No packer/REA/runtime invocation; only Python receipt-reader CLI and read-only git-show binding checks.

CLI (replace reader and shape with the recorded paths):

```text
/usr/bin/python -I -B <reader.py> --check-receipt <shape.json> --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
```

Fixtures derive from the requested round-69 landing receipt. A deliberately synthetic control rebases producer metadata to the freeze and adds dinit by copying the jq row and rebinding the table fields/count. It is NOT a genuine measured round-70 receipt; its acceptance is only a structural positive control. The original round-69 receipt is also tested unchanged. All seven negative shapes are single-dimension corruptions of the synthetic control (orig count also recomputes its dependent ratio to isolate the declared-count clause). Full inputs are preserved as shape-*.json.

Pristine accepts synthetic-control and rejects raw-round69 plus all seven negative shapes; these intended negative rejections are baseline success, not baseline failure. DEAD requires a false input accepted or its named clause removed, never merely nonzero status.

## Mutation table

| Mutant | Frozen line | Change | Targeted false shape | Pristine → mutant rc | Outcome |
|---|---:|---|---|---|---|
| pin | 429 | registry pin → self-comparison | pin | 1 → 0 | DEAD (acceptance) |
| ratio | 472 | recomputed ratio → receipt ratio | ratio | 1 → 0 | DEAD (acceptance) |
| ceiling | 464 | packed > ceiling → packed < ceiling | ceiling | 1 → 1 | DEAD (named-clause removal) |
| rev | 400 | invocation revision → receipt self-comparison | rev | 1 → 0 | DEAD (acceptance) |
| ids | 478 | exact multiset equality → unknown-only set difference | ids | 1 → 0 | DEAD (acceptance) |
| orig | 458 | DECLARED_ORIG lookup → receipt self-comparison | orig | 1 → 0 | DEAD (acceptance) |
| producer | 397 | frozen blob hash → receipt self-comparison | producer | 1 → 0 | DEAD (acceptance) |

The ceiling inversion removes `jq: packed 11 > ceiling 10`, but adds false failures for the other below-ceiling rows. It is DEAD under the assigned clause-shrink rule, not a full forged-receipt acceptance. Six other mutants accept their dedicated rejected input. No syntax-error kills, survivors, or unevaluable runs.

## All shape verdicts

Numbers are CLI exit status (0 accepted; 1 rejected). Restored outputs, including stdout and stderr, match pristine exactly for all 63 restored runs.

| Reader | synthetic-control | raw-round69 | pin | ratio | ceiling | rev | ids | orig | producer |
|---|---|---|---|---|---|---|---|---|---|
| pristine | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| pin | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| ratio | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
| ceiling | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| rev | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 |
| ids | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| orig | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| producer | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |

## Exact patches and restoration

### pin
Mutant SHA-256: `17675269bd198ee02425a409cfdf30c76d142e79c1669330b3c6225f8e3c6d9f`.

```diff
--- frozen/packed-elf.py
+++ mutant/pin.py
@@ -426,7 +426,7 @@
         if row is None:
             failing.append(f"unknown carrier id {cid}")
             continue
-        if c.get("pin") != row["sha256"]:
+        if c.get("pin") != c.get("pin"):
             failing.append(f"{cid}: pin {c.get('pin')} != registry {row['sha256']}")
         if c.get("source") != row["source"]:
             failing.append(f"{cid}: source {c.get('source')} != registry {row['source']}")
```

False-input detector witness:
- `pin`: rc 1 → 0; removed: `jq: pin 0000000000000000000000000000000000000000000000000000000000000000 != registry e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

### ratio
Mutant SHA-256: `b8681a18aef40c6fef9947c436d2cbcdd044b687a62039e53d5ba9d52c6fe0b2`.

```diff
--- frozen/packed-elf.py
+++ mutant/ratio.py
@@ -469,7 +469,7 @@
         elif ceiling is not None and isinstance(orig_counts, dict) \
                 and isinstance(orig_counts.get("procedure_count"), int) \
                 and orig_counts["procedure_count"] > 0:
-            want = round(ceiling / orig_counts["procedure_count"], 4)
+            want = ratio
             if ratio != want:
                 failing.append(f"{cid}: before_ceiling_ratio {ratio} != "
                                f"ceiling/orig {want}")
```

False-input detector witness:
- `ratio`: rc 1 → 0; removed: `jq: before_ceiling_ratio 0.01 != ceiling/orig 0.0599`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

### ceiling
Mutant SHA-256: `ab7fc7b90a9c9ed537da1d83fd90d9230bac053dcbcc08da6be3e6041a06bef7`.

```diff
--- frozen/packed-elf.py
+++ mutant/ceiling.py
@@ -461,7 +461,7 @@
             packed_proc = packed_counts.get("procedure_count")
             if not isinstance(packed_proc, int):
                 failing.append(f"{cid}: packed procedure_count absent")
-            elif ceiling is not None and packed_proc > ceiling:
+            elif ceiling is not None and packed_proc < ceiling:
                 failing.append(f"{cid}: packed {packed_proc} > ceiling {ceiling}")
         ratio = c.get("before_ceiling_ratio")
         if not isinstance(ratio, (int, float)):
```

False-input detector witness:
- `ceiling`: rc 1 → 1; removed: `jq: packed 11 > ceiling 10`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

### rev
Mutant SHA-256: `687f9d9b18673eac51eacba83f53819f2fc12ef4a525801f3f665c3e8b5239e0`.

```diff
--- frozen/packed-elf.py
+++ mutant/rev.py
@@ -397,7 +397,7 @@
         if instrument.get("sha256") != blob_sha:
             failing.append(f"instrument.sha256 {instrument.get('sha256')} != "
                            f"blob at {rev} ({blob_sha})")
-    if receipt.get("rev") != rev:
+    if receipt.get("rev") != receipt.get("rev"):
         failing.append(f"rev {receipt.get('rev')} != {rev}")
     registry = {c["id"]: c for c in CARRIERS}
     target = receipt.get("target")
```

False-input detector witness:
- `raw-round69`: rc 1 → 1; removed: `rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6`
- `rev`: rc 1 → 0; removed: `rev 5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d != 4737a542ae3b1b910d8fe43efbd572bc578b07c6`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

### ids
Mutant SHA-256: `d43b2c6d4a873676d4e2eb1dcb07a78de7beb0180a024bbf0cacf16f3fa4fa15`.

```diff
--- frozen/packed-elf.py
+++ mutant/ids.py
@@ -475,7 +475,7 @@
                                f"ceiling/orig {want}")
             if ratio > 0.75:
                 failing.append(f"{cid}: before_ceiling_ratio {ratio} > 0.75")
-    if sorted(x for x in seen_ids if x is not None) != sorted(registry):
+    if set(x for x in seen_ids if x is not None) - set(registry):
         failing.append(f"carrier ids {seen_ids} != registry {sorted(registry)}")
     out = {"check": "R70-C3", "met": not failing, "failing": failing,
            "target": target, "carriers_matched": receipt.get("carriers_matched"),
```

False-input detector witness:
- `raw-round69`: rc 1 → 1; removed: `carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']`
- `ids`: rc 1 → 0; removed: `carrier ids ['jq', 'jq', 'libz', 'dinit'] != registry ['dinit', 'jq', 'libz', 'xxd']`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

### orig
Mutant SHA-256: `c802afa9c396195dfe430abb8651e7503e288c7f1a03702f13daba15555f6fb6`.

```diff
--- frozen/packed-elf.py
+++ mutant/orig.py
@@ -455,7 +455,7 @@
             failing.append(f"{cid}: counts absent")
         else:
             orig_proc = orig_counts.get("procedure_count")
-            if orig_proc != DECLARED_ORIG[cid]:
+            if orig_proc != orig_counts.get("procedure_count"):
                 failing.append(f"{cid}: orig_procedures {orig_proc} != "
                                f"declared {DECLARED_ORIG[cid]}")
             packed_proc = packed_counts.get("procedure_count")
```

False-input detector witness:
- `orig`: rc 1 → 0; removed: `jq: orig_procedures 168 != declared 167`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

### producer
Mutant SHA-256: `ac860655b9233386dd2d4f917c5e84d754096e43eb2d15aa2a742fadfd99c3a8`.

```diff
--- frozen/packed-elf.py
+++ mutant/producer.py
@@ -394,7 +394,7 @@
     else:
         if instrument.get("path") != TOOL:
             failing.append(f"instrument.path {instrument.get('path')} != {TOOL}")
-        if instrument.get("sha256") != blob_sha:
+        if instrument.get("sha256") != instrument.get("sha256"):
             failing.append(f"instrument.sha256 {instrument.get('sha256')} != "
                            f"blob at {rev} ({blob_sha})")
     if receipt.get("rev") != rev:
```

False-input detector witness:
- `raw-round69`: rc 1 → 1; removed: `instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)`
- `producer`: rc 1 → 0; removed: `instrument.sha256 0000000000000000000000000000000000000000000000000000000000000000 != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)`
Restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`; all nine restored outputs exactly match pristine.

## Disposition and limits

Observed: 7/7 new reader mutants DEAD; 0 survived; 0 unevaluable. No surviving mutation to route. Recommend the next freeze register these seven dedicated false-input shapes as reader regression cases; the existing frozen five target evaluate_carrier, not these new check_receipt clauses. This is a scoped reader mutation result, not a verdict on all three claims or real-carrier execution.

Evidence: `evidence.json` contains actual argv/rc/stdout/stderr for all 135 runs, before/mutated/restored hashes, exact unified diffs and removed-clause witnesses. All receipts were preserved before scratch removal. Frozen lane files were never edited; no git/jj mutation, tool installation, host service change, or PATH write occurred.

Tooling: existing Python 3.14.8; stdlib only; no installs/updates.

Self-evaluation: accuracy 4 (all outputs retained; synthetic control is not measurement); completeness 5 (seven mutants, nine shapes each, restoration and cleanup); clarity 4 (wide matrix supplemented by full JSON); actionability 4 (exact patches/fixtures retained; not integrated into frozen battery); conciseness 4 (raw evidence separated). Overall 4.2/5. Improvement: promote dedicated reader shapes at the next freeze.

VERDICT: met — seven new reader mutants killed on rejected false inputs; exact restoration confirmed; no survivors.
