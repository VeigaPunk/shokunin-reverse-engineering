# ADocsOverclaim — round 34, run-6 re-dispatch, wave 2

Seat `L1Kaidoku34-2.ADocsOverclaim`. Prompt read first at
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/w2/prompts/ADocsOverclaim.md`
(first bytes `/skill:godspeed`; verbatim directive followed). Assignment: read the five wave-1 scribe
drafts and list **every sentence that would overclaim now that R34-C2 is stopped**, with a corrected
sentence for each.

Claim context, not re-scored, not reopened, not re-frozen by this seat: R34-C2 (`axis` depth, type
"capability acquisition"), freeze `c79bbe7b0959132b9873ff3431cf5eb313b58b33`, stop record
`.ufo/waves/round-34/r34b/claim-stop.json` (sha256 `e6303d06…`, landed `cd75b92e`), verdict
`falsified measure; honest stop after wave-1, before any capability or score credit`. Inherited
R34-C1 was not opened, executed or scored here; its production reader and twelve carriers were not
touched.

Result in one line: **34 sentences across the five unlanded drafts would overclaim after the stop,
34 corrected**; every correction is grounded in the stop record plus one reproduction of its
decisive counterexample (nameset 8/8 at two seeds, gate CLEAN while that class is unregistered,
REFUSED once registered); the tracked docs landed at `66b84027` already carry the stop and use none
of the draft blocks, and **4 landed-text residuals** plus one empty untracked file at the draft's
own proposed entry path need the L1's decision.

Contract compliance: writes are this report and
`/fast/scratch/hyaku/kaidoku-r34b/w2/ADocsOverclaim/` only. No lane doc, instrument, claim or stop
record was edited. No `git add/commit/stash/checkout/reset/pull/push`, no `jj` command, no clone in
the lane (a `cp -a` copy into scratch was used for every run). No ELF carrier, fixture or reader was
executed as a program of interest; readers ran only as `python3` children of a counter. No network.
No `pacman`; nothing installed (system `/usr/bin/python3` = 3.14.8 sufficed), so the tooling ledger is
"none". No `lsp` device is mounted in this seat's tool set and the objects audited are Markdown
prose, so every semantic check below is text search over named lines, labelled as such.

---

## 1. Axes named (Godspeed)

| axis | proxy used here | direction | kept move |
|---|---|---|---|
| A1 stop fidelity | every correction restates the stop record's own verdict without widening or softening it | closer to the record = better | §3, §4 |
| A2 sentence coverage | overclaiming clauses found per draft, against the four classes the assignment names (capability notice, score move, coverage credit, identity-keying defeat) | more found and classified = better | §4 (34 items) |
| A3 grounding | each "why" is one observed receipt, one exact line, or one file digest | observed-only = better | §2, §4 |
| A4 landing safety | does the corrected text collide with what is already landed at `66b84027`? | no collision = better | §3, §5, §6 |
| A5 path/custody | does any draft pointer name a file that exists and is committed? | exists+committed = better | §5 L3, §4 E2 |

Cheap parallel iterations kept: one scratch copy + pin re-hash; two seeds of the decisive reader;
two gate runs (frozen config, superset config); one custody sweep over the six doc paths. No move was
made at the cost of another axis; nothing below edits an instrument, claim, target, class or receipt.

---

## 2. What I ran (exact argv, exit, UTC)

All times UTC, read from `date -u` around each command. Scratch root
`S=/fast/scratch/hyaku/kaidoku-r34b/w2/ADocsOverclaim`.

| # | UTC | command (cwd = `$S` unless stated) | exit | observed |
|---|---|---|---|---|
| R1 | 07:29:24Z | `mkdir -p $S/root/tools $S/receipts && cp -a <lane>/tools/round-34 $S/root/tools/ && cp <lane>/.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py $S/nameset.py && sha256sum $S/nameset.py $S/root/tools/round-34/{mini-fix/mini-counter.py,replay-gate.py,c2-shortcut-gate-counter.py}` | 0 | nameset `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` (equals `claim-stop.json.source_sha256`); counter `43ef669f…`; gate `8fa94b23…`; C2 counter `41d59703…` — all equal `claims[0].pins` |
| R2 | 07:29:29Z | `/usr/bin/python3 -I -B root/tools/round-34/mini-fix/mini-counter.py --root $S/root --control-reader $S/nameset.py --seed kaidoku-r34-mini-v1` | 0 | `matched 8 target 8 met True finding records_match` (`receipts/nameset-green-kaidoku-r34-mini-v1.json`) |
| R3 | 07:29:29Z | same, `--seed alt-1` | 0 | `matched 8 target 8 met True` (`receipts/nameset-green-alt-1.json`) |
| R4 | 07:29:35Z | `/usr/bin/python3 -I -B $S/root/tools/round-34/replay-gate.py --root $S/root --config $S/root/tools/round-34/gate-config-mini.json --json-out $S/receipts/gate-green.json` (nameset present in the root, **not** registered) | 0 | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` |
| R5 | 07:29:35Z | same gate, `--config $S/cfg-plus-multiset.json` — the green config with `{"class":"content-multiset","path":"tools/round-34/mini-fix/readers/nameset.py"}` appended | 2 | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=content-multiset` |
| R6 | 07:31:47Z–07:33:11Z | read-only custody sweep, cwd `<lane>`: `git rev-parse HEAD`; `sha256sum .ufo/waves/round-34/r34b/claim-stop.json`; `git log -1 --format='%H %cI %s' cd75b92e`; `git status --porcelain`; `git log --oneline -3 -- SCORECARD.md corpus/knowledge corpus/lessons/round-34.md`; `grep -n 'R34-C2' SCORECARD.md corpus/lessons/round-34.md LOG.md`; `grep -n 'P34-shortcut-replay' SKILL.md` and a second grep for `shortcut-replay`; `awk 'NR==111' corpus/SOURCES.md`; `sha256sum corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md`; `wc -l` on it | 0 (all; `grep` for absent strings returned 1 as expected) | HEAD `66b84027`; stop record `e6303d06…`; stop commit `cd75b92e` (2026-10-25T04:23:47-03:00); landed docs listed in §3; the draft's proposed entry path exists but is **0 bytes** (`e3b0c442…`) and untracked |

Read-only source reads (no execution), with the line anchors used below:
`w1/ScribeKnowledgeEntry.md` (sha256 `f948247c…`), `w1/ScribeScorecardRow.md` (`e026f00f…`),
`w1/ScribeSkillRegistry.md` (`f3a0a7c0…`), `w1/ScribeLesson.md` (`b4164c04…`),
`w1/ScribeSourcesRow.md` (`f20e147b…`); `claims.json` (`de3afbfb…`); `claim-stop.json`;
`SCORECARD.md:3347-3368`; `corpus/lessons/round-34.md:43-72`; `LOG.md:3095-3103`;
`SKILL.md:1209-1221`; `corpus/SOURCES.md:111`;
`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`; `corpus/QUALITY.md:77`
(QUALITY 67); `tools/round-34/mini-fix/mini-counter.py:50-100,104-157`;
`tools/round-34/gate-config-mini.json`; `w1/CtlMultiset-files/nameset.py`.

Why R2–R5 are in scope: the corrected sentences must not assert the counterexample on the stop
record's authority alone. R2/R3 re-observe it (8/8, two seeds); R4/R5 show the exact asymmetry every
correction below has to preserve — **CLEAN while the class is unregistered, REFUSED once registered**.

---

## 3. State that frames every correction

Landed at HEAD `66b84027` ("round-34: land the stopped claim's record — SCORECARD section, LOG entry,
lesson M34-5..M34-11, QUALITY 68-73, SKILL instrument registry, S106, knowledge entry and README
rows"), read-only:

| surface | landed state | carries the stop? |
|---|---|---|
| `SCORECARD.md:3347-3368` | Round-34 run-6 section, heading "…six clauses met, stopped on an unregistered class"; verdict cell `falsified measure / honest stop`; owned axes 10→10; "No capability row enters" | yes |
| `corpus/lessons/round-34.md:43-72` | `## Claim R34-C2 — frozen clauses met, capability denied`; M34-5..M34-11; five controls; S106 gate bullet | yes |
| `LOG.md:3095-3103` | C2 paragraph with a `- **Stop.**` bullet and record-defect bullet | yes |
| `SKILL.md:1209-1221` | `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)`; five instrument rows; limits pointing at the stop entry and QUALITY 68-73 | yes |
| `corpus/SOURCES.md:111` | S106 row, `used-by` = `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | yes |
| `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` | `status: instrument retained; **capability denied** — the claim stopped`; "Why the capability is denied"; "The repair route (not a claim)" | yes |

None of the five wave-1 draft blocks was landed: `SKILL.md` has zero hits for `round34-C2`; the
landed registry section is a different table written by the L1; the landed lesson ids M34-5..M34-11
name different defects from the draft's M34-6..M34-10; the landed entry is the `-stop` file, not the
draft's proposed `…-r34-pre-freeze-shortcut-replay-gate.md`. **The overclaims therefore live only in
the drafts**, and each item below is a "must not land as drafted" instruction. Two pointers are
already live hazards: the draft's proposed entry path exists as a 0-byte untracked file (§5 L3), and
the draft's `used-by` cell names that path (§4 E2).

Byte state caveat: the table above is what I read from the **worktree** at 07:29Z-07:34Z, not
necessarily what `66b84027` contains. `git status --porcelain` at 07:34:21Z shows
`M corpus/QUALITY.md`, `M corpus/SOURCES.md`, `M corpus/lessons/round-34.md` (L1 edits landing while
this audit ran); `SCORECARD.md`, `LOG.md`, `SKILL.md` and the `-stop` entry were clean at their
commit. Hashes of the bytes I read: `SCORECARD.md` `eb63cbfc…`, `LOG.md` `2e552b42…`, lesson
`bd7b4145…`, landed entry `0cb388bc…`.

Anchor drift the landing editor must also handle: the draft's insertion anchors (SKILL tip "line
1207", `SCORECARD.md:626` / `:3345`, "after `SOURCES.md` line 111") are all stale at `66b84027`.

---

## 4. Overclaim inventory

Legend for "why": `SR` = `claim-stop.json` verdict/kill-rule text; `R2–R5` = my runs in §2; `EV` =
exact file/line evidence. Quoted sentences are verbatim; `…` only shortens between clauses and never
inside the overclaiming clause.

### 4.1 `w1/ScribeKnowledgeEntry.md` — draft entry for `corpus/knowledge/` (9 items)

| id | line | sentence that now overclaims | why it overclaims | corrected sentence |
|---|---|---|---|---|
| A1 | 190 | `# Pre-freeze shortcut-replay gate: refuse a counter that shape can satisfy` | The instrument does not refuse a counter shape can satisfy: `nameset.py` is shape-blind and the frozen gate printed CLEAN on it (R4, exit 0) and REFUSED only once registered (R5, exit 2). SR: "falsified measure". A closure reads the title as the capability. | `# Pre-freeze shortcut-replay gate: a registered-class refusal, and the unregistered class that stopped R34-C2` |
| A2 | 205-206 | "This entry records the gate built for the next counter and, more usefully, exactly how narrow its CLEAN verdict is." | "built for the next counter" offers the gate as the admission instrument for a future counter; SR's `not_claimed` list denies capability, and the gate's class set is what failed. | "This entry records the gate, the stop that retired it as admission evidence before any capability credit, and exactly how narrow its CLEAN verdict was." |
| A3 | 224-226 | "A reader that slices fixed byte positions, replays a memorized record set, or scans printable runs has none of the four — it can match bytes without ever associating a name with the record that declares it." | Falsified by this round's decisive class: `nameset.py` scans printable runs *and* replays a memorized table, and matches the canonical per-record output 8/8 (R2/R3) because the fixture set's name→scalar association is itself memorizable. The sentence states the impossibility the stop disproved. | "A reader that slices fixed byte positions, replays a memorized record set, or scans printable runs has none of the four — and it can still match the canonical per-record output whenever the fixture set's name→scalar association is itself memorizable. The content-multiset class does exactly that (8/8), which is why R34-C2 stopped." |
| A4 | 145-149 | "This is a completeness limit, not a claim miss: no registered clause moved, and nothing was re-scaled. The durable fix would be a green surface that also mutates the scalars the memorizer echoes …, or registering a topology class — neither is done here." | `not a claim miss` is the exact sentence the stop contradicts: SR applies the kill rule to this finding. And offering the fix as this entry's route invites a repair of a stopped claim. | "No registered clause moved and nothing was re-scaled, but this is the round's decisive counterexample: a target a control that skips the claimed work can reach is not an improvement, so R34-C2 stopped before any capability or score credit. The fresh-content surface and the class-set assertion are next-round work under QUALITY 69/70, not a repair of this claim." |
| A5 | 302-304 | "Defeated by (2)+(4): basename replay, whole-file digest replay, fixed byte slices, and `name_off` used as an index. **Not touched:** the record count, the record order and every scalar. A replay keyed on those scalars therefore still scores 8/8 — see Limits." | As a partition it omits the invariant that decided the round: `permute()` preserves the **multiset of names** (only pool order and `name_off` change), so the decisive reader keys on the sorted SONAME set and needs no traversal. The "Not touched" list reads as complete; it is not. | "Defeated by (2)+(4): basename replay, whole-file digest replay, fixed byte slices, and `name_off` used as an index. **Not touched:** the record count, the record order, every scalar, and the *set* of names in the pool — only pool order and `name_off` change. Replays keyed on the scalars, and the decisive replay keyed on the sorted set of SONAME tokens (`w1/CtlMultiset-files/nameset.py`, sha256 `2e8feaea…`, reproduced 8/8 at seeds `kaidoku-r34-mini-v1` and `alt-1`, 2026-10-25T07:29:29Z), still score 8/8." |
| A6 | 186 | "source: S106 — binutils `readelf.c` at the pinned release tag recorded in the SOURCES row" | Asserts a landed registry row. At the draft's time none existed (S106 landed only at `66b84027`, `corpus/SOURCES.md:111`, 07:32:53Z). A pointer to a row that did not exist is a fabricated citation. | "source: S106 — binutils `readelf.c` at tag `binutils-2_47` (release commit `6ce87bbc`), registry row `corpus/SOURCES.md:111` (landed `66b84027`); captures …; local instruments under `tools/round-34/` at `c79bbe7b…`" |
| A7 | 187 | "verified-at: … production verdicts and the six C2 clauses remain bound to …/after/c2-at-instruments.json" | Binds the entry's verification to a receipt the stop says "is not the whole test". A reader takes the six clauses as the verdict. | "verified-at: …; the claim was then stopped after wave 1 (`.ufo/waves/round-34/r34b/claim-stop.json`, landed `cd75b92e`): the six clauses hold on the frozen bytes and an unregistered content-multiset class meets the same 8/8 target, so this entry records an instrument and its stop, not a capability." |
| A8 | 188 | "recheck: … `--config tools/round-34/gate-config-mini.json` (expect REPLAY_GATE_CLEAN, exit 0) …" | An expected-CLEAN recheck is the language of a passing capability check. After the stop, CLEAN is only determinism of the frozen bytes and is class-set-relative (R4 vs R5). | "recheck: … `--config tools/round-34/gate-config-mini.json` (expect REPLAY_GATE_CLEAN, exit 0 — determinism only: CLEAN means `no registered class meets the target` and is not claim evidence; adding `w1/CtlMultiset-files/nameset.py` as an eighth class returns REPLAY_GATE_REFUSED, exit 2) …" |
| A9 | 312-313 | "it exists to prove the gate can refuse, not to demonstrate any decoding." | "prove the gate can refuse" is a capability notice; what ran is the refusal branch for one registered class, and an unregistered class at 8/8 coexists with CLEAN (R4). | "it exists to exercise the refusal branch for one registered over-target class, not to demonstrate any decoding." |

