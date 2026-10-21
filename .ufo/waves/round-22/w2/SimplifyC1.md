# SimplifyC1 — count-c1.py YAGNI review (R22 recovery W2)

**Seat:** `KaidokuR22R.SimplifyC1-6`  
**Target:** `.ufo/waves/round-22/tools/count-c1.py`  
**Baseline:** `7787fea4d6fd718726de92ed20759d11ce7b8b48`  
**Lane edits:** none (patch proposal only)

## Axes (godspeed)

| Axis | Intent |
|------|--------|
| Maintainability | One authoritative bind pass; no silent overwrite of `r21._measure` outputs |
| Correctness | Frozen T1 tuple, catalog `zero`/`mentioned`/`catalog_total`, sourced eligibility, `r21.bind` semantics |
| Performance | Drop duplicate `bind()` work on every T1 mention before the sourced gate |
| Clarity | `DEFAULT_TARGETS = ()` documents that catalog mention scan and T1 exercise are separate concerns |

## r21 dependency (observed)

`count-c1.py` loads `.ufo/waves/round-21/tools/verb-coverage.py` for:

- `legacy_helpers(root)` → round-20 `verb-coverage.py` (git tree, citation regex, `command_pattern`, `HEX64`, catalog JSON)
- `_measure(r20, root, rev)` → full-catalog mention counts plus, when `DEFAULT_TARGETS` is non-empty, per-target bind loops
- `bind(blob, verb, evidence_id)` → local JSON record binding (not authentication)

Round-22-specific logic layered on top: `EVIDENCE_PREFIX`, `CITED`, `corpus/SOURCES.md` S051+ mined rows opened `2026-10-21`, and `used-by` path gate before a witness counts toward `t1_exercised_*`.

Frozen `.ufo/waves/round-22/frozen/count-c1.py` omits the source gate; it is **not** behavior-equivalent to production `count-c1.py` and must not replace it.

## Duplicate authority (deletion candidate)

**Problem:** Production sets `r20.DEFAULT_TARGETS = T1`, so `r21._measure` runs a full bind pass over **all** knowledge mentioning each T1 verb, then `measure()` **discards** that `exercised` / `bound_evidence` and recomputes only from **eligible** entries. Catalog fields (`catalog_zero`, `catalog_mentioned_count`, `catalog_total`) still come from the first pass — correct — but T1 bind runs twice with different text sets.

**Rejected deletions (would harm correctness axis):**

- Remove source-row / `used-by` gate → matches frozen script; breaks R22-C1 falsifier “counted entry lacks round-22 S### citation” and `counter-fixtures` `missing_source`.
- Drop `r21._measure` entirely → would reimplement catalog mention scan against `.ufo/waves/round-20/verify/round20/verb-coverage.json`.
- Inline `bind` / fork r21 → second convention; no maintainability win.

## Proposed patch (minimal, behavior-preserving)

1. Set `r20.DEFAULT_TARGETS = ()` so `_measure` only produces catalog mention stats (`zero`, `mentioned`, `cli_commands`, …).
2. Single loop per T1 verb over all knowledge texts: `entries` and `unsupported_candidates` from any mention; `exercised` / `bound_evidence` only when `text in eligible` and `bind` returns code `0`.

Unified diff (apply to `.ufo/waves/round-22/tools/count-c1.py`):

```diff
--- a/.ufo/waves/round-22/tools/count-c1.py
+++ b/.ufo/waves/round-22/tools/count-c1.py
@@ -33,7 +33,7 @@
 def measure(root, rev):
     r21 = load(root, ".ufo/waves/round-21/tools/verb-coverage.py", "kaidoku_r21_bind")
     r20 = r21.legacy_helpers(root)
-    r20.DEFAULT_TARGETS = T1
+    r20.DEFAULT_TARGETS = ()
     r20.EVIDENCE_PREFIX = EVIDENCE_PREFIX
     r20.CITED = re.compile(re.escape(EVIDENCE_PREFIX) + r"[A-Za-z0-9._/-]*", re.ASCII)
     try:
@@ -47,20 +47,25 @@
             if int(cells[1][1:]) >= 51 and cells[8] == "mined" and cells[9] == "2026-10-21":
                 source_rows[cells[1]] = cells[11].split(",")
     paths = [path for path, _ in r20.tree_entries(root, result["rev"])]
-    eligible = []
+    texts = []
+    eligible = set()
     for path in paths:
         if not path.startswith(r20.KNOWLEDGE_PREFIX):
             continue
-        text = r20.git_show(root, result["rev"], path)
-        source = next((line for line in text.splitlines() if line.startswith("source:")), "")
+        body = r20.git_show(root, result["rev"], path)
+        texts.append(body)
+        source = next((line for line in body.splitlines() if line.startswith("source:")), "")
         ids = re.findall(r"\bS[0-9]{3,}\b", source)
         if any(path in [part.strip() for part in source_rows.get(sid, [])] for sid in ids):
-            eligible.append(text)
+            eligible.add(body)
+    result["targets"] = {}
     for verb in T1:
-        witnesses = []
-        for text in eligible:
+        witnesses, unevaluable = [], []
+        entries = 0
+        for text in texts:
             if not r20.command_pattern(verb).search(text):
                 continue
+            entries += 1
             cited = r20.cited_prefixes(text)
             ids = sorted(set(match.group(0) for match in r20.HEX64.finditer(text)))
             for path in paths:
@@ -68,10 +73,19 @@
                     continue
                 blob = r20.git_show(root, result["rev"], path)
                 for evidence_id in ids:
-                    if evidence_id in blob and r21.bind(blob, verb, evidence_id)[1] == 0:
+                    if evidence_id not in blob:
+                        continue
+                    _, code = r21.bind(blob, verb, evidence_id)
+                    if code == 0 and text in eligible:
                         witnesses.append([evidence_id, path])
-        result["targets"][verb]["exercised"] = bool(witnesses)
-        result["targets"][verb]["bound_evidence"] = witnesses[:5]
+                    elif code == 2:
+                        unevaluable.append(path)
+        result["targets"][verb] = {
+            "entries": entries,
+            "exercised": bool(witnesses),
+            "bound_evidence": witnesses[:5],
+            "unsupported_candidates": sorted(set(unevaluable)),
+        }
     exercised = [verb for verb in T1 if result["targets"][verb]["exercised"]]
     return {
```

**Preserved contract:** `T1` tuple; exit codes 0/1/2; JSON keys including `catalog_zero*`, `catalog_mentioned_count`, `catalog_total`, `t1_exercised*`, per-verb `targets` shape; `--selftest` wiring unchanged.

**Tradeoff:** Slightly more code in `measure()` than today, but one bind pass and explicit `targets` construction instead of measure-then-mutate.

## Verification (author-side)

| Command | Exit | Observation |
|---------|------|-------------|
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev 7787fea4d6fd718726de92ed20759d11ce7b8b48` (production, read-only) | **1** | `t1_exercised_count` 0, `catalog_zero_count` 20, `catalog_total` 153 — matches `claims.json` `before_expected` |
| Same command on patched copy vs production stdout | **1** both | `diff` empty (byte-identical JSON on baseline) |
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --selftest` (production) | **0** | `finding`: `counter_controls_clean` |
| Patched script in `git clone --no-local` scratch lane, `--selftest` | **0** | `finding`: `counter_controls_clean` (all six C1 fixture cases pass) |

**Tool installs:** none.

## Blockers

None for L1 integration of this patch.

## Inference

Semantic equivalence of patched vs production outputs was checked only at baseline rev and via `counter-fixtures` C1 cases; not exhaustively diffed across arbitrary revisions.
