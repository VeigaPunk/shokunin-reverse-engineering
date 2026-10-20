# CriticDiscernment: attack on the planned round-18 discernment verdict (QUALITY #21)

Author-side advisory seat. This is not an outside review, and it cannot stand in for the round-18 non-author spot-check (`LEARNING.md:42-46`). I wrote only this file. Installs: none.

Axes judged: calibration, operability, depth.

## Verdict in one line

As planned, #21 has a lesson behind it, but it is **not yet grounded**:
- The r17 miss was not a missing criterion. #19 already required the mid-run map, and the entry cited #19 inline while failing it.
- The drafted row is again prose that an author gate can "satisfy" by naming the fields.
- The C1 counter cannot tell a grounded row from an empty one.

Discernment credit through LEARNING's second disjunct needs:
- the red-before evidence in §4;
- an honest `captured-by` line in round-18.md.

## 1. Counterexample: #19 existed, was cited, and failed

- **[Observation]** QUALITY row 19 at `d0ab299` already says "the producing tool keeps each pin map (per-path SHA-256 and size) with its UTC timestamp and the comparison verdict, **including mid-run checks**" (`corpus/QUALITY.md:29`).
  - Command: `git show d0ab299:corpus/QUALITY.md | grep -E '^\| 19 \|' | grep -oE 'including mid-run checks|…'` printed `including mid-run checks` (exit 0).