### 4.2 `w1/ScribeScorecardRow.md` — DRAFT A (Capabilities row) and DRAFT B (Round-34 subsection) (13 items)

| id | line | sentence that now overclaims | why it overclaims | corrected sentence |
|---|---|---|---|---|
| B1 | 182 | "`REPLAY_GATE_CLEAN` (exit 0) only when the structural control meets it and every shortcut stays below" | False without `registered`: R4 prints CLEAN with an 8/8 unregistered reader in the root. The omitted word is the whole stop. | "…`REPLAY_GATE_CLEAN` (exit 0) only when the structural control meets it and every **registered** shortcut stays below; an unregistered class can meet the target and still print CLEAN (measured with `nameset.py`, 2026-10-25T07:29:35Z)" |
| B2 | 182 | "At `c79bbe7b` it refused the shape-only counter (label-memorization 8/8) and cleared the identity-defeating counter on the same eight fixtures (structural 8/8, seven shortcuts ≤1/8)" | "cleared the identity-defeating counter" is the fabricated success: SR's verdict is `falsified measure`, and the surface is identity-defeating only against label/size/digest/fixed-offset/order, not against the name multiset. | "At `c79bbe7b` it refused the one registered shape-only class that reaches target (label-memorization 8/8 on the red surface) and printed CLEAN on the green surface, where the seven registered classes stay ≤1/8; an eighth, unregistered content-multiset class meets the same 8/8 target, so R34-C2 is a falsified measure and no capability row enters." |
| B3 | 181-183 | The DRAFT A row itself, with the instruction "append after the round-17 row, `SCORECARD.md:626`" | SR: "no capability row enters SCORECARD"; the landings enforce it (`SCORECARD.md:3347` — "No capability row enters"). | Do not append any Capabilities row. If the corrected text is kept, it belongs in the stopped-claim subsection (as landed at `SCORECARD.md:3347-3368`), labelled `falsified measure / honest stop`. |
| B4 | 188 | "The frozen green and red configs and the frozen `mini-counter.py` are not affected; the class inventory and receipt-field consistency are open repair ground" | No frozen byte changed, but the guarantee those bytes were believed to support is exactly what failed (R4/R5); and "open repair ground" on a stopped claim invites work the stop forbids. | "No frozen byte changed, but the guarantee those bytes were believed to support is falsified: CLEAN means only that no *registered* class meets the target, and an unregistered content-multiset class does. The class inventory and receipt-field consistency are routed to QUALITY 69-72 for a future round; R34-C2 is not repaired or reopened." |
| B5 | 191 | "Fit check against the table's own rule (…): the intended invocation ran and is receipted; the row adds no axis score and claims no domain result." | Running + a receipt is not the table's rule; the rule is a demonstrated capability, and the demonstration failed. "Claims no domain result" does not cure a capability row with no capability. | "Fit check: the table's rule requires a demonstrated capability; this round's demonstration failed (an unregistered class meets the target), so no row enters. The receipts are retained as stopped-claim evidence only." |
| B6 | 200 | `### R34-C2 — pre-freeze shortcut-replay gate (capability acquisition, depth)` | A heading that types the round as a capability acquisition while SR types it `falsified measure`. | `### R34-C2 — pre-freeze shortcut-replay gate (attempted capability acquisition, depth): falsified measure / honest stop` |
| B7 | 202 | "R34-C2 / depth, a capability acquisition: the lane now owns a **pre-freeze, config-driven shortcut-replay gate** …" | "now owns" is the capability notice; SR's `not_claimed` lists capability first, and "owned" contradicts "capability denied" in the landed entry. | "R34-C2 / depth, an attempted capability acquisition: the round built and froze a pre-freeze, config-driven shortcut-replay gate …; it was stopped in wave 1 and is retained as a historical instrument, not as an owned capability." |
| B8 | 202 | "the surface this round moves is the lane's structural-counter admission instrument, **not** a numeric proxy score" | "moves" asserts movement; the stop moved nothing and admitted nothing (SR: "owned scores stay 10->10"; landed SCORECARD: "no numeric proxy moved"). | "the surface this round attempted to move was the lane's structural-counter admission instrument; no proxy and no capability moved, so depth stays 10." |
| B9 | 208 | "**target met as measured at the frozen instruments**; owned scores 10→10, delta 0; capability row entered" | Two falsehoods in one cell: the target is not a claim pass (SR says the frozen verdict "is not the whole test"), and no capability row enters. | "the six frozen clauses hold on the frozen bytes (exit 0) — not the whole test; an unregistered content-multiset class meets the same 8/8 target, so the verdict is **falsified measure / honest stop**; owned scores 10→10, delta 0; **no capability row**" |
| B10 | 210 (and report body 121) | "the green surface is the identity-defeating `mini-counter` … so label, size, digest, fixed offsets and build order cannot identify an input and only record-array traversal resolves a name." | Measured false in its last clause: `nameset.py` resolves names from the token set with no traversal and matches (R2/R3). The permutation preserves the name multiset. | "the green surface permutes the name pool and rewrites every `name_off` (same 512-byte size, same record order, same value bytes), so label, size, digest, fixed offsets and build order cannot identify an input, and associating a name with its *record* requires record-array traversal; the *set* of names survives the permutation, so a reader that keys on that set takes the association from a table and still meets the target." |
| B11 | 216 | "Controls (all pre-registered, all landed, none meets the target)" | "none" is true only of the seven registered classes; the decisive class meets it (R2/R3; SR `decisive_counterexample`). | "Controls (all pre-registered, all landed; none of the seven **registered** classes meets the target — an unregistered content-multiset class does, 8/8 across three seeds, which is why the claim stopped)" |
| B12 | 218 | "**Verdict: target met at the frozen instruments (six clauses true, exit 0). Outside closure pending — `[OUTSIDE-R34-C2: pending]` …** The claim's own kill rule was not triggered, so nothing is relabelled, rescaled or re-frozen." | Three overclaims: "target met" as the verdict, a pending outside closure for a claim nobody offers, and "kill rule was not triggered" — SR's `kill_rule_applied` says the opposite (`claim-stop.json` has no outside/pending field, so `[OUTSIDE-…]` is also unbacked). | "**Verdict: falsified measure / honest stop (wave 1; `claim-stop.json`, landed `cd75b92e`).** The six frozen clauses hold on the frozen bytes (exit 0), and that is not the whole test: an unregistered content-multiset class reaches the same target, so the kill rule was applied and nothing was relabelled, rescaled or re-frozen. No outside closure is pending — no capability or score is offered." |
| B13 | 220 | "Owned scores remain **10 → 10** … the capability row is a capability record, not an axis score." | The clause exists to justify a capability row; there is no row and no capability record to enter. | "Owned scores remain **10 → 10** …; no capability row and no capability record enters — the instrument is retained in the stopped-claim registry only (as landed at `SKILL.md:1209`)." |

