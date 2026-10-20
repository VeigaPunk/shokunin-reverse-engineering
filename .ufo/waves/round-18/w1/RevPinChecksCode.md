# RevPinChecksCode — mid-map retention: exact lines, and the 16-receipt compatibility gate

Author-side advisory (round 18, W1), addressed to `CarrierRunMidMaps`. Read-only: this file is my
only lane write; no REA/Ghidra run, no carrier executed, no tool edited, no receipt touched.
Contract anchors: `.ufo/waves/round-18/contract.md:128-131`, defect `.ufo/waves/round-17/...` is
routed at `corpus/lessons/round-17-verifier-spotcheck.md:137`, executor brief
`.ufo/waves/round-18/gen-wave1.py:107-114`.

Axes: **calibration** — R17-PINMAP is discharged only if the new claim is true of retained bytes, not
of prose; **operability** — a retained verdict must be re-derivable without rerunning the carrier;
**depth** — the recorded `equal` becomes a consequence of a digest-anchored map instead of a
free-floating boolean.

## 1. What exists now (observation)

- `.ufo/waves/round-17/tools/carrier-run.py:481-487` appends
  `{taken_at_utc, equal, entries:int, changed, missing}` and discards `mid["entries"]` after
  `len(...)` at `:484`.
- Census over the 8 working-tree receipts: **29** `pin_checks` objects, every one with exactly
  `('changed','entries','equal','missing','taken_at_utc')`; `entries` is an int (146 = 143 Go typeinfo
  JSONs, verified by `find .../typeinfo/golang -type f | wc -l`, + carrier + prediction + selection.py
  in pro-aether/pro-op).
- Census over all 16 receipts (8 working tree + 8 at `da64646`): `map_path` = 0, `map_sha256` = 0.
  The 8 archived first-pass receipts have **zero** `pin_checks` keys at all.
- No `runs/*/pins/` directory exists anywhere. So today the recorded verdict is unfalsifiable: nothing
  anchors `equal` to bytes.
- `.ufo/waves/round-17/tools/receipt-validate.py:119-123` validates shape and `equal is True` only;
  `:304-314` already verifies any `<stem>_path` + `<stem>_sha256` sibling pair generically.

## 2. Baseline commands and exits (observation)

| command | exit | output |
|---|---|---|
| `python3 -I .ufo/waves/round-17/tools/carrier-run.py --selftest` | 0 | `SELFTEST: CLEAN cases=2` |
| `python3 -I .ufo/waves/round-17/tools/receipt-validate.py --selftest` | 0 | `SELFTEST: CLEAN cases=9` |
| `python3 -I .../receipt-validate.py <each of runs/*/receipt.json>` | 0 ×8 | `valid: true`, 343-349 checks each |
| same, 8 receipts at `git archive da64646 .ufo/waves/round-17/runs`, runs-prefix remapped to a `/tmp` copy | 0 ×8 | no findings |

The per-file command was:

```
for r in .ufo/waves/round-17/runs/*/receipt.json; do
  python3 -I .ufo/waves/round-17/tools/receipt-validate.py "$r" >/dev/null 2>&1
  echo "$? $r"
done
```
Output: eight `0 runs/<label>/receipt.json` lines, plus one `2` for the phantom path described below.

The archived run harness (Python, writing only under a `/tmp` mkdtemp):

```
git -C <lane> archive da64646adcb19c1ede7537b799b8c7d283fe43da .ufo/waves/round-17/runs \
  | tar -x -C <tmp>
# copy each receipt with "<lane>/.ufo/waves/round-17/runs" -> "<tmp>/.ufo/waves/round-17/runs"
subprocess.run(["python3","-I",W17+"/tools/receipt-validate.py", remapped_receipt])
```
Output: `[0, 0, 0, 0, 0, 0, 0, 0]`, zero findings each.

