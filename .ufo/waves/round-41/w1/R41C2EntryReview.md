# R41C2EntryReview — R40-CL5 defect list re-verified at 49096c7e before table v3 is drafted

VERDICT: **CONFIRMED** — every R40-CL5 finding re-locates at base `49096c7e6f226af0c750c4b003be58883cb6049f` exactly as filed: **M1–M3 and L1–L7 are all still present in the frozen bytes; none is already fixed.** Of the AxisFit findings, F2 is already repaired by the R41-C2 design, F1 is half-repaired (SCORECARD row + entry Scoring paragraph), and F3/F4/F7 remain open text work. Two description details are wrong (the "40+ of 45 selftest cases" count; F1's "not stated anywhere" framing), and the draft's prose-repairs list (`plans/round-41-claims.md`, R41-C2) omits seven items v3's text must carry — including one no review filed: the frozen v2 rows still prescribe the **suffix matching that R40-CL1 refrozen the C1 counter away from**.

## Method (every byte read at the base)

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` → `49096c7e6f226af0c750c4b003be58883cb6049f` = the base; `git status --porcelain` → only untracked `.ufo/waves/round-41/` and `plans/round-41-claims.md`. Working-tree line numbers of tracked files are therefore at-commit line numbers.
- At-commit copies via `git show 49096c7e…:<path>` into scratch; sha256: `SKILL.md` `926dac301cf0281e2b35b6736b6f6ee869a0a1b415fd5207f9de3959c4ca0054`, `tools/round-40/sqfs-triage-v2.py` `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617`, `tools/round-39/sqfs-triage.py` `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2`, `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` `b160af3fa613d8264660a7d005adb0635fec3dffa51ba57f9b8ddeac481b195c` (at-commit copy and working-tree file hash equal — full digests in `artifacts/R41C2EntryReview/evidence.md`).
- Machine cell-by-cell diff (script + output in `artifacts/R41C2EntryReview/{celldiff.py,celldiff-output.txt}`): v2 SKILL table (`SKILL.md:363-375`) vs the interpreter's `TABLE_BLOCK` (`tools/round-40/sqfs-triage-v2.py:171-187`) → divergence in **exactly 2 cells of 1 row** (avm `cause`, avm `source`); v1 SKILL table (`SKILL.md:337-346`) vs the round-39 embedded copy (`tools/round-39/sqfs-triage.py:131-141`) → **5 decision-cell divergences across 4 rows**.
- Match semantics read at `sqfs-triage-v2.py:604-605` (`match_set`: `any` / `none` / `frozenset(values) == payload`), `:608-633` (`rule_matches`), `:636-640` (`classify`, first match wins): **exact-set equality, no contains operator**.
- Wave-1/2 anchors the findings cite, re-opened read-only: `w1/R40C1MarkerBoundary.md` (H1 `:111-127`, matrix `:92-104`), `w1/R40MistakeHunt.md` (MH-6 `:65`, quoted sentence verbatim present), `w1/R40C2ActionReview.md` (findings 4–7 `:62-72`, D5b/D7 `:55-61`), `w1/R40C2Shortcuts.md` (D2 `:156-163`, one-authority correction `:223-227`), `w2/R40W2MistakeHunt.md` (MH-4 `:45,:81-143`).
- No REA/unblob run, no carrier built, no VCS mutation, nothing installed.

Line map used throughout: SKILL block 18 supersession `:331-334`, v1 table `:336-346`, block-19 bullet `:348-359`, v2 marker `:361`, actions `:362`, header `:363`, v2 rows `:365-375` (no-squashfs 365, dep-be 366, dep-le 367, avm 368, body 369, partial 370, mixed 371, escaping 372, in-tree 373, clean 374, clean-empty 375). Interpreter: `TABLE_BLOCK` `:171-187` (rows 176–186), `--print-table` write `:1520-1522`, selftest region from `:720`. v2 entry: sources `:3-7`, recheck `:9`, What-v2-adds `:11-17`, Domain guard `:19-25`, Three outcomes `:27-35`, AVM paragraph `:37-44`, Scoring `:46-50`, Limits `:52-56`.

## Finding-by-finding at 49096c7e

### M1 — embedded `TABLE_BLOCK` still carries the pre-rewrite AVM cause — **still present** (one count misdescribed)

- `tools/round-40/sqfs-triage-v2.py:179` (stale cause, verbatim): *"mkfs_time equals bytes_used, unblob read the AVM marker and deliberately omitted -be, so sasquatch-v4be read a standard-BE body with the wrong byte order and failed; **the removal of -be, not damage, decides this row** -> rerun through a PATH wrapper named sasquatch-v4be that appends -be (REA has no flag passthrough) and remove the wrapper afterwards"*; source cell *"S112 :44-50; S121 -DFIX_BE build; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40"*.
- `SKILL.md:368` (rewritten cause, verbatim): *"…on a standard-BE body with a doctored marker that is the byte-order handshake, not damage, while a genuine AVM-layout body (little-endian metadata block lengths) extracts without -be and never reaches this row -> walk the inode-table metadata headers little-endian first: if they land on directory_table_start the image is AVM layout and its failure is damage (keep it); otherwise rerun through a PATH wrapper…"*; source cell *"S112 :44-50; S121 -DFIX_BE build; knowledge 2026-10-26-r40-sqfs-triage-v2.md :37-45"*.
- Machine diff confirms the divergence is confined to those two cells; the other 10 rows are byte-identical between SKILL and `TABLE_BLOCK`. `--print-table` writes the stale block (`:1520-1522`), and the py comment `:168` still says *"the frozen v2 table block (printed by --print-table; integrated by the L1)"*.
- The v1 copy diverges too, and by **more cells than filed**: `tools/round-39/sqfs-triage.py:139-141` carry handler `squashfs_v4_be` where `SKILL.md:344-346` carry `squashfs_v4_*` (escaping/in-tree/clean — as filed), **and** `py39:135-136` carry published-files `0` where `SKILL.md:340-341` carry `*` (dep-be/dep-le — not filed).
- **Misdescribed detail:** TableReview says *"40+ of the 45 selftest cases build their SKILL fixtures from it"*. Measured: the selftest region (from `:720`) holds 45 `@case` cases, 41 `_skel(` calls, 22 `TABLE_BLOCK` references, and exactly **19** literal `_skel(TABLE_BLOCK)` fixture builds; the rest build mutant tables (`_block(rows)`) or run the real `SKILL.md` (`c_real_skill`, `:1454+`). M1's substance is unaffected — the selftests that do use the block certify the stale cause story — but the count is wrong.
- `R40C2Shortcuts.md:223-227` prescribed the fix and the round-40 freeze did not adopt it: *"the freeze names exactly one table source (block 19 bytes in `SKILL.md`) and the interpreter's embedded block is either deleted or asserted equal to the `SKILL.md` slice by the counter; `--print-table` must print the frozen slice, not a copy."*
- **Exact text v3 must change:** the v3 interpreter ships **no second table copy** — either no embedded block, or the C2 counter asserts the embedded block equals the SKILL.md v3 slice byte-for-byte and `--print-table` prints the frozen slice. If selftest fixtures need a literal block, derive it from the SKILL slice at selftest time. Any kept copy must carry the v3 cause text (M2/M3 repairs) and cite the v3 entry; the round-39 v1 copy's decision cells must match the SKILL v1 table or be marked divergent-on-purpose in its docstring.

### M2 — `body-extractor-failure` cause falsified by the marker-stripped population — **still present**

- `SKILL.md:369` and `py:180` carry the **identical** falsified cause (both copies, so fixing one fixes both): *"the extractor ran and still failed with zero files published, so the fault is in the image body or the extractor build **rather than the endianness handshake** -> keep the failing command and stderr from diagnostics, diff the carrier against a known-good arm, and never patch the envelope into a success"*; source *"S120 report.py :91-98; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40; R39-CL3 D1"*.
- The falsifying population is measured and committed: `w1/R40C1MarkerBoundary.md` H1 (`:111-127`) and matrix rows `d2`/`m1s`/`m2s` (`:95,:102,:104`) — a genuine AVM-layout body with the marker stripped gets `-be` appended, publishes **0** files, records `extractor-failure`, P=0, while `sasquatch-v4be` **without** `-be` extracts the same body (4/256 files, exit 0). `w1/R40MistakeHunt.md:65` MH-6 states it verbatim: *"The marker-stripped shape is exactly the frozen `body-extractor-failure` tuple (H15: `H=be, G=extractor-failure, BE=yes, P=0` → "image body or header is damaged")"* — the TableReview's quote is accurate.
- The stale-wrapper half is also still missing: ActionReview D5b (`:55-58`) required **both** rows' causes to carry the note that a leftover `sasquatch-v4be` PATH wrapper re-adds `-be` exactly when unblob omits it; the avm row got *"remove the wrapper afterwards"*, the body row (`:369`/`:180`) got nothing.
- **Exact text v3 must change** (body row cause): name the handshake path, e.g. *"…the fault is in the image body or the extractor build — or the endianness handshake reached this row the other way: a genuine AVM-layout body whose marker was stripped receives `-be` and fails (measured, `R40C1MarkerBoundary.md` H1), and a leftover `sasquatch-v4be` PATH wrapper re-adds `-be` exactly when unblob omits it — restore the marker or drop `-be` and rerun before calling the body damaged; keep the failing command and stderr from diagnostics, and never patch the envelope into a success."* Source cell adds the MarkerBoundary/MH-6 anchors and marks which half is measured vs source-cited.

### M3 — avm row's action contradicts its cause's damage branch — **still present**

- `SKILL.md:368`: action `wrap-extractor-be`; cause contains *"if they land on directory_table_start the image is AVM layout and its failure is damage (keep it)"*; bullet `SKILL.md:356-357`: *"The AVM-marker row covers a doctored marker on a standard-BE body only; a genuine AVM-layout body extracts without `-be`"*.
- The draft precedence (`plans/round-41-claims.md` rule 5) keeps the single signature — `extractor-failure` ∈ G, P=0, BE=no, handler `squashfs_v4_be` → `avm-marker-be-dropped` — so a damaged genuine-AVM body still scores `(avm-marker-be-dropped, wrap-extractor-be)` while the cause says keep it. The contradiction survives unless the prose repair changes the row's cause **and** the bullet.
- **Design constraint the v3 drafter must know (new, N4):** the frozen independent evaluator is *"written from the precedence text above, never reading the table, the interpreter or the generator's class map"* and sees only envelope features (OP/PR/H/G/D/BE/SR/P). A layout-walk-conditional **row** (AxisFit F5's split option) is not evaluator-scoreable — the walk result is not an envelope feature. The only evaluator-compatible repair is the cause-level option: the layout walk becomes a **gating procedure above the table**, not a row.
- **Exact text v3 must change:** (a) delete the *"(keep it)"* prescription from the row's cause; (b) state the walk once above the table: *"walk the inode-table metadata headers little-endian; if they land on `directory_table_start` the body is genuine AVM layout and the failure is damage — do not apply the wrapper row; preserve the command and stderr"*; (c) rewrite the bullet so "only" matches the row's actual admissibility: the signature over-admits, the walk gates its use, only the doctored-marker case takes the wrapper; (d) the v3 entry's Limits disclose the over-admission.

### L1 — block-18 supersession verb — **still present**

- `SKILL.md:331-334` verbatim: *"Superseded for routing by rule block 19 (table v2, round 40); this v1 table stays as the round-39 record and **mislabels** mixed-link images, partial failures, empty trees and non-firmware envelopes (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`)."*
- The cited entry `:27-35` itself says *"Three outcomes v1 **could not label**"* — partial failures and empty trees are unlabeled (`unclassified`), not mislabeled; mixed and non-firmware are mislabeled. The SKILL sentence's verb is wrong for half its list.
- **Exact text v3 must change:** split the verb — *"mislabels mixed-link images and non-firmware envelopes; cannot label partial failures and empty trees"* — and (F7, below) widen the scope word and add the avm row to the list. When block 20 lands, block 19 needs its **own** supersession sentence with the same discipline: v2 mislabels nothing on the scored set; its defects are the false cause stories (M1/M2) and the avm row's action-vs-cause contradiction (M3), so the v2 sentence should say that, not "mislabels".

### L2 — wrapper delivery unmeasured, source cell unmarked — **still present**

- `SKILL.md:368` source cell *"S112 :44-50; S121 -DFIX_BE build; knowledge 2026-10-26-r40-sqfs-triage-v2.md :37-45"* — no `[INFERENCE]` marker (quoted verbatim in `celldiff-output.txt`). ActionReview finding 4 (`:62-66`) required marker-or-measurement; neither happened; no wave artifact exercises the PATH wrapper through REA.
- **Exact text v3 must change:** the v3 wrapper row's source cell carries `[INFERENCE]` on the PATH-wrapper delivery through REA — or the mechanism is measured pre-freeze on development inputs only (round-40 carriers are authorized development inputs).

### L3 — dep rows omit REA as the minter of the gap kind — **still present**

- `SKILL.md:366` source *"S112 :68-69; S120 command.py :69-77,101-102; round-36 K3/before.json"*; `:367` source *"S112 :25,37,68-69; S120 command.py :101-102; round-36 K3/before.json"* (`py:177-178` identical). No S119/REA citation, though `missing-extractor-dependency` is REA's vocabulary (`firmwareAnalysis.js:84-91`).
- **Exact text v3 must change:** both v3 dep rows' source cells add *"S119 (REA mints the gap kind)"*.

### L4 — partial row's oracle half unmarked — **still present**, plus a defect no review filed (N1)

- `SKILL.md:370` = `py:181` cause: *"…keep the published files and the failing command, **match files to the oracle only by relative-path suffix and sha256**, mark the run incomplete, and never score the set as clean"* — no `[INFERENCE]` marker (ActionReview finding 5, `:67-70`).
- **N1 (new):** the same rows prescribe the matcher R40-CL1 refrozen the counter away from. `SKILL.md:370` (partial), `:374` (clean: *"match files to the oracle by relative-path suffix and sha256, and ignore nested carves"*), and the v1 rows `:341`/`:346` all instruct suffix matching; `corpus/lessons/round-40.md` R40-CL1 records `same_rel` suffix matching as the defect that made round-40 C1 fail. The suffix instruction was the R40-CL1 defect's prose twin and no round-40 review flagged it.
- **Exact text v3 must change:** the v3 partial and clean rows' causes say *"match files to the oracle by **exact path relative to the chunk extract root** and sha256"* (no suffix language), and the oracle-comparison half carries `[INFERENCE]` unless a partial run is oracle-compared pre-freeze.

### L5 — escaping row absorbs combined gap sets — **still present at bytes; the draft precedence repairs the mechanism**

- `SKILL.md:372` = `py:183`: escaping row gap-kinds cell `*` (decision cells quoted in `celldiff-output.txt`). With `match_set`'s exact-set equality (`py:604-605`) and no contains operator, an SR=yes envelope with `G={unpublished-entry, depth-limited}` falls through mixed (exact `{unpublished-entry}`) to escaping → `expect-link-absent`; AxisFit measured the `extractor-failure` variant (H11 + injected gap → escaping).
- The draft precedence repairs this structurally: rule 7 (`depth-limited` ∈ G → `depth-limited-nested`, *"whatever symlink gaps accompany it"*), rule 8 (membership), rule 9 (SR=yes and G=∅ → escaping), and the kill control *"no contains-operator"* guards the grammar change.
- **Exact text v3 must change:** the v3 escaping row's gap-kinds cell is the **empty set** (not `*`); the failure rows carry membership cells; the v3 interpreter selftest adds a multi-kind gap case (`G={extractor-failure, unpublished-entry}` → partial row) — AxisFit F6's smallest correction, still to be scheduled.

### L6 — clean row's "no symlink was removed" overclaims — **still present** (re-verified in the installed source)

- `SKILL.md:374` = `py:185`: *"every regular file was published, no gap was recorded and **no symlink was removed** -> …"*.
- My own read of the installed unblob 26.6.4 (`…/site-packages/unblob/extractor.py:67-72`): `raw_target = os.readlink(path)`; `if not raw_target: logger.error("Symlink with empty target, removing."); path.unlink(); return path` — **no** `task_result.add_report(...)`, so an empty-target symlink is removed silently and such an envelope (G=∅, SR=no, P>0) lands on clean with a false cause claim.
- **Exact text v3 must change:** the v3 clean row's cause scopes the claim: *"no symlink removal was reported (note: unblob removes an empty-target symlink without a `MaliciousSymlinkRemoved` report — extractor.py :67-72)"*.

### L7 — OOD/no-match pair collapse undisclosed — **still present**

- The v2 vocabulary keeps `none` as clean's action (`SKILL.md:362`, `py:173`), so `(clean, none)` shares its action half with the no-match pair `(unclassified, none)` (Shortcuts D2, `:156-163`); the entry's Limits `:52-56` carry no granularity disclosure.
- **Exact text v3 must change:** the v3 entry's Limits (and the claims' disclosure) state that an OOD envelope and any other no-match envelope share `(unclassified, none)` and are separated only by the counter's `row: null`; alternatively reserve `none`/`unclassified` in the v3 grammar (Shortcuts D2's correction) — a grammar change, so disclosure is the default.