### 4.3 `w1/ScribeSkillRegistry.md` — registry rows (2 items)

| id | line | sentence that now overclaims | why it overclaims | corrected sentence |
|---|---|---|---|---|
| C1 | 61 | "Generic, config-driven pre-freeze replay gate (QUALITY 67): runs the config's counter argv once per reader …" | `(QUALITY 67)` reads as a compliance label. The gate did not discharge QUALITY 67: the obligation exists to catch the structure-blind replay, and an unregistered class met the target (R2/R3). The same cell already says the claim is stopped, so the label is the only overclaim left. | "Generic, config-driven pre-freeze replay gate proposed under QUALITY 67; it does **not** discharge QUALITY 67 — its registered set omits content-multiset memorization, which meets the target (`nameset.py`, 8/8 at three seeds), which is why R34-C2 is stopped" |
| C2 | 147-151 (same quote at `ScribeLesson.md:113`) | "…the committed replay gate refuses the shape-only counter whose label-keyed memorization meets its target, **clears the identity-defeating counter** on the same eight fixtures where every registered shortcut class stays below target…" | Correct as a verbatim quote of the frozen `PREDICATE` constant (that is the F4/F5 defect evidence), but unlabelled it re-publishes the success sentence in a document read at closure. | `(quoted as the frozen record's own pre-stop claim; false as of the stop — the green surface is not identity-defeating for the name multiset, and that is how R34-C2 stopped)` followed by the unchanged quote |