The archived pass-1 receipts were validated from `git archive da64646adcb19c1ede7537b799b8c7d283fe43da`
extracted to `/tmp` (same idiom `Validate16Run` is chartered to use; written outside the lane). Do not
mistake these for lane writes.

Field census command that produced the numbers above (Python `glob`, not a shell glob; `arch` is the
`/tmp` extraction of the `da64646` tree):

```python
import glob, json
W17 = '.ufo/waves/round-17'
wt = sorted(glob.glob(W17 + '/runs/*/receipt.json'))
arch = sorted(glob.glob('/tmp/revpin-arch-*/.ufo/waves/round-17/runs/*/receipt.json'))
hits, total, keysets = [], 0, set()
for p in wt + arch:
    raw = open(p).read()
    hits += [(p, k) for k in ('map_path', 'map_sha256') if k in raw]
    r = json.loads(raw)
    for s in (r.get('steps') or {}).values():
        for c in s.get('pin_checks') or []:
            total += 1
            keysets.add(tuple(sorted(c)))
print(len(wt), len(arch), total, keysets, hits)
```
Observed output: `8 8 29 {('changed', 'entries', 'equal', 'missing', 'taken_at_utc')} []`.
Observed anomaly: this tool's temporary shell expanded `runs/*/receipt.json` to a phantom ninth path
`runs/run-log.txt/receipt.json` (exit 2). `find`, `stat`, and Python's `glob` all agree the path does not
exist (`run-log.txt` is a regular file, 1222 bytes). [inference] wrapper-shell glob artifact, not repo
state. Use `find ... -name receipt.json` or Python for the census so a phantom does not read as a red
receipt.

## 3. Exact lines to change — `.ufo/waves/round-17/tools/carrier-run.py`

| anchor | change |
|---|---|
| `:18-29` imports | add `import itertools` between `import importlib.util` (`:22`) and `import json` (`:23`) |
| `:368` (before the closure) | define one run-wide counter, `mid_seq = itertools.count(1)` |
| `:369-371` closure `run_polled` | pass `mid_seq` into `_run_polled` |
| `:437-438` `_run_polled` signature | add `mid_seq` parameter |
| `:473-475` comment | say the map is written to `<out_dir>/pins/mid-<n>.json`, not only that the instant is retained |
| `:476-492` pin block | build the check dict, write the map atomically, attach `map_path`/`map_sha256`, or `map_error` |
| `:601-623` selftest case 1 `ok` tuple | assert map presence, digest round-trip, and one file per check (unique names) |
| `:411-414`, `:423-424` | unchanged — `pins_changed_during_run`/`equal` semantics stay |

Writer block (replaces `:476-492`; `sha256_file` is at `:52-57`, `json`/`os` already imported):

```python
            now = time.monotonic()
            if now - last_pin_check >= PIN_CHECK_S:
                last_pin_check = now
                mid = pins.snapshot(pin_paths)
                cmp_mid = pins.compare(pins_pre, mid)
                check = {
                    "taken_at_utc": mid["taken_at_utc"],
                    "equal": cmp_mid["equal"],
                    "entries": len(mid["entries"]),   # int; never the map itself
                    "changed": cmp_mid["changed"],
                    "missing": cmp_mid["missing"],
                }
                # R17-PINMAP: retain the map the verdict came from. Atomic write;
                # a failed write is recorded, never claimed.
                tmp_path = None
                try:
                    pins_dir = os.path.join(out_dir, "pins")
                    os.makedirs(pins_dir, exist_ok=True)
                    map_path = os.path.join(pins_dir, "mid-%d.json" % next(mid_seq))
                    tmp_path = map_path + ".tmp"
                    with open(tmp_path, "w", encoding="utf-8") as f:
                        json.dump(mid, f, sort_keys=True, indent=2)
                        f.write("\n")
                    os.replace(tmp_path, map_path)
                    check["map_path"] = map_path
                    check["map_sha256"] = sha256_file(map_path)
                except OSError as e:
                    check["map_error"] = "%s: %s" % (type(e).__name__, e)
                    if tmp_path:
                        try:
                            os.unlink(tmp_path)
                        except OSError:
                            pass
                rec.setdefault("pin_checks", []).append(check)
                if not cmp_mid["equal"]:
                    rec["pins_changed_during_run"] = {
                        "changed": cmp_mid["changed"],
                        "missing": cmp_mid["missing"],
                    }
```

