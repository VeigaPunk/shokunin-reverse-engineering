# PL-2 — seat report (chain c2, planner), wave `arc3-loop1-round4`

Seat PL-2 · chain c2 · role **planner** · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
HEAD `015e1bab914713568f339fd53999bc180459cc40` (unchanged throughout; no git
mutation issued). Lane: devin (`devin/deepseek-v4-1-flash-max`), the declared
fallback recorded in `claims-frozen.md:11-15` after the hyper lane returned 402
out-of-credits on all 48 seats (recorded with cause, not a lane signal).

Task as frozen: plan C2 (PROVINCE staleness census) — method for checking every
Frontier bullet + Core/surface-summary claim against admitted corpus state;
repair form (same-line, line-count held, census-conformant wording — PROVINCE
is a census-scoped file); adjudication rules. Artifact
`claims/c2/PL-2/plan.md`.

Writes by this seat: this report + `claims/c2/PL-2/**` only. The real
`PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `corpus/**`, `.ufo/gates/**` and
every custody path were only ever **read** (hash/stat/parse; the crashpad core
probe read a `/var/tmp` dump of a recorded core, never a custody path). Scratch
under `/var/tmp/pl2-r4` (never `/tmp` — standing EDQUOT rule). No installs by
this seat (C1's vyper venv was polled read-only; EX-02's receipt is in place).

## 1. Work performed (evidence pointers)

All artifacts under `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/`; all
identities re-derived after the final revision (rule #14, §6).

| artifact | what | sha256 |
|---|---|---|
| `plan.md` (363 lines) | the deliverable: method, per-item census table, adjudication rules, repair index, measurement table, attacks, residuals, landing recipe | `0730737bbca86dd5175f8ed0882b2713ab7eb8a11b5e6cafdd935ba7d6fe4aad` |
| `gen-and-measure.py` | generator + measurement harness: rebuilds every patch text from the real bytes, applies to fresh scratch trees, runs the census, RV-4's differ, VZ-2's instrument, the residual/token sweep and the planted-pin control | `125be8409f4c2f3bf14906877591d8b59b6016be990555649fe6dc6adb8140e4` |
| `candidate-repairs.patch.md` | **recommended voice**: 21 hunks (18 Frontier + 3 Core-sweep) | `0ccb7f2dfb3e2ee5c054a7a1df6466380afcfb91f1962b9f1f9c0f68976f68f9` |
| `candidate-with-s5.patch.md` | 21 + the `:18` pointer refresh | `0c28db8f7e95f23d803bcbfcfc78014c22d4057f7185da12055caa50aec9105b` |
| `candidate-coupled-vyper.patch.md` | 21 + the Vyper-naming coupling hunk (true only with C1's entry same-commit) | `a98df66c8274ddd3eaeec069e9adcd06b9a4bd6e9a36ec86d232ab5ab5b90199` |
| `corpus-erratum-coupled.patch.md` | append-only corpus erratum coupled to hunk C46 | `12a7ceb3a62a526c9a04c33c114da1e2e466797f7d649d25723ab910e1832ca2` |
| `evidence/measure-run.txt` | the harness transcript quoted in plan.md §4 | (copied; see dir) |
| `evidence/residual-and-token-sweep.txt` | 9 stale literals gone; zero tokens in new text | |
| `evidence/differ-vs-baseline.txt` | RV-4 differ output, 0 new/removed/moved | |
| `evidence/vz2-phantom-rows.txt` | VZ-2's instrument on baseline + 3 variants | |
| `evidence/pointer-table-check.txt` | the 2 PROVINCE pointer-table predicates, HIT on all variants | |
| `evidence/doctor-6{4,5,7}0.txt` | live catalog re-derivations (S2/S3/S4) | |
| `evidence/crashpad-probe-ev813eed97.json` | this seat's `inspect-recorded-crash` run on the 17.6 MB organic core | |
| `evidence/rv4-harness-run.log` | the delivered patch text through RV-4's independent harness: 21/21 hunks, CONFORMANT | `5e9057ea0d3a83c30ab74a0f92beefdf547c9ebf310cdfd339afdb192cafaa1e` |

**Method built (plan.md §1).** Two units, explicitly separated because this
wave's instruments conflate them: (1) *gate unit* — the census instrument
grades version/pin/pointer loci and is structurally blind to prose (RV-4 §4.2;
re-derived here: the EVM bullet yields zero detections on both sides of any
repair); (2) *staleness unit* — prose-vs-corpus truth, adjudicated per item.
Constraints derived and measured: the repaired regions are UNDECLARED in the
scope table (a token there → `undeclared=1` FAIL, proven live by this seat's
planted-pin control); line count must stay 162 (an insertion trips the `:119`
DATED marker); bare versions are the gate's **silent** class, hence the
explicit token sweep.

**Measurements taken first-hand this sitting** (transcripts in `evidence/`):

- baseline census `PASS 0/0/0/0`; PROVINCE 162 lines, `d075a3c6…` (real tree,
  re-derived at close).
- three variant trees built and measured: all **162 lines**, all **PASS
  0/0/0/0**, all **differ CLEAN** (16/16 assertions, 0 new/removed/moved loci).
- residual sweep: all 9 stale literals gone; token sweep empty; planted-pin
  control **FAIL undeclared=1**.
- live re-derivations: `rea doctor` 6.7.0 → 207/153/`af39310c`; 6.5.0 →
  207/153/`805433f1`; 6.4.0 → 170/127/`25802f6d` (S2/S3/S4 current);
  `ls Ghidra/Features | wc -l` = 34 (C46 stale); `command -v` sweep (C62:
  7z/xxd/radare2/strace/upx present, all installed 2026-10-13 13:52);
  pacman cache 1350 (C50 stale); `config.toml` 3570 lines, pin at `:3546`
  (S5 pointer dead, `:3298` = `max_context_size`).
- **new evidence for F2**: PID 1857 `chrome_crashpad_handler` dumps 17,608,704 B
  (< 33,554,432 cap) and `inspect-recorded-crash` completed on it — exit 0,
  `ev_813eed97569f0cd3d76c41ac30d1ff8268b8ca3bed12e22c308aaa72f9770e8`, 3
  threads, decoded subject sha `0d444cf0…`. The bullet's universal ("all
  organic cores exceed the cap") is false.
- the delivered patch text run through **RV-4's own** `apply-and-census.sh` +
  `prose-apply.py`: 21/21 hunks applied by content match, patched sha
  `8cb86b35…` (identical to this seat's own tree), verdict **CONFORMANT**.

**Chain artifacts read and reconciled** (not trusted): EX-14's two patch texts,
EX-15's `adjudications.md` (A1-A6/B1-B2/C1/D1-D5 + its §4 measurements),
EX-16's interplay work, RV-4's report and instruments, VZ-2's
`province-staleness-census.py` + evidence, SC-2's records drafts. Where this
plan disagrees with EX-15, the disagreement is recorded with the ruling (plan.md
§5 A4/A5) rather than smoothed.

## 2. Proposed changes (patch-text paths)

- **`claims/c2/PL-2/candidate-repairs.patch.md`** — recommended. 21 same-line
  hunks: F1b (`:83`), F2 (`:84-86`), F3 (`:88`), F5a/F5b/F5c (`:91-93`),
  R2 (`:139-144`), X1/X2/X3 (`:157-160`), and the Core sweep C46 (`:46`), C50
  (`:50`), C62 (`:62`). Parent applies; seats never write PROVINCE.
- **`claims/c2/PL-2/candidate-with-s5.patch.md`** — take this voice if the
  parent prefers to refresh the `:18` pointer now (EX-15 A1-repair semantics).
- **`claims/c2/PL-2/candidate-coupled-vyper.patch.md`** — take **only** if C1's
  arc3-r4 vyper corpus entry lands in the same commit.
- **`claims/c2/PL-2/corpus-erratum-coupled.patch.md`** — must land in the same
  commit as hunk C46 (the corpus entry is where the `35` came from; the row is
  otherwise self-contradictory with its own list).
- **No other proposed changes.** No seat wrote the real target.

**One landing warning (the plan's headline):** EX-14's and EX-15's rival EVM
wordings assert `(Core, arc3-r1/r3)` / `held` — a promotion both arc3 entries
disclaim ("RESULT-class, no Core promotion") and that no `LOG.md` entry
supports. This plan's wording is promotion-neutral ("recovered K/K (arc3-r1/r3,
RESULT-class)"); RV-4 §4.1/§4.1b sustained the defect and VZ-2's re-apply
concurs.

## 3. Before → after measurement for chain c2's claim

Chain claim: every Frontier bullet and surface-summary claim census-checked;
every stale item repaired same-line (line count held) or adjudicated NO-CHANGE
with cause; census PASS at the records commit.

| measurement | before (HEAD) | after (candidate-repairs) |
|---|---|---|
| PROVINCE.md lines | 162 | **162 (held)** |
| PROVINCE.md sha256 | `d075a3c6…` | `8cb86b35…` |
| census instrument | `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0 | **`PASS (0/0/0/0)` exit 0** |
| locus differ vs baseline | — | **CLEAN** (16 assertions both sides; 0 new/removed/moved) |
| stale literals (the wave's three censuses' union) | 9 present | **0 present** |
| new version/pin/pointer tokens | — | **0** (token sweep empty) |
| pointer-table PROVINCE predicates | 2 HIT | 2 HIT |
| SHONEN `shonen-province-range` predicate | HIT | HIT |
| planted-pin control | — | **FAIL undeclared=1** (gate live, not vacuous) |

Per-item outcome (plan.md §2): **9 items repaired** (F1b, F2/F2b, F3, F5b, R2,
X1, X2, C46, C50, C62 as rows), **2 adjudicated NO-CHANGE** (S5 with a measured
refresh variant; F5c's Vyper deferral with a measured coupling variant), 4
items re-checked current (S1-S4, S6, S7, R1, R3-R6, F1a, F4, F5a, F5c, plus
Core rows 47/48/52), and 2 coupling rules declared. **On VZ-2's instrument:**
its SUMMARY is corpus-keyed and invariant on patched trees (measured — `stale=9`
on every variant); its meaningful signal is the phantom list, which flips from
`[]` to exactly the repaired anchors. The claim's "census-checked" half is
therefore reviewer-enforced; the round record should say so (plan.md §1.2, §6).

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the repair set moves the gate" | **refuted** — PASS/CLEAN on all three variants; 16/16 assertions unchanged; agrees with RV-4's five-capture byte-identity result |
| A2 | "the gate is vacuous (a blind run would PASS anyway)" | **refuted** — planted-pin control FAILs `undeclared=1`; RV-4's plants A/B/D/F reproduce four further caught classes |
| A3 | "the gate also covers bare-version tokens" | **refuted** — RV-4 plant C reads PASS; hence the explicit token sweep |
| A4 | "EX-15's NO-CHANGE on JEB is right" | **partially sustained, overruled** — the operative claim holds and the cause is sound, but `r2-provider-capability-matrix.md:99` falsifies "unprobed" and the fix is one same-line word at zero gate cost. Ruling: repair |
| A5 | "EX-15's D3 NO-CHANGE on 1556 is right" | **partially sustained, overruled** — cache churn is real, but the row presents 1556 as the live corpus and live reads 1350; the "as of" repair keeps the receipted number and states the live one. Ruling: repair |
| A6 | "VZ-2's `adjudicated` on F2 settles the bullet" | **refuted** — that adjudication is about the exemplar pointer (waybar rows now `missing`); this plan's finding is a different falsified universal, now measured false by this seat's own probe (17.6 MB organic core, exit 0, `ev_813eed97…`) |
| A7 | "the Vyper half of F5b can be repaired now" | **refuted at HEAD** — corpus holds 83 files, no arc3-r4 entry; the base variant is true without C1, the naming variant is the coupled form |
| A8 | "the `35`-features fix is safe alone" | **refuted** — the number originates in the corpus entry's own claim line; the erratum is emitted as a coupled landing |
| A9 | "S5's dead pointer is caught by the census" | **refuted** — `classify()` collects pointer loci only when a block carries no `@`-pin, so `ptr_check` never runs on `:18` (EX-15's direct call reproduces the staleness; unreached) |
| A10 | "the delivered patch text cannot be applied by the parent's tooling" | **refuted** — RV-4's independent harness: 21/21 hunks applied by content match, CONFORMANT, patched sha identical to this seat's tree |

## 5. Blockers, if any

None that block the deliverable. Named residuals (plan.md §6): (1) no
prose-truth instrument exists in this wave — the "census-checked" half is
reviewer-enforced and the round report must say so; (2) S5's dead pointer is
gate-invisible by construction — variant measured, NO-CHANGE cause text is
EX-15's A1-nocause; (3) row 49's host-asar inventory gained new files since the
r1 scan (chatgpt, `obsidian.asar`) — deferred with cause; (4) the two coupling
constraints are landing-order requirements with both voices measured;
(5) seat poll at close: 47/48 reports, all c2 claim dirs read. Custody paths
untouched (read-only); no git mutations; `/tmp` never used.

## 6. Identity discipline (rule #14)

Re-derived **after** the last revision of each object, at 2026-10-19
11:28–11:31 -03:00: `plan.md` `0730737b…` (363 lines, after the final §8
timestamp correction);
`gen-and-measure.py` `125be840…`; the four patch texts as tabled in §1; the
three candidate trees `8cb86b35…`/`9e5dab4d…`/`6fd9059f…`; the harness log
`5e9057ea…` (re-executed after the last wording edit). The real tree's scoped
files were re-hashed at close and are unchanged: `PROVINCE.md` `d075a3c6…`,
`SKILL.md` `5eec51c0…`, `SCORECARD.md` `21042196…`, instrument `d0772ce8…` —
this seat wrote none of them. No artifact records its own digest inline.