### AxisFit findings

- **F1 — partially already fixed.** `SCORECARD.md:3443` (R40-C2 row) already carries: *"**met**; increment bounded: 18/26 envelopes were already decided by v1 and the expected labels come from the generator's class map (`.ufo/waves/round-40/w2/R40W2C2AxisFit.md`)"*, and the entry's Scoring `:46-50` discloses the 18/26 v1 agreement on the dev envelopes with the eight misses named. **Misdescribed detail:** AxisFit's "state the partition next to the score" is thus already done; what remains unstated anywhere is the abstention framing (2 of the 26 are `unclassified`/`none` — absence of a decision) and the "13 independent decisions, not 26" count. **v3 requirement:** the R41-C2 claims and the v3 entry carry the equivalent partition for the new set: 36 held-out envelopes = 26 v2-decided ground (v2's 13 classes × 2) + 10 new (5 combined/new classes × 2).
- **F2 — already fixed by the R41-C2 design.** The claims state the labels come from the precedence text, the evaluator never reads the table/interpreter/generator class map, and *"the generator's own class expectation agrees with the evaluator on every envelope (a disagreement is reported and fails the claim)"*. No frozen byte carries the defect; the v2 entry's `:46-50` wording stays as record and the v3 entry must not copy it.
- **F3 — still open in the claims text.** The claims call the set "held-out" without the re-observation clause. **v3 requirement:** one clause in the claims and the v3 entry's Scoring paragraph: held-out **bytes**; the 26 v2-class envelopes' decisions were already answered by the round-40 held-out run committed with that freeze.
- **F4 — still present.** `SKILL.md:348-349`: *"Table v2 reads eight fields of an REA 6.5.0 envelope, the six of rule block 18 plus `operation` and `provider.id`"*; AxisFit measured an all-`D`-wildcards table scoring 26/26 (`D` redundant with `H` on the class set). **v3 requirement:** block 20's intro says *"screens N fields; `D` only picks the dep row and is redundant with `H` on the scored classes"* — or the held-out set gains a `D`-discriminating envelope (not in the draft's class list, so prose).
- **F5 = M3** (above). **F6 = L5's mechanism plus the partial-row exact-set** (above; repaired by precedence rules 4/7/8/9 + the "no contains-operator" control; the v3 rows and selftest must implement it). **F7 = L1's scope half** (above): `SKILL.md:331` *"Superseded for routing"* is too narrow — v1's action cells still carry procedures and its avm row's unconditional wrapper is exactly what v2 refined; the supersession sentence must cover the action column and list the avm row.