Closure and signature:

```python
    mid_seq = itertools.count(1)   # one counter per run: names must never collide
    def run_polled(name, argv):
        return _run_polled(name, argv, out_dir, cwd, timeout, poll, runner,
                           poller, pins, pins_pre, mid_seq)
...
def _run_polled(name, argv, out_dir, cwd, timeout, poll, runner, poller, pins,
                pins_pre, mid_seq):
```

Selftest case 1 (`:609-623`) additions:

```python
            and os.path.isfile(os.path.join(out_dir, "pins", "mid-1.json"))
            and all(c.get("map_path")
                    and c.get("map_sha256") == sha256_file(c["map_path"])
                    for s in receipt["steps"].values()
                    for c in s.get("pin_checks") or [])
            and len([c.get("map_path") for s in receipt["steps"].values()
                     for c in s.get("pin_checks") or []])
                == len({c.get("map_path") for s in receipt["steps"].values()
                        for c in s.get("pin_checks") or []})
```

Case 1 runs `analyze` + `search:main.main`, so the last assertion is also the collision guard: two
steps, distinct map files.

## 4. Exact lines to change — `.ufo/waves/round-17/tools/receipt-validate.py`

| anchor | change |
|---|---|
| `:113-116` (after `_iter_steps`) | insert `check_mid_map()` below |
| `:119` | `def check_binding(receipt, pins, findings):` |
| `:120-123` docstring | add: a check with `map_path` must carry a matching digest and re-derive its verdict against `pins_pre`; without map fields it stays verdict-only (r17 shape) |
| `:181` (before the steps loop) | `pre_map = receipt.get("pins_pre")` |
| `:187-191` loop body | keep the `equal is True` gate; call `check_mid_map` for every dict check |
| `:448` | `checks += check_binding(receipt, pins, findings)` |
| `:692-701` (after case 4c) | add cases 4f/4g/4h/4i below |
| `:55-68` required-field lists | **unchanged** — no `map_path`/`map_sha256` requirement |
| `:458` `walk_pairs` call | unchanged; `:304-314` already recomputes `map_sha256` generically |

Helper (insert after `:116`):

```python
def check_mid_map(pre, chk, where, pins, findings):
    """Re-derive a retained mid-run map (R17-PINMAP): recompute its digest, then
    recompare it with the recorded pre map and cross-check the recorded verdict.
    A check without map fields is the r17 shape and stays verdict-only."""
    path = chk.get("map_path")
    sha = chk.get("map_sha256")
    if chk.get("map_error"):
        findings.append({"code": "mid_map_unretained", "where": where,
                         "path": path, "error": chk["map_error"]})
        return 1
    if path is None and sha is None:
        return 0                      # retained r17 receipt: no map was ever claimed
    if not (isinstance(path, str) and isinstance(sha, str) and len(sha) == 64):
        findings.append({"code": "mid_map_shape", "where": where,
                         "path": path, "map_sha256": sha})
        return 1
    if os.path.islink(path) or not os.path.isfile(path):
        findings.append({"code": "mid_map_missing", "where": where, "path": path})
        return 1
    try:
        actual = sha256_file(path)
    except OSError as error:
        findings.append({"code": "mid_map_unreadable", "where": where,
                         "path": path, "error": str(error)})
        return 0
    checks = 1
    if actual != sha:
        findings.append({"code": "mid_map_mismatch", "where": where,
                         "path": path, "expected_sha256": sha,
                         "actual_sha256": actual})
        return checks
    if not isinstance(pre, dict) or pins is None:
        return checks
    try:
        with open(path, "r", encoding="utf-8") as handle:
            mid = json.load(handle)
        recomputed = pins.compare(pre, mid)
    except (OSError, ValueError, AttributeError) as error:
        findings.append({"code": "mid_map_unreadable", "where": where,
                         "path": path,
                         "error": "%s: %s" % (type(error).__name__, error)})
        return checks
    checks += 1
    for field in ("equal", "changed", "missing"):
        record = chk.get(field)
        expect = recomputed.get(field)
        if field in ("changed", "missing") and isinstance(expect, list):
            match = isinstance(record, list) and sorted(record) == sorted(expect)
        else:
            match = record == expect
        if not match:
            findings.append({"code": "mid_map_verdict_mismatch", "where": where,
                             "field": field, "recorded": record,
                             "recomputed": expect})
    return checks
```

