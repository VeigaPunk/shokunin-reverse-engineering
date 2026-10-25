# ScoutSiblings — kaidoku round 34 (r34b re-dispatch, wave 1)

Scope: read-only scan of the newest fleet reports (`/home/vgpnk/Projects/shokunin/.ufo/reports/`) and the sibling lane repos for work the frozen **R34-C2 pre-freeze shortcut-replay gate** might duplicate. No lane file written except this report; no VCS mutation; no ELF carrier, fixture or reader executed; no network; no tool installed (§ "Tooling" below). Inheritance honoured: R34-C1 (GNU version-needs) and its twelve carriers were **not** executed, re-scored or relabelled.

## Method and receipts

Receipt file (absolute): `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutSiblings/receipts.txt`.
Raw family sweep: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutSiblings/family-grep.txt` (1 639 lines, includes the `date -u` stamp and `EXIT=`).

| # | 2026-10-25 UTC | command (abbreviated) | exit |
|---|---|---|---|
| R1 | 07:21:49Z | `grep -rIl -E 'structure[- ]blind\|shortcut[- ]replay\|replay[- ]gate\|label[- ]keyed\|fixture[- ]label[- ]shortcut\|fixture[- ]literal\|pre[- ]freeze' --include=*.md --include=*.py --include=*.json --include=*.sh */` over the fleet root, `kaidoku-shokunin/` excluded | 0, **1636 files** |
| R2 | 07:22:16Z | `grep -rn -iE 'tsukuroi-shokunin\|chousa-shokunin\|kama-shokunin\|mado-shokunin\|tameshi-shokunin\|kake-shokunin'` over `kaidoku-shokunin/` (`.git` excluded) | 0, **1822 lines** — 1818 under `.ufo/waves` (legacy luna-run scans, not this round), 4 in `EXAMPLE.kama.md`; `SKILL.md`/`PROVINCE.md`/`corpus/QUALITY.md` = **0** |
| R3 | 07:22:16Z | same name grep restricted to `.ufo/waves/round-34/r34b/` | 0, **0 files** |
| R4 | 07:22:16Z | `git -C kaidoku-shokunin log -1 -S 'structure-blind replay' -- corpus/QUALITY.md` | 0 → `abbd7604 2026-10-23T08:07:18-03:00` |
| R5 | 07:22:16Z | `git -C kake-shokunin log -1 -S 'lookup-table control' -- corpus/QUALITY.md` | 0 → `24a1647 2026-10-22T18:18:49-03:00` |
| R6 | 07:22:16Z | `git -C kake-shokunin log -1 -- .ufo/waves/round-34/criteria/lookup_control_check.py` | 0 → `76fac3b 2026-10-22T18:31:28-03:00` |
| R7 | 07:22:16Z | `stat -c '%y %n' chousa-shokunin/considerthese/2026-10-23.md chousa-shokunin/corpus/lessons/round-42.md tsukuroi-shokunin/corpus/lessons/round-35.md` | 0 → note `2026-10-23 09:23:59 -03`, chousa lesson `2026-10-24 21:14:27 -03`, tsukuroi lesson `2026-10-23 09:25:57 -03` |
| R8 | 07:22:16Z | `ls mado-shokunin/.ufo/waves/round-24/controls/ \| wc -l` | 0 → 22 control artifacts |
| R9 | 07:22:16Z | `grep -rIl -iE 'shortcut' .ufo/reports --include=*.md \| wc -l` | 0 → 44 report files, rounds 1–108 |

Anchors used for ordering: R34-C2 freeze `c79bbe7b0959132b9873ff3431cf5eb313b58b33` = `2026-10-25T04:13:11-03:00` (`2026-10-25T07:13Z`); kaidoku's R34 stop commit `abbd7604` = `2026-10-23T11:07Z`; kake's rule `24a1647` = `2026-10-22T21:18Z`; kake's instrument `76fac3b` = `2026-10-22T21:31Z`.

**Method limit (stated, not concealed).** Every object here is prose, JSON config or Python tool text in sibling trees; no language server is mounted for them, so no `lsp` definition/reference answer exists to trace. All findings are text-grep observations plus `git log`/`stat` ordering — literal evidence, never presented as semantic proof. Working trees were swept; **git history was not exhaustively searched**, so an earlier, since-deleted sibling instance of this gate would not appear (see Limits).

## 1. The overlap family, as measured

Eight sibling lanes plus kaidoku independently record the same failure shape: *a frozen counter gives full marks to a control that does none of the claimed work.* The family is older and wider than this round:

| Lane | Evidence path:line | Shape it caught |
|---|---|---|
| kake | `.ufo/waves/round-34/criteria/lookup_control_check.py:1-22`; `corpus/QUALITY.md:658-675`; `corpus/lessons/round-34.md:68`; `.ufo/reports/round-34/kake.md:39-42` | lookup-table tool `dcef39b5` scored 28/28 on C1, transcription commit `0cce15f0` 5/5 on C2 |
| kaidoku | `SCORECARD.md:3345`; `corpus/QUALITY.md:77` (row 67); `.ufo/reports/round-34/kaidoku.md:9-16` | size/fixed-slice replay met the C1 Verneed counter 12/12 |
| tsukuroi | `corpus/lessons/round-33.md:42` (R33-FIXTURE-LABEL-SHORTCUT); `corpus/lessons/round-35.md:36,42,44` (R35-V1-ROLE-LENGTH, R35-V2-FORCED-SHAPE-CONSTANTS); `.ufo/reports/round-35/tsukuroi.md:13` | repair counter 24/24 by fixed label; census VERSION 1 24/24 by name length; VERSION 2 24/24 by forced fixture shapes |
| chousa | `corpus/QUALITY.md:526-540` (row 60); `corpus/lessons/round-29.md:28`; `corpus/lessons/round-33.md:81,108`; `.ufo/waves/round-29/controls/CtlLabelKeyed/report.md:1,3,97,161` | label-keyed quote replay 82/82 without fetching; fixture-literal mask 156/156 |
| mado | `.ufo/reports/round-24/mado.md:28-30`; `.ufo/reports/round-25/mado.md:9-13` | `CtlC1LabelShortcut` met counter v1; ten shortcut shapes scored under v4 before data |
| kama | `corpus/lessons/round-26.md:78`; `corpus/lessons/round-28.md:48,123`; `corpus/lessons/round-34.md:89-91,107` | all-false control 12/14 pre-data; generic type conversions credited; frontier: a fleet shortcut-class ledger |
| mori | `.ufo/reports/round-34/mori.md:13,27-30`; `.ufo/waves/round-31/controls/shortcut1-grep-list-lines.sh`, `shortcut2-canned-ids.sh` | skip programs give `C1=met`; content-free prose meets a calibration counter |
| tameshi | `.ufo/reports/round-34/tameshi.md:17-22` | frozen set-blind witness rule "voidable in both directions" |
| kotoba | `.ufo/waves/round-55/controls/C1-shortcut.txt:1`; `corpus/lessons/round-55-verifier-spotcheck.md:64,83-85,134` | fabricated table/entry/SOURCES/Gate quotes; C2 reachable by exit remap, entry preflight, argparse shadow |

## 2. Substantive overlaps and dispositions

Dispositions: **cite** = kaidoku may name it as prior art without importing the surface; **adjacent** = same family, different object or contested scope — report, do not absorb; **reject** = same words, different object.

### 2.1 kake — nearest instrument (cite; earliest committed instance)

- `.ufo/waves/round-34/criteria/lookup_control_check.py:2-20`: "a counter must score a lookup-table control below its full score … If the counter gives such a commit its full score, the score cannot tell the claimed capability from transcription." CLI `--counter <counter.py> --repo <repo> --control <rev>`; exit 0 discriminates, 1 criterion fails, 2 no usable JSON.
- `corpus/QUALITY.md:658`: the obligation is explicitly **"run before the counter is frozen"** — the same pre-freeze placement as kaidoku `corpus/QUALITY.md:77` and `tools/round-34/replay-gate.py:4-9`.
- Ordering: kake `24a1647` (2026-10-22T21:18Z) + `76fac3b` (21:31Z) precede kaidoku `abbd7604` (2026-10-23T11:07Z) by ~14 h and the R34-C2 freeze `c79bbe7b` (2026-10-25T07:13Z) by ~2.6 days. chousa's own cross-lane scan already calls kake's file "the fleet's first shortcut detector" (`chousa-shokunin/.ufo/waves/round-35/w2/ConnectorOverlap.md:36`).
- Difference that keeps kaidoku's work non-duplicative: kake tests **one retained control commit per counter, by exit code, pre-freeze as its QUALITY row requires** and states its own limit (`QUALITY.md:672-675`: "one control tests the leak it exploits"). kaidoku runs **seven registered shortcut classes as generated readers** under the counter's own predicate, plus a required positive control and a shortcut floor, and mutates its own refusal/positive/floor branches. That last part answers kake's stated limit directly — worth saying so in the R34-C2 text.
- **kaidoku cites it: no** (R2/R3: zero sibling names in `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, and zero in `r34b/`).