## What the draft's repair list omits (v3 must add all seven)

`plans/round-41-claims.md` R41-C2 names M1, M2, M3, L1, L2/L4, L3, L6 and R40-CL4. Missing:

1. **L5/F6 structural remainder** — escaping-row G=∅ pin, membership cells on the failure rows, the multi-kind selftest case (the precedence text implies it; the rows and selftest must implement it).
2. **L7** — the no-match/OOD pair-collapse disclosure (v3 entry Limits + claims).
3. **F4** — "screens N fields" wording (or a `D`-discriminating envelope).
4. **F7** — block 19's own supersession sentence when block 20 lands (scope covers the action column; verb discipline; the avm row listed).
5. **N1** — the suffix-matching prose: v3's partial/clean rows must prescribe exact extract-root-relative paths (`SKILL.md:370/:374` still prescribe the matcher R40-CL1 removed from the counter).
6. **Timeout corner** (TableReview residual, still open): the v3 entry's Limits must state that `ExtractorTimedOut` records `cmd` not `command` (`report.py:133-138`) so BE reads `n/a` on a timed-out run, and that whether a timeout yields an `extractor-failure` gap is unverified `[INFERENCE]`.
7. **F1/F3 wording** for the new entry and claims (partition + re-observation clause).

## Claims the v2 entry carries that v3 supersedes

