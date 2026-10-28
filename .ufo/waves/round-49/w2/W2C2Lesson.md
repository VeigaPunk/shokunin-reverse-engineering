# W2C2Lesson — round 49 wave 2 (post-landing): attack on `corpus/lessons/round-49.md`

Seat: W2C2Lesson (leaf, read-only on the lane tree). Revision attacked: landing `29883d4ec35a31a8393c4ffb220888c44c0bb022` (lane `main`). Freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` (ancestor of landing: yes; `git log decc5697..29883d4 -- tools/round-49 plans/round-49-claims.md` is empty). Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Every byte read from `git show 29883d4…:<path>`; the worktree was read only for the two untracked files named below. Receipts: `.ufo/waves/round-49/w2/W2C2Lesson/` (`RECEIPTS.md` holds commands, exit codes, sha256s).

## Verdict

**Not clean: amend before the lesson is relied on.** Every number I could re-derive is right (A1–A9 values, the nine-atom counter at the landing and at the freeze, the 16-mutation battery, the 52-case red-before, the registry diff 146→149, the census 15 W04 lines, the three Gate quotes and their sha256s, and all round-48 hashes). But four things are wrong or unresolvable at the landing revision:

1. **M49-1's landed-record pointer is dangling.** `.ufo/waves/round-49/l1/scores/c2-final.json` does not exist at `29883d4` (`git cat-file -t` → MISSING) nor in the worktree. The only file that says "mismatches 0" is `c2-at-landing.json`, which is **untracked** (`git status` `??`). The claim is true (I re-ran it); the cited evidence is not committed.
2. **M49-1's `LOG.md:3437` is a blank line.** The b6f7ca2a amendment sentence is at `LOG.md:3439`.
3. **M49-2's parenthetical "(all exit 0 before the fix)" is false for three of its four files**: `C1ProvCritic` F4 and F5 exit 1 (controls/red by design); `C1RunMut` counter exit is 1 in every scenario, including the ones it calls ACCEPTED (carriers_matched 4, landing bindings absent).
4. **A2's "the two share exactly 8 hex" is false.** The dead and real hashes share a 14-hex prefix and a 21-hex suffix and differ at 4 of 40 positions.

Secondary: a stale present-tense "`--selftest` kills 40 of 75" that was measured on the 47-case pre-freeze draft (the frozen counter has 52 cases); a §3→§2 locator description that contradicts the S145 row; an unsourced "EX_USAGE is 64, not 2". Details below.

## Findings table

Legend: ✔ = resolves / true at `29883d4`; ✘ = does not; ~ = true but imprecise or mis-attributed; n/v = not verifiable from repository or network here.

| # | lesson statement (where) | resolves / true? | evidence (command → exit, sha256/value) |
|---|---|---|---|
| 1 | Freeze `decc5697…` is ONE commit with `plans/round-49-claims.md`, `tools/round-49/**`, `control-fixtures/**`; recorded in `.ufo/waves/round-49/l1/FREEZE` and `LOG.md` (l.4) | ✔ | `git show --stat decc5697` lists plan (+208), `c1-counter.py`, `c2-mismatch.py`, `carriers.json`, control-fixtures; `show 29883d4:.ufo/waves/round-49/l1/FREEZE` = `decc5697…`; `LOG.md:3453` names it. `git log decc5697..29883d4 -- tools/round-49 plans/round-49-claims.md` → empty. |
| 2 | Base `e4f2cfa5…` (l.3) | ✔ | `git cat-file -t` → commit |
| 3 | Counter `c2-mismatch.py` at freeze and landing: `html_norm`, A1–A9, battery 16 (l.17, l.46, M49-1) | ✔ | `c2-R.py` sha256 `9b80b3b0…8595d`… identical to freeze blob `9b80b3b0…` (`c2.F.py`); `html_norm` at line 240 |
| 4 | M49-1 header `corpus/lessons/round-48.md:4` names `0f06251b…` (l.11) | ✔ | `show 29883d4:corpus/lessons/round-48.md` line 4 = "Declared freeze `0f06251bf6a3…`" |
| 5 | M49-1 SCORECARD `## Round 48` amended to `b6f7ca2a…` (A8) (l.11) | ✔ | `SCORECARD.md:3728` heading; line 3730 contains `b6f7ca2a6391964dfdedd477cd560bd42159873a` |
| 6 | M49-1 `LOG.md:3437` (l.11) | ✘ wrong line | `show 29883d4:LOG.md \| awk 'NR==3437'` → empty line; `3438` = "Claims"; `3439` = "Freeze and process disclosure … A8 `b6f7ca2a`". Fix to `LOG.md:3439`. |
| 7 | Atom A1 / battery mutation `A1 swap declared/stale` (l.11) | ✔ | `c2-mismatch.py:606` `les_rep('A1 swap declared/stale', …)`; landing battery `mutations[0].label == 'A1 swap declared/stale'`, `red == ['A1']`, `noop == []`, `ok true` |
| 8 | Freeze reads `mismatches 9` from `.ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json` (l.11) | ✔ | file present; `atoms_total 9, mismatches 9, rev == freeze`. Re-run `c2-F.py --rev decc5697 --freeze decc5697` → exit 1, A1–A9 all `ok false`. |
| 9 | "the landed record reads 0 (`.ufo/waves/round-49/l1/scores/c2-final.json`)" (l.11) | ✘ dangling at `29883d4`; ✔ value | `git cat-file -e 29883d4:.ufo/waves/round-49/l1/scores/c2-final.json` → MISSING. `git ls-tree -r 29883d4 \| grep c2-final` finds only round-36/38/48 files. Worktree has `l1/scores/c2-at-landing.json` (`??`, untracked, `mismatches 0`, `rev 29883d4…`). Re-run at landing: `c2-R.py --rev 29883d4 --freeze decc5697 --battery` → **exit 0**, `atoms_total 9`, `mismatches 0`, `battery.failing []`. Fix: cite a committed file (commit the L1 receipt or cite the battery output). |
| 10 | QUALITY row 88 cited (l.11) | ✔ | `corpus/QUALITY.md` row 88 exists; text names the same atom and mutation |
| 11 | M49-2 "provenance_ok is a prefix test on `/fast/scratch/hyaku/kaidoku-r49/`" (l.12) | ✔ | `c1-counter.py:1184-1192` `output_directory.startswith(PROV_BASE)`, `PROV_BASE='/fast/scratch/hyaku/kaidoku-r49/'`, `..` refused |
| 12 | M49-2 "four new selftest cases" (l.12) | ~ | Frozen `--selftest` = 52 cases (my run, exit 0, failures []). Pre-freeze draft = 47 (`w1/C1CounterMut.md`, `w1/C1SelfTest.md`): delta 5, not 4; plan wave-1 table says "six added". Provenance-named cases at `c1-counter.py:3148,3152,3166,3171` = four. Say which four. |
| 13 | M49-2 red-before: substring test → "52 cases, 2 failures vs 0" (l.12, file `.ufo/waves/round-49/l1/mistakes/m49-2-red-substring-provenance.txt`) | ✔ reproduced | Frozen copy (tree with xpin): `--selftest` → exit 0, `cases 52`, `failures []`. Mutant `return '/kaidoku-r49/' in output_directory`: exit 1, `cases 52`, failures = `provenance under /tmp is refused (prefix, not substring)` and `provenance with the segment inside a lane path is refused`. Exactly the two cases the lesson names. My mutant's bytes sha256 `d38b7a70…1514` ≠ the sha in the landed txt (`fe29bc34…`); the landed mutant file is not committed, so the byte identity is not checkable; behaviour matches. |
| 14 | M49-2 "wave-1 `w1/C1ProvCritic.md` F1–F6, `C1GoldForgery.md`, `C1RunMut.md`, `C1PlanMatch.md` (all exit 0 before the fix)" (l.12) | ✘ parenthetical false for 3 of 4 files | `C1ProvCritic` table: F1, F2, F3, F6 = `0 / 4 / []` landed, counter exit 1 → 0 under the attack; **F4 exit 1** (control, red by design), **F5 exit 1** (`projection_ok` red). `C1GoldForgery`: exit 0 (A13, A5, A11/A12) ✔. `C1RunMut`: "Counter exit is **1** in every scenario including BASE", ACCEPTED rows have exit 1 with carriers_matched 4 (landing bindings absent). `C1PlanMatch`: exit 0 counterfactual ✔. Fix: "F1–F3, F6, GoldForgery exit 0; RunMut accepted with exit 1, carriers_matched 4". |
| 15 | M49-2 "QUALITY row 87" (l.12) | ✔ | row 87 text matches "claim prose the instrument does not implement" |
| 16 | M49-3 "w1/C1ControlsReview.md findings 2–3, w1/C1CounterMut.md F1" (l.13) | ✔ | Finding 2 = CTL-C1-4 is not round-44 receipts; Finding 3 = CTL-C1-5 vacuous; C1CounterMut F1 = "CTL-C1-5 cannot fail" |
| 17 | M49-3 "CTL-C1-4 now plants the committed round-44 receipts verbatim and asserts `run_provenance_ok`" (l.13) | ✔ | `c1-controls.py:757-781` `control_c4` copies `corpus/evidence/round-44/c1/<id>/after.json` verbatim, `expect.failing_any ['run_provenance_ok']`. Landed `controls/c4/counter.json`: `failing ['v1be:run_provenance_ok', 'v1le:…', 'v2be:…', 'v2le:…']`, exit 1 ✔. |
| 18 | M49-3 "CTL-C1-5 is retired from the default set and the plan says so" (l.13) | ✔ | `controls/summary.json` lists CTL-C1-0..4 and POS only; plan wave-1 table line "CTL-C1-5 retired from the default set" |
| 19 | M49-3 "frozen_tables_valid is set true before any check (w1/C1SelfTest.md)" (l.13) | ✔ | `c1-counter.py:2014` `res['frozen_tables_valid'] = True`, before the carriers.json parse checks that follow |
| 20 | M49-3 "`--selftest` kills 40 of 75 single-point mutants (w1/C1CounterMut.md)" (l.13 and "Routed" l.40) | ✘ stale for the frozen counter | `C1CounterMut.md` measured the **draft** (`exit 0, 47 cases`, sha `d6d70cb7…`); the frozen counter has 52 cases (item 13). The 40/75 figure is not a measurement of `tools/round-49/c1-counter.py` at R. Say "on the pre-freeze 47-case draft". |
| 21 | "Gate": S138 `teaches` / row S138 `used-by` old→new; kept `mined` (l.21) | ✔ | `diff 29883d4^ 29883d4` of SOURCES: only S138 and S139 lines changed, each by appending `, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` to `used-by`. Status/opened cells unchanged. |
| 22 | S138 "22 of 22 oracle members re-fetched, mismatch 0"; tree page 200,946 B (l.21) | ✔ at access, ~ as a pin | `w1/C1S138Reopen.md` F5 `mismatch 0`, F0 sha. Live refetch today: tree page **200,967 B** (dynamic page, same `<title>`). Bytes are not a reproducible pin. |
| 23 | S138 listing element `"name": "squashfs_v1.0_be.bin_extract"` (l.21) | ✔ value, ~ formatting | live `contents/…/squashfs_v1/big_endian/__output__?ref=26.6.4` → HTTP 200, element `"name":"squashfs_v1.0_be.bin_extract"` (compact JSON; the lesson's quote adds a space). `<title>` "unblob/tests/integration/filesystem/squashfs at 26.6.4 · onekey-sec/unblob · GitHub" ✔ live. |
| 24 | S139: release JSON `"name": "Squashfs tools 4.7.5"`, `published_at 2026-03-01T23:05:47Z`; `unsquashfs version 4.7.5 (2026/03/01)`; 398,943 B round-44 vs 361,752 B today (l.22) | ✔ (value); ~ (today's byte count) | live `api.github.com/…/releases/tags/4.7.5` → name and published_at match. Local `unsquashfs -version` → `unsquashfs version 4.7.5 (2026/03/01)`. Round-44 row (`.ufo/waves/round-44/w1/R44SrcOracle.md:255`) = 398943 B ✔. Releases page live today = **361,757 B** (lesson 361,752). Dynamic; fine, but say so. |
| 25 | S147 SEP Popper: sha256 `2c2d48c6…207`, 118,135 B, quote 21 words under `2. Backdrop to Popper's Thought` (l.23) | ✔ | snapshot `corpus/evidence/round-49/c2/popper.html` sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`, 118135 B; normalised quote found at offset 12284; `2. Backdrop` heading at 8872, `3. The Problem of Demarcation` heading at 12986; no numbered heading between. Words: 21 ✔. Live refetch sha identical. |
| 26 | S147 "supersedes S145 … locator corrected from §3 to §2" (l.23) | ✘ mis-described | S145 row (`corpus/SOURCES.md` line 151) locator is `2. The Problem of Demarcation`: the **number** is 2, the **title** is §3's. The correction is the heading title, not "§3 to §2". Line 27 says this correctly; line 23 and the S147 row ("not under §3 as S145's locator said") do not. |
| 27 | S148 sysexits.h.3head: sha256 `d9db4b96…340`, 12,725 B, `#define EX_USAGE 64 /* command line usage error */` 9 words (l.24) | ✔ | snapshot sha256 `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340`, 12725 B, quote found; live refetch identical |
| 28 | S149 FreeBSD: sha256 `1fc793a2…5dbf`, 59,251 B, `EX_USAGE (64) The command was used incorrectly` 7 words; reject (l.25) | ✔ | snapshot sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`, 59251 B, quote found; live identical; registry status `rejected`, tier C |
| 29 | "`EX_USAGE` is 64, not 2" (l.24) | ~ unsourced contrast | No lane text at `29883d4` says `EX_USAGE` is 2. The only `EX_USAGE is 2` string is the C2 counter's own mutation (`c2-mismatch.py:636`). Drop "not 2" or say what it refutes. |
| 30 | S146 URL "still returns 404 (196-byte body, sha256 `80c3fe2a…f880`)" (l.27) | ✔ live | `curl` → HTTP 404, 196 B, sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880` (today) |
| 31 | S145 and S146 "byte-identical to the base" (l.29) | ✔ | `grep '^ *\| S145 '` and `'^ *\| S146 '` md5 at base == at landing (`ae43a275…`, `1c8f1b7b…`) |
| 32 | Registry 146→149 by `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`; new rows S147, S148 mined, S149 rejected (l.29) | ✔ | base 146, landing 149; `git diff e4f2cfa 29883d4 -- corpus/SOURCES.md` → 8 insertions, 2 deletions, all on S138/S139/appended rows S147–S149 and two search-log entries |
| 33 | "the only existing rows touched are S138 and S139 … No status or recheck cell … changed" (l.29) | ✔ | the diff hunks touch only lines for S138 and S139 (the `used-by` insertion); no other existing row |
| 34 | Search-log entries for round 48 (late) and round 49, counts "identified/screened/included/excluded" and "rows 144→146", "146→149" (l.56, atom A8) | ✔ | `corpus/SOURCES.md` `## Search log`: entries present; 2 + 3 identified; rows consistent with registry |
| 35 | Census start: exit 0, 15 `W04` lines S033…S142, final `kaidoku ok …`, 146 rows (l.34) | ✔ | `show 29883d4:.ufo/waves/round-49/l1/sources-census-start.txt`: 15 W04 lines (S033 S047 S054 S062 S069 S083 S090 S092 S102 S112 S117 S119 S123 S138 S142), `ok` line, `exit=0`; base registry 146 rows |
| 36 | Census end: "see that file … 149 rows after landing" (l.35) | ✔ | `…sources-census-end.txt` ends `exit=0`; landing registry 149 rows |
| 37 | Assimilation: `considerthese` and `merge/kaidoku` absent at base (l.28) | ✔ | `git ls-tree e4f2cfa -- considerthese merge/kaidoku` → 0 entries each; worktree `considerthese` absent |
| 38 | Package `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` has zero `squashfs_v1`/`squashfs_v2` hits (l.28) | ✔ | path exists; `grep -rIc -E 'squashfs_v1\|squashfs_v2\|SquashFS v1\|SquashFS v2'` → total 0. (ScoutAssimilation's 14 filename/title matches are on other tokens; not in conflict.) |
| 39 | Round-48 closure routed defects 5 and 6 (census2.json binds `paths`; record2.py imports `tools/round-46/gate.py` from worktree) (l.39) | ✔ | closure lines 134–135; `census2.json` keys `rule, paths, named_but_absent, per_claims_file`; `record2.py:36-37` `sys.path.insert(… "round-46"); import gate` |
| 40 | `frozen_tables_valid` tautology, `--selftest` 40/75, six doc bindings presence checks, relabelled replay 4/4 (l.40) | ✔ except 40/75 (item 20) | `c1-counter.py:2014`; `C1DocBindings.md` "presence checks"; plan states the relabelled-replay limit |
| 41 | "further open items … 28 still open" (rounds 46–48) and "ten more … beyond A1–A9" (l.41) | ✔ | `ScoutPriorClosures.md`: "10 are fixed, 1 is declined, 28 are still open"; `C2SelfAssess.md`: "ten places beyond atoms A1–A9" |
| 42 | QUALITY row 80 and "the receipts replay at the freeze revision (`controls/summary.json`)" (l.42) | ✔ (summary); replay n/v | `summary.json`: `counter_sha256 ac83715b…` = frozen `c1-counter.py` blob; `kill_rule_fires false`, `failures []`. I did not re-run the controls. |
| 43 | M49-1 "found by the non-author closure (`corpus/lessons/round-48-verifier-spotcheck.md`, calibration row)" (l.11) | ✔ | closure line 107 calibration row quotes `corpus/lessons/round-48.md:4` declares `0f06251b…` |
| 44 | Stale header: round-48 lesson header `0f06251b…` (A1 stale) and A1 declared `b6f7ca2a…` (l.48) | ✔ | round-48.md line 4 = `0f06251b…`; SCORECARD `## Round 48` and LOG 3439 = `b6f7ca2a…` |
| 45 | A1 "amendment A4 of eight; declared freeze is b6f7ca2a (A8)" (l.56) | ✔ | `LOG.md:3439`: "A1 dc73587a, A2 ac02a79f, A3 f3a7afc4, A4 0f06251b, A5 04f9d4b7, A6 24b4e5cb, A7 c8d7da55, A8 b6f7ca2a" |
| 46 | A2 `663f30ee7516942a0120e7de68fe88356e680822` is not a commit; real is `663f30ee751694fb0970e7de68fe88356e680822` (l.49, l.56) | ✔ | `git cat-file -t` dead → fatal (no object); real → `commit`; fleet report `.ufo/reports/round-48/kaidoku.md` line 13 cites the dead one; `r48-w1-results.json` `pinned_rev` = real |
| 47 | A2 "the two share exactly 8 hex" (l.56) | ✘ | dead vs real: common **prefix 14** hex (`663f30ee751694`), common **suffix 21** hex (`e7de68fe88356e680822`), 4 differing positions of 40. "8" is only the abbreviation's leading run. Fix. |
| 48 | A3 LOG counts: `2e785632` at 3440,3441,3445; `33f65a91` at 3440,3441,3444; `c093e798` at 3440,3441,3445 (l.50) | ✔ | `grep -n` on `show 29883d4:LOG.md` (lines 3440, 3441, 3444/3445) |
| 49 | A3 unnamed `577a02a5`, `8847042a`, `7fe11332` named nowhere in LOG.md (l.50) | ✔ | `grep` on landing LOG.md → no match; all three are commits (`cat-file -t` commit) |
| 50 | A3 prose: "the closure cited `2e785632` at `LOG.md:3445` alone" (l.56) | ~ mis-attributed | closure line 17: "`2e785632` commit is at LOG.md:3445, outside the cited 3442–3444" — it is the fleet report's range the closure attacked, not an "alone" claim. The lesson's A3 digits themselves are right. |
| 51 | A3 "`7fe11332` (a real commit the fleet report cites with LOG.md:3436-3439)" (l.56) | ✔ | fleet report line 21 cites `7fe11332…` with `LOG.md:3436-3439` |
| 52 | A4 seats 75, reports 72, missing C1Battery, C1Meaning, ScribeReportNumbers (l.51) | ✔ | `r48-w1-results.json`: `"seats": 75`, 75 results; closure line 136: "72/75 seats have report artifacts, not 73; missing C1Meaning, C1Battery and ScribeReportNumbers" |
| 53 | A4 per-seat causes: C1Meaning only `receipt.json` (`frozen_worktree_dirty`); `C1Battery-2/` is a receipt directory; ScribeReportNumbers nothing (l.56) | ✔ | `.ufo/waves/round-48/w1/C1Meaning/receipt.json` only; `w1/C1Battery-2/receipt.json`; no `ScribeReportNumbers` path at `29883d4`; closure line 136 gives `frozen_worktree_dirty` for C1Meaning |
| 54 | A5 digests: c1 raw `6320c5d2…`, stripped `3cc2d72d…`; c2 raw `d1bb87d8…`, stripped `c30628ae…` (l.52, l.56) | ✔ exact | `sha256(show 29883d4:.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json)` = `6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e`; with trailing `\n` stripped = `3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77`. c2 file: raw `d1bb87d8…914`, stripped `c30628ae…e8`. All four match. |
| 55 | A6 row S147, A7 row S148 (l.53–54) | ✔ | rows present, see items 25–29 |
| 56 | A9 "calibration line in `SCORECARD.md` `## Record corrections — round 49`" (l.56) | ✔ | heading present; atom A9 green at landing (battery run, `atoms.A9.ok true`) |
| 57 | M49-1 "captured-by `none`", "atom A1 … plus its battery mutation" (l.11) | ✔ (as described) | consistent with `c2-mismatch.py` |
| 58 | "Cross-domain evidence: none … `w1/ConnSibling.md` found no SquashFS/sasquatch/unblob ground in any sibling PROVINCE.md or corpus/knowledge/" (l.58) | ~ overstated | `ConnSibling.md` A1 records unblob hits in game-dev-3d `corpus/knowledge/rea.md:36-39` (host tool presence: binwalk 3.1.0, unblob 26.6.4) and revenger firmware hits. Say "no SquashFS/sasquatch ground; unblob mentions are tool-presence only". |
| 59 | "tsukuroi ADJ-06 remains open" (l.58) | ✔ | fleet `.ufo/reports/round-1/tsukuroi.md:135` still declares ADJ-06 open; `.ufo/l0-questions.md:42` |
| 60 | "Spot-check by a non-author … is the hyaku closure's" (l.30) | n/v | not in this repository's lane tree; not checked |
| 61 | "wave 1 (48 seats)" (l.4) | ✔ | `.ufo/waves/round-49/w1-dispatch.json` `counts.spawn 48` |
| 62 | Freeze `decc5697…` introduced the plan and tools (not in `14936cb9`) (implied by l.4) | ✔ | `cat-file -e 14936cb9:plans/round-49-claims.md` → absent; the freeze commit adds it |

## Counter runs made by this seat (exit codes are semantic)

| command (LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin, R=29883d4…, F=decc5697…) | exit | result |
|---|---|---|
| `GIT_NO_REPLACE_OBJECTS=1 python3 -I -B c2-mismatch.py --root $LANE --rev $R --freeze $F --battery` (counter bytes = landing blob) | 0 | `atoms_total 9`, all `ok`, `mismatches 0`, `battery.failing []`, 16 mutations each `red == [own atom]`, `noop == []`, do-nothing red 9; sha256 of stdout `0cad6d5c…f86` |
| same, `--rev $F` | 1 | every atom `ok false`; A8 "round 48: 0 matching search-log entries, want 1" (the lesson's entry is absent at freeze) — stdout sha256 `7aa900e1…`, file `c2-F.json` |
| `python3 -I -B treeR/tools/round-49/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0>` (frozen copy, xpin placed in scratch tree) | 0 | `cases 52`, `failures []`; stdout sha256 `167b1406…`. No default `--selftest` run on the lane. |
| same, substring mutant | 1 | `cases 52`, failures = 2 provenance cases; sha256 `eeb11371…` |

Not run: the C1 data run (forbidden), the full `--selftest` mutation harness (75 mutants), the full controls replay, `c1-counter.py` main measurement at R (that is the C1 seat's job).

## Required fixes (for L1; non-frozen text only)

1. Replace the M49-1 `c2-final.json` pointer with a committed artifact (commit the landing C2 receipt or cite the committed battery output). Until then the "landed record" is an untracked file.
2. `LOG.md:3437` → `LOG.md:3439` (M49-1).
3. M49-2: say which wave-1 files exit 0 (F1–F3, F6, GoldForgery; PlanMatch's counterfactual) and that F4/F5 are red controls and RunMut is exit 1 with carriers_matched 4.
4. A2: "the two share exactly 8 hex" → "share a 14-hex prefix and a 21-hex suffix, differing at 4 of 40 positions; the fleet abbreviation `663f30ee…822` keeps the 8-hex lead".
5. "`--selftest` kills 40 of 75" (l.13, l.40): qualify as the 47-case pre-freeze draft, or re-measure the frozen counter.
6. M49-2 "four new selftest cases": name the four (`c1-counter.py:3148,3152,3166,3171`) or state 5 added (47→52).
7. S145→S147 locator: "heading title corrected from `The Problem of Demarcation` to `2. Backdrop to Popper's Thought`" (line 23 and the S147 row).
8. Drop or source "EX_USAGE is 64, not 2" (l.24).
9. A3 "closure cited … alone": reword to what the closure says (the fleet report's range 3442–3444 excludes 3445 while the commit is also at 3440/3441).
10. ConnSibling sentence (l.58): "no SquashFS/sasquatch ground; unblob mentions are tool-presence only".

## Limits

- Snapshot-pinned Gate quotes were checked against the committed snapshots and re-fetched live today; the live pages match the pinned sha256 for SEP, man7 3head, FreeBSD, and the 404 URL. The S138 tree and S139 releases pages are dynamic; their byte counts drift (S138 200,946 → 200,967; S139 361,752 → 361,757). I did not pin them.
- The C1 selftest is run from a scratch copy of the frozen counter under a scratch tree that holds only `tools/round-27/xpin-attribute.mjs` from `29883d4`; the frozen counter's bytes are unchanged (blob sha256 `ac83715b…`).
- I did not patch or commit anything. Scratch removed after receipts were copied to `.ufo/waves/round-49/w2/W2C2Lesson/`.

Tooling: none installed. Commands: `git` (read-only: `show`, `ls-tree`, `cat-file`, `diff`, `log`, `grep`, `status`, `check-ignore`), `python3 -I -B`, `curl`, `unsquashfs -version`, `sha256sum`, `md5sum`.