### 2.2 chousa — same obligation, independently stated, and already citing kaidoku (cite; mutual citation missing)

- `chousa-shokunin/corpus/QUALITY.md:526-540` (row 60): "Every frozen counter names the cheapest gate that scores full marks without doing the work, and the control wave is checked against that line … Before the counter is frozen, write one line naming the cheapest gate…". Sourced from `corpus/lessons/round-42.md` (`2026-10-25T00:14Z`; row text carries "Operator proposal mined from `considerthese/2026-10-23.md` (2026-10-23)").
- Provenance: `chousa-shokunin/considerthese/2026-10-23.md:38` ("The new failure mode is a counter that a shortcut can satisfy, and the lane now hunts for it before data") and `:62-68` (the "cheapest gate" self-improvement proposal). File mtime `2026-10-23 09:23:59 -03` = `12:23Z`, i.e. **76 minutes after** kaidoku's `abbd7604` (`11:07Z`) and ~36 h before chousa's QUALITY row landed. kaidoku holds no copy of that note (`kaidoku-shokunin/considerthese/` does not exist), so this is convergence, not derivation, in either direction.
- chousa's counters are the era's richest single counter family to overlap *in kind*: `CtlLabelKeyed` 82/82 with no fetch (`.ufo/waves/round-29/controls/CtlLabelKeyed/report.md:1,3,97`), the receipt-warmed variant 130/130 (`:97,161`), and the fixture-literal mask 156/156 (`corpus/lessons/round-33.md:81`), with the later self-judgement "the fixture-literal shortcut also scores 156/156, so this is not a clean verification" (`.ufo/reports/round-33/chousa.md:70`).
- **Direction of citation already exists one way**: `chousa-shokunin/.ufo/waves/round-34/w2a2/ConnectorOverlap.md:21` names kaidoku's r34 counter method ("structure-blind size-lookup control met the frozen counter 12/12", citing `kaidoku.md:9` and the M34-4 lesson at `:16`) and `:36` records "the round's one cross-lane regularity, hit independently by kaidoku, mori and kake". `.ufo/waves/round-35/w2/ConnectorOverlap.md:36` repeats it for r34/r35. Nobody reciprocates: **kaidoku cites chousa nowhere** (R2).
- Adjacent caution, not a challenge: that r34 cell also asserts kaidoku's pre-freeze replay discipline "is already operationalized here" (chousa), citing its own `dz-mut`/`dz-decoy` classes. Same family, different object (source-quote counter vs ELF structural counter) — an over-claim only if read as instrument equivalence.