- `:52-56` *"Not covered: genuine AVM-layout outcomes (that is the C1 surface), `unknown-chunk-handler`, `encrypted-chunk` and `depth-limited` envelopes, and anything about extracted programs."* — v3 lifts the `depth-limited` half (new `depth-limited-nested` row + combined classes) and touches the genuine-AVM half (the damage branch becomes a gating procedure); `unknown-chunk-handler`, `encrypted-chunk` and extracted programs stay not-covered and must be carried into the v3 entry's Limits.
- `:46-50` Scoring — the generator-assigned-labels framing is superseded by the independent-evaluator design (F2/D3); the v3 entry restates scoring from the precedence text and carries the partition/re-observation clauses.
- `:37-44` AVM paragraph — stays true as record (*"its failure would be damage"*); v3's gating procedure must cite it; the v2 entry should gain a supersession pointer (the pattern the r39 entry got in round 40) so a reader of the v2 entry is routed to v3.
- `:19-25` Domain guard — v3 keeps it (precedence rule 1); the provider-alone disclosure (`:25`) must be carried forward.
- `:9` recheck — stays valid while block 19 remains in SKILL.md; v3 gets its own recheck line.

## Residual risk and verification gaps

- I ran no REA/unblob extraction and built no carrier (bounds). Extractor-behaviour claims rest on the committed wave-1/2 measurements cited above plus my read of the installed unblob 26.6.4 source (`extractor.py:59-98`).
- The omissions list is against the draft as it stands now (untracked `plans/round-41-claims.md`); the draft may change before the freeze.
- I did not re-run the v2 interpreter or the C2 counter: TableReview and AxisFit already re-verified the 26/26 independently at `42c10a58`, and my item is the defect list, not the score.
- My v1-copy divergence list (5 decision cells) is broader than TableReview's parenthetical (which named only the three handler cells); no finding misstates it — it said "decision cells" without an exhaustive list.

## Tooling record

Nothing installed, upgraded or removed; no pacman transaction. Used: system `python3` (scratch scripts, stdlib only), read-only `git` (`rev-parse`, `status --porcelain`, `show`), the `read`/`grep`/`write` tools, and read-only reads of the installed unblob 26.6.4 (`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/extractor.py`). Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2EntryReview` removed at finish; everything cited is in `artifacts/R41C2EntryReview/` (no vendor bytes, no carrier, nothing > 5 MB).

Report: .ufo/waves/round-41/w1/R41C2EntryReview.md
