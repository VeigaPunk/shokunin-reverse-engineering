# A5 — every quantified phrase in `plans/round-41-claims.md` and whether a counting clause closes it

Read at lane base `49096c7e6f226af0c750c4b003be58883cb6049f`. "Enumerator" = the clause name in the
round-40 counter family the round-41 port derives from (`tools/round-40/c1-counter.py` CLAUSES/BINDINGS,
`tools/round-40/c2-counter.py` bindings, `tools/round-40/c1-extra.py` bindings); a round-41 port keeps
the names unless it says otherwise. Nothing here was executed against a carrier.

Legend: **CLOSED** = a frozen clause decides it over a set that exists at the freeze; **OPEN** = no
clause decides it; **HOLE** = a clause exists but its quantifier is weaker than the sentence.

## R41-C1 (claims lines 31–62)

| # | phrase (line) | enumerator | verdict |
|---|---|---|---|
| 1 | "for each of the four frozen carriers V3, V4, L3, L4" (31–32) | `carriers_spec` requires exactly `target` entries with ids equal to the frozen set | CLOSED |
| 2 | "none of which any REA or unblob run touched before the freeze" (32) | — | OPEN (negative provenance; no committed byte records an absence of runs, and the `squashfs` oracle arm is itself an extractor run, so the sentence is also narrower than the reservation it restates) |
| 3 | "names the `squashfs_v4_be` handler" (34) | `handler_ok` | CLOSED |
| 4 | "with no failed chunk" (34) | `chunks_ok` | CLOSED |
| 5 | "first added in a commit descending from the freeze" (33–34) | `receipt_fresh` (+ `first_add`) | HOLE — satisfied by a post-add overwrite (A1): the add commit and the overwritten blob are never compared |
| 6 | "publishes every regular file of the frozen independent oracle at the exact path … with the same sha256" (34–36) | `oracle_hits_ok` (`hits == oracle_files`) | HOLE — one direction only; extra published regular files are not refused. "independent" is CLOSED for V3/V4 (reader vs `squashfs-v4be` cross-check) and OPEN for L3/L4 (the oracle is the lane's own reader, cross-checked by the tool under measurement) |
| 7 | "publishes no non-regular entry at its exact path" (36) | `nonregular_unpublished_ok` (exact after R40-CL1 fix) | CLOSED |
| 8 | "carries gaps only as the frozen gap rule allows" (36–37) | `gaps_ok` + `gap_rule_ok` over `gap-rule.json` (`allowed`/`required`/`structural`) | CLOSED |
| 9 | "has a subject digest equal to the carrier pin" (37) | `subject_pin_ok` | CLOSED |
| 10 | "and recomputes to its evidence id" (37–38) | `evidence_id_ok` | CLOSED |
| 11 | "the carrier bytes hash to the pin" (38) | `carrier_pin_ok` | CLOSED |
| 12 | "carry the AVM marker with little-endian block lengths" (38–39) | `layout_ok` (`layout_probe`) | CLOSED |
| 13 | "a counter-time REA rerun of the same bytes has the same `plus-extractor` projection" (39–40) | `projection_ok` at the profile frozen in `carriers.json` | CLOSED |
| 14 | "for vendor carriers the fetch chain checks image sha256 → member sha256 (R40-CL6) → carrier sha256" (40–41) | — | OPEN (the counter reads the `--carrier-cache` file and re-hashes it; `fetch-vendor.py` runs outside every counting command and `carriers_spec` does not even require `member_sha256`) |
| 15 | "PROVINCE.md holds a `## Round-41 additions to Core` row naming the AVM layout and citing `<entry>`" (41–42) | `province_core_row` | CLOSED |
| 16 | "which cites a SOURCES row absent at the base whose used-by lists it" (42–43) | `c1-extra.sourced_new` (needs `--base`) | CLOSED only if `--base` is in the scoring command line |
| 17 | "a `Round-41 frontier note` names that heading and the entry stem and says what it supersedes" (43–44) | `frontier_note` / `c1-extra.frontier_content` | HOLE — "names" is a word test; "says what it supersedes" is reduced to the token `supersede` |
| 18 | "corpus/README.md maps the entry stem" (44) | `coverage_map_row` | CLOSED |
| 19 | "`carriers_matched == 4`" (60) | counter target | CLOSED |
| 20 | "every binding true" (60) | `all(BINDINGS)` | CLOSED by code, but the ten binding names are not in the claims file, so the *claim* is not self-contained (it is, if the frozen counter is read as part of the claim) |
| 21 | "supplementary gate met" (60) | `c1-extra.py` exit 0 | CLOSED as a second command |
| 22 | "reserved — nobody runs REA/unblob on them or on their source images before the freeze" (46) | — | OPEN (same as #2) |
| 23 | "nested-name collisions in both directions" (52–53) | — | OPEN (a property of the fixture; only the counter's own selftest exercises it, so a mis-built L3/L4 carrier is not refused) |

## R41-C2 (claims lines 72–101)

| # | phrase (line) | enumerator | verdict |
|---|---|---|---|
| 1 | "gives every held-out envelope the (label, action) pair" (90–91) | — | OPEN and unsatisfiable: the precedence block derives an action for `unclassified` only (A2), so a text-derived evaluator cannot produce 11 of the 12 pairs |
| 2 | "the frozen independent evaluator (… never reading the table, the interpreter or the generator's class map)" (91–93) | — | OPEN ("never reading" is a process promise; no clause can observe it unless the evaluator is run where those three paths do not exist) |
| 3 | "for all held-out envelopes (… two replicates each)" (93–94) | `classes_two_each`, `n_equals_twice_classes` in a port | HOLE — no count is stated in the claim, and "every envelope" is vacuously true at N = 0; the draft names the classes, which makes the set enumerable to a fitted table |
| 4 | "seed = the freeze hash" (95) | `seed_matches_freeze` | CLOSED |
| 5 | "carriers regenerate byte-identically" (95) | `carriers_regenerated` | CLOSED |
| 6 | "the generator's own class expectation agrees with the evaluator on every envelope" (95–96) | — | OPEN (no binding; and it is the one clause that would catch an evaluator whose precedence reading differs from the generator's class map) |
| 7 | "the v3 table bytes equal the freeze bytes" (96–97) | `v2_table_identical` analogue | CLOSED |
| 8 | "the frozen v3 interpreter on the base `SKILL.md` exits 2 (no v3 marker), the C2 counter at the freeze exits 2" (69–70) | interpreter + counter | CLOSED, but instrument-specific: the *v2* interpreter exits 0 at the base (A3 3.2) |
| 9 | kill rule "a control at target on the development envelopes … stops C2. Controls: base SKILL; catch-all; the v2 table transcribed into v3 grammar; actions rotated; no contains-operator; a `*` default row" (99–101) | control receipts | HOLE — no minimal-cell control and no identity control (evaluator replaced by the generator's class map); an 18-row exact-set lookup ties the target without the precedence rule |
| 10 | (no target sentence) | — | OPEN — C2 has no stated count, exit code or binding list |

## Freeze-integrity rule (line 15)

| # | phrase | enumerator | verdict |
|---|---|---|---|
| 1 | "no commit in `FREEZE..REV` touches **a frozen path of that claim**" | `frozen_changes` / `frozen_drift` | OPEN — the set is never enumerated; round-40's C1 set is a code constant and its C2 set omits the writer (A4 4.4), so "a frozen path" is currently a code fact, not a claim fact |

## What this table implies for the freeze

Every OPEN/HOLE row is one of: a sentence the closure cannot re-derive (2, 14, 22 C1; 2 C2), a
quantifier weaker than its clause (5, 6, 17 C1; 3 C2), a property no command sees (23 C1), or a
target that cannot be met or cannot be distinguished (1, 9, 10 C2). None requires new data to fix.