### 2.3 tsukuroi — the second independent lane the class needs (cite)

- `tsukuroi-shokunin/corpus/lessons/round-35.md:36`: "C1 counter VERSION 1 … was met pre-freeze by K08FixtureKeyed (24/24, role encoded in name length)"; `:42` R35-V1-ROLE-LENGTH; `:44` R35-V2-FORCED-SHAPE-CONSTANTS ("forced fixture shapes at a fixed count per fixture are themselves a label"); `.ufo/reports/round-35/tsukuroi.md:13` restates both. `corpus/lessons/round-33.md:42` R33-FIXTURE-LABEL-SHORTCUT is the earlier form (repair counter 24/24 by a fixed distractor label).
- This is the closest *behavioural* twin to R34-C2's class list: "an invariant surface property (name length) encodes the answer" ≈ kaidoku's size/label/digest/slice/order classes. It is also the second lane that tameshi's two-lane admission rule requires before any claim of generality (`tameshi-shokunin/PROVINCE.md:14-16`).
- **kaidoku cites it: no**.

### 2.4 mado — methodological twin (pre-data shortcut battery) (cite)

- `.ufo/reports/round-24/mado.md:28-30`: control wave of 12 seats before data; `CtlC1LabelShortcut` and `CtlC1OffTopic` both met counter v1 (`TARGET_MET`); counter v2 added a claim-anchor clause and scored both 0. 22 artifacts retained under `.ufo/waves/round-24/controls/` (R8).
- `.ufo/reports/round-25/mado.md:9-13`: "Ten shortcut shapes were scored under v4, and the receipts landed at `459dd17f` (07:29:16Z), before the a3w2 data registry `createdAt` (07:31:20Z). None met the target." Also records the structural hazard kaidoku's gate has to avoid: v1–v3 "took the expected table for each generated case from the counter's own line model, so a transcription of that model would meet them by construction".
- Overlap: same intent (score shortcuts before data) at **seat scale with timestamp ordering**; kaidoku does it at **instrument scale with a committed gate, floor and selftest**. Complementary, not duplicative — but the lane's "pre-freeze battery" claim should name mado's earlier seat-scale form and state why a committed instrument is the increment.
- **kaidoku cites it: no**.