Loop (replaces `:187-191`):

```python
        for i, chk in enumerate(step.get("pin_checks") or []):
            checks += 1
            if not (isinstance(chk, dict) and chk.get("equal") is True):
                findings.append({"code": "mid_run_pin_drift",
                                 "where": f"{where}.pin_checks[{i}]"})
            if isinstance(chk, dict):
                checks += check_mid_map(pre_map, chk, f"{where}.pin_checks[{i}]",
                                        pins, findings)
```

Selftest cases to add after `:701`:

- **4f r17-shape green** — the exact 5-key check (`equal: True`, no map fields) → exit 0. This is the
  permanent regression guard for the 16 retained receipts; do not fold it into case 4.
- **4g map green** — write `mid-1.json` as `json.dumps(receipt["pins_pre"], sort_keys=True, indent=2) +
  "\n"`, add `map_path`/`map_sha256` to the check → exit 0.
- **4h tampered map red** — mutate one entry's `sha256` inside the map file → exit 1 **and** assert the
  finding code set contains `mid_map_mismatch`. Asserting only exit 1 passes for the wrong reason:
  `walk_pairs` (`:304-314`) already emits generic `sha256_mismatch` for any tampered `*_path` pair, so
  the test would stay green even if the new recompare were never wired.
- **4i shape/missing/error red** — `map_path` without `map_sha256` → `mid_map_shape`; `map_path` to an
  absent file → `mid_map_missing`; a recorded `map_error` → `mid_map_unretained`.

The tampered-map red case belongs only in the validator. A writer cannot test tampering meaningfully
without importing the validator; carrier-run's red-side obligation is the "failed write is recorded,
never claimed" branch (`map_error`), plus the collision assertion in case 1.

## 5. Backward-compatibility risk for the 16 retained receipts

Shape matrix (observed):

| set | revision | `pin_checks` | map fields | exit today |
|---|---|---|---|---|
| 8 working tree | `9011581` (clean for these tools) | 29 objects, 5 keys | 0 | 0 ×8 |
| 8 archived | `da64646` | none | 0 | 0 ×8 (`runs` prefix remapped) |
| `verify/replicate/calib-shfmt` | worktree | 2 objects, 5 keys | 0 | not one of the 16; same shape |

Rules that keep all 16 green:

1. **No new required fields** — leave `CARRIER_REQUIRED`/`CARRIER_STEP_REQUIRED` (`:60-68`) alone.
2. **Absence of both map keys = r17 behaviour**, zero checks, zero findings (the `check_mid_map` gate).
   This is permanent, not a migration shim: the round-18 non-goal forbids editing r17 receipts, so the
   8 pass-2 receipts can never acquire maps honestly.
3. **`entries` stays an int.** Overloading it with the map is the one silent way to break the old shape;
   `mid_run_drift_steps` also reads `equal`, not the map.
4. **Add only.** Do not rewrite any retained receipt; do not relax or tighten the existing `equal`
   branch for map-less checks.