### 4.4 `w1/ScribeLesson.md` — `corpus/lessons/round-34.md` append (8 items)

| id | line | sentence that now overclaims | why it overclaims | corrected sentence |
|---|---|---|---|---|
| D1 | 53 | "Kill rule: any false clause is a miss and stops; no target, counter, predicate or label may be changed afterwards, and no shortcut class may be dropped to reach CLEAN." | States the clause-only rule and omits the rule the round actually applied: a target a control skipping the claimed work can reach is not an improvement (SR `kill_rule_applied`). As written, a reader concludes no stop was owed. | "Kill rule: any false clause is a miss and stops; … and no shortcut class may be dropped to reach CLEAN. The round also applied the frozen-before-data principle: a target a control that skips the claimed work can reach is not an improvement, so the claim stopped although all six clauses held on the frozen bytes." |
| D2 | 57 | "**Green surface (identity-defeating counter clears).** … observed `REPLAY_GATE_CLEAN …` exit 0, `green_positive_matched=8`" | "clears" + "identity-defeating" is the fabricated-success sentence of the lesson. The surface defeats label/size/digest/offset/order identity but not the name multiset (R4 vs R5). | "**Green surface (name-pool permutation; the seven registered classes stay below).** … observed `REPLAY_GATE_CLEAN …` exit 0, `green_positive_matched=8`. It defeats label, size, digest, fixed-offset and build-order identity but not the name multiset, so it does not show the counter forces record traversal." |
| D3 | draft-level (after 65) | The section ends at "**Scope held.**" with no verdict section: `## Claim R34-C2` presents frozen clauses and a green CLEAR and stops there. | Omission in a lesson whose other claims each carry a verdict section. A closure reads the R34-C2 block as a met claim; the landed replacement carries `## Claim R34-C2 — frozen clauses met, capability denied` and must keep it. | Append: `## Claim verdict — frozen clauses met, capability denied` — "All six frozen clauses held on the frozen bytes at `c79bbe7b` (exit 0, receipt `da78f444…`), and the claim still stopped: the green surface's only perturbation was name-pool reordering, so record count, record order, every `flags`/`value` byte and the name multiset survived it. An unregistered content-multiset reader (`w1/CtlMultiset-files/nameset.py`, sha256 `2e8feaea…`) reaches 8/8 without reading a header, a record entry or a `name_off`; registering it flips the same gate to REFUSED. Under §9 (a target a control that skips the claimed work can reach is not an improvement; r29-C1 precedent) this is a falsified measure / honest stop: no capability, coverage, depth or calibration credit; owned scores 10→10, delta 0." |
| D4 | 65 | "No depth/coverage/calibration score moves; the three owned proxies stay tied at 10." | True but now incomplete in the direction of credit: the sentence is the draft's only score statement and reads as a neutral no-change, not as a denied claim. | "No depth/coverage/calibration score moves; the three owned proxies stay tied at 10, and the claim itself is a falsified measure: no capability, coverage, depth or calibration credit is awarded." |
| D5 | 63 | "eight fixtures and **eight readers** pinned separately" | Factual undercount: the pin map carries nine reader files. `claims[0].pins` lists `all_false`, `digest_keyed`, `fixed_slice`, `label_keyed`, `label_replay_full`, `record_order_replay`, `size_keyed`, `string_scan`, `structural` = 9 (26 pins = 9 readers + 8 fixtures + 5 mini-fix + 2 configs + 2 scripts). | "eight fixtures and **nine** reader files pinned separately (the seven registered shortcut classes, the `structural` positive control, and the unregistered `label_keyed.py`)." |
| D6 | 67-75 (`## Mistakes`) | The table has no row for the class that stopped the claim; M34-6..M34-10 are author-side/limit defects only. | A lesson that records how the surface was built but not why it failed invites the next round to repeat it; the landed lesson carries M34-7 (green surface keys on invariants it did not vary) and that row must not be lost. | Append one row (prose if ids collide, see D7): "green surface varied layout, not the keyable invariants — `nameset.py` 8/8 at three seeds; `permute()` changes only pool order and `name_off`. Captured-by: nothing at freeze required the transformation to break every keyable invariant. Fix: stop the claim; route QUALITY 69 (one class per keyable invariant) and the fresh-content counter." |
| D7 | 67-75 (`## Mistakes` ids) | The draft numbers its five rows `M34-6` … `M34-10`. | Collision: the landed lesson uses `M34-5` … `M34-11` for entirely different defects (pins container, predicate triple, green surface, class drop, mutant/label, no-reader gate, unbound evidence). Landing the draft as written would give two meanings per id. | Do not land this table. Either append the five draft rows **unnumbered** as prose under the landed paragraph "Two author-side defects were caught by the instruments themselves…", or renumber from `M34-12`; the landed M34-5..M34-11 stand unchanged. |
| D8 | 125 | "the draft records the frozen surfaces and my reproduction and asserts **no** claim verdict and **no** score." | True of the seat's intent, but the draft body offers no verdict section, so the landing editor must supply one (D3) — otherwise the absence becomes a de-facto pass. | "the draft records the frozen surfaces and my reproduction and asserts no claim verdict and no score; because the body carries no verdict section, the landing editor must add the `## Claim verdict` block above and must not read the green CLEAR line as a pass." |