### 2.5 kama — the class ledger is kama's open frontier, not kaidoku's (adjacent; contested province)

- `kama-shokunin/corpus/lessons/round-26.md:78`: "control seat `KamaR26CtlAllFalse` scored 12 of 14 with CLI help text printed after an invalid option" — the pre-freeze control call broke the A0 counter, A1 hardened it. `corpus/lessons/round-28.md:48,123`: "generic type conversion … credited as field knowledge".
- `corpus/lessons/round-34.md:89-91,107`: "One still-unimplemented proposal is carried as this lesson's frontier item 1 (the shortcut-class ledger) … a shortcut-class ledger across rounds (echo literals r26, help text r26 A0, type conversion r28 A0, declared-bounds projection r28 A1), with the next class flagged before the next depth round."
- That ledger, if built, is the fleet-level roster of shortcut classes into which R34-C2's seven classes would feed. Two lanes must not independently build it (see § 3). **kaidoku cites it: no.**

### 2.6 mori — calibration counters over prose (adjacent)

- `.ufo/reports/round-34/mori.md:13`: "C2 — calibration (5, tied lowest) … QUALITY 98, the pre-data shortcut battery"; `:27`: "Post-data probe `ef936fb4` skips the two-sample read and rule R3, and also gives `C1=met` … C1 is not verified (honest stop, §9)"; retained controls `.ufo/waves/round-31/controls/shortcut1-grep-list-lines.sh`, `shortcut2-canned-ids.sh`.
- Same family, different object (disk-rate calibration and prose counter). No absorption either way; the shared sentence is "a control that does none of the work met the counter".

### 2.7 tameshi — owns the method; its r34 finding is the freeze-side twin (adjacent; province owner)

- `.ufo/reports/round-34/tameshi.md:17-22`: "The frozen set-blind rule was voidable in both directions by sealed-copy construction (inert head rename validated as must-kill; lethal ride-along validated as must-accept; cosmetic clones unsatisfiable)" — a *pre-frozen rule* defeated by construction, i.e. the same defect one level up from a counter.
- `tameshi-shokunin/PROVINCE.md:5-17` claims the reusable craft and refuses sibling gates. See § 3.

### 2.8 kotoba — fabricated-quote controls (adjacent)

- `.ufo/waves/round-55/controls/C1-shortcut.txt:1`: "C1 shortcut control — fabricated table/entry/SOURCES/Gate quotes"; `corpus/lessons/round-55-verifier-spotcheck.md:83-85,134`: shortcuts D (exit remap 1→2), P (entry preflight), S (argparse shadow) each meet C2; "C2 missed and its predicate is shortcut-reachable". These are *tool-contract* shortcuts (argv/exit), a class kaidoku's gate does not enumerate; if R34-C2 ever claims class completeness, kotoba's D/P/S set is the named counterexample.

## 3. Province flags (belongs to another lane)

