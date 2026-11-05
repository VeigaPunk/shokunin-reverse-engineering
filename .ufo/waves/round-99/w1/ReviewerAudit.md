# ReviewerAudit — R99-C1 surgical review (counter at F, landing A)

Seat: ReviewerAudit, lane kaidoku round 99, 2026-11-05. Scope: `tools/round-99/self-assessment-audit.py`
at F `8fb5ac4fa` and `git diff 01c4b79cc..64cc3e10c` (landing A). B0 `de098f51c`, A `64cc3e10c`,
Bk `c19d57cd2`. Scratch `$S=/fast/scratch/hyaku/kaidoku-r99/ReviewerAudit` (shared clone, toplevel
verified, trap-equivalent `rm -rf` after archiving; receipts archived to
`.ufo/waves/round-99/w1/ReviewerAudit/`). No tools installed (nothing needed; pacman untouched).

## Every command cited (all run; exit codes recorded)

| # | command (short form) | exit | result |
|---|---|---|---|
| R1 | `python3 -I -B tools/round-99/self-assessment-audit.py --root . --rev de098f51c… --json-out $S/receipts/audit-B0.json` | 1 | `mismatches 17; head-score mismatch; head-fraction mismatch; map-rows 176 of 182; registry 0 of 9` |
| R2 | same, `--rev 64cc3e10c…` → audit-A.json | 0 | `mismatches 0; head-score ok; head-fraction ok; map-rows 182 of 182; registry 14 of 14` |
| R3 | same, `--rev c19d57cd2…` → audit-Bk.json | 0 | `mismatches 0; …; map-rows 183 of 183; registry 14 of 14` |
| R4 | `printf '\n# working-tree scratch edit\n' >> tools/round-97/kill-rule-v3.py` then R2 form → audit-A-dirtywt.json (file restored after) | 0 | label unchanged (`mismatches 0; registry 14 of 14`); receipt `tools` dict byte-identical to R2's |
| R5 | `python3 probe_a3.py` (archived copy + output) | 0 | CASE1 filler row mismatches=0; CASE2 TBD-pad 0; CASE3 stem-in-4th-cell 0; CASE4 corpus/-prefixed 3 |
| R6 | python compare of R2 vs R4 receipts + sha of counter file | 0 | `tools` identical; `counter_sha256` == working-tree counter bytes |
| R7 | `git ls-tree --name-only <rev> -- .ufo/waves/round-99/l1/scores/` at A, Bk, HEAD; `ls-tree -r HEAD -- .ufo/waves/round-99 \| grep c1-at` | 0/1 | scores/ holds only `c2-at-01c4b79….json` at all three; zero `c1-at` paths under round-99 anywhere |
| R8 | `git show A:.ufo/waves/round-99/pre/c1-selftest.txt` | 0 | `SELFTEST cases=9 failures=0`, `rc=0` |
| R9 | diff reads: A→Bk SCORECARD, L→A (stat + full minus receipt), entries at A | 0 | see Findings/answers |

## Findings (by severity)