### 4.5 `w1/ScribeSourcesRow.md` — S106 row and Gate sentence (2 items)

| id | line | sentence that now overclaims | why it overclaims | corrected sentence |
|---|---|---|---|---|
| E1 | 115-117 | "Truncation in readelf is answered by stopping a chain and warning, never by emitting a plausible record — the exact inverse of the structure-blind shortcut readers the C2 gate scores." | "the C2 gate scores" implies the gate defeats those readers; it refused only its registered ones and CLEANed on the decisive unregistered class (R4/R5). | "Truncation in readelf is answered by stopping a chain and warning, never by emitting a plausible record — the inverse of the structure-blind shortcut classes the C2 gate registers (the gate itself was stopped: an unregistered content-multiset reader met its target)." |
| E2 | 137 | `used-by` cell: `corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` | That path holds a 0-byte untracked file (sha256 `e3b0c442…`, `wc -l` 0, 07:32:49Z); the landed entry is `…-r34b-…-stop.md` and the landed S106 row cites it. A `used-by` cell naming an empty file is a fabricated pointer. | `used-by` = `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` (as landed at `corpus/SOURCES.md:111`); if the drafted entry is never landed, cite the lesson row instead. |

**Inventory total: 9 + 13 + 2 + 8 + 2 = 34.**

