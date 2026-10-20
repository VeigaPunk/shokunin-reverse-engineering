BROKEN — "byte-level Ghidra Go map-misread prediction (swiss-misread.py) confirmed on held-out carriers" is not a round-18 capabilities row. Entering it would count C3 twice. Keep it as C3's depth verdict plus the existing SKILL probe row, and enter no capability row this round.

Seat: KaidokuR18.CapabilityCandidate (critic, w2, author-side advisory, not an outside reviewer).
Revisions: REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; baseline `9011581`; C3 freeze `eb6c266`.
Scope: read-only. No REA, no Ghidra, no carrier executed. No tools installed or updated.
Notation: (O) = observed, (I) = inference.
Anchors: lane paths are `git show REV:path`. AXES.md and PROTOCOL.md are fleet files at fleet HEAD `093c27d`, working tree clean (cmd 16).

## Axes
- calibration (owned): ledger matches observed state; overreach caught.
- depth (owned): C3's verdict.
- operability: the tool's registry row.
- ledger integrity: one authority per verdict; stagnation-interval accounting.

## Decision

### R1 (O) The candidate restates C3's verdict; it is not a new capability
- AXES.md:59-61 sets the line: the axes measure what the skill *knows*; the capabilities table records what the shokunin can *do*.
- C3's declared after-state is a knowledge status: "mechanism status unreplayed INFERENCE -> confirmed/refuted/unresolved per the frozen rule" (`.ufo/waves/round-18/claims.json:39`).
- The knowledge entry lands that status: "the verdict is **confirmed**" (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:83-88`).
- The candidate's "…confirmed on held-out carriers" is that same verdict. Its only demonstration is C3's own 15 compares, of which 2 are held-out matches.
- The predictive content is one byte site per carrier (cmd 8). In aether, s1246-swiss-nethttp and kimi, every failing H1 chain is a slot-40 net/http map (MIMEHeader, url.Values, http.Header). All carry `pkg_path: 40` and converge on one read per carrier: [17645861, 111938854], 22386945 and 15606016.
- That single site is the H1 mechanism itself (knowledge:24-33). It is not a broader ability.

### R2 (O) It cannot enter as its own claim
- Round 18 already has three claims, C1–C3. AXES.md:27 allows 1–3 per round.
- A C4 would not be causally separable (AXES.md:31): it verifies if and only if C3's frozen rule says "confirmed" (`predictions/decision-rule.json:7`).
- It would sit on depth, which is C3's axis, or on operability, which is C2's. Either way AXES.md:32-33 applies: "two claims on one axis in one round count as one claim".

### R3 Strongest counter-case: retype C3 as "depth + capability" (AXES.md:40-41; PROTOCOL.md:507-510)
The two lane precedents differ from C3 on every point that matters.

Round 17, C2 (SCORECARD:2364, 2370-2374):
- The row was declared before the run, in both the claim and its before→after: "enter a capability row" and "capability rows 4 … -> +1 only if the capture runs and its receipt validates" (`.ufo/waves/round-17/claims.json:21-22`).
- It was measured: `.ufo/waves/round-17/measure.py:46,120-160`, `C2_scorecard_capability_row` 0→1.
- Its doing, log capture, validates whether or not the predictions match. Receipt-validate checks digests and log binding, not the compare result (SKILL.md:541).

Round 14, C2 (SCORECARD:2190, 2203-2207):
- The declared observable was the instrument itself: "quote-location fidelity gate …" (`.ufo/waves/round-14/claims.json:20-24`).
- That gate is general-purpose.

Round 18, C3 has none of this (O):
- Its declared axis is depth, with no capability clause (claims.json:24-27, 39). The only "capability" in claims.json is line 7: the nudge is inactive because round 17 entered a row.
- The round-17 "Planned" note names depth (SCORECARD:2422-2426).
- `round-18/measure.py` has 0 capability checks (cmd 3).
- At REV the round-18 section has no capability row (SCORECARD:2428-2440).
- The wave-2 scorecard draft lists "C1 calibration, C2 operability, C3 depth" (`.ufo/waves/round-18/gen-wave2.py:126`; working tree, untracked at REV).

Retyping C3 now would mean a capability credit added after seeing the outcome. Its only evidence would be C3's one demonstration.

### R4 (I, from O anchors) Duplicate authority and stagnation accounting
- A row would be a second ledger entry for C3's verdict.
- Non-author sampling is still pending (`corpus/lessons/round-18.md:45-47`). If it overturns C3, two ledgers need append-only retractions.
- This is the drift class (R17-PINMAP, R17-VALIDATE16) that this round spent C1 repairing.
- A row also resets the capability stagnation interval, as SCORECARD:2391-2392 records for round 17. That reset would come from evidence C3 already credits.

## Counterexample: blocks even a reworded "byte-level prediction" row
- The tool documents its `walk` channel as "the reader Ghidra 12.1.4 actually runs … The first read failure aborts the walk exactly as `GolangSymbolAnalyzer` aborts" (`.ufo/waves/round-18/tools/swiss-misread.py:17-21`).
- (O) On the only real held-out carrier, real-kimi-webbridge, the frozen walk predicts `unmapped at 0x8` under **both** H1 and H0 (`predictions/swiss-misread/real-kimi-webbridge.json:3108-3136`).
- Ghidra instead aborted with `Invalid index: 15606016` (`runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:73,206`).
- The walk is also wrong under both hypotheses on calib-notesmd-cli, and under H0 on calib-aether. It is right only on aether H1 and on the 12 synthetic carriers (cmd 7).
- Only the per-map channel matched. `swiss-misread.py:1461-1464` deliberately keeps the walk out of `predicted_failure`.
- The first-failure model was never shown to work on any real carrier outside calibration. Every positive also converges on one read (R1), so ordering between chains with different reads was never tested.
- (O) This is not disclosed. Knowledge:117-119 names walk false positives only for "(notesmd-cli)". Lessons, SKILL.md and LOG say nothing about the kimi or aether-H0 walk failures (cmd 9).
- This disclosure gap is a fixable calibration defect.

Route wording:
- The round's own gate rejects "aether's failure is on the map path" as stated (lessons:22).
- The kimi stack reaches `GoName.getPkgPath` through `GoStructType`/`GoInterfaceType.additionalMarkup` frames (ghidra.log:100-176).
- A row named "map-misread … confirmed" would restate wording the round rejected.
- (I) The frames cannot show whether that route enters a misread map type: `GoMapType` appears 0 times in the kimi, s1246-swiss-nethttp and aether logs (cmd 17).

## What holds (O): supports C3, not a row
- The predictions, `swiss-misread.py` and `gen-predictions.py` are unchanged from freeze to REV (cmd 5).
- No `.log` at the freeze commit names kimi-webbridge (cmd 13).
- All 15 retained runs show `compare.exit` 0 and `carrier-run.exit` 0 (cmd 6).
- All 3 D-label receipts validate with `--require-mid-maps` (cmd 11).
- Rerunning the tool reproduces the frozen JSON exactly, 3/3, including the kimi walk false positive (cmd 12). The frozen files only lack a trailing newline, which cmd 12 accounts for.
- Carrier sha256s match the pins (cmd 10).
- Both held-out carriers hit their exact predicted index.
- s1250-swiss-nethttp is a correct non-trivial silent case: slot-40 maps, but the name at types+40 has no pkgPath.

## Impacted axes
| Axis | Effect |
|---|---|
| calibration | Harmed if the row enters: a post-outcome double credit, plus the undisclosed walk false positive |
| depth | Unchanged; C3 stands on its own evidence |
| operability | Unchanged; the probe is already registered (SKILL.md:590), and the decision table already says to run it (SKILL.md:559) |
| ledger integrity | Harmed if the row enters: a second authority for one verdict |

## Smallest safe correction
1. Enter no capability row for round 18. The round report should say: "capability: none entered; swiss-misread is C3's depth instrument (SKILL.md:559, 590)."
2. Append a named correction to knowledge:117-119 giving the walk outcome on all three real carriers:
   - aether: H0 `unmapped at 0x8`;
   - notesmd-cli: H1 and H0 `unmapped at 0x8`;
   - kimi: H1 and H0 `unmapped at 0x8`, against the observed `Invalid index: 15606016`.
3. If the repertoire credit is wanted, claim it in a later round as a declared capability acquisition with its own before→after:
   - predictions frozen on unseen real Swiss carriers, including one with two or more distinct failing reads;
   - the walk channel either fixed or excluded from the row's wording;
   - a measured row check, as in `round-17/measure.py:46,120-160`.

## Commands
All run in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` with `REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. All read-only.

1. `git show $REV:SCORECARD.md | awk 'NR>=2428 {printf "%d: %s\n", NR, $0}'; echo "exit=${PIPESTATUS[0]}"`
   - exit 0; section 2428-2440, no capability row.
   - Also `| sed -n '615,650p'` → exit 0.
   - Also `| sed -n '2391,2392p;2422,2426p'` → exit 0.
2. `git show $REV:.ufo/waves/round-18/claims.json | grep -n '"id": "C3"\|"axis": "depth"\|"C3":\|capabilit\|"falsifiable_before_after": "carriers'`
   - exit 0; lines 7, 24, 25, 27, 39.
   - Same against round-17 claims.json (`'"id": "C2"\|"axis": "depth"\|capability row\|capability rows'`) → exit 0; lines 17, 18, 21, 22.
   - Round-14 (`grep -n "quote-location\|\"C2\"\|\"axis\": \"calibration\""`) → exit 0; lines 20, 21, 24.
3. `git show $REV:.ufo/waves/round-18/measure.py | grep -c -i capabil; echo "grep_exit=${PIPESTATUS[1]}"`
   - prints 0; grep_exit 1.
4. `git show $REV:.ufo/waves/round-17/measure.py | grep -n -i "capabil"`
   - exit 0; lines 46, 120-160.
5. `git diff --stat eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 $REV -- .ufo/waves/round-18/predictions/ .ufo/waves/round-18/tools/swiss-misread.py .ufo/waves/round-18/gen-predictions.py; echo "diffexit=$?"`
   - empty output; diffexit 0.
6. `for d in $(git ls-tree --name-only $REV .ufo/waves/round-18/runs/ | grep -v run-log); do printf "%s compare.exit=%s carrier-run.exit=%s\n" "$(basename $d)" "$(git show $REV:$d/compare.exit | tr -d '\n')" "$(git show $REV:$d/carrier-run.exit | tr -d '\n')"; done`
   - exit 0; 15 rows, all 0/0.
7. Map channel vs walk channel, all 15 frozen outputs (exit 0):
   ```
   for f in $(git ls-tree --name-only $REV .ufo/waves/round-18/predictions/swiss-misread/); do L=$(basename $f .json); git show $REV:$f | python3 -I -B -c 'import json,sys
   L=sys.argv[1]; d=json.load(sys.stdin); w=d.get("walk",{})
   def wk(h):
       x=w.get(h) or {}
       return "%s:%s@%s" % (x.get("kind"), x.get("index"), x.get("eof")) if w.get("failed",{}).get(h) else "ok"
   print("%-24s map: h1=%-13s %s h0=%-6s | walk: h1=%s h0=%s | misread_maps=%s" % (L, d.get("predicted_failure_kind_h1"), d.get("predicted_invalid_index_reads_h1") or d.get("predicted_eof_reads_h1"), d.get("predicted_failure_kind_h0"), wk("h1"), wk("h0"), d.get("misread_map_types")))' $L; done
   ```
   Key rows:
   - `real-kimi-webbridge map: h1=invalid_index [15606016] h0=none | walk: h1=unmapped:8@None h0=unmapped:8@None`
   - `calib-notesmd-cli … walk: h1=unmapped:8 h0=unmapped:8`
   - `calib-aether … walk: h1=past_eof … h0=unmapped:8`
   - the 12 synthetic rows match the map channel.
8. Per-map H1 outcome for each uncommon map in real-kimi-webbridge, s1246-swiss-nethttp, calib-aether and s1250-swiss-nethttp (exit 0): one python3 loop over `per_type[]` where `uncommon` is true, printing `name`, `slot_size`, `h1.outcome`, `index`, `eof`, `ghidra_uncommon`.
   - Every failing entry is slot 40 with `pkg_path: 40`.
   - Each carrier has a single read value.
9. `for f in corpus/knowledge/2026-10-20-r18-swiss-map-replay.md corpus/lessons/round-18.md SKILL.md LOG.md; do echo "== $f"; git show $REV:$f | grep -n -i "walk\|unmapped\|false positive"; done`
   - exit 0.
   - Only knowledge:117 concerns the tool. The SKILL and LOG hits are unrelated (binwalk, planning walks). Lessons has no hits.
10. `sha256sum /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nethttp /usr/bin/aether`
    - exit 0; all four equal the pinned values in `carriers/SHA256SUMS` and `predictions/carriers.tsv`.
11. `for L in real-kimi-webbridge s1246-swiss-nethttp calib-aether; do python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/$L/receipt.json >/dev/null 2>&1; echo "$L exit=$?"; done`
    - exit 0 ×3.
    - The working tree under runs, predictions and tools has an empty `git status --porcelain`.
12. Rerun vs frozen (no files written):
    ```
    G=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
    diff <(timeout 600 python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier "$P" --golang-root "$G"; echo "tool_exit=$?") <(git show $REV:.ufo/waves/round-18/predictions/swiss-misread/$N.json; echo; echo "tool_exit=0")
    ```
    - diff exit 0 for real-kimi-webbridge, s1246-swiss-nethttp and s1250-swiss-nethttp.
    - `git show $REV:…/real-kimi-webbridge.json | tail -c 2 | od -c` → `\n }`, i.e. no trailing newline, hence the extra `echo` on the frozen side.
13. `git grep -l "kimi-webbridge" eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 -- '*.log'` → exit 1.
    - Same grep at `9011581` over `.` → exit 0; the only hit is `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/sidecar-inventory-pre.txt`.
14. `git show $REV:.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log | awk 'NR>=68 && NR<=215 {printf "%d: %s\n", NR, substr($0,1,300)}'` → exit 0.
    - Same for `s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log`, lines 400-475 → exit 0.
15. Walk paths: a python3 print of `walk.h1` and `walk.h0` (kind, index, path) for calib-aether, s1246-swiss-nethttp, real-kimi-webbridge and calib-notesmd-cli → exit 0.
    - kimi: the H1 and H0 paths are identical (12 steps) and end in `unmapped at 0x8`.
16. `git -C /home/vgpnk/Projects/shokunin diff --quiet HEAD -- AXES.md PROTOCOL.md` → exit 0.
    - `git cat-file -e $REV:AXES.md` → exit 128 (no lane copy).
    - `git cat-file -e $REV:.ufo/waves/round-18/gen-wave2.py` → exit 128 (file is `??` in the working tree).
17. `for p in real-kimi-webbridge/logs/rea-ghidra-ZSUHpG s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l calib-aether/logs/rea-ghidra-HtDopV; do git show $REV:.ufo/waves/round-18/runs/$p/ghidra.log | grep -c "GoMapType"; done`
    - prints 0 three times; the last grep exits 1.

## Not examined
- Whether the H0 alternative is a strawman, or whether the emulator is independent of the logs: other seats cover the mechanism verdict itself.
- Whether the round-14 capability row was itself a double count: it is cited here only as the strongest precedent.
- Other capability candidates from this round, such as the reproducible synthetic-carrier build recipe.