| Item | Owner and line | Flag |
|---|---|---|
| Reusable method of honest checks; "a pattern is admitted from evidence in TWO independent lanes before it is claimed general"; "Never edits a sibling's gate code" | `tameshi-shokunin/PROVINCE.md:5-17` | `tools/round-34/replay-gate.py:10` says **"The gate is generic: it runs whatever counter argv the config names"**. Generality is a tameshi-province claim. Kaidoku may hold the gate as its own instrument; a *general* pre-freeze gate needs two-lane evidence (now available: kake + tsukuroi) and tameshi's admission. Recommend: scope the docstring/claim to the ELF structural counter and route the generality question to tameshi. |
| "A census blind spot raises a reusable verification/mutation-testing question" → tameshi (ADJ-07, OUT-010) | `tsukuroi-shokunin/PROVINCE.md:52,130` | Any fleet-wide mutation battery spun out of R34-C2 is tameshi's, not tsukuroi's or kaidoku's. |
| Claim-vs-source verification, citation chaining, own gates | `chousa-shokunin/PROVINCE.md:5-8` | The label-keyed quote counter (`quote-reopen`, `c1-count-v2`) stays chousa's. Kaidoku must not import its counter or restate its numbers as its own evidence. |
| Own gates; publishing operator-gated | `kake-shokunin/PROVINCE.md:17-18` | `lookup_control_check.py` is kake's; cite and contrast, do not copy it into kaidoku as a second instrument of the same shape. |
| Retention gate over *own* committed evidence | `mori-shokunin/PROVINCE.md:125` | Different object entirely — reject as overlap, and do not cite under the shortcut family. |
| Requirement that every gate names its hermetic/mutation arms | `kumitate-shokunin/scripts/*` (per `tameshi-shokunin/PROVINCE.md:8-10`), mirrored by `kumitate.md:54` `round-gate.mjs --round 34 → ROUND_GATE: CLEAN … checks=10` | Structural round-record gate, **not** a counter-vs-shortcut gate — reject (also named by `chousa-shokunin/.ufo/waves/round-34/w2a2/ConnectorOverlap.md:25`). |

## 4. What no sibling holds (kaidoku's actual increment)

Not found in any sibling tree by R1:

1. A **single committed command** that takes a counter + config and (a) runs registered shortcut readers under the counter's own predicate, (b) requires a *registered positive control* to meet the target — so a counter no reader can satisfy can never be CLEAN, (c) refuses CLEAN below a shortcut floor `MIN_SHORTCUTS = 3`, (d) selftests its own refusal/positive/floor branches and requires **every mutant to die** (`replay-gate.py:10-17,31`; `c2-shortcut-gate-counter.py:5-21`; frozen target `selftest_failures 0`, `mutants_killed 3`, red `REPLAY_GATE_REFUSED`, green `REPLAY_GATE_CLEAN`, `.ufo/waves/round-34/r34b/claims.json` claims[0].target).
2. Red/green config pair (`tools/round-34/gate-config-naive.json` red, `gate-config-mini.json` green) over eight 512-byte synthetic fixtures (`mini-fix/fixtures/*.mrec`, 8 files, `stat` 512 B) and nine readers: seven registered shortcut classes (`all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`, `string-scan`, `record-order-replay`, `label-keyed`) plus the `structural` positive control — a *portable* demonstration that the same counter flips verdict on shape vs identity, with `target: 8` in both configs.
3. Branch-level falsification of the gate itself, i.e. `controls/gates/gate-always-clean.py`, `gate-junk-clean.py`, `gate-no-positive-check.py`, `gate-vacuous-no-floor.py` (five receipts under `r34b/controls/`).

Nearest neighbours and why they are not this: kake — one known control commit, exit-code only, no floor, no positive control, no self-mutation; mado — seat-scale, ordering by receipt timestamp, no committed gate; chousa — one-line declaration plus control-wave coverage, not an executable pre-freeze gate; tsukuroi — discovery after the fact (V1 met pre-freeze) then a V2 rebuild, no reusable instrument.

## 5. Rejections (same words, different object)

- `audio-shokunin/corpus/live/r79-boundary/RECEIPTS.md:59` and `reports/round-97/*.md` "pre-freeze": PipeWire stream freeze ("pre-freeze tone → silence, no marker") — audio runtime state, unrelated.
- `.ufo/reports/fleet-index-2026.md:36-37,63,169` "calibration": per-round threshold calibration of audio/game-dev batteries — a measurement-calibration index, not a shortcut gate.
- `chousa-shokunin/corpus/knowledge/claim-verification-r2.md:184` "Frozen replay gate conformance": conformance of a pinned expected-set, not a shortcut replay.
- `kaidoku-shokunin/SKILL.md:1153` and `.ufo/waves/round-33/w1/WFreezeMalformed.md:1-45`: the lane's **own** prior freeze-integrity probes. Not sibling overlap, but the R34-C2 gate's direct ancestor (`replay-gate.py:4` inherits the same "freeze is refused" idiom); the earlier finding — "Malformed/empty inputs can print CLEAN and exit 0" — is exactly why R34-C2 added the positive-control and floor branches. Worth one citation inside the lane.