5. New finding codes (`mid_map_*`) may only fire on receipts written after the fix.
6. Retained maps are files under the run dir; they must be delivered with the receipt. The
   absolute-path remap idiom used for the `da64646` re-validation now has to cover `pins/` for any
   future receipt. `measure.py:54` matches only `runs/<label>/receipt.json`, so the new tree does not
   disturb the C1 census; `.gitignore` does not exclude `pins/`, so maps are tracked.

Risk that remains after the change: none of the 16 gains a finding, because the new code paths are
presence-gated; what changes is only that a *future* receipt claiming a verdict must ship the map that
produces it. The acceptance command is unchanged: the 8 working-tree receipts must each still exit 0
(`gen-wave1.py:110-113`), and the `da64646` set must still exit 0 under the committed validator
(`Validate16Run`).

## 6. Traps, ranked

1. **Per-step counters collide.** `_run_polled` is called for `analyze` and each `--search`. A local
   counter would make the search step's `mid-1.json` overwrite `analyze`'s, and the earlier check's
   `map_sha256` would no longer match the file: a clean run validates red. One run-wide counter.
   (`run-carriers.sh` passes no `--search` today, so this is latent, not hypothetical.)
2. **Gate order.** `map_error` must be tested before "both keys absent", otherwise a failed retention is
   indistinguishable from an r17 receipt and passes green — the exact overstatement being corrected.
3. **Tampered-map test for the wrong reason** — see 4h.
4. **The generic walk never checks the verdict.** `walk_pairs` recomputes the digest only; only
   `check_mid_map` re-derives `equal`/`changed`/`missing` from the map. Test 4g with a map whose entries
   disagree with `pins_pre` while its digest is correct → `mid_map_verdict_mismatch`; the generic walk
   cannot catch this.
5. **Duplicate verification is expected** (`walk_pairs` + helper, 2 checks per map). Do not rename the
   fields to dodge it: the contract fixes `map_path`/`map_sha256`, and the sibling convention is what
   makes the digest recompute free.
6. **Size.** A 146-entry map serializes to ~40 KB (`pro-aether` pre map measured at 40,391 B with the
   writer's `sort_keys=True, indent=2`). 29 r17 checks would have been ~1.2 MB; W18's 8 carriers at one
   map per ~30 s stay well under 10 MB. Receipt growth is ~100 B per check.
7. **Stale prose.** Update `carrier-run.py:473-475` and `receipt-validate.py:120-123`; both still state
   the verdict-only semantics.

## 7. Residual risk and limits (label: inference where marked)

- The digest binds the verdict to bytes **as recorded by the run**; a receipt author who consistently
  rewrites `pins_pre`, the map and `map_sha256` can still assert anything. What the change removes is the
  free-floating verdict (today `equal` has no anchor at all). It does not create an append-only witness;
  QUALITY #19 should not be read as more than "re-derivable from the receipt".
- Polling-copy limit (`carrier-run.py:9-12`) is unchanged: mid maps are instants, not continuous proof.
- `pins.compare` ignores `mtime_ns`; a same-bytes restore between instants remains undetectable
  (unchanged). A step that exits before the loop's first test can carry no check and no map; the
  validator correctly does not require one.
- No tools installed, no carrier executed, no REA/Ghidra invocation.

## 8. Hand-off checklist for `CarrierRunMidMaps`

```
python3 -I .ufo/waves/round-17/tools/carrier-run.py --selftest            # exit 0
python3 -I .ufo/waves/round-17/tools/receipt-validate.py --selftest     # exit 0, cases >= 13
for r in $(find .ufo/waves/round-17/runs -maxdepth 2 -name receipt.json); do
  python3 -I .ufo/waves/round-17/tools/receipt-validate.py "$r" >/dev/null; echo "$? $r"; done  # eight 0
git -C . status --porcelain .ufo/waves/round-17/runs                    # empty
git -C . diff --stat -- .ufo/waves/round-17/tools/carrier-run.py \
  .ufo/waves/round-17/tools/receipt-validate.py                         # only these two files
```

Advisory sent to `KaidokuR18.CarrierRunMidMaps` with traps 1-5 in short form.