---

## 5. Landed-text residuals (tracked docs at `66b84027`)

These are not draft sentences, so they are outside the assignment's five-document list, but they are
the same overclaim class and the L1 can still fix them cheaply. Severity is low because each is
surrounded by the stop.

**Concurrency note.** `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`
and `corpus/lessons/round-34.md` were being edited by the L1 while this audit ran (mtimes
07:30:02Z–07:33:09Z). The locations below were re-checked at 07:34:30Z against the current bytes —
`LOG.md` `2e552b42…`, `SCORECARD.md` `eb63cbfc…`, `corpus/lessons/round-34.md` `bd7b4145…`, landed
entry `0cb388bc…` — and both phrases are still present in all four documents named (the lesson's
wording is "makes", the others "making"). If the L1 has already amended them by the time this is
read, treat the row as closed rather than as a defect.

| id | location | text | why it is a residual overclaim | corrected sentence |
|---|---|---|---|---|
| L1 | `LOG.md:3097`; `SCORECARD.md:3353`; `corpus/lessons/round-34.md:43`; landed entry `:10` | "a pre-freeze structure-blind shortcut-replay gate **making/makes QUALITY 67 executable**" | QUALITY 67's purpose is to catch the structure-blind replay *before* a freeze. This gate did not: it CLEANed on an unregistered class and the claim froze. "Making … executable" is a capability notice in tracked docs (R4 vs R5 are the measured asymmetry). | "a pre-freeze structure-blind shortcut-replay gate operationalizing part of QUALITY 67; its registered class set was unfaithful, so the obligation was **not** discharged by it" |
| L2 | `LOG.md:3097`; `corpus/lessons/round-34.md:47`; landed entry `:24` | "…eight synthetic 512-byte `MREC` fixtures …, eight readers" | Under-count of the pinned inventory (nine reader files, §4 D5). Not a score claim, but an inventory claim a closure can falsify from `claims[0].pins`. | "… eight synthetic 512-byte `MREC` fixtures and nine reader files (eight scored classes plus the unregistered `label_keyed.py`)" |
| L3 | `<lane>/corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` | 0-byte untracked file at the draft's own proposed entry path | A closure that lists `corpus/knowledge/2026-10-25*` sees two round-34 entries: the landed `-stop` file and an empty one. The empty one is also the `used-by` target of the draft's SOURCES row (§4 E2). Nothing depends on it; it should not survive. | Delete the empty file, or (if the draft entry is landed after §4 A1-A8) rename it to the draft's path **and** repoint S106 — but the stop entry already covers the round, so deletion is the smaller move. |
| L4 | `SCORECARD.md:3353` | row label "R34-C2 / depth — capability acquisition: a pre-freeze … gate making QUALITY 67 executable" | Same phrase as L1 inside a table row; the verdict column is already correct, so only the label overclaims. | "R34-C2 / depth — attempted capability acquisition: a pre-freeze … gate aimed at QUALITY 67 (registered set unfaithful; claim stopped)" |

