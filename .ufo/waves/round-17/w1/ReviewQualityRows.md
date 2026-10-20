# Review — QUALITY rows 1–18 and proposed row 19

Seat: `KaidokuR17.ReviewQualityRows-3` (read-only). Read: `corpus/QUALITY.md` (all 41 lines), `corpus/lessons/round-15-verifier-spotcheck.md`, `round-16-verifier-spotcheck.md`, `round-16.md`, `round-13.md`, `round-13-verifier-spotcheck.md`, `round-14.md`, `round-15.md`, r9-02 knowledge entry, r2 schema entry, `.ufo/waves/round-16/verification.json` (397–421), `round-17/claims.json`, `round-17/contract.md`, `round-16/measure.py`, `round-17/pilot/README.txt`. No `lsp` device is mounted in this seat; structural checks are direct reads plus a byte-level table parse (no LSP-semantic claim).

## 1. Proposed exact row 19

Insert as the last admission row: after `corpus/QUALITY.md:28` (row 18), before the blank line at `:29`; the Signals table starts at `:30`/`:32`. Copy verbatim, one physical line:

```markdown
| 19 | Temporal-stability claims ("unchanged during", "stable throughout") are admitted only with records at two named instants: the producing tool retains pre- and post-snapshot maps (per-path SHA-256 and size) with each snapshot's UTC timestamp, their comparison verdict, and a retained red run in which a mutated path is named and the comparison fails. Two end-state maps establish equality at those instants, not continuity between them; "throughout" needs a pin at each step boundary, otherwise state the weaker fact — "map matches committed source-revision blobs; temporal stability not evidenced". A lone hash map or a `pins_unchanged_during_run: true`-style boolean is not a measurement; correct an overstatement only by a named append-only correction that names the defect and each corrected site, never by rewriting filed bytes. | `corpus/lessons/round-16-verifier-spotcheck.md:181-184` (R16-PROVENANCE; R16-INVOCATION is #18's per :184); `.ufo/waves/round-16/verification.json:419` | sharpens 18; #18 invocation rule unchanged |
```

Shape check (Python, this text): 4 cells, 5 unescaped pipes, 6 backticks (balanced), 1,039 chars — between row 16 (946) and row 17 (1,222). Prefix `| 19 |` matches the r16 measure precedent `ROW18 = re.compile(r"^\|\s*18\s*\|")` (`round-16/measure.py:30`), so an r17 `ROW19` analog will find it.

## 2. Grounding — clause → lesson:181–184

- Two-instant maps, UTC timestamps, comparison verdict ← `round-16-verifier-spotcheck.md:183`: verification.json "retains one 20-entry hash map and `pins_unchanged_during_run:true`, but no before/after maps, per-command hashes, or before/after timestamps". Artifact: `.ufo/waves/round-16/verification.json:397` (map) and `:419` (boolean).
- Weaker sentence reproduced verbatim ← same line: say "map matches committed source-revision blobs; temporal stability not evidenced".
- "equality at those instants, not continuity" + per-step pins for "throughout" ← same line: the comparison "proves only that recorded hashes match committed S/A bytes 20/20, not that files were stable throughout the run", with per-command hashes named as missing. Corroborated by the r17 contract's mandated pins.py disclaimer ("proves only 'same bytes at two instants', never 'unchanged throughout'", `contract.md`, W/tools/pins.py bullet).
- Named append-only correction, never rewriting filed bytes ← same line: "Append named corrections… Never rewrite filed report/LOG bytes".
- Red run (mutation named, comparison fails) ← QUALITY #2 falsifiability applied to the instrument; matches C1's "pins.py selftest red case exits 1 on a mutated pin" (`claims.json:13`) and the contract selftest red case.
- R16-INVOCATION half ← `round-16-verifier-spotcheck.md:184`; deliberately referenced only in the `why`/`supersedes` cells (see §3), not restated as a norm.

Inference (labeled): I read "per-command hashes" at :183 as the basis for the per-step-pin clause; the wording "pin at each step boundary" is mine, not a quotation.

## 3. Non-duplication vs #18 — exact overlap check

Row 18 (`QUALITY.md:28`) contains two sentences near the new ground:

1. "future recheck guidance either matches the exercised isolation flags and paths or explicitly names an unexercised variant" — this *is* R16-INVOCATION's remedy (`:184`: "Align future runnable guidance with an actual receipt, or explicitly distinguish intended vs exercised invocation, with a lesson/QUALITY18 link"). The proposed row 19 contains no invocation-matching sentence; the cross-reference sits in the `why` cell ("R16-INVOCATION is #18's per :184") and the `supersedes` cell ("#18 invocation rule unchanged").
2. "Structural/no-harm tallies retain the producer and immutable inputs, not only unexplained booleans" — producer + inputs, not time. R16 satisfied the letter of this: `verification.json:397–419` has the producer/fixture map and the boolean, yet could not support "unchanged during". Row 19 adds the missing temporal record and its strength limit; #18 stays in force.

No other row covers two-instant records: #7 is examined-coverage, #9 runtime provenance, #10 carrier-run scope, #11 parsed-vs-excluded, #12 pinned fixture bytes (observation from rows 11–28).

The `supersedes` cell therefore reads "sharpens 18; #18 invocation rule unchanged", matching existing style (#10 "sharpens 8"; #18 "sharpens 1, 6; no change to 17") and `QUALITY.md:6–8` ("A criterion is replaced by a new row naming the row it supersedes, never rewritten"). A full supersession of #18 is rejected: it would have to restate the invocation sentence (the duplication the assignment forbids) or silently retire a still-valid rule.

## 4. Findings on rows 1–18

**F1 (low; concrete; do NOT fix this round).** `corpus/QUALITY.md:23` (row 13) has an unescaped `|` inside the code span `` `grep -o … | wc -l` ``: 6 unescaped pipes versus 5 for every other admission row (rows at `:11–:22`, `:24–:28`). Inference from the GFM table rule (pipes split cells even inside code spans): row 13 renders 5 cells and its `supersedes` cell empties. Not fixed because `contract.md` (`controls.py`) makes "QUALITY rows 1–18 unchanged" a control; editing row 13 would falsify it. Route as next-round debt with the fix `` `grep -o … \| wc -l` ``. No current tool parses QUALITY rows by pipe: `round-16/measure.py:30,102` matches whole lines by regex, and `.ufo/waves/round-17/tools/` does not exist yet (observation: directory listing).

**F2 (info; precision only).** Row 18 cites "four routed duties in `corpus/lessons/round-15-verifier-spotcheck.md:181-188`"; the four duties are at `:185–188`, `:181` is the routing sentence. The range resolves and contains them (file has 192 lines), so no content loss; noted only because row 19 uses exact anchors instead of replicating the loose range.

**F3 (no finding).** Every path citation in rows 1–18 resolves and its range lands on the claimed content: r9-02 candidate heading at `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146` (file 391 lines; cited 146–169); r2 schema errata bullet at `corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:244` (heading `:242`, file 250 lines; cited 244–250); round-13 Mistakes #3/#4 at `corpus/lessons/round-13.md:73–74`; round-13/14/15/16 lessons, both spot-check lessons and `.ufo/waves/round-16/documentation-red.json` exist. Supersession chain is intact (14←15, 16←17; 10 sharpens 8; 18 sharpens 1,6) and numbering is contiguous 1–18 with no unnamed replacement.

**F4 (no finding).** No existing row 19 or temporal-record criterion anywhere in `corpus/`: the only "row 19" string is unrelated (`corpus/knowledge/2026-10-13-r3-mcp-session.md:99`). `claims.json:13` expects exactly one new row ("QUALITY row 19 presence 0 -> 1"); no artifact pre-empts it.

## 5. Residual risk and verification gaps

- The per-step-pin clause is stricter than any current lane tool; that is deliberate — with only run-level pre/post the row forces "temporal stability not evidenced", so it cannot yield a false green.
- C1's "shown able to fail" is discharged only when pins.py's red selftest is actually executed and its stdout/exit retained; the row states the requirement, not the receipt.
- No `lsp` device in this seat, so no diagnostics-backed proof of table semantics; I used a byte-level pipe count plus direct anchor reads. No REA `analyze`/`search`/`decompile`, no Ghidra, no lane tool executed (L1 runs carriers once). Read-only compliance: only this report was written.
- Keep row 19 on one physical line starting `| 19 |`; if the r17 measure tool anchors on a different prefix, adjust the tool, not the row's table shape.
- Tool installs/upgrades this run: none.
