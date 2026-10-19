# EX-2 — C1 `ptr_check` blind spot

**Status: DISCREPANCY.** The collection blind spot is reproduced and the one-hunk patch catches a seeded dead pointer on an isolated scratch tree. However, the frozen claim’s clean-tree precondition does not hold for the actual current source pointer: the pointer matched at `PROVINCE.md:18` is `:3546`, and its live target is stale. The named `:3298` is only an unqualified historical suffix on that line, not a match for `PTR`.

## First-hand source and baseline

- `git rev-parse HEAD` → `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`.
- `sha256sum .ufo/gates/c1-census-v10.py` → `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`; `wc -l` → `713`.
- `.ufo/gates/c1-census-v10.py:498-515` collects `PTR` only inside `if not occ`; `PIN` and bare `VER` populate `occ` first. This confirms the mechanism of the blind spot.
- Direct parse of `PROVINCE.md:18` with the gate’s own regexes: `PIN.findall` → `['6.7.0']`; `PTR.findall` → `[('~/.kimi-code/config.toml', '3546')]`. The text later says “receipt's pointer :3298”, but that suffix alone does not match `PTR` (`:311`). `classify()` at HEAD returns block `15-26`, `disp=info`, with only the `pin` assertion at line 18 (`current-ok`); it returns no pointer assertion there.
- Direct live anchors and pointer checks, via `live_pins()` / `ptr_check()` from this gate:

```text
live_pins: {"devin": "6.5.0", "kimi": "6.7.0", "omp": "6.5.0"}
ptr_check(~/.kimi-code/config.toml,3298): ('stale', 'line holds no rea-agents pin: \'model = "step-5-preview"\'')
ptr_check(~/.kimi-code/config.toml,3546): ('stale', "line holds no rea-agents pin: 'max_output_size = 64000'")
```

The current full-path citation is therefore `:3546`, not `:3298`; both offsets were checked first-hand, and neither target currently holds the pin.

Unmodified command `python3 .ufo/gates/c1-census-v10.py --json` returned `PASS`, with counts `PROVINCE.md={lines:162,loci:6}`, `SCORECARD.md={lines:1757,loci:9}`, `SKILL.md={lines:413,loci:2}`, 14 frontier rows / `[]` errors, and `current_ok_per_file={PROVINCE.md:17,SCORECARD.md:14,SKILL.md:3}`. The PASS does not evaluate the line-18 pointer.

## Candidate patch text (scratch only; gate not edited)

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@
-        if not occ:
-            for m in PTR.finditer(text):
-                occ.append(("ptr", m.start(), m.group(0)))
+        for m in PTR.finditer(text):
+            occ.append(("ptr", m.start(), m.group(0)))
```

This removes the occupancy short-circuit while retaining the existing `occ` path, classification, output fields, and G21 code. It is not merge-ready as a complete C1 solution: the current tree exposes pre-existing stale pointers and requires a defensible receipt classification before the frozen clean-PASS condition can be claimed.

## Scratch measurements

Scratch root and instrument copy: `/var/tmp/kaidoku-ex2-c1.AEG5wS/` (no `/tmp`; only the copied instrument was patched). On the actual current documents, running that patched copy with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --json` returned exit 1 / `FAIL`, with two stale records:

- `PROVINCE.md:18`, `~/.kimi-code/config.toml:3546` → `STALE`, `line holds no rea-agents pin: 'max_output_size = 64000'`.
- `SCORECARD.md:291`, `~/.kimi-code/config.toml:1478` → `STALE`, `line holds no rea-agents pin: ''`; this line lies in the gate’s DATED `SCORECARD.md:273-326` scope.

Despite that failure, the JSON schema stayed at 19 keys with identical key sets before/after. G21 stayed `(14, [])`; G2 stayed `(True, '1/readable-file')`. `current_ok_per_file` changed from `{PROVINCE.md:17,SCORECARD.md:14,SKILL.md:3}` to `{PROVINCE.md:19,SCORECARD.md:16,SKILL.md:3}` as pointer detections were added. Thus the counters/fields remain present, but new pointer evidence changes counts as expected.

For an end-to-end controlled fault test, the scratch fixture `/var/tmp/kaidoku-ex2-c1.AEG5wS/fixture/` used a non-secret `/var/tmp/kaidoku-ex2-c1.AEG5wS/config.toml` with line 1 containing `rea-agents@6.7.0` and line 2 `other = "no package pin"`. Only the two config citations in the scratch documents were pointed at line 1 to make a clean control; the real repository was not changed. Results from `python3 <instrument> --root /var/tmp/kaidoku-ex2-c1.AEG5wS/fixture --json`:

```text
clean fixture, HEAD instrument:   exit 0, PASS, stale=0, G21=(14, []), G2=True
clean fixture, patched copy:      exit 0, PASS, stale=0, G21=(14, []), G2=True
seeded line-2 pointer, HEAD:      exit 0, PASS, stale=0
seeded line-2 pointer, patched:   exit 1, FAIL, stale=1, G21=(14, []), G2=True
```

The seeded pointer was inserted next to the 6.7.0 pin in the same pin-carrying clause; line 1 remained present. The patched result contains, at `PROVINCE.md:18`, the pin `6.7.0` as `current-ok`, `/var/tmp/kaidoku-ex2-c1.AEG5wS/config.toml:1` as `current-ok` (`pins 6.7.0`), and `...config.toml:2` as `STALE` (`line holds no rea-agents pin: 'other = "no package pin"'`). This reproduces the before-PASS / after-FAIL fault catch on the scratch tree. The controlled fixture is not evidence that the actual tree’s stale pointer is current.

## Receipt-anchor limitation and item verdicts

`PROVINCE.md:18` names the `17:55:49Z` receipt; `.ufo/gates/citation-drift/pointer-table.json:21-34` binds that stamp to `PROVINCE.md:18` and the receipt path. But `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt:1-6` contains the timestamp and five path hashes, including the config hash, not a captured config snapshot or the pin’s line content. It cannot validate the current `:3546` target. Also, the text labels `:3298` as the receipt’s pointer while the only full path:line matched on the current line is `:3546`.

- **Blind-spot mechanism — VERIFIED:** pointer enumeration is skipped whenever a pin/version was already found; baseline line-18 `ptr` detections = 0.
- **Frozen exact locus `:3298` — CORRECTED:** direct `ptr_check(:3298)` is stale, but current `PTR.findall(PROVINCE.md:18)` finds only `:3546`; `:3298` is not a full-path match in the current text.
- **Seeded fault catch — REPRODUCED:** the patched scratch entrypoint changes the fixture from PASS to FAIL on the single dead line-2 pointer while retaining the valid line-1 pointer and G21.
- **Actual current-tree patched PASS — DISCREPANCY / UNVERIFIABLE as specified:** the patch detects the stale current full-path pointer at `PROVINCE.md:18`; it also detects a stale pointer in a DATED `SCORECARD` block. The available hash receipt does not authenticate the current pointer’s target contents. No receipt-based exception was added because that would mask a measured stale locus without evidence.
- **G21 and JSON counter inventory — VERIFIED:** G21 remains 14 rows with no errors; the 19 JSON keys are unchanged by the candidate hunk.

No gate, corpus, PROVINCE, SCORECARD, SKILL, LOG, or other tracked file was modified. The patch exists only as text here; its executable copy and all fixtures are under `/var/tmp`.