Facts I checked and found **correct** in the landed docs (so the L1 should not "fix" them): the
SCORECARD verdict cell and "No capability row enters"; the lesson heading "frozen clauses met,
capability denied"; the SKILL heading "(stopped capability)" and its limits line; the landed entry's
`status:` line and "Why the capability is denied"; S106's `used-by` cell. The landed docs' stronger
claims (five unregistered classes, ten warn-only paths) are the stop record's and the S106 seat's,
not mine to re-verify; see §7.

---

## 6. Landing gate — what may land, in what order

1. **`SCORECARD.md`** — land nothing from DRAFT A (B3). If anything from DRAFT B is wanted, use B1/B2
   /B6-B13 corrections, and land it as the stopped-claim subsection; the tracked section at
   `3347-3368` already satisfies this.
2. **`corpus/lessons/round-34.md`** — land nothing from the draft `## Mistakes` table as numbered rows
   (D7 collision) and nothing without the `## Claim verdict` block (D3). Details D1/D2/D4/D5/D6 may
   land as prose.
3. **`corpus/knowledge/…`** — the `-stop` entry is landed and carries the stop; A1-A8 are only needed
   if the draft entry is landed as a second file, which the round does not require. If it is, A5 and
   A3 are mandatory (they are the two epistemic sentences a closure would call fabricated success).
