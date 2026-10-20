# Round 17 W2 — MutateLogExtractRoute

Axes: **calibration** (separate selftest detection from untested behavior) and **depth** (route attribution, regex specificity, conflict precedence, fallback direction, and log binding).

## Scope and result

**Observation:** Eight independent, single-line mutations of `.ufo/waves/round-17/tools/log-extract.py` were applied only to separate `/tmp` copies. The unchanged `--selftest` killed **3/8** and allowed **5/8** to survive; **0 inconclusive**. Every copy passed before mutation and after exact-byte restoration. Supplemental synthetic witnesses distinguished every mutant from pristine/restored behavior, including all five survivors.

This is an author-side **selftest coverage finding**, not evidence that the unmodified parser currently produces the deliberately introduced defects. No contract changes or production fixes were made.

Target revision: `da64646adcb19c1ede7537b799b8c7d283fe43da` (observed HEAD). These commands both returned `41b2c08068a7c619134c8f6f4abda7fe5e07db4c179f86793a26e84909109429`:

```sh
git show da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/tools/log-extract.py | sha256sum
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/log-extract.py
```

The source hash was identical again after the probe. Python: `3.14.8`; no installs/updates. No REA, Ghidra, carrier execution, sibling edits, commits, or pushes.

## Detector and exact outputs

Scratch root `T = /tmp/r17-MutateLogExtractRoute-OVkys8JK`. Executed driver commands, in this order, with eight independent copies probed concurrently within each phase:

```sh
python3 -B -I /tmp/r17-MutateLogExtractRoute-OVkys8JK/probe.py pristine
python3 -B -I /tmp/r17-MutateLogExtractRoute-OVkys8JK/probe.py mutated
python3 -B -I /tmp/r17-MutateLogExtractRoute-OVkys8JK/probe.py restored
```

For every row below, the driver invoked `/usr/bin/python3 -B -I T/<name>.py --selftest` and `/usr/bin/python3 -B -I T/<name>.py --log T/<name>.log`, each with a 20-second subprocess timeout. `T` denotes the exact absolute root above, not another source tree. The original selftest at `tools/log-extract.py:255-457` was unchanged. Verdicts below use **only that selftest**, not the supplemental witness checks.

All 16 pristine/restored selftests exited **0**, stdout exactly `SELFTEST: CLEAN cases=8\n`, stderr empty. Mutated selftests:

| Mutant / scratch basename | Target anchor | Exit | Verdict | Exact stdout, excluding terminal LF |
|---|---|---:|---|---|
| M01-fallback-as-info | `.ufo/waves/round-17/tools/log-extract.py:225` | 1 | killed | `SELFTEST: FAILED case fallback_route: snapshot_route='info' expected 'fallback'` |
| M02-info-as-fallback | `.ufo/waves/round-17/tools/log-extract.py:227` | 0 | survived | `SELFTEST: CLEAN cases=8` |
| M03-drop-route-component | `.ufo/waves/round-17/tools/log-extract.py:196` | 0 | survived | `SELFTEST: CLEAN cases=8` |
| M04-broad-info-regex | `.ufo/waves/round-17/tools/log-extract.py:200` | 0 | survived | `SELFTEST: CLEAN cases=8` |
| M05-conflict-as-fallback | `.ufo/waves/round-17/tools/log-extract.py:223` | 0 | survived | `SELFTEST: CLEAN cases=8` |
| M06-reverse-fallback | `.ufo/waves/round-17/tools/log-extract.py:199` | 1 | killed | `SELFTEST: FAILED case fallback_route: snapshot_fallbacks=[{'from': '1.25.0', 'to': '1.25.8'}] expected [{'from': '1.25.8', 'to': '1.25.0'}]` |
| M07-crosswire-log-binding | `.ufo/waves/round-17/tools/log-extract.py:236` | 0 | survived | `SELFTEST: CLEAN cases=8` |
| M08-echo-as-info-label | `.ufo/waves/round-17/tools/log-extract.py:241` | 1 | killed | `SELFTEST: FAILED case fallback_route: api_snapshot_info_labels=['1.25.8'] expected []` |

Every mutated stderr was empty. All 24 supplemental `--log` invocations exited 0: extraction success is not a behavioral assertion. The driver compared selected JSON fields with fixed expectations; `witness_match` was **true for all pristine/restored copies, false for all mutants**.

## Single-mutation diffs