### M1 — SCORECARD coverage head cites C1 receipts that were never committed (A and Bk)
`SCORECARD.md:23` at A and at Bk: "…at the round-99 record (`tools/round-66/coverage-selfcheck.py
--selfcheck`, stem recipe, and the stricter table-row atom A3 …; receipts
`.ufo/waves/round-99/l1/scores/c1-at-*.json`)". No `c1-at-*.json` exists at A, at Bk, or at lane
HEAD: `l1/scores/` contains only `c2-at-01c4b79cc….json` (R7). The fractions themselves are true
(R2/R3: claimed == observed, exit 0), so the head is honest — but its evidence pointer names files
that do not exist, the same class QUALITY 198 polices (a pointer must name what exists). Fix:
commit the two C1 landing receipts (my R2/R3 runs re-derive them) or repoint the row to the
committed pre/ controls plus the re-derivation command.

### L1 — A3 accepts rows a reader would call unmapped (filler-class; docstring disclosed, selftest gap)
`map_rows` (counter lines 71-93) maps a stem when its row keeps ≥20 chars after removing the
stem/pipes/backticks/commas/whitespace. Probes (R5, archived): a row whose only other content is
`xxxxxxxxxxxxxxxxxxxx` or `TBD TBD …` passes (CASE1/2), and a stem backticked in the 4th cell of an
otherwise unrelated row passes (CASE3). The docstring states the ≥20-char rule honestly, so this is
an acceptance-criterion gap, not a doc/code mismatch; frozen selftest covers F1 prose and F2
stem-only but no filler forgery. Recommendation (future round, counter is frozen): an F9
filler-row case, or require the row's other cells to carry the entry's title/alphabetic content.

### L2 — counter and its round-66 dependency load from the working tree, and the receipt does not pin r66
`load_cs` (54-62) imports `tools/round-66/coverage-selfcheck.py` from `HERE` (working tree);
`counter_sha256` (223-224) hashes the working-tree counter. Only A4's tool shas (`read_rev`
151-163, `git show rev:path` at 162) are bound to `--rev` bytes. A dirty working tree could in
principle change A1/A2's rule source invisibly: the receipt pins the counter's sha but not r66's.
Mitigated in practice — the frozen workflow runs from a detached clone at the audited rev, and my
R4 dirty-tree attack left the label and the receipt's `tools` dict unchanged — but an r66 edit
would be unobservable in the receipt. Recommendation: also record r66's sha256 in the receipt.

## Answers to the seat questions

1. **Atoms vs docstrings — yes, each computes what its docstring says.** A1 (137): parsed head
   score vs `round(10*mapped/files,2)`; A2 (138): parsed `<m>/<n> knowledge files` vs recipe pair;
   A3 (71-93): table row + backticked stem + 20-char residual, exactly as documented (F2 shows the
   stem-only refusal); A4 (97-122): kind word ` — ` (KIND_RE 50, applied 113), exit map `0=` and
   `1=`/`2=` with `(?<![\w.])` guard (115), cell-4 ≥10 chars (117-118), full sha via `\b[0-9a-f]{64}\b`
   (51, 119) — all four docstring clauses present. Receipt `stem_recipe_missing` is emitted (149).
2. **A3 filler acceptance — yes** (finding L1; probe CASE1-3).
3. **A4 binds sha to `--rev` bytes, not the working tree — yes.** `ls-tree --name-only rev -- d/`
   (160) is non-recursive so `controls/`/`forgeries/` subdirs are excluded; sha over
   `git show rev:p` binary (162). Attack-verified: R4 corrupts the working-tree bytes of a
   registered tool; label and receipt `tools` dict unchanged.
4. **Head atoms reused correctly — yes.** Same functions (`map_section` r66:90, `recipe_stem`
   r66:159, `coverage_row` r66:219, `parse_row` r66:229), same composition and rounding as r66's
   own selfcheck; A3 is strictly stronger than the stem recipe (every A3 hit carries a backticked
   stem token in the section, which is exactly what `recipe_stem.mapped` accepts; CASE4 shows both
   reject `corpus/knowledge/…`-prefixed backticks consistently).
5. **Base 17 re-derivable — yes.** R1 reproduces the frozen base control exactly (label and the
   pre-control's missing lists: 6 named stems + 9 named tools); arithmetic 1 (A1) + 1 (A2) + 6
   (A3) + 9 (A4) = 17; the forgery control's 15 = 0+0+6+9 is equally consistent.
6. **SCORECARD head at A/Bk — fraction true.** Receipts: A claimed [182,182]/10.0 == observed;
   Bk [183,183]/10.0 == observed. The parse survives the row's historical strings ("176/182 = 9.67"
   lacks the `knowledge files` suffix; "168/168 knowledge files" appears after the first match, and
   `re.search` takes the first; last `→` gives 10.0). Correct but fragile pattern. The receipts
   pointer dangles (M1).
7. **Six README rows (README.md:134-139 at A) — accurate against their entries.** r134
   citation-semantics: block 31 row 3 → QUALITY 169 miscite, keyword checker, no class move ✓. r135
   fresh-pack-oracle: separates derivation from lookup, S318/S317/S271, "R93-C1 … NOT verified"
   matches the entry's "the R93-C1 verdict in the lesson is not verified" ✓. r136 receipt-path-json:
   S319 TypeError-on-bytes, v3 crash on honest repair ✓ — "receipt-writer family already held" is
   the one phrase I could not pin to a written source (soft assertion, not contradicted). r137
   receipt-world-binding: S320 O_NOFOLLOW, R95-C1 verified with named limits ✓. r138
   kill-rule-coverage: gates incl. main()/fsync-count/probe receipt, five round-95 survivors,
   S321 ✓. r139 receipt-byte-binding: "not admitted" matches the kill-rule-v3 registry row's "NOT
   admitted at closure"; v7 nine-key allow-list harm repaired by v8 ✓; the cited lesson
   `corpus/lessons/round-97-verifier-spotcheck.md` exists at A (R7 batch). QUALITY 201's
   shown-able-to-fail numbers match my R1 and the pre-control. SKILL's 14 registry rows are
   sha-verified by A4 itself (registry 14 of 14); the audit tool's own row sha `e732465b…` equals
   my receipt's tool sha (R6).

## Residual risk / not covered

- The SCORECARD row also credits `tools/round-66/coverage-selfcheck.py --selfcheck`; I verified the
  stem-recipe half through the audit receipts (observed_fraction) and read r66's code, but did not
  re-run `--selfcheck`/`--equiv` at A.
- C2 (battery, repair, forgeries) is outside this seat's item; untouched.
- L1/L2 do not affect the frozen predicate at any measured revision: M=0 held at A and Bk under
  attack; M1 is a landed-documentation defect, not a counter defect.

Receipts: `audit-B0.json`, `audit-A.json`, `audit-A-dirtywt.json`, `audit-Bk.json`, `probe_a3.py`,
`probe-a3-output.txt` in `.ufo/waves/round-99/w1/ReviewerAudit/`.