## 6. Tooling

Nothing installed or upgraded for this seat (no `pacman`, `uv`, `npx`, `cargo` transaction; host-wide pacman pause respected). Tools exercised: `/usr/bin/python3` (reading `claims.json`, line-checking this report), `git -C <lane> log/show` (read-only), `grep`, `stat`, `find`, `ls`, `sed`. No ELF carrier, fixture or reader was executed; no network call was made.

## 7. Limits and unresolved gaps

- Working-tree sweep only; **no git-history search** across the 22 sibling lanes. An earlier, deleted shortcut gate would be missed. kake's "fleet's first shortcut detector" (chousa's wording, `.ufo/waves/round-35/w2/ConnectorOverlap.md:36`) is therefore *first among what I saw*, not first absolutely.
- No `lsp` server answers markdown/JSON/Python-script objects across sibling trees; all claims are text-literal. No semantic reference graph was available to confirm that kake's `lookup_control_check.py` has no in-lane descendants I did not read.
- I did not read the full body of kama's round-34/35/36, kengaku's 28–30, kasegi's 23–24, tabi's 21–23, souji's 20–22 or kagi's 26–28 reports; R1's hit list shows no shortcut-family path in them beyond the rows cited above. Kengaku's earlier "calibration" hits (`round-24/kengaku.md`, `round-25/kengaku.md`) are evaluation-calibration prose, outside R34-C2's object.
- No fleet report dated 2026-10-25 mentions kaidoku: `find .ufo/reports -name '*.md' -newermt '2026-10-25 00:00'` lists **10** reports (`round-68/revenger`, `round-69/kotodama`, `round-22/souji`, `round-22/tabi`, `round-23/kasegi`, `round-28/kagi`, `round-29/kengaku`, `round-35/mado` and two more) and `… | xargs grep -l -i kaidoku` returns empty. So **no sibling has yet scanned this re-dispatch**; chousa's r34/r35 rows cite only the r34 C1 stop.

## 8. Draft text for the lane record (L1 lands it; not written here)

> R34-C2's pre-freeze shortcut-replay gate converges with a fleet regularity held by eight sibling lanes (nine counting kaidoku): a frozen counter can be met by a control that does no work (kake `.ufo/waves/round-34/criteria/lookup_control_check.py`, 2026-10-22; chousa `corpus/QUALITY.md:526`; tsukuroi `corpus/lessons/round-35.md:36,44`; mado `.ufo/reports/round-25/mado.md:9-13`; kama `corpus/lessons/round-26.md:78`; mori `.ufo/reports/round-34/mori.md:13,27`; tameshi `.ufo/reports/round-34/tameshi.md:17-22`; kotoba `corpus/lessons/round-55-verifier-spotcheck.md:83`). Kake's lookup-control criterion states the same pre-freeze obligation one day earlier and its instrument is the nearest prior art; chousa's r34/r35 connector rows already cite this lane's r34 stop. R34-C2's distinct increment is the config-driven battery with a required positive control, a shortcut floor and self-mutation of its own branches, which answers kake's stated limit that one control only tests the leak it exploits. Generality of the gate is a tameshi-province question; the class roster, if consolidated, is kama's open frontier item 1.

## Verdict

`SIBLING_OVERLAP: SUBSTANTIVE_AND_UNCITED` — the counter-met-by-shortcut family is held by eight sibling lanes (nine with kaidoku); kaidoku cites none of them and none of its canonical docs (`SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`) name a sibling; nearest instrument `kake-shokunin/.ufo/waves/round-34/criteria/lookup_control_check.py` (committed `24a1647`/`76fac3b`, 2026-10-22T21:18Z/21:31Z) predates R34-C2's freeze `c79bbe7b` (2026-10-25T07:13Z) by ~2.6 days; chousa already cites kaidoku (`.ufo/waves/round-34/w2a2/ConnectorOverlap.md:21,36`), so the citation is one-way; R34-C2's increment (positive control + shortcut floor + self-mutant selftest + red/green configs + eight fixtures) is not duplicated by any sibling; province flags: gate *generality* belongs to tameshi (`PROVINCE.md:5-17`), the shortcut-class ledger to kama's frontier (`corpus/lessons/round-34.md:107`), the quote-counter instances to chousa and the lookup checker to kake — cite, do not absorb.