- **[Observation]** The same commit `d0ab299` wrote the pin sentence. It tags its own compliance inline: "each pin map is retained … All maps are equal … (QUALITY #19)" (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-33`).
  - Command: `git log … -- corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` lists `d0ab299` and `da64646` (exit 0).
- **[Observation]** The producer at B appends only `{taken_at_utc, equal, entries, changed, missing}` (`git show 9011581:.ufo/waves/round-17/tools/carrier-run.py`, lines 481-487). Its comment at `:475` also self-tags "(QUALITY #19)".
- **[Observation]** At B, all 8 receipts hold 29 mid checks in total, each with exactly that key set; every `equal` is true. Pre and post keep full maps (`pins_pre` has keys `entries, monotonic_ns, taken_at_utc` and 146 entries). Command and output are in §5.
- **[Observation]** This is the third occurrence of the class "a temporal or retention claim outruns the retained fields":
  1. R16-PROVENANCE (`corpus/lessons/round-17.md:81`);
  2. the `da64646` recurrence, "pins equal pre/mid/post", whose mid checks were recorded only on drift (`round-17.md:90`, where captured-by reads "QUALITY #18 (did not catch it); #19 now does");
  3. R17-PINMAP in `d0ab299` (`round-17-verifier-spotcheck.md:108,137`).

  Each was answered with wording in a criterion, and the class recurred anyway.
- **[Inference]** `LEARNING.md:19-21` adds a criterion "when no criterion caught it". Here a criterion covered the case by text, but the gate never checked the claim against the producer's fields. A #21 that restates "retain the mid map" is a **duplicate authority** of #19. It is not new discernment.

## 2. Counterexample against the drafted row (`w1/DraftQualityRow21.md:10`)

- **[Inference]** The draft says "A retention claim names each field the producing tool retains …". The B sentence *does* name its fields: "pin map … with its UTC instant". It was simply false. A gate that reads prose would pass it under #21, exactly as it passed it under #19.
  - The row has no procedure that compares the named fields with the producer's emitted key set at the measured revision.
- **[Inference]** The parenthetical "(for a pin check: `taken_at_utc`, the per-path map with SHA-256 and size, and the comparator verdict)" restates #19's content (`QUALITY.md:29`). That makes two rows that govern pin-map retention and that can drift apart.
- **[Observation]** The `recheck:` header of the entry (`…r17-go-carrier-diagnostics.md:3`) says "exit 0 = digests, pins, log binding and **mid-run checks consistent**". The validator at B only tests `chk.get("equal") is True` (`git show 9011581:…/receipt-validate.py`, lines 187-191). It accepts a forged verdict (§5, run 3).
  - This is the same verdict-as-object overstatement in a fourth place. It is **not routed** by R17-PINMAP (`round-17-verifier-spotcheck.md:137` names only entry:30-32, SCORECARD:2374 and #19).
- **[Observation]** The contract's forward fix keeps r17 behaviour when fields are absent (`contract.md:128-130`).
  - **[Inference]** So an r18-produced receipt whose `pin_checks` lack `map_path`/`map_sha256` is still accepted. That is a silent downgrade path, and #21 would claim to prevent this very gap.

## 3. Counterexample against the C1 counter

- **[Observation]** R17-PINMAP check (c) passes for any admission-table row whose why-cell contains `round-17-verifier-spotcheck.md` and `R17-PINMAP` (`contract.md:31`). The `falsifiable_before_after` for the criterion is "QUALITY data rows 20 -> 21" (`claims.json:13`).
- **[Inference]** A row reading `| 21 | x | round-17-verifier-spotcheck.md R17-PINMAP | — |` closes C1. Neither measure can separate grounded from ungrounded, so neither can be cited as discernment evidence. A row count is the "vacuous" class the lane already mines.

## 4. Red-before evidence that would ground #21

Each item is revision-scoped and is red at B = `9011581`. I observed RB-1 to RB-3 (§5). RB-4 is proposed.

| id | check | red at B (observed) | green at the delivered rev |
|---|---|---|---|
| RB-1 claim | `git show REV:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md \| grep -n 'R17-PINMAP\|comparator verdict'` | exit 1 (no correction); lines 30-32 claim "each pin map is retained" | appended correction line (routed-defects check a) |
| RB-2 producer | for each label, `git show REV:.ufo/waves/round-17/runs/<label>/receipt.json \| jq -c '.steps.analyze.pin_checks\|map(keys)\|unique'` | 8/8 labels, 29 checks, key set `[changed,entries,equal,missing,taken_at_utc]`: the claimed object (per-path map) is absent | unchanged (r17 receipts are frozen); the correction now states the actual key set. New r18 receipts carry `map_path`/`map_sha256` |
| RB-3 validator | B `receipt-validate.py` + `pins.py` in mkdtemp, run on a copy of `pro-aether` with forged `pin_checks` (`entries:7`, a 1970 instant, an extra bare `{"equal":true}`) | **exit 0, findings `[]`**: the verdict is accepted with no recomputable object | the r18 validator rejects a tampered mid map (CarrierRunMidMaps red selftest) **and** rejects an r18-shaped receipt that lacks `map_path` (needs the correction in §6.3) |
| RB-4 gate | round-18.md `## Mistakes` row R17-PINMAP, column "able to fail", lists RB-1 to RB-3 with exits, following the `round-17.md:81,90` convention | — | present, with exits pasted |

## 5. Commands run (all read-only for the lane; the temp dir was removed)

```text
# B producer/receipt key sets, all labels (cwd LANE)
for l in $(git ls-tree --name-only 9011581 .ufo/waves/round-17/runs/ | xargs -n1 basename); do git cat-file -e 9011581:.ufo/waves/round-17/runs/$l/receipt.json 2>/dev/null || continue; git show 9011581:.ufo/waves/round-17/runs/$l/receipt.json | jq -c --arg l $l '[$l,(.steps.analyze.pin_checks|length),(.steps.analyze.pin_checks|map(keys)|unique),(.steps.analyze.pin_checks|map(.equal)|all)]'; done | jq -s 'map(.[1])|add'
-> calib-esbuild-0.25.12 4, calib-shfmt 2, pro-aether 3, pro-containerd-shim 2, pro-esbuild-0.21.5 4, pro-esbuild-0.27.7 4, pro-notesmd-cli 2, pro-op 8; every key set ["changed","entries","equal","missing","taken_at_utc"]; all equal true; sum 29   exit=0
git diff --stat 9011581 -- .ufo/waves/round-17/runs/   -> (empty)   exit=0

# RB-1
git show 9011581:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'R17-PINMAP\|comparator verdict'   -> exit=1

# Overstatement sites at B
git grep -nE 'pin maps? (is|are) retained|each pin map|pre/mid/post pin maps|mid maps|maps with instants|Every check is retained' 9011581 -- . ':!*.json'
-> carrier-run.py:475, SCORECARD.md:2374, QUALITY.md:29, knowledge entry:30, spotcheck:108,137   exit=0

# RB-3 forged-verdict acceptance by the B validator
T=$(mktemp -d /tmp/kr18-critdisc-XXXX); git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py > $T/rv.py; ...   -> exit 2 both: "pins.py unavailable" (my setup error)
(retry, with pins.py placed next to receipt-validate.py from B)
orig   exit=0 {"findings":[]}
forged exit=0 {"findings":[]}      # entries 7 vs 146 pinned, timestamp 1970, bare {"equal":true}
rm -rf "$T"   exit=0

# B validator logic
git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | grep -nE 'pin_checks|mid_run|equal'   -> :187-191 checks only chk.get("equal") is True   exit=0
```

An earlier key-set run on the working tree exited 2. The cause was my own jq precedence error plus a glob that matched `runs/run-log.txt`. It was superseded by the B-scoped run above.

## 6. Smallest safe corrections

These are for the L1. The canonical judge decides.

1. **Row text (calibration).**
   - Drop the pin-check parenthetical; #19 already owns it.
   - Keep the general rule: a verdict, count or digest is never named as the compared or hashed object.
   - Add the operative clause #19 lacked: "a retention or compliance claim, including an inline `(QUALITY #N)` tag, is admitted only with a recheck command that prints the producer's retained key set at the measured revision; a validator `exit 0` is described only by the fields it recomputes."
   - Keep `sharpens 19`.
2. **round-18.md Mistakes row R17-PINMAP.**
   - captured-by: "QUALITY #19 by text; the gate accepted the entry's inline `(QUALITY #19)` without reading `pin_checks` keys". It must **not** read "none".
   - able-to-fail: RB-1 to RB-3 with exits.
   - The why-cell of #21 must cite this row. #21 must not land before round-18.md exists (`DraftQualityRow21.md:22`).
3. **Forward-fix gap (operability).**
   - `receipt-validate.py` must require `map_path`/`map_sha256` on receipts from the r18 producer: a schema marker written by the new `carrier-run.py`, or a `--require-mid-maps` flag used by `W18/verify.py`.
   - Add a red selftest: an r18-shaped receipt without the fields fails.
   - Otherwise RB-3 stays green-when-it-should-be-red for new runs.
4. **Unrouted sites.**
   - Append a correction for the entry's `recheck:` gloss "mid-run checks consistent" (line 3).
   - Mark `carrier-run.py:475`'s "(QUALITY #19)" tag as superseded by the r18 map retention. This is **[Inference]**: the comment's "every check is retained" is literally true of the check record. Only its #19-compliance tag is false.
5. **Verdict wording.**
   - r18 `discernment: improved` may cite #21 only after a non-author judges it grounded (`LEARNING.md:35,42-46`). The primary basis stays r18's own sample agreement.
   - If #21 lands without items 1-2, the honest verdict is `unchanged`: the disagreement is learned through correction, but the criterion duplicates #19.
   - It is `harmed` if the why-cell lesson is missing (`LEARNING.md:35`, "criterion … with no lesson behind it").

## Impacted axes

- **calibration:** the row count and string-presence closure over-credit.
- **operability:** the validator's absent-field fallback, and the forged-verdict acceptance at B.
- **depth:** the recurrence count shows that prose criteria alone have failed three times.

## Limits

- I did not run `routed-defects.py`, `head-rev-lint.py` or the r18 validator; they are peer-owned and not yet landed (`receipt-validate.py` working tree has no `map_sha256`).
- I did not run REA, Ghidra or any carrier.
- My agreement with the r17 "partial disagree" is author-side **[Inference]** and does not count as an outside check.