4. **`SKILL.md`** — C1 applies only if the draft rows are used; the landed section at `1209` does not
   use them and does not carry the `(QUALITY 67)` label.
5. **`corpus/SOURCES.md`** — the landed S106 row is correct; E2 applies only to the draft row.
6. **Custody** — L3 (empty file) before any knowledge listing is published.

---

## 7. Residual risk and verification gaps

- **Not re-run by me:** the five controls, the C2 six-clause counter, the gate `--selftest`, the
  red/green per-class matrix. They are cited from the stop record and w1 reports, not re-observed
  here; the corrected sentences therefore cite them as the stop's evidence, and only R2-R5 as mine.
- **Only one of the five unregistered classes was reproduced here** (content multiset). The stop
  record and the landed docs name four more (payload with names zeroed, value/offset, record
  signature, transform/digest identity leak). I did not run them; my corrections name the class I
  measured and attribute the rest to `claim-stop.json`. A closure that requires all five to be
  independently reproduced will not get that from this report.
- **S106 line claims** (line numbers, "ten warn-only failure paths", `DT_STRTAB` route) are the
  ScribeSourcesRow / ScoutReadelfSource seats' and are not audited here.
- **`mini-counter-fresh.py`** (the "repair route") was not read or run; the corrected sentences
  reference it only as next-round routing under QUALITY 69/70, matching the landed entry's own
  "not a claim" label.
- **Report-body sentences** in the five drafts (not the landing blocks) also carry the same
  overclaims: `ScribeScorecardRow.md:11` ("None of the six frozen clauses is affected; both are
  draft-disclosure material, not claim changes"), `:121` (the B10 sentence in the body), `:250`
  (verdict `SCORECARD_DRAFTS_READY` naming a capability row), and `ScribeSkillRegistry.md:183-186`
  (F11, which is consistent with its verdict line "eleven findings (F1–F11)" at `:222-223` — no
  inconsistency, recorded so the next reader does not re-raise it). They were not landed and should
  not be quoted into docs; I list them so a future citation does not resurrect them.
- **Unrun by contract:** no build, lint or bulk suite; no ELF carrier or fixture executed; no
  `pacman`; no VCS mutation. An unrun check above is marked unrun, not passed.

---

## 8. Artifacts

Lane (my only lane write):
- this report —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/w2/ADocsOverclaim.md`

Scratch (`/fast/scratch/hyaku/kaidoku-r34b/w2/ADocsOverclaim/`):
- `root/tools/round-34/` — `cp -a` copy of the frozen tree (hashes re-checked at R1)
- `nameset.py` (`2e8feaea…`), `root/tools/round-34/mini-fix/readers/nameset.py` (copy for R5)
- `cfg-plus-multiset.json` — green config + `content-multiset` class
- `receipts/nameset-green-{kaidoku-r34-mini-v1,alt-1}.{json,err}` — R2/R3
- `receipts/gate-green.json` — R4 (CLEAN, exit 0)
- `receipts/gate-plus.json` — R5 (REFUSED, exit 2)

Inputs read, never written: the five `w1/Scribe*.md` drafts, `claims.json`, `claim-stop.json`,
`SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-34.md`,
`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`, the empty
`corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md`, `corpus/QUALITY.md:77`,
`tools/round-34/**`.

---

**Verdict: `OVERCLAIMS_ENUMERATED` — 34 sentences across the five unlanded wave-1 drafts would
overclaim after the R34-C2 stop (ScribeKnowledgeEntry 9, ScribeScorecardRow 13,
ScribeSkillRegistry 2, ScribeLesson 8, ScribeSourcesRow 2); each has a corrected sentence grounded
in `claim-stop.json` and, for the decisive class, in my own reproduction (`nameset.py` 8/8 at
`kaidoku-r34-mini-v1` and `alt-1`, 2026-10-25T07:29:29Z; gate CLEAN with the class unregistered,
REFUSED once registered, 07:29:35Z). The tracked docs landed at `66b84027` already carry the stop and
use none of the draft blocks; 4 landed-text residuals and one 0-byte untracked file at the draft's
own proposed entry path are flagged for the L1. No lane doc, instrument, claim or stop record was
edited, and no score or claim verdict is awarded here.**