Each hunk below belongs to a different copy; no mutant accumulated another mutant's edit. Source lines are at the pinned revision.

```diff
--- M01-fallback-as-info/pristine
+++ M01-fallback-as-info/mutated
@@ -225 +225 @@
-        snapshot_route = "fallback"
+        snapshot_route = "info"
--- M02-info-as-fallback/pristine
+++ M02-info-as-fallback/mutated
@@ -227 +227 @@
-        snapshot_route = "info"
+        snapshot_route = "fallback"
--- M03-drop-route-component/pristine
+++ M03-drop-route-component/mutated
@@ -196 +196 @@
-        if component == "GoApiSnapshot":
+        if component.startswith("Go"):
--- M04-broad-info-regex/pristine
+++ M04-broad-info-regex/mutated
@@ -200 +200 @@
-            ai = API_INFO_RE.match(message)
+            ai = SNAPSHOT_RE.match(message)
--- M05-conflict-as-fallback/pristine
+++ M05-conflict-as-fallback/mutated
@@ -223 +223 @@
-        snapshot_route = "conflict"
+        snapshot_route = "fallback"
--- M06-reverse-fallback/pristine
+++ M06-reverse-fallback/mutated
@@ -199 +199 @@
-                fallbacks.append({"from": fb.group(1), "to": fb.group(2)})
+                fallbacks.append({"from": fb.group(2), "to": fb.group(1)})
--- M07-crosswire-log-binding/pristine
+++ M07-crosswire-log-binding/mutated
@@ -236 +236 @@
-        "log_file_line": log_file,
+        "log_file_line": import_target,
--- M08-echo-as-info-label/pristine
+++ M08-echo-as-info-label/mutated
@@ -241 +241 @@
-        "api_snapshot_info_labels": _dedupe(api_info_labels),
+        "api_snapshot_info_labels": _dedupe(snapshot_labels),
```

## Missing tests that would kill each survivor

**Observation:** The following fixtures and expected/observed fields were actually exercised in all three phases. Each line shown is a complete synthetic log record; fixtures used two trailing spaces and LF. The table reports selected fields from the CLI JSON, not the whole stdout. Expectations matched both pristine and restored bytes.

### M02 — exact/info route is not asserted

Fixture:

```text
2026-10-20 10:00:00 INFO  (GoApiSnapshot) Using Go API snapshot for 1.23.12
```

Add assertion `snapshot_route == "info"` (and `api_snapshot_info_labels == ["1.23.12"]`) to the existing `snapshot_loaded` fixture at `.ufo/waves/round-17/tools/log-extract.py:315-336`. Its existing checks omit both route fields despite already containing this positive event. Witness expected `{"snapshot_route":"info"}`; mutant observed `{"snapshot_route":"fallback"}`.

### M03 — component and message guards are not tested independently

Fixture:

```text
2026-10-20 10:00:00 INFO  (GoRttiMapper) Using Go API snapshot for 1.23.12
```

Add negative attribution assertion `snapshot_route == "none"` and `api_snapshot_info_labels == []` while retaining the generic snapshot label. The production component guard is at `.ufo/waves/round-17/tools/log-extract.py:196-202`. Witness expected `{"api_snapshot_info_labels":[],"snapshot_route":"none"}`; mutant observed `{"api_snapshot_info_labels":["1.23.12"],"snapshot_route":"info"}`.

This is a synthetic wrong-component/route-looking-message boundary, not a claim that installed Ghidra emits that Mapper spelling. The existing Mapper echo at `:414-415` contains `version`, so the strict info regex independently rejects it and masks the lost component check.

### M04 — generic snapshot regex can replace the exact route regex undetected

Fixture:

```text
2026-10-20 10:00:00 INFO  (GoApiSnapshot) Using Go API snapshot for version 1.23.12
```

Add negative exact-grammar assertions `snapshot_route == "none"`, `api_snapshot_info_labels == []`, and positive generic `snapshot_labels == ["1.23.12"]`. The distinct regexes are at `.ufo/waves/round-17/tools/log-extract.py:73,82`; route matching is at `:200`. Witness expected `{"api_snapshot_info_labels":[],"snapshot_route":"none"}`; mutant observed `{"api_snapshot_info_labels":["1.23.12"],"snapshot_route":"info"}`.

This deliberately non-emitted GoApiSnapshot spelling isolates the implemented grammar boundary; it is not evidence of an observed Ghidra log. The existing fallback fixture places the `version` spelling only under Mapper, where the component guard hides this regex substitution.

