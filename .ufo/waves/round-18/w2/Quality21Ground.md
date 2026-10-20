# QUALITY #21 grounding — Quality21Ground (wave 2, falsify)

HOLDS — #21 is grounded in round-18 Mistakes row 1 with a reproduced red-before; it is not a restatement of #19; it would have caught the r17 sentence. One caveat kept honest: the glob invocation specified for this check exits 2 (unreadable), not 1/0; the claimed exits hold when the receipts are enumerated.

All anchors at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` unless suffixed with another revision. `git rev-parse HEAD` = REV; `git status --porcelain` lists only untracked wave-2 files (`gen-wave2.py`, `w2/`, `wave2-*.json/txt`), so every tracked file read in the live tree is byte-identical to REV. No tools installed (python3 3.14, git, find preinstalled; pacman-pause rule respected).

## 1. Grounding (observation unless labeled)

- Lesson: `corpus/lessons/round-18.md:62` — Mistakes row 1, class `vacuous`, fix column names QUALITY #21 + the forward fix.
- The lesson's own citations resolve at REV: `corpus/lessons/round-17-verifier-spotcheck.md:108` (outside sample: r17 `pin_checks` → `{changed,entries,equal,missing,taken_at_utc}`; **partial disagree** on the pin sentence) and `:137` (R17-PINMAP: mid-run `pin_checks` retain `{taken_at_utc, equal, entries:int, changed, missing}`, "not per-path maps").
- Producer ground truth at the capture revision `9011581`: `.ufo/waves/round-17/tools/carrier-run.py:481-487` appends exactly `{taken_at_utc, equal, entries, changed, missing}` — no map; the `(QUALITY #19)` tag sits at `:475` in that revision.
- The `9011581` validator accepted verdict-only entries without recomputation: `receipt-validate.py:187-191` at `9011581` checks only `chk.get("equal") is True` and never recomputes `entries` against `pins_pre`. [OBSERVATION — direct source read] This grounds #21's last sentence ("a verdict-only record the validator accepts without recomputation is stated as accepted, not verified") and the "forged verdict-only check accepted by the `9011581` validator" red in the why column of `corpus/QUALITY.md:31`.
- Append-only corrections are in place: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:200-205` (the `:30-32` sentence named and corrected; the `recheck:` line at `:3` named as overstating the `9011581` validator).

## 2. Red-before runs (each command pasted with its exit code)

Enumerated form (the reproducing form):

```text
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    $(find .ufo/waves/round-17/runs -mindepth 2 -maxdepth 2 -name receipt.json | sort)
→ counts {receipts: 8, valid: 0, invalid: 8, unreadable: 0}; R17_EXIT=1
  findings: 29 × mid_map_missing (per receipt 4,2,3,2,4,4,2,8 = every second-pass
  pin_checks entry; calib-shfmt and pro-notesmd-cli 2 … pro-op 8 — matches the
  entry's "2–8 checks per run" and round-18.md:51 "29/29 second-pass checks")
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    $(find .ufo/waves/round-18/runs -mindepth 2 -maxdepth 2 -name receipt.json | sort)
→ counts {receipts: 15, valid: 15, invalid: 0, unreadable: 0}; R18_EXIT=0
  22 mid-run maps recomputed digest-clean (matches
  corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:68 "15/15 exit 0, 22
  mid-run maps recomputed"); r18 pin_checks keys observed:
  {changed, entries, equal, map_path, map_sha256, missing, taken_at_utc}
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest
→ exit 0 (all fixtures green, incl. forged-verdict-entry reds expected at
  receipt-validate.py:976-995; docstring "Exits 0/1" at :748)
```

Glob form exactly as specified in the assignment — **does not reproduce 1/0**:

```text
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-17/runs/*/receipt.json
→ EXIT=2  (counts {receipts: 9, invalid: 8, unreadable: 1}; the extra path is
  `.ufo/waves/round-17/runs/run-log.txt/receipt.json`, "[Errno 20] Not a directory")
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-18/runs/*/receipt.json
→ EXIT=2  (counts {receipts: 16, valid: 15, unreadable: 1}; same cause)
```

Cause [OBSERVATION]: bash globbing matches the file `run-log.txt` as a path component and appends `/receipt.json` with no existence check; `validate_paths` precedence is unreadable→2, invalid→1, else 0 (`receipt-validate.py:649-653`). Impact [INFERENCE]: none on the lane's recorded claims — every recorded form is per-receipt or enumerated (`predictions/decision-rule.json:2` "exits 0 on its receipt"; `.ufo/waves/round-18/w1/CarrierRunMidMaps.md:166` "8 receipts → 1 — invalid: 8, mid_map_missing"; knowledge entry `:68` "15/15 exit 0"). It is a recheck trap, not a lane misstatement: any future glob-form recheck of either round exits 2 regardless of substance — the exact hazard QUALITY #18's "recheck guidance … matches the exercised … paths" targets. Smallest safe correction: always replay with the enumerated/find-form argv above.

## 3. Restatement of #19? No.

- #19 (`corpus/QUALITY.md:29` at REV) regulates *temporal-stability* statements and conditions admission on the tool keeping each pin map. The r17 sentence is rejectable under #19 only by derivation, and in practice #19 failed to catch it: the entry was admitted with the `(QUALITY #19)` tag (`9011581` `carrier-run.py:475`) and the outside sample only partially disagreed (`round-17-verifier-spotcheck.md:108`). Mistakes row 1 records exactly this: "QUALITY #19 by text; not applied (the tag was self-attestation)".
- #21 (`corpus/QUALITY.md:31` at REV) adds four things absent from #19: (a) scope — any retention/compliance statement about producer output, explicitly including inline `(QUALITY #N)` tags; (b) a mechanical recheck command that prints the keys actually retained at the measured revision, with "it names only those keys"; (c) verdict ≠ compared-object naming rule (`equal`/`changed`/`missing`/count never described as the map/bytes/file); (d) validator discipline — exit 0 described only by recomputed fields, accepted ≠ verified. (b)–(d) are grounded in the `9011581` sources in §1. The supersedes column "sharpens 19" is accurate; no duplicate-authority conflict found (#18's argv retention is complementary; #19 remains in force for temporal claims).

## 4. Would #21 have caught the r17 sentence? Yes, mechanically.

The sentence (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` at REV; filed bytes intentionally unchanged, corrected at `:200-205`): "In the second pass each pin map is retained with its UTC instant: pre, every 30 s during analyze (2–8 checks per run, `steps.analyze.pin_checks`), and post. All maps are equal."

At the r17 producer revision the tool actually retained keys `{taken_at_utc, equal, entries, changed, missing}` (`9011581` `carrier-run.py:481-487`; `round-17-verifier-spotcheck.md:137`). Under #21: (i) "each pin map is retained" names an object ("map") absent from the retained key set, with no recheck command printing it — inadmissible; (ii) "All maps are equal" describes the `equal` verdict as the compared objects — verdict-as-object violation. The same rule catches the inline tag (`9011581` `:475`) and the `SCORECARD.md:2374` wording (`:137` lists all three sites). [INFERENCE for the counterfactual "would have caught" — rule text applied to observed retained keys and observed sentence; the fix-day behavior is evidenced by the reproduced red in §2: the validator now demands `map_path`+`map_sha256` per check (`receipt-validate.py:493-498`) and recomputes them.]

The appended correction (`:204`) is itself #21-conformant: "mid-run instants retain the comparator verdict against the retained pre map" names only genuinely retained objects (the pre map; the verdict set).

## 5. Minor findings

- `corpus/lessons/round-18.md:62` cites "`carrier-run.py:475` even tagged "(QUALITY #19)"" with no revision qualifier. `:475` is correct at the capture revision `9011581`; at REV the tag sits at `:482` and REV `:475` is the timeout-deadline check. Smallest safe correction: an append-only qualifier "at `9011581`". Cosmetic; the anchor resolves in the revision the row is about.
- No installs performed; no lane file other than this report written; no `jj`/git writes run (read-only `git rev-parse`, `git status`, `git show`, `git grep` only).
