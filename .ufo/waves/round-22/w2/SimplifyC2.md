# SimplifyC2 — `count-c2.py` probe association & dead weight

**Agent:** `KaidokuR22R.SimplifyC2-6`  
**Target:** `.ufo/waves/round-22/tools/count-c2.py` (read-only; patch for L1 integration only)  
**Baseline:** `7787fea4d6fd718726de92ed20759d11ce7b8b48`  
**Lane HEAD at review:** `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`

## Axes

| Axis | Question |
|------|----------|
| **Calibration** | Does the counter reject receipts whose `meta.command` is not the T2 catalog verb named in the row? |
| **Coverage** | Are all three `observed` grammars (`error:`, `ok-empty:`, `ok-field:`) required by frozen T2 row semantics? |
| **Clarity** | Is the `probe` column’s role obvious vs `verb` and the envelope? |
| **Minimalism** | Any imports or branches with no semantic callers? |

## Commands & observed exits

```bash
python3 -I -B .ufo/waves/round-22/tools/count-c2.py --selftest
# exit 0 — all counter-fixtures C2 cases pass

python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev 7787fea4d6fd718726de92ed20759d11ce7b8b48
# exit 1 — accounted_count 0/14, mismatched [], foreign_rows [] (matches claims.json before_expected)

python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root . --rev HEAD
# exit 0 — accounted_count 14/14, mismatched [], foreign_rows []

python3 -I -B .ufo/waves/round-22/tools/counter-fixtures.py --claim C2 \
  --counter .ufo/waves/round-22/tools/count-c2.py --root .
# exit 0
```

**Tool installs:** none.

## Findings

### 1. Wrong branch (historical) — frozen `count-c2.py`, not current tools copy

`frozen/count-c2.py` (baseline-era) associated receipts only with the **`probe` column**:

```python
if env["meta"].get("command") != row["probe"]:
    return "probe_mismatch"
```

**Adversarial row** (scratch git, one commit):

- `verb` = `inspect-packet-fields` (T2)
- `probe` = `inspect-pcap-client`
- receipt `meta.command` = `inspect-pcap-client`
- `observed` = `error:capability_unavailable` (matches envelope)

| Counter | `per_verb["inspect-packet-fields"].status` | exit | `accounted_count` |
|---------|---------------------------------------------|------|-------------------|
| `frozen/count-c2.py` | **`matched`** | 1 | **1** |
| `tools/count-c2.py` | **`probe_mismatch`** | 1 | 0 |

That is exactly falsifier *“a receipt from a different probe command is accepted”* when read as “accepted for the **verb** named in the catalog row.” Frozen logic treats `probe` as the authority; the row’s `verb` can disagree while still counting as matched for that T2 slot.

Current `tools/count-c2.py` already adds `row["probe"] != row["verb"]` (see diff vs frozen). That closes the fixture exercised by `counter-fixtures.py` case `probe_alias` (`expected_status`: `probe_mismatch`).

### 2. Residual clarity bug — receipt still chained through `probe` in tools copy

At `tools/count-c2.py` lines 104–105:

```python
if row["probe"] != row["verb"] or env["meta"].get("command") != row["probe"]:
    return "probe_mismatch"
```

The second disjunct still matches **envelope → probe**, not **envelope → verb**. Behavior today is correct only because the first disjunct rejects `probe != verb` before a `meta.command == probe != verb` case can reach `matched`. The docstring (line 10) also says `meta.command equals probe`, which reinforces the wrong mental model.

**Smallest clarification** (behavior-preserving on all exercised fixtures and HEAD PROVINCE rows, where `probe == verb` everywhere):

- Anchor envelope checks on `row["verb"]`.
- Keep `probe != verb` as an explicit row-integrity guard (human table column must not disagree with catalog verb).

### 3. Dead import — safe deletion

`import re` (line 24) has **no** `re.` use in this module. Text search only (no LSP server in this lane seat); treat as dead weight, not semantic proof via references.

### 4. Not dead — observed grammars

Production `PROVINCE.md` (HEAD) uses all three forms:

- `error:*` — majority of T2 rows
- `ok-empty:sessions` — `list-cutter-sessions`
- `ok-field:*` — `list-frida-devices`, `list-frida-processes`

Do **not** delete `ok-empty` / `ok-field` branches or `dig()`.

## Preserved contract

- Frozen **T2 tuple** and per-verb counting unchanged.
- Row table shape, placements, receipt prefix, strict JSON, exit codes 0/1/2.
- `counter-fixtures.py` C2 controls remain passing after the proposed patch (equivalence argument above; L1 should re-run `--selftest` on integrate).

## Proposed patch (unified diff — author-side only)

```diff
--- a/.ufo/waves/round-22/tools/count-c2.py
+++ b/.ufo/waves/round-22/tools/count-c2.py
@@ -7,7 +7,8 @@
   - receipt is a lane path under RECEIPT_PREFIX present at REV;
   - the receipt decodes as strict JSON (duplicate members/non-finite refused)
-    and is a REA CLI envelope whose meta.command equals `probe`;
+    and is a REA CLI envelope whose meta.command equals the row `verb`
+    (and the `probe` column must equal that same verb);
   - `observed` matches the envelope: `error:<code>` needs ok==false and
     error.code==<code>; `ok-empty:<dotted.path>` needs ok==true and the list at
     data.<dotted.path> to be empty; `ok-field:<dotted.path>=<json>` needs
@@ -21,7 +22,6 @@
 import importlib.util
 from pathlib import Path
 import json
-import re
 import subprocess
 import sys
@@ -101,8 +101,8 @@
         return "receipt_unevaluable"
     if not isinstance(env, dict) or not isinstance(env.get("meta"), dict):
         return "receipt_not_envelope"
-    if row["probe"] != row["verb"] or env["meta"].get("command") != row["probe"]:
+    if row["probe"] != row["verb"] or env["meta"].get("command") != row["verb"]:
         return "probe_mismatch"
     observed = row["observed"]
```

## Tradeoff

- **Keep separate `probe` column in the table** vs folding into `verb`: retained for human readability and wave-1 table contract; counter only needs to enforce `probe == verb` plus envelope match on **verb**.
- **Do not** revert to frozen’s probe-only envelope check; that regresses calibration.

## Blockers

None for this review seat. Integration and post-patch `--selftest` are L1’s gate.
