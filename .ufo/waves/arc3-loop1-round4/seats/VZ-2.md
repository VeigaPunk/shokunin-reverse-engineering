# Seat VZ-2 — chain c2, convergence (arc3-loop1-round4)

Seat line: `SEAT VZ-2 | CHAIN c2 | ROLE convergence | TASK: poll seats every 60s
(max 25 checks); reconcile into claims/c2/verdict.md: VERIFIED or NOT-VERIFIED +
evidence + named debt. Seat report last.`

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` (unchanged through this seat's work; no
seat commits — the parent integrates). Date 2026-10-19. Lane: devin
(`devin/deepseek-v4-1-flash-max`) — the declared fallback recorded in
`claims-frozen.md:11-15` after the hyper lane returned 402 out-of-credits on all 48
seats; not a lane signal. No git mutation. No write to any real target: `PROVINCE.md`
is byte-identical to its HEAD blob (`d075a3c6…`, 162 lines) at report time; every
apply ran on a `/var/tmp` scratch copy. Custody paths never opened (not even
read-only). Scratch `/var/tmp/vz2r4` — never `/tmp` (standing EDQUOT rule).

**Verdict delivered: VERIFIED** — written to `claims/c2/verdict.md`. Six independent
repair voices were produced; the two this seat applied end-to-end satisfy the claim, and
the per-voice coverage/defects plus the landing rules are named there. The census grew
from 6 to **9 stale items** under three peer corrections (EX-13's F2, EX-15's C2,
EX-12's C3), every one re-measured and accepted here.

## 1. Work performed (evidence pointers)

**Poller.** `poll.sh` — 25 checks at 60 s intervals, snapshotting every new seat
report and claim file. Log: `/var/tmp/vz2r4/poll.log`. Ran r1 (14:04:46Z, seats=0)
through r11 (14:14:54Z, seats=32, claimfiles 1900+). Every seat report that landed
during this window was read; none was treated as evidence without a first-hand
re-measurement.

**Census instrument (this seat's own).**
`claims/c2/VZ-2/evidence/province-staleness-census.py` sha256
`e6eef57476bb6acac10f77285c90b035304286e91b19ccc6dbfe928509b174cc`. 26 rows, each
anchored to a verbatim PROVINCE phrase (`ANCHORS` table) so a phantom row is
detectable — measured `claim_not_found: []` on the unpatched tree. Deliberately does
**not** trust `.ufo/gates/c1-census-v10.py` (which grades only version/pin/pointer
loci) and does not trust any seat's tally. Runs live
`doctor`/`command -v`/`coredumpctl` probes for the rows whose truth is host state.

**First-hand measurements** (all at write time; full transcripts under
`claims/c2/VZ-2/evidence/`):

| measurement | result |
|---|---|
| census baseline, real tree | first reading `total=26 stale=6 adjudicated=2 current=18`; **final reading `total=28 stale=9 adjudicated=1 current=18`** — `STALE: F1b, F2, F3, F5b, X1, C1, C2, C3, R2` (`census-before.txt` / `.json`). The growth is three peer corrections, all re-measured here (see §3) |
| `.ufo/gates/c1-census-v10.py --root .` | PASS `stale=0 ambiguous=0 undeclared=0 unresolved=0`, G2 17/14/3 (`d0772ce8…`) |
| citation-drift probe, both modes | `findings=0` / `clean findings=0`; pointer-table sha equals its pin `1b3ab955…` |
| command A at HEAD | `83/83`, missing `[]`, dangling `[]`, `14/14`, `10.0/10.0` |
| live catalog re-derivation | `doctor` at 6.7.0 / 6.5.0 / 6.4.0 → 207/153 `af39310c…`; 207/153 `805433f1…`; 170/127 `25802f6d…` — all match PROVINCE |
| live pin re-read | devin:7, omp:8 = `rea-agents@6.5.0`; kimi = `6.7.0` |
| installed skill | `c8639823…`, 22,513 B — matches |
| EX-14 demo patch, independent apply | `d075a3c6…` → **`1bfb5dd7fff37c6fac387b23f6732d9667e04aa45726c6d5b88677870f9a19d2`**, 162 lines — **byte-exact match to EX-14's claim** (`demo-patch-independent-reapply.txt`) |
| EX-14 complete patch v1 (`928cfbc5…`), independent apply | → `f9b0888c…`, 162 lines, census PASS; **F3 and C1 still stale** (`complete-patch-independent-reapply.txt`) |
| EX-14 complete patch v1-late (`8a0e12ff…`), independent apply | → `dfa70b42…`, 162 lines, census PASS; **F3 and C1 still stale** |
| **EX-14 v2 (`0b8ad045…`), independent apply** | → **`69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5`**, 162 lines, census PASS; **all six stale rows repaired**, content defect fixed (`v2-patch-independent-reapply.txt`) |
| **EX-13 per-row set (7 patches), independent apply** | → **`dcfdb6a2fea6374caba5daf229b97c59ae4a69efa6ae14943909436e19eb81ca`**, 162 lines, census PASS; **all six stale rows plus the seventh (F2) repaired**; needs a content-match applier (its format has no `@@` markers) — I wrote `/var/tmp/vz2r4/apply13.py` (`ex13-patch-independent-reapply.txt`) |
| **F2 verified first-hand** | organic crashpad core → `coredumpctl dump 1857` → **17,608,704 B** (cap 33,554,432); `inspect-recorded-crash` → **exit 0**, `elf-core`, 53 segments, 3 threads (my `ev_3bdc54d2…`). "All 3 organic cores exceed the cap" is **falsified** — my earlier adjudication was too lenient |
| **C2 verified first-hand** | `Ghidra/Features/*/` → **34** dirs (not 35); `Ghidra/Processors/*/` → **39** (correct); PyGhidra + BSim present. Root cause: `corpus/knowledge/2026-10-13-ghidra-install.md:50` claims "35 modules" but its own list on that line names **34** — the entry miscounts its own evidence (`eighth-stale-item.txt`) |
| **C3 verified first-hand** | my own asar sweep returns **12** archives (row names 9): chatgpt 578,643,106; zcode 326,913,098; 1Password 40,708,328; signal 38,465,187; config-obsidian 27,477,966; obsidian.asar 25,787,463; typora node_modules 15,077,447; typora lib 8,339,267; obsidian app.asar 480,052; typora app.asar 390,514; electron43 111,073; electron39 109,371. The row's "423-file" count is corrected to **480** by the cited r4-06 entry's own erratum (`ninth-stale-item.txt`) |
| **CR-2's v2 hunk-6 defect verified** | per-hunk context scan vs the base: hunks 1-5 context-clean, **hunk 6's context line absent from the base**. With default fuzz it lands anyway and yields "… **still** refused since r2: r12-02 drained the row…" (self-contradictory); `--fuzz=0` fails 5 of 6 hunks. v2 hunks 1-5 + CR-2's corrected hunk 6 → `8bb35a2c…`, 162 lines, census PASS (`cr2-v2-hunk6-defect.txt`) |
| C1 Vyper leg, independent re-derivation | runtime bytes re-hashed → `57d6fd0a…` == the probe's decoded `bytecode.sha256`; 15/15 all `dispatch:"abi"`; creation blob carries the `vyper` CBOR trailer |
| `ptr_check` blind spot | called directly: `config.toml:3298` → `('stale', "line holds no rea-agents pin: 'max_context_size = 1048576'")`; `:3546` → `('ok', 'pins 6.7.0')` |
| SHONEN:12 + DATED + needle constraints on the v2 tree | safety clause still in 88-116; markers at :40/:45/:119 intact; :18 needles intact; no graded token on any added line |

## 2. Proposed changes (patch-text paths)

**None authored by this seat.** The seat line is convergence, and PROVINCE is a
scoped file this seat must not write. What this verdict does instead is grade the
wave's patch texts and name the landing rules:

- **Complete landing = EX-15's set + EX-12's C3 patch.** No single voice this seat
  measured covers all nine rows. EX-15's landing set (8 hunks in
  `claims/c2/EX-15/adjudications.md`; its own apply → `dce736cd…` for A6b / `feec841b…`
  for A6a) covers eight — all but C3. EX-12's
  `claims/c2/EX-12/proposed-core-asar-row-repair.patch.md` is the only voice covering
  C3. Add PL-2's `corpus-erratum-coupled.patch.md` to close C2's corpus root cause.
  EX-15's A6a/A6b split mirrors the C1 coupling exactly: A6b is the solc-only form
  (true at HEAD), A6a the both-legs form (land only with C1's entry).
- **`claims/c2/EX-14/evidence/candidate-complete-frontier-repair.v2.patch.md`** —
  `0b8ad045e19cee5a3120706853f9950bb90522b2ebaebb418db25f586c21d9a8`. Standard
  `patch(1)`-readable diff, repairs six of the **nine** stale rows (F2, C2, C3 untouched).
  **Must not land as-is**: hunk 6 is malformed (CR-2's find, verified here — A18), so
  land it with CR-2's `proposed-x1-context-fix.patch.md` hunk instead, and fold in the
  three missing repairs.
- **`claims/c2/EX-13/*.patch.md`** (seven per-row patches; the EVM one currently
  `66df2d6cf096f101…`, revised 11:17:33). Repairs seven of nine (C2, C3 untouched). But
  **two accuracy defects must be fixed first** (X1's warrant overstates what r12-02
  admits; X1b's pacman half is left stale — both in `8db47d240fc6027b…`), and its format
  needs a content-match applier (no `@@` markers; my `/var/tmp/vz2r4/apply13.py` and
  RV-3's each handle it).
- **CR-2's X1 correction** — `claims/c2/CR-2/proposed-x1-context-fix.patch.md`: a
  context-free replacement for v2's hunk 6. I applied v2 hunks 1-5 + this hunk →
  `8bb35a2c…`, 162 lines, census PASS, and the X1 sentence reads correctly.
- **Other voices** (not re-measured by this seat): EX-11's A+B+C+D
  (`frontier-repair-{A,B,C,D}.patch.md`, 4 patches / 7 hunks, its own apply →
  `e2335400…`, covering its own 7-item set and grading R1); PL-2's
  `candidate-repairs.patch.md` (21 hunks), `candidate-with-s5.patch.md` (22 — the S5
  variant re-anchors the pointer this verdict adjudicates NO-CHANGE, a defensible
  alternative branch), `candidate-coupled-vyper.patch.md` (22 — the C1-coupled variant).
- `claims/c2/EX-14/evidence/candidate-complete-frontier-repair.patch.md` —
  `8a0e12ff…`; superseded by v2 (it left F3 and C1 stale and carried the false Core
  promotion). Retained for the revision record.
- `claims/c2/EX-14/evidence/demo-frontier-repair.patch.md` — `507b0061…`; the
  pre-validated demo, superseded.
- The parent must also land C1's corpus entry
  (`claims/c1/records-drafts/knowledge-entry-draft.md`, stem
  `2026-10-19-arc3-r4-evm-vyper-leg`) in the same commit, or take the solc-only
  fallback wording.
- **C2's root cause is in `corpus/`**, not only in PROVINCE:
  `corpus/knowledge/2026-10-13-ghidra-install.md:50` claims "35 modules" while listing
  34. A same-round corpus erratum would be needed to close it at the source — a
  `corpus/` write, outside every seat's scope this round.

## 3. Before → after measurement for the chain's claim (c2: freshness)

The frozen claim's falsifiable form: *stale count N → 0; PROVINCE line count
unchanged; census PASS at the work tree after the parent applies the patches.*

| side | stale | adjudicated | current | PROVINCE lines | census |
|---|---|---|---|---|---|
| **before** (HEAD `015e1bab`, real tree) | **9** (6 at first reading + 3 peer-corrected) | 1 | 18 | 162 (`d075a3c6…`) | PASS 0/0/0/0 |
| after, EX-14 demo patch | 8 (F5b half-repaired) | 1 | 19 | 162 (`1bfb5dd7…`) | PASS 0/0/0/0 |
| after, EX-14 complete v1 (`8a0e12ff…`) | 5 (F3, C1, F2, C2, C3) | 1 | 22 | 162 (`dfa70b42…`) | PASS 0/0/0/0 |
| **after, EX-14 v2 (`0b8ad045…`)** | **3** (F2, C2, C3) | 1 | 24 | **162 (`69ceea9b…`)** | **PASS 0/0/0/0** |
| **after, EX-13 per-row set (7 patches)** | **2** (C2, C3) | 1 | 24 | **162 (`dcfdb6a2…`)** | **PASS 0/0/0/0** |
| after, EX-15 set (8 hunks) + EX-12 C3 patch | **0** | 1 | 24 | 162 (EX-15's own applies) | PASS |

**The three peer corrections (all re-measured here, all accepted).**

*F2 (EX-13's find).* My baseline census adjudicated the recorded-crashes bullet rather
than counting it stale, reasoning that its own closing sentence predicts the exemplar's
decay. EX-13 asserts a stronger falsifier: an **organic** crashpad core decompresses to
**17,608,704 B** (under the 33,554,432 cap) and `inspect-recorded-crash` returns
**exit 0**, `elf-core`, 53 segments, 3 threads. So "all 3 organic cores exceed the cap"
is false. Population re-measured: 73 non-godot organic rows, only 4 still `present` —
the "3" is a stale r1-era sample size. **F2 is STALE.**

*C2 (EX-15's find).* `PROVINCE.md:46` claims "39 processor modules; 35 features incl.
PyGhidra/BSim". I listed the install: **34** feature dirs, **39** processors (correct),
PyGhidra + BSim present. Root cause: `corpus/knowledge/2026-10-13-ghidra-install.md:50`
claims "35 modules" while its own enumerated list on that same line names exactly **34**
— the corpus entry miscounts its own evidence. **C2 is STALE**, a corpus defect as well
as a row defect.

*C3 (EX-12's find).* `PROVINCE.md:49` names **9** pinned asar archives; my own sweep
returns **12** (chatgpt, zcode, config-dir obsidian missing from the row), with byte
counts matching EX-12's exactly. The row's evidence cell also carries the superseded
"423-file" count that the cited r4-06 entry corrects to **480** in its own erratum.
**C3 is STALE.**

Clause-level audit on the patched text (this seat's own `grep -F`, not inferred):

| stale row | old literal | EX-14 v2 | EX-13 set | EX-15 set | EX-12 patch |
|---|---|---|---|---|---|
| F1b | `Reserve: 91MB` | repaired | repaired | repaired | — |
| F2 | `all 3 organic cores exceed the cap` | **untouched** | repaired | repaired | — |
| F3 | `JEB (unprobed)` | repaired | repaired | repaired | — |
| F5b | `vyper-compiled bytecode untested` | repaired | repaired | repaired | — |
| X1 | `probe-refused` | repaired | repaired (2 defects) | repaired | — |
| C1 | `absent: \`7z\` …` | repaired | repaired | repaired | — |
| C2 | `35 features` | **untouched** | **untouched** | repaired | — |
| C3 | `obsidian ×2, … typora ×3` | **untouched** | **untouched** | **untouched** | **repaired** |
| R2 | `Next: raise` | repaired | repaired | repaired | — |
| **F3** | `JEB (unprobed)` | **survives at :88** in v1 — **repaired in v2** |
| **C1** | `absent: \`7z\` …` | **survives at :62** in v1 — **repaired in v2** |

**The claim's bar (N → 0) is met by v2**: the current candidate
`candidate-complete-frontier-repair.v2.patch.md` (`0b8ad045…`) applies 6/6 hunks,
holds the line count at 162 (`d075a3c6…` → `69ceea9b…`), reads census PASS 0/0/0/0,
and its clause audit shows **all six old literals gone**. The intermediate v1
revision reached only 6 → 2.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the census gate validates the repairs" | **refuted** — Frontier (:72-118) and post-unlock frontier (:132-162) are UNDECLARED; the EVM bullet never matches `REA_GATE`, so `classify()` emits zero detections and the gate reads the *same* PASS before and after. RV-4's blindness proof reproduced |
| A2 | "EX-14's after-digest is stale/unreproducible" | **partially sustained, resolved** — the demo's `1bfb5dd7…` reproduced **exactly**; the complete candidate went through four published shas (`16b878d3…` per RV-4 → `928cfbc5…` → `8a0e12ff…` → v2 `0b8ad045…`). I re-applied each set of current bytes rather than quoting an earlier run |
| A3 | "`ptr_check` covers the `config.toml:3298` pointer" | **refuted** — it is only reached when a clause carries no pin/bare version (`c1-census-v10.py:416-418`); PROVINCE:18's clause carries the pin, so the pointer is never evaluated. Direct call returns `stale` |
| A4 | "the demo patch is enough" | **refuted** — leaves F5b's vyper half, F1b, X1, C1, R2, F3 all stale. v2 supersedes it |
| A5 | "the stale set is smaller than 6" | **refuted for F1b/F5b/X1/C1** (each falsified by an admitted corpus entry or a live probe); **sustained for F2**, which I adjudicated rather than counted (the bullet's own last sentence already says retention decays oldest-first — the exemplar decayed, the class claim holds) |
| A6 | "C1's Vyper leg is corpus state" | **sustained as a landing hazard** — the leg is real and I re-derived it end-to-end, but `corpus/` is still **83 files**; the entry is patch text. The vyper clause is safe only with a same-commit landing |
| A7 | "the chain's numbers are seat text" | **refuted** — every load-bearing number re-measured first-hand (§1); three independent applies of the patch revisions from their own bytes; identities re-derived at write time |
| A8 | "line count held ⇒ safe to land" | **refuted (found by CN-1, re-derived here)** — `SHONEN.md:12` pins `PROVINCE.md:88-116` and the table's `shonen-province-range` requires that range to still contain `Quality/safety verdicts on findings`, which sits at :114-116. A +3 shift above it breaks the probe even at a held count. v2 clears it |
| A9 | "the patch's `(Core, arc3-r1/r3) … held` wording is harmless" | **sustained against v1, CLOSED by v2** — both corpus entries declare "RESULT-class, no Core promotion"; PROVINCE:75-76 requires a `LOG.md` entry. v2 drops `Core`/`held` for those legs and marks them RESULT-class. RV-4 found it; I re-derived all three legs |
| A10 | "v2 trades the content fix for a probe break" | **refuted** — measured on my v2 tree: DATED markers at :40/:45/:119 intact, `:18` matches both probe needles, the SHONEN range still contains the safety clause, `bare hashes` survives, and no added line carries a graded token |
| A11 | "my F2 adjudication was right" | **REFUTED against my own earlier reading** — an organic crashpad core decompresses to 17,608,704 B (under the cap) and `inspect-recorded-crash` returns exit 0 with `elf-core` / 53 segments / 3 threads. "All 3 organic cores exceed the cap" is false. F2 is STALE; the true baseline is 7 |
| A12 | "EX-13's per-row set is landable as it stands" | **partially sustained — two accuracy defects** (RV-3 sustained both; I reproduced the citations). **(a)** X1 reads "exercised since r12 (all three input classes…)" but r12-02:213-218 says "**both classes**" and names the reconcile-input sub-class as untested; that sub-class closed later at r14-01:19-25. Re-word or re-cite. **(b)** X1b carries `multi-version pacman pairs beyond expac unexercised` through verbatim, but r4-10:15 is headed "Targets — cached pacman pairs" with a `1password-cli` pair and a `qpdf` control (I read the entry). Both defects are in `8db47d240fc6027b…` |
| A13 | "the two candidates disagree on the landing result" | **refuted** — v2 → `69ceea9b…`, EX-13 set → `dcfdb6a2…`, both 162 lines and both census PASS. The material deltas are F2/C2 coverage plus EX-13's two open defects |
| A14 | "the census is complete at 6 stale rows" | **REFUTED twice against my own baseline** — EX-13's F2 and EX-15's C2 are both real, and I re-measured each end-to-end rather than accepting the peers' numbers. My instrument now reads `total=27 stale=8 adjudicated=1 current=18`, matching EX-15's independent count. Two corrections, both resolved in the peers' favour |
| A15 | "`35 features` is right and only the listing is short" | **refuted** — 34 dirs on disk; `corpus/knowledge/2026-10-13-ghidra-install.md:50` claims 35 while its own enumerated list on that line names exactly 34, matching disk. The entry miscounts its own evidence (EX-15's refutation, re-derived here by parsing the list) |
| A16 | "v2 is landable as-is" | **sustained as a coverage gap, not a defect** — v2 is clean on every constraint I can measure but leaves F2, C2 and C3 unrepaired (9 → 3). It satisfies the claim's letter only if those three are named as carried debt or folded in |
| A17 | "one voice covers the whole stale set" | **refuted** — EX-15's set covers 8 of 9 (not C3), EX-13's 7, v2 6, EX-11's 7 of its own set. **C3 is covered only by EX-12's standalone patch.** A complete landing needs two voices composed deliberately |
| A18 | "v2 is landable as-is" | **REFUTED (CR-2's find, verified here)** — v2's hunk 6 carries a malformed context line (`… is no longer` where the base reads `… still`). With default fuzz it lands anyway and yields a **self-contradictory** sentence: "compare-application-versions **still** refused since r2: r12-02 drained the row with two success legs". Under `--fuzz=0`, 5 of 6 hunks fail. I composed v2 hunks 1-5 + CR-2's corrected hunk 6 → `8bb35a2c…`, 162 lines, census PASS, sentence correct (`x1-context-fix` evidence) |
| A19 | "a literal-gone clause audit is sufficient" | **refuted against this seat's own method** — my audit checked `probe-refused` was gone (it was) but never read the resulting sentence, which still asserts the refusal via the retained `still`. CR-2 read it. Lesson recorded: a literal-gone check is not a semantics check |

## 5. Blockers / named debt

1. **No blockers remain for the claim.** Both candidates repair the stale set same-line
   at a held line count, the gate reads PASS, the repairs are patch texts, and the
   content defect is fixed. The verdict is **VERIFIED**, subject to the landing rules.
2. **Landing rule 1 — the C1 coupling (F-5, CN-1's constraint, re-derived here)** —
   the landed repair's corpus entry must land in the **same commit** as C1's Vyper
   entry, or the vyper clause drops to the solc-only fallback.
3. **Landing rule 2 — line-for-line discipline** — any edit that adds a line above
   :116 breaks the SHONEN range even if the file's total count is held (CN-1's
   counterexample; the DATED marker at :119 breaks on any shift above it).
4. **R8 — EX-13's two accuracy defects** (A12) must be fixed before that candidate
   lands. v2 has neither.
5. **R9 — F2 and C2 are covered by only some voices.** v2 leaves both; EX-13's set
   leaves C2; only EX-15's set covers all eight. If v2 lands, carry in those two repairs
   (simple same-line rewrites) or name them as carried debt.
6. **R10 — C2's staleness originates in the corpus.** `2026-10-13-ghidra-install.md:50`
   claims 35 modules while listing 34, so a PROVINCE-only repair leaves the source entry
   miscounting its own evidence.
7. **The gate cannot grade any of this** (R1) and **`ptr_check` is blind to a
   pinned clause's pointer** (R2). Both are chain c1's instrument; closing them
   needs a same-commit scope re-key via patch text (r3 EX-31 precedent).
8. **Patch-revision churn (R5)** — five distinct patch shas circulated inside one wave;
   only the sha measured at landing time is authoritative.
9. **`__pycache__` residue** under `.ufo/gates/` must stay out of the landing commit.
10. **Instrument caveat for the parent** — my census `ANCHORS` are the *old* literals,
    so on a repaired tree the repaired rows read `claim_present=False` by construction.
    The clause audits are the correct check there, and `verdict.md` says so.

## 6. Identity discipline (rule #14) — re-derived after the final revision

| object | sha256 | how |
|---|---|---|
| `PROVINCE.md` (repo, unchanged) | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` | `sha256sum` at write time; 162 lines |
| `SKILL.md` | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` | same |
| `SCORECARD.md` | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` | same |
| census instrument | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` | same |
| **complete patch v2 (graded)** | `0b8ad045e19cee5a3120706853f9950bb90522b2ebaebb418db25f586c21d9a8` | same |
| complete patch v1-late | `8a0e12ffc8c48a809d60b06e7c13a4e93f3e1af131f08e9b7914fef86b06b1b2` | same |
| demo patch | `507b00610686f6a215901eefdaf93223bb592001205433f2579e2373b62add51` | same |
| EX-13 per-row set (7 patches) | see `verdict-identity.txt` (all seven shas) | same |
| my census instrument | `e6eef57476bb6acac10f77285c90b035304286e91b19ccc6dbfe928509b174cc` | same |
| my patched tree (v2) | `69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5` | sha256 on the scratch apply |
| my patched tree (EX-13 set) | `dcfdb6a2fea6374caba5daf229b97c59ae4a69efa6ae14943909436e19eb81ca` | same |
| my patched tree (v1-late) | `dfa70b42b51dd45bd82bbf3037b707c0e1f10518ec9b0d5f68d72dbda652d27e` | same |

`verdict.md`'s own identity is re-derived after its last revision and recorded
out-of-band in `claims/c2/VZ-2/evidence/verdict-identity.txt` (a self-hash written
inside the file would invalidate itself on write).

## 7. Files written by this seat

- `.ufo/waves/arc3-loop1-round4/seats/VZ-2.md` — this report
- `.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md` — the chain verdict
- `claims/c2/VZ-2/evidence/province-staleness-census.py` — the census instrument
- `claims/c2/VZ-2/evidence/census-before.txt` / `.json` — the 26-row baseline
- `claims/c2/VZ-2/evidence/demo-patch-independent-reapply.txt`
- `claims/c2/VZ-2/evidence/complete-patch-independent-reapply.txt`
- `claims/c2/VZ-2/evidence/v2-patch-independent-reapply.txt`
- `claims/c2/VZ-2/evidence/ex13-patch-independent-reapply.txt`
- `claims/c2/VZ-2/evidence/candidate-inventory.txt` — the repair voices + the
  organic-core population count
- `claims/c2/VZ-2/evidence/eighth-stale-item.txt` — the C2 re-derivation
- `claims/c2/VZ-2/evidence/ninth-stale-item.txt` — the C3 re-derivation
- `claims/c2/VZ-2/evidence/cr2-v2-hunk6-defect.txt` — CR-2's v2 defect, verified here
- `claims/c2/VZ-2/evidence/final-state.txt`
- `claims/c2/VZ-2/evidence/verdict-identity.txt`