### M05 — contradictory routes lack a conflict test

Fixture:

```text
2026-10-20 10:00:00 WARN  (GoApiSnapshot) Falling back from 1.25.8 to 1.25.0 for Go API snapshot
2026-10-20 10:00:01 INFO  (GoApiSnapshot) Using Go API snapshot for 1.23.12
```

Add assertion `snapshot_route == "conflict"` with both event arrays retained. This tests the conflict-before-fallback branch at `.ufo/waves/round-17/tools/log-extract.py:222-227`. Witness expected `{"snapshot_route":"conflict"}`; mutant observed `{"snapshot_route":"fallback"}`. No single-route fixture can distinguish this mutation.

### M07 — log-file/import-target binding is unasserted

Fixture:

```text
2026-10-20 10:00:00 INFO  (ProgramLoader) Using log file: /tmp/session/ghidra.log
2026-10-20 10:00:01 INFO  (HeadlessAnalyzer) IMPORTING: file:///tmp/carrier.bin
```

Add assertions `log_file_line == "/tmp/session/ghidra.log"` and `import_target == "/tmp/carrier.bin"`, explicitly using different values. Extraction is at `.ufo/waves/round-17/tools/log-extract.py:156-163`, output binding at `:236-237`. Witness expected `{"import_target":"/tmp/carrier.bin","log_file_line":"/tmp/session/ghidra.log"}`; mutant observed `{"import_target":"/tmp/carrier.bin","log_file_line":"/tmp/carrier.bin"}`. The current selftest at `:255-457` has no binding assertions.

**Inference:** Adding these assertions to the unchanged baseline suite would kill the corresponding survivors, because the supplemental comparisons were actually true → false → true across pristine → mutant → restored. They were not integrated here, and their proposed integration was not run.

## Hashes and restoration evidence

Let `P = 41b2c08068a7c619134c8f6f4abda7fe5e07db4c179f86793a26e84909109429`. Each copy's recorded state transition was `P → mutant hash below → P`; each detector also recorded an identical before/after hash within its phase. All eight restores returned the original 18,058 bytes and clean eight-case selftest.

| Mutant | Mutated SHA-256 |
|---|---|
| M01 | `c69349308a04cae520b998143bc22bef1e24dd51a94e99146a03a3a3d6da5251` |
| M02 | `764e82b7eb52577cc86aa070d200fcaae3dc4f11c6d2040a30a63512d3d7a56d` |
| M03 | `2520f420d997dd5756f72b8531cf1a8362911d8ab6fa6d00eb433a0fc1cb140f` |
| M04 | `8a6c49a0f834a10aa515cc8dcc10b772edbe94eeae82e61cdf89a465cf58b997` |
| M05 | `14aed3582de326e8e3b3112ad3300fd2946817a490cbdbfaccf3c0cc0ed659bf` |
| M06 | `00e9ec2dc9a47ed1a769554012b6c58558ad3126d05bb1f8077df011c83f346d` |
| M07 | `fb276fef434404688adba4433c22a8919369dee2a4666bac81a7a6e5e8dc58d8` |
| M08 | `90cacbe80304ba960b7e43076d2056f765929d48783828797bc57782a7bb8f7f` |

Full argv/stdout/stderr/field comparisons and before/after hashes remain in temporary receipts under `T` (this report is the durable scoped deliverable):

| Scratch evidence | SHA-256 |
|---|---|
| `pristine.json` | `176f80acf824dc3762b8fad1ca0caa738c32f6c7fab40f85796de4e0077a2399` |
| `mutated.json` | `4bd8286755ecd3f11086336f11160f535ceb4d3ba0302b7553d03ff505985f99` |
| `restored.json` | `77ab0282d91721e22d76e2f70e8d4dcc4e6c4e6ee75d95d0fad973480ca2aa54` |
| `specs.json` | `d99da149c5c3a9ceab55f9b80c99cbf427c9cc96201cd37a9d50c0d89fd1c8e5` |
| `probe.py` | `7d2c5fa0e166379a5e2b4b5cc2e33c683af88f2f7cab930f4c9ca6d3fba64481` |

Tooling note: ranged `read :raw` omitted the final LF; its initial text failed the source hash before any copies were created. Appending that LF produced the pinned hash and exact byte length before copying. This tool inconsistency was reported via `xd://report_issue`.
